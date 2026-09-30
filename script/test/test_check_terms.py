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


class CsvTest(unittest.TestCase):
    def test_csv_text_fields_scanned(self):
        # CSV 的文字欄也要擋 _Avoid_ 詞；位置報 <代碼>:<欄名>，固定值域的欄不掃
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "doc/contract").mkdir(parents=True)
            (root / "doc/contract/03_messages.csv").write_text(
                "\ufeffcode,status,level,disposition,situation,message,next_step\n"
                "VK0001,舊詞,舊詞,舊詞處置,舊詞出現,正常,\"第一行\n舊詞在第二行\"\n",
                encoding="utf-8",
            )
            cells = check_terms.csv_cells(root)
        fields = ["VK0001:disposition", "VK0001:situation", "VK0001:message", "VK0001:next_step"]
        self.assertEqual([c[1] for c in cells], fields)
        patterns = [("舊詞", check_terms.re.compile("舊詞"))]
        hits = {where: check_terms.line_hits(rel, value, patterns) for rel, where, value in cells}
        self.assertEqual(hits, dict(zip(fields, [["舊詞"], ["舊詞"], [], ["舊詞"]])))

    def test_quote_marker_and_u_tag_apply_to_cells(self):
        patterns = [("舊詞", check_terms.re.compile("舊詞"))]
        self.assertEqual(check_terms.line_hits("x.csv", "舊名：舊詞", patterns), [])
        self.assertEqual(check_terms.line_hits("x.csv", "<u>底線</u>", patterns), ["<u>（改用 <ins>）"])


if __name__ == "__main__":
    unittest.main()
