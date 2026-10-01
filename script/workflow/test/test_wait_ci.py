"""wait_ci.py：用假的 gh 與假時鐘測輪詢與結束碼，不打 GitHub。"""
import json
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import wait_ci as c  # noqa: E402


def chk(name, bucket, state=None):
    return {"name": name, "bucket": bucket, "state": state or bucket.upper()}


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += s


def seq(*rounds):
    it = iter(rounds)
    last = []

    def fetch(pr, repo):
        nonlocal last
        last = next(it, last)
        return last
    return fetch


class Wait(unittest.TestCase):
    def go(self, fetch, timeout=600, interval=15):
        clk = FakeClock()
        return c.wait("7", "o/r", timeout, interval, fetch_fn=fetch, sleep=clk.sleep, clock=clk)

    def test_all_pass(self):
        res, code = self.go(seq([chk("a", "pending")], [chk("a", "pass", "SUCCESS"), chk("b", "skipping")]))
        self.assertEqual(code, 0)
        self.assertTrue(res["all_pass"])
        self.assertEqual(res["checks"], [{"name": "a", "state": "SUCCESS"}, {"name": "b", "state": "SKIPPING"}])

    def test_failure(self):
        res, code = self.go(seq([chk("a", "pass"), chk("b", "fail", "FAILURE")]))
        self.assertEqual(code, 1)
        self.assertFalse(res["all_pass"])

    def test_cancel_counts_as_failure(self):
        _, code = self.go(seq([chk("a", "cancel")]))
        self.assertEqual(code, 1)

    def test_no_checks_yet_keeps_waiting(self):
        res, code = self.go(seq([], [], [chk("a", "pass")]))
        self.assertEqual(code, 0)

    def test_timeout(self):
        res, code = self.go(seq([chk("a", "pending")]), timeout=60, interval=15)
        self.assertEqual(code, 2)
        self.assertTrue(res["timed_out"])
        self.assertFalse(res["all_pass"])

    def test_waits_until_every_check_done(self):
        res, code = self.go(seq([chk("a", "fail"), chk("b", "pending")], [chk("a", "fail"), chk("b", "pass")]))
        self.assertEqual(code, 1)
        self.assertEqual(len(res["checks"]), 2)


class FakeGh(unittest.TestCase):
    """透過 WAIT_CI_GH 換成假的 gh 指令，測 main() 的解析與結束碼。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.gh = pathlib.Path(self.tmp.name) / "gh"
        self.old = os.environ.get("WAIT_CI_GH")
        os.environ["WAIT_CI_GH"] = str(self.gh)

    def tearDown(self):
        if self.old is None:
            os.environ.pop("WAIT_CI_GH", None)
        else:
            os.environ["WAIT_CI_GH"] = self.old
        self.tmp.cleanup()

    def fake(self, stdout="", stderr="", code=0):
        self.gh.write_text(
            "#!/bin/sh\n"
            f"cat <<'OUT'\n{stdout}\nOUT\n"
            f"cat >&2 <<'ERR'\n{stderr}\nERR\n"
            f"exit {code}\n")
        self.gh.chmod(self.gh.stat().st_mode | stat.S_IEXEC)

    def run_main(self, *argv):
        buf = StringIO()
        with redirect_stdout(buf):
            code = c.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_failing_checks_exit_nonzero_but_json_read(self):
        self.fake(json.dumps([chk("docs-lint", "fail", "FAILURE")]), code=1)
        code, out = self.run_main("12", "--interval", "0")
        self.assertEqual(code, 1)
        self.assertEqual(out["checks"], [{"name": "docs-lint", "state": "FAILURE"}])

    def test_pass(self):
        self.fake(json.dumps([chk("docs-lint", "pass", "SUCCESS")]))
        code, out = self.run_main("12", "--interval", "0")
        self.assertEqual(code, 0)
        self.assertTrue(out["all_pass"])

    def test_no_checks_then_timeout(self):
        self.fake(stderr="no checks reported on the 'x' branch", code=1)
        code, out = self.run_main("12", "--interval", "0", "--timeout", "0")
        self.assertEqual(code, 2)
        self.assertEqual(out["checks"], [])

    def test_gh_error(self):
        self.fake(stderr="HTTP 404: Not Found", code=1)
        code, out = self.run_main("12", "--interval", "0")
        self.assertEqual(code, 3)
        self.assertIn("404", out["error"])

    def test_non_numeric_pr(self):
        code, out = self.run_main("abc")
        self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()
