"""Lab 1: NHÌN tận mắt vấn đề đổi chunk khi có độ trễ, và RTC sửa nó ra sao.
Chạy: python lab1_nhin_van_de.py   (cần chạy lab0_train.py trước, hoặc để nó tự train)
Ra: results/lab1_paths.png và bảng độ lệch ở chỗ nối."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from common import H, OBS_C, OBS_R, get_models, make_rtc, run_async

os.makedirs("results", exist_ok=True)
plain, trained, norm = get_models()
d, s, B, seed = 4, 8, 6, 7

runs = {
    "Nối ngây thơ (naive)": run_async(plain, norm, method="naive", d=d, s=s, B=B, seed=seed),
    "Paper 1: guidance (LeRobot)": run_async(plain, norm, method="guided", d=d, s=s, B=B, seed=seed,
                                              rtc=make_rtc("soft", H - s)),
    "Paper 2: prefix lúc huấn luyện": run_async(trained, norm, method="trained", d=d, s=s, B=B, seed=seed),
}

fig, axes = plt.subplots(2, 3, figsize=(15, 7.5), sharey="row")
for col, (name, (env, switches)) in enumerate(runs.items()):
    path = torch.stack(env.path, 1)                        # (B, T+1, 2)
    acts = torch.stack(env.actions, 1)[..., 1]             # vận tốc y đã chạy
    ax = axes[0, col]
    ax.add_patch(plt.Circle(OBS_C, OBS_R, color="0.75"))
    for b in range(B):
        ok = bool(env.success()[b])
        ax.plot(path[b, :, 0], path[b, :, 1], color="tab:green" if ok else "tab:red", lw=1.6)
        ax.plot(1.0, env.goal()[b], "k*", ms=7)
    ax.set_title(f"{name}\nthành công {int(env.success().sum())}/{B}")
    ax.set_xlim(-0.02, 1.05); ax.set_aspect("equal"); ax.set_xlabel("x")
    ax = axes[1, col]
    for b in range(3):
        ax.plot(acts[b], lw=1.4)
    for k in range(1, 6):                                  # vạch: lúc chunk mới bắt đầu được dùng
        ax.axvline(s + d + (k - 1) * s, color="0.6", ls=":", lw=1)
    ax.set_xlabel("bước"); ax.set_title("vận tốc y (vạch chấm: chỗ đổi sang chunk mới)")
    mis = torch.stack([(a - b).abs().mean() for a, b in switches]).mean()
    print(f"{name:32s} lệch trung bình ở {d} bước nối = {mis:.3f} (đơn vị chuẩn hóa) | "
          f"giật lớn nhất TB = {env.max_jerk().mean():.4f}")
axes[0, 0].set_ylabel("y"); axes[1, 0].set_ylabel("vy")
fig.suptitle(f"Độ trễ d = {d} bước, chạy s = {s} hành động mỗi chunk, H = {H}. Xanh: thành công, đỏ: thất bại")
fig.tight_layout()
fig.savefig("results/lab1_paths.png", dpi=110)
print("Đã lưu results/lab1_paths.png")
