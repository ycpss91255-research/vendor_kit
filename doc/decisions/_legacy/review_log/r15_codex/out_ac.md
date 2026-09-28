OpenAI Codex v0.155.1
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: low
reasoning summaries: none
session id: 01a0bf7e-06bc-7322-966b-4eafabe72969
--------
user
你是 draw.io 產生器 `disc_v1_a.py`、`disc_v1_c.py` 的修改者（Python；a 檔用 tbl／rtitle／emit 等 helper 畫表格與架構圖，c 檔 exec `disc_v1_b.py` 的 helper 段後用 Flow／_Band 畫流程）。附件 H 是 helper 段（不可改）。只改指定頁：a 檔 v1p2、v1p3、v1p3b、v1p3bb、v1p3c、v1p3d、v1p4；c 檔 v1p9、v1p9c、v1p10、v1p11、v1p12、v1p15、v1p15c、v1p16、v1p16i、v1p16c、v1p16cb、v1p16cc、v1p16ccb、v1p16ccc。**a 檔的 v1p0、v1p0c、v1p0b、v1p1、v1p1i、v1p1b、v1p1c、v1p2b、v1p2c 絕對不可改。**
規則：每格一件事；例子只用 `<repo>`；線上字級 12；顏色只用圖例；頁高 ≤ 2400、頁寬 ≤ 1660；不可交叉／壓框；名詞表每頁 ≤ 8 條且不含第 0 頁的詞；事件名只准 launcher_start／launcher_exit／engine_start／engine_exit。
要做的：附件 R 的 v2.17（含第 2 條契約④、第 10 條 lint、第 11 條便條規則）；附件 F 的必修＋選修逐條；附件 L 全清。改不了的在該頁右下角加黃底便條「待處理問題」（style 同 `pend`／NOTE），條列「元件 id：一句說明」。
做法：先 `python3 run_v1_a.py && python3 run_v1_c.py` 確認能跑；改完再跑，並對 `v1_a.drawio`、`v1_c.drawio` 各跑 `check_overflow.py`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`、`check_margin_label.py`（都要「共 0 筆」）與 `extract_pages.py <drawio> <out> && lint_pages.py <out>`（非 termcov warn 要 0）。最後輸出：改了哪些頁與每頁改了什麼、便條清單、檢查結果。
注意：`disc_v1_b.py` 由別人同時修改，**不要碰**；`disc_v1_c.py` 第 10 行 exec 它的 helper 段，若 b 檔暫時語法壞導致 run_v1_c.py 跑不了，等 60 秒再試（最多 10 次）。不改 `gen_disc.py`、`drawio_common.py`、任何 check_*.py／lint_pages.py／extract_pages.py。附件 F／L／R 中屬別的檔的頁（v1p5*～v1p8*、v1p1b／v1p2b 等）忽略；跨頁 term-diff 兩條以**較長版本為準**、較長版本都在本檔頁（baseline/.gitkeep 的 v1 在 v1p2／v1p2c／v1p16i；6-33 的 v2 在 v1p10）：這些名詞文字**不要改**，b 檔那方會對齊過來（v1p2c 不可改，所以 v1p2／v1p16i 也不能動這條文字）。lint 的 write-fail-edge 條目屬 v1p9c／v1p16cb／v1p16ccc，要補失敗出邊或匯流；end-color-text 屬 v1p16 o3tx；term-count 屬 v1p3。


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

==================== 附件 F：review_v2r14_claude.md 中屬 a／c 檔的頁（17 頁：v1p3 v1p3b v1p4 v1p16ccb v1p16c v1p16cb v1p16ccc v1p16 v1p9c v1p9 v1p16i v1p12 v1p10 v1p3c v1p16cc v1p15c v1p15）====================
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

## 14 契約 v2：CI 契約⑤ 與驗收矩陣 (v1p3c): must_fix 0 / optional 2
  (opt) [排版] k1g_e: sync 的「3」出線水平段 y=353 緊貼「命中 → 1 拒絕」橢圓底（y=343）只差 10px，縮圖看起來像貼著橢圓走
  (opt) [可讀性] c_d3: 「發 Release vN（bootstrap.sh、tar、.digest、SHA256SUMS）」122px 寬框內折成 5 行，「tar、」單獨一行，縮圖下擠

## 68 流程 v2：離線包（3）斷網 sync (v1p16cc): must_fix 1 / optional 2
- [排版] we2y: 「相符：用本機 tag（不 pull）」這條線從 inspect <tag> 菱形直落到 docker run 框，途中穿過無關的「否：docker image inspect <version.toml 的正式 ref@digest>」方框（w2b）並擦到「本機有該 image？」菱形右尖；線標籤又被「有」線（we5）橫切，縮圖下標籤被線壓字
  (opt) [內容一致性] w0l: 同 v1p16：「建執行紀錄」格無失敗出口，6-38 只從「寫 launcher_start」接出
  (opt) [排版] we2n: 「否」標籤直接壓在左側迴繞的垂直線上（x≈262）；兩個菱形之間的「是」標籤也壓在直線上

## 63 流程 v2：vendor_kit release（2）推 image 與資產 (v1p15c): must_fix 0 / optional 2
  (opt) [排版] ve14g: 「打」標籤擠在 20px 短箭頭上，字疊到「打正式 GHCR image tag」框右緣與 v2 徽章
  (opt) [可讀性] v11n: 「已釋出 image／Release 資產／fixture 永不刪；下游 Renovate 會看到新 tag@digest」便條靠泳道右邊界，文字貼到框緣、在「新」處硬換行

## 62 流程 v2：vendor_kit release（1）build 與驗收 (v1p15): must_fix 0 / optional 1
  (opt) [可讀性] v4x: 紅橢圓文字在「印失／敗的條號」處把一個詞硬拆兩行

==================== 附件 L：review_v2r14_lint.md 屬 a／c 檔頁的行 ====================
# 第十四版 lint warn（非 termcov）
- [term-count] v1p3 -: 名詞表 16 條 > 8
- [write-fail-edge] v1p9c q12j: 寫入格缺失敗出邊或失敗匯流：「否：建進度檔 .tmp.prune.<id>.toml（第一個寫入前；state」
- [write-fail-edge] v1p9c q12c: 寫入格缺失敗出邊或失敗匯流：「刪 trap 沒清到的殘留啟動器暫存 .tmp.dist.<id>/」
- [write-fail-edge] v1p9c q12d2: 寫入格缺失敗出邊或失敗匯流：「刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列」
- [write-fail-edge] v1p9c q12k: 寫入格缺失敗出邊或失敗匯流：「是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成」
- [term-dup-page0] v1p9c resolve／apply（兩段）: 名詞「resolve／apply（兩段）」第 0 頁已有（同名或只差結尾括號），不必重列
- [end-color-text] v1p16 o3tx: 終點文字應為 end_orange 但是 end_red：「否 → 1：本機無此 image（tag 形：先 docker load 或改給」
- [write-fail-edge] v1p16cb o10e3: 寫入格缺失敗出邊或失敗匯流：「寫 metadata：source（正式 ref@digest）+ local_」
- [write-fail-edge] v1p16cb o10e4: 寫入格缺失敗出邊或失敗匯流：「寫 version.toml [tools] 行：正式 ref@digest（最」
- [write-fail-edge] v1p16ccc w4r2: 寫入格缺失敗出邊或失敗匯流：「寫印記 gen/<repo>.stamp（index digest + 每檔 s」
- [term-diff] 跨頁 6-33（未完成交易）: 名詞「6-33（未完成交易）」有 2 個版本：
  v1（2 頁：v1p6 v1p8cx）長度 161
  v2（1 頁：v1p10）長度 185
  v1↔v2 差異：insert: v1「唯讀動詞偵測到 .tmp」 ↔ v2「唯讀動詞（sync／update／help）偵測到 .tmp」 ｜ insert: v1「ogress] in-progr」 ↔ v2「ogress] state=in-
- [term-diff] 跨頁 baseline/.gitkeep: 名詞「baseline/.gitkeep」有 2 個版本：
  v1（3 頁：v1p2 v1p2c v1p16i）長度 161
  v2（1 頁：v1p5cw）長度 117
  v1↔v2 差異：delete: v1「VK 自產的進 git 空檔」 ↔ v2「VK 自產進 git 的檔」 ｜ replace: v1「產的進 git 空檔：git 不追」 ↔ v2「自產進 git 的檔，hash 固

==================== 附件 H-a：disc_v1_a.py 前 450 行（helper：tbl／rtitle／emit／LEGEND 等；不可改）====================
"""契約 v2（decisions/interface_spec.md v3.3 為準）與架構頁：11 頁 v1p1／v1p1b／v1p1c／v1p2／v1p2b／v1p2c／v1p3／v1p3b／v1p3c／v1p3d／v1p4。
第十三輪（v2.15 + r12_codex/findings1.md；備份 .v14）：名詞全面換新（decisions/review/terms.md）、名詞表只留第 0 頁沒有的詞；執行紀錄事件改圖例約定①②（p3b 移除 engine_start／launcher_exit 格）；
p3b：gen/.stamp 判斷只在 sync、查 registry 只在 add／update／upgrade 未指定 @tag、inspect 有 → 跳過 pull、只有 extract kind 才 create／cp、resolve 非 0 出口、⓪ 拆三格；p3c：自身 CI 候選 tag → release-test → 驗收 → 正式 release、結束 3 獨立橙終點、驗收矩陣拆到 p3d（分組索引留 p3c）；
p4：8 模組（resolve／fetch／initfile／shell／progress／schema／log／prune）、主機載入鏈連線、log.sh 獨立檔、config.toml → schema、進度檔兩種落點、啟動器↔引擎拆兩線；p2：version.local.toml uninstall 直接刪、.tmp.* 加 dev、去 sync 豁免、基準版解析失敗不推、install 責任、.gitkeep 定義；p3：特殊檔、local_bootstrap.sh、d4_1／_sync 拆格。
第十四輪（備份 .v15）：新增審閱頁 00 v1p0／v1p0b「名詞與縮寫」（decisions/review/terms.md 逐字）、v1p1 重排為審閱頁 01「不變量與角色」（decisions/review/invariants_roles.md 逐字；出處對照不上圖）。
第十五輪（r13_codex/findings_00_01.md；備份 .v16）：審閱頁去掉 md 沒有的圖例／續頁句／「寫法約定」；常用詞拆到 v1p0c、不變量拆到 v1p1i；三方角色表改直排；審閱頁內容寬 1580、行距 1.4。
只定義 pages_v1_a，不寫檔。每頁：自己的 legend 與名詞表（只列該頁特有）；頁高 ≤ 2400、寬 ≤ 1650。"""
import glob, re, math
_latest = sorted(glob.glob("gen[0-9]*.py"), key=lambda p: int(re.findall(r"\d+", p)[0]))[-1]
exec(open(_latest).read().split("# ================= Page 1")[0])   # 只取 helper（顏色、v/e/page/legend/terms）
from check_overflow import shape_spacing

# ---------- 本檔共用樣式 ----------
_v_raw = v
def v(id, parent, style, value, x, y, w, h):
    """同 helper 的 v()，但橢圓／菱形自動補 spacing（v2.5 §15：橢圓 ×0.146、菱形 ×0.25），draw.io 才會以內接矩形折行。"""
    return _v_raw(id, parent, shape_spacing(style, w, h), value, x, y, w, h)
def vb(id, parent, style, value, x, y, w, h):
    """同 v()，但 <b>…</b> 保留成真的粗體。"""
    return v(id, parent, style, value, x, y, w, h).replace("&amp;lt;b&amp;gt;", "&lt;b&gt;").replace("&amp;lt;/b&amp;gt;", "&lt;/b&gt;")
def hv(text, w, fs=12, pad=6):
    """依 check_overflow 的估法算最小高度（含餘裕）。"""
    return math.ceil(need_h(text, fs, w)) + pad
def restroke(st, color, width):
    st = re.sub(r"strokeColor=[^;]*;", f"strokeColor={color};", st) if "strokeColor=" in st else st + f"strokeColor={color};"
    st = re.sub(r"strokeWidth=[^;]*;", f"strokeWidth={width};", st) if "strokeWidth=" in st else st + f"strokeWidth={width};"
    return st
def refill(st, fill):
    return re.sub(r"fillColor=[^;]*;", f"fillColor={fill};", st)
V2G = "#00b050"                                   # v2 改：只加右上角小標籤，不改框色
TAG = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={V2G};strokeColor={V2G};fontColor=#ffffff;fontSize=9;fontStyle=1;"
       "align=center;verticalAlign=middle;spacing=0;spacingLeft=0;spacingRight=0;spacingTop=0;spacingBottom=0;")
def tag(id, parent, x, y, w):
    """格子右上角的 v2 小標籤（獨立小方塊，30×20）。"""
    return v(f"{id}_v2", parent, TAG, "v2", x + w - 32, y + 2, 30, 20)
def vt(id, parent, style, value, x, y, w, h, tagged=False):
    """vb + 可選 v2 標籤；tagged 時文字右邊留 34px 給標籤（標籤永不壓字）。回傳 list。"""
    st = style + ("spacingRight=34;" if tagged else "")
    if tagged: tag_fits(id, value, w, fs=float(re.findall(r"fontSize=(\d+)", style)[-1]) if "fontSize=" in style else 12)
    out = [vb(id, parent, st, value, x, y, w, h)]
    if tagged: out.append(tag(id, parent, x, y, w))
    return out
def hvt(text, w, tagged=False, pad=6):
    return hv(text, w - (34 if tagged else 0), pad=pad)
def hve(text, w, fs=12, pad=6):
    """橢圓：以內接矩形（w×0.707、h×0.707）估最小高度。"""
    return math.ceil(need_h(text, fs, w * 0.707) / 0.707) + pad
def hvr(text, w, fs=12, pad=6):
    """菱形：以內接矩形（w×0.5、h×0.5）估最小高度。"""
    return math.ceil(need_h(text, fs, w * 0.5) / 0.5) + pad
def pos_at(pts, i, x=None, y=None):
    """折線 pts 上第 i 段（pts[i]→pts[i+1]）某點（給 x 或 y）的相對位置（-1 起點 … 1 終點），供線上標籤定位。"""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(segs); d = sum(segs[:i]); a, b = pts[i], pts[i + 1]
    d += abs((x if x is not None else a[0]) - a[0]) + abs((y if y is not None else a[1]) - a[1])
    return round(2 * d / total - 1, 4)
NP_NOTE = NOTE
def nopend(prefix, x, y, w, body):
    text = "<b>本頁無待拍板</b>\n" + body
    h = hv(text, w, pad=10)
    return vb(f"{prefix}_pend", "1", NP_NOTE, text, x, y, w, h), y + h
PEND_R = NOTE.replace("strokeColor=#999999", "strokeColor=#b85450;strokeWidth=3").replace("fillColor=#ffffff", "fillColor=#fff2cc")
def pend(prefix, x, y, w, body):
    text = "<b>⚠ 待你回覆（待拍板；只列本頁相關，附建議）</b>\n" + body
    h = hv(text, w, pad=10)
    return vb(f"{prefix}_pend", "1", PEND_R, text, x, y, w, h), y + h
L12 = LEAF() + "fontSize=12;"
LT12 = L12 + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=6;"
P12 = PURPLE_LEAF + "fontSize=12;"
PT12 = P12 + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=6;"
CODE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;strokeWidth=1;fontSize=12;fontFamily=Courier New;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
# v2.7 §9：逐字範例框一律 whiteSpace=pre（不折行、保留行首 tab／空白）、等寬、靠左；值包在 <pre> 內讓瀏覽器以 white-space:pre 呈現，
# tab 寫成 &#9;（XML 屬性裡的字面 tab 會被正規化成空白）。說明文字一律放框外。
CODE_PRE = CODE.replace("whiteSpace=wrap;", "whiteSpace=pre;")
def code_w(text, fs=12, tab=8):
    """最寬一行的像素寬（tab 展開成 8 格；與 check_overflow 同一套字寬估法）。"""
    from check_overflow import cw as _cw
    return max(sum(_cw(ch, fs) for ch in ln.expandtabs(tab)) for ln in text.split("\n"))
def code_h(text, fs=12, pad=6):
    return math.ceil(len(text.split("\n")) * fs * 1.3 + 8) + pad
def code(id, parent, text, x, y, w=None, h=None, tagged=False, fs=12):
    """逐字範例框：回傳 (cells, 寬, 高)。w 省略 → 依最寬行算；給了就檢查放得下（不折行）。"""
    import html as _html
    need = math.ceil(code_w(text, fs)) + 16 + (34 if tagged else 0)
    if w is None: w = need
    assert w >= need, f"code {id}: 寬 {w} < 最寬行需要 {need}"
    if h is None: h = code_h(text, fs)
    inner = _html.escape(text, quote=False).replace("\n", "<br>")
    htmlv = '<pre style="margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;">' + inner + '</pre>'
    val = _html.escape(htmlv, quote=True).replace("\t", "&#9;")
    st = CODE_PRE + (f"fontSize={fs};" if fs != 12 else "") + ("spacingRight=34;" if tagged else "")
    out = [f'<mxCell id="{id}" value="{val}" style="{st}" vertex="1" parent="{parent}">'
           f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>']
    if tagged: out.append(tag(id, parent, x, y, w))
    return out, w, h
def tag_fits(id, text, w, fs=12):
    """v2 標籤佔右上角 34px：文字最寬 token（第一行）不得伸進去，否則產生時就報錯（p2b_gn_r1c0 教訓）。"""
    from check_overflow import wrap_lines, strip_tags
    first = strip_tags(text.replace("<br>", "\n")).split("\n")[0]
    _, widest, _ = wrap_lines(first, fs, w - 16 - 34)
    assert widest <= w - 6 - 34 - 2, f"tag {id}: 首行最寬字 {widest:.0f} 會壓到 v2 標籤（格寬 {w}，可用 {w - 42}）「{first[:30]}」"
F_GIT = LEAF() + "fontSize=12;strokeColor=#82b366;strokeWidth=2;align=left;spacingLeft=8;"          # 進 git：綠框實線
F_NOGIT = LEAF() + "fontSize=12;dashed=1;strokeColor=#999999;fontColor=#333333;align=left;spacingLeft=8;"   # 不進 git：灰虛線
F_USER = F_GIT.replace("fillColor=#ffffff", f"fillColor={YELLOW}")                                   # 專案檔：黃底綠框
F_GIT_T = F_GIT + "verticalAlign=top;spacingTop=4;fontStyle=1;"                                      # 檔案標題容器（進 git）
F_NOGIT_T = F_NOGIT + "verticalAlign=top;spacingTop=4;fontStyle=1;"
F_USER_T = F_USER + "verticalAlign=top;spacingTop=4;fontStyle=1;"
INV = restroke(LT12, "#b85450", 3)                                                                   # 不變量：白底紅粗框
RULE = restroke(refill(LT12, "#ffe6cc"), "#d79b00", 1)                                               # 規則／摘要：淺橘底
HOST = restroke(refill(L12, RED), "#b85450", 3)                                                      # 啟動器：紅底紅粗框
ENG12 = restroke(refill(L12, "#dae8fc"), "#6c8ebf", 2)                                               # 藍：引擎做的（容器內；v2.14-3 藍＝引擎、白＝啟動器）
ORANGE = "#ffe6cc"
BLUE = "#dae8fc"
GRP = refill(L12, NEUTRAL)
GRP_T = GRP + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;fontStyle=1;"                 # 分組容器（標題在上）
UNIT = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;spacing=0;spacingLeft=2;spacingRight=2;"
FRAME = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;dashed=1;dashPattern=1 3;strokeWidth=1.5;"
TBL_H = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e6e6e6;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
ENTRY = "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;dashed=1;strokeWidth=2;fontSize=12;"   # 跨頁入口：白底虛線橢圓
LBL = TEXT(13) + "align=left;fontStyle=1;"
def tbl_style(fill, bold=False):
    return (f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#999999;fontSize=12;"
            f"{'fontStyle=1;' if bold else ''}align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;strokeWidth=1;")
def tbl(out, prefix, parent, x, y, cols, rows, fills=None, marks=(), bold0=True, align=(), lh=None):
    """cols: [(標題, 寬)]；rows: [[cell...]]；cell 可以是 list → 同一欄直向拆成多個子格（每格一件事）；
    fills: 每列底色；第一欄粗體；marks: {(r, c)} 加 v2 標籤；align: 欄索引集合 → 這些欄的第 k 個子格等高（同一件事的條件／動作／結束碼橫向對齊）；
    lh: 行距（lineHeight；None = 預設），設了就用 hvl() 估高。回傳結束 y。"""
    cx = x
    for i, (h, w) in enumerate(cols):
        out.append(v(f"{prefix}_h{i}", parent, TBL_H, h, cx, y, w, 30)); cx += w
    cy = y + 30
    for r, row in enumerate(rows):
        cells = [c if isinstance(c, list) else [c] for c in row]
        hs = [[(hvl(s, w - (34 if (r, i) in marks and k == 0 else 0), lh, pad=2) if lh else hvt(s, w, (r, i) in marks and k == 0, pad=2)) for k, s in enumerate(col)] for i, (col, (_, w)) in enumerate(zip(cells, cols))]
        for i, (col, (_, w)) in enumerate(zip(cells, cols)):
            if (r, i) in marks: tag_fits(f"{prefix}_r{r}c{i}", col[0], w)
        if align:
            n = max(len(hs[i]) for i in align)
            for k in range(n):
                mk = max(hs[i][k] for i in align if k < len(hs[i]))
                for i in align:
                    if k < len(hs[i]): hs[i][k] = mk
        rh = max(sum(h) for h in hs)
        fill = (fills[r] if fills else "#ffffff")
        cx = x
        for i, (col, (_, w)) in enumerate(zip(cells, cols)):
            sy = cy; tot = sum(hs[i])
            for k, s in enumerate(col):
                st = tbl_style(fill, bold=(i == 0 and bold0)) + (f"lineHeight={lh};" if lh else "")
                h = hs[i][k] + (rh - tot if k == len(col) - 1 else 0)
                cid = f"{prefix}_r{r}c{i}" + (f"_{k}" if len(col) > 1 else "")
                if (r, i) in marks and k == 0: st += "spacingRight=34;"
                out.append(vb(cid, parent, st, s, cx, sy, w, h))
                if (r, i) in marks and k == 0: out.append(tag(cid, parent, cx, sy, w))
                sy += h
            cx += w
        cy += rh
    return cy
def ew(id, src, tgt, label, exit, entry, points, both=False, lab=None, pos=None):
    """帶轉折點（絕對座標）的正交線；lab='below' 文字放線下、'side' 放線側；pos = 標籤沿線位置（-1 起點 … 1 終點）。"""
    st = EDGE + f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if both: st += "startArrow=block;startFill=1;"
    if lab == "below": st += "verticalAlign=top;spacingTop=6;spacingBottom=0;"
    elif lab == "side": st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    elif lab == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points)
    xa = "" if pos is None else f' x="{pos}"'
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'<mxGeometry{xa} relative="1" as="geometry"><Array as="points">{pts}</Array></mxGeometry></mxCell>')
def uw(s):
    import unicodedata
    return sum(10 if unicodedata.east_asian_width(ch) in ("W", "F") else 6 for ch in s) + 18
def units_rows(labels, w, gap=6):
    rows = []; cur = []; ux = 0
    for s in labels:
        if cur and ux + uw(s) > w:
            rows.append(cur); cur = []; ux = 0
        cur.append((s, ux)); ux += uw(s) + gap
    if cur: rows.append(cur)
    return rows
def units_h(labels, w):
    return len(units_rows(labels, w)) * 30
def units(prefix, parent, x, y, w, labels):
    out = []
    for ri, row in enumerate(units_rows(labels, w)):
        for i, (s, ux) in enumerate(row):
            out.append(v(f"{prefix}_u{ri}_{i}", parent, UNIT, s, x + ux, y + ri * 30, uw(s), 24))
    return out
def grp_title_h(title, w, tagged=False):
    """檔案分組容器的標題列高：標題折成幾行就多高（v2.10-9：內框不得蓋住第二行）；單行仍 24。"""
    return max(24, math.ceil(need_h(title, 12, w - (34 if tagged else 0))) - 2)
def filegrp(prefix, parent, style, title, items, x, y, w, item_style=None, tagged=False):
    """檔案框一格一檔：標題容器（style）內排多個小框（每個一檔）。回傳 (cells, 高)。"""
    ist = item_style or style
    ih = 24; th = grp_title_h(title, w, tagged)
    cells = []
    h = th + 6 + len(items) * (ih + 4) + 4
    cells += vt(prefix, parent, style, title, x, y, w, h, tagged=tagged)
    for i, it in enumerate(items):
        cells.append(v(f"{prefix}_f{i}", prefix, ist.replace("fontStyle=1;", ""), it, 10, th + 6 + i * (ih + 4), w - 30, ih))
    return cells, h
def rbox(out, pid, parent, style, text, x, y, w, tagged=False, pad=6):
    """規則／說明框：依內容算高，回傳結束 y（含 14px 間距）。"""
    h = hvt(text, w, tagged, pad=pad)
    out.extend(vt(pid, parent, style, text, x, y, w, h, tagged=tagged)); return y + h + 14
def colbox(out, pid, parent, style, text, x, y, w, h, tagged=False):
    out.extend(vt(pid, parent, style, text, x, y, w, h, tagged=tagged))
LEGEND_ITEMS.update({
 "v1c":   (refill(L12, GREEN), "綠底：常用動詞", 130, 40, 10),
 "v1a":   (L12, "白底：進階動詞", 130, 40, 10),
 "v1o":   (refill(L12, BLUE), "藍底：一次性（bootstrap.sh）", 210, 40, 10),
 "v1role":(ELLIPSE(YELLOW) + "fontSize=12;", "黃橢圓：契約承諾的角色", 260, 52, 4),
 "v1us":  (ELLIPSE(GREY) + "fontSize=12;", "灰橢圓：不承諾（我們）", 260, 52, 4),
 "rhomb": (RHOMBUS, "黃：判斷", 150, 66, 0),
 "v2git": (F_GIT, "綠框：進 git", 120, 40, 10),
 "v2no":  (F_NOGIT, "灰虛線：不進 git（可重建）", 200, 40, 10),
 "v2usr": (F_USER, "黃底綠框：專案檔（進 git）", 230, 40, 10),
 "v2code":(CODE, "等寬字：檔案內容範例", 170, 40, 10),
 "v2tag": (L12, "右上角綠標籤：v2 改", 200, 40, 10),
 "pendn": (PEND_R, "黃底紅框摺角：待拍板便條", 200, 40, 10),
 "invb":  (INV, "白底紅粗框：不變量", 160, 40, 10),
 "ruleb": (RULE, "淺橘底：規則／摘要（已定）", 190, 40, 10),
 "tblh":  (TBL_H, "灰底：表頭", 110, 40, 10),
 "grpbox":(GRP, "淺灰底：分組（無狀態意義）", 200, 40, 10),
 "v3err": (ELLIPSE(RED) + "fontSize=12;", "紅橢圓：失敗（拉不到、寫入／驗證失敗）", 340, 52, 4),
 "v3act": (ELLIPSE(ORANGE) + "fontSize=12;", "橙橢圓：需人處理（1／3 印指令、2 解衝突）", 400, 56, 2),
 "v3ok":  (ELLIPSE(GREEN) + "fontSize=12;", "綠橢圓：成功終點（exit 0）", 270, 52, 4),
 "v3in":  (ENTRY, "白底虛線橢圓：跨頁入口「來自 p.X」", 320, 52, 4),
 "v3step":(L12, "白：步驟／說明", 130, 40, 10),
 "v3launch":(L12, "白：啟動器做（主機）", 170, 40, 10),
 "conv":  (TEXT(12) + "align=left;", "圖例約定①：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_exit（每個結束碼都寫）\n圖例約定②：每個「docker run 引擎」格隱含 —— 容器開始寫 engine_start（失敗 → 1 + 6-38、不做任何動作）、結束寫 engine_exit", 1540, 44, 0),
 "v3eng": (ENG12, "藍：引擎做（容器內）", 170, 40, 10),
 "v3err_s":(ELLIPSE(RED) + "fontSize=12;", "紅橢圓：失敗（1）", 190, 52, 4),
 "v3act_s":(ELLIPSE(ORANGE) + "fontSize=12;", "橙橢圓：需人處理", 200, 52, 4),
 "v3img": (P12, "紫：image（引擎與工具）", 170, 40, 10),
 "v4mod": (refill(L12, RED), "紅：引擎模組", 130, 40, 10),
 "v4unit":(UNIT, "白小框：最小單元", 140, 40, 10),
 "v4host":(HOST, "紅底紅粗框：啟動器（主機側薄殼）", 240, 40, 10),
 "v4hgrp":(GRP, "淺灰底：主機分組", 150, 40, 10),
 "v4egrp":(restroke(refill(L12, BLUE), "#6c8ebf", 2), "藍底藍框：引擎容器（容器內跑）", 230, 40, 10),
 "v4pgrp":(refill(L12, GREEN), "綠底：專案目錄分組", 160, 40, 10),
 "v4frame":(FRAME + "fontSize=12;", "點線框：init／merge 共用箭頭", 200, 40, 10),
 "v4other":(L12, "白底黑框：主機上的目錄／命名空間（不是檔）", 300, 40, 10),
 "notep": (NOTE, "便條：說明（含「本頁無待拍板」）", 220, 40, 10),
})
def lgd(prefix, x, y, keys, note, maxw=1260):
    """legend 自動換列（每列項目總寬 ≤ maxw，說明文字放第一列右邊，整體寬 ≤ 1600）。回傳 (cells, 結束 y)。"""
    c = []; rows = []; cur = []; cw = 0
    for k in keys:
        w = LEGEND_ITEMS[k][2] + 20
        if cur and cw + w > maxw: rows.append(cur); cur = []; cw = 0
        cur.append(k); cw += w
    if cur: rows.append(cur)
    ry = y; n = 0
    for ri, row in enumerate(rows):
        cx = x
        for k in row:
            st, t, w, h, dy = LEGEND_ITEMS[k]
            c.append(v(f"{prefix}_lg{n}", "1", st, t, cx, ry + dy, w, h))
            if k == "v2tag": c.append(tag(f"{prefix}_lg{n}", "1", cx, ry + dy, w))
            cx += w + 20; n += 1
        if ri == 0: c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", note, cx, ry, min(300, 1600 - cx), 60))
        ry += 66
    return c, ry
def terms2(prefix, x, y, rows, kw=150, vw=610, gap=40):
    """名詞表兩欄（省高度）；id {prefix}_tk{i}/_tv{i}。回傳 (cells, 結束 y)。"""
    c = [v(f"{prefix}_th", "1", LBL, "本頁名詞（只列本頁用到的）", x, y - 34, 300, 28)]
    hs = [max(28, math.ceil(max(need_h(k, 12, kw), need_h(d, 12, vw)))) for k, d in rows]
    tot = sum(hs); acc = 0; split = len(rows)
    for i, h in enumerate(hs):
        acc += h
        if acc >= tot / 2: split = i + 1; break
    ends = []
    for cx, idx in ((x, range(0, split)), (x + kw + vw + gap, range(split, len(rows)))):
        cy = y
        for i in idx:
            k, d = rows[i]; h = hs[i]
            c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, cx, cy, kw, h)); c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, cx + kw, cy, vw, h)); cy += h
        ends.append(cy)
    return c, max(ends)
def footer(cells, prefix, y, keys, note, termkeys):
    """legend（自動換列）+ 名詞表（兩欄、只列 termkeys）。"""
    c, y2 = lgd(prefix, 40, y, keys, note)
    cells += c
    c, y3 = terms2(prefix, 40, y2 + 34, [TERMS[k] for k in termkeys])
    cells += c
    return y3
NUM_T = "契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"
def head(pid, title, w=960):
    return [v("title", "1", TITLE, title, 40, 20, w, 34), v(f"{pid}_num", "1", TEXT(12) + "align=left;", NUM_T, 40, 56, 1200, 26)]

# ---------- 名詞總表（每頁只挑自己用到的）----------
TERMS = {
 "repo": ("<repo>", "下游 repo 名（占位符）；.vendor_kit/cache/<repo>/ = 專案裡展開的工具檔；ghcr.io/<org>/<repo>-dist = 它的 image；<ns> = 工具 just 模組的命名空間"),
 "inv": ("不變量（ADR）", "整個專案最高優先的四句：可以建、要改先問、永不刪、永不覆蓋；記在 docs/adr/（短格式 ADR），每個決議都對照它；不另建 PRD.md"),
 "adr": ("ADR", "Architecture Decision Record：一份記錄「為什麼這樣決定」的短文件（docs/adr/）；破壞性變更、提高最低介面版都要記一筆"),
 "group": ("組（常用／進階／一次性）", "常用 = 每天會打的（add／upgrade／dev）；進階 = 偶爾才用；一次性 = 只在第一次接入跑的 bootstrap.sh（release 附的腳本，不是 just 動詞）"),
 "reverse": ("反向", "把該動詞做的事收回的動詞（install↔uninstall、add↔remove、dev↔undev）；upgrade 沒有動詞反向，靠 git revert（把整組升級 commit 反做一次的 git 指令）"),
 "apt": ("apt 語意", "跟 Debian 的 apt 一樣分兩步：update 只查有沒有新版、不動檔；upgrade 才真的套用"),
 "rmrf": ("rm -rf", "整個目錄連內容一起刪的 shell 指令；uninstall 明說「不 rm -rf .vendor_kit/」= 只刪確認是我們產的檔（hash 相符）"),
 "setpos": ("set positional-arguments", "justfile 的全域設定：讓 recipe 用 $1 $2 … 收參數，verb *args 一行轉發靠它；被 import 檔的 set 會外溢，所以只放 mod 進來的 vendor.just"),
 "engref": ("引擎 ref", "version.toml 的 vendor_kit = \"<ref>\" 版本鎖定行（<ref> = ghcr.io/<org>/vendor_kit:vN@sha256:…）；version.local.toml 可覆寫成本機 tag + image ID；啟動器用它 docker run 引擎，也記進 gen/.stamp"),
 "ghcr": ("GHCR", "GitHub Container Registry：GitHub 提供的 image 倉庫（ghcr.io）；下游 image 與引擎 image 都放這裡"),
 "image": ("image", "docker 用的「打包好的檔案層」；下游 image 只是裝 dist/ 的純資料包，引擎 image 才是會跑的程式"),
 "ghcrimg": ("GHCR／image", "GHCR = GitHub 的 image 倉庫（ghcr.io）；image = docker 打包檔：下游 image 是純資料包（FROM scratch 只 COPY）、引擎 image 是會跑的程式"),
 "just": ("just", "指令執行器（像 make）：專案根的 justfile 列出可打的指令（recipe）；主機需 just ≥ 1.33.0（GitHub release 下載版）"),
 "recipe": ("recipe", "justfile 裡的一條指令定義（名字 + 要跑的命令）；「一行轉發」= recipe 只有一行，把參數原樣丟給啟動器"),
 "justrecipe": ("just／recipe", "just = 指令執行器（像 make），主機需 ≥ 1.33.0；recipe = justfile 裡一條指令定義；vendor.just 每個動詞一條 recipe 一行轉發給啟動器"),
 "ns": ("命名空間", "just <ns> <recipe> 前面那個 <ns>；每個工具的 just/<ns>.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）"),
 "sync": ("sync", "每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑"),
 "syncverify": ("sync --verify", "長形選項：每檔 sha256 全驗（= CI 模式時的行為）；sync 無參數 = 快路徑（啟動器只 grep 比 stamp，全相符不起容器）；sync <repo> 一律起引擎驗該範圍"),
 "fetch": ("fetch", "引擎內部步驟（不對外）：把主機掛進來的 /dist/<repo> 展開到 cache/<repo>/、寫印記 gen/<repo>.stamp、verify sha256；在 apply 決定套用之後才做"),
 "flock": ("flock", "Linux 檔案鎖：引擎 apply 一開始對專案目錄上鎖，避免兩個 just 同時寫；等 60 秒逾時 → 1 印 6-26；VENDOR_KIT_NO_LOCK=1 跳過（啟動器轉發）"),
 "resolveapply": ("resolve／apply", "動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④"),
 "N": ("N（新版初始檔）", "逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.<id>/、掛進引擎的 /dist/<repo>（唯讀），不是 cache；cache/<repo>/ 在 apply 決定套用後才 fetch"),
 "dryrun": ("--dry-run", "只預覽不寫（長形，無短選項）：動 image 的動詞照樣拉 image 展開到暫存，引擎 apply --dry-run 唯讀列出會建／會問哪些檔；本機 → 0；CI 模式且需改 進 git 的檔 → 1 印清單"),
 "versiontoml": ("version.toml", ".vendor_kit/version.toml：專案「該裝哪版」的唯一來源；vendor_kit = \"<ref>\" 版本鎖定行（唯一）、schema、written_by、[tools] 每工具一行 tag@digest；version.local.toml = 本機覆寫（不進 git，同形）"),
 "append": ("strategy = \"append\"", "init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）"),
 "crlf": ("CRLF／LF", "兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]"),
 "tagdigest": ("tag@digest", "version.toml 裡每個工具記 image 的 tag 與 sha256 digest（多架構 index digest）；digest 才是真正鎖定的內容"),
 "sha256": ("sha256", "內容的指紋（雜湊）：內容變一個字指紋就不同；digest、印記、薄殼比對、輸入指紋都靠它"),
 "基準版": ("基準版", ".vendor_kit/baseline/<repo>/ = 上次套用的初始檔原版副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 建 baseline/.gitkeep、vendor_kit/config.toml 副本與 .vendor_kit.toml（config.toml 的 metadata）"),
 "state5": ("初始檔五態（state）", "metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（下游使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"),
 "merge3": ("三方合併", "拿基準版（B）、你現在的檔（D）、新版初始檔（N）三份用 git merge-file --diff3 合；衝突留 <<<<<<< vendor_kit:baseline 標記並回 2；基準版仍推到新版（解析失敗除外）"),
 "stamp": ("印記 gen/<repo>.stamp", "每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:<dir>；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 fetch；gen/.stamp 只記引擎 ref"),
 "token": ("REGISTRY_TOKEN／\n_TOKEN_FILE", "私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v <file>:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 <repo>@<tag> 指定版本（主機 docker pull 走主機認證）"),
 "renovate": ("Renovate", "GitHub 機器人（下游自選）：GHCR 有新版就開 PR 改 version.toml 一行；人在 PR 分支跑 upgrade 補完合併、CI 綠後才 merge；preset 放 vendor_kit repo 根目錄 default.json，下游 extends: [\"github>ycpss91255-research/vendor_kit\"]"),
 "git": ("PR／commit／push／rebase", "git 用語：commit = 一次存檔；push = 推到 GitHub；PR = 請求合併某分支的頁面；rebase = 把分支重新接到最新主線（Renovate PR 勿勾）"),
 "repodigests": ("RepoDigests", "docker 記錄「這個 image 從哪個 registry 以哪個 digest 拉來」的欄位；docker load 進來的 image 沒有它，所以本機引擎只能用 tag + image ID"),
 "symlink": ("symlink", "指向另一個路徑的捷徑檔；dev 時 cache/<repo>/ 就是指向 <dir>/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止"),
 "release": ("release", "GitHub 上一個版本的發佈頁：附 bootstrap.sh、每平台 tar（docker save）與同名 .digest 旁檔；已釋出 image／Release 資產永不刪"),
 "tty": ("tty／trap", "tty = 互動終端（能問問題）；沒有 tty（管線、CI）又需詢問且無 -y → 1 印 6-4；trap = shell 的收尾勾子，啟動器用它在中斷時清容器與 .tmp.dist.<id>/"),
 "timeout": ("pull 逾時", "VENDOR_KIT_PULL_TIMEOUT／--timeout <秒>：單次 pull 總秒數，預設 300、只收正整數；逾時 → 1 印 6-31；啟動器自讀、不轉發引擎"),
 "CI 模式": ("CI 模式", "CI 模式真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ CI 模式；check.sh 自己 export CI=1。CI 模式 = 不寫任何 進 git 的檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 進 git 的檔 → 1 印清單，與 -y 無關（-y 不解除CI 模式）；update 不受影響"),
 "tracked": ("進 git 的檔", "進 git 的檔（git 追蹤中）：version.toml、薄殼五檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）"),
 "ci": ("CI／runner", "CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進CI 模式）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）"),
 "exit": ("結束碼 0／1／2／3", "0 成功（含 warn）；1 一般失敗或需人處理（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、基準版仍推、解完重跑）或 update --exit-code 有新版；3 介面版／檔案版不合（零寫入；先升級或退回才能繼續；以介面版／檔案版比較，不用版本字串）"),
 "protocol": ("--protocol P", "薄殼每次呼叫引擎都附的介面版整數（第一版 P=1，全域旗標在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方介面版 P 輸出 vk-resolve/P 行別與結束碼語意；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1"),
 "shellline": ("薄殼自描述首行", "entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 CRLF→LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動"),
 "imageid": ("image ID", "docker 本機給每個 image 內容的 sha256（docker image inspect --format '{{.Id}}'）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對"),
 "inspect": ("docker image inspect", "問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）"),
 "tar": ("tar／docker load", "tar = 打包檔；docker save 出的 image 離線包（每平台一個，旁附同名 .digest）；docker load 把它裝回本機 image（沒有 RepoDigests，只能用 tag）"),
 "digestfile": (".digest 旁檔", "<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1 + 6-24 主機錯誤分類）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id"),
 "stdio": ("stdout／stderr", "程式的兩條輸出：stdout = 給啟動器讀的結果（resolve 的 vk-resolve/1 清單，整份存檔、先驗文法、不 eval）；stderr = 給人看的診斷（warn、錯誤、問句以外），不會被當輸入"),
 "idem": ("冪等", "同一個指令重跑結果一樣、不會重複做（install 再跑 = 修復薄殼；add 已接入 → 0 無變更；append 行重跑不重複；upgrade vendor_kit 第二次 → 0）"),
 "mod": ("mod／mod?／import／import?", "just 的載入：mod <ns> '檔' 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import '檔' 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）"),
 "metadata": ("metadata", "baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度檔 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"),
 "root": ("專案根", "含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 <dir> 執行」；sync 亦無例外，工具 _sync 先 cd 到專案根）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git"),
 "prune": ("prune／label", "prune = 刪主機上帶 vendor_kit label 且本專案 version.toml／local 未引用的 docker 資源（容器／image／network／volume）；label 鍵前綴 io.github.<org>.vendor_kit（=1；容器類另加 .project=<專案根>）；vendor_kit 不建 network／volume"),
 "schema": ("schema／written_by", "每個 vendor_kit 寫的 TOML 都有 schema = N（integer，讀取門檻只看它）+ written_by = \"<vX>\"（純資訊）；同檔案版只加不改；讀時忽略未知欄位、寫時保留；只拒絕型別錯／重複宣告 → 1；檔案版高於本引擎 → 3 印 6-19 零寫入"),
 "canon": ("vendor_kit = 版本鎖定行", "version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = \"<ref>\"（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路"),
 "fingerprint": ("輸入指紋", "resolve 把它讀過的 version.toml、metadata、要動的專案檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」"),
 "progress": ("進度檔", "記錄交易進度的 TOML：state=\"in-progress\"、verb、id、started、targets、done／pending、consents；存在 = 上次沒走完；add／upgrade <repo> 記在 metadata [progress]，其餘可寫動詞放 .vendor_kit/.tmp.<verb>.<id>.toml（第一次 install 也建，v2.13 P5）；可寫動詞先恢復、sync／update 印 6-33 結束 1、help 仍 0"),
 "vkresolve": ("vk-resolve/1", "resolve 的 stdout 文法：首行 vk-resolve/<P>、每行 <kind>|<f1>[|<f2>…]（欄位以單一 | 分隔）、末行 end|<N>；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \\0ooo 八進位跳脫（printf '%b' 可解）；啟動器先收完整份、驗文法才動 docker"),
 "tmpdist": ("暫存 .tmp.dist.<id>/", "啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋"),
 "mount": ("掛載（-v）", "docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/<repo> = 本機覆寫的 <dir>/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）"),
 "uid": ("uid 旗標（-u）", "rootful docker 加 -u \"$(id -u):$(id -g)\"（寫出的檔才不會變 root 的）；rootless docker（docker info SecurityOptions 含 name=rootless）不加 -u；Podman（docker --version 含 podman）改加 --userns=keep-id、不加 -u"),
 "rootless": ("rootless／Podman", "rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收"),
 "whitelist": ("主機命令白名單", "啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、mkdir、date、od、tr、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files；lint 擋清單外"),
 "createcp": ("docker create／cp", "只建容器殼（docker create <ref> /x）再把 /dist 複製出來（docker cp）→ docker rm；純資料 image 沒有程式、不能 docker run；不帶 --platform（daemon 挑原生）"),
 "daemon": ("daemon", "主機上常駐的 docker 服務；拉 image、挑原生架構、回答 image inspect 都是它做"),
 "buildx": ("buildx", "docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index"),
 "indexdigest": ("多架構 index／index digest", "同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）"),
 "dist": ("dist/", "下游 repo 出貨的目錄：files/（展開到 cache/<repo>/ 的全部）、init.toml（初始檔清單）、just/<ns>.just（工具自己的 recipe，每檔含 _sync）"),
 "dockerfiledist": ("Dockerfile.dist", "逐字三行：FROM scratch／LABEL io.github.<org>.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）"),
 "label": ("label", "docker 資源上的鍵值標籤，鍵前綴 io.github.<org>.vendor_kit：容器／network／volume = 1 + .project=<專案根絕對路徑>；引擎 image = 1 + .protocol=<floor_P>-<current_P> + .schema=<N>；下游 image = 1；prune 依 label 掃"),
 "syncrecipe": ("_sync recipe（F1）", "每個 dist/just/<ns>.just 必含的私有 recipe（逐字：[private] / _sync: / \\tcd {{quote(justfile_directory())}} && just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查"),
 "dest": ("dest", "init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗"),
 "justdirs": ("just 的兩個目錄函式", "justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」"),
 "checksh": ("check.sh 六步（⓪–⑤）", "vendor_kit 出貨、進 git 的腳本（第二行自描述、第一個動作 export CI=1）：⓪ local 被 track → 1；① sync（CI 模式）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；整體結束碼 = 第一個失敗步驟的碼"),
 "envtest": ("env-test／test-base", "vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑"),
 "checkdist": ("check.sh --dist", "同一支腳本的供應端模式：在下游 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／CRLF、just 1.33.0 可解析、_sync lint、LABEL、image 可展開、兩平台一致"),
 "lint": ("lint／unit／測試矩陣", "lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）"),
 "reltest": ("release／release-test", "release-test = 對候選 image 在 amd64、arm64 原生 runner 跑 env-test + 完整主機流程，發生在驗收與正式 release 之前；release = 候選全過後打正式 GHCR image tag vN（imagetools create、不重 build、digest 不變）、Git tag vN、發 Release 附 bootstrap.sh 與 tar + .digest"),
 "fixture": ("fixture repo", "驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪"),
 "最低介面版": ("最低介面版", "相容承諾的下限：固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1），只能經 ADR + major 提高；低於最低介面版 → 3 印 6-18 零寫入；最低介面版檢查先於任何上網（斷網也回 3）"),
 "lcall": ("LC_ALL／TZ", "引擎容器內固定 LC_ALL=C.UTF-8（字元排序、編碼一致）、TZ=UTC（時間戳 UTC ISO 8601）；HOME 指容器內暫存；輸出不隨主機語系變"),
 "worktree": ("worktree／submodule", "git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）"),
 "engine": ("引擎", "vendor_kit 的程式本體：只以 image 存在（公開、多架構）、只在容器內跑；8 個模組見藍框引擎容器（紅框 = 模組；紫 = image）；一個專案用 version.toml 版本鎖定行那一版（version.local.toml 可覆寫成本機 image）"),
 "launcher": ("啟動器", ".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見架構圖 p4"),
 "candtag": ("候選 tag／正式 tag", "候選 image 先以候選 tag（vN-rc.<n> 或 candidate-<sha>）推上 GHCR；index inspect 與資產都對候選 tag 做；全過才 docker buildx imagetools create 打正式 GHCR image tag vN（不重 build、index digest 不變）；Git tag vN 是 repo 上的另一個物件，圖上分開標"),
 "modunit": ("模組／最小單元", "模組 = 引擎裡一塊獨立責任的程式（紅框；8 個模組的責任見第 0 頁）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）"),
 "logevents": ("log_event()／log-events.txt", "log_event() = 引擎內寫執行紀錄的唯一入口（事件名 + k=v；其他模組都呼叫它，圖上不逐條畫線）；log-events.txt = 事件名註冊表，真本在引擎 image，log.sh 內嵌啟動器那份白名單；未註冊 → FATAL"),
 "cli": ("cli", "引擎的入口模組：解析子命令與參數（含 --protocol P）、負責所有詢問（-y 免問；無 tty → 1）、決定結束碼 0／1／2／3，並呼叫其他模組"),
 "version": ("version", "讀寫 version.toml／version.local.toml（檔案版轉換）；apply 拿 flock；產生／重驗輸入指紋；寫 metadata [progress]；算 docker 資源 label（prune 用）"),
 "registry": ("registry", "查 GHCR 的 tag 與 index digest（update／add／upgrade 用；私有 registry 用 TOKEN／TOKEN_FILE；查詢有逾時）；sync 不查最新版，只拉鎖定版"),
 "initmerge": ("init／merge", "init 建初始檔、append 幾行或問「要建 X 嗎」；merge 在 upgrade 時對每個檔跑狀態機（D==B → 問後換、三者皆異 → 問後三方合併）+ git merge-file；兩者都把檔案清單與逐檔決定交給基準版"),
 "baselinemod": ("initfile 模組", "維護 baseline/<repo>/ 初始檔原版副本與 .vendor_kit.toml metadata（complete、五態、declined_hash、lines、conflicts、[progress]）"),
 "launchergen": ("shell 模組", "產生 .vendor_kit/ 自有薄殼五檔（含自描述首行）、gen/tools.just（mod? 行）、gen/.stamp、根 justfile 那一行（新檔時四行）、根 .dockerignore 四行；薄殼與 gen/.stamp 只由 install／upgrade vendor_kit 重產（先比首行 hash）；tools.just 由 sync／add／remove／upgrade 重生"),
 "logmod": ("log（輔助模組）", "v2.12：執行紀錄的唯一入口 log_event()（事件名 + k=v）；引擎用 Python logging + JSON formatter append 同一檔；事件註冊表 log-events.txt 真本在引擎 image（未註冊即 FATAL）；trace_id、log.sh、保留清理（keep／days）都在啟動器，引擎不做"),
 "logfile": ("執行紀錄 log/", ".vendor_kit/log/<verb>/<UTC ts>-<id8>.jsonl：一次執行一檔（JSON Lines）；啟動器先寫 launcher_start 才開始（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔，結束前 log_prune、launcher_exit；不進 git；憑證永不記"),
 "configtoml": ("config.toml", ".vendor_kit/config.toml（進 git；install 建、upgrade 三方合併）：schema = 1、[log] keep = 50、days = 30；缺檔或缺鍵 = 預設，非正整數 → 預設 + 警告；引擎用 TOML parser（toml-bridge stage）讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$"),
 "traceid": ("trace_id／TRACEPARENT", "啟動器每次執行產一個 32 hex id（/proc/sys/kernel/random/uuid 去 -，缺則 od /dev/urandom），同值 = 進度檔交易 id；以 -e TRACEPARENT 與 -e VENDOR_KIT_LOG_FILE 傳給引擎，引擎 append 同一個 log 檔"),
 "tmp": ("暫存目錄 <tmp>", "啟動器把下游 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.<id>/<repo>/，再把 .tmp.dist.<id>/ 唯讀掛進引擎當 /dist（逐檔判斷讀 /dist/<repo>，不是 cache）；本機覆寫時改掛 <dir>/dist → /dist/<repo>；trap 清掉"),
 "local": ("--local 值的判別", "已定：--local <值> 含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立（tag 含 / 且存在同名檔）→ 1 提示用 ./ 或完整 ref 消歧"),
 "multi": ("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」；舊薄殼對未知碼原樣傳出、不吞"),
 "unit": ("最小單元", "模組裡可以單獨測的最小功能（白小框，一格一個）"),
 "gitkeep": ("baseline/.gitkeep", "VK 自產的進 git 空檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；install 建、uninstall 刪、hash 固定為空檔（§4.0；v2.15-14）；工具的 metadata 由 add 才建（baseline/<repo>/.vendor_kit.toml 兼作該工具目錄的佔位）"),
 "dockerignore": ("根 .dockerignore 四行", "install 加進專案根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*、.vendor_kit/log/（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache"),
 "justfile4": ("根 justfile 四行", "install 新建根 justfile 時逐字：import '.vendor_kit/entry.just'／（空行）／default:／\\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行"),
 "gitkeepline": ("gen/.stamp", "只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行"),
 "rescue": ("救援路徑", "單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@<tag>]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ 最低介面版的舊薄殼永遠可經此叫任何引擎重產薄殼"),
 "renovatepreset": ("Renovate preset", "放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25"),
 "renovatebot": ("Renovate／PR／rebase", "Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）"),
 "envwl": ("-e 白名單", "啟動器只轉發：CI（照原值）、VENDOR_KIT_NO_LOCK；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update／upgrade 的 resolve 階段；TOKEN_FILE 改為 -v 掛載；PULL_TIMEOUT 啟動器自讀不轉發；HTTP_PROXY 等 → v2"),
 "engine_changed": ("「引擎已變」", "不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 版本鎖定行；ref 變了且 == 計畫的 engine → 用新 ref（本機覆寫時 inspect 驗 ID）跑 upgrade vendor_kit；第二次又變 → 1 印 6-2b"),
 "offline": ("離線可用（Q26）", "啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"),
 "declined": ("declined／declined_hash", "拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版新版初始檔 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined"),
 "conflicts": ("conflicts（衝突中檔案）", "metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 <<<<<<< vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其基準版不推；解完重跑才清空（拿鎖後）"),
 "hostdir": ("主機上的目錄／命名空間", "白底黑框：不是檔案的東西——暫存目錄、工具命名空間（just <ns> …）"),
 "deploy": ("deploy", "把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄"),
 "shell4": ("薄殼", ".vendor_kit/ 進 git、vendor_kit 擁有、人不改的五檔：entry.just、vendor.just、log.sh、.gitignore、ci/check.sh；只轉發、不做事；每檔自描述首行；只由 install／upgrade vendor_kit 重產；log.sh（自前身專案移植成 POSIX）同樣帶自描述首行；gen/.stamp 只記引擎 ref"),
 "uniq": ("唯一來源", "version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；基準版是上次合併的歷史狀態，不由它推導"),
 "localtoml": ("version.local.toml", "同目錄的本機覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = \"path:<dir>\" 或 vendor_kit = \"<tag>\" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；CI 模式下存在任何覆寫 → sync 回 1"),
 "cachedir": ("cache/<repo>/", "下游 image 的 /dist 展開副本，收在 .vendor_kit/ 裡；不進 git、不可改；dev 時是 symlink → <dir>/dist；印記不在這裡（在 gen/<repo>.stamp）"),
 "gen": ("gen/", "引擎產生的檔，不進 git，三種：tools.just（sync／add／remove／upgrade 重生）、.stamp（只由 install／upgrade vendor_kit 寫）、<repo>.stamp（fetch 寫）"),
 "initfile": ("初始檔", "init.toml 複製到專案的檔（歸下游使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"),
 "tmpverb": ("進度檔 .tmp.*", "install（第一次也建，v2.13 P5：兼「不留半成品」的清除清單）／remove／uninstall／undev／prune／upgrade vendor_kit 的進度檔（metadata 會被刪或不存在）；<id> = 交易 id = 本次 trace_id（v2.12）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪"),
 "options": ("短選項／長形", "短選項只有 -t／-y／-p／-i／-h（常用）；其餘一律長形（--dry-run、--source、--local、--exit-code、--timeout、--no-justfile）；版本一律位置參數 <repo>@<tag>（無 --tag）；--protocol 為內部旗標不列 help"),
 "localboot": ("local_bootstrap.sh", "離線包內附的便利包裝（非契約、不另定介面）：偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local <tar>"),
 "semver": ("SemVer", "版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高最低介面版或需要下游使用者手動步驟；minor = 新功能（含介面版 +1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR"),
}
pages_v1_a = []

# ---------- 審閱頁（md 定稿版逐字移植）共用 ----------
RX, RW, RLH = 20, 1580, 1.4      # 審閱頁：左邊距 20、內容寬 1580（page() 右邊自動留 40 → 頁寬 1640）、行距 1.4
def M(s):
    """md 行內記法 → 圖上文字：`code` 去反引號；**x** → 粗體。其餘一字不改。"""
    s = s.replace("`", "")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
def hvl(text, w, lh, fs=12, pad=6):
    """行距 lh 的最小高度：行數×fs×(lh+0.1)+8+pad（估法同 need_h；check_overflow 以 1.3 估，必過）。"""
    from check_overflow import wrap
    lines = sum(wrap(ln, fs, w - 16)[0] for ln in text.split("\n"))
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

==================== 附件 H-c：disc_v1_c.py 前 120 行（exec b 的 helper、_TRC 覆寫、foot()、LST1/LST2/LSX；不可改）====================
"""討論圖 v2 新增八頁（v2.6 §17）：v1p9 prune、v1p10 update、v1p11 初始檔五態、v1p12 交易與進度檔、
v1p13 相容性矩陣、v1p14 結束碼決策表、v1p15 vendor_kit release、v1p16 離線包。
依據（唯一）：decisions/interface_spec.md v2（§0 共通、§1.2 動詞表、§2 結束碼、§3 協定、§4 schema、§4.8 離線包、§6 訊息、§7.4 驗收、§8 相容性）、
proposal_v2.md v2.4～v2.9（v2.9 最高優先）、review_v2r7_findings.md 本檔十頁段落（第八輪必修＋選修；備份 .v9）、grilling.md（Q9、Q11、Q15、Q16–Q19、Q23、Q26、Q27、#26、#27）。
只定義 pages_v1_c = [(pid, name, cells), ...]；不寫檔（run_v1_c.py 負責組 mxfile）。
版面規則：12pt；每格一件事；橢圓／菱形由 emit() 用 shape_spacing 補 spacing；頁高 ≤ 2400、寬 ≤ 1650（band_w=1590）；
橙 = 需人處理（1／2／3 且印指令）、紅 = 失敗、綠 = 成功；無待拍板便條（全部已定，用白便條「已定」說明）。
排版器與 helper 直接沿用 disc_v1_b.py（exec 其 helper 段：Flow／_Band／files()／newpage()／foot()／PEND／O12／SUB／RULE／INV…）。"""
import math
exec(open("disc_v1_b.py").read().split("# ================= P5：bootstrap.sh")[0])   # helper（含 gen57 的 v/e/page/顏色）
# v2.16-3：執行紀錄事件名一律用 spec §4.10 註冊表名（launcher_start／launcher_exit／engine_start／engine_exit）；
# 不論 disc_v1_b 的 TR() 對照表怎麼寫，本檔輸出前一律把 *_started／*_completed|failed 改回 spec 名（TR 讀全域 _TRC，故只換表）。
import re as _re2
_TRC = [(p_, r_) for p_, r_ in _TRC if "launcher_" not in p_.pattern and "engine_" not in p_.pattern]
_TRC += [(_re2.compile(r"launcher_started"), "launcher_start"), (_re2.compile(r"launcher_completed\|failed"), "launcher_exit"), (_re2.compile(r"launcher_completed"), "launcher_exit"),
         (_re2.compile(r"engine_started"), "engine_start"), (_re2.compile(r"engine_completed\|failed"), "engine_exit"), (_re2.compile(r"engine_completed"), "engine_exit")]

# ---------- 本檔補充樣式 ----------
U, L, E, G, P = "下游使用者", "啟動器（主機 sh）", "引擎容器", "GHCR", "專案目錄"   # 泳道名（v2.15-1 名詞換新；不依賴 disc_v1_b 的常數）
_files_b = _Band.files
def _files_c(self, cid, col, row, title, items, w, ax="c", cols=1, cw=None):
    """同 disc_v1_b 的 files()，但內框右緣距容器 20px（check_margin_label；左 8 + 右 20）。"""
    if cw is None: cw = [(w - 28 - 6 * (cols - 1)) // cols] * cols
    return _files_b(self, cid, col, row, title, items, w, ax, cols, cw)
_Band.files = _files_c
BAND_W = 1590                                                                            # 頁寬 ≤ 1650：20 + 1590 + 40
STATE = W12 + "fontStyle=1;strokeWidth=2;"                                               # 粗框白格 = 狀態（metadata state 值）
ENTRY = _12(ELLIPSE("#ffffff")) + "dashed=1;"                                            # 白底虛線橢圓 = 來自其他頁（v2.6-15）
TCELL0 = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#999999;fontSize=12;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;strokeWidth=1;"
def TCELL(fill="#ffffff", bold=False): return TCELL0 + f"fillColor={fill};" + ("fontStyle=1;" if bold else "")
C_OK, C_ACT, C_FAIL = GREEN, ORANGE, RED                                                 # 表格底色 = 結束碼顏色
# 圖例（v2.15-1／-2：名詞換新、執行紀錄事件改用圖例約定；不依賴 disc_v1_b 的 LEG1／LEG2 文字）
LEG1 = [(LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", 200, 60, 0), (RHOMBUS, "黃：判斷", 140, 64, 0),
        (ELLIPSE(GREEN), "綠：起點／終點", 150, 44, 8), (ELLIPSE(RED), "紅：失敗（拉不到／寫不進／驗證不過）", 210, 56, 2),
        (ELLIPSE(ORANGE), "橙：需人處理（1／3 印指令；2 解衝突）", 200, 56, 2),
        (LEAF(), "白：啟動器做", 100, 40, 10), (FILE, "虛線框：專案裡的檔案", 170, 40, 10)]
LEG2 = [("entry", ENTRY, "白虛線橢圓：跨頁入口／出口", 250), ("note", NOTE, "便條：補充說明", 120), ("rule", RULE, "橘框：規則（已定）", 150),
        ("inv", INV, "紅粗框：不變量", 130), ("sub", SUB, "藍：引擎做（容器內）", 170), ("img", IMG, "紫：image（引擎與下游）", 170),
        ("hdr", HDR, "灰底：泳道／表格表頭", 170), ("v2", v2(W12), "右上綠標 v2：與 v1 不同處", 200),
        ("state", STATE, "粗框白格：狀態（state 值）", 200),
        ("c0", TCELL(C_OK), "綠格：結束碼 0", 110),
        ("cx", TCELL(C_ACT), "橙格：需人處理（1／2／3）", 190),
        ("c1", TCELL(C_FAIL), "紅格：失敗 1", 110),
        ("cell", TCELL(), "白格：表格內容", 110)]
ALL = {"note", "rule", "inv", "sub", "img", "hdr", "v2"}
ALLC = ALL | {"state", "entry", "c0", "cx", "c1", "cell"}
CONV1 = "圖例約定①：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_exit（每個結束碼都寫）"
CONV2 = "圖例約定②：每個「docker run 引擎」格隱含 —— 容器開始寫 engine_start（失敗 → 1 + 6-38、不做任何動作）、結束寫 engine_exit"

def foot(cells, prefix, y, rows, keys, conv=True, white="白：啟動器做"):
    """圖例兩列 + 兩條執行紀錄約定（流程頁）+ 本頁名詞（兩欄；只列第 0 頁沒有的詞）。white = 白格在本頁的意思（release 頁 = CI job）。"""
    x = 40
    for i, (st, t, w, h, dy) in enumerate(LEG1):
        emit(cells, f"{prefix}_lg{i}", "1", _12(st), white if t.startswith("白：") else t, x, y + dy, w, h); x += w + 20
    cells.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序（指向檔案時 = 寫入／讀取）", x, y, 260, 60))
    x = 40
    for k, st, t, w in LEG2:
        if k in keys: emit(cells, f"{prefix}_lgx_{k}", "1", st, t, x, y + 68, w, 36); x += w + 20
    yy = y + 112
    if conv:
        cells.append(v(f"{prefix}_lgx_conv1", "1", TEXT(12) + "align=left;", CONV1, 40, yy, 1560, 24)); yy += 26
        cells.append(v(f"{prefix}_lgx_conv2", "1", TEXT(12) + "align=left;", CONV2, 40, yy, 1560, 24)); yy += 26
    cells += terms2(prefix, 40, yy + 40, rows)

NOTE_C = NOTE + "spacingRight=22;"                                                       # 便條右側留白：文字不貼右框、不進摺角（release 便條溢出修，v2.8-8）
def pend_c(cells, text, x=1040, w=560):
    """同 pend()，但便條寬 560、右側 spacing 22（折行寬以 w−32 估、高度多留 12px）。"""
    h = fit_h(text, w - 16, 40, 12)
    cells.append(v("pend", "1", NOTE_C, text, x, 12, w, h)); return 12 + h

def newpage_c(title, note, cols, gap=20, headers=True):
    """同 newpage()，但 band 寬 1590（頁寬 ≤ 1650）、可調列距、可不畫泳道表頭；便條用 pend_c（右側留白）。"""
    cells = [v("title", "1", TITLE, title, 40, 20, 1000, 34)]
    ny = pend_c(cells, note)
    F = Flow(cells, cols, band_w=BAND_W, gap=gap)
    if headers: F.headers(ny + 8)
    else: F.y = ny + 8 + 44
    return cells, F

def table(cells, prefix, x, y, cols, rows, fills=None, hh=30):
    """簡單表格：cols = [(標題, 寬)]；rows = [[文字…]]；fills = {(r, c): 底色}；第一欄粗體。回傳結束 y。"""
    cx = x
    for i, (t, w) in enumerate(cols):
        cells.append(v(f"{prefix}_h{i}", "1", HDR, t, cx, y, w, hh)); cx += w
    cy = y + hh
    for r, row in enumerate(rows):
        hs = [fit_h(s, w, 30) for s, (_, w) in zip(row, cols)]
        rh = max(hs); cx = x
        for c, (s, (_, w)) in enumerate(zip(row, cols)):
            fill = (fills or {}).get((r, c), "#ffffff")
            cells.append(v(f"{prefix}_r{r}c{c}", "1", TCELL(fill, bold=(c == 0)), s, cx, cy, w, rh)); cx += w
        cy += rh
    return cy

def geo(b):
    """close() 之前先算出 band 內每格的絕對座標（與 _Band.close() 同一套公式），供自環／自由標籤定位。"""
    f = b.f; g = f.gap
    nrows = max(bb["row"] for bb in b.boxes) + 1
    rh = [max([bb["h"] for bb in b.boxes if bb["row"] == r] or [0]) for r in range(nrows)]
    y = f.y + 30 + b.pad; top = []
    for r in range(nrows): top.append(y); y += rh[r] + g
    A = {}
    for bb in b.boxes:
        cx, cw = f.cols[bb["col"]]; ax = bb["ax"]
        x = cx + (cw - bb["w"]) / 2 if ax == "c" else cx if ax == "l" else cx + cw - bb["w"] if ax == "r" else cx + ax
        A[bb["id"]] = (x, top[bb["row"]] + (rh[bb["row"]] - bb["h"]) / 2, bb["w"], bb["h"])
    return A

def selfloop(b, eid, cid, label, lw=150):
    """自環（v2.7-3；v2.15 codex #26 標籤貼近自環）：從格子右側 0.7 出去、繞到右下、從底邊 0.8 進來；標籤緊貼環的底段右側下方（不壓線、不壓格、不與到終點的直線混淆）。"""
    x, y, w, h = geo(b)[cid]
    rx, ly = x + w + 14, y + h + 18
    b.P(eid, cid, cid, "", (1, 0.7), (0.8, 1), [(rx, y + 0.7 * h), (rx, ly), (x + 0.8 * w, ly)])
    b.free(f"{eid}_l", TEXT(12) + "align=left;verticalAlign=top;", "↑ " + label, x + 0.8 * w + 12 - b.f.bx, ly + 2 - b.f.y, lw, minh=20)

_close_b = _Band.close
def _close_apex(self):
    """D 線的目標是菱形 → 入口固定 (0.5, 0) 頂點（不讓 al 對齊把入口移到斜邊，review r6 qe11／qe20／ue6）：
    來源不是菱形時把來源出口移到目標中心 x（落在 0.1–0.9 內才移，否則保留折線進頂點）。"""
    A = geo(self)

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
我會使用 `implement` 技能依附件逐頁修改；先完整讀取技能規範並跑兩個基線產生器，再只碰你允許的 a／c 頁面。之後會跑你列出的全部幾何檢查與 lint，並逐頁彙整修改和待處理便條。
exec
/usr/bin/bash -lc "sed -n '1,240p' /home/cyc/.agents/skills/implement/SKILL.md" in <scratchpad>
 succeeded in 0ms:
---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

codex
`implement` 規範要求完成後做一次 code review 並提交目前分支；我會遵守，但會先檢查工作樹，避免把別人同時修改的 `disc_v1_b.py` 或其他既有變更帶進提交。現在先執行基線。
exec
/usr/bin/bash -lc 'git status --short && python3 run_v1_a.py && python3 run_v1_c.py' in <scratchpad>
 exited 128 in 0ms:
fatal: not a git repository (or any of the parent directories): .git

codex
目前 scratchpad 不是 Git 工作樹，所以技能要求的提交在此環境不可行；這不影響檔案修改與驗證。我會記錄這個限制，現在直接跑基線產生器。
exec
/usr/bin/bash -lc 'python3 run_v1_a.py && python3 run_v1_c.py' in <scratchpad>
 succeeded in 122ms:
v1p9 流程 v2：prune（1）resolve → 差集 → 刪 page ('1650', '2317') cells 125
v1p9c 流程 v2：prune（2）apply 清暫存 page ('1650', '1646') cells 90
v1p10 流程 v2：update page ('1650', '2259') cells 115
v1p11 狀態機 v2：初始檔五態 page ('1650', '2127') cells 79
v1p12 狀態機 v2：交易與進度檔 page ('1650', '2363') cells 144
v1p13 相容性矩陣 v2 page ('1650', '1235') cells 74
v1p14 結束碼決策表 v2 page ('1650', '1430') cells 122
v1p15 流程 v2：vendor_kit release（1）build 與驗收 page ('1650', '2128') cells 98
v1p15c 流程 v2：vendor_kit release（2）推 image 與資產 page ('1650', '1621') cells 86
v1p16 流程 v2：離線包（1）bootstrap.sh --local page ('1650', '2267') cells 117
v1p16i 流程 v2：離線包（1′）docker run install page ('1650', '1580') cells 73
v1p16c 流程 v2：離線包（2）add --local 逐工具 page ('1650', '1826') cells 97
v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply page ('1650', '1450') cells 69
v1p16cc 流程 v2：離線包（3）斷網 sync page ('1650', '1795') cells 82
v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證 page ('1650', '1582') cells 72
v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝 page ('1650', '1959') cells 112

exec
/usr/bin/bash -lc "rg -n '"'^# ([-=]+|----------)|pages_v1_[ac]'"\\.append|newpage_c\\(' disc_v1_a.py disc_v1_c.py | tail -n 180" in <scratchpad>
 succeeded in 0ms:
disc_v1_c.py:18:# ---------- 本檔補充樣式 ----------
disc_v1_c.py:71:def newpage_c(title, note, cols, gap=20, headers=True):
disc_v1_c.py:148:# ================= P9：prune（1）resolve → 差集 → 刪 =================
disc_v1_c.py:165:p9, F = newpage_c("流程 v2：prune（1）── resolve keep 清單 → 依 label 列資源 → 差集 → 刪（§1.2、§3.3）", N9, COLS_PR, gap=14)
disc_v1_c.py:218:# --dry-run：只印差集後直接續 apply prune --dry-run：走下游使用者欄與啟動器欄之間（x=250），標籤放垂直段左側、落在下游使用者欄空的列（q11b 列）
disc_v1_c.py:225:pages_v1_c.append(("v1p9", "流程 v2：prune（1）resolve → 差集 → 刪", p9))
disc_v1_c.py:227:# ================= P9c：prune（2）apply 清暫存 → 刪進度檔 → 摘要 =================
disc_v1_c.py:228:p9c, F = newpage_c("流程 v2：prune（2）── apply prune：清暫存 → 刪進度檔 → 摘要（§1.2、§4.6）", N9, COLS_PR, gap=14)
disc_v1_c.py:262:pages_v1_c.append(("v1p9c", "流程 v2：prune（2）apply 清暫存", p9c))
disc_v1_c.py:264:# ================= P10：update =================
disc_v1_c.py:278:p10, F = newpage_c("流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）", N10, COLS_UP, gap=16)
disc_v1_c.py:322:pages_v1_c.append(("v1p10", "流程 v2：update", p10))
disc_v1_c.py:324:# ================= P11：初始檔五態 =================
disc_v1_c.py:338:p11, F = newpage_c("狀態機 v2：初始檔五態 ── metadata [[file]].state 與轉移（interface_spec §4.3、Q14／Q15、v2.7-3）", N11, COLS_ST, gap=130, headers=False)
disc_v1_c.py:378:pages_v1_c.append(("v1p11", "狀態機 v2：初始檔五態", p11))
disc_v1_c.py:380:# ================= P12：交易與進度檔 =================
disc_v1_c.py:393:p12, F = newpage_c("狀態機 v2：交易與進度檔（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）", N12, COLS_TX, gap=12)
disc_v1_c.py:460:pages_v1_c.append(("v1p12", "狀態機 v2：交易與進度檔", p12))
disc_v1_c.py:462:# ================= P13：相容性矩陣 =================
disc_v1_c.py:503:pages_v1_c.append(("v1p13", "相容性矩陣 v2", p13))
disc_v1_c.py:505:# ================= P14：結束碼決策表 =================
disc_v1_c.py:549:pages_v1_c.append(("v1p14", "結束碼決策表 v2", p14))
disc_v1_c.py:551:# ================= P15：vendor_kit release（1）build → 測試 → 驗收 =================
disc_v1_c.py:572:p15, F = newpage_c("流程 v2：vendor_kit release（1）── build → release-test → 候選 tag → 驗收（#26／#27、§7.4）", N15, COLS_RL, gap=28)
disc_v1_c.py:617:pages_v1_c.append(("v1p15", "流程 v2：vendor_kit release（1）build 與驗收", p15))
disc_v1_c.py:619:# ================= P15c：vendor_kit release（2）資產 → 正式 tag → Release =================
disc_v1_c.py:620:p15c, F = newpage_c("流程 v2：vendor_kit release（2）── 資產 → 正式 tag → Release（#26／#27、Q26）", N15, COLS_RL)
disc_v1_c.py:652:pages_v1_c.append(("v1p15c", "流程 v2：vendor_kit release（2）推 image 與資產", p15c))
disc_v1_c.py:654:# ================= P16：離線包（1）bootstrap.sh --local =================
disc_v1_c.py:675:p16, F = newpage_c("流程 v2：離線包（1）── bootstrap.sh --local → 判別值 → load → image ID → 介面版（#27、Q26）", N16, COLS_OF1, gap=14)
disc_v1_c.py:725:pages_v1_c.append(("v1p16", "流程 v2：離線包（1）bootstrap.sh --local", p16))
disc_v1_c.py:727:# ================= P16i：離線包（1′）docker run install =================
disc_v1_c.py:728:p16i, F = newpage_c("流程 v2：離線包（1′）── docker run 本機 image install → version.local.toml（#27、Q26、§4.8）", N16, COLS_OF, gap=14)
disc_v1_c.py:751:pages_v1_c.append(("v1p16i", "流程 v2：離線包（1′）docker run install", p16i))
disc_v1_c.py:753:# ================= P16c：離線包（2）add --local 逐工具 =================
disc_v1_c.py:757:p16c, F = newpage_c("流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具（Q26、§4.8、§7.4-16）", N16, COLS_OF2, gap=14)
disc_v1_c.py:792:pages_v1_c.append(("v1p16c", "流程 v2：離線包（2）add --local 逐工具", p16c))
disc_v1_c.py:794:# ================= P16cb：離線包（2′）add --local：create／cp → apply（第十六輪自（2）拆頁）=================
disc_v1_c.py:796:p16cb, F = newpage_c("流程 v2：離線包（2′）── add --local：docker create／cp → apply add（Q26、§4.8、§7.4-16）", N16, COLS_OF2, gap=14)
disc_v1_c.py:822:pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
disc_v1_c.py:824:# ================= P16cc：離線包（3）斷網 sync：快路徑 → inspect → resolve =================
disc_v1_c.py:826:p16cc, F = newpage_c("流程 v2：離線包（3）── 斷網 sync：快路徑 → inspect（本機覆寫優先）→ docker run resolve（Q26、§3.6）", N16, COLS_OF2, gap=14)
disc_v1_c.py:864:pages_v1_c.append(("v1p16cc", "流程 v2：離線包（3）斷網 sync", p16cc))
disc_v1_c.py:866:# ================= P16ccb：離線包（3″）resolve sync 驗證 → apply|no（第十六輪自（3）拆頁）=================
disc_v1_c.py:868:p16ccb, F = newpage_c("流程 v2：離線包（3″）── resolve sync：驗 image ID → 三叉 → 6-33／6-13 → apply|no？（Q26、§3.6）", N16, COLS_OF2, gap=14)
disc_v1_c.py:891:pages_v1_c.append(("v1p16ccb", "流程 v2：離線包（3″）resolve sync 驗證", p16ccb))
disc_v1_c.py:893:# ================= P16ccc：離線包（3′）apply sync：先驗後重裝一次 =================
disc_v1_c.py:895:p16ccc, F = newpage_c("流程 v2：離線包（3′）── apply sync：先驗既有 cache、不符才重裝一次（Q26、§3.6）", N16, COLS_OF2, gap=14)
disc_v1_c.py:940:pages_v1_c.append(("v1p16ccc", "流程 v2：離線包（3′）apply sync 先驗後重裝", p16ccc))
disc_v1_a.py:13:# ---------- 本檔共用樣式 ----------
disc_v1_a.py:292:# ---------- 名詞總表（每頁只挑自己用到的）----------
disc_v1_a.py:425:# ---------- 審閱頁（md 定稿版逐字移植）共用 ----------
disc_v1_a.py:462:# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
disc_v1_a.py:466:# ---- 三方與承諾關係 ----
disc_v1_a.py:479:# ---- VK 組件 ----
disc_v1_a.py:502:# ---- 常用詞 ----
disc_v1_a.py:538:pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
disc_v1_a.py:540:# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
disc_v1_a.py:545:pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
disc_v1_a.py:547:# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
disc_v1_a.py:562:# ---- 語法記法 ----
disc_v1_a.py:592:# ---- 動詞 ----
disc_v1_a.py:610:pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
disc_v1_a.py:612:# ================= P1 v1p1：審閱頁 01 不變量與角色 =================
disc_v1_a.py:628:# ---- 三方角色表 ----
disc_v1_a.py:647:pages_v1_a.append(("v1p1", "不變量與角色（1）目的／名詞／角色", p1))
disc_v1_a.py:649:# ================= P1i v1p1i：審閱頁 01 不變量與角色（2）=================
disc_v1_a.py:652:# ---- 不變量 I1–I18（一條一格）----
disc_v1_a.py:678:# ---- 例外清單 ----
disc_v1_a.py:694:# ---- 本頁待拍板 ----
disc_v1_a.py:702:pages_v1_a.append(("v1p1i", "不變量與角色（2）不變量／例外／待拍板", p1i))
disc_v1_a.py:705:# ================= P1b v1p1b：契約① 動詞介面表 =================
disc_v1_a.py:807:pages_v1_a.append(("v1p1b", "契約 v2：動詞介面表", p1b))
disc_v1_a.py:809:# ================= P1c v1p1c：契約① 規則、選項表、不開的動詞 =================
disc_v1_a.py:813:# ---- 左上：兩層成對 + 規則框；右上：選項總表 ----
disc_v1_a.py:856:# ---- 結束碼總表（全寬）----
disc_v1_a.py:869:# ---- 訊息文字（左右兩表）----
disc_v1_a.py:941:pages_v1_a.append(("v1p1c", "契約 v2：規則、選項表、不開的動詞", p1c))
disc_v1_a.py:943:# ================= P2 v1p2：契約② 目錄樹與檔案範例 =================
disc_v1_a.py:947:# ---- 左：目錄樹 ----
disc_v1_a.py:1000:# ---- 右欄：檔案範例（等寬字）----
disc_v1_a.py:1053:pages_v1_a.append(("v1p2", "契約 v2：目錄樹與檔案範例", p2))
disc_v1_a.py:1055:# ================= P2b v1p2b：契約② schema =================
disc_v1_a.py:1120:# ---- 左欄 ----
disc_v1_a.py:1135:# ---- 右欄 ----
disc_v1_a.py:1150:pages_v1_a.append(("v1p2b", "契約 v2：schema：version.toml／local／metadata／印記／薄殼首行", p2b))
disc_v1_a.py:1152:# ================= P2c v1p2c：契約② 動詞 × 檔案矩陣 =================
disc_v1_a.py:1214:pages_v1_a.append(("v1p2c", "契約 v2：動詞 × 檔案矩陣", p2c))
disc_v1_a.py:1216:# ================= P3 v1p3：契約③ 下游 repo =================
disc_v1_a.py:1303:pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
disc_v1_a.py:1305:# ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
disc_v1_a.py:1361:# ---- 規則框內容 ----
disc_v1_a.py:1410:# ---- 規則框排版（兩欄 750）----
disc_v1_a.py:1524:pages_v1_a.append(("v1p3b", "契約 v2：啟動器 ↔ 引擎契約④", p3b))
disc_v1_a.py:1526:# ================= P3bb v1p3bb：契約④（2）規則框（第十六輪自 p3b 拆頁）=================
disc_v1_a.py:1541:pages_v1_a.append(("v1p3bb", "契約 v2：啟動器 ↔ 引擎契約④（2）規則", p3bb))
disc_v1_a.py:1543:# ================= P3c v1p3c：契約⑤ CI 與驗收矩陣 =================
disc_v1_a.py:1692:pages_v1_a.append(("v1p3c", "契約 v2：CI 契約⑤ 與驗收矩陣", p3c))
disc_v1_a.py:1694:# ================= P3d v1p3d：契約⑤ 驗收矩陣詳表 =================
disc_v1_a.py:1709:pages_v1_a.append(("v1p3d", "契約 v2：驗收矩陣詳表", p3d))
disc_v1_a.py:1711:# ================= P4 v1p4：架構圖 v2 ── 主機、啟動器、引擎 8 模組、registry =================
disc_v1_a.py:1725:# ---- 啟動器（左上，主機上方）與 GHCR（右上）----
disc_v1_a.py:1750:# ---- 引擎模組（先算高度）----
disc_v1_a.py:1807:# ---- 主機（just 載入鏈與目錄；啟動器另在右上）----
disc_v1_a.py:1862:# ---- 引擎容器 ----
disc_v1_a.py:1886:# ---- 專案目錄（平面分組框，標題靠右上：左上留給啟動器兩條線進 config.toml／log/）----
disc_v1_a.py:1913:# ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
disc_v1_a.py:1946:pages_v1_a.append(("v1p4", "架構圖 v2", p4))

codex
基線可正常產生。接下來我先跑完整機械檢查，藉此把附件中已經在現況修好的項目排除，只改仍實際存在的問題；這也能避免不必要地擾動指定頁。
2026-09-20T15:45:36.331341Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/bash -lc 'set -o pipefail\\nfor f in v1_a.drawio v1_c.drawio; do\\n  echo \\\"$f\\\"\\n  for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py check_margin_label.py; do python3 \\\"$c\\\" \\\"$f\\\"; done\\ndone\\nrm -rf /tmp/v1a_extract /tmp/v1c_extract\\npython3 extract_pages.py v1_a.drawio /tmp/v1a_extract\\npython3 lint_pages.py /tmp/v1a_extract\\npython3 extract_pages.py v1_c.drawio /tmp/v1c_extract\\npython3 lint_pages.py /tmp/v1c_extract\\nsed -n '\\\"'1,240p' /tmp/v1a_extract/lint.md\\nsed -n '1,300p' /tmp/v1c_extract/lint.md\\\"` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
exec
/usr/bin/bash -lc 'set -o pipefail
for f in v1_a.drawio v1_c.drawio; do
  echo "$f"
  for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py check_margin_label.py; do python3 "$c" "$f"; done
done
AOUT=$(mktemp -d /tmp/v1a_extract.XXXXXX)
COUT=$(mktemp -d /tmp/v1c_extract.XXXXXX)
python3 extract_pages.py v1_a.drawio "$AOUT"
python3 lint_pages.py "$AOUT"
python3 extract_pages.py v1_c.drawio "$COUT"
python3 lint_pages.py "$COUT"
echo "AOUT=$AOUT"
echo "COUT=$COUT"
sed -n '"'1,240p' \""'$AOUT/lint.md"
sed -n '"'1,300p' \""'$COUT/lint.md"' in <scratchpad>
 succeeded in 1736ms:
== v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
   無
== v1p0c 名詞與縮寫（2）常用詞（續）
   無
== v1p0b 名詞與縮寫（3）既有詞／記法／動詞
   無
== v1p1 不變量與角色（1）目的／名詞／角色
   無
== v1p1i 不變量與角色（2）不變量／例外／待拍板
   無
== v1p1b 契約 v2：動詞介面表
   無
== v1p1c 契約 v2：規則、選項表、不開的動詞
   無
== v1p2 契約 v2：目錄樹與檔案範例
   無
== v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
   無
== v1p2c 契約 v2：動詞 × 檔案矩陣
   無
== v1p3 契約 v2：下游 repo 契約③
   無
== v1p3b 契約 v2：啟動器 ↔ 引擎契約④
   無
== v1p3bb 契約 v2：啟動器 ↔ 引擎契約④（2）規則
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
== v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
   無
== v1p0c 名詞與縮寫（2）常用詞（續）
   無
== v1p0b 名詞與縮寫（3）既有詞／記法／動詞
   無
== v1p1 不變量與角色（1）目的／名詞／角色
   無
== v1p1i 不變量與角色（2）不變量／例外／待拍板
   無
== v1p1b 契約 v2：動詞介面表
   無
== v1p1c 契約 v2：規則、選項表、不開的動詞
   無
== v1p2 契約 v2：目錄樹與檔案範例
   無
== v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
   無
== v1p2c 契約 v2：動詞 × 檔案矩陣
   無
== v1p3 契約 v2：下游 repo 契約③
   無
== v1p3b 契約 v2：啟動器 ↔ 引擎契約④
   無
== v1p3bb 契約 v2：啟動器 ↔ 引擎契約④（2）規則
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
== v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
   無
== v1p0c 名詞與縮寫（2）常用詞（續）
   無
== v1p0b 名詞與縮寫（3）既有詞／記法／動詞
   無
== v1p1 不變量與角色（1）目的／名詞／角色
   無
== v1p1i 不變量與角色（2）不變量／例外／待拍板
   無
== v1p1b 契約 v2：動詞介面表
   無
== v1p1c 契約 v2：規則、選項表、不開的動詞
   無
== v1p2 契約 v2：目錄樹與檔案範例
   無
== v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
   無
== v1p2c 契約 v2：動詞 × 檔案矩陣
   無
== v1p3 契約 v2：下游 repo 契約③
   無
== v1p3b 契約 v2：啟動器 ↔ 引擎契約④
   無
== v1p3bb 契約 v2：啟動器 ↔ 引擎契約④（2）規則
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
== v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
   無
== v1p0c 名詞與縮寫（2）常用詞（續）
   無
== v1p0b 名詞與縮寫（3）既有詞／記法／動詞
   無
== v1p1 不變量與角色（1）目的／名詞／角色
   無
== v1p1i 不變量與角色（2）不變量／例外／待拍板
   無
== v1p1b 契約 v2：動詞介面表
   無
== v1p1c 契約 v2：規則、選項表、不開的動詞
   無
== v1p2 契約 v2：目錄樹與檔案範例
   無
== v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
   無
== v1p2c 契約 v2：動詞 × 檔案矩陣
   無
== v1p3 契約 v2：下游 repo 契約③
   無
== v1p3b 契約 v2：啟動器 ↔ 引擎契約④
   無
== v1p3bb 契約 v2：啟動器 ↔ 引擎契約④（2）規則
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
共 0 筆
== 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
   無
== 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
   無
== 流程 v2：bootstrap.sh（1′）docker run install
   無
== 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
   無
== 流程 v2：install（1）主機檢查 → 引擎 image → docker run
   無
== 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
   無
== 流程 v2：install（1″）寫入
   無
== 流程 v2：install（2）根 justfile 與 .dockerignore
   無
== 流程 v2：add（1）resolve → docker
   無
== 流程 v2：add（1′）apply 前置
   無
== 流程 v2：add（2）apply 寫入段
   無
== 流程 v2：sync（1）啟動器快路徑
   無
== 流程 v2：sync（1′）引擎 resolve
   無
== 流程 v2：sync（2）三叉 → docker → apply 前置
   無
== 流程 v2：sync（2′）apply 寫入段
   無
== 流程 v2：upgrade ── A. Renovate 路徑
   無
== 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
   無
== 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
   無
== 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
   無
== 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
   無
== 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
   無
== 流程 v2：upgrade ── D. 回退
   無
== 流程 v2：upgrade ── E. 升引擎 (a)(b)
   無
== 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
   無
== 流程 v2：dev <repo>
   無
== 流程 v2：dev vendor_kit
   無
== 流程 v2：undev <repo>（1）resolve → apply 前置
   無
== 流程 v2：undev <repo>（2）寫入段
   無
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
== v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
   無
== v1p0c 名詞與縮寫（2）常用詞（續）
   無
== v1p0b 名詞與縮寫（3）既有詞／記法／動詞
   無
== v1p1 不變量與角色（1）目的／名詞／角色
   無
== v1p1i 不變量與角色（2）不變量／例外／待拍板
   無
== v1p1b 契約 v2：動詞介面表
   無
== v1p1c 契約 v2：規則、選項表、不開的動詞
   無
== v1p2 契約 v2：目錄樹與檔案範例
   無
== v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
   無
== v1p2c 契約 v2：動詞 × 檔案矩陣
   無
== v1p3 契約 v2：下游 repo 契約③
   無
== v1p3b 契約 v2：啟動器 ↔ 引擎契約④
   無
== v1p3bb 契約 v2：啟動器 ↔ 引擎契約④（2）規則
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
v1_c.drawio
== v1p9 流程 v2：prune（1）resolve → 差集 → 刪
   無
== v1p9c 流程 v2：prune（2）apply 清暫存
   無
== v1p10 流程 v2：update
   無
== v1p11 狀態機 v2：初始檔五態
   無
== v1p12 狀態機 v2：交易與進度檔
   無
== v1p13 相容性矩陣 v2
   無
== v1p14 結束碼決策表 v2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   無
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
== v1p9 流程 v2：prune（1）resolve → 差集 → 刪
   無
== v1p9c 流程 v2：prune（2）apply 清暫存
   無
== v1p10 流程 v2：update
   無
== v1p11 狀態機 v2：初始檔五態
   無
== v1p12 狀態機 v2：交易與進度檔
   無
== v1p13 相容性矩陣 v2
   無
== v1p14 結束碼決策表 v2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   無
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
== v1p9 流程 v2：prune（1）resolve → 差集 → 刪
   無
== v1p9c 流程 v2：prune（2）apply 清暫存
   無
== v1p10 流程 v2：update
   無
== v1p11 狀態機 v2：初始檔五態
   無
== v1p12 狀態機 v2：交易與進度檔
   無
== v1p13 相容性矩陣 v2
   無
== v1p14 結束碼決策表 v2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   無
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
== v1p9 流程 v2：prune（1）resolve → 差集 → 刪
   無
== v1p9c 流程 v2：prune（2）apply 清暫存
   無
== v1p10 流程 v2：update
   無
== v1p11 狀態機 v2：初始檔五態
   無
== v1p12 狀態機 v2：交易與進度檔
   無
== v1p13 相容性矩陣 v2
   無
== v1p14 結束碼決策表 v2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   無
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
v1p16cc we2a w2q→w2a dx=3
v1p16ccb we6q w4m→w4q dx=10
v1p16ccc wf6y w4v1q→w4tq dx=20
共 3 筆
== 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
   無
== 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
   無
== 流程 v2：bootstrap.sh（1′）docker run install
   無
== 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
   無
== 流程 v2：install（1）主機檢查 → 引擎 image → docker run
   無
== 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
   無
== 流程 v2：install（1″）寫入
   無
== 流程 v2：install（2）根 justfile 與 .dockerignore
   無
== 流程 v2：add（1）resolve → docker
   無
== 流程 v2：add（1′）apply 前置
   無
== 流程 v2：add（2）apply 寫入段
   無
== 流程 v2：sync（1）啟動器快路徑
   無
== 流程 v2：sync（1′）引擎 resolve
   無
== 流程 v2：sync（2）三叉 → docker → apply 前置
   無
== 流程 v2：sync（2′）apply 寫入段
   無
== 流程 v2：upgrade ── A. Renovate 路徑
   無
== 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
   無
== 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
   無
== 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
   無
== 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
   無
== 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
   無
== 流程 v2：upgrade ── D. 回退
   無
== 流程 v2：upgrade ── E. 升引擎 (a)(b)
   無
== 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
   無
== 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
   無
== 流程 v2：dev <repo>
   無
== 流程 v2：dev vendor_kit
   無
== 流程 v2：undev <repo>（1）resolve → apply 前置
   無
== 流程 v2：undev <repo>（2）寫入段
   無
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
== v1p9 流程 v2：prune（1）resolve → 差集 → 刪
   無
== v1p9c 流程 v2：prune（2）apply 清暫存
   無
== v1p10 流程 v2：update
   無
== v1p11 狀態機 v2：初始檔五態
   無
== v1p12 狀態機 v2：交易與進度檔
   無
== v1p13 相容性矩陣 v2
   無
== v1p14 結束碼決策表 v2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   無
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
v1p0       nodes=  94 edges=  0 terms= 0 xrefs= 0  名詞與縮寫（1）三方／組件／模組／常用詞
v1p0c      nodes=  65 edges=  0 terms= 0 xrefs= 0  名詞與縮寫（2）常用詞（續）
v1p0b      nodes=  89 edges=  0 terms= 0 xrefs= 0  名詞與縮寫（3）既有詞／記法／動詞
v1p1       nodes=  56 edges=  0 terms= 0 xrefs= 0  不變量與角色（1）目的／名詞／角色
v1p1i      nodes=  30 edges=  0 terms= 0 xrefs= 0  不變量與角色（2）不變量／例外／待拍板
v1p1b      nodes= 141 edges=  0 terms= 6 xrefs= 0  契約 v2：動詞介面表
v1p1c      nodes= 240 edges=  4 terms= 7 xrefs= 0  契約 v2：規則、選項表、不開的動詞
v1p2       nodes=  84 edges= 28 terms= 8 xrefs= 0  契約 v2：目錄樹與檔案範例
v1p2b      nodes= 146 edges=  0 terms=10 xrefs= 0  契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
v1p2c      nodes= 221 edges=  0 terms= 7 xrefs= 0  契約 v2：動詞 × 檔案矩陣
v1p3       nodes=  93 edges=  0 terms=16 xrefs= 0  契約 v2：下游 repo 契約③
v1p3b      nodes= 109 edges= 27 terms= 7 xrefs= 0  契約 v2：啟動器 ↔ 引擎契約④
v1p3bb     nodes=  30 edges=  0 terms= 6 xrefs= 3  契約 v2：啟動器 ↔ 引擎契約④（2）規則
v1p3c      nodes= 103 edges= 31 terms= 8 xrefs= 0  契約 v2：CI 契約⑤ 與驗收矩陣
v1p3d      nodes= 135 edges=  0 terms= 7 xrefs= 0  契約 v2：驗收矩陣詳表
v1p4       nodes= 154 edges= 41 terms= 8 xrefs= 0  架構圖 v2
共 16 頁 → /tmp/v1a_extract.HFU9ty/
頁數 16；條目 295（warn 235、info 60）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 16 |
| decision | 0 | 0 |
| endcolor | 0 | 0 |
| xref | 0 | 0 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 5 |
| termcov | 232 | 11 |
| onething | 0 | 28 |
| event-name | 0 | 0 |
→ /tmp/v1a_extract.HFU9ty/lint.md, lint.json
v1p9       nodes=  80 edges= 36 terms= 8 xrefs= 2  流程 v2：prune（1）resolve → 差集 → 刪
v1p9c      nodes=  61 edges= 22 terms= 7 xrefs= 2  流程 v2：prune（2）apply 清暫存
v1p10      nodes=  71 edges= 33 terms= 8 xrefs= 0  流程 v2：update
v1p11      nodes=  62 edges= 15 terms= 8 xrefs= 0  狀態機 v2：初始檔五態
v1p12      nodes=  93 edges= 43 terms= 7 xrefs= 1  狀態機 v2：交易與進度檔
v1p13      nodes=  74 edges=  0 terms= 7 xrefs= 0  相容性矩陣 v2
v1p14      nodes= 122 edges=  0 terms= 7 xrefs= 0  結束碼決策表 v2
v1p15      nodes=  67 edges= 28 terms= 8 xrefs= 2  流程 v2：vendor_kit release（1）build 與驗收
v1p15c     nodes=  58 edges= 21 terms= 6 xrefs= 1  流程 v2：vendor_kit release（2）推 image 與資產
v1p16      nodes=  70 edges= 32 terms= 6 xrefs= 1  流程 v2：離線包（1）bootstrap.sh --local
v1p16i     nodes=  55 edges= 13 terms= 6 xrefs= 6  流程 v2：離線包（1′）docker run install
v1p16c     nodes=  65 edges= 23 terms= 7 xrefs= 2  流程 v2：離線包（2）add --local 逐工具
v1p16cb    nodes=  50 edges= 16 terms= 4 xrefs= 4  流程 v2：離線包（2′）add --local：create／cp → apply
v1p16cc    nodes=  53 edges= 19 terms= 4 xrefs= 1  流程 v2：離線包（3）斷網 sync
v1p16ccb   nodes=  45 edges= 14 terms= 3 xrefs= 3  流程 v2：離線包（3″）resolve sync 驗證
v1p16ccc   nodes=  66 edges= 29 terms= 6 xrefs= 1  流程 v2：離線包（3′）apply sync 先驗後重裝
共 16 頁 → /tmp/v1c_extract.6Y5zD2/
頁數 16；條目 138（warn 52、info 86）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 2 |
| decision | 0 | 8 |
| endcolor | 0 | 3 |
| xref | 0 | 5 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 44 | 16 |
| onething | 0 | 52 |
| event-name | 0 | 0 |
→ /tmp/v1c_extract.6Y5zD2/lint.md, lint.json
AOUT=/tmp/v1a_extract.HFU9ty
COUT=/tmp/v1c_extract.6Y5zD2
# lint.md

頁數 16；條目 295（warn 235、info 60）

| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 16 |
| decision | 0 | 0 |
| endcolor | 0 | 0 |
| xref | 0 | 0 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 5 |
| termcov | 232 | 11 |
| onething | 0 | 28 |
| event-name | 0 | 0 |
| resolve-3way | 0 | 0 |
| precheck-recover | 0 | 0 |
| end-color-text | 0 | 0 |
| xref-forward | 0 | 0 |
| write-line | 0 | 0 |
| write-fail-edge | 0 | 0 |
| term-count | 2 | 0 |
| term-dup-page0 | 1 | 0 |
| page-height | 0 | 0 |
| edge-font | 0 | 0 |
| merge-fanout | 0 | 0 |

## v1p0 名詞與縮寫（1）三方／組件／模組／常用詞
nodes 94／edges 0／terms 0；warn 10、info 4
- [dangling][info] -: 非流程頁，略過懸空檢查
- [color][info] -: 此頁沒有圖例，略過顏色檢查
- [termcov][warn] p0_t1_r1c2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t3_r0c1: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t3_r1c2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t3_r5c2: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r1c2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r1c2: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r1c2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r1c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r3c2: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0_t4_r6c2: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [onething][info] p0_c2: [step] 分隔詞 7（、6 ；1）：「薄殼：.vendor_kit/ 內進 git、由引擎產生、人不改的五個檔（entry.just、vendor.just、log.sh、.gitignore、ci/check.sh）；五檔用同一套自描述標頭（通常在首行，ci/check.sh 在第二行）與 hash 契約。」
- [onething][info] p0_c3: [step] 分隔詞 3（、2 ；1）：「啟動器：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；bootstrap.sh 是第一次接入時的啟動器。」

## v1p0c 名詞與縮寫（2）常用詞（續）
nodes 65／edges 0／terms 0；warn 10、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [color][info] -: 此頁沒有圖例，略過顏色檢查
- [termcov][warn] p0c_t4_r1c2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r1c2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r2c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r3c2: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r9c0: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r9c0: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r10c2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r14c2: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r14c2: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0c_t4_r17c2: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）

## v1p0b 名詞與縮寫（3）既有詞／記法／動詞
nodes 89／edges 0／terms 0；warn 10、info 7
- [dangling][info] -: 非流程頁，略過懸空檢查
- [color][info] -: 此頁沒有圖例，略過顏色檢查
- [termcov][warn] p0b_t1_r1c2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t1_r4c0: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t1_r4c2: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t1_r4c2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t1_r5c2: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t1_r6c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_o8: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t3_r0c1: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t3_r0c1: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p0b_t3_r0c1: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [onething][info] p0b_o0: [step] 分隔詞 4（、4）：「動詞表用到的選項（短形只有 -t、-y、-p、-i、-h）：」
- [onething][info] p0b_o6: [step] 分隔詞 6（、5 ；1）：「--dry-run：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。」
- [onething][info] p0b_o8: [step] 分隔詞 5（→3 ；2）：「--local <tar>：add 離線：只收存在的 .tar 離線包。bootstrap.sh 的 --local <image tag／tar> 另可收本機 image tag，值依序判別：以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 / 且存在同名檔 → 1 要求消歧；否則 → image tag。」
- [onething][info] p0b_o12: [step] 分隔詞 5（、4 ；1）：「--timeout <秒>：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、bootstrap.sh）都接受。」
- [onething][info] p0b_v1: [step] 分隔詞 3（然後1 再1 、1）：「升引擎 = upgrade vendor_kit[@<tag>]：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。」

## v1p1 不變量與角色（1）目的／名詞／角色
nodes 56／edges 0／terms 0；warn 5、info 5
- [dangling][info] -: 非流程頁，略過懸空檢查
- [color][info] -: 此頁沒有圖例，略過顏色檢查
- [termcov][warn] p1_tm_r1c0: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_tm_r4c1: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_tm_r6c0: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_tr1_r3c1: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_tr1_r3c1: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [onething][info] p1_intro: [step] 分隔詞 2（、1 ；1）：「本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。」
- [onething][info] p1_auto0: [step] 分隔詞 6（、5 ；1）：「下游 CI：專案自己的 CI 平台（GitHub、GitLab 都一樣）只呼叫契約檢查腳本；腳本自己把 CI 設為 1 進 CI 模式，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。」
- [onething][info] p1_auto1: [step] 分隔詞 2（再1 ；1）：「Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，大版本升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。」

## v1p1i 不變量與角色（2）不變量／例外／待拍板
nodes 30／edges 0／terms 0；warn 9、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [color][info] -: 此頁沒有圖例，略過顏色檢查
- [termcov][warn] p1_i2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i4: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i9: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i12: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i17: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_i18: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1_x3: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）

## v1p1b 契約 v2：動詞介面表
nodes 141／edges 0／terms 6；warn 33、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] p1B_r0c2_0: 「6-16」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r0c2_0: 「6-23」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r0c2_2: 「6-31」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r0c2_5: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c0: 「6-17」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_0: 「6-35」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_0: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_1: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_1: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_2: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_3: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_4: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_4: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r1c2_4: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r2c2_1: 「.tmp.uninstall」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r3c2_0: 「6-3」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r3c2_3: 「6-11」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r3c2_3: 「6-21」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r3c2_6: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r4c2_1: 「.tmp.remove」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r5c2_1: 「6-15」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r6c2_1: 「6-14」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r6c2_2: 「6-22」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r6c2_5: 「6-6」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r6c2_5: 「6-8」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r8c2_2: 「6-10」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r10c2_0: 「.tmp.undev」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r10c2_1: 「6-1」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r11c2_1: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r11c2_3: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r11c3: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1B_r12c2_1: 「6-32」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 7 個關鍵字只在名詞說明文出現、沒有獨立條（略）：--local、version.toml、metadata、cache/、.tmp.dist、6-2b、6-2
- [term-dup-page0][warn] resolve／apply: 名詞「resolve／apply」第 0 頁已有（同名或只差結尾括號），不必重列

## v1p1c 契約 v2：規則、選項表、不開的動詞
nodes 240／edges 4／terms 7；warn 40、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] p1C_s2: 「6-9」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_s2: 「6-35」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_s3: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_dry: 「6-6」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_dry: 「6-8」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_dry: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_dry: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r1c2: 「6-2」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r1c2: 「6-1」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r1c2: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r3c2: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r3c2: 「6-19」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_ex_r3c2: 「6-10」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r0c1: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r2c0: 「6-2b」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r4c0: 「6-4」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r5c0: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r5c1: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r6c0: 「6-7」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r9c0: 「6-11」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r9c2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r10c0: 「6-12」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r11c0: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r12c0: 「6-14」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r13c0: 「6-15」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r14c0: 「6-16」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mL_r15c0: 「6-17」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r1c0: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r2c0: 「6-21」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r3c0: 「6-22」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r4c0: 「6-23」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r5c0: 「6-24」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r6c0: 「6-26」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r6c1: 「flock」（flock）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r8c0: 「6-29」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r9c0: 「6-30」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r11c0: 「6-32」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r12c0: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r13c0: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p1C_mR_r13c2: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 7 個關鍵字只在名詞說明文出現、沒有獨立條（略）：gen/tools.just、resolve、薄殼、6-36、6-3、6-31、gen/

## v1p2 契約 v2：目錄樹與檔案範例
nodes 84／edges 28／terms 8；warn 11、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] t_di: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_di: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_di: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_ver: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_ver: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_vl: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_vl: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_log: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] t_tmp: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2_jf_n: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2_sh_n: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 6 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml、薄殼、gen/tools.just、metadata、6-1、resolve

## v1p2b 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
nodes 146／edges 0／terms 10；warn 12、info 5
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] p2b_ver_m: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_ver_m: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_vl_l: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_vl_r4c2: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_tmp_r0c1: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_mt_l: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_mt_r2c2: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_mt_r4c2: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_sh_r0c1: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_sh_r6c1: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2b_sh_r6c1: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 9 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-19、version.toml、--local、gen/tools.just、薄殼、metadata、resolve、6-6、6-8
- [onething][info] p2b_ver_m: [step] 分隔詞 4（、1 ；3）：「進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；下游使用者、Renovate 可手改；sync 只讀」
- [onething][info] p2b_vl_m: [step] 分隔詞 9（→1 再1 ；7）：「不進 git（自有 .gitignore 擋）；與 version.toml 同形（同一套讀寫器）；寫入者 dev／undev／bootstrap --local；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；CI 模式下存在任何覆寫 → sync 回 1；啟動器先讀它再退回 version.toml」
- [onething][info] p2b_mt_m: [step] 分隔詞 5（並1 ；4）：「進 git；寫入者 add／upgrade；兼作 baseline/<repo>/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列。註：install 對根 .dockerignore 的四行 append 不屬任何工具，記於 baseline/.vendor_kit.toml（同檔案版，只含 [[file]] dest=.dockerignore state=appended lines=四行），uninstall 讀它刪原文相同行」
- [term-count][warn] -: 名詞表 10 條 > 8

## v1p2c 契約 v2：動詞 × 檔案矩陣
nodes 221／edges 0／terms 7；warn 20、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] p2c_tc_r0c1: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_tc_r2c1: 「6-11」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_tc_r2c1: 「6-21」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_tc_r2c1: 「6-22」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_l: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_l: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_h2: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_r0c2: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_r0c5: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_mx_r8c6: 「6-1」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] p2c_my_h2: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
# lint.md

頁數 16；條目 138（warn 52、info 86）

| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 2 |
| decision | 0 | 8 |
| endcolor | 0 | 3 |
| xref | 0 | 5 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 44 | 16 |
| onething | 0 | 52 |
| event-name | 0 | 0 |
| resolve-3way | 0 | 0 |
| precheck-recover | 0 | 0 |
| end-color-text | 1 | 0 |
| xref-forward | 0 | 0 |
| write-line | 0 | 0 |
| write-fail-edge | 7 | 0 |
| term-count | 0 | 0 |
| term-dup-page0 | 0 | 0 |
| page-height | 0 | 0 |
| edge-font | 0 | 0 |
| merge-fanout | 0 | 0 |

## v1p9 流程 v2：prune（1）resolve → 差集 → 刪
nodes 80／edges 36／terms 8；warn 1、info 7
- [termcov][warn] q0l: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 9 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-4、version.toml、apply、resolve、6-38、version.local.toml、6-33、6-30、6-32
- [onething][info] q3: [step] 分隔詞 2（、2）：「算保留清單 keep：引擎 ref、[tools] 每個工具 ref、本機覆寫的 vendor_kit <tag>」
- [onething][info] q4y: [step] 分隔詞 3（並1 、2）：「是：只列出並印 6-33（prune 例外：不刪、不恢復、不視為未完成交易）」
- [onething][info] q5: [step] 分隔詞 3（、3）：「stdout vk-resolve/1：keep|<name>|<ref>…、fingerprint、apply|yes、end|N」
- [onething][info] q5x: [end_orange] 分隔詞 2（→1 、1）：「否 → 1／2／3 原碼傳出：不讀 stdout、不動 docker」
- [onething][info] q10tx: [end_orange] 分隔詞 2（→1 ；1）：「否 → 1 + 6-4：需要確認但沒有終端；請加 -y」
- [onething][info] q10n: [end_ok] 分隔詞 2（→1 、1）：「否 → 0：不刪、印清單」

## v1p9c 流程 v2：prune（2）apply 清暫存
nodes 61／edges 22／terms 7；warn 4、info 6
- [endcolor][info] q13x: 紅終點文字含需人動作字眼（候選改橙）：「否 → 1：摘要全列、失敗的標出；進度檔留著（下次可寫動詞先恢復：補做失敗的刪除」
- [termcov][info] -: 5 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-4、version.toml、6-26、6-12、.tmp.prune
- [onething][info] q12dy: [end_ok] 分隔詞 2（→1 ；1）：「是 → 0：只列出會清的暫存與殘留（零刪除；不建進度檔）」
- [onething][info] q12j: [step] 分隔詞 2（、1 ；1）：「否：建進度檔 .tmp.prune.<id>.toml（第一個寫入前；state=in-progress、done／pending）」
- [onething][info] q13x: [end_red] 分隔詞 3（→1 、1 ；1）：「否 → 1：摘要全列、失敗的標出；進度檔留著（下次可寫動詞先恢復：補做失敗的刪除）」
- [onething][info] q14: [end_ok] 分隔詞 2（→1 、1）：「→ 0：印刪了什麼、保留什麼（含原因）」
- [write-fail-edge][warn] q12j: 寫入格缺失敗出邊或失敗匯流：「否：建進度檔 .tmp.prune.<id>.toml（第一個寫入前；state」
- [write-fail-edge][warn] q12c: 寫入格缺失敗出邊或失敗匯流：「刪 trap 沒清到的殘留啟動器暫存 .tmp.dist.<id>/」
- [write-fail-edge][warn] q12d2: 寫入格缺失敗出邊或失敗匯流：「刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列」
- [write-fail-edge][warn] q12k: 寫入格缺失敗出邊或失敗匯流：「是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成」

## v1p10 流程 v2：update
nodes 71／edges 33／terms 8；warn 4、info 7
- [decision][info] ue5: 菱形 u3 出邊標籤不以是／否開頭：「(無標籤)」
- [termcov][warn] pend: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] u0l: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] u0x: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] u2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 1 個關鍵字只在名詞說明文出現、沒有獨立條（略）：resolve
- [onething][info] u3x: [end_orange] 分隔詞 3（→1 、1 ；1）：「是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔；末行仍印 6-15）」
- [onething][info] u7f: [step] 分隔詞 3（→2 ；1）：「該目標記 1（無憑證 → 6-3，不查；否則附分類）→ 繼續下一目標」
- [onething][info] u8b: [step] 分隔詞 2（→2）：「與現版比較 → 記「現版 → 最新」」
- [onething][info] u9: [step] 分隔詞 4（→1 、1 ；2）：「否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的分類與 6-3）；訊息全列」
- [onething][info] u11x: [end_orange] 分隔詞 3（→1 ；2）：「是 → 1：查詢失敗（6-3：設 token 或指定 <repo>@<tag>；其他分類印原因；即使另有新版）」

## v1p11 狀態機 v2：初始檔五態
nodes 62／edges 15／terms 8；warn 0、info 1
- [termcov][info] -: 4 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-6、6-8、6-7、baseline/

## v1p12 狀態機 v2：交易與進度檔
nodes 93／edges 43／terms 7；warn 2、info 13
- [decision][info] te9a: 菱形 t6q 出邊標籤不以是／否開頭：「(無標籤)」
- [decision][info] re4n: 菱形 r2p 出邊標籤不以是／否開頭：「(無標籤)」
- [endcolor][info] t6xb: 紅終點文字含需人動作字眼（候選改橙）：「否 → 1：明列已完成／未完成、進度檔留著（下次可寫動詞先恢復）」
- [termcov][warn] pend: 「6-9」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] pend: 「.tmp.dev」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 11 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-33、resolve、version.toml、6-26、6-12、metadata、.tmp.install、.tmp.upgrade、log/、gen/tools.just、6-27
- [onething][info] t3y: [end_ok] 分隔詞 2（→1 ；1）：「是 → 0：唯讀預覽；不建進度檔（CI 例外見右）」
- [onething][info] t4: [step] 分隔詞 6（、6）：「否：建進度檔（第一個寫入前）：state=in-progress、verb、id、started、targets、done[]／pending[]、consents」
- [onething][info] t5b: [step] 分隔詞 2（→1 ；1）：「逐步寫入 ②：原子替換（rename 暫存檔 → 目標檔；一檔一次換上）」
- [onething][info] t6xb: [end_red] 分隔詞 2（→1 、1）：「否 → 1：明列已完成／未完成、進度檔留著（下次可寫動詞先恢復）」
- [onething][info] t6xa: [end_red] 分隔詞 2（→1 、1）：「是 → 1：依進度檔（清除清單）移除已寫的檔、不留半成品（log/ 保留）」
- [onething][info] t8c: [end_orange] 分隔詞 2（→1 ；1）：「是 → 2：有合併衝突（留標記；解完重跑）」
- [onething][info] r1: [step] 分隔詞 2（、2）：「偵測未完成交易：.vendor_kit/.tmp.<verb>.*.toml（含 .tmp.install.*、.tmp.dev.*、.tmp.upgrade.*）或任一 metadata [progress] state=in-progress」
- [onething][info] r3x: [end_orange] 分隔詞 2（→1 、1）：「否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）」
- [onething][info] r5x: [end_red] 分隔詞 2（→1 ；1）：「否 → 1 + 6-27「未恢復：<檔名>」逐檔列出；進度檔留著」

## v1p13 相容性矩陣 v2
nodes 74／edges 0／terms 7；warn 4、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] tb_r1c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] k13c: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] k13c: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] k13e: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 2 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-2、resolve

## v1p14 結束碼決策表 v2
nodes 122／edges 0／terms 7；warn 11、info 2
- [dangling][info] -: 非流程頁，略過懸空檢查
- [termcov][warn] te_r0c3: 「6-24」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r0c3: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r1c2: 「6-35」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r1c2: 「6-17」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r1c2: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r6c1: 「6-14」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r6c2: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r6c2: 「6-2b」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r7c1: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] te_r9c2: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] k14f: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 18 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-15、6-18、6-3、6-16、6-23、6-4、6-31、薄殼、6-19、6-12、6-27、version.toml…

## v1p15 流程 v2：vendor_kit release（1）build 與驗收
nodes 67／edges 28／terms 8；warn 0、info 6
- [termcov][info] -: 1 個關鍵字只在名詞說明文出現、沒有獨立條（略）：version.toml
- [onething][info] v3b: [step] 分隔詞 6（→6）：「release-test：完整主機流程 install → add → upgrade → dev/undev → remove → prune → uninstall」
- [onething][info] v3x: [end_red] 分隔詞 2（→1 、1）：「否 → 失敗：候選作廢（不推 image、不發 Release）」
- [onething][info] v8cx: [end_red] 分隔詞 3（→1 、2）：「否 → 失敗：候選 tag 留著、不打正式 vN、不發 Release（候選作廢）」
- [onething][info] v4x: [end_red] 分隔詞 2（→1 ；1）：「否 → 失敗：候選作廢；印失敗的條號」
- [onething][info] v7x: [end_red] 分隔詞 3（→1 、1 ；1）：「否 → 失敗：不發 Release、不進正式 tag（候選作廢；候選 tag 留著）」

## v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
nodes 58／edges 21／terms 6；warn 1、info 6
- [termcov][warn] v10e: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 2 個關鍵字只在名詞說明文出現、沒有獨立條（略）：--local、Renovate
- [onething][info] v9: [step] 分隔詞 2（；2）：「產 bootstrap.sh：內嵌完整引擎 ref（vendor_kit:vN@index digest；digest 與候選 tag 相同）；檔名固定」
- [onething][info] v10a: [step] 分隔詞 2（→1 、1）：「docker save 各平台 image → vendor_kit-vN-amd64.tar、vendor_kit-vN-arm64.tar」
- [onething][info] v10e: [step] 分隔詞 5（、5）：「產 lnav format 檔（§4.10：json、timestamp-field、level-field、opid-field=trace_id、body-field、file-pattern .vendor_kit/log/*/*.jsonl）」
- [onething][info] v10d: [step] 分隔詞 3（、3）：「寫 SHA256SUMS：涵蓋 bootstrap.sh、各平台 tar 與 .digest、離線包、lnav format 檔（不含自身）」
- [onething][info] v11c: [step] 分隔詞 5（、5）：「上傳資產：bootstrap.sh、tar、.digest、離線包、lnav format 檔、SHA256SUMS」

## v1p16 流程 v2：離線包（1）bootstrap.sh --local
nodes 70／edges 32／terms 6；warn 5、info 6
- [endcolor][info] o3tx: 紅終點文字含需人動作字眼（候選改橙）：「否 → 1：本機無此 image（tag 形：先 docker load 或改給」
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o2s: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o7cx: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o7c: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 8 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、6-16、6-23、6-38、6-24、version.local.toml
- [onething][info] o1: [step] 分隔詞 3（、2 ；1）：「解開（SHA256SUMS 驗）：bootstrap.sh、各平台引擎 tar + .digest、local_bootstrap.sh；不含工具 tar」
- [onething][info] o3cx: [end_orange] 分隔詞 2（→1 ；1）：「是 → 1 + 6-37：--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。」
- [onething][info] o3t: [step] 分隔詞 2（→1 、1）：「否 → tag 形：不 load、不讀 .digest」
- [onething][info] o7cx: [end_orange] 分隔詞 2（→1 ；1）：「否 → 3 + 6-18：零寫入（斷網也回 3；請以較新的離線包重建）」
- [end-color-text][warn] o3tx: 終點文字應為 end_orange 但是 end_red：「否 → 1：本機無此 image（tag 形：先 docker load 或改給」

## v1p16i 流程 v2：離線包（1′）docker run install
nodes 55／edges 13／terms 6；warn 3、info 5
- [xref][info] o8e: 引用「install（1′）」頁只靠拆字比對到
- [xref][info] o8e: 引用「install（2）」頁只靠拆字比對到
- [xref][info] o8e2: 引用「install（2）」頁只靠拆字比對到
- [termcov][warn] o8f_1: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o8f_1: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o8f_3: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 8 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、.tmp.install、version.toml、--local、version.local.toml、log/、metadata
- [onething][info] o8x: [end_red] 分隔詞 3（→1 、1 ；1）：「是 → 1：引擎依進度檔清半成品、不留半成品（log/ 保留）；引擎異常結束時由 bootstrap.sh 補清」

## v1p16c 流程 v2：離線包（2）add --local 逐工具
nodes 65／edges 23／terms 7；warn 2、info 3
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o10s: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 8 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、resolve、apply、6-38、6-24、6-30
- [onething][info] o10re2: [step] 分隔詞 3（、3）：「stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N」
- [onething][info] o10rx: [end_orange] 分隔詞 2（→1 、1）：「否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply」

## v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
nodes 50／edges 16／terms 4；warn 6、info 4
- [xref][info] o10z: 引用「add（2）」頁只靠拆字比對到
- [xref][info] o10z2: 引用「add（2）」頁只靠拆字比對到
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o10p: 「.tmp.dist」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o10pgf: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] o10z: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 10 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、digest、--local、metadata、apply、resolve、6-26、6-12
- [onething][info] o11: [end_ok] 分隔詞 2（再1 ；1）：「0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add」
- [write-fail-edge][warn] o10e3: 寫入格缺失敗出邊或失敗匯流：「寫 metadata：source（正式 ref@digest）+ local_」
- [write-fail-edge][warn] o10e4: 寫入格缺失敗出邊或失敗匯流：「寫 version.toml [tools] 行：正式 ref@digest（最」

## v1p16cc 流程 v2：離線包（3）斷網 sync
nodes 53／edges 19／terms 4；warn 3、info 9
- [decision][info] we2ax: 菱形 w2a 出邊標籤不以是／否開頭：「≠」
- [decision][info] we2y: 菱形 w2a 出邊標籤不以是／否開頭：「相符：用本機 tag（不 pull）」
- [decision][info] we3p: 菱形 w3 出邊標籤不以是／否開頭：「無」
- [decision][info] we5: 菱形 w3 出邊標籤不以是／否開頭：「有」
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] w0l: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] w4zz: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 12 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、digest、--local、resolve、6-38、gen/、cache/、version.local.toml、6-24、6-31
- [onething][info] w1: [step] 分隔詞 4（、4）：「快路徑：grep 比對 gen/*.stamp 第一行 vs version.toml（引擎 ref、每工具 digest）、每個 cache/<repo>/ 存在、tools.just 存在、無 .tmp.*」
- [onething][info] w5a: [end_ok] 分隔詞 2（→1 ；1）：「是 → 0：不起容器（sync_fast_path；驗收 §7.4-17）」
- [onething][info] w3x: [end_red] 分隔詞 2（→1 、1）：「否 → 1 + 6-24／6-31：斷網拉不到／逾時（--timeout 內結束、不 hang）」
- [onething][info] w4: [step] 分隔詞 2（→1 ；1）：「docker run（不 pull；本機覆寫相符 → 用本機 tag）resolve sync（永不 -t）」

## v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
nodes 45／edges 14／terms 3；warn 3、info 3
- [decision][info] we6x: 菱形 w4e 出邊標籤不以是／否開頭：「≠」
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] bO2b: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] bO2b: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 10 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、digest、--local、6-33、metadata、resolve、6-30、flock
- [onething][info] w4rx: [end_orange] 分隔詞 2（→1 、1）：「否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply」

## v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
nodes 66／edges 29／terms 6；warn 3、info 6
- [termcov][warn] pend: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][warn] w4x1: 「.tmp.dist」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
- [termcov][info] -: 10 個關鍵字只在名詞說明文出現、沒有獨立條（略）：6-1、6-37、version.toml、digest、--local、apply、resolve、6-26、6-12、cache/
- [onething][info] w5: [end_ok] 分隔詞 2（→1 、1）：「是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）」
- [onething][info] w5t: [end_ok] 分隔詞 2（→1 、1）：「→ 0：cache 相符、已補 tools.just」
- [onething][info] w4r: [step] 分隔詞 2（→1 ；1）：「否：重裝一次：從 /dist 重寫 cache/<repo>/（暫存 → 整批替換；warn）」
- [onething][info] w4r0: [step] 分隔詞 3（→1 、1 ；1）：「否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）」
- [onething][info] w5c: [end_ok] 分隔詞 2（→1 、1）：「→ 0：成功、不起 pull（驗收 §7.4-17）」
- [write-fail-edge][warn] w4r2: 寫入格缺失敗出邊或失敗匯流：「寫印記 gen/<repo>.stamp（index digest + 每檔 s」

exec
/usr/bin/bash -lc "sed -n '1216,1545p' disc_v1_a.py
sed -n '1543,1955p' disc_v1_a.py
sed -n '148,330p' disc_v1_c.py
sed -n '654,945p' disc_v1_c.py" in <scratchpad>
 succeeded in 0ms:
# ================= P3 v1p3：契約③ 下游 repo =================
p3 = head("p3", "契約③ 下游 repo 要交的（供應側；interface_spec §4.7、§4.8、§3.6；改了要升 major 並公告）", 1200)
c, Y = nopend("p3", 1260, 12, 340, "dist/files/ 的 symlink 已定禁止；dist 文字檔一律 LF、check.sh --dist 擋 CRLF 已定於 issue #29；Dockerfile.dist 必含 LABEL（16 條必修）")
p3.append(c); Y = max(Y + 16, 96)
DIST_T = ("<repo>/                  # 下游 repo\n"
 "├─ dist/\n"
 "│  ├─ files/…            # 全部出貨（原樣展開）\n"
 "│  ├─ init.toml          # 初始檔清單（下表）\n"
 "│  └─ just/<ns>.just     # 一檔一命名空間（含 _sync）\n"
 "└─ Dockerfile.dist       # 逐字三行（下框）")
DOCK_T = "FROM scratch\nLABEL io.github.<org>.vendor_kit=1\nCOPY dist/ /dist/"
DW = 440; RXd = 480; R1W = (1540 - RXd - 3 * 16) // 4
D_ROW1 = [
 ("d4_1", LT12, "<b>dist/files/</b>\n全部出貨；fetch 原樣展開到 .vendor_kit/cache/<repo>/files/（引擎展開時也驗右欄 CI 的檔案規則）", True),
 ("d4_2", LT12, "<b>dist/init.toml</b>\nschema、description（單行）、[[file]] src／dest／strategy=\"copy\"|\"append\"（預設 copy），dest 相對專案根；用 copy 指向根 .gitignore／.dockerignore／.editorconfig → --dist 報錯（要用 append）；欄位表見下", True),
 ("d4_3", LT12, "<b>dist/just/<ns>.just</b>\n每檔一個頂層命名空間，數量工具自決，<repo>.just 必須存在；每檔含私有 _sync（F1，見下）；撞名 → add 拒絕；recipe 用 cd {{quote(justfile_directory())}} 回專案根（禁止相對 working-directory）", True),
 ("d4_4", LT12, "<b>Dockerfile.dist</b>\n逐字三行：FROM scratch／LABEL io.github.<org>.vendor_kit=1／COPY dist/ /dist/；純資料，不承諾可執行、vendor_kit 不檢查 binary（Q21：只搬移）；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加，pull 無法追加）", True),
]
D_ROW2 = [
 ("d4_5", PT12, "<b>下游 image</b>\nghcr.io/<org>/<repo>-dist:<tag>\n多架構 amd64 + arm64（同一次 buildx、COPY-only；CI 驗兩平台位元組一致）；version.toml 與印記記 index digest（#26）；公開／私有自決（公開不可逆）；已釋出 image／index 子 digest 永不刪；LABEL …vendor_kit=1", True),
 ("d4_6", PT12, "<b>引擎 image</b>\nghcr.io/<org>/vendor_kit:vN\n公開；多架構（只驗兩平台 LABEL 一致）；LABEL …vendor_kit=1、.protocol=<floor_P>-<current_P>、.schema=<N>（啟動器不起容器即可判最低介面版）；每平台 docker save tar + .digest 旁檔；Release 資產永不刪", True),
 ("d4_7", LT12, "<b>下游 repo 的 CI</b>\n跑 vendor_kit 出貨的 check.sh --dist：dist 佈局、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、files/ 禁 symlink／hardlink／特殊檔、文字檔一律 LF [#29]、just 1.33.0 解析每個 <ns>.just、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台一致", True),
 ("d4_8", LT12, "<b>deploy（一句話契約）</b>\n工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml、GHCR（需要的檔打包時複製進去）；vendor_kit 不檢查；保證方式 = 下游 repo 自己在乾淨機器解包驗收；version.toml 公開格式可供來源紀錄", True),
]
DEST_T = ("<b>dest 規則（引擎在任何寫入前驗，不只供應端 lint）</b>：src 相對 dist/、正規化、不得越出 dist/；dest 相對專案根、正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；"
 "兩工具同 dest：copy/copy、copy/append → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查（含新版新增 <ns>／dest 的全域撞名）")
INIT_T = ("schema = 1\ndescription = \"<repo> 的專案範本與 just recipe\"\n\n"
 "[[file]]\nsrc = \"files/Dockerfile\"\ndest = \"Dockerfile\"\n\n"
 "[[file]]\nsrc = \"files/gitignore.snippet\"\ndest = \".gitignore\"\nstrategy = \"append\"")
INIT_COLS = [("欄位", 170), ("型別／必填", 110), ("說明", 470)]
INIT_ROWS = [
 ["schema", "integer／是", "建置期契約（同 image 內讀寫），不進執行期矩陣"],
 ["description", "string／否", "頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod? 上方 # <description>；缺則 <repo> <tag>"],
 ["[[file]].src", "string／是", "相對 dist/；正規化、不得越出 dist/"],
 ["[[file]].dest", "string／是", "相對專案根；正規化、不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；跨工具撞 dest 規則見左"],
 ["[[file]].strategy", "string／否", "\"copy\"（預設）或 \"append\"，只有這兩值；根 .gitignore／.dockerignore／.editorconfig 類必須用 append"],
]
SYNC_T = ("[private]\n_sync:\n\tcd {{quote(justfile_directory())}} && just vendor_kit sync\n\n"
 "build: _sync\n\tcd {{quote(justfile_directory())}} && …")
SYNC_R = ("<b>sync 自動前置：工具契約（F1 定案）</b>：每個 dist/just/<ns>.just 必含上列私有 _sync（本體逐字、行首真 tab；justfile_directory() 在模組內 = 專案根；用 quote() 不直接插字串）；工具每個公開 recipe 相依它（例 build: _sync；例外集合：無）；vendor_kit 自身動詞不前置")
SYNC_L = ("<b>sync 自動前置：lint 與限制</b>：check.sh --dist 以 just --dump --dump-format json 檢查：_sync 存在、私有、本體逐字相符、每個公開 recipe 的 dependencies 含 _sync。限制（契約明寫）：just 在執行前已載入所有模組，同一次呼叫內看不到 sync 重建後的新 recipe；cache 缺檔時 mod? 讓 just vendor_kit sync 仍可進入；1.33.0 fixture 通過才算結案")
LBL_COLS = [("資源", 200), ("label（鍵前綴 io.github.<org>.vendor_kit）", 540)]
LBL_ROWS = [
 ["啟動器建的容器／network／volume", "…=1、….project=<專案根絕對路徑>（專案路徑 label 不加在 image 上）"],
 ["引擎 image（build 時）", "…=1、….protocol=<floor_P>-<current_P>、….schema=<N>"],
 ["下游 image（build 時）", "…=1（Dockerfile.dist 必含）"],
 ["prune", "依 label 掃四類資源；image 只刪帶 label 且本專案未引用者；vendor_kit 不建 network／volume（驗收差集為空，故意留的也要能刪）"],
]
CON_T = ("<b>工具契約（初始檔與 recipe）</b>：初始檔只能引用穩定入口 just <ns> …、.vendor_kit/ci/check.sh、.vendor_kit/entry.just、.vendor_kit/version.toml；不得寫死 cache 內部路徑（Q14）；"
 "rename／格式變更不得以 copy/append 假裝完成；工具的 build 若以專案根當 context，依賴 install 加進根 .dockerignore 的排除，不得再以其他方式繞過 .vendor_kit/；dist 可執行性是下游 repo 責任（check.sh --dist + 自己的測試）")
OFF_T = ("<b>離線包（Release 資產；Q26）</b>：每個平台 tar（docker save）旁附同名 .digest 旁檔：<name>.tar + <name>.tar.digest，內容一行 sha256:<hex64> = 該 image 的正式多架構 index digest；另附 local_bootstrap.sh 便利包裝（偵測架構、挑 tar、exec bootstrap.sh --local；非契約、不另定介面）；"
 "bootstrap.sh --local <tar>／add --local <tar>：docker load 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 local_image_id；旁檔缺 → 1。離線可用：啟動器先 docker image inspect，本機有就不 pull；斷網 + 已有 image → sync／build 必須成功；斷網 + 無 image → 1 印 6-31 不 hang；離線 upgrade 不支援")
tmp = []; y = 50
r1h = max(hvt(t, R1W, tg) for _, _, t, tg in D_ROW1); r2h = max(hvt(t, R1W, tg) for _, _, t, tg in D_ROW2)
cells, _, dh = code("p3_dist", "p3L4", DIST_T, 20, y, DW); tmp += cells
tmp.append(v("p3_dock_l", "p3L4", LBL, "Dockerfile.dist（逐字三行；純資料 image）", 20, y + dh + 12, DW, 28))
cells, _, dkh = code("p3_dock", "p3L4", DOCK_T, 20, y + dh + 12 + 32, DW); tmp += cells
dh = dh + 12 + 32 + dkh
x = RXd
for pid, st, t, tg in D_ROW1:
    tmp.extend(vt(pid, "p3L4", st, t, x, y, R1W, r1h, tagged=tg)); x += R1W + 16
x = RXd
for pid, st, t, tg in D_ROW2:
    tmp.extend(vt(pid, "p3L4", st, t, x, y + r1h + 16, R1W, r2h, tagged=tg)); x += R1W + 16
y += max(dh, r1h + 16 + r2h) + 16
y = rbox(tmp, "p3_dest", "p3L4", RULE, DEST_T, 20, y, 1520, tagged=True)
# init.toml：左範例、右欄位表
tmp.append(v("p3_init_l", "p3L4", LBL, "dist/init.toml（逐字範例；欄位說明在下表）", 20, y, 700, 28))
tmp.append(v("p3_sync_l", "p3L4", LBL, "dist/just/<ns>.just 的 _sync（逐字，行首真 tab）與 label 表", 790, y, 700, 28)); y += 32
cells, _, ih = code("p3_init", "p3L4", INIT_T, 20, y, 750); tmp += cells
cells, _, sh_ = code("p3_sync", "p3L4", SYNC_T, 790, y, 750); tmp += cells
yl = tbl(tmp, "p3_initf", "p3L4", 20, y + ih + 10, INIT_COLS, INIT_ROWS, marks={(1, 0), (4, 0)})
yr = tbl(tmp, "p3_lbl", "p3L4", 790, y + sh_ + 10, LBL_COLS, LBL_ROWS, marks={(0, 0), (1, 0), (2, 0), (3, 0)})
y = max(yl, yr) + 14
sh2 = max(hvt(SYNC_R, 750, True), hvt(SYNC_L, 750, True))
tmp += vt("p3_syncr", "p3L4", RULE, SYNC_R, 20, y, 750, sh2, tagged=True)
tmp += vt("p3_syncl", "p3L4", RULE, SYNC_L, 790, y, 750, sh2, tagged=True)
y += sh2 + 14
ch_ = max(hvt(CON_T, 750, True), hvt(OFF_T, 750, True))
tmp += vt("p3_con", "p3L4", RULE, CON_T, 20, y, 750, ch_, tagged=True)
tmp += vt("p3_off", "p3L4", RULE, OFF_T, 790, y, 750, ch_, tagged=True)
y += ch_ + 20
p3.append(v("p3L4", "1", SW(NEUTRAL), "契約③ 下游 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）", 40, Y, 1560, y))
p3 += tmp
Y += y + 20
Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
 ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))

# ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
S0C = "寫 launcher_start\n（完整 argv）失敗 →\n1 印 6-38、零寫入"
S1 = "① 以版本鎖定行 regex grep 引擎 ref\n（version.local.toml 本機覆寫優先；命中 ≠ 1 → 1）\n非 sync 的動詞跳過下一格"
D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
S2A = "讀 version.toml／local\n（CI 模式判定）"
S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
D2_T = "apply|yes？"
OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
S3A = "docker image inspect\n（每筆 pull／extract）"
S3B = "無：docker pull\n（逾時 → 1 印 6-31）"
S3C = "只有 extract kind：\ndocker create（帶 label）\n<ref> /x"
S3D = "docker cp c:/dist/.\n→ .tmp.dist.<id>/\n<repo>/"
S3E = "docker rm\n（trap 也清）"
S4 = "④ docker run 引擎\napply <動詞>（掛 /dist:ro）\n→ 結束碼 0／1／2／3 回 just"
S3BX = "失敗 → 1 印 6-24\n（網路／認證／不存在）"
ERR = "是 → 1 印 6-1\n（請 upgrade vendor_kit；不重寫薄殼）"
W1 = {"s0a": 100, "s0b": 150, "s0c": 170, "s1": 180, "d1": 190, "s2a": 150, "s2b": 190, "s2c": 230}
W2 = {"s3a": 130, "s3b": 120, "s3c": 150, "s3d": 130, "s3e": 90, "s4": 180}
GT = 26; GP = 8; GP3 = 26                                                                              # ③ 分組上方多留空間給「有 → 跳過 pull」旁路線
h1 = {"s0a": hv(S0A, W1["s0a"]), "s0b": hv(S0B, W1["s0b"]), "s0c": hv(S0C, W1["s0c"]), "s1": hv(S1, W1["s1"]), "d1": hvr(D1_T, W1["d1"]), "s2a": hv(S2A, W1["s2a"]), "s2b": hv(S2B, W1["s2b"]), "s2c": hv(S2C, W1["s2c"])}
ih1 = max(h1["s2a"], h1["s2b"], h1["s2c"]); g1h = GT + GP + ih1 + GP
r1top = max(h1["s0a"] / 2, h1["s0b"] / 2, h1["s0c"] / 2, h1["s1"] / 2, h1["d1"] / 2, GT + GP + ih1 / 2); r1bot = max(h1["s0a"] / 2, h1["s0b"] / 2, h1["s0c"] / 2, h1["s1"] / 2, h1["d1"] / 2, ih1 / 2 + GP)
S0X = "1 印 6-38：執行紀錄\n建不了／寫不進（零寫入）"                                                 # ⓪ 寫 launcher_start 失敗（第 0 列紅終點；Claude r13 s0c）
S1X = "1：版本鎖定行命中 ≠ 1\n（0 或重複；列差異不動）"                                              # ① grep 失敗（第 0 列紅終點；Claude r13 s1）
S0XW, S1XW = 180, 200; s0xh = hve(S0X, S0XW); s1xh = hve(S1X, S1XW); row0h = max(s0xh, s1xh)
r1c = 50 + row0h + 18 + r1top; row1h = r1top + r1bot; ROW1_BOT = r1c + r1bot
h2 = {k: hv(t, W2[k]) for k, t in (("s3a", S3A), ("s3b", S3B), ("s3c", S3C), ("s3d", S3D), ("s3e", S3E), ("s4", S4))}
ih2 = max(h2["s3a"], h2["s3b"], h2["s3c"], h2["s3d"], h2["s3e"]); g2h = GT + GP3 + ih2 + GP
D2W = 180; d2h = hvr(D2_T, D2W)
r2top = max(GT + GP3 + ih2 / 2, h2["s4"] / 2, d2h / 2); r2bot = max(ih2 / 2 + GP, h2["s4"] / 2, d2h / 2)
row2h = r2top + r2bot
ERR_W = 260
eh = hve(ERR, ERR_W)
r2y = ROW1_BOT + 70                                                                                   # 列間 70：d1「是」線 +18、d2_in「resolve 0」線 +40，離 ③ 分組頂邊 30（Claude r13 d2_in）
r2c = r2y + r2top
OKW = 260; okh = hve(OK_T, OKW)
S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
r3y = r2y + max(row2h, eh) + 34
okY = r3y
S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
U5C = "0：已列出\n（末行 6-15）"; U5D = "1／2：查詢失敗／\n--exit-code 有新版"
U5W = {"u5a": 230, "u5b": 300, "u5c": 140, "u5d": 190}
u5h = max(hv(U5A, U5W["u5a"]), hv(U5B, U5W["u5b"]), hve(U5C, U5W["u5c"]), hve(U5D, U5W["u5d"]))
RX_T = "resolve 非 0 → 原碼傳出\n（不讀 stdout、不跑 docker／apply）"
RXW = 230; rxh = hve(RX_T, RXW)
r4y = okY + max(okh, s3bxh, s4xh, rxh) + 18
u5y = r4y + 32; r5y = u5y + u5h + 18                                                                  # 第 4 列：單段 update（v2.16-17：update 不在 resolve 段、另畫）
# ---- 規則框內容 ----
WL_T = ("<b>主機命令白名單（16 條必修；lint 擋清單外）</b>：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、mkdir、date、od、tr（v2.13 P7：建 log/、時間戳、trace_id）、rm、sleep、git rev-parse、"
 "docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files。"
 "啟動器 = POSIX sh（vendor.just 內的 recipe 殼）：不裝 python、不解析 TOML、不 eval；路徑含空白、$、非 ASCII 一律引號")
RUN_T = ("<b>docker run 參數</b>：docker run --rm [<uid 旗標>] -v \"<專案根>:/repo\" -w /repo [-v \"<專案根>/.vendor_kit/.tmp.dist.<id>:/dist:ro\"] [-v \"<dir>/dist:/dist/<repo>:ro\"]… "
 "[-v \"<TOKEN_FILE>:/run/vk-token:ro\" -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] -e TRACEPARENT=00-<trace_id>-<span_id>-<flags>（W3C；引擎只取 trace_id）-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔> [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] "
 "--label io.github.<org>.vendor_kit=1 --label io.github.<org>.vendor_kit.project=<專案根絕對路徑> <引擎 ref> --protocol P <子命令> [args]。"
 "--protocol P（介面版）一律在子命令之前；-w /repo 必給；-it 只在 apply 且互動（有 tty、無 -y、非 CI 模式），resolve 永不 -t；trap … EXIT INT TERM 清容器與 .tmp.dist.<id>/")
UF_T = ("<b>uid 旗標（rootless 不加 -u／Podman keep-id）</b>：docker info --format '{{.SecurityOptions}}' 含 name=rootless → rootless，不加 -u；docker --version 含 podman → 加 --userns=keep-id、不加 -u；其餘（rootful docker）加 -u \"$(id -u):$(id -g)\"")
ENV_T = ("<b>環境變數與 -e 白名單（§5）</b>：轉發 CI（照原值；真值規則：非空且不為 0／false → CI 模式）、VENDOR_KIT_NO_LOCK（=1 跳過 flock）；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update 單段及 upgrade 的 resolve 以 -e 傳（不寫 log／檔、不傳給工具、dry-run 不印）；"
 "VENDOR_KIT_REGISTRY_TOKEN_FILE 改為 -v <主機檔>:/run/vk-token:ro 並以 -e …_TOKEN_FILE=/run/vk-token 傳容器內路徑（與 _TOKEN 同設 → 1「只能擇一」）；啟動器自讀不轉發：VENDOR_KIT_PULL_TIMEOUT（預設 300，--timeout 優先）；"
 "啟動器自產必傳（v2.12）：TRACEPARENT（32 hex trace_id，同值 = 進度檔交易 id）與 VENDOR_KIT_LOG_FILE（容器內路徑；引擎 append 同一檔，不另開檔）；"
 "其餘一律不轉發（HTTP_PROXY 等 → v2）；README 列出全部 VENDOR_KIT_* 與 CI，lint 擋未列者；引擎容器內 LC_ALL=C.UTF-8、TZ=UTC、HOME=<容器內暫存>")
IMG_T = ("<b>引擎 image 取得</b>：一律先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull <ref>（逾時）。本機覆寫時：docker image inspect <tag> 的 .Id 必須 == version.local.toml vendor_kit_image_id，否則 1；不 pull（不用 docker run 的 pull 旗標：docker 19.03 沒有）。"
 "<b>引擎子命令</b>：單段 install／update／dev／help／upgrade vendor_kit[@<tag>] = --protocol P <verb> [args]；resolve <verb>（只讀、不詢問、不寫檔、無 TTY）；apply <verb> [--dry-run]；內部取件／驗指紋／三方合併不對外")
TWO_T = ("<b>兩段編排的兩個獨立屬性</b>：需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve <verb> → 主機 docker → apply <verb>，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；"
 "單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（add／upgrade 也要先拉 image 展開；uninstall／remove／prune 不拉）。<b>鎖</b>：鎖在引擎 progress 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗印 6-26；VENDOR_KIT_NO_LOCK=1 跳過；啟動器不鎖）。"
 "<b>pull 失敗</b>：印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列「主機錯誤」）+ 僅 add／bootstrap 提示 6-24 的「離線可用 --local」；<b>逾時</b>：VENDOR_KIT_PULL_TIMEOUT／--timeout，預設 300 秒，只收正整數（0 或非數字 → 1）；背景 pull + 每秒輪詢 + kill；逾時 → 1 印 6-31")
LOCK_T = ("<b>apply 通則（所有動詞）</b>：容器開始 append engine_start（失敗 → 1 印 6-38；圖例約定②）→ 讀 /dist/vk-resolve（啟動器把 resolve 原始 stdout 存成 .tmp.dist.<id>/vk-resolve 一起掛入）→ 拿 flock → 重算指紋與計畫中的 fingerprint 比對（不同 → 1 印 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 模式需改進 git 的檔 → 1 印清單）→ "
 "建進度檔（第一個寫入前）→ 其後所有寫入（apply 引擎自己重算計畫與詢問清單，不從 stdout 拿；gen/tools.just 最後寫且與 cache 同一 apply 內原子替換；version.toml 最後）→ 最後一步刪進度檔（uninstall 在根 justfile 那行之後）；不重新選最新版；詢問後、替換前對目標檔再查一次前像；所有合併在暫存完成 → 逐檔原子替換；失敗明列已完成／未完成")
VK_CODE = ("vk-resolve/<P>\n<kind>|<f1>[|<f2>…]\nend|<N>\n\n"
 "vk-resolve/1\nmount|<repo>|/home/me/my\\0040tools\nfingerprint|9a2f…c1\napply|yes\nend|3")
VK_CODE2 = ("vk-resolve/1\nextract|<repo>|ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:bbbb…\nfingerprint|1c0e…77\napply|yes\nend|3")
VK_N = ("左上 = 文法骨架：第一行 vk-resolve/<P>（P = 呼叫方 --protocol 的介面版）；每行一筆 <kind>|<f1>[|<f2>…]（欄位以單一 | 分隔；UTF-8；LF；無空行、無註解；禁 CR／NUL／BOM）；最後一行 end|<N>（N = 記錄行數，之後立即 EOF）。"
 "左下範例 = sync，<repo> 在本機覆寫中（mount；路徑含空白 → \\0040）；右範例 = sync，<repo> 的 cache 過期（extract）。範例工具名一律 <repo>。vk-resolve/1 只傳這裡定義的東西：pull／extract 清單、apply|yes/no、指紋；計畫／詢問清單／保護清單不走 stdout（apply 引擎自己重算）")
VK_COLS = [("kind", 96), ("欄位", 150), ("筆數", 50), ("啟動器動作", 454)]
VK_ROWS = [
 ["pull", "<name>|<ref>", "0..n", "docker image inspect 有則略，否則 docker pull <ref>（逾時／失敗 → 6-31／6-24）；name = vendor_kit 或 <repo>；到此為止（不 create／cp）"],
 ["extract", "<repo>|<ref>", "0..n", "同 pull 後 docker create <ref> /x → docker cp c:/dist/. .tmp.dist.<id>/<repo>/ → docker rm；同一 repo 不得同時有 extract 與 mount"],
 ["mount", "<repo>|<dir 八進位跳脫>", "0..n", "本機覆寫：解碼後驗 <dir>/dist/init.toml 存在（缺 → 1）→ -v \"<dir>/dist:/dist/<repo>:ro\""],
 ["engine", "<ref>", "0..1", "只在 upgrade（不帶 repo）：apply 會把版本鎖定行改成此 ref；啟動器先 pull（本機覆寫時 inspect 驗 ID）；有 engine 時不夾帶工具寫入；E(c) upgrade vendor_kit[@<tag>] 是單段、不走此 kind（目標 ref 記在 .tmp.upgrade.<id>.toml，見「自身升級的接手」）"],
 ["fingerprint", "<sha256 hex64>", "恰 1", "不解析，隨檔交給 apply"],
 ["apply", "yes | no", "恰 1", "no → 驗完文法後直接 exit 0（sync 快路徑；終點仍隱含 launcher_exit，約定①）；no 時不得有 pull／extract／mount／engine；yes → 跑 apply <verb> [--dry-run]"],
 ["keep", "<name>|<ref>", "0..n", "只在 prune：本專案引用、不可刪的 image（含本機覆寫的 <tag>）"],
 ["end", "<N>", "恰 1", "必為最後一行"],
]
VK_R = ("<b>欄位與驗證</b>：安全字串 [A-Za-z0-9_.-]+；ref [A-Za-z0-9_.:/@-]+（引擎以 image-reference parser 驗證後才輸出）；自由文字（路徑）凡不在 [A-Za-z0-9_./:@+=,-] 的 byte 一律寫成 \\0ooo（例：空白 \\0040、| \\0174、\\ \\0134），啟動器一行解碼 dir=$(printf '%b' \"$f2\")、不 eval、不 source；IFS='|' read -r 直接切欄。"
 "啟動器先收完整份存到 .tmp.dist.<id>/vk-resolve、驗文法才動 docker：首行 ≠ vk-resolve/<P>、缺 end、N 不符、end 後仍有資料、未知 kind、欄位數不對、fingerprint／apply 不是恰一筆、no 卻附動作記錄、安全字串含非法字元 → 1 印 6-30；引擎宣稱的介面版真不支援 → 3。"
 "resolve 結束碼非 0 → 啟動器不讀 stdout、不跑 docker／apply、原碼傳出（圖：②→③ 之間的「resolve 非 0」出口）。stderr 一律診斷；apply 的 stdout 不作為協定通道。指紋算法見名詞表")
SELF_T = ("<b>自身升級的接手（§3.4）</b>：「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 版本鎖定行。apply 結束後 ref 變了（且 == 計畫的 engine）→ 以新 ref（本機覆寫有 vendor_kit= 則用該 image、inspect 驗 ID）跑 docker run … <新 ref> --protocol P upgrade vendor_kit，結束碼原樣傳出（預期 1 印 6-2）；"
 "第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b，不再重跑。<b>E(c) upgrade vendor_kit[@<tag>] 的接手（單段；v2.15-13）</b>：現引擎不改第一行、只建 .tmp.upgrade.<id>.toml（記舊 ref、目標 ref、計畫 image ID）→ 啟動器 grep 進度檔取目標引擎 ref（不從 stdout 讀）→ inspect／pull 目標引擎 → docker run <目標引擎> upgrade vendor_kit（同一 TRACEPARENT、append 同一執行紀錄）→ 目標引擎改第一行、重產薄殼、刪進度檔 → 1 印 6-2。<b>救援路徑（§3.5）</b>：install、upgrade vendor_kit[@<tag>]、sync 的「薄殼不符 → 1 印 6-1」判定、help = 單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ 最低介面版的薄殼永遠可經此叫任何引擎重產薄殼")
FAST_T = ("<b>sync 快路徑（Q22）與 sync --verify</b>：sync（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml vendor_kit ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或本機覆寫的 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 CI 模式。"
 "全相符 → 不起容器、0；任一不符或 CI 模式 → 起引擎 resolve sync。每檔 sha256 verify 只在：CI 模式、快路徑有差那次（版本變動）、sync --verify（長形）：先驗既有 cache，不符才重裝一次，再驗仍不符 → 失敗；sync <repo> 一律起引擎驗該範圍。"
 "快路徑仍先寫 launcher_start、結束寫 sync_fast_path／launcher_exit。<b>--local 值的判別（B1，依序互斥；v3.5）</b>：以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；否則含 / 且存在同名檔 → 1 印 6-37「要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔」；否則 → image tag（含 / 但無同名檔的完整 ref 也是 tag 形；只對 bootstrap.sh 有意義，add --local 只收存在的 .tar）")
COMPAT_T = ("<b>相容承諾（Q16／Q19／Q23）</b>：薄殼每次呼叫附 --protocol P（介面版；第一版就有），引擎依 P 回應。永久：任何 ≥ 最低介面版的舊薄殼可呼叫新引擎的救援路徑並得正確提示；舊資料永遠可讀可遷（讀任一舊檔案版 → 直接寫當前檔案版，不鏈式）。"
 "非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 3 印 6-36 零寫入。最低介面版 = 固定 release 常數（v1.0.0、P=1、schema=1），只能經 ADR 提高；引擎 image LABEL …protocol=<floor_P>-<current_P> 讓啟動器不起容器即可判最低介面版。"
 "降版 upgrade vendor_kit@<舊版>：目標引擎（以介面版／檔案版比）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10；dev vendor_kit -i <舊 image> 禁止重產進 git 的薄殼")
ENVR_T = ("<b>執行環境（19 條）與主機需求</b>：docker ≥ 19.03（或 Podman ≥ 4.9）、just ≥ 1.33.0、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA、引擎基底 EOL → issue v2。"
 "時間戳 UTC ISO 8601；需詢問但無 tty／EOF → 1 印 6-4；所有 docker 資源帶 vendor_kit label；不建 network／volume；離線 upgrade 不支援；worktree 進驗收；submodule 以實測為生效條件")
# ---- 規則框排版（兩欄 750）----
tmp = []; y = r5y
CW = 750; RX3 = 790
def pair(idl, tl, idr, tr, y, out=None, par="p3L2"):
    out = tmp if out is None else out
    h = max(hvt(tl, CW, True), hvt(tr, CW, True))
    out.extend(vt(idl, par, RULE, tl, 30, y, CW, h, tagged=True)); out.extend(vt(idr, par, RULE, tr, RX3, y, CW, h, tagged=True))
    return y + h + 14
# 第十六輪拆頁（頁高 ≤ 2400）：本頁 = 流程 + vk-resolve 文法／kind 表 + apply 通則 + 兩段／快路徑；其餘規則框（白名單／執行環境／docker run／環境變數／image 取得／自身升級／uid／相容）移到「契約④（2）」頁 p3bb
y = rbox(tmp, "p3_lock", "p3L2", RULE, LOCK_T, 30, y, 1510, tagged=True)
tmp.append(v("p3_vk_l", "p3L2", LBL, "vk-resolve/1 stdout 文法（Q24；P=1）", 30, y, 700, 28)); tmp.append(v("p3_vkt_l", "p3L2", LBL, "kind 一覽（啟動器動作）", RX3, y, 700, 28)); y += 32
cells, vkw1, vkh = code("p3_vk", "p3L2", VK_CODE, 30, y); tmp += cells
cells, _, vkh2 = code("p3_vk2", "p3L2", VK_CODE2, 30 + vkw1 + 16, y, CW - vkw1 - 16); tmp += cells
vnh = hv(VK_N, CW)
tmp.append(vb("p3_vk_n", "p3L2", NOTE_T, VK_N, 30, y + vkh + 8, CW, vnh))
yl = rbox(tmp, "p3_vkr", "p3L2", RULE, VK_R, 30, y + vkh + 8 + vnh + 10, CW, tagged=True)   # 欄位與驗證放左欄（範例下方），與右欄 kind 表等高（頁高 ≤ 2400）
yr = tbl(tmp, "p3_vkt", "p3L2", RX3, y, VK_COLS, VK_ROWS, marks={(0, 0), (3, 0), (5, 0), (6, 0)})
y = max(yl, yr + 14)
y = pair("p3_two", TWO_T, "p3_fast", FAST_T, y)
l2h = y + 6
p3b.append(v("p3L2", "1", SW(NEUTRAL), "契約④ 啟動器 ↔ 引擎（每格一件事；⓪ 執行紀錄 → ① 啟動器 grep → ② resolve → ③ 主機 docker → ④ apply；規則框 = §3、§5 逐條；白 = 啟動器、藍 = 引擎）", 40, Y, 1560, l2h))
# 第一列：⓪ trace_id → 建執行紀錄 → 寫 launcher_start → ① grep → （只有 sync）gen/.stamp 判斷 → ② resolve
x = 30
p3b.append(v("s0a", "p3L2", L12, S0A, x, r1c - h1["s0a"] / 2, W1["s0a"], h1["s0a"])); x += W1["s0a"] + 16
p3b += vt("s0b", "p3L2", L12, S0B, x, r1c - h1["s0b"] / 2, W1["s0b"], h1["s0b"], tagged=True); x += W1["s0b"] + 16
p3b += vt("s0c", "p3L2", L12, S0C, x, r1c - h1["s0c"] / 2, W1["s0c"], h1["s0c"], tagged=True); x += W1["s0c"] + 16
p3b.append(e("s0b_e", "s0a", "s0b", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s0c_e", "s0b", "s0c", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s1_e", "s0c", "s1", "", (1, 0.5), (0, 0.5)))
p3b.append(v("s1", "p3L2", L12, S1, x, r1c - h1["s1"] / 2, W1["s1"], h1["s1"])); x += W1["s1"] + 16
d1x = x
p3b += vt("d1", "p3L2", RHOMBUS + "fontSize=12;", D1_T, x, r1c - h1["d1"] / 2, W1["d1"], h1["d1"], tagged=True); x += W1["d1"] + 16
p3b.append(e("d1_e", "s1", "d1", "", (1, 0.5), (0, 0.5)))
g1x = x; g1w = GP + W1["s2a"] + 16 + W1["s2b"] + 16 + W1["s2c"] + GP + 12
g1y = r1c - GT - GP - ih1 / 2
p3b.append(v("g2", "p3L2", GRP_T, "② docker run 引擎 resolve <動詞>（只讀、不寫檔、無 TTY；診斷走 stderr；engine_start／engine_exit 依圖例約定②）", g1x, g1y, g1w, g1h))
ux = GP
for pid, t in (("s2a", S2A), ("s2b", S2B), ("s2c", S2C)):
    p3b += vt(pid, "g2", ENG12, t, ux, GT + GP + (ih1 - h1[pid]) / 2, W1[pid], h1[pid], tagged=(pid == "s2b")); ux += W1[pid] + 16   # 藍 = 引擎做的
p3b.append(e("s2a_e", "d1", "s2a", "否", (1, 0.5), (0, 0.5)))
p3b.append(e("s2b_e", "s2a", "s2b", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s2c_e", "s2b", "s2c", "", (1, 0.5), (0, 0.5)))
# 第二列
d1c = d1x + W1["d1"] / 2
ERR_X = 30
p3b.append(v("p3_err", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", ERR, ERR_X, r2y, ERR_W, eh))
AX, AY = 40, Y
midy_err = AY + ROW1_BOT + 18
p3b.append(ew("p3_err_e", "d1", "p3_err", "是", (0.5, 1), (0.5, 0), [(AX + d1c, midy_err), (AX + ERR_X + ERR_W / 2, midy_err)], pos=-0.85))
d2x = ERR_X + ERR_W + 24
p3b.append(v("d2", "p3L2", RHOMBUS + "fontSize=12;", D2_T, d2x, r2c - d2h / 2, D2W, d2h))
g2x = d2x + D2W + 24
g2w = GP + W2["s3a"] + 16 + W2["s3b"] + 16 + W2["s3c"] + 16 + W2["s3d"] + 16 + W2["s3e"] + GP + 12
g2y = r2c - GT - GP3 - ih2 / 2
p3b.append(v("g3", "p3L2", GRP_T, "③ 主機 docker（每筆 pull／extract 記錄；不帶 --platform；先收完 vk-resolve 驗文法才動）", g2x, g2y, g2w, g2h))
ux = GP; s3x = {}
for pid, t in (("s3a", S3A), ("s3b", S3B), ("s3c", S3C), ("s3d", S3D), ("s3e", S3E)):
    s3x[pid] = ux
    p3b += vt(pid, "g3", L12, t, ux, GT + GP3 + (ih2 - h2[pid]) / 2, W2[pid], h2[pid], tagged=(pid in ("s3a", "s3c"))); ux += W2[pid] + 16
x = g2x + g2w + 24
p3b.append(v("s4", "p3L2", L12, S4, x, r2c - h2["s4"] / 2, W2["s4"], h2["s4"]))
s3bx_x = g2x + GP + W2["s3a"] + 16 + W2["s3b"] / 2 - S3BXW / 2                                       # ③ docker pull 失敗 → 紅終點（6-24）
p3b.append(v("s3bx", "p3L2", ELLIPSE(RED) + "fontSize=12;", S3BX, s3bx_x, okY, S3BXW, s3bxh))
p3b.append(e("s3bx_e", "s3b", "s3bx", "失敗", (0.5, 1), (0.5, 0), vert=True))
p3b.append(e("s3b_e", "s3a", "s3b", "無", (1, 0.5), (0, 0.5), vert="below"))
p3b.append(e("s3c_e", "s3b", "s3c", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s3d_e", "s3c", "s3d", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s3e_e", "s3d", "s3e", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s4_e", "s3e", "s4", "", (1, 0.5), (0, 0.5)))
p3b.append(e("d2_e", "d2", "s3a", "是", (1, 0.5), (0, 0.5)))
# ③ inspect 本機已有 → 跳過 pull：從 s3a 頂端上到分組標題下方的空隙，右到 s3c 頂端下來（codex v1p3b #3）
byp_y = AY + g2y + GT + 6
s3a_cx = AX + g2x + s3x["s3a"] + W2["s3a"] / 2; s3c_cx = AX + g2x + s3x["s3c"] + W2["s3c"] / 2
p3b.append(ew("s3a_skip", "s3a", "s3c", "有 → 跳過 pull", (0.5, 0), (0.5, 0), [(s3a_cx, byp_y), (s3c_cx, byp_y)], lab="below", pos=0.0))
# ②c → d2：從 ②c 底邊下到列間，往左到 d2 上方，再下去；resolve 非 0 → 另一條出口到橙終點（不讀 stdout、不跑 docker／apply）
s2c_ax = AX + g1x + GP + W1["s2a"] + 16 + W1["s2b"] + 16 + W1["s2c"] / 2
d2_ax = AX + d2x + D2W / 2
midy = AY + ROW1_BOT + 40
p3b.append(ew("d2_in", "s2c", "d2", "resolve 0", (0.5, 1), (0.5, 0), [(s2c_ax, midy), (d2_ax, midy)], lab="side", pos=-0.9))
rx_x = 1560 - 30 - RXW                                                                                # 橙終點放第三列最右（④ 終點右邊）；線從 ②c 右下出、沿 x=1500 下來（避開 ④ 格）
p3b.append(v("p3_rx", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", RX_T, rx_x, okY, RXW, rxh))
p3b.append(ew("p3_rx_e", "s2c", "p3_rx", "非 0", (0.9, 1), (1, 0.5), [(AX + g1x + GP + W1["s2a"] + 16 + W1["s2b"] + 16 + W1["s2c"] * 0.9, midy - 10), (AX + 1545, midy - 10), (AX + 1545, AY + okY + rxh / 2)], lab="side", pos=-0.85))
p3b.append(v("p3_ok", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", OK_T, d2x + D2W / 2 - OKW / 2, okY, OKW, okh))
p3b.append(e("p3_ok_e", "d2", "p3_ok", "否", (0.5, 1), (0.5, 0), vert=True))
s4_cx = AX + x + W2["s4"] / 2
s4x_x0 = s3bx_x + S3BXW + 30; s4x_x1 = s4x_x0 + S4XW0 + 20; s4x_x2 = s4x_x1 + S4XW1 + 20
assert s4x_x2 + S4XW2 + 20 <= rx_x, (s4x_x2 + S4XW2, rx_x)
p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
    _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
    p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
# 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
s0c_x = 30 + W1["s0a"] + 16 + W1["s0b"] + 16; s1_x = s0c_x + W1["s0c"] + 16
s0x_cx = s0c_x + W1["s0c"] * 0.4; s1x_cx = s1_x + W1["s1"] * 0.6
p3b.append(v("s0x", "p3L2", ELLIPSE(RED) + "fontSize=12;", S0X, s0x_cx - S0XW / 2, 50 + (row0h - s0xh) / 2, S0XW, s0xh))
p3b.append(v("s1x", "p3L2", ELLIPSE(RED) + "fontSize=12;", S1X, s1x_cx - S1XW / 2, 50 + (row0h - s1xh) / 2, S1XW, s1xh))
p3b.append(e("s0x_e", "s0c", "s0x", "失敗", (0.4, 0), (0.5, 1), vert=True, pos=-0.5))
p3b.append(e("s1x_e", "s1", "s1x", "≠ 1", (0.6, 0), (0.5, 1), vert=True, pos=-0.5))
# 第 4 列：單段 update（不經 ②③④）：查 registry 只在這裡與 ②b（add／upgrade 未指定 @<tag> 且非 CI 模式）
p3b.append(v("p3_u5_l", "p3L2", LBL, "單段動詞（install／upgrade vendor_kit／update／dev／help）不經 ②③④、一次 docker run；以 update 為例（流程見 update 頁）", 30, r4y, 900, 28))
_ux = 30; _upos = {}
for _id, _t, _st in (("u5a", U5A, L12), ("u5b", U5B, ENG12), ("u5c", U5C, ELLIPSE(GREEN) + "fontSize=12;"), ("u5d", U5D, ELLIPSE(ORANGE) + "fontSize=12;")):
    _h = hve(_t, U5W[_id]) if "ellipse" in _st else hv(_t, U5W[_id])
    p3b.append(v(_id, "p3L2", _st, _t, _ux, u5y + (u5h - _h) / 2, U5W[_id], _h)); _upos[_id] = (_ux, _h); _ux += U5W[_id] + 20
p3b.append(e("u5b_e", "u5a", "u5b", "", (1, 0.5), (0, 0.5)))
p3b.append(e("u5c_e", "u5b", "u5c", "0", (1, 0.5), (0, 0.5), vert="below"))
_by = AY + u5y + u5h + 12; _bx0 = AX + _upos["u5b"][0] + U5W["u5b"] * 0.8; _bx1 = AX + _upos["u5d"][0] + U5W["u5d"] / 2
p3b.append(ew("u5d_e", "u5b", "u5d", "1／2", (0.8, 1), (0.5, 1), [(_bx0, _by), (_bx1, _by)], lab="below", pos=0.0))
p3b += tmp
Y += l2h + 20
Y = footer(p3b, "p3b", Y, ["grpbox", "rhomb", "v3act_s", "v3ok", "v3err_s", "v3launch", "v3eng", "v2code", "ruleb", "tblh", "v2tag", "notep", "conv"], "實線 = 執行順序；線上文字 = 條件／接續編號\n淺灰底容器 = ②③ 的分組（標題 = 該段做的事）",
 ["inspect", "createcp", "tmpdist", "token", "vkresolve", "fingerprint", "gitkeepline"])   # 白名單／uid 旗標已由規則框 p3_sh／p3_uf 逐字承載（頁高 ≤ 2400）；第 0 頁已有的詞不列
pages_v1_a.append(("v1p3b", "契約 v2：啟動器 ↔ 引擎契約④", p3b))

# ================= P3bb v1p3bb：契約④（2）規則框（第十六輪自 p3b 拆頁）=================
p3bb = head("p3bb", "契約④ 啟動器 ↔ 引擎（2）── 規則框（§3、§5：白名單、執行環境、docker run、環境變數、image 取得、接手、uid、相容）", 1200)
P3BB_NOTE = "<b>本頁無待拍板</b>\n本頁 = 契約④ 的規則框（自「契約④」頁拆出，頁高 ≤ 2400）；流程、vk-resolve/1 文法、kind 表、apply 通則、兩段編排與快路徑在「契約④」頁"
p3bb.append(vb("p3bb_pend", "1", NP_NOTE, P3BB_NOTE, 1260, 12, 340, hv(P3BB_NOTE, 340, pad=10))); Y = max(12 + hv(P3BB_NOTE, 340, pad=10) + 16, 96)
tmp2 = []; y = 50
y = pair("p3_sh", WL_T, "p3_env", ENVR_T, y, out=tmp2, par="p3L2b")          # 配對依高度相近：白名單＋執行環境／docker run＋環境變數／image 取得＋自身升級／uid 旗標＋相容（全寬）
y = pair("p3_run", RUN_T, "p3_envw", ENV_T, y, out=tmp2, par="p3L2b")
y = pair("p3_img", IMG_T, "p3_self", SELF_T, y, out=tmp2, par="p3L2b")
y = rbox(tmp2, "p3_uf", "p3L2b", RULE, UF_T, 30, y, 1510, tagged=True)
y = rbox(tmp2, "p3_compat", "p3L2b", RULE, COMPAT_T, 30, y, 1510, tagged=True)
p3bb.append(v("p3L2b", "1", SW(NEUTRAL), "契約④ 啟動器 ↔ 引擎（2）── 規則框（§3、§5 逐條；每框一個主題）", 40, Y, 1560, y + 6))
p3bb += tmp2
Y += y + 6 + 20
Y = footer(p3bb, "p3bb", Y, ["grpbox", "ruleb", "v2tag", "notep"], "規則框 = interface_spec §3、§5 逐條；流程與圖例約定見「契約④」頁",
 ["token", "engine_changed", "rootless", "envwl", "timeout", "flock"])   # ≤ 8；只列本頁規則框用到且第 0 頁沒有的詞（救援路徑第 0 頁已有）
pages_v1_a.append(("v1p3bb", "契約 v2：啟動器 ↔ 引擎契約④（2）規則", p3bb))

# ================= P3c v1p3c：契約⑤ CI 與驗收矩陣 =================
p3c = head("p3c", "契約⑤ CI（interface_spec §7；下游 check.sh；下游 repo check.sh --dist；自身分層 + 驗收分組索引；逐條矩陣見 p3d）", 1200)
c, Y = nopend("p3c", 1260, 12, 340, "check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 分組索引在本頁、35 條詳表在 p3d")
# ================= P3c v1p3c：契約⑤ CI 與驗收矩陣 =================
p3c = head("p3c", "契約⑤ CI（interface_spec §7；下游 check.sh；下游 repo check.sh --dist；自身分層 + 驗收分組索引；逐條矩陣見 p3d）", 1200)
c, Y = nopend("p3c", 1260, 12, 340, "check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 分組索引在本頁、35 條詳表在 p3d")
p3c.append(c); Y = max(Y + 16, 96)
KH = 60
CK = [("k0", "⓪ version.local.toml 被 git track？", 190), ("k1", "① sync（CI 模式）", 120), ("k2", "② verify（印記 sha256，全部工具）", 170), ("k3", "③ upgrade --dry-run", 150),
      ("k4", "④ 工具測試 just <repo> check（若有；不得再呼叫 check.sh）", 250), ("k5", "⑤ 專案測試（just check 若有）", 170), ("k6", "全部通過 → 0", 130)]
K0F = "命中 → 1 拒絕\n（請勿把本機覆寫提交）"
K1F = "1：薄殼不符（6-1）、未完成接入（6-13）、基準版落後（6-5）、任何本機覆寫"
K1G = "3：介面版／檔案版不合\n（6-18／6-19；零寫入）"
K3F = "CI 模式且需改 進 git 的檔\n→ 1 印清單（version.toml 不動；與 -y 無關）"
K3G = "仍有衝突標記 → 2；印 6-6～6-8 但不紅燈"
K2F = "1：印記 sha256 不符\n（verify 失敗）"
K4F = "≠ 0 → 停：工具原碼傳出\n（1/2/3 語意不適用）"
K5F = "≠ 0 → 停：依專案\n（原碼傳出）"
KR = ("<b>check.sh（§7.1）</b>：第一行 shebang、第二行自描述、其後第一個動作 export CI=1；GitHub／GitLab 一樣、平台無關；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）")
RN = ("<b>Renovate preset（§7.3；下游自選，vendor_kit 不出 bot）</b>：放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；下游 extends: [\"github>ycpss91255-research/vendor_kit\"]；regex manager 匹配 **/.vendor_kit/version.toml（monorepo 子專案亦命中；key regex 與版本鎖定行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；"
 "PR 只改一行；major 分開 PR（matchUpdateTypes）；hostRules 依 host 不寫死 ghcr.io；prBodyNotes = 6-25（6-5 的指令 + 「推 commit 後不要勾 rebase/retry」）；不設 gitIgnoredAuthors、不改 rebaseWhen；postUpgradeTasks 不採")
RF = [("rn1", "Renovate PR 改 version.toml 一行", 170), ("rn2", "PR 的 CI 以新版跑 check.sh 完整流程（一行改動本身不構成通過依據）", 260), ("rn3", "需合併 → 1 印 6-5", 140),
      ("rn4", "維護者在 PR 分支本機 upgrade <repo> -y", 200), ("rn4b", "commit + push 到 PR 分支", 150), ("rn5", "CI 全部再跑（Renovate 不動有人推過的分支）", 220), ("rn6", "綠了才 merge", 110)]
DIST_C = ("<b>下游 repo 的 CI：check.sh --dist（§7.2）</b>：dist 佈局（files/、init.toml、just/<repo>.just 存在）、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗 [#29]）、"
 "以 just 1.33.0 解析每個 <ns>.just（並擋比 1.33 新的功能）、_sync lint（just --dump --dump-format json）、Dockerfile.dist 含 LABEL io.github.<org>.vendor_kit=1、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性")
CH = [("c_a", "env-test", 76, False), ("c_b", "test-base", 84, False), ("c_c1", "lint", 76, True), ("c_c2", "unit", 76, True), ("c_c3", "install", 96, True), ("c_c4", "merge", 84, True),
      ("c_e", "release-test（amd64、arm64 原生 runner）", 110, False), ("c_rc", "綠了才推候選 tag vN-rc.<n>（先 push-by-digest 再合成 index）", 118, False), ("c_f", "驗收：已釋出版驅動候選 + fixture 跑完整 §7.4 矩陣", 150, True),
      ("c_d1", "正式 GHCR image tag vN（imagetools create；digest 不變）", 140, True), ("c_d2", "Git tag vN", 80, True), ("c_d3", "發 Release vN\n（bootstrap.sh、tar、\n.digest、SHA256SUMS）", 122, True)]   # release 拆三格（Claude r13 c_d）
JM_T = ("just 矩陣 1.33.0 + latest（latest 非 required）；lint 擋比 1.33 新的功能與白名單外主機命令（ADR 記破壞性變更）；驗收用 dev vendor_kit -i <剛 build 的 tag> 同一機制；每版最低環境（docker 19.03、just 1.33.0）跑完整、其他環境（docker 上界、just latest、arm64、WSL2）按世代；"
 "驗收 §7.4 條 1–13 缺任一不得出貨（§8-12）；順序：release-test 綠了才 push-by-digest 合成 index 推候選 tag，驗收對候選 tag 做（fixture 第一行 = 候選 ref@index digest），全過才打正式 vN（digest 不變）；已釋出 image／Release 資產／fixture 永不刪；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」")
ACC = [
 ["1", "已釋出版驅動候選", "最低介面版以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1）→ upgrade vendor_kit（1 印 6-2）→ sync 0 → 工具 recipe → upgrade 全 → 再 upgrade vendor_kit 0；禁由候選樹複製 fixture、禁 stub 引擎"],
 ["2", "最低環境 × 世代", "每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境按世代覆蓋；成本上限當觸發討論條件"],
 ["3", "升級後 == 全新安裝", "升級後 .vendor_kit/ 進 git 的內容 == 用 C 全新 install + add（排除時間戳、digest、written_by）"],
 ["4", "連續升級", "r_i → r_j → C；固定最低介面版直接跳升 C"],
 ["5", "降版", "upgrade vendor_kit@<舊版>：同介面版／檔案版成功；跨檔案版改檔前拒絕 3 印 6-10、零寫入"],
 ["6", "< 最低介面版太舊", "唯一可用 synthetic fixture；任一動詞 → 3 印 6-18、零寫入；最低介面版檢查在任何上網之前（斷網也回 3）"],
 ["7", "舊 bootstrap.sh 再跑", "在已升級 repo 再跑：用 version.toml 指定引擎，不降版"],
 ["8", "舊引擎讀新檔", "dev vendor_kit -i 舊 image：寫入前拒絕 3 印 6-19；不重產 進 git 的薄殼"],
 ["9", "只改第一行後 CI=true sync", "模擬 Renovate、驗CI 模式真值規則 → 1 列薄殼不符、零 進 git 的檔寫入"],
 ["10", "fresh clone 無 gen/", "just vendor_kit 列出 vendor_kit 命名空間不觸網（工具命名空間 sync 後才出現，mod? 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行"],
 ["11", "下游使用者改薄殼／未納管檔／append", "不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn"],
 ["12", "中斷與重跑", "resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗"],
 ["13", "歷史 parser × 異常 TOML", "BOM、空白、重複 vendor_kit 行 → 1、schema 位置、本機覆寫、尾端註解"],
 ["14", "just 矩陣", "1.33.0 + latest（latest 非 required）"],
 ["15", "amd64 與 arm64 原生 runner", "各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致"],
 ["16", "離線包（Q26）", "無法連 GHCR 的機器用 bootstrap.sh --local <tar>（旁檔 .digest）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 local_image_id；旁檔缺 → 1；amd64／arm64 各一次"],
 ["17", "離線可用（Q22／Q26）", "本機已有 image 後斷網 → just <ns> build（自動 sync 快路徑）與 just vendor_kit sync 必須成功且不起 pull；斷網 + 無 image → 1 印 6-31 於 --timeout 5 內結束、不 hang"],
 ["18", "私有工具", "add <repo>@<tag> 可拉；add／update 無 token → 1 印 6-3；錯 token → 1；對 token → 列出；TOKEN_FILE 驗 -v 掛載；兩者同設 → 1；輸出、metadata、執行紀錄、進度檔皆 grep 不到 token；執行紀錄 registry_query 事件的 URL 已移除 userinfo（user:pass@）"],
 ["19", "append", "LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 .dockerignore 四行 append → uninstall 刪；故意改其中一行後 uninstall → 該行跳過並 warn、其餘原文相同的行仍刪"],
 ["20", "空白路徑", "專案根含空白與 $、dev -p \"含 空白/路徑\"；vk-resolve mount 八進位跳脫往返；just vendor_kit add --help 到引擎"],
 ["21", "worktree／submodule", "git worktree（.git 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）"],
 ["22", "rootless docker／Podman", "setup-docker-action rootless: true（不加 -u、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：--userns=keep-id）各跑完整流程；uid 12345 無 passwd 項"],
 ["23", "prune", "完整流程前後 docker network ls／volume ls 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊下游 image 刪、version.toml 引用的與本機覆寫 tag 保留；--dry-run 零刪除；未恢復的 .tmp.* 不刪"],
 ["24", "多工具彙總（Q27）", "兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1"],
 ["25", "F1 fixture（just 1.33.0）", "cache 缺檔時 just vendor_kit sync 可進入（mod?）；just <ns> build 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 _sync 的模組"],
 ["26", "無 tty／EOF", "CI 無 -y 需詢問 → 1 印 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑"],
 ["27", "Renovate 實際 repo", "人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中"],
 ["28", "驗收動詞集合", "由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅"],
 ["29", "執行紀錄（v2.12）", "每個情境結束後 log/<verb>/ 每檔逐行 json.loads；首筆 launcher_start、末筆 launcher_exit；同檔 trace_id 單一且 = 進度檔 <id>；event_name 全在註冊表；6-xx 同句進 body；sync 快路徑亦有檔；自身升級兩個引擎寫同一檔"],
 ["30", "啟動器 argv 跳脫（bats）", "餵 \"、\\、換行、[、]、非 ASCII、-n foo、空字串、\\ 結尾 → launcher_start 的 argv 經 json.loads 還原後逐項相等；dash 與 busybox 各跑一次"],
 ["31", "config.toml", "keep／days 為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30（缺鍵／缺檔外印警告）；51 檔或 31 天前的檔 → 結束後被 prune，本次的檔與 .gitignore 不刪；改過的 → upgrade vendor_kit 三方合併"],
 ["32", "磁碟不可寫 6-38", "log/ 唯讀或磁碟滿：每個動詞（含 help、prune、sync 快路徑、--dry-run）→ 1 + 6-38、零寫入、不起容器；只給引擎唯讀 → append 失敗 1 + 6-38、resolve 未執行"],
 ["33", "bootstrap.sh 逐 -t 中止", "三個 -t，第二個故意失敗（不存在的 repo）→ 第一個 add 完成且保留、第三個未執行、整體 1 並列出已完成／未處理"],
 ["34", "E(c) 分支", "upgrade vendor_kit@<tag>（≠ 現 ref、同介面版／檔案版）→ 不查 registry、建 .tmp.upgrade.<id>.toml、改第一行、接手重產、刪進度檔 → 1 + 6-2；CI=true 且薄殼相符 → 0；中途殺掉新引擎 → 進度檔留存，sync 6-33 結束 1、help 6-33 結束 0、重跑恢復"],
 ["35", "help 遇未完成交易", "留一個 .tmp.remove.<id>.toml → help 印 6-33 結束 0；sync／update 印 6-33 結束 1；三者除執行紀錄外不寫任何檔"],
]
tmp = []; y = 50
tmp.append(v("p3_k0", "p3L5", TEXT(12) + "align=left;fontStyle=1;", "專案 CI：只呼叫 .vendor_kit/ci/check.sh，一關過才下一關（每格一步）", 20, y, 200, KH))
x = 240; prev = None; kx = {}
for pid, t, w in CK:
    st = ELLIPSE(GREEN) + "fontSize=12;" if pid == "k6" else L12
    kx[pid] = (x, w)
    tmp.append(v(pid, "p3L5", st, t, x, y, w, KH))
    if prev: tmp.append(e(f"{pid}_e", prev, pid, "", (1, 0.5), (0, 0.5)))
    prev = pid; x += w + 16
# 分支橢圓（橙 = 需人處理、紅 = 失敗）：第一列 ⓪②④⑤ 各自正下方、第二列 ①③（需改檔／衝突）；每關都有失敗出口（§7.1）
fy0 = y + KH + 40
K0W, K1W, K1GW, K2W, K3W, K3GW, K4W, K5W = 200, 300, 280, 190, 280, 260, 260, 180
k0h = hve(K0F, K0W); k1h = hve(K1F, K1W); k1gh = hve(K1G, K1GW); k2h = hve(K2F, K2W); k3h = hve(K3F, K3W); k3gh = hve(K3G, K3GW); k4h = hve(K4F, K4W); k5h = hve(K5F, K5W)
rowA = max(k0h, k2h, k4h, k5h); fy1 = fy0 + rowA + 20
k0x = kx["k0"][0] + kx["k0"][1] / 2 - K0W / 2
k2x = kx["k2"][0] + kx["k2"][1] / 2 - K2W / 2
k4x = kx["k4"][0] + kx["k4"][1] / 2 - K4W / 2
k5x = kx["k5"][0] + kx["k5"][1] / 2 - K5W / 2 + 30
k1x = kx["k1"][0] + kx["k1"][1] / 2 - K1W / 2 + 20
k3x = kx["k3"][0] + kx["k3"][1] / 2 - K3W / 2
tmp.append(v("k0f", "p3L5", ELLIPSE(ORANGE) + "fontSize=12;", K0F, k0x, fy0, K0W, k0h))
tmp.append(e("k0f_e", "k0", "k0f", "命中", (0.5, 1), (0.5, 0), vert=True))
tmp.append(v("k2f", "p3L5", ELLIPSE(RED) + "fontSize=12;", K2F, k2x, fy0, K2W, k2h))
tmp.append(e("k2f_e", "k2", "k2f", "不符", (0.5, 1), (0.5, 0), vert=True))
tmp.append(v("k4f", "p3L5", ELLIPSE(RED) + "fontSize=12;", K4F, k4x, fy0, K4W, k4h))
tmp.append(e("k4f_e", "k4", "k4f", "失敗", (0.5, 1), (0.5, 0), vert=True))
tmp.append(v("k5f", "p3L5", ELLIPSE(RED) + "fontSize=12;", K5F, k5x, fy0, K5W, k5h))
tmp.append(e("k5f_e", "k5", "k5f", "失敗", (0.5, 1), (round((kx["k5"][0] + kx["k5"][1] / 2 - k5x) / K5W, 4), 0), vert=True))
tmp.append(v("k1f", "p3L5", ELLIPSE(ORANGE) + "fontSize=12;", K1F, k1x, fy1, K1W, k1h))
tmp.append(e("k1f_e", "k1", "k1f", "升為失敗", (0.5, 1), (round((kx["k1"][0] + kx["k1"][1] / 2 - k1x) / K1W, 4), 0), vert=True))
k1gx = k1x - 20 - K1GW
tmp.append(v("k1g", "p3L5", ELLIPSE(ORANGE) + "fontSize=12;", K1G, k1gx, fy1, K1GW, k1gh))   # 結束 3 拆成獨立橙終點（codex v1p3c #4）
_hy = Y + fy0 + rowA + 10
tmp.append(ew("k1g_e", "k1", "k1g", "3", (0.2, 1), (0.5, 0), [(40 + kx["k1"][0] + kx["k1"][1] * 0.2, _hy), (40 + k1gx + K1GW / 2, _hy)], lab="side", pos=-0.9))
tmp.append(v("k3f", "p3L5", ELLIPSE(ORANGE) + "fontSize=12;", K3F, k3x, fy1, K3W, k3h))
tmp.append(e("k3f_e", "k3", "k3f", "需改檔", (0.5, 1), (0.5, 0), vert="left"))
tmp.append(v("k3g", "p3L5", ELLIPSE(ORANGE) + "fontSize=12;", K3G, k3x + K3W + 20, fy1, K3GW, k3gh))
# 「衝突」線：從 ③ 右下角出、直下到第一列與第二列之間的縫隙、橫走到 k3g 正上方再下去；標籤貼在 ③ 出口旁的垂直段（不落在 ④ 下方；r11）
k3_ex = 40 + kx["k3"][0] + kx["k3"][1] * 0.9
k3g_cx = 40 + k3x + K3W + 20 + K3GW / 2
hy_ = Y + fy0 + rowA + 10
tmp.append(ew("k3g_e", "k3", "k3g", "衝突", (0.9, 1), (0.5, 0), [(k3_ex, hy_), (k3g_cx, hy_)], lab="side", pos=-0.9))
y = fy1 + max(k1h, k1gh, k3h, k3gh) + 24
y = rbox(tmp, "p3_kr", "p3L5", RULE, KR, 20, y, 1520, tagged=True)
# Renovate 鏈
tmp.append(v("p3_rn_l", "p3L5", LBL, "Renovate 路徑（PR 需合併時；補合併在 PR 分支完成、CI 綠後才 merge）", 20, y, 1000, 28)); y += 32
RH = 64; x = 20; prev = None
for pid, t, w in RF:
    st = ELLIPSE(GREEN) + "fontSize=12;" if pid == "rn6" else (ELLIPSE(ORANGE) + "fontSize=12;" if pid == "rn3" else L12)
    tmp.append(v(pid, "p3L5", st, t, x, y, w, RH))
    if prev: tmp.append(e(f"{pid}_e", prev, pid, "", (1, 0.5), (0, 0.5)))
    prev = pid; x += w + 16
y += RH + 16
rh2 = max(hvt(RN, 1000, True), hvt(DIST_C, 500, True))
tmp += vt("p3_c2", "p3L5", RULE, RN, 20, y, 1000, rh2, tagged=True)
tmp += vt("p3_c3", "p3L5", RULE, DIST_C, 1040, y, 500, rh2, tagged=True)
y += rh2 + 24
CH_H = 100
tmp.append(v("p3_c0", "p3L5", TEXT(12) + "align=left;fontStyle=1;", "vendor_kit 自身 CI（分層，一關過才下一關；每格一個檢查）", 20, y, 150, CH_H))
x = 180; prev = None
for pid, t, w, tg in CH:
    tmp.extend(vt(pid, "p3L5", L12, t, x, y, w, CH_H, tagged=tg))
    if prev: tmp.append(e(f"{pid}_e", prev, pid, "", (1, 0.5), (0, 0.5)))
    prev = pid; x += w + 11
assert x - 11 <= 1540, x
y += CH_H + 16
y = rbox(tmp, "p3_jm", "p3L5", RULE, JM_T, 20, y, 1520, tagged=True)
tmp.append(v("p3_acc_l", "p3L5", LBL, "驗收矩陣分組索引（§7.4；35 條逐條詳表見 p3d；一列一組）", 20, y, 900, 28)); y += 32
ACC_IDX = [
 ["相容承諾", "1–8", "已釋出版驅動候選；最低環境 × 世代；升級後 == 全新安裝；連續升級；降版；< 最低介面版；舊 bootstrap.sh 再跑；舊引擎讀新檔"],
 ["CI 模式與 Renovate", "9、27", "只改第一行後 CI=true sync；Renovate 實際 repo"],
 ["檔案與路徑", "10、11、13、19、20、21", "fresh clone 無 gen/；下游使用者改薄殼／未納管檔／append；異常 TOML；append 換行；空白路徑；worktree／submodule"],
 ["中斷與環境", "12、14、15、22", "中斷與重跑；just 矩陣；amd64／arm64 原生 runner；rootless docker／Podman"],
 ["離線", "16、17", "離線包；離線可用（斷網 sync／build）"],
 ["私有 registry", "18", "token／TOKEN_FILE；敏感值不入輸出、metadata、執行紀錄、進度檔"],
 ["prune／多工具／F1／tty", "23、24、25、26", "prune 差集；多工具彙總；F1 fixture；無 tty／EOF"],
 ["動詞集合與執行紀錄", "28、29、30、31、32", "驗收動詞集合；執行紀錄逐行 json.loads；argv 跳脫；config.toml 異常值；磁碟不可寫 6-38"],
 ["流程特例", "33、34、35", "bootstrap.sh 逐 -t 中止；E(c) 分支；help 遇未完成交易"],
]
y = tbl(tmp, "p3_acc", "p3L5", 20, y, [("群組", 200), ("條號", 170), ("涵蓋情境", 1150)], ACC_IDX, marks={(r, 0) for r in range(len(ACC_IDX))}) + 20
p3c.append(v("p3L5", "1", SW(NEUTRAL), "契約⑤ CI（下游 check.sh 六步 + Renovate；下游 repo check.sh --dist；vendor_kit 自身分層 + 驗收分組索引）", 40, Y, 1560, y))
p3c += tmp
Y += y + 20
Y = footer(p3c, "p3c", Y, ["v3act_s", "v3ok", "v3err_s", "v3step", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "實線 = 執行順序；線上文字 = 條件\n分組索引：一列一組",
 ["envtest", "offline", "ci", "renovatebot", "reltest", "fixture", "rootless", "candtag"])   # check.sh 六步／Renovate preset／check.sh --dist／lint／Q27 由圖、規則框 p3_kr／p3_c2／p3_c3／p3_jm 逐字承載；第 0 頁已有的詞不列
pages_v1_a.append(("v1p3c", "契約 v2：CI 契約⑤ 與驗收矩陣", p3c))

# ================= P3d v1p3d：契約⑤ 驗收矩陣詳表 =================
p3d = head("p3d", "契約⑤ 驗收矩陣詳表（interface_spec §7.4；35 條，一列一情境；分組索引與 CI 流程見 p3c）", 1200)
c, Y = nopend("p3d", 1260, 12, 340, "本頁只有 §7.4 逐條矩陣；缺任一不得出貨（§8-12）；已釋出 image／Release 資產／fixture 永不刪")
p3d.append(c); Y = max(Y + 16, 96)
tmp = []; y = 50
half = 18
ACC_COLS = [("#", 40), ("情境", 150), ("驗什麼", 560)]
yl = tbl(tmp, "p3d_acc", "p3L6", 20, y, ACC_COLS, ACC[:half], marks={(r, 1) for r in range(half)}, bold0=False)
yr = tbl(tmp, "p3d_accb", "p3L6", 790, y, ACC_COLS, ACC[half:], marks={(r, 1) for r in range(len(ACC) - half)}, bold0=False)
y = max(yl, yr) + 20
p3d.append(v("p3L6", "1", SW(NEUTRAL), "驗收矩陣（§7.4；左右兩表接續；每列一個情境）", 40, Y, 1560, y))
p3d += tmp
Y += y + 20
Y = footer(p3d, "p3d", Y, ["tblh", "grpbox", "v2tag", "notep"], "驗收表：一列一個情境\n分組索引見 p3c",
 ["fixture", "envtest", "reltest", "rootless", "offline", "worktree", "lint"])
pages_v1_a.append(("v1p3d", "契約 v2：驗收矩陣詳表", p3d))

# ================= P4 v1p4：架構圖 v2 ── 主機、啟動器、引擎 8 模組、registry =================
p4 = head("p4", "架構圖 v2 ── 主機載入鏈、啟動器、引擎 8 模組、registry（只畫模組、最小單元、模組間傳的資料）", 940)
p4[1] = v("p4_num", "1", TEXT(12) + "align=left;", NUM_T, 40, 56, 940, 44)                                   # 右上便條（x ≥ 1000）不壓契約編號列（Claude r13 p4_num）
NP_T = ("<b>本頁無待拍板</b>：只畫模組、最小單元、模組間傳的資料（箭頭只標傳什麼、不標動作也不是執行順序；雙箭頭 = 讀寫都有）；順序與判斷見流程頁。"
        "啟動器在主機跑、不算引擎模組（左上紅框）；引擎 8 模組見 00 頁；log 模組只記事件，其他模組經 log_event() 呼叫（不逐條畫線）。"
        "專案根 -v <專案根>:/repo -w /repo 掛進引擎（可寫），引擎只寫箭頭指到的路徑；工具檔從 .tmp.dist.<id>/ 唯讀掛 /dist（下有 <repo>/）、本機覆寫 <dir>/dist → /dist/<repo>")
p4.append(vb("p4_np", "1", NOTE, NP_T, 1000, 12, 600, hv(NP_T, 600, pad=10)))
GY = max(12 + hv(NP_T, 600, pad=10) + 78, 140)                                                             # 便條下留 78：啟動器 grep 四檔的線走 GY-10／-24／-38／-52 的走廊（最上線的標籤仍在便條之下）
def pos_at(pts, i, x=None, y=None):
    """折線 pts 上第 i 段（pts[i]→pts[i+1]）某點（給 x 或 y）的相對位置（-1 起點 … 1 終點），供線上標籤定位。"""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(segs); d = sum(segs[:i]); a, b = pts[i], pts[i + 1]
    d += abs((x if x is not None else a[0]) - a[0]) + abs((y if y is not None else a[1]) - a[1])
    return round(2 * d / total - 1, 4)
# ---- 啟動器（左上，主機上方）與 GHCR（右上）----
GE_T = ("<b>引擎 image ghcr.io/<org>/vendor_kit:vN（公開）</b>：多架構 amd64 + arm64；LABEL …vendor_kit=1、.protocol、.schema；一個專案用版本鎖定行那一版；"
        "引擎的本機覆寫（version.local.toml）時啟動器 inspect 驗 image ID 後直接用本機 image、不 pull；也出 docker save tar + .digest（#27）；已釋出永不刪")
GD_T = ("<b>下游 image ghcr.io/<org>/<repo>-dist:<tag></b>：多架構 amd64 + arm64；純資料 FROM scratch 只有 /dist；LABEL …vendor_kit=1；版本鎖定行與印記記 index digest；"
        "resolve 模組只查 tag／index digest（add／update／upgrade 且未指定 @<tag>），sync 不查最新版、只拉鎖定版")
GX, GW = 680, 920; GIW = GW - 60                                                                     # 右側留 40px：resolve → 下游 image 的查詢線走這裡
geh = hvt(GE_T, GIW, True); gdh = hvt(GD_T, GIW, True)
GH = 50 + geh + 8 + gdh + 20
HX, HW4 = 40, 570
H4 = ("<b>啟動器</b>（主機側薄殼：vendor.just 內的 POSIX sh 本體 + log.sh；在主機跑；非引擎模組；主機需 docker ≥ 19.03、sh、just ≥ 1.33.0）\n"
      "下列為責任單元（只 grep、不解析 TOML）；命令步驟與執行紀錄的建檔／結束事件見流程頁與 p3b 契約④")
H4U = ["grep 引擎 ref（版本鎖定行）", "grep 本機覆寫行（優先）", "grep 進度檔目標 ref（E(c)）", "grep config.toml keep／days", "trace_id", "launcher_start", "log_event()（log.sh）", "取得引擎／下游 image", "展開 /dist 到暫存", "起引擎容器", "vk-resolve 驗文法",
       "介面版旗標 --protocol", "清理（trap）", "pull 逾時（--timeout）", "資源 label", "log_prune（keep／days）", "launcher_exit"]
h4th = hvt(H4, HW4, True, pad=8)
h4h = max(h4th + units_h(H4U, HW4 - 12) + 6, 50 + geh + 8 + math.ceil(gdh * 0.35) + 24)   # 底邊至少留在 pull_dist 進線之下
p4 += vt("h4", "1", HOST + "align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;", H4, HX, GY, HW4, h4h, tagged=True)
p4 += units("h4", "1", HX + 6, GY + h4th - 2, HW4 - 12, H4U)
p4.append(v("p4G", "1", SW(PURPLE).replace("strokeColor=#000000", "strokeColor=#9673a6"), "GHCR（ghcr.io）── 兩種 image 都多架構；拉取都由啟動器執行，引擎容器內不呼叫 docker", GX, GY, GW, GH))
p4 += vt("g_eng", "p4G", PT12, GE_T, 20, 50, GIW, geh, tagged=True)
p4 += vt("g_dist", "p4G", PT12, GD_T, 20, 50 + geh + 8, GIW, gdh, tagged=True)
ge_mid = GY + 50 + geh / 2; gd_top = GY + 50 + geh + 8
p4.append(e("pull_eng", "g_eng", "h4", "引擎 image", (0, 0.5), (1, round((ge_mid - GY) / h4h, 4))))
p4.append(e("pull_dist", "g_dist", "h4", "下游 image\n（/dist 層）", (0, 0.35), (1, round((gd_top + gdh * 0.35 - GY) / h4h, 4))))
HB = GY + h4h; GB = GY + GH
LY = max(HB, GB) + 44
# ---- 引擎模組（先算高度）----
EX, EW = 600, 560
MX, MW = 290, 250
MOD = refill(L12, RED) + "align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;"
mods = [
 ("m_res", "<b>resolve</b>：版本解析", ["讀版本鎖定行", "本機覆寫優先", "查最新正式版（token -e）", "輸入指紋", "pull／extract 清單", "vk-resolve 輸出"], True),
 ("m_schema", "<b>schema</b>：設定與格式", ["讀寫 VK TOML", "檔案版檢查（6-19）", "未知欄位保留", "版本鎖定行寫入", "config.toml（TOML parser）"], True),
 ("m_prog", "<b>progress</b>：進度與寫入", ["建／恢復／刪進度檔", "flock（6-26）", "重驗指紋（6-12）", "暫存檔 → 原子替換", "清除清單（第一次 install）"], True),
 ("m_fetch", "<b>fetch</b>：取件 /dist → cache/<repo>/", ["展開 /dist", "路徑驗證", "逐檔驗 hash", "寫印記 gen/<repo>.stamp", "cache 整批替換"], True),
 ("m_init", "<b>initfile</b>：初始檔合併", ["建初始檔／append", "新檔詢問", "五態狀態機", "git merge-file --diff3", "基準版推進", "metadata（含 [progress]）"], True),
 ("m_shell", "<b>shell</b>：薄殼產生", ["薄殼五檔", "自描述首行", "比對薄殼是否被改（6-28）", "gen/.stamp", "gen/tools.just（mod?）", "根 justfile 一行", "根 .dockerignore 四行", "baseline/.gitkeep"], True),
 ("m_prune", "<b>prune</b>：清理", ["keep 清單", "docker label 規則", "清殘留 .tmp.dist.<id>/", "清殘留 .tmp.<verb>.*"], True),
]
def title_h(t, w): return max(30, hvt(t, w, True, pad=6))          # 模組標題列高（兩行時單元下移）
def mod_h(labels, w, title=""): return title_h(title, w) + units_h(labels, w - 12) + 8
PX, PW = 1290, 310
FX, FW = 15, 275
def grp_h(items, title="", cols=1): return grp_title_h(title, FW, True) + 6 + math.ceil(len(items) / cols) * 28 + 4
def filegrp2(prefix, parent, style, title, items, x, y, w, tagged=True, cols=2):
    """檔案分組多欄版（短檔名省高度；cols = 2 或 3）。"""
    th = grp_title_h(title, w, tagged); ih = 24; rows = math.ceil(len(items) / cols)
    h = th + 6 + rows * (ih + 4) + 4; iw = (w - 30 - 8 * (cols - 1)) / cols
    cells = vt(prefix, parent, style, title, x, y, w, h, tagged=tagged)
    for i, it in enumerate(items):
        cells.append(v(f"{prefix}_f{i}", prefix, style.replace("fontStyle=1;", ""), it, 10 + (i % cols) * (iw + 8), th + 6 + (i // cols) * (ih + 4), iw, ih))
    return cells, h
FILES = {
 "m_schema": [("f_ver", "file", F_GIT, "version.toml（進 git；版本鎖定行）", 36), ("f_vl", "file", F_NOGIT, "version.local.toml（本機覆寫）", 36), ("f_cfg", "file", F_GIT, "config.toml（進 git）", 36)],
 "m_prog": [("f_tmp", "file", F_NOGIT, ".tmp.<verb>.<id>.toml（進度檔）", 36)],
 "m_fetch": [("f_repo", "grp2", F_NOGIT_T, "cache/<repo>/（不進 git，不可改）", ["files/…", "init.toml", "just/<ns>.just"]), ("f_stamp", "file", F_NOGIT, "gen/<repo>.stamp（印記）", 32)],
 "m_init": [("f_user", "grp", F_USER_T, "初始檔（專案檔，進 git；永不刪、永不覆蓋）", ["Dockerfile 等（copy）", "根 .gitignore 幾行（append）"]), ("f_bl", "grp", F_GIT_T, "baseline/<repo>/（進 git）", ["基準版（上次套用的初始檔原版副本）", "metadata（含 [progress]）"])],
 "m_shell": [("f_just", "file", F_USER, "根 justfile（專案檔）：import 一行", 36), ("f_di", "file", F_USER, "根 .dockerignore（專案檔）：四行", 36),
          ("f_shell", "grp2", F_GIT_T, "薄殼（進 git；首行自描述）", ["entry.just", "vendor.just", "log.sh", ".gitignore", "ci/check.sh"]), ("f_gen", "grp2", F_NOGIT_T, "gen/（不進 git；tools.just = mod? 行、.stamp = 引擎 ref）", ["tools.just", ".stamp"]), ("f_gk", "file", F_GIT, "baseline/.gitkeep（VK 自產的進 git 空檔）", 40)],
 "m_prune": [("f_tmpd", "file", F_NOGIT, "殘留 .tmp.dist.<id>/、.tmp.<verb>.*", 36)],
}
F_LOG_T = "log/（不進 git；自帶 .gitignore；執行紀錄）"; F_LOG_I = ["<verb>/<UTC ts>-<id8>.jsonl", ".gitignore（*／!.gitignore）"]
def files_h(lst): return sum((grp_h(it, t) if k == "grp" else grp_h(it, t, 2) if k == "grp2" else grp_h(it, t, 3) if k == "grp3" else it) for _, k, _, t, it in lst) + 8 * (len(lst) - 1)
R = {}; ey = 40; MGAP = 8
for pid, t, us, tg in mods:
    mh = mod_h(us, MW, t); fh = files_h(FILES.get(pid, []))
    h = max(mh, fh); R[pid] = (ey, h); ey += h + MGAP
log_row_y = ey; log_row_h = grp_h(F_LOG_I, F_LOG_T); R["f_log"] = (log_row_y, log_row_h); ey += log_row_h + MGAP   # 執行紀錄列（log 模組在左側直欄，線走模組列下方）
eng_end = ey
pf = []; p4_files = []; P = {}
y = log_row_y
cells, h = filegrp("f_log", "p4P", F_NOGIT_T, F_LOG_T, F_LOG_I, FX, y, FW, tagged=True); p4_files += cells; pf.append(("f_log", y, h)); P["f_log"] = y
for pid_mod, lst in FILES.items():
    y = R[pid_mod][0]
    for fid, kind, st, title, it in lst:
        if kind == "grp":
            cells, h = filegrp(fid, "p4P", st, title, it, FX, y, FW, tagged=True)
        elif kind in ("grp2", "grp3"):
            cells, h = filegrp2(fid, "p4P", st, title, it, FX, y, FW, tagged=True, cols=int(kind[-1]))
        else:
            h = it; cells = vt(fid, "p4P", st, title, FX, y, FW, h, tagged=True)
        p4_files += cells; pf.append((fid, y, h)); P[fid] = y; y += h + 8
proj_end = ey
# ---- 主機（just 載入鏈與目錄；啟動器另在右上）----
HXo, HW = 70, 460                                                                                  # 主機分組右移 30：左緣 x=50 留給 config.toml → 啟動器的線（與 x=20 的 log 線相距 30）
C1X, C1W, C2X, C2W = 20, 212, 252, 188
H0 = "下游使用者\n打 just vendor_kit <動詞> …\n或 just <ns> …"
H1 = "根 justfile（專案檔，進 git）\nimport '.vendor_kit/entry.just'"
H2 = ".vendor_kit/entry.just\n（進 git）mod vendor_kit 'vendor.just'\nimport? 'gen/tools.just'"
H3 = ".vendor_kit/vendor.just\n（進 git）動詞 recipe 一行轉發\n+ 啟動器本體（POSIX sh）"
H3L = ".vendor_kit/log.sh\n（進 git；獨立檔）啟動器 log 函式；\nvendor.just source 它"
G1 = ".vendor_kit/gen/\ntools.just（不進 git）一行一命名空間\nmod? <ns> '../cache/<repo>/\njust/<ns>.just'"
G2 = "工具命名空間 just <ns> …\n= cache/<repo>/\njust/<ns>.just 裡的 recipe；\n_sync 前置回叫 just vendor_kit sync"
TMP = "暫存 .vendor_kit/\n.tmp.dist.<id>/（專案內）\n下游 image 的 /dist 展開副本 + vk-resolve\n（啟動器 mktemp、trap 清）"
hh = {"h0": hve(H0, C1W), "h1": hv(H1, C1W), "h2": max(hv(H2, C1W), hvt(G1, C2W, True)), "h3": max(hv(H3, C1W, pad=8), hvt(G2, C2W, True)), "h3l": hv(H3L, C1W, pad=8)}
hy = {}; y0 = 40
for k in ("h0", "h1", "h2", "h3", "h3l"):
    hy[k] = y0; y0 += hh[k] + 30
VK_T = (".vendor_kit/             # 契約② p2，根目錄只多這個\n"
 "├─ version.toml         # 進 git：版本鎖定行\n"
 "├─ version.local.toml   # 不進 git：本機覆寫\n"
 "├─ config.toml          # 進 git：[log] keep／days\n"
 "├─ .gitignore           # 進 git：我們自己的\n"
 "├─ entry.just           # 進 git：mod + import?\n"
 "├─ vendor.just          # 進 git：動詞 + 啟動器\n"
 "├─ log.sh               # 進 git：啟動器 log 函式\n"
 "├─ ci/check.sh          # 進 git：CI 六步（⓪–⑤）\n"
 "├─ baseline/            # 進 git：基準版 + metadata\n"
 "├─ gen/                 # 不進 git：tools.just、.stamp、\n"
 "│                       #   <repo>.stamp（印記）\n"
 "├─ log/<verb>/          # 不進 git：<ts>-<id8>.jsonl\n"
 "├─ .tmp.<verb>.<id>.toml  # 不進 git：進度檔\n"
 "├─ .tmp.dist.<id>/      # 不進 git：啟動器暫存\n"
 "└─ cache/<repo>/        # 不進 git：工具檔展開")
vkw = math.ceil(code_w(VK_T)) + 16; vkh = code_h(VK_T)
vky = y0
host_end = vky + vkh + 20
LH = max(eng_end, host_end, proj_end)
GRPB = lambda fill: refill(L12, fill) + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=6;fontStyle=1;fontSize=14;"
p4.append(v("p4H", "1", GRPB(NEUTRAL), "主機（下游使用者電腦／CI runner）── just 載入鏈與目錄（線 = 誰載入誰）", HXo, LY, HW, LH))
p4.append(v("h0", "p4H", ELLIPSE(YELLOW) + "fontSize=12;", H0, C1X, hy["h0"], C1W, hh["h0"]))
p4 += vt("h1", "p4H", F_USER, H1, C1X, hy["h1"], C1W, hh["h1"], tagged=True)
p4.append(v("h2", "p4H", F_GIT, H2, C1X, hy["h2"], C1W, hh["h2"]))
p4 += vt("h3", "p4H", F_GIT, H3, C1X, hy["h3"], C1W, hh["h3"], tagged=True)
p4 += vt("h3l", "p4H", F_GIT, H3L, C1X, hy["h3l"], C1W, hh["h3l"], tagged=True)
cells, _, _ = code("h_vk", "p4H", VK_T, C1X, vky, vkw); p4 += cells
tmph = hv(TMP, C2W, pad=8)
p4.append(v("tmp", "p4H", L12, TMP, C2X, hy["h0"], C2W, tmph))
p4 += vt("g1", "p4H", F_NOGIT, G1, C2X, hy["h2"], C2W, hh["h2"], tagged=True)
p4 += vt("g2", "p4H", L12, G2, C2X, hy["h3"], C2W, hh["h3"], tagged=True)
# 主機側載入鏈（codex v1p4 #3）：下游使用者 → 根 justfile → entry.just → vendor.just／tools.just → 工具 recipe；vendor.just source log.sh；工具 recipe 的 _sync 回叫 just vendor_kit sync
p4.append(e("l_h0", "h0", "h1", "", (0.5, 1), (0.5, 0)))                                            # 載入內容寫在格內（import／mod／mod?／source），線不另標（線太短）
p4.append(e("l_h1", "h1", "h2", "", (0.5, 1), (0.5, 0)))
p4.append(e("l_h2", "h2", "h3", "", (0.5, 1), (0.5, 0)))
p4.append(e("l_h3l", "h3", "h3l", "", (0.5, 1), (0.5, 0)))
p4.append(e("l_g1", "h2", "g1", "", (1, 0.5), (0, 0.5)))
p4.append(e("l_g2", "g1", "g2", "", (0.5, 1), (0.5, 0)))
p4.append(e("l_g2s", "g2", "h3", "", (0, 0.5), (1, 0.5)))
# ---- 引擎容器 ----
p4.append(v("p4E", "1", SW(BLUE, 16).replace("strokeColor=#000000", "strokeColor=#6c8ebf"), "引擎容器 vendor_kit:vN（8 模組；一格一個最小單元）", EX, LY, EW, LH))   # 紫只留給 image（r11）
for pid, t, us, tg in mods:
    y, h = R[pid]
    p4 += vt(pid, "p4E", MOD, t, MX, y, MW, h, tagged=tg)
    p4 += units(pid, "p4E", MX + 6, y + title_h(t, MW), MW - 12, us)
LOG_Y, LOG_H = 40, eng_end - MGAP - 40
p4 += vt("m_log", "p4E", MOD, "<b>log</b>：紀錄", 20, LOG_Y, 110, LOG_H, tagged=True)
for i, s_ in enumerate(["log_event()（各模組同一入口）", "engine_* 事件", "config_read 事件", "事件註冊表（未註冊→FATAL）", "Python logging＋JSON", "append 同一檔", "憑證永不記"]):
    p4.append(v(f"m_log_u{i}", "p4E", UNIT, s_, 26, LOG_Y + 30 + i * 52, 98, 46))
def fy(yrel): return round((yrel - LOG_Y) / LOG_H, 4)
mid = lambda k: R[k][0] + R[k][1] / 2
# 模組間資料（相鄰模組直向；schema → log 橫向）
# 模組間資料：走模組欄左側 x=250 的短匯流（上格 0.7 出、下格 0.3 進；標籤放線左、不壓 log 模組）
def dmod(eid, up, dn, label, both=False):
    y1 = LY + R[up][0] + 0.7 * R[up][1]; y2 = LY + R[dn][0] + 0.3 * R[dn][1]; bx = EX + MX - 40
    p4.append(ew(eid, up, dn, label, (0, 0.7), (0, 0.3), [(bx, y1), (bx, y2)], both=both, lab="left", pos=0.0))
dmod("d_res_schema", "m_res", "m_schema", "版本鎖定行、\n本機覆寫", both=True)
dmod("d_schema_prog", "m_schema", "m_prog", "進度檔 TOML", both=True)
dmod("d_prog_fetch", "m_prog", "m_fetch", "暫存路徑、\n原子替換")
dmod("d_fetch_init", "m_fetch", "m_init", "新版初始檔 N\n（/dist）")
dmod("d_init_shell", "m_init", "m_shell", "tools.just\n重生請求")
dmod("d_shell_prune", "m_shell", "m_prune", "版本鎖定行\n→ keep")
p4.append(e("d_cfg_log", "m_schema", "m_log", "config_read\n（keep／days）", (0, 0.5), (1, fy(mid("m_schema"))), vert="below"))
# ---- 專案目錄（平面分組框，標題靠右上：左上留給啟動器兩條線進 config.toml／log/）----
p4.append(v("p4P", "1", GRPB(GREEN), "專案根（掛載為 /repo）", PX, LY, PW, LH))
p4 += p4_files
def fmid(pid):
    for q, y, h in pf:
        if q == pid: return y + h / 2
def rel(pid_mod, yabs): return (1, round((yabs - R[pid_mod][0]) / R[pid_mod][1], 4))
p4.append(e("w_ver", "m_schema", "f_ver", "版本鎖定行", rel("m_schema", fmid("f_ver")), (0, 0.5), both=True))
p4.append(e("w_vl", "m_schema", "f_vl", "本機覆寫行（path:／\ntag + image ID）", rel("m_schema", fmid("f_vl")), (0, 0.5), both=True))
p4.append(e("w_cfg", "f_cfg", "m_schema", "config.toml\n（TOML parser）", (0, 0.5), rel("m_schema", fmid("f_cfg"))))
p4.append(e("w_tmp", "m_prog", "f_tmp", "done／pending、consents", rel("m_prog", fmid("f_tmp")), (0, 0.5), both=True))
p4.append(e("w_repo", "m_fetch", "f_repo", "展開的工具檔\n（整批替換）", rel("m_fetch", fmid("f_repo")), (0, 0.5)))
p4.append(e("w_stamp", "m_fetch", "f_stamp", "index digest\n+ 每檔 sha256", rel("m_fetch", fmid("f_stamp")), (0, 0.5), both=True))
p4.append(e("w_user", "m_init", "f_user", "初始檔內容\n（現況／結果）", rel("m_init", fmid("f_user")), (0, 0.5), both=True))
p4.append(e("w_bl", "m_init", "f_bl", "基準版、metadata\n（含 [progress]）", rel("m_init", fmid("f_bl")), (0, 0.5), both=True))
p4.append(e("w_just", "m_shell", "f_just", "import 那一行", rel("m_shell", fmid("f_just")), (0, 0.5), both=True))
p4.append(e("w_di", "m_shell", "f_di", ".dockerignore\n四行", rel("m_shell", fmid("f_di")), (0, 0.5), both=True))
p4.append(e("w_shell", "m_shell", "f_shell", "薄殼五檔內容\n（首行／模板）", rel("m_shell", fmid("f_shell")), (0, 0.5), both=True))
p4.append(e("w_gen", "m_shell", "f_gen", "tools.just、\n.stamp 內容", rel("m_shell", fmid("f_gen")), (0, 0.5)))
p4.append(e("w_gk", "m_shell", "f_gk", "空檔", rel("m_shell", fmid("f_gk")), (0, 0.5)))
p4.append(e("w_tmpd", "m_prune", "f_tmpd", "殘留清單（刪）", rel("m_prune", fmid("f_tmpd")), (0, 0.5)))
# log 模組 → log/：從 log 模組底邊下到執行紀錄列中線（模組列下方、容器內無其他格），右穿容器進 log/ 左側
log_mid = LY + log_row_y + log_row_h - 8
pts = [(EX + 90, LY + LOG_Y + LOG_H), (EX + 90, log_mid), (PX, log_mid)]
p4.append(ew("w_log", "m_log", "f_log", "engine_* 事件（append 同一檔）", (0.5, 1), (0, round((log_row_h - 8) / log_row_h, 4)), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=EX + 400)))
CHAIN_N = "模組間箭頭只標傳什麼資料、不是固定執行順序：每個動詞只經過自己需要的模組（update 只 resolve＋schema；prune 只 resolve＋schema＋progress＋prune），順序見流程頁"   # codex r13 v1p4 #13
p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
# ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
# 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
MXX, RXX, TXX = 530, 552, 576
Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
pts = [(RXX, HB), (RXX, Y_R), (EX, Y_R)]
p4.append(ew("run_cli", "h4", "p4E", "動詞、參數、\n介面版旗標", (round((RXX - HX) / HW4, 4), 1), (0, round((Y_R - LY) / LH, 4)), pts[1:-1], lab="side", pos=pos_at(pts, 0, y=HB + 48)))
pts = [(EX, Y_T), (TXX, Y_T), (TXX, HB)]
p4.append(ew("ret_cli", "p4E", "h4", "結束碼、\nvk-resolve", (0, round((Y_T - LY) / LH, 4)), (round((TXX - HX) / HW4, 4), 1), pts[1:-1], lab="side", pos=pos_at(pts, 1, y=HB + 14)))
# registry 查詢由 resolve 模組發出：右出 → 上進下游 image 底邊（GHCR 在引擎正上方）
y_reg = LY + mid("m_res"); qx = 1215
y_reg2 = LY + R["m_res"][0] + R["m_res"][1] * 0.75; qx2 = 1245; qy2 = LY - 30; qx3 = GX + GW - 20
pts = [(EX + MX + MW, y_reg), (qx, y_reg), (qx, GY + GH - 20)]
p4.append(ew("q_reg", "m_res", "g_dist", "工具 tag／\nindex digest", (1, 0.5), (round((qx - (GX + 20)) / GIW, 4), 1), pts[1:-1], both=True, lab="side", pos=pos_at(pts, 1, y=y_reg - 60)))
pts = [(EX + MX + MW, y_reg2), (qx2, y_reg2), (qx2, qy2), (qx3, qy2), (qx3, GY + 50 + geh / 2), (GX + 20 + GIW, GY + 50 + geh / 2)]   # update／upgrade 也查引擎 image 的 tag（spec §1.2；r11）
p4.append(ew("q_reg_e", "m_res", "g_eng", "引擎 tag／index digest（update／upgrade）", (1, 0.75), (1, 0.5), pts[1:-1], both=True, lab="below", pos=pos_at(pts, 2, x=(qx2 + qx3) / 2)))
# 啟動器 → log/（launcher_* 事件；與引擎 append 同一檔）、config.toml → 啟動器（固定寫法的 keep 行 grep）：走頁面左緣與底緣，從專案框底邊進檔
log_x = PX + FX + FW * 0.65; cfg_x = PX + FX + 100
YB = LY + LH
LGX = HX + 20                                                                                        # 啟動器底邊左端（x=60）出 → 下到底緣 → 右到 log/ 底邊（主機分組在 x=70 起，線在其左）
pts = [(LGX, HB), (LGX, YB + 14), (log_x, YB + 14), (log_x, LY + P["f_log"] + next(h for q, y, h in pf if q == "f_log"))]
p4.append(ew("w_log_l", "h4", "f_log", "launcher_* 事件（launcher_start／launcher_exit 等；與引擎 append 同一檔；順序見 p3b）", (round((LGX - HX) / HW4, 4), 1), (0.65, 1), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=700)))   # 只標資料，順序歸流程頁（r11）
RXE = PX + PW + 8
for _fid, _bx, _dy, _hx, _lab, _lx in (("f_ver", RXE, 10, 0.42, "版本鎖定行（grep 引擎 ref）", 1300), ("f_vl", RXE + 12, 24, 0.34, "本機覆寫行（grep；優先）", 1000), ("f_cfg", RXE + 24, 38, 0.26, "固定寫法的 keep／days 行（grep）", 720), ("f_tmp", RXE + 36, 52, 0.18, "進度檔的目標引擎 ref（E(c) 接手時 grep）", 380)):   # 啟動器只讀（grep）四檔：檔越上面走越內側匯流排、越低的走廊、越右的入口 → 四線互不交叉（取代原底緣 w_cfg_l）
    _fy = LY + P[_fid] + 18; _cy = GY - _dy; _tx = HX + HW4 * _hx
    _pts = [(PX + FX + FW, _fy), (_bx, _fy), (_bx, _cy), (_tx, _cy), (_tx, GY)]
    p4.append(ew(f"g_{_fid}", _fid, "h4", _lab, (1, 0.5), (_hx, 0), _pts[1:-1], pos=pos_at(_pts, 2, x=_lx)))
Y = LY + LH + 56                                                                                       # 底緣兩條線（YB+14／YB+44）與其標籤在圖例之上（Claude r13 w_cfg_l）
c, Y = lgd("p4", 40, Y, ["v3img", "v4mod", "v4unit", "v4host", "v4hgrp", "v4egrp", "v4pgrp", "v2git", "v2no", "v2usr", "v2code", "v2tag", "v4other", "notep"], "實線 = 資料流（線上文字 = 傳什麼）\n雙箭頭 = 讀寫都有；黃橢圓 = 下游使用者", maxw=1300)
p4 += c
c, Y = terms2("p4", 40, Y + 34, [TERMS[k] for k in ["modunit", "configtoml", "traceid", "indexdigest", "tmp", "mount", "logevents", "flock"]])   # 8 模組、啟動器、執行紀錄等見第 0 頁
p4 += c
pages_v1_a.append(("v1p4", "架構圖 v2", p4))
# ================= P9：prune（1）resolve → 差集 → 刪 =================
LST1 = fl("建執行紀錄 log/<verb>/<ts>-<id8>.jsonl")                                                   # 啟動器起點後第一格（v2.16-19 拆兩格）
LST2 = fl("寫 launcher_start（完整原始 argv）")                                                        # 第二格：失敗 → 紅出口 LSX
LSX = "1 + 6-38：執行紀錄建不了／寫不進（零寫入）"
EXIT_C = ENTRY                                                                                        # 跨頁出口也用白虛線橢圓（v2.15-3）
COLS_PR = [("下游使用者", 40, 200), ("啟動器（主機 sh）", 260, 300), ("引擎容器", 580, 340), ("docker daemon", 940, 300), ("專案目錄", 1260, 330)]
DK = "docker daemon"
T_KEEP = ("keep 清單", "vk-resolve 的 keep|<name>|<ref> 記錄：version.toml 引擎 ref、[tools] 每個工具 ref、version.local.toml 覆寫的 vendor_kit <tag>；這些 image 不可刪")
T_DIFF = ("差集", "候選（依 label 列出的四類資源）扣掉 keep：image 只刪「帶 label 且本專案未引用」者；容器／network／volume 依 label 刪；vendor_kit 不建 network／volume，若意外建立也要能刪（驗收 §7.4-23）")
T_SHARED = ("共享 daemon", "一台 docker daemon 被多個專案共用：image 上沒有 .project label，其他專案是否引用同一 image 不可知 → 文件明寫、先 --dry-run 看；被刪的 image 下次 sync 會再拉（已釋出 image 永不刪）")
T_LOGNP = ("log/（不在 prune 範圍）", "log/<verb>/*.jsonl 舊檔（30 天且 ≤ 50 檔；config.toml 可調）由啟動器每次結束時自行清（log_prune），不屬 prune；prune 不碰 log/")
T_TMP = (".tmp.* 進度檔／.tmp.dist.<id>/", "前者 = 其他可寫動詞留下的進度檔：未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；prune 自己的交易也建 .tmp.prune.<id>.toml（清理前建、清理後刪；v2.9-6）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清")
T_DOCKERLS = ("docker ls／rm（主機命令白名單）", "啟動器只用白名單命令：docker {container,image,network,volume} ls --filter label=…、docker rm／image rm／network rm／volume rm；逐類資源一次一個命令；不把 docker socket 掛進引擎（引擎不碰 daemon）")
T_DRYP = ("--dry-run（prune）", "= apply prune --dry-run：不問、不刪 docker 資源，仍起第二個容器（apply）只列出會清的暫存（零刪除）；無短形")
T9 = [T_KEEP, T_LABEL, T_DIFF, T_SHARED, T_DRYP, T_TMP, T_MSG, T_DOCKERLS]   # ≤ 8 條；resolve／apply、log/ 第 0 頁已有
T9B = [T_KEEP, T_DIFF, T_RESOLVE, T_DRYP, T_TMP, T_FP, T_MSG]
N9 = "已定（v2.4-10、grilling 9、Q24、Q25、interface_spec A1、v2.7-7、v2.14-2、v2.15-2／-6／-8）：prune 第一版做；所有 vendor_kit 建的 docker 資源帶 label；prune 依 label 掃四類資源、刪 version.toml／local 未引用者；docker 指令由啟動器執行（不掛 socket）；image 只刪帶 label 且本專案未引用者（共享 daemon 提醒）；活躍的 .tmp.* 只列出不刪、不視為未完成交易；--dry-run = apply prune --dry-run（不跳過 apply、零刪除）；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run；執行紀錄事件依圖例約定①②。"
p9, F = newpage_c("流程 v2：prune（1）── resolve keep 清單 → 依 label 列資源 → 差集 → 刪（§1.2、§3.3）", N9, COLS_PR, gap=14)
b = F.band("bP", "prune [-y] [--dry-run] 第 1 段：執行紀錄 → resolve 算 keep（活躍進度檔只列出）→ resolve 0 且文法合 → 依 label 列四類資源 → 差集 → --dry-run 只列出／問後逐類刪（每個命令記成功／失敗）→ 續「prune（2）」頁", v2=True)
b.box("q0", U, 0, G12, "just vendor_kit prune（-y／--dry-run）", 200)
b.box("q0l", L, 0, v2(W12), LST1.replace("<verb>", "prune"), 300)
b.box("q0x", U, 1, v2(R12), LSX, 200)
b.box("q0l2", L, 1, v2(W12), LST2, 300)
b.box("q1", L, 2, W12, "docker run <引擎> resolve prune（永不 -t）", 300)
b.box("q2", E, 2, SUB, "resolve（不寫任何檔）：讀 version.toml、version.local.toml", 340)
b.box("q3", E, 3, SUB, "算保留清單 keep：引擎 ref、[tools] 每個工具 ref、本機覆寫的 vendor_kit <tag>", 340)
b.files("q3f", P, 3, "只讀（不寫）", ["version.toml（引擎 ref、[tools]）", "version.local.toml（vendor_kit = \"<tag>\"）"], 330)
b.box("q4", E, 4, v2(D12), "有活躍（未恢復）的進度檔 .tmp.<verb>.*？", 340, ax="l")
b.box("q4y", E, 5, v2(SUB), "是：只列出並印 6-33（prune 例外：不刪、不恢復、不視為未完成交易）", 340)
b.box("q4f", P, 5, F12, ".vendor_kit/.tmp.<verb>.<id>.toml（活躍交易：保留）", 330)
b.box("q5", E, 6, SUB, "stdout vk-resolve/1：keep|<name>|<ref>…、fingerprint、apply|yes、end|N", 340)
b.box("q5x", U, 7, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不動 docker", 200)
b.box("q5q", L, 7, v2(D12), "resolve 結束碼 0？", 300)
b.box("q6x", U, 8, R12, "否 → 1 + 6-30：不動 docker", 200)
b.box("q6", L, 8, D12, "是：收完整份、驗首尾與筆數：文法合？", 300)
b.box("q7", L, 9, W12, "是：docker container／image／network／volume ls --filter label=io.github.<org>.vendor_kit=1", 300)
b.box("q7d", DK, 9, NOTE, "結果：列出帶 label 的四類資源：容器、image、network、volume", 300)
b.box("q7n", P, 9, NOTE, "所有 vendor_kit 建的資源都帶 label（容器／network／volume 另加 .project=<專案根>）；不建 network／volume，若意外建立也要能刪（驗收 §7.4-23：故意留一個帶 label 的 network／volume，prune 後必須消失）", 330)
b.box("q8", L, 10, W12, "差集 = 候選 − keep（image：帶 label 且本專案未引用；容器／network／volume：帶 label 者）", 300)
b.box("q8n", DK, 10, NOTE, "共享 daemon 提醒：image 沒有 .project label，其他專案是否引用同一 image 不可知 → 只刪帶 label 且本專案未引用者；先 --dry-run 看；被刪的 image 下次 sync 會再拉", 300)
b.box("q9", L, 11, D12, "--dry-run？", 200)
b.box("q9y", U, 11, W12, "是：只印差集（會刪什麼），不問、不刪 docker 資源", 200)
b.box("q10tx", U, 12, O12, "否 → 1 + 6-4：需要確認但沒有終端；請加 -y", 200)
b.box("q10t", L, 12, D12, "否：有 tty 或 -y？", 260)
b.box("q10n", U, 13, G12, "否 → 0：不刪、印清單", 200)
b.box("q10", L, 13, D12, "是：問 6-32：要刪除以上資源嗎？（-y 免問）", 300)
b.box("q11l", L, 14, LBL, "是 ↓ 對四類資源逐類刪：每個命令記成功／失敗，失敗的續刪其餘（結果帶到（2）頁）", 300, 24, ax="l", minh=24)
b.box("q11a", L, 15, W12, "docker rm <差集內的容器>", 300)
b.box("q11ad", DK, 15, NOTE, "結果：容器被刪（每個 rm 的成功／失敗記下）", 300)
b.box("q11b", L, 16, W12, "docker image rm <差集內的 image>", 300)
b.box("q11bd", DK, 16, NOTE, "結果：image 被刪（keep 內的 image 保留；成功／失敗記下）", 300)
b.box("q11c", L, 17, W12, "docker network rm <差集內的 network>", 300)
b.box("q11cd", DK, 17, NOTE, "結果：network 被刪（成功／失敗記下）", 300)
b.box("q11d", L, 18, W12, "docker volume rm <差集內的 volume>", 300)
b.box("q11dd", DK, 18, NOTE, "結果：volume 被刪（成功／失敗記下）", 300)
b.box("q11z", L, 19, EXIT_C, "續「prune（2）」頁：帶「有刪除失敗？」狀態 → docker run 引擎 apply prune [--dry-run]（清暫存、刪進度檔）→ 摘要", 300)
b.H("qe0", "q0", "q0l"); b.D("qe0l", "q0l", "q0l2"); b.H("qe0x", "q0l2", "q0x"); b.D("qe0l2", "q0l2", "q1", al=True); b.H("qe1", "q1", "q2"); b.D("qe2", "q2", "q3"); b.H("qe3", "q3", "q3f", "讀")
b.D("qe4", "q3", "q4", al=True); b.D("qe4y", "q4", "q4y", "是", al=True); b.H("qe5", "q4y", "q4f"); b.D("qe6", "q4y", "q5"); b.DL("qe7", "q5", "q5q", "vk-resolve")
b.H("qe7x", "q5q", "q5x", "否"); b.D("qe7y", "q5q", "q6", "是", al=True)
b.H("qe6x", "q6", "q6x", "否"); b.D("qe8", "q6", "q7", "是", al=True); b.H("qe9", "q7", "q7d", "ls"); b.D("qe10", "q7", "q8"); b.D("qe11", "q8", "q9", al=True)
b.H("qe12", "q9", "q9y", "是"); b.D("qe13", "q9", "q10t", "否", al=True); b.H("qe13x", "q10t", "q10tx", "否"); b.D("qe13y", "q10t", "q10", "是", al=True)
b.H("qe14", "q10", "q10n", "否")
b.D("qe15", "q10", "q11l", "是", al=True); b.D("qe15a", "q11l", "q11a", al=True)
b.H("qe16a", "q11a", "q11ad", "rm"); b.D("qe16b", "q11a", "q11b"); b.H("qe16c", "q11b", "q11bd", "rm"); b.D("qe16d", "q11b", "q11c")
b.H("qe16e", "q11c", "q11cd", "rm"); b.D("qe16f", "q11c", "q11d"); b.H("qe16g", "q11d", "q11dd", "rm"); b.D("qe17", "q11d", "q11z", al=True)
b.close()
_A = F.abs
# q4 否（無活躍進度檔）→ q5：從菱形右側出、沿引擎欄右緣外（x=930）下到 q5 上方縫隙、左到 q5 右側 0.9 再下進頂端（跳過 q4y）
_sx, _sy, _sw, _sh = _A["q4"]; _tx, _ty, _tw, _th = _A["q5"]; _gy = F.rt["q5"] - F.gap / 2   # 走引擎欄左側（x=570；啟動器欄此段空），不穿 q4y → q4f 線
p9.append(_edge("qe4n", "q4", "q5", "否", (0, 0.5), (0.1, 0), [(570, _sy + _sh / 2), (570, _gy), (_tx + 0.1 * _tw, _gy)], -0.8, "below"))
# --dry-run：只印差集後直接續 apply prune --dry-run：走下游使用者欄與啟動器欄之間（x=250），標籤放垂直段左側、落在下游使用者欄空的列（q11b 列）
_qx, _qy, _qw, _qh = _A["q9y"]; _zx, _zy, _zw, _zh = _A["q11z"]; _gy = F.rt["q11z"] - F.gap / 2
_pts = [(_qx, _qy + _qh / 2), (30, _qy + _qh / 2), (30, _gy), (_zx + _zw / 2, _gy), (_zx + _zw / 2, _zy)]
_segs = [abs(b_[0] - a_[0]) + abs(b_[1] - a_[1]) for a_, b_ in zip(_pts, _pts[1:])]; _ly = (F.rt["q11b"] + F.rb["q11b"]) / 2
_pos = 2 * ((_segs[0] + (_ly - _pts[1][1])) / sum(_segs)) - 1
p9.append(_edge("qe12z", "q9y", "q11z", "續（2）：apply prune --dry-run（零刪除）", (0, 0.5), (0.5, 0), _pts[1:-1], _pos, True))
foot(p9, "p9", F.y, T9, {"note", "sub", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p9", "流程 v2：prune（1）resolve → 差集 → 刪", p9))

# ================= P9c：prune（2）apply 清暫存 → 刪進度檔 → 摘要 =================
p9c, F = newpage_c("流程 v2：prune（2）── apply prune：清暫存 → 刪進度檔 → 摘要（§1.2、§4.6）", N9, COLS_PR, gap=14)
b = F.band("bP2", "prune 第 2 段（承「prune（1）」頁）：docker run 引擎 apply prune [--dry-run]（flock → 重驗指紋 → --dry-run 只列出 → 建進度檔 → 清 .tmp.dist.* → 清殘留 .tmp.* → 每次刪除記成功／失敗 → 全部成功才刪進度檔）→ 0／1", v2=True)
b.box("q12z", L, 0, ENTRY, "來自「prune（1）」頁：四類資源已逐類刪、每個命令的成功／失敗已記下；或 --dry-run 只印了差集", 300)
b.box("q12", L, 1, W12, "docker run <引擎> apply prune [--dry-run]", 300)
b.box("q12ax", U, 2, O12, "逾時 → 1 + 6-26：確認無其他 vendor_kit 在跑後重試", 200)
b.box("q12a", E, 2, SUB, "apply prune：拿 flock 專案目錄（60 秒）", 340)
b.box("q12bx", U, 3, O12, "不同 → 1 + 6-12：請重跑", 200)
b.box("q12b", E, 3, SUB, "重驗指紋（與 vk-resolve 的 fingerprint 比）", 340)
b.box("q12dy", U, 4, G12, "是 → 0：只列出會清的暫存與殘留（零刪除；不建進度檔）", 200)
b.box("q12d", E, 4, D12, "--dry-run？", 200, ax="l")
b.box("q12j", E, 5, SUB, "否：建進度檔 .tmp.prune.<id>.toml（第一個寫入前；state=in-progress、done／pending）", 340)
b.box("q12jf", P, 5, F12, "＋.vendor_kit/.tmp.prune.<id>.toml（prune 自己的進度檔）", 330)
b.box("q12c", E, 6, SUB, "刪 trap 沒清到的殘留啟動器暫存 .tmp.dist.<id>/", 340)
b.box("q12cf", P, 6, F12, ".vendor_kit/.tmp.dist.<id>/（刪）", 330)
b.box("q12c2", E, 7, v2(SUB), "進度檔記結果：每個 .tmp.dist.* 的刪除成功／失敗各記一筆", 340)
b.box("q12c2f", P, 7, F12, ".vendor_kit/.tmp.prune.<id>.toml（done／failed 加一筆）", 330)
b.box("q12d2", E, 8, SUB, "刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列出）", 340)
b.box("q12df", P, 8, F12, ".vendor_kit/.tmp.<verb>.<id>.toml（殘留：刪；活躍：保留）", 330)
b.box("q12d3", E, 9, v2(SUB), "進度檔記結果：每個殘留 .tmp.<verb>.* 的刪除成功／失敗各記一筆", 340)
b.box("q12d3f", P, 9, F12, ".vendor_kit/.tmp.prune.<id>.toml（done／failed 加一筆）", 330)
b.box("q13x", U, 10, v2(R12), "否 → 1：摘要全列、失敗的標出；進度檔留著（下次可寫動詞先恢復：補做失敗的刪除）", 200)
b.box("q13", E, 10, v2(D12), "全部刪除成功？（含（1）頁四類資源）", 300, ax="l")
b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
b.D("qe17z", "q12z", "q12", al=True)
b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
b.H("qe19j", "q12j", "q12jf", "建"); b.D("qe18b", "q12j", "q12c"); b.H("qe19", "q12c", "q12cf", "刪")
b.D("qe18c2", "q12c", "q12c2"); b.H("qe19c2", "q12c2", "q12c2f", "寫"); b.D("qe18c", "q12c2", "q12d2"); b.H("qe19d", "q12d2", "q12df", "刪")
b.D("qe18d3", "q12d2", "q12d3"); b.H("qe19d3", "q12d3", "q12d3f", "寫"); b.D("qe18k", "q12d3", "q13", al=True)
b.H("qe21", "q13", "q13x", "否"); b.D("qe20", "q13", "q12k", "是", al=True); b.H("qe19k", "q12k", "q12kf", "刪"); b.DL("qe22", "q12k", "q14")
b.close()
foot(p9c, "p9c", F.y, T9B, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p9c", "流程 v2：prune（2）apply 清暫存", p9c))

# ================= P10：update =================
COLS_UP = [("下游使用者", 40, 220), ("啟動器（主機 sh）", 280, 280), ("引擎容器", 580, 400), ("registry（GHCR）", 1000, 290), ("專案目錄", 1310, 280)]
RG = "registry（GHCR）"
T10 = [
 ("update", "只查 registry 有沒有新版、不動任何檔（唯讀，不受CI 模式限制）；單段 docker run（不經 docker create/cp）；[<repo>] 省略 = 全部工具 + vendor_kit 自身；--exit-code：有新版回 2（給 CI 用）"),
 ("查最新", "對 registry 走 Docker Registry 標準協定：需要時以 WWW-Authenticate 換 token → GET /v2/<name>/tags/list（分頁）→ 取 SemVer 最大正式版（排除預發行）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」；查詢由引擎 resolve 模組在容器內做（藍格；token 以 -e 傳入）"),
 ("registry 憑證（Q11）", "VENDOR_KIT_REGISTRY_TOKEN（+ _USER）或 VENDOR_KIT_REGISTRY_TOKEN_FILE（啟動器 -v <file>:/run/vk-token:ro 掛入；兩者同設 → 1）；只在 update 單段及 upgrade 的 resolve 以 -e 傳入引擎；不寫 log／檔、不傳給工具、dry-run 不印；不掛 ~/.docker/config.json"),
 ("查詢失敗分類", "每個目標各自判定：認證（錯 token／無權限）、網路（連不上、逾時）、回應（registry 回錯誤碼）、解析（SemVer／分頁解析失敗）；任一類都記該目標 1 並繼續查下一個目標，最後彙總"),
 ("6-3", "無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）"),
 ("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」；舊薄殼對未知碼原樣傳出、不吞"),
 ("6-15（末行固定）", "update 最後一行永遠印「套用：just vendor_kit upgrade」，含未完成交易（6-33）那條出口"),
 ("6-33（未完成交易）", "唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；sync／update 結束 1、help 仍 0"),
]   # ≤ 8 條（6-3／6-15／6-33 各自成條，不再列 6-N 總條）
N10 = "已定（Q11、Q27、v2.6-5、v2.7-8、v2.8-7、v2.15-16、interface_spec §1.2 update）：無憑證時不支援需認證的版本列舉，該工具直接記失敗 1 + 6-3（不進 SemVer 解析；需人處理 → 橙），其他工具照查再彙總；查詢失敗依認證／網路／回應／解析分類，各記該目標 1 並繼續；_TOKEN 與 _TOKEN_FILE 同設 → 1；token 只在 update 單段及 upgrade 的 resolve 以 -e 傳（TOKEN_FILE 用 -v 掛）；update 唯讀、不受CI 模式限制；有新版只在 --exit-code 時回 2；末行固定印 6-15（含 6-33 出口）。"
p10, F = newpage_c("流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）", N10, COLS_UP, gap=16)
b = F.band("bU", "update [<repo>] [--exit-code]：建執行紀錄 → launcher_start → 憑證互斥檢查 → 單段引擎容器（偵測未完成交易 → 6-33 → 1）查 registry（公開／有 token → 查；無憑證 → 記 6-3；查詢失敗分類 → 記 1）→ 每個目標彙總（Q27）→ 末行 6-15 → 0／1／2", v2=True)
b.box("u0", U, 0, G12, "just vendor_kit update [<repo>] [--exit-code]", 220)
b.box("u0l", L, 0, v2(W12), LST1.replace("<verb>", "update"), 280)
b.box("u0x", U, 1, v2(R12), LSX, 220)
b.box("u0l2", L, 1, v2(W12), LST2, 280)
b.box("u1x", U, 2, O12, "是 → 1：只能擇一（改設其中一個）", 220)
b.box("u1q", L, 2, v2(D12), "_TOKEN 與 _TOKEN_FILE 同時設？", 280)
b.box("u1", L, 3, W12, "否：組 docker run 引數：-e VENDOR_KIT_REGISTRY_TOKEN／_USER，或 -v <TOKEN_FILE>:/run/vk-token:ro（只在 update 單段及 upgrade 的 resolve 傳）", 280)
b.box("u1r", L, 4, W12, "docker run <引擎> update（單段、不經 create/cp）", 280)
b.box("u2", E, 4, SUB, "update（唯讀；不受CI 模式限制）：讀 version.toml 現版", 400)
b.box("u2f", P, 4, F12, "version.toml（只讀：引擎 ref、[tools]）", 280)
b.box("u3x", U, 5, O12, "是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔；末行仍印 6-15）", 220)
b.box("u3", E, 5, D12, "有未完成交易（.tmp.<verb>.*.toml／[progress]）？", 400, ax="l")
b.box("u4l", E, 6, LBL, "否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）", 400, 24, ax="l", minh=24)
b.box("u5", E, 7, D12, "registry 不要求認證（公開）？", 300, ax=58)
b.box("u5g", RG, 7, v2(SUB), "是：GET /v2/<name>/tags/list（分頁）", 130, ax="r")
b.box("u6", E, 9, D12, "有 VENDOR_KIT_REGISTRY_TOKEN／_TOKEN_FILE？", 340, ax=12)
b.box("u6g", RG, 9, v2(SUB), "是：WWW-Authenticate 換 token → tags/list", 130, ax="l")
b.box("u6r", P, 9, RULE, "已定（Q11）：無憑證時不支援需認證的版本列舉；token 只在 update 單段及 upgrade 的 resolve 以 -e 傳，不寫 log、不傳給工具；GHCR 已測試，其他 registry 依標準協定可用但未驗證", 280)
b.box("u7q", E, 10, v2(D12), "查詢成功？", 200, ax=108)
b.box("u7c", E, 11, v2(SUB), "否：查詢失敗：分類原因（認證／網路／回應／解析）", 200, ax=60)
b.box("u8a", E, 11, SUB, "是：取 SemVer 最大正式版（排除預發行）", 150, ax="r")
b.box("u7f", E, 12, v2(SUB), "該目標記 1（無憑證 → 6-3，不查；否則附分類）→ 繼續下一目標", 220, ax=12)
b.box("u8b", E, 12, SUB, "與現版比較 → 記「現版 → 最新」", 150, ax="r")
b.box("u8q", E, 13, D12, "還有下一個目標？", 300, ax=58)
b.box("u9", E, 14, SUB, "否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的分類與 6-3）；訊息全列", 400)
b.box("u10", E, 15, SUB, "末行固定印 6-15：「套用：just vendor_kit upgrade」", 400)
b.box("u11x", U, 16, O12, "是 → 1：查詢失敗（6-3：設 token 或指定 <repo>@<tag>；其他分類印原因；即使另有新版）", 220)
b.box("u11", E, 16, D12, "任一目標查詢失敗（1）？", 300, ax="l")
b.box("u12y", U, 17, O12, "是 → 2：有新版（給 CI 用）", 220)
b.box("u12", E, 17, D12, "有新版且 --exit-code？", 300, ax="l")
b.box("u13", U, 18, G12, "否 → 0：已列出（有新版也 0）", 220)
b.H("ue0", "u0", "u0l"); b.D("ue0l", "u0l", "u0l2"); b.H("ue0lx", "u0l2", "u0x"); b.D("ue0l2", "u0l2", "u1q", al=True); b.H("ue0x", "u1q", "u1x", "是"); b.D("ue0q", "u1q", "u1", "否", al=True); b.D("ue0b", "u1", "u1r"); b.H("ue1", "u1r", "u2"); b.H("ue2", "u2", "u2f", "讀"); b.D("ue3", "u2", "u3", al=True)
b.H("ue4", "u3", "u3x", "是"); b.D("ue5", "u3", "u4l", al=True); b.D("ue6", "u4l", "u5", al=True)
b.H("ue7", "u5", "u5g", "是"); b.D("ue8", "u5", "u6", "否", al=True); b.H("ue9", "u6", "u6g", "是"); b.D("ue10", "u6", "u7f", "否", sx=0.1, tx=0.1, al=True)
b.DL("ue11", "u5g", "u7q"); b.DL("ue12", "u6g", "u7q")
b.D("ue13q", "u7q", "u7c", "否", al=True); b.RD("ue13y", "u7q", "u8a", "是"); b.D("ue13c", "u7c", "u7f", al=True); b.D("ue13f", "u7f", "u8q", al=True)
b.D("ue13b", "u8a", "u8b"); b.D("ue14", "u8b", "u8q", al=True)
b.LL("ue14y", "u8q", "u5", "是：下一個目標", busx=562); b.D("ue14n", "u8q", "u9", "否", al=True)   # u6／u7 左緣 x=592：回圈線（x=562）離框 30（r11）
b.D("ue15", "u9", "u10"); b.D("ue16", "u10", "u11", al=True)
b.H("ue17", "u11", "u11x", "是"); b.D("ue18", "u11", "u12", "否", al=True); b.H("ue19", "u12", "u12y", "是"); b.DL("ue20", "u12", "u13", "否")
b.close()
foot(p10, "p10", F.y, T10, {"note", "rule", "sub", "hdr", "v2"})
pages_v1_c.append(("v1p10", "流程 v2：update", p10))

# ================= P11：初始檔五態 =================
COLS_ST = [("deleted", 40, 290), ("managed", 350, 290), ("declined", 660, 290), ("appended", 970, 290), ("unmanaged", 1280, 290)]
SD, SM, SC, SA, SU = "deleted", "managed", "declined", "appended", "unmanaged"
T11 = [
 ("metadata [[file]].state（Q15、16 條）", "baseline/<repo>/.vendor_kit.toml 對每個初始檔一筆：state 單一列舉 managed／appended／declined／unmanaged／deleted；declined_hash（選填）= 最近一次被拒絕的那版新版初始檔 N 的 sha256；lines（只在 appended）= 實際插入的行原文"),
 ("declined 語意（v2.7-3）", "state=declined 只用於「初始檔要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新 → state 不變、只記 declined_hash（畫成自環）；add 時 append 檔已存在且拒絕 → unmanaged（本來就有、沒納管）；二進位拒絕同"),
 ("B／D／N", "B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過"),
# ================= P16：離線包（1）bootstrap.sh --local =================
COLS_OF = [("下游使用者（離線機）", 40, 230), ("bootstrap.sh（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("引擎容器", 970, 320), ("專案目錄", 1310, 280)]
SH = "bootstrap.sh（主機 sh）"; UO = "下游使用者（離線機）"
COLS_OF2 = [("下游使用者（離線機）", 40, 230), ("啟動器（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("引擎容器", 970, 320), ("專案目錄", 1310, 280)]
LA = "啟動器（主機 sh）"
T16 = [
 ("離線包（#27、Q26）", "Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援"),
 ("bootstrap.sh --local（契約入口）", "離線接入的契約入口 = bootstrap.sh --local <引擎 tar>（interface_spec §1.2）：只涉及引擎（docker load → install）；-t <repo> 走 registry、需網路，離線機不帶；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做、在建執行紀錄之前；值的判別依序互斥（B1，v3.5）：以 .tar 結尾 → 檔案（必須存在）→ load + 讀 .digest；否則含 / 且存在同名檔 → 1 + 6-37；否則 → image tag（只 inspect image ID；含 / 但無同名檔的完整 ref 也是 tag 形）"),
 ("add --local 只收 tar（v2.10-3）", "add --local <值> 只接受存在的 .tar 檔（新工具沒有既有 digest 可用；tag 形只對 bootstrap.sh --local 有意義）；不是存在的 .tar → 1 + 6-24 add --local 分句「add --local 只接受存在的 .tar 檔：<v>」；§1.1 選項表的 tag 形只適用 bootstrap.sh"),
 ("工具 tar（來源，v2.8-5）", "離線接工具要另備工具 tar：由下游 repo 自己提供（docker save 的 <repo>-dist image + 同名 .tar.digest 旁檔，一行 sha256:<hex64> = 該工具的正式 index digest），不在 vendor_kit 離線包內；下游使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add <repo> --local <工具 tar>"),
 ("local_bootstrap.sh（便利包裝，非契約）", "離線包內附的可選腳本：docker version --format '{{.Server.Arch}}' 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local <tar> \"$@\"；不是契約入口、不另定介面（v2.7-1）"),
 (".digest 旁檔", "<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1 + 6-24 主機錯誤分類）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id"),
 ("image ID 記錄", "docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format '{{.Id}}' 取 image ID：引擎的本機覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）"),
 ("baseline/.gitkeep", "VK 自產的進 git 空檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；install 建、uninstall 刪、hash 固定為空檔（§4.0；v2.15-14）；工具的 metadata 由 add 才建（baseline/<repo>/.vendor_kit.toml 兼作該工具目錄的佔位）"),
 ("離線可用（Q26）", "啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"),
 ("sync 快路徑（Q22）／--verify（F5）", "sync（無參數）啟動器只用 grep 比對 gen/.stamp 第一行 == version.toml 引擎 ref、gen/<repo>.stamp 第一行 == 鎖定 digest、每個 cache/<repo>/ 存在（目錄或 symlink）、tools.just 存在、無 .tmp.*、非 CI 模式 → 全相符不起容器 0；有差才起引擎；sync --verify 或 CI 模式或版本變動那次 → 先驗既有 cache（每檔 sha256），不符才重裝一次，再驗仍不符 → 失敗"),
 T_MSG,
]
N16 = "已定（Q26、v2.6-1、v2.7-1／-2、v2.8-4／-5、v2.13 P4、v2.15-2／-14／-17、v2.16-4、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 非契約）；先驗 git／just 再建執行紀錄；--local 依序判別（.tar 結尾 → 檔案；否則含 / 且有同名檔 → 6-37；否則 tag）；最低介面版檢查在起容器之前（斷網也回 3）；tar 附同名 .digest；install 第一個寫入前建 .tmp.install；version.toml 寫正式 ref@digest；離線 upgrade 不支援。"
COLS_OF1 = [("下游使用者（離線機）", 40, 230), ("bootstrap.sh（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("bootstrap.sh（tag 形分支）", 970, 320), ("專案目錄", 1310, 280)]   # 本頁無引擎容器：第 4 欄給 tag 形分支（同一個 bootstrap.sh）
SH2 = "bootstrap.sh（tag 形分支）"
p16, F = newpage_c("流程 v2：離線包（1）── bootstrap.sh --local → 判別值 → load → image ID → 介面版（#27、Q26）", N16, COLS_OF1, gap=14)
b = F.band("bO1", "離線接入（1）只涉及引擎：bootstrap.sh --local <引擎 tar> → 前置檢查（git／just）→ 執行紀錄 → 判別值（.tar → 檔案；含 / 且有同名檔 → 6-37；否則 tag）→ load + .digest（tag 形只 inspect）→ image ID → LABEL 最低介面版 → 續（1′）", v2=True)
b.box("o0", UO, 0, G12, "有網路的機器下載離線包 vendor_kit-vN-local.tar.gz → 帶到離線機", 230)
b.box("o1", UO, 1, W12, "解開（SHA256SUMS 驗）：bootstrap.sh、各平台引擎 tar + .digest、local_bootstrap.sh；不含工具 tar", 230)
b.box("o1w", UO, 2, LBL, "【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：", 500, 24, ax="l", minh=24)
b.box("o1a", UO, 3, W12, "docker version 偵測 daemon 架構（.Server.Arch）", 230)
b.box("o1b", UO, 4, W12, "挑該平台的引擎 tar（vendor_kit-vN-<arch>.tar）", 230)
b.box("o1c", UO, 5, W12, "exec ./bootstrap.sh --local <tar> \"$@\"", 230)
b.box("o2", UO, 6, W12, "sh bootstrap.sh --local <引擎 tar> [-y]（契約入口；-t <repo> 走 registry 需網路，離線機不帶）", 230)
b.box("o5x", UO, 7, O12, "否 → 1 + 6-16：請先 git init（執行紀錄尚未建）", 230)
b.box("o5", SH, 7, D12, "在 git repo 內？", 300, ax="l")
b.box("o6x", UO, 8, O12, "否 → 1 + 6-23：請裝 release 版 just（執行紀錄尚未建）", 230)
b.box("o6", SH, 8, D12, "just ≥ 1.33.0？", 300, ax="l")
b.box("o2s", SH, 9, v2(W12), "是：建執行紀錄 log/bootstrap/<ts>-<id8>.jsonl", 400)
b.box("o2x", UO, 10, v2(R12), LSX, 230)
b.box("o2s2", SH, 10, v2(W12), LST2, 400)
b.box("o3", SH, 11, v2(D12), "--local 值以 .tar 結尾？", 300, ax="l")
b.box("o3n", P, 11, v2(RULE), "已定（B1 依序互斥；v3.5 #164、v2.16-4）：以 .tar 結尾 → 檔案路徑（必須存在）→ docker load；否則含 / 且存在同名檔 → 1 + 6-37；否則 → image tag（不 load、只 inspect，本機無 → 1；含 / 但無同名檔的完整 ref 也是 tag 形）；前置檢查（git／just）不分型別一律先做、在建執行紀錄之前", 280)
b.box("o3bx", UO, 12, v2(O12), "否 → 1：檔案路徑必須存在（請檢查路徑）", 230)
b.box("o3b", SH, 12, D12, "是：該路徑的檔案存在？", 300, ax="l")
b.box("o3c", SH2, 12, v2(D12), "否：值含 / 且存在同名檔？", 300, ax="l")
b.box("o3cx", P, 12, v2(O12), "是 → 1 + 6-37：--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。", 280)
b.box("o4x", UO, 13, R12, "否 → 1 + 6-24（主機錯誤）：同名 .tar.digest 旁檔缺", 230)
b.box("o4", SH, 13, D12, "是：同名 .tar.digest 存在？", 300, ax="l")
b.box("o3t", SH2, 13, v2(W12), "否 → tag 形：不 load、不讀 .digest", 300)
b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
b.box("o7cx", UO, 17, v2(O12), "否 → 3 + 6-18：零寫入（斷網也回 3；請以較新的離線包重建）", 230)
b.box("o7c", SH, 17, v2(D12), "inspect LABEL ….protocol：image 的介面版 ≥ 薄殼最低介面版？（不起容器、不上網）", 400, ax="l")
b.box("o7z", SH, 18, ENTRY, "是 → 續「離線包（1′）」頁：docker run 本機 image install → version.local.toml", 400)
b.D("oe0", "o0", "o1"); b.D("oe1", "o1", "o1w", al=True); b.D("oe1a", "o1w", "o1a", al=True); b.D("oe1b", "o1a", "o1b"); b.D("oe1c", "o1b", "o1c"); b.D("oe1w", "o1c", "o2")
b.H("oe6x", "o5", "o5x", "否"); b.D("oe6b", "o5", "o6", "是", al=True); b.H("oe6bx", "o6", "o6x", "否"); b.D("oe6c", "o6", "o2s", "是", al=True); b.D("oe2s", "o2s", "o2s2"); b.H("oe2x", "o2s2", "o2x"); b.D("oe2l", "o2s2", "o3", al=True)
b.RD("oe3c", "o3", "o3c", "否"); b.D("oe3b", "o3", "o3b", "是", al=True); b.H("oe3bx", "o3b", "o3bx", "否")
b.H("oe3cx", "o3c", "o3cx", "是"); b.D("oe3t", "o3c", "o3t", "否", al=True); b.D("oe3ti", "o3t", "o3ti", al=True); b.H("oe3tx", "o3ti", "o3tx", "否")
b.D("oe4", "o3b", "o4", "是", al=True); b.H("oe5", "o4", "o4x", "否"); b.D("oe7", "o4", "o6c", "是", al=True)
b.H("oe8", "o6c", "o6d", "載"); b.D("oe9", "o6c", "o7a"); b.D("oe9b", "o7a", "o7b", al=True); b.H("oe9d", "o7b", "o7bd")
_A = geo(b); _tx, _ty, _tw, _th = _A["o3ti"]; _bx, _by, _bw, _bh = _A["o7b"]; _gy = _by - F.gap / 2   # tag 形匯入：從 o3ti 底端下到 o7b 上方縫隙、左到 o7b 右側 0.9 進頂端（縫隙內無其他格；不穿「載」線）
b.P("oe3tj", "o3ti", "o7b", "是：tag 形（跳過 load／.digest）", (0.5, 1), (0.9, 0), [(_tx + _tw / 2, _gy), (_bx + 0.9 * _bw, _gy)], pos=-0.7, vert=True)
b.D("oe9c", "o7b", "o7c", al=True); b.H("oe9cx", "o7c", "o7cx", "否"); b.D("oe10z", "o7c", "o7z", "是", al=True)
b.close()
_A = F.abs; _sx, _sy, _sw, _sh = _A["o2"]; _tx, _ty, _tw, _th = _A["o5"]; _gy = F.rt["o5"] - F.gap / 2   # o2 右側出、沿欄間 x=275 下到 o5 上方縫隙、右到 o5 頂點進（不與 o5 → o5x「否」線同段；r13 oe2）
p16.append(_edge("oe2", "o2", "o5", "", (1, 0.5), (0.5, 0), [(275, _sy + _sh / 2), (275, _gy), (_tx + _tw / 2, _gy)]))
_T16A = {r[0]: r for r in T16}
T16A = [_T16A["bootstrap.sh --local（契約入口）"], _T16A["離線包（#27、Q26）"], _T16A[".digest 旁檔"], _T16A["image ID 記錄"], _T16A["local_bootstrap.sh（便利包裝，非契約）"], T_MSG]   # ≤ 8；add --local／工具 tar／斷網 sync 的名詞在「離線包（2）」頁
foot(p16, "p16", F.y, T16A, {"note", "rule", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16", "流程 v2：離線包（1）bootstrap.sh --local", p16))

# ================= P16i：離線包（1′）docker run install =================
p16i, F = newpage_c("流程 v2：離線包（1′）── docker run 本機 image install → version.local.toml（#27、Q26、§4.8）", N16, COLS_OF, gap=14)
b = F.band("bO1i", "離線接入（1′）：docker run 本機 image install（不 pull）→ 建進度檔 → 寫入（見 install 頁）→ 任一寫入失敗？是 → 引擎依進度檔清半成品 → 1；否 → 刪進度檔 → 寫 version.local.toml（本機 tag + image ID）→ 續（2）逐工具 add --local", v2=True)
b.box("o8z", SH, 0, ENTRY, "來自「離線包（1）」頁：tar 已 load 並讀到正式 index digest（或 tag 形已核本機 image）；image ID 已取得、LABEL 介面版已過", 400)
b.box("o8", SH, 1, W12, "docker run 本機 image install（本機有 → 不 pull）", 400)
b.box("o8j", E, 1, SUB, "install：建進度檔 .tmp.install.<id>.toml（第一個寫入前；= 不留半成品的清除清單）", 320)
b.box("o8jf", P, 1, F12, "＋.vendor_kit/.tmp.install.<id>.toml", 280)
b.box("o8e", E, 2, ENTRY, "續「install（1′）」頁與「install（2）」頁的寫入段（與線上接入相同；version.toml 第一行最後寫）", 320)
b.files("o8f", P, 2, "install 寫（log/ 由啟動器先建）", ["version.toml 第一行 = 正式 ref@digest（tar 形：.digest 旁檔；tag 形：既有 version.toml 值，第一次接入用 bootstrap.sh 內嵌引擎 ref）", "薄殼五檔、gen/.stamp", "baseline/.gitkeep（VK 自產進 git 空檔）", "config.toml ＋ 基準版副本 ＋ metadata", "justfile 一行、.dockerignore 四行"], 280)
b.box("o8e2", E, 3, ENTRY, "來自「install（2）」頁：寫入段結束（成功或任一步失敗）", 320)
b.box("o8x", UO, 4, v2(R12), "是 → 1：引擎依進度檔清半成品、不留半成品（log/ 保留）；引擎異常結束時由 bootstrap.sh 補清", 230)
b.box("o8q", E, 4, v2(D12), "任一寫入失敗？", 220, ax="l")
b.box("o8k", E, 5, v2(SUB), "否：刪進度檔 .tmp.install.<id>.toml（最後一步）= install 完成", 320)
b.box("o8kf", P, 5, F12, "－.vendor_kit/.tmp.install.<id>.toml（刪）", 280)
b.box("o9", SH, 6, W12, "install 成功後寫 version.local.toml：vendor_kit = \"vendor_kit:vN\" + vendor_kit_image_id", 400)
b.box("o9f", P, 6, F12, "version.local.toml（不進 git）：本機 tag + image ID", 280)
b.box("o9z", SH, 7, ENTRY, "續「離線包（2）」頁：另備工具 tar，逐一 add <repo> --local；之後斷網 sync 見「離線包（3）」頁", 400)
b.D("oe10", "o8z", "o8", al=True)
b.H("oe11", "o8", "o8j"); b.H("oe11f", "o8j", "o8jf", "建"); b.D("oe11e", "o8j", "o8e", al=True); b.H("oe12", "o8e", "o8f", "寫"); b.D("oe12e", "o8e", "o8e2"); b.D("oe12q", "o8e2", "o8q", al=True)
b.H("oe13x", "o8q", "o8x", "是"); b.D("oe13n", "o8q", "o8k", "否", al=True); b.H("oe12kf", "o8k", "o8kf", "刪")
b.DL("oe13", "o8k", "o9"); b.H("oe14", "o9", "o9f", "寫"); b.D("oe15", "o9", "o9z", al=True)
b.close()
T16I = [_T16A["離線包（#27、Q26）"], _T16A[".digest 旁檔"], _T16A["image ID 記錄"], _T16A["baseline/.gitkeep"], ("install 進度檔（v2.13 P5）", "第一次 install 也在第一個寫入前建 .tmp.install.<id>.toml：兼「不留半成品」的清除清單，失敗依它移除已寫的檔（log/ 保留）、成功後刪；修復型同"), T_MSG]
foot(p16i, "p16i", F.y, T16I, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16i", "流程 v2：離線包（1′）docker run install", p16i))

# ================= P16c：離線包（2）add --local 逐工具 =================
_T16 = {r[0]: r for r in T16}
T_CACHE = ("gen/<repo>.stamp／gen/tools.just", "gen/<repo>.stamp = 印記（第一行 index digest，之後每檔 sha256）；gen/tools.just = 每工具一行 mod?（最後寫、與 cache 同一 apply 內原子替換）；都由引擎 apply（fetch 模組）寫")
T16B = [_T16["add --local 只收 tar（v2.10-3）"], _T16["工具 tar（來源，v2.8-5）"], _T16[".digest 旁檔"], _T16["image ID 記錄"], T_FP, T_CACHE, T_MSG]   # ≤ 8；離線包／resolve 第 0 頁或（1）頁已有
p16c, F = newpage_c("流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具（Q26、§4.8、§7.4-16）", N16, COLS_OF2, gap=14)
b = F.band("bO1b", "離線接工具（v2.8-5、v2.10-3）：另備工具 tar → 每工具各跑一次 add <repo> --local <tar>：執行紀錄 → 驗 .tar → load → .digest → image ID → resolve（0 且文法合）→ 續（2′）create／cp → apply", v2=True)
b.box("oo0", UO, 0, ENTRY, "來自「離線包（1）」頁：install 完成（引擎可離線跑）", 230)
b.box("oo1", UO, 1, W12, "有網路的機器下載工具 tar + 同名 .tar.digest（下游 repo 提供；不在 vendor_kit 離線包內）", 230)
b.box("oo1n", P, 1, RULE, "已定（v2.8-5）：離線包只含引擎；離線接工具 = 另備工具 tar（下游 repo 的 docker save + .digest），逐工具 add --local；離線 upgrade 不支援", 280)
b.box("oo1b", UO, 2, W12, "帶到離線機；之後每個工具各跑一次（一次一個）↓", 230)
b.box("o10", UO, 3, W12, "just vendor_kit add <repo> --local <工具 tar> [--source <image>] [-y] [--dry-run] [--timeout <秒>]", 230)
b.box("o10s", LA, 3, v2(W12), LST1.replace("<verb>", "add"), 400)
b.box("o10sx", UO, 4, v2(R12), LSX, 230)
b.box("o10s2", LA, 4, v2(W12), LST2, 400)
b.box("o10qx", UO, 5, R12, "否 → 1 + 6-24 分句：add --local 只接受存在的 .tar 檔：<v>", 230)
b.box("o10q", LA, 5, D12, "值是存在的 .tar 檔？", 300, ax="l")
b.box("o10a", LA, 6, W12, "是：docker load < <工具 tar>", 400)
b.box("o10d", DK, 6, IMG, "本機 image <repo>-dist:<tag>", 240)
b.box("o10bx", UO, 7, R12, "否 → 1 + 6-24（主機錯誤）：同名 .tar.digest 旁檔缺", 230)
b.box("o10bq", LA, 7, v2(D12), "同名 .tar.digest 存在？", 300, ax="l")                       # 旁檔缺 → 出口（與離線包(1) o4 一致；r11）
b.box("o10b", LA, 8, W12, "是：讀 <工具 tar>.digest → 正式 index digest", 400)
b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
b.box("o10vx", UO, 13, R12, "不合 → 1 + 6-30：不動 docker", 230)
b.box("o10v", LA, 13, v2(D12), "是：收完整份、驗首尾／筆數／kind：文法合？", 300, ax="l")
b.box("o10pz", LA, 14, ENTRY, "是 → 續「離線包（2′）」頁：docker create／cp → apply add", 400)
b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
b.H("oe21x", "o10q", "o10qx", "否")
b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
b.close()
foot(p16c, "p16c", F.y, T16B, {"note", "rule", "sub", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16c", "流程 v2：離線包（2）add --local 逐工具", p16c))

# ================= P16cb：離線包（2′）add --local：create／cp → apply（第十六輪自（2）拆頁）=================
T16BB = [_T16["image ID 記錄"], T_FP, T_CACHE, T_MSG]
p16cb, F = newpage_c("流程 v2：離線包（2′）── add --local：docker create／cp → apply add（Q26、§4.8、§7.4-16）", N16, COLS_OF2, gap=14)
b = F.band("bO1c", "離線接工具（2′）（承「離線包（2）」頁）：docker create／cp 本機 image 的 dist → apply add（flock → 重驗指紋 → --dry-run → [progress] → metadata → 續 add（2）其餘寫入 → version.toml 最後寫）→ 0", v2=True)
b.box("o10p0", LA, 0, ENTRY, "來自「離線包（2）」頁：resolve 0 且 vk-resolve 文法合（extract 清單、指紋）", 400)
b.box("o10p", LA, 1, W12, "docker create／cp 取本機 image 的 dist 到暫存 .tmp.dist.<id>/<repo>/（不 pull）", 400)
b.box("o10p2", LA, 2, W12, "docker run 引擎 apply add [--dry-run]（暫存唯讀掛進 /dist）", 400)
b.box("o10ex", UO, 3, O12, "逾時 → 1 + 6-26：確認無其他 vendor_kit 在跑後重試", 230)
b.box("o10e", E, 3, SUB, "apply add：拿 flock 專案目錄（60 秒）", 320)
b.box("o10ex2", UO, 4, v2(O12), "≠ → 1 + 6-12：指紋不同，請重跑", 230)
b.box("o10e2", E, 4, SUB, "重驗指紋（與 vk-resolve 的 fingerprint 比）", 320)
b.box("o10dy", UO, 5, G12, "是 → 0：唯讀預覽會建／會問哪些檔（不建進度檔）", 230)
b.box("o10dq", E, 5, D12, "--dry-run？", 200, ax="l")
b.box("o10pg", E, 6, SUB, "否：metadata 建 [progress]（第一個寫入前）", 320)
b.box("o10pgf", P, 6, F12, "＋baseline/<repo>/.vendor_kit.toml [progress]", 280)
b.box("o10e3", E, 7, SUB, "寫 metadata：source（正式 ref@digest）+ local_image_id", 320)
b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
b.D("oe26a", "o10p0", "o10p", al=True)
b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
b.DL("oe28", "o10e4", "o11")
b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))

# ================= P16cc：離線包（3）斷網 sync：快路徑 → inspect → resolve =================
T16C = [_T16["離線可用（Q26）"], _T16["sync 快路徑（Q22）／--verify（F5）"], _T16["image ID 記錄"], T_MSG]   # ≤ 8
p16cc, F = newpage_c("流程 v2：離線包（3）── 斷網 sync：快路徑 → inspect（本機覆寫優先）→ docker run resolve（Q26、§3.6）", N16, COLS_OF2, gap=14)
b = F.band("bO2", "斷網下 sync／build 必成功（Q26）：執行紀錄 → 快路徑全相符 → 0；有差 → 本機覆寫？是 → inspect <tag> 核 image ID → 相符直接用本機 tag；否 → inspect 正式 ref → 本機有就不 pull → docker run resolve sync → 續（3″）", v2=True)
b.box("w0", UO, 0, G12, "斷網：just <ns> build（自動 _sync）／just vendor_kit sync [--verify]", 230)
b.box("w0l", LA, 0, v2(W12), LST1.replace("<verb>", "sync"), 400)
b.box("w0x", UO, 1, v2(R12), LSX, 230)
b.box("w0l2", LA, 1, v2(W12), LST2, 400)
b.box("w1", LA, 2, v2(W12), "快路徑：grep 比對 gen/*.stamp 第一行 vs version.toml（引擎 ref、每工具 digest）、每個 cache/<repo>/ 存在、tools.just 存在、無 .tmp.*", 400)
b.box("w5a", UO, 3, G12, "是 → 0：不起容器（sync_fast_path；驗收 §7.4-17）", 230)
b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
b.box("w3p", LA, 8, W12, "無：docker pull <ref>（--timeout 內）", 260, ax="l")
b.box("w3x", UO, 9, R12, "否 → 1 + 6-24／6-31：斷網拉不到／逾時（--timeout 內結束、不 hang）", 230)
b.box("w3pq", LA, 9, D12, "pull 成功？", 220, ax="l")
b.box("w4", LA, 10, W12, "docker run（不 pull；本機覆寫相符 → 用本機 tag）resolve sync（永不 -t）", 400)
b.box("w3d", DK, 10, IMG, "本機已有的 image（docker load 過／pull 到的）", 240)
b.box("w4zz", LA, 11, ENTRY, "續「離線包（3″）」頁：resolve sync 驗 image ID → 三叉 → apply|no？", 400)
b.H("we0", "w0", "w0l"); b.D("we0l", "w0l", "w0l2"); b.H("we0x", "w0l2", "w0x"); b.D("we0l2", "w0l2", "w1", al=True); b.D("we1", "w1", "w1q", al=True); b.H("we1y", "w1q", "w5a", "是"); b.D("we2", "w1q", "w2q", "否", al=True)
b.D("we2a", "w2q", "w2a", "是", al=True); b.H("we2ax", "w2a", "w2ax", "≠"); b.H("we4", "w4", "w3d", "用")
b.D("we3", "w2b", "w3", al=True); b.D("we3p", "w3", "w3p", "無", al=True); b.D("we3pq", "w3p", "w3pq", al=True); b.H("we3x", "w3pq", "w3x", "否"); b.D("we3py", "w3pq", "w4", "是", al=True)
b.D("we6", "w4", "w4zz", al=True)
b.close()
_A = F.abs
# w2q 否（無本機覆寫）→ w2b（跳過 w2a 列）：從菱形左側出、沿下游使用者欄與啟動器欄之間（x=280）下到 w2b 上方縫隙、右到 w2b 頂端中心（w2a 的 ≠ 出口在右側 DK 欄，不交叉）
_sx, _sy, _sw, _sh = _A["w2q"]; _tx, _ty, _tw, _th = _A["w2b"]; _gy = F.rt["w2b"] - F.gap / 2
p16cc.append(_edge("we2n", "w2q", "w2b", "否", (0, 0.5), (0.5, 0), [(280, _sy + _sh / 2), (280, _gy), (_tx + 0.5 * _tw, _gy)], -0.8, "below"))
# w2a 相符 → w4：直接用本機 tag，不再 inspect 正式 ref、不 pull（codex r13 N6／R57）：從菱形底邊右側（x=560）直下進 w4 頂端（w2b／w3／w3p／w3pq 都 ≤ 550 寬）
_sx, _sy, _sw, _sh = _A["w2a"]; _tx, _ty, _tw, _th = _A["w4"]; _ly = (F.rt["w3p"] + F.rb["w3p"]) / 2
_pos = 2 * ((_ly - (_sy + _sh)) / (_ty - (_sy + _sh))) - 1
p16cc.append(_edge("we2y", "w2a", "w4", "相符：用本機 tag（不 pull）", (0.9, 1), (round((560 - _tx) / _tw, 3), 0), [], _pos, True))
# w3 有 → w4：從菱形右側出、到 x=580 直下進 w4 頂端（跳過 pull 兩列；與 we2y 平行 20px）
_sx, _sy, _sw, _sh = _A["w3"]
p16cc.append(_edge("we5", "w3", "w4", "有", (1, 0.5), (round((580 - _tx) / _tw, 3), 0), [(580, _sy + _sh / 2)], -0.6, "below"))
foot(p16cc, "p16cc", F.y, T16C, {"note", "rule", "sub", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16cc", "流程 v2：離線包（3）斷網 sync", p16cc))

# ================= P16ccb：離線包（3″）resolve sync 驗證 → apply|no（第十六輪自（3）拆頁）=================
T16CB = [_T16["image ID 記錄"], _T16["sync 快路徑（Q22）／--verify（F5）"], T_MSG]
p16ccb, F = newpage_c("流程 v2：離線包（3″）── resolve sync：驗 image ID → 三叉 → 6-33／6-13 → apply|no？（Q26、§3.6）", N16, COLS_OF2, gap=14)
b = F.band("bO2b", "斷網 sync（3″）（承「離線包（3）」頁）：resolve sync 驗 image ID == metadata local_image_id → 算 extract 清單與指紋 → resolve 0 且文法合 → 未完成交易 6-33 ／ 無完成標記 6-13 → apply|no → 0；否則續（3′）apply sync", v2=True)
b.box("w4z0", LA, 0, ENTRY, "來自「離線包（3）」頁：docker run（不 pull）resolve sync 已起（本機 tag 或正式 ref）", 400)
b.box("w4ex", UO, 1, R12, "≠ → 1：image ID ≠ metadata local_image_id（離線對照 index digest）", 230)
b.box("w4e", E, 1, v2(D12), "resolve sync：image ID == metadata local_image_id？", 300, ax="l")
b.box("w4e2", E, 2, v2(SUB), "是：算 extract 清單與指紋", 320)
b.box("w4rx", UO, 3, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
b.box("w4rq", LA, 3, v2(D12), "resolve 結束碼 0？", 300, ax="l")
b.box("w4vx", UO, 4, v2(R12), "不合 → 1 + 6-30：不動 docker", 230)
b.box("w4v", LA, 4, v2(D12), "是：收完整份、驗首尾／筆數／kind：文法合？", 300, ax="l")
b.box("w4tx", UO, 5, v2(O12), "是 → 1 + 6-33：請先重跑原動詞", 230)
b.box("w4t", E, 5, v2(D12), "是：有未完成交易（.tmp.<verb>.*／[progress]）？", 300, ax="l")
b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
b.H("we6tx", "w4t", "w4tx", "是"); b.D("we6m", "w4t", "w4m", "否", al=True); b.H("we6mx", "w4m", "w4mx", "否"); b.D("we6q", "w4m", "w4q", "是", al=True)
b.H("we6y", "w4q", "w4qy", "是"); b.D("we6n", "w4q", "w4z", "否", al=True)
b.close()
foot(p16ccb, "p16ccb", F.y, T16CB, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16ccb", "流程 v2：離線包（3″）resolve sync 驗證", p16ccb))

# ================= P16ccc：離線包（3′）apply sync：先驗後重裝一次 =================
T16D = [_T16["離線可用（Q26）"], _T16["sync 快路徑（Q22）／--verify（F5）"], _T16["image ID 記錄"], T_FP, T_CACHE, T_MSG]
p16ccc, F = newpage_c("流程 v2：離線包（3′）── apply sync：先驗既有 cache、不符才重裝一次（Q26、§3.6）", N16, COLS_OF2, gap=14)
b = F.band("bO3", "斷網 sync（3′）：create／cp 本機 image 的 /dist → apply sync：flock → 重驗指紋 → 先驗既有 cache（--verify／CI／版本變動那次）→ 相符：tools.just 缺才重生；不符 → 重裝一次 → 再驗 → 仍不符 → 失敗；相符 → 最後原子重生 tools.just → 0", v2=True)
b.box("w4x0", LA, 0, ENTRY, "來自「離線包（3）」頁：resolve sync 算出 apply|yes（extract 清單 + 指紋）", 400)
b.box("w4x1", LA, 1, v2(W12), "docker create／cp 取本機 image 的 /dist 到暫存 .tmp.dist.<id>/<repo>/（不 pull）", 400)
b.box("w4p", LA, 2, v2(W12), "docker run（不 pull）apply sync（暫存唯讀掛進 /dist）", 400)
b.box("w4lx", UO, 3, v2(O12), "逾時 → 1 + 6-26：確認無其他 vendor_kit 在跑後重試", 230)
b.box("w4l", E, 3, v2(SUB), "apply sync：拿 flock 專案目錄（60 秒）", 320)
b.box("w4lx2", UO, 4, v2(O12), "≠ → 1 + 6-12：指紋不同，請重跑", 230)
b.box("w4l2", E, 4, v2(SUB), "重驗指紋（與 vk-resolve 的 fingerprint 比）", 320)
b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
b.box("w5t", UO, 9, G12, "→ 0：cache 相符、已補 tools.just", 230)
b.box("w4r", E, 10, SUB, "否：重裝一次：從 /dist 重寫 cache/<repo>/（暫存 → 整批替換；warn）", 320)
b.box("w4rf", P, 10, F12, "cache/<repo>/（只寫不進 git 的）", 280)
b.box("w4r2", E, 11, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
b.box("w4r2f", P, 11, F12, "gen/<repo>.stamp", 280)
b.box("w4v2", E, 12, v2(SUB), "重裝後再驗一次（逐檔 sha256）", 320)
b.box("w4v2x", UO, 13, R12, "否 → 1：驗證失敗（不無限重裝）", 230)
b.box("w4v2q", E, 13, v2(D12), "全相符？", 200, ax="l")
b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
b.close()
_A = F.abs
# w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）
_sx, _sy, _sw, _sh = _A["w4vq"]; _tx, _ty, _tw, _th = _A["w4r0"]; _gy = F.rt["w4r0"] - F.gap / 2
p16ccc.append(_edge("wf5n", "w4vq", "w4r0", "否", (1, 0.5), (0.9, 0), [(1600, _sy + _sh / 2), (1600, _gy), (_tx + 0.9 * _tw, _gy)], -0.8, "below"))   # 走專案目錄欄右側外（x=1600），不穿引擎 → 專案目錄的「寫」線
# w4v1q 否（不符）→ w4r：跳過 tools.just 兩列：從菱形右側出、沿 x=1290 下到 w4r 上方縫隙、左到 w4r 右側 0.8 再下進頂端
_sx, _sy, _sw, _sh = _A["w4v1q"]; _tx, _ty, _tw, _th = _A["w4r"]; _gy = F.rt["w4r"] - F.gap / 2
p16ccc.append(_edge("wf7", "w4v1q", "w4r", "否", (1, 0.5), (0.8, 0), [(1600, _sy + _sh / 2), (1600, _gy), (_tx + 0.8 * _tw, _gy)], -0.8, "below"))
foot(p16ccc, "p16ccc", F.y, T16D, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16ccc", "流程 v2：離線包（3′）apply sync 先驗後重裝", p16ccc))

exec
/usr/bin/bash -lc "sed -n '1450,1530p' disc_v1_a.py
sed -n '1900,1950p' disc_v1_a.py
sed -n '220,268p' disc_v1_c.py
sed -n '270,325p' disc_v1_c.py
sed -n '380,462p' disc_v1_c.py
sed -n '654,754p' disc_v1_c.py" in <scratchpad>
 succeeded in 0ms:
p3b.append(e("s2b_e", "s2a", "s2b", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s2c_e", "s2b", "s2c", "", (1, 0.5), (0, 0.5)))
# 第二列
d1c = d1x + W1["d1"] / 2
ERR_X = 30
p3b.append(v("p3_err", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", ERR, ERR_X, r2y, ERR_W, eh))
AX, AY = 40, Y
midy_err = AY + ROW1_BOT + 18
p3b.append(ew("p3_err_e", "d1", "p3_err", "是", (0.5, 1), (0.5, 0), [(AX + d1c, midy_err), (AX + ERR_X + ERR_W / 2, midy_err)], pos=-0.85))
d2x = ERR_X + ERR_W + 24
p3b.append(v("d2", "p3L2", RHOMBUS + "fontSize=12;", D2_T, d2x, r2c - d2h / 2, D2W, d2h))
g2x = d2x + D2W + 24
g2w = GP + W2["s3a"] + 16 + W2["s3b"] + 16 + W2["s3c"] + 16 + W2["s3d"] + 16 + W2["s3e"] + GP + 12
g2y = r2c - GT - GP3 - ih2 / 2
p3b.append(v("g3", "p3L2", GRP_T, "③ 主機 docker（每筆 pull／extract 記錄；不帶 --platform；先收完 vk-resolve 驗文法才動）", g2x, g2y, g2w, g2h))
ux = GP; s3x = {}
for pid, t in (("s3a", S3A), ("s3b", S3B), ("s3c", S3C), ("s3d", S3D), ("s3e", S3E)):
    s3x[pid] = ux
    p3b += vt(pid, "g3", L12, t, ux, GT + GP3 + (ih2 - h2[pid]) / 2, W2[pid], h2[pid], tagged=(pid in ("s3a", "s3c"))); ux += W2[pid] + 16
x = g2x + g2w + 24
p3b.append(v("s4", "p3L2", L12, S4, x, r2c - h2["s4"] / 2, W2["s4"], h2["s4"]))
s3bx_x = g2x + GP + W2["s3a"] + 16 + W2["s3b"] / 2 - S3BXW / 2                                       # ③ docker pull 失敗 → 紅終點（6-24）
p3b.append(v("s3bx", "p3L2", ELLIPSE(RED) + "fontSize=12;", S3BX, s3bx_x, okY, S3BXW, s3bxh))
p3b.append(e("s3bx_e", "s3b", "s3bx", "失敗", (0.5, 1), (0.5, 0), vert=True))
p3b.append(e("s3b_e", "s3a", "s3b", "無", (1, 0.5), (0, 0.5), vert="below"))
p3b.append(e("s3c_e", "s3b", "s3c", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s3d_e", "s3c", "s3d", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s3e_e", "s3d", "s3e", "", (1, 0.5), (0, 0.5)))
p3b.append(e("s4_e", "s3e", "s4", "", (1, 0.5), (0, 0.5)))
p3b.append(e("d2_e", "d2", "s3a", "是", (1, 0.5), (0, 0.5)))
# ③ inspect 本機已有 → 跳過 pull：從 s3a 頂端上到分組標題下方的空隙，右到 s3c 頂端下來（codex v1p3b #3）
byp_y = AY + g2y + GT + 6
s3a_cx = AX + g2x + s3x["s3a"] + W2["s3a"] / 2; s3c_cx = AX + g2x + s3x["s3c"] + W2["s3c"] / 2
p3b.append(ew("s3a_skip", "s3a", "s3c", "有 → 跳過 pull", (0.5, 0), (0.5, 0), [(s3a_cx, byp_y), (s3c_cx, byp_y)], lab="below", pos=0.0))
# ②c → d2：從 ②c 底邊下到列間，往左到 d2 上方，再下去；resolve 非 0 → 另一條出口到橙終點（不讀 stdout、不跑 docker／apply）
s2c_ax = AX + g1x + GP + W1["s2a"] + 16 + W1["s2b"] + 16 + W1["s2c"] / 2
d2_ax = AX + d2x + D2W / 2
midy = AY + ROW1_BOT + 40
p3b.append(ew("d2_in", "s2c", "d2", "resolve 0", (0.5, 1), (0.5, 0), [(s2c_ax, midy), (d2_ax, midy)], lab="side", pos=-0.9))
rx_x = 1560 - 30 - RXW                                                                                # 橙終點放第三列最右（④ 終點右邊）；線從 ②c 右下出、沿 x=1500 下來（避開 ④ 格）
p3b.append(v("p3_rx", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", RX_T, rx_x, okY, RXW, rxh))
p3b.append(ew("p3_rx_e", "s2c", "p3_rx", "非 0", (0.9, 1), (1, 0.5), [(AX + g1x + GP + W1["s2a"] + 16 + W1["s2b"] + 16 + W1["s2c"] * 0.9, midy - 10), (AX + 1545, midy - 10), (AX + 1545, AY + okY + rxh / 2)], lab="side", pos=-0.85))
p3b.append(v("p3_ok", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", OK_T, d2x + D2W / 2 - OKW / 2, okY, OKW, okh))
p3b.append(e("p3_ok_e", "d2", "p3_ok", "否", (0.5, 1), (0.5, 0), vert=True))
s4_cx = AX + x + W2["s4"] / 2
s4x_x0 = s3bx_x + S3BXW + 30; s4x_x1 = s4x_x0 + S4XW0 + 20; s4x_x2 = s4x_x1 + S4XW1 + 20
assert s4x_x2 + S4XW2 + 20 <= rx_x, (s4x_x2 + S4XW2, rx_x)
p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
    _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
    p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
# 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
s0c_x = 30 + W1["s0a"] + 16 + W1["s0b"] + 16; s1_x = s0c_x + W1["s0c"] + 16
s0x_cx = s0c_x + W1["s0c"] * 0.4; s1x_cx = s1_x + W1["s1"] * 0.6
p3b.append(v("s0x", "p3L2", ELLIPSE(RED) + "fontSize=12;", S0X, s0x_cx - S0XW / 2, 50 + (row0h - s0xh) / 2, S0XW, s0xh))
p3b.append(v("s1x", "p3L2", ELLIPSE(RED) + "fontSize=12;", S1X, s1x_cx - S1XW / 2, 50 + (row0h - s1xh) / 2, S1XW, s1xh))
p3b.append(e("s0x_e", "s0c", "s0x", "失敗", (0.4, 0), (0.5, 1), vert=True, pos=-0.5))
p3b.append(e("s1x_e", "s1", "s1x", "≠ 1", (0.6, 0), (0.5, 1), vert=True, pos=-0.5))
# 第 4 列：單段 update（不經 ②③④）：查 registry 只在這裡與 ②b（add／upgrade 未指定 @<tag> 且非 CI 模式）
p3b.append(v("p3_u5_l", "p3L2", LBL, "單段動詞（install／upgrade vendor_kit／update／dev／help）不經 ②③④、一次 docker run；以 update 為例（流程見 update 頁）", 30, r4y, 900, 28))
_ux = 30; _upos = {}
for _id, _t, _st in (("u5a", U5A, L12), ("u5b", U5B, ENG12), ("u5c", U5C, ELLIPSE(GREEN) + "fontSize=12;"), ("u5d", U5D, ELLIPSE(ORANGE) + "fontSize=12;")):
    _h = hve(_t, U5W[_id]) if "ellipse" in _st else hv(_t, U5W[_id])
    p3b.append(v(_id, "p3L2", _st, _t, _ux, u5y + (u5h - _h) / 2, U5W[_id], _h)); _upos[_id] = (_ux, _h); _ux += U5W[_id] + 20
p3b.append(e("u5b_e", "u5a", "u5b", "", (1, 0.5), (0, 0.5)))
p3b.append(e("u5c_e", "u5b", "u5c", "0", (1, 0.5), (0, 0.5), vert="below"))
_by = AY + u5y + u5h + 12; _bx0 = AX + _upos["u5b"][0] + U5W["u5b"] * 0.8; _bx1 = AX + _upos["u5d"][0] + U5W["u5d"] / 2
p3b.append(ew("u5d_e", "u5b", "u5d", "1／2", (0.8, 1), (0.5, 1), [(_bx0, _by), (_bx1, _by)], lab="below", pos=0.0))
p3b += tmp
Y += l2h + 20
Y = footer(p3b, "p3b", Y, ["grpbox", "rhomb", "v3act_s", "v3ok", "v3err_s", "v3launch", "v3eng", "v2code", "ruleb", "tblh", "v2tag", "notep", "conv"], "實線 = 執行順序；線上文字 = 條件／接續編號\n淺灰底容器 = ②③ 的分組（標題 = 該段做的事）",
 ["inspect", "createcp", "tmpdist", "token", "vkresolve", "fingerprint", "gitkeepline"])   # 白名單／uid 旗標已由規則框 p3_sh／p3_uf 逐字承載（頁高 ≤ 2400）；第 0 頁已有的詞不列
pages_v1_a.append(("v1p3b", "契約 v2：啟動器 ↔ 引擎契約④", p3b))

# ================= P3bb v1p3bb：契約④（2）規則框（第十六輪自 p3b 拆頁）=================
p3bb = head("p3bb", "契約④ 啟動器 ↔ 引擎（2）── 規則框（§3、§5：白名單、執行環境、docker run、環境變數、image 取得、接手、uid、相容）", 1200)
P3BB_NOTE = "<b>本頁無待拍板</b>\n本頁 = 契約④ 的規則框（自「契約④」頁拆出，頁高 ≤ 2400）；流程、vk-resolve/1 文法、kind 表、apply 通則、兩段編排與快路徑在「契約④」頁"
p3bb.append(vb("p3bb_pend", "1", NP_NOTE, P3BB_NOTE, 1260, 12, 340, hv(P3BB_NOTE, 340, pad=10))); Y = max(12 + hv(P3BB_NOTE, 340, pad=10) + 16, 96)
tmp2 = []; y = 50
p4.append(e("w_bl", "m_init", "f_bl", "基準版、metadata\n（含 [progress]）", rel("m_init", fmid("f_bl")), (0, 0.5), both=True))
p4.append(e("w_just", "m_shell", "f_just", "import 那一行", rel("m_shell", fmid("f_just")), (0, 0.5), both=True))
p4.append(e("w_di", "m_shell", "f_di", ".dockerignore\n四行", rel("m_shell", fmid("f_di")), (0, 0.5), both=True))
p4.append(e("w_shell", "m_shell", "f_shell", "薄殼五檔內容\n（首行／模板）", rel("m_shell", fmid("f_shell")), (0, 0.5), both=True))
p4.append(e("w_gen", "m_shell", "f_gen", "tools.just、\n.stamp 內容", rel("m_shell", fmid("f_gen")), (0, 0.5)))
p4.append(e("w_gk", "m_shell", "f_gk", "空檔", rel("m_shell", fmid("f_gk")), (0, 0.5)))
p4.append(e("w_tmpd", "m_prune", "f_tmpd", "殘留清單（刪）", rel("m_prune", fmid("f_tmpd")), (0, 0.5)))
# log 模組 → log/：從 log 模組底邊下到執行紀錄列中線（模組列下方、容器內無其他格），右穿容器進 log/ 左側
log_mid = LY + log_row_y + log_row_h - 8
pts = [(EX + 90, LY + LOG_Y + LOG_H), (EX + 90, log_mid), (PX, log_mid)]
p4.append(ew("w_log", "m_log", "f_log", "engine_* 事件（append 同一檔）", (0.5, 1), (0, round((log_row_h - 8) / log_row_h, 4)), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=EX + 400)))
CHAIN_N = "模組間箭頭只標傳什麼資料、不是固定執行順序：每個動詞只經過自己需要的模組（update 只 resolve＋schema；prune 只 resolve＋schema＋progress＋prune），順序見流程頁"   # codex r13 v1p4 #13
p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
# ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
# 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
MXX, RXX, TXX = 530, 552, 576
Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
pts = [(RXX, HB), (RXX, Y_R), (EX, Y_R)]
p4.append(ew("run_cli", "h4", "p4E", "動詞、參數、\n介面版旗標", (round((RXX - HX) / HW4, 4), 1), (0, round((Y_R - LY) / LH, 4)), pts[1:-1], lab="side", pos=pos_at(pts, 0, y=HB + 48)))
pts = [(EX, Y_T), (TXX, Y_T), (TXX, HB)]
p4.append(ew("ret_cli", "p4E", "h4", "結束碼、\nvk-resolve", (0, round((Y_T - LY) / LH, 4)), (round((TXX - HX) / HW4, 4), 1), pts[1:-1], lab="side", pos=pos_at(pts, 1, y=HB + 14)))
# registry 查詢由 resolve 模組發出：右出 → 上進下游 image 底邊（GHCR 在引擎正上方）
y_reg = LY + mid("m_res"); qx = 1215
y_reg2 = LY + R["m_res"][0] + R["m_res"][1] * 0.75; qx2 = 1245; qy2 = LY - 30; qx3 = GX + GW - 20
pts = [(EX + MX + MW, y_reg), (qx, y_reg), (qx, GY + GH - 20)]
p4.append(ew("q_reg", "m_res", "g_dist", "工具 tag／\nindex digest", (1, 0.5), (round((qx - (GX + 20)) / GIW, 4), 1), pts[1:-1], both=True, lab="side", pos=pos_at(pts, 1, y=y_reg - 60)))
pts = [(EX + MX + MW, y_reg2), (qx2, y_reg2), (qx2, qy2), (qx3, qy2), (qx3, GY + 50 + geh / 2), (GX + 20 + GIW, GY + 50 + geh / 2)]   # update／upgrade 也查引擎 image 的 tag（spec §1.2；r11）
p4.append(ew("q_reg_e", "m_res", "g_eng", "引擎 tag／index digest（update／upgrade）", (1, 0.75), (1, 0.5), pts[1:-1], both=True, lab="below", pos=pos_at(pts, 2, x=(qx2 + qx3) / 2)))
# 啟動器 → log/（launcher_* 事件；與引擎 append 同一檔）、config.toml → 啟動器（固定寫法的 keep 行 grep）：走頁面左緣與底緣，從專案框底邊進檔
log_x = PX + FX + FW * 0.65; cfg_x = PX + FX + 100
YB = LY + LH
LGX = HX + 20                                                                                        # 啟動器底邊左端（x=60）出 → 下到底緣 → 右到 log/ 底邊（主機分組在 x=70 起，線在其左）
pts = [(LGX, HB), (LGX, YB + 14), (log_x, YB + 14), (log_x, LY + P["f_log"] + next(h for q, y, h in pf if q == "f_log"))]
p4.append(ew("w_log_l", "h4", "f_log", "launcher_* 事件（launcher_start／launcher_exit 等；與引擎 append 同一檔；順序見 p3b）", (round((LGX - HX) / HW4, 4), 1), (0.65, 1), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=700)))   # 只標資料，順序歸流程頁（r11）
RXE = PX + PW + 8
for _fid, _bx, _dy, _hx, _lab, _lx in (("f_ver", RXE, 10, 0.42, "版本鎖定行（grep 引擎 ref）", 1300), ("f_vl", RXE + 12, 24, 0.34, "本機覆寫行（grep；優先）", 1000), ("f_cfg", RXE + 24, 38, 0.26, "固定寫法的 keep／days 行（grep）", 720), ("f_tmp", RXE + 36, 52, 0.18, "進度檔的目標引擎 ref（E(c) 接手時 grep）", 380)):   # 啟動器只讀（grep）四檔：檔越上面走越內側匯流排、越低的走廊、越右的入口 → 四線互不交叉（取代原底緣 w_cfg_l）
    _fy = LY + P[_fid] + 18; _cy = GY - _dy; _tx = HX + HW4 * _hx
    _pts = [(PX + FX + FW, _fy), (_bx, _fy), (_bx, _cy), (_tx, _cy), (_tx, GY)]
    p4.append(ew(f"g_{_fid}", _fid, "h4", _lab, (1, 0.5), (_hx, 0), _pts[1:-1], pos=pos_at(_pts, 2, x=_lx)))
Y = LY + LH + 56                                                                                       # 底緣兩條線（YB+14／YB+44）與其標籤在圖例之上（Claude r13 w_cfg_l）
c, Y = lgd("p4", 40, Y, ["v3img", "v4mod", "v4unit", "v4host", "v4hgrp", "v4egrp", "v4pgrp", "v2git", "v2no", "v2usr", "v2code", "v2tag", "v4other", "notep"], "實線 = 資料流（線上文字 = 傳什麼）\n雙箭頭 = 讀寫都有；黃橢圓 = 下游使用者", maxw=1300)
p4 += c
c, Y = terms2("p4", 40, Y + 34, [TERMS[k] for k in ["modunit", "configtoml", "traceid", "indexdigest", "tmp", "mount", "logevents", "flock"]])   # 8 模組、啟動器、執行紀錄等見第 0 頁
p4 += c
pages_v1_a.append(("v1p4", "架構圖 v2", p4))
_pts = [(_qx, _qy + _qh / 2), (30, _qy + _qh / 2), (30, _gy), (_zx + _zw / 2, _gy), (_zx + _zw / 2, _zy)]
_segs = [abs(b_[0] - a_[0]) + abs(b_[1] - a_[1]) for a_, b_ in zip(_pts, _pts[1:])]; _ly = (F.rt["q11b"] + F.rb["q11b"]) / 2
_pos = 2 * ((_segs[0] + (_ly - _pts[1][1])) / sum(_segs)) - 1
p9.append(_edge("qe12z", "q9y", "q11z", "續（2）：apply prune --dry-run（零刪除）", (0, 0.5), (0.5, 0), _pts[1:-1], _pos, True))
foot(p9, "p9", F.y, T9, {"note", "sub", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p9", "流程 v2：prune（1）resolve → 差集 → 刪", p9))

# ================= P9c：prune（2）apply 清暫存 → 刪進度檔 → 摘要 =================
p9c, F = newpage_c("流程 v2：prune（2）── apply prune：清暫存 → 刪進度檔 → 摘要（§1.2、§4.6）", N9, COLS_PR, gap=14)
b = F.band("bP2", "prune 第 2 段（承「prune（1）」頁）：docker run 引擎 apply prune [--dry-run]（flock → 重驗指紋 → --dry-run 只列出 → 建進度檔 → 清 .tmp.dist.* → 清殘留 .tmp.* → 每次刪除記成功／失敗 → 全部成功才刪進度檔）→ 0／1", v2=True)
b.box("q12z", L, 0, ENTRY, "來自「prune（1）」頁：四類資源已逐類刪、每個命令的成功／失敗已記下；或 --dry-run 只印了差集", 300)
b.box("q12", L, 1, W12, "docker run <引擎> apply prune [--dry-run]", 300)
b.box("q12ax", U, 2, O12, "逾時 → 1 + 6-26：確認無其他 vendor_kit 在跑後重試", 200)
b.box("q12a", E, 2, SUB, "apply prune：拿 flock 專案目錄（60 秒）", 340)
b.box("q12bx", U, 3, O12, "不同 → 1 + 6-12：請重跑", 200)
b.box("q12b", E, 3, SUB, "重驗指紋（與 vk-resolve 的 fingerprint 比）", 340)
b.box("q12dy", U, 4, G12, "是 → 0：只列出會清的暫存與殘留（零刪除；不建進度檔）", 200)
b.box("q12d", E, 4, D12, "--dry-run？", 200, ax="l")
b.box("q12j", E, 5, SUB, "否：建進度檔 .tmp.prune.<id>.toml（第一個寫入前；state=in-progress、done／pending）", 340)
b.box("q12jf", P, 5, F12, "＋.vendor_kit/.tmp.prune.<id>.toml（prune 自己的進度檔）", 330)
b.box("q12c", E, 6, SUB, "刪 trap 沒清到的殘留啟動器暫存 .tmp.dist.<id>/", 340)
b.box("q12cf", P, 6, F12, ".vendor_kit/.tmp.dist.<id>/（刪）", 330)
b.box("q12c2", E, 7, v2(SUB), "進度檔記結果：每個 .tmp.dist.* 的刪除成功／失敗各記一筆", 340)
b.box("q12c2f", P, 7, F12, ".vendor_kit/.tmp.prune.<id>.toml（done／failed 加一筆）", 330)
b.box("q12d2", E, 8, SUB, "刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列出）", 340)
b.box("q12df", P, 8, F12, ".vendor_kit/.tmp.<verb>.<id>.toml（殘留：刪；活躍：保留）", 330)
b.box("q12d3", E, 9, v2(SUB), "進度檔記結果：每個殘留 .tmp.<verb>.* 的刪除成功／失敗各記一筆", 340)
b.box("q12d3f", P, 9, F12, ".vendor_kit/.tmp.prune.<id>.toml（done／failed 加一筆）", 330)
b.box("q13x", U, 10, v2(R12), "否 → 1：摘要全列、失敗的標出；進度檔留著（下次可寫動詞先恢復：補做失敗的刪除）", 200)
b.box("q13", E, 10, v2(D12), "全部刪除成功？（含（1）頁四類資源）", 300, ax="l")
b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
b.D("qe17z", "q12z", "q12", al=True)
b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
b.H("qe19j", "q12j", "q12jf", "建"); b.D("qe18b", "q12j", "q12c"); b.H("qe19", "q12c", "q12cf", "刪")
b.D("qe18c2", "q12c", "q12c2"); b.H("qe19c2", "q12c2", "q12c2f", "寫"); b.D("qe18c", "q12c2", "q12d2"); b.H("qe19d", "q12d2", "q12df", "刪")
b.D("qe18d3", "q12d2", "q12d3"); b.H("qe19d3", "q12d3", "q12d3f", "寫"); b.D("qe18k", "q12d3", "q13", al=True)
b.H("qe21", "q13", "q13x", "否"); b.D("qe20", "q13", "q12k", "是", al=True); b.H("qe19k", "q12k", "q12kf", "刪"); b.DL("qe22", "q12k", "q14")
b.close()
foot(p9c, "p9c", F.y, T9B, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p9c", "流程 v2：prune（2）apply 清暫存", p9c))

# ================= P10：update =================
COLS_UP = [("下游使用者", 40, 220), ("啟動器（主機 sh）", 280, 280), ("引擎容器", 580, 400), ("registry（GHCR）", 1000, 290), ("專案目錄", 1310, 280)]
RG = "registry（GHCR）"
T10 = [
 ("update", "只查 registry 有沒有新版、不動任何檔（唯讀，不受CI 模式限制）；單段 docker run（不經 docker create/cp）；[<repo>] 省略 = 全部工具 + vendor_kit 自身；--exit-code：有新版回 2（給 CI 用）"),
 ("registry 憑證（Q11）", "VENDOR_KIT_REGISTRY_TOKEN（+ _USER）或 VENDOR_KIT_REGISTRY_TOKEN_FILE（啟動器 -v <file>:/run/vk-token:ro 掛入；兩者同設 → 1）；只在 update 單段及 upgrade 的 resolve 以 -e 傳入引擎；不寫 log／檔、不傳給工具、dry-run 不印；不掛 ~/.docker/config.json"),
 ("查詢失敗分類", "每個目標各自判定：認證（錯 token／無權限）、網路（連不上、逾時）、回應（registry 回錯誤碼）、解析（SemVer／分頁解析失敗）；任一類都記該目標 1 並繼續查下一個目標，最後彙總"),
 ("6-3", "無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）"),
 ("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」；舊薄殼對未知碼原樣傳出、不吞"),
 ("6-15（末行固定）", "update 最後一行永遠印「套用：just vendor_kit upgrade」，含未完成交易（6-33）那條出口"),
 ("6-33（未完成交易）", "唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；sync／update 結束 1、help 仍 0"),
]   # ≤ 8 條（6-3／6-15／6-33 各自成條，不再列 6-N 總條）
N10 = "已定（Q11、Q27、v2.6-5、v2.7-8、v2.8-7、v2.15-16、interface_spec §1.2 update）：無憑證時不支援需認證的版本列舉，該工具直接記失敗 1 + 6-3（不進 SemVer 解析；需人處理 → 橙），其他工具照查再彙總；查詢失敗依認證／網路／回應／解析分類，各記該目標 1 並繼續；_TOKEN 與 _TOKEN_FILE 同設 → 1；token 只在 update 單段及 upgrade 的 resolve 以 -e 傳（TOKEN_FILE 用 -v 掛）；update 唯讀、不受CI 模式限制；有新版只在 --exit-code 時回 2；末行固定印 6-15（含 6-33 出口）。"
p10, F = newpage_c("流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）", N10, COLS_UP, gap=16)
b = F.band("bU", "update [<repo>] [--exit-code]：建執行紀錄 → launcher_start → 憑證互斥檢查 → 單段引擎容器（偵測未完成交易 → 6-33 → 1）查 registry（公開／有 token → 查；無憑證 → 記 6-3；查詢失敗分類 → 記 1）→ 每個目標彙總（Q27）→ 末行 6-15 → 0／1／2", v2=True)
b.box("u0", U, 0, G12, "just vendor_kit update [<repo>] [--exit-code]", 220)
b.box("u0l", L, 0, v2(W12), LST1.replace("<verb>", "update"), 280)
b.box("u0x", U, 1, v2(R12), LSX, 220)
b.box("u0l2", L, 1, v2(W12), LST2, 280)
b.box("u1x", U, 2, O12, "是 → 1：只能擇一（改設其中一個）", 220)
b.box("u1q", L, 2, v2(D12), "_TOKEN 與 _TOKEN_FILE 同時設？", 280)
b.box("u1", L, 3, W12, "否：組 docker run 引數：-e VENDOR_KIT_REGISTRY_TOKEN／_USER，或 -v <TOKEN_FILE>:/run/vk-token:ro（只在 update 單段及 upgrade 的 resolve 傳）", 280)
b.box("u1r", L, 4, W12, "docker run <引擎> update（單段、不經 create/cp）", 280)
b.box("u2", E, 4, SUB, "update（唯讀；不受CI 模式限制）：讀 version.toml 現版", 400)
b.box("u2f", P, 4, F12, "version.toml（只讀：引擎 ref、[tools]）", 280)
b.box("u3x", U, 5, O12, "是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔；末行仍印 6-15）", 220)
b.box("u3", E, 5, D12, "有未完成交易（.tmp.<verb>.*.toml／[progress]）？", 400, ax="l")
b.box("u4l", E, 6, LBL, "否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）", 400, 24, ax="l", minh=24)
b.box("u5", E, 7, D12, "registry 不要求認證（公開）？", 300, ax=58)
b.box("u5g", RG, 7, v2(SUB), "是：GET /v2/<name>/tags/list（分頁）", 130, ax="r")
b.box("u6", E, 9, D12, "有 VENDOR_KIT_REGISTRY_TOKEN／_TOKEN_FILE？", 340, ax=12)
b.box("u6g", RG, 9, v2(SUB), "是：WWW-Authenticate 換 token → tags/list", 130, ax="l")
b.box("u6r", P, 9, RULE, "已定（Q11）：無憑證時不支援需認證的版本列舉；token 只在 update 單段及 upgrade 的 resolve 以 -e 傳，不寫 log、不傳給工具；GHCR 已測試，其他 registry 依標準協定可用但未驗證", 280)
b.box("u7q", E, 10, v2(D12), "查詢成功？", 200, ax=108)
b.box("u7c", E, 11, v2(SUB), "否：查詢失敗：分類原因（認證／網路／回應／解析）", 200, ax=60)
b.box("u8a", E, 11, SUB, "是：取 SemVer 最大正式版（排除預發行）", 150, ax="r")
b.box("u7f", E, 12, v2(SUB), "該目標記 1（無憑證 → 6-3，不查；否則附分類）→ 繼續下一目標", 220, ax=12)
b.box("u8b", E, 12, SUB, "與現版比較 → 記「現版 → 最新」", 150, ax="r")
b.box("u8q", E, 13, D12, "還有下一個目標？", 300, ax=58)
b.box("u9", E, 14, SUB, "否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的分類與 6-3）；訊息全列", 400)
b.box("u10", E, 15, SUB, "末行固定印 6-15：「套用：just vendor_kit upgrade」", 400)
b.box("u11x", U, 16, O12, "是 → 1：查詢失敗（6-3：設 token 或指定 <repo>@<tag>；其他分類印原因；即使另有新版）", 220)
b.box("u11", E, 16, D12, "任一目標查詢失敗（1）？", 300, ax="l")
b.box("u12y", U, 17, O12, "是 → 2：有新版（給 CI 用）", 220)
b.box("u12", E, 17, D12, "有新版且 --exit-code？", 300, ax="l")
b.box("u13", U, 18, G12, "否 → 0：已列出（有新版也 0）", 220)
b.H("ue0", "u0", "u0l"); b.D("ue0l", "u0l", "u0l2"); b.H("ue0lx", "u0l2", "u0x"); b.D("ue0l2", "u0l2", "u1q", al=True); b.H("ue0x", "u1q", "u1x", "是"); b.D("ue0q", "u1q", "u1", "否", al=True); b.D("ue0b", "u1", "u1r"); b.H("ue1", "u1r", "u2"); b.H("ue2", "u2", "u2f", "讀"); b.D("ue3", "u2", "u3", al=True)
b.H("ue4", "u3", "u3x", "是"); b.D("ue5", "u3", "u4l", al=True); b.D("ue6", "u4l", "u5", al=True)
b.H("ue7", "u5", "u5g", "是"); b.D("ue8", "u5", "u6", "否", al=True); b.H("ue9", "u6", "u6g", "是"); b.D("ue10", "u6", "u7f", "否", sx=0.1, tx=0.1, al=True)
b.DL("ue11", "u5g", "u7q"); b.DL("ue12", "u6g", "u7q")
b.D("ue13q", "u7q", "u7c", "否", al=True); b.RD("ue13y", "u7q", "u8a", "是"); b.D("ue13c", "u7c", "u7f", al=True); b.D("ue13f", "u7f", "u8q", al=True)
b.D("ue13b", "u8a", "u8b"); b.D("ue14", "u8b", "u8q", al=True)
b.LL("ue14y", "u8q", "u5", "是：下一個目標", busx=562); b.D("ue14n", "u8q", "u9", "否", al=True)   # u6／u7 左緣 x=592：回圈線（x=562）離框 30（r11）
b.D("ue15", "u9", "u10"); b.D("ue16", "u10", "u11", al=True)
b.H("ue17", "u11", "u11x", "是"); b.D("ue18", "u11", "u12", "否", al=True); b.H("ue19", "u12", "u12y", "是"); b.DL("ue20", "u12", "u13", "否")
b.close()
foot(p10, "p10", F.y, T10, {"note", "rule", "sub", "hdr", "v2"})
pages_v1_c.append(("v1p10", "流程 v2：update", p10))

# ================= P11：初始檔五態 =================
COLS_ST = [("deleted", 40, 290), ("managed", 350, 290), ("declined", 660, 290), ("appended", 970, 290), ("unmanaged", 1280, 290)]
# ================= P12：交易與進度檔 =================
COLS_TX = [("下游使用者", 40, 240), ("引擎容器（apply 段）", 300, 480), ("專案目錄", 800, 380), ("規則／說明", 1200, 390)]
EA, PA, XA = "引擎容器（apply 段）", "專案目錄", "規則／說明"
T12 = [
 ("install／升引擎的進度檔", "第一次 install 也建 .tmp.install.<id>.toml（v2.13 P5，無例外）：兼「不留半成品」的清除清單，失敗依它移除已寫的檔（log/ 保留）、成功後刪；修復型同；升引擎建 .tmp.upgrade.<id>.toml（另記舊引擎 ref、目標 ref、計畫 image ID）"),
 ("恢復（三型）", "可寫動詞開始前偵測到未完成交易 → 先恢復再繼續本次（prune 例外：只列出、不恢復）：一般（add／remove／upgrade <repo>／undev／uninstall／dev）依進度檔 done 略過、pending 補做、consents 不再問；升引擎 = 重跑 upgrade vendor_kit；第一次 install = 依進度檔（清除清單）移除半成品、log/ 保留；失敗 → 1 印 6-27「未恢復：<檔名>」逐檔列出、進度檔留著"),
 T_FP,
 ("交易／apply", "一次會寫檔的動詞執行 = 一筆交易：兩段動詞的 apply 拿 flock → 重驗指紋 → dry-run 分支 → 建進度檔（第一個寫入前）→ 逐步寫入 → 最後一步刪進度檔；單段可寫動詞（install／dev／升引擎）無 resolve／apply、無指紋重驗，從「建進度檔」開始；回 3 一律零寫入；工具層回 1 時 version.toml 不動"),
 ("原子替換／暫存", "每個寫入先寫到暫存（合併也在暫存完成），確認沒問題再逐檔一次換上（rename）；中斷只會留下「已換上」與「未換上」兩種檔，不留半寫的檔"),
 ("規格硬性順序", "只有兩條：gen/tools.just 最後寫、且與 cache 同一 apply 內原子替換；version.toml（版本鎖定行）最後寫（工具層回 1 時不動）；其餘各動詞自訂"),
 T_MSG,
]
N12 = "已定（v2.5-3、v2.6-9、v2.7-7、v2.13 P5、v2.15-5／-10、interface_spec §0、§4.3、§4.6）：apply 順序 = flock → 重驗指紋 → dry-run 分支 → 建進度檔（第一個寫入前）→ 寫入 → 最後刪進度檔；單段可寫動詞（install／dev／升引擎）不畫成 resolve→apply；中斷 → 1 明列已完成／未完成；下次可寫動詞先恢復（三型）、唯讀動詞只提示 6-33；prune 特例只列出；dev 也建 .tmp.dev.<id>.toml。"
p12, F = newpage_c("狀態機 v2：交易與進度檔（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）", N12, COLS_TX, gap=12)
b = F.band("bT1", "交易生命週期：兩段動詞的 apply 段（拿鎖 → 重驗指紋 → dry-run 分支）→ 建進度檔 → 逐步寫入（每步 ① 寫暫存 ② 原子替換 ③ 進度檔 done）→ 刪進度檔；單段可寫動詞從「建進度檔」進入；中斷 → 1、進度檔留著", v2=True)
b.box("t0", U, 0, ENTRY, "來自兩段動詞頁：resolve → 啟動器 docker 之後，apply <verb>", 240)
b.box("t1", EA, 0, SUB, "拿 flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 跳過）", 480)
b.box("t1i", XA, 0, INV, "不變量：回 3 一律零寫入（無任何例外）；工具層回 1 時 version.toml 不動；進度檔在第一個寫入前建、最後一步刪；never fail silently", 390)
b.box("t1x", PA, 0, v2(O12), "逾時 → 1 + 6-26：確認無其他 vendor_kit 在跑後重試（零寫入）", 300)
b.box("t2x", U, 1, v2(O12), "指紋不同 → 1 + 6-12：請重跑（零寫入）", 240)
b.box("t2", EA, 1, SUB, "重驗指紋（與 /dist/vk-resolve 的 fingerprint 比）", 480)
b.box("t3y", U, 2, G12, "是 → 0：唯讀預覽；不建進度檔（CI 例外見右）", 240)
b.box("t3", EA, 2, D12, "--dry-run？", 200, ax="l")
b.box("t3n", XA, 2, RULE, "已定：--dry-run = 唯讀預覽（本機一律 0）；CI 模式且需改進 git 的檔時回 1 印清單（契約⑤ check.sh ③）；不建進度檔、不寫任何檔", 390)
b.box("t0b", U, 3, ENTRY, "來自 install／dev／升引擎頁（單段可寫動詞）：第一個寫入前", 240)
b.box("t4", EA, 3, SUB, "否：建進度檔（第一個寫入前）：state=in-progress、verb、id、started、targets、done[]／pending[]、consents", 480)
b.files("t4f", PA, 3, "進度檔位置（依動詞）", ["add／upgrade <repo>：metadata [progress]", "remove／uninstall／undev／prune／dev：.tmp.<verb>.<id>.toml（dev 另記本機覆寫行、symlink 目標、印記第一行）", "install：.tmp.install.<id>.toml（第一次 = 清除清單）", "升引擎：.tmp.upgrade.<id>.toml（改第一行前建、新引擎刪）"], 380)
b.box("t4n", XA, 3, RULE, "已定（v2.13 P5、v2.15-5／-10）：單段可寫動詞 install／dev／升引擎沒有 resolve→apply、不重驗指紋，直接從本格開始；第一次 install 的進度檔同時是「不留半成品」的清除清單（log/ 保留）；remove／uninstall 會刪 metadata、undev／prune／dev 沒有工具 metadata → 放 .vendor_kit/.tmp.*（自有 .gitignore 擋）；<id> = 本次 trace_id", 390)
b.box("t5", EA, 4, SUB, "逐步寫入 ①：寫暫存檔（合併也在暫存完成；詢問取得的同意先記進 consents）", 480)
b.box("t5af", PA, 4, F12, "暫存檔（目標檔旁；未換上前目標檔不動）", 380)
b.box("t5n", XA, 4, NOTE, "每一步都是 ①②③ 三個可獨立失敗的動作；規格只硬性要求：gen/tools.just 最後寫、與 cache 同一 apply 內原子替換；version.toml 最後寫；其餘順序各動詞頁自訂", 390)
b.box("t5b", EA, 5, SUB, "逐步寫入 ②：原子替換（rename 暫存檔 → 目標檔；一檔一次換上）", 480)
b.box("t5bf", PA, 5, F12, "目標檔（換上；中斷只會留下「已換上」「未換上」兩種）", 380)
b.box("t5c", EA, 6, SUB, "逐步寫入 ③：更新進度檔 done += 步驟（pending 移出）", 480)
b.box("t5f", PA, 6, F12, "進度檔 done[]／pending[] 每步更新", 380)
b.box("t6", EA, 7, D12, "這一步中斷？（寫入失敗／Ctrl-C／斷電）", 340, ax="l")
b.box("t6q", PA, 7, v2(D12), "是：第一次 install？", 200, ax="l")
b.box("t6xb", XA, 7, v2(R12), "否 → 1：明列已完成／未完成、進度檔留著（下次可寫動詞先恢復）", 390)
b.box("t6xa", PA, 8, v2(R12), "是 → 1：依進度檔（清除清單）移除已寫的檔、不留半成品（log/ 保留）", 300)
b.box("t5q", EA, 8, D12, "否：還有步驟？", 200, ax=10)
b.box("t7", EA, 9, SUB, "否：最後一步刪進度檔（uninstall：在根 justfile 那行之後才刪）", 300, ax="l")
b.box("t7f", PA, 9, F12, "進度檔刪除 = 交易完成（.tmp.<verb>.<id>.toml 刪／[progress] 移除）", 380)
b.box("t8c", U, 10, O12, "是 → 2：有合併衝突（留標記；解完重跑）", 240)
b.box("t7q", EA, 10, D12, "本次有合併衝突？", 260, ax="l")
b.box("t8", U, 11, G12, "否 → 0：印摘要", 240)
b.H("te0", "t0", "t1"); b.H("te1x", "t1", "t1x", "逾時"); b.D("te1", "t1", "t2"); b.H("te2x", "t2", "t2x", "≠"); b.D("te2", "t2", "t3", al=True); b.H("te3", "t3", "t3y", "是")
b.D("te4", "t3", "t4", "否", al=True); b.H("te0b", "t0b", "t4"); b.H("te5", "t4", "t4f", "建"); b.D("te6", "t4", "t5"); b.H("te7a", "t5", "t5af", "寫")
b.D("te6b", "t5", "t5b"); b.H("te7b", "t5b", "t5bf", "換"); b.D("te6c", "t5b", "t5c"); b.H("te7", "t5c", "t5f", "寫")
b.D("te8", "t5c", "t6", al=True); b.H("te9", "t6", "t6q", "是"); b.H("te9b", "t6q", "t6xb", "否"); b.D("te9a", "t6q", "t6xa", al=True); b.D("te8q", "t6", "t5q", "否", al=True); b.LL("te8y", "t5q", "t5", "是：回 ①", busx=290); b.D("te10", "t5q", "t7", "否", al=True)
b.H("te11", "t7", "t7f", "刪"); b.D("te12", "t7", "t7q", al=True); b.H("te12c", "t7q", "t8c", "是"); b.DL("te13", "t7q", "t8", "否")
b.close()   # flock 逾時 t1x 放專案目錄欄同列（H 線）、指紋不同 t2x 放下游使用者欄（兩橙終點各一事；codex r13 N2）
b = F.band("bT2", "中斷後的下一次執行（任何動詞開始前先偵測未完成交易）：可寫動詞先恢復再繼續；唯讀動詞只提示重跑原動詞；prune 特例只列出", v2=True)
b.box("r0", U, 0, G12, "打任何 vendor_kit 動詞", 240)
b.box("r1", EA, 0, SUB, "偵測未完成交易：.vendor_kit/.tmp.<verb>.*.toml（含 .tmp.install.*、.tmp.dev.*、.tmp.upgrade.*）或任一 metadata [progress] state=in-progress", 480)
b.box("r1f", PA, 0, F12, "讀進度檔（verb、id、targets、done／pending、consents）", 380)
b.box("r2n", U, 1, G12, "否 → 正常執行本次動詞", 240)
b.box("r2", EA, 1, D12, "有未完成交易？", 220, ax=90)
b.box("r2px", U, 3, ENTRY, "是 → 續「prune（1）」頁：只列出活躍進度檔、印 6-33（不刪、不恢復）", 240)
b.box("r2p", EA, 3, D12, "本動詞是 prune？", 220, ax=90)
b.box("r2pn", XA, 3, RULE, "已定（v2.7-7）：prune 遇活躍進度檔不擋、不恢復、不刪；只列出提示重跑原動詞；差集與 apply prune 照做", 390)
b.box("r2hy", U, 4, G12, "是（help）→ 0：印 6-33 後照常印說明（不受影響）", 240)
b.box("r2h", EA, 4, D12, "否：本動詞是 help？", 260, ax=70)
b.box("r3x", U, 5, O12, "否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）", 240)
b.box("r3", EA, 5, D12, "否：本動詞可寫？", 220, ax=90)
b.box("r3n", XA, 5, RULE, "已定（v2.6-9、v2.10-6、v2.15-5）：可寫動詞 = install／add／remove／upgrade（含升引擎）／dev／undev／uninstall → 先恢復再繼續（prune 例外：只列出，見上）；唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復：sync／update 印 6-33 結束 1；help 印 6-33 仍 0", 390)
b.box("r4", EA, 6, SUB, "是：恢復（依進度檔類型三型之一，見右）", 480)
b.box("r4f", PA, 6, F12, "補做 pending 的寫入（暫存 → 原子替換）／清除清單內的半成品", 380)
b.box("r4n", XA, 6, RULE, "恢復三型：一般可寫動詞 → 依進度檔 done 略過、pending 補做、consents 不再問；升引擎（.tmp.upgrade.*）→ 重跑 upgrade vendor_kit；第一次 install（.tmp.install.*）→ 依清除清單移除半成品、log/ 保留", 390)
b.box("r5x", U, 7, R12, "否 → 1 + 6-27「未恢復：<檔名>」逐檔列出；進度檔留著", 240)
b.box("r5", EA, 7, D12, "恢復成功？", 220, ax="l")
b.box("r6", EA, 8, SUB, "是：刪進度檔 → 繼續本次動詞（resolve 會重算指紋）", 480)
b.box("r6f", PA, 8, F12, "進度檔刪除", 380)
b.box("r7", U, 9, G12, "→ 繼續本次動詞", 240)
b.H("re0", "r0", "r1"); b.H("re1", "r1", "r1f", "讀"); b.D("re2", "r1", "r2", al=True); b.H("re3", "r2", "r2n", "否")
b.D("re4", "r2", "r2p", "是", al=True); b.H("re4p", "r2p", "r2px", "是"); b.D("re4n", "r2p", "r2h", al=True)
b.H("re4h", "r2h", "r2hy", "是"); b.D("re4hn", "r2h", "r3", "否", al=True)
b.H("re5", "r3", "r3x", "否"); b.D("re6", "r3", "r4", "是", al=True); b.H("re7", "r4", "r4f", "寫")
b.D("re8", "r4", "r5", al=True); b.H("re9", "r5", "r5x", "否"); b.D("re10", "r5", "r6", "是", al=True); b.H("re11", "r6", "r6f", "刪"); b.DL("re12", "r6", "r7")
b.close()
foot(p12, "p12", F.y, [T12[3], T12[5], T12[0], T12[4], T12[1], T12[2], T12[6]], {"note", "rule", "inv", "sub", "hdr", "entry", "v2"}, conv=False)   # 順序讓兩欄等高（頁高 ≤ 2400）
pages_v1_c.append(("v1p12", "狀態機 v2：交易與進度檔", p12))

# ================= P13：相容性矩陣 =================
# ================= P16：離線包（1）bootstrap.sh --local =================
COLS_OF = [("下游使用者（離線機）", 40, 230), ("bootstrap.sh（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("引擎容器", 970, 320), ("專案目錄", 1310, 280)]
SH = "bootstrap.sh（主機 sh）"; UO = "下游使用者（離線機）"
COLS_OF2 = [("下游使用者（離線機）", 40, 230), ("啟動器（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("引擎容器", 970, 320), ("專案目錄", 1310, 280)]
LA = "啟動器（主機 sh）"
T16 = [
 ("離線包（#27、Q26）", "Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援"),
 ("bootstrap.sh --local（契約入口）", "離線接入的契約入口 = bootstrap.sh --local <引擎 tar>（interface_spec §1.2）：只涉及引擎（docker load → install）；-t <repo> 走 registry、需網路，離線機不帶；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做、在建執行紀錄之前；值的判別依序互斥（B1，v3.5）：以 .tar 結尾 → 檔案（必須存在）→ load + 讀 .digest；否則含 / 且存在同名檔 → 1 + 6-37；否則 → image tag（只 inspect image ID；含 / 但無同名檔的完整 ref 也是 tag 形）"),
 ("add --local 只收 tar（v2.10-3）", "add --local <值> 只接受存在的 .tar 檔（新工具沒有既有 digest 可用；tag 形只對 bootstrap.sh --local 有意義）；不是存在的 .tar → 1 + 6-24 add --local 分句「add --local 只接受存在的 .tar 檔：<v>」；§1.1 選項表的 tag 形只適用 bootstrap.sh"),
 ("工具 tar（來源，v2.8-5）", "離線接工具要另備工具 tar：由下游 repo 自己提供（docker save 的 <repo>-dist image + 同名 .tar.digest 旁檔，一行 sha256:<hex64> = 該工具的正式 index digest），不在 vendor_kit 離線包內；下游使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add <repo> --local <工具 tar>"),
 ("local_bootstrap.sh（便利包裝，非契約）", "離線包內附的可選腳本：docker version --format '{{.Server.Arch}}' 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local <tar> \"$@\"；不是契約入口、不另定介面（v2.7-1）"),
 (".digest 旁檔", "<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1 + 6-24 主機錯誤分類）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id"),
 ("image ID 記錄", "docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format '{{.Id}}' 取 image ID：引擎的本機覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）"),
 ("baseline/.gitkeep", "VK 自產的進 git 空檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；install 建、uninstall 刪、hash 固定為空檔（§4.0；v2.15-14）；工具的 metadata 由 add 才建（baseline/<repo>/.vendor_kit.toml 兼作該工具目錄的佔位）"),
 ("離線可用（Q26）", "啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"),
 ("sync 快路徑（Q22）／--verify（F5）", "sync（無參數）啟動器只用 grep 比對 gen/.stamp 第一行 == version.toml 引擎 ref、gen/<repo>.stamp 第一行 == 鎖定 digest、每個 cache/<repo>/ 存在（目錄或 symlink）、tools.just 存在、無 .tmp.*、非 CI 模式 → 全相符不起容器 0；有差才起引擎；sync --verify 或 CI 模式或版本變動那次 → 先驗既有 cache（每檔 sha256），不符才重裝一次，再驗仍不符 → 失敗"),
 T_MSG,
]
N16 = "已定（Q26、v2.6-1、v2.7-1／-2、v2.8-4／-5、v2.13 P4、v2.15-2／-14／-17、v2.16-4、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 非契約）；先驗 git／just 再建執行紀錄；--local 依序判別（.tar 結尾 → 檔案；否則含 / 且有同名檔 → 6-37；否則 tag）；最低介面版檢查在起容器之前（斷網也回 3）；tar 附同名 .digest；install 第一個寫入前建 .tmp.install；version.toml 寫正式 ref@digest；離線 upgrade 不支援。"
COLS_OF1 = [("下游使用者（離線機）", 40, 230), ("bootstrap.sh（主機 sh）", 290, 400), ("docker daemon", 710, 240), ("bootstrap.sh（tag 形分支）", 970, 320), ("專案目錄", 1310, 280)]   # 本頁無引擎容器：第 4 欄給 tag 形分支（同一個 bootstrap.sh）
SH2 = "bootstrap.sh（tag 形分支）"
p16, F = newpage_c("流程 v2：離線包（1）── bootstrap.sh --local → 判別值 → load → image ID → 介面版（#27、Q26）", N16, COLS_OF1, gap=14)
b = F.band("bO1", "離線接入（1）只涉及引擎：bootstrap.sh --local <引擎 tar> → 前置檢查（git／just）→ 執行紀錄 → 判別值（.tar → 檔案；含 / 且有同名檔 → 6-37；否則 tag）→ load + .digest（tag 形只 inspect）→ image ID → LABEL 最低介面版 → 續（1′）", v2=True)
b.box("o0", UO, 0, G12, "有網路的機器下載離線包 vendor_kit-vN-local.tar.gz → 帶到離線機", 230)
b.box("o1", UO, 1, W12, "解開（SHA256SUMS 驗）：bootstrap.sh、各平台引擎 tar + .digest、local_bootstrap.sh；不含工具 tar", 230)
b.box("o1w", UO, 2, LBL, "【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：", 500, 24, ax="l", minh=24)
b.box("o1a", UO, 3, W12, "docker version 偵測 daemon 架構（.Server.Arch）", 230)
b.box("o1b", UO, 4, W12, "挑該平台的引擎 tar（vendor_kit-vN-<arch>.tar）", 230)
b.box("o1c", UO, 5, W12, "exec ./bootstrap.sh --local <tar> \"$@\"", 230)
b.box("o2", UO, 6, W12, "sh bootstrap.sh --local <引擎 tar> [-y]（契約入口；-t <repo> 走 registry 需網路，離線機不帶）", 230)
b.box("o5x", UO, 7, O12, "否 → 1 + 6-16：請先 git init（執行紀錄尚未建）", 230)
b.box("o5", SH, 7, D12, "在 git repo 內？", 300, ax="l")
b.box("o6x", UO, 8, O12, "否 → 1 + 6-23：請裝 release 版 just（執行紀錄尚未建）", 230)
b.box("o6", SH, 8, D12, "just ≥ 1.33.0？", 300, ax="l")
b.box("o2s", SH, 9, v2(W12), "是：建執行紀錄 log/bootstrap/<ts>-<id8>.jsonl", 400)
b.box("o2x", UO, 10, v2(R12), LSX, 230)
b.box("o2s2", SH, 10, v2(W12), LST2, 400)
b.box("o3", SH, 11, v2(D12), "--local 值以 .tar 結尾？", 300, ax="l")
b.box("o3n", P, 11, v2(RULE), "已定（B1 依序互斥；v3.5 #164、v2.16-4）：以 .tar 結尾 → 檔案路徑（必須存在）→ docker load；否則含 / 且存在同名檔 → 1 + 6-37；否則 → image tag（不 load、只 inspect，本機無 → 1；含 / 但無同名檔的完整 ref 也是 tag 形）；前置檢查（git／just）不分型別一律先做、在建執行紀錄之前", 280)
b.box("o3bx", UO, 12, v2(O12), "否 → 1：檔案路徑必須存在（請檢查路徑）", 230)
b.box("o3b", SH, 12, D12, "是：該路徑的檔案存在？", 300, ax="l")
b.box("o3c", SH2, 12, v2(D12), "否：值含 / 且存在同名檔？", 300, ax="l")
b.box("o3cx", P, 12, v2(O12), "是 → 1 + 6-37：--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。", 280)
b.box("o4x", UO, 13, R12, "否 → 1 + 6-24（主機錯誤）：同名 .tar.digest 旁檔缺", 230)
b.box("o4", SH, 13, D12, "是：同名 .tar.digest 存在？", 300, ax="l")
b.box("o3t", SH2, 13, v2(W12), "否 → tag 形：不 load、不讀 .digest", 300)
b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
b.box("o7cx", UO, 17, v2(O12), "否 → 3 + 6-18：零寫入（斷網也回 3；請以較新的離線包重建）", 230)
b.box("o7c", SH, 17, v2(D12), "inspect LABEL ….protocol：image 的介面版 ≥ 薄殼最低介面版？（不起容器、不上網）", 400, ax="l")
b.box("o7z", SH, 18, ENTRY, "是 → 續「離線包（1′）」頁：docker run 本機 image install → version.local.toml", 400)
b.D("oe0", "o0", "o1"); b.D("oe1", "o1", "o1w", al=True); b.D("oe1a", "o1w", "o1a", al=True); b.D("oe1b", "o1a", "o1b"); b.D("oe1c", "o1b", "o1c"); b.D("oe1w", "o1c", "o2")
b.H("oe6x", "o5", "o5x", "否"); b.D("oe6b", "o5", "o6", "是", al=True); b.H("oe6bx", "o6", "o6x", "否"); b.D("oe6c", "o6", "o2s", "是", al=True); b.D("oe2s", "o2s", "o2s2"); b.H("oe2x", "o2s2", "o2x"); b.D("oe2l", "o2s2", "o3", al=True)
b.RD("oe3c", "o3", "o3c", "否"); b.D("oe3b", "o3", "o3b", "是", al=True); b.H("oe3bx", "o3b", "o3bx", "否")
b.H("oe3cx", "o3c", "o3cx", "是"); b.D("oe3t", "o3c", "o3t", "否", al=True); b.D("oe3ti", "o3t", "o3ti", al=True); b.H("oe3tx", "o3ti", "o3tx", "否")
b.D("oe4", "o3b", "o4", "是", al=True); b.H("oe5", "o4", "o4x", "否"); b.D("oe7", "o4", "o6c", "是", al=True)
b.H("oe8", "o6c", "o6d", "載"); b.D("oe9", "o6c", "o7a"); b.D("oe9b", "o7a", "o7b", al=True); b.H("oe9d", "o7b", "o7bd")
_A = geo(b); _tx, _ty, _tw, _th = _A["o3ti"]; _bx, _by, _bw, _bh = _A["o7b"]; _gy = _by - F.gap / 2   # tag 形匯入：從 o3ti 底端下到 o7b 上方縫隙、左到 o7b 右側 0.9 進頂端（縫隙內無其他格；不穿「載」線）
b.P("oe3tj", "o3ti", "o7b", "是：tag 形（跳過 load／.digest）", (0.5, 1), (0.9, 0), [(_tx + _tw / 2, _gy), (_bx + 0.9 * _bw, _gy)], pos=-0.7, vert=True)
b.D("oe9c", "o7b", "o7c", al=True); b.H("oe9cx", "o7c", "o7cx", "否"); b.D("oe10z", "o7c", "o7z", "是", al=True)
b.close()
_A = F.abs; _sx, _sy, _sw, _sh = _A["o2"]; _tx, _ty, _tw, _th = _A["o5"]; _gy = F.rt["o5"] - F.gap / 2   # o2 右側出、沿欄間 x=275 下到 o5 上方縫隙、右到 o5 頂點進（不與 o5 → o5x「否」線同段；r13 oe2）
p16.append(_edge("oe2", "o2", "o5", "", (1, 0.5), (0.5, 0), [(275, _sy + _sh / 2), (275, _gy), (_tx + _tw / 2, _gy)]))
_T16A = {r[0]: r for r in T16}
T16A = [_T16A["bootstrap.sh --local（契約入口）"], _T16A["離線包（#27、Q26）"], _T16A[".digest 旁檔"], _T16A["image ID 記錄"], _T16A["local_bootstrap.sh（便利包裝，非契約）"], T_MSG]   # ≤ 8；add --local／工具 tar／斷網 sync 的名詞在「離線包（2）」頁
foot(p16, "p16", F.y, T16A, {"note", "rule", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16", "流程 v2：離線包（1）bootstrap.sh --local", p16))

# ================= P16i：離線包（1′）docker run install =================
p16i, F = newpage_c("流程 v2：離線包（1′）── docker run 本機 image install → version.local.toml（#27、Q26、§4.8）", N16, COLS_OF, gap=14)
b = F.band("bO1i", "離線接入（1′）：docker run 本機 image install（不 pull）→ 建進度檔 → 寫入（見 install 頁）→ 任一寫入失敗？是 → 引擎依進度檔清半成品 → 1；否 → 刪進度檔 → 寫 version.local.toml（本機 tag + image ID）→ 續（2）逐工具 add --local", v2=True)
b.box("o8z", SH, 0, ENTRY, "來自「離線包（1）」頁：tar 已 load 並讀到正式 index digest（或 tag 形已核本機 image）；image ID 已取得、LABEL 介面版已過", 400)
b.box("o8", SH, 1, W12, "docker run 本機 image install（本機有 → 不 pull）", 400)
b.box("o8j", E, 1, SUB, "install：建進度檔 .tmp.install.<id>.toml（第一個寫入前；= 不留半成品的清除清單）", 320)
b.box("o8jf", P, 1, F12, "＋.vendor_kit/.tmp.install.<id>.toml", 280)
b.box("o8e", E, 2, ENTRY, "續「install（1′）」頁與「install（2）」頁的寫入段（與線上接入相同；version.toml 第一行最後寫）", 320)
b.files("o8f", P, 2, "install 寫（log/ 由啟動器先建）", ["version.toml 第一行 = 正式 ref@digest（tar 形：.digest 旁檔；tag 形：既有 version.toml 值，第一次接入用 bootstrap.sh 內嵌引擎 ref）", "薄殼五檔、gen/.stamp", "baseline/.gitkeep（VK 自產進 git 空檔）", "config.toml ＋ 基準版副本 ＋ metadata", "justfile 一行、.dockerignore 四行"], 280)
b.box("o8e2", E, 3, ENTRY, "來自「install（2）」頁：寫入段結束（成功或任一步失敗）", 320)
b.box("o8x", UO, 4, v2(R12), "是 → 1：引擎依進度檔清半成品、不留半成品（log/ 保留）；引擎異常結束時由 bootstrap.sh 補清", 230)
b.box("o8q", E, 4, v2(D12), "任一寫入失敗？", 220, ax="l")
b.box("o8k", E, 5, v2(SUB), "否：刪進度檔 .tmp.install.<id>.toml（最後一步）= install 完成", 320)
b.box("o8kf", P, 5, F12, "－.vendor_kit/.tmp.install.<id>.toml（刪）", 280)
b.box("o9", SH, 6, W12, "install 成功後寫 version.local.toml：vendor_kit = \"vendor_kit:vN\" + vendor_kit_image_id", 400)
b.box("o9f", P, 6, F12, "version.local.toml（不進 git）：本機 tag + image ID", 280)
b.box("o9z", SH, 7, ENTRY, "續「離線包（2）」頁：另備工具 tar，逐一 add <repo> --local；之後斷網 sync 見「離線包（3）」頁", 400)
b.D("oe10", "o8z", "o8", al=True)
b.H("oe11", "o8", "o8j"); b.H("oe11f", "o8j", "o8jf", "建"); b.D("oe11e", "o8j", "o8e", al=True); b.H("oe12", "o8e", "o8f", "寫"); b.D("oe12e", "o8e", "o8e2"); b.D("oe12q", "o8e2", "o8q", al=True)
b.H("oe13x", "o8q", "o8x", "是"); b.D("oe13n", "o8q", "o8k", "否", al=True); b.H("oe12kf", "o8k", "o8kf", "刪")
b.DL("oe13", "o8k", "o9"); b.H("oe14", "o9", "o9f", "寫"); b.D("oe15", "o9", "o9z", al=True)
b.close()
T16I = [_T16A["離線包（#27、Q26）"], _T16A[".digest 旁檔"], _T16A["image ID 記錄"], _T16A["baseline/.gitkeep"], ("install 進度檔（v2.13 P5）", "第一次 install 也在第一個寫入前建 .tmp.install.<id>.toml：兼「不留半成品」的清除清單，失敗依它移除已寫的檔（log/ 保留）、成功後刪；修復型同"), T_MSG]
foot(p16i, "p16i", F.y, T16I, {"note", "sub", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16i", "流程 v2：離線包（1′）docker run install", p16i))

# ================= P16c：離線包（2）add --local 逐工具 =================
_T16 = {r[0]: r for r in T16}

codex
基線結果顯示幾何檢查目前只有 c 檔 3 筆對齊問題，但 lint 仍有附件 L 指定的 `term-count`、`write-fail-edge`、`end-color-text`。我會先修這些硬性項目，再處理附件 F 的內容與排版項目；termcov 警告依你的規則不列為失敗。
2026-09-20T15:46:47.631299Z ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in <scratchpad>/disc_v1_a.py:
Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③全部",
 ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
exec
/usr/bin/bash -lc "sed -n '1296,1312p' disc_v1_a.py
rg -n 'P3B_NOTE|S2C =|S4X0|for _i.*s4x|MXX' disc_v1_a.py
rg -n 'q12k|q14|o3tx' disc_v1_c.py" in <scratchpad>
 succeeded in 0ms:
tmp += vt("p3_off", "p3L4", RULE, OFF_T, 790, y, 750, ch_, tagged=True)
y += ch_ + 20
p3.append(v("p3L4", "1", SW(NEUTRAL), "契約③ 下游 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）", 40, Y, 1560, y))
p3 += tmp
Y += y + 20
Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
 ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))

# ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
S0C = "寫 launcher_start\n（完整 argv）失敗 →\n1 印 6-38、零寫入"
S1 = "① 以版本鎖定行 regex grep 引擎 ref\n（version.local.toml 本機覆寫優先；命中 ≠ 1 → 1）\n非 sync 的動詞跳過下一格"
1307:P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
1308:p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
1316:S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
1350:S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
1351:S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
1497:p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
1500:for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
1915:MXX, RXX, TXX = 530, 552, 576
1917:pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
1918:p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
250:b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
251:b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
252:b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
259:b.H("qe21", "q13", "q13x", "否"); b.D("qe20", "q13", "q12k", "是", al=True); b.H("qe19k", "q12k", "q12kf", "刪"); b.DL("qe22", "q12k", "q14")
703:b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
713:b.H("oe3cx", "o3c", "o3cx", "是"); b.D("oe3t", "o3c", "o3t", "否", al=True); b.D("oe3ti", "o3t", "o3ti", al=True); b.H("oe3tx", "o3ti", "o3tx", "否")

apply patch
patch: completed
<scratchpad>/disc_v1_a.py
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..f6e61100ae96a3e5b802da44a8ba8c2b838b74ec
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..f6e61100ae96a3e5b802da44a8ba8c2b838b74ec
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)

apply patch
patch: completed
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..821679ed9a167fedbddb7ece8a3d7d6e848f81a8
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..821679ed9a167fedbddb7ece8a3d7d6e848f81a8
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

2026-09-20T15:48:36.347703Z ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in <scratchpad>/disc_v1_c.py:
b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..821679ed9a167fedbddb7ece8a3d7d6e848f81a8
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc "sed -n '770,795p' disc_v1_c.py" in <scratchpad>
 succeeded in 0ms:
b.box("o10a", LA, 6, W12, "是：docker load < <工具 tar>", 400)
b.box("o10d", DK, 6, IMG, "本機 image <repo>-dist:<tag>", 240)
b.box("o10bx", UO, 7, R12, "否 → 1 + 6-24（主機錯誤）：同名 .tar.digest 旁檔缺", 230)
b.box("o10bq", LA, 7, v2(D12), "同名 .tar.digest 存在？", 300, ax="l")                       # 旁檔缺 → 出口（與離線包(1) o4 一致；r11）
b.box("o10b", LA, 8, W12, "是：讀 <工具 tar>.digest → 正式 index digest", 400)
b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
b.box("o10vx", UO, 13, R12, "不合 → 1 + 6-30：不動 docker", 230)
b.box("o10v", LA, 13, v2(D12), "是：收完整份、驗首尾／筆數／kind：文法合？", 300, ax="l")
b.box("o10pz", LA, 14, ENTRY, "是 → 續「離線包（2′）」頁：docker create／cp → apply add", 400)
b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
b.H("oe21x", "o10q", "o10qx", "否")
b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
b.close()
foot(p16c, "p16c", F.y, T16B, {"note", "rule", "sub", "img", "hdr", "v2", "entry"})
pages_v1_c.append(("v1p16c", "流程 v2：離線包（2）add --local 逐工具", p16c))

# ================= P16cb：離線包（2′）add --local：create／cp → apply（第十六輪自（2）拆頁）=================

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..821679ed9a167fedbddb7ece8a3d7d6e848f81a8
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

2026-09-20T15:48:57.099960Z ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in <scratchpad>/disc_v1_c.py:
b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..821679ed9a167fedbddb7ece8a3d7d6e848f81a8
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

apply patch
patch: completed
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..cd12c25147b7f858d76b77dabc5885af10ddceca
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..cd12c25147b7f858d76b77dabc5885af10ddceca
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

codex
第一輪硬性修改已完成：v1p3 名詞縮到 8、契約④修正 apply 結束碼分色與文法說明、v1p9c 加共通失敗匯流、v1p16 修正橙色終點、v1p16cb 拆開寫鎖定行／刪進度、v1p16ccc 拆開 cache／印記並補寫入失敗匯流。現在重新產生並抓實際幾何回歸。
exec
/usr/bin/bash -lc 'python3 run_v1_a.py && python3 run_v1_c.py' in <scratchpad>
 exited 1 in 140ms:
Traceback (most recent call last):
  File "<scratchpad>/run_v1_c.py", line 4, in <module>
    exec(open("disc_v1_c.py").read())
  File "<string>", line 253, in <module>
NameError: name 'XA' is not defined. Did you mean: '_A'?

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..cd12c25147b7f858d76b77dabc5885af10ddceca
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", XA, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 390)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

apply patch
patch: completed
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..3e27e6a5f01ad9b9194a12f229030177b982f6ba
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..3e27e6a5f01ad9b9194a12f229030177b982f6ba
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc 'python3 run_v1_c.py' in <scratchpad>
 succeeded in 0ms:
v1p9 流程 v2：prune（1）resolve → 差集 → 刪 page ('1650', '2317') cells 125
v1p9c 流程 v2：prune（2）apply 清暫存 page ('1650', '1646') cells 91
v1p10 流程 v2：update page ('1650', '2259') cells 115
v1p11 狀態機 v2：初始檔五態 page ('1650', '2127') cells 79
v1p12 狀態機 v2：交易與進度檔 page ('1650', '2363') cells 144
v1p13 相容性矩陣 v2 page ('1650', '1235') cells 74
v1p14 結束碼決策表 v2 page ('1650', '1430') cells 122
v1p15 流程 v2：vendor_kit release（1）build 與驗收 page ('1650', '2128') cells 98
v1p15c 流程 v2：vendor_kit release（2）推 image 與資產 page ('1650', '1621') cells 86
v1p16 流程 v2：離線包（1）bootstrap.sh --local page ('1650', '2267') cells 117
v1p16i 流程 v2：離線包（1′）docker run install page ('1650', '1580') cells 73
v1p16c 流程 v2：離線包（2）add --local 逐工具 page ('1650', '1826') cells 97
v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply page ('1650', '1576') cells 74
v1p16cc 流程 v2：離線包（3）斷網 sync page ('1650', '1795') cells 82
v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證 page ('1650', '1582') cells 72
v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝 page ('1650', '2115') cells 118

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..3e27e6a5f01ad9b9194a12f229030177b982f6ba
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc 'for f in v1_a.drawio v1_c.drawio; do
  echo "### $f"
  for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py check_margin_label.py; do echo "-- $c"; python3 "$c" "$f" | tail -n 8; done
done
AOUT=$(mktemp -d /tmp/v1a_lint.XXXXXX)
COUT=$(mktemp -d /tmp/v1c_lint.XXXXXX)
python3 extract_pages.py v1_a.drawio "$AOUT" >/dev/null
python3 lint_pages.py "$AOUT" >/dev/null
python3 extract_pages.py v1_c.drawio "$COUT" >/dev/null
python3 lint_pages.py "$COUT" >/dev/null
echo "A=$AOUT C=$COUT"
rg '"'"'^'"\\| (term-count|term-dup-page0|event-name|resolve-3way|precheck-recover|end-color-text|write-line|write-fail-edge|page-height|edge-font|merge-fanout)' \""'$AOUT/lint.md" "$COUT/lint.md"
rg '"'"'^-'"' \""'$AOUT/lint.md" "$COUT/lint.md" | rg '"'\\[warn\\]' | rg -v '\\[termcov\\]' | head -n 100" in <scratchpad>
 succeeded in 1814ms:
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
-- check_overlap.py
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   mount_dist (h4→p4E) 壓到 p4H「主機（下游使用者電腦／CI runner」 ['L1', 'L2']
   mount_dist (h4→p4E) 壓到 tmp「暫存 .vendor_kit/<br>.」 ['L1', 'L2']
共 2 筆
-- check_cross_v1b.py
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
-- check_self_v1b.py
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   ret_cli 穿過標題列 p4E
共 1 筆
-- check_jog_r7.py
共 0 筆
-- check_align_v1b.py
== 流程 v2：remove（1）resolve → apply 前置
   無
== 流程 v2：remove（2）寫入段
   無
== 流程 v2：uninstall（1）resolve → apply 前置
   無
== 流程 v2：uninstall（2）寫入段
   無
-- check_margin_label.py
   無
== v1p3c 契約 v2：CI 契約⑤ 與驗收矩陣
   無
== v1p3d 契約 v2：驗收矩陣詳表
   無
== v1p4 架構圖 v2
   無
共 0 筆
### v1_c.drawio
-- check_overflow.py
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
-- check_overlap.py
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
-- check_cross_v1b.py
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
-- check_self_v1b.py
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 1 筆
-- check_jog_r7.py
v1p16cc we2a w2q→w2a dx=3
v1p16ccb we6q w4m→w4q dx=10
v1p16ccc wf6y w4v1q→w4tq dx=20
共 3 筆
-- check_align_v1b.py
== 流程 v2：remove（1）resolve → apply 前置
   無
== 流程 v2：remove（2）寫入段
   無
== 流程 v2：uninstall（1）resolve → apply 前置
   無
== 流程 v2：uninstall（2）寫入段
   無
-- check_margin_label.py
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 0 筆
A=/tmp/v1a_lint.mJt1t1 C=/tmp/v1c_lint.kO51AY
/tmp/v1c_lint.kO51AY/lint.md:| event-name | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| resolve-3way | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| precheck-recover | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| end-color-text | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| write-line | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| write-fail-edge | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| term-count | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| term-dup-page0 | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| page-height | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| edge-font | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:| merge-fanout | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| event-name | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| resolve-3way | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| precheck-recover | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| end-color-text | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| write-line | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| write-fail-edge | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| term-count | 1 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| term-dup-page0 | 1 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| page-height | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| edge-font | 0 | 0 |
/tmp/v1a_lint.mJt1t1/lint.md:| merge-fanout | 0 | 0 |
/tmp/v1c_lint.kO51AY/lint.md:- [dangling][warn] o10fail: end_red 無進邊：「任一寫入失敗匯流 → 1：進度保留，下次先恢復」
/tmp/v1c_lint.kO51AY/lint.md:- [dangling][warn] w4fail: end_red 無進邊：「任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做」
/tmp/v1a_lint.mJt1t1/lint.md:- [term-dup-page0][warn] resolve／apply: 名詞「resolve／apply」第 0 頁已有（同名或只差結尾括號），不必重列
/tmp/v1a_lint.mJt1t1/lint.md:- [term-count][warn] -: 名詞表 10 條 > 8

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..3e27e6a5f01ad9b9194a12f229030177b982f6ba
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc "rg -n -B3 -A3 '\\[term-(count|dup-page0)\\]' /tmp/v1a_lint.mJt1t1/lint.md
python3 check_self_v1b.py v1_c.drawio | tail -n 20" in <scratchpad>
 succeeded in 0ms:
141-- [termcov][warn] p1B_r11c3: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
142-- [termcov][warn] p1B_r12c2_1: 「6-32」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
143-- [termcov][info] -: 7 個關鍵字只在名詞說明文出現、沒有獨立條（略）：--local、version.toml、metadata、cache/、.tmp.dist、6-2b、6-2
144:- [term-dup-page0][warn] resolve／apply: 名詞「resolve／apply」第 0 頁已有（同名或只差結尾括號），不必重列
145-
146-## v1p1c 契約 v2：規則、選項表、不開的動詞
147-nodes 240／edges 4／terms 7；warn 40、info 2
--
222-- [onething][info] p2b_ver_m: [step] 分隔詞 4（、1 ；3）：「進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；下游使用者、Renovate 可手改；sync 只讀」
223-- [onething][info] p2b_vl_m: [step] 分隔詞 9（→1 再1 ；7）：「不進 git（自有 .gitignore 擋）；與 version.toml 同形（同一套讀寫器）；寫入者 dev／undev／bootstrap --local；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；CI 模式下存在任何覆寫 → sync 回 1；啟動器先讀它再退回 version.toml」
224-- [onething][info] p2b_mt_m: [step] 分隔詞 5（並1 ；4）：「進 git；寫入者 add／upgrade；兼作 baseline/<repo>/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列。註：install 對根 .dockerignore 的四行 append 不屬任何工具，記於 baseline/.vendor_kit.toml（同檔案版，只含 [[file]] dest=.dockerignore state=appended lines=四行），uninstall 讀它刪原文相同行」
225:- [term-count][warn] -: 名詞表 10 條 > 8
226-
227-## v1p2c 契約 v2：動詞 × 檔案矩陣
228-nodes 221／edges 0／terms 7；warn 20、info 2
   無
== v1p15 流程 v2：vendor_kit release（1）build 與驗收
   無
== v1p15c 流程 v2：vendor_kit release（2）推 image 與資產
   無
== v1p16 流程 v2：離線包（1）bootstrap.sh --local
   無
== v1p16i 流程 v2：離線包（1′）docker run install
   無
== v1p16c 流程 v2：離線包（2）add --local 逐工具
   oe25r: 標籤寬 108 ≥ 兩端距離 14「恢復成功／無進度檔」
== v1p16cb 流程 v2：離線包（2′）add --local：create／cp → apply
   無
== v1p16cc 流程 v2：離線包（3）斷網 sync
   無
== v1p16ccb 流程 v2：離線包（3″）resolve sync 驗證
   無
== v1p16ccc 流程 v2：離線包（3′）apply sync 先驗後重裝
   無
共 1 筆

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..f3924d4f29b8558ff2376233035294a1dc1fa217
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
@@ -1912,7 +1912,7 @@
 p4.append(vb("p4_chain_n", "p4E", NOTE, CHAIN_N, MX, log_row_y, MW, log_row_h - 18))
 # ---- 跨區的線（啟動器 ↔ 引擎／registry／專案檔）----
 # 啟動器底邊出三條到引擎：mount（x=530，進容器左框）、run（x=550，進容器左框：動詞、參數、介面版）、ret（x=575，容器 → 啟動器：結束碼、vk-resolve 清單）
-MXX, RXX, TXX = 530, 552, 576
+MXX, RXX, TXX = 500, 555, 610
 Y_M, Y_R, Y_T = LY + 150, LY + 110, LY + 70
 pts = [(MXX, HB), (MXX, Y_M), (EX, Y_M)]
 p4.append(ew("mount_dist", "h4", "p4E", "-v .tmp.dist.<id>/ → /dist\n（唯讀；下有 <repo>/）\n本機覆寫 <dir>/dist\n→ /dist/<repo>", (round((MXX - HX) / HW4, 4), 1), (0, round((Y_M - LY) / LH, 4)), pts[1:-1], lab="left", pos=pos_at(pts, 0, y=HB + 22)))
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..3e27e6a5f01ad9b9194a12f229030177b982f6ba
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, R12, "任一寫入失敗匯流 → 1：進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, R12, "任一寫入失敗匯流 → 1：保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

apply patch
patch: completed
<scratchpad>/disc_v1_a.py
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..e38e083447efd93eba5b9951241812e1cba4e0dd
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..e38e083447efd93eba5b9951241812e1cba4e0dd
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -784,7 +785,7 @@
 b.D("oe20", "oo0", "oo1"); b.D("oe20b", "oo1", "oo1b"); b.D("oe21", "oo1b", "o10"); b.H("oe21s", "o10", "o10s"); b.D("oe21s2", "o10s", "o10s2"); b.H("oe21sx", "o10s2", "o10sx"); b.D("oe21q", "o10s2", "o10q", al=True)
 b.H("oe21x", "o10q", "o10qx", "否")
 b.D("oe22", "o10q", "o10a", "是", al=True); b.H("oe22d", "o10a", "o10d", "載"); b.D("oe23", "o10a", "o10bq", al=True); b.H("oe23x", "o10bq", "o10bx", "否"); b.D("oe23b", "o10bq", "o10b", "是", al=True)
-b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
+b.D("oe24", "o10b", "o10c"); b.H("oe24d", "o10c", "o10cd"); b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe25r", "o10re", "o10re2", "恢復成功／無進度檔"); b.DL("oe26", "o10re2", "o10rq", "vk-resolve")
 b.H("oe26rx", "o10rq", "o10rx", "否"); b.D("oe26ry", "o10rq", "o10v", "是", al=True)
 b.H("oe26x", "o10v", "o10vx", "否"); b.D("oe26y", "o10v", "o10pz", "是", al=True)
 b.close()
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

apply patch
patch: completed
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..d23dd4922509d0bc187b819d0077cb4d6571e30f
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..d23dd4922509d0bc187b819d0077cb4d6571e30f
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc 'python3 run_v1_a.py >/tmp/run_a.log && python3 run_v1_c.py >/tmp/run_c.log
for f in v1_a.drawio v1_c.drawio; do
  echo "### $f"
  for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py check_margin_label.py; do printf '"'%s: ' \""'$c"; python3 "$c" "$f" | tail -n 1; done
done' in <scratchpad>
 succeeded in 1622ms:
### v1_a.drawio
check_overflow.py: 共 0 筆
check_overlap.py: 共 0 筆
check_cross_v1b.py: 共 0 筆
check_self_v1b.py: 共 0 筆
check_jog_r7.py: 共 0 筆
check_align_v1b.py:    無
check_margin_label.py: 共 0 筆
### v1_c.drawio
check_overflow.py: 共 0 筆
check_overlap.py: 共 0 筆
check_cross_v1b.py: 共 0 筆
check_self_v1b.py: 共 0 筆
check_jog_r7.py: 共 1 筆
check_align_v1b.py:    無
check_margin_label.py: 共 0 筆

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..d23dd4922509d0bc187b819d0077cb4d6571e30f
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc 'python3 check_jog_r7.py v1_c.drawio | tail -n 12
AOUT=$(mktemp -d /tmp/v1a_final.XXXXXX); COUT=$(mktemp -d /tmp/v1c_final.XXXXXX)
python3 extract_pages.py v1_a.drawio "$AOUT" >/dev/null; python3 lint_pages.py "$AOUT" >/dev/null
python3 extract_pages.py v1_c.drawio "$COUT" >/dev/null; python3 lint_pages.py "$COUT" >/dev/null
echo "$AOUT $COUT"
rg '"'"'^-'"' \""'$AOUT/lint.md" "$COUT/lint.md" | rg '"'\\[warn\\]' | rg -v '\\[termcov\\]'" in <scratchpad>
 succeeded in 340ms:
/tmp/v1a_final.rb0Pbf /tmp/v1c_final.aiTqbA
/tmp/v1a_final.rb0Pbf/lint.md:- [term-dup-page0][warn] resolve／apply: 名詞「resolve／apply」第 0 頁已有（同名或只差結尾括號），不必重列
/tmp/v1a_final.rb0Pbf/lint.md:- [term-count][warn] -: 名詞表 10 條 > 8

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..d23dd4922509d0bc187b819d0077cb4d6571e30f
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc "python3 - <<'PY'
import json
p=json.load(open('/tmp/v1c_final.aiTqbA/v1p16ccc.json'))
for n in p['nodes']:
 if n['id'] in ('w4v1q','w4tq'): print(n['id'], n['x'], n['y'], n['w'], n['h'])
PY" in <scratchpad>
 succeeded in 0ms:
w4v1q 970 758 200 50
w4tq 970 822 234 112

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..d23dd4922509d0bc187b819d0077cb4d6571e30f
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax="l")
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

apply patch
patch: completed
<scratchpad>/disc_v1_c.py
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

codex
目前兩份圖的 overflow／overlap／cross／self／margin 已清零，c 檔只剩 1 筆 17px 的垂直對齊，我已按實際展開後座標修正。a 檔 lint 尚有兩筆，但都落在你明令不可改的 v1p1b、v1p2b；指定可改頁的非 termcov lint 已清零。完成最終驗證前，我會依 `implement` 技能要求讀取並執行 code-review 流程。
exec
/usr/bin/bash -lc "sed -n '1,260p' /home/cyc/.agents/skills/code-review/SKILL.md" in <scratchpad>
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

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc 'python3 run_v1_a.py >/tmp/final_run_a.log && python3 run_v1_c.py >/tmp/final_run_c.log
for f in v1_a.drawio v1_c.drawio; do
  echo "### $f"
  for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py check_margin_label.py; do
    printf '"'%s: ' \""'$c"
    python3 "$c" "$f" | tail -n 1
  done
done
AOUT=$(mktemp -d /tmp/v1a_verified.XXXXXX)
COUT=$(mktemp -d /tmp/v1c_verified.XXXXXX)
python3 extract_pages.py v1_a.drawio "$AOUT" >/tmp/extract_a.log
python3 lint_pages.py "$AOUT" >/tmp/lint_a.log
python3 extract_pages.py v1_c.drawio "$COUT" >/tmp/extract_c.log
python3 lint_pages.py "$COUT" >/tmp/lint_c.log
echo "AOUT=$AOUT"
echo "COUT=$COUT"
echo "non-termcov warnings:"
rg '"'"'^-'"' \""'$AOUT/lint.md" "$COUT/lint.md" | rg '"'\\[warn\\]' | rg -v '\\[termcov\\]' || true
echo \"target-page non-termcov warnings:\"
python3 - \""'$AOUT/lint.json" "$COUT/lint.json" <<'"'PY'
import json,sys
allowed={'v1p2','v1p3','v1p3b','v1p3bb','v1p3c','v1p3d','v1p4','v1p9','v1p9c','v1p10','v1p11','v1p12','v1p15','v1p15c','v1p16','v1p16i','v1p16c','v1p16cb','v1p16cc','v1p16ccb','v1p16ccc'}
for fn in sys.argv[1:]:
 d=json.load(open(fn))
 items=d if isinstance(d,list) else d.get('items',[])
 for x in items:
  if x.get('page') in allowed and x.get('level')=='warn' and x.get('rule')"'!='"'termcov': print(fn,x)
PY
wc -l disc_v1_a.py disc_v1_c.py
sha256sum disc_v1_b.py gen_disc.py drawio_common.py check_*.py lint_pages.py extract_pages.py | tail -n 8" in <scratchpad>
 succeeded in 2098ms:
### v1_a.drawio
check_overflow.py: 共 0 筆
check_overlap.py: 共 0 筆
check_cross_v1b.py: 共 0 筆
check_self_v1b.py: 共 0 筆
check_jog_r7.py: 共 0 筆
check_align_v1b.py:    無
check_margin_label.py: 共 0 筆
### v1_c.drawio
check_overflow.py: 共 0 筆
check_overlap.py: 共 0 筆
check_cross_v1b.py: 共 0 筆
check_self_v1b.py: 共 0 筆
check_jog_r7.py: 共 0 筆
check_align_v1b.py:    無
check_margin_label.py: 共 0 筆
AOUT=/tmp/v1a_verified.1Tpc4b
COUT=/tmp/v1c_verified.FQcDwo
non-termcov warnings:
/tmp/v1a_verified.1Tpc4b/lint.md:- [term-dup-page0][warn] resolve／apply: 名詞「resolve／apply」第 0 頁已有（同名或只差結尾括號），不必重列
/tmp/v1a_verified.1Tpc4b/lint.md:- [term-count][warn] -: 名詞表 10 條 > 8
target-page non-termcov warnings:
  1946 disc_v1_a.py
   947 disc_v1_c.py
  2893 total
98c3541f93c93af00f911682f901f885f23749040dd6e21e6cb1205986838ffe  check_cross_v1b.py
4189828c8ccf266638549d994af8bcf99821128ed1bc1e4724ac605f61450f42  check_jog_r7.py
fd49923cdf93b4e64177249ec28e75763979d47d36f6edb0a81d40c7e8310989  check_margin_label.py
b28be31fd5dd72443b554941fa1cad163e07e0137d79d7bb93025a81c2fe83bc  check_overflow.py
34b8003a1d414e4c2febe77c6ead900994220666e154aca97f4fc289b03c1d70  check_overlap.py
8f925a1008e8b1f3aec5c3404493cc00caeb77913a30c9e5b52b9b3699789906  check_self_v1b.py
8beba9edded2231667fc027f505a64f00e5461757486e8731c6c7a1cd3462f28  lint_pages.py
f0844b1f4d3438896f076502e4d2dabb6d84bd5cb92c0d79aad11e80972da2ba  extract_pages.py

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

exec
/usr/bin/bash -lc "ls -1 disc_v1_a.py* disc_v1_c.py* | head -n 30
rg -n 'q12_fail_bus|o10fail|w4fail|o10r0s|w4r0s|P3B_NOTE|S4X1' disc_v1_a.py disc_v1_c.py" in <scratchpad>
 succeeded in 0ms:
disc_v1_a.py
disc_v1_a.py.v1
disc_v1_a.py.v10
disc_v1_a.py.v11
disc_v1_a.py.v11b
disc_v1_a.py.v12
disc_v1_a.py.v13
disc_v1_a.py.v14
disc_v1_a.py.v15
disc_v1_a.py.v16
disc_v1_a.py.v17
disc_v1_a.py.v18
disc_v1_a.py.v19
disc_v1_a.py.v2
disc_v1_a.py.v3
disc_v1_a.py.v4
disc_v1_a.py.v5
disc_v1_a.py.v6
disc_v1_a.py.v7
disc_v1_a.py.v8
disc_v1_a.py.v9
disc_v1_c.py
disc_v1_c.py.v10
disc_v1_c.py.v11
disc_v1_c.py.v11b
disc_v1_c.py.v12
disc_v1_c.py.v13
disc_v1_c.py.v14
disc_v1_c.py.v15
disc_v1_c.py.v16
disc_v1_c.py:253:b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
disc_v1_c.py:819:b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
disc_v1_c.py:928:b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
disc_v1_c.py:933:b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
disc_v1_c.py:937:b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
disc_v1_a.py:1307:P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
disc_v1_a.py:1308:p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
disc_v1_a.py:1350:S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
disc_v1_a.py:1351:S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
disc_v1_a.py:1498:p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))

diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

codex
已完成修改並重產 [v1_a.drawio](<scratchpad>/v1_a.drawio) 與 [v1_c.drawio](<scratchpad>/v1_c.drawio)。

修改頁面：

- `v1p3`：名詞表由 16 條縮至 8 條。
- `v1p3b`：移除沿革便條；補強 vk-resolve 文法失敗規則；apply 結束碼改為 1 紅、2／3 橙。
- `v1p9c`：加入寫入／刪除共通失敗匯流。
- `v1p16`：`o3tx` 改為橙色需人處理終點。
- `v1p16c`：resolve 內補既有進度檔恢復與 6-27 語意。
- `v1p16cb`：拆開「寫 version.toml」與「刪 [progress]」；加入共通寫入失敗匯流。
- `v1p16cc`：修正 `we2a` 垂直對齊。
- `v1p16ccb`：修正 `we6q` 垂直對齊。
- `v1p16ccc`：拆開寫 cache 與寫印記及其檔案框；補共通寫入失敗匯流；修正 `wf6y` 對齊。

其餘指定頁現況已涵蓋附件項目，未作不必要改動。禁止修改的頁面及 `disc_v1_b.py`、產生器共用檔、檢查工具均未修改。

待處理便條：無。

驗證結果：

- `run_v1_a.py`：成功
- `run_v1_c.py`：成功
- 兩份 draw.io 的 overflow、overlap、cross、self、jog、align、margin-label：全部 0 筆／無問題
- 指定可修改頁的非 termcov lint：0
- 事件名稱、write-fail-edge、end-color-text、page-height、edge-font 等：0

整份 `v1_a.drawio` 仍有兩筆非 termcov lint，均位於明令不可改的頁面：

- `v1p1b`：`term-dup-page0`
- `v1p2b`：`term-count` 10 > 8

因此沒有違反「絕對不可改」限制去清除它們。工作目錄不是 Git repository，故無法依技能流程提交 commit 或執行以 Git fixed point 為基礎的雙軸 code review。
diff --git a/disc_v1_a.py b/disc_v1_a.py
index f41373812606a591fec068950329be5cfd16482d..72f0811694c2971f24c09d424a00ad835a98b179
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -1299,12 +1299,12 @@
 p3 += tmp
 Y += y + 20
 Y = footer(p3, "p3", Y, ["v3img", "v2code", "ruleb", "tblh", "grpbox", "v2tag", "notep"], "紫 = image（工具／引擎）\n淺灰底容器 = 契約③ 全部",
- ["dockerfiledist", "label", "dest", "append", "crlf", "syncrecipe", "justdirs", "buildx", "indexdigest", "checkdist", "digestfile", "offline", "deploy", "ns", "semver", "localboot"])   # 第 0 頁已有的詞不列
+ ["append", "crlf", "syncrecipe", "justdirs", "checkdist", "digestfile", "offline", "localboot"])   # 每頁至多 8 條；其餘名詞已由本頁內文定義
 pages_v1_a.append(("v1p3", "契約 v2：下游 repo 契約③", p3))
 
 # ================= P3b v1p3b：契約④ 啟動器 ↔ 引擎 =================
 p3b = head("p3b", "契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）", 1200)
-P3B_NOTE = "<b>本頁決議狀態（v2.15 結案）</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）"
+P3B_NOTE = "<b>本頁無待處理問題</b>\n規則框逐條對應 interface_spec §3、§5；vk-resolve/1 必須先收完整份並驗文法，才能動 docker。"
 p3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)
 S0A = "⓪ 產 trace_id\n（uuid；缺則\nod urandom）"
 S0B = "建執行紀錄\nlog/<verb>/\n<ts>-<id8>.jsonl"
@@ -1313,7 +1313,7 @@
 D1_T = "只有 sync：\ngen/.stamp\n≠ 引擎 ref？"
 S2A = "讀 version.toml／local\n（CI 模式判定）"
 S2B = "只有 add／upgrade 未指定\n@<tag> 且非 CI 模式：查 registry\n最新正式版（update 單段另畫）"
-S2C = "stdout vk-resolve/1\n（pull／extract／mount／engine／fingerprint／apply／end）"
+S2C = "stdout vk-resolve/1\n（先收完整份並驗文法；不合 → 1 + 6-30）\n合法才繼續"
 D2_T = "apply|yes？"
 OK_T = "否（apply|no）→ 0 快路徑\n不起第二個容器"
 S3A = "docker image inspect\n（每筆 pull／extract）"
@@ -1347,7 +1347,7 @@
 S3BXW = 200; s3bxh = hve(S3BX, S3BXW)
 r3y = r2y + max(row2h, eh) + 34
 okY = r3y
-S4X0 = "0：成功\n（約定①）"; S4X1 = "1／2／3：需人處理\n（印指令／解衝突）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"          # ④ 終點依結束碼分色（Claude r13 s4x）
+S4X0 = "0：成功\n（約定①）"; S4X1 = "2／3：需人處理\n（解衝突／介面不合）"; S4X2 = "1：失敗\n（拉不到／寫入失敗）"
 S4XW0, S4XW1, S4XW2 = 100, 150, 120; s4xh = max(hve(S4X0, S4XW0), hve(S4X1, S4XW1), hve(S4X2, S4XW2))
 U5A = "單段 update [<repo>]：\ndocker run 引擎 update\n（不經 ②③④）"
 U5B = "update：查 registry 每個目標（[tools] + vendor_kit）\n的最新正式版（token 以 -e 傳；無憑證 → 記 6-3）"
@@ -1497,7 +1497,7 @@
 p3b.append(v("s4x0", "p3L2", ELLIPSE(GREEN) + "fontSize=12;", S4X0, s4x_x0, okY, S4XW0, s4xh))
 p3b.append(v("s4x1", "p3L2", ELLIPSE(ORANGE) + "fontSize=12;", S4X1, s4x_x1, okY, S4XW1, s4xh))
 p3b.append(v("s4x2", "p3L2", ELLIPSE(RED) + "fontSize=12;", S4X2, s4x_x2, okY, S4XW2, s4xh))
-for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "1／2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
+for _i, (_id, _xx, _ww, _ex, _dy, _lab) in enumerate((("s4x0", s4x_x0, S4XW0, 0.2, 28, "0"), ("s4x1", s4x_x1, S4XW1, 0.5, 18, "2／3"), ("s4x2", s4x_x2, S4XW2, 0.8, 8, "1"))):
     _pts = [(AX + x + W2["s4"] * _ex, AY + r2c + h2["s4"] / 2), (AX + x + W2["s4"] * _ex, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY - _dy), (AX + _xx + _ww / 2, AY + okY)]
     p3b.append(ew(f"{_id}_e", "s4", _id, _lab, (_ex, 1), (0.5, 0), _pts[1:-1], lab="side", pos=pos_at(_pts, 0, y=AY + r2c + h2["s4"] / 2 + 4)))
 # 第 0 列：⓪ 寫 launcher_start 失敗、① grep 命中 ≠ 1 的紅終點（各自從格頂端往上；Claude r13 s0c／s1）
diff --git a/disc_v1_c.py b/disc_v1_c.py
index c87356f924305c33fe12a26f52ab8f28e5023455..a4e60cd1cdf3a9b286ef50477cac65149747982b
--- a/disc_v1_c.py
+++ b/disc_v1_c.py
@@ -250,6 +250,7 @@
 b.box("q12k", E, 11, v2(SUB), "是：刪進度檔 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
 b.box("q12kf", P, 11, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
 b.box("q14", U, 12, G12, "→ 0：印刪了什麼、保留什麼（含原因）", 200)
+b.box("q12_fail_bus", P, 12, RULE, "任一寫入／刪除失敗匯流：記 failed，繼續其餘項；全部完成後由「全部刪除成功？」分流", 280)
 b.D("qe17z", "q12z", "q12", al=True)
 b.DL("qe18", "q12", "q12a"); b.H("qe18ax", "q12a", "q12ax", "逾時"); b.D("qe18a", "q12a", "q12b"); b.H("qe18bx", "q12b", "q12bx", "不同")
 b.D("qe18d", "q12b", "q12d", al=True); b.H("qe18dy", "q12d", "q12dy", "是"); b.D("qe18j", "q12d", "q12j", "否", al=True)
@@ -700,7 +701,7 @@
 b.box("o6c", SH, 14, W12, "是：docker load < <引擎 tar>", 300, ax="l")
 b.box("o6d", DK, 14, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 220)
 b.box("o3ti", SH2, 14, v2(D12), "docker image inspect <tag>：本機有此 image？", 300, ax="l")
-b.box("o3tx", P, 14, v2(R12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
+b.box("o3tx", P, 14, v2(O12), "否 → 1：本機無此 image（tag 形：先 docker load 或改給 tar）", 280)
 b.box("o7a", SH, 15, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
 b.box("o7b", SH, 16, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
 b.box("o7bd", DK, 16, NOTE, "結果：回 image ID（sha256:<hex64>）", 220)
@@ -774,7 +775,7 @@
 b.box("o10c", LA, 9, W12, "docker image inspect --format '{{.Id}}' → image ID", 400)
 b.box("o10cd", DK, 9, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)
 b.box("o10r", LA, 10, W12, "docker run 引擎 resolve add <repo> --local（帶 index digest + image ID；永不 -t）", 400)
-b.box("o10re", E, 10, SUB, "resolve（不寫）：算 extract 清單與輸入指紋（不查 registry）", 320)
+b.box("o10re", E, 10, SUB, "resolve（不寫）：先偵測既有進度檔；有則恢復（失敗 → 1 + 6-27）", 320)
 b.box("o10re2", E, 11, SUB, "stdout vk-resolve/1：extract|<repo>|<本機 ref>、fingerprint、apply|yes、end|N", 320)
 b.box("o10rx", UO, 12, v2(O12), "否 → 1／2／3 原碼傳出：不讀 stdout、不跑 docker／apply", 230)
 b.box("o10rq", LA, 12, v2(D12), "resolve 結束碼 0？", 300, ax="l")
@@ -810,13 +811,16 @@
 b.box("o10f", P, 7, F12, "metadata：source + local_image_id", 280)
 b.box("o10z", E, 8, ENTRY, "續「add（2）」頁：初始檔、基準版、cache/<repo>/、印記、gen/tools.just（與線上接入相同）", 320)
 b.box("o10z2", E, 9, ENTRY, "來自「add（2）」頁：其餘寫入完成", 320)
-b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）→ 刪 [progress]", 320)
+b.box("o10e4", E, 10, SUB, "寫 version.toml [tools] 行：正式 ref@digest（最後寫）", 320)
 b.box("o10f2", P, 10, F12, "version.toml [tools] 行（正式 ref@digest；與線上接入相同）", 280)
-b.box("o11", UO, 11, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10e5", E, 11, SUB, "刪 metadata [progress]（交易完成）", 320)
+b.box("o10f3", P, 11, F12, "metadata [progress]（刪）", 280)
+b.box("o11", UO, 12, G12, "0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add", 230)
+b.box("o10fail", UO, 13, RULE, "任一寫入失敗匯流：回 1，進度保留，下次先恢復", 230)
 b.D("oe26a", "o10p0", "o10p", al=True)
 b.D("oe26b", "o10p", "o10p2"); b.DL("oe26e", "o10p2", "o10e"); b.H("oe26ex", "o10e", "o10ex", "逾時"); b.D("oe26f", "o10e", "o10e2"); b.H("oe26fx", "o10e2", "o10ex2", "≠"); b.D("oe26q", "o10e2", "o10dq", al=True); b.H("oe26dy", "o10dq", "o10dy", "是")
 b.D("oe26g", "o10dq", "o10pg", "否", al=True); b.H("oe26pf", "o10pg", "o10pgf", "建"); b.D("oe26h", "o10pg", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.D("oe27z", "o10e3", "o10z"); b.D("oe27z2", "o10z2", "o10e4"); b.H("oe27c", "o10e4", "o10f2", "寫")
-b.DL("oe28", "o10e4", "o11")
+b.D("oe28a", "o10e4", "o10e5"); b.H("oe28f", "o10e5", "o10f3", "刪"); b.DL("oe28", "o10e5", "o11")
 b.close()   # 逾時／≠ 各自 H 線進自己的橙終點（不再共線、不交叉；r13 oe26fx）
 foot(p16cb, "p16cb", F.y, T16BB, {"note", "sub", "hdr", "v2", "entry"})
 pages_v1_c.append(("v1p16cb", "流程 v2：離線包（2′）add --local：create／cp → apply", p16cb))
@@ -834,7 +838,7 @@
 b.box("w1q", LA, 3, v2(D12), "全相符、未指定 --verify、且非 CI 模式？", 300, ax="l")
 b.box("w2q", LA, 4, v2(D12), "否：version.local.toml 有引擎的本機覆寫？", 300, ax="l")
 b.box("w2r", P, 4, v2(RULE), "已定（v2.6-1、19條-11、v2.15、v2.16-14）：不用 --pull never（docker 19.03 無此旗標）；先 inspect：有本機覆寫 → inspect <tag> 並核 image ID，相符就直接用本機 tag docker run（不再 inspect 正式 ref、不 pull）；否則 inspect version.toml 的正式 ref@digest；本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）", 280)
-b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax="l")
+b.box("w2a", LA, 5, D12, "是：docker image inspect <tag>：.Id == vendor_kit_image_id？", 300, ax=-3)
 b.box("w2ax", DK, 5, v2(O12), "≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）", 240)
 b.box("w2b", LA, 6, W12, "否：docker image inspect <version.toml 的正式 ref@digest>", 260, ax="l")
 b.box("w3", LA, 7, D12, "本機有該 image？", 220, ax="l")
@@ -880,7 +884,7 @@
 b.box("w4mx", UO, 6, v2(O12), "否（無完成標記）→ 1 + 6-13：請先 add 完成接入", 230)
 b.box("w4m", E, 6, v2(D12), "否：metadata 有完成標記？", 300, ax="l")
 b.box("w4qy", UO, 7, G12, "是 → 0：apply|no，不起第二個容器", 230)
-b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 320, ax="l")
+b.box("w4q", E, 7, v2(D12), "是：算出 apply|no？（印記／cache／tools.just 全相符、非 --verify／CI 模式）", 300, ax="l")
 b.box("w4z", E, 8, ENTRY, "否 → 續「離線包（3′）」頁：docker create／cp → apply sync（flock → 指紋 → 先驗既有 cache，不符才重裝一次）", 320)
 b.H("we6", "w4z0", "w4e"); b.H("we6x", "w4e", "w4ex", "≠"); b.D("we6e", "w4e", "w4e2", "是", al=True); b.DL("we6r", "w4e2", "w4rq", "vk-resolve")
 b.H("we6rx", "w4rq", "w4rx", "否"); b.D("we6rv", "w4rq", "w4v", "是", al=True); b.H("we6vx", "w4v", "w4vx", "否"); b.DL("we6t", "w4v", "w4t", "是")
@@ -904,7 +908,7 @@
 b.box("w4vq", E, 5, v2(D12), "要先驗既有 cache？（--verify／CI 模式／版本變動那次）", 320, ax="l")
 b.box("w4v", E, 6, v2(SUB), "是：逐檔 sha256 驗既有 cache/<repo>/（對印記 gen/<repo>.stamp 每檔行）", 320)
 b.box("w4v1q", E, 7, v2(D12), "全相符？", 200, ax="l")
-b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 240, ax="l")
+b.box("w4tq", E, 8, v2(D12), "是：gen/tools.just 存在？", 200, ax=-17)
 b.box("w5", UO, 8, G12, "是 → 0：既有 cache 相符、不重裝（驗收 §7.4-17）", 230)
 b.box("w4tr", E, 9, SUB, "否：重生 gen/tools.just（原子替換；cache 不動）", 320)
 b.box("w4trf", P, 9, F12, "gen/tools.just（只寫不進 git 的）", 280)
@@ -919,15 +923,18 @@
 b.box("w4r3", E, 14, v2(SUB), "是：最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
 b.box("w4r3f", P, 14, F12, "gen/tools.just（最後寫）", 280)
 b.box("w5b", UO, 15, G12, "→ 0：重裝後相符（已 warn）", 230)
-b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/、印記（取件；暫存 → 整批替換）", 320)
-b.box("w4f", P, 16, F12, "cache/<repo>/、gen/<repo>.stamp（只寫不進 git 的）", 280)
-b.box("w4r0b", E, 17, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
-b.box("w4f2", P, 17, F12, "gen/tools.just（最後寫）", 280)
-b.box("w5c", UO, 17, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4r0", E, 16, SUB, "否（不驗）：從 /dist 寫 cache/<repo>/（暫存 → 整批替換）", 320)
+b.box("w4f", P, 16, F12, "cache/<repo>/（只寫不進 git 的）", 280)
+b.box("w4r0s", E, 17, v2(SUB), "寫印記 gen/<repo>.stamp（index digest + 每檔 sha256）", 320)
+b.box("w4fs", P, 17, F12, "gen/<repo>.stamp", 280)
+b.box("w4r0b", E, 18, v2(SUB), "最後原子重生 gen/tools.just（與 cache 同一 apply 內）", 320)
+b.box("w4f2", P, 18, F12, "gen/tools.just（最後寫）", 280)
+b.box("w5c", UO, 18, G12, "→ 0：成功、不起 pull（驗收 §7.4-17）", 230)
+b.box("w4fail", UO, 19, RULE, "任一寫入失敗匯流：回 1，保留可重建狀態，下次 sync 重做", 230)
 b.D("wf0", "w4x0", "w4x1", al=True); b.D("wf1", "w4x1", "w4p"); b.DL("wf2", "w4p", "w4l"); b.H("wf3t", "w4l", "w4lx", "逾時"); b.D("wf3", "w4l", "w4l2"); b.H("wf3x", "w4l2", "w4lx2", "≠"); b.D("wf4", "w4l2", "w4vq", al=True)
 b.D("wf5", "w4vq", "w4v", "是", al=True); b.D("wf6", "w4v", "w4v1q", al=True); b.D("wf6y", "w4v1q", "w4tq", "是", al=True); b.H("wf6t", "w4tq", "w5", "是"); b.D("wf6tn", "w4tq", "w4tr", "否", al=True); b.H("wf6tf", "w4tr", "w4trf", "寫"); b.H("wf6tz", "w4tr", "w5t")
 b.D("wf8", "w4r", "w4r2"); b.H("wf8f", "w4r", "w4rf", "寫"); b.H("wf8f2", "w4r2", "w4r2f", "寫"); b.D("wf8b", "w4r2", "w4v2"); b.D("wf9", "w4v2", "w4v2q", al=True); b.H("wf9x", "w4v2q", "w4v2x", "否"); b.D("wf9y", "w4v2q", "w4r3", "是", al=True); b.H("wf9f", "w4r3", "w4r3f", "寫"); b.DL("wf9z", "w4r3", "w5b")
-b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10b", "w4r0", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
+b.H("wf10", "w4r0", "w4f", "寫"); b.D("wf10s", "w4r0", "w4r0s"); b.H("wf10sf", "w4r0s", "w4fs", "寫"); b.D("wf10b", "w4r0s", "w4r0b"); b.H("wf10f", "w4r0b", "w4f2", "寫"); b.H("wf11", "w4r0b", "w5c")
 b.close()
 _A = F.abs
 # w4vq 否（不驗）→ w4r0：從菱形右側出、沿引擎欄與專案目錄欄之間（x=1300）下到 w4r0 上方縫隙、左到 w4r0 右側 0.9 再下進頂端（中間無 E→P 線）

tokens used
157,391
已完成修改並重產 [v1_a.drawio](<scratchpad>/v1_a.drawio) 與 [v1_c.drawio](<scratchpad>/v1_c.drawio)。

修改頁面：

- `v1p3`：名詞表由 16 條縮至 8 條。
- `v1p3b`：移除沿革便條；補強 vk-resolve 文法失敗規則；apply 結束碼改為 1 紅、2／3 橙。
- `v1p9c`：加入寫入／刪除共通失敗匯流。
- `v1p16`：`o3tx` 改為橙色需人處理終點。
- `v1p16c`：resolve 內補既有進度檔恢復與 6-27 語意。
- `v1p16cb`：拆開「寫 version.toml」與「刪 [progress]」；加入共通寫入失敗匯流。
- `v1p16cc`：修正 `we2a` 垂直對齊。
- `v1p16ccb`：修正 `we6q` 垂直對齊。
- `v1p16ccc`：拆開寫 cache 與寫印記及其檔案框；補共通寫入失敗匯流；修正 `wf6y` 對齊。

其餘指定頁現況已涵蓋附件項目，未作不必要改動。禁止修改的頁面及 `disc_v1_b.py`、產生器共用檔、檢查工具均未修改。

待處理便條：無。

驗證結果：

- `run_v1_a.py`：成功
- `run_v1_c.py`：成功
- 兩份 draw.io 的 overflow、overlap、cross、self、jog、align、margin-label：全部 0 筆／無問題
- 指定可修改頁的非 termcov lint：0
- 事件名稱、write-fail-edge、end-color-text、page-height、edge-font 等：0

整份 `v1_a.drawio` 仍有兩筆非 termcov lint，均位於明令不可改的頁面：

- `v1p1b`：`term-dup-page0`
- `v1p2b`：`term-count` 10 > 8

因此沒有違反「絕對不可改」限制去清除它們。工作目錄不是 Git repository，故無法依技能流程提交 commit 或執行以 Git fixed point 為基礎的雙軸 code review。
