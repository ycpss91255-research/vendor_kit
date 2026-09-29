"""mark_changes.py 的版本號行為：跑法 `python3 -m unittest discover -s test`。"""
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "script"))
import mark_changes  # noqa: E402


class VersionTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/decisions/review").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def write_page(self, body, backup):
        pathlib.Path("doc/decisions/review/09_x.md").write_text(body)
        pathlib.Path("doc/decisions/_backup/doc_decisions_review_09_x.pre_r1.md").write_text(backup)

    def test_rev_falls_back_to_stamped_version_without_local_rev(self):
        # 新 clone：沒有 .rev，正式檔檔頭是 v7 → 下一版是 v8，不從 v1 重來
        self.write_page("# 標題\n\n> 版本 v7\n\n新內容\n", "# 標題\n\n> 版本 v7\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        self.assertIn("> 版本 v8", pathlib.Path("doc/decisions/review/09_x.md").read_text())
        self.assertTrue(pathlib.Path("doc/decisions/_marked/09_x.v8.md").exists())

    def test_rev_takes_larger_of_local_and_stamped(self):
        self.write_page("# 標題\n\n> 版本 v3\n\n內容\n", "# 標題\n\n內容\n")
        marked = pathlib.Path("doc/decisions/_marked")
        marked.mkdir(parents=True)
        (marked / ".09_x.rev").write_text("5")
        mark_changes.build("09_x", "pre_r1")
        self.assertIn("> 版本 v6", pathlib.Path("doc/decisions/review/09_x.md").read_text())

    def test_all_three_copies_carry_same_version(self):
        self.write_page("# 標題\n\n新內容\n", "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        official = pathlib.Path("doc/decisions/review/09_x.md").read_text()
        plain = pathlib.Path("doc/decisions/_marked/09_x.v1.md").read_text()
        marked = pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").read_text()
        self.assertIn("> 版本 v1", official)
        self.assertEqual(official, plain)
        self.assertIn("版本 v1", marked)  # 新加的版本行會被標成新增，中間夾著 <mark>


if __name__ == "__main__":
    unittest.main()
