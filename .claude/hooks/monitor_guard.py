#!/usr/bin/env python3
"""PreToolUse hook（matcher: Monitor）：一律擋下 Monitor，改用沒有時間上限的背景指令。

為什麼：Claude Code v2.1.271 起 Monitor 最多 30 分鐘，每次到期重開都要花一輪 token
（release note：「replacing the no-timeout `persistent` option」；anthropics/claude-code#94553）。
Bash 的 run_in_background 沒有時間上限，只在指令結束時通知一次，沒事件時不花 token。
出處：issue #70。
"""
import json
import sys

REASON = (
    "這個 repo 不用 Monitor（最長 30 分鐘，到期重開都要花 token；issue #70）。"
    "改用 Bash run_in_background 跑一支「查到事件就印出來並結束」的指令，收到通知、處理完再用同一行重開。"
    "盯 GitHub issue／PR：在 repo 根目錄執行 sh script/github/watch_github.sh 60 --once（用 Bash run_in_background）。"
    "等某個條件成立：until <條件>; do sleep 60; done; echo <結果>。"
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # 讀不到輸入就放行，不擋正常操作
    if data.get("tool_name") != "Monitor":
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": REASON,
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
