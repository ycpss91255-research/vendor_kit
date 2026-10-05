"""round.py 的輪次編號：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "round.py"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


class RoundTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self._tmp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "commit.gpgsign", "false")

    def tearDown(self):
        self._tmp.cleanup()

    def commit(self, msg):
        git(self.repo, "commit", "-q", "--allow-empty", "-m", msg)

    def backup(self, *names):
        d = self.repo / "doc/decisions/_backup"
        d.mkdir(parents=True, exist_ok=True)
        for n in names:
            (d / n).write_text("x\n")

    def run_round(self, *args):
        r = subprocess.run([sys.executable, str(SCRIPT), *args, "--repo", str(self.repo)],
                           capture_output=True, text=True)
        lines = r.stdout.splitlines()
        self.assertEqual(len(lines), 1, r.stdout + r.stderr)
        return r.returncode, json.loads(lines[0])

    def test_nothing_gives_r1(self):
        code, out = self.run_round("next")
        self.assertEqual(code, 0)
        self.assertEqual(out, {"ok": True, "max": 0, "next": "r1", "backup_max": None, "footer_max": None})

    def test_commits_without_footer_and_empty_backup_dir(self):
        self.commit("feat: x")
        (self.repo / "doc/decisions/_backup").mkdir(parents=True)
        code, out = self.run_round("next")
        self.assertEqual((code, out["max"], out["next"], out["backup_max"], out["footer_max"]), (0, 0, "r1", None, None))

    def test_backup_only(self):
        self.backup("doc_contract_01_purpose.pre_r7.md", "README.pre_r3.md", "note.txt")
        code, out = self.run_round("next")
        self.assertEqual((code, out["max"], out["next"], out["backup_max"], out["footer_max"]), (0, 7, "r8", 7, None))

    def test_footer_only(self):
        self.commit("docs: a\n\nDoc-Edit: r4")
        self.commit("docs: b\n\nRefs: #1\nDoc-Edit: r9")
        self.commit("docs: c\n\n說明 Doc-Edit: r99 不在行首不算")
        code, out = self.run_round("next")
        self.assertEqual((code, out["max"], out["next"], out["backup_max"], out["footer_max"]), (0, 9, "r10", None, 9))

    def test_both_take_larger(self):
        self.backup("README.pre_r20.md")
        self.commit("docs: a\n\nDoc-Edit: r15")
        _, out = self.run_round("next")
        self.assertEqual((out["max"], out["next"], out["backup_max"], out["footer_max"]), (20, "r21", 20, 15))
        self.commit("docs: b\n\nDoc-Edit: r30")
        _, out = self.run_round("next")
        self.assertEqual((out["max"], out["next"], out["backup_max"], out["footer_max"]), (30, "r31", 20, 30))

    def test_sequenced_backup_counts_round(self):
        self.backup("doc_contract_02_invariants.pre_r12.2.md", "doc_contract_03_output.pre_r11.csv")
        _, out = self.run_round("next")
        self.assertEqual((out["max"], out["next"]), (12, "r13"))

    def test_check_ok(self):
        self.backup("README.pre_r5.md")
        code, out = self.run_round("check", "r6")
        self.assertEqual(code, 0)
        self.assertTrue(out["ok"])
        self.assertEqual((out["round"], out["expected"], out["max"]), ("r6", "r6", 5))

    def test_check_reuse_fails(self):
        self.backup("README.pre_r5.md")
        for rnd in ("r5", "r4"):
            code, out = self.run_round("check", rnd)
            self.assertEqual(code, 1, rnd)
            self.assertFalse(out["ok"])
            self.assertEqual((out["round"], out["expected"]), (rnd, "r6"))
            self.assertIn("重用", out["error"])

    def test_check_skip_fails(self):
        self.commit("docs: a\n\nDoc-Edit: r5")
        code, out = self.run_round("check", "r8")
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertEqual(out["expected"], "r6")
        self.assertIn("跳號", out["error"])

    def test_check_bad_format_fails(self):
        for rnd in ("6", "R6", "r6a", "pre_r6"):
            code, out = self.run_round("check", rnd)
            self.assertEqual(code, 1, rnd)
            self.assertFalse(out["ok"])
            self.assertIn("格式", out["error"])

    def test_not_git_repo(self):
        other = pathlib.Path(self._tmp.name) / "plain"
        other.mkdir()
        r = subprocess.run([sys.executable, str(SCRIPT), "next", "--repo", str(other)],
                           capture_output=True, text=True, cwd=self._tmp.name,
                           env={**os.environ, "GIT_CEILING_DIRECTORIES": self._tmp.name})
        self.assertEqual(r.returncode, 2)
        self.assertFalse(json.loads(r.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
