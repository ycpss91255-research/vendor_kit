#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：issue 本文與標題開好後不准再改，後續一律用留言。

擋的內容：
- gh issue edit 帶 --body／-b／--body-file／-F（改本文）或 --title／-t（改標題；標題也算開頭）。
- gh api 對 repos/<o>/<r>/issues/<n>（不含 /comments 等子路徑）用 -X PATCH／--method PATCH，
  且帶 body 或 title 欄位（-f／-F／--field／--raw-field body=…、title=…）或 --input。

放行：gh issue edit 改標籤、指派、milestone 等其他欄位；gh issue comment／close／reopen／create；
PR 相關指令；gh api 的 GET 與 sub_issues、dependencies 等子路徑的 POST。

指令用 shlex 依 &&、||、;、|、& 與換行切段後逐段比對，串接的指令每段都查。
"""
import json
import re
import shlex
import sys

SEPARATORS = {"&&", "||", ";", "|", "&", "\n", ";;", "|&"}
ISSUE_EDIT_OPTS = {"--body", "-b", "--body-file", "-F", "--title", "-t"}
FIELD_OPTS = {"-f", "-F", "--field", "--raw-field"}
ISSUE_PATH = re.compile(r"^/?repos/[^/\s]+/[^/\s]+/issues/[^/\s]+/?$")
FIELD_KEYS = ("body=", "title=")
REASON = (
    "issue 本文與標題開好後不准再改；後續一律用 `gh issue comment` 留言。"
    "map（wayfinder）的新定案也用留言記錄。"
)


def segments(command: str) -> list[list[str]]:
    try:
        lx = shlex.shlex(command, posix=True, punctuation_chars="();<>|&\n")
        lx.whitespace = " \t\r"
        lx.whitespace_split = True
        toks = list(lx)
    except ValueError:
        # 引號不成對時退回逐段切：寧可多查，不要整段跳過
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


def issue_edit_violation(args: list[str]) -> bool:
    for t in args:
        if t in ISSUE_EDIT_OPTS or t.split("=", 1)[0] in ISSUE_EDIT_OPTS:
            return True
        # 短選項黏值：-bxxx、-txxx、-Fxxx
        if re.fullmatch(r"-[btF].+", t):
            return True
    return False


def api_violation(args: list[str]) -> bool:
    method = None
    has_path = False
    has_body = False
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
        elif t in FIELD_OPTS:
            if nxt.startswith(FIELD_KEYS):
                has_body = True
            i += 2
            continue
        elif t.startswith(("--field=", "--raw-field=")):
            if t.split("=", 1)[1].startswith(FIELD_KEYS):
                has_body = True
        elif re.fullmatch(r"-[fF].+", t):
            if t[2:].startswith(FIELD_KEYS):
                has_body = True
        elif t == "--input" or t.startswith("--input="):
            has_body = True
        elif ISSUE_PATH.match(t.split("?", 1)[0]):
            has_path = True
        i += 1
    return has_path and method == "PATCH" and has_body


def violations(command: str) -> list[str]:
    bad = []
    for toks in segments(command):
        toks = strip_prefix(toks)
        if len(toks) < 2 or toks[0] != "gh":
            continue
        if toks[1] == "issue" and len(toks) >= 3 and toks[2] == "edit":
            if issue_edit_violation(toks[3:]):
                bad.append(" ".join(toks))
        elif toks[1] == "api":
            if api_violation(toks[2:]):
                bad.append(" ".join(toks))
    return bad


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    bad = violations(command)
    if not bad:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"{REASON}（擋下：{'；'.join(bad)}）",
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
