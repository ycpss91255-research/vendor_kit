"""check_overflow / check_overlap 共用：解析 .drawio（未壓縮 XML），給絕對座標。"""
import re, html, sys

def load(path):
    x = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<diagram id="([^"]+)" name="([^"]+)">(.*?)</diagram>', x, re.S):
        pid, name, body = m.groups()
        cells = {}
        for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*?)(?:/>|>(.*?)</mxCell>)', body, re.S):
            cid, attrs, inner = c.group(1), c.group(2) or "", c.group(3) or ""
            g = re.search(r'<mxGeometry ([^>]*)/?>', inner)
            geo = dict(re.findall(r'(\w+)="([^"]*)"', g.group(1))) if g else {}
            a = dict(re.findall(r'(\w+)="((?:[^"\\]|\\.)*)"', attrs))
            st = dict(kv.split('=', 1) for kv in a.get('style', '').split(';') if '=' in kv)
            shape = a.get('style', '').split(';')[0]
            pts = [(float(px), float(py)) for px, py in re.findall(r'<mxPoint x="([\d.-]+)" y="([\d.-]+)"(?! as="(?:offset|sourcePoint|targetPoint)")', inner)]
            cells[cid] = dict(id=cid, attrs=a, style=st, shape=shape, geo=geo, inner=inner, points=pts,
                              value=html.unescape(a.get('value', '')))
        yield pid, html.unescape(name), cells

def absbox(cells, cid):
    c = cells[cid]; g = c['geo']
    x0, y0, w, h = float(g.get('x', 0)), float(g.get('y', 0)), float(g.get('width', 0)), float(g.get('height', 0))
    p = c['attrs'].get('parent')
    while p and p not in ('0', '1'):
        pg = cells[p]['geo']; x0 += float(pg.get('x', 0)); y0 += float(pg.get('y', 0)); p = cells[p]['attrs'].get('parent')
    return x0, y0, w, h

def vertices(cells):
    return [c for c in cells.values() if c['attrs'].get('vertex') == '1']

def edges(cells):
    return [c for c in cells.values() if c['attrs'].get('edge') == '1']

def args():
    """argv: <file.drawio> [page_id ...]；沒給頁就全部。"""
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <file.drawio> [page_id ...]"); sys.exit(2)
    return sys.argv[1], set(sys.argv[2:])
