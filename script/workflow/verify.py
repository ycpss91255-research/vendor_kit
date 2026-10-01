"""在 worktree 根目錄跑完送 PR 前的全部驗證，結果寫成一行 JSON。

用法：python3 script/workflow/verify.py [--root <worktree 根目錄>] [--workflow .github/workflows/docs.yml]

依序跑：
1. docs.yml 每個 job 的每個 `run:`，原樣用 shell 在根目錄執行（單行與 `run: |` 區塊都認）。
2. 每個 `script/*/test` 目錄的 `python3 -m unittest discover -s <目錄>`；docs.yml 已經跑過同一個目錄就不重跑。
3. `python3 script/repo/check_script_layout.py`。
4. `python3 .claude/hooks/test_guard.py`：檔案存在才跑；不存在就跳過，該步標 `"skipped": true`、不算失敗
   （hooks 的測試改由 `.claude/hooks/test` 跑）。

另外檢查每個 `script/*/test` 都有出現在 docs.yml 裡（CI 跑得到），沒出現的列在 `not_in_ci`，算失敗。

--root 不給時用目前目錄所在 git worktree 的根目錄。輸出一行 JSON：
{"ok", "root", "steps": [{"source", "cmd", "code", "ok", "output"}], "not_in_ci"}；output 只留最後 40 行。
跳過的步驟另有 "skipped": true，code 是 null。
全過結束碼 0，有失敗 1，根目錄或 docs.yml 找不到 2。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TAIL = 40
RUN = re.compile(r"^(\s*)(?:-\s+)?run:\s*(.*)$")
GUARD = ".claude/hooks/test_guard.py"


def run_commands(text: str) -> list[str]:
    """從 workflow YAML 取出每個 run: 的指令（不依賴 PyYAML）。"""
    lines = text.splitlines()
    cmds = []
    i = 0
    while i < len(lines):
        m = RUN.match(lines[i])
        i += 1
        if not m:
            continue
        val = m.group(2).strip()
        if val and val[0] in "|>":
            block = []
            indent = None
            while i < len(lines):
                ln = lines[i]
                if ln.strip() == "":
                    block.append("")
                    i += 1
                    continue
                cur = len(ln) - len(ln.lstrip())
                if indent is None:
                    if cur <= len(m.group(1)):
                        break
                    indent = cur
                if cur < indent:
                    break
                block.append(ln[indent:])
                i += 1
            sep = "\n" if val[0] == "|" else " "
            cmd = sep.join(block).strip()
        else:
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
                val = val[1:-1]
            cmd = val
        if cmd:
            cmds.append(cmd)
    return cmds


def test_dirs(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.glob("script/*/test") if p.is_dir())


def covered(test_dir: str, cmds: list[str]) -> bool:
    pat = re.compile(r"(?<![\w/.-])" + re.escape(test_dir) + r"/?(?![\w/.-])")
    return any(pat.search(c) for c in cmds)


def execute(root: Path, source: str, cmd: str) -> dict:
    r = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True, executable="/bin/bash")
    out = (r.stdout + r.stderr).rstrip().splitlines()
    return {"source": source, "cmd": cmd, "code": r.returncode, "ok": r.returncode == 0,
            "output": "\n".join(out[-TAIL:])}


def git_root() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        raise FileNotFoundError("目前目錄不在 git worktree 裡，請給 --root")
    return Path(r.stdout.strip())


def verify(root: Path, workflow: str) -> dict:
    wf = root / workflow
    cmds = run_commands(wf.read_text(encoding="utf-8"))
    plan = [(workflow, c) for c in cmds]
    dirs = test_dirs(root)
    plan += [("script/*/test", f"python3 -m unittest discover -s {d}") for d in dirs if not covered(d, cmds)]
    plan += [("check_script_layout", "python3 script/repo/check_script_layout.py"),
             ("hooks test_guard", f"python3 {GUARD}")]
    seen = set()
    steps = []
    for source, cmd in plan:
        if cmd in seen:
            continue
        seen.add(cmd)
        if source == "hooks test_guard" and not (root / GUARD).is_file():
            steps.append({"source": source, "cmd": cmd, "code": None, "ok": True, "skipped": True,
                          "output": f"{GUARD} 不存在，跳過"})
            continue
        steps.append(execute(root, source, cmd))
    not_in_ci = [d for d in dirs if not covered(d, cmds)]
    return {"ok": all(s["ok"] for s in steps) and not not_in_ci, "root": str(root),
            "steps": steps, "not_in_ci": not_in_ci}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="跑送 PR 前的全部驗證")
    p.add_argument("--root", help="worktree 根目錄；不給就用目前目錄的 git 根目錄")
    p.add_argument("--workflow", default=".github/workflows/docs.yml")
    a = p.parse_args(argv)
    try:
        root = Path(a.root).resolve() if a.root else git_root()
        res = verify(root, a.workflow)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
