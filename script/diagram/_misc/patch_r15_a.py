"""第十五輪：v1p0／v1p0b／v1p1 依 r13_codex/findings_00_01.md 修（備份 .v16）。只動審閱頁區塊與 tbl() 的 lh 參數。"""
import re
src = open("disc_v1_a.py", encoding="utf-8").read()
def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:80])
    src = src.replace(old, new)

# ---- 0. 檔頭說明 ----
rep("只定義 pages_v1_a，不寫檔。", "第十五輪（r13_codex/findings_00_01.md；備份 .v16）：審閱頁去掉 md 沒有的圖例／續頁句／「寫法約定」；常用詞拆到 v1p0c、不變量拆到 v1p1i；三方角色表改直排；審閱頁內容寬 1580、行距 1.4。\n只定義 pages_v1_a，不寫檔。")

# ---- 1. tbl()：加 lh（行距）參數；審閱頁用 ----
rep('def tbl(out, prefix, parent, x, y, cols, rows, fills=None, marks=(), bold0=True, align=()):',
    'def tbl(out, prefix, parent, x, y, cols, rows, fills=None, marks=(), bold0=True, align=(), lh=None):')
rep('    fills: 每列底色；第一欄粗體；marks: {(r, c)} 加 v2 標籤；align: 欄索引集合 → 這些欄的第 k 個子格等高（同一件事的條件／動作／結束碼橫向對齊）。回傳結束 y。"""',
    '    fills: 每列底色；第一欄粗體；marks: {(r, c)} 加 v2 標籤；align: 欄索引集合 → 這些欄的第 k 個子格等高（同一件事的條件／動作／結束碼橫向對齊）；\n    lh: 行距（lineHeight；None = 預設），設了就用 hvl() 估高。回傳結束 y。"""')
rep('        hs = [[hvt(s, w, (r, i) in marks and k == 0, pad=2) for k, s in enumerate(col)] for i, (col, (_, w)) in enumerate(zip(cells, cols))]',
    '        hs = [[(hvl(s, w - (34 if (r, i) in marks and k == 0 else 0), lh, pad=2) if lh else hvt(s, w, (r, i) in marks and k == 0, pad=2)) for k, s in enumerate(col)] for i, (col, (_, w)) in enumerate(zip(cells, cols))]')
rep('                st = tbl_style(fill, bold=(i == 0 and bold0))\n',
    '                st = tbl_style(fill, bold=(i == 0 and bold0)) + (f"lineHeight={lh};" if lh else "")\n')

# ---- 2. 審閱頁共用 helper ----
old_helpers = src[src.index("# ---------- 審閱頁（md 定稿版逐字移植）共用 ----------"):src.index("# ================= P0 v1p0")]
new_helpers = '''# ---------- 審閱頁（md 定稿版逐字移植）共用 ----------
RX, RW, RLH = 20, 1580, 1.4      # 審閱頁：左邊距 20、內容寬 1580（page() 右邊自動留 40 → 頁寬 1640）、行距 1.4
def M(s):
    """md 行內記法 → 圖上文字：`code` 去反引號；**x** → 粗體。其餘一字不改。"""
    s = s.replace("`", "")
    return re.sub(r"\\*\\*(.+?)\\*\\*", r"<b>\\1</b>", s)
def hvl(text, w, lh, fs=12, pad=6):
    """行距 lh 的最小高度：行數×fs×(lh+0.1)+8+pad（估法同 need_h；check_overflow 以 1.3 估，必過）。"""
    from check_overflow import wrap
    lines = sum(wrap(ln, fs, w - 16)[0] for ln in text.split("\\n"))
    return math.ceil(lines * fs * (lh + 0.1) + 8) + pad
def rlh(st):
    return st + f"lineHeight={RLH};"
def sec(out, pid, y, title, w=None):
    """節標題（LBL）。回傳結束 y。"""
    out.append(v(pid, "1", LBL, title, RX, y, w or RW, 28)); return y + 32
def para(out, pid, y, text, style=None, w=None, x=RX, pad=6):
    """一段文字一格（白底 12pt、行距 RLH）。回傳結束 y（含 10px 間距）。"""
    w = w or RW; st = rlh(style or LT12)
    h = hvl(text, w, RLH, pad=pad)
    out.append(vb(pid, "1", st, text, x, y, w, h)); return y + h + 10
def mtbl(out, prefix, y, cols, rows, x=RX, bold0=True):
    """md 表格 → tbl()（表頭灰底、第一欄粗體、行距 RLH）；rows 內每格先過 M()。回傳結束 y（含 14px 間距）。"""
    return tbl(out, prefix, "1", x, y, cols, [[M(c) for c in r] for r in rows], bold0=bold0, lh=RLH) + 14
def kvblock(out, prefix, y, rows, kw=130, x=RX, w=None):
    """直排的「標籤｜內容」表：一列一格對（第 0 列灰底當該組標題）；rows: [(標籤, 內容)]，內容先過 M()。回傳結束 y（含 14px 間距）。"""
    w = w or RW
    for r, (k, val) in enumerate(rows):
        val = M(val); fill = "#e6e6e6" if r == 0 else "#ffffff"
        h = max(hvl(k, kw, RLH, pad=2), hvl(val, w - kw, RLH, pad=2))
        out.append(vb(f"{prefix}_r{r}c0", "1", rlh(tbl_style(fill, bold=True)), k, x, y, kw, h))
        out.append(vb(f"{prefix}_r{r}c1", "1", rlh(tbl_style(fill, bold=(r == 0))), val, x + kw, y, w - kw, h))
        y += h
    return y + 14
def rtitle(pid, title):
    return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]

'''
src = src.replace(old_helpers, new_helpers)

# ---- 3. v1p0 ----
rep('p0 = rtitle("p0", "審閱頁 00：名詞與縮寫（1）三方／組件／常用詞")', 'p0 = rtitle("p0", "審閱頁 00：名詞與縮寫（1）三方／組件／模組／常用詞")')
rep('[("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 850), ("地位", 260)]', '[("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)]')
rep('[("中文名", 150), ("英文", 200), ("定義", 1210)]', '[("中文名", 150), ("英文", 200), ("定義", 1230)]')
rep('''CW = 510; ch = max(hv(t, CW) for t in COMP)
for i, t in enumerate(COMP):
    p0.append(vb(f"p0_c{i + 1}", "1", LT12, t, 40 + i * (CW + 15), Y, CW, ch))''',
'''CW = 516; ch = max(hvl(t, CW, RLH) for t in COMP)          # 516×3 + 16×2 = 1580
for i, t in enumerate(COMP):
    p0.append(vb(f"p0_c{i + 1}", "1", rlh(LT12), t, RX + i * (CW + 16), Y, CW, ch))''')
rep('[("中文名", 150), ("英文代號", 150), ("做什麼", 1260)]', '[("中文名", 150), ("英文代號", 150), ("做什麼", 1280)]')
rep('''Y = sec(p0, "p0_s3", Y, "常用詞")
Y = mtbl(p0, "p0_t4", Y, [("中文名", 190), ("英文", 170), ("定義", 1200)], [
''', '''T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
T4 = [
''')
rep('''一次執行的交易 id"],
])
c, Y = lgd("p0", 40, Y + 6, ["tblh"], "本頁只定義、不決議；續「名詞與縮寫（2）既有詞／記法／動詞」頁")
p0 += c
pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／常用詞", p0))
''', '''一次執行的交易 id"],
]
T4_SPLIT = 14                                    # 常用詞 29 條：前 14 條留本頁，其餘到 v1p0c
Y = sec(p0, "p0_s3", Y, "常用詞")
Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))

# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
p0c = rtitle("p0c", "審閱頁 00：名詞與縮寫（2）常用詞（續）")
Y = 70
Y = sec(p0c, "p0c_s3", Y, "常用詞")
Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
''')

# ---- 4. v1p0b ----
rep('p0b = rtitle("p0b", "審閱頁 00：名詞與縮寫（2）既有詞／記法／動詞")', 'p0b = rtitle("p0b", "審閱頁 00：名詞與縮寫（3）既有詞／記法／動詞")')
rep('[("中文名", 190), ("英文", 190), ("定義", 1180)]', '[("中文名", 190), ("英文", 190), ("定義", 1200)]')
rep('[("記法", 260), ("意思", 1300)]', '[("記法", 260), ("意思", 1320)]')
rep('''for i, t in enumerate(OPTS):
    h = hv(M(t), 1560, pad=2)
    p0b.append(vb(f"p0b_o{i + 1}", "1", LT12, M(t), 40, Y, 1560, h)); Y += h''',
'''for i, t in enumerate(OPTS):
    h = hvl(M(t), RW, RLH, pad=2)
    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h''')
rep('[("動詞", 330), ("做什麼", 1230)]', '[("動詞", 330), ("做什麼", 1250)]')
rep('''# ---- 寫法約定 ----
Y = sec(p0b, "p0b_s4", Y, "寫法約定")
Y = para(p0b, "p0b_w1", Y, M("「→ 1：X」= 以結束碼 1 結束並印出 X；「→ 0」= 以結束碼 0 結束。「→ 2」「→ 3」同理。"), style=RULE)
Y = para(p0b, "p0b_w2", Y, M("圖上顏色：**藍** = 引擎做；**白** = 啟動器做；**綠** = 結束碼 0；**橙** = 需人處理；**紅** = 失敗；**白虛線橢圓** = 來自其他頁的節點。"), style=RULE)
c, Y = lgd("p0b", 40, Y + 6, ["tblh", "ruleb"], "續「名詞與縮寫（1）三方／組件／常用詞」頁；本頁只定義、不決議")
p0b += c
pages_v1_a.append(("v1p0b", "名詞與縮寫（2）既有詞／記法／動詞", p0b))''',
'''pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))''')

# ---- 5. v1p1 ----
rep('p1 = rtitle("p1", "審閱頁 01：不變量與角色")', 'p1 = rtitle("p1", "審閱頁 01：不變量與角色（1）目的／名詞／角色")')
rep('[("名詞", 170), ("定義", 1390)]', '[("名詞", 170), ("定義", 1410)]')
rep('''Y = mtbl(p1, "p1_tr", Y, [("名稱", 120), ("是誰", 200), ("負責", 580), ("不負責", 340), ("地位", 320)], [
 ["**下游開發者**",''', '''ROLES = [                                        # md 五欄表 → 一個角色一組直排（名稱列灰底＋是誰／負責／不負責／地位）
 ["**下游開發者**",''')
rep('''"承諾方：內部怎麼實作不屬於本契約，可自由變更"],
])
Y = para(p1, "p1_trn",''', '''"承諾方：內部怎麼實作不屬於本契約，可自由變更"],
]
for i, row in enumerate(ROLES):
    Y = kvblock(p1, f"p1_tr{i}", Y, list(zip(["名稱", "是誰", "負責", "不負責", "地位"], row)))
Y = para(p1, "p1_trn",''')
rep('''AW = 772; ah = max(hv(t, AW) for t in AUTO)
for i, t in enumerate(AUTO):
    p1.append(vb(f"p1_auto{i}", "1", LT12, t, 40 + i * (AW + 16), Y, AW, ah))
Y += ah + 10
# ---- 不變量 I1–I18（一條一格）----
Y = sec(p1, "p1_s4", Y, "不變量")''',
'''AW = 782; ah = max(hvl(t, AW, RLH) for t in AUTO)          # 782×2 + 16 = 1580
for i, t in enumerate(AUTO):
    p1.append(vb(f"p1_auto{i}", "1", rlh(LT12), t, RX + i * (AW + 16), Y, AW, ah))
Y += ah + 10
pages_v1_a.append(("v1p1", "不變量與角色（1）目的／名詞／角色", p1))

# ================= P1i v1p1i：審閱頁 01 不變量與角色（2）=================
p1i = rtitle("p1i", "審閱頁 01：不變量與角色（2）不變量／例外／待拍板")
Y = 70
# ---- 不變量 I1–I18（一條一格）----
Y = sec(p1i, "p1_s4", Y, "不變量")''')
rep('''for i, t in enumerate(INVS):
    h = hv(M(t), 1560, pad=4)
    p1.append(vb(f"p1_i{i + 1}", "1", INV, M(t), 40, Y, 1560, h)); Y += h + 4
Y += 6
# ---- 例外清單 ----
Y = sec(p1, "p1_s5", Y, "例外清單（不變量的明文例外）")''',
'''for i, t in enumerate(INVS):
    h = hvl(M(t), RW, RLH, pad=8)
    p1i.append(vb(f"p1_i{i + 1}", "1", rlh(INV), M(t), RX, Y, RW, h)); Y += h + 6
Y += 6
# ---- 例外清單 ----
Y = sec(p1i, "p1_s5", Y, "例外清單（不變量的明文例外）")''')
rep('''for i, t in enumerate(EXC):
    h = hv(M(t), 1560, pad=4)
    p1.append(vb(f"p1_x{i + 1}", "1", RULE, M(t), 40, Y, 1560, h)); Y += h + 4
Y += 6''', '''for i, t in enumerate(EXC):
    h = hvl(M(t), RW, RLH, pad=8)
    p1i.append(vb(f"p1_x{i + 1}", "1", rlh(RULE), M(t), RX, Y, RW, h)); Y += h + 6
Y += 6''')
rep('''Y = para(p1, "p1_pend", Y, PEND_T, style=NP_NOTE, pad=10)
c, Y = lgd("p1", 40, Y + 6, ["invb", "ruleb", "tblh", "notep"], "一條不變量一格；出處對照不上圖（見 md）")
p1 += c
pages_v1_a.append(("v1p1", "不變量與角色", p1))''',
'''Y = para(p1i, "p1_pend", Y, PEND_T, style=NP_NOTE, pad=10)
pages_v1_a.append(("v1p1i", "不變量與角色（2）不變量／例外／待拍板", p1i))''')
open("disc_v1_a.py", "w", encoding="utf-8").write(src)
print("ok")
