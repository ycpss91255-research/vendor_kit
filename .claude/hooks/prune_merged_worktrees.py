#!/usr/bin/env python3
"""SessionStart hook：刪掉 PR 已 merge 而且乾淨的 worktree。

主目錄是 repo 的主 worktree（CLAUDE_PROJECT_DIR；在 linked worktree 裡開 session 時，
從 .git 檔回推主 worktree）。只看位於 <主目錄上一層>/worktree/ 底下的 worktree，
目前 session 所在的 worktree 不動。

每個 worktree 取分支名，下面任一成立就算已 merge：
- gh pr list --head <分支> --state merged 有結果；
- 分支是 origin/main 的祖先，而且分支頂端不在 origin/main 的 first-parent 鏈上
  （剛從 main 開出、還沒有自己 commit 的分支不算）。

已 merge 且 git status --porcelain 為空：git worktree remove、git branch -d（失敗就留著）、
最後 git worktree prune。已 merge 但有未提交改動：不刪，在 additionalContext 裡提醒。
gh 或 git fetch 失敗（沒網路等）就什麼都不刪。整體限時 20 秒，任何例外都 exit 0。
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from repo_paths import main_dir

REPO = "ycpss91255-research/vendor_kit"
BUDGET = 20.0
DEADLINE = time.monotonic() + BUDGET


class Abort(Exception):
    """gh／fetch 失敗或超時：什麼都不刪。"""




def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    left = DEADLINE - time.monotonic()
    if left <= 0:
        raise Abort("timeout")
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=left)
    except (subprocess.TimeoutExpired, OSError) as e:
        raise Abort(str(e))


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(root), *args])


def list_worktrees(root: Path) -> list[tuple[Path, str | None]]:
    out = git(root, "worktree", "list", "--porcelain")
    if out.returncode != 0:
        raise Abort("worktree list")
    items = []
    path, branch = None, None
    for line in out.stdout.splitlines() + [""]:
        if line.startswith("worktree "):
            path, branch = Path(line[len("worktree "):]), None
        elif line.startswith("branch refs/heads/"):
            branch = line[len("branch refs/heads/"):]
        elif not line and path is not None:
            items.append((path, branch))
            path, branch = None, None
    return items


def inside(path: Path, root: Path) -> bool:
    return root in path.parents


def merged_by_gh(branch: str) -> bool:
    out = run(["gh", "pr", "list", "-R", REPO, "--head", branch, "--state", "merged",
               "--json", "number", "-q", "length"])
    if out.returncode != 0:
        raise Abort("gh")
    try:
        return int(out.stdout.strip() or "0") > 0
    except ValueError:
        raise Abort("gh output")


def merged_by_ancestry(root: Path, branch: str, first_parent: set[str]) -> bool:
    tip = git(root, "rev-parse", "--verify", "-q", f"refs/heads/{branch}")
    if tip.returncode != 0:
        return False
    sha = tip.stdout.strip()
    if sha in first_parent:
        return False
    return git(root, "merge-base", "--is-ancestor", sha, "origin/main").returncode == 0


def prune(root: Path) -> tuple[list[str], list[str]]:
    base = root.parent / "worktree"
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    targets = [(p, b) for p, b in list_worktrees(root)
               if b and inside(p.resolve(), base) and p.resolve() != project]
    if not targets:
        return [], []
    if git(root, "fetch", "-q", "origin").returncode != 0:
        raise Abort("fetch")
    fp = git(root, "rev-list", "--first-parent", "origin/main")
    first_parent = set(fp.stdout.split()) if fp.returncode == 0 else set()

    # 先把判斷全部做完（gh 並行查）；gh 任何一次失敗就整批不刪
    with ThreadPoolExecutor(max_workers=8) as pool:
        by_gh = list(pool.map(merged_by_gh, [b for _, b in targets]))
    merged = [(p, b) for (p, b), g in zip(targets, by_gh)
              if g or merged_by_ancestry(root, b, first_parent)]

    removed, dirty = [], []
    for path, branch in merged:
        st = git(path, "status", "--porcelain")
        if st.returncode != 0:
            continue
        changes = [l for l in st.stdout.splitlines() if l.strip()]
        if changes:
            dirty.append(f"{path}（分支 {branch}，{len(changes)} 個未提交的檔）")
            continue
        if git(root, "worktree", "remove", str(path)).returncode != 0:
            continue
        kept = git(root, "branch", "-d", branch).returncode != 0
        removed.append(f"{path}（分支 {branch}{'，本機分支未刪' if kept else ''}）")
    if removed:
        git(root, "worktree", "prune")
    return removed, dirty


def main() -> int:
    try:
        sys.stdin.read()
    except Exception:
        pass
    try:
        removed, dirty = prune(main_dir())
    except Exception:
        return 0
    if not removed and not dirty:
        return 0
    lines = []
    if removed:
        lines.append("已刪除 PR 已 merge 且乾淨的 worktree：")
        lines += [f"- {r}" for r in removed]
    if dirty:
        lines.append("PR 已 merge 但有未提交改動，沒刪（處理完再手動 git worktree remove）：")
        lines += [f"- {d}" for d in dirty]
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(lines),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
