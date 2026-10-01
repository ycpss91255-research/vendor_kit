#!/usr/bin/env python3
"""repo 追蹤的檔案不准有本機絕對路徑（#236、#255）。

本機絕對路徑對其他人沒用（別人的機器上不存在），還會洩漏使用者名稱與本機目錄結構。

規則：直接載入 .claude/hooks/comment_tag_guard.py 的 LOCAL_PATHS，不另抄一份；hook 改了，
這支自動跟著變。用 importlib 載 hook 檔本身，不 import script/workflow/hook_rules.py：
那樣 script/repo 會依賴另一個類別，而兩者載入的是同一份 hook，結果一樣。

範圍：git ls-files 列出的檔（只看追蹤中的）。符號連結、已刪未 stage 的檔、
二進位檔（含 NUL 位元組或不是 UTF-8）跳過。

白名單：ALLOW，以檔為單位，每條寫理由。白名單上的檔若已經掃不到本機路徑（或檔不見了），
算過時，一樣以 1 結束，提醒把那條刪掉。

用法：python3 script/repo/check_local_paths.py [--root <repo 根目錄>]

輸出一行 JSON：
  {"ok": true|false, "hits": [{"file", "line", "rule"}...], "stale_allow": [檔...]}
rule 是 LOCAL_PATHS 每條樣式附的標籤。有 hits 或 stale_allow 時以 1 結束；
載不到 hook 規則時印 {"ok": false, "error": ...} 並以 2 結束。
"""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = Path(".claude/hooks/comment_tag_guard.py")

# 檔 → 理由。只放「這個檔必須寫出樣式」或「這個 PR 不能改、另開 issue 處理」的檔。
ALLOW = {
    ".claude/hooks/comment_tag_guard.py":
        "LOCAL_PATHS 的定義本身，以及擋下時給使用者看的說明，必須寫出要擋的樣式",
    "script/workflow/prepare_comment.py":
        "REPLACE 是把本機路徑改寫成相對寫法的替換樣式，必須寫出同樣的路徑前綴",
    "script/workflow/body.py":
        "docstring 列出自檢擋哪些樣式（用 <user> 佔位），不是真路徑",
    ".claude/hooks/test/test_comment_tag_guard.py":
        "hook 測試資料刻意含本機路徑；改成拆字串寫法要動 hook 範圍，不在 #255（一個 PR 一類範圍），改完刪這條",
    "script/workflow/test/test_body.py":
        "body.py 測試資料刻意含本機路徑，部分還沒拆字串；改要動 script/workflow 範圍，不在 #255，改完刪這條",
    ".codex/config.toml":
        "真違規：drawio MCP 路徑寫死本機 npx 快取，另開 #257 修，修完刪這條",
}


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
    except RuntimeError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    result = check(root, rules, tracked_files(root), ALLOW)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
