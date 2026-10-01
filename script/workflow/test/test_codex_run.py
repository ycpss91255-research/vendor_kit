"""codex_run.py：用測試產生的假 codex（Python 腳本，經 CODEX_BIN 換上）測參數形狀與結束碼，不呼叫真的 codex。"""
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "codex_run.py"

# 假 codex：把 argv 與讀到的 stdin 記進 FAKE_LOG，依 FAKE_MODE 決定行為。
FAKE = r'''#!{python}
import json, os, sys, time
argv = sys.argv[1:]
data = sys.stdin.read()
with open(os.environ["FAKE_LOG"], "w", encoding="utf-8") as f:
    json.dump({{"argv": argv, "stdin": data}}, f, ensure_ascii=False)
mode = os.environ.get("FAKE_MODE", "ok")
out = argv[argv.index("-o") + 1]
if mode == "ok":
    with open(out, "w", encoding="utf-8") as f:
        f.write("結果\n")
elif mode == "empty":
    open(out, "w").close()
elif mode == "sleep":
    time.sleep(30)
print("codex 的 stdout", flush=True)
sys.stderr.write("E" * 2500 + "尾巴")
sys.exit(int(os.environ.get("FAKE_EXIT", "0")))
'''


class CodexRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.fake = self.dir / "codex"
        self.fake.write_text(FAKE.format(python=sys.executable), encoding="utf-8")
        self.fake.chmod(self.fake.stat().st_mode | stat.S_IEXEC)
        self.log = self.dir / "log.json"
        self.brief = self.dir / "brief.md"
        self.brief.write_text("只讀。\n回答 \"問題\" 與 $HOME。", encoding="utf-8")
        self.out = self.dir / "nested" / "deeper" / "out.md"

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, *extra, mode="ok", exit_code=0, brief=None):
        env = dict(os.environ, CODEX_BIN=str(self.fake), FAKE_LOG=str(self.log),
                   FAKE_MODE=mode, FAKE_EXIT=str(exit_code))
        argv = [sys.executable, str(SCRIPT), "--cd", str(self.dir),
                "--brief", str(brief or self.brief), "--out", str(self.out), *extra]
        # stdin 給一個有內容的管道：腳本要自己換成 /dev/null，假 codex 才會立刻讀到 EOF
        r = subprocess.run(argv, input="不該被 codex 讀到", capture_output=True, text=True,
                           env=env, timeout=60)
        lines = r.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1, r.stdout)
        return r.returncode, json.loads(lines[0])

    def logged(self):
        return json.loads(self.log.read_text(encoding="utf-8"))

    def test_success_and_argv_shape(self):
        code, res = self.go()
        self.assertEqual(code, 0)
        self.assertTrue(res["ok"])
        self.assertEqual(res["exit"], 0)
        self.assertEqual(res["out"], str(self.out))
        self.assertEqual(res["out_bytes"], len("結果\n".encode()))
        self.assertFalse(res["timed_out"])
        self.assertIsNone(res["error"])
        argv = self.logged()["argv"]
        self.assertEqual(argv, ["exec", "--skip-git-repo-check", "-C", str(self.dir),
                                "-o", str(self.out), self.brief.read_text(encoding="utf-8")])
        self.assertFalse(any(a.startswith("--sandbox") or a == "-s" for a in argv))

    def test_stdin_is_dev_null(self):
        self.go()
        self.assertEqual(self.logged()["stdin"], "")

    def test_creates_output_dir(self):
        self.assertFalse(self.out.parent.exists())
        code, _ = self.go()
        self.assertEqual(code, 0)
        self.assertTrue(self.out.is_file())

    def test_stderr_tail(self):
        _, res = self.go()
        self.assertEqual(len(res["stderr_tail"]), 2000)
        self.assertTrue(res["stderr_tail"].endswith("尾巴"))

    def test_nonzero_exit(self):
        code, res = self.go(exit_code=7)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["exit"], 7)
        self.assertIn("7", res["error"])

    def test_empty_output(self):
        code, res = self.go(mode="empty")
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])
        self.assertEqual(res["exit"], 0)
        self.assertEqual(res["out_bytes"], 0)

    def test_missing_output(self):
        code, res = self.go(mode="none")
        self.assertEqual(code, 2)
        self.assertIn("不存在", res["error"])

    def test_timeout(self):
        code, res = self.go("--timeout", "1", mode="sleep")
        self.assertEqual(code, 3)
        self.assertFalse(res["ok"])
        self.assertTrue(res["timed_out"])
        self.assertIsNone(res["exit"])
        self.assertLess(res["elapsed_s"], 20)

    def test_brief_missing(self):
        code, res = self.go(brief=self.dir / "nope.md")
        self.assertEqual(code, 4)
        self.assertFalse(res["ok"])
        self.assertIn("brief", res["error"])
        self.assertFalse(self.log.exists())

    def test_usage_error(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--cd", "x"], capture_output=True,
                           text=True, timeout=60)
        self.assertEqual(r.returncode, 4)
        res = json.loads(r.stdout)
        self.assertFalse(res["ok"])
        self.assertIn("用法錯", res["error"])

    def test_delete_brief_on_success(self):
        code, _ = self.go("--delete-brief")
        self.assertEqual(code, 0)
        self.assertFalse(self.brief.exists())

    def test_delete_brief_on_failure(self):
        code, _ = self.go("--delete-brief", exit_code=1)
        self.assertEqual(code, 1)
        self.assertFalse(self.brief.exists())

    def test_keeps_brief_by_default(self):
        self.go()
        self.assertTrue(self.brief.exists())

    def test_codex_not_found(self):
        self.fake.unlink()
        code, res = self.go()
        self.assertEqual(code, 1)
        self.assertIsNone(res["exit"])
        self.assertIn("跑不起來", res["error"])


if __name__ == "__main__":
    unittest.main()
