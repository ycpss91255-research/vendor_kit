# 第十三輪 Claude 三階段 must_fix 95，optional 106，rejected 2

## 14 流程 v2：bootstrap.sh（1）檢查 → 引擎 image (v1p5): must_fix 2 / optional 2
- [內容一致性] a8q: --local 值判別與 interface_spec v3.5 #164／§9.2 B1 矛盾：規格改為依序互斥（以 .tar 結尾 → 檔案；否則含 / 且存在同名檔 → 1 + 6-37；否則 tag），圖仍畫舊規則「值含 / 或以 .tar 結尾？→ 檔案存在？→ 本機也有同名 image tag？→ 6-37」（a8q／a8e／a8t 三格），且 6-37 觸發條件不再是「本機有同名 image tag」；同頁名詞 p5_tv2 也仍寫「兩者皆成立 → 6-37」
- [lint] a0l: onething：「建 log/bootstrap/ 執行紀錄」與「寫 launcher_started」是兩個動作（建檔、寫第一筆事件；紅終點 a0lx 也寫成「建不了／寫不進」兩種失敗）。拆成「建執行紀錄 log/bootstrap/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b 已拆的 s0b／s0c。
  (opt) [可讀性] ae6y: 「有」標籤放在 ae8n（x=535 的「否」線）旁而非自己的線（x=555）；兩條垂直線相距僅 20px 並行約 400px，縮圖上分不清「有」「否」各屬哪條
  (opt) [排版] ae6px: docker pull「失敗」線從 (698,1088) 往右繞到 x=1610、往下到 y=1677 再折回 1130 才進紅橢圓 a6px，橫跨整頁三折；紅橢圓可直接放在 pull 格下方

## 10 契約 v2：啟動器 ↔ 引擎契約④ (v1p3b): must_fix 1 / optional 5
- [內容一致性] p3_fast: 規則框末段「--local 值的判別：值含 / 或以 .tar 結尾 → 檔案路徑…兩者皆成立 → 1 提示用 ./ 或完整 ref 消歧」是 v3.5 #164 之前的舊規則（新規則：.tar 結尾 → 檔案；否則含 / 且存在同名檔 → 6-37；否則 tag）
  (opt) [內容一致性] s2b: s2b 位在「② docker run 引擎 resolve」分組內卻寫「只有 add／update／upgrade…查 registry」，而同頁 p3_two 把 update 列為單段（不經 resolve）、p3_envw 也寫「update 單段」；update 不會出現在 resolve 段
  (opt) [顏色] s4x: s4x 是綠橢圓（圖例：成功終點 exit 0）卻寫「終點：結束碼 0／1／2／3」，把失敗／需人處理的結束碼也畫成綠色，與圖例「紅橢圓：失敗（1）」「橙橢圓：需人處理」衝突
  (opt) [內容一致性] s1: 缺分支：s1「命中 ≠ 1 → 1」與 s0c「失敗 → 1 印 6-38」兩個失敗只寫在格內文字，沒有對應的紅／橙終點與出邊（其他流程頁如 v1p5 a0lx 都有獨立終點）
  (opt) [內容一致性] p3_self: 「自身升級的接手（§3.4）」只描述 upgrade 不帶 repo 的路徑（apply 前後 grep version.toml 第一行）；本輪已定的 E(c) 路徑（現引擎只建進度檔記目標 ref → 啟動器 grep 進度檔 → inspect/pull 目標引擎 → 目標引擎改第一行，見 v1p7bcx s12h）在契約④ 沒有任何一句，kind 表 engine 列（p3_vkt_r3c3）也只寫「apply 會把版本鎖定行改
  (opt) [排版] d2_in: 「resolve 0」線（y=340）緊貼 ③ 主機 docker 分組 g3 頂邊（y=350）橫跨整組寬度，上方 16px 又是 p3_err_e「是」線（y=324）；縮圖上三條平行橫線疊在一起，看起來像分組框的一部分

## 16 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add (v1p5ccc): must_fix 1 / optional 1
- [內容一致性] a12: bootstrap.sh 結束碼與 spec #157（codex r2 N13）矛盾：規格為「失敗那一步的碼原樣傳出（install／add 回 3 → 3、回 2 → 2、其餘 → 1）」，圖上 a12 與分組標題 bA2 都寫「任一段非 0 → 立即中止 1」；名詞 p5d_tv2 亦沿用舊 --local 判別規則（同 v1p5 a8q 問題）
  (opt) [排版] a12: 三條中止線（ae20x／ae20dx／ae23）都繞到右緣 x=1610/1624/1638 再折回，以 14px 間距並排進紅橢圓 a12、三個箭頭擠在一起；其中 ae20dx「失敗」線（y=842）離 add 寫虛線框 a10f 頂邊只有 10px

## 15 流程 v2：bootstrap.sh（1′）docker run install (v1p5i): must_fix 1 / optional 4
- [排版] ae14y: 「需人處理？」是→「1：install 需人處理」的水平線（y≈774）與 ae15（install 回 0？ 是→續頁虛線橢圓，x=330 垂直線）在 (330,774) 交叉
  (opt) [內容一致性] a9hx: install 非 0 只畫「1」兩個終點（a9hx、a9x）；spec §1.2 install 結束碼為 0／1／3，且 bootstrap.sh 須原樣傳出（install 回 3 → 3，#157），圖上沒有 3 的出口
  (opt) [內容一致性] a9c: 誰做不清：a9c（白 = 啟動器）「依 .tmp.install 進度檔清半成品」，但 install（1′）頁 i4wx 已寫引擎在寫入失敗時「依進度檔移除已寫的檔」；兩頁都畫同一件清除，看不出是引擎清、啟動器清，還是引擎異常結束時才由 bootstrap.sh 補清
  (opt) [內容一致性] a9f_5: 一格兩檔：「config.toml 的基準版副本＋metadata」是 baseline/vendor_kit/config.toml 與 baseline/.vendor_kit.toml 兩個檔（檔案群其他格都是一格一檔）
  (opt) [lint] a9e: xref：a9e、a9f、bA1 引用「install（1）（2）」頁，實際頁名是「install（1）」「install（1′）」「install（2）」三頁，引用漏了（1′）且與任一頁名不完全對應

## 20 流程 v2：add（1）resolve → docker (v1p5b): must_fix 2 / optional 1
- [內容一致性] c2b: 缺分支：--local 路徑（c1l docker load → c1d 讀旁檔）之後仍一路進 c2b「查 tag 與 index digest」→ GHCR（c3），離線情境下 resolve 會去查 registry；且啟動器在 c1d 讀到的正式 index digest 沒有任何一條線／參數進入引擎 resolve（c1），digest 怎麼寫進 version.toml 在圖上斷掉
- [lint] c0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/add/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [顏色] c1x: 「1 + 6-24：--local 只收存在的 .tar」畫成橙（需人處理），但 spec §6 把 6-24 歸類為「失敗」（§0 也列 6-24 為紅）；同頁名詞 p5b_tv5 更明寫「→ 1 + 6-24，橙」，與圖例／規格的紅橙定義不一致

## 11 契約 v2：CI 契約⑤ 與驗收矩陣 (v1p3c): must_fix 1 / optional 1
- [lint] c_d: onething：「release：正式 GHCR tag vN、Git tag、資產」一格三件事；且本頁名詞 p3c_tv7 明寫「Git tag vN 是 repo 上的另一個物件，圖上分開標」（v2.15-15），與此格自相矛盾
  (opt) [內容一致性] p3c_tv4: 名詞「release-test = 對剛發佈的 image…再測一次」「release = 發佈版本（push 多架構 image…）」與流程不符：流程已改為候選 tag（c_rc）→ release-test（c_e）→ 驗收（c_f）→ release（c_d，imagetools create 打正式 tag、不重 build），release-test 測的是候選、發生在 release 之前

## 13 架構圖 v2 (v1p4): must_fix 2 / optional 3
- [排版] p4_num: 右上便條 p4_np（x 1000–1600）壓住契約編號列 p4_num（x 40–1240）右段，縮圖上文字在「interface_」處被截斷看不到
- [排版] w_cfg_l: 線標籤「下線：固定寫法的 keep 行（grep）」落在外框底邊與圖例列（p4_lg4／p4_lg5，y=1939）之間僅約 10px 的縫，縮圖上貼到圖例框頂邊、像是圖例的一部分
  (opt) [內容一致性] h4: 啟動器讀取的資料流不完整：config.toml 的 grep 有畫（w_cfg_l），但啟動器 grep version.toml／version.local.toml 取引擎 ref（單元 h4_u0_0）沒有 f_ver／f_vl → h4 的線；E(c) 升引擎時啟動器 grep 進度檔的目標引擎 ref（v1p7bcx s12h）也沒有 f_tmp → h4 的線，h4 責任單元亦未列
  (opt) [內容一致性] mount_dist: 掛載路徑自相矛盾：mount_dist、p4_np、p4_tv4 寫「.tmp.dist.<id>/ → /dist/<repo>」，同頁 p4_tv5 與契約④ p3_run 則是「.tmp.dist.<id> → /dist（其下 <repo>/ 子目錄）、<dir>/dist → /dist/<repo>（本機覆寫）」
  (opt) [lint] m_prog_u0_1: termcov：「flock」（m_prog_u0_1）與「gen/.stamp」（m_shell_u1_1、f_gen_f1）第 0 頁與本頁名詞表都沒有；其餘 termcov warn（薄殼、resolve、cache/、metadata、6-xx 訊息碼等）第 0 頁已有或屬 §6 訊息編號引用，不成立

## 17 流程 v2：install（1）薄殼 (v1p5c): must_fix 1 / optional 1
- [lint] i0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/install/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [內容一致性] i1: 就地執行 just vendor_kit install（i0 起點）時，主機檢查後直接 i1「docker run <引擎> install」，缺「grep 版本鎖定行取引擎 ref → docker image inspect → 無才 pull（失敗 6-24／6-31）」步驟；便條 pend 卻寫「引擎 image 一律先 docker image inspect」，且 sync 頁（v1p6 n1／n1i／n1p）有畫

## 19 流程 v2：install（2）根 justfile 與 .dockerignore (v1p5cc): must_fix 1 / optional 1
- [可讀性] i11f: justfile 檔案框第一行「…recipe 本體 tab 縮排）」溢出虛線框右緣，被右側兩條垂直匯流線（ie12sr／ie13br／ie18r，x=1610）壓過，且 v2 小標蓋在文字上；框寬 360 不夠或需換行
  (opt) [內容一致性] i7: i7「無：建 justfile（四行）」與 ign「無：建 .dockerignore（四行）」都是寫檔，但沒有指向檔案格 i11f／igyf 的「寫」線；同頁 i11、igy 的 append 分支有畫，圖例又規定「指向檔案 = 寫入」，新建分支看起來像沒寫檔

## 06 契約 v2：目錄樹與檔案範例 (v1p2): must_fix 0 / optional 1
  (opt) [lint] t_ver: termcov：「Renovate」在 t_ver 出現，第 0 頁與本頁名詞表都沒有定義（只在 p3c 有）

## 09 契約 v2：下游 repo 契約③ (v1p3): must_fix 0 / optional 1
  (opt) [內容一致性] -: v1p3（契約③）與 v1p5cw（install（1′））對照 spec v3.5 與 codex 第十二版條目後沒有發現問題；v1p3d 為純表格頁未審

## 21 流程 v2：add（1′）apply 前置 (v1p5bcc): must_fix 1 / optional 3
- [內容一致性] c11a: flock 專案目錄（60 秒）沒有逾時失敗出口；spec §3.1／§6 定為 60 秒逾時 → 1 + 6-26（離線包頁 v1p16ccc 有畫，本頁缺）
  (opt) [lint] c9q: onething：菱形同時問「resolve 回 0」與「vk-resolve/1 文法合法」兩件事，紅終點 c9qx 也混了「1 + 6-30」與「resolve 非 0 原碼傳出（可能是 2／3，屬需人處理橙）」兩種結果
  (opt) [內容一致性] extract：docker create <image> /x → cp c:/dist/. <tmp>/<repo>/ → rm: 一格三個動作（create → cp → rm）；v1p6c 同名 extract 格同樣情形，若要守一格一事需拆或改成「extract（見名詞）」
  (opt) [lint] c9qx: onething：紅終點混兩種結果（「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」結束碼不同），根源是菱形 c9q「resolve 回 0 且 文法合法？」一格兩個判斷。建議拆成「resolve 回 0？」→ 否：「原碼傳出（不讀 stdout、不跑 docker／apply）」與「vk-resolve/1 文法合法？」→ 否：「1 + 6-30」，同 v1p3b 獨立的 p3_rx。

## 22 流程 v2：add（2）apply 寫入段 (v1p5bc): must_fix 0 / optional 2
  (opt) [內容一致性] c21c: add 對新檔不問「要建嗎」（無 → 直接建），本頁寫「新檔被拒才 declined」是 upgrade 才有的情況，add 頁不會發生
  (opt) [排版] ce38a: 最左的「失敗」線（x=2）幾乎貼著泳道容器左邊框走，縮圖下像雙重邊框；三條失敗線可統一往右挪

## 23 流程 v2：sync（1）啟動器快路徑 (v1p6): must_fix 4 / optional 4
- [內容一致性] nqr: 快路徑條件漏掉 spec §3.6（codex r2 #55 已採納）的「每個工具的 cache/<repo>/ 存在（目錄或 symlink），印記在而 cache 被刪 → 不走快路徑」；名詞表 p6_tv0 同樣缺
- [排版] ne5pv: 「無：docker pull」→ 跨頁橢圓的直線（x=530）正好擦過「覆寫中且 .Id ≠ 記的 image ID？」菱形右頂點，看起來像 pull 也進了那顆判斷；同一出口另一條「失敗」線（ne5x）的標籤壓在 pull 框右下角上
- [排版] ne5q: 「快路徑」菱形 → 「是：執行紀錄寫 sync_fast_path」的線從菱形左下邊緣懸空起步、先下再左再下多折一次，「是」標籤被線穿過並貼到框的 v2 小標；框離菱形太近（28px）
- [lint] n0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/sync/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [內容一致性] n1i: 本機覆寫（vendor_kit=）時 spec §3.1 規定「不 pull」、inspect 無此 image 即失敗；本頁「無」一律走 n1p docker pull，覆寫且本機無 image 的情況會去 pull <tag>
  (opt) [內容一致性] n1: grep 版本鎖定行「命中須恰 1」沒有命中 0／重複 → 1 的出口（spec §3.1 引擎 ref 取得）
  (opt) [顏色] n1vx: 紅終點文字附下一步指令「請 undev 或重新 dev」，依 §0「需人處理 = 印指令」應為橙；若視為驗證不過（紅）則文字不該帶指令
  (opt) [lint] n1px: termcov：6-24／6-31 出現在終點但本頁名詞表沒有對應條（其他頁如 v1p5bcc 有列）

## 24 流程 v2：sync（1′）引擎 resolve (v1p6cc): must_fix 2 / optional 3
- [排版] te15y: 「是：下一個工具」回圈的水平段（y=511）擠在「CI 模式」與「覆寫兩種」兩張便條之間（上下各只 10px），並碰到「覆寫兩種」便條的 v2 小標
- [排版] te0／te3／te3q／te6／te16: 五條「菱形右頂點 → 右側藍框」連線只有 20px 長，「是」「否」標籤擠在菱形尖端與框邊之間、貼到目標框（且與框上 v2 小標相鄰）；右側框應右移或把標籤放到線上方
  (opt) [內容一致性] z0q: 待辦為空 → 直接 0（apply|no），跳過 z1 產生指紋；spec §3.3 規定 apply|no 時 stdout 仍須恰 1 筆 fingerprint（範例 3），啟動器驗完文法才 0
  (opt) [內容一致性] p6r_tv7: 名詞「6-33」只寫「update 結束 1」，但本頁 njx 就是 sync 印 6-33 結束 1（spec：sync／update 皆 1，help 仍 0）；v1p6 p6_tv8、v1p6c p6c_tv6 同一條相同
  (opt) [顏色] t3mx: 紅終點文字附下一步指令「請 git checkout 或重新 add <repo>」，依 §0 需人處理應為橙，或去掉指令維持紅

## 25 流程 v2：sync（2）apply (v1p6c): must_fix 1 / optional 4
- [內容一致性] m2a: flock 專案目錄沒有 60 秒逾時 → 1 + 6-26 的失敗出口
  (opt) [內容一致性] m3vd: resolve 頁已把「驗不符 → 重裝一次 + 再驗」列為待辦的工具，到本頁重裝後再驗不符又走 m3vn 重裝一次，合計會重裝兩次，與 v2.15-17「不符才重裝一次，再驗仍不符 → 失敗」不一致
  (opt) [lint] m0q: onething：同 v1p5bcc c9q，一個菱形問兩件事、紅終點 m0qx 混「1 + 6-30」與「原碼傳出（可能 2／3）」
  (opt) [排版] me4vn: 「逐檔驗？」的「否」回圈線緊貼「1：重裝後仍不符」紅橢圓右側（20px）與下緣（10px）繞過，縮圖下看起來像連到那顆橢圓
  (opt) [lint] m0qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 26 流程 v2：upgrade ── A. Renovate 路徑 (v1p7): must_fix 0 / optional 2
  (opt) [內容一致性] a4f: ②～⑤ 四步畫成全部串完才判「任一失敗？」，與 spec §7.1「一關過才下一關、整體結束碼 = 第一個失敗步驟」及終點文字「第一個失敗即停止」不符
  (opt) [lint] a4q: termcov：6-13、6-33 出現在菱形但本頁名詞表沒有對應條

## 27 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker (v1p7c): must_fix 1 / optional 3
- [lint] b0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/upgrade/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [內容一致性] b7c: 查 registry 只畫「需憑證但沒有 → 6-3」，網路／回應／解析失敗 → 1 沒有出口（v2.15-16 對 update 已定分類，upgrade 查最新版同樣會失敗）
  (opt) [lint] b7q: termcov：6-24 出現在菱形文字但本頁名詞表沒有對應條
  (opt) [排版] be1q／be2／be6: 連續四顆菱形中心不對齊（x=880／920／920／815），每段連線都多出一個小折（先橫 40px 再往下），不該折的折了

## 28 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 (v1p7ccc): must_fix 2 / optional 6
- [內容一致性] b10a: flock 專案目錄沒有 60 秒逾時 → 1 + 6-26 的失敗出口
- [排版] be11y: 「有」線從 inspect 菱形右出、繞到 image 框右外側（x=1310）再折回 y=593 橫穿 pull 框與 image 框正下方（各只離 18 單位）、與「拉 /dist」線平行貼近，最後併入 pull→extract 的垂直線；縮圖看起來像從 image 框底出來，太繞
  (opt) [內容一致性] p7cp_tv11: 名詞「命名空間撞名」仍寫「→ add 回 1 拒絕」，本頁終點 b10nx 已改為「upgrade 回 1」（codex r12 #2 只改了一半）
  (opt) [lint] b11y: termcov：6-6／6-7／6-8 出現在終點但本頁名詞表沒有對應條
  (opt) [lint] b8q: onething：同 v1p5bcc c9q，一個菱形問兩件事、紅終點 b8qx 混兩種結果
  (opt) [排版] be17: 「CI 模式且需改…？」（中心 910）與「--dry-run？」（寬 240，中心 860）不對齊，否線多一個折且「否」標籤落在折點；b10c（中心 920）→ b12（910）也差 10
  (opt) [內容一致性] b8b: 一格三動作：「extract：docker create → cp → rm」（v1p7bd 的 d1c 同樣）；若 extract 視為一個單位可接受，否則應拆
  (opt) [lint] b8qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 29 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 (v1p7cc): must_fix 3 / optional 5
- [內容一致性] b14pc2: 「記 conflicts」後直接接跨頁出口 b14z，繞過 b14w「通過的檔逐檔原子替換」；只要有一檔解析失敗，其他通過的檔就不會被寫入，與 spec §4.3「解析失敗 → 2 留原檔（只該檔）」不符
- [排版] be23pc: 「可解析格式：重新解析失敗？」左尖（x=900）到「是：該檔留原檔」框右緣（x=880）只有 20 單位，「是」線標疊在箭頭與框緣上
- [內容一致性] b10f: 一格兩事：「(0) 判定已解 → 清除 metadata 的衝突狀態」是一個判斷加一個動作，應拆成判斷菱形＋清除步驟
  (opt) [內容一致性] b14s: 呼叫「逐檔判斷」頁只寫在步驟文字裡，沒有白虛線出入口；v1p7b 的 c_in「來自 B（2）」與 c_ask／c_skip「續 B（2）」在本頁找不到對應橢圓（v2.15-3）
  (opt) [lint] b14m: onething：「暫存合併完成」與「TOML／just 重新解析」兩件事在同一格
  (opt) [lint] b14r: termcov：6-6／6-8 出現在規則框但本頁名詞表沒有對應條
  (opt) [排版] be22y: 「結果 = 要問？」「還有下一個檔？」菱形（寬 200，中心 840）與 360 寬藍框（中心 920）不對齊，be22y／be23m 各多一個 10 單位小折且「是」「否」標籤落在折點；be23pq／be23z 同樣因 b14pq 中心 1000 與 b14m 中心 920 不對齊而折
  (opt) [內容一致性] b14m: 「否：暫存合併完成 → TOML／just 等可解析格式重新解析」一格含狀態與重新解析動作兩件事，建議只留「重新解析」

## 30 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 (v1p7cccc): must_fix 1 / optional 1
- [排版] be26xa: 兩條「失敗」線往右繞到 x=1624／1610 再下到紅色橢圓：x=1624 已超出泳道右邊界（1620）被裁切，x=1610 剛好壓在泳道邊框與右側虛線檔案框、Q27 便條的 v2 小標上；「失敗」線標又貼在來源框右下角被框線與向下箭頭蓋住
  (opt) [lint] b18r: termcov：6-14 出現在規則框但本頁名詞表沒有對應條

## 31 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 (v1p7b): must_fix 3 / optional 0
- [內容一致性] q9: declined_hash 只在 state=declined（q3b）檢查；已納管 managed／appended 檔拒絕過（state 不變、只記 declined_hash）且 N 的 hash 仍相同時，本圖會再問一次，與 v2.15-18／spec §4.3「declined_hash 相同不再問（印 6-6／6-8）、N 變才問」矛盾
- [排版] ce_q1cy: 右側四條「是（要建 X 嗎）」「是（再問要建 X 嗎）」「是（要替換嗎？）」「是（二進位換成新版？）」線標都落在轉角處，被 x=1230 的垂直匯流線穿過；第一個還貼到「N = 目標版範本」虛線框左下角
- [排版] ce_9y: 最後一個菱形「是」線標（930,1488）剛好壓在右側匯流線的水平段（y=1488，930→1230）上

## 32 流程 v2：upgrade ── D. 回退 (v1p7bd): must_fix 2 / optional 1
- [排版] de1e: 「下次 just…」框右出到「sync resolve」框左入的線自動繞成 Z 字雙折（720→705 再下），不該折的折；改成底出頂入或加路點
- [排版] de2y: 「有」線同 v1p7ccc：繞到 image 框右外側 x=1310 再折回 y=607 橫穿 pull 框與 image 框下方後併入 pull→extract 垂直線，太繞且像從 image 框出來
  (opt) [內容一致性] d2c3: 回退後的 sync 是「版本變動那次」，依 v2.15-17／sync（2）頁 apply 後必逐檔驗證，本頁寫印記後直接重生 tools.just，沒有驗證步驟

## 33 流程 v2：upgrade ── E. 升引擎 (a)(b) (v1p7bc): must_fix 2 / optional 3
- [內容一致性] s2b: flock 專案目錄沒有 60 秒逾時 → 1 + 6-26 的失敗出口
- [lint] s0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [內容一致性] s2h2: 「第一行變了且 == 計畫的 engine？」的「否」同時包含「未變」與「變成非計畫值」，後者依 v2.15-7／§3.4 屬 6-2b，本頁一律落到 s2hx「apply 未改第一行」
  (opt) [排版] se2dq: 「resolve：完整預檢」藍框（中心 810）與「任一工具預檢不過？」「否 → 引擎有新版？」菱形（中心 750）不對齊，se2dq／se2n 各多一個小折；se3 的「是」標籤貼著 x=610 垂直線
  (opt) [排版] se6y: 「有」線同前：繞到 image 框右外側 x=1230 再折回 y=875 橫穿 pull 框與 image 框下方後併入 pull→extract 垂直線

## 36 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） (v1p7bccc): must_fix 5 / optional 2
- [內容一致性] s12jn: 缺分支：「否：建進度檔 .tmp.upgrade」只有一條「寫」線到檔案框 s12jnf，沒有往下的執行線；從 E(c)（1）目標 = 現 ref 進來、薄殼不符的「同引擎重產」路徑在這裡斷掉，接不到 s12jy／s13（spec §1.2 (b)：否 → 建進度檔 → 用現引擎重產薄殼）
- [內容一致性] s13gy: 缺分支：三方合併格內嵌「要改先問 6-22」，但沒有像 s13gp→s13gpa 那樣的「同意？」判斷與拒絕出口（只有 tty 小標 s13gy_tty）；下游使用者拒絕合併時流程不明，直接流向 s13gc→s13gw 原子替換；同時一格含「合併」與「詢問」兩件事
- [排版] s12jn: 「否：建進度檔 .tmp.upgrade.<id>.toml」框（x=825）壓在「是 → 第一行已是本引擎 ref？」菱形右尖（菱形到 x=860）上，兩元件重疊，看不出建進度檔後接到哪裡
- [排版] s13gp: 「否：問「要建 config.toml 嗎」」框（到 x=820）被「是：三方合併」框（從 x=760 起）蓋住，文字被截成「config.tom」；「無tty→6-4」小標又疊在三方合併框左上角並蓋住「是」線標，整區擠成一團
- [排版] se15jy: 「是」線（第一行已是本引擎 ref → 重產薄殼五檔）與「失敗」匯流線、「同意？否」線全走同一條 x=610 垂直線：是線 712–846、失敗線 951–1710、同意否線 1306–1456 完全重疊在失敗線上，縮圖看起來像「是」直接通到失敗橢圓
  (opt) [lint] s13gw: onething：「config.toml 原子替換」同格附「拒絕建 → 略過、用預設」，一格含寫入與條件略過兩件事（s13gpa 否 直接接到這格）
  (opt) [內容一致性] s13gcx: 一格兩事且重複：「留衝突標記／留原檔」加「metadata 記 conflicts」，後者與後面的 s13gm「寫 metadata baseline/.vendor_kit.toml：state／conflicts」重複

## 37 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） (v1p7bccd): must_fix 2 / optional 3
- [內容一致性] s13k: 誰做／讀哪個檔：啟動器判斷「本次換了引擎（進度檔的舊 ref ≠ 本引擎）」，但進度檔已在 s13d 由引擎刪掉（最後一步）後引擎才結束，啟動器此時讀不到它；§3.4 的依據是啟動器在 apply 前後各 grep 一次第一行，不是進度檔
- [排版] se18x: 「重生 gen/tools.just」的失敗線（x=610，404→502）與「成功：刪進度檔」出口線（x=610，468→646）在同一條垂直線上重疊 468–502，再加上下方「第一行 == 計畫？是」線也走 x=610（762→979），三段共線，分不清哪條線接哪裡；「失敗」標籤擠在線與框之間
  (opt) [內容一致性] s13q: 「引擎結束 = 失敗（非 0 且非 6-2／2）？」把訊息碼 6-2 當結束碼：1 + 6-2 與重產失敗的 1 結束碼相同，啟動器如何分辨（進度檔是否仍在？）沒有畫出來
  (opt) [lint] s13c: termcov：「重生 gen/tools.just（mod? 行）」本頁名詞表沒有 gen/tools.just／mod? 條（相鄰 E(c)（2）頁有）
  (opt) [排版] se19q: 「啟動器：引擎結束 = 失敗？」的「是」線標畫在 x=270 垂直線正上方（字被線穿過），線末端併入「第一行 == 計畫？否」的垂直線中段

## 46 流程 v2：prune（1）resolve → 差集 → 刪 (v1p9): must_fix 4 / optional 1
- [內容一致性] q0l: 缺分支：格內寫「失敗 → 1 + 6-38，零寫入」，但本頁沒有 6-38 紅終點也沒有失敗線（本組其他 12 頁都有 x0x 類終點）
- [內容一致性] q6: 缺分支：只有「文法合？否 → 1 + 6-30」，沒有本輪新增的「resolve 結束碼非 0 → 啟動器不讀 stdout、原碼傳出」分支（其他頁至少在終點文字裡有寫）
- [排版] qe12z: q9y → q11z 的線走 x=30（比情境框左緣 20 還靠外），標籤「續 apply prune --dry-run（零刪除）」被頁面左緣裁切，並壓到 q10n 橢圓與 qe14 的「否」字；直線段也緊貼 q10tx／q10n 左緣
- [lint] q0l: onething：「建執行紀錄並寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/prune/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] q4: onething：「偵測活躍的 .tmp.<verb>.<id>.toml → 只列出、印 6-33」是檢查加輸出兩件事。建議拆成菱形「有活躍（未恢復）進度檔？」→ 是：「列出並印 6-33（不刪、不視為未完成交易）」→ 匯回 q5；否：直接到 q5。

## 40 流程 v2：undev <repo> (v1p8c): must_fix 6 / optional 4
- [排版] ue5y: 「有」線繞到 x≈1040 再折回，最後與 u5p→u5b 的線共用同一段直線進 u5b 頂端，兩條線疊在一起分不出來
- [排版] ue11d: u6ced（否：刪整個 version.local.toml）到 u6d 只有約 29px 的短線，箭頭幾乎佔滿間隙，看不出有一條線
- [排版] ue10x: 四條「失敗」線標籤都貼在折角上壓線，ue10x 標籤貼到 u6ced 的 v2 標、ue14x 貼到 u6g 的 v2 標；線束緊貼右側虛線框右緣
- [排版] ue15: u6g（中心 x=780）到 u7（中心 x=690）的線先直下再斜切進橢圓，出現斜線段
- [lint] u0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/undev/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
- [lint] u4b: onething：一格塞三個動作「算計畫（extract 鎖定版）」＋「算指紋」→「stdout vk-resolve/1」。拆成三格：「算執行計畫（extract 鎖定版）」／「產生輸入指紋」／「stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋」，同 v1p5b 已拆的 c2c／c2d／c2d2。
  (opt) [lint] u4qx: onething：一個紅終點同時裝兩種不同結束（1 + 6-30 文法不合；resolve 非 0 → 原碼 1／2／3 傳出），且原碼 2／3 屬需人處理（橙）卻畫紅；對應判斷 u4q 也同時驗「回 0」與「文法合法」兩件事
  (opt) [lint] u6x: termcov：終點提到「sync／update 印 6-33」，本頁名詞表沒有 6-33
  (opt) [內容一致性] u5b: 一格三個動作（docker create → cp → rm）；若 extract 視為一個名詞可保留，否則應拆
  (opt) [lint] u4qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 41 流程 v2：undev vendor_kit (v1p8cc): must_fix 2 / optional 3
- [排版] we2edx: w2ed → w2x 的失敗線繞到 x≈1580 沿 w2edf／w2gf 虛線框右緣下行（壓到框線與 v2 標），再於 y≈1245 橫穿 w2gf（－.tmp.undev 進度檔）框內回到 w2x
- [lint] w0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] w1qx: onething：同 v1p8c u4qx，一個紅終點含 6-30 與 resolve 非 0 原碼傳出兩種結束（後者可為 2／3，非紅色語意）
  (opt) [內容一致性] w1b: 「docker run 引擎 apply undev vendor_kit」沒有掛 vk-resolve（-v …:/dist:ro），但 w2b 重驗指紋、w2c 原 argv 與計畫一致都要讀 /dist/vk-resolve（本頁名詞表與 v1p8c u5r 都這樣寫）
  (opt) [lint] w1qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 42 流程 v2：remove（1）resolve → apply 前置 (v1p8b): must_fix 1 / optional 3
- [lint] m0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/remove/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] m8qx: onething：同 v1p8c u4qx，一個紅終點含 6-30 與 resolve 非 0 原碼傳出兩種結束
  (opt) [排版] —: 本頁沒有問題
  (opt) [lint] m8qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 44 流程 v2：uninstall（1）resolve → apply 前置 (v1p8bc): must_fix 1 / optional 3
- [lint] x0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/uninstall/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] x1qx: onething：同 v1p8c u4qx，一個紅終點含 6-30 與 resolve 非 0 原碼傳出兩種結束
  (opt) [排版] —: 本頁沒有問題
  (opt) [lint] x1qx: onething：紅終點混「1 + 6-30：stdout 文法不合」與「resolve 非 0 → 原碼傳出」兩種結束碼；對應菱形一格兩判斷。建議拆成兩個菱形、兩個終點（同 v1p3b p3_rx）。

## 34 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） (v1p7bcc): must_fix 3 / optional 2
- [排版] s12jr: 「是：恢復：目標 = 進度檔記的目標引擎 ref」框只有 100×63，且從 x=900 起壓在「有未完成的 .tmp.upgrade」菱形右尖（到 x=969）上；箭頭反向穿過框內文字，「是」線標與框文字疊在一起，讀不出來
- [排版] se12u: 「否 → CI 模式？」的否線在 y=1556 從左側繞到「否：查 registry」框頂，但「是：不查 registry」框底（1546）與查 registry 框頂（1566）只差 20，縮圖看起來像「不查 registry」接著流進「查 registry」；另 se12d2v／se12d1n 的「是」「否」線標剛好落在右側匯流線的水平段上（壓線）
- [lint] s10l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [內容一致性] s12jr: 順序：恢復路徑（s12j 是 → s12jr → s12v）跳過「薄殼 == 上次產物」（6-28）檢查；spec §1.2 (b) 前置是先驗薄殼被改再恢復，且 E(c)（2）頁 s12n 便條宣稱「已在 E(c)（1）頁拿鎖後、任何寫入前驗過」，對恢復路徑不成立
  (opt) [排版] se12s: 「有未完成的 .tmp.upgrade」菱形（寬 349，中心 794）與下方菱形（寬 260，中心 750）中心不對齊，否線多一個 10 單位小折；「否」標籤落在折點上

## 35 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） (v1p7bcx): must_fix 0 / optional 3
  (opt) [lint] s12j: onething：一格含「建進度檔」、隱藏判斷「已有 → 沿用」與「→ 引擎結束」三件事；引擎結束依圖例約定已隱含在 docker run 格
  (opt) [排版] se12hy: 本頁其餘無問題；只有「有」線同樣繞到 image 框右外側再折回併入 pull→覆寫 垂直線，但此頁間距較大（離框 60 單位），可讀
  (opt) [lint] s12j: onething：「建進度檔 .tmp.upgrade.<id>.toml（…）→ 引擎結束」把寫檔動作和「引擎結束（交回啟動器）」合在一格。建議把「引擎結束」獨立一格（或改成到 s12h 的線上文字），本格只留「建進度檔 .tmp.upgrade.<id>.toml（記舊／目標引擎 ref、image ID、pending；已有 → 沿用）」。

## 43 流程 v2：remove（2）寫入段 (v1p8bccc): must_fix 1 / optional 2
- [lint] m10b: onething：「刪 cache/<repo>/ 並重生 gen/tools.just」是刪一物、重生另一物兩個動作。拆成「刪 cache/<repo>/」＋「重生 gen/tools.just（去掉該工具所有 mod? 行）」，兩格都連到現有的 m10bf「同一次原子替換」註記格以保留 I17 原子性；同 v1p6c 把 m5「重生 gen/tools.just」獨立一格的做法。
  (opt) [內容一致性] m10af: 檔案框寫「－baseline/<repo>/」整個目錄，但 metadata baseline/<repo>/.vendor_kit.toml 在同目錄、要到 m10q 才決定保留（m10k）或刪（m10m，「目錄空則一併移除」）；動作格 m10a 說的是「內範本副本」，兩者不一致
  (opt) [內容一致性] m10b: 一格兩件事「刪 cache/<repo>/ 並重生 gen/tools.just」；設計上是同一次原子替換，若要守一格一事需拆成兩格並保留同一原子替換的檔案群組

## 39 流程 v2：dev vendor_kit (v1p8ccc): must_fix 2 / optional 2
- [排版] ve2: v1 → v2q（CI 模式？）的線從菱形左頂點進入，與同一頂點出去的「是」線（ve3）重疊，看起來像進出線接在一起
- [lint] v0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] v1x: endcolor：紅終點「1：本機無此 image（tar 請先 docker load）」印的是下一步指令，依 §0 屬需人處理（橙）；同類前置缺失在 v1p8 d1x「init.toml 不存在」用橙，兩頁不一致
  (opt) [可讀性] v1lx: 橙色橢圓塞五行字（「3：該 image 介面版／檔案版低於薄殼自描述首行…」），縮圖下字擠、邊緣貼字

## 45 流程 v2：uninstall（2）寫入段 (v1p8bcc): must_fix 2 / optional 1
- [排版] xe_x8: x8／x8b 往下匯入 x9a 的直線（x≈935）與 x7y → x7f 的「寫」橫線（y≈1221）交叉
- [排版] xe_x9z: x9z／x9z2／x9z3 往下匯入 x5b 的直線（x≈935）與 x9y → x9f 的「寫」橫線（y≈1589）交叉
  (opt) [lint] x9q: termcov：問句 6-34（與 x7 的 6-20）本頁名詞表沒有獨立條，6-20 只在說明文裡

## 55 流程 v2：離線包（1）bootstrap.sh --local (v1p16): must_fix 6 / optional 2
- [內容一致性] o3: --local 判別與 interface_spec v3.5 §1.1 B1（#164）不符：規格是依序互斥「以 .tar 結尾 → 檔案（必須存在）；否則含 / 且存在同名檔 → 6-37；否則 tag」，圖卻是「含 / 或以 .tar 結尾 → 檔案存在？否 → 1」——值含 / 但無同名檔（完整 ref）依規格是 tag 形，圖會判成 1 檔案不存在
- [內容一致性] o3n: 規則框 o3n 與名詞 p16_tv0 寫的仍是舊三分支（含 / 或 .tar → 檔案；既存檔且可解讀為 tag → 6-37），要同步改成 B1 依序判別
- [內容一致性] o7b: 缺 bootstrap 前置的引擎 image LABEL 最低介面版檢查（3 + 6-18 零寫入；§1.2 bootstrap.sh 前置、§7.4-6「斷網也回 3」）：load／inspect 取得 image ID 後直接續 (1′) install；線上頁 v1p5 a8p 有此格，離線頁沒有
- [內容一致性] o2s: 「建執行紀錄並寫 launcher_started（失敗 → 1 + 6-38）」只有框內文字，沒有失敗出口與紅終點；v2.15-2 保留此格的理由是它有真實分支，其他流程頁（v1p5／v1p5b／v1p6…）都畫了 --失敗--> 1 + 6-38 終點
- [排版] oe2: o2→o5 的線在 (275,700) 轉入 o5 左尖端，與 o5→o5x 的「否」箭頭（oe6x，y=700，x 270–290）重疊同一段；且 oe2 垂直段 x=275 貼著 o5x 橢圓右緣（270）走，看起來像 o2 直接接到「否 → 1 + 6-16」；oe2 應改從 o5 頂部進入或把 o5x 下移
- [lint] o2s: onething：「建執行紀錄 log/bootstrap/<ts>-<id8>.jsonl 並寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/bootstrap/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [顏色] o3bx: 「1：檔案路徑必須存在」畫紅（失敗），同一結果在 v1p5 a8ex 畫橙（需人處理：請檢查路徑）；兩頁顏色不一致
  (opt) [排版] oe3tj: 「是：tag 形（跳過 load／.digest）」線的水平段 y=1447 只高出 o7bd 便條頂邊（1454）7px，縮圖下像壓在「結果：回 image ID」便條上緣；把便條下移或水平段抬高

## 56 流程 v2：離線包（1′）docker run install (v1p16i): must_fix 1 / optional 2
- [內容一致性] o8q: 順序錯：「install 失敗？」接在 o8k「刪進度檔 = install 完成」之後，但 o8x 說「依進度檔清半成品」；進度檔已刪就無清除清單可依。失敗判斷應在寫入段之後、刪進度檔之前（失敗 → 依進度檔清半成品；成功 → 刪進度檔）
  (opt) [可讀性] o8e: 一格一事：一格列七項寫入（薄殼五檔、gen/.stamp、baseline/.gitkeep、config.toml＋基準版副本＋metadata、justfile 一行、.dockerignore 四行、version.toml 第一行）；雖引用 install 頁，仍是多件事一格，且跨頁引用只是框內文字不是白虛線橢圓
  (opt) [排版] bU: 本頁沒有問題

## 57 流程 v2：離線包（2）add --local 逐工具 (v1p16c): must_fix 4 / optional 1
- [內容一致性] o10v: 缺 resolve 非 0 分支（v2.15-4、§3.3：resolve 結束碼非 0 → 啟動器不讀 stdout、不跑 docker／apply、原碼傳出）；o10v 只判文法合不合，v1p5bcc c9q 同位置有「resolve 回 0 且文法合」兩條件
- [內容一致性] o10s: launcher_started 格沒有「失敗 → 1 + 6-38」出口與紅終點（同組其他 add 頁 c0l → c0x 有）
- [排版] oe26fx: 「≠」線（o10e2→o10ex）在 y=1236 的水平段與 oe26e（o10p2→o10e）的水平段共線重疊（x 490–620），o10ex 的入箭看起來像從 apply add 那格出來；另「逾時」線 oe26ex 的水平段 y=1283 橫穿 oe26fx 的垂直段（x≈620），兩線交叉；建議照 v1p12 的排法：逾時從 o10ex 頂部進、≠ 從右側直接進
- [lint] o10s: onething：「建執行紀錄並寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [可讀性] o10ex: 一格一事：一個橙終點同時放 flock 逾時（6-26）與指紋不同（6-12）兩種結束，來源邊也不同（o10e、o10e2）；v1p9c 同情境拆成 q12ax／q12bx 兩格

## 58 流程 v2：離線包（3）斷網 sync (v1p16cc): must_fix 5 / optional 3
- [內容一致性] w2b: we2b 把「本機覆寫 image ID 相符」也導到 w2b「docker image inspect <version.toml 正式 ref@digest>」：§3.1 規定 local 覆寫時 inspect <tag> 核 ID 後直接 docker run、不 pull；docker load 過的 image 無 RepoDigests，用正式 ref@digest inspect 會找不到 → 走 w3p pull → 斷網必失敗，與 Q26「必成功」矛盾（w3d「本機已有 image（docker load 過的）」在此路徑也不成立）。相符應直接到 w4
- [lint] w2ax: endcolor：「≠ → 1：本機 image 已被重 build（請 undev vendor_kit 或重新 dev -i）」附下一步指令，依 §0「結束的兩種語意」與圖例「橙：需人處理（印指令）」應為橙，現為紅
- [內容一致性] w0l: launcher_started 格沒有「失敗 → 1 + 6-38」出口與紅終點（其他 sync／add 頁有）
- [排版] we6x: 「≠」線（w4e→w4ex，y=1174）與 we6（w4→w4e）的末段（x 830–970，y=1174）共線重疊，成 T 字接點，≠ 橢圓的入箭看似從 docker run 那格出來；we6 改由 w4e 頂部進入
- [lint] w0l: onething：「建執行紀錄並寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [可讀性] w4e: 一格一事：「驗 image ID == metadata local_image_id；算 extract 清單與指紋」是檢查＋計算兩件事，且 ≠ 分支直接從 step 框出來而不是菱形
  (opt) [內容一致性] w4q: w4q 的條件含「無未完成交易、metadata 完成標記」，但其「否」出口只到 (3′) apply sync；依 §1.2 sync／6-33／6-13，未完成交易 → 1 + 6-33、無完成標記 → 1 + 6-13，不是進 apply。本頁沒有這兩個 1 出口
  (opt) [內容一致性] w1: 快路徑比對條件漏「每個工具的 cache/<repo>/ 存在（目錄或 symlink）」（§3.6 快路徑，codex r2 #55：印記在而 cache 被刪不走快路徑）；名詞 p16cc_tv2 同樣漏

## 59 流程 v2：離線包（3′）apply sync 先驗後重裝 (v1p16ccc): must_fix 2 / optional 3
- [內容一致性] w4r: 驗證不符後的「重裝一次」只重寫 cache/<repo>/ 與印記，沒有 gen/tools.just；I17／§4.4 要求 tools.just 與 cache 同一 apply 內原子替換，同頁 w4r0（不驗路徑）有寫 tools.just，兩條路徑不一致；檔案框 w4f 也只接 w4r0 不接 w4r
- [排版] wf3x: 「≠」線（w4l2→w4lx）在 y=428 的水平段與 wf2（w4p→w4l）水平段共線重疊（x 490–620）；「逾時」線 wf3t 的水平段 y=475 又橫穿 wf3x 的垂直段（x≈620，y 428–502），兩線交叉、≠ 標籤夾在交叉點旁；與 v1p16c 同病，照 v1p12 排法改
  (opt) [可讀性] w4v: 「逐檔 sha256 驗既有 cache（用 local_image_id 對照 index digest）」把兩種驗證混在一格：逐檔 sha256 是對印記每檔行比對，image ID ↔ index digest 對照是 resolve（w4e）已做的 image 驗證，讀者會以為 cache 檔案用 image ID 驗
  (opt) [可讀性] w4lx: 一格一事：一個橙終點同時放 flock 逾時（6-26）與指紋不同（6-12）兩種結束（v1p9c 拆成兩格）
  (opt) [lint] w4r0: onething：「從 /dist 寫 cache/<repo>/、印記」（複製取件）與「gen/tools.just」（由各 <ns>.just 重生）是兩種不同操作。建議拆成「從 /dist 寫 cache/<repo>/、印記」＋「重生 gen/tools.just（原子替換）」，同 v1p6c m5 獨立一格的做法。

## 50 狀態機 v2：交易與進度檔 (v1p12): must_fix 1 / optional 3
- [內容一致性] r2px: 「prune 特例 … → 繼續 prune（接 prune 頁）」是跨頁出口，卻畫成綠終點橢圓；v2.15-3 規定跨頁出入口一律白虛線橢圓「續「X」頁」，本頁 xrefs 也因此抓不到
  (opt) [內容一致性] r3n: 規則框把 prune 列進「可寫動詞 → 先恢復再繼續」，名詞 p12_tv4「恢復（三型）」的一般型也含 prune；與同頁 r2pn／§0 進度檔「prune 不擋、不恢復、不刪」矛盾（流程上 r2p 已先分流，只是規則文字自相矛盾）
  (opt) [可讀性] t1x: 一格一事：一個橙終點同時放 flock 逾時（6-26）與指紋不同（6-12），來源邊分別是 t1 與 t2
  (opt) [排版] t1: 本頁沒有問題（flock／逾時／≠ 三線分開走，可作 v1p16c／cc／ccc 的範本）

## 49 狀態機 v2：初始檔五態 (v1p11): must_fix 2 / optional 0
- [內容一致性] in_u: 缺 upgrade 的轉入：新版新增檔但 dest 已存在 → 不納管 state=unmanaged + 6-11（v2.15-18、§3.3「apply 對新檔只建不存在者，已存在 → 不納管 6-11」）；se_u 標籤與 in_u 只寫 add 的兩種情況，in_m 則寫 upgrade 新增檔一律問「要建 X 嗎」
- [可讀性] se_m: se_m 標籤「add：dest 不存在 → 建；upgrade：新增檔同意建」與 se_c 標籤「upgrade：拒絕建新檔」同在 y=383 同一基線、間距僅約 20px，縮圖下連成一句，分不出哪段條件屬 managed、哪段屬 declined；兩條線的水平段錯開高度或把 se_c 標籤移到其垂直段旁

## 48 流程 v2：update (v1p10): must_fix 3 / optional 1
- [內容一致性] u0l: launcher_started 格沒有「失敗 → 1 + 6-38」出口與紅終點；本頁非圖例 fills 也沒有紅色，其他動詞頁（v1p5／v1p6／v1p8…）都畫了 --失敗--> 1 + 6-38
- [排版] ue10: u6→u7f 的線標籤「否：無憑證」置於 x≈631、y≈1054，正好貼到 u7q 菱形左尖端（688,1054），縮圖下讀成「否：無憑證 查詢成功？」一句；標籤應移到線的上段（u6 下方）或把 u7q 右移
- [lint] u0l: onething：「建執行紀錄並寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/update/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。
  (opt) [lint] u7f: onething：同一格處理兩條進線（無憑證／查詢失敗）且含「分類失敗原因（認證／網路／回應／解析）」與「該目標記 1」兩個動作。建議拆成「查詢失敗：分類原因」（只接 u7q 否）＋「該目標記 1（無憑證 → 6-3；否則附分類）」（兩條進線都匯到這格）→ u8q。

## 53 流程 v2：vendor_kit release（1）build 與驗收 (v1p15): must_fix 0 / optional 2
  (opt) [內容一致性] v4b: 驗收（v4a–v4c）排在 push-by-digest／合成 index／候選 tag（release（2））之前，此時候選 C 尚無 index digest，fixture 的 version.toml 第一行寫不出正式 ref@digest（§7.4-1「第一行改為候選 C」），只能靠框內「dev -i 同一機制」繞過；與 v2.15-15「候選 image 先推候選 tag，驗收矩陣全過才打正式 vN」及本頁 pend／p15
  (opt) [排版] ve4r: 「取」線（v4a→v4r）水平段 y=671 擠在 v4a／v4g 底邊（661）與下一格 fixture 頂邊之間各約 10px 的縫裡，縮圖下像貼著 v4g 底邊走，且從 v4a 底部進出與主流程箭頭並排，方向不易辨；建議改從 v4r 左側直接水平接 v4a 右側（與「拉」線分層）

## 54 流程 v2：vendor_kit release（2）推 image 與資產 (v1p15c): must_fix 1 / optional 2
- [lint] v11d: onething：「寫 release notes … → 發布」是寫檔與發布兩個動作。拆成「寫 release notes（index digest、替代 docker run 指令）」＋「發布 Release vN」；或刪掉「→ 發布」，因下一格綠終點 v12「0：Release vN 發布」已表示發布結果。
  (opt) [可讀性] v11d: 一格一事：「寫 release notes … → 發布」把寫 notes 與發布 Release 兩個可獨立失敗的動作放同一格（v11b 建草稿、v11c 上傳已拆開，發布未拆）
  (opt) [排版] bU: 本頁沒有問題

## 18 流程 v2：install（1′）寫入 (v1p5cw): must_fix 2 / optional 0
- [排版] ie7x: 「失敗（任一步）」標籤的末字壓在「缺才建 baseline/.gitkeep」框的左邊框上
- [lint] i4wx: onething：紅終點內藏一個判斷（第一次 vs 修復型）與兩個不同動作（「依進度檔移除已寫的檔」vs「列已完成／未完成」）。拆成菱形「第一次安裝？」→ 是：紅終點「1：依進度檔移除已寫的檔、不留半成品（log/ 保留）」／否：紅終點「1：列已完成／未完成，下次可寫動詞先恢復」。

## 38 流程 v2：dev <repo> (v1p8): must_fix 4 / optional 0
- [排版] de13x: 「失敗」標籤貼在折角上，壓到下方「成功：刪進度檔」格（d6d）的 v2 綠標；de6x／de7x 的「失敗」同樣壓在轉折處的直線上
- [排版] de6x: 三條失敗線繞到最右側（x≈1590–1620）成束下行，緊貼 d6pf／d7bf／d6df 虛線框右緣與其 v2 標，de13x 橫段擠在 d7bf 與 d6df 之間幾乎貼框
- [排版] de14: d6d（中心 x=780）到 d8（中心 x=690）的線先直下再斜切進橢圓，出現斜線段
- [lint] d0l: onething：「建執行紀錄、寫 launcher_started」兩個動作合在一格。拆成「建執行紀錄 log/dev/<ts>-<id8>.jsonl」＋「寫 launcher_started（失敗 → 1 + 6-38，零寫入）」，同 v1p3b s0b／s0c。

## 47 流程 v2：prune（2）apply 清暫存 (v1p9c): must_fix 1 / optional 0
- [排版] qe18ax: 「逾時」線從 q12a 左邊出發到 q12ax，與 q12 → q12a 的來線在 y≈433、x 410–580 這段完全重疊，看起來像 T 字接頭，「逾時」標籤又剛好放在接點上