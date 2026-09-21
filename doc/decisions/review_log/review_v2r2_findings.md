
## 契約 v2：工具 repo、啟動器↔引擎、CI: must_fix 10 / optional 0
- [內容一致性] p3_ens: 寫「會動 image 的動詞（add／upgrade／sync）走 ②③④；其他動詞沒有東西要拉，不經 ③」，但 p8 undev 流程是 resolve → docker pull／cp → apply（要拉鎖定版 image），p1 undev 列也寫「重新 materialize」。
- [內容一致性] p3L4（目錄樹）, d4_2, d4_7, p3_tk11: 目錄樹「src／dest／mode」、init.toml 框「[mode="copy"|"append"]」、工具 repo CI「mode 只能 copy|append」、名詞表「mode="append"」全部仍用 mode，應改 strategy。
- [顏色] s5: 「結束狀態 0／1／2 回到 just」框是紫底紫框，但本頁 legend 紫 = image／容器；結束狀態不是 image。
- [內容一致性] d1, p3_err: 契約④ 把「gen/.stamp = 引擎 ref？」比對放在啟動器（① grep 之後、② docker run resolve 之前），但 p6 sync 頁把同一個判斷畫在引擎泳道的 resolve sync 內（n3）；兩頁對「誰做這個判斷」不一致。且 p3 沒註明 upgrade vendor_kit／install 本身不被這一關擋（p1 有寫）。
- [顏色] s5、p3_lg4: s5 是執行結果／狀態，卻使用圖例代表 image／容器的紫色，應改用符合結果用途的樣式。
- [可讀性] s2: 協定說明使用 stdout、stderr，本頁名詞表未說明「給啟動器讀的輸出」與「診斷訊息」的差別。
- [內容一致性] p3_dist、d4_2、d4_7、p3_tk11: 仍使用 mode 欄位，應改為 strategy。
- [內容一致性] p3_pend、d4_1: dist symlink 仍列為待拍板，但 v2.2 E 已明定第一版禁止，且引擎展開時也要驗證。
- [內容一致性] d1、s1、p3_ens: 薄殼不符即退出的共通前置未畫出 install／upgrade vendor_kit 的修復例外，與 p1 p1B_r9c3 相反，照本頁執行會擋住提示使用者執行的修復指令。
- [內容一致性] p3_dry、k3f（對照 p7 b11y、p7b c_r7c2）: 本頁的 CI 預覽需要改 tracked 檔時回 1，後兩頁卻無條件標示 dry-run 回 0，必須補齊 CI 條件。

## 流程 v2：bootstrap.sh + install: must_fix 5 / optional 3
- [排版] a8f: 專案目錄的「＋version.local.toml（不進 git；記 image tag + image ID）」檔案框沒有任何線連到（a8 寫它卻沒有「寫」箭頭），懸空。
- [排版] a12: 紅橢圓「是 → 1：第一次 install 不留半成品；add 失敗 → 明列已完成／未完成」文字超出橢圓外框。
- [可讀性] a10、a10f: 使用 resolve/apply、baseline/metadata，本頁名詞表未完整說明這些階段與產物的用途。
- [內容一致性] a9、a10、ae12: install 後直接接到逐工具 add，失敗判斷卻在後面，應在 install 失敗時先中止，不能繼續接入工具。
- [內容一致性] i4、i4f: install 的產物未列出 gen/.stamp，但 p2 要求 install 建立包含薄殼 hash 的印記，後續修復比對也依賴它，應補入寫入結果。
  (opt) [內容一致性] i4f: install 寫入的檔案框只列 version.toml、薄殼四檔、baseline/，沒列 gen/.stamp；但 i4 說再跑要比對「hash 在 gen/.stamp」、p2 表 B 也寫 install 重生 gen/，第一次 install 若不寫 .stamp 就無從比對。
  (opt) [排版] ae9: 從 GHCR 引擎 image 回到「docker run <引擎> install」的線與 a8→a9 的線在 a9 上方同一點合流重疊，看起來像一條線。
  (opt) [可讀性] bA（標題）, bI（標題）, p5_tk3: 分組標題與名詞表重複提「取代 --repair」「不開 --repair」「不開 init」；p1 已有不開清單，這裡對第一次看的人只是多出不存在的名詞。

## 流程 v2：upgrade ── Renovate 路徑、手動路徑: must_fix 10 / optional 2
- [排版] be5: b4「有 baseline/？」→ b5 的「否」線從 b4 上緣往上折再往右，與 b2 → b4 的「否」線在 b4 上方重疊，兩個「否」擠在一起，看不出哪條線屬於哪個判斷。
- [排版] b2: 判斷菱形「(0) 衝突中檔案仍有我們的標籤 <<<<<<< vendor_kit:baseline？…」文字大幅超出菱形。
- [排版] b7: 白框「否：(2) 才查最新…」左緣壓在 b6 菱形的右頂點上，框與菱形重疊。
- [排版] a5: 紅橢圓「1：baseline 落後 version.toml → PR 紅，印「本機 just vendor_kit upgrade <repo> -y 後 push」」文字超出橢圓。
- [內容一致性] b15, b16: B 手動路徑從 materialize → 逐檔詢問 → 推 baseline → 寫 version.toml，沒有「重生 gen/tools.just」步驟；p2 表 B 寫 upgrade 對 gen/ 是「重生」，add 頁也有 c22；新版的 just/<ns>.just 可能增減，少了這步就對不上。
- [排版] b6、b7: 兩元件的水平範圍重疊 10px，應拉開判斷框與結果框。
- [可讀性] p7_tv4、b13、pend: 使用 flock、materialize、CRLF，本頁名詞表未完整解釋其意義。
- [內容一致性] b2: 在 resolve 階段寫出「清除衝突狀態」，但 resolve 不得寫檔，狀態清除應放到拿鎖並重驗後的 apply。
- [內容一致性] b15、b16: 更新 baseline 後直接寫版本／結束，沒有重生工具的 gen 定義，與 p2 upgrade 矩陣不一致，也未交代新版命名空間變動如何生效。
- [內容一致性] b11y: dry-run 無條件回 0，漏掉 p3 下游 CI「需要改 tracked 檔則回 1」的判定。
  (opt) [排版] b11y: 綠橢圓「0：唯讀預覽：印會問哪些檔（換／合併／append），不動」文字貼到橢圓邊。
  (opt) [排版] be18, be19: b12「CI=1 且無 -y 又需改檔？」的「是」「否」兩條線都從下頂點同一點出發再分開，「是」「否」標籤擠在同一處。

## 契約 v2：目的、角色、介面: must_fix 7 / optional 1
- [內容一致性] p1_pend: Q12 已定（init.toml 欄位名 strategy=copy|append），右上便條仍列為「待你回覆 (4)」且建議 mode = "append"；應改成已定並改用 strategy。
- [內容一致性] p1B_inv, p1_tv16: 不變量框「工具以 mode=append 宣告」與名詞表「mode="append"」仍用舊欄位名，應改為 strategy。
- [內容一致性] p1B_r6c3: upgrade 列寫「自身升級（不帶 repo 或 upgrade vendor_kit）→ 重產薄殼 + gen → 印請 commit = 1」，但 p7b E(a) 畫成不帶 repo 時只改 version.toml 第一行就停下、要求另跑 upgrade vendor_kit，且 p7b s14 結束狀態是 0；兩頁互相矛盾。另「細節見 p7、p8」頁碼錯（upgrade 在 p7／p7b，p8 是 dev）。
- [可讀性] p1B_r7c3、p1B_r5c3: 使用 image ID、VENDOR_KIT_REGISTRY_TOKEN，但本頁名詞表未解釋兩者的用途，不能只靠 RepoDigests 或 GHCR 的定義代替。
- [內容一致性] p1_pend、p1B_inv、p1_tv16: 仍使用 mode，且便條仍將欄位名列為待拍板，應依 Q12 改成已定的 strategy="copy"|"append"。
- [內容一致性] p1B_inv、p1B_r6c3（對照 p7b s2、p7b_tv9）: 本頁說不帶 repo 的 upgrade 當次重產薄殼，p7b 卻說只改引擎版本並要求另跑 upgrade vendor_kit，兩頁必須統一。
- [內容一致性] p1B_r6c4、p1_tv3: 將退出 1 一律解釋為「不動 version.toml」，與自身升級已改第一行、要求重跑而退出 1 的狀態衝突，應分開描述。
  (opt) [可讀性] p1_tv10, p1_tv12: 名詞表寫「v1 叫 ensure」「materialize（v1 叫 install）」；v2-only 圖沒有 v1 可對照，且 install 現在是對外動詞，第一次看的人會混淆。

## 契約 v2：專案裡的檔與 version.toml: must_fix 6 / optional 0
- [內容一致性] t_init, t_gi, p2_not, p2_tk12: init.toml 框「mode = "copy"|"append"」、.gitignore 框「mode=append」、不碰框、名詞表「mode="append"」仍用舊欄位名，應改 strategy。
- [可讀性] p2_tk8, p2_tk10, p2_not: 舊名詞殘留：「v1 叫 .<repo>/」「v1 叫 ensure」「v1 的 dev 會寫 exclude」；本圖已無 v1 頁，這些對照無處可查。
- [可讀性] t_just、t_entry、t_vj: 使用 just、recipe、mod/import? 等語法，但本頁名詞表未完整解釋這些載入與指令概念。
- [內容一致性] t_gi、t_init、p2_not、p2_tv12: 仍將初始檔策略寫成 mode，違反 Q12。
- [內容一致性] t_vl、p2_mx_r1c1、p2_mx_r1c2、p2_my_r1c1～p2_my_r1c3: uninstall 的說明／矩陣仍呈現直接刪除，應補上「只刪確認為自產且 hash 相符的檔；未知或被改的保留」，避免與 v2.2 E、p8b 的保留規則矛盾。
- [內容一致性] p2_my_r6c2、t_gstamp: 矩陣將 sync 對 gen 寫成「重生」，但 gen 包含本頁另限定由 install／自身 upgrade 寫入的 .stamp，應明確區分 tools.just 與薄殼產物印記。

## 架構圖 v2：主機、引擎模組、registry: must_fix 6 / optional 0
- [排版] mount_dist: 線上文字「掛載 /dist:ro」被主機分組框的右邊線直接壓過（字被線切）。
- [排版] w_ver, w_vl, w_repo, w_bl, w_user, w_shell, w_gen: 引擎模組→專案目錄的線上文字（讀寫、讀（覆寫）、整批替換、寫、建／append 問後合併、薄殼 just 檔、重生）都落在紫色容器框與黑色專案框的邊線上，字被邊線壓過。
- [顏色] g_note: 使用橘色規則框，但本頁底部圖例沒有對應的橘色意義。
- [內容一致性] h0h1_e、h1h2_e、h2h3_e、h3h4_e、g1g2_e: 架構頁仍包含載入／執行順序鏈，應移到流程頁，架構連線只保留模組間傳遞的資料。
- [內容一致性] f_shell: 把根 justfile 與 vendor_kit 自有薄殼放在同一類，模糊了「使用者檔只問後改一行」與「自有薄殼按 hash 重產」的權限差別。
- [內容一致性] g_note: 只以 cache 缺少作為拉取條件，漏掉鎖定 digest 改變及驗證失敗的情況，與 p6 的同步流程不一致。

## 流程 v2：add: must_fix 8 / optional 2
- [內容一致性] pend: 便條仍寫「待拍板 (4) 初始檔 mode="append" 在 init.toml 的欄位名」；Q12 已定為 strategy，應改為已定。
- [內容一致性] c18, p5b_tk5: 判斷菱形「mode="append"？」與名詞表「[mode="copy"|"append"]」仍用 mode，應改 strategy。
- [排版] c6: 綠橢圓「0：已接入且完成，無變更（-t 與鎖定不同 → 1…）」文字超出橢圓，「是」箭頭的箭頭壓到「0：」。
- [排版] c23x: 紅橢圓「失敗 → 1：明列已完成／未完成；version.toml 不動」文字超出橢圓外框。
- [顏色] c6: 同一綠色終點包含退出 1 的錯誤結果，與本頁「紅色＝錯誤終止」的圖例不一致，應拆開成功與錯誤結果。
- [可讀性] p5b_tv1、p5b_tv9: 名詞說明本身又使用未解釋的 stdout/stderr/eval、set/recipe，仍需以白話解釋或刪除不必要的實作詞。
- [內容一致性] pend、c18、p5b_tv5: 仍使用 mode，且欄位名仍作為待拍板內容，違反 Q12。
- [內容一致性] c2: 輸入指紋只列 version／metadata，漏掉將修改的使用者檔 hash，與 v2.2 C 及本頁 p5b_tv2 的完整指紋契約不一致。
  (opt) [可讀性] c6: 綠色終點（成功 0）裡混入「-t 與鎖定不同 → 1」的失敗結果，顏色與內容打架。
  (opt) [排版] ce35: c23 → version.toml 檔案框的「寫」線從 c23 頂端出發時緊貼 c23 右上角的 v2 標籤。

## 流程 v2：sync（每次 just 都跑）: must_fix 6 / optional 1
- [排版] n3n: 紅橢圓「1：印「vendor_kit 已更新 vX → vY，請 just vendor_kit upgrade vendor_kit」（不重寫薄殼）」文字超出橢圓，且線上文字「否」壓到橢圓內文字。
- [排版] z0、eB／m0: 第一階段只有「無需變更」的退出連線，沒有通往第二階段的「需要 materialize」連線，兩段流程未接起來。
- [可讀性] t0s: 工具覆寫分支使用 symlink，本頁名詞表未解釋它是指向本機目錄的連結。
- [內容一致性] t1y、te5、t2、t2n: cache 缺少或版本印記不同後仍走舊 cache 的 verify 分支，會把正常的首次建立／版本切換誤判為「被改過」，應與內容損壞的警告分支分開。
- [內容一致性] p6_tv8、m5: 名詞表說 gen 的 tools.just 與 .stamp 由引擎「每次重生」，但流程限制薄殼印記由 install／自身 upgrade 更新，且無變更有快路徑，兩處應統一。
- [內容一致性] eA、n3n: 「任何 just」遇薄殼不符都退出，未呈現 p1 明列的 install／upgrade vendor_kit 修復例外。
  (opt) [可讀性] eA（標題）, pend, p6_tk0: 分組標題、便條、名詞表三處寫「v1 叫 ensure」，舊名詞殘留，v2-only 圖無 v1 可對照。

## 流程 v2：upgrade ── 逐檔判斷、回退、自身升級: must_fix 12 / optional 0
- [內容一致性] c_r5c0: 逐檔判斷表「append 行（mode=append）」仍用 mode，應改 strategy。
- [內容一致性] uE（標題）, s2, s14: E(a) 畫成不帶 repo 的 upgrade 只改 version.toml 第一行就停下（薄殼不動）、要求另跑 (c)，與 p1 不變量「薄殼重產只由 upgrade vendor_kit（含不帶 repo 的 upgrade）／install 做」及 p1 upgrade 列矛盾；s14 結束狀態寫 0，p1／p3 寫「請 commit 並再跑原指令」= 1；標題「只由 upgrade vendor_kit 做」也漏了 install 修復。
- [排版] cx1: 判斷菱形「metadata 記有衝突中檔案且檔內仍有我們的標籤 <<<<<<< vendor_kit:baseline？」文字超出菱形。
- [排版] s3, s8, s14: 紅橢圓 s3、s8「1：統一提示「vendor_kit 已更新 vX → vY，請 just vendor_kit upgrade vendor_kit」」與綠橢圓 s14「0：印「請 commit .vendor_kit/ 並再跑原指令」」文字都超出橢圓。
- [排版] c_m、cx1、cx2: 合併／衝突處理元件落在 Renovate 或啟動器欄位，而非引擎欄位，未符合本輪「判斷邏輯全部在引擎泳道」的修正要求。
- [可讀性] s13、p7b_tv1、p7b_tv5: 使用 flock、apply，本頁名詞表卻只在其他定義裡再次使用，沒有解釋鎖與套用階段本身。
- [內容一致性] c_r5c0、p7b_tv6: 仍使用 mode=append，應改為 strategy=append。
- [內容一致性] s12、s13: 先比對薄殼 hash、再取得 flock，拿鎖後沒有重驗，無法符合 v2.2 C「鎖內重驗後才寫」的要求。
- [內容一致性] s11、s13: 先啟動目前鎖定的引擎，之後才查最新並改第一行，卻沒有取得／執行新引擎的步驟，不能由這條流程保證產出新引擎對應的薄殼。
- [內容一致性] s11（對照 p8 v9）: 此處固定讀 version.toml 並 pull，未呈現本機引擎覆寫優先且不得 pull 的分支，與 p8 用本機 image 執行自身重產的流程矛盾。
- [內容一致性] s14（對照 p1 p1B_r6c3）: 自身升級完成後本頁回 0、p1 回 1，應區分「實際換引擎後要求重跑」與「僅修復現有版本」，統一退出狀態。
- [內容一致性] p7b_tv4: 仍把所有退出 1 解釋為 version.toml 未動，與本頁 s2／s3 已改第一行後要求重跑的路徑矛盾。

## 流程 v2：dev / undev: must_fix 8 / optional 0
- [內容一致性] vB′（標題）: undev vendor_kit 分組標題寫「薄殼／gen 不符則重寫並統一提示」，違反 Q10 (2)（sync 不寫薄殼，只回 1 提示）；同組流程 w7 本身是對的，標題與流程打架。
- [排版] d2: 判斷菱形「CI=1？／<repo>不在 version.toml？／dist、init.toml 不合法？」三個問題塞一格，文字大幅超出菱形。
- [排版] d3, v9, w7, u6x: 橢圓文字超出外框：d3「是 → 1：CI 拒絕 dev／未接入…」、v9「打 upgrade vendor_kit（用該本機 image；比對 hash…）」、w7「否 → 1：提示 just vendor_kit upgrade vendor_kit（比對 hash 後重產薄殼 + gen）」、u6x「失敗 → 1：保留可恢復狀態」（且 u6x 溢出的字貼到 u6 藍框）。
- [排版] ue9: u6 → u6f 的線上文字「寫」被放在 GHCR 紫框「<repo>-dist@digest」的底邊上，字壓在框線上，且看起來像屬於 GHCR 框。
- [可讀性] vB、u4、u6: 流程使用 resolve/apply，但本頁名詞表未說明兩段各自做什麼。
- [內容一致性] vB′: 分組標題仍寫「薄殼／gen 不符則重寫並統一提示」，與 Q10(2) 及同區 w7 的「只提示 upgrade vendor_kit」矛盾。
- [內容一致性] u6: undev 的 apply 取得 flock 後直接刪覆寫與拆連結，漏掉輸入指紋重驗，與契約④的 apply 規則不一致。
- [內容一致性] d7、d7f: 先將 cache/<repo>/ 改成指向本機 dist 的 symlink，再寫其 .stamp，圖上路徑因此落到本機工具 dist，與唯讀掛載契約衝突，必須交代印記的獨立儲存位置。

## 流程 v2：remove / uninstall: must_fix 5 / optional 2
- [排版] x4x: 紅橢圓「任一工具失敗 → 1 中止，列出已完成部分」文字超出橢圓。
- [排版] x1: 「docker run <引擎> uninstall（-n → 唯讀預覽，覆蓋所有刪改與詢問）」的 v2 綠標籤蓋在文字「覆蓋」上。
- [可讀性] x8、pend: 使用 import、CRLF，本頁名詞表未解釋載入行與換行格式的意義。
- [內容一致性] x4 → m10 → x5: uninstall 先呼叫 remove 刪掉整個 baseline／cache，之後才做 hash 保護，已無法保留那些目錄裡的未知或被改檔案，保護檢查必須在刪除前生效。
- [內容一致性] m9、m10: 先修改 append 行、再刪除含 metadata 的 baseline、最後才改 version.toml，卻未呈現可存活到操作完成的進度日誌，與 v2.2 C 的失敗後可恢復契約不一致。
  (opt) [可讀性] x5f: 檔案框「－.vendor_kit/（自產檔）；初始檔留著使用者 .gitignore：除非…」兩句黏在一起沒有分隔，讀起來像「初始檔留著使用者的 .gitignore」。
  (opt) [可讀性] vC（標題）, p8b_tk5: 分組標題與名詞表提「不開 --purge」，舊名詞殘留（p1 不開清單已有）。

TOTAL must_fix 83; rejected 2