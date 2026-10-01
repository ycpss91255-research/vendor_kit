"""worktree.py：用暫存的 origin／主 repo 測 add 與 remove。跑法 `python3 -m unittest discover -s script/workflow/test`。"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import worktree as w  # noqa: E402


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


def run(*argv):
    buf = StringIO()
    with redirect_stdout(buf):
        code = w.main(list(argv))
    return code, json.loads(buf.getvalue())


class Worktree(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ws = pathlib.Path(self.tmp.name)
        origin = ws / "origin.git"
        sh(ws, "git", "init", "-q", "--bare", "-b", "main", str(origin))
        self.repo = ws / "src"
        sh(ws, "git", "clone", "-q", str(origin), str(self.repo))
        for k, v in (("user.name", "t"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
            sh(self.repo, "git", "config", k, v)
        (self.repo / "a.txt").write_text("a\n")
        sh(self.repo, "git", "add", "a.txt")
        sh(self.repo, "git", "commit", "-q", "-m", "init")
        sh(self.repo, "git", "push", "-q", "origin", "HEAD:main")
        self.ws = ws

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_creates_worktree_at_fixed_location(self):
        code, out = run("add", "feat/x", "--repo", str(self.repo))
        self.assertEqual(code, 0, out)
        path = self.ws / "worktree" / "branch" / "feat" / "x"
        self.assertEqual(out["path"], str(path))
        self.assertTrue((path / "a.txt").exists())

    def test_add_from_inside_worktree_uses_main_repo(self):
        run("add", "feat/x", "--repo", str(self.repo))
        inner = self.ws / "worktree" / "branch" / "feat" / "x"
        code, out = run("add", "feat/y", "--repo", str(inner))
        self.assertEqual(code, 0, out)
        self.assertEqual(out["path"], str(self.ws / "worktree" / "branch" / "feat" / "y"))

    def test_add_existing_fails(self):
        run("add", "feat/x", "--repo", str(self.repo))
        code, out = run("add", "feat/x", "--repo", str(self.repo))
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertIn("已存在", out["error"])

    def test_add_existing_local_branch_fails(self):
        sh(self.repo, "git", "branch", "feat/z")
        code, out = run("add", "feat/z", "--repo", str(self.repo))
        self.assertEqual(code, 1)
        self.assertIn("本機分支已存在", out["error"])

    def test_bad_branch_name_fails(self):
        code, out = run("add", "../evil", "--repo", str(self.repo))
        self.assertEqual(code, 1)
        self.assertIn("不合法", out["error"])

    def test_remove_pushed_branch(self):
        run("add", "feat/x", "--repo", str(self.repo))
        path = self.ws / "worktree" / "branch" / "feat" / "x"
        code, out = run("remove", "feat/x", "--repo", str(self.repo))
        self.assertEqual(code, 0, out)
        self.assertTrue(out["removed_worktree"] and out["removed_branch"])
        self.assertFalse(path.exists())
        self.assertFalse(w.branch_exists(self.repo, "feat/x"))

    def test_remove_keeps_remote_branch(self):
        run("add", "feat/x", "--repo", str(self.repo))
        path = self.ws / "worktree" / "branch" / "feat" / "x"
        (path / "b.txt").write_text("b\n")
        sh(path, "git", "add", "b.txt")
        sh(path, "git", "commit", "-q", "-m", "b")
        sh(path, "git", "push", "-q", "origin", "feat/x")
        code, out = run("remove", "feat/x", "--repo", str(self.repo))
        self.assertEqual(code, 0, out)
        remote = subprocess.run(["git", "-C", str(self.repo), "ls-remote", "--heads", "origin", "feat/x"],
                                capture_output=True, text=True).stdout
        self.assertIn("refs/heads/feat/x", remote)

    def test_remove_unpushed_commit_refused_without_force(self):
        run("add", "feat/x", "--repo", str(self.repo))
        path = self.ws / "worktree" / "branch" / "feat" / "x"
        (path / "b.txt").write_text("b\n")
        sh(path, "git", "add", "b.txt")
        sh(path, "git", "commit", "-q", "-m", "b")
        code, out = run("remove", "feat/x", "--repo", str(self.repo))
        self.assertEqual(code, 1)
        self.assertIn("還沒推上遠端", out["error"])
        self.assertTrue(path.exists())
        code, out = run("remove", "feat/x", "--repo", str(self.repo), "--force")
        self.assertEqual(code, 0, out)
        self.assertFalse(path.exists())

    def test_remove_missing_fails(self):
        code, out = run("remove", "feat/none", "--repo", str(self.repo))
        self.assertEqual(code, 1)
        self.assertIn("都不存在", out["error"])


if __name__ == "__main__":
    unittest.main()
