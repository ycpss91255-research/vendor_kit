"""check_review_pages.py 的規則：跑法 `python3 -m unittest discover -s script/test`。"""
import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_review_pages as c  # noqa: E402


class SlugTest(unittest.TestCase):
    def test_github_style(self):
        self.assertEqual(c.slug("1. 使用者寫的內容歸使用者：可以建、要改先問"), "1-使用者寫的內容歸使用者可以建要改先問")
        self.assertEqual(c.slug("CI 檢查腳本"), "ci-檢查腳本")
        self.assertEqual(c.slug("<ins>引擎</ins> 版本"), "引擎-版本")


class RulesTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n`--engine`\n")
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n")

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def run_main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = c.main()
        return code, out.getvalue()

    def write(self, name, body):
        pathlib.Path("doc/contract", name).write_text(body)

    def test_clean_pages_pass(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n\n依 [01](01_a.md#第一節)。\n")
        self.assertEqual(self.run_main()[0], 0)

    def test_backward_link_provenance_version_and_anchor_fail(self):
        self.write("01_a.md", "# 01\n\n> 版本 v3\n\n## 目錄\n\n見 [02](02_b.md)。\n\n出處：ADR-0001\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n\n[壞錨點](01_a.md#沒有這節)\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for want in ("只能向前依賴", "不寫「出處」", "不寫版本號", "錨點不存在"):
            self.assertIn(want, out)

    def test_html_other_than_ins_fails(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n<a id=\"x\"></a>名詞 <ins>底線</ins>，第一行<br>第二行，`<repo>` 是占位符\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("'a'", out)
        self.assertIn("'br'", out)
        self.assertNotIn("'ins'", out)
        self.assertNotIn("'repo'", out)

    def test_messages_page_commands_must_be_defined_earlier(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`just vendor_kit upgrade --engine` `just vendor_kit add <repo> -z`\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("-z", out)
        self.assertNotIn("用了 --engine", out)

    def test_new_style_rule_citation_passes(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n\n依 [01 第 1 條](01_a.md#第一節)。\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_old_style_rule_citation_fails(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n\n依 [01](01_a.md#第一節) 第 1 條。\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("依 [頁名第 N 條](連結#錨點)", out)

    def test_old_style_rule_citation_in_code_span_passes(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n舊寫法 `[01](01_a.md) 第 1 條` 不要用。\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

if __name__ == "__main__":
    unittest.main()
