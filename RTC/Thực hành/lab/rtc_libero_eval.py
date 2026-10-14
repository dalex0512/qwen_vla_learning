"""Đánh giá một policy chunk (SmolVLA, Pi0, Pi0.5) trên LIBERO với ĐỘ TRỄ GIẢ LẬP.

Mô phỏng LIBERO đứng chờ mô hình, nên bình thường không có độ trễ. Script này giả lập đúng
cách paper 1 làm trên Kinetix: chunk mới được tính từ quan sát lúc bắt đầu hỏi, nhưng chỉ
được dùng sau `delay` bước; trong lúc đó robot chạy tiếp chunk cũ. Mọi thứ khác (môi trường,
tiền/hậu xử lý, đếm thành công, video) là của `lerobot-eval`, chỉ policy được bọc lại.

Tham số riêng (phần còn lại chuyển nguyên cho lerobot-eval):
  --lab.mode       naive | rtc | rtc_full | trained
                   rtc = RTC lúc suy luận của LeRobot; rtc_full = gradient qua mô hình (đúng paper 1);
                   trained = RTC lúc huấn luyện (paper 2), cần checkpoint train với patch
                   smolvla_training_rtc.patch và --policy.rtc_training_max_delay > 0
  --lab.delay      d, số bước trễ giả lập (LIBERO 20 Hz: 1 bước = 50 ms)
  --lab.s          số hành động chạy của mỗi chunk trước khi hỏi chunk mới (cần d <= s <= H - d)
  --lab.execution_horizon, --lab.beta, --lab.schedule   tham số RTCConfig
  --seed           (của lerobot-eval, mặc định 1000) đổi để chạy nhiều seed; tong_hop_libero.py gộp theo cấu hình
  --lab.stats      file JSON ghi độ giật và thời gian gọi mô hình (mặc định: <output_dir>/rtc_lab_stats.json)

Ví dụ:
  python rtc_libero_eval.py --lab.mode=rtc --lab.delay=4 --lab.s=10 \
    --policy.path=outputs/train/obj_bs16x4_21k/checkpoints/021000/pretrained_model \
    --env.type=libero --env.task=libero_object --env.task_ids='[0,1,2]' \
    --eval.batch_size=1 --eval.n_episodes=5 --output_dir=outputs/rtc_lab/rtc_d4
"""
import argparse
import json
import os
import sys
import time

import torch

pre = argparse.ArgumentParser(add_help=False)
pre.add_argument("--lab.mode", dest="mode", default="naive", choices=["naive", "rtc", "rtc_full", "trained"])
pre.add_argument("--lab.delay", dest="delay", type=int, default=0)
pre.add_argument("--lab.s", dest="s", type=int, default=10)
pre.add_argument("--lab.execution_horizon", dest="eh", type=int, default=10)
pre.add_argument("--lab.beta", dest="beta", type=float, default=10.0)
pre.add_argument("--lab.schedule", dest="schedule", default="EXP", choices=["ZEROS", "ONES", "LINEAR", "EXP"])
pre.add_argument("--lab.stats", dest="stats", default=None)
LAB, rest = pre.parse_known_args()
if LAB.stats is None:                      # mặc định: ghi cạnh eval_info.json trong --output_dir
    for a in rest:
        if a.startswith("--output_dir="):
            LAB.stats = os.path.join(a.split("=", 1)[1], "rtc_lab_stats.json")
sys.argv = [sys.argv[0]] + rest

from lerobot.configs import RTCAttentionSchedule  # noqa: E402
from lerobot.policies.rtc import RTCConfig  # noqa: E402
from lerobot.scripts import lerobot_eval as E  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtc_full_jacobian import FullJacobianRTC  # noqa: E402

SEED = next((a.split("=", 1)[1] for a in rest if a.startswith("--seed=")), "1000")   # mặc định của lerobot-eval
POLICY = next((a.split("=", 1)[1] for a in rest if a.startswith("--policy.path=")), "")
STATS = {"lab": vars(LAB), "seed": SEED, "policy": POLICY, "episodes": [], "predict_s": []}


class DelayedChunk:
    """Gắn vào policy: lerobot-eval vẫn gọi policy.select_action mỗi bước như cũ, nhưng
    select_action giờ tự quản lý chunk và độ trễ. (Không bọc bằng lớp khác vì lerobot-eval
    kiểm isinstance(policy, PreTrainedPolicy); thay vào đó ghi đè 2 phương thức của chính object.)"""

    def __init__(self, policy, lab):
        self.p, self.lab = policy, lab
        H = policy.config.chunk_size
        if not lab.delay <= lab.s <= H - lab.delay:
            raise ValueError(f"cần d <= s <= H - d, đang có d={lab.delay}, s={lab.s}, H={H}")
        if lab.mode == "naive":
            if hasattr(policy.config, "rtc_config"):
                policy.config.rtc_config = None
        else:
            policy.config.rtc_config = RTCConfig(
                enabled=True, mode="trained" if lab.mode == "trained" else "guided",
                execution_horizon=lab.eh, max_guidance_weight=lab.beta,
                prefix_attention_schedule=RTCAttentionSchedule[lab.schedule])
            if lab.mode == "trained":
                max_d = int(getattr(policy.config, "rtc_training_max_delay", 0))
                if not 0 < lab.delay <= max_d:
                    raise ValueError(f"mode trained cần 0 < delay <= rtc_training_max_delay của checkpoint ({max_d})")
        if hasattr(policy, "init_rtc_processor"):
            policy.init_rtc_processor()
        elif lab.mode != "naive":
            raise ValueError(f"{type(policy).__name__} không hỗ trợ RTC; chỉ dùng được --lab.mode=naive")
        if lab.mode == "rtc_full":
            policy.rtc_processor.__class__ = FullJacobianRTC   # cùng object với policy.model.rtc_processor
        self._orig_reset = policy.reset
        self._executed = []
        self._clear()
        policy.select_action = self.select_action               # ghi đè trên object, không đổi lớp
        policy.reset = self.reset

    def _clear(self):
        self.chunk, self.i, self.pending, self.wait = None, 0, None, 0

    def flush(self):
        if self._executed:
            a = torch.stack(self._executed, 1)                   # (B, T, A), không gian đã chuẩn hóa
            jump = (a[:, 1:, :6] - a[:, :-1, :6]).abs().amax(dim=(1, 2))
            STATS["episodes"] += [{"steps": a.shape[1], "max_jump": float(j)} for j in jump]
        self._executed = []

    def reset(self):
        self.flush()
        self._orig_reset()
        self._clear()

    def _predict(self, batch, leftover=None):
        # lerobot-eval gọi select_action trong torch.inference_mode(); guidance cần autograd nên tắt nó ở đây
        with torch.inference_mode(False):
            batch = {k: (v.clone() if torch.is_tensor(v) else v) for k, v in batch.items()}
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            if leftover is not None and self.lab.mode != "naive":
                out = self.p.predict_action_chunk(
                    batch, inference_delay=self.lab.delay, prev_chunk_left_over=leftover.clone(),
                    execution_horizon=self.lab.eh)
            else:
                out = self.p.predict_action_chunk(batch)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            STATS["predict_s"].append(time.perf_counter() - t0)
        return out                                               # (B, H, A) đã chuẩn hóa

    def select_action(self, batch, *args, **kwargs):
        s, d = self.lab.s, self.lab.delay
        if self.chunk is None:                                   # chunk đầu tiên: đồng bộ
            self.chunk, self.i = self._predict(batch), 0
        if self.pending is None and self.i == s:                 # đến lúc hỏi chunk mới
            leftover = self.chunk[:, s:]                         # phần CHƯA chạy của chunk cũ
            self.pending, self.wait = self._predict(batch, leftover), d
        if self.pending is not None and self.wait == 0:          # chunk mới "về" sau d bước
            self.chunk, self.i, self.pending = self.pending, d, None
        action = self.chunk[:, self.i]
        self.i += 1
        if self.pending is not None:
            self.wait -= 1
        self._executed.append(action.detach().float().cpu())
        return action


CTRL = []
_make_policy = E.make_policy


def _patched_make_policy(*a, **k):
    policy = _make_policy(*a, **k)
    CTRL.append(DelayedChunk(policy, LAB))
    return policy


E.make_policy = _patched_make_policy


def summarize():
    for c in CTRL:
        c.flush()
    if STATS["episodes"] or STATS["predict_s"]:
        ps = sorted(STATS["predict_s"][1:] or STATS["predict_s"])   # bỏ lần đầu (khởi động)
        jumps = [e["max_jump"] for e in STATS["episodes"]]
        STATS["summary"] = {
            "n_episodes_logged": len(jumps),
            "mean_max_jump": sum(jumps) / max(1, len(jumps)),
            "predict_ms_median": 1000 * ps[len(ps) // 2] if ps else None,
            "predict_ms_p95": 1000 * ps[int(0.95 * (len(ps) - 1))] if ps else None,
        }
        print("[rtc-lab]", json.dumps(STATS["summary"], ensure_ascii=False))
        if LAB.stats:
            os.makedirs(os.path.dirname(os.path.abspath(LAB.stats)), exist_ok=True)
            with open(LAB.stats, "w") as f:
                json.dump(STATS, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    try:
        E.main()
    finally:
        summarize()
