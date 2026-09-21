"""md 定稿版 vs v1_a.drawio 頁面文字：md 正文每個片段（表格格、列點、段落）都要在圖上一字不差出現。"""
import json, re, sys
def frag_md(path, stop):
    txt = open(path, encoding="utf-8").read()
    txt = txt.split(stop)[0]
    out = []
    for ln in txt.splitlines():
        s = ln.strip()
        if not s or s.startswith("#") or s == "---": continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r"-+", c) for c in cells): continue
            out += cells
        elif s.startswith("- "): out.append(s[2:])
        elif re.match(r"^\d+\. ", s): out.append(s)
        else: out.append(s)
    norm = lambda s: s.replace("`", "").replace("**", "")
    return [norm(f) for f in out]
def page_text(outdir, pid):
    d = json.load(open(f"{outdir}/{pid}.json"))
    lines = []
    for n in d["nodes"]:
        for l in n["text"].split("⏎"): lines.append(l.strip())
    return lines
def check(mdpath, stop, pages, outdir="r14_a_out", extra_stop=None):
    frags = frag_md(mdpath, stop)
    if extra_stop: frags += extra_stop
    have = set()
    for p in pages: have |= set(page_text(outdir, p))
    miss = [f for f in frags if f not in have]
    print(f"{mdpath}: {len(frags)} 片段, 缺 {len(miss)}")
    for m in miss: print("  MISSING:", m[:120])
    return miss
m1 = check("decisions/review/00_terms.md", "## 附錄", ["v1p0", "v1p0b"])
# 附錄「寫法約定」兩條
app = open("decisions/review/00_terms.md", encoding="utf-8").read().split("### 寫法約定")[1].split("### 規則")[0]
app = [l.strip()[2:].replace("`", "").replace("**", "") for l in app.splitlines() if l.strip().startswith("- ")]
have = set(page_text("r14_a_out", "v1p0b"))
print("寫法約定 缺:", [a for a in app if a not in have])
m2 = check("decisions/review/01_invariants_roles.md", "## 出處對照", ["v1p1"])
# 反向：圖上有、md 沒有的字（排除標題／圖例／節名）
# 本頁名詞：兩欄以「：」接回後比對
d = json.load(open("r14_a_out/v1p1.json"))
rows = {}
for n in d["nodes"]:
    m = re.match(r"p1_tm_r(\d+)c(\d)$", n["id"])
    if m: rows.setdefault(int(m.group(1)), {})[int(m.group(2))] = n["text"]
joined = {r[0] + "：" + r[1] for r in rows.values()}
print("本頁名詞 接回後仍缺:", [x for x in m2 if x not in joined])
# 反向：圖上每行都要能在 md 找到（排除標題／節名／圖例）
def md_all(path):
    t = open(path, encoding="utf-8").read().replace("`", "").replace("**", "")
    return t
for pid, mdp in (("v1p0", "decisions/review/00_terms.md"), ("v1p0b", "decisions/review/00_terms.md"), ("v1p1", "decisions/review/01_invariants_roles.md")):
    md = md_all(mdp); d = json.load(open(f"r14_a_out/{pid}.json"))
    extra = []
    for n in d["nodes"]:
        if n["legend"] or n["cls"] in ("TITLE",) or n["kind"] == "header": continue
        for l in n["text"].split("⏎"):
            l = l.strip()
            if l and l not in md: extra.append((n["id"], l))
    print(pid, "圖上有、md 沒有:", extra)
