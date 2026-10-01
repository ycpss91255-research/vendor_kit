"""ask_guard、decision_guard、contract_edit_guard 的測試：用 subprocess 餵 PreToolUse 的 JSON，看輸出。

對外文件的路徑要同時認 main 現在的 doc/decisions/review/ 與之後的 doc/contract/，不認舊的 docs/。
跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
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
    def write(self, path: str, content: str = DATE) -> dict:
        return run("decision_guard.py", "Write", {"file_path": path, "content": content})

    def test_allows_contract_pages_current_and_future(self):
        for p in ("/r/doc/decisions/review/01_purpose.md", "/r/doc/contract/01_purpose.md",
                  "doc/decisions/review/02_invariants.md"):
            self.assertEqual(self.write(p), {}, p)

    def test_allows_adr_and_readme(self):
        self.assertEqual(self.write("/r/doc/adr/0001-x.md"), {})
        self.assertEqual(self.write("/r/README.md"), {})

    def test_denies_old_docs_paths(self):
        for p in ("/r/docs/contract/01_purpose.md", "/r/docs/adr/0001-x.md"):
            self.assertEqual(self.write(p).get("permissionDecision"), "deny", p)

    def test_denies_other_doc(self):
        self.assertEqual(self.write("/r/doc/agents/domain.md").get("permissionDecision"), "deny")
        self.assertEqual(self.write("/r/doc/decisions/scope_roadmap.md").get("permissionDecision"), "deny")

    def test_denies_quote(self):
        self.assertEqual(self.write("/r/doc/agents/domain.md", QUOTE).get("permissionDecision"), "deny")

    def test_allows_plain_text(self):
        self.assertEqual(self.write("/r/doc/agents/domain.md", "維護者回覆定案才 merge"), {})

    def test_edit_checks_new_string(self):
        out = run("decision_guard.py", "Edit",
                  {"file_path": "/r/doc/agents/domain.md", "old_string": "a", "new_string": DATE})
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
