"""ask_guard、decision_guard、contract_edit_guard 的測試：用 subprocess 餵 PreToolUse 的 JSON，看輸出。

對外文件的路徑要同時認 main 現在的 doc/decisions/review/ 與之後的 doc/contract/，不認舊的 docs/。
跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1]


def run(hook: str, tool: str, tool_input: dict) -> dict:
    out = subprocess.run(
        [sys.executable, str(HOOKS / hook)],
        input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return json.loads(out)["hookSpecificOutput"] if out else {}


# 會被 decision_guard 擋的內容；拆開組，免得本檔自己被 hook 擋
DATE = "-".join(["2026", "01", "01"]) + " 定案"
QUOTE = "維護者" + "：" + "「" + "好」"
MARK = "已確認" + "："


class AskGuardTest(unittest.TestCase):
    def ask(self, *questions: str) -> dict:
        qs = [{"header": f"Q{i}", "question": q} for i, q in enumerate(questions)]
        return run("ask_guard.py", "AskUserQuestion", {"questions": qs})

    def test_allows_with_mark(self):
        self.assertEqual(self.ask(f"要哪個？\n{MARK}codex 討論見 #1；對照過 ADR 0001"), {})

    def test_denies_without_mark(self):
        out = self.ask(f"A？\n{MARK}x", "B？")
        self.assertEqual(out.get("permissionDecision"), "deny")
        self.assertIn("Q1", out["permissionDecisionReason"])
        self.assertNotIn("Q0", out["permissionDecisionReason"])

    def test_ignores_other_tools(self):
        self.assertEqual(run("ask_guard.py", "Bash", {"command": "ls"}), {})


class DecisionGuardTest(unittest.TestCase):
    """主 repo 與 linked worktree 用 tmp 目錄假造；repo 外的 scratchpad 也放在 tmp 底下。"""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name).resolve()
        cls.src = base / "src"
        cls.src.mkdir()
        subprocess.run(["git", "init", "-q", str(cls.src)], check=True)
        (cls.src / ".gitignore").write_text("doc/research/\n")
        cls.wt = base / "worktree" / "pr" / "1"
        (cls.src / ".git" / "worktrees" / "1").mkdir(parents=True)
        cls.wt.mkdir(parents=True)
        (cls.wt / ".git").write_text(f"gitdir: {cls.src}/.git/worktrees/1\n")
        cls.scratch = base / "scratchpad" / "pr" / "1-x"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_guard(self, tool: str, tool_input: dict) -> dict:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.src))
        payload = {"tool_name": tool, "tool_input": tool_input, "cwd": str(self.src)}
        out = subprocess.run(
            [sys.executable, str(HOOKS / "decision_guard.py")], input=json.dumps(payload),
            capture_output=True, text=True, env=env, check=True,
        ).stdout.strip()
        return json.loads(out)["hookSpecificOutput"] if out else {}

    def write(self, path, content: str = DATE) -> dict:
        return self.run_guard("Write", {"file_path": str(path), "content": content})

    def test_allows_contract_pages_current_and_future(self):
        for p in (self.src / "doc/decisions/review/01_purpose.md", self.src / "doc/contract/01_purpose.md",
                  "doc/decisions/review/02_invariants.md"):
            self.assertEqual(self.write(p), {}, p)

    def test_allows_adr_and_readme(self):
        self.assertEqual(self.write(self.src / "doc/adr/0001-x.md"), {})
        self.assertEqual(self.write(self.src / "README.md"), {})

    def test_denies_old_docs_paths(self):
        for p in (self.src / "docs/contract/01_purpose.md", self.src / "docs/adr/0001-x.md"):
            self.assertEqual(self.write(p).get("permissionDecision"), "deny", p)

    def test_denies_other_doc(self):
        for p in (self.src / "doc/agents/domain.md", self.src / "doc/decisions/scope_roadmap.md",
                  "doc/agents/domain.md"):
            self.assertEqual(self.write(p).get("permissionDecision"), "deny", p)

    def test_denies_in_linked_worktree(self):
        self.assertEqual(self.write(self.wt / "doc/agents/domain.md").get("permissionDecision"), "deny")

    def test_denies_quote(self):
        out = self.write(self.src / "doc/agents/domain.md", QUOTE)
        self.assertEqual(out.get("permissionDecision"), "deny")

    def test_allows_plain_text(self):
        self.assertEqual(self.write(self.src / "doc/agents/domain.md", "維護者回覆定案才 merge"), {})

    def test_allows_outside_repo(self):
        for p in (self.scratch / "comment.md", self.src.parent / "reference" / "x.md"):
            self.assertEqual(self.write(p, f"{DATE}\n{QUOTE}"), {}, p)

    def test_allows_gitignored_artifacts(self):
        self.assertEqual(self.write(self.src / "doc/research/x.md"), {})

    def test_edit_checks_new_string(self):
        out = self.run_guard("Edit", {"file_path": str(self.src / "doc/agents/domain.md"),
                                      "old_string": "a", "new_string": DATE})
        self.assertEqual(out.get("permissionDecision"), "deny")


class ContractEditGuardTest(unittest.TestCase):
    def edit(self, path: str) -> dict:
        return run("contract_edit_guard.py", "Edit", {"file_path": path, "new_string": "x"})

    def test_reminds_on_contract_page_current_and_future(self):
        for p in ("/r/doc/decisions/review/01_purpose.md", "/r/doc/contract/04_interface.md"):
            self.assertIn(p, self.edit(p).get("additionalContext", ""), p)

    def test_reminds_on_readme_and_glossary(self):
        for p in ("/r/README.md", "/r/GLOSSARY.md"):
            self.assertIn(p, self.edit(p).get("additionalContext", ""), p)

    def test_skips_review_readme(self):
        for p in ("/r/doc/contract/README.md", "doc/contract/README.md",
                  "/r/doc/decisions/review/README.md"):
            self.assertEqual(self.edit(p), {}, p)

    def test_ignores_old_docs_path_and_internal_doc(self):
        for p in ("/r/docs/contract/04_interface.md", "/r/doc/decisions/scope_roadmap.md"):
            self.assertEqual(self.edit(p), {}, p)


if __name__ == "__main__":
    unittest.main()
