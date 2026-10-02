"""check_review_pages.py 的規則：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

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
        self.write("01_a.md", "# 01\n\n> 版本 v3\n\n## 目錄\n\n依 [02](02_b.md)。\n\n出處：ADR-0001\n")
        self.write("02_b.md", "# 02\n\n## 目錄\n\n[壞錨點](01_a.md#沒有這節)\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for want in ("內容只能往前依賴", "不寫「出處」", "不寫版本號", "錨點不存在"):
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
        pathlib.Path("doc/contract/reason_codes.csv").write_text(
            "\ufeffcode,status,level,exit_code,disposition,situation,message,description,next_step\n"
            "VK0001,active,warn,1,,開發模式中執行 just vendor_kit undev …,"
            "Run just vendor_kit upgrade --engine and retry.,中文說明,just vendor_kit upgrade --engine\n"
            "VK0002,active,error,2,待處理,執行 just vendor_kit add --bad 也不行,"
            "Run just vendor_kit upgrade <repo> -z and retry.,中文說明 just vendor_kit test --description-only,"
            "just vendor_kit upgrade <repo> -z\n",
            encoding="utf-8",
        )
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn(
            "reason_codes.csv:VK0002:message: 指令 `just vendor_kit upgrade <repo> -z` 用了 -z",
            out,
        )
        self.assertIn(
            "reason_codes.csv:VK0002:next_step: 指令 `just vendor_kit upgrade <repo> -z` 用了 -z",
            out,
        )
        self.assertIn("reason_codes.csv:VK0002:situation: 指令 `just vendor_kit add --bad` 用了 --bad", out)
        # 訊息表明列 reason_codes.csv（#137）；其他 03_*.csv 不掃
        pathlib.Path("doc/contract/03_other.csv").write_text(
            "code,situation,message,next_step\nVK0009,just vendor_kit add --other,,\n", encoding="utf-8")
        _, out = self.run_main()
        self.assertNotIn("--other", out)
        self.assertNotIn("VK0001", out)
        self.assertNotIn("--description-only", out)

    def test_l1_reason_codes_fail_in_early_pages_including_inline_code(self):
        for page in ("01_a.md", "02_b.md"):
            for text in ("VK0001", "`VK0001`"):
                with self.subTest(page=page, text=text):
                    self.write(page, f"# 頁\n\n## 目錄\n\n{text}\n")
                    code, out = self.run_main()
                    self.assertEqual(code, 1, out)
                    self.assertIn("L1", out)
                    pathlib.Path("doc/contract", page).unlink()

    def test_l1_fenced_codes_and_later_page_codes_pass(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n```text\nVK0001\n```\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`VK0001`\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_l2_exit_values_fail_on_both_sides(self):
        for page in ("01_a.md", "02_b.md"):
            for text in ("結束碼 `2`", "`2` 是結束碼", "結束碼 exit code 2"):
                with self.subTest(page=page, text=text):
                    self.write(page, f"# 頁\n\n## 目錄\n\n{text}\n")
                    code, out = self.run_main()
                    self.assertEqual(code, 1, out)
                    pathlib.Path("doc/contract", page).unlink()

    def test_l2_distant_values_and_fenced_examples_pass(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n結束碼" + "甲" * 11 + "`2`\n\n```text\n結束碼 `2`\nexit code 2\n```\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_l3_readme_argument_links_fail(self):
        self.write("02_b.md", "# 02\n\n## 目錄\n")
        for prefix in ("依", "依照"):
            with self.subTest(prefix=prefix):
                pathlib.Path("README.md").write_text(f"# VK\n\n## 目錄\n\n{prefix} [不變量](doc/contract/02_b.md)。\n")
                code, out = self.run_main()
                self.assertEqual(code, 1, out)
                self.assertIn("README.md:5:", out)

    def test_l3_navigation_links_pass_for_readme_and_early_pages(self):
        self.write("01_a.md", "# 01\n\n## 目錄\n\n詳見 [介面](04_i.md)。\n")
        self.write("04_i.md", "# 04\n\n## 目錄\n")
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n詳見 [介面](doc/contract/04_i.md)。\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_l4_recipe_options_fail_across_pages(self):
        for page in ("README.md", "doc/contract/03_m.md"):
            for command in ("update --missing", "just vendor_kit update --missing", "add <repo> --"):
                with self.subTest(page=page, command=command):
                    pathlib.Path(page).write_text(f"# 頁\n\n## 目錄\n\n`{command}`\n")
                    code, out = self.run_main()
                    self.assertEqual(code, 1, out)
                    self.assertIn("用了 --", out)
                    pathlib.Path(page).unlink()
                    pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n")

    def test_l4_interface_is_out_of_scope(self):
        self.write("04_i.md", "# 04\n\n## 目錄\n\n`update --foo`\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_l4_options_require_exact_inline_tokens(self):
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n`--engine-extra` `--image`\n文字 --missing\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`upgrade --engine` `dev -i image` `update --missing`\n")
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        for token in ("--engine", "-i", "--missing"):
            self.assertIn(f"用了 {token}，", out)

    def test_l4_defined_tokens_and_non_recipe_code_pass(self):
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n`--engine` `-i` `--`\n")
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`upgrade --engine=value` `dev -i image` `add <repo> --` `other --missing`\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_l4_csv_short_recipes_and_separator_fail(self):
        self.write("03_m.md", "# 03\n\n## 目錄\n")
        pathlib.Path("doc/contract/reason_codes.csv").write_text(
            "code,situation,message,next_step,description\n"
            "VK0001,update --missing,add <repo> --,upgrade --missing,update --ignored\n"
        )
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        for field in ("situation", "message", "next_step"):
            self.assertIn(f"reason_codes.csv:VK0001:{field}:", out)
        self.assertNotIn("--ignored", out)

    def test_allowlist_exact_match_is_waived_but_new_violation_fails(self):
        self.write("02_b.md", "# 02\n\n## 目錄\n")
        pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n依 [不變量](doc/contract/02_b.md)。\n")
        errors = []
        c.check_page(pathlib.Path("README.md"), errors)
        self.assertEqual(len(errors), 1, errors)
        with mock.patch.object(c, "TEMP_ALLOWLIST", {errors[0]: "#135 待修；審完 README 後移除"}):
            code, out = self.run_main()
            self.assertEqual(code, 0, out)
            self.assertIn("暫時白名單：1 筆；本次命中 1 筆", out)
            pathlib.Path("README.md").write_text("# VK\n\n## 目錄\n\n依照 [另一條不變量](doc/contract/02_b.md)。\n")
            code, out = self.run_main()
            self.assertEqual(code, 1, out)
            self.assertIn("本次命中 0 筆", out)
            self.assertIn("L3", out)

    def test_allowlist_entries_document_issue_and_expiry(self):
        for error, reason in c.TEMP_ALLOWLIST.items():
            with self.subTest(error=error):
                self.assertIn("#135 待修", reason)
                self.assertRegex(reason, r"審完 (?:03|README) 後移除")

    def test_missing_readme_and_pages_are_skipped(self):
        # README.md 或 doc/contract/ 還不存在時少掃那些，不崩潰
        pathlib.Path("README.md").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("OK: 掃 0 個對外文件", out)
        pathlib.Path("doc/contract").rmdir()
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_missing_glossary_skips_option_checks(self):
        # 沒有 GLOSSARY.md（main 上仍是 CONTEXT.md）時，選項 token 比對整段跳過，其他規則照查
        pathlib.Path("GLOSSARY.md").unlink()
        self.write("03_m.md", "# 03\n\n## 目錄\n\n`update --missing`\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.write("03_m.md", "# 03\n\n`update --missing`\n")
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("沒有「## 目錄」", out)
        self.assertNotIn("--missing", out)

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
        self.write("03_m.md", "# 03\n\n## 目錄\n\n## 第一節\n\n[結束碼](03_m.md#第一節) `2`、[訊息](03_m.md#第一節) `VK0005`。\n")
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n[`--engine`](README.md)\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_backtick_link_text_in_code_span_passes(self):
        # 行內程式碼裡的反例不算
        self.write("03_m.md", "# 03\n\n## 目錄\n\n不要寫 `` [`VK0028`](03_m.md) `` 這種寫法。\n")
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
