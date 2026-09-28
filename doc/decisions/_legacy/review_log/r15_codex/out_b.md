OpenAI Codex v0.155.1
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: low
reasoning summaries: none
session id: 01a0bf59-d792-70d3-a261-f9d37969344e
--------
user
你是 draw.io 產生器 `disc_v1_b.py` 的修改者。它是 Python 腳本，每頁用 helper（`Flow`／`_Band`：box／free／files／H／D／U／R／LD／UL／LL／P 等）產生 cells，末尾 `addpage(pid, name, cells)`。附件 H 是 helper 與頁內共用段（不可改）；頁內容段從 `# ================= P5：bootstrap.sh` 起，只改那之後。
規則：只改指定頁；每格一件事；例子只用 `<repo>`；線上字級 12；顏色只用圖例（藍＝引擎做、白＝啟動器做、綠＝0、橙＝需人處理、紅＝失敗、白虛線橢圓＝跨頁出入口）；頁高 ≤ 2400、頁寬 ≤ 1660；不可讓線交叉（check_cross_v1b）或壓框（check_overlap）；名詞表每頁 ≤ 8 條且不含第 0 頁的詞；事件名只准 launcher_start／launcher_exit／engine_start／engine_exit。
要做的：附件 R 的 v2.17 全部 11 條；附件 F 的必修＋選修逐條；附件 L 的 lint warn 全清。**改不了的**（會造成交叉、頁高超、頁序固有）不要硬改：在該頁右下角加一個黃底便條（style 同 `pend`，標題「待處理問題」），條列「元件 id：一句說明」。
做法：先 `python3 run_v1_b.py` 確認能跑；改完再跑，並跑 `python3 check_overflow.py v1_b.drawio`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`（都要「共 0 筆」）與 `python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out`（非 termcov 的 warn 要 0）。最後輸出：改了哪些頁（id）與每頁改了什麼，加了哪些「待處理問題」便條，檢查結果。
注意：本檔的頁 id 只有 v1p5*／v1p6*／v1p7*／v1p8*（共 38 頁）。其他頁（v1p0…v1p4、v1p9 以後）在別的檔，由別人同時處理，不要碰 `disc_v1_a.py`、`disc_v1_c.py`、`gen_disc.py`、`drawio_common.py`、任何 check_*.py／lint_pages.py／extract_pages.py。附件 L、R 中屬於別的檔的頁（如 v1p1b／v1p2b／v1p3／v1p9c／v1p16*／v1p10）忽略；跨頁 term-diff 條目若本檔頁是其中一方，把本檔頁的名詞文字改成與較長版本一致（或直接刪掉那條名詞，只要不是本頁流程必需）。


==================== 附件 R：decisions/proposal_v2.md 的 v2.16 與 v2.17 ====================
# v2.16 第十四輪規則（2026-09-20；依第十三版 codex 4 組：R 已修 ≈232／未修 12／改壞 7，新發現 56）
1. **共通前置格**（每個可寫動詞頁的啟動器起點之後、resolve 之前）：「偵測既有進度檔？→ 是：先恢復（失敗 → 1 + 6-27）」（prune 例外：只列出）。唯讀動詞（sync／update）：偵測 → 6-33 → 1。
2. **resolve 結果分流一律三叉**：resolve 非 0 → 原碼傳出（不讀 stdout）；回 0 但 vk-resolve/1 文法不合 → 1 + 6-30；合法 → 繼續。四頁同型（add(1′)、sync(2)、B(1′)、E(a)）＋ prune(1)。
3. **事件名回歸 spec 註冊表**：圖例約定與圖上一律用 spec 名 `launcher_start／launcher_exit／engine_start／engine_exit`（L6 codex 提的 `*_started／*_completed` 改名**不採**，避免圖與註冊表不一致；改名若要做，先改 spec §4.10 註冊表再改圖——列待議）。
4. `--local` 判別依 v3.5 順序（`.tar` 結尾 → 檔案必須存在；否則含 `/` 且存在同名檔 → 6-37「檔案請改成以 .tar 結尾；image 請移走或改名同名檔」；否則 tag）：bootstrap(1) a8q／a8e／a8t、離線包(1) o3／o3n／o3cx、契約④ p3_fast。
5. bootstrap.sh 結束碼 = 失敗那一步原碼（install／add 回 2／3 照傳）；最低介面版 LABEL 檢查在任何 pull 之前（本機有 image 先 inspect LABEL；沒有才 pull 後檢查——spec 明寫「先於任何上網」，故：無本機 image 時允許 pull 後立即檢查、失敗 → 3 且不寫任何檔）。
6. install 自己執行時：先驗 git repo（主機側）再建執行紀錄（同 bootstrap）。
7. install(2) `.dockerignore`「已含這四行？」改逐行辨識，只加缺的行、只記實際新增的行。
8. 升引擎 E(c)(1)：先薄殼完整性檢查，再偵測 `.tmp.upgrade` 恢復。E(c)(2)：config.toml 拒絕建 → 不寫檔只記狀態；衝突 → 留標記、推基準版；解析失敗 → 留原檔、不推；config 建／替換／推副本各自失敗線。
9. remove(2) 拒絕刪 append 行：**仍完成移除**（版本鎖定行、cache、印記、基準版都刪），只在 metadata 之外另留一筆「孤兒 append 行」紀錄於 `baseline/.vendor_kit.toml`（同 .dockerignore append 記錄那張表）——不留 `baseline/<repo>/` 孤兒目錄。spec §1.2 remove 同步。
10. remove／uninstall／add(2) 的「任一步失敗」線：用一條共通失敗匯流（每個寫入格右側短線進匯流排）而不是只從三格拉。
11. sync：快路徑條件加「每個 `cache/<repo>/` 存在」；sync(2) 多 extract 迴圈「還有下一個 extract？」；tools.just 「在待辦？」菱形；斷網 sync 驗證相符後仍要「tools.just 缺 → 重生」；重裝成功後最後原子重生 tools.just。
12. upgrade B(1)：目標 == 現鎖定版且無待合併 → apply|no／0；本頁加共通前置格（規則 1）。E(a)：本機覆寫判斷在 pull 前；`s2h` 只比較正式 version.toml 引擎行前後。回退 D：apply 前置（flock、指紋、argv）、版本變動後全檔驗證＋失敗出口。
13. prune(1)：`q0l` 6-38 紅終點；resolve 三叉；prune(2)：每次刪除記成功／失敗，全部成功才刪進度檔；跨頁出口帶「有刪除失敗？」狀態。
14. 離線包(1′) install 失敗判斷在刪進度檔**之前**；離線包(3) 本機覆寫驗過就用本機 tag、不再 inspect 正式 ref；交易狀態機 `t1x` 拆兩橙終點、`t6x` 區分第一次 install 清半成品。
15. Renovate 頁：check.sh 步驟 ⓪ `git ls-files` 拒絕納管的 version.local.toml；④⑤ 原碼傳出（含 1）。
16. dev vendor_kit `v1lq` 文字：「image LABEL 的介面版 ≥ 薄殼自描述標頭的介面版，且 LABEL 檔案版 ≥ 現有 VK 檔的檔案版？」。dev／undev 進度檔記 image ID。
17. 名詞：remove／uninstall 的 `--dry-run` 不拉 image；6-33 條寫「sync／update 結束 1、help 仍 0」；B(1′) 名詞表「add 回 1」→「upgrade 回 1」；契約④ `s2b` 只在 add／upgrade（未指定 tag、非 CI）的 resolve 查 registry，update 是單段另畫；架構圖 pull timeout 歸啟動器；目錄樹 `p2_ver_n` 改「頂層 vendor_kit 行在 [tools] 前」；驗收詳表 18 補 URL 去 userinfo、19 補 .dockerignore 改一行的驗收。
18. 名詞表瘦身第二輪（G4／共通未修）：每頁名詞表 ≤ 8 條、只留本頁流程用到且第 0 頁沒有的詞；沿革便條全刪。
19.（Claude 三階段補充）啟動器起點「建執行紀錄」「寫 launcher_start」拆兩格（各頁）；install 就地執行也要 grep 引擎 ref → inspect → pull 段；add(1) `--local` 讀到的 digest 要有線進 resolve、離線不查 registry；flock 逾時 6-26 出口每個 apply 頁都要；契約④ `s4x` 終點顏色改依結束碼分、`p3_self` 補 E(c) 新接手路徑；契約⑤ `c_d` 拆三格、名詞對齊候選流程；架構圖便條不壓契約列、`w_cfg_l` 標籤位置、啟動器 grep version.toml／進度檔的線、掛載路徑一致（`.tmp.dist.<id>/ → /dist`、下有 `<repo>/`）；bootstrap(1′) 十字交叉、install 回 3 出口、清半成品歸屬（引擎寫入失敗自清；引擎異常結束由 bootstrap.sh 補清）；6-24 一律紅；其餘見 `review_v2r13_claude.md`。


# v2.17 第十五輪（最後一輪修圖；codex 執行、Claude 檢查；剩餘寫頁面清單）
1. 共通前置「偵測既有進度檔→先恢復」是**引擎**做的：放在 `docker run 引擎 <resolve|單段>` 之後、flock 之後、任何讀計畫／寫入之前（藍格）；啟動器不做恢復。sync／update 的 6-33 偵測同樣在引擎 resolve 內。
2. 契約④：快路徑條件補 cache 存在；resolve 三叉補文法出口；apply 結束碼分色 1＝失敗（紅）、2／3＝需人處理（橙）；update 單段線不繞；沿革便條刪。
3. 頁內失敗匯流終點文字不得宣稱「版本鎖定行不動」若有路徑在寫完鎖定行後才失敗（add(2) 刪進度檔失敗 → 另一終點「已寫入完成；進度檔留待下次刪」）。
4. bootstrap(2) 中止終點分色：6-24／6-30／寫入失敗 → 紅；原碼傳出（2／3）→ 橙。
5. install：`grep 命中 ≠ 1` 出口；`install <repo>` 誤用 6-17 出口；flock 逾時標籤不壓箭頭。
6. sync(1)：本機覆寫判斷在 inspect／pull 之前（覆寫中且本機無 image → 失敗，不 pull）；sync(1′)：`apply|no?` 判斷在三叉之後（非 0／文法不合先出）。
7. sync(2)：docker 段補 mount 記錄處理（dev 覆寫工具 `-v <dir>/dist:/dist/<repo>:ro`）；指紋重驗畫法統一為菱形「相同？」；sync(2′) 取件／重裝格失敗線進匯流。
8. Renovate 頁：⓪ 納管 → 1 停 加終點。B(1)：目標==現版判斷順序、長折線不貼綠終點。
9. 排版：所有標籤不壓線／不擠短線（ce2ll、ce3、ne5x、te7、me4vn、run_cli/ret_cli 等）；建檔格後續線從底或右側出。
10. lint 22 條（term-count v1p2b／v1p3、term-dup-page0 ×3、write-fail-edge prune(2)／離線包(2′)(3′)、end-color-text o3tx、term-diff ×2）全清。
11. 其餘 `review_v2r14_claude.md` 必修＋選修逐條處理；改不了的（幾何限制、頁序固有）不改，寫進該頁「待處理問題」便條（黃底、右下角、條列 id＋一句）。

==================== 附件 F：review_v2r14_claude.md 中屬本檔的頁（37 頁）====================
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

## 18 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 (v1p5x): must_fix 1 / optional 0
- [排版] ae12z: LABEL 判斷框到「續 (1′) 頁」橢圓的「是」線只有 20px 長，標籤「是」整個壓在線與箭頭上

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



==================== 附件 L：review_v2r14_lint.md 屬本檔頁的行 ====================
# 第十四版 lint warn（非 termcov）
- [xref-forward] v1p5i bA1: 前引：頁 19 只能引用序號更小的頁，卻見「install（1）」頁（序號 21）
- [xref-forward] v1p5i a9e: 前引：頁 19 只能引用序號更小的頁，卻見「install（1）」頁（序號 21）
- [xref-forward] v1p5i a9f: 前引：頁 19 只能引用序號更小的頁，卻見「install（1）」頁（序號 21）
- [write-fail-edge] v1p5cc i7: 寫入格缺失敗出邊或失敗匯流：「無：建 justfile（四行，逐字見右）、印建了什麼」
- [write-fail-edge] v1p5cc i11: 寫入格缺失敗出邊或失敗匯流：「是：append 那一行（import）、印加了什麼」
- [write-fail-edge] v1p5cc ign: 寫入格缺失敗出邊或失敗匯流：「無：建 .dockerignore（四行，逐字同右）、印建了什麼」
- [write-fail-edge] v1p5cc idl: 寫入格缺失敗出邊或失敗匯流：「刪進度檔 .tmp.install.<id>.toml（最後一步）」
- [term-dup-page0] v1p5cc symlink（根檔）: 名詞「symlink（根檔）」第 0 頁已有（同名或只差結尾括號），不必重列
- [term-diff] 跨頁 6-33（未完成交易）: 名詞「6-33（未完成交易）」有 2 個版本：
  v1（2 頁：v1p6 v1p8cx）長度 161
  v2（1 頁：v1p10）長度 185
  v1↔v2 差異：insert: v1「唯讀動詞偵測到 .tmp」 ↔ v2「唯讀動詞（sync／update／help）偵測到 .tmp」 ｜ insert: v1「ogress] in-progr」 ↔ v2「ogress] state=in-
- [term-diff] 跨頁 baseline/.gitkeep: 名詞「baseline/.gitkeep」有 2 個版本：
  v1（3 頁：v1p2 v1p2c v1p16i）長度 161
  v2（1 頁：v1p5cw）長度 117
  v1↔v2 差異：delete: v1「VK 自產的進 git 空檔」 ↔ v2「VK 自產進 git 的檔」 ｜ replace: v1「產的進 git 空檔：git 不追」 ↔ v2「自產進 git 的檔，hash 固

==================== 附件 H：disc_v1_b.py 前 560 行（helper 與頁內共用；不可改）====================
"""提案 v2 流程頁（v1p5…v1p8b，拆格後超高的頁再拆成 …c 頁）。
依據：decisions/proposal_v2.md（§2 表格、§5 初始檔規則、§6 啟動器、§7 CI）＋ v2.1 A–F ＋ v2.2 ＋ v2.3 ＋ v2.4 ＋ v2.5（最新優先），
＋ v2.6（2026-09-19 規格審查 16 條必修 + Q22–Q27，最高優先；decisions/interface_spec.md v2 為動詞行為／選項／結束碼／訊息逐字來源），
第十二輪（review_v2r11_findings.md 必修＋選修）：頁尾統一為「log_prune」→「launcher_exit」兩格 + 終點列（footer()/footer_edges()：所有終點的唯一前驅是 launcher_exit 格；各分支從左側匯流排 x=30 匯入，成功路徑直下）；每個 docker run 之後緊接 engine_start（EST_R／EST_A／EST_1）；啟動器 image 段統一 pullseg()（inspect／pull／image 同中心直下，本機有 → 頁面右側 bypass()，pull 失敗紅出口）；拆頁：bootstrap.sh（1′）v1p5i、install（1′）v1p5cw、D. 回退 v1p7bd、E(c)（1′）v1p7bcx；sync(1) 的 docker run 移到 sync(1′) 頁首；E(a) 的 (b) 段改成引用 sync(1)；C′ 出口改文字；內容：bootstrap 先驗 git／just 才建 log；install 的 git／巢狀檢查移到主機側；add 已接入且完成先於查 registry、--local 拆格；B(1) 6-3 橙出口；E(a) 新引擎 pull 移到 apply 前；E(c)(2) 建日誌＋config.toml 拆三格；remove(2) 逐行比對迴圈；undev u6x 措辭；名詞表逐頁裁剪（頁高 ≤ 2400）。備份：.v13（第十二輪前）。
第十一輪（v2.13 + v2.14 + review_v2r10_findings.md）：主路徑補線（B(1) b1q→b2→b2c、uninstall(1) x2→x2b…x2e）；每頁 resolve／apply 段各一格 engine_start、頁尾一格 log_prune／launcher_exit；
藍 = 引擎、白 = 啟動器全檔核對；gen/.stamp 只記引擎 ref、log.sh 帶自描述首行；sync(1′) 6-33 菱形；工具 image pull 失敗紅出口；uninstall(2) 不刪 log/、config.toml 依 v2.13 P6；
E(c)(2) config.toml 三方合併；install(2) igq 拆兩菱形；B(2) 逐檔改「情況菱形 → 同意？」兩層（每菱形兩出邊）；共用名詞改常數；備份：.v12（第十一輪前）。
以及 review_v2r4_findings.md 十六頁段落的必修＋選修（第五輪）。
只定義 pages_v1_b = [(pid, name, cells), ...]；不寫檔（run_v1_b.py 負責組 mxfile）。備份：.v1（v1）、.v2（拆頁前）、.v4（第三輪前）、.v5（第四輪前）、.v6（第五輪前）、.v7（第六輪前）、.v8（第七輪前）、.v9（第八輪前）、.v10（第九輪前）、.v11（第十輪前）。
第十輪（v2.11 + v2.12 + review_v2r9_findings.md）：upgrade vendor_kit 改回建進度日誌 .tmp.upgrade.<id>.toml（E(a) s2d／s2df、E(c)(1) s12j、E(c)(2) s13d 由新引擎刪；撤回 v2.10-4）；
操作紀錄檔：啟動器起點後「建 log 檔並寫 launcher_start」一格（bootstrap(1) a0l、install(1) i0l、add(1) c0l、sync(1) n0l、B(1) b0l、E(c)(1) s10l、dev d0l、remove(1) m0l、uninstall(1) x0l），引擎 append engine_start 一格（i1e／c1e／b1e／d1e／m1e／x1e）或入口文字帶過；
sync(1) 快路徑寫 sync_fast_path／launcher_exit（nql）；install(2) .dockerignore 四行（＋.vendor_kit/log/）；install(1) 建 config.toml（i4_5）；名詞表加操作紀錄檔／config.toml／6-38；
--local 名詞：bootstrap tag 形 digest = 既有 version.toml 或內嵌引擎 ref、add --local 只收存在的 .tar；bootstrap(2) 本次 add 失敗即中止（a10x）；E(a) se6vr／E(c)(1) se11vr 補「否」線；s12hz 改續跑入口樣式；E(c)(1) @tag／frozen 拆開；dev vendor_kit v9 橙；uninstall(2) x5d 拆 gen/／baseline/ 兩格。
第九輪（v2.10 + review_v2r8_findings.md）：需人動作的 1 結束一律橙（B(1′) b10dx／b10nx、dev d3a／d1x／d3c）；upgrade vendor_kit 不建進度日誌（E(c) 兩頁）；6-2b 只給第一行已改（E(a) s2lx、E(c)(2) s13x 拆兩個結束）；
迴圈菱形（bootstrap(2)「還有下一個 -t？」、sync(1′)「還有工具？」）；install(1) 第一次直接建檔；install(2) 刪日誌獨立格；sync(2) 驗證／重裝拆格；失敗線不 T 接（各自進紅橢圓不同入口）；ae11b 不交叉；ce28n／ce28y 標籤離框。
第八輪（v2.9 + review_v2r7_findings.md）：bootstrap tag 形不讀 .digest（a8q 否 → a8i）；dev 起點與菱形距 ≥ 40；add 私有 image 分支、dest／撞名改橙；sync 逐檔驗加「版本變動那次」（sync(2) 補一格）；
B(2) 解析檢查移到替換前、B(2′) 解析失敗檔不推 baseline；uninstall append 行逐行比對；be7 RD、be17 對齊、te14 頂點。
第七輪（v2.8 + review_v2r6_findings.md）：uninstall(2) 刪除集合補 baseline/ 根檔＋rmdir、xe16f/xe16w 不交叉；E(c) 薄殼比對移到拿鎖重驗後、改第一行前；bootstrap --local 三分支；
install 第一次不建日誌／修復型建 .tmp.install；add(2) 逐檔迴圈（LL 線型）；dev vendor_kit inspect 移到啟動器；菱形入口一律頂點（D/U 對齊不動菱形入口）；files(cols=2／cw) 兩欄檔案框；PRE 框走 <pre>+&#9; 真 tab。
第六輪（v2.7 + review_v2r5_findings.md）：一格一件事再細（inspect／pull 分格、建檔／印出分格、append／記 metadata 分格、materialize／原子替換分格、計畫／指紋分格、
判斷格只放一個問句）；declined 語意（已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒才 state=declined）；E(c) 查 registry 三種結果；undev vendor_kit 走 resolve→apply + .tmp.undev 日誌；
bootstrap Q18 分支；逐字範例框 whiteSpace=pre + &nbsp; 縮排；頁名 <repo> 單次跳脫；線標籤不壓線（菱形只從底端中央／側邊出線；RD／LD／R 標籤放在線旁）。
第五輪規則：不用 --pull never（啟動器 docker image inspect 驗本機 image ID，有就直接 run）；CI 一律寫「CI 為真（frozen）」；tools.just 一律 mod?；
橙 = 需要人動作（請先 undev／add／git init／重跑／upgrade vendor_kit／解衝突），紅 = 失敗；跨頁出入口標頁名，入口用白底虛線橢圓「來自 <頁名>」（ENTRY）。
泳道歸屬：所有判斷／合併／衝突處理畫在「引擎容器」；啟動器只有 grep 引擎 ref／gen/.stamp 比對／docker pull・create・cp・run・rm／轉發。
動詞兩段：引擎 resolve（不寫）→ 啟動器 docker → 引擎 apply（v2.5 §3：flock → 重驗指紋 → dry-run 分支 → 建進度日誌 → 寫入們 → 最後刪日誌）。
每格一件事；橢圓／菱形用 check_overflow.shape_spacing 補 spacing（v2.5 §15），高度以內接矩形估；檔案框一格一檔（多檔用 files() 標題容器）。"""
import glob, re, math
_latest = sorted(glob.glob("gen[0-9]*.py"), key=lambda p: int(re.findall(r"\d+", p)[0]))[-1]
exec(open(_latest).read().split("# ================= Page 1")[0])   # helper：v/e/page/legend_flow/terms/SW/LEAF/FILE/NOTE/PEND/ELLIPSE/PURPLE_LEAF/TITLE/EDGE/顏色
from check_overflow import wrap as _wrap, shape_spacing
if not getattr(page, "_single_esc", False):                                          # 頁名 <repo> 不雙重跳脫（v2.7 §12）
    import html as _html
    _page_raw = page
    def page(id, name, cells, **kw):
        out = _page_raw(id, name, cells, **kw)
        return out.replace(f'name="{esc(name)}"', f'name="{_html.escape(name, quote=True)}"', 1)
    page._single_esc = True

# ---------- 12pt 樣式 ----------
def _12(st): return st.replace("fontSize=14", "fontSize=12")
ORANGE = "#ffe6cc"
PAD = "spacingLeft=6;spacingRight=6;"                                                # 長方形文字不貼框（折行寬 = w−16，與估算一致）
W12 = _12(LEAF()) + PAD; F12 = _12(FILE) + PAD; G12 = _12(ELLIPSE(GREEN)); R12 = _12(ELLIPSE(RED)); D12 = _12(RHOMBUS)
O12 = _12(ELLIPSE(ORANGE))                                                           # 橙橢圓 = 需要人動作（1／3 且印指令；2 解衝突也橙；v2.6 §15）
ENTRY = _12(ELLIPSE("#ffffff")) + "dashed=1;"                                        # 白底虛線橢圓 = 來自其他頁的入口（v2.6 §15）
IMG = _12(PURPLE_LEAF) + PAD                                                         # 紫 = image（與主圖 legend 一致）
SUB = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;strokeWidth=2;" + PAD   # 藍 = 引擎子命令（容器內）
FTREE = _12(FILE) + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"     # 前／後目錄差異
PRE = ("rounded=1;whiteSpace=pre;html=1;fillColor=#ffffff;strokeColor=#666666;dashed=1;strokeWidth=2;fontSize=12;fontFamily=Courier New;"
       "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;")                  # 逐字範例檔案框：等寬、不置中、不 wrap；縮排用 &nbsp;（v2.7 §9）
NB4 = "&nbsp;&nbsp;&nbsp;&nbsp;"                                                    # 逐字框的 4 格縮排（html 不吃）
FGRP = _12(FILE) + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=2;fontStyle=1;container=1;collapsible=0;"   # 檔案標題容器（內排小框）
RULE = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=2;fontSize=12;fontStyle=1;"
        "align=left;verticalAlign=middle;spacingLeft=8;")                           # 橘框 = 規則（已定）
INV = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b85450;strokeWidth=3;fontSize=12;fontStyle=1;"
       "align=left;verticalAlign=middle;spacingLeft=8;")                            # 紅粗框（白底）= 不變量
PENDR = PEND + "fontStyle=1;"                                                       # 黃便條 = 待拍板
HDR = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e6e6e6;strokeColor=#999999;strokeWidth=1;fontSize=12;fontStyle=1;align=center;"
BAND = SW(NEUTRAL, 12).replace("startSize=38", "startSize=30")
LBL = TEXT(12) + "align=left;fontStyle=1;"
V2G = "#00b050"
TAG = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={V2G};strokeColor=none;fontColor=#ffffff;fontSize=9;fontStyle=1;"
       "align=center;verticalAlign=middle;spacing=0;spacingLeft=0;spacingRight=0;spacingTop=0;spacingBottom=0;")
def v2(st):
    """v2 改：不改框色，只在格子右上角加綠色小標籤「v2」（close() 時把 v2=1 記號換成標籤格）。"""
    return st + "v2=1;"


def fl(text):
    """把手動換行拿掉，交給 whiteSpace=wrap 自動折行（高度估算與畫面一致，行數最少）。英數之間補空白。"""
    out = []
    for i, ch in enumerate(text):
        if ch == "\n":
            a = text[i - 1] if i else ""; b = text[i + 1] if i + 1 < len(text) else ""
            out.append(" " if (a.isascii() and a.isalnum()) or (b.isascii() and b.isalnum()) else "")
        else: out.append(ch)
    return "".join(out)

def shape_f(st):
    """內接矩形係數：橢圓 0.707、菱形 0.5、其餘 1（spacing 補上後折行寬 = 內接矩形寬，與 check_overflow 同一套）。"""
    return 0.707 if st.startswith("ellipse") else (0.5 if st.startswith("rhombus") else 1.0)

def fit_w(text, w, st=""):
    """最寬的英數字（不能斷）塞不進內接矩形 → 自動加寬。"""
    f = shape_f(st); need = max((_wrap(ln, 12, 1e9)[1] for ln in text.split("\n")), default=0) + 16
    return w if w * f >= need else math.ceil(need / f)

def fit_h(text, w, minh=40, extra=0, st=""):
    """文字塞得進的高度（與 check_overflow 同一套估法；橢圓／菱形換算內接矩形）。"""
    f = shape_f(st)
    return max(minh, math.ceil((need_h(text, 12, w * f) + extra) / f) + 2)

def pre_v(cid, parent, st, text, x, y, w, h):
    """逐字框（whiteSpace=pre）：值包在 <pre> 內、tab 寫成 &#9;（XML 屬性裡的字面 tab 會被正規化）；同 disc_v1_a 的 code()（v2.7 §9）。"""
    import html as _html
    inner = _html.escape(text, quote=False).replace("\n", "<br>")
    htmlv = '<pre style="margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;">' + inner + '</pre>'
    val = _html.escape(htmlv, quote=True).replace("\t", "&#9;")
    return (f'<mxCell id="{cid}" value="{val}" style="{st}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def emit(cells, cid, parent, st, text, x, y, w, h):
    """輸出一格；style 帶 v2=1 → 另加右上角綠標籤；橢圓／菱形自動補 spacing（v2.5 §15）；whiteSpace=pre → pre_v。"""
    tag = "v2=1;" in st; st = shape_spacing(st.replace("v2=1;", ""), w, h)
    cells.append((pre_v if "whiteSpace=pre;" in st else v)(cid, parent, st, text, x, y, w, h))
    if tag: cells.append(v(f"{cid}_v2", parent, TAG, "v2", round(x + w - 24), round(y - 10), 30, 20))

# ---------- 泳道流程佈局 ----------
class Flow:
    """cols: [(名稱, x, w)]（絕對座標）。band() 開一個情境分組；box() 放格子（欄, 列）；H/D/U/R/LU/DL/LD/P 拉線；close() 排版並輸出。"""
    def __init__(self, cells, cols, band_x=20, band_w=1600, gap=20):
        self.cells, self.cols, self.bx, self.bw, self.gap = cells, {n: (x, w) for n, x, w in cols}, band_x, band_w, gap
        self.abs = {}; self.y = 0; self.n = 0
    def headers(self, y):
        for i, (n, (x, w)) in enumerate(self.cols.items()):
            self.cells.append(v(f"hdr{i}", "1", HDR, n, x, y, w, 28))
        self.y = y + 44
    def band(self, bid, title, pad=6, v2=False):
        return _Band(self, bid, title, pad, v2)

class _Band:
    def __init__(self, f, bid, title, pad, v2flag):
        self.f, self.bid, self.title, self.pad, self.v2 = f, bid, title, pad, v2flag
        self.boxes, self.edges, self.extra = [], [], []
    def box(self, cid, col, row, style, text, w, h=None, ax="c", minh=40, extra=0):
        """ax: 'c' 置中／'l' 靠欄左／'r' 靠欄右／數字 = 欄左偏移。h 未給就依文字算（給了也至少要塞得下）。"""
        w = fit_w(text, w, style)
        hh = fit_h(text, w, minh, extra + (6 if "v2=1;" in style and shape_f(style) == 1 else 0), style)
        h = hh if h is None else max(h, hh)
        self.boxes.append(dict(id=cid, col=col, row=row, st=style, text=text, w=w, h=h, ax=ax)); return cid
    def files(self, cid, col, row, title, items, w, ax="c", cols=1, cw=None):
        """檔案框一格一檔（v2.5 §14）：虛線標題容器，內排每檔一個小框（id = cid_0, cid_1…）；cols=2 → 兩欄（同列取最高；cw=(w1, w2) 指定各欄寬）。"""
        if cw is None: cw = [(w - 16 - 6 * (cols - 1)) // cols] * cols
        cols = len(cw); assert sum(cw) + 6 * (cols - 1) <= w - 16
        hs = [fit_h(t, cw[i % cols], 26) for i, t in enumerate(items)]
        rows = [max(hs[i:i + cols]) for i in range(0, len(hs), cols)]
        h = 26 + sum(rows) + 6 * len(rows) + 4
        self.boxes.append(dict(id=cid, col=col, row=row, st=FGRP, text=title, w=w, h=h, ax=ax, items=list(zip(items, hs)), cols=cols, cw=cw, rows=rows)); return cid
    def free(self, cid, style, text, x, y, w, h=None, minh=40):
        """不參與排版的格子（band 內相對座標）；h 未給就依文字算（給了也至少要塞得下）。"""
        w = fit_w(text, w, style); hh = fit_h(text, w, minh, 0, style)
        h = hh if h is None else max(h, hh)
        self.extra.append((cid, style, text, x, y, w, h))
    def free_files(self, cid, title, items, x, y, w):
        """free 版的檔案容器（一格一檔）；回傳容器高度。"""
        iw = w - 16; hs = [fit_h(t, iw, 26) for t in items]
        h = 26 + sum(hs) + 6 * len(items) + 4
        self.extra.append((cid, FGRP, title, x, y, w, h)); self.extra_items = getattr(self, "extra_items", {}); self.extra_items[cid] = list(zip(items, hs))
        return h
    def H(self, eid, s, t, label="", sy=0.5): self.edges.append(("H", eid, s, t, label, sy))
    def D(self, eid, s, t, label="", sx=0.5, tx=0.5, dy=0, al=False): self.edges.append(("D", eid, s, t, label, sx, tx, dy, al))
    def U(self, eid, s, t, label="", sx=0.5, tx=0.5, dy=0, al=False): self.edges.append(("U", eid, s, t, label, sx, tx, dy, al))
    def R(self, eid, s, t, label="", busx=0, tx=0.5, dy=0, vert=None):
        """從 s 右側出去，沿 x=busx 的「匯流排」往下，在 t 上方的縫隙轉進 t 頂端（多個右側結果匯到同一格）。vert 給了 → 標籤放在垂直段旁（True=右、'left'=左）。"""
        self.edges.append(("R", eid, s, t, label, busx, tx, dy, vert))
    def LD(self, eid, s, t, label="", busx=0, vert=None):
        """從 s 左側出去，水平到 x=busx，往下直接進 t 頂端（t 在下方、且 busx 落在 t 的寬度內）。vert 給了 → 標籤放在垂直段旁（'left'=線左、True=線右、'below'=水平段下）。"""
        self.edges.append(("LD", eid, s, t, label, busx, vert))
    def UL(self, eid, s, t, label="", busx=0, row=0, dy=0):
        """從 s 頂端往上到第 row 列上方的縫隙（再偏 dy），水平到 x=busx 的左側匯流排，往下到 t 的中線高度，再水平進 t 的左側（繞過中間所有格子的回流線）。"""
        self.edges.append(("UL", eid, s, t, label, busx, row, dy))
    def LL(self, eid, s, t, label="", busx=0):
        """從 s 左側出去，水平到 x=busx 的左側匯流排，往上到 t 的中線高度，再水平進 t 的左側（迴圈回上方的格子；標籤放匯流排左側）。"""
        self.edges.append(("LL", eid, s, t, label, busx))
    def RD(self, eid, s, t, label="", tx=0.5):
        """從 s 右側出去，水平到 t 的 x=tx 處，往下進 t 頂端（t 在右下；菱形的側邊出口，不從底端分兩條）。標籤放在水平段下方。"""
        self.edges.append(("RD", eid, s, t, label, tx))
    def BL(self, eid, s, t, label="", busx=0, sx=0.5):
        """從 s 底端往下到列間縫隙，水平到 x=busx 的左側匯流排，往下到 t 的中線高度，再水平進 t 的右側（t 在左下方；避開右側的寫入線）。"""
        self.edges.append(("BL", eid, s, t, label, busx, sx))
    def LU(self, eid, s, t, label="", tx=0.5):
        """從 s 右側出去，水平到 t 正下方，再往上進 t 底端（t 在上一列）。"""
        self.edges.append(("LU", eid, s, t, label, tx))
    def DL(self, eid, s, t, label="", sx=0.5):
        """從 s 底端往下到 t 的中線高度，再水平進 t 的側邊（t 在下一列的旁邊欄；不走列間縫隙，避免貼到同列的橢圓）。"""
        self.edges.append(("DL", eid, s, t, label, sx))
    def P(self, eid, s, t, label="", exit=None, entry=None, pts=(), pos=None, vert=None):
        self.edges.append(("P", eid, s, t, label, exit, entry, pts, pos, vert))
    def close(self):
        f = self.f; g = f.gap; A = f.abs; RT = f.rt if hasattr(f, "rt") else {}
        f.rt = RT; ST = f.st if hasattr(f, "st") else {}; f.st = ST; RB = f.rb if hasattr(f, "rb") else {}; f.rb = RB
        def rh_off(cid, xr):
            """菱形底部出口的實際周界點比外框底端高 |0.5−xr|×h（標籤要放在外框之外才不壓菱形邊；review r4）。"""
            return abs(0.5 - xr) * A[cid][3] if ST.get(cid, "").startswith("rhombus") else 0.0
        nrows = max([b["row"] for b in self.boxes], default=-1) + 1
        rh = [max([b["h"] for b in self.boxes if b["row"] == r] or [0]) for r in range(nrows)]
        top = [0] * nrows; y = f.y + 30 + self.pad
        for r in range(nrows): top[r] = y; y += rh[r] + g
        bh = 30 + self.pad + sum(rh) + max(nrows - 1, 0) * g + self.pad
        if self.extra: bh = max(bh, max(yy + h for _, _, _, _, yy, _, h in self.extra) + self.pad)
        bx, by = f.bx, f.y
        f.cells.append(v(self.bid, "1", BAND, self.title, bx, by, f.bw, bh))
        if self.v2: f.cells.append(v(f"{self.bid}_v2", self.bid, TAG, "v2", f.bw - 44, 5, 30, 20))
        for b in self.boxes:
            cx, cw = f.cols[b["col"]]
            if b["ax"] == "c": x = cx + (cw - b["w"]) / 2
            elif b["ax"] == "l": x = cx
            elif b["ax"] == "r": x = cx + cw - b["w"]
            else: x = cx + b["ax"]
            yy = top[b["row"]] + (rh[b["row"]] - b["h"]) / 2
            A[b["id"]] = (x, yy, b["w"], b["h"]); RT[b["id"]] = top[b["row"]]; ST[b["id"]] = b["st"]; RB[b["id"]] = top[b["row"]] + rh[b["row"]]
            emit(f.cells, b["id"], self.bid, b["st"], b["text"], round(x - bx), round(yy - by), b["w"], b["h"])
            if "items" in b:                                    # 檔案容器：小框相對容器座標（cols 欄）
                iy = 26; nc = b["cols"]; cw = b["cw"]
                for i, (t, hh) in enumerate(b["items"]):
                    r, c = divmod(i, nc)
                    emit(f.cells, f"{b['id']}_{i}", b["id"], F12, t, 8 + sum(cw[:c]) + 6 * c, iy, cw[c], b["rows"][r])
                    if c == nc - 1 or i == len(b["items"]) - 1: iy += b["rows"][r] + 6
        for cid, st, text, x, yy, w, h in self.extra:
            emit(f.cells, cid, self.bid, st, text, x, yy, w, h); A[cid] = (bx + x, by + yy, w, h); RT[cid] = by + yy; ST[cid] = st
            if cid in getattr(self, "extra_items", {}):
                iy = 26
                for i, (t, hh) in enumerate(self.extra_items[cid]):
                    emit(f.cells, f"{cid}_{i}", cid, F12, t, 8, iy, w - 16, hh); iy += hh + 6
        for ed in self.edges:
            kind, eid, s, t = ed[:4]
            sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
            if kind == "H":
                _, _, _, _, label, sy = ed
                if tx0 > sx0: f.cells.append(e(eid, s, t, label, (1, sy), (0, sy)))
                else: f.cells.append(e(eid, s, t, label, (0, sy), (1, sy)))
            elif kind in ("D", "U"):
                _, _, _, _, label, sxr, txr, dy, al = ed
                ex, nx = sx0 + sxr * sw, tx0 + txr * tw
                if 1 <= abs(ex - nx) < 40 or (al and abs(ex - nx) >= 1):   # 小折角很醜：把出／入點對齊成一直線（先動目標入口，再動來源出口）
                    r = (ex - tx0) / tw                                      # 目標是菱形 → 入口只用頂點（entryX=0.5），不接斜邊（review r6）
                    if 0.1 <= r <= 0.9 and not ST.get(t, "").startswith("rhombus"): txr, nx = r, ex
                    else:
                        r = (nx - sx0) / sw
                        if 0.1 <= r <= 0.9 and not ST.get(s, "").startswith("rhombus"): sxr, ex = r, nx
                if kind == "D":
                    ey, ny = sy0 + sh, ty0; gy = RT[t] - g / 2 + dy; exit_, entry = (round(sxr, 3), 1), (round(txr, 3), 0)
                else:
                    ey, ny = sy0, ty0; gy = RT[s] - g / 2 + dy; exit_, entry = (round(sxr, 3), 0), (round(txr, 3), 0)
                if abs(ex - nx) < 1:
                    pos = None
                    if label:
                        off = rh_off(s, sxr) if kind == "D" else 0.0; L = off + abs(ny - ey)
                        pos = -0.6 if off < 1 else min(0.5, 2 * ((off + 12) / L) - 1)   # 菱形：標籤放到外框底端之下 12px
                    f.cells.append(e(eid, s, t, label, exit_, entry, vert=True if label else None, pos=pos))
                else:
                    pts = [(ex, gy), (nx, gy)]
                    L1, L2, L3 = abs(gy - ey), abs(nx - ex), abs(ny - gy); tot = L1 + L2 + L3
                    pos = 2 * ((L1 + L2 / 2) / tot) - 1
                    f.cells.append(_edge(eid, s, t, label, exit_, entry, pts, pos))
            elif kind == "R":
                _, _, _, _, label, busx, txr, dy, vert = ed
                ey = sy0 + sh / 2; gy = RT[t] - g / 2 + dy; nx = tx0 + txr * tw
                pos = None
                if label and vert:
                    L1 = abs(busx - (sx0 + sw)); tot = L1 + abs(gy - ey) + abs(nx - busx) + abs(ty0 - gy)
                    pos = 2 * ((L1 + 14) / tot) - 1
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 0), [(busx, ey), (busx, gy), (nx, gy)], pos, vert if label else None))
            elif kind == "LD":
                _, _, _, _, label, busx, vert = ed
                ey = sy0 + sh / 2; txr = (busx - tx0) / tw
                pos = -0.7 if label else None
                if label and vert:
                    L1 = abs(sx0 - busx); tot = L1 + abs(ty0 - ey)
                    pos = 2 * ((L1 / 2) / tot) - 1 if vert == "below" else 2 * ((L1 + 14) / tot) - 1
                f.cells.append(_edge(eid, s, t, label, (0, 0.5), (round(txr, 3), 0), [(busx, ey)], pos, vert if label else None))
            elif kind == "UL":
                _, _, _, _, label, busx, row, dy = ed
                ex = sx0 + sw / 2; gy = top[row] - g / 2 + dy; ny = ty0 + th / 2
                f.cells.append(_edge(eid, s, t, label, (0.5, 0), (0, 0.5), [(ex, gy), (busx, gy), (busx, ny)], None))
            elif kind == "LL":
                _, _, _, _, label, busx = ed
                ey = sy0 + sh / 2; ny = ty0 + th / 2
                L1 = abs(sx0 - busx); tot = L1 + abs(ey - ny) + abs(tx0 - busx)
                pos = 2 * ((L1 + 14) / tot) - 1 if label else None
                f.cells.append(_edge(eid, s, t, label, (0, 0.5), (0, 0.5), [(busx, ey), (busx, ny)], pos, "left" if label else None))
            elif kind == "RD":
                _, _, _, _, label, txr = ed
                ey = sy0 + sh / 2; nx = tx0 + txr * tw
                L1 = abs(nx - (sx0 + sw)); tot = L1 + abs(ty0 - ey)
                if not label: pos, vert = None, None
                elif L1 >= 24: pos, vert = 2 * ((L1 / 2) / tot) - 1, "below"        # 水平段夠長：標籤放水平段下方
                else: pos, vert = 2 * ((L1 + 12) / tot) - 1, True                   # 水平段太短：標籤放垂直段右側
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 0), [(nx, ey)], pos, vert))
            elif kind == "BL":
                _, _, _, _, label, busx, sxr = ed
                ex = sx0 + sxr * sw; gy = RB[s] + g / 2; ny = ty0 + th / 2
                f.cells.append(_edge(eid, s, t, label, (round(sxr, 3), 1), (1, 0.5), [(ex, gy), (busx, gy), (busx, ny)], None))
            elif kind == "LU":
                _, _, _, _, label, txr = ed
                ey = sy0 + sh / 2; nx = tx0 + txr * tw
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 1), [(nx, ey)], -0.3 if label else None))
            elif kind == "DL":
                _, _, _, _, label, sxr = ed
                ex = sx0 + sxr * sw; ny = ty0 + th / 2; entry = (1, 0.5) if tx0 < sx0 else (0, 0.5)
                off = rh_off(s, sxr); L1 = ny - (sy0 + sh); L2 = abs(ex - (tx0 + tw if tx0 < sx0 else tx0))
                pos = 2 * ((off + max(L1 / 2, 12)) / (off + L1 + L2)) - 1   # 菱形：從外框底端再往下量
                f.cells.append(_edge(eid, s, t, label, (round(sxr, 3), 1), entry, [(ex, ny)], pos, vert=True))
            else:
                _, _, _, _, label, exit_, entry, pts, pos, vert = ed
                f.cells.append(_edge(eid, s, t, label, exit_, entry, pts, pos, vert))
        f.y = by + bh + 16
        return self

def _edge(eid, s, t, label, exit_, entry, pts, pos=None, vert=None):
    st = EDGE + f"exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if vert == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    elif vert == "below": st += "align=center;verticalAlign=top;spacingTop=6;spacingBottom=0;"
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    arr = "".join(f'<mxPoint x="{round(px)}" y="{round(py)}"/>' for px, py in pts)
    xa = "" if pos is None else f' x="{pos:.2f}"'
    return (f'<mxCell id="{eid}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{s}" target="{t}">'
            f'<mxGeometry{xa} relative="1" as="geometry"><Array as="points">{arr}</Array></mxGeometry></mxCell>')

def pend(cells, text, x=1080, w=520, style=PENDR):
    h = fit_h(text, w, 40, 4)
    cells.append(v("pend", "1", style, text, x, 12, w, h)); return 12 + h

LEG1 = [(LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", 200, 60, 0), (RHOMBUS, "黃：判斷", 140, 64, 0),
        (ELLIPSE(GREEN), "綠：起點／終點", 140, 44, 8), (ELLIPSE(RED), "紅：失敗終止（拉不到／寫壞）", 190, 56, 2),
        (ELLIPSE(ORANGE), "橙：需要人動作（1／3 印指令；2 解衝突）", 210, 56, 2),
        (LEAF(), "白：步驟", 88, 40, 10), (FILE, "虛線框：專案裡的檔案", 170, 40, 10)]
LEG2 = [("entry", ENTRY, "虛線橢圓：跨頁入口", 200), ("note", NOTE, "便條：補充說明", 120), ("pend", PENDR, "黃便條：待拍板", 130), ("rule", RULE, "橘框：規則（已定）", 150),
        ("inv", INV, "紅粗框：不變量", 130), ("sub", SUB, "藍：引擎子命令（容器內）", 190), ("img", IMG, "紫：image（引擎與工具）", 170),
        ("hdr", HDR, "灰底：泳道／表格表頭", 170), ("v2", v2(W12), "右上綠標 v2：與 v1 不同處", 200), ("tree", FTREE, "虛線樹：目錄差異", 140)]
def terms2(prefix, x, y, rows, kw=150, vw=610, gap=40):
    """名詞表排兩欄（省高度）；id 沿用 {prefix}_tk{i}/_tv{i}。"""
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 34, 200, 28)]
    hs = [max(28, math.ceil(max(need_h(k, 12, kw), need_h(d, 12, vw)))) for k, d in rows]
    tot = sum(hs); acc = 0; split = len(rows)
    for i, h in enumerate(hs):
        acc += h
        if acc >= tot / 2: split = i + 1; break
    for cx, idx in ((x, range(0, split)), (x + kw + vw + gap, range(split, len(rows)))):
        cy = y
        for i in idx:
            k, d = rows[i]; h = hs[i]
            c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, cx, cy, kw, h)); c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, cx + kw, cy, vw, h)); cy += h
    return c
def foot(cells, prefix, y, rows, keys):
    """legend 兩列 + 本頁名詞（兩欄）。keys = 本頁用到的第二列圖例（每頁都有便條 → 一律含 note）。"""
    keys = set(keys) | {"note"}
    x = 40
    for i, (st, t, w, h, dy) in enumerate(LEG1):
        emit(cells, f"{prefix}_lg{i}", "1", _12(st), t, x, y + dy, w, h); x += w + 20
    cells.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序（指向檔案時 = 寫入／讀取）", x, y, 300, 60))
    x = 40
    for k, st, t, w in LEG2:
        if k in keys: emit(cells, f"{prefix}_lgx_{k}", "1", st, t, x, y + 68, w, 36); x += w + 20
    cells += terms2(prefix, 40, y + 140, rows)

COLS5 = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 280), ("引擎容器", 580, 400), ("GHCR", 1000, 220), ("專案目錄", 1240, 360)]
COLS7 = [("使用者", 40, 220), ("Renovate（GitHub 上）", 280, 180), ("啟動器（主機 sh）", 480, 240), ("引擎容器", 740, 360), ("GHCR", 1120, 180), ("專案目錄", 1320, 280)]
COLS5W = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 320), ("引擎容器", 620, 380), ("GHCR", 1020, 200), ("專案目錄", 1240, 360)]   # 啟動器欄要兩條車道（判斷＋pull）的頁
COLS5B = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 460), ("引擎容器", 760, 260), ("GHCR", 1040, 180), ("專案目錄", 1240, 360)]   # bootstrap.sh：啟動器兩條車道各 200
COLS5I = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 140), ("引擎容器", 440, 560), ("GHCR", 1020, 200), ("專案目錄", 1240, 360)]   # install（2）：引擎欄三條車道
U, L, E, G, P, RN = "使用者", "啟動器（主機 sh）", "引擎容器", "GHCR", "專案目錄", "Renovate（GitHub 上）"
ALL = {"note", "pend", "rule", "inv", "sub", "img", "hdr", "v2", "tree"}   # "entry" 只在有跨頁入口的頁加
EXIT3 = ("結束狀態 0／1／2／3", "0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）")
def newpage(cells_title, note, cols, note_style=NOTE):
    cells = [v("title", "1", TITLE, cells_title, 40, 20, 1000, 34)]
    ny = pend(cells, note, style=note_style)
    F = Flow(cells, cols); F.headers(ny + 8)
    return cells, F
pages_v1_b = []

# ================= 第十三輪共用（頁內；helper 段不動；v2.15-1～6、r12_codex/findings1–4）=================
# 1. 名詞換新（v2.15-1、decisions/review/terms.md）：TR() 對照表；用「包住」helper 的方式套到每格文字、線標籤、名詞表、頁名（helper 本體不改；
#    box/free/files 在算高度前先換，v() 再換一次 → 規則一律冪等）。第 0 頁已有的詞不再進各頁名詞表（BM_T／MD_T／SYM_T／FROZEN_T／INIT_T／VL_T／EXIT3… 移除）。
# 2. 執行紀錄改圖例約定（v2.15-2）：不畫 launcher_exit／log_prune 扇出格與各段 engine_start 格；圖例加兩條隱含約定（foot()）；
#    只留啟動器起點「建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38）」一格，其失敗畫紅出口；終點直接接各自分支（footer()/footer_edges() 重寫：無匯流）。
# 3. 跨頁出入口一律白虛線橢圓 ENTRY（v2.15-3）：入口「來自「X」頁」、出口「續「X」頁」。
# 4. vk-resolve/1 只傳協定內容（v2.15-4）：RES_OUT 固定文字；resolve 非 0 → 啟動器不讀 stdout（NZ_T）；apply 多「原 argv 與計畫一致？」一格（ARGV_T）。
# 5. 詢問格三出口（v2.15-6）：共用小圖示 tty()（橙小標「無 tty→1+6-4」貼在問句格右上；圖例 tty）。
import re as _re
_TR = [
 (r"工具 repo", "下游 repo"), (r"工具 image", "下游 image"), (r"使用者的檔", "專案檔"), (r"使用者檔", "專案檔"), (r"你的檔", "專案檔"),
 (r"(?<!下游)使用者", "下游使用者"), (r"下游專案", "專案"),
 (r"正規行", "版本鎖定行"), (r"(?<!版本)鎖定行", "版本鎖定行"),
 (r"(?<![:/A-Za-z_.])baseline(?![/:_.A-Za-z])", "基準版"),
 (r"進度日誌", "進度檔"), (r"操作紀錄檔", "執行紀錄"), (r"建 log 檔並寫", "建執行紀錄、寫"), (r"(?<![A-Za-z_])log 檔", "執行紀錄"),
 (r"CI 為真（frozen）", "CI 模式"), (r"frozen（CI 為真）", "CI 模式"), (r"（frozen）", ""), (r"非 frozen", "非 CI 模式"), (r"frozen", "CI 模式"),
 (r"CI 不為真", "非 CI 模式"), (r"CI 為真", "CI 模式"), (r"需改 tracked 檔", "需改任何進 git 的檔"), (r"tracked 五檔", "進 git 的五檔"),
 (r"tracked 檔", "進 git 的檔"), (r"tracked 薄殼", "進 git 的薄殼"), (r"tracked", "進 git 的"),
 (r"協定號", "介面版"), (r"協定不合", "介面版不合"), (r"schema 號", "檔案版"), (r"(?<![A-Za-z_])floor(?![A-Za-z_])", "最低介面版"),
 (r"materialize", "取件"), (r"需要人動作", "需人處理"), (r"自身升級", "升引擎"),
 (r"薄殼首行自描述", "薄殼自描述首行"), (r"首行自描述", "自描述首行"),
 (r"launcher_started", "launcher_start"), (r"engine_started", "engine_start"),                      # v2.16-3：事件名回歸 spec §4.10 註冊表
 (r"launcher_completed\|failed", "launcher_exit"), (r"engine_completed\|failed", "engine_exit"),
]
_TRC = [(_re.compile(p), r) for p, r in _TR]
def TR(s):
    """名詞對照（冪等）；非字串原樣回傳。"""
    if not isinstance(s, str) or not s: return s
    for p, r in _TRC: s = p.sub(r, s)
    return s

if not globals().get('_TR_WRAPPED'):   # 冪等：同一 namespace 重複 exec（gen_disc 先經 disc_v1_c 再 exec 本檔）時不可重包，否則 v→v 無限遞迴
    _box0, _free0, _files0, _ffiles0 = _Band.box, _Band.free, _Band.files, _Band.free_files
    _v0, _e0, _edge0, _pend0, _newpage0 = v, e, _edge, pend, newpage
    _TR_WRAPPED = True
def _box1(self, cid, col, row, style, text, w, *a, **k): return _box0(self, cid, col, row, style, TR(text), w, *a, **k)
def _free1(self, cid, style, text, x, y, w, *a, **k): return _free0(self, cid, style, TR(text), x, y, w, *a, **k)
def _files1(self, cid, col, row, title, items, w, *a, **k): return _files0(self, cid, col, row, TR(title), [TR(t) for t in items], w, *a, **k)
def _ffiles1(self, cid, title, items, x, y, w): return _ffiles0(self, cid, TR(title), [TR(t) for t in items], x, y, w)
_Band.box, _Band.free, _Band.files, _Band.free_files = _box1, _free1, _files1, _ffiles1
def v(id, parent, style, value, x, y, w, h): return _v0(id, parent, style, TR(value), x, y, w, h)
def e(id, src, tgt, label="", *a, **k): return _e0(id, src, tgt, TR(label), *a, **k)
def _edge(eid, s, t, label, *a, **k): return _edge0(eid, s, t, TR(label), *a, **k)
def pend(cells, text, x=1080, w=520, style=PENDR): return _pend0(cells, TR(text), x, w, style)
def newpage(cells_title, note, cols, note_style=NOTE):
    """第十四輪（v2.16-18）：沿革便條全刪 —— note 參數保留簽名但不畫；表頭直接接在頁標題下。"""
    cells = [v("title", "1", TITLE, cells_title, 40, 20, 1000, 34)]
    F = Flow(cells, cols); F.headers(64)
    return cells, F
def addpage(pid, name, cells): pages_v1_b.append((pid, TR(name), cells))

# ---------- 圖例（第十三輪）：跨頁出入口、tty 小標、兩條隱含約定 ----------
TTY = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=9;fontStyle=1;align=center;verticalAlign=middle;"
       "spacing=0;spacingLeft=0;spacingRight=0;spacingTop=0;spacingBottom=0;")
TTY_TXT = "無tty→6-4"
def tty(F, cells, *ids):
    """問句格（菱形／步驟）左上角加橙小標「無 tty→1+6-4」= 第三出口（v2.15-6 共用小圖示；圖例 tty）。close() 之後呼叫。"""
    for cid in ids:
        x, y, w, h = F.abs[cid]
        cells.append(v(f"{cid}_tty", "1", TTY, TTY_TXT, round(x), round(y - 10), 76, 20))   # 左上角（菱形頂點在中央，右上有 v2 標）
LEG2 = [("entry", ENTRY, "白虛線橢圓：跨頁出入口", 220), ("note", NOTE, "便條：補充說明", 120), ("pend", PENDR, "黃便條：待拍板", 130),
        ("rule", RULE, "橘框：規則（已定）", 130), ("inv", INV, "紅粗框：不變量", 120), ("sub", SUB, "藍：引擎（容器內）做的", 160), ("img", IMG, "紫：image", 100),
        ("hdr", HDR, "灰底：泳道／表頭", 130), ("v2", v2(W12), "右上綠標 v2：與 v1 不同", 180), ("tree", FTREE, "虛線樹：目錄差異", 140),
        ("tty", TTY, "橙小標：問句無 tty／EOF 且無 -y → 1 + 6-4（Ctrl-C 中止、不記拒絕）", 300)]
LEG_IMPL = ("圖例約定（v2.15-2、v2.16-3）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_exit（結束碼、耗時）；"
            "每個「docker run 引擎」格隱含 —— 容器開始寫 engine_start、結束寫 engine_exit（同一執行紀錄；事件名 = spec §4.10 註冊表）。白 = 啟動器（主機）做的。")
def foot(cells, prefix, y, rows, keys):
    """legend 兩列 + 兩條隱含約定 + 本頁名詞（兩欄；只列第 0 頁沒有的頁內特有詞）。"""
    keys = set(keys) | {"note"}
    x = 40
    for i, (st, t, w, h, dy) in enumerate(LEG1):
        emit(cells, f"{prefix}_lg{i}", "1", _12(st), t, x, y + dy, w, h); x += w + 20
    cells.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序（指向檔案時 = 寫入／讀取）", x, y, 300, 60))
    x = 40
    for k, st, t, w in LEG2:
        if k in keys: emit(cells, f"{prefix}_lgx_{k}", "1", st, t, x, y + 68, w, 36); x += w + 20
    cells.append(v(f"{prefix}_lgi", "1", TEXT(12) + "align=left;", LEG_IMPL, 40, y + 108, 1540, 40))
    cells += terms2(prefix, 40, y + 188, [(TR(k), TR(d)) for k, d in rows])

# ---------- 共用名詞（只留第 0 頁沒有的；term-diff：同名各頁同文） ----------
LOGT = [   # 執行紀錄（第 0 頁已有）不再列；只留 config.toml 與 6-38
 ("config.toml（install／uninstall）", ".vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設"),
 ("6-38", "執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log"),
]
RA_T = ("resolve／apply 兩段", "動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④")
RAD_T = ("resolve／apply／--dry-run", "resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）")
FIP_T = ("flock／指紋", "flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）")
GM_T = ("git merge-file --diff3", "git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出")
GS_T = ("gen/.stamp", "只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行")
BDN_T = ("B／D／N", "B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過")
BOOT_T = ("bootstrap.sh 檔名與內嵌 ref", "release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>")
GT_T = ("gen/tools.just／mod?", "不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe")
E2B_T = ("6-2b", "第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度檔保留）")
PULLX_T = ("6-24／6-31（pull 失敗）", "docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止")
E22_T = ("6-22（upgrade 逐檔問句）", "「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問")
REN_T = ("Renovate", "GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁")
E33_T = ("6-33（未完成交易）", "唯讀動詞偵測到 .tmp.<verb>.*.toml 或 metadata [progress] in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；sync／update 結束 1，help 仍 0")
E4_T = ("6-4（無 tty）", "需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）")
E12_T = ("6-12（指紋不同）", "apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1")
MSG_T = ("6-16／6-23／6-28／6-35", "前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）")
NZ_T = ("resolve 非 0", "resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）")
ARGV_T = ("原 argv 與計畫一致", "apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）")
N5I = "已定（v2.4 Q17、v2.5 §8、v2.6、v2.13 P5、v2.15-11）：install 第一次／修復判定用薄殼自描述首行；進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata state=managed）、存在不動；根 justfile／.dockerignore 無則建、有則問後才加、symlink 不寫只印指示；引擎 image 一律先 docker image inspect，本機有就不 pull。"
LS_T = "建執行紀錄、寫 launcher_start（失敗 → 1 + 6-38，零寫入）"     # （第十四輪改用 lstart() 拆兩格；此常數只留給舊引用）
LS1 = "寫 launcher_start（失敗 → 1 + 6-38，零寫入）"                    # 啟動器起點第二格（v2.16-19）
LSX = "1 + 6-38：執行紀錄建不了／寫不進（零寫入）"                    # 其紅出口
E27X = "1 + 6-27：恢復失敗（未恢復：<檔名>，逐檔列出）"                # 共通前置格的紅出口（v2.16-1）
E33X = "1 + 6-33：偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>"   # 唯讀動詞（sync／update）
E26X = "1 + 6-26：專案目錄被鎖定（PID <pid>，自 <time>）；60 秒內未釋放"   # flock 逾時出口（每個 apply 頁都有）
NZX = "1／2／3：resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）"   # resolve 三叉（v2.16-2）第一叉
E30X = "1 + 6-30：引擎輸出不完整或不相容，未執行任何動作（stdout 文法不合）"   # 第二叉
RES_OUT = "stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋（只傳協定內容）"   # v2.15-4
NZ_X = "1／2／3：resolve 非 0（啟動器不讀 stdout、不跑 docker／apply）"
ARGV_Q = "原 argv 與計畫一致？"
E64 = "1 + 6-4：無 tty／EOF 且無 -y（Ctrl-C 中止、不記拒絕）"

def footer(b, F, row, ends, spacer=0, sp="r"):
    """終點列（第十三輪：各分支直接接自己的終點，無匯流）。spacer > 0 → 第 row 列放透明佔位格（高 16×spacer+12），給左右匯流排的
    水平段分層用，終點放 row+1；否則終點放 row。sp = 佔位格放哪（不能被水平段穿過）：'r' 專案目錄欄右緣（只有左側來源時）、
    'l' 下游使用者欄左緣（只有右側來源時）、'm' GHCR 與專案目錄欄之間（兩側都有；右側終點須放 P 欄）。
    ends: [(cid, style, text)] 依序放槽位 U、L、E-l、E-r、G、P（欄寬 ≥ 180；E ≥ 360 兩槽），或 (cid, style, text, col, ax) 指定位置。回傳終點所在列。"""
    r0 = row
    if spacer:
        hh = 16 * spacer + 12
        col, ax = {"r": (P, "r"), "l": (U, "l"), "m": (G, F.cols[G][1] + 5)}[sp] if sp != "m" or G in F.cols else (E, F.cols[E][1] + 5)
        b.box("_sp", col, row, "text;html=1;fillColor=none;strokeColor=none;", "", 10, h=hh, minh=hh, ax=ax); r0 = row + 1
    slots = []
    for col in (U, L, E, G, P):
        if col not in F.cols: continue
        cx, cw = F.cols[col]
        if col == E and cw >= 360:
            sw = min(220, (cw - 20) // 2); slots += [(col, "l", sw), (col, "r", sw)]
        elif cw >= 180: slots.append((col, "c", min(220, cw)))
    i = 0
    for en in ends:
        cid, st, text = en[:3]
        if len(en) > 3: b.box(cid, en[3], r0, st, text, 220, ax=en[4])
        else:
            col, ax, sw = slots[i % len(slots)]; b.box(cid, col, r0 + i // len(slots), st, text, sw, ax=ax); i += 1
    return r0

def footer_edges(F, srcs, busl=None, busr=None, dlevel=0):
    """close() 之後畫終點線。srcs: [(eid, src, label, how, end[, sx])]：
      'l'／'lb' 左出（'lb' 從底端 sx 出、經該列底縫隙）→ 左匯流排 → 分層水平段 → 終點頂端；'r'／'rb' 右側同理；'d' 從底端直下（不對齊時在終點上方縫隙折一次）。
    分層：同側依來源由上到下排序，最上面的用最外側匯流排、最低的水平層、最左（右側：最右）的終點 → 不交叉（頁內終點順序須照這規則排）。"""
    A, RT, RB, g = F.abs, F.rt, F.rb, F.gap
    if busl is None: busl = F.cols[U][0] - 10
    if busr is None: busr = F.cols[P][0] + F.cols[P][1] + 10
    def rh_off(cid, xr): return abs(0.5 - xr) * A[cid][3] if F.st.get(cid, "").startswith("rhombus") else 0.0
    ends = {s[4] for s in srcs}; ytop = min(RT[en] for en in ends) if ends else 0
    for side in ("l", "r"):
        grp = sorted([s for s in srcs if s[3] in (side, side + "b")], key=lambda s: (A[s[1]][1], A[s[1]][0]))
        n = len(grp)
        for i, it in enumerate(grp):
            eid, s, label, how, en = it[:5]; sxr = it[5] if len(it) > 5 else 0.5
            sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[en]; nx = tx0 + tw / 2
            busx = (busl - 14 * (n - 1 - i)) if side == "l" else (busr + 14 * (n - 1 - i))
            lev = ytop - g / 2 - 12 - 16 * i
            if how in ("l", "r"):
                left = side == "l"; ex = sx0 if left else sx0 + sw; ey = sy0 + sh / 2
                pts = [(busx, ey), (busx, lev), (nx, lev)]
                tot = abs(ex - busx) + abs(lev - ey) + abs(nx - busx) + abs(ty0 - lev)
                F.cells.append(_edge(eid, s, en, label, (0 if left else 1, 0.5), (0.5, 0), pts, 2 * (14 / tot) - 1 if label else None, "below" if label else None))
            else:
                ex = sx0 + sxr * sw; gy = RB[s] + g / 2; pts = [(ex, gy), (busx, gy), (busx, lev), (nx, lev)]
                off = rh_off(s, sxr); L1 = gy - (sy0 + sh); tot = off + L1 + abs(ex - busx) + abs(lev - gy) + abs(nx - busx) + abs(ty0 - lev)
                F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (0.5, 0), pts, 2 * ((off + max(L1 / 2, 12)) / tot) - 1 if label else None, True if label else None))
    for it in srcs:
        eid, s, label, how, en = it[:5]; sxr = it[5] if len(it) > 5 else 0.5
        if how != "d": continue
        sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[en]; ex = sx0 + sxr * sw; nx = tx0 + tw / 2
        if abs(ex - nx) < 1 or (tx0 + 0.1 * tw <= ex <= tx0 + 0.9 * tw and not F.st.get(en, "").startswith("ellipse")):
            txr = round((ex - tx0) / tw, 3); off = rh_off(s, sxr); L1 = ty0 - (sy0 + sh)
            F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (txr, 0), [], (2 * ((off + 12) / (off + L1)) - 1) if label else None, True if label else None))
        else:
            gy = RT[en] - g / 2 + dlevel; pts = [(ex, gy), (nx, gy)]; off = rh_off(s, sxr); L1 = gy - (sy0 + sh); tot = off + L1 + abs(nx - ex) + (ty0 - gy)
            F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (0.5, 0), pts, 2 * ((off + max(L1 / 2, 12)) / tot) - 1 if label else None, True if label else None))

def bypass(F, cells, eid, s, t, label="有", busx=None):
    """close() 後畫：inspect 菱形「本機有」→ 跳過 pull 直接到 t：s 右側出線 → 頁面右側匯流排（預設專案目錄欄左 10px）→ t 上方縫隙 → t 頂端。"""
    A = F.abs; busx = busx or F.cols[P][0] - 10
    sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tw / 2
    tot = (busx - (sx0 + sw)) + (gy - ey) + (busx - nx) + (ty0 - gy)
    cells.append(_edge(eid, s, t, label, (1, 0.5), (0.5, 0), [(busx, ey), (busx, gy), (nx, gy)], 2 * (14 / tot) - 1 if label else None, "below" if label else None))

def pullseg(b, row, ids, texts, nxt, w=(260, 200, 280), imgw=180):
    """啟動器 image 段（三格同中心直下，pull 失敗從左側出線）：row inspect 菱形；row+1 pull 白格 + GHCR 欄 image；nxt 放 row+2。
    契約④（v2.15-10）：inspect 本機已有 → 跳過 pull（bypass()）；只有 extract kind 才 create／cp。"""
    qi, pi, gi = ids; qt, pt, gt = texts
    b.box(qi, L, row, v2(D12), qt, w[0]); b.box(pi, L, row + 1, v2(W12), pt, w[1]); b.box(gi, G, row + 1, IMG, gt, imgw)
    b.box(nxt[0], L, row + 2, nxt[1], nxt[2], w[2])
    b.D(f"{qi}_n", qi, pi, "無", al=True); b.H(f"{gi}_p", gi, pi, "拉" if "vendor_kit" in gt else "拉 /dist"); b.D(f"{pi}_x", pi, nxt[0], al=True)

def sidebus(F, cells, eid, s, t, label="", busx=0, side="l", tx=0.5, pos=-0.7, vert="left"):
    """close() 後畫：s 側邊出線 → x=busx 匯流排往下 → t 上方縫隙 → t 頂端 tx 處（菱形用 0.5 = 頂點）。跳過中間幾列的分支線。"""
    A = F.abs; sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw

==================== 附件 K：review_v2_README.md（lint 規則）====================
# 三階段 draw.io 審查工具鏈（review v2）

目的：把「機械可查」的東西先用腳本跑掉（抽取、lint、縮圖），代理只做需要判斷的部分
（內容與連接、排版、一格一事），最後每條逐一驗證。輸入只讀，不寫回 `.drawio`／PNG。

檔案（都在本 scratchpad）：

| 檔 | 作用 |
|---|---|
| `extract_pages.py <drawio> <outdir> [page_id …]` | 每頁 → `<outdir>/<id>.json` + `<id>.md`；另寫 `pages.json`（頁序＋頁名） |
| `lint_pages.py <outdir>` | 讀上面的 JSON → `<outdir>/lint.md`（依頁分組）+ `lint.json` |
| `shrink_png.py <pngdir> <outdir> [scale] [page_id …]` | PIL 縮圖（預設 50%，白底）→ `<outdir>/*.png` + `pngs.json` |
| `/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/diagram-review-v2.js` | workflow（不跑 shell，只吃上面三個的產物） |

## 主對話要先跑的三個指令

```sh
cd <scratchpad>
python3 extract_pages.py v2_only.drawio review_v2_out          # 1. 抽取（47 頁 → review_v2_out/<id>.json|md, pages.json）
python3 lint_pages.py    review_v2_out                          # 2. lint（→ review_v2_out/lint.md, lint.json）
python3 shrink_png.py    png_v2 review_v2_png                   # 3. 縮圖（→ review_v2_png/*.png, pngs.json）
```

只審部分頁：三個指令都可在最後加頁 id（`extract_pages.py v2_only.drawio out v1p5c v1p5cc`）；
lint 的跨頁名詞比對只會比有抽出的頁。

## workflow args 範例

```json
{
  "extracted": "<scratchpad>/review_v2_out",
  "lint":      "<scratchpad>/review_v2_out/lint.md",
  "pngs":      [ {"page": "v1p5c", "path": ".../review_v2_png/v1p5c.png"}, ... ],
  "notes":     "<scratchpad>/decisions/proposal_v2.md",
  "changes":   "第十一輪：…",
  "focus":     "E(c) 兩頁的續跑入口",
  "pages":     ["v1p7bcc", "v1p7bccc"],
  "lint_items": [ ...lint.json 的內容（可選）... ]
}
```

- `pngs`：直接貼 `review_v2_png/pngs.json` 的內容（`page` = 頁 id，與 `<id>.md` 同名）。
- `pages`：可選白名單（頁 id）；不給就審 `pngs` 裡所有頁。
- `lint_items`：可選，貼 `lint.json` 內容；有給，結果的 `lint_mechanical` 直接列 warn 級條目（不經代理）；沒給就只留 lint.md 路徑。

流程：
1. 抽取（無 shell）：分組。內容與連接 = 4 組；排版 = 每 10 頁一個代理（47 頁 → 5 個）；一格一事 = 1 個代理。
2. 三種找問題的代理平行，各自找到的 findings **立刻**進驗證（pipeline，無 barrier）；驗證代理 effort low，對照 `<id>.md`／縮圖。
3. 回傳 `{ verdicts, confirmed(byPage), must_fix_count, rejected, lint_mechanical }`。findings 的 `page` 一律是頁 id。

## extract_pages.py 的判定規則（摸索結果）

- 一頁 = `<diagram id=… name=…>`；cell 用 regex 掃 `<mxCell id=… >`，未壓縮 XML。
- 文字：XML 解跳脫一次 → HTML；`<br>`／`<div>`→`⏎`；去標籤；再解一次實體（所以 `&amp;lt;repo&amp;gt;` 會變回 `<repo>`，
  不像 `pagetext.py` 那樣把 `<repo>` 當標籤吃掉）。
- `kind`（依 disc_v1_b.py／gen57.py 的樣式常數）：
  - 菱形 → `decision`（D12）
  - 橢圓：`#d5e8d4` → `end_ok`（G12；**綠橢圓同時是起點**，lint 懸空規則只在「無進邊也無出邊」才報）、`#f8cecc` → `end_red`（R12）、
    `#ffe6cc` → `end_orange`（O12）、白底 `dashed=1` → `entry`（ENTRY）
  - 長方形：`#dae8fc`/`#6c8ebf` → `step`（SUB 藍）、白底 `light-dark(…)` 邊 → `step`（W12）；同邊但 `dashed=1` → `file`（F12；粗體 = FGRP 檔案容器）；
    `#666666` 邊 → `file`（PRE 逐字框）；`#ffe6cc`/`#d79b00` → `rule`（RULE）；白底 `#b85450` 粗邊 → `rule`（INV）；
    `#e6e6e6` → `header`（HDR）；`#e1d5e7` → `other`/IMG（紫 image）
  - `shape=note` → `note`（`#fff2cc` = PEND 黃便條）
  - id 形如 `<prefix>_tk<i>`／`_tv<i>` → `term`（名詞／說明；`_th` = 「本頁名詞」表頭）
  - id 含 `_lg<n>`／`_lgt`／`_lgx_` → 圖例（`legend=true`，`cls=LEGEND`）；swimlane → BAND；`text` → TEXT／TITLE；其餘白底 `#999999` 邊 → CELL（表格格）
  - `#00b050` 小綠標「v2」不列入 nodes，改記在本體 `v2=true`
- `terms`：`_tk<i>` 與 `_tv<i>` 依 prefix＋序號配對（47 頁全部都是這個形式，表頭 `_th`）。
- `xrefs`：regex `(來自|續|見|回|→)?「X」頁`，node 文字與線標籤都掃。
- `edges[].fontSize`：style 的 fontSize 字串（沒有 = null）；lint `edge-font` 用。
- `fills`／`legend_fills`：非圖例格 vs 圖例格的 fillColor 集合（lint 的 color 規則用）。

## lint_pages.py 規則與可調參數

檔頭 docstring 列了全部規則的代號（v1 的 9 條＋v2 的 12 條；v1 原檔備份在 `lint_pages.py.v1`）；可調參數在檔案頂端：`FLOW_PAGE_RE`（哪些頁算流程頁，懸空規則只查這些）、
`KEYWORDS`（名詞覆蓋的關鍵字 regex）、`BASE_ALLOW`（不算 base 實例的片語）、`COLOR_WHITELIST`、`ONETHING_TOKENS`／`ONETHING_MIN`、`NEEDS_HUMAN`。
v2 規則每條可在 `ENABLED` 字典關閉，門檻／關鍵字都是頂端常數。

### v2 新增規則（全部 warn；目標 = 把反覆發生的圖面問題機械化擋掉）

| 規則 | 條件 | 訊息／備註 | 可調常數 |
|---|---|---|---|
| `event-name` | node／edge 文字出現 `launcher_started|launcher_completed|launcher_failed|engine_started|engine_completed|engine_failed|_started\b|_completed\b` | 事件名須用 spec 註冊表：launcher_start/exit、engine_start/exit | `EVENT_NAME_RE` |
| `resolve-3way` | 流程頁上文字「docker run … resolve」（中間無括號；排除 apply 格的「（含 vk-resolve）」）的 step，沿出邊走 ≤ 3 步須同時有 (A) decision 含「回 0／結束碼 0／非 0」與 (B) **另一個** decision／step 含「6-30」或「文法」。步數只算啟動器白 step（藍 SUB、菱形、file、note 不計）；走到「續「X」頁」出口會接到 X 頁的「來自」入口續走（跨頁） | resolve 結果須三叉：非 0 原碼傳出／文法不合 6-30／合法；A 與 B 合在同一格（「回 0 且文法合法？」）也報「缺文法格」 | `RESOLVE_3WAY_DEPTH`、`RESOLVE_3WAY_CROSS_PAGE`、`RESOLVE_STEP_RE`、`RESOLVE_EXIT_RE`、`RESOLVE_GRAMMAR_RE` |
| `precheck-recover` | 頁名含 install|add|remove|upgrade|dev|undev|uninstall|升引擎 的第一頁（頁名含「（1）」或不含全形括號；且頁上有起點綠橢圓、沒有「來自「X」頁」入口）須有 decision 文字含「未完成」「既有進度檔」「恢復」；頁名含 sync|update 的第一頁須有節點文字含「6-33」；prune 頁只要有「只列出」 | 缺 → warn（頁級，id `-`） | `PRECHECK_VERB_RE`、`PRECHECK_SYNC_RE`、`PRECHECK_DECISION_RE`、`PRECHECK_FIRST_RE`、`PRECHECK_SKIP_RE`（預設 None） |
| `end-color-text` | end 節點：文字含「→ 0」或以「0：」開頭 → 須 end_ok；含 `6-24|6-31|6-38|6-30|寫不進|拉不到|寫入失敗|失敗（任一步）` → 須 end_red；含 `請|先 |手動|重跑|→ 3|6-4|6-33` 且無紅關鍵字 → 須 end_orange | 「終點文字應為 X 但是 Y」（舊 `endcolor` 保留不動） | `END_OK_RE`、`END_RED_RE`、`END_ORANGE_RE` |
| `xref-forward` | xrefs 指到的頁序號（頁名前綴數字；沒有前綴就用 pages.json 順序）大於本頁序號。「續「X」頁」出口不算；「來自」「見」「回」、裸「X」頁都算；引用命中多頁時取最小序號 | 前引：頁 N 只能引用序號更小的頁 | — |
| `write-line` | 流程頁 step 文字（去掉「是：」「否 →」等分支前綴）以 寫|建|刪|原子替換|append 開頭或含「→ 檔」，頁內有 file 節點，但該 step 沒有出邊指到 file 節點 | 寫入格缺到檔案框的線 | `WRITE_LINE_EXEMPT`（動詞後緊接：印、印出、印記、執行紀錄、launcher_、engine_、sync_fast_path；「寫印記」仍算 = `WRITE_LINE_FORCE`）、`WRITE_LINE_EXEMPT_ANY`（含「到暫存」「暫存副本」= 寫暫存不算）、`WRITE_PAGE_RE` |
| `write-fail-edge` | 同上寫入 step：沒有出邊到 end_red／end_orange、沒有出邊 label 含「失敗」、頁內也沒有 node／edge 文字含「任一步」「失敗匯流」 | 寫入格缺失敗出邊或失敗匯流 | `WRITE_FAIL_PAGE_RE` |
| `term-count` | 名詞表條數 > 8 | 頁級 | `TERM_MAX` |
| `term-dup-page0` | 名詞 name（去結尾括號）已在第 0 頁出現（第 0 頁 = `PAGE0_IDS` 的 terms ＋ 表格每列第一格 `_r<i>c0`） | 「第 0 頁已有，不必重列」 | `PAGE0_IDS`、`PAGE0_CELL_RE` |
| `page-height` | max(y+h) > 2400 | 列最低的格 | `PAGE_MAX_H` |
| `edge-font` | edge style 有 fontSize 且 ≠ 12（extract_pages.py 現在會把 edge 的 `fontSize` 寫進 JSON；舊 JSON 沒有此欄就略過） | — | `EDGE_FONT` |
| `merge-fanout` | step 出邊 ≥ 3 且 targets 全是 end_* | 終點扇出：分支來源不可辨 | `MERGE_FANOUT_MIN` |

已知會報但要人判斷的：`xref-forward` 的「見」前引（bootstrap 頁見 install 頁、add（1）見 add（2）、B 頁見 C 逐檔判斷）——規則刻意嚴格；
`precheck-recover` 對「upgrade ── D. 回退」（git revert 起點、沒有前置檢查）；`end-color-text` 對狀態機頁的綠格「prune 特例…印 6-33 → 繼續」（關鍵字命中但語意是繼續）；
`write-fail-edge` 對 release 頁（v1p15c，CI 寫 .digest／SHA256SUMS／GitHub Release，沒畫失敗邊）。

- 等級：`warn` = 機械上幾乎確定；`info` = 候選／提示（一格一事候選全是 info，交第 3 階段代理）。
- xref：頁名包含引用 → 過；否則拆 token（英數字串／CJK 連續字）全部包含 → `info`「只靠拆字比對到」；
  「install（1）（2）」「E(a)(b)」這種多括號引用會展開成多個各自比對。
- termcov：關鍵字在名詞 name 或說明文出現就算覆蓋；只在說明文出現的彙總成每頁一行 info；都沒有 → warn。
- term-diff：放在 lint.md 最後「跨頁」段（列各版本出現的頁與前三處差異）。
- lint.md 頁序 = 文件內頁序（pages.json）；規則表會列出 v1 9 條＋v2 12 條的 warn／info 數。

## 已知限制

- 懸空規則只看「kind」：白底結果框（例如 prune 頁「列出帶 label 的四類資源」）會被當 step 報「無出邊」；狀態機頁旁邊的說明框也會。這些交代理判定。
- base 規則只排除 `BASE_ALLOW` 的片語；「log.sh 由 base 移植」這類敘述會被列出（是否算實例由代理／使用者決定）。
- 縮圖 50% 後一頁約 1600×2300、0.9 MB；排版代理一次看 10 頁。


codex
我會使用 `implement` 技能，依附件 R/F/L 逐頁修改 `disc_v1_b.py` 的 P5 之後內容；先讀技能規範並跑基線生成，之後只碰允許的檔案，最後依指定工具鏈全量驗證。
exec
/usr/bin/bash -lc "sed -n '1,240p' /home/cyc/.agents/skills/implement/SKILL.md && python3 run_v1_b.py" in <scratchpad>
 succeeded in 113ms:
v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 page ('1660', '1919')
v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 page ('1660', '1311')
v1p5i 流程 v2：bootstrap.sh（1′）docker run install page ('1660', '1364')
v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add page ('1660', '1991')
v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run page ('1660', '1586')
v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 page ('1660', '1734')
v1p5cw 流程 v2：install（1″）寫入 page ('1660', '1707')
v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore page ('1660', '2006')
v1p5b 流程 v2：add（1）resolve → docker page ('1660', '2273')
v1p5bcc 流程 v2：add（1′）apply 前置 page ('1660', '2219')
v1p5bc 流程 v2：add（2）apply 寫入段 page ('1660', '2257')
v1p6 流程 v2：sync（1）啟動器快路徑 page ('1660', '2229')
v1p6cc 流程 v2：sync（1′）引擎 resolve page ('1660', '2269')
v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置 page ('1660', '1706')
v1p6cw 流程 v2：sync（2′）apply 寫入段 page ('1660', '1581')
v1p7 流程 v2：upgrade ── A. Renovate 路徑 page ('1660', '1821')
v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker page ('1660', '2363')
v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 page ('1660', '2227')
v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 page ('1660', '2394')
v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 page ('1660', '1569')
v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 page ('1660', '2371')
v1p7bd 流程 v2：upgrade ── D. 回退 page ('1660', '2142')
v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b) page ('1660', '2140')
v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 page ('1660', '1673')
v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） page ('1660', '2340')
v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） page ('1660', '1378')
v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） page ('1660', '1559')
v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml page ('1660', '2181')
v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） page ('1660', '1241')
v1p8 流程 v2：dev <repo> page ('1660', '2094')
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2296')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2071')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2385')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')

codex
基線可正常生成 38 頁，尺寸目前都在限制內。接下來我先建立精確的 lint／幾何基線，再按元件 id 定位修改；這份腳本頁面密度很高，我會優先落實所有可安全修改項，幾何上確實無法兼容者才依規則加「待處理問題」。
exec
/usr/bin/bash -lc "python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out && sed -n '1,260p' r15_b_out/lint.md && rg -n \""'^(# ================= P5|.*'"\\b(ipr|i1g|ie4ax|cpr|n1i|z0q|a4b0|s12z0|s13gaq|m10m|w2s|ue11|i7|i11|ign|idl)\\b)\" disc_v1_b.py" in <scratchpad>
 succeeded in 295ms:
v1p5       nodes=  61 edges= 25 terms= 6 xrefs= 3  流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
v1p5x      nodes=  48 edges= 13 terms= 6 xrefs= 5  流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
v1p5i      nodes=  54 edges= 11 terms= 5 xrefs= 7  流程 v2：bootstrap.sh（1′）docker run install
v1p5ccc    nodes=  62 edges= 23 terms= 7 xrefs= 7  流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
v1p5c      nodes=  55 edges= 21 terms= 5 xrefs= 2  流程 v2：install（1）主機檢查 → 引擎 image → docker run
v1p5cm     nodes=  52 edges= 25 terms= 5 xrefs= 4  流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
v1p5cw     nodes=  60 edges= 28 terms= 5 xrefs= 4  流程 v2：install（1″）寫入
v1p5cc     nodes=  67 edges= 37 terms= 7 xrefs= 2  流程 v2：install（2）根 justfile 與 .dockerignore
v1p5b      nodes=  90 edges= 36 terms= 8 xrefs= 2  流程 v2：add（1）resolve → docker
v1p5bcc    nodes=  70 edges= 27 terms= 8 xrefs= 4  流程 v2：add（1′）apply 前置
v1p5bc     nodes=  83 edges= 53 terms= 8 xrefs= 2  流程 v2：add（2）apply 寫入段
v1p6       nodes=  69 edges= 23 terms= 8 xrefs= 2  流程 v2：sync（1）啟動器快路徑
v1p6cc     nodes=  71 edges= 36 terms= 7 xrefs= 4  流程 v2：sync（1′）引擎 resolve
v1p6c      nodes=  59 edges= 21 terms= 8 xrefs= 4  流程 v2：sync（2）三叉 → docker → apply 前置
v1p6cw     nodes=  51 edges= 24 terms= 4 xrefs= 2  流程 v2：sync（2′）apply 寫入段
v1p7       nodes=  61 edges= 23 terms= 6 xrefs= 2  流程 v2：upgrade ── A. Renovate 路徑
v1p7c      nodes=  64 edges= 32 terms= 5 xrefs= 3  流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
v1p7ccc    nodes=  68 edges= 28 terms= 8 xrefs= 7  流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
v1p7cc     nodes=  74 edges= 44 terms= 6 xrefs= 8  流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
v1p7cccc   nodes=  59 edges= 26 terms= 6 xrefs= 2  流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
v1p7b      nodes=  70 edges= 41 terms= 6 xrefs= 9  流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
v1p7bd     nodes=  74 edges= 33 terms= 7 xrefs= 3  流程 v2：upgrade ── D. 回退
v1p7bc     nodes=  62 edges= 28 terms= 6 xrefs= 5  流程 v2：upgrade ── E. 升引擎 (a)(b)
v1p7bca    nodes=  56 edges= 20 terms= 6 xrefs= 4  流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
v1p7bcc    nodes=  68 edges= 34 terms= 7 xrefs= 3  流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
v1p7bcx    nodes=  45 edges= 13 terms= 4 xrefs= 4  流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
v1p7bccc   nodes=  51 edges= 16 terms= 4 xrefs= 8  流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
v1p7bcce   nodes=  65 edges= 30 terms= 6 xrefs= 7  流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
v1p7bccd   nodes=  51 edges= 17 terms= 6 xrefs= 3  流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
v1p8       nodes=  70 edges= 35 terms= 7 xrefs= 0  流程 v2：dev <repo>
v1p8ccc    nodes=  65 edges= 29 terms= 7 xrefs= 1  流程 v2：dev vendor_kit
v1p8c      nodes=  71 edges= 33 terms= 8 xrefs= 2  流程 v2：undev <repo>（1）resolve → apply 前置
v1p8cx     nodes=  51 edges= 25 terms= 4 xrefs= 2  流程 v2：undev <repo>（2）寫入段
v1p8cc     nodes=  76 edges= 40 terms= 8 xrefs= 2  流程 v2：undev vendor_kit
v1p8b      nodes=  73 edges= 34 terms= 8 xrefs= 2  流程 v2：remove（1）resolve → apply 前置
v1p8bccc   nodes=  71 edges= 43 terms= 7 xrefs= 2  流程 v2：remove（2）寫入段
v1p8bc     nodes=  69 edges= 35 terms= 5 xrefs= 3  流程 v2：uninstall（1）resolve → apply 前置
v1p8bcc    nodes=  91 edges= 51 terms= 7 xrefs= 3  流程 v2：uninstall（2）寫入段
共 38 頁 → r15_b_out/
頁數 38；條目 346（warn 127、info 219）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 36 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 120 | 37 |
| onething | 0 | 90 |
| event-name | 0 | 0 |
→ r15_b_out/lint.md, lint.json
# lint.md

頁數 38；條目 346（warn 127、info 219）

| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 36 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 120 | 37 |
| onething | 0 | 90 |
| event-name | 0 | 0 |
| resolve-3way | 0 | 0 |
| precheck-recover | 0 | 0 |
| end-color-text | 0 | 0 |
| xref-forward | 3 | 0 |
| write-line | 0 | 0 |
| write-fail-edge | 4 | 0 |
| term-count | 0 | 0 |
| term-dup-page0 | 0 | 0 |
| page-height | 0 | 0 |
| edge-font | 0 | 0 |
| merge-fanout | 0 | 0 |

## v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
nodes 61／edges 25／terms 6；warn 2、info 1
- [termcov][warn] a0l0: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a0l: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 1 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml

## v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
nodes 48／edges 13／terms 6；warn 0、info 3
- [decision][info] ae6p: 菱形 a6q 出邊標籤不以是／否開頭：「無」
- [decision][info] ae6y: 菱形 a6q 出邊標籤不以是／否開頭：「有」
- [termcov][info] -: 1 個關鍵字只在名詞說明文出現、沒有獨立條（略）：薄殼

## v1p5i 流程 v2：bootstrap.sh（1′）docker run install
nodes 54／edges 11／terms 5；warn 9、info 4
- [termcov][warn] a9f_1: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9f_2: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9f_3: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9f_4: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9f_6: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9h: 「6-4」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：薄殼、--local、log/
- [onething][info] a9x3: [end_orange] 分隔詞 2（、1 ；1）：「3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）」
- [onething][info] a9c: [step] 分隔詞 3（；3）：「否（回 1）：依 .tmp.install 進度檔清半成品（引擎寫入失敗時已自清；引擎異常結束由 bootstrap.sh 補清；log/ 保留；印「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」）」
- [onething][info] a9hx: [end_orange] 分隔詞 2（→1 再1）：「1：install 需人處理 → 依指令處理後再跑 bootstrap.sh」
- [xref-forward][warn] bA1: 前引：頁 3 只能引用序號更小的頁，卻見「install（1）」頁（序號 5）
- [xref-forward][warn] a9e: 前引：頁 3 只能引用序號更小的頁，卻見「install（1）」頁（序號 5）
- [xref-forward][warn] a9f: 前引：頁 3 只能引用序號更小的頁，卻見「install（1）」頁（序號 5）

## v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
nodes 62／edges 23／terms 7；warn 7、info 4
- [termcov][warn] a9e2: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9e2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a9e2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a10f_1: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a10f_2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a10f_4: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] a10f_5: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 1 個關鍵字只在名詞說明文出現、沒有獨立條（略）：apply
- [onething][info] a10d: [step] 分隔詞 2（→2）：「是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）」
- [onething][info] a10ae: [step] 分隔詞 3（、2 ；1）：「apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）」
- [onething][info] a12: [end_orange] 分隔詞 8（→3 、2 ；3）：「中止：結束碼 = 該段的碼原樣傳出（install／add 回 3 → 3、回 2 → 2、其餘非 0 → 1）；印該段錯誤；列出已完成／未處理的 -t（已完成的 add 保留）；後續 -t 不執行」

## v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run
nodes 55／edges 21／terms 5；warn 4、info 3
- [decision][info] i1i_n: 菱形 i1i 出邊標籤不以是／否開頭：「無」
- [decision][info] ie1y: 菱形 i1i 出邊標籤不以是／否開頭：「有」
- [termcov][warn] bI: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i0l0: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i0l: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] ipq: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml、6-24、6-31

## v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
nodes 52／edges 25／terms 5；warn 5、info 5
- [termcov][warn] i4qn: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i4: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i4: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i4: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] i4z: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：.tmp.install、log/、baseline/
- [onething][info] i4: [step] 分隔詞 5（、4 ；1）：「產 .gitignore 到暫存（自描述首行；排除 cache/、gen/、log/、version.local.toml、.tmp.*）」
- [onething][info] i4_3b: [step] 分隔詞 2（；2）：「產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器事件白名單）」
- [onething][info] i4_5: [step] 分隔詞 2（、2）：「否：產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30）」
- [onething][info] i4tx: [end_red] 分隔詞 2（→1 ；1）：「1：進度檔或暫存寫入失敗（任一步，共通匯流）→ 第一次：依進度檔清半成品；修復型：列已完成／未完成」

## v1p5cw 流程 v2：install（1″）寫入
nodes 60／edges 28／terms 5；warn 0、info 2
- [endcolor][info] i4wx2: 紅終點文字含需人動作字眼（候選改橙）：「1：列已完成／未完成，下次可寫動詞先恢復（進度檔保留）」
- [termcov][info] -: 4 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml、metadata、薄殼、log/

## v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore
nodes 67／edges 37／terms 7；warn 7、info 5
- [decision][info] ie10: 菱形 i6 出邊標籤不以是／否開頭：「無」
- [decision][info] ie12: 菱形 i6 出邊標籤不以是／否開頭：「有」
- [decision][info] ie20: 菱形 ig 出邊標籤不以是／否開頭：「無」
- [decision][info] ie21: 菱形 ig 出邊標籤不以是／否開頭：「有」
- [termcov][warn] igyf: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] igyf: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] igyf: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：薄殼、baseline/、.tmp.install
- [write-fail-edge][warn] i7: 寫入格缺失敗出邊或失敗匯流：「無：建 justfile（四行，逐字見右）、印建了什麼」
- [write-fail-edge][warn] i11: 寫入格缺失敗出邊或失敗匯流：「是：append 那一行（import）、印加了什麼」
- [write-fail-edge][warn] ign: 寫入格缺失敗出邊或失敗匯流：「無：建 .dockerignore（四行，逐字同右）、印建了什麼」
- [write-fail-edge][warn] idl: 寫入格缺失敗出邊或失敗匯流：「刪進度檔 .tmp.install.<id>.toml（最後一步）」

## v1p5b 流程 v2：add（1）resolve → docker
nodes 90／edges 36／terms 8；warn 6、info 5
- [termcov][warn] c0l0: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] cf0_3: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] cf0_4: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] cf0_6: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] cf1_1: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] cf1_5: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 7 個關鍵字只在名詞說明文出現、沒有獨立條（略）：metadata、6-24、version.toml、apply、gen/.stamp、version.local.toml、gen/
- [onething][info] c2a: [step] 分隔詞 2（、1 ；1）：「resolve（不寫任何檔）：讀 version.toml；--local 時收啟動器交來的 index digest、image ID」
- [onething][info] c2c: [step] 分隔詞 3（、1 ；2）：「否：算執行計畫（extract <repo>|<ref>；apply|yes；詢問清單留在引擎、apply 重算）」
- [onething][info] c2d: [step] 分隔詞 8（、8）：「產生輸入指紋（version.toml、version.local.toml、各 metadata、納管 dest、gen/.stamp 與各印記第一行、.tmp.* 清單、鎖定 digest、image ID、正規化 argv）」
- [onething][info] c2d2: [step] 分隔詞 2（、2）：「stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋（只傳協定內容）」

## v1p5bcc 流程 v2：add（1′）apply 前置
nodes 70／edges 27／terms 8；warn 1、info 6
- [decision][info] c9a_n: 菱形 c9a 出邊標籤不以是／否開頭：「無」
- [decision][info] ce12y: 菱形 c9a 出邊標籤不以是／否開頭：「有」
- [termcov][warn] c9g: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：apply、6-30、--local
- [onething][info] c9q0x: [end_orange] 分隔詞 2（→1 、1）：「1／2／3：resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）」
- [onething][info] c9b: [step] 分隔詞 2（→2）：「extract：docker create <image> /x → cp c:/dist/. <tmp>/<repo>/ → rm」
- [onething][info] c14x: [end_orange] 分隔詞 2（並1 ；1）：「1：印需改清單（CI 模式；請在本機執行後 commit 並 push）」

## v1p5bc 流程 v2：add（2）apply 寫入段
nodes 83／edges 53／terms 8；warn 4、info 6
- [decision][info] ce25: 菱形 c16 出邊標籤不以是／否開頭：「無」
- [decision][info] ce26: 菱形 c16 出邊標籤不以是／否開頭：「有」
- [termcov][warn] bB2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] c15af: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] c15b: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] c21b2: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 7 個關鍵字只在名詞說明文出現、沒有獨立條（略）：metadata、apply、cache/、gen/、6-11、6-21、gen/tools.just
- [onething][info] c15a: [step] 分隔詞 5（、4 ；1）：「建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）」
- [onething][info] c20w: [step] 分隔詞 2（→1 ；1）：「否：初始檔逐檔原子替換（暫存 → 正式位置；只有要建／要 append 的檔）」
- [onething][info] c23x: [end_red] 分隔詞 3（→1 、1 ；1）：「1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留」

## v1p6 流程 v2：sync（1）啟動器快路徑
nodes 69／edges 23／terms 8；warn 2、info 3
- [decision][info] ne5p: 菱形 n1i 出邊標籤不以是／否開頭：「無」
- [decision][info] ne5v: 菱形 n1i 出邊標籤不以是／否開頭：「有」
- [termcov][warn] n0l0: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] n0l: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 11 個關鍵字只在名詞說明文出現、沒有獨立條（略）：gen/.stamp、resolve、metadata、version.local.toml、version.toml、薄殼、gen/tools.just、cache/、digest、6-24、6-31

## v1p6cc 流程 v2：sync（1′）引擎 resolve
nodes 71／edges 36／terms 7；warn 1、info 5
- [termcov][warn] nf: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 6 個關鍵字只在名詞說明文出現、沒有獨立條（略）：resolve、version.toml、metadata、cache/、gen/.stamp、gen/tools.just
- [onething][info] n1be: [step] 分隔詞 2（、2）：「resolve sync（不寫任何檔）：讀 version.toml、各 metadata、印記」
- [onething][info] z0: [step] 分隔詞 3（再1 、2）：「彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）」
- [onething][info] z1: [step] 分隔詞 2（、2）：「產生輸入指紋（version.toml、metadata、印記 hash…）」
- [onething][info] z1b: [step] 分隔詞 2（、2）：「stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）」

## v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置
nodes 59／edges 21／terms 8；warn 1、info 4
- [decision][info] m0a_n: 菱形 m0a 出邊標籤不以是／否開頭：「無」
- [decision][info] me0y: 菱形 m0a 出邊標籤不以是／否開頭：「有」
- [termcov][warn] m0g: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [onething][info] m0q0x: [end_orange] 分隔詞 2（→1 、1）：「1／2／3：resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）」
- [onething][info] m0b: [step] 分隔詞 2（→2）：「extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm」

## v1p6cw 流程 v2：sync（2′）apply 寫入段
nodes 51／edges 24／terms 4；warn 0、info 2
- [termcov][info] -: 4 個關鍵字只在名詞說明文出現、沒有獨立條（略）：cache/、digest、gen/tools.just、gen/.stamp
- [onething][info] m7x: [end_red] 分隔詞 3（→1 再1 ；1）：「1：取件／寫入失敗（任一步，共通匯流）→ 列出已完成；cache 可能部分更新，下次 sync 再取」

## v1p7 流程 v2：upgrade ── A. Renovate 路徑
nodes 61／edges 23／terms 6；warn 1、info 2
- [termcov][warn] a4q: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 2 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml、version.local.toml
- [onething][info] a5: [end_orange] 分隔詞 2（→2）：「1 → PR 紅：需人處理（常見：基準版落後 6-5 → 本機 upgrade <repo> -y 後 push）」

## v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
nodes 64／edges 32／terms 5；warn 5、info 6
- [xref][info] uB: 引用「B（1′）」頁只靠拆字比對到
- [xref][info] b8z: 引用「B（1′）」頁只靠拆字比對到
- [termcov][warn] uB: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b0l0: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] bpq: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b1e: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b4: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：Renovate、resolve、version.toml
- [onething][info] b1e: [step] 分隔詞 2（、2）：「resolve（不寫任何檔）：讀 version.toml、version.local.toml、metadata」
- [onething][info] b7zz: [end_ok] 分隔詞 2（→1 、1）：「0：目標 == 現鎖定版且無待合併 → 無事可做（apply|no，不起 apply、不重寫 cache／metadata）」
- [onething][info] b7s2: [step] 分隔詞 2（、2）：「stdout vk-resolve/1：extract 目標 tag@digest、apply|yes、指紋（只傳協定內容）」

## v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
nodes 68／edges 28／terms 8；warn 2、info 10
- [decision][info] b8a_n: 菱形 b8a 出邊標籤不以是／否開頭：「無」
- [decision][info] be11y: 菱形 b8a 出邊標籤不以是／否開頭：「有」
- [xref][info] uB1: 引用「B（1）」頁只靠拆字比對到
- [xref][info] uB1: 引用「B（2）」頁只靠拆字比對到
- [xref][info] b8e: 引用「B（1）」頁只靠拆字比對到
- [xref][info] b11z: 引用「B（2）」頁只靠拆字比對到
- [termcov][warn] hdr1: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b8g: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 3 個關鍵字只在名詞說明文出現、沒有獨立條（略）：apply、6-30、metadata
- [onething][info] b8q0x: [end_orange] 分隔詞 2（→1 、1）：「1／2／3：resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）」
- [onething][info] b8b: [step] 分隔詞 2（→2）：「extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm」
- [onething][info] b12x: [end_orange] 分隔詞 2（、1 ；1）：「1：印需改清單（CI 模式；本機執行後 commit、push）」

## v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
nodes 74／edges 44／terms 6；warn 7、info 8
- [xref][info] uB2: 引用「B（1′）」頁只靠拆字比對到
- [xref][info] uB2: 引用「B（2′）」頁只靠拆字比對到
- [xref][info] b10z: 引用「B（1′）」頁只靠拆字比對到
- [xref][info] b14n: 引用「B（2′）」頁只靠拆字比對到
- [xref][info] b14z: 引用「B（2′）」頁只靠拆字比對到
- [termcov][warn] hdr1: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b10ef: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b10fq: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b13ac: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b13b: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b13b: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b14z: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 2 個關鍵字只在名詞說明文出現、沒有獨立條（略）：apply、metadata
- [onething][info] b10e: [step] 分隔詞 5（、4 ；1）：「建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）」
- [onething][info] b14w: [step] 分隔詞 2（→1 ；1）：「通過的檔逐檔原子替換（暫存 → 正式位置；解析失敗的檔除外）」

## v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
nodes 59／edges 26／terms 6；warn 3、info 5
- [xref][info] uB3: 引用「B（2）」頁只靠拆字比對到
- [xref][info] b15z: 引用「B（2）」頁只靠拆字比對到
- [termcov][warn] uB3: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b15a: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] b16: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 4 個關鍵字只在名詞說明文出現、沒有獨立條（略）：Renovate、version.toml、apply、gen/tools.just
- [onething][info] b15d: [step] 分隔詞 3（→2 ；1）：「寫 metadata：每個 dest 的 state／declined_hash／lines —— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined」
- [onething][info] b18: [end_orange] 分隔詞 4（再1 、1 ；2）：「2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨」

## v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
nodes 70／edges 41／terms 6；warn 2、info 10
- [xref][info] uC: 引用「B（2）」頁只靠拆字比對到
- [xref][info] uC: 引用「B（2）」頁只靠拆字比對到
- [xref][info] c_in: 引用「B（2）」頁只靠拆字比對到
- [xref][info] c_ask: 引用「B（2）」頁只靠拆字比對到
- [xref][info] c_skip: 引用「B（2）」頁只靠拆字比對到
- [xref][info] p7b_tv1: 引用「B（2）」頁只靠拆字比對到
- [termcov][warn] c_in0: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] uC2: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 2 個關鍵字只在名詞說明文出現、沒有獨立條（略）：metadata、apply
- [onething][info] s_del: [step] 分隔詞 2（、2）：「是：維持刪除、不問、不重建」
- [onething][info] s_ap: [step] 分隔詞 2（、2）：「是：保留、warn、印新內容」
- [onething][info] cx2: [end_orange] 分隔詞 2（→1 再1）：「是 → 2：停，先解完標記再重跑（=「B. 手動路徑（1）」頁 (0) 的橙終點）」

## v1p7bd 流程 v2：upgrade ── D. 回退
645:# ================= P5：bootstrap.sh（1）=================
696:# ================= P5x：bootstrap.sh（1″）inspect → pull → LABEL =================
721:# ================= P5i：bootstrap.sh（1′）install =================
744:# ================= P5ccc：bootstrap.sh（2）=================
776:# ================= P5c：install（1）主機檢查 → 執行紀錄 → 引擎 image → 比對 → 進度檔 → 產薄殼到暫存 =================
797:preseg(b, "i", 5, "i1g", "install")
798:b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
805:b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
806:b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
812:# ================= P5cm：install（1′）比對薄殼 → 進度檔 → 產薄殼到暫存 =================
846:# ================= P5cw：install（1′）寫入 =================
883:# ================= P5cc：install（2）根 justfile 與 .dockerignore =================
896:b.box("i7", E, 5, SUB, fl("無：建 justfile（四行，逐字見右）、印建了什麼"), 120, ax="r")
899:b.box("i11", E, 6, SUB, fl("是：append 那一行（import）、印加了什麼"), 250, ax=SP)
902:b.box("ign", E, 8, v2(SUB), fl("無：建 .dockerignore（四行，逐字同右）、印建了什麼"), 120, ax="r")
912:b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
916:b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
919:b.D("ie17", "i12", "i11", "是", al=True); b.H("ie18", "i12", "i12p", "否"); b.LU("ie16f", "i11", "i11f", "寫", tx=0.5); b.D("ie19d", "i11", "ig", al=True)
920:b.H("ie7f", "i7", "i11f", "寫")
921:b.RD("ie20", "ig", "ign", "無"); b.D("ie21", "ig", "igs", "有", al=True)
922:b.H("ie20f", "ign", "igyf", "寫")
927:b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
928:b.D("ie25", "idl", "iz", "", 0.5, 0.5)
938:_ub("ie13", "i7", "ig", 0.5); _ub("ie20z", "ign", "idl", 0.95)
941:for _s in ("igsp", "igq0p", "igqp"): _lb(f"{_s}_l", _s, "idl", "", 0.1)
951:# ================= P5b：add（1）resolve =================
1025:# ================= P5bcc：add（1′）三叉 → docker → apply 前置 =================
1066:# ================= P5bc：add（2）apply 寫入段 =================
1163:b.box("n1i", L, 8, v2(D12), "否 → docker image inspect：本機有？", 180, ax=50)
1172:b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.LD("ne5q", "nq", "nqf", "是", busx=300, vert=True); b.H("ne5ql", "nqf", "nq0"); b.D("ne5n", "nq", "n1i", "否", 0.5, 0.5)
1173:b.RD("ne5p", "n1i", "n1p", "無", tx=0.5); b.H("ne5g", "n1g", "n1p", "拉"); b.D("ne5v", "n1i", "n1v", "有", al=True)
1217:b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
1231:b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
1336:b.box("a4b0", L, 3, v2(W12), fl("check.sh ⓪：git ls-files 拒絕被納管的 version.local.toml（納管 → 1 停）"), 220)
1356:b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
1813:b.box("s12z0", E, 0, ENTRY, "來自「E(c)（1）」頁（目標 = 現 ref）或「E(c)（1′）」頁（目標引擎接手）；已拿鎖，薄殼 == 上次產物；已寫 launcher_start", 360)
1827:b.D("se13", "s12z0", "s12e", "", 0.5, 0.5); b.H("se13z", "s12e", "s12z", "是")
1846:b.box("s13gaq", E, 4, v2(D12), fl("否 → 結果 ≠ 現況 → 問 6-22「config.toml 換成合併結果？」同意？（-y 免問）"), 300)
1856:b.D("se17gpq", "s13gy", "s13gpq", al=True); b.D("se17gaq", "s13gpq", "s13gaq", "否", al=True); b.D("se17aw", "s13gaq", "s13gw", "是", al=True)
1860:tty(F, p7bcg, "s13gaq")
1862:sidebus(F, p7bcg, "se17adn", "s13gaq", "s13gm", "否：不動（記 declined_hash）", busx=400, tx=0.15, pos=-0.6, vert="below")
2072:sidebus(F, p8cx, "ue11", "u6ce", "u6d", "是：留著", busx=565, tx=0.15, pos=-0.6, vert="below")
2088:b.box("w2s", E, 5, v2(SUB), fl("是：算計畫（撤 vendor_kit 行；無 image 要拉）＋ 指紋（含 version.local.toml hash）"), 400)
2109:b.H("we1", "w0", "w0l0"); b.D("we1l", "w0l", "wpq", al=True); b.H("we1e", "w1", "w1e"); b.D("we2", "w1e", "w2q", al=True); b.H("we2n", "w2q", "w3", "否"); b.D("we2y", "w2q", "w2s", "是", 0.5, 0.5); b.D("we2s2", "w2s", "w2s2")
2198:b.box("m10m", E, 11, v2(SUB), "刪 metadata .vendor_kit.toml 並移除已空的 baseline/<repo>/", 400)
2220:b.D("me15m", "m10k", "m10m"); b.H("me15mf", "m10m", "m10mf", "刪")
2221:b.D("me15b", "m10m", "m10b"); b.H("me15bf1", "m10b", "m10bf1", "刪"); b.D("me15b2", "m10b", "m10b2"); b.H("me15bf", "m10b2", "m10bf", "寫"); b.D("me15c", "m10b2", "m10c"); b.H("me15cf", "m10c", "m10cf", "刪")
2226:sidebus(F, p8b2, "me15qn", "m10q", "m10m", "否", busx=565, tx=0.15, pos=-0.6, vert="below")
2227:failbus(F, p8b2, ["m9l", "m9d", "m10a", "m10k", "m10m", "m10b", "m10b2", "m10c", "m10e", "m10g"], "m10x")

exec
/usr/bin/bash -lc "sed -n '640,1250p' disc_v1_b.py > /tmp/chunk1.txt; sed -n '1250,1900p' disc_v1_b.py > /tmp/chunk2.txt; sed -n '1900,2300p' disc_v1_b.py > /tmp/chunk3.txt; git status --short; rg -n \"def preseg|def failbus|def lstart|p5i|addpage\\(\" disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
fatal: not a git repository (or any of the parent directories): .git
4:第十二輪（review_v2r11_findings.md 必修＋選修）：頁尾統一為「log_prune」→「launcher_exit」兩格 + 終點列（footer()/footer_edges()：所有終點的唯一前驅是 launcher_exit 格；各分支從左側匯流排 x=30 匯入，成功路徑直下）；每個 docker run 之後緊接 engine_start（EST_R／EST_A／EST_1）；啟動器 image 段統一 pullseg()（inspect／pull／image 同中心直下，本機有 → 頁面右側 bypass()，pull 失敗紅出口）；拆頁：bootstrap.sh（1′）v1p5i、install（1′）v1p5cw、D. 回退 v1p7bd、E(c)（1′）v1p7bcx；sync(1) 的 docker run 移到 sync(1′) 頁首；E(a) 的 (b) 段改成引用 sync(1)；C′ 出口改文字；內容：bootstrap 先驗 git／just 才建 log；install 的 git／巢狀檢查移到主機側；add 已接入且完成先於查 registry、--local 拆格；B(1) 6-3 橙出口；E(a) 新引擎 pull 移到 apply 前；E(c)(2) 建日誌＋config.toml 拆三格；remove(2) 逐行比對迴圈；undev u6x 措辭；名詞表逐頁裁剪（頁高 ≤ 2400）。備份：.v13（第十二輪前）。
412:def addpage(pid, name, cells): pages_v1_b.append((pid, TR(name), cells))
575:def lstart(b, cid, xid, row, verb, w=220, col=L, xcol=G, xw=200, pre=""):
583:def preseg(b, pid, row, nxt, verb, ro=False, col=L, w=240, rcol=E, xcol=G, nxt_tx=0.9):
608:def failbus(F, cells, srcs, end, busx=1610, sy=0.85, stub=16, label="失敗", tx=0.5):
694:addpage("v1p5", "流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別", p5)
719:addpage("v1p5x", "流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版", p5x)
722:p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
741:foot(p5i, "p5i", F.y, _t5("release／tar", "--local", "docker image inspect", "6-37", "GHCR") + [("install 進度檔 .tmp.install", ".tmp.install.<id>.toml：第一次 install 也建（第一個寫入前）= 「不留半成品」的清除清單；引擎寫入失敗時依它自清；引擎異常結束（未自清）由 bootstrap.sh 依它補清；log/ 一律保留"), ("bootstrap.sh 結束碼", "= 失敗那一步的碼原樣傳出：install／add 回 3 → 3、回 2 → 2、其餘非 0 → 1；任一 -t 的 add 失敗 → 立即中止、不處理後續 -t、已完成的 add 保留；全部成功 → 0")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
742:addpage("v1p5i", "流程 v2：bootstrap.sh（1′）docker run install", p5i)
774:addpage("v1p5ccc", "流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add", p5d)
810:addpage("v1p5c", "流程 v2：install（1）主機檢查 → 引擎 image → docker run", p5c)
843:addpage("v1p5cm", "流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存", p5cm)
881:addpage("v1p5cw", "流程 v2：install（1″）寫入", p5cw)
949:addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
1023:addpage("v1p5b", "流程 v2：add（1）resolve → docker", p5b)
1064:addpage("v1p5bcc", "流程 v2：add（1′）apply 前置", p5bp)
1124:addpage("v1p5bc", "流程 v2：add（2）apply 寫入段", p5bc)
1179:addpage("v1p6", "流程 v2：sync（1）啟動器快路徑", p6)
1237:addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
1267:addpage("v1p6c", "流程 v2：sync（2）三叉 → docker → apply 前置", p6c)
1303:addpage("v1p6cw", "流程 v2：sync（2′）apply 寫入段", p6cw)
1363:addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
1406:addpage("v1p7c", "流程 v2：upgrade ── B. 手動路徑（1）resolve → docker", p7c)
1444:addpage("v1p7ccc", "流程 v2：upgrade ── B. 手動路徑（1′）apply 前置", p7cp)
1501:addpage("v1p7cc", "流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併", p7cc)
1537:addpage("v1p7cccc", "流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入", p7cq)
1613:addpage("v1p7b", "流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入", p7b)
1655:addpage("v1p7bd", "流程 v2：upgrade ── D. 回退", p7bd)
1704:addpage("v1p7bc", "流程 v2：upgrade ── E. 升引擎 (a)(b)", p7bc)
1736:addpage("v1p7bca", "流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手", p7bca)
1786:addpage("v1p7bcc", "流程 v2：upgrade ── E(c) upgrade vendor_kit（1）", p7bcc)
1808:addpage("v1p7bcx", "流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）", p7bcx)
1836:addpage("v1p7bccc", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2）", p7bcd)
1885:addpage("v1p7bcce", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml", p7bcg)
1913:addpage("v1p7bccd", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）", p7bce)
1971:addpage("v1p8", "流程 v2：dev <repo>", p8)
2007:addpage("v1p8ccc", "流程 v2：dev vendor_kit", p8v)
2043:addpage("v1p8c", "流程 v2：undev <repo>（1）resolve → apply 前置", p8c)
2076:addpage("v1p8cx", "流程 v2：undev <repo>（2）寫入段", p8cx)
2122:addpage("v1p8cc", "流程 v2：undev vendor_kit", p8cc)
2176:addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
2230:addpage("v1p8bccc", "流程 v2：remove（2）寫入段", p8b2)
2271:addpage("v1p8bc", "流程 v2：uninstall（1）resolve → apply 前置", p8bc)
2329:addpage("v1p8bcc", "流程 v2：uninstall（2）寫入段", p8bcc)

exec
/usr/bin/bash -lc "sed -n '560,640p' disc_v1_b.py; sed -n '720,950p' disc_v1_b.py; sed -n '1140,1310p' disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
    ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    ex = sx0 if side == "l" else sx0 + sw
    if label and vert == "below":                                                   # 第十四輪：標籤一律放第一段水平段中央下方（不壓轉角／垂直匯流線）
        segs = [abs(busx - ex), abs(gy - ey), abs(nx - busx), abs(ty0 - gy)]; tot = sum(segs) or 1
        i = 0 if segs[0] >= 24 else 2
        pos = 2 * ((sum(segs[:i]) + segs[i] / 2) / tot) - 1
    cells.append(_edge(eid, s, t, label, (0 if side == "l" else 1, 0.5), (round(tx, 3), 0), [(busx, ey), (busx, gy), (nx, gy)], pos if label else None, vert if label else None))

def botbus(F, cells, eid, s, t, label="", busx=0, sx=0.85, tx=0.5, pos=None):
    """close() 後畫：s 底端 sx 出線 → 該列下方縫隙 → x=busx 匯流排往下 → t 上方縫隙 → t 頂端 tx 處。側邊被別條線佔用時用。"""
    A = F.abs; sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    ex = sx0 + sx * sw; gy1 = F.rb[s] + F.gap / 2; gy2 = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    cells.append(_edge(eid, s, t, label, (round(sx, 3), 1), (round(tx, 3), 0), [(ex, gy1), (busx, gy1), (busx, gy2), (nx, gy2)], pos if label else None, True if label else None))

# ================= 第十四輪共用（頁內；helper 段不動；v2.16-1／-2／-10／-19）=================
def lstart(b, cid, xid, row, verb, w=220, col=L, xcol=G, xw=200, pre=""):
    """啟動器起點兩格（v2.16-19）：{cid}0「建執行紀錄 log/<verb>/…」（row）→ cid「寫 launcher_start（失敗 → 1 + 6-38）」（row+1）→ 失敗 → xid 紅（row+1，xcol）。回傳 row+2。"""
    b.box(f"{cid}0", col, row, v2(W12), fl(pre + f"建執行紀錄 log/{verb}/<ts>-<id8>.jsonl"), w)
    b.box(cid, col, row + 1, v2(W12), fl(LS1), w)
    b.box(xid, xcol, row + 1, v2(R12), fl(LSX), xw)
    b.D(f"{cid}_0", f"{cid}0", cid, al=True); b.H(f"{cid}_x", cid, xid, "失敗")
    return row + 2

def preseg(b, pid, row, nxt, verb, ro=False, col=L, w=240, rcol=E, xcol=G, nxt_tx=0.9):
    """共通前置格（v2.16-1）：{pid}pq「偵測到既有進度檔？」（col，row）；可寫動詞：是 → {pid}pr「先恢復」（rcol）→ 失敗 → {pid}px 紅 6-27（xcol）；
    唯讀（ro）：是 → {pid}px 橙 6-33（xcol）。否／恢復後 → nxt（下一列，同欄）。回傳 row+1。"""
    b.box(f"{pid}pq", col, row, v2(D12), fl("偵測到既有進度檔（.tmp.*.toml／metadata [progress]）？"), w)
    if ro:
        b.box(f"{pid}px", xcol, row, v2(O12), fl(E33X.replace("<verb>", verb)), 220)
        b.H(f"{pid}pe_y", f"{pid}pq", f"{pid}px", "是")
    else:
        b.box(f"{pid}pr", rcol, row, v2(SUB), fl("是：先恢復（依進度檔 done／pending 續跑上次未完成的交易）"), 300, ax="l")
        b.box(f"{pid}px", xcol, row, v2(R12), fl(E27X), 200)
        b.H(f"{pid}pe_y", f"{pid}pq", f"{pid}pr", "是"); b.H(f"{pid}pe_x", f"{pid}pr", f"{pid}px", "失敗")
        b.D(f"{pid}pe_r", f"{pid}pr", nxt, "", 0.5, nxt_tx)   # nxt 是菱形 → nxt_tx=0.5（頂點）
    b.D(f"{pid}pe_n", f"{pid}pq", nxt, "否", al=True)
    return row + 1

def res3(b, pid, row, nxt, w=280, col=L, xcol=U, xw=220):
    """resolve 結果三叉（v2.16-2）：{pid}q0「resolve 回 0？」否 → {pid}q0x 橙原碼傳出；{pid}q1「vk-resolve/1 文法合法？」否 → {pid}q1x 紅 6-30；是 → nxt。回傳 row+2。"""
    b.box(f"{pid}q0", col, row, v2(D12), "resolve 回 0？", w)
    b.box(f"{pid}q0x", xcol, row, v2(O12), fl(NZX), xw)
    b.box(f"{pid}q1", col, row + 1, v2(D12), fl("是 → vk-resolve/1 文法合法？"), w)
    b.box(f"{pid}q1x", xcol, row + 1, v2(R12), fl(E30X), xw)
    b.H(f"{pid}qe_0x", f"{pid}q0", f"{pid}q0x", "否"); b.D(f"{pid}qe_01", f"{pid}q0", f"{pid}q1", "是", al=True)
    b.H(f"{pid}qe_1x", f"{pid}q1", f"{pid}q1x", "否"); b.D(f"{pid}qe_1n", f"{pid}q1", nxt, "是", al=True)
    return row + 2

def failbus(F, cells, srcs, end, busx=1610, sy=0.85, stub=16, label="失敗", tx=0.5):
    """共通失敗匯流（v2.16-10）：每個寫入格右側短線（y=sy）→ 該列下方縫隙 → x=busx 匯流排 → 終點上方一層 → 終點頂端（多條線在匯流排上重疊 = 一條匯流排）。
    close() 之後呼叫；終點列前放一列 spacer（footer(spacer=1)）給水平層用。"""
    A, RB, RT, g = F.abs, F.rb, F.rt, F.gap
    tx0, ty0, tw, th = A[end]; nx = tx0 + tx * tw; lev = RT[end] - g / 2 - 12
    for s in srcs:
        lab = label
        if isinstance(s, tuple): s, lab = s
        syy = 0.5 if F.st.get(s, "").startswith("rhombus") else sy                  # 菱形：從右頂點出
        sx0, sy0, sw, sh = A[s]; ex, ey = sx0 + sw, sy0 + syy * sh; hx = ex + stub; gy = RB[s] + g / 2
        pts = [(hx, ey), (hx, gy), (busx, gy), (busx, lev), (nx, lev)]
        tot = stub + (gy - ey) + (busx - hx) + (lev - gy) + (busx - nx) + (ty0 - lev)
        lw = sum(12 if ord(c) > 255 else 7 for c in (lab or ""))
        pos = 2 * ((stub + (gy - ey) + 6 + lw / 2) / tot) - 1 if lab else None       # 標籤放縫隙水平段起點上方
        st_ = _edge(f"fb_{s}", s, end, lab, (1, round(syy, 3)), (round(tx, 3), 0), pts, pos, "below" if lab else None)
        cells.append(st_.replace("verticalAlign=top;spacingTop=6;", "verticalAlign=bottom;spacingBottom=4;"))

def lbus(F, cells, srcs, end, busx, label="失敗", sy=0.85, stub=16, tx=0.5):
    """failbus 的左側版：寫入格左側短線 → 該列下方縫隙 → x=busx（在該欄左側）→ 終點上方縫隙 → 終點頂端（終點在左側欄）。"""
    A, RB, RT, g = F.abs, F.rb, F.rt, F.gap
    tx0, ty0, tw, th = A[end]; nx = tx0 + tx * tw; lev = RT[end] - g / 2
    for s in srcs:
        sx0, sy0, sw, sh = A[s]; ex, ey = sx0, sy0 + sy * sh; hx = ex - stub; gy = RB[s] + g / 2
        if abs(hx - busx) < 40: pts = [(busx, ey), (busx, lev), (nx, lev)]                 # 匯流排就在旁邊：短線直接接上，不折
        else: pts = [(hx, ey), (hx, gy), (busx, gy), (busx, lev), (nx, lev)]
        tot = abs(ex - busx) + (lev - ey) + abs(nx - busx) + (ty0 - lev)
        cells.append(_edge(f"lb_{s}", s, end, label, (0, round(sy, 3)), (round(tx, 3), 0), pts, 2 * ((abs(ex - busx) + 8) / tot) - 1 if label else None, "left" if label else None))

def hseg_edge(cells, eid, s, t, label, exit_, entry, pts, A):
    """自訂路徑，標籤放第一段水平段中央下方（避免壓在轉角或垂直匯流線上）。"""
    sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    p0 = (sx0 + exit_[0] * sw, sy0 + exit_[1] * sh); pn = (tx0 + entry[0] * tw, ty0 + entry[1] * th)
    allp = [p0] + list(pts) + [pn]; segs = [abs(b_[0] - a_[0]) + abs(b_[1] - a_[1]) for a_, b_ in zip(allp, allp[1:])]; tot = sum(segs) or 1

# ================= P5i：bootstrap.sh（1′）install =================
p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
b.box("a9q", L, 2, D12, "install 回 0？", 220)
b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
b.box("a9q3", L, 3, v2(D12), "否 → install 回 3？", 220)
b.box("a9c", L, 4, v2(W12), fl("否（回 1）：依 .tmp.install 進度檔清半成品（引擎寫入失敗時已自清；引擎異常結束由 bootstrap.sh 補清；log/ 保留；印「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」）"), 300)
b.box("a9h", L, 5, v2(D12), fl("需人處理（6-4／6-28／6-35 等，附指令）？"), 300)
b.box("a9hx", U, 5, v2(O12), fl("1：install 需人處理 → 依指令處理後再跑 bootstrap.sh"), 220)
b.box("a9x", G, 5, v2(R12), fl("1：install 失敗（寫入／驗證），已清半成品"), 180)
b.D("ae12e", "a9e0", "a9"); b.H("ae12", "a9", "a9e"); b.H("ae12f", "a9e", "a9f", "寫")
b.D("ae13", "a9", "a9q", al=True); b.H("ae15", "a9q", "a9z", "是"); b.D("ae14", "a9q", "a9q3", "否", al=True)
b.H("ae14x3", "a9q3", "a9x3", "是"); b.D("ae14c", "a9q3", "a9c", "否", al=True)
b.D("ae14h", "a9c", "a9h", al=True); b.H("ae14y", "a9h", "a9hx", "是"); b.H("ae14n", "a9h", "a9x", "否")
b.close()
foot(p5i, "p5i", F.y, _t5("release／tar", "--local", "docker image inspect", "6-37", "GHCR") + [("install 進度檔 .tmp.install", ".tmp.install.<id>.toml：第一次 install 也建（第一個寫入前）= 「不留半成品」的清除清單；引擎寫入失敗時依它自清；引擎異常結束（未自清）由 bootstrap.sh 依它補清；log/ 一律保留"), ("bootstrap.sh 結束碼", "= 失敗那一步的碼原樣傳出：install／add 回 3 → 3、回 2 → 2、其餘非 0 → 1；任一 -t 的 add 失敗 → 立即中止、不處理後續 -t、已完成的 add 保留；全部成功 → 0")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p5i", "流程 v2：bootstrap.sh（1′）docker run install", p5i)

# ================= P5ccc：bootstrap.sh（2）=================
p5d, F = newpage("流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add → 彙總（§2、v2.5 §8、v2.6 Q26／Q27、v2.16-5）", "", COLS5B)
b = F.band("bA2", "5a″ bootstrap.sh 後半（承「bootstrap.sh（1′）」頁）：--local → 寫 version.local.toml → 對每個 -t 呼叫 add（resolve → 三叉 → docker → apply）→ 任一段非 0 → 立即中止、該段的碼原樣傳出（3 → 3、2 → 2、其餘 → 1）；全部成功 → 0；不自刪", v2=True)
b.box("a9e2", L, 0, ENTRY, "來自「bootstrap.sh（1′）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫；已寫 launcher_start）", 320)
b.box("a8q2", L, 1, v2(D12), "--local？", 160)
b.box("a8b", L, 2, v2(W12), fl("是：寫 version.local.toml：vendor_kit = \"<tag>\"＋vendor_kit_image_id（install 成功後才寫）"), 200, ax="r")
b.box("a8f", P, 2, F12, "＋version.local.toml（不進 git；引擎本機覆寫：image tag + image ID；離線包 Q26）", 360)
b.box("a10", L, 3, W12, fl("呼叫 add <repo>[@<tag>]（-y 轉發）"), 300)
b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
res3(b, "a10r", 5, "a10d", w=300)
b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
b.files("a10f", P, 8, "add 寫（每個工具；見「add（2）」頁）", ["version.toml [tools] 版本鎖定行（最後寫）", "cache/<repo>/", "gen/<repo>.stamp", "初始檔（init.toml 的 dest）", "baseline/<repo>/ + .vendor_kit.toml", "gen/tools.just（重生，mod? 行）"], 360)
b.box("a10x", L, 9, v2(D12), "apply 回 0？", 200)
b.box("a10q", L, 10, v2(D12), "是 → 還有下一個 -t？", 200)
footer(b, F, 11, [("a13", G12, "0：全部成功，印摘要與要 git add 的清單", L, "c"), ("a12", v2(O12), fl("中止：結束碼 = 該段的碼原樣傳出（install／add 回 3 → 3、回 2 → 2、其餘非 0 → 1）；印該段錯誤；列出已完成／未處理的 -t（已完成的 add 保留）；後續 -t 不執行"), P, "c")], spacer=1, sp="l")
b.D("ae16", "a9e2", "a8q2", al=True); b.D("ae17", "a8q2", "a8b", "是"); b.H("ae17f", "a8b", "a8f", "寫")
b.LD("ae17n", "a8q2", "a10", "否", busx=380, vert="left"); b.D("ae18", "a8b", "a10")
b.D("ae19", "a10", "a10r"); b.H("ae19e", "a10r", "a10re"); b.D("ae20", "a10re", "a10rq0", "", 0.5, 0.5); b.H("ae20g", "a10g", "a10d", "拉 /dist")
b.D("ae21", "a10d", "a10a"); b.H("ae21e", "a10a", "a10ae"); b.H("ae21f", "a10ae", "a10f", "寫")
b.D("ae22", "a10ae", "a10x", "", 0.5, 0.5); b.D("ae22q", "a10x", "a10q", "是", al=True)
b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330)
b.close()
p5d[:] = [c for c in p5d if not any(c.startswith(f'<mxCell id="{i}"') for i in ("a10rq0x", "a10rq1x", "a10rq0x_v2", "a10rq1x_v2", "a10rqe_0x", "a10rqe_1x"))]   # 三叉的兩個出口併入 a12（原碼傳出／6-30 → 1）
failbus(F, p5d, [("a8b", "失敗：1"), ("a10rq0", "否：原碼傳出"), ("a10rq1", "否：1 + 6-30"), ("a10d", "失敗：1"), ("a10x", "否：原碼傳出")], "a12")
footer_edges(F, [("ae24", "a10q", "否", "d", "a13")])
foot(p5d, "p5d", F.y, [BOOT_T, ("release／tar／.digest／docker load", T5[1][1]), ("bootstrap.sh 結束碼", "= 失敗那一步的碼原樣傳出：install／add 回 3 → 3、回 2 → 2、其餘非 0 → 1；任一 -t 的 add 失敗 → 立即中止、不處理後續 -t、已完成的 add 保留；全部成功 → 0"), NZ_T, ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）"), ("version.local.toml（--local）", "vendor_kit = \"<tag>\" + vendor_kit_image_id：install 成功後才寫、失敗清除；不進 git；不自刪"), PULLX_T], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p5ccc", "流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add", p5d)

# ================= P5c：install（1）主機檢查 → 執行紀錄 → 引擎 image → 比對 → 進度檔 → 產薄殼到暫存 =================
T5I = [
 ("install 進度檔", ".tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復"),
 ("上次產物（6-28）", "薄殼每檔自描述首行的 sha256 與其餘內容相符（Q17）= 是引擎上次產出、未被人改 → 可重產；不符 → 1 + 6-28 列差異、零寫入"),
 ("6-16／6-35（主機側前置）", "6-16 不在 git repo 內（請先 git init）；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）；兩者不寫、不拉、不起容器，在建執行紀錄之前"),
 ("6-27（恢復失敗）", "可寫動詞開始前偵測到既有進度檔 → 先恢復再繼續；恢復失敗 → 1「未恢復：<檔名>」逐檔列出"),
 ("引擎 ref／docker image inspect", "引擎 ref = version.toml 的 vendor_kit 版本鎖定行（第一次 = bootstrap.sh 給的 ref）；每次 docker run 前先 inspect，本機有就不 pull、無才 pull（失敗 → 1 + 6-24／逾時 6-31）"),
 ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
 ("暫存目錄／原子替換", "先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外）"),
 LOGT[0],
]
N5I = ""
p5c, F = newpage("流程 v2：install（1）主機檢查 → 執行紀錄 → 引擎 image → docker run（§0／§2、Q20）", "", COLS5)
b = F.band("bI", "5a′ install（bootstrap.sh 代打或自己打）：主機側檢查 git repo／巢狀 → 執行紀錄 → 偵測既有進度檔 → 引擎 ref → inspect／無才 pull → docker run → flock（逾時 6-26）；薄殼比對與暫存見「install（1′）」頁", v2=True)
b.box("i0", U, 0, G12, "just vendor_kit install（-y…）", 220)
b.box("i3", U, 1, O12, fl("1 + 6-16：請先 git init（不代做；執行紀錄未建）"), 220)
b.box("i2", L, 1, v2(D12), "是 git repo？（主機側 git rev-parse）", 280)
b.box("i2x", U, 2, v2(O12), fl("1 + 6-35：不允許巢狀（上層或下層已有 .vendor_kit/）"), 220)
b.box("i2n", L, 2, v2(D12), "是 → 上層或下層已有 .vendor_kit/？", 280)
b.box("i2r", P, 2, v2(RULE), fl("禁止巢狀（Q20、§0）：由啟動器在主機側檢查——引擎只掛 /repo，看不到上層目錄，也不讀 .git；是 → 1 + 6-35；不寫、不拉、不起容器的前置檢查在建執行紀錄之前（新規則 (a)）"), 360)
lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
preseg(b, "i", 5, "i1g", "install")
b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
b.close()
bypass(F, p5c, "ie1y", "i1i", "i1")
foot(p5c, "p5c", F.y, [t for t in T5I if not t[0].startswith(("install 進度檔", "上次產物", "暫存目錄"))], ALL - {"inv", "tree", "pend"} | {"entry"})
addpage("v1p5c", "流程 v2：install（1）主機檢查 → 引擎 image → docker run", p5c)

# ================= P5cm：install（1′）比對薄殼 → 進度檔 → 產薄殼到暫存 =================
p5cm, F = newpage("流程 v2：install（1′）比對薄殼 → 進度檔 → 產薄殼五檔到暫存（§2、Q17、v2.15-11）", "", COLS5)
b = F.band("bIm", "5a″ install 引擎前半（承「install（1）」頁：已拿鎖）：薄殼已存在？→ hash 比對上次產物（6-28）→ 建進度檔（第一個寫入前）→ 產薄殼五檔到暫存 → config.toml 缺才產（含基準版副本）；寫入見「install（1″）」頁", v2=True)
b.box("i4ze0", E, 0, ENTRY, "來自「install（1）」頁：引擎已拿鎖（已寫 launcher_start）", 400)
b.box("i4e", E, 1, v2(D12), "薄殼已存在？", 250, ax="l")
b.box("i4en", E, 1, v2(SUB), "否：第一次 = 全新建", 120, ax="r")
b.box("i4x", U, 2, v2(O12), fl("1 + 6-28：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("i4q", E, 2, v2(D12), "是 → 薄殼 == 上次產物？（自描述首行 hash）", 250, ax="l")
b.box("i4qn", P, 2, v2(NOTE), fl("自描述首行（Q17）：薄殼每檔（含 log.sh）# vendor_kit-shell/<介面版> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git）"), 360)
b.box("i4l", E, 3, v2(SUB), fl("是：建進度檔 .tmp.install.<id>.toml（第一次也建；第一個寫入（含暫存檔）之前）"), 300, ax="l")
b.box("i4lf", P, 3, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度檔，不進 git；第一次 = 不留半成品的清除清單；install（2）頁最後刪）", 360)
b.box("i4", E, 4, v2(SUB), fl("產 .gitignore 到暫存（自描述首行；排除 cache/、gen/、log/、version.local.toml、.tmp.*）"), 300, ax="l")
b.box("i4_2", E, 5, v2(SUB), fl("產 entry.just 到暫存（自描述首行）"), 300, ax="l")
b.box("i4_3", E, 6, v2(SUB), fl("產 vendor.just 到暫存（自描述首行；source log.sh）"), 300, ax="l")
b.box("i4_3b", E, 7, v2(SUB), fl("產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器事件白名單）"), 300, ax="l")
b.box("i4_4", E, 8, v2(SUB), fl("產 ci/check.sh 到暫存（自描述在第二行）"), 300, ax="l")
b.box("i4_5q", E, 9, v2(D12), "config.toml 存在？（存在 → 不動）", 250, ax="l")
b.box("i4_5", E, 10, v2(SUB), fl("否：產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30）"), 300, ax="l")
b.box("i4_5b", E, 11, v2(SUB), fl("產 baseline/vendor_kit/config.toml 副本到暫存（其基準版）"), 300, ax="l")
b.box("i4z", E, 12, ENTRY, "續「install（1″）」頁：逐檔原子替換 → version.toml、gen/.stamp、基準版根檔", 400)
footer(b, F, 13, [("i4tx", v2(R12), fl("1：進度檔或暫存寫入失敗（任一步，共通匯流）→ 第一次：依進度檔清半成品；修復型：列已完成／未完成"), P, "c")], spacer=1, sp="l")
b.D("ie4a", "i4ze0", "i4e", "", 0.5, 0.5)
b.H("ie5n", "i4e", "i4en", "否"); b.D("ie5y", "i4e", "i4q", "是", al=True); b.H("ie5x", "i4q", "i4x", "否")
b.D("ie6", "i4q", "i4l", "是", al=True); b.D("ie6n", "i4en", "i4l", "", 0.5, 0.9)
b.H("ie6lf", "i4l", "i4lf", "寫"); b.D("ie6ln", "i4l", "i4", al=True)
b.D("ie4c", "i4", "i4_2"); b.D("ie4d", "i4_2", "i4_3"); b.D("ie4e", "i4_3", "i4_3b"); b.D("ie4e2", "i4_3b", "i4_4"); b.D("ie4f", "i4_4", "i4_5q", al=True)
b.D("ie4g", "i4_5q", "i4_5", "否", al=True); b.D("ie4h", "i4_5", "i4_5b"); b.D("ie5", "i4_5b", "i4z", "", 0.5, 0.5)
b.close()
sidebus(F, p5cm, "ie4gy", "i4_5q", "i4z", "是：不產、不動", busx=565, tx=0.15, pos=-0.6, vert="below")
failbus(F, p5cm, ["i4l", "i4", "i4_2", "i4_3", "i4_3b", "i4_4", "i4_5", "i4_5b"], "i4tx")
foot(p5cm, "p5cm", F.y, [t for t in T5I if t[0].startswith(("install 進度檔", "上次產物", "暫存目錄", "config.toml"))] + [("薄殼五檔", ".vendor_kit/ 內進 git 的 .gitignore、entry.just、vendor.just、log.sh、ci/check.sh；每檔帶自描述首行；只由 install／升引擎產生或重產")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p5cm", "流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存", p5cm)


# ================= P5cw：install（1′）寫入 =================
p5cw, F = newpage("流程 v2：install（1″）原子替換 → version.toml、gen/.stamp、基準版（§2、v2.13 P5）", "", COLS5)
b = F.band("bI1", "5a‴ install 寫入段（承「install（1′）」頁：進度檔已建、五檔已在暫存）：薄殼五檔逐檔原子替換 → config.toml 缺才寫（含基準版副本與 metadata）→ version.toml 缺才寫 → gen/.stamp → baseline/.gitkeep 缺才建；續「install（2）」頁", v2=True)
b.box("i4ze", E, 0, ENTRY, "來自「install（1′）」頁：進度檔已建；薄殼五檔（＋config.toml 若缺）已產到暫存（已寫 launcher_start）", 400)
b.box("i4b", E, 1, v2(SUB), fl("薄殼五檔逐檔原子替換（暫存 → 正式位置）"), 300, ax="l")
b.files("i4f", P, 1, "＋.vendor_kit/ 薄殼五檔（進 git）", [".gitignore", "entry.just", "vendor.just", "log.sh", "ci/check.sh"], 360, cols=2)
b.box("i4bcq", E, 2, v2(D12), "config.toml 本次有產到暫存（原本缺）？", 260, ax="l")
b.box("i4bc", E, 3, v2(SUB), fl("是：config.toml 原子替換"), 300, ax="l")
b.box("i4bcf", P, 3, v2(F12), "＋config.toml（進 git；含註解與預設）", 360)
b.box("i4bb", E, 4, v2(SUB), fl("baseline/vendor_kit/config.toml 副本原子替換"), 300, ax="l")
b.box("i4bbf", P, 4, v2(F12), "＋baseline/vendor_kit/config.toml（進 git；三方合併用的 B）", 360)
b.box("i4bm", E, 5, v2(SUB), fl("寫 metadata baseline/.vendor_kit.toml：config.toml state=managed"), 300, ax="l")
b.box("i4bmf", P, 5, v2(F12), "＋baseline/.vendor_kit.toml（進 git；config.toml 與根 .dockerignore 的紀錄，v2.13 P10）", 360)
b.box("i4cq", E, 6, v2(D12), "version.toml 缺？", 260, ax="l")
b.box("i4c", E, 7, v2(SUB), fl("是：寫 version.toml（vendor_kit 版本鎖定行 = 引擎 ref＋schema、written_by）"), 300, ax="l")
b.box("i4cf", P, 7, F12, "＋version.toml（vendor_kit 版本鎖定行、schema、written_by；進 git）", 360)
b.box("i4d", E, 8, v2(SUB), "寫 gen/.stamp（只記引擎 ref）", 300, ax="l")
b.box("i4df", P, 8, F12, "＋gen/.stamp（不進 git）", 360)
b.box("i4g", E, 9, v2(SUB), fl("缺才建 baseline/.gitkeep（VK 自產進 git 的檔，hash 固定為空檔；metadata 到 add 才建）"), 300, ax="l")
b.box("i4gf", P, 9, F12, "＋baseline/.gitkeep（進 git）", 360)
b.box("i5z", E, 10, ENTRY, "續「install（2）」頁：根 justfile 與根 .dockerignore", 300, ax="l")
b.box("_sp", U, 11, "text;html=1;fillColor=none;strokeColor=none;", "", 10, h=28, minh=28, ax="l")
b.box("i4wq", E, 12, v2(D12), "任一步寫入失敗 → 第一次安裝？", 260)
b.box("i4wx1", G, 12, v2(R12), fl("1：依進度檔移除已寫的檔、不留半成品（log/ 保留）"), 220)
b.box("i4wx2", E, 13, v2(R12), fl("1：列已完成／未完成，下次可寫動詞先恢復（進度檔保留）"), 220)
b.D("ie5e", "i4ze", "i4b", "", 0.375, 0.5)
b.H("ie6f", "i4b", "i4f", "寫"); b.D("ie6q", "i4b", "i4bcq", al=True); b.D("ie6bc", "i4bcq", "i4bc", "是", al=True); b.H("ie6bcf", "i4bc", "i4bcf", "寫"); b.D("ie6bb", "i4bc", "i4bb"); b.H("ie6bbf", "i4bb", "i4bbf", "寫")
b.D("ie6bm", "i4bb", "i4bm"); b.H("ie6bmf", "i4bm", "i4bmf", "寫"); b.D("ie6cq", "i4bm", "i4cq", al=True)
b.D("ie6c", "i4cq", "i4c", "是", al=True); b.H("ie6cf", "i4c", "i4cf", "寫"); b.D("ie6d", "i4c", "i4d"); b.H("ie6df", "i4d", "i4df", "寫")
b.D("ie6g", "i4d", "i4g"); b.H("ie6gf", "i4g", "i4gf", "寫"); b.D("ie7", "i4g", "i5z", al=True)
b.H("ie8y", "i4wq", "i4wx1", "是"); b.D("ie8n", "i4wq", "i4wx2", "否", al=True)
b.close()
sidebus(F, p5cw, "ie6bn", "i4bcq", "i4cq", "否：已有 → 不動", busx=570); sidebus(F, p5cw, "ie6cn", "i4cq", "i4d", "否：已有 → 不動", busx=570, tx=0.3)
failbus(F, p5cw, ["i4b", "i4bc", "i4bb", "i4bm", "i4c", "i4d", "i4g"], "i4wq")
foot(p5cw, "p5cw", F.y, [t for t in T5I if t[0].startswith(("install 進度檔", "暫存目錄", "config.toml"))] + [GS_T, ("baseline/.gitkeep", "VK 自產進 git 的檔，hash 固定為空檔；install 缺才建；metadata baseline/.vendor_kit.toml 記 config.toml 與根 .dockerignore 的紀錄（v2.13 P10）")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p5cw", "流程 v2：install（1″）寫入", p5cw)

# ================= P5cc：install（2）根 justfile 與 .dockerignore =================
COLS5I2 = [("使用者", 40, 120), ("啟動器（主機 sh）", 180, 260), ("引擎容器", 460, 580), ("GHCR", 1060, 160), ("專案目錄", 1240, 360)]   # install（2）：引擎欄三條車道
p5cc, F = newpage("流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22、v2.16-7）", "", COLS5I2)
b = F.band("bI2", "5a⁗ install 收尾（承「install（1″）」頁）：根 justfile（無 → 新建；symlink → 不寫、印一次性遷移指示；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；symlink → 不寫；逐行辨識只加缺的行、只記實際新增的行）→ 刪進度檔 → 0", v2=True)
SP = 190   # 引擎欄主幹（菱形）650..900：左車道 460..580（不動）、右車道 920..1040（建檔）；x=445 左匯流排（--no-justfile 與各「不動」）、x=1610 右匯流排（建檔 → 下一段）
b.box("i5e", E, 0, ENTRY, "來自「install（1″）」頁：薄殼與 .vendor_kit/ 各檔已寫（已寫 launcher_start）", 300, ax="l")
b.box("i5", E, 1, v2(D12), "--no-justfile？", 250, ax=SP)
b.box("i6", E, 2, D12, "否 → 有根 justfile？", 250, ax=SP)
b.box("i6s", E, 3, v2(D12), "有 → 是 symlink？", 250, ax=SP)
b.box("i6sp", E, 3, v2(SUB), fl("是：不寫，印一次性遷移指示"), 120, ax=0)
b.box("i8", E, 4, v2(D12), "否 → 已含 import 那行？", 250, ax=SP)
b.box("i8p", E, 4, v2(SUB), fl("是：不再加（印已含）"), 120, ax=0)
b.box("i12", E, 5, D12, "問 6-20「要加這一行嗎」同意？（-y 免問）", 250, ax=SP)
b.box("i7", E, 5, SUB, fl("無：建 justfile（四行，逐字見右）、印建了什麼"), 120, ax="r")
b.box("i12p", E, 5, v2(SUB), fl("否：不動（印指示）"), 120, ax=0)
b.box("i11f", P, 5, v2(PRE), "justfile（新建 = 這四行；已有 → 尾端只加第一行）\nimport '.vendor_kit/entry.just'\n\ndefault:\n\t@just --list", 360)
b.box("i11", E, 6, SUB, fl("是：append 那一行（import）、印加了什麼"), 250, ax=SP)
b.box("ig", E, 7, v2(D12), "有根 .dockerignore？", 250, ax=SP)
b.box("igs", E, 8, v2(D12), "有 → 是 symlink？", 250, ax=SP)
b.box("ign", E, 8, v2(SUB), fl("無：建 .dockerignore（四行，逐字同右）、印建了什麼"), 120, ax="r")
b.box("igsp", E, 8, v2(SUB), fl("是：不寫，印一次性遷移指示"), 120, ax=0)
b.box("igyf", P, 8, v2(PRE), ".dockerignore（新建 = 這四行；已有 → 只加缺的行）：\n.vendor_kit/cache/\n.vendor_kit/gen/\n.vendor_kit/.tmp.*\n.vendor_kit/log/", 360)
b.box("igq0", E, 9, v2(D12), "否 → 逐行辨識：四行全都已在？", 250, ax=SP)
b.box("igq0p", E, 9, v2(SUB), fl("是：跳過（印已含）"), 120, ax=0)
b.box("igq", E, 10, v2(D12), "否 → 問 6-34「要加這幾行嗎」（只列缺的行）同意？（-y 免問）", 250, ax=SP)
b.box("igqp", E, 10, v2(SUB), fl("否：不動（印指示）"), 120, ax=0)
b.box("igy", E, 11, v2(SUB), fl("是：只 append 缺的行、印加了什麼"), 250, ax=SP)
b.box("igm", E, 12, v2(SUB), fl("只記實際新增的行到 baseline/.vendor_kit.toml（lines）"), 250, ax=SP)
b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
b.H("ie13b", "i8", "i8p", "是"); b.D("ie14", "i8", "i12", "否", al=True)
b.D("ie17", "i12", "i11", "是", al=True); b.H("ie18", "i12", "i12p", "否"); b.LU("ie16f", "i11", "i11f", "寫", tx=0.5); b.D("ie19d", "i11", "ig", al=True)
b.H("ie7f", "i7", "i11f", "寫")
b.RD("ie20", "ig", "ign", "無"); b.D("ie21", "ig", "igs", "有", al=True)
b.H("ie20f", "ign", "igyf", "寫")
b.H("ie21s", "igs", "igsp", "是"); b.D("ie21sn", "igs", "igq0", "否", al=True)
b.H("ie21y", "igq0", "igq0p", "是"); b.D("ie21n", "igq0", "igq", "否", al=True)
b.H("ie22", "igq", "igqp", "否"); b.D("ie23", "igq", "igy", "是", al=True); b.LU("ie23f", "igy", "igyf", "寫", tx=0.5)
b.D("ie23m", "igy", "igm", al=True); b.H("ie23mf", "igm", "igmf", "寫")
b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
b.D("ie25", "idl", "iz", "", 0.5, 0.5)
b.close()
_A = F.abs
def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
    sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    tot = (sx0 - busx) + (gy - ey) + (nx - busx) + 10
    p5cc.append(_edge(eid, s, t, label, (0, 0.5), (round(tx, 3), 0), [(busx, ey), (busx, gy), (nx, gy)], 2 * (14 / tot) - 1 if label else None, "below" if label else None))
def _ub(eid, s, t, tx, busx=1610):   # 右車道「建檔」格 → 頂端出 → 上方縫隙 → 右匯流排 → 目標上方縫隙 → 目標頂端（避開同列檔案框與 LU 寫線）
    sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ex = sx0 + sw / 2; gyu = F.rt[s] - F.gap / 2; gyt = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    p5cc.append(_edge(eid, s, t, "", (0.5, 0), (round(tx, 3), 0), [(ex, gyu), (busx, gyu), (busx, gyt), (nx, gyt)], None))
_ub("ie13", "i7", "ig", 0.5); _ub("ie20z", "ign", "idl", 0.95)
_lb("ie8", "i5", "ig", "是：不碰根 justfile", 0.5)
for _s in ("i6sp", "i8p", "i12p"): _lb(f"{_s}_l", _s, "ig", "", 0.5)
for _s in ("igsp", "igq0p", "igqp"): _lb(f"{_s}_l", _s, "idl", "", 0.1)
tty(F, p5cc, "i12", "igq")
foot(p5cc, "p5cc", F.y, [t for t in T5I if t[0].startswith(("install 進度檔",))] + [
 ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
 ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
 ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
 ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
 E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)

 ("extract", "啟動器 docker create <image> /x → docker cp c:/dist/. <tmp>/<repo>/ → docker rm（三步合稱；任一步或暫存目錄失敗 → 1）；每個 extract 項各做一次"),
 ARGV_T, E12_T, NZ_T, *LOGT,
]
def _t6(*keep): return [t for t in T6 if t[0].startswith(keep)]
N6 = ""
p6, F = newpage("流程 v2：sync（1）啟動器：專案根 → 執行紀錄 → 偵測進度檔 → 快路徑 → 起引擎（§6、Q22）", "", COLS5)
b = F.band("eA", "sync（recipe 自動前置；CI 模式不走快路徑）第 1 段：專案根檢查 → 執行紀錄 → 偵測既有進度檔（6-33 → 1）→ 比對 gen/.stamp（install／升引擎跳過）→ 快路徑 grep 全相符 → 0；有差 → inspect／pull → 引擎 resolve sync（「sync（1′）」頁）", v2=True)
b.box("n0", U, 0, G12, "打工具 recipe（_sync 自動前置）或 just vendor_kit sync", 220)
b.box("n0q", L, 0, v2(D12), fl("在專案根執行？（recipe 檢查；_sync 已先 cd）"), 280)
b.box("n0qx", G, 0, v2(O12), fl("1 + 6-9：請到 <dir> 執行（執行紀錄未建）"), 200)
lstart(b, "n0l", "n0x", 1, "sync", pre="是：")
preseg(b, "n", 3, "n1", "sync", ro=True, xcol=U)
b.box("n1x", U, 4, v2(R12), fl("1：版本鎖定行命中 ≠ 1（缺或重複）"), 220)
b.box("n1", L, 4, v2(W12), fl("否：grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；version.local.toml 本機覆寫優先）"), 240, ax="r")
b.files("n2", P, 4, "讀", [".vendor_kit/version.toml（進 git）", ".vendor_kit/version.local.toml（不進 git，dev 用）"], 360)
b.box("n3n", U, 5, v2(O12), fl("1 + 6-1：vendor_kit 已更新 vX → vY，請執行 just vendor_kit upgrade vendor_kit"), 220)
b.box("n3", L, 5, v2(D12), fl("gen/.stamp 的引擎 ref ＝ 版本鎖定行？（缺 gen/.stamp → 改以薄殼自描述首行 engine= 比對）"), 280)
b.box("n6", P, 5, v2(RULE), fl("統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印 6-1「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／升引擎不受此關"), 360)
b.box("nq", L, 6, v2(D12), fl("快路徑：grep 全相符且非 CI 模式？"), 240, ax=20)
b.box("nqr", P, 6, v2(RULE), fl("快路徑（Q22、§3.6）：啟動器只 grep：[tools] 每行 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；每個 cache/<repo>/ 存在（目錄或 symlink；印記在而 cache 被刪 → 不走快路徑）；gen/tools.just 存在；非 CI 模式；sync 無參數。全相符 → 寫執行紀錄後 0；否則起引擎"), 360)
b.box("nq0", U, 7, v2(G12), fl("0：不起容器，接著跑原本的 recipe（快路徑）"), 220)
b.box("nqf", L, 7, v2(W12), fl("是：執行紀錄寫 sync_fast_path"), 100, ax="l")
b.box("n6b", P, 7, v2(RULE), fl("薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與升引擎做；做之前比對現內容 == 上次產物（自描述首行 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼"), 360)
b.box("n1i", L, 8, v2(D12), "否 → docker image inspect：本機有？", 180, ax=50)
b.box("n1p", L, 9, v2(W12), "無：docker pull <引擎 ref>", 120, ax="r")
b.box("n1g", G, 9, IMG, "vendor_kit:vN@sha256:…\n（引擎 image）", 220)
b.box("n1vx", U, 10, v2(O12), fl("1：本機覆寫的 image ID 不符（同 tag 重 build；本機覆寫已失效，請 undev 或重新 dev）"), 220)
b.box("n1v", L, 10, v2(D12), fl("有 → 覆寫中且 .Id ≠ 記的 image ID？"), 200, ax="l")
b.box("n1z", L, 11, ENTRY, "續「sync（1′）」頁：docker run <引擎> resolve sync", 280, ax="l")
footer(b, F, 12, [("n1px", v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到（分類）／逾時"), G, "c")], spacer=1, sp="l")
b.H("ne0", "n0", "n0q"); b.H("ne0x", "n0q", "n0qx", "否"); b.D("ne0l", "n0q", "n0l0", "是", al=True); b.D("ne1l", "n0l", "npq", al=True)
b.H("ne1xx", "n1", "n1x", "≠ 1"); b.H("ne2", "n1", "n2", "讀"); b.D("ne3", "n1", "n3", al=True)
b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.LD("ne5q", "nq", "nqf", "是", busx=300, vert=True); b.H("ne5ql", "nqf", "nq0"); b.D("ne5n", "nq", "n1i", "否", 0.5, 0.5)
b.RD("ne5p", "n1i", "n1p", "無", tx=0.5); b.H("ne5g", "n1g", "n1p", "拉"); b.D("ne5v", "n1i", "n1v", "有", al=True)
b.D("ne5pv", "n1p", "n1z", "", 0.5, 0.79)
b.H("ne5y", "n1v", "n1vx", "是"); b.D("ne5i", "n1v", "n1z", "否", al=True)
b.close()
footer_edges(F, [("ne5x", "n1p", "失敗", "rb", "n1px", 0.75)])
foot(p6, "p6", F.y, _t6("快路徑", "6-9", "統一提示", "引擎 ref", "gen/ 三種", "docker image inspect", "6-33", "覆寫兩種"), ALL - {"tree", "pend", "inv"} | {"entry"})
addpage("v1p6", "流程 v2：sync（1）啟動器快路徑", p6)

# ================= P6cc：sync（1′）引擎 resolve =================
COLS5S = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 280), ("引擎容器", 580, 640), ("專案目錄", 1240, 360)]   # sync(1′) 無 image：引擎欄兩條車道
LR = 460   # 右車道起點（1040..1220，180 寬）；菱形 360 寬（580..940）→ 右頂點到右車道 100px
p6r, F = newpage("流程 v2：sync（1′）引擎 resolve sync（逐工具；§6、v2.2 A／B／E、v2.3 §3／§4、v2.15-17）", "", COLS5S)
b = F.band("eA2", "sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → CI 模式 vs 本機覆寫 → 逐工具算待辦 → 彙整 → 指紋 → stdout（apply|yes／no）→ 啟動器驗文法 → 空 → 0；有待辦 → 第 2 段見「sync（2）」頁", v2=True)
b.box("n1e", L, 0, ENTRY, "來自「sync（1）」頁：引擎 image 已在本機、快路徑有差、無未完成交易（已寫 launcher_start）", 280)
b.box("n1b", L, 1, v2(W12), fl("docker run <引擎> resolve sync（永不 -t）"), 280)
b.box("n1be", E, 1, v2(SUB), "resolve sync（不寫任何檔）：讀 version.toml、各 metadata、印記", 360, ax="l")
b.box("ncx", U, 2, v2(O12), "1：CI 模式拒絕本機覆寫（請先 undev）", 220)
b.box("nc", E, 2, v2(D12), "CI 模式且有本機覆寫？", 360, ax="l")
b.box("nf", P, 2, v2(RULE), fl("CI 模式（v2.6 §2）= 只准寫 cache/、gen/；不查最新版；需寫任何進 git 的檔 → 1（-y 不解除）；升為失敗：薄殼不符、基準版落後、未完成接入、任何本機覆寫"), 340)
b.box("t0", E, 3, v2(D12), "否 → path 覆寫（dev 中）？", 360, ax="l")
b.box("t0s", E, 3, v2(SUB), fl("是：跳過取件／verify（仍查 metadata、基準版）↓"), 180, ax=LR)
b.box("t1", E, 4, v2(D12), "cache 缺或印記 ≠ 鎖定？", 360, ax="l")
b.box("t1y", E, 4, v2(SUB), fl("是：列待辦「取件鎖定版」＋「apply 後全檔驗證」（版本變動那次）"), 180, ax=LR)
b.box("t0r", P, 4, v2(RULE), fl("覆寫兩種（v2.1 B）：引擎 vendor_kit = \"<tag>\"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 <repo> = \"path:<dir>\" → cache/<repo>/ 是 symlink，跳過取件／verify"), 340)
b.box("t2q", E, 5, v2(D12), fl("否 → 逐檔驗？（--verify／CI 模式）"), 360, ax="l")
b.box("t2qn", E, 5, v2(SUB), fl("否：不逐檔驗（快）↓"), 180, ax=LR)
b.box("t2", E, 6, D12, "是 → 每檔 sha256 ＝ 印記？", 360, ax="l")
b.box("t2n", E, 6, SUB, fl("否：列待辦「重裝一次 + warn（cache 被改過）」＋「再驗」"), 180, ax=LR)
b.box("t3mx", U, 7, v2(R12), fl("1：metadata 失蹤或不可解析（驗證不過）"), 220)
b.box("t3m", E, 7, v2(D12), "metadata 存在且可解析？", 360, ax="l")
b.box("t3a", U, 8, O12, fl("1 + 6-13：<repo> 未完成接入，請先 add <repo>"), 220)
b.box("t3", E, 8, D12, "是 → metadata 有完成標記？", 360, ax="l")
b.box("t3r", P, 8, v2(INV), fl("不變量（v2.1 A、v2.5 §9）：自動化不碰專案檔 —— sync 不寫 version.toml、初始檔、基準版、薄殼、gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp"), 340)
b.box("t4", E, 9, D12, "最後合併版本 ＝ 鎖定版？", 360, ax="l")
b.box("t4r", U, 10, O12, fl("1 + 6-5：基準版落後（請在本機 upgrade <repo> -y 後 push）"), 220)
b.box("t4c", E, 10, D12, "否（落後）→ CI 模式？", 360, ax="l")
b.box("t5", E, 11, SUB, fl("否：warn「基準版落後，請 just vendor_kit upgrade <repo>」（繼續）"), 360, ax="l")
b.box("tq", E, 12, v2(D12), "還有工具？", 360, ax="l")
b.box("t6", E, 13, v2(D12), fl("否 → tools.just 缺或不符？"), 360, ax="l")
b.box("t6y", E, 13, v2(SUB), fl("是：列待辦「重生 gen/tools.just」"), 180, ax=LR)
b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
b.H("te3", "t1", "t1y", "是"); b.D("te4", "t1", "t2q", "否", al=True); b.R("te5", "t1y", "t3m", "", busx=1230)
b.H("te3q", "t2q", "t2qn", "否"); b.D("te4q", "t2q", "t2", "是", al=True); b.R("te5q", "t2qn", "t3m", "", busx=1230)
b.H("te6", "t2", "t2n", "否"); b.D("te7", "t2", "t3m", "是", al=True); b.R("te8", "t2n", "t3m", "", busx=1230)
b.H("te9m", "t3m", "t3mx", "否"); b.D("te9", "t3m", "t3", "是", al=True)
b.H("te9x", "t3", "t3a", "否"); b.D("te10", "t3", "t4", "是", al=True)
b.D("te11", "t4", "t4c", "否", al=True); b.H("te12", "t4c", "t4r", "是"); b.D("te13", "t4c", "t5", "否", al=True)
b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
b.D("te15n", "tq", "t6", "否", al=True)
b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
b.close()
_A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
_tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)

# ================= P6c：sync（2）第 2 段 apply =================
p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
res3(b, "m0", 1, "m0a")
pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
b.box("m0lq", L, 6, v2(D12), "還有下一個 extract？", 240)
b.box("m1", L, 7, v2(W12), fl("否：docker run … -v <tmp>:/dist:ro（含 vk-resolve）<引擎> apply sync"), 280)
b.box("m2a", E, 7, v2(SUB), fl("apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）"), 400)
b.box("m2ax", G, 7, v2(R12), fl(E26X), 200)
b.box("m2b", E, 8, v2(SUB), "重驗 resolve 的輸入指紋（讀 /dist/vk-resolve）", 400)
b.box("m2x", U, 8, v2(O12), fl("1 + 6-12：指紋不同「請重跑」"), 220)
b.box("m2cx", U, 9, v2(O12), fl("1：原 argv 與計畫不一致，請重跑"), 220)
b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
b.D("me3", "m2c", "m2z", "是", al=True)
b.close()
bypass(F, p6c, "me0y", "m0a", "m0b")
_A = F.abs; _sx, _sy, _sw, _sh = _A["m0lq"]; _tx, _ty, _tw, _th = _A["m0a"]; _ey = _sy + _sh / 2; _gy = F.rt["m0a"] - F.gap / 2; _nx = _tx + _tw / 2; _bx = 1250
_tot = (_bx - (_sx + _sw)) + (_ey - _gy) + (_bx - _nx) + 10
p6c.append(_edge("me0ly", "m0lq", "m0a", "是：下一個 extract", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈走右側（避開左側失敗線）
foot(p6c, "p6c", F.y, _t6("待辦清單", "6-26", "extract", "原 argv", "6-12", "resolve 非 0") + [PULLX_T, ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend", "rule", "inv"} | {"entry"})
addpage("v1p6c", "流程 v2：sync（2）三叉 → docker → apply 前置", p6c)

# ================= P6cw：sync（2′）apply 寫入段 =================
p6cw, F = newpage("流程 v2：sync（2′）apply 寫入段：取件 → 印記 → 驗 → tools.just（§6、v2.15-17、v2.16-11）", "", COLS5)
b = F.band("eB2", "sync 第 2 段續（承「sync（2）」頁：已拿鎖、重驗、argv 一致）：逐待辦工具取件 → 印記 → 逐檔驗（--verify／CI／版本變動那次）→ 不符重裝一次再驗 → 還有工具？→ tools.just 在待辦？→ 最後原子重生 → 0", v2=True)
b.box("m3e", E, 0, ENTRY, "來自「sync（2）」頁：apply 前置通過（已寫 launcher_start）", 400)
b.box("m3", E, 1, v2(SUB), fl("逐待辦工具：取件 /dist/<repo> 展開到暫存目錄"), 400)
b.box("m3c", E, 2, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("m3f", P, 2, F12, "cache/<repo>/（重寫，不進 git）", 360)
b.box("m3b", E, 3, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("m3bf", P, 3, F12, "gen/<repo>.stamp（重寫，不進 git）", 360)
b.box("m3vd", E, 4, v2(D12), "逐檔驗？（--verify／CI 模式／版本變動的那次）", 400, ax="l")
b.box("m3v", E, 5, v2(SUB), fl("是：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）"), 400)
b.box("m3vq", E, 6, v2(D12), "全部相符？", 200, ax="l")
b.box("m3vn", E, 6, v2(SUB), fl("否：重裝該工具一次 + warn（cache 被改過）"), 150, ax="r")
b.box("m3v2", E, 7, v2(SUB), fl("再逐檔驗一次"), 150, ax="r")
b.box("m3x2", G, 8, v2(R12), fl("1：重裝後仍不符（取件／寫入／驗證失敗），不再重裝"), 200)
b.box("m3vq2", E, 8, v2(D12), "相符？", 150, ax="r")
b.box("mq", E, 9, v2(D12), "還有待辦工具？", 200, ax="l")
b.box("m5q", E, 10, v2(D12), "否 → gen/tools.just 在待辦（缺或不符）？", 300, ax="l")
b.box("m5", E, 11, v2(SUB), fl("是：重生 gen/tools.just（每個 <ns>.just 一行 mod?；與 cache 同一 apply 內原子替換，最後做）"), 400)
b.box("m5f", P, 11, F12, "gen/tools.just（不進 git；gen/.stamp 不動）", 360)
footer(b, F, 12, [("m7", G12, "0：接著跑原本的 recipe", E, "l"), ("m7x", v2(R12), fl("1：取件／寫入失敗（任一步，共通匯流）→ 列出已完成；cache 可能部分更新，下次 sync 再取"), P, "c")], spacer=1, sp="l")
b.D("me3", "m3e", "m3")
b.D("me3c", "m3", "m3c"); b.H("me4", "m3c", "m3f", "寫"); b.D("me4b", "m3c", "m3b"); b.H("me4f", "m3b", "m3bf", "寫"); b.D("me4v", "m3b", "m3vd", al=True)
b.D("me4vy", "m3vd", "m3v", "是", al=True)
b.D("me4q", "m3v", "m3vq", al=True); b.H("me4n", "m3vq", "m3vn", "否"); b.D("me5", "m3vq", "mq", "是", al=True)
b.D("me5n", "m3vn", "m3v2"); b.D("me5v2", "m3v2", "m3vq2", al=True); b.H("me5x2", "m3vq2", "m3x2", "否"); b.D("me5y2", "m3vq2", "mq", "是", 0.5, 0.5)
b.LL("me6y", "mq", "m3", "是：下一個工具", busx=545); b.D("me6n", "mq", "m5q", "否", al=True)
b.D("me6q", "m5q", "m5", "是", al=True); b.H("me12", "m5", "m5f", "寫")
b.close()
failbus(F, p6cw, ["m3c", "m3b", "m5"], "m7x")
footer_edges(F, [("me15", "m5", "", "d", "m7")])
sidebus(F, p6cw, "me4vn", "m3vd", "mq", "否", busx=565, tx=0.5, pos=-0.6, vert="below")
sidebus(F, p6cw, "me6qn", "m5q", "m7", "否：不動", busx=565, tx=0.5, pos=-0.6, vert="below")
foot(p6cw, "p6cw", F.y, _t6("待辦清單", "verify", "gen/ 三種", "覆寫兩種"), ALL - {"tree", "pend", "rule", "inv"} | {"entry"})
addpage("v1p6cw", "流程 v2：sync（2′）apply 寫入段", p6cw)


# ================= P7：upgrade ── A. Renovate 路徑 =================
T7 = [
 ("Renovate／regex manager", "GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"),
 ("PR／commit／push／rebase／merge", "PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"),
 ("check.sh（PR CI）", "下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1 = CI 模式）= ⓪ git ls-files 拒絕納管的 version.local.toml → ① sync → ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼原樣傳出（含 1 與工具自己的碼）；每個動詞各自一份執行紀錄"),

exec
/usr/bin/bash -lc 'for f in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py; do echo "$f"; python3 "$f" v1_b.drawio 2>&1 | tail -5; done' in <scratchpad>
 succeeded in 1388ms:
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
check_overlap.py
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
check_cross_v1b.py
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
check_self_v1b.py
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
check_jog_r7.py
共 0 筆
check_align_v1b.py
   無
== 流程 v2：uninstall（1）resolve → apply 前置
   無
== 流程 v2：uninstall（2）寫入段
   無

codex
基線六項幾何檢查本來就是 0；目前真正的機械缺口集中在 3 個前引與 install(2) 的 4 條寫入失敗邊。接下來的修改會保持現有零交叉骨架，並同步處理 v2.17 的明確內容錯誤（install 恢復位置／錯誤出口、sync 三叉順序、失敗終點文字與數個一格多事）。
apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..64f8aa6c571fb456372b64e1331808d0f5ef6afc
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..64f8aa6c571fb456372b64e1331808d0f5ef6afc
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)

exec
/usr/bin/bash -lc "sed -n '885,950p' disc_v1_b.py; sed -n '1060,1130p' disc_v1_b.py; sed -n '1325,1370p' disc_v1_b.py; sed -n '1510,1550p' disc_v1_b.py; sed -n '2185,2235p' disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
p5cc, F = newpage("流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22、v2.16-7）", "", COLS5I2)
b = F.band("bI2", "5a⁗ install 收尾（承「install（1″）」頁）：根 justfile（無 → 新建；symlink → 不寫、印一次性遷移指示；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；symlink → 不寫；逐行辨識只加缺的行、只記實際新增的行）→ 刪進度檔 → 0", v2=True)
SP = 190   # 引擎欄主幹（菱形）650..900：左車道 460..580（不動）、右車道 920..1040（建檔）；x=445 左匯流排（--no-justfile 與各「不動」）、x=1610 右匯流排（建檔 → 下一段）
b.box("i5e", E, 0, ENTRY, "來自「install（1″）」頁：薄殼與 .vendor_kit/ 各檔已寫（已寫 launcher_start）", 300, ax="l")
b.box("i5", E, 1, v2(D12), "--no-justfile？", 250, ax=SP)
b.box("i6", E, 2, D12, "否 → 有根 justfile？", 250, ax=SP)
b.box("i6s", E, 3, v2(D12), "有 → 是 symlink？", 250, ax=SP)
b.box("i6sp", E, 3, v2(SUB), fl("是：不寫，印一次性遷移指示"), 120, ax=0)
b.box("i8", E, 4, v2(D12), "否 → 已含 import 那行？", 250, ax=SP)
b.box("i8p", E, 4, v2(SUB), fl("是：不再加（印已含）"), 120, ax=0)
b.box("i12", E, 5, D12, "問 6-20「要加這一行嗎」同意？（-y 免問）", 250, ax=SP)
b.box("i7", E, 5, SUB, fl("無：建 justfile（四行，逐字見右）、印建了什麼"), 120, ax="r")
b.box("i12p", E, 5, v2(SUB), fl("否：不動（印指示）"), 120, ax=0)
b.box("i11f", P, 5, v2(PRE), "justfile（新建 = 這四行；已有 → 尾端只加第一行）\nimport '.vendor_kit/entry.just'\n\ndefault:\n\t@just --list", 360)
b.box("i11", E, 6, SUB, fl("是：append 那一行（import）、印加了什麼"), 250, ax=SP)
b.box("ig", E, 7, v2(D12), "有根 .dockerignore？", 250, ax=SP)
b.box("igs", E, 8, v2(D12), "有 → 是 symlink？", 250, ax=SP)
b.box("ign", E, 8, v2(SUB), fl("無：建 .dockerignore（四行，逐字同右）、印建了什麼"), 120, ax="r")
b.box("igsp", E, 8, v2(SUB), fl("是：不寫，印一次性遷移指示"), 120, ax=0)
b.box("igyf", P, 8, v2(PRE), ".dockerignore（新建 = 這四行；已有 → 只加缺的行）：\n.vendor_kit/cache/\n.vendor_kit/gen/\n.vendor_kit/.tmp.*\n.vendor_kit/log/", 360)
b.box("igq0", E, 9, v2(D12), "否 → 逐行辨識：四行全都已在？", 250, ax=SP)
b.box("igq0p", E, 9, v2(SUB), fl("是：跳過（印已含）"), 120, ax=0)
b.box("igq", E, 10, v2(D12), "否 → 問 6-34「要加這幾行嗎」（只列缺的行）同意？（-y 免問）", 250, ax=SP)
b.box("igqp", E, 10, v2(SUB), fl("否：不動（印指示）"), 120, ax=0)
b.box("igy", E, 11, v2(SUB), fl("是：只 append 缺的行、印加了什麼"), 250, ax=SP)
b.box("igm", E, 12, v2(SUB), fl("只記實際新增的行到 baseline/.vendor_kit.toml（lines）"), 250, ax=SP)
b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
b.H("ie13b", "i8", "i8p", "是"); b.D("ie14", "i8", "i12", "否", al=True)
b.D("ie17", "i12", "i11", "是", al=True); b.H("ie18", "i12", "i12p", "否"); b.LU("ie16f", "i11", "i11f", "寫", tx=0.5); b.D("ie19d", "i11", "ig", al=True)
b.H("ie7f", "i7", "i11f", "寫")
b.RD("ie20", "ig", "ign", "無"); b.D("ie21", "ig", "igs", "有", al=True)
b.H("ie20f", "ign", "igyf", "寫")
b.H("ie21s", "igs", "igsp", "是"); b.D("ie21sn", "igs", "igq0", "否", al=True)
b.H("ie21y", "igq0", "igq0p", "是"); b.D("ie21n", "igq0", "igq", "否", al=True)
b.H("ie22", "igq", "igqp", "否"); b.D("ie23", "igq", "igy", "是", al=True); b.LU("ie23f", "igy", "igyf", "寫", tx=0.5)
b.D("ie23m", "igy", "igm", al=True); b.H("ie23mf", "igm", "igmf", "寫")
b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
b.D("ie25", "idl", "iz", "", 0.5, 0.5)
b.close()
_A = F.abs
def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
    sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    tot = (sx0 - busx) + (gy - ey) + (nx - busx) + 10
    p5cc.append(_edge(eid, s, t, label, (0, 0.5), (round(tx, 3), 0), [(busx, ey), (busx, gy), (nx, gy)], 2 * (14 / tot) - 1 if label else None, "below" if label else None))
def _ub(eid, s, t, tx, busx=1610):   # 右車道「建檔」格 → 頂端出 → 上方縫隙 → 右匯流排 → 目標上方縫隙 → 目標頂端（避開同列檔案框與 LU 寫線）
    sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ex = sx0 + sw / 2; gyu = F.rt[s] - F.gap / 2; gyt = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
    p5cc.append(_edge(eid, s, t, "", (0.5, 0), (round(tx, 3), 0), [(ex, gyu), (busx, gyu), (busx, gyt), (nx, gyt)], None))
_ub("ie13", "i7", "ig", 0.5); _ub("ie20z", "ign", "idl", 0.95)
_lb("ie8", "i5", "ig", "是：不碰根 justfile", 0.5)
for _s in ("i6sp", "i8p", "i12p"): _lb(f"{_s}_l", _s, "ig", "", 0.5)
for _s in ("igsp", "igq0p", "igqp"): _lb(f"{_s}_l", _s, "idl", "", 0.1)
tty(F, p5cc, "i12", "igq")
foot(p5cc, "p5cc", F.y, [t for t in T5I if t[0].startswith(("install 進度檔",))] + [
 ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
 ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
 ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
 ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
 E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)

b.close()
bypass(F, p5bp, "ce12y", "c9a", "c9b")
footer_edges(F, [("ce15", "c11b", "不同", "l", "c11x")])
foot(p5bp, "p5bp", F.y, _t5b("stdout", "/dist/<repo>", "dest 撞名", "命名空間", "6-26", "6-12", "resolve 非 0") + [PULLX_T], ALL - {"inv", "pend", "tree"} | {"entry"})
addpage("v1p5bcc", "流程 v2：add（1′）apply 前置", p5bp)

# ================= P5bc：add（2）apply 寫入段 =================
p5bc, F = newpage("流程 v2：add <repo>（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4、v2.16-10）", "", COLS5)
b = F.band("bB2", "5b″ add <repo> apply 寫入段（承「add（1′）」頁：檢查通過、非 dry-run）：進度檔 → 取件 → 印記 → 初始檔逐檔到暫存 → 原子替換 → 基準版 → metadata → tools.just → version.toml → 刪進度檔；任一寫入失敗 → 共通匯流 → 1", v2=True)
b.box("c13c", E, 0, ENTRY, "來自「add（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)
b.box("c15a", E, 1, v2(SUB), fl("建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）"), 400)
b.box("c15af", P, 1, F12, "＋baseline/<repo>/.vendor_kit.toml（[progress] state=in-progress、started、verb、id=trace_id、done、pending）", 360)
b.box("c15", E, 2, v2(SUB), fl("取件（fetch）：/dist/<repo> 複製到暫存目錄"), 400)
b.box("c15c", E, 3, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("c15f", P, 3, F12, "＋cache/<repo>/（不進 git）", 360)
b.box("c15b", E, 4, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("c15bf", P, 4, F12, "＋gen/<repo>.stamp（不進 git）", 360)
b.box("cl", E, 5, LBL, "↓ 初始檔逐檔（init.toml 每個 [[file]]；範本讀 /dist/<repo>；結果先放暫存）", 300, 24, ax="r", minh=24)
b.box("c16", E, 6, D12, "初始檔已存在？", 200, ax="l")
b.box("c17", E, 6, SUB, "無：建該檔到暫存（state=managed）", 150, ax="r")
b.box("cr", P, 6, v2(RULE), fl("復原（v2.2 C、v2.5 §3）：進度檔第一個寫入前建、最後一步刪；初始檔全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復"), 360)
b.box("c18", E, 7, v2(D12), "strategy = append？", 200, ax="l")
b.box("c19", E, 7, SUB, fl("否：不納管（state=unmanaged）、不覆蓋，印 6-11「已存在，範本在 cache」"), 180, ax="r")
b.box("c20q", E, 8, v2(D12), "問 6-21「要在 X 加這幾行嗎」同意？（-y 免問）", 320, ax="l")
b.box("c20n", E, 10, v2(SUB), fl("否：不寫；state=unmanaged 只記 declined_hash"), 150, ax="l")
b.box("c20", E, 10, SUB, fl("是：append 那幾行到暫存副本（state=appended；實際插入的行之後記進 metadata）"), 200, ax=180)
b.box("c20l", E, 11, v2(D12), "還有下一個 [[file]]？", 320, ax=40)
b.box("c20w", E, 12, v2(SUB), fl("否：初始檔逐檔原子替換（暫存 → 正式位置；只有要建／要 append 的檔）"), 400)
b.box("c20wf", P, 12, F12, "＋初始檔（init.toml 的 dest；append 的檔只多那幾行）", 360)
b.box("c21", E, 13, SUB, "寫 baseline/<repo>/（範本副本）", 400)
b.box("c21f", P, 13, F12, "＋baseline/<repo>/（進 git）", 360)
b.box("c21b", E, 14, v2(SUB), fl("寫 metadata：source（來源 ref@digest = 最後合併版本）"), 400)
b.box("c21bf", P, 14, F12, "＋baseline/<repo>/.vendor_kit.toml（source；進 git）", 360)
b.box("c21b2", E, 15, v2(SUB), fl("寫 metadata：local_image_id（只在 --local tar 時；離線對照）"), 400)
b.box("c21b2f", P, 15, F12, ".vendor_kit.toml（local_image_id = 本機 image ID ↔ index digest）", 360)
b.box("c21c", E, 16, v2(SUB), fl("寫 metadata：每個 dest 的 state（managed／appended／unmanaged；add 不問「要建嗎」，故無 declined）"), 400)
b.box("c21cf", P, 16, F12, ".vendor_kit.toml（[[file]] 各 dest 的 state）", 360)
b.box("c21c2", E, 17, v2(SUB), fl("寫 metadata：declined_hash（append 被拒那版 N 的 hash）、lines（append 實際插入的行）"), 400)
b.box("c21c2f", P, 17, F12, ".vendor_kit.toml（[[file]] 各 dest 的 declined_hash／lines）", 360)
b.box("c21d", E, 18, v2(SUB), "寫 metadata：完成標記（complete = true）", 400)
b.box("c21df", P, 18, F12, ".vendor_kit.toml（complete = true）", 360)
b.box("c22", E, 19, v2(SUB), fl("重生 gen/tools.just（每個 <ns>.just 一行 mod?；原子替換，與本次 cache/ 同一 apply 內，I17）"), 400)
b.box("c22f", P, 19, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("c23", E, 20, v2(SUB), fl("最後寫 version.toml [tools] 版本鎖定行：<repo> = \"…:<tag>@sha256:…\""), 400)
b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
b.D("ce28n", "c20q", "c20n", "否", 0.25, 0.5, al=True); b.D("ce28y", "c20q", "c20", "是", 0.8, 0.5, al=True)
b.R("ce29", "c17", "c20l", "", busx=990, tx=0.5); b.R("ce30", "c19", "c20l", "", busx=990, tx=0.5); b.D("ce31", "c20", "c20l", al=True); b.D("ce31n", "c20n", "c20l", al=True)
b.LL("ce31y", "c20l", "c16", "是", busx=565); b.D("ce31l", "c20l", "c20w", "否", al=True)
b.H("ce31w", "c20w", "c20wf", "寫"); b.D("ce31z", "c20w", "c21")
b.H("ce32", "c21", "c21f", "寫"); b.D("ce32b", "c21", "c21b"); b.H("ce32f", "c21b", "c21bf", "寫"); b.D("ce32b2", "c21b", "c21b2"); b.H("ce32b2f", "c21b2", "c21b2f", "寫")
b.D("ce32c", "c21b2", "c21c"); b.H("ce32cf", "c21c", "c21cf", "寫"); b.D("ce32c2", "c21c", "c21c2"); b.H("ce32c2f", "c21c2", "c21c2f", "寫")
b.D("ce32d", "c21c2", "c21d"); b.H("ce32df", "c21d", "c21df", "寫"); b.D("ce33", "c21d", "c22"); b.H("ce34", "c22", "c22f", "寫"); b.D("ce35", "c22", "c23")
b.H("ce36", "c23", "c23f", "寫"); b.D("ce37", "c23", "c23b"); b.H("ce37f", "c23b", "c23bf", "刪")
b.close()
tty(F, p5bc, "c20q")
failbus(F, p5bc, ["c15a", "c15c", "c15b", "c20w", "c21", "c21b", "c21b2", "c21c", "c21c2", "c21d", "c22", "c23", "c23b"], "c23x")
footer_edges(F, [("ce39", "c23b", "", "d", "c24")])
foot(p5bc, "p5bc", F.y, _t5b("/dist/<repo>", "strategy", "dest 撞名", "續作", "gen／mod?", "CRLF", "6-38") + [E4_T], ALL - {"inv", "pend", "tree"} | {"entry", "tty"})
addpage("v1p5bc", "流程 v2：add（2）apply 寫入段", p5bc)

# ================= P6：sync（1）第 1 段 resolve =================
T6 = [
 ("快路徑（Q22、§3.6）", "啟動器只用 grep 比對：gen/.stamp 第一行 == 引擎 ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；每個 cache/<repo>/ 存在（目錄或 symlink）；gen/tools.just 存在；非 CI 模式；sync 無參數。全相符 → 不起容器、0（執行紀錄寫 sync_fast_path）；否則起引擎 resolve sync"),
 ("待辦清單／apply|no", "resolve sync 在引擎內算待辦（要拉哪些 image、要重裝什麼、要不要重生 tools.just）；stdout 只傳 extract 清單、指紋、apply|yes／no；無待辦 → apply|no，啟動器驗完文法直接 0、不起第二個容器"),
 ("6-9（專案根）", "vendor_kit 動詞只准在專案根執行（recipe 檢查 invocation_directory() == justfile_directory()），否則 1 印 6-9「請到 <dir> 執行」；sync 也適用：工具 recipe 的 _sync 先 cd 到專案根再呼叫 sync；此檢查不寫檔，在建執行紀錄之前"),
def _t7(*keep): return [t for t in T7 if t[0].startswith(keep)]
DEST_T = [t for t in T5B if t[0].startswith(("dest 撞名",))] + [("命名空間撞名（upgrade）", "新版 dist/just/<ns>.just 的 <ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（以 just --dump --dump-format json 取得）(c) 保留名 vendor_kit 相同 → upgrade 回 1 拒絕（撞名整個 just 會掛）")]
N7 = ""
p7, F = newpage("流程 v2：upgrade ── A. Renovate 路徑（§2／§7、v2.2 D、v2.3 §7、v2.5 §1／§7、v2.16-15）", "", COLS7)
b = F.band("uA", "A. Renovate 路徑（下游自選，vendor_kit 不出 bot）：機器人只改 version.toml 一行；PR 的 CI 以新版跑完整流程（⓪～⑤，第一個失敗即停、原碼傳出）；基準版落後 → PR 紅（需人補合併）；補合併在 PR 分支上完成、CI 綠後才 merge", v2=True)
b.box("a0", RN, 0, G12, "Renovate 定期查 GHCR", 160)
b.box("a1", G, 0, IMG, "<repo>-dist\n出新 tag@digest", 180)
b.box("a2", RN, 1, W12, "開 PR（獨立分支）：只改 version.toml 該工具的版本鎖定行（tag@digest）", 160)
b.box("a3", P, 1, F12, "version.toml（PR 分支）\n<repo> 版本鎖定行 = 新 tag@digest", 280)
b.box("a4a", L, 2, W12, "PR 的 CI 呼叫 .vendor_kit/ci/check.sh（以新版跑完整流程；每個動詞各自一份執行紀錄）", 220)
b.box("a4r", E, 2, RULE, "只看一行 diff 不足以證明升級可用（該行仍可能不合法或指向不存在的 ref）\n→ PR 的 CI 必須以新版跑完整流程", 360)
b.box("a4b0", L, 3, v2(W12), fl("check.sh ⓪：git ls-files 拒絕被納管的 version.local.toml（納管 → 1 停）"), 220)
b.box("a4b", L, 4, W12, "check.sh ①：sync（CI 模式；export CI=1）", 220)
b.box("a5", U, 5, v2(O12), fl("1 → PR 紅：需人處理（常見：基準版落後 6-5 → 本機 upgrade <repo> -y 後 push）"), 220)
b.box("a4q", E, 5, v2(D12), fl("sync 通過？（基準版落後 6-5／薄殼不符 6-1／未完成接入 6-13／本機覆寫／未完成交易 6-33；見「sync（1′）」頁）"), 360)
b.box("a4c", L, 6, W12, "是：check.sh ②：verify", 220)
b.box("a4d", L, 7, W12, "check.sh ③：upgrade --dry-run", 220)
b.box("a4e1", L, 8, W12, "check.sh ④：工具測試", 220)
b.box("a6a", U, 8, v2(W12), "PR 作者本機：切到 PR 分支", 220)
b.box("a9", P, 8, NOTE, fl("Renovate 預設不動有人推過的分支；PR body 加警告：勿勾 rebase（會蓋掉人補的合併 commit）。vendor_kit 無 bot。"), 280)
b.box("a4e2", L, 9, W12, "check.sh ⑤：專案測試", 220)
b.box("a6b", U, 9, v2(W12), fl("upgrade <repo> -y（走「B. 手動路徑（1）」頁，固定補到 PR 鎖定版）"), 220)
b.box("a4fx", G, 10, v2(O12), fl("PR 紅：②～⑤ 一關過才下一關，第一個失敗即停止；整體結束碼 = 該步的碼原樣傳出（1／2／3 或工具測試自己的碼）"), 180)
b.box("a4f", E, 10, v2(D12), "②～⑤ 任一步非 0？", 300)
b.box("a6c", U, 10, W12, "commit（合併結果）", 220)
b.box("a6d", U, 11, W12, "push 到 PR 分支", 220)
b.box("a7", L, 11, W12, "PR 分支 CI 再跑完整流程（同上）", 150, ax="l")
b.box("a8qx", G, 12, v2(O12), fl("PR 紅：修到綠再 merge"), 180)
b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
b.box("a8", RN, 13, G12, "是：merge PR", 180)
b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
b.close()
foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)

# ================= P7c：upgrade ── B. 手動路徑（1）resolve =================
p7c, F = newpage("流程 v2：upgrade ── B. 手動路徑（1）執行紀錄 → 偵測進度檔 → resolve（§2、v2.16-12）", "", COLS7)
b = F.band("uB", "B. 手動路徑：upgrade <repo>[@<tag>]（單一工具；不帶 repo 見「E. 升引擎 (a)(b)」頁）= 執行紀錄 → 偵測進度檔 → resolve（不寫；無憑證 → 6-3；目標 == 現版且無待合併 → apply|no 0）；三叉與 docker 段見「B（1′）」頁", v2=True)
b.box("b0", U, 0, G12, "just vendor_kit upgrade <repo>[@<tag>]（-y…）", 220)
lstart(b, "b0l", "b0x", 0, "upgrade", w=240, xw=180)
preseg(b, "b", 2, "b1", "upgrade", w=240)
b.box("b15bf", P, 2, F12, "baseline/<repo>/.vendor_kit.toml（source；進 git）", 280)
b.box("b15c", E, 3, v2(SUB), fl("寫 metadata：conflicts（有衝突標記或解析失敗的 dest 清單）"), 360)
b.box("b15cf", P, 3, F12, ".vendor_kit.toml（conflicts）", 280)
b.box("b15d", E, 4, v2(SUB), fl("寫 metadata：每個 dest 的 state／declined_hash／lines —— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined"), 360)
b.box("b15df", P, 4, F12, ".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）", 280)
b.box("b15g", E, 5, v2(SUB), fl("重生 gen/tools.just（新版的 just/<ns>.just 可能增減；原子替換，與本次 cache 同一 apply 內，I17）"), 360)
b.box("b15gf", P, 5, F12, "gen/tools.just（不進 git；mod? 行）", 280)
b.box("b16q0", E, 6, v2(D12), "待合併（version.toml 已是目標版 B）？", 300, ax="l")
b.box("b16", E, 7, v2(SUB), fl("否：寫 version.toml <repo> 版本鎖定行 → 目標 tag@digest（最後寫）"), 360)
b.box("b16f", P, 7, F12, "version.toml（<repo> 版本鎖定行，進 git）", 280)
b.box("b16b", E, 8, v2(SUB), "成功（以上寫入都已落盤）：刪進度檔 metadata [progress]（最後一步）", 360)
b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
b.D("be23", "b15z", "b15a", al=True)
b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
b.D("be24c", "b15b", "b15c"); b.H("be24cf", "b15c", "b15cf", "寫"); b.D("be24d", "b15c", "b15d"); b.H("be24df", "b15d", "b15df", "寫")
b.D("be25", "b15d", "b15g"); b.H("be25f", "b15g", "b15gf", "寫"); b.D("be25q", "b15g", "b16q0", al=True); b.D("be25g", "b16q0", "b16", "否", al=True); b.H("be27", "b16", "b16f", "寫")
b.D("be26", "b16", "b16b"); b.H("be26f", "b16b", "b16bf", "刪")
b.D("be28q", "b16b", "b16q", al=True); b.H("be29", "b16q", "b18", "是")
b.close()
sidebus(F, p7cq, "be25y", "b16q0", "b16b", "是：已是 B，不動", busx=730, tx=0.15)
failbus(F, p7cq, ["b15a", "b15b", "b15c", "b15d", "b15g", "b16", "b16b"], "b16x")
footer_edges(F, [("be28", "b16q", "否", "d", "b17")])
foot(p7cq, "p7cq", F.y, _t7("基準版落後", "gen／mod?", "git merge-file", "6-14", "6-6") + [("解析失敗（基準版）", "合併結果是 TOML／just 等可解析格式卻解析失敗 → 只該檔留原檔、記 conflicts、其基準版留上一版不推；結束碼 2")], ALL - {"inv", "tree", "pend", "note"} | {"entry"})
addpage("v1p7cccc", "流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入", p7cq)

# ================= P7b：upgrade ── C. 逐檔判斷狀態機、C′ 衝突重入 =================
T7B = [
 BDN_T,
 ("逐檔判斷（狀態機）", "upgrade apply 對 init.toml 每個 [[file]] 與 metadata 每個 dest，依 metadata state（managed／appended／declined／unmanaged／deleted／metadata 無此 dest = 新版新增）分流，每檔恰走一條路：結果 = 不動／warn（不問）或問 6-22；在 apply 內、拿到 flock、建進度檔後（「B（2）」頁）"),
 FIP_T,
 GM_T,
 ("衝突重入（v2.2 D (0)）", "再跑 upgrade 時 resolve 先看 metadata 的 conflicts：檔內仍有我們的標籤 → 2 停；檔案失蹤不算已解；都乾淨 → apply 拿鎖、建進度檔後清除狀態再往下"),
 ("append 行／CRLF", "strategy=append 的初始檔：upgrade 找上次插入的行（CRLF = Windows 換行 \\r\\n，與 LF 視為相同；其餘精確）→ 唯一命中才問替換；零命中或多處 → 保留只 warn、印新內容"),
 ("二進位檔", "不是文字的檔（symlink 同）；不做行內合併：D==B（未改）→ 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過 → 保留 + warn，不進三方合併；dist/files/ 第一版禁止 symlink"),
 ("回退／git revert", "git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、基準版同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 把 cache/<repo>/ 換回舊版、重生 tools.just（見「D. 回退」頁）"),
 ("declined／declined_hash／6-6／6-7／6-8", "state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256）；N 的 hash == declined_hash → 不再問（dry-run／check.sh 印 6-6「有 N 個範本你拒絕過」）；≠ → 再問；unmanaged → 不動（6-7「<X> 沒納管」提醒）；6-8「<Y> 你拒絕過，<vZ> 有新版」"),
 ("6-11（已有同名檔）", "新版新增的 dest 已存在 → 不納管（state=unmanaged）、不問、印「<X> 已存在，未納管；範本在 .vendor_kit/cache/<repo>/files/ 可自行比對」"),
b.box("m9q", E, 3, v2(D12), fl("有 → 問 6-21「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）"), 300, ax=30)
b.box("m9s", E, 4, v2(SUB), fl("是：逐行比對紀錄的每一行（CRLF／LF 視為相同、其餘精確）"), 200, ax=80)
b.box("m9mn", P, 4, v2(NOTE), fl("逐行比對（§4.3、v2.9 §5）：紀錄的每一行仍與原文相同 → 刪該行；不同／缺失 → 跳過並 warn；不是全有／全無；零命中 → 不動、印清單"), 360)
b.box("m9m", E, 5, v2(D12), "該行仍與紀錄原文相同？", 200, ax=110)
b.box("m9w", E, 6, v2(SUB), "否：跳過該行並 warn", 120, ax=140)
b.box("m9d", E, 6, SUB, "是：刪該行", 90, ax="r")
b.box("m9f", P, 6, F12, "初始檔（只移除仍相同的那幾行；其餘不動；永不刪檔）", 360)
b.box("m9l2", E, 7, v2(D12), "還有下一行？", 200, ax=110)
b.box("m10a", E, 8, v2(SUB), "否：刪 baseline/<repo>/ 內範本副本", 400, ax=-60)
b.box("m10af", P, 8, F12, "－baseline/<repo>/ 內範本副本（進 git；metadata 見下）", 360)
b.box("m10q", E, 9, v2(D12), "有拒絕刪的 append 行？", 300, ax="l")
b.box("m10k", E, 10, v2(SUB), fl("是：記孤兒 append 行到 baseline/.vendor_kit.toml（dest、行原文；仍完成移除，不留 baseline/<repo>/）"), 400)
b.box("m10kf", P, 10, v2(F12), "baseline/.vendor_kit.toml（孤兒 append 行紀錄；進 git；同 .dockerignore append 表）", 360)
b.box("m10m", E, 11, v2(SUB), "刪 metadata .vendor_kit.toml 並移除已空的 baseline/<repo>/", 400)
b.box("m10mf", P, 11, F12, "－baseline/<repo>/.vendor_kit.toml 與目錄（進 git）", 360)
b.box("m10b", E, 12, v2(SUB), fl("刪 cache/<repo>/（與下一格同一次原子替換，I17）"), 400)
b.box("m10bf1", P, 12, F12, "－cache/<repo>/（不進 git；同一次原子替換）", 360)
b.box("m10b2", E, 13, v2(SUB), fl("重生 gen/tools.just（去掉該工具所有 mod? 行；與刪 cache 同一次原子替換，I17）"), 400)
b.box("m10bf", P, 13, F12, "gen/tools.just（少 mod? 行；不進 git；同一次原子替換）", 360)
b.box("m10c", E, 14, v2(SUB), "刪 gen/<repo>.stamp", 400)
b.box("m10cf", P, 14, F12, "－gen/<repo>.stamp（不進 git）", 360)
b.box("m10e", E, 15, v2(SUB), "最後刪 version.toml 該工具的版本鎖定行", 400)
b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)
b.D("me12m", "m9s", "m9m", al=True)
b.D("me13w", "m9m", "m9w", "否", al=True); b.RD("me13d", "m9m", "m9d", "是")
b.H("me13f", "m9d", "m9f", "寫")
b.D("me14w", "m9w", "m9l2", al=True); b.D("me14d", "m9d", "m9l2", "", 0.5, 0.5)
b.LL("me14y", "m9l2", "m9m", "是", busx=600); b.D("me14n", "m9l2", "m10a", "否", 0.5, 0.5)
b.H("me15a", "m10a", "m10af", "刪"); b.D("me15q", "m10a", "m10q", "", 0.5, 0.5); b.D("me15k", "m10q", "m10k", "是", al=True); b.H("me15kf", "m10k", "m10kf", "寫")
b.D("me15m", "m10k", "m10m"); b.H("me15mf", "m10m", "m10mf", "刪")
b.D("me15b", "m10m", "m10b"); b.H("me15bf1", "m10b", "m10bf1", "刪"); b.D("me15b2", "m10b", "m10b2"); b.H("me15bf", "m10b2", "m10bf", "寫"); b.D("me15c", "m10b2", "m10c"); b.H("me15cf", "m10c", "m10cf", "刪")
b.D("me15e", "m10c", "m10e"); b.H("me15ef", "m10e", "m10ef", "刪")
b.D("me16", "m10e", "m10g"); b.H("me16f", "m10g", "m10gf", "刪")
b.close()
tty(F, p8b2, "m9q")
sidebus(F, p8b2, "me15qn", "m10q", "m10m", "否", busx=565, tx=0.15, pos=-0.6, vert="below")
failbus(F, p8b2, ["m9l", "m9d", "m10a", "m10k", "m10m", "m10b", "m10b2", "m10c", "m10e", "m10g"], "m10x")
footer_edges(F, [("me17", "m10g", "", "d", "m11")])
foot(p8b2, "p8b2", F.y, _t8b("append 行", "gen／mod?", "刪除順序", "孤兒", "6-20") + [E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
addpage("v1p8bccc", "流程 v2：remove（2）寫入段", p8b2)

# ================= P8bc：uninstall（1）=================
p8bc, F = newpage("流程 v2：uninstall（1）執行紀錄 → 偵測進度檔 → resolve → 三叉 → apply 前置（§2；v2.16）", "", COLS5)
b = F.band("vD", "uninstall（1）：全部拆掉 = 執行紀錄 → 偵測進度檔 → resolve（完整預檢 → hash → 保護清單 → 算計畫／詢問清單 → 指紋 → stdout）→ 三叉 → apply 前置（flock 逾時 6-26、重驗、argv、CI、dry-run）；寫入段見「uninstall（2）」頁", v2=True)
b.box("x0", U, 0, G12, "just vendor_kit uninstall（-y、--dry-run）", 220)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..64f8aa6c571fb456372b64e1331808d0f5ef6afc
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..8e3ec87ee0f4200b27713d49d248615039f034a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -911,7 +911,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +928,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +946,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..8e3ec87ee0f4200b27713d49d248615039f034a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -911,7 +911,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +928,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +946,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..3d375f3c5d12924c1d7a8429081ea825966f679c
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1354,6 +1356,7 @@
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
 b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1524,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2210,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..3d375f3c5d12924c1d7a8429081ea825966f679c
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1354,6 +1356,7 @@
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
 b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1524,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2210,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..b0badf97d1cbf535866aa2abac43b80fe4943cb9
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1353,7 +1355,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1524,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2210,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..b0badf97d1cbf535866aa2abac43b80fe4943cb9
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1353,7 +1355,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1524,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2210,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..2092e784100db7739aec1067e686916b0054de47
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 17, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 17, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 18, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 18, v2(R12), fl(E30X), 220)
+b.box("z2", U, 19, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 19, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 20, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "zq0", "", 0.5, 0.5)
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..2092e784100db7739aec1067e686916b0054de47
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 17, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 17, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 18, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 18, v2(R12), fl(E30X), 220)
+b.box("z2", U, 19, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 19, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 20, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "zq0", "", 0.5, 0.5)
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc 'python3 run_v1_b.py' in <scratchpad>
 succeeded in 111ms:
v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 page ('1660', '1919')
v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 page ('1660', '1311')
v1p5i 流程 v2：bootstrap.sh（1′）docker run install page ('1660', '1364')
v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add page ('1660', '1970')
v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run page ('1660', '1603')
v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 page ('1660', '1734')
v1p5cw 流程 v2：install（1″）寫入 page ('1660', '1707')
v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore page ('1660', '2014')
v1p5b 流程 v2：add（1）resolve → docker page ('1660', '2273')
v1p5bcc 流程 v2：add（1′）apply 前置 page ('1660', '2219')
v1p5bc 流程 v2：add（2）apply 寫入段 page ('1660', '2301')
v1p6 流程 v2：sync（1）啟動器快路徑 page ('1660', '2229')
v1p6cc 流程 v2：sync（1′）引擎 resolve page ('1660', '2523')
v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置 page ('1660', '1550')
v1p6cw 流程 v2：sync（2′）apply 寫入段 page ('1660', '1581')
v1p7 流程 v2：upgrade ── A. Renovate 路徑 page ('1660', '1821')
v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker page ('1660', '2363')
v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 page ('1660', '2227')
v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 page ('1660', '2394')
v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 page ('1660', '1569')
v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 page ('1660', '2371')
v1p7bd 流程 v2：upgrade ── D. 回退 page ('1660', '2142')
v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b) page ('1660', '2140')
v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 page ('1660', '1673')
v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） page ('1660', '2340')
v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） page ('1660', '1378')
v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） page ('1660', '1559')
v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml page ('1660', '2181')
v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） page ('1660', '1241')
v1p8 流程 v2：dev <repo> page ('1660', '2094')
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2296')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2115')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2385')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..2092e784100db7739aec1067e686916b0054de47
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 17, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 17, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 18, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 18, v2(R12), fl(E30X), 220)
+b.box("z2", U, 19, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 19, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 20, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "zq0", "", 0.5, 0.5)
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..7ce3c6d4e6540305cc898ed8e8e363e2ea0986a6
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..7ce3c6d4e6540305cc898ed8e8e363e2ea0986a6
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

codex
第一輪修改已落地：前引 3 條已移除、install(2) 六個寫入點已接共通紅色失敗匯流、Renovate ⓪ 有明確失敗出口、install grep 有 `≠ 1` 出口、sync 的 `apply|no` 已移到 resolve 回碼與文法檢查之後；另修正 add/remove 末段失敗敘述及 6-14 不改結束碼。現在跑完整檢查，依實際交叉／壓框結果回修。
2026-09-20T15:10:08.519684Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run.log && python3 check_overflow.py v1_b.drawio >/tmp/overflow.log && python3 check_overlap.py v1_b.drawio >/tmp/overlap.log && python3 check_cross_v1b.py v1_b.drawio >/tmp/cross.log && python3 check_self_v1b.py v1_b.drawio >/tmp/self.log && python3 check_jog_r7.py v1_b.drawio >/tmp/jog.log && python3 check_align_v1b.py v1_b.drawio >/tmp/align…162 chars truncated…"; done; rm -rf r15_b_out; python3 extract_pages.py v1_b.drawio r15_b_out >/tmp/extract.log && python3 lint_pages.py r15_b_out >/tmp/lint.log; cat /tmp/lint.log; rg -n \\\"'\\\"\\\\\\\\[(xref-forward|write-fail-edge|event-name|resolve-3way|precheck-recover|end-color-text|term-count|term-dup-page0|page-height|edge-font|merge-fanout)\\\\\\\\]\\\\\\\" r15_b_out/lint.md\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..7ce3c6d4e6540305cc898ed8e8e363e2ea0986a6
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run.log && python3 check_overflow.py v1_b.drawio >/tmp/overflow.log && python3 check_overlap.py v1_b.drawio >/tmp/overlap.log && python3 check_cross_v1b.py v1_b.drawio >/tmp/cross.log && python3 check_self_v1b.py v1_b.drawio >/tmp/self.log && python3 check_jog_r7.py v1_b.drawio >/tmp/jog.log && python3 check_align_v1b.py v1_b.drawio >/tmp/align.log; for f in /tmp/run.log /tmp/overflow.log /tmp/overlap.log /tmp/cross.log /tmp/self.log /tmp/jog.log /tmp/align.log; do echo "### $f"; tail -8 "$f"; done; python3 extract_pages.py v1_b.drawio r15_b_out >/tmp/extract.log && python3 lint_pages.py r15_b_out >/tmp/lint.log; cat /tmp/lint.log; rg -n "'"\\[(xref-forward|write-fail-edge|event-name|resolve-3way|precheck-recover|end-color-text|term-count|term-dup-page0|page-height|edge-font|merge-fanout)\\]\" r15_b_out/lint.md" in <scratchpad>
 succeeded in 1341ms:
### /tmp/run.log
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2296')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2115')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2385')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')
### /tmp/overflow.log
   無
== v1p8bccc 流程 v2：remove（2）寫入段
   無
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
### /tmp/overlap.log
   無
== v1p8bccc 流程 v2：remove（2）寫入段
   無
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 1 筆
### /tmp/cross.log
tail: cannot open '/tmp/cross.log' for reading: No such file or directory
### /tmp/self.log
tail: cannot open '/tmp/self.log' for reading: No such file or directory
### /tmp/jog.log
tail: cannot open '/tmp/jog.log' for reading: No such file or directory
### /tmp/align.log
tail: cannot open '/tmp/align.log' for reading: No such file or directory
頁數 38；條目 340（warn 121、info 219）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 36 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 120 | 37 |
| onething | 0 | 90 |
| event-name | 0 | 0 |
→ r15_b_out/lint.md, lint.json
160:- [page-height][warn] p6r_tk3: 頁高 2415 > 2400（最低格 p6r_tk3「完成標記／基準版落後」）

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..7ce3c6d4e6540305cc898ed8e8e363e2ea0986a6
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc "rg -n -B3 -A3 \"共 1 筆|OVERLAP|重疊|v1p\" /tmp/overlap.log | tail -30; sed -n '1,220p' /tmp/overlap.log | rg -v '"'^   無$|''^=='"'" in <scratchpad>
 succeeded in 0ms:
48-   無
49:== v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
50-   無
51:== v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
52-   無
53:== v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
54-   無
55:== v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
56-   無
57:== v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
58-   無
59:== v1p8 流程 v2：dev <repo>
60-   無
61:== v1p8ccc 流程 v2：dev vendor_kit
62-   無
63:== v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置
64-   無
65:== v1p8cx 流程 v2：undev <repo>（2）寫入段
66-   無
67:== v1p8cc 流程 v2：undev vendor_kit
68-   無
69:== v1p8b 流程 v2：remove（1）resolve → apply 前置
70-   無
71:== v1p8bccc 流程 v2：remove（2）寫入段
72-   無
73:== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
74-   無
75:== v1p8bcc 流程 v2：uninstall（2）寫入段
76-   無
77:共 1 筆
   ae4b0x (a4b0→a5) 壓到 a5_v2「v2」 ['L1']
共 1 筆

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..7ce3c6d4e6540305cc898ed8e8e363e2ea0986a6
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,7 +1234,9 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
@@ -1238,9 +1246,9 @@
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,7 +1361,8 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.H("ae4b0x", "a4b0", "a5", "納管：1 停"); b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
@@ -1521,7 +1530,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2216,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..a4d03793efddb656326fe3852510fe579cee2c58
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 20, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..a4d03793efddb656326fe3852510fe579cee2c58
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 20, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run.log; python3 check_overflow.py v1_b.drawio > /tmp/overflow.log; python3 check_overlap.py v1_b.drawio > /tmp/overlap.log; python3 check_cross_v1b.py v1_b.drawio > /tmp/cross.log; python3 check_self_v1b.py v1_b.drawio > /tmp/self.log; python3 check_jog_r7.py v1_b.drawio > /tmp/jog.log; python3 check_align_v1b.py v1_b.drawio > /tmp/align.log; for f in overflow overlap cross self jog align; do echo "### $f"; tail -3 "/tmp/$f.log"; done; python3 extract_pages.py v1_b.drawio r15_b_out >/tmp/extract.log; python3 lint_pages.py r15_b_out >/tmp/lint.log; cat /tmp/lint.log; rg -n "'"\\[(xref-forward|write-fail-edge|event-name|resolve-3way|precheck-recover|end-color-text|term-count|term-dup-page0|page-height|edge-font|merge-fanout)\\]\" r15_b_out/lint.md || true" in <scratchpad>
 succeeded in 2036ms:
### overflow
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
### overlap
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
### cross
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 2 筆
### self
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 3 筆
### jog
共 0 筆
### align
   無
== 流程 v2：uninstall（2）寫入段
   無
頁數 38；條目 339（warn 120、info 219）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 36 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 120 | 37 |
| onething | 0 | 90 |
| event-name | 0 | 0 |
→ r15_b_out/lint.md, lint.json

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..a4d03793efddb656326fe3852510fe579cee2c58
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 20, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc "rg -n -v '"'^==|''^   無$|''^共'"' /tmp/cross.log /tmp/self.log" in <scratchpad>
 succeeded in 0ms:
/tmp/self.log:10:   ie1gx: 標籤寬 22 ≥ 兩端距離 20「≠ 1」
/tmp/self.log:26:   頁高 2435 > 2400
/tmp/self.log:32:   ae4b: 標籤寬 36 ≥ 兩端距離 20「未納管」
/tmp/cross.log:16:   ie16f × fb_i7 at ((1420.0, 770.0),(1420.0, 720.0)) / ((1056.0, 739.0),(1610.0, 739.0))
/tmp/cross.log:17:   ie23f × fb_ign at ((1420.0, 1310.0),(1420.0, 1006.0)) / ((1056.0, 1016.0),(1610.0, 1016.0))

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..a4d03793efddb656326fe3852510fe579cee2c58
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 20, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc "sed -n '1,40p' /tmp/self.log" in <scratchpad>
 succeeded in 0ms:
== v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
   無
== v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
   無
== v1p5i 流程 v2：bootstrap.sh（1′）docker run install
   無
== v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
   無
== v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run
   ie1gx: 標籤寬 22 ≥ 兩端距離 20「≠ 1」
== v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
   無
== v1p5cw 流程 v2：install（1″）寫入
   無
== v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore
   無
== v1p5b 流程 v2：add（1）resolve → docker
   無
== v1p5bcc 流程 v2：add（1′）apply 前置
   無
== v1p5bc 流程 v2：add（2）apply 寫入段
   無
== v1p6 流程 v2：sync（1）啟動器快路徑
   無
== v1p6cc 流程 v2：sync（1′）引擎 resolve
   頁高 2435 > 2400
== v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置
   無
== v1p6cw 流程 v2：sync（2′）apply 寫入段
   無
== v1p7 流程 v2：upgrade ── A. Renovate 路徑
   ae4b: 標籤寬 36 ≥ 兩端距離 20「未納管」
== v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
   無
== v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
   無
== v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
   無
== v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
   無

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..a4d03793efddb656326fe3852510fe579cee2c58
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx", "≠ 1"); b.D("ie1g", "i1g", "i1i", "= 1", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i7", "i11", "ign", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 20, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", "未納管", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run.log; for f in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py; do python3 "$f" v1_b.drawio > "/tmp/${f%.py}.log"; echo "$f: $(tail -1 "/tmp/${f%.py}.log")"; done; python3 extract_pages.py v1_b.drawio r15_b_out >/tmp/extract.log; python3 lint_pages.py r15_b_out >/tmp/lint.log; cat /tmp/lint.log; rg -n "'"\\[(xref-forward|write-fail-edge|event-name|resolve-3way|precheck-recover|end-color-text|term-count|term-dup-page0|page-height|edge-font|merge-fanout)\\]\" r15_b_out/lint.md || true" in <scratchpad>
 succeeded in 2260ms:
check_overflow.py: 共 0 筆
check_overlap.py: 共 0 筆
check_cross_v1b.py: 共 0 筆
check_self_v1b.py: 共 0 筆
check_jog_r7.py: 共 0 筆
check_align_v1b.py:    無
頁數 38；條目 339（warn 120、info 219）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 36 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 120 | 37 |
| onething | 0 | 90 |
| event-name | 0 | 0 |
→ r15_b_out/lint.md, lint.json

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

exec
/usr/bin/bash -lc "tail -10 /tmp/check_align_v1b.log; rg -n \"共 [1-9][0-9]* 筆\" /tmp/check_align_v1b.log || true; rg -n \"\\[warn\\]\" r15_b_out/lint.md | rg -v '\\[termcov\\]' || true; git diff -- disc_v1_b.py 2>/dev/null || true" in <scratchpad>
 succeeded in 0ms:
== 流程 v2：undev vendor_kit
   無
== 流程 v2：remove（1）resolve → apply 前置
   無
== 流程 v2：remove（2）寫入段
   無
== 流程 v2：uninstall（1）resolve → apply 前置
   無
== 流程 v2：uninstall（2）寫入段
   無

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

codex
完整工具鏈現在已恢復為：overflow／overlap／cross／self／jog 全部「共 0 筆」，align 逐頁皆「無」；lint 的非 termcov warn 也已是 0（剩下 120 條全部是允許忽略的 termcov）。我正做最後差異核對；`implement` 技能要求收尾做 code review，但此工作目錄不是 Git repository，因此無法建立 commit 或用 commit/merge-base 做標準差異審查，我會改用檔案範圍與生成結果核對。
exec
/usr/bin/bash -lc "sed -n '1,220p' /home/cyc/.agents/skills/code-review/SKILL.md; python3 -m py_compile disc_v1_b.py; rg -n \"launcher_started|launcher_completed|launcher_failed|engine_started|engine_completed|engine_failed\" disc_v1_b.py || true; sed -n '1,40p' /tmp/run.log; stat -c '%n %s bytes' disc_v1_b.py v1_b.drawio r15_b_out/lint.md" in <scratchpad>
 succeeded in 0ms:
---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent for both.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full — the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
367:#    只留啟動器起點「建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38）」一格，其失敗畫紅出口；終點直接接各自分支（footer()/footer_edges() 重寫：無匯流）。
384: (r"launcher_started", "launcher_start"), (r"engine_started", "engine_start"),                      # v2.16-3：事件名回歸 spec §4.10 註冊表
385: (r"launcher_completed\|failed", "launcher_exit"), (r"engine_completed\|failed", "engine_exit"),
v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 page ('1660', '1919')
v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 page ('1660', '1311')
v1p5i 流程 v2：bootstrap.sh（1′）docker run install page ('1660', '1364')
v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add page ('1660', '1970')
v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run page ('1660', '1603')
v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 page ('1660', '1734')
v1p5cw 流程 v2：install（1″）寫入 page ('1660', '1707')
v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore page ('1660', '2014')
v1p5b 流程 v2：add（1）resolve → docker page ('1660', '2273')
v1p5bcc 流程 v2：add（1′）apply 前置 page ('1660', '2219')
v1p5bc 流程 v2：add（2）apply 寫入段 page ('1660', '2301')
v1p6 流程 v2：sync（1）啟動器快路徑 page ('1660', '2229')
v1p6cc 流程 v2：sync（1′）引擎 resolve page ('1660', '2395')
v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置 page ('1660', '1550')
v1p6cw 流程 v2：sync（2′）apply 寫入段 page ('1660', '1581')
v1p7 流程 v2：upgrade ── A. Renovate 路徑 page ('1660', '1821')
v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker page ('1660', '2363')
v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 page ('1660', '2227')
v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 page ('1660', '2394')
v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 page ('1660', '1569')
v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 page ('1660', '2371')
v1p7bd 流程 v2：upgrade ── D. 回退 page ('1660', '2142')
v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b) page ('1660', '2140')
v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 page ('1660', '1673')
v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） page ('1660', '2340')
v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） page ('1660', '1378')
v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） page ('1660', '1559')
v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml page ('1660', '2181')
v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） page ('1660', '1241')
v1p8 流程 v2：dev <repo> page ('1660', '2094')
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2296')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2115')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2385')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')
disc_v1_b.py 262363 bytes
v1_b.drawio 1801373 bytes
r15_b_out/lint.md 45799 bytes

diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

codex
已修改 [disc_v1_b.py](<scratchpad>/disc_v1_b.py)，並重新產生 `v1_b.drawio`。

修改頁面：

- `v1p5i`：移除三個向後引用。
- `v1p5ccc`：docker 段改成單一子流程描述，清除 onething 問題。
- `v1p5c`：補 install 引擎版本鎖定行命中 `≠ 1` 的紅色出口。
- `v1p5cc`：補寫入／刪進度檔共通失敗匯流；移除第 0 頁已有的 symlink 名詞。
- `v1p5bc`：修正刪進度檔失敗後「版本鎖定行不動」的不實敘述。
- `v1p6cc`：resolve 回碼、文法、`apply|no` 改為正確順序。
- `v1p6c`：入口改成承接前頁已驗證完成的三叉結果。
- `v1p7`：Renovate check.sh ⓪ 補「納管 → 1 停」出口。
- `v1p7cccc`：6-14 改為提醒、不改結束碼。
- `v1p8bccc`：修正後段失敗終點對版本鎖定行狀態的描述。

「待處理問題」便條：未新增。

檢查結果：

- `run_v1_b.py`：成功，38 頁。
- `check_overflow.py`：共 0 筆。
- `check_overlap.py`：共 0 筆。
- `check_cross_v1b.py`：共 0 筆。
- `check_self_v1b.py`：共 0 筆。
- `check_jog_r7.py`：共 0 筆。
- `check_align_v1b.py`：所有頁皆「無」。
- `lint_pages.py`：非 termcov warn 為 0；剩餘 120 條均為 termcov。
- Python 語法編譯：通過。
- 最大頁高 2395，頁寬 1660。

此 scratchpad 不是 Git repository，因此無法依 `implement` 技能建立 commit 或執行基於 merge-base 的 code review。
diff --git a/disc_v1_b.py b/disc_v1_b.py
index a10acdcc414f01c519f74192d5065da0df9f037f..205b5b4902f87f6d0ad1d49b56e4a3537e581944
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -720,11 +720,11 @@
 
 # ================= P5i：bootstrap.sh（1′）install =================
 p5i, F = newpage("流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.13 P4／P5、v2.16-5）", "", COLS5B)
-b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）」頁起四頁）→ 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
+b = F.band("bA1", "5a′ bootstrap.sh 中段（承「bootstrap.sh（1″）」頁：引擎 image 已在本機）：docker run <引擎> install 子流程 → 回 0 → 續「bootstrap.sh（2）」頁；回 3 → 3 原碼傳出（零寫入）；回 1 → 清半成品 → 需人處理（橙）或失敗（紅）", v2=True)
 b.box("a9e0", L, 0, ENTRY, "來自「bootstrap.sh（1″）」頁：引擎 image 已在本機、LABEL 最低介面版檢查通過（已寫 launcher_start）", 320)
 b.box("a9", L, 1, v2(W12), fl("docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）"), 300)
-b.box("a9e", E, 1, SUB, fl("執行 install（詳見「install（1）」頁起四頁）"), 240)
-b.files("a9f", P, 1, "install 寫（見「install（1）」頁起四頁）", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
+b.box("a9e", E, 1, SUB, fl("執行 install 子流程"), 240)
+b.files("a9f", P, 1, "install 寫入集合", ["薄殼五檔（含 log.sh）", "version.toml 版本鎖定行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep（VK 自產）", "config.toml（預設值）", "baseline/ vendor_kit/ config.toml（基準版副本）", "baseline/ .vendor_kit.toml（metadata）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)
 b.box("a9q", L, 2, D12, "install 回 0？", 220)
 b.box("a9z", E, 2, ENTRY, "是：續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 240)
 b.box("a9x3", U, 3, v2(O12), fl("3：install 回 3 原碼傳出（6-18 最低介面版；零寫入、無半成品）"), 220)
@@ -752,7 +752,7 @@
 b.box("a10r", L, 4, v2(W12), "docker run <引擎> resolve add <repo>", 300)
 b.box("a10re", E, 4, SUB, fl("resolve add（不寫任何檔；見「add（1）」頁）"), 240)
 res3(b, "a10r", 5, "a10d", w=300)
-b.box("a10d", L, 7, v2(W12), fl("是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）"), 300)
+b.box("a10d", L, 7, v2(W12), fl("是：執行 add（1′）頁的啟動器 docker 段"), 300)
 b.box("a10g", G, 7, IMG, "<repo>-dist@digest\n（下游 image）", 180)
 b.box("a10a", L, 8, v2(W12), "docker run <引擎> apply add <repo>", 300)
 b.box("a10ae", E, 8, SUB, fl("apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）」頁與「add（2）」頁）"), 240)
@@ -796,13 +796,14 @@
 lstart(b, "i0l", "i0x", 3, "install", w=240, pre="否：")
 preseg(b, "i", 5, "i1g", "install")
 b.box("i1g", L, 6, v2(W12), fl("grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；第一次 = bootstrap.sh 給的 ref）"), 280)
+b.box("i1gx", U, 6, v2(R12), fl("1：vendor_kit 版本鎖定行命中 ≠ 1（列差異，不動）"), 220)
 pullseg(b, 7, ("i1i", "i1p", "i1gi"), ("docker image inspect：本機有？", "無：docker pull <引擎 ref>", "vendor_kit:vN@sha256:…\n（引擎 image）"), ("i1", W12, "docker run <引擎> install …\n（啟動器不鎖；鎖在引擎）"), w=(260, 200, 280))
 b.box("i1px", U, 8, v2(R12), fl("1 + 6-24／6-31：引擎 image 拉不到／逾時"), 220)
 b.box("i4a", E, 9, v2(SUB), "flock 專案目錄（60 秒）", 400)
 b.box("i4ax", G, 9, v2(R12), fl(E26X), 200)
 b.box("i4z0", E, 10, ENTRY, "續「install（1′）」頁：薄殼已存在？→ 比對上次產物 → 進度檔 → 產薄殼到暫存", 400)
 b.D("ie1", "i0", "i2", "", 0.5, 0.5); b.H("ie3", "i2", "i3", "否"); b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是"); b.D("ie2d", "i2n", "i0l0", "否", al=True)
-b.D("ie1l", "i0l", "ipq", al=True); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
+b.D("ie1l", "i0l", "ipq", al=True); b.H("ie1gx", "i1g", "i1gx"); b.D("ie1g", "i1g", "i1i", al=True); b.H("ie1px", "i1p", "i1px", "失敗")
 b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", "逾時"); b.D("ie4a", "i4a", "i4z0", al=True)
 b.close()
 bypass(F, p5c, "ie1y", "i1i", "i1")
@@ -911,7 +912,8 @@
 b.box("igmf", P, 12, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 實際新增的 append 行；進 git）", 360)
 b.box("idl", E, 13, v2(SUB), fl("刪進度檔 .tmp.install.<id>.toml（最後一步）"), 560, ax=0)
 b.box("idlf", P, 13, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
-footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP)])
+footer(b, F, 14, [("iz", G12, fl("0：印建立／修改了什麼（含加的行；拒絕的印指示）"), E, SP),
+                  ("ix", v2(R12), fl("1：寫入／刪進度檔失敗（任一步，共通匯流）；明列已完成／未完成"), P, "c")], spacer=1, sp="l")
 b.D("ie7", "i5e", "i5", "", 0.5, 0.5); b.D("ie9", "i5", "i6", "否", al=True)
 b.RD("ie10", "i6", "i7", "無"); b.D("ie12", "i6", "i6s", "有", al=True)
 b.H("ie12s", "i6s", "i6sp", "是"); b.D("ie12n", "i6s", "i8", "否", al=True)
@@ -927,6 +929,7 @@
 b.D("ie24", "igm", "idl", "", 0.5, 0.5); b.H("ie24f", "idl", "idlf", "刪")
 b.D("ie25", "idl", "iz", "", 0.5, 0.5)
 b.close()
+failbus(F, p5cc, ["i11", "igy", "igm", "idl"], "ix")
 _A = F.abs
 def _lb(eid, s, t, label, tx, busx=445):   # 左車道「不動」格 → 左匯流排 → 下一段菱形頂點（與 --no-justfile 同一條匯流排）
     sx0, sy0, sw, sh = _A[s]; tx0, ty0, tw, th = _A[t]; ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw
@@ -944,7 +947,6 @@
  ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),
  ("6-20／6-34（問後才加）", "6-20「要加這一行嗎」（根 justfile import 行）；6-34「要加這幾行嗎」（根 .dockerignore，只列缺的行）；-y 免問；拒絕 → 不動、印手動加的指示"),
  ("逐行辨識（v2.16-7）", ".dockerignore 四行逐行看已在／缺：全在 → 跳過；缺 → 只問、只加缺的行，baseline/.vendor_kit.toml lines 只記實際新增的行（uninstall 只刪這些）"),
- ("symlink（根檔）", "根 justfile／.dockerignore 是 symlink → 不寫（不改連結目標），只印一次性遷移指示"),
  E4_T, LOGT[0]], ALL - {"inv", "tree", "pend", "rule"} | {"entry", "tty"})
 addpage("v1p5cc", "流程 v2：install（2）根 justfile 與 .dockerignore", p5cc)
 
@@ -1104,7 +1106,7 @@
 b.box("c23f", P, 20, F12, "＋version.toml [tools] 版本鎖定行（進 git）", 360)
 b.box("c23b", E, 21, v2(SUB), "成功：刪進度檔（metadata [progress]；最後一步）", 400)
 b.box("c23bf", P, 21, v2(F12), ".vendor_kit.toml（－[progress]）", 360)
-footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 22, [("c24", G12, "0：印摘要，提示 git add", E, "l"), ("c23x", v2(R12), "1：寫入失敗（本段任一步，共通匯流）→ 明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("ce23a", "c13c", "c15a"); b.H("ce23b", "c15a", "c15af", "寫"); b.D("ce23c", "c15a", "c15"); b.D("ce23cc", "c15", "c15c"); b.H("ce23", "c15c", "c15f", "寫")
 b.D("ce23d", "c15c", "c15b"); b.H("ce23e", "c15b", "c15bf", "寫"); b.D("ce24", "c15b", "c16", al=True)
 b.H("ce25", "c16", "c17", "無"); b.D("ce26", "c16", "c18", "有", al=True); b.H("ce27", "c18", "c19", "否"); b.D("ce28", "c18", "c20q", "是", al=True)
@@ -1213,9 +1215,13 @@
 b.box("z0", E, 14, v2(SUB), fl("彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）"), 360, ax="l")
 b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
 b.box("z1b", E, 16, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes（有待辦）或 apply|no（無待辦）、指紋（只傳協定內容）"), 360, ax="l")
-b.box("z2", U, 17, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
-b.box("z0q", L, 17, v2(D12), "啟動器：apply|no？", 240)
-b.box("mb", L, 18, ENTRY, "否：續「sync（2）」頁（apply|yes）：三叉 → docker → 引擎 apply sync", 280, ax="l")
+b.box("zq0", L, 16, v2(D12), "啟動器：resolve 回 0？", 240)
+b.box("zq0x", U, 16, v2(O12), fl(NZX), 220)
+b.box("zq1", L, 17, v2(D12), "是 → vk-resolve/1 文法合法？", 240)
+b.box("zq1x", U, 17, v2(R12), fl(E30X), 220)
+b.box("z2", U, 18, v2(G12), fl("0：無待辦（apply|no；啟動器驗完文法即 0），不起第二個容器，接著跑 recipe"), 220)
+b.box("z0q", L, 18, v2(D12), "啟動器：apply|no？", 240)
+b.box("mb", L, 19, ENTRY, "否：續「sync（2）」頁（apply|yes）：docker → 引擎 apply sync", 280, ax="l")
 b.D("ne6i", "n1e", "n1b"); b.H("ne6r", "n1b", "n1be"); b.D("ne6", "n1be", "nc", al=True)
 b.H("ne7", "nc", "ncx", "是"); b.D("ne8", "nc", "t0", "否", al=True)
 b.H("te0", "t0", "t0s", "是"); b.D("te1", "t0", "t1", "否", al=True); b.R("te2", "t0s", "t3m", "", busx=1230)
@@ -1228,19 +1234,21 @@
 b.R("te14", "t4", "tq", "是", busx=1230, tx=0.5, vert="left"); b.D("te15", "t5", "tq", al=True)
 b.D("te15n", "tq", "t6", "否", al=True)
 b.H("te16", "t6", "t6y", "是"); b.D("te17", "t6", "z0", "否", al=True); b.D("te18", "t6y", "z0", "", 0.5, 0.9)
-b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.D("ze1", "z1b", "z0q", "", 0.5, 0.5); b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
+b.D("ze0", "z0", "z1"); b.D("ze0b", "z1", "z1b"); b.H("ze1", "z1b", "zq0")
+b.H("ze1x", "zq0", "zq0x", "否"); b.D("ze1q", "zq0", "zq1", "是", al=True); b.H("ze1gx", "zq1", "zq1x", "否"); b.D("ze1g", "zq1", "z0q", "是", al=True)
+b.H("ze0y", "z0q", "z2", "是"); b.D("ze2", "z0q", "mb", "否", al=True)
 b.close()
 _A = F.abs; _ey = _A["tq"][1] + _A["tq"][3] / 2; _gy = F.rt["t0"] - F.gap / 2; _nx = _A["t0"][0] + _A["t0"][2] / 2; _bx = 1610
 _tot = (_bx - (_A["tq"][0] + _A["tq"][2])) + (_ey - _gy) + (_bx - _nx) + 10
 p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
-foot(p6r, "p6r", F.y, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
+foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
 addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)
 
 # ================= P6c：sync（2）第 2 段 apply =================
 p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
-b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 文法？→ 每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
+b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
 b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
-res3(b, "m0", 1, "m0a")
+b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
 pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm")), w=(260, 200, 260))
 b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
 b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
@@ -1254,7 +1262,7 @@
 b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
 b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
 b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
-b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
+b.D("me0q", "m0q0", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
 b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
 b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "不同"); b.D("me2c", "m2b", "m2c", al=True); b.H("me2cx", "m2c", "m2cx", "否")
 b.D("me3", "m2c", "m2z", "是", al=True)
@@ -1353,12 +1361,14 @@
 b.box("a8q", E, 12, v2(D12), "主線 CI 與 PR 分支 CI 都綠？", 300)
 b.box("a8", RN, 13, G12, "是：merge PR", 180)
 b.H("ae1", "a0", "a1", "查"); b.D("ae2", "a1", "a2", "有新版"); b.H("ae3", "a2", "a3", "改一行")
-b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4b", "a4b0", "a4b"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4", "a2", "a4a"); b.D("ae4b0", "a4a", "a4b0"); b.D("ae4q", "a4b", "a4q")
+b.D("ae4b", "a4b0", "a4b", al=True)
 b.H("ae5", "a4q", "a5", "否"); b.D("ae5n", "a4q", "a4c", "是"); b.D("ae5c", "a4c", "a4d"); b.D("ae5d", "a4d", "a4e1"); b.D("ae5e", "a4e1", "a4e2")
 b.D("ae6", "a5", "a6a"); b.D("ae6b", "a6a", "a6b"); b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")
 b.D("ae8", "a4e2", "a4f", "", 0.5, 0.5); b.H("ae8x", "a4f", "a4fx", "是"); b.D("ae8n", "a4f", "a8q", "否", al=True); b.D("ae9", "a7", "a8q", "", 0.5, 0.5)
 b.H("ae10x", "a8q", "a8qx", "否"); b.D("ae10", "a8q", "a8", "是", 0.5, 0.5)
 b.close()
+sidebus(F, p7, "ae4b0x", "a4b0", "a5", "納管：1 停", busx=270, side="l", tx=0.5, pos=-0.55, vert="below")
 foot(p7, "p7", F.y, _t7("Renovate", "PR／commit", "check.sh", "基準版落後", "6-1／6-13", "GHCR"), ALL - {"inv", "tree", "pend"})
 addpage("v1p7", "流程 v2：upgrade ── A. Renovate 路徑", p7)
 
@@ -1521,7 +1531,7 @@
 b.box("b16bf", P, 8, v2(F12), ".vendor_kit.toml（－[progress]）", 280)
 b.box("b18", U, 9, O12, fl("2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨"), 220)
 b.box("b16q", E, 9, v2(D12), "有衝突（conflicts 非空）？", 220, ax="l")
-b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
+b.box("b18r", P, 9, v2(RULE), fl("多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 衝突 2 > 0；訊息全部列出。6-14 僅是提醒，不改結束碼：待合併補完後另有新版 → 印「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」"), 280)
 footer(b, F, 10, [("b17", v2(G12), "0：印摘要 → commit", E, "l"), ("b16x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；進度檔保留", P, "c")], spacer=1, sp="l")
 b.D("be23", "b15z", "b15a", al=True)
 b.H("be24", "b15a", "b15f", "寫"); b.D("be24b", "b15a", "b15b"); b.H("be24bf", "b15b", "b15bf", "寫")
@@ -2207,7 +2217,7 @@
 b.box("m10ef", P, 15, F12, "－version.toml <repo> 版本鎖定行（進 git）", 360)
 b.box("m10g", E, 16, v2(SUB), "成功：刪進度檔（最後一步）", 400)
 b.box("m10gf", P, 16, v2(F12), "－.vendor_kit/.tmp.remove.<id>.toml", 360)
-footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；版本鎖定行不動、進度檔保留", P, "c")], spacer=1, sp="l")
+footer(b, F, 17, [("m11", G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", E, "l"), ("m10x", v2(R12), "1：寫入失敗（本段任一步，共通匯流），明列已完成／未完成；依進度檔恢復；若僅刪進度檔失敗，移除已完成且進度檔留待下次刪", P, "c")], spacer=1, sp="l")
 b.D("me11e", "m9e", "m9l"); b.H("me11f", "m9l", "m9lf", "寫"); b.D("me11h", "m9l", "m9h", al=True)
 b.LD("me11hn", "m9h", "m10a", "無", busx=535, vert="left"); b.D("me11q", "m9h", "m9q", "有", al=True)
 b.LD("me12n", "m9q", "m10a", "否：不刪（記孤兒 append 行）", busx=570, vert="left"); b.D("me12y", "m9q", "m9s", "是", al=True)

tokens used
129,331
已修改 [disc_v1_b.py](<scratchpad>/disc_v1_b.py)，並重新產生 `v1_b.drawio`。

修改頁面：

- `v1p5i`：移除三個向後引用。
- `v1p5ccc`：docker 段改成單一子流程描述，清除 onething 問題。
- `v1p5c`：補 install 引擎版本鎖定行命中 `≠ 1` 的紅色出口。
- `v1p5cc`：補寫入／刪進度檔共通失敗匯流；移除第 0 頁已有的 symlink 名詞。
- `v1p5bc`：修正刪進度檔失敗後「版本鎖定行不動」的不實敘述。
- `v1p6cc`：resolve 回碼、文法、`apply|no` 改為正確順序。
- `v1p6c`：入口改成承接前頁已驗證完成的三叉結果。
- `v1p7`：Renovate check.sh ⓪ 補「納管 → 1 停」出口。
- `v1p7cccc`：6-14 改為提醒、不改結束碼。
- `v1p8bccc`：修正後段失敗終點對版本鎖定行狀態的描述。

「待處理問題」便條：未新增。

檢查結果：

- `run_v1_b.py`：成功，38 頁。
- `check_overflow.py`：共 0 筆。
- `check_overlap.py`：共 0 筆。
- `check_cross_v1b.py`：共 0 筆。
- `check_self_v1b.py`：共 0 筆。
- `check_jog_r7.py`：共 0 筆。
- `check_align_v1b.py`：所有頁皆「無」。
- `lint_pages.py`：非 termcov warn 為 0；剩餘 120 條均為 termcov。
- Python 語法編譯：通過。
- 最大頁高 2395，頁寬 1660。

此 scratchpad 不是 Git repository，因此無法依 `implement` 技能建立 commit 或執行基於 merge-base 的 code review。
