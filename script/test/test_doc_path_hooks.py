"""decision_guard、contract_edit_guard、send_guard 的路徑測試：只認 doc/，不認 docs/。

用 subprocess 餵 PreToolUse 的 JSON，看輸出。
跑法：python3 -m unittest discover -s script/test
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[2] / ".claude" / "hooks"


def run(hook: str, tool: str, tool_input: dict) -> dict:
    out = subprocess.run(
        [sys.executable, str(HOOKS / hook)],
        input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return json.loads(out)["hookSpecificOutput"] if out else {}


# 會被 decision_guard 擋的內容（日期）；拆開組，免得本檔自己被 hook 擋
DECISION = "-".join(["2026", "01", "01"]) + " 定案"


class DecisionGuardTest(unittest.TestCase):
    def write(self, path: str) -> dict:
        return run("decision_guard.py", "Write", {"file_path": path, "content": DECISION})

    def test_allows_contract_page(self):
        self.assertEqual(self.write("/r/doc/contract/01_purpose.md"), {})

    def test_allows_adr(self):
        self.assertEqual(self.write("/r/doc/adr/0001-x.md"), {})

    def test_denies_old_docs_paths(self):
        for p in ("/r/docs/contract/01_purpose.md", "/r/docs/adr/0001-x.md"):
            self.assertEqual(self.write(p).get("permissionDecision"), "deny", p)

    def test_denies_other_doc(self):
        self.assertEqual(self.write("/r/doc/agents/domain.md").get("permissionDecision"), "deny")


class ContractEditGuardTest(unittest.TestCase):
    def edit(self, path: str) -> dict:
        return run("contract_edit_guard.py", "Edit", {"file_path": path, "new_string": "x"})

    def test_reminds_on_contract_page(self):
        out = self.edit("/r/doc/contract/04_interface.md")
        self.assertIn("doc/contract/04_interface.md", out.get("additionalContext", ""))

    def test_skips_review_readme(self):
        self.assertEqual(self.edit("/r/doc/contract/README.md"), {})
        self.assertEqual(self.edit("doc/contract/README.md"), {})

    def test_ignores_old_docs_path(self):
        self.assertEqual(self.edit("/r/docs/contract/04_interface.md"), {})


class SendGuardTest(unittest.TestCase):
    def send(self, *files: str) -> dict:
        return run("send_guard.py", "SendUserFile", {"files": list(files)})

    def test_denies_formal_contract_page(self):
        out = self.send("/r/doc/contract/02_invariants.md")
        self.assertEqual(out.get("permissionDecision"), "deny")
        self.assertIn("doc/contract/02_invariants.md", out["permissionDecisionReason"])

    def test_allows_marked_copies(self):
        self.assertEqual(self.send("/r/doc/decisions/_marked/02_invariants.v3.md",
                                   "/r/doc/decisions/_marked/02_invariants.v3.marked.md"), {})

    def test_allows_review_readme(self):
        self.assertEqual(self.send("/r/doc/contract/README.md"), {})

    def test_ignores_old_docs_path(self):
        self.assertEqual(self.send("/r/docs/contract/02_invariants.md"), {})


if __name__ == "__main__":
    unittest.main()
