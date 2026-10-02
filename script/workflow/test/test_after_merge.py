"""after_merge.py：用暫存的 origin／主 repo／worktree 與假的 gh 測 merge 後的收尾。"""
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import after_merge as t  # noqa: E402


def sh(cwd, *args):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def cfg(repo):
    for k, v in (("user.name", "t"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
        sh(repo, "git", "config", k, v)


class AfterMerge(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ws = pathlib.Path(self.tmp.name)
        origin = ws / "origin.git"
        sh(ws, "git", "init", "-q", "--bare", "-b", "main", str(origin))
        self.repo = ws / "src"
        sh(ws, "git", "clone", "-q", str(origin), str(self.repo))
        cfg(self.repo)
        (self.repo / "a.txt").write_text("a\n")
        sh(self.repo, "git", "add", "a.txt")
        sh(self.repo, "git", "commit", "-q", "-m", "init")
        sh(self.repo, "git", "push", "-q", "-u", "origin", "HEAD:main")
        # PR 分支的 worktree：commit、push，再由另一個 clone merge 進 origin/main
        self.wt = ws / "worktree" / "branch" / "feat" / "x"
        sh(self.repo, "git", "worktree", "add", "-q", "-b", "feat/x", str(self.wt), "origin/main")
        (self.wt / "b.txt").write_text("b\n")
        sh(self.wt, "git", "add", "b.txt")
        sh(self.wt, "git", "commit", "-q", "-m", "b")
        sh(self.wt, "git", "push", "-q", "origin", "feat/x")
        other = ws / "other"
        sh(ws, "git", "clone", "-q", str(origin), str(other))
        cfg(other)
        sh(other, "git", "merge", "-q", "--no-ff", "-m", "merge", "origin/feat/x")
        sh(other, "git", "push", "-q", "origin", "main")
        self.merged_head = sh(other, "git", "rev-parse", "HEAD")
        # scratchpad：慣例目錄與不該動的目錄
        self.scratch = ws / "scratch"
        for d in ("pr-fix/5", "pr-fix/6", "pr/139-x", "pr/139-y", "other"):
            (self.scratch / d).mkdir(parents=True)
            (self.scratch / d / "f.txt").write_text("x\n")
        self.pr_json = ws / "pr.json"
        self.calls = ws / "calls.txt"
        self.set_pr()
        gh = ws / "gh"
        gh.write_text(f"#!/bin/sh\necho \"$@\" >> '{self.calls}'\ncat '{self.pr_json}'\n")
        gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
        self.env = mock.patch.dict(os.environ, {"AFTER_MERGE_GH": str(gh)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def set_pr(self, state="MERGED", merged_at="2026-01-01T00:00:00Z", branch="feat/x"):
        self.pr_json.write_text(json.dumps({"state": state, "headRefName": branch, "mergedAt": merged_at}))

    def run_main(self, *extra):
        buf = StringIO()
        with redirect_stdout(buf):
            code = t.main(["5", "--repo", str(self.repo), *extra])
        return code, json.loads(buf.getvalue())

    def head(self):
        return sh(self.repo, "git", "rev-parse", "HEAD")

    def test_full_cleanup(self):
        code, out = self.run_main("--scratch", str(self.scratch), "--item", "139-x")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"] and out["merged"])
        self.assertEqual(out["pulled"], self.merged_head)
        self.assertEqual(self.head(), self.merged_head)
        self.assertTrue(out["worktree_removed"])
        self.assertFalse(self.wt.exists())
        self.assertEqual(sh(self.repo, "git", "branch", "--list", "feat/x"), "")
        self.assertEqual(sorted(pathlib.Path(p).relative_to(self.scratch).as_posix() for p in out["scratch_removed"]),
                         ["pr-fix/5", "pr/139-x"])
        for d in ("pr-fix/6", "pr/139-y", "other"):
            self.assertTrue((self.scratch / d).is_dir(), d)
        self.assertIsNone(out["error"])
        # 只呼叫唯讀的 gh pr view
        for line in self.calls.read_text().splitlines():
            self.assertTrue(line.startswith("pr view 5 "), line)

    def test_not_merged_touches_nothing(self):
        self.set_pr(state="OPEN", merged_at=None)
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch), "--item", "139-x")
        self.assertEqual(code, 1)
        self.assertFalse(out["merged"])
        self.assertIsNone(out["pulled"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())
        self.assertIn("還沒 merge", out["error"])

    def test_dirty_repo_stops(self):
        (self.repo / "a.txt").write_text("changed\n")
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertIn("未提交", out["error"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())
        self.assertEqual((self.repo / "a.txt").read_text(), "changed\n")

    def test_untracked_file_does_not_block(self):
        (self.repo / "local.txt").write_text("x\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertTrue((self.repo / "local.txt").exists())

    def test_not_on_main_stops(self):
        sh(self.repo, "git", "switch", "-q", "-c", "topic")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("不在 main", out["error"])
        self.assertEqual(sh(self.repo, "git", "rev-parse", "--abbrev-ref", "HEAD"), "topic")
        self.assertTrue(self.wt.exists())

    def test_missing_worktree_is_skipped(self):
        sh(self.repo, "git", "worktree", "remove", str(self.wt))
        sh(self.repo, "git", "branch", "-D", "feat/x")
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 0, out)
        self.assertTrue(out["worktree_skipped"])
        self.assertFalse(out["worktree_removed"])
        self.assertEqual([pathlib.Path(p).name for p in out["scratch_removed"]], ["5"])

    def test_no_scratch_keeps_dirs(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["scratch_removed"], [])
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())

    def test_bad_item_touches_nothing(self):
        before = self.head()
        for bad in ("..", "x-1", "139-", "139-../other", "*"):
            code, out = self.run_main("--scratch", str(self.scratch), "--item", bad)
            self.assertEqual(code, 1, bad)
            self.assertIn("--item", out["error"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "other").is_dir())

    def test_item_sanitized_like_pr_js(self):
        (self.scratch / "pr" / "139-a_b").mkdir(parents=True)
        code, out = self.run_main("--scratch", str(self.scratch), "--item", "139-a/b")
        self.assertEqual(code, 0, out)
        self.assertFalse((self.scratch / "pr" / "139-a_b").exists())

    def test_gh_failure(self):
        self.pr_json.write_text("not json")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("不是 JSON", out["error"])
        self.assertTrue(self.wt.exists())


if __name__ == "__main__":
    unittest.main()
