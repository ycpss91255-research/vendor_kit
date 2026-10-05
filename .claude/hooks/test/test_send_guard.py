"""send_guard.py 的測試：用 subprocess 跑 hook，餵 PreToolUse 的 JSON。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "send_guard.py"
REPO = Path(__file__).resolve().parents[3]


def run_hook(files, tool_name: str = "SendUserFile") -> str:
    stdin = json.dumps({"tool_name": tool_name, "tool_input": {"files": files}})
    return subprocess.run(
        [sys.executable, str(HOOK)], input=stdin,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def denied(out: str) -> bool:
    return bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


class SendGuardTest(unittest.TestCase):
    def test_formal_files_are_denied(self):
        for f in ("README.md", "doc/decisions/review/01_purpose.md",
                  "doc/contract/03_output.md", "doc/contract/03_output.csv"):
            with self.subTest(f=f):
                self.assertTrue(denied(run_hook([f])))

    def test_unversioned_review_copies_are_denied(self):
        for f in ("doc/review/01_purpose/01_purpose.md",
                  "doc/review/01_purpose/01_purpose.marked.md"):
            with self.subTest(f=f):
                self.assertTrue(denied(run_hook([f])))

    def test_absolute_path_in_repo_is_denied(self):
        self.assertTrue(denied(run_hook([str(REPO / "README.md")])))

    def test_reason_names_repo_scripts(self):
        reason = json.loads(run_hook(["README.md"]))["hookSpecificOutput"]["permissionDecisionReason"]
        for script in ("script/doc/mark_changes.py", "script/doc/pack_review.py", "script/doc/README.md"):
            self.assertIn(script, reason)
            self.assertTrue((REPO / script).is_file())
        self.assertNotIn(str(Path.home()), reason)  # 不准寫本機絕對路徑

    def test_other_files_pass(self):
        for f in ("review_v3.zip", "script/doc/README.md", "doc/decisions/README.md",
                  "doc/contract/README.md", "doc/decisions/review/01_purpose.v4.marked.md"):
            with self.subTest(f=f):
                self.assertEqual(run_hook([f]), "")

    def test_other_tool_passes(self):
        self.assertEqual(run_hook(["README.md"], tool_name="Bash"), "")

    def test_bad_json_passes(self):
        out = subprocess.run([sys.executable, str(HOOK)], input="not json",
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
