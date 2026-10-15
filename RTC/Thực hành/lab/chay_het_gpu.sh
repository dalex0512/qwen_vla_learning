#!/usr/bin/env bash
# Chạy hết phần GPU (Lab 6 → kiểm tra cài đặt → Lab 7) một lượt, không cần ngồi chờ.
# Tự đo độ trễ, tự tính d, rồi chạy lưới naive/rtc × 3 mức trễ × 2 seed. Khoảng 3–4 giờ.
#
# Dùng (trong ~/lerobot, đã conda activate lerobot):
#   bash ~/rtc_lab/chay_het_gpu.sh                      # checkpoint mặc định
#   bash ~/rtc_lab/chay_het_gpu.sh <đường_dẫn_checkpoint>
# Chạy nền, tắt terminal vẫn chạy:
#   nohup bash ~/rtc_lab/chay_het_gpu.sh > ~/rtc_lab_gpu.log 2>&1 &
#   tail -f ~/rtc_lab_gpu.log                           # xem tiến độ (Ctrl+C chỉ thoát xem)
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"
CKPT="${1:-./outputs/train/obj_bs16x4_21k/checkpoints/021000/pretrained_model}"
OUT=outputs/rtc_lab
TASKS='[0,1,2,3,4]'
EPS=5
SEEDS="1000 2000"
export MUJOCO_GL=egl
mkdir -p "$OUT"
log() { echo "[$(date '+%H:%M:%S')] $*"; }

run() {  # run <tên> <mode> <d> <seed> [task_ids] [n_eps]
  local name=$1 mode=$2 d=$3 seed=$4 tids=${5:-$TASKS} eps=${6:-$EPS}
  local s=$(( d > 10 ? d : 10 ))
  # execution_horizon phải >= d, nếu không phần đầu đã đóng băng sẽ không được kéo hết.
  # Dùng d + 10, nhưng không quá H - s (vùng chunk cũ còn lại). H = 50.
  local eh=$(( d + 10 )); [ "$eh" -gt $(( 50 - s )) ] && eh=$(( 50 - s ))
  if [ -f "$OUT/$name/eval_info.json" ]; then log "bỏ qua $name (đã có kết quả)"; return; fi
  rm -rf "$OUT/$name"                                      # lượt hỏng trước đó (nếu có)
  log "chạy $name: mode=$mode d=$d s=$s execution_horizon=$eh seed=$seed"
  python "$LAB/rtc_libero_eval.py" --lab.mode=$mode --lab.delay=$d --lab.s=$s \
    --lab.execution_horizon=$eh --lab.beta=10 --lab.schedule=EXP --seed=$seed \
    --policy.path="$CKPT" --env.type=libero --env.task=libero_object --env.task_ids="$tids" \
    --eval.batch_size=1 --eval.n_episodes=$eps --output_dir="$OUT/$name" \
    > "$OUT/$name.log" 2>&1 || log "LỖI ở $name, xem $OUT/$name.log"
  grep '\[rtc-lab\]' "$OUT/$name.log" | tail -1
}

log "== Lab 6: đo độ trễ (1 tác vụ, 2 episode mỗi cách)"
for m in naive rtc rtc_full; do run "latency_$m" $m 4 1000 '[0]' 2; done

# d lấy theo độ trễ KHI BẬT RTC (lượt latency_rtc): đó là độ trễ thật robot sẽ gặp khi chạy RTC
D=$(python - "$OUT/latency_rtc/rtc_lab_stats.json" <<'PY'
import json, math, sys
s = json.load(open(sys.argv[1]))["summary"]
print(max(1, math.ceil(s["predict_ms_p95"] / 50)))
PY
) || { log "Không đọc được độ trễ, dừng. Xem $OUT/latency_rtc.log"; exit 1; }
D2=$(( (3 * D + 1) / 2 ))
log "p95 (có RTC) → d = $D bước (LIBERO 20 Hz); mức thứ hai = $D2"
if [ "$D2" -gt 25 ]; then log "d quá lớn so với H = 50, dừng để xem lại. Gửi kết quả latency cho Claude."; exit 1; fi

log "== Kiểm tra cài đặt RTC"
rm -f "$OUT/kiem_tra_cai_dat.txt"
python "$LAB/kiem_tra_cai_dat.py" --ckpt "$CKPT" --delay "$D" --s "$(( D > 10 ? D : 10 ))" --eh "$(( D + 10 ))" 2>&1 | tee "$OUT/kiem_tra_cai_dat.txt" | sed -n '/=== Kiểm tra/,$p'
if grep -q "KHÔNG ĐẠT" "$OUT/kiem_tra_cai_dat.txt"; then log "Có kiểm tra KHÔNG ĐẠT, dừng trước Lab 7."; exit 1; fi

log "== Lab 7: lưới naive / rtc × d = 0, $D, $D2 × seed $SEEDS"
for seed in $SEEDS; do
  for d in 0 $D $D2; do
    for m in naive rtc; do run "${m}_d${d}_s${seed}" $m $d $seed; done
  done
done

log "== Tổng hợp"
python "$LAB/tong_hop_libero.py" "$OUT" | tee "$OUT/tong_hop.txt"
log "XONG. Gửi Claude: $OUT/tong_hop.txt và $OUT/kiem_tra_cai_dat.txt"
