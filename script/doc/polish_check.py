#!/usr/bin/env python3
"""潤稿越界檢查：潤稿只准改這一輪改過的行，落在範圍外的變動找出來，可選擇還原。

範圍是「這一輪的基準 → 潤稿前」的新增或修改行（difflib 的 replace／insert 落在潤稿前的行）。
比對「潤稿前 → 潤稿後」：
- 等長的 replace 逐行判斷，每一行都要在範圍內；
- 其他變動整段判斷，整段都要在範圍內；純插入（潤稿前沒有對應行）只要緊鄰的前一行或後一行在範圍內就保留。
不在範圍內的變動記進 violations；帶 --fix 時把那些段還原成潤稿前的原文，寫回 <潤稿後>。

用法：
    python3 script/doc/polish_check.py <基準> <潤稿前> <潤稿後> [--fix]

輸出（stdout 一行 JSON）：
    {"ok": bool, "round_changed_lines": int, "violations": [...], "reverted": bool}
    violations 每筆 {"pre_lines": [起, 迄], "post_lines": [起, 迄], "post_text": "..."}，
    行號從 1 起算、迄為含；純插入或純刪除時起比迄大 1。
    ok 為 true：沒有越界，或越界已用 --fix 還原。
    讀不到或寫不了檔：{"ok": false, "error": "..."}。

結束碼：
    0  沒有越界；或有越界且已 --fix 還原
    1  有越界、沒有還原
    2  讀不到檔（或 --fix 寫不了檔）
"""
import argparse
import difflib
import json
import sys


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines(keepends=True)


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
    ap = argparse.ArgumentParser(description="潤稿越界檢查：找出（並可還原）落在這一輪改動範圍外的潤稿變動")
    ap.add_argument("base", help="這一輪的基準（這一輪改之前的原檔）")
    ap.add_argument("pre", help="潤稿前的備份")
    ap.add_argument("post", help="潤稿後的檔（--fix 時就地還原）")
    ap.add_argument("--fix", action="store_true", help="把越界的變動還原成潤稿前的原文")
    args = ap.parse_args(argv)

    try:
        base, pre, cur = (read_lines(p) for p in (args.base, args.pre, args.post))
    except (OSError, UnicodeDecodeError) as e:
        emit({"ok": False, "error": f"讀不到檔：{e}"})
        return 2

    allowed, bad, out = check(base, pre, cur)
    reverted = bool(args.fix and bad)
    if reverted:
        try:
            with open(args.post, "w", encoding="utf-8") as f:
                f.write("".join(out))
        except OSError as e:
            emit({"ok": False, "error": f"寫不了檔：{e}"})
            return 2

    ok = not bad or reverted
    emit({"ok": ok, "round_changed_lines": len(allowed), "violations": bad, "reverted": reverted})
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
