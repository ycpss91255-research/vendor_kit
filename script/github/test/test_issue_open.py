"""issue_open.py 的測試：假 gh（ISSUE_OPEN_GH）記錄 argv；hook 檢查用 repo 真的 settings.json 與 hook。

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
import issue_open as io_  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑
REPO = "ycpss91255-research/vendor_kit"
FAKE_GH = """#!{python}
import json, os, sys
args = sys.argv[1:]
with open({log!r}, "a", encoding="utf-8") as f:
    f.write(json.dumps(args) + "\\n")
fail = os.environ.get("FAKE_GH_FAIL", "")
if args[:2] == ["issue", "create"]:
    if fail == "create":
        sys.stderr.write("create boom\\n"); sys.exit(1)
    print("https://github.com/{repo}/issues/42")
elif args[:1] == ["api"] and "--jq" in args:
    if fail == "id":
        sys.stderr.write("id boom\\n"); sys.exit(1)
    print("9000")
elif args[:3] == ["api", "-X", "POST"]:
    if fail == "attach":
        sys.stderr.write("attach boom\\n"); sys.exit(1)
    print("{{}}")
"""


class IssueOpenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.log = self.dir / "gh.log"
        gh = self.dir / "fake_gh"
        gh.write_text(FAKE_GH.format(python=sys.executable, log=str(self.log), repo=REPO),
                      encoding="utf-8")
        gh.chmod(0o755)
        self.env = {"ISSUE_OPEN_GH": str(gh), "FAKE_GH_FAIL": ""}
        self.body = self.dir / "issue.md"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, args, fail=""):
        out = StringIO()
        env = dict(self.env, FAKE_GH_FAIL=fail)
        with mock.patch.dict(os.environ, env), redirect_stdout(out):
            code = io_.main(args)
        return code, json.loads(out.getvalue())

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines()]

    def create(self, text, *extra, fail=""):
        self.body.write_text(text, encoding="utf-8")
        return self.run_cli(["create", "--title", "標題", "--label", "enhancement",
                             "--body-file", str(self.body), *extra], fail=fail)

    def test_create_and_attach(self):
        code, data = self.create("Part of #139\n\n## 要做的\n", "--parent", "139")
        self.assertEqual(code, 0, data)
        self.assertTrue(data["ok"])
        self.assertEqual(data["step"], "done")
        self.assertEqual(data["issue"], 42)
        self.assertEqual(data["url"], f"https://github.com/{REPO}/issues/42")
        self.assertEqual(data["parent"], 139)
        self.assertTrue(data["attached"])
        self.assertEqual(data["sub_issue_id"], 9000)
        self.assertEqual(self.calls(), [
            ["issue", "create", "-R", REPO, "--title", "標題", "--label", "enhancement",
             "--body-file", str(self.body.resolve())],
            ["api", f"repos/{REPO}/issues/42", "--jq", ".id"],
            ["api", "-X", "POST", f"repos/{REPO}/issues/139/sub_issues", "-F", "sub_issue_id=9000"],
        ])
        self.assertFalse(self.body.exists())

    def test_without_parent(self):
        code, data = self.create("沒有父題的本文\n")
        self.assertEqual(code, 0, data)
        self.assertEqual(data["step"], "done")
        self.assertEqual(data["issue"], 42)
        self.assertIsNone(data["parent"])
        self.assertFalse(data["attached"])
        self.assertEqual(len(self.calls()), 1)
        self.assertFalse(self.body.exists())

    def test_title_file(self):
        title = self.dir / "title.txt"
        title.write_text("檔案裡的標題\n", encoding="utf-8")
        self.body.write_text("本文\n", encoding="utf-8")
        code, data = self.run_cli(["create", "--title-file", str(title), "--label", "bug",
                                   "--body-file", str(self.body)])
        self.assertEqual(code, 0, data)
        self.assertIn("檔案裡的標題", self.calls()[0])

    def test_wrong_first_line_does_not_call_gh(self):
        code, data = self.create("## 要做的\nPart of #139\n", "--parent", "139")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertTrue(data["problems"])
        self.assertEqual(self.calls(), [])
        self.assertTrue(self.body.exists())

    def test_local_path_stopped_at_check(self):
        code, data = self.create(f"Part of #139\n見 {HOME}x.py\n", "--parent", "139")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertTrue(any("本機絕對路徑" in p for p in data["problems"]))
        self.assertEqual(self.calls(), [])
        code, data = self.create(f"見 {HOME}x.py\n")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertEqual(self.calls(), [])

    def test_local_path_denied_by_real_hook(self):
        # 繞過自檢，確認真的 comment_tag_guard 也會擋，而且不呼叫 gh
        with mock.patch.object(io_, "self_check", return_value=[]):
            code, data = self.create(f"Part of #139\n見 {HOME}x.py\n", "--parent", "139")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "create")
        self.assertIn("comment_tag_guard.py", [d.get("hook") for d in data["denied"]])
        self.assertEqual(self.calls(), [])
        self.assertTrue(self.body.exists())

    def test_attribution_denied_by_real_hook(self):
        code, data = self.create("Part of #139\n\nCo-Authored-By: " + "Claude <x>\n", "--parent", "139")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "create")
        self.assertIn("attribution_guard.py", [d.get("hook") for d in data["denied"]])
        self.assertEqual(self.calls(), [])
        self.assertTrue(self.body.exists())

    def test_create_failure_keeps_body(self):
        code, data = self.create("Part of #139\n", "--parent", "139", fail="create")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "create")
        self.assertIn("create boom", data["error"])
        self.assertTrue(self.body.exists())

    def test_attach_failure_returns_3(self):
        code, data = self.create("Part of #139\n", "--parent", "139", fail="attach")
        self.assertEqual(code, 3)
        self.assertFalse(data["ok"])
        self.assertEqual(data["step"], "attach")
        self.assertEqual(data["issue"], 42)
        self.assertFalse(data["attached"])
        self.assertIn("attach boom", data["error"])
        self.assertFalse(self.body.exists())

    def test_id_lookup_failure_returns_3(self):
        code, data = self.create("Part of #139\n", "--parent", "139", fail="id")
        self.assertEqual(code, 3)
        self.assertEqual(data["issue"], 42)
        self.assertIsNone(data["sub_issue_id"])
        self.assertEqual(len(self.calls()), 2)

    def test_attach_subcommand(self):
        code, data = self.run_cli(["attach", "--parent", "139", "--issue", "7"])
        self.assertEqual(code, 0, data)
        self.assertEqual(data["step"], "done")
        self.assertTrue(data["attached"])
        self.assertEqual(self.calls(), [
            ["api", f"repos/{REPO}/issues/7", "--jq", ".id"],
            ["api", "-X", "POST", f"repos/{REPO}/issues/139/sub_issues", "-F", "sub_issue_id=9000"],
        ])

    def test_attach_subcommand_failure(self):
        code, data = self.run_cli(["attach", "--parent", "139", "--issue", "7"], fail="attach")
        self.assertEqual(code, 3)
        self.assertEqual(data["issue"], 7)

    def test_keep_body(self):
        code, data = self.create("Part of #139\n", "--parent", "139", "--keep-body")
        self.assertEqual(code, 0, data)
        self.assertTrue(self.body.exists())

    def test_usage_errors(self):
        self.body.write_text("x\n", encoding="utf-8")
        for args in ([], ["other"], ["create", "--label", "x", "--body-file", str(self.body)],
                     ["create", "--title", "t", "--title-file", "f", "--label", "x",
                      "--body-file", str(self.body)],
                     ["create", "--title", " ", "--label", "x", "--body-file", str(self.body)],
                     ["attach", "--parent", "1"]):
            with self.subTest(args=args):
                code, data = self.run_cli(args)
                self.assertEqual(code, 2)
                self.assertFalse(data["ok"])
                self.assertIn("用法錯", data["error"])
        self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    unittest.main()
