#!/usr/bin/env python3
"""PreToolUse hook（matcher: Edit|Write|NotebookEdit|Bash）：repo 主目錄只放最新的 main。

主目錄是 repo 的主 worktree（CLAUDE_PROJECT_DIR；在 linked worktree 裡開 session 時，
從 .git 檔回推主 worktree）。所有改動到上一層的 worktree/pr/<編號>、worktree/issue/<編號>
或 worktree/branch/<分支名> 做。

擋的內容：
- Edit／Write／NotebookEdit：目標檔在主目錄底下。例外是 .claude/hooks/、.claude/workflows/、
  .claude/settings.json、.claude/settings.local.json：還沒 merge 的 hook、workflow、設定
  要在主目錄放一份本機生效副本。
- Bash：對主目錄做的 git 寫入（工作目錄在主目錄且沒用 -C 指到別處，或 -C 指到主目錄）。
  擋 commit、revert、rebase、reset、cherry-pick、am、stash（list／show 除外）、
  tag（列出除外）、branch -f、restore、switch／checkout 到 main 以外（含 checkout -- <路徑>）、
  merge（只放行 merge --ff-only origin/main）、pull（只放行 pull --ff-only）。
  status、log、diff、show、fetch、worktree 等唯讀或不動主目錄的指令放行。

只攔 Edit／Write 與 git 寫入；Bash 用 sed、cp、重導寫進主目錄的檔不攔。
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

SPLIT = re.compile(r"&&|\|\||;|\||\n")
EXEMPT_DIRS = (".claude/hooks/", ".claude/workflows/")
EXEMPT_FILES = {".claude/settings.json", ".claude/settings.local.json"}
# git 全域選項裡會吃掉下一個 token 的
GLOBAL_VALUE_OPTS = {"-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
ALWAYS_DENY = {"commit", "revert", "rebase", "reset", "cherry-pick", "am", "restore"}
HINT = (
    "主目錄只放最新的 main，不在這裡改檔或動 git 狀態。"
    "改動到 ../worktree/pr/<編號>（沒 PR 用 issue/<編號>，都沒有用 branch/<分支名>）做；"
    "主目錄只准 git switch main、git pull --ff-only、git merge --ff-only origin/main 跟上最新。"
)


def main_dir() -> Path:
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    dotgit = project / ".git"
    if dotgit.is_file():
        # linked worktree：.git 內容是 gitdir: <主 worktree>/.git/worktrees/<名>
        m = re.match(r"gitdir:\s*(.+)", dotgit.read_text(errors="ignore").strip())
        if m:
            gitdir = Path(m.group(1))
            gitdir = gitdir if gitdir.is_absolute() else project / gitdir
            gitdir = gitdir.resolve()
            if gitdir.parent.name == "worktrees":
                return gitdir.parent.parent.parent
    return project


def resolve(raw: str, base: Path) -> Path:
    p = Path(os.path.expandvars(os.path.expanduser(raw)))
    return (p if p.is_absolute() else base / p).resolve()


def inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def deny(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))
    return 0


def check_file(path: str, cwd: Path, root: Path) -> str | None:
    target = resolve(path, cwd)
    if not inside(target, root):
        return None
    rel = target.relative_to(root).as_posix()
    if rel in EXEMPT_FILES or rel.startswith(EXEMPT_DIRS):
        return None
    return f"{target} 在主目錄 {root} 底下。{HINT}"


def git_violation(sub: str, args: list[str]) -> bool:
    """這個 git 子指令在主目錄執行時會不會改動主目錄。"""
    opts = [a for a in args if a.startswith("-")]
    plain = [a for a in args if not a.startswith("-")]
    if sub in ALWAYS_DENY:
        return True
    if sub == "stash":
        return not (plain and plain[0] in ("list", "show"))
    if sub == "tag":
        return not (not args or "-l" in args or "--list" in args)
    if sub == "branch":
        return any(a == "--force" or re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a) for a in opts)
    if sub == "switch":
        creates = {"-c", "-C", "--create", "--force-create", "--orphan", "--detach", "-d"}
        return bool(creates & set(opts)) or plain != ["main"]
    if sub == "checkout":
        if "--" in args:
            return True
        creates = {"-b", "-B", "--orphan", "--detach", "-p", "--patch"}
        return bool(creates & set(opts)) or plain != ["main"]
    if sub == "merge":
        return sorted(args) != ["--ff-only", "origin/main"]
    if sub == "pull":
        return "--ff-only" not in args or any(a.startswith("--rebase") or a == "-r" for a in args)
    return False


def check_bash(command: str, cwd: Path, root: Path) -> list[str]:
    bad = []
    here = cwd
    for seg in SPLIT.split(command):
        try:
            toks = shlex.split(seg)
        except ValueError:
            continue
        while toks and re.fullmatch(r"\w+=.*", toks[0]):
            toks = toks[1:]  # 前置的環境變數
        if not toks:
            continue
        if toks[0] == "cd" and len(toks) >= 2:
            here = resolve(toks[1], here)
            continue
        if toks[0] != "git":
            continue
        target = here
        i = 1
        while i < len(toks) and toks[i].startswith("-"):
            t = toks[i]
            if t == "-C" and i + 1 < len(toks):
                target = resolve(toks[i + 1], target)
                i += 2
                continue
            if t in GLOBAL_VALUE_OPTS:
                i += 2
                continue
            i += 1
        if i >= len(toks) or not inside(target, root):
            continue
        sub, args = toks[i], toks[i + 1:]
        if git_violation(sub, args):
            bad.append(seg.strip())
    return bad


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool = data.get("tool_name")
    inp = data.get("tool_input") or {}
    cwd = Path(data.get("cwd") or os.getcwd())
    root = main_dir()
    if tool in ("Edit", "Write", "NotebookEdit"):
        path = str(inp.get("file_path") or inp.get("notebook_path") or "")
        reason = check_file(path, cwd, root) if path else None
        return deny(reason) if reason else 0
    if tool == "Bash":
        bad = check_bash(inp.get("command") or "", cwd, root)
        if bad:
            return deny(f"這些 git 指令會改動主目錄 {root}：{'；'.join(bad)}。{HINT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
