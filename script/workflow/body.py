"""issue／PR 本文檔的自檢（不呼叫 gh，只讀檔）。

用法：
  python3 script/workflow/body.py check <file> --kind issue --parent <N>
  python3 script/workflow/body.py check <file> --kind pr --issue <N>

檢查：
- issue：第一行是 `Part of #<parent>`。
- pr：第一行以 `[claude] ` 開頭，且本文有一行 `Closes #<issue>`。
- 兩者：不是空檔；不含本機絕對路徑（/home/<user>/、/Users/<user>/、/tmp/claude-、C:\\Users\\）。
  規則直接取自 .claude/hooks/comment_tag_guard.py（經 hook_rules.py 載入 LOCAL_PATHS），不另抄一份。

輸出一行 JSON：{"ok", "file", "kind", "problems": [...]}；全過結束碼 0，有問題 1。
"""
import argparse
import json
import sys
from pathlib import Path

from hook_rules import LOCAL_PATHS


def problems(text: str, kind: str, parent=None, issue=None) -> list[str]:
    out = []
    if not text.strip():
        return ["本文是空的"]
    lines = text.splitlines()
    first = lines[0]
    if kind == "issue":
        want = f"Part of #{parent}"
        if first.strip() != want:
            out.append(f"第一行要是 `{want}`，現在是 `{first}`")
    else:
        if not first.startswith("[claude] "):
            out.append(f"第一行要以 `[claude] ` 開頭，現在是 `{first}`")
        want = f"Closes #{issue}"
        if not any(l.strip() == want for l in lines):
            out.append(f"缺一行 `{want}`")
    for no, line in enumerate(lines, 1):
        for pat, label in LOCAL_PATHS:
            if pat.search(line):
                out.append(f"第 {no} 行有本機絕對路徑（{label}）")
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="issue／PR 本文檔自檢")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--kind", choices=["issue", "pr"], required=True)
    c.add_argument("--parent", type=int, help="issue 的父題編號")
    c.add_argument("--issue", type=int, help="PR 要關的 issue 編號")
    a = p.parse_args(argv)
    if a.kind == "issue" and a.parent is None:
        p.error("--kind issue 要給 --parent")
    if a.kind == "pr" and a.issue is None:
        p.error("--kind pr 要給 --issue")
    path = Path(a.file)
    try:
        text = path.read_text(encoding="utf-8")
        probs = problems(text, a.kind, a.parent, a.issue)
    except OSError as e:
        probs = [f"讀不到檔：{e}"]
    print(json.dumps({"ok": not probs, "file": str(path), "kind": a.kind, "problems": probs}, ensure_ascii=False))
    return 0 if not probs else 1


if __name__ == "__main__":
    sys.exit(main())
