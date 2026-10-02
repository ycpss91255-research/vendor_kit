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

    def branch(self, name, *paths, remote=True):
        """從 main 開分支 name、commit paths；remote 為真時設 origin/<name>。結束後切回 main。"""
        git(self.repo, "checkout", "-q", "-b", name, "main")
        self.change(*paths)
        if remote:
            git(self.repo, "update-ref", f"refs/remotes/origin/{name}", "HEAD")
        git(self.repo, "checkout", "-q", "main")

    def stale_cwd(self):
        """hook 的 cwd 停在另一個舊分支（改了兩個範圍，用它會被擋）。"""
        self.branch("old", ".claude/workflows/doc-edit.js", "CONTEXT.md", remote=False)
        git(self.repo, "checkout", "-q", "old")

    def test_head_branch_diff_used_over_stale_cwd(self):
        self.branch("feat", "CONTEXT.md")
        self.stale_cwd()
        b = self.body("Refs: #3\n")
        cmd = f"gh pr create -R o/r --base main --head feat --body-file {b}"
        self.assertIsNone(run_hook(cmd, self.repo))
        spec = run_hook(f"gh pr create -R o/r --base main --body-file {b}", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("2 個範圍", spec["permissionDecisionReason"])

    def test_head_branch_with_owner_prefix(self):
        self.branch("feat", "CONTEXT.md")
        self.stale_cwd()
        b = self.body("Refs: #3\n")
        self.assertIsNone(run_hook(f"gh pr create --head=o:feat --body-file {b}", self.repo))

    def test_head_without_remote_ref_falls_back_to_cwd(self):
        self.change("CONTEXT.md")
        b = self.body("Refs: #3\n")
        self.assertIsNone(run_hook(f"gh pr create --head nope --body-file {b}", self.repo))

    def test_cd_prefix_used_over_stale_cwd(self):
        other = tempfile.TemporaryDirectory()
        self.addCleanup(other.cleanup)
        stale = Path(other.name) / "stale"
        git(self.repo, "worktree", "add", "-q", "-b", "old", str(stale), "main")
        (stale / "CONTEXT.md").write_text("y\n")
        (stale / "x.js").write_text("y\n")
        git(stale, "add", ".")
        git(stale, "commit", "-qm", "old")
        self.change("CONTEXT.md")
        b = self.body("Refs: #3\n")
        cmd = f"cd {self.repo} && gh pr create --body-file {b}"
        self.assertIsNone(run_hook(cmd, stale))
        cmd = f"git -C {self.repo} status && gh pr create --body-file {self.repo / b}"
        self.assertIsNone(run_hook(cmd, stale))

    def test_no_changed_files_is_denied(self):
        b = self.body("Refs: #3\n")
        spec = run_hook(f"gh pr create --body-file {b}", self.repo)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("--head", spec["permissionDecisionReason"])

    def test_not_a_repo_is_denied(self):
        other = tempfile.TemporaryDirectory()
        self.addCleanup(other.cleanup)
        spec = run_hook("gh pr create --body 'Refs: #3'", other.name)
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("取不到", spec["permissionDecisionReason"])

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
