#!/usr/bin/env python3
"""檢查 commit 訊息格式（規格見 vendor_kit#110 的「維護者決議與定案」）。

格式：

    <type>[(<scope>)][!]: <繁中描述>
    <空行>
    <內文，可省略>
    <空行>
    <footer，可省略：Refs: #N／Closes #N／BREAKING CHANGE: …／Doc-Edit: rNN>

用法：
    python3 script/check_commit_msg.py <訊息檔>        # commit-msg hook 用；會去掉 # 註解行
    python3 script/check_commit_msg.py -               # 從 stdin 讀整則訊息
    python3 script/check_commit_msg.py --title -       # 只檢查一行標題（PR 標題）
    python3 script/check_commit_msg.py --range A..B    # 逐一檢查 A..B 的每個 commit

全部合格回 0；有不合格逐條印出回 1；用法錯誤回 2。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata

# type 固定九種（#110 定案）。perf、build 暫時用不到，但先留著，以後補反而要改檢查器。
TYPES = ("feat", "fix", "docs", "refactor", "test", "perf", "build", "ci", "chore")

# scope 固定清單（#110 定案的初版）。scope 可省略；跨區域的改動就不寫。
# 新增 scope 要開 PR 改這個常數，跟一般 PR 一起審；不准在 commit 裡自己發明新 scope，
# 否則很快就會出現同義詞（「圖」「圖面」「架構圖」都已經出現過）。
SCOPES = (
    "contract",
    "adr",
    "glossary",
    "readme",
    "diagram",
    "cli",
    "engine",
    "bootstrap",
    "hooks",
    "ci",
    "tools",
)

MAX_WIDTH = 72  # 標題顯示寬度硬上限（東亞寬字元算 2 欄）
SOFT_WIDTH = 50  # 建議值，超過只提示、不算失敗

# 句尾不准出現的標點（全形與半形）。
TRAILING_PUNCT = "。．.，,、；;：:！!？?…"

HEADER_RE = re.compile(
    r"^(?P<type>[^(!:：\s]+)(?:\((?P<scope>[^)]*)\))?(?P<bang>!)?(?P<colon>[:：])(?P<space>\s*)(?P<desc>.*)$"
)

# 豁免：git revert 與 git merge 產生的預設標題。
REVERT_RE = re.compile(r'^Revert ".+"$')
MERGE_RE = re.compile(r"^Merge (branch|remote-tracking branch|pull request|tag|commit|refs/)\b")
# 例外中的例外：把 main 併進自己分支的 merge commit。分支更新一律用 rebase。
MERGE_MAIN_RE = re.compile(
    r"^Merge (branch|remote-tracking branch) '(origin/)?main'( of \S+)? into "
)

# Claude 署名與 session 連結（跟 .claude/hooks/attribution_guard.py 同一組）。
# 那支只擋 Claude 的工具呼叫；這裡在 commit-msg 與 CI 再擋一次，其他來源的 commit 也擋得到。
BANNED_RE = re.compile(
    r"Co-Authored-By:\s*Claude|noreply@anthropic\.com|claude\.ai/code/session_|Generated with \[?Claude Code",
    re.IGNORECASE,
)

ISSUE = r"(?:[\w.-]+/[\w.-]+)?#\d+"
REFS_RE = re.compile(rf"^Refs: {ISSUE}(?:, {ISSUE})*$")
CLOSES_RE = re.compile(rf"^Closes {ISSUE}$")
BREAKING_RE = re.compile(r"^BREAKING CHANGE: \S")
DOC_EDIT_RE = re.compile(r"^Doc-Edit: r\d{2,}( light)?$")

# 看起來像 footer 的行：開頭是這些關鍵字（不分大小寫、後面接冒號、空白或 #）。
# issue 類要後面接 `#N`，其他要接冒號，免得內文剛好用 fix、refs 開頭的句子被誤判。
FOOTER_KEY_RE = re.compile(
    rf"^(?:(?P<key>refs?|close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s*{ISSUE}"
    r"|(?P<key2>breaking[ -]change|doc[ -]?edit)\s*:)",
    re.IGNORECASE,
)

FOOTER_HELP = {
    "refs": "只是相關寫 `Refs: #N`（多個用 `Refs: #1, #2`）",
    "closes": "真的完整解決才寫 `Closes #N`（沒有冒號、一行一個）",
    "fixes": "關閉 issue 一律寫 `Closes #N`；只是相關寫 `Refs: #N`",
    "breaking": "破壞性變更寫 `BREAKING CHANGE: <內容與遷移方式>`（大寫、空格、冒號）",
    "doc-edit": "doc-edit 輪次寫 `Doc-Edit: rNN`（light 模式可寫 `Doc-Edit: rNN light`）",
}


def display_width(s: str) -> int:
    """終端機顯示寬度：東亞寬字元（W、F）算 2 欄，其他算 1 欄。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)


def strip_comments(text: str) -> str:
    """去掉 git 編輯器模板的 # 註解行與 scissors 線以下的內容（commit-msg hook 用）。"""
    out = []
    for ln in text.splitlines():
        if ln.startswith("# ") and ">8" in ln and "-" * 8 in ln:
            break
        if ln.startswith("#"):
            continue
        out.append(ln)
    return "\n".join(out)


def check_title(title: str) -> tuple[list[str], list[str]]:
    """檢查標題。回傳 (錯誤, 提示)。"""
    errors: list[str] = []
    notes: list[str] = []
    fmt = "正確寫法：`<type>(<scope>): <繁中描述>`，例如 `docs(contract): 補上承諾對象的定義`"

    if MERGE_MAIN_RE.match(title):
        errors.append(
            "分支裡不准有把 main 併進來的 merge commit。更新分支請改用 rebase："
            "`git fetch origin && git rebase origin/main`，再 `git push --force-with-lease`"
        )
        return errors, notes
    if REVERT_RE.match(title) or MERGE_RE.match(title):
        return errors, notes

    if title != title.strip():
        errors.append("標題前後不能有空白")
        title = title.strip()
    if not title:
        errors.append("標題是空的。" + fmt)
        return errors, notes

    m = HEADER_RE.match(title)
    if not m:
        errors.append("標題缺少 `type: ` 前綴。" + fmt)
        return errors, notes

    typ, scope, colon, space, desc = m["type"], m["scope"], m["colon"], m["space"], m["desc"]
    if typ not in TYPES:
        hint = f"（type 要小寫：`{typ.lower()}`）" if typ.lower() in TYPES else ""
        errors.append(f"type `{typ}` 不在清單內{hint}。可用的 type：{' '.join(TYPES)}")
    if scope is not None:
        if scope == "":
            errors.append("scope 的括號是空的。沒有 scope 就整個省略，寫成 `type: 描述`")
        elif scope not in SCOPES:
            errors.append(
                f"scope `{scope}` 不在清單內。可用的 scope：{' '.join(SCOPES)}；"
                "跨區域的改動就省略 scope；要新增 scope 請開 PR 改 script/check_commit_msg.py 的 SCOPES"
            )
    if colon == "：":
        errors.append("冒號要用半形 `:` 再加一個空格，不能用全形 `：`")
    elif space != " ":
        errors.append("冒號後面要剛好一個半形空格，例如 `fix(cli): 修正…`")
    if not desc.strip():
        errors.append("冒號後面缺少描述。" + fmt)
    elif desc[-1] in TRAILING_PUNCT:
        errors.append(f"標題句尾不加標點（去掉最後的 `{desc[-1]}`）")

    w = display_width(title)
    if w > MAX_WIDTH:
        errors.append(
            f"標題顯示寬度 {w} 欄，超過上限 {MAX_WIDTH} 欄（中文字算 2 欄）。"
            "請縮短描述，細節移到內文"
        )
    elif w > SOFT_WIDTH:
        notes.append(f"標題顯示寬度 {w} 欄，建議控制在 {SOFT_WIDTH} 欄以內")
    return errors, notes


def paragraphs(lines: list[str]) -> list[list[tuple[int, str]]]:
    """把行切成段落（以空行分隔），每行帶原本的行號（從 1 起算）。"""
    paras: list[list[tuple[int, str]]] = []
    cur: list[tuple[int, str]] = []
    for i, ln in enumerate(lines, 1):
        if ln.strip():
            cur.append((i, ln))
        elif cur:
            paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    return paras


def check_footer_line(ln: str) -> str | None:
    """檢查一行 footer；合格回 None，不合格回錯誤訊息。"""
    if REFS_RE.match(ln) or CLOSES_RE.match(ln) or BREAKING_RE.match(ln) or DOC_EDIT_RE.match(ln):
        return None
    m = FOOTER_KEY_RE.match(ln)
    key = (m["key"] or m["key2"]).lower()
    if key.startswith("ref"):
        help_ = FOOTER_HELP["refs"]
    elif key.startswith("close"):
        help_ = FOOTER_HELP["closes"]
    elif key.startswith(("fix", "resolve")):
        help_ = FOOTER_HELP["fixes"]
    elif key.startswith("breaking"):
        help_ = FOOTER_HELP["breaking"]
    else:
        help_ = FOOTER_HELP["doc-edit"]
    return f"footer `{ln}` 格式不對：{help_}"


def check_message(text: str, title_only: bool = False) -> tuple[list[str], list[str]]:
    """檢查整則訊息。回傳 (錯誤, 提示)。"""
    errors: list[str] = []
    lines = text.rstrip("\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ["訊息是空的"], []

    if BANNED_RE.search(text):
        errors.append(
            "訊息含 Claude 署名或 session 連結（Co-Authored-By: Claude、claude.ai/code/session_、"
            "Generated with Claude Code）。commit 只寫作者本人的資訊，請刪掉"
        )

    title = lines[0].rstrip()
    t_err, notes = check_title(title)
    errors += t_err
    if title_only:
        if len(lines) > 1:
            errors.append("PR 標題只能有一行")
        return errors, notes

    exempt = bool(REVERT_RE.match(title) or (MERGE_RE.match(title) and not MERGE_MAIN_RE.match(title)))
    if exempt:
        return errors, notes

    if len(lines) > 1 and lines[1].strip():
        errors.append("標題與內文之間要空一行（第 2 行必須是空行）")

    body = lines[1:]
    paras = paragraphs(body)
    footer_lines: list[tuple[int, str]] = []
    for pi, para in enumerate(paras):
        is_last = pi == len(paras) - 1
        for n, ln in para:
            if not FOOTER_KEY_RE.match(ln):
                continue
            if not is_last:
                errors.append(
                    f"第 {n + 1} 行 `{ln}` 像是 footer，footer 要放在最後一段、跟內文之間空一行"
                )
                continue
            footer_lines.append((n + 1, ln))
            err = check_footer_line(ln)
            if err:
                errors.append(f"第 {n + 1} 行：{err}")

    m = HEADER_RE.match(title)
    bang = bool(m and m["bang"])
    has_breaking = any(BREAKING_RE.match(ln) for _, ln in footer_lines)
    if bang and not has_breaking:
        errors.append("標題有 `!`（破壞性變更），footer 也要寫 `BREAKING CHANGE: <內容與遷移方式>`")
    if has_breaking and not bang:
        errors.append("footer 有 `BREAKING CHANGE:`，標題的 type／scope 後面也要加 `!`，例如 `feat(cli)!: …`")
    return errors, notes


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def check_range(rev_range: str) -> int:
    """逐一檢查 rev_range 裡的每個 commit。merge commit 只檢查是不是把 main 併進來。"""
    try:
        revs = git("rev-list", "--reverse", "--parents", rev_range).split("\n")
    except subprocess.CalledProcessError as e:
        print(f"git rev-list {rev_range} 失敗：{e.stderr.strip()}", file=sys.stderr)
        return 2
    bad = 0
    total = 0
    for row in filter(None, revs):
        sha, *parents = row.split()
        total += 1
        msg = git("log", "-1", "--format=%B", sha)
        subject = msg.split("\n", 1)[0]
        if len(parents) > 1:
            errors = check_title(subject)[0] if MERGE_MAIN_RE.match(subject) else []
            notes: list[str] = []
        else:
            errors, notes = check_message(msg)
        for n in notes:
            print(f"提示 {sha[:10]} {subject}：{n}")
        if errors:
            bad += 1
            print(f"✗ {sha[:10]} {subject}")
            for e in errors:
                print(f"    - {e}")
    print(f"檢查 {total} 個 commit，{bad} 個不合格")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="檢查 commit 訊息格式（#110）")
    ap.add_argument("file", nargs="?", help="訊息檔；`-` 或省略代表 stdin")
    ap.add_argument("--title", action="store_true", help="只檢查一行標題（PR 標題）")
    ap.add_argument("--range", dest="rev_range", metavar="A..B", help="逐一檢查這段範圍的每個 commit")
    args = ap.parse_args(argv)

    if args.rev_range:
        if args.file or args.title:
            ap.error("--range 不能跟訊息檔或 --title 一起用")
        return check_range(args.rev_range)

    if args.file and args.file != "-":
        with open(args.file, encoding="utf-8") as f:
            text = strip_comments(f.read())
    else:
        text = sys.stdin.read()

    errors, notes = check_message(text, title_only=args.title)
    for n in notes:
        print(f"提示：{n}", file=sys.stderr)
    if errors:
        print("commit 訊息格式不合（規格見 vendor_kit#110）：", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
