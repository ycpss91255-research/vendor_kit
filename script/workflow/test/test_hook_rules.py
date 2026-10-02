"""hook_rules.py：直接取用 .claude/hooks/comment_tag_guard.py 與 attribution_guard.py 的規則。"""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import body  # noqa: E402
import hook_rules as hr  # noqa: E402

HOME = "/" + "home/someone/"  # 拆開寫，避免這個測試檔本身被當成含本機路徑


class SameObject(unittest.TestCase):
    def test_body_uses_hook_local_paths(self):
        self.assertIs(body.LOCAL_PATHS, hr.hook.LOCAL_PATHS)
        self.assertIs(hr.LOCAL_PATHS, hr.hook.LOCAL_PATHS)

    def test_exports_come_from_hook(self):
        for name in hr.NAMES:
            with self.subTest(name=name):
                self.assertIs(getattr(hr, name), getattr(hr.hook, name))

    def test_banned_comes_from_attribution_guard(self):
        self.assertIs(hr.BANNED, hr.attribution.BANNED)
        self.assertEqual(hr.ATTRIBUTION_HOOK.parts[-3:], (".claude", "hooks", "attribution_guard.py"))
        self.assertTrue(hr.BANNED.search("Co-Authored-By: Claude <x>"))
        self.assertIsNone(hr.BANNED.search("一般的 PR 本文"))

    def test_default_path_is_the_hook(self):
        self.assertEqual(hr.HOOK.parts[-3:], (".claude", "hooks", "comment_tag_guard.py"))
        self.assertTrue(hr.HOOK.is_file())


class LoadErrors(unittest.TestCase):
    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path)
            self.assertIn(str(path), str(cm.exception))

    def test_missing_names_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            path.write_text("TAGS = ()\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path)
            self.assertIn("LOCAL_PATHS", str(cm.exception))

    def test_missing_attribution_names_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "attribution_guard.py"
            path.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError) as cm:
                hr.load(path, hr.ATTRIBUTION_NAMES)
            self.assertIn("BANNED", str(cm.exception))

    def test_broken_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "comment_tag_guard.py"
            path.write_text("raise RuntimeError('x')\n", encoding="utf-8")
            with self.assertRaises(hr.HookRulesError):
                hr.load(path)


class Rules(unittest.TestCase):
    def test_tagged(self):
        self.assertTrue(hr.tagged("[agy] 原文"))
        self.assertTrue(hr.tagged("  \n[claude] x"))
        self.assertFalse(hr.tagged("沒有標記"))

    def test_raw_with_note_passes(self):
        text = f"[agy] 原文提到 {HOME}x.py\n（註：對應 repo 的 script/x.py）\n"
        self.assertIsNone(hr.local_path_problem(text, "留言", raw_ok=True))

    def test_claude_with_local_path_blocked(self):
        text = f"[claude] 見 {HOME}x.py\n（註：對應 repo 的 script/x.py）\n"
        problem = hr.local_path_problem(text, "留言", raw_ok=True)
        self.assertIsNotNone(problem)
        self.assertIn("本機絕對路徑", problem)

    def test_relative_path_ok(self):
        self.assertIsNone(hr.local_path_problem("[claude] 見 script/x.py", "留言", raw_ok=False))


if __name__ == "__main__":
    unittest.main()
