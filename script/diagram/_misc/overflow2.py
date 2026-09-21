import re, html, math, unicodedata
import xml.etree.ElementTree as ET
t = ET.parse('v2_only.drawio')
def last(key, st):
    m = re.findall(key+r'=([^;]+)', st); return m[-1] if m else None
def cw(ch, fs):
    if unicodedata.east_asian_width(ch) in ('W','F'): return fs
    if ch==' ': return fs*0.3
    if ch.isupper(): return fs*0.66
    return fs*0.55
def wrap(s, fs, maxw):
    lines=[]; cur=''; w=0
    for ch in s:
        c=cw(ch,fs)
        if w+c>maxw and cur:
            lines.append(cur); cur=ch; w=c
        else:
            cur+=ch; w+=c
    lines.append(cur); return lines
out=[]
for d in t.getroot().findall('diagram'):
    root = d.find('mxGraphModel/root')
    for c in root.findall('mxCell'):
        if c.get('vertex')!='1': continue
        st=c.get('style') or ''
        if not st.startswith('ellipse'): continue
        if '_lg' in c.get('id'): continue
        v=c.get('value') or ''
        v=re.sub(r'<br\s*/?>','\n',v); v=re.sub(r'<[^>]+>','',v); v=html.unescape(v)
        g=c.find('mxGeometry'); W=float(g.get('width')); H=float(g.get('height'))
        fs=float(last('fontSize',st) or 12)
        sl=float(last('spacingLeft',st) or 0); sr=float(last('spacingRight',st) or 0); sp=float(last('spacing',st) or 2)
        maxw=W-sl-sr-2*sp
        lines=[]
        for para in v.split('\n'): lines+=wrap(para,fs,maxw)
        lh=fs*1.2; total=len(lines)*lh
        y0=H/2-total/2
        bad=[]
        for i,l in enumerate(lines):
            lw=sum(cw(ch,fs) for ch in l)
            # worst y of this line: top or bottom edge farthest from center
            ytop=y0+i*lh; ybot=ytop+lh
            dy=max(abs(ytop-H/2),abs(ybot-H/2))
            if dy>=H/2: chord=0
            else: chord=W*math.sqrt(1-(dy/(H/2))**2)
            if lw>chord+2: bad.append((round(lw),round(chord)))
        if bad:
            out.append((d.get('id'), c.get('id'), f"{W:.0f}x{H:.0f}", bad, v.replace('\n',' | ')[:50]))
for o in out: print(*o)
print(len(out))
