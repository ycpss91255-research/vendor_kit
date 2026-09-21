
## 流程 v2：sync（每次 just 都跑）: must_fix 11 / optional 3
- [內容一致性] t1, t2, t3, t4, z0（啟動器泳道）: sync 的印記比對、verify sha256、metadata 完成標記／最後合併版本判斷、重生 gen/ 全畫在「啟動器（主機 sh）」泳道；但契約②（p3）說啟動器只 grep 第一行 + docker，sync 是引擎子命令，p4 也說「邏輯全在引擎 8 模組、啟動器不解析 toml」。頁與頁矛盾。
- [排版] n2, n6, t1f, t2f, t3r, z1: 右側檔案框／規則框右緣貼到分組框邊線，圓角被裁切。
- [排版] t2, t3, t4, z0: verify、metadata 判斷與 gen 產生均落在「啟動器」欄，容易被讀成主機 sh 負責引擎邏輯。
- [顏色] t1g: GHCR image 使用只代表「容器內子命令」的紫底。
- [可讀性] n1, t2, z0: 引擎 ref、sha256、recipe、mod、GHCR 未有本頁獨立白話解釋。
- [內容一致性] n4, t3r, p6_tv0: 一條路徑重寫 tracked 薄殼，另一處卻宣告「永不寫要進 git 的檔」，須先統一決策。
- [內容一致性] n1, n4, t1a, t2a, z0: frozen 路徑仍可寫薄殼、cache、gen，與第 1 頁 p1_tv14、第 4 頁 h_note 的「只檢查不寫」不一致。
- [內容一致性] n1, t0, t0s: CI 讀到 dev 覆寫沒有拒絕分支，會走跳過檢查路徑，與第 2 頁 local 覆寫「CI 拒絕」矛盾。
- [內容一致性] t0, t0s: 把 path 與 image 覆寫合併成「cache 是 symlink」，但自身 image tag 覆寫不是工具 symlink。
- [內容一致性] te18: dev 分支直接繞過 metadata 完成標記與 baseline 判斷；notes 只授權跳過 pull/verify，沒有授權跳過這些檢查。
- [內容一致性] z0, p6_tv8: 再次寫成每工具一行 mod，漏掉一工具多命名空間。
  (opt) [排版] te3: 「取 /dist」線上文字壓在 t1g（<repo>-dist@digest）框的左邊框與箭頭上。
  (opt) [排版] te15: CI=1？→ warn 框的「否」線先往下、再往右、再往下，多折一次。
  (opt) [顏色] p6_lgx1: 圖例文字叫「黃粗框」，實際為黃底紅粗框，應準確命名。

## 流程 v2：upgrade: must_fix 14 / optional 4
- [內容一致性] s0 / uD（E. 自身升級）: E 段寫「version.toml 第一行變 → 下次 just 才換薄殼、統一提示」；notes §2 與 p1 表格定的是 upgrade 不帶 repo 時碰到自身變了就「停下要求重跑」（當次就停，不是下次 just）。
- [排版] a3, a9, b8f, b10f, b14f, b15f, d3, s2: 右側檔案框右緣貼到分組框邊線，圓角被裁切。
- [排版] uA～uD, c_note: 四組流程加逐檔表擠成超長頁，右側便條過窄且大量換行，整頁難以閱讀。
- [顏色] a1, b3: image 紫底不符合本頁「紫＝容器內子命令」的圖例。
- [顏色] pend: 本頁圖例沒有定義黃底紅框「待拍板便條」；規則框與待定建議不能混為同一語意。
- [可讀性] c_r1c0, a0, a9: D、B 未明確定義，PR、commit、push、rebase、regex manager 等也缺本頁白話說明。
- [內容一致性] b8→b12→b13: 先實際改 version.toml，之後才因 CI 無 -y 回 1，沒有還原路徑，直接違反 §2「1 不動 version.toml」。
- [內容一致性] b6→b7, b12: dry-run 無條件回 0，完全繞過 CI「無 -y 又需改檔→1」判斷，與 §5 及本頁 c_note 衝突。
- [內容一致性] b6, b7, b11: dry-run 在逐檔判斷之前就結束，沒有畫出取得新版範本與比對後如何產生詢問清單。
- [內容一致性] b2: notes 的「先補待合併→查最新」被改成「先補待合併；否則查最新」，將順序改為互斥路徑。
- [內容一致性] s0, s1: 自身升級被延到「下次 just」才換薄殼，而 §2 upgrade 列要求自身變更時換薄殼並停下要求重跑。
- [內容一致性] b17, b2, c_r0c1: 已寫「衝突解完重跑」，但重入流程未檢查既有衝突記錄；baseline 已推新版後可能走「新版沒改→不動」，缺少清除／保留衝突狀態的路徑。
- [內容一致性] de3, d3: materialize 的「寫」箭頭連到包含初始檔與 baseline 的框，誤示 sync 也寫回它們；這兩者應由 git revert 還原。
- [內容一致性] c_note: 「多工具 init.toml 指到同一路徑→add 報錯」是新增政策，notes 只明定命名空間撞名，沒有明定 dest 撞名，應移除或標待定。
  (opt) [顏色] a4r, p7_lgx1 vs pend: 同一頁上「黃粗框＝規則」(a4r) 與「待拍板」便條 (pend) 都是黃底紅框，只靠形狀區分；p6 的 n6/t3r 也同樣，且 p1–p5 這組顏色代表待拍板，跨頁意義不一致。
  (opt) [內容一致性] b2, c_note: b2「比現版舊 → warn 仍執行」與 c_note「多工具 init.toml 指到同一路徑 → add 時報錯」都不在 notes；notes 的撞名規則是 just 命名空間 <ns>.just 撞名（§4），不是 init.toml dest。
  (opt) [可讀性] b6 → b7: --dry-run 分支在 materialize 之前就「只印會問哪些檔」，沒有畫出它從哪裡拿到新版檔案做逐檔判斷；一般讀者看不懂。
  (opt) [可讀性] s0: E 段自身升級沒有起點（綠橢圓），s0 是白色步驟框且沒有任何進入線，看起來懸空。

## 架構圖 v2：主機、引擎模組、registry: must_fix 15 / optional 0
- [顏色] h4 vs p4_lg2 / p4_np: 圖例與右上註記都說啟動器是「紅粗框」，但 h4 實際是紅底＋亮綠細框（v2 改）的樣式，沒有任何紅粗框元件；圖例對不上圖。
- [排版] mount_dist, pull_dist, q_reg: 「掛載 /dist/<repo>:ro」標籤正好壓在主機黑框邊線上；「拉 image（docker create／cp）」垂直線穿過主機標題列（docker ≥ 19.03、sh、just）；「查 tag／digest」線穿過引擎容器標題列。
- [排版] h0～h4, h_note: 架構頁混入使用者操作順序、sync 判斷與退出流程，不符合「架構只畫模組、最小單元與傳遞資料」。
- [排版] cli_m_reg～cli_m_init, dep1～dep3: 模組間只有呼叫／依賴箭頭，沒有標傳遞資料；八個模組也未呈現最小單元。
- [排版] pull_dist, q_reg: 垂直線穿過主機／引擎容器的標題帶，PNG 中與標題文字區重疊。
- [排版] h2g1_e, m_mg_f_user: 線上文字長於兩端框間的空隙，文字侵入端點框的閱讀區。
- [顏色] h4, p4_lg2: 圖例說啟動器用粗框區別，實際 h4 是 1.5 的亮綠細框，與引擎模組的 v2 框無法區別。
- [顏色] p4H: 主機分組使用淺灰底，本頁圖例未定義該底色。
- [顏色] f_ver, f_shell: 同框混放 tracked 與 untracked 檔案，無法一致套用本頁「綠框／灰虛線」的檔案狀態圖例。
- [可讀性] m_cli, m_ver, g_dist: cli、flock、buildx、sha256、recipe 等缺本頁白話定義，模組說明仍以工程縮寫為主。
- [內容一致性] g_note, p4_tv2: 「sync 不上網」比 notes 更強，且第 6 頁明畫 cache 缺失時向 GHCR 取 image；應區分「不查最新版」與「不下載鎖定版」。
- [內容一致性] g_eng, p4_tv0: 「只用 version.toml 第一行那一版」漏掉已定的 version.local.toml 本機引擎覆寫。
- [內容一致性] e_note, dep1～dep3, p4_tv11: 模組依賴方向、import-linter 與禁止依賴工作目錄，是 notes §8 未定義的新增架構決策，應移除或標待定。
- [內容一致性] f_user, p_note; f_note, h4: 分別重現 .gitignore 可 append／不碰，以及 sync 只寫 cache/gen／重寫薄殼的兩組矛盾，須先統一決策。
- [內容一致性] p4_tv7: append 的「不建整檔」再次漏掉檔不存在時建立的分支。

## 契約 v2：專案裡的檔與 version.toml: must_fix 10 / optional 5
- [顏色] p2_lg0 vs p2_lg4；t_ver, t_vk, t_vj, t_bl（#00b050）vs t_entry, t_ci, t_meta（#82b366）: 圖例「綠框＝進 git」(#82b366) 與「亮綠細框＝v2 改」(#00b050) 兩種綠肉眼幾乎分不出；多數進 git 的檔被 v2 改覆寫成 #00b050，而 cache/、tools.just、init.toml 等不進 git 的檔變成「綠虛線」——圖例裡沒有這種顏色（只有灰虛線）。同問題出現在 p4（f_repo、g1 綠虛線；p4b_lg0）。
- [排版] t_gstamp: gen/.stamp 框內文字「…退出 1」的「1」頂到右邊框被切，未在框內換行。
- [排版] t_rjust: PNG 中首行文字超出右側框線，須重新換行或增高。
- [顏色] t_vl, t_tools, t_repo, t_rstamp: 不進 git 的框改成綠色虛線，但圖例只定義「灰虛線＝不進 git」，未說明 v2 標記會覆蓋邊框顏色。
- [顏色] p2_tc_h0, p2_mt_h0, p2_mx_h0 等表頭: 灰底表頭未列入本頁圖例。
- [可讀性] p2_reno, t_tools, p2_vl: regex manager、docker datasource、currentValue/currentDigest、命名空間、RepoDigests、flock 沒有本頁名詞解釋。
- [內容一致性] p2_rule, p2_mx_r6c4: 規則摘要說 sync 只寫 cache/gen，矩陣卻說它會重寫薄殼，須先統一決策。
- [內容一致性] p2_tv0: 「baseline 都由 version.toml 推導」不成立於待合併情境：version 已 B、baseline 仍 A，baseline 保存的是歷史狀態。
- [內容一致性] p2_mx_r3c6: gen 欄寫「刪該工具 recipe」，應改為刪除該工具的命名空間引用。
- [內容一致性] p2_mx_r1c8: uninstall 的初始檔欄只有「永不刪」，漏掉 append 行經詢問可移除的既定例外。
  (opt) [內容一致性] p2_mt_l: metadata 標題寫「欄位名待定」，但 notes §9 待拍板五項沒有這一項（只有 init.toml 的 mode 欄位名待定）。
  (opt) [排版] te15: cache/<repo>/ → .stamp 的樹線從上方進入框頂（箭頭壓在虛線框上），其他所有樹線都是從左側進入，不一致。
  (opt) [排版] te2, te19 / te3〜te14: 專案/ 與 .vendor_kit/ 往下的多條樹線在 x≈20〜40 與 x≈75〜90 重疊成雙線，看起來像兩條平行幹線。
  (opt) [可讀性] p2_reno, t_ver（Renovate、flock）: 本頁用到 Renovate、flock 但「本頁名詞」表沒有這兩條（p8 也用 flock 而無名詞）。
  (opt) [排版] p2_mx_h0～p2_mx_r7c8: 九欄矩陣大量窄欄換行，動作與例外難以快速對照。

## 流程 v2：bootstrap.sh + install + add: must_fix 13 / optional 6
- [排版] a9f, a10f, i4f, i6f, i8f, cf1: 專案目錄泳道的虛線檔案框右緣 (x=1600) 與淺灰分組框右緣重疊，圓角被裁掉、看起來像被切掉一截。
- [排版] bA, bI, bB, p5_tv0～p5_tv11: 三個完整流程塞在高達 3409 的單頁，整頁顯示時文字極小，應拆頁或減少重複文字。
- [顏色] a7, c3: GHCR image 用紫底，但本頁紫色只定義為「容器內子命令」。
- [顏色] pend: 黃底紅框待拍板便條沒有本頁圖例定義。
- [可讀性] a0, a8, c9, c17: release、tar、GHCR、daemon、index digest、mod／命名空間等缺本頁白話定義。
- [內容一致性] i0, i4→i5: 列出 --no-justfile，流程卻沒有跳過 justfile 操作的分支。
- [內容一致性] i5→i7→i8: 只檢查 justfile 存不存在，沒有檢查 import 行已存在；重跑 install -y 會依圖再次 append，違反冪等。
- [內容一致性] bI, i4: 把修復定義成「只補缺的、已存在不動」，無法表達 notes 的薄殼修復，且是未註明的新限制。
- [內容一致性] a9, a10, a12: 已畫出直接寫專案，失敗卻只以丟棄暫存目錄保證「專案不留任何檔」；未呈現如何保留原有內容、撤回本輪變更。
- [內容一致性] c0, c7～c18: add 接受 -n，卻沒有 dry-run 分支，照圖仍寫 version.toml、初始檔與 baseline。
- [內容一致性] c7～c18: 獨立 add 流程只有成功路徑，未表達寫 version.toml 後失敗如何滿足 §2「回 1 不動 version.toml」。
- [內容一致性] c17, cf1: 「每工具一行 mod」與 §4 允許一工具多個命名空間，以及第 2 頁「一行一命名空間」矛盾。
- [內容一致性] i1, c1, c2: flock 被放在主機且先於 docker run，docker load 又寫在引擎步驟內，與 §8 version 模組負責鎖、主機負責 docker 的分工不一致。
  (opt) [內容一致性] c7 → c9 → c10（及 p7 b8 → b9 → b10）: add／upgrade 流程畫成引擎先查 tag、寫 version.toml，再回啟動器 docker create/cp，再回引擎 materialize；但 p3 契約② 說每次動詞固定三步：啟動器先 create/cp 每個工具、再 docker run 引擎一次。兩頁順序互相矛盾（引擎容器跑到一半無法叫主機 docker）。
  (opt) [內容一致性] i1, c1（及 p7 b1、p8 d1/u1/m1）: flock 畫在「啟動器」泳道、docker run 之前；p4 卻把 flock 放在引擎的 version 模組。頁與頁不一致。
  (opt) [顏色] p5_lgx2（#2ea043）vs p1–p4 的 #00b050: 「v2 改」綠細框在 p1–p4 用 #00b050，p5–p8 用 #2ea043，同一意義兩種綠。
  (opt) [內容一致性] a8, a9f: bootstrap --local 畫成「寫 version.local.toml（只記 image tag）」；notes 的 bootstrap 只說 --local 用本機 image／先 docker load，沒說會寫 version.local.toml。
  (opt) [排版] ae8, ae6, ce7, ce16: a5→a8「是」線多折一次才進框；「否」標籤壓在 a6 左邊框上；c4→c7、c13→c15 兩條線微斜、不是正交線。
  (opt) [排版] a9f, a10f, i4f, cf1: 右側檔案框貼齊父框右界，框線重疊，缺乏閱讀留白。

## 流程 v2：dev/undev、remove/uninstall: must_fix 12 / optional 0
- [排版] df1, v3, u5, m7, m9f, x3f, x5f: 右側檔案框右緣貼到分組框邊線，圓角被裁切（放大確認）。
- [排版] vA～vD, df0, df1: 五組操作集中於長頁，右上目錄差異框過窄，路徑拆行後難以比較。
- [排版] vI, v2, v3: 自身 dev 流程停在寫檔箭頭，未分開本次命令結束與下次 just 的執行邊界。
- [顏色] pend: 黃底紅框待拍板便條未在本頁圖例定義。
- [可讀性] d1, vI, m8: flock、RepoDigests、index digest、metadata、CI、dry-run 缺本頁名詞說明；symlink 雖有條目，解釋仍只換成另一個專有名詞。
- [內容一致性] d1: 掛載寫成 -v <dir>:/dist/<repo>:ro，少了來源的 /dist，與 §6、第 3、4 頁不同。
- [內容一致性] vB, u4, u5: 宣稱自身 undev「同理」，卻只畫拆 symlink、展開工具 cache，沒有恢復引擎 ref 與換薄殼的自身路徑。
- [內容一致性] m0～m10, x0～x7: remove／uninstall 列出 --dry-run，但流程完全沒有不寫檔分支。
- [內容一致性] m6→m8: 先刪 baseline 及其中 metadata，才問 metadata 是否記有 append 行；未畫出先讀取保存的資料，流程所需資訊來源消失。
- [內容一致性] x2, xe3: 逐工具 remove 可能回 1，但箭頭仍無條件通往刪除整個 .vendor_kit/，缺少失敗中止分支。
- [內容一致性] x3f, x2, p8_tv6: 「使用者 .gitignore 不碰」與 uninstall 移除其 append 行再次衝突，須先統一決策。
- [內容一致性] d8: 「upgrade 的合併來源不受 dev 影響」是 notes 未明定的額外保證，也未說明如何避開 symlink cache 取得正式新版範本；補決策或移除保證。

## 契約 v2：工具 repo、啟動器↔引擎、CI: must_fix 8 / optional 5
- [內容一致性] p3_sub（及 p4 m_cli、p3_tk9）: 引擎子命令框與 cli 模組都寫「--porcelain 機器可讀（留給 CI）」並列為本頁名詞，但 proposal_v2 沒有這個旗標；屬未定案內容畫成定案。
- [排版] p3_dist: 目錄樹註解因欄寬不足拆行，[mode] 和 Dockerfile 註解容易被讀成獨立目錄項目。
- [可讀性] s3, p3_jm, c_a～c_e: uid/gid、rootless、ADR、lint、unit、runner、測試矩陣等未在本頁名詞表解釋。
- [內容一致性] k6_e, k6: 專案測試後無條件連到「需改檔→1」，把條件式失敗畫成整條 CI 的必經終點，且沒有成功終點。
- [內容一致性] p3_sub: 將結束狀態 2 一律解釋為衝突，漏掉 §2 的 update --exit-code 有新版也回 2。
- [內容一致性] p3_sub, p3_tv9: 新增 --porcelain 及「第一版保留旗標給 CI」，notes 沒有這項介面決策，應移除或標待定。
- [內容一致性] p3_dist, d4_1: 「dist/files 不含 symlink」是 notes §4 未列出的新增供應限制，不能當已定契約，應移除或標待定。
- [內容一致性] p3_tv6: append 被定義成「不整檔建立」，漏掉 §2 已定的「檔不存在→建」。
  (opt) [可讀性] k6: 「需改檔（無 -y）→ 1 印清單」接在 ⑤ 專案測試之後，讀起來像專案測試後才判斷；依 §5 它是 ③ upgrade --dry-run 那一步的結果。
  (opt) [內容一致性] d4_7, p3_c3, p3_tv10（check.sh --dist）: 工具 repo CI 跑「check.sh --dist」在 p1 便條、p3 多處出現並列為名詞，但 notes §4/§7 只說「CI 驗兩平台內容一致」，沒有 --dist 這個介面。
  (opt) [內容一致性] c_b（test-base）: vendor_kit 自身 CI 階段名 test-base 含「base」字樣；雖是 notes §7 原文，但使用者規定 base 只能出現在「對齊 base 的 just 慣例」描述，請確認是否要改名。
  (opt) [可讀性] title / p3L2 / p4_np: 各頁用「契約①〜⑤」編號（②＝啟動器↔引擎、⑤＝CI），與 notes 的 §2（使用者介面）、§7（CI）編號對不上；p1 也沒標自己是契約①，p4 註記卻寫「(4) 見契約①」。第一次看的人找不到對應。
  (opt) [排版] p3_lg0（及 p4 p4_lg0/p4_lg3/p4_lg4、p5–p8 淺灰圖例）: 圖例色塊用 swimlane 樣式，文字擠在標題列、下方留一塊空白，看起來像沒填完的容器。

## 契約 v2：目的、角色、介面: must_fix 8 / optional 2
- [排版] p1B_r0c3, p1B_r1c3, p1B_r9c3: 多段契約擠在單一儲存格，難以辨識條件、操作與失敗結果，未達「字少、一般人可懂」。
- [顏色] p1A, p1B, p1B_h0～p1B_h5: 淺灰分組底與灰色表頭未在本頁圖例定義；灰橢圓的角色意義不能涵蓋它們。
- [可讀性] p1A_goal, p1B_sem: GHCR、image、just、recipe、mod/import、PR、CI 沒有本頁白話定義，「一行轉發」的解釋仍依賴這些詞。
- [內容一致性] p1B_r6c3, p1_tv12: 將補合併定位成「Renovate merge 後」，但 notes §7 與第 7 頁要求在 PR 分支補完、CI 通過後才 merge。
- [內容一致性] p1B_r4c3: 「gen 內該工具 recipe」與 §2 的「gen/tools.just 零 recipe」衝突，應寫移除該工具的 mod 引用。
- [內容一致性] p1_tv14: 「frozen 只檢查不寫、不上網」是 notes 未明定的額外限制，且與第 6 頁 CI 路徑仍 materialize、重生 gen 的畫法矛盾。
- [內容一致性] p1B_inv, p1B_r9c3: 同頁同時宣告 sync 只碰不進 git 的東西，又重寫 tracked 薄殼；是 notes §1/§2 vs §2/§6 內部矛盾的直接呈現，須先統一決策。
- [內容一致性] p1A_goal: 未交代 §0 已定的「自寫＋主機 docker＋引擎 git merge-file，第一版排除既有整套方案」實作範圍，補短註即可。
  (opt) [顏色] p1B_inv vs p1_pend: 不變量框與待拍板便條同為 #fff2cc 底＋#b85450 寬 3 邊框，只差便條摺角；圖例分寫「黃底紅框便條＝待拍板」「紅粗框＝不變量」但視覺上同一種顏色兩種意義。
  (opt) [顏色] p1A_r1, p1B_r0c0, p1_pend: 同一黃色 (#FFF4C3/#fff2cc) 同頁承擔三種意義：承諾角色橢圓、一次性動詞列、待拍板便條。

TOTAL must_fix 91; rejected 3