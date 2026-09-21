import sys, re, html
import xml.etree.ElementTree as ET
t = ET.parse('v2_only.drawio')
pages = {d.get('id'): d for d in t.getroot().findall('diagram')}
d = pages[sys.argv[1]]
for c in d.iter('mxCell'):
    if c.get('edge'): continue
    st = c.get('style') or ''
    m = re.search(r'fillColor=([^;]+)', st)
    fill = m.group(1) if m else '-'
    v = re.sub('<[^>]+>',' ',html.unescape(c.get('value') or ''))
    if not v.strip(): continue
    shape = 'rhombus' if 'rhombus' in st else ('ellipse' if 'ellipse' in st else ('note' if 'note' in st else 'rect'))
    print(c.get('id'), fill, shape, '|', v[:90].replace('\n',' '))
