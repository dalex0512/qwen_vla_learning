"""Lab 4: tinh chỉnh các núm của RTC trong LeRobot ở độ trễ cố định d = 4.
  4a. max_guidance_weight (beta) x execution_horizon, lịch EXP và LINEAR
  4b. s (bao lâu hỏi chunk mới một lần): phản ứng nhanh hay ổn định
Chạy: python lab4_tinh_chinh.py  (khoảng 1 phút)   Ra: results/lab4_tuning.json"""
import json
import os

from common import H, get_models, make_rtc, run_async

os.makedirs("results", exist_ok=True)
plain, trained, norm = get_models()
d, B = 4, 1000
out = {"4a": [], "4b": []}

print(f"4a) d = {d}, s = 8 (phần còn lại của chunk cũ dài H - s = {H - 8})")
print(f"   {'lịch':7s} {'exec_h':>6s} " + " ".join(f"{'β=' + str(b):>13s}" for b in [0.5, 1, 2, 5, 10, 20]))
for kind in ["soft", "linear"]:
    for eh in [4, 6, 8]:
        cells = []
        for beta in [0.5, 1, 2, 5, 10, 20]:
            env, _ = run_async(plain, norm, method="guided", d=d, s=8, rtc=make_rtc(kind, eh, beta), B=B)
            sc, jk = env.success().float().mean().item(), env.max_jerk().mean().item()
            out["4a"].append(dict(schedule=kind, execution_horizon=eh, beta=beta, success=sc, jerk=jk))
            cells.append(f"{sc:.2f} / {100 * jk:4.2f}")
        name = "EXP" if kind == "soft" else "LINEAR"
        print(f"   {name:7s} {eh:6d} " + " ".join(f"{c:>13s}" for c in cells))
print("   (mỗi ô: tỉ lệ thành công / độ giật x100)")

print(f"\n4b) d = {d}, đổi s (số hành động chạy mỗi chunk trước khi hỏi chunk mới)")
for name, kw in [("naive", dict(model=plain, method="naive")),
                 ("RTC-1 hard", dict(model=plain, method="guided", kind="hard")),
                 ("RTC-1 soft", dict(model=plain, method="guided", kind="soft")),
                 ("RTC-2 trained", dict(model=trained, method="trained"))]:
    cells = []
    for s in [4, 6, 8, 10, 12]:
        rtc = make_rtc(kw["kind"], H - s) if "kind" in kw else None
        env, _ = run_async(kw["model"], norm, method=kw["method"], d=d, s=s, rtc=rtc, B=B)
        sc, jk = env.success().float().mean().item(), env.max_jerk().mean().item()
        out["4b"].append(dict(method=name, s=s, success=sc, jerk=jk))
        cells.append(f"s={s:2d}: {sc:.2f}/{100 * jk:4.2f}")
    print(f"   {name:14s} " + "  ".join(cells))
json.dump(out, open("results/lab4_tuning.json", "w"), indent=1, ensure_ascii=False)
print("\nĐã lưu results/lab4_tuning.json")
