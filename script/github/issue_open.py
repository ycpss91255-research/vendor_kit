"""開 issue 並掛成 sub-issue：本文自檢 → gh issue create → 查 id → POST sub_issues。

寫入（gh issue create、POST sub_issues）一律經 script/workflow/hook_rules.py 的 guarded_run：
把即將執行的同一個 argv 交給 .claude/settings.json 註冊的每支 Bash hook 檢查，被擋就不執行。
唯一不經 hook 的是唯讀的 `gh api repos/<repo>/issues/<N> --jq .id`（取 sub-issue 要的 database id）。

用法（在 repo 裡任一目錄）：
  python3 script/github/issue_open.py create (--title <標題> | --title-file <檔>) --label <標籤> \
      --body-file <檔> [--parent <N>] [--keep-body]
  python3 script/github/issue_open.py attach --parent <P> --issue <N>

create：
  1. 自檢（step check）：有 --parent 用 script/workflow/body.py 的 problems(kind="issue", parent=N)
     （第一行要是 `Part of #N`、不含本機絕對路徑）；沒有 --parent 只查本機絕對路徑
     （hook_rules.local_path_problem，raw_ok=False）。有問題就停，不寫入。
  2. 開 issue（step create）：guarded_run 跑
     gh issue create -R <repo> --title T --label L --body-file <本文檔的絕對路徑>，從輸出的網址取編號。
  3. 有 --parent（step attach）：唯讀查 id，再 guarded_run 跑
     gh api -X POST repos/<repo>/issues/<P>/sub_issues -F sub_issue_id=<id>。
  issue 開成功就刪掉本文檔（之後重試只需要 attach，不再用本文），--keep-body 保留；開之前失敗不刪。
attach：只做第 3 步，給 create 開了 issue 但掛失敗時重試。

測試用環境變數 ISSUE_OPEN_GH 把 gh 換成假程式（hook 檢查仍用字面的 gh）。

輸出一行 JSON（ensure_ascii=False）：
  {"ok", "step", "issue", "url", "parent", "attached", "sub_issue_id", "problems", "denied", "error"}
  step：停下或完成的步驟（check／create／attach／done）；problems：自檢的問題；
  denied：hook 擋下或出錯的明細（precheck 的 denied 加 errors）；error：其他錯誤說明。
結束碼：0 成功；1 自檢不過、hook 擋下或 gh issue create 失敗（什麼都沒寫）；2 用法錯；
  3 issue 已開（或 attach 指定的 issue）但掛 sub-issue 失敗，JSON 帶 issue 編號，
  呼叫端用 attach 重試，不要再 create。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "workflow"))
import body  # noqa: E402
import hook_rules  # noqa: E402

REPO = "ycpss91255-research/vendor_kit"
BIN_ENV = "ISSUE_OPEN_GH"
ISSUE_URL = re.compile(r"/issues/(\d+)\s*$")


class UsageError(Exception):
    """命令列用法錯。"""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def result(**kw) -> dict:
    out = {"ok": False, "step": None, "issue": None, "url": None, "parent": None,
           "attached": False, "sub_issue_id": None, "problems": [], "denied": [], "error": None}
    out.update(kw)
    return out


def denied_of(run: dict) -> list:
    check = run.get("precheck") or {}
    return list(check.get("denied") or []) + list(check.get("errors") or [])


def gh_bin() -> str:
    return os.environ.get(BIN_ENV) or "gh"


def issue_id(number: int) -> tuple[int | None, str | None]:
    """唯讀查 issue 的 database id；回傳 (id, 錯誤說明)。"""
    argv = [gh_bin(), "api", f"repos/{REPO}/issues/{number}", "--jq", ".id"]
    try:
        r = subprocess.run(argv, capture_output=True, text=True)
    except OSError as e:
        return None, f"無法執行 {argv[0]}：{e}"
    if r.returncode != 0:
        return None, f"查 #{number} 的 id 失敗：{r.stderr.strip()}"
    try:
        return int(r.stdout.strip()), None
    except ValueError:
        return None, f"查 #{number} 的 id 回傳看不懂：{r.stdout.strip()[:200]}"


def attach(parent: int, number: int, cwd: Path, out: dict) -> int:
    """把 #number 掛到 #parent 底下；成功回 0，失敗回 3（out 已填好）。"""
    out.update(step="attach", parent=parent, issue=number)
    sid, err = issue_id(number)
    if sid is None:
        out["error"] = err
        return 3
    out["sub_issue_id"] = sid
    run = hook_rules.guarded_run(
        ["gh", "api", "-X", "POST", f"repos/{REPO}/issues/{parent}/sub_issues",
         "-F", f"sub_issue_id={sid}"], cwd, bin_env=BIN_ENV)
    if not run["ok"]:
        out["denied"] = denied_of(run)
        out["error"] = run.get("error") or (
            f"掛 sub-issue 失敗：{run['stderr'].strip()}" if run.get("ran") else "hook 擋下掛 sub-issue")
        return 3
    out.update(ok=True, step="done", attached=True)
    return 0


def read_title(a) -> str:
    if a.title is not None:
        title = a.title
    else:
        try:
            title = Path(a.title_file).read_text(encoding="utf-8")
        except OSError as e:
            raise UsageError(f"讀不到標題檔：{e}") from e
    title = title.strip()
    if not title or "\n" in title:
        raise UsageError("標題要是一行非空字串")
    return title


def self_check(text: str, parent) -> list[str]:
    if parent is not None:
        return body.problems(text, "issue", parent=parent)
    problem = hook_rules.local_path_problem(text, "本文檔", raw_ok=False)
    return [problem] if problem else []


def create(a, cwd: Path, out: dict) -> int:
    title = read_title(a)
    path = Path(a.body_file).resolve()
    out.update(step="check", parent=a.parent)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        out["problems"] = [f"讀不到本文檔：{e}"]
        return 1
    out["problems"] = self_check(text, a.parent)
    if out["problems"]:
        return 1

    out["step"] = "create"
    run = hook_rules.guarded_run(
        ["gh", "issue", "create", "-R", REPO, "--title", title, "--label", a.label,
         "--body-file", str(path)], cwd, bin_env=BIN_ENV)
    if not run["ok"]:
        out["denied"] = denied_of(run)
        out["error"] = run.get("error") or (
            f"gh issue create 失敗：{run['stderr'].strip()}" if run.get("ran") else "hook 擋下 gh issue create")
        return 1
    url = run["stdout"].strip().splitlines()[-1].strip() if run["stdout"].strip() else ""
    m = ISSUE_URL.search(url)
    if not m:
        out["url"] = url or None
        out["error"] = f"gh issue create 成功但輸出裡沒有 issue 網址：{run['stdout'].strip()[:200]}"
        return 1
    out.update(issue=int(m.group(1)), url=url)
    if not a.keep_body:
        path.unlink(missing_ok=True)

    if a.parent is None:
        out.update(ok=True, step="done")
        return 0
    return attach(a.parent, out["issue"], cwd, out)


def parser() -> Parser:
    p = Parser(prog="issue_open.py", description="開 issue 並掛成 sub-issue（寫入經 hook 檢查）")
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=Parser)
    c = sub.add_parser("create")
    t = c.add_mutually_exclusive_group(required=True)
    t.add_argument("--title")
    t.add_argument("--title-file")
    c.add_argument("--label", required=True)
    c.add_argument("--body-file", required=True)
    c.add_argument("--parent", type=int)
    c.add_argument("--keep-body", action="store_true")
    at = sub.add_parser("attach")
    at.add_argument("--parent", type=int, required=True)
    at.add_argument("--issue", type=int, required=True)
    return p


def main(argv=None) -> int:
    out = result()
    cwd = Path.cwd()
    try:
        a = parser().parse_args(argv)
        if a.cmd == "create":
            code = create(a, cwd, out)
        else:
            code = attach(a.parent, a.issue, cwd, out)
    except UsageError as e:
        out["error"] = f"用法錯：{e}"
        code = 2
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
