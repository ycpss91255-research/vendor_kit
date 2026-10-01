"""check_review_pages.py 的規則：跑法 `python3 -m unittest discover -s script/doc/test`。"""
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

    def test_any_html_fails_including_ins(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n<a id=\"x\"></a>名詞 <ins>底線</ins>，第一行<br>第二行，`<repo>` 是占位符\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("'a'", out)
        self.assertIn("'br'", out)
        self.assertIn("'ins'", out)
        self.assertNotIn("'repo'", out)

    def test_messages_page_commands_must_be_defined_earlier(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`just vendor_kit upgrade --engine` `just vendor_kit add <repo> -z`\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("-z", out)
        self.assertNotIn("用了 --engine", out)

    def test_messages_csv_commands_must_be_defined_earlier(self):
        # CSV 不准 Markdown，指令沒有反引號；掃 situation、message、next_step 三欄，錯誤位置報 <檔>:<代碼>:<欄名>
        self.write("01_a.md", "# 01\n\n## 目錄\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n")
        pathlib.Path("doc/contract/03_m.csv").write_text(
            "\ufeffcode,status,level,exit_code,disposition,situation,message,description,next_step\n"
            "VK0001,active,warn,1,,開發模式中執行 just vendor_kit undev …,"
            "Run just vendor_kit upgrade --engine and retry.,中文說明,just vendor_kit upgrade --engine\n"
            "VK0002,active,error,2,需人處理,執行 just vendor_kit add --bad 也不行,"
            "Run just vendor_kit upgrade <repo> -z and retry.,中文說明 just vendor_kit test --description-only,"
            "just vendor_kit upgrade <repo> -z\n",
            encoding="utf-8",
        )
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(
            "03_m.csv:VK0002:message: 指令 `just vendor_kit upgrade <repo> -z` 用了 -z",
            out,
        )
        self.assertIn(
            "03_m.csv:VK0002:next_step: 指令 `just vendor_kit upgrade <repo> -z` 用了 -z",
            out,
        )
        self.assertIn("03_m.csv:VK0002:situation: 指令 `just vendor_kit add --bad` 用了 --bad", out)
        self.assertNotIn("VK0001", out)
        self.assertNotIn("--description-only", out)

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

    def test_backtick_in_link_text_fails(self):
        # 對外頁（README、doc/contract/0N_*.md）的連結文字不得含反引號；錯誤位置報 <檔>:<行>
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n\n見 [`VK0001`](01_a.md#第一節) 與 [結束碼 `2`](01_a.md#第一節)。\n")
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n[`just vendor_kit`](doc/contract/01_a.md)\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for want in (
            "doc/contract/01_a.md:7: 連結文字不得含反引號：[`VK0001`](01_a.md#第一節)",
            "doc/contract/01_a.md:7: 連結文字不得含反引號：[結束碼 `2`](01_a.md#第一節)",
            "README.md:5: 連結文字不得含反引號：[`just vendor_kit`](doc/contract/01_a.md)",
        ):
            self.assertIn(want, out)
        self.assertEqual(out.count("連結文字不得含反引號"), 3)

    def test_code_outside_link_text_passes(self):
        # 維護者定案的寫法：只連「結束碼」或「訊息」，碼放在連結外；非對外頁（GLOSSARY.md）不檢查
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n\n[結束碼](01_a.md#第一節) `2`、[訊息](01_a.md#第一節) `VK0005`。\n")
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n[`--engine`](README.md)\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_backtick_link_text_in_code_span_passes(self):
        # 行內程式碼裡的反例不算
        self.write("01_a.md", "# 01\n\n## 目錄\n\n不要寫 `` [`VK0028`](01_a.md) `` 這種寫法。\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_escaped_angle_link_text_passes(self):
        # 維護者定案 B 案：程式碼名詞當連結時直接寫名詞、< > 用反斜線跳脫；\<repo\> 不是 HTML 標籤
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n## 工具與出貨\n\n`<repo>`\n")
        self.write(
            "01_a.md",
            "# 01\n\n## 目錄\n\n## 第一節\n\n"
            "用 [\\<repo\\>](../../GLOSSARY.md#工具與出貨) 與 [dist/](01_a.md#第一節)，"
            "連結外的 \\<ns\\> 也不是標籤；例子 `[<repo>](01_a.md)` 在行內程式碼裡不算。\n",
        )
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n[\\<ns\\>/\\<repo\\>](GLOSSARY.md#工具與出貨)\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_unescaped_angle_in_link_text_fails(self):
        # 對外頁連結文字裡未跳脫的 <…> 要擋，提示改成 \<…\>；錯誤位置報 <檔>:<行>
        self.write("01_a.md", "# 01\n\n## 目錄\n\n## 第一節\n\n見 [<repo>](01_a.md#第一節)。\n")
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n[用 <ns> 分](doc/contract/01_a.md)\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for where, link in (
            ("doc/contract/01_a.md:7:", "[<repo>](01_a.md#第一節)"),
            ("README.md:5:", "[用 <ns> 分](doc/contract/01_a.md)"),
        ):
            hits = [l for l in out.splitlines() if l.startswith(where) and link in l and "\\<" in l]
            self.assertEqual(len(hits), 1, out)


if __name__ == "__main__":
    unittest.main()
