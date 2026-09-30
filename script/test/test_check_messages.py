"""check_messages.py 的規則（每條一正一反）：跑法 `python3 -m unittest discover -s script/test`。"""
import contextlib
import csv
import io
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_messages as m  # noqa: E402

HEADER = m.FIELDS


def row(**kw):
    return [kw.get(f, "") for f in HEADER]


def good_rows():
    return [
        row(code="VK0001", status="active", level="error", disposition="需人處理", situation="要確認但不能互動",
            message="請加上 -y 重新執行：<加上 -y 的原指令>", next_step="<加上 -y 的原指令>", invariant="1;3",
            details="03_messages.md#vk0001"),
        row(code="VK0002", status="active", level="error", disposition="失敗", situation="建不出執行紀錄",
            message="無法寫入 <path>。請重試。", note="在任何副作用之前結束"),
        row(code="VK0003", status="active", level="warn", situation="合併衝突",
            message="<file> 留下合併衝突，請檢視後解決：git status", next_step="git status"),
        row(code="VK0004", status="retired", situation="舊的情況", note="改用 VK0003"),
    ]


def encode(rows, header=HEADER, bom=True, newline="\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    w.writerows(rows)
    return (("﻿" if bom else "") + buf.getvalue()).encode("utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        pathlib.Path("doc/contract").mkdir(parents=True)
        pathlib.Path("doc/adr").mkdir(parents=True)
        pathlib.Path("README.md").write_text("# VK\n")
        pathlib.Path("GLOSSARY.md").write_text("# 名詞\n")
        self.write("02_invariants.md", "# 02\n\n## 1. 甲\n\n## 2. 乙\n\n## 3. 丙\n")
        self.write("03_messages.md", "# 03\n\n## 目錄\n\n## 長說明\n\n### VK0001\n\n說明。\n")
        self.write_csv(good_rows())

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def write(self, name, body):
        pathlib.Path("doc/contract", name).write_text(body)

    def write_csv(self, rows, **kw):
        pathlib.Path("doc/contract/03_messages.csv").write_bytes(encode(rows, **kw))

    def edit(self, i, **kw):
        rows = good_rows()
        for k, v in kw.items():
            rows[i][HEADER.index(k)] = v
        self.write_csv(rows)

    def run_main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = m.main()
        return code, out.getvalue()

    def assert_ok(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def assert_fail(self, *wants):
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        for want in wants:
            self.assertIn(want, out)


class MissingTest(Base):
    def test_missing_csv_skips(self):
        pathlib.Path("doc/contract/03_messages.csv").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("還不存在，跳過", out)

    def test_good_passes(self):
        self.assert_ok()


class FormatTest(Base):
    def test_no_bom(self):
        self.write_csv(good_rows(), bom=False)
        self.assert_fail("BOM")

    def test_double_bom(self):
        pathlib.Path("doc/contract/03_messages.csv").write_bytes("﻿".encode() + encode(good_rows()))
        self.assert_fail("BOM 只准出現一次")

    def test_crlf(self):
        self.write_csv(good_rows(), newline="\r\n")
        self.assert_fail("只准 LF")

    def test_trailing_newline(self):
        p = pathlib.Path("doc/contract/03_messages.csv")
        p.write_bytes(encode(good_rows()) + b"\n")
        self.assert_fail("檔尾要恰好一個換行")
        p.write_bytes(encode(good_rows()).rstrip(b"\n"))
        self.assert_fail("檔尾要恰好一個換行")

    def test_header(self):
        self.write_csv(good_rows(), header=HEADER[:-1] + ["detail"])
        self.assert_fail("表頭要逐字等於")

    def test_column_count(self):
        rows = good_rows()
        rows[1] = rows[1][:-1]
        self.write_csv(rows)
        self.assert_fail("有 9 欄")

    def test_strict_parse(self):
        p = pathlib.Path("doc/contract/03_messages.csv")
        p.write_bytes(encode(good_rows()) + 'VK0005,active,warn,,"a"b,x,,,,\n'.encode())
        self.assert_fail("CSV 解析失敗")

    def test_quoted_newline_parses(self):
        self.edit(1, message="第一行\n第二行")
        self.assert_ok()

    def test_surrounding_space(self):
        self.edit(1, note="前後有空白 ")
        self.assert_fail("VK0002:note: 頭尾不准有空白")

    def test_formula_start(self):
        for bad in ("=1+1", "+x", "-x", "@x"):
            with self.subTest(bad=bad):
                self.edit(1, note=bad)
                self.assert_fail("VK0002:note: 不准以 =")


class CodeTest(Base):
    def test_format(self):
        self.edit(1, code="VK002")
        self.assert_fail("code: 格式要是 VK 加四位數字")

    def test_duplicate(self):
        self.edit(1, code="VK0001")
        self.assert_fail("代碼重複")

    def test_gap_or_order(self):
        self.edit(1, code="VK0009")
        self.assert_fail("第 2 列要是 VK0002")

    def test_status(self):
        self.edit(1, status="reserved")
        self.assert_fail("VK0002:status: 只准 active、retired")

    def test_retired_must_be_empty(self):
        rows = good_rows()
        rows[3][HEADER.index("message")] = "還留著"
        rows[3][HEADER.index("details")] = "03_messages.md#vk0004"
        self.write_csv(rows)
        self.assert_fail("VK0004:message: retired 列只留", "VK0004:details: retired 列只留")

    def test_situation_required(self):
        self.edit(3, situation="")
        self.assert_fail("VK0004:situation: 必填")


class FieldTest(Base):
    def test_level(self):
        self.edit(1, level="info")
        self.assert_fail("VK0002:level: active 列只准 warn、error、fatal")

    def test_message_required(self):
        self.edit(1, message="")
        self.assert_fail("VK0002:message: active 列必填")

    def test_disposition_values(self):
        self.edit(1, disposition="requires_action")
        self.assert_fail("VK0002:disposition: 只准")
        self.edit(1, disposition="—")
        self.assert_fail("VK0002:disposition: 只准")

    def test_empty_disposition_on_error_ok(self):
        self.edit(1, disposition="")
        self.assert_ok()

    def test_warn_disposition_empty(self):
        self.edit(2, disposition="失敗", next_step="")
        self.assert_fail("VK0003:disposition: warn 一律空白")

    def test_needs_action_requires_next_step(self):
        self.edit(0, next_step="")
        self.assert_fail("VK0001:next_step: 需人處理必有下一步")

    def test_failure_has_no_next_step(self):
        self.edit(1, next_step="請重試")
        self.assert_fail("VK0002:next_step: 失敗的 next_step 必須空白")

    def test_next_step_verbatim_in_message(self):
        self.edit(2, next_step="git status -s")
        self.assert_fail("VK0003:next_step: 要逐字出現在 message 裡")

    def test_html(self):
        for bad in ("<ins>導入</ins>", "第一行<br>", '<a href="x">', "<!-- x -->"):
            with self.subTest(bad=bad):
                self.edit(1, note=bad)
                self.assert_fail("VK0002:note: 不准 HTML")

    def test_placeholder_is_not_html(self):
        self.edit(1, note="<P> 與 <repo> 與 <加上 -y 的原指令> 是占位符")
        self.assert_ok()

    def test_markdown(self):
        for bad in ("`x`", "**x**", "[x](y)", "~~x~~"):
            with self.subTest(bad=bad):
                self.edit(1, note=bad)
                self.assert_fail("VK0002:note: 不准 Markdown")

    def test_angle_pairs(self):
        for bad in ("<repo", "repo>", "<a<b>>"):
            with self.subTest(bad=bad):
                self.edit(1, note=bad)
                self.assert_fail("VK0002:note:")

    def test_invariant(self):
        self.edit(1, invariant="2")
        self.assert_ok()
        for bad, want in (("x", "要是 02 的條號"), ("3;1", "條號要遞增"), ("1;1", "條號要遞增"), ("13", "02 沒有第 [13] 條"),
                          ("1,2", "要是 02 的條號")):
            with self.subTest(bad=bad):
                self.edit(1, invariant=bad)
                self.assert_fail(f"VK0002:invariant: {want}")


class DetailsTest(Base):
    def test_details_must_equal_own_code(self):
        self.edit(0, details="03_messages.md#vk0002")
        self.assert_fail("VK0001:details: 只准空白或 03_messages.md#vk0001")

    def test_details_needs_section(self):
        self.write("03_messages.md", "# 03\n\n## 目錄\n")
        self.assert_fail("沒有 `### VK0001` 節")

    def test_section_needs_details(self):
        self.write("03_messages.md", "# 03\n\n## 目錄\n\n### VK0001\n\n### VK0002\n")
        self.assert_fail("`### VK0002` 節在 CSV 裡沒有對應的 details")

    def test_section_heading_only_code(self):
        self.write("03_messages.md", "# 03\n\n## 目錄\n\n### VK0001 參數重組\n")
        self.assert_fail("標題只寫代碼")


class RefTest(Base):
    def test_good_links(self):
        self.write("04_interface.md", "# 04\n\n見 [`VK0002`](03_messages.csv)、[`VK0001`](03_messages.md#vk0001)。\n")
        pathlib.Path("doc/adr/0001-x.md").write_text("歷史：曾用 [`VK0004`](../contract/03_messages.csv)。\n")
        self.assert_ok()

    def test_unknown_code(self):
        self.write("04_interface.md", "# 04\n\n`VK0099`\n")
        self.assert_fail("04_interface.md:3: VK0099 不在")
        pathlib.Path("doc/contract/04_interface.md").unlink()
        pathlib.Path("doc/adr/0001-x.md").write_text("VK0099\n")
        self.assert_fail("0001-x.md:1: VK0099 不在")

    def test_retired_only_in_adr(self):
        pathlib.Path("GLOSSARY.md").write_text("VK0004\n")
        self.assert_fail("GLOSSARY.md:1: VK0004 已停用")

    def test_csv_link_without_fragment(self):
        self.write("04_interface.md", "# 04\n\n[`VK0002`](03_messages.csv#L3)\n")
        self.assert_fail("連 CSV 不帶 #")

    def test_md_link_needs_code_anchor(self):
        self.write("04_interface.md", "# 04\n\n[`VK0002`](03_messages.md#訊息)\n")
        self.assert_fail("改連 03_messages.csv")

    def test_md_link_anchor_matches_text(self):
        self.write("04_interface.md", "# 04\n\n[`VK0002`](03_messages.md#vk0001)\n")
        self.assert_fail("不是同一個代碼")

    def test_md_link_needs_details(self):
        self.write("04_interface.md", "# 04\n\n[`VK0002`](03_messages.md#vk0002)\n")
        self.assert_fail("VK0002 的 details 是空的或不同")

    def test_01_02_must_not_link_csv(self):
        self.write("01_purpose.md", "# 01\n\n[訊息表](03_messages.csv)\n")
        self.assert_fail("01、02 不准連 CSV")


if __name__ == "__main__":
    unittest.main()
