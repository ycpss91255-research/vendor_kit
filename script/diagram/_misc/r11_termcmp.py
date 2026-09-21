import json,re,collections,sys
orig=open("disc_v1_a.py.v12",encoding="utf-8").read()
blk = orig[orig.index("TERMS = {"):orig.index("\n}\n", orig.index("TERMS = {"))+3]
ns={}; exec(blk, ns); TO=ns["TERMS"]
cur=open("disc_v1_a.py",encoding="utf-8").read()
blk = cur[cur.index("TERMS = {"):cur.index("\n}\n", cur.index("TERMS = {"))+3]
ns={}; exec(blk, ns); TC=ns["TERMS"]
pages=json.load(open("r11_all_out/pages.json"))
d=collections.defaultdict(lambda: collections.defaultdict(list))
for p in pages:
    pid=p["id"] if isinstance(p,dict) else p[0]
    j=json.load(open(f"r11_all_out/{pid}.json"))
    for t in j["terms"]: d[t["name"]][t["text"]].append(pid)
for key in sys.argv[1:]:
    name, txt = TO[key]
    print("=====",key,name)
    for v,ps in d[name].items():
        tag = "A-ORIG" if v==txt else ("A-CUR " if v==TC[key][1] else "      ")
        print("   ", tag, len(v), ps[:8], v[:50])
