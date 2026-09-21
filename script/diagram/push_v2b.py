import re, json, urllib.request
import os
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "discussion.drawio")   # repo 根的 discussion.drawio
BASE="http://127.0.0.1:6002/api/state"; SID="mcp-mu5d9mmb-rfe5ca"
src=open(SRC).read()
segs=re.findall(r'<diagram id="v1p[^"]*"[^>]*>.*?</diagram>', src, re.S)
print("segments", len(segs))
ids=[re.match(r'<diagram id="([^"]*)"',s).group(1) for s in segs]
print(ids)
open("v2_only.drawio","w").write('<mxfile host="Electron" version="24.0.0" type="device">\n'+"\n".join(segs)+"\n</mxfile>\n")
# push
d=json.load(urllib.request.urlopen(f"{BASE}?sessionId={SID}")); xml=d.get("xml","")
old=re.findall(r'<diagram id="([^"]*)"', xml); print("before:", len(old), old)
xml2=re.sub(r'<diagram id="v1p[^"]*"[^>]*>.*?</diagram>\s*', '', xml, flags=re.S)
rest=re.findall(r'<diagram id="([^"]*)"', xml2); print("rest:", len(rest), rest)
m=re.search(r'<mxfile[^>]*>', xml2)
xml3=xml2[:m.end()]+"\n"+"\n".join(segs)+"\n"+xml2[m.end():]
r=urllib.request.Request(BASE,data=json.dumps({"sessionId":SID,"xml":xml3}).encode(),headers={"Content-Type":"application/json"})
print("POST:", urllib.request.urlopen(r).read().decode()[:200])
d=json.load(urllib.request.urlopen(f"{BASE}?sessionId={SID}")); xml=d.get("xml","")
after=re.findall(r'<diagram id="([^"]*)"', xml); print("after:", len(after), after)
assert after[:len(ids)]==ids and len(after)==len(ids)+len(rest), "mismatch"
open("state_after_v2b.json","w").write(json.dumps({"xml":xml}))
print("saved state_after_v2b.json", len(xml))
