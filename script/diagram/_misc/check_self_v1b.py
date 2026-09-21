"""自檢：檔案／規則框右緣距父分組框 ≥ 20；線標籤寬 < 兩端距離；頁高 ≤ 2400；線不穿分組標題列。用法: python3 check_self_v1b.py v1_b.drawio"""
import re, sys, math
from drawio_common import load, absbox, vertices, edges
from check_overlap import endpoint, routes, seg_hits
from check_overflow import cw, strip_tags
x = open(sys.argv[1], encoding="utf-8").read(); total = 0
heights = dict(re.findall(r'<diagram id="([^"]+)" name="[^"]*"><mxGraphModel[^>]*pageHeight="(\d+)"', x))
for pid, name, cells in load(sys.argv[1]):
    iss = []
    if int(heights[pid]) > 2400: iss.append(f"頁高 {heights[pid]} > 2400")
    for c in vertices(cells):
        par = c['attrs'].get('parent')
        if par in ('0', '1') or c['id'].endswith('_v2'): continue
        pc = cells[par]
        if pc['shape'] != 'swimlane': continue
        px, py, pw, ph = absbox(cells, par); cx, cy, cw_, ch = absbox(cells, c['id'])
        m = px + pw - (cx + cw_)
        if m < 20: iss.append(f"{c['id']}: 右緣距分組框 {m:.0f} < 20")
    for ed in edges(cells):
        a = ed['attrs']; st = ed['style']; lab = strip_tags(ed['value'])
        if not lab.strip() or 'source' not in a: continue
        p = endpoint(cells, a['source'], 'exitX', 'exitY', st); q = endpoint(cells, a['target'], 'entryX', 'entryY', st)
        dist = math.hypot(p[0] - q[0], p[1] - q[1])
        w = max(sum(cw(ch, 12) for ch in ln) for ln in lab.split('\n'))
        if w >= dist: iss.append(f"{ed['id']}: 標籤寬 {w:.0f} ≥ 兩端距離 {dist:.0f}「{lab}」")
    # 線不穿標題列（swimlane startSize）與泳道表頭 hdr*
    for ed in edges(cells):
        a = ed['attrs']; st = ed['style']
        if 'source' not in a: continue
        pts = [endpoint(cells, a['source'], 'exitX', 'exitY', st)] + ed['points'] + [endpoint(cells, a['target'], 'entryX', 'entryY', st)]
        for vtx in vertices(cells):
            if vtx['shape'] == 'swimlane' or vtx['id'].startswith('hdr'):
                bx, by, bw, bh = absbox(cells, vtx['id'])
                r = (bx, by, bw, float(vtx['style'].get('startSize', 23)) if vtx['shape'] == 'swimlane' else bh)
                if any(seg_hits(pp, qq, r) for pp, qq, _ in routes(pts)): iss.append(f"{ed['id']} 穿過標題列 {vtx['id']}")
    total += len(iss); print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
print(f"共 {total} 筆")
