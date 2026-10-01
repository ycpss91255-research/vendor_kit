"""settings.json 的 hook 註冊測試：註冊的檔都在、跑得起來，hook 目錄下的每支 hook 都有註冊。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import os
import shlex
import unittest
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = HOOKS_DIR.parents[1]
SETTINGS = PROJECT_DIR / ".claude" / "settings.json"

# 不是 hook、不註冊的檔：repo_paths.py 是給 hook import 的共用模組；
# test_guard.py 是 guard.py 的測試，還沒搬進 test/（搬走後從這裡拿掉）
NOT_HOOKS = {"repo_paths.py", "test_guard.py"}

PREFIXES = ("${CLAUDE_PROJECT_DIR}/", "$CLAUDE_PROJECT_DIR/")


def commands():
    data = json.loads(SETTINGS.read_text(encoding="utf-8"))
    for event, groups in data.get("hooks", {}).items():
        for group in groups:
            for hook in group.get("hooks", []):
                if hook.get("type") == "command":
                    yield event, hook["command"]


def resolve(command):
    """回傳 (是否以 python3 呼叫, 指到的檔)；路徑必須以 CLAUDE_PROJECT_DIR 開頭。"""
    parts = shlex.split(command)
    via_python = parts[0] in ("python3", "python")
    target = parts[1] if via_python else parts[0]
    for prefix in PREFIXES:
        if target.startswith(prefix):
            return via_python, PROJECT_DIR / target[len(prefix):]
    raise AssertionError(f"hook 指令沒用 CLAUDE_PROJECT_DIR 的相對寫法：{command}")


class SettingsHooksTest(unittest.TestCase):
    def test_registered_files_exist_and_runnable(self):
        found = list(commands())
        self.assertTrue(found, "settings.json 沒有註冊任何 hook")
        for event, command in found:
            with self.subTest(event=event, command=command):
                via_python, path = resolve(command)
                self.assertTrue(path.is_file(), f"{path} 不存在")
                if not via_python:
                    self.assertTrue(os.access(path, os.X_OK), f"{path} 沒有執行權限")

    def test_every_hook_is_registered(self):
        registered = {resolve(c)[1].name for _, c in commands()}
        on_disk = {p.name for p in HOOKS_DIR.glob("*.py")} - NOT_HOOKS
        self.assertEqual(sorted(on_disk - registered), [], "這些 hook 沒有在 settings.json 註冊")

    def test_whitelist_is_current(self):
        # 白名單裡的檔不在了就該拿掉，免得白名單默默變成任意豁免
        for name in NOT_HOOKS:
            with self.subTest(name=name):
                self.assertTrue((HOOKS_DIR / name).is_file())


if __name__ == "__main__":
    unittest.main()
