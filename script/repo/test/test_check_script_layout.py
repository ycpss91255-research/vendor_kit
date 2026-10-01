"""check_script_layout.py 的目錄規則：跑法 `python3 -m unittest discover -s script/repo/test`。"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_script_layout as c  # noqa: E402

GOOD = [
    "README.md",
    "script/README.md",
    "script/doc/README.md",
    "script/doc/check_terms.py",
    "script/doc/test/test_check_terms.py",
    "script/repo/README.md",
    "script/repo/check_script_layout.py",
    "script/repo/test/test_check_script_layout.py",
]


class LayoutErrors(unittest.TestCase):
    def test_good_layout_passes(self):
        self.assertEqual(c.layout_errors(GOOD), [])

    def test_script_at_top_level_fails(self):
        errs = c.layout_errors(GOOD + ["script/check_x.py"])
        self.assertEqual(len(errs), 1)
        self.assertTrue(errs[0].startswith("script/check_x.py:"))

    def test_category_without_readme_fails(self):
        files = [f for f in GOOD if f != "script/repo/README.md"]
        self.assertEqual(c.layout_errors(files), ["script/repo/:缺 README.md"])

    def test_bad_category_name_fails(self):
        for name in ["Doc", "doc_tool", "文件"]:
            with self.subTest(name=name):
                errs = c.layout_errors(GOOD + [f"script/{name}/README.md", f"script/{name}/x.py"])
                self.assertTrue(errs)
                self.assertTrue(all(e.startswith(f"script/{name}/") for e in errs))

    def test_hyphen_and_digits_allowed(self):
        self.assertEqual(c.layout_errors(GOOD + ["script/ci-2/README.md", "script/ci-2/x.py"]), [])

    def test_subdir_other_than_test_fails(self):
        errs = c.layout_errors(GOOD + ["script/doc/lib/x.py"])
        self.assertEqual(len(errs), 1)
        self.assertTrue(errs[0].startswith("script/doc/lib/x.py:"))

    def test_files_outside_script_ignored(self):
        self.assertEqual(c.layout_errors(GOOD + ["doc/x.py", "scripts/y.py"]), [])


class EndToEnd(unittest.TestCase):
    """在暫存 git repo 裡跑腳本：只看 git ls-files -co --exclude-standard。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        for f in GOOD:
            self.write(f)
        (self.root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x\n", encoding="utf-8")

    def run_main(self):
        old = c.ROOT
        c.ROOT = self.root
        try:
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = c.main()
            return code, buf.getvalue()
        finally:
            c.ROOT = old

    def test_good_tree_prints_ok(self):
        self.write("script/doc/__pycache__/check_terms.cpython-312.pyc")  # 被忽略的檔不算
        self.assertEqual(self.run_main(), (0, "OK\n"))

    def test_top_level_script_fails(self):
        self.write("script/check_x.py")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("script/check_x.py:", out)


if __name__ == "__main__":
    unittest.main()
