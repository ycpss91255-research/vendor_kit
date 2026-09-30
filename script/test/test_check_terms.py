"""check_terms.py 的目錄規則：跑法 `python3 -m unittest discover -s script/test`。"""
import contextlib
import io
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_terms  # noqa: E402


class LayoutTest(unittest.TestCase):
    def test_docs_dir_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "doc").mkdir()
            self.assertEqual(check_terms.layout_errors(root), [])
            (root / "docs").mkdir()
            errs = check_terms.layout_errors(root)
            self.assertEqual(len(errs), 1)
            self.assertIn("一律用 doc/，不用 docs/", errs[0])

    def test_docs_file_is_not_a_dir(self):
        # 只擋目錄；同名檔案不是這條規則要管的
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "docs").write_text("")
            self.assertEqual(check_terms.layout_errors(root), [])


class CsvTest(unittest.TestCase):
    def test_csv_text_fields_scanned(self):
        # CSV 的文字欄也要擋 _Avoid_ 詞；位置報 <代碼>:<欄名>，固定值域的欄不掃
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "doc/contract").mkdir(parents=True)
            (root / "doc/contract/03_messages.csv").write_text(
                "\ufeffcode,status,level,exit_code,disposition,situation,message,description,next_step\n"
                "VK0001,舊詞,舊詞,舊詞,舊詞處置,舊詞情況,Old .version message,"
                "\"第一行\n舊詞說明\",Old term next step\n",
                encoding="utf-8",
            )
            cells = check_terms.csv_cells(root)
        fields = [
            "VK0001:situation",
            "VK0001:message",
            "VK0001:description",
            "VK0001:next_step",
        ]
        self.assertEqual([c[1] for c in cells], fields)
        patterns = [
            ("舊詞", check_terms.re.compile("舊詞")),
            (".version", check_terms.re.compile(r"\.version")),
        ]
        hits = {where: check_terms.line_hits(rel, value, patterns) for rel, where, value in cells}
        self.assertEqual(
            hits,
            {
                "VK0001:situation": ["舊詞"],
                "VK0001:message": [".version"],
                "VK0001:description": ["舊詞"],
                "VK0001:next_step": [],
            },
        )

    def test_quote_marker_and_u_tag_apply_to_cells(self):
        patterns = [("舊詞", check_terms.re.compile("舊詞"))]
        self.assertEqual(check_terms.line_hits("x.csv", "舊名：舊詞", patterns), [])
        self.assertEqual(check_terms.line_hits("x.csv", "<u>底線</u>", patterns), ["<u>（名詞改用連結）"])


class GlossaryLinkTest(unittest.TestCase):
    GLOSSARY = """# 名詞表

### 角色與情境

**VK** (vendor_kit)：
工具簡稱。
_Avoid_: 舊 VK

### 工具與出貨

**`<repo>`** (repository name)：
工具名。

**`dist/`**：
出貨目錄。

**工具** (tool)：
要導入的內容。

### VK recipe 與用途

**`test`**：
檢查用的 recipe。
"""

    def run_check(self, body):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "doc/contract").mkdir(parents=True)
            (root / "GLOSSARY.md").write_text(self.GLOSSARY, encoding="utf-8")
            page = root / "doc/contract/01_purpose.md"
            page.write_text(body, encoding="utf-8")
            old_root = check_terms.ROOT
            old_target_files = check_terms.target_files
            check_terms.ROOT = root
            check_terms.target_files = lambda: [page]
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out):
                    code = check_terms.main()
            finally:
                check_terms.ROOT = old_root
                check_terms.target_files = old_target_files
        return code, out.getvalue()

    def assert_term_failure(self, body, line, term):
        code, out = self.run_check(body)
        self.assertEqual(code, 1, out)
        self.assertIn(f"doc/contract/01_purpose.md:{line}", out)
        self.assertIn(term, out)

    def test_first_glossary_terms_linked_to_their_groups_pass(self):
        code, out = self.run_check(
            "# 目的\n\n"
            "[VK](../../GLOSSARY.md#角色與情境) 把 "
            "[\\<repo\\>](../../GLOSSARY.md#工具與出貨) 的 "
            "[dist/](../../GLOSSARY.md#工具與出貨) 當成"
            "[工具](../../GLOSSARY.md#工具與出貨)；後面的 VK 與工具不必再連。\n"
        )
        self.assertEqual(code, 0, out)

    def test_unlinked_first_term_fails(self):
        self.assert_term_failure("# 目的\n\nVK 管理工具。\n", 3, "VK")

    def test_link_to_wrong_glossary_group_fails(self):
        self.assert_term_failure(
            "# 目的\n\n[VK](../../GLOSSARY.md#工具與出貨) 管理工具。\n",
            3,
            "VK",
        )

    def test_link_to_missing_glossary_anchor_fails(self):
        self.assert_term_failure(
            "# 目的\n\n[VK](../../GLOSSARY.md#不存在) 管理工具。\n",
            3,
            "VK",
        )

    def test_ins_tag_fails(self):
        self.assert_term_failure("# 目的\n\n<ins>VK</ins> 管理工具。\n", 3, "<ins>")

    def test_heading_fenced_code_and_inline_code_do_not_count_as_first_use(self):
        code, out = self.run_check(
            "# VK 與工具\n\n"
            "```text\nVK 工具 <repo> dist/\n```\n\n"
            "`用 VK 管理工具的 <repo> dist/`\n\n"
            "正文的 [VK](../../GLOSSARY.md#角色與情境) 與"
            "[工具](../../GLOSSARY.md#工具與出貨)，來自 "
            "[\\<repo\\>](../../GLOSSARY.md#工具與出貨) 的 "
            "[dist/](../../GLOSSARY.md#工具與出貨)。\n"
        )
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
