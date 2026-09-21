"""自檢：(1) 有父容器的 vertex 右緣距父框右緣 ≥ 20；(2) 有文字的直線（無轉折點、線上文字）最寬行 < 兩端距離。"""
import sys, re, unicodedata
from drawio_common import load, absbox, vertices, edges, args
from check_overflow import strip_tags
def tw(s, fs=12): return sum(fs if unicodedata.east_asian_width(c) in ('W','F') else 0.6*fs for c in s)
path, pages = args(); total = 0
for pid, name, cells in load(path):
    if pages and pid not in pages: continue
    iss = []
    for c in vertices(cells):
        p = c['attrs'].get('parent')
        if p in ('0','1') or p not in cells: continue
        if c['id'].endswith('_v2'): continue
        x, y, w, h = absbox(cells, c['id']); px, py, pw, ph = absbox(cells, p)
        m = px + pw - (x + w)
        if m < 20: iss.append(f"{c['id']}: 右緣距父框 {m:.0f}px（父 {p}）")
    for ed in edges(cells):
        lab = strip_tags(ed['value']).strip()
        if not lab or ed['points']: continue
        st = ed['style']; a = ed['attrs']
        side = st.get('verticalAlign') == 'middle'   # 線側文字不算
        if side: continue
        sx, sy, sw, sh = absbox(cells, a['source']); tx, ty, tw_, th = absbox(cells, a['target'])
        ex, ey = sx + float(st.get('exitX', .5))*sw, sy + float(st.get('exitY', .5))*sh
        nx, ny = tx + float(st.get('entryX', .5))*tw_, ty + float(st.get('entryY', .5))*th
        dist = max(abs(ex-nx), abs(ey-ny)); L = max(tw(l) for l in lab.split('\n'))
        if L >= dist: iss.append(f"{ed['id']}: 標籤 {L:.0f}px ≥ 兩端距離 {dist:.0f}px「{lab[:20]}」")
    total += len(iss); print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
print(f"共 {total} 筆")
