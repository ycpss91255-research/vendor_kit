import re
p = "disc_v1_b.py"; s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:80])
    s = s.replace(old, new)

# 1. emit：PRE 框（whiteSpace=pre）值包 <pre>，tab 寫成 &#9;（同 disc_v1_a code()；v2.7 §9）
rep('''def emit(cells, cid, parent, st, text, x, y, w, h):
    """輸出一格；style 帶 v2=1 → 另加右上角綠標籤；橢圓／菱形自動補 spacing（v2.5 §15）。"""
    tag = "v2=1;" in st; st = shape_spacing(st.replace("v2=1;", ""), w, h)
    cells.append(v(cid, parent, st, text, x, y, w, h))''',
'''def pre_v(cid, parent, st, text, x, y, w, h):
    """逐字框（whiteSpace=pre）：值包在 <pre> 內、tab 寫成 &#9;（XML 屬性裡的字面 tab 會被正規化）；同 disc_v1_a 的 code()（v2.7 §9）。"""
    import html as _html
    inner = _html.escape(text, quote=False).replace("\\n", "<br>")
    htmlv = '<pre style="margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;">' + inner + '</pre>'
    val = _html.escape(htmlv, quote=True).replace("\\t", "&#9;")
    return (f'<mxCell id="{cid}" value="{val}" style="{st}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def emit(cells, cid, parent, st, text, x, y, w, h):
    """輸出一格；style 帶 v2=1 → 另加右上角綠標籤；橢圓／菱形自動補 spacing（v2.5 §15）；whiteSpace=pre → pre_v。"""
    tag = "v2=1;" in st; st = shape_spacing(st.replace("v2=1;", ""), w, h)
    cells.append((pre_v if "whiteSpace=pre;" in st else v)(cid, parent, st, text, x, y, w, h))''')

# 2. files()：cols=2 兩欄排小框（省高度）
rep('''    def files(self, cid, col, row, title, items, w, ax="c"):
        """檔案框一格一檔（v2.5 §14）：虛線標題容器，內排每檔一個小框（id = cid_0, cid_1…）。"""
        iw = w - 16; hs = [fit_h(t, iw, 26) for t in items]
        h = 26 + sum(hs) + 6 * len(items) + 4
        self.boxes.append(dict(id=cid, col=col, row=row, st=FGRP, text=title, w=w, h=h, ax=ax, items=list(zip(items, hs)))); return cid''',
'''    def files(self, cid, col, row, title, items, w, ax="c", cols=1):
        """檔案框一格一檔（v2.5 §14）：虛線標題容器，內排每檔一個小框（id = cid_0, cid_1…）；cols=2 → 兩欄（同列取最高）。"""
        iw = (w - 16 - 6 * (cols - 1)) // cols; hs = [fit_h(t, iw, 26) for t in items]
        rows = [max(hs[i:i + cols]) for i in range(0, len(hs), cols)]
        h = 26 + sum(rows) + 6 * len(rows) + 4
        self.boxes.append(dict(id=cid, col=col, row=row, st=FGRP, text=title, w=w, h=h, ax=ax, items=list(zip(items, hs)), cols=cols, iw=iw, rows=rows)); return cid''')
rep('''            if "items" in b:                                    # 檔案容器：小框相對容器座標
                iy = 26
                for i, (t, hh) in enumerate(b["items"]):
                    emit(f.cells, f"{b['id']}_{i}", b["id"], F12, t, 8, iy, b["w"] - 16, hh); iy += hh + 6''',
'''            if "items" in b:                                    # 檔案容器：小框相對容器座標（cols 欄）
                iy = 26; nc = b["cols"]
                for i, (t, hh) in enumerate(b["items"]):
                    r, c = divmod(i, nc)
                    emit(f.cells, f"{b['id']}_{i}", b["id"], F12, t, 8 + c * (b["iw"] + 6), iy, b["iw"], b["rows"][r])
                    if c == nc - 1 or i == len(b["items"]) - 1: iy += b["rows"][r] + 6''')

# 3. D／U 對齊：目標是菱形 → 入口固定頂點（entryX=0.5），改動來源出口；來源也是菱形 → 留縫隙折線（review r6）
rep('''                if 1 <= abs(ex - nx) < 40 or (al and abs(ex - nx) >= 1):   # 小折角很醜：把出／入點對齊成一直線（先動目標入口，再動來源出口）
                    r = (ex - tx0) / tw
                    if 0.1 <= r <= 0.9: txr, nx = r, ex
                    else:
                        r = (nx - sx0) / sw
                        if 0.1 <= r <= 0.9: sxr, ex = r, nx''',
'''                if 1 <= abs(ex - nx) < 40 or (al and abs(ex - nx) >= 1):   # 小折角很醜：把出／入點對齊成一直線（先動目標入口，再動來源出口）
                    r = (ex - tx0) / tw                                      # 目標是菱形 → 入口只用頂點（entryX=0.5），不接斜邊（review r6）
                    if 0.1 <= r <= 0.9 and not ST.get(t, "").startswith("rhombus"): txr, nx = r, ex
                    else:
                        r = (nx - sx0) / sw
                        if 0.1 <= r <= 0.9 and not ST.get(s, "").startswith("rhombus"): sxr, ex = r, nx''')

# 4. 新線型 LL：從 s 左側出去，水平到 x=busx，往上到 t 中線，再水平進 t 左側（迴圈回上方）
rep('''    def RD(self, eid, s, t, label="", tx=0.5):''',
'''    def LL(self, eid, s, t, label="", busx=0):
        """從 s 左側出去，水平到 x=busx 的左側匯流排，往上到 t 的中線高度，再水平進 t 的左側（迴圈回上方的格子；標籤放匯流排左側）。"""
        self.edges.append(("LL", eid, s, t, label, busx))
    def RD(self, eid, s, t, label="", tx=0.5):''')
rep('''            elif kind == "RD":
                _, _, _, _, label, txr = ed''',
'''            elif kind == "LL":
                _, _, _, _, label, busx = ed
                ey = sy0 + sh / 2; ny = ty0 + th / 2
                L1 = abs(sx0 - busx); tot = L1 + abs(ey - ny) + abs(tx0 - busx)
                pos = 2 * ((L1 + 14) / tot) - 1 if label else None
                f.cells.append(_edge(eid, s, t, label, (0, 0.5), (0, 0.5), [(busx, ey), (busx, ny)], pos, "left" if label else None))
            elif kind == "RD":
                _, _, _, _, label, txr = ed''')
open(p, "w", encoding="utf-8").write(s); print("ok")
