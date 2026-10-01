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
        base = Path(cls.tmp.name).resolve()
        cls.src = base / "src"
        cls.linked = base / "worktree" / "branch" / "feat" / "w"
        (cls.src / ".git" / "worktrees" / "w").mkdir(parents=True)
        cls.linked.mkdir(parents=True)
        (cls.linked / ".git").write_text(f"gitdir: {cls.src}/.git/worktrees/w\n")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def bash(self, command, tool="Bash", project=None, cwd=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project or self.src))
        payload = {"tool_name": tool, "tool_input": {"command": command},
                   "cwd": str(cwd or self.src)}
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

    def test_linked_project_dir_same_as_main(self):
        # session 開在 linked worktree：worktree 根目錄仍是主 worktree 上一層的 worktree/
        for cmd, want in (
            (f"git -C {self.src} worktree add ../worktree/pr/12 feat/x", "allow"),
            (f"git worktree add {self.src.parent}/worktree/issue/7", "allow"),
            ("git worktree add /tmp/x feat/x", "deny"),
            ("git worktree add ../other feat/x", "deny"),
        ):
            with self.subTest(cmd=cmd):
                main = self.bash(cmd, project=self.src)
                linked = self.bash(cmd, project=self.linked)
                self.assertEqual(main, want)
                self.assertEqual(linked, want)


if __name__ == "__main__":
    unittest.main()
