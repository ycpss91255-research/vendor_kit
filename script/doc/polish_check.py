#!/usr/bin/env python3
"""潤稿越界檢查：潤稿只准改這一輪改過的行，落在範圍外的變動找出來，可選擇還原。

範圍是「這一輪的基準 → 潤稿前」的新增或修改行（difflib 的 replace／insert 落在潤稿前的行）。
比對「潤稿前 → 潤稿後」：
- 等長的 replace 逐行判斷，每一行都要在範圍內；
- 其他變動整段判斷，整段都要在範圍內；純插入（潤稿前沒有對應行）只要緊鄰的前一行或後一行在範圍內就保留。
不在範圍內的變動記進 violations；帶 --fix 時把那些段還原成潤稿前的原文，寫回 <潤稿後>。

用法：
    python3 script/doc/polish_check.py <基準> <潤稿前> <潤稿後> [--fix]
    python3 script/doc/polish_check.py --repo <R> --round <rNN> <file> <潤稿前> [--fix]

第二種用法（doc-edit 用這個）自己取基準：<file> 是相對 <R> 的路徑（也可以給 <R> 底下的絕對路徑），
潤稿後＝<R>/<file>；基準跟 `backup.py diff` 同一套順序：這一輪的基準備份存在就用它，否則用
`git show HEAD:<file>`，都沒有就是空內容。判定用 backup.py 的 base_path、head_bytes，
基準只在記憶體裡比，不寫暫存檔。

輸出（stdout 一行 JSON）：
    {"ok": bool, "round_changed_lines": int, "violations": [...], "reverted": bool}
    第二種用法多兩欄：base_kind（"backup"|"HEAD"|"none"）與 base（backup 時是基準備份的路徑，其他是 null）。
    violations 每筆 {"pre_lines": [起, 迄], "post_lines": [起, 迄], "post_text": "..."}，
    行號從 1 起算、迄為含；純插入或純刪除時起比迄大 1。
    ok 為 true：沒有越界，或越界已用 --fix 還原。
    讀不到或寫不了檔、參數不對：{"ok": false, "error": "..."}。

結束碼：
    0  沒有越界；或有越界且已 --fix 還原
    1  有越界、沒有還原
    2  讀不到檔（或 --fix 寫不了檔）；第二種用法的參數不對（位置參數個數、輪次格式、repo 不是 git repo、
       檔案不在 repo 裡）
"""
import argparse
import difflib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import backup  # noqa: E402


def decode_lines(data):
    """跟 read_lines 同一套解碼（UTF-8、通用換行）。"""
    return io.TextIOWrapper(io.BytesIO(data), encoding="utf-8").read().splitlines(keepends=True)


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines(keepends=True)


def round_base(repo, rnd, file):
    """依輪次取基準，順序同 backup.py diff。回傳 (root, rel, base_kind, base 路徑或 None, 基準的行)。"""
    root = backup.repo_root(repo)
    rnd = backup.check_round(rnd)
    rel = backup.rel_path(root, file)
    path = backup.base_path(root, rel, rnd)
    if path.is_file():
        return root, rel, "backup", str(path), read_lines(path)
    data = backup.head_bytes(root, rel)
    if data is not None:
        return root, rel, "HEAD", None, decode_lines(data)
    return root, rel, "none", None, []


def allowed_lines(base, pre):
    """潤稿前裡屬於這一輪改動（新增或修改）的行號，從 0 起算。"""
    allowed = set()
    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(None, base, pre, autojunk=False).get_opcodes():
        if tag in ("replace", "insert"):
            allowed.update(range(j1, j2))
    return allowed


def check(base, pre, cur):
    """回傳 (allowed, violations, 還原後的行)。"""
    allowed = allowed_lines(base, pre)
    out, bad = [], []

    def keep(i1, i2, j1, j2):
        ok = all(i in allowed for i in range(i1, i2)) if i2 > i1 else (i1 - 1 in allowed or i1 in allowed)
        if ok:
            out.extend(cur[j1:j2])
        else:
            bad.append({"pre_lines": [i1 + 1, i2], "post_lines": [j1 + 1, j2], "post_text": "".join(cur[j1:j2])})
            out.extend(pre[i1:i2])

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pre, cur, autojunk=False).get_opcodes():
        if tag == "equal":
            out.extend(pre[i1:i2])
        elif tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                keep(i1 + k, i1 + k + 1, j1 + k, j1 + k + 1)
        else:
            keep(i1, i2, j1, j2)
    return allowed, bad, out


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="潤稿越界檢查：找出（並可還原）落在這一輪改動範圍外的潤稿變動",
        usage="%(prog)s <基準> <潤稿前> <潤稿後> [--fix]\n"
              "       %(prog)s --repo <R> --round <rNN> <file> <潤稿前> [--fix]")
    ap.add_argument("paths", nargs="+",
                    help="<基準> <潤稿前> <潤稿後>；帶 --repo、--round 時是 <file> <潤稿前>")
    ap.add_argument("--repo", help="repo 根目錄；給了就依 --round 自己取基準")
    ap.add_argument("--round", help="輪次 rNN，跟 --repo 一起給")
    ap.add_argument("--fix", action="store_true", help="把越界的變動還原成潤稿前的原文")
    args = ap.parse_args(argv)

    extra = {}
    if args.repo is not None or args.round is not None:
        if args.repo is None or args.round is None or len(args.paths) != 2:
            emit({"ok": False, "error": "--repo 與 --round 要一起給，位置參數是 <file> <潤稿前>"})
            return 2
        try:
            root, rel, kind, base_name, base = round_base(args.repo, args.round, args.paths[0])
        except backup.UsageError as e:
            emit({"ok": False, "error": str(e)})
            return 2
        except (OSError, UnicodeDecodeError) as e:
            emit({"ok": False, "error": f"讀不到基準：{e}"})
            return 2
        pre_path, post_path = args.paths[1], str(root / rel)
        extra = {"base_kind": kind, "base": base_name}
        try:
            pre, cur = read_lines(pre_path), read_lines(post_path)
        except (OSError, UnicodeDecodeError) as e:
            emit({"ok": False, "error": f"讀不到檔：{e}", **extra})
            return 2
    else:
        if len(args.paths) != 3:
            emit({"ok": False, "error": "位置參數是 <基準> <潤稿前> <潤稿後>"})
            return 2
        post_path = args.paths[2]
        try:
            base, pre, cur = (read_lines(p) for p in args.paths)
        except (OSError, UnicodeDecodeError) as e:
            emit({"ok": False, "error": f"讀不到檔：{e}"})
            return 2

    allowed, bad, out = check(base, pre, cur)
    reverted = bool(args.fix and bad)
    if reverted:
        try:
            with open(post_path, "w", encoding="utf-8") as f:
                f.write("".join(out))
        except OSError as e:
            emit({"ok": False, "error": f"寫不了檔：{e}", **extra})
            return 2

    ok = not bad or reverted
    emit({"ok": ok, "round_changed_lines": len(allowed), "violations": bad, "reverted": reverted, **extra})
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
