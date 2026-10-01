#!/usr/bin/env python3
"""檢查現行文件遵守 GLOSSARY.md 的名詞規則。

`check_context.py` 只管 GLOSSARY.md 自己；這支管其他所有文件。改名改到一半、
舊詞留在某一頁，靠人逐輪目視一定會漏，所以寫成腳本擋掉。

用法：python3 script/check_terms.py
已定案要保留舊詞的個別行寫在 WHITELIST（逐行、逐字串登記）。
另外檢查對外頁的名詞首次出現連結，並擋目錄規則：repo 根目錄有 docs/ 就失敗。
CSV 的殘留位置報 `<檔>:<代碼>:<欄名>`，不報實體行號。
全乾淨印 OK 回 0；有殘留逐筆印出回 1。
"""
import csv
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

# 這些路徑不掃：送審副本、vendored 的第三方 skill。
# 共同點是「文字不是我們寫的，或不是現行規範」，拿我們的名詞規範去掃它只會產生假警報。
EXCLUDE_PREFIXES = (
    "doc/review/",  # 送審資料夾：正文副本與標示版，正式檔另外掃
    ".claude/skills/",
    ".agents/skills/",  # skill 的實體目錄；.claude/skills 是指過來的 symlink，git 追蹤的是這條路徑
)
EXCLUDE_FILES = ()

# 帶這些標記的行是在引述舊詞，不算殘留。要放行新的講法就加在這裡。
QUOTE_MARKERS = (
    "舊名",
    "已廢止",
    "已移除",
    "之名作廢",
    "舊審閱頁",
    "改名",  # 「已定案的改名：X→Y」這種紀錄本來就得同時寫出新舊兩個詞
)

# 白名單：(檔案路徑, 該行必須包含的字串, 理由)。三個欄位都要對上才放行，而且只
# 放行「那段字串裡面」的舊詞——把字串從該行挖掉之後還找得到舊詞，照樣算殘留。
# 只比對詞會讓那個詞全域失效、只比對檔案會讓整個檔失效，白名單就變成漏洞。
WHITELIST = ()

# 特例：只有單獨的「簽章」才是名詞「印記」的舊名；「數位簽章」是密碼學的標準
# 術語（digital signature），跟印記無關，講 registry 或 image 的簽章時本來就該
# 這樣寫，所以用負向前瞻把它排除，不然這支腳本會逼著大家把正確的詞改掉。
SPECIAL_PATTERNS = {
    "簽章": r"(?<!數位)簽章",
}


def whitelisted(rel: str, line: str, pat: re.Pattern) -> bool:
    """這一行的這個舊詞是否被白名單放行。

    放行的條件：檔案路徑相符、該行含有白名單登記的字串，而且把那段字串（所有出現
    處）挖掉之後，這一行就再也搜不到這個舊詞——也就是舊詞只出現在被放行的那段字
    裡。同一個檔的其他行、或同一行的其他位置用到舊詞，都還是會被抓到。
    """
    rest = line
    matched = False
    for wl_rel, wl_text, _reason in WHITELIST:
        if wl_rel == rel and wl_text in rest:
            rest = rest.replace(wl_text, "")
            matched = True
    return matched and not pat.search(rest)


def avoid_terms(context: Path) -> list[str]:
    """從 GLOSSARY.md 的 `_Avoid_:` 行抽出所有要避免的詞（不寫死清單）。"""
    terms = []
    for ln in context.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("_Avoid_:"):
            continue
        for w in re.split(r"[、,，]", ln[len("_Avoid_:"):]):
            w = w.strip().strip("`").strip()
            if w and w not in terms:
                terms.append(w)
    return terms


def target_files() -> list[Path]:
    """現行的 .md 檔：git 追蹤的加上未追蹤的，扣掉排除路徑與已刪除的項目。"""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    files, seen = [], set()
    for rel in out:
        rel = rel.strip()
        if not rel or rel in seen:
            continue
        seen.add(rel)
        if not rel.endswith(".md"):
            continue
        if rel.startswith(EXCLUDE_PREFIXES) or rel in EXCLUDE_FILES:
            continue
        path = ROOT / rel
        if not path.is_file():  # index 裡還留著已刪除的項目
            continue
        files.append(path)
    return sorted(files)


U_TAG = re.compile(r"</?u>")
INS_TAG = re.compile(r"</?ins>")
HEADING = re.compile(r"^#{1,6}\s+")
FENCE = re.compile(r"^\s*(```|~~~)")
LINK = re.compile(r"\[([^\[\]]*)\]\(([^)\s]+)\)")
GLOSSARY_ENTRY = re.compile(r"^\*\*(.+?)\*\*(?:\s+\([^)]*\))?：")
GLOSSARY_GROUP = re.compile(r"^###\s+(.+?)\s*#*\s*$")
REVIEW_PAGE = re.compile(r"^0[1-4]_.+\.md$")
# CSV 裡會寫出文字的欄；code、status、level、exit_code、disposition 是固定值域，由 check_messages.py 管
CSV_TEXT_FIELDS = ("situation", "message", "description", "next_step")


def csv_cells(root: Path) -> list[tuple[str, str, str]]:
    """doc/contract/*.csv 的文字欄：（檔, `<代碼>:<欄名>`, 欄位文字）。格式錯誤交給 check_messages.py。"""
    out = []
    for path in sorted((root / "doc/contract").glob("*.csv")):
        rel = path.relative_to(root).as_posix()
        try:
            rows = list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines(keepends=True)))
        except (csv.Error, UnicodeDecodeError):
            continue
        for row in rows:
            for field in CSV_TEXT_FIELDS:
                value = row.get(field) or ""
                if value:
                    out.append((rel, f"{row.get('code', '?')}:{field}", value))
    return out


def line_hits(rel: str, ln: str, patterns) -> list[str]:
    """這一行（或 CSV 的一格）殘留的 _Avoid_ 詞與 <u>。"""
    if ln.startswith("_Avoid_:") or any(mark in ln for mark in QUOTE_MARKERS):
        return []
    found = [term for term, pat in patterns if pat.search(ln) and not whitelisted(rel, ln, pat)]
    # GitHub 轉換 markdown 時會刪掉 <u>；名詞改用連結，不再用 HTML 標記。
    spans = code_spans(ln) if rel.endswith(".md") else []
    if any(not any(start <= match.start() < end for start, end in spans) for match in U_TAG.finditer(ln)):
        found.append("<u>（名詞改用連結）")
    return found


def github_slug(text: str) -> str:
    """產生本 repo 標題所用的 GitHub 錨點。"""
    text = re.sub(r"\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def glossary_terms(context: Path) -> dict[str, str]:
    """依粗體詞條抽出「名詞 -> 所在 ### 分群錨點」；`A` / `B` 拆成兩詞。"""
    terms: dict[str, str] = {}
    group = ""
    for line in context.read_text(encoding="utf-8").splitlines():
        heading = GLOSSARY_GROUP.match(line)
        if heading:
            group = github_slug(heading.group(1))
            continue
        entry = GLOSSARY_ENTRY.match(line)
        if not entry or not group:
            continue
        for name in re.split(r"\s+/\s+", entry.group(1)):
            name = name.strip().strip("`")
            if name:
                terms[name] = group
    return terms


def review_pages(root: Path) -> list[Path]:
    """需要名詞首次出現連結的對外文件。"""
    paths = [root / "README.md"]
    paths.extend(sorted(p for p in (root / "doc/contract").glob("*.md") if REVIEW_PAGE.match(p.name)))
    return [p for p in paths if p.is_file()]


def code_spans(line: str) -> list[tuple[int, int]]:
    """回傳 CommonMark 行內 code span 的近似範圍（相同長度反引號成對）。"""
    runs = [(m.start(), m.end()) for m in re.finditer(r"`+", line)]
    spans = []
    used = set()
    for i, (start, end) in enumerate(runs):
        if i in used:
            continue
        for j in range(i + 1, len(runs)):
            if j not in used and runs[j][1] - runs[j][0] == end - start:
                spans.append((start, runs[j][1]))
                used.update((i, j))
                break
    return spans


def body_segments(line: str):
    """依原文順序產生正文片段；行內碼略過，連結則附上目的地。"""
    excluded = code_spans(line)
    links = list(LINK.finditer(line))
    pos = 0
    while pos < len(line):
        code = next((span for span in excluded if span[0] == pos), None)
        if code:
            pos = code[1]
            continue
        link = next((match for match in links if match.start() == pos), None)
        if link:
            yield link.group(1), link.group(2)
            pos = link.end()
            continue
        stops = [len(line)]
        stops.extend(start for start, _ in excluded if start > pos)
        stops.extend(match.start() for match in links if match.start() > pos)
        end = min(stops)
        yield line[pos:end], None
        pos = end


def mentioned_terms(text: str, names: list[str]) -> list[str]:
    """由左至右找名詞；同位置取最長者，避免把「VK recipe」再算成「VK」。"""
    text = text.replace(r"\<", "<").replace(r"\>", ">")
    found = []
    pos = 0
    while pos < len(text):
        candidates = []
        for name in names:
            start = text.find(name, pos)
            while start >= 0:
                end = start + len(name)
                left_bad = name[0].isalnum() and start and (text[start - 1].isalnum() or text[start - 1] == "_")
                right_bad = name[-1].isalnum() and end < len(text) and (text[end].isalnum() or text[end] == "_")
                if not left_bad and not right_bad:
                    candidates.append((start, -len(name), name))
                    break
                start = text.find(name, start + 1)
        if not candidates:
            break
        start, neg_len, name = min(candidates)
        found.append(name)
        pos = start - neg_len
    return found


def glossary_link_matches(page: Path, destination: str, term: str, groups: dict[str, str], context: Path) -> bool:
    """連結是否指到 GLOSSARY.md 中實際收錄 term 的分群。"""
    raw_path, separator, fragment = destination.partition("#")
    raw_path = raw_path.strip("<>")
    try:
        target = (page.parent / unquote(raw_path)).resolve()
    except (OSError, ValueError):
        return False
    return separator == "#" and target == context.resolve() and unquote(fragment) == groups[term]


def links_to_glossary(page: Path, destination: str, context: Path) -> bool:
    """目的地檔案是否為 GLOSSARY.md（錨點可錯，留給 matches 報錯）。"""
    raw_path = destination.partition("#")[0].strip("<>")
    try:
        return (page.parent / unquote(raw_path)).resolve() == context.resolve()
    except (OSError, ValueError):
        return False


def glossary_link_errors(root: Path, context: Path, groups: dict[str, str]) -> list[tuple[str, int, str, str]]:
    """檢查對外頁的 <ins>，以及每個名詞第一次正文出現時的連結。"""
    errors = []
    names = sorted(groups, key=len, reverse=True)
    for page in review_pages(root):
        rel = page.relative_to(root).as_posix()
        seen = set()
        fenced = False
        for no, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced or HEADING.match(line):
                continue
            if INS_TAG.search(line):
                errors.append((rel, no, "<ins>", "名詞不再用底線，改用 GLOSSARY.md 連結"))
            for text, destination in body_segments(line):
                # 一般連結文字不是正文（目錄等頁內連結尤其不能搶走第一次出現）；
                # 指向名詞表的連結則是本規則要驗證的標記。
                if destination is not None and not links_to_glossary(page, destination, context):
                    continue
                for term in mentioned_terms(text, names):
                    if destination is not None and not glossary_link_matches(page, destination, term, groups, context):
                        errors.append((rel, no, term, f"名詞連結分群錯誤：{destination}"))
                    if term in seen:
                        continue
                    seen.add(term)
                    if destination is None:
                        errors.append((rel, no, term, "第一次出現於正文時沒有連到 GLOSSARY.md"))
    return errors


def layout_errors(root: Path) -> list[str]:
    """repo 的目錄規則：文件一律放 doc/，根目錄不准有 docs/。

    兩個目錄並存時，新檔放哪邊全看當下誰寫，連結與腳本裡寫死的路徑會跟著分岔。
    """
    if (root / "docs").is_dir():
        return ["repo 根目錄有 docs/：一律用 doc/，不用 docs/"]
    return []


def main() -> int:
    context = ROOT / "GLOSSARY.md"
    if not context.is_file():
        print(f"找不到 {context}")
        return 1

    terms = avoid_terms(context)
    if not terms:
        print("GLOSSARY.md 抽不到任何 _Avoid_ 詞，格式可能壞了")
        return 1
    patterns = [(t, re.compile(SPECIAL_PATTERNS.get(t, re.escape(t)))) for t in terms]
    groups = glossary_terms(context)
    if not groups:
        print("GLOSSARY.md 抽不到任何粗體名詞，格式可能壞了")
        return 1

    files = target_files()
    hits = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        for no, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for term in line_hits(rel, ln, patterns):
                hits.append((rel, no, term, ln.strip()))
    cells = csv_cells(ROOT)
    for rel, where, value in cells:
        for term in line_hits(rel, value, patterns):
            hits.append((rel, where, term, value.replace("\n", " ").strip()))

    term_link_hits = glossary_link_errors(ROOT, context, groups)

    layout = layout_errors(ROOT)
    for e in layout:
        print(e)

    for rel, no, term, ln in hits:
        shown = ln if len(ln) <= 60 else ln[:60] + "…"
        print(f"{rel}:{no}  {term}  {shown}")
    for rel, no, term, reason in term_link_hits:
        print(f"{rel}:{no}  {term}  {reason}")
    tail = f"掃 {len(files)} 個 .md 檔、{len(list((ROOT / 'doc/contract').glob('*.csv')))} 個 CSV、{len(terms)} 個 _Avoid_ 詞、{len(groups)} 個名詞、白名單 {len(WHITELIST)} 筆"
    bad = bool(hits or term_link_hits or layout)
    print(f"{'OK' if not bad else 'FAIL'}: {tail}" + ("" if not hits else f"、殘留 {len(hits)} 處")
          + ("" if not term_link_hits else f"、名詞連結 {len(term_link_hits)} 處")
          + ("" if not layout else "、根目錄有 docs/"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
