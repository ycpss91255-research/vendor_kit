"""pr_target.py：用暫存的 origin／主 repo 與假的 gh 測找分支、issue、建或沿用 worktree、乾淨檢查與並行時的鎖。"""
import fcntl
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pr_target as t  # noqa: E402


def sh(cwd, *args):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class Issue(unittest.TestCase):
    def test_first_ref(self):
        self.assertEqual(t.first_issue("x\nRefs: #12\nCloses #7\n"), 12)
        self.assertEqual(t.first_issue("[claude] y\n\ncloses #7"), 7)
        self.assertEqual(t.first_issue("Fixes #3"), 3)
        self.assertIsNone(t.first_issue("see #5 later"))


class PrTarget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ws = pathlib.Path(self.tmp.name)
        self.ws = ws
        origin = ws / "origin.git"
        sh(ws, "git", "init", "-q", "--bare", "-b", "main", str(origin))
        self.repo = ws / "src"
        sh(ws, "git", "clone", "-q", str(origin), str(self.repo))
        self.cfg(self.repo)
        (self.repo / "a.txt").write_text("a\n")
        sh(self.repo, "git", "add", "a.txt")
        sh(self.repo, "git", "commit", "-q", "-m", "init")
        sh(self.repo, "git", "push", "-q", "origin", "HEAD:main")
        # 遠端的 PR 分支，由另一個 clone 推上去，主 repo 沒有本機分支
        other = ws / "other"
        sh(ws, "git", "clone", "-q", str(origin), str(other))
        self.cfg(other)
        sh(other, "git", "switch", "-q", "-c", "feat/x")
        (other / "b.txt").write_text("b\n")
        sh(other, "git", "add", "b.txt")
        sh(other, "git", "commit", "-q", "-m", "b")
        sh(other, "git", "push", "-q", "origin", "feat/x")
        self.other = other
        self.pr_json = ws / "pr.json"
        self.set_pr()
        gh = ws / "gh"
        gh.write_text(f"#!/bin/sh\ncat '{self.pr_json}'\n")
        gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
        self.env = mock.patch.dict(os.environ, {"PR_TARGET_GH": str(gh)})
        self.env.start()
        self.wt = ws / "worktree" / "branch" / "feat" / "x"

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    @staticmethod
    def cfg(repo):
        for k, v in (("user.name", "t"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
            sh(repo, "git", "config", k, v)

    def set_pr(self, state="OPEN", body="[claude] x\n\nCloses #9\n", branch="feat/x"):
        self.pr_json.write_text(json.dumps({"number": 5, "state": state, "headRefName": branch,
                                            "body": body, "url": "https://example.com/pull/5"}))

    def run_main(self):
        buf = StringIO()
        with redirect_stdout(buf):
            code = t.main(["5", "--repo", str(self.repo)])
        return code, json.loads(buf.getvalue())

    def test_creates_worktree_from_remote_branch(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertEqual((out["branch"], out["issue"], out["path"]), ("feat/x", 9, str(self.wt)))
        self.assertEqual(out["repo"], str(self.repo))
        self.assertTrue(out["created"])
        self.assertTrue((self.wt / "b.txt").exists())
        self.assertEqual(out["behind_main"], 0)

    def test_reuses_existing_and_fast_forwards(self):
        self.run_main()
        (self.other / "c.txt").write_text("c\n")
        sh(self.other, "git", "add", "c.txt")
        sh(self.other, "git", "commit", "-q", "-m", "c")
        sh(self.other, "git", "push", "-q", "origin", "feat/x")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertFalse(out["created"])
        self.assertTrue(out["fast_forwarded"])
        self.assertTrue((self.wt / "c.txt").exists())

    def test_dirty_worktree_fails(self):
        self.run_main()
        (self.wt / "junk.txt").write_text("x\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("未提交", out["error"])

    def test_unpushed_commit_fails(self):
        self.run_main()
        self.cfg(self.wt)
        (self.wt / "d.txt").write_text("d\n")
        sh(self.wt, "git", "add", "d.txt")
        sh(self.wt, "git", "commit", "-q", "-m", "d")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("還沒推", out["error"])

    def test_closed_pr_fails(self):
        self.set_pr(state="MERGED")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertFalse(self.wt.exists())

    def test_no_issue_ref_fails(self):
        self.set_pr(body="[claude] x\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("Closes", out["error"])

    def test_missing_remote_branch_fails(self):
        self.set_pr(branch="feat/none")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("遠端沒有分支", out["error"])

    def test_lock_blocks_second_holder(self):
        lock = pathlib.Path(sh(self.repo, "git", "rev-parse", "--path-format=absolute",
                                "--git-common-dir")) / "pr_target.lock"
        with t.repo_lock(self.repo):
            with open(lock, "w") as f:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with open(lock, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)   # 放開之後拿得到

    def test_parallel_prepare_two_branches(self):
        sh(self.other, "git", "switch", "-q", "-c", "feat/y")
        sh(self.other, "git", "push", "-q", "origin", "feat/y")
        res, errs = {}, []

        def run(b):
            try:
                res[b] = t.prepare(self.repo, b)
            except Exception as e:  # noqa: BLE001
                errs.append(f"{b}: {e}")

        ths = [threading.Thread(target=run, args=(b,)) for b in ("feat/x", "feat/y")]
        for th in ths:
            th.start()
        for th in ths:
            th.join()
        self.assertEqual(errs, [])
        self.assertTrue(res["feat/x"]["created"] and res["feat/y"]["created"])
        self.assertTrue((self.ws / "worktree" / "branch" / "feat" / "y" / "b.txt").exists())


if __name__ == "__main__":
    unittest.main()
