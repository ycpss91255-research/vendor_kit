"""backup.py 的鍵、備份序號、快照比對與 diff 基準：跑法 `python3 -m unittest discover -s script/doc/test`。"""
import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import backup  # noqa: E402
import mark_changes  # noqa: E402

SCRIPT = HERE.parent / "backup.py"


def run(*args):
    """跑腳本，回傳（結束碼, JSON）。"""
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    assert len(lines) == 1, r.stdout + r.stderr
    return r.returncode, json.loads(lines[0])


class KeyTest(unittest.TestCase):
    FILES = [
        "doc/contract/01_purpose.md",
        "doc/contract/03_output.md",
        "doc/contract/03_output.csv",
        "README.md",
        ".claude/workflows/README.md",
        "doc/decisions/review/03_output.csv",
    ]

    def test_backup_key_matches_mark_changes_target(self):
        code, out = run("key", *self.FILES)
        self.assertEqual(code, 0)
        self.assertTrue(out["ok"])
        for item in out["keys"]:
            self.assertEqual(item["backup_key"], mark_changes.target(item["file"])[1], item["file"])

    def test_run_key_keeps_extension(self):
        _, out = run("key", *self.FILES, "Makefile")
        keys = {k["file"]: k for k in out["keys"]}
        self.assertEqual(keys["doc/decisions/review/03_output.csv"]["run_key"], "doc_decisions_review_03_output_csv")
        self.assertEqual(keys["README.md"]["run_key"], "README_md")
        self.assertEqual(keys["Makefile"]["run_key"], keys["Makefile"]["backup_key"])
        md, csv = keys["doc/contract/03_output.md"], keys["doc/contract/03_output.csv"]
        self.assertEqual(md["backup_key"], csv["backup_key"])
        self.assertNotEqual(md["run_key"], csv["run_key"])

    def test_usage_error_is_json_exit_2(self):
        code, out = run("key")
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])


class RepoCase(unittest.TestCase):
    """暫存 git repo：doc/contract/01_purpose.md、03_output.csv、README.md 已 commit。"""

    R = "r7"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name).resolve() / "repo"
        self.root.mkdir()
        self.scratch = pathlib.Path(self.tmp.name).resolve() / "scratch"
        self.scratch.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("config", "commit.gpgsign", "false")
        (self.root / ".gitignore").write_text("doc/decisions/_backup/\ndoc/decisions/review_log/\n")
        self.write("doc/contract/01_purpose.md", "原文\n")
        self.write("doc/contract/03_output.csv", "code,message\nVK0001,a\n")
        self.write("README.md", "readme\n")
        self.write("doc/decisions/scope_roadmap.md", "scope\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def backup_dir(self):
        return self.root / "doc/decisions/_backup"

    def save(self, *files):
        return run("save", "--repo", self.root, "--round", self.R, *files)

    def snapshot(self, *files):
        out = self.scratch / "before.json"
        code, res = run("snapshot", "--repo", self.root, "--out", out, "--files", *files)
        self.assertEqual(code, 0, res)
        return out

    def verify(self, before, scope, round_files):
        return run("verify", "--repo", self.root, "--round", self.R, "--before", before,
                   "--scope", *scope, "--round-files", *round_files)


class SaveTest(RepoCase):
    F = "doc/contract/01_purpose.md"

    def test_first_save_creates_base_then_same_content_is_not_saved(self):
        code, out = self.save(self.F)
        self.assertEqual(code, 0)
        r = out["results"][0]
        self.assertTrue(r["created"])
        self.assertEqual(r["seq"], 1)
        self.assertEqual(pathlib.Path(r["backup"]).name, "doc_contract_01_purpose.pre_r7.md")
        _, out = self.save(self.F)
        r2 = out["results"][0]
        self.assertFalse(r2["created"])
        self.assertEqual(r2["backup"], r["backup"])
        self.assertEqual(len(list(self.backup_dir().iterdir())), 1)

    def test_changed_content_gets_2_then_3(self):
        self.save(self.F)
        self.write(self.F, "改一\n")
        _, out = self.save(self.F)
        self.assertEqual(out["results"][0]["seq"], 2)
        self.assertTrue(out["results"][0]["backup"].endswith("doc_contract_01_purpose.pre_r7.2.md"))
        self.write(self.F, "改二\n")
        _, out = self.save(self.F)
        self.assertEqual(out["results"][0]["seq"], 3)
        # 回到已備份過的內容：回報那一份，不另存
        self.write(self.F, "改一\n")
        _, out = self.save(self.F)
        self.assertFalse(out["results"][0]["created"])
        self.assertEqual(out["results"][0]["seq"], 2)

    def test_csv_backup_ext(self):
        _, out = self.save("doc/contract/03_output.csv")
        self.assertTrue(out["results"][0]["backup"].endswith("doc_contract_03_output.pre_r7.csv"))

    def test_missing_file_not_backed_up(self):
        code, out = self.save("doc/contract/new.md")
        self.assertEqual(code, 0)
        self.assertTrue(out["results"][0]["missing"])
        self.assertFalse(self.backup_dir().exists())

    def test_bad_round_is_usage_error(self):
        code, out = run("save", "--repo", self.root, "--round", "7", self.F)
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])

    def test_base(self):
        _, out = run("base", "--repo", self.root, "--round", self.R, self.F)
        self.assertFalse(out["exists"])
        self.save(self.F)
        _, out = run("base", "--repo", self.root, "--round", self.R, self.F)
        self.assertTrue(out["exists"])


class VerifyTest(RepoCase):
    F = "doc/contract/01_purpose.md"
    G = "doc/contract/03_output.csv"

    def test_r152_base_equals_before_no_extra_backup_is_ok(self):
        # 改寫前已建基準；套用必改時內容等於基準、codex 沒另存備份就改檔（#133）
        self.save(self.F)
        before = self.snapshot(self.F)
        self.write(self.F, "套用必改\n")
        code, out = self.verify(before, [self.F], [self.F, self.G])
        self.assertEqual(code, 0, out)
        self.assertTrue(out["ok"])
        self.assertEqual(out["backup_problems"], [])
        self.assertIn(self.F, out["changed"])
        self.assertIn("01_purpose", out["diffstat"])

    def test_before_not_in_any_backup_is_problem(self):
        self.save(self.F)
        self.write(self.F, "改寫後\n")
        before = self.snapshot(self.F)
        self.write(self.F, "套用必改\n")
        code, out = self.verify(before, [self.F], [self.F])
        self.assertEqual(code, 1)
        self.assertFalse(out["ok"])
        self.assertEqual([p["file"] for p in out["backup_problems"]], [self.F])

    def test_saved_before_change_is_ok_and_reported_as_new_backup(self):
        self.save(self.F)
        self.write(self.F, "改寫後\n")
        before = self.snapshot(self.F)
        _, saved = self.save(self.F)
        self.write(self.F, "套用必改\n")
        code, out = self.verify(before, [self.F], [self.F])
        self.assertEqual(code, 0, out)
        self.assertEqual(out["new_backups"], [saved["results"][0]["backup"]])

    def test_no_base_is_problem(self):
        before = self.snapshot(self.F)
        self.write(self.F, "改\n")
        code, out = self.verify(before, [self.F], [self.F])
        self.assertEqual(code, 1)
        self.assertIn("不存在", out["backup_problems"][0]["reason"])

    def test_out_of_scope_and_parallel(self):
        self.save(self.F)
        before = self.snapshot(self.F)
        self.write(self.F, "改\n")
        self.write("README.md", "越界\n")
        self.write(self.G, "code,message\nVK0001,b\n")
        self.write("script/new.py", "x\n")
        code, out = self.verify(before, [self.F], [self.F, self.G])
        self.assertEqual(code, 1)
        self.assertEqual(out["out_of_scope"], ["README.md", "script/new.py"])
        self.assertEqual(out["parallel"], [self.G])
        self.assertEqual(out["backup_problems"], [])

    def test_doc_decisions_not_out_of_scope(self):
        self.save(self.F)
        before = self.snapshot(self.F)
        self.write(self.F, "改\n")
        self.write("doc/decisions/scope_roadmap.md", "變\n")
        self.write("doc/decisions/review_log/codex/r7-x.md", "log\n")
        code, out = self.verify(before, [self.F], [self.F])
        self.assertEqual(code, 0, out)
        self.assertEqual(out["out_of_scope"], [])
        self.assertIn("doc/decisions/scope_roadmap.md", out["changed"])

    def test_file_dirty_before_and_unchanged_is_not_changed(self):
        self.write("README.md", "先前就改了\n")
        self.save(self.F)
        before = self.snapshot(self.F)
        self.write(self.F, "改\n")
        code, out = self.verify(before, [self.F], [self.F])
        self.assertEqual(code, 0, out)
        self.assertNotIn("README.md", out["changed"])


class DiffTest(RepoCase):
    F = "doc/contract/01_purpose.md"

    def diff(self, f=None):
        return run("diff", "--repo", self.root, "--round", self.R, f or self.F)

    def test_falls_back_to_head_without_backup(self):
        self.write(self.F, "新文\n")
        code, out = self.diff()
        self.assertEqual(code, 0)
        self.assertEqual(out["base_kind"], "HEAD")
        self.assertFalse(out["empty"])
        self.assertIn("-原文", out["diff"])
        self.assertIn("+新文", out["diff"])

    def test_uses_round_base_when_present(self):
        self.write(self.F, "改寫後\n")
        self.save(self.F)
        _, out = self.diff()
        self.assertEqual(out["base_kind"], "backup")
        self.assertTrue(out["empty"])
        self.assertEqual(out["diff"], "")

    def test_new_file_is_all_added(self):
        self.write("doc/contract/new.md", "全新\n")
        _, out = self.diff("doc/contract/new.md")
        self.assertEqual(out["base_kind"], "none")
        self.assertIn("+全新", out["diff"])


class InProcessTest(unittest.TestCase):
    def test_main_returns_code(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = backup.main(["key", "README.md"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(buf.getvalue())["keys"][0]["run_key"], "README_md")


if __name__ == "__main__":
    unittest.main()
