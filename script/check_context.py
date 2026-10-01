#!/usr/bin/env python3
"""檢查根 GLOSSARY.md：照 domain-modeling skill 的格式（.claude/skills/domain-modeling/CONTEXT-FORMAT.md）。

- `## Language` 底下用 `### 分群` 分群，名詞一行 `**名詞** (english)：`（舊寫法 `**名詞**（英文）：` 也認），下一行起是定義，可接 `_Avoid_:`。
- 不寫目錄、不寫 HTML 錨點：skill 沒有這些；不准任何 HTML 標籤（`<ins>` 也不放行；名詞改連到 GLOSSARY.md 分群）。
- `_Avoid_` 詞不得出現在正文。

用法：python3 script/check_context.py [GLOSSARY.md]
成功印 OK 並回 0；有問題逐條印出並回 1。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 英文注名兩種寫法都認：全形「**X**（y）：」與半形「**X** (y)：」（括號內全 ASCII 時用半形並空一格）。
TERM = re.compile(r"^\*\*(.+?)\*\*(（[^）]*）| \([^)]*\))?[:：]\s*$")
# 看起來像名詞行（粗體開頭、冒號結尾）卻不合 TERM：寫法改了而 regex 沒跟上時會靜默少算，所以報錯。
LOOKS_LIKE_TERM = re.compile(r"^\*\*.+\*\*.*[:：]\s*$")
TAG = re.compile(r"<(/?)([a-zA-Z][\w-]*)[^>]*>")


def bare(line: str) -> str:
    """拿掉行內程式碼：`<repo>` 這類占位符寫在反引號裡，不算 HTML。"""
    return re.sub(r"`[^`]*`", "", line)


def main(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    errs = []
    try:
        lang = next(i for i, ln in enumerate(lines) if ln.strip() == "## Language")
    except StopIteration:
        print("找不到 '## Language'")
        return 1

    fence = False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        bad = sorted({name for _, name in TAG.findall(bare(ln))})
        if bad:
            errs.append(f"第 {i} 行用了 HTML {bad}：不准任何 HTML 標籤；名詞連到 GLOSSARY.md，錨點用標題產生")
    if any(ln.strip() == "## 目錄" for ln in lines):
        errs.append("有「## 目錄」：skill 的格式沒有目錄，分群標題本身就是大綱")

    groups, terms = [], []
    body = lines[lang + 1:]
    for i, ln in enumerate(body):
        if ln.startswith("### "):
            groups.append(ln[4:].strip())
            continue
        m = TERM.match(ln)
        if not m:
            if LOOKS_LIKE_TERM.match(ln):
                errs.append(f"正文第 {lang + i + 2} 行像名詞行但格式不認得：{ln.strip()}；用 `**名詞** (english)：` 或 `**名詞**（中文注名）：`")
            continue
        if not groups:
            errs.append(f"名詞 {m.group(1)} 不在任何 ### 分群底下")
        nxt = body[i + 1].strip() if i + 1 < len(body) else ""
        if not nxt or nxt.startswith(("**", "_Avoid_", "#")):
            errs.append(f"名詞 {m.group(1)} 下一行沒有定義")
        terms.append(m.group(1))
    dup = sorted({t for t in terms if terms.count(t) > 1})
    if dup:
        errs.append(f"名詞重複：{dup}")

    avoid = set()
    for ln in body:
        if ln.startswith("_Avoid_:"):
            for w in ln[len("_Avoid_:"):].split("、"):
                w = w.strip().strip("`")
                if w:
                    avoid.add(w)
    for i, ln in enumerate(body):
        if ln.startswith("_Avoid_:"):
            continue
        for w in avoid:
            if w in ln:
                errs.append(f"正文第 {lang + i + 2} 行出現 _Avoid_ 詞 {w!r}：{ln.strip()}")

    for e in errs:
        print(e)
    print(f"{'OK' if not errs else 'FAIL'}: 分群 {len(groups)}、名詞 {len(terms)}、_Avoid_ 詞 {len(avoid)}")
    return 1 if errs else 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "GLOSSARY.md"
    sys.exit(main(target))
