"""rebase_push.py 的測試：暫存 bare remote 加兩個 clone（自己的 worktree、讓 main 前進的另一個人），
push 經 repo 真的 Bash hook。

跑法：python3 -m unittest discover -s script/git/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import rebase_push as rp  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
    "CLAUDE_PROJECT_DIR": str(ROOT),
}
BRANCH = "feat/x"


class Base(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, GIT_ENV)
        self.env.start()
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.remote = base / "remote.git"
        self.repo = base / "mine"
        self.other = base / "other"
        self.git(base, "init", "-q", "--bare", "-b", "main", str(self.remote))
        self.git(base, "init", "-q", "-b", "main", str(self.repo))
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.commit(self.repo, "a.txt", "a\n", "chore: 初始")
        self.git(self.repo, "push", "-q", "origin", "main")
        self.git(base, "clone", "-q", str(self.remote), str(self.other))
        self.git(self.repo, "switch", "-q", "-c", BRANCH)
        self.commit(self.repo, "b.txt", "b\n", "feat: 分支的改動")
        self.git(self.repo, "push", "-q", "-u", "origin", BRANCH)
        self.git(self.repo, "fetch", "-q", "origin")

    def tearDown(self):
        self.tmp.cleanup()
        self.env.stop()

    def git(self, cwd, *args):
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def commit(self, repo, name, text, message):
        (repo / name).write_text(text, encoding="utf-8")
        self.git(repo, "add", name)
        self.git(repo, "commit", "-q", "-m", message)

    def advance_main(self, name="c.txt", text="c\n"):
        """另一個人讓 origin/main 前進。"""
        self.git(self.other, "switch", "-q", "main")
        self.git(self.other, "pull", "-q", "origin", "main")
        self.commit(self.other, name, text, "chore: main 前進")
        self.git(self.other, "push", "-q", "origin", "main")

    def head(self, repo=None):
        return self.git(repo or self.repo, "rev-parse", "HEAD")

    def remote_sha(self, branch=BRANCH):
        return self.git(self.remote, "rev-parse", f"refs/heads/{branch}")

    def lease_file(self):
        return self.repo / ".git" / rp.LEASE_FILE

    def run_rp(self, *extra, branch=BRANCH, settings=None):
        argv = ["--repo", str(self.repo), "--branch", branch, *extra]
        if settings is not None:
            return rp.run(argv, settings=settings)
        out = StringIO()
        with redirect_stdout(out):
            code = rp.main(argv)
        return code, json.loads(out.getvalue())


class Rebase(Base):
    def test_up_to_date(self):
        before = self.remote_sha()
        code, out = self.run_rp()
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(out["state"], "up_to_date")
        self.assertFalse(out["pushed"])
        self.assertEqual(out["before"], out["after"])
        self.assertEqual(self.remote_sha(), before)
        self.assertFalse(self.lease_file().exists())

    def test_rebased_and_pushed(self):
        self.advance_main()
        old = self.head()
        code, out = self.run_rp()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["state"], "rebased")
        self.assertTrue(out["pushed"])
        self.assertEqual(out["before"], old)
        self.assertEqual(out["after"], self.head())
        self.assertNotEqual(out["after"], old)
        self.assertEqual(self.remote_sha(), out["after"])
        main = self.git(self.remote, "rev-parse", "refs/heads/main")
        self.git(self.repo, "merge-base", "--is-ancestor", main, "HEAD")
        self.assertFalse(self.lease_file().exists())

    def test_no_push(self):
        self.advance_main()
        before = self.remote_sha()
        code, out = self.run_rp("--no-push")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["state"], "rebased")
        self.assertFalse(out["pushed"])
        self.assertEqual(self.remote_sha(), before)

    def test_branch_never_pushed(self):
        """遠端還沒有這個分支：lease 要求遠端仍然沒有，push 會建立它。"""
        self.git(self.repo, "switch", "-q", "-c", "feat/new")
        self.commit(self.repo, "d.txt", "d\n", "feat: 新分支")
        self.advance_main()
        code, out = self.run_rp(branch="feat/new")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["pushed"])
        self.assertEqual(self.remote_sha("feat/new"), self.head())


class Conflict(Base):
    def make_conflict(self):
        self.advance_main(name="b.txt", text="main 的 b\n")
        code, out = self.run_rp()
        self.assertEqual(code, 3, out)
        return out

    def test_conflict_lists_files(self):
        before = self.remote_sha()
        out = self.make_conflict()
        self.assertFalse(out["ok"])
        self.assertEqual(out["state"], "conflict")
        self.assertEqual(out["conflicts"], ["b.txt"])
        self.assertIsNone(out["error"])
        self.assertFalse(out["pushed"])
        self.assertTrue((self.repo / ".git" / "rebase-merge").is_dir())
        self.assertTrue(self.lease_file().is_file())
        self.assertEqual(self.remote_sha(), before)

    def test_continue_without_resolving(self):
        self.make_conflict()
        code, out = self.run_rp("--continue")
        self.assertEqual(code, 3, out)
        self.assertEqual(out["conflicts"], ["b.txt"])

    def test_continue_after_resolving_pushes(self):
        start = self.head()
        self.make_conflict()
        (self.repo / "b.txt").write_text("合併後的 b\n", encoding="utf-8")
        self.git(self.repo, "add", "b.txt")
        code, out = self.run_rp("--continue")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["state"], "rebased")
        self.assertTrue(out["pushed"])
        self.assertEqual(out["before"], start)
        self.assertEqual(self.remote_sha(), self.head())
        self.assertEqual(self.git(self.repo, "symbolic-ref", "--short", "HEAD"), BRANCH)
        self.assertFalse(self.lease_file().exists())

    def test_abort(self):
        start = self.head()
        self.make_conflict()
        code, out = self.run_rp("--abort")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(out["state"], "aborted")
        self.assertEqual(self.head(), start)
        self.assertFalse((self.repo / ".git" / "rebase-merge").exists())
        self.assertFalse(self.lease_file().exists())

    def test_lease_fails_when_remote_branch_moved(self):
        """衝突停下時別人推了同一個分支：--continue 的 push 用開始時的 lease，要失敗。"""
        self.make_conflict()
        self.git(self.other, "fetch", "-q", "origin")
        self.git(self.other, "switch", "-q", "-c", BRANCH, f"origin/{BRANCH}")
        self.commit(self.other, "e.txt", "e\n", "feat: 別人的改動")
        self.git(self.other, "push", "-q", "origin", BRANCH)
        theirs = self.remote_sha()
        (self.repo / "b.txt").write_text("合併後的 b\n", encoding="utf-8")
        self.git(self.repo, "add", "b.txt")
        code, out = self.run_rp("--continue")
        self.assertEqual(code, 1, out)
        self.assertFalse(out["ok"])
        self.assertEqual(out["state"], "rebased")
        self.assertFalse(out["pushed"])
        self.assertIn("push", out["error"])
        self.assertEqual(self.remote_sha(), theirs)


class Refused(Base):
    def test_main_refused(self):
        self.git(self.repo, "switch", "-q", "main")
        code, out = self.run_rp(branch="main")
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertIn("main", out["error"])
        self.assertIsNone(out["state"])

    def test_branch_mismatch(self):
        code, out = self.run_rp(branch="feat/other")
        self.assertEqual(code, 1)
        self.assertIn("feat/other", out["error"])

    def test_dirty_worktree(self):
        (self.repo / "b.txt").write_text("改了\n", encoding="utf-8")
        code, out = self.run_rp()
        self.assertEqual(code, 1)
        self.assertIn("不乾淨", out["error"])

    def test_continue_without_rebase(self):
        for flag in ("--continue", "--abort"):
            with self.subTest(flag=flag):
                code, out = self.run_rp(flag)
                self.assertEqual(code, 1)
                self.assertIn("沒有進行中的 rebase", out["error"])

    def test_hook_denied_push(self):
        self.advance_main()
        hook = Path(self.tmp.name) / "deny.py"
        hook.write_text(
            "import json\nprint(json.dumps({'hookSpecificOutput': {'permissionDecision': 'deny',"
            " 'permissionDecisionReason': 'no'}}))\n", encoding="utf-8")
        settings = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": f"{sys.executable} {hook}"}]}]}}
        before = self.remote_sha()
        code, out = self.run_rp(settings=settings)
        self.assertEqual(code, 1, out)
        self.assertEqual(out["state"], "rebased")
        self.assertFalse(out["pushed"])
        self.assertEqual(out["denied"][0]["hook"], "deny.py")
        self.assertEqual(self.remote_sha(), before)

    def test_guard_denies_push_to_main(self):
        """guard.py 本身也擋推到 main（腳本前面已經擋，這裡確認 push 的 argv 會交給它）。"""
        with self.assertRaises(rp.Fail) as ctx:
            rp.push(self.repo, "main", "", project_dir=ROOT)
        hooks = [d["hook"] for d in ctx.exception.extra["denied"]]
        self.assertIn("guard.py", hooks)


class Usage(Base):
    def test_usage_errors(self):
        for extra in (["--continue", "--abort"], ["--bogus"]):
            with self.subTest(extra=extra):
                code, out = self.run_rp(*extra)
                self.assertEqual(code, 2)
                self.assertFalse(out["ok"])
                self.assertIn("用法錯", out["error"])


if __name__ == "__main__":
    unittest.main()
