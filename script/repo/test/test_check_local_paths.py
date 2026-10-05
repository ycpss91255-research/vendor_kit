"""check_local_paths.py：跑法 `python3 -m unittest discover -s script/repo/test`。

測試資料裡的本機路徑一律拆開拼，避免這個測試檔本身被當成含本機路徑。
"""
import importlib.util
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



class LoadAllow(unittest.TestCase):
    """白名單資料檔：repo 裡那份讀得到，格式錯就 RuntimeError。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write_allow(self, text):
        p = self.root / c.ALLOW_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_repo_allow_file_loads_with_reasons(self):
        allow = c.load_allow(REPO)
        self.assertTrue(allow)
        for f, why in allow.items():
            with self.subTest(file=f):
                self.assertTrue(why.strip())

    def test_reads_path_and_reason(self):
        self.write_allow(json.dumps({"allow": [{"path": "a.md", "reason": "理由"}]}))
        self.assertEqual(c.load_allow(self.root), {"a.md": "理由"})

    def test_missing_file_raises(self):
        with self.assertRaisesRegex(RuntimeError, "找不到白名單檔"):
            c.load_allow(self.root)

    def test_bad_entries_raise(self):
        for text in ["{", "[]", "{}", '{"allow": {}}',
                     '{"allow": [{"path": "a.md"}]}',
                     '{"allow": [{"path": "a.md", "reason": " "}]}',
                     '{"allow": [{"path": "", "reason": "理由"}]}',
                     '{"allow": ["a.md"]}',
                     '{"allow": [{"path": "a.md", "reason": "x"}, {"path": "a.md", "reason": "y"}]}']:
            with self.subTest(text=text):
                self.write_allow(text)
                with self.assertRaises(RuntimeError):
                    c.load_allow(self.root)


def load_pr_rules():
    """用路徑載入 script/github/check_pr_rules.py（不加進 sys.path，比照腳本載入 hook 的做法）。"""
    spec = importlib.util.spec_from_file_location("check_pr_rules", REPO / "script/github/check_pr_rules.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class AllowFileScope(unittest.TestCase):
    """白名單資料檔在範圍表是附屬檔：跟被放行的檔一起改算一個範圍（#264）。"""

    @classmethod
    def setUpClass(cls):
        cls.pr = load_pr_rules()
        cls.table = cls.pr.load_table()

    def test_attaches_to_fixed_hook_test(self):
        s, p = self.pr.scopes_of([".claude/hooks/test/test_comment_tag_guard.py", str(c.ALLOW_FILE)], self.table)
        self.assertEqual((s, p), (["hook:comment_tag_guard"], []))

    def test_alone_is_script_repo(self):
        s, p = self.pr.scopes_of([str(c.ALLOW_FILE)], self.table)
        self.assertEqual((s, p), (["script:repo"], []))


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
        self.write_allow([])
        subprocess.run(["git", "-C", str(self.root), "add", "a.md", str(c.HOOK)], check=True)

    def write_allow(self, entries):
        p = self.root / c.ALLOW_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"allow": entries}, ensure_ascii=False), encoding="utf-8")

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

    def test_allow_file_skips_and_stale_fails(self):
        allow = [{"path": "a.md", "reason": "理由"}, {"path": str(c.HOOK), "reason": "規則定義"}]
        self.write_allow(allow)
        code, out = self.run_main()
        self.assertEqual((code, out), (0, {"ok": True, "hits": [], "stale_allow": []}))
        self.write_allow(allow + [{"path": "gone.md", "reason": "理由"}])
        code, out = self.run_main()
        self.assertEqual((code, out["stale_allow"]), (1, ["gone.md"]))

    def test_missing_allow_file_exit_2(self):
        (self.root / c.ALLOW_FILE).unlink()
        code, out = self.run_main()
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertIn("local_paths_allow.json", out["error"])

    def test_missing_hook_exit_2(self):
        (self.root / c.HOOK).unlink()
        code, out = self.run_main()
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertIn("comment_tag_guard.py", out["error"])


if __name__ == "__main__":
    unittest.main()
