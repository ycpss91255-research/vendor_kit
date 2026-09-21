"""r15：md 定稿版 vs chk_a 抽取文字，雙向逐字比對。
正向：md 正文每個片段（表格格、列點、段落、節標題）都要在圖上一字不差出現（terms.md 到「## 附錄」為止；01 到「## 出處對照」為止）。
反向：圖上每一行（頁標題除外）都要能在 md 文字裡找到。"""
import json, re, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "chk_a"
norm = lambda s: s.replace("`", "").replace("**", "").strip()
def md_frags(path, stop):
    txt = open(path, encoding="utf-8").read().split(stop)[0]
    out = []
    for ln in txt.splitlines():
        s = ln.strip()
        if not s or s == "---": continue
        if s.startswith("#"):
            t = s.lstrip("#").strip()
            if t.startswith("審閱頁 0"): continue          # md 檔標題（圖上是帶拆頁副標的頁標題）
            out.append(t); continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r"-+", c) for c in cells): continue
            out += cells
        elif s.startswith("- "): out.append(s[2:])
        else: out.append(s)
    return [norm(f) for f in out], norm(txt)
def page_lines(pid):
    d = json.load(open(f"{OUT}/{pid}.json"))
    out = []
    for n in d["nodes"]:
        for l in n["text"].split("⏎"):
            if l.strip(): out.append((n["id"], n["cls"], l.strip()))
    return out
total_miss = total_extra = 0
for mdp, stop, pages in (("decisions/review/terms.md", "## 附錄", ["v1p0"]),
                         ("decisions/review/invariants_roles.md", "## 出處對照", ["v1p1", "v1p1i"])):
    frags, mdtxt = md_frags(mdp, stop)
    lines = [x for p in pages for x in page_lines(p)]
    have = {l for _, _, l in lines}
    # v1p1 本頁名詞：md 是「名詞：定義」一列，圖上拆兩格 → 接回
    d = {}
    for pid_, cls, l in lines: pass
    for p in pages:
        rows = {}
        for n in json.load(open(f"{OUT}/{p}.json"))["nodes"]:
            m = re.match(r"p1_tm_r(\d+)c(\d)$", n["id"])
            if m: rows.setdefault(int(m.group(1)), {})[int(m.group(2))] = n["text"].strip()
        have |= {r[0] + "：" + r[1] for r in rows.values()}
    miss = [f for f in frags if f not in have]
    extra = [(i, l) for i, cls, l in lines if cls != "TITLE" and l not in mdtxt]
    total_miss += len(miss); total_extra += len(extra)
    print(f"{mdp} ↔ {pages}: md 片段 {len(frags)}、圖上行 {len(lines)}；md 有圖沒有 {len(miss)}；圖有 md 沒有 {len(extra)}")
    for m in miss: print("  MISSING:", m[:120])
    for i, l in extra: print("  EXTRA:", i, l[:120])
print("差異合計:", total_miss + total_extra)
