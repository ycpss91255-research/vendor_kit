#!/usr/bin/env python3
"""產生審閱頁的標示版：改動處底線 <ins>、被取代的舊文字刪除線 <del>。

用法：
    python3 script/mark_changes.py <舊版後綴> <檔名…>
例：
    python3 script/mark_changes.py pre_r63 01_purpose 02_terms 03_invariants

舊版讀 doc/decisions/_backup/review/<name>.<後綴>.md，
新版讀 doc/decisions/review/<name>.md，
輸出 doc/decisions/review/_marked/<name>.marked.md。

表格列（以 | 開頭）在儲存格內標記，不把整列包起來——整列包住會讓那一列
不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
"""
import difflib
import re
import pathlib
import sys

REVIEW = pathlib.Path("doc/decisions/review")
BACKUP = pathlib.Path("doc/decisions/_backup/review")
MARKED = REVIEW / "_marked"


def wrap(line: str, tag: str) -> str:
    """把一行包成 <ins>／<del>。

    標題、清單、引言的行首記號留在標籤外，否則 `<ins>## 目錄</ins>` 會讓標題
    變成普通文字；表格列改成逐格包，整列包住會切斷表格。
    """
    if not line.strip():
        return line
    if line.lstrip().startswith("|"):
        cells = line.split("|")
        out = []
        for cell in cells:
            body = cell.strip()
            if body and not set(body) <= set("-: "):  # 跳過分隔列
                out.append(f" <{tag}>{body}</{tag}> ")
            else:
                out.append(cell)
        return "|".join(out)
    m = re.match(r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+|>\s*)?)(.*)$", line)
    prefix, body = m.group(1), m.group(2)
    if not body.strip():
        return line
    return f"{prefix}<{tag}>{body}</{tag}>"


def mark(name: str, suffix: str) -> tuple[int, int]:
    old = (BACKUP / f"{name}.{suffix}.md").read_text().splitlines()
    new = (REVIEW / f"{name}.md").read_text().splitlines()
    out = []
    ins = dele = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, old, new, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            out.extend(new[j1:j2])
            continue
        for line in old[i1:i2]:
            if line.strip():
                out.append(wrap(line, "del"))
                dele += 1
        for line in new[j1:j2]:
            out.append(wrap(line, "ins"))
            if line.strip():
                ins += 1
    header = [
        f"<!-- 標示版：改動處底線 <ins>、被取代的舊文字刪除線 <del>；"
        f"基準 {suffix}。正式內容看 ../{name}.md -->",
        "",
    ]
    MARKED.mkdir(exist_ok=True)
    (MARKED / f"{name}.marked.md").write_text("\n".join(header + out) + "\n")
    return ins, dele


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    suffix, names = sys.argv[1], sys.argv[2:]
    for name in names:
        ins, dele = mark(name, suffix)
        print(f"{name}: {ins} ins, {dele} del")


if __name__ == "__main__":
    main()
