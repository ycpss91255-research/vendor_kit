"""pr_rules_guard.py 的測試：在暫存 git repo 裡用 subprocess 跑 hook，餵 PreToolUse 的 JSON。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "pr_rules_guard.py"


def git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


def run_hook(command, cwd, tool="Bash"):
    payload = json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": str(cwd)})
    out = subprocess.run([sys.executable, str(HOOK)], input=payload,
                         capture_output=True, text=True, check=True).stdout.strip()
    return json.loads(out)["hookSpecificOutput"] if out else None


class PrRulesGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "README.md").write_text("x\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "init")
        git(self.repo, "update-ref", "refs/remotes/origin/main", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def change(self, *paths):
        for p in paths:
            f = self.repo / p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("y\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "change")

    def body(self, text):
        (self.repo / "body.md").write_text(text, encoding="utf-8")
        return "body.md"

    def test_ok_passes(self):
        self.change("script/doc/check_terms.py", "script/doc/test/test_check_terms.py")
        b = self.body("[claude] x\n\nCloses #9\n")
        self.assertIsNone(run_hook(f"gh pr create -R o/r --base main --body-file {b}", self.repo))

    def test_no_issue_is_denied(self):
        self.change("script/doc/check_terms.py")
        b = self.body("[claude] x\n")
        spec = run_hook(f"gh pr create -R o/r --body-file {b}", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("沒有連 issue", spec["permissionDecisionReason"])

    def test_two_scopes_is_denied(self):
        self.change(".claude/workflows/doc-edit.js", "CONTEXT.md")
        b = self.body("Refs #1\n")
        spec = run_hook(f"gh pr create --body-file={b}", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("2 個範圍", spec["permissionDecisionReason"])

    def test_cd_prefix_and_inline_body(self):
        self.change("CONTEXT.md")
        sub = self.repo.parent
        cmd = f"cd {self.repo} && gh pr create --body 'Refs: #3'"
        self.assertIsNone(run_hook(cmd, sub))

    def test_missing_body_is_denied(self):
        spec = run_hook("gh pr create --fill", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("--body-file", spec["permissionDecisionReason"])

    def test_unreadable_body_file_is_denied(self):
        spec = run_hook("gh pr create --body-file nope.md", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")

    def test_other_commands_pass(self):
        for cmd in ("gh pr view 1", "git push", "echo gh pr create", "gh issue create --title x"):
            with self.subTest(cmd=cmd):
                self.assertIsNone(run_hook(cmd, self.repo))

    def test_other_tool_and_bad_input_pass(self):
        self.assertIsNone(run_hook("gh pr create --fill", self.repo, tool="Read"))
        out = subprocess.run([sys.executable, str(HOOK)], input="not json",
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
