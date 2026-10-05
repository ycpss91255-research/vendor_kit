"""review_paths.py 的送審副本路徑、版號、基準與 zip 清單：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import mark_changes  # noqa: E402
import review_paths  # noqa: E402

SCRIPT = HERE / "review_paths.py"


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


class ReviewPathsTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self._tmp.name).resolve() / "repo"
        self.repo.mkdir()
        r = self.repo
        git("init", "-q", cwd=r)
        git("config", "user.email", "t@example.com", cwd=r)
        git("config", "user.name", "t", cwd=r)
        git("config", "commit.gpgsign", "false", cwd=r)
        (r / "doc/contract").mkdir(parents=True)
        (r / "doc/contract/02_invariants.md").write_text("# 02\n")
        (r / "doc/contract/03_output.md").write_text("# 03\n")
        (r / "doc/contract/reason_codes.csv").write_text("code,status\nVK0001,active\n")
        (r / "doc/contract/04_interface.md").write_text("# 04\n")
        (r / "GLOSSARY.md").write_text("# 名詞\n")
        git("add", "-A", cwd=r)
        git("commit", "-q", "-m", "c", cwd=r)
        head = git("rev-parse", "HEAD", cwd=r)
        (r / "doc/review").mkdir(parents=True)
        (r / "doc/review/versions.json").write_text(json.dumps({
            "review_zip": 11,
            "pages": {
                "02_invariants": [{"v": 22, "commit": head, "replied": True}],
                "03_output": [{"v": 20, "commit": head, "replied": True}],
                "04_interface": [{"v": 25, "commit": head, "replied": True},
                                 {"v": 26, "commit": head, "replied": False}],
            },
            "finalized": {"02_invariants": {"v": 22, "commit": head}},
        }))
        os.chdir(r)
        for name in ("03_output", "04_interface", "GLOSSARY"):
            mark_changes.build_from_version(name)
        os.chdir(self._cwd)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def run_pages(self, *names):
        return review_paths.pages(self.repo, list(names))

    def by_key(self, out):
        return {p["key"]: p for p in out["pages"]}

    def test_zip_next_and_versions(self):
        out = self.run_pages("02_invariants", "03_output", "04_interface", "GLOSSARY.md")
        self.assertTrue(out["ok"])
        self.assertEqual(out["zip_next"], 12)
        rows = self.by_key(out)
        self.assertEqual(rows["02_invariants"]["version"], 23)
        self.assertEqual(rows["03_output"]["version"], 21)
        self.assertEqual(rows["04_interface"]["version"], 27)
        self.assertEqual(rows["GLOSSARY"]["version"], 1)

    def test_base_kinds(self):
        rows = self.by_key(self.run_pages("02_invariants", "03_output", "04_interface", "GLOSSARY"))
        self.assertEqual(rows["02_invariants"]["base"], {"kind": "finalized", "v": 22})
        self.assertEqual(rows["03_output"]["base"], {"kind": "replied", "v": 20})
        # 送出後還沒回覆的 v26 不算基準
        self.assertEqual(rows["04_interface"]["base"], {"kind": "replied", "v": 25})
        self.assertEqual(rows["GLOSSARY"]["base"], {"kind": "none", "v": None})

    def test_files_are_absolute_and_include_csv(self):
        rows = self.by_key(self.run_pages("03_output", "GLOSSARY.md"))
        d = self.repo / "doc/review/03_output"
        self.assertEqual(rows["03_output"]["dir"], str(d))
        self.assertEqual(rows["03_output"]["rel_dir"], "doc/review/03_output")
        self.assertEqual(rows["03_output"]["files"],
                         [str(d / "03_output.marked.md"), str(d / "03_output.md"), str(d / "reason_codes.csv")])
        for f in rows["03_output"]["files"] + rows["GLOSSARY"]["files"]:
            self.assertTrue(pathlib.Path(f).is_absolute())
            self.assertTrue(pathlib.Path(f).exists())

    def test_missing_dir_lists_no_files(self):
        rows = self.by_key(self.run_pages("02_invariants"))
        self.assertEqual(rows["02_invariants"]["files"], [])

    def test_dirty_lists_uncommitted_copies(self):
        out = self.run_pages("03_output", "04_interface")
        self.assertTrue(any("doc/review/03_output/" in line for line in out["dirty"]))
        git("add", "-A", cwd=self.repo)
        git("commit", "-q", "-m", "copies", cwd=self.repo)
        self.assertEqual(self.run_pages("03_output", "04_interface")["dirty"], [])

    def test_cwd_restored(self):
        before = os.getcwd()
        self.run_pages("03_output")
        self.assertEqual(os.getcwd(), before)

    def test_cli_pages_and_zip(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "pages", "--repo", str(self.repo), "04_interface"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["pages"][0]["version"], 27)
        z = self.repo.parent / "review_v12.zip"
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("note.md", "說明")
            zf.writestr("04_interface.v27.md", "# 04\n")
        proc = subprocess.run([sys.executable, str(SCRIPT), "zip", str(z)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["zip"], str(z))
        self.assertEqual(out["files"], ["note.md", "04_interface.v27.md"])

    def test_cli_errors(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "zip", str(self.repo / "nope.zip")],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(json.loads(proc.stdout)["ok"])
        proc = subprocess.run([sys.executable, str(SCRIPT), "pages", "--repo", str(self.repo.parent), "03_output"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("git repo", json.loads(proc.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
