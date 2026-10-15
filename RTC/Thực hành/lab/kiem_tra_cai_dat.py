"""Kiểm tra RTC được cài ĐÚNG trên SmolVLA thật (không cần LIBERO, chỉ cần checkpoint + dataset trong cache).
Đây là bằng chứng "cài đúng", mạnh hơn mọi con số thành công.

Chạy (trong ~/lerobot):
  python ~/rtc_lab/kiem_tra_cai_dat.py \
    --ckpt ./outputs/train/obj_bs16x4_21k/checkpoints/021000/pretrained_model --delay 4
Với checkpoint fine-tune bằng patch (Lab 8) script tự chạy thêm kiểm tra K4.

K1  β gần 0  → RTC phải cho gần đúng chunk như không RTC (cùng nhiễu).
K2  β = 10   → d hành động đầu của chunk mới phải gần đuôi chunk cũ hơn hẳn so với không RTC.
K3  Jacobian → bản LeRobot: correction == err; bản đúng paper (FullJacobianRTC): khác err.
K4  trained  → d hành động đầu trùng ĐÚNG chunk cũ (chỉ khi checkpoint có rtc_training_max_delay > 0).
"""
import argparse
import os
import sys
import time

import torch

from lerobot.configs import RTCAttentionSchedule
from lerobot.policies.rtc import RTCConfig

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtc_full_jacobian import FullJacobianRTC  # noqa: E402


def set_rtc(policy, cfg, full=False):
    policy.config.rtc_config = cfg
    policy.init_rtc_processor()
    if full:
        policy.rtc_processor.__class__ = FullJacobianRTC


def predict(policy, batch, noise, **kw):
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    out = policy.predict_action_chunk({k: (v.clone() if torch.is_tensor(v) else v) for k, v in batch.items()},
                                      noise=noise.clone(), **kw)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    return out, 1000 * (time.perf_counter() - t0)


def run_checks(policy, batch_old, batch_new, delay=4, s=10, eh=10, device="cpu"):
    H, A = policy.config.chunk_size, policy.config.max_action_dim
    res = []
    g = torch.Generator(device="cpu").manual_seed(0)
    n_old = torch.randn(1, H, A, generator=g).to(device)
    n_new = torch.randn(1, H, A, generator=g).to(device)
    set_rtc(policy, None)
    old, _ = predict(policy, batch_old, n_old)
    leftover = old[:, s:]                                    # phần chưa chạy của chunk cũ, (1, H - s, A_thật)
    plain, ms_plain = predict(policy, batch_new, n_new)
    d_plain = (plain[:, :delay] - leftover[:, :delay]).abs().mean().item()
    kw = dict(inference_delay=delay, prev_chunk_left_over=leftover, execution_horizon=eh)

    plain2, _ = predict(policy, batch_new, n_new)                # chạy lại y hệt: đo "nhiễu nền" của GPU
    floor = (plain2 - plain).abs().max().item()

    # K2 + K3a (bản LeRobot), chạy trước để có mốc cho K1
    set_rtc(policy, RTCConfig(enabled=True, execution_horizon=eh, max_guidance_weight=10.0,
                              prefix_attention_schedule=RTCAttentionSchedule.EXP, debug=True))
    with torch.inference_mode(False):
        guided, ms_rtc = predict(policy, batch_new, n_new, **kw)
    d_rtc = (guided[:, :delay] - leftover[:, :delay]).abs().mean().item()
    effect = (guided - plain).abs().max().item()

    # K1: β gần 0 thì RTC gần như không đổi gì, so với tác động khi β = 10.
    # Không đòi trùng tuyệt đối: trên GPU, bật autograd có thể làm PyTorch chọn kernel attention khác,
    # sai số nhỏ cộng dồn qua 10 bước khử nhiễu.
    set_rtc(policy, RTCConfig(enabled=True, execution_horizon=eh, max_guidance_weight=1e-6,
                              prefix_attention_schedule=RTCAttentionSchedule.EXP))
    with torch.inference_mode(False):
        tiny, _ = predict(policy, batch_new, n_new, **kw)
    diff = (tiny - plain).abs().max().item()
    res.append(("K0 nhiễu nền (chạy lại y hệt)", None, f"lệch lớn nhất {floor:.2e} (chỉ để tham khảo)"))
    res.append(("K1 β ≈ 0 gần như không đổi gì", diff < 0.1 * effect,
                f"lệch {diff:.2e}, so với tác động của β = 10 là {effect:.2e} ({100 * diff / max(effect, 1e-12):.1f}%)"))
    res.append(("K2 phần đầu bám chunk cũ", d_rtc < 0.25 * d_plain,
                f"lệch {delay} ô đầu: không RTC {d_plain:.3f} → RTC {d_rtc:.3f}"))
    set_rtc(policy, RTCConfig(enabled=True, execution_horizon=eh, max_guidance_weight=10.0,
                              prefix_attention_schedule=RTCAttentionSchedule.EXP, debug=True))
    with torch.inference_mode(False):
        predict(policy, batch_new, n_new, **kw)
    steps = [st for st in policy.rtc_processor.get_all_debug_steps() if st.correction is not None]
    same = all(torch.allclose(st.correction, st.err) for st in steps) and len(steps) > 0
    res.append(("K3a LeRobot: correction == err", same, f"{len(steps)} bước có guidance"))

    set_rtc(policy, RTCConfig(enabled=True, execution_horizon=eh, max_guidance_weight=10.0,
                              prefix_attention_schedule=RTCAttentionSchedule.EXP, debug=True), full=True)
    with torch.inference_mode(False):
        full, ms_full = predict(policy, batch_new, n_new, **kw)
    steps = [st for st in policy.rtc_processor.get_all_debug_steps() if st.correction is not None]
    cos = torch.nn.functional.cosine_similarity(steps[1].correction.flatten().float(), steps[1].err.flatten().float(), dim=0).item()
    d_full = (full[:, :delay] - leftover[:, :delay]).abs().mean().item()
    res.append(("K3b đúng paper: correction ≠ err", cos < 0.999,
                f"cos ở bước 2 = {cos:.3f}; lệch {delay} ô đầu {d_full:.3f}"))

    # K4
    maxd = int(getattr(policy.config, "rtc_training_max_delay", 0))
    if maxd > 0 and delay <= maxd:
        set_rtc(policy, RTCConfig(enabled=True, mode="trained", execution_horizon=eh))
        tr, ms_tr = predict(policy, batch_new, n_new, **kw)
        ok = torch.allclose(tr[:, :delay], leftover[:, :delay], atol=1e-5)
        res.append(("K4 trained: prefix trùng chunk cũ", ok,
                    f"lệch {(tr[:, :delay] - leftover[:, :delay]).abs().max().item():.2e}; {ms_tr:.0f} ms"))
    else:
        res.append(("K4 trained", None, "bỏ qua: checkpoint không có rtc_training_max_delay > 0"))
    set_rtc(policy, None)

    print("\n=== Kiểm tra cài đặt RTC ===")
    for name, ok, msg in res:
        tag = "THÔNG TIN" if ok is None and name.startswith("K0") else ("BỎ QUA" if ok is None else ("ĐẠT" if ok else "KHÔNG ĐẠT"))
        print(f"[{tag:9s}] {name:36s} {msg}")
    print(f"\nThời gian 1 lần gọi (lần đo đơn, chỉ tham khảo): không RTC {ms_plain:.0f} ms · "
          f"RTC LeRobot {ms_rtc:.0f} ms · RTC đúng paper {ms_full:.0f} ms")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--dataset", default="lerobot/libero")
    ap.add_argument("--episode", type=int, default=0)
    ap.add_argument("--delay", type=int, default=4)
    ap.add_argument("--s", type=int, default=10)
    ap.add_argument("--eh", type=int, default=10)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    a = ap.parse_args()

    from torch.utils.data import default_collate

    from lerobot.configs import PreTrainedConfig
    from lerobot.datasets import LeRobotDataset, LeRobotDatasetMetadata, resolve_delta_timestamps
    from lerobot.policies import get_policy_class, make_pre_post_processors

    config = PreTrainedConfig.from_pretrained(a.ckpt)
    config.pretrained_path = a.ckpt
    policy = get_policy_class(config.type).from_pretrained(a.ckpt, config=config).to(a.device).eval()
    pre, _ = make_pre_post_processors(policy_cfg=config, pretrained_path=a.ckpt,
                                      preprocessor_overrides={"device_processor": {"device": a.device}})
    meta = LeRobotDatasetMetadata(a.dataset)
    ds = LeRobotDataset(a.dataset, episodes=[a.episode], delta_timestamps=resolve_delta_timestamps(config, meta))
    # chunk cũ tính ở khung t, chunk mới ở khung t + s: đúng như lúc chạy thật
    b_old = pre(default_collate([ds[0]]))
    b_new = pre(default_collate([ds[min(a.s, len(ds) - 1)]]))
    run_checks(policy, b_old, b_new, delay=a.delay, s=a.s, eh=a.eh, device=a.device)


if __name__ == "__main__":
    main()
