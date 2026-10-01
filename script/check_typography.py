#!/usr/bin/env python3
"""檢查對外文件的中英混排：括號與空白（維護者定案的兩條規則）。

1. 括號內容全是 ASCII（英文、數字、符號）時用半形括號，而且半形括號與中文之間空一格：
   「檢查（test）」→「檢查 (test)」。括號內有中文就維持全形括號「（…）」。
2. 中文與英文字母或阿拉伯數字相鄰時中間空一格：「VK的recipe」→「VK 的 recipe」、
   「第12條」→「第 12 條」。全形標點（，。、：；「」（）等）與英數之間不加空白。
   行內程式碼（反引號包住的）與前後的中文相鄰時也空一格：「`0`結束」→「`0` 結束」、
   「印`VK0024`」→「印 `VK0024`」；與全形標點相鄰不加空白。

掃描範圍：README.md、doc/contract/*.md、GLOSSARY.md，以及 doc/contract/*.csv 的文字欄
（TEXT_FIELDS）。不檢查、不改：行內程式碼的內容（反引號內）、程式碼區塊、HTML 註解、URL、
Markdown 連結目標（括號裡的路徑與錨點）與參照定義行、HTML 標籤本身、CSV 的固定欄
（code、status、level、exit_code、disposition）。

HTML 標籤、連結的 [ ] 與 ](目標)、粗體記號 ** 與 __ 不算字元：`[VK](…)的` 照樣算
「VK」緊貼「的」，空格補在 ](目標) 之後、[ 之前；HTML 標籤也一樣，空格補在標籤外側，標籤不會被拆開；行內程式碼緊貼連結的
[ 或 ](目標) 時也一樣，看 [ 前、](目標) 後的字元。URL 兩側不檢查規則 2，行內程式碼兩側只查
中文（與英數、半形符號相鄰不管）；全形括號改成半形時，外側緊貼中文、英數或行內程式碼就補一格空白，
緊貼空白、行首行尾或標點就不補。反斜線跳脫的字元（程式碼名詞當連結文字時的寫法
`[\\<repo\\>](…)` 裡的 `\\<`、`\\>`）不是 HTML 標籤，兩側也不檢查規則 2。

錯誤位置：.md 報 `<檔>:<行>`，CSV 照 check_messages.py 報 `<檔>:<代碼>:<欄名>`。

用法（在 repo 根目錄跑）：
  python3 script/check_typography.py            檢查；有問題逐筆印出並以 1 結束
  python3 script/check_typography.py --fix      就地修正（只動上面兩條規則的字元），再檢查一次
  python3 script/check_typography.py [--fix] 檔...   只處理指定的檔
CSV 修正後若 next_step 不再逐字出現在 message 裡，照樣報錯（check_messages.py 的規則 6）。
"""
import argparse
import csv
import io
import pathlib
import re
import sys
from dataclasses import dataclass, field

ROOT = pathlib.Path(".")
CSV_FIELDS = [
    "code", "status", "level", "exit_code", "disposition", "situation", "message", "description", "next_step",
]
TEXT_FIELDS = ("situation", "message", "description", "next_step")
BOM = "﻿"

# 中文（含日文假名、注音、部首）；全形標點（U+3000–303F、U+FF00–FFEF）不算
CJK = re.compile(
    "[⺀-⻿⼀-⿟぀-ゟ゠-ヿ㄀-ㄯㆠ-ㆿ"
    "㐀-䶿一-鿿豈-﫿\U00020000-\U0003ffff]"
)
ALNUM = re.compile(r"[A-Za-z0-9]")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*\S")
# 網址可以含中文（IRI），一路到空白、全形標點、<、>、`、[、] 為止
URL = re.compile(r"(?:https?|ftp)://[^\s<>`\[\]\u3000-\u303f\uff00-\uffef]+|www\.[A-Za-z0-9-]+\.[^\s<>`\[\]\u3000-\u303f\uff00-\uffef]+")
TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>")
AUTOLINK = re.compile(r"<(?:[a-z][a-z0-9+.-]*:|mailto:)[^<>\s]*>|<[^<>\s@]+@[^<>\s]+>", re.I)
# 換行型的標籤兩側不算相鄰
BREAK_TAGS = {"br", "hr", "img", "p", "div", "details", "summary", "table", "tr", "td", "th", "ul", "ol", "li"}


def is_cjk(ch: str | None) -> bool:
    return bool(ch) and bool(CJK.match(ch))


def is_alnum(ch: str | None) -> bool:
    return bool(ch) and bool(ALNUM.match(ch))


@dataclass
class Tok:
    """一段文字：visible（一般字元）、open/close（不佔字元的標記）、word/brk（不檢查的區段）。"""
    kind: str
    start: int
    end: int
    ascii_text: str = ""  # 判斷括號內容是否全為 ASCII 時，這段貢獻的文字
    code: bool = False  # word 是行內程式碼（反引號包住的）


@dataclass
class Unit:
    text: str
    toks: list[Tok] = field(default_factory=list)


def _match_backticks(text: str, i: int) -> int | None:
    """text[i] 是反引號；回傳對應行內程式碼的結尾（不含），沒有結尾回 None。"""
    run = len(text[i:]) - len(text[i:].lstrip("`"))
    j = i + run
    while True:
        k = text.find("`", j)
        if k < 0:
            return None
        m = k
        while m < len(text) and text[m] == "`":
            m += 1
        if m - k == run:
            return m
        j = m


def tokenize(text: str, markdown: bool = True) -> list[Tok]:
    toks: list[Tok] = []
    i = 0
    n = len(text)
    bracket_depth = 0
    strong_open = {"**": False, "__": False}
    while i < n:
        ch = text[i]
        m = URL.match(text, i)
        if m and (i == 0 or not is_alnum(text[i - 1])):
            end = m.end()
            # 結尾的標點不算網址
            while end > i and text[end - 1] in ".,;:!?)]'\"":
                if text[end - 1] == ")" and text[i:end].count("(") >= text[i:end].count(")"):
                    break
                end -= 1
            toks.append(Tok("word", i, end, text[i:end]))
            i = end
            continue
        if not markdown:
            toks.append(Tok("visible", i, i + 1, ch))
            i += 1
            continue
        if ch == "\\" and i + 1 < n and text[i + 1] in "\\`*_{}[]()#+-.!|<>~":
            toks.append(Tok("brk", i, i + 2, text[i + 1]))
            i += 2
            continue
        if ch == "`":
            end = _match_backticks(text, i)
            if end is not None:
                toks.append(Tok("word", i, end, text[i:end], code=True))
                i = end
                continue
            run_end = i + len(text[i:]) - len(text[i:].lstrip("`"))
            toks.append(Tok("brk", i, run_end, text[i:run_end]))
            i = run_end
            continue
        if text.startswith("<!--", i):
            end = text.find("-->", i + 4)
            end = n if end < 0 else end + 3
            toks.append(Tok("brk", i, end))
            i = end
            continue
        if ch == "<":
            m = AUTOLINK.match(text, i)
            if m:
                toks.append(Tok("word", i, m.end(), text[i:m.end()]))
                i = m.end()
                continue
            m = TAG.match(text, i)
            if m:
                raw = m.group(0)
                name = re.match(r"</?([A-Za-z][A-Za-z0-9-]*)", raw).group(1).lower()
                if name in BREAK_TAGS or raw.endswith("/>"):
                    toks.append(Tok("brk", i, m.end()))
                else:
                    toks.append(Tok("close" if raw.startswith("</") else "open", i, m.end()))
                i = m.end()
                continue
        if ch == "!" and text.startswith("![", i):
            bracket_depth += 1
            toks.append(Tok("open", i, i + 2))
            i += 2
            continue
        if ch == "[":
            close = _link_close(text, i)
            if close is not None:
                bracket_depth += 1
                toks.append(Tok("open", i, i + 1))
                i += 1
                continue
        if ch == "]" and bracket_depth:
            end = _link_target_end(text, i)
            if end is not None:
                bracket_depth -= 1
                toks.append(Tok("close", i, end))
                i = end
                continue
        if text.startswith("**", i) or text.startswith("__", i):
            mark = text[i:i + 2]
            kind = "close" if strong_open[mark] else "open"
            strong_open[mark] = not strong_open[mark]
            toks.append(Tok(kind, i, i + 2))
            i += 2
            continue
        toks.append(Tok("visible", i, i + 1, ch))
        i += 1
    return toks


def _link_target_end(text: str, i: int) -> int | None:
    """text[i] 是 ]；後面接 (目標) 或 [參照] 時回傳該段結尾，否則 None。"""
    j = i + 1
    if j < len(text) and text[j] == "(":
        depth = 0
        k = j
        while k < len(text):
            if text[k] == "\\":
                k += 2
                continue
            if text[k] == "(":
                depth += 1
            elif text[k] == ")":
                depth -= 1
                if depth == 0:
                    return k + 1
            k += 1
        return None
    if j < len(text) and text[j] == "[":
        k = text.find("]", j + 1)
        return None if k < 0 else k + 1
    return None


def _link_close(text: str, i: int) -> int | None:
    """text[i] 是 [；找對應的 ]，且其後接連結目標，才算連結。"""
    depth = 0
    k = i
    while k < len(text):
        c = text[k]
        if c == "\\":
            k += 2
            continue
        if c == "`":
            end = _match_backticks(text, k)
            if end is not None:
                k = end
                continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return k if _link_target_end(text, k) is not None else None
        k += 1
    return None


@dataclass
class Issue:
    rule: str
    edits: list[tuple[int, int, str]]  # (start, end, replacement)，位置是這個字串的原始位置


def _neighbors(toks: list[Tok], idx: int, step: int):
    """從 toks[idx] 往 step 方向找第一個佔字元的 token，途中經過的 open/close 一併回傳。"""
    passed = []
    j = idx + step
    while 0 <= j < len(toks) and toks[j].kind in ("open", "close"):
        passed.append(toks[j])
        j += step
    return (toks[j] if 0 <= j < len(toks) else None), passed


def _space_pos(left: Tok, gap: list[Tok]) -> int:
    """left 與右邊字元之間夾著 gap（open/close 標記，由左至右）時空格該插在哪。
    結束標記留在左邊、開始標記留在右邊。"""
    pos = left.end
    for t in gap:
        if t.kind == "close":
            pos = t.end
        else:
            break
    return pos


def _ascii_pairs(text: str, toks: list[Tok], opener: str, closer: str) -> list[tuple[int, int]]:
    """回傳 toks 裡內容全是 ASCII 的括號對（token 索引）。"""
    stack: list[int] = []
    pairs = []
    for k, t in enumerate(toks):
        if t.kind != "visible":
            continue
        c = text[t.start]
        if c == opener:
            stack.append(k)
        elif c == closer and stack:
            o = stack.pop()
            content = "".join(x.ascii_text for x in toks[o + 1:k])
            if content.strip() and all(ord(ch) < 128 for ch in content):
                pairs.append((o, k))
    return pairs


def _outer_needs_space(tok: Tok | None, text: str, converted: bool) -> bool:
    if tok is None:
        return False
    if tok.kind == "word":
        return converted
    if tok.kind == "brk":
        return False
    c = text[tok.start]
    if is_cjk(c):
        return True
    return converted and is_alnum(c)


def find_issues(text: str, markdown: bool = True) -> list[Issue]:
    """回傳一個字串（一行或一個 CSV 欄位）裡違反規則 1、2 的地方。"""
    toks = tokenize(text, markdown)
    issues: list[Issue] = []
    spaced: set[int] = set()  # 已由規則 1 處理的插入位置

    # 規則 1：全形括號內容全是 ASCII → 半形，外側補空白
    for o, c in _ascii_pairs(text, toks, "（", "）"):
        edits = [(toks[o].start, toks[o].end, "("), (toks[c].start, toks[c].end, ")")]
        left, gap_l = _neighbors(toks, o, -1)
        if _outer_needs_space(left, text, True):
            pos = _space_pos(left, list(reversed(gap_l)))
            edits.append((pos, pos, " "))
            spaced.add(pos)
        right, gap_r = _neighbors(toks, c, 1)
        if _outer_needs_space(right, text, True):
            pos = _space_pos(toks[c], gap_r)
            edits.append((pos, pos, " "))
            spaced.add(pos)
        issues.append(Issue("括號內全是 ASCII，改用半形括號，與中文之間空一格", edits))

    # 規則 1（已是半形）：半形括號與中文之間空一格
    for o, c in _ascii_pairs(text, toks, "(", ")"):
        left, gap_l = _neighbors(toks, o, -1)
        if left is not None and left.kind == "visible" and is_cjk(text[left.start]):
            pos = _space_pos(left, list(reversed(gap_l)))
            if pos not in spaced:
                spaced.add(pos)
                issues.append(Issue("半形括號與中文之間要空一格", [(pos, pos, " ")]))
        right, gap_r = _neighbors(toks, c, 1)
        if right is not None and right.kind == "visible" and is_cjk(text[right.start]):
            pos = _space_pos(toks[c], gap_r)
            if pos not in spaced:
                spaced.add(pos)
                issues.append(Issue("半形括號與中文之間要空一格", [(pos, pos, " ")]))

    # 規則 2：中文與英數相鄰；中文與行內程式碼相鄰
    for k, t in enumerate(toks):
        if not _rule2_side(t):
            continue
        right, gap = _neighbors(toks, k, 1)
        if right is None or not _rule2_side(right):
            continue
        if t.code or right.code:
            other = right if t.code else t
            if (t.code and right.code) or not is_cjk(text[other.start]):
                continue
            rule = "行內程式碼與中文之間要空一格"
        else:
            a, b = text[t.start], text[right.start]
            if not ((is_cjk(a) and is_alnum(b)) or (is_alnum(a) and is_cjk(b))):
                continue
            rule = "中文與英數之間要空一格"
        pos = _space_pos(t, gap)
        if pos not in spaced:
            spaced.add(pos)
            issues.append(Issue(rule, [(pos, pos, " ")]))
    return issues


def _rule2_side(tok: Tok) -> bool:
    """規則 2 比對的一側：一般字元或行內程式碼。"""
    return tok.kind == "visible" or tok.code


def apply_edits(text: str, edits: list[tuple[int, int, str]]) -> str:
    for start, end, rep in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:start] + rep + text[end:]
    return text


def fix_text(text: str, markdown: bool = True) -> str:
    """修正一個字串（一行或一個 CSV 欄位）。"""
    edits = [e for iss in find_issues(text, markdown) for e in iss.edits]
    return apply_edits(text, edits)


def describe(text: str, issue: Issue) -> str:
    """「原文片段」→「修正後片段」。"""
    lo = min(e[0] for e in issue.edits)
    hi = max(e[1] for e in issue.edits)
    a, b = max(0, lo - 6), min(len(text), hi + 6)
    before = text[a:b]
    after = apply_edits(before, [(s - a, e - a, r) for s, e, r in issue.edits])
    return f"{issue.rule}：「{before}」→「{after}」"


# ---- Markdown ----

def markdown_units(lines: list[str]) -> list[int]:
    """要檢查的行索引（程式碼區塊、多行 HTML 註解的後續行、參照定義行跳過）。"""
    out: list[int] = []
    fence: str | None = None
    in_comment = False
    for idx, line in enumerate(lines):
        if fence is not None:
            m = FENCE.match(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line.strip()[len(m.group(1)):].strip():
                fence = None
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        m = FENCE.match(line)
        if m:
            fence = m.group(1)
            continue
        if REF_DEF.match(line):
            continue
        # 這一行開了 HTML 註解但沒關：這行照查（tokenize 會跳過註解），後面的行跳過
        stripped = re.sub(r"<!--.*?-->", "", line)
        if "<!--" in stripped:
            in_comment = True
        out.append(idx)
    return out


def check_markdown_text(text: str, where: str) -> list[str]:
    lines = text.split("\n")
    msgs = []
    for idx in markdown_units(lines):
        for iss in find_issues(lines[idx]):
            msgs.append(f"{where}:{idx + 1}: {describe(lines[idx], iss)}")
    return msgs


def fix_markdown_text(text: str) -> str:
    lines = text.split("\n")
    for idx in markdown_units(lines):
        lines[idx] = fix_text(lines[idx])
    return "\n".join(lines)


# ---- CSV ----

def _read_csv(text: str) -> tuple[bool, list[list[str]]]:
    bom = text.startswith(BOM)
    body = text[1:] if bom else text
    return bom, list(csv.reader(io.StringIO(body, newline=""), strict=True))


def _write_csv(bom: bool, records: list[list[str]]) -> str:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(records)
    return (BOM if bom else "") + buf.getvalue()


def _csv_rows(records: list[list[str]]):
    """(列序, code, {欄名: 欄索引})；表頭不對回空。"""
    if not records:
        return
    header = records[0]
    idx = {f: header.index(f) for f in TEXT_FIELDS if f in header}
    code_i = header.index("code") if "code" in header else None
    for n, rec in enumerate(records[1:], 1):
        code = rec[code_i] if code_i is not None and code_i < len(rec) else ""
        yield n, code or f"第 {n + 1} 筆", {f: i for f, i in idx.items() if i < len(rec)}, rec


def check_csv_text(text: str, where: str) -> list[str]:
    try:
        _bom, records = _read_csv(text)
    except csv.Error as e:
        return [f"{where}: CSV 解析失敗：{e}（格式由 check_messages.py 檢查）"]
    msgs = []
    for _n, code, cols, rec in _csv_rows(records):
        for f, i in cols.items():
            for iss in find_issues(rec[i], markdown=False):
                msgs.append(f"{where}:{code}:{f}: {describe(rec[i], iss)}")
        ns, msg = cols.get("next_step"), cols.get("message")
        if ns is None or msg is None or not rec[ns]:
            continue
        if rec[ns] in rec[msg] and fix_text(rec[ns], False) not in fix_text(rec[msg], False):
            msgs.append(f"{where}:{code}:next_step: 照規則修正後不會逐字出現在 message 裡，兩欄要一起手動改")
    return msgs


def fix_csv_text(text: str, where: str = "") -> tuple[str, list[str]]:
    """回傳（修正後文字, 修不了的問題）。CSV 不是 csv 模組的標準寫法時不改，免得動到其他字元。"""
    try:
        bom, records = _read_csv(text)
    except csv.Error as e:
        return text, [f"{where}: CSV 解析失敗，--fix 不改：{e}"]
    if _write_csv(bom, records) != text:
        return text, [f"{where}: CSV 不是標準寫法（引號或換行跟 csv 模組輸出不同），--fix 不改，請手動修"]
    problems = []
    for _n, code, cols, rec in _csv_rows(records):
        for i in cols.values():
            rec[i] = fix_text(rec[i], markdown=False)
        ns, msg = cols.get("next_step"), cols.get("message")
        if ns is not None and msg is not None and rec[ns] and rec[ns] not in rec[msg]:
            problems.append(f"{where}:{code}:next_step: 修正後不再逐字出現在 message 裡，請手動對齊")
    return _write_csv(bom, records), problems


# ---- 檔案 ----

def targets() -> list[pathlib.Path]:
    out = [ROOT / "README.md"]
    contract = ROOT / "doc/contract"
    out += sorted(contract.glob("*.md"))
    out += sorted(contract.glob("*.csv"))
    out.append(ROOT / "GLOSSARY.md")
    return [p for p in out if p.exists()]


def check_file(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    where = path.as_posix()
    if path.suffix == ".csv":
        return check_csv_text(text, where)
    return check_markdown_text(text, where)


def fix_file(path: pathlib.Path) -> tuple[bool, list[str]]:
    """就地修正；回傳（有沒有改, 修不了的問題）。"""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".csv":
        new, problems = fix_csv_text(text, path.as_posix())
    else:
        new, problems = fix_markdown_text(text), []
    if new != text:
        path.write_bytes(new.encode("utf-8"))
    return new != text, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="檢查中英混排的括號與空白")
    ap.add_argument("--fix", action="store_true", help="就地修正（只動規則 1、2 的字元）")
    ap.add_argument("files", nargs="*", type=pathlib.Path, help="只處理這些檔（預設：README.md、doc/contract/*.md|*.csv、GLOSSARY.md）")
    args = ap.parse_args(argv)
    files = args.files or targets()
    problems: list[str] = []
    if args.fix:
        for p in files:
            changed, bad = fix_file(p)
            problems += bad
            if changed:
                print(f"修正：{p.as_posix()}")
    for p in files:
        problems += check_file(p)
    for msg in problems:
        print(msg)
    if problems:
        print(f"FAIL: {len(problems)} 個問題")
        return 1
    print(f"OK: 檢查 {len(files)} 個檔")
    return 0


if __name__ == "__main__":
    sys.exit(main())
