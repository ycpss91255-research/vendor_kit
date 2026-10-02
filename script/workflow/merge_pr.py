"""PR 等 CI、merge、收尾一次做完：記下 head → 等 CI → 查 mergeable、head 與署名 → gh pr merge --merge → 主 repo pull
→ 移除 worktree 與本機分支 → 刪慣例暫存目錄。

用法：
  python3 script/workflow/merge_pr.py <pr> [--no-merge] [--repo <主 repo>] [--scratch <scratchpad 根>] [--item <父題>-<no> ...]

1. 先唯讀 gh pr view <pr> --json headRefOid 記下 head sha（取不到就以 1 結束），再跑同目錄的 wait_ci.py <pr>；
   不是全部必過檢查都 SUCCESS（失敗或逾時）就以 1 結束，不 merge。
2. gh pr view <pr> --json mergeable,headRefOid,...：UNKNOWN 時每 5 秒重查，最多 6 次；CONFLICTING 就以 1 結束，要先 rebase。
   PR 不是 OPEN 也停下（已經 merge 過就改用 --no-merge）。headRefOid 跟步驟 1 記下的不同（等 CI 的期間有新 push，
   CI 跑過的不是現在的 head）就以 1 結束，不 merge。
3. PR 標題與本文經 hook_rules.BANNED（attribution_guard.py 的規則）確認沒有 Claude 署名，
   再經 hook_rules.guarded_run 跑 gh pr merge <pr> -R ycpss91255-research/vendor_kit --merge --match-head-commit <sha>
   （只用 merge，不 squash、不 rebase；GitHub 端也確認 head 沒變）。被 hook 擋就不執行，以 1 結束。
4. 確認已 merge（state=MERGED 且有 mergedAt），主 repo git pull --ff-only；主 repo 有未提交的改動
   （未追蹤檔不算）或不在 main 時停下，不 stash、不 checkout。要 merge 時這項在步驟 1 之前就先查，不過就不 merge。
5. worktree.py 的 remove <headRefName>；worktree 與本機分支都不存在就跳過，算成功。
6. 有給 --scratch 才刪暫存目錄，只刪慣例路徑：<scratch>/pr-fix/<pr>/（pr-fix.js），以及每個 --item 的
   <scratch>/pr/<父題>-<no>/（pr.js）。不做萬用刪除。
--no-merge：PR 已經 merge 過時用，跳過 1–3，只做 4–6（沒 merge 就以 1 結束，什麼都不動）。

輸出一行 JSON：{"ok", "pr", "branch", "head", "ci", "mergeable", "merge", "merged", "pulled", "worktree_removed",
"worktree_skipped", "scratch_removed", "denied", "error"}；head 是步驟 1 記下的 sha（--no-merge 時 null），
ci 是 wait_ci.py 輸出的 JSON（--no-merge 時 null），mergeable 是最後查到的值，merge 是這次有沒有執行 gh pr merge，
pulled 是 pull 後主 repo 的 HEAD，denied 是 hook 擋下 gh pr merge 時 precheck 的 denied 與 errors（沒擋時空陣列）。
結束碼：成功 0；任何一步失敗 1，失敗的那一步之後都不做。
gh 的位置可用環境變數 MERGE_PR_GH（gh pr merge 經 guarded_run 的 bin_env 換，hook 仍檢查字面的 gh）、wait_ci 可用 MERGE_PR_WAIT_CI（可執行檔）換掉（測試用）。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hook_rules  # noqa: E402
import worktree  # noqa: E402

Fail = worktree.Fail
git = worktree.git


class CiFail(Fail):
    """CI 沒有全過；res 是 wait_ci.py 的 JSON。"""

    def __init__(self, res, msg):
        super().__init__(msg)
        self.res = res

ITEM = re.compile(r"^[1-9][0-9]*-[A-Za-z0-9_.-]+$")
REPO = "ycpss91255-research/vendor_kit"
WAIT_CI = Path(__file__).resolve().parent / "wait_ci.py"
UNKNOWN_RETRIES = 6
UNKNOWN_INTERVAL = 5


def gh(*args) -> subprocess.CompletedProcess:
    return subprocess.run([os.environ.get("MERGE_PR_GH", "gh"), *args], capture_output=True, text=True)


def pr_info(pr: int, fields: str = "state,headRefName,mergedAt") -> dict:
    r = gh("pr", "view", str(pr), "-R", REPO, "--json", fields)
    if r.returncode != 0:
        raise Fail(f"gh pr view {pr} 失敗：{(r.stderr or r.stdout).strip()}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise Fail(f"gh pr view {pr} 的輸出不是 JSON：{e}")


def wait_ci(pr: int) -> dict:
    """跑 wait_ci.py；全部通過回傳它的 JSON，否則 raise Fail（訊息含失敗或逾時）。"""
    exe = os.environ.get("MERGE_PR_WAIT_CI")
    cmd = [exe, str(pr)] if exe else [sys.executable, str(WAIT_CI), str(pr), "--repo", REPO]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        res = {"error": (r.stderr or r.stdout).strip()}
    res["code"] = r.returncode
    if r.returncode != 0 or not res.get("all_pass"):
        why = {1: "有檢查失敗", 2: "等 CI 逾時"}.get(r.returncode, f"wait_ci 出錯：{res.get('error')}")
        raise CiFail(res, f"PR #{pr} 的 CI 沒有全過（{why}），不 merge")
    return res


def check_mergeable(pr: int, sleep=None) -> dict:
    """查 mergeable；UNKNOWN 時每 UNKNOWN_INTERVAL 秒重查，最多 UNKNOWN_RETRIES 次。回傳最後一次的 gh pr view。"""
    fields = "state,headRefName,headRefOid,mergedAt,mergeable,title,body"
    info = pr_info(pr, fields)
    for _ in range(UNKNOWN_RETRIES):
        if info.get("mergeable") != "UNKNOWN":
            break
        (sleep or time.sleep)(UNKNOWN_INTERVAL)
        info = pr_info(pr, fields)
    return info


def attribution_problem(info: dict):
    """PR 標題或本文含 Claude 署名就回傳說明，否則 None。規則是 attribution_guard.py 的 BANNED。"""
    hits = [k for k in ("title", "body") if hook_rules.BANNED.search(info.get(k) or "")]
    if hits:
        return f"PR 的{'、'.join('標題' if k == 'title' else '本文' for k in hits)}含 Claude 署名或 session 連結，先拿掉再 merge"
    return None


def merge(pr: int, out: dict, cwd: Path, sleep=None) -> dict:
    """記下 head → 等 CI → 查 mergeable、head 與署名 → guarded_run 的 gh pr merge --merge --match-head-commit。

    回傳 merge 後的 gh pr view。cwd 是 hook 檢查與執行 gh 的目錄。
    """
    head = pr_info(pr, "state,headRefOid").get("headRefOid")
    if not head:
        raise Fail(f"PR #{pr} 取不到 headRefOid，不 merge")
    out["head"] = head
    out["ci"] = wait_ci(pr)
    info = check_mergeable(pr, sleep)
    out["mergeable"] = info.get("mergeable")
    out["branch"] = info.get("headRefName")
    if info.get("state") == "MERGED":
        raise Fail(f"PR #{pr} 已經 merge 過，收尾改用 --no-merge")
    if info.get("state") != "OPEN":
        raise Fail(f"PR #{pr} 不是 OPEN（state={info.get('state')}），不 merge")
    if out["mergeable"] == "CONFLICTING":
        raise Fail(f"PR #{pr} 跟 main 衝突（mergeable=CONFLICTING），先 rebase origin/main、push 後再跑")
    if out["mergeable"] != "MERGEABLE":
        raise Fail(f"PR #{pr} 的 mergeable 是 {out['mergeable']}（重查 {UNKNOWN_RETRIES} 次後），不 merge")
    now = info.get("headRefOid")
    if now != head:
        raise Fail(f"PR #{pr} 的 head 在等 CI 的期間變了（{head} → {now}），CI 跑過的不是現在的 head，不 merge；"
                   "重跑一次等新的 CI")
    problem = attribution_problem(info)
    if problem:
        raise Fail(problem)
    run = hook_rules.guarded_run(["gh", "pr", "merge", str(pr), "-R", REPO, "--merge", "--match-head-commit", head],
                                 cwd, bin_env="MERGE_PR_GH")
    if not run["ok"]:
        check = run.get("precheck") or {}
        out["denied"] = list(check.get("denied") or []) + list(check.get("errors") or [])
        if run.get("ran"):
            raise Fail(f"gh pr merge {pr} 失敗：{(run['stderr'] or run['stdout']).strip()}")
        raise Fail(run.get("error") or f"hook 擋下 gh pr merge {pr}，不 merge")
    out["merge"] = True
    return pr_info(pr)


def check_repo(repo: Path) -> None:
    """主 repo 要在 main、沒有未提交的改動（未追蹤檔不算），否則 raise Fail。"""
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        raise Fail(f"主 repo 不在 main（目前是 {branch}），不 checkout，先自己切回 main")
    dirty = git(repo, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise Fail(f"主 repo 有未提交的改動，不 stash，先自己處理：\n{dirty}")


def pull(repo: Path) -> str:
    check_repo(repo)
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


def run(a, sleep=None) -> dict:
    out = {"ok": False, "pr": a.pr, "branch": None, "head": None, "ci": None, "mergeable": None, "merge": False,
           "merged": False, "pulled": None,
           "worktree_removed": False, "worktree_skipped": False, "scratch_removed": [], "denied": [], "error": None}
    try:
        scratch = None
        if a.scratch:
            scratch = Path(a.scratch)
            if not scratch.is_dir():
                raise Fail(f"--scratch 不是目錄：{scratch}")
            dirs = scratch_dirs(scratch, a.pr, a.item)  # 先檢查 --item，不合法就什麼都不動
        repo = worktree.main_repo(Path(a.repo) if a.repo else Path(__file__).resolve().parent)
        if not a.no_merge:
            check_repo(repo)  # merge 前先確認收尾做得了，免得 merge 了卻卡在 pull
        info = pr_info(a.pr) if a.no_merge else merge(a.pr, out, repo, sleep)
        out["branch"] = info.get("headRefName")
        out["merged"] = info.get("state") == "MERGED" and bool(info.get("mergedAt"))
        if not out["merged"]:
            raise Fail(f"PR #{a.pr} 還沒 merge（state={info.get('state')}），什麼都不動")
        if not out["branch"]:
            raise Fail(f"PR #{a.pr} 沒有 headRefName")
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
        if isinstance(e, CiFail):
            out["ci"] = e.res
        out["error"] = str(e)
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="等 CI、merge PR，再收尾：pull、移除 worktree、刪暫存目錄")
    p.add_argument("pr", type=int)
    p.add_argument("--no-merge", action="store_true", help="PR 已經 merge 過：不等 CI、不 merge，只收尾")
    p.add_argument("--repo", help="主 repo 根目錄；不給就從這支腳本的位置推")
    p.add_argument("--scratch", help="scratchpad 根目錄；給了才刪 pr-fix/<pr>/ 與 --item 的 pr/<父題>-<no>/")
    p.add_argument("--item", action="append", default=[], help="pr workflow 的 <父題>-<no>，可重複")
    a = p.parse_args(argv)
    out = run(a)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
