"""PR merge 之後的收尾：確認已 merge → 主 repo pull → 移除 worktree 與本機分支 → 刪慣例暫存目錄。

用法：
  python3 script/workflow/after_merge.py <pr> [--repo <主 repo>] [--scratch <scratchpad 根>] [--item <父題>-<no> ...]

1. 唯讀的 gh pr view <pr> --json state,headRefName,mergedAt 確認已 merge；沒 merge 就以 1 結束，什麼都不動。
2. 主 repo git pull --ff-only；主 repo 有未提交的改動（未追蹤檔不算）或不在 main 時停下，不 stash、不 checkout。
3. worktree.py 的 remove <headRefName>；worktree 與本機分支都不存在就跳過，算成功。
4. 有給 --scratch 才刪暫存目錄，只刪慣例路徑：<scratch>/pr-fix/<pr>/（pr-fix.js），以及每個 --item 的
   <scratch>/pr/<父題>-<no>/（pr.js）。不做萬用刪除。

輸出一行 JSON：{"ok", "pr", "branch", "merged", "pulled", "worktree_removed", "worktree_skipped",
"scratch_removed", "error"}；pulled 是 pull 後主 repo 的 HEAD。結束碼：成功 0；沒 merge 或任何一步失敗 1。
不執行 gh pr merge 或任何 GitHub 寫入：寫入動作留在呼叫端，hook 才看得到。
gh 的位置可用環境變數 AFTER_MERGE_GH 換掉（測試用）。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worktree  # noqa: E402

Fail = worktree.Fail
git = worktree.git

ITEM = re.compile(r"^[1-9][0-9]*-[A-Za-z0-9_.-]+$")


def pr_info(pr: int) -> dict:
    gh = os.environ.get("AFTER_MERGE_GH", "gh")
    r = subprocess.run([gh, "pr", "view", str(pr), "-R", "ycpss91255-research/vendor_kit",
                        "--json", "state,headRefName,mergedAt"], capture_output=True, text=True)
    if r.returncode != 0:
        raise Fail(f"gh pr view {pr} 失敗：{(r.stderr or r.stdout).strip()}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise Fail(f"gh pr view {pr} 的輸出不是 JSON：{e}")


def pull(repo: Path) -> str:
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        raise Fail(f"主 repo 不在 main（目前是 {branch}），不 checkout，先自己切回 main")
    dirty = git(repo, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise Fail(f"主 repo 有未提交的改動，不 stash，先自己處理：\n{dirty}")
    git(repo, "pull", "--ff-only")
    return git(repo, "rev-parse", "HEAD")


def scratch_dirs(scratch: Path, pr: int, items: list) -> list:
    """回傳要刪的慣例暫存目錄（不檢查是否存在）。item 照 pr.js 的規則換掉 / 空白 :。"""
    dirs = [scratch / "pr-fix" / str(pr)]
    for it in items:
        tag = re.sub(r"[/\s:]+", "_", it.strip())
        if not ITEM.match(tag) or ".." in tag:
            raise Fail(f"--item 要是 <父題>-<no>：{it!r}")
        dirs.append(scratch / "pr" / tag)
    return dirs


def remove_scratch(dirs: list) -> list:
    removed = []
    for d in dirs:
        if d.is_symlink():
            raise Fail(f"暫存目錄是符號連結，不刪：{d}")
        if d.is_dir():
            shutil.rmtree(d)
            removed.append(str(d))
    return removed


def run(a) -> dict:
    out = {"ok": False, "pr": a.pr, "branch": None, "merged": False, "pulled": None,
           "worktree_removed": False, "worktree_skipped": False, "scratch_removed": [], "error": None}
    try:
        info = pr_info(a.pr)
        out["branch"] = info.get("headRefName")
        out["merged"] = info.get("state") == "MERGED" and bool(info.get("mergedAt"))
        if not out["merged"]:
            raise Fail(f"PR #{a.pr} 還沒 merge（state={info.get('state')}），什麼都不動")
        if not out["branch"]:
            raise Fail(f"PR #{a.pr} 沒有 headRefName")
        scratch = None
        if a.scratch:
            scratch = Path(a.scratch)
            if not scratch.is_dir():
                raise Fail(f"--scratch 不是目錄：{scratch}")
            dirs = scratch_dirs(scratch, a.pr, a.item)  # 先檢查 --item，不合法就什麼都不動
        repo = worktree.main_repo(Path(a.repo) if a.repo else Path(__file__).resolve().parent)
        out["pulled"] = pull(repo)
        branch = out["branch"]
        if worktree.worktree_path(repo, branch).exists() or worktree.branch_exists(repo, branch):
            r = worktree.remove(repo, branch, False)
            out["worktree_removed"] = r["removed_worktree"] or r["removed_branch"]
        else:
            out["worktree_skipped"] = True
        if scratch is not None:
            out["scratch_removed"] = remove_scratch(dirs)
        out["ok"] = True
    except Fail as e:
        out["error"] = str(e)
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="PR merge 後的收尾：pull、移除 worktree、刪暫存目錄")
    p.add_argument("pr", type=int)
    p.add_argument("--repo", help="主 repo 根目錄；不給就從這支腳本的位置推")
    p.add_argument("--scratch", help="scratchpad 根目錄；給了才刪 pr-fix/<pr>/ 與 --item 的 pr/<父題>-<no>/")
    p.add_argument("--item", action="append", default=[], help="pr workflow 的 <父題>-<no>，可重複")
    a = p.parse_args(argv)
    out = run(a)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
