import re, html
import xml.etree.ElementTree as ET
from collections import defaultdict
t = ET.parse('v2_only.drawio')
def last(key, st):
    m = re.findall(key+r'=([^;]+)', st)
    return m[-1] if m else '-'
for d in t.getroot().findall('diagram'):
    print("="*20, d.get('id'), d.get('name'))
    root = d.find('mxGraphModel/root')
    combos = defaultdict(list)
    for c in root.findall('mxCell'):
        if c.get('vertex')!='1': continue
        st = c.get('style') or ''
        if st.startswith('text') or 'strokeColor=none' in st and 'fillColor=none' in st: continue
        shape = re.search(r'^(ellipse|rhombus|shape=[^;]+|swimlane)', st)
        key=(last('fillColor',st), last('strokeColor',st), 'dashed' if 'dashed=1' in st else '', last('strokeWidth',st), shape.group(0) if shape else 'rect')
        combos[key].append(c.get('id'))
    for k,v in sorted(combos.items(), key=lambda x:-len(x[1])):
        print(k, len(v), v[:6])
