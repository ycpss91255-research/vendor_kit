# 第十四輪 Claude 三階段 must_fix 67，optional 89

## 11 契約 v2：下游 repo 契約③ (v1p3): must_fix 1 / optional 0
- [lint] p3_th: term-count：本頁名詞表 16 條 > 8，未落實 v2.16-18（每頁 ≤ 8、只留第 0 頁沒有的詞）；Dockerfile.dist／label／dest／SemVer／命名空間／多架構 index 等第 0 頁或契約③本文已有

## 12 契約 v2：啟動器 ↔ 引擎契約④ (v1p3b): must_fix 3 / optional 3
- [內容一致性] p3_fast: sync 快路徑條件缺「每個 cache/<repo>/ 存在（印記在而 cache 被刪 → 不走快路徑）」，未落實 v2.16-11／spec §3.6 codex r2 #55
- [排版] u5d_e: update 單段的「1／2」線從 u5b 底部繞到橢圓下方 y≈944（貼著 apply 通則框 p3_lock 上緣 y=950），再從下往上穿過 u5d 橢圓本體進 top 端點；線與標籤「1／2」壓在橘框邊上，縮圖幾乎看不到這條線
- [內容一致性] s4x1: apply 結束碼分流「1／2／3：需人處理」與「1：失敗」都含 1，同一結束碼指向兩個終點；依 spec 應為 1 = 失敗、2／3 = 需人處理
  (opt) [內容一致性] d2_in: resolve 結果只有兩叉（resolve 0 → apply|yes？、非 0 → p3_rx）；「回 0 但 vk-resolve/1 文法不合 → 1 + 6-30」只寫在規則框 p3_vkr，流程上沒有出口，與 v2.16-2 三叉不一致
  (opt) [內容一致性] p3b_pend: 便條寫「本頁決議狀態（v2.15 結案）…（v2.15-2）」屬沿革便條，v2.16-18 要求沿革便條全刪
  (opt) [內容一致性] s2c: resolve 出口只有「resolve 0」與「非 0」兩叉；v2.16 的第三叉「stdout 文法不合 → 1 印 6-30」只寫在規則框 p3_vkr 文字，流程圖上沒有分支

## 16 架構圖 v2 (v1p4): must_fix 1 / optional 1
- [排版] run_cli / ret_cli: 啟動器→引擎容器的「動詞、參數、介面版旗標」與「結束碼、vk-resolve」兩個標籤正好蓋在 x=552／576 兩條垂直線上（三條線相距 22–24px，標籤寬度超過），字與線互壓
  (opt) [內容一致性] d_shell_prune: 線「版本鎖定行 → keep」由 shell 模組傳給 prune；keep 清單依 spec §1.2 由 resolve prune 依版本鎖定行／本機覆寫算出，shell 模組不讀版本鎖定行（讀寫在 schema 模組 m_schema_u1_1），資料來源模組錯

## 20 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add (v1p5ccc): must_fix 1 / optional 3
- [顏色] a12: 所有中止線（含 fb_a10d 啟動器 docker 段 pull 失敗 6-24／6-31、fb_a10rq1 文法不合 6-30、fb_a8b 寫 version.local.toml 失敗）全部匯到同一個橙終點；6-24／6-30 屬失敗，v2.16-19 明定「6-24 一律紅」，需人處理與失敗兩種結束應分色（同組 bootstrap（1′）頁 a9hx／a9x 有分）
  (opt) [lint] a10d: onething：「啟動器 docker 段：inspect → pull → extract /dist 到暫存」一格三個動作；雖註明見「add（1′）」頁，仍是三件事在一格
  (opt) [可讀性] a10d: 「是：啟動器 docker 段：inspect → pull → extract /dist 到暫存」一格三個動作（a10ae「apply add（拿鎖、重驗、建進度檔後寫入）」同樣）；雖是引到 add 頁的摘要格，仍違反一格一事，若要保留建議只寫「照 add (1′) 頁做 docker 段」不列步驟
  (opt) [lint] a10d: onething：「啟動器 docker 段：inspect → pull → extract /dist 到暫存」一格三個動作。若本頁只想當子流程摘要，改寫成單一件事「啟動器 docker 段（見「add（1′）」頁）」；否則拆成 inspect／pull／extract 三格（與 add（1′）頁 c9a／c9b 對齊）。

## 21 流程 v2：install（1）主機檢查 → 引擎 image → docker run (v1p5c): must_fix 3 / optional 3
- [內容一致性] ipr: 順序錯／誰做：「偵測既有進度檔 → 先恢復」（藍＝引擎做）畫在 docker run 引擎 install（i1）與 flock（i4a）之前，此時引擎容器尚未啟動、也未拿鎖；spec 恢復由引擎 progress 模組做（journal_detected／recovered 為 engine 事件），v2.16-1 共通前置格應在 docker run 之後、寫入之前
- [內容一致性] i1g: 「grep version.toml … 命中須恰 1」只有一條出線；spec（命中數必須恰 1，0 或重複 → 1）與 sync 頁（v1p6 n1 有「≠ 1」紅框）都有失敗分支，此頁缺
- [排版] ie4ax: 「逾時」標籤擠在 flock 框（右邊 980）與 1+6-26 橢圓（左邊 1010）之間 30px 的短箭頭上，壓到箭頭
  (opt) [內容一致性] i1g: 缺分支：格內寫「命中須恰 1」但沒有「命中 ≠ 1 → 1 列差異不動」的出口（契約④ s1x 有）
  (opt) [內容一致性] i1: 缺分支：spec §1.2「install <repo> 誤用 → 1 + 6-17」在 install 四頁都沒有出口
  (opt) [排版] ipe_r: 「是：先恢復」回到 grep 框的線在 (532,786) 進框，箭頭緊貼框右上角 v2 小標

## 24 流程 v2：install（2）根 justfile 與 .dockerignore (v1p5cc): must_fix 2 / optional 1
- [排版] ie13: 「無：建 justfile」的後續線從方框「頂邊」出去（exit 0.5,0），與從「有根 justfile？」進來的線重疊同一段，再往右到 x=1610 匯流；縮圖看起來像在框上方分岔、沒經過方框，該改從框底或右側出線
- [排版] ie20z: 同 ie13：「無：建 .dockerignore」的後續線也從頂邊出去，與進來的「無」線重疊，讀不出方框有被執行
  (opt) [lint] p5cc_tk4: term-dup-page0：名詞「symlink（根檔）」第 0 頁已有 symlink，v2.16-18 只留第 0 頁沒有的詞；根檔不寫的規則已在 i6sp／igsp 格內

## 25 流程 v2：add（1）resolve → docker (v1p5b): must_fix 2 / optional 1
- [排版] ce2ll: 「是」標籤擠在「--local（離線）？」菱形左尖與「是：目標 = 交來的 index digest」框（右邊 700）之間 20px 的短線上，貼到框邊
- [排版] ce3: 「查」標籤擠在「否：查 tag…」框與紫色 image 框之間約 10px 的短線上，蓋住箭頭
  (opt) [內容一致性] cpr: 「先恢復」格是藍色（引擎做）卻放在 docker run resolve 之前，沒有任何容器可執行它；啟動器不解析 TOML 也做不了恢復，spec §4.10 恢復事件（journal_recovered）屬 engine——誰做、在哪個容器內不明。同型格 v1p7c bpr、v1p7bc spr 亦同。

## 27 流程 v2：add（2）apply 寫入段 (v1p5bc): must_fix 0 / optional 1
  (opt) [內容一致性] c23x: 共通失敗匯流終點寫「版本鎖定行不動」，但 fb_c23b（刪進度檔失敗）進入此匯流時 c23 已寫完 version.toml [tools] 行，文字與該路徑事實矛盾（spec add 回 1 時 version.toml 一律未動，此路徑無法成立）。

## 28 流程 v2：sync（1）啟動器快路徑 (v1p6): must_fix 2 / optional 0
- [內容一致性] n1i: 缺分支／順序：本機覆寫判斷放在 inspect「有」之後，「無」一律走 n1p docker pull；但 spec §3.1 引擎 image 取得明寫 local 覆寫時「不 pull」、tag 形本機無此 image 為失敗出口（v2.16-12 對 E(a) 也要求覆寫判斷在 pull 前）。覆寫中且本機無 image 時此頁會去 pull。
- [排版] ne5x: 「失敗」標籤正好落在線的轉角（530,1398）上壓線；且 n1p 底邊同時出兩條線（x=500 往出口、x=530 往失敗）與左邊「有」線同高 y=1398，縮圖看起來像三條線交會

## 29 流程 v2：sync（1′）引擎 resolve (v1p6cc): must_fix 2 / optional 0
- [內容一致性] z0q: 順序錯：啟動器「apply|no？」判斷（→ z2 直接 0）放在 resolve 結束碼／vk-resolve/1 文法三叉之前，三叉卻在下一頁 v1p6c（m00 入口只接 apply|yes）。spec §3.3：no 是「啟動器驗完文法後」才 exit 0；resolve 非 0 或文法不合時不該讀到 apply|no。
- [排版] te7: 「是 → 每檔 sha256 = 印記？」到「metadata 存在且可解析？」的「是」標籤（760,811）正好壓在 y=809 的右側匯流橫線上

## 30 流程 v2：sync（2）三叉 → docker → apply 前置 (v1p6c): must_fix 0 / optional 5
  (opt) [內容一致性] m0a: 缺分支：docker 段只有 extract 迴圈，沒有 mount 記錄的處理（dev 覆寫工具：驗 <dir>/dist/init.toml 存在、-v <dir>/dist:/dist/<repo>:ro）；spec §3.3 mount 表與範例 2 明寫 sync 會帶 mount。
  (opt) [排版] me0y: inspect「有」的折線最後一段（y=719→x=420）直接接在 pull→extract 既有箭頭上，沒有自己的箭頭，是線接線；v1p7ccc、v1p7bd 同型
  (opt) [內容一致性] m2b: 「重驗 resolve 的輸入指紋」在本頁是藍色步驟框帶「不同」出口，在 v1p7ccc／v1p7bd 同一步是黃色菱形「相同？」；同一判斷兩種畫法
  (opt) [排版] m0b: 「extract：docker create → cp → rm」一格三步（名詞表已定義為合稱，若已接受可忽略）
  (opt) [lint] m0b: onething：同 add（1′）頁 c9b，「extract：docker create → cp → rm」一格三個指令；拆成 create／cp／rm 三格，或縮成單一件事「extract /dist 到暫存（見契約④）」。

## 31 流程 v2：sync（2′）apply 寫入段 (v1p6cw): must_fix 1 / optional 2
- [排版] me4vn: 「逐檔驗？」的「否」標籤被放到線的末端，貼在「還有待辦工具？」菱形左上、與「是：下一個工具」並排，讀起來像該菱形多了一個「否」出口；應移到 逐檔驗 菱形左側出口旁
  (opt) [內容一致性] m3: 缺分支：m7x 寫「取件／寫入失敗（任一步，共通匯流）」，但 m3（取件到暫存）與 m3vn（重裝一次）沒有失敗線進匯流，只有 m3c／m3b／m5 有。
  (opt) [排版] m3vn: 「否：重裝該工具一次 + warn（cache 被改過）」一格兩事（重裝＋印 warn），可拆或把 warn 移到便條

## 32 流程 v2：upgrade ── A. Renovate 路徑 (v1p7): must_fix 1 / optional 1
- [內容一致性] a4b0: 缺分支：check.sh ⓪「納管 → 1 停」（spec §7.1 結束碼 1）只寫在格內文字，沒有失敗線與 PR 紅終點；①（a5）與 ②～⑤（a4fx）都有終點，只有 ⓪ 沒有。
  (opt) [內容一致性] a4b0: check.sh ⓪ 的失敗只寫在格內「納管 → 1 停」，沒有畫出分支；②～⑤ 有匯到橙圓、⓪ 沒有

## 33 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker (v1p7c): must_fix 1 / optional 4
- [排版] be9: 目標版=B 直達產生指紋的長折線（x=1310）貼著綠色終點「0：目標 == 現鎖定版…」右緣往下走（僅 10px），縮圖下像把綠圓框住；建議外移或改走更右側
  (opt) [內容一致性] b7zz: 順序：「目標 == 現鎖定版 → 0（apply|no）」從引擎判斷 b7e 直接接綠終點，跳過 stdout vk-resolve/1（b7s2）與啟動器三叉（resolve 回 0？文法？）；spec §3.3 apply|no 仍走 stdout、由啟動器驗完文法才 exit 0，且 exit 是啟動器做的。
  (opt) [內容一致性] b7q: 缺分支：格內寫「網路／回應／解析失敗 → 1 失敗」但只有「是 → 6-3 橙」與「否 → 繼續」兩條線，查 registry 失敗沒有紅色終點。
  (opt) [排版] be10n: 「查 registry 需憑證但沒有？」的「否」標籤正好落在三條目標版折線匯入點（890,1616）旁，看起來像匯流線的標籤
  (opt) [內容一致性] b7q: 菱形同時判兩種失敗：無憑證→橙 6-3 有畫分支，但「網路／回應／解析失敗 → 1」只寫在菱形字裡沒有分支；缺分支

## 36 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 (v1p7cccc): must_fix 1 / optional 1
- [內容一致性] p7cq_tv4: 與 spec 矛盾：名詞表寫 6-14「結束 2，需人處理」，spec §6 6-14 類別為「—（提醒，不改結束碼）」；b18r 便條「衝突與有新版兩者皆回 2」同樣把 6-14 當成回 2。
  (opt) [排版] -: 本頁未發現人眼可見的排版問題（失敗匯流線與右側檔案框間距 10px 與其他頁一致，可辨）

## 38 流程 v2：upgrade ── D. 回退 (v1p7bd): must_fix 0 / optional 5
  (opt) [內容一致性] d2c2: 缺分支：apply 寫入段（d2c2 cache 原子替換、d2c3 印記、d2c4 tools.just）沒有任何寫入失敗線與紅終點；同段在 sync（2′）頁有共通匯流 m7x，此頁只畫了驗證不符出口 d2vz。
  (opt) [內容一致性] p7bd_tv0: 名詞「回退／git revert」說明末尾「見「D. 回退」頁」指向本頁自己（從別頁複製來的引用）。
  (opt) [lint] hdr1: termcov：泳道表頭「Renovate（GitHub 上）」在本頁與第 0 頁都沒有名詞條（本頁流程未用到此泳道）。
  (opt) [內容一致性] 暫存 → cache/<repo>/（原子替換）: 本頁的暫存→cache、寫印記、重生 tools.just 三個寫入步驟沒有「失敗」匯流到紅終點，而同樣步驟在 v1p6cw／v1p7cccc 都有；缺分支
  (opt) [lint] d1c: onething：同 c9b，「extract：docker create → cp → rm」一格三個指令；拆成 create／cp／rm 三格，或縮成單一件事「extract /dist 到暫存（見契約④）」。

## 39 流程 v2：upgrade ── E. 升引擎 (a)(b) (v1p7bc): must_fix 2 / optional 1
- [排版] se3: 「是」標籤壓在「是：stdout vk-resolve/1…」方框左上角，與框內開頭的「是：」疊成一團
- [排版] se6lo: 「否」標籤放在「是 → 本機覆寫中（vendor_kit=）？」菱形內部下緣，壓到菱形第二行文字，且離它實際的右側出口線很遠，人眼會以為是底部出口
  (opt) [內容一致性] s2ln: 本機覆寫路徑（s2lo 是 → s2lv 否）進入 s2ln 後仍有「無 → s2lp docker pull 新引擎」出口；spec §3.1／§3.4 local 覆寫時不 pull、用該本機 image 驗 ID。覆寫時 s2ln 應只有「有」一條路，否則與「不 pull」矛盾。

## 34 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 (v1p7ccc): must_fix 0 / optional 3
  (opt) [lint] hdr1: termcov：泳道表頭「Renovate（GitHub 上）」在本頁與第 0 頁都沒有名詞條（本頁流程也未用到此泳道）。
  (opt) [排版] -: 本頁除與 v1p6c 相同的「有」線接線外未發現其他排版問題
  (opt) [lint] b8b: onething：同 c9b，「extract：docker create → cp → rm」一格三個指令；拆成 create／cp／rm 三格，或縮成單一件事「extract /dist 到暫存（見契約④）」。

## 35 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 (v1p7cc): must_fix 1 / optional 1
- [排版] be20qn: 「否」標籤落在「取件目標版：/dist/<repo> 複製到暫存目錄」藍框內部左上角，標籤壓框
  (opt) [lint] hdr1: termcov：泳道表頭「Renovate（GitHub 上）」在本頁與第 0 頁都沒有名詞條（本頁流程也未用到此泳道）。

## 43 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） (v1p7bccc): must_fix 2 / optional 2
- [內容一致性] s12z0: 入口寫「已拿鎖，薄殼 == 上次產物」，但從「E(c)（1′）」頁接手的目標引擎是新起的容器（v1p7bcx s12hr），前一容器（現引擎）已結束、flock 已釋放，目標引擎在改第一行前沒有再 flock 也沒有再驗薄殼；spec §3.1「apply 一開始 flock」、§3.2 順序在此路徑缺一步（E(a′) 路徑經 E(c)(1) s12a 有重新 flock，(1′) 路徑沒有）
- [排版] se15ns: 「否：建進度檔」→「重產薄殼五檔」的直線（x≈910）穿過「否：改 version.toml」框的「寫」線（se15wf）與「失敗」線（fb_s12jw），兩處交叉；改進度檔框下接線改走右側或把重產框上移到改行框正下方
  (opt) [內容一致性] s12z: 從 E(c)(1) 恢復路徑進來（進度檔仍在、第一行已改、薄殼上次已重產但刪進度檔失敗）時走「薄殼相符 → 0 無變更」不刪既有進度檔，進度檔永遠留著：之後 sync／update 一律 6-33、可寫動詞每次恢復又回到 0；缺「刪殘留進度檔」分支
  (opt) [排版] 是 → 第一行已是本引擎 ref？ 的「是」線: 「是」線從菱形左頂點下行到重產框，垂直段距「否：改 version.toml」框左緣只約 10px，貼框

## 44 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml (v1p7bcce): must_fix 2 / optional 1
- [內容一致性] s13gaq: 一格兩個判斷（「結果 ≠ 現況」與「同意？」），且「結果 == 現況」沒有出路：依 §4.3 狀態機 D==N／B==N 時不問、不動、也不記 declined_hash，但此格只有 是／否 兩條，== 現況 會落到「否：不動（記 declined_hash）」而誤記拒絕
- [排版] se17n: 「config.toml 存在？」的「否」線繞到頁面最左（x≈8），沿 A、B 兩個情境分組框的外框邊緣貼著走 900px，縮圖上像分組框多了一道邊；改走分組框內側並留白，或把「否」直接接到 B 段入口
  (opt) [內容一致性] se17adn: 拒絕合併時直接跳到 s13gm 寫 metadata、略過 s13gb 推基準版；spec §4.3「不論結果基準版推到 N（解析失敗除外）」、拒絕只記 declined_hash，兩者不一致（若為 config.toml 特例，notes 未見）

## 40 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 (v1p7bca): must_fix 0 / optional 3
  (opt) [內容一致性] s2dx: 共通匯流文字寫「進度檔保留」，但 fb_s2d 是「建進度檔失敗」（沒有進度檔可保留）；與 v1p7bcx s12jx「建進度檔失敗（第一行未改；印原因）」寫法不一致
  (opt) [可讀性] s2h3x: 橙橢圓「1 + 6-2b：…just vendor_kit upgrade vendor_kit（進度檔保留）」五行字塞滿橢圓，上下貼邊；加大橢圓或縮短文字
  (opt) [lint] s2h: onething：「apply 後再 grep …，與 apply 前比較」= grep + 比較兩件事，而比較其實就是下一格判斷 s2h2「第一行變了？」。建議本格只留「apply 後再 grep 正式 version.toml 的 vendor_kit 版本鎖定行（不看本機覆寫、不從 stdout 讀）」，「與 apply 前比較」併進 s2h2 判斷框。

## 52 流程 v2：remove（2）寫入段 (v1p8bccc): must_fix 2 / optional 1
- [內容一致性] m10m: 一格兩件事：「刪 metadata .vendor_kit.toml 並移除已空的 baseline/<repo>/」（刪檔＋刪目錄，「並」）；依規則 7 要拆兩格
- [排版] me15qn: 「否」標籤（有拒絕刪的 append 行？→ 刪 metadata 格）落在 m10m 格左上角、頂邊上（線的轉角 (640,1088) 距格頂只 10px），縮圖看成標籤在格內；標籤應放在 x=565 垂直段旁
  (opt) [內容一致性] m10x: 匯流文字「版本鎖定行不動」對 fb_m10e／fb_m10g 不成立：fb_m10g（刪進度檔失敗）發生時 m10e 已刪掉版本鎖定行；spec §2「回 1 時鎖定行不動」只保證在刪鎖定行之前失敗的情況

## 50 流程 v2：undev vendor_kit (v1p8cc): must_fix 3 / optional 0
- [內容一致性] w2s: 一格兩件事：「算計畫（撤 vendor_kit 行）＋ 指紋」；同組 undev <repo>（v1p8c）已拆成 u4b 算計畫、u4c 產生指紋，此頁應同拆
- [排版] we2ax: 「逾時」標籤（apply flock 格 → 1 + 6-26 橢圓）兩端只隔 30px，兩字標籤壓在藍格右邊框與橢圓左緣上；加大間距或把標籤移到線段上方
- [排版] we2g: 「是：留著」標籤落在「刪進度檔（最後一步）」格（w2g）左上角，卡在 w2ed 底邊與 w2g 頂邊之間 20px 縫裡，縮圖看起來像貼在格上；標籤應移到 x=565 垂直段旁

## 49 流程 v2：undev <repo>（2）寫入段 (v1p8cx): must_fix 1 / optional 2
- [排版] ue11: 「還有其他覆寫行？」的「是：留著」線標籤壓在「拆掉 cache/<repo>/ 的 symlink」框左上角裡面，箭頭也落在框的左上角；標籤要移到折線垂直段旁，箭頭進框頂中央或左側中段
  (opt) [內容一致性] u6e: 缺分支：「取件鎖定版：/dist/<repo> 展開到暫存目錄」沒有失敗邊到共通匯流 u6x（其餘寫入步 u6l／u6c／u6ced／u6d／u6e2／u6f／u6g 都有）
  (opt) [內容一致性] u6e: 「取件鎖定版：/dist/<repo> 展開到暫存目錄」是本頁唯一沒有「失敗」線的寫入步驟；名詞表 6-24／6-31 說 docker create／cp／rm 或暫存目錄失敗同樣 → 1，應接共通匯流

## 46 流程 v2：dev <repo> (v1p8): must_fix 1 / optional 2
- [排版] de8ax: flock 框→「1 + 6-26」的「逾時」標籤擠在 v2 綠標與紅橢圓之間，字貼到橢圓邊與綠標；紅橢圓右移或標籤放線上方
  (opt) [內容一致性] dpr: 「先恢復」畫成藍色（引擎做）卻在 docker run 引擎（d1）之前、也在 flock（d6a）之前；spec §3.2 沒有獨立的恢復子命令、resolve 不寫檔、寫入須在 apply 拿鎖後，圖上看不出誰起容器做恢復、恢復寫檔為何不在鎖內。同型：v1p8ccc vpr、v1p8c upr、v1p8cc wpr、v1p8b mpr、v1p8bc xpr
  (opt) [排版] dpe_r: 「先恢復」框回接線落在「偵測到既有進度檔」菱形與「init.toml 存在？」之間約 26px 的縫裡，「否」標籤壓在回接橫線上

## 51 流程 v2：remove（1）resolve → apply 前置 (v1p8b): must_fix 1 / optional 1
- [排版] me8ax: 「逾時」標籤（apply flock 格 → 1 + 6-26 橢圓）間距僅 30px，標籤壓在藍格右邊框上（與 v1p8cc、v1p8bc 同一問題）
  (opt) [內容一致性] m3: 「0：未接入（提示）」直接從引擎判斷 m2 終止，啟動器三叉（m8q0／m8q1）沒有 apply|no → 0 的出路；spec §3.3 未接入時 resolve 回 0 + apply|no、由啟動器驗完文法後 exit 0，圖上此 0 終點在啟動器側不可達。同型：v1p8c u3、v1p8cc w3

## 53 流程 v2：uninstall（1）resolve → apply 前置 (v1p8bc): must_fix 2 / optional 1
- [排版] xe5ax: 「逾時」標籤（apply flock 格 → 1 + 6-26 橢圓）間距僅 30px，標籤壓在藍格右邊框上
- [排版] xe_r: 虛線「約束」標籤放在 x=1230 垂直段上，距橙框（x2r，x=1240）只 10px，兩字標籤壓在橙框左邊框上；標籤應移到 y=981 水平段中段
  (opt) [lint] x4bx: termcov：本頁用到 6-12（x4bx）但名詞表沒有 6-12 條（同組 v1p8b／v1p8c／v1p8cc 都有列；本頁名詞只 5 條、有空位）

## 69 流程 v2：離線包（3″）resolve sync 驗證 (v1p16ccb): must_fix 3 / optional 1
- [內容一致性] w4t: spec §1.2 sync：「resolve sync 一開始偵測未完成交易 → 印 6-33 結束 1」（v2.16-1 唯讀動詞偵測→6-33→1）；本頁卻把「有未完成交易？」放在 resolve 結束碼 0 且文法合之後，變成啟動器在收完 vk-resolve 後才判 6-33，與三叉「非 0 原碼傳出」互相矛盾（順序錯、誰做錯）；w4m 6-13（metadata 無完成標記）同樣是 resolve 側判定卻畫在 vk-resolve 驗完之後
- [排版] we6／we6x: 入口橢圓→「resolve sync：image ID ==…」菱形的線，與菱形→「≠ → 1」紅橢圓的「≠」線在 x≈810–950、y≈370 共用同一段，成雙箭頭線
- [排版] we6t／we6tx: 「文法合？」是→「有未完成交易？」菱形的線，與該菱形 是→「6-33」橙橢圓的線在 y≈755 共用 x≈420–950 一段，成雙箭頭線，「是」標籤歸屬不清
  (opt) [內容一致性] w4e: 誰做不明：w4e「image ID == metadata local_image_id？」畫在引擎 resolve（藍格），但 image ID 只能由啟動器 docker image inspect 取得；前頁 v1p16cc 啟動器只 inspect 引擎 image，沒有任何一格取工具 image ID 並傳給 resolve

## 66 流程 v2：離線包（2）add --local 逐工具 (v1p16c): must_fix 1 / optional 3
- [內容一致性] o10re: v2.16-1 共通前置格未落實：add --local 是可寫動詞，resolve 段起點應有「偵測既有進度檔？→ 是：先恢復（失敗 → 1 + 6-27）」；本頁 o10re 直接「算 extract 清單與輸入指紋」，沒有偵測／恢復格與 6-27 終點
  (opt) [內容一致性] o10s: 同 v1p16：「建執行紀錄」格無失敗出口，6-38 只從「寫 launcher_start」接出
  (opt) [內容一致性] oo1b: 一格兩事：「帶到離線機；之後每個工具各跑一次（一次一個）」是一個動作加一句迴圈說明
  (opt) [排版] oe22d: 「載」標籤擠在 docker load 框與紫色 image 框之間 20px 的短箭頭上，字疊到框邊；同頁三個「是」標籤都貼在菱形下尖上

## 67 流程 v2：離線包（2′）add --local：create／cp → apply (v1p16cb): must_fix 4 / optional 0
- [內容一致性] o10e4: 一格兩事：「寫 version.toml [tools] 行（最後寫）→ 刪 [progress]」是寫 version.toml 與刪 metadata [progress] 兩個動作、兩個檔（v1p12 t7 也把「刪進度檔」獨立成格），要拆成兩格
- [lint] o10e3: write-fail-edge：o10e3（寫 metadata）與 o10e4（寫 version.toml）兩個寫入格都沒有失敗出邊或失敗匯流，本頁沒有任何紅終點；v2.16-10 要求 add(2) 的「任一步失敗」走共通失敗匯流，本頁的兩個寫入卻失敗無終點
- [排版] oe26e／oe26ex: 「docker run 引擎 apply add」→「apply add：拿 flock」的順序線與「拿 flock」→「逾時 6-26」的失敗線共用同一水平段（y≈428），看起來是一條雙箭頭線，「逾時」標籤看不出屬於哪一段
- [內容一致性] o10e4: 一格兩事：「寫 version.toml [tools] 行 → 刪 [progress]」把寫與刪放同一格，而同頁「metadata 建 [progress]」與「寫 metadata」已拆兩格，粒度不一致；應拆成「寫 version.toml 行」「刪 [progress]」兩格

## 70 流程 v2：離線包（3′）apply sync 先驗後重裝 (v1p16ccc): must_fix 5 / optional 2
- [內容一致性] w4r0: 一格兩檔：「從 /dist 寫 cache/<repo>/、印記」把 cache 與 gen/<repo>.stamp 兩個檔放同一格（w4f 也列兩檔），而驗證分支已拆成 w4r（cache）與 w4r2（印記）兩格；不驗分支應同樣拆開
- [排版] wf2／wf3t: 同 v1p16cb：「docker run apply sync」→「拿 flock」與「拿 flock」→「逾時 6-26」共用同一水平段，成雙箭頭線
- [內容一致性] w4r0: 一格兩事：「否（不驗）：從 /dist 寫 cache/<repo>/、印記」把寫 cache 與寫印記合在一格（連帶檔案框 w4f 也合併），而驗證路徑已拆成「重裝一次」「寫印記」兩格；應比照拆開
- [lint] w4r0: onething：「從 /dist 寫 cache/<repo>/、印記」一格寫兩個檔（cache 目錄 + gen/<repo>.stamp）；同頁「重裝一次」分支已拆成 w4r（重寫 cache）＋ w4r2（寫印記），sync（2′）頁也拆成 m3c／m3b。建議拆成「從 /dist 寫 cache/<repo>/（暫存 → 整批替換）」與「寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）」兩格。
- [lint] w4f: onething：檔案框「cache/<repo>/、gen/<repo>.stamp」一格兩個檔；隨 w4r0 拆格後對應拆成兩個檔案框（同頁 w4rf／w4r2f 的做法）。
  (opt) [內容一致性] w4r0b: 缺分支：不驗分支 w4r0 → w4r0b → w5c 全程沒有寫入失敗的終點（驗證分支有 w4v2x），apply sync 寫 cache／印記／tools.just 失敗時無出口
  (opt) [排版] wf5n／wf7: 「要先驗既有 cache？」否 與第一個「全相符？」否 兩條線在 x=1600 共用同一段垂直幹線（y 783–1013），且幹線距右側五個檔案框右緣只有 10px，縮圖下像貼著框邊走

## 64 流程 v2：離線包（1）bootstrap.sh --local (v1p16): must_fix 1 / optional 3
- [lint] o3tx: end-color-text：o3tx「否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）」是使用者輸入錯、印可複製的處理指令，依圖例應為橙（需人處理），同型的 o3bx／o3cx 都是橙，只有它是紅
  (opt) [排版] oe3tj: 線標籤「是：tag 形（跳過 load／.digest）」直接壓在該線的水平段與轉角上
  (opt) [內容一致性] o2s: 起點拆成「建執行紀錄」「寫 launcher_start」後，只有 launcher_start 格接到「1 + 6-38：執行紀錄建不了／寫不進」；「建執行紀錄」格建不了時沒有出口（v1p16c o10s、v1p16cc w0l 同樣情形）
  (opt) [lint] o1: onething：「解開（SHA256SUMS 驗）：…」= 驗 checksum + 解包兩個動作（驗不過應停、解包才是下一步）。建議拆成「用 SHA256SUMS 驗離線包」與「解開：bootstrap.sh、各平台引擎 tar + .digest、local_bootstrap.sh（不含工具 tar）」兩格。

## 56 流程 v2：prune（2）apply 清暫存 (v1p9c): must_fix 1 / optional 3
- [排版] qe18ax: 「逾時」邊（apply prune 格左側 → 橙橢圓）與主流程 qe18（docker run 格 → apply prune 格左側）在 y=433、x=410～580 共線重疊，看不出哪段是進入、哪段是逾時出去；逾時邊應改從格的其他邊出或另走一條路
  (opt) [內容一致性] q13x: q13x 說「進度檔留著（下次可寫動詞先恢復：補做失敗的刪除）」，但 q13 的失敗含（1）頁啟動器做的 docker rm；docker 指令由啟動器執行、引擎不掛 socket，且進度檔（q12c2／q12d3）只記 .tmp 刪除結果，恢復三型（v1p12 r4n）補做不了 docker 資源刪除——與 notes「docker 指令由啟動器執行」矛盾
  (opt) [lint] q12j: write-fail-edge：q12j（建進度檔）與 q12k（刪進度檔）沒有失敗出邊或失敗匯流；q12c／q12d2 的失敗已由 q12c2／q12d3 記錄並流到 q13，不算成立
  (opt) [lint] resolve／apply（兩段）: term-dup-page0：名詞「resolve／apply（兩段）」第 0 頁已有，v2.16-18 要求只留第 0 頁沒有的詞

## 55 流程 v2：prune（1）resolve → 差集 → 刪 (v1p9): must_fix 1 / optional 3
- [排版] qe12z: 「是：只印差集…」→ 跨頁出口的線沿 x=30 走（離泳道左框只 10px），且長標籤「續（2）：apply prune --dry-run（零刪除）」直接壓在這條垂直線上、貼到泳道邊框；線應內縮、標籤放線旁
  (opt) [內容一致性] q7: 一格四命令：q7 把 docker container／image／network／volume ls 四個命令放同一格，而刪除側已拆成 q11a–q11d 四格（名詞表也寫「逐類資源一次一個命令」），列出側應同樣一類一格
  (opt) [可讀性] q11l: 「是 ↓ 對四類資源逐類刪：每個命令記成功／失敗，失敗的續刪其餘（結果帶到（2）頁）」是無框粗體文字疊在流程線上（線從字中穿過），既不是格也不是線標籤，與圖例任何一種形狀都對不上；應改成步驟格或縮成短線標籤
  (opt) [內容一致性] pend: 右上「已定（v2.4-10、grilling 9、Q24、Q25…）」便條仍在（v1p9c、v1p10、v1p11、v1p12 同樣有 pend），本輪說「沿革便條全刪」；便條列的是版本沿革且 5 行小字擠在 560×132，縮圖讀不出；若屬決策便條請維護者確認保留，否則刪

## 65 流程 v2：離線包（1′）docker run install (v1p16i): must_fix 1 / optional 2
- [排版] oe13／oe14: 「刪進度檔」→「install 成功後寫 version.local.toml」的順序線與「成功後寫」→ version.local.toml 檔案的「寫」線共用同一條水平段，畫面上變成一條兩端都有箭頭的線，方向與「寫」標籤歸屬不清
  (opt) [內容一致性] o8j: v2.16-1 共通前置格：install 是可寫動詞，o8j「建進度檔」之前沒有「偵測既有 .tmp.install → 依清除清單移除半成品」格（v1p12 r4n 第三型）；上次離線 install 中斷後再跑，本頁沒有恢復路徑
  (opt) [排版] oe12kf: 「刪」標籤夾在 v2 徽章與檔案框之間，字貼到「－.vendor_kit/.tmp.install.<id>.toml（刪）」框邊；「建」（oe11f）同樣擠在 20px 短箭頭上

## 59 狀態機 v2：交易與進度檔 (v1p12): must_fix 0 / optional 2
  (opt) [lint] te9a: decision：菱形 t6q 的出邊 te9a 無標籤（另一邊標「否」）；re4n（r2p → r2h）同樣無標籤，其他菱形皆兩邊都標是／否
  (opt) [排版] te5: 步驟格到右側虛線檔案框的單字標籤（te5 建、te7a 寫、te7b 換、te7 寫、re1 讀、re7 寫、re11 刪）兩端只隔 20px，12pt 單字幾乎填滿縫隙，縮圖看起來貼在兩邊框上；建議把檔案框右移 20～30px

## 57 流程 v2：update (v1p10): must_fix 2 / optional 2
- [排版] ue9: 「是」標籤（有 VENDOR_KIT_REGISTRY_TOKEN？→ WWW-Authenticate 格）兩端只隔 16px，標籤同時壓在菱形右尖與藍格左邊框上；把 u6g 右移或標籤上移
- [排版] ue13y: 「查詢成功？」菱形右尖同時是兩條進線（ue11 從 GET 格、ue12 從 WWW-Authenticate 格）的終點和「是」出線的起點，三條線在 (888～905,1128) 共線，進出分不開；進線應改接菱形頂點，「是」從底或右另出
  (opt) [lint] ue5: decision：菱形 u3 的出邊 ue5 無標籤（另一邊標「是」），只靠目標格文字「否 ↓」補
  (opt) [可讀性] u4l: 「否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）」是無框粗體文字節點插在流程線中（與 v1p9 q11l 同型），不符任何圖例形狀；應改成步驟格或短線標籤

## 18 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 (v1p5x): must_fix 1 / optional 0
- [排版] ae12z: LABEL 判斷框到「續 (1′) 頁」橢圓的「是」線只有 20px 長，標籤「是」整個壓在線與箭頭上

## 14 契約 v2：CI 契約⑤ 與驗收矩陣 (v1p3c): must_fix 0 / optional 2
  (opt) [排版] k1g_e: sync 的「3」出線水平段 y=353 緊貼「命中 → 1 拒絕」橢圓底（y=343）只差 10px，縮圖看起來像貼著橢圓走
  (opt) [可讀性] c_d3: 「發 Release vN（bootstrap.sh、tar、.digest、SHA256SUMS）」122px 寬框內折成 5 行，「tar、」單獨一行，縮圖下擠

## 17 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 (v1p5): must_fix 0 / optional 2
  (opt) [排版] ae8tn: 「否 → 值含 / 且存在同名檔？」到「續 (1″) 頁 A」的「否」線在 y≈1125 有一個約 30px 的不必要側折（無 waypoint，是自動路由造成）
  (opt) [排版] ae8tx: 同一菱形到 6-37 橢圓的「是」線走右→下→左→下→右五段折線，明顯多折

## 19 流程 v2：bootstrap.sh（1′）docker run install (v1p5i): must_fix 0 / optional 1
  (opt) [排版] a9f: 「install 寫（見「install（1）」頁起四頁）」虛線分組的標題壓在虛線框上緣上

## 22 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 (v1p5cm): must_fix 1 / optional 0
- [排版] ie4gy: 「是：不產、不動」標籤落在線的轉折（565,1104→640,1104）處，壓到「續「install (1″)」頁」虛線橢圓頂邊與旁邊 ie5 的箭頭，縮圖下文字與橢圓文字疊在一起

## 26 流程 v2：add（1′）apply 前置 (v1p5bcc): must_fix 1 / optional 2
- [排版] ce14ax: 同 v1p5c：「逾時」標籤擠在 flock 框與 1+6-26 橢圓間 30px 的短箭頭上，壓到箭頭
  (opt) [排版] ce16: 「原 argv 與計畫一致？」（w=300，中心 730）與下面各菱形（中心 780）沒對齊，「是」線多折一次；菱形對齊即可直線
  (opt) [lint] c9b: onething：「extract：docker create → cp → rm」一格三個 docker 指令；契約④ 頁（v1p3b）自己把它拆成 s3c／s3d／s3e 三格。建議拆成「docker create <image> /x」「docker cp c:/dist/. <tmp>/<repo>/」「docker rm」三格，或縮成單一件事「extract /dist 到暫存（create／cp／rm 見契約④）」。

## 23 流程 v2：install（1″）寫入 (v1p5cw): must_fix 1 / optional 0
- [可讀性] i4g: 「缺才建 baseline/.gitkeep（…）」一格同時含判斷（缺？）與動作（建），同頁 config.toml／version.toml 都是「菱形 + 動作」兩格，此處不一致，應拆成「baseline/.gitkeep 缺？」菱形 + 「建 .gitkeep」

## 37 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 (v1p7b): must_fix 2 / optional 2
- [排版] ce_q3cy: 線標籤「是（再問要建 X 嗎）」被右側匯流直線（x=1230）壓過字尾「嗎）」，縮圖下字被線切開
- [排版] ce_q8y: 線標籤「是（二進位換成新版？）」被右側匯流直線壓過「版？）」，線壓字
  (opt) [排版] ce_q4y: 線標籤「是（要替換嗎？）」右端貼到匯流直線，與上下兩條同病，建議三個標籤一起左移到轉角內側
  (opt) [排版] ce_9n: q9 底點出來的「否」線先走一小段再往左折一格才下去，和旁邊「是」線共用一小段出口；不該折的折了，兩線在頂點處重疊

## 42 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） (v1p7bcx): must_fix 1 / optional 0
- [排版] fb_s12j: 「建進度檔」框的「失敗」線與往左去「啟動器 grep 進度檔」的線（se12wh）折在同一個 y（緊貼框底），縮圖看起來像一條橫線從框底下整段穿過，分不出哪條是失敗、哪條是主流程；失敗線改從框右側直接出去或拉開高度

## 47 流程 v2：dev vendor_kit (v1p8ccc): must_fix 1 / optional 1
- [排版] ve4ax: 同 v1p8：「逾時」標籤擠在 v2 綠標與「1 + 6-26」橢圓之間，貼邊
  (opt) [可讀性] v10: 跨頁出口橢圓塞了四行邏輯（覆寫優先／gen/.stamp ≠ → 6-1／.Id ≠ → 1／不 pull），出入口應只寫去哪一頁，規則留給 sync 頁

## 48 流程 v2：undev <repo>（1）resolve → apply 前置 (v1p8c): must_fix 1 / optional 1
- [排版] ue8ax: 同 v1p8：apply flock 框→「1 + 6-26」的「逾時」標籤擠在 v2 綠標與紅橢圓之間，貼邊
  (opt) [lint] u5b: onething：同 c9b，「extract：docker create → cp → rm」一格三個指令；拆成 create／cp／rm 三格，或縮成單一件事「extract /dist 到暫存（見契約④）」。

## 41 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） (v1p7bcc): must_fix 0 / optional 2
  (opt) [排版] se12f: 「指定 @<tag>？」的「否」線在 x≈590 垂直下行，距「是：目標 = @<tag>」框左緣只約 10px，縮圖上貼著框走；且「否」標籤放在終點（CI 模式菱形旁）而不是出發的菱形旁
  (opt) [排版] se11y: inspect「有」線的回繞在 vendor_kit:vN 紫框右側與下側都只離約 15px，把紫框框住一半；回繞線外移

## 45 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） (v1p7bccd): must_fix 0 / optional 1
  (opt) [內容一致性] s13h: 菱形「啟動器：apply 後 grep 第一行 == apply 前（未變）？」把 grep 動作與比對判斷合在一格；E(a′) 頁（v1p7bca）同一件事拆成 s2h 白框 + 「第一行變了？」菱形，兩頁不一致

## 68 流程 v2：離線包（3）斷網 sync (v1p16cc): must_fix 1 / optional 2
- [排版] we2y: 「相符：用本機 tag（不 pull）」這條線從 inspect <tag> 菱形直落到 docker run 框，途中穿過無關的「否：docker image inspect <version.toml 的正式 ref@digest>」方框（w2b）並擦到「本機有該 image？」菱形右尖；線標籤又被「有」線（we5）橫切，縮圖下標籤被線壓字
  (opt) [內容一致性] w0l: 同 v1p16：「建執行紀錄」格無失敗出口，6-38 只從「寫 launcher_start」接出
  (opt) [排版] we2n: 「否」標籤直接壓在左側迴繞的垂直線上（x≈262）；兩個菱形之間的「是」標籤也壓在直線上

## 63 流程 v2：vendor_kit release（2）推 image 與資產 (v1p15c): must_fix 0 / optional 2
  (opt) [排版] ve14g: 「打」標籤擠在 20px 短箭頭上，字疊到「打正式 GHCR image tag」框右緣與 v2 徽章
  (opt) [可讀性] v11n: 「已釋出 image／Release 資產／fixture 永不刪；下游 Renovate 會看到新 tag@digest」便條靠泳道右邊界，文字貼到框緣、在「新」處硬換行

## 62 流程 v2：vendor_kit release（1）build 與驗收 (v1p15): must_fix 0 / optional 1
  (opt) [可讀性] v4x: 紅橢圓文字在「印失／敗的條號」處把一個詞硬拆兩行