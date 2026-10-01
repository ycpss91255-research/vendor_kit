"""prepare_comment.py：留言檔的標記、註記行、本機路徑替換、切分與 clean。"""
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import hook_rules  # noqa: E402
import prepare_comment as pc  # noqa: E402

# 拆開寫，避免這個測試檔本身被當成含本機路徑
HOME = "/" + "home/someone/"
MAC = "/" + "Users/someone/"
SCRATCH = "/" + "tmp/claude-1000/-proj/abc123/scratchpad/"
WIN = "C:" + "\\Users\\someone\\"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.ws = self.root / "ws"
        (self.ws / "reference/research/1").mkdir(parents=True)
        self.out = self.root / "post"

    def tearDown(self):
        self.tmp.cleanup()

    def src(self, name, text):
        p = self.ws / "reference/research/1" / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def run_main(self, *argv):
        buf = StringIO()
        with redirect_stdout(buf):
            code = pc.main(list(argv))
        return code, json.loads(buf.getvalue())

    def prepare(self, *items, max_=None):
        argv = ["prepare", "--out-dir", str(self.out), "--workspace", str(self.ws)]
        if max_ is not None:
            argv += ["--max", str(max_)]
        for it in items:
            argv += ["--item", *it]
        return self.run_main(*argv)

    def read(self, f):
        return pathlib.Path(f["path"]).read_text(encoding="utf-8")


class TagsAndNotes(Base):
    def test_tag_and_note_lines(self):
        a = self.src("a_agy.md", "agy 原文\n")
        c = self.src("a_codex.md", "codex 原文\n")
        r = self.src("review.md", "結論\n")
        code, out = self.prepare(("agy", a, "A 的 agy 調查原文"), ("codex", c, "A 的 codex 核對原文"),
                                 ("claude", r, "整合結論"))
        self.assertEqual((code, out["ok"]), (0, True), out)
        texts = [self.read(f).split("\n") for f in out["files"]]
        self.assertEqual(texts[0][0], "[agy] A 的 agy 調查原文")
        self.assertEqual(texts[0][1], "（註：以下是 reference/research/1/a_agy.md 的原文，未改寫。）")
        self.assertEqual(texts[0][2:4], ["", "agy 原文"])
        self.assertEqual(texts[1][0], "[codex] A 的 codex 核對原文")
        self.assertTrue(texts[1][1].startswith(hook_rules.NOTE_PREFIXES))
        self.assertEqual(texts[2][:3], ["[claude] 整合結論", "", "結論"])

    def test_order_and_names(self):
        a = self.src("a.md", "x\n")
        b = self.src("b.md", "y\n")
        r = self.src("r.md", "z\n")
        code, out = self.prepare(("agy", a, "1"), ("codex", b, "2"), ("agy", b, "3"), ("claude", r, "4"))
        self.assertEqual(code, 0, out)
        names = [pathlib.Path(f["path"]).name for f in out["files"]]
        self.assertEqual(names, ["post_01_agy.md", "post_02_codex.md", "post_03_agy.md", "post_04_claude.md"])
        self.assertEqual(names, sorted(names))
        self.assertEqual([f["source"] for f in out["files"]], [a, b, b, r])
        self.assertEqual([(f["part"], f["parts"]) for f in out["files"]], [(1, 1)] * 4)
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), names)

    def test_bad_tag_is_usage_error(self):
        a = self.src("a.md", "x\n")
        code, out = self.prepare(("gemini", a, "t"))
        self.assertEqual((code, out["ok"]), (2, False))
        self.assertIn("tag", out["error"])

    def test_missing_source(self):
        code, out = self.prepare(("claude", str(self.ws / "nope.md"), "t"))
        self.assertEqual((code, out["ok"]), (1, False))
        self.assertIn("讀不到來源檔", out["problems"][0])


class Paths(Base):
    def test_workspace_path_becomes_relative(self):
        text = f"見 {self.ws}/reference/research/1/x.md 與 {self.ws}/src/a.py 其他不動\n"
        a = self.src("a.md", text)
        code, out = self.prepare(("agy", a, "t"))
        self.assertEqual(code, 0, out)
        body = self.read(out["files"][0])
        self.assertIn("見 reference/research/1/x.md 與 src/a.py 其他不動\n", body)
        self.assertIn("原文的本機路徑已換成 workspace 相對路徑。", body.split("\n")[1])
        self.assertEqual(out["replaced"], [{"source": a, "from": f"{self.ws}/", "to": "", "count": 2}])

    def test_outside_workspace_and_scratchpad(self):
        text = (f"a {HOME}proj/x.py\nb {MAC}y\nc {SCRATCH}z.json\nd {WIN}w.txt\n"
                "e /" + "tmp/claude-1000/q\n")
        a = self.src("a.md", text)
        code, out = self.prepare(("codex", a, "t"))
        self.assertEqual(code, 0, out)
        body = self.read(out["files"][0])
        self.assertIn("a ~/proj/x.py\nb ~/y\nc <scratchpad>/z.json\nd ~\\w.txt\ne <scratchpad>/q\n", body)
        self.assertIn("~/", body.split("\n")[1])
        for pat, _label in hook_rules.LOCAL_PATHS:
            self.assertIsNone(pat.search(body))
        tos = {r["to"] for r in out["replaced"]}
        self.assertEqual(tos, {"~/", "<scratchpad>/", "~\\"})

    def test_claude_paths_replaced_without_note(self):
        r = self.src("r.md", f"見 {self.ws}/src/a.py\n")
        code, out = self.prepare(("claude", r, "整合結論"))
        self.assertEqual(code, 0, out)
        self.assertEqual(self.read(out["files"][0]), "[claude] 整合結論\n\n見 src/a.py\n")

    def test_no_replacement_no_extra_note(self):
        a = self.src("a.md", "純文字\n")
        _code, out = self.prepare(("agy", a, "t"))
        self.assertNotIn("本機路徑", self.read(out["files"][0]))
        self.assertEqual(out["replaced"], [])

    def test_table_covers_hook_patterns(self):
        for _pat, label in hook_rules.LOCAL_PATHS:
            self.assertIn(label, pc.REPLACE)


class Split(Base):
    def test_split_on_blank_line_with_numbering(self):
        paras = ["\n".join(f"段{p}行{i}" + "x" * 20 for i in range(5)) for p in range(6)]
        a = self.src("a.md", "\n\n".join(paras) + "\n")
        code, out = self.prepare(("agy", a, "標題"), max_=400)
        self.assertEqual(code, 0, out)
        n = len(out["files"])
        self.assertGreater(n, 1)
        bodies = []
        for k, f in enumerate(out["files"], 1):
            text = self.read(f)
            self.assertLessEqual(len(text), 400)
            self.assertEqual(f["chars"], len(text))
            self.assertEqual((f["part"], f["parts"]), (k, n))
            lines = text.split("\n")
            self.assertEqual(lines[0], f"[agy] 標題（{k}/{n}）")
            self.assertTrue(lines[1].startswith("（註"))
            body = "\n".join(lines[3:])
            if k < n:
                self.assertTrue(body.endswith("\n\n"), repr(body[-30:]))
            bodies.append(body)
        self.assertEqual("".join(bodies), self.read_src(a))

    def read_src(self, a):
        return pathlib.Path(a).read_text(encoding="utf-8")

    def test_no_cut_inside_code_block_when_avoidable(self):
        before = "".join(f"前文{i}\n" for i in range(30))
        code_block = "```python\n" + "".join(f"x{i} = {i}\n" for i in range(10)) + "```\n"
        a = self.src("a.md", before + code_block + "後文\n")
        code, out = self.prepare(("claude", a, "t"), max_=300)
        self.assertEqual(code, 0, out)
        for f in out["files"]:
            body = self.read(f).split("\n", 2)[2]
            self.assertEqual(sum(1 for ln in body.split("\n") if ln.startswith("```")) % 2, 0, body)
        joined = "".join(self.read(f).split("\n", 2)[2] for f in out["files"])
        self.assertEqual(joined, self.read_src(a))

    def test_long_code_block_closed_and_reopened(self):
        code_block = "```sh\n" + "".join(f"echo {i}\n" for i in range(80)) + "```\n"
        a = self.src("a.md", code_block)
        code, out = self.prepare(("claude", a, "t"), max_=200)
        self.assertEqual(code, 0, out)
        self.assertGreater(len(out["files"]), 1)
        for k, f in enumerate(out["files"]):
            text = self.read(f)
            self.assertLessEqual(len(text), 200)
            body = text.split("\n", 2)[2]
            self.assertTrue(body.startswith("```sh\n"), body[:20])
            self.assertTrue(body.endswith("```\n"), body[-20:])

    def test_overlong_line_hard_split(self):
        a = self.src("a.md", "y" * 1000 + "\n")
        code, out = self.prepare(("claude", a, "t"), max_=300)
        self.assertEqual(code, 0, out)
        self.assertGreater(len(out["files"]), 3)
        joined = "".join(self.read(f).split("\n", 2)[2] for f in out["files"])
        self.assertEqual(joined, "y" * 1000 + "\n")
        for f in out["files"]:
            self.assertLessEqual(f["chars"], 300)

    def test_no_split_under_default_max(self):
        a = self.src("a.md", "x\n" * 1000)
        _code, out = self.prepare(("agy", a, "t"))
        self.assertEqual(len(out["files"]), 1)
        self.assertEqual(self.read(out["files"][0]).split("\n")[0], "[agy] t")


class HookRules(Base):
    def test_outputs_pass_hook(self):
        a = self.src("a.md", f"{HOME}x {SCRATCH}y\n" * 40)
        r = self.src("r.md", f"{self.ws}/src/a.py\n" * 40)
        code, out = self.prepare(("agy", a, "t"), ("claude", r, "結論"), max_=500)
        self.assertEqual(code, 0, out)
        for f in out["files"]:
            text = self.read(f)
            self.assertTrue(hook_rules.tagged(text))
            self.assertIsNone(hook_rules.local_path_problem(text, "x", raw_ok=True))
            self.assertIsNone(hook_rules.local_path_problem(text, "x", raw_ok=False))

    def test_self_check_reports_leftover(self):
        problems = pc.self_check(f"[claude] x\n{HOME}y\n", "post_01_claude.md")
        self.assertTrue(problems)


class Clean(Base):
    def test_clean_and_prepare_replaces_old(self):
        self.out.mkdir()
        (self.out / "post_09_agy.md").write_text("old", encoding="utf-8")
        (self.out / "keep.md").write_text("keep", encoding="utf-8")
        a = self.src("a.md", "x\n")
        _code, out = self.prepare(("claude", a, "t"))
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["keep.md", "post_01_claude.md"])
        code, out = self.run_main("clean", "--out-dir", str(self.out))
        self.assertEqual((code, out["ok"]), (0, True))
        self.assertEqual([pathlib.Path(p).name for p in out["removed"]], ["post_01_claude.md"])
        self.assertEqual([p.name for p in self.out.iterdir()], ["keep.md"])

    def test_clean_missing_dir(self):
        code, out = self.run_main("clean", "--out-dir", str(self.root / "none"))
        self.assertEqual((code, out), (0, {"ok": True, "removed": []}))


if __name__ == "__main__":
    unittest.main()
