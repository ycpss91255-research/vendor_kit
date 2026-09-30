"""comment_tag_guard.py 的測試：用 subprocess 餵 PreToolUse 的 JSON，看 deny 或放行。

跑法：python3 -m unittest discover -s script/test
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "comment_tag_guard.py"
API = "repos/ycpss91255-research/vendor_kit/issues/5/comments"


class CommentTagGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name).resolve()
        (cls.dir / "ok.md").write_text("\n  [claude] 已處理\n第二行\n")
        (cls.dir / "codex.md").write_text("[codex] 原文\n")
        (cls.dir / "bad.md").write_text("已處理\n[claude] 不在第一行\n")
        (cls.dir / "ok.json").write_text(json.dumps({"body": "[agy] 看過了"}))
        (cls.dir / "bad.json").write_text(json.dumps({"body": "看過了"}))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_hook(self, tool, tool_input):
        payload = {"tool_name": tool, "tool_input": tool_input, "cwd": str(self.dir)}
        out = subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(payload),
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if not out:
            return "allow"
        return json.loads(out)["hookSpecificOutput"]

    def decision(self, command):
        r = self.run_hook("Bash", {"command": command})
        return r if r == "allow" else r["permissionDecision"]

    def assertDeny(self, command):
        self.assertEqual(self.decision(command), "deny", command)

    def assertAllow(self, command):
        self.assertEqual(self.decision(command), "allow", command)

    # 留言：--body 字串
    def test_issue_comment_tagged_allowed(self):
        for tag in ("[claude]", "[codex]", "[agy]"):
            self.assertAllow(f"gh issue comment 5 --body '{tag} 已處理'")

    def test_issue_comment_leading_space_allowed(self):
        self.assertAllow("gh issue comment 5 --body '  \n[claude] 已處理'")

    def test_issue_comment_untagged_denied(self):
        self.assertDeny("gh issue comment 5 --body '已處理'")

    def test_issue_comment_tag_not_first_line_denied(self):
        self.assertDeny("gh issue comment 5 --body '已處理\n[claude]'")

    def test_issue_comment_b_and_equals(self):
        self.assertDeny("gh issue comment 5 -b x")
        self.assertAllow("gh issue comment 5 --body='[claude] x'")

    def test_pr_comment(self):
        self.assertAllow("gh pr comment 3 --body '[codex] 原文'")
        self.assertDeny("gh pr comment 3 --body 'LGTM'")

    def test_comment_without_body_denied(self):
        self.assertDeny("gh issue comment 5")

    # 留言：讀檔
    def test_body_file_tagged_allowed(self):
        self.assertAllow("gh issue comment 5 --body-file ok.md")
        self.assertAllow(f"gh pr comment 3 -F {self.dir / 'codex.md'}")

    def test_body_file_untagged_denied(self):
        self.assertDeny("gh issue comment 5 --body-file bad.md")
        self.assertDeny("gh pr comment 3 -F bad.md")

    def test_body_file_missing_denied(self):
        self.assertDeny("gh issue comment 5 --body-file nope.md")

    def test_body_file_stdin_denied(self):
        self.assertDeny("gh issue comment 5 --body-file - <<'EOF'\n[claude] x\nEOF")

    # pr review
    def test_pr_review_body(self):
        self.assertAllow("gh pr review 3 --comment --body '[claude] 看過'")
        self.assertDeny("gh pr review 3 --request-changes -b '要改'")
        self.assertDeny("gh pr review 3 --comment -F bad.md")

    def test_pr_review_without_body_allowed(self):
        self.assertAllow("gh pr review 3 --approve")

    # close 帶留言
    def test_close_with_comment_denied(self):
        self.assertDeny("gh issue close 5 --comment '[claude] 完成'")
        self.assertDeny("gh pr close 3 -c '[claude] 完成'")

    def test_close_plain_allowed(self):
        self.assertAllow("gh issue close 5 --reason completed")
        self.assertAllow("gh pr close 3")

    # gh api comments 端點
    def test_api_comment_tagged_allowed(self):
        self.assertAllow(f"gh api {API} -f body='[claude] x'")
        self.assertAllow(f"gh api {API} -X POST --raw-field 'body=[agy] x'")

    def test_api_comment_untagged_denied(self):
        self.assertDeny(f"gh api {API} -f body=x")
        self.assertDeny(f"gh api {API} --field body=x")

    def test_api_comment_patch_denied(self):
        self.assertDeny("gh api repos/o/r/issues/comments/99 -X PATCH -f body=x")

    def test_api_comment_file_field(self):
        self.assertAllow(f"gh api {API} -F body=@ok.md")
        self.assertDeny(f"gh api {API} -F body=@bad.md")

    def test_api_comment_input(self):
        self.assertAllow(f"gh api {API} --input ok.json")
        self.assertDeny(f"gh api {API} --input bad.json")

    def test_api_pull_comment_denied(self):
        self.assertDeny("gh api repos/o/r/pulls/3/comments -f body=x -f commit_id=a -f path=p")

    def test_api_get_comments_allowed(self):
        self.assertAllow(f"gh api {API}")
        self.assertAllow(f"gh api {API} -X GET -f per_page=100")

    def test_api_other_endpoint_allowed(self):
        self.assertAllow("gh api repos/o/r/issues/5/sub_issues -X POST -F sub_issue_id=1")

    # create
    def test_issue_create(self):
        self.assertAllow("gh issue create -R o/r --title t --body-file ok.md --label needs-triage")
        self.assertAllow("gh issue create --title t -F bad.md -l bug")
        self.assertDeny("gh issue create --title t --body b --label bug")
        self.assertDeny("gh issue create --title t -b b --label bug")
        self.assertDeny("gh issue create --title t --body-file ok.md")
        self.assertDeny("gh issue create --title t --label bug")

    def test_pr_create(self):
        self.assertAllow("gh pr create --title t --body-file ok.md")
        self.assertAllow("gh pr create --base main -F ok.md --title t")
        self.assertDeny("gh pr create --title t --body b")
        self.assertDeny("gh pr create --fill")

    # 串接指令
    def test_chained_denied(self):
        self.assertDeny("gh issue comment 5 --body '[claude] ok' && gh pr comment 3 --body 'no tag'")
        self.assertDeny("git push && gh issue comment 5 --body-file bad.md")

    def test_chained_allowed(self):
        self.assertAllow("gh issue comment 5 --body '[claude] a && b' && gh issue close 5")

    def test_deny_message(self):
        r = self.run_hook("Bash", {"command": "gh issue comment 5 --body x"})
        reason = r["permissionDecisionReason"]
        for s in ("[claude]", "[codex]", "[agy]", "維護者本人", "不得代寫"):
            self.assertIn(s, reason)

    def test_unrelated_allowed(self):
        self.assertAllow("gh issue view 5 --comments")
        self.assertAllow("gh issue edit 5 --add-label bug")
        self.assertEqual(self.run_hook("Edit", {"file_path": "/tmp/x"}), "allow")


if __name__ == "__main__":
    unittest.main()
