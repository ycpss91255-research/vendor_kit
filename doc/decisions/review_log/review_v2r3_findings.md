
## 契約 v2：工具 repo、啟動器↔引擎、CI: must_fix 6 / optional 1
- [排版] c_f_v2: 「驗收：剛 build 的引擎 image + 乾淨 fixture repo 跑完整流程」的 v2 綠標壓在「跑」字上
- [可讀性] s3: 契約④ 的 ③（pull→create→cp→rm）與 ②（讀 version.toml、查 registry、輸出 stdout）一格塞多個動作，違反每格一件事
- [排版] s3: pull、create、cp、rm 四個動作放在一格
- [排版] c_c: lint／unit／install／merge 四項檢查放在同一動作格，應拆開
- [可讀性] k1, s2: 使用 frozen，本頁名詞表未交代其禁止寫 tracked 檔、禁止查最新版的意義
- [內容一致性] p3_pend, p3_tv15: 新增「check.sh --dist 擋來源檔含 CRLF」限制，notes 無此決策；Q13 換行等價比對不能解讀成禁止 CRLF 來源檔
  (opt) [排版] s4: 「④ docker run … 引擎 apply <動詞>」換行後第二行只剩孤立的「>」

## 流程 v2：upgrade ── Renovate 路徑、手動路徑: must_fix 13 / optional 2
- [排版] a5: 橢圓文字超出輪廓：a5、b5、b18
- [顏色] a5: a5 是紅橢圓（圖例＝錯誤終止）卻有後續箭頭接到 a6，終止不該有出邊
- [內容一致性] b4: B 手動路徑沒有 v2.1 B「工具在 dev 覆寫中 → 1 提示先 undev」判斷（p8 d9、p8b m4 都有，upgrade 沒有）
- [排版] be9: be9 起點在 b6y 底邊上沿框走，be10 與它平行只差 6px，兩線壓到「是：目標版 = B」框的底框
- [可讀性] b16: 一格多件事：b16（寫 version.toml 並刪進度日誌）、b10（flock → 重驗）、b10b（清除衝突狀態＋建進度日誌）、b13（materialize＋寫印記）、b14（詢問／合併／替換／記日誌）、b8（docker 四命令）、a4、a6（三步鏈）
- [排版] b10b, b14, b15, b16: 清除狀態與建日誌、詢問與合併替換、baseline 與 metadata、寫版本與刪日誌仍各自合併
- [可讀性] b10b, b15g: 使用 metadata、mod，本頁名詞表未充分解釋其內容與作用
- [內容一致性] b10b → b12／b11: 判斷 dry-run 之前已清除衝突狀態並建立日誌，違反唯讀預覽
- [內容一致性] b10b: 非 dry-run 時也把清除衝突狀態排在建立日誌之前，違反「第一個寫入前建立日誌」
- [內容一致性] b12: CI 判斷含「無 -y」，與 v2.3 §7 的 dry-run 結束狀態規則不一致
- [內容一致性] b10c, b13: 逐檔比較發生在 materialize 新版 cache 之前，卻把新版 N 定義為 cache 內容，應使用此次拉到暫存的新版範本
- [內容一致性] b1 起始的單一工具路徑: 缺少 dev 覆寫時拒絕 upgrade 的分支，與 p8 d9 及 v2.1 B 不一致
- [內容一致性] 寫入前的預檢段: 未呈現 upgrade 也必須執行的 dest 撞名、正規化與越界檢查
  (opt) [排版] a6: a6、a7 文字貼到框邊
  (opt) [可讀性] be26: b16 有三條出邊，只有「無衝突」「衝突」有線上文字，到 b16x 的那條沒有條件

## 契約 v2：目的、角色、介面: must_fix 5 / optional 3
- [排版] p1B_r0c3, p1B_r3c3, p1B_r6c3: 每格包含多個連續動作及分支，upgrade 格同時描述工具升級、自身升級與 PR 路徑，不符「每格一件事」
- [可讀性] p1B_inv, p1B_sem: 使用 PRD、set positional-arguments，本頁名詞表未解釋
- [內容一致性] p1B_no, p1_tv15: 把所有 dry-run 描述為「照樣拉 image」，但 remove／uninstall 不走工具 image 拉取，須限定適用動詞
- [內容一致性] p1B_r8c3: 「刪 version.local.toml 該行 → 重新 materialize」把刪除排在 resolve 前，與 v2.3 §6 及 p8 拿鎖後刪除流程不一致
- [內容一致性] p1B_r4c3: remove 的刪除清單漏掉 gen/<repo>.stamp，與印記搬遷後的 p8b 流程不一致
  (opt) [內容一致性] p1B_r6c3: upgrade 列沒有 v2.1 B「工具在 dev 覆寫中 → 1 提示先 undev」（remove 列有、p8 名詞表有，p7 B 路徑也沒畫）
  (opt) [可讀性] p1_th: 表格用到 tracked、引擎 ref、apt 語意、git revert、rm -rf，本頁名詞表沒有這幾個詞
  (opt) [內容一致性] p1_pend: proposal_v2.md 在本輪期間新增 v2.4（全部[定]：--protocol、結束狀態 3、薄殼第一行自描述且 gen/.stamp 只記引擎 ref、Q14/Q15 拒絕過狀態、prune…），全部圖面仍以 v2.3 為準（例：p2 gen/.stamp 內容、p1 結束狀態 0/1/2），需拍板是否納入本輪

## 契約 v2：專案裡的檔與 version.toml: must_fix 7 / optional 1
- [顏色] t_root: 「專案/」根節點是白底黑框，圖例只有綠框（進 git）／灰虛線／黃底綠框，沒有這種樣式
- [排版] p2_my_h2 及該欄儲存格: 把 gen/ 下三種寫入規則不同的檔案合成一欄，未達「一格一個檔案」
- [排版] p2_mx_r5c0: dev／undev 合成一列，建立與撤除覆寫的不同動作混在同一組格子
- [可讀性] t_ver, p2_reno: 使用 PR，但本頁名詞表未解釋
- [內容一致性] t_vl, p2_mx_r1c2: uninstall 刪 local 檔寫成無條件動作，漏掉 v2.2 E／v2.3 §6「未知或被改過則保留」條件
- [內容一致性] t_gi: 寫入者只列 install，漏掉自身升級重產 .vendor_kit/.gitignore，與 p7b s13 不一致
- [內容一致性] p2_rule: 不進 git 的例外清單漏掉 .tmp.*，與同頁 t_gi 忽略規則及 remove／uninstall 日誌位置不一致
  (opt) [可讀性] t_entry: 樹狀圖多格寫「寫：引擎 launcher-gen」，本頁名詞表沒有 launcher-gen（只在 p4 定義）

## 架構圖 v2：主機、引擎模組、registry: must_fix 10 / optional 1
- [可讀性] h4: 啟動器方塊內寫三步順序鏈（grep → docker pull/create/cp → docker run），架構頁不該有順序鏈，應像引擎模組一樣拆成最小單元小白框
- [顏色] tmp: 「暫存目錄 <tmp>」與 g2「工具命名空間 just <repo>」是白底黑框圓角，本頁圖例沒有這種樣式（白小框只定義為最小單元）
- [排版] h4: 仍含 grep → docker → run 操作順序，違反架構頁只放模組、最小單元與資料流
- [排版] pull_dist, run_cli, w_user, w_just, w_shell: 線上標籤描述執行命令或修改動作，而非模組間傳遞的資料
- [排版] m_ver_u3: 「指紋」與「進度日誌」兩個最小單元放在同格
- [排版] f_bl, f_shell, f_gen, f_repo: 各自把多個檔案或不同種類產物合在一格，違反第 7 條
- [顏色] p4_lg0, g_dist: 圖例把紫色限定為「引擎容器（image）」，實際也用於工具 image，圖例定義與使用範圍不一致
- [可讀性] CI／runner／tar 相關文字: 名詞表未完整解釋 CI、runner、tar，讀者須借用其他頁知識
- [內容一致性] w_vl: 標成「讀」卻由 version 模組指向 local 檔，資料方向與讀取意義相反，也未呈現 dev／undev 的寫入關係
- [內容一致性] w_ver: 用單向箭頭表示「讀寫」，與本頁雙箭頭表達往返的圖例不一致，無法辨識輸入與輸出
  (opt) [顏色] p4_lg3: 本頁「紅底＝引擎模組」「紅底紅粗框＝啟動器」，但其他頁紅橢圓＝錯誤終止、白底紅粗框＝不變量，跨頁同色不同義，初次閱讀會混淆

## 流程 v2：bootstrap.sh + install: must_fix 8 / optional 3
- [可讀性] i4: 「flock 專案目錄 → 產薄殼四檔到暫存」一格兩件事（上鎖、產檔），要拆
- [內容一致性] i4b: 寫「baseline/ 不動」且流程沒有建 baseline/ 的步驟，但 p1 install 列、p2 表 B（install→建空目錄）、本頁名詞表都說 install 建空的 baseline/
- [排版] ae19: a11「否」→a13 的水平線只離 a12 紅橢圓底部 10px，看起來像「1：明列已完成／未完成」直接接到「0」；同型問題：ie18 附近、p5b ce9/ce39、p7 be28、p7b se9
- [排版] i4, i4b, i4f: 拿鎖與產生檔案、重產多個檔案及多檔產物仍各自合在一格
- [可讀性] i9: 「冪等」未在本頁名詞表解釋
- [內容一致性] a8b: install 成功前就寫 local 覆寫，失敗路徑未清除此檔，不滿足「第一次 install 失敗不留半成品」
- [內容一致性] i4qn: 把「沒有 gen/.stamp」等同第一次安裝，但該檔不進 git，重新 clone 時同樣不存在，不能據此跳過既有薄殼保護比對
- [內容一致性] i4b 與後續失敗出口: 已重產正式位置薄殼後，失敗處理仍只描述丟棄暫存，未涵蓋已寫入檔案的恢復
  (opt) [可讀性] i7: 白色步驟框內寫「→ 0」當結束，沒有綠色終點橢圓，與其他分支終點畫法不一致
  (opt) [可讀性] a9f: a9f、a10f 一個檔案框列四、五個檔（每格一個檔案）
  (opt) [排版] ie5: i4→i4q、i4d→i5、a3→a5 因上下格未對齊而多出折點（不該折的折）

## 流程 v2：add: must_fix 10 / optional 1
- [排版] c6x: 橢圓文字以外框寬度換行，文字超出橢圓輪廓：c0、c6x、c11x、c13y（check_overflow 用內接矩形估，但 draw.io 實際以整個 bounding box 換行，需加 spacing 或縮短文字／加寬橢圓）
- [可讀性] c11: 一格多件事：c11（flock → 重驗指紋）、c15（展開到 cache ＋ 寫印記）、c20（問 → append → 記 metadata）、c9（pull→create→cp→rm）、c2（讀、查、輸出）
- [排版] ce39: c23b→c24 的水平線緊貼 c23x「失敗→1」橢圓底部，看起來像失敗接到成功；ce9（c5t 否→c6）同樣貼著 c6x
- [排版] cf_l, cf0, cf1: 標題 y=40 高 40，下方內容從 y=70 開始，XML 配置有 10px 重疊
- [排版] c9, c11, c15, c20, c21: 分別把多個 docker 動作、拿鎖與重驗、cache 與印記寫入、詢問與 append、baseline 與 metadata 寫入合在一格
- [可讀性] c1: 使用 tar／docker load，本頁名詞表未說明離線包及載入的意思
- [內容一致性] c14: 以「CI 且無 -y」判斷 dry-run 失敗，會讓 CI 帶 -y 的 tracked 修改預覽回 0，違反 v2.3 §7
- [內容一致性] c13 → c15, c23b: 第一個寫入前沒有建立進度日誌的節點，結尾卻刪除日誌，未落實 v2.3 §6
- [內容一致性] c20: 詢問後直接接 append，沒有拒絕分支，未表達使用者不同意時不得修改
- [內容一致性] c12: 只有 dest 檢查，漏掉工具命名空間撞名時 add 必須拒絕的檢查
  (opt) [排版] c9: c9、c10 文字貼到框邊（幾乎無邊距）

## 流程 v2：sync（每次 just 都跑）: must_fix 8 / optional 2
- [排版] n3n: 橢圓文字超出輪廓：n3n、t3a、t4r、z2
- [可讀性] m2: 一格多件事：m2（flock → 重驗指紋）、m3（展開 ＋ 寫印記）、m0（pull→create→cp→rm）
- [排版] m0, m2, m3: 仍分別合併多個 docker 動作、拿鎖與重驗、展開 cache 與寫印記
- [排版] m3f, n2: 同一個檔案格包含多個不同檔案，不符第 7 條
- [可讀性] 引擎覆寫相關元件: 使用 image ID，本頁未解釋它與 tag／digest 的差別
- [內容一致性] z0 及通往快路徑的判斷鏈: 未檢查 gen/tools.just 缺失或需重生，可能在 cache 全部有效時直接回 0，與 sync 負責重生 tools.just 的契約不一致
- [內容一致性] p6_tv0: 可寫範圍描述成 cache 與 tools.just，漏掉本頁 m3 寫入的 gen/<repo>.stamp
- [內容一致性] p6_tk6: 稱 gen 下有「兩種檔」，實際已是 tools.just、引擎印記與工具印記三種，搬遷前分類殘留
  (opt) [可讀性] z0: 待辦清單含「要重生 gen/tools.just」，但前面的判斷鏈沒有任何一格判斷 tools.just 何時要重生
  (opt) [排版] t2n: t2n、t1y、m0 文字貼到框邊

## 流程 v2：upgrade ── 逐檔判斷、回退、自身升級: must_fix 13 / optional 3
- [排版] s0: 橢圓文字超出輪廓：s0、s4、s5、s8、s10
- [排版] de4: 「revert 還原」線上文字壓到 d2 藍框底邊
- [可讀性] s1: 一格多件事：s1（resolve → pull → apply）、s2c（pull 新引擎 → run）、s6（grep → 比對）、s11（grep → pull → run）、s12a（flock → 重驗）、d1（resolve → pull/cp → apply）
- [排版] c_h0～c_h2, c_r0*: 表頭 y=44 高 40，首列從 y=72 開始，重疊 12px
- [排版] c_r4*／c_r5*, c_r6*／c_r7*: 前列高度增加後，下列位置未同步下移，各有 12px 重疊
- [排版] s2c, s11, s12a, s13: pull 與執行、讀 ref 與啟動、拿鎖與比對、多檔重產仍合在一格
- [顏色] s14: 成功升級後要求重跑使用紅色，但圖例只定義紅色為「錯誤終止」，未區分成功升級後回 1 的狀態
- [可讀性] s2a, s2c 等自身升級元件: 使用 resolve、GHCR、metadata 等詞，本頁名詞表未完整解釋
- [內容一致性] s2a → s2b: 缺少「引擎確實有新版」的判斷分支，圖上變成不帶 repo 就一定改第一行並要求重跑
- [內容一致性] s2b: 舊引擎第一次修改 version.toml 前未呈現拿鎖、重驗指紋與建立進度日誌；後面新引擎拿鎖不能補保護前一次寫入
- [內容一致性] s11, se11g: 宣告 local 覆寫優先、--pull never，卻仍無條件接 GHCR pull，缺少本機覆寫繞過 pull 的分支
- [內容一致性] c_in2: 把 N 指向新版 cache，與 p7 在 materialize 前比較、dry-run 不修改 cache 的執行順序衝突
- [內容一致性] c_r7c0: CI 條件仍含「無 -y」，與同列 dry-run 結果及 v2.3 §7 不一致
  (opt) [排版] c_e3: c_m→左表的線沿著表格右框往上、箭頭插進「結果」表頭，線貼框
  (opt) [可讀性] s12: 同一判斷 p5 寫「薄殼 ≠ 上次產物？」（是→1），本頁寫「薄殼 == 上次產物？」（否→1），兩頁相反寫法
  (opt) [排版] s11: s11 文字貼到框邊

## 流程 v2：dev / undev: must_fix 12 / optional 1
- [排版] d3b: 橢圓文字超出輪廓：d0、d3b、v8、u6x、w7
- [顏色] v8: v8 紅橢圓（錯誤終止）後面又接綠橢圓 v9，終止有出邊
- [可讀性] v2_: v2_「…不動薄殼 → 0」與 w2「→ 0，本次結束（無 → 0 提示未啟用）」把結束狀態與判斷寫在藍框內，沒有終點橢圓也沒有菱形
- [可讀性] u6b: 一格多件事：u6b（刪 local 行並拆 symlink）、u6a（flock → 重驗）、u6c（materialize＋寫印記）、d6（flock → 寫 local）、d1（test -f → docker run）、w5（grep → pull）、u5（docker 鏈）
- [排版] d1, d6, v2_, u5, u6a: 檢查與執行、拿鎖與寫入、多個 docker 動作等仍合在一格
- [排版] u6b, u6bf: 刪 local 行與拆 symlink 是兩件事、兩個修改對象，應拆格
- [排版] u6c, u6f: 展開 cache 與寫印記及其兩個產物仍混在同格
- [顏色] u4: 位於引擎泳道且是 resolve 子命令的工作，卻使用白色，與本頁「藍：引擎子命令」配色不一致
- [可讀性] hdr3, v1: 使用 GHCR、tar／docker load，本頁名詞表未解釋
- [內容一致性] u6a → u6b → u6c: 刪覆寫及拆 symlink 前沒有建立日誌，卻在 u6x 承諾可恢復，缺少 v2.3 §6 要求的實際步驟
- [內容一致性] w2: 只寫刪除 vendor_kit 行，但 p2 覆寫資料另有 image ID 欄位，未撤除成對的 ID 資料
- [內容一致性] v6 → v7: 先執行 docker run 再檢查引擎印記，與啟動器先判斷薄殼是否相符的其他流程順序不一致
  (opt) [排版] d1: d1、v6、u4、u6c、w5 文字貼到框邊；「═══ 下次 just ═══」分隔文字放在 v6 右側而非列上方，讀不出是分段

## 流程 v2：remove / uninstall: must_fix 12 / optional 2
- [排版] m11: 橢圓文字超出輪廓：m0、m5、m7y、m11（箭頭還壓到「git」）、x0、x2x、x3y、x4x、x8
- [可讀性] m10: 一格多件事：m10（刪四樣東西）、m9（flock → 重驗）、x4a（flock → 建進度日誌）、x5（刪自產檔並刪進度日誌）、x7（白框內含同意／拒絕兩條路，應是菱形）
- [內容一致性] x4a: uninstall 拿 flock 後沒有「重驗指紋」，且只畫單段 docker run uninstall（remove 有 resolve→apply 兩段），與 v2.3 §6 apply 通則和同頁 remove 畫法不一致
- [排版] m9, m9b, m10: 拿鎖與重驗、詢問與刪除、多個不同檔案的刪除仍各自合在一格
- [排版] x4a, x5, x7: 拿鎖與建日誌、刪自產檔與回報與刪日誌、詢問與分支修改仍未拆開
- [排版] m10f: baseline、cache、工具印記與 tools.just 四種修改對象放在同一個檔案格
- [可讀性] m10, p8b_tv4: baseline 只出現路徑，未解釋為「上次合併的範本副本」，一般讀者無法理解刪除的是哪種資料
- [內容一致性] m7y, x3y: dry-run 無條件回 0，缺少「CI=1 且需改 tracked 檔 → 1 印清單」
- [內容一致性] x2b → x4a: 拿鎖前做 hash 預檢，拿鎖後直接建日誌並修改，漏掉重驗指紋
- [內容一致性] x5 → x7: 先刪進度日誌，之後才修改根 justfile，違反日誌必須最後刪除
- [內容一致性] x4 → m10: uninstall 呼叫「同上 remove」會先無條件刪整個 baseline／cache，繞過 uninstall 的 hash 保留清單，未知或被改的檔可能在 x5 之前就被刪掉
- [內容一致性] m9b, p8b_tv5: 只處理原文相同及找不到，漏掉「多處命中須保留並警告」，無法保證只刪可辨識的上次插入行
  (opt) [內容一致性] x5: x5 說「最後刪進度日誌」，但之後還有 x6/x7 刪根 justfile 那行；v2.3 §6 進度日誌應在最後一步才刪
  (opt) [排版] m6: m6、x5 文字貼到框邊

TOTAL must_fix 104; by category {'排版': 35, '可讀性': 21, '內容一致性': 41, '顏色': 7}; rejected 1