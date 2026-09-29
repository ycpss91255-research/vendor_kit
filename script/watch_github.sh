#!/bin/sh
# 盯 GitHub 上這個 repo 的 issue 與 PR，有事就印一行，給 Claude Code 的 Monitor 當事件來源。
#
# 用法：sh script/watch_github.sh [間隔秒數，預設 60] [--once]
# 事件：新開的 issue／PR、新留言、被關閉或 merge 的 issue／PR。每行一件事。
# --once：查到第一批事件就印出來並結束。給沒有時間上限的背景指令用（Bash run_in_background），
#         結束時才通知一次；收到後再重新啟動，就能一直盯著，不受 Monitor 30 分鐘的上限。
# 只讀：只呼叫 gh api 的 GET，不改 GitHub 上任何東西。
set -u
R=ycpss91255-research/vendor_kit
INTERVAL=${1:-60}
ONCE=${2:-}
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)

while true; do
  sleep "$INTERVAL"
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  out=$(
  # 新留言（issue 與 PR 的一般留言都在這支 API）
  gh api "repos/$R/issues/comments?since=$last&per_page=50" --jq \
    '.[] | select(.created_at >= "'"$last"'") | "留言 #\(.issue_url | split("/") | last) \(.user.login)：\(.body | gsub("\\s+"; " ") | .[0:120])"' \
    2>/dev/null || true

  # 這段時間內有動靜的 issue／PR：新開的、被關閉或 merge 的
  gh api "repos/$R/issues?state=all&since=$last&per_page=50" --jq \
    '.[] | (if .pull_request then "PR" else "issue" end) as $k
     | if .created_at >= "'"$last"'" then "新開 \($k) #\(.number) \(.title)"
       elif (.closed_at // "") >= "'"$last"'" then "關閉 \($k) #\(.number) \(.title)"
       else empty end' \
    2>/dev/null || true
  )

  if [ -n "$out" ]; then
    printf '%s\n' "$out"
    [ "$ONCE" = "--once" ] && exit 0
  fi
  last=$now
done
