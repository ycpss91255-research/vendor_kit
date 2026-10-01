"""找出已開 PR 的修改目標：分支、worktree、issue 編號，並把 worktree 準備到「乾淨且在 PR 分支最新」。

用法：python3 script/workflow/pr_target.py <pr> [--repo <主 repo>] [--gh-repo ycpss91255-research/vendor_kit]

1. `gh pr view <pr> --json number,state,headRefName,body,url` 取分支與本文（唯讀）。PR 不是 OPEN 就報錯。
2. issue：PR 本文裡第一個 `Closes #N`／`Refs #N`（也認 `Refs: #N`、Fixes、Resolves，大小寫不拘）。找不到就報錯。
3. worktree：位置跟 worktree.py 相同（主 repo 上一層的 worktree/branch/<分支>）。git fetch origin 後，
   不存在就從 origin/<分支> 建（本機分支已存在就直接掛上）；存在就沿用。
4. 檢查：worktree 所在分支要是 PR 分支、沒有未提交或未追蹤的改動、沒有還沒推的 commit；
   落後 origin/<分支> 就 fast-forward，跟遠端分岔就報錯。
5. 並行：pr-fix 一次修多個 PR 時，幾支 pr_target.py 會同時對同一個主 repo 跑 fetch 與 worktree add，
   git 的 ref 鎖會讓其中一支失敗。所以動到主 repo 的這兩步用檔案鎖（git common dir 的 pr_target.lock）排隊，
   其餘在各自 worktree 裡的檢查不鎖。

輸出一行 JSON：成功 {"ok": true, "pr", "branch", "issue", "repo", "path", "url", "created", "head",
"fast_forwarded", "behind_main"}（repo 是主 worktree 根目錄）；失敗 {"ok": false, "pr", "error"}，結束碼 1。只做本機的 git 動作與唯讀的 gh 查詢，不 push。
gh 的位置可用環境變數 PR_TARGET_GH 換掉（測試用）。
"""
import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worktree import Fail, branch_exists, git, main_repo, worktree_path  # noqa: E402

REPO = "ycpss91255-research/vendor_kit"
ISSUE_REF = re.compile(r"\b(?:closes|closed|close|fixes|fixed|fix|resolves|resolved|resolve|refs)\b:?\s+#(\d+)",
                       re.IGNORECASE)


def pr_info(pr: str, gh_repo: str) -> dict:
    gh = os.environ.get("PR_TARGET_GH", "gh")
    r = subprocess.run([gh, "pr", "view", str(pr), "-R", gh_repo, "--json", "number,state,headRefName,body,url"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Fail(f"gh pr view 失敗（{r.returncode}）：{(r.stderr or r.stdout).strip()}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise Fail(f"gh pr view 的輸出不是 JSON：{e}")


def first_issue(body: str):
    m = ISSUE_REF.search(body or "")
    return int(m.group(1)) if m else None


@contextmanager
def repo_lock(repo: Path):
    """主 repo 的排他鎖：同時跑的幾支 pr_target.py 依序做 fetch 與 worktree add。"""
    common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    with open(common / "pr_target.lock", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def prepare(repo: Path, branch: str) -> dict:
    path = worktree_path(repo, branch)
    remote = f"origin/{branch}"
    created = False
    with repo_lock(repo):
        git(repo, "fetch", "origin")
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", remote],
                          capture_output=True).returncode != 0:
            raise Fail(f"遠端沒有分支 {remote}")
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            if branch_exists(repo, branch):
                git(repo, "worktree", "add", str(path), branch)
            else:
                git(repo, "worktree", "add", "--track", "-b", branch, str(path), remote)
            created = True
    current = git(path, "rev-parse", "--abbrev-ref", "HEAD")
    if current != branch:
        raise Fail(f"worktree {path} 在分支 {current}，不是 PR 分支 {branch}")
    dirty = git(path, "status", "--porcelain")
    if dirty:
        raise Fail(f"worktree 有未提交或未追蹤的改動：{dirty.splitlines()[:5]}")
    ahead = git(path, "rev-list", "--count", f"{remote}..HEAD")
    behind = git(path, "rev-list", "--count", f"HEAD..{remote}")
    if int(ahead) and int(behind):
        raise Fail(f"本機分支跟 {remote} 分岔（本機多 {ahead}、遠端多 {behind}），要人看過再處理")
    if int(ahead):
        raise Fail(f"本機分支有 {ahead} 個 commit 還沒推上 {remote}")
    ff = False
    if int(behind):
        git(path, "merge", "--ff-only", remote)
        ff = True
    behind_main = None
    if subprocess.run(["git", "-C", str(path), "rev-parse", "--verify", "--quiet", "origin/main"],
                      capture_output=True).returncode == 0:
        behind_main = int(git(path, "rev-list", "--count", "HEAD..origin/main"))
    return {"path": str(path), "created": created, "head": git(path, "rev-parse", "HEAD"),
            "fast_forwarded": ff, "behind_main": behind_main}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="找出已開 PR 的分支、worktree 與 issue，並把 worktree 準備好")
    p.add_argument("pr")
    p.add_argument("--repo", help="主 repo 根目錄；不給就從這支腳本的位置推")
    p.add_argument("--gh-repo", default=REPO)
    a = p.parse_args(argv)
    try:
        if not a.pr.isdigit():
            raise Fail(f"PR 編號要是數字：{a.pr!r}")
        info = pr_info(a.pr, a.gh_repo)
        if info.get("state") != "OPEN":
            raise Fail(f"PR #{a.pr} 的狀態是 {info.get('state')}，不是 OPEN")
        branch = info.get("headRefName") or ""
        issue = first_issue(info.get("body", ""))
        if issue is None:
            raise Fail(f"PR #{a.pr} 的本文找不到 Closes／Refs #N")
        repo = main_repo(Path(a.repo) if a.repo else Path(__file__).resolve().parent)
        out = {"ok": True, "pr": int(a.pr), "branch": branch, "issue": issue, "repo": str(repo),
               "url": info.get("url"),
               **prepare(repo, branch)}
    except Fail as e:
        print(json.dumps({"ok": False, "pr": a.pr, "error": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
