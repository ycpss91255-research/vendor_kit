#!/usr/bin/env python3
"""把送審資料夾打包成 review_v<N>.zip，並在 doc/review/versions.json 記下這次送審。

用法（在 repo 根目錄執行）：
  python3 script/pack_review.py [--out <目錄>] [--note <審閱說明.md>] <頁鍵> [<頁鍵> ...]

頁鍵的寫法跟 mark_changes.py 相同：審閱頁傳頁名（03_messages），其他檔傳路徑（GLOSSARY.md）。
標示版照舊由 mark_changes.py 產生；這支只打包 doc/review/<鍵>/ 裡的
<鍵>.marked.md、<鍵>.md，有 <鍵>.csv 也放進去。repo 裡的檔名不帶版本號，zip 裡的檔名才帶：
<鍵>.v<N>.marked.md、<鍵>.v<N>.md、<鍵>.v<N>.csv；N 是該鍵最後送審的版號加一（從沒送審過是 1）。
zip 名是 review_v<review_zip+1>.zip；zip 內檔名不帶目錄，有 --note 時審閱說明排第一個。
沒給 --out 就放在系統暫存目錄，不寫進 repo。

送審的內容要能從 git 取回（下一輪 mark_changes.py 用 git show 當基準），所以先檢查：
正式檔（與附屬 CSV）沒有未 commit 的改動，送審資料夾的正文副本跟正式檔一致（不一致就是沒重跑
mark_changes.py）。任何一項不過或缺檔就停下，不取號、不寫 versions.json。
都過了才打包，並把 {"v": N, "commit": HEAD} 追加進各鍵的紀錄、review_zip 加一。
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mark_changes  # noqa: E402


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失敗：{proc.stderr.strip()}")
    return proc.stdout


def dirty(paths: list[pathlib.Path]) -> list[str]:
    """這些檔裡有未 commit 改動（含 staged、未追蹤）的，回傳 git status 的行。"""
    out = git("status", "--porcelain", "--untracked-files=all", "--", *[p.as_posix() for p in paths])
    return [line for line in out.splitlines() if line.strip()]


def collect(names: list[str], table: dict) -> tuple[list[tuple[pathlib.Path, str]], dict[str, int]]:
    """回傳（[(檔, zip 內檔名)], 鍵 → 這次的版號）。缺檔、未 commit、副本過期就丟 SystemExit。"""
    files: list[tuple[pathlib.Path, str]] = []
    versions: dict[str, int] = {}
    errors: list[str] = []
    for raw in names:
        name = mark_changes.resolve_base_name(raw)
        path, key = mark_changes.target(name)
        csv_path = mark_changes.companion_csv(name)
        official = [path] + ([] if csv_path is None else [csv_path])
        for line in dirty(official):
            errors.append(f"{raw}：正式檔有未 commit 的改動，先 commit 再打包：{line}")
        last = mark_changes.last_sent(key, table)
        n = (last["v"] if last else 0) + 1
        versions[key] = n
        d = mark_changes.out_dir(key)
        for suffix in (".marked.md", ".md"):
            p = d / f"{key}{suffix}"
            if p.exists():
                files.append((p, f"{key}.v{n}{suffix}"))
            else:
                errors.append(f"{raw}：找不到 {p}（先跑 mark_changes.py）")
        copy = d / f"{key}.md"
        if copy.exists() and path.exists() and \
                copy.read_text() != mark_changes.rewrite_links(path.read_text(), path, d):
            errors.append(f"{raw}：{copy} 跟 {path} 不一致，先重跑 mark_changes.py")
        csv_copy = d / f"{key}.csv"
        if csv_path is not None:
            if not csv_copy.exists():
                errors.append(f"{raw}：找不到 {csv_copy}（先跑 mark_changes.py）")
            elif csv_copy.read_bytes() != csv_path.read_bytes():
                errors.append(f"{raw}：{csv_copy} 跟 {csv_path} 不一致，先重跑 mark_changes.py")
            else:
                files.append((csv_copy, f"{key}.v{n}.csv"))
    if errors:
        raise SystemExit("沒有打包：\n" + "\n".join(f"  {e}" for e in errors))
    return files, versions


def pack(names: list[str], out: pathlib.Path, note: pathlib.Path | None = None) -> tuple[pathlib.Path, list[str]]:
    """打包並回傳（zip 路徑, zip 內檔名清單）。先檢查全部過關才取號，失敗不會用掉版號。"""
    if note is not None and not note.exists():
        raise SystemExit(f"找不到審閱說明 {note}")
    table = mark_changes.load_versions()
    files, versions = collect(names, table)
    if note is not None:
        files.insert(0, (note, note.name))
    arcnames = [arc for _, arc in files]
    dup = sorted({a for a in arcnames if arcnames.count(a) > 1})
    if dup:
        raise SystemExit("zip 內檔名重複：" + "、".join(dup))
    head = git("rev-parse", "HEAD").strip()
    n = int(table[mark_changes.ZIP_KEY]) + 1
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"review_v{n}.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f, arc in files:
            zf.write(f, arc)
    for key, v in versions.items():
        table["pages"].setdefault(key, []).append({"v": v, "commit": head})
    table[mark_changes.ZIP_KEY] = n
    mark_changes.save_versions(table)
    return path, arcnames


def main() -> None:
    ap = argparse.ArgumentParser(description="把送審資料夾打包成 review_v<N>.zip")
    ap.add_argument("--out", type=pathlib.Path, help="輸出目錄；不給就用系統暫存目錄")
    ap.add_argument("--note", type=pathlib.Path, help="審閱說明 .md，放在 zip 第一個")
    ap.add_argument("names", nargs="+", help="頁鍵，例如 03_messages 04_interface GLOSSARY.md")
    args = ap.parse_args()
    out = args.out if args.out is not None else pathlib.Path(tempfile.mkdtemp(prefix="review_"))
    path, arcnames = pack(args.names, out, args.note)
    print(path)
    for a in arcnames:
        print(f"  {a}")


if __name__ == "__main__":
    main()
