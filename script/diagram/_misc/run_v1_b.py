"""exec disc_v1_b.py，把四頁組成 mxfile 寫到 v1_b.drawio 供檢查。"""
exec(open("disc_v1_b.py").read())
doc = '<mxfile host="app.diagrams.net">' + "".join(page(pid, name, cells) for pid, name, cells in pages_v1_b) + "</mxfile>"
open("v1_b.drawio", "w").write(doc)
import re
for pid, name, cells in pages_v1_b:
    m = re.search(r'pageWidth="(\d+)" pageHeight="(\d+)"', page(pid, name, cells))
    print(pid, name, "page", m.groups())
