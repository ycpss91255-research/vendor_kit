"""第十一輪 patch 7：頁高第二輪（install(1) i4f、sync(1′) 菱形加寬＋右側格移 GHCR 欄、E(c)(1) s12s、uninstall(2) 菱形加寬）。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

rep('''"config.toml（第一次才建）", "config.toml 的 baseline 副本"], 360, cols=2)''', '''"config.toml（第一次）", "config.toml 副本"], 360, cols=2)''')
# sync(1′)：菱形 400 寬（一行）、右側步驟移到 GHCR 欄（本頁沒有 image）、匯流排 1230、迴圈走左側 565
rep('''b.box("nj", E, 1, v2(D12), "偵測到未完成交易？（.tmp.<verb>.*）", 330, ax="l")   # v2.14-4（與 update 同）''', '''b.box("nj", E, 1, v2(D12), "偵測到未完成交易？", 400)   # v2.14-4（與 update 同；.tmp.<verb>.<id>.toml）''')
rep('''b.box("nc", E, 2, v2(D12), "frozen 且有 local 覆寫？", 330, ax="l")''', '''b.box("nc", E, 2, v2(D12), "frozen 且有 local 覆寫？", 400)''')
rep('''b.box("t0", E, 3, v2(D12), "path 覆寫（dev 中）？", 250, ax="l")
b.box("t0s", E, 3, v2(SUB), fl("是：跳過 materialize／verify ↓"), 130, ax="r")''',
'''b.box("t0", E, 3, v2(D12), "path 覆寫（dev 中）？", 400)   # 菱形一行（頁高）；右側步驟放 GHCR 欄（本頁無 image）
b.box("t0s", G, 3, v2(SUB), fl("是：跳過 materialize／verify（仍查 metadata、baseline）↓"), 220)''')
rep('''b.box("t1", E, 4, v2(D12), "cache 缺或印記 ≠ 鎖定 digest？", 250, ax="l")
b.box("t1y", E, 4, v2(SUB), fl("是：列待辦「materialize 鎖定版」（不 verify 舊 cache）"), 130, ax="r")
b.box("t2q", E, 5, v2(D12), fl("否 → --verify／CI／版本變動？"), 250, ax="l")   # §3.6、v2.9 §3
b.box("t2qn", E, 5, v2(SUB), fl("否：不逐檔驗（快）↓"), 130, ax="r")
b.box("t2", E, 6, D12, "是 → 每檔 sha256 ＝ 印記？", 250, ax="l")
b.box("t2n", E, 6, SUB, fl("否：列待辦「重裝 + warn（cache 被改過）」"), 130, ax="r")
b.box("t3a", U, 7, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)
b.box("t3", E, 7, D12, "metadata 有完成標記？", 250, ax="l")''',
'''b.box("t1", E, 4, v2(D12), "cache 缺或印記 ≠ 鎖定？", 400)
b.box("t1y", G, 4, v2(SUB), fl("是：列待辦「materialize 鎖定版」（不 verify 舊 cache）"), 220)
b.box("t2q", E, 5, v2(D12), fl("否 → 逐檔驗？"), 400)   # §3.6、v2.9 §3：只在 --verify、CI、版本變動那次
b.box("t2qn", G, 5, v2(SUB), fl("否：不逐檔驗（快；只在 --verify、CI、版本變動那次驗）↓"), 220)
b.box("t2", E, 6, D12, "是 → 每檔 sha256 ＝ 印記？", 400)
b.box("t2n", G, 6, SUB, fl("否：列待辦「重裝 + warn（cache 被改過）」"), 220)
b.box("t3a", U, 7, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)
b.box("t3", E, 7, D12, "metadata 有完成標記？", 400)''')
rep('''b.box("t4", E, 8, D12, "最後合併版本 ＝ version.toml？", 250, ax="l")
b.box("t4r", U, 9, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)
b.box("t4c", E, 9, D12, "否（落後）→ CI 為真（frozen）？", 250, ax="l")
b.box("t5", E, 10, SUB, fl("否：warn「baseline 落後，請 just vendor_kit upgrade <repo>」（繼續）"), 300, ax="l")
b.box("tq", E, 11, v2(D12), "還有工具？", 270, ax="l")
b.box("t6", E, 12, v2(D12), fl("否 → tools.just 缺或不符？"), 270, ax="l")   # 兩行（頁高 ≤ 2400）；t6y 寫全名 gen/tools.just
b.box("t6y", E, 12, v2(SUB), fl("是：列待辦「重生 gen/tools.just」"), 90, ax="r")''',
'''b.box("t4", E, 8, D12, "最後合併版本 ＝ 鎖定版？", 400)
b.box("t4r", U, 9, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)
b.box("t4c", E, 9, D12, "否（落後）→ frozen？", 400)
b.box("t5", E, 10, SUB, fl("否：warn「baseline 落後，請 just vendor_kit upgrade <repo>」（繼續）"), 400)
b.box("tq", E, 11, v2(D12), "還有工具？", 400)
b.box("t6", E, 12, v2(D12), fl("否 → tools.just 缺或不符？"), 400)   # t6y 寫全名 gen/tools.just
b.box("t6y", G, 12, v2(SUB), fl("是：列待辦「重生 gen/tools.just」"), 220)''')
rep('''b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3", "", busx=990)
b.H("te3", "t1", "t1y", "是"); b.D("te4", "t1", "t2q", "否", al=True); b.R("te5", "t1y", "t3", "", busx=990)
b.H("te3q", "t2q", "t2qn", "否"); b.D("te4q", "t2q", "t2", "是", al=True); b.R("te5q", "t2qn", "t3", "", busx=990)
b.H("te6", "t2", "t2n", "否"); b.D("te7", "t2", "t3", "是", al=True); b.R("te8", "t2n", "t3", "", busx=990)''',
'''b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3", "", busx=1230)
b.H("te3", "t1", "t1y", "是"); b.D("te4", "t1", "t2q", "否", al=True); b.R("te5", "t1y", "t3", "", busx=1230)
b.H("te3q", "t2q", "t2qn", "否"); b.D("te4q", "t2q", "t2", "是", al=True); b.R("te5q", "t2qn", "t3", "", busx=1230)
b.H("te6", "t2", "t2n", "否"); b.D("te7", "t2", "t3", "是", al=True); b.R("te8", "t2n", "t3", "", busx=1230)''')
rep('''b.R("te14", "t4", "tq", "是", busx=990, tx=0.5); b.D("te15", "t5", "tq", al=True)   # 菱形入口頂點（v2.9 §9）''',
    '''b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5); b.D("te15", "t5", "tq", al=True)   # 菱形入口頂點（v2.9 §9）''')
rep('''b.close()
# 迴圈「還有工具？」是 → 回 t0（path 覆寫判斷）：從 tq 右側出、走 x=1020 匯流排往上（R 線匯流排 990 右邊 30px、GHCR 欄空），從 t0 上方縫隙進頂點（r8）
_A = F.abs; _tq, _t0 = _A["tq"], _A["t0"]; _bus = 1020; _ey = _tq[1] + _tq[3] / 2; _gy = F.rt["t0"] - 10; _ax = _t0[0] + _t0[2] / 2
_L1 = _bus - (_tq[0] + _tq[2]); _tot = _L1 + (_ey - _gy) + (_bus - _ax) + (_t0[1] - _gy)
p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bus, _ey), (_bus, _gy), (_ax, _gy)], 2 * ((_L1 / 2) / _tot) - 1, "below"))''',
'''b.LL("te15y", "tq", "t0", "是：下一個工具", busx=565)   # 迴圈：走啟動器欄與引擎欄之間的左側匯流排回 t0（GHCR 欄改放右側步驟，r11）
b.close()''')
# E(c)(1)
rep('''b.box("s12s", E, 8, v2(D12), "薄殼 == 上次產物？（首行 hash）", 340, ax="l")''', '''b.box("s12s", E, 8, v2(D12), "薄殼 == 上次產物？", 340, ax="l")''')
# uninstall(2)
rep('''b.files("x5af", P, 3, "－.vendor_kit/ 薄殼五檔（保護清單內的保留）", [".gitignore", "entry.just", "vendor.just", "log.sh", "ci/check.sh"], 360, cols=2)''',
    '''b.files("x5af", P, 3, "－.vendor_kit/ 薄殼五檔（保護清單內的保留）", [".gitignore", "entry.just", "vendor.just", "log.sh", "ci/check.sh"], 360, cols=3)''')
rep('''b.files("x5ef", P, 8, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml", "config.toml 的 baseline 副本"], 360, cw=(140, 198))''',
    '''b.files("x5ef", P, 8, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml", "config.toml 副本"], 360, cw=(150, 188))''')
rep('''b.box("x6", E, 10, D12, "根 justfile 有我們那一行？", 340, ax="r")''', '''b.box("x6", E, 10, D12, "根 justfile 有我們那一行？", 380, ax="r")''')
rep('''b.box("x7", E, 11, v2(D12), "有 → 問「要刪這一行嗎」？", 340, ax="r")''', '''b.box("x7", E, 11, v2(D12), "有 → 問「要刪這一行嗎」？", 380, ax="r")''')
rep('''b.box("x9a", E, 13, v2(D12), "根 .dockerignore 存在？", 340, ax="r")
b.box("x9b", E, 14, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 340, ax="r")''',
'''b.box("x9a", E, 13, v2(D12), "根 .dockerignore 存在？", 380, ax="r")
b.box("x9b", E, 14, v2(D12), fl("有 → 仍有與紀錄相同的行？"), 380, ax="r")''')
rep('''b.box("x9q", E, 15, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 340, ax="r")''', '''b.box("x9q", E, 15, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 380, ax="r")''')
rep('''b.LD("xe16an", "x9a", "x9z", "無", busx=615, vert="left"); b.LD("xe16bn", "x9b", "x9z", "無", busx=615, vert="left");''',
    '''b.LD("xe16an", "x9a", "x9z", "無", busx=595, vert="left"); b.LD("xe16bn", "x9b", "x9z", "無", busx=595, vert="left");''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 7 ok")
