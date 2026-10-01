"""pack_review.py 的版號、zip 內檔名、versions.json 紀錄與檢查：跑法 `python3 -m unittest discover -s script/doc/test`。"""
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
                         [{"v": 12, "commit": self.first}, {"v": 13, "commit": self.head, "replied": False}])
        self.assertEqual(table["pages"]["GLOSSARY"], [{"v": 1, "commit": self.head, "replied": False}])
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

    def run_main(self, *argv):
        old = sys.argv
        sys.argv = ["pack_review.py", *argv]
        try:
            pack_review.main()
        finally:
            sys.argv = old

    def test_main_without_out_fails(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_main("04_interface")
        self.assertEqual(cm.exception.code, 2)
        self.assert_not_bumped()
        self.assertFalse(list(pathlib.Path(".").glob("**/review_v*.zip")))

    def test_replied_marks_only_that_entry(self):
        pack_review.pack(["04_interface"], self.out)
        before = self.table()
        self.run_main("--replied", "04_interface=18", "04_interface=17")
        table = self.table()
        self.assertEqual(table["pages"]["04_interface"],
                         [{"v": 17, "commit": self.first, "replied": True},
                          {"v": 18, "commit": self.head, "replied": True}])
        # 不打包、不取號：review_zip 與其他鍵不變，也沒有新 zip
        self.assertEqual(table["review_zip"], before["review_zip"])
        self.assertEqual(table["pages"]["03_messages"], before["pages"]["03_messages"])
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["review_v2.zip"])

    def test_replied_accepts_root_file_key(self):
        pack_review.pack(["GLOSSARY.md"], self.out)
        self.run_main("--replied", "GLOSSARY=1")
        self.assertEqual(self.table()["pages"]["GLOSSARY"][0]["replied"], True)

    def test_replied_missing_entry_fails_and_changes_nothing(self):
        before = VERSIONS.read_text()
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--replied", "04_interface=17", "04_interface=99")
        self.assertIn("v99", str(cm.exception))
        self.assertEqual(VERSIONS.read_text(), before)
        with self.assertRaises(SystemExit):
            self.run_main("--replied", "nope=1")
        self.assertEqual(VERSIONS.read_text(), before)

    def test_replied_rejects_bad_pair(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_main("--replied", "04_interface")
        self.assertIn("<鍵>=<版號>", str(cm.exception))

    def test_finalized_records_version_commit_and_removes_review_dir(self):
        self.run_main("--replied", "04_interface=17")
        before = self.table()

        self.run_main("--finalized", "04_interface=17")

        table = self.table()
        self.assertEqual(table["finalized"]["04_interface"],
                         {"v": 17, "commit": self.first})
        self.assertEqual(table["review_zip"], before["review_zip"])
        self.assertEqual(table["pages"], before["pages"])
        self.assertFalse(pathlib.Path("doc/review/04_interface").exists())
        self.assertFalse(self.out.exists())

    def test_finalized_batch_fails_if_any_version_is_not_replied(self):
        self.run_main("--replied", "04_interface=17")
        before = VERSIONS.read_text()

        with self.assertRaises(SystemExit) as cm:
            self.run_main("--finalized", "04_interface=17", "03_messages=12")

        self.assertIn("replied: true", str(cm.exception))
        self.assertEqual(VERSIONS.read_text(), before)
        self.assertTrue(pathlib.Path("doc/review/04_interface").is_dir())
        self.assertTrue(pathlib.Path("doc/review/03_messages").is_dir())

    def test_finalized_rejects_version_that_was_not_sent(self):
        before = VERSIONS.read_text()

        with self.assertRaises(SystemExit) as cm:
            self.run_main("--finalized", "04_interface=99")

        self.assertIn("v99", str(cm.exception))
        self.assertEqual(VERSIONS.read_text(), before)
        self.assertTrue(pathlib.Path("doc/review/04_interface").is_dir())

    def test_pack_changed_finalized_page_as_new_review_round(self):
        self.run_main("--replied", "04_interface=17")
        self.run_main("--finalized", "04_interface=17")
        pathlib.Path("doc/contract/04_interface.md").write_text("# 04\n\n定案後改了\n")
        changed = self.commit()
        mark_changes.build_from_version("04_interface")

        path, arcnames = pack_review.pack(["04_interface"], self.out)

        self.assertEqual(path.name, "review_v2.zip")
        self.assertEqual(arcnames, ["04_interface.v18.marked.md", "04_interface.v18.md"])
        table = self.table()
        self.assertEqual(table["pages"]["04_interface"][-1],
                         {"v": 18, "commit": changed, "replied": False})
        self.assertNotIn("finalized", table)

    def test_main_creates_missing_out_dir(self):
        out = pathlib.Path("ws/reference/review_sent")
        self.assertFalse(out.exists())
        self.run_main("--out", str(out), "04_interface")
        self.assertTrue((out / "review_v2.zip").is_file())
        self.assertEqual(self.table()["review_zip"], 2)


if __name__ == "__main__":
    unittest.main()
