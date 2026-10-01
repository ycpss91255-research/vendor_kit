#!/usr/bin/env python3
"""產生審閱頁的標示版：新增用綠底 <mark>，刪除（被取代或拿掉的舊文字）用紅底 <mark>。

名詞連到 GLOSSARY.md 分群、不用底線；改動也不用底線。

用法：
    python3 script/doc/mark_changes.py <檔名…>                      # 基準：該鍵維護者最後一次回覆過的版本；已定案的鍵用定案版（未改就不產檔）
    python3 script/doc/mark_changes.py --base-version 03_output=13 GLOSSARY=6   # 指定送審版本當基準
    python3 script/doc/mark_changes.py <舊版後綴> <檔名…>           # 本機 _backup 的改前快照當基準
例：
    python3 script/doc/mark_changes.py 01_purpose 02_invariants README.md
    python3 script/doc/mark_changes.py pre_r63 01_purpose 02_invariants
    python3 script/doc/mark_changes.py new doc/contract/README.md   # 新建的檔：整份標新增

審閱頁傳頁名（新版讀 doc/contract/<name>.md），其他檔傳路徑；--base-version 左邊也可以直接寫鍵
（GLOSSARY 對到根目錄的 GLOSSARY.md）。鍵：審閱頁是頁名，其他檔是攤平後的路徑。
第一個參數是 new、或對不到任何檔時，當成舊版後綴。

輸出到送審資料夾 doc/review/<鍵>/，檔名固定、不帶版本號，每次產生就覆蓋：
<鍵>.md（正文副本）、<鍵>.marked.md（標示版），有同名 CSV 的審閱頁再加 <鍵>.csv。
版本號不寫在檔名或檔內：送審的版號與送審當時的 commit 記在 doc/review/versions.json，
由 pack_review.py 打包時取號並寫進 zip 內的檔名；維護者回覆後用 pack_review.py --replied 把那筆標成
replied: true。這支只讀 versions.json，不寫。

送審資料夾是「維護者要審的」：基準是維護者最後一次回覆過的那一版，看過的內容不再標紅綠，只標之後的改動。
- 已定案的鍵：正式檔與定案 commit 相同就不產生送審檔，並刪除殘留的該鍵資料夾；
  定案後又有改動就以定案版為基準重新產生，回到待審。
- 不帶後綴：versions.json 裡該鍵最後一筆 replied: true 的紀錄；沒有就整份標新增
  （送出後還沒回覆的版本不算，否則重產時會以剛送出的版本自己為基準，紅綠全不見）。
- --base-version <鍵>=<N>：versions.json 裡該鍵版本 N 的紀錄（不論有沒有回覆）。
  兩種都用 git show <commit>:<路徑> 取基準：紀錄有 path 就取那個路徑（例如當時進 git 的正文副本），
  沒有就取正式檔路徑；CSV 同理，看 csv_path。副本裡的相對連結是從副本所在目錄寫的，比對前先改寫回
  正式檔的位置；紀錄帶 raw_links: true 表示副本的連結照正式檔位置寫、不改寫。
  基準 commit 裡沒有那份 CSV 時視為新建、整份標新增。找不到指定版號就停下報錯，整批不產。
- <舊版後綴>：讀本機 doc/decisions/_backup/doc_contract_<name>.<後綴>.md（docs/ 併進 doc/ 之前的
  docs_contract_<name>、更早的 doc_decisions_review_<name> 也認）。_backup/ 不進 git，本機沒有就報錯。

標示版與正文副本裡的相對連結會改寫成從 doc/review/<鍵>/ 出發（錨點照留；指到其他審閱頁的
連結指正式檔），放進送審資料夾後才不會因為深度不同而指錯；原檔不動。

標題行（# 開頭）保持原樣、不加標籤，否則檢視器產生的錨點會含標籤文字，目錄連結
跳不過去：新增的標題在下一行註記「（本節新增）」，改過的標題在下一行標紅舊標題並註記
「（標題已修改）」，刪掉的標題去掉 # 以紅底呈現在普通文字行。

表格列（以 | 開頭）在儲存格內標記，不把整列包起來——整列包住會讓那一列
不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。

審閱頁旁邊有同名的 CSV（例如 doc/contract/03_output.csv，#122）時，一個頁名同時處理兩個檔：
輸出 <鍵>.md、<鍵>.csv，與一份合併的 <鍵>.marked.md——前半是
.md 的逐行差異，後半是 CSV 的逐碼差異（依 code 對齊、逐欄比較，只列有改動的代碼）。
表頭改了（例如刪掉 note 欄）時，後半開頭先標出新舊表頭；刪掉的欄在各碼照樣列出舊值並標紅。
表頭新增欄位（例如在 level 後新增 exit_code、在 message 後新增 description）也會依新表頭的位置
列入逐碼差異；欄位順序一律以新版表頭為準，已刪欄位才接在最後。
後綴模式下 CSV 的基準版是 _backup/doc_contract_<name>.<後綴>.csv；傳 doc/contract/<name>.csv 等於傳頁名。
兩個檔只有一個有基準版時，另一個視為這一輪沒改（CSV 不在 git 的 HEAD 裡則視為新建、整份標新增），
並在輸出與標示版開頭註明。
"""
import csv
import difflib
import html
import subprocess
import json
import os
import re
import pathlib
import shutil
import sys

REVIEW = pathlib.Path("doc/contract")
# 本機的改前快照，不進 git（#128）；只有後綴模式讀它
BACKUP = pathlib.Path("doc/decisions/_backup")
# 送審資料夾：每個鍵一個子資料夾，進 git；定案後不保留該鍵的送審資料
REVIEW_OUT = pathlib.Path("doc/review")
# 每個鍵送審過的版號與送審當時的 commit；進 git。只有 pack_review.py 寫它
VERSIONS = REVIEW_OUT / "versions.json"
ZIP_KEY = "review_zip"
# 改過名的正式檔：新路徑 → 改名前的路徑（#137：03_messages 改名為 03_output）。
# 送審紀錄沒寫 path／csv_path 時，基準在紀錄的 commit 裡找不到新路徑，就改取改名前的路徑；
# 基準裡連到改名前路徑的連結也換成新路徑，只因改名而不同的行不標成改動。
RENAMED = {
    REVIEW / "03_output.md": REVIEW / "03_messages.md",
    REVIEW / "03_output.csv": REVIEW / "03_messages.csv",
}
RENAMED_FROM = {old: new for new, old in RENAMED.items()}


def mark(body: str, tag: str) -> str:
    """新增用綠底 <mark>，刪除（被取代或拿掉的舊文字）用紅底 <mark>。

    tag 是 "ins"（新增）或 "del"（刪除），只用來選顏色，輸出一律是 <mark>。
    GitHub 會濾掉內嵌樣式；標示版進 git，定案時刪除該鍵的送審資料夾。
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


def out_dir(key: str) -> pathlib.Path:
    """這個鍵的送審資料夾 doc/review/<鍵>/。"""
    return REVIEW_OUT / key


def relink(dest: str, src: pathlib.Path, base: pathlib.Path) -> str:
    """把一個連結目標改寫成從 base 目錄出發；外部網址、純錨點、根目錄絕對路徑原樣回傳。"""
    angled = dest.startswith("<") and dest.endswith(">")
    raw = dest[1:-1] if angled else dest
    if not raw or raw.startswith(("#", "/")) or SCHEME.match(raw):
        return dest
    file_part, sep, anchor = raw.partition("#")
    if not file_part:
        return dest
    resolved = os.path.normpath(os.path.join(src.parent.as_posix(), file_part))
    new = os.path.relpath(resolved, base.as_posix()).replace(os.sep, "/")
    if file_part.endswith("/") and not new.endswith("/"):
        new += "/"
    new += sep + anchor
    return f"<{new}>" if angled else new


def rewrite_links(text: str, src: pathlib.Path, base: pathlib.Path) -> str:
    """把 src 裡照原位置寫的相對連結改寫成從 base 目錄出發；程式碼區塊與行內程式碼不動。"""
    return map_links(text, lambda dest: relink(dest, src, base))


def follow_rename(dest: str, where: pathlib.Path) -> str:
    """從 where 目錄寫的連結若指到改名前的正式檔，換成改名後的路徑（錨點照留）；其他連結原樣回傳。"""
    angled = dest.startswith("<") and dest.endswith(">")
    raw = dest[1:-1] if angled else dest
    if not raw or raw.startswith(("#", "/")) or SCHEME.match(raw):
        return dest
    file_part, sep, anchor = raw.partition("#")
    if not file_part:
        return dest
    resolved = pathlib.Path(os.path.normpath(os.path.join(where.as_posix(), file_part)))
    renamed = RENAMED_FROM.get(resolved)
    if renamed is None:
        return dest
    new = os.path.relpath(renamed.as_posix(), where.as_posix()).replace(os.sep, "/") + sep + anchor
    return f"<{new}>" if angled else new


def follow_renames(text: str, official: pathlib.Path) -> str:
    """基準文字（照 official 的位置寫連結）裡指到改名前正式檔的連結，換成改名後的路徑。

    不換的話，只因為改名，基準裡每一行連到那頁的文字都會被標成改動（#137）。
    """
    return map_links(text, lambda dest: follow_rename(dest, official.parent))


def map_links(text: str, fix) -> str:
    """把每個行內連結目標交給 fix 改寫；程式碼區塊與行內程式碼裡的字樣不動。"""
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
            parts.append(LINK.sub(lambda l: l.group(1) + l.group(2) + fix(l.group(3)) + l.group(4),
                                  line[pos:cm.start()]))
            parts.append(cm.group(0))
            pos = cm.end()
        parts.append(LINK.sub(lambda l: l.group(1) + l.group(2) + fix(l.group(3)) + l.group(4),
                              line[pos:]))
        out.append("".join(parts))
    return "\n".join(out)


def load_versions() -> dict:
    """讀 versions.json。

    pages.<鍵> 是送審版本陣列；finalized.<鍵> 記定案的 {"v": N, "commit": "<sha>"}，
    那版紀錄有 path、csv_path、raw_links 時也照抄。
    每筆版本還可以帶 path、csv_path 與 raw_links。
    檔案不存在就當成從沒送審過；沒寫 replied 的紀錄當成還沒回覆。
    """
    table = json.loads(VERSIONS.read_text()) if VERSIONS.exists() else {}
    table.setdefault(ZIP_KEY, 0)
    table.setdefault("pages", {})
    return table


def save_versions(table: dict) -> None:
    for entries in table["pages"].values():
        entries.sort(key=lambda e: e["v"])
    VERSIONS.parent.mkdir(parents=True, exist_ok=True)
    VERSIONS.write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n")


def page_versions(key: str, table: dict | None = None) -> list[dict]:
    """該鍵的送審版本紀錄。"""
    return (table or load_versions())["pages"].get(key, [])


def finalized(key: str, table: dict | None = None) -> dict | None:
    """該鍵的定案紀錄（至少有 v、commit）；未定案回 None。"""
    table = table or load_versions()
    return table.get("finalized", {}).get(key)


def last_sent(key: str, table: dict | None = None) -> dict | None:
    """該鍵最後一次送審的紀錄 {"v", "commit"}；從沒送審過回 None。"""
    entries = page_versions(key, table)
    return max(entries, key=lambda e: e["v"]) if entries else None


def last_replied(key: str, table: dict | None = None) -> dict | None:
    """該鍵最後一筆 replied: true 的紀錄；沒有回 None。"""
    entries = [e for e in page_versions(key, table) if e.get("replied") is True]
    return max(entries, key=lambda e: e["v"]) if entries else None


def sent_version(key: str, v: int, table: dict | None = None) -> dict | None:
    """該鍵送審版本 v 的紀錄；沒有回 None。"""
    for entry in page_versions(key, table):
        if entry["v"] == v:
            return entry
    return None


def git_show(commit: str, path: pathlib.Path) -> str | None:
    """git show <commit>:<path> 的內容；那個 commit 裡沒有這個檔回 None。"""
    try:
        proc = subprocess.run(["git", "show", f"{commit}:{path.as_posix()}"], capture_output=True)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8")


def base_text(entry: dict, field: str, official: pathlib.Path) -> tuple[pathlib.Path, str | None]:
    """紀錄的基準內容：回傳（取用的路徑, git show 的內容或 None）。

    field 是 path 或 csv_path：紀錄有這欄就從那個路徑取，沒有就取正式檔路徑；正式檔改過名
    （RENAMED）而那個 commit 裡還沒有新路徑時，取改名前的路徑。
    從副本取的 .md 先把相對連結改寫回正式檔的位置（副本的連結是從副本所在目錄寫的），
    否則每一行連結都會被當成改動；紀錄帶 raw_links: true 時副本照正式檔位置寫，不改寫。
    """
    src = pathlib.Path(entry[field]) if entry.get(field) else official
    text = git_show(entry["commit"], src)
    if text is None and not entry.get(field) and official in RENAMED:
        src = RENAMED[official]
        text = git_show(entry["commit"], src)
    if text is not None and src != official and official.suffix == ".md" and not entry.get("raw_links"):
        text = rewrite_links(text, src, official.parent)
    if text is not None and official.suffix == ".md":
        text = follow_renames(text, official)
    return src, text


def normalize(name: str) -> str:
    """doc/contract/<頁>.csv 等於傳頁名：CSV 是那一頁的附屬資料，跟 .md 一起產標示版、共用版本號。"""
    path = pathlib.Path(name)
    if path.suffix == ".csv" and path.parent == REVIEW:
        return path.stem
    return name


def companion_csv(name: str) -> pathlib.Path | None:
    """審閱頁旁邊的同名 CSV（例如 03_output.csv）；沒有就回 None。以路徑指定的檔沒有附屬 CSV。"""
    if "/" in name or name.endswith(".md"):
        return None
    path = REVIEW / f"{name}.csv"
    return path if path.exists() else None


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


def find_backup(name: str, suffix: str, ext: str = ".md") -> tuple[pathlib.Path | None, list[pathlib.Path]]:
    """回傳（找到的基準版或 None, 試過的路徑）。命名規則見 backup_path()。"""
    path, key = target(name)
    tried: list[pathlib.Path] = []
    if key != name:
        keys = [key]
        if key.startswith("doc_"):
            keys.append("docs_" + key[len("doc_"):])
        for k in keys:
            tried += [BACKUP / f"{k}.{suffix}{ext}", BACKUP / f".{k}.{suffix}{ext}"]
    else:
        tried = [
            BACKUP / f"doc_contract_{name}.{suffix}{ext}",
            BACKUP / f"docs_contract_{name}.{suffix}{ext}",
            BACKUP / f"doc_decisions_review_{name}.{suffix}{ext}",
            BACKUP / "review" / f"{name}.{suffix}{ext}",
        ]
    for candidate in tried:
        if candidate.exists():
            return candidate, tried
    return None, tried


def backup_path(name: str, suffix: str, ext: str = ".md") -> pathlib.Path:
    """備份檔的四種命名都認：攤平的（doc_contract_<name>）、docs/ 併進 doc/ 之前的
    攤平命名（docs_contract_<name>）、審閱頁搬到 docs/contract/ 之前的攤平命名
    （doc_decisions_review_<name>），與 review/ 子目錄的。

    攤平是主要慣例（doc-edit 與各子代理都用它，因為它對任何路徑都成立）；
    後三種是搬目錄前的歷史寫法，留著讀得到舊備份就好，不要再產生新的。
    以路徑指定的檔同理：doc/<子目錄>/… 攤平成 doc_<子目錄>_…，也認併目錄前的 docs_<子目錄>_…。
    ext 是副檔名：審閱頁旁的 CSV 用 ".csv"（doc_contract_<name>.<後綴>.csv；歷史命名不會有 CSV）。
    """
    found, tried = find_backup(name, suffix, ext)
    if found is None:
        raise SystemExit(
            f"找不到 {name} 的基準版。試過：\n  " + "\n  ".join(map(str, tried))
            + "\n改檔之前要先備份，命名見 script/doc/README.md。"
        )
    return found


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


def diff_md(old: list[str], new: list[str]) -> tuple[list[str], int, int]:
    """逐行比較，回傳（標示後的行, 新增數, 刪除數）。"""
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
    return out, ins, dele


def read_rows(text: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    """CSV 文字（可帶 BOM）→（欄名, code → 列）。"""
    reader = csv.DictReader(text.lstrip("\ufeff").splitlines(keepends=True))
    rows = {row.get("code", ""): row for row in reader}
    return list(reader.fieldnames or []), rows


def show(value: str) -> str:
    """CSV 欄位值放進 Markdown：<repo> 這類占位符要照原樣看得到，換行改成 <br>。"""
    if value == "":
        return "（空）"
    return html.escape(value, quote=False).replace("\n", "<br>")


CODE_ADDED = mark("（本碼新增）", "ins")
CODE_RETIRED = mark("（本碼停用）", "del")
CODE_REMOVED = mark("（本列刪除）", "del")
COLUMN_REMOVED = mark("（本欄刪除）", "del")
COLUMN_ADDED = mark("（本欄新增）", "ins")


def diff_csv(old_text: str | None, new_text: str, name: str) -> tuple[list[str], int, int]:
    """依 code 對齊、逐欄比較；只列有改動的代碼，每碼一段 #### VKnnnn。回傳（行, 新增數, 刪除數）。

    old_text 是 None 表示 CSV 是新建的：每個代碼都算新增。
    欄位照新表頭的順序，新表頭拿掉的欄接在後面：
    刪掉的欄在表頭與各碼都標紅，否則只刪欄的代碼會被當成沒改動。
    新表頭新增的欄在各碼標綠新值並註記（本欄新增）；舊值是空的不算改動。
    """
    old_fields, old_rows = read_rows(old_text) if old_text is not None else ([], {})
    new_fields, new_rows = read_rows(new_text)
    removed = [f for f in old_fields if f not in new_fields]
    added = [f for f in new_fields if f not in old_fields] if old_text is not None else []
    fields = new_fields + removed
    out = ["---", "", f"## {name}.csv 的逐碼差異", "",
           "依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。", ""]
    if removed or added:
        out += [f"- 表頭：{mark(','.join(old_fields), 'del')} → {mark(','.join(new_fields), 'ins')}"]
        out += [f"- `{f}`：{COLUMN_REMOVED}" for f in removed]
        out += [f"- `{f}`：{COLUMN_ADDED}" for f in added]
        out.append("")
    ins = dele = 0
    same = []
    for code in sorted(set(old_rows) | set(new_rows)):
        old, new = old_rows.get(code), new_rows.get(code)
        if old is not None and new is not None and all(old.get(f, "") == new.get(f, "") for f in fields):
            same.append(code)
            continue
        out.append(f"#### {code}")
        if old is None:
            out.append(CODE_ADDED)
        elif new is None:
            out.append(CODE_REMOVED)
        elif old.get("status") != "retired" and new.get("status") == "retired":
            out.append(CODE_RETIRED)
        out.append("")
        for f in fields:
            if f == "code":  # 已經是這一段的標題
                continue
            a = "" if old is None else old.get(f, "")
            b = "" if new is None else new.get(f, "")
            if old is None:
                if b:
                    out.append(f"- `{f}`：{mark(show(b), 'ins')}")
                    ins += 1
            elif new is None:
                if a:
                    out.append(f"- `{f}`：{mark(show(a), 'del')}")
                    dele += 1
            elif f in removed:
                if a:
                    out.append(f"- `{f}`：{mark(show(a), 'del')} {COLUMN_REMOVED}")
                    dele += 1
            elif f in added:
                if b:
                    out.append(f"- `{f}`：{mark(show(b), 'ins')} {COLUMN_ADDED}")
                    ins += 1
            elif a == b:
                if b:
                    out.append(f"- `{f}`：{show(b)}")
            else:
                out.append(f"- `{f}`：{mark(show(a), 'del')} → {mark(show(b), 'ins')}")
                ins += 1
                dele += 1
        out.append("")
    if len(same) == len(set(old_rows) | set(new_rows)):
        out += ["CSV 沒有改動。", ""]
    out.append(f"沒改動的代碼 {len(same)} 個" + (f"：{'、'.join(same)}" if same else "") + "。")
    return out, ins, dele


def in_head(path: pathlib.Path) -> bool:
    """這個檔在 git 的 HEAD 裡嗎（不在 git 裡、或 git 失敗都算不在）。"""
    try:
        return subprocess.run(["git", "cat-file", "-e", f"HEAD:{path.as_posix()}"],
                              capture_output=True).returncode == 0
    except OSError:
        return False


def diff_all(old: list[str], old_csv: str | None, path: pathlib.Path, csv_path: pathlib.Path | None,
             name: str) -> tuple[list[str], int, int]:
    """.md 逐行差異，有附屬 CSV 時接上逐碼差異。比的是原檔寫法，連結在輸出時才改寫。"""
    out, ins, dele = diff_md(old, path.read_text().splitlines())
    if csv_path is not None:
        csv_out, c_ins, c_del = diff_csv(old_csv, csv_path.read_text(encoding="utf-8"), name)
        out += [""] + csv_out
        ins += c_ins
        dele += c_del
    return out, ins, dele


def write_outputs(name: str, out: list[str], basis: str, notes: list[str]) -> None:
    """寫進 doc/review/<鍵>/：<鍵>.md、<鍵>.marked.md，有附屬 CSV 時加 <鍵>.csv。檔名固定，每次覆蓋。

    版本號不寫進檔名也不寫進檔內：送審的版號由 pack_review.py 取號，只出現在 zip 內的檔名。
    兩份 .md 都放在 doc/review/<鍵>/，相對連結改寫成從那裡出發才不會指錯；正式檔不動。
    """
    path, key = target(name)
    csv_path = companion_csv(name)
    d = out_dir(key)
    d.mkdir(parents=True, exist_ok=True)
    official = f"/{path.as_posix()}" + ("" if csv_path is None else f" 與 /{csv_path.as_posix()}")
    header = [
        f"<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定案時刪除該鍵的送審資料夾；"
        f"{basis}。正式內容看 {official} -->",
        "",
    ]
    for note in notes:
        print(f"{name}: {note}")
        header += [f"> 注意：{note}", ""]
    (d / f"{key}.md").write_text(rewrite_links(path.read_text(), path, d))
    copy_csv = d / f"{key}.csv"
    if csv_path is not None:
        # CSV 逐位元組照抄（BOM、LF 都保留）；CSV 裡不准 Markdown，所以沒有連結要改寫
        copy_csv.write_bytes(csv_path.read_bytes())
    elif copy_csv.exists():
        copy_csv.unlink()
    (d / f"{key}.marked.md").write_text(rewrite_links("\n".join(header + out) + "\n", path, d))


def build(name: str, suffix: str) -> tuple[int, int]:
    """以本機 _backup/ 的改前快照（<後綴>）當基準；後綴 new 表示新建的檔，整份標新增。"""
    name = normalize(name)
    path, key = target(name)
    csv_path = companion_csv(name)
    new = path.read_text().splitlines()
    notes: list[str] = []
    old_csv: str | None = None
    if suffix != "new" and not BACKUP.is_dir():
        raise SystemExit(
            f"後綴模式要讀本機的 {BACKUP}/，但它不存在（它不進 git，換電腦或新 clone 就沒有）。\n"
            "改用送審紀錄當基準：不帶後綴（最後一次回覆過的版本），或 --base-version <鍵>=<N>。"
        )
    if suffix == "new":
        old = []
    elif csv_path is None:
        old = follow_renames(backup_path(name, suffix).read_text(), path).splitlines()
    else:
        md_backup, md_tried = find_backup(name, suffix, ".md")
        csv_backup, csv_tried = find_backup(name, suffix, ".csv")
        if md_backup is None and csv_backup is None:
            raise SystemExit(
                f"找不到 {name} 的基準版（.md 與 .csv 都沒有）。試過：\n  "
                + "\n  ".join(map(str, md_tried + csv_tried))
                + "\n改檔之前要先備份，命名見 script/doc/README.md。"
            )
        if md_backup is None:
            old = new
            notes.append(f"沒有 {path.as_posix()} 的基準版 {suffix}：視為這一輪沒改")
        else:
            old = follow_renames(md_backup.read_text(), path).splitlines()
        if csv_backup is not None:
            old_csv = csv_backup.read_text(encoding="utf-8")
        elif in_head(csv_path):
            old_csv = csv_path.read_text(encoding="utf-8")
            notes.append(f"沒有 {csv_path.as_posix()} 的基準版 {suffix}：視為這一輪沒改")
        else:
            notes.append(f"沒有 {csv_path.as_posix()} 的基準版 {suffix}，而且它不在 git 的 HEAD 裡：視為新建，整份標新增")
    out, ins, dele = diff_all(old, old_csv, path, csv_path, name)
    write_outputs(name, out, f"基準 {suffix}", notes)
    return ins, dele


def resolve_base_name(name: str) -> str:
    """參數裡的名字 → mark_changes 的名字。

    審閱頁照舊傳頁名；其他檔可傳路徑，也可以直接傳鍵：repo 根目錄有 <名>.md 時（例如 GLOSSARY、README），
    當成那個根目錄檔。根目錄檔優先：鍵 README 是根目錄的 README.md，doc/contract/README.md 的鍵是
    doc_contract_README（傳路徑），兩者不能共用一個鍵。
    """
    name = normalize(name)
    if "/" not in name and not name.endswith(".md") and pathlib.Path(f"{name}.md").exists():
        return f"{name}.md"
    return name


def base_entry(name: str, base: int | None) -> tuple[dict | None, str | None]:
    """回傳（送審紀錄或 None, 錯誤訊息或 None）。

    base 是 None 時，已定案的鍵取 finalized，其餘取最後一筆 replied: true 的紀錄；
    兩者都沒有時回（None, None），整份標新增。
    指定的版號不在 versions.json、或那個 commit 裡沒有基準檔，回錯誤訊息。
    """
    name = resolve_base_name(name)
    path, key = target(name)
    if base is None:
        final = finalized(key)
        if final is not None:
            entry = sent_version(key, final["v"])
            if entry is None:
                return None, f"{name}：{VERSIONS} 沒有鍵 {key} 的定案版本 v{final['v']} 的送審紀錄"
        else:
            entry = last_replied(key)
        if entry is None:
            return None, None
    else:
        entry = sent_version(key, base)
        if entry is None:
            return None, f"{name}：{VERSIONS} 沒有鍵 {key} 的送審版本 v{base}"
    src, text = base_text(entry, "path", path)
    if text is None:
        return None, f"{name}：commit {entry['commit']} 裡沒有 {src.as_posix()}（v{entry['v']} 的基準）"
    if entry.get("csv_path") and git_show(entry["commit"], pathlib.Path(entry["csv_path"])) is None:
        return None, f"{name}：commit {entry['commit']} 裡沒有 {entry['csv_path']}（v{entry['v']} 的 CSV 基準）"
    return entry, None


def finalized_content_is_current(name: str, entry: dict) -> bool:
    """正式檔與定案送審版的內容是否相同；審閱頁旁的 CSV 也一起比。"""
    path, _ = target(name)
    _, old = base_text(entry, "path", path)
    if old is None or old != path.read_text():
        return False
    if path.parent != REVIEW:
        return True
    csv_path = path.with_suffix(".csv")
    _, old_csv = base_text(entry, "csv_path", csv_path)
    current_csv = csv_path.read_text(encoding="utf-8") if csv_path.exists() else None
    return old_csv == current_csv


def clear_finalized_output(name: str) -> None:
    """刪除已定案鍵殘留的送審資料夾，並輸出處理結果。"""
    _, key = target(name)
    d = out_dir(key)
    if d.exists():
        shutil.rmtree(d)
        print(f"{name}: 已定案且正式檔未改，已刪除 {d}，不產生送審檔")
    else:
        print(f"{name}: 已定案且正式檔未改，不產生送審檔")


def build_from_version(name: str, base: int | None = None) -> tuple[int, int, str | None]:
    """以送審紀錄當基準：versions.json 裡該鍵版本 base 的 commit，用 git show 取正式檔（與 CSV）。

    base 是 None 時，已定案的鍵先比對定案 commit：內容未改就清掉舊送審資料夾且不產檔，
    定案後又改過就以定案版為基準重新產生。未定案的鍵取最後一筆 replied: true 的紀錄；
    沒有就整份標新增。
    維護者看過並回覆的那一版不再標紅綠，只標之後的改動。找不到指定版號就停下報錯。
    """
    name = resolve_base_name(name)
    path, key = target(name)
    csv_path = companion_csv(name)
    final = finalized(key) if base is None else None
    entry, error = base_entry(name, base)
    if error:
        raise SystemExit(error)
    if final is not None and finalized_content_is_current(name, entry):
        clear_finalized_output(name)
        return 0, 0, None
    notes: list[str] = []
    if entry is None:
        old, old_csv = [], None
        basis = "基準：沒有維護者回覆過的版本，整份標新增"
        notes.append(f"{key} 沒有維護者回覆過的版本：整份標新增")
    else:
        commit = entry["commit"]
        src, text = base_text(entry, "path", path)
        old = text.splitlines()
        old_csv = None
        if csv_path is not None:
            csv_src, old_csv = base_text(entry, "csv_path", csv_path)
            if old_csv is None:
                notes.append(f"送審時的 commit {commit[:7]} 裡沒有 {csv_src.as_posix()}：視為新建，整份標新增")
        if final is not None:
            notes.append("定案後又有改動，回到待審")
            basis = f"基準是定案 commit {commit[:7]}"
        else:
            state = "維護者回覆過" if entry.get("replied") is True else "維護者還沒回覆"
            # 版本號不寫進檔內；副本路徑通常帶版號，所以只寫 commit
            basis = f"基準是{state}的送審 commit {commit[:7]}"
    out, ins, dele = diff_all(old, old_csv, path, csv_path, name)
    write_outputs(name, out, basis, notes)
    if base is not None:
        where = f"送審 v{base}"
    elif final is not None:
        where = f"定案版 v{final['v']}"
    else:
        where = "最後一次回覆過的版本"
    return ins, dele, where


def is_name(arg: str) -> bool:
    """這個參數對得到要標示的檔嗎（對不到就當成舊版後綴）。"""
    return target(resolve_base_name(arg))[0].exists()


def run_from_versions(parsed: list[tuple[str, int | None]]) -> None:
    """先全部檢查過再產：缺一個就整批不做。"""
    errors = [err for name, base in parsed for err in [base_entry(name, base)[1]] if err]
    if errors:
        sys.exit("找不到指定的送審版本，沒有產生任何標示版：\n  " + "\n  ".join(errors))
    for name, base in parsed:
        ins, dele, where = build_from_version(name, base)
        if where is None:
            continue
        print(f"{name}: {ins} ins, {dele} del（基準 {where}）")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--base-version":
        pairs = args[1:]
        if not pairs:
            sys.exit(__doc__)
        parsed: list[tuple[str, int | None]] = []
        for pair in pairs:
            name, sep, num = pair.rpartition("=")
            if not sep or not name or not num.isdigit():
                sys.exit(f"--base-version 的參數要寫成 <頁>=<版號>，例如 03_output=13：{pair}")
            parsed.append((name, int(num)))
        run_from_versions(parsed)
        return
    if args[0] == "new" or (len(args) >= 2 and not is_name(args[0])):
        suffix, names = args[0], args[1:]
        for name in names:
            ins, dele = build(name, suffix)
            print(f"{name}: {ins} ins, {dele} del")
        return
    run_from_versions([(name, None) for name in args])


if __name__ == "__main__":
    main()
