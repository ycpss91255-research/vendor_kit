"""每頁：流程結束 y、名詞表高、總高；各名詞表每條高度。"""
import re
exec(open("disc_v1_b.py").read())
for pid, name, cells in pages_v1_b:
    ys = [int(m) for m in re.findall(r'<mxCell id="[^"]*_th" [^>]*?>.*?y="(\d+)"', "".join(c for c in cells if "_th" in c), re.S)]
    m = re.search(r'pageHeight="(\d+)"', page(pid, name, cells))
    th = [c for c in cells if '_th"' in c]
    ty = int(re.search(r'y="(-?\d+)"', th[0]).group(1)) if th else 0
    print(f"{pid:10s} 總高 {m.group(1):>5s} 名詞表起 y={ty}  表高≈{int(m.group(1))-ty}")
def th(rows):
    return [(k[:18], max(28, math.ceil(max(need_h(k, 12, 150), need_h(d, 12, 610))))) for k, d in rows]
import sys
for nm in ["T5", "T5B", "T6", "T7", "T7B", "T7E", "T8", "T8B"]:
    rows = th(globals()[nm]); print(nm, "總", sum(h for _, h in rows), [(k, h) for k, h in rows if h > 45])
