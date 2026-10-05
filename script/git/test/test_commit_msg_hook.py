""".githooks/commit-msg 的測試：在暫存 git repo 設 core.hooksPath，實際跑 git commit。

跑法：python3 -m unittest discover -s script/git/test
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# hook 用 git rev-parse --show-toplevel 找檢查器，所以暫存 repo 要放同樣的相對路徑
FILES = (
    ".githooks/commit-msg",
    "script/git/check_commit_msg.py",
    ".claude/hooks/attribution_guard.py",
)


class TestCommitMsgHook(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        for rel in FILES:
            dst = self.repo / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        self.env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
        }
        self.git("init", "-q")
        self.git("config", "core.hooksPath", ".githooks")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env,
            capture_output=True, text=True,
        )

    def commit(self, message):
        return self.git("commit", "-q", "--allow-empty", "-m", message)

    def test_hook_is_executable(self):
        self.assertTrue(os.access(ROOT / ".githooks/commit-msg", os.X_OK))

    def test_valid_message_passes(self):
        r = self.commit("feat(cli): 新增 --output 參數\n\nRefs: #110")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.git("rev-list", "--count", "HEAD").stdout.strip(), "1")

    def test_invalid_message_blocked(self):
        r = self.commit("隨便改一下")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("commit 訊息格式不合", r.stderr)
        self.assertNotEqual(self.git("rev-parse", "--verify", "-q", "HEAD").returncode, 0)


if __name__ == "__main__":
    unittest.main()
