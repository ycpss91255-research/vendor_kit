"""（b 檔專用）列出某頁 band 內每列（依 y 分組）的高度與最高格。用法：python3 r11b_rows.py <pid>"""
import sys, re
from drawio_common import load, absbox, vertices
pid = sys.argv[1]
for p, name, cells in load("v1_b.drawio"):
    if p != pid: continue
    rows = {}
    for c in vertices(cells):
        cid = c['id']; par = c['attrs'].get('parent')
        if par in ('0', '1') or cid.endswith('_v2') or re.search(r'_\d+$', cid): continue
        if cells[par]['shape'] != 'swimlane': continue
        x, y, w, h = absbox(cells, cid)
        rows.setdefault(round(y / 10), []).append((cid, int(h), int(w)))
    tot = 0
    for y in sorted(rows):
        items = sorted(rows[y], key=lambda t: -t[1]); tot += items[0][1]
        print(f"y≈{y*10:5d} h={items[0][1]:4d}  " + "  ".join(f"{i}({h},{w})" for i, h, w in items))
    print("列高總和", tot, "列數", len(rows))
