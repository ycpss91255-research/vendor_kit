"""doc-edit 的輪次編號：算出已用過的最大輪次與下一個輪次，或檢查給定的輪次是不是下一個。

已用過的輪次有兩個來源：
- 本機 `doc/decisions/_backup/` 的備份檔名裡的 `pre_rNN`（不進 git，#128）；帶序號的備份
  （例如 `x.pre_r12.2.md`）也算 12。只看這個目錄本身的檔名，不往下找。
- `git log --format=%B`（目前 HEAD 的歷史）裡行首的 `Doc-Edit: rNN` footer；換電腦或新 clone 時
  `_backup/` 是空的，靠 footer 才不會重用。

用法：
  python3 script/doc/round.py next [--repo <R>]
  python3 script/doc/round.py check <rNN> [--repo <R>]

--repo 不給時用目前目錄所在 git repo 的根目錄。

輸出一行 JSON 到 stdout：
  next：{"ok": true, "max", "next", "backup_max", "footer_max"}
    backup_max／footer_max 是各來源的最大編號，沒有就是 null；max 取兩者最大（都沒有是 0）；
    next 是 "r<max+1>"。
  check：同上，再加 "round"（給的輪次）與 "expected"（等於 next）；
    round 格式不是 rNN（r 後面接數字），或編號不等於 max+1（重用或跳號）時 ok=false，並附 "error"。
  失敗（不是 git repo、git 執行失敗）：{"ok": false, "error"}。

結束碼：0＝成功（check 時輪次正確）；1＝check 的輪次格式不對、重用或跳號；2＝執行失敗。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

BACKUP_DIR = Path("doc/decisions/_backup")
BACKUP_RE = re.compile(r"pre_r(\d+)")
FOOTER_RE = re.compile(r"^Doc-Edit: r(\d+)", re.MULTILINE)
ROUND_RE = re.compile(r"^r(\d+)$")


class Fail(Exception):
    pass


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def repo_root(repo: str | None) -> Path:
    start = Path(repo) if repo else Path.cwd()
    r = git(start, "rev-parse", "--show-toplevel")
    if r.returncode != 0:
        raise Fail(f"不是 git repo：{start}：{(r.stderr or r.stdout).strip()}")
    return Path(r.stdout.strip())


def backup_max(root: Path) -> int | None:
    d = root / BACKUP_DIR
    if not d.is_dir():
        return None
    nums = [int(m.group(1)) for p in d.iterdir() for m in BACKUP_RE.finditer(p.name)]
    return max(nums) if nums else None


def footer_max(root: Path) -> int | None:
    if git(root, "rev-parse", "--verify", "--quiet", "HEAD").returncode != 0:
        return None  # 還沒有任何 commit
    r = git(root, "log", "--format=%B")
    if r.returncode != 0:
        raise Fail(f"git log 失敗：{(r.stderr or r.stdout).strip()}")
    nums = [int(n) for n in FOOTER_RE.findall(r.stdout)]
    return max(nums) if nums else None


def compute(root: Path) -> dict:
    b = backup_max(root)
    f = footer_max(root)
    m = max([x for x in (b, f) if x is not None], default=0)
    return {"ok": True, "max": m, "next": f"r{m + 1}", "backup_max": b, "footer_max": f}


def check(info: dict, rnd: str) -> dict:
    out = dict(info, round=rnd, expected=info["next"])
    m = ROUND_RE.match(rnd)
    if not m:
        out.update(ok=False, error=f"round 格式要是 rNN：{rnd!r}")
    elif int(m.group(1)) != info["max"] + 1:
        kind = "重用" if int(m.group(1)) <= info["max"] else "跳號"
        out.update(ok=False, error=f"round {rnd} {kind}：已用過的最大是 r{info['max']}，這一輪要用 {info['next']}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="doc-edit 的輪次編號")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_next = sub.add_parser("next", help="算下一個輪次")
    p_next.add_argument("--repo")
    p_check = sub.add_parser("check", help="檢查輪次是不是下一個")
    p_check.add_argument("round")
    p_check.add_argument("--repo")
    args = ap.parse_args(argv)
    try:
        info = compute(repo_root(args.repo))
    except Fail as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    if args.cmd == "next":
        print(json.dumps(info, ensure_ascii=False))
        return 0
    out = check(info, args.round)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
