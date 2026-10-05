"""verify.py：用暫存的根目錄與假的 docs.yml 測指令抽取、去重、CI 覆蓋與結束碼。"""
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import verify as v  # noqa: E402

YML = """jobs:
  a:
    steps:
      - uses: actions/checkout@v4
      - name: one
        run: echo one
      - run: "echo quoted"
  b:
    steps:
      - name: block
        run: |
          echo first
          echo second
      - name: tests
        run: python3 -m unittest discover -s script/x/test -v
"""

PASS_TEST = "import unittest\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n"
FAIL_TEST = "import unittest\n\nclass T(unittest.TestCase):\n    def test_bad(self):\n        self.fail('x')\n"


class Extract(unittest.TestCase):
    def test_run_commands(self):
        self.assertEqual(v.run_commands(YML),
                         ["echo one", "echo quoted", "echo first\necho second",
                          "python3 -m unittest discover -s script/x/test -v"])

    def test_covered_is_exact_dir(self):
        cmds = ["python3 -m unittest discover -s script/x/test -v"]
        self.assertTrue(v.covered("script/x/test", cmds))
        self.assertFalse(v.covered("script/x/te", cmds))
        self.assertFalse(v.covered("script/xx/test", ["python3 -m unittest discover -s script/xx/tests"]))


class Verify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.write(".github/workflows/docs.yml", YML)
        self.write("script/x/test/test_a.py", PASS_TEST)
        self.write("script/repo/check_script_layout.py", "print('OK')\n")
        self.write(".claude/hooks/test_guard.py", "print('ok')\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def run_main(self):
        buf = StringIO()
        with redirect_stdout(buf):
            code = v.main(["--root", str(self.root)])
        return code, json.loads(buf.getvalue())

    def test_all_pass(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        cmds = [s["cmd"] for s in out["steps"]]
        self.assertIn("python3 script/repo/check_script_layout.py", cmds)
        self.assertIn("python3 .claude/hooks/test_guard.py", cmds)
        # docs.yml 已跑 script/x/test，不重跑
        self.assertEqual(sum("script/x/test" in c for c in cmds), 1)
        self.assertEqual(out["not_in_ci"], [])

    def test_failure_in_run_step(self):
        self.write(".github/workflows/docs.yml", YML.replace("echo one", "exit 3"))
        code, out = self.run_main()
        self.assertEqual(code, 1)
        bad = [s for s in out["steps"] if not s["ok"]]
        self.assertEqual([(s["cmd"], s["code"]) for s in bad], [("exit 3", 3)])

    def test_failing_unittest(self):
        self.write("script/x/test/test_b.py", FAIL_TEST)
        code, out = self.run_main()
        self.assertEqual(code, 1)

    def test_test_dir_not_in_ci_runs_and_fails(self):
        self.write("script/y/test/test_c.py", PASS_TEST)
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertEqual(out["not_in_ci"], ["script/y/test"])
        step = [s for s in out["steps"] if "script/y/test" in s["cmd"]]
        self.assertEqual(len(step), 1)
        self.assertTrue(step[0]["ok"])

    def test_missing_guard_script_skipped(self):
        (self.root / ".claude/hooks/test_guard.py").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        step = [s for s in out["steps"] if s["source"] == "hooks test_guard"]
        self.assertEqual(len(step), 1)
        self.assertTrue(step[0]["skipped"])
        self.assertTrue(step[0]["ok"])
        self.assertIsNone(step[0]["code"])

    def test_present_guard_script_runs(self):
        code, out = self.run_main()
        step = [s for s in out["steps"] if s["source"] == "hooks test_guard"]
        self.assertEqual(step[0]["code"], 0)
        self.assertNotIn("skipped", step[0])

    def test_failing_guard_script_fails(self):
        self.write(".claude/hooks/test_guard.py", "raise SystemExit(4)\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        step = [s for s in out["steps"] if s["source"] == "hooks test_guard"]
        self.assertEqual(step[0]["code"], 4)

    def test_missing_workflow(self):
        (self.root / ".github/workflows/docs.yml").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])


if __name__ == "__main__":
    unittest.main()
