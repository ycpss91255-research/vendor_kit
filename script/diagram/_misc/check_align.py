import re, sys, html
x = open('../../../dist_distribution.drawio', encoding='utf-8').read()
for m in re.finditer(r'<diagram id="([^"]+)" name="([^"]+)">(.*?)</diagram>', x, re.S):
    pid, name, body = m.groups()
    cells = {}
    for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*)>(.*?)</mxCell>|<mxCell id="([^"]+)"([^>]*)/>', body, re.S):
        cid = c.group(1) or c.group(4); attrs = c.group(2) or c.group(5) or ""; inner = c.group(3) or ""
        g = re.search(r'<mxGeometry ([^>]*)/?>', inner)
        geo = dict(re.findall(r'(\w+)="([^"]*)"', g.group(1))) if g else {}
        cells[cid] = dict(attrs=dict(re.findall(r'(\w+)="([^"]*)"', attrs)), geo=geo, inner=inner)
    def absbox(cid):
        c = cells[cid]; g = c['geo']
        x0, y0, w, h = float(g.get('x',0)), float(g.get('y',0)), float(g.get('width',0)), float(g.get('height',0))
        p = c['attrs'].get('parent')
        while p and p not in ('0','1'):
            pg = cells[p]['geo']; x0 += float(pg.get('x',0)); y0 += float(pg.get('y',0)); p = cells[p]['attrs'].get('parent')
        return x0, y0, w, h
    issues = []
    for cid, c in cells.items():
        a = c['attrs']
        if a.get('edge') != '1' or 'points' in c['inner']: continue
        st = dict(kv.split('=',1) for kv in a.get('style','').split(';') if '=' in kv)
        if not all(k in st for k in ('exitX','exitY','entryX','entryY')):
            sx, sy, sw, sh = absbox(a['source']); tx, ty, tw, th = absbox(a['target'])
            scx, scy, tcx, tcy = sx+sw/2, sy+sh/2, tx+tw/2, ty+th/2
            if abs(scx-tcx) > 1 and abs(scx-tcx) < 60 and abs(scy-tcy) > 40: issues.append(f"{cid}: 自動路徑，中心左右差 {scx-tcx:+.0f}px（{a['source']}→{a['target']}）")
            if abs(scy-tcy) > 1 and abs(scy-tcy) < 60 and abs(scx-tcx) > 40: issues.append(f"{cid}: 自動路徑，中心高度差 {scy-tcy:+.0f}px（{a['source']}→{a['target']}）")
            continue
        sx, sy, sw, sh = absbox(a['source']); tx, ty, tw, th = absbox(a['target'])
        ex, ey = sx + float(st['exitX'])*sw, sy + float(st['exitY'])*sh
        nx, ny = tx + float(st['entryX'])*tw, ty + float(st['entryY'])*th
        horiz = float(st['exitX']) in (0,1) and float(st['entryX']) in (0,1)
        vert = float(st['exitY']) in (0,1) and float(st['entryY']) in (0,1)
        if horiz and abs(ey-ny) > 1 and abs(ey-ny) < 60: issues.append(f"{cid}: 水平線高度差 {ey-ny:+.0f}px（{a['source']}→{a['target']}）")
        if vert and abs(ex-nx) > 1 and abs(ex-nx) < 60: issues.append(f"{cid}: 垂直線左右差 {ex-nx:+.0f}px（{a['source']}→{a['target']}）")
    print(f"== {html.unescape(name)}"); [print("  ", i) for i in issues] or print("   無")
