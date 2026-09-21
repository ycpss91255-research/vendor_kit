"""第十一輪 patch 3：add(1)(1′)(2)、sync(1)(1′)(2)。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- T5B ----
rep(''' ("resolve／apply", "同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）"),''',
''' RA_T, GS_T, VL_T,''')
rep(''' ("materialize／印記", "引擎內部步驟：apply 決定套用後才把 /dist/<repo> 展開到 cache/<repo>/；印記 = gen/<repo>.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）"),''',
''' MP_T,''')
rep(''' ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）"),''',
''' BM_T,''')
rep(''' ("symlink", "指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕"),''', ''' SYM_T,''')

# ---- P5b add(1)：c8 藍；c9p pull 失敗紅出口 ----
rep('''b.box("c8", E, 7, W12, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 120, ax="r")''', '''b.box("c8", E, 7, SUB, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 120, ax="r")''')
rep('''b.box("c9b", L, 13, v2(W12), "docker create <image> /x", 280)''',
'''b.box("c9px", E, 13, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31（離線可用 --local <tar>）"), 240, ax="l")   # v2.14-5
b.box("c9b", L, 13, v2(W12), "docker create <image> /x", 280)''')
rep('''b.D("ce12y", "c9a", "c9b", "有", al=True); b.D("ce12p", "c9p", "c9b", al=True); b.D("ce12c", "c9b", "c9c"); b.D("ce12d", "c9c", "c9d")''',
'''b.D("ce12y", "c9a", "c9b", "有", al=True); b.D("ce12p", "c9p", "c9b", "", 0.25, 0.5); b.D("ce12px", "c9p", "c9px", "失敗", 0.75, 0.25, dy=8); b.D("ce12c", "c9b", "c9c"); b.D("ce12d", "c9c", "c9d")   # pull 失敗紅出口（v2.14-5）''')

# ---- P5bcc add(1′)：apply 容器 engine_start 獨立格 ----
rep('''b.box("c11a", E, 1, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("c11b", E, 2, v2(SUB), "重驗 resolve 的輸入指紋", 240, ax="l")
b.box("c11x", E, 2, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("c12x", U, 3, v2(O12), "否 → 1：dest 不合法（請修 init.toml／dest；需人動作）", 220)
b.box("c12", E, 3, v2(D12), fl("init.toml 的 dest 全部合法？（任何寫入前檢查）"), 400, ax="l")
b.box("c12r", P, 3, v2(RULE), fl("dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/；dist 含 symlink → 拒絕"), 360)
b.box("c12bx", U, 4, v2(O12), "是 → 1：命名空間撞名（請改名／移除撞名者；需人動作）", 220)
b.box("c12b", E, 4, v2(D12), fl("just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"), 400, ax="l")
b.box("c12br", P, 4, v2(RULE), fl("命名空間撞名（v2.5 §5）：<ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）"), 360)
b.box("c14x", U, 5, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("c14", E, 5, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax=30)
b.box("c13y", U, 6, v2(G12), "是 → 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/<repo>）", 220)
b.box("c13", E, 6, D12, "--dry-run？", 240, ax=80)
b.box("c13z", E, 7, LBL, "否 ↓ 續「add（2）」頁：apply 寫入段", 300, 24, ax="l", minh=24)
b.D("ce13e", "c9e", "c10"); b.H("ce14", "c10", "c11a"); b.D("ce14b", "c11a", "c11b", al=True); b.H("ce15", "c11b", "c11x")''',
'''b.box("c10e", E, 1, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("c11a", E, 2, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("c11b", E, 3, v2(SUB), "重驗 resolve 的輸入指紋", 240, ax="l")
b.box("c11x", E, 3, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("c12x", U, 4, v2(O12), "否 → 1：dest 不合法（請修 init.toml／dest；需人動作）", 220)
b.box("c12", E, 4, v2(D12), fl("init.toml 的 dest 全部合法？（任何寫入前檢查）"), 400, ax="l")
b.box("c12r", P, 4, v2(RULE), fl("dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/；dist 含 symlink → 拒絕"), 360)
b.box("c12bx", U, 5, v2(O12), "是 → 1：命名空間撞名（請改名／移除撞名者；需人動作）", 220)
b.box("c12b", E, 5, v2(D12), fl("just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"), 400, ax="l")
b.box("c12br", P, 5, v2(RULE), fl("命名空間撞名（v2.5 §5）：<ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）"), 360)
b.box("c14x", U, 6, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("c14", E, 6, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax=30)
b.box("c13y", U, 7, v2(G12), "是 → 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/<repo>）", 220)
b.box("c13", E, 7, D12, "--dry-run？", 240, ax=80)
b.box("c13z", E, 8, LBL, "否 ↓ 續「add（2）」頁：apply 寫入段", 300, 24, ax="l", minh=24)
b.D("ce13e", "c9e", "c10"); b.H("ce14", "c10", "c10e"); b.D("ce14e", "c10e", "c11a"); b.D("ce14b", "c11a", "c11b", al=True); b.H("ce15", "c11b", "c11x")''')

# ---- P5bc add(2)：藍白；頁尾 launcher_exit ----
rep('''b.box("c17", E, 6, W12, "無：建該檔（state=managed）", 150, ax="r")''', '''b.box("c17", E, 6, SUB, "無：建該檔（state=managed）", 150, ax="r")''')
rep('''b.box("c19", E, 7, W12, fl("否：不納管（state=unmanaged）、不覆蓋，印「已存在，範本在 cache」"), 180, ax="r")''', '''b.box("c19", E, 7, SUB, fl("否：不納管（state=unmanaged）、不覆蓋，印「已存在，範本在 cache」"), 180, ax="r")''')
rep('''b.box("c20n", E, 11, v2(W12), fl("否：不寫；state=unmanaged 只記 declined_hash"), 150, ax="l")
b.box("c20", E, 11, W12, fl("是：append 那幾行（state=appended；實際插入的行之後記進 metadata）"), 210, ax="r")''',
'''b.box("c20n", E, 11, v2(SUB), fl("否：不寫；state=unmanaged 只記 declined_hash"), 150, ax="l")
b.box("c20", E, 11, SUB, fl("是：append 那幾行（state=appended；實際插入的行之後記進 metadata）"), 210, ax="r")''')
rep('''b.box("c24", U, 20, G12, "成功 → 0：印摘要，提示 git add", 220)''',
'''b.box("c24l", L, 20, v2(W12), LXT, 280)
b.box("c24", U, 20, G12, "成功 → 0：印摘要，提示 git add", 220)''')
rep('''b.H("ce36", "c23", "c23f", "寫"); b.D("ce37", "c23", "c23b", "成功", 0.6, 0.5, al=True); b.D("ce38", "c23", "c23x", "失敗", 0.2, 0.5); b.DL("ce39", "c23b", "c24")''',
'''b.H("ce36", "c23", "c23f", "寫"); b.D("ce37", "c23", "c23b", "成功", 0.6, 0.5, al=True); b.D("ce38", "c23", "c23x", "失敗", 0.2, 0.5); b.D("ce39", "c23b", "c24l"); b.H("ce39l", "c24l", "c24")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- T6 ----
rep(''' ("sync", "工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/<repo>/、gen/tools.just、gen/<repo>.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑"),''',
''' SYNC_T,''')
rep(''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no"),''',
''' RA_T,
 ("待辦清單／apply|no", "resolve sync 把待辦（要拉哪些 image、要重裝什麼、要不要重生 tools.just）以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；無待辦 → apply|no，不起第二個容器"),''')
rep(''' ("frozen（CI 為真）", "CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1"),''',
''' FROZEN_T,''')
rep(''' ("symlink", "指向另一個路徑的捷徑；dev 中的工具 cache/<repo>/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify"),''',
''' SYM_T, E33_T,''')

# ---- P6 sync(1)：ne5q 標籤下移；n1b 後 engine_start 格 ----
rep('''b.box("n1b", L, 7, v2(W12), fl("否：docker run <引擎> resolve sync（永不 -t）"), 280)
b.box("n1z", E, 7, LBL, "→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）", 300, 24, ax="l", minh=24)''',
'''b.box("n1b", L, 7, v2(W12), fl("否：docker run <引擎> resolve sync（永不 -t）"), 280)
b.box("n1be", E, 7, v2(SUB), EST, 400)   # resolve 容器（v2.14-2）
b.box("n1z", E, 8, LBL, "↓ 續「sync（1′）」頁：引擎 resolve sync（逐工具）", 300, 24, ax="l", minh=24)''')
rep('''b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.H("ne5q", "nq", "nql", "是"); b.D("ne5ql", "nql", "nq0", al=True); b.D("ne5n", "nq", "n1i", "否", al=True)   # 快路徑寫 log 才結束（v2.12）''',
'''b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.P("ne5q", "nq", "nql", "是", (0, 0.5), (1, 0.5), (), pos=0, vert="below"); b.D("ne5ql", "nql", "nq0", al=True); b.D("ne5n", "nq", "n1i", "否", al=True)   # 快路徑寫 log 才結束（v2.12）；「是」放線下，不碰 nql 的 v2 標（r10）''')
rep('''b.D("ne5i", "n1v", "n1b", "否", al=True); b.H("ne6", "n1b", "n1z")''', '''b.D("ne5i", "n1v", "n1b", "否", al=True); b.H("ne6", "n1b", "n1be"); b.D("ne6e", "n1be", "n1z", al=True)''')

# ---- P6cc sync(1′)：6-33 菱形；藍白；頁尾 launcher_exit ----
rep('''b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync（已寫 launcher_start、engine_start）", 400)
b.box("ncx", U, 1, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev）", 220)
b.box("nc", E, 1, v2(D12), "CI 為真（frozen）且有 local 覆寫？", 330, ax="l")
b.box("nf", P, 1, v2(RULE), fl("frozen（CI 為真 = CI 非空且不為 0／false；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；任何需要寫 tracked 檔 → 1（-y 不解除）；升為失敗的警告：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫"), 360)
b.box("t0", E, 2, v2(D12), "path 覆寫（dev 中）？", 250, ax="l")
b.box("t0s", E, 2, v2(W12), fl("是：跳過 materialize／verify，仍查 metadata、baseline ↓"), 130, ax="r")
b.box("t0r", P, 2, v2(RULE), fl("覆寫兩種（v2.1 B）：引擎 vendor_kit = \\"<tag>\\"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 <repo> = \\"path:<dir>\\" → cache/<repo>/ 是 symlink，跳過 materialize／verify"), 360)
b.box("t1", E, 3, v2(D12), "cache 缺或印記 ≠ 鎖定 digest？", 250, ax="l")
b.box("t1y", E, 3, v2(W12), fl("是：列待辦「materialize 鎖定版」（不 verify 舊 cache）"), 130, ax="r")
b.box("t2q", E, 4, v2(D12), fl("否 → --verify／CI／版本變動那次？"), 250, ax="l")   # §3.6、v2.9 §3
b.box("t2qn", E, 4, v2(W12), fl("否：不逐檔驗（快）↓"), 130, ax="r")
b.box("t2", E, 5, D12, "是 → 每檔 sha256 ＝ 印記？", 250, ax="l")
b.box("t2n", E, 5, W12, fl("否：列待辦「重裝 + warn（cache 被改過）」"), 130, ax="r")
b.box("t3a", U, 6, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)
b.box("t3", E, 6, D12, "metadata 有完成標記？", 250, ax="l")
b.box("t3r", P, 6, v2(INV), fl("不變量（v2.1 A、v2.5 §9）：自動化不碰使用者的檔 —— sync 不寫 version.toml、初始檔、baseline、薄殼、gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp"), 360)
b.box("t4", E, 7, D12, "最後合併版本 ＝ version.toml？", 250, ax="l")
b.box("t4r", U, 8, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)
b.box("t4c", E, 8, D12, "否（落後）→ CI 為真（frozen）？", 250, ax="l")
b.box("t5", E, 9, W12, fl("否：warn「baseline 落後，請 just vendor_kit upgrade <repo>」（繼續）"), 300, ax="l")
b.box("tq", E, 10, v2(D12), "還有工具？", 270, ax="l")
b.box("t6", E, 11, v2(D12), fl("否 → tools.just 缺或不符？"), 270, ax="l")   # 兩行（頁高 ≤ 2400）；t6y 寫全名 gen/tools.just
b.box("t6y", E, 11, v2(W12), fl("是：列待辦「重生 gen/tools.just」"), 90, ax="r")
b.box("z0", E, 12, v2(SUB), fl("resolve 完：產生待辦清單（要拉的 image、要重裝、要重生 gen/tools.just）→ 空 = apply|no"), 400)
b.box("z2", U, 13, v2(G12), fl("無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe"), 220)
b.box("z1", E, 13, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash）→ 清單＋指紋＋apply|yes／no 以 stdout 回啟動器"), 400)
b.box("mb", E, 14, LBL, "有待辦 ↓ 續「sync（2）」頁：啟動器 docker → 引擎 apply sync", 400, 24, minh=24)
b.D("ne6", "n1e", "nc", al=True)''',
'''b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync（已寫 launcher_start、engine_start）", 400)
b.box("njx", U, 1, v2(O12), "是 → 1：印 6-33（未完成的 <verb>，請先重跑它）", 220)
b.box("nj", E, 1, v2(D12), "偵測到未完成交易（.tmp.<verb>.*）？", 330, ax="l")   # v2.14-4（與 update 同）
b.box("ncx", U, 2, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev）", 220)
b.box("nc", E, 2, v2(D12), "CI 為真（frozen）且有 local 覆寫？", 330, ax="l")
b.box("nf", P, 2, v2(RULE), fl("frozen（CI 為真；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；需寫 tracked 檔 → 1（-y 不解除）；升為失敗：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫"), 360)
b.box("t0", E, 3, v2(D12), "path 覆寫（dev 中）？", 250, ax="l")
b.box("t0s", E, 3, v2(SUB), fl("是：跳過 materialize／verify，仍查 metadata、baseline ↓"), 130, ax="r")
b.box("t0r", P, 3, v2(RULE), fl("覆寫兩種（v2.1 B）：引擎 vendor_kit = \\"<tag>\\"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 <repo> = \\"path:<dir>\\" → cache/<repo>/ 是 symlink，跳過 materialize／verify"), 360)
b.box("t1", E, 4, v2(D12), "cache 缺或印記 ≠ 鎖定 digest？", 250, ax="l")
b.box("t1y", E, 4, v2(SUB), fl("是：列待辦「materialize 鎖定版」（不 verify 舊 cache）"), 130, ax="r")
b.box("t2q", E, 5, v2(D12), fl("否 → --verify／CI／版本變動那次？"), 250, ax="l")   # §3.6、v2.9 §3
b.box("t2qn", E, 5, v2(SUB), fl("否：不逐檔驗（快）↓"), 130, ax="r")
b.box("t2", E, 6, D12, "是 → 每檔 sha256 ＝ 印記？", 250, ax="l")
b.box("t2n", E, 6, SUB, fl("否：列待辦「重裝 + warn（cache 被改過）」"), 130, ax="r")
b.box("t3a", U, 7, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)
b.box("t3", E, 7, D12, "metadata 有完成標記？", 250, ax="l")
b.box("t3r", P, 7, v2(INV), fl("不變量（v2.1 A、v2.5 §9）：自動化不碰使用者的檔 —— sync 不寫 version.toml、初始檔、baseline、薄殼、gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp"), 360)
b.box("t4", E, 8, D12, "最後合併版本 ＝ version.toml？", 250, ax="l")
b.box("t4r", U, 9, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)
b.box("t4c", E, 9, D12, "否（落後）→ CI 為真（frozen）？", 250, ax="l")
b.box("t5", E, 10, SUB, fl("否：warn「baseline 落後，請 just vendor_kit upgrade <repo>」（繼續）"), 300, ax="l")
b.box("tq", E, 11, v2(D12), "還有工具？", 270, ax="l")
b.box("t6", E, 12, v2(D12), fl("否 → tools.just 缺或不符？"), 270, ax="l")   # 兩行（頁高 ≤ 2400）；t6y 寫全名 gen/tools.just
b.box("t6y", E, 12, v2(SUB), fl("是：列待辦「重生 gen/tools.just」"), 90, ax="r")
b.box("z0", E, 13, v2(SUB), fl("resolve 完：產生待辦清單（要拉的 image、要重裝、要重生 gen/tools.just）→ 空 = apply|no"), 400)
b.box("z2", U, 14, v2(G12), fl("無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe"), 220)
b.box("z2l", L, 14, v2(W12), LXT, 280)
b.box("z1", E, 14, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash）→ 清單＋指紋＋apply|yes／no 以 stdout 回啟動器"), 400)
b.box("mb", E, 15, LBL, "有待辦 ↓ 續「sync（2）」頁：啟動器 docker → 引擎 apply sync", 400, 24, minh=24)
b.D("ne6", "n1e", "nj", al=True); b.H("ne6x", "nj", "njx", "是"); b.D("ne6n", "nj", "nc", "否", al=True)   # 6-33（v2.14-4）''')
rep('''b.D("ze0", "z0", "z1"); b.H("ze1", "z1", "z2", "無待辦"); b.D("ze2", "z1", "mb")''',
'''b.D("ze0", "z0", "z1"); b.H("ze1", "z1", "z2l", "無待辦"); b.H("ze1l", "z2l", "z2"); b.D("ze2", "z1", "mb")   # 頁尾 launcher_exit（v2.14-2）''')
rep('''b = F.band("eA2", "sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 逐工具算待辦 → 無待辦（apply|no）→ 0；有待辦 → 第 2 段見「sync（2）」頁", v2=True)''',
'''b = F.band("eA2", "sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 偵測未完成交易（印 6-33 → 1）→ 逐工具算待辦 → 無待辦（apply|no）→ 0；有待辦 → 第 2 段見「sync（2）」頁", v2=True)''')

# ---- P6c sync(2)：m0p 紅出口；apply 容器 engine_start；頁尾 launcher_exit ----
rep('''b.box("m0b", L, 3, v2(W12), "docker create <img> /x", 280)
b.box("m0c", L, 4, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("m0d", L, 5, v2(W12), "docker rm 該容器", 280)
b.box("m1", L, 6, v2(W12), fl("docker run … -v <tmp>:/dist:ro\\n<引擎> apply sync"), 280)
b.box("m2a", E, 6, v2(SUB), fl("apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）"), 400)
b.box("m2b", E, 7, v2(SUB), "重驗 resolve 的輸入指紋", 240, ax="l")
b.box("m2x", E, 7, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m3", E, 8, v2(SUB), fl("materialize／重裝（每個待辦工具）：/dist/<repo> 展開到暫存目錄"), 400)
b.box("m3c", E, 9, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("m3f", P, 9, F12, "cache/<repo>/（重寫，不進 git）", 360)
b.box("m3b", E, 10, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("m3bf", P, 10, F12, "gen/<repo>.stamp（重寫，不進 git）", 360)
b.box("m3v", E, 11, v2(SUB), fl("版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）"), 400)   # v2.9 §3
b.box("m3vq", E, 12, v2(D12), "全部相符？", 200, ax="l")
b.box("m3vn", E, 12, v2(SUB), fl("否：重裝該工具 + warn（cache 被改過）"), 150, ax="r")
b.box("m7", U, 13, G12, "0：接著跑原本的 recipe", 220)
b.box("m5", E, 13, v2(SUB), fl("重生 gen/tools.just（待辦有它時；每個 <ns>.just 一行 mod?）"), 400)
b.box("m5f", P, 13, F12, "gen/tools.just（不進 git；gen/.stamp 不動）", 360)
b.D("me0", "m00", "m0a", "", 0.5, 0.5); b.RD("me0n", "m0a", "m0p", "無"); b.H("me0g", "m0g", "m0p", "拉 /dist"); b.D("me0y", "m0a", "m0b", "有", al=True); b.D("me0p", "m0p", "m0b", al=True)
b.D("me0c", "m0b", "m0c"); b.D("me0d", "m0c", "m0d")
b.D("me1", "m0d", "m1"); b.H("me2", "m1", "m2a"); b.D("me2b", "m2a", "m2b", al=True); b.H("me2x", "m2b", "m2x"); b.D("me3", "m2b", "m3", al=True)''',
'''b.box("m0px", E, 3, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31"), 240, ax="l")   # v2.14-5
b.box("m0b", L, 3, v2(W12), "docker create <img> /x", 280)
b.box("m0c", L, 4, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("m0d", L, 5, v2(W12), "docker rm 該容器", 280)
b.box("m1", L, 6, v2(W12), fl("docker run … -v <tmp>:/dist:ro\\n<引擎> apply sync"), 280)
b.box("m1e", E, 6, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("m2a", E, 7, v2(SUB), fl("apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）"), 400)
b.box("m2b", E, 8, v2(SUB), "重驗 resolve 的輸入指紋", 240, ax="l")
b.box("m2x", E, 8, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m3", E, 9, v2(SUB), fl("materialize／重裝（每個待辦工具）：/dist/<repo> 展開到暫存目錄"), 400)
b.box("m3c", E, 10, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("m3f", P, 10, F12, "cache/<repo>/（重寫，不進 git）", 360)
b.box("m3b", E, 11, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("m3bf", P, 11, F12, "gen/<repo>.stamp（重寫，不進 git）", 360)
b.box("m3v", E, 12, v2(SUB), fl("版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）"), 400)   # v2.9 §3
b.box("m3vq", E, 13, v2(D12), "全部相符？", 200, ax="l")
b.box("m3vn", E, 13, v2(SUB), fl("否：重裝該工具 + warn（cache 被改過）"), 150, ax="r")
b.box("m7", U, 14, G12, "0：接著跑原本的 recipe", 220)
b.box("m7l", L, 14, v2(W12), LXT, 280)
b.box("m5", E, 14, v2(SUB), fl("重生 gen/tools.just（待辦有它時；每個 <ns>.just 一行 mod?）"), 400)
b.box("m5f", P, 14, F12, "gen/tools.just（不進 git；gen/.stamp 不動）", 360)
b.D("me0", "m00", "m0a", "", 0.5, 0.5); b.RD("me0n", "m0a", "m0p", "無"); b.H("me0g", "m0g", "m0p", "拉 /dist"); b.D("me0y", "m0a", "m0b", "有", al=True); b.D("me0p", "m0p", "m0b", "", 0.25, 0.5); b.D("me0px", "m0p", "m0px", "失敗", 0.75, 0.25, dy=8)
b.D("me0c", "m0b", "m0c"); b.D("me0d", "m0c", "m0d")
b.D("me1", "m0d", "m1"); b.H("me2", "m1", "m1e"); b.D("me2e", "m1e", "m2a"); b.D("me2b", "m2a", "m2b", al=True); b.H("me2x", "m2b", "m2x"); b.D("me3", "m2b", "m3", al=True)''')
rep('''b.H("me12", "m5", "m5f", "寫"); b.H("me15", "m5", "m7")''', '''b.H("me12", "m5", "m5f", "寫"); b.H("me15", "m5", "m7l"); b.H("me15l", "m7l", "m7")   # 頁尾 launcher_exit（v2.14-2）''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 3 ok")
