import re,html,sys
txt=open('v2_only.drawio',encoding='utf-8').read()
namepart=sys.argv[1]; filt=sys.argv[2] if len(sys.argv)>2 else None
for m in re.finditer(r'<diagram id="([^"]+)" name="([^"]+)">(.*?)</diagram>',txt,re.S):
    pid,name,body=m.groups()
    if namepart not in html.unescape(name): continue
    vals={}
    for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*)>',body):
        cid,attrs=c.groups()
        v=re.search(r'value="([^"]*)"',attrs); val=re.sub('<[^>]+>','',html.unescape(html.unescape(v.group(1)))) if v else ''
        vals[cid]=val.replace('\n',' ')
    for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*edge="1"[^>]*)>',body):
        cid,attrs=c.groups()
        s=re.search(r'source="([^"]*)"',attrs); t=re.search(r'target="([^"]*)"',attrs)
        s=s.group(1) if s else '?'; t=t.group(1) if t else '?'
        line=f"{cid} | {vals.get(cid,'')[:12]} | {s} {vals.get(s,'')[:28]} -> {t} {vals.get(t,'')[:28]}"
        if filt is None or filt in line: print(line)
