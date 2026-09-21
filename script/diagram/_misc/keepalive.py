"""每 20 分鐘對兩個 drawio session POST 一次現況，避免 60 分鐘 TTL 清空；若發現被清空就用最近備份還原。"""
import json, time, urllib.request, re, sys
BASE="http://127.0.0.1:6002/api/state"
S={"mcp-mu5d9mmb-rfe5ca":"state_after_v2b.json","mcp-mu5l7tm8-smav8t":"../../../dist_distribution.drawio"}
def get(sid): return json.load(urllib.request.urlopen(f"{BASE}?sessionId={sid}"))
def post(sid,xml):
    r=urllib.request.Request(BASE,data=json.dumps({"sessionId":sid,"xml":xml}).encode(),headers={"Content-Type":"application/json"})
    return urllib.request.urlopen(r).read().decode()
while True:
    for sid,bak in S.items():
        try:
            d=get(sid); xml=d.get("xml",""); n=len(re.findall(r"<diagram",xml))
            if n<=1 and 'id="blank"' in xml:
                src=open(bak).read(); xml=json.loads(src)["xml"] if bak.endswith(".json") else src
                print(time.strftime("%H:%M"),sid,"EMPTY -> restore",post(sid,xml),flush=True)
            else:
                if sid=="mcp-mu5d9mmb-rfe5ca": open("state_latest_A.json","w").write(json.dumps({"xml":xml}))
                print(time.strftime("%H:%M"),sid,"pages",n,"touch",post(sid,xml),flush=True)
        except Exception as e: print(time.strftime("%H:%M"),sid,"ERR",e,flush=True)
    time.sleep(20*60)
