#!/usr/bin/env python3
"""產生審閱頁的標示版：新增用綠底 <mark>，刪除（被取代或拿掉的舊文字）用紅底 <mark>。

底線 <ins> 是名詞標記，所以改動不用底線，避免兩種意思混在一起。

用法：
    python3 script/mark_changes.py <舊版後綴> <檔名…>
例：
    python3 script/mark_changes.py pre_r63 01_purpose 02_invariants
    python3 script/mark_changes.py pre_r91 README.md          # 其他檔傳路徑
    python3 script/mark_changes.py new doc/contract/README.md   # 新建的檔：整份標新增

舊版讀 doc/decisions/_backup/doc_contract_<name>.<後綴>.md（docs/ 併進 doc/ 之前的 docs_contract_<name>、
更早的 doc_decisions_review_<name> 也認），
新版讀 doc/contract/<name>.md，
輸出 doc/decisions/_marked/<鍵>.v<N>.marked.md（審閱頁的鍵是頁名，其他檔是攤平後的路徑）。

標示版與正文副本裡的相對連結會改寫成從 _marked/ 出發（錨點照留；指到其他審閱頁的
連結指正式檔，不指版本副本），放到 _marked/ 後才不會因為深度不同而指錯；原檔不動。

標題行（# 開頭）保持原樣、不加標籤，否則檢視器產生的錨點會含標籤文字，目錄連結
跳不過去：新增的標題在下一行註記「（本節新增）」，改過的標題在下一行標紅舊標題並註記
「（標題已修改）」，刪掉的標題去掉 # 以紅底呈現在普通文字行。

表格列（以 | 開頭）在儲存格內標記，不把整列包起來——整列包住會讓那一列
不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
"""
import difflib
import json
import os
import re
import pathlib
import sys

REVIEW = pathlib.Path("doc/contract")
BACKUP = pathlib.Path("doc/decisions/_backup")
MARKED = pathlib.Path("doc/decisions/_marked")
# 各鍵最後產出的版本號；進 git（_marked/ 不進 git）
VERSIONS = pathlib.Path("doc/decisions/review_log/versions.json")


def mark(body: str, tag: str) -> str:
    """新增用綠底 <mark>，刪除（被取代或拿掉的舊文字）用紅底 <mark>。

    tag 是 "ins"（新增）或 "del"（刪除），只用來選顏色，輸出一律是 <mark>。
    GitHub 會濾掉內嵌樣式；標示版只在本地 review 用、不進 git。
    """
    if tag == "ins":
        return '<mark style="background-color:#c8f0c8">' + body + "</mark>"
    return '<mark style="background-color:#f8c8c8">' + body + "</mark>"


def wrap(line: str, tag: str) -> str:
    """把一行包成新增或刪除的 <mark>（tag 是 "ins" 或 "del"）。

    清單、引言的行首記號留在標籤外；表格列改成逐格包，整列包住會切斷表格。
    標題行不經過這裡：build() 讓標題保持原樣，改動註記在下一行。
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


# 行內連結與圖片：](目標) 或 ](<目標>)，後面可接 "標題"
LINK = re.compile(r'(\]\()(\s*)(<[^>\n]*>|[^\s()<>]+)((?:\s+"[^"\n]*")?\s*\))')
# 反引號包住的行內程式碼：裡面的字樣不改
CODE_SPAN = re.compile(r"(`+)(?:.+?)\1")
FENCE = re.compile(r"^\s*(```|~~~)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def relink(dest: str, src: pathlib.Path) -> str:
    """把一個連結目標改寫成從 MARKED 出發；外部網址、純錨點、根目錄絕對路徑原樣回傳。"""
    angled = dest.startswith("<") and dest.endswith(">")
    raw = dest[1:-1] if angled else dest
    if not raw or raw.startswith(("#", "/")) or SCHEME.match(raw):
        return dest
    file_part, sep, anchor = raw.partition("#")
    if not file_part:
        return dest
    resolved = os.path.normpath(os.path.join(src.parent.as_posix(), file_part))
    new = os.path.relpath(resolved, MARKED.as_posix()).replace(os.sep, "/")
    if file_part.endswith("/") and not new.endswith("/"):
        new += "/"
    new += sep + anchor
    return f"<{new}>" if angled else new


def rewrite_links(text: str, src: pathlib.Path) -> str:
    """把 src 裡照原位置寫的相對連結改寫成從 MARKED 出發；程式碼區塊與行內程式碼不動。"""
    out = []
    fence = None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence:
            if m and m.group(1) == fence:
                fence = None
            out.append(line)
            continue
        if m:
            fence = m.group(1)
            out.append(line)
            continue
        parts, pos = [], 0
        for cm in CODE_SPAN.finditer(line):
            parts.append(LINK.sub(lambda l: l.group(1) + l.group(2) + relink(l.group(3), src) + l.group(4),
                                  line[pos:cm.start()]))
            parts.append(cm.group(0))
            pos = cm.end()
        parts.append(LINK.sub(lambda l: l.group(1) + l.group(2) + relink(l.group(3), src) + l.group(4),
                              line[pos:]))
        out.append("".join(parts))
    return "\n".join(out)


def next_rev(name: str) -> int:
    """下一個版本號：取 VERSIONS 裡這個鍵的號碼加一，並寫回。

    VERSIONS 進 git，換電腦或新 clone 也接得上；版本號只放在 _marked/ 的檔名，
    正式檔裡不寫（檔名已經說了是哪一版）。
    """
    table = json.loads(VERSIONS.read_text()) if VERSIONS.exists() else {}
    n = int(table.get(name, 0)) + 1
    table[name] = n
    VERSIONS.parent.mkdir(parents=True, exist_ok=True)
    VERSIONS.write_text(json.dumps(table, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return n


def target(name: str) -> tuple[pathlib.Path, str]:
    """回傳（正式檔路徑, 標示版與備份用的鍵）。

    - 審閱頁照舊傳頁名（不含 .md），例如 04_interface → doc/contract/04_interface.md，鍵是頁名。
    - 其他檔傳相對 repo 根目錄的路徑，例如 README.md、doc/contract/README.md；
      鍵是攤平後的路徑（/ 換成 _、去掉 .md），跟備份檔的攤平命名一致。
    """
    if "/" in name or name.endswith(".md"):
        path = pathlib.Path(name)
        # 開頭的點要去掉，否則 .claude/… 會攤平成隱藏檔
        return path, str(path.with_suffix("")).replace("/", "_").lstrip(".")
    return REVIEW / f"{name}.md", name


def backup_path(name: str, suffix: str) -> pathlib.Path:
    """備份檔的四種命名都認：攤平的（doc_contract_<name>）、docs/ 併進 doc/ 之前的
    攤平命名（docs_contract_<name>）、審閱頁搬到 docs/contract/ 之前的攤平命名
    （doc_decisions_review_<name>），與 review/ 子目錄的。

    攤平是主要慣例（doc-apply workflow 與各子代理都用它，因為它對任何路徑都成立）；
    後三種是搬目錄前的歷史寫法，留著讀得到舊備份就好，不要再產生新的。
    以路徑指定的檔同理：doc/<子目錄>/… 攤平成 doc_<子目錄>_…，也認併目錄前的 docs_<子目錄>_…。
    """
    path, key = target(name)
    if key != name:  # 以路徑指定的檔：備份就是攤平後的路徑
        keys = [key]
        if key.startswith("doc_"):
            keys.append("docs_" + key[len("doc_"):])  # docs/ 併進 doc/ 之前的備份
        tried = []
        for k in keys:
            # 備份檔也可能照原路徑攤平、保留開頭的點（例如 .claude_workflows_README），兩種都認
            for flat in (BACKUP / f"{k}.{suffix}.md", BACKUP / f".{k}.{suffix}.md"):
                tried.append(flat)
                if flat.exists():
                    return flat
        raise SystemExit(
            f"找不到 {name} 的基準版。試過：\n  " + "\n  ".join(map(str, tried))
            + "\n改檔之前要先備份，命名見 script/README.md。"
        )
    flat = BACKUP / f"doc_contract_{name}.{suffix}.md"
    pre_merge = BACKUP / f"docs_contract_{name}.{suffix}.md"
    old_flat = BACKUP / f"doc_decisions_review_{name}.{suffix}.md"
    nested = BACKUP / "review" / f"{name}.{suffix}.md"
    for candidate in (flat, pre_merge, old_flat, nested):
        if candidate.exists():
            return candidate
    raise SystemExit(
        f"找不到 {name} 的基準版。試過：\n  {flat}\n  {pre_merge}\n  {old_flat}\n  {nested}\n"
        f"改檔之前要先備份，命名見 script/README.md。"
    )


HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)(?:\s+#+)?\s*$")
ADDED_NOTE = mark("（本節新增）", "ins")
CHANGED_NOTE = mark("（標題已修改）", "ins")


def headings(lines: list[str]) -> set[int]:
    """回傳是標題的行號（程式碼區塊裡以 # 開頭的行不算）。"""
    found, fence = set(), None
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if fence:
            if m and m.group(1) == fence:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        if HEADING.match(line):
            found.add(i)
    return found


def heading_text(line: str) -> str:
    return HEADING.match(line).group(1)


def build(name: str, suffix: str) -> tuple[int, int]:
    path, key = target(name)
    # 基準後綴寫 new 表示這個檔是新建的：沒有舊版，整份都標成新增
    old = [] if suffix == "new" else backup_path(name, suffix).read_text().splitlines()
    new = path.read_text().splitlines()
    old_heads, new_heads = headings(old), headings(new)
    out = []
    ins = dele = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, old, new, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            out.extend(new[j1:j2])
            continue
        # 標題行保持原樣、不加任何標籤：檢視器用標題的文字產生錨點，
        # 標籤混進去錨點就變了，目錄連結跳不過去。改動改在標題下一行註記。
        # 同一段改動裡的舊標題與新標題依序配對，配到的算「標題已修改」。
        gone = [i for i in range(i1, i2) if i in old_heads]
        came = [j for j in range(j1, j2) if j in new_heads]
        renamed = dict(zip(came, gone))
        for i in range(i1, i2):
            line = old[i]
            if not line.strip() or i in renamed.values():
                continue
            # 刪掉的標題：去掉行首的 #，當成普通文字標紅，不產生錨點
            out.append(mark(heading_text(line), "del") if i in old_heads else wrap(line, "del"))
            dele += 1
        for j in range(j1, j2):
            line = new[j]
            if j in new_heads:
                out.append(line)
                if j in renamed:
                    out.append(mark("舊標題：" + heading_text(old[renamed[j]]), "del"))
                    out.append(CHANGED_NOTE)
                    dele += 1
                else:
                    out.append(ADDED_NOTE)
                # 註記自成一段，不跟下一行的清單或表格黏在一起
                if j + 1 < len(new) and new[j + 1].strip():
                    out.append("")
            else:
                out.append(wrap(line, "ins"))
            if line.strip():
                ins += 1
    rev = next_rev(key)
    MARKED.mkdir(parents=True, exist_ok=True)
    header = [
        f"<!-- 標示版 v{rev}：綠底 <mark> 是新增、紅底 <mark> 是刪除；底線 <ins> 是名詞標記；本檔只供本地 review，不進 git；"
        f"基準 {suffix}。正式內容看 /{path.as_posix()} -->",
        "",
    ]
    for old_file in list(MARKED.glob(f"{key}.v*.marked.md")) + list(MARKED.glob(f"{key}.v*[0-9].md")):
        old_file.unlink()
    # 同一版的正文副本，檔名帶版本號：送審時跟標示版一起給，不用打開檔案才知道是哪一版。
    # 正式檔名（沒有版本號）不動，其他文件的連結才不會斷。
    # 兩份都放在 _marked/，相對連結要改寫成從 _marked/ 出發才不會指錯
    (MARKED / f"{key}.v{rev}.md").write_text(rewrite_links(path.read_text(), path))
    (MARKED / f"{key}.v{rev}.marked.md").write_text(rewrite_links("\n".join(header + out) + "\n", path))
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
