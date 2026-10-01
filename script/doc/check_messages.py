#!/usr/bin/env python3
"""檢查訊息表 doc/contract/03_output.csv（每個原因代碼的唯一出處，#122）。

格式：UTF-8 加 BOM（恰好一個）、只准 LF、檔尾一個換行、逗號分隔、照 RFC 4180 跳脫；
表頭逐字等於 FIELDS。規則：

1. 格式：每列欄數相同、用 csv 模組以 strict 解析；欄位頭尾不准空白；
   不准以 =、+、-、@、Tab、CR 開頭（Excel 公式注入）。
2. 代碼：VK 加四位數字；從 VK0001 起逐列加一（唯一、遞增、不缺列；停用的留列）。
3. status 只准 active、retired；retired 列除 code、status、situation 外都要空白。
4. active 列：level 只准 warn、error、fatal；exit_code 必須分別是 1、2、3；
   situation、message、description 必填，message 不准含中文字元。
5. disposition 只准「待處理」「失敗」或空白；只有 warn 與 situation 以「用法錯誤：」開頭的列可留空；
   待處理必有 next_step；失敗的 next_step 必須空白。
6. next_step 有值時必須逐字出現在 message 裡。
7. 欄位不准 HTML 與 Markdown；不帶屬性的 <…> 算占位符；< 與 > 要成對。
8. 引用：README.md、doc/contract/*.md、GLOSSARY.md 裡的每個 VKnnnn 都要在 CSV 且是 active；
   doc/adr/*.md 只要求存在。連 03_output.csv 不准帶 #；連結文字是代碼時不准連 03_output.md
   （03_output.md 不放逐碼內容，一律連 CSV）。01、02 不准連 CSV。
9. 診斷範例：README.md、doc/contract/*.md、GLOSSARY.md 裡的
   `vendor_kit: <level>[VKnnnn]: <本文>`，level 要等於 CSV；本文要符合 message 第一行，
   message 裡的 <…> 占位符可對應範例中的任意文字。
10. active 列的 message 句首要大寫，或以占位符、小寫指令名 just 開頭；結尾要是句點，
    或以 next_step、just vendor_kit 指令結尾。

指令寫法（CSV 的 situation、message、next_step 裡的 `just vendor_kit …`）由 check_review_pages.py 檢查。
錯誤位置報 `<檔>:<代碼>:<欄名>`，不報實體行號。CSV 還不存在時跳過並印 OK。

用法：python3 script/doc/check_messages.py（在 repo 根目錄跑；有問題以 1 結束）
"""
import csv
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
REVIEW = ROOT / "doc/contract"
CSV_PATH = REVIEW / "03_output.csv"
MD_PATH = REVIEW / "03_output.md"
FIELDS = [
    "code", "status", "level", "exit_code", "disposition", "situation", "message", "description", "next_step",
]
STATUS = {"active", "retired"}
LEVELS = {"warn", "error", "fatal"}
EXIT_CODES = {"warn": "1", "error": "2", "fatal": "3"}
DISPOSITIONS = {"待處理", "失敗", ""}
RETIRED_KEEP = {"code", "status", "situation"}
CODE = re.compile(r"^VK\d{4}$")
CODE_ANY = re.compile(r"(?<![A-Za-z0-9])VK\d{4}(?!\d)")
BOM = "﻿"
# Excel 會把這些開頭的儲存格當公式（OWASP CSV injection）
FORMULA_START = ("=", "+", "-", "@", "\t", "\r")
# 常見 HTML 標籤名（只比小寫；<P> 這類大寫的是占位符）
HTML_NAMES = {
    "a", "b", "i", "u", "s", "p", "br", "hr", "em", "strong", "code", "kbd", "pre", "ins", "del", "mark",
    "sup", "sub", "span", "div", "img", "details", "summary", "table", "tr", "td", "th", "ul", "ol", "li",
}
ANGLE = re.compile(r"<([^<>]*)>")
MARKDOWN = (
    (re.compile(r"`"), "反引號"),
    (re.compile(r"\*\*|__"), "粗體"),
    (re.compile(r"~~"), "刪除線"),
    (re.compile(r"\]\("), "連結"),
    (re.compile(r"(?m)^(#{1,6}\s|[-*+]\s|>\s|\d+\.\s)"), "行首的標題、清單或引言記號"),
)
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
CHINESE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
DIAGNOSTIC = re.compile(r"vendor_kit: (warn|error|fatal)\[(VK\d{4})\]: (.*)$")
PLACEHOLDER = re.compile(r"<[^<>]+>")
COMMAND_END = re.compile(r"just vendor_kit\b[^\n]*\Z")


def rel(path: pathlib.Path) -> str:
    return path.as_posix()


def load(path: pathlib.Path, errors: list[str]) -> list[dict[str, str]] | None:
    """讀 CSV 並檢查檔案層級的格式；回傳每列的 dict（表頭不對或解析失敗回 None）。"""
    raw = path.read_bytes()
    where = rel(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        errors.append(f"{where}: 不是 UTF-8：{e}")
        return None
    if not text.startswith(BOM):
        errors.append(f"{where}: 開頭要有 UTF-8 BOM（Windows 的 Excel 雙擊開才不會亂碼）")
    else:
        text = text[1:]
    if BOM in text:
        errors.append(f"{where}: BOM 只准出現一次，而且在檔頭")
    if "\r" in text:
        errors.append(f"{where}: 只准 LF，不准 CR（Excel 另存會改成 CRLF；Excel 只看不存）")
    if not text.endswith("\n") or text.endswith("\n\n"):
        errors.append(f"{where}: 檔尾要恰好一個換行")
    try:
        records = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as e:
        errors.append(f"{where}: CSV 解析失敗（RFC 4180）：{e}")
        return None
    if not records:
        errors.append(f"{where}: 是空的")
        return None
    if records[0] != FIELDS:
        errors.append(f"{where}: 表頭要逐字等於 {','.join(FIELDS)}，現在是 {','.join(records[0])}")
        return None
    rows = []
    for n, rec in enumerate(records[1:], 2):
        if len(rec) != len(FIELDS):
            errors.append(f"{where}:第 {n} 筆: 有 {len(rec)} 欄，表頭是 {len(FIELDS)} 欄")
            continue
        rows.append(dict(zip(FIELDS, rec)))
    return rows


def placeholders_ok(value: str) -> str | None:
    """< 與 > 要成對、不巢狀；回傳問題描述或 None。"""
    depth = 0
    for ch in value:
        if ch == "<":
            if depth:
                return "< 沒有對應的 >（或巢狀）"
            depth = 1
        elif ch == ">":
            if not depth:
                return "> 沒有對應的 <"
            depth = 0
    return "< 沒有對應的 >" if depth else None


def html_in(value: str) -> list[str]:
    found = []
    if "<!--" in value:
        found.append("<!--")
    for inner in ANGLE.findall(value):
        name = inner.strip().lstrip("/").rstrip("/").split(" ")[0]
        if inner.startswith("/") or inner.endswith("/") or "=" in inner or '"' in inner or name in HTML_NAMES:
            found.append(f"<{inner}>")
    return found


def check_rows(rows: list[dict[str, str]], errors: list[str]) -> dict[str, dict[str, str]]:
    where = rel(CSV_PATH)
    by_code: dict[str, dict[str, str]] = {}
    for n, row in enumerate(rows, 1):
        code = row["code"]
        at = f"{where}:{code or f'第 {n + 1} 筆'}"
        if not CODE.match(code):
            errors.append(f"{at}:code: 格式要是 VK 加四位數字")
        elif code in by_code:
            errors.append(f"{at}:code: 代碼重複")
        elif code != f"VK{n:04d}":
            errors.append(f"{at}:code: 第 {n} 列要是 VK{n:04d}（從 VK0001 起逐列加一；停用的留列、不刪）")
        if CODE.match(code) and code not in by_code:
            by_code[code] = row
        for f in FIELDS:
            v = row[f]
            fa = f"{at}:{f}"
            if v != v.strip():
                errors.append(f"{fa}: 頭尾不准有空白")
            if v.startswith(FORMULA_START) or v.lstrip().startswith(FORMULA_START):
                errors.append(f"{fa}: 不准以 =、+、-、@、Tab、CR 開頭（Excel 會當成公式）")
            tags = html_in(v)
            if tags:
                errors.append(f"{fa}: 不准 HTML {tags}（GitHub 不渲染 CSV 裡的 HTML）；不帶屬性的 <…> 才算占位符")
            for pat, what in MARKDOWN:
                if pat.search(v):
                    errors.append(f"{fa}: 不准 Markdown（{what}）：GitHub 不渲染 CSV 裡的 Markdown")
            bad = placeholders_ok(v)
            if bad:
                errors.append(f"{fa}: {bad}")
        status, level, exit_code, disp = row["status"], row["level"], row["exit_code"], row["disposition"]
        if status not in STATUS:
            errors.append(f"{at}:status: 只准 active、retired")
        if not row["situation"]:
            errors.append(f"{at}:situation: 必填（retired 也保留原意）")
        if status == "retired":
            for f in FIELDS:
                if f not in RETIRED_KEEP and row[f]:
                    errors.append(f"{at}:{f}: retired 列只留 code、status、situation，這欄要清空")
            continue
        if status == "active":
            if level not in LEVELS:
                errors.append(f"{at}:level: active 列只准 warn、error、fatal")
            elif exit_code != EXIT_CODES[level]:
                errors.append(f"{at}:exit_code: {level} 必須是 {EXIT_CODES[level]}")
            if not row["message"]:
                errors.append(f"{at}:message: active 列必填")
            if not row["description"]:
                errors.append(f"{at}:description: active 列必填")
        if CHINESE.search(row["message"]):
            errors.append(f"{at}:message: 不准含中文字元；中文說明放 description")
        if disp not in DISPOSITIONS:
            errors.append(f"{at}:disposition: 只准「待處理」「失敗」或空白")
        if level == "warn" and disp:
            errors.append(f"{at}:disposition: warn 一律空白")
        if status == "active" and not disp and level != "warn" and not row["situation"].startswith("用法錯誤："):
            errors.append(f"{at}:disposition: 只有 warn 與用法錯誤可留空")
        if disp == "待處理" and not row["next_step"]:
            errors.append(f"{at}:next_step: 待處理必有下一步")
        if disp == "失敗" and row["next_step"]:
            errors.append(f"{at}:next_step: 失敗的 next_step 必須空白")
        if row["next_step"] and row["next_step"] not in row["message"]:
            errors.append(f"{at}:next_step: 要逐字出現在 message 裡")
        message = row["message"]
        if message and not (message[0].isupper() or message.startswith("<") or re.match(r"just(?:\s|$)", message)):
            errors.append(f"{at}:message: 句首要大寫，或以占位符、小寫指令名 just 開頭")
        if message and not (
            message.endswith(".")
            or (row["next_step"] and message.endswith(row["next_step"]))
            or COMMAND_END.search(message)
        ):
            errors.append(f"{at}:message: 結尾要是句點，或以 next_step、just vendor_kit 指令結尾")
    return by_code


def ref_files() -> list[tuple[pathlib.Path, bool]]:
    """（檔案, 是否要求 active）。ADR 可以引用 retired，但要寫成歷史。"""
    out = [(ROOT / "README.md", True), (ROOT / "GLOSSARY.md", True)]
    out += [(p, True) for p in sorted(REVIEW.glob("*.md"))]
    out += [(p, False) for p in sorted((ROOT / "doc/adr").glob("*.md"))]
    return [(p, a) for p, a in out if p.exists()]


def same(a: pathlib.Path, b: pathlib.Path) -> bool:
    return a.resolve() == b.resolve()


def check_refs(by_code: dict[str, dict[str, str]], errors: list[str]) -> None:
    for path, need_active in ref_files():
        page = re.match(r"^(\d\d)_", path.name) if same(path.parent, REVIEW) else None
        for i, line in enumerate(path.read_text().splitlines(), 1):
            where = f"{rel(path)}:{i}"
            for code in CODE_ANY.findall(line):
                row = by_code.get(code)
                if row is None:
                    errors.append(f"{where}: {code} 不在 {rel(CSV_PATH)}")
                elif need_active and row["status"] != "active":
                    errors.append(f"{where}: {code} 已停用（retired）；只有 ADR 可以引用停用的代碼")
            for text, target in LINK.findall(line):
                if re.match(r"^[a-z]+:", target):
                    continue
                file_part, sep, _ = target.partition("#")
                if not file_part:
                    continue
                dest = path.parent / file_part
                label = text.strip().strip("`")
                if same(dest, CSV_PATH):
                    if page and int(page.group(1)) <= 2:
                        errors.append(f"{where}: 01、02 不准連 CSV（{target}）")
                    if sep:
                        errors.append(f"{where}: 連 CSV 不帶 #（行號會隨排序與增刪變動）：{target}")
                    continue
                if same(dest, MD_PATH) and CODE.match(label):
                    errors.append(f"{where}: [{text}]({target}) 改連 03_output.csv；03_output.md 不放逐碼內容")


def message_pattern(message: str) -> re.Pattern[str]:
    """把 message 第一行轉成整行比對；<…> 占位符是萬用字元。"""
    parts = []
    end = 0
    for placeholder in PLACEHOLDER.finditer(message):
        parts.append(re.escape(message[end:placeholder.start()]))
        parts.append(".*")
        end = placeholder.end()
    parts.append(re.escape(message[end:]))
    return re.compile("".join(parts) + r"\Z")


def check_diagnostics(by_code: dict[str, dict[str, str]], errors: list[str]) -> None:
    """規則 9：文件裡的診斷範例要與 CSV 的 level、message 第一行一致。"""
    paths = [ROOT / "README.md", ROOT / "GLOSSARY.md", *sorted(REVIEW.glob("*.md"))]
    for path in paths:
        if not path.exists():
            continue
        for i, line in enumerate(path.read_text().splitlines(), 1):
            match = DIAGNOSTIC.search(line)
            if not match:
                continue
            level, code, body = match.groups()
            row = by_code.get(code)
            if row is None or row["status"] != "active":
                continue  # 規則 8 會回報不存在或已停用的代碼
            where = f"{rel(path)}:{i}"
            if level != row["level"]:
                errors.append(f"{where}: {code} 的 level 是 {level}，CSV 是 {row['level']}")
            first_line = row["message"].splitlines()[0]
            if not message_pattern(first_line).fullmatch(body):
                errors.append(f"{where}: {code} 的本文不符合 CSV message 第一行：{first_line}")


def check(errors: list[str]) -> bool:
    """回傳 CSV 是否存在。"""
    if not CSV_PATH.exists():
        return False
    rows = load(CSV_PATH, errors)
    if rows is None:
        return True
    by_code = check_rows(rows, errors)
    check_refs(by_code, errors)
    check_diagnostics(by_code, errors)
    return True


def main() -> int:
    errors: list[str] = []
    present = check(errors)
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL: {len(errors)} 個問題")
        return 1
    print(f"OK: 檢查 {rel(CSV_PATH)}" if present else f"OK: {rel(CSV_PATH)} 還不存在，跳過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
