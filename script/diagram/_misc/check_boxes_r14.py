"""方塊互相重疊（同頁、非父子、排除 v2 小標／tty 小標／swimlane／透明佔位）。用法: python3 check_boxes_r14.py v1_b.drawio"""
import sys
from drawio_common import load, absbox, vertices
tot = 0
for pid, name, cells in load(sys.argv[1]):
    vs = [c for c in vertices(cells) if c['shape'] != 'swimlane' and not c['id'].endswith('_v2') and not c['id'].endswith('_tty') and 'strokeColor=none' not in c['attrs'].get('style', '') and c['attrs'].get('parent') not in ('0',)]
    def anc(cid):
        out=set(); p=cells[cid]['attrs'].get('parent')
        while p and p in cells: out.add(p); p=cells[p]['attrs'].get('parent')
        return out
    iss=[]
    for i in range(len(vs)):
        for j in range(i+1, len(vs)):
            a, b = vs[i], vs[j]
            if a['id'] in anc(b['id']) or b['id'] in anc(a['id']): continue
            ax, ay, aw, ah = absbox(cells, a['id']); bx, by, bw, bh = absbox(cells, b['id'])
            if ax < bx + bw - 1 and bx < ax + aw - 1 and ay < by + bh - 1 and by < ay + ah - 1:
                iss.append(f"{a['id']} × {b['id']}")
    tot += len(iss)
    if iss: print("==", pid, name); [print("  ", x) for x in iss]
print("共", tot, "筆")
