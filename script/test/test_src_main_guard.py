"""src_main_guard.py 的測試：用 subprocess 餵 PreToolUse 的 JSON，看 deny 或放行。

跑法：python3 -m unittest discover -s script/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "src_main_guard.py"


class SrcMainGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name).resolve()
        cls.src = base / "src"
        cls.wt = base / "worktree" / "pr" / "1"
        (cls.src / ".git" / "worktrees" / "1").mkdir(parents=True)
        cls.wt.mkdir(parents=True)
        (cls.wt / ".git").write_text(f"gitdir: {cls.src}/.git/worktrees/1\n")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_hook(self, tool, tool_input, cwd=None, project=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project or self.src))
        payload = {"tool_name": tool, "tool_input": tool_input, "cwd": str(cwd or self.src)}
        out = subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(payload),
            capture_output=True, text=True, env=env, check=True,
        ).stdout.strip()
        if not out:
            return "allow"
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]

    def bash(self, command, cwd=None):
        return self.run_hook("Bash", {"command": command}, cwd=cwd)

    # Edit／Write
    def test_edit_in_main_denied(self):
        self.assertEqual(self.run_hook("Edit", {"file_path": str(self.src / "README.md")}), "deny")

    def test_write_relative_in_main_denied(self):
        self.assertEqual(self.run_hook("Write", {"file_path": "doc/x.md"}), "deny")

    def test_edit_in_worktree_allowed(self):
        self.assertEqual(self.run_hook("Edit", {"file_path": str(self.wt / "README.md")}), "allow")

    def test_edit_hooks_exempt(self):
        path = self.src / ".claude" / "hooks" / "x.py"
        self.assertEqual(self.run_hook("Write", {"file_path": str(path)}), "allow")

    def test_edit_settings_exempt(self):
        path = self.src / ".claude" / "settings.json"
        self.assertEqual(self.run_hook("Edit", {"file_path": str(path)}), "allow")

    def test_notebook_in_main_denied(self):
        path = self.src / "a.ipynb"
        self.assertEqual(self.run_hook("NotebookEdit", {"notebook_path": str(path)}), "deny")

    def test_session_in_worktree_guards_main(self):
        # 在 linked worktree 開 session：CLAUDE_PROJECT_DIR 是 worktree，仍守主目錄、不擋 worktree
        wt_edit = self.run_hook("Edit", {"file_path": str(self.wt / "a.md")}, cwd=self.wt, project=self.wt)
        src_edit = self.run_hook("Edit", {"file_path": str(self.src / "a.md")}, cwd=self.wt, project=self.wt)
        self.assertEqual((wt_edit, src_edit), ("allow", "deny"))

    # Bash
    def test_commit_in_main_denied(self):
        self.assertEqual(self.bash('git commit -m "x"'), "deny")

    def test_commit_with_C_main_denied(self):
        self.assertEqual(self.bash(f"git -C {self.src} commit -m x", cwd=self.wt), "deny")

    def test_commit_with_C_worktree_allowed(self):
        self.assertEqual(self.bash(f"git -C {self.wt} commit -m x"), "allow")

    def test_commit_after_cd_worktree_allowed(self):
        self.assertEqual(self.bash(f"cd {self.wt} && git commit -m x"), "allow")

    def test_commit_in_worktree_cwd_allowed(self):
        self.assertEqual(self.bash("git commit -m x", cwd=self.wt), "allow")

    def test_switch_main_allowed(self):
        self.assertEqual(self.bash("git switch main"), "allow")

    def test_checkout_main_allowed(self):
        self.assertEqual(self.bash("git checkout main"), "allow")

    def test_switch_create_denied(self):
        self.assertEqual(self.bash("git switch -c x"), "deny")

    def test_switch_other_denied(self):
        self.assertEqual(self.bash("git switch feat/x"), "deny")

    def test_checkout_path_denied(self):
        self.assertEqual(self.bash("git checkout -- file"), "deny")

    def test_merge_ff_only_origin_main_allowed(self):
        self.assertEqual(self.bash("git fetch && git merge --ff-only origin/main"), "allow")

    def test_merge_other_denied(self):
        self.assertEqual(self.bash("git merge feat/x"), "deny")

    def test_pull_ff_only_allowed(self):
        self.assertEqual(self.bash("git pull --ff-only"), "allow")

    def test_pull_plain_denied(self):
        self.assertEqual(self.bash("git pull"), "deny")

    def test_read_only_allowed(self):
        for cmd in ("git status", "git log --oneline -3", "git diff", "git show HEAD",
                    "git worktree add ../worktree/pr/2 -b x", "git worktree list"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd), "allow")

    def test_other_writes_denied(self):
        for cmd in ("git reset --hard", "git rebase main", "git cherry-pick abc", "git am x.patch",
                    "git stash", "git branch -f main HEAD", "git tag v1", "git restore a.md"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd), "deny")


if __name__ == "__main__":
    unittest.main()
