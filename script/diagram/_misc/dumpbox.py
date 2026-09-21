"""python3 dumpbox.py file page id..."""
import sys, re
from drawio_common import load, absbox, edges
from check_overlap import endpoint
path, pid = sys.argv[1], sys.argv[2]; ids = sys.argv[3:]
for p, name, cells in load(path):
    if p != pid: continue
    for i in ids:
        c = cells.get(i)
        if not c: print(i, "MISSING"); continue
        if c['attrs'].get('edge') == '1':
            a = c['attrs']; st = c['style']
            pts = [endpoint(cells, a['source'], 'exitX', 'exitY', st)] + c['points'] + [endpoint(cells, a['target'], 'entryX', 'entryY', st)]
            print(i, a['source'], '->', a['target'], [(round(x), round(y)) for x, y in pts])
        else:
            x, y, w, h = absbox(cells, i); print(i, f"x={x:.0f} y={y:.0f} w={w} h={h} right={x+w:.0f} bottom={y+h:.0f}")
