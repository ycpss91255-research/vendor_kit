#!/bin/sh
cd <scratchpad>/decisions
for p in a b c; do
  timeout 570 agy --sandbox -p "$(cat ci_brief_$p.txt)" > ci_agy_$p.md 2>&1
  echo "part $p exit=$?" >> ci_agy_status.txt
done
