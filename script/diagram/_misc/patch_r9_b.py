import re
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:80])
    src = src.replace(old, new)

# ---- header note ----
rep("備份：.v1（v1）、.v2（拆頁前）、.v4（第三輪前）、.v5（第四輪前）、.v6（第五輪前）、.v7（第六輪前）、.v8（第七輪前）、.v9（第八輪前）。",
    "備份：.v1（v1）、.v2（拆頁前）、.v4（第三輪前）、.v5（第四輪前）、.v6（第五輪前）、.v7（第六輪前）、.v8（第七輪前）、.v9（第八輪前）、.v10（第九輪前）。\n"
    "第九輪（v2.10 + review_v2r8_findings.md）：需人動作的 1 結束一律橙（B(1′) b10dx／b10nx、dev d3a／d1x／d3c）；upgrade vendor_kit 不建進度日誌（E(c) 兩頁）；6-2b 只給第一行已改（E(a) s2lx、E(c)(2) s13x 拆兩個結束）；\n"
    "迴圈菱形（bootstrap(2)「還有下一個 -t？」、sync(1′)「還有工具？」）；install(1) 第一次直接建檔；install(2) 刪日誌獨立格；sync(2) 驗證／重裝拆格；失敗線不 T 接（各自進紅橢圓不同入口）；ae11b 不交叉；ce28n／ce28y 標籤離框。")

# ---- bootstrap(1)：ae11b 從 a6p 底 0.3 直下進 a9 頂 0.87（不與 ae6y x=545 交叉）----
rep('b.D("ae11", "a8i", "a9"); b.D("ae11b", "a6p", "a9")',
    'b.D("ae11", "a8i", "a9"); b.D("ae11b", "a6p", "a9", "", 0.3, 0.87)   # 直下一條線（x=621），不與 ae6y（x=545）交叉（r8）')

# ---- bootstrap(2)：迴圈菱形 a10q，移除浮動文字 a10l ----
rep('b.box("a10l", G, 3, LBL, "← 對每個 -t <repo>[@<tag>] 重複；一個失敗即中止", 180, 40, minh=40)\n', "")
rep('''b.box("a12", U, 7, v2(R12), fl("是 → 1：明列已完成／未完成（多工具彙總：1 > 2 > 0）"), 220)
b.box("a11", L, 7, D12, "任一 add 失敗？", 200)
b.box("a13", U, 8, G12, "0：印摘要與要 git add 的清單", 220)''',
'''b.box("a10q", L, 7, v2(D12), "還有下一個 -t？", 200)
b.box("a12", U, 8, v2(R12), fl("是 → 1：明列已完成／未完成（多工具彙總：1 > 2 > 0）"), 220)
b.box("a11", L, 8, D12, "任一 add 失敗？", 200)
b.box("a13", U, 9, G12, "0：印摘要與要 git add 的清單", 220)''')
rep('b.D("ae22", "a10a", "a11", al=True); b.H("ae23", "a11", "a12", "是"); b.DL("ae24", "a11", "a13", "否")',
    'b.D("ae22", "a10a", "a10q", al=True); b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330); b.D("ae22n", "a10q", "a11", "否", al=True)   # 迴圈菱形（r8）\n'
    'b.H("ae23", "a11", "a12", "是"); b.DL("ae24", "a11", "a13", "否")')

# ---- install(1)：i4en 直接接 i4b；移除 i4ld；i4q 是 → i4l（修復型建日誌）→ i4b ----
rep('''b.box("i4ld", E, 10, v2(D12), "第一次 install（薄殼原本不存在）？", 240, ax="l")
b.box("i4l", E, 10, v2(W12), fl("否（修復型）：建進度日誌 .tmp.install.<id>.toml"), 130, ax="r")''',
'''b.box("i4l", E, 10, v2(W12), fl("是（修復型）：建進度日誌 .tmp.install.<id>.toml（第一個寫入前）"), 240, ax="l")''')
rep('''b.D("ie6", "i4q", "i4ld", "是", al=True); b.D("ie6n", "i4en", "i4ld", al=True)
b.H("ie6l", "i4ld", "i4l", "否"); b.H("ie6lf", "i4l", "i4lf", "寫"); b.D("ie6ly", "i4ld", "i4b", "是", al=True); b.D("ie6ln", "i4l", "i4b", al=True)''',
'''b.D("ie6", "i4q", "i4l", "是", al=True); b.D("ie6n", "i4en", "i4b", al=True)   # 第一次 = 全新建 → 直接建檔，不再問「第一次？」（r8）
b.H("ie6lf", "i4l", "i4lf", "寫"); b.D("ie6ln", "i4l", "i4b", al=True)''')

# ---- install(2)：igx／igz 前各加獨立「刪進度日誌」格 ----
rep('''b.box("igx", U, 7, v2(G12), fl("否 → 0：不寫 .dockerignore、印指示（含 justfile 結果；修復型先刪進度日誌）"), 220)
b.box("igq", E, 7, v2(D12), "有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）", 250, ax="l")
b.box("igz", E, 7, v2(G12), fl("0：印建立了什麼（含 justfile 結果；修復型先刪進度日誌）"), 120, ax="r")''',
'''b.box("idlx", U, 7, v2(W12), fl("否：刪進度日誌 .tmp.install.<id>.toml（修復型才有；最後一步）"), 220)
b.box("igq", E, 7, v2(D12), "有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）", 250, ax="l")
b.box("idlz", E, 7, v2(W12), fl("刪進度日誌 .tmp.install.<id>.toml（修復型才有；最後一步）"), 120, ax="r")
b.box("idlzf", P, 7, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（修復型才有）", 360)
b.box("igx", U, 8, v2(G12), fl("0：不寫 .dockerignore、印指示（含 justfile 結果）"), 220)
b.box("igz", E, 9, v2(G12), fl("0：印建立了什麼（含 justfile 結果）"), 120, ax="r")''')
rep('b.box("igy", E, 8, v2(W12), fl("是：append 三行"), 250, ax="l")\nb.box("igyf", P, 8,',
    'b.box("igy", E, 8, v2(W12), fl("是：append 三行"), 250, ax="l")\nb.box("igyf", P, 8,')
rep('b.H("ie20", "ig", "ign", "無"); b.H("ie20f", "ign", "ignf", "寫"); b.D("ie21", "ig", "igq", "有", al=True); b.D("ie20z", "ign", "igz", al=True)\nb.H("ie22", "igq", "igx", "否");',
    'b.H("ie20", "ig", "ign", "無"); b.H("ie20f", "ign", "ignf", "寫"); b.D("ie21", "ig", "igq", "有", al=True)\n'
    'b.D("ie20z", "ign", "idlz", al=True); b.H("ie20zf", "idlz", "idlzf", "刪"); b.D("ie20zz", "idlz", "igz", al=True)   # 刪日誌獨立格（r8）\n'
    'b.H("ie22", "igq", "idlx", "否"); b.D("ie22x", "idlx", "igx", al=True);')

# ---- add(2)：c20q 與 c20／c20n 拉開（空兩列 = +40px → 線長 60，標籤離框緣）----
for cid, r in [("c20n", 9), ("c20", 9)]:
    rep(f'b.box("{cid}", E, {r}, ', f'b.box("{cid}", E, {r+2}, ')
for cid, r in [("c20l", 10), ("c21", 11), ("c21f", 11), ("c21b", 12), ("c21bf", 12), ("c21c", 13), ("c21cf", 13), ("c21d", 14), ("c21df", 14), ("c22", 15), ("c22f", 15), ("c23", 16), ("c23f", 16), ("c23x", 17), ("c23b", 17), ("c24", 18)]:
    col = "U" if cid in ("c23x", "c24") else ("P" if cid.endswith("f") else "E")
    rep(f'b.box("{cid}", {col}, {r}, ', f'b.box("{cid}", {col}, {r+2}, ')
rep('b.box("c20q", E, 8, v2(D12), "問「要在 X 加這幾行嗎」？（-y 免問）", 320, ax="l")',
    'b.box("c20q", E, 8, v2(D12), "問「要在 X 加這幾行嗎」？（-y 免問）", 320, ax="l")   # 第 9、10 列留空：菱形到 c20／c20n 線長 60，「是」「否」標籤不壓框緣（r8）')

# ---- sync(1)：ne5x 不 T 接（從 n1p 底折進 n1x 頂 0.25）----
rep('b.D("ne5pv", "n1p", "n1v", "", 0.25, 0.5); b.DL("ne5x", "n1p", "n1x", "失敗", 0.75); b.H("ne5y", "n1v", "n1x", "是")',
    'b.D("ne5pv", "n1p", "n1v", "", 0.25, 0.5); b.D("ne5x", "n1p", "n1x", "失敗", 0.75, 0.25, dy=8); b.H("ne5y", "n1v", "n1x", "是")   # 失敗線進紅橢圓頂端，不與「是」T 接（r8）')

# ---- sync(1′)：迴圈菱形 tq，移除浮動文字 nl ----
rep('b.box("nl", G, 2, LBL, "← 對每個工具重複\\n（範圍 = 全部；先比印記，便宜）", 220, 40, minh=40)\n', "")
rep('''b.box("t6", E, 10, v2(D12), fl("gen/tools.just 缺或與工具清單不符？（全部工具看完後）"), 270, ax="l")
b.box("t6y", E, 10, v2(W12), fl("是：列待辦「重生 gen/tools.just」"), 90, ax="r")
b.box("z0", E, 11, v2(SUB),''',
'''b.box("tq", E, 10, v2(D12), "還有工具？", 250, ax="l")
b.box("t6", E, 11, v2(D12), fl("否 → gen/tools.just 缺或與工具清單不符？（全部工具看完後）"), 270, ax="l")
b.box("t6y", E, 11, v2(W12), fl("是：列待辦「重生 gen/tools.just」"), 90, ax="r")
b.box("z0", E, 12, v2(SUB),''')
rep('b.box("z2", U, 12, v2(G12),', 'b.box("z2", U, 13, v2(G12),')
rep('b.box("z1", E, 12, v2(SUB),', 'b.box("z1", E, 13, v2(SUB),')
rep('b.box("mb", E, 13, LBL,', 'b.box("mb", E, 14, LBL,')
rep('b.R("te14", "t4", "t6", "是", busx=990, tx=0.5); b.D("te15", "t5", "t6", al=True)   # 菱形入口頂點（v2.9 §9）',
    'b.R("te14", "t4", "tq", "是", busx=990, tx=0.5); b.D("te15", "t5", "tq", al=True)   # 菱形入口頂點（v2.9 §9）\n'
    'b.P("te15y", "tq", "t0", "是：下一個工具", exit=(1, 0.5), entry=(0.5, 0), pts=None, pos=None, vert="below")   # 迴圈：右側匯流排 x=1000 往上，從 t0 頂點進（pts 在 close 後補）\n'
    'b.D("te15n", "tq", "t6", "否", al=True)')

# ---- sync(2)：m3v 拆「逐檔驗證」→「全部相符？」→ 否「重裝 + warn」----
rep('''b.box("m3v", E, 11, v2(SUB), fl("版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 全驗 cache/<repo>/ ＝ 印記（§3.6；不符 → 重裝 + warn）"), 400)   # v2.9 §3
b.box("m7", U, 12, G12, "0：接著跑原本的 recipe", 220)
b.box("m5", E, 12, v2(SUB), fl("重生 gen/tools.just（待辦有它時；每個 <ns>.just 一行 mod?）"), 400)
b.box("m5f", P, 12, F12, "gen/tools.just（不進 git；gen/.stamp 不動）", 360)''',
'''b.box("m3v", E, 11, v2(SUB), fl("版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）"), 400)   # v2.9 §3
b.box("m3vq", E, 12, v2(D12), "全部相符？", 200, ax="l")
b.box("m3vn", E, 12, v2(SUB), fl("否：重裝該工具 + warn（cache 被改過）"), 150, ax="r")
b.box("m7", U, 13, G12, "0：接著跑原本的 recipe", 220)
b.box("m5", E, 13, v2(SUB), fl("重生 gen/tools.just（待辦有它時；每個 <ns>.just 一行 mod?）"), 400)
b.box("m5f", P, 13, F12, "gen/tools.just（不進 git；gen/.stamp 不動）", 360)''')
rep('b.D("me4v", "m3b", "m3v"); b.D("me5", "m3v", "m5")',
    'b.D("me4v", "m3b", "m3v"); b.D("me4q", "m3v", "m3vq", al=True); b.H("me4n", "m3vq", "m3vn", "否"); b.D("me5", "m3vq", "m5", "是", al=True); b.D("me5n", "m3vn", "m5", al=True)   # 驗證／重裝拆格（r8）')

# ---- B(1′)：b10dx／b10nx 改橙 ----
rep('b.box("b10dx", U, 3, v2(R12), "否 → 1：dest 不合法", 220)', 'b.box("b10dx", U, 3, v2(O12), "否 → 1：dest 不合法", 220)')
rep('b.box("b10nx", U, 4, v2(R12), "是 → 1：命名空間撞名", 220)', 'b.box("b10nx", U, 4, v2(O12), "是 → 1：命名空間撞名", 220)')

# ---- B(2′)：b18 加「除解析失敗檔外」----
rep('b.box("b18", E, 8, O12, fl("是 → 2：印衝突檔名（含解析失敗的檔；解完再跑直到乾淨；baseline 已在目標版）"), 360)',
    'b.box("b18", E, 8, O12, fl("是 → 2：印衝突檔名（含解析失敗的檔；解完再跑直到乾淨；baseline 已在目標版，除解析失敗檔外）"), 360)')

# ---- E 名詞表：upgrade vendor_kit 不建進度日誌 ----
rep(''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）"),''',
''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗；不建日誌）"),
 ("upgrade vendor_kit 不建進度日誌（v2.10）", "進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）"),''')

# ---- E(a)(b)：s2lx 文字；se6px 不 T 接 ----
rep('b.box("s2lx", E, 11, v2(R12), fl("拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"), 240, ax="l")',
    'b.box("s2lx", E, 11, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產）"), 240, ax="l")')
rep('b.D("se6pv", "s2lp", "s2lv", "", 0.25, 0.5); b.DL("se6px", "s2lp", "s2lx", "失敗", 0.75); b.H("se6vx", "s2lv", "s2lx", "是")',
    'b.D("se6pv", "s2lp", "s2lv", "", 0.25, 0.5); b.D("se6px", "s2lp", "s2lx", "失敗", 0.75, 0.25, dy=8); b.H("se6vx", "s2lv", "s2lx", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）')

# ---- E(c)(1)：不建日誌字樣；se11px 不 T 接 ----
rep('b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗 → 薄殼 == 上次產物？',
    'b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗（不建日誌，v2.10）→ 薄殼 == 上次產物？')
rep('b.box("s12w", E, 11, v2(SUB), fl("是：改 version.toml 第一行 = 新引擎 ref（其餘不動）"), 260, ax="l")',
    'b.box("s12w", E, 11, v2(SUB), fl("是：改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動、不建日誌）"), 260, ax="l")')
rep('b.D("se11pv", "s11p", "s11v", "", 0.25, 0.5); b.DL("se11px", "s11p", "s11x", "失敗", 0.75); b.H("se11vx", "s11v", "s11x", "是")',
    'b.D("se11pv", "s11p", "s11v", "", 0.25, 0.5); b.D("se11px", "s11p", "s11x", "失敗", 0.75, 0.25, dy=8); b.H("se11vx", "s11v", "s11x", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）')

# ---- E(c)(2)：不建／刪日誌；s13x 拆兩個結束 ----
rep('已是本引擎產物？→ 是 → 0 無變更；否 → 建日誌 → 重產薄殼四檔 + gen/.stamp + tools.just → 刪日誌 → 1", v2=True)',
    '已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼四檔 + gen/.stamp + tools.just（不建日誌，v2.10；未完成由第一行 ≠ gen/.stamp 辨識）→ 1", v2=True)')
rep('b.box("s12l", E, 2, v2(SUB), "否：建進度日誌（第一個寫入前）", 360)\n', "")
rep('b.box("s13", E, 3, v2(SUB), "重產薄殼四檔（暫存 → 原子替換）", 360)', 'b.box("s13", E, 2, v2(SUB), "否：重產薄殼四檔（暫存 → 原子替換）", 360)')
rep('b.files("s13f", P, 3,', 'b.files("s13f", P, 2,')
rep('b.box("s13b", E, 4, v2(SUB),', 'b.box("s13b", E, 3, v2(SUB),'); rep('b.box("s13bf", P, 4,', 'b.box("s13bf", P, 3,')
rep('b.box("s13c", E, 5, v2(SUB),', 'b.box("s13c", E, 4, v2(SUB),'); rep('b.box("s13cf", P, 5,', 'b.box("s13cf", P, 4,')
rep('''b.box("s13x", U, 6, v2(O12), fl("失敗 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("s13d", E, 6, v2(SUB), "刪進度日誌（最後一步）", 360)
b.box("s14", U, 7, v2(O12), fl("1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)''',
'''b.box("s14", U, 4, v2(O12), fl("成功 → 1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)
b.box("s13x", U, 5, v2(O12), fl("是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("s13q", E, 5, v2(D12), fl("失敗 → 第一行已改（或又變）？"), 240, ax="r")
b.box("s13xn", E, 6, v2(O12), fl("否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"), 240, ax="r")''')
rep('''b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s12l", "否", al=True)
b.D("se15s", "s12l", "s13"); b.H("se16", "s13", "s13f", "寫")''',
'''b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s13", "否", al=True)
b.H("se16", "s13", "s13f", "寫")''')
rep('b.D("se18d", "s13c", "s13d", "成功", 0.6, 0.5, al=True); b.D("se18x", "s13c", "s13x", "失敗", 0.2, 0.5); b.DL("se19", "s13d", "s14")',
    'b.H("se18d", "s13c", "s14", "成功"); b.D("se18x", "s13c", "s13q", "失敗", 0.75, 0.5, al=True)   # 6-2b 只給第一行已改（v2.10-5）\n'
    'b.H("se19", "s13q", "s13x", "是"); b.D("se19n", "s13q", "s13xn", "否", al=True)')

# ---- dev <repo>：d3a／d1x／d3c 改橙 ----
rep('b.box("d1x", U, 1, v2(R12), "否 → 1：<dir>/dist/init.toml 不存在", 220)', 'b.box("d1x", U, 1, v2(O12), "否 → 1：<dir>/dist/init.toml 不存在", 220)')
rep('b.box("d3a", U, 3, R12, "是 → 1：CI 拒絕 dev", 220)', 'b.box("d3a", U, 3, O12, "是 → 1：CI 拒絕 dev", 220)')
rep('b.box("d3c", U, 4, R12, "否 → 1：dist/ 或 init.toml 不合法", 220)', 'b.box("d3c", U, 4, O12, "否 → 1：dist/ 或 init.toml 不合法", 220)')

open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("ok")
