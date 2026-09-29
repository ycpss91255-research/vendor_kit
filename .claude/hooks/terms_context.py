#!/usr/bin/env python3
"""UserPromptSubmit hook：每次使用者送出訊息，把 CONTEXT.md 的正式名詞與命名規則放進上下文。

為什麼要有：提案、取名、寫對外文件之前沒先對齊名詞表和 01、02，
就會憑印象取名（例如把「本機開發來源」講成「本機 image」、把 VK 講成「開發者」）。
靠記得去查一定會漏，所以每一輪都自動附上名詞清單。

輸出：hookSpecificOutput.additionalContext。讀不到 CONTEXT.md 就安靜放行（exit 0、不輸出）。
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

RULE = (
    "命名與提案規則（hook 自動附上）：提出任何名稱、選項名、指令寫法，或改對外文件之前，"
    "先對照根目錄 CONTEXT.md、doc/decisions/review/01_purpose.md、02_invariants.md 的正式名詞與已定案內容；"
    "只用下面這些正式名詞，不用 _Avoid_ 詞，不自己發明近義詞。"
    "新概念若名詞表沒有，先說明它不在名詞表裡，再提議要不要新增。"
)


def terms(context: Path) -> list[str]:
    """抓 <a id="term-..."></a> 下一行的「**名詞**（英文）：」。"""
    lines = context.read_text(encoding="utf-8").splitlines()
    out = []
    for i, ln in enumerate(lines[:-1]):
        if ln.startswith('<a id="term-'):
            m = re.match(r"\*\*(.+?)\*\*(（[^）]*）)?", lines[i + 1])
            if m:
                out.append(m.group(1) + (m.group(2) or ""))
    return out


def main() -> int:
    try:
        json.load(sys.stdin)  # 內容用不到，只確認是 hook 呼叫
    except Exception:
        pass
    context = ROOT / "CONTEXT.md"
    if not context.is_file():
        return 0
    names = terms(context)
    if not names:
        return 0
    text = RULE + "\n正式名詞（" + str(len(names)) + " 個）：" + "、".join(names)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
