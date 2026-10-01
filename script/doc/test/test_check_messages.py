"""check_messages.py 的規則（每條一正一反）：跑法 `python3 -m unittest discover -s script/doc/test`。"""
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
        row(code="VK0001", status="active", level="error", exit_code="2", disposition="待處理",
            situation="要確認但不能互動", message="Run again with -y: <original command with -y>",
            description="請加上 -y 重新執行。", next_step="<original command with -y>"),
        row(code="VK0002", status="active", level="error", exit_code="2", disposition="失敗",
            situation="建不出執行紀錄", message="Could not write <path>. Try again.",
            description="無法寫入執行紀錄，請重試。"),
        row(code="VK0003", status="active", level="warn", exit_code="1", situation="合併衝突",
            message="Resolve the merge conflicts left in <file>: git status",
            description="檔案留下合併衝突，請檢視後解決。", next_step="git status"),
        row(code="VK0004", status="retired", situation="舊的情況"),
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
        self.write("03_output.md", "# 03\n\n## 訊息表怎麼讀\n")
        self.write_csv(good_rows())

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def write(self, name, body):
        pathlib.Path("doc/contract", name).write_text(body)

    def write_csv(self, rows, **kw):
        m.CSV_PATH.write_bytes(encode(rows, **kw))

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
        m.CSV_PATH.unlink()
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
        m.CSV_PATH.write_bytes("﻿".encode() + encode(good_rows()))
        self.assert_fail("BOM 只准出現一次")

    def test_crlf(self):
        self.write_csv(good_rows(), newline="\r\n")
        self.assert_fail("只准 LF")

    def test_trailing_newline(self):
        p = m.CSV_PATH
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
        self.assert_fail(f"有 {len(HEADER) - 1} 欄")

    def test_strict_parse(self):
        p = m.CSV_PATH
        malformed = ["VK0005", "active", "warn", "1", "", "x", '"a"b', "x", ""]
        p.write_bytes(encode(good_rows()) + (",".join(malformed) + "\n").encode())
        self.assert_fail("CSV 解析失敗")

    def test_quoted_newline_parses(self):
        self.edit(1, message="First line.\nSecond line.")
        self.assert_ok()

    def test_surrounding_space(self):
        self.edit(1, situation="前後有空白 ")
        self.assert_fail("VK0002:situation: 頭尾不准有空白")

    def test_formula_start(self):
        for bad in ("=1+1", "+x", "-x", "@x"):
            with self.subTest(bad=bad):
                self.edit(1, situation=bad)
                self.assert_fail("VK0002:situation: 不准以 =")


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
        rows[3][HEADER.index("next_step")] = "git status"
        self.write_csv(rows)
        self.assert_fail("VK0004:message: retired 列只留", "VK0004:next_step: retired 列只留")

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

    def test_description_required(self):
        self.edit(1, description="")
        self.assert_fail("VK0002:description: active 列必填")

    def test_message_must_be_english(self):
        self.edit(1, message="無法寫入 <path>. Try again.")
        self.assert_fail("VK0002:message:", "中文字元")

    def test_exit_code_matches_level(self):
        for level, exit_code in (("warn", "1"), ("error", "2"), ("fatal", "3")):
            with self.subTest(level=level):
                disposition = "" if level == "warn" else "失敗"
                self.edit(1, level=level, exit_code=exit_code, disposition=disposition)
                self.assert_ok()

    def test_wrong_exit_code(self):
        self.edit(1, exit_code="3")
        self.assert_fail("VK0002:exit_code: error 必須是 2")

    def test_exit_code_required(self):
        self.edit(1, exit_code="")
        self.assert_fail("VK0002:exit_code:")

    def test_disposition_values(self):
        self.edit(1, disposition="requires_action")
        self.assert_fail("VK0002:disposition: 只准")
        self.edit(1, disposition="—")
        self.assert_fail("VK0002:disposition: 只准")

    def test_empty_disposition_on_non_usage_error_fails(self):
        self.edit(1, disposition="")
        self.assert_fail("VK0002:disposition: 只有 warn 與用法錯誤可留空")

    def test_empty_disposition_on_usage_error_ok(self):
        self.edit(1, disposition="", situation="用法錯誤：缺少必要參數")
        self.assert_ok()

    def test_empty_disposition_on_warn_ok(self):
        self.edit(2, disposition="")
        self.assert_ok()

    def test_warn_disposition_empty(self):
        self.edit(2, disposition="失敗", next_step="")
        self.assert_fail("VK0003:disposition: warn 一律空白")

    def test_action_required_requires_next_step(self):
        self.edit(0, next_step="")
        self.assert_fail("VK0001:next_step: 待處理必有下一步")

    def test_failure_has_no_next_step(self):
        self.edit(1, next_step="請重試")
        self.assert_fail("VK0002:next_step: 失敗的 next_step 必須空白")

    def test_next_step_verbatim_in_message(self):
        self.edit(2, next_step="git status -s")
        self.assert_fail("VK0003:next_step: 要逐字出現在 message 裡")

    def test_message_sentence_start(self):
        self.edit(1, message="could not write <path>. Try again.")
        self.assert_fail("VK0002:message: 句首要大寫")

        self.edit(1, message="justice was not done.")
        self.assert_fail("VK0002:message: 句首要大寫")

    def test_message_sentence_end(self):
        self.edit(1, message="Could not write <path>. Try again")
        self.assert_fail("VK0002:message: 結尾要是句點")

    def test_message_start_and_end_exceptions(self):
        cases = (
            ("<file> already exists.", ""),
            ("just 1.33.0 or later is required.", ""),
            ("Run it now: <command>", "<command>"),
            ("Retry with: just vendor_kit upgrade <repo>", ""),
            ("Retry with: just vendor_kit add <repo>@v1.2.3", ""),
        )
        for message, next_step in cases:
            with self.subTest(message=message):
                disposition = "待處理" if next_step else "失敗"
                self.edit(1, message=message, next_step=next_step, disposition=disposition)
                self.assert_ok()

    def test_html(self):
        for bad in ("<ins>導入</ins>", "第一行<br>", '<a href="x">', "<!-- x -->"):
            with self.subTest(bad=bad):
                self.edit(1, situation=bad)
                self.assert_fail("VK0002:situation: 不准 HTML")

    def test_placeholder_is_not_html(self):
        self.edit(1, situation="<P> 與 <repo> 與 <加上 -y 的原指令> 是占位符")
        self.assert_ok()

    def test_markdown(self):
        for bad in ("`x`", "**x**", "[x](y)", "~~x~~"):
            with self.subTest(bad=bad):
                self.edit(1, situation=bad)
                self.assert_fail("VK0002:situation: 不准 Markdown")

    def test_angle_pairs(self):
        for bad in ("<repo", "repo>", "<a<b>>"):
            with self.subTest(bad=bad):
                self.edit(1, situation=bad)
                self.assert_fail("VK0002:situation:")


class RefTest(Base):
    def test_good_links(self):
        self.write("04_interface.md", "# 04\n\n見[訊息](03_output.csv) `VK0002`、[`VK0001`](03_output.csv)。\n")
        pathlib.Path("doc/adr/0001-x.md").write_text("歷史：曾用 [`VK0004`](../contract/03_output.csv)。\n")
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
        self.write("04_interface.md", "# 04\n\n[`VK0002`](03_output.csv#L3)\n")
        self.assert_fail("連 CSV 不帶 #")

    def test_code_link_to_md_goes_to_csv(self):
        for target in ("03_output.md#vk0002", "03_output.md#訊息", "03_output.md"):
            with self.subTest(target=target):
                self.write("04_interface.md", f"# 04\n\n[`VK0002`]({target})\n")
                self.assert_fail("改連 03_output.csv")

    def test_01_02_must_not_link_csv(self):
        self.write("01_purpose.md", "# 01\n\n[訊息表](03_output.csv)\n")
        self.assert_fail("01、02 不准連 CSV")


class DiagnosticTest(Base):
    def test_level_must_match_csv(self):
        self.write("04_interface.md", "vendor_kit: warn[VK0002]: Could not write /tmp/log. Try again.\n")
        self.assert_fail("VK0002 的 level 是 warn，CSV 是 error")

    def test_body_must_match_message_first_line(self):
        self.write("04_interface.md", "vendor_kit: error[VK0002]: A different message.\n")
        self.assert_fail("VK0002 的本文不符合 CSV message 第一行")

    def test_placeholder_matches_actual_value(self):
        self.write("04_interface.md", "vendor_kit: error[VK0002]: Could not write /tmp/run.jsonl. Try again.\n")
        self.assert_ok()

    def test_retired_and_unknown_codes_are_skipped_by_rule_9(self):
        self.write(
            "04_interface.md",
            "vendor_kit: error[VK0004]: Historical example.\n"
            "vendor_kit: fatal[VK9999]: Unknown example.\n",
        )
        by_code = {r[HEADER.index("code")]: dict(zip(HEADER, r)) for r in good_rows()}
        errors = []
        m.check_diagnostics(by_code, errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
