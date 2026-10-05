"""依序把留言檔貼到 issue 或 PR，可選貼完關閉 issue；寫入一律先過 .claude/settings.json 的 Bash hook。

取代「逐則 `gh issue comment --body-file` → 記網址 → 遇錯停 →（可選）`gh issue close`」逐一下指令。
每個寫入（每則留言、關閉）都經 script/workflow/hook_rules.py 的 guarded_run：把即將執行的同一個 argv
交給註冊的每支 Bash hook（例如 comment_tag_guard.py 查標記與本機絕對路徑、attribution_guard.py
擋 Claude 署名）檢查，被擋就不執行；這支腳本不另抄 hook 的規則。

用法（在 repo 裡任一目錄）：
  python3 script/github/post_comments.py --kind issue|pr --number <N> \
      (--body-file <檔> [<檔> …] | --dir <目錄>) [--close] [--delete]

- 留言檔：--body-file 依給的順序（可重複給）；--dir 取目錄裡的 `post_*.md`，依檔名排序
  （script/workflow/prepare_comment.py 產生的命名，檔名排序就是貼出順序）。一則都沒有、
  檔案不存在或 --dir 不是目錄都算用法錯。
- 先全部 precheck：對每一則用 hook_rules.precheck 檢查
  `gh <kind> comment <N> -R ycpss91255-research/vendor_kit --body-file <絕對路徑>`；
  任何一則被擋（或 hook 出錯）就一則都不貼。
- 再依序經 guarded_run 貼，從 stdout 最後一行取留言網址；某一則失敗就停，不貼後面的。
- --close（只限 --kind issue）：全部貼完才經 guarded_run 跑 `gh issue close <N> -R <repo>`；
  不帶 --comment（hook 不准，留言已經先貼了）。
- --delete：全部貼成功後刪掉留言檔（在 --close 之前刪，關閉失敗重試時不需要再貼）。

測試用環境變數 POST_COMMENTS_GH 把 gh 換成假程式（hook 檢查仍用字面的 gh）。

輸出一行 JSON（ensure_ascii=False）：
  {"ok", "planned", "urls", "failed_at", "closed", "denied", "error"}
  planned：要貼的留言檔絕對路徑，依貼出順序；urls：已貼出的留言網址（輸出沒有網址時記 null）；
  failed_at：失敗那一則的路徑（precheck 擋下或貼的時候失敗；關閉失敗時是 null）；
  closed：是否已關閉 issue；denied：hook 擋下或出錯的明細，每筆
  {"path", "hook", "decision", "reason"} 或 {"path", "hook", "error"}（關閉時 path 是 null）；
  error：錯誤說明。
結束碼：0 全部成功；1 precheck 擋下（什麼都沒貼）；2 用法錯（什麼都沒貼）；
  3 貼的階段失敗（urls 是已貼的，failed_at 是失敗那一則），或留言全部貼完但關閉失敗
  （failed_at 是 null，只需重跑 `gh issue close`）。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "workflow"))
import hook_rules  # noqa: E402

REPO = "ycpss91255-research/vendor_kit"
BIN_ENV = "POST_COMMENTS_GH"
PATTERN = "post_*.md"


class UsageError(Exception):
    """命令列用法錯。"""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def result(**kw) -> dict:
    out = {"ok": False, "planned": [], "urls": [], "failed_at": None, "closed": False,
           "denied": [], "error": None}
    out.update(kw)
    return out


def denied_of(check: dict, path) -> list:
    """precheck 結果的 denied 與 errors，每筆加上 path。"""
    return ([dict(d, path=path) for d in check.get("denied") or []]
            + [dict(e, path=path) for e in check.get("errors") or []])


def comment_argv(kind: str, number: int, path: Path) -> list[str]:
    return ["gh", kind, "comment", str(number), "-R", REPO, "--body-file", str(path)]


def parser() -> Parser:
    p = Parser(prog="post_comments.py", description="依序貼留言、可選貼完關閉 issue（寫入經 hook 檢查）")
    p.add_argument("--kind", required=True, choices=("issue", "pr"))
    p.add_argument("--number", required=True, type=int)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--body-file", action="extend", nargs="+")
    src.add_argument("--dir")
    p.add_argument("--close", action="store_true")
    p.add_argument("--delete", action="store_true")
    return p


def planned_files(a) -> list[Path]:
    if a.dir is not None:
        d = Path(a.dir)
        if not d.is_dir():
            raise UsageError(f"--dir 不是目錄：{a.dir}")
        files = sorted(d.resolve().glob(PATTERN), key=lambda p: p.name)
        if not files:
            raise UsageError(f"--dir 裡沒有 {PATTERN}：{a.dir}")
        return files
    files = [Path(f).resolve() for f in a.body_file]
    missing = [str(f) for f in files if not f.is_file()]
    if missing:
        raise UsageError(f"留言檔不存在：{'、'.join(missing)}")
    return files


def post(a, cwd: Path, out: dict) -> int:
    if a.number <= 0:
        raise UsageError("--number 要是正整數")
    if a.close and a.kind != "issue":
        raise UsageError("--close 只限 --kind issue")
    files = planned_files(a)
    out["planned"] = [str(f) for f in files]

    for f in files:
        check = hook_rules.precheck(comment_argv(a.kind, a.number, f), cwd)
        if not check["ok"]:
            out["denied"] += denied_of(check, str(f))
            if out["failed_at"] is None:
                out["failed_at"] = str(f)
    if out["denied"]:
        out["error"] = f"hook 擋下 {out['failed_at']}，一則都沒貼"
        return 1

    for f in files:
        run = hook_rules.guarded_run(comment_argv(a.kind, a.number, f), cwd, bin_env=BIN_ENV)
        if not run["ok"]:
            out["failed_at"] = str(f)
            out["denied"] = denied_of(run.get("precheck") or {}, str(f))
            out["error"] = run.get("error") or (
                f"gh {a.kind} comment 失敗：{run['stderr'].strip()}" if run.get("ran")
                else "hook 擋下 gh comment")
            return 3
        lines = [ln.strip() for ln in run["stdout"].splitlines() if ln.strip()]
        out["urls"].append(lines[-1] if lines else None)

    if a.delete:
        for f in files:
            f.unlink(missing_ok=True)

    if a.close:
        run = hook_rules.guarded_run(["gh", "issue", "close", str(a.number), "-R", REPO], cwd,
                                     bin_env=BIN_ENV)
        if not run["ok"]:
            out["denied"] = denied_of(run.get("precheck") or {}, None)
            out["error"] = run.get("error") or (
                f"留言已全部貼出，但 gh issue close 失敗：{run['stderr'].strip()}" if run.get("ran")
                else "留言已全部貼出，但 hook 擋下 gh issue close")
            return 3
        out["closed"] = True

    out["ok"] = True
    return 0


def main(argv=None) -> int:
    out = result()
    try:
        code = post(parser().parse_args(argv), Path.cwd(), out)
    except UsageError as e:
        out["error"] = f"用法錯：{e}"
        code = 2
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
