#!/usr/bin/env python3
"""repo 追蹤的檔案不准有本機絕對路徑（#236、#255）。

本機絕對路徑對其他人沒用（別人的機器上不存在），還會洩漏使用者名稱與本機目錄結構。

規則：直接載入 .claude/hooks/comment_tag_guard.py 的 LOCAL_PATHS，不另抄一份；hook 改了，
這支自動跟著變。用 importlib 載 hook 檔本身，不 import script/workflow/hook_rules.py：
那樣 script/repo 會依賴另一個類別，而兩者載入的是同一份 hook，結果一樣。

範圍：git ls-files 列出的檔（只看追蹤中的）。符號連結、已刪未 stage 的檔、
二進位檔（含 NUL 位元組或不是 UTF-8）跳過。

白名單：資料檔 script/repo/local_paths_allow.json，以檔為單位，每條 path 與 reason。
白名單上的檔若已經掃不到本機路徑（或檔不見了），算過時，一樣以 1 結束，提醒把那條刪掉。
白名單放資料檔、不寫在腳本內：它是附屬檔（scope.json 設 attach any），修好被放行的檔時
可以在同一個 PR 刪掉那條，不必連腳本一起改而跨兩個範圍（#264）。

用法：python3 script/repo/check_local_paths.py [--root <repo 根目錄>]

輸出一行 JSON：
  {"ok": true|false, "hits": [{"file", "line", "rule"}...], "stale_allow": [檔...]}
rule 是 LOCAL_PATHS 每條樣式附的標籤。有 hits 或 stale_allow 時以 1 結束；
載不到 hook 規則或白名單檔時印 {"ok": false, "error": ...} 並以 2 結束。
"""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = Path(".claude/hooks/comment_tag_guard.py")

ALLOW_FILE = Path("script/repo/local_paths_allow.json")


def load_allow(root: Path) -> dict[str, str]:
    """讀 ALLOW_FILE，回傳 {檔: 理由}；檔不見、格式錯、缺理由或重複就 raise RuntimeError。"""
    path = root / ALLOW_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RuntimeError(f"找不到白名單檔：{ALLOW_FILE}") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"白名單檔讀不了：{ALLOW_FILE}：{e}") from e
    entries = data.get("allow") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise RuntimeError(f"白名單檔 {ALLOW_FILE} 要有 allow 清單")
    allow: dict[str, str] = {}
    for i, entry in enumerate(entries):
        f = entry.get("path") if isinstance(entry, dict) else None
        why = entry.get("reason") if isinstance(entry, dict) else None
        if not isinstance(f, str) or not f.strip() or not isinstance(why, str) or not why.strip():
            raise RuntimeError(f"白名單檔 {ALLOW_FILE} 第 {i + 1} 條要有非空的 path 與 reason")
        if f in allow:
            raise RuntimeError(f"白名單檔 {ALLOW_FILE} 重複列了 {f}")
        allow[f] = why
    return allow


def load_rules(root: Path):
    """回傳 hook 的 LOCAL_PATHS；載不到就 raise RuntimeError。"""
    path = root / HOOK
    if not path.is_file():
        raise RuntimeError(f"找不到 hook 檔：{HOOK}")
    spec = importlib.util.spec_from_file_location("comment_tag_guard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入 hook 檔：{HOOK}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001 — 任何載入錯誤都換成同一種例外
        raise RuntimeError(f"載入 hook 檔失敗：{HOOK}：{e}") from e
    if not hasattr(mod, "LOCAL_PATHS"):
        raise RuntimeError(f"hook 檔 {HOOK} 缺少 LOCAL_PATHS")
    return mod.LOCAL_PATHS


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True, capture_output=True, text=True,
    ).stdout
    return sorted(f for f in out.split("\0") if f)


def read_text(path: Path) -> str | None:
    """文字檔回傳內容；符號連結、不存在、二進位（含 NUL 或不是 UTF-8）回傳 None。"""
    if path.is_symlink() or not path.is_file():
        return None
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_text(text: str, rules) -> list[tuple[int, str]]:
    """回傳 [(行號, 規則標籤)]；同一行比到多條規則就各記一筆。"""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for pat, label in rules:
            if pat.search(line):
                hits.append((n, label))
    return hits


def check(root: Path, rules, files: list[str], allow: dict[str, str]) -> dict:
    hits, allowed_hit = [], set()
    for f in files:
        text = read_text(root / f)
        if text is None:
            continue
        found = scan_text(text, rules)
        if not found:
            continue
        if f in allow:
            allowed_hit.add(f)
            continue
        hits += [{"file": f, "line": n, "rule": label} for n, label in found]
    stale = sorted(set(allow) - allowed_hit)
    return {"ok": not hits and not stale, "hits": hits, "stale_allow": stale}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="repo 追蹤的檔案不准有本機絕對路徑")
    ap.add_argument("--root", type=Path, default=ROOT, help="repo 根目錄（預設：這支腳本所在的 repo）")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    try:
        rules = load_rules(root)
        allow = load_allow(root)
    except RuntimeError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    result = check(root, rules, tracked_files(root), allow)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
