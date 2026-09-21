import sys
from drawio_common import load, absbox, vertices
path, pid = sys.argv[1:3]
for p, name, cells in load(path):
    if p != pid: continue
    rows = []
    for c in vertices(cells):
        x, y, w, h = absbox(cells, c['id'])
        if c['attrs'].get('parent') in ('1',) or True:
            rows.append((round(y), round(h), c['id'], c['value'][:30]))
    rows.sort()
    for r in rows:
        if not r[2].endswith('_v2'): print(r)
