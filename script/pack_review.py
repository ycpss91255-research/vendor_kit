#!/usr/bin/env python3
"""把送審的檔打包成 review_v<N>.zip：只打包，標示版照舊由 mark_changes.py 產生。

用法（在 repo 根目錄執行）：
  python3 script/pack_review.py [--out <目錄>] [--note <審閱說明.md>] <頁鍵> [<頁鍵> ...]

頁鍵的寫法跟 mark_changes.py 相同：審閱頁傳頁名（03_messages），其他檔傳路徑（GLOSSARY.md）。
每個鍵取 doc/decisions/_marked/ 裡 versions.json 記的那一版：
<鍵>.v<N>.marked.md、<鍵>.v<N>.md，有 <鍵>.v<N>.csv 也放進去；缺檔就停下，不取號。
zip 的版本號是 versions.json 的 review_zip 加一並寫回；zip 內檔名不帶目錄，
有 --note 時審閱說明排第一個。沒給 --out 就放在系統暫存目錄，不寫進 repo。
"""
import argparse
import json
import pathlib
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mark_changes  # noqa: E402

ZIP_KEY = "review_zip"


def key_of(name: str) -> str:
    """頁鍵 → versions.json 與 _marked/ 用的鍵（規則同 mark_changes.py）。"""
    return mark_changes.target(mark_changes.normalize(name))[1]


def collect(names: list[str]) -> list[pathlib.Path]:
    """依序列出每個鍵最新版的檔；缺版號或缺檔就丟 SystemExit。"""
    table = json.loads(mark_changes.VERSIONS.read_text()) if mark_changes.VERSIONS.exists() else {}
    files: list[pathlib.Path] = []
    errors: list[str] = []
    for name in names:
        key = key_of(name)
        if key not in table:
            errors.append(f"{name}：{mark_changes.VERSIONS} 沒有鍵 {key}")
            continue
        n = int(table[key])
        for suffix in (".marked.md", ".md"):
            path = mark_changes.MARKED / f"{key}.v{n}{suffix}"
            if path.exists():
                files.append(path)
            else:
                errors.append(f"{name}：找不到 {path}")
        csv = mark_changes.MARKED / f"{key}.v{n}.csv"
        if csv.exists():
            files.append(csv)
    if errors:
        raise SystemExit("缺檔，沒有打包：\n" + "\n".join(f"  {e}" for e in errors))
    return files


def next_zip() -> int:
    """review_zip 加一並寫回 versions.json。"""
    return mark_changes.next_rev(ZIP_KEY)


def pack(names: list[str], out: pathlib.Path, note: pathlib.Path | None = None) -> tuple[pathlib.Path, list[str]]:
    """打包並回傳（zip 路徑, zip 內檔名清單）。先檢查齊全才取號，失敗不會用掉版號。"""
    if note is not None and not note.exists():
        raise SystemExit(f"找不到審閱說明 {note}")
    files = ([note] if note is not None else []) + collect(names)
    arcnames = [f.name for f in files]
    dup = sorted({a for a in arcnames if arcnames.count(a) > 1})
    if dup:
        raise SystemExit("zip 內檔名重複：" + "、".join(dup))
    n = next_zip()
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"review_v{n}.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f, arc in zip(files, arcnames):
            zf.write(f, arc)
    return path, arcnames


def main() -> None:
    ap = argparse.ArgumentParser(description="把送審的檔打包成 review_v<N>.zip")
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
