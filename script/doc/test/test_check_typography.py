"""check_typography.py 的排版規則（正反例與排除範圍）：跑法 `python3 -m unittest discover -s script/doc/test`。

規則 (1)：括號內容全是 ASCII 用半形括號，半形括號與中文之間空一格；括號內有中文維持全形。
規則 (2)：中文與英文字母或阿拉伯數字相鄰要空一格；全形標點與英數之間不加空白。
  行內程式碼與前後的中文相鄰也要空一格；與全形標點相鄰不加空白；連結的 [ 與 ](…) 不算字元。
排除：行內程式碼的內容、程式碼區塊、URL、Markdown 連結目標、HTML 標籤、CSV 的固定欄。

以黑箱方式跑：把 script/doc/*.py 複製進暫存目錄的 script/doc/，在暫存目錄當 repo 根目錄執行，
不依賴腳本內部的函式名稱；腳本以 cwd 或自身位置找 repo 根目錄都一樣會對到暫存目錄。
"""
import csv
import io
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent.parent
FIELDS = [
    "code", "status", "level", "exit_code", "disposition", "situation", "message", "description", "next_step",
]
CSV_REL = "doc/contract/03_messages.csv"


def row(**kw):
    return [kw.get(f, "") for f in FIELDS]


def good_rows():
    return [
        row(code="VK0001", status="active", level="error", exit_code="2", disposition="待續",
            situation="要確認但不能互動", message="Run again with -y: <original command with -y>",
            description="請加上 -y 重新執行。", next_step="<original command with -y>"),
        row(code="VK0002", status="active", level="warn", exit_code="1", situation="第 2 次重試",
            message="Retry the VK recipe.", description="VK recipe 失敗，請重試。"),
    ]


def encode(rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(FIELDS)
    w.writerows(rows)
    return ("﻿" + buf.getvalue()).encode("utf-8")


class Base(unittest.TestCase):
    """暫存 repo：README.md、GLOSSARY.md、doc/contract/01_purpose.md、03_messages.csv，初始全乾淨。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        (self.root / "script/doc").mkdir(parents=True)
        for p in SCRIPT_DIR.glob("*.py"):
            shutil.copy(p, self.root / "script/doc" / p.name)
        (self.root / "doc/contract").mkdir(parents=True)
        self.write("README.md", "# VK\n\nVK 的 recipe 說明。\n")
        self.write("GLOSSARY.md", "# 名詞\n\n用 VK 管理 recipe。\n")
        self.write("doc/contract/01_purpose.md", "# 01 目的與承諾\n\n第 12 條成立。\n")
        self.write_csv(good_rows())

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, body):
        (self.root / rel).write_text(body, encoding="utf-8")

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def write_csv(self, rows):
        (self.root / CSV_REL).write_bytes(encode(rows))

    def run_tool(self, *args):
        p = subprocess.run(
            [sys.executable, "script/doc/check_typography.py", *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )
        return p.returncode, p.stdout + p.stderr

    def assert_ok(self):
        code, out = self.run_tool()
        self.assertEqual(code, 0, out)

    def assert_fail(self, *where):
        """where 是 (檔, 行號)；行號為 None 時只要求檔名出現在報告裡。"""
        code, out = self.run_tool()
        self.assertEqual(code, 1, out)
        for rel, line in where:
            pat = re.escape(rel) + (f":{line}:" if line is not None else "")
            self.assertRegex(out, pat, out)
        return out

    def assert_fix(self, rel, before, after):
        """寫入 before，check 要失敗；--fix 後內容恰好等於 after，再 check 要過。"""
        self.write(rel, before)
        self.assertEqual(self.run_tool()[0], 1)
        self.run_tool("--fix")
        self.assertEqual(self.read(rel), after)
        self.assert_ok()


class CleanTest(Base):
    def test_clean_repo_passes(self):
        self.assert_ok()


class ParenTest(Base):
    """規則 (1)。"""

    def test_fullwidth_ascii_paren_fails(self):
        self.write("README.md", "# VK\n\n檢查（test）之後再跑。\n")
        self.assert_fail(("README.md", 3))

    def test_fullwidth_ascii_paren_fix(self):
        self.assert_fix("README.md", "# VK\n\n檢查（test）之後再跑。\n", "# VK\n\n檢查 (test) 之後再跑。\n")

    def test_fullwidth_digits_and_symbols_fix(self):
        # 數字與符號也算 ASCII；後面緊接全形標點不加空白
        self.assert_fix("README.md", "# VK\n\n見第 1 項（v1.2-rc）。\n", "# VK\n\n見第 1 項 (v1.2-rc)。\n")

    def test_halfwidth_paren_without_space_fails(self):
        self.write("README.md", "# VK\n\n檢查(test)之後再跑。\n")
        self.assert_fail(("README.md", 3))

    def test_halfwidth_paren_without_space_fix(self):
        self.assert_fix("README.md", "# VK\n\n檢查(test)之後再跑。\n", "# VK\n\n檢查 (test) 之後再跑。\n")

    def test_halfwidth_paren_spaced_passes(self):
        self.write("README.md", "# VK\n\n檢查 (test) 之後再跑，(test)。\n")
        self.assert_ok()

    def test_fullwidth_paren_with_chinese_passes(self):
        self.write("README.md", "# VK\n\n只跑一次（例如 VK0001 的情況）。\n")
        self.assert_ok()

    def test_heading_is_checked(self):
        self.write("doc/contract/01_purpose.md", "# 01 目的與承諾\n\n## 檢查（test）\n")
        self.assert_fail(("doc/contract/01_purpose.md", 3))


class SpacingTest(Base):
    """規則 (2)。"""

    def test_chinese_letter_adjacent_fails(self):
        self.write("README.md", "# VK\n\n這是VK的recipe。\n")
        self.assert_fail(("README.md", 3))

    def test_chinese_letter_adjacent_fix(self):
        self.assert_fix("README.md", "# VK\n\n這是VK的recipe。\n", "# VK\n\n這是 VK 的 recipe。\n")

    def test_chinese_digit_adjacent_fix(self):
        self.assert_fix("doc/contract/01_purpose.md", "# 01\n\n第12條成立。\n", "# 01\n\n第 12 條成立。\n")

    def test_glossary_is_scanned(self):
        self.write("GLOSSARY.md", "# 名詞\n\n用VK管理 recipe。\n")
        self.assert_fail(("GLOSSARY.md", 3))

    def test_fullwidth_punct_no_space_passes(self):
        self.write("README.md", "# VK\n\n先跑，VK。再看「recipe」：12、34；（例如 A）\n")
        self.assert_ok()

    def test_space_after_fullwidth_punct_not_added(self):
        # 修正只補中文與英數之間的空白，不在全形標點旁加空白
        self.assert_fix("README.md", "# VK\n\n先跑，VK的recipe。\n", "# VK\n\n先跑，VK 的 recipe。\n")

    def test_fix_touches_only_rule_chars(self):
        # 同一檔裡其他地方（空行、全形括號內的中文、行尾）一個字都不動
        before = "# VK\n\n\n第12條（見下）\n\n- 項目 VK 的 recipe\n"
        after = "# VK\n\n\n第 12 條（見下）\n\n- 項目 VK 的 recipe\n"
        self.assert_fix("README.md", before, after)

    def test_every_violation_line_reported(self):
        self.write("README.md", "# VK\n\n第1條\n\n正常的 VK。\n\n第2條\n")
        self.assert_fail(("README.md", 3), ("README.md", 7))


class InlineCodeSpacingTest(Base):
    """規則 (2) 的行內程式碼邊界：反引號包住的整段當一個單位，內容仍不查。"""

    def test_code_then_chinese_fails(self):
        self.write("README.md", "# VK\n\n以`0`結束。\n")
        self.assert_fail(("README.md", 3))

    def test_code_then_chinese_fix(self):
        self.assert_fix("README.md", "# VK\n\n以`0`結束。\n", "# VK\n\n以 `0` 結束。\n")

    def test_chinese_then_code_fix(self):
        self.assert_fix("README.md", "# VK\n\n印`VK0024`。\n", "# VK\n\n印 `VK0024`。\n")

    def test_code_content_not_touched_by_fix(self):
        # 只補兩側的空白，反引號內的中英混排一個字都不動
        self.assert_fix("README.md", "# VK\n\n執行`a的b（c）`之後\n", "# VK\n\n執行 `a的b（c）` 之後\n")

    def test_double_backtick_code_fix(self):
        self.assert_fix("README.md", "# VK\n\n以``a`b``結束\n", "# VK\n\n以 ``a`b`` 結束\n")

    def test_spaced_code_passes(self):
        self.write("README.md", "# VK\n\n以 `0` 結束，印 `VK0024` 後停。\n")
        self.assert_ok()

    def test_fullwidth_punct_no_space_passes(self):
        # 與全形標點相鄰不加空白；--fix 也不動
        body = "# VK\n\n`0`，結束碼「`0`」：`VK0024`、`x`；\n"
        self.write("README.md", body)
        self.assert_ok()
        self.run_tool("--fix")
        self.assertEqual(self.read("README.md"), body)

    def test_link_markers_are_transparent_fix(self):
        # 隔著 [ 看前面的中文、隔著 ](…) 看後面的中文；空白補在連結記號外側
        self.assert_fix("README.md", "# VK\n\n見[`x`](a.md)的說明\n", "# VK\n\n見 [`x`](a.md) 的說明\n")

    def test_unclosed_backtick_is_not_code(self):
        # 沒有結尾的反引號不是行內程式碼，兩側不補空白
        body = "# VK\n\n單獨的`反引號\n"
        self.write("README.md", body)
        self.assert_ok()
        self.run_tool("--fix")
        self.assertEqual(self.read("README.md"), body)


class ExcludeTest(Base):
    """排除範圍：不誤報、--fix 也不動。"""

    def assert_untouched(self, rel, body):
        self.write(rel, body)
        self.assert_ok()
        self.run_tool("--fix")
        self.assertEqual(self.read(rel), body)

    def test_inline_code(self):
        self.assert_untouched("README.md", "# VK\n\n執行 `just vendor_kit的recipe（test）` 即可。\n")

    def test_code_block(self):
        self.assert_untouched("README.md", "# VK\n\n範例：\n\n```sh\necho VK的recipe（test）\n```\n")

    def test_url(self):
        self.assert_untouched("README.md", "# VK\n\n網址 https://example.com/路徑abc/第12頁 在此。\n")

    def test_link_target(self):
        # 連結文字照查（這裡是乾淨的），括號裡的路徑與錨點不查
        self.assert_untouched("README.md", "# VK\n\n見[審閱頁說明](doc/設定abc.md#檢查test第12條)。\n")

    def test_link_text_is_checked(self):
        self.write("README.md", "# VK\n\n見[VK的說明](doc/a.md)。\n")
        self.assert_fail(("README.md", 3))

    def test_html_tag(self):
        # 標籤本身（含屬性值）不查；標籤外的文字照查（這裡是乾淨的）
        self.assert_untouched("README.md", "# VK\n\n這是<ins title=\"名詞abc第12條\">名詞</ins>說明，<br>換行。\n")

    def test_csv_fixed_columns(self):
        rows = good_rows()
        rows[1][FIELDS.index("status")] = "啟用active"
        rows[1][FIELDS.index("level")] = "等級warn"
        rows[1][FIELDS.index("exit_code")] = "結束碼1"
        rows[1][FIELDS.index("code")] = "代碼VK0002"
        self.write_csv(rows)
        before = (self.root / CSV_REL).read_bytes()
        self.assert_ok()
        self.run_tool("--fix")
        self.assertEqual((self.root / CSV_REL).read_bytes(), before)


class CsvTest(Base):
    """CSV 的中文文字欄 situation、description，以及英文 message、next_step。"""

    def test_chinese_text_columns_scanned(self):
        for field in ["situation", "description"]:
            with self.subTest(field=field):
                rows = good_rows()
                rows[1][FIELDS.index(field)] = "無法寫入VK設定"
                self.write_csv(rows)
                self.assert_fail((CSV_REL, None))

    def test_english_message_and_next_step_pass(self):
        rows = good_rows()
        rows[1][FIELDS.index("message")] = "Run command2 (test): <next_step>."
        rows[1][FIELDS.index("next_step")] = "<next_step>"
        self.write_csv(rows)
        self.assert_ok()

    def test_csv_fix_keeps_format(self):
        rows = good_rows()
        rows[1][FIELDS.index("description")] = "無法寫入VK設定（test），\"引號\"與\n第2行"
        rows[1][FIELDS.index("situation")] = "第12條"
        self.write_csv(rows)
        self.assertEqual(self.run_tool()[0], 1)
        self.run_tool("--fix")
        data = (self.root / CSV_REL).read_bytes()
        self.assertTrue(data.startswith("﻿".encode()))
        self.assertFalse(data.startswith("﻿﻿".encode()))
        self.assertNotIn(b"\r", data)
        want = good_rows()
        want[1][FIELDS.index("description")] = "無法寫入 VK 設定 (test)，\"引號\"與\n第 2 行"
        want[1][FIELDS.index("situation")] = "第 12 條"
        self.assertEqual(data, encode(want))
        self.assert_ok()


if __name__ == "__main__":
    unittest.main()
