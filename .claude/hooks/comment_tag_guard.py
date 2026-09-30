#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：agent 發的 issue／PR 留言要標出是誰寫的，開 issue／PR 要用檔案。

留言標記：本文去掉前導空白後，第一行開頭必須是 [claude]、[codex] 或 [agy]。
沒有標記的留言視為維護者本人寫的；[codex] 只能貼 codex 原文，Claude 不得代寫。
查的指令：
- gh issue comment、gh pr comment：--body／-b 查字串，--body-file／-F 讀檔查；
  讀 stdin（-）或沒給本文的無法確認，一律擋。
- gh pr review 帶 --body／-b／--body-file／-F：同上；沒帶本文（只 --approve 等）放行。
- gh issue close、gh pr close 帶 --comment／-c：直接擋，要先用 comment 留言再關。
- gh api 寫入 .../comments 端點（方法不是 GET，且帶 body 欄位或 --input）：
  -f／--raw-field body=… 查字串，-F／--field body=@檔 讀檔查，--input 讀 JSON 的 body 查。

開 issue／PR：
- gh issue create、gh pr create 必須用 --body-file／-F，不准 --body／-b。
- gh issue create 必須帶 --label／-l。

本機絕對路徑：上面查到的本文（留言、review、create 的 --body-file、gh api 的 body）
都不准含本機絕對路徑（見 LOCAL_PATHS）。例外：[codex]／[agy] 留言是工具原文不能改寫，
只要本文第二行以後另有一行以「註：」或「（註」開頭（說明對應 repo 的相對路徑）就放行。
[claude] 留言與 issue／PR 本文一律不准含。create 的本文檔讀不到時也擋（無法確認）。

指令用 shlex 依 &&、||、;、|、& 與換行切段後逐段比對，串接的指令每段都查。
相對路徑以 hook 收到的 cwd 為準。
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

TAGS = ("[claude]", "[codex]", "[agy]")
SEPARATORS = {"&&", "||", ";", "|", "&", "\n", ";;", "|&"}
BODY_OPTS = {"--body", "-b"}
FILE_OPTS = {"--body-file", "-F"}
FIELD_OPTS = {"-f", "-F", "--field", "--raw-field"}
# 本機絕對路徑的樣式：這些路徑對其他人沒用（別人的機器上不存在），
# 還會洩漏使用者名稱與本機目錄結構，所以不准出現在發到 GitHub 的內容。
LOCAL_PATHS = (
    (re.compile(r"/home/[^/\s]+/"), "/home/<user>/"),
    (re.compile(r"/Users/[^/\s]+/"), "/Users/<user>/"),
    (re.compile(r"/tmp/claude-"), "/tmp/claude-"),
    (re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE), "C:\\Users\\"),
)
RAW_TAGS = ("[codex]", "[agy]")
NOTE_PREFIXES = ("註：", "（註")
PATH_MARK = "本機絕對路徑"
PATH_RULE = (
    "發到 GitHub 的內容（留言、review、issue／PR 本文、gh api 的 body）不准含本機絕對路徑"
    "（/home/<user>/、/Users/<user>/、/tmp/claude-、C:\\Users\\）：對其他人沒用，也會洩漏使用者名稱；"
    "改寫成 repo 內的相對路徑。[codex]／[agy] 留言是原文不能改，改在第二行以後另起一行，"
    "以「註：」或「（註」開頭說明，例如「（註：原文含本機路徑，對應 repo 的 script/x.py）」。"
)
TAG_RULE = (
    "agent 發的 issue／PR 留言，本文第一行一律以 [claude]、[codex] 或 [agy] 開頭；"
    "沒有標記的留言視為維護者本人寫的。[codex] 只能貼 codex 原文，Claude 不得代寫。"
)


def segments(command: str) -> list[list[str]]:
    try:
        lx = shlex.shlex(command, posix=True, punctuation_chars="();<>|&\n")
        lx.whitespace = " \t\r"
        lx.whitespace_split = True
        toks = list(lx)
    except ValueError:
        toks = []
        for seg in re.split(r"&&|\|\||;|\||\n", command):
            toks += seg.split() + [";"]
    out, cur = [], []
    for t in toks:
        if t in SEPARATORS or set(t) <= set("();<>|&\n"):
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        out.append(cur)
    return out


def strip_prefix(toks: list[str]) -> list[str]:
    while toks and re.fullmatch(r"\w+=.*", toks[0]):
        toks = toks[1:]  # 前置的環境變數
    while toks and toks[0] in ("env", "command", "sudo", "exec"):
        toks = toks[1:]
    return toks


def opt_values(args: list[str], names: set[str]) -> list[str]:
    """取出 names 裡任一選項的值（支援 --opt v、--opt=v、短選項黏值 -bv）。"""
    vals = []
    i = 0
    while i < len(args):
        t = args[i]
        if t in names:
            vals.append(args[i + 1] if i + 1 < len(args) else "")
            i += 2
            continue
        key = t.split("=", 1)[0]
        if t.startswith("--") and "=" in t and key in names:
            vals.append(t.split("=", 1)[1])
        elif not t.startswith("--") and len(t) > 2 and t[:2] in names:
            vals.append(t[2:])
        i += 1
    return vals


def has_opt(args: list[str], names: set[str]) -> bool:
    return any(t in names or t.split("=", 1)[0] in names
               or (not t.startswith("--") and len(t) > 2 and t[:2] in names)
               for t in args)


def tagged(text: str) -> bool:
    first = text.lstrip().split("\n", 1)[0]
    return first.startswith(TAGS)


def local_path_problem(text: str, src: str, raw_ok: bool) -> str | None:
    """text 含本機絕對路徑就回傳問題說明；raw_ok 時 [codex]／[agy] 原文附註解行可放行。"""
    hits = [label for pat, label in LOCAL_PATHS if pat.search(text)]
    if not hits:
        return None
    lines = text.lstrip().split("\n")
    if raw_ok and lines[0].startswith(RAW_TAGS) and any(
            ln.strip().startswith(NOTE_PREFIXES) for ln in lines[1:]):
        return None
    return f"{src} 含{PATH_MARK}（{'、'.join(hits)}）"


def read(path: str, cwd: Path) -> str | None:
    if not path or path == "-":
        return None
    p = Path(os.path.expandvars(os.path.expanduser(path)))
    p = p if p.is_absolute() else cwd / p
    try:
        return p.read_text(errors="ignore")
    except OSError:
        return None


def body_problem(args: list[str], cwd: Path, required: bool) -> str | None:
    """查 --body／--body-file 給的本文；回傳問題說明，沒問題回 None。"""
    bodies = opt_values(args, BODY_OPTS)
    files = opt_values(args, FILE_OPTS)
    if not bodies and not files:
        return "沒給本文，無法確認標記；用 --body-file 或 --body 給本文" if required else None
    for b in bodies:
        if not tagged(b):
            return "--body 本文第一行沒有 [claude]／[codex]／[agy] 標記"
        problem = local_path_problem(b, "--body 本文", raw_ok=True)
        if problem:
            return problem
    for f in files:
        text = read(f, cwd)
        if text is None:
            return f"讀不到本文檔 {f!r}（stdin 無法確認標記；先寫成檔再用 --body-file）"
        if not tagged(text):
            return f"本文檔 {f} 第一行沒有 [claude]／[codex]／[agy] 標記"
        problem = local_path_problem(text, f"本文檔 {f}", raw_ok=True)
        if problem:
            return problem
    return None


def api_problem(args: list[str], cwd: Path) -> str | None:
    path = next((t for t in args if re.match(r"^/?repos/\S+/comments(/\S*)?$", t.split("?", 1)[0])), None)
    if not path:
        return None
    method = None
    bodies = []  # (來源, 文字或 None)
    i = 0
    while i < len(args):
        t = args[i]
        nxt = args[i + 1] if i + 1 < len(args) else ""
        if t in ("-X", "--method"):
            method, i = nxt.upper(), i + 2
            continue
        if t.startswith("--method="):
            method = t.split("=", 1)[1].upper()
        elif re.fullmatch(r"-X.+", t):
            method = t[2:].upper()
        elif t in FIELD_OPTS or t.startswith(("--field=", "--raw-field=")) or re.fullmatch(r"-[fF].+", t):
            if t in FIELD_OPTS:
                opt, val = t, nxt
                i += 1
            elif t.startswith("--"):
                opt, val = t.split("=", 1)
            else:
                opt, val = t[:2], t[2:]
            if val.startswith("body="):
                val = val[len("body="):]
                typed = opt in ("-F", "--field")
                if typed and val.startswith("@"):
                    bodies.append((val[1:], read(val[1:], cwd)))
                else:
                    bodies.append(("body 欄位", val))
        elif t == "--input" or t.startswith("--input="):
            src = nxt if t == "--input" else t.split("=", 1)[1]
            if t == "--input":
                i += 1
            raw = read(src, cwd)
            try:
                text = json.loads(raw).get("body") if raw is not None else None
            except (ValueError, AttributeError):
                text = None
            bodies.append((f"--input {src}", text if isinstance(text, str) else None))
        i += 1
    if method == "GET" or not bodies:
        return None
    for src, text in bodies:
        if text is None:
            return f"讀不到 {src} 的 body，無法確認標記"
        if not tagged(text):
            return f"{src} 第一行沒有 [claude]／[codex]／[agy] 標記"
        problem = local_path_problem(text, src, raw_ok=True)
        if problem:
            return problem
    return None


def check(toks: list[str], cwd: Path) -> str | None:
    if len(toks) < 3 or toks[0] != "gh":
        return None
    kind, sub, args = toks[1], toks[2], toks[3:]
    if kind in ("issue", "pr"):
        if sub == "comment":
            return body_problem(args, cwd, required=True)
        if kind == "pr" and sub == "review":
            return body_problem(args, cwd, required=False)
        if sub == "close" and has_opt(args, {"--comment", "-c"}):
            return "close 不准帶 --comment；先用 gh issue comment／gh pr comment 留言再關"
        if sub == "create":
            if has_opt(args, BODY_OPTS) or not has_opt(args, FILE_OPTS):
                return "create 的本文一律用 --body-file 給，不准 --body／-b"
            if kind == "issue" and not has_opt(args, {"--label", "-l"}):
                return "issue create 必須帶 --label"
            for f in opt_values(args, FILE_OPTS):
                text = read(f, cwd)
                if text is None:
                    return f"讀不到本文檔 {f!r}，無法確認是否含{PATH_MARK}（先寫成檔再用 --body-file）"
                problem = local_path_problem(text, f"本文檔 {f}", raw_ok=False)
                if problem:
                    return problem
        return None
    if kind == "api":
        return api_problem(toks[2:], cwd)
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    cwd = Path(data.get("cwd") or os.getcwd())
    bad = []
    for toks in segments(command):
        toks = strip_prefix(toks)
        problem = check(toks, cwd)
        if problem:
            bad.append(f"{' '.join(toks[:3])}：{problem}")
    if not bad:
        return 0
    rule = PATH_RULE + TAG_RULE if any(PATH_MARK in b for b in bad) else TAG_RULE
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{'；'.join(bad)}。{rule}",
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
