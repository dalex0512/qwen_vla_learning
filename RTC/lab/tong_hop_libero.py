"""Gom kết quả các lượt rtc_libero_eval.py thành một bảng.
Chạy: python tong_hop_libero.py outputs/rtc_lab     (thư mục chứa các --output_dir con)"""
import glob
import json
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "outputs/rtc_lab"
rows = []
for info_path in sorted(glob.glob(os.path.join(root, "*", "eval_info.json"))):
    d = os.path.dirname(info_path)
    ov = json.load(open(info_path))["overall"]
    st_path = os.path.join(d, "rtc_lab_stats.json")
    st = json.load(open(st_path)) if os.path.exists(st_path) else {}
    lab, sm = st.get("lab", {}), st.get("summary", {})
    rows.append((os.path.basename(d), lab.get("mode", "?"), lab.get("delay", "?"), lab.get("s", "?"),
                 ov["pc_success"], ov["n_episodes"], sm.get("mean_max_jump"), sm.get("predict_ms_median")))
print(f"{'lượt':28s} {'mode':9s} {'d':>3s} {'s':>3s} {'thành công':>11s} {'số ep':>6s} {'giật TB':>8s} {'ms/lần gọi':>10s}")
for r in rows:
    jump = "-" if r[6] is None else f"{r[6]:.3f}"
    ms = "-" if r[7] is None else f"{r[7]:.0f}"
    print(f"{r[0]:28s} {r[1]:9s} {r[2]!s:>3s} {r[3]!s:>3s} {r[4]:10.1f}% {r[5]:6d} {jump:>8s} {ms:>10s}")
