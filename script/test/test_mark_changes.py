"""mark_changes.py 的版本號行為：跑法 `python3 -m unittest discover -s script/test`。"""
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
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

    def test_rev_continues_from_tracked_table(self):
        # 新 clone：_marked/ 是空的，版本號照進 git 的表接下去，不從 v1 重來
        self.write_page("# 標題\n\n新內容\n", "# 標題\n\n舊內容\n")
        table = pathlib.Path("doc/decisions/review_log/versions.json")
        table.parent.mkdir(parents=True)
        table.write_text('{"09_x": 7}\n')
        mark_changes.build("09_x", "pre_r1")
        self.assertTrue(pathlib.Path("doc/decisions/_marked/09_x.v8.md").exists())
        self.assertIn('"09_x": 8', table.read_text())

    def test_official_and_plain_copy_have_no_version_line(self):
        # 版本號只在檔名：正式檔與正文副本內容相同，裡面不寫版本
        body = "# 標題\n\n新內容\n"
        self.write_page(body, "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        self.assertEqual(pathlib.Path("doc/decisions/review/09_x.md").read_text(), body)
        self.assertEqual(pathlib.Path("doc/decisions/_marked/09_x.v1.md").read_text(), body)
        self.assertTrue(pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").exists())


if __name__ == "__main__":
    unittest.main()
