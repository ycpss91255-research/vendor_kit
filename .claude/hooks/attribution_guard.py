#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：commit、PR、issue 不准寫入 Claude 署名或 session 連結。

擋的內容：Co-Authored-By: Claude、noreply@anthropic.com、claude.ai/code/session_、
「Generated with [Claude Code]」。指令本身與 -F／--file／--body-file／--message-file 帶入的檔都查。

全域設定 ~/.claude/settings.json 的 attribution 已關掉，這個 hook 是第二道。
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

BANNED = re.compile(
    r"Co-Authored-By:\s*Claude|noreply@anthropic\.com|claude\.ai/code/session_|Generated with \[?Claude Code",
    re.IGNORECASE,
)
# 會把文字寫進 commit、PR、issue 的子指令（逐段比對開頭，避免唯讀指令因字串裡碰巧有這些字被擋）
WRITES = re.compile(
    r"^\s*(?:\w+=\S*\s+)*(?:"
    r"git(?:\s+-C\s+\S+)?\s+commit\b"
    r"|gh\s+(?:pr|issue)\s+(?:create|edit|comment)\b"
    r"|gh\s+api\b.*(?:-X\s*(?:POST|PATCH|PUT)|\s-[fF]\s|--field|--raw-field|--input)"
    r")"
)
SPLIT = re.compile(r"&&|\|\||;|\||\n")
FILE_OPTS = {"-F", "--file", "--body-file", "--message-file"}


def files_in(command: str, cwd: Path) -> list[Path]:
    out = []
    try:
        toks = shlex.split(command)
    except ValueError:
        return out
    for i, t in enumerate(toks):
        val = None
        if t in FILE_OPTS and i + 1 < len(toks):
            val = toks[i + 1]
        elif "=" in t and t.split("=", 1)[0] in FILE_OPTS:
            val = t.split("=", 1)[1]
        if val and val != "-":
            p = Path(os.path.expanduser(val))
            out.append(p if p.is_absolute() else cwd / p)
    return out


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    cwd = Path(data.get("cwd") or os.getcwd())
    hits = []
    segs = SPLIT.split(command)
    if not any(WRITES.search(seg) for seg in segs):
        return 0
    # 有寫入指令時查整個指令：多行 -m 訊息會被換行切開，只查那一段會漏掉署名行
    if BANNED.search(command):
        hits.append("指令內容")
    for f in files_in(command, cwd):
        try:
            if BANNED.search(f.read_text(errors="ignore")):
                hits.append(str(f))
        except OSError:
            pass
    if not hits:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"{'、'.join(hits)}含 Claude 署名或 session 連結（Co-Authored-By: Claude、"
            "claude.ai/code/session_、Generated with Claude Code）。commit、PR、issue 只寫作者本人的資訊："
            "拿掉這些行再執行。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
