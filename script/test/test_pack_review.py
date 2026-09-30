"""pack_review.py 的版號、內容與缺檔行為：跑法 `python3 -m unittest discover -s script/test`。"""
import json
import os
import pathlib
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pack_review  # noqa: E402

VERSIONS = pathlib.Path("doc/decisions/review_log/versions.json")
MARKED = pathlib.Path("doc/decisions/_marked")


class PackReviewTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        VERSIONS.parent.mkdir(parents=True)
        MARKED.mkdir(parents=True)
        VERSIONS.write_text(json.dumps({"03_messages": 12, "04_interface": 17, "GLOSSARY": 5, "review_zip": 1}))
        for name in ["03_messages.v12.marked.md", "03_messages.v12.md", "03_messages.v12.csv",
                     "03_messages.v11.md",
                     "04_interface.v17.marked.md", "04_interface.v17.md",
                     "GLOSSARY.v5.marked.md", "GLOSSARY.v5.md"]:
            (MARKED / name).write_text(name)
        pathlib.Path("note.md").write_text("說明")
        self.out = pathlib.Path("out")

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def zip_version(self):
        return json.loads(VERSIONS.read_text())["review_zip"]

    def test_version_increments(self):
        path, _ = pack_review.pack(["04_interface"], self.out)
        self.assertEqual(path.name, "review_v2.zip")
        path, _ = pack_review.pack(["04_interface"], self.out)
        self.assertEqual(path.name, "review_v3.zip")
        self.assertEqual(self.zip_version(), 3)

    def test_contents_complete_and_flat(self):
        path, arcnames = pack_review.pack(["03_messages", "04_interface", "GLOSSARY.md"], self.out,
                                          pathlib.Path("note.md"))
        expected = ["note.md",
                    "03_messages.v12.marked.md", "03_messages.v12.md", "03_messages.v12.csv",
                    "04_interface.v17.marked.md", "04_interface.v17.md",
                    "GLOSSARY.v5.marked.md", "GLOSSARY.v5.md"]
        self.assertEqual(arcnames, expected)
        with zipfile.ZipFile(path) as zf:
            self.assertEqual(zf.namelist(), expected)
            self.assertEqual(zf.read("GLOSSARY.v5.md").decode(), "GLOSSARY.v5.md")

    def test_missing_file_stops_without_bumping(self):
        (MARKED / "04_interface.v17.md").unlink()
        with self.assertRaises(SystemExit) as cm:
            pack_review.pack(["04_interface"], self.out)
        self.assertIn("04_interface.v17.md", str(cm.exception))
        self.assertEqual(self.zip_version(), 1)
        self.assertFalse(self.out.exists())

    def test_unknown_key_stops(self):
        with self.assertRaises(SystemExit):
            pack_review.pack(["05_nothing"], self.out)
        self.assertEqual(self.zip_version(), 1)

    def test_missing_note_stops(self):
        with self.assertRaises(SystemExit):
            pack_review.pack(["04_interface"], self.out, pathlib.Path("nope.md"))
        self.assertEqual(self.zip_version(), 1)


if __name__ == "__main__":
    unittest.main()
