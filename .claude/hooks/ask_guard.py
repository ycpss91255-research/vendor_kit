#!/usr/bin/env python3
"""PreToolUse hook（matcher: AskUserQuestion）：問維護者之前，先跟 codex 討論並對照已定案的內容。

每個問題（question 欄）要含一行「已確認：」，寫明兩件事：
- codex 討論的出處（discuss workflow 的輸出檔、issue 留言等）
- 對照過的定案（issue、ADR 或對外契約的哪一條），以及為什麼仍然模糊、需要維護者決定

沒有這一行就擋下。能從已定案原則推出答案的題目，不該問，直接照做。
"""
import json
import sys

MARK = "已確認："


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "AskUserQuestion":
        return 0
    questions = (data.get("tool_input") or {}).get("questions") or []
    missing = [q.get("header") or q.get("question", "")[:20] for q in questions if MARK not in (q.get("question") or "")]
    if not missing:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"問題 {'、'.join(missing)} 沒有「{MARK}」這一行。問之前：先跑 discuss workflow 跟 codex 討論；"
            "對照已定案的 issue、ADR 與對外契約；確定真的模糊、推不出答案才問，"
            f"並在題目裡寫「{MARK}codex 討論見 <出處>；對照過 <定案>；仍需決定的原因 <…>」。"
            "推得出答案的就直接照做。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
