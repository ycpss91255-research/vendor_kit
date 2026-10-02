"""commit_push.py 的測試：暫存 git repo 加暫存 bare remote，commit 與 push 經 repo 真的 Bash hook。

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
import commit_push as cp  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
    "CLAUDE_PROJECT_DIR": str(ROOT),
}
BRANCH = "feat/x"
# 署名樣式拆開寫，免得這個測試檔本身被 attribution_guard 當成署名
SIGNATURE = "Co-Authored-" + "By: Claude <x@example.com>"


class Base(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, GIT_ENV)
        self.env.start()
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.remote = base / "remote.git"
        self.repo = base / "repo"
        self.msg = base / "msg" / "commit-msg.txt"
        self.msg.parent.mkdir()
        self.git(base, "init", "-q", "--bare", str(self.remote))
        self.git(base, "init", "-q", "-b", "main", str(self.repo))
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        (self.repo / "a.txt").write_text("a\n", encoding="utf-8")
        self.git(self.repo, "add", "a.txt")
        self.git(self.repo, "commit", "-q", "-m", "chore: 初始")
        self.git(self.repo, "push", "-q", "origin", "main")
        self.git(self.repo, "switch", "-q", "-c", BRANCH)
        self.base_head = self.head()

    def tearDown(self):
        self.tmp.cleanup()
        self.env.stop()

    def git(self, cwd, *args):
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def head(self):
        return self.git(self.repo, "rev-parse", "HEAD")

    def write(self, name, text="x\n"):
        (self.repo / name).write_text(text, encoding="utf-8")

    def run_cp(self, *extra, message="feat(git): 新增測試功能", branch=BRANCH):
        self.msg.write_text(message + "\n", encoding="utf-8")
        argv = ["--repo", str(self.repo), "--branch", branch, "--message-file", str(self.msg),
                "--refs", "7", *extra]
        out = StringIO()
        with redirect_stdout(out):
            code = cp.main(argv)
        return code, json.loads(out.getvalue())


class Success(Base):
    def test_commit_and_push(self):
        self.write("b.txt")
        code, out = self.run_cp("--all")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(out["step"], "done")
        self.assertTrue(out["pushed"])
        self.assertEqual(out["files"], ["b.txt"])
        self.assertEqual(out["commit"], self.head())
        remote = self.git(self.remote, "rev-parse", f"refs/heads/{BRANCH}")
        self.assertEqual(remote, out["commit"])
        body = self.git(self.repo, "log", "-1", "--format=%B")
        self.assertTrue(body.endswith("\n\nRefs: #7"), body)
        upstream = self.git(self.repo, "rev-parse", "--abbrev-ref", "@{u}")
        self.assertEqual(upstream, f"origin/{BRANCH}")

    def test_no_push(self):
        self.write("b.txt")
        code, out = self.run_cp("--all", "--no-push")
        self.assertEqual(code, 0, out)
        self.assertFalse(out["pushed"])
        self.assertNotEqual(self.head(), self.base_head)
        r = subprocess.run(["git", "rev-parse", "--verify", "-q", f"refs/heads/{BRANCH}"],
                           cwd=self.remote, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)

    def test_add_only_given_paths(self):
        self.write("b.txt")
        self.write("c.txt")
        code, out = self.run_cp("--add", "b.txt", "--no-push")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["files"], ["b.txt"])
        self.assertIn("?? c.txt", self.git(self.repo, "status", "--porcelain"))

    def test_refs_not_duplicated(self):
        self.write("b.txt")
        code, out = self.run_cp("--all", "--no-push", message="feat(git): 新增測試功能\n\nRefs: #7")
        self.assertEqual(code, 0, out)
        body = self.git(self.repo, "log", "-1", "--format=%B")
        self.assertEqual(body.count("Refs: #7"), 1)
        self.assertTrue(self.msg.with_name("commit-msg.txt.final").is_file())


class Refused(Base):
    def assert_no_commit(self):
        self.assertEqual(self.head(), self.base_head)

    def test_bad_message_not_committed(self):
        self.write("b.txt")
        code, out = self.run_cp("--all", message="隨便改一下")
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "message")
        self.assertTrue(out["problems"])
        self.assert_no_commit()
        self.assertEqual(self.git(self.repo, "diff", "--cached", "--name-only"), "")

    def test_main_refused(self):
        self.git(self.repo, "switch", "-q", "main")
        self.write("b.txt")
        code, out = self.run_cp("--all", branch="main")
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "repo")
        self.assertIn("main", out["error"])
        self.assertEqual(self.head(), self.git(self.remote, "rev-parse", "refs/heads/main"))

    def test_branch_mismatch(self):
        self.write("b.txt")
        code, out = self.run_cp("--all", branch="feat/other")
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "repo")

    def test_not_worktree_root(self):
        (self.repo / "sub").mkdir()
        self.write("sub/b.txt")
        self.msg.write_text("feat(git): 新增測試功能\n", encoding="utf-8")
        code, out = cp.run(["--repo", str(self.repo / "sub"), "--branch", BRANCH,
                            "--message-file", str(self.msg), "--refs", "7", "--all"])
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "repo")

    def test_no_changes(self):
        code, out = self.run_cp("--all")
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "repo")
        self.assert_no_commit()

    def test_add_path_without_changes(self):
        self.write("b.txt")
        code, out = self.run_cp("--add", "a.txt")
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "stage")
        self.assert_no_commit()

    def test_signature_not_committed(self):
        self.write("b.txt")
        code, out = self.run_cp("--all", message="feat(git): 新增測試功能\n\n" + SIGNATURE)
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "message")
        self.assertTrue(any("署名" in p for p in out["problems"]))
        self.assert_no_commit()

    def test_signature_denied_by_hook(self):
        """訊息檢查之外，commit 那一步本身也經 attribution_guard 擋下。"""
        self.write("b.txt")
        self.git(self.repo, "add", "-A")
        final = self.msg.with_name("bad.final")
        final.write_text("feat(git): 新增測試功能\n\n" + SIGNATURE + "\n", encoding="utf-8")
        with self.assertRaises(cp.Fail) as ctx:
            cp.commit(self.repo, final, project_dir=ROOT)
        self.assertEqual(ctx.exception.step, "commit")
        hooks = [d["hook"] for d in ctx.exception.extra["denied"]]
        self.assertIn("attribution_guard.py", hooks)
        self.assert_no_commit()

    def test_hook_denied_reported(self):
        hook = Path(self.tmp.name) / "deny.py"
        hook.write_text(
            "import json\nprint(json.dumps({'hookSpecificOutput': {'permissionDecision': 'deny',"
            " 'permissionDecisionReason': 'no'}}))\n", encoding="utf-8")
        settings = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": f"{sys.executable} {hook}"}]}]}}
        self.write("b.txt")
        self.msg.write_text("feat(git): 新增測試功能\n", encoding="utf-8")
        code, out = cp.run(["--repo", str(self.repo), "--branch", BRANCH,
                            "--message-file", str(self.msg), "--refs", "7", "--all"],
                           settings=settings)
        self.assertEqual(code, 1)
        self.assertEqual(out["step"], "commit")
        self.assertEqual(out["denied"][0]["hook"], "deny.py")
        self.assert_no_commit()


class Usage(Base):
    def test_usage_errors(self):
        self.write("b.txt")
        cases = (
            [],                                    # 缺 --add／--all
            ["--add", "b.txt", "--all"],           # 兩個一起給
            ["--all", "--bogus"],
        )
        for extra in cases:
            with self.subTest(extra=extra):
                code, out = self.run_cp(*extra)
                self.assertEqual(code, 2)
                self.assertFalse(out["ok"])
                self.assertEqual(out["step"], "usage")
        self.assertEqual(self.head(), self.base_head)

    def test_bad_refs(self):
        self.msg.write_text("feat(git): 新增測試功能\n", encoding="utf-8")
        code, out = cp.run(["--repo", str(self.repo), "--branch", BRANCH,
                            "--message-file", str(self.msg), "--refs", "abc", "--all"])
        self.assertEqual(code, 2)


class WithRefs(unittest.TestCase):
    def test_appends_after_blank_line(self):
        self.assertEqual(cp.with_refs("feat: x\n\n內文\n", "3"), "feat: x\n\n內文\n\nRefs: #3\n")

    def test_joins_existing_footer_paragraph(self):
        self.assertEqual(cp.with_refs("feat: x\n\nDoc-Edit: r12\n", "3"),
                         "feat: x\n\nDoc-Edit: r12\nRefs: #3\n")


if __name__ == "__main__":
    unittest.main()
