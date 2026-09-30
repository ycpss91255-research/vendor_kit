#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：commit、PR、issue 不准寫入 Claude 署名或 session 連結。

擋的內容：Co-Authored-By: Claude、noreply@anthropic.com、claude.ai/code/session_、
「Generated with [Claude Code]」。指令本身與 -F／--file／--body-file／--message-file 帶入的檔都查。

維護者 2026-09-30：GitHub Contributors 出現 claude（Co-Authored-By 對應到 claude 帳號）、
commit 裡有 session 連結；「用 hook 確保以後不會再有這個資訊被寫入 commit 或是 issue 或是 pr」。
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
# 會把文字寫進 commit、PR、issue 的指令
WRITES = re.compile(r"\bgit\b.*\bcommit\b|\bgh\s+(pr|issue)\s+(create|edit|comment)\b|\bgh\s+api\b")
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
    if not WRITES.search(command):
        return 0
    cwd = Path(data.get("cwd") or os.getcwd())
    hits = []
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
            "claude.ai/code/session_、Generated with Claude Code）。維護者規定 commit、PR、issue "
            "只寫維護者本人的資訊：拿掉這些行再執行。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
