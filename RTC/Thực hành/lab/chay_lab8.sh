#!/usr/bin/env bash
# Lab 8 một lượt: áp patch RTC lúc huấn luyện cho SmolVLA → chạy thử 50 bước → fine-tune 2 lượt
# (có prefix và đối chứng, mỗi lượt 4.000 bước) → kiểm tra K4 → eval 3 cách ở cùng d → tổng hợp.
# Tổng khoảng 3,5–4 giờ. Chạy lại được: phần nào xong rồi sẽ bỏ qua.
#
# Dùng (trong ~/lerobot, đã conda activate lerobot):
#   nohup bash ~/rtc_lab/chay_lab8.sh > ~/rtc_lab8.log 2>&1 &
#   tail -f ~/rtc_lab8.log
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"
BASE="${BASE:-./outputs/train/obj_bs16x4_21k/checkpoints/021000/pretrained_model}"
D="${D:-15}"                 # độ trễ đo ở Lab 6 (có RTC)
MAXD="${MAXD:-20}"           # d lớn nhất khi huấn luyện, phải >= D
STEPS="${STEPS:-4000}"
EPI="$HOME/libero_object_episodes.txt"
OUT=outputs/rtc_lab8
export MUJOCO_GL=egl
mkdir -p "$OUT"
log() { echo "[$(date '+%H:%M:%S')] $*"; }
die() { log "DỪNG: $*"; exit 1; }

[ -d "$BASE" ] || die "không thấy checkpoint gốc $BASE"
[ -f "$EPI" ] || die "không thấy $EPI (danh sách 454 episode LIBERO-Object, tạo ở trang SmolVLA-LeRobot)"
[ "$MAXD" -ge "$D" ] || die "MAXD ($MAXD) phải >= D ($D)"

log "== 1. Áp patch"
if git apply -R --check "$LAB/smolvla_training_rtc.patch" 2>/dev/null; then
  log "patch đã áp từ trước"
elif git apply --check "$LAB/smolvla_training_rtc.patch" 2>/dev/null; then
  git apply "$LAB/smolvla_training_rtc.patch" && log "đã áp patch" && git diff --stat
else
  die "không áp được patch (repo khác commit b9cb121c hoặc đã sửa 2 file smolvla). Gửi Claude: git status; git log -1"
fi

train() {  # train <tên> <max_delay> <steps>
  local name=$1 md=$2 steps=$3 dir=./outputs/train/$1
  if ls -d "$dir"/checkpoints/[0-9]* >/dev/null 2>&1 && [ -f "$dir/.xong" ]; then log "bỏ qua train $name (đã xong)"; return 0; fi
  rm -rf "$dir"
  log "train $name: rtc_training_max_delay=$md, $steps bước"
  lerobot-train \
    --policy.path="$BASE" \
    --policy.rtc_training_max_delay=$md \
    --policy.push_to_hub=false --policy.device=cuda \
    --dataset.repo_id=lerobot/libero --dataset.video_backend=torchcodec \
    "--dataset.episodes=$(cat "$EPI")" \
    --output_dir="$dir" \
    --batch_size=16 --accelerator.gradient_accumulation.steps=4 \
    --steps=$steps --log_freq=200 --save_freq=$steps \
    --num_workers=4 --accelerator.mixed_precision=bf16 \
    --policy.scheduler_warmup_steps=$(( steps / 20 )) --policy.scheduler_decay_steps=$steps \
    --wandb.enable=false > "$OUT/train_$name.log" 2>&1 || { tail -n 30 "$OUT/train_$name.log"; die "train $name lỗi, xem $OUT/train_$name.log"; }
  touch "$dir/.xong"
  grep -E "loss" "$OUT/train_$name.log" | tail -n 2
}
ckpt() { ls -d ./outputs/train/$1/checkpoints/[0-9]* | sort | tail -1; }

log "== 2. Chạy thử 50 bước (bắt lỗi trước khi train lâu)"
train rtc_try50 $MAXD 50
log "== 3. Fine-tune có prefix (paper ②)"
train obj_rtc_ft $MAXD $STEPS
log "== 4. Fine-tune đối chứng (cùng số bước, không prefix)"
train obj_plain_ft 0 $STEPS

RTC_CK="$(ckpt obj_rtc_ft)/pretrained_model"
PLAIN_CK="$(ckpt obj_plain_ft)/pretrained_model"
log "checkpoint có prefix: $RTC_CK"
log "checkpoint đối chứng: $PLAIN_CK"

log "== 5. Kiểm tra cài đặt trên checkpoint có prefix (có K4)"
python "$LAB/kiem_tra_cai_dat.py" --ckpt "$RTC_CK" --delay "$D" --s "$D" --eh "$(( D + 10 ))" 2>&1 \
  | tee "$OUT/kiem_tra_k4.txt" | sed -n '/=== Kiểm tra/,$p'
grep -q "KHÔNG ĐẠT" "$OUT/kiem_tra_k4.txt" && die "có kiểm tra KHÔNG ĐẠT"

ev() {  # ev <tên> <mode> <checkpoint> <seed>
  local name=$1 mode=$2 ck=$3 seed=$4 s=$D eh=$(( D + 10 ))
  [ "$eh" -gt $(( 50 - D )) ] && eh=$(( 50 - D ))
  if [ -f "$OUT/$name/eval_info.json" ]; then log "bỏ qua $name"; return; fi
  rm -rf "$OUT/$name"
  log "eval $name: mode=$mode d=$D seed=$seed"
  python "$LAB/rtc_libero_eval.py" --lab.mode=$mode --lab.delay=$D --lab.s=$s \
    --lab.execution_horizon=$eh --lab.beta=10 --lab.schedule=EXP --seed=$seed \
    --policy.path="$ck" --env.type=libero --env.task=libero_object --env.task_ids='[0,1,2,3,4]' \
    --eval.batch_size=1 --eval.n_episodes=5 --output_dir="$OUT/$name" \
    > "$OUT/$name.log" 2>&1 || log "LỖI ở $name, xem $OUT/$name.log"
  grep '\[rtc-lab\]' "$OUT/$name.log" | tail -1
}

log "== 6. Eval ở d = $D: đối chứng + ngây thơ, đối chứng + RTC suy luận, có prefix + RTC huấn luyện"
for seed in 1000 2000; do
  ev "ft_plain_naive_s$seed" naive   "$PLAIN_CK" $seed
  ev "ft_plain_rtc_s$seed"   rtc     "$PLAIN_CK" $seed
  ev "ft_rtc_trained_s$seed" trained "$RTC_CK"   $seed
done

log "== 7. Tổng hợp"
{
  python "$LAB/tong_hop_libero.py" "$OUT"
  echo; echo "Loss cuối (KHÔNG so được với nhau: lượt có prefix bỏ phần đầu khỏi loss):"
  for n in obj_plain_ft obj_rtc_ft; do echo "  $n: $(grep -oE "loss[:=] ?[0-9.]+" "$OUT/train_$n.log" | tail -1)"; done
} | tee "$OUT/tong_hop_lab8.txt"
log "XONG. Chép kết quả: cp $OUT/*.txt \"/mnt/d/VLA Modeling/RTC/Thực hành/ket_qua/\""
