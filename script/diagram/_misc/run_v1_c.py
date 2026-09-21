"""exec disc_v1_c.py → 組成 mxfile 寫到 scratchpad/v1_c.drawio 供檢查（八頁 v1p9…v1p16）。"""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
exec(open("disc_v1_c.py").read())
doc = '<mxfile host="app.diagrams.net">' + "".join(page(pid, name, cells) for pid, name, cells in pages_v1_c) + "</mxfile>"
open("v1_c.drawio", "w").write(doc)
for pid, name, cells in pages_v1_c:
    m = re.search(r'pageWidth="(\d+)" pageHeight="(\d+)"', page(pid, name, cells))
    print(pid, name, "page", m.groups(), "cells", len(cells))
