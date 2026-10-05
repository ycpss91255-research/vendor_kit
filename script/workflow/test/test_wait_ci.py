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


RUN = "https://github.com/o/r/actions/runs/{}/job/{}"


class FailedLogs(unittest.TestCase):
    """--failed-logs：假 gh 依 argv 分派 pr checks 與 run view，並記錄收到的 argv。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = pathlib.Path(self.tmp.name)
        self.gh = d / "gh"
        self.cfg = d / "cfg.json"
        self.log = d / "argv.jsonl"
        self.gh.write_text(
            f"#!{sys.executable}\n"
            "import json, sys\n"
            f"cfg = json.load(open({str(self.cfg)!r}))\n"
            f"with open({str(self.log)!r}, 'a') as f:\n"
            "    f.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "a = sys.argv[1:]\n"
            "if a[:2] == ['pr', 'checks']:\n"
            "    print(json.dumps(cfg['checks']))\n"
            "    sys.exit(cfg.get('checks_code', 0))\n"
            "if a[:2] == ['run', 'view']:\n"
            "    r = cfg['runs'].get(a[2])\n"
            "    if r is None:\n"
            "        sys.stderr.write('HTTP 404: run not found')\n"
            "        sys.exit(1)\n"
            "    sys.stdout.write(r)\n"
            "    sys.exit(0)\n"
            "sys.exit(9)\n")
        self.gh.chmod(self.gh.stat().st_mode | stat.S_IEXEC)
        self.old = os.environ.get("WAIT_CI_GH")
        os.environ["WAIT_CI_GH"] = str(self.gh)

    def tearDown(self):
        if self.old is None:
            os.environ.pop("WAIT_CI_GH", None)
        else:
            os.environ["WAIT_CI_GH"] = self.old
        self.tmp.cleanup()

    def setup_gh(self, checks, runs=None):
        failing = any(ch["bucket"] in c.FAIL for ch in checks)
        self.cfg.write_text(json.dumps({"checks": checks, "runs": runs or {}, "checks_code": 1 if failing else 0}))

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(x) for x in self.log.read_text().splitlines()]

    def run_views(self):
        return [a for a in self.calls() if a[:2] == ["run", "view"]]

    def run_main(self, *argv):
        buf = StringIO()
        with redirect_stdout(buf):
            code = c.main(list(argv))
        return code, json.loads(buf.getvalue())

    @staticmethod
    def check(name, bucket, link):
        return {"name": name, "bucket": bucket, "state": bucket.upper(), "link": link}

    def test_failure_attaches_log_tail(self):
        log = "".join(f"line {i}\n" for i in range(1, 101))
        self.setup_gh([self.check("docs-lint", "fail", RUN.format(111, 1)),
                       self.check("docs-tool-test", "pass", RUN.format(222, 2))], {"111": log})
        code, out = self.run_main("12", "--interval", "0", "--repo", "o/r", "--failed-logs", "--log-lines", "3")
        self.assertEqual(code, 1)
        self.assertEqual(out["failed_logs"], [
            {"name": "docs-lint", "run_id": 111, "tail": "line 98\nline 99\nline 100", "error": None}])
        self.assertEqual(self.run_views(), [["run", "view", "111", "-R", "o/r", "--log-failed"]])
        self.assertEqual(out["checks"], [{"name": "docs-lint", "state": "FAIL"},
                                         {"name": "docs-tool-test", "state": "PASS"}])

    def test_default_log_lines_is_80(self):
        log = "".join(f"l{i}\n" for i in range(200))
        self.setup_gh([self.check("a", "fail", RUN.format(5, 1))], {"5": log})
        _, out = self.run_main("12", "--interval", "0", "--failed-logs")
        self.assertEqual(len(out["failed_logs"][0]["tail"].splitlines()), 80)
        self.assertTrue(out["failed_logs"][0]["tail"].endswith("l199"))

    def test_same_run_fetched_once(self):
        self.setup_gh([self.check("a", "fail", RUN.format(7, 1)),
                       self.check("b", "cancel", RUN.format(7, 2))], {"7": "boom\n"})
        code, out = self.run_main("12", "--interval", "0", "--failed-logs")
        self.assertEqual(code, 1)
        self.assertEqual(len(self.run_views()), 1)
        self.assertEqual([(x["name"], x["run_id"], x["tail"]) for x in out["failed_logs"]],
                         [("a", 7, "boom"), ("b", 7, "boom")])

    def test_link_without_run_id_sets_error(self):
        self.setup_gh([self.check("ext", "fail", "https://example.com/status/1")])
        code, out = self.run_main("12", "--interval", "0", "--failed-logs")
        self.assertEqual(code, 1)
        [entry] = out["failed_logs"]
        self.assertEqual(entry["name"], "ext")
        self.assertIsNone(entry["run_id"])
        self.assertIsNone(entry["tail"])
        self.assertTrue(entry["error"])
        self.assertEqual(self.run_views(), [])

    def test_run_view_failure_sets_error(self):
        self.setup_gh([self.check("a", "fail", RUN.format(9, 1))])
        code, out = self.run_main("12", "--interval", "0", "--failed-logs")
        self.assertEqual(code, 1)
        [entry] = out["failed_logs"]
        self.assertEqual(entry["run_id"], 9)
        self.assertIsNone(entry["tail"])
        self.assertIn("404", entry["error"])

    def test_all_pass_gives_empty_list(self):
        self.setup_gh([self.check("a", "pass", RUN.format(3, 1))])
        code, out = self.run_main("12", "--interval", "0", "--failed-logs")
        self.assertEqual(code, 0)
        self.assertEqual(out["failed_logs"], [])
        self.assertEqual(self.run_views(), [])

    def test_without_flag_output_unchanged(self):
        self.setup_gh([self.check("a", "fail", RUN.format(4, 1))], {"4": "x\n"})
        code, out = self.run_main("12", "--interval", "0")
        self.assertEqual(code, 1)
        self.assertNotIn("failed_logs", out)
        self.assertEqual(set(out), {"pr", "all_pass", "timed_out", "checks"})
        self.assertEqual(self.run_views(), [])

    def test_checks_query_requests_link(self):
        self.setup_gh([self.check("a", "pass", RUN.format(3, 1))])
        self.run_main("12", "--interval", "0")
        [first] = self.calls()
        self.assertEqual(first[first.index("--json") + 1], "name,state,bucket,link")

    def test_bad_log_lines(self):
        code, out = self.run_main("12", "--failed-logs", "--log-lines", "0")
        self.assertEqual(code, 3)
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
