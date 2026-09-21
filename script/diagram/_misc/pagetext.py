import re,html,sys
s=open('v2_only.drawio',encoding='utf-8').read()
want=sys.argv[1]
def strip(v):
    v=html.unescape(html.unescape(v)); v=re.sub(r'<br\s*/?>',' ⏎ ',v); v=re.sub(r'<[^>]+>','',v); return v
for m in re.finditer(r'<diagram [^>]*name="([^"]*)"[^>]*>(.*?)</diagram>',s,re.S):
    name=html.unescape(m.group(1))
    if want not in name: continue
    body=m.group(2)
    for c in re.finditer(r'<mxCell id="([^"]*)"([^>]*)>',body):
        attrs=c.group(2)
        v=re.search(r'value="([^"]*)"',attrs); st=re.search(r'style="([^"]*)"',attrs)
        if not v or not v.group(1): continue
        t=strip(v.group(1))
        style=st.group(1) if st else ''
        edge='E' if 'edge="1"' in attrs else 'V'
        fs=re.search(r'fontSize=(\d+)',style); fc=re.search(r'fillColor=([^;]+)',style); sc=re.search(r'strokeColor=([^;]+)',style)
        print(f"[{edge}] {c.group(1)} fs={fs.group(1) if fs else '-'} fill={fc.group(1) if fc else '-'} stroke={sc.group(1) if sc else '-'} | {t[:400]}")
