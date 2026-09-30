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
    for f in files:
        text = read(f, cwd)
        if text is None:
            return f"讀不到本文檔 {f!r}（stdin 無法確認標記；先寫成檔再用 --body-file）"
        if not tagged(text):
            return f"本文檔 {f} 第一行沒有 [claude]／[codex]／[agy] 標記"
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
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{'；'.join(bad)}。{TAG_RULE}",
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
