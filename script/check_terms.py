#!/usr/bin/env python3
"""檢查現行 .md 檔沒有殘留根 CONTEXT.md 的 _Avoid_ 詞。

`check_context.py` 只管 CONTEXT.md 自己；這支管其他所有文件。改名改到一半、
舊詞留在某一頁，靠人逐輪目視一定會漏，所以寫成腳本擋掉。

用法：python3 script/check_terms.py
已定案要保留舊詞的個別行寫在 WHITELIST（逐行、逐字串登記）。
全乾淨印 OK 回 0；有殘留逐筆印出回 1。
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 這些路徑不掃：歷史快照、本地產物、外部素材原文、vendored 的第三方 skill、已凍結的架構圖。
# 共同點是「文字不是我們寫的，或不是現行規範」，拿我們的名詞規範去掃它只會產生假警報。
EXCLUDE_PREFIXES = (
    "doc/decisions/_legacy/",
    "doc/decisions/_backup/",
    "doc/decisions/review_log/",
    "doc/decisions/review/research/",
    "doc/decisions/research/",
    "doc/decisions/_marked/",
    ".claude/skills/",
    ".agents/skills/",  # skill 的實體目錄；.claude/skills 是指過來的 symlink，git 追蹤的是這條路徑
    "script/diagram/",
)
EXCLUDE_FILES = ("discussion.drawio",)

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
    """從 CONTEXT.md 的 `_Avoid_:` 行抽出所有要避免的詞（不寫死清單）。"""
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


def main() -> int:
    context = ROOT / "CONTEXT.md"
    if not context.is_file():
        print(f"找不到 {context}")
        return 1

    terms = avoid_terms(context)
    if not terms:
        print("CONTEXT.md 抽不到任何 _Avoid_ 詞，格式可能壞了")
        return 1
    patterns = [(t, re.compile(SPECIAL_PATTERNS.get(t, re.escape(t)))) for t in terms]

    files = target_files()
    hits = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        for no, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if ln.startswith("_Avoid_:"):
                continue
            if any(mark in ln for mark in QUOTE_MARKERS):
                continue
            for term, pat in patterns:
                if pat.search(ln) and not whitelisted(rel, ln, pat):
                    hits.append((rel, no, term, ln.strip()))
            # GitHub 轉換 markdown 時會刪掉 <u>，底線不會顯示；名詞底線一律用 <ins>（#60）
            if U_TAG.search(ln):
                hits.append((rel, no, "<u>（改用 <ins>）", ln.strip()))

    for rel, no, term, ln in hits:
        shown = ln if len(ln) <= 60 else ln[:60] + "…"
        print(f"{rel}:{no}  {term}  {shown}")
    tail = f"掃 {len(files)} 個 .md 檔、{len(terms)} 個 _Avoid_ 詞、白名單 {len(WHITELIST)} 筆"
    print(f"{'OK' if not hits else 'FAIL'}: {tail}" + ("" if not hits else f"、殘留 {len(hits)} 處"))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
