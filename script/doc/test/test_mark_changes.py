"""mark_changes.py 的標記格式、輸出位置與基準：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import contextlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import mark_changes  # noqa: E402


def out(key, suffix=".marked.md"):
    """送審資料夾裡的檔：doc/review/<鍵>/<鍵><後綴>，檔名不帶版本號。"""
    return pathlib.Path(f"doc/review/{key}/{key}{suffix}")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def init_repo():
    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    git("config", "commit.gpgsign", "false")


def commit_all(msg="c"):
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD")


def write_versions(pages, review_zip=0, finalized=None):
    path = pathlib.Path("doc/review/versions.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    table = {"review_zip": review_zip, "pages": pages}
    if finalized is not None:
        table["finalized"] = finalized
    path.write_text(json.dumps(table))

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
                text = out("09_x").read_text()
            finally:
                os.chdir(cwd)
        self.assertIn(self.GREEN + "新內容</mark>", text)
        self.assertIn(self.RED + "舊內容</mark>", text)
        self.assertNotIn("<del", text)


class OutputTest(unittest.TestCase):
    """輸出到 doc/review/<鍵>/，檔名固定、不帶版本號，每次覆蓋；這支不寫 versions.json。"""

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

    def test_fixed_names_no_version(self):
        self.write_page("# 標題\n\n新內容\n", "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        names = sorted(p.name for p in pathlib.Path("doc/review/09_x").iterdir())
        self.assertEqual(names, ["09_x.marked.md", "09_x.md"])
        text = out("09_x").read_text()
        self.assertNotRegex(text, r"v\d")
        self.assertFalse(pathlib.Path("doc/review/versions.json").exists())

    def test_rerun_overwrites(self):
        self.write_page("# 標題\n\n新內容\n", "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        pathlib.Path("doc/contract/09_x.md").write_text("# 標題\n\n再改\n")
        mark_changes.build("09_x", "pre_r1")
        self.assertEqual(out("09_x", ".md").read_text(), "# 標題\n\n再改\n")
        self.assertIn("再改", out("09_x").read_text())
        self.assertEqual(len(list(pathlib.Path("doc/review/09_x").iterdir())), 2)

    def test_official_and_plain_copy_have_no_version_line(self):
        # 正式檔與正文副本內容相同，裡面不寫版本
        body = "# 標題\n\n新內容\n"
        self.write_page(body, "# 標題\n\n舊內容\n")
        mark_changes.build("09_x", "pre_r1")
        self.assertEqual(pathlib.Path("doc/contract/09_x.md").read_text(), body)
        self.assertEqual(out("09_x", ".md").read_text(), body)

    def test_root_file_key(self):
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n")
        mark_changes.build("GLOSSARY.md", "new")
        self.assertTrue(out("GLOSSARY").exists())

    def test_suffix_mode_without_backup_dir_fails_clearly(self):
        pathlib.Path("doc/contract/09_x.md").write_text("# 標題\n")
        pathlib.Path("doc/decisions/_backup").rmdir()
        with self.assertRaises(SystemExit) as cm:
            mark_changes.build("09_x", "pre_r1")
        self.assertIn("doc/decisions/_backup", str(cm.exception))
        self.assertIn("--base-version", str(cm.exception))
        # new 不需要 _backup
        mark_changes.build("09_x", "new")
        self.assertTrue(out("09_x").exists())


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
        return out("09_x").read_text()

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
    """標示版放在 doc/review/<鍵>/：相對連結改寫成從那裡出發，解析回去要等於原本的目標。"""

    SRC = pathlib.Path("doc/contract/01_purpose.md")
    BASE = mark_changes.out_dir("01_purpose")

    def back(self, rewritten):
        """把改寫後的目標從 doc/review/<鍵>/ 解析回 repo 內路徑（錨點分開回傳）。"""
        file_part, _, anchor = rewritten.partition("#")
        return os.path.normpath(os.path.join(self.BASE.as_posix(), file_part)), anchor

    def link(self, text):
        got = mark_changes.rewrite_links(text, self.SRC, self.BASE)
        return got[got.index("](") + 2:got.rindex(")")]

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
        got = self.link("[03](03_output.md#結束碼)")
        self.assertEqual(got, "../../contract/03_output.md#結束碼")

    def test_external_and_anchor_unchanged(self):
        for text in ("[a](https://git-scm.com/)", "[b](http://x.org/a.md)",
                     "[c](mailto:a@b.c)", "[d](#4-永不靜默失敗)"):
            with self.subTest(text=text):
                self.assertEqual(mark_changes.rewrite_links(text, self.SRC, self.BASE), text)

    def test_code_untouched(self):
        text = "`[x](../../GLOSSARY.md)` 與 [y](../../GLOSSARY.md)"
        out = mark_changes.rewrite_links(text, self.SRC, self.BASE)
        self.assertTrue(out.startswith("`[x](../../GLOSSARY.md)`"))
        self.assertNotIn("[y](../../GLOSSARY.md)", out)
        block = "```\n[x](../../GLOSSARY.md)\n```"
        self.assertEqual(mark_changes.rewrite_links(block, self.SRC, self.BASE), block)

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
                copy = out("09_x", ".md").read_text()
                marked = out("09_x").read_text()
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
    """審閱頁旁的同名 CSV：跟 .md 放同一個送審資料夾，合併成一份標示版；CSV 部分依 code 逐欄標示。"""

    GREEN = '<mark style="background-color:#c8f0c8">'
    RED = '<mark style="background-color:#f8c8c8">'
    # 表頭照 check_messages.FIELDS：note、invariant、details 三欄已刪
    HEAD = "code,status,level,exit_code,disposition,situation,message,description,next_step\n"
    OLD = ("\ufeff" + HEAD
           + "VK0001,active,error,2,失敗,舊情境,Old message <repo>.,舊本文 <repo>,\n"
           "VK0002,active,warn,1,,情境,Unchanged.,不變,\n"
           "VK0003,active,error,2,失敗,要停用的情境,Retire this message.,要停用,\n")
    NEW = ("\ufeff" + HEAD
           + "VK0001,active,error,2,待處理,新情境,New message <repo>. Rerun <repo>.,新本文 <repo>,Rerun <repo>.\n"
           "VK0002,active,warn,1,,情境,Unchanged.,不變,\n"
           "VK0003,retired,,,,,,,\n"
           "VK0004,active,warn,1,,新增的情境,\"First line.\nSecond line.\",新增的本文,\n")

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/decisions/_backup").mkdir(parents=True)
        pathlib.Path("doc/contract/03_output.md").write_text("# 03\n\n規則\n")
        pathlib.Path("doc/contract/03_output.csv").write_text(self.NEW, encoding="utf-8")

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def backup(self, ext, text):
        pathlib.Path(f"doc/decisions/_backup/doc_contract_03_output.pre_r1{ext}").write_text(text, encoding="utf-8")

    def marked(self):
        return out("03_output").read_text()

    def test_outputs_in_one_folder(self):
        self.backup(".md", "# 03\n\n舊規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_output", "pre_r1")
        d = pathlib.Path("doc/review/03_output")
        self.assertEqual(sorted(p.name for p in d.iterdir()),
                         ["03_output.csv", "03_output.marked.md", "03_output.md"])
        # CSV 副本逐位元組照抄（BOM 保留）
        self.assertEqual((d / "03_output.csv").read_bytes(),
                         pathlib.Path("doc/contract/03_output.csv").read_bytes())
        text = self.marked()
        # md 部分照舊逐行標示，CSV 部分接在後面
        self.assertLess(text.index(self.GREEN + "規則</mark>"), text.index("## 03_output.csv 的逐碼差異"))

    def test_csv_path_is_same_as_page_name(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("doc/contract/03_output.csv", "pre_r1")
        self.assertTrue(out("03_output").exists())

    def test_per_code_per_field(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_output", "pre_r1")
        text = self.marked()
        lines = text.splitlines()
        # 改欄位：舊值紅、新值綠；沒改的欄不標；占位符照原樣看得到
        self.assertIn(f"- `disposition`：{self.RED}失敗</mark> → {self.GREEN}待處理</mark>", lines)
        self.assertIn(f"- `situation`：{self.RED}舊情境</mark> → {self.GREEN}新情境</mark>", lines)
        self.assertIn(f"- `message`：{self.RED}Old message &lt;repo&gt;.</mark> → "
                      f"{self.GREEN}New message &lt;repo&gt;. Rerun &lt;repo&gt;.</mark>", lines)
        self.assertIn(f"- `description`：{self.RED}舊本文 &lt;repo&gt;</mark> → "
                      f"{self.GREEN}新本文 &lt;repo&gt;</mark>", lines)
        self.assertIn(f"- `next_step`：{self.RED}（空）</mark> → {self.GREEN}Rerun &lt;repo&gt;.</mark>", lines)
        self.assertIn("- `status`：active", lines)
        self.assertIn("- `level`：error", lines)
        self.assertIn("- `exit_code`：2", lines)
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
        self.assertIn(f"- `message`：{self.GREEN}First line.<br>Second line.</mark>", lines[i:])
        self.assertIn(f"- `description`：{self.GREEN}新增的本文</mark>", lines[i:])
        # 標題不加標籤（錨點不變）
        for line in lines:
            if line.startswith("#"):
                self.assertNotIn("<", line)

    def test_removed_column(self):
        # 舊表頭多一欄 note：VK0001 的 note 有值、VK0002 的 note 是空的
        old_head = self.HEAD.rstrip("\n") + ",note\n"
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", "\ufeff" + old_head
                    + "VK0001,active,error,2,失敗,舊情境,Old message <repo>.,舊本文 <repo>,,舊值\n"
                    "VK0002,active,warn,1,,情境,Unchanged.,不變,,\n"
                    "VK0003,active,error,2,失敗,要停用的情境,Retire this message.,要停用,,\n")
        mark_changes.build("03_output", "pre_r1")
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
        self.backup(".csv", "\ufeff" + old_head
                    + "VK0001,active,error,2,失敗,舊情境,Old message <repo>.,舊本文 <repo>\n"
                    "VK0002,active,warn,1,,情境,Unchanged.,不變\n"
                    "VK0003,active,error,2,失敗,要停用的情境,Retire this message.,要停用\n")
        mark_changes.build("03_output", "pre_r1")
        lines = self.marked().splitlines()
        self.assertIn(f"- 表頭：{self.RED}{old_head.strip()}</mark> → {self.GREEN}{self.HEAD.strip()}</mark>", lines)
        self.assertIn(f"- `next_step`：{self.GREEN}（本欄新增）</mark>", lines)
        self.assertNotIn(f"- `next_step`：{self.RED}（本欄刪除）</mark>", lines)
        self.assertIn(
            f"- `next_step`：{self.GREEN}Rerun &lt;repo&gt;.</mark> {self.GREEN}（本欄新增）</mark>",
            lines,
        )
        self.assertIn("沒改動的代碼 1 個：VK0002。", lines)

    def test_removed_row(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD
                    + "VK0009,active,warn,1,,拿掉的情境,Remove this message.,拿掉,\n")
        mark_changes.build("03_output", "pre_r1")
        lines = self.marked().splitlines()
        i = lines.index("#### VK0009")
        self.assertEqual(lines[i + 1], self.RED + "（本列刪除）</mark>")
        self.assertIn(f"- `situation`：{self.RED}拿掉的情境</mark>", lines[i:])
        self.assertIn(f"- `message`：{self.RED}Remove this message.</mark>", lines[i:])
        self.assertIn(f"- `description`：{self.RED}拿掉</mark>", lines[i:])

    def test_md_backup_missing_means_md_unchanged(self):
        self.backup(".csv", self.OLD)
        mark_changes.build("03_output", "pre_r1")
        text = self.marked()
        self.assertIn("> 注意：沒有 doc/contract/03_output.md 的基準版 pre_r1：視為這一輪沒改", text)
        self.assertNotIn(self.GREEN + "規則</mark>", text)
        self.assertIn("#### VK0001", text)

    def test_csv_backup_missing_and_not_in_git_means_new(self):
        self.backup(".md", "# 03\n\n規則\n")
        mark_changes.build("03_output", "pre_r1")
        text = self.marked()
        self.assertIn("視為新建，整份標新增", text)
        for code in ("VK0001", "VK0002", "VK0003", "VK0004"):
            self.assertIn(f"#### {code}\n{self.GREEN}（本碼新增）</mark>", text)

    def test_both_backups_missing_fails(self):
        with self.assertRaises(SystemExit):
            mark_changes.build("03_output", "pre_r1")

    def test_rerun_keeps_same_names(self):
        self.backup(".md", "# 03\n\n規則\n")
        self.backup(".csv", self.OLD)
        mark_changes.build("03_output", "pre_r1")
        mark_changes.build("03_output", "pre_r1")
        names = sorted(p.name for p in pathlib.Path("doc/review/03_output").iterdir())
        self.assertEqual(names, ["03_output.csv", "03_output.marked.md", "03_output.md"])

    def test_csv_backup_path(self):
        self.backup(".csv", self.OLD)
        self.assertEqual(mark_changes.backup_path("03_output", "pre_r1", ".csv"),
                         pathlib.Path("doc/decisions/_backup/doc_contract_03_output.pre_r1.csv"))


class BaseVersionTest(unittest.TestCase):
    """基準取自 versions.json 記的送審 commit：git show <commit>:<正式檔>（CSV 也一樣）。"""

    GREEN = '<mark style="background-color:#c8f0c8">'
    RED = '<mark style="background-color:#f8c8c8">'
    PAGE = "# 03\n\n見 [名詞表](../../GLOSSARY.md#vk) 與 [04](04_interface.md)。\n\n不變的段落\n"
    CSV = ("\ufeffcode,status,level,exit_code,disposition,situation,message,description,next_step\n"
           "VK0001,active,error,2,失敗,情境,Message text.,本文,\n")

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        init_repo()
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/contract/03_output.md").write_text(self.PAGE)
        pathlib.Path("doc/contract/03_output.csv").write_text(self.CSV, encoding="utf-8")
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n\n[03](doc/contract/03_output.md)\n")
        self.v13 = commit_all("v13")
        write_versions({"03_output": [{"v": 13, "commit": self.v13, "replied": True}]}, review_zip=2)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def marked(self):
        return out("03_output").read_text()

    def change(self):
        pathlib.Path("doc/contract/03_output.md").write_text(self.PAGE.replace("不變的段落", "改過的段落"))
        pathlib.Path("doc/contract/03_output.csv").write_text(
            self.CSV.replace("Message text.", "New message text."), encoding="utf-8")

    def test_same_content_has_no_marks(self):
        # 正式檔與送審時相同：沒有紅綠，連結照新深度改寫
        ins, dele, _ = mark_changes.build_from_version("03_output", 13)
        self.assertEqual((ins, dele), (0, 0))
        text = self.marked()
        self.assertNotIn("<mark", text.split("-->", 1)[1])
        self.assertIn("../../../GLOSSARY.md#vk", text)
        self.assertIn(self.v13[:7], text)
        self.assertNotRegex(text, r"v1[34]")

    def test_finalized_unchanged_removes_review_folder_and_writes_nothing(self):
        # 已定案且正式檔仍與定案 commit 相同：不留送審資料。
        mark_changes.build_from_version("03_output", 13)
        self.assertTrue(out("03_output").exists())
        write_versions(
            {"03_output": [{"v": 13, "commit": self.v13, "replied": True}]},
            finalized={"03_output": {"v": 13, "commit": self.v13}},
        )
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            mark_changes.build_from_version("03_output")
        self.assertFalse(pathlib.Path("doc/review/03_output").exists())
        self.assertIn("已定案", stdout.getvalue())
        self.assertIn("刪除", stdout.getvalue())

    def test_finalized_changed_uses_finalized_commit_and_returns_to_review(self):
        # 即使後來又有 replied 版本，回到待審時仍以定案 commit 為基準。
        finalized = {"03_output": {"v": 13, "commit": self.v13}}
        self.change()
        v14 = commit_all("v14")
        pathlib.Path("doc/contract/03_output.md").write_text(
            self.PAGE.replace("不變的段落", "定案後再改的段落")
        )
        write_versions(
            {"03_output": [
                {"v": 13, "commit": self.v13, "replied": True},
                {"v": 14, "commit": v14, "replied": True},
            ]},
            finalized=finalized,
        )
        mark_changes.build_from_version("03_output")
        text = self.marked()
        self.assertIn(self.RED + "不變的段落</mark>", text)
        self.assertIn(self.GREEN + "定案後再改的段落</mark>", text)
        self.assertNotIn(self.RED + "改過的段落</mark>", text)
        self.assertIn("定案後又有改動，回到待審", text)
        self.assertIn(self.v13[:7], text)

    def test_only_later_changes_marked(self):
        self.change()
        ins, dele, _ = mark_changes.build_from_version("03_output", 13)
        text = self.marked()
        self.assertIn(self.GREEN + "改過的段落</mark>", text)
        self.assertIn(self.RED + "不變的段落</mark>", text)
        self.assertIn(self.RED + "Message text.</mark> → " + self.GREEN + "New message text.</mark>", text)
        self.assertNotIn(self.GREEN + "見 [名詞表]", text)
        self.assertEqual((ins, dele), (2, 2))

    def test_uses_commit_of_requested_version(self):
        # v14 送審在後面的 commit；指定 v13 時基準仍是 v13 的 commit
        self.change()
        v14 = commit_all("v14")
        write_versions({"03_output": [{"v": 13, "commit": self.v13, "replied": True},
                                        {"v": 14, "commit": v14, "replied": False}]}, 3)
        result = mark_changes.build_from_version("03_output", 13)
        self.assertEqual(result[:2], (2, 2))
        self.assertEqual(result[2], "送審 v13")
        self.assertEqual(mark_changes.build_from_version("03_output", 14)[:2], (0, 0))

    def test_default_base_is_last_replied(self):
        self.change()
        v14 = commit_all("v14")
        write_versions({"03_output": [{"v": 14, "commit": v14, "replied": True},
                                        {"v": 13, "commit": self.v13, "replied": True}]}, 3)
        result = mark_changes.build_from_version("03_output")
        self.assertEqual(result[:2], (0, 0))
        self.assertEqual(result[2], "最後一次回覆過的版本")

    def test_default_base_skips_unreplied(self):
        # v14 送出後維護者還沒回覆：基準仍是回覆過的 v13，v13 之後的改動照樣標紅綠
        self.change()
        v14 = commit_all("v14")
        write_versions({"03_output": [{"v": 13, "commit": self.v13, "replied": True},
                                        {"v": 14, "commit": v14, "replied": False}]}, 3)
        self.assertEqual(mark_changes.build_from_version("03_output")[:2], (2, 2))
        self.assertIn(self.GREEN + "改過的段落</mark>", self.marked())
        self.assertIn(self.v13[:7], self.marked())
        # 指定版號時不看 replied
        self.assertEqual(mark_changes.build_from_version("03_output", 14)[:2], (0, 0))

    def test_missing_replied_field_counts_as_unreplied(self):
        write_versions({"03_output": [{"v": 13, "commit": self.v13}]})
        mark_changes.build_from_version("03_output")
        self.assertIn("沒有維護者回覆過的版本", self.marked())

    def test_never_sent_is_all_new(self):
        write_versions({})
        ins, dele, _ = mark_changes.build_from_version("03_output")
        text = self.marked()
        self.assertGreater(ins, 0)
        self.assertEqual(dele, 0)
        self.assertIn("沒有維護者回覆過的版本", text)
        self.assertIn(self.GREEN + "不變的段落</mark>", text)
        self.assertIn(f"#### VK0001\n{self.GREEN}（本碼新增）</mark>", text)

    def test_no_replied_entry_is_all_new(self):
        # 送過但都還沒回覆：整份標新增
        write_versions({"03_output": [{"v": 13, "commit": self.v13, "replied": False}]})
        ins, dele, _ = mark_changes.build_from_version("03_output")
        text = self.marked()
        self.assertEqual(dele, 0)
        self.assertIn("沒有維護者回覆過的版本", text)
        self.assertIn(self.GREEN + "不變的段落</mark>", text)
        self.assertIn(f"#### VK0001\n{self.GREEN}（本碼新增）</mark>", text)

    def copy_commit(self):
        """把送審當時的正文副本（連結從副本目錄寫）與 CSV 副本放進 git，正式檔之後再改。"""
        d = pathlib.Path("doc/decisions/_marked")
        d.mkdir(parents=True)
        page = self.PAGE.replace("不變的段落", "副本裡的段落")
        (d / "03_output.v13.md").write_text(
            mark_changes.rewrite_links(page, pathlib.Path("doc/contract/03_output.md"), d))
        (d / "03_output.v13.csv").write_text(self.CSV.replace("Message text.", "Copy text."), encoding="utf-8")
        return commit_all("copies"), page

    def test_path_overrides_official(self):
        commit, page = self.copy_commit()
        write_versions({"03_output": [{"v": 13, "commit": commit, "replied": True,
                                         "path": "doc/decisions/_marked/03_output.v13.md"}]})
        mark_changes.build_from_version("03_output")
        text = self.marked()
        # 基準是副本：副本的段落標紅；副本的連結改寫回正式檔位置，連結行不算改動
        self.assertIn(self.RED + "副本裡的段落</mark>", text)
        self.assertIn(self.GREEN + "不變的段落</mark>", text)
        self.assertNotIn(self.GREEN + "見 [名詞表]", text)
        self.assertNotIn(self.RED + "見 [名詞表]", text)
        # 沒有 csv_path：CSV 基準取正式檔路徑，跟現在一樣
        self.assertNotIn("Copy text.", text)
        self.assertNotIn("#### VK0001", text)

    def test_csv_path_overrides_official(self):
        commit, _ = self.copy_commit()
        write_versions({"03_output": [{"v": 13, "commit": commit, "replied": True,
                                         "csv_path": "doc/decisions/_marked/03_output.v13.csv"}]})
        mark_changes.build_from_version("03_output")
        text = self.marked()
        self.assertIn(self.RED + "Copy text.</mark> → " + self.GREEN + "Message text.</mark>", text)
        # 沒有 path：.md 基準取正式檔，沒有改動
        self.assertNotIn("副本裡的段落", text)

    def test_raw_links_copy_not_rewritten(self):
        d = pathlib.Path("doc/decisions/_marked")
        d.mkdir(parents=True)
        (d / "03_output.v13.md").write_text(self.PAGE)  # 連結照正式檔位置寫
        commit = commit_all("raw copy")
        entry = {"v": 13, "commit": commit, "replied": True, "path": "doc/decisions/_marked/03_output.v13.md"}
        write_versions({"03_output": [dict(entry, raw_links=True)]})
        self.assertEqual(mark_changes.build_from_version("03_output")[:2], (0, 0))
        write_versions({"03_output": [entry]})
        self.assertNotEqual(mark_changes.build_from_version("03_output")[:2], (0, 0))

    def test_renamed_page_uses_old_path_and_old_links_follow(self):
        # 正式檔改過名（RENAMED，#137）：紀錄的 commit 裡只有改名前的檔，基準照改名前的路徑取；
        # 基準裡連到改名前路徑的連結換成新路徑，只因改名而不同的行不標成改動
        old_md, old_csv = pathlib.Path("doc/contract/03_messages.md"), pathlib.Path("doc/contract/03_messages.csv")
        new_md, new_csv = pathlib.Path("doc/contract/03_output.md"), pathlib.Path("doc/contract/03_output.csv")
        new_md.rename(old_md)
        new_csv.rename(old_csv)
        p04 = pathlib.Path("doc/contract/04_interface.md")
        p04.write_text("# 04\n\n見 [03](03_messages.md#結束碼) 與 [訊息](03_messages.csv) `VK0001`。\n")
        before = commit_all("before rename")
        old_md.rename(new_md)
        old_csv.rename(new_csv)
        p04.write_text("# 04\n\n見 [03](03_output.md#結束碼) 與 [訊息](03_output.csv) `VK0001`。\n")
        write_versions({"03_output": [{"v": 13, "commit": before, "replied": True}],
                        "04_interface": [{"v": 20, "commit": before, "replied": True}]})
        self.assertEqual(mark_changes.build_from_version("03_output")[:2], (0, 0))
        self.assertNotIn("#### VK0001", self.marked())
        self.assertEqual(mark_changes.build_from_version("04_interface")[:2], (0, 0))
        self.assertIn("../../contract/03_output.md#結束碼", out("04_interface").read_text())

    def test_missing_path_in_commit_fails(self):
        write_versions({"03_output": [{"v": 13, "commit": self.v13, "replied": True,
                                         "path": "doc/decisions/_marked/nope.md"}]})
        with self.assertRaises(SystemExit) as cm:
            mark_changes.build_from_version("03_output")
        self.assertIn("nope.md", str(cm.exception))
        self.assertFalse(out("03_output").exists())

    def test_csv_missing_in_commit_is_new(self):
        pathlib.Path("doc/contract/03_output.csv").unlink()
        no_csv = commit_all("no csv")
        pathlib.Path("doc/contract/03_output.csv").write_text(self.CSV, encoding="utf-8")
        write_versions({"03_output": [{"v": 13, "commit": no_csv}]})
        mark_changes.build_from_version("03_output", 13)
        text = self.marked()
        self.assertIn("視為新建，整份標新增", text)
        self.assertIn(f"#### VK0001\n{self.GREEN}（本碼新增）</mark>", text)

    def test_does_not_write_versions(self):
        before = pathlib.Path("doc/review/versions.json").read_text()
        mark_changes.build_from_version("03_output", 13)
        self.assertEqual(pathlib.Path("doc/review/versions.json").read_text(), before)

    def test_missing_version_fails(self):
        with self.assertRaises(SystemExit) as cm:
            mark_changes.build_from_version("03_output", 12)
        self.assertIn("v12", str(cm.exception))
        self.assertFalse(out("03_output").exists())

    def test_root_file_by_key(self):
        write_versions({"GLOSSARY": [{"v": 6, "commit": self.v13}]})
        result = mark_changes.build_from_version("GLOSSARY", 6)
        self.assertEqual(result[:2], (0, 0))
        self.assertEqual(result[2], "送審 v6")
        self.assertTrue(out("GLOSSARY").exists())

    def test_root_readme_key_wins_over_contract_readme(self):
        # doc/contract/README.md 也存在時，鍵 README 仍是根目錄的 README.md
        pathlib.Path("README.md").write_text("# 根目錄\n")
        pathlib.Path("doc/contract/README.md").write_text("# 審閱頁\n")
        self.assertEqual(mark_changes.resolve_base_name("README"), "README.md")
        commit = commit_all("readme")
        write_versions({"README": [{"v": 6, "commit": commit, "replied": True}]})
        mark_changes.build_from_version("README")
        self.assertIn("/README.md -->", out("README").read_text())
        self.assertEqual(out("README", ".md").read_text(), "# 根目錄\n")

    def run_cli(self, *args):
        argv = sys.argv
        sys.argv = ["mark_changes.py", *args]
        try:
            mark_changes.main()
        finally:
            sys.argv = argv

    def test_cli_parses_pairs(self):
        self.run_cli("--base-version", "03_output=13")
        self.assertTrue(out("03_output").exists())

    def test_cli_names_only_uses_last_replied(self):
        self.change()
        self.run_cli("03_output", "GLOSSARY.md")
        self.assertIn(self.GREEN + "改過的段落</mark>", self.marked())
        # GLOSSARY 從沒送審過：整份標新增
        self.assertIn("沒有維護者回覆過的版本", out("GLOSSARY").read_text())

    def test_cli_first_arg_not_a_file_is_suffix(self):
        # 第一個參數對不到檔就當成後綴；本機沒有 _backup/ 時清楚報錯
        with self.assertRaises(SystemExit) as cm:
            self.run_cli("pre_r1", "03_output")
        self.assertIn("doc/decisions/_backup", str(cm.exception))

    def test_cli_rejects_bad_pair(self):
        with self.assertRaises(SystemExit):
            self.run_cli("--base-version", "03_output")

    def test_cli_missing_one_builds_none(self):
        with self.assertRaises(SystemExit):
            self.run_cli("--base-version", "03_output=13", "GLOSSARY=6")
        self.assertFalse(out("03_output").exists())


if __name__ == "__main__":
    unittest.main()
