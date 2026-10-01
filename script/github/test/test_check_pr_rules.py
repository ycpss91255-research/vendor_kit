"""check_pr_rules.py 的測試。

跑法：python3 -m unittest discover -s script/github/test
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import check_pr_rules as c  # noqa: E402

SCRIPT = HERE.parent / "check_pr_rules.py"
TABLE = c.load_table()


class IssueLinkTest(unittest.TestCase):
    def test_accepted_forms(self):
        for body in ("Refs #3", "Refs: #3", "Closes #3", "fixes #3", "Resolves: #3", "x\nREFS #3\n"):
            with self.subTest(body=body):
                self.assertEqual(c.linked_issues(body), [3])

    def test_multiple_allowed(self):
        r = c.check("Closes #1\nRefs #2", [], TABLE)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["issues"], [1, 2])

    def test_missing_is_violation_no_exemption(self):
        for body in ("", "typo fix", "#12", "see issue 12", "no bug"):
            with self.subTest(body=body):
                r = c.check(body, [], TABLE)
                self.assertFalse(r["ok"])
                self.assertIn("沒有連 issue", r["problems"][0])


class ScopeTest(unittest.TestCase):
    def scopes(self, files):
        return c.scopes_of(files, TABLE)

    def test_tool_with_test_and_readme_is_one_scope(self):
        s, p = self.scopes(["script/doc/pack_review.py", "script/doc/test/test_pack_review.py",
                            "script/doc/README.md", "script/README.md", ".github/workflows/docs.yml"])
        self.assertEqual((s, p), (["script:doc"], []))

    def test_hook_with_its_test(self):
        s, p = self.scopes([".claude/hooks/terms_context.py", ".claude/hooks/test/test_terms_context.py",
                            ".github/workflows/docs.yml"])
        self.assertEqual((s, p), (["hook:terms_context"], []))

    def test_agents_line_attaches(self):
        s, p = self.scopes(["AGENTS.md", "doc/agents/drawio.md"])
        self.assertEqual((s, p), (["agents-doc:drawio"], []))

    def test_two_scopes_is_violation(self):
        s, p = self.scopes([".claude/workflows/doc-edit.js", ".claude/workflows/discuss.js"])
        self.assertEqual(len(s), 2)
        self.assertIn("2 個範圍", p[0])

    def test_test_alone_counts_as_scope(self):
        s, p = self.scopes([".claude/hooks/test_guard.py"])
        self.assertEqual((s, p), (["hook:guard"], []))

    def test_test_of_other_scope_is_not_attached(self):
        s, p = self.scopes([".claude/workflows/doc-edit.js", ".claude/hooks/test_guard.py"])
        self.assertEqual(sorted(s), ["hook:guard", "workflow:doc-edit"])
        self.assertTrue(p)

    def test_only_attached_files(self):
        s, p = self.scopes(["AGENTS.md"])
        self.assertEqual((s, p), (["agents"], []))

    def test_group_merges(self):
        s, p = self.scopes([".claude/hooks/pr_rules_guard.py", ".claude/hooks/test/test_pr_rules_guard.py",
                            "script/github/check_pr_rules.py", "script/github/scope.json",
                            "script/github/test/test_check_pr_rules.py", "script/github/README.md"])
        self.assertEqual((s, p), (["hook:pr_rules_guard"], []))

    def test_group_does_not_merge_outsiders(self):
        s, p = self.scopes([".claude/hooks/pr_rules_guard.py", "script/doc/check_terms.py"])
        self.assertEqual(len(s), 2)
        self.assertTrue(p)

    def test_unlisted_file_is_violation(self):
        s, p = self.scopes(["discussion.drawio"])
        self.assertIn("沒有列到", p[0])

    def test_contract_pages_are_separate(self):
        s, _ = self.scopes(["doc/decisions/review/01_purpose.md", "doc/decisions/review/02_invariants.md"])
        self.assertEqual(s, ["contract:01_purpose", "contract:02_invariants"])

    def test_every_tracked_file_is_listed(self):
        root = HERE.parents[2]
        out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True).stdout
        unlisted = [f for f in out.splitlines() if c.classify(f, TABLE) is None]
        self.assertEqual(unlisted, [], "範圍表沒列到這些追蹤中的檔")


class CliTest(unittest.TestCase):
    def run_cli(self, body, files):
        with tempfile.TemporaryDirectory() as d:
            b = Path(d) / "body.md"
            b.write_text(body, encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), "--body-file", str(b), "--files-from", "-"],
                               input="\n".join(files), capture_output=True, text=True)
            return r.returncode, json.loads(r.stdout)

    def test_ok(self):
        code, out = self.run_cli("Closes #5\n", ["script/doc/check_terms.py"])
        self.assertEqual(code, 0)
        self.assertEqual(out["scopes"], ["script:doc"])

    def test_violation(self):
        code, out = self.run_cli("nothing", ["script/doc/check_terms.py", "CONTEXT.md"])
        self.assertEqual(code, 1)
        self.assertEqual(len(out["problems"]), 2)

    def test_missing_body_file(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--body-file", "/nonexistent/x.md"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("讀不到輸入", json.loads(r.stdout)["problems"][0])


if __name__ == "__main__":
    unittest.main()
