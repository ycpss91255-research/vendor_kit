"""check_local_paths.py：跑法 `python3 -m unittest discover -s script/repo/test`。

測試資料裡的本機路徑一律拆開拼，避免這個測試檔本身被當成含本機路徑。
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_local_paths as c  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[3]
HOME = "/" + "home/someone/"
MAC = "/" + "Users/someone/"
SCRATCH = "/" + "tmp/claude-1000/"
WIN = "C:" + "\\Users\\"
RULES = c.load_rules(REPO)


class ScanText(unittest.TestCase):
    def test_each_rule_hits(self):
        for path in [HOME + "x", MAC + "x", SCRATCH + "x", WIN + "x"]:
            with self.subTest(path=path):
                hits = c.scan_text(f"ok\n見 {path}\n", RULES)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0][0], 2)

    def test_rule_labels_come_from_hook(self):
        labels = {label for _, label in RULES}
        hits = c.scan_text(HOME + "x\n", RULES)
        self.assertIn(hits[0][1], labels)

    def test_relative_and_home_shorthand_ok(self):
        self.assertEqual(c.scan_text("script/repo/x.py\n~/x\n/home\n/tmp/x\n", RULES), [])


class Check(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, data):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            p.write_bytes(data)
        else:
            p.write_text(data, encoding="utf-8")
        return name

    def test_hit_reported_with_file_line_rule(self):
        f = self.write("a.md", "x\ny\n見 " + HOME + "z\n")
        res = c.check(self.root, RULES, [f], {})
        self.assertFalse(res["ok"])
        self.assertEqual(len(res["hits"]), 1)
        self.assertEqual(res["hits"][0]["file"], "a.md")
        self.assertEqual(res["hits"][0]["line"], 3)
        self.assertIn(res["hits"][0]["rule"], {label for _, label in RULES})

    def test_clean_files_ok(self):
        f = self.write("a.md", "見 script/x.py\n")
        self.assertEqual(c.check(self.root, RULES, [f], {}), {"ok": True, "hits": [], "stale_allow": []})

    def test_binary_skipped(self):
        nul = self.write("a.bin", b"\x00" + HOME.encode())
        latin = self.write("b.dat", b"\xff\xfe" + HOME.encode())
        self.assertTrue(c.check(self.root, RULES, [nul, latin], {})["ok"])

    def test_missing_and_symlink_skipped(self):
        target = self.write("t.md", HOME + "x\n")
        (self.root / "link.md").symlink_to("t.md")
        res = c.check(self.root, RULES, ["gone.md", "link.md", target], {})
        self.assertEqual([h["file"] for h in res["hits"]], ["t.md"])

    def test_allowlisted_file_skipped(self):
        f = self.write("a.md", HOME + "x\n")
        self.assertTrue(c.check(self.root, RULES, [f], {"a.md": "理由"})["ok"])

    def test_stale_allow_fails(self):
        f = self.write("a.md", "乾淨\n")
        res = c.check(self.root, RULES, [f], {"a.md": "理由", "gone.md": "理由"})
        self.assertFalse(res["ok"])
        self.assertEqual(res["stale_allow"], ["a.md", "gone.md"])

    def test_every_allow_entry_has_reason(self):
        for f, why in c.ALLOW.items():
            with self.subTest(file=f):
                self.assertTrue(why.strip())


class EndToEnd(unittest.TestCase):
    """在暫存 git repo 裡跑 main()：只看 git ls-files 追蹤的檔、規則取自 hook。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        hook = self.root / c.HOOK
        hook.parent.mkdir(parents=True)
        shutil.copy(REPO / c.HOOK, hook)
        (self.root / "a.md").write_text("見 " + HOME + "x\n", encoding="utf-8")
        (self.root / "untracked.md").write_text(HOME + "x\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "a.md", str(c.HOOK)], check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def run_main(self):
        buf = StringIO()
        with redirect_stdout(buf):
            code = c.main(["--root", str(self.root)])
        out = buf.getvalue()
        self.assertEqual(len(out.strip().splitlines()), 1)
        return code, json.loads(out)

    def test_reports_tracked_hits_only(self):
        code, out = self.run_main()
        self.assertEqual(code, 1)
        files = {h["file"] for h in out["hits"]}
        self.assertIn("a.md", files)
        self.assertNotIn("untracked.md", files)

    def test_missing_hook_exit_2(self):
        (self.root / c.HOOK).unlink()
        code, out = self.run_main()
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertIn("comment_tag_guard.py", out["error"])


if __name__ == "__main__":
    unittest.main()
