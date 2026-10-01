#!/usr/bin/env python3
"""產生審閱頁的標示版：新增綠底、被取代的舊文字紅底。

底線 <u> 是名詞標記，所以改動不用底線，避免兩種意思混在一起。

用法：
    python3 script/doc/mark_changes.py <舊版後綴> <檔名…>
例：
    python3 script/doc/mark_changes.py pre_r63 01_purpose 02_invariants

舊版讀 doc/decisions/_backup/doc_decisions_review_<name>.<後綴>.md，
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
BACKUP = pathlib.Path("doc/decisions/_backup")
MARKED = REVIEW / "_marked"


def mark(body: str, tag: str) -> str:
    """新增用綠底、被取代的舊文字用紅底。

    標示版只在本地 review 用、不進 git，所以可以用 GitHub 會濾掉的內嵌樣式。
    """
    color = "#c8f7c5" if tag == "ins" else "#ffc9c9"
    return '<mark style="background:' + color + '">' + body + "</mark>"


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
                out.append(f" {mark(body, tag)} ")
            else:
                out.append(cell)
        return "|".join(out)
    m = re.match(r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+|>\s*)?)(.*)$", line)
    prefix, body = m.group(1), m.group(2)
    if not body.strip():
        return line
    return f"{prefix}{mark(body, tag)}"


def next_rev(name: str) -> int:
    """每產一次標示版就把版本號加一，檔名帶 v<N> 方便分辨新舊。"""
    f = MARKED / f".{name}.rev"
    n = int(f.read_text().strip()) + 1 if f.exists() else 1
    MARKED.mkdir(exist_ok=True)
    f.write_text(str(n))
    return n


def backup_path(name: str, suffix: str) -> pathlib.Path:
    """備份檔的兩種命名都認：攤平的（doc_decisions_review_<name>）與 review/ 子目錄的。

    攤平是主要慣例（doc-apply workflow 與各子代理都用它，因為它對任何路徑都成立）；
    review/ 子目錄是早期寫法，留著讀得到就好，不要再產生新的。
    """
    flat = BACKUP / f"doc_decisions_review_{name}.{suffix}.md"
    nested = BACKUP / "review" / f"{name}.{suffix}.md"
    for candidate in (flat, nested):
        if candidate.exists():
            return candidate
    raise SystemExit(
        f"找不到 {name} 的基準版。試過：\n  {flat}\n  {nested}\n"
        f"改檔之前要先備份，命名見 script/doc/README.md。"
    )


def build(name: str, suffix: str) -> tuple[int, int]:
    old = backup_path(name, suffix).read_text().splitlines()
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
    rev = next_rev(name)
    header = [
        f"<!-- 標示版 v{rev}：綠底是新文字、紅底是被取代的舊文字；底線 <u> 是名詞標記；本檔只供本地 review，不進 git；"
        f"基準 {suffix}。正式內容看 ../{name}.md -->",
        "",
    ]
    MARKED.mkdir(exist_ok=True)
    for old_file in MARKED.glob(f"{name}.v*.marked.md"):
        old_file.unlink()
    (MARKED / f"{name}.v{rev}.marked.md").write_text("\n".join(header + out) + "\n")
    return ins, dele


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    suffix, names = sys.argv[1], sys.argv[2:]
    for name in names:
        ins, dele = build(name, suffix)
        print(f"{name}: {ins} ins, {dele} del")


if __name__ == "__main__":
    main()
