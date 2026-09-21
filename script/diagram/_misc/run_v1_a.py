"""exec disc_v1_a.py → 組成 mxfile 寫到 scratchpad/v1_a.drawio 供檢查。"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
exec(open("disc_v1_a.py").read())
doc = '<mxfile host="app.diagrams.net">' + "".join(page(pid, name, cells) for pid, name, cells in pages_v1_a) + "</mxfile>"
open("v1_a.drawio", "w").write(doc)
print("pages:", [(pid, n, len(c)) for pid, n, c in pages_v1_a])
