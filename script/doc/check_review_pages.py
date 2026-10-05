#!/usr/bin/env python3
r"""檢查對外文件（doc/contract/0N_*.md）的寫法規則。

規則見 doc/contract/README.md「寫法規則」與「版本怎麼迭代」：
1. 不寫「出處：」行：沿用規則時在正文寫「依 [頁名第 N 條](連結#錨點)」。
2. 不寫「> 版本 vN」：版本只記在 doc/review/versions.json，只出現在送審 zip 內的檔名。
3. 每頁有「## 目錄」。
3a. 不准任何 HTML 標籤（<ins> 也不行；名詞改連到 GLOSSARY.md 分群）：<a id>、<br> 這類只有部分環境顯示得出來；錨點一律用標題產生。
    反斜線跳脫的 \<repo\> 是字面文字，不算標籤。
4. 相對連結的檔案與錨點都存在（錨點照 GitHub 的標題轉換規則算）。
5. 內容只能往前依賴；導覽指標可以往後指。入口頁不是第 0 頁。
   L1、L2：01、02 不寫原因代碼與結束碼數字；L3：入口頁不以「依」連結審閱頁。
6. L4：入口頁與 03 的行內程式碼、訊息表 reason_codes.csv 的指令欄，掃 VK recipe 開頭的片段，
   選項 token（含單獨的 --）與 @<tag> 必須在 GLOSSARY.md、01、02 行內程式碼定義過。
7. 引用別頁條目不寫舊寫法「[名字](連結) 第 N 條」：一律寫「依 [頁名第 N 條](連結#錨點)」；
   行內程式碼（反引號內）不算。
8. 連結文字不得含反引號：碼放在連結外，寫「[結束碼](03_output.md#結束碼) `2`」、
   「[訊息](reason_codes.csv) `VK0028`」；行內程式碼裡的連結例子不算。
   程式碼名詞本身當連結時直接寫名詞，例如「[dist/](…)」。
9. 連結文字裡的 <…> 要跳脫：寫「[\<repo\>](../../GLOSSARY.md#工具與出貨)」；沒跳脫的 <repo> 會被當成
   HTML 標籤吃掉。<ins> 也一樣要跳脫。

用法：python3 script/doc/check_review_pages.py（在 repo 根目錄跑；有問題以 1 結束）
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
REVIEW = ROOT / "doc/contract"
# 03 的訊息表（#137：從 03_output.csv 改名為 reason_codes.csv）
MESSAGES_CSV = REVIEW / "reason_codes.csv"
PAGE = re.compile(r"^(\d\d)_.+\.md$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
OLD_CITE = re.compile(r"\]\([^)]+\)\s*第\s*\d+\s*條")
# 連結文字取最內層的 [ ]，避免從行內程式碼裡落單的 [ 一路吃到後面的連結
LINK_TEXT = re.compile(r"\[([^\[\]]*)\]\([^)\s]+\)")
# HTML 標籤；前面有反斜線的 \<repo\> 是跳脫過的字面文字，不算
TAG = re.compile(r"(?<!\\)</?([a-zA-Z][\w-]*)[^>]*>")
# 連結文字裡沒跳脫的 <…>
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
    """連結文字裡有沒跳脫的 <…> 的連結：（整段原文, 第一個 <…>）。"""
    out = []
    for link, text in link_texts(line):
        m = RAW_ANGLE.search(text)
        if m:
            out.append((link, m.group(0)))
    return out


def pages() -> list[pathlib.Path]:
    """要掃的對外文件；檔案或 doc/contract/ 還不存在時就少掃那些，不當錯誤。"""
    found = [ROOT / "README.md"] + sorted(p for p in REVIEW.glob("*.md") if PAGE.match(p.name))
    return [p for p in found if p.is_file()]


def slug(text: str) -> str:
    """GitHub 的標題錨點：小寫、去掉標點（保留文字、數字、_、-、空白），空白換成 -。"""
    text = re.sub(r"(?<!\\)<[^>]+>", "", text)   # HTML 標籤；跳脫的 \<repo\> 留著，反斜線下面當標點去掉
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
        if me in (1, 2):
            reason = re.search(r"VK\d{4}", line)
            if reason:
                errors.append(f"{where}: L1：01、02 不准原因代碼 {reason.group(0)}")
            # 連結只留顯示文字，避免名詞連結的路徑把十字距離拉長。
            visible = LINK_TEXT.sub(lambda m: m.group(1), line)
            if re.search(r"exit code \d", visible):
                errors.append(f"{where}: L2：01、02 不准 exit code 數字")
            numbers = list(re.finditer(r"`[0-9]`", visible))
            for term in re.finditer("結束碼", visible):
                if any(max(0, number.start() - term.end(), term.start() - number.end()) <= 10
                       for number in numbers):
                    errors.append(f"{where}: L2：結束碼前後 10 字內不准碼值")
                    break
        if re.match(r"^\s*(?:[-*]\s*)?出處[:：]", line):
            errors.append(f"{where}: 對外頁不寫「出處」行；沿用規則時在正文寫「依 [頁名第 N 條](連結#錨點)」")
        tags = sorted({t for t in TAG.findall(re.sub(r"`[^`]*`", "", line))})
        if tags:
            errors.append(f"{where}: 用了 HTML {tags}：對外頁不准任何 HTML 標籤（<ins> 也不行；名詞改連到 GLOSSARY.md 分群）；錨點用標題產生")
        if OLD_CITE.search(re.sub(r"`[^`]*`", "", line)):
            errors.append(f"{where}: 引用條目的舊寫法「[名字](連結) 第 N 條」；改成「依 [頁名第 N 條](連結#錨點)」")
        for link in backtick_link_texts(line):
            errors.append(f"{where}: 連結文字不得含反引號：{link}；碼放在連結外，寫「[結束碼](03_output.md#結束碼) `2`」「[訊息](reason_codes.csv) `VK0028`」；程式碼名詞本身當連結時直接寫名詞，例如「[dist/](…)」")
        for link, raw in raw_angle_link_texts(line):
            fixed = "\\<" + raw[1:-1] + "\\>"
            errors.append(f"{where}: 連結文字裡的 {raw} 沒跳脫：{link}；改成 {fixed}，例如「[\\<repo\\>](../../GLOSSARY.md#工具與出貨)」")
        if re.match(r"^>\s*版本\s*v\d+\s*$", line):
            errors.append(f"{where}: 正式檔不寫版本號；版本只記在 doc/review/versions.json 與送審 zip 的檔名")
        spans = code_spans(line)
        for match in LINK.finditer(line):
            if any(start <= match.start() < end for start, end in spans):
                continue
            target = match.group(1)
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
            evidence = re.search(r"依(?:照)?\s*$", line[:match.start()]) is not None
            if path.resolve() == (ROOT / "README.md").resolve() and other is not None and evidence:
                errors.append(f"{where}: L3：README 不能以論據依賴審閱頁：{match.group(0)}")
            if me is not None and other is not None and other > me and evidence:
                errors.append(f"{where}: 審閱頁 {me:02d} 以「依」連到後面的頁 {dest.name}：內容只能往前依賴；只是導覽就改寫成「詳見」")


# recipe 名依 GLOSSARY.md「VK recipe 與用途」；完整呼叫也接受介面佔位符。
RECIPES = ("add", "remove", "update", "upgrade", "dev", "undev", "sync", "prune", "install", "uninstall", "test")
RECIPE = "(?:" + "|".join(RECIPES) + ")"
CMD_MD = re.compile(r"`((?:just vendor_kit\s+)?" + RECIPE + r"\b[^`]*)`")
CMD_CSV = re.compile(
    r"(?<![\w-])(?:just vendor_kit\s+(?:" + RECIPE + r"|<command>)|" + RECIPE + r")\b"
    r"[ -~]*?(?=\s+and\s+retry\.(?:\s|$)|[;,(]|\.(?:\s|$)|[^ -~]|$)"
)
# 訊息表給人看的欄照語言分組（situation.<lang>、message.<lang>），依首行欄名找，不寫死語言。
CSV_COMMAND_PREFIXES = ("situation.", "message.")
OPTION = re.compile(r"(?<![\w<-])(?:--?[a-zA-Z][\w-]*|--(?![\w-])|@<[^>]+>)(?![\w-])")


def inline_texts(line: str):
    for start, end in code_spans(line):
        yield line[start:end].strip("`").strip()


def option_tokens(text: str) -> set[str]:
    return set(OPTION.findall(text))


def command_errors(cmds, where: str, defined) -> list[str]:
    """選項逐 token 比對；不讓 -i 被 --image 或一般文字誤當定義。"""
    tokens = option_tokens(defined) if isinstance(defined, str) else defined
    errors = []
    for cmd in cmds:
        cmd = cmd.strip()
        for tok in sorted(option_tokens(cmd)):
            if tok not in tokens:
                errors.append(f"{where}: 指令 `{cmd}` 用了 {tok}，但 GLOSSARY.md、01、02 都沒出現過；先補進前面的頁")
    return errors


def csv_command_texts(path: pathlib.Path):
    """03 的 CSV 裡會印出指令的欄：（位置 `<檔>:<代碼>:<欄名>`, 欄位文字）。讀不了的格式交給 check_messages.py。"""
    try:
        reader = csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines(keepends=True))
        rows = list(reader)
    except (csv.Error, UnicodeDecodeError):
        return
    fields = [f for f in reader.fieldnames or () if f.startswith(CSV_COMMAND_PREFIXES)]
    for row in rows:
        for field in fields:
            value = row.get(field) or ""
            if value:
                yield f"{path}:{row.get('code', '?')}:{field}", value


def check_commands(errors: list[str]) -> None:
    # 選項要先在名詞表定義；沒有根 GLOSSARY.md 時整段跳過。
    if not (ROOT / "GLOSSARY.md").is_file():
        return
    defined = set()
    for path in [ROOT / "GLOSSARY.md", *sorted(REVIEW.glob("0[12]_*.md"))]:
        if path.exists():
            for _, line in body_lines(path):
                for code in inline_texts(line):
                    defined.update(option_tokens(code))
    for path in pages():
        if path != ROOT / "README.md" and page_no(path) != 3:
            continue
        if not path.exists():
            continue
        for i, line in body_lines(path):
            cmds = [code for code in inline_texts(line)
                    if re.match(r"^(?:just vendor_kit\s+)?" + RECIPE + r"\b", code)]
            # 單獨的 -- 也可能在說明文字的行內程式碼出現。
            cmds.extend(code for code in inline_texts(line) if code == "--")
            errors.extend(command_errors(cmds, f"{path}:{i}", defined))
    # 03 的訊息表明列檔名（#137），不靠 03_ 前綴推；還不存在就少掃
    for path in [MESSAGES_CSV] if MESSAGES_CSV.exists() else []:
        for where, value in csv_command_texts(path):
            cmds = CMD_CSV.findall(value)
            if "--" in option_tokens(value) and not any("--" in option_tokens(cmd) for cmd in cmds):
                cmds.append("--")
            errors.extend(command_errors(cmds, where, defined))


# 僅豁免已盤點的原文與位置；新增或改動的違規不會自動列入。
TEMP_ALLOWLIST: dict[str, str] = {}


def main() -> int:
    errors: list[str] = []
    ps = pages()
    for p in ps:
        check_page(p, errors)
    check_commands(errors)
    waived = [error for error in errors if error in TEMP_ALLOWLIST]
    errors = [error for error in errors if error not in TEMP_ALLOWLIST]
    print(f"暫時白名單：{len(TEMP_ALLOWLIST)} 筆；本次命中 {len(waived)} 筆")
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL: {len(errors)} 個問題")
        return 1
    print(f"OK: 掃 {len(ps)} 個對外文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
