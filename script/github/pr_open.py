"""開 PR：確認分支已推齊、沒有重複的 PR → 自檢標題、本文與 PR 規則 → gh pr create。

取代 pr workflow 裡「本文寫檔 → body.py check → check_pr_rules.py --git-diff → gh pr create → 刪本文」
逐一下指令。寫入（gh pr create）經 script/workflow/hook_rules.py 的 guarded_run：把即將執行的
同一個 argv 交給 .claude/settings.json 註冊的每支 Bash hook 檢查（pr_rules_guard.py 會用 --head 的
遠端分支取改動檔再查一次範圍），被擋就不執行。唯讀的 git 指令與
`gh pr list -R <repo> --head <分支> --state open --json number,url` 不經 hook。

用法（在 repo 裡任一目錄）：
  python3 script/github/pr_open.py --repo <worktree> --branch <分支> --issue <N> --body-file <檔>
      (--title <標題> | --title-from-commit) [--base main] [--keep-body]

  --repo：要開 PR 的分支所在的 worktree（git 指令與 hook 都在這裡跑）；
  GitHub 上的 repo 固定是 ycpss91255-research/vendor_kit。

步驟：
  1. push：worktree 的 HEAD 要等於 origin/<分支>（不 fetch，只用已有的 ref）；沒 push 或沒推齊就停，
     先 push 再跑。
  2. existing：這個分支已有 open PR 就停，existing 帶那個 PR 的 number 與 url。
  3. check：標題（--title-from-commit 取 HEAD 的 subject）用 script/git/check_commit_msg.py 的
     check_title；本文用 script/workflow/body.py 的 problems(kind="pr", issue=N)（第一行 `[claude] `、
     有一行 `Closes #N`、不含本機絕對路徑）；PR 規則用 script/github/check_pr_rules.py 的 check，
     改動檔取 `git diff --name-only origin/<base>...origin/<分支>`（三點；沒有改動檔也算問題）。問題原樣放 problems，
     有任何一條就停，不寫入。
  4. create：guarded_run 跑
     gh pr create -R <repo> --base <base> --head <分支> --title T --body-file <本文檔的絕對路徑>，
     從輸出的網址取 PR 編號。成功後刪掉本文檔，--keep-body 保留；失敗不刪。

測試用環境變數 PR_OPEN_GH 把 gh 換成假程式（hook 檢查仍用字面的 gh）。

輸出一行 JSON（ensure_ascii=False）：
  {"ok", "step", "pr", "url", "existing", "problems", "denied", "error"}
  step：停下或完成的步驟（push／existing／check／create／done）；existing：已存在的 open PR
  （{"number", "url"}，沒有是 null）；problems：標題、本文、PR 規則的問題；
  denied：hook 擋下或出錯的明細（precheck 的 denied 加 errors）；error：其他錯誤說明。
結束碼：0 成功；1 沒推齊、已有 PR、檢查不過、hook 擋下或 gh 失敗（沒開 PR）；2 用法錯。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("workflow", "git"):
    sys.path.insert(0, str(HERE.parent / sub))
sys.path.insert(0, str(HERE))
import body  # noqa: E402
import check_commit_msg  # noqa: E402
import check_pr_rules  # noqa: E402
import hook_rules  # noqa: E402

REPO = "ycpss91255-research/vendor_kit"
BIN_ENV = "PR_OPEN_GH"
PR_URL = re.compile(r"/pull/(\d+)\s*$")


class UsageError(Exception):
    """命令列用法錯。"""


class StepError(Exception):
    """唯讀的 git／gh 查詢失敗。"""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def result(**kw) -> dict:
    out = {"ok": False, "step": None, "pr": None, "url": None, "existing": None,
           "problems": [], "denied": [], "error": None}
    out.update(kw)
    return out


def denied_of(run: dict) -> list:
    check = run.get("precheck") or {}
    return list(check.get("denied") or []) + list(check.get("errors") or [])


def git(cwd: Path, *args: str) -> str:
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)
    except OSError as e:
        raise StepError(f"無法執行 git：{e}") from e
    if r.returncode != 0:
        raise StepError(f"git {' '.join(args)} 失敗：{r.stderr.strip()}")
    return r.stdout


def remote_head(cwd: Path, branch: str):
    """origin/<branch> 的 commit；ref 不存在回傳 None。"""
    r = subprocess.run(["git", "-C", str(cwd), "rev-parse", "--verify", "--quiet",
                        f"refs/remotes/origin/{branch}^{{commit}}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def open_prs(branch: str, cwd: Path) -> list:
    """唯讀查這個分支的 open PR：[{"number", "url"}, …]。"""
    argv = [os.environ.get(BIN_ENV) or "gh", "pr", "list", "-R", REPO, "--head", branch,
            "--state", "open", "--json", "number,url"]
    try:
        r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    except OSError as e:
        raise StepError(f"無法執行 {argv[0]}：{e}") from e
    if r.returncode != 0:
        raise StepError(f"gh pr list 失敗：{r.stderr.strip()}")
    try:
        data = json.loads(r.stdout or "[]")
    except ValueError as e:
        raise StepError(f"gh pr list 輸出看不懂：{r.stdout.strip()[:200]}") from e
    if not isinstance(data, list):
        raise StepError(f"gh pr list 輸出不是陣列：{r.stdout.strip()[:200]}")
    return data


def run(a, out: dict) -> int:
    cwd = Path(a.repo).resolve()
    if not cwd.is_dir():
        raise UsageError(f"--repo 不是目錄：{a.repo}")
    path = Path(a.body_file).resolve()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise UsageError(f"讀不到本文檔：{e}") from e

    out["step"] = "push"
    head = git(cwd, "rev-parse", "HEAD").strip()
    remote = remote_head(cwd, a.branch)
    if remote is None:
        out["error"] = f"沒有 origin/{a.branch}：分支還沒 push，先 git push -u origin {a.branch}"
        return 1
    if remote != head:
        out["error"] = (f"HEAD（{head[:12]}）不等於 origin/{a.branch}（{remote[:12]}）："
                        f"先 git push origin {a.branch} 推齊")
        return 1

    out["step"] = "existing"
    prs = open_prs(a.branch, cwd)
    if prs:
        pr = prs[0]
        out.update(existing={"number": pr.get("number"), "url": pr.get("url")},
                   pr=pr.get("number"), url=pr.get("url"),
                   error=f"分支 {a.branch} 已有 open PR #{pr.get('number')}，不再開")
        return 1

    out["step"] = "check"
    title = a.title if a.title is not None else git(cwd, "log", "-1", "--format=%s").strip()
    errors, _notes = check_commit_msg.check_title(title)
    problems = [f"標題：{e}" for e in errors]
    problems += body.problems(text, "pr", issue=a.issue)
    files = git(cwd, "diff", "--name-only", f"origin/{a.base}...origin/{a.branch}").splitlines()
    files = [f.strip() for f in files if f.strip()]
    if not files:
        problems.append(f"origin/{a.base}...origin/{a.branch} 沒有改動檔，沒有東西可以開 PR")
    problems += check_pr_rules.check(text, files)["problems"]
    out["problems"] = problems
    if problems:
        return 1

    out["step"] = "create"
    r = hook_rules.guarded_run(
        ["gh", "pr", "create", "-R", REPO, "--base", a.base, "--head", a.branch,
         "--title", title, "--body-file", str(path)], cwd, bin_env=BIN_ENV)
    if not r["ok"]:
        out["denied"] = denied_of(r)
        out["error"] = r.get("error") or (
            f"gh pr create 失敗：{r['stderr'].strip()}" if r.get("ran") else "hook 擋下 gh pr create")
        return 1
    url = r["stdout"].strip().splitlines()[-1].strip() if r["stdout"].strip() else ""
    m = PR_URL.search(url)
    if not m:
        out["url"] = url or None
        out["error"] = f"gh pr create 成功但輸出裡沒有 PR 網址：{r['stdout'].strip()[:200]}"
        return 1
    out.update(ok=True, step="done", pr=int(m.group(1)), url=url)
    if not a.keep_body:
        path.unlink(missing_ok=True)
    return 0


def parser() -> Parser:
    p = Parser(prog="pr_open.py", description="自檢標題、本文與 PR 規則後開 PR（寫入經 hook 檢查）")
    p.add_argument("--repo", required=True, help="分支所在的 worktree")
    p.add_argument("--branch", required=True)
    p.add_argument("--issue", type=int, required=True)
    p.add_argument("--body-file", required=True)
    t = p.add_mutually_exclusive_group(required=True)
    t.add_argument("--title")
    t.add_argument("--title-from-commit", action="store_true")
    p.add_argument("--base", default="main")
    p.add_argument("--keep-body", action="store_true")
    return p


def main(argv=None) -> int:
    out = result()
    try:
        code = run(parser().parse_args(argv), out)
    except UsageError as e:
        out["error"] = f"用法錯：{e}"
        code = 2
    except StepError as e:
        out["error"] = str(e)
        code = 1
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
