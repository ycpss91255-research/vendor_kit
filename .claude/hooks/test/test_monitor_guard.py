"""monitor_guard.py 的測試：用 subprocess 跑 hook，餵 PreToolUse 的 JSON。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "monitor_guard.py"


def run_hook(stdin: str) -> str:
    return subprocess.run(
        [sys.executable, str(HOOK)], input=stdin,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


class MonitorGuardTest(unittest.TestCase):
    def test_monitor_is_denied(self):
        out = run_hook(json.dumps({"tool_name": "Monitor", "tool_input": {}}))
        spec = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(spec["hookEventName"], "PreToolUse")
        self.assertEqual(spec["permissionDecision"], "deny")
        self.assertIn("run_in_background", spec["permissionDecisionReason"])

    def test_other_tool_passes(self):
        self.assertEqual(run_hook(json.dumps({"tool_name": "Bash", "tool_input": {}})), "")

    def test_bad_input_passes(self):
        self.assertEqual(run_hook("not json"), "")


if __name__ == "__main__":
    unittest.main()
