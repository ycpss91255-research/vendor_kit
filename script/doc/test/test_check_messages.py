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
        row(**{"code": "VK0001", "status": "active", "level": "error", "exit_code": "2", "disposition": "pending",
               "situation.en": "Confirmation needed but not interactive",
               "message.en": "Run again with -y: <original command with -y>",
               "situation.zh-TW": "要確認但不能互動",
               "message.zh-TW": "請加上 -y 重新執行：<original command with -y>"}),
        row(**{"code": "VK0002", "status": "active", "level": "error", "exit_code": "2", "disposition": "failed",
               "situation.en": "Cannot create the run log",
               "message.en": "Could not write <path>. Try again.",
               "situation.zh-TW": "建不出執行紀錄",
               "message.zh-TW": "無法寫入 <path>，請重試。"}),
        row(**{"code": "VK0003", "status": "active", "level": "warn", "exit_code": "1",
               "situation.en": "Merge conflicts",
               "message.en": "Resolve the merge conflicts left in <file>: git status",
               "situation.zh-TW": "合併衝突",
               "message.zh-TW": "<file> 留下合併衝突，請檢視後解決：git status"}),
        row(**{"code": "VK0004", "status": "retired", "situation.en": "Old situation", "situation.zh-TW": "舊的情況"}),
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
            rows[i][HEADER.index(k.replace("__", ".").replace("_TW", "-TW"))] = v
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

    def test_header_unknown_column(self):
        self.write_csv(good_rows(), header=HEADER[:-1] + ["detail"])
        self.assert_fail("未知欄名：detail")

    def test_header_old_columns_rejected(self):
        old = ["code", "status", "level", "exit_code", "disposition", "situation", "message", "description", "next_step"]
        self.write_csv(good_rows(), header=old)
        self.assert_fail("未知欄名：situation", "未知欄名：description", "未知欄名：next_step")

    def test_header_must_start_with_base(self):
        header = ["status", "code"] + HEADER[2:]
        self.write_csv(good_rows(), header=header)
        self.assert_fail("表頭要以 code,status,level,exit_code,disposition 開頭")

    def test_header_missing_language(self):
        rows = [r[:7] for r in good_rows()]
        self.write_csv(rows, header=HEADER[:7])
        self.assert_fail("表頭缺少語言組：zh-TW")
        rows = [r[:5] + r[7:] for r in good_rows()]
        self.write_csv(rows, header=HEADER[:5] + HEADER[7:])
        self.assert_fail("表頭缺少語言組：en")

    def test_header_group_must_pair(self):
        header = HEADER[:5] + ["situation.en", "situation.zh-TW", "message.en", "message.zh-TW"]
        self.write_csv(good_rows(), header=header)
        self.assert_fail("不成組")

    def test_columns_read_by_name(self):
        """語言組換順序（zh-TW 在前）也照欄名讀；以後加語言就在右邊接一組。"""
        order = HEADER[:5] + HEADER[7:] + HEADER[5:7]
        rows = [[r[HEADER.index(h)] for h in order] for r in good_rows()]
        self.write_csv(rows, header=order)
        self.assert_ok()
        header = HEADER + ["situation.ja", "message.ja"]
        rows = good_rows()
        for r, (sit, msg) in zip(rows, (
            ("確認", "再実行：<original command with -y>"),
            ("記録", "<path> に書けません。"),
            ("競合", "<file> に競合：git status"),
            ("旧", ""),
        )):
            r += [sit, msg]
        self.write_csv(rows, header=header)
        self.assert_ok()

    def test_column_count(self):
        rows = good_rows()
        rows[1] = rows[1][:-1]
        self.write_csv(rows)
        self.assert_fail(f"有 {len(HEADER) - 1} 欄")

    def test_strict_parse(self):
        p = m.CSV_PATH
        malformed = ["VK0005", "active", "warn", "1", "", "x", '"a"b', "x", "y"]
        p.write_bytes(encode(good_rows()) + (",".join(malformed) + "\n").encode())
        self.assert_fail("CSV 解析失敗")

    def test_quoted_newline_parses(self):
        self.edit(1, message__en="First line.\nSecond line.", message__zh_TW="第一行。\n第二行。")
        self.assert_ok()

    def test_surrounding_space(self):
        self.edit(1, situation__en="前後有空白 ")
        self.assert_fail("VK0002:situation.en: 頭尾不准有空白")

    def test_formula_start(self):
        for bad in ("=1+1", "+x", "-x", "@x"):
            with self.subTest(bad=bad):
                self.edit(1, situation__en=bad)
                self.assert_fail("VK0002:situation.en: 不准以 =")


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
        rows[3][HEADER.index("message.en")] = "Still here."
        rows[3][HEADER.index("message.zh-TW")] = "還留著"
        rows[3][HEADER.index("level")] = "warn"
        self.write_csv(rows)
        self.assert_fail(
            "VK0004:message.en: retired 列只留", "VK0004:message.zh-TW: retired 列只留", "VK0004:level: retired 列只留",
        )

    def test_retired_keeps_all_situations(self):
        self.assert_ok()

    def test_situation_required(self):
        self.edit(3, situation__en="")
        self.assert_fail("VK0004:situation.en: 必填")
        self.edit(3, situation__zh_TW="")
        self.assert_fail("VK0004:situation.zh-TW: 必填")
        self.edit(1, situation__zh_TW="")
        self.assert_fail("VK0002:situation.zh-TW: 必填")


class FieldTest(Base):
    def test_level(self):
        self.edit(1, level="info")
        self.assert_fail("VK0002:level: active 列只准 warn、error、fatal")

    def test_message_required(self):
        self.edit(1, message__en="")
        self.assert_fail("VK0002:message.en: active 列必填")
        self.edit(1, message__zh_TW="")
        self.assert_fail("VK0002:message.zh-TW: active 列必填")

    def test_english_columns_must_not_contain_chinese(self):
        self.edit(1, message__en="無法寫入 <path>. Try again.")
        self.assert_fail("VK0002:message.en: 不准含中文字元")
        self.edit(1, situation__en="建不出執行紀錄")
        self.assert_fail("VK0002:situation.en: 不准含中文字元")

    def test_other_language_columns_may_contain_chinese(self):
        self.edit(1, situation__zh_TW="中文", message__zh_TW="中文 <path>。")
        self.assert_ok()

    def test_placeholders_must_match_en(self):
        self.edit(1, message__zh_TW="無法寫入檔案，請重試。")
        self.assert_fail("VK0002:message.zh-TW: <…> 占位符要與 message.en 相同")
        self.edit(1, message__zh_TW="無法寫入 <path> 與 <other>，請重試。")
        self.assert_fail("VK0002:message.zh-TW: <…> 占位符要與 message.en 相同")

    def test_placeholders_may_reorder_or_repeat(self):
        self.edit(1, message__en="Could not write <path> in <dir>. Try again.",
                  message__zh_TW="在 <dir> 寫不了 <path>（<path>），請重試。")
        self.assert_ok()

    def test_newlines_must_match_en(self):
        self.edit(1, message__en="First line.\nSecond line.", message__zh_TW="第一行。")
        self.assert_fail("VK0002:message.zh-TW: 換行數要與 message.en 相同")

    def test_exit_code_matches_level(self):
        for level, exit_code in (("warn", "1"), ("error", "2"), ("fatal", "3")):
            with self.subTest(level=level):
                disposition = "" if level == "warn" else "failed"
                self.edit(1, level=level, exit_code=exit_code, disposition=disposition)
                self.assert_ok()

    def test_wrong_exit_code(self):
        self.edit(1, exit_code="3")
        self.assert_fail("VK0002:exit_code: error 必須是 2")

    def test_exit_code_required(self):
        self.edit(1, exit_code="")
        self.assert_fail("VK0002:exit_code:")

    def test_disposition_values(self):
        for bad in ("requires_action", "—", "待處理", "失敗", "Pending"):
            with self.subTest(bad=bad):
                self.edit(1, disposition=bad)
                self.assert_fail("VK0002:disposition: 只准 pending、failed 或空白")

    def test_empty_disposition_on_non_usage_error_fails(self):
        self.edit(1, disposition="")
        self.assert_fail("VK0002:disposition: 只有 warn 與用法錯誤")

    def test_empty_disposition_on_usage_error_ok(self):
        self.edit(1, disposition="", situation__en="Usage error: missing required argument")
        self.assert_ok()

    def test_usage_error_is_read_from_situation_en(self):
        self.edit(1, disposition="", situation__en="usage error: missing argument")
        self.assert_fail("VK0002:disposition: 只有 warn 與用法錯誤")
        self.edit(1, disposition="", situation__zh_TW="用法錯誤：缺少必要參數")
        self.assert_fail("VK0002:disposition: 只有 warn 與用法錯誤")

    def test_empty_disposition_on_warn_ok(self):
        self.edit(2, disposition="")
        self.assert_ok()

    def test_warn_disposition_empty(self):
        self.edit(2, disposition="failed")
        self.assert_fail("VK0003:disposition: warn 一律空白")

    def test_pending_must_end_with_command(self):
        for message in ("Run again with -y.", "Run again with -y: now", "Run: ls <dir>"):
            with self.subTest(message=message):
                self.edit(0, message__en=message, message__zh_TW="請重新執行。")
                self.assert_fail("VK0001:message.en: pending 列要以指令結尾")

    def test_pending_command_forms(self):
        for message in (
            "Run: <original_command>",
            "Run: just vendor_kit add <repo>",
            "Review them: git status",
            "Run: sh <script>",
            "Run: cd <install_dir>",
            "Download: <download_url>\nInstall: <install_command>",
        ):
            with self.subTest(message=message):
                command = message.splitlines()[-1].rsplit(": ", 1)[1]
                zh = " ".join(m.PLACEHOLDER.findall(message)) + "\n" * message.count("\n") + "：" + command
                self.edit(0, message__en=message, message__zh_TW=zh)
                self.assert_ok()

    def test_failed_has_no_command_requirement(self):
        self.edit(1, message__en="Could not write <path>.", message__zh_TW="無法寫入 <path>。")
        self.assert_ok()

    def test_other_language_must_contain_ending_command(self):
        self.edit(0, message__zh_TW="請加上 -y 重新執行 <original command with -y>")
        self.assert_ok()
        self.edit(2, message__zh_TW="<file> 留下合併衝突，請檢視後解決。")
        self.assert_fail("VK0003:message.zh-TW: 要逐字包含 message.en 的結尾指令：git status")
        self.edit(2, message__zh_TW="<file> 留下合併衝突：git status -s")
        self.assert_ok()  # 包含即可
        self.edit(2, message__zh_TW="<file> 留下合併衝突：git  status")
        self.assert_fail("VK0003:message.zh-TW: 要逐字包含")

    def test_message_sentence_start(self):
        self.edit(1, message__en="could not write <path>. Try again.")
        self.assert_fail("VK0002:message.en: 句首要大寫")

        self.edit(1, message__en="justice was not done <path>.")
        self.assert_fail("VK0002:message.en: 句首要大寫")

    def test_message_sentence_end(self):
        self.edit(1, message__en="Could not write <path>. Try again")
        self.assert_fail("VK0002:message.en: 結尾要是句點")

    def test_sentence_rules_only_apply_to_en(self):
        self.edit(1, message__zh_TW="無法寫入 <path>，請重試")
        self.assert_ok()

    def test_message_start_and_end_exceptions(self):
        cases = (
            ("<file> already exists.", "failed"),
            ("just 1.33.0 or later is required.", "failed"),
            ("Run it now: <command>", "pending"),
            ("Retry with: just vendor_kit upgrade <repo>", "failed"),
            ("Retry with: just vendor_kit add <repo>@v1.2.3", "failed"),
            ("Retry later, or run just vendor_kit sync", "failed"),
        )
        for message, disposition in cases:
            with self.subTest(message=message):
                command = m.ending_command(message) or ""
                zh = " ".join(sorted(set(m.PLACEHOLDER.findall(message)))) + "：" + command
                self.edit(1, message__en=message, message__zh_TW=zh, disposition=disposition)
                self.assert_ok()

    def test_html(self):
        for bad in ("<ins>導入</ins>", "第一行<br>", '<a href="x">', "<!-- x -->"):
            with self.subTest(bad=bad):
                self.edit(1, situation__en=bad)
                self.assert_fail("VK0002:situation.en: 不准 HTML")

    def test_placeholder_is_not_html(self):
        self.edit(1, situation__zh_TW="<P> 與 <repo> 與 <加上 -y 的原指令> 是占位符")
        self.assert_ok()

    def test_markdown(self):
        for bad in ("`x`", "**x**", "[x](y)", "~~x~~"):
            with self.subTest(bad=bad):
                self.edit(1, situation__en=bad)
                self.assert_fail("VK0002:situation.en: 不准 Markdown")

    def test_angle_pairs(self):
        for bad in ("<repo", "repo>", "<a<b>>"):
            with self.subTest(bad=bad):
                self.edit(1, situation__en=bad)
                self.assert_fail("VK0002:situation.en:")


class RefTest(Base):
    def test_good_links(self):
        self.write("04_interface.md", "# 04\n\n見[訊息](reason_codes.csv) `VK0002`、[`VK0001`](reason_codes.csv)。\n")
        pathlib.Path("doc/adr/0001-x.md").write_text("歷史：曾用 [`VK0004`](../contract/reason_codes.csv)。\n")
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
        self.write("04_interface.md", "# 04\n\n[`VK0002`](reason_codes.csv#L3)\n")
        self.assert_fail("連 CSV 不帶 #")

    def test_code_link_to_md_goes_to_csv(self):
        for target in ("03_output.md#vk0002", "03_output.md#訊息", "03_output.md"):
            with self.subTest(target=target):
                self.write("04_interface.md", f"# 04\n\n[`VK0002`]({target})\n")
                self.assert_fail("改連 reason_codes.csv")

    def test_01_02_must_not_link_csv(self):
        self.write("01_purpose.md", "# 01\n\n[訊息表](reason_codes.csv)\n")
        self.assert_fail("01、02 不准連 CSV")


class DiagnosticTest(Base):
    def test_level_must_match_csv(self):
        self.write("04_interface.md", "vendor_kit: warn[VK0002]: Could not write /tmp/log. Try again.\n")
        self.assert_fail("VK0002 的 level 是 warn，CSV 是 error")

    def test_body_must_match_message_first_line(self):
        self.write("04_interface.md", "vendor_kit: error[VK0002]: A different message.\n")
        self.assert_fail("VK0002 的本文不符合 CSV message.en 第一行")

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
