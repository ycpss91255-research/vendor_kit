# 第十輪審查（兩位 Claude，無 codex）；must_fix 22，optional 14，rejected 1

## 契約 v2：啟動器 ↔ 引擎契約④: must_fix 2 / optional 2
- [內容一致性] p3_sh: 主機命令白名單缺 spec §3.1 已列的 od、tr（產 trace_id）與 v2.13 P7 加的 mkdir、date（建 log 目錄與時間戳）；同頁流程⓪⓪格卻已用「od urandom」。  (claude+codex)
- [內容一致性] p3_fast: 快路徑前提寫「.vendor_kit/.gitignore 明列 cache/、gen/、version.local.toml、.tmp.*」漏 log/（spec §3.6、§4.5；目錄樹 t_gi 與 install(1) i4 都列了 log/）  (codex)
  (opt) [內容一致性] p3_run / p3_envw（另見 目錄樹 p2_tv12、架構圖 p4_tv12）: 把 -e VENDOR_KIT_LOG_FILE 寫成已定、頁面又標「本頁無待拍板」；spec §9.1 P8 仍列為待定（引擎如何定位 log 檔），§3.1／§5 的 -e 白名單也沒有此變數  (codex)
  (opt) [內容一致性] s0b 之後（各流程頁結束處同）: spec §1.2 通則／§4.10：每次結束前啟動器寫 log_prune、launcher_exit，引擎寫 engine_exit；契約④ 流程與所有動詞頁只畫 launcher_start／engine_start，僅 sync 快路徑畫了 launcher_exit  (codex)

## 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker: must_fix 2 / optional 0
- [排版] b2 / b1q / b2c: 「(0) 衝突檔仍含我們的標籤？」菱形沒有入線（b1q「在 dev 覆寫中？」的否分支沒接到它），也沒有「是」出線到 b2c「是 → 2：先解完衝突再重跑」；主路徑在 b1q 之後斷掉，b2c 懸空。  (claude)
- [排版] b1q / b2 / b2c: 「<repo> 在 dev 覆寫中？」沒有「否」線接到「(0) 衝突檔仍含我們的標籤？」，且「(0)」也沒有「是」線接到「是 → 2：先解完衝突再重跑」（XML 無 b1q→b2、b2→b2c 邊）；主路徑在 dev 判斷後斷掉、2 出口懸空  (codex)

## 流程 v2：uninstall（1）resolve → apply 前置: must_fix 2 / optional 0
- [排版] x2 / x2b / x2bb / x2c / x2d / x2e: 「預檢全部工具通過？」只有「否」出線；「是：算每個自產檔的 hash」「分類」「產生執行計畫」「產生詢問清單」四格完全沒有連線，「產生輸入指紋」也沒有入線，resolve 段整段懸空。  (claude)
- [排版] x2 → x2b → x2bb → x2c → x2d → x2e: 「預檢全部工具通過？」的「是」分支到「算每個自產檔的 hash」、以及「分類」「產生執行計畫」「產生詢問清單」「產生輸入指紋」五個藍格之間完全沒有連線（XML 無邊），resolve 段整段懸空  (codex)

## 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）: must_fix 2 / optional 1
- [內容一致性] s13 / s13b / s13c: 新引擎重產段只畫薄殼五檔、gen/.stamp、tools.just、刪日誌，沒有 spec §1.2 upgrade (b)／§4.9 的「config.toml 缺則建／有則三方合併（6-22 詢問）」步驟，也沒有對應的檔案框。  (claude)
- [內容一致性] 重產薄殼五檔 → 寫 gen/.stamp 之間: spec §1.2 upgrade(b)／§4.9：新引擎重產薄殼後須「config.toml 缺則建／有則三方合併（問）」再刪日誌；本頁沒有 config.toml 步驟（install(1) 有建、契約② 說 upgrade 三方合併，但流程頁缺）  (codex)
  (opt) [顏色] 「是 → 1 + 6-2b」「否 → 1：印原因」: 這兩個是重產薄殼失敗（寫入失敗）的出口，依本頁圖例應為紅色，卻用橙色；E(a)(b) 頁同樣的 6-2b 出口是紅色，兩頁不一致  (codex)

## 流程 v2：uninstall（2）寫入段: must_fix 1 / optional 0
- [內容一致性] 刪已空的子目錄 baseline/（gen/、cache/、log/、ci/ 亦同；rmdir） / .vendor_kit/ 已空？: 格子寫會 rmdir log/，且最後判斷「.vendor_kit/ 已空？→ rmdir」；但本頁名詞表自己說 uninstall 仍在寫 log 檔、v2.13 P6 定 log/ 一律保留，log/ 永遠非空，這兩格與之矛盾。  (claude)

## 流程 v2：dev <repo>: must_fix 2 / optional 0
- [排版] de1x: 「<dir>/dist/ 內有 init.toml？」的否分支線沿著「是：準備掛載 -v …」方框的左邊框往下走、再從框中間高度轉出，看起來像是從「準備掛載」格出去到「否 → 1」，線壓框且分支歧義。  (claude)
- [排版] 「<dir>/dist/ 內有 init.toml？」的「否」線 / 「是：準備掛載 -v」格: 「否」線沿著「是：準備掛載 -v …」格的左邊框重疊往下走，看起來像是從該格出去而不是從菱形出去（線壓框）  (codex)

## 流程 v2：undev <repo>: must_fix 1 / optional 0
- [可讀性] u6c: 「刪 version.local.toml 該行（最後一個覆寫 → 刪整個檔）」一格含刪行與刪整檔兩件事；undev vendor_kit 頁已拆成 w2／w2e／w2ed 三格，本頁應同樣拆。  (claude)

## 架構圖 v2: must_fix 0 / optional 2
  (opt) [內容一致性] h4: 啟動器方框寫「log 前置（先寫 launcher_start 才開始）見 p12」，但 p12（交易與進度日誌狀態機）整頁沒有任何 log／launcher_start 內容，指錯頁。  (claude)
  (opt) [內容一致性] m_log（trace_id、prune keep／days、log.sh（POSIX））／ m_lg_u0_2: 引擎容器內的 log 模組放了 trace_id 與 prune keep／days 單元，spec §4.10 說 trace_id 由啟動器產、保留清理由啟動器做、引擎不做保留清理；且 log.sh 同時列在 launcher-gen 與 log 兩個模組的最小單元，與啟動器方框內的 trace_id／log prune 單元重複  (codex)

## 契約 v2：目錄樹與檔案範例: must_fix 0 / optional 1
  (opt) [內容一致性] t_gstamp: gen/.stamp 寫成「引擎 ref ＋ log.sh hash」（install(1) i4d、E(c)(2) s13b 亦同），與 spec §4.4「gen/.stamp 只記引擎 ref、不承擔薄殼 hash」矛盾；log.sh 已列為薄殼五檔且有首行自描述，兩種機制並存需拍板。  (claude)

## 狀態機 v2：交易與進度日誌: must_fix 0 / optional 1
  (opt) [排版] re5h: 「本動詞可寫？」菱形有兩條「否」出線，接 help 的那條沒有標籤、且從菱形斜邊中段出線，初看不知道為何同一個「否」分成兩個出口。  (claude)

## 流程 v2：install（1）薄殼: must_fix 1 / optional 1
- [內容一致性] i4_3b / i4d（另見 目錄樹 t_logsh、t_gstamp；E(c)(2)「寫 gen/.stamp」格）: log.sh 被畫成無自描述首行、改把 hash 寫進 gen/.stamp（「引擎 ref＋log.sh hash」）；spec §4.5 規定薄殼每檔（拆出的啟動器檔亦同）帶自描述首行，§4.4 規定 gen/.stamp 只記引擎 ref、不承擔薄殼 hash 且不進 git，fresh clone 時 log.sh 無法比對  (codex)
  (opt) [內容一致性] i4b: spec §1.2 install 副作用含建 log/（含目錄內 .gitignore：*／!.gitignore），本頁只畫啟動器建 log 檔，沒有畫 log/.gitignore 由誰、何時建。  (claude)

## 契約 v2：CI 契約⑤ 與驗收矩陣: must_fix 1 / optional 0
- [內容一致性] p3_acc / p3_accb（標題「驗收 28 條」）: 驗收矩陣只到 28 條，spec v3 §7.4 已有 35 條（29 log 逐行 json.loads、30 argv 跳脫、31 config.toml、32 磁碟不可寫 6-38、33 bootstrap 逐 -t 中止、34 E(c) 分支、35 help 6-33）；release(1) 頁已畫 log 驗收但本頁未同步  (codex)

## 流程 v2：add（1′）apply 前置: must_fix 1 / optional 0
- [內容一致性] c10 → c11a（同型：remove(1)、uninstall(1)、sync(2) m1→m2a、upgrade B(1′) b9→b10a、undev、prune；sync(1) n1b）: spec §3.2：每個引擎子命令（resolve 與 apply 各一個容器）啟動時都先 append engine_start，失敗 → 1 + 6-38；各 apply 頁 docker run 後直接 flock、沒有 engine_start 格，sync(1) 的 resolve 也沒有；只有 E(c)(1) 以括號塞在 flock 格、E(a)(b) s2a 塞在 resolve 格，表現法不一致  (codex)

## 流程 v2：sync（1′）引擎 resolve: must_fix 1 / optional 0
- [內容一致性] ne6 之後（CI 為真且有 local 覆寫？ 之前）: spec §0／§1.2：sync 偵測到未完成交易 → 印 6-33 結束 1、不恢復；update 頁有這個菱形，sync resolve 頁完全沒有此分支（快路徑頁只把「無 .tmp.*」當作起引擎的條件）  (codex)

## 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install: must_fix 1 / optional 0
- [排版] a6p（無：docker pull）／ a8i: a1vy 文字寫「拉不到 → 1，不退回內嵌」，但「無：docker pull」只有一條線直接進 docker run install，沒有拉取失敗的紅色出口；tag 形 a8i「docker image inspect 取 image ID」本機無此 image 也沒有失敗分支  (codex)

## 流程 v2：add（1）resolve → docker: must_fix 0 / optional 1
  (opt) [排版] c9p（同型：upgrade B(1) b8p、sync(2) m0p、回退 d1p、undev）: 工具 image 的「無：docker pull」都沒有失敗／逾時出口（6-24／6-31），只有 E(a)(b)、E(c)(1)、sync(1) 的引擎 pull 有畫「失敗」分支  (codex)

## 流程 v2：install（2）根 justfile 與 .dockerignore: must_fix 2 / optional 0
- [可讀性] igq: 一個菱形同時做兩個判斷：「已含則跳過」和「問要加這四行嗎同意？」；justfile 側是分成「已含 import 那行？」與「問同意？」兩格，.dockerignore 側應拆成同樣兩格  (codex)
- [顏色] idlx / idlz（vs idl）；i7 / i11 / ign / igy: 同樣是引擎的「刪進度日誌」步驟，idl 用藍色、idlx 與 idlz 用白色；引擎實際寫檔的「建 justfile」「append 那一行」「建 .dockerignore」「append 四行」也是白色，而「插入的行記在 baseline」是藍色，藍白混用沒有規則  (codex)

## 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併: must_fix 2 / optional 0
- [排版] be22x1 / be22x1b / be22x2 / be22x3 / be22x4: 五條「否」線在左側平行貼很近，下方菱形的「否」橫線穿過上方「否」線的直線段（交叉），「否」字貼在鄰線上（壓字）  (codex)
- [可讀性] b13a（另見 逐檔判斷頁 d2c）: 「materialize 目標版：/dist → 暫存 → cache/<repo>/（原子替換）」一格含展開與原子替換兩件事；回退段 d2c「materialize 舊版 → cache/、寫印記」也併兩件事；add(2)、sync(2) 同樣步驟已拆成兩格（materialize／原子替換／寫印記）  (codex)

## 流程 v2：sync（1）啟動器快路徑: must_fix 0 / optional 1
  (opt) [排版] ne5q 的「是」標籤 / nql 的 v2 標籤: 快路徑「是」線的文字緊貼到「是：log 檔寫 sync_fast_path」格右上角的 v2 綠標，字與標籤相碰  (codex)

## 流程 v2：update: must_fix 1 / optional 0
- [可讀性] 本頁名詞（另見 離線包(1)、離線包(2)、prune；sync(1) 的 sync_fast_path／launcher_exit）: 流程格用了 launcher_start（操作紀錄檔），但 update、離線包(1)、離線包(2) 的本頁名詞沒有操作紀錄檔／launcher_start 條目（prune 只有「log/ 不在 prune 範圍」）；sync(1) 用到 sync_fast_path、launcher_exit 事件名也未列在名詞表  (codex)

## 流程 v2：upgrade ── E. 自身升級 (a)(b): must_fix 0 / optional 1
  (opt) [可讀性] 本頁名詞（E(c)(1)、E(c)(2) 同）: 三頁流程都用 6-2b，但名詞表只有結束狀態，沒有 6-2b（引擎已鎖定但薄殼未重產）的說明  (codex)

## 流程 v2：prune: must_fix 0 / optional 1
  (opt) [顏色] bP_v2（同型：update bU_v2、狀態機×2、release×2、離線包×2）: 這 8 頁群組標題右上有綠色 v2 標籤，但頁底圖例沒有「右上綠標 v2：與 v1 不同處」項目（其他流程頁有）  (codex)

## 流程 v2：離線包（1）bootstrap.sh --local: must_fix 0 / optional 1
  (opt) [可讀性] sh bootstrap.sh --local 入口格 / docker run 本機 image install 格: 「先建 log/bootstrap/ 並寫 launcher_start」與「install 失敗 → 1：清半成品、保留 log/」都藏在格子括號裡，沒有像 bootstrap(1) 那樣獨立成格與紅色出口  (codex)

## 總評（全 40 頁）: must_fix 0 / optional 1
  (opt) [內容一致性] —: 第九輪 23 項已修（架構圖線端與 .dockerignore 單元、--local 名詞、bootstrap(2) 逐 -t 中止、E(a)(b)/E(c)(1) 缺線、@tag 與 frozen 分開、s12hz 續跑入口、v9 橙、uninstall(2) 拆格、交易頁 help 出口、離線包(2) 拆格）。本輪沒有問題的頁：bootstrap(2)、add(2)、upgrade A、B(2′)、E(c)(1)、dev vendor_kit、undev <repo>、undev vendor_kit、remove(1)、remove(2)、uninstall(2)、狀態機初始檔五態、交易與進度日誌、release(1)、release(2)。但 upgrade B(1) 與 uninstall(1) 各有主路徑斷線（明顯是本輪插入 engine_start 格後沒接回），加上 log 模組漏格（apply 的 engine_start、E(c)(2) 的 config.toml、契約④ 白名單／.gitignore、契約⑤ 驗收矩陣）與 log.sh hash 與 spec §4.4／§4.5 矛盾，這 40 頁還不能交給使用者看  (codex)

## rejected
- [架構圖 v2] w_log_l / w_cfg_l: 底邊兩條平行線：上面那條是 config.toml→啟動器，下面那條是啟動器→log/，但「launcher_* 事件…」標籤貼在上面那條、「keep 正規行（grep）」貼在下面那條，線上文字與所屬線段對調 → XML：w_cfg_l（f_cfg→h4，config.toml→啟動器）走 y=1688 是上面那條，label「keep 正規行（grep）」verticalAlign=top 貼在它下方；w_log_l（h4→f_log，啟動器→lo