#!/bin/sh
# 用法: sh chk.sh [pid ...]   （無參數 = 全部；只印有問題的頁）
cd "$(dirname "$0")"   # 原本 cd 到 scratchpad；現為 script/diagram/_misc（run_v1_b.py 等輸入請自備）
python3 run_v1_b.py 2>&1 | grep -i "Traceback\|Error" && exit 1
for s in check_overflow check_overlap check_cross_v1b check_self_v1b check_jog_r7 check_align_v1b; do
  out=$(python3 $s.py v1_b.drawio "$@" 2>&1 | grep -v "^   無$" | grep -v "^共 0 筆" )
  if [ -n "$(echo "$out" | grep -v '^== ')" ]; then echo "## $s"; echo "$out" | awk '/^== /{h=$0;next}{if(h){print h;h=""}print}'; fi
done
python3 run_v1_b.py 2>/dev/null | awk '{h=$NF; gsub(/[^0-9]/,"",h); if (h+0>2400) print "PAGE HEIGHT >2400:", $0}'
