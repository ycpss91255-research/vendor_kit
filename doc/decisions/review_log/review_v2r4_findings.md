
## 契約 v2：目的、角色、介面: must_fix 12 / optional 1
- [內容一致性] p1B_r7c3_2, p1B_r8c3_0, p1B_r9c3_2: 仍寫「--pull never」；16 條必修已改為啟動器用 docker image inspect 驗本機 image（覆寫時不 pull），三格都要改寫
- [內容一致性] p1B_inv, p1B_r4c3_0, p1B_r11c1, p1B_r11c3_2, p1_tk36: 仍以「CI=1」字面當 frozen 條件；16 條必修改為 CI 真值規則（非空且非 0/false），判斷格與名詞表都要改寫（例如「CI 為真且需改 tracked 檔？」並在名詞表定義真值）
- [內容一致性] p1B_r5c3_1, p1_tk28: 私有 registry 寫「需 VENDOR_KIT_REGISTRY_TOKEN」（環境變數）；16 條必修改為 TOKEN_FILE 以 -v 掛進容器，名詞表條目也要改
- [排版] p1B, p1_th～p1_tv49: 單頁同時放不變量、完整動詞表、規則及 50 組名詞，PNG 縮放後正文無法閱讀；建議至少拆成「不變量與角色」「動詞介面」「共用名詞」三頁。
- [排版] p1B_r0c3_2, p1B_r3c3_3, p1B_r6c3_2: 一格仍串接多個動作（如「呼叫 install → 每個工具 add → 冪等修復 → trap 清理」及多步寫入收尾），不符每格一件事。
- [可讀性] p1B_inv: 一個不變量框塞入 sync、薄殼 hash、frozen、append、三方合併、二進位等多個主題，非工程讀者無法由主圖理解。
- [可讀性] p1_tv1: 把 PRD 解釋為 doc/PRD.md，但 v2.4 已定「不建 PRD.md」。
- [內容一致性] p1B_sem, p1_tv46（及所有描述 gen/tools.just 的文字）: 仍寫每行 mod，未改成必修的 mod?。
- [內容一致性] p1B_inv, p1B_r4c3_0, p1B_r11c1（全部 CI=1）: 仍把 CI 判斷寫成字面等於 1，未套用「CI 真值規則」。
- [內容一致性] p1B_r5c3_1, p1_tk28/p1_tv28: 仍直接使用 VENDOR_KIT_REGISTRY_TOKEN 環境變數，未呈現必修的 TOKEN_FILE 以 -v 掛載。
- [內容一致性] p1B_inv: 「二進位／symlink 未改才換」缺少必修的「先問，答應後才換」。
- [內容一致性] p1B_r1c3_1: 只說無 justfile 時「建」，沒有明列根 justfile 必須同時產生 import … 與 default: @just --list 兩行。
  (opt) [可讀性] 整頁（8886px 高）: p1–p3 每頁 8800px+ 一次看不完；建議拆頁點：p1 在「不開的動詞／動詞語意」之前拆（動詞表一頁、規則＋名詞表一頁）；p2 在「動詞 × 檔案」表之前拆（目錄樹＋檔案範例一頁、動詞×檔案＋metadata 表一頁）；p3 依契約

## 架構圖 v2：主機、引擎模組、registry: must_fix 6 / optional 1
- [內容一致性] g_eng: 引擎 image 框仍寫「不 pull（--pull never）」，應改 docker image inspect
- [內容一致性] g1, p4_tv34: gen/tools.just 框內容與名詞表寫 mod 而非 mod?
- [排版] w_user（等資料邊）: 箭頭標籤仍包含「判斷、建、append、換、合併」等動作，不是單純傳遞的資料；違反架構頁箭頭只標資料。
- [排版] g_note: 把 cache 缺、digest 變、verify 失敗等流程條件放在架構頁，應移到 sync/materialize 流程頁。
- [內容一致性] h1（根 justfile）: 只呈現 import，漏掉新建檔的 default: @just --list。
- [內容一致性] CI 相關單元: 仍使用 CI=1 字面規則。
  (opt) [內容一致性] w_user, w_shell: 箭頭文字含動作（「現況 → 判斷；…合併結果 → 寫」「首行 hash → 比對；模板 → 重產」），v2.5 §12 架構頁箭頭只標傳遞的資料

## 契約 v2：專案裡的檔與 version.toml: must_fix 7 / optional 0
- [內容一致性] t_tools: gen/tools.just 寫成「mod <ns> '../cache/<repo>/just/<ns>.just'」，16 條必修規定 tools.just 用 mod?（檔不在也不掛）
- [內容一致性] p2_vl, p2_mx_r5c2: version.local.toml 範例註解與動詞×檔案表仍寫「docker run --pull never」，應改為 docker image inspect 驗 image ID
- [內容一致性] t_vl, p2_vl_l, p2_mx_r8c2, p2_tk31, p2_tv12: 「CI=1 有任何覆寫 → 1」「CI=1 frozen」等仍是 CI=1 字面
- [排版] t_root～名詞表（整頁）: 目錄樹、欄位矩陣、相容性規格和名詞表疊成超長頁，PNG 縮放後字體不可讀；建議拆成「目錄樹」「TOML／metadata」「寫入者與相容性」。
- [內容一致性] t_just: 把 install 說成只加 import 一行；新建根 justfile 時還必須有 default: @just --list。
- [內容一致性] t_vl（及頁內本機 image 說明）: 仍沿用 --pull never 契約，應改成 docker image inspect 驗證。
- [內容一致性] t_bl, t_meta: 一方面說 install 建「進 git 的空 baseline/」，另一方面說 install 不建 metadata；Git 不追蹤空目錄，兩格合起來無法成立，需加佔位檔或改正「進 git」敘述。

## 流程 v2：add（1）resolve → docker → apply 前置: must_fix 4 / optional 1
- [內容一致性] c12br: 規則框末尾寫「base ADR-10」，「base」只允許出現在「對齊 base 的 just 慣例」與 test-base，此處要拿掉
- [內容一致性] c14, p5b_tv14: 判斷格「CI=1 且需改 tracked 檔？」用 CI=1 字面（add（2）p5bc_tv14、sync（1）eA／nc／ncx／nf／t4c／p6_tk3、B(1) b12、逐檔判斷表 c_r7c0、Renovate a4b／p7_tv2、dev d2a／v2q、remove m7c、uninstall x3c、
- [顏色] c6x, c11x: 「請用 upgrade」「請重跑」都是需要人動作的結束 1，應為橙色，不應為紅色。
- [內容一致性] 所有 CI=1 判斷: 仍為字面規則。
  (opt) [排版] cf0, cf1: 「add 前／後」是一格塞整棵目錄樹（多檔一格），與「檔案框一格一檔」相違；且本頁 legend 沒有「虛線樹：目錄差異」（該條目卻放在沒有樹的 add（2）頁）

## 契約 v2：工具 repo、啟動器↔引擎、CI: must_fix 10 / optional 0
- [內容一致性] p3_sh: 啟動器規則框寫「引擎覆寫 vendor_kit= 時 docker run --pull never」，且主機命令白名單（docker pull／create／cp／run／rm）少了 image inspect；應改為 inspect 並列進白名單
- [內容一致性] s2a, k1, k3f, p3_dry, p3_ens, p3_acc_r3c1: 契約④／⑤ 的「frozen：CI=1」「① sync（CI=1 frozen）」「③ CI=1 且需改 tracked 檔」皆為 CI=1 字面，且沒有任何一頁定義 CI 真值規則
- [內容一致性] p3_ens, p3_tk33: 「引擎需 VENDOR_KIT_REGISTRY_TOKEN」應改為 TOKEN_FILE 用 -v 掛載（架構頁 g_note／p4_tv5／p4_tk6 同）
- [內容一致性] d4_4, p3_dist, p3_tv1: Dockerfile.dist 寫「只有 FROM scratch + COPY dist/ /dist/」，16 條必修要求必含 vendor_kit LABEL（prune 依 label 刪），三處都少了 LABEL
- [排版] 全頁: 工具交付、啟動器協定、CI、驗收矩陣及名詞表集中於超長頁，主圖文字低於實用閱讀尺寸；建議至少拆成三頁。
- [內容一致性] d4_4 / p3_dist（Dockerfile.dist）: 只列 FROM scratch、COPY dist/ /dist/，缺介面審查必修的 LABEL。
- [內容一致性] p3_sh（及本機引擎路徑）: 仍寫 --pull never。
- [內容一致性] registry token 相關方塊: 仍直接傳 token，沒有 TOKEN_FILE 與 -v 掛載。
- [內容一致性] 頁內所有 CI=1: 未改用 CI 真值規則。
- [內容一致性] gen/tools.just 相關描述: 仍為 mod，未改成 mod?。

## 流程 v2：bootstrap.sh: must_fix 4 / optional 0
- [內容一致性] a9, p5_tk14, p5_tv14: 「docker run <引擎> install（--local：--pull never）」與名詞表「--pull never」條目仍是舊寫法
- [顏色] a2, a4: 「請先 git init」「印下載＋安裝指令」都是結束 1 且要求人採取動作，卻使用紅色失敗終止；依本輪規則應為橙色。
- [內容一致性] a9（及本頁 --local 引擎路徑）: 仍寫 --pull never。
- [內容一致性] a9f_4: 「根 justfile 一行」：新檔實際應包含 import 與 default 兩行。

## 流程 v2：install: must_fix 2 / optional 1
- [內容一致性] p5c_tk14, p5c_tv14: 名詞表仍收「--pull never」條目
- [內容一致性] i4gf（空 baseline/）: 標成進 git，但流程又明定 install 不建 metadata；空目錄無法由 Git 追蹤。
  (opt) [內容一致性] i2（是 git repo？）: v2.4 Q20「install 時上層已有 .vendor_kit/ → 1 禁止巢狀」在 p1 動詞表有寫，但 install 流程頁沒有這個判斷

## 流程 v2：sync（1）resolve: must_fix 5 / optional 1
- [內容一致性] n1b, p6_tv13: 「是：docker run <引擎> resolve sync（覆寫時用該本機 image，--pull never）」與名詞表仍寫 --pull never
- [顏色] t3a, t4r: 「請 add」「請 upgrade」均明確要求人採取動作，現在為紅色；應改橙色。
- [內容一致性] 本機引擎覆寫路徑: 仍寫 --pull never。
- [內容一致性] tools.just 相關判斷: 仍以 mod 為內容，未改 mod?。
- [內容一致性] 所有 CI=1／frozen 判斷: 仍未使用 CI 真值規則。
  (opt) [內容一致性] n1b（是：docker run <引擎> resolve sync）: grilling Q22 定案：啟動器先 grep 比對 gen/*.stamp 第一行 vs version.toml 各行，全相符不起容器；本頁 gen/.stamp 相符後一律起容器跑 resolve、每檔 sha256 verify

## 流程 v2：sync（2）apply: must_fix 2 / optional 1
- [內容一致性] p6c_tv13: 名詞表仍寫 --pull never
- [內容一致性] frozen 分支: 仍使用 CI=1 字面規則。
  (opt) [顏色] pend: 本頁有便條（pend）但 legend 沒有「便條：補充說明」條目（B(2)、E. 自身升級 (a)(b)、uninstall 三頁同）

## 流程 v2：upgrade ── E. 自身升級 (a)(b): must_fix 4 / optional 0
- [內容一致性] s2ly, pend, p7bc_tk5, p7bc_tv5: 「是：用該本機 image（--pull never）」、便條與名詞表仍寫 --pull never
- [排版] 刪進度日誌 → 回報啟動器「引擎已變」: 一格兩件事（刪日誌 + 回報啟動器），要拆成兩格
- [排版] s4, s8: 只寫「接 E(c)／走 (c)」，未標頁名或頁次，且第 16 頁沒有對應的具名跨頁入口；拆頁後連接不夠明確。
- [內容一致性] 本機覆寫支線: 仍使用 --pull never。

## 流程 v2：upgrade ── E(c) upgrade vendor_kit: must_fix 5 / optional 1
- [內容一致性] uE2, s11y, pend, p7bcc_tk5, p7bcc_tv5: 分組標題、「是：用該本機 image（--pull never）」、便條與名詞表仍寫 --pull never
- [排版] s10: 頁面只有「使用者執行 upgrade vendor_kit」入口，沒有接收第 15 頁 (a)/(b) 內部續行的入口節點；兩種入口被錯誤地畫成同一種使用者起點。
- [顏色] s12bx: 「請重跑」為需要人動作，應使用橙色，不應為紅色。
- [內容一致性] s11y（及名詞表）: 仍寫 --pull never。
- [內容一致性] 薄殼／gen 重產段: 沒有畫出「建進度日誌 → 寫入 → 最後刪日誌」，不符合 v2.5 所定 apply 寫入順序。
  (opt) [可讀性] docker run 該引擎 upgrade vendor_kit: E(a) 頁出口寫「同一次指令內接 (c) 的引擎段」，但本頁沒有標出 (a) 從哪一格接入（(a) 已由啟動器選好引擎，不會再走 grep／local 覆寫判斷），只有頂端的使用者指令入口

## 流程 v2：undev: must_fix 2 / optional 0
- [內容一致性] pend, p8c_tk7, p8c_tv7: 便條與名詞表仍寫 --pull never
- [顏色] u6bx: 「請重跑」是需要人動作，應為橙色，不應為紅色。

## 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退: must_fix 3 / optional 0
- [內容一致性] c_r6c0: 二進位／symlink 列寫「你未改（D==B）才換」直接換；16 條必修定為「二進位問後換」，缺詢問步驟（p1 不變量框 p1B_inv 同句同錯）
- [內容一致性] 二進位／symlink 列（「你未改才換、改過保留」）: 缺少介面審查必修的「先問，答應後替換」。
- [內容一致性] 拒絕／declined 列: 「之後不問」沒有補上「目標新版再次更新時重新詢問」。

## 流程 v2：upgrade ── A. Renovate 路徑: must_fix 1 / optional 0
- [排版] ae7, ae8: commit/push → 「PR 分支 CI 再跑」的線（ae7）與 check.sh ⑤ → merge PR 的線（ae8）在 ⑤ 正下方十字交叉

## 流程 v2：upgrade ── B. 手動路徑（2）寫入: must_fix 6 / optional 0
- [排版] 同意：合併在暫存做（換新版／git merge-file --diff3／append 行替換）→ 逐檔原子替換: 一格兩件事（暫存合併 + 逐檔原子替換），要拆成兩格
- [排版] b14q: 一格同時涵蓋換新版、三方合併及 append 替換三種不同詢問，違反一格一個判斷。
- [排版] b14: 同格同時執行合併與替換，必須依不同分支拆開。
- [內容一致性] b14q: 未包含 Q14「新版新增初始檔 → 問要不要建」的詢問分支。
- [內容一致性] tools.just 寫入: 仍是 mod，未改 mod?。
- [內容一致性] CI 判斷: 仍為 CI=1 字面規則。

## 流程 v2：upgrade ── B. 手動路徑（1）前置: must_fix 3 / optional 2
- [排版] b10d: 同一菱形同時判斷 dest 合法與命名空間無撞名，屬兩個獨立判斷，必須拆格。
- [顏色] b1x, b2c, b5, b10x: 「先 undev」「解衝突」「先 add」「請重跑」都是需要人動作的終止，應為橙色，不應為紅色。
- [內容一致性] 所有 frozen 判斷: 仍使用 CI=1 字面規則。
  (opt) [顏色] 是 → 1：請先 undev <repo>／否 → 1：無 baseline，請先 add <repo>: legend 說橙 = 需要人動作（1／3）、紅 = 失敗終止，但「請先 undev」「請先 add」「請先 git init」（bootstrap a2、install i3、sync t?「從未完成接入請 add」、remove、dev
  (opt) [排版] 線上文字「是」（(1) 有待合併？ 左下出口）: 「是」標籤壓在菱形邊線上；dev 頁「<dir>/dist/init.toml 存在？」左下的「否」同樣壓在菱形邊上

## 流程 v2：remove: must_fix 3 / optional 1
- [排版] m9q: 同一菱形同時判斷是否有 append 行並執行詢問，應拆成「有 append 行？」與「使用者同意？」兩格。
- [顏色] m5, m9x: 「請先 undev」「請重跑」均為需要人動作，應改橙色。
- [內容一致性] m7c（等 frozen 判斷）: 仍使用 CI=1 字面規則。
  (opt) [可讀性] 有 append 行 → 問「要刪我們加的這幾行嗎」？: 判斷格只有「拒絕」「同意」兩個出口，沒有「無 append 行 → 跳過」分支，只靠便條說明；沒有背景的人看不出無 append 行時往哪走

## 流程 v2：add（2）apply 寫入段: must_fix 2 / optional 0
- [排版] c15: 同格同時表示從 /dist 複製到暫存、原子替換 cache 與寫入 materialize 結果，仍是多件事。
- [內容一致性] gen/tools.just／mod 行相關方塊: 仍使用 mod，應改成 mod?。

## 流程 v2：dev: must_fix 1 / optional 0
- [內容一致性] v6b, p8_tk7/p8_tv7: 仍明列 docker run --pull never，應改為 docker image inspect 驗證本機 image。

## 流程 v2：uninstall: must_fix 3 / optional 0
- [排版] x2b: 同格同時算 hash、分類可刪／保護、建立保護清單及宣告不寫入，仍是多件事，應拆格。
- [顏色] x4bx: 「請重跑」為需要人動作，應改橙色。
- [內容一致性] x3c（及名詞表）: 仍使用 CI=1 字面規則。

TOTAL must_fix 85; by category {'內容一致性': 58, '排版': 17, '可讀性': 2, '顏色': 8}; rejected 24