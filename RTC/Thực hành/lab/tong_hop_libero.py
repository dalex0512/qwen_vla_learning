"""Gom kết quả các lượt rtc_libero_eval.py thành bảng, gộp các seed của cùng một cấu hình,
kèm khoảng tin cậy Wilson 95% cho tỉ lệ thành công.
Chạy: python tong_hop_libero.py outputs/rtc_lab     (thư mục chứa các --output_dir con)"""
import glob
import json
import math
import os
import sys
from collections import defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (100 * max(0.0, c - h), 100 * min(1.0, c + h))


root = sys.argv[1] if len(sys.argv) > 1 else "outputs/rtc_lab"
groups = defaultdict(lambda: {"k": 0, "n": 0, "seeds": [], "jumps": [], "ms": [], "runs": []})
for info_path in sorted(glob.glob(os.path.join(root, "*", "eval_info.json"))):
    d = os.path.dirname(info_path)
    ov = json.load(open(info_path))["overall"]
    st_path = os.path.join(d, "rtc_lab_stats.json")
    st = json.load(open(st_path)) if os.path.exists(st_path) else {}
    lab, sm = st.get("lab", {}), st.get("summary", {})
    key = (lab.get("mode", "?"), lab.get("delay", "?"), lab.get("s", "?"), lab.get("execution_horizon", lab.get("eh", "?")),
           st.get("policy", ""), os.path.basename(d).startswith("latency_"))   # lượt đo độ trễ tách riêng
    g = groups[key]
    g["k"] += int(ov["n_success"]); g["n"] += int(ov["n_episodes"])
    g["seeds"].append(str(st.get("seed", "?"))); g["runs"].append(os.path.basename(d))
    g["jumps"] += [e["max_jump"] for e in st.get("episodes", [])]
    if sm.get("predict_ms_median") is not None:
        g["ms"].append(sm["predict_ms_median"])

print(f"{'mode':9s} {'d':>3s} {'s':>3s} {'thành công':>11s} {'KTC 95%':>14s} {'k/n':>8s} {'seed':>10s} {'giật TB':>8s} {'ms/lần':>7s}  lượt")
for key in sorted(groups, key=lambda k: (str(k[1]), str(k[0]))):
    g = groups[key]
    lo, hi = wilson(g["k"], g["n"])
    pc = 100 * g["k"] / max(1, g["n"])
    jump = "-" if not g["jumps"] else f"{sum(g['jumps']) / len(g['jumps']):.3f}"
    ms = "-" if not g["ms"] else f"{sum(g['ms']) / len(g['ms']):.0f}"
    print(f"{key[0] + ('*' if key[5] else ''):9s} {key[1]!s:>3s} {key[2]!s:>3s} {pc:10.1f}% {f'[{lo:.0f}; {hi:.0f}]':>14s} {g['k']:>3d}/{g['n']:<4d} "
          f"{','.join(g['seeds']):>10s} {jump:>8s} {ms:>7s}  {' '.join(g['runs'])}")
print("\n* = lượt đo độ trễ (Lab 6), ít episode, không dùng để so thành công.")
print("KTC 95%: khoảng tin cậy Wilson của tỉ lệ thành công. Hai cấu hình có khoảng chồng nhau nhiều thì chưa kết luận được bên nào hơn.")
