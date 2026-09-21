"""線與線是否交叉（正交折線；共點／共線接合不算）。用法: python3 check_cross_v1b.py <file.drawio>"""
import sys
from drawio_common import load, absbox, edges, args
from check_overlap import endpoint
def polyline(cells, ed):
    a = ed['attrs']; st = ed['style']
    return [endpoint(cells, a['source'], 'exitX', 'exitY', st)] + ed['points'] + [endpoint(cells, a['target'], 'entryX', 'entryY', st)]
def cross(p, q, r, s):
    """p→q 與 r→s 是否在內部交叉（一垂一橫）。"""
    def vert(a, b): return abs(a[0]-b[0]) < 1e-6
    if vert(p, q) == vert(r, s): return False
    if not vert(p, q): p, q, r, s = r, s, p, q
    x = p[0]; y = r[1]
    return min(r[0], s[0]) + 1 < x < max(r[0], s[0]) - 1 and min(p[1], q[1]) + 1 < y < max(p[1], q[1]) - 1
path, pages = args(); total = 0
for pid, name, cells in load(path):
    if pages and pid not in pages: continue
    E = [(ed['id'], polyline(cells, ed)) for ed in edges(cells) if 'source' in ed['attrs']]
    iss = []
    for i in range(len(E)):
        for j in range(i+1, len(E)):
            for a, b in zip(E[i][1], E[i][1][1:]):
                for c, d in zip(E[j][1], E[j][1][1:]):
                    if cross(a, b, c, d): iss.append(f"{E[i][0]} × {E[j][0]} at ({a},{b}) / ({c},{d})")
    total += len(iss); print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
print(f"共 {total} 筆")
