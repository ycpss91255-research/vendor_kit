import sys,re,html
txt=open('v2_only.drawio',encoding='utf-8').read()
want=sys.argv[1:]  # page index numbers (1-based)
pages=list(re.finditer(r'<diagram id="([^"]+)" name="([^"]+)">(.*?)</diagram>',txt,re.S))
for i,m in enumerate(pages,1):
    if want and str(i) not in want: continue
    pid,name,body=m.groups()
    print('=== PAGE',i,html.unescape(name))
    cells={}
    for c in re.finditer(r'<mxCell id="([^"]+)"([^>]*?)(/>|>)',body):
        cid,attrs,_=c.groups()
        v=re.search(r'value="([^"]*)"',attrs)
        val=html.unescape(v.group(1)) if v else ''
        val=re.sub('<[^>]+>',' ',html.unescape(val)); val=re.sub(r'\s+',' ',val).strip()
        st=re.search(r'style="([^"]*)"',attrs); st=st.group(1) if st else ''
        src=re.search(r'source="([^"]*)"',attrs); tgt=re.search(r'target="([^"]*)"',attrs)
        isedge='edge="1"' in attrs
        fill=re.search(r'fillColor=([^;]+)',st); fill=fill.group(1) if fill else ''
        cells[cid]=(val,isedge,src.group(1) if src else None,tgt.group(1) if tgt else None,fill,st)
    for cid,(val,isedge,src,tgt,fill,st) in cells.items():
        if isedge:
            s=cells.get(src,('?',))[0][:30] if src else 'NONE'
            t=cells.get(tgt,('?',))[0][:30] if tgt else 'NONE'
            print(f'  E {cid}: [{s}] -> [{t}]  "{val[:60]}"')
        elif val:
            print(f'  V {cid} fill={fill}: {val[:200]}')
