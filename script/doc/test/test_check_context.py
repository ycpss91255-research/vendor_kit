"""check_context.py 的名詞行解析：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import contextlib
import io
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_context  # noqa: E402


def run(text: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "GLOSSARY.md"
        path.write_text(text, encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = check_context.main(path)
    return rc, out.getvalue()


class TermRegexTest(unittest.TestCase):
    def test_both_paren_styles_and_bare(self):
        for line, name in [
            ("**VK** (vendor_kit)：", "VK"),
            ("**導入**（consume）：", "導入"),
            ("**導入** (consume):", "導入"),
            ("**名詞**：", "名詞"),
        ]:
            m = check_context.TERM.match(line)
            self.assertIsNotNone(m, line)
            self.assertEqual(m.group(1), name)

    def test_half_width_without_space_is_not_term(self):
        self.assertIsNone(check_context.TERM.match("**VK**(vendor_kit)："))


class MainTest(unittest.TestCase):
    def test_counts_every_style(self):
        rc, out = run(
            "# G\n\n## Language\n\n### 群\n\n"
            "**甲** (alpha)：\n定義甲。\n\n"
            "**乙**（beta）：\n定義乙。\n\n"
            "**丙**：\n定義丙。\n"
        )
        self.assertEqual(rc, 0, out)
        self.assertIn("名詞 3", out)

    def test_unrecognized_term_line_fails(self):
        # 名詞行寫法變了但 regex 沒跟上，不能靜默少算
        rc, out = run("# G\n\n## Language\n\n### 群\n\n**甲**(alpha)：\n定義甲。\n")
        self.assertEqual(rc, 1)
        self.assertIn("格式不認得", out)


class HtmlTest(unittest.TestCase):
    HEAD = "# G\n\n## Language\n\n### 群\n\n**甲** (alpha)：\n"

    def test_ins_fails(self):
        # r144 起名詞改連到 GLOSSARY 分群，<ins> 不再放行
        rc, out = run(self.HEAD + "定義<ins>甲</ins>。\n")
        self.assertEqual(rc, 1)
        self.assertIn("ins", out)

    def test_inline_code_and_fence_not_html(self):
        rc, out = run(self.HEAD + "定義 `<ins>` 與 `<repo>`。\n\n```\n<ins>甲</ins>\n```\n")
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
