#!/usr/bin/env python3
"""PreToolUse hook（matcher: Edit|Write）：檔案只寫做什麼與相關說明，不寫決策紀錄。

決策與討論經過放 issue。例外：對外契約（根目錄 README.md、審閱頁 doc/contract/0N_*.md；
搬家前在 doc/decisions/review/0N_*.md）
與 ADR（doc/adr/）本來就是記錄決定的地方。

只管 repo 追蹤範圍內的檔：主 worktree 或 linked worktree（repo_paths 的 main_dir、worktree_root）
底下、且沒被 .gitignore 忽略的路徑。repo 外的檔（scratchpad 裡的 issue 留言暫存檔、/tmp、
workspace 的 reference/、Claude Code 的記憶檔）與被忽略的過程產物目錄一律放行。

擋的內容（只看這次寫入的新文字）：日期（YYYY-MM-DD），以及直接引用某人的話（「維護者：「…」」這種寫法）。
描述流程的句子（例如「維護者回覆定案才 merge」）不擋。
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from repo_paths import main_dir, worktree_root

ALLOWED = re.compile(r"(^|/)(README\.md|doc/(?:contract|decisions/review)/0\d_[^/]+\.md|doc/adr/[^/]+\.md)$")
BANNED = re.compile(r"\b20\d\d-\d\d-\d\d\b|(?:維護者|使用者)[^\n。]{0,4}[:：]\s*「")


def new_text(tool: str, inp: dict) -> str:
    if tool == "Write":
        return inp.get("content") or ""
    if tool == "Edit":
        return inp.get("new_string") or ""
    return ""


def inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def ignored(target: Path) -> bool:
    """git check-ignore 說被忽略才算；不在 git 裡或 git 出錯都當沒被忽略（照擋）。"""
    base = target.parent
    while not base.is_dir() and base != base.parent:
        base = base.parent
    try:
        r = subprocess.run(["git", "-C", str(base), "check-ignore", "-q", str(target)],
                           capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0


def in_repo(raw: str, cwd: Path) -> bool:
    p = Path(os.path.expanduser(raw))
    target = (p if p.is_absolute() else cwd / p).resolve()
    if not any(inside(target, root) for root in (main_dir(), worktree_root())):
        return False
    return not ignored(target)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool = data.get("tool_name")
    inp = data.get("tool_input") or {}
    path = str(inp.get("file_path") or "")
    if tool not in ("Edit", "Write") or not path or ALLOWED.search(path):
        return 0
    if not in_repo(path, Path(data.get("cwd") or os.getcwd())):
        return 0  # repo 外（scratchpad、/tmp、記憶檔）或被 .gitignore 忽略的過程產物
    hits = sorted(set(BANNED.findall(new_text(tool, inp))))
    if not hits:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"{path} 的新內容有決策紀錄（{'、'.join(hits)}）。檔案只寫做什麼與相關說明；"
            "日期、誰決定的、討論經過放 issue。對外契約（README、審閱頁 01～04）與 ADR 除外。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
