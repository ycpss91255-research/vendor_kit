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
session id: 01a0bed6-4de9-7b30-b222-cff801f7ec1b
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


----- 頁 v1p5bcc -----
# v1p5bcc  21 流程 v2：add（1′）apply 前置

nodes 78（不含 v2 小標）／edges 24／terms 13／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：add <repo>（1′）啟動器 docker → apply 前置（v2.2 E、v2.5 §3／§5、v2.15-4）
- [note/NOTE] pend: 已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = "copy" | "append"（預設 copy）。已定（v2.5 §2／§3／§5、v2.15-4）：逐檔判斷讀暫存 /dist/<repo>，取件在決定套用後；apply 順序 = flock → 重驗指紋 → 驗原 argv 與計畫一致 → dry-run 分支 → 建進度檔 → 寫入 → 刪進度檔；vk-resolve/1 只傳 pull／extract／mount 清單、apply|yes／no、指紋；已接入且完成 → 0 先於查 registry。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bB1 [v2]: 5b′ add <repo> docker 段與 apply 前置（承「add（1）」頁）：resolve 回 0？→ inspect → 無才 pull → extract → apply → 拿鎖 → 重驗指紋 → argv 一致 → dest？→ 撞名？→ CI 模式 → dry-run；寫入段見「add（2）」頁
- [entry/ENTRY] c9e: 來自「add（1）」頁：resolve 容器已結束（已寫 launcher_started）
- [end_red/R12] c9qx [v2]: 1 + 6-30：stdout 文法不合；resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）
- [decision/D12] c9q [v2]: resolve 回 0 且 vk-resolve/1 文法合法？
- [decision/D12] c9a [v2]: 是 → docker image inspect：本機有？
- [step/W12] c9p [v2]: 無：docker pull
- [other/IMG] c9g: <repo>-dist@digest⏎（鎖定的那一版）
- [step/W12] c9b [v2]: extract：docker create <image> /x → cp c:/dist/. <tmp>/<repo>/ → rm
- [end_red/R12] c9px [v2]: 1 + 6-24／6-31：pull 失敗／逾時（離線可用 --local <tar>）
- [end_red/R12] c9bx [v2]: 1：extract 失敗（create／cp／rm 或暫存目錄；已清暫存）
- [step/W12] c10 [v2]: docker run … -v <tmp>:/dist:ro（含 vk-resolve）<引擎> apply add <repo>（--dry-run 原樣轉發）
- [step/SUB] c11a [v2]: apply：flock 專案目錄（60 秒）
- [step/SUB] c11b [v2]: 重驗 resolve 的輸入指紋（讀 /dist/vk-resolve）
- [end_orange/O12] c11cx [v2]: 1：原 argv 與計畫不一致，請重跑
- [decision/D12] c11c [v2]: 原 argv 與計畫一致？
- [end_orange/O12] c12x [v2]: 1：dest 不合法（請修 init.toml／dest）
- [decision/D12] c12 [v2]: 是 → init.toml 的 dest 全部合法？（任何寫入前檢查）
- [rule/RULE] c12r [v2]: dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 不得越出 dist；dist 含 symlink → 拒絕
- [end_orange/O12] c12bx [v2]: 1：命名空間撞名（請改名／移除撞名者）
- [decision/D12] c12b [v2]: just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／module／alias／保留名 vendor_kit）
- [rule/RULE] c12br [v2]: 命名空間撞名（v2.5 §5）：<ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（just --dump --dump-format json）(c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）
- [end_orange/O12] c14x [v2]: 1：印需改清單（CI 模式；請在本機執行後 commit 並 push）
- [decision/D12] c14 [v2]: CI 模式且需改任何進 git 的檔？
- [end_ok/G12] c13y [v2]: 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/<repo>）
- [decision/D12] c13: --dry-run？
- [entry/ENTRY] c13z: 續「add（2）」頁：apply 寫入段（非 dry-run）
- [other/TEXT] _sp: 
- [end_orange/O12] c11x [v2]: 1 + 6-12：指紋不同「請重跑」（中間有人改了）
- [other/LEGEND] p5bp_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5bp_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5bp_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5bp_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5bp_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5bp_lg5 [legend]: 白：步驟
- [other/LEGEND] p5bp_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5bp_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5bp_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5bp_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5bp_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p5bp_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5bp_lgx_img [legend]: 紫：image
- [other/LEGEND] p5bp_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5bp_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p5bp_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5bp_th: 本頁名詞
- [term/TERM_K] p5bp_tk0: resolve／apply 兩段
- [term/TERM_V] p5bp_tv0: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p5bp_tk1: resolve 非 0
- [term/TERM_V] p5bp_tv1: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p5bp_tk2: index digest／docker image inspect
- [term/TERM_V] p5bp_tv2: 多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台
- [term/TERM_K] p5bp_tk3: /dist/<repo>（暫存）／N
- [term/TERM_V] p5bp_tv3: 啟動器把目標版 image 的 dist/ 展開（extract）到主機暫存目錄，掛進引擎 /dist/<repo>:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/<repo>
- [term/TERM_K] p5bp_tk4: strategy（copy／append）
- [term/TERM_V] p5bp_tv4: init.toml [[file]] src/dest 的 strategy = copy（預設）或 append：copy 無→建、有→不納管（6-11）；append（.gitignore 類）無→建、有→問 6-21「要加這幾行嗎」→ 同意加入並記 metadata（state=appended、lines）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）
- [term/TERM_K] p5bp_tk5: dest 撞名
- [term/TERM_V] p5bp_tv5: 兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 正規化不得越出 dist
- [term/TERM_K] p5bp_tk6: 命名空間撞名（v2.5 §5）
- [term/TERM_V] p5bp_tv6: 下游 dist/just/<ns>.just 的 <ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（以 just --dump --dump-format json 取得）(c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）
- [term/TERM_K] p5bp_tk7: gen／mod?／recipe
- [term/TERM_V] p5bp_tv7: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- [term/TERM_K] p5bp_tk8: flock
- [term/TERM_V] p5bp_tv8: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5bp_tk9: 原 argv 與計畫一致
- [term/TERM_V] p5bp_tv9: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- [term/TERM_K] p5bp_tk10: 6-12（指紋不同）
- [term/TERM_V] p5bp_tv10: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- [term/TERM_K] p5bp_tk11: 6-38
- [term/TERM_V] p5bp_tv11: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5bp_tk12: 6-24／6-31（pull 失敗）
- [term/TERM_V] p5bp_tv12: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## edges
- c9a_n: c9a(是 → docker image inspect：本機有？) --無--> c9p(無：docker pull)
- c9g_p: c9g(<repo>-dist@digest （鎖定的那一版）) --拉 /dist--> c9p(無：docker pull)
- c9p_x: c9p(無：docker pull) --(無標籤)--> c9b(extract：docker create <image> …)
- ce13e: c9e(來自「add（1）」頁：resolve 容器已結束（已寫 l…) --(無標籤)--> c9q(resolve 回 0 且 vk-resolve/1 文法合…)
- ce13x: c9q(resolve 回 0 且 vk-resolve/1 文法合…) --否--> c9qx(1 + 6-30：stdout 文法不合；resolve 非…)
- ce13a: c9q(resolve 回 0 且 vk-resolve/1 文法合…) --是--> c9a(是 → docker image inspect：本機有？)
- ce12px: c9p(無：docker pull) --失敗--> c9px(1 + 6-24／6-31：pull 失敗／逾時（離線可用 …)
- ce12bx: c9b(extract：docker create <image> …) --失敗--> c9bx(1：extract 失敗（create／cp／rm 或暫存目…)
- ce13d: c9b(extract：docker create <image> …) --(無標籤)--> c10(docker run … -v <tmp>:/dist:ro…)
- ce14: c10(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> c11a(apply：flock 專案目錄（60 秒）)
- ce14b: c11a(apply：flock 專案目錄（60 秒）) --(無標籤)--> c11b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…)
- ce14c: c11b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --(無標籤)--> c11c(原 argv 與計畫一致？)
- ce14cx: c11c(原 argv 與計畫一致？) --否--> c11cx(1：原 argv 與計畫不一致，請重跑)
- ce16: c11c(原 argv 與計畫一致？) --是--> c12(是 → init.toml 的 dest 全部合法？（任何寫…)
- ce17: c12(是 → init.toml 的 dest 全部合法？（任何寫…) --否--> c12x(1：dest 不合法（請修 init.toml／dest）)
- ce18: c12(是 → init.toml 的 dest 全部合法？（任何寫…) --是--> c12b(just/<ns>.just 的 <ns> 撞名？（其他工具…)
- ce18x: c12b(just/<ns>.just 的 <ns> 撞名？（其他工具…) --是--> c12bx(1：命名空間撞名（請改名／移除撞名者）)
- ce18b: c12b(just/<ns>.just 的 <ns> 撞名？（其他工具…) --否--> c14(CI 模式且需改任何進 git 的檔？)
- ce19: c14(CI 模式且需改任何進 git 的檔？) --是--> c14x(1：印需改清單（CI 模式；請在本機執行後 commit 並…)
- ce20: c14(CI 模式且需改任何進 git 的檔？) --否--> c13(--dry-run？)
- ce21: c13(--dry-run？) --是--> c13y(0：唯讀預覽（印會建／會問哪些檔；讀 /dist/<repo…)
- ce22: c13(--dry-run？) --否--> c13z(續「add（2）」頁：apply 寫入段（非 dry-run…)
- ce12y: c9a(是 → docker image inspect：本機有？) --有--> c9b(extract：docker create <image> …)
- ce15: c11b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --不同--> c11x(1 + 6-12：指紋不同「請重跑」（中間有人改了）)

## terms
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- index digest／docker image inspect: 多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台
- /dist/<repo>（暫存）／N: 啟動器把目標版 image 的 dist/ 展開（extract）到主機暫存目錄，掛進引擎 /dist/<repo>:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/<repo>
- strategy（copy／append）: init.toml [[file]] src/dest 的 strategy = copy（預設）或 append：copy 無→建、有→不納管（6-11）；append（.gitignore 類）無→建、有→問 6-21「要加這幾行嗎」→ 同意加入並記 metadata（state=appended、lines）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）
- dest 撞名: 兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 正規化不得越出 dist
- 命名空間撞名（v2.5 §5）: 下游 dist/just/<ns>.just 的 <ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（以 just --dump --dump-format json 取得）(c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）
- gen／mod?／recipe: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- 原 argv 與計畫一致: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- 6-12（指紋不同）: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## xrefs
- bB1: 其他「add（1）」頁
- bB1: 見「add（2）」頁
- c9e: 來自「add（1）」頁
- c13z: 續「add（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p5bc -----
# v1p5bc  22 流程 v2：add（2）apply 寫入段

nodes 84（不含 v2 小標）／edges 41／terms 9／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：add <repo>（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4）
- [note/NOTE] pend: 已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = "copy" | "append"（預設 copy）。已定（v2.5 §2／§3／§5、v2.15-4）：逐檔判斷讀暫存 /dist/<repo>，取件在決定套用後；apply 順序 = flock → 重驗指紋 → 驗原 argv 與計畫一致 → dry-run 分支 → 建進度檔 → 寫入 → 刪進度檔；vk-resolve/1 只傳 pull／extract／mount 清單、apply|yes／no、指紋；已接入且完成 → 0 先於查 registry。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] bB2 [v2]: 5b″ add <repo> 的 apply 寫入段（承「add（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建進度檔 → 取件 → 印記 → 初始檔逐檔（每個 [[file]] 迴圈）→ 基準版 → metadata → tools.just → version.toml → 刪進度檔
- [entry/ENTRY] c13c: 來自「add（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_started）
- [step/SUB] c15a [v2]: 建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）
- [file/F12] c15af: ＋baseline/<repo>/.vendor_kit.toml（[progress] state=in-progress、started、verb、id=trace_id、done、pending）
- [step/SUB] c15 [v2]: 取件（fetch）：/dist/<repo> 複製到暫存目錄
- [step/SUB] c15c [v2]: 暫存 → cache/<repo>/（原子替換）
- [file/F12] c15f: ＋cache/<repo>/（不進 git）
- [step/SUB] c15b [v2]: 寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）
- [file/F12] c15bf: ＋gen/<repo>.stamp（不進 git）
- [other/TEXT] cl: ↓ 初始檔逐檔（init.toml 每個 [[file]]；範本讀 /dist/<repo>）
- [decision/D12] c16: 初始檔已存在？
- [step/SUB] c17: 無：建該檔（state=managed）
- [rule/RULE] cr [v2]: 復原（v2.2 C、v2.5 §3）：進度檔第一個寫入前建、最後一步刪；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復
- [decision/D12] c18 [v2]: strategy = append？
- [step/SUB] c19: 否：不納管（state=unmanaged）、不覆蓋，印 6-11「已存在，範本在 cache」
- [decision/D12] c20q [v2]: 問 6-21「要在 X 加這幾行嗎」同意？（-y 免問）
- [step/SUB] c20n [v2]: 否：不寫；state=unmanaged 只記 declined_hash
- [step/SUB] c20: 是：append 那幾行（state=appended；實際插入的行之後記進 metadata）
- [decision/D12] c20l [v2]: 還有下一個 [[file]]？
- [step/SUB] c21: 否：寫 baseline/<repo>/（範本副本）
- [file/F12] c21f: ＋baseline/<repo>/（進 git）
- [step/SUB] c21b [v2]: 寫 metadata：source（來源 ref@digest = 最後合併版本）
- [file/F12] c21bf: ＋baseline/<repo>/.vendor_kit.toml（source；進 git）
- [step/SUB] c21b2 [v2]: 寫 metadata：local_image_id（只在 --local tar 時；離線對照）
- [file/F12] c21b2f: .vendor_kit.toml（local_image_id = 本機 image ID ↔ index digest）
- [step/SUB] c21c [v2]: 寫 metadata：每個 dest 的 state（managed／appended／unmanaged；新檔被拒才 declined）
- [file/F12] c21cf: .vendor_kit.toml（[[file]] 各 dest 的 state）
- [step/SUB] c21c2 [v2]: 寫 metadata：declined_hash（被拒那版 N 的 hash）、lines（append 實際插入的行）
- [file/F12] c21c2f: .vendor_kit.toml（[[file]] 各 dest 的 declined_hash／lines）
- [step/SUB] c21d [v2]: 寫 metadata：完成標記（complete = true）
- [file/F12] c21df: .vendor_kit.toml（complete = true）
- [step/SUB] c22 [v2]: 重生 gen/tools.just（每個 <ns>.just 一行 mod?；原子替換，與本次 cache/ 同一 apply 內，I17）
- [file/F12] c22f: gen/tools.just（不進 git；mod? 行）
- [step/SUB] c23 [v2]: 最後寫 version.toml [tools] 版本鎖定行：<repo> = "…:<tag>@sha256:…"
- [file/F12] c23f: ＋version.toml [tools] 版本鎖定行（進 git）
- [step/SUB] c23b [v2]: 成功：刪進度檔（metadata [progress]；最後一步）
- [file/F12] c23bf [v2]: .vendor_kit.toml（－[progress]）
- [other/TEXT] _sp: 
- [end_red/R12] c23x [v2]: 1：寫入失敗（本段任一步）→ 明列已完成／未完成；進度檔保留
- [end_ok/G12] c24: 0：印摘要，提示 git add
- [rule/RULE] c20q_tty: 無tty→6-4
- [other/LEGEND] p5bc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p5bc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p5bc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p5bc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p5bc_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p5bc_lg5 [legend]: 白：步驟
- [other/LEGEND] p5bc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p5bc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p5bc_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p5bc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p5bc_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p5bc_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p5bc_lgx_img [legend]: 紫：image
- [other/LEGEND] p5bc_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p5bc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/LEGEND] p5bc_lgx_tty [legend]: 橙小標：問句無 tty／EOF 且無 -y → 1 + 6-4（Ctrl-C 中止、不記拒絕）
- [other/TEXT] p5bc_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p5bc_th: 本頁名詞
- [term/TERM_K] p5bc_tk0: resolve／apply 兩段
- [term/TERM_V] p5bc_tv0: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p5bc_tk1: /dist/<repo>（暫存）／N
- [term/TERM_V] p5bc_tv1: 啟動器把目標版 image 的 dist/ 展開（extract）到主機暫存目錄，掛進引擎 /dist/<repo>:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/<repo>
- [term/TERM_K] p5bc_tk2: strategy（copy／append）
- [term/TERM_V] p5bc_tv2: init.toml [[file]] src/dest 的 strategy = copy（預設）或 append：copy 無→建、有→不納管（6-11）；append（.gitignore 類）無→建、有→問 6-21「要加這幾行嗎」→ 同意加入並記 metadata（state=appended、lines）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）
- [term/TERM_K] p5bc_tk3: 續作
- [term/TERM_V] p5bc_tv3: add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補下游使用者刻意刪的檔
- [term/TERM_K] p5bc_tk4: gen／mod?／recipe
- [term/TERM_V] p5bc_tv4: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- [term/TERM_K] p5bc_tk5: flock
- [term/TERM_V] p5bc_tv5: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- [term/TERM_K] p5bc_tk6: CRLF
- [term/TERM_V] p5bc_tv6: Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn
- [term/TERM_K] p5bc_tk7: 6-38
- [term/TERM_V] p5bc_tv7: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p5bc_tk8: 6-4（無 tty）
- [term/TERM_V] p5bc_tv8: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## edges
- ce23a: c13c(來自「add（1′）」頁：apply 檢查通過（非 dry-…) --(無標籤)--> c15a(建進度檔：metadata [progress]（state…)
- ce23b: c15a(建進度檔：metadata [progress]（state…) --寫--> c15af(＋baseline/<repo>/.vendor_kit.t…)
- ce23c: c15a(建進度檔：metadata [progress]（state…) --(無標籤)--> c15(取件（fetch）：/dist/<repo> 複製到暫存目錄)
- ce23cc: c15(取件（fetch）：/dist/<repo> 複製到暫存目錄) --(無標籤)--> c15c(暫存 → cache/<repo>/（原子替換）)
- ce23: c15c(暫存 → cache/<repo>/（原子替換）) --寫--> c15f(＋cache/<repo>/（不進 git）)
- ce23d: c15c(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> c15b(寫印記 gen/<repo>.stamp（第一行 index…)
- ce23e: c15b(寫印記 gen/<repo>.stamp（第一行 index…) --寫--> c15bf(＋gen/<repo>.stamp（不進 git）)
- ce24: c15b(寫印記 gen/<repo>.stamp（第一行 index…) --(無標籤)--> c16(初始檔已存在？)
- ce25: c16(初始檔已存在？) --無--> c17(無：建該檔（state=managed）)
- ce26: c16(初始檔已存在？) --有--> c18(strategy = append？)
- ce27: c18(strategy = append？) --否--> c19(否：不納管（state=unmanaged）、不覆蓋，印 6…)
- ce28: c18(strategy = append？) --是--> c20q(問 6-21「要在 X 加這幾行嗎」同意？（-y 免問）)
- ce28n: c20q(問 6-21「要在 X 加這幾行嗎」同意？（-y 免問）) --否--> c20n(否：不寫；state=unmanaged 只記 declin…)
- ce28y: c20q(問 6-21「要在 X 加這幾行嗎」同意？（-y 免問）) --是--> c20(是：append 那幾行（state=appended；實際…)
- ce29: c17(無：建該檔（state=managed）) --(無標籤)--> c20l(還有下一個 [[file]]？)
- ce30: c19(否：不納管（state=unmanaged）、不覆蓋，印 6…) --(無標籤)--> c20l(還有下一個 [[file]]？)
- ce31: c20(是：append 那幾行（state=appended；實際…) --(無標籤)--> c20l(還有下一個 [[file]]？)
- ce31n: c20n(否：不寫；state=unmanaged 只記 declin…) --(無標籤)--> c20l(還有下一個 [[file]]？)
- ce31y: c20l(還有下一個 [[file]]？) --是--> c16(初始檔已存在？)
- ce31l: c20l(還有下一個 [[file]]？) --否--> c21(否：寫 baseline/<repo>/（範本副本）)
- ce32: c21(否：寫 baseline/<repo>/（範本副本）) --寫--> c21f(＋baseline/<repo>/（進 git）)
- ce32b: c21(否：寫 baseline/<repo>/（範本副本）) --(無標籤)--> c21b(寫 metadata：source（來源 ref@diges…)
- ce32f: c21b(寫 metadata：source（來源 ref@diges…) --寫--> c21bf(＋baseline/<repo>/.vendor_kit.t…)
- ce32b2: c21b(寫 metadata：source（來源 ref@diges…) --(無標籤)--> c21b2(寫 metadata：local_image_id（只在 -…)
- ce32b2f: c21b2(寫 metadata：local_image_id（只在 -…) --寫--> c21b2f(.vendor_kit.toml（local_image_i…)
- ce32c: c21b2(寫 metadata：local_image_id（只在 -…) --(無標籤)--> c21c(寫 metadata：每個 dest 的 state（man…)
- ce32cf: c21c(寫 metadata：每個 dest 的 state（man…) --寫--> c21cf(.vendor_kit.toml（[[file]] 各 de…)
- ce32c2: c21c(寫 metadata：每個 dest 的 state（man…) --(無標籤)--> c21c2(寫 metadata：declined_hash（被拒那版 …)
- ce32c2f: c21c2(寫 metadata：declined_hash（被拒那版 …) --寫--> c21c2f(.vendor_kit.toml（[[file]] 各 de…)
- ce32d: c21c2(寫 metadata：declined_hash（被拒那版 …) --(無標籤)--> c21d(寫 metadata：完成標記（complete = tru…)
- ce32df: c21d(寫 metadata：完成標記（complete = tru…) --寫--> c21df(.vendor_kit.toml（complete = tr…)
- ce33: c21d(寫 metadata：完成標記（complete = tru…) --(無標籤)--> c22(重生 gen/tools.just（每個 <ns>.just…)
- ce34: c22(重生 gen/tools.just（每個 <ns>.just…) --寫--> c22f(gen/tools.just（不進 git；mod? 行）)
- ce35: c22(重生 gen/tools.just（每個 <ns>.just…) --(無標籤)--> c23(最後寫 version.toml [tools] 版本鎖定行…)
- ce36: c23(最後寫 version.toml [tools] 版本鎖定行…) --寫--> c23f(＋version.toml [tools] 版本鎖定行（進 …)
- ce37: c23(最後寫 version.toml [tools] 版本鎖定行…) --(無標籤)--> c23b(成功：刪進度檔（metadata [progress]；最後…)
- ce37f: c23b(成功：刪進度檔（metadata [progress]；最後…) --刪--> c23bf(.vendor_kit.toml（－[progress]）)
- ce38a: c15c(暫存 → cache/<repo>/（原子替換）) --失敗--> c23x(1：寫入失敗（本段任一步）→ 明列已完成／未完成；進度檔保留)
- ce38b: c21(否：寫 baseline/<repo>/（範本副本）) --失敗--> c23x(1：寫入失敗（本段任一步）→ 明列已完成／未完成；進度檔保留)
- ce38: c23(最後寫 version.toml [tools] 版本鎖定行…) --失敗--> c23x(1：寫入失敗（本段任一步）→ 明列已完成／未完成；進度檔保留)
- ce39: c23b(成功：刪進度檔（metadata [progress]；最後…) --(無標籤)--> c24(0：印摘要，提示 git add)

## terms
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- /dist/<repo>（暫存）／N: 啟動器把目標版 image 的 dist/ 展開（extract）到主機暫存目錄，掛進引擎 /dist/<repo>:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/<repo>
- strategy（copy／append）: init.toml [[file]] src/dest 的 strategy = copy（預設）或 append：copy 無→建、有→不納管（6-11）；append（.gitignore 類）無→建、有→問 6-21「要加這幾行嗎」→ 同意加入並記 metadata（state=appended、lines）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）
- 續作: add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補下游使用者刻意刪的檔
- gen／mod?／recipe: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just' = 把工具的 just 檔掛成一個命名空間；mod?（帶問號）= 檔不在也不掛；recipe = justfile 裡的一條指令；gen/.stamp 只記引擎 ref，install 寫、add 不動
- flock: 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖
- CRLF: Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-4（無 tty）: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## xrefs
- bB2: 其他「add（1′）」頁
- c13c: 來自「add（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p6 -----
# v1p6  23 流程 v2：sync（1）啟動器快路徑

nodes 74（不含 v2 小標）／edges 19／terms 12／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：sync（1）啟動器：專案根 → 執行紀錄 → gen/.stamp 比對 → 快路徑（Q22）→ 起引擎（§6、v2.5 §9）
- [note/NOTE] pend: 已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit；install／升引擎跳過這關。已定（v2.5 §9、Q22、v2.15-17）：sync 可寫範圍 = cache/<repo>/、gen/tools.just、gen/<repo>.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 模式、版本變動那次才做，不符重裝一次再驗，仍不符 → 失敗。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] eA [v2]: sync（recipe 自動前置；CI 模式不走快路徑）第 1 段：專案根檢查 → 執行紀錄 → 比對 gen/.stamp（install／升引擎跳過）→ 快路徑 grep 全相符 → 0；有差 → inspect／pull → 引擎 resolve sync（「sync（1′）」頁）
- [end_ok/G12] n0: 打工具 recipe（_sync 自動前置）或 just vendor_kit sync
- [decision/D12] n0q [v2]: 在專案根執行？（recipe 檢查；_sync 已先 cd）
- [end_orange/O12] n0qx [v2]: 1 + 6-9：請到 <dir> 執行（執行紀錄未建）
- [step/W12] n0l [v2]: 是：建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入）
- [end_red/R12] n0x [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [step/W12] n1 [v2]: grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（命中須恰 1；version.local.toml 本機覆寫優先）
- [file/FGRP] n2: 讀
- [file/F12] n2_0: .vendor_kit/version.toml（進 git）
- [file/F12] n2_1: .vendor_kit/version.local.toml（不進 git，dev 用）
- [end_orange/O12] n3n [v2]: 1 + 6-1：vendor_kit 已更新 vX → vY，請執行 just vendor_kit upgrade vendor_kit
- [decision/D12] n3 [v2]: gen/.stamp 的引擎 ref ＝ 版本鎖定行？（缺 gen/.stamp → 改以薄殼自描述首行 engine= 比對）
- [rule/RULE] n6 [v2]: 統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印 6-1「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／升引擎不受此關
- [decision/D12] nq [v2]: 快路徑：grep 全相符且非 CI 模式？
- [rule/RULE] nqr [v2]: 快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 CI 模式；sync 無參數。全相符 → 寫執行紀錄後 0；否則起引擎；每檔 sha256 只在 sync --verify、CI 模式、或版本變動的那次才做（§3.6）
- [end_ok/G12] nq0 [v2]: 0：不起容器，接著跑原本的 recipe（快路徑）
- [step/W12] nqf [v2]: 是：執行紀錄寫 sync_fast_path
- [rule/RULE] n6b [v2]: 薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與升引擎做；做之前比對現內容 == 上次產物（自描述首行 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼
- [decision/D12] n1i [v2]: 否 → docker image inspect：本機有？
- [step/W12] n1p [v2]: 無：docker pull <引擎 ref>
- [other/IMG] n1g: vendor_kit:vN@sha256:…⏎（引擎 image）
- [end_red/R12] n1vx [v2]: 1：本機覆寫的 image ID 不符（同 tag 重 build；本機覆寫已失效，請 undev 或重新 dev）
- [decision/D12] n1v [v2]: 覆寫中且 .Id ≠ 記的 image ID？
- [entry/ENTRY] n1z: 續「sync（1′）」頁：docker run <引擎> resolve sync
- [other/TEXT] _sp: 
- [end_red/R12] n1px [v2]: 1 + 6-24／6-31：引擎 image 拉不到（分類）／逾時
- [other/LEGEND] p6_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p6_lg1 [legend]: 黃：判斷
- [other/LEGEND] p6_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p6_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p6_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p6_lg5 [legend]: 白：步驟
- [other/LEGEND] p6_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p6_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p6_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p6_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p6_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p6_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p6_lgx_img [legend]: 紫：image
- [other/LEGEND] p6_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p6_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p6_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p6_th: 本頁名詞
- [term/TERM_K] p6_tk0: 快路徑（Q22）
- [term/TERM_V] p6_tv0: 啟動器只用 grep 比對：gen/.stamp 第一行 == 引擎 ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 CI 模式；sync 無參數。全相符 → 不起容器、0（執行紀錄寫 sync_fast_path）；否則起引擎 resolve sync
- [term/TERM_K] p6_tk1: resolve／apply 兩段
- [term/TERM_V] p6_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p6_tk2: 6-9（專案根）
- [term/TERM_V] p6_tv2: vendor_kit 動詞只准在專案根執行（recipe 檢查 invocation_directory() == justfile_directory()），否則 1 印 6-9「請到 <dir> 執行」；sync 也適用：工具 recipe 的 _sync 先 cd 到專案根再呼叫 sync，所以不受影響；此檢查不寫檔，在建執行紀錄之前
- [term/TERM_K] p6_tk3: 統一提示 6-1（Q10 (2)）
- [term/TERM_V] p6_tv3: 啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需人處理，橙）；install／升引擎跳過這關；fresh clone 缺 gen/.stamp 時改用薄殼自描述首行 engine= 做相容判定（不是視為相符）
- [term/TERM_K] p6_tk4: 引擎 ref
- [term/TERM_V] p6_tv4: version.toml 的 vendor_kit 版本鎖定行指到的引擎 image 版本（啟動器 grep 命中須恰 1；version.local.toml 的本機覆寫優先）
- [term/TERM_K] p6_tk5: gen/ 三種檔
- [term/TERM_V] p6_tv5: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- [term/TERM_K] p6_tk6: image tag／digest／docker image inspect
- [term/TERM_V] p6_tv6: tag = 人看的版本名（可重 build）；digest = 從倉庫拉來的內容 sha256（鎖定用）；啟動器每次 docker run 前先 inspect：本機有 → 不 pull；引擎本機覆寫時 .Id 必須等於 version.local.toml 記的 image ID，否則 1（本機覆寫已失效）
- [term/TERM_K] p6_tk7: 完成標記／基準版落後
- [term/TERM_V] p6_tv7: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- [term/TERM_K] p6_tk8: 6-33（未完成交易）
- [term/TERM_V] p6_tv8: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- [term/TERM_K] p6_tk9: 覆寫兩種（v2.1 B／v2.2 B）
- [term/TERM_V] p6_tv9: 引擎本機覆寫 vendor_kit = "<tag>"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具本機覆寫 <repo> = "path:<dir>" → cache 是 symlink，跳過取件／verify，仍查 metadata／基準版
- [term/TERM_K] p6_tk10: GHCR／daemon／flock
- [term/TERM_V] p6_tv10: GHCR = GitHub 容器倉庫；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎
- [term/TERM_K] p6_tk11: 6-38
- [term/TERM_V] p6_tv11: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## edges
- ne0: n0(打工具 recipe（_sync 自動前置）或 just v…) --(無標籤)--> n0q(在專案根執行？（recipe 檢查；_sync 已先 cd）)
- ne0x: n0q(在專案根執行？（recipe 檢查；_sync 已先 cd）) --否--> n0qx(1 + 6-9：請到 <dir> 執行（執行紀錄未建）)
- ne0l: n0q(在專案根執行？（recipe 檢查；_sync 已先 cd）) --是--> n0l(是：建執行紀錄、寫 launcher_started（失敗 …)
- ne1x: n0l(是：建執行紀錄、寫 launcher_started（失敗 …) --失敗--> n0x(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- ne1l: n0l(是：建執行紀錄、寫 launcher_started（失敗 …) --(無標籤)--> n1(grep version.toml 的 vendor_kit…)
- ne2: n1(grep version.toml 的 vendor_kit…) --讀--> n2(讀)
- ne3: n1(grep version.toml 的 vendor_kit…) --(無標籤)--> n3(gen/.stamp 的引擎 ref ＝ 版本鎖定行？（缺 …)
- ne4: n3(gen/.stamp 的引擎 ref ＝ 版本鎖定行？（缺 …) --否--> n3n(1 + 6-1：vendor_kit 已更新 vX → vY…)
- ne5: n3(gen/.stamp 的引擎 ref ＝ 版本鎖定行？（缺 …) --是--> nq(快路徑：grep 全相符且非 CI 模式？)
- ne5q: nq(快路徑：grep 全相符且非 CI 模式？) --是--> nqf(是：執行紀錄寫 sync_fast_path)
- ne5ql: nqf(是：執行紀錄寫 sync_fast_path) --(無標籤)--> nq0(0：不起容器，接著跑原本的 recipe（快路徑）)
- ne5n: nq(快路徑：grep 全相符且非 CI 模式？) --否--> n1i(否 → docker image inspect：本機有？)
- ne5p: n1i(否 → docker image inspect：本機有？) --無--> n1p(無：docker pull <引擎 ref>)
- ne5g: n1g(vendor_kit:vN@sha256:… （引擎 ima…) --拉--> n1p(無：docker pull <引擎 ref>)
- ne5v: n1i(否 → docker image inspect：本機有？) --有--> n1v(覆寫中且 .Id ≠ 記的 image ID？)
- ne5pv: n1p(無：docker pull <引擎 ref>) --(無標籤)--> n1z(續「sync（1′）」頁：docker run <引擎> r…)
- ne5y: n1v(覆寫中且 .Id ≠ 記的 image ID？) --是--> n1vx(1：本機覆寫的 image ID 不符（同 tag 重 bu…)
- ne5i: n1v(覆寫中且 .Id ≠ 記的 image ID？) --否--> n1z(續「sync（1′）」頁：docker run <引擎> r…)
- ne5x: n1p(無：docker pull <引擎 ref>) --失敗--> n1px(1 + 6-24／6-31：引擎 image 拉不到（分類）…)

## terms
- 快路徑（Q22）: 啟動器只用 grep 比對：gen/.stamp 第一行 == 引擎 ref；[tools] 每個 <repo> 的 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；非 CI 模式；sync 無參數。全相符 → 不起容器、0（執行紀錄寫 sync_fast_path）；否則起引擎 resolve sync
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- 6-9（專案根）: vendor_kit 動詞只准在專案根執行（recipe 檢查 invocation_directory() == justfile_directory()），否則 1 印 6-9「請到 <dir> 執行」；sync 也適用：工具 recipe 的 _sync 先 cd 到專案根再呼叫 sync，所以不受影響；此檢查不寫檔，在建執行紀錄之前
- 統一提示 6-1（Q10 (2)）: 啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需人處理，橙）；install／升引擎跳過這關；fresh clone 缺 gen/.stamp 時改用薄殼自描述首行 engine= 做相容判定（不是視為相符）
- 引擎 ref: version.toml 的 vendor_kit 版本鎖定行指到的引擎 image 版本（啟動器 grep 命中須恰 1；version.local.toml 的本機覆寫優先）
- gen/ 三種檔: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- image tag／digest／docker image inspect: tag = 人看的版本名（可重 build）；digest = 從倉庫拉來的內容 sha256（鎖定用）；啟動器每次 docker run 前先 inspect：本機有 → 不 pull；引擎本機覆寫時 .Id 必須等於 version.local.toml 記的 image ID，否則 1（本機覆寫已失效）
- 完成標記／基準版落後: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- 6-33（未完成交易）: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- 覆寫兩種（v2.1 B／v2.2 B）: 引擎本機覆寫 vendor_kit = "<tag>"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具本機覆寫 <repo> = "path:<dir>" → cache 是 symlink，跳過取件／verify，仍查 metadata／基準版
- GHCR／daemon／flock: GHCR = GitHub 容器倉庫；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## xrefs
- eA: 其他「sync（1′）」頁
- n1z: 續「sync（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p6cc -----
# v1p6cc  24 流程 v2：sync（1′）引擎 resolve

nodes 80（不含 v2 小標）／edges 38／terms 10／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：sync（1′）引擎 resolve sync（逐工具；§6、v2.2 A／B／E、v2.3 §3／§4、v2.5 §9、v2.15-17）
- [note/NOTE] pend: 已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit；install／升引擎跳過這關。已定（v2.5 §9、Q22、v2.15-17）：sync 可寫範圍 = cache/<repo>/、gen/tools.just、gen/<repo>.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 模式、版本變動那次才做，不符重裝一次再驗，仍不符 → 失敗。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: 專案目錄
- [other/BAND] eA2 [v2]: sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 偵測未完成交易（6-33 → 1）→ 逐工具算待辦 → 空 → apply|no → 0；有待辦 → stdout 只傳協定內容 → 第 2 段見「sync（2）」頁
- [entry/ENTRY] n1e: 來自「sync（1）」頁：引擎 image 已在本機、快路徑有差（已寫 launcher_started）
- [step/W12] n1b [v2]: docker run <引擎> resolve sync（永不 -t）
- [step/SUB] n1be [v2]: resolve sync（不寫任何檔）：讀 version.toml、各 metadata、印記
- [end_orange/O12] njx [v2]: 1 + 6-33：偵測到未完成交易，請先重跑該動詞
- [decision/D12] nj [v2]: 偵測到未完成交易？
- [end_orange/O12] ncx [v2]: 1：CI 模式拒絕本機覆寫（請先 undev）
- [decision/D12] nc [v2]: 否 → CI 模式且有本機覆寫？
- [rule/RULE] nf [v2]: CI 模式（v2.6 §2）= 只准寫 cache/、gen/；不查最新版；需寫任何進 git 的檔 → 1（-y 不解除）；升為失敗：薄殼不符、基準版落後、未完成接入、任何本機覆寫
- [decision/D12] t0 [v2]: 否 → path 覆寫（dev 中）？
- [step/SUB] t0s [v2]: 是：跳過取件／verify（仍查 metadata、基準版）↓
- [rule/RULE] t0r [v2]: 覆寫兩種（v2.1 B）：引擎 vendor_kit = "<tag>"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 <repo> = "path:<dir>" → cache/<repo>/ 是 symlink，跳過取件／verify
- [decision/D12] t1 [v2]: cache 缺或印記 ≠ 鎖定？
- [step/SUB] t1y [v2]: 是：列待辦「取件鎖定版」＋「apply 後全檔驗證」（版本變動那次）
- [decision/D12] t2q [v2]: 否 → 逐檔驗？（--verify／CI 模式）
- [step/SUB] t2qn [v2]: 否：不逐檔驗（快）↓
- [decision/D12] t2: 是 → 每檔 sha256 ＝ 印記？
- [step/SUB] t2n: 否：列待辦「重裝一次 + warn（cache 被改過）」＋「再驗」
- [end_red/R12] t3mx [v2]: 1：metadata 失蹤或不可解析（請 git checkout 或重新 add <repo>）
- [decision/D12] t3m [v2]: metadata 存在且可解析？
- [end_orange/O12] t3a: 1 + 6-13：<repo> 未完成接入，請先 add <repo>
- [decision/D12] t3: 是 → metadata 有完成標記？
- [rule/INV] t3r [v2]: 不變量（v2.1 A、v2.5 §9）：自動化不碰專案檔 —— sync 不寫 version.toml、初始檔、基準版、薄殼、gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp
- [decision/D12] t4: 最後合併版本 ＝ 鎖定版？
- [end_orange/O12] t4r: 1 + 6-5：基準版落後（請在本機 upgrade <repo> -y 後 push）
- [decision/D12] t4c: 否（落後）→ CI 模式？
- [step/SUB] t5: 否：warn「基準版落後，請 just vendor_kit upgrade <repo>」（繼續）
- [decision/D12] tq [v2]: 還有工具？
- [decision/D12] t6 [v2]: 否 → tools.just 缺或不符？
- [step/SUB] t6y [v2]: 是：列待辦「重生 gen/tools.just」
- [step/SUB] z0 [v2]: 彙整待辦清單（要 extract 的 image、要重裝／再驗的工具、要重生 gen/tools.just）
- [end_ok/G12] z2 [v2]: 0：無待辦（apply|no），不起第二個容器，接著跑 recipe
- [decision/D12] z0q [v2]: 待辦為空？
- [step/SUB] z1 [v2]: 否：產生輸入指紋（version.toml、metadata、印記 hash…）
- [step/SUB] z1b [v2]: stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋（只傳協定內容）
- [entry/ENTRY] mb: 續「sync（2）」頁（apply|yes）：啟動器驗 vk-resolve → docker → 引擎 apply sync
- [other/LEGEND] p6r_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p6r_lg1 [legend]: 黃：判斷
- [other/LEGEND] p6r_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p6r_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p6r_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p6r_lg5 [legend]: 白：步驟
- [other/LEGEND] p6r_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p6r_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p6r_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p6r_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p6r_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p6r_lgx_inv [legend]: 紅粗框：不變量
- [other/LEGEND] p6r_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p6r_lgx_img [legend]: 紫：image
- [other/LEGEND] p6r_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p6r_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p6r_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p6r_th: 本頁名詞
- [term/TERM_K] p6r_tk0: resolve／apply 兩段
- [term/TERM_V] p6r_tv0: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p6r_tk1: 待辦清單／apply|no
- [term/TERM_V] p6r_tv1: resolve sync 在引擎內算待辦（要拉哪些 image、要重裝什麼、要不要重生 tools.just）；stdout 只傳 extract 清單、指紋、apply|yes／no；無待辦 → apply|no，啟動器驗完文法直接 0、不起第二個容器
- [term/TERM_K] p6r_tk2: 引擎 ref
- [term/TERM_V] p6r_tv2: version.toml 的 vendor_kit 版本鎖定行指到的引擎 image 版本（啟動器 grep 命中須恰 1；version.local.toml 的本機覆寫優先）
- [term/TERM_K] p6r_tk3: gen/ 三種檔
- [term/TERM_V] p6r_tv3: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- [term/TERM_K] p6r_tk4: verify／sha256
- [term/TERM_V] p6r_tv4: verify 把 cache/<repo>/ 每個檔的 sha256 跟印記比；不符 → 重裝一次 + warn，再驗仍不符 → 1 失敗（不無限重裝）；只在 sync --verify、CI 模式、或版本變動那次做；cache 缺或印記變了就直接重裝，apply 後再驗
- [term/TERM_K] p6r_tk5: 完成標記／基準版落後
- [term/TERM_V] p6r_tv5: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- [term/TERM_K] p6r_tk6: mod?／recipe
- [term/TERM_V] p6r_tv6: mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe
- [term/TERM_K] p6r_tk7: 6-33（未完成交易）
- [term/TERM_V] p6r_tv7: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- [term/TERM_K] p6r_tk8: 覆寫兩種（v2.1 B／v2.2 B）
- [term/TERM_V] p6r_tv8: 引擎本機覆寫 vendor_kit = "<tag>"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具本機覆寫 <repo> = "path:<dir>" → cache 是 symlink，跳過取件／verify，仍查 metadata／基準版
- [term/TERM_K] p6r_tk9: 6-38
- [term/TERM_V] p6r_tv9: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## edges
- ne6i: n1e(來自「sync（1）」頁：引擎 image 已在本機、快路徑…) --(無標籤)--> n1b(docker run <引擎> resolve sync（永…)
- ne6r: n1b(docker run <引擎> resolve sync（永…) --(無標籤)--> n1be(resolve sync（不寫任何檔）：讀 version.…)
- ne6: n1be(resolve sync（不寫任何檔）：讀 version.…) --(無標籤)--> nj(偵測到未完成交易？)
- ne6x: nj(偵測到未完成交易？) --是--> njx(1 + 6-33：偵測到未完成交易，請先重跑該動詞)
- ne6n: nj(偵測到未完成交易？) --否--> nc(否 → CI 模式且有本機覆寫？)
- ne7: nc(否 → CI 模式且有本機覆寫？) --是--> ncx(1：CI 模式拒絕本機覆寫（請先 undev）)
- ne8: nc(否 → CI 模式且有本機覆寫？) --否--> t0(否 → path 覆寫（dev 中）？)
- te0: t0(否 → path 覆寫（dev 中）？) --是--> t0s(是：跳過取件／verify（仍查 metadata、基準版）…)
- te1: t0(否 → path 覆寫（dev 中）？) --否--> t1(cache 缺或印記 ≠ 鎖定？)
- te2: t0s(是：跳過取件／verify（仍查 metadata、基準版）…) --(無標籤)--> t3m(metadata 存在且可解析？)
- te3: t1(cache 缺或印記 ≠ 鎖定？) --是--> t1y(是：列待辦「取件鎖定版」＋「apply 後全檔驗證」（版本變…)
- te4: t1(cache 缺或印記 ≠ 鎖定？) --否--> t2q(否 → 逐檔驗？（--verify／CI 模式）)
- te5: t1y(是：列待辦「取件鎖定版」＋「apply 後全檔驗證」（版本變…) --(無標籤)--> t3m(metadata 存在且可解析？)
- te3q: t2q(否 → 逐檔驗？（--verify／CI 模式）) --否--> t2qn(否：不逐檔驗（快）↓)
- te4q: t2q(否 → 逐檔驗？（--verify／CI 模式）) --是--> t2(是 → 每檔 sha256 ＝ 印記？)
- te5q: t2qn(否：不逐檔驗（快）↓) --(無標籤)--> t3m(metadata 存在且可解析？)
- te6: t2(是 → 每檔 sha256 ＝ 印記？) --否--> t2n(否：列待辦「重裝一次 + warn（cache 被改過）」＋…)
- te7: t2(是 → 每檔 sha256 ＝ 印記？) --是--> t3m(metadata 存在且可解析？)
- te8: t2n(否：列待辦「重裝一次 + warn（cache 被改過）」＋…) --(無標籤)--> t3m(metadata 存在且可解析？)
- te9m: t3m(metadata 存在且可解析？) --否--> t3mx(1：metadata 失蹤或不可解析（請 git check…)
- te9: t3m(metadata 存在且可解析？) --是--> t3(是 → metadata 有完成標記？)
- te9x: t3(是 → metadata 有完成標記？) --否--> t3a(1 + 6-13：<repo> 未完成接入，請先 add <…)
- te10: t3(是 → metadata 有完成標記？) --是--> t4(最後合併版本 ＝ 鎖定版？)
- te11: t4(最後合併版本 ＝ 鎖定版？) --否--> t4c(否（落後）→ CI 模式？)
- te12: t4c(否（落後）→ CI 模式？) --是--> t4r(1 + 6-5：基準版落後（請在本機 upgrade <re…)
- te13: t4c(否（落後）→ CI 模式？) --否--> t5(否：warn「基準版落後，請 just vendor_kit…)
- te14: t4(最後合併版本 ＝ 鎖定版？) --是--> tq(還有工具？)
- te15: t5(否：warn「基準版落後，請 just vendor_kit…) --(無標籤)--> tq(還有工具？)
- te15n: tq(還有工具？) --否--> t6(否 → tools.just 缺或不符？)
- te16: t6(否 → tools.just 缺或不符？) --是--> t6y(是：列待辦「重生 gen/tools.just」)
- te17: t6(否 → tools.just 缺或不符？) --否--> z0(彙整待辦清單（要 extract 的 image、要重裝／再…)
- te18: t6y(是：列待辦「重生 gen/tools.just」) --(無標籤)--> z0(彙整待辦清單（要 extract 的 image、要重裝／再…)
- ze0: z0(彙整待辦清單（要 extract 的 image、要重裝／再…) --(無標籤)--> z0q(待辦為空？)
- ze0y: z0q(待辦為空？) --是--> z2(0：無待辦（apply|no），不起第二個容器，接著跑 re…)
- ze0n: z0q(待辦為空？) --否--> z1(否：產生輸入指紋（version.toml、metadata…)
- ze0b: z1(否：產生輸入指紋（version.toml、metadata…) --(無標籤)--> z1b(stdout vk-resolve/1：pull／extra…)
- ze2: z1b(stdout vk-resolve/1：pull／extra…) --(無標籤)--> mb(續「sync（2）」頁（apply|yes）：啟動器驗 vk…)
- te15y: tq(還有工具？) --是：下一個工具--> t0(否 → path 覆寫（dev 中）？)

## terms
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- 待辦清單／apply|no: resolve sync 在引擎內算待辦（要拉哪些 image、要重裝什麼、要不要重生 tools.just）；stdout 只傳 extract 清單、指紋、apply|yes／no；無待辦 → apply|no，啟動器驗完文法直接 0、不起第二個容器
- 引擎 ref: version.toml 的 vendor_kit 版本鎖定行指到的引擎 image 版本（啟動器 grep 命中須恰 1；version.local.toml 的本機覆寫優先）
- gen/ 三種檔: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- verify／sha256: verify 把 cache/<repo>/ 每個檔的 sha256 跟印記比；不符 → 重裝一次 + warn，再驗仍不符 → 1 失敗（不無限重裝）；只在 sync --verify、CI 模式、或版本變動那次做；cache 缺或印記變了就直接重裝，apply 後再驗
- 完成標記／基準版落後: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- mod?／recipe: mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe
- 6-33（未完成交易）: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- 覆寫兩種（v2.1 B／v2.2 B）: 引擎本機覆寫 vendor_kit = "<tag>"＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具本機覆寫 <repo> = "path:<dir>" → cache 是 symlink，跳過取件／verify，仍查 metadata／基準版
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## xrefs
- eA2: 其他「sync（1）」頁
- eA2: 見「sync（2）」頁
- n1e: 來自「sync（1）」頁
- mb: 續「sync（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p6c -----
# v1p6c  25 流程 v2：sync（2）apply

nodes 79（不含 v2 小標）／edges 34／terms 12／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：sync（2）第 2 段 apply（§6、v2.3 §3／§4、v2.5 §9、v2.15-17）
- [note/NOTE] pend: 已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit；install／升引擎跳過這關。已定（v2.5 §9、Q22、v2.15-17）：sync 可寫範圍 = cache/<repo>/、gen/tools.just、gen/<repo>.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 模式、版本變動那次才做，不符重裝一次再驗，仍不符 → 失敗。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] eB [v2]: sync 第 2 段（承「sync（1′）」頁）：resolve 回 0？→ 每個 extract：inspect → pull → extract → apply sync：逐工具取件 → 印記 → 驗（--verify／CI／版本變動那次）→ 不符重裝一次再驗 → tools.just
- [entry/ENTRY] m00: 來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_started）
- [end_red/R12] m0qx [v2]: 1 + 6-30：stdout 文法不合；resolve 非 0 → 原碼傳出（不跑 docker／apply）
- [decision/D12] m0q [v2]: resolve 回 0 且 vk-resolve/1 文法合法？
- [decision/D12] m0a [v2]: 是 → 對每個 extract：docker image inspect 本機有？
- [step/W12] m0p [v2]: 無：docker pull
- [other/IMG] m0g: <repo>-dist@digest⏎（鎖定版；多架構 index）
- [step/W12] m0b [v2]: extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm
- [end_red/R12] m0px [v2]: 1 + 6-24／6-31：pull 失敗／逾時
- [end_red/R12] m0bx [v2]: 1：extract 失敗（create／cp／rm 或暫存目錄）
- [step/W12] m1 [v2]: docker run … -v <tmp>:/dist:ro（含 vk-resolve）<引擎> apply sync
- [step/SUB] m2a [v2]: apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）
- [step/SUB] m2b [v2]: 重驗 resolve 的輸入指紋（讀 /dist/vk-resolve）
- [end_orange/O12] m2x [v2]: 1 + 6-12：指紋不同「請重跑」
- [end_orange/O12] m2cx [v2]: 1：原 argv 與計畫不一致，請重跑
- [decision/D12] m2c [v2]: 原 argv 與計畫一致？
- [step/SUB] m3 [v2]: 逐待辦工具：取件 /dist/<repo> 展開到暫存目錄
- [step/SUB] m3c [v2]: 暫存 → cache/<repo>/（原子替換）
- [file/F12] m3f: cache/<repo>/（重寫，不進 git）
- [step/SUB] m3b [v2]: 寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）
- [file/F12] m3bf: gen/<repo>.stamp（重寫，不進 git）
- [decision/D12] m3vd [v2]: 逐檔驗？（--verify／CI 模式／版本變動的那次）
- [step/SUB] m3v [v2]: 是：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）
- [decision/D12] m3vq [v2]: 全部相符？
- [step/SUB] m3vn [v2]: 否：重裝該工具一次 + warn（cache 被改過）
- [step/SUB] m3v2 [v2]: 再逐檔驗一次
- [end_red/R12] m3x2 [v2]: 1：重裝後仍不符（取件／寫入／驗證失敗），不再重裝
- [decision/D12] m3vq2 [v2]: 相符？
- [decision/D12] mq [v2]: 還有待辦工具？
- [step/SUB] m5 [v2]: 否：重生 gen/tools.just（待辦有它時；每個 <ns>.just 一行 mod?；與 cache 同一 apply 內原子替換）
- [file/F12] m5f: gen/tools.just（不進 git；gen/.stamp 不動）
- [end_ok/G12] m7: 0：接著跑原本的 recipe
- [other/LEGEND] p6c_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p6c_lg1 [legend]: 黃：判斷
- [other/LEGEND] p6c_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p6c_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p6c_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p6c_lg5 [legend]: 白：步驟
- [other/LEGEND] p6c_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p6c_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p6c_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p6c_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p6c_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p6c_lgx_img [legend]: 紫：image
- [other/LEGEND] p6c_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p6c_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p6c_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p6c_th: 本頁名詞
- [term/TERM_K] p6c_tk0: resolve／apply 兩段
- [term/TERM_V] p6c_tv0: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p6c_tk1: resolve 非 0
- [term/TERM_V] p6c_tv1: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p6c_tk2: gen/ 三種檔
- [term/TERM_V] p6c_tv2: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- [term/TERM_K] p6c_tk3: image tag／digest／docker image inspect
- [term/TERM_V] p6c_tv3: tag = 人看的版本名（可重 build）；digest = 從倉庫拉來的內容 sha256（鎖定用）；啟動器每次 docker run 前先 inspect：本機有 → 不 pull；引擎本機覆寫時 .Id 必須等於 version.local.toml 記的 image ID，否則 1（本機覆寫已失效）
- [term/TERM_K] p6c_tk4: verify／sha256
- [term/TERM_V] p6c_tv4: verify 把 cache/<repo>/ 每個檔的 sha256 跟印記比；不符 → 重裝一次 + warn，再驗仍不符 → 1 失敗（不無限重裝）；只在 sync --verify、CI 模式、或版本變動那次做；cache 缺或印記變了就直接重裝，apply 後再驗
- [term/TERM_K] p6c_tk5: 完成標記／基準版落後
- [term/TERM_V] p6c_tv5: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- [term/TERM_K] p6c_tk6: 6-33（未完成交易）
- [term/TERM_V] p6c_tv6: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- [term/TERM_K] p6c_tk7: GHCR／daemon／flock
- [term/TERM_V] p6c_tv7: GHCR = GitHub 容器倉庫；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎
- [term/TERM_K] p6c_tk8: 原 argv 與計畫一致
- [term/TERM_V] p6c_tv8: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- [term/TERM_K] p6c_tk9: 6-12（指紋不同）
- [term/TERM_V] p6c_tv9: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- [term/TERM_K] p6c_tk10: 6-38
- [term/TERM_V] p6c_tv10: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p6c_tk11: 6-24／6-31（pull 失敗）
- [term/TERM_V] p6c_tv11: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## edges
- m0a_n: m0a(是 → 對每個 extract：docker image i…) --無--> m0p(無：docker pull)
- m0g_p: m0g(<repo>-dist@digest （鎖定版；多架構 in…) --拉 /dist--> m0p(無：docker pull)
- m0p_x: m0p(無：docker pull) --(無標籤)--> m0b(extract：docker create <img> /x…)
- me0: m00(來自「sync（1′）」頁：有待辦（apply|yes；已寫…) --(無標籤)--> m0q(resolve 回 0 且 vk-resolve/1 文法合…)
- me0x: m0q(resolve 回 0 且 vk-resolve/1 文法合…) --否--> m0qx(1 + 6-30：stdout 文法不合；resolve 非…)
- me0a: m0q(resolve 回 0 且 vk-resolve/1 文法合…) --是--> m0a(是 → 對每個 extract：docker image i…)
- me0px: m0p(無：docker pull) --失敗--> m0px(1 + 6-24／6-31：pull 失敗／逾時)
- me0bx: m0b(extract：docker create <img> /x…) --失敗--> m0bx(1：extract 失敗（create／cp／rm 或暫存目…)
- me1: m0b(extract：docker create <img> /x…) --(無標籤)--> m1(docker run … -v <tmp>:/dist:ro…)
- me2: m1(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> m2a(apply：flock 專案目錄（60 秒；VENDOR_K…)
- me2b: m2a(apply：flock 專案目錄（60 秒；VENDOR_K…) --(無標籤)--> m2b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…)
- me2x: m2b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --不同--> m2x(1 + 6-12：指紋不同「請重跑」)
- me2c: m2b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --(無標籤)--> m2c(原 argv 與計畫一致？)
- me2cx: m2c(原 argv 與計畫一致？) --否--> m2cx(1：原 argv 與計畫不一致，請重跑)
- me3: m2c(原 argv 與計畫一致？) --是--> m3(逐待辦工具：取件 /dist/<repo> 展開到暫存目錄)
- me3c: m3(逐待辦工具：取件 /dist/<repo> 展開到暫存目錄) --(無標籤)--> m3c(暫存 → cache/<repo>/（原子替換）)
- me4: m3c(暫存 → cache/<repo>/（原子替換）) --寫--> m3f(cache/<repo>/（重寫，不進 git）)
- me4b: m3c(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> m3b(寫印記 gen/<repo>.stamp（第一行 index…)
- me4f: m3b(寫印記 gen/<repo>.stamp（第一行 index…) --寫--> m3bf(gen/<repo>.stamp（重寫，不進 git）)
- me4v: m3b(寫印記 gen/<repo>.stamp（第一行 index…) --(無標籤)--> m3vd(逐檔驗？（--verify／CI 模式／版本變動的那次）)
- me4vy: m3vd(逐檔驗？（--verify／CI 模式／版本變動的那次）) --是--> m3v(是：逐檔 sha256 驗 cache/<repo>/ ＝ …)
- me4vn: m3vd(逐檔驗？（--verify／CI 模式／版本變動的那次）) --否--> mq(還有待辦工具？)
- me4q: m3v(是：逐檔 sha256 驗 cache/<repo>/ ＝ …) --(無標籤)--> m3vq(全部相符？)
- me4n: m3vq(全部相符？) --否--> m3vn(否：重裝該工具一次 + warn（cache 被改過）)
- me5: m3vq(全部相符？) --是--> mq(還有待辦工具？)
- me5n: m3vn(否：重裝該工具一次 + warn（cache 被改過）) --(無標籤)--> m3v2(再逐檔驗一次)
- me5v2: m3v2(再逐檔驗一次) --(無標籤)--> m3vq2(相符？)
- me5x2: m3vq2(相符？) --否--> m3x2(1：重裝後仍不符（取件／寫入／驗證失敗），不再重裝)
- me5y2: m3vq2(相符？) --是--> mq(還有待辦工具？)
- me6y: mq(還有待辦工具？) --是：下一個工具--> m3(逐待辦工具：取件 /dist/<repo> 展開到暫存目錄)
- me6n: mq(還有待辦工具？) --否--> m5(否：重生 gen/tools.just（待辦有它時；每個 <…)
- me12: m5(否：重生 gen/tools.just（待辦有它時；每個 <…) --寫--> m5f(gen/tools.just（不進 git；gen/.sta…)
- me15: m5(否：重生 gen/tools.just（待辦有它時；每個 <…) --(無標籤)--> m7(0：接著跑原本的 recipe)
- me0y: m0a(是 → 對每個 extract：docker image i…) --有--> m0b(extract：docker create <img> /x…)

## terms
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- gen/ 三種檔: gen/tools.just：每個 <ns>.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／升引擎寫；gen/<repo>.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）
- image tag／digest／docker image inspect: tag = 人看的版本名（可重 build）；digest = 從倉庫拉來的內容 sha256（鎖定用）；啟動器每次 docker run 前先 inspect：本機有 → 不 pull；引擎本機覆寫時 .Id 必須等於 version.local.toml 記的 image ID，否則 1（本機覆寫已失效）
- verify／sha256: verify 把 cache/<repo>/ 每個檔的 sha256 跟印記比；不符 → 重裝一次 + warn，再驗仍不符 → 1 失敗（不無限重裝）；只在 sync --verify、CI 模式、或版本變動那次做；cache 缺或印記變了就直接重裝，apply 後再驗
- 完成標記／基準版落後: metadata 無完成標記 = add 沒做完 → 1 + 6-13「<repo> 未完成接入，請執行：just vendor_kit add <repo>」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 模式 → 1 + 6-5）；metadata 失蹤或不可解析 → 1 失敗
- 6-33（未完成交易）: 唯讀動詞（sync／update／help）偵測到 .tmp.<verb>.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；update 結束 1
- GHCR／daemon／flock: GHCR = GitHub 容器倉庫；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎
- 原 argv 與計畫一致: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- 6-12（指紋不同）: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## xrefs
- eB: 其他「sync（1′）」頁
- m00: 來自「sync（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7 -----
# v1p7  26 流程 v2：upgrade ── A. Renovate 路徑

nodes 71（不含 v2 小標）／edges 22／terms 11／xrefs 3

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── A. Renovate 路徑（§2／§7、v2.2 D、v2.3 §7、v2.5 §1／§7）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；唯一命中才問；零命中或多處 → 保留只 warn。已定（v2.5 §3／§6、v2.15-18）：apply 順序 = flock → 重驗指紋 → 驗 argv → dry-run 分支 → 建進度檔 → 清除衝突狀態與其他寫入 → 刪進度檔；逐檔判斷依 metadata state 分流；目標工具在本機覆寫中 → 1 先 undev。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uA [v2]: A. Renovate 路徑（下游自選，vendor_kit 不出 bot）：機器人只改 version.toml 一行；PR 的 CI 以新版跑完整流程（第一個失敗即停）；基準版落後 → PR 紅（需人補合併）；補合併在 PR 分支上完成、CI 綠後才 merge
- [end_ok/G12] a0: Renovate 定期查 GHCR
- [other/IMG] a1: <repo>-dist⏎出新 tag@digest
- [step/W12] a2: 開 PR（獨立分支）：只改 version.toml 該工具的版本鎖定行（tag@digest）
- [file/F12] a3: version.toml（PR 分支）⏎<repo> 版本鎖定行 = 新 tag@digest
- [step/W12] a4a: PR 的 CI 呼叫 .vendor_kit/ci/check.sh（以新版跑完整流程；每個動詞各自一份執行紀錄）
- [rule/RULE] a4r: 只看一行 diff 不足以證明升級可用（該行仍可能不合法或指向不存在的 ref）⏎→ PR 的 CI 必須以新版跑完整流程
- [step/W12] a4b: check.sh ①：sync（CI 模式；export CI=1）
- [end_orange/O12] a5 [v2]: 1 → PR 紅：需人處理（常見：基準版落後 6-5 → 本機 upgrade <repo> -y 後 push）
- [decision/D12] a4q [v2]: sync 通過？（基準版落後 6-5／薄殼不符 6-1／未完成接入 6-13／本機覆寫／未完成交易 6-33；見「sync（1′）」頁）
- [step/W12] a4c: 是：check.sh ②：verify
- [step/W12] a4d: check.sh ③：upgrade --dry-run
- [step/W12] a4e1: check.sh ④：工具測試
- [step/W12] a6a [v2]: PR 作者本機：切到 PR 分支
- [note/NOTE] a9: Renovate 預設不動有人推過的分支；PR body 加警告：勿勾 rebase（會蓋掉人補的合併 commit）。vendor_kit 無 bot。
- [step/W12] a4e2: check.sh ⑤：專案測試
- [step/W12] a6b [v2]: upgrade <repo> -y（走「B. 手動路徑（1）」頁，固定補到 PR 鎖定版）
- [end_orange/O12] a4fx [v2]: PR 紅：②～⑤ 第一個失敗即停止（印該步的錯誤／結束碼 2、3）
- [decision/D12] a4f [v2]: ②～⑤ 任一失敗或回 2／3？
- [step/W12] a6c: commit（合併結果）
- [step/W12] a6d: push 到 PR 分支
- [step/W12] a7: PR 分支 CI 再跑完整流程（同上）
- [end_orange/O12] a8qx [v2]: PR 紅：修到綠再 merge
- [decision/D12] a8q [v2]: 主線 CI 與 PR 分支 CI 都綠？
- [end_ok/G12] a8: 是：merge PR
- [other/LEGEND] p7_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7_lg5 [legend]: 白：步驟
- [other/LEGEND] p7_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p7_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7_lgx_img [legend]: 紫：image
- [other/LEGEND] p7_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7_th: 本頁名詞
- [term/TERM_K] p7_tk0: Renovate／regex manager
- [term/TERM_V] p7_tv0: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- [term/TERM_K] p7_tk1: PR／commit／push／rebase／merge
- [term/TERM_V] p7_tv1: PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線
- [term/TERM_K] p7_tk2: check.sh（PR CI）
- [term/TERM_V] p7_tv2: 下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1 = CI 模式）= sync → verify → upgrade --dry-run → 工具測試 → 專案測試；每個動詞各自一份執行紀錄（一次啟動器呼叫一檔）；第一個失敗即停止
- [term/TERM_K] p7_tk3: 基準版落後／待合併
- [term/TERM_V] p7_tv3: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- [term/TERM_K] p7_tk4: resolve／apply／--dry-run
- [term/TERM_V] p7_tv4: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- [term/TERM_K] p7_tk5: flock／指紋
- [term/TERM_V] p7_tv5: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7_tk6: B／D／N、逐檔判斷後詢問
- [term/TERM_V] p7_tv6: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- [term/TERM_K] p7_tk7: gen／mod?
- [term/TERM_V] p7_tv7: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- [term/TERM_K] p7_tk8: git merge-file --diff3
- [term/TERM_V] p7_tv8: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7_tk9: CRLF／append 行
- [term/TERM_V] p7_tv9: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- [term/TERM_K] p7_tk10: GHCR／tag@digest
- [term/TERM_V] p7_tv10: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）

## edges
- ae1: a0(Renovate 定期查 GHCR) --查--> a1(<repo>-dist 出新 tag@digest)
- ae2: a1(<repo>-dist 出新 tag@digest) --有新版--> a2(開 PR（獨立分支）：只改 version.toml 該工具…)
- ae3: a2(開 PR（獨立分支）：只改 version.toml 該工具…) --改一行--> a3(version.toml（PR 分支） <repo> 版本鎖…)
- ae4: a2(開 PR（獨立分支）：只改 version.toml 該工具…) --(無標籤)--> a4a(PR 的 CI 呼叫 .vendor_kit/ci/chec…)
- ae4b: a4a(PR 的 CI 呼叫 .vendor_kit/ci/chec…) --(無標籤)--> a4b(check.sh ①：sync（CI 模式；export C…)
- ae4q: a4b(check.sh ①：sync（CI 模式；export C…) --(無標籤)--> a4q(sync 通過？（基準版落後 6-5／薄殼不符 6-1／未完…)
- ae5: a4q(sync 通過？（基準版落後 6-5／薄殼不符 6-1／未完…) --否--> a5(1 → PR 紅：需人處理（常見：基準版落後 6-5 → 本…)
- ae5n: a4q(sync 通過？（基準版落後 6-5／薄殼不符 6-1／未完…) --是--> a4c(是：check.sh ②：verify)
- ae5c: a4c(是：check.sh ②：verify) --(無標籤)--> a4d(check.sh ③：upgrade --dry-run)
- ae5d: a4d(check.sh ③：upgrade --dry-run) --(無標籤)--> a4e1(check.sh ④：工具測試)
- ae5e: a4e1(check.sh ④：工具測試) --(無標籤)--> a4e2(check.sh ⑤：專案測試)
- ae6: a5(1 → PR 紅：需人處理（常見：基準版落後 6-5 → 本…) --(無標籤)--> a6a(PR 作者本機：切到 PR 分支)
- ae6b: a6a(PR 作者本機：切到 PR 分支) --(無標籤)--> a6b(upgrade <repo> -y（走「B. 手動路徑（1）…)
- ae6c: a6b(upgrade <repo> -y（走「B. 手動路徑（1）…) --(無標籤)--> a6c(commit（合併結果）)
- ae6d: a6c(commit（合併結果）) --(無標籤)--> a6d(push 到 PR 分支)
- ae7: a6d(push 到 PR 分支) --(無標籤)--> a7(PR 分支 CI 再跑完整流程（同上）)
- ae8: a4e2(check.sh ⑤：專案測試) --(無標籤)--> a4f(②～⑤ 任一失敗或回 2／3？)
- ae8x: a4f(②～⑤ 任一失敗或回 2／3？) --是--> a4fx(PR 紅：②～⑤ 第一個失敗即停止（印該步的錯誤／結束碼 2…)
- ae8n: a4f(②～⑤ 任一失敗或回 2／3？) --否--> a8q(主線 CI 與 PR 分支 CI 都綠？)
- ae9: a7(PR 分支 CI 再跑完整流程（同上）) --(無標籤)--> a8q(主線 CI 與 PR 分支 CI 都綠？)
- ae10x: a8q(主線 CI 與 PR 分支 CI 都綠？) --否--> a8qx(PR 紅：修到綠再 merge)
- ae10: a8q(主線 CI 與 PR 分支 CI 都綠？) --是--> a8(是：merge PR)

## terms
- Renovate／regex manager: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- PR／commit／push／rebase／merge: PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線
- check.sh（PR CI）: 下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1 = CI 模式）= sync → verify → upgrade --dry-run → 工具測試 → 專案測試；每個動詞各自一份執行紀錄（一次啟動器呼叫一檔）；第一個失敗即停止
- 基準版落後／待合併: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- B／D／N、逐檔判斷後詢問: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- gen／mod?: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- CRLF／append 行: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- GHCR／tag@digest: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）

## xrefs
- a4q: 見「sync（1′）」頁
- a6b: 其他「B. 手動路徑（1）」頁
- p7_tv6: 見「逐檔判斷」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #e1d5e7 #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7c -----
# v1p7c  27 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker

nodes 70（不含 v2 小標）／edges 25／terms 10／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── B. 手動路徑（1）resolve（§2、v2.2 C／D、v2.5 §2／§3／§6）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；唯一命中才問；零命中或多處 → 保留只 warn。已定（v2.5 §3／§6、v2.15-18）：apply 順序 = flock → 重驗指紋 → 驗 argv → dry-run 分支 → 建進度檔 → 清除衝突狀態與其他寫入 → 刪進度檔；逐檔判斷依 metadata state 分流；目標工具在本機覆寫中 → 1 先 undev。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uB [v2]: B. 手動路徑：upgrade <repo>[@<tag>]（單一工具；不帶 repo 的多工具與升引擎見「E. 升引擎」頁 (a)：完整預檢後每個工具走本頁）= resolve（不寫；查 registry 無憑證 → 6-3）→ stdout 只傳協定內容；docker 段與 apply 前置見「B（1′）」頁
- [end_ok/G12] b0: just vendor_kit upgrade <repo>[@<tag>]（-y…）
- [step/W12] b0l [v2]: 建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入）
- [end_red/R12] b0x [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [step/W12] b1 [v2]: docker run <引擎> resolve upgrade <repo>⏎（啟動器不鎖）
- [step/SUB] b1e [v2]: resolve（不寫任何檔）：讀 version.toml、version.local.toml、metadata
- [end_orange/O12] b1x [v2]: 1：請先 undev <repo>（本機覆寫中）
- [decision/D12] b1q [v2]: <repo> 在本機覆寫（dev）中？
- [end_orange/O12] b2c [v2]: 2：先解完衝突再重跑
- [decision/D12] b2 [v2]: 否 → (0) conflicts 中的檔仍含我們的標籤，或檔案失蹤？
- [note/NOTE] b2n: 標籤 = 我們自己產的 <<<<<<< vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建進度檔之後（v2.5 §3）
- [end_orange/O12] b5: 1：無基準版，請先 add <repo>
- [decision/D12] b4: 否 → 有 baseline/<repo>/？
- [decision/D12] b6 [v2]: (1) 有待合併？
- [step/SUB] b6y [v2]: 是：目標版 = B（version.toml 那版），補到就停，不查最新
- [decision/D12] b7a [v2]: 否 → 指定 @<tag>？
- [step/SUB] b7t [v2]: 是：目標版 = @<tag>（比現版舊 → warn 仍執行）
- [decision/D12] b7b [v2]: 否 → CI 模式？
- [step/SUB] b7z [v2]: 是：不查最新；目標版 = 鎖定版
- [end_ok/G12] b7zz [v2]: 0：無待合併、無事可做（apply|no，不起 apply）
- [step/SUB] b7c [v2]: 否：(2) 查 registry 最新正式版 = 目標版
- [end_orange/O12] b7x [v2]: 1 + 6-3：查 registry 需要憑證但沒有，請指定 @<tag> 或提供憑證
- [decision/D12] b7q [v2]: 查 registry 需憑證但沒有？（只在查最新版時；docker pull 的認證另計 6-24）
- [step/SUB] b7s [v2]: 否：產生輸入指紋（同 add（1）頁「輸入指紋」）
- [step/SUB] b7s2 [v2]: stdout vk-resolve/1：extract 目標 tag@digest、apply|yes、指紋（只傳協定內容）
- [entry/ENTRY] b8z: 續「B（1′）」頁：啟動器驗 vk-resolve → inspect → pull → extract → apply 前置
- [other/LEGEND] p7c_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7c_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7c_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7c_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7c_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7c_lg5 [legend]: 白：步驟
- [other/LEGEND] p7c_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7c_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7c_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7c_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7c_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7c_lgx_img [legend]: 紫：image
- [other/LEGEND] p7c_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7c_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7c_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7c_th: 本頁名詞
- [term/TERM_K] p7c_tk0: Renovate／regex manager
- [term/TERM_V] p7c_tv0: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- [term/TERM_K] p7c_tk1: PR／commit／push／rebase／merge
- [term/TERM_V] p7c_tv1: PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線
- [term/TERM_K] p7c_tk2: 基準版落後／待合併
- [term/TERM_V] p7c_tv2: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- [term/TERM_K] p7c_tk3: resolve／apply／--dry-run
- [term/TERM_V] p7c_tv3: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- [term/TERM_K] p7c_tk4: flock／指紋
- [term/TERM_V] p7c_tv4: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7c_tk5: B／D／N、逐檔判斷後詢問
- [term/TERM_V] p7c_tv5: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- [term/TERM_K] p7c_tk6: git merge-file --diff3
- [term/TERM_V] p7c_tv6: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7c_tk7: GHCR／tag@digest
- [term/TERM_V] p7c_tv7: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- [term/TERM_K] p7c_tk8: resolve 非 0
- [term/TERM_V] p7c_tv8: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p7c_tk9: 6-38
- [term/TERM_V] p7c_tv9: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## edges
- be1: b0(just vendor_kit upgrade <repo>…) --(無標籤)--> b0l(建執行紀錄、寫 launcher_started（失敗 → …)
- be1x: b0l(建執行紀錄、寫 launcher_started（失敗 → …) --失敗--> b0x(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- be1l: b0l(建執行紀錄、寫 launcher_started（失敗 → …) --(無標籤)--> b1(docker run <引擎> resolve upgrad…)
- be1e: b1(docker run <引擎> resolve upgrad…) --(無標籤)--> b1e(resolve（不寫任何檔）：讀 version.toml、…)
- be1q: b1e(resolve（不寫任何檔）：讀 version.toml、…) --(無標籤)--> b1q(<repo> 在本機覆寫（dev）中？)
- be1qx: b1q(<repo> 在本機覆寫（dev）中？) --是--> b1x(1：請先 undev <repo>（本機覆寫中）)
- be2: b1q(<repo> 在本機覆寫（dev）中？) --否--> b2(否 → (0) conflicts 中的檔仍含我們的標籤，或…)
- be3: b2(否 → (0) conflicts 中的檔仍含我們的標籤，或…) --是--> b2c(2：先解完衝突再重跑)
- be4: b2(否 → (0) conflicts 中的檔仍含我們的標籤，或…) --否--> b4(否 → 有 baseline/<repo>/？)
- be5: b4(否 → 有 baseline/<repo>/？) --否--> b5(1：無基準版，請先 add <repo>)
- be6: b4(否 → 有 baseline/<repo>/？) --是--> b6((1) 有待合併？)
- be7: b6((1) 有待合併？) --是--> b6y(是：目標版 = B（version.toml 那版），補到就…)
- be8: b6((1) 有待合併？) --否--> b7a(否 → 指定 @<tag>？)
- be8t: b7a(否 → 指定 @<tag>？) --是--> b7t(是：目標版 = @<tag>（比現版舊 → warn 仍執行…)
- be8b: b7a(否 → 指定 @<tag>？) --否--> b7b(否 → CI 模式？)
- be8z: b7b(否 → CI 模式？) --是--> b7z(是：不查最新；目標版 = 鎖定版)
- be8c: b7b(否 → CI 模式？) --否--> b7c(否：(2) 查 registry 最新正式版 = 目標版)
- be8zz: b7z(是：不查最新；目標版 = 鎖定版) --(無標籤)--> b7zz(0：無待合併、無事可做（apply|no，不起 apply）)
- be9: b6y(是：目標版 = B（version.toml 那版），補到就…) --(無標籤)--> b7s(否：產生輸入指紋（同 add（1）頁「輸入指紋」）)
- be9t: b7t(是：目標版 = @<tag>（比現版舊 → warn 仍執行…) --(無標籤)--> b7s(否：產生輸入指紋（同 add（1）頁「輸入指紋」）)
- be10: b7c(否：(2) 查 registry 最新正式版 = 目標版) --(無標籤)--> b7q(查 registry 需憑證但沒有？（只在查最新版時；doc…)
- be10x: b7q(查 registry 需憑證但沒有？（只在查最新版時；doc…) --是--> b7x(1 + 6-3：查 registry 需要憑證但沒有，請指定…)
- be10n: b7q(查 registry 需憑證但沒有？（只在查最新版時；doc…) --否--> b7s(否：產生輸入指紋（同 add（1）頁「輸入指紋」）)
- be11: b7s(否：產生輸入指紋（同 add（1）頁「輸入指紋」）) --(無標籤)--> b7s2(stdout vk-resolve/1：extract 目標…)
- be12: b7s2(stdout vk-resolve/1：extract 目標…) --(無標籤)--> b8z(續「B（1′）」頁：啟動器驗 vk-resolve → in…)

## terms
- Renovate／regex manager: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- PR／commit／push／rebase／merge: PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線
- 基準版落後／待合併: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- B／D／N、逐檔判斷後詢問: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- GHCR／tag@digest: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## xrefs
- uB: 見「E. 升引擎」頁
- uB: 見「B（1′）」頁
- b8z: 續「B（1′）」頁
- p7c_tv5: 見「逐檔判斷」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7ccc -----
# v1p7ccc  28 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置

nodes 76（不含 v2 小標）／edges 25／terms 13／xrefs 7

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── B. 手動路徑（1′）docker → apply 前置（§2、v2.5 §3／§5、v2.15-4）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；唯一命中才問；零命中或多處 → 保留只 warn。已定（v2.5 §3／§6、v2.15-18）：apply 順序 = flock → 重驗指紋 → 驗 argv → dry-run 分支 → 建進度檔 → 清除衝突狀態與其他寫入 → 刪進度檔；逐檔判斷依 metadata state 分流；目標工具在本機覆寫中 → 1 先 undev。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uB1 [v2]: B（1′）docker 段與 apply 前置（承「B（1）」頁）：resolve 回 0？→ inspect → 無才 pull → extract → apply → 拿鎖 → 重驗 → argv 一致 → dest／命名空間 → 逐檔狀態機只算會問的項目 → CI 模式 → dry-run；寫入段見「B（2）」頁
- [entry/ENTRY] b8e: 來自「B（1）」頁：resolve 容器已結束（已寫 launcher_started）
- [end_red/R12] b8qx [v2]: 1 + 6-30：stdout 文法不合；resolve 非 0 → 原碼傳出（不跑 docker／apply）
- [decision/D12] b8q [v2]: resolve 回 0 且 vk-resolve/1 文法合法？
- [decision/D12] b8a [v2]: 是 → inspect：本機有？
- [step/W12] b8p [v2]: 無：docker pull
- [other/IMG] b8g: <repo>-dist⏎目標 tag@digest
- [step/W12] b8b [v2]: extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm
- [end_red/R12] b8px [v2]: 1 + 6-24／6-31：pull 失敗／逾時
- [end_red/R12] b8bx [v2]: 1：extract 失敗（create／cp／rm 或暫存目錄）
- [step/W12] b9 [v2]: docker run … -v <tmp>:/dist:ro（含 vk-resolve）<引擎> apply upgrade <repo>（--dry-run 原樣轉發）
- [step/SUB] b10a [v2]: apply：flock 專案目錄（60 秒）
- [end_orange/O12] b10x [v2]: 1 + 6-12：指紋不同「請重跑」
- [decision/D12] b10b [v2]: 重驗 resolve 的輸入指紋（讀 /dist/vk-resolve）：相同？
- [end_orange/O12] b10cx [v2]: 1：原 argv 與計畫不一致，請重跑
- [decision/D12] b10c2 [v2]: 原 argv 與計畫一致？
- [end_orange/O12] b10dx [v2]: 1：dest 不合法
- [decision/D12] b10d [v2]: 是 → 新版 init.toml 的 dest 全部合法？（規則同「add（1′）」頁，含父目錄不得經 symlink）
- [end_orange/O12] b10nx [v2]: 1：命名空間撞名（upgrade 回 1）
- [decision/D12] b10n [v2]: 是 → 新版 <ns> 撞名？（其他工具／根 justfile recipe／module／alias／保留名）
- [step/SUB] b10c [v2]: 否 → 逐檔依 metadata state 分流（B／D／N，見「逐檔判斷」頁）：只計算會問的項目，不發問
- [end_orange/O12] b12x [v2]: 1：印需改清單（CI 模式；本機執行後 commit、push）
- [decision/D12] b12 [v2]: CI 模式且需改任何進 git 的檔？
- [end_ok/G12] b11y [v2]: 0：唯讀預覽（印會問哪些檔；6-6／6-7／6-8 提醒）
- [decision/D12] b11: --dry-run？
- [entry/ENTRY] b11z: 續「B（2）」頁：apply 寫入段（非 dry-run）
- [other/LEGEND] p7cp_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7cp_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7cp_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7cp_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7cp_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7cp_lg5 [legend]: 白：步驟
- [other/LEGEND] p7cp_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7cp_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7cp_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7cp_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7cp_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7cp_lgx_img [legend]: 紫：image
- [other/LEGEND] p7cp_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7cp_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7cp_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7cp_th: 本頁名詞
- [term/TERM_K] p7cp_tk0: Renovate／regex manager
- [term/TERM_V] p7cp_tv0: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- [term/TERM_K] p7cp_tk1: resolve／apply／--dry-run
- [term/TERM_V] p7cp_tv1: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- [term/TERM_K] p7cp_tk2: flock／指紋
- [term/TERM_V] p7cp_tv2: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7cp_tk3: B／D／N、逐檔判斷後詢問
- [term/TERM_V] p7cp_tv3: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- [term/TERM_K] p7cp_tk4: git merge-file --diff3
- [term/TERM_V] p7cp_tv4: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7cp_tk5: GHCR／tag@digest
- [term/TERM_V] p7cp_tv5: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- [term/TERM_K] p7cp_tk6: resolve 非 0
- [term/TERM_V] p7cp_tv6: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p7cp_tk7: 原 argv 與計畫一致
- [term/TERM_V] p7cp_tv7: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- [term/TERM_K] p7cp_tk8: 6-12（指紋不同）
- [term/TERM_V] p7cp_tv8: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- [term/TERM_K] p7cp_tk9: 6-38
- [term/TERM_V] p7cp_tv9: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7cp_tk10: dest 撞名
- [term/TERM_V] p7cp_tv10: 兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 正規化不得越出 dist
- [term/TERM_K] p7cp_tk11: 命名空間撞名（v2.5 §5）
- [term/TERM_V] p7cp_tv11: 下游 dist/just/<ns>.just 的 <ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（以 just --dump --dump-format json 取得）(c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）
- [term/TERM_K] p7cp_tk12: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7cp_tv12: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## edges
- b8a_n: b8a(是 → inspect：本機有？) --無--> b8p(無：docker pull)
- b8g_p: b8g(<repo>-dist 目標 tag@digest) --拉 /dist--> b8p(無：docker pull)
- b8p_x: b8p(無：docker pull) --(無標籤)--> b8b(extract：docker create <img> /x…)
- be13e: b8e(來自「B（1）」頁：resolve 容器已結束（已寫 lau…) --(無標籤)--> b8q(resolve 回 0 且 vk-resolve/1 文法合…)
- be13x: b8q(resolve 回 0 且 vk-resolve/1 文法合…) --否--> b8qx(1 + 6-30：stdout 文法不合；resolve 非…)
- be13a: b8q(resolve 回 0 且 vk-resolve/1 文法合…) --是--> b8a(是 → inspect：本機有？)
- be11px: b8p(無：docker pull) --失敗--> b8px(1 + 6-24／6-31：pull 失敗／逾時)
- be12bx: b8b(extract：docker create <img> /x…) --失敗--> b8bx(1：extract 失敗（create／cp／rm 或暫存目…)
- be13: b8b(extract：docker create <img> /x…) --(無標籤)--> b9(docker run … -v <tmp>:/dist:ro…)
- be14: b9(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> b10a(apply：flock 專案目錄（60 秒）)
- be15: b10a(apply：flock 專案目錄（60 秒）) --(無標籤)--> b10b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…)
- be15x: b10b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --否--> b10x(1 + 6-12：指紋不同「請重跑」)
- be15c: b10b(重驗 resolve 的輸入指紋（讀 /dist/vk-re…) --是--> b10c2(原 argv 與計畫一致？)
- be15cx: b10c2(原 argv 與計畫一致？) --否--> b10cx(1：原 argv 與計畫不一致，請重跑)
- be15b: b10c2(原 argv 與計畫一致？) --是--> b10d(是 → 新版 init.toml 的 dest 全部合法？（…)
- be15d: b10d(是 → 新版 init.toml 的 dest 全部合法？（…) --否--> b10dx(1：dest 不合法)
- be15n: b10d(是 → 新版 init.toml 的 dest 全部合法？（…) --是--> b10n(是 → 新版 <ns> 撞名？（其他工具／根 justfil…)
- be15nx: b10n(是 → 新版 <ns> 撞名？（其他工具／根 justfil…) --是--> b10nx(1：命名空間撞名（upgrade 回 1）)
- be15cc: b10n(是 → 新版 <ns> 撞名？（其他工具／根 justfil…) --否--> b10c(否 → 逐檔依 metadata state 分流（B／D／…)
- be15e: b10c(否 → 逐檔依 metadata state 分流（B／D／…) --(無標籤)--> b12(CI 模式且需改任何進 git 的檔？)
- be16: b12(CI 模式且需改任何進 git 的檔？) --是--> b12x(1：印需改清單（CI 模式；本機執行後 commit、pus…)
- be17: b12(CI 模式且需改任何進 git 的檔？) --否--> b11(--dry-run？)
- be18: b11(--dry-run？) --是--> b11y(0：唯讀預覽（印會問哪些檔；6-6／6-7／6-8 提醒）)
- be19: b11(--dry-run？) --否--> b11z(續「B（2）」頁：apply 寫入段（非 dry-run）)
- be11y: b8a(是 → inspect：本機有？) --有--> b8b(extract：docker create <img> /x…)

## terms
- Renovate／regex manager: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- B／D／N、逐檔判斷後詢問: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- GHCR／tag@digest: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- 原 argv 與計畫一致: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- 6-12（指紋不同）: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- dest 撞名: 兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 正規化不得越出 dist
- 命名空間撞名（v2.5 §5）: 下游 dist/just/<ns>.just 的 <ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（以 just --dump --dump-format json 取得）(c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## xrefs
- uB1: 其他「B（1）」頁
- uB1: 見「B（2）」頁
- b8e: 來自「B（1）」頁
- b10d: 其他「add（1′）」頁
- b10c: 見「逐檔判斷」頁
- b11z: 續「B（2）」頁
- p7cp_tv3: 見「逐檔判斷」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7cc -----
# v1p7cc  29 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併

nodes 82（不含 v2 小標）／edges 37／terms 11／xrefs 8

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併（§5、v2.5 §2～§4、v2.15-18）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；唯一命中才問；零命中或多處 → 保留只 warn。已定（v2.5 §3／§6、v2.15-18）：apply 順序 = flock → 重驗指紋 → 驗 argv → dry-run 分支 → 建進度檔 → 清除衝突狀態與其他寫入 → 刪進度檔；逐檔判斷依 metadata state 分流；目標工具在本機覆寫中 → 1 先 undev。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uB2 [v2]: B（2）apply 寫入段前半（承「B（1′）」頁）：建進度檔 → 清衝突狀態 → 取件 → 印記 → 逐檔迴圈：依 state 分流（「逐檔判斷」頁）→ 要問？→ 問 6-22 → 同意？→ 依情況在暫存套用 → 還有下一個檔？→ 解析檢查 → 通過才原子替換；收尾見「B（2′）」頁
- [entry/ENTRY] b10z: 來自「B（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_started）
- [step/SUB] b10e [v2]: 建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）
- [file/F12] b10ef: baseline/<repo>/.vendor_kit.toml（[progress]）
- [step/SUB] b10f [v2]: (0) 判定已解 → 清除 metadata 的衝突狀態（有的話）
- [file/F12] b10ff: .vendor_kit.toml（conflicts 清空）
- [step/SUB] b13a [v2]: 取件目標版：/dist/<repo> 複製到暫存目錄
- [step/SUB] b13ac [v2]: 暫存 → cache/<repo>/（原子替換）
- [file/F12] b13f: cache/<repo>/（目標版，不進 git）
- [step/SUB] b13b [v2]: 寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）
- [file/F12] b13bf: gen/<repo>.stamp（不進 git）
- [step/SUB] b14s [v2]: 逐檔（init.toml 每個 [[file]]＋metadata 每個 dest）：依 state 分流（狀態機見「逐檔判斷」頁）→ 結果 = 不動／warn 或問 6-22
- [decision/D12] b14q [v2]: 結果 = 要問？
- [step/SUB] b14n2 [v2]: 否：不動／warn（依狀態機；不記拒絕）
- [step/SUB] b14ask [v2]: 是：問 6-22（情況對應的問句：換成新版？／三方合併？／要建 X 嗎／二進位換版？／替換 append 行？；-y 免問）
- [decision/D12] b14y [v2]: 同意？
- [step/SUB] b14n [v2]: 否：不動（拒絕；「B（2′）」頁記 declined_hash）
- [rule/RULE] b14r [v2]: Q14／Q15、v2.7 §3：拒絕 → 已納管檔 state 不變、只記 declined_hash（N 的 hash 變了才再問，相同不再問）；新檔（B 無）被拒 → state=declined；dry-run／check.sh 印 6-6／6-8
- [decision/D12] b14d1 [v2]: 是 → 新檔（B 無）？
- [step/SUB] b14a1 [v2]: 是：建新檔到暫存（state=managed）
- [decision/D12] b14d2 [v2]: 否 → append 行？
- [step/SUB] b14a2 [v2]: 是：替換上次插入的行（暫存）
- [decision/D12] b14d3 [v2]: 否 → 兩邊都改（三者皆異）？
- [step/SUB] b14a3 [v2]: 是：git merge-file --diff3（暫存）
- [step/SUB] b14a4 [v2]: 否：換成新版 N（暫存；二進位／symlink 同）
- [decision/D12] b14l [v2]: 還有下一個檔？
- [step/SUB] b14m [v2]: 否：暫存合併完成（每檔已定；都還在暫存）→ TOML／just 等可解析格式重新解析
- [decision/D12] b14pq [v2]: 可解析格式：重新解析失敗？
- [step/SUB] b14pc [v2]: 是：該檔留原檔
- [step/SUB] b14pc2 [v2]: 記 conflicts（metadata；該檔基準版不推）
- [step/SUB] b14w [v2]: 否：通過的檔逐檔原子替換（暫存 → 正式位置）
- [file/F12] b14f: 初始檔（合併後；衝突留 <<<<<<< vendor_kit:baseline 標記）
- [entry/ENTRY] b14z: 續「B（2′）」頁：基準版（解析失敗的檔不推）→ metadata → tools.just → version.toml → 刪進度檔
- [rule/RULE] b14y_tty: 無tty→6-4
- [other/LEGEND] p7cc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7cc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7cc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7cc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7cc_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7cc_lg5 [legend]: 白：步驟
- [other/LEGEND] p7cc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7cc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7cc_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7cc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7cc_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p7cc_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7cc_lgx_img [legend]: 紫：image
- [other/LEGEND] p7cc_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7cc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/LEGEND] p7cc_lgx_tty [legend]: 橙小標：問句無 tty／EOF 且無 -y → 1 + 6-4（Ctrl-C 中止、不記拒絕）
- [other/TEXT] p7cc_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7cc_th: 本頁名詞
- [term/TERM_K] p7cc_tk0: 基準版落後／待合併
- [term/TERM_V] p7cc_tv0: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- [term/TERM_K] p7cc_tk1: resolve／apply／--dry-run
- [term/TERM_V] p7cc_tv1: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- [term/TERM_K] p7cc_tk2: flock／指紋
- [term/TERM_V] p7cc_tv2: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7cc_tk3: B／D／N、逐檔判斷後詢問
- [term/TERM_V] p7cc_tv3: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- [term/TERM_K] p7cc_tk4: gen／mod?
- [term/TERM_V] p7cc_tv4: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- [term/TERM_K] p7cc_tk5: git merge-file --diff3
- [term/TERM_V] p7cc_tv5: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7cc_tk6: CRLF／append 行
- [term/TERM_V] p7cc_tv6: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- [term/TERM_K] p7cc_tk7: GHCR／tag@digest
- [term/TERM_V] p7cc_tv7: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- [term/TERM_K] p7cc_tk8: 6-38
- [term/TERM_V] p7cc_tv8: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7cc_tk9: 6-22（upgrade 逐檔問句）
- [term/TERM_V] p7cc_tv9: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問
- [term/TERM_K] p7cc_tk10: 6-4（無 tty）
- [term/TERM_V] p7cc_tv10: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## edges
- be20: b10z(來自「B（1′）」頁：apply 檢查通過（非 dry-ru…) --(無標籤)--> b10e(建進度檔：metadata [progress]（state…)
- be20f: b10e(建進度檔：metadata [progress]（state…) --寫--> b10ef(baseline/<repo>/.vendor_kit.to…)
- be20b: b10e(建進度檔：metadata [progress]（state…) --(無標籤)--> b10f((0) 判定已解 → 清除 metadata 的衝突狀態（有…)
- be20ff: b10f((0) 判定已解 → 清除 metadata 的衝突狀態（有…) --寫--> b10ff(.vendor_kit.toml（conflicts 清空）)
- be21: b10f((0) 判定已解 → 清除 metadata 的衝突狀態（有…) --(無標籤)--> b13a(取件目標版：/dist/<repo> 複製到暫存目錄)
- be21a: b13a(取件目標版：/dist/<repo> 複製到暫存目錄) --(無標籤)--> b13ac(暫存 → cache/<repo>/（原子替換）)
- be21f: b13ac(暫存 → cache/<repo>/（原子替換）) --寫--> b13f(cache/<repo>/（目標版，不進 git）)
- be21b: b13ac(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> b13b(寫印記 gen/<repo>.stamp（第一行 index…)
- be21bf: b13b(寫印記 gen/<repo>.stamp（第一行 index…) --寫--> b13bf(gen/<repo>.stamp（不進 git）)
- be22: b13b(寫印記 gen/<repo>.stamp（第一行 index…) --(無標籤)--> b14s(逐檔（init.toml 每個 [[file]]＋metad…)
- be22a: b14s(逐檔（init.toml 每個 [[file]]＋metad…) --(無標籤)--> b14q(結果 = 要問？)
- be22n: b14q(結果 = 要問？) --否--> b14n2(否：不動／warn（依狀態機；不記拒絕）)
- be22y: b14q(結果 = 要問？) --是--> b14ask(是：問 6-22（情況對應的問句：換成新版？／三方合併？／要…)
- be22ay: b14ask(是：問 6-22（情況對應的問句：換成新版？／三方合併？／要…) --(無標籤)--> b14y(同意？)
- be23n: b14y(同意？) --否--> b14n(否：不動（拒絕；「B（2′）」頁記 declined_has…)
- be23y: b14y(同意？) --是--> b14d1(是 → 新檔（B 無）？)
- be23a1: b14d1(是 → 新檔（B 無）？) --是--> b14a1(是：建新檔到暫存（state=managed）)
- be23d2: b14d1(是 → 新檔（B 無）？) --否--> b14d2(否 → append 行？)
- be23a2: b14d2(否 → append 行？) --是--> b14a2(是：替換上次插入的行（暫存）)
- be23d3: b14d2(否 → append 行？) --否--> b14d3(否 → 兩邊都改（三者皆異）？)
- be23a3: b14d3(否 → 兩邊都改（三者皆異）？) --是--> b14a3(是：git merge-file --diff3（暫存）)
- be23a4: b14d3(否 → 兩邊都改（三者皆異）？) --否--> b14a4(否：換成新版 N（暫存；二進位／symlink 同）)
- be23l: b14a4(否：換成新版 N（暫存；二進位／symlink 同）) --(無標籤)--> b14l(還有下一個檔？)
- be23r0: b14n2(否：不動／warn（依狀態機；不記拒絕）) --(無標籤)--> b14l(還有下一個檔？)
- be23r1: b14n(否：不動（拒絕；「B（2′）」頁記 declined_has…) --(無標籤)--> b14l(還有下一個檔？)
- be23r2: b14a1(是：建新檔到暫存（state=managed）) --(無標籤)--> b14l(還有下一個檔？)
- be23r3: b14a2(是：替換上次插入的行（暫存）) --(無標籤)--> b14l(還有下一個檔？)
- be23r4: b14a3(是：git merge-file --diff3（暫存）) --(無標籤)--> b14l(還有下一個檔？)
- be23ll: b14l(還有下一個檔？) --是--> b14s(逐檔（init.toml 每個 [[file]]＋metad…)
- be23m: b14l(還有下一個檔？) --否--> b14m(否：暫存合併完成（每檔已定；都還在暫存）→ TOML／jus…)
- be23pq: b14m(否：暫存合併完成（每檔已定；都還在暫存）→ TOML／jus…) --(無標籤)--> b14pq(可解析格式：重新解析失敗？)
- be23pc: b14pq(可解析格式：重新解析失敗？) --是--> b14pc(是：該檔留原檔)
- be23pc2: b14pc(是：該檔留原檔) --(無標籤)--> b14pc2(記 conflicts（metadata；該檔基準版不推）)
- be23pw: b14pq(可解析格式：重新解析失敗？) --否--> b14w(否：通過的檔逐檔原子替換（暫存 → 正式位置）)
- be22f: b14w(否：通過的檔逐檔原子替換（暫存 → 正式位置）) --寫--> b14f(初始檔（合併後；衝突留 <<<<<<< vendor_kit…)
- be23z: b14w(否：通過的檔逐檔原子替換（暫存 → 正式位置）) --(無標籤)--> b14z(續「B（2′）」頁：基準版（解析失敗的檔不推）→ metad…)
- be23pz: b14pc2(記 conflicts（metadata；該檔基準版不推）) --(無標籤)--> b14z(續「B（2′）」頁：基準版（解析失敗的檔不推）→ metad…)

## terms
- 基準版落後／待合併: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- B／D／N、逐檔判斷後詢問: B = 基準版（上次合併的範本）、D = 現況（專案檔）、N = 目標版範本（暫存 /dist/<repo>，不是 cache）；依 metadata state 分流的狀態機（見「逐檔判斷」頁）決定不動／warn／問 6-22；-y 免問；拒絕 → 不動、記 declined_hash，新檔被拒才 state=declined
- gen／mod?: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- CRLF／append 行: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- GHCR／tag@digest: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-22（upgrade 逐檔問句）: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問
- 6-4（無 tty）: 需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）

## xrefs
- uB2: 其他「B（1′）」頁
- uB2: 其他「逐檔判斷」頁
- uB2: 見「B（2′）」頁
- b10z: 來自「B（1′）」頁
- b14s: 見「逐檔判斷」頁
- b14n: 其他「B（2′）」頁
- b14z: 續「B（2′）」頁
- p7cc_tv3: 見「逐檔判斷」頁

## fills（非圖例）: #FFF4C3 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7cccc -----
# v1p7cccc  30 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入

nodes 64（不含 v2 小標）／edges 21／terms 8／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入（§5、v2.2 D、v2.5 §3／§4、v2.6 Q27）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；唯一命中才問；零命中或多處 → 保留只 warn。已定（v2.5 §3／§6、v2.15-18）：apply 順序 = flock → 重驗指紋 → 驗 argv → dry-run 分支 → 建進度檔 → 清除衝突狀態與其他寫入 → 刪進度檔；逐檔判斷依 metadata state 分流；目標工具在本機覆寫中 → 1 先 undev。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uB3 [v2]: B（2′）apply 寫入段後半（承「B（2）」頁：通過解析的檔已替換；解析失敗的檔留原檔、已記 conflicts）：推基準版（解析失敗的檔不推）→ metadata → tools.just（原子替換）→ 待合併？否 → 寫 version.toml → 刪進度檔 → 0／2
- [entry/ENTRY] b15z: 來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原檔、已記 conflicts（已寫 launcher_started）
- [step/SUB] b15a [v2]: 推 baseline/<repo>/ 到目標版：逐檔，通過的檔推到 N（有衝突標記也推）；解析失敗的檔跳過不推（該檔基準版留上一版）
- [file/F12] b15f: baseline/<repo>/（目標版範本副本，進 git；解析失敗的檔留上一版）
- [step/SUB] b15b [v2]: 寫 metadata：source = 目標版（= 最後合併版本；解析失敗的檔另在 conflicts，其基準版留舊版）
- [file/F12] b15bf: baseline/<repo>/.vendor_kit.toml（source；進 git）
- [step/SUB] b15c [v2]: 寫 metadata：conflicts（有衝突標記或解析失敗的 dest 清單）
- [file/F12] b15cf: .vendor_kit.toml（conflicts）
- [step/SUB] b15d [v2]: 寫 metadata：每個 dest 的 state／declined_hash／lines —— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined
- [file/F12] b15df: .vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）
- [step/SUB] b15g [v2]: 重生 gen/tools.just（新版的 just/<ns>.just 可能增減；原子替換，與本次 cache 同一 apply 內，I17）
- [file/F12] b15gf: gen/tools.just（不進 git；mod? 行）
- [decision/D12] b16q0 [v2]: 待合併（version.toml 已是目標版 B）？
- [step/SUB] b16 [v2]: 否：寫 version.toml <repo> 版本鎖定行 → 目標 tag@digest（最後寫）
- [file/F12] b16f: version.toml（<repo> 版本鎖定行，進 git）
- [step/SUB] b16b [v2]: 成功（以上寫入都已落盤）：刪進度檔 metadata [progress]（最後一步）
- [file/F12] b16bf [v2]: .vendor_kit.toml（－[progress]）
- [end_orange/O12] b18: 2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版、解析失敗的檔留舊版；解完再跑直到乾淨
- [decision/D12] b16q [v2]: 有衝突（conflicts 非空）？
- [rule/RULE] b18r [v2]: 多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 > 2 > 0；衝突與有新版兩者皆回 2，訊息全部列出；待合併補完後另有新版 → 印 6-14「已補齊 <repo> 至 vB；另有新版 vX，再跑一次可升」
- [other/TEXT] _sp: 
- [end_ok/G12] b17 [v2]: 0：印摘要 → commit
- [end_red/R12] b16x [v2]: 1：寫入失敗（本段任一步），明列已完成／未完成；進度檔保留
- [other/LEGEND] p7cq_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7cq_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7cq_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7cq_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7cq_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7cq_lg5 [legend]: 白：步驟
- [other/LEGEND] p7cq_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7cq_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7cq_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7cq_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7cq_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p7cq_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7cq_lgx_img [legend]: 紫：image
- [other/LEGEND] p7cq_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7cq_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7cq_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7cq_th: 本頁名詞
- [term/TERM_K] p7cq_tk0: 基準版落後／待合併
- [term/TERM_V] p7cq_tv0: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- [term/TERM_K] p7cq_tk1: resolve／apply／--dry-run
- [term/TERM_V] p7cq_tv1: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- [term/TERM_K] p7cq_tk2: flock／指紋
- [term/TERM_V] p7cq_tv2: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7cq_tk3: gen／mod?
- [term/TERM_V] p7cq_tv3: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- [term/TERM_K] p7cq_tk4: git merge-file --diff3
- [term/TERM_V] p7cq_tv4: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7cq_tk5: CRLF／append 行
- [term/TERM_V] p7cq_tv5: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- [term/TERM_K] p7cq_tk6: GHCR／tag@digest
- [term/TERM_V] p7cq_tv6: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- [term/TERM_K] p7cq_tk7: 6-38
- [term/TERM_V] p7cq_tv7: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## edges
- be23: b15z(來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原…) --(無標籤)--> b15a(推 baseline/<repo>/ 到目標版：逐檔，通過的…)
- be24: b15a(推 baseline/<repo>/ 到目標版：逐檔，通過的…) --寫--> b15f(baseline/<repo>/（目標版範本副本，進 git…)
- be24b: b15a(推 baseline/<repo>/ 到目標版：逐檔，通過的…) --(無標籤)--> b15b(寫 metadata：source = 目標版（= 最後合併…)
- be24bf: b15b(寫 metadata：source = 目標版（= 最後合併…) --寫--> b15bf(baseline/<repo>/.vendor_kit.to…)
- be24c: b15b(寫 metadata：source = 目標版（= 最後合併…) --(無標籤)--> b15c(寫 metadata：conflicts（有衝突標記或解析失…)
- be24cf: b15c(寫 metadata：conflicts（有衝突標記或解析失…) --寫--> b15cf(.vendor_kit.toml（conflicts）)
- be24d: b15c(寫 metadata：conflicts（有衝突標記或解析失…) --(無標籤)--> b15d(寫 metadata：每個 dest 的 state／dec…)
- be24df: b15d(寫 metadata：每個 dest 的 state／dec…) --寫--> b15df(.vendor_kit.toml（[[file]] 各 de…)
- be25: b15d(寫 metadata：每個 dest 的 state／dec…) --(無標籤)--> b15g(重生 gen/tools.just（新版的 just/<ns…)
- be25f: b15g(重生 gen/tools.just（新版的 just/<ns…) --寫--> b15gf(gen/tools.just（不進 git；mod? 行）)
- be25q: b15g(重生 gen/tools.just（新版的 just/<ns…) --(無標籤)--> b16q0(待合併（version.toml 已是目標版 B）？)
- be25g: b16q0(待合併（version.toml 已是目標版 B）？) --否--> b16(否：寫 version.toml <repo> 版本鎖定行 …)
- be27: b16(否：寫 version.toml <repo> 版本鎖定行 …) --寫--> b16f(version.toml（<repo> 版本鎖定行，進 gi…)
- be26: b16(否：寫 version.toml <repo> 版本鎖定行 …) --(無標籤)--> b16b(成功（以上寫入都已落盤）：刪進度檔 metadata [pr…)
- be26f: b16b(成功（以上寫入都已落盤）：刪進度檔 metadata [pr…) --刪--> b16bf(.vendor_kit.toml（－[progress]）)
- be28q: b16b(成功（以上寫入都已落盤）：刪進度檔 metadata [pr…) --(無標籤)--> b16q(有衝突（conflicts 非空）？)
- be29: b16q(有衝突（conflicts 非空）？) --是--> b18(2：印衝突檔名（含解析失敗的檔）；基準版：通過的檔已在目標版…)
- be25y: b16q0(待合併（version.toml 已是目標版 B）？) --是：已是 B，不動--> b16b(成功（以上寫入都已落盤）：刪進度檔 metadata [pr…)
- be26xa: b15a(推 baseline/<repo>/ 到目標版：逐檔，通過的…) --失敗--> b16x(1：寫入失敗（本段任一步），明列已完成／未完成；進度檔保留)
- be26x: b16(否：寫 version.toml <repo> 版本鎖定行 …) --失敗--> b16x(1：寫入失敗（本段任一步），明列已完成／未完成；進度檔保留)
- be28: b16q(有衝突（conflicts 非空）？) --否--> b17(0：印摘要 → commit)

## terms
- 基準版落後／待合併: 最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1 + 6-5（PR 紅，需人處理）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- gen／mod?: gen/tools.just（不進 git）每個 <ns>.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just <ns> …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它（與 cache 同一 apply 內原子替換）
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- CRLF／append 行: CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；唯一命中才問替換；零命中或多處 → 保留只 warn
- GHCR／tag@digest: GHCR = GitHub 的容器倉庫；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log

## xrefs
- uB3: 其他「B（2）」頁
- b15z: 來自「B（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7b -----
# v1p7b  31 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入

nodes 74（不含 v2 小標）／edges 41／terms 8／xrefs 12

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── C. 逐檔判斷狀態機、C′ 衝突重入（§4.3、v2.2 D、v2.15-18）
- [note/NOTE] pend: 已定（v2.3 §1、v2.15-18）：逐檔判斷 = 依 metadata state 分流的狀態機：managed／appended／declined／unmanaged／deleted／新版新增各自路徑；二進位／symlink 改過 → 保留 warn，不進三方合併；append 命中分唯一／零／多處；新版新增但 dest 已有 → 不納管 + 6-11；declined_hash 相同不再問、N 變才問；解析失敗檔基準版不推（「B（2′）」頁）。升引擎見「E. 升引擎」頁；回退見「D. 回退」頁。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: 專案目錄
- [other/BAND] uC [v2]: C. 逐檔判斷狀態機（每個 init.toml [[file]]＋metadata 每個 dest；在「B（2）」頁 apply 內逐檔呼叫）：依 metadata state 分流 → 每檔恰一條路 → 「不動／warn」或「問 6-22」回「B（2）」頁
- [entry/ENTRY] c_in: 來自「B（2）」頁：逐檔迴圈的一個檔（B／D／N 三份已備）
- [file/F12] c_in0: B = baseline/<repo>/<檔>（上次合併的範本）
- [file/F12] c_in1: D = 專案裡的 <檔>（現況，下游使用者可能改過）
- [decision/D12] q1 [v2]: metadata 無此 dest（新版新增）且 dest 已存在？
- [step/SUB] s_un [v2]: 是：不納管、印 6-11（state=unmanaged）
- [file/F12] c_in2 [v2]: N = 目標版範本：暫存 /dist/<repo>/<檔>（不是 cache）
- [decision/D12] q1c [v2]: 否 → 新版新增且 dest 不存在？
- [decision/D12] q2 [v2]: 否 → state = deleted？
- [step/SUB] s_del [v2]: 是：維持刪除、不問、不重建
- [decision/D12] q3a [v2]: 否 → state = unmanaged？
- [step/SUB] s_um [v2]: 是：不動（dry-run／check.sh 印 6-7）
- [decision/D12] q3b [v2]: 否 → state = declined 且 N 的 hash == declined_hash？
- [step/SUB] s_dq [v2]: 是：不再問（印 6-6）
- [decision/D12] q3c [v2]: 否 → state = declined（N 變了）？
- [decision/D12] q4 [v2]: 否 → state = appended 且上次插入的行唯一命中？
- [decision/D12] q4c [v2]: 否 → state = appended（零／多處命中）？
- [step/SUB] s_ap [v2]: 是：保留、warn、印新內容
- [decision/D12] q5 [v2]: 否（managed）→ D 缺（下游使用者刪了）？
- [step/SUB] s_dd [v2]: 是：state=deleted、維持刪除
- [decision/D12] q6 [v2]: 否 → N 缺（新版刪檔）？
- [step/SUB] s_nd [v2]: 是：不刪、只 warn
- [decision/D12] q7 [v2]: 否 → D==N 或 B==N？
- [step/SUB] s_eq [v2]: 是：不動
- [decision/D12] q8 [v2]: 否 → 二進位／symlink 且 D==B（未改）？
- [decision/D12] q8c [v2]: 否 → 二進位／symlink（改過）？
- [step/SUB] s_bk [v2]: 是：保留 + warn（不進三方合併）
- [decision/D12] q9 [v2]: 否（文字檔）→ D==B（你沒改、新版改了）？
- [note/NOTE] c_note: 三者皆異（D≠B、N≠B、D≠N）= 兩邊都改 → 問三方合併。--dry-run 只印會問哪些檔。衝突解完 → 再跑 upgrade 直到乾淨（2 = 需人處理，橙）。dest 撞名規則見「add（1′）」頁。
- [entry/ENTRY] c_ask: 續「B（2）」頁：問 6-22（新檔：要建 X 嗎／append：要替換嗎／二進位：換成新版？／換成新版？／三方合併？）
- [entry/ENTRY] c_skip: 續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）
- [other/BAND] uC2 [v2]: C′ 衝突重入（解完衝突後再跑 upgrade；v2.2 D (0)）—— 偵測在 resolve，清除在 apply（拿鎖、建進度檔後）
- [end_ok/G12] cx0: 解完衝突後再跑 upgrade <repo>
- [decision/D12] cx1 [v2]: conflicts 中的檔仍含我們的標籤，或檔案失蹤？
- [end_orange/O12] cx2 [v2]: 是 → 2：停，先解完標記再重跑（=「B. 手動路徑（1）」頁 (0) 的橙終點）
- [entry/ENTRY] cx3: 續「B. 手動路徑（1）」頁 (1)(2)：apply 拿鎖、建進度檔後清除衝突狀態
- [other/LEGEND] p7b_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7b_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7b_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7b_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7b_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7b_lg5 [legend]: 白：步驟
- [other/LEGEND] p7b_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7b_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7b_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7b_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7b_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7b_lgx_img [legend]: 紫：image
- [other/LEGEND] p7b_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7b_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7b_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7b_th: 本頁名詞
- [term/TERM_K] p7b_tk0: B／D／N
- [term/TERM_V] p7b_tv0: B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過
- [term/TERM_K] p7b_tk1: 逐檔判斷（狀態機）
- [term/TERM_V] p7b_tv1: upgrade apply 對 init.toml 每個 [[file]] 與 metadata 每個 dest，依 metadata state（managed／appended／declined／unmanaged／deleted／metadata 無此 dest = 新版新增）分流，每檔恰走一條路：結果 = 不動／warn（不問）或問 6-22；在 apply 內、拿到 flock、建進度檔後（「B（2）」頁）
- [term/TERM_K] p7b_tk2: flock／指紋
- [term/TERM_V] p7b_tv2: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7b_tk3: git merge-file --diff3
- [term/TERM_V] p7b_tv3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7b_tk4: 二進位檔
- [term/TERM_V] p7b_tv4: 不是文字的檔（symlink 同）；不做行內合併：D==B（未改）→ 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過 → 保留 + warn，不進三方合併；dist/files/ 第一版禁止 symlink
- [term/TERM_K] p7b_tk5: declined／declined_hash／6-6／6-7／6-8
- [term/TERM_V] p7b_tv5: state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256）；N 的 hash == declined_hash → 不再問（dry-run／check.sh 印 6-6「有 N 個範本你拒絕過」）；≠ → 再問；unmanaged → 不動（6-7「<X> 沒納管」提醒）；6-8「<Y> 你拒絕過，<vZ> 有新版」
- [term/TERM_K] p7b_tk6: 6-11（已有同名檔）
- [term/TERM_V] p7b_tv6: 新版新增的 dest 已存在 → 不納管（state=unmanaged）、不問、印「<X> 已存在，未納管；範本在 .vendor_kit/cache/<repo>/files/ 可自行比對」
- [term/TERM_K] p7b_tk7: 6-22（upgrade 逐檔問句）
- [term/TERM_V] p7b_tv7: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問

## edges
- ce_0: c_in(來自「B（2）」頁：逐檔迴圈的一個檔（B／D／N 三份已備）) --(無標籤)--> q1(metadata 無此 dest（新版新增）且 dest 已…)
- ce_1y: q1(metadata 無此 dest（新版新增）且 dest 已…) --是--> s_un(是：不納管、印 6-11（state=unmanaged）)
- ce_1n: q1(metadata 無此 dest（新版新增）且 dest 已…) --否--> q1c(否 → 新版新增且 dest 不存在？)
- ce_1cn: q1c(否 → 新版新增且 dest 不存在？) --否--> q2(否 → state = deleted？)
- ce_2y: q2(否 → state = deleted？) --是--> s_del(是：維持刪除、不問、不重建)
- ce_2n: q2(否 → state = deleted？) --否--> q3a(否 → state = unmanaged？)
- ce_3ay: q3a(否 → state = unmanaged？) --是--> s_um(是：不動（dry-run／check.sh 印 6-7）)
- ce_3an: q3a(否 → state = unmanaged？) --否--> q3b(否 → state = declined 且 N 的 has…)
- ce_3by: q3b(否 → state = declined 且 N 的 has…) --是--> s_dq(是：不再問（印 6-6）)
- ce_3bn: q3b(否 → state = declined 且 N 的 has…) --否--> q3c(否 → state = declined（N 變了）？)
- ce_3cn: q3c(否 → state = declined（N 變了）？) --否--> q4(否 → state = appended 且上次插入的行唯一…)
- ce_4n: q4(否 → state = appended 且上次插入的行唯一…) --否--> q4c(否 → state = appended（零／多處命中）？)
- ce_4cy: q4c(否 → state = appended（零／多處命中）？) --是--> s_ap(是：保留、warn、印新內容)
- ce_4cn: q4c(否 → state = appended（零／多處命中）？) --否--> q5(否（managed）→ D 缺（下游使用者刪了）？)
- ce_5y: q5(否（managed）→ D 缺（下游使用者刪了）？) --是--> s_dd(是：state=deleted、維持刪除)
- ce_5n: q5(否（managed）→ D 缺（下游使用者刪了）？) --否--> q6(否 → N 缺（新版刪檔）？)
- ce_6y: q6(否 → N 缺（新版刪檔）？) --是--> s_nd(是：不刪、只 warn)
- ce_6n: q6(否 → N 缺（新版刪檔）？) --否--> q7(否 → D==N 或 B==N？)
- ce_7y: q7(否 → D==N 或 B==N？) --是--> s_eq(是：不動)
- ce_7n: q7(否 → D==N 或 B==N？) --否--> q8(否 → 二進位／symlink 且 D==B（未改）？)
- ce_8n: q8(否 → 二進位／symlink 且 D==B（未改）？) --否--> q8c(否 → 二進位／symlink（改過）？)
- ce_8cy: q8c(否 → 二進位／symlink（改過）？) --是--> s_bk(是：保留 + warn（不進三方合併）)
- ce_8cn: q8c(否 → 二進位／symlink（改過）？) --否--> q9(否（文字檔）→ D==B（你沒改、新版改了）？)
- ce_9y: q9(否（文字檔）→ D==B（你沒改、新版改了）？) --是--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- ce_s_un: s_un(是：不納管、印 6-11（state=unmanaged）) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_del: s_del(是：維持刪除、不問、不重建) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_um: s_um(是：不動（dry-run／check.sh 印 6-7）) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_dq: s_dq(是：不再問（印 6-6）) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_ap: s_ap(是：保留、warn、印新內容) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_dd: s_dd(是：state=deleted、維持刪除) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_nd: s_nd(是：不刪、只 warn) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_eq: s_eq(是：不動) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_s_bk: s_bk(是：保留 + warn（不進三方合併）) --(無標籤)--> c_skip(續「B（2）」頁：不動／warn → 下一個檔（不記拒絕）)
- ce_q1cy: q1c(否 → 新版新增且 dest 不存在？) --是（要建 X 嗎）--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- ce_q3cy: q3c(否 → state = declined（N 變了）？) --是（再問要建 X 嗎）--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- ce_q4y: q4(否 → state = appended 且上次插入的行唯一…) --是（要替換嗎？）--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- ce_q8y: q8(否 → 二進位／symlink 且 D==B（未改）？) --是（二進位換成新版？）--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- ce_9n: q9(否（文字檔）→ D==B（你沒改、新版改了）？) --否--> c_ask(續「B（2）」頁：問 6-22（新檔：要建 X 嗎／appe…)
- cx_e0: cx0(解完衝突後再跑 upgrade <repo>) --(無標籤)--> cx1(conflicts 中的檔仍含我們的標籤，或檔案失蹤？)
- cx_e1: cx1(conflicts 中的檔仍含我們的標籤，或檔案失蹤？) --是--> cx2(是 → 2：停，先解完標記再重跑（=「B. 手動路徑（1）」…)
- cx_e2: cx1(conflicts 中的檔仍含我們的標籤，或檔案失蹤？) --否--> cx3(續「B. 手動路徑（1）」頁 (1)(2)：apply 拿鎖…)

## terms
- B／D／N: B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過
- 逐檔判斷（狀態機）: upgrade apply 對 init.toml 每個 [[file]] 與 metadata 每個 dest，依 metadata state（managed／appended／declined／unmanaged／deleted／metadata 無此 dest = 新版新增）分流，每檔恰走一條路：結果 = 不動／warn（不問）或問 6-22；在 apply 內、拿到 flock、建進度檔後（「B（2）」頁）
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- 二進位檔: 不是文字的檔（symlink 同）；不做行內合併：D==B（未改）→ 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過 → 保留 + warn，不進三方合併；dist/files/ 第一版禁止 symlink
- declined／declined_hash／6-6／6-7／6-8: state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256）；N 的 hash == declined_hash → 不再問（dry-run／check.sh 印 6-6「有 N 個範本你拒絕過」）；≠ → 再問；unmanaged → 不動（6-7「<X> 沒納管」提醒）；6-8「<Y> 你拒絕過，<vZ> 有新版」
- 6-11（已有同名檔）: 新版新增的 dest 已存在 → 不納管（state=unmanaged）、不問、印「<X> 已存在，未納管；範本在 .vendor_kit/cache/<repo>/files/ 可自行比對」
- 6-22（upgrade 逐檔問句）: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問

## xrefs
- pend: 其他「B（2′）」頁
- pend: 見「E. 升引擎」頁
- pend: 見「D. 回退」頁
- uC: 其他「B（2）」頁
- uC: 回「B（2）」頁
- c_in: 來自「B（2）」頁
- c_note: 見「add（1′）」頁
- c_ask: 續「B（2）」頁
- c_skip: 續「B（2）」頁
- cx2: 其他「B. 手動路徑（1）」頁
- cx3: 續「B. 手動路徑（1）」頁
- p7b_tv1: 其他「B（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bd -----
# v1p7bd  32 流程 v2：upgrade ── D. 回退

nodes 60（不含 v2 小標）／edges 19／terms 7／xrefs 5

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── D. 回退 = git revert 該升級 commit（§5、v2.5 §1／§9）
- [note/NOTE] pend: 已定（v2.3 §1、v2.15-18）：逐檔判斷 = 依 metadata state 分流的狀態機：managed／appended／declined／unmanaged／deleted／新版新增各自路徑；二進位／symlink 改過 → 保留 warn，不進三方合併；append 命中分唯一／零／多處；新版新增但 dest 已有 → 不納管 + 6-11；declined_hash 相同不再問、N 變才問；解析失敗檔基準版不推（「B（2′）」頁）。升引擎見「E. 升引擎」頁；回退見「D. 回退」頁。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uD [v2]: D. 回退 ＝ git revert 該升級 commit（version.toml + 初始檔 + 基準版同一 commit）；下次 just 的 sync（resolve → docker → apply）把 cache/ 換回舊版、重生 gen/tools.just；初始檔與基準版由 git revert 還原
- [end_ok/G12] d0: git revert 該升級 commit
- [step/W12] d1a [v2]: 下次 just（已寫 launcher_started）：docker run 引擎 resolve sync
- [file/FGRP] d3b: 由 git revert 還原（不是 sync 寫）
- [file/F12] d3b_0: 初始檔
- [file/F12] d3b_1: baseline/<repo>/
- [file/F12] d3b_2: version.toml
- [step/SUB] d2: sync resolve：gen/<repo>.stamp 第一行 ≠ version.toml 鎖定 digest → 待辦「取件舊版」＋「重生 gen/tools.just」
- [decision/D12] d1b [v2]: inspect：舊版本機有？
- [step/W12] d1p [v2]: 無：docker pull
- [other/IMG] d1g: <repo>-dist@digest⏎（version.toml 還原後的舊版）
- [step/W12] d1c: extract：docker create <img> /x → cp c:/dist/. <tmp>/<repo>/ → rm
- [end_red/R12] d1px [v2]: 1 + 6-24／6-31：pull 失敗（原文＋分類）／逾時（--timeout）
- [end_red/R12] d1cx [v2]: 1：extract 失敗（create／cp／rm 或暫存目錄）
- [step/W12] d1f: docker run … -v <tmp>:/dist:ro 引擎 apply sync
- [step/SUB] d2c: 取件舊版：/dist/<repo> 複製到暫存目錄
- [step/SUB] d2c2: 暫存 → cache/<repo>/（原子替換）
- [file/F12] d3: cache/<repo>/（舊版；sync 寫）
- [step/SUB] d2c3: 寫印記 gen/<repo>.stamp（舊版 index digest）
- [file/F12] d3s: gen/<repo>.stamp（舊版；sync 寫）
- [step/SUB] d2c4 [v2]: 重生 gen/tools.just（舊版 just/；與 cache 同一 apply 內原子替換）
- [file/F12] d3t: gen/tools.just（不進 git）
- [end_ok/G12] d8 [v2]: 0：接著跑原本的 recipe（cache 已是舊版）
- [other/LEGEND] p7bd_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bd_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bd_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bd_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bd_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bd_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bd_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bd_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bd_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bd_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7bd_lgx_img [legend]: 紫：image
- [other/LEGEND] p7bd_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7bd_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7bd_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7bd_th: 本頁名詞
- [term/TERM_K] p7bd_tk0: B／D／N
- [term/TERM_V] p7bd_tv0: B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過
- [term/TERM_K] p7bd_tk1: flock／指紋
- [term/TERM_V] p7bd_tv1: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7bd_tk2: git merge-file --diff3
- [term/TERM_V] p7bd_tv2: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- [term/TERM_K] p7bd_tk3: 回退／git revert
- [term/TERM_V] p7bd_tv3: git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、基準版同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 把 cache/<repo>/ 換回舊版、重生 tools.just（見「D. 回退」頁）
- [term/TERM_K] p7bd_tk4: 6-38
- [term/TERM_V] p7bd_tv4: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bd_tk5: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7bd_tv5: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止
- [term/TERM_K] p7bd_tk6: Renovate
- [term/TERM_V] p7bd_tv6: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁

## edges
- d1b_n: d1b(inspect：舊版本機有？) --無--> d1p(無：docker pull)
- d1g_p: d1g(<repo>-dist@digest （version.to…) --拉 /dist--> d1p(無：docker pull)
- d1p_x: d1p(無：docker pull) --(無標籤)--> d1c(extract：docker create <img> /x…)
- de1: d0(git revert 該升級 commit) --(無標籤)--> d1a(下次 just（已寫 launcher_started）：d…)
- de1e: d1a(下次 just（已寫 launcher_started）：d…) --(無標籤)--> d2(sync resolve：gen/<repo>.stamp …)
- de2b: d2(sync resolve：gen/<repo>.stamp …) --(無標籤)--> d1b(inspect：舊版本機有？)
- de2px: d1p(無：docker pull) --失敗--> d1px(1 + 6-24／6-31：pull 失敗（原文＋分類）／逾…)
- de2cx: d1c(extract：docker create <img> /x…) --失敗--> d1cx(1：extract 失敗（create／cp／rm 或暫存目…)
- de2f: d1c(extract：docker create <img> /x…) --(無標籤)--> d1f(docker run … -v <tmp>:/dist:ro…)
- de2h: d1f(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> d2c(取件舊版：/dist/<repo> 複製到暫存目錄)
- de2i: d2c(取件舊版：/dist/<repo> 複製到暫存目錄) --(無標籤)--> d2c2(暫存 → cache/<repo>/（原子替換）)
- de3: d2c2(暫存 → cache/<repo>/（原子替換）) --寫--> d3(cache/<repo>/（舊版；sync 寫）)
- de2j: d2c2(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> d2c3(寫印記 gen/<repo>.stamp（舊版 index …)
- de3s: d2c3(寫印記 gen/<repo>.stamp（舊版 index …) --寫--> d3s(gen/<repo>.stamp（舊版；sync 寫）)
- de2k: d2c3(寫印記 gen/<repo>.stamp（舊版 index …) --(無標籤)--> d2c4(重生 gen/tools.just（舊版 just/；與 c…)
- de3t: d2c4(重生 gen/tools.just（舊版 just/；與 c…) --寫--> d3t(gen/tools.just（不進 git）)
- de4: d0(git revert 該升級 commit) --(無標籤)--> d3b(由 git revert 還原（不是 sync 寫）)
- de5: d2c4(重生 gen/tools.just（舊版 just/；與 c…) --(無標籤)--> d8(0：接著跑原本的 recipe（cache 已是舊版）)
- de2y: d1b(inspect：舊版本機有？) --有--> d1c(extract：docker create <img> /x…)

## terms
- B／D／N: B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出
- 回退／git revert: git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、基準版同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 把 cache/<repo>/ 換回舊版、重生 tools.just（見「D. 回退」頁）
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止
- Renovate: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁

## xrefs
- pend: 其他「B（2′）」頁
- pend: 見「E. 升引擎」頁
- pend: 見「D. 回退」頁
- p7bd_tv3: 見「D. 回退」頁
- p7bd_tv6: 見「A. Renovate 路徑」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bc -----
# v1p7bc  33 流程 v2：upgrade ── E. 升引擎 (a)(b)

nodes 82（不含 v2 小標）／edges 32／terms 13／xrefs 5

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── E. vendor_kit 升引擎 (a)(b)（v2.2 A／B、v2.3 §2、v2.5 §7、v2.6 §5）
- [note/NOTE] pend: 已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11、v2.15-7）：(a) 不帶 repo：resolve 先完整預檢、判斷「引擎有新版？」，否 → 只升工具；是 → 啟動器先 pull 新引擎（覆寫時驗 image ID）→ 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 進度檔）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎跑 upgrade vendor_kit；(c) 單段：先恢復既有進度檔 → 目標判定（@<tag>／CI 模式／查 registry 三條分開）→ 目標 ≠ 現 ref → 建進度檔 → 啟動器 pull 目標引擎（失敗 → 6-24／6-31，第一行未改）→ 新引擎改第一行、重產 → 1 + 6-2。
- [header/HDR] hdr0: 下游使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] uE [v2]: E. 升引擎：(a) upgrade 不帶 repo：完整預檢 → 引擎有新版 → 啟動器先 pull 新引擎 → 舊引擎 apply 建 .tmp.upgrade 進度檔、改第一行 → 啟動器接手新引擎（「E(c)（1）」頁）；(b) 別人 pull 後只回 1 提示（sync 頁）；(c) 見「E(c)（1）」頁
- [end_ok/G12] s0 [v2]: (a) upgrade 不帶 repo（含 vendor_kit 自身）
- [step/W12] s0l [v2]: 建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38，零寫入）
- [end_red/R12] s0x [v2]: 1 + 6-38：執行紀錄建不了／寫不進（零寫入）
- [step/W12] s1 [v2]: docker run 舊引擎 resolve upgrade（全部）
- [step/SUB] s2a [v2]: resolve：完整預檢每個工具（dev 中？新版 <ns>／dest 全域撞名？registry 憑證？需詢問項目）
- [end_orange/O12] s2dx [v2]: 1：預檢不過（請先 undev／撞名／6-3 無憑證…），整體不動、原因全列
- [decision/D12] s2dq [v2]: 任一工具預檢不過？
- [decision/D12] s2q [v2]: 否 → 引擎有新版？
- [entry/ENTRY] s2n: 續「B. 手動路徑（1）」頁：否 → 只升工具，每個工具依序走 B（1）～（2′）（Q27 彙總）
- [decision/D12] s2ln [v2]: 是 → inspect 新引擎：本機有？
- [step/W12] s2lp [v2]: 無：docker pull 新引擎
- [other/IMG] s2gi: vendor_kit:vY⏎（新引擎）
- [decision/D12] s2lo [v2]: 本機覆寫中（vendor_kit=）？
- [end_red/R12] s2lx [v2]: 1 + 6-24／6-31：新引擎拉不到／逾時（第一行未改）
- [end_red/R12] s2lvx [v2]: 1：本機覆寫的 image ID 不符（同 tag 重 build；第一行未改）
- [decision/D12] s2lv [v2]: 是 → docker image inspect .Id ≠ 記的 image ID？
- [step/W12] s2r0 [v2]: 否：docker run 舊引擎 apply upgrade
- [step/SUB] s2b [v2]: apply（舊引擎）：flock 專案目錄
- [end_orange/O12] s2cx [v2]: 1 + 6-12：指紋不同「請重跑」
- [decision/D12] s2c [v2]: 重驗指紋：相同？
- [end_orange/O12] s2c2x [v2]: 1：原 argv 與計畫不一致，請重跑
- [decision/D12] s2c2 [v2]: 原 argv 與計畫一致？
- [step/SUB] s2d [v2]: 是 → 建進度檔 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前）
- [file/F12] s2df [v2]: ＋.vendor_kit/.tmp.upgrade.<id>.toml（進度檔，不進 git；新引擎重產薄殼完成後才刪）
- [step/SUB] s2e [v2]: 只改 version.toml 的 vendor_kit 版本鎖定行 → 新引擎 ref（其餘工具等重跑原指令；進度檔留給新引擎）
- [file/F12] s2f: version.toml 的 vendor_kit 版本鎖定行 = 新引擎 ref
- [step/W12] s2h [v2]: apply 後再 grep version.toml 的 vendor_kit 版本鎖定行（本機覆寫 vendor_kit= 優先；不從 stdout 讀）
- [end_red/R12] s2hx [v2]: 1：apply 未改第一行（印 apply 的錯誤）
- [decision/D12] s2h2 [v2]: 第一行變了且 == 計畫的 engine？
- [step/W12] s2r [v2]: 是：docker run 新引擎 upgrade vendor_kit（同一 TRACEPARENT、同一執行紀錄）
- [entry/ENTRY] s4: 續「E(c)（1）」頁「docker run 該引擎」格（同一次指令內；接手 §3.4，結束碼原樣傳出）
- [note/NOTE] sb: (b) 別人 pull 後（第一行已變）打任何 vendor_kit 動詞或帶 _sync 的工具 recipe：走「sync（1）」頁 gen/.stamp 比對 → 1 + 6-1「請 upgrade vendor_kit」→ 打 (c)
- [other/LEGEND] p7bc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bc_lg4 [legend]: 橙：需人處理（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bc_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bc_lgx_entry [legend]: 白虛線橢圓：跨頁出入口
- [other/LEGEND] p7bc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bc_lgx_sub [legend]: 藍：引擎（容器內）做的
- [other/LEGEND] p7bc_lgx_img [legend]: 紫：image
- [other/LEGEND] p7bc_lgx_hdr [legend]: 灰底：泳道／表頭
- [other/LEGEND] p7bc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同
- [other/TEXT] p7bc_lgi: 圖例約定（v2.15-2）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_completed|failed（結束碼、耗時）；每個「docker run 引擎」格隱含 —— 容器開始寫 engine_started、結束寫 engine_completed|failed（同一執行紀錄）。白 = 啟動器（主機）做的。
- [other/TEXT] p7bc_th: 本頁名詞
- [term/TERM_K] p7bc_tk0: 升引擎 (a)(b)(c)
- [term/TERM_V] p7bc_tv0: (a) 不帶 repo：resolve 先完整預檢、判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 建 .tmp.upgrade 進度檔、只改第一行 → 啟動器 grep 第一行變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示（sync 頁）；(c) upgrade vendor_kit[@<tag>]：單段、無指紋重驗；先恢復既有 .tmp.upgrade；目標 ≠ 現 ref → 建進度檔 → 啟動器 pull 目標引擎 → 新引擎改第一行、重產 → 1 + 6-2；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- [term/TERM_K] p7bc_tk1: resolve／apply 兩段
- [term/TERM_V] p7bc_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- [term/TERM_K] p7bc_tk2: 6-2b
- [term/TERM_V] p7bc_tv2: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度檔保留）
- [term/TERM_K] p7bc_tk3: 升引擎進度檔
- [term/TERM_V] p7bc_tv3: .tmp.upgrade.<id>.toml：改第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；啟動器 grep 其目標 ref 決定拉哪個引擎；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- [term/TERM_K] p7bc_tk4: gen/.stamp
- [term/TERM_V] p7bc_tv4: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p7bc_tk5: docker image inspect（引擎）
- [term/TERM_V] p7bc_tv5: 啟動器每次先 docker image inspect：本機有就不 pull（本機覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never；引擎 image LABEL 帶介面版／檔案版，供降版判定
- [term/TERM_K] p7bc_tk6: flock／指紋
- [term/TERM_V] p7bc_tv6: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- [term/TERM_K] p7bc_tk7: 多工具彙總（upgrade）
- [term/TERM_V] p7bc_tv7: 不帶 repo 的 upgrade 先對全部工具完整預檢（撞名、憑證、需詢問項目、dev 中）；任一不過整體不動；做得完的做完，最後回最需要處理的碼：1 > 2 > 0，訊息全列
- [term/TERM_K] p7bc_tk8: resolve 非 0
- [term/TERM_V] p7bc_tv8: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- [term/TERM_K] p7bc_tk9: 原 argv 與計畫一致
- [term/TERM_V] p7bc_tv9: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- [term/TERM_K] p7bc_tk10: 6-12（指紋不同）
- [term/TERM_V] p7bc_tv10: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- [term/TERM_K] p7bc_tk11: 6-38
- [term/TERM_V] p7bc_tv11: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bc_tk12: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7bc_tv12: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## edges
- s2ln_n: s2ln(是 → inspect 新引擎：本機有？) --無--> s2lp(無：docker pull 新引擎)
- s2gi_p: s2gi(vendor_kit:vY （新引擎）) --拉--> s2lp(無：docker pull 新引擎)
- s2lp_x: s2lp(無：docker pull 新引擎) --(無標籤)--> s2lo(本機覆寫中（vendor_kit=）？)
- se1: s0((a) upgrade 不帶 repo（含 vendor_k…) --(無標籤)--> s0l(建執行紀錄、寫 launcher_started（失敗 → …)
- se1x: s0l(建執行紀錄、寫 launcher_started（失敗 → …) --失敗--> s0x(1 + 6-38：執行紀錄建不了／寫不進（零寫入）)
- se1l: s0l(建執行紀錄、寫 launcher_started（失敗 → …) --(無標籤)--> s1(docker run 舊引擎 resolve upgrade…)
- se2: s1(docker run 舊引擎 resolve upgrade…) --(無標籤)--> s2a(resolve：完整預檢每個工具（dev 中？新版 <ns>…)
- se2dq: s2a(resolve：完整預檢每個工具（dev 中？新版 <ns>…) --(無標籤)--> s2dq(任一工具預檢不過？)
- se2dx: s2dq(任一工具預檢不過？) --是--> s2dx(1：預檢不過（請先 undev／撞名／6-3 無憑證…），整…)
- se2q: s2dq(任一工具預檢不過？) --否--> s2q(否 → 引擎有新版？)
- se2n: s2q(否 → 引擎有新版？) --否--> s2n(續「B. 手動路徑（1）」頁：否 → 只升工具，每個工具依序…)
- se6px: s2lp(無：docker pull 新引擎) --失敗--> s2lx(1 + 6-24／6-31：新引擎拉不到／逾時（第一行未改）)
- se6lv: s2lo(本機覆寫中（vendor_kit=）？) --是--> s2lv(是 → docker image inspect .Id ≠…)
- se6vx: s2lv(是 → docker image inspect .Id ≠…) --是--> s2lvx(1：本機覆寫的 image ID 不符（同 tag 重 bu…)
- se6vr: s2lv(是 → docker image inspect .Id ≠…) --否--> s2r0(否：docker run 舊引擎 apply upgrade)
- se3b0: s2r0(否：docker run 舊引擎 apply upgrade) --(無標籤)--> s2b(apply（舊引擎）：flock 專案目錄)
- se3c: s2b(apply（舊引擎）：flock 專案目錄) --(無標籤)--> s2c(重驗指紋：相同？)
- se3cx: s2c(重驗指紋：相同？) --否--> s2cx(1 + 6-12：指紋不同「請重跑」)
- se3c2: s2c(重驗指紋：相同？) --是--> s2c2(原 argv 與計畫一致？)
- se3c2x: s2c2(原 argv 與計畫一致？) --否--> s2c2x(1：原 argv 與計畫不一致，請重跑)
- se3d: s2c2(原 argv 與計畫一致？) --是--> s2d(是 → 建進度檔 .tmp.upgrade.<id>.tom…)
- se3df: s2d(是 → 建進度檔 .tmp.upgrade.<id>.tom…) --寫--> s2df(＋.vendor_kit/.tmp.upgrade.<id>…)
- se3e: s2d(是 → 建進度檔 .tmp.upgrade.<id>.tom…) --(無標籤)--> s2e(只改 version.toml 的 vendor_kit 版…)
- se4: s2e(只改 version.toml 的 vendor_kit 版…) --寫--> s2f(version.toml 的 vendor_kit 版本鎖定…)
- se5: s2e(只改 version.toml 的 vendor_kit 版…) --(無標籤)--> s2h(apply 後再 grep version.toml 的 v…)
- se5h: s2h(apply 後再 grep version.toml 的 v…) --(無標籤)--> s2h2(第一行變了且 == 計畫的 engine？)
- se5x: s2h2(第一行變了且 == 計畫的 engine？) --否--> s2hx(1：apply 未改第一行（印 apply 的錯誤）)
- se5l: s2h2(第一行變了且 == 計畫的 engine？) --是--> s2r(是：docker run 新引擎 upgrade vendo…)
- se7: s2r(是：docker run 新引擎 upgrade vendo…) --(無標籤)--> s4(續「E(c)（1）」頁「docker run 該引擎」格（同…)
- se6y: s2ln(是 → inspect 新引擎：本機有？) --有--> s2lo(本機覆寫中（vendor_kit=）？)
- se3: s2q(否 → 引擎有新版？) --是--> s2ln(是 → inspect 新引擎：本機有？)
- se6lo: s2lo(本機覆寫中（vendor_kit=）？) --否--> s2r0(否：docker run 舊引擎 apply upgrade)

## terms
- 升引擎 (a)(b)(c): (a) 不帶 repo：resolve 先完整預檢、判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 建 .tmp.upgrade 進度檔、只改第一行 → 啟動器 grep 第一行變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示（sync 頁）；(c) upgrade vendor_kit[@<tag>]：單段、無指紋重驗；先恢復既有 .tmp.upgrade；目標 ≠ 現 ref → 建進度檔 → 啟動器 pull 目標引擎 → 新引擎改第一行、重產 → 1 + 6-2；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- resolve／apply 兩段: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④
- 6-2b: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度檔保留）
- 升引擎進度檔: .tmp.upgrade.<id>.toml：改第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；啟動器 grep 其目標 ref 決定拉哪個引擎；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- docker image inspect（引擎）: 啟動器每次先 docker image inspect：本機有就不 pull（本機覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never；引擎 image LABEL 帶介面版／檔案版，供降版判定
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）
- 多工具彙總（upgrade）: 不帶 repo 的 upgrade 先對全部工具完整預檢（撞名、憑證、需詢問項目、dev 中）；任一不過整體不動；做得完的做完，最後回最需要處理的碼：1 > 2 > 0，訊息全列
- resolve 非 0: resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）
- 原 argv 與計畫一致: apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）
- 6-12（指紋不同）: apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1
- 6-38: 執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止

## xrefs
- uE: 其他「E(c)（1）」頁
- uE: 見「E(c)（1）」頁
- s2n: 續「B. 手動路徑（1）」頁
- s4: 續「E(c)（1）」頁
- sb: 其他「sync（1）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


=== 附件 R：第十二版 codex 對本組頁的審查條目 ===
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
# r12 codex 審查 — 第 3 組（v1p7bd v1p7bc v1p7bcc v1p7bcx v1p7bccc v1p8 v1p8ccc v1p8c v1p8cc v1p8b v1p8bccc v1p8bc）

來源：`r12_codex/out3.md`（codex exec，gpt-5.6-sol，reasoning low，tokens used 171,705；附件 S 為完整 spec_0_9.md，未縮減）。以下逐條整理 codex 原文，不加審查者意見。

## 跨頁共通問題（codex 標為本組全部 12 頁）

| 頁 id | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 全部 12 頁 | `lp → lx → 多個終點` | B | 所有成功、失敗與需人處理分支先匯入同一個 `launcher_exit`，再由它無條件分岔至所有終點，讀圖上無法判斷哪條來源對應哪個結束狀態；應在匯流前保留結果碼，或各結果分別接自己的結束序列 | 必修 |
| 全部 12 頁 | 各 `docker run`／`engine_start` 區段 | A | 規格要求每個引擎子命令結束前 append `engine_exit`，圖面普遍只畫 `engine_start`，未畫 `engine_exit`，跨頁接手時無法確認同一紀錄檔內每個容器都有成對事件 | 必修 |
| 全部 12 頁 | 名詞表 | F | 每頁重複十餘條完整契約，許多名詞未在該頁流程使用，反而使真正分支難以閱讀；名詞表宜只保留該頁實際出現且一般人不懂的詞 | 選修 |

## v1p7bd

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `uD`、`d2c2`、`d2c3` | A | 頁首及流程宣稱 sync「只把 cache 換回舊版」，但規格要求 sync 在需要時也重生 `gen/tools.just`，本頁完全缺少該判斷與寫入 | 必修 |
| `d2c`「materialize 舊版：/dist/<repo> 複製到暫存目錄」 | C | 此格同時描述取件與「初始檔、baseline 不碰」的範圍規則，應把動作縮為「從 `/dist/<repo>` 取件」，限制另作便條 | 選修 |
| `d1px` | B | pull 失敗與逾時共用一個終點，但沒有從失敗分支保存 6-24 或 6-31 的判定，配合共通的 `launcher_exit` 扇出後語意不成立 | 必修 |

## v1p7bc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `s2a`、`s2dq` | A | 「完整預檢」後只畫「含 dev 中工具？」一項；規格要求不帶 repo 的 upgrade 在任何寫入前預檢全部工具（撞名、憑證、需詢問項目），任一不過整體不動 | 必修 |
| `s2n` | B | 「每個工具走 B（1）頁」只是文字，沒有跨頁出口圖形與實線，屬懸空流程；應改為白虛線跨頁出口並標出回傳彙總位置 | 必修 |
| `s2r → s4` | B | 接到下一頁的文字不是白虛線跨頁入口／出口，且本頁沒有交代新引擎子命令的 `engine_start` 由下一頁接續 | 必修 |
| `s2lv` | A | 把「是否為 local 覆寫」與「image ID 是否不符」合成一個判斷，正常非覆寫路徑也只能沿「否」通過，容易誤讀；應先分 local 覆寫，再只對覆寫檢查 ID | 選修 |

## v1p7bcc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `s12a`、`s12b` | A | `upgrade vendor_kit` 是單段動詞，沒有先前 resolve 所產生的指紋可供「重驗」；本頁卻畫成拿鎖後重驗指紋，混入兩段動詞模型 | 必修 |
| `s12a0` 之後 | A | 缺少偵測與恢復既有 `.tmp.upgrade.<id>.toml` 的分支；規格要求直接執行 `upgrade vendor_kit` 時若有未完成自身升級，本次立即依日誌恢復 | 必修 |
| `s12tt → s12v → s12jz` | A | 指定新 `@<tag>` 或 registry 找到新目標後，沒有 inspect／pull「目標引擎」的步驟便直接去改第一行；目前頁首 inspect／pull 的是現行引擎，不是新目標 | 必修 |
| `s11x` | D | 「image ID 不符」是無法執行的失敗可用紅色，但「拉不到」應明列 6-24／6-31；目前合併文字遺失逾時及分類訊息 | 必修 |
| `s12d`「@<tag> 舊版且無法無損讀？」 | C | 同格同時判斷「是否降版」與「相容性是否通過」，應拆成兩個判斷，否則「指定相同版／新版」與「舊版但可讀」共用同一路徑 | 選修 |

## v1p7bcx

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `s12hr` | A | 改完第一行後直接 `docker run 新引擎`，缺少對新 ref 的 `docker image inspect`、必要時 pull，以及 pull／ID 不符時的 6-2b 分支 | 必修 |
| `s12hq --否→ s12hx` | A | 判斷是「第一行變了且等於計畫值」，「否」可能包括「沒變」或「變成非計畫值」；後者屬第二次改變並應走 6-2b，本頁卻一律說「第一行未變、不是 6-2b」 | 必修 |
| `s12hz` | B | 跨頁出口以普通文字表示，沒有白虛線橢圓，也沒有明確連到 `v1p7bcc` 的元件 `s11r` | 必修 |
| `s12w` | C | 同格同時包含修改 version.toml、原子替換與寫 `engine_exit` 三件事；至少應把 `engine_exit` 拆出 | 必修 |

## v1p7bccc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `s13gn` | A | config.toml 不存在時直接建立，少了規格要求的詢問／`-y` 分支 | 必修 |
| `s13gy`、`s13gw` | A | 三方合併可能衝突或解析失敗並回 2，但圖上沒有結束碼 2、衝突標記、基準版是否推進等分支，全部直接流向寫檔 | 必修 |
| `s13gb` | A | 只推進 `baseline/vendor_kit/config.toml`，漏畫同步更新 `baseline/.vendor_kit.toml` 中 config.toml 的 metadata | 必修 |
| `s13 → s13gq` | A | 薄殼五檔已先原子替換，之後 config 合併若失敗便留下部分重產；圖上沒有用進度檔恢復或暫存整批提交來說明跨檔失敗狀態 | 必修 |
| `s14` | F | 無新版但薄殼需修復時也會到此格，文案卻固定寫「已升級引擎 vX → vY」，一般人會誤以為版本真的改變；應區分「換引擎後重產」與「同引擎修復重產」 | 必修 |
| `s13q` | C | 「任一步失敗」與「第一行是否已改／又變」揉成一格，且無法表達第二次第一行又變的獨立情況 | 選修 |

## v1p8

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `d6a` 之前 | A | dev 是可寫動詞，規格要求第一個寫入前建立 `.tmp.dev.<id>.toml`，記覆寫行、symlink 目標與印記；本頁完全缺少建立、成功刪除及失敗恢復 | 必修 |
| `d6` | A | 圖中寫成頂層 `<repo> = "path:<dir>"`；規格要求工具覆寫位於 `[tools].<repo>` | 必修 |
| `d1q`、`d2c` | F | 前者只查 init.toml 是否存在，後者再查「dist 合法」，但未說合法包含哪些最低條件，兩個判斷看似重複；應把前者標成主機掛載前存在性檢查，後者標成引擎完整驗證 | 選修 |
| `d3c` | D | 「dist／init.toml 不合法」屬驗證失敗，依顏色規則應為紅色，不是橙色需人處理 | 必修 |

## v1p8ccc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `v2a` 之後 | A | 與 v1p8 相同，缺少 `.tmp.dev.<id>.toml` 的建立、內容、成功刪除與恢復路徑 | 必修 |
| `v1i` 至 `v1` | A | 缺少依目標 image LABEL 檢查介面版／檔案版；若舊 image 會要求重產 tracked 薄殼，規格要求改檔前回 3，本頁沒有此分支 | 必修 |
| `v2b`、`v2c` | C | 兩格分別寫同一個 TOML 的兩行尚可，但對外實際是一個原子更新；目前兩條分開的檔案寫入線會使人以為第一行可以先落盤。應以一個原子替換動作寫兩欄 | 必修 |
| `v5`「下次打任何 just」 | F | 不是每個任意 just recipe 都必然進 vendor_kit 啟動器；應寫成「下次執行 vendor_kit 動詞或有 `_sync` 前置的工具 recipe」 | 必修 |

## v1p8c

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `u6l` | A | 進度檔文字沒有說明須記錄「要撤的覆寫行與 image ID」，與 undev 的恢復契約不足 | 必修 |
| `u6g` | B | 只有「刪進度日誌」動作，沒有對應檔案節點及刪除線，和同頁其他檔案變更表示法不一致 | 選修 |
| `u6c → u6d` | A | 先撤 version.local.toml、再拆 symlink、最後重建 cache，任一步失敗時要保留可恢復狀態；圖雖有總括失敗出口，但未畫從 `u6c`、`u6d`、`u6e2` 等各步到失敗處，只有 `u6f` 有「任一步」線，容易被讀成前面寫失敗仍繼續 | 必修 |
| `u6d`「是／已刪：拆掉 cache/<repo>/ 的 symlink」 | F | 「是／已刪」指的是前一判斷兩條路，文字脫離箭線後難懂；改成單純「拆掉 cache symlink」 | 選修 |

## v1p8cc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `w2l` | A | 進度檔未標明必須記錄要撤的 `vendor_kit`、`vendor_kit_image_id` 與 image ID，恢復資訊表達不足 | 必修 |
| `w4`「下次打任何 just」 | F | 同 v1p8ccc，並非任何 just 都會進 sync；應限縮為 vendor_kit 動詞或有 `_sync` 的工具 recipe | 必修 |
| `w5b → w5p → w5c` | A | 這整段與本頁主題「undev vendor_kit」不是同一次動詞，而是下一次 sync 的流程；依審查標準應移到獨立 sync 頁，本頁只保留跨頁出口 | 必修 |
| `w5p_x` | B | pull 成功的線未標「成功」，而 pull 失敗另繞到底部；在縮圖上兩條長線來源難辨，應直接從 pull 畫成功／失敗兩支 | 選修 |

## v1p8b

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `m6d2` | A | 宣稱 vk-resolve/1 stdout 含「計畫」，但規格列出的 kind 沒有刪除清單或詢問清單；啟動器只需保存合法協定並把原 argv 交 apply，不能傳未定義記錄 | 必修 |
| `m6c` | A | resolve 產生詢問清單本身可以是引擎內部計算，但本頁畫成送到啟動器；詢問必須由 apply 引擎執行，不能讓啟動器解讀未定義的問句資料 | 必修 |
| `m7 → m7z` | B | 通往下一頁的「否」沒有畫成跨頁出口，且 edge 沒有「否」標籤 | 必修 |
| `m0` | C | 起點同格放命令與兩個可選參數，尚可作語法，但括號寫法容易誤認兩者必須成組；建議改成規格形式 `remove <repo> [-y] [--dry-run]` | 選修 |

## v1p8bccc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `m9q --否→ m10a` | A | 使用者明確拒絕移除 append 行後仍刪 metadata／baseline，將失去這些行的所有權紀錄；規格說明確回答否要在 metadata 記錄，不能隨即刪掉承載紀錄的 metadata 而不交代保留狀態 | 必修 |
| `m9q` | A | 缺少無 tty／EOF／Ctrl-C 分支；規格要求無 tty 或 EOF 且無 `-y` 回 1、不套用，Ctrl-C 亦中止且不記 declined | 必修 |
| `m10d` | A | `gen/tools.just` 必須最後寫並與 cache 同一 apply 原子替換；本頁在它之後仍刪 version.toml，且沒有表達 tools.just 的原子替換要求。若「最後」指所有產生檔的提交點，現順序不符 | 必修 |
| `m10e --失敗（任一步）→ lp` | B | 「任一步」的線卻只從最後刪 version.toml 的元件出發，視覺上不能涵蓋前面的 append、baseline、cache、stamp、tools.just 寫入失敗 | 必修 |

## v1p8bc

| 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|
| `x2e2` | A | 同 v1p8b，vk-resolve/1 沒有「執行計畫／詢問清單／保護清單」的協定 kind，不能宣稱這些資料透過 stdout 傳給啟動器 | 必修 |
| `x2`、`x2x` | A | 預檢失敗例只列 dev 與未完成接入，漏掉多工具寫入動詞要求的完整預檢項目及「任一不過整體不動、原因全列」 | 必修 |
| `x2b` | C | 一格同時列薄殼、version.toml、config.toml、gen、cache、baseline 全部 hash 計算，屬多個最小單元；至少應分成「計算 tracked 自產檔」與「計算本機產物」，或收成一個抽象模組動作 | 選修 |
| `x3 → x4z` | B | 跨頁出口未使用白虛線橢圓，且 edge 未標「否」，與同頁 dry-run 的「是」支線不對稱 | 必修 |
| `x2r` | F | 規則框位於流程右側但沒有任何連線指明它約束 `x2c` 或下一頁的逐工具 remove；一般讀者會把它當孤立註解 | 選修 |

## 沒問題的頁

無。codex 對本組 12 頁每頁都列出至少一條。

## 未附完整頁面（codex 附註）

附件只有 `uninstall（1）` 的 `v1p8bc`；規格與跨頁引用所稱的 `uninstall（2）` 不在本組附件內，因此無法審查其實際刪除順序、config.toml 保護、根 justfile／`.dockerignore` 逐行詢問、`log/` 保留及進度檔最後刪除。

## 總評（codex 原文）

本組頁面目前不能交給使用者看；核心流程仍有多項規格矛盾、跨頁斷點與結果線歧義，尤其自身升級、dev 進度檔及 vk-resolve/1 內容必須先修正。

## 統計

- 跨頁共通：3 條（必修 2、選修 1）
- 逐頁：v1p7bd 3、v1p7bc 4、v1p7bcc 5、v1p7bcx 4、v1p7bccc 6、v1p8 4、v1p8ccc 4、v1p8c 4、v1p8cc 4、v1p8b 4、v1p8bccc 4、v1p8bc 5 ＝ 51 條
- 合計 54 條；必修 42、選修 12
- 類別分布：A 28、B 10、C 7、D 2、E 0、F 7


=== 附件 L：機械 lint（本組頁）===
[termcov] v1p5bc bB2: 「version.toml」（version.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5bc c15af: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5bc c15b: 「digest」（digest）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p5bc c21b2: 「--local」（--local）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p6 pend: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p6 n1px: 「6-24」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p6 n1px: 「6-31」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p6cc pend: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p6c pend: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7 a4q: 「6-13」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7 a4q: 「6-33」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7 a4q: 「薄殼」（薄殼）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7c b1e: 「version.local.toml」（version.local.toml）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7c b4: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7c b7q: 「6-24」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7ccc b11y: 「6-6」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7ccc b11y: 「6-7」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7ccc b11y: 「6-8」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cc b10ef: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cc b13ac: 「cache/」（cache/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cc b14r: 「6-6」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cc b14r: 「6-8」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cccc b15a: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7cccc b18r: 「6-14」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7b c_in0: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7bd pend: 「6-11」（訊息碼 6-xx）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7bd pend: 「metadata」（metadata）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7bd uD: 「gen/tools.just」（gen/…）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7bd d3b_1: 「baseline/」（baseline/）名詞表沒有對應條（name 與說明文都沒有）
[termcov] v1p7bd d2: 「gen/」（gen/…）名詞表沒有對應條（name 與說明文都沒有）

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
ERROR: Reconnecting... 2/5
ERROR: Reconnecting... 3/5
ERROR: Reconnecting... 4/5
ERROR: Reconnecting... 5/5
warning: Falling back from WebSockets to HTTPS transport. stream disconnected before completion: websocket closed by server before response.completed
codex
## 一、附件 R 逐條複核

判定以本次附件 P 與 PNG 為準；附件 L 已列者不重複。`v1p5b` 未附本版文字或縮圖，無法核對其頁內條目。

### 共通條目

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| G1 | 已修 | 現版改由各頁圖例統一約定每個「docker run 引擎」格隱含容器開始／結束事件；依本次審查指示，不再要求逐格畫事件。 |
| G2 | 已修 | 現版已移除所有結果先匯入同一 `launcher_exit` 再扇出的畫法，各結果直接進自己的終點；終點事件由圖例約定。 |
| G3 | 已修 | `v1p5bcc:c9bx`、`v1p6c:m0bx`、`v1p7ccc:b8bx` 均已補 create／cp／rm／暫存失敗出口。 |
| G4 | 未修 | 各頁仍重複大段沿革便條、共通名詞及完整契約；例如 upgrade 各頁反覆解釋 Renovate、GHCR、flock、resolve/apply，主流程仍被壓縮。此項原為選修。 |

### v1p5b

本版未附 `v1p5b`，R 的 1–5 均無法由目前附件判定。另依使用者本次明示，R-4 的 `baseline/.gitkeep` 屬已接受事項，不應再列為新問題。

### v1p5bcc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `c11b → c11c` 已分別畫重驗指紋與 argv／計畫一致性。 |
| 2 | 已修 | `c12` 及 `c12r` 已補父目錄不得經 symlink、src 不得越出 dist。 |
| 3 | 已修 | `c12b／c12br` 已納入 recipe／module／alias。 |
| 4 | 已修 | `c13 --否→ c13z` 已有「否」標籤。 |
| 5 | 未修 | `c12`、`c12b` 菱形仍以「是 →」起句，把前一步結果塞進判斷格；原條目為選修。 |

### v1p5bc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `c15a／c15af` 已列 state、started、verb、id、done、pending。 |
| 2 | 已修 | source 與 `local_image_id` 已拆成 `c21b`、`c21b2`。 |
| 3 | 已修 | state 與 declined_hash／lines 已拆成 `c21c`、`c21c2`。 |
| 4 | 未修 | `c23x` 仍宣稱「本段任一步」，但只從 `c15c`、`c21`、`c23` 拉失敗線；印記、各初始檔、metadata、tools.just、刪進度檔等失敗在圖上仍會繼續。 |
| 5 | 已修 | `c22` 已明寫原子替換，且與本次 cache 在同一 apply 內。 |

### v1p6

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `n0q` 已補專案根檢查，並說明 `_sync` 先 `cd`。 |
| 2 | 已修 | `n3` 明寫缺 stamp 時改用薄殼自描述首行比對，名詞表也強調不是視為相符。 |
| 3 | 已修 | pull 失敗與 local image ID 不符已拆成 `n1px`、`n1vx`。 |
| 4 | 已修 | `nq` 已收斂成「快路徑條件全部成立？」式摘要，細項移到 `nqr`。 |

### v1p6cc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `t3m` 與紅色失敗出口 `t3mx`。 |
| 2 | 已修 | `t1y` 已明列取件後全檔驗證。 |
| 3 | 已修 | `z0` 與 `z0q` 已拆成彙整及空清單判斷。 |
| 4 | 已修 | 現版以 `z0q` 的是／否明確分成 `apply|no` 與 `apply|yes`。 |

### v1p6c

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `m2c` 已補 argv／計畫一致性。 |
| 2 | 已修 | `m3vd` 已列 `--verify／CI 模式／版本變動那次`。 |
| 3 | 已修 | 已限制只重裝一次，第二次仍不符到紅色 `m3x2`。 |
| 4 | 已修 | 已補 `mq` 多工具迴圈。 |

### v1p7

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `a4a` 已明寫每個動詞各有一份執行紀錄。 |
| 2 | 已修 | `a4q` 已列薄殼、未完成接入、本機覆寫、未完成交易等，並引用 sync 頁。 |
| 3 | 已修 | `a4f／a4fx` 已補 ②～⑤ 第一個失敗即停。 |
| 4 | 已修 | 已拆成 `a8q` 門檻判斷與 `a8` merge 動作。 |
| 5 | 已修 | `a4r` 已改成「只看一行 diff 不足以證明升級可用」。 |

### v1p7c

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 頁首已限定單一工具，多工具／升引擎另指 E 頁。 |
| 2 | 已修 | `b2` 已納入「檔案失蹤」。 |
| 3 | 已修 | CI 未指定 tag 已由 `b7z → b7zz` 直接 `apply|no／0`。 |
| 4 | 已修 | `b7q` 已明確限定 registry 列舉憑證，並註明 pull 認證另走 6-24。 |
| 5 | 已修 | 已收斂成 `stdout vk-resolve/1` 協定輸出；原條目為選修。 |

### v1p7ccc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `b10c2`。 |
| 2 | 已修 | `b10n` 已含 alias，終點也改為 upgrade 回 1；但名詞表仍殘留「add 回 1」，另列新問題。 |
| 3 | 已修 | `b10c` 已明寫只計算會問的項目。 |
| 4 | 已修 | `b11 --否→ b11z` 已有標籤。 |
| 5 | 已修 | `b10c` 明寫「不發問」，再進 CI 判斷。 |

### v1p7cc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 狀態分流已移至 `v1p7b` 的互斥狀態機。 |
| 2 | 已修 | `v1p7b:q8c → s_bk` 已把改過的二進位／symlink 導向保留 warn。 |
| 3 | 已修 | deleted、unmanaged、declined、N 缺、D 缺及相等分支均已在 `v1p7b` 補齊。 |
| 4 | 已修 | append 已區分唯一命中與零／多處。 |
| 5 | 已修 | 新增檔 dest 已存在已導向 unmanaged + 6-11。 |
| 6 | 已修 | 判斷與問句已拆到 `b14q`、`b14ask`。 |
| 7 | 已修 | 建新檔、append、三方合併、換 N 已拆成 `b14a1`～`b14a4`。 |
| 8 | 已修 | 留原檔與記 conflicts 已拆成 `b14pc`、`b14pc2`。 |

### v1p7cccc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `b15b` 已交代 source 是整體目標版，而解析失敗檔以 conflicts 記錄、逐檔 baseline 留舊。 |
| 2 | 已修 | `b18` 已改成「通過的檔已在目標版、解析失敗檔留舊版」。 |
| 3 | 已修 | `b16b` 已明寫所有寫入落盤後才刪進度檔；衝突碼判定只讀已持久化的 metadata。 |
| 4 | 已修 | 待合併「是」分支直接到 `b16b`，不再連到 `b16f`。 |
| 5 | 已修 | `b18r` 已改成兩種情況皆回 2、訊息全列。 |

### v1p7b

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 名詞表已列完整 state 集合，不再限定 managed。 |
| 2 | 已修 | 已改為同一 declined_hash 不再問、N 改變才再問。 |
| 3 | 已修 | `q8／q8c` 先排除二進位／symlink，`q9` 才處理文字檔。 |
| 4 | 已修 | `s_un` 已明列 `state=unmanaged` 與 6-11。 |
| 5 | 已修 | 唯一命中判斷與後續詢問已分離。 |
| 6 | 已修 | `cx2` 已是橙色終點，`cx3` 已用白虛線跨頁出口。 |
| 7 | 已修 | 現版改為完整流程樹，不再把箭頭指向表頭。 |
| 8 | 已修 | 過密表格已改為狀態機；細節移至名詞表。 |

### v1p7bd（R 第 3 組）

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `d2c4` 重生 `gen/tools.just`。 |
| 2 | 已修 | `d2c` 已縮成單一取件動作。 |
| 3 | 已修 | `d1px` 已明列 6-24／6-31。 |

### v1p7bc（R 第 3 組）

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `s2a／s2dq` 已列 dev、全域撞名、憑證與詢問項目，任一不過整體不動。 |
| 2 | 已修 | `s2n` 已改白虛線跨頁出口並說明 Q27 彙總。 |
| 3 | 已修 | `s4` 已改白虛線跨頁出口，銜接 E(c) 頁。 |
| 4 | 已修 | 已拆成 `s2lo` 是否覆寫與 `s2lv` ID 是否不符。 |

## 二、本輪新發現

以下不重複附件 L。

| 頁 id | 元件 id／引文 | 類別 | 說明 | 必修／選修 |
|---|---|---|---|---|
| v1p5bcc | `c9q → c9qx` | A | 「resolve 非 0」與「resolve 回 0 但 stdout 文法不合法」被合成同一個否分支；前者須原碼傳出，後者才是 1 + 6-30，現圖無法決定實際結果。 | 必修 |
| v1p5bc | `c23x` 及失敗線 | B | 終點稱「本段任一步失敗」，但多個實際寫入格沒有連到它；應用明確的共通失敗匯流或逐步失敗線，不能只從三格代表全部。 | 必修 |
| v1p6 | `nqr`、`p6_tv0` | A | sync 快路徑漏掉「每個 `cache/<repo>/` 必須存在（目錄或 symlink）」；目前印記與 tools.just 相符但 cache 被刪時仍可能錯走快路徑。 | 必修 |
| v1p6cc | `p6r_tv7` | F | 6-33 名詞只寫 update 結束 1，漏掉 sync 也結束 1、help 才是仍回 0，容易誤解唯讀動詞的差異。 | 選修 |
| v1p6c | `m0q → m0qx` | A | 同 v1p5bcc：resolve 非 0 與 stdout 文法錯誤共用單一否分支，無法表達原碼傳出與 6-30 的差別。 | 必修 |
| v1p6c | `m0a → m0b → m1` | A／B | `m0a` 說「對每個 extract」，但 extract 完成後直接進 apply，沒有「還有下一個 extract？」迴圈；多工具 sync 可能只展開第一個 image。 | 必修 |
| v1p6c | `m5 → m5f` | A／B | `m5` 說「待辦有它時」才重生 tools.just，卻無判斷且始終畫寫入 `m5f`；應畫「tools.just 在待辦？」或將檔案寫線標成條件式。 | 必修 |
| v1p7 | `a4a → a4b` | A | check.sh 完整流程漏掉步驟 ⓪：先以 `git ls-files` 拒絕被納管的 `version.local.toml`。 | 必修 |
| v1p7 | `a4f／a4fx` | A | ④工具測試、⑤專案測試須原樣傳出第一個失敗碼；終點只寫「結束碼 2、3」，漏掉常見的 1 與工具可能回傳的其他碼。 | 必修 |
| v1p7c | `b7t／b7c → b7s` | A | 指定 tag 或查最新版後未判斷「目標是否等於現鎖定版」；沒有待合併且目標未變時應 `apply|no`／0，不應仍 extract、apply、重寫 cache 與 metadata。 | 必修 |
| v1p7c | `b1e` 之後 | A | upgrade 是可寫動詞；開始時若已有其他未完成交易應先恢復再繼續，本頁只檢查 conflicts，未畫一般進度檔偵測／恢復入口。 | 必修 |
| v1p7ccc | `b8q → b8qx` | A | 同 add／sync 頁：resolve 非 0 與協定文法不合法被壓成同一否分支，結果碼語意不成立。 | 必修 |
| v1p7ccc | `p7cp_tv11` | F | 本頁是 upgrade，名詞表卻仍寫命名空間撞名「add 回 1」，與流程格 `b10nx` 不一致。 | 選修 |
| v1p7bd | `d1f → d2c` | A | 本頁把 sync apply 畫成起容器後直接寫 cache，漏掉 flock、重驗指紋與原 argv／計畫一致性；既然本頁展開完整回退 sync，就不能省略這些寫入前檢查。 | 必修 |
| v1p7bd | `d2c3 → d2c4` | A | 版本變動取件後規格要求全檔 sha256 驗證，本頁寫完印記便直接重生 tools.just，漏掉驗證及失敗出口。 | 必修 |
| v1p7bc | `s1 → s2a` | A | resolve 輸出後未畫啟動器驗 `vk-resolve/1` 文法；現圖直接依「引擎有新版」操作 image、apply，缺少 6-30 與 resolve 非 0 原碼傳出。 | 必修 |
| v1p7bc | `s2q → s2ln／s2lo` | A | 有新版時先 inspect／pull 正式新引擎，之後才判斷本機引擎覆寫；規格是「正式 ref inspect/pull」與「有 local 覆寫時 inspect 並驗 ID」二擇一，判斷覆寫必須在 pull 前。 | 必修 |
| v1p7bc | `s2h` | A | 格內寫「grep version.toml…（本機覆寫 vendor_kit= 優先）」錯誤；接手判定必須比較正式 `version.toml` 的引擎版本鎖定行前後，local 覆寫只影響接手時實際使用哪個 image。 | 必修 |

## 三、逐頁結論

- `v1p5bcc`：仍有 resolve 結果分流錯誤。
- `v1p5bc`：仍有寫入失敗線不能涵蓋「任一步」的問題。
- `v1p6`：快路徑缺 cache 存在條件。
- `v1p6cc`：主流程無新規格錯誤；只有一項名詞說明可再補。
- `v1p6c`：仍缺多 extract 迴圈，且 resolve 錯誤分流不正確。
- `v1p7`：漏 check.sh 步驟 ⓪及完整失敗碼。
- `v1p7c`：漏目標版本未變的 no-op 與未完成交易恢復。
- `v1p7ccc`：resolve 非 0／文法錯誤仍混在一起。
- `v1p7cc`：本輪未發現附件 L 以外的新問題。
- `v1p7cccc`：本輪未發現附件 L 以外的新問題。
- `v1p7b`：本輪未發現附件 L 以外的新問題。
- `v1p7bd`：回退 sync 漏 apply 前置檢查與版本變動後全檔驗證。
- `v1p7bc`：升引擎的協定驗證、local 覆寫判斷順序及版本鎖定行來源仍錯。
- `v1p5b`：本版未附，無法判定。

總評：本組已修掉上一版多數狀態機與跨頁問題，但 sync 快路徑、回退驗證及升引擎接手仍有會導致錯誤實作的必修缺口，目前仍不能交給使用者看。
tokens used
184,630
## 一、附件 R 逐條複核

判定以本次附件 P 與 PNG 為準；附件 L 已列者不重複。`v1p5b` 未附本版文字或縮圖，無法核對其頁內條目。

### 共通條目

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| G1 | 已修 | 現版改由各頁圖例統一約定每個「docker run 引擎」格隱含容器開始／結束事件；依本次審查指示，不再要求逐格畫事件。 |
| G2 | 已修 | 現版已移除所有結果先匯入同一 `launcher_exit` 再扇出的畫法，各結果直接進自己的終點；終點事件由圖例約定。 |
| G3 | 已修 | `v1p5bcc:c9bx`、`v1p6c:m0bx`、`v1p7ccc:b8bx` 均已補 create／cp／rm／暫存失敗出口。 |
| G4 | 未修 | 各頁仍重複大段沿革便條、共通名詞及完整契約；例如 upgrade 各頁反覆解釋 Renovate、GHCR、flock、resolve/apply，主流程仍被壓縮。此項原為選修。 |

### v1p5b

本版未附 `v1p5b`，R 的 1–5 均無法由目前附件判定。另依使用者本次明示，R-4 的 `baseline/.gitkeep` 屬已接受事項，不應再列為新問題。

### v1p5bcc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `c11b → c11c` 已分別畫重驗指紋與 argv／計畫一致性。 |
| 2 | 已修 | `c12` 及 `c12r` 已補父目錄不得經 symlink、src 不得越出 dist。 |
| 3 | 已修 | `c12b／c12br` 已納入 recipe／module／alias。 |
| 4 | 已修 | `c13 --否→ c13z` 已有「否」標籤。 |
| 5 | 未修 | `c12`、`c12b` 菱形仍以「是 →」起句，把前一步結果塞進判斷格；原條目為選修。 |

### v1p5bc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `c15a／c15af` 已列 state、started、verb、id、done、pending。 |
| 2 | 已修 | source 與 `local_image_id` 已拆成 `c21b`、`c21b2`。 |
| 3 | 已修 | state 與 declined_hash／lines 已拆成 `c21c`、`c21c2`。 |
| 4 | 未修 | `c23x` 仍宣稱「本段任一步」，但只從 `c15c`、`c21`、`c23` 拉失敗線；印記、各初始檔、metadata、tools.just、刪進度檔等失敗在圖上仍會繼續。 |
| 5 | 已修 | `c22` 已明寫原子替換，且與本次 cache 在同一 apply 內。 |

### v1p6

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `n0q` 已補專案根檢查，並說明 `_sync` 先 `cd`。 |
| 2 | 已修 | `n3` 明寫缺 stamp 時改用薄殼自描述首行比對，名詞表也強調不是視為相符。 |
| 3 | 已修 | pull 失敗與 local image ID 不符已拆成 `n1px`、`n1vx`。 |
| 4 | 已修 | `nq` 已收斂成「快路徑條件全部成立？」式摘要，細項移到 `nqr`。 |

### v1p6cc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `t3m` 與紅色失敗出口 `t3mx`。 |
| 2 | 已修 | `t1y` 已明列取件後全檔驗證。 |
| 3 | 已修 | `z0` 與 `z0q` 已拆成彙整及空清單判斷。 |
| 4 | 已修 | 現版以 `z0q` 的是／否明確分成 `apply|no` 與 `apply|yes`。 |

### v1p6c

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `m2c` 已補 argv／計畫一致性。 |
| 2 | 已修 | `m3vd` 已列 `--verify／CI 模式／版本變動那次`。 |
| 3 | 已修 | 已限制只重裝一次，第二次仍不符到紅色 `m3x2`。 |
| 4 | 已修 | 已補 `mq` 多工具迴圈。 |

### v1p7

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `a4a` 已明寫每個動詞各有一份執行紀錄。 |
| 2 | 已修 | `a4q` 已列薄殼、未完成接入、本機覆寫、未完成交易等，並引用 sync 頁。 |
| 3 | 已修 | `a4f／a4fx` 已補 ②～⑤ 第一個失敗即停。 |
| 4 | 已修 | 已拆成 `a8q` 門檻判斷與 `a8` merge 動作。 |
| 5 | 已修 | `a4r` 已改成「只看一行 diff 不足以證明升級可用」。 |

### v1p7c

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 頁首已限定單一工具，多工具／升引擎另指 E 頁。 |
| 2 | 已修 | `b2` 已納入「檔案失蹤」。 |
| 3 | 已修 | CI 未指定 tag 已由 `b7z → b7zz` 直接 `apply|no／0`。 |
| 4 | 已修 | `b7q` 已明確限定 registry 列舉憑證，並註明 pull 認證另走 6-24。 |
| 5 | 已修 | 已收斂成 `stdout vk-resolve/1` 協定輸出；原條目為選修。 |

### v1p7ccc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `b10c2`。 |
| 2 | 已修 | `b10n` 已含 alias，終點也改為 upgrade 回 1；但名詞表仍殘留「add 回 1」，另列新問題。 |
| 3 | 已修 | `b10c` 已明寫只計算會問的項目。 |
| 4 | 已修 | `b11 --否→ b11z` 已有標籤。 |
| 5 | 已修 | `b10c` 明寫「不發問」，再進 CI 判斷。 |

### v1p7cc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 狀態分流已移至 `v1p7b` 的互斥狀態機。 |
| 2 | 已修 | `v1p7b:q8c → s_bk` 已把改過的二進位／symlink 導向保留 warn。 |
| 3 | 已修 | deleted、unmanaged、declined、N 缺、D 缺及相等分支均已在 `v1p7b` 補齊。 |
| 4 | 已修 | append 已區分唯一命中與零／多處。 |
| 5 | 已修 | 新增檔 dest 已存在已導向 unmanaged + 6-11。 |
| 6 | 已修 | 判斷與問句已拆到 `b14q`、`b14ask`。 |
| 7 | 已修 | 建新檔、append、三方合併、換 N 已拆成 `b14a1`～`b14a4`。 |
| 8 | 已修 | 留原檔與記 conflicts 已拆成 `b14pc`、`b14pc2`。 |

### v1p7cccc

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `b15b` 已交代 source 是整體目標版，而解析失敗檔以 conflicts 記錄、逐檔 baseline 留舊。 |
| 2 | 已修 | `b18` 已改成「通過的檔已在目標版、解析失敗檔留舊版」。 |
| 3 | 已修 | `b16b` 已明寫所有寫入落盤後才刪進度檔；衝突碼判定只讀已持久化的 metadata。 |
| 4 | 已修 | 待合併「是」分支直接到 `b16b`，不再連到 `b16f`。 |
| 5 | 已修 | `b18r` 已改成兩種情況皆回 2、訊息全列。 |

### v1p7b

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 名詞表已列完整 state 集合，不再限定 managed。 |
| 2 | 已修 | 已改為同一 declined_hash 不再問、N 改變才再問。 |
| 3 | 已修 | `q8／q8c` 先排除二進位／symlink，`q9` 才處理文字檔。 |
| 4 | 已修 | `s_un` 已明列 `state=unmanaged` 與 6-11。 |
| 5 | 已修 | 唯一命中判斷與後續詢問已分離。 |
| 6 | 已修 | `cx2` 已是橙色終點，`cx3` 已用白虛線跨頁出口。 |
| 7 | 已修 | 現版改為完整流程樹，不再把箭頭指向表頭。 |
| 8 | 已修 | 過密表格已改為狀態機；細節移至名詞表。 |

### v1p7bd（R 第 3 組）

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | 已補 `d2c4` 重生 `gen/tools.just`。 |
| 2 | 已修 | `d2c` 已縮成單一取件動作。 |
| 3 | 已修 | `d1px` 已明列 6-24／6-31。 |

### v1p7bc（R 第 3 組）

| R 條目 | 判定 | 複核結果 |
|---|---|---|
| 1 | 已修 | `s2a／s2dq` 已列 dev、全域撞名、憑證與詢問項目，任一不過整體不動。 |
| 2 | 已修 | `s2n` 已改白虛線跨頁出口並說明 Q27 彙總。 |
| 3 | 已修 | `s4` 已改白虛線跨頁出口，銜接 E(c) 頁。 |
| 4 | 已修 | 已拆成 `s2lo` 是否覆寫與 `s2lv` ID 是否不符。 |

## 二、本輪新發現

以下不重複附件 L。

| 頁 id | 元件 id／引文 | 類別 | 說明 | 必修／選修 |
|---|---|---|---|---|
| v1p5bcc | `c9q → c9qx` | A | 「resolve 非 0」與「resolve 回 0 但 stdout 文法不合法」被合成同一個否分支；前者須原碼傳出，後者才是 1 + 6-30，現圖無法決定實際結果。 | 必修 |
| v1p5bc | `c23x` 及失敗線 | B | 終點稱「本段任一步失敗」，但多個實際寫入格沒有連到它；應用明確的共通失敗匯流或逐步失敗線，不能只從三格代表全部。 | 必修 |
| v1p6 | `nqr`、`p6_tv0` | A | sync 快路徑漏掉「每個 `cache/<repo>/` 必須存在（目錄或 symlink）」；目前印記與 tools.just 相符但 cache 被刪時仍可能錯走快路徑。 | 必修 |
| v1p6cc | `p6r_tv7` | F | 6-33 名詞只寫 update 結束 1，漏掉 sync 也結束 1、help 才是仍回 0，容易誤解唯讀動詞的差異。 | 選修 |
| v1p6c | `m0q → m0qx` | A | 同 v1p5bcc：resolve 非 0 與 stdout 文法錯誤共用單一否分支，無法表達原碼傳出與 6-30 的差別。 | 必修 |
| v1p6c | `m0a → m0b → m1` | A／B | `m0a` 說「對每個 extract」，但 extract 完成後直接進 apply，沒有「還有下一個 extract？」迴圈；多工具 sync 可能只展開第一個 image。 | 必修 |
| v1p6c | `m5 → m5f` | A／B | `m5` 說「待辦有它時」才重生 tools.just，卻無判斷且始終畫寫入 `m5f`；應畫「tools.just 在待辦？」或將檔案寫線標成條件式。 | 必修 |
| v1p7 | `a4a → a4b` | A | check.sh 完整流程漏掉步驟 ⓪：先以 `git ls-files` 拒絕被納管的 `version.local.toml`。 | 必修 |
| v1p7 | `a4f／a4fx` | A | ④工具測試、⑤專案測試須原樣傳出第一個失敗碼；終點只寫「結束碼 2、3」，漏掉常見的 1 與工具可能回傳的其他碼。 | 必修 |
| v1p7c | `b7t／b7c → b7s` | A | 指定 tag 或查最新版後未判斷「目標是否等於現鎖定版」；沒有待合併且目標未變時應 `apply|no`／0，不應仍 extract、apply、重寫 cache 與 metadata。 | 必修 |
| v1p7c | `b1e` 之後 | A | upgrade 是可寫動詞；開始時若已有其他未完成交易應先恢復再繼續，本頁只檢查 conflicts，未畫一般進度檔偵測／恢復入口。 | 必修 |
| v1p7ccc | `b8q → b8qx` | A | 同 add／sync 頁：resolve 非 0 與協定文法不合法被壓成同一否分支，結果碼語意不成立。 | 必修 |
| v1p7ccc | `p7cp_tv11` | F | 本頁是 upgrade，名詞表卻仍寫命名空間撞名「add 回 1」，與流程格 `b10nx` 不一致。 | 選修 |
| v1p7bd | `d1f → d2c` | A | 本頁把 sync apply 畫成起容器後直接寫 cache，漏掉 flock、重驗指紋與原 argv／計畫一致性；既然本頁展開完整回退 sync，就不能省略這些寫入前檢查。 | 必修 |
| v1p7bd | `d2c3 → d2c4` | A | 版本變動取件後規格要求全檔 sha256 驗證，本頁寫完印記便直接重生 tools.just，漏掉驗證及失敗出口。 | 必修 |
| v1p7bc | `s1 → s2a` | A | resolve 輸出後未畫啟動器驗 `vk-resolve/1` 文法；現圖直接依「引擎有新版」操作 image、apply，缺少 6-30 與 resolve 非 0 原碼傳出。 | 必修 |
| v1p7bc | `s2q → s2ln／s2lo` | A | 有新版時先 inspect／pull 正式新引擎，之後才判斷本機引擎覆寫；規格是「正式 ref inspect/pull」與「有 local 覆寫時 inspect 並驗 ID」二擇一，判斷覆寫必須在 pull 前。 | 必修 |
| v1p7bc | `s2h` | A | 格內寫「grep version.toml…（本機覆寫 vendor_kit= 優先）」錯誤；接手判定必須比較正式 `version.toml` 的引擎版本鎖定行前後，local 覆寫只影響接手時實際使用哪個 image。 | 必修 |

## 三、逐頁結論

- `v1p5bcc`：仍有 resolve 結果分流錯誤。
- `v1p5bc`：仍有寫入失敗線不能涵蓋「任一步」的問題。
- `v1p6`：快路徑缺 cache 存在條件。
- `v1p6cc`：主流程無新規格錯誤；只有一項名詞說明可再補。
- `v1p6c`：仍缺多 extract 迴圈，且 resolve 錯誤分流不正確。
- `v1p7`：漏 check.sh 步驟 ⓪及完整失敗碼。
- `v1p7c`：漏目標版本未變的 no-op 與未完成交易恢復。
- `v1p7ccc`：resolve 非 0／文法錯誤仍混在一起。
- `v1p7cc`：本輪未發現附件 L 以外的新問題。
- `v1p7cccc`：本輪未發現附件 L 以外的新問題。
- `v1p7b`：本輪未發現附件 L 以外的新問題。
- `v1p7bd`：回退 sync 漏 apply 前置檢查與版本變動後全檔驗證。
- `v1p7bc`：升引擎的協定驗證、local 覆寫判斷順序及版本鎖定行來源仍錯。
- `v1p5b`：本版未附，無法判定。

總評：本組已修掉上一版多數狀態機與跨頁問題，但 sync 快路徑、回退驗證及升引擎接手仍有會導致錯誤實作的必修缺口，目前仍不能交給使用者看。
