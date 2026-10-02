#!/usr/bin/env python3
"""檢查 commit 訊息後 commit，並 push 到自己的分支（給 pr、pr-fix workflow 用）。

取代 workflow 裡照文字做的「寫訊息檔 → git commit -F → git push -u」：訊息先用
check_commit_msg.check_message（import 同目錄的 check_commit_msg.py，不另寫規則）檢查，
commit 與 push 都經 script/workflow/hook_rules.py 的 guarded_run，把即將執行的同一個 argv
交給 .claude/settings.json 註冊的 Bash hook（不准推 main、不准在主目錄 commit、不准署名等），
被擋就不執行。

用法：
  python3 script/git/commit_push.py --repo <worktree> --branch <分支> --message-file <檔> --refs <issue>
                                    (--add <路徑>… | --all) [--no-push]

步驟（任何一步失敗就停，後面都不做）：
  1. repo：--repo 是 git worktree 的根目錄、目前分支等於 --branch、--branch 不是 main、
     git status --porcelain 有改動。
  2. message：--message-file 是標題（可加空行與內文），不含 footer。在最後空一行加 `Refs: #<refs>`
     （訊息檔已經有同一行就不重複加；最後一段已經全是 footer 時加在那一段），寫到
     `<訊息檔>.final`，用 check_message 檢查；有錯誤就停、不 stage。
  3. stage：git add -- <--add 的路徑>，或 --all 時 git add -A；stage 後沒有任何改動也算失敗。
  4. commit：guarded_run(["git", "-C", <repo>, "commit", "-F", <final>])。
  5. push：guarded_run(["git", "-C", <repo>, "push", "-u", "origin", <branch>])；--no-push 時跳過。

輸出一行 JSON（ensure_ascii=False）：
  {"ok", "step", "branch", "commit", "files", "pushed", "problems", "denied", "error"}
  step：成功時 "done"，失敗時停在哪一步（usage、repo、message、stage、commit、push）。
  commit：新 commit 的 SHA（還沒 commit 是 null）。files：這個 commit 的檔案清單。
  pushed：有沒有 push 成功。problems：check_message 的錯誤。
  denied：hook 擋下的 [{"hook", "decision", "reason"}]。error：失敗說明（成功是 null）。
結束碼：成功 0；檢查、hook 或 git 失敗 1；用法錯 2。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "workflow"))
import check_commit_msg  # noqa: E402
import hook_rules  # noqa: E402


class Fail(Exception):
    def __init__(self, step, error, **extra):
        super().__init__(error)
        self.step = step
        self.error = error
        self.extra = extra


class Usage(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Usage(message)


def parser() -> Parser:
    ap = Parser(description="檢查 commit 訊息後 commit 並 push 到自己的分支")
    ap.add_argument("--repo", required=True, help="worktree 根目錄")
    ap.add_argument("--branch", required=True, help="目前分支（不能是 main）")
    ap.add_argument("--message-file", required=True, help="標題（可加空行與內文），不含 footer")
    ap.add_argument("--refs", required=True, help="issue 編號，footer 寫成 Refs: #<refs>")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--add", nargs="+", metavar="路徑", help="只 stage 這些路徑")
    group.add_argument("--all", action="store_true", help="git add -A")
    ap.add_argument("--no-push", action="store_true", help="只 commit，不 push")
    return ap


def git(repo: Path, *args: str, step: str = "repo") -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Fail(step, f"git {' '.join(args)} 失敗：{(r.stderr or r.stdout).strip()}")
    return r.stdout


def check_repo(repo: Path, branch: str) -> None:
    if branch == "main":
        raise Fail("repo", "--branch 不能是 main：一律 commit、push 到自己的分支，進 main 只能走 merge")
    if not repo.is_dir():
        raise Fail("repo", f"--repo 不是目錄：{repo}")
    top = git(repo, "rev-parse", "--show-toplevel").strip()
    if Path(top).resolve() != repo.resolve():
        raise Fail("repo", f"--repo 不是 git worktree 的根目錄（根目錄是 {top}）")
    r = subprocess.run(["git", "-C", str(repo), "symbolic-ref", "--short", "-q", "HEAD"],
                       capture_output=True, text=True)
    current = r.stdout.strip() if r.returncode == 0 else ""
    if current != branch:
        raise Fail("repo", f"目前分支是 {current or '（detached HEAD）'}，不是 --branch 給的 {branch}")
    if not git(repo, "status", "--porcelain").strip():
        raise Fail("repo", "沒有改動可以 commit")


def with_refs(text: str, refs: str) -> str:
    """在訊息最後加 `Refs: #<refs>`；已經有同一行就不重複加。"""
    footer = f"Refs: #{refs}"
    lines = text.rstrip().split("\n")
    if any(ln.strip() == footer for ln in lines):
        return "\n".join(lines) + "\n"
    paras = check_commit_msg.paragraphs(lines[1:])
    last = paras[-1] if paras else []
    if last and all(check_commit_msg.FOOTER_KEY_RE.match(ln) for _, ln in last):
        return "\n".join(lines + [footer]) + "\n"  # 最後一段已經是 footer，接在同一段
    return "\n".join(lines + ["", footer]) + "\n"


def prepare_message(message_file: Path, refs: str) -> Path:
    try:
        text = message_file.read_text(encoding="utf-8")
    except OSError as e:
        raise Fail("message", f"讀不到 --message-file：{e}")
    final = message_file.with_name(message_file.name + ".final")
    final.write_text(with_refs(text, refs), encoding="utf-8")
    errors, _notes = check_commit_msg.check_message(final.read_text(encoding="utf-8"))
    if errors:
        raise Fail("message", "commit 訊息格式不合（規格見 vendor_kit#110）", problems=errors)
    return final


def stage(repo: Path, paths, all_: bool) -> None:
    if all_:
        git(repo, "add", "-A", step="stage")
    else:
        git(repo, "add", "--", *paths, step="stage")
    r = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        raise Fail("stage", "stage 之後沒有任何改動（--add 給的路徑沒有改動？）")


def guarded(step: str, argv, repo: Path, settings=None, project_dir=None) -> dict:
    r = hook_rules.guarded_run(argv, repo, settings=settings, project_dir=project_dir)
    if r["ok"]:
        return r
    check = r.get("precheck") or {}
    if not r.get("ran"):
        if check.get("denied"):
            raise Fail(step, "hook 擋下", denied=check["denied"])
        if check.get("errors"):
            msgs = "；".join(f"{e.get('hook')}：{e.get('error')}" for e in check["errors"])
            raise Fail(step, f"hook 檢查出錯，不執行：{msgs}")
        raise Fail(step, r.get("error") or "沒有執行")
    raise Fail(step, f"git {argv[3]} 失敗（結束碼 {r['returncode']}）："
                     f"{(r['stderr'] or r['stdout']).strip()}")


def commit(repo: Path, final: Path, settings=None, project_dir=None) -> dict:
    return guarded("commit", ["git", "-C", str(repo), "commit", "-F", str(final)], repo,
                   settings=settings, project_dir=project_dir)


def push(repo: Path, branch: str, settings=None, project_dir=None) -> dict:
    return guarded("push", ["git", "-C", str(repo), "push", "-u", "origin", branch], repo,
                   settings=settings, project_dir=project_dir)


def run(argv=None, *, settings=None, project_dir=None) -> tuple[int, dict]:
    out = {"ok": False, "step": "usage", "branch": None, "commit": None, "files": [],
           "pushed": False, "problems": [], "denied": [], "error": None}
    try:
        args = parser().parse_args(argv)
        if not (args.add or args.all):
            raise Usage("要給 --add <路徑>… 或 --all")
        if not re.fullmatch(r"#?\d+", args.refs):
            raise Usage(f"--refs 要是 issue 編號：{args.refs}")
    except Usage as e:
        out["error"] = f"用法錯：{e}"
        return 2, out
    refs = args.refs.lstrip("#")
    repo = Path(args.repo)
    out["branch"] = args.branch
    try:
        out["step"] = "repo"
        check_repo(repo, args.branch)
        out["step"] = "message"
        final = prepare_message(Path(args.message_file), refs)
        out["step"] = "stage"
        stage(repo, args.add, args.all)
        out["step"] = "commit"
        commit(repo, final, settings=settings, project_dir=project_dir)
        out["commit"] = git(repo, "rev-parse", "HEAD", step="commit").strip()
        out["files"] = [f for f in git(repo, "diff-tree", "--root", "--no-commit-id", "--name-only",
                                       "-r", "-z", "HEAD", step="commit").split("\0") if f]
        if not args.no_push:
            out["step"] = "push"
            push(repo, args.branch, settings=settings, project_dir=project_dir)
            out["pushed"] = True
    except Fail as e:
        out["step"] = e.step
        out["error"] = e.error
        out["problems"] = e.extra.get("problems", [])
        out["denied"] = e.extra.get("denied", [])
        return 1, out
    out["ok"] = True
    out["step"] = "done"
    return 0, out


def main(argv=None) -> int:
    code, out = run(argv)
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
