"""check_terms.py 的目錄規則：跑法 `python3 -m unittest discover -s script/test`。"""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_terms  # noqa: E402


class LayoutTest(unittest.TestCase):
    def test_docs_dir_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "doc").mkdir()
            self.assertEqual(check_terms.layout_errors(root), [])
            (root / "docs").mkdir()
            errs = check_terms.layout_errors(root)
            self.assertEqual(len(errs), 1)
            self.assertIn("一律用 doc/，不用 docs/", errs[0])

    def test_docs_file_is_not_a_dir(self):
        # 只擋目錄；同名檔案不是這條規則要管的
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "docs").write_text("")
            self.assertEqual(check_terms.layout_errors(root), [])


if __name__ == "__main__":
    unittest.main()
