# 第十一輪（三階段 v2，20 分鐘）must_fix 49，optional 90，rejected 5

## 11 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install: must_fix 1 / optional 2
- [內容一致性] a0l: 順序與 spec 相反：a0l（建 log/bootstrap/ 並寫 launcher_start）畫在 a1「是 git repo？」與 a3「just ≥ 1.33.0？」之前；interface_spec §1.2 bootstrap.sh 列（v2.13 P4）與 §9.1 P4 明寫順序 = 驗 git repo／just → mkdir log/bootstrap/ → trace_id → launcher_start → pull／install，且 §1.1 --local 亦寫「前置檢查一律先做」；照圖會在非 git 目錄先建 .vendor_kit/log/。  (內容與連接 1/4)
  (opt) [內容一致性] a8d: 缺分支：「旁檔缺 → 1」只寫在括號裡，沒有紅色終點（本輪對離線包(1) 已補紅出口，此頁同一判斷仍無）。  (內容與連接 1/4)
  (opt) [排版] ae8n: 「是：值含 / 或以 .tar 結尾？」的 否 線垂直段在 x=522，緊貼「docker load」「tar 形才讀 .digest」「docker image inspect 取 image ID」三格右緣（相距 12px），縮圖下像是沿框邊畫、看不出是獨立線  (排版 1/4)

## 13 流程 v2：install（1）薄殼: must_fix 1 / optional 4
- [內容一致性] i2: 誰做／順序錯：i2「是 git repo？」與 i2n「上層或下層已有 .vendor_kit/？」接在 i1 docker run → i1e engine_start 之後（引擎內）；spec §0 git 列明寫 git 檢查在主機側（git rev-parse）、引擎不讀 .git，且引擎只掛 /repo 看不到上層目錄，巢狀檢查無法在容器內做；兩個判斷應在啟動器 docker run 之前。  (內容與連接 1/4)
  (opt) [lint] i4_5: onething：一格產兩個檔（config.toml 與其 baseline 副本），依「一格一件事」應拆兩格。  (內容與連接 1/4)
  (opt) [內容一致性] i1e: install 是單段動詞，engine_start 失敗註記寫「不進 resolve」是從兩段頁複製來的；spec §3.2 單段為「不做任何動作」。  (內容與連接 1/4)
  (opt) [內容一致性] i4_5: 「產 config.toml 與其 baseline 副本到暫存」一格產兩個檔，依一格一件事應拆成 config.toml 一格、baseline 副本一格  (排版 1/4)
  (opt) [lint] i4_5: onething：同頁其餘薄殼檔一檔一格（i4、i4_2、i4_3、i4_3b、i4_4），這格卻產兩個檔（config.toml 與其 baseline 副本）。建議拆成「產 config.toml 到暫存（含註解與預設；已有 → 不產、不動）」與「產 baseline/vendor_kit/config.toml 副本到暫存」；若視為同一範本的兩份輸出可保留，由使用者定。  (一格一事判定)

## 15 流程 v2：add（1）resolve → docker: must_fix 2 / optional 3
- [內容一致性] c2pq: 順序錯：c2b 查 registry → c2pq「私有 image 且未指定 @<tag> 且無憑證？→ 1 + 6-3」畫在 c4「已接入？」／c5「完成標記？」之前；spec §1.2 add 前置檢查順序是「已接入且完成 → 0 無變更」優先，照圖已接入且完成的私有工具重跑 add（無 token）會回 1 + 6-3 而不是 0，結果不同。  (內容與連接 1/4)
- [lint] c2d: onething：「產生輸入指紋」與「計畫＋指紋以 stdout 回啟動器」是兩個獨立動作（算 → 送）。建議拆成「產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）」與「stdout vk-resolve/1：計畫＋指紋回啟動器」，比照 prune 頁 q3／q5 的拆法。  (一格一事判定)
  (opt) [可讀性] c1: docker run resolve 格的括號塞了另一件事（--local：docker load + 讀 .digest，這是啟動器主機動作），且「值不是存在的 .tar → 1 + 6-24」無出口；一格一件事。  (內容與連接 1/4)
  (opt) [排版] ce10: 「已接入 <repo>？」的 否 線垂直段 x=990 與「否：續作」框 (c8) 右緣只差 10px，且 c8 出線隨即併入同一垂直線，縮圖下像 否 線穿過 c8  (排版 1/4)
  (opt) [內容一致性] c2d: 「產生輸入指紋 … → 計畫＋指紋以 stdout 回啟動器」一格兩個動作（算指紋、stdout 回傳），可拆兩格  (排版 1/4)

## 14 流程 v2：install（2）根 justfile 與 .dockerignore: must_fix 2 / optional 3
- [內容一致性] ignf: 標「逐字」的 .dockerignore 四行順序為 cache/、gen/、log/、.tmp.*，與 spec §1.2 install／6-34 及 p2（t_di、p2_di）的 cache/、gen/、.tmp.*、log/ 不一致；igyf 同。  (內容與連接 1/4)
- [內容一致性] igz: 兩個成功終點「0：印結果（建了／已含）」(igz) 與「0：不寫 .dockerignore；印指示」(igx) 直接從 idlz／idl 出去，未經過頁尾「結束前：寫 log_prune、launcher_exit」(ixl)；該格自稱「每個結束碼都寫」且本輪要求每頁尾 launcher_exit，此頁三個 0 出口只有一個接到它，順序缺分支  (排版 1/4)
  (opt) [內容一致性] igz: 三個 0 終點中 igz（建了／已含）與 igx（拒絕不寫）都不經 ixl（log_prune／launcher_exit），只有 iz 那條有；本輪規則是頁尾一格 launcher_exit 且每個結束碼都寫。  (內容與連接 1/4)
  (opt) [內容一致性] i6: 缺分支：spec §1.2 install 詢問點「根檔是 symlink → 不寫、印一次性遷移指示」在根 justfile／.dockerignore 判斷裡都沒有出口。  (內容與連接 1/4)
  (opt) [排版] ie13: 「無：建 justfile」回到「印 justfile 結果」的線在 y=248 橫越頁面頂端，與跨頁入口虛線橢圓 i5e 頂緣（y=258）只差 10px，縮圖下像壓到橢圓  (排版 1/4)

## 04 契約 v2：目錄樹與檔案範例: must_fix 1 / optional 0
- [內容一致性] t_bl: 目錄樹缺 baseline/vendor_kit/config.toml（config.toml 的 baseline 副本，spec §4.0／§4.9、v2.13 P10；install(1) 頁 i4f_6 有寫它）；t_bl 說明的 .vendor_kit.toml 也只寫 .dockerignore append 記錄，未含 config.toml 的 metadata（§4.9）。  (內容與連接 1/4)

## 12 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add: must_fix 0 / optional 2
  (opt) [內容一致性] a10re: 本頁 resolve 段（a10r／a10re）與 apply 段（a10a／a10ae）都沒有 engine_start 格；本輪規則是每頁 resolve／apply 段各一格（若以引用 add 頁承載，格內未明說）。  (內容與連接 1/4)
  (opt) [內容一致性] a13l: 「結束前：寫 log_prune、launcher_exit」一格兩件事；且紅色「是 → 1：立即中止」(a12) 直接離開未經此格，與格內「每個結束碼都寫」矛盾（v1p5cc ixl 同款寫法，同樣兩件事）  (排版 1/4)

## 08 契約 v2：啟動器 ↔ 引擎契約④: must_fix 1 / optional 7
- [lint] s4x: onething：一格混了兩個角色的兩個動作（引擎結束寫 engine_exit；啟動器結束寫 log_prune、launcher_exit）。同頁已把 append engine_start 獨立成 s2z，這格應比照拆成「④′ 引擎結束 append engine_exit」與「啟動器結束前 log_prune、launcher_exit（best-effort）」兩格。  (一格一事判定)
  (opt) [內容一致性] s4: ④ apply 段沒有 engine_start 格（只有 ② resolve 段的 s2z 與規則框 p3_lock 文字）；本輪規則是 resolve／apply 段各一格。  (內容與連接 1/4)
  (opt) [顏色] s4x: 白格（啟動器）內混入引擎事件 engine_exit（藍＝引擎、白＝啟動器），且一格三件事（engine_exit、log_prune、launcher_exit）；已接受的頁尾格只含 launcher_exit／log_prune。  (內容與連接 1/4)
  (opt) [內容一致性] p3_run: docker run 參數寫 -e TRACEPARENT=<trace_id>；spec §5 TRACEPARENT 是 W3C 格式 00-<trace_id>-<span_id>-<flags>，引擎只取其中 trace_id；契約頁應照 spec 寫。  (內容與連接 1/4)
  (opt) [內容一致性] s3b: ③ 主機 docker 段的 docker pull 只在括號寫「逾時 → 1 印 6-31」，pull 失敗（6-24）沒有終點；本輪已對 sync(1′)／工具 image pull 補紅出口，此頁同一步驟仍無。  (內容與連接 1/4)
  (opt) [內容一致性] p3b_tv0: 名詞「啟動器」說明結尾「最小單元見紅粗框」是架構圖 p4 的句子，本頁沒有紅粗框（fills 無 #f8cecc）。  (內容與連接 1/4)
  (opt) [lint] s2a: termcov：s2a 用到「frozen」、s1 用到 version.local.toml、d1 用到 gen/.stamp、p3_envw 用到「進度日誌」，本頁名詞表都沒有對應條（非工程師看不懂）。  (內容與連接 1/4)
  (opt) [內容一致性] s4x: ④′ 一格放三個事件（engine_exit、log_prune、launcher_exit），依「一格一件事」應拆為引擎結束一格、啟動器結束（log_prune）一格、launcher_exit 一格  (排版 1/4)

## 09 契約 v2：CI 契約⑤ 與驗收矩陣: must_fix 2 / optional 3
- [排版] k3g_e: 「衝突」線從 ③ upgrade --dry-run 右下角出來後沿 y=245 橫走到右邊橢圓，標籤「衝突」落在 ④ 工具測試 框正下方，縮圖下讀成「④ → 仍有衝突標記 → 2」；標籤應貼回 ③ 的出口或線改由 ③ 正下方走  (排版 1/4)
- [lint] rn4: onething：本頁小標寫「每格一步」，但 rn4 是三個連續動作（upgrade <repo> -y → commit → push）。建議拆成「維護者在 PR 分支本機 upgrade <repo> -y」與「commit + push 到 PR 分支」兩格。  (一格一事判定)
  (opt) [內容一致性] k2: 缺分支：② verify（spec §7.1 失敗 → 1）、④ 工具測試、⑤ 專案測試（原碼傳出）都沒有失敗出口，只有 ⓪①③ 有；規則框說「一關過才下一關」但圖上這三關看起來不會失敗。  (內容與連接 1/4)
  (opt) [內容一致性] p3_jm: 「驗收 §7.4 條 1–13、29–35 缺任一不得出貨」與 spec §8-12「條 1–13 缺任一不得出貨」不同（圖多列 29–35）。  (內容與連接 1/4)
  (opt) [lint] p3_accb_r10c2: termcov：驗收表用到「進度日誌」「metadata」「config.toml」「log/」，本頁名詞表沒有對應條。  (內容與連接 1/4)

## 10 架構圖 v2: must_fix 0 / optional 5
  (opt) [內容一致性] q_reg: registry 模組只有一條「tag／digest」箭頭到工具 image g_dist；update（不帶 repo 含 vendor_kit）與 upgrade 也查引擎 image 的 tag（spec §1.2 update／upgrade），缺到 g_eng 的資料流。  (內容與連接 1/4)
  (opt) [可讀性] w_log_l: 架構圖線上文字很長且描述順序（「先寫 launcher_start 才開始、結束 log_prune／launcher_exit」）；架構圖只該標傳的資料，順序歸流程頁（p4_np 自己也這麼寫）。  (內容與連接 1/4)
  (opt) [顏色] p4_tv0: 名詞「引擎」寫「8 個模組見紫色容器」，但圖例紫 = image（引擎與工具）、紅 = 引擎模組；若引擎容器帶 p4E 底色是紫，紫就有兩個意思。  (內容與連接 1/4)
  (opt) [排版] w_log_l: 「↓ 下線：launcher_* 事件」與「↑ 上線：keep 正規行」兩條線的垂直段分別在 x=22 與 x=30，只隔 8px 並排貫穿整頁高度（y≈254→1700），縮圖下成一條粗雙線、分不出誰進誰出  (排版 1/4)
  (opt) [內容一致性] h4: 啟動器方塊標題寫「先寫 launcher_start 才開始」，責任單元列有 launcher_exit、log prune 卻沒有 launcher_start 單元  (排版 1/4)

## 16 流程 v2：add（1′）apply 前置: must_fix 1 / optional 1
- [內容一致性] c11x／c12x／c12bx／c14x／c13y: 本頁五個終點（指紋不同、dest 不合法、撞名、frozen 清單、dry-run 預覽 0）都直接結束，整頁沒有「結束前：寫 log_prune、launcher_exit」格；spec §1.2 通則（v2.14-2）要求每頁頁尾一格，同組的 add（2）c24l、sync（1′）z2l、sync（2）m7l 都有，本頁缺  (內容與連接 2/4)
  (opt) [內容一致性] c13z（否 ↓ 續「add（2）」頁）: 本頁四個出口（c12x／c12bx／c14x → 1、c13y → 0）直接結束，沒有 spec §1.2「頁尾一格 launcher_exit／log_prune」；只有 add(2) 的成功路徑畫了，早退出口沒交代（sync(1)、B(1) 同型）  (排版 2/4)

## 22 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker: must_fix 2 / optional 2
- [內容一致性] b1x／b2c／b5／b8px: 四個終點（先 undev、先解衝突 2、無 baseline、pull 失敗）都直接結束，整頁沒有 launcher_exit／log_prune 格（只在名詞表提到）；與 spec §1.2 通則「頁尾一格 launcher_exit／log_prune」及同組其他頁不一致  (內容與連接 2/4)
- [內容一致性] b7c: 「(2) 查 registry 最新正式版」只有一條出線到 b7s；spec §1.2／§6 6-3：update／upgrade／add 無 registry 憑證且未指定 @<tag> → 1 + 6-3，add（1）頁已畫 c2pq→c2px 這條橙色出口，upgrade B（1）的查詢失敗沒有終點  (內容與連接 2/4)
  (opt) [可讀性] b8p: 「無：docker pull」70×63 小格三行字擠，同頁其他啟動器格都 240 寬  (排版 2/4)
  (opt) [排版] be9／be9t／be9z 共用的 x=1110 直線: 三個「是：目標版…」藍格右邊（1100）與匯流直線只差 10px，縮圖看起來線黏在框上  (排版 2/4)

## 23 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置: must_fix 1 / optional 1
- [內容一致性] b10x／b10dx／b10nx／b12x／b11y: 五個終點（指紋不同、dest 不合法、撞名、frozen 清單、dry-run 預覽 0）都直接結束，整頁沒有 launcher_exit／log_prune 格；spec §1.2 通則要求每頁頁尾一格  (內容與連接 2/4)
  (opt) [可讀性] b10d／b10n: b10d 寫「規則同「add（1）」頁」，但 dest 規則框 c12r 與命名空間規則框 c12br 在 add（1′）頁（v1p5bcc），add（1）頁沒有；且本頁用到「dest 合法」「命名空間撞名」兩個專有名詞，本頁名詞表沒有對應條目（add 三頁都有 dest 撞名／命名空間撞名條）  (內容與連接 2/4)

## 18 流程 v2：sync（1）啟動器快路徑: must_fix 1 / optional 5
- [排版] ne5pv（n1p → n1v）／n1v 的 v2 綠標: docker pull 格接回「覆寫中且 .Id ≠ 記的 image ID？」的水平線段（y≈917）正好被該菱形右上角的 v2 綠標蓋住，縮圖下線像斷在綠標上、看不出接到哪裡  (排版 2/4)
  (opt) [內容一致性] n3n／n1x／nql: 只有快路徑 nql 寫 launcher_exit（且漏 log_prune，spec §4.10 每次呼叫 trap 內都 prune），n3n（6-1 → 1）與 n1x（拉不到 → 1）兩個終點沒有經過任何 launcher_exit／log_prune 格  (內容與連接 2/4)
  (opt) [內容一致性] n3: 「gen/.stamp 的引擎 ref ＝ 第一行？」否 → 1 印 6-1；spec §4.4／§6 6-1：fresh clone（CI 最常見情況）缺 gen/.stamp 時改用薄殼自描述首行的 engine=<vX> 判定，圖上沒有這條，照圖讀 fresh clone 一律回 1  (內容與連接 2/4)
  (opt) [內容一致性] n1: 「grep version.toml 第一行取引擎 ref」與名詞 p6_tv7「引擎 ref = version.toml 第一行」：spec §4.1 明寫「第一行只是 install 寫出慣例、不是契約」，啟動器是以 vendor_kit 正規行 regex 取、命中數須恰 1  (內容與連接 2/4)
  (opt) [內容一致性] nql: 快路徑格只寫 sync_fast_path、launcher_exit，沒有 log_prune；spec §4.10 說每次呼叫結束 trap 內都 prune，其他頁頁尾格都是「寫 log_prune、launcher_exit」，表現法不一致（且一格兩個事件）  (排版 2/4)
  (opt) [可讀性] n1p: 「無：docker pull <引擎 ref>」80×79 小格塞四行字，縮圖下擠；sync(2) 同型 m0p 是 100 寬單行  (排版 2/4)

## 25 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入: must_fix 1 / optional 1
- [排版] be28（b16q → b17l）的「否」標籤: 「有衝突？」左尖到「結束前：寫 log_prune、launcher_exit」右邊只有 20px，「否」字擠在箭頭與該格 v2 綠標之間、壓在箭桿上  (排版 2/4)
  (opt) [內容一致性] b17l: launcher_exit／log_prune 格只掛在 b16q「有衝突？」的否分支上，是分支（b18 → 2）直接結束沒經過它；spec §4.10 每個結束碼都寫，格子放在 b16q 之前或兩支共用才合理（add（2）c23x 紅出口同樣繞過 c24l）  (內容與連接 2/4)

## 24 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併: must_fix 0 / optional 4
  (opt) [可讀性] b14y／b14m: bl 說「逐檔」，但五個情況菱形＋同意菱形只走一次就進 b14m「暫存合併完成」，沒有像 add（2）c20l「還有下一個 [[file]]？」的迴圈菱形接回 b14q1，讀者看不出每檔都要跑一遍  (內容與連接 2/4)
  (opt) [可讀性] b14pc: 「是：留原檔、記 conflicts」90×63 小格三行字擠，與菱形左尖只隔 30px、「是」字塞在中間  (排版 2/4)
  (opt) [內容一致性] bl（↓ 逐檔 …）: 逐檔迴圈只用文字說明，沒有 add(2) 那樣的「還有下一個檔？」菱形回圈；兩頁同型流程表現法不一致  (排版 2/4)
  (opt) [lint] b14n: onething：「不動該檔」之外還寫了「記 declined_hash／state=declined」，而 metadata 的寫入其實在「（2′）收尾寫入」頁 b15d 才做，這格等於兩件事又重複。建議這格只留「否：不動該檔（拒絕結果留到寫 metadata 那步記）」，declined_hash／state=declined 保留在 b15d。  (一格一事判定)

## 21 流程 v2：upgrade ── A. Renovate 路徑: must_fix 0 / optional 2
  (opt) [lint] p7_tk9: term-diff：「metadata」條在 upgrade 九頁（v1p7～v1p7bccc）與契約頁 v1p1／v1p2b 的說明文不同（一邊列 schema + written_by、local_image_id、conflicts，一邊列完成標記、每個 dest 的 state），本輪宣稱名詞表已統一但此條仍分兩版  (內容與連接 2/4)
  (opt) [排版] ae9（a7 → a8）的「綠」標籤: 「綠」字落在 push→「PR 分支 CI 再跑」那條線下方、a7 左側，離自己的線轉角遠，容易讀成 push 線的標籤  (排版 2/4)

## 29 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）: must_fix 3 / optional 2
- [內容一致性] s13: E(c)(2) 由 s12e「否」直接進 s13 重產薄殼，沒有先建 .tmp.upgrade.<id>.toml；spec §0 進度日誌／§1.2 upgrade (b)「否 → 建 .tmp.upgrade.<id>.toml → 用現引擎重產薄殼 → 刪日誌」／G2 明定不設例外，s13d 的「有的話」也印證從 E(c)(1) s12vz／s12fz 進來時沒有日誌  (內容與連接 3/4)
- [排版] se18x: 「重生 gen/tools.just」的「失敗」直線（x≈880）往下到菱形 s13q 時，穿過「刪進度日誌」→「－.tmp.upgrade 日誌」的「刪」水平線（y≈900），兩線交叉；把菱形移到左側或讓失敗線繞過刪線  (排版 3/4)
- [lint] s13g: onething：一格內是判斷＋兩個不同動作（config.toml 缺則建；有則三方合併）。建議拆成菱形「config.toml 存在？」→ 否「建 config.toml（新版範本）」／是「三方合併 config.toml（B=baseline 副本、D=現況、N=新版範本；要改先問 6-22，-y 免問）」。  (一格一事判定)
  (opt) [可讀性] s13q: 失敗出口（se18x）只從 s13c 接出，s13 重產薄殼／s13g config.toml／s13b gen/.stamp 失敗沒有出路；其他頁用「失敗（任一步）」  (內容與連接 3/4)
  (opt) [內容一致性] s13g: 「config.toml：缺則建；有則三方合併（B/D/N…要改先問 6-22）」一格含判斷＋兩種動作，違反一格一件事；可拆成「config.toml 已存在？」菱形＋「建」／「三方合併」兩格  (排版 3/4)

## 27 流程 v2：upgrade ── E. 自身升級 (a)(b): must_fix 2 / optional 1
- [內容一致性] s2ln: 順序錯：新引擎 inspect／pull（s2ln、s2lp、s2lv）畫在舊引擎 apply 改完第一行（s2e）之後；spec §3.3 `pull|vendor_kit`／`engine` 記錄由啟動器在 docker 階段、apply 之前先 pull（或覆寫時驗 ID），apply 後才依 §3.4 接手  (內容與連接 3/4)
- [內容一致性] s2hx: 全頁沒有 launcher_exit／log_prune 格：s2hx、s2lx、s8 三個終點都在本頁結束，卻沒有頁尾格（v2.14-2 每頁表現法；其他頁如 v1p8 d8l 都有）  (內容與連接 3/4)
  (opt) [內容一致性] s2a: 缺分支：「含 dev 中工具 → 1 提示 undev」只寫在格內沒有終點；同樣的判斷在 v1p8b 畫成菱形 m4 ＋ 橙出口 m5  (內容與連接 3/4)

## 32 流程 v2：undev <repo>: must_fix 1 / optional 0
- [內容一致性] u6x: 「下次任何動詞先恢復」與 spec 矛盾：唯讀動詞只偵測不恢復（sync／update 印 6-33 結束 1、help 仍 0），只有可寫動詞先恢復；同組 v1p8cc w2x 寫的是「可寫動詞」  (內容與連接 3/4)

## 35 流程 v2：remove（2）寫入段: must_fix 2 / optional 0
- [內容一致性] m9m2: append 行以整組「唯一命中 → 刪／零命中 → 不刪／多處 → 保留」判定（m9m、m9m2、note m9mn），spec §1.2 uninstall（v2.9-5）與 §7.4-19 為逐行比對、只刪仍與紀錄原文相同的行、缺失／被改的行跳過並 warn（不是全有／全無），§1.2 remove 亦「只刪原文相同的」  (內容與連接 3/4)
- [排版] me12n: 「metadata 有 append 過的行？」的「無」線與「同意？」的「否」線兩條垂直線只隔 10px 並排下到「刪 baseline」，「否」標籤壓在「無」線上；兩線間距拉開或把標籤改放菱形出口旁  (排版 3/4)

## 33 流程 v2：undev vendor_kit: must_fix 2 / optional 0
- [內容一致性] w5p: 缺分支：「下次 just」段的 docker pull 該引擎沒有失敗／逾時紅出口（本輪規則 pull 一律紅出口；同組 v1p8c u5p 有 u5px，v1p7bcc s11p 有 s11x）  (內容與連接 3/4)
- [內容一致性] w5p: 「無：docker pull 該引擎」沒有「失敗」紅出口，與 E(a)(b)／E(c)(1)／undev <repo> 同款 pull 格（都有 失敗／逾時 → 1 紅色終點）不一致，缺分支  (排版 3/4)

## 26 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退: must_fix 2 / optional 5
- [內容一致性] d1a: D 回退段兩個引擎容器（d1a resolve sync、d1f apply sync）都沒有 engine_start 格，頁尾也沒有 launcher_exit／log_prune 格；v2.14-2 每頁 resolve／apply 段各一格 engine_start、頁尾一格 launcher_exit，本頁名詞 tv12 自己也這樣寫  (內容與連接 3/4)
- [內容一致性] d1a: D. 回退段「docker run 引擎 resolve sync」與「docker run … apply sync」後都沒有 engine_start 格，且流程在「寫印記 gen/<repo>.stamp」（d2c3）就停住，沒有 launcher_exit／log_prune 也沒有終點；本頁 resolve／apply 段是唯一沒補這兩格的  (排版 3/4)
  (opt) [內容一致性] cx1: 缺分支：「衝突檔仍含我們的標籤？」否 → 直接清除衝突狀態；spec（與本頁 tv6）「檔案失蹤不算已解」，檔案不見時圖上會走「否」  (內容與連接 3/4)
  (opt) [排版] d3b: 一個檔案框放三個檔（初始檔、baseline/<repo>/、version.toml），違反一格一個檔案；其他頁用檔案群組（如 v1p7bccc s13f）拆開  (內容與連接 3/4)
  (opt) [可讀性] cx3: C′ 的「否」分支終點是無框純文字（「否 ↓ apply 拿鎖、建日誌後清除衝突狀態 → 接 B(1)」），既不是白格也不是綠／虛線橢圓，看起來像懸空標籤；且一句含拿鎖、建日誌、清除三件事，建議改成跨頁入口橢圓只寫「→ 接 B(1) 頁」  (排版 3/4)
  (opt) [可讀性] d1p: 「無：docker pull」白格太小，三個字一行折成三行（無：／docker／pull），縮圖下難讀；加寬到與其他步驟格同寬  (排版 3/4)
  (opt) [lint] c_m: onething：「三份比對逐檔判斷」與「要改的先問（-y 免問）」是兩個動作，且括號內又塞了拒絕後的處理。此格是左表的總說明格，若要留作概述可接受；否則拆成「引擎 merge 模組：三份比對、逐檔判斷（左表）」與「要改的先問（-y 免問；拒絕 → 不動）」兩格。  (一格一事判定)

## 28 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）: must_fix 1 / optional 6
- [lint] s12h: onething：一格內有動作（apply 前後 grep 第一行）＋判斷（變了？）＋動作（用新引擎再跑 upgrade vendor_kit）。建議比照「E(a)(b)」頁 s2h／s2h2 的畫法拆成「apply 後 grep version.toml 第一行」→ 菱形「第一行變了？」→「是：用新引擎再跑 upgrade vendor_kit」三格。  (一格一事判定)
  (opt) [lint] s12h: onething：一格三件事（apply 前後 grep 第一行、判斷「變了」、用新引擎再跑），「未變」沒有出路；E(a)(b) 頁同一邏輯拆成 s2h／s2h2／s2hx 三格且有紅出口  (內容與連接 3/4)
  (opt) [內容一致性] s12hz: 缺分支：E(c) 續跑由 s12hz → s10a 直接進 s11r，跳過新引擎 inspect／pull；「新引擎拉不到／ID 不符 → 1 + 6-2b」的出口只存在於 E(a)(b) 頁，本頁只用文字「接手邏輯同 E(a)(b) 頁」帶過  (內容與連接 3/4)
  (opt) [內容一致性] s11x: 頁尾沒有 launcher_exit／log_prune 格：s11x、s12bx、s12sx、s12dx 四個終點在本頁結束，尾格只畫在 E(c)(2) 頁 s14l  (內容與連接 3/4)
  (opt) [內容一致性] s12f: frozen 菱形排在「指定 @<tag>？」之前，frozen 且指定 @<tag> 時一律走 frozen 分支；spec §1.2 (b)／§3.4 措辭是「frozen 且未指定 → 目標 = 現 ref」，frozen＋@tag 的結果與 spec 字面不一致  (內容與連接 3/4)
  (opt) [可讀性] 是：不查 registry、不改第一行 → 續「E(c)（2）」頁: CI 為真 的「是」分支與「目標引擎 ref ≠ 現 ref？」的「否」分支都是無框粗體文字當終點，而同頁左側「續跑」用虛線綠橢圓，跨頁出口樣式不一致  (排版 3/4)
  (opt) [排版] 續跑：新引擎回到本頁「docker run 該引擎」格再跑一次: 「續跑」橢圓回到「來自 E(a)(b)」入口的回路線貼著頁面最左邊（x≈13）往上跑，緊貼「否 → 1：薄殼被改過」「是 → 3」兩個橙色橢圓左緣，縮圖下像切到橢圓；建議把回路線往內縮或把兩個橙橢圓右移  (排版 3/4)

## 34 流程 v2：remove（1）resolve → apply 前置: must_fix 1 / optional 2
- [lint] m6d: onething：「產生輸入指紋」與「計畫＋指紋以 stdout 回啟動器」是兩個動作。建議拆成「產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）」與「stdout vk-resolve/1：計畫＋指紋回啟動器」。  (一格一事判定)
  (opt) [內容一致性] m3: 頁尾沒有 launcher_exit／log_prune 格：m3、m5、m9x、m7cx、m7y 五個終點在本頁結束，尾格只畫在 remove（2）頁 m11l  (內容與連接 3/4)
  (opt) [內容一致性] p8b_tv4: 名詞表「install 只建 baseline/.gitkeep（metadata 到 add 才建）」與 v2.13 P10（install 建 baseline/vendor_kit/config.toml 副本、metadata 記於 baseline/.vendor_kit.toml）及同頁 tv12 矛盾  (內容與連接 3/4)

## 31 流程 v2：dev vendor_kit: must_fix 0 / optional 4
  (opt) [內容一致性] v6c: 「下次 just」段 docker run resolve sync 之後沒有 engine_start 格，該段 v8／v6x／v10 也沒有 launcher_exit；同一狀況見 v1p8cc w5c  (內容與連接 3/4)
  (opt) [內容一致性] v1i: 缺分支：「本機無此 image → 1」只寫在格內沒有終點；E(c)(1) 同一判斷畫成菱形 s11n／s11v ＋ 紅出口 s11x  (內容與連接 3/4)
  (opt) [可讀性] v8: 橙終點 v8 還有出線（ve10）到另一個橙終點 v9，一個結束畫成兩格；終點不該有出邊  (內容與連接 3/4)
  (opt) [內容一致性] v8: 橙色終點「否 → 1：vendor_kit 已更新，請執行 upgrade vendor_kit」又接一條線到另一個橙色終點「需人動作：打 just vendor_kit upgrade vendor_kit」，終點帶出線且兩格內容重複；合併成一格  (排版 3/4)

## 30 流程 v2：dev <repo>: must_fix 0 / optional 1
  (opt) [內容一致性] d1e: dev 是單段動詞、沒有 resolve 段，engine_start 格卻寫「不進 resolve」（spec §3.2 為「不做任何動作」）；本頁其餘流程未發現問題  (內容與連接 3/4)

## 38 流程 v2：prune: must_fix 3 / optional 1
- [內容一致性] q1, q12, q14: v2.14-2／spec §1.2 通則規定每頁 resolve 段與 apply 段各一格「append engine_start（失敗 → 1 + 6-38）」、頁尾一格 launcher_exit／log_prune：本頁 q1（docker run resolve prune）後直接 q2、q12（docker run apply prune）後直接 q12a flock，兩處都沒有 engine_start 格；q13x／q14 結束前也沒有 launcher_exit 格；q0 的 launcher_start 只塞在括號裡，不像 uninstall(1) x0l 獨立成格  (內容與連接 4/4)
- [內容一致性] q2: resolve 段（q1 docker run resolve prune → q2）與 apply 段（q12 docker run apply prune → q12a）都沒有「append engine_start」格；spec §1.2 通則要求每頁 resolve／apply 段各一格，prune 頁本輪未補  (排版 4/4)
- [內容一致性] q14: 頁尾（q13 有刪除失敗？→ q13x／q14）沒有「log_prune／launcher_exit」格，起點卻寫「已寫 launcher_start」，與其他動詞頁及 spec 圖面表現法不一致  (排版 4/4)
  (opt) [lint] q12a: termcov：q12a 用到 6-26（flock 逾時），本頁名詞表 p9_tv8 的 6-N 清單沒列 6-26  (內容與連接 4/4)

## 39 流程 v2：update: must_fix 4 / optional 1
- [內容一致性] u1r, u13: v2.14-2：單段動詞的引擎容器也要先 append engine_start；u1r（docker run <引擎> update）後直接 u2 讀 version.toml，沒有 engine_start 格；u11x／u12y／u13 三個結束前沒有 launcher_exit／log_prune 格；u0 的 launcher_start 也只在括號裡  (內容與連接 4/4)
- [顏色] u5g, u6g, u7: v2.14-3 藍 = 引擎做的、白 = 啟動器做的：查 registry（GET tags/list、換 token、記查詢失敗）是引擎容器做的（token 以 -e 傳入引擎、registry_query 是 engine 事件），這三格卻是白色，讀起來像啟動器在查；名詞表 p10_tv1「查詢步驟畫白格（不是 image）」是舊理由，與新規則衝突  (內容與連接 4/4)
- [內容一致性] u2: 單段 update：u1r docker run <引擎> update → u2 之間沒有「append engine_start」格（spec：單段也各一）  (排版 4/4)
- [內容一致性] u13: 三個結束橢圓（u11x／u12y／u13）前沒有「log_prune／launcher_exit」格，頁尾結束事件缺  (排版 4/4)
  (opt) [排版] ue14y: 「是：下一個目標」回圈線走 x=570，只離 u6 菱形左尖（x=580）與 u7 框左緣 10px，縮圖下看起來貼到不相關的菱形尖與方框  (排版 4/4)

## 47 流程 v2：離線包（2）add --local 與斷網 sync: must_fix 6 / optional 4
- [內容一致性] o10r, o10p2, w4, o11, w5: v2.14-2：本頁畫了 resolve add（o10r→o10re）、apply add（o10p2→o10e）、resolve／apply sync（w4→w4e）三個引擎容器，都沒有 engine_start 格；o11 與 w5 兩個 0 結束前沒有 launcher_exit／log_prune 格；o10、w0 每次都是新的啟動器呼叫，launcher_start 也只在括號或入口橢圓裡  (內容與連接 4/4)
- [內容一致性] o10re: add --local 的 resolve（o10re）／apply（o10e）與斷網 sync 的 o10re→w4e 引擎段都沒有「append engine_start」格；o11、w5 結束前也沒有「log_prune／launcher_exit」格，起點卻標「已寫 launcher_start」  (排版 4/4)
- [內容一致性] w1: 快路徑格文字寫「全相符 → 不起容器 → 0」，但圖上 w1 只有一條線接到 w2「有差」，全相符 → 0 的主成功路徑沒有畫（缺分支；應拆成「全相符？」菱形，是 → w5）  (排版 4/4)
- [lint] o10re: onething：「算計畫、指紋」與「stdout vk-resolve/1 回啟動器」是算與送兩個動作。建議拆成「resolve（不寫）：算計畫與輸入指紋」與「stdout vk-resolve/1 回啟動器」，與 prune 頁 q2～q5 一致。  (一格一事判定)
- [lint] w1: onething：一格內有動作（grep 比對 gen/*.stamp 第一行 vs version.toml）＋判斷（全相符？）＋結束（→ 0 不起容器）。建議比照 sync（1）頁 nq／nq0 的畫法拆成「grep 比對 gen/*.stamp 第一行 vs version.toml」→ 菱形「全相符且非 --verify／CI？」→ 綠「是 → 0：不起容器」，w2 接「否」。  (一格一事判定)
- [lint] w4e2: onething：「印記不符 → 重展開」是檢查＋重生（使用者舉的典型例子），再加「verify 逐檔 sha256」共三件事。建議拆成菱形「印記相符？」→ 否「重展開 cache/<repo>/（materialize）」，以及獨立一格「--verify：逐檔 sha256 比對」。  (一格一事判定)
  (opt) [內容一致性] o10b: 缺分支：o10b「讀 <工具 tar>.digest（旁檔缺 → 1）」失敗只寫在括號裡，沒有出口；離線包(1) 同一步驟已拆成 o4 菱形 + o4x 出口，兩頁不一致  (內容與連接 4/4)
  (opt) [可讀性] w1: w1「快路徑：grep 比對…；全相符 → 不起容器 → 0」一格含比對、判斷、全驗三件事，且「全相符 → 0」這個結束沒有線也沒有終點，只有「有差」一條線到 w2；斷網 build 走快路徑成功的主情境（驗收 §7.4-17）反而沒畫出來  (內容與連接 4/4)
  (opt) [lint] bO1b, o10e, o10f_1, w4f: termcov：bO1b 的 flock／apply、o10e 的 6-26、o10f_1 的 cache/、w4f 的 gen/tools.just 在本頁名詞表都沒有對應條  (內容與連接 4/4)
  (opt) [lint] oo1: onething：「有網路的機器取得工具 tar + .tar.digest」與「帶到離線機」是兩個人工步驟。建議拆成「有網路機器下載工具 tar + 同名 .tar.digest（工具 repo 提供）」與「帶到離線機」兩格；屬前置人工作業，可由使用者決定是否合併。  (一格一事判定)

## 46 流程 v2：離線包（1）bootstrap.sh --local: must_fix 2 / optional 3
- [內容一致性] o3t, o7b: v2.14-5 定 bootstrap(1) tag 形 docker image inspect 本機無此 image 要有紅出口（bootstrap(1) 已加 a8ix）；本頁 tag 形 o3t → o7b「docker image inspect 取 image ID」只有一條線進 o8，本機無該 image 時沒有失敗終點  (內容與連接 4/4)
- [內容一致性] o8e: 有 o2s launcher_start 格，但 o8 docker run 本機 image install → o8e 之間沒有「append engine_start」格，頁尾 o9 → 續頁前也沒有「log_prune／launcher_exit」格（bootstrap.sh 就是啟動器，spec 通則含 bootstrap）  (排版 4/4)
  (opt) [內容一致性] o8f_1: install 寫的檔案框漏 config.toml 與 baseline/vendor_kit/config.toml 副本（v2.12 L3′、v2.13 P10；install(1) 頁與目錄樹都有），也未列 log/ 由啟動器建  (內容與連接 4/4)
  (opt) [lint] o5x, o6x, o8e: termcov：o5x 的 6-16、o6x 的 6-23、o8e 的 薄殼／gen/.stamp／baseline/ 在本頁名詞表都沒有對應條  (內容與連接 4/4)
  (opt) [排版] oe3tj: 線標籤「tag 形：跳過 load／.digest」左端壓到 o3t 框（否 → tag 形…）右緣，貼框  (排版 4/4)

## 37 流程 v2：uninstall（2）寫入段: must_fix 0 / optional 3
  (opt) [內容一致性] x5e: 順序：x5e 刪 baseline/.vendor_kit.toml（spec §4.3 註：根 .dockerignore append 行的紀錄，uninstall 讀它刪原文相同行）發生在 x9b「仍有與紀錄相同的行？」之前，紀錄先被刪再比對；remove(2) 是先問 append 行再刪 baseline/<repo>/，兩頁順序相反（若依賴 resolve 計畫已帶行內容，格內應註明）  (內容與連接 4/4)
  (opt) [排版] xe16an: x9a／x9b 的「無」線共用 x=595 垂直段往下到 x9z，途中離不相關的 x9q 菱形左尖（x=600）只有 5px，縮圖下像貼在菱形尖上  (排版 4/4)
  (opt) [可讀性] x9q: x9q「問要刪這幾行嗎？」的「否」「是」兩條出線都從底尖出發，兩個標籤並排擠在一起（否 緊貼 是），難分辨哪條是哪條  (排版 4/4)

## 36 流程 v2：uninstall（1）resolve → apply 前置: must_fix 1 / optional 2
- [lint] x2e: onething：「產生輸入指紋」與「計畫＋詢問清單＋指紋以 stdout 回啟動器」是兩個動作。建議拆成「產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）」與「stdout vk-resolve/1：計畫＋詢問清單＋指紋回啟動器」。  (一格一事判定)
  (opt) [內容一致性] x2b: x2b 算 hash 的自產檔清單（薄殼、version.toml、gen/、cache/、baseline/）漏了 config.toml（v2.13 P6：hash == baseline/vendor_kit/config.toml 副本才刪），uninstall(2) x5cg 已依此比對，本頁保護清單來源未含它  (內容與連接 4/4)
  (opt) [lint] x2e: onething：x2e「產生輸入指紋 → 計畫＋詢問清單＋指紋以 stdout 回啟動器」一格含算指紋與 stdout 回傳兩件事；prune 頁 q4→q5 已把 stdout vk-resolve 拆成獨立格  (內容與連接 4/4)

## 41 狀態機 v2：交易與進度日誌: must_fix 1 / optional 3
- [lint] t5c: onething：「更新日誌 done += 步驟」是動作，「還有步驟 → 回 ①」是控制流程的判斷，塞在同一格且圖上沒有對應的迴圈邊。建議把「還有步驟？」拆成菱形（是 → 回 ①，否 → 接 t6 中斷？），t5c 只留更新日誌。  (一格一事判定)
  (opt) [可讀性] t5c: t5c「更新日誌 done += 步驟；還有步驟 → 回 ①」一格含更新日誌與「還有步驟？」判斷，且「回 ①」沒有線，t5c 唯一出線接 t6 中斷？→ 否 → t7 刪日誌，讀起來像每一步之後就刪日誌；迴圈只存在於文字  (內容與連接 4/4)
  (opt) [lint] t1, t4f_0, t4f_3: termcov：t1 的 6-26、t4f_0 的 baseline/、t4f_3 的 薄殼 在本頁名詞表都沒有對應條（pend 的「6-9」是 v2.6-9 誤判，不算）  (內容與連接 4/4)
  (opt) [內容一致性] t5c: 「逐步寫入 ③…；還有步驟 → 回 ①」只寫在字裡，沒有畫回 t5（①）的迴圈線，且一格含更新日誌＋判斷兩件事  (排版 4/4)

## 44 流程 v2：vendor_kit release（1）build 與驗收: must_fix 0 / optional 1
  (opt) [排版] ve4r: ve4r 從紫色 image 格 v4g 指向檔案框 v4r（bootstrap.sh(r)）並標「取」，實線語意是執行順序／讀寫，image 不會「取」檔案；應由 v4a 指向 v4r  (內容與連接 4/4)

## 45 流程 v2：vendor_kit release（2）推 image 與資產: must_fix 0 / optional 2
  (opt) [內容一致性] v8c: 缺分支：v8c「imagetools inspect 斷言：index 含 linux/amd64 + linux/arm64」是檢查，卻畫成單出口步驟，斷言失敗沒有終點（spec §8-12／§7.4：失敗不進正式 tag）；本頁從 push 到發布全程無任何失敗出口  (內容與連接 4/4)
  (opt) [內容一致性] v11b: spec §4.10 lnav 列：Release 資產附 lnav format 檔（json、timestamp-field、opid-field=trace_id…）；v11b 列出的資產（bootstrap.sh、tar、.digest、離線包、SHA256SUMS）沒有它  (內容與連接 4/4)

## 19 流程 v2：sync（1′）引擎 resolve: must_fix 2 / optional 2
- [排版] te14（t4 → tq）的「是」標籤: 「最後合併版本＝鎖定版？」的「是」字放在路徑右下轉角（x≈1230,y≈1070），離來源菱形約 160px、緊鄰「還有工具？」右上方，會被讀成「還有工具？」的出線標籤；標籤應貼在 t4 右尖旁  (排版 2/4)
- [lint] z1: onething：「產生輸入指紋」與「清單＋指紋＋apply|yes／no 以 stdout 回啟動器」是算與送兩個動作。建議拆成「產生輸入指紋（version.toml、metadata、印記 hash）」與「stdout vk-resolve/1：清單＋指紋＋apply|yes／no」兩格。  (一格一事判定)
  (opt) [排版] te2／te5／te5q／te8／te14 共用的 x=1230 直線: 右側匯流直線左貼四個藍格右邊（1220）、右貼 nf／t0r／t3r 橘框左邊（1240），各只 10px，縮圖看起來線黏在框上  (排版 2/4)
  (opt) [可讀性] z1: 「產生輸入指紋 … → 清單＋指紋＋apply|yes／no 以 stdout 回啟動器」一格兩件事（算指紋、回傳 stdout），應拆兩格  (排版 2/4)

## 20 流程 v2：sync（2）apply: must_fix 0 / optional 1
  (opt) [可讀性] m3v: 「版本變動的那次（…）：逐檔 sha256 驗 cache = 印記」把條件與動作合在一格，沒有「是否版本變動那次」菱形；不是那次時線也直接進「全部相符？」，讀者會以為每次都驗  (排版 2/4)

## 17 流程 v2：add（2）apply 寫入段: must_fix 0 / optional 1
  (opt) [排版] ce29／ce30（x=990 直線）與 c20: 右側匯流直線與「是：append 那幾行」格右邊只差 10px，縮圖看起來貼框  (排版 2/4)