import re, os, json, sys
from PIL import Image
src=open("v2_only.drawio").read()
pages=re.findall(r'<diagram id="([^"]*)" name="([^"]*)"', src)
ids=[i for i,_ in pages]
bad=[]
for i,_ in pages:
    p=f"png_v2/{i}.png"
    try:
        im=Image.open(p); im.verify()
        im=Image.open(p); im.load()
        w,h=im.size
        if w<200 or h<200: raise ValueError(f"tiny {w}x{h}")
        # detect mostly-empty image
        small=im.convert("L").resize((64,64)); ext=small.getextrema()
        if ext[1]-ext[0]<10: raise ValueError("flat image")
        print(i, w, h, "ok")
    except Exception as e:
        print(i, "BAD", e); bad.append(i)
print("BAD:", bad)
