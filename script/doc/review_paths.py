#!/usr/bin/env python3
"""列出送審副本的本機路徑與版本表、列出送審 zip 的內容（給 review-pack workflow 用）。

用法：
  python3 script/doc/review_paths.py pages --repo <repo> <頁鍵> [<頁鍵> ...]
  python3 script/doc/review_paths.py zip <zip 檔>

頁鍵的寫法跟 mark_changes.py、pack_review.py 相同（03_output、GLOSSARY.md、GLOSSARY 都可以）。
鍵、送審資料夾、附屬 CSV、版號與基準一律呼叫 mark_changes.py 的函式算，不另寫規則。

pages：在 --repo 讀 doc/review/versions.json 與 doc/review/<鍵>/，印一行 JSON：
  {"ok", "repo", "versions", "zip_next", "pages", "dirty", "error"}
  zip_next：這次打包會用的 zip 號（review_zip＋1，跟 pack_review.py 同一套）。
  pages：每個頁鍵一筆 {"name", "key", "dir", "rel_dir", "files", "version", "base"}；
    dir 是送審資料夾的絕對路徑、rel_dir 是相對 repo 的路徑（給 commit_push.py --add），
    files 是資料夾裡的 .md、.marked.md、.csv 的絕對路徑（排序過），
    version 是這次打包的版號（該鍵最後送審的版號＋1，從沒送審過是 1），
    base 是 mark_changes.py 預設的基準 {"kind", "v"}：kind 是 finalized（定案版）、
    replied（維護者最後回覆的版本）或 none（沒有基準、整份標新增），none 時 v 是 null。
  dirty：送審資料夾裡有未 commit 改動（含未追蹤）的 git status --porcelain 行。
  版號與基準要在 pack_review.py 打包之前取：打包會追加這一版的紀錄並清掉 finalized。

zip：印一行 JSON {"ok", "zip", "files", "error"}，files 是 zip 內的檔名（照 zip 內順序）。

結束碼：成功 0；檔案或資料有錯 1（JSON 的 ok 是 false、error 寫原因）；用法錯 2。
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mark_changes  # noqa: E402

SUFFIXES = (".md", ".csv")


def base_of(key: str, table: dict) -> dict:
    """mark_changes.base_entry 不帶版號時選的基準：定案版優先，其次最後回覆的版本。"""
    final = mark_changes.finalized(key, table)
    if final is not None:
        return {"kind": "finalized", "v": final["v"]}
    replied = mark_changes.last_replied(key, table)
    if replied is not None:
        return {"kind": "replied", "v": replied["v"]}
    return {"kind": "none", "v": None}


def pages(repo: pathlib.Path, names: list[str]) -> dict:
    """在 repo 算每個頁鍵的送審資料夾、檔案、版號與基準。"""
    repo = repo.resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"{repo} 不是 git repo 的根目錄")
    cwd = os.getcwd()
    os.chdir(repo)  # mark_changes 的路徑都相對 repo 根目錄
    try:
        table = mark_changes.load_versions()
        rows, rel_dirs = [], []
        for raw in names:
            name = mark_changes.resolve_base_name(raw)
            _, key = mark_changes.target(name)
            rel = mark_changes.out_dir(key)
            d = repo / rel
            files = sorted(str(p) for p in d.iterdir() if p.is_file() and p.suffix in SUFFIXES) if d.is_dir() else []
            last = mark_changes.last_sent(key, table)
            rows.append({
                "name": raw, "key": key, "dir": str(d), "rel_dir": rel.as_posix(), "files": files,
                "version": (last["v"] if last else 0) + 1, "base": base_of(key, table),
            })
            rel_dirs.append(rel.as_posix())
        proc = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", *rel_dirs],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise ValueError(f"git status 失敗：{proc.stderr.strip()}")
        dirty = [line for line in proc.stdout.splitlines() if line.strip()]
        return {
            "ok": True, "repo": str(repo), "versions": str(repo / mark_changes.VERSIONS),
            "zip_next": int(table[mark_changes.ZIP_KEY]) + 1, "pages": rows, "dirty": dirty, "error": None,
        }
    finally:
        os.chdir(cwd)


def zip_files(path: pathlib.Path) -> dict:
    """zip 內的檔名清單。"""
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"找不到 {path}")
    with zipfile.ZipFile(path) as zf:
        return {"ok": True, "zip": str(path), "files": zf.namelist(), "error": None}


def main() -> int:
    ap = argparse.ArgumentParser(description="列出送審副本路徑與版本表、送審 zip 的內容")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pages", help="送審副本的路徑、版號與基準")
    p.add_argument("--repo", required=True, type=pathlib.Path, help="repo（或 worktree）根目錄")
    p.add_argument("names", nargs="+", help="頁鍵，例如 03_output 04_interface GLOSSARY.md")
    z = sub.add_parser("zip", help="zip 內的檔名")
    z.add_argument("zip", type=pathlib.Path)
    args = ap.parse_args()
    try:
        out = pages(args.repo, args.names) if args.cmd == "pages" else zip_files(args.zip)
    except (ValueError, OSError, zipfile.BadZipFile, json.JSONDecodeError, KeyError) as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
