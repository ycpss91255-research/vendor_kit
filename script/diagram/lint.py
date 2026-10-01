#!/usr/bin/env python3
"""圖的 lint：一次跑完 .drawio 的機械檢查（#138）。

用法：
  python3 script/diagram/lint.py <file.drawio> [--base <old.drawio>] [--rules a,b]

規則（--rules 用這些名字，逗號分隔；不給就全跑）：
  overlap   壓線：線穿過不相干的方塊（沿用 check_overlap.check）
  overflow  溢字：文字超出方塊、橢圓或菱形（沿用 check_overflow.check 的字寬估算）
  dangling  懸空：流程頁的步驟與判斷沒有進線或出線；終點沒有進線；跨頁出入口少了該有的線
  decision  判斷：菱形出線不是兩條，或兩條沒有分別標「是」「否」
  endcolor  終點顏色：橢圓底色不是 STYLE.md 的終點色；文字寫結束碼 0 卻不是綠、寫非 0 卻是綠；
            紅終點寫了要人動手的字眼（請、手動、重跑）就該用橙
  term      名詞：文字用了名詞表 _Avoid_ 的說法；本頁名詞表的名詞不在名詞表；
            同一名詞在各頁的寫法或定義不一致。名詞表讀 repo 根目錄 GLOSSARY.md，沒有就讀 CONTEXT.md，
            都沒有就跳過，在輸出的 skipped 標出來
  legend    圖例：每頁要有圖例（id 依 STYLE.md 3.1：<前綴>_lg<n>／_lgt／_lgx_<鍵>）；
            頁上的底色只能是圖例裡有的；圖例的底色要是 STYLE.md 定義過的
  page-id   頁 id：同一檔內 <diagram id> 不准重複或缺；給 --base 時，舊檔每頁的 id 在新檔都要還在

流程頁 = 頁上有非圖例的菱形或終點／出入口橢圓（STYLE.md：菱形只出現在流程頁）。
讀未壓縮與壓縮（base64＋deflate）兩種 <diagram>；也讀 <object>／<UserObject> 包起來的格子。

輸出一行 JSON 到 stdout：
  {"ok", "file", "base", "rules", "skipped": [{"rule", "reason"}], "count",
   "violations": [{"page", "cell", "rule", "msg"}]}
page 是 <diagram id>；跨頁的違規 page 寫違規所在那頁。
結束碼：0 沒有違規；1 有違規；2 用法錯（參數錯、檔案讀不到、不是 drawio 檔）。
只用 Python 標準函式庫，只讀檔，不連 drawio 服務。
"""
import argparse
import base64
import json
import re
import sys
import urllib.parse
import zlib
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import check_overflow  # noqa: E402
import check_overlap  # noqa: E402
import extract_pages  # noqa: E402

REPO_ROOT = HERE.parents[1]
STYLE_MD = HERE / "STYLE.md"

RULES = ["overlap", "overflow", "dangling", "decision", "endcolor", "term", "legend", "page-id"]

LEGEND_ID_RE = re.compile(r"_lg\d+$|_lgt$|_lgx_")
NO_FILL = {"none", "-", "", "#ffffff", "default"}
END_KINDS = ("end_ok", "end_orange", "end_red")
FLOW_KINDS = ("decision",) + END_KINDS + ("entry",)
END_OK_TEXT = re.compile(r"(?:→|結束碼)\s*0(?!\d)|^0：")
END_FAIL_TEXT = re.compile(r"(?:→|結束碼)\s*[1-9]|^[1-9]：")
NEEDS_HUMAN = ("請", "手動", "重跑")
TERM_NAME_RE = re.compile(r"_tk(\d+)$")
TERM_DEF_RE = re.compile(r"_tv(\d+)$")


class UsageError(Exception):
    pass


# ---------------------------------------------------------------- 讀檔

def _diagram_root(d):
    """<diagram> → <mxGraphModel> 元素；壓縮的先解開。"""
    model = d.find("mxGraphModel")
    if model is not None:
        return model
    text = (d.text or "").strip()
    if not text:
        return None
    try:
        raw = zlib.decompress(base64.b64decode(text), -15)
        return ET.fromstring(urllib.parse.unquote(raw.decode("utf-8")))
    except Exception as e:  # noqa: BLE001
        raise UsageError(f"頁 {d.get('id')} 的內容解不開：{e}")


def _cells(model):
    """依文件順序回傳 [(id, attrs, mxCell 元素)]；<object>／<UserObject> 的 id 與 label 搬到格子上。"""
    out = []
    root = model.find("root")
    if root is None:
        return out
    for el in root:
        if el.tag == "mxCell":
            out.append((el.get("id"), dict(el.attrib), el))
        elif el.tag in ("object", "UserObject"):
            cell = el.find("mxCell")
            if cell is None:
                continue
            a = dict(cell.attrib)
            a["id"] = el.get("id")
            a["value"] = el.get("label", "")
            out.append((el.get("id"), a, cell))
    return out


def _geo_points(cell):
    g = cell.find("mxGeometry")
    if g is None:
        return {}, []
    pts = []
    arr = g.find("Array[@as='points']")
    if arr is not None:
        for p in arr.findall("mxPoint"):
            pts.append((float(p.get("x", 0)), float(p.get("y", 0))))
    return dict(g.attrib), pts


def load(path):
    """回傳 [Page]；Page = dict(id, name, common, extract, order)。
    common 是 drawio_common.load 的格子結構（給 check_overlap／check_overflow），
    extract 是 extract_pages.load 的格子結構（給 extract_pages.extract）。"""
    try:
        tree = ET.parse(path)
    except (OSError, ET.ParseError) as e:
        raise UsageError(f"讀不到 {path}：{e}")
    root = tree.getroot()
    if root.tag != "mxfile":
        raise UsageError(f"{path} 不是 drawio 檔（根元素是 <{root.tag}>）")
    pages = []
    for d in root.findall("diagram"):
        model = _diagram_root(d)
        common, extract, order = {}, {}, []
        for cid, a, cell in (_cells(model) if model is not None else []):
            if cid is None:
                continue
            geo, pts = _geo_points(cell)
            style = a.get("style", "")
            st = dict(kv.split("=", 1) for kv in style.split(";") if "=" in kv)
            head = style.split(";")[0]
            value = a.get("value", "")
            common[cid] = dict(id=cid, attrs=a, style=st, shape=head, geo=geo, inner="", points=pts, value=value)
            extract[cid] = dict(id=cid, attrs=a, style=style, st=st, head=head, geo=geo, points=pts,
                                raw_value=escape(value, {'"': "&quot;"}))
            order.append(cid)
        pages.append(dict(id=d.get("id"), name=d.get("name", ""), common=common, extract=extract, order=order))
    return pages


# ---------------------------------------------------------------- 名詞表與 STYLE

def _norm(s):
    return re.sub(r"\s+", "", s).replace("`", "")


def term_key(s):
    """比對鍵：去空白與反引號、去掉結尾一組括號（「引擎（engine）」→「引擎」）。"""
    return re.sub(r"[（(][^（）()]*[）)]$", "", _norm(s))


def load_glossary(repo_root):
    """回傳 (來源檔名, {名詞鍵}, {避免詞: 名詞})；都沒有回 (None, None, None)。"""
    for name in ("GLOSSARY.md", "CONTEXT.md"):
        p = Path(repo_root) / name
        if p.is_file():
            break
    else:
        return None, None, None
    terms, avoid, last = set(), {}, None
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\*\*(.+?)\*\*(?:[（(]([^）)]+)[）)])?\s*[：:]", ln)
        if m:
            last = m.group(1).replace("`", "").strip()
            terms.add(term_key(last))
            if m.group(2):
                terms.add(term_key(m.group(2)))
            continue
        if ln.startswith("_Avoid_:") and last:
            for w in re.split(r"[、,，]", ln[len("_Avoid_:"):]):
                w = w.strip().strip("`").strip()
                if w:
                    avoid[w] = last
    return name, terms, avoid


def style_palette(style_md=STYLE_MD):
    """STYLE.md 裡出現過的底色（小寫）；檔不在回 None。"""
    try:
        text = Path(style_md).read_text(encoding="utf-8")
    except OSError:
        return None
    return {c.lower() for c in re.findall(r"#[0-9A-Fa-f]{6}\b", text)}


# ---------------------------------------------------------------- 規則

def _fill(n):
    return (n.get("fill") or "-").lower()


def _short(t, n=30):
    t = t.replace("⏎", " ")
    return t[:n] + ("…" if len(t) > n else "")


def _graph(d):
    byid = {n["id"]: n for n in d["nodes"]}
    ins, outs = defaultdict(list), defaultdict(list)
    for e in d["edges"]:
        if e.get("hidden") or e["source"] not in byid or e["target"] not in byid:
            continue
        outs[e["source"]].append(e)
        ins[e["target"]].append(e)
    return byid, ins, outs


def is_flow_page(d):
    return any(n["kind"] in FLOW_KINDS and not n["legend"] for n in d["nodes"])


def rule_overlap(page, d, add):
    for s in check_overlap.check(page["common"]):
        add("overlap", s.split(" ", 1)[0], s)


def rule_overflow(page, d, add):
    for s in check_overflow.check(page["common"]):
        cid, _, msg = s.partition(": ")
        add("overflow", cid, msg)


def rule_dangling(page, d, add):
    if not is_flow_page(d):
        return
    byid, ins, outs = _graph(d)
    for n in d["nodes"]:
        if n["legend"]:
            continue
        k, i, o = n["kind"], len(ins[n["id"]]), len(outs[n["id"]])
        t = _short(n["text"])
        if k in ("step", "decision"):
            miss = [w for w, c in (("進線", i), ("出線", o)) if c == 0]
            if miss:
                add("dangling", n["id"], f"{'步驟' if k == 'step' else '判斷'}沒有{'也沒有'.join(miss)}：「{t}」")
        elif k in ("end_orange", "end_red") and i == 0:
            add("dangling", n["id"], f"終點沒有進線：「{t}」")
        elif k == "end_ok" and i == 0 and o == 0:
            add("dangling", n["id"], f"起點／終點沒有任何線：「{t}」")
        elif k == "entry":
            if "續「" in n["text"] and "來自" not in n["text"]:
                if i == 0:
                    add("dangling", n["id"], f"出口沒有進線：「{t}」")
            elif o == 0:
                add("dangling", n["id"], f"入口沒有出線：「{t}」")


def rule_decision(page, d, add):
    byid, ins, outs = _graph(d)
    for n in d["nodes"]:
        if n["kind"] != "decision" or n["legend"]:
            continue
        o = outs[n["id"]]
        t = _short(n["text"])
        if len(o) != 2:
            add("decision", n["id"], f"菱形出線 {len(o)} 條，要剛好 2 條：「{t}」")
            continue
        heads = sorted(e["label"].replace("⏎", " ").strip()[:1] for e in o)
        if heads != ["否", "是"]:
            labels = "、".join(f"「{e['label'] or '(無標籤)'}」" for e in o)
            add("decision", n["id"], f"菱形兩條出線要分別標「是」「否」，現在是 {labels}：「{t}」")


def rule_endcolor(page, d, add):
    green, red, orange = (c.lower() for c in (extract_pages.GREEN, extract_pages.RED, extract_pages.ORANGE))
    for n in d["nodes"]:
        if n["legend"] or (n["shape"] != "ellipse" and "shape=ellipse" not in n.get("_style", "")):
            continue
        k, t = n["kind"], n["text"]
        if k == "other":
            add("endcolor", n["id"], f"橢圓底色 {n['fill']} 不是終點色（綠 {green}、紅 {red}、橙 {orange}）或跨頁出入口（白虛線）：「{_short(t)}」")
            continue
        if k not in END_KINDS:
            continue
        if END_OK_TEXT.search(t) and k != "end_ok":
            add("endcolor", n["id"], f"文字寫結束碼 0，終點卻不是綠：「{_short(t)}」")
        elif END_FAIL_TEXT.search(t) and k == "end_ok":
            add("endcolor", n["id"], f"文字寫非 0 結束碼，終點卻是綠：「{_short(t)}」")
        elif k == "end_red" and any(w in t for w in NEEDS_HUMAN):
            add("endcolor", n["id"], f"紅終點寫了要人動手的字眼，需人處理用橙：「{_short(t)}」")


def page_terms(d):
    """本頁名詞表：[(名詞格 id, 名詞, 定義)]，以 <前綴>_tk<i>／_tv<i> 配對。"""
    names, defs = {}, {}
    for n in d["nodes"]:
        m = TERM_NAME_RE.search(n["id"])
        if m:
            names[(n["id"][:m.start()], m.group(1))] = n
        m = TERM_DEF_RE.search(n["id"])
        if m:
            defs[(n["id"][:m.start()], m.group(1))] = n["text"]
    return [(n["id"], n["text"], defs.get(k, "")) for k, n in sorted(names.items())]


def rule_term_page(page, d, add, glossary):
    _, terms, avoid = glossary
    texts = [(n["id"], n["text"]) for n in d["nodes"] if not n["legend"]]
    texts += [(e["id"], e["label"]) for e in d["edges"]]
    for cid, text in texts:
        for w, canon in avoid.items():
            if w in text:
                add("term", cid, f"「{w}」是名詞表要避免的說法，改用「{canon}」：「{_short(text)}」")
    for cid, name, _ in page_terms(d):
        if name and term_key(name) not in terms:
            add("term", cid, f"本頁名詞「{name}」不在名詞表")


def rule_term_cross(extracted, add):
    """同一名詞（比對鍵相同）在各頁的寫法與定義要一致；少數版本逐頁報。"""
    by = defaultdict(lambda: defaultdict(list))  # key -> (名詞, 定義) -> [(page, cell)]
    for pid, d in extracted:
        for cid, name, text in page_terms(d):
            if name:
                by[term_key(name)][(name, _norm(text))].append((pid, cid))
    for key, variants in by.items():
        if len(variants) < 2:
            continue
        ranked = sorted(variants.items(), key=lambda kv: -len(kv[1]))
        (base_name, _), base_at = ranked[0]
        for (name, _), where in ranked[1:]:
            what = "寫法" if name != base_name else "定義"
            for pid, cid in where:
                add(pid, "term", cid, f"名詞「{name}」的{what}跟其他頁（{base_at[0][0]} 等 {len(base_at)} 處）不一致")


def rule_legend(page, d, add, palette):
    legend = {_fill(n) for n in d["nodes"] if n["legend"]}
    if not any(n["legend"] for n in d["nodes"]):
        add("legend", "-", "這頁沒有圖例（STYLE.md 3：每頁都要有圖例；圖例格 id 是 <前綴>_lg<n>）")
        return
    bad = defaultdict(list)
    for n in d["nodes"]:
        if n["legend"] or n["cls"] == "TAG":
            continue
        f = _fill(n)
        if f not in NO_FILL and f not in legend:
            bad[f].append(n["id"])
    for f, ids in bad.items():
        for cid in ids:
            add("legend", cid, f"底色 {f} 不在這頁的圖例")
    if palette is not None:
        for n in d["nodes"]:
            f = _fill(n)
            if n["legend"] and f not in NO_FILL and f not in palette:
                add("legend", n["id"], f"圖例的底色 {f} 不是 STYLE.md 定義的顏色")


def rule_page_id(pages, base_pages, add_page):
    seen = defaultdict(int)
    for p in pages:
        if not p["id"]:
            add_page("-", "page-id", "-", f"頁「{p['name']}」沒有 <diagram id>")
        else:
            seen[p["id"]] += 1
    for pid, c in seen.items():
        if c > 1:
            add_page(pid, "page-id", "-", f"<diagram id=\"{pid}\"> 重複 {c} 次")
    if base_pages is None:
        return
    now = {p["id"]: p for p in pages if p["id"]}
    base_ids = {p["id"] for p in base_pages if p["id"]}
    for bp in base_pages:
        if not bp["id"] or bp["id"] in now:
            continue
        renamed = [p["id"] for p in pages if p["name"] == bp["name"] and p["id"] not in base_ids]
        if renamed:
            add_page(renamed[0], "page-id", "-", f"頁「{bp['name']}」的 id 由 {bp['id']} 改成 {renamed[0]}；<diagram id> 不准改變")
        else:
            add_page(bp["id"], "page-id", "-", f"舊檔的頁 {bp['id']}（「{bp['name']}」）在新檔找不到：id 改了或頁被刪了")


# ---------------------------------------------------------------- 主程式

def lint(path, base=None, rules=None, repo_root=REPO_ROOT, style_md=STYLE_MD):
    rules = list(rules or RULES)
    pages = load(path)
    base_pages = load(base) if base else None
    violations, skipped = [], []

    def add_page(pid, rule, cell, msg):
        violations.append(dict(page=pid, cell=cell, rule=rule, msg=msg))

    glossary = None
    if "term" in rules:
        glossary = load_glossary(repo_root)
        if glossary[0] is None:
            skipped.append(dict(rule="term", reason="repo 根目錄沒有 GLOSSARY.md 也沒有 CONTEXT.md"))
    palette = style_palette(style_md) if "legend" in rules else None
    if "legend" in rules and palette is None:
        skipped.append(dict(rule="legend", reason="找不到 STYLE.md，只查頁內顏色對圖例，不查圖例對 STYLE.md"))

    extracted = []
    for page in pages:
        pid = page["id"] or "-"
        d = extract_pages.extract(pid, page["name"], page["extract"], page["order"])
        for n in d["nodes"]:
            n["_style"] = page["extract"][n["id"]]["style"]
        extracted.append((pid, d))

        def add(rule, cell, msg, _pid=pid):
            add_page(_pid, rule, cell, msg)

        if "overlap" in rules:
            rule_overlap(page, d, add)
        if "overflow" in rules:
            rule_overflow(page, d, add)
        if "dangling" in rules:
            rule_dangling(page, d, add)
        if "decision" in rules:
            rule_decision(page, d, add)
        if "endcolor" in rules:
            rule_endcolor(page, d, add)
        if glossary and glossary[0]:
            rule_term_page(page, d, add, glossary)
        if "legend" in rules:
            rule_legend(page, d, add, palette)
    if glossary and glossary[0]:
        rule_term_cross(extracted, add_page)
    if "page-id" in rules:
        rule_page_id(pages, base_pages, add_page)
    return dict(ok=not violations, file=str(path), base=str(base) if base else None, rules=rules,
                skipped=skipped, count=len(violations), violations=violations)


def parse_rules(s):
    if s is None:
        return list(RULES)
    want = [r.strip() for r in s.split(",") if r.strip()]
    unknown = [r for r in want if r not in RULES]
    if unknown or not want:
        raise UsageError(f"不認得的規則：{', '.join(unknown) or '(空)'}；可用 {', '.join(RULES)}")
    return [r for r in RULES if r in want]


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def main(argv=None):
    p = _Parser(description="圖的 lint（#138）")
    p.add_argument("file")
    p.add_argument("--base", help="舊版 .drawio；給了才比對每頁 <diagram id>")
    p.add_argument("--rules", help="只跑這些規則，逗號分隔：" + ",".join(RULES))
    p.add_argument("--repo-root", default=str(REPO_ROOT), help="讀名詞表的 repo 根目錄（預設本 repo）")
    try:
        a = p.parse_args(argv)
        res = lint(a.file, a.base, parse_rules(a.rules), repo_root=a.repo_root)
    except UsageError as e:
        print(json.dumps(dict(ok=False, error=str(e)), ensure_ascii=False))
        return 2
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
