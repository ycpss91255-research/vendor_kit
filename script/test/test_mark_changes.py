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


class CsvTest(unittest.TestCase):
    """審閱頁旁的同名 CSV：跟 .md 共用版本號，合併成一份標示版；CSV 部分依 code 逐欄標示。"""

    GREEN = '<mark style="background-color:#c8f0c8">'
    RED = '<mark style="background-color:#f8c8c8">'
    # 表頭照 check_messages.FIELDS：note、invariant、details 三欄已刪
    HEAD = "code,status,level,disposition,situation,message,next_step\n"
    OLD = ("\ufeff" + HEAD + "VK0001,active,error,失敗,舊情境,舊本文 <repo>,\n"
           "VK0002,active,warn,,情境,不變,\nVK0003,active,error,失敗,要停用的情境,要停用,\n")
    NEW = ("\ufeff" + HEAD + "VK0001,active,error,需人處理,新情境,新本文 <repo>,重跑 <repo>\n"
           "VK0002,active,warn,,情境,不變,\nVK0003,retired,,,,,\n"
           "VK0004,active,warn,,新增的情境,\"第一行\n第二行\",\n")

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)
        pathlib.Path("doc/decisions/review_log").mkdir(parents=True)
        pathlib.Path("doc/decisions/review_log/versions.json").write_text('{"03_messages": 8}\n')
        pathlib.Path("doc/contract/03_messages.md").write_text("# 03\n\n規則\n")
        pathlib.Path("doc/contract/03_messages.csv").write_text(self.NEW, encoding="utf-8")

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def backup(self, ext, text):
        pathlib.Path(f"doc/decisions/_backup/doc_contract_03_messages.pre_r1{ext}").write_text(text, encoding="utf-8")

    def marked(self, rev=9):
        return pathlib.Path(f"doc/decisions/_marked/03_messages.v{rev}.marked.md").read_text()

    def test_outputs_share_one_version(self):
        self.backup(".md", "# 03\n\n舊規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_messages", "pre_r1")
        out = pathlib.Path("doc/decisions/_marked")
        self.assertEqual(sorted(p.name for p in out.iterdir()),
                         ["03_messages.v9.csv", "03_messages.v9.marked.md", "03_messages.v9.md"])
        # CSV 副本逐位元組照抄（BOM 保留）
        self.assertEqual((out / "03_messages.v9.csv").read_bytes(),
                         pathlib.Path("doc/contract/03_messages.csv").read_bytes())
        self.assertIn('"03_messages": 9', pathlib.Path("doc/decisions/review_log/versions.json").read_text())
        text = self.marked()
        # md 部分照舊逐行標示，CSV 部分接在後面
        self.assertLess(text.index(self.GREEN + "規則</mark>"), text.index("## 03_messages.csv 的逐碼差異"))

    def test_csv_path_is_same_as_page_name(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("doc/contract/03_messages.csv", "pre_r1")
        self.assertTrue(pathlib.Path("doc/decisions/_marked/03_messages.v9.marked.md").exists())

    def test_per_code_per_field(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_messages", "pre_r1")
        text = self.marked()
        lines = text.splitlines()
        # 改欄位：舊值紅、新值綠；沒改的欄不標；占位符照原樣看得到
        self.assertIn(f"- `disposition`：{self.RED}失敗</mark> → {self.GREEN}需人處理</mark>", lines)
        self.assertIn(f"- `situation`：{self.RED}舊情境</mark> → {self.GREEN}新情境</mark>", lines)
        self.assertIn(f"- `message`：{self.RED}舊本文 &lt;repo&gt;</mark> → {self.GREEN}新本文 &lt;repo&gt;</mark>", lines)
        self.assertIn(f"- `next_step`：{self.RED}（空）</mark> → {self.GREEN}重跑 &lt;repo&gt;</mark>", lines)
        self.assertIn("- `status`：active", lines)
        self.assertIn("- `level`：error", lines)
        # 沒改的代碼不成段，只在摘要
        self.assertNotIn("#### VK0002", lines)
        self.assertIn("沒改動的代碼 1 個：VK0002。", lines)
        # 停用：整段註記，改掉的欄都標
        i = lines.index("#### VK0003")
        self.assertEqual(lines[i + 1], self.RED + "（本碼停用）</mark>")
        self.assertIn(f"- `status`：{self.RED}active</mark> → {self.GREEN}retired</mark>", lines[i:])
        # 新增：整段綠，格內換行改成 <br>
        i = lines.index("#### VK0004")
        self.assertEqual(lines[i + 1], self.GREEN + "（本碼新增）</mark>")
        self.assertIn(f"- `situation`：{self.GREEN}新增的情境</mark>", lines[i:])
        self.assertIn(f"- `message`：{self.GREEN}第一行<br>第二行</mark>", lines[i:])
        # 標題不加標籤（錨點不變）
        for line in lines:
            if line.startswith("#"):
                self.assertNotIn("<", line)

    def test_removed_column(self):
        # 舊表頭多一欄 note：VK0001 的 note 有值、VK0002 的 note 是空的
        old_head = self.HEAD.rstrip("\n") + ",note\n"
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", "\ufeff" + old_head + "VK0001,active,error,失敗,舊情境,舊本文 <repo>,,舊值\n"
                    "VK0002,active,warn,,情境,不變,,\nVK0003,active,error,失敗,要停用的情境,要停用,,\n")
        mark_changes.build("03_messages", "pre_r1")
        lines = self.marked().splitlines()
        self.assertIn(f"- 表頭：{self.RED}{old_head.strip()}</mark> → {self.GREEN}{self.HEAD.strip()}</mark>", lines)
        self.assertIn(f"- `note`：{self.RED}（本欄刪除）</mark>", lines)
        # 刪掉的欄在各碼標紅舊值
        i = lines.index("#### VK0001")
        j = lines.index("", i + 2)
        self.assertIn(f"- `note`：{self.RED}舊值</mark> {self.RED}（本欄刪除）</mark>", lines[i:j])
        # 舊值是空的代碼不因刪欄而算改動
        self.assertNotIn("#### VK0002", lines)
        self.assertIn("沒改動的代碼 1 個：VK0002。", lines)

    def test_added_column(self):
        # 舊表頭沒有 next_step
        old_head = self.HEAD.replace(",next_step", "")
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", "\ufeff" + old_head + "VK0001,active,error,失敗,舊情境,舊本文 <repo>\n"
                    "VK0002,active,warn,,情境,不變\nVK0003,active,error,失敗,要停用的情境,要停用\n")
        mark_changes.build("03_messages", "pre_r1")
        lines = self.marked().splitlines()
        self.assertIn(f"- 表頭：{self.RED}{old_head.strip()}</mark> → {self.GREEN}{self.HEAD.strip()}</mark>", lines)
        self.assertIn(f"- `next_step`：{self.GREEN}（本欄新增）</mark>", lines)
        self.assertNotIn(f"- `next_step`：{self.RED}（本欄刪除）</mark>", lines)
        self.assertIn(f"- `next_step`：{self.RED}（空）</mark> → {self.GREEN}重跑 &lt;repo&gt;</mark>", lines)
        self.assertIn("沒改動的代碼 1 個：VK0002。", lines)

    def test_removed_row(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD + "VK0009,active,warn,,拿掉的情境,拿掉,\n")
        mark_changes.build("03_messages", "pre_r1")
        lines = self.marked().splitlines()
        i = lines.index("#### VK0009")
        self.assertEqual(lines[i + 1], self.RED + "（本列刪除）</mark>")
        self.assertIn(f"- `situation`：{self.RED}拿掉的情境</mark>", lines[i:])
        self.assertIn(f"- `message`：{self.RED}拿掉</mark>", lines[i:])

    def test_md_backup_missing_means_md_unchanged(self):
        self.backup(".csv", self.OLD)
        mark_changes.build("03_messages", "pre_r1")
        text = self.marked()
        self.assertIn("> 注意：沒有 doc/contract/03_messages.md 的基準版 pre_r1：視為這一輪沒改", text)
        self.assertNotIn(self.GREEN + "規則</mark>", text)
        self.assertIn("#### VK0001", text)

    def test_csv_backup_missing_and_not_in_git_means_new(self):
        self.backup(".md", "# 03\n\n規則\n")
        mark_changes.build("03_messages", "pre_r1")
        text = self.marked()
        self.assertIn("視為新建，整份標新增", text)
        for code in ("VK0001", "VK0002", "VK0003", "VK0004"):
            self.assertIn(f"#### {code}\n{self.GREEN}（本碼新增）</mark>", text)

    def test_both_backups_missing_fails(self):
        with self.assertRaises(SystemExit):
            mark_changes.build("03_messages", "pre_r1")

    def test_old_version_files_removed(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_messages", "pre_r1")
        mark_changes.build("03_messages", "pre_r1")
        names = sorted(p.name for p in pathlib.Path("doc/decisions/_marked").iterdir())
        self.assertEqual(names, ["03_messages.v10.csv", "03_messages.v10.marked.md", "03_messages.v10.md"])

    def test_csv_backup_path(self):
        self.backup(".csv", self.OLD)
        self.assertEqual(mark_changes.backup_path("03_messages", "pre_r1", ".csv"),
                         pathlib.Path("doc/decisions/_backup/doc_contract_03_messages.pre_r1.csv"))


if __name__ == "__main__":
    unittest.main()
