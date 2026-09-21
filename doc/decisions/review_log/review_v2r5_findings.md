
## 流程 v2：prune: must_fix 2 / optional 0
- [內容一致性] p9_tv6: 名詞表寫「-n/--dry-run = apply 的唯讀預覽」，Q25 選項表已無 -n 短形（規格 §10-14 明列 `-n` → `--dry-run`）
- [排版] q11: 同格包含四種資源的四個刪除命令及「失敗繼續」；至少應拆成逐類資源迴圈／單一刪除動作。

## 契約 v2：目錄樹與檔案範例: must_fix 2 / optional 1
- [內容一致性] p2_jf: 「逐字」根 justfile 範例的 `\t@just --list` 渲染後 tab 被吃掉、變成頂格，照抄就是 just 語法錯誤（recipe 本體必須縮排），與規格 §4.5 逐字四行不符（第四輪「根 justfile 兩行」項未真正修好）
- [內容一致性] p2_ver: vendor_kit = "<ref>" 範例行後附了「# 唯一正規行…」註解；規格要求正規行不得有尾端註解，此範例會被規格拒絕。
  (opt) [內容一致性] p2_pend: 「待拍板」便條仍列「version.toml vs lock.toml」，此題規格 §4.1 已定 version.toml，不該再標待拍板

## 契約 v2：啟動器 ↔ 引擎契約④: must_fix 4 / optional 0
- [內容一致性] p3_vk: vk-resolve 範例仍用具體工具名當實例：`extract|base|ghcr.io/<org>/base-dist:…` 與 `mount|robot_tools|/home/me/robot\0040tools`；規則是例子一律 <repo>（base 只准出現在「對齊 base 的 ju
- [內容一致性] p3b_pend: 宣稱 B1、F5 已依 grilling 定案，但 interface_spec §9.1 明列兩者仍待定。
- [內容一致性] p3_fast: 把 sync --verify 和 B1 判別畫成正式規則，超出目前規格。
- [可讀性] p3_fast: 一般讀者無法知道 B1、F5 尚未拍板；頁首反而明確說「本頁無待拍板」。

## 流程 v2：install（2）根 justfile 與 .dockerignore: must_fix 5 / optional 0
- [內容一致性] i7f: 「＋justfile（新建，逐字）」的 `@just --list` 渲染時前導空白被 HTML 摺掉、變頂格，逐字內容失去縮排、不再是合法 justfile
- [排版] ie13: i7（無：建 justfile）回主線的線與 ie8「是」、ie12「有」兩條垂直線交叉；ie8 的「是」字直接落在自己的垂直線上；ie22「否」標籤撞到 igx 的 v2 綠標
- [排版] i7: 同格包含建檔與印出。
- [排版] i11: 同格包含 append 與印出。
- [排版] igy: 同格同時 append 三行及寫入 baseline metadata。

## 契約 v2：工具 repo 契約③: must_fix 1 / optional 0
- [內容一致性] p3_sync: `_sync` 逐字本體範例的 `cd {{quote(justfile_directory())}} && just vendor_kit sync` 與 `build:` 本體行縮排（tab）渲染後消失，顯示成頂格，照抄不是合法 just；規格 §3.6 要求逐字（含 \t）

## 流程 v2：vendor_kit release: must_fix 4 / optional 2
- [內容一致性] v10r_2: Release 附件「vendor_kit-vN-local.tar.gz（local_bootstrap.sh、bootstrap.sh、…）」與名詞表 p15_tv6 仍列 local_bootstrap.sh；規格 §1.2 bootstrap.sh 列已定「離線包 = bootstrap.s
- [內容一致性] v10r_2、p15_tv6: Release 資產包含 local_bootstrap.sh，但 interface_spec §1.2 明定「無獨立 local_bootstrap.sh」，§4.8 也只定義 tar 與 .digest。
- [排版] v8: 同格包含兩平台 push-by-digest、建立 index、inspect 驗平台三個動作。
- [排版] v10: 同格同時 docker save、寫 .digest、組離線包及寫 SHA256SUMS。
  (opt) [可讀性] v8: 一格多件事：v8「push-by-digest 兩平台 → imagetools create 合成 index → inspect 斷言」、v11「打正式 tag vN、發布 Release」；v3／v4／v5 也各塞
  (opt) [內容一致性] p15_tv1: 同一句同時宣稱「同一次 buildx --platform linux/amd64,linux/arm64」及「兩個 runner 各自單平台 build」，兩種 release 策略互相矛盾；主流程採後者，名詞表應同步

## 流程 v2：離線包: must_fix 5 / optional 0
- [內容一致性] bO1: 整頁以 local_bootstrap.sh 為入口（泳道 hdr1、o1、o2、p16_tk1／p16_tv1、名詞表 p16_tv0），規格已定無獨立 local_bootstrap.sh、離線包就是 `bootstrap.sh --local <tar>`；與規格及 §7.4-16 驗收條不一
- [可讀性] o6: 一格三件事：「bootstrap.sh：git repo？just ≥ 1.33.0？→ docker load <tar>」（兩個判斷加一個動作）；o7「讀 <tar>.digest → index digest；docker image inspect → image ID」也是兩件事
- [排版] o6: 同格同時檢查 git、檢查 just 版本與 docker load。
- [排版] o7: 同格同時讀 .digest 與 inspect image ID。
- [排版] o10: 同格同時迭代工具、docker load、讀 digest、取得 image ID 及呼叫 add。

## 架構圖 v2: must_fix 2 / optional 4
- [排版] pull_dist: 線段標籤「工具 image 的 /dist 層 → .tmp.dist.<id>/」壓在 cli 模組標題文字上，且該線穿過「引擎容器」泳道標頭與 cli 模組框（線壓字、線穿無關方框）
- [排版] m_bl: 模組標題「baseline：baseline/<repo>/ + metadata」換行後第二行被最小單元方塊蓋住（文字裁切）；同樣情形見 m_lg（launcher-gen…第二行被「薄殼四檔」蓋住）與 m_mg（merge：逐檔合併 第二行被「狀態機」蓋住）
  (opt) [內容一致性] h_vk: 目錄樹註解「ci/check.sh # 進 git：CI 六步」，契約⑤、目錄樹頁、結束碼表都寫五步（⓪～⑤）
  (opt) [排版] p4H、h0～h4、h_vk、g1、g2: 架構圖混入使用者操作入口、載入關係、主機命令及完整檔案樹，不只是「模組 → 最小單元與模組間資料」。
  (opt) [排版] h4_u0_0～h4_u7_1: 列的是流程中的命令步驟，不是啟動器模組的最小責任單元；應移至流程／契約頁或改成抽象責任。
  (opt) [排版] p4P 全欄: 逐檔列出專案檔案並標寫入箭頭，已接近動詞副作用流程，而不是模組間資料架構。

## 契約 v2：CI 契約⑤ 與驗收矩陣: must_fix 1 / optional 1
- [排版] k3g_e: 「衝突」線的垂直段壓過旁邊「需改檔」（k3f_e）線上文字，線壓字
  (opt) [可讀性] c_a: vendor_kit 自身 CI 流程格「env-test」未在本頁名詞表定義

## 流程 v2：bootstrap.sh: must_fix 6 / optional 1
- [排版] ae10: 「拉」線（a6 → a7 引擎 image）與 a8 → a8i 的垂直線交叉
- [內容一致性] a6: 直接使用「內嵌引擎 ref」，缺少「已有 version.toml 時必須使用該行引擎、拉不到不得退回內嵌」分支。
- [排版] a6: 同格同時做 docker image inspect 與 docker pull。
- [排版] a8: 同格同時判別 --local 值與執行 docker load。
- [排版] a8i: 同格同時 inspect image ID 與讀 .digest。
- [排版] a10: 同格包含對每個工具迴圈、呼叫 add 及 resolve→docker→apply 三段。
  (opt) [可讀性] a6: 「docker image inspect 有 → 不 pull；無 → pull」把判斷和動作塞在一個步驟格（同型格：a8 判別＋docker load、a8i inspect＋讀 .digest；add（1）、upg

## 狀態機 v2：初始檔五態: must_fix 2 / optional 1
- [排版] se_end_m: 五條「狀態 → 終點」直線（se_end_d／m／c／a／u）直接穿過下方便條 up_d、up_m、up_c、up_a、pr_c 並壓在文字上
- [內容一致性] in_c: 把「add 時 append 既有檔被拒」轉成 declined，與 metadata schema 矛盾；declined 僅代表新增檔被拒、從未納管。
  (opt) [可讀性] se_c: 起點 → declined 的箭頭只標「拒絕」，其他箭頭都是「動詞：條件」格式；看不出是 add append 已存在拒絕還是 upgrade 新增檔拒絕

## 流程 v2：remove: must_fix 3 / optional 0
- [排版] me12y: 「是」標籤（m9q → m9m）壓在自己的線上；me13w（m9m → m9w 多處）沒有標籤且箭頭被 m9w 的 v2 綠標蓋住；me13z「0」標籤壓在轉折線上
- [排版] m6: 同格包含讀 metadata、產生五類刪除清單、產生詢問清單、輸出 stdout 與輸入指紋。
- [排版] m9m: 同格做尋找與計數；應將「找行」與「判斷命中數」拆開。

## 流程 v2：uninstall（2）寫入段: must_fix 1 / optional 0
- [排版] xe14y: x7 菱形出口「是」（xe14y）與「否」（xe14n）標籤都落在線上並與 x7n 的 v2 綠標重疊；x9 → x9y 的「是」（xe16q）壓在線與方塊上緣交界

## 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行: must_fix 1 / optional 0
- [排版] p2b_gn_r1c0_v2: v2 綠標（x=128，格寬 140）壓在「gen/<repo>.stamp」粗體文字的尾端

## 流程 v2：update: must_fix 3 / optional 0
- [顏色] u5g: 「GET /v2/<name>/tags/list」與 u6g「WWW-Authenticate 換 token」用紫色，本頁圖例紫 = image（引擎與工具），這兩格是 registry 查詢步驟不是 image
- [排版] u1: 同格同時描述 docker run、TOKEN 環境變數與 TOKEN_FILE 掛載。
- [排版] u8: 同格同時解析 SemVer、比較版本及建立輸出紀錄。

## 結束碼決策表 v2: must_fix 1 / optional 0
- [顏色] te_r5c3: update 列「任一目標查詢失敗（含無憑證 6-3）」放在紅色「1 失敗」欄，但 6-3 是印指令要人動作（設 token 或 upgrade <repo>@<tag>），依 v2.6-15 應為橙；update 流程頁同一情況畫成白格＋橙彙總，兩頁顏色語意不一致

## 流程 v2：upgrade ── E(c) upgrade vendor_kit: must_fix 1 / optional 0
- [內容一致性] b_c_flow: 規格 §1.2 upgrade (b)：`upgrade vendor_kit[@<tag>]` 先查 registry（@<tag>／frozen 不查）→ 有新版且薄殼相符才改第一行、無新版且薄殼相符 → 0 無變更、@<舊版> 無法無損讀 → 3 + 6-10；本頁主流程沒有「查 regist

## 流程 v2：undev vendor_kit: must_fix 2 / optional 1
- [內容一致性] undev_vk_flow: 規格 §1.2 undev、§3.1 兩段：undev（含 vendor_kit）建 `.tmp.undev.<id>.toml` 日誌後才撤覆寫行；本頁畫成單段 docker run → flock → 直接刪行，沒有建日誌／刪日誌，與 undev <repo> 頁及本頁便條「建日誌後才動」不一致
- [排版] w5b: 同格同時 inspect 與 pull。
  (opt) [內容一致性] w2、w2f: 寫「刪 vendor_kit 行（tag＋image ID 一起撤）」但沒有呈現「若這是最後一個覆寫，刪除整個 version.local.toml」分支。

## 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併: must_fix 0 / optional 1
  (opt) [可讀性] b14q1: 四個菱形（b14q1～b14q4）各自同時含「情況判斷」與「問句」，且各有三個出口（是／否／無標籤往下），四條「否」（be22x1～x4）共用同一條垂直線重疊到 b14n；第一次看的人分不清「否」與「往下」的差別

## 流程 v2：undev &lt;repo&gt;: must_fix 0 / optional 1
  (opt) [可讀性] diagram name v1p8c: 頁名在 XML 裡雙重跳脫（`&amp;lt;repo&amp;gt;`），draw.io 分頁標籤會顯示成「undev &lt;repo&gt;」字面，不是「undev <repo>」

## 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入: must_fix 0 / optional 1
  (opt) [可讀性] 刪進度日誌（最後一步）: 「刪進度日誌」步驟格直接分岔成「無衝突 → 0」「衝突 → 2」兩條線，沒有判斷菱形

## 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退: must_fix 0 / optional 1
  (opt) [內容一致性] c_r0c0: 逐檔判斷表缺 §4.3 的「D 缺（使用者刪了已納管檔）→ state=deleted、維持刪除」列（五態頁有，本表沒有）

## 契約 v2：不變量與角色: must_fix 1 / optional 0
- [排版] p1B_b1、p1B_b2、p1B_b3、p1B_b4、p1B_b5、p1B_b6: 每格同時包含規則、條件、動作、結束碼和訊息，違反「每格一件事」，且對非工程讀者資訊量過高。

## 契約 v2：動詞介面表: must_fix 1 / optional 0
- [排版] p1B_r2c2_0、p1B_r2c2_1、p1B_r3c2_4、p1B_r6c2_3: 單格包含多個順序動作，沒有做到一格一件事。

## 契約 v2：規則、選項表、不開的動詞: must_fix 1 / optional 0
- [內容一致性] p1C_opt_r7c4、p1c_tk3／p1c_tv3: 把 B1 的 --local 判別建議畫成已定規則；interface_spec §9.1 明確仍標示待定。

## 契約 v2：動詞 × 檔案矩陣: must_fix 1 / optional 0
- [內容一致性] p2c_mx_r12c5: 「結束碼 3 零寫入」後又寫「救援路徑例外」；規格明定回 3 一律零寫入，救援路徑也沒有寫入例外。

## 流程 v2：install（1）薄殼: must_fix 1 / optional 1
- [排版] i4: 「產薄殼四檔」把四個獨立檔案寫入放在同一動作格；應拆開或改成明確的單一批次模組呼叫。
  (opt) [內容一致性] i4c、i4cf: 只寫「version.toml 第一行」，未呈現 install 同時建立必要的 schema、written_by；若此格代表完整檔案寫入，內容不完整。

## 流程 v2：add（1）: must_fix 2 / optional 0
- [排版] c9a: 同格同時 inspect 與 pull。
- [排版] c2c: 同格同時輸出 image、metadata 資訊與輸入指紋；應拆成「產生計畫」及「產生指紋」。

## 流程 v2：add（2）: must_fix 1 / optional 0
- [排版] c21b: 同格同時寫來源、版本、完成標記、append 行、拒絕紀錄和 local image ID。

## 流程 v2：sync（1）啟動器快路徑: must_fix 1 / optional 0
- [排版] n1i: 同格同時 inspect、決定是否 pull、驗證 local image ID。

## 流程 v2：sync（1′）引擎 resolve: must_fix 1 / optional 0
- [排版] z0: 同格同時產生待辦清單、輸入指紋和 apply|yes/no。

## 流程 v2：sync（2）apply: must_fix 2 / optional 0
- [排版] m0a: 同格同時 inspect 與 pull。
- [排版] m3: 同格同時 materialize、暫存、原子替換。

## 流程 v2：upgrade B（1）: must_fix 2 / optional 0
- [排版] b7: 同格同時查最新版、處理明確 tag、比較是否降版與處理 frozen。
- [排版] b8a: 同格同時 inspect 與 pull。

## 流程 v2：upgrade B（2）: must_fix 2 / optional 0
- [內容一致性] b14r: 寫成「拒絕 → metadata 記 declined + declined_hash」，沒有區分已納管檔；已納管檔拒絕時 state 必須維持 managed，只能記 declined_hash。
- [排版] b14q1: 同一判斷格同時放文字檔與二進位檔兩種不同問句／處理規則。

## 流程 v2：upgrade B（2′）: must_fix 2 / optional 0
- [內容一致性] b15b: metadata 寫入仍只寫「declined」，未表達已納管檔拒絕應保留 state 並記 declined_hash。
- [排版] b15a: 同格包含推 baseline、判斷衝突、判斷解析失敗及記 conflicts。

## 流程 v2：upgrade 逐檔判斷、衝突重入、回退: must_fix 3 / optional 0
- [內容一致性] c_r1c2、c_r2c2、c_r5c2、c_r6c2: 既有 managed／appended／二進位檔拒絕均寫成「記 declined」；規格要求 state 不變、只記 declined_hash。
- [內容一致性] p7b_tv1: 名詞表也把所有拒絕概括成「metadata 記 declined」，延續同一錯誤。
- [排版] c_r2c1: 同格同時詢問、執行 merge-file 及指定暫存位置。

## 流程 v2：upgrade E(a)(b): must_fix 2 / optional 0
- [排版] s2ln: 同格同時 inspect 與 pull。
- [排版] s2h: 同格包含 grep、比較、驗計畫 engine 及接手判斷。

## 流程 v2：upgrade E(c): must_fix 1 / optional 1
- [排版] s11n: 同格同時 inspect 與 pull。
  (opt) [內容一致性] s12n: 「無新版且薄殼相符 → 0」只出現在便條，主流程沒有「是否有新版／只需重產」判斷，無法表達規格的三種結果（無新版且相符 0、只重產薄殼 1、有新版重產 1）。

## 流程 v2：dev: must_fix 2 / optional 0
- [排版] d1: 同格包含啟動引擎與建立 mount。
- [排版] v2b: 同格同時寫 tag 與 image ID；應表達成一次「寫完整 local engine override」或拆成兩欄位寫入。

## 流程 v2：undev <repo>: must_fix 2 / optional 0
- [排版] u5a: 同格同時 inspect 與 pull。
- [排版] u6e: 同格同時 materialize、使用暫存及替換 cache。

## 流程 v2：uninstall（1）: must_fix 1 / optional 0
- [排版] x2c: 同格同時輸出保護清單、刪除清單、三類詢問與指紋。

## 流程 v2：uninstall（2）: must_fix 1 / optional 1
- [排版] x9: 同一格同時做存在檢查、原文比對與詢問。
  (opt) [排版] x5z: 「刪進度日誌」後才判斷 .vendor_kit/ 是否空；建議把「完成交易」與「刪空目錄」明確分開，避免被理解為日誌刪除等於完整卸載。

## 狀態機 v2：交易與進度日誌: must_fix 2 / optional 0
- [排版] p12_lgx_entry: XML 中出現兩個相同 id（「跨頁入口」與「來自其他頁」）；draw.io 元件 id 必須唯一，否則後續編輯／引用可能指錯元件。
- [內容一致性] r3、p12_tv3: prune 的特殊行為只在便條，主判斷會落入「不可寫」分支並印 sync/update 的 6-33；規格要求 prune 只列出、不刪活躍日誌，需畫出 prune 特例分支。

TOTAL must_fix 78; by category {'內容一致性': 22, '排版': 52, '可讀性': 2, '顏色': 2}; rejected 18; pages with findings 43/40