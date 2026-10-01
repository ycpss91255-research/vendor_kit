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


if __name__ == "__main__":
    unittest.main()
