#!/usr/bin/env python3
"""檢查訊息表 doc/contract/03_messages.csv（每個原因代碼的唯一出處，#122）。

格式：UTF-8 加 BOM（恰好一個）、只准 LF、檔尾一個換行、逗號分隔、照 RFC 4180 跳脫；
表頭逐字等於 FIELDS。規則：

1. 格式：每列欄數相同、用 csv 模組以 strict 解析；欄位頭尾不准空白；
   不准以 =、+、-、@、Tab、CR 開頭（Excel 公式注入）。
2. 代碼：VK 加四位數字；從 VK0001 起逐列加一（唯一、遞增、不缺列；停用的留列）。
3. status 只准 active、retired；retired 列除 code、status、situation、note 外都要空白。
4. active 列：level 只准 warn、error、fatal；situation、message 必填。
5. disposition 只准「需人處理」「失敗」或空白；warn 一律空白；需人處理必有 next_step；失敗的 next_step 必須空白。
6. next_step 有值時必須逐字出現在 message 裡。
7. 欄位不准 HTML 與 Markdown；不帶屬性的 <…> 算占位符；< 與 > 要成對。
8. invariant：空白，或 02 的條號（`## N.` 標題），多個用 ; 分隔、遞增。
9. details：空白，或 `03_messages.md#vknnnn`（只准等於本列代碼）；跟 03_messages.md 的
   `### VKnnnn` 節一一對應。
10. 引用：README.md、doc/contract/*.md、GLOSSARY.md 裡的每個 VKnnnn 都要在 CSV 且是 active；
    doc/adr/*.md 只要求存在。連結文字是代碼時：目標是 03_messages.csv 不准帶 #；
    目標是 03_messages.md 時錨點要是 #vknnnn、跟連結文字同一個代碼、該列 details 指同一個目標。
    01、02 不准連 CSV。

指令寫法（CSV 的 message、next_step、note 裡的 `just vendor_kit …`）由 check_review_pages.py 檢查。
錯誤位置報 `<檔>:<代碼>:<欄名>`，不報實體行號。CSV 還不存在時跳過並印 OK。

用法：python3 script/check_messages.py（在 repo 根目錄跑；有問題以 1 結束）
"""
import csv
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
REVIEW = ROOT / "doc/contract"
CSV_PATH = REVIEW / "03_messages.csv"
MD_PATH = REVIEW / "03_messages.md"
FIELDS = ["code", "status", "level", "disposition", "situation", "message", "next_step", "note", "invariant", "details"]
STATUS = {"active", "retired"}
LEVELS = {"warn", "error", "fatal"}
DISPOSITIONS = {"需人處理", "失敗", ""}
RETIRED_KEEP = {"code", "status", "situation", "note"}
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
FENCE = re.compile(r"^\s*(```|~~~)")


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


def invariant_numbers(errors: list[str]) -> set[int]:
    pages = sorted(REVIEW.glob("02_*.md"))
    if not pages:
        errors.append(f"{rel(REVIEW)}: 找不到 02 不變量頁，無法檢查 invariant")
        return set()
    return {int(m.group(1)) for m in re.finditer(r"(?m)^##\s+(\d+)\.", pages[0].read_text())}


def detail_sections(errors: list[str]) -> dict[str, int]:
    """03_messages.md 的 `### VKnnnn` 節：代碼 → 行號。標題只准寫代碼，錨點才會是 #vknnnn。"""
    out: dict[str, int] = {}
    if not MD_PATH.exists():
        return out
    fenced = False
    for i, line in enumerate(MD_PATH.read_text().splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^###\s+(.*?)\s*$", line)
        if not m or not re.match(r"VK\d{4}", m.group(1)):
            continue
        code = m.group(1)
        if not CODE.match(code):
            errors.append(f"{rel(MD_PATH)}:{i}: 長說明節的標題只寫代碼（`### VKnnnn`），錨點才會是 #vknnnn")
            continue
        if code in out:
            errors.append(f"{rel(MD_PATH)}:{i}: {code} 的長說明節重複")
        out[code] = i
    return out


def check_rows(rows: list[dict[str, str]], errors: list[str]) -> dict[str, dict[str, str]]:
    where = rel(CSV_PATH)
    invariants = invariant_numbers(errors)
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
        status, level, disp = row["status"], row["level"], row["disposition"]
        if status not in STATUS:
            errors.append(f"{at}:status: 只准 active、retired")
        if not row["situation"]:
            errors.append(f"{at}:situation: 必填（retired 也保留原意）")
        if status == "retired":
            for f in FIELDS:
                if f not in RETIRED_KEEP and row[f]:
                    errors.append(f"{at}:{f}: retired 列只留 code、status、situation、note，這欄要清空")
            continue
        if status == "active":
            if level not in LEVELS:
                errors.append(f"{at}:level: active 列只准 warn、error、fatal")
            if not row["message"]:
                errors.append(f"{at}:message: active 列必填")
        if disp not in DISPOSITIONS:
            errors.append(f"{at}:disposition: 只准「需人處理」「失敗」或空白")
        if level == "warn" and disp:
            errors.append(f"{at}:disposition: warn 一律空白")
        if disp == "需人處理" and not row["next_step"]:
            errors.append(f"{at}:next_step: 需人處理必有下一步")
        if disp == "失敗" and row["next_step"]:
            errors.append(f"{at}:next_step: 失敗的 next_step 必須空白")
        if row["next_step"] and row["next_step"] not in row["message"]:
            errors.append(f"{at}:next_step: 要逐字出現在 message 裡")
        inv = row["invariant"]
        if inv:
            parts = inv.split(";")
            if not all(re.fullmatch(r"[1-9]\d*", p) for p in parts):
                errors.append(f"{at}:invariant: 要是 02 的條號（整數），多個用 ; 分隔")
            else:
                nums = [int(p) for p in parts]
                if nums != sorted(set(nums)):
                    errors.append(f"{at}:invariant: 條號要遞增、不重複")
                missing = [x for x in nums if invariants and x not in invariants]
                if missing:
                    errors.append(f"{at}:invariant: 02 沒有第 {missing} 條（`## N.` 標題）")
        det = row["details"]
        if det and CODE.match(code) and det != f"03_messages.md#{code.lower()}":
            errors.append(f"{at}:details: 只准空白或 03_messages.md#{code.lower()}（純文字、等於本列代碼）")
    sections = detail_sections(errors)
    for code, row in by_code.items():
        if row["details"] and code not in sections:
            errors.append(f"{where}:{code}:details: {rel(MD_PATH)} 沒有 `### {code}` 節")
    for code, line in sections.items():
        if code not in by_code or not by_code[code]["details"]:
            errors.append(f"{rel(MD_PATH)}:{line}: `### {code}` 節在 CSV 裡沒有對應的 details")
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
                file_part, sep, frag = target.partition("#")
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
                if not same(dest, MD_PATH) or not CODE.match(label):
                    continue
                if not re.fullmatch(r"vk\d{4}", frag):
                    errors.append(f"{where}: [{text}]({target}) 改連 03_messages.csv；只有 details 有值的代碼才連 03_messages.md#vknnnn")
                    continue
                if frag != label.lower():
                    errors.append(f"{where}: 連結文字 {label} 跟錨點 #{frag} 不是同一個代碼")
                    continue
                row = by_code.get(label)
                if row is not None and row["details"] != f"03_messages.md#{frag}":
                    errors.append(f"{where}: {label} 的 details 是空的或不同，要連 03_messages.csv：{target}")


def check(errors: list[str]) -> bool:
    """回傳 CSV 是否存在。"""
    if not CSV_PATH.exists():
        return False
    rows = load(CSV_PATH, errors)
    if rows is None:
        return True
    by_code = check_rows(rows, errors)
    check_refs(by_code, errors)
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
