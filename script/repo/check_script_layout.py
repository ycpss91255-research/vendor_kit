"""script/ 的目錄規則：依類型分子目錄。

1. script/ 頂層只准有 README.md 與子目錄，腳本不准直接放頂層。
2. 每個子目錄是一個類別，名稱只用小寫英數與連字號。
3. 每個類別底下要有 README.md。
4. 類別底下的子目錄只准有 test/。

只看 git ls-files -co --exclude-standard（追蹤中與未追蹤但沒被忽略的檔）。

用法：python3 script/repo/check_script_layout.py（有問題逐筆印出 `檔:原因` 並以 1 結束）
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATEGORY = re.compile(r"^[a-z0-9-]+$")
TOP_ALLOWED = {"README.md"}
SUBDIR_ALLOWED = {"test"}


def repo_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard"],
        check=True, capture_output=True, text=True,
    ).stdout
    # 已刪但還沒 stage 的檔不算
    return sorted({f for f in out.splitlines() if f and (root / f).exists()})


def layout_errors(files: list[str]) -> list[str]:
    """files 是相對 repo 根目錄的 posix 路徑；回傳 `檔:原因` 清單。"""
    errors = []
    categories = set()
    readmes = set()
    for f in files:
        parts = f.split("/")
        if parts[0] != "script":
            continue
        rest = parts[1:]
        if len(rest) == 1:
            if rest[0] not in TOP_ALLOWED:
                errors.append(f"{f}:script/ 頂層只准有 README.md 與子目錄，檔案要放進類別子目錄")
            continue
        cat = rest[0]
        categories.add(cat)
        if not CATEGORY.match(cat):
            errors.append(f"{f}:類別目錄名 {cat!r} 只能用小寫英數與連字號")
        if len(rest) == 2 and rest[1] == "README.md":
            readmes.add(cat)
        if len(rest) > 2 and rest[1] not in SUBDIR_ALLOWED:
            errors.append(f"{f}:類別底下的子目錄只准有 test/")
    for cat in sorted(categories - readmes):
        errors.append(f"script/{cat}/:缺 README.md")
    return errors


def main() -> int:
    errors = layout_errors(repo_files(ROOT))
    for e in errors:
        print(e)
    if errors:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
