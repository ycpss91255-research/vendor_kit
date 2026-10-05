"""script/diagram/lint.py 的測試：圖都在測試裡組出來，不連 drawio 服務。"""
import base64
import contextlib
import io
import json
import sys
import tempfile
import unittest
import urllib.parse
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import lint  # noqa: E402

STEP = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;"
RHOMB = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF4C3;strokeColor=#000000;strokeWidth=2;fontSize=14;spacingLeft=40;spacingRight=40;spacingTop=20;spacingBottom=20;"
GREEN = "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#000000;strokeWidth=2;fontSize=14;spacingLeft=30;spacingRight=30;spacingTop=6;spacingBottom=6;"
RED = GREEN.replace("#d5e8d4", "#f8cecc")
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;fontSize=12;"

GLOSSARY = """# 名詞

**引擎**（engine）：
執行 recipe 的主程式。

**repo**：
使用者的 git repo。
_Avoid_: 專案、下游 repo
"""


def v(cid, value, style, x, y, w=200, h=40, parent="1"):
    return (f'<mxCell id="{cid}" value="{value}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def e(cid, s, t, label="", style=EDGE):
    return (f'<mxCell id="{cid}" value="{label}" style="{style}" edge="1" parent="1" source="{s}" target="{t}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')


def legend(prefix="p", fills=("#FFF4C3", "#d5e8d4", "#f8cecc")):
    out = []
    for i, f in enumerate(fills):
        out.append(v(f"{prefix}_lg{i}", "圖例", f"rounded=1;whiteSpace=wrap;html=1;fillColor={f};fontSize=12;", 40 + i * 200, 900, 180, 40))
    return out


def page(pid, cells, name=None):
    body = '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells)
    return f'<diagram id="{pid}" name="{name or pid}"><mxGraphModel><root>{body}</root></mxGraphModel></diagram>'


def mxfile(*pages):
    return '<mxfile host="test">' + "".join(pages) + "</mxfile>"


def flow_cells():
    """乾淨的流程頁：起點 → 步驟 → 判斷 →（是）綠終點／（否）紅終點。"""
    return [
        v("s", "開始", GREEN, 400, 20, 160, 50),
        v("a", "讀版本", STEP, 380, 120),
        v("d", "相符？", RHOMB, 380, 220, 200, 100),
        v("ok", "結束碼 0", GREEN, 100, 400, 160, 50),
        v("ng", "結束碼 1", RED, 700, 400, 160, 50),
        e("e1", "s", "a"), e("e2", "a", "d"),
        e("e3", "d", "ok", "是"), e("e4", "d", "ng", "否"),
    ] + legend()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "CONTEXT.md").write_text(GLOSSARY, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, xml):
        p = self.dir / name
        p.write_text(xml, encoding="utf-8")
        return p

    def run_lint(self, xml, rules=None, base_xml=None, root=None):
        f = self.write("a.drawio", xml)
        b = self.write("b.drawio", base_xml) if base_xml else None
        return lint.lint(f, b, rules, repo_root=root or self.dir)

    def rules_hit(self, res):
        return {x["rule"] for x in res["violations"]}

    def cells_hit(self, res, rule):
        return {x["cell"] for x in res["violations"] if x["rule"] == rule}


class TestClean(Base):
    def test_clean_flow_page_passes(self):
        res = self.run_lint(mxfile(page("p1", flow_cells())))
        self.assertTrue(res["ok"], res["violations"])
        self.assertEqual(res["skipped"], [])

    def test_compressed_diagram_is_read(self):
        inner = '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(flow_cells()) + "</root></mxGraphModel>"
        co = zlib.compressobj(9, zlib.DEFLATED, -15)
        data = base64.b64encode(co.compress(urllib.parse.quote(inner).encode()) + co.flush()).decode()
        res = self.run_lint(f'<mxfile><diagram id="z" name="z">{data}</diagram></mxfile>')
        self.assertTrue(res["ok"], res["violations"])

    def test_user_object_wrapper(self):
        cells = flow_cells()
        cells[1] = (f'<object id="a" label="讀版本"><mxCell style="{STEP}" vertex="1" parent="1">'
                    '<mxGeometry x="380" y="120" width="200" height="40" as="geometry"/></mxCell></object>')
        res = self.run_lint(mxfile(page("p1", cells)))
        self.assertTrue(res["ok"], res["violations"])


class TestRules(Base):
    def test_overlap(self):
        cells = flow_cells() + [v("blk", "擋路", STEP, 380, 60, 200, 30)]
        res = self.run_lint(mxfile(page("p1", cells)), ["overlap"])
        self.assertIn("e1", self.cells_hit(res, "overlap"))

    def test_overflow_counts_fullwidth(self):
        cells = flow_cells()
        cells[1] = v("a", "讀版本讀版本讀版本讀版本讀版本讀版本讀版本", STEP, 380, 120, 100, 40)
        res = self.run_lint(mxfile(page("p1", cells)), ["overflow"])
        self.assertEqual(self.cells_hit(res, "overflow"), {"a"})
        # 同樣字數的半形字比較窄，放得下
        cells[1] = v("a", "abc", STEP, 380, 120, 100, 40)
        self.assertTrue(self.run_lint(mxfile(page("p1", cells)), ["overflow"])["ok"])

    def test_dangling(self):
        cells = flow_cells() + [v("lone", "孤單的步驟", STEP, 380, 600)]
        res = self.run_lint(mxfile(page("p1", cells)), ["dangling"])
        self.assertEqual(self.cells_hit(res, "dangling"), {"lone"})

    def test_dangling_skips_non_flow_page(self):
        cells = [v("x", "最小單元", STEP, 40, 40)] + legend()
        self.assertTrue(self.run_lint(mxfile(page("p1", cells)), ["dangling"])["ok"])

    def test_decision_needs_two_edges(self):
        cells = flow_cells() + [e("e5", "d", "a", "再試")]
        res = self.run_lint(mxfile(page("p1", cells)), ["decision"])
        self.assertEqual(self.cells_hit(res, "decision"), {"d"})

    def test_decision_needs_yes_no(self):
        cells = [c.replace('value="否"', 'value="不相符"') for c in flow_cells()]
        res = self.run_lint(mxfile(page("p1", cells)), ["decision"])
        self.assertEqual(self.cells_hit(res, "decision"), {"d"})

    def test_endcolor_text_vs_fill(self):
        cells = [c.replace('value="結束碼 1"', 'value="結束碼 0"') for c in flow_cells()]
        res = self.run_lint(mxfile(page("p1", cells)), ["endcolor"])
        self.assertEqual(self.cells_hit(res, "endcolor"), {"ng"})

    def test_endcolor_green_with_failure_code(self):
        cells = [c.replace('value="結束碼 0"', 'value="結束碼 2"') for c in flow_cells()]
        res = self.run_lint(mxfile(page("p1", cells)), ["endcolor"])
        self.assertEqual(self.cells_hit(res, "endcolor"), {"ok"})

    def test_endcolor_unknown_ellipse_fill(self):
        cells = flow_cells() + [v("odd", "怪", GREEN.replace("#d5e8d4", "#123456"), 40, 600, 160, 50)]
        res = self.run_lint(mxfile(page("p1", cells)), ["endcolor"])
        self.assertEqual(self.cells_hit(res, "endcolor"), {"odd"})

    def test_legend_missing(self):
        cells = [c for c in flow_cells() if "_lg" not in c]
        res = self.run_lint(mxfile(page("p1", cells)), ["legend"])
        self.assertEqual(self.cells_hit(res, "legend"), {"-"})

    def test_legend_color_not_in_legend(self):
        cells = flow_cells() + [v("b", "藍", STEP.replace("#ffffff", "#dae8fc"), 40, 600)]
        res = self.run_lint(mxfile(page("p1", cells)), ["legend"])
        self.assertEqual(self.cells_hit(res, "legend"), {"b"})

    def test_legend_color_not_in_style(self):
        cells = flow_cells() + legend("q", ("#123456",))
        res = self.run_lint(mxfile(page("p1", cells)), ["legend"])
        self.assertEqual(self.cells_hit(res, "legend"), {"q_lg0"})


class TestTerm(Base):
    def test_avoid_word(self):
        cells = flow_cells()
        cells[1] = v("a", "讀專案設定", STEP, 380, 120)
        res = self.run_lint(mxfile(page("p1", cells)), ["term"])
        self.assertEqual(self.cells_hit(res, "term"), {"a"})
        self.assertIn("repo", res["violations"][0]["msg"])

    def test_page_term_table_not_in_glossary(self):
        cells = flow_cells() + [v("t_tk0", "啟動器", STEP, 40, 1000), v("t_tv0", "入口", STEP, 260, 1000),
                                v("t_tk1", "引擎（engine）", STEP, 40, 1040), v("t_tv1", "主程式", STEP, 260, 1040)]
        res = self.run_lint(mxfile(page("p1", cells)), ["term"])
        self.assertEqual(self.cells_hit(res, "term"), {"t_tk0"})

    def test_cross_page_consistency(self):
        def with_term(text):
            return flow_cells() + [v("t_tk0", "引擎", STEP, 40, 1000), v("t_tv0", text, STEP, 260, 1000)]
        xml = mxfile(page("p1", with_term("主程式")), page("p2", with_term("主程式")), page("p3", with_term("別的說法")))
        res = self.run_lint(xml, ["term"])
        self.assertEqual([(x["page"], x["cell"]) for x in res["violations"]], [("p3", "t_tk0")])

    def test_glossary_prefers_glossary_md(self):
        (self.dir / "GLOSSARY.md").write_text("**啟動器**（launcher）：\n入口。\n", encoding="utf-8")
        cells = flow_cells() + [v("t_tk0", "啟動器", STEP, 40, 1000)]
        self.assertTrue(self.run_lint(mxfile(page("p1", cells)), ["term"])["ok"])

    def test_skipped_without_glossary(self):
        with tempfile.TemporaryDirectory() as empty:
            cells = flow_cells()
            cells[1] = v("a", "讀專案設定", STEP, 380, 120)
            res = self.run_lint(mxfile(page("p1", cells)), ["term"], root=empty)
        self.assertTrue(res["ok"])
        self.assertEqual([s["rule"] for s in res["skipped"]], ["term"])


class TestPageId(Base):
    def test_id_changed_against_base(self):
        base = mxfile(page("p1", flow_cells(), "流程"), page("p2", flow_cells(), "另一頁"))
        now = mxfile(page("p1-new", flow_cells(), "流程"), page("p2", flow_cells(), "另一頁改名"))
        res = self.run_lint(now, ["page-id"], base)
        self.assertEqual([x["page"] for x in res["violations"]], ["p1-new"])

    def test_rename_and_reorder_keep_id(self):
        base = mxfile(page("p1", flow_cells(), "甲"), page("p2", flow_cells(), "乙"))
        now = mxfile(page("p2", flow_cells(), "乙二"), page("p1", flow_cells(), "甲二"))
        self.assertTrue(self.run_lint(now, ["page-id"], base)["ok"])

    def test_missing_page(self):
        base = mxfile(page("p1", flow_cells()), page("p2", flow_cells()))
        res = self.run_lint(mxfile(page("p1", flow_cells())), ["page-id"], base)
        self.assertEqual([x["page"] for x in res["violations"]], ["p2"])

    def test_duplicate_id(self):
        res = self.run_lint(mxfile(page("p1", flow_cells(), "甲"), page("p1", flow_cells(), "乙")), ["page-id"])
        self.assertEqual(self.rules_hit(res), {"page-id"})


class TestCli(Base):
    def call(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = lint.main([str(a) for a in argv])
        out = buf.getvalue()
        self.assertEqual(out.count("\n"), 1, out)
        return rc, json.loads(out)

    def test_exit_codes(self):
        good = self.write("good.drawio", mxfile(page("p1", flow_cells())))
        rc, out = self.call(good, "--repo-root", self.dir)
        self.assertEqual((rc, out["ok"]), (0, True))
        bad = self.write("bad.drawio", mxfile(page("p1", flow_cells() + [v("lone", "孤單", STEP, 380, 600)])))
        rc, out = self.call(bad, "--repo-root", self.dir, "--rules", "dangling")
        self.assertEqual(rc, 1)
        self.assertEqual(out["rules"], ["dangling"])
        self.assertEqual(set(out["violations"][0]), {"page", "cell", "rule", "msg"})

    def test_usage_errors(self):
        good = self.write("good.drawio", mxfile(page("p1", flow_cells())))
        self.assertEqual(self.call(good, "--rules", "nope")[0], 2)
        self.assertEqual(self.call(self.dir / "missing.drawio")[0], 2)
        notdrawio = self.write("x.drawio", "<html/>")
        self.assertEqual(self.call(notdrawio)[0], 2)
        self.assertEqual(self.call()[0], 2)


if __name__ == "__main__":
    unittest.main()
