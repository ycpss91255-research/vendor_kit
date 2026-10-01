"""terms_context.py 的測試：用 subprocess 跑 hook，CLAUDE_PROJECT_DIR 指到暫存的 GLOSSARY.md。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "terms_context.py"


def run_hook(glossary: str | None) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        if glossary is not None:
            (Path(tmp) / "GLOSSARY.md").write_text(glossary, encoding="utf-8")
        env = {**os.environ, "CLAUDE_PROJECT_DIR": tmp}
        return subprocess.run(
            [sys.executable, str(HOOK)], input="{}", env=env,
            capture_output=True, text=True, check=True,
        ).stdout.strip()


class TermsContextTest(unittest.TestCase):
    def test_both_paren_styles_and_bare(self):
        out = run_hook(
            "# G\n\n## Language\n\n### 群\n\n"
            "**VK** (vendor_kit)：\n定義。\n\n"
            "**導入**（consume）：\n定義。\n\n"
            "**名詞**：\n定義。\n"
        )
        text = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("正式名詞（3 個）", text)
        self.assertIn("VK (vendor_kit)", text)
        self.assertIn("導入（consume）", text)
        self.assertIn("、名詞", text)

    def test_no_glossary_is_silent(self):
        self.assertEqual(run_hook(None), "")


if __name__ == "__main__":
    unittest.main()
