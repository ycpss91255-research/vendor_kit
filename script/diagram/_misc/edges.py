import sys,re,html
page=sys.argv[1]
txt=open('v2_only.drawio',encoding='utf-8').read()
m=re.search(r'<diagram id="%s" name="[^"]+">(.*?)</diagram>'%re.escape(page),txt,re.S).group(1)
vals={}
for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*)>',m):
    cid,attrs=c.groups(); v=re.search(r'value="([^"]*)"',attrs)
    vals[cid]=re.sub('<[^>]+>','',html.unescape(html.unescape(v.group(1))))[:40].replace('\n',' ') if v else ''
for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*edge="1"[^>]*)>(.*?)</mxCell>',m,re.S):
    cid,attrs,inner=c.groups()
    s=re.search(r'source="([^"]+)"',attrs); t=re.search(r'target="([^"]+)"',attrs)
    pts=re.findall(r'<mxPoint x="([^"]+)" y="([^"]+)"',inner)
    st=re.search(r'style="([^"]*)"',attrs).group(1)
    ex=re.findall(r'(entry[XY]|exit[XY])=([0-9.]+)',st)
    print(cid,'[%s]'%vals.get(cid,''), (s.group(1) if s else '-')+'('+vals.get(s.group(1) if s else '','')+')','->',(t.group(1) if t else '-')+'('+vals.get(t.group(1) if t else '','')+')',pts,ex)
