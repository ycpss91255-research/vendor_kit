#!/usr/bin/env python3
"""把自己的分支 rebase 到 origin/main，再用 --force-with-lease 推回自己的分支（給 pr、pr-fix workflow 用）。

取代 workflow 裡照文字做的「git fetch → git rebase origin/main → git push --force-with-lease」。
解衝突要判斷，留給子代理：腳本碰到衝突就停在 rebase 中途、列出衝突檔；子代理解完、git add 後
用 --continue 接著做。push 經 script/workflow/hook_rules.py 的 guarded_run，把即將執行的同一個
argv 交給 .claude/settings.json 註冊的 Bash hook（guard.py 不准推 main），被擋就不執行。

用法：
  python3 script/git/rebase_push.py --repo <worktree> --branch <分支> [--onto origin/main]
                                    [--continue | --abort] [--no-push]

開始（沒給 --continue／--abort）：
  1. --branch 不是 main；--repo 是 git worktree 的根目錄；目前分支等於 --branch；沒有進行中的 rebase；
     git status --porcelain 是空的。
  2. git fetch origin；記下 origin/<分支> 的 sha 當 lease（遠端還沒有這個分支就記成空，push 時要求遠端
     仍然沒有）；lease 與開始時的 HEAD 寫進 git dir 的 rebase_push.lease。
  3. HEAD 已經包含 --onto（merge-base 等於 --onto）：state up_to_date，不 rebase、不 push。
  4. 否則 git rebase <onto>。衝突時不 abort：state conflict，conflicts 列出未合併的檔
     （git diff --name-only --diff-filter=U），結束碼 3。
  5. rebase 完成：state rebased，接著 push（--no-push 時跳過）。
--continue：要有進行中的 rebase 與 rebase_push.lease，而且 rebase 的分支等於 --branch；還有未合併的檔就
  再回 conflict（結束碼 3）；否則 git -c core.editor=true rebase --continue（環境 GIT_EDITOR=true），
  又碰到衝突同樣回 3，做完就 state rebased 並 push。
--abort：git rebase --abort，刪掉 rebase_push.lease，state aborted。
push：guarded_run(["git", "push", "--force-with-lease=<分支>:<lease>", "origin", <分支>], cwd=<repo>)，
  lease 一律用開始時記下的 sha（--continue 時從 rebase_push.lease 讀）；push 之後刪掉 rebase_push.lease。
  不用 git -C <repo>：guard.py 只認得字面的 `git push`，中間夾 -C 就看不出是 push、擋不到推 main。

輸出一行 JSON（ensure_ascii=False）：
  {"ok", "state", "branch", "before", "after", "pushed", "conflicts", "denied", "error"}
  state：up_to_date、rebased、conflict、aborted；還沒走到這些狀態就失敗時是 null。
  before：開始時分支的 HEAD sha；after：目前的 HEAD sha（rebase 完成後是新的 sha）。
  pushed：有沒有 push 成功。conflicts：未合併的檔。denied：hook 擋下的 [{"hook", "decision", "reason"}]。
  error：失敗說明（成功與 conflict 是 null）。
結束碼：成功 0；檢查、hook 或 git 失敗 1；用法錯 2；衝突 3。
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "workflow"))
import hook_rules  # noqa: E402

LEASE_FILE = "rebase_push.lease"


class Fail(Exception):
    def __init__(self, error, **extra):
        super().__init__(error)
        self.error = error
        self.extra = extra


class Usage(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Usage(message)


def parser() -> Parser:
    ap = Parser(description="rebase 到 origin/main 後 force-with-lease 推自己的分支")
    ap.add_argument("--repo", required=True, help="worktree 根目錄")
    ap.add_argument("--branch", required=True, help="自己的分支（不能是 main）")
    ap.add_argument("--onto", default="origin/main", help="rebase 的目標（預設 origin/main）")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--continue", dest="cont", action="store_true", help="解完衝突、git add 後接著做")
    group.add_argument("--abort", action="store_true", help="放棄這次 rebase")
    ap.add_argument("--no-push", action="store_true", help="只 rebase，不 push")
    return ap


def run_git(repo: Path, *args: str, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env)


def git(repo: Path, *args: str) -> str:
    r = run_git(repo, *args)
    if r.returncode != 0:
        raise Fail(f"git {' '.join(args)} 失敗：{(r.stderr or r.stdout).strip()}")
    return r.stdout


def head(repo: Path) -> str:
    return git(repo, "rev-parse", "HEAD").strip()


def git_path(repo: Path, name: str) -> Path:
    p = Path(git(repo, "rev-parse", "--git-path", name).strip())
    return p if p.is_absolute() else repo / p


def rebase_dir(repo: Path):
    """進行中的 rebase 的狀態目錄；沒有進行中的 rebase 回 None。"""
    for name in ("rebase-merge", "rebase-apply"):
        p = git_path(repo, name)
        if p.is_dir():
            return p
    return None


def conflicts(repo: Path) -> list[str]:
    return [f for f in git(repo, "diff", "--name-only", "--diff-filter=U", "-z").split("\0") if f]


def check_repo(repo: Path, branch: str) -> None:
    if branch == "main":
        raise Fail("--branch 不能是 main：只准 rebase、push 自己的分支，進 main 只能走 merge")
    if not repo.is_dir():
        raise Fail(f"--repo 不是目錄：{repo}")
    top = git(repo, "rev-parse", "--show-toplevel").strip()
    if Path(top).resolve() != repo.resolve():
        raise Fail(f"--repo 不是 git worktree 的根目錄（根目錄是 {top}）")


def check_rebasing_branch(rdir: Path, branch: str) -> None:
    head_name = rdir / "head-name"
    name = head_name.read_text(encoding="utf-8").strip() if head_name.is_file() else ""
    if name != f"refs/heads/{branch}":
        raise Fail(f"進行中的 rebase 是 {name or '（不明）'}，不是 --branch 給的 {branch}")


def read_lease(repo: Path, branch: str) -> dict:
    path = git_path(repo, LEASE_FILE)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Fail(f"讀不到 {LEASE_FILE}（要先跑一次不帶 --continue 的 rebase_push.py）：{e}")
    if data.get("branch") != branch:
        raise Fail(f"{LEASE_FILE} 記的分支是 {data.get('branch')}，不是 --branch 給的 {branch}")
    return data


def write_lease(repo: Path, data: dict) -> None:
    git_path(repo, LEASE_FILE).write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")


def drop_lease(repo: Path) -> None:
    try:
        git_path(repo, LEASE_FILE).unlink()
    except (FileNotFoundError, Fail):
        pass


def push(repo: Path, branch: str, lease: str, settings=None, project_dir=None) -> None:
    # 不用 git -C：guard.py 的 check_git 只認得字面的 `git push`，-C 夾在中間就看不出是 push，
    # 所以改成 cwd＝repo，讓 hook 看到的就是 `git push …`。
    argv = ["git", "push", f"--force-with-lease={branch}:{lease}", "origin", branch]
    r = hook_rules.guarded_run(argv, repo, settings=settings, project_dir=project_dir)
    if r["ok"]:
        return
    check = r.get("precheck") or {}
    if not r.get("ran"):
        if check.get("denied"):
            raise Fail("hook 擋下 push", denied=check["denied"])
        if check.get("errors"):
            msgs = "；".join(f"{e.get('hook')}：{e.get('error')}" for e in check["errors"])
            raise Fail(f"hook 檢查出錯，不執行 push：{msgs}")
        raise Fail(r.get("error") or "沒有執行 push")
    raise Fail(f"git push 失敗（結束碼 {r['returncode']}）：{(r['stderr'] or r['stdout']).strip()}")


def start(repo: Path, args, out: dict) -> str:
    """回傳 state：up_to_date、rebased 或 conflict。"""
    r = run_git(repo, "symbolic-ref", "--short", "-q", "HEAD")
    current = r.stdout.strip() if r.returncode == 0 else ""
    if rebase_dir(repo):
        raise Fail("已經有進行中的 rebase：解完衝突用 --continue，要放棄用 --abort")
    if current != args.branch:
        raise Fail(f"目前分支是 {current or '（detached HEAD）'}，不是 --branch 給的 {args.branch}")
    if git(repo, "status", "--porcelain").strip():
        raise Fail("worktree 不乾淨：先 commit 或清掉改動再 rebase")
    out["before"] = out["after"] = head(repo)
    git(repo, "fetch", "origin")
    r = run_git(repo, "rev-parse", "--verify", "-q", f"refs/remotes/origin/{args.branch}^{{commit}}")
    lease = r.stdout.strip() if r.returncode == 0 else ""
    onto = run_git(repo, "rev-parse", "--verify", "-q", f"{args.onto}^{{commit}}")
    if onto.returncode != 0:
        raise Fail(f"找不到 --onto：{args.onto}")
    if git(repo, "merge-base", "HEAD", onto.stdout.strip()).strip() == onto.stdout.strip():
        return "up_to_date"
    write_lease(repo, {"branch": args.branch, "lease": lease, "before": out["before"]})
    r = run_git(repo, "rebase", args.onto)
    out["after"] = head(repo)
    if r.returncode != 0:
        files = conflicts(repo) if rebase_dir(repo) else []
        if files:
            out["conflicts"] = files
            return "conflict"
        drop_lease(repo)
        if rebase_dir(repo):
            run_git(repo, "rebase", "--abort")
        raise Fail(f"git rebase {args.onto} 失敗：{(r.stderr or r.stdout).strip()}")
    return "rebased"


def resume(repo: Path, args, out: dict) -> str:
    """--continue：回傳 rebased 或 conflict。"""
    rdir = rebase_dir(repo)
    if not rdir:
        raise Fail("沒有進行中的 rebase，不能 --continue")
    check_rebasing_branch(rdir, args.branch)
    data = read_lease(repo, args.branch)
    out["before"] = data.get("before")
    out["after"] = head(repo)
    files = conflicts(repo)
    if files:
        out["conflicts"] = files
        return "conflict"
    env = dict(os.environ, GIT_EDITOR="true")
    r = run_git(repo, "-c", "core.editor=true", "rebase", "--continue", env=env)
    out["after"] = head(repo)
    if r.returncode != 0:
        files = conflicts(repo) if rebase_dir(repo) else []
        if files:
            out["conflicts"] = files
            return "conflict"
        raise Fail(f"git rebase --continue 失敗：{(r.stderr or r.stdout).strip()}")
    return "rebased"


def abort(repo: Path, args, out: dict) -> str:
    rdir = rebase_dir(repo)
    if not rdir:
        raise Fail("沒有進行中的 rebase，不能 --abort")
    check_rebasing_branch(rdir, args.branch)
    git(repo, "rebase", "--abort")
    drop_lease(repo)
    out["after"] = head(repo)
    return "aborted"


def run(argv=None, *, settings=None, project_dir=None) -> tuple[int, dict]:
    out = {"ok": False, "state": None, "branch": None, "before": None, "after": None,
           "pushed": False, "conflicts": [], "denied": [], "error": None}
    try:
        args = parser().parse_args(argv)
    except Usage as e:
        out["error"] = f"用法錯：{e}"
        return 2, out
    repo = Path(args.repo)
    out["branch"] = args.branch
    try:
        check_repo(repo, args.branch)
        if args.abort:
            out["state"] = abort(repo, args, out)
        else:
            state = resume(repo, args, out) if args.cont else start(repo, args, out)
            if state == "conflict":
                out["state"] = state
                return 3, out
            out["state"] = state
            if state == "rebased" and not args.no_push:
                lease = read_lease(repo, args.branch)["lease"]
                try:
                    push(repo, args.branch, lease, settings=settings, project_dir=project_dir)
                finally:
                    drop_lease(repo)
                out["pushed"] = True
            else:
                drop_lease(repo)
    except Fail as e:
        out["error"] = e.error
        out["denied"] = e.extra.get("denied", [])
        return 1, out
    out["ok"] = True
    return 0, out


def main(argv=None) -> int:
    code, out = run(argv)
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
