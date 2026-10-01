#!/usr/bin/env python3
"""PreToolUse hook（matcher: SendUserFile）：對外文件不准傳沒帶版本號的正式檔。

對外文件（根目錄 README.md、doc/contract/0N_*.md）送審時，必須傳 doc/decisions/_marked/
裡檔名帶版本號的 <鍵>.vN.md（正文副本）與 <鍵>.vN.marked.md（標示版）。傳正式檔，
維護者要打開檔案才知道是哪一版。流程見 doc/contract/README.md「版本怎麼迭代」。
"""
import json
import re
import sys
from pathlib import PurePosixPath

EXTERNAL = re.compile(r"(^|/)(README\.md|doc/contract/0\d_[^/]+\.md)$")
INTERNAL = re.compile(r"(^|/)doc/contract/README\.md$")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "SendUserFile":
        return 0
    files = (data.get("tool_input") or {}).get("files") or []
    bad = []
    for f in files:
        p = PurePosixPath(str(f))
        if INTERNAL.search(str(p)):
            continue  # 審閱頁說明是內部文件
        if EXTERNAL.search(str(p)) and "/_marked/" not in str(p):
            bad.append(str(p))
    if not bad:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "對外文件要傳檔名帶版本號的副本，不傳正式檔：" + "、".join(bad) + "。"
            "改傳 doc/decisions/_marked/<鍵>.vN.md 與 <鍵>.vN.marked.md（先跑 script/doc/mark_changes.py）。"
            "流程見 doc/contract/README.md「版本怎麼迭代」。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
