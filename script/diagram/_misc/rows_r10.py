"""列出某頁各格 y／h（分組內相對 → 絕對），依 y 排序，找出撐高列的格子。用法: python3 rows_r10.py <pid>"""
import sys, html
from drawio_common import load, absbox, vertices
from check_overflow import strip_tags
pid = sys.argv[1]
for p, name, cells in load("v1_b.drawio"):
    if p != pid: continue
    rows = []
    for c in vertices(cells):
        if c['id'].endswith('_v2') or c['id'].startswith('hdr') or c['id'] in ('title', 'pend'): continue
        par = c['attrs'].get('parent')
        if par in ('0', '1') and not c['id'].startswith(('p', 'c_', 'cx')): pass
        x, y, w, h = absbox(cells, c['id'])
        rows.append((round(y), round(h), round(x), c['id'], strip_tags(c['value'])[:28].replace('\n', ' ')))
    rows.sort()
    for r in rows: print(f"y={r[0]:5d} h={r[1]:4d} x={r[2]:5d} {r[3]:10s} {r[4]}")
