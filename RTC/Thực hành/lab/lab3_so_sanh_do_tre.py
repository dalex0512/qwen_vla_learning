"""Lab 3: thí nghiệm chính, phiên bản thu nhỏ của Hình 5 (paper 1) và Hình 3 (paper 2).
Cùng một mô hình, đổi cách nối chunk, quét độ trễ d = 0..8 (s = 8, H = 16), 1000 episode mỗi ô.
Chạy: python lab3_so_sanh_do_tre.py  (khoảng 1 phút CPU)
Ra: results/lab3_delay.png và results/lab3_delay.json"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from common import H, get_models, make_rtc, run_async

os.makedirs("results", exist_ok=True)
plain, trained, norm = get_models()
s, B, DELAYS = 8, 1000, list(range(0, 9))
MAX_TRAIN_DELAY = 6   # mô hình "trained" được huấn luyện với d trong {0..6}

METHODS = {
    "naive (nối ngây thơ)":          dict(model=plain, method="naive"),
    "RTC-1 hard (ZEROS)":            dict(model=plain, method="guided", kind="hard"),
    "RTC-1 soft (EXP, LeRobot)":     dict(model=plain, method="guided", kind="soft"),
    "RTC-1 soft, gradient đầy đủ":   dict(model=plain, method="guided", kind="soft_full"),
    "RTC-2 prefix lúc huấn luyện":   dict(model=trained, method="trained"),
}
res = {}
for name, m in METHODS.items():
    res[name] = []
    for d in DELAYS:
        rtc = make_rtc(m["kind"], H - s) if "kind" in m else None
        env, sw = run_async(m["model"], norm, method=m["method"], d=d, s=s, rtc=rtc, B=B)
        mis = torch.stack([(a - b).abs().mean() for a, b in sw]).mean().item() if d > 0 else 0.0
        row = dict(d=d, success=env.success().float().mean().item(), hit=env.hit.float().mean().item(),
                   jerk=env.max_jerk().mean().item(), mismatch=mis)
        res[name].append(row)
    print(f"\n{name}")
    print("   d      : " + " ".join(f"{r['d']:6d}" for r in res[name]))
    print("   thành công: " + " ".join(f"{r['success']:6.2f}" for r in res[name]))
    print("   chạm vật : " + " ".join(f"{r['hit']:6.2f}" for r in res[name]))
    print("   giật x100: " + " ".join(f"{100 * r['jerk']:6.2f}" for r in res[name]))

json.dump(res, open("results/lab3_delay.json", "w"), indent=1, ensure_ascii=False)
fig, ax = plt.subplots(1, 3, figsize=(16, 4.2))
for name, rows in res.items():
    ls = "--" if "đầy đủ" in name else "-"
    ax[0].plot(DELAYS, [r["success"] for r in rows], ls, marker="o", label=name)
    ax[1].plot(DELAYS, [r["hit"] for r in rows], ls, marker="o", label=name)
    ax[2].plot(DELAYS, [100 * r["jerk"] for r in rows], ls, marker="o", label=name)
for a, t in zip(ax, ["Tỉ lệ thành công", "Tỉ lệ chạm vật cản", "Độ giật lớn nhất (x100)"]):
    a.set_title(t); a.set_xlabel("độ trễ d (bước)"); a.axvspan(MAX_TRAIN_DELAY + 0.5, 8.5, color="0.9")
ax[0].legend(fontsize=8)
ax[0].text(7.5, 0.04, "ngoài vùng d\nđã huấn luyện", ha="center", fontsize=8, transform=ax[0].get_xaxis_transform())
fig.tight_layout(); fig.savefig("results/lab3_delay.png", dpi=110)
print("\nĐã lưu results/lab3_delay.png, results/lab3_delay.json")
