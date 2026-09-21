import sys, re, html
import xml.etree.ElementTree as ET
t = ET.parse('v2_only.drawio')
pages = {d.get('id'): d for d in t.getroot().findall('diagram')}
if sys.argv[1] == 'list':
    for k,d in pages.items(): print(k, d.get('name'))
    sys.exit()
d = pages[sys.argv[1]]
q = sys.argv[2] if len(sys.argv)>2 else None
for c in d.iter('mxCell'):
    cid = c.get('id'); v = c.get('value') or ''
    txt = re.sub('<[^>]+>',' ',html.unescape(v))
    if q and q not in cid and q not in txt: continue
    g = c.find('mxGeometry')
    geo = f"({g.get('x')},{g.get('y')},{g.get('width')},{g.get('height')})" if g is not None else ''
    edge = ''
    if c.get('edge'): edge = f"EDGE {c.get('source')}->{c.get('target')}"
    print(cid, edge, geo, '|', txt[:200].replace('\n',' '))
