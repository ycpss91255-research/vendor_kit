"""第十一輪 patch 4：upgrade 九頁（A、B(1)(1′)(2)(2′)、逐檔／回退、E(a)(b)、E(c)(1)(2)）。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- T7 ----
rep(''' ("resolve／apply／--dry-run", "resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"),
 ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"),''',
''' RAD_T, FIP_T,''')
rep(''' ("materialize／印記", "引擎內部步驟：apply 決定套用後把目標版 /dist/<repo> 展開到 cache/<repo>/（暫存 → 原子替換）；印記 gen/<repo>.stamp 第一行 index digest，之後每檔 sha256"),''', ''' MP_T,''')
rep(''' ("metadata", "baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"),''', ''' MD_T,''')
rep(''' ("git merge-file --diff3", "git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 > 2 > 0，訊息全列"),''', ''' GM_T,''')

# ---- P7c B(1)：主路徑補線；b8p 紅出口；藍白 ----
rep('''b.box("b6y", E, 6, v2(W12), fl("是：目標版 = B（version.toml 那版），補到就停，不查最新"), 170, ax="r")''', '''b.box("b6y", E, 6, v2(SUB), fl("是：目標版 = B（version.toml 那版），補到就停，不查最新"), 170, ax="r")''')
rep('''b.box("b7t", E, 7, v2(W12), fl("是：目標版 = @<tag>（比現版舊 → warn 仍執行）"), 170, ax="r")''', '''b.box("b7t", E, 7, v2(SUB), fl("是：目標版 = @<tag>（比現版舊 → warn 仍執行）"), 170, ax="r")''')
rep('''b.box("b7z", E, 8, v2(W12), fl("是：不查最新；目標版 = 鎖定版（無事可做）"), 170, ax="r")''', '''b.box("b7z", E, 8, v2(SUB), fl("是：不查最新；目標版 = 鎖定版（無事可做）"), 170, ax="r")''')
rep('''b.box("b7c", E, 9, v2(W12), fl("否：(2) 查 registry 最新正式版 = 目標版"), 170, ax="l")''', '''b.box("b7c", E, 9, v2(SUB), fl("否：(2) 查 registry 最新正式版 = 目標版"), 170, ax="l")''')
rep('''b.box("b8b", L, 13, v2(W12), "docker create <img> /x", 240)''',
'''b.box("b8px", E, 13, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31"), 240, ax="l")   # v2.14-5
b.box("b8b", L, 13, v2(W12), "docker create <img> /x", 240)''')
rep('''b.H("be1", "b0", "b0l"); b.D("be1l", "b0l", "b1"); b.H("be1e", "b1", "b1e"); b.D("be1q", "b1e", "b1q", al=True); b.H("be1x", "b1q", "b1x", "是")   # launcher_start／engine_start（v2.12）; b.D("be2", "b1q", "b2", "否", al=True); b.H("be3", "b2", "b2c", "是")''',
'''b.H("be1", "b0", "b0l"); b.D("be1l", "b0l", "b1"); b.H("be1e", "b1", "b1e"); b.D("be1q", "b1e", "b1q", al=True); b.H("be1x", "b1q", "b1x", "是")   # launcher_start／engine_start（v2.12）
b.D("be2", "b1q", "b2", "否", al=True); b.H("be3", "b2", "b2c", "是")   # r10：第十版註解吃掉這兩條線，主路徑斷掉''')
rep('''b.D("be11", "b7s", "b8a", "", 0.5, 0.5); b.RD("be11n", "b8a", "b8p", "無"); b.H("be12", "b8g", "b8p", "拉 /dist"); b.D("be11y", "b8a", "b8b", "有", al=True); b.D("be11p", "b8p", "b8b", al=True)''',
'''b.D("be11", "b7s", "b8a", "", 0.5, 0.5); b.RD("be11n", "b8a", "b8p", "無"); b.H("be12", "b8g", "b8p", "拉 /dist"); b.D("be11y", "b8a", "b8b", "有", al=True); b.D("be11p", "b8p", "b8b", "", 0.25, 0.5); b.D("be11px", "b8p", "b8px", "失敗", 0.75, 0.25, dy=8)   # pull 失敗紅出口（v2.14-5）''')

# ---- P7ccc B(1′)：apply 容器 engine_start ----
rep('''b.box("b10a", E, 1, v2(SUB), "apply：flock 專案目錄（60 秒）", 360)
b.box("b10b", E, 2, v2(SUB), "重驗 resolve 的輸入指紋", 220, ax="l")
b.box("b10x", E, 2, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("b10dx", U, 3, v2(O12), "否 → 1：dest 不合法", 220)
b.box("b10d", E, 3, v2(D12), fl("新版 init.toml 的 dest 全部合法？（任何寫入前；規則同「add（1）」頁）"), 340, ax="l")
b.box("b10nx", U, 4, v2(O12), "是 → 1：命名空間撞名", 220)
b.box("b10n", E, 4, v2(D12), fl("是 → 新版 just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"), 340, ax="l")
b.box("b10c", E, 5, v2(SUB), fl("否 → 逐檔判斷（B baseline／D 現況／N = 暫存 /dist/<repo>，見「逐檔判斷」頁）→ 詢問清單"), 360)
b.box("b12x", U, 6, v2(O12), "是 → 1：印需改清單（frozen；請在本機 upgrade <repo> -y 後 commit 並 push）", 220)
b.box("b12", E, 6, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("b11y", U, 7, v2(G12), "是 → 0：唯讀預覽（印會問哪些檔）", 220)
b.box("b11", E, 7, D12, "--dry-run？", 240, ax=50)   # 中心與 b12（340 寬）對齊 → 垂直「否」線無小折（v2.9 §9）
b.box("b11z", E, 8, LBL, "否 ↓ 續「B（2）」頁：apply 寫入段", 300, 24, ax="l", minh=24)
b.D("be13e", "b8e", "b9"); b.H("be14", "b9", "b10a"); b.D("be15", "b10a", "b10b", al=True); b.H("be15x", "b10b", "b10x")''',
'''b.box("b9e", E, 1, v2(SUB), EST, 360)   # apply 容器（v2.14-2）
b.box("b10a", E, 2, v2(SUB), "apply：flock 專案目錄（60 秒）", 360)
b.box("b10b", E, 3, v2(SUB), "重驗 resolve 的輸入指紋", 220, ax="l")
b.box("b10x", E, 3, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("b10dx", U, 4, v2(O12), "否 → 1：dest 不合法", 220)
b.box("b10d", E, 4, v2(D12), fl("新版 init.toml 的 dest 全部合法？（任何寫入前；規則同「add（1）」頁）"), 340, ax="l")
b.box("b10nx", U, 5, v2(O12), "是 → 1：命名空間撞名", 220)
b.box("b10n", E, 5, v2(D12), fl("是 → 新版 just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"), 340, ax="l")
b.box("b10c", E, 6, v2(SUB), fl("否 → 逐檔判斷（B baseline／D 現況／N = 暫存 /dist/<repo>，見「逐檔判斷」頁）→ 詢問清單"), 360)
b.box("b12x", U, 7, v2(O12), "是 → 1：印需改清單（frozen；請在本機 upgrade <repo> -y 後 commit 並 push）", 220)
b.box("b12", E, 7, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("b11y", U, 8, v2(G12), "是 → 0：唯讀預覽（印會問哪些檔）", 220)
b.box("b11", E, 8, D12, "--dry-run？", 240, ax=50)   # 中心與 b12（340 寬）對齊 → 垂直「否」線無小折（v2.9 §9）
b.box("b11z", E, 9, LBL, "否 ↓ 續「B（2）」頁：apply 寫入段", 300, 24, ax="l", minh=24)
b.D("be13e", "b8e", "b9"); b.H("be14", "b9", "b9e"); b.D("be14e", "b9e", "b10a"); b.D("be15", "b10a", "b10b", al=True); b.H("be15x", "b10b", "b10x")''')

# ---- P7cc B(2)：b13a 拆兩格；逐檔改「情況菱形（是：問）→ 同意？」兩層，每菱形兩出邊；藍白 ----
rep('''b = F.band("uB2", "B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔詢問（四種情況各一問）→ 暫存合併 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換（§4.3）；收尾見「B（2′）」頁", v2=True)''',
'''b = F.band("uB2", "B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔：判定情況 → 問 6-22 → 同意？→ 在暫存套用／不動 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換（§4.3）；收尾見「B（2′）」頁", v2=True)''')
rep('''b.box("b13a", E, 3, v2(SUB), fl("materialize 目標版：/dist/<repo> → 暫存 → cache/<repo>/（原子替換）"), 360)
b.box("b13f", P, 3, F12, "cache/<repo>/（目標版，不進 git）", 280)
b.box("b13b", E, 4, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 360)
b.box("b13bf", P, 4, F12, "gen/<repo>.stamp（不進 git）", 280)
b.box("bl", E, 5, LBL, "↓ 逐檔（每檔恰一種情況，依「逐檔判斷」頁；不是該情況就看下一格；-y 免問）", 360, 24, minh=24)
b.box("b14q1", E, 6, v2(D12), fl("文字檔：你沒改、新版改了 → 問「X 換成新版？」"), 240, ax=0)
b.box("b14a", E, 6, v2(W12), "是：換新版（在暫存）", 90, ax="r")
b.box("b14q1b", E, 7, v2(D12), fl("二進位／symlink 你沒改、新版改了 → 問「是二進位檔，換新版？」"), 240, ax=0)
b.box("b14ab", E, 7, v2(W12), "是：換新版（在暫存）", 90, ax="r")
b.box("b14q2", E, 8, v2(D12), fl("兩邊都改 → 問「都改了 X，要三方合併嗎？」"), 240, ax=0)
b.box("b14b", E, 8, v2(W12), fl("是：git merge-file --diff3（在暫存）"), 90, ax="r")
b.box("b14q3", E, 9, v2(D12), fl("append 行找到上次插入的行 → 問「要替換嗎？」"), 240, ax=0)
b.box("b14c", E, 9, v2(W12), "是：append 行替換（在暫存）", 90, ax="r")
b.box("b14q4", E, 10, v2(D12), fl("新版新增（B 無）→ 問「要建 X 嗎」"), 240, ax=0)
b.box("b14d", E, 10, v2(W12), fl("是：建新檔（已有同名 → 不納管）"), 90, ax="r")
b.box("b14r", P, 10, v2(RULE), fl("Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑時訊息醒目"), 280)
b.box("b14n", E, 11, v2(W12), fl("否：不動該檔；已納管檔 state 不變只記 declined_hash，新檔被拒 → state=declined（新版再更新時再問）"), 280, ax=-100)
b.box("b14m", E, 12, v2(SUB), fl("暫存合併完成（每檔已定：換新版／合併／替換／建新／不動；都還在暫存）→ TOML／just 等可解析格式先重新解析"), 360)
b.box("b14pc", E, 13, v2(W12), fl("是：留原檔、記 conflicts（baseline 不推）"), 90, ax="l")
b.box("b14pq", E, 13, v2(D12), fl("可解析格式：重新解析失敗？"), 240, ax="r")   # §4.3、v2.9 §4：解析在替換前
b.box("b14w", E, 14, v2(SUB), fl("否：通過的檔逐檔原子替換（暫存 → 正式位置）"), 240, ax="r")
b.box("b14f", P, 14, F12, "初始檔（合併後；衝突留 <<<<<<< vendor_kit:baseline 標記）", 280)
b.box("b14z", E, 15, LBL, "↓ 續「B（2′）」頁：baseline（解析失敗的檔不推）→ metadata → tools.just → version.toml → 刪日誌", 360, 24, minh=24)
b.D("be20", "b10z", "b10e"); b.H("be20f", "b10e", "b10ef", "寫"); b.D("be20b", "b10e", "b10f"); b.H("be20ff", "b10f", "b10ff", "寫")
b.D("be21", "b10f", "b13a"); b.H("be21f", "b13a", "b13f", "寫"); b.D("be21b", "b13a", "b13b"); b.H("be21bf", "b13b", "b13bf", "寫")
b.D("be22", "b13b", "bl"); b.D("be22a", "bl", "b14q1", "", 0.5, 0.5, al=True)
b.H("be22y1", "b14q1", "b14a", "是"); b.D("be22n1", "b14q1", "b14q1b", al=True); b.LD("be22x1", "b14q1", "b14n", "否", busx=700, vert="below")
b.H("be22y1b", "b14q1b", "b14ab", "是"); b.D("be22n1b", "b14q1b", "b14q2", al=True); b.LD("be22x1b", "b14q1b", "b14n", "否", busx=690, vert="below")
b.H("be22y2", "b14q2", "b14b", "是"); b.D("be22n2", "b14q2", "b14q3", al=True); b.LD("be22x2", "b14q2", "b14n", "否", busx=680, vert="below")
b.H("be22y3", "b14q3", "b14c", "是"); b.D("be22n3", "b14q3", "b14q4", al=True); b.LD("be22x3", "b14q3", "b14n", "否", busx=670, vert="below")
b.H("be22y4", "b14q4", "b14d", "是"); b.LD("be22x4", "b14q4", "b14n", "否", busx=660, vert="below")
b.R("be23a", "b14a", "b14m", "", busx=1110, tx=0.9); b.R("be23ab", "b14ab", "b14m", "", busx=1110, tx=0.9); b.R("be23b", "b14b", "b14m", "", busx=1110, tx=0.9); b.R("be23c", "b14c", "b14m", "", busx=1110, tx=0.9); b.R("be23d", "b14d", "b14m", "", busx=1110, tx=0.9)
b.D("be23n", "b14n", "b14m", al=True); b.D("be23m", "b14m", "b14pq", al=True); b.H("be23pc", "b14pq", "b14pc", "是"); b.D("be23pw", "b14pq", "b14w", "否", al=True)''',
'''b.box("b13a", E, 3, v2(SUB), fl("materialize 目標版：/dist/<repo> 複製到暫存目錄"), 360)
b.box("b13ac", E, 4, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 360)   # r10：materialize／原子替換拆兩格
b.box("b13f", P, 4, F12, "cache/<repo>/（目標版，不進 git）", 280)
b.box("b13b", E, 5, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 360)
b.box("b13bf", P, 5, F12, "gen/<repo>.stamp（不進 git）", 280)
b.box("bl", E, 6, LBL, "↓ 逐檔（每檔恰一種情況，依「逐檔判斷」頁；是 → 問 6-22 → 同意？；-y 免問）", 360, 24, minh=24)
b.box("b14q1", E, 7, v2(D12), fl("文字檔、你沒改、新版改了？→ 問「X 換成新版？」"), 360, ax=0)   # r10：每菱形兩出邊（是：問；否：下一情況）
b.box("b14q1b", E, 8, v2(D12), fl("二進位／symlink、你沒改、新版改了？→ 問「是二進位檔，換新版？」"), 360, ax=0)
b.box("b14q2", E, 9, v2(D12), fl("兩邊都改？→ 問「都改了 X，要三方合併嗎？」"), 360, ax=0)
b.box("b14q3", E, 10, v2(D12), fl("append 行找到上次插入的行？→ 問「要替換嗎？」"), 360, ax=0)
b.box("b14q4", E, 11, v2(D12), fl("新版新增（B 無）？→ 問「要建 X 嗎」"), 360, ax=0)
b.box("b14r", P, 11, v2(RULE), fl("Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑時訊息醒目"), 280)
b.box("b14y", E, 12, v2(D12), "同意？（-y 免問）", 200, ax="r")
b.box("b14n", P, 12, v2(SUB), fl("否：不動該檔；已納管檔 state 不變只記 declined_hash，新檔被拒 → state=declined（新版再更新時再問）"), 280)
b.box("b14x", E, 13, v2(SUB), fl("是：依情況在暫存套用（換新版／git merge-file --diff3／append 行替換／建新檔，已有同名 → 不納管）"), 300, ax="r")
b.box("b14m", E, 14, v2(SUB), fl("暫存合併完成（每檔已定：換新版／合併／替換／建新／不動；都還在暫存）→ TOML／just 等可解析格式先重新解析"), 360)
b.box("b14pc", E, 15, v2(SUB), fl("是：留原檔、記 conflicts（baseline 不推）"), 90, ax="l")
b.box("b14pq", E, 15, v2(D12), fl("可解析格式：重新解析失敗？"), 240, ax="r")   # §4.3、v2.9 §4：解析在替換前
b.box("b14w", E, 16, v2(SUB), fl("否：通過的檔逐檔原子替換（暫存 → 正式位置）"), 240, ax="r")
b.box("b14f", P, 16, F12, "初始檔（合併後；衝突留 <<<<<<< vendor_kit:baseline 標記）", 280)
b.box("b14z", E, 17, LBL, "↓ 續「B（2′）」頁：baseline（解析失敗的檔不推）→ metadata → tools.just → version.toml → 刪日誌", 360, 24, minh=24)
b.D("be20", "b10z", "b10e"); b.H("be20f", "b10e", "b10ef", "寫"); b.D("be20b", "b10e", "b10f"); b.H("be20ff", "b10f", "b10ff", "寫")
b.D("be21", "b10f", "b13a"); b.D("be21a", "b13a", "b13ac"); b.H("be21f", "b13ac", "b13f", "寫"); b.D("be21b", "b13ac", "b13b"); b.H("be21bf", "b13b", "b13bf", "寫")
b.D("be22", "b13b", "bl"); b.D("be22a", "bl", "b14q1", "", 0.5, 0.5, al=True)
b.R("be22y1", "b14q1", "b14y", "是", busx=1110, tx=0.5); b.D("be22n1", "b14q1", "b14q1b", "否", al=True)
b.R("be22y1b", "b14q1b", "b14y", "是", busx=1110, tx=0.5); b.D("be22n1b", "b14q1b", "b14q2", "否", al=True)
b.R("be22y2", "b14q2", "b14y", "是", busx=1110, tx=0.5); b.D("be22n2", "b14q2", "b14q3", "否", al=True)
b.R("be22y3", "b14q3", "b14y", "是", busx=1110, tx=0.5); b.D("be22n3", "b14q3", "b14q4", "否", al=True)
b.R("be22y4", "b14q4", "b14y", "是", busx=1110, tx=0.5); b.LD("be22n4", "b14q4", "b14m", "否：不是任何情況 = 不動", busx=760, vert="left")
b.H("be23n", "b14y", "b14n", "否"); b.D("be23y", "b14y", "b14x", "是", al=True)
b.D("be23nm", "b14n", "b14m", "", 0.5, 0.9); b.D("be23x", "b14x", "b14m", al=True); b.D("be23m", "b14m", "b14pq", al=True); b.H("be23pc", "b14pq", "b14pc", "是"); b.D("be23pw", "b14pq", "b14w", "否", al=True)''')

# ---- P7cccc B(2′)：頁尾 launcher_exit ----
rep('''b.box("b17", U, 7, v2(G12), "否 → 0：印摘要 → commit", 220)''',
'''b.box("b17", U, 7, v2(G12), "否 → 0：印摘要 → commit", 220)
b.box("b17l", L, 7, v2(W12), LXT, 240)''')
rep('''b.D("be28q", "b16b", "b16q", al=True); b.H("be28", "b16q", "b17", "否"); b.D("be29", "b16q", "b18", "是", al=True)''',
'''b.D("be28q", "b16b", "b16q", al=True); b.H("be28", "b16q", "b17l", "否"); b.H("be28l", "b17l", "b17"); b.D("be29", "b16q", "b18", "是", al=True)   # 頁尾 launcher_exit（v2.14-2）''')

# ---- T7B ----
rep(''' ("B／D／N", "B = baseline（上次合併時的範本副本，進 git）；D = 現況（專案裡你的那份檔）；N = 目標版範本 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過"),''', ''' BDN_T,''')
rep(''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（查目標版、輸出要拉的 image 與輸入指紋，不寫檔）→ 啟動器 docker 拉 image、展開到暫存 → apply 拿 flock 後重驗指紋才寫"),''', ''' RA_T,''')
rep(''' ("metadata", "baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行、衝突中檔案清單、進度日誌 state；衝突重入靠它的「衝突中檔案」清單"),
 ("git merge-file --diff3", "git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤）；回傳衝突數 → 映射為結束狀態 2"),''',
''' MD_T, GM_T,''')
rep(''' ("GHCR／image／印記／declined／declined_hash", "GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；印記 = gen/<repo>.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（= 被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）"),''',
''' ("印記／declined／declined_hash", "印記 = gen/<repo>.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）"),''')
# ---- P7b：cx3 改成文字標籤（無出邊的續頁）；回退 d2c 拆三格、d1p 紅出口 ----
rep('''b.free("cx3", v2(W12), "否：apply 拿鎖、建日誌後清除衝突狀態 → 接「B. 手動路徑（1）」頁的 (1)(2)（version.toml、baseline 已在目標版 → 通常「不動」）", 730, cy2 + 110, 340, 40)''',
'''b.free("cx3", v2(LBL), "否 ↓ apply 拿鎖、建日誌後清除衝突狀態 → 接「B. 手動路徑（1）」頁的 (1)(2)（version.toml、baseline 已在目標版 → 通常「不動」）", 730, cy2 + 110, 340, 40)   # 續頁文字（r10 dangling）''')
rep('''b.box("d1c", L, 3, W12, "docker create <img> /x", 240)
b.box("d1d", L, 4, W12, "docker cp c:/dist/. <tmp>/<repo>/", 240)
b.box("d1e", L, 5, W12, "docker rm 該容器", 240)
b.box("d1f", L, 6, W12, "docker run … -v <tmp>:/dist:ro 引擎 apply sync", 240)
b.box("d2c", E, 6, SUB, fl("materialize 舊版 → cache/<repo>/、寫印記（只寫 cache/、gen/；初始檔與 baseline 不碰）"), 360)
b.box("d3", P, 6, F12, fl("cache/<repo>/、gen/<repo>.stamp（舊版；sync 寫）"), 280)
b.H("de1", "d0", "d1a"); b.H("de2", "d1a", "d2"); b.D("de2b", "d2", "d1b", "", 0.5, 0.5); b.RD("de2n", "d1b", "d1p", "無"); b.H("de2g", "d1g", "d1p", "拉 /dist")
b.D("de2y", "d1b", "d1c", "有", al=True); b.D("de2p", "d1p", "d1c", al=True); b.D("de2d", "d1c", "d1d"); b.D("de2e", "d1d", "d1e"); b.D("de2f", "d1e", "d1f")
b.H("de2h", "d1f", "d2c"); b.H("de3", "d2c", "d3", "寫"); b.D("de4", "d0", "d3b")''',
'''b.box("d1px", E, 3, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31"), 240, ax="l")   # v2.14-5
b.box("d1c", L, 3, W12, "docker create <img> /x", 240)
b.box("d1d", L, 4, W12, "docker cp c:/dist/. <tmp>/<repo>/", 240)
b.box("d1e", L, 5, W12, "docker rm 該容器", 240)
b.box("d1f", L, 6, W12, "docker run … -v <tmp>:/dist:ro 引擎 apply sync", 240)
b.box("d2c", E, 6, SUB, fl("materialize 舊版：/dist/<repo> 複製到暫存目錄（初始檔與 baseline 不碰）"), 360)   # r10：拆三格
b.box("d2c2", E, 7, SUB, fl("暫存 → cache/<repo>/（原子替換）"), 360)
b.box("d3", P, 7, F12, fl("cache/<repo>/（舊版；sync 寫）"), 280)
b.box("d2c3", E, 8, SUB, fl("寫印記 gen/<repo>.stamp（舊版 index digest）"), 360)
b.box("d3s", P, 8, F12, fl("gen/<repo>.stamp（舊版；sync 寫）"), 280)
b.H("de1", "d0", "d1a"); b.H("de2", "d1a", "d2"); b.D("de2b", "d2", "d1b", "", 0.5, 0.5); b.RD("de2n", "d1b", "d1p", "無"); b.H("de2g", "d1g", "d1p", "拉 /dist")
b.D("de2y", "d1b", "d1c", "有", al=True); b.D("de2p", "d1p", "d1c", "", 0.25, 0.5); b.D("de2px", "d1p", "d1px", "失敗", 0.75, 0.25, dy=8); b.D("de2d", "d1c", "d1d"); b.D("de2e", "d1d", "d1e"); b.D("de2f", "d1e", "d1f")
b.H("de2h", "d1f", "d2c"); b.D("de2i", "d2c", "d2c2"); b.H("de3", "d2c2", "d3", "寫"); b.D("de2j", "d2c2", "d2c3"); b.H("de3s", "d2c3", "d3s", "寫"); b.D("de4", "d0", "d3b")''')

# ---- T7E ----
rep(''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗、建日誌）"),''',
''' RA_T, E2B_T,''')
rep(''' ("gen/.stamp", "不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）"),''', ''' GS_T, GT_T,''')
rep(''' ("metadata", "baseline/<repo>/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列"),
 ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪"),''',
''' MD_T, FIP_T,''')
rep(''' ("自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）", "(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：frozen 不查／@<tag> 為目標／查 registry → 目標 ≠ 現 ref → 建日誌、改第一行、用新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3"),''',
''' ("自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）", "(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3"),''')
rep('''N7E = "已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。"''',
'''N7E = "已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：(a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎（覆寫時驗 image ID）跑 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更；結束 1 = 需要人動作（橙）。"''')

# ---- P7bc E(a)(b)：resolve／apply 容器各一格 engine_start；s4 綠終點去 1；文字精簡 ----
rep('''b.box("s1", L, 1, v2(W12), "docker run 舊引擎 resolve upgrade（全部）", 280)
b.box("s2a", E, 1, v2(SUB), fl("resolve（已 append engine_start）：先完整預檢（含 dev 中工具 → 1 提示 undev）"), 360)
b.box("s2n", U, 2, v2(G12), "否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）", 220)
b.box("s2q", E, 2, v2(D12), "引擎有新版？", 240, ax="l")
b.box("s2b", E, 3, v2(SUB), "是：apply（舊引擎）：flock 專案目錄", 360)
b.box("s2c", E, 4, v2(SUB), "重驗指紋（不同 → 1「請重跑」，橙）", 360)
b.box("s2d", E, 5, v2(SUB), fl("建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 360)
b.box("s2df", P, 5, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 280)
b.box("s2e", E, 6, v2(SUB), fl("只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令；日誌留給新引擎）"), 360)
b.box("s2f", P, 6, F12, "version.toml 第一行 = 新引擎 ref", 280)
b.box("s2h", L, 7, v2(W12), fl("apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）"), 280)
b.box("s2hx", U, 8, v2(R12), fl("否 → 1：apply 未改第一行（印 apply 的錯誤）"), 220)
b.box("s2h2", L, 8, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 240)
b.box("s2ln", L, 9, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)
b.box("s2lp", L, 10, v2(W12), "無：docker pull 新引擎", 80, ax="r")
b.box("s2gi", G, 10, IMG, "vendor_kit:vY\\n（新引擎）", 200)
b.box("s2lv", L, 11, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=50)
b.box("s2lx", E, 11, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產；日誌保留）"), 240, ax="l")
b.box("s4", U, 12, v2(G12), fl("→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）"), 220)
b.box("s2r", L, 12, v2(W12), "否：docker run 新引擎 upgrade vendor_kit", 320)
b.box("s5", U, 13, v2(G12), "(b) 別人 pull 後（第一行已變）打任何 just", 220)
b.box("s6a", L, 13, v2(W12), "啟動器：grep version.toml 第一行（已寫 launcher_start）", 280)
b.box("s8", U, 14, v2(O12), fl("否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）"), 220)
b.box("s6q", L, 14, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 240)
b.box("s6y", L, 15, G12, "是 → 正常跑（「sync（1）」頁）", 240)
b.H("se1", "s0", "s0l"); b.D("se1l", "s0l", "s1"); b.H("se2", "s1", "s2a"); b.D("se2q", "s2a", "s2q", al=True); b.H("se2n", "s2q", "s2n", "否")
b.D("se3", "s2q", "s2b", "是", al=True); b.D("se3c", "s2b", "s2c"); b.D("se3d", "s2c", "s2d"); b.H("se3df", "s2d", "s2df", "寫"); b.D("se3e", "s2d", "s2e"); b.H("se4", "s2e", "s2f", "寫")''',
'''b.box("s1", L, 1, v2(W12), "docker run 舊引擎 resolve upgrade（全部）", 280)
b.box("s2a0", E, 1, v2(SUB), EST, 360)   # resolve 容器（v2.14-2：從括號改獨立格）
b.box("s2a", E, 2, v2(SUB), fl("resolve：先完整預檢（含 dev 中工具 → 1 提示 undev）"), 360)
b.box("s2n", U, 3, v2(G12), "否 → 只升工具（每個工具走「B（1）」頁；Q27 彙總）", 220)
b.box("s2q", E, 3, v2(D12), "引擎有新版？", 240, ax="l")
b.box("s2r0", L, 4, v2(W12), "是：docker run 舊引擎 apply upgrade", 280)
b.box("s2b0", E, 4, v2(SUB), EST, 360)   # apply 容器（v2.14-2）
b.box("s2b", E, 5, v2(SUB), "apply（舊引擎）：flock 專案目錄", 360)
b.box("s2c", E, 6, v2(SUB), "重驗指紋（不同 → 1「請重跑」，橙）", 360)
b.box("s2d", E, 7, v2(SUB), fl("建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 360)
b.box("s2df", P, 7, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 280)
b.box("s2e", E, 8, v2(SUB), fl("只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令；日誌留給新引擎）"), 360)
b.box("s2f", P, 8, F12, "version.toml 第一行 = 新引擎 ref", 280)
b.box("s2h", L, 9, v2(W12), fl("apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）"), 280)
b.box("s2hx", U, 10, v2(R12), fl("否 → 1：apply 未改第一行（印 apply 的錯誤）"), 220)
b.box("s2h2", L, 10, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 300)
b.box("s2ln", L, 11, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)
b.box("s2lp", L, 12, v2(W12), "無：docker pull 新引擎", 80, ax="r")
b.box("s2gi", G, 12, IMG, "vendor_kit:vY\\n（新引擎）", 200)
b.box("s2lv", L, 13, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=50)
b.box("s2lx", E, 13, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產；日誌保留）"), 240, ax="l")
b.box("s4", U, 14, v2(G12), fl("→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內接手）"), 220)   # 綠終點不含 1／2／3（lint endcolor）
b.box("s2r", L, 14, v2(W12), "否：docker run 新引擎 upgrade vendor_kit", 320)
b.box("s5", U, 15, v2(G12), "(b) 別人 pull 後（第一行已變）打任何 just", 220)
b.box("s6a", L, 15, v2(W12), "啟動器：grep version.toml 第一行（已寫 launcher_start）", 280)
b.box("s8", U, 16, v2(O12), fl("否 → 1：印 6-1「vendor_kit 已更新 vX → vY，請執行 upgrade vendor_kit」→ 打 (c)"), 220)
b.box("s6q", L, 16, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 300)
b.box("s6y", L, 17, G12, "是 → 正常跑（「sync（1）」頁）", 240)
b.H("se1", "s0", "s0l"); b.D("se1l", "s0l", "s1"); b.H("se2", "s1", "s2a0"); b.D("se2a", "s2a0", "s2a"); b.D("se2q", "s2a", "s2q", al=True); b.H("se2n", "s2q", "s2n", "否")
b.DL("se3", "s2q", "s2r0", "是"); b.H("se3b0", "s2r0", "s2b0"); b.D("se3b", "s2b0", "s2b"); b.D("se3c", "s2b", "s2c"); b.D("se3d", "s2c", "s2d"); b.H("se3df", "s2d", "s2df", "寫"); b.D("se3e", "s2d", "s2e"); b.H("se4", "s2e", "s2f", "寫")''')

# ---- P7bcc E(c)(1)：engine_start 獨立格；s12hz 續跑線回 s10a；s12tt 藍 ----
rep('''b.box("s11r", L, 5, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 320)
b.box("s12a", E, 5, v2(SUB), "flock 專案目錄（60 秒；已 append engine_start）", 360)
b.box("s12b", E, 6, v2(SUB), "重驗指紋", 220, ax="l")
b.box("s12bx", E, 6, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("s12sx", U, 7, v2(O12), fl("否 → 1：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 340, ax="l")
b.box("s12sn", P, 7, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)
b.box("s12dx", U, 8, v2(O12), fl("是 → 3：印 6-10（無法無損讀現有檔；零寫入）"), 220)
b.box("s12d", E, 8, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀？（P／schema）"), 340, ax="l")
b.box("s12f", E, 9, v2(D12), fl("否 → CI 為真（frozen）？"), 260, ax="l")
b.box("s12fz", E, 9, LBL, "是：不查 registry、不改第一行 → 續「E(c)（2）」頁", 100, ax="r", minh=40)
b.box("s12t", E, 10, v2(D12), fl("否 → 指定 @<tag>？"), 260, ax="l")
b.box("s12tt", E, 10, v2(W12), fl("是：目標 = @<tag>（不查 registry）"), 100, ax="r")
b.box("s12u", E, 11, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 260, ax="l")
b.box("s12v", E, 12, v2(D12), "目標引擎 ref ≠ 現 ref？", 240, ax="l")
b.box("s12vz", E, 12, LBL, "否 → 續「E(c)（2）」頁：薄殼比對與重產", 110, ax="r", minh=40)
b.box("s12j", E, 13, v2(SUB), fl("是：建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 260, ax="l")
b.box("s12jf", P, 13, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 360)
b.box("s12hz", U, 14, v2(ENTRY), fl("續跑：新引擎回到本頁「docker run 該引擎」格再跑一次（第二次第一行又變 → 1 + 6-2b）"), 220)
b.box("s12h", L, 14, v2(W12), fl("啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）"), 300)
b.box("s12w", E, 14, v2(SUB), fl("改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動）"), 260, ax="l")
b.box("s12wf", P, 14, F12, "version.toml 第一行 = 新引擎 ref（進 git）", 360)''',
'''b.box("s11r", L, 5, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 320)
b.box("s12a0", E, 5, v2(SUB), EST, 360)   # 單段容器（v2.14-2：從括號改獨立格）
b.box("s12a", E, 6, v2(SUB), "flock 專案目錄（60 秒）", 360)
b.box("s12b", E, 7, v2(SUB), "重驗指紋", 220, ax="l")
b.box("s12bx", E, 7, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("s12sx", U, 8, v2(O12), fl("否 → 1：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("s12s", E, 8, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 340, ax="l")
b.box("s12sn", P, 8, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)
b.box("s12dx", U, 9, v2(O12), fl("是 → 3：印 6-10（無法無損讀現有檔；零寫入）"), 220)
b.box("s12d", E, 9, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀？（P／schema）"), 340, ax="l")
b.box("s12f", E, 10, v2(D12), fl("否 → CI 為真（frozen）？"), 260, ax="l")
b.box("s12fz", E, 10, LBL, "是：不查 registry、不改第一行 → 續「E(c)（2）」頁", 100, ax="r", minh=40)
b.box("s12t", E, 11, v2(D12), fl("否 → 指定 @<tag>？"), 260, ax="l")
b.box("s12tt", E, 11, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 100, ax="r")
b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 260, ax="l")
b.box("s12v", E, 13, v2(D12), "目標引擎 ref ≠ 現 ref？", 240, ax="l")
b.box("s12vz", E, 13, LBL, "否 → 續「E(c)（2）」頁：薄殼比對與重產", 110, ax="r", minh=40)
b.box("s12j", E, 14, v2(SUB), fl("是：建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 260, ax="l")
b.box("s12jf", P, 14, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 360)
b.box("s12hz", U, 15, v2(ENTRY), fl("續跑：新引擎回到本頁「docker run 該引擎」格再跑一次（第二次第一行又變 → 1 + 6-2b）"), 220)
b.box("s12h", L, 15, v2(W12), fl("啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）"), 300)
b.box("s12w", E, 15, v2(SUB), fl("改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動）"), 260, ax="l")
b.box("s12wf", P, 15, F12, "version.toml 第一行 = 新引擎 ref（進 git）", 360)''')
rep('''b.H("se12", "s11r", "s12a"); b.D("se12b", "s12a", "s12b", al=True);''', '''b.H("se12", "s11r", "s12a0"); b.D("se12a", "s12a0", "s12a"); b.D("se12b", "s12a", "s12b", al=True);''')
rep('''b.H("se12wh", "s12w", "s12h"); b.H("se12hz", "s12h", "s12hz")''', '''b.H("se12wh", "s12w", "s12h"); b.H("se12hz", "s12h", "s12hz"); b.LL("se12hz2", "s12hz", "s10a", "", busx=28)   # 續跑：左側匯流排回到入口 s10a（r10 dangling）''')
rep('''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → grep 第一行 → inspect／pull → 拿鎖、重驗''', '''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → grep 第一行 → inspect／pull → engine_start → 拿鎖、重驗''')

# ---- P7bccc E(c)(2)：gen/.stamp 只記引擎 ref；config.toml 三方合併一格＋檔案框；6-2b 兩出口改紅；頁尾 launcher_exit ----
rep('''b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼五檔 + gen/.stamp + tools.just → 刪 .tmp.upgrade 日誌（有的話；v2.11）→ 1", v2=True)''',
'''b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼五檔 → config.toml 缺則建／三方合併（v2.14-7）→ gen/.stamp → tools.just → 刪 .tmp.upgrade 日誌（v2.11）→ 1", v2=True)''')
rep('''b.box("s13b", E, 3, v2(SUB), "寫 gen/.stamp（本引擎 ref＋log.sh hash）", 360)
b.box("s13bf", P, 3, F12, "gen/.stamp（不進 git）", 360)
b.box("s13c", E, 4, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
b.box("s13cf", P, 4, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("s13d", E, 5, v2(SUB), fl("刪進度日誌 .tmp.upgrade.<id>.toml（有的話；最後一步，由新引擎刪，v2.11）"), 220, ax="l")
b.box("s13df", P, 5, v2(F12), "－.vendor_kit/.tmp.upgrade.<id>.toml（E(a)／E(c)(1) 建的進度日誌）", 360)
b.box("s14", U, 5, v2(O12), fl("成功 → 1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)
b.box("s13x", U, 6, v2(O12), fl("是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（日誌保留）"), 220)
b.box("s13q", E, 6, v2(D12), fl("失敗 → 第一行已改（或又變）？"), 240, ax="r")
b.box("s13xn", E, 7, v2(O12), fl("否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"), 240, ax="r")
b.D("se13", "s12z0", "s12e", al=True)
b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s13", "否", al=True)
b.H("se16", "s13", "s13f", "寫")
b.D("se17", "s13", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
b.D("se18cd", "s13c", "s13d", "成功", 0.25, 0.5, al=True); b.H("se18df", "s13d", "s13df", "刪"); b.H("se18d", "s13d", "s14")''',
'''b.box("s13g", E, 3, v2(SUB), fl("config.toml：缺則建；有則三方合併（B = baseline/vendor_kit/config.toml、D = 現況、N = 新版範本；要改先問 6-22，-y 免問）"), 360)   # v2.14-7
b.box("s13gf", P, 3, v2(F12), "config.toml（進 git；三方合併初始檔）＋ baseline/vendor_kit/config.toml（副本推到新版）", 360)
b.box("s13b", E, 4, v2(SUB), "寫 gen/.stamp（只記本引擎 ref）", 360)   # v2.14-1
b.box("s13bf", P, 4, F12, "gen/.stamp（不進 git）", 360)
b.box("s13c", E, 5, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
b.box("s13cf", P, 5, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("s13d", E, 6, v2(SUB), fl("刪進度日誌 .tmp.upgrade.<id>.toml（有的話；最後一步，由新引擎刪，v2.11）"), 220, ax="l")
b.box("s13df", P, 6, v2(F12), "－.vendor_kit/.tmp.upgrade.<id>.toml（E(a)／E(c)(1) 建的進度日誌）", 360)
b.box("s14l", L, 6, v2(W12), LXT, 300)
b.box("s14", U, 6, v2(O12), fl("成功 → 1：印 6-2「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)
b.box("s13x", U, 7, v2(R12), fl("是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（日誌保留）"), 220)   # 重產失敗 = 寫入失敗 → 紅（與 E(a) 一致）
b.box("s13q", E, 7, v2(D12), fl("失敗 → 第一行已改（或又變）？"), 240, ax="r")
b.box("s13xn", E, 8, v2(R12), fl("否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"), 240, ax="r")
b.D("se13", "s12z0", "s12e", al=True)
b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s13", "否", al=True)
b.H("se16", "s13", "s13f", "寫")
b.D("se17", "s13", "s13g"); b.H("se17f", "s13g", "s13gf", "寫"); b.D("se17b", "s13g", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
b.D("se18cd", "s13c", "s13d", "成功", 0.25, 0.5, al=True); b.H("se18df", "s13d", "s13df", "刪"); b.H("se18d", "s13d", "s14l"); b.H("se18dl", "s14l", "s14")   # 頁尾 launcher_exit（v2.14-2）''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 4 ok")
