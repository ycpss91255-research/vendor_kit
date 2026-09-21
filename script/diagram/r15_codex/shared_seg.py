"""共線段偵測（雙箭頭線）：兩條 edge 的折線有同向段重疊 > 8px。用法: python3 r15_codex/shared_seg.py <drawio> [pid...]"""
import sys
from drawio_common import load, edges, args
from check_cross_v1b import polyline
path, pages = args(); total = 0
for pid, name, cells in load(path):
    if pages and pid not in pages: continue
    E = [(ed['id'], polyline(cells, ed)) for ed in edges(cells) if 'source' in ed['attrs']]
    iss = []
    for i in range(len(E)):
        for j in range(i+1, len(E)):
            for a, b in zip(E[i][1], E[i][1][1:]):
                for c, d in zip(E[j][1], E[j][1][1:]):
                    va = abs(a[0]-b[0]) < 1e-6; vc = abs(c[0]-d[0]) < 1e-6
                    if va and vc and abs(a[0]-c[0]) < 1:
                        lo = max(min(a[1],b[1]), min(c[1],d[1])); hi = min(max(a[1],b[1]), max(c[1],d[1]))
                        if hi - lo > 8: iss.append(f"{E[i][0]} ∥ {E[j][0]} 垂直 x={a[0]:.0f} y {lo:.0f}–{hi:.0f}")
                    elif (not va) and (not vc) and abs(a[1]-c[1]) < 1:
                        lo = max(min(a[0],b[0]), min(c[0],d[0])); hi = min(max(a[0],b[0]), max(c[0],d[0]))
                        if hi - lo > 8: iss.append(f"{E[i][0]} ∥ {E[j][0]} 水平 y={a[1]:.0f} x {lo:.0f}–{hi:.0f}")
    total += len(iss); print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
print(f"共 {total} 筆")
