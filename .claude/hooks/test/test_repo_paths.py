"""repo_paths.py 的測試：主 worktree 與 linked worktree 都回推到同一個主目錄。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import repo_paths  # noqa: E402


class RepoPathsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name).resolve()
        self.src = base / "src"
        self.abs_wt = base / "worktree" / "pr" / "1"
        self.rel_wt = base / "worktree" / "issue" / "2"
        for name in ("1", "2"):
            (self.src / ".git" / "worktrees" / name).mkdir(parents=True)
        self.abs_wt.mkdir(parents=True)
        self.rel_wt.mkdir(parents=True)
        (self.abs_wt / ".git").write_text(f"gitdir: {self.src}/.git/worktrees/1\n")
        (self.rel_wt / ".git").write_text("gitdir: ../../../src/.git/worktrees/2\n")

    def tearDown(self):
        self.tmp.cleanup()

    def at(self, project):
        with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(project)}):
            return repo_paths.main_dir(), repo_paths.worktree_root()

    def test_main_and_linked_agree(self):
        want = (self.src, self.src.parent / "worktree")
        for project in (self.src, self.abs_wt, self.rel_wt):
            with self.subTest(project=project):
                self.assertEqual(self.at(project), want)


if __name__ == "__main__":
    unittest.main()
