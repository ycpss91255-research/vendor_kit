import re, os, json, html
from PIL import Image
SP=os.getcwd()
src=open("v2_only.drawio").read()
pages=re.findall(r'<diagram id="([^"]*)" name="([^"]*)"', src)
ids={i for i,_ in pages}
# delete stale
for f in os.listdir("png_v2"):
    if f[:-4] not in ids or not f.endswith(".png"):
        os.remove(os.path.join("png_v2",f)); print("removed", f)
# whiten
ws=[];hs=[]
for i,_ in pages:
    p=f"png_v2/{i}.png"; im=Image.open(p).convert("RGBA")
    bg=Image.new("RGBA",im.size,"white"); bg.alpha_composite(im); bg.convert("RGB").save(p)
    w,h=im.size; ws.append(w); hs.append(h)
out=[{"page": html.unescape(html.unescape(n)), "path": os.path.join(SP,"png_v2",f"{i}.png")} for i,n in pages]
json.dump(out, open("pngs_r14.json","w"), ensure_ascii=False, indent=0)
print(len(out), "entries; width", min(ws),"-",max(ws), "height", min(hs),"-",max(hs))
print(len(os.listdir("png_v2")), "files in png_v2")
for e in out: print(e["page"])
