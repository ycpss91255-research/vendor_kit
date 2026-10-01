"""pack_review.py 的版號、zip 內檔名、versions.json 紀錄與檢查：跑法 `python3 -m unittest discover -s script/test`。"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import mark_changes  # noqa: E402
import pack_review  # noqa: E402

VERSIONS = pathlib.Path("doc/review/versions.json")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


class PackReviewTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        git("init", "-q")
        git("config", "user.email", "t@example.com")
        git("config", "user.name", "t")
        git("config", "commit.gpgsign", "false")
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/contract/03_messages.md").write_text("# 03\n\n[名詞](../../GLOSSARY.md)\n")
        pathlib.Path("doc/contract/03_messages.csv").write_text("code,status\nVK0001,active\n")
        pathlib.Path("doc/contract/04_interface.md").write_text("# 04\n")
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n")
        self.first = self.commit()
        VERSIONS.parent.mkdir(parents=True)
        VERSIONS.write_text(json.dumps({"review_zip": 1, "pages": {
            "03_messages": [{"v": 12, "commit": self.first}],
            "04_interface": [{"v": 17, "commit": self.first}],
        }}))
        for name in ("03_messages", "04_interface", "GLOSSARY.md"):
            mark_changes.build_from_version(name)
        pathlib.Path("note.md").write_text("說明")
        self.out = pathlib.Path("out")
        self.head = self.commit()

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def commit(self):
        git("add", "-A")
        git("commit", "-q", "-m", "c")
        return git("rev-parse", "HEAD")

    def table(self):
        return json.loads(VERSIONS.read_text())

    def test_zip_names_carry_version(self):
        path, arcnames = pack_review.pack(["03_messages", "04_interface", "GLOSSARY.md"], self.out,
                                          pathlib.Path("note.md"))
        self.assertEqual(path.name, "review_v2.zip")
        expected = ["note.md",
                    "03_messages.v13.marked.md", "03_messages.v13.md", "03_messages.v13.csv",
                    "04_interface.v18.marked.md", "04_interface.v18.md",
                    "GLOSSARY.v1.marked.md", "GLOSSARY.v1.md"]
        self.assertEqual(arcnames, expected)
        with zipfile.ZipFile(path) as zf:
            self.assertEqual(zf.namelist(), expected)
            self.assertEqual(zf.read("GLOSSARY.v1.md").decode(), "# 名詞\n")
        # repo 裡的檔名不帶版本號
        self.assertEqual(sorted(p.name for p in pathlib.Path("doc/review/03_messages").iterdir()),
                         ["03_messages.csv", "03_messages.marked.md", "03_messages.md"])

    def test_records_version_and_head(self):
        pack_review.pack(["03_messages", "GLOSSARY.md"], self.out)
        table = self.table()
        self.assertEqual(table["review_zip"], 2)
        self.assertEqual(table["pages"]["03_messages"],
                         [{"v": 12, "commit": self.first}, {"v": 13, "commit": self.head}])
        self.assertEqual(table["pages"]["GLOSSARY"], [{"v": 1, "commit": self.head}])
        self.assertEqual(table["pages"]["04_interface"], [{"v": 17, "commit": self.first}])

    def test_version_increments(self):
        path, _ = pack_review.pack(["04_interface"], self.out)
        self.assertEqual(path.name, "review_v2.zip")
        path, arcnames = pack_review.pack(["04_interface"], self.out)
        self.assertEqual(path.name, "review_v3.zip")
        self.assertIn("04_interface.v19.md", arcnames)
        self.assertEqual(self.table()["review_zip"], 3)

    def assert_not_bumped(self):
        self.assertEqual(self.table()["review_zip"], 1)
        self.assertEqual(self.table()["pages"]["04_interface"], [{"v": 17, "commit": self.first}])
        self.assertFalse(self.out.exists())

    def test_uncommitted_official_fails(self):
        pathlib.Path("doc/contract/04_interface.md").write_text("# 04\n\n改了\n")
        mark_changes.build_from_version("04_interface")
        with self.assertRaises(SystemExit) as cm:
            pack_review.pack(["04_interface"], self.out)
        self.assertIn("未 commit", str(cm.exception))
        self.assert_not_bumped()

    def test_uncommitted_csv_fails(self):
        pathlib.Path("doc/contract/03_messages.csv").write_text("code,status\nVK0001,retired\n")
        mark_changes.build_from_version("03_messages")
        with self.assertRaises(SystemExit) as cm:
            pack_review.pack(["03_messages"], self.out)
        self.assertIn("03_messages.csv", str(cm.exception))

    def test_staged_official_fails(self):
        pathlib.Path("doc/contract/04_interface.md").write_text("# 04\n\n改了\n")
        git("add", "doc/contract/04_interface.md")
        with self.assertRaises(SystemExit):
            pack_review.pack(["04_interface"], self.out)
        self.assert_not_bumped()

    def test_stale_copy_fails(self):
        pathlib.Path("doc/contract/04_interface.md").write_text("# 04\n\n改了\n")
        self.commit()
        with self.assertRaises(SystemExit) as cm:
            pack_review.pack(["04_interface"], self.out)
        self.assertIn("mark_changes.py", str(cm.exception))
        self.assert_not_bumped()

    def test_missing_file_stops_without_bumping(self):
        (pathlib.Path("doc/review/04_interface") / "04_interface.md").unlink()
        with self.assertRaises(SystemExit) as cm:
            pack_review.pack(["04_interface"], self.out)
        self.assertIn("04_interface.md", str(cm.exception))
        self.assert_not_bumped()

    def test_missing_note_stops(self):
        with self.assertRaises(SystemExit):
            pack_review.pack(["04_interface"], self.out, pathlib.Path("nope.md"))
        self.assert_not_bumped()


if __name__ == "__main__":
    unittest.main()
