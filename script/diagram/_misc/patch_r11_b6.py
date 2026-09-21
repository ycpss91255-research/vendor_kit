"""第十一輪 patch 6：頁高 ≤ 2400 的瘦身、check_overflow／overlap／self 修正。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- 名詞表瘦身 ----
rep(''' ("install／uninstall", "專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 四行問後加；建 config.toml）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"),''',
''' ("install／uninstall", "專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋config.toml、根 justfile 加 import 行、根 .dockerignore 四行）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"),''')
rep(''' ("薄殼首行自描述（Q17）", "薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）"),''',
''' ("薄殼首行自描述（Q17）", "薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；install 用它判定第一次／修復可重產／被改過 → 1，不用 gen/.stamp"),''')
rep(''' RA_T, GS_T, VL_T,''', ''' RA_T,''')
rep(''' ("--local <tar>／.digest（Q26、v2.10 §3）", "add --local 只收存在的 .tar（docker save 存的工具 image 檔；值不是存在的 .tar → 1 + 6-24 類提示，橙；不提供 --digest；tag 形只有 bootstrap.sh 有意義）：先 docker load，讀同名 .digest 旁檔 = 正式 index digest 寫進 version.toml（旁檔缺 → 1）；metadata 記 image ID ↔ digest 對照供離線驗證"),''',
''' ("--local <tar>／.digest（Q26、v2.10 §3）", "add --local 只收存在的 .tar（docker save 存的工具 image 檔；不是 → 1 + 6-24，橙；tag 形只有 bootstrap.sh 收，那時才寫 version.local.toml）：先 docker load，讀同名 .digest 旁檔 = 正式 index digest 寫進 version.toml（旁檔缺 → 1）；metadata 記 image ID ↔ digest 對照"),''')
rep(''' ("gen／mod?／recipe", "gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間（just <ns> …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe"),''',
''' ("gen／mod?／recipe", "gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動"),''')
rep(''' ("快路徑（Q22）", "啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或 local 覆寫的 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync"),''',
''' ("快路徑（Q22）", "啟動器只用 grep 比對：gen/.stamp 第一行 == 引擎 ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 frozen。全相符 → 不起容器、0；否則起引擎 resolve sync"),''')
rep(''' ("image tag／digest／image ID／image inspect", "tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1"),''',
''' ("image tag／digest／image ID／image inspect", "tag = 人看的版本名（可重 build）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID，否則 1"),''')
rep(''' ("覆寫兩種（v2.1 B／v2.2 B）", "引擎覆寫 vendor_kit = \\"<tag>\\"＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 <repo> = \\"path:<dir>\\" → cache 是 symlink，仍查 metadata／baseline"),''',
''' ("覆寫兩種（v2.1 B／v2.2 B）", "引擎覆寫 vendor_kit = \\"<tag>\\"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具覆寫 <repo> = \\"path:<dir>\\" → cache 是 symlink，仍查 metadata／baseline"),''')
rep(''' ("B／D／N、逐檔判斷後詢問", "B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/<repo>，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"),''',
''' ("B／D／N、逐檔判斷後詢問", "B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined；細表見「逐檔判斷」頁"),''')
rep(''' ("逐檔判斷後詢問／apply", "apply = 動詞的第二段（拿到 flock、重驗指紋、建日誌後才寫檔）；三份比：N 改了才問「換成新版？」，兩邊都改才問「三方合併？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash，新檔（B 無）被拒才 state=declined；全部在暫存完成再逐檔原子替換；materialize 到 cache 在決定套用之後"),''',
''' ("逐檔判斷後詢問／apply", "apply = 動詞的第二段（拿到 flock、重驗指紋、建日誌後才寫檔）；三份比：N 改了才問「換成新版？」，兩邊都改才問「三方合併？」；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined；全部在暫存完成再逐檔原子替換"),''')
rep(''' ("二進位／symlink", "二進位 = 不是文字的檔（圖片等）；symlink = 指向另一個路徑的捷徑；兩者不做行內合併：你沒改 → 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過保留 + warn；dist/files/ 第一版禁止 symlink"),''',
''' ("二進位／symlink", "二進位 = 不是文字的檔；symlink = 指向另一個路徑的捷徑；兩者不做行內合併：你沒改 → 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過保留 + warn；dist/files/ 第一版禁止 symlink"),''')
rep(''' ("進度日誌（upgrade vendor_kit；v2.11）", "upgrade vendor_kit 也建進度日誌 .tmp.upgrade.<id>.toml（統一規則，無例外）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後由新引擎刪；重跑遇既有日誌 = 續作；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 印 6-33 仍 0"),''',
''' ("進度日誌（upgrade vendor_kit；v2.11）", "upgrade vendor_kit 也建 .tmp.upgrade.<id>.toml（統一規則）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0"),''')
rep(''' ("--protocol P／降版（Q19）／結束碼 3", "薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@<舊版>：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用"),''',
''' ("--protocol P／降版（Q19）／結束碼 3", "薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@<舊版>：目標引擎（image LABEL 的 P／schema）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入）；救援路徑永久可用"),''')
rep(''' ("薄殼首行自描述（Q17）／上次產物／相符", "薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更"),''',
''' ("薄殼首行自描述（Q17）／上次產物／相符", "薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「== 上次產物」= 首行 hash 與內容相符，被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更"),''')

# ---- bootstrap(1) ----
rep('''b.box("a1r", P, 3, v2(RULE), fl("Q18（v2.4 §5）：舊 bootstrap.sh 在已裝過的 repo 再跑 → 用 version.toml 第一行的引擎跑 install（不降版、不用內嵌）；該引擎拉不到 → 1 失敗，不得退回內嵌；只有第一次接入才用內嵌 ref"), 360)''',
'''b.box("a1r", P, 3, v2(RULE), fl("Q18（v2.4 §5）：已裝過的 repo 再跑舊 bootstrap.sh → 用 version.toml 第一行的引擎跑 install（不降版）；拉不到 → 1，不得退回內嵌；只有第一次接入才用內嵌 ref"), 360)''')
rep('''b.box("a8ix", U, 11, v2(R12), fl("失敗 → 1：本機無此 image（tag 形）"), 220)   # v2.14-5''', '''b.box("a8ix", U, 12, v2(R12), fl("失敗 → 1：本機無此 image（tag 形）"), 220)   # v2.14-5''')
rep('''b.H("ae8ix", "a8i", "a8ix", "失敗"); b.D("ae11", "a8i", "a9");''', '''b.DL("ae8ix", "a8i", "a8ix", "失敗", 0.12); b.D("ae11", "a8i", "a9");''')
# ---- install(1) ----
rep('''"config.toml（第一次才建）", "baseline/vendor_kit/config.toml（副本）"], 360, cols=2)''', '''"config.toml（第一次才建）", "config.toml 的 baseline 副本"], 360, cols=2)''')
rep('''b.box("i4n", P, 5, NOTE, fl("第一次 install：失敗 → 依日誌移除已寫的檔 → 1（不留半成品；log/ 保留，v2.13 P4／P5）；修復型：失敗 → 1 列已完成／未完成，下次可寫動詞先恢復；日誌在「install（2）」頁最後一步刪"), 360)''',
'''b.box("i4n", P, 5, NOTE, fl("第一次 install 失敗 → 依日誌移除已寫的檔 → 1（不留半成品；log/ 保留，v2.13 P4／P5）；修復型失敗 → 1 列已完成／未完成，下次可寫動詞先恢復；日誌在「install（2）」頁最後刪"), 360)''')
# ---- install(2) band 一行 ----
rep('''b = F.band("bI2", "5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；有 → 已含跳過／問後 append；v2.12 加 log/）→ 刪日誌 → 0", pad=40, v2=True)''',
'''b = F.band("bI2", "5a″ install 收尾（承「install（1）」頁）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；有 → 已含跳過／問後 append；v2.12 加 log/）→ 刪日誌 → 0", pad=40, v2=True)''')
# ---- add(2) ----
rep('''b.box("cr", P, 6, v2(RULE), fl("復原（v2.2 C、v2.5 §3）：進度日誌在第一個寫入前建立、最後一步刪除；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復（唯讀動詞只提示重跑）"), 360)''',
'''b.box("cr", P, 6, v2(RULE), fl("復原（v2.2 C、v2.5 §3）：進度日誌第一個寫入前建、最後一步刪；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復"), 360)''')
rep('''b.box("c20l", E, 12, v2(D12), "還有下一個 [[file]]？", 300, ax=50)''', '''b.box("c20l", E, 12, v2(D12), "還有下一個 [[file]]？", 320, ax=40)''')
# ---- sync(1′) ----
rep('''b.box("njx", U, 1, v2(O12), "是 → 1：印 6-33（未完成的 <verb>，請先重跑它）", 220)
b.box("nj", E, 1, v2(D12), "偵測到未完成交易（.tmp.<verb>.*）？", 330, ax="l")   # v2.14-4（與 update 同）
b.box("ncx", U, 2, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev）", 220)
b.box("nc", E, 2, v2(D12), "CI 為真（frozen）且有 local 覆寫？", 330, ax="l")
b.box("nf", P, 2, v2(RULE), fl("frozen（CI 為真；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；需寫 tracked 檔 → 1（-y 不解除）；升為失敗：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫"), 360)
b.box("t0", E, 3, v2(D12), "path 覆寫（dev 中）？", 250, ax="l")
b.box("t0s", E, 3, v2(SUB), fl("是：跳過 materialize／verify，仍查 metadata、baseline ↓"), 130, ax="r")''',
'''b.box("njx", U, 1, v2(O12), "是 → 1：印 6-33（請先重跑該動詞）", 220)
b.box("nj", E, 1, v2(D12), "偵測到未完成交易？（.tmp.<verb>.*）", 330, ax="l")   # v2.14-4（與 update 同）
b.box("ncx", U, 2, v2(O12), "是 → 1：CI 拒絕 local 覆寫（請先 undev）", 220)
b.box("nc", E, 2, v2(D12), "frozen 且有 local 覆寫？", 330, ax="l")
b.box("nf", P, 2, v2(RULE), fl("frozen（CI 為真；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；需寫 tracked 檔 → 1（-y 不解除）；升為失敗：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫"), 360)
b.box("t0", E, 3, v2(D12), "path 覆寫（dev 中）？", 250, ax="l")
b.box("t0s", E, 3, v2(SUB), fl("是：跳過 materialize／verify ↓"), 130, ax="r")''')
rep('''b.box("t2q", E, 5, v2(D12), fl("否 → --verify／CI／版本變動那次？"), 250, ax="l")   # §3.6、v2.9 §3''', '''b.box("t2q", E, 5, v2(D12), fl("否 → --verify／CI／版本變動？"), 250, ax="l")   # §3.6、v2.9 §3''')
rep('''b.box("z2", U, 14, v2(G12), fl("無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe"), 220)
b.box("z2l", L, 14, v2(W12), LXT, 280)''',
'''b.box("z2", U, 14, v2(G12), fl("無待辦 → 0：不起第二個容器，接著跑 recipe"), 220)
b.box("z2l", L, 14, v2(W12), LXT, 240, ax="l")''')
# ---- B(2) ----
rep('''b = F.band("uB2", "B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔：判定情況 → 問 6-22 → 同意？→ 在暫存套用／不動 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換（§4.3）；收尾見「B（2′）」頁", v2=True)''',
'''b = F.band("uB2", "B（2）apply 寫入段前半（承「B（1′）」頁）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔：判定情況 → 問 6-22 → 同意？→ 在暫存套用／不動 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換；收尾見「B（2′）」頁", v2=True)''')
rep('''b.box("b14q1b", E, 8, v2(D12), fl("二進位／symlink、你沒改、新版改了？→ 問「是二進位檔，換新版？」"), 360, ax=0)''', '''b.box("b14q1b", E, 8, v2(D12), fl("二進位／symlink、你沒改、新版改了？→ 問「換新版？」"), 360, ax=0)''')
rep('''b.box("b14r", P, 11, v2(RULE), fl("Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑時訊息醒目"), 280)''',
'''b.box("b14r", P, 11, v2(RULE), fl("Q14／Q15、v2.7 §3：拒絕 → 已納管檔 state 不變、只記 declined_hash（新版再變才再問）；新檔（B 無）被拒 → state=declined、之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」"), 280)''')
rep('''b.box("b14pc", E, 15, v2(SUB), fl("是：留原檔、記 conflicts（baseline 不推）"), 90, ax="l")''', '''b.box("b14pc", E, 15, v2(SUB), fl("是：留原檔、記 conflicts"), 90, ax="l")''')
# ---- 7b 回退 ----
rep('''b.box("d1b", L, 1, D12, "docker image inspect：舊版本機有？", 170, ax="l")''', '''b.box("d1b", L, 1, D12, "inspect：舊版本機有？", 200, ax="l")''')
# ---- E(a) ----
rep('''b.box("s2n", U, 3, v2(G12), "否 → 只升工具（每個工具走「B（1）」頁；Q27 彙總）", 220)''', '''b.box("s2n", U, 3, v2(G12), "否 → 只升工具（每個工具走「B（1）」頁；Q27）", 220)''')
rep('''b.DL("se3", "s2q", "s2r0", "是"); b.H("se3b0", "s2r0", "s2b0");''', '''b.D("se3", "s2q", "s2r0", "是", 0.5, 0.5); b.H("se3b0", "s2r0", "s2b0");''')
rep('''b.box("s2ln", L, 11, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)''', '''b.box("s2ln", L, 11, v2(D12), "是 → inspect：本機有？", 260, ax=0)''')
rep('''b.box("s2lv", L, 13, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=50)
b.box("s2lx", E, 13, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產；日誌保留）"), 240, ax="l")
b.box("s4", U, 14, v2(G12), fl("→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內接手）"), 220)   # 綠終點不含 1／2／3（lint endcolor）''',
'''b.box("s2lv", L, 13, v2(D12), fl("覆寫中且 .Id ≠ 記的 ID？"), 260, ax=0)
b.box("s2lx", E, 13, v2(R12), fl("拉不到／ID 不符 → 1 + 6-2b（引擎已鎖定，薄殼尚未重產）"), 240, ax="l")
b.box("s4", U, 14, v2(G12), fl("→ 接「E(c)」頁「docker run 該引擎」格（同一次指令內）"), 220)   # 綠終點不含 1／2／3（lint endcolor）''')
rep('''b.box("s8", U, 16, v2(O12), fl("否 → 1：印 6-1「vendor_kit 已更新 vX → vY，請執行 upgrade vendor_kit」→ 打 (c)"), 220)''', '''b.box("s8", U, 16, v2(O12), fl("否 → 1：印 6-1「已更新 vX → vY，請 upgrade vendor_kit」→ 打 (c)"), 220)''')
# ---- E(c)(1) ----
rep('''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → grep 第一行 → inspect／pull → engine_start → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則「E(c)（2）」頁", v2=True)''',
'''b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → inspect／pull → engine_start → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則「E(c)（2）」頁", v2=True)''')
rep('''b.box("s12s", E, 8, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 340, ax="l")
b.box("s12sn", P, 8, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)
b.box("s12dx", U, 9, v2(O12), fl("是 → 3：印 6-10（無法無損讀現有檔；零寫入）"), 220)
b.box("s12d", E, 9, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀？（P／schema）"), 340, ax="l")''',
'''b.box("s12s", E, 8, v2(D12), "薄殼 == 上次產物？（首行 hash）", 340, ax="l")
b.box("s12sn", P, 8, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17；install 頁同）；拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)
b.box("s12dx", U, 9, v2(O12), fl("是 → 3：印 6-10（無法無損讀現有檔；零寫入）"), 220)
b.box("s12d", E, 9, v2(D12), fl("是 → @<tag> 舊版且無法無損讀？"), 340, ax="l")''')
# ---- E(c)(2) band 一行 ----
rep('''b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼五檔 → config.toml 缺則建／三方合併（v2.14-7）→ gen/.stamp → tools.just → 刪 .tmp.upgrade 日誌（v2.11）→ 1", v2=True)''',
'''b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：第一行未變）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼五檔 → config.toml 缺則建／三方合併（v2.14-7）→ gen/.stamp → tools.just → 刪 .tmp.upgrade 日誌（v2.11）→ 1", v2=True)''')
# ---- uninstall(2) ----
rep('''b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（config.toml == baseline 副本才刪，v2.13 P6；gen/、baseline/ 根檔各一步）→ justfile 那行、.dockerignore 四行問後逐行刪 → 刪日誌 → .vendor_kit/ 保留（只剩 log/）", v2=True)''',
'''b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（config.toml == baseline 副本才刪，v2.13 P6）→ justfile 那行、.dockerignore 四行問後逐行刪 → 刪日誌 → .vendor_kit/ 保留（只剩 log/）", v2=True)''')
rep('''"baseline/vendor_kit/config.toml（副本）"], 360, cw=(140, 198))''', '''"config.toml 的 baseline 副本"], 360, cw=(140, 198))''')
rep('''b.box("x6", E, 10, D12, "根 justfile 有我們那一行？", 260, ax="r")''', '''b.box("x6", E, 10, D12, "根 justfile 有我們那一行？", 340, ax="r")''')
rep('''b.box("x8", E, 11, SUB, fl("無／否：印指示（請自行移除 import 那行）"), 100, ax=0)
b.box("x7", E, 11, v2(D12), "有 → 問「要刪這一行嗎」？", 260, ax="r")''',
'''b.box("x8", U, 11, SUB, fl("無／否：印指示（請自行移除 import 那行）"), 220)   # 移到左欄，讓菱形加寬成一行（頁高）
b.box("x7", E, 11, v2(D12), "有 → 問「要刪這一行嗎」？", 340, ax="r")''')
rep('''b.box("x9a", E, 13, v2(D12), "根 .dockerignore 存在？", 260, ax=120)
b.box("x9b", E, 14, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 260, ax=120)''',
'''b.box("x9a", E, 13, v2(D12), "根 .dockerignore 存在？", 340, ax="r")
b.box("x9b", E, 14, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 340, ax="r")''')
rep('''b.box("x9q", E, 15, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 260, ax=120)''', '''b.box("x9q", E, 15, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 340, ax="r")''')
rep('''b.box("x5y", U, 19, v2(G12), fl("0：印摘要（.vendor_kit/log/ 留存、可手動刪；保護清單內的檔保留）"), 220)''', '''b.box("x5y", U, 19, v2(G12), fl("0：印摘要（log/ 留存可手動刪；保護清單內的檔保留）"), 220)''')
rep('''b.D("xe12", "x5dd", "x6", "", 0.5, 0.5); b.LD("xe13", "x6", "x8", "無", busx=630, vert="left"); b.D("xe14", "x6", "x7", "有", al=True)''',
    '''b.D("xe12", "x5dd", "x6", "", 0.5, 0.5); b.LD("xe13", "x6", "x8", "無", busx=150, vert="left"); b.D("xe14", "x6", "x7", "有", al=True)''')
rep('''b.LD("xe16an", "x9a", "x9z", "無", busx=635, vert="left"); b.LD("xe16bn", "x9b", "x9z", "無", busx=635, vert="left"); b.D("xe16qn", "x9q", "x9z", "否", 0.5, 0.5)''',
    '''b.LD("xe16an", "x9a", "x9z", "無", busx=615, vert="left"); b.LD("xe16bn", "x9b", "x9z", "無", busx=615, vert="left"); b.D("xe16qn", "x9q", "x9z", "否", 0.5, 0.5)''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 6 ok")
