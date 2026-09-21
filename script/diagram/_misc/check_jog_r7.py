"""小折診斷：垂直—短水平(1≤dx<40)—垂直 的 z 折。"""
import sys
from drawio_common import load, edges, args
from check_overlap import endpoint
path, pages = args(); total = 0
for pid, name, cells in load(path):
    if pages and pid not in pages: continue
    for ed in edges(cells):
        a = ed['attrs']; st = ed['style']
        if 'source' not in a: continue
        pts = [endpoint(cells, a['source'], 'exitX', 'exitY', st)] + ed['points'] + [endpoint(cells, a['target'], 'entryX', 'entryY', st)]
        for i in range(len(pts) - 3):
            p, q, r, s2 = pts[i:i+4]
            if abs(p[0]-q[0]) < 1 and abs(q[1]-r[1]) < 1 and 1 <= abs(q[0]-r[0]) < 40 and abs(r[0]-s2[0]) < 1:
                print(pid, ed['id'], f"{a['source']}→{a['target']}", f"dx={abs(q[0]-r[0]):.0f}"); total += 1
print("共", total, "筆")
