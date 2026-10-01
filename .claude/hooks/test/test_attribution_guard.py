"""attribution_guard.py 的測試：用 subprocess 跑 hook，餵 PreToolUse 的 JSON。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "attribution_guard.py"
# 拆開拼，避免測試檔本身含完整的署名字串
CO_AUTHOR = "Co-Authored" + "-By: Claude <noreply@" + "anthropic.com>"


def run_hook(command: str, cwd: str = ".", tool: str = "Bash") -> str:
    payload = {"tool_name": tool, "tool_input": {"command": command}, "cwd": cwd}
    return subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(payload),
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def denied(out: str) -> bool:
    return bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


class AttributionGuardTest(unittest.TestCase):
    def test_commit_message_with_attribution_denied(self):
        self.assertTrue(denied(run_hook(f'git commit -m "feat: x\n\n{CO_AUTHOR}"')))

    def test_body_file_with_attribution_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "body.md").write_text(f"摘要\n\n{CO_AUTHOR}\n", encoding="utf-8")
            self.assertTrue(denied(run_hook("gh pr create --body-file body.md", cwd=tmp)))

    def test_clean_write_allowed(self):
        self.assertEqual(run_hook('git commit -m "feat: x\n\nRefs: #1"'), "")

    def test_read_only_command_allowed(self):
        self.assertEqual(run_hook(f'grep -r "{CO_AUTHOR}" .'), "")

    def test_non_bash_tool_ignored(self):
        self.assertEqual(run_hook(f'git commit -m "{CO_AUTHOR}"', tool="Edit"), "")


if __name__ == "__main__":
    unittest.main()
