#!/usr/bin/env bash
# Chạy hết phần A (Lab 0–4) một lượt, khoảng 5 phút CPU. Hình/JSON vào results/, chữ in ra vào ket_qua_cpu.txt
# (kết quả mẫu của Claude nằm riêng ở results_mau/ để so)
set -e
cd "$(dirname "$0")"
for f in lab0_train.py lab1_nhin_van_de.py lab2_ben_trong_rtc.py lab3_so_sanh_do_tre.py lab4_tinh_chinh.py; do
  echo "===== $f"; python "$f"
done 2>&1 | tee ket_qua_cpu.txt
echo "XONG. Gửi Claude file ket_qua_cpu.txt"
