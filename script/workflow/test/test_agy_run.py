"""agy_run.py：用 AGY_BIN 換成假的 agy，測模型選擇、沿用、.part 改名、.err 清理與結束碼。"""
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "agy_run.py"

# 假 agy：行為由環境變數決定，每次被呼叫都把參數與工作目錄記到 FAKE_LOG
FAKE = r'''#!/usr/bin/env python3
import json, os, sys, time
with open(os.environ["FAKE_LOG"], "a") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd()}) + "\n")
if sys.argv[1:2] == ["models"]:
    sys.stdout.write(os.environ.get("FAKE_MODELS", ""))
    sys.exit(0)
sys.stdout.write(os.environ.get("FAKE_OUT", ""))
sys.stdout.flush()
sys.stderr.write(os.environ.get("FAKE_ERR", ""))
time.sleep(float(os.environ.get("FAKE_SLEEP", "0")))
sys.exit(int(os.environ.get("FAKE_EXIT", "0")))
'''

MODELS = """Fetching available models...
gemini-3.6-flash-high\tGemini 3.6 Flash (High)
gemini-3.10-flash-medium\tGemini 3.10 Flash (Medium)
gemini-3.9-flash-high\tGemini 3.9 Flash (High)
gemini-3.10-flash-low\tGemini 3.10 Flash (Low)
gemini-3.10-pro-high\tGemini 3.10 Pro (High)
gemini-3.8-flash-high\tGemini 3.8 Flash (High)
claude-sonnet-4-6\tClaude Sonnet 4.6
"""


class AgyRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = pathlib.Path(self.tmp.name)
        self.work = self.d / "work"
        self.work.mkdir()
        self.agy = self.d / "agy"
        self.agy.write_text(FAKE)
        self.agy.chmod(self.agy.stat().st_mode | stat.S_IXUSR)
        self.log = self.d / "log.jsonl"
        self.brief = self.work / "x_brief.md"
        self.brief.write_text("調查 X\n第二行")
        self.out = self.work / "x_agy.md"
        self.part = self.work / "x_agy.md.part"
        self.err = self.work / "x_agy.err"

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, *extra, **env):
        e = dict(os.environ, AGY_BIN=str(self.agy), FAKE_LOG=str(self.log), FAKE_MODELS=MODELS,
                 FAKE_OUT="結果\n")
        e.update({k: str(v) for k, v in env.items()})
        args = ["--cd", str(self.work), "--brief", str(self.brief), "--out", str(self.out), *extra]
        r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=e)
        lines = r.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1, r.stdout + r.stderr)
        return json.loads(lines[0]), r.returncode

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(x) for x in self.log.read_text().splitlines()]

    def test_auto_picks_latest_flash_high(self):
        res, code = self.go()
        self.assertEqual(code, 0, res)
        self.assertEqual(res["model"], "gemini-3.9-flash-high")
        run = self.calls()[-1]
        self.assertEqual(run["argv"], ["--model", "gemini-3.9-flash-high", "-p", "調查 X\n第二行"])
        self.assertEqual(pathlib.Path(run["cwd"]).resolve(), self.work.resolve())

    def test_given_model_skips_models(self):
        res, code = self.go("--model", "gemini-9.9-flash-high")
        self.assertEqual(code, 0, res)
        self.assertEqual(res["model"], "gemini-9.9-flash-high")
        self.assertEqual([c["argv"][0] for c in self.calls()], ["--model"])

    def test_success_renames_part(self):
        res, code = self.go()
        self.assertEqual(code, 0)
        self.assertTrue(res["ok"])
        self.assertFalse(res["reused"])
        self.assertEqual(self.out.read_text(), "結果\n")
        self.assertEqual(res["out_bytes"], len("結果\n".encode()))
        self.assertFalse(self.part.exists())

    def test_reuses_existing_nonempty_out(self):
        self.out.write_text("舊的")
        res, code = self.go()
        self.assertEqual(code, 0)
        self.assertTrue(res["ok"])
        self.assertTrue(res["reused"])
        self.assertEqual(self.out.read_text(), "舊的")
        self.assertEqual(self.calls(), [])

    def test_empty_out_is_rerun(self):
        self.out.write_text("")
        res, code = self.go("--model", "m")
        self.assertEqual(code, 0)
        self.assertFalse(res["reused"])
        self.assertEqual(self.out.read_text(), "結果\n")

    def test_failure_leaves_no_out(self):
        res, code = self.go("--model", "m", FAKE_EXIT=3, FAKE_ERR="壞了\n")
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["exit"], 3)
        self.assertIn("壞了", res["err_tail"])
        self.assertFalse(self.out.exists())
        self.assertFalse(self.part.exists())
        self.assertEqual(self.err.read_text(), "壞了\n")

    def test_empty_output(self):
        res, code = self.go("--model", "m", FAKE_OUT="")
        self.assertEqual(code, 2)
        self.assertFalse(self.out.exists())
        self.assertFalse(self.part.exists())

    def test_timeout_leaves_no_out(self):
        res, code = self.go("--model", "m", "--timeout", "0.5", FAKE_SLEEP=5)
        self.assertEqual(code, 3)
        self.assertTrue(res["timed_out"])
        self.assertFalse(self.out.exists())
        self.assertFalse(self.part.exists())

    def test_interrupted_partial_is_not_reused(self):
        # 上次被中斷留下的 .part 不算輸出，這次照跑並覆蓋
        self.part.write_text("半成品")
        res, code = self.go("--model", "m")
        self.assertEqual(code, 0)
        self.assertFalse(res["reused"])
        self.assertEqual(self.out.read_text(), "結果\n")
        self.assertFalse(self.part.exists())

    def test_empty_err_removed(self):
        res, code = self.go("--model", "m")
        self.assertEqual(code, 0)
        self.assertFalse(self.err.exists())

    def test_custom_err_path(self):
        err = self.d / "elsewhere.err"
        res, code = self.go("--model", "m", "--err", str(err), FAKE_ERR="警告\n")
        self.assertEqual(code, 0)
        self.assertEqual(err.read_text(), "警告\n")
        self.assertFalse(self.err.exists())

    def test_no_model_found(self):
        res, code = self.go(FAKE_MODELS="gemini-3.8-flash-low\tx\nclaude-sonnet-4-6\ty\n")
        self.assertEqual(code, 5)
        self.assertFalse(res["ok"])
        self.assertIn("flash-high", res["error"])
        self.assertEqual([c["argv"] for c in self.calls()], [["models"]])

    def test_missing_brief(self):
        self.brief.unlink()
        res, code = self.go("--model", "m")
        self.assertEqual(code, 4)
        self.assertFalse(res["ok"])
        self.assertEqual(self.calls(), [])

    def test_usage_error_is_json(self):
        e = dict(os.environ, AGY_BIN=str(self.agy))
        r = subprocess.run([sys.executable, str(SCRIPT), "--cd", str(self.work)],
                           capture_output=True, text=True, env=e)
        self.assertEqual(r.returncode, 4)
        res = json.loads(r.stdout)
        self.assertFalse(res["ok"])
        self.assertTrue(res["error"])


if __name__ == "__main__":
    unittest.main()
