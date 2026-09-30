"""mark_changes.py 的標記格式與版本號行為：跑法 `python3 -m unittest discover -s script/test`。"""
import os
import pathlib
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import mark_changes  # noqa: E402


class MarkFormatTest(unittest.TestCase):
    GREEN = '<mark style="background-color:#c8f0c8">'
    RED = '<mark style="background-color:#f8c8c8">'

    def test_ins_is_green_mark(self):
        self.assertEqual(mark_changes.mark("新", "ins"), self.GREEN + "新</mark>")

    def test_del_is_red_mark_not_del_tag(self):
        out = mark_changes.mark("舊", "del")
        self.assertEqual(out, self.RED + "舊</mark>")
        self.assertNotIn("<del", out)

    def test_heading_prefix_stays_outside(self):
        self.assertEqual(mark_changes.wrap("## 目錄", "del"), "## " + self.RED + "目錄</mark>")

    def test_table_row_marked_per_cell(self):
        out = mark_changes.wrap("| a | b |", "del")
        self.assertEqual(out, "| " + self.RED + "a</mark> | " + self.RED + "b</mark> |")
        self.assertEqual(mark_changes.wrap("|---|:-:|", "ins"), "|---|:-:|")

    def test_build_uses_mark_for_both(self):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                pathlib.Path("doc/contract").mkdir(parents=True)
                pathlib.Path("doc/decisions/_backup").mkdir(parents=True)
                pathlib.Path("doc/contract/09_x.md").write_text("# 標題\n\n新內容\n")
                pathlib.Path("doc/decisions/_backup/doc_contract_09_x.pre_r1.md").write_text("# 標題\n\n舊內容\n")
                mark_changes.build("09_x", "pre_r1")
                text = pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").read_text()
            finally:
                os.chdir(cwd)
        self.assertIn(self.GREEN + "新內容</mark>", text)
        self.assertIn(self.RED + "舊內容</mark>", text)
        self.assertNotIn("<del", text)


class VersionTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def write_page(self, body, backup, key="doc_contract_09_x"):
        pathlib.Path("doc/contract/09_x.md").write_text(body)
        pathlib.Path(f"doc/decisions/_backup/{key}.pre_r1.md").write_text(backup)

    def test_rev_continues_from_tracked_table(self):
        # 新 clone：_marked/ 是空的，版本號照進 git 的表接下去，不從 v1 重來
        self.write_page("# 標題\n\n新內容\n", "# 標題\n\n舊內容\n")
        table = pathlib.Path("doc/decisions/review_log/versions.json")
        table.parent.mkdir(parents=True)
        table.write_text('{"09_x": 7}\n')
        mark_changes.build("09_x", "pre_r1")
        self.assertTrue(pathlib.Path("doc/decisions/_marked/09_x.v8.md").exists())
        self.assertIn('"09_x": 8', table.read_text())

    def test_official_and_plain_copy_have_no_version_line(self):
        # 版本號只在檔名：正式檔與正文副本內容相同，裡面不寫版本
        body = "# 標題\n\n新內容\n"
        self.write_page(body, "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        self.assertEqual(pathlib.Path("doc/contract/09_x.md").read_text(), body)
        self.assertEqual(pathlib.Path("doc/decisions/_marked/09_x.v1.md").read_text(), body)
        self.assertTrue(pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").exists())


class HeadingTest(unittest.TestCase):
    """標題行不加標籤：錨點（GitHub slug）要跟正式檔一樣，目錄連結才跳得過去。"""

    GREEN = '<mark style="background-color:#c8f0c8">'
    RED = '<mark style="background-color:#f8c8c8">'

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    @staticmethod
    def slug(heading):
        """GitHub 的錨點規則：小寫、去標點、空白換成 -。"""
        text = re.sub(r"^#+\s+", "", heading).strip().lower()
        return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")

    @staticmethod
    def heads(text):
        return [line for line in text.splitlines() if re.match(r"^#{1,6}\s", line)]

    def run_build(self, old, new):
        pathlib.Path("doc/contract/09_x.md").write_text(new)
        pathlib.Path("doc/decisions/_backup/doc_contract_09_x.pre_r1.md").write_text(old)
        mark_changes.build("09_x", "pre_r1")
        return pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").read_text()

    def assert_anchors_match(self, marked, new):
        got = self.heads(marked)
        for line in got:
            self.assertNotRegex(line, r"<[^>]+>")
        self.assertEqual([self.slug(h) for h in got], [self.slug(h) for h in self.heads(new)])

    def test_added_heading(self):
        old = "# 頁\n\n## 1. 甲\n\n內容\n"
        new = old + "\n## 2. 乙：新的, 一條\n\n新內容\n"
        marked = self.run_build(old, new)
        self.assert_anchors_match(marked, new)
        lines = marked.splitlines()
        i = lines.index("## 2. 乙：新的, 一條")
        self.assertEqual(lines[i + 1], self.GREEN + "（本節新增）</mark>")
        self.assertIn("2-乙新的-一條", [self.slug(h) for h in self.heads(marked)])

    def test_renamed_heading(self):
        old = "# 頁\n\n## 1. 舊名稱\n\n內容\n"
        new = "# 頁\n\n## 1. 新名稱\n\n內容\n"
        marked = self.run_build(old, new)
        self.assert_anchors_match(marked, new)
        lines = marked.splitlines()
        i = lines.index("## 1. 新名稱")
        self.assertEqual(lines[i + 1], self.RED + "舊標題：1. 舊名稱</mark>")
        self.assertEqual(lines[i + 2], self.GREEN + "（標題已修改）</mark>")
        self.assertNotIn("## 1. 舊名稱", marked)

    def test_deleted_heading(self):
        old = "# 頁\n\n## 1. 甲\n\n內容\n\n## 2. 要刪的\n\n舊內容\n"
        new = "# 頁\n\n## 1. 甲\n\n內容\n"
        marked = self.run_build(old, new)
        self.assert_anchors_match(marked, new)
        self.assertIn(self.RED + "2. 要刪的</mark>", marked.splitlines())

    def test_toc_anchor_unchanged(self):
        old = "# 頁\n\n## 目錄\n\n1. [甲](#1-甲)\n\n## 1. 甲\n"
        new = "# 頁\n\n## 目錄\n\n1. [甲](#1-甲)\n2. [乙](#2-乙)\n\n## 1. 甲\n\n## 2. 乙\n"
        marked = self.run_build(old, new)
        self.assert_anchors_match(marked, new)
        self.assertIn("](#2-乙)", marked)
        self.assertIn("2-乙", [self.slug(h) for h in self.heads(marked)])


class RelinkTest(unittest.TestCase):
    """標示版放在 _marked/：相對連結改寫成從 _marked/ 出發，解析回去要等於原本的目標。"""

    SRC = pathlib.Path("doc/contract/01_purpose.md")

    def back(self, rewritten):
        """把改寫後的目標從 _marked/ 解析回 repo 內路徑（錨點分開回傳）。"""
        file_part, _, anchor = rewritten.partition("#")
        return os.path.normpath(os.path.join(mark_changes.MARKED.as_posix(), file_part)), anchor

    def link(self, text):
        out = mark_changes.rewrite_links(text, self.SRC)
        return out[out.index("](") + 2:out.rindex(")")]

    def test_relative_targets_resolve_to_original(self):
        cases = {
            "../../GLOSSARY.md": ("GLOSSARY.md", ""),
            "02_invariants.md#4-永不靜默失敗": ("doc/contract/02_invariants.md", "4-永不靜默失敗"),
            "../adr/x.md": ("doc/adr/x.md", ""),
        }
        for dest, want in cases.items():
            with self.subTest(dest=dest):
                got = self.link(f"見 [名詞]({dest})。")
                self.assertNotEqual(got, dest)
                self.assertEqual(self.back(got), want)

    def test_review_page_links_point_to_official_file(self):
        got = self.link("[03](03_messages.md#結束碼)")
        self.assertEqual(got, "../../contract/03_messages.md#結束碼")

    def test_external_and_anchor_unchanged(self):
        for text in ("[a](https://git-scm.com/)", "[b](http://x.org/a.md)",
                     "[c](mailto:a@b.c)", "[d](#4-永不靜默失敗)"):
            with self.subTest(text=text):
                self.assertEqual(mark_changes.rewrite_links(text, self.SRC), text)

    def test_code_untouched(self):
        text = "`[x](../../GLOSSARY.md)` 與 [y](../../GLOSSARY.md)"
        out = mark_changes.rewrite_links(text, self.SRC)
        self.assertTrue(out.startswith("`[x](../../GLOSSARY.md)`"))
        self.assertNotIn("[y](../../GLOSSARY.md)", out)
        block = "```\n[x](../../GLOSSARY.md)\n```"
        self.assertEqual(mark_changes.rewrite_links(block, self.SRC), block)

    def test_angle_bracket_target(self):
        got = self.link("[a](<../adr/x y.md>)")
        self.assertTrue(got.startswith("<") and got.endswith(">"))
        self.assertEqual(self.back(got[1:-1]), ("doc/adr/x y.md", ""))

    def test_build_rewrites_both_outputs_not_original(self):
        cwd = os.getcwd()
        body = "# 標題\n\n見 [名詞](../../GLOSSARY.md#a)。\n"
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                pathlib.Path("doc/contract").mkdir(parents=True)
                pathlib.Path("doc/decisions/_backup").mkdir(parents=True)
                pathlib.Path("doc/contract/09_x.md").write_text(body)
                pathlib.Path("doc/decisions/_backup/doc_contract_09_x.pre_r1.md").write_text("# 標題\n")
                mark_changes.build("09_x", "pre_r1")
                official = pathlib.Path("doc/contract/09_x.md").read_text()
                copy = pathlib.Path("doc/decisions/_marked/09_x.v1.md").read_text()
                marked = pathlib.Path("doc/decisions/_marked/09_x.v1.marked.md").read_text()
            finally:
                os.chdir(cwd)
        self.assertEqual(official, body)
        self.assertIn("](../../../GLOSSARY.md#a)", copy)
        self.assertIn("](../../../GLOSSARY.md#a)", marked)


class BackupKeyTest(unittest.TestCase):
    """docs/ 併進 doc/ 之後，新備份用 doc_contract_<name>；之前的 docs_contract_<name> 照樣讀得到。"""

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def backup(self, key, suffix="pre_r1"):
        path = pathlib.Path(f"doc/decisions/_backup/{key}.{suffix}.md")
        path.write_text("舊\n")
        return path

    def test_old_page_key_still_found(self):
        old = self.backup("docs_contract_09_x")
        self.assertEqual(mark_changes.backup_path("09_x", "pre_r1"), old)

    def test_new_page_key_preferred(self):
        self.backup("docs_contract_09_x")
        new = self.backup("doc_contract_09_x")
        self.assertEqual(mark_changes.backup_path("09_x", "pre_r1"), new)

    def test_path_key_falls_back_to_old_prefix(self):
        # 以路徑指定的檔：doc/contract/README.md 的鍵是 doc_contract_README，也認 docs_contract_README
        old = self.backup("docs_contract_README")
        self.assertEqual(mark_changes.backup_path("doc/contract/README.md", "pre_r1"), old)
        new = self.backup("doc_contract_README")
        self.assertEqual(mark_changes.backup_path("doc/contract/README.md", "pre_r1"), new)


if __name__ == "__main__":
    unittest.main()
