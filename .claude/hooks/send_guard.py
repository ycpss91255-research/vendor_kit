#!/usr/bin/env python3
"""PreToolUse hook（matcher: SendUserFile）：送審不准傳沒帶版本號的檔。

對外文件（根目錄 README.md、審閱頁 doc/decisions/review/0N_*.md，以及搬家後的
doc/contract/0N_*.md）送審時，要傳 script/doc/pack_review.py 打包的 review_v<N>.zip：
zip 裡的檔名才帶版本號（<鍵>.v<N>.md、<鍵>.v<N>.marked.md）。正式檔與送審資料夾
doc/review/<鍵>/ 裡的副本檔名都不帶版本號，維護者要打開檔案才知道是哪一版，所以一律擋下。
流程見 script/doc/README.md「對外文件的改動標示」與「送審打包」。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

FORMAL = re.compile(r"^(README\.md|doc/(decisions/review|contract)/0\d_[^/]+\.(md|csv))$")
REVIEW_COPY = re.compile(r"^doc/review/[^/]+/[^/]+\.(md|csv)$")
VERSIONED = re.compile(r"\.v\d+\.[^/]+$")


def repo_relative(path: str) -> str:
    """絕對路徑換成它所在 git repo（含 worktree）的相對路徑；相對路徑照原樣。"""
    p = Path(path)
    if not p.is_absolute():
        return p.as_posix().removeprefix("./")
    try:
        top = subprocess.run(
            ["git", "-C", str(p.parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return p.resolve().relative_to(Path(top).resolve()).as_posix()
    except Exception:
        return p.as_posix()


def requested_files(tool_input: dict) -> list[str]:
    files = tool_input.get("files") or []
    if isinstance(files, str):
        files = [files]
    for key in ("file", "file_path", "path"):
        if isinstance(tool_input.get(key), str):
            files.append(tool_input[key])
    return [str(f.get("path") if isinstance(f, dict) else f) for f in files]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "SendUserFile":
        return 0
    bad = []
    for f in requested_files(data.get("tool_input") or {}):
        rel = repo_relative(f)
        if VERSIONED.search(rel):
            continue  # 檔名帶版本號
        if FORMAL.match(rel) or REVIEW_COPY.match(rel):
            bad.append(f)
    if not bad:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "送審要傳檔名帶版本號的檔，不傳正式檔或 doc/review/ 裡不帶版本號的副本："
            + "、".join(bad) + "。先跑 script/doc/mark_changes.py 產標示版，"
            "再跑 script/doc/pack_review.py --out <目錄> <鍵…> 打包，改傳產出的 review_v<N>.zip"
            "（zip 裡是 <鍵>.v<N>.md 與 <鍵>.v<N>.marked.md）。"
            "流程見 script/doc/README.md「對外文件的改動標示」與「送審打包」。"
        ),
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
