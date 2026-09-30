#!/usr/bin/env python3
"""PreToolUse hook（matcher: Bash）：git worktree 只准開在固定位置。

位置是 repo 上一層的 worktree/，依序判斷：
- 有 PR：worktree/pr/<編號>
- 沒 PR、有 issue：worktree/issue/<編號>
- 都沒有：worktree/branch/<分支名>

開在 /tmp、scratchpad 或 repo 上一層的其他地方，用完常忘了收，
2026-09-20 以前在上一層留下幾十個目錄就是這樣來的（維護者 2026-09-30）。
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

VALUE_OPTS = {"-b", "-B", "--reason", "--orphan"}
ALLOWED = re.compile(r"^(pr|issue)/\d+$|^branch/.+$")


def worktree_root() -> Path:
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    return project.parent / "worktree"


def add_paths(command: str) -> list[str]:
    """找出指令裡每個 `git … worktree add` 的目標路徑。"""
    out = []
    for part in re.split(r"&&|\|\||;|\n", command):
        try:
            toks = shlex.split(part)
        except ValueError:
            continue
        for i in range(len(toks) - 1):
            if toks[i] == "worktree" and toks[i + 1] == "add" and "git" in toks[:i]:
                rest = toks[i + 2:]
                j = 0
                while j < len(rest):
                    t = rest[j]
                    if t in VALUE_OPTS:
                        j += 2
                        continue
                    if t.startswith("-"):
                        j += 1
                        continue
                    out.append(t)
                    break
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
    root = worktree_root()
    bad = []
    for raw in add_paths(command):
        target = Path(os.path.expandvars(os.path.expanduser(raw)))
        target = (cwd / target) if not target.is_absolute() else target
        target = Path(os.path.normpath(target))
        try:
            rel = target.relative_to(root).as_posix()
        except ValueError:
            bad.append(raw)
            continue
        if not ALLOWED.match(rel):
            bad.append(raw)
    if not bad:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"worktree 位置不對：{'、'.join(bad)}。只准開在 {root}/ 底下："
            "有 PR 放 pr/<編號>，沒 PR 有 issue 放 issue/<編號>，都沒有放 branch/<分支名>。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
