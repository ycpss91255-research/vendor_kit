#!/bin/sh
# 用法：sh r13_codex/run_group.sh <n>   （在 scratchpad 執行）
set -e
n="$1"; d=r13_codex
ids=$(python3 -c "import json;print(' '.join(json.load(open('$d/group$n.json'))))")
{
  cat $d/task.txt
  printf '\n\n=== 附件 S：規格 §0–§9 ===\n'; cat $d/spec_0_9.md
  printf '\n\n=== 附件 P：本組頁面抽取文字 ===\n'
  for i in $ids; do printf '\n\n----- 頁 %s -----\n' "$i"; cat review_v2_out/$i.md; done
  printf '\n\n=== 附件 R：第十二版 codex 對本組頁的審查條目 ===\n'
  for g in $(python3 -c "import json;print(' '.join(map(str,json.load(open('$d/group${n}_prev.json')))))"); do cat r12_codex/findings$g.md; done
  printf '\n\n=== 附件 L：機械 lint（本組頁）===\n'
  python3 - "$ids" <<'PY'
import json,sys
ids=set(sys.argv[1].split()); 
for e in json.load(open('review_v2_out/lint.json')):
    if e['page'] in ids and e['level']=='warn': print(f"[{e['rule']}] {e['page']} {e['id']}: {e['msg'][:200]}")
PY
} > $d/brief$n.txt
imgs=""; for i in $ids; do imgs="$imgs -i review_v2_png/$i.png"; done
timeout 580 codex exec --sandbox read-only --skip-git-repo-check $imgs - < $d/brief$n.txt > $d/out$n.md 2>&1
echo "exit=$?"; wc -c $d/brief$n.txt $d/out$n.md
