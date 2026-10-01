"""PR 規則檢查（#140）：PR 本文要連 issue，改到的檔要落在同一個範圍。

規則：
- 規則 A：本文至少連一個 issue（`Refs #N`、`Refs: #N`、`Closes`／`Fixes`／`Resolves #N`，大小寫不拘）。
  不設豁免；連多個允許。
- 一個邏輯目的：每個改動檔照範圍表 script/github/scope.json 對到一個範圍；扣掉附屬檔後只准一個範圍。
  表上沒列到的檔算違規。
- 規則 B（epic／sub-issue）只是指引，這裡不檢查。

用法：
  python3 script/github/check_pr_rules.py --body-file <本文檔> [--files-from <改動檔清單，一行一個；- 表示 stdin>] [--table <範圍表>]

輸出一行 JSON：{"ok", "issues": [...], "scopes": [...], "problems": [...]}；全過結束碼 0，有違規 1。
本機 hook .claude/hooks/pr_rules_guard.py 與之後的 CI 都呼叫這支，不另寫一份規則。
"""
import argparse
import json
import re
import sys
from pathlib import Path

TABLE = Path(__file__).resolve().parent / "scope.json"
ISSUE_LINK = re.compile(r"(?i)\b(?:refs|closes|fixes|resolves):?\s+#(\d+)\b")


def load_table(path: Path = TABLE) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = [(re.compile(r["pattern"]), r["scope"], r.get("attach")) for r in data["rules"]]
    groups = [(g["name"], set(g["scopes"])) for g in data.get("groups", [])]
    return {"rules": rules, "groups": groups}


def linked_issues(body: str) -> list[int]:
    return sorted({int(n) for n in ISSUE_LINK.findall(body)})


def classify(path: str, table: dict):
    """回傳 (範圍, attach)；表上沒列到回傳 None。"""
    for pat, scope, attach in table["rules"]:
        m = pat.search(path)
        if m:
            return scope.format(**m.groupdict()), attach
    return None


def scopes_of(files: list[str], table: dict) -> tuple[list[str], list[str]]:
    """回傳 (範圍清單, 問題清單)。"""
    problems = []
    primary, same, anys = set(), set(), set()
    for f in files:
        c = classify(f, table)
        if c is None:
            problems.append(f"{f}：範圍表 script/github/scope.json 沒有列到這個檔，先補表")
            continue
        scope, attach = c
        {"same": same, "any": anys}.get(attach, primary).add(scope)
    primary |= same  # same：有同範圍主檔時本來就在 primary；沒有就自己算一個範圍
    if not primary:
        primary = anys
    if len(primary) > 1:
        for name, members in table["groups"]:
            if primary <= members:
                return [name], problems
        problems.append(
            "改到 " + str(len(primary)) + " 個範圍（" + "、".join(sorted(primary))
            + "），一個 PR 只做一個邏輯目的：拆成多個 PR，或在 scope.json 的 groups 說明它們為何是同一件事"
        )
    return sorted(primary), problems


def check(body: str, files: list[str], table: dict | None = None) -> dict:
    table = table or load_table()
    issues = linked_issues(body)
    problems = []
    if not issues:
        problems.append("PR 本文沒有連 issue：至少要有一行 `Refs #N`、`Refs: #N` 或 `Closes／Fixes／Resolves #N`（不設豁免）")
    scopes, scope_problems = scopes_of([f for f in files if f], table)
    problems += scope_problems
    return {"ok": not problems, "issues": issues, "scopes": scopes, "problems": problems}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="PR 規則檢查：連 issue 與一個範圍")
    p.add_argument("--body-file", required=True)
    p.add_argument("--files-from", help="改動檔清單，一行一個；- 表示 stdin")
    p.add_argument("--table", default=str(TABLE))
    a = p.parse_args(argv)
    try:
        body = Path(a.body_file).read_text(encoding="utf-8")
        if a.files_from is None:
            files = []
        elif a.files_from == "-":
            files = sys.stdin.read().splitlines()
        else:
            files = Path(a.files_from).read_text(encoding="utf-8").splitlines()
        result = check(body, [f.strip() for f in files], load_table(Path(a.table)))
    except (OSError, ValueError, KeyError) as e:
        result = {"ok": False, "issues": [], "scopes": [], "problems": [f"讀不到輸入：{e}"]}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
