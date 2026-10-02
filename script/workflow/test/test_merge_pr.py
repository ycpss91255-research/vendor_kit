"""merge_pr.py：用暫存的 origin／主 repo／worktree、假的 gh 與假的 wait_ci 測等 CI、merge 與收尾。"""
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import merge_pr as t  # noqa: E402


def sh(cwd, *args):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def cfg(repo):
    for k, v in (("user.name", "t"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
        sh(repo, "git", "config", k, v)


FAKE_GH = """#!{0}
import json, sys
args = sys.argv[1:]
with open({1!r}, "a") as f:
    f.write(" ".join(args) + "\\n")
path = {2!r}
raw = open(path).read()
try:
    d = json.loads(raw)
except ValueError:  # 測試故意放的壞輸出：原樣印出
    print(raw)
    sys.exit(0)
if args[:2] == ["pr", "merge"]:
    if d.get("merge_fails"):
        sys.stderr.write("merge refused\\n")
        sys.exit(1)
    d["state"], d["mergedAt"] = "MERGED", "2026-01-01T00:00:00Z"
    json.dump(d, open(path, "w"))
    sys.exit(0)
view = dict(d)
m = d.get("mergeable")
if isinstance(m, list):
    view["mergeable"] = m[0]
    if len(m) > 1:
        d["mergeable"] = m[1:]
        json.dump(d, open(path, "w"))
print(json.dumps(view))
"""


class MergePr(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ws = pathlib.Path(self.tmp.name)
        origin = ws / "origin.git"
        sh(ws, "git", "init", "-q", "--bare", "-b", "main", str(origin))
        self.repo = ws / "src"
        sh(ws, "git", "clone", "-q", str(origin), str(self.repo))
        cfg(self.repo)
        (self.repo / "a.txt").write_text("a\n")
        sh(self.repo, "git", "add", "a.txt")
        sh(self.repo, "git", "commit", "-q", "-m", "init")
        sh(self.repo, "git", "push", "-q", "-u", "origin", "HEAD:main")
        # PR 分支的 worktree：commit、push，再由另一個 clone merge 進 origin/main
        self.wt = ws / "worktree" / "branch" / "feat" / "x"
        sh(self.repo, "git", "worktree", "add", "-q", "-b", "feat/x", str(self.wt), "origin/main")
        (self.wt / "b.txt").write_text("b\n")
        sh(self.wt, "git", "add", "b.txt")
        sh(self.wt, "git", "commit", "-q", "-m", "b")
        sh(self.wt, "git", "push", "-q", "origin", "feat/x")
        other = ws / "other"
        sh(ws, "git", "clone", "-q", str(origin), str(other))
        cfg(other)
        sh(other, "git", "merge", "-q", "--no-ff", "-m", "merge", "origin/feat/x")
        sh(other, "git", "push", "-q", "origin", "main")
        self.merged_head = sh(other, "git", "rev-parse", "HEAD")
        # scratchpad：慣例目錄與不該動的目錄
        self.scratch = ws / "scratch"
        for d in ("pr-fix/5", "pr-fix/6", "pr/139-x", "pr/139-y", "other"):
            (self.scratch / d).mkdir(parents=True)
            (self.scratch / d / "f.txt").write_text("x\n")
        self.pr_json = ws / "pr.json"
        self.calls = ws / "calls.txt"
        self.set_pr()
        # 假 gh：pr view 印 pr.json（mergeable 是清單時每次取出第一個）；pr merge 把 state 改成 MERGED
        gh = ws / "gh"
        gh.write_text(FAKE_GH.format(sys.executable, str(self.calls), str(self.pr_json)))
        gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
        self.wait_ci = ws / "wait_ci"
        self.set_ci(0)
        self.env = mock.patch.dict(os.environ, {"MERGE_PR_GH": str(gh), "MERGE_PR_WAIT_CI": str(self.wait_ci)})
        self.env.start()
        self.sleeps = []

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def set_pr(self, state="MERGED", merged_at="2026-01-01T00:00:00Z", branch="feat/x", mergeable="MERGEABLE",
               title="feat: x", body="[claude] x\n\nCloses #1\n"):
        self.pr_json.write_text(json.dumps({"state": state, "headRefName": branch, "mergedAt": merged_at,
                                            "mergeable": mergeable, "title": title, "body": body}))

    def set_open(self, **kw):
        self.set_pr(state="OPEN", merged_at=None, **kw)

    def set_ci(self, code):
        res = {"pr": 5, "all_pass": code == 0, "timed_out": code == 2, "checks": [{"name": "docs-lint", "state":
               "SUCCESS" if code == 0 else "FAILURE"}]}
        self.wait_ci.write_text(f"#!/bin/sh\necho 'wait_ci' \"$@\" >> '{self.calls}'\n"
                                f"echo '{json.dumps(res)}'\nexit {code}\n")
        self.wait_ci.chmod(self.wait_ci.stat().st_mode | stat.S_IEXEC)

    def run_main(self, *extra):
        buf = StringIO()
        with redirect_stdout(buf), mock.patch.object(t.time, "sleep", self.sleeps.append):
            code = t.main(["5", "--repo", str(self.repo), *extra])
        return code, json.loads(buf.getvalue())

    def run_no_merge(self, *extra):
        return self.run_main("--no-merge", *extra)

    def call_lines(self):
        return self.calls.read_text().splitlines() if self.calls.exists() else []

    def merge_calls(self):
        return [line for line in self.call_lines() if line.startswith("pr merge")]

    def assert_untouched(self, before):
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())
        self.assertEqual(self.merge_calls(), [])

    def head(self):
        return sh(self.repo, "git", "rev-parse", "HEAD")

    def test_no_merge_full_cleanup(self):
        code, out = self.run_no_merge("--scratch", str(self.scratch), "--item", "139-x")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"] and out["merged"])
        self.assertEqual(out["pulled"], self.merged_head)
        self.assertEqual(self.head(), self.merged_head)
        self.assertTrue(out["worktree_removed"])
        self.assertFalse(self.wt.exists())
        self.assertEqual(sh(self.repo, "git", "branch", "--list", "feat/x"), "")
        self.assertEqual(sorted(pathlib.Path(p).relative_to(self.scratch).as_posix() for p in out["scratch_removed"]),
                         ["pr-fix/5", "pr/139-x"])
        for d in ("pr-fix/6", "pr/139-y", "other"):
            self.assertTrue((self.scratch / d).is_dir(), d)
        self.assertIsNone(out["error"])
        # --no-merge：不等 CI、不 merge，只呼叫唯讀的 gh pr view
        for line in self.call_lines():
            self.assertTrue(line.startswith("pr view 5 "), line)
        self.assertIsNone(out["ci"])
        self.assertFalse(out["merge"])

    def test_not_merged_touches_nothing(self):
        self.set_pr(state="OPEN", merged_at=None)
        before = self.head()
        code, out = self.run_no_merge("--scratch", str(self.scratch), "--item", "139-x")
        self.assertEqual(code, 1)
        self.assertFalse(out["merged"])
        self.assertIsNone(out["pulled"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())
        self.assertIn("還沒 merge", out["error"])

    def test_dirty_repo_stops(self):
        (self.repo / "a.txt").write_text("changed\n")
        before = self.head()
        code, out = self.run_no_merge("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertIn("未提交", out["error"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())
        self.assertEqual((self.repo / "a.txt").read_text(), "changed\n")

    def test_untracked_file_does_not_block(self):
        (self.repo / "local.txt").write_text("x\n")
        code, out = self.run_no_merge()
        self.assertEqual(code, 0, out)
        self.assertTrue((self.repo / "local.txt").exists())

    def test_not_on_main_stops(self):
        sh(self.repo, "git", "switch", "-q", "-c", "topic")
        code, out = self.run_no_merge()
        self.assertEqual(code, 1)
        self.assertIn("不在 main", out["error"])
        self.assertEqual(sh(self.repo, "git", "rev-parse", "--abbrev-ref", "HEAD"), "topic")
        self.assertTrue(self.wt.exists())

    def test_missing_worktree_is_skipped(self):
        sh(self.repo, "git", "worktree", "remove", str(self.wt))
        sh(self.repo, "git", "branch", "-D", "feat/x")
        code, out = self.run_no_merge("--scratch", str(self.scratch))
        self.assertEqual(code, 0, out)
        self.assertTrue(out["worktree_skipped"])
        self.assertFalse(out["worktree_removed"])
        self.assertEqual([pathlib.Path(p).name for p in out["scratch_removed"]], ["5"])

    def test_no_scratch_keeps_dirs(self):
        code, out = self.run_no_merge()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["scratch_removed"], [])
        self.assertTrue((self.scratch / "pr-fix" / "5").is_dir())

    def test_bad_item_touches_nothing(self):
        before = self.head()
        for bad in ("..", "x-1", "139-", "139-../other", "*"):
            code, out = self.run_no_merge("--scratch", str(self.scratch), "--item", bad)
            self.assertEqual(code, 1, bad)
            self.assertIn("--item", out["error"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())
        self.assertTrue((self.scratch / "other").is_dir())

    def test_item_sanitized_like_pr_js(self):
        (self.scratch / "pr" / "139-a_b").mkdir(parents=True)
        code, out = self.run_no_merge("--scratch", str(self.scratch), "--item", "139-a/b")
        self.assertEqual(code, 0, out)
        self.assertFalse((self.scratch / "pr" / "139-a_b").exists())

    def test_gh_failure(self):
        self.pr_json.write_text("not json")
        code, out = self.run_no_merge()
        self.assertEqual(code, 1)
        self.assertIn("不是 JSON", out["error"])
        self.assertTrue(self.wt.exists())


    # ---- 等 CI → merge → 收尾 ----

    def test_merge_all_the_way(self):
        self.set_open()
        code, out = self.run_main("--scratch", str(self.scratch), "--item", "139-x")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"] and out["merge"] and out["merged"])
        self.assertTrue(out["ci"]["all_pass"])
        self.assertEqual(out["mergeable"], "MERGEABLE")
        self.assertEqual(self.merge_calls(), ["pr merge 5 -R ycpss91255-research/vendor_kit --merge"])
        lines = self.call_lines()
        self.assertTrue(lines[0].startswith("wait_ci 5"), lines)
        self.assertLess(lines.index(self.merge_calls()[0]), len(lines) - 1)  # merge 後再查一次 state
        self.assertEqual(self.head(), self.merged_head)
        self.assertFalse(self.wt.exists())
        self.assertEqual(sorted(pathlib.Path(p).relative_to(self.scratch).as_posix() for p in out["scratch_removed"]),
                         ["pr-fix/5", "pr/139-x"])
        self.assertIsNone(out["error"])

    def test_ci_failure_does_not_merge(self):
        self.set_open()
        before = self.head()
        for ci_code in (1, 2):
            with self.subTest(ci_code=ci_code):
                self.set_ci(ci_code)
                code, out = self.run_main("--scratch", str(self.scratch))
                self.assertEqual(code, 1)
                self.assertFalse(out["merge"])
                self.assertFalse(out["ci"]["all_pass"])
                self.assertEqual(out["ci"]["code"], ci_code)
                self.assertIn("CI 沒有全過", out["error"])
                self.assert_untouched(before)

    def test_conflicting_does_not_merge(self):
        self.set_open(mergeable="CONFLICTING")
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertEqual(out["mergeable"], "CONFLICTING")
        self.assertIn("rebase", out["error"])
        self.assertFalse(out["merge"])
        self.assert_untouched(before)

    def test_unknown_is_rechecked(self):
        self.set_open(mergeable=["UNKNOWN", "UNKNOWN", "MERGEABLE"])
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.sleeps, [5, 5])
        self.assertEqual(len(self.merge_calls()), 1)

    def test_unknown_gives_up_after_6(self):
        self.set_open(mergeable=["UNKNOWN"])
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertEqual(self.sleeps, [5] * 6)
        self.assertEqual(out["mergeable"], "UNKNOWN")
        self.assert_untouched(before)

    def test_attribution_in_body_does_not_merge(self):
        before = self.head()
        for kw in ({"body": "[claude] x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"},
                   {"title": "feat: x Generated with Claude Code"}):
            with self.subTest(**kw):
                self.set_open(**kw)
                code, out = self.run_main("--scratch", str(self.scratch))
                self.assertEqual(code, 1)
                self.assertIn("署名", out["error"])
                self.assert_untouched(before)

    def test_already_merged_points_to_no_merge(self):
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertIn("--no-merge", out["error"])
        self.assert_untouched(before)

    def test_dirty_repo_stops_before_merge(self):
        self.set_open()
        (self.repo / "a.txt").write_text("changed\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("未提交", out["error"])
        self.assertEqual(self.call_lines(), [])  # 連 CI 都還沒等

    def test_gh_merge_failure(self):
        self.set_open()
        self.pr_json.write_text(self.pr_json.read_text().replace('"OPEN"', '"OPEN", "merge_fails": true'))
        before = self.head()
        code, out = self.run_main("--scratch", str(self.scratch))
        self.assertEqual(code, 1)
        self.assertIn("gh pr merge 5 失敗", out["error"])
        self.assertFalse(out["merge"])
        self.assertEqual(self.head(), before)
        self.assertTrue(self.wt.exists())


if __name__ == "__main__":
    unittest.main()
