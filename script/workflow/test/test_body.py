"""body.py：issue／PR 本文檔的自檢。"""
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import body as b  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑


class Problems(unittest.TestCase):
    def test_issue_ok(self):
        self.assertEqual(b.problems("Part of #148\n\n## 要做的\n", "issue", parent=148), [])

    def test_issue_wrong_first_line(self):
        p = b.problems("## 要做的\nPart of #148\n", "issue", parent=148)
        self.assertEqual(len(p), 1)
        self.assertIn("Part of #148", p[0])

    def test_issue_wrong_parent(self):
        self.assertTrue(b.problems("Part of #14\n", "issue", parent=148))

    def test_pr_ok(self):
        self.assertEqual(b.problems("[claude] 做了 x\n\nCloses #150\n", "pr", issue=150), [])

    def test_pr_missing_tag(self):
        p = b.problems("做了 x\n\nCloses #150\n", "pr", issue=150)
        self.assertEqual(len(p), 1)
        self.assertIn("[claude] ", p[0])

    def test_pr_missing_closes(self):
        p = b.problems("[claude] 做了 x\n\nRefs #150\n", "pr", issue=150)
        self.assertEqual(len(p), 1)
        self.assertIn("Closes #150", p[0])

    def test_pr_closes_other_issue(self):
        self.assertTrue(b.problems("[claude] x\nCloses #15\n", "pr", issue=150))

    def test_local_paths(self):
        for path in [HOME + "x", "/Users/someone/x", "/tmp/claude-1000/x", "C:\\Users\\x"]:
            with self.subTest(path=path):
                p = b.problems(f"[claude] x\n見 {path}\nCloses #1\n", "pr", issue=1)
                self.assertEqual(len(p), 1)
                self.assertIn("第 2 行", p[0])

    def test_relative_path_ok(self):
        self.assertEqual(b.problems("[claude] 見 script/workflow/body.py\nCloses #1\n", "pr", issue=1), [])

    def test_empty(self):
        self.assertEqual(b.problems("  \n", "pr", issue=1), ["本文是空的"])


class Main(unittest.TestCase):
    def run_main(self, *argv):
        buf = StringIO()
        with redirect_stdout(buf):
            code = b.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_file_ok_and_bad(self):
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "pr.md"
            f.write_text("[claude] x\n\nCloses #3\n", encoding="utf-8")
            code, out = self.run_main("check", str(f), "--kind", "pr", "--issue", "3")
            self.assertEqual((code, out["ok"]), (0, True))
            f.write_text("x\n", encoding="utf-8")
            code, out = self.run_main("check", str(f), "--kind", "pr", "--issue", "3")
            self.assertEqual((code, out["ok"]), (1, False))
            self.assertEqual(len(out["problems"]), 2)

    def test_missing_file(self):
        code, out = self.run_main("check", "/nonexistent/x.md", "--kind", "issue", "--parent", "1")
        self.assertEqual(code, 1)
        self.assertIn("讀不到檔", out["problems"][0])


if __name__ == "__main__":
    unittest.main()
