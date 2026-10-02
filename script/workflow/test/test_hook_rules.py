"""hook_rules.py：直接取用 .claude/hooks/comment_tag_guard.py 與 attribution_guard.py 的規則。"""
import json
import os
import pathlib
import shlex
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import body  # noqa: E402
import hook_rules as hr  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑


class SameObject(unittest.TestCase):
    def test_body_uses_hook_local_paths(self):
        self.assertIs(body.LOCAL_PATHS, hr.hook.LOCAL_PATHS)
        self.assertIs(hr.LOCAL_PATHS, hr.hook.LOCAL_PATHS)

    def test_exports_come_from_hook(self):
        for name in hr.NAMES:
            with self.subTest(name=name):
                self.assertIs(getattr(hr, name), getattr(hr.hook, name))

    def test_banned_comes_from_attribution_guard(self):
        self.assertIs(hr.BANNED, hr.attribution.BANNED)
        self.assertEqual(hr.ATTRIBUTION_HOOK.parts[-3:], (".claude", "hooks", "attribution_guard.py"))
        self.assertTrue(hr.BANNED.search("Co-Authored-By: Claude <x>"))
        self.assertIsNone(hr.BANNED.search("一般的 PR 本文"))

    def test_default_path_is_the_hook(self):
        self.assertEqual(hr.HOOK.parts[-3:], (".claude", "hooks", "comment_tag_guard.py"))
        self.assertTrue(hr.HOOK.is_file())


class LoadErrors(unittest.TestCase):
    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path)
            self.assertIn(str(path), str(cm.exception))

    def test_missing_names_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            path.write_text("TAGS = ()\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path)
            self.assertIn("LOCAL_PATHS", str(cm.exception))

    def test_missing_attribution_names_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "attribution_guard.py"
            path.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path, hr.ATTRIBUTION_NAMES)
            self.assertIn("BANNED", str(cm.exception))

    def test_broken_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            path.write_text("raise RuntimeError('x')\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError):
                hr.load(path)


class Rules(unittest.TestCase):
    def test_tagged(self):
        self.assertTrue(hr.tagged("[agy] 原文"))
        self.assertTrue(hr.tagged("  \n[claude] x"))
        self.assertFalse(hr.tagged("沒有標記"))

    def test_raw_with_note_passes(self):
        text = f"[agy] 原文提到 {HOME}x.py\n（註：對應 repo 的 script/x.py）\n"
        self.assertIsNone(hr.local_path_problem(text, "留言", raw_ok=True))

    def test_claude_with_local_path_blocked(self):
        text = f"[claude] 見 {HOME}x.py\n（註：對應 repo 的 script/x.py）\n"
        problem = hr.local_path_problem(text, "留言", raw_ok=True)
        self.assertIsNotNone(problem)
        self.assertIn("本機絕對路徑", problem)

    def test_relative_path_ok(self):
        self.assertIsNone(hr.local_path_problem("[claude] 見 script/x.py", "留言", raw_ok=False))


PY = shlex.quote(sys.executable)
FAKE_HOOKS = {
    # 名稱: 內容；每支都把收到的 stdin 記到 <名稱>.stdin
    "allow_empty.py": "sys.exit(0)",
    "allow_json.py": "print(json.dumps({'hookSpecificOutput': {'permissionDecision': 'allow'}}))",
    "deny.py": "print(json.dumps({'hookSpecificOutput': {'permissionDecision': 'deny', "
               "'permissionDecisionReason': '不准'}}))",
    "ask.py": "print(json.dumps({'hookSpecificOutput': {'permissionDecision': 'ask', "
              "'permissionDecisionReason': '要問'}}))",
    "exit2.py": "sys.stderr.write('結束碼二'); sys.exit(2)",
    "exit1.py": "sys.stderr.write('壞了'); sys.exit(1)",
    "not_json.py": "print('hello')",
    "no_decision.py": "print(json.dumps({'systemMessage': 'x'}))",
    "slow.py": "import time; time.sleep(5)",
    "record_env.py": "open(os.path.join(os.environ['CLAUDE_PROJECT_DIR'], 'env.txt'), 'w')"
                     ".write(os.environ['CLAUDE_PROJECT_DIR'])",
}


class FakeHooks(unittest.TestCase):
    """暫存目錄裡的假 settings.json 與假 hook。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        for name, body in FAKE_HOOKS.items():
            (self.dir / name).write_text(
                "import json, os, sys\n"
                f"open(os.path.join(os.path.dirname(__file__), {name!r} + '.stdin'), 'w').write(sys.stdin.read())\n"
                + body + "\n", encoding="utf-8")
        self.cwd = self.dir / "work"
        self.cwd.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def settings(self, *names, matcher="Bash", extra=()):
        groups = [{"matcher": matcher, "hooks": [
            {"type": "command", "command": f'{PY} "${{CLAUDE_PROJECT_DIR}}/{n}"'} for n in names]}]
        groups.extend(extra)
        path = self.dir / "settings.json"
        path.write_text(json.dumps({"hooks": {"PreToolUse": groups}}), encoding="utf-8")
        return path

    def check(self, *names, argv=("gh", "issue", "comment", "1"), **kw):
        kw.setdefault("timeout", 3)
        return hr.precheck(list(argv), self.cwd, settings=self.settings(*names),
                           project_dir=self.dir, **kw)


class BashHooks(FakeHooks):
    def test_matchers(self):
        extra = [
            {"matcher": "Workflow|Bash", "hooks": [{"type": "command", "command": "both"}]},
            {"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "edit"}]},
            {"matcher": "Bashful", "hooks": [{"type": "command", "command": "partial"}]},
            {"hooks": [{"type": "command", "command": "any"}]},
        ]
        path = self.settings("allow_empty.py", extra=extra)
        cmds = hr.bash_hooks(path)
        self.assertEqual(len(cmds), 3)
        self.assertIn("allow_empty.py", cmds[0])
        self.assertEqual(cmds[1:], ["both", "any"])

    def test_dict_settings(self):
        data = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "x"}]}]}}
        self.assertEqual(hr.bash_hooks(data), ["x"])

    def test_missing_settings_raises(self):
        with self.assertRaises(hr.HookRulesError):
            hr.bash_hooks(self.dir / "nope.json")

    def test_real_settings_has_all_bash_hooks_in_order(self):
        names = [hr.hook_name(c) for c in hr.bash_hooks()]
        self.assertEqual(names[:7], ["guard.py", "worktree_guard.py", "attribution_guard.py",
                                     "issue_body_guard.py", "comment_tag_guard.py",
                                     "pr_rules_guard.py", "src_main_guard.py"])
        self.assertNotIn("decision_guard.py", names)


class Precheck(FakeHooks):
    def test_allow_empty_and_json(self):
        r = self.check("allow_empty.py", "allow_json.py")
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["command"], "gh issue comment 1")
        self.assertEqual(r["denied"], [])
        self.assertEqual(r["errors"], [])

    def test_stdin_and_cwd(self):
        self.check("allow_empty.py", argv=("gh", "pr", "comment", "2", "--body", "a b"))
        data = json.loads((self.dir / "allow_empty.py.stdin").read_text(encoding="utf-8"))
        self.assertEqual(data["hook_event_name"], "PreToolUse")
        self.assertEqual(data["tool_name"], "Bash")
        self.assertEqual(data["tool_input"], {"command": "gh pr comment 2 --body 'a b'"})
        self.assertEqual(data["cwd"], str(self.cwd.resolve()))

    def test_argv0_is_literal_name(self):
        r = self.check("allow_empty.py", argv=(str(self.dir / "bin" / "gh"), "pr", "view"))
        self.assertEqual(r["command"], "gh pr view")

    def test_project_dir_env(self):
        self.check("record_env.py")
        self.assertEqual((self.dir / "env.txt").read_text(encoding="utf-8"), str(self.dir))

    def test_deny(self):
        r = self.check("allow_empty.py", "deny.py")
        self.assertFalse(r["ok"])
        self.assertEqual(r["denied"], [{"hook": "deny.py", "decision": "deny", "reason": "不准"}])

    def test_ask_blocks(self):
        r = self.check("ask.py")
        self.assertFalse(r["ok"])
        self.assertEqual(r["denied"][0]["decision"], "ask")

    def test_exit2_blocks_with_stderr(self):
        r = self.check("exit2.py")
        self.assertFalse(r["ok"])
        self.assertEqual(r["denied"], [{"hook": "exit2.py", "decision": "deny", "reason": "結束碼二"}])

    def test_fail_closed(self):
        for name in ("exit1.py", "not_json.py", "no_decision.py", "slow.py"):
            with self.subTest(hook=name):
                r = self.check("allow_empty.py", name, timeout=1)
                self.assertFalse(r["ok"])
                self.assertEqual(r["denied"], [])
                self.assertEqual([e["hook"] for e in r["errors"]], [name])

    def test_no_hooks_fails_closed(self):
        r = self.check()
        self.assertFalse(r["ok"])
        self.assertTrue(r["errors"])

    def test_bad_settings_fails_closed(self):
        r = hr.precheck(["gh", "pr", "view"], self.cwd, settings=self.dir / "nope.json")
        self.assertFalse(r["ok"])
        self.assertIn("nope.json", r["errors"][0]["error"])


class GuardedRun(FakeHooks):
    def setUp(self):
        super().setUp()
        self.log = self.dir / "gh.log"
        self.gh = self.dir / "fake_gh"
        self.gh.write_text(
            f"#!{sys.executable}\nimport json, sys\n"
            f"open({str(self.log)!r}, 'w').write(json.dumps(sys.argv[1:]))\n"
            "print('done')\n", encoding="utf-8")
        self.gh.chmod(0o755)
        patcher = mock.patch.dict(os.environ, {"HOOK_RULES_TEST_GH": str(self.gh)})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_gh(self, *names):
        return hr.guarded_run(["gh", "issue", "comment", "1", "--body-file", "x.md"], self.cwd,
                              bin_env="HOOK_RULES_TEST_GH", settings=self.settings(*names),
                              project_dir=self.dir)

    def test_denied_does_not_run(self):
        r = self.run_gh("deny.py")
        self.assertFalse(r["ok"])
        self.assertFalse(r["ran"])
        self.assertFalse(r["precheck"]["ok"])
        self.assertFalse(self.log.exists())

    def test_error_does_not_run(self):
        r = self.run_gh("not_json.py")
        self.assertFalse(r["ran"])
        self.assertFalse(self.log.exists())

    def test_allowed_runs_same_argv(self):
        r = self.run_gh("allow_empty.py")
        self.assertTrue(r["ok"], r)
        self.assertTrue(r["ran"])
        self.assertEqual(r["returncode"], 0)
        self.assertEqual(r["stdout"].strip(), "done")
        self.assertEqual(json.loads(self.log.read_text(encoding="utf-8")),
                         ["issue", "comment", "1", "--body-file", "x.md"])
        stdin = json.loads((self.dir / "allow_empty.py.stdin").read_text(encoding="utf-8"))
        self.assertEqual(stdin["tool_input"]["command"], "gh issue comment 1 --body-file x.md")


class RealHooks(unittest.TestCase):
    """用 repo 真的 settings.json 與 hook。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def comment(self, text):
        body = self.dir / "body.md"
        body.write_text(text, encoding="utf-8")
        return hr.precheck(["gh", "issue", "comment", "1", "-R", "ycpss91255-research/vendor_kit",
                            "--body-file", str(body)], hr.ROOT, project_dir=hr.ROOT)

    def test_untagged_comment_denied(self):
        r = self.comment("沒有標記的留言\n")
        self.assertFalse(r["ok"])
        self.assertIn("comment_tag_guard.py", [d["hook"] for d in r["denied"]])

    def test_tagged_comment_allowed(self):
        r = self.comment("[claude] 見 script/workflow/hook_rules.py\n")
        self.assertTrue(r["ok"], r)

    def test_push_main_denied(self):
        r = hr.precheck(["git", "push", "origin", "main"], hr.ROOT, project_dir=hr.ROOT)
        self.assertFalse(r["ok"])
        self.assertIn("guard.py", [d["hook"] for d in r["denied"]])


class Cli(FakeHooks):
    def cli(self, args):
        out = StringIO()
        with redirect_stdout(out):
            code = hr.main(args)
        return code, json.loads(out.getvalue())

    def test_usage_errors(self):
        for args in ([], ["other"], ["precheck", "gh"], ["precheck", "--"], ["precheck", "--x", "--", "gh"]):
            with self.subTest(args=args):
                code, data = self.cli(args)
                self.assertEqual(code, 2)
                self.assertFalse(data["ok"])

    def test_precheck_exit_codes(self):
        with mock.patch.object(hr, "SETTINGS", self.settings("allow_empty.py")), \
                mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(self.dir)}):
            code, data = self.cli(["precheck", "--cwd", str(self.cwd), "--", "gh", "pr", "view"])
            self.assertEqual(code, 0)
            self.assertTrue(data["ok"])
        with mock.patch.object(hr, "SETTINGS", self.settings("deny.py")), \
                mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(self.dir)}):
            code, data = self.cli(["precheck", "--", "gh", "pr", "view"])
            self.assertEqual(code, 1)
            self.assertFalse(data["ok"])


if __name__ == "__main__":
    unittest.main()
