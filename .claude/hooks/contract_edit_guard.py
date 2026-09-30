#!/usr/bin/env python3
"""PreToolUse hook（matcher: Edit|Write）：改對外文件時附上兩條提醒。

對外文件＝根目錄 README.md、doc/decisions/review/0N_*.md，另含 CONTEXT.md。
1. 介面細節（結束碼與優先序、選項寫法、說明與用法錯誤、訊息格式）先對照主流 CLI 慣例
   （GNU／POSIX、diff、grep、git、Python argparse），附來源；舊文件搬來的內容也要重新檢查。
2. 對外頁的改動走 doc-edit workflow（它的 codex 審查會逐條對照慣例）。

維護者 2026-09-30：結束碼優先序從舊 02 直接搬、沒查慣例 →「這個不要再犯了，有需要就寫成 hook」。
不擋：doc-edit 的子代理本身也要改這些檔；強制檢查在 doc-edit 的審查步驟，這裡是第二道提醒。
"""
import json
import re
import sys

TARGET = re.compile(r"(^|/)(README\.md|CONTEXT\.md|doc/decisions/review/0\d_[^/]+\.md)$")
REMIND = (
    "你正在改對外文件 {path}。"
    "（1）介面細節（結束碼與優先序、選項寫法、說明與用法錯誤、訊息格式）先對照主流 CLI 慣例"
    "（GNU／POSIX、diff、grep、git、Python argparse），寫下依據；從舊文件搬來的也要重新檢查，不能只搬位置。"
    "（2）對外頁改動應走 doc-edit workflow；若不是 doc-edit 的子代理，先停下改用 doc-edit。"
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    path = str((data.get("tool_input") or {}).get("file_path") or "")
    if data.get("tool_name") not in ("Edit", "Write") or not TARGET.search(path):
        return 0
    if "/doc/decisions/review/README.md" in path:
        return 0  # 審閱頁說明是內部文件
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": REMIND.format(path=path),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
