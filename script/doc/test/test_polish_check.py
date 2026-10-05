"""polish_check.py 的越界判斷與還原：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "polish_check.py"


class PolishCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, lines):
        p = self.dir / name
        p.write_text("".join(l + "\n" for l in lines), encoding="utf-8")
        return p

    def setup_files(self, base, pre, post):
        return self.write("base.md", base), self.write("pre.md", pre), self.write("post.md", post)

    def run_check(self, *paths, fix=False):
        cmd = [sys.executable, str(SCRIPT), *map(str, paths)] + (["--fix"] if fix else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout.strip().splitlines()
        self.assertEqual(len(out), 1, r.stdout + r.stderr)
        return r.returncode, json.loads(out[0])

    BASE = ["a", "b", "c", "d", "e"]
    PRE = ["a", "B", "c", "d", "e"]  # 這一輪改了第 2 行

    def test_only_round_lines_changed(self):
        files = self.setup_files(self.BASE, self.PRE, ["a", "B2", "c", "d", "e"])
        code, res = self.run_check(*files)
        self.assertEqual(code, 0)
        self.assertEqual(res, {"ok": True, "round_changed_lines": 1, "violations": [], "reverted": False})

    def test_out_of_range_then_fix_then_clean(self):
        base, pre, post = self.setup_files(self.BASE, self.PRE, ["a", "B", "c", "D", "e"])
        code, res = self.run_check(base, pre, post)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertFalse(res["reverted"])
        self.assertEqual(res["violations"], [{"pre_lines": [4, 4], "post_lines": [4, 4], "post_text": "D\n"}])
        self.assertEqual(post.read_text(encoding="utf-8"), "a\nB\nc\nD\ne\n")  # 沒 --fix 不動檔

        code, res = self.run_check(base, pre, post, fix=True)
        self.assertEqual(code, 0)
        self.assertTrue(res["ok"])
        self.assertTrue(res["reverted"])
        self.assertEqual(len(res["violations"]), 1)
        self.assertEqual(post.read_text(encoding="utf-8"), pre.read_text(encoding="utf-8"))

        code, res = self.run_check(base, pre, post)
        self.assertEqual(code, 0)
        self.assertEqual(res["violations"], [])

    def test_equal_length_replace_line_by_line(self):
        # 第 2、3 行一起被改（等長 replace）：第 2 行在範圍內保留，第 3 行越界還原
        base, pre, post = self.setup_files(self.BASE, self.PRE, ["a", "B2", "C", "d", "e"])
        code, res = self.run_check(base, pre, post, fix=True)
        self.assertEqual(code, 0)
        self.assertEqual([v["pre_lines"] for v in res["violations"]], [[3, 3]])
        self.assertEqual(post.read_text(encoding="utf-8"), "a\nB2\nc\nd\ne\n")

    def test_insert_adjacent_kept_far_reverted(self):
        # 緊鄰第 2 行（範圍內）之後插入保留；第 4 行之後插入越界被還原
        base, pre, post = self.setup_files(self.BASE, self.PRE, ["a", "B", "new1", "c", "d", "new2", "e"])
        code, res = self.run_check(base, pre, post, fix=True)
        self.assertEqual(code, 0)
        self.assertEqual([v["post_text"] for v in res["violations"]], ["new2\n"])
        self.assertEqual(post.read_text(encoding="utf-8"), "a\nB\nnew1\nc\nd\ne\n")

    def test_base_equals_pre_any_change_violates(self):
        base, pre, post = self.setup_files(self.BASE, self.BASE, ["a", "B", "c", "d", "e"])
        code, res = self.run_check(base, pre, post)
        self.assertEqual(code, 1)
        self.assertEqual(res["round_changed_lines"], 0)
        self.assertEqual(len(res["violations"]), 1)

    def test_missing_file_exit_2(self):
        base, pre, _ = self.setup_files(self.BASE, self.PRE, self.PRE)
        code, res = self.run_check(base, pre, self.dir / "nope.md")
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])
        self.assertIn("error", res)


class RoundBaseTest(unittest.TestCase):
    """--repo、--round 用法：基準照 backup.py diff 的順序自己取（基準備份 → HEAD → 空內容）。"""

    REL = "doc/page.md"
    BACKUP = "doc/decisions/_backup/doc_page.pre_r7.md"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "repo"
        self.root.mkdir()
        self.side = pathlib.Path(self.tmp.name) / "side"
        self.side.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("config", "commit.gpgsign", "false")
        (self.root / "keep.md").write_text("x\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def write(self, path, lines):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(l + "\n" for l in lines), encoding="utf-8")
        return path

    def commit_page(self, lines):
        self.write(self.root / self.REL, lines)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "page")

    def run_round(self, pre, fix=False, rnd="r7"):
        cmd = [sys.executable, str(SCRIPT), "--repo", str(self.root), "--round", rnd, self.REL, str(pre)]
        r = subprocess.run(cmd + (["--fix"] if fix else []), capture_output=True, text=True)
        out = r.stdout.strip().splitlines()
        self.assertEqual(len(out), 1, r.stdout + r.stderr)
        return r.returncode, json.loads(out[0])

    def post_text(self):
        return (self.root / self.REL).read_text(encoding="utf-8")

    def test_backup_base_preferred_over_head(self):
        # HEAD 跟基準備份不同：範圍要照基準備份算（第 2 行），不是照 HEAD（第 3 行）
        self.commit_page(["a", "b", "C", "d"])
        backup_file = self.write(self.root / self.BACKUP, ["a", "b", "c", "d"])
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "backup")
        pre = self.write(self.side / "pre.md", ["a", "B", "c", "d"])
        self.write(self.root / self.REL, ["a", "B2", "c", "d"])
        code, res = self.run_round(pre)
        self.assertEqual(code, 0, res)
        self.assertEqual(res["base_kind"], "backup")
        self.assertEqual(pathlib.Path(res["base"]).resolve(), backup_file.resolve())
        self.assertEqual(res["round_changed_lines"], 1)
        self.assertEqual(res["violations"], [])

    def test_head_base_when_no_backup(self):
        self.commit_page(["a", "b", "c", "d"])
        pre = self.write(self.side / "pre.md", ["a", "B", "c", "d"])
        self.write(self.root / self.REL, ["a", "B2", "c", "D"])
        code, res = self.run_round(pre)
        self.assertEqual(code, 1)
        self.assertEqual(res["base_kind"], "HEAD")
        self.assertIsNone(res["base"])
        self.assertEqual(res["round_changed_lines"], 1)
        self.assertEqual([v["pre_lines"] for v in res["violations"]], [[4, 4]])
        self.assertEqual(self.post_text(), "a\nB2\nc\nD\n")  # 沒 --fix 不動檔

    def test_none_base_whole_file_in_range(self):
        # 不在 HEAD、也沒有基準備份（這一輪新建的檔）：整份都算這一輪的新增
        pre = self.write(self.side / "pre.md", ["a", "b", "c"])
        self.write(self.root / self.REL, ["A", "b", "C"])
        code, res = self.run_round(pre)
        self.assertEqual(code, 0, res)
        self.assertEqual(res["base_kind"], "none")
        self.assertIsNone(res["base"])
        self.assertEqual(res["round_changed_lines"], 3)
        self.assertEqual(res["violations"], [])

    def test_fix_reverts_out_of_range_lines(self):
        self.commit_page(["a", "b", "c", "d", "e"])
        pre = self.write(self.side / "pre.md", ["a", "B", "c", "d", "e"])
        self.write(self.root / self.REL, ["a", "B2", "C", "d", "new", "e"])
        code, res = self.run_round(pre, fix=True)
        self.assertEqual(code, 0, res)
        self.assertTrue(res["ok"])
        self.assertTrue(res["reverted"])
        self.assertEqual(res["base_kind"], "HEAD")
        self.assertEqual(self.post_text(), "a\nB2\nc\nd\ne\n")

        code, res = self.run_round(pre)
        self.assertEqual(code, 0)
        self.assertEqual(res["violations"], [])
        self.assertFalse(res["reverted"])

    def test_no_temp_files_written(self):
        self.commit_page(["a", "b"])
        pre = self.write(self.side / "pre.md", ["a", "B"])
        self.write(self.root / self.REL, ["a", "B"])
        before = sorted(p.relative_to(self.tmp.name) for p in pathlib.Path(self.tmp.name).rglob("*"))
        code, _ = self.run_round(pre, fix=True)
        self.assertEqual(code, 0)
        after = sorted(p.relative_to(self.tmp.name) for p in pathlib.Path(self.tmp.name).rglob("*"))
        self.assertEqual(before, after)

    def test_usage_errors_exit_2(self):
        pre = self.write(self.side / "pre.md", ["a"])
        code, res = self.run_round(pre, rnd="7")
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])
        r = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root), self.REL, str(pre)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertFalse(json.loads(r.stdout)["ok"])
        r = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.side), "--round", "r7", self.REL, str(pre)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("git repo", json.loads(r.stdout)["error"])

    def test_missing_post_exit_2(self):
        self.commit_page(["a"])
        (self.root / self.REL).unlink()
        pre = self.write(self.side / "pre.md", ["a"])
        code, res = self.run_round(pre)
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])
        self.assertEqual(res["base_kind"], "HEAD")


if __name__ == "__main__":
    unittest.main()
