#!/usr/bin/env python3
"""檢查訊息表 doc/contract/reason_codes.csv（每個原因代碼的唯一出處，#122）。

格式：UTF-8 加 BOM（恰好一個）、只准 LF、檔尾一個換行、逗號分隔、照 RFC 4180 跳脫。
表頭（#343）：以 BASE_FIELDS 開頭，其後是一組組 situation.<lang>,message.<lang>（照語言分組，
加語言就在最右邊接一組）；必須有 REQUIRED_LANGS 的每一組。讀表依表頭欄名，不依欄序。規則：

1. 格式：表頭照上面；未知欄名報錯；每列欄數相同、用 csv 模組以 strict 解析；欄位頭尾不准空白；
   不准以 =、+、-、@、Tab、CR 開頭（Excel 公式注入）。
2. 代碼：VK 加四位數字；從 VK0001 起逐列加一（唯一、遞增、不缺列；停用的留列）。
3. status 只准 active、retired；每列每個語言的 situation 必填；
   retired 列除 code、status、situation.<lang> 外都要空白。
4. active 列：level 只准 warn、error、fatal；exit_code 必須分別是 1、2、3；
   每個語言的 message 必填；message.en、situation.en 不准含中文字元（其他語言欄不限）；
   message.<lang> 的 <…> 占位符集合與換行數要與 message.en 相同。
5. disposition 只准 pending、failed 或空白；warn 一律空白；
   只有 warn 與 situation.en 以 `Usage error:` 開頭的列可留空。
6. pending 列的 message.en 必須以指令結尾（見 ending_command）；failed 列不限。
   message.en 以指令結尾時，其他語言的 message 必須逐字包含同一個指令。
7. 欄位不准 HTML 與 Markdown；不帶屬性的 <…> 算占位符；< 與 > 要成對。
8. 引用：README.md、doc/contract/*.md、GLOSSARY.md 裡的每個 VKnnnn 都要在 CSV 且是 active；
   doc/adr/*.md 只要求存在。連 reason_codes.csv 不准帶 #；連結文字是代碼時不准連 03_output.md
   （03_output.md 不放逐碼內容，一律連 CSV）。01、02 不准連 CSV。
9. 診斷範例：README.md、doc/contract/*.md、GLOSSARY.md 裡的
   `vendor_kit: <level>[VKnnnn]: <本文>`，level 要等於 CSV；本文要符合 message.en 第一行，
   message.en 裡的 <…> 占位符可對應範例中的任意文字。
   比對對象是 message.en。
10. active 列的 message.en 句首要大寫，或以占位符、小寫指令名 just 開頭；結尾要是句點，
    或以指令結尾（ending_command 或 just vendor_kit 指令）。

指令寫法（CSV 的 situation.<lang>、message.<lang> 裡的 `just vendor_kit …`）不在這支的範圍。
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
# 訊息表與說明頁的路徑只寫在這裡（#137：訊息表從 03_output.csv 改名為 reason_codes.csv）
CSV_PATH = REVIEW / "reason_codes.csv"
MD_PATH = REVIEW / "03_output.md"
BASE_FIELDS = ["code", "status", "level", "exit_code", "disposition"]
# 必備的語言組；en 是基準語言（VK 印出的字句目前都用英文），其他語言跟 en 比對
BASE_LANG = "en"
REQUIRED_LANGS = ("en", "zh-TW")
LANG_FIELDS = ("situation", "message")
# 目前的完整表頭（照語言分組）
FIELDS = BASE_FIELDS + [f"{kind}.{lang}" for lang in REQUIRED_LANGS for kind in LANG_FIELDS]
STATUS = {"active", "retired"}
LEVELS = {"warn", "error", "fatal"}
EXIT_CODES = {"warn": "1", "error": "2", "fatal": "3"}
DISPOSITIONS = {"pending", "failed", ""}
USAGE_ERROR = "Usage error:"
LANG_COLUMN = re.compile(r"^(situation|message)\.([a-z]{2,3}(?:-[A-Za-z0-9]+)*)$")
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
# 結尾指令：最後一行最後一個「: 」之後的片段，是單一占位符或以這些指令名開頭
COMMAND_NAMES = ("just", "git", "sh", "cd")
COMMAND_TAIL = re.compile(r"^(?:<[^<>]+>|(?:" + "|".join(COMMAND_NAMES) + r") \S.*)$")


def rel(path: pathlib.Path) -> str:
    return path.as_posix()


def load(path: pathlib.Path, errors: list[str]) -> list[dict[str, str]] | None:
    """讀 CSV 並檢查檔案層級的格式；回傳每列以表頭欄名為鍵的 dict（表頭不對或解析失敗回 None）。"""
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
    header = records[0]
    if parse_header(header, where, errors) is None:
        return None
    rows = []
    for n, rec in enumerate(records[1:], 2):
        if len(rec) != len(header):
            errors.append(f"{where}:第 {n} 筆: 有 {len(rec)} 欄，表頭是 {len(header)} 欄")
            continue
        rows.append(dict(zip(header, rec)))
    return rows


def parse_header(header: list[str], where: str, errors: list[str]) -> list[str] | None:
    """檢查表頭，回傳語言清單（照表頭順序）；不合格回 None。"""
    ok = True
    if header[: len(BASE_FIELDS)] != BASE_FIELDS:
        errors.append(f"{where}: 表頭要以 {','.join(BASE_FIELDS)} 開頭，現在是 {','.join(header)}")
        ok = False
    rest = header[len(BASE_FIELDS):] if ok else [h for h in header if h not in BASE_FIELDS]
    langs: list[str] = []
    seen: set[str] = set()
    for name in rest:
        if name in seen:
            errors.append(f"{where}: 表頭欄名重複：{name}")
            ok = False
        seen.add(name)
        if not LANG_COLUMN.match(name):
            errors.append(f"{where}: 表頭有未知欄名：{name}（只准 {','.join(BASE_FIELDS)} 與 situation.<lang>、message.<lang>）")
            ok = False
    if not ok:
        return None
    if len(rest) % 2:
        errors.append(f"{where}: 語言欄要一組組 situation.<lang>,message.<lang>，現在是 {','.join(rest)}")
        return None
    for i in range(0, len(rest), 2):
        s, msg = LANG_COLUMN.match(rest[i]), LANG_COLUMN.match(rest[i + 1])
        if s.group(1) != "situation" or msg.group(1) != "message" or s.group(2) != msg.group(2):
            errors.append(f"{where}: 語言欄要一組組 situation.<lang>,message.<lang>，{rest[i]},{rest[i + 1]} 不成組")
            return None
        langs.append(s.group(2))
    missing = [lang for lang in REQUIRED_LANGS if lang not in langs]
    if missing:
        errors.append(f"{where}: 表頭缺少語言組：{','.join(missing)}（必須有 {','.join(REQUIRED_LANGS)}）")
        return None
    return langs


def ending_command(message: str) -> str | None:
    """message 結尾的指令：最後一行最後一個「: 」之後的片段，
    是單一占位符（例如 <original_command>）或以 just、git、sh、cd 加空白開頭；沒有回 None。"""
    last = message.splitlines()[-1] if message else ""
    if ": " not in last:
        return None
    tail = last.rsplit(": ", 1)[1]
    return tail if COMMAND_TAIL.match(tail) else None


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
        langs = [k.split(".", 1)[1] for k in row if k.startswith("situation.")]
        for f, v in row.items():
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
        for lang in langs:
            if not row[f"situation.{lang}"]:
                errors.append(f"{at}:situation.{lang}: 必填（retired 也保留原意）")
        for f in (f"situation.{BASE_LANG}", f"message.{BASE_LANG}"):
            if CHINESE.search(row[f]):
                errors.append(f"{at}:{f}: 不准含中文字元；中文寫在 .zh-TW 欄")
        if status == "retired":
            for f, v in row.items():
                if f not in ("code", "status") and not f.startswith("situation.") and v:
                    errors.append(f"{at}:{f}: retired 列只留 code、status、situation.<lang>，這欄要清空")
            continue
        message = row[f"message.{BASE_LANG}"]
        if status == "active":
            if level not in LEVELS:
                errors.append(f"{at}:level: active 列只准 warn、error、fatal")
            elif exit_code != EXIT_CODES[level]:
                errors.append(f"{at}:exit_code: {level} 必須是 {EXIT_CODES[level]}")
            for lang in langs:
                if not row[f"message.{lang}"]:
                    errors.append(f"{at}:message.{lang}: active 列必填")
        command = ending_command(message)
        base_placeholders = set(PLACEHOLDER.findall(message))
        for lang in langs:
            if lang == BASE_LANG:
                continue
            fa = f"{at}:message.{lang}"
            other = row[f"message.{lang}"]
            if not other or not message:
                continue
            if set(PLACEHOLDER.findall(other)) != base_placeholders:
                errors.append(f"{fa}: <…> 占位符要與 message.{BASE_LANG} 相同：{' '.join(sorted(base_placeholders))}")
            if other.count("\n") != message.count("\n"):
                errors.append(f"{fa}: 換行數要與 message.{BASE_LANG} 相同（{message.count(chr(10))} 個）")
            if command and command not in other:
                errors.append(f"{fa}: 要逐字包含 message.{BASE_LANG} 的結尾指令：{command}")
        if disp not in DISPOSITIONS:
            errors.append(f"{at}:disposition: 只准 pending、failed 或空白")
        if level == "warn" and disp:
            errors.append(f"{at}:disposition: warn 一律空白")
        if (
            status == "active"
            and not disp
            and level != "warn"
            and not row[f"situation.{BASE_LANG}"].startswith(USAGE_ERROR)
        ):
            errors.append(f"{at}:disposition: 只有 warn 與用法錯誤（situation.{BASE_LANG} 以 {USAGE_ERROR} 開頭）可留空")
        if disp == "pending" and message and not command:
            errors.append(f"{at}:message.{BASE_LANG}: pending 列要以指令結尾（「: 」後接占位符或 {'、'.join(COMMAND_NAMES)} 指令）")
        fa = f"{at}:message.{BASE_LANG}"
        if message and not (message[0].isupper() or message.startswith("<") or re.match(r"just(?:\s|$)", message)):
            errors.append(f"{fa}: 句首要大寫，或以占位符、小寫指令名 just 開頭")
        if message and not (message.endswith(".") or command or COMMAND_END.search(message)):
            errors.append(f"{fa}: 結尾要是句點，或以指令結尾")
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
                    errors.append(f"{where}: [{text}]({target}) 改連 {CSV_PATH.name}；{MD_PATH.name} 不放逐碼內容")


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
    """規則 9：文件裡的診斷範例要與 CSV 的 level、message.en 第一行一致。"""
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
            message = row.get(f"message.{BASE_LANG}") or ""
            first_line = message.splitlines()[0] if message else ""
            if not message_pattern(first_line).fullmatch(body):
                errors.append(f"{where}: {code} 的本文不符合 CSV message.{BASE_LANG} 第一行：{first_line}")


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
