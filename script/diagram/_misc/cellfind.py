import sys,re,html
pat=sys.argv[1]; page=sys.argv[2] if len(sys.argv)>2 else None
txt=open('v2_only.drawio',encoding='utf-8').read()
for m in re.finditer(r'<diagram id="([^"]+)" name="([^"]+)">(.*?)</diagram>',txt,re.S):
    pid,name,body=m.groups()
    if page and page!=pid: continue
    for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*)>',body):
        cid,attrs=c.groups()
        v=re.search(r'value="([^"]*)"',attrs)
        val=html.unescape(v.group(1)) if v else ''
        val=re.sub('<[^>]+>','',html.unescape(val))
        if re.search(pat,val):
            print(pid,cid,'|',val[:160].replace('\n',' '))
