#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：`gh pr create` 之前檢查 PR 規則，違規就擋下。

規則本身不寫在這裡：本文從 --body-file（或 --body）讀，改動檔用
`git diff --name-only origin/<base>...HEAD` 取，交給 script/github/check_pr_rules.py 判斷
（規則 A：至少連一個 issue；一個邏輯目的：範圍表 script/github/scope.json）。之後的 CI 呼叫同一支。
出處：issue #140。

讀不到輸入、指令不是 `gh pr create`、找不到檢查腳本時一律放行，不擋正常操作。
沒給本文（--fill、互動模式）時擋下，要求改用 --body-file。
"""
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[2] / "script" / "github" / "check_pr_rules.py"
SEPARATORS = {"&&", "||", ";", "|", "&", "\n"}


def segments(command: str) -> list[list[str]]:
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    out, cur = [], []
    try:
        for tok in lex:
            if tok in SEPARATORS or set(tok) <= set("&|;"):
                if cur:
                    out.append(cur)
                cur = []
            else:
                cur.append(tok)
    except ValueError:
        return []
    if cur:
        out.append(cur)
    return out


def option(args: list[str], *names: str):
    for i, a in enumerate(args):
        for n in names:
            if a == n and i + 1 < len(args):
                return args[i + 1]
            if n.startswith("--") and a.startswith(n + "="):
                return a[len(n) + 1:]
    return None


def find_pr_create(command: str, cwd: str):
    """回傳 (gh pr create 的參數, 執行時的目錄)；不是就回傳 None。"""
    for seg in segments(command):
        if len(seg) >= 2 and seg[0] == "cd":
            cwd = os.path.join(cwd, os.path.expanduser(seg[1]))
            continue
        if seg[:3] == ["gh", "pr", "create"]:
            return seg[3:], cwd
    return None


def deny(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))


def changed_files(cwd: str, base: str) -> list[str]:
    r = subprocess.run(["git", "-C", cwd, "diff", "--name-only", f"origin/{base}...HEAD"],
                       capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    found = find_pr_create(command, data.get("cwd") or os.getcwd())
    if found is None or not CHECKER.is_file():
        return 0
    args, cwd = found
    body_file = option(args, "--body-file", "-F")
    body = option(args, "--body", "-b")
    if body_file is None and body is None:
        deny("gh pr create 要用 --body-file 給本文，才能檢查 PR 有沒有連 issue（#140）。")
        return 0
    if body_file is not None:
        try:
            body = Path(cwd, os.path.expanduser(body_file)).read_text(encoding="utf-8")
        except OSError as e:
            deny(f"讀不到 --body-file：{e}")
            return 0
    files = changed_files(cwd, option(args, "--base", "-B") or "main")
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(body)
        tmp = f.name
    try:
        r = subprocess.run([sys.executable, str(CHECKER), "--body-file", tmp, "--files-from", "-"],
                           input="\n".join(files), capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    try:
        result = json.loads(r.stdout)
    except ValueError:
        return 0
    if not result.get("ok"):
        deny("PR 規則不符（#140；規則在 script/github/check_pr_rules.py 與 scope.json）：\n- "
             + "\n- ".join(result.get("problems", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
