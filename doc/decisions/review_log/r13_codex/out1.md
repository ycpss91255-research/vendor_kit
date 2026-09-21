Reading prompt from stdin...
OpenAI Codex v0.155.1
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 01a0bed6-14b3-7e52-8a48-85a274423d5d
--------
user
你是圖面審查員。vendor_kit：下游 repo 把 dist/ 打成純資料容器 image，下游專案用 bootstrap.sh + `just vendor_kit <動詞>` 取得工具、鎖版本、三方合併初始檔。附件 S 是規格正本（§0–§9，v3.5）；附件 R 是上一版（第十二版）codex 對本組頁的審查條目，請逐條核對是否已修。附件 P 是本組每一頁從 draw.io XML 抽出的文字（節點 [kind] id: 文字；邊 src --標籤--> dst；名詞表；跨頁引用），附上縮圖 PNG（頁 id 同名）。附件 L 是機械 lint 已抓到的條目（不必重複）。

注意：本版名詞已換新（下游開發者／下游使用者／VK／專案／下游 repo／版本鎖定行／基準版／進度檔／執行紀錄／CI 模式／介面版／檔案版）；執行紀錄事件改由圖例兩條約定表達（終點隱含 launcher_completed|failed、引擎格隱含 engine_started|completed），不再逐格畫——**不要**再要求逐格 engine_exit／launcher_exit。已接受、不要再質疑：add --local 只收 tar、升引擎由目標引擎改第一行、baseline/.gitkeep 保留、ie13 繞行。附件 R 每條請標「已修／未修／改壞」。

審查標準（使用者定）：1 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。2 顏色語意一致：藍＝引擎做、白＝啟動器做、綠＝0、橙＝需人處理、紅＝失敗、白虛線橢圓＝來自其他頁。3 字要少，一般人看得懂；專有名詞要在該頁名詞表。4 線段不穿無關方框、不交叉、不壓字、不懸空、不該折的不折。5 每個方塊只放一件事（一個動作／判斷／檔案）；一格兩件事就是問題。6 內容要跟規格一致；例子一律 `<repo>`。

逐頁找：(A) 與規格矛盾、缺分支、順序錯、誰做的（啟動器 vs 引擎）畫錯；(B) 頁間入口出口不對、懸空、缺線；(C) 一格多事；(D) 顏色不符語意；(E) 排版（看縮圖：線壓字、標籤位置歧義、線穿框）；(F) 一般人看不懂的句子或名詞表漏項。每條給：頁 id、元件 id（或引文）、類別、一句說明、必修／選修。若某頁沒有問題請明說。最後一句總評：本組頁面能否交給使用者看。繁體中文。


=== 附件 S：規格 §0–§9 ===
# vendor_kit 介面規格（interface reference）v3.5（2026-09-20；**v3.5 = codex 三審 00–02 頁（新發現 R1–R9）全部採納 + grilling「00–02 codex 三審新定案」，改動見 §10 #161–#168**；v3.4 = codex 二審 00–02 頁（未修 #31、#55、改壞 #52、新發現 N1–N16）全部採納，改動見 §10 #148–#160**；v3.3 = codex 審 00–02 頁 56 條全部採納 + 02 頁 6 點定案 + 兩條新規則 (a)(b) + 三條補列不變量 + 「專案」定名，改動見 §10 #131–#146**；v3.2 = 01 頁四點拍板（2026-09-20）+ 名詞定案（第 0 頁）落實，改動見 §10 #117–#130；v3 併入 proposal_v2 v2.10–v2.12、grilling「2026-09-20 第八～九輪審查後定案」、r9 規格層矛盾，改動見 §10 #58–#95；**v3.1 併入 v2.13（§9.1 P4–P13 結案）與 v2.14（第十輪後圖面落實與小定案），改動見 §10 #96–#116**）

用途：後續每張票唯一可引用的 input／output 定義；`/to-spec` 的原料。前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）、`interface_spec.v2.final.md`（v2 定稿 = v2.7 併入後、v3 併入前）、`interface_spec.v3.0.md`（v3 = v2.13／v2.14 併入前）、`interface_spec.v3.1.md`（v3.1 = 01 頁拍板與名詞定案落實前）、`interface_spec.pre_codex1.md`（v3.2 = codex 00–02 審查併入前）、`interface_spec.pre_r3.md`（v3.3 = codex 二審併入前）、`interface_spec.pre_r4.md`（v3.4 = codex 三審併入前）。

來源優先序（高 → 低）：
0000. v3.5 新併入：`decisions/review/codex_findings_00_02_r3.md`（R1–R9 全部採納）與 `grilling.md`「00–02 codex 三審新定案」（2026-09-20）：`<repo>` 名稱規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點）；工具版本鎖定行在 `[tools]` 表下、正規形在第 0 頁完整定義；`--local` 判別順序（`.tar` 結尾 → 檔案；否則含 `/` 且存在同名檔 → 6-37；否則 tag）；執行紀錄含每次 bootstrap.sh 執行；名詞「工具 recipe」。
000. v3.4 新併入：`decisions/review/codex_findings_00_02_r2.md`（#31、#52、#55 與 N1–N16 全部採納；需定義者由使用者定：N1 公開或私有自決、N2 可寫動詞 = 會建進度檔、N7／N10 prune 例外、N8 失敗策略依各動詞、N13 bootstrap.sh 結束碼原樣傳出、#31 版本鎖定行正規形、#52 `--dry-run` 只有需新版內容的動詞拉 image、#55 快路徑補 cache 存在、N15 resolve／apply 名詞）。
00. v3.3 新併入：`decisions/review/codex_findings_00_02.md`（56 條全部採納）；`grilling.md`「02 頁 6 點定案」「兩條新規則 (a)(b)」「補三條不變量」「專案定名」（2026-09-20）。
0. v3.1 新併入：`proposal_v2.md` **v2.14 → v2.13**（v2.13 = 主對話依既定原則對 §9.1 P4–P13 的取捨，使用者可否決；v2.14 = 第十輪後圖面落實與兩個小定案）。
0′. v3 併入：`grilling.md`「2026-09-20 第八～九輪審查後定案」；`proposal_v2.md` **v2.12 → v2.11 → v2.10**（v2.11-1 撤回 v2.10-4；衝突以最新為準）；`review_v2r9_findings.md` 中屬**規格層**的矛盾（選項表 `--local` 適用欄拆 bootstrap.sh／add、E(c) 指定 `@tag` 與 CI 模式是兩條分支、help 遇未完成交易印 6-33 仍 0、bootstrap 逐 `-t` 一個失敗即中止）；`decisions/log/agy_summary.md`、`agy_summary2.md`、`draft.md` 只作 §4.10 的設計依據，**只取 v2.12 已定案的部分**。
1. `grilling.md` 2026-09-19 條目（Q22 sync 快路徑、Q23 結束碼 3、Q24 vk-resolve 格式與實作層取捨、Q25 選項表、Q26 離線 `.digest`、Q27 多工具彙總、「規格審查 16 條必修」直接採納）。
2. `interface_spec_review.md`「最終建議」一～五節（16 條必修、22 個待定的建議值、vk-resolve/1 骨架、結束碼 3 邊界、F1 定案）與「規格與定案不符」清單——全部套用，除非與 grilling 相衝（grilling 勝）。
3. `proposal_v2.md`：v2.5 → v2.4 → v2.3 → v2.2 → v2.1 → 正文。
4. 其他 decisions／issue（#26、#27、#28、#29、base_pitfalls、compat、isolation、contract）。

每條規格後以 <sub>[來源]</sub> 標注；`[待定]` 集中於 §9；本次每處改動的依據列於 §10；矛盾處理於 §11。占位符（名詞一律照第 0 頁「00 名詞與縮寫」，`<sub>` 出處註記保留來源原文的舊詞）：`<repo>` 下游 repo 名（名稱規則見 §1.2 add：`[a-z0-9_][a-z0-9_-]*`）、`<ns>` just 命名空間、`<dir>` 目錄、`<tag>`、`<digest>`、`<ref>` = `<image>:<tag>@sha256:<digest>`、`vX`／`vY` 引擎版本、`P` 協定整數、`N` schema 整數、`<org>` GitHub 組織名、`<id>` 交易 id（= `<trace_id>`，32 hex）、`<id8>` = trace_id 前 8 碼、`<UTC-ts>` = `YYYYMMDDTHHMMSSZ`、`<verb>` 動詞名、`<專案根>` = 含 `.vendor_kit/` 的目錄。**專案** = 下游使用者的 git repo（或 monorepo 子專案），接入後含 `.vendor_kit/`；VK 的動詞都在專案裡跑（與提供工具的「下游 repo」區分；grilling 2026-09-20 定名）。

## 0. 共通前提（所有動詞）

| 項目 | 規格 |
|---|---|
| 專案根 | = 專案內含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；不是 git toplevel。第一次 `install` 時尚無 `.vendor_kit/`，候選專案根 = 呼叫目錄。<sub>[grilling Q20 定案（改）；review I-47]</sub> |
| 執行位置 | vendor_kit 動詞只准在專案根執行：recipe 檢查 `invocation_directory() == justfile_directory()`，否則 1 印 6-9。**所有動詞一體適用，`sync` 亦無例外**（原 F1「sync 豁免此檢查」撤回）；工具 recipe 自動觸發的 `_sync` 自己先 `cd` 到專案根再呼叫 `just vendor_kit sync`（§3.6），故不受影響。工具自己的 recipe 是否擋由工具決定。<sub>[grilling Q20 修正；01 頁拍板 2026-09-20 (2)]</sub> |
| git | 專案根須在某 git repo 內（主機側 `git rev-parse --is-inside-work-tree`）；引擎不讀 `.git`、不碰 index；不做 `git init`。禁止巢狀：install 時上層**或下層**已有 `.vendor_kit/` → 1 + 6-35（01 頁拍板確認）。worktree（`.git` 是檔）與 submodule 同樣適用（後者以 §7.4-20 實測為準）。<sub>[grilling Q20、19條-1、-10；review I-47]</sub> |
| 主機需求 | docker ≥ 19.03（或 Podman ≥ 4.9，見 §3.1）、just ≥ 1.33.0（GitHub release 下載版）、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA → issue v2。主機命令白名單見 §3.1。<sub>[grilling Q4、Q8、19條-2、-13；v2.4-10]</sub> |
| 不變量 | 對專案檔：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（= 不用工具版本取代客製內容；例外只有根 justfile 一行、根 `.dockerignore` 四行、已納管初始檔（含 `config.toml`）經同意的換版／三方合併）。執行紀錄（§4.10）與進度檔是 vendor_kit 自己的檔，不適用四原則。自動化（sync）只碰不進 git 的東西（cache/、gen/）。never fail silently（失敗印原因；需人處理另附可複製指令，§2「結束的兩種語意」）。另三條資料／原子性不變量（01 頁 I15–I17，grilling 2026-09-20 補列）：**I15** 每個 VK TOML 有檔案版、讀時忽略未知欄位寫時保留、跨版直接遷移（§4 通則、§8-7）；**I16** 多工具可寫動詞（不帶 repo 的 upgrade、uninstall）先對全部工具完整預檢、任一不過整體不動（§1.2）；**I17** `gen/tools.just` 最後寫且與 cache 同一 apply 內原子替換（§4.4、§8-9）；**I18** 版本鎖定行唯一正規形——引擎行在頂層 `vendor_kit = "<ref>"`、工具行在 `[tools]` 表下每工具一行 `<repo> = "<ref>"`（`<repo>` 照 §1.2 add 名稱規則，與頂層 `schema`／`written_by`／`vendor_kit` 不撞名），禁 BOM、重複鍵、TOML 表旁路，引擎讀到非正規形 → 1 列差異不動（§4.1）。I15 的「寫時保留未知欄位」只約束重寫仍存在的 TOML；uninstall／remove 合法刪掉整個檔或整個工具項目不在此限（codex r2 N9）。<sub>[grilling 隔離題、Q22 補、2026-09-20 補三條不變量；proposal §1；isolation 最終建議；codex 00–02 #19、#30、#32、#33；codex r2 #31、N9]</sub> |
| 詢問通則 | 需詢問但無 tty／EOF 且無 `-y` → 1 印 6-4；EOF／Ctrl-C = 中止整個 apply 回 1、不套用、**不記 declined**（declined 只記明確回答「否」）。明確回答「否」→ 不寫、metadata 依 §4.3 記錄。`-y` 只省略詢問，不授權覆蓋既有未納管檔、不硬加 append 行、**不解除 CI 模式**（`-y` 與 CI 模式為獨立開關，見下列 CI 模式）。<sub>[grilling 19條-6、Q13；v2.5-1、v2.5-4；review Claude 原文 12；01 頁拍板 2026-09-20 (3)]</sub> |
| CI 模式 | `CI` 真值規則：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；check.sh 自己 `export CI=1`。CI 模式 = 不寫任何 tracked 檔、不查最新版（**`update` 除外**：仍查 registry，它是唯讀動詞、查詢即其用途；02 頁 6 點定案 ①）；升為失敗的警告**明列**：薄殼不符、基準版落後、未完成接入、任何 local 覆寫、需改 tracked 檔（與 `-y` 無關）；Q15 的「沒納管／拒絕過」提醒**不**紅燈；仍拉鎖定版 image、仍寫 cache/、gen/。`update` 不受 CI 模式影響（唯讀、不寫檔）。**`-y` 與 CI 模式是兩個獨立開關**：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`；CI 模式下需改進 git 的檔一律 → 1 印清單，與 `-y` 無關。CI 模式由 `CI` 環境變數為真觸發（CI 平台自設或 check.sh 自設；本機手設 = 唯讀驗證，允許）。<sub>[v2.1 A；v2.2 A；v2.5-1；review 必修 4；review I-02、Claude 原文 25；01 頁拍板 2026-09-20 (3)]</sub> |
| 進度檔 | **所有可寫動詞第一個寫入前必建進度檔，不設例外**：add／`upgrade <repo>` 記 metadata `[progress]`；install（**第一次也建**，該日誌同時是「不留半成品」的清除清單，成功後刪；v2.13 P5）／remove／uninstall／undev／prune／**dev**（新規則 (b)：它寫本機覆寫、cache symlink、印記三處，同樣建 `.tmp.dev.<id>.toml`；撤回原「dev 不建」）／`upgrade vendor_kit`（含不帶 repo 時 E(a) 的自身那段）放 `.vendor_kit/.tmp.<verb>.<id>.toml`（§4.6；自身升級 = `.tmp.upgrade.<id>.toml`，在改 version.toml 第一行**之前**建，新引擎重產薄殼完成後由新引擎刪）。`<id>` = trace_id（§4.10）。可寫動詞開始前偵測到未完成交易 → 先恢復再繼續（`upgrade vendor_kit` 的恢復 = 重跑 `upgrade vendor_kit`），失敗明列 6-27；唯讀動詞只偵測、**不自動恢復**、除執行紀錄外不寫任何檔：**sync／update 印 6-33 結束 1，help 印 6-33 仍 0**。prune 特例：遇活躍（未恢復）日誌只列出並印 6-33、不刪、**不視為未完成交易**（不擋 prune、不恢復；差集與 `apply prune` 照做）。第一次 install 也建（v2.13 P5）；dev 也建（新規則 (b)）。<sub>[grilling 進度日誌條、Q24、2026-09-20 定案、新規則 (b)；v2.2 C；review 必修 9；v2.7-7；v2.9-6、-8；v2.10-6；v2.11-1；v2.12 L5]</sub> |
| 執行紀錄 | 每個動詞每次執行（含 help、update、sync 快路徑、prune、`--dry-run`）及每次 `bootstrap.sh` 執行（自身那段在 `log/bootstrap/`）除印 tty 外必寫一檔 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）：**順序（新規則 (a)）**：不寫檔、不拉 image、不起容器的前置檢查（git repo？just 版本？）可在建紀錄之前；任何寫入／pull／起引擎之前必已有紀錄（非 git 目錄無處可寫）。啟動器 mkdir + 建檔 + 寫 `launcher_start`，失敗 → 1 + 6-38、零寫入；引擎啟動時 append `engine_start`，失敗 → 1 + 6-38、不進 resolve；無 `--no-log`。它是 vendor_kit 自己的檔（不進 git、不進 build context、不適用專案檔四原則），與進度檔分工：進度檔管交易恢復（成功即刪），執行紀錄管事後追溯（保留規則 §4.10）。`trace_id` 同時是進度檔交易 id。凡印到 tty 的訊息一律同句進 `body`。bootstrap.sh 就是第一次接入的啟動器：驗 git repo／just（唯讀）→ `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`，之後才 pull／install（§1.2 bootstrap.sh）。<sub>[v2.11-3；v2.12 L1–L5；v2.13 P4；grilling 新規則 (a)；codex 00–02 #8、#26、#37]</sub> |
| config.toml | `.vendor_kit/config.toml`（§4.9）：進 git；install 建（含註解與預設值）；缺檔或缺鍵 = 預設；`schema = 1`、`[log] keep = 50`、`days = 30`；非正整數 → 預設 + 警告；對 `upgrade vendor_kit` 是三方合併初始檔（要改先問）；啟動器只 grep 正規行、引擎用 TOML parser。<sub>[v2.12 L3′]</sub> |
| 事件註冊表 | `log-events.txt`：`event_name` 的有限集合（§4.10 事件表；L6 集合**待 codex 審**），啟動器與引擎寫 log 前以 `grep -Fxq` 對表，未註冊 → FATAL（實作錯誤，不是下游使用者錯誤）；CI 靜態擋原始碼中未註冊的事件名。落點：真本 `log-events.txt` 在引擎 image；啟動器端薄殼 `log.sh` 內嵌一份啟動器事件白名單（`case`），release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（§4.10）。<sub>[v2.12 L5、L6；agy_summary2「事件名註冊表前例」；v2.13 P9]</sub> |
| 引擎環境 | 容器內 `LC_ALL=C.UTF-8`、`TZ=UTC`，時間戳 UTC ISO 8601；HOME 指容器內暫存（實作細節）。使用者身分見 §3.1 `-u` 規則。<sub>[grilling 19條-3、-4]</sub> |
| 路徑 | 啟動器一律引號（含空白、`$`、非 ASCII）；vk-resolve 內自由文字以八進位跳脫（§3.3）；執行紀錄內 argv 與路徑逐項 JSON 跳脫（§4.10）。<sub>[grilling 19條-8、Q24；v2.12 L5]</sub> |
| 多工具彙總 | 不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）；預檢後的失敗策略**依各動詞**：`upgrade` 逐工具做得完的做完；`uninstall` apply 期間任一工具失敗 → 中止並列出已完成／未處理（§1.2 uninstall）；`update` 逐工具查完；最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；`update` 同時遇 1 與 2 → 1；訊息全列。<sub>[grilling Q27；codex r2 N8]</sub> |
| 結束碼 3 | 介面版／檔案版不合，須先升級或退回才能繼續；回 3 時**零寫入**（「零寫入」= 不寫任何專案檔，執行紀錄例外：`launcher_start`／`engine_start` 已寫屬預期，§4.10；v2.13 P12 已定）；新舊以介面版／檔案版比較，不用版本字串；最低介面版檢查先於任何上網。細節 §2。<sub>[grilling Q23]</sub> |
| 結束的兩種語意 | 非 0 的結束分兩類，訊息與圖色都要分得出來：**需人處理** = 動詞停下並印出下一步指令的結束——結束碼 1 或 3 且附可直接複製的指令，合併衝突 2 亦同；圖上**橙**。**失敗**（error）= 無法繼續的結束——拉不到、寫不進、驗證不過；結束碼 1；圖上**紅**。§6 每則訊息標類別。<sub>[grilling 2026-09-20（v2.10-1）；01 頁拍板 2026-09-20 (4)]</sub> |

## 1. 下游使用者動詞

語法：`just vendor_kit <verb> [args]`；所有動詞 recipe 一律 `verb *args` 一行轉發（`set positional-arguments` 只在 vendor.just），各動詞 `--help` 由引擎印。分組 `[group('常用')]`：add、upgrade、dev；`[group('進階')]`：其餘。<sub>[proposal §2]</sub> 不開：init、ensure、diff、accept、rollback、`--repair`（併進 install 冪等修復）、`--purge`（明確不提供，永不刪專案檔；開 issue 供後續討論）、`--porcelain`、`--tag`、`--digest`（`add --local` 只收 tar，index digest 一律來自 `.digest` 旁檔；tag 形只有 bootstrap.sh 有既有 version.toml／內嵌引擎 ref 可當來源；使用者：想不到用途）、`--no-log`（執行紀錄不可關閉；寫不進 → 1 + 6-38）。<sub>[proposal §2；v2.1 E；grilling Q25、2026-09-20；v2.10-3；v2.11-2；v2.12 L4]</sub>

### 1.1 選項總表（Q25）

| 選項 | 短形 | 型別 | 適用 | 說明 |
|---|---|---|---|---|
| `--tool <repo>[@<tag>]` | `-t` | string，可重複 | bootstrap.sh | 接入的工具與版本；`@<tag>` 省略 = 最新正式版 |
| `--yes` | `-y` | bool | bootstrap.sh、install、uninstall、add、remove、upgrade、prune | 免詢問（不解除 CI 模式） |
| `--path <dir>` | `-p` | string | dev `<repo>` | 本機工具目錄 |
| `--image <tag>` | `-i` | string | dev `vendor_kit` | 本機引擎 image tag（只能 tag） |
| `--help` | `-h` | bool | 全部 | 由引擎印；bootstrap.sh 自印 |
| `--dry-run` | — | bool | uninstall、add、remove、upgrade、prune | 唯讀預覽、不建進度檔；需要新版內容的動詞（add、upgrade）仍拉 image 展開，uninstall、remove、prune 不拉（它們不需展開 image；§3.1 兩段編排）<sub>[codex r2 #52]</sub> |
| `--source <image>` | — | string | add | image 路徑不符 `<org>/<repo>-dist` 慣例時 |
| `--local <image tag 或 tar>` | — | string | bootstrap.sh | 離線。值的判別（B1，**依序、互斥**）：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 + 6-37 消歧；否則 → image tag（含 `/` 但無同名檔的完整 ref 也是 tag 形）。**tar 形**：`docker load` 後由同名 `.digest` 旁檔取 index digest（§4.8）。**tag 形**：不讀 `.digest`、只 `docker image inspect` 本機 image ID（記 version.local.toml）；version.toml 正式 ref@digest 來源 = 專案已有 version.toml → 該行；第一次接入 → bootstrap.sh 內嵌引擎 ref。不論哪形，前置檢查（git repo、just ≥ 1.33.0）一律先做 <sub>[grilling 2026-09-19 末條；v2.7-2；v2.9-1；v2.10-2；r9]</sub> |
| `--local <tar>` | — | string | add | 離線。**只收存在的 `.tar` 檔**（新工具沒有既有 digest 可當 tag 形來源）：值不是存在的 `.tar` → 1 + 6-24（add `--local` 分句）；`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml、metadata 記 `local_image_id`；不收 image tag 形 <sub>[v2.10-3；v2.11-2；grilling 2026-09-20；r9]</sub> |
| `--verify` | — | bool | sync | 每檔 sha256 全驗（F5 已定；CI 為真時等同、不必加）<sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |
| `--exit-code` | — | bool | update | 有新版回 2 |
| `--timeout <秒>` | — | 正整數 | bootstrap.sh、add、upgrade、sync、undev | = `VENDOR_KIT_PULL_TIMEOUT`，由啟動器攔截、不轉發引擎；優先於環境變數 |
| `--no-justfile` | — | bool | install | 跳過根 justfile 步驟只印指示 |
| `--protocol P` | — | 整數 | 內部 | 薄殼→引擎全域旗標，不列 help |

版本一律寫在位置參數：`<repo>@<tag>`、`vendor_kit@<tag>`；`@<tag>` 比現版舊 → warn 仍執行。短選項只有 `-t`、`-y`、`-p`、`-i`、`-h`。<sub>[grilling Q25、19條-7]</sub>

### 1.2 動詞表

通則（每個動詞，含 help 與 bootstrap.sh —— 它就是第一次接入的啟動器，v2.13 P4）：啟動器在任何寫入／pull／起引擎之前建執行紀錄並寫 `launcher_start`（失敗 → 1 + 6-38、零寫入）；不寫、不拉、不起容器的前置檢查（git repo、just 版本、專案根位置）可在建紀錄之前，其餘前置檢查（需 docker 或引擎者）在建紀錄之後（新規則 (a)）；**每個**引擎子命令（resolve 容器、apply 容器、單段各一）啟動時先 append `engine_start`（失敗 → 1 + 6-38、不做任何動作）、結束寫 `engine_exit`；啟動器結束前 `log_prune`、`launcher_exit` 記結束碼與耗時（§4.10）。下表不逐格重複；圖面表現法：每頁 resolve 段與 apply 段各一格 `engine_start`、頁尾一格 `launcher_exit`／`log_prune`。<sub>[v2.12 L4；v2.14-2]</sub>

| 動詞 | 語法 | 位置參數 | 前置檢查 | 副作用（寫哪些檔，見 §4） | 詢問點（`-y`／無 tty） | 結束碼 | stdout／stderr 概要 |
|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag 或 tar>] [--timeout <秒>] [-h]` | 無 | **順序**：驗 git repo／just（下列）→ `mkdir -p .vendor_kit/log/bootstrap/`（含目錄內 `.gitignore`）→ 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install（v2.13 P4）。在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref；最低介面版檢查（§2）；`--local` 不論 tar 或 tag 形，以上前置檢查一律先做 <sub>[grilling Q8、Q18；v2.4-5；v2.9-1]</sub> | `docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref（拉不到 → 1 + 6-24／逾時 6-31，**失敗出口**、不退回內嵌；tag 形 `--local` 的 `docker image inspect` 本機無此 image 亦為失敗出口；v2.14-5）→ 引擎 `install`（失敗 → 1：依 `.tmp.install.<id>.toml` 清半成品，**`.vendor_kit/log/` 保留**，訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」；v2.13 P4、P5）→ 逐 `-t` **依序**呼叫 `add <repo>[@<tag>]`，**任一 add 回非 0 → 立即中止**、不處理後續 `-t`、列出已完成／未處理的工具（已完成的 add 保留；「不留半成品」只對第一次 install 成立）；**結束碼 = 失敗那一步的碼原樣傳出**：install 或 add 回 3 → 3、回 2 → 2、其餘非 0 → 1（codex r2 N13）；`--local` 時 version.toml 仍寫正式 ref@digest：tar 形由同名 `.digest` 旁檔取得 index digest（§4.8），tag 形**不讀 `.digest`**、只 `docker image inspect` 本機 image ID，正式 ref 來源 = 專案已有 version.toml → 該行、第一次接入 → bootstrap.sh 內嵌引擎 ref；version.local.toml 寫 `vendor_kit = "<tag>"` + `vendor_kit_image_id`，在 install 成功後才寫、失敗清除；不自刪。離線契約入口 = `bootstrap.sh --local <tar>`（值判別見 §1.1 B1）；離線包內另含 `local_bootstrap.sh` **便利包裝**（偵測 daemon 架構 `docker version --format '{{.Server.Arch}}'`、挑該平台 tar、`exec ./bootstrap.sh --local <tar> "$@"`），不是契約入口、不另定介面 <sub>[proposal §2；#27；grilling Q26；v2.5-8；review 必修 15；v2.7-1；v2.9-1；v2.10-2；r9]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 | 0；1 失敗不留半成品（只對第一次 install 成立）；任一 `-t` 的 add 失敗 → 中止；非 0 一律原樣傳出該步的碼（3 → 3、2 → 2、其餘 → 1）；3 見 §2 <sub>[proposal §2；v2.2 C；r9；codex r2 N13]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" -w /repo <引擎 ref> --protocol P install` <sub>[#27；review B7]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 + 6-17 <sub>[codex_verbs]</sub> | 在 git repo 內（否 → 1 + 6-16）；上層與下層皆無 `.vendor_kit/`（否 → 1 + 6-35）；不被 gen/.stamp 比對擋；第一次／修復判定用薄殼自描述首行（§4.5）：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 + 6-28 列差異不動 <sub>[proposal §2；grilling Q20、Q17；v2.5-8]</sub> | 建 `.vendor_kit/`：version.toml（含 schema、written_by）、**config.toml**（§4.9，含註解與預設值；修復型缺則建、存在不動）、entry.just、vendor.just、.gitignore（含 `log/`）、ci/check.sh、baseline/（空、不建 metadata）、gen/.stamp；**log/**（含目錄內 `.gitignore`）由**啟動器**在寫 `launcher_start` 前建（第一次接入 = bootstrap.sh 建 `log/bootstrap/`；§4.10、v2.13 P4），引擎不建；根 justfile 無 → 建（§4.5 兩段式內容：import 一行 + `default:`／`\t@just --list` 兩行）；有 → 問後加一行；已含那行 → 不再加；根 `.dockerignore`：無 → 建（四行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；有 → 問後 append（同 §4.3 append 規則；插入的行記於 `baseline/.vendor_kit.toml`，見 §4.3 註）；再跑 = 用引擎重寫薄殼（hash 相符才重寫）；**第一次與修復型都**在第一個寫入前建 `.tmp.install.<id>.toml`（統一規則、無例外；第一次時它同時是「不留半成品」的清除清單，失敗依它移除已寫的檔、`log/` 保留，成功後刪；§4.6、v2.13 P5）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1；v2.9-8；v2.12 L1、L3′；v2.13 P4、P5]</sub> | 根 justfile 已存在 → 6-20「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示；`.dockerignore` 已存在 → 6-34 <sub>[proposal §2；isolation A1(4)；grilling Q22 補]</sub> | 0／1／3 | 印建立或修改了什麼（含加進根 justfile 的那一行、加進 .dockerignore 的四行） |
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分（該工具鎖定行不動，見 remove；已完成的工具已整個移除）<sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7；grilling 12 個疑慮取捨]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；**config.toml** 比照初始檔保護模式：hash == `baseline/vendor_kit/config.toml` 副本 → 刪，被下游使用者改過 → 留下並列出（永不刪下游使用者改過的檔）；**`log/` 一律保留**（uninstall 自己也在寫）、不 rmdir `log/`，`.vendor_kit/` 因此保留（只剩 `log/`），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪；進度檔 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12；v2.13 P6；v2.14-6]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的四行同 append 規則問後只刪原文相同的；append 行問後**逐行**比對、只刪仍與紀錄原文相同的行，缺失／被改的行跳過並 warn（不是全有／全無）<sub>[proposal §2、§5；grilling Q22 補；v2.9-5]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點：它是 `[tools]` 下未加引號的 TOML 鍵，句點會被讀成 dotted key；OCI repo 名本就小寫）、不得為 `vendor_kit`（保留）；頂層 `schema`／`written_by`／`vendor_kit` 與 `[tools]` 下的工具鍵不同層、不撞名 | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；`--local <v>`：`<v>` 必須是存在的 `.tar` 檔（不收 image tag 形），否則 1 + 6-24（add `--local` 分句）；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`（只收 tar）：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26；v2.10-3]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [--dry-run]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；兩段（resolve→apply、重驗指紋）但不經 docker create/cp <sub>[proposal §2；v2.3 §5；review Claude 原文 3]</sub> | 刪 cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行，**最後才刪 version.toml 該行**（與 add／upgrade 一致：回 1 時該行不動；失敗留下的狀態 = 工具仍鎖定、cache 可能部分缺，進度檔保留、下次可寫動詞先恢復）；初始檔永不刪，印清單；進度檔 `.tmp.remove.<id>.toml` <sub>[proposal §2；v2.1 E；grilling 進度日誌、12 個疑慮取捨]</sub> | append 過的行 → 6-21 問後只刪原文相同的（CRLF/LF 等價）<sub>[proposal §5；grilling Q13]</sub> | 0／1／3 | 初始檔清單 |
| `update [<repo>]` | `update [<repo>] [--exit-code]` | `<repo>` 可省 = 全部含 vendor_kit | 只查 registry（`tags/list` 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 CI 模式影響；單段、不經 docker create/cp；無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；不可同時宣稱「已是最新」；偵測到未完成交易 → 印 6-33 結束 1（不恢復）<sub>[proposal §2；grilling Q11、Q27；#28；v2.10-6]</sub> | 無 | 只寫執行紀錄（§1.2 通則） | 0 已列出；1 查詢失敗（任一工具 1 → 整體 1，即使另有新版）；`--exit-code` 有新版 → 2；3 <sub>[proposal §2；v2.1 E；grilling Q27]</sub> | 末行固定 6-15 <sub>[proposal §2]</sub> |
| `upgrade [<repo>[@<tag>]]` | `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 可省 = 全部含 vendor_kit 自身；`vendor_kit[@<tag>]` 為特殊值；`@<tag>` 限單一 repo | 順序：(0) metadata `conflicts` 非空且檔案仍含 `<<<<<<< vendor_kit:baseline` → 2 停（檔案失蹤不算已解）；(1) 有待合併（version.toml 已 B、基準版仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 `@<tag>`；CI 模式不查）；無基準版 → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新版新增 `<ns>`／dest 的全域撞名）再動任何東西；不帶 repo 且引擎有新版 → **本次只改第一行、工具不升** <sub>[v2.2 D；v2.1 B；v2.2 B；v2.5-6、-7；proposal §2；review I-20]</sub> | resolve → docker → apply：cache/、gen/<repo>.stamp、初始檔逐檔（§4.3 狀態機，N 讀自 `/dist/<repo>`）、基準版推到新版（有衝突仍推；解析失敗不推）+ metadata、gen/tools.just；version.toml 最後寫。自身：(a) 不帶 repo 遇引擎新版 → 舊引擎 apply（拿鎖、重驗、建 `.tmp.upgrade.<id>.toml`：記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending）只改第一行 → 啟動器比對第一行前後（§3.4）→ 用新引擎跑 `upgrade vendor_kit`；(b) `upgrade vendor_kit[@<tag>]`（單段救援路徑）主流程：前置 —— 薄殼被改（hash 不符自描述首行）→ 1 + 6-28 不動；有未完成的 `.tmp.upgrade.<id>.toml` → 本次即恢復（依日誌的目標 ref 續跑）；(1) 目標判定，**三條分支分開**：**指定 `@<tag>`** → 不查 registry，目標 = 指定 tag（≠ 現 ref 仍走「有新版」分支；降版以其 image LABEL 的介面版／檔案版判）；**CI 模式且未指定** → 不查、目標 = 現 ref；**其餘** → 查 registry 取最新正式版；(2) 目標 ≠ 現 ref？**是** → 先建 `.tmp.upgrade.<id>.toml` → 改第一行 → 啟動器再以新 ref 跑一次（§3.4）→ 新引擎重產薄殼五檔（含 log.sh）+ gen/.stamp → **config.toml 缺則建／有則三方合併（6-22 問；B = `baseline/vendor_kit/config.toml`；§4.9）** → 新引擎刪日誌 → **1 + 6-2**（E(c)(2) 圖須有此格與檔案框；v2.14-7）；**否** → 薄殼與現引擎相符？是 → **0 無變更**；否 → 建 `.tmp.upgrade.<id>.toml` → 用現引擎重產薄殼 → 刪日誌 → **1 + 6-2**，重產失敗（第一行未變）→ 1 + 印原因（**不是** 6-2b）；`@<舊版>` 降版：目標引擎（以其 image LABEL 的介面版／檔案版判）能無損讀現有檔才做（同介面版／檔案版 → 依上列 0／1），否則改檔前拒絕 **3 + 6-10** <sub>[v2.3 §2；v2.5-7；grilling Q19、Q23；review 必修 6、「自身升級第二次」一致；v2.7-5；v2.10-5；v2.11-1；v2.12 L3′；r9 E(c)]</sub> | 逐檔 6-22：「X 換成新版？」／「你和新版都改了 X，要三方合併嗎？」／新增檔「要建 X 嗎」（拒絕 → state=declined + declined_hash）／二進位／symlink 未改 → 問後換、改過保留 + warn／append 行找到 → 問後替換、找不到 → 不動印新內容；`-y` 全免問；CI 且需改 tracked 檔 → 1 印清單（與 `-y` 無關）<sub>[proposal §5；grilling Q14、Q6；v2.5-1；review 必修 10]</sub> | 0；1 工具層不動 version.toml（自身升級已改第一行後回 1 是明列例外）；2 有衝突（留標記、印檔名、基準版仍推到新版、解完重跑直到乾淨；`git merge-file` 衝突數映射為 2，其 I/O／執行錯誤 → 1）；3 <sub>[proposal §2；v2.3 §2；v2.2 D；grilling Q19、Q23；review I-25]</sub> | `--dry-run`：印會問哪些檔、6-6～6-8、metadata 遷移明列；dest 在 CI 路徑時 6-29 <sub>[grilling Q14、Q15]</sub> |
| `dev <repo>` | `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | `<repo>` 必填 | `-p`（工具必填）／`-i`（僅 `vendor_kit`，只能 tag 不能 digest）互斥；工具必須已在 version.toml（否 → 1）；`<dir>/dist/init.toml` 存在（缺 → 1）；CI 拒絕；單段、不經 docker create/cp；`-i` 的 image 以 LABEL 介面版／檔案版判定為「舊」時允許但禁止重產 tracked 薄殼（§2 (d)）<sub>[proposal §2；v2.2 B；v2.3 §5；grilling Q19；review Claude 原文 35]</sub> | 工具：version.local.toml `[tools].<repo> = "path:<dir>"`，cache/<repo>/ 改 symlink → `<dir>/dist`（唯讀性只在容器 mount 上成立），gen/<repo>.stamp 第一行 `path:<dir>`。自身：version.local.toml `vendor_kit = "<tag>"` + `vendor_kit_image_id`；之後啟動器用 `docker image inspect` 驗 ID、不 pull。**進度檔** `.tmp.dev.<id>.toml`（新規則 (b)：記要寫的覆寫行、symlink 目標、印記；第一個寫入前建、成功後刪）<sub>[proposal §2；v2.2 B；review 必修 3、I-42；grilling 新規則 (b)]</sub> | 無 | 0／1／3 | — |
| `undev <repo>` | `undev <repo> [--timeout <秒>]`／`undev vendor_kit [--timeout <秒>]` | `<repo>` 必填 | 未啟用 = 0 + 提示 | 兩段（`undev <repo>` 與 `undev vendor_kit` 皆走 resolve→apply）：apply 先建日誌 `.tmp.undev.<id>.toml`（記要撤的行，含 image ID）**才**撤 version.local.toml 該行（`undev vendor_kit` 把 `vendor_kit = "<tag>"` 與 `vendor_kit_image_id` 一起撤）；撤掉的是最後一個覆寫 → 刪除整個 version.local.toml；→ 重新 fetch 鎖定版（經 docker create/cp；`undev vendor_kit` 無 fetch）→ 最後刪日誌；失敗 → 1 保留可恢復狀態。`undev vendor_kit`：下次 just 用 version.toml 引擎，gen/.stamp（`<tag>`）≠ ref → 只提示 6-1、不重寫 <sub>[proposal §2；v2.2 B；v2.3 §5；v2.5-10；review F2、I-31]</sub> | 無 | 0／1／3 | — |
| `sync [<repo>]` | `sync [<repo>] [--verify] [--timeout <秒>]` | `<repo>` 可省 = 全部 | 每次工具 recipe 自動前置（§3.6）；快路徑（§3.6）；`--verify` 或 CI 為真 → 每檔 sha256 全驗（F5 已定）；引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；`resolve sync` 一開始偵測未完成交易 → 印 6-33 結束 1、不恢復（與 update 同一菱形；快路徑只把「無 `.tmp.*`」當起引擎條件）；下游 image `docker pull` 失敗 → 1 + 6-24／6-31 失敗出口 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9；v2.10-6；v2.14-4、-5]</sub> | 只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp。每工具順序：覆寫 path → 跳過 fetch/verify（仍查完成標記、基準版落後）；cache 缺或印記第一行 ≠ 鎖定 digest → fetch；否則 verify sha256 → 失敗 → 重裝 + warn；tools.just 缺或需重生 → 重生。無待辦 → resolve 回 `apply\|no` 快路徑 0（不起第二個容器）<sub>[v2.3 §4；v2.2 E；v2.5-9]</sub> | 無 | 0；1：薄殼不符、metadata 無完成標記（6-13）、CI 下基準版落後（6-5）、CI 下任何 local 覆寫；3 <sub>[proposal §2；v2.1 A]</sub> | 本機基準版落後 → warn 提示 upgrade |
| `prune` | `prune [-y] [--dry-run]` | 無 | 兩段：`resolve prune` 輸出 `keep` 清單（version.toml 引用的全部 image + version.local.toml **實際引用的 image**：只有引擎的 tag／image ID 覆寫有 image；工具的 `path:<dir>` 覆寫沒有 image、不列；02 頁 6 點定案 ④）；啟動器 `docker {container,image,network,volume} ls --filter label=io.github.<org>.vendor_kit=1` 列出候選、扣掉 keep；image 只刪「帶 label 且本專案未引用」者（共享 daemon 上其他專案的引用不可知 → 文件明寫、`--dry-run` 先看）；活躍（未恢復）的 `.tmp.<verb>.<id>.toml` 不刪、只列出提示 6-33、不視為未完成交易（不擋 prune、不恢復）<sub>[grilling 9 修正、9 補充、Q24；review A1、I-33、I-34；v2.7-7]</sub> | 啟動器執行 docker rm／image rm／network rm／volume rm（不掛 docker socket）；`apply prune` 先建 `.tmp.prune.<id>.toml` → 刪失效的 `.vendor_kit/.tmp.dist.*/` 與已完成交易殘留的 `.tmp.*` → 刪日誌；執行紀錄的保留清理**不屬** `prune` 動詞（由啟動器每次呼叫 best-effort 做，§4.10）；磁碟滿連 prune 也被 6-38 擋（訊息附清空間提示）<sub>[v2.9-6；v2.12 L3、L4]</sub> | 列出候選後 6-32「要刪除以上 vendor_kit 資源嗎？」（`-y` 免問） | 0／1／3 | 列出刪了什麼、保留什麼（含原因） |
| `help`／`h` | `help` | 無 | 不觸網、不安裝、不偵測交易以外的任何狀態；偵測到未完成交易 → 印 6-33 **仍 0** <sub>[v2.10-6]</sub> | 只寫執行紀錄（§1.2 通則） | 無 | 0（6-33 不影響）；1 只在 6-38 | 命名空間層說明；help 明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」<sub>[codex_verbs]</sub> |

## 2. 結束碼總表

| 碼 | 定義 | 動詞例外／特例 |
|---|---|---|
| 0 | 成功（含 warn）；`add` 已接入完成、`remove` 未接、`undev` 未啟用、`upgrade vendor_kit` 無新版且薄殼相符皆 0 + 提示；`help` 偵測到未完成交易印 6-33 仍 0 <sub>[proposal §2；review 一致；v2.10-6]</sub> | — |
| 1 | 一般失敗、需人處理／重跑；「工具層動詞回 1 時 version.toml 不動」適用 add／`upgrade <repo>`／remove／uninstall（寫入前檢查；鎖定行最後才寫／最後才刪）；remove／uninstall 回 1 時其餘檔（cache/、baseline/、gen/）可能已部分刪除（工具仍鎖定），進度檔保留、下次可寫動詞先恢復 <sub>[proposal §2；compat 條 4；codex 00–02 #20；grilling 12 個疑慮取捨]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3；所有動詞（含 help／prune）執行紀錄建檔或 `launcher_start`／`engine_start` 寫入失敗 → 1 + 6-38（零寫入）；bootstrap.sh 任一步非 0 → 中止並原樣傳出該步的碼（install／add 回 1 → 1；回 3 → 3；回 2 → 2）；引擎讀到非正規形的版本鎖定行（§4.1）→ 1 列差異不動 <sub>[v2.3 §2；grilling Q23；v2.12 L4；r9；codex r2 #31、N13]</sub> |
| 2 | 合併衝突（留 `<<<<<<< vendor_kit:baseline` 標記、印檔名、基準版仍推到新版）<sub>[proposal §2；v2.2 D]</sub> | `update --exit-code` 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔基準版不推、記入 `conflicts` <sub>[v2.1 E；review Claude 原文 29]</sub> |
| 3 | 現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且**零寫入（無任何例外；救援路徑亦同；執行紀錄不算寫入，§4.10）**：(a) 薄殼 P < 引擎 floor_P → 6-18；(b) 引擎讀到 schema > 支援上限 → 6-19；(c) `upgrade vendor_kit@<舊版>` 目標引擎介面版／檔案版低於現有檔 → 6-10；(d) `dev vendor_kit -i` 的引擎介面版／檔案版低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 提示先 `upgrade vendor_kit`。「舊」一律以介面版／檔案版比，不以 SemVer。網路／認證／不存在 → 1，不得偽裝成 3；最低介面版檢查在任何上網之前（啟動器可先 `docker image inspect` 引擎 LABEL 判最低介面版）<sub>[grilling Q19、Q23；review 最終建議四；contract 3]</sub> | — |

多工具彙總見 §0；舊薄殼對未知碼原樣傳出、不吞。<sub>[grilling Q27；compat codex 原文]</sub>

**結束的兩種語意**（§0）：碼 1 分兩類——**需人處理**（印出下一步指令：6-1、6-2、6-4、6-5、6-9、6-13、6-28、6-33、6-35 等；圖上橙）與**失敗**（拉不到、寫不進、驗證不過：6-24、6-30、6-31、6-38 等；圖上紅）；碼 3 一律需人處理（6-10、6-18、6-19、6-36；橙）；碼 2 需人處理（橙）；碼 0 綠。每則 6-xx 的類別見 §6「類別」欄。<sub>[grilling 2026-09-20；01 頁拍板 2026-09-20 (4)]</sub>

### 2c. 動詞×檔案矩陣

每格：建／改／刪／讀／—（不碰）。檔案定義見 §4；專案檔規則見 §0 不變量；`log/` 欄 = 執行紀錄 `log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）。<sub>[由 §1.2、§4 推導；v2.9-6、-8；v2.11-1；v2.12 L1、L3′；本次新增]</sub>

| 動詞 | version.toml | config.toml | 薄殼五檔 + gen/.stamp | baseline/（含 metadata） | version.local.toml | cache/、gen/<repo>.stamp、gen/tools.just | 專案檔（根 justfile 行、根 .dockerignore 行、初始檔） | 進度檔 | log/ |
|---|---|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | 經 install／add | 經 install | 經 install | 經 add | `--local`（tar 或 tag 形）：install 成功後寫 `vendor_kit` + `vendor_kit_image_id`、失敗清除 | 經 add | 經 install／add | 經 install／add（`.tmp.install.<id>.toml`；失敗依它清半成品） | 寫 `log/bootstrap/`（自己建目錄、寫 `launcher_start`；失敗仍保留） |
| `install`（第一次） | 建 | 建 | 建 | 建 baseline/（空）；根 .dockerignore 的 append 記於 baseline/.vendor_kit.toml | — | — | 根 justfile 建或問後加一行；根 .dockerignore 建或問後 append 四行 | `.tmp.install.<id>.toml`（兼不留半成品的清除清單） | 寫（目錄由啟動器建） |
| `install`（修復型） | 讀 | 缺則建、存在不動 | hash 相符才重寫 | — | — | — | 已含那行 → 不再加 | `.tmp.install.<id>.toml` | 寫 |
| `uninstall` | 各工具行最後才刪；整檔刪（hash 相符） | hash == 基準版副本 → 刪；被改 → 留並列出 | 刪（hash 相符） | 刪自產 | 刪 | 刪自產 | 問後逐行刪原文相同行；初始檔保留 | `.tmp.uninstall.<id>.toml` | 寫；一律保留（不 rmdir） |
| `add` | 最後寫該行 | — | — | 建 baseline/<repo>/ + metadata（`[progress]` → `complete`） | 讀 | 建 cache/<repo>/、gen/<repo>.stamp；重生 tools.just | 初始檔：無 → 建；append 問後加；已存在 → 不納管 | metadata `[progress]` | 寫 |
| `remove` | 最後才刪該行 | — | — | 刪 baseline/<repo>/ | 讀（dev 中 → 1） | 刪 cache/<repo>/、gen/<repo>.stamp；重生 tools.just | append 行問後逐行刪 | `.tmp.remove.<id>.toml` | 寫 |
| `update` | 讀 | — | — | 讀 | 讀 | — | — | 只偵測（6-33 → 1） | 寫 |
| `upgrade <repo>` | 最後寫該行 | — | — | 推到新版 + metadata | 讀 | 同 add | 逐檔狀態機（換版／三方合併／append 替換／新增檔） | metadata `[progress]` | 寫 |
| `upgrade`（不帶 repo，遇引擎新版） | 只改第一行 | — | 接手後同 `upgrade vendor_kit` | — | 讀 | — | — | `.tmp.upgrade.<id>.toml`（舊引擎建、新引擎刪） | 寫（接手後同一檔） |
| `upgrade vendor_kit[@<tag>]` | 目標 ≠ 現 ref 時改第一行 | 缺則建（問）／有則三方合併（問） | 新引擎重產 | — | 讀 | — | — | `.tmp.upgrade.<id>.toml` | 寫 |
| `dev <repo>` | 讀 | — | — | — | 寫 `[tools].<repo>` | cache/<repo>/ → symlink；gen/<repo>.stamp 第一行 | — | `.tmp.dev.<id>.toml` | 寫 |
| `dev vendor_kit` | 讀 | — | — | — | 寫 `vendor_kit` + `vendor_kit_image_id` | — | — | `.tmp.dev.<id>.toml` | 寫 |
| `undev` | 讀 | — | — | — | 撤行；最後一個 → 刪檔 | 重新 fetch（`undev vendor_kit` 無） | — | `.tmp.undev.<id>.toml` | 寫 |
| `sync` | 讀 | — | 讀（比對 gen/.stamp） | 讀 | 讀 | fetch／verify／重生 tools.just | — | 只偵測（6-33 → 1） | 寫（快路徑亦寫） |
| `prune` | 讀（keep） | — | — | — | 讀（keep） | — | — | `.tmp.prune.<id>.toml`；刪已完成交易殘留 `.tmp.*`、`.tmp.dist.*`；活躍者不刪 | 寫 |
| `help` | — | — | — | — | — | — | — | 只偵測（6-33 仍 0） | 寫 |
| 啟動器（每次呼叫，任何動詞） | grep 版本鎖定行 | grep `keep`／`days` 正規行 | 讀 vendor.just 自身 | — | grep 版本鎖定行 | grep stamp 第一行（sync 快路徑） | — | 偵測 `.tmp.<verb>.*` 存在（快路徑條件） | 建檔、寫啟動器事件、prune 舊檔（best-effort） |


## 3. 薄殼 ↔ 引擎介面

### 3.1 啟動器（POSIX sh；本體為 vendor.just 內的 recipe 殼；不解析 TOML、不 eval）<sub>[proposal §6；v2.2 C]</sub>

| 項目 | 規格 |
|---|---|
| 主機命令白名單 | `sh`（含內建 `printf`、`read`、`trap`、`kill`、`cd`）、`grep`、`sed`、`id`、`mktemp`、`mkdir`、`date`、`rm`、`sleep`、`od`、`tr`（`mkdir`／`date`／`od`／`tr` 只用於執行紀錄：建 `log/<verb>/`、時間戳、trace_id，§4.10）、`git rev-parse`、`docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}`；check.sh 另可用 `git ls-files`。lint 擋清單外的命令。啟動器 timestamp：試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級（`.000000Z` 補零）；引擎一律微秒 <sub>[review 必修 12；grilling Q24；v2.12 L5；v2.13 P7]</sub> |
| 引擎 ref 取得 | 以 §4.1 版本鎖定行 regex 於 version.local.toml（覆寫優先）→ version.toml 取 `vendor_kit`；命中數 ≠ 1（0 或重複）→ 1 明確訊息 <sub>[base_pitfalls 1-11；v2.1 B；review 必修 11]</sub> |
| 引擎 image 取得 | 一律先 `docker image inspect <ref>`：本機有 → 不 pull（離線可用）；無 → `docker pull <ref>`（逾時 §5）。local 覆寫時：`docker image inspect <tag>` 的 `.Id` 必須 == version.local.toml `vendor_kit_image_id`，否則 1；**不 pull**（不用 `--pull never`，docker 19.03 無此旗標）<sub>[review 必修 3；grilling Q26]</sub> |
| docker run 參數 | `docker run --rm [<使用者旗標>] -v "<專案根>:/repo" -w /repo [-v "<專案根>/.vendor_kit/.tmp.dist.<id>:/dist:ro"] [-v "<dir>/dist:/dist/<repo>:ro"]… [-v "<TOKEN_FILE>:/run/vk-token:ro" -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] [-e CI] [-e VENDOR_KIT_NO_LOCK] -e TRACEPARENT=<…> -e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔> [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.<org>.vendor_kit=1 --label io.github.<org>.vendor_kit.project=<專案根絕對路徑> <引擎 ref> --protocol P <子命令> [args]`。`--protocol P` 為全域旗標，一律在子命令之前；`-w /repo` 必給（不依賴 image 的 WORKDIR）；`-it` 只在 apply 且互動（有 tty、無 `-y`、非 CI 模式），**resolve 永不 `-t`**；啟動器 `trap … EXIT INT TERM` 清容器與 `.tmp.dist.<id>/` <sub>[proposal §6；v2.2 B、C；#27；grilling Q16、19條-5、9 補充、Q24；review 必修 6、B5、B7]</sub> |
| 使用者旗標 | 偵測：`docker info --format '{{.SecurityOptions}}'` 含 `name=rootless` → rootless，不加 `-u`；`docker --version` 含 `podman` → 加 `--userns=keep-id`、不加 `-u`；其餘（rootful docker）加 `-u "$(id -u):$(id -g)"` <sub>[review 必修 6（rootless）、Claude 原文 14；grilling 12 修正]</sub> |
| `-e` 白名單 | 轉發：`CI`（照原值）、`VENDOR_KIT_NO_LOCK`、`TRACEPARENT` 與 `VENDOR_KIT_LOG_FILE`（每次呼叫，啟動器自產、必傳；容器內路徑 `/repo/.vendor_kit/log/<verb>/<檔>`，§4.10、§5；v2.13 P8）；`VENDOR_KIT_REGISTRY_TOKEN`／`_USER` 只在 update／upgrade 的 resolve 階段；`VENDOR_KIT_REGISTRY_TOKEN_FILE` 改為 `-v <主機檔>:/run/vk-token:ro` 並傳容器內路徑（同階段）。啟動器自讀不轉發：`VENDOR_KIT_PULL_TIMEOUT`。其餘一律不轉發（`HTTP_PROXY` 等 → v2）<sub>[#28；grilling 19條-2；review 必修 5、B2]</sub> |
| 下游 image 展開 | 每工具先 `docker image inspect <ref>` 有則略過 pull → `docker create --label io.github.<org>.vendor_kit=1 --label …project=<專案根> <ref> /x` → `docker cp c:/dist/. "<專案根>/.vendor_kit/.tmp.dist.<id>/<repo>/"` → `docker rm`；不帶 `--platform`（daemon 挑原生）；不執行下游 image <sub>[proposal §6；v2.1 C；#26；grilling Q24、Q26]</sub> |
| 暫存目錄 | 專案內 `.vendor_kit/.tmp.dist.<id>/`（`mktemp -d "<專案根>/.vendor_kit/.tmp.dist.XXXXXX"`；同檔案系統、remote docker context 亦可掛）；trap 刪；自有 .gitignore 擋 <sub>[grilling Q24；review B6]</sub> |
| 兩段編排 | 兩個獨立屬性：**需展開 image**（docker create/cp）= add／upgrade／sync／undev；**兩段**（`resolve <verb>` → 主機 docker → `apply <verb>`，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；**單段** = install／`upgrade vendor_kit`／update／dev／help。`--dry-run` = `apply --dry-run`（需展開 image 的動詞 add／upgrade 也要先拉 image 展開；uninstall／remove／prune 本來就不展開、`--dry-run` 亦不拉）<sub>[v2.3 §5；v2.2 C；v2.5-10；review 必修 7、Claude 原文 3；codex r2 #52]</sub> |
| 鎖 | 鎖在引擎 resolve 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗，印 6-26）；`VENDOR_KIT_NO_LOCK=1` 跳過；啟動器不鎖 <sub>[proposal §6；v2.1 C；base_pitfalls 3-8]</sub> |
| 執行紀錄 | 每次呼叫在任何寫入／pull／docker run 之前（新規則 (a)：不寫、不拉、不起容器的前置檢查——git repo、just 版本——可在建紀錄之前；引擎 ref 取得、最低介面版檢查仍在建紀錄之後）：讀 config.toml（grep 正規行，§4.9）→ 產 trace_id → `mkdir -p .vendor_kit/log/<verb>/`（第一次建 `log/` 時一起建目錄內 `.gitignore`）→ 建 `<UTC-ts>-<id8>.jsonl` 並寫 `launcher_start`（完整原始 argv）；任一步失敗 → 1 + 6-38、零寫入。之後每個 docker pull／extract／engine spawn／sync 快路徑各記一筆；結束時（trap 內）依 config 保留規則 prune 舊檔（best-effort：失敗只 warn、不改結束碼）→ 最後一筆 `launcher_exit`（exit_code、duration_ms、reason）。值一律經 §4.10 跳脫；不 eval、不用 echo <sub>[v2.12 L3、L4、L5、L6]</sub> |
| 自身升級編排 | §3.4 |
| pull 失敗 | 印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列為「主機錯誤」）+ 僅在 add／bootstrap 提示 6-24 的「離線可用 `--local`」（upgrade 不支援離線，不提示）；本機已有 image 時不 pull <sub>[base_pitfalls 2-9；review I-37、I-38]</sub> |
| 逾時 | `VENDOR_KIT_PULL_TIMEOUT`／`--timeout`：單次 pull 總經過時間，預設 300 秒，只收正整數（0 或非數字 → 1）；POSIX 實作 = 背景 pull + 每秒輪詢 + `kill`；逾時 → 1 + 6-31 指出 ref <sub>[grilling 19條-14、Q24；review B3]</sub> |

### 3.2 引擎子命令與 argv

| 子命令 | argv | 說明 |
|---|---|---|
| `install`、`update`、`dev`、`help`、`upgrade vendor_kit[@<tag>]` | `--protocol P <verb> [verb args]` | 單段對外動詞，argv 與 §1 相同（`*args` 原樣轉發）<sub>[proposal §6；grilling Q16]</sub> |
| `resolve <verb>` | `--protocol P resolve <verb> [verb args]` | verb ∈ add／remove／upgrade／sync／undev／uninstall／prune。只讀：讀 version.toml／local、查 registry（CI 模式不查）、算執行計畫（要拉哪些 image@digest、mount、指紋、apply 與否），stdout 回啟動器（§3.3）；不詢問、不寫任何檔、無 TTY <sub>[v2.1 C；v2.2 C；review 三]</sub> |
| `apply <verb> [--dry-run]` | `--protocol P apply <verb> [--dry-run] [verb args]` | 讀 `/dist/vk-resolve`（啟動器把 resolve 原始 stdout 存成 `.tmp.dist.<id>/vk-resolve` 一起掛入）→ 拿 flock → 重算指紋與計畫中的 `fingerprint` 比對（不同 → 1 + 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 需改 tracked → 1）→ 建進度檔 → 寫入 → 最後刪日誌；不重新選最新版 <sub>[v2.3 §6；v2.2 C；v2.5-3；review 三]</sub> |
| 內部（不對外） | `fetch`、`verify`、`merge` | 不列入契約；`fetch` 原名 `materialize`，改名對齊第 0 頁模組名「取件 `fetch`」（02 頁 6 點定案 ⑤）<sub>[proposal §6；grilling 2026-09-20]</sub> |

**每個**子命令（resolve 容器、apply 容器、單段各自）啟動時先 append `engine_start`（記收到的 argv、component=engine）到啟動器建的同一執行紀錄，失敗 → 1 + 6-38、不做任何動作（含 resolve）；結束前 append `engine_exit`（exit_code、message_id、duration_ms、summary）。引擎以 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` 定位該檔（與 `TRACEPARENT` 並用；§3.1、§5）。<sub>[v2.12 L4、L5、L6；v2.13 P8；v2.14-2]</sub>

`--protocol P`：單一整數，與 release 版號分開，從第一版就有（P=1）；引擎接受 `[floor_P, current_P]` 並以呼叫方的 P 輸出行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1。<sub>[grilling Q16；compat codex 2]</sub>

### 3.3 `vk-resolve/1` stdout 格式

**呼叫**：`docker run --rm [<使用者旗標>] -v "<專案根>:/repo" -w /repo [-e …] <引擎> --protocol P resolve <verb> [args]`，永不 `-t`。resolve 結束碼非 0 → 啟動器不讀 stdout，原碼傳出（1／2／3）。啟動器把 stdout **整份**存到 `.tmp.dist.<id>/vk-resolve`，先驗文法再動任何 docker；之後整份原樣掛進 apply（`/dist/vk-resolve`）供重驗指紋。<sub>[grilling Q24；review 三]</sub>

**文法**（P=1）：
```
vk-resolve/<P>            ← 第一行；P = 呼叫方 --protocol 的值（不是引擎的 current_P）
<kind>|<f1>[|<f2>…]       ← 每行一筆；欄位以單一 `|` 分隔；UTF-8；LF 結尾；無空行、無註解；禁 CR／NUL／BOM
end|<N>                   ← 最後一行，之後立即 EOF；N = 記錄行數（不含首行與 end 行）
```

欄位類別：
- **安全字串**（`<kind>`、`<name>`、`<repo>`、`yes|no`、整數）：`[A-Za-z0-9_.-]+`（`<repo>` 另受 §1.2 add 名稱規則 `[a-z0-9_][a-z0-9_-]*` 限制，是其子集）。
- **ref**：`[A-Za-z0-9_.:/@-]+`，引擎以 image-reference parser 驗證後才輸出。
- **自由文字**（`<dir>` 等路徑；任何 byte）：以 POSIX `printf '%b'` 可解碼的八進位跳脫編碼——凡不在 `[A-Za-z0-9_./:@+=,-]` 的 byte 一律寫成 `\0ooo`（反斜線、`0`、三位八進位；例：空白 `\0040`、`|` `\0174`、`\` `\0134`、非 ASCII 逐 byte）。啟動器一行解碼：`dir=$(printf '%b' "$f2")`，結果只當單一引號 argv 使用、不 eval、不 source。編碼結果不含空白與 `|`，故 `IFS='|' read -r kind f1 f2 f3` 可直接切欄。<sub>[grilling Q24]</sub>

| kind | 欄位 | 筆數 | 啟動器動作 |
|---|---|---|---|
| `pull` | `<name>\|<ref>` | 0..n | `docker image inspect` 有則略，否則 `docker pull <ref>`（逾時／失敗 → 6-24／6-31）。name = `vendor_kit` 或 `<repo>` |
| `extract` | `<repo>\|<ref>` | 0..n | 同 pull 後 `docker create … <ref> /x` → `docker cp c:/dist/. ".tmp.dist.<id>/<repo>/"` → `docker rm`；apply 見 `/dist/<repo>/`。同一 repo 不得同時有 extract 與 mount |
| `mount` | `<repo>\|<dir 八進位跳脫>` | 0..n | dev 覆寫：解碼後驗 `<dir>/dist/init.toml` 存在（缺 → 1）→ `-v "<dir>/dist:/dist/<repo>:ro"` |
| `engine` | `<ref>` | 0..1 | 只在 `upgrade`（不帶 repo）：apply 會把第一行改成此 ref。啟動器先 pull（或 local 覆寫時 inspect 驗 ID）；apply 後依 §3.4 接手。有 engine 時本次不得夾帶工具寫入 |
| `fingerprint` | `<sha256 hex64>` | 恰 1 | 不解析，隨檔交給 apply。算法見下 |
| `apply` | `yes` \| `no` | 恰 1 | `no` → 啟動器驗完文法後直接 exit 0（sync 快路徑，不起第二個容器）；`no` 時不得有 pull／extract／mount／engine 記錄。`yes` → docker 階段後跑 `apply <verb> [--dry-run] [args]` |
| `keep` | `<name>\|<ref>` | 0..n | 只在 `prune`：本專案引用、不可刪的 image（含 local 覆寫的 `<tag>`）。prune 的 `apply` 只處理 `.tmp.*` |
| `end` | `<N>` | 恰 1 | 必為最後一行 |

**啟動器驗證**：首行 ≠ `vk-resolve/<P>`、缺 `end`、N 不符、`end` 後仍有資料、未知 kind、欄位數不對、`fingerprint`／`apply` 不是恰一筆、`no` 卻附動作記錄、安全字串含非法字元 → 1 + 6-30，不得繼續；引擎宣稱的 P 真不支援 → 3。<sub>[review 三、codex C-1]</sub>

**指紋算法**：sha256（hex64）。引擎對下列輸入依路徑 byte 順序排序，串接 `<path>\0<kind>\0<sha256(content) 或 ->\n` 再 sha256：version.toml、version.local.toml（缺記 `-`）、每個 `baseline/*/.vendor_kit.toml`、metadata 中 state=managed／appended 的每個 dest（區分檔案／symlink／缺）、gen/.stamp 第一行、每個 gen/<repo>.stamp 第一行、`.tmp.*` 日誌清單、鎖定 digest、本機引擎 image ID（local 覆寫時）、本次 verb 正規化 argv（含 `--dry-run`／`-y`／CI 模式）。**不含**新版新增檔（resolve 時 N 未展開；apply 對新檔只建不存在者，已存在 → 不納管 6-11）。apply 拿鎖後重算，不同 → 1 + 6-12；詢問後、替換前對目標檔再查一次前像（flock 擋不住編輯器）。<sub>[review 三、I-12、I-13]</sub>

**範例 1：`upgrade`（不帶 repo）遇引擎新版**（只改第一行、工具不升）
```
vk-resolve/1
pull|vendor_kit|ghcr.io/<org>/vendor_kit:v1.3.0@sha256:aaaa…
engine|ghcr.io/<org>/vendor_kit:v1.3.0@sha256:aaaa…
fingerprint|9f2c…e1
apply|yes
end|4
```
**範例 2：`sync`，一個 cache 過期、一個 dev 工具（路徑含空白）**
```
vk-resolve/1
extract|<repo>|ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:bbbb…
mount|robot_tools|/home/me/robot\0040tools
fingerprint|1c0e…77
apply|yes
end|4
```
**範例 3：`sync` 無待辦（快路徑）**
```
vk-resolve/1
fingerprint|1c0e…77
apply|no
end|2
```
**範例 4：`prune`**
```
vk-resolve/1
keep|vendor_kit|ghcr.io/<org>/vendor_kit:v1.2.0@sha256:…
keep|<repo>|ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:…
fingerprint|77ab…03
apply|yes
end|4
```

**stderr**：診斷（warn、錯誤、問句以外的人看訊息）一律 stderr；apply 的 stdout 不作為協定通道（互動時 TTY 會合流）。**對舊 P**：不得輸出呼叫方不認識的 kind／欄位、不得要求其未提供的 mount／環境變數（缺少時明確拒絕）。<sub>[v2.2 C；compat 條 4；compat codex 2；review 一致]</sub>

### 3.4 自身升級的接手（啟動器）

「引擎已變」**不從 stdout 讀**：啟動器在 apply 前後各 grep 一次 version.toml 的 `vendor_kit` 版本鎖定行。apply 結束後 ref 變了（且 == 計畫的 `engine`）→ 以新 ref（local 覆寫有 `vendor_kit=` 則用該 image、驗 ID）跑 `docker run … <新 ref> --protocol P upgrade vendor_kit`（同一 `TRACEPARENT`、append 同一執行紀錄），其結束碼原樣傳出（預期 1 + 6-2）；新引擎重產薄殼完成後刪舊引擎建的 `.tmp.upgrade.<id>.toml`；第二次第一行又變 → 1 + 6-2b，不再重跑。第一行已改但新引擎拉取／ID 不符／重產失敗 → 1 + 6-2b，日誌保留（下次任何可寫動詞先恢復 = 重跑 `upgrade vendor_kit`；sync／update 印 6-33 結束 1；help 印 6-33 仍 0）。**6-2b 只適用「第一行已改（或第二次又變）」**；第一行未變的重產失敗 → 1 + 印原因。直接執行 `upgrade vendor_kit[@<tag>]`（E(c)）的目標判定**三條分支分開**（§1.2 upgrade (b)）：指定 `@<tag>` → 不查 registry 但目標 = 指定 tag，≠ 現 ref 仍改第一行並由啟動器接手；CI 模式且未指定 → 不查、目標 = 現 ref；其餘 → 查 registry——「指定 `@<tag>`」不得與「CI 模式」合成同一個「不查 = 無新版、第一行未變」分支。local 覆寫（`bootstrap.sh --local` tag 形、`dev vendor_kit -i`）下 version.toml 正式 ref@digest 的來源：專案已有 version.toml → 該行；第一次接入 → bootstrap.sh 內嵌引擎 ref；tag 形不讀 `.digest`（§1.1、§4.8）。<sub>[grilling Q24；review 必修 6；codex D1；v2.9-1；v2.10-2、-5；v2.11-1；r9 E(c)]</sub>

### 3.5 救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/，永久保證）

清單：`install`、`upgrade vendor_kit[@<tag>]`、`sync` 的「薄殼不符 → 1 + 6-1」判定、`help`。任何 ≥ 最低介面版的薄殼可經此路徑叫任何引擎重產薄殼；反向（新薄殼叫舊引擎降版）亦然，受 §2 (c)(d) 限制。<sub>[grilling Q16；compat codex 3]</sub>

### 3.6 sync 自動前置（F1 定案）與快路徑（Q22）

| 項目 | 規格 |
|---|---|
| gen/tools.just | 每個 `<ns>.just` 一行 `mod? <ns> '../cache/<repo>/just/<ns>.just'`（`mod?`：cache 缺檔時其他 recipe 與修復入口仍可跑）；零 set 零 recipe <sub>[review 必修 2；grilling 16 條]</sub> |
| 工具模組內 `_sync` | 每個 `dist/just/<ns>.just` 必含私有 recipe，本體逐字：<br>`[private]`<br>`_sync:`<br>`\tcd {{quote(justfile_directory())}} && just vendor_kit sync`<br>（`justfile_directory()` 在模組內 = 根 justfile 所在目錄 = 專案根；用 `quote()` 不直接插字串）。因為先 `cd` 再呼叫，被呼叫的 `sync` 其 `invocation_directory()` 已是專案根，**不需要也不再有**執行位置檢查的豁免（§0 執行位置）<sub>[grilling 16 條、F1；review 五；01 頁拍板 2026-09-20 (2)]</sub> |
| 公開 recipe | 工具每個公開 recipe 相依 `_sync`（`build: _sync`）；例外集合：無（工具內全部公開 recipe）。vendor_kit 自身動詞（vendor.just 內全部）**不**自動前置 |
| `--dist` lint | `check.sh --dist` 以 `just --dump --dump-format json` 解析每個 `<ns>.just`：`_sync` 存在、私有、本體逐字相符；每個公開 recipe 的 dependencies 含 `_sync`；違反 → 失敗 <sub>[review F1、F4]</sub> |
| 限制（契約明寫） | just 在執行任何 recipe 前已載入所有模組：同一次 just 呼叫內不會看到 sync 重建後的新 recipe（Q9 契約）；cache 缺檔時 `mod?` 讓 `just vendor_kit sync` 仍可進入；1.33.0 fixture 通過才算結案（§7.4-25）<sub>[grilling Q9；review 五]</sub> |
| 快路徑 | `sync`（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml `vendor_kit` ref；version.toml `[tools]` 每個 `<repo>` 的 ref 之 digest == gen/<repo>.stamp 第一行（或 local 覆寫的 `path:<dir>`）；每個工具的 `cache/<repo>/` 存在（目錄或 symlink；印記在而 cache 被刪 → 不走快路徑，由引擎 fetch；codex r2 #55）；gen/tools.just 存在；無 `.tmp.<verb>.*.toml`；非 CI 模式。全相符 → 寫完執行紀錄後不起容器、0（仍寫執行紀錄：`launcher_start`／`sync_fast_path`／`launcher_exit`，§4.10）；任一不符或 CI 模式 → 起引擎 `resolve sync`。每檔 sha256 verify 只在：CI（CI 模式）、快路徑有差那次（版本變動）、以及 `sync --verify`（長形；F5 已定）做；`sync`（無參數，含工具 `_sync` 自動呼叫）一律快路徑 <sub>[grilling Q22、2026-09-19 末條；v2.7-2]</sub> |
| 快路徑前提 | `.vendor_kit/.gitignore` 明列 `cache/`、`gen/`、`version.local.toml`、`.tmp.*`、`log/`；install 把 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/` 加進根 `.dockerignore`（無則建；有則問後 append、`-y` 免問）；工具契約：build 以專案根當 context 時不得再排除 `.vendor_kit/` 以外的方式繞過 <sub>[grilling Q22、Q22 補]</sub> |

## 4. 檔案格式（檔案版）

通則：每個 vendor_kit 寫的 TOML 有 `schema = N`（integer）+ `written_by = "<vX>"`（string，純資訊，不作讀取門檻）；讀取門檻只看 `schema`；同檔案版只加不改；**讀時忽略未知欄位、寫時保留**（不能保留則拒絕寫）；只拒絕型別錯、重複宣告 → 1；檔案版高於本引擎支援 → 3 + 6-19 零寫入；讀任一舊檔案版 → 直接寫當前檔案版（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。第一版 `schema = 1`。<sub>[grilling 相容性其餘採納、16 條 written_by；review 必修 8、C1；base_pitfalls 1-11]</sub>

### 4.0 目錄樹（`<專案根>`）

```
<專案根>/
├── justfile                        專案檔；install 加一行 import '.vendor_kit/entry.just'（§4.5）
├── .dockerignore                   專案檔；install append 四行（§4.5）
├── <初始檔…>                       工具範本建立的專案檔（copy／append；§4.3、§4.7）
└── .vendor_kit/
    ├── version.toml                進 git；§4.1（install／add／upgrade／remove 寫）
    ├── config.toml                 進 git；§4.9（install 建；upgrade vendor_kit 三方合併）
    ├── entry.just                  進 git；薄殼（§4.5）
    ├── vendor.just                 進 git；薄殼 + 啟動器本體（§4.5）
    ├── log.sh                      進 git；薄殼第五檔：啟動器 log 函式（§4.5、§4.10；v2.13 P9）
    ├── .gitignore                  進 git；薄殼：cache/ gen/ version.local.toml .tmp.* log/（§4.5）
    ├── ci/check.sh                 進 git；薄殼（§7.1）
    ├── baseline/
    │   ├── .vendor_kit.toml        進 git；根 .dockerignore append 記錄 + config.toml 的 metadata（§4.3 註、§4.9）
    │   ├── vendor_kit/config.toml  進 git；config.toml 的基準版副本（§4.9；v2.13 P10）
    │   └── <repo>/                 進 git；基準版副本 + .vendor_kit.toml metadata（§4.3）
    ├── version.local.toml          不進 git；§4.2（dev／undev／bootstrap --local）
    ├── cache/<repo>/               不進 git；§4.4（fetch；dev 時 symlink）
    ├── gen/                        不進 git；.stamp、<repo>.stamp、tools.just（§4.4）
    ├── log/                        不進 git；執行紀錄（§4.10）；目錄與其 .gitignore（* / !.gitignore）由啟動器建；uninstall 保留
    │   └── <verb>/<UTC-ts>-<id8>.jsonl   一次執行一檔；所有動詞寫（bootstrap.sh 那段在 bootstrap/）
    ├── .tmp.<verb>.<id>.toml       不進 git；進度檔（§4.6）：install（第一次也建，v2.13 P5）／remove／uninstall／undev／prune／dev（新規則 (b)）／upgrade(自身)
    └── .tmp.dist.<id>/             不進 git；啟動器暫存（§4.6）
```
<sub>[§4 各節彙整；v2.9-8；v2.10-8；v2.11-1；v2.12 L1、L3′；v2.13 P5、P9、P10；本次新增]</sub>

### 4.1 `.vendor_kit/version.toml`

| 項目 | 規格 |
|---|---|
| 進 git | 是；唯一來源。寫入者：install／add／upgrade／remove（apply 最後寫）；下游使用者、Renovate 可手改；sync 只讀。<sub>[proposal §3]</sub> |
| 版本鎖定行契約 | **每一行唯一正規形**（本節為正本；00 頁「版本鎖定行」與 01 頁 I18 引用本節）：引擎行在頂層 `vendor_kit = "<ref>"`、`[tools]` 表下每工具一行 `<repo> = "<ref>"`（`<ref>` = `<image>:<tag>@sha256:<digest>`；`<repo>` 為未加引號的 TOML 鍵，須符合 §1.2 add 的 `[a-z0-9_][a-z0-9_-]*`，故不含句點、不會成 dotted key；頂層 `schema`／`written_by`／`vendor_kit` 與工具鍵不同層、不撞名，保留名只有 `vendor_kit`）——行首無空白、鍵後一個空白、`=`、一個空白、雙引號基本字串、無尾端註解、LF 結尾；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：引擎行 `^vendor_kit[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$`、工具行 `^<repo>[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$`（POSIX BRE，不用 `\s`）；每個鍵命中數必須恰為 1（`grep -c`），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 `[tools]` 之前。禁止：BOM、重複鍵、`[vendor_kit]`／`[tools.<repo>]` 表旁路等 regex 讀不到／讀錯的等價寫法；**引擎讀到非正規形 → 1 列出差異（哪一行、期望的形）、不動任何檔**。<sub>[grilling 相容性其餘採納、16 條；review 必修 11；codex r2 #31]</sub> |
| 公開格式 | 工具可讀它寫來源紀錄。<sub>[grilling deploy 定案]</sub> |

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 是 | 引擎 ref `ghcr.io/<org>/vendor_kit:vN@sha256:<digest>`（多架構 index digest）<sub>[proposal §3；#26]</sub> |
| `schema` | integer | 是 | 啟動器不讀、只引擎讀 <sub>[compat codex 5]</sub> |
| `written_by` | string | 是 | 寫入引擎版本，純資訊 <sub>[review C1]</sub> |
| `[tools].<repo>` | string | 每工具 | `<repo>` 照 §1.2 add 名稱規則（小寫、不含句點）；`ghcr.io/<org>/<repo>-dist:<tag>@sha256:<digest>`（index digest；`add --local` 亦寫正式 index digest，來自 `.digest` 旁檔）<sub>[proposal §3；grilling Q26]</sub> |

```toml
vendor_kit = "ghcr.io/<org>/vendor_kit:v1.0.0@sha256:<digest>"
schema = 1
written_by = "v1.0.0"

[tools]
<repo> = "ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:<digest>"
```

### 4.2 `.vendor_kit/version.local.toml`

不進 git（自有 .gitignore 擋）；與 version.toml **同形**（同一套讀寫器）；寫入者 dev／undev／bootstrap `--local`；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；CI 模式下存在任何覆寫 → sync 回 1。啟動器先讀它再退回 version.toml。<sub>[proposal §3；v2.1 A；isolation B(b)；review C3、I-31]</sub>

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 否 | 本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）<sub>[proposal §2；#27]</sub> |
| `vendor_kit_image_id` | string | 有 `vendor_kit` 時必填 | `sha256:<hex64>`，dev 時解析；啟動器每次 `docker image inspect` 比對，同 tag 重 build 才會被發現；`undev vendor_kit` 一併撤 <sub>[v2.2 B；review C2]</sub> |
| `schema`、`written_by` | integer、string | 是 | 同通則 |
| `[tools].<repo>` | string | 否 | `path:<dir>`（絕對路徑）；cache/<repo>/ 為 symlink → `<dir>/dist` <sub>[proposal §2、§3；review C3]</sub> |

```toml
vendor_kit = "vendor_kit:dev"
vendor_kit_image_id = "sha256:<image id>"
schema = 1
written_by = "v1.0.0"

[tools]
<repo> = "path:/home/me/<repo>"
```

### 4.3 `baseline/<repo>/.vendor_kit.toml`（metadata）

進 git；寫入者 add／upgrade；兼作 baseline/<repo>/ 空目錄佔位；apply 重驗指紋時一起比；檔案版遷移由 `upgrade vendor_kit` 做並在 dry-run 明列。<sub>[proposal §3；grilling 相容性其餘採納]</sub>

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema`、`written_by` | integer、string | 是 | 同通則 |
| `source` | string | 是 | 這份基準版來自哪個下游 image `<ref>`（tag@index digest）= 最後合併版本；≠ version.toml → sync 本機 warn／CI 1 + 6-5；upgrade 先補待合併到該版然後停 <sub>[review C4；v2.2 D]</sub> |
| `local_image_id` | string | `add --local` 時 | `sha256:<hex64>`：本機 image ID ↔ `source` 的 index digest 對照，供離線驗證 <sub>[grilling Q26]</sub> |
| `complete` | bool | 是 | add 走完 fetch → 初始檔 → 基準版才 true；缺或 false → sync 1 + 6-13；true 且再 add → 0 無變更 <sub>[interface；proposal §2]</sub> |
| `conflicts` | array of string | 是（可空） | upgrade 回 2 時留標記或解析失敗的 dest 清單；仍含標籤 → 2 停；解析失敗的 dest 其基準版不推；解完重跑才清空 <sub>[v2.2 D；review Claude 原文 29]</sub> |
| `[[file]]` | table array | 每個範本一筆 | `dest`（string，相對專案根）；`state`（string，單一列舉）∈ `managed`（已納管）／`appended`（append 已插入）／`declined`（新增檔被拒、從未納管）／`unmanaged`（本來就有、沒納管）／`deleted`（下游使用者刪了已納管檔，upgrade 維持刪除）；`declined_hash`（string，選填）= 最近一次被拒絕的那版範本 N 的 sha256。**declined 語意（v2.7-3）**：`state=declined` 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新（換版、三方合併、append 行替換、二進位換版）→ state 不變、只記 `declined_hash`（新版再變才再問）；add 時 `strategy=append` 檔已存在且拒絕 → `unmanaged`（只記 `declined_hash`）；新版 N 的 hash ≠ `declined_hash` → 再問一次，相同 → 不問但 6-6／6-8；`lines`（array of string，只在 appended）= 實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）<sub>[grilling Q13、Q14、Q15、16 條；review C4、I-21、I-22]</sub> |
| `[progress]` | table | 交易中 | `state = "in-progress"`、`started`（UTC ISO 8601）、`verb`、`id`（= trace_id，§4.10）、`done`／`pending`（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、sync／update 6-33 結束 1、help 6-33 仍 0 <sub>[v2.2 C；v2.3 §6；v2.5-3；v2.10-6；v2.12 L5]</sub> |

註：install 對根 `.dockerignore` 的四行 append 不屬任何工具，記於 `baseline/.vendor_kit.toml`（同 schema，只含 `[[file]]` dest=`.dockerignore` state=appended lines=四行），uninstall 讀它刪原文相同行。<sub>[grilling Q22 補；本規格為實作補齊]</sub>

upgrade 逐檔狀態機（B=基準版、D=磁碟、N=新版讀自 `/dist/<repo>`；只對 state=managed、無待解衝突）：D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 `git merge-file --diff3`（標籤 `<<<<<<< vendor_kit:baseline` 等），衝突 → 2；不論結果基準版推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → **問後換**、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 `conflicts`、基準版不推。任何拒絕 → 記 `declined_hash`；只有「新檔從未建立」的拒絕才 state=declined，已納管檔拒絕 state 不變（v2.7-3）。<sub>[isolation C；proposal §5；v2.5-2、-4；review 必修 10；base_pitfalls 2-12；v2.7-3]</sub>

### 4.4 `gen/.stamp`、`gen/<repo>.stamp`、`gen/tools.just`（不進 git）

| 檔 | 寫入者 | 內容 |
|---|---|---|
| `gen/.stamp` | 只由 install／upgrade vendor_kit | 第一行 = 產生薄殼的引擎 ref（local 覆寫時為 `<tag>`），供 sync grep 快速比對；**不承擔薄殼 hash**（含 log.sh：其 hash 在自身自描述首行；第十版「gen/.stamp 記 log.sh hash」畫法撤回）；fresh clone 缺此檔時相容判定改用薄殼自描述首行 <sub>[grilling Q17；review I-15；v2.14-1]</sub> |
| `gen/<repo>.stamp` | fetch | 第一行 = 多架構 index digest `sha256:<hex64>`（與 version.toml 一致；`add --local` 亦為正式 index digest，本機驗證用 metadata `local_image_id`）或 dev 時 `path:<dir>`；**無 `image:<tag>` 形**；之後每檔一行 `<sha256>  <相對路徑>`（files/…、init.toml、just/<ns>.just）；verify 逐檔比 <sub>[v2.3 §3；#26；grilling Q26；review 必修 15]</sub> |
| `gen/tools.just` | sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換 | 每個 `<ns>.just` 一行 `mod? <ns> '../cache/<repo>/just/<ns>.just'`（一工具可多行），每行上方一行 `# <description>` 註解；零 set 零 recipe <sub>[v2.1 E；v2.3 §3；base_pitfalls 2-4；review 必修 2]</sub> |

### 4.5 薄殼（進 git，vendor_kit 擁有，人不改）

| 檔 | 內容 |
|---|---|
| 自描述首行 | entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：`# vendor_kit-shell/<P> engine=<vX> sha256=<hash>`；hash = 首行（含其換行）之後全部位元組 CRLF→LF 正規化後的 sha256（check.sh 的 shebang 行算進內容）；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 + 6-28 列差異不動（下游使用者 `git checkout` 還原後再跑）；mode 變更只 warn <sub>[grilling Q17；review Claude 原文 28；base_pitfalls §5 CRLF]</sub> |
| `entry.just` | `mod vendor_kit 'vendor.just'` + `import? 'gen/tools.just'`；零 set 零 recipe <sub>[proposal §2、§3]</sub> |
| `vendor.just` | 動詞 recipe 一行轉發 + 啟動器本體（POSIX sh recipe）；`set positional-arguments` 只放這；若實作把啟動器拆成獨立檔，該檔納入本表並帶自描述首行 <sub>[proposal §2]</sub> |
| `.gitignore` | `cache/`、`gen/`、`version.local.toml`、`.tmp.*`、`log/` <sub>[proposal §3；grilling Q22；v2.12 L1]</sub> |
| `log.sh` | 啟動器 log 函式（自外部 repo 的 `dist/script/docker/lib/log.sh` 移植成 POSIX sh（出處見註記），§4.10）；內嵌啟動器事件白名單（`case`）；由引擎 shell 模組重產（install／upgrade vendor_kit），**帶自描述首行 `# vendor_kit-shell/<P> engine=<vX> sha256=…`**，hash 不記 gen/.stamp；vendor.just 內啟動器 `. ./log.sh`。薄殼由四檔改**五檔**：entry.just、vendor.just、log.sh、.gitignore、ci/check.sh（+ version.toml）<sub>[v2.13 P9；v2.14-1]</sub> |
| `ci/check.sh` | §7 |
| 根 justfile（專案檔） | install 只加一行 `import '.vendor_kit/entry.just'`；無檔則建，內容逐字四行：<br>`import '.vendor_kit/entry.just'`<br>（空行）<br>`default:`<br>`\t@just --list`<br>（`default: @just --list` 單行為 just 語法錯誤）；uninstall 只刪完全相同行 <sub>[proposal §2；review 必修 1]</sub> |
| 根 `.dockerignore`（專案檔） | install append 四行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`（無則建；有則問）；uninstall 問後逐行只刪原文相同行 <sub>[grilling Q22 補；v2.9-5；v2.12 L1]</sub> |

### 4.6 `.vendor_kit/.tmp.*`

| 檔 | 規格 |
|---|---|
| `.tmp.<verb>.<id>.toml` | install（第一次也建：兼「不留半成品」的清除清單，成功後刪；修復型同；v2.13 P5）／remove／uninstall／undev／prune／dev（新規則 (b)：記要寫的覆寫行、symlink 目標、印記第一行）／`upgrade vendor_kit`（含 E(a) 自身段）的進度檔（metadata 會被刪、不存在、或本動詞不碰 metadata）；`<id>` = 交易 id = 啟動器產的 **trace_id**（32 hex，§4.10；不用 `<repo>` 以免 uninstall 多工具撞名）；內容 = `schema`、`written_by`、`verb`、`id`、`targets`（array）、`started`、`done`／`pending`、`consents`（已取得的同意）；成功結束時刪；未完成 → 可寫動詞恢復、sync／update 6-33 結束 1、help 6-33 仍 0；prune 遇未恢復者只列出（6-33）、不刪、不視為未完成交易（v2.7-7）；`undev`（含 `undev vendor_kit`）的日誌記要撤的覆寫行與 image ID；**`.tmp.upgrade.<id>.toml`**（自身升級）另記舊引擎 ref、目標引擎 ref、計畫 image ID，在改 version.toml 第一行**之前**建，新引擎重產薄殼完成後由新引擎刪，恢復 = 重跑 `upgrade vendor_kit`（v2.11-1，撤回 v2.10-4「不建日誌」的例外）；`.tmp.prune.<id>.toml` 在 `apply prune` 清理前建 <sub>[grilling 進度日誌、Q24；review C5、I-33；v2.7-6、-7；v2.9-6、-8；v2.10-6；v2.11-1；v2.12 L5]</sub> |
| `.tmp.dist.<id>/` | 啟動器暫存（展開的工具 dist、`vk-resolve`）；trap 刪；prune 清殘留 <sub>[grilling Q24]</sub> |

兩者皆由自有 .gitignore `.tmp.*` 擋。

### 4.7 下游 repo 側 `dist/`、`dist/init.toml`、`Dockerfile.dist`、image

| 項目 | 規格 |
|---|---|
| `dist/` 佈局 | `dist/files/`（全部出貨，原樣展開到 cache/<repo>/files/）、`dist/init.toml`、`dist/just/<ns>.just`（每檔一個頂層命名空間，數量工具自決，`<repo>.just` 必須存在，每檔含 §3.6 `_sync`）；symlink／hardlink／特殊檔第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF <sub>[proposal §4；v2.2 E；#29；review I-41]</sub> |
| `Dockerfile.dist` | 逐字三行：`FROM scratch`／`LABEL io.github.<org>.vendor_kit=1`／`COPY dist/ /dist/`；純資料，不承諾可執行、vendor_kit 不檢查 binary；缺 LABEL → check.sh --dist 失敗（image 的 label 只能在 build 時加，pull 無法追加）<sub>[proposal §4；grilling Q21、16 條；review 必修 14]</sub> |
| image 命名 | 工具 `ghcr.io/<org>/<repo>-dist:<tag>`；引擎 `ghcr.io/<org>/vendor_kit:vN`；皆多架構 amd64+arm64（同一次 buildx）；工具 dist COPY-only、CI 驗兩平台位元組一致；引擎 image 只驗兩平台 LABEL（protocol／schema）一致；引擎 image 公開，工具自決（公開不可逆）；已釋出 image／index 子 digest／Release 資產／fixture 永不刪 <sub>[proposal §4；grilling Q4、Q7、相容性；review 必修 16]</sub> |
| label | 鍵前綴 `io.github.<org>.vendor_kit`。啟動器建的容器／network／volume：`…=1`、`….project=<專案根絕對路徑>`；引擎 image（build 時）：`…=1`、`….protocol=<floor_P>-<current_P>`、`….schema=<N>`；下游 image（build 時）：`…=1`。專案路徑 label 不加在 image 上。<sub>[grilling 9 補充、Q24；review B5、必修 14]</sub> |
| 工具契約（初始檔與 recipe） | 初始檔只能引用穩定入口 `just <ns> …`、`.vendor_kit/ci/check.sh`、`.vendor_kit/entry.just`、`.vendor_kit/version.toml`；不得寫死 cache 內部路徑；交付物執行期不得依賴 `.vendor_kit/`、version.toml、GHCR；rename／格式變更不得以 copy/append 假裝完成；工具 recipe 用 `cd {{quote(justfile_directory())}}` 回專案根，禁止相對 working-directory；每個公開 recipe 相依 `_sync`（§3.6）；工具的 build 若以專案根當 context，依賴 install 加進根 `.dockerignore` 的排除 <sub>[grilling Q14、deploy、Q22；base_pitfalls 1-4、2-13；proposal §4]</sub> |

`dist/init.toml`：

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema` | integer | 是 | 建置期契約（同 image 內讀寫），不進執行期矩陣 <sub>[contract 4；base_pitfalls 1-11]</sub> |
| `description` | string | 否 | 頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod 上方 `# <description>`；缺則 `<repo> <tag>` <sub>[review C6；base_pitfalls 2-4]</sub> |
| `[[file]].src` | string | 是 | 相對 `dist/`；正規化、不得越出 dist/ <sub>[review C6]</sub> |
| `[[file]].dest` | string | 是 | 相對專案根；正規化、不得越出 repo、不得指向 `.vendor_kit/`、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；append/append 允許（各工具行分開記，重疊或歸屬不明 → 拒絕）；引擎與 lint 都驗 <sub>[proposal §4；v2.2 E；review I-41]</sub> |
| `[[file]].strategy` | string | 否 | `"copy"`（預設）或 `"append"`，只有這兩值；根 `.gitignore`／`.dockerignore`／`.editorconfig` 類必須用 append，用 copy 指向它們 → check.sh --dist 報錯 <sub>[grilling Q12、Q6]</sub> |

```toml
schema = 1
description = "<repo> 的專案範本與 just recipe"

[[file]]
src = "files/Dockerfile"
dest = "Dockerfile"

[[file]]
src = "files/gitignore.snippet"
dest = ".gitignore"
strategy = "append"
```

### 4.8 離線包（Release 資產）

每個平台 tar（`docker save`）旁附同名 `.digest` 旁檔：`<name>.tar` + `<name>.tar.digest`，內容一行 `sha256:<hex64>` = 該 image 的正式多架構 index digest。`bootstrap.sh --local <tar>`／`add --local <tar>`：`docker load` 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 `local_image_id`；旁檔缺 → 1。`bootstrap.sh --local <tag>`（tag 形）**不讀旁檔**：正式 ref 來源 = 專案已有 version.toml → 該行；第一次接入 → bootstrap.sh 內嵌引擎 ref；本機 image ID 只記 version.local.toml。`add --local` **只收 tar**、無 tag 形（新工具沒有既有 digest 可當來源）；不提供 `--digest`。離線包 `vendor_kit-vN-local.tar.gz` = bootstrap.sh + 各平台 tar + `.digest`，另附 `local_bootstrap.sh` 便利包裝（非契約，見 §1.2 bootstrap.sh）。離線可用：啟動器先 `docker image inspect`，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1「拉不到」不 hang（逾時）；離線 upgrade 不支援。<sub>[grilling Q26、19條-11、2026-09-20；v2.9-1；v2.10-2、-3；v2.11-2]</sub>


### 4.9 `.vendor_kit/config.toml`

| 項目 | 規格 |
|---|---|
| 進 git | 是。寫入者：install（建，含註解與預設值；修復型缺則建、存在不動）；`upgrade vendor_kit` 視為**三方合併初始檔**（B = 基準版副本、D = 磁碟、N = 新版範本，走 §4.3 狀態機與 6-22 詢問；`-y` 免問）；下游使用者可手改（要改先問、永不覆蓋）。基準版副本 = `baseline/vendor_kit/config.toml`（install 建、`upgrade vendor_kit` 推進），metadata 記在 `baseline/.vendor_kit.toml`（與根 `.dockerignore` 同表，`[[file]]` dest=`.vendor_kit/config.toml` state=managed）；uninstall 比照初始檔保護模式（hash == 副本 → 刪，被改 → 留並列出）。**例外於 §4 通則：config.toml 不寫 `written_by`、也不寫 `schema` 以外的任何機器欄位**（下游使用者可編輯、含註解），只保留 `schema = 1`。<sub>[v2.12 L3′；v2.13 P6、P10]</sub> |
| 缺檔／缺鍵 | = 預設值，不警告、不自動補建（只有 install／upgrade vendor_kit 會建）。<sub>[v2.12 L3′]</sub> |
| 值檢查 | `keep`、`days` 只收正整數；`0`、負數、非數字、非整數 → 該鍵用預設 + 警告（stderr 與執行紀錄同句，`config_read` 事件）；未知欄位讀時忽略、寫時保留（§4 通則）；`schema` 高於支援 → 3 + 6-19。<sub>[v2.12 L3′；§4 通則]</sub> |
| 引擎讀法 | TOML parser；**parser 以 stage 明確帶進引擎 image**：`COPY --from=ghcr.io/ycpss91255-docker/toml-bridge:<tag>@sha256:…`，不依賴基底 Python 的 `tomllib`。<sub>[v2.12 L3′]</sub> |
| 啟動器讀法 | 不解析 TOML：只 grep 正規行 `^keep *= *[0-9]+ *$`、`^days *= *[0-9]+ *$`（POSIX BRE 寫法 `^keep[[:space:]]*=[[:space:]]*[0-9][0-9]*[[:space:]]*$`）；命中恰 1 且為正整數 → 採用；命中 0 → 預設（不警告）；其餘（重複、非正整數）→ 預設 + 警告；檔不可讀 → 預設 + 警告。**待議**：config 鍵變多時改由引擎產啟動器專用平面檔或其他方式（§9.1 P1）。<sub>[v2.12 L3′；grilling 2026-09-20]</sub> |
| 正規行契約 | `keep`／`days` 行唯一正規形：整行 `keep = 50`——行首無空白、鍵後一個空白、`=`、一個空白、十進位整數、無尾端註解、LF 結尾；引擎寫出一律此形；註解只准獨立成行；兩鍵必在 `[log]` 表內、其他表不得再出現同名鍵（啟動器 grep 不分表）。<sub>[v2.12 L3′；同 §4.1 版本鎖定行精神]</sub> |

| 欄位 | 型別 | 必填 | 預設 | 說明 |
|---|---|---|---|---|
| `schema` | integer | 是 | `1` | 同 §4 通則 |
| `written_by` | — | **不寫** | — | 例外於 §4 通則：config.toml 是下游使用者可編輯的檔，不放機器欄位（v2.13 P10） |
| `[log].keep` | integer（正） | 否 | `50` | 每個 `log/<verb>/` 目錄最多保留檔數 |
| `[log].days` | integer（正） | 否 | `30` | 每個 `log/<verb>/` 目錄保留天數；與 `keep` 同時生效、較嚴者勝 |

install 寫出的範本（逐字；同一份也放 `baseline/vendor_kit/config.toml`）：
```toml
# vendor_kit 設定檔（進 git）。缺檔或缺鍵 = 預設值；非正整數會退回預設並警告。
schema = 1

[log]
# 每個動詞目錄最多保留的執行紀錄數（正整數）
keep = 50
# 執行紀錄保留天數（正整數）；與 keep 同時生效，較嚴者勝
days = 30
```

### 4.10 執行紀錄（`.vendor_kit/log/`）

| 項目 | 規格 |
|---|---|
| 位置與切割 | `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`；`<verb>` = vendor_kit 動詞名（`upgrade vendor_kit`、不帶 repo 的 `upgrade` 皆在 `upgrade/`；bootstrap.sh 自身那段在 `bootstrap/`，由 bootstrap.sh 自己建目錄、產 trace_id、寫 `launcher_start`，install 失敗清半成品時 `log/` 保留；v2.13 P4）；`<UTC-ts>` = `YYYYMMDDTHHMMSSZ`；`<id8>` = trace_id 前 8 碼。**一次執行一檔**：同一次啟動器呼叫（含 §3.4 接手的第二個引擎、resolve 與 apply 兩個容器）append 同一檔，同一時間只有一個寫者；不做 latest symlink（Windows／CIFS 上 symlink 不可靠，檔名排序即可）。目錄內自帶 `.gitignore`（`*`／`!.gitignore`；由啟動器第一次建 `log/` 時一起建）；`.vendor_kit/.gitignore` 列 `log/`；根 `.dockerignore` 由 install append `.vendor_kit/log/`（三行改**四行**，與 Q22 cache 同理；v2.13 P13）。<sub>[v2.12 L1；agy_summary 前例 npm `_logs/`；出處：base `log/<verb>/<ts>-<traceid8>.log`]</sub> |
| 格式 | JSON Lines：UTF-8、每行一個 JSON object、LF 結尾、無空行；欄位名對齊現行 OTel Logs Data Model（`EventName` 為頂層欄位，`Body` 留給人讀訊息），**不引 OTel SDK**；捨棄 `observed_timestamp`、`span_id`、`trace_flags`、`severity_number`、`resource`、`instrumentation_scope`。欄位表見下。<sub>[v2.12 L2；agy_summary「JSONL+OTel 適用性」]</sub> |
| 保留 | 每個 `log/<verb>/` 目錄各自「最近 `days`（預設 30）天**且**最多 `keep`（預設 50）檔」，較嚴者勝；年齡用檔名時間戳（不用 mtime）、計數用檔名排序；由**啟動器**在每次呼叫結束時（trap 內、`launcher_exit` 前）prune，**best-effort**：失敗只 warn、不改結束碼；只刪 `*.jsonl`，不刪 `.gitignore`、不刪本次的檔；記 `log_prune` 事件。值來自 config.toml（§4.9）。不屬 `prune` 動詞。<sub>[v2.12 L3；出處：base 為 20／14]</sub> |
| 寫失敗（fail-closed） | **先確認能寫才開始**：啟動器 mkdir + 建檔 + 寫 `launcher_start` 任一失敗 → 1 + 6-38、零寫入（不進引擎 ref 取得、最低介面版檢查、docker）；引擎 append `engine_start` 失敗 → 1 + 6-38、不進 resolve／apply。所有動詞一致（含 help、prune、sync 快路徑、`--dry-run`）；無 `--no-log`。磁碟滿連 `prune` 也擋：6-38 附清空間提示。理由：紀錄以備追責；never fail silently。<sub>[v2.12 L4（取代 draft「不改結束碼」與 agy「唯讀動詞放行」）]</sub> |
| 憑證與敏感值 | `VENDOR_KIT_REGISTRY_TOKEN`／`_USER`／`_TOKEN_FILE` 內容永不記；`attributes` 不收環境變數；URL 一律去 userinfo；不記 `docker login` 相關輸出。驗收：所有 log 檔 grep 不到 token（§7.4-18）。<sub>[v2.12 L6；#28]</sub> |
| 6-xx 訊息 | 凡印到 tty 的訊息（含 §6 全部）一律**同句**進 `body`，並在 `attributes.message_id` 記 `6-xx`；問句記 `prompt_asked`、回答記 `prompt_answered`（`auto: true` 表 `-y`）。<sub>[v2.12 L2、L6]</sub> |
| trace_id | 32 hex，由啟動器產：`/proc/sys/kernel/random/uuid` 去 `-`；缺則 `od -An -N16 -tx1 /dev/urandom` 去空白（白名單加 `od`、`tr`）；同值 = 進度檔交易 id `<id>`（§4.6）；以 `TRACEPARENT`（W3C Trace Context `00-<trace_id>-<span_id>-<flags>`；span_id／flags 為實作細節，引擎只取 trace_id）傳給每個引擎容器（含 §3.4 接手的第二次，同值）；啟動器一律自產，不採用環境中既有的 `TRACEPARENT`。<sub>[v2.12 L5；agy_summary2「trace_id 傳遞前例」（`TRACEPARENT` 為 otel-cli／Thoth 事實標準）]</sub> |
| 啟動器 argv | `launcher_start` 記**完整原始 argv**（`"$@"` 逐項、array of string，不論合法與否、不做任何正規化）；引擎 `engine_start` 再記一次收到的 argv。逐項 JSON 跳脫（採 `decisions/log/json_escape_fixed.sh`，dash 與 busybox sh 實測 15 案例通過）：順序 `\` → `\\`、`"` → `\"`、U+0008／0009／000C／000D → `\b`／`\t`／`\f`／`\r`、其餘 U+0001–001F → `\u00XX`、換行 → `\n`；全程 `printf '%s'`、不用 `echo`、只跑一次 sed。已知限制：NUL 進不了 shell 變數；無效 UTF-8 位元組原樣輸出。<sub>[v2.12 L5；agy_summary2 修正版]</sub> |
| 引擎寫法 | 以 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` 定位（§5；v2.13 P8）；每個子命令容器各自 `engine_start`／`engine_exit`（v2.14-2）；Python `logging` + JSON formatter（`json.dumps`）append 同一檔（`open(path, 'a')` + 每筆 flush），不引 OTel SDK；核心模組只透過單一介面 `log_event()` 呼叫，log 與 ci 為輔助模組（不是 sidecar 容器）；引擎不做保留清理。<sub>[v2.12 L5、架構]</sub> |
| 啟動器寫法 | 薄殼第五檔 `log.sh`（§4.5；由引擎重產、帶自描述首行）：移植外部 repo 的 `dist/script/docker/lib/log.sh` 到 POSIX sh（出處見註記），API `_log_<level> <event> [k=v]…`；`body` → `event_name`、`service.name` → `component` + `verb`；bats 測試隨附。sync 快路徑不起引擎，由啟動器自己寫 `sync_fast_path`（實測 grep 0.00 s vs 引擎容器 0.42 s，且不依賴 daemon）。<sub>[v2.12 L5、架構；出處：base log.sh]</sub> |
| 事件註冊表落點 | 真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌一份啟動器事件白名單（`case`）；release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（同 base）。<sub>[v2.13 P9]</sub> |
| 零寫入例外 | 「零寫入」= 不寫任何專案檔，執行紀錄例外：`launcher_start`／`engine_start` 已寫屬預期（結束碼 3、6-12、6-30、6-37 等情境皆同）。<sub>[v2.13 P12]</sub> |
| lnav | Release 資產附 lnav format 檔：`json: true`、`timestamp-field: timestamp`、`level-field: severity_text`、`opid-field: trace_id`（timeline 用；須含在 line-format）、`body-field: body`、`file-pattern` 對 `.vendor_kit/log/*/*.jsonl`；`attributes/duration_ms` 供 timeline duration。<sub>[v2.12 L5；agy_summary「lnav timeline 需要的欄位」]</sub> |

欄位表（每行）：

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `timestamp` | string | 是 | ISO 8601 UTC，微秒：`YYYY-MM-DDTHH:MM:SS.ffffffZ`；啟動器端試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級補零；引擎一律微秒（v2.13 P7） |
| `severity_text` | string | 是 | `DEBUG`／`INFO`／`WARN`／`ERROR`／`FATAL`（對齊 OTel SeverityText；warn 與 error 事件對應印到 stderr 的 warn／錯誤） |
| `event_name` | string | 是 | 事件註冊表內的名稱（下表）；未註冊 → FATAL |
| `body` | string | 否 | 人讀一句話；凡印到 tty 的訊息一律同句進此欄 |
| `trace_id` | string | 是 | 32 hex；= 進度檔交易 id |
| `attributes` | object | 是 | 必有 `component` ∈ `launcher`／`engine`、`verb`；其餘依事件：`phase` ∈ resolve／apply／single、`path`、`action` ∈ create／modify／append／delete、`exit_code`、`duration_ms`、`message_id`、`prompt`、`answer`、`auto`、`argv`（array of string）、`engine_ref`、`cwd`、`launcher_version`、`ci`、`ref`、`digest`、`reason`、`keep`、`days`… |

事件集合（**L6：依建議先行，待 codex 審過才最後定案**；審後只准增刪事件名與屬性，不改欄位表）：

| component | event_name | 時機 | 主要 attributes |
|---|---|---|---|
| launcher | `launcher_start` | 建檔後第一筆 | `argv`（完整原始）、`verb`、`engine_ref`、`cwd`、`launcher_version`（薄殼首行 `engine=<vX>`）、`ci`（CI 模式真值） |
| launcher | `config_read` | 讀 config.toml 後 | `keep`、`days`、`source` ∈ file／default、警告（非正整數時，body 同句） |
| launcher | `docker_pull_start`／`docker_pull_finish` | 每筆 `pull` 記錄 | `name`、`ref`、`exit_code`、`duration_ms`、`reason`（逾時／網路／認證／不存在／主機錯誤） |
| launcher | `docker_extract` | 每筆 `extract` 記錄 | `repo`、`ref`、`path`（`.tmp.dist.<id>/<repo>/`） |
| launcher | `engine_spawn` | 每次 docker run 引擎前 | `engine_ref`、`subcommand`（resolve／apply／單段 verb）、`interactive` |
| launcher | `sync_fast_path` | sync 快路徑判定 | `result` ∈ hit／miss、`reason` |
| launcher | `log_prune` | trap 內保留清理後 | `deleted`（數）、`keep`、`days`、`error`（best-effort 失敗時） |
| launcher | `launcher_exit` | 最後一筆 | `exit_code`、`duration_ms`、`reason` |
| engine | `engine_start` | 子命令第一筆 | `argv`（收到的）、`verb`、`subcommand`、`engine_version`、`protocol` |
| engine | `journal_detected`／`journal_recovered` | 偵測到／恢復未完成交易 | `verb`、`id`、`path`、`result`（唯讀動詞只有 detected） |
| engine | `resolve_finish` | resolve 結束 | 計畫摘要（pull／extract／mount／engine 筆數、`apply` yes／no）、`fingerprint` |
| engine | `lock_acquired` | apply 拿到 flock | `wait_ms` |
| engine | `fingerprint_verified` | apply 重驗指紋 | `result` |
| engine | `journal_created`／`journal_deleted` | 進度檔建／刪 | `path`、`verb`、`id` |
| engine | `prompt_asked`／`prompt_answered` | 每個詢問 | `prompt`（6-20／6-21／6-22／6-32／6-34）、`path`、`answer` ∈ yes／no／eof、`auto`（true = `-y`） |
| engine | `file_created`／`file_modified`／`file_appended`／`file_deleted` | 每個實際寫入 | `path`、`action`、`strategy`、`lines`（appended 時） |
| engine | `merge_conflict` | 三方合併衝突 | `path` |
| engine | `declined` | 拒絕（記 `declined_hash`） | `path`、`state` |
| engine | `version_written` | version.toml 寫入 | `path`、`changed`（鍵清單） |
| engine | `registry_query` | 每次查 registry | `host`、`repo`、`result`、`duration_ms`（URL 去 userinfo；不記 token） |
| engine | `prune_candidate`／`prune_removed` | prune 候選／已刪 | `kind` ∈ container／image／network／volume／tmp、`id` |
| engine | `engine_exit` | 最後一筆 | `exit_code`、`message_id`、`duration_ms`、`summary` |

<sub>[v2.12 L6；draft 方案 A 事件集合]</sub>

範例（`sync` 快路徑，一檔三行；`…` 省略）：
```
{"timestamp":"2026-09-20T01:02:03.000000Z","severity_text":"INFO","event_name":"launcher_start","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","argv":["sync"],"engine_ref":"ghcr.io/<org>/vendor_kit:v1.0.0@sha256:…","cwd":"/home/me/<專案根>","launcher_version":"v1.0.0","ci":false}}
{"timestamp":"2026-09-20T01:02:03.004000Z","severity_text":"INFO","event_name":"sync_fast_path","body":"快路徑：stamp 與 version.toml 全相符","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","result":"hit"}}
{"timestamp":"2026-09-20T01:02:03.006000Z","severity_text":"INFO","event_name":"launcher_exit","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","exit_code":0,"duration_ms":6}}
```

## 5. 環境變數與參數

| 名稱 | 讀者 | 規格 |
|---|---|---|
| `VENDOR_KIT_REGISTRY_TOKEN` | 引擎 resolve 模組 | registry 讀取憑證（GHCR：PAT classic `read:packages`，細節手動測後定）；只在 update／upgrade 的 resolve 階段以 `-e` 傳；不寫 log／檔、不傳給工具、dry-run 不印 <sub>[grilling Q11；#28]</sub> |
| `VENDOR_KIT_REGISTRY_USER` | 同上 | 換 token 的使用者名（GHCR 任意非空）<sub>[#28]</sub> |
| `VENDOR_KIT_REGISTRY_TOKEN_FILE` | 同上 | 主機檔路徑；啟動器 `-v <file>:/run/vk-token:ro` 並以 `-e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token` 傳容器內路徑；與 `_TOKEN` 同時設定 → 1「只能擇一」<sub>[#28；review 必修 5、I-36]</sub> |
| `VENDOR_KIT_NO_LOCK` | 引擎 resolve 模組 | `=1` 跳過 flock；啟動器轉發 <sub>[proposal §6；review 必修 5]</sub> |
| `VENDOR_KIT_PULL_TIMEOUT` | 啟動器（不轉發） | 單次 pull 總秒數，預設 `300`，只收正整數（`0`／非數字 → 1）；`--timeout` 優先 <sub>[grilling 19條-14、Q24；review B3]</sub> |
| `TRACEPARENT` | 啟動器產 → 轉發引擎 | W3C Trace Context `00-<trace_id 32 hex>-<span_id 16 hex>-<flags 2 hex>`；trace_id 由啟動器自產（§4.10），每次 docker run 皆傳（含 §3.4 接手，同值）；引擎只取 trace_id 當執行紀錄 `trace_id` 與進度檔 `<id>`；不採用下游使用者環境既有值；與 `VENDOR_KIT_LOG_FILE` 並用 <sub>[v2.12 L5；v2.13 P8]</sub> |
| `VENDOR_KIT_LOG_FILE` | 啟動器產 → 轉發引擎 | 容器內路徑 `/repo/.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（啟動器建的那一檔）；每次 docker run 皆傳（含 §3.4 接手，同值）；引擎 append 同一檔、不另開檔；不採用下游使用者環境既有值；在 `-e` 白名單（§3.1）<sub>[v2.13 P8]</sub> |
| `CI` | 啟動器（CI 模式判定）→ 轉發引擎 | 真值規則：非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；check.sh `export CI=1` <sub>[review 必修 4]</sub> |
| `HTTP_PROXY`／`HTTPS_PROXY`／`NO_PROXY` | — | v2（issue），第一版不轉發 <sub>[grilling 19條-2]</sub> |
| 其餘 `VENDOR_KIT_*` | — | 不轉發；README 一節列出全部 `VENDOR_KIT_*` 與 `CI`，lint 擋未列者 <sub>[base_pitfalls 2-6；review B2]</sub> |
| docker label | 啟動器／prune | §4.7 |
| 暫存目錄 | 啟動器 | `.vendor_kit/.tmp.dist.<id>/`（§3.1）；不用 `TMPDIR` |
| 引擎容器內 | 引擎 | `LC_ALL=C.UTF-8`、`TZ=UTC`、`HOME=<容器內暫存>`（實作細節）<sub>[grilling 19條-3、-4]</sub> |

## 6. 訊息文字清單（逐字；`<…>` 為占位符；每句含可直接複製的指令）

「類別」欄依 §0「結束的兩種語意」：**需人處理**（印指令、橙）／**失敗**（紅）；問句與不改結束碼的提醒標「—」；**待審** = 依訊息內容難以判定、待使用者定。<sub>[01 頁拍板 2026-09-20 (4)]</sub>

| # | 時機 | 文字 | 類別 | 來源 |
|---|---|---|---|---|
| 6-1 | sync 發現 gen/.stamp 第一行 ≠ 引擎 ref（含 undev vendor_kit 後） | `vendor_kit 已更新 <vX> → <vY>，請執行：just vendor_kit upgrade vendor_kit`（結束 1；缺 gen/.stamp 時 `<vX>` 讀薄殼自描述首行）| 需人處理 | <sub>[review D1；grilling Q10]</sub> |
| 6-2 | `upgrade vendor_kit` 確實重產薄殼後 | `已升級引擎 <vX> → <vY> 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令`（結束 1）| 需人處理 | <sub>[v2.3 §2；review D1]</sub> |
| 6-2b | 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 | `引擎版本已鎖定為 <vY>，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit`（結束 1）| 需人處理 | <sub>[review codex D1；§3.4]</sub> |
| 6-3 | update／upgrade／add 無 registry 憑證 | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）` | 需人處理 | <sub>[#28；grilling Q11、Q25]</sub> |
| 6-4 | 需詢問但無 tty／EOF 且無 `-y` | `需要確認但沒有終端可互動。請加 -y，或在終端執行。`（結束 1）| 需人處理 | <sub>[grilling 19條-6]</sub> |
| 6-5 | CI 下基準版落後 version.toml；Renovate PR 需合併 | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push`（結束 1）| 需人處理 | <sub>[remaining Q5；proposal §7]</sub> |
| 6-6 | dry-run／check.sh 有拒絕過的範本 | `有 <N> 個範本你拒絕過` | —（提醒，不改結束碼） | <sub>[grilling Q14]</sub> |
| 6-7 | dry-run／check.sh 未納管檔 | `<X> 沒納管，與範本差 <N> 行` | —（提醒，不改結束碼） | <sub>[grilling Q15]</sub> |
| 6-8 | dry-run／check.sh 拒絕過且新版有更新 | `<Y> 你拒絕過，<vZ> 有新版` | —（提醒，不改結束碼） | <sub>[grilling Q15]</sub> |
| 6-9 | 不在專案根執行 | `請到 <dir> 執行`（結束 1）| 需人處理 | <sub>[grilling Q20 修正]</sub> |
| 6-10 | `upgrade vendor_kit@<舊版>` 無法無損讀 | `目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。未修改任何檔。要退回舊版請 git revert 相關 commit。`（結束 3）| 需人處理 | <sub>[grilling Q19、Q23]</sub> |
| 6-11 | add 初始檔已存在（copy） | `<X> 已存在，未納管；範本在 .vendor_kit/cache/<repo>/files/ 可自行比對` | —（提醒，不改結束碼） | <sub>[proposal §2]</sub> |
| 6-12 | apply 重驗指紋不同 | `專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …`（結束 1）| 需人處理 | <sub>[v2.2 C]</sub> |
| 6-13 | sync metadata 無完成標記 | `<repo> 未完成接入，請執行：just vendor_kit add <repo>`（結束 1）| 需人處理 | <sub>[proposal §2]</sub> |
| 6-14 | upgrade 補完待合併後另有新版 | `已補齊 <repo> 至 <vB>；另有新版 <vX>，再跑一次 just vendor_kit upgrade <repo> 可升` | —（提醒，不改結束碼） | <sub>[v2.2 D]</sub> |
| 6-15 | update 末行 | `套用：just vendor_kit upgrade` | —（提醒，不改結束碼） | <sub>[proposal §2]</sub> |
| 6-16 | install 非 git repo | `目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。`（結束 1）| 需人處理 | <sub>[review D2 codex 模板]</sub> |
| 6-17 | `install <repo>` 誤用 | `install 不接受工具名稱。接入工具請執行：just vendor_kit add <repo>`（結束 1）| 需人處理 | <sub>[review D2]</sub> |
| 6-18 | 薄殼／版本低於最低介面版 | `目前薄殼或引擎低於最低介面版 <floor>。請以 bootstrap.sh 重建。`（結束 3、零寫入）| 需人處理 | <sub>[review D2；grilling Q23]</sub> |
| 6-19 | 引擎讀到檔案版高於支援上限 | `無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請使用支援此檔案版的引擎，或使用 version.toml 指定的引擎。`（結束 3、寫入前退出）| 需人處理 | <sub>[review D2、必修 8；grilling Q23]</sub> |
| 6-20 | 問句：根 justfile | `要在 justfile 加這一行嗎：import '.vendor_kit/entry.just'`／`要從 justfile 刪這一行嗎：import '.vendor_kit/entry.just'` | —（問句） | <sub>[proposal §2]</sub> |
| 6-21 | 問句：append | `要在 <X> 加這幾行嗎`（接列出行）／`要刪我們加在 <X> 的這幾行嗎`（接列出行）| —（問句） | <sub>[proposal §2、§5]</sub> |
| 6-22 | 問句：upgrade 逐檔 | `<X> 換成新版？`／`你和新版都改了 <X>，要三方合併嗎？`／`要建 <X> 嗎`／`<X> 是二進位檔，要換成新版嗎？` | —（問句） | <sub>[proposal §5；grilling Q14；review 必修 10]</sub> |
| 6-23 | bootstrap just 太舊 | `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。` + 固定兩行 `下載：<平台對應 URL>`、`安裝：<不覆蓋既有檔的安裝指令>`（不新增 curl／tar 主機依賴、不覆蓋既有 just）| 需人處理 | <sub>[review D2；grilling Q8]</sub> |
| 6-24 | docker pull 失敗 | 原文 + 三分類（網路／認證／不存在；另有「主機錯誤」：daemon 不可用、磁碟滿）；認證類：`<ref> 不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login <host>`；僅 add／bootstrap 追加 `離線可用：--local <tar>`；add `--local <v>` 的 `<v>` 不是存在的 `.tar` 檔 → 主機錯誤分類 + `add --local 只接受存在的 .tar 檔：<v>`（結束 1；文案採草擬，待 codex／使用者審，不擋規格；v2.13 P11）| 失敗 | <sub>[base_pitfalls 2-9；remaining Q7；review I-37、I-38；v2.10-3；v2.13 P11]</sub> |
| 6-25 | Renovate PR body（preset `prBodyNotes`） | 6-5 的指令 + `推 commit 後不要勾 rebase/retry` | —（PR 說明文字） | <sub>[remaining Q5]</sub> |
| 6-26 | flock 逾時 | `專案目錄被鎖定（PID <pid>，自 <time>）；60 秒內未釋放。確認無其他 vendor_kit 在跑後重試，或設 VENDOR_KIT_NO_LOCK=1。`（結束 1）| 待審 | <sub>[base_pitfalls 3-8]</sub> |
| 6-27 | 進度檔恢復失敗 | `未恢復：<檔名>`（逐檔列出，結束 1）| 待審 | <sub>[base_pitfalls 3-7]</sub> |
| 6-28 | 薄殼被改（install／upgrade vendor_kit） | `偵測到薄殼被修改：<files>。未重產任何薄殼。請先檢視下列差異；確認並手動還原（git checkout -- .vendor_kit/<file>）後，再執行 just vendor_kit upgrade vendor_kit。`（接差異，結束 1）| 需人處理 | <sub>[review D2；grilling Q10、Q17]</sub> |
| 6-29 | upgrade 新增初始檔 dest 在 CI 路徑（`.github/workflows/`、`.gitlab-ci.yml`） | `注意：新版範本將建立或修改 CI 設定 <X>。請確認下列內容後再決定是否套用。` | —（提醒，不改結束碼） | <sub>[review D2；grilling Q14]</sub> |
| 6-30 | 啟動器驗 vk-resolve 失敗 | `引擎輸出不完整或不相容（<原因>），未執行任何動作。`（結束 1）| 失敗 | <sub>[review 三]</sub> |
| 6-31 | pull 逾時 | `拉取 <ref> 超過 <秒> 秒未完成，已中止。可用 --timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整。`（結束 1）| 失敗 | <sub>[grilling 19條-14]</sub> |
| 6-32 | 問句：prune | `要刪除以上 vendor_kit 資源嗎？` | —（問句） | <sub>[review A1]</sub> |
| 6-33 | 唯讀動詞偵測未完成交易 | `偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>`（sync／update 印後結束 1；**help 印後仍 0**；prune 只列出不刪、不視為未完成交易；可寫動詞不印此句而是先恢復）| 需人處理 | <sub>[review 必修 9；v2.7-7；v2.10-6]</sub> |
| 6-34 | 問句：根 .dockerignore | `要在 .dockerignore 加這四行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.* .vendor_kit/log/` | —（問句） | <sub>[grilling Q22 補；v2.12 L1]</sub> |
| 6-35 | install 巢狀 | `<dir> 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。`（結束 1）| 需人處理 | <sub>[grilling Q20]</sub> |
| 6-36 | 舊薄殼跑新 major 一般動詞 | `薄殼介面版 <P_shell> 低於引擎 <vY> 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit`（結束 3、零寫入）| 需人處理 | <sub>[grilling Q23]</sub> |
| 6-37 | `--local` 值不以 `.tar` 結尾、含 `/`、且存在同名檔（B1 第二支） | `--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。`（結束 1、零寫入）| 需人處理 | <sub>[grilling 2026-09-19 末條；v2.7-2；grilling 三審新定案 2026-09-20；codex r3 R6]</sub> |
| 6-38 | 無法建立或寫入執行紀錄（啟動器 mkdir／建檔／`launcher_start`，或引擎 `engine_start`） | `無法寫入執行紀錄 <path>：<原因>。vendor_kit 不在沒有紀錄的情況下執行。請清出磁碟空間（例如刪除 .vendor_kit/log/ 下的舊檔）或修正權限後重試。`（結束 1、零寫入；所有動詞一致，含 help／prune／sync 快路徑；無 `--no-log`；文案採草擬，待 codex／使用者審，不擋規格；v2.13 P11）| 失敗 | <sub>[v2.12 L4；v2.13 P11]</sub> |

## 7. CI 契約

### 7.1 `.vendor_kit/ci/check.sh`（下游 CI 只呼叫它；GitHub／GitLab 一樣；平台無關）

第一行 shebang、第二行自描述、其後第一個動作 `export CI=1`。<sub>[review 必修 4]</sub>

| 步驟 | 內容 | 結束碼 |
|---|---|---|
| ⓪ | `git ls-files --error-unmatch .vendor_kit/version.local.toml` 命中 → 拒絕 | 1 |
| ① | `sync`（CI 模式） | 1：薄殼不符、未完成接入、基準版落後、任何 local 覆寫；3 |
| ② | verify（印記 sha256，全部工具） | 1 |
| ③ | `upgrade --dry-run` | CI 且需改 tracked 檔 → 1 印清單（version.toml 不動）；仍有衝突標記 → 2；印 6-6～6-8 但不紅燈 |
| ④ | 工具測試 `just <repo> check`（每個 `[tools]` 工具、該 recipe 存在時；不存在則印「無」跳過；工具 check 不得再呼叫 check.sh） | 工具原碼傳出 |
| ⑤ | 專案測試（`just check` 若存在於根 justfile，否則跳過） | 依專案 |

一關過才下一關；全部通過 → 0。**check.sh 整體結束碼 = 第一個失敗步驟的碼**（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）。<sub>[proposal §7；v2.3 §7；review E1、I-44、I-45]</sub>

### 7.2 `check.sh --dist`（下游 repo CI）

驗：dist 佈局（files/、init.toml、just/<repo>.just 存在）、init.toml 合法（schema、`description` 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗）、以 just 1.33.0 解析每個 `<ns>.just`（並擋比 1.33 新的功能）、§3.6 `_sync` lint（`just --dump --dump-format json`）、`Dockerfile.dist` 含 `LABEL io.github.<org>.vendor_kit=1`、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性。<sub>[v2.1 E；#29；base_pitfalls 1-7、2-13；grilling Q21；review 必修 14、F1]</sub>

### 7.3 Renovate preset（放 vendor_kit repo 根目錄 `default.json`；vendor_kit 自身設定用 `renovate.json`；下游 `extends: ["github>ycpss91255-research/vendor_kit"]`）

regex manager 匹配 `**/.vendor_kit/version.toml`（monorepo 子專案亦命中；`(?m)` 多行，key regex 與 §4.1 版本鎖定行契約共用）+ docker datasource，同時擷取 `currentValue`（tag）與 `currentDigest`；PR 只改一行；major 分開 PR（`matchUpdateTypes`）；分組／排程範例；`hostRules` 依 host 不寫死 ghcr.io；`prBodyNotes` = 6-25；不設 `gitIgnoredAuthors`、不改 `rebaseWhen`；postUpgradeTasks 不採（文件附註）。流程：PR CI 以新版跑 §7.1 完整流程；需合併 → 1（6-5）→ 維護者在 PR 分支本機 `upgrade <repo> -y` → commit → push → CI 全部再跑 → 綠了才 merge。<sub>[grilling Q5、CI 平台定案、Q24 E2；remaining Q5；v2.1 E；review 必修 13、I-46]</sub>

### 7.4 驗收矩陣（每條一情境）

驗收 harness 一律**明確設 `CI=0`** 跑會寫檔的完整流程（`install` → `add` → `upgrade` → …），不依賴 GitHub Actions 等平台的 `CI=true` 預設；另設 `CI=1` 案例驗唯讀與拒寫（條 9、32 等）。<sub>[02 頁 6 點定案 ②；grilling 2026-09-20]</sub>

1. 最低介面版以來每個已釋出 `bootstrap.sh(r)` + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 + 6-1、零 tracked 寫入）→ `upgrade vendor_kit`（1 + 6-2、薄殼重產）→ sync 0 → 工具 recipe → `upgrade` 全；**第二次 `upgrade vendor_kit` → 0 無變更**；禁止由候選樹複製 fixture、禁 stub 引擎。<sub>[grilling 相容性驗收 F；review I-27]</sub>
2. 每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境（docker 上界、just latest、arm64、WSL2）按世代覆蓋；成本上限當觸發討論條件。<sub>[grilling 相容性]</sub>
3. **升級後 == 全新安裝**：升級後 `.vendor_kit/` tracked 內容 == 用 C 全新 install + add（排除清單：時間戳、digest、`written_by`）。<sub>[grilling 19條-18]</sub>
4. 連續升級 r_i → r_j → C；固定最低介面版直接跳升 C。<sub>[compat 矩陣]</sub>
5. 降版 `upgrade vendor_kit@<舊版>`：同介面版／檔案版成功；跨檔案版改檔前拒絕 3 + 6-10、零寫入。<sub>[grilling Q19、Q23]</sub>
6. `< floor` 太舊：唯一可用 synthetic fixture；任一動詞 → 3 + 6-18、零寫入；最低介面版檢查發生在任何上網之前（斷網也回 3）。<sub>[compat；grilling Q23]</sub>
7. 舊 bootstrap.sh 在已升級 repo 再跑：用 version.toml 指定引擎，不降版。<sub>[grilling Q18]</sub>
8. 舊引擎（`dev vendor_kit -i`）讀新檔：寫入前拒絕 3 + 6-19；不重產 tracked 薄殼。<sub>[grilling Q19、Q23]</sub>
9. 只改第一行後 `CI=true` sync（模擬 Renovate；驗 CI 真值規則）→ 1 列薄殼不符、零 tracked 寫入。<sub>[grilling 相容性補列；review 必修 4]</sub>
10. fresh clone 無 gen/：`just vendor_kit` 列出 **vendor_kit 命名空間**不觸網（工具命名空間在 sync 後才出現，`mod?` 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行。<sub>[interface 驗收；review I-15、I-19]</sub>
11. 使用者改薄殼／未納管檔／append 零／多命中：不覆蓋、不刪、詢問與結束碼符合契約。<sub>[grilling 相容性補列、Q13]</sub>
12. 中斷與重跑：resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗。<sub>[grilling 相容性；review 必修 9]</sub>
13. 歷史啟動器 parser × 合法／異常 TOML（BOM、空白、重複 `vendor_kit` 行 → 1、schema 位置、local 覆寫、尾端註解）。<sub>[grilling 相容性；review 必修 11]</sub>
14. just 矩陣 1.33.0 + latest（latest 非 required）。<sub>[grilling Q8]</sub>
15. amd64 與 arm64 原生 runner 各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致。<sub>[#26；review 必修 16]</sub>
16. 離線包（Q26）：無法連 GHCR 的機器用 `bootstrap.sh --local <tar>`（旁檔 `.digest`）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 `local_image_id`；旁檔缺 → 1；amd64／arm64 各一次。<sub>[#27；grilling Q26]</sub>
17. 離線可用（Q22／Q26）：本機已有 image 後斷網 → `just <ns> build`（自動 sync 快路徑）與 `just vendor_kit sync` 必須成功且不起 pull；斷網 + 無 image → 1 + 6-31 於 `--timeout 5` 內結束、不 hang。<sub>[grilling Q22、Q26]</sub>
18. 私有工具：`add <repo>@<tag>` 可拉；`add <repo>` 無 token → 1 + 6-3；`update` 無 token → 1 + 6-3 逐字；錯 token → 1；對 token → 列出；`TOKEN_FILE`（驗 `-v` 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／執行紀錄／進度檔 grep 不到 token；`registry_query` 的 URL 無 userinfo。<sub>[#28；review 必修 5；v2.12 L6]</sub>
19. append：LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 `.dockerignore` 四行 append → uninstall 逐行刪（故意改掉其中一行 → 該行跳過並 warn、其餘刪）。<sub>[#29；grilling Q22 補；v2.9-5；v2.12 L1]</sub>
20. 空白路徑：專案根含空白與 `$`、`dev -p "含 空白/路徑"`；vk-resolve `mount` 八進位跳脫往返；`just vendor_kit add --help` 到引擎。<sub>[grilling 19條-8、Q24]</sub>
21. git worktree（`.git` 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）。<sub>[grilling 19條-1、-10]</sub>
22. rootless docker（setup-docker-action `rootless: true`：不加 `-u`、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：`--userns=keep-id`）各跑完整流程；uid 12345 無 passwd 項。<sub>[grilling 12 修正；review 必修 6]</sub>
23. prune：完整流程前後 `docker network ls`／`volume ls` 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊下游 image 刪、version.toml 引用的與 local 覆寫 tag 保留；`--dry-run` 零刪除；未恢復的 `.tmp.*` 不刪。<sub>[grilling 9 修正、9 補充]</sub>
24. 多工具彙總（Q27）：兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1。<sub>[grilling Q27]</sub>
25. F1 fixture（just 1.33.0）：cache 缺檔時 `just vendor_kit sync` 可進入（`mod?`）；`just <ns> build` 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 `_sync` 的模組。<sub>[review 五]</sub>
26. 無 tty／EOF：CI 無 `-y` 需詢問 → 1 + 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑。<sub>[grilling 19條-6；§0]</sub>
27. Renovate：實際 repo 驗證人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中。<sub>[remaining Q5；review I-46]</sub>
28. 驗收動詞集合由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅。<sub>[base_pitfalls 2-18、1-10]</sub>
29. 執行紀錄：每個驗收情境結束後，`.vendor_kit/log/<verb>/` 下**每個 log 檔逐行 `json.loads`** 必須通過；每檔首筆 `launcher_start`、末筆 `launcher_exit`；同一檔 `trace_id` 單一值且 = 同次進度檔 `<id>`；`event_name` 全在註冊表內（CI 另靜態擋原始碼中未註冊者）；每個 6-xx 訊息同句出現在 `body` 且 `message_id` 相符；sync 快路徑亦有檔；`upgrade` 自身升級接手後兩個引擎寫同一檔。<sub>[v2.12 L2、L5、L6]</sub>
30. 啟動器 argv 跳脫（bats）：餵 `"`、`\`、換行、`[`、`]`、非 ASCII、`-n foo`、空字串、以 `\` 結尾的 argv → `launcher_start.attributes.argv` 經 `json.loads` 還原後逐項相等；dash 與 busybox sh 各跑一次。<sub>[v2.12 L5；agy_summary2 修正版實測]</sub>
31. config.toml：`keep`／`days` 各為 `0`、負數、非數字、非整數、重複、缺鍵、缺檔 → 退回預設 50／30，除缺鍵／缺檔外印警告（stderr 與 `config_read` 同句）；放 51 檔或檔名時間戳 31 天前的檔 → 任一動詞結束後被 prune，本次的檔與 `.gitignore` 不刪；`upgrade vendor_kit` 對下游使用者改過的 config.toml 走三方合併並詢問。<sub>[v2.12 L3、L3′]</sub>
32. 磁碟不可寫（`.vendor_kit/log/` 唯讀、或磁碟滿）：每個動詞（含 help、prune、sync 快路徑、`--dry-run`）→ 1 + 6-38、**零寫入**（version.toml、cache/、gen/、進度檔、`.tmp.dist.*` 皆不動、不起容器）；引擎 append 失敗（只給引擎唯讀）→ 1 + 6-38、resolve 未執行。<sub>[v2.12 L4]</sub>
33. bootstrap.sh 逐 `-t`：三個 `-t`，第二個故意失敗（不存在的 repo）→ 第一個 add 完成且保留、第三個未執行、整體 1 並列出已完成／未處理。<sub>[r9]</sub>
34. E(c) 分支：`upgrade vendor_kit@<tag>`（tag ≠ 現 ref、同介面版／檔案版）→ 不查 registry、建 `.tmp.upgrade.<id>.toml`、改第一行、接手重產、日誌刪除 → 1 + 6-2；`CI=true upgrade vendor_kit`（未指定）→ 不查、薄殼相符 → 0；中途殺掉接手的新引擎 → 日誌留存，`sync` 印 6-33 結束 1、`help` 印 6-33 結束 0、重跑 `upgrade vendor_kit` 恢復。<sub>[r9；v2.10-5；v2.11-1]</sub>
35. help 遇未完成交易：留一個 `.tmp.remove.<id>.toml` → `help` 印 6-33 結束 0；`sync`／`update` 印 6-33 結束 1；三者除執行紀錄外不寫任何檔。<sub>[v2.10-6]</sub>

## 8. 相容性契約條文（13 條）

1. **公開介面集合**：`vendor_kit` 命名空間內 recipe 名與 argv（§1.1 選項表）、結束碼 0/1/2/3、薄殼→引擎 docker run 呼叫方式（子命令、mount、使用者旗標規則、`-w /repo`、`--protocol` 位置、label 鍵）、`vk-resolve/<P>` 文法、§4 各檔格式（含 `config.toml` 正規行、執行紀錄欄位表；事件集合待 codex 審後納入）、根 justfile 那一行、根 `.dockerignore` 四行、救援動詞名稱與 argv 皆列入契約；主機依賴不得新增（§3.1 白名單：docker ≥ 19.03、git、just ≥ 1.33.0、sh、grep、sed、id、mktemp、mkdir、date、rm、sleep、od、tr）。<sub>[compat 條 1；grilling Q8；review 必修 12；v2.12 L5；v2.13 P7]</sub>
2. **介面版 P**：單一整數、與 release 版號分開；薄殼每次呼叫附 `--protocol P`（第一版起）；引擎接受 `[floor_P, current_P]` 並以呼叫方 P 回應；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1；引擎 image LABEL `….protocol=<floor_P>-<current_P>` 讓啟動器不起容器即可判最低介面版。<sub>[grilling Q16；review B5]</sub>
3. **最低介面版**：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1）寫在契約，只能經 ADR 提高；低於最低介面版 → 3 + 6-18、零寫入；最低介面版檢查先於任何上網。<sub>[grilling Q16、Q23]</sub>
4. **永久義務**：任何 ≥ 最低介面版的舊薄殼可呼叫新引擎的救援路徑（§3.5）並得正確提示；舊資料永遠可讀、可遷（讀任一舊檔案版 → 直接寫當前檔案版，不鏈式）。<sub>[grilling Q16]</sub>
5. **非永久義務**：舊薄殼跑新 major 的一般動詞只保證乾淨回 **3** + 6-36 提示先 `upgrade vendor_kit`（零寫入）；同 major 內保留所有已承諾薄殼的一般呼叫能力。<sub>[grilling Q23；v2.4 §3]</sub>
6. **薄殼自描述**：§4.5 首行；未被改過以重算 hash + image 內模板（含歷史版本模板）二次比對判定，不依賴 gen/；不符 → 1 + 6-28 列差異不動。<sub>[grilling Q17；review I-16]</sub>
7. **檔案 schema**：每檔 `schema = N` + `written_by`（純資訊）；讀取門檻只看 schema；同檔案版只加不改；讀忽略未知欄位、寫保留（不能保留則拒絕）；檔案版高於本引擎 → 任何寫入前退出 3 + 6-19；version.toml 契約 = 唯一版本鎖定行（§4.1；禁 BOM／重複鍵／表旁路）；config.toml 同通則且 `keep`／`days` 有正規行（§4.9）。<sub>[grilling 相容性其餘採納、Q23；review 必修 8、11、C1；v2.12 L3′]</sub>
8. **新讀舊與遷移**：新引擎在記憶體轉換，只在本來要寫該檔的明確動作寫回；metadata 遷移由 `upgrade vendor_kit` 做並在 dry-run 明列；缺失且無法可靠還原的所有權資訊不得猜，停下報告。<sub>[grilling 相容性其餘採納；compat 條 6]</sub>
9. **讀先出貨、寫延後**：同 major 內 N-1 必能讀 N 寫的檔；tools.just 最後寫且與 cache 同一 apply 內原子替換；跨檔提交點與故障恢復由進度檔定義（§4.3、§4.6），所有可寫動詞不設例外（含 `upgrade vendor_kit`）。<sub>[grilling 相容性其餘採納；review I-14；v2.11-1]</sub>
10. **bootstrap.sh 與降版**：已有 version.toml → 用該行引擎跑 install，拉不到即失敗、不得退回內嵌；`upgrade vendor_kit@<舊版>` 只在目標引擎（以介面版／檔案版比）能無損讀現有檔時成功，否則改檔前拒絕 3 + 6-10；`dev vendor_kit -i <舊 image>` 禁止重產 tracked 薄殼。<sub>[grilling Q18、Q19、Q23]</sub>
11. **專案檔與失敗恢復**：§0 不變量；`-y` 不授權覆蓋、不解除 CI 模式；結束碼 3 一律零寫入；遷移與升降版先做可行性檢查，失敗不留無法辨識的混合狀態；衝突（2）與自身升級要求重跑（1）是獨立狀態；唯讀動詞不自動恢復。<sub>[compat 條 10；v2.2 C；v2.5-1；grilling Q23；review 必修 9]</sub>
12. **發行與驗收**：已釋出 GHCR image（含 index 子 digest）、Release 資產（含 tar 與 `.digest` 旁檔）、fixture 永不刪；SemVer：major = 提高最低介面版或需手動步驟；Renovate preset 建議 major 分開 PR；驗收 §7.4 條 1–13 缺任一不得出貨；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」。<sub>[grilling 相容性其餘採納、Q11、Q26；base_pitfalls 2-17]</sub>
13. **多工具原子性**：一次處理多個工具的可寫動詞（不帶 repo 的 `upgrade`、`uninstall`）先對全部工具完整預檢（dev 中、撞名、憑證、要問什麼），任一不過 → 整體不動、1 並列出原因；預檢過後的寫入階段失敗適用 Q27（做得完的做完、進度檔保留、回最需處理的碼）。<sub>[grilling 2026-09-20 補三條不變量；§1.2 upgrade／uninstall；codex 00–02 #32]</sub>

## 9. [待定] 清單與已定值

### 9.1 仍待定（3 條）

B1、F5 已依 grilling 2026-09-19 末條定案（見 §9.2）。v3 併入時發現的 P4–P13 已依 v2.13 結案（見下「已結案」；使用者可否決）。

待議（來源已明列，等時機或第三方）：
- **P1** 啟動器讀 config.toml 的方式：現為 grep 正規行（§4.9）；config 鍵變多時改由引擎產啟動器專用平面檔或其他方式；重評觸發 = 新增第二個表或啟動器要讀的鍵超過兩個。<sub>[v2.12 L3′；grilling 2026-09-20]</sub>
- **P2** 外部 repo（出處註記）反向採用 vendor_kit 的 POSIX log.sh（單一 owner）：開 issue；不影響本規格。<sub>[v2.12 L5；grilling 2026-09-20]</sub>
- **P3** L6 事件集合（§4.10 事件表）依建議先行，**待 codex 審過才最後定案**；審後只准增刪事件名與屬性，不改欄位表。<sub>[v2.12 L6]</sub>

已結案（v2.13，主對話依既定原則決定；落點）：
- **P4** bootstrap.sh 就是第一次接入的啟動器：驗 git repo／just → `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`（失敗 → 1 + 6-38）→ 才 pull／install；install 失敗清半成品但 **`.vendor_kit/log/` 保留**，訊息明說紀錄位置 → §1.2 bootstrap.sh、§2c、§4.10。
- **P5** 第一次 install 也建 `.tmp.install.<id>.toml`（統一規則、無例外），兼「不留半成品」的清除清單，成功後刪 → §0、§1.2 install、§2c、§4.6。
- **P6** uninstall：config.toml 比照初始檔保護模式（hash == 基準版副本 → 刪；被改 → 留並列出）；`log/` 一律保留、不 rmdir、`.vendor_kit/` 只剩 `log/`，訊息說明 → §1.2 uninstall、§2c。
- **P7** 白名單加 `mkdir`、`date`（連同 `od`、`tr`）；啟動器 timestamp 試 `%N`、busybox 退回秒級；引擎一律微秒 → §3.1、§4.10 欄位表。
- **P8** `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>`，與 `TRACEPARENT` 並用 → §3.1 docker run 參數與 `-e` 白名單、§3.2、§5。
- **P9** 真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌啟動器事件白名單，release CI 驗內嵌 ⊆ 真本；未註冊 → FATAL 1；薄殼四檔改五檔（`log.sh` 由引擎重產、帶自描述首行）→ §0、§4.5、§4.10。
- **P10** 基準版副本 `baseline/vendor_kit/config.toml`，metadata 記於 `baseline/.vendor_kit.toml`（與根 `.dockerignore` 同表）；config.toml 不寫 `written_by`／`schema` 以外的機器欄位 → §4.9。
- **P11** 6-38／6-24 文案採草擬，待 codex／使用者審（不擋規格）→ §6。
- **P12** 「零寫入」= 不寫任何專案檔，執行紀錄例外 → §0、§4.10。
- **P13** 根 `.dockerignore` 四行（加 `.vendor_kit/log/`），與 Q22 cache 同理 → §4.10（各節已為四行）。
- 低風險推論照子代理所寫：`upgrade vendor_kit` 對 config.toml 走狀態機＋6-22；grep 命中 0 → 預設不警告、重複／非正整數 → 預設＋警告；log prune 不刪本次檔與 `.gitignore`；啟動器一律自產 `TRACEPARENT`。

### 9.2 已定值（本次填入；來源）

| 編號 | 值 | 來源 |
|---|---|---|
| A1 | `prune [-y] [--dry-run]`；兩段：`resolve prune` 出 `keep`（version.toml + 本機覆寫實際引用的 image：引擎 tag／ID 覆寫有、工具 `path:<dir>` 無），啟動器執行 docker ls／rm（不掛 socket）；image 只刪帶 label 且本專案未引用者；未恢復 `.tmp.*` 不刪；問句 6-32 | grilling Q24（prune 由啟動器執行）、9 修正／補充；review A1 |
| B1 | `--local` 值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則含 `/` 且存在同名檔 → 1 + 6-37 消歧；否則 → image tag；不加前綴語法 | grilling 2026-09-19 末條；v2.7-2；grilling 三審新定案 2026-09-20（codex r3 R6） |
| F5 | `sync`（無參數，含工具 `_sync` 自動呼叫）= Q22 快路徑；`sync --verify`（長形）或 CI 為真 = 每檔 sha256 全驗 | grilling 2026-09-19 末條；v2.7-2 |
| B2 | 轉發 `CI`、`VENDOR_KIT_NO_LOCK`、registry 三變數（resolve 階段；TOKEN_FILE 改 `-v`）；`PULL_TIMEOUT` 啟動器自讀；其餘不轉發 | review 必修 5、B2 |
| B3 | `VENDOR_KIT_PULL_TIMEOUT`／`--timeout`，預設 300，只收正整數 | grilling Q24、Q25；review B3 |
| B4 | vk-resolve/1：`\|` 分隔、八進位跳脫、kind 八種、`end\|<N>`、先收完再驗、整份掛 apply、引擎已變由 grep 第一行判 | grilling Q24；review 三 |
| B5 | 前綴 `io.github.<org>.vendor_kit`；容器等 `=1` + `.project`；引擎 image `=1`／`.protocol`／`.schema`；下游 image `=1`（Dockerfile.dist 必含） | grilling Q24、16 條；review B5、必修 14 |
| B6 | 專案內 `.vendor_kit/.tmp.dist.<id>/`（mktemp）+ trap | grilling Q24；review B6 |
| B7 | `-w /repo`；`--protocol P` 在子命令前 | review B7；grilling 16 條 |
| C1 | `written_by`（純資訊）；讀取門檻只看 `schema`；無 `min_reader` | grilling 16 條；review C1 |
| C2 | `vendor_kit_image_id` | review C2 |
| C3 | version.local.toml 與 version.toml 同形；工具在 `[tools]`；含 schema／written_by；undev vendor_kit 一併撤 ID | review C3 |
| C4 | metadata：`source`、`local_image_id`、`complete`、`conflicts`、`[[file]] dest/state/declined_hash/lines`、`[progress]`；state 單一列舉五值 | grilling Q24、16 條、Q26；review C4 |
| C5 | `.tmp.<verb>.<id>.toml`（交易 id，不用 repo） | grilling Q24；review C5 |
| C6 | 頂層 `description` 單行；`src` 相對 `dist/` | review C6 |
| D1 | 6-1 sync 用「請執行：just vendor_kit upgrade vendor_kit」；6-2 重產完成；6-2b 第一行已改但未重產；Q9 舊句不用 | review D1 |
| D2 | 6-16／17／18／19／23／28／29 採 codex 模板，6-19 改印「schema N 高於本引擎支援的 M」並回 3 | review D2、必修 8；grilling Q23 |
| E1 | check.sh = 第一個失敗步驟的碼；`export CI=1`；local 被 track → 1 | review E1、必修 4 |
| E2 | 根目錄 `default.json`；自身 `renovate.json`；extends 無路徑 | grilling Q24；review 必修 13 |
| F1 | `mod?` + 工具模組私有 `_sync`（逐字本體）+ 公開 recipe 相依 + --dist lint + vendor_kit 自身動詞不前置；「sync 豁免 6-9」已於 v3.2 撤回（`_sync` 先 cd 到專案根即可）；1.33 fixture 驗證 | grilling 16 條；review 五；01 頁拍板 2026-09-20 |
| F2 | undev vendor_kit 後只提示 6-1 不重寫 | grilling Q10；review F2 |
| F3 | submodule：契約先寫「已初始化且有工作樹的 submodule 可作專案根」，以 §7.4-21 實測通過為生效條件（非決策題） | review F3 |
| F4 | `just --dump --dump-format json` 取根檔既有 recipe／module／alias 名（不用 `--summary`） | review F4；v2.5-5 |
| G1 | `add --local` 只收存在的 `.tar`；tag 形只有 bootstrap.sh；不提供 `--digest` | v2.10-3；v2.11-2；grilling 2026-09-20 |
| G2 | `upgrade vendor_kit` 一律建 `.tmp.upgrade.<id>.toml`（撤回 v2.10-4） | v2.11-1；grilling 2026-09-20 |
| G3 | help 遇未完成交易印 6-33 仍 0；6-2b 只適用第一行已改 | v2.10-5、-6 |
| L1 | 執行紀錄位置 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`、一次一檔、無 latest symlink、目錄內 `.gitignore` | v2.12 L1 |
| L2 | JSONL；`timestamp`／`severity_text`／`event_name`／`body`／`trace_id`／`attributes{component, verb, …}`；tty 訊息同句進 body | v2.12 L2 |
| L3 | 每動詞目錄 30 天且 50 檔（stricter wins）；啟動器結束時 best-effort prune | v2.12 L3 |
| L3′ | `config.toml`（進 git；schema=1；`[log] keep=50 days=30`；缺 = 預設；非正整數 → 預設 + 警告；引擎 toml-bridge stage；啟動器 grep 正規行；upgrade 三方合併） | v2.12 L3′ |
| L4 | fail-closed：建檔／`launcher_start`／`engine_start` 失敗 → 1 + 6-38 零寫入；所有動詞一致；無 `--no-log` | v2.12 L4 |


=== 附件 P：本組頁面抽取文字 ===


----- 頁 v1p2 -----
# v1p2  06 契約 v2：目錄樹與檔案範例

nodes 84（不含 v2 小標）／edges 28／terms 8／xrefs 0

## nodes
- [other/TITLE] title: 契約② 專案裡的檔（1／3）── 目錄樹與檔案範例（interface_spec §4；誰寫它、誰可以改、進不進 git）
- [other/TEXT] p2_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p2_pend: 本頁無待拍板⏎檔名 version.toml 已定（§4.1：它是「該裝哪版」的宣告，不是 lock 產物）；右欄範例框逐字（等寬、保留縮排），說明一律放框外
- [other/TEXT] p2_lbl: 3. 目錄樹（專案根 = 含 .vendor_kit/ 的目錄；每格：用途｜寫：誰產生｜改：誰可改）
- [other/RECT] t_root: 專案/（下游使用者的；專案根）
- [other/RECT] t_just [v2]: justfile ── 專案檔；install 只加一行 import '.vendor_kit/entry.just'（無 → 建四行；有 → 問／-y；已含 → 不再加）⏎寫：install｜改：隨意；uninstall 問後只刪完全相同那行；add 只讀它查撞名
- [other/RECT] t_di [v2]: .dockerignore ── 下游使用者的；install 加四行 .vendor_kit/cache/、gen/、.tmp.*、log/（無 → 建；有 → 問 6-34／-y）⏎寫：install（記於 baseline/.vendor_kit.toml）｜改：下游使用者隨意；uninstall 問後只刪原文相同行
- [other/RECT] t_vk [v2]: .vendor_kit/ ── 根目錄只多這一個；薄殼 + 狀態 + 快取都在裡面；上層或下層不得再有一個（禁止巢狀）⏎寫：install、upgrade vendor_kit 重產薄殼（先比對薄殼首行）｜改：人不改；uninstall 只刪 hash 相符的自產檔
- [other/RECT] t_ver [v2]: version.toml ── 進 git：唯一來源。vendor_kit = "<ref>" 版本鎖定行（唯一）、schema、written_by、[tools] 一行一工具 tag@digest⏎寫：install／add／upgrade／remove（apply 最後才寫）｜改：下游使用者可手改、Renovate PR 改；sync 只讀
- [file/FILEBOX] t_vl [v2]: version.local.toml ── 不進 git（自有 .gitignore 擋）；與 version.toml 同形：工具的本機覆寫 path:<dir>、引擎的本機覆寫 tag + vendor_kit_image_id⏎寫：dev／undev（含 image ID）；bootstrap --local 在 install 成功後才寫｜改：不建議手改
- [file/FILEBOX] t_vl2 [v2]: （規則）CI 模式下有任何本機覆寫 → sync 回 1；uninstall 直接刪（VK 自有檔，不比 hash）；undev 撤掉最後一個覆寫時刪整個檔
- [other/RECT] t_cfg [v2]: config.toml ── 進 git：schema = 1、[log] keep = 50、days = 30（含註解與預設值；缺檔或缺鍵 = 預設；非正整數 → 預設 + 警告）⏎寫：install 建；upgrade 當初始檔三方合併｜改：下游使用者隨意；引擎用 TOML parser 讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$
- [other/RECT] t_gi [v2]: .gitignore ── 進 git，我們自己的：cache/ gen/ log/ version.local.toml .tmp.*；第一行自描述⏎寫：install／upgrade vendor_kit 重產｜改：人不改
- [other/RECT] t_entry [v2]: entry.just ── 進 git：mod vendor_kit 'vendor.just' + import? 'gen/tools.just'（零 set 零 recipe）；第一行自描述⏎寫：引擎 shell 模組（install／upgrade vendor_kit）｜改：人不改
- [other/RECT] t_vj [v2]: vendor.just ── 進 git：動詞 recipe 一行轉發＋啟動器本體（POSIX sh；set positional-arguments 只放這；附 --protocol P）；第一行自描述⏎寫：引擎 shell 模組｜改：人不改
- [other/RECT] t_logsh [v2]: log.sh ── 進 git：啟動器 log 函式（POSIX；內嵌啟動器事件白名單）；第一行自描述（同其他薄殼檔）⏎寫：引擎 shell 模組｜改：人不改
- [other/RECT] t_ci [v2]: ci/check.sh ── 進 git：下游 CI 呼叫的契約檢查（⓪–⑤ 六步，契約⑤ p3c）；第一行 shebang、第二行自描述、之後 export CI=1⏎寫：引擎 shell 模組｜改：人不改
- [other/RECT] t_bl [v2]: baseline/ ── 進 git：install 建 .gitkeep（VK 自產空檔；uninstall 刪）、vendor_kit/config.toml 副本、.vendor_kit.toml（根 .dockerignore 的 append 記錄 + config.toml 的 metadata）；<repo>/ = 基準版（上次套用的初始檔原版副本）⏎寫：install；add 建 <repo>/、upgrade 推進（衝突仍推；解析失敗的檔不推）｜改：人不改
- [other/RECT] t_blcfg [v2]: vendor_kit/config.toml ── 進 git：config.toml 的基準版副本（三方合併的 B；uninstall 比 hash）⏎寫：install 建、upgrade vendor_kit 推進｜改：人不改
- [other/RECT] t_meta [v2]: <repo>/.vendor_kit.toml ── 進 git：metadata（欄位見 p2b）；兼作該目錄佔位⏎寫：add／upgrade（install 不建）｜改：人不改
- [file/FILEBOX] t_gen [v2]: gen/ ── 不進 git：引擎產生的三種檔（下列三格），各自由不同動詞寫⏎寫：引擎｜改：人不改（會被覆蓋）
- [file/FILEBOX] t_tools [v2]: tools.just ── 每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（上方一行 # <description>；零 set 零 recipe）⏎寫：sync／add／remove／upgrade 重生（最後寫、與 cache 同一 apply 內原子替換）｜改：人不改
- [file/FILEBOX] t_gstamp [v2]: .stamp ── 只記引擎 ref（一行；本機覆寫時為 <tag>；不承擔薄殼 hash）；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1（不重寫）⏎寫：只由 install／upgrade vendor_kit｜改：人不改
- [file/FILEBOX] t_rstamp [v2]: <repo>.stamp ── 每工具一個印記：第一行 index digest（dev 時 path:<dir>），之後每檔 sha256；sync 用它決定要不要 fetch⏎寫：引擎 fetch｜改：不可改
- [file/FILEBOX] t_log [v2]: log/ ── 不進 git（自帶 .gitignore）：執行紀錄，每動詞一個子目錄，各留最近 30 天且 ≤ 50 檔（config.toml [log]）⏎寫：啟動器建檔並先寫 launcher_started（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔；結束 log_prune、launcher_completed|failed｜改：人不改
- [file/FILEBOX] t_logf [v2]: <verb>/<UTC ts>-<id8>.jsonl ── 一次執行一檔、JSON Lines（timestamp／severity_text／event_name／body／trace_id／attributes）；<id8> = trace_id 前 8 碼；憑證永不記⏎寫：啟動器 launcher_*、引擎 engine_* 事件｜改：人不改
- [file/FILEBOX] t_repo [v2]: cache/<repo>/ ── 不進 git、下游使用者不可改；只放從暫存 /dist 展開的內容（dev 時是 symlink → <dir>/dist）⏎寫：引擎 fetch（apply 決定套用之後）｜改：不可改（verify 失敗 → 重裝並 warn）
- [file/FILEBOX] t_files: files/ … ── 工具檔案（dist/files/ 全部；無 symlink，展開時驗）｜寫：fetch｜改：不可改
- [file/FILEBOX] t_init [v2]: init.toml ── 初始檔清單（[[file]] src／dest／strategy = "copy"|"append"；schema；description）｜寫：fetch｜改：不可改
- [file/FILEBOX] t_rjust [v2]: just/<ns>.just ── 工具的 just 模組，每檔一個頂層命名空間（<repo>.just 必有；含私有 _sync）｜寫：fetch｜改：不可改
- [file/FILEBOX] t_tmp [v2]: .tmp.<verb>.<id>.toml ── 不進 git：進度檔（install 第一次也建、remove／uninstall／undev／prune／dev／升引擎；add／upgrade <repo> 記在 metadata）；<id> = trace_id⏎寫：第一個寫入前建、最後一步刪｜改：人不改；未完成 → 可寫動詞先恢復、sync／update 印 6-33 結束 1、help 仍 0
- [file/FILEBOX] t_tmpd [v2]: .tmp.dist.<id>/ ── 不進 git：啟動器暫存目錄（展開的 dist、vk-resolve 輸出）⏎寫：啟動器 mktemp、trap 刪｜改：人不改；失效殘留由 prune 清
- [other/RECT] t_user [v2]: 初始檔（例 Dockerfile…；路徑由 init.toml 的 dest 決定）── 專案檔；進 git；state 記在 metadata（五態）⏎寫：add 建（已存在不納管；append 問後加行）、upgrade 逐檔問後換／三方合併／建新檔｜改：下游使用者隨意；remove／uninstall 永不刪，印清單
- [other/TEXT] p2_ver_l: .vendor_kit/version.toml（進 git；schema = 1）── 啟動器只靠 grep 讀版本鎖定行
- [other/CELL] p2_ver [v2]: vendor_kit = "ghcr.io/<org>/vendor_kit:v1.0.0@sha256:<digest>"⏎schema = 1⏎written_by = "v1.0.0"⏎[tools]⏎<repo> = "ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:<digest>"
- [other/CELL] p2_ver_n: 第 1 行 = 唯一版本鎖定行：行首無空白、鍵後一空白、=、一空白、雙引號、無尾端註解、LF（regex 讀不到就是 1）⏎schema：格式版本，引擎讀、啟動器不讀；written_by：寫入引擎版本，純資訊⏎[tools]：每工具一行 tag@digest（多架構 index digest）
- [other/TEXT] p2_vl_l: .vendor_kit/version.local.toml（不進 git；與 version.toml 同形）── dev 寫、undev 刪、bootstrap --local 寫
- [other/CELL] p2_vl [v2]: vendor_kit = "vendor_kit:dev"⏎vendor_kit_image_id = "sha256:<image id>"⏎schema = 1⏎written_by = "v1.0.0"⏎[tools]⏎<repo> = "path:/home/me/<repo>"
- [other/CELL] p2_vl_n: vendor_kit：dev vendor_kit -i <tag> 寫的本機引擎 image，只能 tag（docker load 後無 RepoDigests）；同樣是版本鎖定行、無尾端註解⏎vendor_kit_image_id：啟動器每次 docker image inspect 比對、不 pull；同 tag 重 build 才會被發現；undev 一併撤⏎[tools].<repo>：dev <repo> -p <dir> 寫 path:<dir>；cache/<repo>/ 變 symlink → <dir>/dist；啟動器掛 -v <dir>/dist:/dist/<repo>:ro
- [other/TEXT] p2_jf_l: 根 justfile（下游使用者的；install 新建時逐字四行；已有時只加第一行）
- [other/CELL] p2_jf [v2]: import '.vendor_kit/entry.just'⏎default:⏎	@just --list
- [other/CELL] p2_jf_n: 第 4 行行首是真 tab（recipe 本體必須縮排；default: @just --list 寫成單行是 just 語法錯誤，所以拆兩行）⏎已有 justfile → 問 6-20 只加第 1 行；uninstall 只刪完全相同的那行
- [other/TEXT] p2_di_l: 根 .dockerignore（下游使用者的；install append 四行；uninstall 問後只刪原文相同行）
- [other/CELL] p2_di [v2]: .vendor_kit/cache/⏎.vendor_kit/gen/⏎.vendor_kit/.tmp.*⏎.vendor_kit/log/
- [other/CELL] p2_di_n: 無 → 建；有 → 問 6-34 後 append（-y 免問）；插入的行記於 baseline/.vendor_kit.toml⏎工具以專案根當 build context 時靠它排除 cache
- [other/TEXT] p2_tj_l: .vendor_kit/gen/tools.just（不進 git；每個 <ns>.just 一行 mod?；零 set 零 recipe）
- [other/CELL] p2_tj [v2]: # <description>⏎mod? <ns> '../cache/<repo>/just/<ns>.just'
- [other/CELL] p2_tj_n: # <description>：來自 init.toml 頂層 description；缺則 <repo> <tag>⏎mod?：cache 缺檔時其他 recipe 與 just vendor_kit sync 仍可跑
- [other/TEXT] p2_sh_l: 薄殼自描述首行（entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行）
- [other/CELL] p2_sh [v2]: # vendor_kit-shell/1 engine=v1.0.0 sha256=<hash>
- [other/CELL] p2_sh_n: <P> = 介面版（1）、engine = 產生它的引擎；<hash> = 其餘內容 CRLF→LF 正規化後的 sha256⏎引擎重算 hash + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動
- [other/TEXT] p2_st_l: .vendor_kit/gen/<repo>.stamp（每工具印記；fetch 寫）
- [other/CELL] p2_st [v2]: sha256:<hex64>⏎<sha256>  files/…⏎<sha256>  init.toml⏎<sha256>  just/<ns>.just
- [other/CELL] p2_st_n: 第 1 行：多架構 index digest（add --local 亦為正式 digest）；dev 時 path:<dir>；無 image:<tag> 形⏎之後每檔一行 <sha256>  <相對路徑>；verify 逐檔比；檔內沒有註解
- [other/TEXT] p2_gs_l: .vendor_kit/gen/.stamp（只由 install／upgrade vendor_kit 寫）
- [other/CELL] p2_gs [v2]: ghcr.io/<org>/vendor_kit:v1.0.0@sha256:<digest>
- [other/CELL] p2_gs_n: 唯一一行：產生薄殼的引擎 ref（本機覆寫時為 <tag>）；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1
- [other/TEXT] p2_tv_l: .vendor_kit/.tmp.<verb>.<id>.toml（進度檔；<verb> = 可寫動詞名（add／upgrade <repo> 除外）；<id> = trace_id）
- [other/CELL] p2_tv [v2]: schema = 1⏎written_by = "v1.0.0"⏎verb = "remove"⏎id = "<id>"⏎targets = ["<repo>"]⏎started = "<UTC ISO 8601>"⏎done = [...]⏎pending = [...]⏎consents = [...]
- [other/CELL] p2_tv_n: consents = 已取得的同意；done／pending = 已完成／未完成步驟⏎第一個寫入前建、成功結束時整個檔刪除；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33
- [other/TEXT] p2_th: 本頁名詞
- [term/TERM_K] p2_tk0: vendor_kit = 版本鎖定行
- [term/TERM_V] p2_tv0: version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = "<ref>"（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路
- [term/TERM_K] p2_tk1: config.toml
- [term/TERM_V] p2_tv1: .vendor_kit/config.toml（進 git；install 建、upgrade 三方合併）：schema = 1、[log] keep = 50、days = 30；缺檔或缺鍵 = 預設，非正整數 → 預設 + 警告；引擎用 TOML parser（toml-bridge stage）讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$
- [term/TERM_K] p2_tk2: mod／mod?／import／import?
- [term/TERM_V] p2_tv2: just 的載入：mod <ns> '檔' 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import '檔' 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）
- [term/TERM_K] p2_tk3: trace_id／TRACEPARENT
- [term/TERM_V] p2_tv3: 啟動器每次執行產一個 32 hex id（/proc/sys/kernel/random/uuid 去 -，缺則 od /dev/urandom），同值 = 進度檔交易 id；以 -e TRACEPARENT 與 -e VENDOR_KIT_LOG_FILE 傳給引擎，引擎 append 同一個 log 檔
- [term/TERM_K] p2_tk4: 初始檔五態（state）
- [term/TERM_V] p2_tv4: metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（下游使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈
- [term/TERM_K] p2_tk5: 暫存 .tmp.dist.<id>/
- [term/TERM_V] p2_tv5: 啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋
- [term/TERM_K] p2_tk6: baseline/.gitkeep
- [term/TERM_V] p2_tv6: VK 自產的進 git 空檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；install 建、uninstall 刪、hash 固定為空檔（§4.0；v2.15-14）；工具的 metadata 由 add 才建（baseline/<repo>/.vendor_kit.toml 兼作該工具目錄的佔位）
- [term/TERM_K] p2_tk7: gen/.stamp
- [term/TERM_V] p2_tv7: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [other/LEGEND] p2_lg0 [legend]: 綠框：進 git
- [other/LEGEND] p2_lg1 [legend]: 灰虛線：不進 git（可重建）
- [other/LEGEND] p2_lg2 [legend]: 黃底綠框：專案檔（進 git）
- [other/LEGEND] p2_lg3 [legend]: 等寬字：檔案內容範例
- [other/LEGEND] p2_lg4 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p2_lg5 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/LEGEND] p2_lgt [legend]: 樹線 = 目錄包含；範例框右邊 = 框外說明⏎綠標籤 = v2 改；schema 表 p2b、矩陣 p2c

## edges
- te1: t_root(專案/（下游使用者的；專案根）) --(無標籤)--> t_just(justfile ── 專案檔；install 只加一行 i…)
- te21: t_root(專案/（下游使用者的；專案根）) --(無標籤)--> t_di(.dockerignore ── 下游使用者的；instal…)
- te2: t_root(專案/（下游使用者的；專案根）) --(無標籤)--> t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …)
- te3: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_ver(version.toml ── 進 git：唯一來源。ven…)
- te4: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_vl(version.local.toml ── 不進 git（自…)
- te5: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_gi(.gitignore ── 進 git，我們自己的：cach…)
- te6: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_entry(entry.just ── 進 git：mod vendor…)
- te7: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_vj(vendor.just ── 進 git：動詞 recipe…)
- te8: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_ci(ci/check.sh ── 進 git：下游 CI 呼叫的…)
- te26: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_logsh(log.sh ── 進 git：啟動器 log 函式（POS…)
- te9: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_bl(baseline/ ── 進 git：install 建 .…)
- te27: t_bl(baseline/ ── 進 git：install 建 .…) --(無標籤)--> t_blcfg(vendor_kit/config.toml ── 進 gi…)
- te10: t_bl(baseline/ ── 進 git：install 建 .…) --(無標籤)--> t_meta(<repo>/.vendor_kit.toml ── 進 g…)
- te11: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_gen(gen/ ── 不進 git：引擎產生的三種檔（下列三格），…)
- te12: t_gen(gen/ ── 不進 git：引擎產生的三種檔（下列三格），…) --(無標籤)--> t_tools(tools.just ── 每個 <ns>.just 一行 …)
- te13: t_gen(gen/ ── 不進 git：引擎產生的三種檔（下列三格），…) --(無標籤)--> t_gstamp(.stamp ── 只記引擎 ref（一行；本機覆寫時為 <…)
- te15: t_gen(gen/ ── 不進 git：引擎產生的三種檔（下列三格），…) --(無標籤)--> t_rstamp(<repo>.stamp ── 每工具一個印記：第一行 in…)
- te14: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_repo(cache/<repo>/ ── 不進 git、下游使用者不…)
- te16: t_repo(cache/<repo>/ ── 不進 git、下游使用者不…) --(無標籤)--> t_files(files/ … ── 工具檔案（dist/files/ 全…)
- te17: t_repo(cache/<repo>/ ── 不進 git、下游使用者不…) --(無標籤)--> t_init(init.toml ── 初始檔清單（[[file]] sr…)
- te18: t_repo(cache/<repo>/ ── 不進 git、下游使用者不…) --(無標籤)--> t_rjust(just/<ns>.just ── 工具的 just 模組，…)
- te20: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_tmp(.tmp.<verb>.<id>.toml ── 不進 gi…)
- te22: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_tmpd(.tmp.dist.<id>/ ── 不進 git：啟動器暫…)
- te19: t_root(專案/（下游使用者的；專案根）) --(無標籤)--> t_user(初始檔（例 Dockerfile…；路徑由 init.tom…)
- te28: t_vl(version.local.toml ── 不進 git（自…) --(無標籤)--> t_vl2(（規則）CI 模式下有任何本機覆寫 → sync 回 1；u…)
- te23: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_cfg(config.toml ── 進 git：schema = …)
- te24: t_vk(.vendor_kit/ ── 根目錄只多這一個；薄殼 + …) --(無標籤)--> t_log(log/ ── 不進 git（自帶 .gitignore）：…)
- te25: t_log(log/ ── 不進 git（自帶 .gitignore）：…) --(無標籤)--> t_logf(<verb>/<UTC ts>-<id8>.jsonl ──…)

## terms
- vendor_kit = 版本鎖定行: version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = "<ref>"（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路
- config.toml: .vendor_kit/config.toml（進 git；install 建、upgrade 三方合併）：schema = 1、[log] keep = 50、days = 30；缺檔或缺鍵 = 預設，非正整數 → 預設 + 警告；引擎用 TOML parser（toml-bridge stage）讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$
- mod／mod?／import／import?: just 的載入：mod <ns> '檔' 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import '檔' 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）
- trace_id／TRACEPARENT: 啟動器每次執行產一個 32 hex id（/proc/sys/kernel/random/uuid 去 -，缺則 od /dev/urandom），同值 = 進度檔交易 id；以 -e TRACEPARENT 與 -e VENDOR_KIT_LOG_FILE 傳給引擎，引擎 append 同一個 log 檔
- 初始檔五態（state）: metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（下游使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈
- 暫存 .tmp.dist.<id>/: 啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋
- baseline/.gitkeep: VK 自產的進 git 空檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；install 建、uninstall 刪、hash 固定為空檔（§4.0；v2.15-14）；工具的 metadata 由 add 才建（baseline/<repo>/.vendor_kit.toml 兼作該工具目錄的佔位）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行

## xrefs

## fills（非圖例）: #FFF4C3 #ffffff
## legend_fills: #FFF4C3 #ffffff none


----- 頁 v1p3 -----
# v1p3  09 契約 v2：下游 repo 契約③

nodes 93（不含 v2 小標）／edges 0／terms 16／xrefs 0

## nodes
- [other/TITLE] title: 契約③ 下游 repo 要交的（供應側；interface_spec §4.7、§4.8、§3.6；改了要升 major 並公告）
- [other/TEXT] p3_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p3_pend: 本頁無待拍板⏎dist/files/ 的 symlink 已定禁止；dist 文字檔一律 LF、check.sh --dist 擋 CRLF 已定於 issue #29；Dockerfile.dist 必含 LABEL（16 條必修）
- [other/BAND] p3L4: 契約③ 下游 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）
- [other/CELL] p3_dist: <repo>/                  # 下游 repo⏎├─ dist/⏎│  ├─ files/…            # 全部出貨（原樣展開）⏎│  ├─ init.toml          # 初始檔清單（下表）⏎│  └─ just/<ns>.just     # 一檔一命名空間（含 _sync）⏎└─ Dockerfile.dist       # 逐字三行（下框）
- [other/TEXT] p3_dock_l: Dockerfile.dist（逐字三行；純資料 image）
- [other/CELL] p3_dock: FROM scratch⏎LABEL io.github.<org>.vendor_kit=1⏎COPY dist/ /dist/
- [step/W12] d4_1 [v2]: dist/files/⏎全部出貨；fetch 原樣展開到 .vendor_kit/cache/<repo>/files/（引擎展開時也驗右欄 CI 的檔案規則）
- [step/W12] d4_2 [v2]: dist/init.toml⏎schema、description（單行）、[[file]] src／dest／strategy="copy"|"append"（預設 copy），dest 相對專案根；用 copy 指向根 .gitignore／.dockerignore／.editorconfig → --dist 報錯（要用 append）；欄位表見下
- [step/W12] d4_3 [v2]: dist/just/<ns>.just⏎每檔一個頂層命名空間，數量工具自決，<repo>.just 必須存在；每檔含私有 _sync（F1，見下）；撞名 → add 拒絕；recipe 用 cd {{quote(justfile_directory())}} 回專案根（禁止相對 working-directory）
- [step/W12] d4_4 [v2]: Dockerfile.dist⏎逐字三行：FROM scratch／LABEL io.github.<org>.vendor_kit=1／COPY dist/ /dist/；純資料，不承諾可執行、vendor_kit 不檢查 binary（Q21：只搬移）；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加，pull 無法追加）
- [other/IMG] d4_5 [v2]: 下游 image⏎ghcr.io/<org>/<repo>-dist:<tag>⏎多架構 amd64 + arm64（同一次 buildx、COPY-only；CI 驗兩平台位元組一致）；version.toml 與印記記 index digest（#26）；公開／私有自決（公開不可逆）；已釋出 image／index 子 digest 永不刪；LABEL …vendor_kit=1
- [other/IMG] d4_6 [v2]: 引擎 image⏎ghcr.io/<org>/vendor_kit:vN⏎公開；多架構（只驗兩平台 LABEL 一致）；LABEL …vendor_kit=1、.protocol=<floor_P>-<current_P>、.schema=<N>（啟動器不起容器即可判最低介面版）；每平台 docker save tar + .digest 旁檔；Release 資產永不刪
- [step/W12] d4_7 [v2]: 下游 repo 的 CI⏎跑 vendor_kit 出貨的 check.sh --dist：dist 佈局、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、files/ 禁 symlink／hardlink／特殊檔、文字檔一律 LF [#29]、just 1.33.0 解析每個 <ns>.just、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台一致
- [step/W12] d4_8 [v2]: deploy（一句話契約）⏎工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml、GHCR（需要的檔打包時複製進去）；vendor_kit 不檢查；保證方式 = 下游 repo 自己在乾淨機器解包驗收；version.toml 公開格式可供來源紀錄
- [rule/RULE] p3_dest [v2]: dest 規則（引擎在任何寫入前驗，不只供應端 lint）：src 相對 dist/、正規化、不得越出 dist/；dest 相對專案根、正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；兩工具同 dest：copy/copy、copy/append → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查（含新版新增 <ns>／dest 的全域撞名）
- [other/TEXT] p3_init_l: dist/init.toml（逐字範例；欄位說明在下表）
- [other/TEXT] p3_sync_l: dist/just/<ns>.just 的 _sync（逐字，行首真 tab）與 label 表
- [other/CELL] p3_init: schema = 1⏎description = "<repo> 的專案範本與 just recipe"⏎[[file]]⏎src = "files/Dockerfile"⏎dest = "Dockerfile"⏎[[file]]⏎src = "files/gitignore.snippet"⏎dest = ".gitignore"⏎strategy = "append"
- [other/CELL] p3_sync: [private]⏎_sync:⏎	cd {{quote(justfile_directory())}} && just vendor_kit sync⏎build: _sync⏎	cd {{quote(justfile_directory())}} && …
- [header/HDR] p3_initf_h0: 欄位
- [header/HDR] p3_initf_h1: 型別／必填
- [header/HDR] p3_initf_h2: 說明
- [other/CELL] p3_initf_r0c0: schema
- [other/CELL] p3_initf_r0c1: integer／是
- [other/CELL] p3_initf_r0c2: 建置期契約（同 image 內讀寫），不進執行期矩陣
- [other/CELL] p3_initf_r1c0 [v2]: description
- [other/CELL] p3_initf_r1c1: string／否
- [other/CELL] p3_initf_r1c2: 頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod? 上方 # <description>；缺則 <repo> <tag>
- [other/CELL] p3_initf_r2c0: [[file]].src
- [other/CELL] p3_initf_r2c1: string／是
- [other/CELL] p3_initf_r2c2: 相對 dist/；正規化、不得越出 dist/
- [other/CELL] p3_initf_r3c0: [[file]].dest
- [other/CELL] p3_initf_r3c1: string／是
- [other/CELL] p3_initf_r3c2: 相對專案根；正規化、不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；跨工具撞 dest 規則見左
- [other/CELL] p3_initf_r4c0 [v2]: [[file]].strategy
- [other/CELL] p3_initf_r4c1: string／否
- [other/CELL] p3_initf_r4c2: "copy"（預設）或 "append"，只有這兩值；根 .gitignore／.dockerignore／.editorconfig 類必須用 append
- [header/HDR] p3_lbl_h0: 資源
- [header/HDR] p3_lbl_h1: label（鍵前綴 io.github.<org>.vendor_kit）
- [other/CELL] p3_lbl_r0c0 [v2]: 啟動器建的容器／network／volume
- [other/CELL] p3_lbl_r0c1: …=1、….project=<專案根絕對路徑>（專案路徑 label 不加在 image 上）
- [other/CELL] p3_lbl_r1c0 [v2]: 引擎 image（build 時）
- [other/CELL] p3_lbl_r1c1: …=1、….protocol=<floor_P>-<current_P>、….schema=<N>
- [other/CELL] p3_lbl_r2c0 [v2]: 下游 image（build 時）
- [other/CELL] p3_lbl_r2c1: …=1（Dockerfile.dist 必含）
- [other/CELL] p3_lbl_r3c0 [v2]: prune
- [other/CELL] p3_lbl_r3c1: 依 label 掃四類資源；image 只刪帶 label 且本專案未引用者；vendor_kit 不建 network／volume（驗收差集為空，故意留的也要能刪）
- [rule/RULE] p3_syncr [v2]: sync 自動前置：工具契約（F1 定案）：每個 dist/just/<ns>.just 必含上列私有 _sync（本體逐字、行首真 tab；justfile_directory() 在模組內 = 專案根；用 quote() 不直接插字串）；工具每個公開 recipe 相依它（例 build: _sync；例外集合：無）；vendor_kit 自身動詞不前置
- [rule/RULE] p3_syncl [v2]: sync 自動前置：lint 與限制：check.sh --dist 以 just --dump --dump-format json 檢查：_sync 存在、私有、本體逐字相符、每個公開 recipe 的 dependencies 含 _sync。限制（契約明寫）：just 在執行前已載入所有模組，同一次呼叫內看不到 sync 重建後的新 recipe；cache 缺檔時 mod? 讓 just vendor_kit sync 仍可進入；1.33.0 fixture 通過才算結案
- [rule/RULE] p3_con [v2]: 工具契約（初始檔與 recipe）：初始檔只能引用穩定入口 just <ns> …、.vendor_kit/ci/check.sh、.vendor_kit/entry.just、.vendor_kit/version.toml；不得寫死 cache 內部路徑（Q14）；rename／格式變更不得以 copy/append 假裝完成；工具的 build 若以專案根當 context，依賴 install 加進根 .dockerignore 的排除，不得再以其他方式繞過 .vendor_kit/；dist 可執行性是下游 repo 責任（check.sh --dist + 自己的測試）
- [rule/RULE] p3_off [v2]: 離線包（Release 資產；Q26）：每個平台 tar（docker save）旁附同名 .digest 旁檔：<name>.tar + <name>.tar.digest，內容一行 sha256:<hex64> = 該 image 的正式多架構 index digest；另附 local_bootstrap.sh 便利包裝（偵測架構、挑 tar、exec bootstrap.sh --local；非契約、不另定介面）；bootstrap.sh --local <tar>／add --local <tar>：docker load 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 local_image_id；旁檔缺 → 1。離線可用：啟動器先 docker image inspect，本機有就不 pull；斷網 + 已有 image → sync／build 必須成功；斷網 + 無 image → 1 印 6-31 不 hang；離線 upgrade 不支援
- [other/LEGEND] p3_lg0 [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p3_lg1 [legend]: 等寬字：檔案內容範例
- [other/LEGEND] p3_lg2 [legend]: 淺橘底：規則／摘要（已定）
- [other/LEGEND] p3_lg3 [legend]: 灰底：表頭
- [other/LEGEND] p3_lg4 [legend]: 淺灰底：分組（無狀態意義）
- [other/LEGEND] p3_lg5 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p3_lgt [legend]: 紫 = image（工具／引擎）⏎淺灰底容器 = 契約③ 全部
- [other/LEGEND] p3_lg6 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/TEXT] p3_th: 本頁名詞（只列本頁用到的）
- [term/TERM_K] p3_tk0: Dockerfile.dist
- [term/TERM_V] p3_tv0: 逐字三行：FROM scratch／LABEL io.github.<org>.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）
- [term/TERM_K] p3_tk1: label
- [term/TERM_V] p3_tv1: docker 資源上的鍵值標籤，鍵前綴 io.github.<org>.vendor_kit：容器／network／volume = 1 + .project=<專案根絕對路徑>；引擎 image = 1 + .protocol=<floor_P>-<current_P> + .schema=<N>；下游 image = 1；prune 依 label 掃
- [term/TERM_K] p3_tk2: dest
- [term/TERM_V] p3_tv2: init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗
- [term/TERM_K] p3_tk3: strategy = "append"
- [term/TERM_V] p3_tv3: init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）
- [term/TERM_K] p3_tk4: CRLF／LF
- [term/TERM_V] p3_tv4: 兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]
- [term/TERM_K] p3_tk5: _sync recipe（F1）
- [term/TERM_V] p3_tv5: 每個 dist/just/<ns>.just 必含的私有 recipe（逐字：[private] / _sync: / \tcd {{quote(justfile_directory())}} && just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查
- [term/TERM_K] p3_tk6: just 的兩個目錄函式
- [term/TERM_V] p3_tv6: justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」
- [term/TERM_K] p3_tk7: buildx
- [term/TERM_V] p3_tv7: docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index
- [term/TERM_K] p3_tk8: 多架構 index／index digest
- [term/TERM_V] p3_tv8: 同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）
- [term/TERM_K] p3_tk9: check.sh --dist
- [term/TERM_V] p3_tv9: 同一支腳本的供應端模式：在下游 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／CRLF、just 1.33.0 可解析、_sync lint、LABEL、image 可展開、兩平台一致
- [term/TERM_K] p3_tk10: .digest 旁檔
- [term/TERM_V] p3_tv10: <name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1 + 6-24 主機錯誤分類）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id
- [term/TERM_K] p3_tk11: 離線可用（Q26）
- [term/TERM_V] p3_tv11: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- [term/TERM_K] p3_tk12: deploy
- [term/TERM_V] p3_tv12: 把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄
- [term/TERM_K] p3_tk13: 命名空間
- [term/TERM_V] p3_tv13: just <ns> <recipe> 前面那個 <ns>；每個工具的 just/<ns>.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）
- [term/TERM_K] p3_tk14: SemVer
- [term/TERM_V] p3_tv14: 版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高最低介面版或需要下游使用者手動步驟；minor = 新功能（含介面版 +1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR
- [term/TERM_K] p3_tk15: local_bootstrap.sh
- [term/TERM_V] p3_tv15: 離線包內附的便利包裝（非契約、不另定介面）：偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local <tar>

## edges

## terms
- Dockerfile.dist: 逐字三行：FROM scratch／LABEL io.github.<org>.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）
- label: docker 資源上的鍵值標籤，鍵前綴 io.github.<org>.vendor_kit：容器／network／volume = 1 + .project=<專案根絕對路徑>；引擎 image = 1 + .protocol=<floor_P>-<current_P> + .schema=<N>；下游 image = 1；prune 依 label 掃
- dest: init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗
- strategy = "append": init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）
- CRLF／LF: 兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]
- _sync recipe（F1）: 每個 dist/just/<ns>.just 必含的私有 recipe（逐字：[private] / _sync: / \tcd {{quote(justfile_directory())}} && just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查
- just 的兩個目錄函式: justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」
- buildx: docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index
- 多架構 index／index digest: 同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）
- check.sh --dist: 同一支腳本的供應端模式：在下游 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／CRLF、just 1.33.0 可解析、_sync lint、LABEL、image 可展開、兩平台一致
- .digest 旁檔: <name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1 + 6-24 主機錯誤分類）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id
- 離線可用（Q26）: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- deploy: 把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄
- 命名空間: just <ns> <recipe> 前面那個 <ns>；每個工具的 just/<ns>.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）
- SemVer: 版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高最低介面版或需要下游使用者手動步驟；minor = 新功能（含介面版 +1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR
- local_bootstrap.sh: 離線包內附的便利包裝（非契約、不另定介面）：偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local <tar>

## xrefs

## fills（非圖例）: #e1d5e7 #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #e1d5e7 #e6e6e6 #f5f5f5 #ffe6cc #ffffff none


----- 頁 v1p3b -----
# v1p3b  10 契約 v2：啟動器 ↔ 引擎契約④

nodes 108（不含 v2 小標）／edges 20／terms 7／xrefs 0

## nodes
- [other/TITLE] title: 契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）
- [other/TEXT] p3b_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p3b_pend: 本頁決議狀態（v2.15 結案）⏎規則框逐條對應 interface_spec §3、§5；vk-resolve/1 文法（Q24）；執行紀錄事件依圖例約定①②（v2.15-2）
- [other/BAND] p3L2: 契約④ 啟動器 ↔ 引擎（每格一件事；⓪ 執行紀錄 → ① 啟動器 grep → ② resolve → ③ 主機 docker → ④ apply；規則框 = §3、§5 逐條；白 = 啟動器、藍 = 引擎）
- [step/W12] s0a: ⓪ 產 trace_id⏎（uuid；缺則⏎od urandom）
- [step/W12] s0b [v2]: 建執行紀錄⏎log/<verb>/⏎<ts>-<id8>.jsonl
- [step/W12] s0c [v2]: 寫 launcher_started⏎（完整 argv）失敗 →⏎1 印 6-38、零寫入
- [step/W12] s1: ① 以版本鎖定行 regex grep 引擎 ref⏎（version.local.toml 本機覆寫優先；命中 ≠ 1 → 1）⏎非 sync 的動詞跳過下一格
- [decision/D12] d1 [v2]: 只有 sync：⏎gen/.stamp⏎≠ 引擎 ref？
- [other/LEAF] g2: ② docker run 引擎 resolve <動詞>（只讀、不寫檔、無 TTY；診斷走 stderr；engine_started／completed 依圖例約定②）
- [step/SUB] s2a: 讀 version.toml／local⏎（CI 模式判定）
- [step/SUB] s2b [v2]: 只有 add／update／upgrade⏎且未指定 @<tag>：⏎查 registry 最新正式版
- [step/SUB] s2c: stdout vk-resolve/1⏎（pull／extract／mount／engine／fingerprint／apply／end）
- [end_orange/O12] p3_err: 是 → 1 印 6-1⏎（請 upgrade vendor_kit；不重寫薄殼）
- [decision/D12] d2: apply|yes？
- [other/LEAF] g3: ③ 主機 docker（每筆 pull／extract 記錄；不帶 --platform；先收完 vk-resolve 驗文法才動）
- [step/W12] s3a [v2]: docker image inspect⏎（每筆 pull／extract）
- [step/W12] s3b: 無：docker pull⏎（逾時 → 1 印 6-31）
- [step/W12] s3c [v2]: 只有 extract kind：⏎docker create（帶 label）⏎<ref> /x
- [step/W12] s3d: docker cp c:/dist/.⏎→ .tmp.dist.<id>/⏎<repo>/
- [step/W12] s3e: docker rm⏎（trap 也清）
- [step/W12] s4: ④ docker run 引擎⏎apply <動詞>（掛 /dist:ro）⏎→ 結束碼 0／1／2／3 回 just
- [end_red/R12] s3bx: 失敗 → 1 印 6-24⏎（網路／認證／不存在）
- [end_orange/O12] p3_rx: resolve 非 0 → 原碼傳出⏎（不讀 stdout、不跑 docker／apply）
- [end_ok/G12] p3_ok: 否（apply|no）→ 0 快路徑⏎不起第二個容器
- [end_ok/G12] s4x: → 終點：結束碼 0／1／2／3⏎launcher_completed|failed⏎依圖例約定①
- [rule/RULE] p3_sh [v2]: 主機命令白名單（16 條必修；lint 擋清單外）：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、mkdir、date、od、tr（v2.13 P7：建 log/、時間戳、trace_id）、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files。啟動器 = POSIX sh（vendor.just 內的 recipe 殼）：不裝 python、不解析 TOML、不 eval；路徑含空白、$、非 ASCII 一律引號
- [rule/RULE] p3_env [v2]: 執行環境（19 條）與主機需求：docker ≥ 19.03（或 Podman ≥ 4.9）、just ≥ 1.33.0、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA、引擎基底 EOL → issue v2。時間戳 UTC ISO 8601；需詢問但無 tty／EOF → 1 印 6-4；所有 docker 資源帶 vendor_kit label；不建 network／volume；離線 upgrade 不支援；worktree 進驗收；submodule 以實測為生效條件
- [rule/RULE] p3_run [v2]: docker run 參數：docker run --rm [<uid 旗標>] -v "<專案根>:/repo" -w /repo [-v "<專案根>/.vendor_kit/.tmp.dist.<id>:/dist:ro"] [-v "<dir>/dist:/dist/<repo>:ro"]… [-v "<TOKEN_FILE>:/run/vk-token:ro" -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] -e TRACEPARENT=00-<trace_id>-<span_id>-<flags>（W3C；引擎只取 trace_id）-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔> [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.<org>.vendor_kit=1 --label io.github.<org>.vendor_kit.project=<專案根絕對路徑> <引擎 ref> --protocol P <子命令> [args]。--protocol P（介面版）一律在子命令之前；-w /repo 必給；-it 只在 apply 且互動（有 tty、無 -y、非 CI 模式），resolve 永不 -t；trap … EXIT INT TERM 清容器與 .tmp.dist.<id>/
- [rule/RULE] p3_envw [v2]: 環境變數與 -e 白名單（§5）：轉發 CI（照原值；真值規則：非空且不為 0／false → CI 模式）、VENDOR_KIT_NO_LOCK（=1 跳過 flock）；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update 單段及 upgrade 的 resolve 以 -e 傳（不寫 log／檔、不傳給工具、dry-run 不印）；VENDOR_KIT_REGISTRY_TOKEN_FILE 改為 -v <主機檔>:/run/vk-token:ro 並以 -e …_TOKEN_FILE=/run/vk-token 傳容器內路徑（與 _TOKEN 同設 → 1「只能擇一」）；啟動器自讀不轉發：VENDOR_KIT_PULL_TIMEOUT（預設 300，--timeout 優先）；啟動器自產必傳（v2.12）：TRACEPARENT（32 hex trace_id，同值 = 進度檔交易 id）與 VENDOR_KIT_LOG_FILE（容器內路徑；引擎 append 同一檔，不另開檔）；其餘一律不轉發（HTTP_PROXY 等 → v2）；README 列出全部 VENDOR_KIT_* 與 CI，lint 擋未列者；引擎容器內 LC_ALL=C.UTF-8、TZ=UTC、HOME=<容器內暫存>
- [rule/RULE] p3_img [v2]: 引擎 image 取得：一律先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull <ref>（逾時）。本機覆寫時：docker image inspect <tag> 的 .Id 必須 == version.local.toml vendor_kit_image_id，否則 1；不 pull（不用 docker run 的 pull 旗標：docker 19.03 沒有）。引擎子命令：單段 install／update／dev／help／upgrade vendor_kit[@<tag>] = --protocol P <verb> [args]；resolve <verb>（只讀、不詢問、不寫檔、無 TTY）；apply <verb> [--dry-run]；內部取件／驗指紋／三方合併不對外
- [rule/RULE] p3_self [v2]: 自身升級的接手（§3.4）：「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 版本鎖定行。apply 結束後 ref 變了（且 == 計畫的 engine）→ 以新 ref（本機覆寫有 vendor_kit= 則用該 image、inspect 驗 ID）跑 docker run … <新 ref> --protocol P upgrade vendor_kit，結束碼原樣傳出（預期 1 印 6-2）；第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b，不再重跑。救援路徑（§3.5）：install、upgrade vendor_kit[@<tag>]、sync 的「薄殼不符 → 1 印 6-1」判定、help = 單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ 最低介面版的薄殼永遠可經此叫任何引擎重產薄殼
- [rule/RULE] p3_lock [v2]: apply 通則（所有動詞）：容器開始 append engine_started（失敗 → 1 印 6-38；圖例約定②）→ 讀 /dist/vk-resolve（啟動器把 resolve 原始 stdout 存成 .tmp.dist.<id>/vk-resolve 一起掛入）→ 拿 flock → 重算指紋與計畫中的 fingerprint 比對（不同 → 1 印 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 模式需改進 git 的檔 → 1 印清單）→ 建進度檔（第一個寫入前）→ 其後所有寫入（apply 引擎自己重算計畫與詢問清單，不從 stdout 拿；gen/tools.just 最後寫且與 cache 同一 apply 內原子替換；version.toml 最後）→ 最後一步刪進度檔（uninstall 在根 justfile 那行之後）；不重新選最新版；詢問後、替換前對目標檔再查一次前像；所有合併在暫存完成 → 逐檔原子替換；失敗明列已完成／未完成
- [other/TEXT] p3_vk_l: vk-resolve/1 stdout 文法（Q24；P=1）
- [other/TEXT] p3_vkt_l: kind 一覽（啟動器動作）
- [other/CELL] p3_vk: vk-resolve/<P>⏎<kind>|<f1>[|<f2>…]⏎end|<N>⏎vk-resolve/1⏎mount|<repo>|/home/me/my\0040tools⏎fingerprint|9a2f…c1⏎apply|yes⏎end|3
- [other/CELL] p3_vk2: vk-resolve/1⏎extract|<repo>|ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:bbbb…⏎fingerprint|1c0e…77⏎apply|yes⏎end|3
- [other/CELL] p3_vk_n: 左上 = 文法骨架：第一行 vk-resolve/<P>（P = 呼叫方 --protocol 的介面版）；每行一筆 <kind>|<f1>[|<f2>…]（欄位以單一 | 分隔；UTF-8；LF；無空行、無註解；禁 CR／NUL／BOM）；最後一行 end|<N>（N = 記錄行數，之後立即 EOF）。左下範例 = sync，<repo> 在本機覆寫中（mount；路徑含空白 → \0040）；右範例 = sync，<repo> 的 cache 過期（extract）。範例工具名一律 <repo>。vk-resolve/1 只傳這裡定義的東西：pull／extract 清單、apply|yes/no、指紋；計畫／詢問清單／保護清單不走 stdout（apply 引擎自己重算）
- [rule/RULE] p3_vkr [v2]: 欄位與驗證：安全字串 [A-Za-z0-9_.-]+；ref [A-Za-z0-9_.:/@-]+（引擎以 image-reference parser 驗證後才輸出）；自由文字（路徑）凡不在 [A-Za-z0-9_./:@+=,-] 的 byte 一律寫成 \0ooo（例：空白 \0040、| \0174、\ \0134），啟動器一行解碼 dir=$(printf '%b' "$f2")、不 eval、不 source；IFS='|' read -r 直接切欄。啟動器先收完整份存到 .tmp.dist.<id>/vk-resolve、驗文法才動 docker：首行 ≠ vk-resolve/<P>、缺 end、N 不符、end 後仍有資料、未知 kind、欄位數不對、fingerprint／apply 不是恰一筆、no 卻附動作記錄、安全字串含非法字元 → 1 印 6-30；引擎宣稱的介面版真不支援 → 3。resolve 結束碼非 0 → 啟動器不讀 stdout、不跑 docker／apply、原碼傳出（圖：②→③ 之間的「resolve 非 0」出口）。stderr 一律診斷；apply 的 stdout 不作為協定通道。指紋算法見名詞表
- [header/HDR] p3_vkt_h0: kind
- [header/HDR] p3_vkt_h1: 欄位
- [header/HDR] p3_vkt_h2: 筆數
- [header/HDR] p3_vkt_h3: 啟動器動作
- [other/CELL] p3_vkt_r0c0 [v2]: pull
- [other/CELL] p3_vkt_r0c1: <name>|<ref>
- [other/CELL] p3_vkt_r0c2: 0..n
- [other/CELL] p3_vkt_r0c3: docker image inspect 有則略，否則 docker pull <ref>（逾時／失敗 → 6-31／6-24）；name = vendor_kit 或 <repo>；到此為止（不 create／cp）
- [other/CELL] p3_vkt_r1c0: extract
- [other/CELL] p3_vkt_r1c1: <repo>|<ref>
- [other/CELL] p3_vkt_r1c2: 0..n
- [other/CELL] p3_vkt_r1c3: 同 pull 後 docker create <ref> /x → docker cp c:/dist/. .tmp.dist.<id>/<repo>/ → docker rm；同一 repo 不得同時有 extract 與 mount
- [other/CELL] p3_vkt_r2c0: mount
- [other/CELL] p3_vkt_r2c1: <repo>|<dir 八進位跳脫>
- [other/CELL] p3_vkt_r2c2: 0..n
- [other/CELL] p3_vkt_r2c3: 本機覆寫：解碼後驗 <dir>/dist/init.toml 存在（缺 → 1）→ -v "<dir>/dist:/dist/<repo>:ro"
- [other/CELL] p3_vkt_r3c0 [v2]: engine
- [other/CELL] p3_vkt_r3c1: <ref>
- [other/CELL] p3_vkt_r3c2: 0..1
- [other/CELL] p3_vkt_r3c3: 只在 upgrade（不帶 repo）：apply 會把版本鎖定行改成此 ref；啟動器先 pull（本機覆寫時 inspect 驗 ID）；有 engine 時不夾帶工具寫入
- [other/CELL] p3_vkt_r4c0: fingerprint
- [other/CELL] p3_vkt_r4c1: <sha256 hex64>
- [other/CELL] p3_vkt_r4c2: 恰 1
- [other/CELL] p3_vkt_r4c3: 不解析，隨檔交給 apply
- [other/CELL] p3_vkt_r5c0 [v2]: apply
- [other/CELL] p3_vkt_r5c1: yes | no
- [other/CELL] p3_vkt_r5c2: 恰 1
- [other/CELL] p3_vkt_r5c3: no → 驗完文法後直接 exit 0（sync 快路徑；終點仍隱含 launcher_completed，約定①）；no 時不得有 pull／extract／mount／engine；yes → 跑 apply <verb> [--dry-run]
- [other/CELL] p3_vkt_r6c0 [v2]: keep
- [other/CELL] p3_vkt_r6c1: <name>|<ref>
- [other/CELL] p3_vkt_r6c2: 0..n
- [other/CELL] p3_vkt_r6c3: 只在 prune：本專案引用、不可刪的 image（含本機覆寫的 <tag>）
- [other/CELL] p3_vkt_r7c0: end
- [other/CELL] p3_vkt_r7c1: <N>
- [other/CELL] p3_vkt_r7c2: 恰 1
- [other/CELL] p3_vkt_r7c3: 必為最後一行
- [rule/RULE] p3_two [v2]: 兩段編排的兩個獨立屬性：需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve <verb> → 主機 docker → apply <verb>，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（add／upgrade 也要先拉 image 展開；uninstall／remove／prune 不拉）。鎖：鎖在引擎 progress 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗印 6-26；VENDOR_KIT_NO_LOCK=1 跳過；啟動器不鎖）。pull 失敗：印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列「主機錯誤」）+ 僅 add／bootstrap 提示 6-24 的「離線可用 --local」；逾時：VENDOR_KIT_PULL_TIMEOUT／--timeout，預設 300 秒，只收正整數（0 或非數字 → 1）；背景 pull + 每秒輪詢 + kill；逾時 → 1 印 6-31
- [rule/RULE] p3_fast [v2]: sync 快路徑（Q22）與 sync --verify：sync（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml vendor_kit ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或本機覆寫的 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 CI 模式。全相符 → 不起容器、0；任一不符或 CI 模式 → 起引擎 resolve sync。每檔 sha256 verify 只在：CI 模式、快路徑有差那次（版本變動）、sync --verify（長形）：先驗既有 cache，不符才重裝一次，再驗仍不符 → 失敗；sync <repo> 一律起引擎驗該範圍。快路徑仍先寫 launcher_started、結束寫 sync_fast_path／launcher_completed。--local 值的判別：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立 → 1 提示用 ./ 或完整 ref 消歧
- [rule/RULE] p3_uf [v2]: uid 旗標（rootless 不加 -u／Podman keep-id）：docker info --format '{{.SecurityOptions}}' 含 name=rootless → rootless，不加 -u；docker --version 含 podman → 加 --userns=keep-id、不加 -u；其餘（rootful docker）加 -u "$(id -u):$(id -g)"
- [rule/RULE] p3_compat [v2]: 相容承諾（Q16／Q19／Q23）：薄殼每次呼叫附 --protocol P（介面版；第一版就有），引擎依 P 回應。永久：任何 ≥ 最低介面版的舊薄殼可呼叫新引擎的救援路徑並得正確提示；舊資料永遠可讀可遷（讀任一舊檔案版 → 直接寫當前檔案版，不鏈式）。非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 3 印 6-36 零寫入。最低介面版 = 固定 release 常數（v1.0.0、P=1、schema=1），只能經 ADR 提高；引擎 image LABEL …protocol=<floor_P>-<current_P> 讓啟動器不起容器即可判最低介面版。降版 upgrade vendor_kit@<舊版>：目標引擎（以介面版／檔案版比）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10；dev vendor_kit -i <舊 image> 禁止重產進 git 的薄殼
- [other/LEGEND] p3b_lg0 [legend]: 淺灰底：分組（無狀態意義）
- [other/LEGEND] p3b_lg1 [legend]: 黃：判斷
- [other/LEGEND] p3b_lg2 [legend]: 橙橢圓：需人處理
- [other/LEGEND] p3b_lg3 [legend]: 綠橢圓：成功終點（exit 0）
- [other/LEGEND] p3b_lg4 [legend]: 紅橢圓：失敗（1）
- [other/LEGEND] p3b_lgt [legend]: 實線 = 執行順序；線上文字 = 條件／接續編號⏎淺灰底容器 = ②③ 的分組（標題 = 該段做的事）
- [other/LEGEND] p3b_lg5 [legend]: 白：啟動器做（主機）
- [other/LEGEND] p3b_lg6 [legend]: 藍：引擎做（容器內）
- [other/LEGEND] p3b_lg7 [legend]: 等寬字：檔案內容範例
- [other/LEGEND] p3b_lg8 [legend]: 淺橘底：規則／摘要（已定）
- [other/LEGEND] p3b_lg9 [legend]: 灰底：表頭
- [other/LEGEND] p3b_lg10 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p3b_lg11 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/LEGEND] p3b_lg12 [legend]: 圖例約定①：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（每個結束碼都寫）⏎圖例約定②：每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started（失敗 → 1 + 6-38、不做任何動作）、結束寫 engine_completed|failed
- [other/TEXT] p3b_th: 本頁名詞（只列本頁用到的）
- [term/TERM_K] p3b_tk0: docker image inspect
- [term/TERM_V] p3b_tv0: 問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）
- [term/TERM_K] p3b_tk1: docker create／cp
- [term/TERM_V] p3b_tv1: 只建容器殼（docker create <ref> /x）再把 /dist 複製出來（docker cp）→ docker rm；純資料 image 沒有程式、不能 docker run；不帶 --platform（daemon 挑原生）
- [term/TERM_K] p3b_tk2: 暫存 .tmp.dist.<id>/
- [term/TERM_V] p3b_tv2: 啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋
- [term/TERM_K] p3b_tk3: REGISTRY_TOKEN／⏎_TOKEN_FILE
- [term/TERM_V] p3b_tv3: 私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v <file>:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 <repo>@<tag> 指定版本（主機 docker pull 走主機認證）
- [term/TERM_K] p3b_tk4: vk-resolve/1
- [term/TERM_V] p3b_tv4: resolve 的 stdout 文法：首行 vk-resolve/<P>、每行 <kind>|<f1>[|<f2>…]（欄位以單一 | 分隔）、末行 end|<N>；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \0ooo 八進位跳脫（printf '%b' 可解）；啟動器先收完整份、驗文法才動 docker
- [term/TERM_K] p3b_tk5: 輸入指紋
- [term/TERM_V] p3b_tv5: resolve 把它讀過的 version.toml、metadata、要動的專案檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」
- [term/TERM_K] p3b_tk6: gen/.stamp
- [term/TERM_V] p3b_tv6: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行

## edges
- s0b_e: s0a(⓪ 產 trace_id （uuid；缺則 od urand…) --(無標籤)--> s0b(建執行紀錄 log/<verb>/ <ts>-<id8>.j…)
- s0c_e: s0b(建執行紀錄 log/<verb>/ <ts>-<id8>.j…) --(無標籤)--> s0c(寫 launcher_started （完整 argv）失敗…)
- s1_e: s0c(寫 launcher_started （完整 argv）失敗…) --(無標籤)--> s1(① 以版本鎖定行 regex grep 引擎 ref （ve…)
- d1_e: s1(① 以版本鎖定行 regex grep 引擎 ref （ve…) --(無標籤)--> d1(只有 sync： gen/.stamp ≠ 引擎 ref？)
- s2a_e: d1(只有 sync： gen/.stamp ≠ 引擎 ref？) --否--> s2a(讀 version.toml／local （CI 模式判定）)
- s2b_e: s2a(讀 version.toml／local （CI 模式判定）) --(無標籤)--> s2b(只有 add／update／upgrade 且未指定 @<t…)
- s2c_e: s2b(只有 add／update／upgrade 且未指定 @<t…) --(無標籤)--> s2c(stdout vk-resolve/1 （pull／extr…)
- p3_err_e: d1(只有 sync： gen/.stamp ≠ 引擎 ref？) --是--> p3_err(是 → 1 印 6-1 （請 upgrade vendor_…)
- s3bx_e: s3b(無：docker pull （逾時 → 1 印 6-31）) --失敗--> s3bx(失敗 → 1 印 6-24 （網路／認證／不存在）)
- s3b_e: s3a(docker image inspect （每筆 pull／…) --無--> s3b(無：docker pull （逾時 → 1 印 6-31）)
- s3c_e: s3b(無：docker pull （逾時 → 1 印 6-31）) --(無標籤)--> s3c(只有 extract kind： docker create…)
- s3d_e: s3c(只有 extract kind： docker create…) --(無標籤)--> s3d(docker cp c:/dist/. → .tmp.dis…)
- s3e_e: s3d(docker cp c:/dist/. → .tmp.dis…) --(無標籤)--> s3e(docker rm （trap 也清）)
- s4_e: s3e(docker rm （trap 也清）) --(無標籤)--> s4(④ docker run 引擎 apply <動詞>（掛 /…)
- d2_e: d2(apply|yes？) --是--> s3a(docker image inspect （每筆 pull／…)
- s3a_skip: s3a(docker image inspect （每筆 pull／…) --有 → 跳過 pull--> s3c(只有 extract kind： docker create…)
- d2_in: s2c(stdout vk-resolve/1 （pull／extr…) --resolve 0--> d2(apply|yes？)
- p3_rx_e: s2c(stdout vk-resolve/1 （pull／extr…) --非 0--> p3_rx(resolve 非 0 → 原碼傳出 （不讀 stdout、…)
- p3_ok_e: d2(apply|yes？) --否--> p3_ok(否（apply|no）→ 0 快路徑 不起第二個容器)
- s4x_e: s4(④ docker run 引擎 apply <動詞>（掛 /…) --(無標籤)--> s4x(→ 終點：結束碼 0／1／2／3 launcher_comp…)

## terms
- docker image inspect: 問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）
- docker create／cp: 只建容器殼（docker create <ref> /x）再把 /dist 複製出來（docker cp）→ docker rm；純資料 image 沒有程式、不能 docker run；不帶 --platform（daemon 挑原生）
- 暫存 .tmp.dist.<id>/: 啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋
- REGISTRY_TOKEN／⏎_TOKEN_FILE: 私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v <file>:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 <repo>@<tag> 指定版本（主機 docker pull 走主機認證）
- vk-resolve/1: resolve 的 stdout 文法：首行 vk-resolve/<P>、每行 <kind>|<f1>[|<f2>…]（欄位以單一 | 分隔）、末行 end|<N>；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \0ooo 八進位跳脫（printf '%b' 可解）；啟動器先收完整份、驗文法才動 docker
- 輸入指紋: resolve 把它讀過的 version.toml、metadata、要動的專案檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行

## xrefs

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p3c -----
# v1p3c  11 契約 v2：CI 契約⑤ 與驗收矩陣

nodes 101（不含 v2 小標）／edges 29／terms 8／xrefs 0

## nodes
- [other/TITLE] title: 契約⑤ CI（interface_spec §7；下游 check.sh；下游 repo check.sh --dist；自身分層 + 驗收分組索引；逐條矩陣見 p3d）
- [other/TEXT] p3c_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p3c_pend: 本頁無待拍板⏎check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 分組索引在本頁、35 條詳表在 p3d
- [other/BAND] p3L5: 契約⑤ CI（下游 check.sh 六步 + Renovate；下游 repo check.sh --dist；vendor_kit 自身分層 + 驗收分組索引）
- [other/TEXT] p3_k0: 專案 CI：只呼叫 .vendor_kit/ci/check.sh，一關過才下一關（每格一步）
- [step/W12] k0: ⓪ version.local.toml 被 git track？
- [step/W12] k1: ① sync（CI 模式）
- [step/W12] k2: ② verify（印記 sha256，全部工具）
- [step/W12] k3: ③ upgrade --dry-run
- [step/W12] k4: ④ 工具測試 just <repo> check（若有；不得再呼叫 check.sh）
- [step/W12] k5: ⑤ 專案測試（just check 若有）
- [end_ok/G12] k6: 全部通過 → 0
- [end_orange/O12] k0f: 命中 → 1 拒絕⏎（請勿把本機覆寫提交）
- [end_red/R12] k2f: 1：印記 sha256 不符⏎（verify 失敗）
- [end_red/R12] k4f: ≠ 0 → 停：工具原碼傳出⏎（1/2/3 語意不適用）
- [end_red/R12] k5f: ≠ 0 → 停：依專案⏎（原碼傳出）
- [end_orange/O12] k1f: 1：薄殼不符（6-1）、未完成接入（6-13）、基準版落後（6-5）、任何本機覆寫
- [end_orange/O12] k1g: 3：介面版／檔案版不合⏎（6-18／6-19；零寫入）
- [end_orange/O12] k3f: CI 模式且需改 進 git 的檔⏎→ 1 印清單（version.toml 不動；與 -y 無關）
- [end_orange/O12] k3g: 仍有衝突標記 → 2；印 6-6～6-8 但不紅燈
- [rule/RULE] p3_kr [v2]: check.sh（§7.1）：第一行 shebang、第二行自描述、其後第一個動作 export CI=1；GitHub／GitLab 一樣、平台無關；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）
- [other/TEXT] p3_rn_l: Renovate 路徑（PR 需合併時；補合併在 PR 分支完成、CI 綠後才 merge）
- [step/W12] rn1: Renovate PR 改 version.toml 一行
- [step/W12] rn2: PR 的 CI 以新版跑 check.sh 完整流程（一行改動本身不構成通過依據）
- [end_orange/O12] rn3: 需合併 → 1 印 6-5
- [step/W12] rn4: 維護者在 PR 分支本機 upgrade <repo> -y
- [step/W12] rn4b: commit + push 到 PR 分支
- [step/W12] rn5: CI 全部再跑（Renovate 不動有人推過的分支）
- [end_ok/G12] rn6: 綠了才 merge
- [rule/RULE] p3_c2 [v2]: Renovate preset（§7.3；下游自選，vendor_kit 不出 bot）：放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；下游 extends: ["github>ycpss91255-research/vendor_kit"]；regex manager 匹配 **/.vendor_kit/version.toml（monorepo 子專案亦命中；key regex 與版本鎖定行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR（matchUpdateTypes）；hostRules 依 host 不寫死 ghcr.io；prBodyNotes = 6-25（6-5 的指令 + 「推 commit 後不要勾 rebase/retry」）；不設 gitIgnoredAuthors、不改 rebaseWhen；postUpgradeTasks 不採
- [rule/RULE] p3_c3 [v2]: 下游 repo 的 CI：check.sh --dist（§7.2）：dist 佈局（files/、init.toml、just/<repo>.just 存在）、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗 [#29]）、以 just 1.33.0 解析每個 <ns>.just（並擋比 1.33 新的功能）、_sync lint（just --dump --dump-format json）、Dockerfile.dist 含 LABEL io.github.<org>.vendor_kit=1、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性
- [other/TEXT] p3_c0: vendor_kit 自身 CI（分層，一關過才下一關；每格一個檢查）
- [step/W12] c_a: env-test
- [step/W12] c_b: test-base
- [step/W12] c_c1 [v2]: lint
- [step/W12] c_c2 [v2]: unit
- [step/W12] c_c3 [v2]: install
- [step/W12] c_c4 [v2]: merge
- [step/W12] c_rc [v2]: 推候選 tag（vN-rc.<n>）
- [step/W12] c_e: release-test（amd64、arm64 原生 runner）
- [step/W12] c_f [v2]: 驗收：已釋出版驅動候選 + fixture 跑完整 §7.4 矩陣
- [step/W12] c_d [v2]: release：正式 GHCR tag vN、Git tag、資產
- [rule/RULE] p3_jm [v2]: just 矩陣 1.33.0 + latest（latest 非 required）；lint 擋比 1.33 新的功能與白名單外主機命令（ADR 記破壞性變更）；驗收用 dev vendor_kit -i <剛 build 的 tag> 同一機制；每版最低環境（docker 19.03、just 1.33.0）跑完整、其他環境（docker 上界、just latest、arm64、WSL2）按世代；驗收 §7.4 條 1–13 缺任一不得出貨（§8-12）；已釋出 image／Release 資產／fixture 永不刪；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」
- [other/TEXT] p3_acc_l: 驗收矩陣分組索引（§7.4；35 條逐條詳表見 p3d；一列一組）
- [header/HDR] p3_acc_h0: 群組
- [header/HDR] p3_acc_h1: 條號
- [header/HDR] p3_acc_h2: 涵蓋情境
- [other/CELL] p3_acc_r0c0 [v2]: 相容承諾
- [other/CELL] p3_acc_r0c1: 1–8
- [other/CELL] p3_acc_r0c2: 已釋出版驅動候選；最低環境 × 世代；升級後 == 全新安裝；連續升級；降版；< 最低介面版；舊 bootstrap.sh 再跑；舊引擎讀新檔
- [other/CELL] p3_acc_r1c0 [v2]: CI 模式與 Renovate
- [other/CELL] p3_acc_r1c1: 9、27
- [other/CELL] p3_acc_r1c2: 只改第一行後 CI=true sync；Renovate 實際 repo
- [other/CELL] p3_acc_r2c0 [v2]: 檔案與路徑
- [other/CELL] p3_acc_r2c1: 10、11、13、19、20、21
- [other/CELL] p3_acc_r2c2: fresh clone 無 gen/；下游使用者改薄殼／未納管檔／append；異常 TOML；append 換行；空白路徑；worktree／submodule
- [other/CELL] p3_acc_r3c0 [v2]: 中斷與環境
- [other/CELL] p3_acc_r3c1: 12、14、15、22
- [other/CELL] p3_acc_r3c2: 中斷與重跑；just 矩陣；amd64／arm64 原生 runner；rootless docker／Podman
- [other/CELL] p3_acc_r4c0 [v2]: 離線
- [other/CELL] p3_acc_r4c1: 16、17
- [other/CELL] p3_acc_r4c2: 離線包；離線可用（斷網 sync／build）
- [other/CELL] p3_acc_r5c0 [v2]: 私有 registry
- [other/CELL] p3_acc_r5c1: 18
- [other/CELL] p3_acc_r5c2: token／TOKEN_FILE；敏感值不入輸出、metadata、執行紀錄、進度檔
- [other/CELL] p3_acc_r6c0 [v2]: prune／多工具／F1／tty
- [other/CELL] p3_acc_r6c1: 23、24、25、26
- [other/CELL] p3_acc_r6c2: prune 差集；多工具彙總；F1 fixture；無 tty／EOF
- [other/CELL] p3_acc_r7c0 [v2]: 動詞集合與執行紀錄
- [other/CELL] p3_acc_r7c1: 28、29、30、31、32
- [other/CELL] p3_acc_r7c2: 驗收動詞集合；執行紀錄逐行 json.loads；argv 跳脫；config.toml 異常值；磁碟不可寫 6-38
- [other/CELL] p3_acc_r8c0 [v2]: 流程特例
- [other/CELL] p3_acc_r8c1: 33、34、35
- [other/CELL] p3_acc_r8c2: bootstrap.sh 逐 -t 中止；E(c) 分支；help 遇未完成交易
- [other/LEGEND] p3c_lg0 [legend]: 橙橢圓：需人處理
- [other/LEGEND] p3c_lg1 [legend]: 綠橢圓：成功終點（exit 0）
- [other/LEGEND] p3c_lg2 [legend]: 紅橢圓：失敗（1）
- [other/LEGEND] p3c_lg3 [legend]: 白：步驟／說明
- [other/LEGEND] p3c_lg4 [legend]: 淺橘底：規則／摘要（已定）
- [other/LEGEND] p3c_lg5 [legend]: 灰底：表頭
- [other/LEGEND] p3c_lgt [legend]: 實線 = 執行順序；線上文字 = 條件⏎分組索引：一列一組
- [other/LEGEND] p3c_lg6 [legend]: 淺灰底：分組（無狀態意義）
- [other/LEGEND] p3c_lg7 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p3c_lg8 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/TEXT] p3c_th: 本頁名詞（只列本頁用到的）
- [term/TERM_K] p3c_tk0: env-test／test-base
- [term/TERM_V] p3c_tv0: vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑
- [term/TERM_K] p3c_tk1: 離線可用（Q26）
- [term/TERM_V] p3c_tv1: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- [term/TERM_K] p3c_tk2: CI／runner
- [term/TERM_V] p3c_tv2: CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進CI 模式）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）
- [term/TERM_K] p3c_tk3: Renovate／PR／rebase
- [term/TERM_V] p3c_tv3: Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）
- [term/TERM_K] p3c_tk4: release／release-test
- [term/TERM_V] p3c_tv4: release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次
- [term/TERM_K] p3c_tk5: fixture repo
- [term/TERM_V] p3c_tv5: 驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪
- [term/TERM_K] p3c_tk6: rootless／Podman
- [term/TERM_V] p3c_tv6: rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收
- [term/TERM_K] p3c_tk7: 候選 tag／正式 tag
- [term/TERM_V] p3c_tv7: 候選 image 先以候選 tag（vN-rc.<n> 或 candidate-<sha>）推上 GHCR；index inspect 與資產都對候選 tag 做；全過才 docker buildx imagetools create 打正式 GHCR image tag vN（不重 build、index digest 不變）；Git tag vN 是 repo 上的另一個物件，圖上分開標

## edges
- k1_e: k0(⓪ version.local.toml 被 git tra…) --(無標籤)--> k1(① sync（CI 模式）)
- k2_e: k1(① sync（CI 模式）) --(無標籤)--> k2(② verify（印記 sha256，全部工具）)
- k3_e: k2(② verify（印記 sha256，全部工具）) --(無標籤)--> k3(③ upgrade --dry-run)
- k4_e: k3(③ upgrade --dry-run) --(無標籤)--> k4(④ 工具測試 just <repo> check（若有；不得…)
- k5_e: k4(④ 工具測試 just <repo> check（若有；不得…) --(無標籤)--> k5(⑤ 專案測試（just check 若有）)
- k6_e: k5(⑤ 專案測試（just check 若有）) --(無標籤)--> k6(全部通過 → 0)
- k0f_e: k0(⓪ version.local.toml 被 git tra…) --命中--> k0f(命中 → 1 拒絕 （請勿把本機覆寫提交）)
- k2f_e: k2(② verify（印記 sha256，全部工具）) --不符--> k2f(1：印記 sha256 不符 （verify 失敗）)
- k4f_e: k4(④ 工具測試 just <repo> check（若有；不得…) --失敗--> k4f(≠ 0 → 停：工具原碼傳出 （1/2/3 語意不適用）)
- k5f_e: k5(⑤ 專案測試（just check 若有）) --失敗--> k5f(≠ 0 → 停：依專案 （原碼傳出）)
- k1f_e: k1(① sync（CI 模式）) --升為失敗--> k1f(1：薄殼不符（6-1）、未完成接入（6-13）、基準版落後（…)
- k1g_e: k1(① sync（CI 模式）) --3--> k1g(3：介面版／檔案版不合 （6-18／6-19；零寫入）)
- k3f_e: k3(③ upgrade --dry-run) --需改檔--> k3f(CI 模式且需改 進 git 的檔 → 1 印清單（vers…)
- k3g_e: k3(③ upgrade --dry-run) --衝突--> k3g(仍有衝突標記 → 2；印 6-6～6-8 但不紅燈)
- rn2_e: rn1(Renovate PR 改 version.toml 一行) --(無標籤)--> rn2(PR 的 CI 以新版跑 check.sh 完整流程（一行改…)
- rn3_e: rn2(PR 的 CI 以新版跑 check.sh 完整流程（一行改…) --(無標籤)--> rn3(需合併 → 1 印 6-5)
- rn4_e: rn3(需合併 → 1 印 6-5) --(無標籤)--> rn4(維護者在 PR 分支本機 upgrade <repo> -y)
- rn4b_e: rn4(維護者在 PR 分支本機 upgrade <repo> -y) --(無標籤)--> rn4b(commit + push 到 PR 分支)
- rn5_e: rn4b(commit + push 到 PR 分支) --(無標籤)--> rn5(CI 全部再跑（Renovate 不動有人推過的分支）)
- rn6_e: rn5(CI 全部再跑（Renovate 不動有人推過的分支）) --(無標籤)--> rn6(綠了才 merge)
- c_b_e: c_a(env-test) --(無標籤)--> c_b(test-base)
- c_c1_e: c_b(test-base) --(無標籤)--> c_c1(lint)
- c_c2_e: c_c1(lint) --(無標籤)--> c_c2(unit)
- c_c3_e: c_c2(unit) --(無標籤)--> c_c3(install)
- c_c4_e: c_c3(install) --(無標籤)--> c_c4(merge)
- c_rc_e: c_c4(merge) --(無標籤)--> c_rc(推候選 tag（vN-rc.<n>）)
- c_e_e: c_rc(推候選 tag（vN-rc.<n>）) --(無標籤)--> c_e(release-test（amd64、arm64 原生 ru…)
- c_f_e: c_e(release-test（amd64、arm64 原生 ru…) --(無標籤)--> c_f(驗收：已釋出版驅動候選 + fixture 跑完整 §7.4…)
- c_d_e: c_f(驗收：已釋出版驅動候選 + fixture 跑完整 §7.4…) --(無標籤)--> c_d(release：正式 GHCR tag vN、Git tag…)

## terms
- env-test／test-base: vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑
- 離線可用（Q26）: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- CI／runner: CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進CI 模式）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）
- Renovate／PR／rebase: Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）
- release／release-test: release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次
- fixture repo: 驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪
- rootless／Podman: rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收
- 候選 tag／正式 tag: 候選 image 先以候選 tag（vN-rc.<n> 或 candidate-<sha>）推上 GHCR；index inspect 與資產都對候選 tag 做；全過才 docker buildx imagetools create 打正式 GHCR image tag vN（不重 build、index digest 不變）；Git tag vN 是 repo 上的另一個物件，圖上分開標

## xrefs

## fills（非圖例）: #d5e8d4 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #d5e8d4 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p3d -----
# v1p3d  12 契約 v2：驗收矩陣詳表

nodes 135（不含 v2 小標）／edges 0／terms 7／xrefs 0

## nodes
- [other/TITLE] title: 契約⑤ 驗收矩陣詳表（interface_spec §7.4；35 條，一列一情境；分組索引與 CI 流程見 p3c）
- [other/TEXT] p3d_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p3d_pend: 本頁無待拍板⏎本頁只有 §7.4 逐條矩陣；缺任一不得出貨（§8-12）；已釋出 image／Release 資產／fixture 永不刪
- [other/BAND] p3L6: 驗收矩陣（§7.4；左右兩表接續；每列一個情境）
- [header/HDR] p3d_acc_h0: #
- [header/HDR] p3d_acc_h1: 情境
- [header/HDR] p3d_acc_h2: 驗什麼
- [other/CELL] p3d_acc_r0c0: 1
- [other/CELL] p3d_acc_r0c1 [v2]: 已釋出版驅動候選
- [other/CELL] p3d_acc_r0c2: 最低介面版以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1）→ upgrade vendor_kit（1 印 6-2）→ sync 0 → 工具 recipe → upgrade 全 → 再 upgrade vendor_kit 0；禁由候選樹複製 fixture、禁 stub 引擎
- [other/CELL] p3d_acc_r1c0: 2
- [other/CELL] p3d_acc_r1c1 [v2]: 最低環境 × 世代
- [other/CELL] p3d_acc_r1c2: 每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境按世代覆蓋；成本上限當觸發討論條件
- [other/CELL] p3d_acc_r2c0: 3
- [other/CELL] p3d_acc_r2c1 [v2]: 升級後 == 全新安裝
- [other/CELL] p3d_acc_r2c2: 升級後 .vendor_kit/ 進 git 的內容 == 用 C 全新 install + add（排除時間戳、digest、written_by）
- [other/CELL] p3d_acc_r3c0: 4
- [other/CELL] p3d_acc_r3c1 [v2]: 連續升級
- [other/CELL] p3d_acc_r3c2: r_i → r_j → C；固定最低介面版直接跳升 C
- [other/CELL] p3d_acc_r4c0: 5
- [other/CELL] p3d_acc_r4c1 [v2]: 降版
- [other/CELL] p3d_acc_r4c2: upgrade vendor_kit@<舊版>：同介面版／檔案版成功；跨檔案版改檔前拒絕 3 印 6-10、零寫入
- [other/CELL] p3d_acc_r5c0: 6
- [other/CELL] p3d_acc_r5c1 [v2]: < 最低介面版太舊
- [other/CELL] p3d_acc_r5c2: 唯一可用 synthetic fixture；任一動詞 → 3 印 6-18、零寫入；最低介面版檢查在任何上網之前（斷網也回 3）
- [other/CELL] p3d_acc_r6c0: 7
- [other/CELL] p3d_acc_r6c1 [v2]: 舊 bootstrap.sh 再跑
- [other/CELL] p3d_acc_r6c2: 在已升級 repo 再跑：用 version.toml 指定引擎，不降版
- [other/CELL] p3d_acc_r7c0: 8
- [other/CELL] p3d_acc_r7c1 [v2]: 舊引擎讀新檔
- [other/CELL] p3d_acc_r7c2: dev vendor_kit -i 舊 image：寫入前拒絕 3 印 6-19；不重產 進 git 的薄殼
- [other/CELL] p3d_acc_r8c0: 9
- [other/CELL] p3d_acc_r8c1 [v2]: 只改第一行後 CI=true sync
- [other/CELL] p3d_acc_r8c2: 模擬 Renovate、驗CI 模式真值規則 → 1 列薄殼不符、零 進 git 的檔寫入
- [other/CELL] p3d_acc_r9c0: 10
- [other/CELL] p3d_acc_r9c1 [v2]: fresh clone 無 gen/
- [other/CELL] p3d_acc_r9c2: just vendor_kit 列出 vendor_kit 命名空間不觸網（工具命名空間 sync 後才出現，mod? 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行
- [other/CELL] p3d_acc_r10c0: 11
- [other/CELL] p3d_acc_r10c1 [v2]: 下游使用者改薄殼／未納管檔／append
- [other/CELL] p3d_acc_r10c2: 不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn
- [other/CELL] p3d_acc_r11c0: 12
- [other/CELL] p3d_acc_r11c1 [v2]: 中斷與重跑
- [other/CELL] p3d_acc_r11c2: resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗
- [other/CELL] p3d_acc_r12c0: 13
- [other/CELL] p3d_acc_r12c1 [v2]: 歷史 parser × 異常 TOML
- [other/CELL] p3d_acc_r12c2: BOM、空白、重複 vendor_kit 行 → 1、schema 位置、本機覆寫、尾端註解
- [other/CELL] p3d_acc_r13c0: 14
- [other/CELL] p3d_acc_r13c1 [v2]: just 矩陣
- [other/CELL] p3d_acc_r13c2: 1.33.0 + latest（latest 非 required）
- [other/CELL] p3d_acc_r14c0: 15
- [other/CELL] p3d_acc_r14c1 [v2]: amd64 與 arm64 原生 runner
- [other/CELL] p3d_acc_r14c2: 各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致
- [other/CELL] p3d_acc_r15c0: 16
- [other/CELL] p3d_acc_r15c1 [v2]: 離線包（Q26）
- [other/CELL] p3d_acc_r15c2: 無法連 GHCR 的機器用 bootstrap.sh --local <tar>（旁檔 .digest）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 local_image_id；旁檔缺 → 1；amd64／arm64 各一次
- [other/CELL] p3d_acc_r16c0: 17
- [other/CELL] p3d_acc_r16c1 [v2]: 離線可用（Q22／Q26）
- [other/CELL] p3d_acc_r16c2: 本機已有 image 後斷網 → just <ns> build（自動 sync 快路徑）與 just vendor_kit sync 必須成功且不起 pull；斷網 + 無 image → 1 印 6-31 於 --timeout 5 內結束、不 hang
- [other/CELL] p3d_acc_r17c0: 18
- [other/CELL] p3d_acc_r17c1 [v2]: 私有工具
- [other/CELL] p3d_acc_r17c2: add <repo>@<tag> 可拉；add／update 無 token → 1 印 6-3；錯 token → 1；對 token → 列出；TOKEN_FILE 驗 -v 掛載；兩者同設 → 1；輸出、metadata、執行紀錄、進度檔皆 grep 不到 token
- [header/HDR] p3d_accb_h0: #
- [header/HDR] p3d_accb_h1: 情境
- [header/HDR] p3d_accb_h2: 驗什麼
- [other/CELL] p3d_accb_r0c0: 19
- [other/CELL] p3d_accb_r0c1 [v2]: append
- [other/CELL] p3d_accb_r0c2: LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 .dockerignore 四行 append → uninstall 刪
- [other/CELL] p3d_accb_r1c0: 20
- [other/CELL] p3d_accb_r1c1 [v2]: 空白路徑
- [other/CELL] p3d_accb_r1c2: 專案根含空白與 $、dev -p "含 空白/路徑"；vk-resolve mount 八進位跳脫往返；just vendor_kit add --help 到引擎
- [other/CELL] p3d_accb_r2c0: 21
- [other/CELL] p3d_accb_r2c1 [v2]: worktree／submodule
- [other/CELL] p3d_accb_r2c2: git worktree（.git 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）
- [other/CELL] p3d_accb_r3c0: 22
- [other/CELL] p3d_accb_r3c1 [v2]: rootless docker／Podman
- [other/CELL] p3d_accb_r3c2: setup-docker-action rootless: true（不加 -u、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：--userns=keep-id）各跑完整流程；uid 12345 無 passwd 項
- [other/CELL] p3d_accb_r4c0: 23
- [other/CELL] p3d_accb_r4c1 [v2]: prune
- [other/CELL] p3d_accb_r4c2: 完整流程前後 docker network ls／volume ls 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊下游 image 刪、version.toml 引用的與本機覆寫 tag 保留；--dry-run 零刪除；未恢復的 .tmp.* 不刪
- [other/CELL] p3d_accb_r5c0: 24
- [other/CELL] p3d_accb_r5c1 [v2]: 多工具彙總（Q27）
- [other/CELL] p3d_accb_r5c2: 兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1
- [other/CELL] p3d_accb_r6c0: 25
- [other/CELL] p3d_accb_r6c1 [v2]: F1 fixture（just 1.33.0）
- [other/CELL] p3d_accb_r6c2: cache 缺檔時 just vendor_kit sync 可進入（mod?）；just <ns> build 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 _sync 的模組
- [other/CELL] p3d_accb_r7c0: 26
- [other/CELL] p3d_accb_r7c1 [v2]: 無 tty／EOF
- [other/CELL] p3d_accb_r7c2: CI 無 -y 需詢問 → 1 印 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑
- [other/CELL] p3d_accb_r8c0: 27
- [other/CELL] p3d_accb_r8c1 [v2]: Renovate 實際 repo
- [other/CELL] p3d_accb_r8c2: 人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中
- [other/CELL] p3d_accb_r9c0: 28
- [other/CELL] p3d_accb_r9c1 [v2]: 驗收動詞集合
- [other/CELL] p3d_accb_r9c2: 由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅
- [other/CELL] p3d_accb_r10c0: 29
- [other/CELL] p3d_accb_r10c1 [v2]: 執行紀錄（v2.12）
- [other/CELL] p3d_accb_r10c2: 每個情境結束後 log/<verb>/ 每檔逐行 json.loads；首筆 launcher_started、末筆 launcher_completed|failed；同檔 trace_id 單一且 = 進度檔 <id>；event_name 全在註冊表；6-xx 同句進 body；sync 快路徑亦有檔；自身升級兩個引擎寫同一檔
- [other/CELL] p3d_accb_r11c0: 30
- [other/CELL] p3d_accb_r11c1 [v2]: 啟動器 argv 跳脫（bats）
- [other/CELL] p3d_accb_r11c2: 餵 "、\、換行、[、]、非 ASCII、-n foo、空字串、\ 結尾 → launcher_started 的 argv 經 json.loads 還原後逐項相等；dash 與 busybox 各跑一次
- [other/CELL] p3d_accb_r12c0: 31
- [other/CELL] p3d_accb_r12c1 [v2]: config.toml
- [other/CELL] p3d_accb_r12c2: keep／days 為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30（缺鍵／缺檔外印警告）；51 檔或 31 天前的檔 → 結束後被 prune，本次的檔與 .gitignore 不刪；改過的 → upgrade vendor_kit 三方合併
- [other/CELL] p3d_accb_r13c0: 32
- [other/CELL] p3d_accb_r13c1 [v2]: 磁碟不可寫 6-38
- [other/CELL] p3d_accb_r13c2: log/ 唯讀或磁碟滿：每個動詞（含 help、prune、sync 快路徑、--dry-run）→ 1 + 6-38、零寫入、不起容器；只給引擎唯讀 → append 失敗 1 + 6-38、resolve 未執行
- [other/CELL] p3d_accb_r14c0: 33
- [other/CELL] p3d_accb_r14c1 [v2]: bootstrap.sh 逐 -t 中止
- [other/CELL] p3d_accb_r14c2: 三個 -t，第二個故意失敗（不存在的 repo）→ 第一個 add 完成且保留、第三個未執行、整體 1 並列出已完成／未處理
- [other/CELL] p3d_accb_r15c0: 34
- [other/CELL] p3d_accb_r15c1 [v2]: E(c) 分支
- [other/CELL] p3d_accb_r15c2: upgrade vendor_kit@<tag>（≠ 現 ref、同介面版／檔案版）→ 不查 registry、建 .tmp.upgrade.<id>.toml、改第一行、接手重產、刪進度檔 → 1 + 6-2；CI=true 且薄殼相符 → 0；中途殺掉新引擎 → 進度檔留存，sync 6-33 結束 1、help 6-33 結束 0、重跑恢復
- [other/CELL] p3d_accb_r16c0: 35
- [other/CELL] p3d_accb_r16c1 [v2]: help 遇未完成交易
- [other/CELL] p3d_accb_r16c2: 留一個 .tmp.remove.<id>.toml → help 印 6-33 結束 0；sync／update 印 6-33 結束 1；三者除執行紀錄外不寫任何檔
- [other/LEGEND] p3d_lg0 [legend]: 灰底：表頭
- [other/LEGEND] p3d_lg1 [legend]: 淺灰底：分組（無狀態意義）
- [other/LEGEND] p3d_lg2 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p3d_lg3 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/LEGEND] p3d_lgt [legend]: 驗收表：一列一個情境⏎分組索引見 p3c
- [other/TEXT] p3d_th: 本頁名詞（只列本頁用到的）
- [term/TERM_K] p3d_tk0: fixture repo
- [term/TERM_V] p3d_tv0: 驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪
- [term/TERM_K] p3d_tk1: env-test／test-base
- [term/TERM_V] p3d_tv1: vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑
- [term/TERM_K] p3d_tk2: release／release-test
- [term/TERM_V] p3d_tv2: release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次
- [term/TERM_K] p3d_tk3: rootless／Podman
- [term/TERM_V] p3d_tv3: rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收
- [term/TERM_K] p3d_tk4: 離線可用（Q26）
- [term/TERM_V] p3d_tv4: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- [term/TERM_K] p3d_tk5: worktree／submodule
- [term/TERM_V] p3d_tv5: git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）
- [term/TERM_K] p3d_tk6: lint／unit／測試矩陣
- [term/TERM_V] p3d_tv6: lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）

## edges

## terms
- fixture repo: 驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪
- env-test／test-base: vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑
- release／release-test: release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次
- rootless／Podman: rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收
- 離線可用（Q26）: 啟動器一律先 docker image inspect：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → docker pull 失敗 → 1 + 6-24／6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援
- worktree／submodule: git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）
- lint／unit／測試矩陣: lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）

## xrefs

## fills（非圖例）: #e6e6e6 #f5f5f5 #ffffff
## legend_fills: #e6e6e6 #f5f5f5 #ffffff none


----- 頁 v1p4 -----
# v1p4  13 架構圖 v2

nodes 149（不含 v2 小標）／edges 38／terms 7／xrefs 0

## nodes
- [other/TITLE] title: 架構圖 v2 ── 主機載入鏈、啟動器、引擎 8 模組、registry（只畫模組、最小單元、模組間傳的資料）
- [other/TEXT] p4_num: 契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③下游 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c／驗收詳表 p3d｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字
- [note/NOTE] p4_np: 本頁無待拍板：本頁只畫模組、最小單元、模組間傳的資料（箭頭只標傳什麼，不標動作；雙箭頭 = 讀寫都有）；順序與判斷一律見流程頁（p5～）。啟動器在主機跑、不算引擎模組（右上紅框；vendor.just 內的 POSIX sh 本體 + 獨立檔 log.sh）；引擎 8 模組見 00 頁名詞；log 模組只記事件，其他模組經同一入口 log_event() 呼叫（不逐條畫線）。專案根 -v <專案根>:/repo -w /repo 掛進引擎（可寫），引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.<id>/ 唯讀掛 /dist/<repo>
- [other/RECT] h4 [v2]: 啟動器（主機側薄殼：vendor.just 內的 POSIX sh 本體 + log.sh；在主機跑；非引擎模組；主機需 docker ≥ 19.03、sh、just ≥ 1.33.0）⏎下列為責任單元；命令步驟見流程頁與 p3b；執行紀錄的建檔／launcher_started 與結束（log_prune、launcher_completed|failed）見 p3b 契約④
- [file/PRE] h4_u0_0: 讀引擎 ref（版本鎖定行／本機覆寫）
- [file/PRE] h4_u0_1: trace_id
- [file/PRE] h4_u0_2: launcher_started
- [file/PRE] h4_u1_0: log_event()（log.sh：source）
- [file/PRE] h4_u1_1: 取得引擎／下游 image
- [file/PRE] h4_u1_2: 展開 /dist 到暫存
- [file/PRE] h4_u1_3: 起引擎容器
- [file/PRE] h4_u2_0: vk-resolve 驗文法
- [file/PRE] h4_u2_1: 介面版旗標 --protocol
- [file/PRE] h4_u2_2: 清理（trap）
- [file/PRE] h4_u2_3: pull 逾時
- [file/PRE] h4_u2_4: 資源 label
- [file/PRE] h4_u3_0: log_prune（keep／days）
- [file/PRE] h4_u3_1: launcher_completed|failed
- [other/BAND] p4G: GHCR（ghcr.io）── 兩種 image 都多架構；拉取都由啟動器執行，引擎容器內不呼叫 docker
- [other/IMG] g_eng [v2]: 引擎 image ghcr.io/<org>/vendor_kit:vN（公開）：多架構 amd64 + arm64；LABEL …vendor_kit=1、.protocol、.schema；一個專案用版本鎖定行那一版；引擎的本機覆寫（version.local.toml）時啟動器 inspect 驗 image ID 後直接用本機 image、不 pull；也出 docker save tar + .digest（#27）；已釋出永不刪
- [other/IMG] g_dist [v2]: 下游 image ghcr.io/<org>/<repo>-dist:<tag>：多架構 amd64 + arm64；純資料 FROM scratch 只有 /dist；LABEL …vendor_kit=1；版本鎖定行與印記記 index digest；resolve 模組只查 tag／index digest（add／update／upgrade 且未指定 @<tag>），sync 不查最新版、只拉鎖定版
- [other/LEAF] p4H: 主機（下游使用者電腦／CI runner）── just 載入鏈與目錄（線 = 誰載入誰）
- [other/ELLIPSE] h0: 下游使用者⏎打 just vendor_kit <動詞> …⏎或 just <ns> …
- [other/RECT] h1 [v2]: 根 justfile（專案檔，進 git）⏎import '.vendor_kit/entry.just'
- [other/RECT] h2: .vendor_kit/entry.just⏎（進 git）mod vendor_kit 'vendor.just'⏎import? 'gen/tools.just'
- [other/RECT] h3 [v2]: .vendor_kit/vendor.just⏎（進 git）動詞 recipe 一行轉發⏎+ 啟動器本體（POSIX sh）
- [other/RECT] h3l [v2]: .vendor_kit/log.sh⏎（進 git；獨立檔）啟動器 log 函式；⏎vendor.just source 它
- [other/CELL] h_vk: .vendor_kit/             # 契約② p2，根目錄只多這個⏎├─ version.toml         # 進 git：版本鎖定行⏎├─ version.local.toml   # 不進 git：本機覆寫⏎├─ config.toml          # 進 git：[log] keep／days⏎├─ .gitignore           # 進 git：我們自己的⏎├─ entry.just           # 進 git：mod + import?⏎├─ vendor.just          # 進 git：動詞 + 啟動器⏎├─ log.sh               # 進 git：啟動器 log 函式⏎├─ ci/check.sh          # 進 git：CI 六步（⓪–⑤）⏎├─ baseline/            # 進 git：基準版 + metadata⏎├─ gen/                 # 不進 git：tools.just、.stamp、⏎│                       #   <repo>.stamp（印記）⏎├─ log/<verb>/          # 不進 git：<ts>-<id8>.jsonl⏎├─ .tmp.<verb>.<id>.toml  # 不進 git：進度檔⏎├─ .tmp.dist.<id>/      # 不進 git：啟動器暫存⏎└─ cache/<repo>/        # 不進 git：工具檔展開
- [step/W12] tmp: 暫存 .vendor_kit/⏎.tmp.dist.<id>/（專案內）⏎下游 image 的 /dist 展開副本 + vk-resolve⏎（啟動器 mktemp、trap 清）
- [file/FILEBOX] g1 [v2]: .vendor_kit/gen/⏎tools.just（不進 git）一行一命名空間⏎mod? <ns> '../cache/<repo>/⏎just/<ns>.just'
- [step/W12] g2 [v2]: 工具命名空間 just <ns> …⏎= cache/<repo>/⏎just/<ns>.just 裡的 recipe；⏎_sync 前置回叫 just vendor_kit sync
- [other/BAND] p4E: 引擎容器 vendor_kit:vN（8 模組；一格一個最小單元）
- [other/LEAF] m_res [v2]: resolve：版本解析
- [file/PRE] m_res_u0_0: 讀版本鎖定行
- [file/PRE] m_res_u0_1: 本機覆寫優先
- [file/PRE] m_res_u1_0: 查最新正式版
- [file/PRE] m_res_u1_1: token／逾時
- [file/PRE] m_res_u2_0: pull／extract 清單
- [file/PRE] m_res_u2_1: 輸入指紋
- [file/PRE] m_res_u3_0: vk-resolve 輸出
- [other/LEAF] m_schema [v2]: schema：設定與格式
- [file/PRE] m_schema_u0_0: 讀寫 VK TOML
- [file/PRE] m_schema_u0_1: 檔案版檢查（6-19）
- [file/PRE] m_schema_u1_0: 未知欄位保留
- [file/PRE] m_schema_u1_1: 版本鎖定行寫入
- [file/PRE] m_schema_u2_0: config.toml（TOML parser）
- [other/LEAF] m_prog [v2]: progress：進度與寫入
- [file/PRE] m_prog_u0_0: 建／恢復／刪進度檔
- [file/PRE] m_prog_u0_1: flock（6-26）
- [file/PRE] m_prog_u1_0: 重驗指紋（6-12）
- [file/PRE] m_prog_u1_1: 暫存檔 → 原子替換
- [file/PRE] m_prog_u2_0: 清除清單（第一次 install）
- [other/LEAF] m_fetch [v2]: fetch：取件 /dist → cache/<repo>/
- [file/PRE] m_fetch_u0_0: 展開 /dist
- [file/PRE] m_fetch_u0_1: 路徑驗證
- [file/PRE] m_fetch_u1_0: 逐檔驗指紋（hash）
- [file/PRE] m_fetch_u2_0: 寫印記 gen/<repo>.stamp
- [file/PRE] m_fetch_u3_0: cache 整批替換
- [other/LEAF] m_init [v2]: initfile：初始檔合併
- [file/PRE] m_init_u0_0: 建初始檔／append
- [file/PRE] m_init_u0_1: 新檔詢問
- [file/PRE] m_init_u1_0: 五態狀態機
- [file/PRE] m_init_u1_1: git merge-file --diff3
- [file/PRE] m_init_u2_0: 基準版推進
- [file/PRE] m_init_u2_1: metadata（含 [progress]）
- [other/LEAF] m_shell [v2]: shell：薄殼產生
- [file/PRE] m_shell_u0_0: 薄殼五檔
- [file/PRE] m_shell_u0_1: 自描述首行
- [file/PRE] m_shell_u1_0: 比對薄殼是否被改（6-28）
- [file/PRE] m_shell_u1_1: gen/.stamp
- [file/PRE] m_shell_u2_0: gen/tools.just（mod?）
- [file/PRE] m_shell_u3_0: 根 justfile 一行
- [file/PRE] m_shell_u4_0: 根 .dockerignore 四行
- [file/PRE] m_shell_u5_0: baseline/.gitkeep
- [other/LEAF] m_prune [v2]: prune：清理
- [file/PRE] m_prune_u0_0: keep 清單
- [file/PRE] m_prune_u0_1: docker label 規則
- [file/PRE] m_prune_u1_0: 清殘留 .tmp.dist.<id>/
- [file/PRE] m_prune_u2_0: 清殘留 .tmp.<verb>.*
- [other/LEAF] m_log [v2]: log：紀錄
- [file/PRE] m_log_u0: log_event()（各模組同一入口）
- [file/PRE] m_log_u1: engine_* 事件
- [file/PRE] m_log_u2: config_read 事件
- [file/PRE] m_log_u3: 事件註冊表（未註冊→FATAL）
- [file/PRE] m_log_u4: Python logging＋JSON
- [file/PRE] m_log_u5: append 同一檔
- [file/PRE] m_log_u6: 憑證永不記
- [other/LEAF] p4P: 專案根（掛載為 /repo）
- [file/FILEBOX] f_log [v2]: log/（不進 git；自帶 .gitignore；執行紀錄）
- [file/FILEBOX] f_log_f0: <verb>/<UTC ts>-<id8>.jsonl
- [file/FILEBOX] f_log_f1: .gitignore（*／!.gitignore）
- [other/RECT] f_ver [v2]: version.toml（進 git；版本鎖定行）
- [file/FILEBOX] f_vl [v2]: version.local.toml（本機覆寫）
- [other/RECT] f_cfg [v2]: config.toml（進 git）
- [file/FILEBOX] f_tmp [v2]: .tmp.<verb>.<id>.toml（進度檔）
- [file/FILEBOX] f_repo [v2]: cache/<repo>/（不進 git，不可改）
- [file/FILEBOX] f_repo_f0: files/…
- [file/FILEBOX] f_repo_f1: init.toml
- [file/FILEBOX] f_repo_f2: just/<ns>.just
- [file/FILEBOX] f_stamp [v2]: gen/<repo>.stamp（印記）
- [other/RECT] f_user [v2]: 初始檔（專案檔，進 git；永不刪、永不覆蓋）
- [other/RECT] f_user_f0: Dockerfile 等（copy）
- [other/RECT] f_user_f1: 根 .gitignore 幾行（append）
- [other/RECT] f_bl [v2]: baseline/<repo>/（進 git）
- [other/RECT] f_bl_f0: 基準版（上次套用的初始檔原版副本）
- [other/RECT] f_bl_f1: metadata（含 [progress]）
- [other/RECT] f_just [v2]: 根 justfile（專案檔）：import 一行
- [other/RECT] f_di [v2]: 根 .dockerignore（專案檔）：四行
- [other/RECT] f_shell [v2]: 薄殼（進 git；首行自描述）
- [other/RECT] f_shell_f0: entry.just
- [other/RECT] f_shell_f1: vendor.just
- [other/RECT] f_shell_f2: log.sh
- [other/RECT] f_shell_f3: .gitignore
- [other/RECT] f_shell_f4: ci/check.sh
- [file/FILEBOX] f_gen [v2]: gen/（不進 git；tools.just = mod? 行、.stamp = 引擎 ref）
- [file/FILEBOX] f_gen_f0: tools.just
- [file/FILEBOX] f_gen_f1: .stamp
- [other/RECT] f_gk [v2]: baseline/.gitkeep（VK 自產的進 git 空檔）
- [file/FILEBOX] f_tmpd [v2]: 殘留 .tmp.dist.<id>/、.tmp.<verb>.*
- [other/LEGEND] p4_lg0 [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p4_lg1 [legend]: 紅：引擎模組
- [other/LEGEND] p4_lg2 [legend]: 白小框：最小單元
- [other/LEGEND] p4_lg3 [legend]: 紅底紅粗框：啟動器（主機側薄殼）
- [other/LEGEND] p4_lg4 [legend]: 淺灰底：主機分組
- [other/LEGEND] p4_lg5 [legend]: 藍底藍框：引擎容器（容器內跑）
- [other/LEGEND] p4_lgt [legend]: 實線 = 資料流（線上文字 = 傳什麼）⏎雙箭頭 = 讀寫都有；黃橢圓 = 下游使用者
- [other/LEGEND] p4_lg6 [legend]: 綠底：專案目錄分組
- [other/LEGEND] p4_lg7 [legend]: 綠框：進 git
- [other/LEGEND] p4_lg8 [legend]: 灰虛線：不進 git（可重建）
- [other/LEGEND] p4_lg9 [legend]: 黃底綠框：專案檔（進 git）
- [other/LEGEND] p4_lg10 [legend]: 等寬字：檔案內容範例
- [other/LEGEND] p4_lg11 [v2] [legend]: 右上角綠標籤：v2 改
- [other/LEGEND] p4_lg12 [legend]: 白底黑框：主機上的目錄／命名空間（不是檔）
- [other/LEGEND] p4_lg13 [legend]: 便條：說明（含「本頁無待拍板」）
- [other/TEXT] p4_th: 本頁名詞（只列本頁用到的）
- [term/TERM_K] p4_tk0: 模組／最小單元
- [term/TERM_V] p4_tv0: 模組 = 引擎裡一塊獨立責任的程式（紅框；8 個模組的責任見第 0 頁）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）
- [term/TERM_K] p4_tk1: config.toml
- [term/TERM_V] p4_tv1: .vendor_kit/config.toml（進 git；install 建、upgrade 三方合併）：schema = 1、[log] keep = 50、days = 30；缺檔或缺鍵 = 預設，非正整數 → 預設 + 警告；引擎用 TOML parser（toml-bridge stage）讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$
- [term/TERM_K] p4_tk2: trace_id／TRACEPARENT
- [term/TERM_V] p4_tv2: 啟動器每次執行產一個 32 hex id（/proc/sys/kernel/random/uuid 去 -，缺則 od /dev/urandom），同值 = 進度檔交易 id；以 -e TRACEPARENT 與 -e VENDOR_KIT_LOG_FILE 傳給引擎，引擎 append 同一個 log 檔
- [term/TERM_K] p4_tk3: 多架構 index／index digest
- [term/TERM_V] p4_tv3: 同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）
- [term/TERM_K] p4_tk4: 暫存目錄 <tmp>
- [term/TERM_V] p4_tv4: 啟動器把下游 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.<id>/，再唯讀掛進引擎當 /dist/<repo>（逐檔判斷讀這裡，不是 cache）；dev 時改掛 <dir>/dist；trap 清掉
- [term/TERM_K] p4_tk5: 掛載（-v）
- [term/TERM_V] p4_tv5: docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/<repo> = 本機覆寫的 <dir>/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）
- [term/TERM_K] p4_tk6: log_event()／log-events.txt
- [term/TERM_V] p4_tv6: log_event() = 引擎內寫執行紀錄的唯一入口（事件名 + k=v；其他模組都呼叫它，圖上不逐條畫線）；log-events.txt = 事件名註冊表，真本在引擎 image，log.sh 內嵌啟動器那份白名單；未註冊 → FATAL

## edges
- pull_eng: g_eng(引擎 image ghcr.io/<org>/vendor_…) --引擎 image--> h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…)
- pull_dist: g_dist(下游 image ghcr.io/<org>/<repo>-…) --下游 image （/dist 層）--> h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…)
- l_h0: h0(下游使用者 打 just vendor_kit <動詞> ……) --(無標籤)--> h1(根 justfile（專案檔，進 git） import '…)
- l_h1: h1(根 justfile（專案檔，進 git） import '…) --(無標籤)--> h2(.vendor_kit/entry.just （進 git）…)
- l_h2: h2(.vendor_kit/entry.just （進 git）…) --(無標籤)--> h3(.vendor_kit/vendor.just （進 git…)
- l_h3l: h3(.vendor_kit/vendor.just （進 git…) --(無標籤)--> h3l(.vendor_kit/log.sh （進 git；獨立檔）…)
- l_g1: h2(.vendor_kit/entry.just （進 git）…) --(無標籤)--> g1(.vendor_kit/gen/ tools.just（不進…)
- l_g2: g1(.vendor_kit/gen/ tools.just（不進…) --(無標籤)--> g2(工具命名空間 just <ns> … = cache/<re…)
- l_g2s: g2(工具命名空間 just <ns> … = cache/<re…) --(無標籤)--> h3(.vendor_kit/vendor.just （進 git…)
- d_res_schema: m_res(resolve：版本解析) --版本鎖定行、 本機覆寫--> m_schema(schema：設定與格式)
- d_schema_prog: m_schema(schema：設定與格式) --進度檔 TOML--> m_prog(progress：進度與寫入)
- d_prog_fetch: m_prog(progress：進度與寫入) --暫存路徑、 原子替換--> m_fetch(fetch：取件 /dist → cache/<repo>/)
- d_fetch_init: m_fetch(fetch：取件 /dist → cache/<repo>/) --新版初始檔 N （/dist）--> m_init(initfile：初始檔合併)
- d_init_shell: m_init(initfile：初始檔合併) --tools.just 重生請求--> m_shell(shell：薄殼產生)
- d_shell_prune: m_shell(shell：薄殼產生) --版本鎖定行 → keep--> m_prune(prune：清理)
- d_cfg_log: m_schema(schema：設定與格式) --config_read （keep／days）--> m_log(log：紀錄)
- w_ver: m_schema(schema：設定與格式) --版本鎖定行--> f_ver(version.toml（進 git；版本鎖定行）)
- w_vl: m_schema(schema：設定與格式) --本機覆寫行（path:／ tag + image ID）--> f_vl(version.local.toml（本機覆寫）)
- w_cfg: f_cfg(config.toml（進 git）) --config.toml （TOML parser）--> m_schema(schema：設定與格式)
- w_tmp: m_prog(progress：進度與寫入) --done／pending、consents--> f_tmp(.tmp.<verb>.<id>.toml（進度檔）)
- w_repo: m_fetch(fetch：取件 /dist → cache/<repo>/) --展開的工具檔 （整批替換）--> f_repo(cache/<repo>/（不進 git，不可改）)
- w_stamp: m_fetch(fetch：取件 /dist → cache/<repo>/) --index digest + 每檔 sha256--> f_stamp(gen/<repo>.stamp（印記）)
- w_user: m_init(initfile：初始檔合併) --初始檔內容 （現況／結果）--> f_user(初始檔（專案檔，進 git；永不刪、永不覆蓋）)
- w_bl: m_init(initfile：初始檔合併) --基準版、metadata （含 [progress]）--> f_bl(baseline/<repo>/（進 git）)
- w_just: m_shell(shell：薄殼產生) --import 那一行--> f_just(根 justfile（專案檔）：import 一行)
- w_di: m_shell(shell：薄殼產生) --.dockerignore 四行--> f_di(根 .dockerignore（專案檔）：四行)
- w_shell: m_shell(shell：薄殼產生) --薄殼五檔內容 （首行／模板）--> f_shell(薄殼（進 git；首行自描述）)
- w_gen: m_shell(shell：薄殼產生) --tools.just、 .stamp 內容--> f_gen(gen/（不進 git；tools.just = mod? …)
- w_gk: m_shell(shell：薄殼產生) --空檔--> f_gk(baseline/.gitkeep（VK 自產的進 git …)
- w_tmpd: m_prune(prune：清理) --殘留清單（刪）--> f_tmpd(殘留 .tmp.dist.<id>/、.tmp.<verb>…)
- w_log: m_log(log：紀錄) --engine_* 事件（append 同一檔）--> f_log(log/（不進 git；自帶 .gitignore；執行紀錄…)
- mount_dist: h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…) ---v .tmp.dist.<id>/ → /dist/<repo>（唯讀）--> p4E(引擎容器 vendor_kit:vN（8 模組；一格一個最小…)
- run_cli: h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…) --動詞、參數、 介面版旗標--> p4E(引擎容器 vendor_kit:vN（8 模組；一格一個最小…)
- ret_cli: p4E(引擎容器 vendor_kit:vN（8 模組；一格一個最小…) --結束碼、 vk-resolve--> h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…)
- q_reg: m_res(resolve：版本解析) --工具 tag／ index digest--> g_dist(下游 image ghcr.io/<org>/<repo>-…)
- q_reg_e: m_res(resolve：版本解析) --引擎 tag／index digest（update／upgrade）--> g_eng(引擎 image ghcr.io/<org>/vendor_…)
- w_log_l: h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…) --↑ 上線：launcher_* 事件（launcher_started／launcher_completed|failed 等；與引擎 append 同一檔；順序見 p3b）--> f_log(log/（不進 git；自帶 .gitignore；執行紀錄…)
- w_cfg_l: f_cfg(config.toml（進 git）) --↑ 下線：固定寫法的 keep 行（grep）--> h4(啟動器（主機側薄殼：vendor.just 內的 POSIX…)

## terms
- 模組／最小單元: 模組 = 引擎裡一塊獨立責任的程式（紅框；8 個模組的責任見第 0 頁）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）
- config.toml: .vendor_kit/config.toml（進 git；install 建、upgrade 三方合併）：schema = 1、[log] keep = 50、days = 30；缺檔或缺鍵 = 預設，非正整數 → 預設 + 警告；引擎用 TOML parser（toml-bridge stage）讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$
- trace_id／TRACEPARENT: 啟動器每次執行產一個 32 hex id（/proc/sys/kernel/random/uuid 去 -，缺則 od /dev/urandom），同值 = 進度檔交易 id；以 -e TRACEPARENT 與 -e VENDOR_KIT_LOG_FILE 傳給引擎，引擎 append 同一個 log 檔
- 多架構 index／index digest: 同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）
- 暫存目錄 <tmp>: 啟動器把下游 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.<id>/，再唯讀掛進引擎當 /dist/<repo>（逐檔判斷讀這裡，不是 cache）；dev 時改掛 <dir>/dist；trap 清掉
- 掛載（-v）: docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/<repo> = 本機覆寫的 <dir>/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）
- log_event()／log-events.txt: log_event() = 引擎內寫執行紀錄的唯一入口（事件名 + k=v；其他模組都呼叫它，圖上不逐條畫線）；log-events.txt = 事件名註冊表，真本在引擎 image，log.sh 內嵌啟動器那份白名單；未註冊 → FATAL

## xrefs

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #f5f5f5 #f8cecc #ffffff none


----- 頁 v1p5 -----
# v1p5  14 流程 v2：bootstrap.sh（1）檢查 → 引擎 image

nodes 80（不含 v2 小標）／edges 33／terms 12／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：bootstrap.sh（1）檢查 → 引擎 image（§2／§3、v2.2 B／C、Q17／Q18、v2.6、v2.13 P4）
- [note/NOTE] pend: 已定（v2.4 Q17／Q18、v2.5 §8、v2.6、v2.13 P4／P5、v2.15）：bootstrap.sh 先驗 git repo／just 才建 log/bootstrap/ 執行紀錄寫 launcher_started；引擎 image 到本機後先讀 LABEL 檢查最低介面版（3 + 6-18 零寫入）；專案已有 version.toml → 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫；install 建 baseline/.gitkeep（VK 自產進 git 的檔）、不建 metadata；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bA [v2]: 5a bootstrap.sh 前半：檢查 git／just → 建執行紀錄 → 引擎 ref（Q18）→ --local 三分支 → inspect → 無才 pull → LABEL 最低介面版檢查；install 見「bootstrap.sh（1′）」頁
- [end_ok/G12] a0: 執行 bootstrap.sh -t <repo>[@<tag>]…
- [end_orange/O12] a2: 1 + 6-16：請先 git init（執行紀錄未建）
- [decision/D12] a1: 是 git repo？（主機側）
- [end_orange/O12] a4: 1 + 6-23：印 just 安裝指令（執行紀錄未建）
- [decision/D12] a3: just ≥ 1.33.0？
- [end_red/R12] a0lx [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [step/W12] a0l [v2]: 是：建 log/bootstrap/ 執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入；v2.13 P4）
- [decision/D12] a1v [v2]: 專案已有 version.toml？
- [rule/RULE] a1r [v2]: Q18（v2.4 §5）：已裝過的 repo 再跑舊 bootstrap.sh → 用 version.toml 的 vendor_kit 版本鎖定行的引擎跑 install（不降版）；拉不到 → 1，不得退回內嵌；只有第一次接入才用內嵌 ref
- [step/W12] a1vy [v2]: 是：引擎 ref = version.toml 的版本鎖定行（拉不到 → 1，不退回內嵌）
- [step/W12] a1vn [v2]: 否：引擎 ref = 內嵌引擎 ref（第一次接入）
- [decision/D12] a5: --local？
- [decision/D12] a8q [v2]: 是：值含 / 或以 .tar 結尾？
- [step/W12] a6i [v2]: 否：docker image inspect <引擎 ref>
- [end_orange/O12] a8ex [v2]: 1：--local 檔案不存在（請檢查路徑）
- [decision/D12] a8e [v2]: 是：該檔案存在？
- [decision/D12] a6q [v2]: 本機有？
- [end_orange/O12] a8tx [v2]: 1 + 6-37：既是檔案也是 image tag，請消歧
- [decision/D12] a8t [v2]: 是：本機也有同名 image tag？
- [step/W12] a6p [v2]: 無：docker pull <引擎 ref>
- [other/IMG] a7: ghcr.io/…/vendor_kit:vN⏎（引擎 image；多架構 amd64+arm64）
- [step/W12] a8l [v2]: 否：docker load <tar>
- [end_red/R12] a8dx [v2]: 1：.digest 旁檔缺（tar 形需要）
- [decision/D12] a8dq [v2]: 有同名 .digest 旁檔？
- [step/W12] a8d [v2]: 是：讀旁檔 = 正式 index digest（tar 形才讀）
- [end_red/R12] a8ix [v2]: 1：本機無此 image（tag 形 --local 不得 pull）
- [step/W12] a8i [v2]: docker image inspect 取 image ID（tag 形 = 值即本機 image tag，不讀 .digest）
- [end_orange/O12] a8px [v2]: 3 + 6-18：引擎低於／高於可用介面版（零寫入）
- [decision/D12] a8p [v2]: 引擎 image LABEL：最低介面版 ≤ bootstrap.sh 介面版？（上網之後、寫入之前）
- [entry/ENTRY] a8z: 續「bootstrap.sh（1′）」頁：docker run <引擎> install（本機 image 直接 run）
- [end_red/R12] a6px [v2]: 1 + 6-24／6-31：pull 失敗／逾時（不退回內嵌）
- [other/LEGEND] p5_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5_lg5 [legend]: 白：步驟
- [other/LEGEND] p5_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p5_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5_lgx_img [legend]: 紫：image
- [other/LEGEND] p5_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5_th: 本頁名詞
- [term/TERM_K] p5_tk0: bootstrap.sh 檔名與內嵌 ref
- [term/TERM_V] p5_tv0: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- [term/TERM_K] p5_tk1: release／tar／.digest／docker load
- [term/TERM_V] p5_tv1: release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker
- [term/TERM_K] p5_tk2: --local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）
- [term/TERM_V] p5_tv2: 離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取，tag 形不讀 .digest（專案已有 version.toml → 用該行，第一次 → 內嵌引擎 ref）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar
- [term/TERM_K] p5_tk3: GHCR／引擎 ref
- [term/TERM_V] p5_tv3: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5_tk4: docker image inspect（啟動器）
- [term/TERM_V] p5_tv4: 啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1；不用 --pull never；引擎 image 的 LABEL 帶介面版／最低介面版，供上網前檢查
- [term/TERM_K] p5_tk5: 6-18（最低介面版）
- [term/TERM_V] p5_tv5: 引擎 image LABEL 的最低介面版高於 bootstrap.sh／薄殼的介面版 → 3 + 6-18「目前薄殼或引擎低於最低介面版 <最低介面版>。請以 bootstrap.sh 重建。」（零寫入；此檢查在任何寫入之前）
- [term/TERM_K] p5_tk6: gen/.stamp
- [term/TERM_V] p5_tv6: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p5_tk7: gen/tools.just／mod?
- [term/TERM_V] p5_tv7: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5_tk8: config.toml（install／uninstall）
- [term/TERM_V] p5_tv8: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- [term/TERM_K] p5_tk9: 6-38
- [term/TERM_V] p5_tv9: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5_tk10: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5_tv10: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- [term/TERM_K] p5_tk11: 6-24／6-31（pull 失敗）
- [term/TERM_V] p5_tv11: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## edges
- ae1: a0(執行 bootstrap.sh -t <repo>[@<ta…) --(無標籤)--> a1(是 git repo？（主機側）)
- ae2: a1(是 git repo？（主機側）) --否--> a2(1 + 6-16：請先 git init（執行紀錄未建）)
- ae3: a1(是 git repo？（主機側）) --是--> a3(just ≥ 1.33.0？)
- ae4: a3(just ≥ 1.33.0？) --否--> a4(1 + 6-23：印 just 安裝指令（執行紀錄未建）)
- ae5: a3(just ≥ 1.33.0？) --是--> a0l(是：建 log/bootstrap/ 執行紀錄、寫 laun…)
- ae5x: a0l(是：建 log/bootstrap/ 執行紀錄、寫 laun…) --失敗--> a0lx(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- ae5l: a0l(是：建 log/bootstrap/ 執行紀錄、寫 laun…) --(無標籤)--> a1v(專案已有 version.toml？)
- ae5y: a1v(專案已有 version.toml？) --是--> a1vy(是：引擎 ref = version.toml 的版本鎖定行…)
- ae5n: a1v(專案已有 version.toml？) --否--> a1vn(否：引擎 ref = 內嵌引擎 ref（第一次接入）)
- ae5a: a1vy(是：引擎 ref = version.toml 的版本鎖定行…) --(無標籤)--> a5(--local？)
- ae5b: a1vn(否：引擎 ref = 內嵌引擎 ref（第一次接入）) --(無標籤)--> a5(--local？)
- ae6: a5(--local？) --是--> a8q(是：值含 / 或以 .tar 結尾？)
- ae7: a5(--local？) --否--> a6i(否：docker image inspect <引擎 ref…)
- ae8: a8q(是：值含 / 或以 .tar 結尾？) --是--> a8e(是：該檔案存在？)
- ae8n: a8q(是：值含 / 或以 .tar 結尾？) --否--> a8i(docker image inspect 取 image I…)
- ae8e: a8e(是：該檔案存在？) --否--> a8ex(1：--local 檔案不存在（請檢查路徑）)
- ae8ey: a8e(是：該檔案存在？) --是--> a8t(是：本機也有同名 image tag？)
- ae8t: a8t(是：本機也有同名 image tag？) --是--> a8tx(1 + 6-37：既是檔案也是 image tag，請消歧)
- ae8tn: a8t(是：本機也有同名 image tag？) --否--> a8l(否：docker load <tar>)
- ae9: a8l(否：docker load <tar>) --(無標籤)--> a8dq(有同名 .digest 旁檔？)
- ae9x: a8dq(有同名 .digest 旁檔？) --否--> a8dx(1：.digest 旁檔缺（tar 形需要）)
- ae9d: a8dq(有同名 .digest 旁檔？) --是--> a8d(是：讀旁檔 = 正式 index digest（tar 形才…)
- ae9i: a8d(是：讀旁檔 = 正式 index digest（tar 形才…) --(無標籤)--> a8i(docker image inspect 取 image I…)
- ae6q: a6i(否：docker image inspect <引擎 ref…) --(無標籤)--> a6q(本機有？)
- ae6p: a6q(本機有？) --無--> a6p(無：docker pull <引擎 ref>)
- ae10: a7(ghcr.io/…/vendor_kit:vN （引擎 im…) --拉--> a6p(無：docker pull <引擎 ref>)
- ae8ix: a8i(docker image inspect 取 image I…) --失敗--> a8ix(1：本機無此 image（tag 形 --local 不得 …)
- ae11: a8i(docker image inspect 取 image I…) --(無標籤)--> a8p(引擎 image LABEL：最低介面版 ≤ bootstr…)
- ae11b: a6p(無：docker pull <引擎 ref>) --(無標籤)--> a8p(引擎 image LABEL：最低介面版 ≤ bootstr…)
- ae11p: a8p(引擎 image LABEL：最低介面版 ≤ bootstr…) --否--> a8px(3 + 6-18：引擎低於／高於可用介面版（零寫入）)
- ae12z: a8p(引擎 image LABEL：最低介面版 ≤ bootstr…) --是--> a8z(續「bootstrap.sh（1′）」頁：docker ru…)
- ae6y: a6q(本機有？) --有--> a8p(引擎 image LABEL：最低介面版 ≤ bootstr…)
- ae6px: a6p(無：docker pull <引擎 ref>) --失敗--> a6px(1 + 6-24／6-31：pull 失敗／逾時（不退回內嵌…)

## terms
- bootstrap.sh 檔名與內嵌 ref: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- release／tar／.digest／docker load: release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker
- --local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）: 離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取，tag 形不讀 .digest（專案已有 version.toml → 用該行，第一次 → 內嵌引擎 ref）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- docker image inspect（啟動器）: 啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1；不用 --pull never；引擎 image 的 LABEL 帶介面版／最低介面版，供上網前檢查
- 6-18（最低介面版）: 引擎 image LABEL 的最低介面版高於 bootstrap.sh／薄殼的介面版 → 3 + 6-18「目前薄殼或引擎低於最低介面版 <最低介面版>。請以 bootstrap.sh 重建。」（零寫入；此檢查在任何寫入之前）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- config.toml（install／uninstall）: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## xrefs
- bA: 見「bootstrap.sh（1′）」頁
- a8z: 續「bootstrap.sh（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5i -----
# v1p5i  15 流程 v2：bootstrap.sh（1′）docker run install

nodes 66（不含 v2 小標）／edges 9／terms 12／xrefs 7

## nodes
- [other/TITLE] title: 流程 v2：bootstrap.sh（1′）docker run install（§2／§3、v2.2 C、v2.13 P4／P5）
- [note/NOTE] pend: 已定（v2.4 Q17／Q18、v2.5 §8、v2.6、v2.13 P4／P5、v2.15）：bootstrap.sh 先驗 git repo／just 才建 log/bootstrap/ 執行紀錄寫 launcher_started；引擎 image 到本機後先讀 LABEL 檢查最低介面版（3 + 6-18 零寫入）；專案已有 version.toml → 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫；install 建 baseline/.gitkeep（VK 自產進 git 的檔）、不建 metadata；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bA1 [v2]: 5a′ bootstrap.sh 中段（承「bootstrap.sh（1）」頁：引擎 image 已在本機）：docker run <引擎> install（見「install（1）（2）」頁）→ 非 0 → 依進度檔清半成品、保留 log/ → 需人處理（橙）或失敗（紅）；成功 → 續「bootstrap.sh（2）」頁
- [entry/ENTRY] a9e0: 來自「bootstrap.sh（1）」頁：引擎 image 已在本機、最低介面版檢查通過（已寫 launcher_started）
- [step/W12] a9 [v2]: docker run <引擎> install（-y 轉發；本機 image 直接 run，不 pull）
- [step/SUB] a9e: 執行 install（詳見「install（1）（2）」頁）
- [file/FGRP] a9f: install 寫（見「install（1）（2）」頁）
- [file/F12] a9f_0: 薄殼五檔（含 log.sh）
- [file/F12] a9f_1: version.toml 版本鎖定行
- [file/F12] a9f_2: gen/.stamp（引擎 ref）
- [file/F12] a9f_3: baseline/.gitkeep（VK 自產）
- [file/F12] a9f_4: config.toml（預設值）
- [file/F12] a9f_5: config.toml 的基準版副本＋metadata
- [file/F12] a9f_6: 根 justfile import 行
- [file/F12] a9f_7: 根 .dockerignore 四行
- [decision/D12] a9q: install 回 0？
- [step/W12] a9c [v2]: 否：依 .tmp.install 進度檔清半成品（log/ 保留；印「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」）
- [decision/D12] a9h [v2]: 需人處理（6-4／6-28／6-35 等，附指令）？
- [end_orange/O12] a9hx [v2]: 1：install 需人處理 → 依指令處理後再跑 bootstrap.sh
- [end_red/R12] a9x [v2]: 1：install 失敗（寫入／驗證），已清半成品
- [entry/ENTRY] a9z: 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）
- [other/LEGEND] p5i_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5i_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5i_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5i_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5i_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5i_lg5 [legend]: 白：步驟
- [other/LEGEND] p5i_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5i_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5i_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5i_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5i_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5i_lgx_img [legend]: 紫：image
- [other/LEGEND] p5i_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5i_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5i_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5i_th: 本頁名詞
- [term/TERM_K] p5i_tk0: bootstrap.sh 檔名與內嵌 ref
- [term/TERM_V] p5i_tv0: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- [term/TERM_K] p5i_tk1: GHCR／引擎 ref
- [term/TERM_V] p5i_tv1: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5i_tk2: 冪等
- [term/TERM_V] p5i_tv2: 同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋下游使用者改過的東西（薄殼被改過 → 1 列差異不動）
- [term/TERM_K] p5i_tk3: gen/.stamp
- [term/TERM_V] p5i_tv3: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p5i_tk4: gen/tools.just／mod?
- [term/TERM_V] p5i_tv4: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5i_tk5: 暫存目錄／原子替換
- [term/TERM_V] p5i_tv5: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- [term/TERM_K] p5i_tk6: just／recipe／import／default
- [term/TERM_V] p5i_tv6: just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）
- [term/TERM_K] p5i_tk7: docker pull／run
- [term/TERM_V] p5i_tv7: pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台
- [term/TERM_K] p5i_tk8: flock
- [term/TERM_V] p5i_tv8: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5i_tk9: config.toml（install／uninstall）
- [term/TERM_V] p5i_tv9: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- [term/TERM_K] p5i_tk10: 6-38
- [term/TERM_V] p5i_tv10: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5i_tk11: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5i_tv11: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## edges
- ae12e: a9e0(來自「bootstrap.sh（1）」頁：引擎 image …) --(無標籤)--> a9(docker run <引擎> install（-y 轉發；…)
- ae12: a9(docker run <引擎> install（-y 轉發；…) --(無標籤)--> a9e(執行 install（詳見「install（1）（2）」頁）)
- ae12f: a9e(執行 install（詳見「install（1）（2）」頁）) --寫--> a9f(install 寫（見「install（1）（2）」頁）)
- ae13: a9(docker run <引擎> install（-y 轉發；…) --(無標籤)--> a9q(install 回 0？)
- ae15: a9q(install 回 0？) --是--> a9z(續「bootstrap.sh（2）」頁：--local 記錄…)
- ae14: a9q(install 回 0？) --否--> a9c(否：依 .tmp.install 進度檔清半成品（log/ …)
- ae14h: a9c(否：依 .tmp.install 進度檔清半成品（log/ …) --(無標籤)--> a9h(需人處理（6-4／6-28／6-35 等，附指令）？)
- ae14y: a9h(需人處理（6-4／6-28／6-35 等，附指令）？) --是--> a9hx(1：install 需人處理 → 依指令處理後再跑 boot…)
- ae14n: a9h(需人處理（6-4／6-28／6-35 等，附指令）？) --否--> a9x(1：install 失敗（寫入／驗證），已清半成品)

## terms
- bootstrap.sh 檔名與內嵌 ref: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- 冪等: 同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋下游使用者改過的東西（薄殼被改過 → 1 列差異不動）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- 暫存目錄／原子替換: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- just／recipe／import／default: just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）
- docker pull／run: pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- config.toml（install／uninstall）: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## xrefs
- bA1: 其他「bootstrap.sh（1）」頁
- bA1: 見「install（1）（2）」頁
- bA1: 續「bootstrap.sh（2）」頁
- a9e0: 來自「bootstrap.sh（1）」頁
- a9e: 見「install（1）（2）」頁
- a9f: 見「install（1）（2）」頁
- a9z: 續「bootstrap.sh（2）」頁

## fills（非圖例）: #FFF4C3 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5ccc -----
# v1p5ccc  16 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add

nodes 76（不含 v2 小標）／edges 20／terms 14／xrefs 6

## nodes
- [other/TITLE] title: 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add → 彙總（§2、v2.2 C、v2.5 §8、v2.6 Q26／Q27）
- [note/NOTE] pend: 已定（v2.4 Q17／Q18、v2.5 §8、v2.6、v2.13 P4／P5、v2.15）：bootstrap.sh 先驗 git repo／just 才建 log/bootstrap/ 執行紀錄寫 launcher_started；引擎 image 到本機後先讀 LABEL 檢查最低介面版（3 + 6-18 零寫入）；專案已有 version.toml → 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫；install 建 baseline/.gitkeep（VK 自產進 git 的檔）、不建 metadata；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bA2 [v2]: 5a″ bootstrap.sh 後半（承「bootstrap.sh（1′）」頁）：--local → 寫 version.local.toml → 對每個 -t 呼叫 add（resolve → 啟動器驗 vk-resolve → docker → apply）→ 任一段非 0 → 立即中止 1（後續 -t 不執行）；全部成功 → 0；不自刪
- [entry/ENTRY] a9e2: 來自「bootstrap.sh（1′）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫；已寫 launcher_started）
- [decision/D12] a8q2 [v2]: --local？
- [step/W12] a8b [v2]: 是：寫 version.local.toml：vendor_kit = "<tag>"＋vendor_kit_image_id（install 成功後才寫）
- [file/F12] a8f: ＋version.local.toml（不進 git；引擎本機覆寫：image tag + image ID；離線包 Q26）
- [step/W12] a10: 呼叫 add <repo>[@<tag>]（-y 轉發）
- [step/W12] a10r [v2]: docker run <引擎> resolve add <repo>
- [step/SUB] a10re: resolve add（不寫任何檔；見「add（1）」頁）
- [decision/D12] a10rq [v2]: resolve 回 0 且 vk-resolve/1 文法合法？
- [step/W12] a10d [v2]: 是：啟動器 docker 段：inspect → pull → extract /dist 到暫存（步驟見「add（1′）」頁）
- [other/IMG] a10g: <repo>-dist@digest⏎（下游 image）
- [step/W12] a10a [v2]: docker run <引擎> apply add <repo>
- [step/SUB] a10ae: apply add（拿鎖、重驗、建進度檔後寫入；見「add（1′）（2）」頁）
- [file/FGRP] a10f: add 寫（每個工具；見「add（2）」頁）
- [file/F12] a10f_0: version.toml [tools] 版本鎖定行（最後寫）
- [file/F12] a10f_1: cache/<repo>/
- [file/F12] a10f_2: gen/<repo>.stamp
- [file/F12] a10f_3: 初始檔（init.toml 的 dest）
- [file/F12] a10f_4: baseline/<repo>/ + .vendor_kit.toml
- [file/F12] a10f_5: gen/tools.just（重生，mod? 行）
- [decision/D12] a10x [v2]: apply 回 0？
- [decision/D12] a10q [v2]: 是 → 還有下一個 -t？
- [other/TEXT] _sp: 
- [end_ok/G12] a13: 0：全部成功，印摘要與要 git add 的清單
- [end_red/R12] a12 [v2]: 1：立即中止（印該段（resolve／docker／apply）的錯誤；列出已完成／未完成，後續 -t 不執行）
- [other/LEGEND] p5d_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5d_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5d_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5d_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5d_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5d_lg5 [legend]: 白：步驟
- [other/LEGEND] p5d_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5d_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5d_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5d_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5d_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5d_lgx_img [legend]: 紫：image
- [other/LEGEND] p5d_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5d_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5d_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5d_th: 本頁名詞
- [term/TERM_K] p5d_tk0: bootstrap.sh 檔名與內嵌 ref
- [term/TERM_V] p5d_tv0: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- [term/TERM_K] p5d_tk1: release／tar／.digest／docker load
- [term/TERM_V] p5d_tv1: release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker
- [term/TERM_K] p5d_tk2: --local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）
- [term/TERM_V] p5d_tv2: 離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取，tag 形不讀 .digest（專案已有 version.toml → 用該行，第一次 → 內嵌引擎 ref）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar
- [term/TERM_K] p5d_tk3: GHCR／引擎 ref
- [term/TERM_V] p5d_tv3: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5d_tk4: docker image inspect（啟動器）
- [term/TERM_V] p5d_tv4: 啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1；不用 --pull never；引擎 image 的 LABEL 帶介面版／最低介面版，供上網前檢查
- [term/TERM_K] p5d_tk5: gen/.stamp
- [term/TERM_V] p5d_tv5: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p5d_tk6: gen/tools.just／mod?
- [term/TERM_V] p5d_tv6: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5d_tk7: resolve／apply 兩段
- [term/TERM_V] p5d_tv7: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p5d_tk8: resolve 非 0
- [term/TERM_V] p5d_tv8: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p5d_tk9: docker pull／run
- [term/TERM_V] p5d_tv9: pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台
- [term/TERM_K] p5d_tk10: flock
- [term/TERM_V] p5d_tv10: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5d_tk11: config.toml（install／uninstall）
- [term/TERM_V] p5d_tv11: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- [term/TERM_K] p5d_tk12: 6-38
- [term/TERM_V] p5d_tv12: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5d_tk13: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5d_tv13: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## edges
- ae16: a9e2(來自「bootstrap.sh（1′）」頁：install …) --(無標籤)--> a8q2(--local？)
- ae17: a8q2(--local？) --是--> a8b(是：寫 version.local.toml：vendor_…)
- ae17f: a8b(是：寫 version.local.toml：vendor_…) --寫--> a8f(＋version.local.toml（不進 git；引擎本…)
- ae17n: a8q2(--local？) --否--> a10(呼叫 add <repo>[@<tag>]（-y 轉發）)
- ae18: a8b(是：寫 version.local.toml：vendor_…) --(無標籤)--> a10(呼叫 add <repo>[@<tag>]（-y 轉發）)
- ae19: a10(呼叫 add <repo>[@<tag>]（-y 轉發）) --(無標籤)--> a10r(docker run <引擎> resolve add <r…)
- ae19e: a10r(docker run <引擎> resolve add <r…) --(無標籤)--> a10re(resolve add（不寫任何檔；見「add（1）」頁）)
- ae20: a10re(resolve add（不寫任何檔；見「add（1）」頁）) --(無標籤)--> a10rq(resolve 回 0 且 vk-resolve/1 文法合…)
- ae20d: a10rq(resolve 回 0 且 vk-resolve/1 文法合…) --是--> a10d(是：啟動器 docker 段：inspect → pull …)
- ae20g: a10g(<repo>-dist@digest （下游 image）) --拉 /dist--> a10d(是：啟動器 docker 段：inspect → pull …)
- ae21: a10d(是：啟動器 docker 段：inspect → pull …) --(無標籤)--> a10a(docker run <引擎> apply add <rep…)
- ae21e: a10a(docker run <引擎> apply add <rep…) --(無標籤)--> a10ae(apply add（拿鎖、重驗、建進度檔後寫入；見「add（…)
- ae21f: a10ae(apply add（拿鎖、重驗、建進度檔後寫入；見「add（…) --寫--> a10f(add 寫（每個工具；見「add（2）」頁）)
- ae22: a10ae(apply add（拿鎖、重驗、建進度檔後寫入；見「add（…) --(無標籤)--> a10x(apply 回 0？)
- ae22q: a10x(apply 回 0？) --是--> a10q(是 → 還有下一個 -t？)
- ae22y: a10q(是 → 還有下一個 -t？) --是：下一個 -t--> a10(呼叫 add <repo>[@<tag>]（-y 轉發）)
- ae20x: a10rq(resolve 回 0 且 vk-resolve/1 文法合…) --否--> a12(1：立即中止（印該段（resolve／docker／appl…)
- ae20dx: a10d(是：啟動器 docker 段：inspect → pull …) --失敗--> a12(1：立即中止（印該段（resolve／docker／appl…)
- ae23: a10x(apply 回 0？) --否--> a12(1：立即中止（印該段（resolve／docker／appl…)
- ae24: a10q(是 → 還有下一個 -t？) --否--> a13(0：全部成功，印摘要與要 git add 的清單)

## terms
- bootstrap.sh 檔名與內嵌 ref: release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>
- release／tar／.digest／docker load: release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker
- --local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）: 離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取，tag 形不讀 .digest（專案已有 version.toml → 用該行，第一次 → 內嵌引擎 ref）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- docker image inspect（啟動器）: 啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1；不用 --pull never；引擎 image 的 LABEL 帶介面版／最低介面版，供上網前檢查
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- docker pull／run: pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- config.toml（install／uninstall）: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## xrefs
- bA2: 其他「bootstrap.sh（1′）」頁
- a9e2: 來自「bootstrap.sh（1′）」頁
- a10re: 見「add（1）」頁
- a10d: 見「add（1′）」頁
- a10ae: 見「add（1′）（2）」頁
- a10f: 見「add（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5c -----
# v1p5c  17 流程 v2：install（1）薄殼

nodes 71（不含 v2 小標）／edges 25／terms 10／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：install（1）主機檢查 → 比對薄殼 → 進度檔 → 產薄殼到暫存（§0／§2、Q17／Q20、v2.15-11）
- [note/NOTE] pend: 已定（v2.4 Q17、v2.5 §8、v2.6、v2.13 P5、v2.15-11）：install 第一次／修復判定用薄殼自描述首行；進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata state=managed）、存在不動；根 justfile／.dockerignore 無則建、有則問後才加、symlink 不寫只印指示；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bI [v2]: 5a′ install（bootstrap.sh 代打或自己打）：執行紀錄 → 主機側檢查 git repo／巢狀 → docker run → flock → 薄殼已存在？→ hash 比對（6-28）→ 建進度檔（第一個寫入前）→ 產薄殼五檔到暫存 → config.toml 缺才產（含基準版副本）；寫入見「install（1′）」頁
- [end_ok/G12] i0: just vendor_kit install（-y…）
- [step/W12] i0l [v2]: 建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入）
- [end_red/R12] i0x [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [end_orange/O12] i3: 1 + 6-16：請先 git init（不代做）
- [decision/D12] i2 [v2]: 是 git repo？（主機側 git rev-parse）
- [end_orange/O12] i2x [v2]: 1 + 6-35：不允許巢狀（上層或下層已有 .vendor_kit/）
- [decision/D12] i2n [v2]: 上層或下層已有 .vendor_kit/？
- [rule/RULE] i2r [v2]: 禁止巢狀（Q20、§0）：由啟動器在主機側檢查——引擎只掛 /repo，看不到上層目錄，也不讀 .git；否 → 1 + 6-35
- [step/W12] i1: 否：docker run <引擎> install …⏎（啟動器不鎖；鎖在引擎）
- [step/SUB] i4a [v2]: flock 專案目錄（60 秒）
- [decision/D12] i4e [v2]: 薄殼已存在？
- [step/SUB] i4en [v2]: 否：第一次 = 全新建
- [end_orange/O12] i4x [v2]: 1 + 6-28：薄殼被改過，列差異不動（零寫入）
- [decision/D12] i4q [v2]: 是 → 薄殼 == 上次產物？（自描述首行 hash）
- [note/NOTE] i4qn [v2]: 自描述首行（Q17）：薄殼每檔（含 log.sh）# vendor_kit-shell/<介面版> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git）
- [step/SUB] i4l [v2]: 是：建進度檔 .tmp.install.<id>.toml（第一次也建；第一個寫入（含暫存檔）之前）
- [file/F12] i4lf [v2]: ＋.vendor_kit/.tmp.install.<id>.toml（進度檔，不進 git；第一次 = 不留半成品的清除清單；install（2）頁最後刪）
- [step/SUB] i4 [v2]: 產 .gitignore 到暫存（自描述首行；排除 cache/、gen/、log/、version.local.toml、.tmp.*）
- [step/SUB] i4_2 [v2]: 產 entry.just 到暫存（自描述首行）
- [step/SUB] i4_3 [v2]: 產 vendor.just 到暫存（自描述首行；source log.sh）
- [step/SUB] i4_3b [v2]: 產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器事件白名單）
- [step/SUB] i4_4 [v2]: 產 ci/check.sh 到暫存（自描述在第二行）
- [decision/D12] i4_5q [v2]: config.toml 存在？（存在 → 不動）
- [step/SUB] i4_5 [v2]: 否：產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30）
- [step/SUB] i4_5b [v2]: 產 baseline/vendor_kit/config.toml 副本到暫存（其基準版）
- [entry/ENTRY] i4z: 續「install（1′）」頁：逐檔原子替換 → version.toml、gen/.stamp、基準版根檔
- [other/LEGEND] p5c_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5c_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5c_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5c_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5c_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5c_lg5 [legend]: 白：步驟
- [other/LEGEND] p5c_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5c_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5c_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5c_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5c_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p5c_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5c_lgx_img [legend]: 紫：image
- [other/LEGEND] p5c_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5c_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5c_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5c_th: 本頁名詞
- [term/TERM_K] p5c_tk0: GHCR／引擎 ref
- [term/TERM_V] p5c_tv0: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5c_tk1: gen/.stamp
- [term/TERM_V] p5c_tv1: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p5c_tk2: gen/tools.just／mod?
- [term/TERM_V] p5c_tv2: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5c_tk3: 暫存目錄／原子替換
- [term/TERM_V] p5c_tv3: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- [term/TERM_K] p5c_tk4: flock
- [term/TERM_V] p5c_tv4: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5c_tk5: config.toml（install／uninstall）
- [term/TERM_V] p5c_tv5: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- [term/TERM_K] p5c_tk6: 6-38
- [term/TERM_V] p5c_tv6: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5c_tk7: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5c_tv7: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- [term/TERM_K] p5c_tk8: install 進度檔
- [term/TERM_V] p5c_tv8: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復
- [term/TERM_K] p5c_tk9: 上次產物
- [term/TERM_V] p5c_tv9: 薄殼每檔自描述首行的 sha256 與其餘內容相符（Q17）= 是引擎上次產出、未被人改 → 可重產；不符 → 1 + 6-28 列差異、零寫入

## edges
- ie1: i0(just vendor_kit install（-y…）) --(無標籤)--> i0l(建執行紀錄、寫 launcher_started（失敗 → …)
- ie1x: i0l(建執行紀錄、寫 launcher_started（失敗 → …) --失敗--> i0x(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- ie1l: i0l(建執行紀錄、寫 launcher_started（失敗 → …) --(無標籤)--> i2(是 git repo？（主機側 git rev-parse）)
- ie3: i2(是 git repo？（主機側 git rev-parse）) --否--> i3(1 + 6-16：請先 git init（不代做）)
- ie2n: i2(是 git repo？（主機側 git rev-parse）) --是--> i2n(上層或下層已有 .vendor_kit/？)
- ie2x: i2n(上層或下層已有 .vendor_kit/？) --是--> i2x(1 + 6-35：不允許巢狀（上層或下層已有 .vendor…)
- ie2d: i2n(上層或下層已有 .vendor_kit/？) --否--> i1(否：docker run <引擎> install … （啟…)
- ie1e: i1(否：docker run <引擎> install … （啟…) --(無標籤)--> i4a(flock 專案目錄（60 秒）)
- ie4a: i4a(flock 專案目錄（60 秒）) --(無標籤)--> i4e(薄殼已存在？)
- ie5n: i4e(薄殼已存在？) --否--> i4en(否：第一次 = 全新建)
- ie5y: i4e(薄殼已存在？) --是--> i4q(是 → 薄殼 == 上次產物？（自描述首行 hash）)
- ie5x: i4q(是 → 薄殼 == 上次產物？（自描述首行 hash）) --否--> i4x(1 + 6-28：薄殼被改過，列差異不動（零寫入）)
- ie6: i4q(是 → 薄殼 == 上次產物？（自描述首行 hash）) --是--> i4l(是：建進度檔 .tmp.install.<id>.toml（…)
- ie6n: i4en(否：第一次 = 全新建) --(無標籤)--> i4l(是：建進度檔 .tmp.install.<id>.toml（…)
- ie6lf: i4l(是：建進度檔 .tmp.install.<id>.toml（…) --寫--> i4lf(＋.vendor_kit/.tmp.install.<id>…)
- ie6ln: i4l(是：建進度檔 .tmp.install.<id>.toml（…) --(無標籤)--> i4(產 .gitignore 到暫存（自描述首行；排除 cach…)
- ie4c: i4(產 .gitignore 到暫存（自描述首行；排除 cach…) --(無標籤)--> i4_2(產 entry.just 到暫存（自描述首行）)
- ie4d: i4_2(產 entry.just 到暫存（自描述首行）) --(無標籤)--> i4_3(產 vendor.just 到暫存（自描述首行；source…)
- ie4e: i4_3(產 vendor.just 到暫存（自描述首行；source…) --(無標籤)--> i4_3b(產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器…)
- ie4e2: i4_3b(產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器…) --(無標籤)--> i4_4(產 ci/check.sh 到暫存（自描述在第二行）)
- ie4f: i4_4(產 ci/check.sh 到暫存（自描述在第二行）) --(無標籤)--> i4_5q(config.toml 存在？（存在 → 不動）)
- ie4g: i4_5q(config.toml 存在？（存在 → 不動）) --否--> i4_5(否：產 config.toml 到暫存（含註解與預設 sch…)
- ie4h: i4_5(否：產 config.toml 到暫存（含註解與預設 sch…) --(無標籤)--> i4_5b(產 baseline/vendor_kit/config.t…)
- ie5: i4_5b(產 baseline/vendor_kit/config.t…) --(無標籤)--> i4z(續「install（1′）」頁：逐檔原子替換 → versi…)
- ie4gy: i4_5q(config.toml 存在？（存在 → 不動）) --是：不產、不動--> i4z(續「install（1′）」頁：逐檔原子替換 → versi…)

## terms
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- 暫存目錄／原子替換: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- config.toml（install／uninstall）: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- install 進度檔: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復
- 上次產物: 薄殼每檔自描述首行的 sha256 與其餘內容相符（Q17）= 是引擎上次產出、未被人改 → 可重產；不符 → 1 + 6-28 列差異、零寫入

## xrefs
- bI: 見「install（1′）」頁
- i4z: 續「install（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5cw -----
# v1p5cw  18 流程 v2：install（1′）寫入

nodes 67（不含 v2 小標）／edges 20／terms 9／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：install（1′）原子替換 → version.toml、gen/.stamp、基準版（§2、v2.13 P5、v2.15）
- [note/NOTE] pend: 已定（v2.4 Q17、v2.5 §8、v2.6、v2.13 P5、v2.15-11）：install 第一次／修復判定用薄殼自描述首行；進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata state=managed）、存在不動；根 justfile／.dockerignore 無則建、有則問後才加、symlink 不寫只印指示；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bI1 [v2]: 5a′′ install 寫入段（承「install（1）」頁：進度檔已建、五檔已在暫存）：薄殼五檔逐檔原子替換 → config.toml 缺才寫（含基準版副本與 metadata）→ version.toml 缺才寫 → gen/.stamp → baseline/.gitkeep 缺才建；續「install（2）」頁
- [entry/ENTRY] i4ze: 來自「install（1）」頁：進度檔已建；薄殼五檔（＋config.toml 若缺）已產到暫存（已寫 launcher_started）
- [step/SUB] i4b [v2]: 薄殼五檔逐檔原子替換（暫存 → 正式位置）
- [file/FGRP] i4f: ＋.vendor_kit/ 薄殼五檔（進 git）
- [file/F12] i4f_0: .gitignore
- [file/F12] i4f_1: entry.just
- [file/F12] i4f_2: vendor.just
- [file/F12] i4f_3: log.sh
- [file/F12] i4f_4: ci/check.sh
- [decision/D12] i4bcq [v2]: config.toml 本次有產到暫存（原本缺）？
- [step/SUB] i4bc [v2]: 是：config.toml 原子替換
- [file/F12] i4bcf [v2]: ＋config.toml（進 git；含註解與預設）
- [step/SUB] i4bb [v2]: baseline/vendor_kit/config.toml 副本原子替換
- [file/F12] i4bbf [v2]: ＋baseline/vendor_kit/config.toml（進 git；三方合併用的 B）
- [step/SUB] i4bm [v2]: 寫 metadata baseline/.vendor_kit.toml：config.toml state=managed
- [file/F12] i4bmf [v2]: ＋baseline/.vendor_kit.toml（進 git；config.toml 與根 .dockerignore 的紀錄，v2.13 P10）
- [decision/D12] i4cq [v2]: version.toml 缺？
- [step/SUB] i4c [v2]: 是：寫 version.toml（vendor_kit 版本鎖定行 = 引擎 ref＋schema、written_by）
- [file/F12] i4cf: ＋version.toml（vendor_kit 版本鎖定行、schema、written_by；進 git）
- [step/SUB] i4d [v2]: 寫 gen/.stamp（只記引擎 ref）
- [file/F12] i4df: ＋gen/.stamp（不進 git）
- [step/SUB] i4g [v2]: 缺才建 baseline/.gitkeep（VK 自產進 git 的檔，hash 固定為空檔；metadata 到 add 才建）
- [file/F12] i4gf: ＋baseline/.gitkeep（進 git）
- [entry/ENTRY] i5z: 續「install（2）」頁：根 justfile 與根 .dockerignore
- [other/TEXT] _sp: 
- [end_red/R12] i4wx [v2]: 1：寫入失敗 → 第一次：依進度檔移除已寫的檔、不留半成品（log/ 保留）；修復型：列已完成／未完成，下次可寫動詞先恢復
- [other/LEGEND] p5cw_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5cw_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5cw_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5cw_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5cw_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5cw_lg5 [legend]: 白：步驟
- [other/LEGEND] p5cw_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5cw_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5cw_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5cw_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5cw_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5cw_lgx_img [legend]: 紫：image
- [other/LEGEND] p5cw_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5cw_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5cw_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5cw_th: 本頁名詞
- [term/TERM_K] p5cw_tk0: GHCR／引擎 ref
- [term/TERM_V] p5cw_tv0: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5cw_tk1: gen/.stamp
- [term/TERM_V] p5cw_tv1: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p5cw_tk2: gen/tools.just／mod?
- [term/TERM_V] p5cw_tv2: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5cw_tk3: 暫存目錄／原子替換
- [term/TERM_V] p5cw_tv3: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- [term/TERM_K] p5cw_tk4: flock
- [term/TERM_V] p5cw_tv4: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5cw_tk5: config.toml（install／uninstall）
- [term/TERM_V] p5cw_tv5: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- [term/TERM_K] p5cw_tk6: 6-38
- [term/TERM_V] p5cw_tv6: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5cw_tk7: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5cw_tv7: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- [term/TERM_K] p5cw_tk8: install 進度檔
- [term/TERM_V] p5cw_tv8: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復

## edges
- ie5e: i4ze(來自「install（1）」頁：進度檔已建；薄殼五檔（＋co…) --(無標籤)--> i4b(薄殼五檔逐檔原子替換（暫存 → 正式位置）)
- ie6f: i4b(薄殼五檔逐檔原子替換（暫存 → 正式位置）) --寫--> i4f(＋.vendor_kit/ 薄殼五檔（進 git）)
- ie6q: i4b(薄殼五檔逐檔原子替換（暫存 → 正式位置）) --(無標籤)--> i4bcq(config.toml 本次有產到暫存（原本缺）？)
- ie6bc: i4bcq(config.toml 本次有產到暫存（原本缺）？) --是--> i4bc(是：config.toml 原子替換)
- ie6bcf: i4bc(是：config.toml 原子替換) --寫--> i4bcf(＋config.toml（進 git；含註解與預設）)
- ie6bb: i4bc(是：config.toml 原子替換) --(無標籤)--> i4bb(baseline/vendor_kit/config.tom…)
- ie6bbf: i4bb(baseline/vendor_kit/config.tom…) --寫--> i4bbf(＋baseline/vendor_kit/config.to…)
- ie6bm: i4bb(baseline/vendor_kit/config.tom…) --(無標籤)--> i4bm(寫 metadata baseline/.vendor_ki…)
- ie6bmf: i4bm(寫 metadata baseline/.vendor_ki…) --寫--> i4bmf(＋baseline/.vendor_kit.toml（進 g…)
- ie6cq: i4bm(寫 metadata baseline/.vendor_ki…) --(無標籤)--> i4cq(version.toml 缺？)
- ie6c: i4cq(version.toml 缺？) --是--> i4c(是：寫 version.toml（vendor_kit 版本…)
- ie6cf: i4c(是：寫 version.toml（vendor_kit 版本…) --寫--> i4cf(＋version.toml（vendor_kit 版本鎖定行…)
- ie6d: i4c(是：寫 version.toml（vendor_kit 版本…) --(無標籤)--> i4d(寫 gen/.stamp（只記引擎 ref）)
- ie6df: i4d(寫 gen/.stamp（只記引擎 ref）) --寫--> i4df(＋gen/.stamp（不進 git）)
- ie6g: i4d(寫 gen/.stamp（只記引擎 ref）) --(無標籤)--> i4g(缺才建 baseline/.gitkeep（VK 自產進 g…)
- ie6gf: i4g(缺才建 baseline/.gitkeep（VK 自產進 g…) --寫--> i4gf(＋baseline/.gitkeep（進 git）)
- ie7: i4g(缺才建 baseline/.gitkeep（VK 自產進 g…) --(無標籤)--> i5z(續「install（2）」頁：根 justfile 與根 .…)
- ie6bn: i4bcq(config.toml 本次有產到暫存（原本缺）？) --否：已有 → 不動--> i4cq(version.toml 缺？)
- ie6cn: i4cq(version.toml 缺？) --否：已有 → 不動--> i4d(寫 gen/.stamp（只記引擎 ref）)
- ie7x: i4g(缺才建 baseline/.gitkeep（VK 自產進 g…) --失敗（任一步）--> i4wx(1：寫入失敗 → 第一次：依進度檔移除已寫的檔、不留半成品（…)

## terms
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- 暫存目錄／原子替換: 先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依進度檔丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- config.toml（install／uninstall）: .vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- install 進度檔: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復

## xrefs
- bI1: 其他「install（1）」頁
- bI1: 續「install（2）」頁
- i4ze: 來自「install（1）」頁
- i5z: 續「install（2）」頁

## fills（非圖例）: #FFF4C3 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5cc -----
# v1p5cc  19 流程 v2：install（2）根 justfile 與 .dockerignore

nodes 70（不含 v2 小標）／edges 35／terms 8／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22 補）
- [note/NOTE] pend: 已定（v2.4 Q17、v2.5 §8、v2.6、v2.13 P5、v2.15-11）：install 第一次／修復判定用薄殼自描述首行；進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata state=managed）、存在不動；根 justfile／.dockerignore 無則建、有則問後才加、symlink 不寫只印指示；引擎 image 一律先 docker image inspect，本機有就不 pull。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bI2 [v2]: 5a‴ install 收尾（承「install（1′）」頁）：根 justfile（無 → 新建；symlink → 不寫、印一次性遷移指示；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；symlink → 不寫；已含跳過；問後 append）→ 刪進度檔 → 0
- [entry/ENTRY] i5e: 來自「install（1′）」頁：薄殼與 .vendor_kit/ 各檔已寫（已寫 launcher_started）
- [decision/D12] i5 [v2]: --no-justfile？
- [decision/D12] i6: 否 → 有根 justfile？
- [decision/D12] i6s [v2]: 有 → 是 symlink？
- [step/SUB] i6sp [v2]: 是：不寫，印一次性遷移指示
- [decision/D12] i8 [v2]: 否 → 已含 import 那行？
- [step/SUB] i8p [v2]: 是：不再加（印已含）
- [decision/D12] i12: 問 6-20「要加這一行嗎」同意？（-y 免問）
- [step/SUB] i7: 無：建 justfile（四行，逐字見右）、印建了什麼
- [step/SUB] i11: 是：append 那一行（import）、印加了什麼
- [step/SUB] i12p [v2]: 否：不動（印指示）
- [file/PRE] i11f [v2]: justfile（無 → 新建逐字四行；有 → 尾端只＋第一行；recipe 本體 tab 縮排）⏎import '.vendor_kit/entry.just'⏎default:⏎	@just --list
- [decision/D12] ig [v2]: 有根 .dockerignore？
- [decision/D12] igs [v2]: 有 → 是 symlink？
- [step/SUB] ign [v2]: 無：建 .dockerignore（四行，逐字同右下）、印建了什麼
- [decision/D12] igq0 [v2]: 否 → 已含這四行？
- [step/SUB] igsp [v2]: 是：不寫，印一次性遷移指示
- [decision/D12] igq [v2]: 問 6-34「要加這四行嗎」同意？（-y 免問）
- [step/SUB] igq0p [v2]: 是：跳過（印已含）
- [step/SUB] igy [v2]: 是：append 四行、印加了什麼
- [step/SUB] igqp [v2]: 否：不動（印指示）
- [file/PRE] igyf [v2]: .dockerignore（新建或尾端＋四行，逐字；Q22 補）：⏎.vendor_kit/cache/⏎.vendor_kit/gen/⏎.vendor_kit/.tmp.*⏎.vendor_kit/log/
- [step/SUB] igm [v2]: 插入的行記在 baseline/.vendor_kit.toml（lines）
- [file/F12] igmf [v2]: baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）
- [step/SUB] idl [v2]: 刪進度檔 .tmp.install.<id>.toml（最後一步）
- [file/F12] idlf [v2]: －.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）
- [end_ok/G12] iz: 0：印建立／修改了什麼（含加的行；拒絕的印指示）
- [rule/RULE] i12_tty: 無tty→6-4
- [rule/RULE] igq_tty: 無tty→6-4
- [other/LEGEND] p5cc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5cc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5cc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5cc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5cc_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5cc_lg5 [legend]: 白：步驟
- [other/LEGEND] p5cc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5cc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5cc_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5cc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5cc_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5cc_lgx_img [legend]: 紫：image
- [other/LEGEND] p5cc_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5cc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/LEGEND] p5cc_lgx_tty [legend]: 橙小標：問句無 tty／EOF 且無 -y → 1 + 6-4（Ctrl-C 中止、不記拒絕）
- [other/TEXT] p5cc_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5cc_th: 本頁名詞
- [term/TERM_K] p5cc_tk0: GHCR／引擎 ref
- [term/TERM_V] p5cc_tv0: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- [term/TERM_K] p5cc_tk1: gen/tools.just／mod?
- [term/TERM_V] p5cc_tv1: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- [term/TERM_K] p5cc_tk2: just／recipe／import／default
- [term/TERM_V] p5cc_tv2: just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）
- [term/TERM_K] p5cc_tk3: flock
- [term/TERM_V] p5cc_tv3: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5cc_tk4: 6-38
- [term/TERM_V] p5cc_tv4: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5cc_tk5: 6-16／6-23／6-28／6-35
- [term/TERM_V] p5cc_tv5: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- [term/TERM_K] p5cc_tk6: install 進度檔
- [term/TERM_V] p5cc_tv6: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復
- [term/TERM_K] p5cc_tk7: 6-4（無 tty）
- [term/TERM_V] p5cc_tv7: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## edges
- ie7: i5e(來自「install（1′）」頁：薄殼與 .vendor_k…) --(無標籤)--> i5(--no-justfile？)
- ie9: i5(--no-justfile？) --否--> i6(否 → 有根 justfile？)
- ie10: i6(否 → 有根 justfile？) --無--> i7(無：建 justfile（四行，逐字見右）、印建了什麼)
- ie12: i6(否 → 有根 justfile？) --有--> i6s(有 → 是 symlink？)
- ie12s: i6s(有 → 是 symlink？) --是--> i6sp(是：不寫，印一次性遷移指示)
- ie12n: i6s(有 → 是 symlink？) --否--> i8(否 → 已含 import 那行？)
- ie13b: i8(否 → 已含 import 那行？) --是--> i8p(是：不再加（印已含）)
- ie14: i8(否 → 已含 import 那行？) --否--> i12(問 6-20「要加這一行嗎」同意？（-y 免問）)
- ie17: i12(問 6-20「要加這一行嗎」同意？（-y 免問）) --是--> i11(是：append 那一行（import）、印加了什麼)
- ie18: i12(問 6-20「要加這一行嗎」同意？（-y 免問）) --否--> i12p(否：不動（印指示）)
- ie16f: i11(是：append 那一行（import）、印加了什麼) --寫--> i11f(justfile（無 → 新建逐字四行；有 → 尾端只＋第一…)
- ie19d: i11(是：append 那一行（import）、印加了什麼) --(無標籤)--> ig(有根 .dockerignore？)
- ie13: i7(無：建 justfile（四行，逐字見右）、印建了什麼) --(無標籤)--> ig(有根 .dockerignore？)
- ie12sr: i6sp(是：不寫，印一次性遷移指示) --(無標籤)--> ig(有根 .dockerignore？)
- ie13br: i8p(是：不再加（印已含）) --(無標籤)--> ig(有根 .dockerignore？)
- ie18r: i12p(否：不動（印指示）) --(無標籤)--> ig(有根 .dockerignore？)
- ie20: ig(有根 .dockerignore？) --無--> ign(無：建 .dockerignore（四行，逐字同右下）、印建…)
- ie21: ig(有根 .dockerignore？) --有--> igs(有 → 是 symlink？)
- ie20z: ign(無：建 .dockerignore（四行，逐字同右下）、印建…) --(無標籤)--> idl(刪進度檔 .tmp.install.<id>.toml（最後…)
- ie21s: igs(有 → 是 symlink？) --是--> igsp(是：不寫，印一次性遷移指示)
- ie21sn: igs(有 → 是 symlink？) --否--> igq0(否 → 已含這四行？)
- ie21y: igq0(否 → 已含這四行？) --是--> igq0p(是：跳過（印已含）)
- ie21n: igq0(否 → 已含這四行？) --否--> igq(問 6-34「要加這四行嗎」同意？（-y 免問）)
- ie22: igq(問 6-34「要加這四行嗎」同意？（-y 免問）) --否--> igqp(否：不動（印指示）)
- ie23: igq(問 6-34「要加這四行嗎」同意？（-y 免問）) --是--> igy(是：append 四行、印加了什麼)
- ie23f: igy(是：append 四行、印加了什麼) --寫--> igyf(.dockerignore（新建或尾端＋四行，逐字；Q22 …)
- ie23m: igy(是：append 四行、印加了什麼) --(無標籤)--> igm(插入的行記在 baseline/.vendor_kit.to…)
- ie23mf: igm(插入的行記在 baseline/.vendor_kit.to…) --寫--> igmf(baseline/.vendor_kit.toml（記 .d…)
- ie24: igm(插入的行記在 baseline/.vendor_kit.to…) --(無標籤)--> idl(刪進度檔 .tmp.install.<id>.toml（最後…)
- ie24f: idl(刪進度檔 .tmp.install.<id>.toml（最後…) --刪--> idlf(－.vendor_kit/.tmp.install.<id>…)
- ie21sr: igsp(是：不寫，印一次性遷移指示) --(無標籤)--> idl(刪進度檔 .tmp.install.<id>.toml（最後…)
- ie21yr: igq0p(是：跳過（印已含）) --(無標籤)--> idl(刪進度檔 .tmp.install.<id>.toml（最後…)
- ie22r: igqp(否：不動（印指示）) --(無標籤)--> idl(刪進度檔 .tmp.install.<id>.toml（最後…)
- ie25: idl(刪進度檔 .tmp.install.<id>.toml（最後…) --(無標籤)--> iz(0：印建立／修改了什麼（含加的行；拒絕的印指示）)
- ie8: i5(--no-justfile？) --是：不碰根 justfile--> ig(有根 .dockerignore？)

## terms
- GHCR／引擎 ref: GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe
- just／recipe／import／default: just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）
- install 進度檔: .tmp.install.<id>.toml：拿鎖、比對薄殼之後、第一個寫入（含暫存檔）之前建；第一次也建 = 「不留半成品」的清除清單；最後一步（install（2）頁）刪；未完成 → 下次可寫動詞先恢復
- 6-4（無 tty）: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## xrefs
- bI2: 其他「install（1′）」頁
- i5e: 來自「install（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5b -----
# v1p5b  20 流程 v2：add（1）resolve → docker

nodes 88（不含 v2 小標）／edges 28／terms 9／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：add <repo>（1）--local → 引擎 resolve（§2／§5、v2.5 §2／§3／§5、v2.15-4）
- [note/NOTE] pend: 已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = "copy" | "append"（預設 copy）。已定（v2.5 §2／§3／§5、v2.15-4）：逐檔判斷讀暫存 /dist/<repo>，取件在決定套用後；apply 順序 = flock → 重驗指紋 → 驗原 argv 與計畫一致 → dry-run 分支 → 建進度檔 → 寫入 → 刪進度檔；vk-resolve/1 只傳 pull／extract／mount 清單、apply|yes／no、指紋；已接入且完成 → 0 先於查 registry。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bB [v2]: 5b add <repo>[@<tag>]：執行紀錄 →（--local：主機 docker load、讀 .digest）→ resolve（不寫；已接入且完成 → 0 先判；私有無憑證 → 6-3）→ stdout 只傳協定內容；docker 段見「add（1′）」頁
- [end_ok/G12] c0: just vendor_kit add <repo>[@<tag>]（-y、--dry-run…）
- [step/W12] c0l [v2]: 建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入）
- [end_red/R12] c0x [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [decision/D12] c1q [v2]: --local？
- [end_orange/O12] c1x [v2]: 1 + 6-24：--local 只收存在的 .tar
- [decision/D12] c1t [v2]: 是 → 值是存在的 .tar？
- [end_red/R12] c1lx [v2]: 1：docker load 失敗（印原文）
- [step/W12] c1l [v2]: 是：docker load <tar>
- [end_red/R12] c1dx [v2]: 1：.digest 旁檔缺／格式不合法／讀不到
- [step/W12] c1d [v2]: 讀同名 .digest 旁檔 = 正式 index digest
- [step/W12] c1 [v2]: docker run <引擎> resolve add <repo>
- [step/SUB] c2a [v2]: resolve（不寫任何檔）：讀 version.toml
- [decision/D12] c4: 已接入 <repo>？
- [decision/D12] c5: metadata 有完成標記？
- [end_orange/O12] c6x [v2]: 1：@<tag> 與鎖定不同，請改用 upgrade
- [decision/D12] c5t: @<tag> 與鎖定不同？
- [step/SUB] c8: 否：續作，只做缺的步驟（不補刻意刪的檔）
- [step/SUB] c2b [v2]: 查 tag（預設最新正式版／@<tag>）與 index digest（--source 改來源）
- [other/IMG] c3: ghcr.io/<org>/<repo>-dist⏎（下游 image；多架構 index digest）
- [end_orange/O12] c2px [v2]: 1 + 6-3：私有 image，請指定 @<tag> 或提供 registry 憑證
- [decision/D12] c2pq [v2]: 私有 image 且未指定 @<tag> 且無憑證？
- [step/SUB] c2c [v2]: 否：算執行計畫（extract <repo>|<ref>；apply|yes；詢問清單留在引擎、apply 重算）
- [step/SUB] c2d [v2]: 產生輸入指紋（version.toml、version.local.toml、各 metadata、納管 dest、gen/.stamp 與各印記第一行、.tmp.* 清單、鎖定 digest、image ID、正規化 argv）
- [step/SUB] c2d2 [v2]: stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋（只傳協定內容）
- [entry/ENTRY] c9z: 續「add（1′）」頁：啟動器驗 vk-resolve → inspect → pull → extract → apply 前置
- [other/TEXT] _sp: 
- [end_ok/G12] c6: 0：已接入且完成，無變更
- [other/TEXT] cf_l: add 前 → 後（專案目錄，一格一檔；＋ = add 新增）
- [file/FGRP] cf0: add 前（install 後）
- [file/F12] cf0_0: justfile（＋import 行）
- [file/F12] cf0_1: .dockerignore（＋四行，含 log/）
- [file/F12] cf0_2: version.toml（vendor_kit 版本鎖定行）
- [file/F12] cf0_3: config.toml（keep／days 預設）
- [file/F12] cf0_4: 薄殼五檔：.gitignore、entry.just、vendor.just、log.sh、ci/check.sh
- [file/F12] cf0_5: gen/.stamp
- [file/F12] cf0_6: baseline/.gitkeep
- [file/F12] cf0_7: baseline/ vendor_kit/ config.toml（副本）
- [file/F12] cf0_8: baseline/ .vendor_kit.toml （metadata）
- [file/FGRP] cf1: add 後（＋ = 新增）
- [file/F12] cf1_0: ＋version.toml [tools] <repo> 版本鎖定行
- [file/F12] cf1_1: ＋cache/<repo>/（不進 git：files/、init.toml、just/）
- [file/F12] cf1_2: ＋gen/<repo>.stamp
- [file/F12] cf1_3: ＋初始檔（init.toml 的 dest；append 問後加）
- [file/F12] cf1_4: ＋baseline/<repo>/ + .vendor_kit.toml
- [file/F12] cf1_5: ＋gen/tools.just（每個 <ns>.just 一行 mod?）
- [other/LEGEND] p5b_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5b_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5b_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5b_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5b_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5b_lg5 [legend]: 白：步驟
- [other/LEGEND] p5b_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5b_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5b_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5b_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5b_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p5b_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5b_lgx_img [legend]: 紫：image
- [other/LEGEND] p5b_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5b_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5b_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5b_th: 本頁名詞
- [term/TERM_K] p5b_tk0: resolve／apply 兩段
- [term/TERM_V] p5b_tv0: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p5b_tk1: resolve 非 0
- [term/TERM_V] p5b_tv1: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p5b_tk2: stdout／stderr
- [term/TERM_V] p5b_tv2: resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀、先驗文法（不合 → 1 + 6-30），不把內容當指令執行；計畫／詢問清單是引擎內部資料，apply 自己重算，不經 stdout
- [term/TERM_K] p5b_tk3: 輸入指紋（算法）
- [term/TERM_V] p5b_tv3: resolve 對下列輸入依路徑排序串接後 sha256：version.toml、version.local.toml（缺記 -）、每個 metadata、state=managed／appended 的每個 dest、gen/.stamp 第一行、每個印記第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID（本機覆寫時）、本次 verb 正規化 argv（含 --dry-run／-y／CI 模式）；不含新版新增檔；apply 拿鎖後重算，不同（中間有人改了）→ 1 + 6-12「請重跑」
- [term/TERM_K] p5b_tk4: index digest／docker image inspect
- [term/TERM_V] p5b_tv4: 多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台
- [term/TERM_K] p5b_tk5: --local <tar>／.digest（Q26、v2.10 §3）
- [term/TERM_V] p5b_tv5: add --local 只收存在的 .tar（docker save 存的下游 image 檔；不是 → 1 + 6-24，橙；tag 形只有 bootstrap.sh 收）：先 docker load（失敗 → 1），讀同名 .digest 旁檔 = 正式 index digest 寫進 version.toml（旁檔缺／格式不合法／讀不到 → 1）；metadata 記 image ID ↔ digest 對照
- [term/TERM_K] p5b_tk6: 續作
- [term/TERM_V] p5b_tv6: add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補下游使用者刻意刪的檔
- [term/TERM_K] p5b_tk7: gen／mod?／recipe
- [term/TERM_V] p5b_tv7: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- [term/TERM_K] p5b_tk8: 6-38
- [term/TERM_V] p5b_tv8: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## edges
- ce1: c0(just vendor_kit add <repo>[@<t…) --(無標籤)--> c0l(建執行紀錄、寫 launcher_started（失敗 → …)
- ce1x: c0l(建執行紀錄、寫 launcher_started（失敗 → …) --失敗--> c0x(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- ce1l: c0l(建執行紀錄、寫 launcher_started（失敗 → …) --(無標籤)--> c1q(--local？)
- ce1q: c1q(--local？) --是--> c1t(是 → 值是存在的 .tar？)
- ce1tx: c1t(是 → 值是存在的 .tar？) --否--> c1x(1 + 6-24：--local 只收存在的 .tar)
- ce1t: c1t(是 → 值是存在的 .tar？) --是--> c1l(是：docker load <tar>)
- ce1lx: c1l(是：docker load <tar>) --失敗--> c1lx(1：docker load 失敗（印原文）)
- ce1d: c1l(是：docker load <tar>) --(無標籤)--> c1d(讀同名 .digest 旁檔 = 正式 index dige…)
- ce1dx: c1d(讀同名 .digest 旁檔 = 正式 index dige…) --缺／不合法--> c1dx(1：.digest 旁檔缺／格式不合法／讀不到)
- ce1c: c1d(讀同名 .digest 旁檔 = 正式 index dige…) --(無標籤)--> c1(docker run <引擎> resolve add <r…)
- ce1n: c1q(--local？) --否--> c1(docker run <引擎> resolve add <r…)
- ce2: c1(docker run <引擎> resolve add <r…) --(無標籤)--> c2a(resolve（不寫任何檔）：讀 version.toml)
- ce2b: c2a(resolve（不寫任何檔）：讀 version.toml) --(無標籤)--> c4(已接入 <repo>？)
- ce5: c4(已接入 <repo>？) --是--> c5(metadata 有完成標記？)
- ce7: c5(metadata 有完成標記？) --是--> c5t(@<tag> 與鎖定不同？)
- ce7b: c5(metadata 有完成標記？) --否--> c8(否：續作，只做缺的步驟（不補刻意刪的檔）)
- ce8: c5t(@<tag> 與鎖定不同？) --是--> c6x(1：@<tag> 與鎖定不同，請改用 upgrade)
- ce10: c4(已接入 <repo>？) --否--> c2b(查 tag（預設最新正式版／@<tag>）與 index d…)
- ce11: c8(否：續作，只做缺的步驟（不補刻意刪的檔）) --(無標籤)--> c2b(查 tag（預設最新正式版／@<tag>）與 index d…)
- ce3: c2b(查 tag（預設最新正式版／@<tag>）與 index d…) --查--> c3(ghcr.io/<org>/<repo>-dist （下游 …)
- ce4p: c2b(查 tag（預設最新正式版／@<tag>）與 index d…) --(無標籤)--> c2pq(私有 image 且未指定 @<tag> 且無憑證？)
- ce4px: c2pq(私有 image 且未指定 @<tag> 且無憑證？) --是--> c2px(1 + 6-3：私有 image，請指定 @<tag> 或提…)
- ce4: c2pq(私有 image 且未指定 @<tag> 且無憑證？) --否--> c2c(否：算執行計畫（extract <repo>|<ref>；a…)
- ce12: c2c(否：算執行計畫（extract <repo>|<ref>；a…) --(無標籤)--> c2d(產生輸入指紋（version.toml、version.lo…)
- ce12b: c2d(產生輸入指紋（version.toml、version.lo…) --(無標籤)--> c2d2(stdout vk-resolve/1：pull／extra…)
- ce13: c2d2(stdout vk-resolve/1：pull／extra…) --(無標籤)--> c9z(續「add（1′）」頁：啟動器驗 vk-resolve → …)
- cfe: cf0(add 前（install 後）) --(無標籤)--> cf1(add 後（＋ = 新增）)
- ce9: c5t(@<tag> 與鎖定不同？) --否--> c6(0：已接入且完成，無變更)

## terms
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- stdout／stderr: resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀、先驗文法（不合 → 1 + 6-30），不把內容當指令執行；計畫／詢問清單是引擎內部資料，apply 自己重算，不經 stdout
- 輸入指紋（算法）: resolve 對下列輸入依路徑排序串接後 sha256：version.toml、version.local.toml（缺記 -）、每個 metadata、state=managed／appended 的每個 dest、gen/.stamp 第一行、每個印記第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID（本機覆寫時）、本次 verb 正規化 argv（含 --dry-run／-y／CI 模式）；不含新版新增檔；apply 拿鎖後重算，不同（中間有人改了）→ 1 + 6-12「請重跑」
- index digest／docker image inspect: 多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台
- --local <tar>／.digest（Q26、v2.10 §3）: add --local 只收存在的 .tar（docker save 存的下游 image 檔；不是 → 1 + 6-24，橙；tag 形只有 bootstrap.sh 收）：先 docker load（失敗 → 1），讀同名 .digest 旁檔 = 正式 index digest 寫進 version.toml（旁檔缺／格式不合法／讀不到 → 1）；metadata 記 image ID ↔ digest 對照
- 續作: add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補下游使用者刻意刪的檔
- gen／mod?／recipe: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## xrefs
- bB: 見「add（1′）」頁
- c9z: 續「add（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


=== 附件 R：第十二版 codex 對本組頁的審查條目 ===
# 第十二輪 codex 審查 — 第 1 組（v1p2, v1p3, v1p3b, v1p3c, v1p4, v1p5, v1p5i, v1p5ccc, v1p5c, v1p5cw, v1p5cc）

來源：`r12_codex/out1.md`（codex exec，11 張縮圖 + brief1.txt 376 KB，exit=0）。以下為 codex 結論的逐條整理，未加審查者意見。codex 聲明：不重複附件 L 已列的機械 lint，不回報舊名／新名問題。

## 逐條

### v1p2
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `t_vl` | A | 「uninstall hash 相符才刪」與規格不符；`version.local.toml` 是自有覆寫檔，uninstall 應刪除，不以內容 hash 為條件。 | 必修 |
| 2 | `t_tmp`、`p2_tv`、`p2_tv16` | A | `.tmp.<verb>.<id>.toml` 的適用動詞漏掉 `dev`；規格已要求 `dev` 在第一個寫入前建立 `.tmp.dev.<id>.toml`。 | 必修 |
| 3 | `p2_tv18`「sync 豁免」 | A | 規格已撤回 sync 的執行位置豁免；工具 `_sync` 是先 `cd` 到專案根，因此 sync 仍須通過相同位置檢查。 | 必修 |
| 4 | `t_bl` | A | 「有衝突仍推」寫得過度絕對；合併衝突可推基準版，但 TOML／just 解析失敗時該檔基準版不得推進。 | 必修 |
| 5 | `p2_tv15` | A | 「install 只建 baseline/.gitkeep」漏掉 `baseline/vendor_kit/config.toml` 與 `baseline/.vendor_kit.toml` 的 install 責任。 | 必修 |
| 6 | `t_vl` | C | 同一格同時描述檔案格式、dev／undev／bootstrap 寫入、uninstall、CI 行為，超出「一格一件事」；建議拆成「格式／寫入者」與「CI、移除行為」。 | 選修 |
| 7 | 縮圖左欄目錄樹 | E | 內容密度過高，數個虛線子框與樹線貼近文字，尤其 `baseline/`、`gen/`、`log/` 區難以快速辨識父子關係。 | 選修 |

### v1p3
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `d4_7` | A | 工具 repo CI 的摘要漏列「特殊檔禁止」；規格要求 symlink、hardlink、特殊檔三類都由 `check.sh --dist` 擋下。 | 必修 |
| 2 | `p3_off` | A | 只寫 tar 形離線入口，漏掉 release 離線包另附 `local_bootstrap.sh` 便利包裝及其非契約定位；若本格宣稱完整描述 Release 資產，應補上。 | 選修 |
| 3 | `d4_1` | C | 一格同時承擔出貨範圍、展開位置、三類檔案禁止與換行規則，閱讀負擔過高；可將驗證規則移到 CI 格。 | 選修 |
| 4 | `p3_syncr` | C | 一格混合 `_sync` 內容、公開 recipe 相依、lint、載入限制與 fixture 驗收五件事，應至少拆成「工具契約」及「lint／限制」。 | 選修 |

### v1p3b
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `d1`「gen/.stamp = 引擎 ref？」 | A | 此判斷被畫成所有兩段動詞進 resolve 前的共同閘門，會讓 add、remove、upgrade、undev、uninstall、prune 也錯誤地走 6-1；它只屬 sync 相容性路徑。 | 必修 |
| 2 | `s2b` | A | 「查 registry 最新 tag／digest」被畫成每次 resolve 的固定步驟；remove、sync、undev、uninstall、prune 不查最新版，指定 `@<tag>` 也不得查。 | 必修 |
| 3 | `s3a → s3b` | A／B | `docker image inspect` 後缺「本機已有 → 跳過 pull」分支，現圖看起來無論結果都會執行 pull。 | 必修 |
| 4 | `s3b → s3c` | A | 圖把每筆 pull 都接到 create／cp；`pull` kind 只拉 image，只有 `extract` kind 才 create／cp，remove、uninstall、prune 等也可能完全沒有展開。 | 必修 |
| 5 | `s2z…s2c` | A | resolve 容器缺 `engine_exit`；規格要求每個 resolve、apply、單段容器結束前各自 append `engine_exit`。 | 必修 |
| 6 | `p3_ok` | B | `apply|no` 直接到綠色終點，漏掉啟動器仍須寫 `sync_fast_path`、`log_prune`、`launcher_exit`。 | 必修 |
| 7 | `s0a`、`s0b` | C | 建目錄、建檔、寫 `launcher_start` 與失敗處理塞在同一格；依一格一事標準至少應拆成「建紀錄檔」與「寫 launcher_start」。 | 必修 |
| 8 | `s4`、`s4z` | F | 先畫「docker run apply」，下一格才畫容器第一個動作 `engine_start`，一般讀者容易理解成 apply 已開始後才記錄；應將 `engine_start` 明確置於 apply 動作之前或容器框內最上方。 | 選修 |
| 9 | 縮圖主流程 | E | `s3b` 的成功主線與「失敗」支線在狹窄區域交會，且 `s4` 後的線折返，條件歸屬不夠直觀。 | 選修 |

### v1p3c
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `c_d → c_e → c_f` | A | 自身 CI 先正式 release，再跑完整驗收矩陣；規格要求必要驗收不得缺少才可出貨，不能在發布不可刪資產後才決定候選是否合格。應把候選驗收放在正式 release 前，release-test 可留在發布後。 | 必修 |
| 2 | `p3_accb_r12c2`（驗收 31） | A | config.toml 異常值清單漏掉「非整數」；規格明列 0、負數、非數字、非整數、重複、缺鍵、缺檔。 | 必修 |
| 3 | `p3_acc_r17c2`（驗收 18） | A | 敏感值驗收只寫輸出、metadata、log，漏掉進度檔；規格要求 metadata、執行紀錄、進度檔全部 grep 不到 token。 | 必修 |
| 4 | `k1f` | C | 同一終點同時放四種結束 1 與結束 3，沒有指出 3 的具體相容性原因；至少應把「結束 3」拆成獨立橙色終點。 | 選修 |
| 5 | 驗收矩陣 | F | 單頁放 35 條完整敘述，字級與行距已低於快速審閱用途；建議本頁只放分組索引，完整逐條矩陣另頁呈現。 | 選修 |

### v1p4
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `f_cfg --config_read--> m_log` | A | 資料流把 config.toml 直接送到 log 模組，像是由 log 模組解析設定；規格是引擎以 TOML parser 讀設定，再透過 `log_event()` 記 `config_read`。 | 必修 |
| 2 | `h3`「vendor.just…含 log.sh」 | A | `log.sh` 是獨立薄殼檔，由 vendor.just source／使用，不是包含在 vendor.just 內；目前文字會誤導檔案邊界。 | 必修 |
| 3 | `h0`、`h1`、`h2`、`h3`、`g1`、`g2` | B | 抽取結果沒有使用者 → 根 justfile → entry.just → vendor.just／tools.just → 工具 recipe 的連線；主機側載入關係因而成為六個懸空方塊。 | 必修 |
| 4 | `m_ver_u2_0`「進度日誌」 | A | 把所有進度日誌歸給 version 模組不完整：工具 add／upgrade 的 `[progress]` 在 metadata，由 baseline 模組維護；應畫出兩類落點或把責任抽成交易模組。 | 必修 |
| 5 | `run_cli` | F | 同一條線同時標「動詞、參數、協定」與反向的「結束碼、vk-resolve 清單」，但箭頭並非清楚的雙向箭頭；應拆兩條資料流或使用明確雙箭頭。 | 選修 |
| 6 | 引擎容器區 | E | 模組、最小單元與專案檔的連線高度集中在容器右側，數條線共用長水平路徑，難以判定各自端點；建議按讀寫檔案群重新對齊模組。 | 選修 |

### v1p5
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a0l` 之後至 `a6i/a6p` | A | 缺少引擎 LABEL 的最低介面版檢查；規格要求此檢查在任何上網／pull 之前，過舊須 3 + 6-18。 | 必修 |
| 2 | `a8z` | B／D | 跨頁出口只是普通文字，不是規定的白色虛線橢圓；與下一頁的虛線入口視覺語意不成對。 | 必修 |
| 3 | `a8e --否--> lp` 與其他失敗匯流 | B | 多個不同失敗先匯入共同收尾，再由 `launcher_exit` 無條件分岔到五個終點；圖上沒有保存「原失敗原因」的條件，出口歸屬歧義。 | 必修 |
| 4 | `a8ix` | F | 「本機無此 image」未標出 tag 形 `--local` 不得 pull，需回失敗；讀者需回看前文才能理解為何不是走一般 pull。 | 選修 |

### v1p5i
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a9e` | C | 一格同時寫「建／重寫薄殼、根 justfile、根 .dockerignore」，跨越多個判斷與詢問，與後續 install 分頁也重複；應只寫「執行 install，詳見跨頁」。 | 必修 |
| 2 | `a9es…a9q` | A | 單段 install 容器缺 `engine_exit`，成功及失敗都必須在容器結束前寫入。 | 必修 |
| 3 | `a9x` | D | 所有 install 失敗都畫紅色，但 install 可能因 6-4、6-28 等「需人處理」而結束，這些應是橙色；紅色只適用寫入、驗證等真正失敗。 | 必修 |
| 4 | `a9z` | B／D | 成功跨頁出口不是白色虛線橢圓，與下一頁入口語意不一致。 | 必修 |

### v1p5ccc
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a10re → a10d → a10a` | A | resolve 非 0、vk-resolve 驗證失敗、pull／extract 失敗都缺分支；現圖只能一路進 apply，與「resolve 非 0 不讀 stdout、不跑 docker／apply」矛盾。 | 必修 |
| 2 | `a10re0…a10re`、`a10ae0…a10ae` | A | resolve 與 apply 兩個容器都缺各自的 `engine_exit`。 | 必修 |
| 3 | `lx → a13`、`lx → a12` | B | `launcher_exit` 同時無條件連到成功與失敗終點，沒有保存 add 結果的條件，出口歧義。 | 必修 |
| 4 | `a10x` | F | 判斷放在 apply 後，文字卻叫「本次 add 失敗？」；應明確涵蓋 resolve、主機 docker、apply 任一階段，否則會被理解為只檢查 apply。 | 必修 |
| 5 | `a10f` | A | 檔案群把 version.toml 列在首項，容易暗示先寫；規格要求 version.toml 最後寫，建議在群組中直接標示「最後」。 | 選修 |

### v1p5c
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i4` 至 `i4_5b` | A | 先在專案內產生多個暫存檔，下一頁才建 `.tmp.install.<id>.toml`；規格要求所有可寫動詞在第一個寫入前先建進度檔。 | 必修 |
| 2 | `i4_5b` | A | 不論 config.toml 是否已存在都接著產 baseline 副本；修復型中 config.toml 已存在時規格要求不動，不能用目前內容偷偷建立／覆蓋基準版。 | 必修 |
| 3 | `i1e…i4z` | A | install 容器在本頁及後續兩頁都沒有明確的 `engine_exit` 收尾點。 | 必修 |
| 4 | `i4n` | F | 便條把「第一次失敗清除」與「修復失敗保留進度」混在一段，且未指出哪些寫入已發生；建議移到各自失敗出口。 | 選修 |

### v1p5cw
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i4bc` | A | 只在「第一次」建立 config.toml；規格要求修復型若 config.toml 缺失也要建立，存在才不動。 | 必修 |
| 2 | `i4bb` | A | baseline config 副本也只畫第一次建立；修復型補建缺失 config.toml 時必須同時建立相應基準版與 metadata。 | 必修 |
| 3 | `i4bc/i4bb/i4g` | A | 整頁未建立 `baseline/.vendor_kit.toml` 中 config.toml 的 `state=managed` metadata；下一頁只在 append `.dockerignore` 時寫該檔，無法涵蓋所有 install。 | 必修 |
| 4 | `i4c` | F | 「寫 version.toml」與括號「已有則不動」放在同格，動作與不動條件衝突；應先判斷缺檔，再只在缺檔分支寫。 | 選修 |
| 5 | `i5z` | B／D | 跨頁出口仍是普通文字，未採白色虛線橢圓。 | 必修 |

### v1p5cc
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i12`、`igq` | A | 詢問只畫「是／否」，漏掉無 tty／EOF／Ctrl-C 分支；規格要求無 tty／EOF 且無 `-y` → 1 + 6-4，Ctrl-C 中止且不記 declined。 | 必修 |
| 2 | `igs --是--> idl` | A | 根 `.dockerignore` 是 symlink 時直接收尾，沒有像 justfile 一樣印一次性遷移指示；頁首又宣稱 symlink 會「不寫只印指示」，流程與自身說明不一致。 | 必修 |
| 3 | `im` | C | 一格同時處理建檔、append、已含、拒絕、symlink 五種結果與輸出，違反一格一件事，且遮蔽各分支是否真的寫檔。 | 必修 |
| 4 | `idl → lp → lx` | A | install 單段容器刪進度檔後直接進啟動器收尾，缺少容器的 `engine_exit`。 | 必修 |
| 5 | `i5e` | B | 跨頁入口只寫「已寫 launcher_start」，沒有承接上一頁已寫的 `engine_start` 與仍在同一引擎容器內，容易被誤讀為新呼叫。 | 選修 |

## 沒問題的頁
（無 — 11 頁 codex 都列出至少一條。）

## 統計
- 共 58 條：必修 42、選修 16。
- 類別分布：A 31、A／B 1、B 5、B／D 3、C 7、D 1、E 3、F 7。
- 反覆出現的主題：容器缺 `engine_exit`（v1p3b、v1p5i、v1p5ccc、v1p5c、v1p5cc）；跨頁出口未用白色虛線橢圓（v1p5、v1p5i、v1p5cw）；`launcher_exit` 無條件分岔至多個終點（v1p5、v1p5ccc）；install 進度檔／config baseline 責任（v1p2、v1p5c、v1p5cw）。

## 總評（codex 原文）
本組頁面目前仍有多項會改變實作行為的必修錯誤，尤其通用 resolve/apply 流程、執行紀錄收尾、install 進度檔順序與 config baseline；修正前不宜交給使用者看。
# r12 codex 審查 — 第 2 組（v1p5b, v1p5bcc, v1p5bc, v1p6, v1p6cc, v1p6c, v1p7, v1p7c, v1p7ccc, v1p7cc, v1p7cccc, v1p7b）

來源：`r12_codex/out2.md`（codex exec, gpt-5.6-sol, 177,508 tokens；附件 S 為完整 spec_0_9.md，未縮減）。以下只整理 codex 原文，不含整理者意見。codex 聲明：未回報名詞新舊問題、未重複機械 lint。

## 共通問題（跨多頁）

| # | 頁 id | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|---|
| G1 | v1p5b, v1p5bcc, v1p5bc, v1p6cc, v1p6c, v1p7c, v1p7ccc, v1p7cc, v1p7cccc | 各頁 `engine_start` 至後續流程 | A | 每個 resolve／apply 容器結束前都應寫 `engine_exit`，圖上完全缺少，容易誤解成只有整次呼叫的 `launcher_exit` | 必修 |
| G2 | v1p5b, v1p5bcc, v1p5bc, v1p6, v1p6cc, v1p6c, v1p7c, v1p7ccc, v1p7cccc | `lp`、`lx` 與所有終點 | B／E | 所有成功與錯誤路徑先匯入同一 `launcher_exit`，再由同一格同時連到多個結果，沒有保存「本次是哪個結果」，讀者無法判斷實際出口 | 必修 |
| G3 | v1p5bcc, v1p6c, v1p7ccc | docker `create → cp → rm` | A | 只替 pull 畫失敗出口，沒有表現 create、cp、rm 或暫存目錄處理失敗均應停止並回 1 | 必修 |
| G4 | v1p5b, v1p5bcc, v1p6, v1p6cc, v1p6c, v1p7c, v1p7ccc, v1p7cc, v1p7cccc | 頁首流程帶與名詞表 | F | 每頁大量重複整套共通名詞與版本沿革，主流程反而只佔小部分，與「字要少、一般人看得懂」不符；建議改成共通名詞頁引用，本頁只保留實際出現且需解釋者 | 選修 |

## v1p5b

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `c1l`、`c1d` | A | `docker load` 失敗，以及 `.digest` 缺失、格式不合法或讀取失敗都沒有失敗分支，卻直接進 resolve | 必修 |
| 2 | `c2d`「產生輸入指紋」 | A | 列出的指紋輸入不完整，規格另含 version.local.toml、各 stamp 第一行、`.tmp.*` 清單、正規化 argv、CI／`-y`／dry-run 等，現圖會讓人實作出不完整指紋 | 必修 |
| 3 | `c2c`「產生執行計畫（要拉的 image@digest、mount、apply 與否）」 | C | 同格同時處理 pull／mount／apply 三類輸出，違反一格一件事 | 選修 |
| 4 | `cf0_7`「baseline/.gitkeep」 | A | 規格只要求 install 建空的 baseline/，沒有要求 tracked 的 `.gitkeep`，而 metadata／config 基準副本已有實體檔可承載目錄 | 必修 |
| 5 | `cf0_4`「version.local.toml（--local 時）」 | A | 這是 add 前的 install 後狀態，但 `add --local` 不寫 version.local.toml；只有 bootstrap 的 local 形可能留下它，現文字把兩者混為一談 | 必修 |

## v1p5bcc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `c10` | A | apply 應讀完整 `/dist/vk-resolve` 並驗原 argv 與計畫一致，圖上只畫重驗指紋，漏掉計畫／argv 一致性檢查 | 必修 |
| 2 | `c12` | A | dest 合法性規則漏畫「父目錄不得經 symlink」及 src 正規化不得越出 dist | 必修 |
| 3 | `c12b`／`c12br` | A | 命名空間撞名漏掉根 justfile 的 alias，規格要求以 dump JSON 檢查 recipe／module／alias | 必修 |
| 4 | `c13 --dry-run?` 至 `c13z` | B／E | `c13` 到跨頁出口的線未標「否」，與另一條「是」分支並存，分支語意不完整 | 必修 |
| 5 | `c12`、`c12b` | C | 菱形內同時寫「相同」前提、檢查對象及「任何寫入前檢查」，應把前一步結果放在線標籤，菱形只保留單一問題 | 選修 |

## v1p5bc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `c15a` | A | `[progress]` 除 state 外還必須含 started、verb、id、done、pending，圖和檔案框只表現 `state=in-progress`，不足以支援恢復 | 必修 |
| 2 | `c21b` | C | 同格寫 source、最後合併版本與 local_image_id 三件事；可拆成「寫來源／離線對照」與後續 metadata 收尾 | 選修 |
| 3 | `c21c` | C | 同格同時寫 state、declined_hash、lines 三類狀態，且每類適用條件不同 | 選修 |
| 4 | `ce38`「失敗（任一步）」 | B | 失敗線只從最後寫 version.toml 的格子拉出，視覺上並不能代表前面任一步失敗 | 必修 |
| 5 | `c22`、`c23` | A | 規格不變量要求 `gen/tools.just` 與 cache 在同一 apply 內原子替換，圖只寫「重生」而沒有「原子替換」，容易被實作成直接覆寫 | 必修 |

## v1p6

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `n0l → n1` | A | sync 也適用「只能在專案根執行」，圖未畫專案根檢查或引用共通前置頁 | 必修 |
| 2 | `n3` | F | 「缺 gen/.stamp → 改讀薄殼首行 engine=」沒有說清楚是用薄殼首行做相容／舊版本判定，而不是把缺失 stamp 當成已相符；一般讀者可能誤判快路徑條件 | 必修 |
| 3 | `n1x` | D | 把「pull 失敗」與「local image ID 不符」合成同一紅色終點尚可，但前者應明列 6-24／6-31，後者應說明本機覆寫已失效；目前資訊不足以採取修復動作 | 必修 |
| 4 | `nq` | C | 單一判斷格同時檢查 stamp、tools.just、交易檔、參數及 CI 五種條件；至少應以「快路徑條件全部成立？」配合旁邊規則表，不要在流程格中塞多項判斷 | 選修 |

## v1p6cc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `t3 → t4` | A | 規格要求 path 覆寫仍檢查完成標記與基準版落後，圖有做到，但沒有畫出 metadata 檔案失蹤／不可解析的失敗處理 | 必修 |
| 2 | `t2q` | A | 「版本變動那次」在 cache 缺或印記不符時直接走 materialize，卻沒有在本頁計畫中明示 apply 後必做全檔驗證；需把 verify 要求放進待辦，否則跨頁容易遺失 | 必修 |
| 3 | `z0` | C | 同格同時彙整 pull、重裝、重生 tools.just 並判斷空清單，應拆成「完成計畫」與「計畫為空？」 | 選修 |
| 4 | `z1b → mb／lp` | E | 同一輸出格一條無標籤線往跨頁、一條標 `apply|no` 往結束，`apply|yes` 只寫在跨頁文字中，建議兩條線明標 yes／no | 必修 |

## v1p6c

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `m2b → m3` | A | apply 漏畫「原 argv 與 resolve 計畫一致」檢查，只有指紋重驗 | 必修 |
| 2 | `m3vd` | A | `sync --verify` 與 CI 為真也要求全檔驗證，但此頁只問「版本變動的那次？」；因此 `--verify`／CI 的 apply 路徑會被畫成不驗 | 必修 |
| 3 | `m3vn` | A | 在剛完成 materialize 並寫印記後驗證不符，應視為 fetch／寫入／驗證失敗；「再重裝一次 + warn 後成功」沒有終止條件，可能形成無限或掩蓋損壞 | 必修 |
| 4 | `m3` | C | 同格同時表示 materialize 與「每個待辦工具」迴圈，卻沒有「還有工具？」分支，無法看出多工具逐一處理 | 必修 |

## v1p7

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a4a`、`a4b` | A | 每個 check.sh 內動詞都有自己的執行紀錄，圖卻說「已寫 launcher_start」如同整個 check.sh 共用一檔，與一次啟動器呼叫一檔不符 | 必修 |
| 2 | `a4q` | A | 把 CI 第一關簡化成只判 baseline 落後，漏掉薄殼不符、未完成接入、local 覆寫、未完成交易等 sync 失敗出口；若此頁宣稱「完整流程」，應畫聚合失敗出口或明確引用 sync 頁 | 必修 |
| 3 | `a4c → a4e2` | A | verify、dry-run、工具測試、專案測試都可能失敗或回 2／3，圖卻只有直達 merge 的成功線，缺第一個失敗即停止的分支 | 必修 |
| 4 | `a8` | C | 「主線 CI 與 PR 分支 CI 都綠後才 merge」把兩個條件與 merge 動作塞在終點，應先判斷門檻再畫 merge | 選修 |
| 5 | `a4r` | F | 「一行改動本身不可能出錯」過度絕對，該行仍可能不合法或指向不存在的 ref；應改成「只看一行 diff 不足以證明升級可用」 | 必修 |

## v1p7c

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | 頁首 `uB` 與整頁流程 | A | 頁首宣稱支援不帶 repo、包含 vendor_kit 自身，但流程只描述單一工具 `<repo>`；自身升級及多工具完整預檢完全沒有分流，範圍與內容矛盾 | 必修 |
| 2 | `b2` | A | 規格規定 conflicts 中的檔案失蹤也不算已解；菱形只問是否仍含標籤，檔案失蹤會走「否」繼續，與旁註及規格矛盾 | 必修 |
| 3 | `b7z` | A／B | CI 未指定 tag 時目標等於現鎖定版，若無待合併應輸出 `apply|no`／0；圖卻仍接指紋、docker 與 apply 前置頁 | 必修 |
| 4 | `b7q` | A | 只有「查 registry 最新版」分支需要列舉憑證，指定 tag 或待合併仍可能在 pull 時因認證失敗；本格文案把「registry 查詢憑證」與「docker pull 認證」混成同一概念 | 必修 |
| 5 | `b7s2` | C | 同格把目標 ref 與指紋輸出混在一起，可改成單一「輸出 vk-resolve 計畫」並在名詞表列內容 | 選修 |

## v1p7ccc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `b10b → b10d` | A | 同 add 頁，漏掉 apply 對原 argv／計畫一致性的檢查 | 必修 |
| 2 | `b10n` | A | 命名空間撞名規則漏 alias；其名詞表還寫成「add 回 1」，本頁應是 upgrade 同樣回 1 | 必修 |
| 3 | `b10c` | C | 「逐檔判斷 → 詢問清單」同格包含判定與產生詢問兩件事 | 選修 |
| 4 | `b11 → b11z` | B／E | 往跨頁出口的線未標「否」，同時另有「是」線往結束，閱讀歧義 | 必修 |
| 5 | `b12`（在 `b10c` 後） | A | 流程已先「逐檔判斷／詢問清單」再判 CI；規格要求 CI 需改 tracked 檔時列清單退出且不詢問，圖中文字容易理解成已實際詢問；應明確寫「只計算會問項目，不發問」 | 必修 |

## v1p7cc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `b14q1 → b14q1b → b14q2 → b14q3 → b14q4` | A | 這串判斷不是互斥狀態機：append 檔可能先被一般文字檔或「兩邊都改」分支攔走，得到錯誤問句與合併方式 | 必修 |
| 2 | `b14q1b` 否分支接 `b14q2` | A | 二進位／symlink 若下游使用者改過，規格是保留並 warn，圖卻會落入「兩邊都改 → 三方合併」 | 必修 |
| 3 | 整個逐檔迴圈 | A | 漏畫 D 缺 → state=deleted、N 缺 → 保留 warn、B==N／D==N → 不動、declined_hash 相同不再問、unmanaged／declined 等分支；不能只靠另一頁表格補救，因本頁自稱實際 apply 流程 | 必修 |
| 4 | `b14q3` | A | 只問「找到上次插入的行？」但規格需區分唯一命中、零命中、多處命中；只有唯一命中才可詢問替換 | 必修 |
| 5 | `b14q4` | A | 新版新增但 dest 已有同名檔時應直接不納管並印 6-11，不應先問建檔 | 必修 |
| 6 | 五個 `b14q*` | C | 每個菱形同時放條件與要顯示的問句，應讓菱形只判斷情況，問句另成步驟 | 選修 |
| 7 | `b14x` | C | 同格包含換版、三方合併、append 替換、建新檔四種互異動作，錯誤與結果也不同 | 必修 |
| 8 | `b14pc` | C | 「留原檔」與「記 conflicts」是兩件事，且後者是 metadata 寫入；建議拆開以清楚表現解析失敗時 baseline 不推 | 選修 |

## v1p7cccc

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `b15b` | A | 即使某檔解析失敗、該檔 baseline 留舊版，格子仍把整體「最後合併版本 = 目標版」寫成無條件成立；需說明 source 與逐檔 baseline／conflicts 的關係，避免恢復時誤判 | 必修 |
| 2 | `b18` | A | 終點寫「baseline 已在目標版」，但解析失敗的檔依規格不得推 baseline，與本頁 `b15a` 自相矛盾 | 必修 |
| 3 | `b16b → b16q` | A | 圖先刪進度日誌才判 conflicts；若 conflicts 是 apply 的最終結果，至少應先確定 metadata、version.toml、衝突碼與摘要均已成功持久化，再刪 `[progress]`，目前順序看不出故障恢復邊界 | 必修 |
| 4 | `b16` | A | 有待合併時 version.toml 已是目標 B，圖說「不動」正確，但仍畫一條「寫」到 `b16f`，會被理解成仍重寫檔案 | 必修 |
| 5 | `b18r` | F | 「衝突 2 > 有新版 2」把兩種同碼狀態寫成優先序，但實際彙總需要保留不同訊息，建議直接寫「兩者皆回 2，訊息全部列出」 | 選修 |

## v1p7b

| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `p7b_tv0` | A | 名詞表宣稱逐檔判斷「只對 state=managed」，但 append 更新必須處理 state=appended，新檔／deleted／declined 也有各自規則 | 必修 |
| 2 | `c_r4c2` | A／F | 同時寫「之後不再問」與「目標新版再次更新時重新詢問」互相矛盾；應改成「同一 declined_hash 不再問，N 的 hash 改變後再問」 | 必修 |
| 3 | `c_r3c0` | A | 「兩邊都改」未排除二進位／symlink，容易與 `c_r7` 衝突；應明列此列只適用可文字合併的 managed 檔 | 必修 |
| 4 | `c_r4c1`／`c_r4c2` | A | 「已有同名 → 不納管」沒有標出 state=unmanaged 與 6-11，狀態機資訊不完整 | 必修 |
| 5 | `c_r6c1` | C | 同格同時包含比對規則、判定與詢問動作；應把「唯一命中？」與「問後替換」拆開 | 選修 |
| 6 | `cx2`、`cx3` | B／D | 兩個跨頁出口只是普通文字，沒有使用規定的白虛線橢圓；`cx2` 又是結束碼 2 卻不是橙色終點 | 必修 |
| 7 | `c_m2 → c_h2` | B／E | 流程箭頭直接指到表頭「結果」，沒有連到任何實際資料列或明確的表格入口，屬語意懸空 | 必修 |
| 8 | 逐檔判斷表 | E | 表格字量過密，長句跨多行且結果欄擠滿規則，縮圖尺寸下難以辨識；建議把每列壓成「條件／動作／狀態」短句，把細節移至名詞表 | 選修 |

## 沒問題的頁

無——本組 12 頁 codex 每頁都有列條目。

## 統計

共通 4 條（必修 3、選修 1）＋ 逐頁 63 條（必修 49、選修 14）。逐頁類別分布（複合類別各計一次）：A 37、B 6、C 14、D 2、E 5、F 4。

## 總評（codex 原文）

本組頁面目前仍有數個會導致錯誤實作的流程缺口，尤其是 `engine_exit`、sync 驗證條件、upgrade 逐檔狀態機與跨頁出口，修正前不宜交給使用者看。


=== 附件 L：機械 lint（本組頁）===
[termcov] v1p2 t_di: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_di: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_di: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_ver: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_ver: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_ver: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_vl: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_vl: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_log: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 t_tmp: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 p2_jf_n: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p2 p2_sh_n: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3 d4_1: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3 p3_initf_r1c2: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b s0b: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b s0c: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b s1: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b s3b: 「6-31」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b s3bx: 「6-24」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_env: 「6-4」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_self: 「6-2」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_self: 「6-2b」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_lock: 「6-12」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_lock: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_vkr: 「6-30」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_two: 「6-26」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_two: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_compat: 「6-36」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3b p3_compat: 「6-10」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k0: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1f: 「6-1」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1f: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1f: 「6-5」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1f: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1g: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k1g: 「6-19」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k3g: 「6-6」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c k3g: 「6-8」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c p3_c2: 「6-25」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c p3_acc_r2c2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c p3_acc_r5c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c p3_acc_r7c2: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3c p3_acc_r7c2: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r0c2: 「6-1」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r4c2: 「6-10」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r5c2: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r6c2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r7c2: 「6-19」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r7c2: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r8c2: 「Renovate」（Renovate）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r9c1: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r9c2: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r11c2: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r11c2: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r11c2: 「apply」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r15c2: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_acc_r15c2: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r6c2: 「6-9」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r7c2: 「6-4」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r10c2: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r12c1: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r13c1: 「6-38」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r15c2: 「.tmp.upgrade」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p3d p3d_accb_r16c2: 「.tmp.remove」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h4: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h4_u2_0: 「resolve」（resolve／apply）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 g_eng: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h2: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h_vk: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h_vk: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h_vk: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h_vk: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 h_vk: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_schema_u0_1: 「6-19」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_prog_u0_1: 「6-26」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_prog_u0_1: 「flock」（flock）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_prog_u1_0: 「6-12」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_shell_u1_0: 「6-28」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p4 m_shell_u1_1: 「gen/.stamp」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5 pend: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5 pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5i pend: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5i pend: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5i pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5i a9c: 「.tmp.install」（.tmp.*）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5i a9h: 「6-4」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5ccc pend: 「6-18」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5ccc pend: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5ccc pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5c pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5c i4: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cw pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc pend: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc i12: 「6-20」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc igq: 「6-34」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc igyf: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5cc igm: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5b pend: 「flock」（flock）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5b cf0_1: 「log/」（log/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5b cf0_3: 「config.toml」（config.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5b cf0_4: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5b cf0_6: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
ERROR: Reconnecting... 2/5
ERROR: Reconnecting... 3/5
ERROR: Reconnecting... 4/5
ERROR: Reconnecting... 5/5
warning: Falling back from WebSockets to HTTPS transport. stream disconnected before completion: websocket closed by server before response.completed
codex
以下依規格 v3.5、附件 P 與縮圖核對；附件 L 已列的機械 lint 不重複。執行紀錄依新版圖例約定審查，不要求逐格補 `engine_exit`／`launcher_exit`。

## 附件 R 逐條核對

### v1p2

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `t_vl2` 已明載 uninstall 直接刪 `version.local.toml`，不再比 hash。 |
| 2 | 已修 | `t_tmp` 與進度檔範例已納入 `dev`／`.tmp.dev.<id>.toml`。 |
| 3 | 已修 | 「sync 豁免」已移除；`_sync` 改為先 `cd` 專案根。 |
| 4 | 已修 | `t_bl` 已補「衝突仍推；解析失敗的檔不推」。 |
| 5 | 已修 | 已列 `baseline/vendor_kit/config.toml` 與 `baseline/.vendor_kit.toml` 的 install 責任。 |
| 6 | 已修 | `t_vl` 與 `t_vl2` 已拆成格式／寫入者與 CI／移除規則。 |
| 7 | 未修 | 左欄仍非常密集，`baseline/`、`gen/`、`log/` 的樹線與多層框仍難快速辨識。 |

### v1p3

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `d4_7` 已列 symlink、hardlink、特殊檔三類禁止。 |
| 2 | 已修 | `p3_off` 已補 `local_bootstrap.sh` 並標明便利包裝、非契約入口。 |
| 3 | 已修 | `d4_1` 已縮成出貨與展開責任，驗證規則移往 CI 格。 |
| 4 | 已修 | `_sync` 工具契約與 lint／限制已拆成 `p3_syncr`、`p3_syncl`。 |

### v1p3b

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `s1` 已註明非 sync 跳過 `d1`，6-1 不再成為所有兩段動詞的共同閘門。 |
| 2 | 改壞 | `s2b` 雖不再涵蓋所有動詞，卻把單段 `update` 畫在 resolve 內，且未排除 CI 模式；仍會導出錯誤編排。 |
| 3 | 已修 | 已有「本機有 → 跳過 pull」的明確分支。 |
| 4 | 已修 | `s3c` 已限定「只有 extract kind」才 create／cp。 |
| 5 | 已修 | 依本版圖例約定②，引擎格已隱含容器開始與結束事件。 |
| 6 | 已修 | `apply|no` 說明已補快路徑事件，終點依圖例約定①完成紀錄收尾。 |
| 7 | 已修 | trace id、建紀錄、寫 launcher 事件已拆成 `s0a`、`s0b`、`s0c`。 |
| 8 | 已修 | 引擎格與圖例約定②已清楚表達先記開始事件才執行。 |
| 9 | 已修 | pull 成功／失敗與 extract 主線已重新分開，條件歸屬可辨。 |

### v1p3c

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 已改成候選 tag → release-test／完整驗收 → 正式 release。 |
| 2 | 已修 | 驗收 31 已補「非整數」。 |
| 3 | 已修 | 私有 registry 驗收索引已包含進度檔。 |
| 4 | 已修 | 結束 1 與結束 3 已拆為 `k1f`、`k1g`。 |
| 5 | 已修 | 本頁只留分組索引，35 條移至 v1p3d。 |

### v1p4

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `config.toml` 先流向 schema 模組，schema 再傳 `config_read` 至 log。 |
| 2 | 已修 | `log.sh` 已畫成獨立檔，並由 `vendor.just` source。 |
| 3 | 已修 | 使用者、根 justfile、entry.just、vendor.just／tools.just、工具命名空間均已有連線。 |
| 4 | 已修 | 交易責任已集中在 progress；工具 metadata `[progress]` 仍由 initfile／baseline 路徑承接。 |
| 5 | 已修 | 呼叫資料與回傳結果已拆成 `run_cli`、`ret_cli` 兩條線。 |
| 6 | 未修 | 容器右側仍有多條長距離共線與折返，模組到檔案的端點需沿線追蹤才能辨識。 |

### v1p5

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 改壞 | 已新增 LABEL 最低介面版檢查，但放在 inspect／pull 之後；規格要求最低介面版檢查先於任何上網。 |
| 2 | 已修 | `a8z` 已改為白色虛線橢圓跨頁出口。 |
| 3 | 已修 | 不再經共同 launcher 格無條件分岔；各失敗原因保留自己的終點。 |
| 4 | 已修 | `a8ix` 已明載 tag 形 `--local` 不得 pull。 |

### v1p5i

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `a9e` 只表達執行 install；檔案結果另以檔案群呈現。 |
| 2 | 已修 | 依圖例約定②，引擎格隱含完整開始／結束事件。 |
| 3 | 已修 | 已以 `a9h` 分流需人處理的橙色出口與真正失敗的紅色出口。 |
| 4 | 已修 | `a9z` 已使用白色虛線橢圓。 |

### v1p5ccc

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 改壞 | 已補 resolve／文法、docker、apply 失敗分支，但全部匯成結束 1；bootstrap.sh 應原樣傳出 add 的 2／3。 |
| 2 | 已修 | resolve、apply 引擎格依圖例約定②各自隱含完成事件。 |
| 3 | 已修 | 已移除共同 launcher 格的無條件成功／失敗分岔。 |
| 4 | 已修 | 現在分別判斷 resolve＋文法、docker 段、apply 結果。 |
| 5 | 已修 | `version.toml` 已明標「最後寫」。 |

### v1p5c

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `.tmp.install.<id>.toml` 已移到所有暫存寫入之前。 |
| 2 | 已修 | config 存在時直接略過；缺檔才產 config 與其基準版。 |
| 3 | 已修 | 同一 docker run 的結束事件由圖例約定②涵蓋。 |
| 4 | 已修 | 第一次／修復型失敗結果已移往 v1p5cw 的明確失敗出口。 |

### v1p5cw

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 改為判斷「本次是否因原本缺檔而產生 config」，第一次與修復型皆適用。 |
| 2 | 已修 | 補建 config 時會一併建立基準版副本。 |
| 3 | 已修 | 已新增 `baseline/.vendor_kit.toml` 的 `state=managed` 寫入。 |
| 4 | 已修 | 已先判斷 `version.toml` 缺失，再只於「是」分支寫入。 |
| 5 | 已修 | `i5z` 已改為白色虛線橢圓。 |

### v1p5cc

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 兩問句旁已有無 tty／EOF 標示，圖例補充 Ctrl-C 中止且不記 declined。 |
| 2 | 已修 | `.dockerignore` symlink 分支已新增一次性遷移指示。 |
| 3 | 已修 | 建檔、symlink、已含、詢問、append／拒絕均已拆開。 |
| 4 | 已修 | 容器結束事件由圖例約定②涵蓋。 |
| 5 | 未修 | `i5e` 仍只寫「已寫 launcher_started」，未明說承接同一 install 容器；跨頁仍可能被誤認為新呼叫。 |

### v1p5b：附件 R 第二組中適用本頁的條目

| R項 | 狀態 | 核對結果 |
|---|---|---|
| G1 | 已修 | resolve 引擎格依新版圖例約定②隱含開始與結束事件。 |
| G2 | 已修 | 本頁已移除共同 launcher 收尾格的無條件多出口。 |
| G4 | 未修 | 頁首沿革、重複名詞與共通規則仍占大量版面，主流程辨識度偏低。 |
| 1 | 已修 | `docker load` 與 `.digest` 均已有獨立失敗出口。 |
| 2 | 已修 | `c2d` 已列 version.local、metadata、stamp、`.tmp.*`、image ID、argv／CI／`-y`／dry-run 等輸入。 |
| 3 | 已修 | `c2c` 已收斂為單一「算執行計畫」動作，詳細輸出另由 `c2d2` 表達。 |
| 4 | 已修 | 現行定案明確接受 `baseline/.gitkeep`；圖面與本版規格一致。 |
| 5 | 已修 | add 前狀態不再宣稱 `add --local` 會寫 version.local.toml。 |

附件 R 本組相關共 66 條：已修 59、未修 4、改壞 3。

## 本輪新發現

以下不重複附件 L。

| 頁 id | 元件 id／引文 | 類別 | 說明 | 必修／選修 |
|---|---|---|---|---|
| v1p2 | `p2_ver_n`「第 1 行 = 唯一版本鎖定行」 | A | 規格明定第一行只是 install 的寫出慣例、不是契約；契約是頂層 `vendor_kit` 位於 `[tools]` 前且符合正規形。 | 必修 |
| v1p3b | `s2b` | A | `update` 是單段動詞，不應畫成 `resolve` 容器內的步驟；CI 模式下 upgrade 未指定 tag 也不得查最新版。 | 必修 |
| v1p3b | `p3_fast` 的 `--local` 判別 | A | 仍採「含 `/` 或 `.tar` 即檔案」及「用 `./`／完整 ref 消歧」的舊規則；v3.5 必須依 `.tar` → 同名檔消歧 → tag 的順序判定。 | 必修 |
| v1p4 | `m_res_u1_1`「token／逾時」 | A／F | pull timeout 是啟動器責任且不轉發引擎；與 registry 查詢 token 放在 resolve 模組會誤導責任邊界。 | 必修 |
| v1p5 | `a8q`、`a8e`、`a8t` | A | bootstrap `--local` 仍以「含 `/`」先判檔案，並以「本機有同名 image」判 6-37；正確條件是非 `.tar`、含 `/`、且存在同名檔，與 image 是否存在無關。 | 必修 |
| v1p5 | `a8p` | A | LABEL 檢查應在可能的 `docker pull` 前；現圖只有 image 到本機後才檢查，斷網時可能先回 pull 失敗而不是 3＋6-18。 | 必修 |
| v1p5i | `a9q`、`a9hx`、`a9x` | A | install 非 0 只畫兩個結束 1，漏掉 install 回 3 時 bootstrap.sh 必須原碼傳出 3。 | 必修 |
| v1p5ccc | `a10rq`／`a10d`／`a10x` → `a12` | A | resolve 或 apply 回 2／3 時被統一改成 1；bootstrap 逐 `-t` 中止正確，但結束碼必須保留失敗步驟原碼。 | 必修 |
| v1p5c | `i0l → i2` | A | 自己執行 install 時先嘗試建立執行紀錄、後檢查是否在 git repo；非 git 目錄無合法紀錄落點，應先做主機 git 前置檢查，再建紀錄。 | 必修 |
| v1p5cc | `igq0`「已含這四行？」 | A | 這是全有／全無判斷；若只已有其中幾行，後續 append 四行可能重複。應逐行辨識，只記實際新增的行。 | 必修 |
| v1p3d | 驗收 18 `p3d_acc_r17c2` | A | 詳表漏驗 `registry_query` URL 必須移除 userinfo；只有「grep 不到 token」不足以涵蓋 §7.4-18。 | 必修 |
| v1p3d | 驗收 19 `p3d_accb_r0c2` | A | 漏掉故意修改 `.dockerignore` 其中一行後，uninstall 應跳過該行並 warn、其餘原文相同行仍刪除的驗收。 | 必修 |
| v1p4 | 引擎模組鏈 `m_res → m_schema → m_prog → …` | F | 雖以資料名稱標線，整體仍像固定執行順序；架構頁應避免讓八模組被理解為每個動詞都依序經過全部模組。 | 選修 |
| v1p3d | 全頁 | F | 作為「逐條詳表」，多列已壓縮掉規格中的關鍵驗證子條件；建議保留可判定 pass/fail 的完整條件，否則改名為驗收摘要。 | 選修 |

## 逐頁結論

- v1p3：未發現附件 R 以外的新問題。
- v1p3c：未發現附件 R 以外的新問題。
- v1p3b、v1p5、v1p5i、v1p5ccc、v1p5c、v1p5cc 仍有會改變實作行為的必修問題。
- v1p2、v1p4、v1p3d 另有契約文字或架構表達問題。
- v1p5b 本身的舊問題大致已修，但版面仍過度重複共通資訊。

總評：本組修正幅度很大，但 `--local` 判別、最低介面版檢查順序、bootstrap 原碼傳出及 install 前置順序仍可能導致錯誤實作，目前尚不能交給使用者看。
tokens used
196,200
以下依規格 v3.5、附件 P 與縮圖核對；附件 L 已列的機械 lint 不重複。執行紀錄依新版圖例約定審查，不要求逐格補 `engine_exit`／`launcher_exit`。

## 附件 R 逐條核對

### v1p2

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `t_vl2` 已明載 uninstall 直接刪 `version.local.toml`，不再比 hash。 |
| 2 | 已修 | `t_tmp` 與進度檔範例已納入 `dev`／`.tmp.dev.<id>.toml`。 |
| 3 | 已修 | 「sync 豁免」已移除；`_sync` 改為先 `cd` 專案根。 |
| 4 | 已修 | `t_bl` 已補「衝突仍推；解析失敗的檔不推」。 |
| 5 | 已修 | 已列 `baseline/vendor_kit/config.toml` 與 `baseline/.vendor_kit.toml` 的 install 責任。 |
| 6 | 已修 | `t_vl` 與 `t_vl2` 已拆成格式／寫入者與 CI／移除規則。 |
| 7 | 未修 | 左欄仍非常密集，`baseline/`、`gen/`、`log/` 的樹線與多層框仍難快速辨識。 |

### v1p3

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `d4_7` 已列 symlink、hardlink、特殊檔三類禁止。 |
| 2 | 已修 | `p3_off` 已補 `local_bootstrap.sh` 並標明便利包裝、非契約入口。 |
| 3 | 已修 | `d4_1` 已縮成出貨與展開責任，驗證規則移往 CI 格。 |
| 4 | 已修 | `_sync` 工具契約與 lint／限制已拆成 `p3_syncr`、`p3_syncl`。 |

### v1p3b

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `s1` 已註明非 sync 跳過 `d1`，6-1 不再成為所有兩段動詞的共同閘門。 |
| 2 | 改壞 | `s2b` 雖不再涵蓋所有動詞，卻把單段 `update` 畫在 resolve 內，且未排除 CI 模式；仍會導出錯誤編排。 |
| 3 | 已修 | 已有「本機有 → 跳過 pull」的明確分支。 |
| 4 | 已修 | `s3c` 已限定「只有 extract kind」才 create／cp。 |
| 5 | 已修 | 依本版圖例約定②，引擎格已隱含容器開始與結束事件。 |
| 6 | 已修 | `apply|no` 說明已補快路徑事件，終點依圖例約定①完成紀錄收尾。 |
| 7 | 已修 | trace id、建紀錄、寫 launcher 事件已拆成 `s0a`、`s0b`、`s0c`。 |
| 8 | 已修 | 引擎格與圖例約定②已清楚表達先記開始事件才執行。 |
| 9 | 已修 | pull 成功／失敗與 extract 主線已重新分開，條件歸屬可辨。 |

### v1p3c

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 已改成候選 tag → release-test／完整驗收 → 正式 release。 |
| 2 | 已修 | 驗收 31 已補「非整數」。 |
| 3 | 已修 | 私有 registry 驗收索引已包含進度檔。 |
| 4 | 已修 | 結束 1 與結束 3 已拆為 `k1f`、`k1g`。 |
| 5 | 已修 | 本頁只留分組索引，35 條移至 v1p3d。 |

### v1p4

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `config.toml` 先流向 schema 模組，schema 再傳 `config_read` 至 log。 |
| 2 | 已修 | `log.sh` 已畫成獨立檔，並由 `vendor.just` source。 |
| 3 | 已修 | 使用者、根 justfile、entry.just、vendor.just／tools.just、工具命名空間均已有連線。 |
| 4 | 已修 | 交易責任已集中在 progress；工具 metadata `[progress]` 仍由 initfile／baseline 路徑承接。 |
| 5 | 已修 | 呼叫資料與回傳結果已拆成 `run_cli`、`ret_cli` 兩條線。 |
| 6 | 未修 | 容器右側仍有多條長距離共線與折返，模組到檔案的端點需沿線追蹤才能辨識。 |

### v1p5

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 改壞 | 已新增 LABEL 最低介面版檢查，但放在 inspect／pull 之後；規格要求最低介面版檢查先於任何上網。 |
| 2 | 已修 | `a8z` 已改為白色虛線橢圓跨頁出口。 |
| 3 | 已修 | 不再經共同 launcher 格無條件分岔；各失敗原因保留自己的終點。 |
| 4 | 已修 | `a8ix` 已明載 tag 形 `--local` 不得 pull。 |

### v1p5i

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `a9e` 只表達執行 install；檔案結果另以檔案群呈現。 |
| 2 | 已修 | 依圖例約定②，引擎格隱含完整開始／結束事件。 |
| 3 | 已修 | 已以 `a9h` 分流需人處理的橙色出口與真正失敗的紅色出口。 |
| 4 | 已修 | `a9z` 已使用白色虛線橢圓。 |

### v1p5ccc

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 改壞 | 已補 resolve／文法、docker、apply 失敗分支，但全部匯成結束 1；bootstrap.sh 應原樣傳出 add 的 2／3。 |
| 2 | 已修 | resolve、apply 引擎格依圖例約定②各自隱含完成事件。 |
| 3 | 已修 | 已移除共同 launcher 格的無條件成功／失敗分岔。 |
| 4 | 已修 | 現在分別判斷 resolve＋文法、docker 段、apply 結果。 |
| 5 | 已修 | `version.toml` 已明標「最後寫」。 |

### v1p5c

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | `.tmp.install.<id>.toml` 已移到所有暫存寫入之前。 |
| 2 | 已修 | config 存在時直接略過；缺檔才產 config 與其基準版。 |
| 3 | 已修 | 同一 docker run 的結束事件由圖例約定②涵蓋。 |
| 4 | 已修 | 第一次／修復型失敗結果已移往 v1p5cw 的明確失敗出口。 |

### v1p5cw

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 改為判斷「本次是否因原本缺檔而產生 config」，第一次與修復型皆適用。 |
| 2 | 已修 | 補建 config 時會一併建立基準版副本。 |
| 3 | 已修 | 已新增 `baseline/.vendor_kit.toml` 的 `state=managed` 寫入。 |
| 4 | 已修 | 已先判斷 `version.toml` 缺失，再只於「是」分支寫入。 |
| 5 | 已修 | `i5z` 已改為白色虛線橢圓。 |

### v1p5cc

| R# | 狀態 | 核對結果 |
|---|---|---|
| 1 | 已修 | 兩問句旁已有無 tty／EOF 標示，圖例補充 Ctrl-C 中止且不記 declined。 |
| 2 | 已修 | `.dockerignore` symlink 分支已新增一次性遷移指示。 |
| 3 | 已修 | 建檔、symlink、已含、詢問、append／拒絕均已拆開。 |
| 4 | 已修 | 容器結束事件由圖例約定②涵蓋。 |
| 5 | 未修 | `i5e` 仍只寫「已寫 launcher_started」，未明說承接同一 install 容器；跨頁仍可能被誤認為新呼叫。 |

### v1p5b：附件 R 第二組中適用本頁的條目

| R項 | 狀態 | 核對結果 |
|---|---|---|
| G1 | 已修 | resolve 引擎格依新版圖例約定②隱含開始與結束事件。 |
| G2 | 已修 | 本頁已移除共同 launcher 收尾格的無條件多出口。 |
| G4 | 未修 | 頁首沿革、重複名詞與共通規則仍占大量版面，主流程辨識度偏低。 |
| 1 | 已修 | `docker load` 與 `.digest` 均已有獨立失敗出口。 |
| 2 | 已修 | `c2d` 已列 version.local、metadata、stamp、`.tmp.*`、image ID、argv／CI／`-y`／dry-run 等輸入。 |
| 3 | 已修 | `c2c` 已收斂為單一「算執行計畫」動作，詳細輸出另由 `c2d2` 表達。 |
| 4 | 已修 | 現行定案明確接受 `baseline/.gitkeep`；圖面與本版規格一致。 |
| 5 | 已修 | add 前狀態不再宣稱 `add --local` 會寫 version.local.toml。 |

附件 R 本組相關共 66 條：已修 59、未修 4、改壞 3。

## 本輪新發現

以下不重複附件 L。

| 頁 id | 元件 id／引文 | 類別 | 說明 | 必修／選修 |
|---|---|---|---|---|
| v1p2 | `p2_ver_n`「第 1 行 = 唯一版本鎖定行」 | A | 規格明定第一行只是 install 的寫出慣例、不是契約；契約是頂層 `vendor_kit` 位於 `[tools]` 前且符合正規形。 | 必修 |
| v1p3b | `s2b` | A | `update` 是單段動詞，不應畫成 `resolve` 容器內的步驟；CI 模式下 upgrade 未指定 tag 也不得查最新版。 | 必修 |
| v1p3b | `p3_fast` 的 `--local` 判別 | A | 仍採「含 `/` 或 `.tar` 即檔案」及「用 `./`／完整 ref 消歧」的舊規則；v3.5 必須依 `.tar` → 同名檔消歧 → tag 的順序判定。 | 必修 |
| v1p4 | `m_res_u1_1`「token／逾時」 | A／F | pull timeout 是啟動器責任且不轉發引擎；與 registry 查詢 token 放在 resolve 模組會誤導責任邊界。 | 必修 |
| v1p5 | `a8q`、`a8e`、`a8t` | A | bootstrap `--local` 仍以「含 `/`」先判檔案，並以「本機有同名 image」判 6-37；正確條件是非 `.tar`、含 `/`、且存在同名檔，與 image 是否存在無關。 | 必修 |
| v1p5 | `a8p` | A | LABEL 檢查應在可能的 `docker pull` 前；現圖只有 image 到本機後才檢查，斷網時可能先回 pull 失敗而不是 3＋6-18。 | 必修 |
| v1p5i | `a9q`、`a9hx`、`a9x` | A | install 非 0 只畫兩個結束 1，漏掉 install 回 3 時 bootstrap.sh 必須原碼傳出 3。 | 必修 |
| v1p5ccc | `a10rq`／`a10d`／`a10x` → `a12` | A | resolve 或 apply 回 2／3 時被統一改成 1；bootstrap 逐 `-t` 中止正確，但結束碼必須保留失敗步驟原碼。 | 必修 |
| v1p5c | `i0l → i2` | A | 自己執行 install 時先嘗試建立執行紀錄、後檢查是否在 git repo；非 git 目錄無合法紀錄落點，應先做主機 git 前置檢查，再建紀錄。 | 必修 |
| v1p5cc | `igq0`「已含這四行？」 | A | 這是全有／全無判斷；若只已有其中幾行，後續 append 四行可能重複。應逐行辨識，只記實際新增的行。 | 必修 |
| v1p3d | 驗收 18 `p3d_acc_r17c2` | A | 詳表漏驗 `registry_query` URL 必須移除 userinfo；只有「grep 不到 token」不足以涵蓋 §7.4-18。 | 必修 |
| v1p3d | 驗收 19 `p3d_accb_r0c2` | A | 漏掉故意修改 `.dockerignore` 其中一行後，uninstall 應跳過該行並 warn、其餘原文相同行仍刪除的驗收。 | 必修 |
| v1p4 | 引擎模組鏈 `m_res → m_schema → m_prog → …` | F | 雖以資料名稱標線，整體仍像固定執行順序；架構頁應避免讓八模組被理解為每個動詞都依序經過全部模組。 | 選修 |
| v1p3d | 全頁 | F | 作為「逐條詳表」，多列已壓縮掉規格中的關鍵驗證子條件；建議保留可判定 pass/fail 的完整條件，否則改名為驗收摘要。 | 選修 |

## 逐頁結論

- v1p3：未發現附件 R 以外的新問題。
- v1p3c：未發現附件 R 以外的新問題。
- v1p3b、v1p5、v1p5i、v1p5ccc、v1p5c、v1p5cc 仍有會改變實作行為的必修問題。
- v1p2、v1p4、v1p3d 另有契約文字或架構表達問題。
- v1p5b 本身的舊問題大致已修，但版面仍過度重複共通資訊。

總評：本組修正幅度很大，但 `--local` 判別、最低介面版檢查順序、bootstrap 原碼傳出及 install 前置順序仍可能導致錯誤實作，目前尚不能交給使用者看。
