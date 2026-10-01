#!/usr/bin/env python3
"""doc-edit 的備份、改前快照、備份檢查、範圍外檢查與這一輪的 diff（#139）。

這些動作以前由子代理照 workflow 的文字步驟自己做，r152 因此誤判（#133），r163 又因暫存鍵不含副檔名，
03_output.md 與 03_output.csv 的暫存檔互相覆蓋。規則一律以這支為準。

用法（<file> 一律是相對 repo 根目錄的路徑，也可以給 repo 底下的絕對路徑；<rNN> 是輪次，例如 r163）：
    python3 script/doc/backup.py key <file>...
    python3 script/doc/backup.py save     --repo <R> --round <rNN> <file>...
    python3 script/doc/backup.py base     --repo <R> --round <rNN> <file>
    python3 script/doc/backup.py diff     --repo <R> --round <rNN> <file>
    python3 script/doc/backup.py snapshot --repo <R> --out <json> [--files <f>...]
    python3 script/doc/backup.py verify   --repo <R> --round <rNN> --before <json> --scope <f>... --round-files <f>...

鍵：
- backup_key：路徑去掉結尾的 .md 或 .csv、/ 換成 _、去掉開頭的點（跟 mark_changes.py 的 target() 同一套），
  例如 doc/contract/03_output.csv → doc_contract_03_output。備份檔名用它。
- run_key：.md 或 .csv 檔是 backup_key 接 `_` 加副檔名（doc_contract_03_output_csv、README_md）；
  其他檔等於 backup_key（副檔名沒被去掉，本來就不會撞）。暫存目錄與 review_log 檔名用它。

備份放 <R>/doc/decisions/_backup/：
- 這一輪的基準：<backup_key>.pre_<round><ext>，一定是這一輪改之前的原檔。<ext>：.csv 檔是 .csv，其他一律 .md。
- 之後的備份：<backup_key>.pre_<round>.<N><ext>，N 從 2 起、取現有最大加一。

子命令與輸出（stdout 一行 JSON，ensure_ascii=False；成功與失敗都有 "ok"）：
- key → {"ok", "keys": [{"file", "backup_key", "run_key"}]}
- save：基準不存在就建它；已存在時，目前內容的 md5 等於這一輪任何一份既有備份就不另存、回報那一份，
  否則另存下一個序號。檔案不存在（這一輪新建的檔）就不備份，標 "missing": true。
  → {"ok", "results": [{"file", "backup", "created", "seq", "md5", "missing"}]}（基準的 seq 是 1）
- base → {"ok", "file", "base", "exists"}
- diff：基準優先用這一輪的基準備份，不存在就用 `git show HEAD:<file>`，都沒有就整份算新增。
  → {"ok", "file", "base", "base_kind": "backup"|"HEAD"|"none", "empty", "diff"}；diff 是 unified diff 文字。
- snapshot：記下 `git status --porcelain -z --untracked-files=all`（同 --short 的路徑）每個路徑的 md5、
  --files 每個檔的 md5、_backup/ 的檔名清單，寫進 --out。--out 不要放在 repo 裡，否則它自己會被當成變動。
  → {"ok", "out", "paths"}（paths 是記下的路徑數）
- verify：重做一次快照，跟 --before 比對。
  → {"ok", "changed", "new_backups", "backup_problems", "out_of_scope", "parallel", "diffstat"}
  1. 變動（changed）：改前快照或現在的 git status 裡出現的路徑、以及 --files 記過的檔，改前與現在的 md5 不同的。
     改前快照沒記到的路徑，改前內容視為 HEAD 的版本（不在 HEAD 就是不存在）。
  2. 備份（backup_problems，#133）：--scope 裡有變動、改前就存在的檔，這一輪的基準必須存在，而且改前的 md5
     必須等於這一輪某一份既有備份（基準或帶序號的），也就是改前狀態可以從既有備份還原。
  3. 範圍外（out_of_scope）：變動的路徑不在 --round-files、也不在 doc/decisions/ 底下。
  4. 並行（parallel）：變動的路徑在 --round-files、不在 --scope，是別的並行子代理造成的，不算錯。
  5. diffstat：`git diff --stat -- <scope>` 的輸出。
  backup_problems 或 out_of_scope 非空時 ok 為 false。

結束碼：全過 0；有問題 1（save 寫檔失敗、verify 找到問題）；用法錯 2（參數不對、輪次格式不對、
repo 不是 git repo、檔案不在 repo 裡、--before 讀不到）。
"""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROUND = re.compile(r"^r[0-9]+$")
BACKUP_DIR = Path("doc/decisions/_backup")
KEY_EXT = re.compile(r"\.(md|csv)$")


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def emit(data: dict, code: int) -> int:
    print(json.dumps(data, ensure_ascii=False))
    return code


# ───────────────── 鍵 ─────────────────
def backup_key(rel: str) -> str:
    return KEY_EXT.sub("", rel).replace("/", "_").lstrip(".")


def run_key(rel: str) -> str:
    m = KEY_EXT.search(rel)
    return backup_key(rel) + (f"_{m.group(1)}" if m else "")


def backup_ext(rel: str) -> str:
    return ".csv" if rel.endswith(".csv") else ".md"


# ───────────────── repo 與檔案 ─────────────────
def repo_root(repo: str) -> Path:
    path = Path(repo).resolve()
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise UsageError(f"--repo 不是 git repo：{repo}")
    return Path(r.stdout.strip()).resolve()


def rel_path(root: Path, f: str) -> str:
    p = Path(f)
    if p.is_absolute():
        try:
            return p.resolve().relative_to(root).as_posix()
        except ValueError:
            raise UsageError(f"檔案不在 repo 裡：{f}")
    norm = PurePosixPath(p.as_posix())
    if ".." in norm.parts:
        raise UsageError(f"路徑不能含 ..：{f}")
    return norm.as_posix()


def check_round(rnd: str) -> str:
    if not ROUND.match(rnd):
        raise UsageError(f"--round 要是 rNN（收到 {rnd!r}）")
    return rnd


def md5_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def md5_file(path: Path) -> str | None:
    try:
        return md5_bytes(path.read_bytes())
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return None


def head_bytes(root: Path, rel: str) -> bytes | None:
    r = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def git_status_paths(root: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-z", "--untracked-files=all"],
                         capture_output=True, check=True).stdout.decode("utf-8", "surrogateescape")
    tokens = out.split("\0")
    paths = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        i += 1
        if len(tok) < 4:
            continue
        xy, path = tok[:2], tok[3:]
        paths.append(path)
        if "R" in xy or "C" in xy:  # 改名或複製：下一個 token 是原路徑
            if i < len(tokens) and tokens[i]:
                paths.append(tokens[i])
            i += 1
    return sorted(set(paths))


# ───────────────── 備份 ─────────────────
def base_path(root: Path, rel: str, rnd: str) -> Path:
    return root / BACKUP_DIR / f"{backup_key(rel)}.pre_{rnd}{backup_ext(rel)}"


def round_backups(root: Path, rel: str, rnd: str) -> list[tuple[int, Path]]:
    """這一輪既有的備份，依序號排：基準是 1，帶序號的是 N。"""
    found = []
    base = base_path(root, rel, rnd)
    if base.is_file():
        found.append((1, base))
    pattern = re.compile(re.escape(f"{backup_key(rel)}.pre_{rnd}.") + r"([0-9]+)" + re.escape(backup_ext(rel)) + "$")
    d = root / BACKUP_DIR
    if d.is_dir():
        for p in d.iterdir():
            m = pattern.match(p.name)
            if m and p.is_file():
                found.append((int(m.group(1)), p))
    return sorted(found)


def save_one(root: Path, rel: str, rnd: str) -> dict:
    src = root / rel
    if not src.is_file():
        return {"file": rel, "backup": None, "created": False, "seq": None, "md5": None, "missing": True}
    data = src.read_bytes()
    digest = md5_bytes(data)
    existing = round_backups(root, rel, rnd)
    base = base_path(root, rel, rnd)
    if not any(seq == 1 for seq, _ in existing):
        target, seq = base, 1
    else:
        for seq, p in existing:
            if md5_file(p) == digest:
                return {"file": rel, "backup": str(p), "created": False, "seq": seq, "md5": digest, "missing": False}
        seq = max(2, max(s for s, _ in existing) + 1)
        target = root / BACKUP_DIR / f"{backup_key(rel)}.pre_{rnd}.{seq}{backup_ext(rel)}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"file": rel, "backup": str(target), "created": True, "seq": seq, "md5": digest, "missing": False}


# ───────────────── 快照 ─────────────────
def take_snapshot(root: Path, files: list[str]) -> dict:
    status = {p: md5_file(root / p) for p in git_status_paths(root)}
    tracked = {f: md5_file(root / f) for f in files}
    d = root / BACKUP_DIR
    backups = sorted(p.name for p in d.iterdir()) if d.is_dir() else []
    return {"status": status, "files": tracked, "backups": backups}


def before_md5(root: Path, snap: dict, rel: str) -> str | None:
    if rel in snap.get("files", {}):
        return snap["files"][rel]
    if rel in snap.get("status", {}):
        return snap["status"][rel]
    data = head_bytes(root, rel)
    return md5_bytes(data) if data is not None else None


def under(rel: str, prefix: str) -> bool:
    return rel == prefix.rstrip("/") or rel.startswith(prefix)


# ───────────────── 子命令 ─────────────────
def cmd_key(args) -> int:
    keys = []
    for f in args.files:
        rel = PurePosixPath(Path(f).as_posix()).as_posix()
        keys.append({"file": rel, "backup_key": backup_key(rel), "run_key": run_key(rel)})
    return emit({"ok": True, "keys": keys}, 0)


def cmd_save(args) -> int:
    root = repo_root(args.repo)
    rnd = check_round(args.round)
    rels = [rel_path(root, f) for f in args.files]
    results = []
    try:
        for rel in rels:
            results.append(save_one(root, rel, rnd))
    except OSError as e:
        return emit({"ok": False, "results": results, "error": f"備份失敗：{e}"}, 1)
    return emit({"ok": True, "results": results}, 0)


def cmd_base(args) -> int:
    root = repo_root(args.repo)
    rnd = check_round(args.round)
    rel = rel_path(root, args.file)
    base = base_path(root, rel, rnd)
    return emit({"ok": True, "file": rel, "base": str(base), "exists": base.is_file()}, 0)


def cmd_diff(args) -> int:
    root = repo_root(args.repo)
    rnd = check_round(args.round)
    rel = rel_path(root, args.file)
    base = base_path(root, rel, rnd)
    if base.is_file():
        old, kind, base_name = base.read_bytes(), "backup", str(base)
    else:
        old = head_bytes(root, rel)
        kind, base_name = ("HEAD", f"HEAD:{rel}") if old is not None else ("none", None)
        old = old or b""
    cur = root / rel
    new = cur.read_bytes() if cur.is_file() else b""
    lines = difflib.unified_diff(
        old.decode("utf-8", "replace").splitlines(keepends=True),
        new.decode("utf-8", "replace").splitlines(keepends=True),
        fromfile=f"a/{rel}", tofile=f"b/{rel}",
    )
    text = "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in lines)
    return emit({"ok": True, "file": rel, "base": base_name, "base_kind": kind, "empty": text == "", "diff": text}, 0)


def cmd_snapshot(args) -> int:
    root = repo_root(args.repo)
    files = [rel_path(root, f) for f in args.files]
    snap = take_snapshot(root, files)
    snap["repo"] = str(root)
    out = Path(args.out)
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError as e:
        return emit({"ok": False, "out": str(out), "error": f"寫不進 --out：{e}"}, 1)
    paths = len(set(snap["status"]) | set(snap["files"]))
    return emit({"ok": True, "out": str(out), "paths": paths}, 0)


def cmd_verify(args) -> int:
    root = repo_root(args.repo)
    rnd = check_round(args.round)
    try:
        before = json.loads(Path(args.before).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise UsageError(f"--before 讀不到：{e}")
    scope = [rel_path(root, f) for f in args.scope]
    round_files = {rel_path(root, f) for f in args.round_files}
    after = take_snapshot(root, [])
    candidates = set(before.get("status", {})) | set(before.get("files", {})) | set(after["status"]) | set(scope)
    changed = sorted(p for p in candidates if before_md5(root, before, p) != md5_file(root / p))

    before_backups = set(before.get("backups", []))
    new_backups = [str(root / BACKUP_DIR / n) for n in after["backups"] if n not in before_backups]

    problems = []
    for rel in scope:
        if rel not in changed:
            continue
        prev = before_md5(root, before, rel)
        if prev is None:  # 這一步新建的檔，改前不存在，沒有東西要還原
            continue
        existing = round_backups(root, rel, rnd)
        names = [str(p) for _, p in existing]
        if not any(seq == 1 for seq, _ in existing):
            problems.append({"file": rel, "reason": f"這一輪的基準 {base_path(root, rel, rnd).name} 不存在",
                             "before_md5": prev, "backups": names})
        elif not any(md5_file(p) == prev for _, p in existing):
            problems.append({"file": rel, "reason": "改前內容跟這一輪任何一份備份都不同，無法還原",
                             "before_md5": prev, "backups": names})

    scope_set = set(scope)
    out_of_scope = [p for p in changed if p not in round_files and p not in scope_set and not under(p, "doc/decisions/")]
    parallel = [p for p in changed if p in round_files and p not in scope_set]
    diffstat = subprocess.run(["git", "-C", str(root), "diff", "--stat", "--", *scope],
                              capture_output=True, text=True).stdout if scope else ""
    ok = not problems and not out_of_scope
    return emit({"ok": ok, "changed": changed, "new_backups": new_backups, "backup_problems": problems,
                 "out_of_scope": out_of_scope, "parallel": parallel, "diffstat": diffstat}, 0 if ok else 1)


def build_parser() -> Parser:
    p = Parser(prog="backup.py", description="doc-edit 的備份、快照與範圍檢查")
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=Parser)

    s = sub.add_parser("key")
    s.add_argument("files", nargs="+")
    s.set_defaults(func=cmd_key)

    for name, func in (("save", cmd_save), ("base", cmd_base), ("diff", cmd_diff)):
        s = sub.add_parser(name)
        s.add_argument("--repo", required=True)
        s.add_argument("--round", required=True)
        if name == "save":
            s.add_argument("files", nargs="+")
        else:
            s.add_argument("file")
        s.set_defaults(func=func)

    s = sub.add_parser("snapshot")
    s.add_argument("--repo", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--files", nargs="*", default=[])
    s.set_defaults(func=cmd_snapshot)

    s = sub.add_parser("verify")
    s.add_argument("--repo", required=True)
    s.add_argument("--round", required=True)
    s.add_argument("--before", required=True)
    s.add_argument("--scope", nargs="+", required=True)
    s.add_argument("--round-files", nargs="+", required=True)
    s.set_defaults(func=cmd_verify)
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return args.func(args)
    except UsageError as e:
        return emit({"ok": False, "error": str(e)}, 2)


if __name__ == "__main__":
    sys.exit(main())
