"""issue_body_guard.py 的測試：用 subprocess 餵 PreToolUse 的 JSON，看 deny 或放行。

跑法：python3 -m unittest discover -s .claude/hooks/test
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "issue_body_guard.py"
R = "-R ycpss91255-research/vendor_kit"
API = "repos/ycpss91255-research/vendor_kit/issues/5"


class IssueBodyGuardTest(unittest.TestCase):
    def run_hook(self, tool, tool_input):
        payload = {"tool_name": tool, "tool_input": tool_input, "cwd": "/tmp"}
        out = subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(payload),
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if not out:
            return "allow"
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]

    def bash(self, command):
        return self.run_hook("Bash", {"command": command})

    def assertDeny(self, command):
        self.assertEqual(self.bash(command), "deny", command)

    def assertAllow(self, command):
        self.assertEqual(self.bash(command), "allow", command)

    # gh issue edit：本文與標題
    def test_issue_edit_body_denied(self):
        self.assertDeny(f"gh issue edit 5 {R} --body 'new'")

    def test_issue_edit_body_equals_denied(self):
        self.assertDeny("gh issue edit 5 --body=new")

    def test_issue_edit_b_denied(self):
        self.assertDeny("gh issue edit 5 -b new")

    def test_issue_edit_body_file_denied(self):
        self.assertDeny("gh issue edit 5 --body-file body.md")

    def test_issue_edit_F_denied(self):
        self.assertDeny("gh issue edit 5 -F body.md")

    def test_issue_edit_title_denied(self):
        self.assertDeny("gh issue edit 5 --title 'x'")

    def test_issue_edit_t_denied(self):
        self.assertDeny("gh issue edit 5 -t x")

    def test_issue_edit_reason_text(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "gh issue edit 5 --body x"}}
        out = subprocess.run(
            [sys.executable, str(HOOK)], input=json.dumps(payload),
            capture_output=True, text=True, check=True,
        ).stdout
        reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("gh issue comment", reason)
        self.assertIn("wayfinder", reason)

    # gh issue edit：其他欄位放行
    def test_issue_edit_add_label_allowed(self):
        self.assertAllow(f"gh issue edit 5 {R} --add-label needs-triage")

    def test_issue_edit_remove_label_allowed(self):
        self.assertAllow("gh issue edit 5 --remove-label needs-triage")

    def test_issue_edit_assignee_allowed(self):
        self.assertAllow("gh issue edit 5 --add-assignee @me")

    def test_issue_edit_milestone_allowed(self):
        self.assertAllow("gh issue edit 5 --milestone v1")

    # 其他 issue 與 PR 指令放行
    def test_issue_comment_allowed(self):
        self.assertAllow(f"gh issue comment 5 {R} --body 'x'")

    def test_issue_comment_body_file_allowed(self):
        self.assertAllow("gh issue comment 5 -F note.md")

    def test_issue_close_reopen_allowed(self):
        self.assertAllow("gh issue close 5")
        self.assertAllow("gh issue reopen 5")

    def test_issue_create_allowed(self):
        self.assertAllow(f"gh issue create {R} --title t --body b")

    def test_pr_edit_body_allowed(self):
        self.assertAllow("gh pr edit 3 --body x --title y")

    def test_pr_create_allowed(self):
        self.assertAllow("gh pr create --title t --body b")

    # gh api：PATCH 本文
    def test_api_patch_f_body_denied(self):
        self.assertDeny(f"gh api {API} -X PATCH -f body=x")

    def test_api_patch_F_body_denied(self):
        self.assertDeny(f"gh api {API} -X PATCH -F body=@b.md")

    def test_api_method_patch_field_denied(self):
        self.assertDeny(f"gh api --method PATCH {API} --field body=x")

    def test_api_raw_field_denied(self):
        self.assertDeny(f"gh api {API} --method=PATCH --raw-field body=x")

    def test_api_input_denied(self):
        self.assertDeny(f"gh api {API} -X PATCH --input body.json")

    def test_api_leading_slash_denied(self):
        self.assertDeny(f"gh api /{API} -XPATCH -f body=x")

    def test_api_placeholder_denied(self):
        self.assertDeny("gh api repos/{owner}/{repo}/issues/5 -X PATCH -f body=x")

    # gh api：放行
    def test_api_get_allowed(self):
        self.assertAllow(f"gh api {API}")

    def test_api_patch_labels_only_allowed(self):
        self.assertAllow(f"gh api {API} -X PATCH -f state=closed")

    def test_api_comments_patch_allowed(self):
        self.assertAllow(f"gh api {API}/comments -X PATCH -f body=x")

    def test_api_sub_issues_post_allowed(self):
        self.assertAllow(f"gh api {API}/sub_issues -X POST -F sub_issue_id=123")

    def test_api_dependencies_post_allowed(self):
        self.assertAllow(f"gh api {API}/dependencies/blocked_by -X POST -F issue_id=123")

    # 串接指令
    def test_chained_denied(self):
        self.assertDeny("gh issue comment 5 --body 'a && b' && gh issue edit 5 --body x")

    def test_chained_newline_denied(self):
        self.assertDeny("gh issue comment 5 --body ok\ngh api " + API + " -X PATCH -f body=x")

    def test_quoted_mention_allowed(self):
        self.assertAllow("gh issue comment 5 --body 'do not run gh issue edit 5 --body x'")

    def test_non_bash_ignored(self):
        self.assertEqual(self.run_hook("Edit", {"file_path": "/tmp/x"}), "allow")


if __name__ == "__main__":
    unittest.main()
