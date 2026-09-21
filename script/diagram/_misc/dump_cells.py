import re, html, sys
import xml.etree.ElementTree as ET
t = ET.parse('v2_only.drawio')
def last(key, st):
    m = re.findall(key+r'=([^;]+)', st)
    return m[-1] if m else '-'
for d in t.getroot().findall('diagram'):
    print("="*20, d.get('id'), d.get('name'))
    root = d.find('mxGraphModel/root')
    for c in root.findall('mxCell'):
        v = c.get('value') or ''
        v = re.sub(r'<br\s*/?>', ' | ', v)
        v = re.sub(r'<[^>]+>', '', v)
        v = html.unescape(v).replace('\n',' | ')
        st = c.get('style') or ''
        g = c.find('mxGeometry')
        geo = ''
        if g is not None:
            geo = f"({g.get('x')},{g.get('y')},{g.get('width')},{g.get('height')})"
        kind = 'E' if c.get('edge')=='1' else ('V' if c.get('vertex')=='1' else '-')
        dash = 'dashed' if 'dashed=1' in st else ''
        shape = re.search(r'^(ellipse|rhombus|shape=[^;]+|swimlane|text|note[^;]*)', st)
        extra = f"fill={last('fillColor',st)} stroke={last('strokeColor',st)} fs={last('fontSize',st)} {dash} sw={last('strokeWidth',st)} {shape.group(0) if shape else ''} parent={c.get('parent')}"
        if kind=='E':
            extra += f" src={c.get('source')} tgt={c.get('target')}"
            pts = [ (p.get('x'),p.get('y')) for p in g.findall('Array/mxPoint')] if g is not None else []
            if pts: extra += f" pts={pts}"
            sp = g.find("mxPoint[@as='sourcePoint']") if g is not None else None
            tp = g.find("mxPoint[@as='targetPoint']") if g is not None else None
            if c.get('source') is None and sp is not None: extra += f" srcPt=({sp.get('x')},{sp.get('y')})"
            if c.get('target') is None and tp is not None: extra += f" tgtPt=({tp.get('x')},{tp.get('y')})"
        if v or kind=='E':
            print(f"[{kind}] {c.get('id')} {geo} {extra}\n    {v}")
