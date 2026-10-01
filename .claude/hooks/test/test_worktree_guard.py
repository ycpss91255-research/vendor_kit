"""worktree_guard.py 的測試：用 subprocess 餵 PreToolUse 的 JSON，看 deny 或放行。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "worktree_guard.py"


class WorktreeGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.src = Path(cls.tmp.name).resolve() / "src"
        cls.src.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def bash(self, command, tool="Bash"):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.src))
        payload = {"tool_name": tool, "tool_input": {"command": command}, "cwd": str(self.src)}
        out = subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(payload),
            capture_output=True, text=True, env=env, check=True,
        ).stdout.strip()
        if not out:
            return "allow"
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]

    def test_allowed_locations(self):
        for cmd in ("git worktree add ../worktree/pr/12 feat/x",
                    "git worktree add -b feat/y ../worktree/issue/7",
                    "git -C . worktree add ../worktree/branch/feat/z"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd), "allow")

    def test_denied_locations(self):
        for cmd in ("git worktree add /tmp/x feat/x",
                    "git worktree add ../other feat/x",
                    "git worktree add ../worktree/pr/abc feat/x",
                    "git fetch && git worktree add -b feat/y ../worktree/foo"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd), "deny")

    def test_other_commands_allowed(self):
        self.assertEqual(self.bash("git worktree list"), "allow")
        self.assertEqual(self.bash("echo git worktree add /tmp/x", tool="Edit"), "allow")


if __name__ == "__main__":
    unittest.main()
