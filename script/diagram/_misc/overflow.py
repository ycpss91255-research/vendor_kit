import re, html, math, unicodedata
import xml.etree.ElementTree as ET
t = ET.parse('v2_only.drawio')
def last(key, st):
    m = re.findall(key+r'=([^;]+)', st); return m[-1] if m else None
def width(s, fs):
    w=0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ('W','F'): w+=fs
        elif ch==' ': w+=fs*0.3
        elif ch.isupper(): w+=fs*0.65
        else: w+=fs*0.53
    return w
for d in t.getroot().findall('diagram'):
    root = d.find('mxGraphModel/root')
    for c in root.findall('mxCell'):
        if c.get('vertex')!='1': continue
        st=c.get('style') or ''
        if not (st.startswith('ellipse') or st.startswith('rhombus')): continue
        v=c.get('value') or ''
        v=re.sub(r'<br\s*/?>','\n',v); v=re.sub(r'<[^>]+>','',v); v=html.unescape(v)
        g=c.find('mxGeometry'); W=float(g.get('width')); H=float(g.get('height'))
        fs=float(last('fontSize',st) or 12)
        f = 0.707 if st.startswith('ellipse') else 0.5
        iw, ih = W*f, H*f
        lines=0
        for para in v.split('\n'):
            lines += max(1, math.ceil(width(para,fs)/iw))
        need = lines*fs*1.25
        if need > ih*1.05:
            print(d.get('id'), c.get('id'), f"{W:.0f}x{H:.0f} lines={lines} need={need:.0f} avail={ih:.0f}", v.replace('\n',' | ')[:60])
