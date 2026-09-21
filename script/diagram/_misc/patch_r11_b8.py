"""第十一輪 patch 8：sync(1′) 迴圈改走最左匯流排（t3a／t4r 移啟動器欄）、E(a) 小折、E(c)(1) 頁高、x5ef 寬。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)
rep('''b.box("t3a", U, 7, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)''', '''b.box("t3a", L, 7, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)   # 放啟動器欄：讓迴圈匯流排（x=270）不被橫線穿過''')
rep('''b.box("t4r", U, 9, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)''', '''b.box("t4r", L, 9, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)''')
rep('''b.LL("te15y", "tq", "t0", "是：下一個工具", busx=565)   # 迴圈：走啟動器欄與引擎欄之間的左側匯流排回 t0（GHCR 欄改放右側步驟，r11）''',
    '''b.LL("te15y", "tq", "t0", "是：下一個工具", busx=270)   # 迴圈：走使用者欄與啟動器欄之間的最左匯流排回 t0（GHCR 欄改放右側步驟，r11）''')
rep('''b.box("s2h2", L, 10, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 300)
b.box("s2ln", L, 11, v2(D12), "是 → inspect：本機有？", 260, ax=0)''',
'''b.box("s2h2", L, 10, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 280, ax=0)
b.box("s2ln", L, 11, v2(D12), "是 → inspect：本機有？", 280, ax=0)''')
rep('''b.box("s2lv", L, 13, v2(D12), fl("覆寫中且 .Id ≠ 記的 ID？"), 260, ax=0)''', '''b.box("s2lv", L, 13, v2(D12), fl("覆寫中且 .Id ≠ 記的 ID？"), 280, ax=0)''')
rep('''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → inspect／pull → engine_start → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則「E(c)（2）」頁", v2=True)''',
'''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → inspect／pull → engine_start → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌、改第一行 → 新引擎再跑；否則「E(c)（2）」頁", v2=True)''')
rep('''b.box("s12sn", P, 8, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17；install 頁同）；拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)''',
    '''b.box("s12sn", P, 8, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17；install 頁同）；拿鎖重驗後、任何寫入前檢查，不符 → 1 列差異、零寫入（v2.8 §3）"), 360)''')
rep('''"config.toml 副本"], 360, cw=(150, 188))''', '''"config.toml 副本"], 360, cw=(140, 198))''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 8 ok")
