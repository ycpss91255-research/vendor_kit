#!/usr/bin/env python3
"""PreToolUse hook（matcher: Edit|Write）：檔案只寫做什麼與相關說明，不寫決策紀錄。

決策與討論經過放 issue。例外：對外契約（根目錄 README.md、doc/contract/0N_*.md）
與 ADR（doc/adr/）本來就是記錄決定的地方。

擋的內容（只看這次寫入的新文字）：日期（YYYY-MM-DD），以及直接引用某人的話（「維護者：「…」」這種寫法）。
描述流程的句子（例如「維護者回覆定案才 merge」）不擋。
"""
import json
import re
import sys

ALLOWED = re.compile(r"(^|/)(README\.md|doc/contract/0\d_[^/]+\.md|doc/adr/[^/]+\.md)$")
BANNED = re.compile(r"\b20\d\d-\d\d-\d\d\b|(?:維護者|使用者)[^\n。]{0,4}[:：]\s*「")


def new_text(tool: str, inp: dict) -> str:
    if tool == "Write":
        return inp.get("content") or ""
    if tool == "Edit":
        return inp.get("new_string") or ""
    return ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool = data.get("tool_name")
    inp = data.get("tool_input") or {}
    path = str(inp.get("file_path") or "")
    if tool not in ("Edit", "Write") or not path or ALLOWED.search(path):
        return 0
    if "/.claude/projects/" in path:
        return 0  # Claude Code 自己的記憶檔，不在 repo 裡
    hits = sorted(set(BANNED.findall(new_text(tool, inp))))
    if not hits:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"{path} 的新內容有決策紀錄（{'、'.join(hits)}）。檔案只寫做什麼與相關說明；"
            "日期、誰決定的、討論經過放 issue。對外契約（README、審閱頁 01～04）與 ADR 除外。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
