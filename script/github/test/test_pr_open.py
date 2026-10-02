"""pr_open.py 的測試：暫存 bare remote 加 clone；假 gh（PR_OPEN_GH）處理 pr list 與 pr create 並記錄 argv。
hook 檢查用 repo 真的 settings.json 與 hook（pr_rules_guard.py 用 --head 的遠端分支取改動檔）。

跑法：python3 -m unittest discover -s script/github/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import pr_open  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑
REPO = "ycpss91255-research/vendor_kit"
BRANCH = "feat/x"
TITLE = "feat(github): 新增 x 工具"
BODY = "[claude] 新增 x 工具\n\n## 做了什麼\n\n新增 x。\n\nCloses #7\n"
FAKE_GH = """#!{python}
import json, os, sys
args = sys.argv[1:]
with open({log!r}, "a", encoding="utf-8") as f:
    f.write(json.dumps(args) + "\\n")
fail = os.environ.get("FAKE_GH_FAIL", "")
if args[:2] == ["pr", "list"]:
    if os.environ.get("FAKE_GH_EXISTING"):
        print(json.dumps([{{"number": 5, "url": "https://github.com/{repo}/pull/5"}}]))
    else:
        print("[]")
elif args[:2] == ["pr", "create"]:
    if fail == "create":
        sys.stderr.write("create boom\\n"); sys.exit(1)
    print("https://github.com/{repo}/pull/42")
"""
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


class PrOpenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.log = self.dir / "gh.log"
        gh = self.dir / "fake_gh"
        gh.write_text(FAKE_GH.format(python=sys.executable, log=str(self.log), repo=REPO),
                      encoding="utf-8")
        gh.chmod(0o755)
        self.env = {"PR_OPEN_GH": str(gh), "FAKE_GH_FAIL": "", "FAKE_GH_EXISTING": ""}
        self.body = self.dir / "pr.md"
        self.remote = self.dir / "remote.git"
        self.wt = self.dir / "wt"
        self.git(self.dir, "init", "-q", "--bare", "-b", "main", str(self.remote))
        self.git(self.dir, "clone", "-q", str(self.remote), str(self.wt))
        self.commit("README.md", "init\n", "chore: init")
        self.git(self.wt, "push", "-q", "origin", "HEAD:main")
        self.git(self.wt, "checkout", "-q", "-b", BRANCH)

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, cwd, *args):
        subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                       env=dict(os.environ, **GIT_ENV))

    def commit(self, rel, text, msg):
        f = self.wt / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
        self.git(self.wt, "add", rel)
        self.git(self.wt, "commit", "-q", "-m", msg)

    def push(self):
        self.git(self.wt, "push", "-q", "-u", "origin", BRANCH)

    def run_cli(self, *extra, body=BODY, title=("--title", TITLE), **env):
        self.body.write_text(body, encoding="utf-8")
        out = StringIO()
        with mock.patch.dict(os.environ, dict(self.env, **env)), redirect_stdout(out):
            code = pr_open.main(["--repo", str(self.wt), "--branch", BRANCH, "--issue", "7",
                                 "--body-file", str(self.body), *title, *extra])
        return code, json.loads(out.getvalue())

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines()]

    def creates(self):
        return [c for c in self.calls() if c[:2] == ["pr", "create"]]

    def test_open(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli()
        self.assertEqual(code, 0, data)
        self.assertTrue(data["ok"])
        self.assertEqual(data["step"], "done")
        self.assertEqual(data["pr"], 42)
        self.assertEqual(data["url"], f"https://github.com/{REPO}/pull/42")
        self.assertIsNone(data["existing"])
        self.assertEqual(self.calls(), [
            ["pr", "list", "-R", REPO, "--head", BRANCH, "--state", "open", "--json", "number,url"],
            ["pr", "create", "-R", REPO, "--base", "main", "--head", BRANCH, "--title", TITLE,
             "--body-file", str(self.body.resolve())],
        ])
        self.assertFalse(self.body.exists())

    def test_title_from_commit_and_keep_body(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli("--keep-body", title=("--title-from-commit",))
        self.assertEqual(code, 0, data)
        create = self.creates()[0]
        self.assertEqual(create[create.index("--title") + 1], TITLE)
        self.assertTrue(self.body.exists())

    def test_not_pushed(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        code, data = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "push")
        self.assertIn("push", data["error"])
        self.assertEqual(self.calls(), [])
        self.assertTrue(self.body.exists())

    def test_not_pushed_up_to_date(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        self.commit("script/doc/y.py", "y\n", "feat(github): 再改一個")
        code, data = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "push")
        self.assertEqual(self.calls(), [])

    def test_existing_pr(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli(FAKE_GH_EXISTING="1")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "existing")
        self.assertEqual(data["existing"], {"number": 5, "url": f"https://github.com/{REPO}/pull/5"})
        self.assertEqual(data["pr"], 5)
        self.assertEqual(self.creates(), [])
        self.assertTrue(self.body.exists())

    def test_body_missing_closes(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli(body="[claude] 新增 x 工具\n\nRefs #7\n")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertTrue(any("Closes #7" in p for p in data["problems"]), data["problems"])
        self.assertEqual(self.creates(), [])
        self.assertTrue(self.body.exists())

    def test_body_local_path(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli(body=f"[claude] x\n見 {HOME}x.py\nCloses #7\n")
        self.assertEqual(code, 1)
        self.assertTrue(any("本機絕對路徑" in p for p in data["problems"]))
        self.assertEqual(self.creates(), [])

    def test_bad_title(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli(title=("--title", "新增 x 工具"))
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertTrue(any(p.startswith("標題：") for p in data["problems"]), data["problems"])
        self.assertEqual(self.creates(), [])

    def test_two_scopes_stopped(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.commit("script/git/y.py", "y\n", "feat(git): 新增 y")
        self.push()
        code, data = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "check")
        self.assertTrue(any("2 個範圍" in p for p in data["problems"]), data["problems"])
        self.assertEqual(self.creates(), [])
        self.assertTrue(self.body.exists())

    def test_two_scopes_denied_by_real_hook(self):
        # 繞過自檢，確認真的 pr_rules_guard 用 --head 的遠端分支也會擋，而且不呼叫 create
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.commit("script/git/y.py", "y\n", "feat(git): 新增 y")
        self.push()
        with mock.patch.object(pr_open.check_pr_rules, "check",
                               return_value={"ok": True, "problems": []}):
            code, data = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "create")
        self.assertIn("pr_rules_guard.py", [d.get("hook") for d in data["denied"]])
        self.assertEqual(self.creates(), [])
        self.assertTrue(self.body.exists())

    def test_create_failure_keeps_body(self):
        self.commit("script/doc/x.py", "x\n", TITLE)
        self.push()
        code, data = self.run_cli(FAKE_GH_FAIL="create")
        self.assertEqual(code, 1)
        self.assertEqual(data["step"], "create")
        self.assertIn("create boom", data["error"])
        self.assertTrue(self.body.exists())

    def test_usage_errors(self):
        self.body.write_text(BODY, encoding="utf-8")
        base = ["--repo", str(self.wt), "--branch", BRANCH, "--issue", "7",
                "--body-file", str(self.body)]
        for args in ([], base, [*base, "--title", "t", "--title-from-commit"],
                     ["--repo", str(self.dir / "nope"), "--branch", BRANCH, "--issue", "7",
                      "--body-file", str(self.body), "--title", TITLE],
                     [*base[:-1], str(self.dir / "missing.md"), "--title", TITLE]):
            with self.subTest(args=args):
                out = StringIO()
                with mock.patch.dict(os.environ, self.env), redirect_stdout(out):
                    code = pr_open.main(args)
                data = json.loads(out.getvalue())
                self.assertEqual(code, 2)
                self.assertFalse(data["ok"])
                self.assertIn("用法錯", data["error"])
        self.assertEqual(self.calls(), [])


if __name__ == "__main__":
    unittest.main()
