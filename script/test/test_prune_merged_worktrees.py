"""prune_merged_worktrees.py 的測試：臨時 git repo＋worktree，gh 用 PATH 裡的假腳本。

跑法：python3 -m unittest discover -s script/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "prune_merged_worktrees.py"

FAKE_GH = """#!/bin/sh
[ -n "$FAKE_GH_FAIL" ] && exit 1
head=""
while [ $# -gt 0 ]; do
  [ "$1" = "--head" ] && head="$2"
  shift
done
for b in $FAKE_GH_MERGED; do
  [ "$b" = "$head" ] && { echo 1; exit 0; }
done
echo 0
"""


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True,
                          text=True, check=True).stdout


class PruneMergedWorktreesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name).resolve()
        self.base = base
        self.src = base / "src"
        origin = base / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.src)], check=True)
        git(self.src, "config", "user.email", "t@example.com")
        git(self.src, "config", "user.name", "t")
        (self.src / "a.txt").write_text("a\n")
        git(self.src, "add", "a.txt")
        git(self.src, "commit", "-qm", "init")
        git(self.src, "remote", "add", "origin", str(origin))
        git(self.src, "push", "-q", "origin", "main")
        bindir = base / "bin"
        bindir.mkdir()
        gh = bindir / "gh"
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        self.env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.src),
                        PATH=f"{bindir}{os.pathsep}{os.environ['PATH']}")
        self.env.pop("FAKE_GH_FAIL", None)

    def tearDown(self):
        self.tmp.cleanup()

    def add_wt(self, rel, branch, commit=True):
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        git(self.src, "worktree", "add", "-q", "-b", branch, str(path))
        if commit:
            (path / f"{branch.replace('/', '_')}.txt").write_text("x\n")
            git(path, "add", "-A")
            git(path, "commit", "-qm", branch)
        return path

    def run_hook(self, merged=(), fail=False):
        env = dict(self.env, FAKE_GH_MERGED=" ".join(merged))
        if fail:
            env["FAKE_GH_FAIL"] = "1"
        proc = subprocess.run([sys.executable, str(HOOK)], input="{}", capture_output=True,
                              text=True, env=env, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout.strip()
        return json.loads(out)["hookSpecificOutput"] if out else None

    def branches(self):
        return git(self.src, "branch", "--format=%(refname:short)").split()

    def test_merged_clean_removed(self):
        wt = self.add_wt("worktree/pr/1", "feat/a")
        out = self.run_hook(merged=["feat/a"])
        self.assertFalse(wt.exists())
        self.assertEqual(out["hookEventName"], "SessionStart")
        self.assertIn(str(wt), out["additionalContext"])
        self.assertNotIn(str(wt), git(self.src, "worktree", "list"))
        # 分支沒進 main，branch -d 失敗就留著
        self.assertIn("feat/a", self.branches())

    def test_merged_by_ancestry_removed_with_branch(self):
        wt = self.add_wt("worktree/pr/2", "feat/b")
        git(self.src, "merge", "-q", "--no-ff", "-m", "merge", "feat/b")
        git(self.src, "push", "-q", "origin", "main")
        out = self.run_hook()
        self.assertFalse(wt.exists())
        self.assertIn(str(wt), out["additionalContext"])
        self.assertNotIn("feat/b", self.branches())

    def test_merged_dirty_kept_with_notice(self):
        wt = self.add_wt("worktree/pr/3", "feat/c")
        (wt / "new1.txt").write_text("n\n")
        (wt / "new2.txt").write_text("n\n")
        out = self.run_hook(merged=["feat/c"])
        self.assertTrue(wt.exists())
        self.assertIn(str(wt), out["additionalContext"])
        self.assertIn("2 個未提交", out["additionalContext"])

    def test_unmerged_untouched(self):
        wt = self.add_wt("worktree/pr/4", "feat/d")
        fresh = self.add_wt("worktree/branch/fresh", "fresh", commit=False)
        self.assertIsNone(self.run_hook())
        self.assertTrue(wt.exists())
        self.assertTrue(fresh.exists())

    def test_gh_failure_untouched(self):
        wt = self.add_wt("worktree/pr/5", "feat/e")
        git(self.src, "merge", "-q", "--no-ff", "-m", "merge", "feat/e")
        git(self.src, "push", "-q", "origin", "main")
        self.assertIsNone(self.run_hook(merged=["feat/e"], fail=True))
        self.assertTrue(wt.exists())

    def test_outside_worktree_dir_untouched(self):
        wt = self.add_wt("elsewhere/x", "feat/f")
        self.assertIsNone(self.run_hook(merged=["feat/f"]))
        self.assertTrue(wt.exists())

    def test_session_in_linked_worktree_uses_main(self):
        here = self.add_wt("worktree/pr/6", "feat/g")
        wt = self.add_wt("worktree/pr/7", "feat/h")
        self.env["CLAUDE_PROJECT_DIR"] = str(here)
        out = self.run_hook(merged=["feat/g", "feat/h"])
        self.assertFalse(wt.exists())
        self.assertTrue(here.exists())  # 目前 session 所在的 worktree 不動
        self.assertIn(str(wt), out["additionalContext"])


if __name__ == "__main__":
    unittest.main()
