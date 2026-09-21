"""線是否壓到無關方塊。用法: python3 check_overlap.py <file.drawio> [page_id ...]
每條 edge 依 exit/entry 與 waypoints 算正交折線：相鄰兩點若不共線，兩種 L 形都算（保守）；
沒有 exit/entry 的用方塊中心。檢查每段是否穿過任何非 source/target 的 vertex 矩形
（swimlane 只算標題列；source/target 的祖先容器不算）。"""
import sys, html
from drawio_common import load, absbox, vertices, edges, args

def ancestors(cells, cid):
    out = set(); p = cells[cid]['attrs'].get('parent')
    while p and p in cells: out.add(p); p = cells[p]['attrs'].get('parent')
    return out

def obstacle_rect(cells, c):
    x, y, w, h = absbox(cells, c['id'])
    if c['shape'] == 'swimlane': h = float(c['style'].get('startSize', 23))
    return x, y, w, h

def seg_hits(p, q, r, eps=0.5):
    """正交線段 p→q 是否穿過矩形 r（內縮 eps 避免貼邊誤判）。"""
    x, y, w, h = r; x1, y1, x2, y2 = x + eps, y + eps, x + w - eps, y + h - eps
    if x1 >= x2 or y1 >= y2: return False
    (px, py), (qx, qy) = p, q
    if abs(px - qx) < 1e-6:   # 垂直
        return x1 < px < x2 and max(py, qy) > y1 and min(py, qy) < y2
    if abs(py - qy) < 1e-6:   # 水平
        return y1 < py < y2 and max(px, qx) > x1 and min(px, qx) < x2
    return False

def routes(pts):
    """相鄰點不共線 → 兩種 L 形都列出。回傳 [(seg_p, seg_q, 說明)]。"""
    segs = []
    for (a, b) in zip(pts, pts[1:]):
        if abs(a[0] - b[0]) < 1e-6 or abs(a[1] - b[1]) < 1e-6:
            segs.append((a, b, ''))
        else:
            segs.append((a, (b[0], a[1]), 'L1')); segs.append(((b[0], a[1]), b, 'L1'))
            segs.append((a, (a[0], b[1]), 'L2')); segs.append(((a[0], b[1]), b, 'L2'))
    return segs

def endpoint(cells, cid, kx, ky, st):
    x, y, w, h = absbox(cells, cid)
    if kx in st and ky in st: return x + float(st[kx]) * w, y + float(st[ky]) * h
    return x + w / 2, y + h / 2

def check(cells):
    issues = []
    verts = vertices(cells)
    for ed in edges(cells):
        a = ed['attrs']; st = ed['style']
        if 'source' not in a or 'target' not in a or a['source'] not in cells or a['target'] not in cells: continue
        s, t = a['source'], a['target']
        pts = [endpoint(cells, s, 'exitX', 'exitY', st)] + ed['points'] + [endpoint(cells, t, 'entryX', 'entryY', st)]
        skip = {s, t} | ancestors(cells, s) | ancestors(cells, t)
        for vtx in verts:
            if vtx['id'] in skip: continue
            r = obstacle_rect(cells, vtx)
            if r[2] <= 0 or r[3] <= 0: continue
            hit = [tag for p, q, tag in routes(pts) if seg_hits(p, q, r)]
            if hit:
                issues.append(f"{ed['id']} ({s}→{t}) 壓到 {vtx['id']}「{html.unescape(vtx['value'])[:20]}」 {sorted(set(hit)) or ''}")
    return issues

if __name__ == '__main__':
    path, pages = args(); total = 0
    for pid, name, cells in load(path):
        if pages and pid not in pages: continue
        iss = check(cells); total += len(iss)
        print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
    print(f"共 {total} 筆"); sys.exit(1 if total else 0)
