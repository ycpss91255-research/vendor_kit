"""script/git/check_commit_msg.py 的測試。

跑法：python3 -m unittest discover -s script/git/test
"""
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_commit_msg as ccm  # noqa: E402


def errors(text, title_only=False):
    return ccm.check_message(text, title_only=title_only)[0]


def assert_error_contains(tc, text, needle, title_only=False):
    errs = errors(text, title_only)
    tc.assertTrue(any(needle in e for e in errs), f"找不到含「{needle}」的錯誤：{errs}")


class TestValid(unittest.TestCase):
    def test_title_only_forms(self):
        for title in (
            "feat(cli): 新增 --output 參數",
            "fix: 修正路徑解析錯誤",
            "docs(contract): 補上承諾對象的定義",
            "ci(tools): 新增 commit 訊息檢查與 commit-msg hook",
            "perf(engine): 減少重複讀檔",
            "build: 調整建置腳本",
            "chore: 清掉過時的設定",
            "refactor(bootstrap): 拆開初始化步驟",
            "test(hooks): 補上 guard 的反例",
        ):
            with self.subTest(title=title):
                self.assertEqual(errors(title), [])

    def test_all_types_and_scopes_accepted(self):
        for t in ccm.TYPES:
            for s in ccm.SCOPES:
                self.assertEqual(errors(f"{t}({s}): 調整設定"), [])

    def test_full_message_with_body_and_footer(self):
        msg = (
            "feat(cli)!: 更改預設設定檔路徑\n"
            "\n"
            "舊路徑跟其他工具衝突，改放到 XDG 目錄。\n"
            "\n"
            "BREAKING CHANGE: 設定檔改放 ~/.config/vk，舊路徑不再讀取\n"
            "Refs: #110, #97\n"
            "Closes #12\n"
            "Doc-Edit: r125\n"
        )
        self.assertEqual(errors(msg), [])

    def test_footer_only_paragraph(self):
        self.assertEqual(errors("ci(tools): 新增檢查\n\nRefs: #110\n"), [])

    def test_doc_edit_light(self):
        self.assertEqual(errors("docs(contract): 調整用詞\n\nDoc-Edit: r126 light\n"), [])

    def test_cross_repo_refs(self):
        self.assertEqual(errors("docs: 補連結\n\nRefs: ycpss91255-research/vendor_kit#1\n"), [])

    def test_body_line_starting_with_fix_word_is_prose(self):
        self.assertEqual(errors("fix: 修正\n\nfix the parser so it works\n\nRefs: #1\n"), [])


class TestTitleErrors(unittest.TestCase):
    def test_missing_type(self):
        assert_error_contains(self, "hook：inline workflow 不再跳確認", "全形")
        assert_error_contains(self, "修正路徑解析", "缺少 `type: ` 前綴")

    def test_unknown_type(self):
        assert_error_contains(self, "feature: 新增功能", "type `feature` 不在清單內")

    def test_uppercase_type(self):
        assert_error_contains(self, "Fix: 修正錯誤", "type 要小寫")

    def test_unknown_scope(self):
        assert_error_contains(self, "docs(圖面): 調整", "scope `圖面` 不在清單內")
        assert_error_contains(self, "docs(r125): 調整", "不在清單內")

    def test_empty_scope(self):
        assert_error_contains(self, "docs(): 調整", "括號是空的")

    def test_fullwidth_colon(self):
        assert_error_contains(self, "docs(contract)：調整", "全形")

    def test_missing_space(self):
        assert_error_contains(self, "docs:調整", "一個半形空格")

    def test_double_space(self):
        assert_error_contains(self, "docs:  調整", "一個半形空格")

    def test_empty_description(self):
        assert_error_contains(self, "docs: ", "缺少描述")

    def test_trailing_punct(self):
        for title in ("docs: 調整用詞。", "docs: fix typo.", "docs: 調整！", "docs: 調整？", "docs: 調整，"):
            with self.subTest(title=title):
                assert_error_contains(self, title, "句尾不加標點")

    def test_leading_space(self):
        assert_error_contains(self, " docs: 調整", "前後不能有空白")

    def test_empty_message(self):
        assert_error_contains(self, "\n\n", "訊息是空的")


class TestWidth(unittest.TestCase):
    def test_display_width(self):
        self.assertEqual(ccm.display_width("abc"), 3)
        self.assertEqual(ccm.display_width("中文"), 4)
        self.assertEqual(ccm.display_width("中a"), 3)
        self.assertEqual(ccm.display_width("："), 2)  # 全形冒號是 F／W
        self.assertEqual(ccm.display_width("ｱ"), 1)  # 半形片假名是 H

    def test_exactly_max_ok(self):
        title = "docs: " + "中" * 33  # 6 + 66 = 72
        self.assertEqual(ccm.display_width(title), 72)
        self.assertEqual(errors(title), [])

    def test_over_max(self):
        title = "docs: " + "中" * 33 + "a"  # 73
        assert_error_contains(self, title, "超過上限 72 欄")

    def test_chars_under_max_but_width_over(self):
        title = "docs: " + "中" * 40  # 46 字元、86 欄
        self.assertLess(len(title), 72)
        assert_error_contains(self, title, "超過上限")

    def test_soft_limit_is_note_only(self):
        title = "docs: " + "中" * 25  # 56 欄
        errs, notes = ccm.check_message(title)
        self.assertEqual(errs, [])
        self.assertTrue(any("建議" in n for n in notes))


class TestBodyAndFooter(unittest.TestCase):
    def test_blank_line_after_title(self):
        assert_error_contains(self, "docs: 調整\n內文緊貼標題\n", "要空一行")

    def test_refs_without_colon(self):
        assert_error_contains(self, "docs: 調整\n\nRefs #110\n", "`Refs: #N`")

    def test_ref_singular(self):
        assert_error_contains(self, "docs: 調整\n\nRef: #110\n", "`Refs: #N`")

    def test_closes_with_colon(self):
        assert_error_contains(self, "docs: 調整\n\nCloses: #110\n", "`Closes #N`")

    def test_fixes_keyword(self):
        assert_error_contains(self, "docs: 調整\n\nFixes #110\n", "`Closes #N`")

    def test_lowercase_closes(self):
        assert_error_contains(self, "docs: 調整\n\ncloses #110\n", "`Closes #N`")

    def test_breaking_change_bad_form(self):
        assert_error_contains(self, "feat!: 調整\n\nBreaking change: 改路徑\n", "BREAKING CHANGE")
        assert_error_contains(self, "feat!: 調整\n\nBREAKING-CHANGE: 改路徑\n", "BREAKING CHANGE")

    def test_bang_requires_breaking_footer(self):
        assert_error_contains(self, "feat(cli)!: 更改預設路徑", "footer 也要寫 `BREAKING CHANGE")

    def test_breaking_footer_requires_bang(self):
        assert_error_contains(self, "feat(cli): 更改預設路徑\n\nBREAKING CHANGE: 舊路徑不讀\n", "也要加 `!`")

    def test_doc_edit_bad_forms(self):
        for ln in ("Doc-Edit: 125", "Doc-Edit: r1", "doc-edit: r125", "Doc-Edit: r125 heavy"):
            with self.subTest(ln=ln):
                assert_error_contains(self, f"docs: 調整\n\n{ln}\n", "`Doc-Edit: rNN`")

    def test_footer_not_in_last_paragraph(self):
        msg = "docs: 調整\n\nRefs: #110\n\n這段是內文，放在 footer 後面\n"
        assert_error_contains(self, msg, "footer 要放在最後一段")

    def test_claude_attribution_blocked(self):
        for ln in (
            "Co-Authored-By: Claude <noreply@anthropic.com>",
            "https://claude.ai/code/session_abc",
            "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ):
            with self.subTest(ln=ln):
                assert_error_contains(self, f"docs: 調整\n\n{ln}\n", "Claude 署名")

    def test_human_coauthor_ok(self):
        self.assertEqual(errors("docs: 調整\n\nCo-authored-by: cyc <a@b.c>\n"), [])


class TestExemptions(unittest.TestCase):
    def test_revert(self):
        self.assertEqual(errors('Revert "docs: 調整用詞"\n\nThis reverts commit abc.\n'), [])

    def test_merge_defaults(self):
        for title in (
            "Merge pull request #61 from ycpss91255-research/fix/ins-underline",
            "Merge branch 'feature/x'",
            "Merge branch 'feature/x' into dev",
            "Merge remote-tracking branch 'origin/feature/x'",
        ):
            with self.subTest(title=title):
                self.assertEqual(errors(title + "\n\n任何內文\nRefs #1\n"), [])

    def test_merge_main_into_branch_rejected(self):
        for title in (
            "Merge branch 'main' into ci/commit-format",
            "Merge remote-tracking branch 'origin/main' into ci/commit-format",
            "Merge branch 'main' of github.com:ycpss91255-research/vendor_kit into x",
        ):
            with self.subTest(title=title):
                assert_error_contains(self, title, "rebase")

    def test_revert_not_exempt_if_malformed(self):
        assert_error_contains(self, "Revert docs 調整", "缺少 `type: ` 前綴")


class TestTitleOnly(unittest.TestCase):
    def test_pr_title_ok(self):
        self.assertEqual(errors("ci(tools): commit 訊息格式檢查（#110）", title_only=True), [])

    def test_pr_title_bang_without_footer_ok(self):
        # PR 標題沒有 footer，BREAKING CHANGE 寫在 commit 裡，所以只查標題本身
        self.assertEqual(errors("feat(cli)!: 更改預設路徑", title_only=True), [])

    def test_pr_title_multiline(self):
        assert_error_contains(self, "docs: 調整\n第二行", "只能有一行", title_only=True)


class TestStripComments(unittest.TestCase):
    def test_strips_comment_lines_and_scissors(self):
        raw = (
            "docs: 調整\n"
            "# Please enter the commit message\n"
            "\n"
            "Refs: #1\n"
            "# ------------------------ >8 ------------------------\n"
            "diff --git a/x b/x\n"
        )
        self.assertEqual(ccm.strip_comments(raw), "docs: 調整\n\nRefs: #1")


class TestCli(unittest.TestCase):
    def run_main(self, argv, stdin=""):
        out, err = io.StringIO(), io.StringIO()
        old = sys.stdin
        sys.stdin = io.StringIO(stdin)
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = ccm.main(argv)
        finally:
            sys.stdin = old
        return code, out.getvalue(), err.getvalue()

    def test_file_mode(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("docs: 調整\n# 註解\n")
        try:
            self.assertEqual(self.run_main([f.name])[0], 0)
        finally:
            os.unlink(f.name)

    def test_stdin_bad(self):
        code, _, err = self.run_main(["-"], stdin="壞標題\n")
        self.assertEqual(code, 1)
        self.assertIn("格式不合", err)

    def test_title_mode(self):
        self.assertEqual(self.run_main(["--title", "-"], stdin="fix(cli): 修正\n")[0], 0)


class TestRange(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        self.cwd = os.getcwd()
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
        self.env = {**os.environ, **env}
        self.git("init", "-q", "-b", "main")
        self.commit("chore: 初始化")
        self.base = self.git("rev-parse", "HEAD").strip()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], env=self.env, capture_output=True,
                              text=True, check=True).stdout

    def commit(self, msg):
        self.git("commit", "-q", "--allow-empty", "--no-verify", "-m", msg)

    def run_range(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = ccm.main(["--range", f"{self.base}..HEAD"])
        return code, out.getvalue()

    def test_all_good(self):
        self.commit("feat(cli): 新增指令")
        self.commit("docs: 補說明\n\nRefs: #110")
        code, out = self.run_range()
        self.assertEqual(code, 0, out)
        self.assertIn("檢查 2 個 commit，0 個不合格", out)

    def test_bad_commit_reported(self):
        self.commit("feat(cli): 新增指令")
        self.commit("待討論佇列：補一題")
        code, out = self.run_range()
        self.assertEqual(code, 1)
        self.assertIn("待討論佇列：補一題", out)
        self.assertIn("1 個不合格", out)

    def test_merge_commits(self):
        self.git("checkout", "-q", "-b", "side")
        self.commit("fix: 側分支修正")
        self.git("checkout", "-q", "main")
        self.commit("docs: 主線改動")
        self.git("checkout", "-q", "-b", "feature", self.base)
        self.commit("feat: 功能")
        # 一般的 merge commit 豁免
        self.git("merge", "-q", "--no-ff", "--no-verify", "-m", "Merge branch 'side' into feature", "side")
        code, out = self.run_range()
        self.assertEqual(code, 0, out)
        # 把 main 併進來要擋，提示改用 rebase
        self.git("merge", "-q", "--no-ff", "--no-verify", "-m", "Merge branch 'main' into feature", "main")
        code, out = self.run_range()
        self.assertEqual(code, 1)
        self.assertIn("rebase", out)

    def test_bad_range(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(ccm.main(["--range", "nope..HEAD"]), 2)


class TestBannedFromHook(unittest.TestCase):
    """擋署名的 pattern 直接取自 .claude/hooks/attribution_guard.py，不另抄一份。"""

    def test_same_pattern_as_hook(self):
        self.assertEqual(ccm.ATTRIBUTION_HOOK.parts[-3:], (".claude", "hooks", "attribution_guard.py"))
        self.assertTrue(ccm.ATTRIBUTION_HOOK.is_file())
        hook_banned = ccm.load_banned()
        self.assertEqual(ccm.BANNED_RE.pattern, hook_banned.pattern)
        self.assertEqual(ccm.BANNED_RE.flags, hook_banned.flags)

    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ccm.HookLoadError) as cm:
                ccm.load_banned(Path(d) / "nope.py")
            self.assertIn("找不到 hook 檔", str(cm.exception))

    def test_missing_banned_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "attribution_guard.py"
            p.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(ccm.HookLoadError) as cm:
                ccm.load_banned(p)
            self.assertIn("缺少 BANNED", str(cm.exception))

    def test_broken_hook_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "attribution_guard.py"
            p.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
            with self.assertRaises(ccm.HookLoadError) as cm:
                ccm.load_banned(p)
            self.assertIn("載入 hook 檔失敗", str(cm.exception))

    def test_main_scopes_present(self):
        for s in ("workflow", "hooks", "drawio", "lint", "doc", "review", "diagram", "agents", "tools", "repo", "github", "git"):
            with self.subTest(scope=s):
                self.assertIn(s, ccm.SCOPES)


if __name__ == "__main__":
    unittest.main()
