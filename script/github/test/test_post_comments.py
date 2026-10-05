"""post_comments.py 的測試：假 gh（POST_COMMENTS_GH）記錄 argv；hook 檢查用 repo 真的 settings.json 與 hook。

跑法：python3 -m unittest discover -s script/github/test
"""
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import post_comments as pc  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑
REPO = "ycpss91255-research/vendor_kit"
FAKE_GH = """#!{python}
import json, os, sys
args = sys.argv[1:]
with open({log!r}, "a", encoding="utf-8") as f:
    f.write(json.dumps(args) + "\\n")
counter = {counter!r}
if args[1:2] == ["comment"]:
    n = int(open(counter).read()) + 1 if os.path.exists(counter) else 1
    open(counter, "w").write(str(n))
    if os.environ.get("FAKE_GH_FAIL_AT") == str(n):
        sys.stderr.write("comment boom\\n"); sys.exit(1)
    print("https://github.com/{repo}/issues/" + args[2] + "#issuecomment-" + str(100 + n))
elif args[:2] == ["issue", "close"]:
    if os.environ.get("FAKE_GH_FAIL") == "close":
        sys.stderr.write("close boom\\n"); sys.exit(1)
    print("Closed issue #" + args[2])
"""


class PostCommentsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.log = self.dir / "gh.log"
        gh = self.dir / "fake_gh"
        gh.write_text(FAKE_GH.format(python=sys.executable, log=str(self.log),
                                     counter=str(self.dir / "count"), repo=REPO),
                      encoding="utf-8")
        gh.chmod(0o755)
        self.env = {"POST_COMMENTS_GH": str(gh), "FAKE_GH_FAIL_AT": "", "FAKE_GH_FAIL": ""}
        self.posts = self.dir / "posts"
        self.posts.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        p = self.posts / name
        p.write_text(text, encoding="utf-8")
        return p

    def run_cli(self, args, **env):
        out = StringIO()
        with mock.patch.dict(os.environ, dict(self.env, **env)), redirect_stdout(out):
            code = pc.main(args)
        return code, json.loads(out.getvalue())

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines()]

    def comment(self, path, kind="issue", number="7"):
        return [kind, "comment", number, "-R", REPO, "--body-file", str(path.resolve())]

    def test_dir_sorted_by_name(self):
        b = self.write("post_02_codex.md", "[codex] 二\n")
        a = self.write("post_01_agy.md", "[agy] 一\n")
        c = self.write("post_03_claude.md", "[claude] 三\n")
        self.write("note.md", "[claude] 不是 post_ 開頭，不貼\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts)])
        self.assertEqual(code, 0, data)
        self.assertTrue(data["ok"])
        self.assertEqual(data["planned"], [str(p.resolve()) for p in (a, b, c)])
        self.assertEqual(self.calls(), [self.comment(p) for p in (a, b, c)])
        self.assertEqual(data["urls"], [
            f"https://github.com/{REPO}/issues/7#issuecomment-{100 + n}" for n in (1, 2, 3)])
        self.assertIsNone(data["failed_at"])
        self.assertFalse(data["closed"])
        self.assertTrue(a.exists())

    def test_body_file_order_kept(self):
        a = self.write("b.md", "[claude] 先\n")
        b = self.write("a.md", "[claude] 後\n")
        code, data = self.run_cli(["--kind", "pr", "--number", "9", "--body-file", str(a), str(b)])
        self.assertEqual(code, 0, data)
        self.assertEqual(self.calls(), [self.comment(p, "pr", "9") for p in (a, b)])

    def test_untagged_file_blocks_whole_batch(self):
        self.write("post_01_claude.md", "[claude] 有標記\n")
        bad = self.write("post_02_claude.md", "沒有標記\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts)])
        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["failed_at"], str(bad.resolve()))
        self.assertEqual(data["urls"], [])
        self.assertIn("comment_tag_guard.py", [d.get("hook") for d in data["denied"]])
        self.assertEqual({d["path"] for d in data["denied"]}, {str(bad.resolve())})
        self.assertEqual(self.calls(), [])

    def test_local_path_blocks_whole_batch(self):
        self.write("post_01_claude.md", f"[claude] 見 {HOME}x.py\n")
        self.write("post_02_claude.md", "[claude] 沒問題\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts)])
        self.assertEqual(code, 1)
        self.assertEqual(self.calls(), [])

    def test_second_failure_returns_3(self):
        a = self.write("post_01_claude.md", "[claude] 一\n")
        b = self.write("post_02_claude.md", "[claude] 二\n")
        self.write("post_03_claude.md", "[claude] 三\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts),
                                   "--close", "--delete"], FAKE_GH_FAIL_AT="2")
        self.assertEqual(code, 3)
        self.assertFalse(data["ok"])
        self.assertEqual(data["urls"], [f"https://github.com/{REPO}/issues/7#issuecomment-101"])
        self.assertEqual(data["failed_at"], str(b.resolve()))
        self.assertIn("comment boom", data["error"])
        self.assertFalse(data["closed"])
        self.assertEqual(self.calls(), [self.comment(a), self.comment(b)])
        self.assertTrue(a.exists())

    def test_close_after_all_posted(self):
        a = self.write("post_01_claude.md", "[claude] 一\n")
        b = self.write("post_02_claude.md", "[claude] 二\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts),
                                   "--close"])
        self.assertEqual(code, 0, data)
        self.assertTrue(data["closed"])
        self.assertEqual(self.calls(), [self.comment(a), self.comment(b),
                                        ["issue", "close", "7", "-R", REPO]])

    def test_close_failure_returns_3(self):
        self.write("post_01_claude.md", "[claude] 一\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts),
                                   "--close"], FAKE_GH_FAIL="close")
        self.assertEqual(code, 3)
        self.assertEqual(len(data["urls"]), 1)
        self.assertIsNone(data["failed_at"])
        self.assertFalse(data["closed"])
        self.assertIn("close boom", data["error"])

    def test_close_with_pr_is_usage_error(self):
        self.write("post_01_claude.md", "[claude] 一\n")
        code, data = self.run_cli(["--kind", "pr", "--number", "7", "--dir", str(self.posts),
                                   "--close"])
        self.assertEqual(code, 2)
        self.assertIn("用法錯", data["error"])
        self.assertEqual(self.calls(), [])

    def test_delete_after_success(self):
        a = self.write("post_01_claude.md", "[claude] 一\n")
        b = self.write("post_02_claude.md", "[claude] 二\n")
        code, data = self.run_cli(["--kind", "issue", "--number", "7", "--dir", str(self.posts),
                                   "--delete"])
        self.assertEqual(code, 0, data)
        self.assertFalse(a.exists())
        self.assertFalse(b.exists())

    def test_usage_errors(self):
        f = self.write("x.md", "[claude] x\n")
        empty = self.dir / "empty"
        empty.mkdir()
        for args in ([], ["--kind", "issue", "--number", "7"],
                     ["--kind", "other", "--number", "7", "--body-file", str(f)],
                     ["--kind", "issue", "--number", "x", "--body-file", str(f)],
                     ["--kind", "issue", "--number", "0", "--body-file", str(f)],
                     ["--kind", "issue", "--number", "7", "--body-file", str(f), "--dir", str(empty)],
                     ["--kind", "issue", "--number", "7", "--dir", str(empty)],
                     ["--kind", "issue", "--number", "7", "--dir", str(self.dir / "nope")],
                     ["--kind", "issue", "--number", "7", "--body-file", str(self.dir / "nope.md")]):
            with self.subTest(args=args):
                code, data = self.run_cli(args)
                self.assertEqual(code, 2)
                self.assertFalse(data["ok"])
                self.assertIn("用法錯", data["error"])
        self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    unittest.main()
