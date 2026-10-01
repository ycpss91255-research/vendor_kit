"""開／收 PR 用的 worktree：位置固定在主 repo 上一層的 worktree/branch/<分支名>。

位置規則跟 .claude/hooks/worktree_guard.py 一致（沒有 PR、issue 編號時用 branch/<分支名>）。
透過腳本開的 worktree 不會經過 hook，所以這裡自己只開在允許的位置。

用法：
  python3 script/workflow/worktree.py add <branch> [--repo <主 repo>] [--base origin/main]
  python3 script/workflow/worktree.py remove <branch> [--repo <主 repo>] [--force]

add：git fetch origin，再從 <base> 開新分支 <branch> 與 worktree；worktree 目錄或本機分支已存在就報錯。
remove：git worktree remove，再刪本機分支；不刪遠端分支。分支有還沒推上遠端的 commit 時拒絕，
除非給 --force。

輸出一行 JSON：成功 {"ok": true, "action", "branch", "path", ...}；失敗 {"ok": false, "error"}，結束碼 1。
--repo 不給時用這支腳本所在 repo 的主 worktree（git common dir 的上一層），從 worktree 裡跑也一樣。
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


class Fail(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Fail(f"git {' '.join(args)} 失敗：{(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


def main_repo(start: Path) -> Path:
    """回傳主 worktree 的根目錄（git common dir 的上一層）。"""
    common = git(start, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(common).parent


def worktree_path(repo: Path, branch: str) -> Path:
    if not branch or branch.startswith("-") or ".." in branch.split("/"):
        raise Fail(f"分支名不合法：{branch!r}")
    return repo.parent / "worktree" / "branch" / branch


def branch_exists(repo: Path, branch: str) -> bool:
    r = subprocess.run(["git", "-C", str(repo), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"])
    return r.returncode == 0


def add(repo: Path, branch: str, base: str) -> dict:
    path = worktree_path(repo, branch)
    if path.exists():
        raise Fail(f"worktree 目錄已存在：{path}")
    if branch_exists(repo, branch):
        raise Fail(f"本機分支已存在：{branch}")
    git(repo, "fetch", "origin")
    path.parent.mkdir(parents=True, exist_ok=True)
    git(repo, "worktree", "add", "-b", branch, str(path), base)
    head = git(path, "rev-parse", "HEAD")
    return {"ok": True, "action": "add", "branch": branch, "path": str(path), "base": base, "head": head}


def remove(repo: Path, branch: str, force: bool) -> dict:
    path = worktree_path(repo, branch)
    if not path.exists() and not branch_exists(repo, branch):
        raise Fail(f"worktree 與本機分支都不存在：{branch}")
    if branch_exists(repo, branch) and not force:
        unpushed = git(repo, "rev-list", f"refs/heads/{branch}", "--not", "--remotes")
        if unpushed:
            n = len(unpushed.splitlines())
            raise Fail(f"分支 {branch} 有 {n} 個 commit 還沒推上遠端；確定要丟掉就加 --force")
    removed_path = False
    if path.exists():
        git(repo, "worktree", "remove", *(["--force"] if force else []), str(path))
        removed_path = True
    git(repo, "worktree", "prune")
    removed_branch = False
    if branch_exists(repo, branch):
        git(repo, "branch", "-D", branch)
        removed_branch = True
    return {"ok": True, "action": "remove", "branch": branch, "path": str(path),
            "removed_worktree": removed_path, "removed_branch": removed_branch}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="開／收 worktree/branch/<分支名>")
    p.add_argument("action", choices=["add", "remove"])
    p.add_argument("branch")
    p.add_argument("--repo", help="主 repo 根目錄；不給就從這支腳本的位置推")
    p.add_argument("--base", default="origin/main", help="add 的起點，預設 origin/main")
    p.add_argument("--force", action="store_true", help="remove 時丟掉未推的 commit 與未提交的改動")
    a = p.parse_args(argv)
    try:
        repo = main_repo(Path(a.repo) if a.repo else Path(__file__).resolve().parent)
        out = add(repo, a.branch, a.base) if a.action == "add" else remove(repo, a.branch, a.force)
    except Fail as e:
        print(json.dumps({"ok": False, "action": a.action, "branch": a.branch, "error": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
