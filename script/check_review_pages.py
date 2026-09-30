#!/usr/bin/env python3
r"""檢查對外文件（根目錄 README.md 與 doc/contract/0N_*.md）的寫法規則。

規則見 doc/contract/README.md「寫法規則」與「版本怎麼迭代」：
1. 不寫「出處：」行：沿用規則時在正文寫「依 [頁名第 N 條](連結#錨點)」。
2. 不寫「> 版本 vN」：版本只在 doc/decisions/_marked/ 的檔名。
3. 每頁有「## 目錄」。
3a. HTML 只准 <ins>：<a id>、<br> 這類只有部分環境顯示得出來；錨點一律用標題產生。
    反斜線跳脫的 \<repo\> 是字面文字，不算標籤。
4. 相對連結的檔案與錨點都存在（錨點照 GitHub 的標題轉換規則算）。
5. 只能向前依賴：審閱頁 N 不能連到編號比它大的審閱頁。
6. 03 的指令寫法只能用前面頁定義過的：03 頁反引號裡的 `just vendor_kit …`，以及 03 的 CSV
   （situation、message、next_step 欄）裡的 just vendor_kit …，每個選項（-x、--xxx）與 @<tag> 寫法
   都要在 GLOSSARY.md、01、02 出現過。CSV 的錯誤位置報 `<檔>:<代碼>:<欄名>`。
7. 引用別頁條目不寫舊寫法「[名字](連結) 第 N 條」：一律寫「依 [頁名第 N 條](連結#錨點)」；
   行內程式碼（反引號內）不算。
8. 連結文字不得含反引號：碼放在連結外，寫「[結束碼](03_messages.md#結束碼) `2`」、
   「[訊息](03_messages.csv) `VK0028`」；行內程式碼裡的連結例子不算。
   程式碼名詞本身當連結時直接寫名詞，例如「[dist/](…)」。
9. 連結文字裡的 <…> 要跳脫：寫「[\<repo\>](../../GLOSSARY.md#工具與出貨)」；沒跳脫的 <repo> 會被當成
   HTML 標籤吃掉。<ins> 不算。

用法：python3 script/check_review_pages.py（在 repo 根目錄跑；有問題以 1 結束）
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
REVIEW = ROOT / "doc/contract"
PAGE = re.compile(r"^(\d\d)_.+\.md$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
OLD_CITE = re.compile(r"\]\([^)]+\)\s*第\s*\d+\s*條")
# 連結文字取最內層的 [ ]，避免從行內程式碼裡落單的 [ 一路吃到後面的連結
LINK_TEXT = re.compile(r"\[([^\[\]]*)\]\([^)\s]+\)")
# HTML 標籤；前面有反斜線的 \<repo\> 是跳脫過的字面文字，不算
TAG = re.compile(r"(?<!\\)</?([a-zA-Z][\w-]*)[^>]*>")
# 連結文字裡沒跳脫的 <…>（<ins> 另外放行）
RAW_ANGLE = re.compile(r"(?<!\\)<(/?)([^<>]*)>")


def code_spans(line: str) -> list[tuple[int, int]]:
    """行內程式碼的範圍：一串 n 個反引號配下一串同樣 n 個反引號（CommonMark 的配對規則）。"""
    runs = [(m.start(), m.end()) for m in re.finditer(r"`+", line)]
    spans = []
    k = 0
    while k < len(runs):
        s, e = runs[k]
        for j in range(k + 1, len(runs)):
            if runs[j][1] - runs[j][0] == e - s:
                spans.append((s, runs[j][1]))
                k = j
                break
        k += 1
    return spans


def link_texts(line: str):
    """連結（整段原文, 連結文字）；[ 或 ]( 落在行內程式碼裡的是例子，不是連結，不算。"""
    spans = code_spans(line)
    inside = lambda pos: any(s <= pos < e for s, e in spans)  # noqa: E731
    for m in LINK_TEXT.finditer(line):
        close = m.start() + 1 + len(m.group(1))
        if inside(m.start()) or inside(close):
            continue
        yield m.group(0), m.group(1)


def backtick_link_texts(line: str) -> list[str]:
    """連結文字含反引號的連結（整段原文）。"""
    return [link for link, text in link_texts(line) if "`" in text]


def raw_angle_link_texts(line: str) -> list[tuple[str, str]]:
    """連結文字裡有沒跳脫的 <…> 的連結：（整段原文, 第一個 <…>）；<ins>、</ins> 不算。"""
    out = []
    for link, text in link_texts(line):
        for m in RAW_ANGLE.finditer(text):
            if m.group(2) != "ins":
                out.append((link, m.group(0)))
                break
    return out


def pages() -> list[pathlib.Path]:
    return [ROOT / "README.md"] + sorted(p for p in REVIEW.glob("*.md") if PAGE.match(p.name))


def slug(text: str) -> str:
    """GitHub 的標題錨點：小寫、去掉標點（保留文字、數字、_、-、空白），空白換成 -。"""
    text = re.sub(r"(?<!\\)<[^>]+>", "", text)   # <ins> 之類的標籤；跳脫的 \<repo\> 留著，反斜線下面當標點去掉
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 連結只留文字
    text = text.replace("`", "").lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: pathlib.Path) -> set[str]:
    seen: dict[str, int] = {}
    out = set()
    fenced = False
    for line in path.read_text().splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        m = None if fenced else HEADING.match(line)
        if not m:
            continue
        s = slug(m.group(2))
        n = seen.get(s, 0)
        out.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    return out


def body_lines(path: pathlib.Path):
    fenced = False
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line


def page_no(path: pathlib.Path) -> int | None:
    m = PAGE.match(path.name)
    return int(m.group(1)) if m and path.parent.resolve() == REVIEW.resolve() else None


def check_page(path: pathlib.Path, errors: list[str]) -> None:
    text = path.read_text()
    if "## 目錄" not in text:
        errors.append(f"{path}: 沒有「## 目錄」")
    me = page_no(path)
    for i, line in body_lines(path):
        where = f"{path}:{i}"
        if re.match(r"^\s*(?:[-*]\s*)?出處[:：]", line):
            errors.append(f"{where}: 對外頁不寫「出處」行；沿用規則時在正文寫「依 [頁名第 N 條](連結#錨點)」")
        tags = sorted({t for t in TAG.findall(re.sub(r"`[^`]*`", "", line)) if t != "ins"})
        if tags:
            errors.append(f"{where}: 用了 HTML {tags}：對外頁只准 <ins>（GitHub 與 GitLab 都顯示）；錨點用標題產生")
        if OLD_CITE.search(re.sub(r"`[^`]*`", "", line)):
            errors.append(f"{where}: 引用條目的舊寫法「[名字](連結) 第 N 條」；改成「依 [頁名第 N 條](連結#錨點)」")
        for link in backtick_link_texts(line):
            errors.append(f"{where}: 連結文字不得含反引號：{link}；碼放在連結外，寫「[結束碼](03_messages.md#結束碼) `2`」「[訊息](03_messages.csv) `VK0028`」；程式碼名詞本身當連結時直接寫名詞，例如「[dist/](…)」")
        for link, raw in raw_angle_link_texts(line):
            fixed = "\\<" + raw[1:-1] + "\\>"
            errors.append(f"{where}: 連結文字裡的 {raw} 沒跳脫：{link}；改成 {fixed}，例如「[\\<repo\\>](../../GLOSSARY.md#工具與出貨)」")
        if re.match(r"^>\s*版本\s*v\d+\s*$", line):
            errors.append(f"{where}: 正式檔不寫版本號；版本只在 _marked/ 的檔名")
        for target in LINK.findall(line):
            if re.match(r"^[a-z]+:", target):
                continue
            file_part, _, frag = target.partition("#")
            dest = path if not file_part else (path.parent / file_part)
            if file_part.startswith("/"):
                errors.append(f"{where}: 連結 {target} 以 / 開頭，改成相對路徑")
                continue
            if not dest.exists():
                errors.append(f"{where}: 連結目標不存在：{target}")
                continue
            if frag and dest.suffix == ".md" and frag not in anchors(dest):
                errors.append(f"{where}: 錨點不存在：{target}")
            other = page_no(dest) if dest.suffix == ".md" else None
            if me is not None and other is not None and other > me:
                errors.append(f"{where}: 審閱頁 {me:02d} 連到後面的頁 {dest.name}；只能向前依賴")


CMD_MD = re.compile(r"`(just vendor_kit [^`]+)`")
# CSV 不准 Markdown，指令沒有反引號：從 just vendor_kit 起取到第一個非 ASCII 字（中文、全形標點）或欄尾
CMD_CSV = re.compile(r"just vendor_kit [ -~]*")
CSV_COMMAND_FIELDS = ("situation", "message", "next_step")


def command_errors(cmds, where: str, defined: str) -> list[str]:
    """共用：每個指令裡的選項（-x、--xxx）與 @<tag> 寫法都要在 defined（GLOSSARY.md、01、02）出現過。"""
    errors = []
    for cmd in cmds:
        cmd = cmd.strip()
        for tok in re.findall(r"(?<![\w<])(--?[a-z][\w-]*|@<[^>]+>)", cmd):
            if tok not in defined:
                errors.append(f"{where}: 指令 `{cmd}` 用了 {tok}，但 GLOSSARY.md、01、02 都沒出現過；先補進前面的頁")
    return errors


def csv_command_texts(path: pathlib.Path):
    """03 的 CSV 裡會印出指令的欄：（位置 `<檔>:<代碼>:<欄名>`, 欄位文字）。讀不了的格式交給 check_messages.py。"""
    try:
        rows = list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines(keepends=True)))
    except (csv.Error, UnicodeDecodeError):
        return
    for row in rows:
        for field in CSV_COMMAND_FIELDS:
            value = row.get(field) or ""
            if value:
                yield f"{path}:{row.get('code', '?')}:{field}", value


def check_commands(errors: list[str]) -> None:
    defined = "\n".join(
        p.read_text() for p in [ROOT / "GLOSSARY.md", *sorted(REVIEW.glob("0[12]_*.md"))] if p.exists()
    )
    msgs = sorted(REVIEW.glob("03_*.md"))
    if msgs:
        for i, line in body_lines(msgs[0]):
            errors.extend(command_errors(CMD_MD.findall(line), f"{msgs[0]}:{i}", defined))
    for path in sorted(REVIEW.glob("03_*.csv")):
        for where, value in csv_command_texts(path):
            errors.extend(command_errors(CMD_CSV.findall(value), where, defined))


def main() -> int:
    errors: list[str] = []
    ps = pages()
    for p in ps:
        check_page(p, errors)
    check_commands(errors)
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL: {len(errors)} 個問題")
        return 1
    print(f"OK: 掃 {len(ps)} 個對外文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
