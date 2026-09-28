#!/usr/bin/env python3
"""guard.py 的回歸測試。

跑法：python3 .claude/hooks/test_guard.py
每個案例餵一份 PreToolUse 的 stdin JSON 給 guard.py，比對 permissionDecision。
預期 None = 放行（exit 0 無輸出）。

改 guard.py 之前先跑一次、改完再跑一次；新擋一種情況就補一個案例。
"""

import json
import subprocess
import sys
from pathlib import Path

GUARD = str(Path(__file__).parent / "guard.py")

SCRIPT_OK = """export const meta = {
  name: 'x',
  description: '測試用',
  phases: [{ title: '一' }],
}
const ASK = `規則：禁止 Date.now()、Math.random()、無參數 new Date()。
interface spec 那份文件不要再引用。as const 也不要用。`
phase('一')
await agent(ASK, { phase: '一' })
"""

SCRIPT_REAL_RANDOM = """export const meta = { name: 'x', description: 'y' }
const pick = Math.random()
await agent('x')
"""

SCRIPT_META_INTERP = """const N = 3
export const meta = { name: `x-${N}`, description: 'y' }
"""

SCRIPT_BLOCK_COMMENT = """/* 這份腳本的用途說明
   跨兩行 */
export const meta = { name: 'x', description: 'y' }
await agent('x')
"""

HEREDOC_DOC = """cat > note.md <<'EOF'
呼叫方式：codex exec --skip-git-repo-check -C <dir> -o <out.md> "<brief>" < /dev/null
不要自己加 --sandbox，會讓 bubblewrap 失敗。
EOF"""

HEREDOC_THEN_REAL = """cat > a.md <<'EOF'
說明文字
EOF
codex exec --skip-git-repo-check -C /x -o /y.md "brief\""""

CASES = [
    # (說明, tool_name, tool_input, 預期)
    ("Workflow 帶 name", "Workflow", {"name": "doc-apply", "args": {}}, None),
    ("Workflow 帶 scriptPath", "Workflow", {"scriptPath": "/tmp/x.js"}, None),
    ("inline script、乾淨", "Workflow", {"script": SCRIPT_OK}, "ask"),
    ("prompt 字串裡有禁用 API 與 TS 詞", "Workflow", {"script": SCRIPT_OK}, "ask"),
    ("程式碼真的呼叫 Math.random()", "Workflow", {"script": SCRIPT_REAL_RANDOM}, "deny"),
    ("meta 有模板插值", "Workflow", {"script": SCRIPT_META_INTERP}, "deny"),
    ("開頭是區塊註解", "Workflow", {"script": SCRIPT_BLOCK_COMMENT}, "ask"),
    ("codex 帶 < /dev/null", "Bash",
     {"command": 'codex exec --skip-git-repo-check -C /x -o /y.md "b" < /dev/null'}, None),
    ("codex 無重導", "Bash",
     {"command": 'codex exec --skip-git-repo-check -C /x -o /y.md "b"'}, "deny"),
    ("codex brief 裡有角括號、無重導", "Bash",
     {"command": 'codex exec -C /x -o /y.md "說明裡有 <repo> 這種角括號"'}, "deny"),
    ("codex brief 裡提到沙箱旗標、有重導", "Bash",
     {"command": 'codex exec -C /x -o /y.md "brief 提到 --sandbox 這個旗標" < /dev/null'}, None),
    ("codex 輸出接 pipe、無重導", "Bash",
     {"command": 'codex exec -C /x -o /y.md "b" | tee /z.log'}, "deny"),
    ("pipe 餵進 codex", "Bash",
     {"command": 'printf %s "$brief" | codex exec -C /x -o /y.md'}, None),
    ("重導到變數檔", "Bash",
     {"command": 'codex exec -C /x -o /y.md "b" < "$tmp"'}, None),
    ("heredoc 是文件內容", "Bash", {"command": HEREDOC_DOC}, None),
    ("heredoc 之後真的跑 codex、無重導", "Bash", {"command": HEREDOC_THEN_REAL}, "deny"),
    ("引號內提到 codex exec", "Bash",
     {"command": 'printf %s "說明：codex exec 要帶重導" > note.txt'}, None),
    ("|| 不是 pipe", "Bash",
     {"command": 'test -f a || codex exec -C /x -o /y.md "b"'}, "deny"),
    ("與 codex 無關的指令", "Bash", {"command": "ls -la"}, None),
    # 第 7 條：git commit / git push
    # commit 與 push 本身不攔；只有目標是 main 的 push 要擋（進 main 走 merge）
    ("git commit -m x", "Bash", {"command": 'git commit -m "x"'}, None),
    ("git commit --amend", "Bash", {"command": "git commit --amend --no-edit"}, None),
    ("git add && git commit", "Bash", {"command": 'git add -A && git commit -m "x"'}, None),
    ("push 到分支", "Bash", {"command": "git push -u origin docs/contract-and-adr"}, None),
    ("push origin main", "Bash", {"command": "git push origin main"}, "deny"),
    ("push HEAD:main", "Bash", {"command": "git push origin HEAD:main"}, "deny"),
    ("force push main", "Bash", {"command": "git push --force origin main"}, "deny"),
    ("force-with-lease 到 main", "Bash",
     {"command": "git push --force-with-lease origin main"}, "deny"),
    ("push refs/heads/main", "Bash", {"command": "git push origin refs/heads/main"}, "deny"),
    ("文件裡寫 push origin main", "Bash",
     {"command": 'printf %s "範例：git push origin main" > note.txt'}, None),
    ("git log", "Bash", {"command": 'git log --oneline -5'}, None),
]


def run(tool_name, tool_input):
    payload = json.dumps({
        "hook_event_name": "PreToolUse",
        "tool_name": tool_name,
        "tool_input": tool_input,
    })
    proc = subprocess.run([sys.executable, GUARD], input=payload,
                          capture_output=True, text=True, timeout=20)
    if not proc.stdout.strip():
        return None
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return "輸出不是合法 JSON"
    return out.get("hookSpecificOutput", {}).get("permissionDecision")


def main():
    failed = []
    for desc, tool, ti, want in CASES:
        got = run(tool, ti)
        ok = got == want
        print(f"{'PASS' if ok else 'FAIL'}  {desc}：預期 {want}，實得 {got}")
        if not ok:
            failed.append(desc)

    # 裸 git push 推的是當前分支：在 main 上就等於推 main
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    want = "deny" if branch == "main" else None
    got = run("Bash", {"command": "git push"})
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  裸 git push（目前在 {branch}）：預期 {want}，實得 {got}")
    if not ok:
        failed.append("裸 git push")

    # 壞 JSON 不能擋住工具
    proc = subprocess.run([sys.executable, GUARD], input="{ 壞掉",
                          capture_output=True, text=True, timeout=20)
    ok = proc.returncode == 0 and not proc.stdout.strip()
    print(f"{'PASS' if ok else 'FAIL'}  壞 JSON 放行：exit {proc.returncode}")
    if not ok:
        failed.append("壞 JSON")

    print(f"\n{len(CASES) + 2 - len(failed)}/{len(CASES) + 2} 通過")
    if failed:
        print("失敗：" + "、".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
