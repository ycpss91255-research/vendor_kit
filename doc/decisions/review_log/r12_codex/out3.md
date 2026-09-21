Reading prompt from stdin...
OpenAI Codex v0.155.0
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 01a0b9e8-2af7-7ff0-9659-cae28da7b41e
--------
user
你是圖面審查員。vendor_kit：下游 repo 把 dist/ 打成純資料容器 image，下游專案用 bootstrap.sh + `just vendor_kit <動詞>` 取得工具、鎖版本、三方合併初始檔。附件 S 是規格正本（§0–§9）。附件 P 是本組每一頁從 draw.io XML 抽出的文字（節點 [kind] id: 文字；邊 src --標籤--> dst；名詞表；跨頁引用），附上縮圖 PNG（頁 id 同名）。附件 L 是機械 lint 已抓到的條目（不必重複）。

注意：圖上名詞仍是舊名（工具 repo、使用者、鎖定行、frozen、進度日誌、操作紀錄檔、協定號、floor 等），第十三輪才統一換新名——**不要**回報名詞新舊問題。

審查標準（使用者定）：1 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。2 顏色語意一致：藍＝引擎做、白＝啟動器做、綠＝0、橙＝需人處理、紅＝失敗、白虛線橢圓＝來自其他頁。3 字要少，一般人看得懂；專有名詞要在該頁名詞表。4 線段不穿無關方框、不交叉、不壓字、不懸空、不該折的不折。5 每個方塊只放一件事（一個動作／判斷／檔案）；一格兩件事就是問題。6 內容要跟規格一致；例子一律 `<repo>`。

逐頁找：(A) 與規格矛盾、缺分支、順序錯、誰做的（啟動器 vs 引擎）畫錯；(B) 頁間入口出口不對、懸空、缺線；(C) 一格多事；(D) 顏色不符語意；(E) 排版（看縮圖：線壓字、標籤位置歧義、線穿框）；(F) 一般人看不懂的句子或名詞表漏項。每條給：頁 id、元件 id（或引文）、類別、一句說明、必修／選修。若某頁沒有問題請明說。最後一句總評：本組頁面能否交給使用者看。繁體中文。


=== 附件 S：規格 §0–§9 ===
# vendor_kit 介面規格（interface reference）v3.3（2026-09-20；**v3.3 = codex 審 00–02 頁 56 條全部採納 + 02 頁 6 點定案 + 兩條新規則 (a)(b) + 三條補列不變量 + 「專案」定名，改動見 §10 #131–#146**；v3.2 = 01 頁四點拍板（2026-09-20）+ 名詞定案（第 0 頁）落實，改動見 §10 #117–#130；v3 併入 proposal_v2 v2.10–v2.12、grilling「2026-09-20 第八～九輪審查後定案」、r9 規格層矛盾，改動見 §10 #58–#95；**v3.1 併入 v2.13（§9.1 P4–P13 結案）與 v2.14（第十輪後圖面落實與小定案），改動見 §10 #96–#116**）

用途：後續每張票唯一可引用的 input／output 定義；`/to-spec` 的原料。前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）、`interface_spec.v2.final.md`（v2 定稿 = v2.7 併入後、v3 併入前）、`interface_spec.v3.0.md`（v3 = v2.13／v2.14 併入前）、`interface_spec.v3.1.md`（v3.1 = 01 頁拍板與名詞定案落實前）、`interface_spec.pre_codex1.md`（v3.2 = codex 00–02 審查併入前）。

來源優先序（高 → 低）：
00. v3.3 新併入：`decisions/review/codex_findings_00_02.md`（56 條全部採納）；`grilling.md`「02 頁 6 點定案」「兩條新規則 (a)(b)」「補三條不變量」「專案定名」（2026-09-20）。
0. v3.1 新併入：`proposal_v2.md` **v2.14 → v2.13**（v2.13 = 主對話依既定原則對 §9.1 P4–P13 的取捨，使用者可否決；v2.14 = 第十輪後圖面落實與兩個小定案）。
0′. v3 併入：`grilling.md`「2026-09-20 第八～九輪審查後定案」；`proposal_v2.md` **v2.12 → v2.11 → v2.10**（v2.11-1 撤回 v2.10-4；衝突以最新為準）；`review_v2r9_findings.md` 中屬**規格層**的矛盾（選項表 `--local` 適用欄拆 bootstrap.sh／add、E(c) 指定 `@tag` 與 CI 模式是兩條分支、help 遇未完成交易印 6-33 仍 0、bootstrap 逐 `-t` 一個失敗即中止）；`decisions/log/agy_summary.md`、`agy_summary2.md`、`draft.md` 只作 §4.10 的設計依據，**只取 v2.12 已定案的部分**。
1. `grilling.md` 2026-09-19 條目（Q22 sync 快路徑、Q23 結束碼 3、Q24 vk-resolve 格式與實作層取捨、Q25 選項表、Q26 離線 `.digest`、Q27 多工具彙總、「規格審查 16 條必修」直接採納）。
2. `interface_spec_review.md`「最終建議」一～五節（16 條必修、22 個待定的建議值、vk-resolve/1 骨架、結束碼 3 邊界、F1 定案）與「規格與定案不符」清單——全部套用，除非與 grilling 相衝（grilling 勝）。
3. `proposal_v2.md`：v2.5 → v2.4 → v2.3 → v2.2 → v2.1 → 正文。
4. 其他 decisions／issue（#26、#27、#28、#29、base_pitfalls、compat、isolation、contract）。

每條規格後以 <sub>[來源]</sub> 標注；`[待定]` 集中於 §9；本次每處改動的依據列於 §10；矛盾處理於 §11。占位符（名詞一律照第 0 頁「00 名詞與縮寫」，`<sub>` 出處註記保留來源原文的舊詞）：`<repo>` 下游 repo 名、`<ns>` just 命名空間、`<dir>` 目錄、`<tag>`、`<digest>`、`<ref>` = `<image>:<tag>@sha256:<digest>`、`vX`／`vY` 引擎版本、`P` 協定整數、`N` schema 整數、`<org>` GitHub 組織名、`<id>` 交易 id（= `<trace_id>`，32 hex）、`<id8>` = trace_id 前 8 碼、`<UTC-ts>` = `YYYYMMDDTHHMMSSZ`、`<verb>` 動詞名、`<專案根>` = 含 `.vendor_kit/` 的目錄。**專案** = 下游使用者的 git repo（或 monorepo 子專案），接入後含 `.vendor_kit/`；VK 的動詞都在專案裡跑（與提供工具的「下游 repo」區分；grilling 2026-09-20 定名）。

## 0. 共通前提（所有動詞）

| 項目 | 規格 |
|---|---|
| 專案根 | = 專案內含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；不是 git toplevel。第一次 `install` 時尚無 `.vendor_kit/`，候選專案根 = 呼叫目錄。<sub>[grilling Q20 定案（改）；review I-47]</sub> |
| 執行位置 | vendor_kit 動詞只准在專案根執行：recipe 檢查 `invocation_directory() == justfile_directory()`，否則 1 印 6-9。**所有動詞一體適用，`sync` 亦無例外**（原 F1「sync 豁免此檢查」撤回）；工具 recipe 自動觸發的 `_sync` 自己先 `cd` 到專案根再呼叫 `just vendor_kit sync`（§3.6），故不受影響。工具自己的 recipe 是否擋由工具決定。<sub>[grilling Q20 修正；01 頁拍板 2026-09-20 (2)]</sub> |
| git | 專案根須在某 git repo 內（主機側 `git rev-parse --is-inside-work-tree`）；引擎不讀 `.git`、不碰 index；不做 `git init`。禁止巢狀：install 時上層**或下層**已有 `.vendor_kit/` → 1 + 6-35（01 頁拍板確認）。worktree（`.git` 是檔）與 submodule 同樣適用（後者以 §7.4-20 實測為準）。<sub>[grilling Q20、19條-1、-10；review I-47]</sub> |
| 主機需求 | docker ≥ 19.03（或 Podman ≥ 4.9，見 §3.1）、just ≥ 1.33.0（GitHub release 下載版）、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA → issue v2。主機命令白名單見 §3.1。<sub>[grilling Q4、Q8、19條-2、-13；v2.4-10]</sub> |
| 不變量 | 對專案檔：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（= 不用工具版本取代客製內容；例外只有根 justfile 一行、根 `.dockerignore` 四行、已納管初始檔（含 `config.toml`）經同意的換版／三方合併）。執行紀錄（§4.10）與進度檔是 vendor_kit 自己的檔，不適用四原則。自動化（sync）只碰不進 git 的東西（cache/、gen/）。never fail silently（失敗印原因；需人處理另附可複製指令，§2「結束的兩種語意」）。另三條資料／原子性不變量（01 頁 I15–I17，grilling 2026-09-20 補列）：**I15** 每個 VK TOML 有檔案版、讀時忽略未知欄位寫時保留、跨版直接遷移（§4 通則、§8-7）；**I16** 多工具可寫動詞（不帶 repo 的 upgrade、uninstall）先對全部工具完整預檢、任一不過整體不動（§1.2）；**I17** `gen/tools.just` 最後寫且與 cache 同一 apply 內原子替換（§4.4、§8-9）。<sub>[grilling 隔離題、Q22 補、2026-09-20 補三條不變量；proposal §1；isolation 最終建議；codex 00–02 #19、#30、#32、#33]</sub> |
| 詢問通則 | 需詢問但無 tty／EOF 且無 `-y` → 1 印 6-4；EOF／Ctrl-C = 中止整個 apply 回 1、不套用、**不記 declined**（declined 只記明確回答「否」）。明確回答「否」→ 不寫、metadata 依 §4.3 記錄。`-y` 只省略詢問，不授權覆蓋既有未納管檔、不硬加 append 行、**不解除 CI 模式**（`-y` 與 CI 模式為獨立開關，見下列 CI 模式）。<sub>[grilling 19條-6、Q13；v2.5-1、v2.5-4；review Claude 原文 12；01 頁拍板 2026-09-20 (3)]</sub> |
| CI 模式 | `CI` 真值規則：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；check.sh 自己 `export CI=1`。CI 模式 = 不寫任何 tracked 檔、不查最新版（**`update` 除外**：仍查 registry，它是唯讀動詞、查詢即其用途；02 頁 6 點定案 ①）；升為失敗的警告**明列**：薄殼不符、基準版落後、未完成接入、任何 local 覆寫、需改 tracked 檔（與 `-y` 無關）；Q15 的「沒納管／拒絕過」提醒**不**紅燈；仍拉鎖定版 image、仍寫 cache/、gen/。`update` 不受 CI 模式影響（唯讀、不寫檔）。**`-y` 與 CI 模式是兩個獨立開關**：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`；CI 模式下需改進 git 的檔一律 → 1 印清單，與 `-y` 無關。CI 模式由 `CI` 環境變數為真觸發（CI 平台自設或 check.sh 自設；本機手設 = 唯讀驗證，允許）。<sub>[v2.1 A；v2.2 A；v2.5-1；review 必修 4；review I-02、Claude 原文 25；01 頁拍板 2026-09-20 (3)]</sub> |
| 進度檔 | **所有可寫動詞第一個寫入前必建進度檔，不設例外**：add／`upgrade <repo>` 記 metadata `[progress]`；install（**第一次也建**，該日誌同時是「不留半成品」的清除清單，成功後刪；v2.13 P5）／remove／uninstall／undev／prune／**dev**（新規則 (b)：它寫本機覆寫、cache symlink、印記三處，同樣建 `.tmp.dev.<id>.toml`；撤回原「dev 不建」）／`upgrade vendor_kit`（含不帶 repo 時 E(a) 的自身那段）放 `.vendor_kit/.tmp.<verb>.<id>.toml`（§4.6；自身升級 = `.tmp.upgrade.<id>.toml`，在改 version.toml 第一行**之前**建，新引擎重產薄殼完成後由新引擎刪）。`<id>` = trace_id（§4.10）。可寫動詞開始前偵測到未完成交易 → 先恢復再繼續（`upgrade vendor_kit` 的恢復 = 重跑 `upgrade vendor_kit`），失敗明列 6-27；唯讀動詞只偵測、**不自動恢復**、除執行紀錄外不寫任何檔：**sync／update 印 6-33 結束 1，help 印 6-33 仍 0**。prune 特例：遇活躍（未恢復）日誌只列出並印 6-33、不刪、**不視為未完成交易**（不擋 prune、不恢復；差集與 `apply prune` 照做）。第一次 install 也建（v2.13 P5）；dev 也建（新規則 (b)）。<sub>[grilling 進度日誌條、Q24、2026-09-20 定案、新規則 (b)；v2.2 C；review 必修 9；v2.7-7；v2.9-6、-8；v2.10-6；v2.11-1；v2.12 L5]</sub> |
| 執行紀錄 | 每個動詞每次執行（含 help、update、sync 快路徑、prune、`--dry-run`）除印 tty 外必寫一檔 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）：**順序（新規則 (a)）**：不寫檔、不拉 image、不起容器的前置檢查（git repo？just 版本？）可在建紀錄之前；任何寫入／pull／起引擎之前必已有紀錄（非 git 目錄無處可寫）。啟動器 mkdir + 建檔 + 寫 `launcher_start`，失敗 → 1 + 6-38、零寫入；引擎啟動時 append `engine_start`，失敗 → 1 + 6-38、不進 resolve；無 `--no-log`。它是 vendor_kit 自己的檔（不進 git、不進 build context、不適用專案檔四原則），與進度檔分工：進度檔管交易恢復（成功即刪），執行紀錄管事後追溯（保留規則 §4.10）。`trace_id` 同時是進度檔交易 id。凡印到 tty 的訊息一律同句進 `body`。bootstrap.sh 就是第一次接入的啟動器：驗 git repo／just（唯讀）→ `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`，之後才 pull／install（§1.2 bootstrap.sh）。<sub>[v2.11-3；v2.12 L1–L5；v2.13 P4；grilling 新規則 (a)；codex 00–02 #8、#26、#37]</sub> |
| config.toml | `.vendor_kit/config.toml`（§4.9）：進 git；install 建（含註解與預設值）；缺檔或缺鍵 = 預設；`schema = 1`、`[log] keep = 50`、`days = 30`；非正整數 → 預設 + 警告；對 `upgrade vendor_kit` 是三方合併初始檔（要改先問）；啟動器只 grep 正規行、引擎用 TOML parser。<sub>[v2.12 L3′]</sub> |
| 事件註冊表 | `log-events.txt`：`event_name` 的有限集合（§4.10 事件表；L6 集合**待 codex 審**），啟動器與引擎寫 log 前以 `grep -Fxq` 對表，未註冊 → FATAL（實作錯誤，不是下游使用者錯誤）；CI 靜態擋原始碼中未註冊的事件名。落點：真本 `log-events.txt` 在引擎 image；啟動器端薄殼 `log.sh` 內嵌一份啟動器事件白名單（`case`），release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（§4.10）。<sub>[v2.12 L5、L6；agy_summary2「事件名註冊表前例」；v2.13 P9]</sub> |
| 引擎環境 | 容器內 `LC_ALL=C.UTF-8`、`TZ=UTC`，時間戳 UTC ISO 8601；HOME 指容器內暫存（實作細節）。使用者身分見 §3.1 `-u` 規則。<sub>[grilling 19條-3、-4]</sub> |
| 路徑 | 啟動器一律引號（含空白、`$`、非 ASCII）；vk-resolve 內自由文字以八進位跳脫（§3.3）；執行紀錄內 argv 與路徑逐項 JSON 跳脫（§4.10）。<sub>[grilling 19條-8、Q24；v2.12 L5]</sub> |
| 多工具彙總 | 不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；`update` 同時遇 1 與 2 → 1；訊息全列。<sub>[grilling Q27]</sub> |
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
| `--dry-run` | — | bool | uninstall、add、remove、upgrade、prune | 唯讀預覽（仍拉 image 展開） |
| `--source <image>` | — | string | add | image 路徑不符 `<org>/<repo>-dist` 慣例時 |
| `--local <image tag 或 tar>` | — | string | bootstrap.sh | 離線。值的判別（B1）：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立 → 1 + 6-37。**tar 形**：`docker load` 後由同名 `.digest` 旁檔取 index digest（§4.8）。**tag 形**：不讀 `.digest`、只 `docker image inspect` 本機 image ID（記 version.local.toml）；version.toml 正式 ref@digest 來源 = 專案已有 version.toml → 該行；第一次接入 → bootstrap.sh 內嵌引擎 ref。不論哪形，前置檢查（git repo、just ≥ 1.33.0）一律先做 <sub>[grilling 2026-09-19 末條；v2.7-2；v2.9-1；v2.10-2；r9]</sub> |
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
| `bootstrap.sh` | `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag 或 tar>] [--timeout <秒>] [-h]` | 無 | **順序**：驗 git repo／just（下列）→ `mkdir -p .vendor_kit/log/bootstrap/`（含目錄內 `.gitignore`）→ 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install（v2.13 P4）。在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref；最低介面版檢查（§2）；`--local` 不論 tar 或 tag 形，以上前置檢查一律先做 <sub>[grilling Q8、Q18；v2.4-5；v2.9-1]</sub> | `docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref（拉不到 → 1 + 6-24／逾時 6-31，**失敗出口**、不退回內嵌；tag 形 `--local` 的 `docker image inspect` 本機無此 image 亦為失敗出口；v2.14-5）→ 引擎 `install`（失敗 → 1：依 `.tmp.install.<id>.toml` 清半成品，**`.vendor_kit/log/` 保留**，訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」；v2.13 P4、P5）→ 逐 `-t` **依序**呼叫 `add <repo>[@<tag>]`，**任一 add 回非 0 → 立即中止**、不處理後續 `-t`、整體回 1 並列出已完成／未處理的工具（已完成的 add 保留；「不留半成品」只對第一次 install 成立）；`--local` 時 version.toml 仍寫正式 ref@digest：tar 形由同名 `.digest` 旁檔取得 index digest（§4.8），tag 形**不讀 `.digest`**、只 `docker image inspect` 本機 image ID，正式 ref 來源 = 專案已有 version.toml → 該行、第一次接入 → bootstrap.sh 內嵌引擎 ref；version.local.toml 寫 `vendor_kit = "<tag>"` + `vendor_kit_image_id`，在 install 成功後才寫、失敗清除；不自刪。離線契約入口 = `bootstrap.sh --local <tar>`（值判別見 §1.1 B1）；離線包內另含 `local_bootstrap.sh` **便利包裝**（偵測 daemon 架構 `docker version --format '{{.Server.Arch}}'`、挑該平台 tar、`exec ./bootstrap.sh --local <tar> "$@"`），不是契約入口、不另定介面 <sub>[proposal §2；#27；grilling Q26；v2.5-8；review 必修 15；v2.7-1；v2.9-1；v2.10-2；r9]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 | 0；1 失敗不留半成品（只對第一次 install 成立）；任一 `-t` 的 add 失敗 → 1（中止）；3 見 §2 <sub>[proposal §2；v2.2 C；r9]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" -w /repo <引擎 ref> --protocol P install` <sub>[#27；review B7]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 + 6-17 <sub>[codex_verbs]</sub> | 在 git repo 內（否 → 1 + 6-16）；上層與下層皆無 `.vendor_kit/`（否 → 1 + 6-35）；不被 gen/.stamp 比對擋；第一次／修復判定用薄殼自描述首行（§4.5）：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 + 6-28 列差異不動 <sub>[proposal §2；grilling Q20、Q17；v2.5-8]</sub> | 建 `.vendor_kit/`：version.toml（含 schema、written_by）、**config.toml**（§4.9，含註解與預設值；修復型缺則建、存在不動）、entry.just、vendor.just、.gitignore（含 `log/`）、ci/check.sh、baseline/（空、不建 metadata）、gen/.stamp；**log/**（含目錄內 `.gitignore`）由**啟動器**在寫 `launcher_start` 前建（第一次接入 = bootstrap.sh 建 `log/bootstrap/`；§4.10、v2.13 P4），引擎不建；根 justfile 無 → 建（§4.5 兩段式內容：import 一行 + `default:`／`\t@just --list` 兩行）；有 → 問後加一行；已含那行 → 不再加；根 `.dockerignore`：無 → 建（四行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；有 → 問後 append（同 §4.3 append 規則；插入的行記於 `baseline/.vendor_kit.toml`，見 §4.3 註）；再跑 = 用引擎重寫薄殼（hash 相符才重寫）；**第一次與修復型都**在第一個寫入前建 `.tmp.install.<id>.toml`（統一規則、無例外；第一次時它同時是「不留半成品」的清除清單，失敗依它移除已寫的檔、`log/` 保留，成功後刪；§4.6、v2.13 P5）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1；v2.9-8；v2.12 L1、L3′；v2.13 P4、P5]</sub> | 根 justfile 已存在 → 6-20「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示；`.dockerignore` 已存在 → 6-34 <sub>[proposal §2；isolation A1(4)；grilling Q22 補]</sub> | 0／1／3 | 印建立或修改了什麼（含加進根 justfile 的那一行、加進 .dockerignore 的四行） |
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分 <sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；**config.toml** 比照初始檔保護模式：hash == `baseline/vendor_kit/config.toml` 副本 → 刪，被下游使用者改過 → 留下並列出（永不刪下游使用者改過的檔）；**`log/` 一律保留**（uninstall 自己也在寫）、不 rmdir `log/`，`.vendor_kit/` 因此保留（只剩 `log/`），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪；進度檔 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12；v2.13 P6；v2.14-6]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的四行同 append 規則問後只刪原文相同的；append 行問後**逐行**比對、只刪仍與紀錄原文相同的行，缺失／被改的行跳過並 warn（不是全有／全無）<sub>[proposal §2、§5；grilling Q22 補；v2.9-5]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留） | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；`--local <v>`：`<v>` 必須是存在的 `.tar` 檔（不收 image tag 形），否則 1 + 6-24（add `--local` 分句）；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`（只收 tar）：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26；v2.10-3]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [--dry-run]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；兩段（resolve→apply、重驗指紋）但不經 docker create/cp <sub>[proposal §2；v2.3 §5；review Claude 原文 3]</sub> | 刪 version.toml 該行、cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行；初始檔永不刪，印清單；進度檔 `.tmp.remove.<id>.toml` <sub>[proposal §2；v2.1 E；grilling 進度日誌]</sub> | append 過的行 → 6-21 問後只刪原文相同的（CRLF/LF 等價）<sub>[proposal §5；grilling Q13]</sub> | 0／1／3 | 初始檔清單 |
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
| 1 | 一般失敗、需人處理／重跑；「工具層動詞回 1 時 version.toml 不動」適用 add／`upgrade <repo>`（寫入前檢查、最後才寫）；remove／uninstall 回 1 時可能已有部分刪除，但進度檔保留、下次可寫動詞先恢復 <sub>[proposal §2；compat 條 4；codex 00–02 #20]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3；所有動詞（含 help／prune）執行紀錄建檔或 `launcher_start`／`engine_start` 寫入失敗 → 1 + 6-38（零寫入）；bootstrap.sh 任一 `-t` 的 add 失敗 → 1 中止 <sub>[v2.3 §2；grilling Q23；v2.12 L4；r9]</sub> |
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
| `uninstall` | 刪（hash 相符） | hash == 基準版副本 → 刪；被改 → 留並列出 | 刪（hash 相符） | 刪自產 | 刪 | 刪自產 | 問後逐行刪原文相同行；初始檔保留 | `.tmp.uninstall.<id>.toml` | 寫；一律保留（不 rmdir） |
| `add` | 最後寫該行 | — | — | 建 baseline/<repo>/ + metadata（`[progress]` → `complete`） | 讀 | 建 cache/<repo>/、gen/<repo>.stamp；重生 tools.just | 初始檔：無 → 建；append 問後加；已存在 → 不納管 | metadata `[progress]` | 寫 |
| `remove` | 刪該行 | — | — | 刪 baseline/<repo>/ | 讀（dev 中 → 1） | 刪 cache/<repo>/、gen/<repo>.stamp；重生 tools.just | append 行問後逐行刪 | `.tmp.remove.<id>.toml` | 寫 |
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
| 兩段編排 | 兩個獨立屬性：**需展開 image**（docker create/cp）= add／upgrade／sync／undev；**兩段**（`resolve <verb>` → 主機 docker → `apply <verb>`，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；**單段** = install／`upgrade vendor_kit`／update／dev／help。`--dry-run` = `apply --dry-run`（也要先拉 image 展開）<sub>[v2.3 §5；v2.2 C；v2.5-10；review 必修 7、Claude 原文 3]</sub> |
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
- **安全字串**（`<kind>`、`<name>`、`<repo>`、`yes|no`、整數）：`[A-Za-z0-9_.-]+`。
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
| 快路徑 | `sync`（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml `vendor_kit` ref；version.toml `[tools]` 每個 `<repo>` 的 ref 之 digest == gen/<repo>.stamp 第一行（或 local 覆寫的 `path:<dir>`）；gen/tools.just 存在；無 `.tmp.<verb>.*.toml`；非 CI 模式。全相符 → 不起容器、0（仍寫執行紀錄：`launcher_start`／`sync_fast_path`／`launcher_exit`，§4.10）；任一不符或 CI 模式 → 起引擎 `resolve sync`。每檔 sha256 verify 只在：CI（CI 模式）、快路徑有差那次（版本變動）、以及 `sync --verify`（長形；F5 已定）做；`sync`（無參數，含工具 `_sync` 自動呼叫）一律快路徑 <sub>[grilling Q22、2026-09-19 末條；v2.7-2]</sub> |
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
| 版本鎖定行契約 | `vendor_kit` 行**唯一正規形**：整行 `vendor_kit = "<ref>"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號基本字串、無尾端註解、LF 結尾；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：`^vendor_kit[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$`（POSIX BRE，不用 `\s`）；命中數必須恰為 1（`grep -c`），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 `[tools]` 之前。禁止：BOM、重複鍵、`[vendor_kit]` 表旁路等 regex 讀不到／讀錯的等價寫法。<sub>[grilling 相容性其餘採納、16 條；review 必修 11]</sub> |
| 公開格式 | 工具可讀它寫來源紀錄。<sub>[grilling deploy 定案]</sub> |

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 是 | 引擎 ref `ghcr.io/<org>/vendor_kit:vN@sha256:<digest>`（多架構 index digest）<sub>[proposal §3；#26]</sub> |
| `schema` | integer | 是 | 啟動器不讀、只引擎讀 <sub>[compat codex 5]</sub> |
| `written_by` | string | 是 | 寫入引擎版本，純資訊 <sub>[review C1]</sub> |
| `[tools].<repo>` | string | 每工具 | `ghcr.io/<org>/<repo>-dist:<tag>@sha256:<digest>`（index digest；`add --local` 亦寫正式 index digest，來自 `.digest` 旁檔）<sub>[proposal §3；grilling Q26]</sub> |

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
| 6-37 | `--local` 值既是存在的檔案也像 image tag（B1 兩者皆成立） | `--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請寫 ./<v>，要指定 image 請寫完整 ref（<host>/<org>/<name>:<tag>）。`（結束 1、零寫入）| 需人處理 | <sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |
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
| B1 | `--local` 值：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立 → 1 + 6-37 消歧；不加前綴語法 | grilling 2026-09-19 末條；v2.7-2 |
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
| L5 | 移植外部 repo 的 log.sh（出處註記）到 POSIX sh；跳脫採 `json_escape_fixed.sh`；argv 完整記錄；trace_id 由啟動器產、`TRACEPARENT` 傳引擎、= 進度檔 id；引擎 `json.dumps`；lnav format 隨 release | v2.12 L5 |



=== 附件 P：本組頁面抽取文字 ===


----- 頁 v1p7bd -----
# v1p7bd  29 流程 v2：upgrade ── D. 回退

nodes 76（不含 v2 小標）／edges 23／terms 14／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── D. 回退 = git revert 該升級 commit（§5、v2.5 §1／§9）
- [note/NOTE] pend: 已定（v2.3 §1）：append 行比對 CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.2 E）：dist/files/ 第一版禁止 symlink。已定（v2.5 §2）：N 讀暫存 /dist/<repo>，materialize 在決定套用之後。自身升級見「E. 自身升級」頁；回退見「D. 回退」頁。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: Renovate（GitHub 上）
- [header/HDR] hdr2: 啟動器（主機 sh）
- [header/HDR] hdr3: 引擎容器
- [header/HDR] hdr4: GHCR
- [header/HDR] hdr5: 專案目錄
- [other/BAND] uD [v2]: D. 回退 ＝ git revert 該升級 commit（version.toml + 初始檔 + baseline 同一 commit）；下次 just 的 sync（resolve → docker → apply，各容器先 engine_start）只把 cache/ 換回舊版
- [end_ok/G12] d0: git revert 該升級 commit
- [step/W12] d1a [v2]: 下次 just（已寫 launcher_start）：docker run 引擎 resolve sync
- [step/SUB] d1ae [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [file/FGRP] d3b: 由 git revert 還原（不是 sync 寫）
- [file/F12] d3b_0: 初始檔
- [file/F12] d3b_1: baseline/<repo>/
- [file/F12] d3b_2: version.toml
- [step/SUB] d2: sync resolve：gen/<repo>.stamp 第一行 ≠ version.toml 鎖定 digest → 待辦「materialize 舊版」
- [decision/D12] d1b [v2]: inspect：舊版本機有？
- [step/W12] d1p [v2]: 無：docker pull
- [other/IMG] d1g: <repo>-dist@digest⏎（version.toml 還原後的舊版）
- [step/W12] d1c: docker create <img> /x
- [step/W12] d1d: docker cp c:/dist/. <tmp>/<repo>/
- [step/W12] d1e: docker rm 該容器
- [step/W12] d1f: docker run … -v <tmp>:/dist:ro 引擎 apply sync
- [step/SUB] d1fe [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] d2c: materialize 舊版：/dist/<repo> 複製到暫存目錄（初始檔與 baseline 不碰）
- [step/SUB] d2c2: 暫存 → cache/<repo>/（原子替換）
- [file/F12] d3: cache/<repo>/（舊版；sync 寫）
- [step/SUB] d2c3: 寫印記 gen/<repo>.stamp（舊版 index digest）
- [file/F12] d3s: gen/<repo>.stamp（舊版；sync 寫）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] d8 [v2]: 0：接著跑原本的 recipe（cache 已是舊版）
- [end_red/R12] d1px [v2]: 1 + 6-24／6-31：pull 失敗／逾時
- [other/LEGEND] p7bd_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bd_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bd_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bd_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bd_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bd_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bd_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bd_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bd_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bd_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p7bd_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p7bd_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p7bd_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p7bd_th: 本頁名詞
- [term/TERM_K] p7bd_tk0: B／D／N
- [term/TERM_V] p7bd_tv0: B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/<repo>，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突
- [term/TERM_K] p7bd_tk1: resolve／apply
- [term/TERM_V] p7bd_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p7bd_tk2: flock／指紋
- [term/TERM_V] p7bd_tv2: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」
- [term/TERM_K] p7bd_tk3: metadata
- [term/TERM_V] p7bd_tv3: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- [term/TERM_K] p7bd_tk4: git merge-file --diff3
- [term/TERM_V] p7bd_tv4: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為結束狀態 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 > 2 > 0，訊息全列
- [term/TERM_K] p7bd_tk5: 回退／git revert
- [term/TERM_V] p7bd_tv5: git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、baseline 同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 只把 cache/<repo>/ 換回舊版（見「D. 回退」頁）
- [term/TERM_K] p7bd_tk6: 印記／declined／declined_hash
- [term/TERM_V] p7bd_tv6: 印記 = gen/<repo>.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）
- [term/TERM_K] p7bd_tk7: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p7bd_tv7: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p7bd_tk8: config.toml（v2.12／v2.13）
- [term/TERM_V] p7bd_tv8: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p7bd_tk9: 6-38
- [term/TERM_V] p7bd_tv9: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bd_tk10: 結束狀態 0／1／2／3
- [term/TERM_V] p7bd_tv10: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p7bd_tk11: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7bd_tv11: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- [term/TERM_K] p7bd_tk12: sync
- [term/TERM_V] p7bd_tv12: 每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑
- [term/TERM_K] p7bd_tk13: Renovate
- [term/TERM_V] p7bd_tv13: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁

## edges
- d1b_n: d1b(inspect：舊版本機有？) --無--> d1p(無：docker pull)
- d1g_p: d1g(<repo>-dist@digest （version.to…) --拉 /dist--> d1p(無：docker pull)
- d1p_x: d1p(無：docker pull) --(無標籤)--> d1c(docker create <img> /x)
- de1: d0(git revert 該升級 commit) --(無標籤)--> d1a(下次 just（已寫 launcher_start）：doc…)
- de1e: d1a(下次 just（已寫 launcher_start）：doc…) --(無標籤)--> d1ae(append engine_start 到同一 log 檔（…)
- de2: d1ae(append engine_start 到同一 log 檔（…) --(無標籤)--> d2(sync resolve：gen/<repo>.stamp …)
- de2b: d2(sync resolve：gen/<repo>.stamp …) --(無標籤)--> d1b(inspect：舊版本機有？)
- de2d: d1c(docker create <img> /x) --(無標籤)--> d1d(docker cp c:/dist/. <tmp>/<rep…)
- de2e: d1d(docker cp c:/dist/. <tmp>/<rep…) --(無標籤)--> d1e(docker rm 該容器)
- de2f: d1e(docker rm 該容器) --(無標籤)--> d1f(docker run … -v <tmp>:/dist:ro…)
- de2h: d1f(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> d1fe(append engine_start 到同一 log 檔（…)
- de2he: d1fe(append engine_start 到同一 log 檔（…) --(無標籤)--> d2c(materialize 舊版：/dist/<repo> 複製…)
- de2i: d2c(materialize 舊版：/dist/<repo> 複製…) --(無標籤)--> d2c2(暫存 → cache/<repo>/（原子替換）)
- de3: d2c2(暫存 → cache/<repo>/（原子替換）) --寫--> d3(cache/<repo>/（舊版；sync 寫）)
- de2j: d2c2(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> d2c3(寫印記 gen/<repo>.stamp（舊版 index …)
- de3s: d2c3(寫印記 gen/<repo>.stamp（舊版 index …) --寫--> d3s(gen/<repo>.stamp（舊版；sync 寫）)
- de4: d0(git revert 該升級 commit) --(無標籤)--> d3b(由 git revert 還原（不是 sync 寫）)
- de2y: d1b(inspect：舊版本機有？) --有--> d1c(docker create <img> /x)
- de2px: d1p(無：docker pull) --失敗--> lp(結束前：log_prune（best-effort）)
- de5: d2c3(寫印記 gen/<repo>.stamp（舊版 index …) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d8(0：接著跑原本的 recipe（cache 已是舊版）)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d1px(1 + 6-24／6-31：pull 失敗／逾時)

## terms
- B／D／N: B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/<repo>，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- flock／指紋: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」
- metadata: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- git merge-file --diff3: git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為結束狀態 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 > 2 > 0，訊息全列
- 回退／git revert: git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、baseline 同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 只把 cache/<repo>/ 換回舊版（見「D. 回退」頁）
- 印記／declined／declined_hash: 印記 = gen/<repo>.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- sync: 每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑
- Renovate: GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁

## xrefs
- pend: 見「E. 自身升級」頁
- pend: 見「D. 回退」頁
- p7bd_tv5: 見「D. 回退」頁
- p7bd_tv13: 見「A. Renovate 路徑」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bc -----
# v1p7bc  30 流程 v2：upgrade ── E. 自身升級 (a)(b)

nodes 83（不含 v2 小標）／edges 34／terms 15／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── E. vendor_kit 自身升級 (a)(b)（v2.2 A／B、v2.3 §2、v2.5 §7、v2.6 §5）
- [note/NOTE] pend: 已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：(a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 啟動器先 pull 新引擎（§3.3 engine 記錄；覆寫時驗 image ID）→ 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎跑 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更；結束 1 = 需要人動作（橙）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] uE [v2]: E. vendor_kit 自身升級：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼（啟動器先 pull 新引擎 → 舊引擎建 .tmp.upgrade 日誌、改第一行 → 新引擎重產後刪日誌）；(b) 別人 pull 後只回 1 提示（sync 頁）；(c) upgrade vendor_kit 見「E(c)」頁
- [end_ok/G12] s0 [v2]: (a) upgrade 不帶 repo（含 vendor_kit 自身）
- [step/W12] s0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] s1 [v2]: docker run 舊引擎 resolve upgrade（全部）
- [step/SUB] s2a0 [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [step/SUB] s2a [v2]: resolve：先完整預檢（dev 中工具、新版新增 <ns>／dest 的全域撞名）
- [decision/D12] s2dq [v2]: 含 dev 中工具？
- [decision/D12] s2q [v2]: 否 → 引擎有新版？
- [other/TEXT] s2n: 否 → 只升工具：每個工具走「B（1）」頁（Q27）
- [decision/D12] s2ln [v2]: 是 → inspect 新引擎：本機有？
- [step/W12] s2lp [v2]: 無：docker pull 新引擎
- [other/IMG] s2gi: vendor_kit:vY⏎（新引擎）
- [decision/D12] s2lv [v2]: 覆寫中且 .Id ≠ 記的 image ID？
- [step/W12] s2r0 [v2]: 否：docker run 舊引擎 apply upgrade
- [step/SUB] s2b0 [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] s2b [v2]: apply（舊引擎）：flock 專案目錄
- [step/SUB] s2c [v2]: 重驗指紋
- [step/SUB] s2d [v2]: 相同 → 建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）
- [file/F12] s2df [v2]: ＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）
- [step/SUB] s2e [v2]: 只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令；日誌留給新引擎）
- [file/F12] s2f: version.toml 第一行 = 新引擎 ref
- [step/W12] s2h [v2]: apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）
- [decision/D12] s2h2 [v2]: 第一行變了且 == 計畫的 engine？
- [step/W12] s2r [v2]: 是：docker run 新引擎 upgrade vendor_kit（同一 TRACEPARENT、同一 log 檔）
- [other/TEXT] s4: → 接「E(c)（1）」頁「docker run 該引擎」格（同一次指令內；接手 §3.4，結束碼原樣傳出）
- [other/TEXT] sb: (b) 別人 pull 後（第一行已變）打任何 just：走「sync（1）」頁 gen/.stamp 比對 → 1 + 6-1「請 upgrade vendor_kit」→ 打 (c)
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_orange/O12] s2dx [v2]: 1：請先 undev dev 中的工具（v2.5 §6）
- [end_orange/O12] s2cx [v2]: 1：指紋不同「請重跑」
- [end_red/R12] s2lx [v2]: 1 + 6-24／6-31：新引擎拉不到／ID 不符（第一行未改）
- [end_red/R12] s2hx [v2]: 1：apply 未改第一行（印 apply 的錯誤）
- [other/LEGEND] p7bc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bc_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bc_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bc_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p7bc_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p7bc_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p7bc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p7bc_th: 本頁名詞
- [term/TERM_K] p7bc_tk0: 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）
- [term/TERM_V] p7bc_tv0: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- [term/TERM_K] p7bc_tk1: resolve／apply
- [term/TERM_V] p7bc_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p7bc_tk2: 6-2b
- [term/TERM_V] p7bc_tv2: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- [term/TERM_K] p7bc_tk3: gen/.stamp
- [term/TERM_V] p7bc_tv3: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p7bc_tk4: gen/tools.just／mod?
- [term/TERM_V] p7bc_tv4: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- [term/TERM_K] p7bc_tk5: GHCR／registry／引擎 image／引擎 ref
- [term/TERM_V] p7bc_tv5: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- [term/TERM_K] p7bc_tk6: image ID／docker image inspect／local 覆寫
- [term/TERM_V] p7bc_tv6: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- [term/TERM_K] p7bc_tk7: metadata
- [term/TERM_V] p7bc_tv7: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- [term/TERM_K] p7bc_tk8: flock／指紋／進度日誌
- [term/TERM_V] p7bc_tv8: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p7bc_tk9: dev 覆寫／undev／多工具彙總（Q27）
- [term/TERM_V] p7bc_tv9: 工具在 version.local.toml 有 path:<dir> 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 > 2 > 0，訊息全列
- [term/TERM_K] p7bc_tk10: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p7bc_tv10: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p7bc_tk11: config.toml（v2.12／v2.13）
- [term/TERM_V] p7bc_tv11: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p7bc_tk12: 6-38
- [term/TERM_V] p7bc_tv12: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bc_tk13: 結束狀態 0／1／2／3
- [term/TERM_V] p7bc_tv13: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p7bc_tk14: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7bc_tv14: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）

## edges
- s2ln_n: s2ln(是 → inspect 新引擎：本機有？) --無--> s2lp(無：docker pull 新引擎)
- s2gi_p: s2gi(vendor_kit:vY （新引擎）) --拉--> s2lp(無：docker pull 新引擎)
- s2lp_x: s2lp(無：docker pull 新引擎) --(無標籤)--> s2lv(覆寫中且 .Id ≠ 記的 image ID？)
- se1: s0((a) upgrade 不帶 repo（含 vendor_k…) --(無標籤)--> s0l(建 log 檔並寫 launcher_start（失敗 → …)
- se1l: s0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> s1(docker run 舊引擎 resolve upgrade…)
- se2: s1(docker run 舊引擎 resolve upgrade…) --(無標籤)--> s2a0(append engine_start 到同一 log 檔（…)
- se2a: s2a0(append engine_start 到同一 log 檔（…) --(無標籤)--> s2a(resolve：先完整預檢（dev 中工具、新版新增 <ns…)
- se2dq: s2a(resolve：先完整預檢（dev 中工具、新版新增 <ns…) --(無標籤)--> s2dq(含 dev 中工具？)
- se2q: s2dq(含 dev 中工具？) --否--> s2q(否 → 引擎有新版？)
- se2n: s2q(否 → 引擎有新版？) --否--> s2n(否 → 只升工具：每個工具走「B（1）」頁（Q27）)
- se3: s2q(否 → 引擎有新版？) --是--> s2ln(是 → inspect 新引擎：本機有？)
- se6vr: s2lv(覆寫中且 .Id ≠ 記的 image ID？) --否--> s2r0(否：docker run 舊引擎 apply upgrade)
- se3b0: s2r0(否：docker run 舊引擎 apply upgrade) --(無標籤)--> s2b0(append engine_start 到同一 log 檔（…)
- se3b: s2b0(append engine_start 到同一 log 檔（…) --(無標籤)--> s2b(apply（舊引擎）：flock 專案目錄)
- se3c: s2b(apply（舊引擎）：flock 專案目錄) --(無標籤)--> s2c(重驗指紋)
- se3d: s2c(重驗指紋) --(無標籤)--> s2d(相同 → 建進度日誌 .tmp.upgrade.<id>.t…)
- se3df: s2d(相同 → 建進度日誌 .tmp.upgrade.<id>.t…) --寫--> s2df(＋.vendor_kit/.tmp.upgrade.<id>…)
- se3e: s2d(相同 → 建進度日誌 .tmp.upgrade.<id>.t…) --(無標籤)--> s2e(只改 version.toml 第一行 → 新引擎 ref（…)
- se4: s2e(只改 version.toml 第一行 → 新引擎 ref（…) --寫--> s2f(version.toml 第一行 = 新引擎 ref)
- se5: s2e(只改 version.toml 第一行 → 新引擎 ref（…) --(無標籤)--> s2h(apply 後再 grep version.toml 第一行…)
- se5h: s2h(apply 後再 grep version.toml 第一行…) --(無標籤)--> s2h2(第一行變了且 == 計畫的 engine？)
- se5l: s2h2(第一行變了且 == 計畫的 engine？) --是--> s2r(是：docker run 新引擎 upgrade vendo…)
- se7: s2r(是：docker run 新引擎 upgrade vendo…) --(無標籤)--> s4(→ 接「E(c)（1）」頁「docker run 該引擎」格…)
- se6y: s2ln(是 → inspect 新引擎：本機有？) --有--> s2lv(覆寫中且 .Id ≠ 記的 image ID？)
- se2dx: s2dq(含 dev 中工具？) --是--> lp(結束前：log_prune（best-effort）)
- se6px: s2lp(無：docker pull 新引擎) --失敗--> lp(結束前：log_prune（best-effort）)
- se6vx: s2lv(覆寫中且 .Id ≠ 記的 image ID？) --是--> lp(結束前：log_prune（best-effort）)
- se3cx: s2c(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- se5x: s2h2(第一行變了且 == 計畫的 engine？) --否--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s2dx(1：請先 undev dev 中的工具（v2.5 §6）)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s2cx(1：指紋不同「請重跑」)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s2lx(1 + 6-24／6-31：新引擎拉不到／ID 不符（第一行…)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s2hx(1：apply 未改第一行（印 apply 的錯誤）)

## terms
- 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- 6-2b: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- GHCR／registry／引擎 image／引擎 ref: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- image ID／docker image inspect／local 覆寫: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- metadata: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- dev 覆寫／undev／多工具彙總（Q27）: 工具在 version.local.toml 有 path:<dir> 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 > 2 > 0，訊息全列
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）

## xrefs
- uE: 見「E(c)」頁
- s2n: 其他「B（1）」頁
- s4: 其他「E(c)（1）」頁
- sb: 其他「sync（1）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bcc -----
# v1p7bcc  31 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）

nodes 86（不含 v2 小標）／edges 33／terms 17／xrefs 6

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）啟動器 → 查 registry → 目標判定（v2.7 §5）
- [note/NOTE] pend: 已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：(a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 啟動器先 pull 新引擎（§3.3 engine 記錄；覆寫時驗 image ID）→ 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎跑 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更；結束 1 = 需要人動作（橙）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] uE2 [v2]: E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → inspect／pull → engine_start → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref？是 → 「E(c)（1′）」頁；否 → 「E(c)（2）」頁
- [end_ok/G12] s10 [v2]: (c) just vendor_kit upgrade vendor_kit[@<tag>]
- [step/W12] s10l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] s11a [v2]: grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）
- [decision/D12] s11n [v2]: docker image inspect：本機有？
- [step/W12] s11p [v2]: 無：docker pull 該引擎
- [other/IMG] s11g: vendor_kit:vN⏎（第一行指到的引擎）
- [decision/D12] s11v [v2]: 覆寫中且 .Id ≠ 記的 image ID？
- [entry/ENTRY] s10a: 來自「E(a)(b)」頁：啟動器已改用新引擎 ref（已寫 launcher_start）
- [step/W12] s11r [v2]: 否：docker run 該引擎 upgrade vendor_kit
- [step/SUB] s12a0 [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不做任何動作）
- [step/SUB] s12a [v2]: flock 專案目錄（60 秒）
- [step/SUB] s12b [v2]: 重驗指紋
- [decision/D12] s12s [v2]: 相同 → 薄殼 == 上次產物？
- [note/NOTE] s12sn [v2]: 「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17；install 頁同）；拿鎖重驗後、任何寫入前檢查，不符 → 1 列差異、零寫入（v2.8 §3）
- [decision/D12] s12d [v2]: 是 → @<tag> 舊版且無法無損讀？
- [decision/D12] s12t [v2]: 否 → 指定 @<tag>？
- [step/SUB] s12tt [v2]: 是：目標 = @<tag>（不查 registry）
- [decision/D12] s12f [v2]: 否 → CI 為真（frozen）？
- [other/TEXT] s12fz: 是：不查 registry、不改第一行 → 續「E(c)（2）」頁
- [step/SUB] s12u [v2]: 否：查 registry（GHCR）取引擎最新正式版 = 目標
- [decision/D12] s12v [v2]: 目標引擎 ref ≠ 現 ref？
- [other/TEXT] s12vz: 否 → 續「E(c)（2）」頁：薄殼比對與重產
- [other/TEXT] s12jz: 是 ↓ 續「E(c)（1′）」頁：建 .tmp.upgrade 日誌 → 改第一行 → 啟動器接手新引擎
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_orange/O12] s12bx [v2]: 1：指紋不同「請重跑」
- [end_orange/O12] s12sx [v2]: 1 + 6-28：薄殼被改過，列差異不動（零寫入）
- [end_orange/O12] s12dx [v2]: 3 + 6-10：無法無損讀現有檔（零寫入）
- [end_red/R12] s11x [v2]: 1：拉不到／image ID 不符（同 tag 重 build）
- [other/LEGEND] p7bcc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bcc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bcc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bcc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bcc_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bcc_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bcc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bcc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bcc_lgx_entry [legend]: 虛線橢圓：跨頁入口
- [other/LEGEND] p7bcc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bcc_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p7bcc_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p7bcc_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p7bcc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p7bcc_th: 本頁名詞
- [term/TERM_K] p7bcc_tk0: 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）
- [term/TERM_V] p7bcc_tv0: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- [term/TERM_K] p7bcc_tk1: resolve／apply
- [term/TERM_V] p7bcc_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p7bcc_tk2: 6-2b
- [term/TERM_V] p7bcc_tv2: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- [term/TERM_K] p7bcc_tk3: 薄殼首行自描述（Q17）／上次產物／相符
- [term/TERM_V] p7bcc_tv3: 薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「== 上次產物」= 首行 hash 與內容相符，被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更
- [term/TERM_K] p7bcc_tk4: gen/.stamp
- [term/TERM_V] p7bcc_tv4: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p7bcc_tk5: gen/tools.just／mod?
- [term/TERM_V] p7bcc_tv5: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- [term/TERM_K] p7bcc_tk6: GHCR／registry／引擎 image／引擎 ref
- [term/TERM_V] p7bcc_tv6: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- [term/TERM_K] p7bcc_tk7: image ID／docker image inspect／local 覆寫
- [term/TERM_V] p7bcc_tv7: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- [term/TERM_K] p7bcc_tk8: metadata
- [term/TERM_V] p7bcc_tv8: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- [term/TERM_K] p7bcc_tk9: flock／指紋／進度日誌
- [term/TERM_V] p7bcc_tv9: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p7bcc_tk10: --protocol P／降版（Q19）／結束碼 3
- [term/TERM_V] p7bcc_tv10: 薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@<舊版>：目標引擎（image LABEL 的 P／schema）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入）；救援路徑永久可用
- [term/TERM_K] p7bcc_tk11: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p7bcc_tv11: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p7bcc_tk12: config.toml（v2.12／v2.13）
- [term/TERM_V] p7bcc_tv12: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p7bcc_tk13: 6-38
- [term/TERM_V] p7bcc_tv13: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bcc_tk14: 結束狀態 0／1／2／3
- [term/TERM_V] p7bcc_tv14: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p7bcc_tk15: 6-24／6-31（pull 失敗）
- [term/TERM_V] p7bcc_tv15: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- [term/TERM_K] p7bcc_tk16: 6-16／6-23／6-28／6-35
- [term/TERM_V] p7bcc_tv16: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## edges
- s11n_n: s11n(docker image inspect：本機有？) --無--> s11p(無：docker pull 該引擎)
- s11g_p: s11g(vendor_kit:vN （第一行指到的引擎）) --拉--> s11p(無：docker pull 該引擎)
- s11p_x: s11p(無：docker pull 該引擎) --(無標籤)--> s11v(覆寫中且 .Id ≠ 記的 image ID？)
- se11: s10((c) just vendor_kit upgrade ve…) --(無標籤)--> s10l(建 log 檔並寫 launcher_start（失敗 → …)
- se11l: s10l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> s11a(grep version.toml 第一行取引擎 ref（l…)
- se11q: s11a(grep version.toml 第一行取引擎 ref（l…) --(無標籤)--> s11n(docker image inspect：本機有？)
- se11vr: s11v(覆寫中且 .Id ≠ 記的 image ID？) --否--> s11r(否：docker run 該引擎 upgrade vendo…)
- se11e: s10a(來自「E(a)(b)」頁：啟動器已改用新引擎 ref（已寫 …) --(無標籤)--> s11r(否：docker run 該引擎 upgrade vendo…)
- se12: s11r(否：docker run 該引擎 upgrade vendo…) --(無標籤)--> s12a0(append engine_start 到同一 log 檔（…)
- se12a: s12a0(append engine_start 到同一 log 檔（…) --(無標籤)--> s12a(flock 專案目錄（60 秒）)
- se12b: s12a(flock 專案目錄（60 秒）) --(無標籤)--> s12b(重驗指紋)
- se12s: s12b(重驗指紋) --(無標籤)--> s12s(相同 → 薄殼 == 上次產物？)
- se12d: s12s(相同 → 薄殼 == 上次產物？) --是--> s12d(是 → @<tag> 舊版且無法無損讀？)
- se12t: s12d(是 → @<tag> 舊版且無法無損讀？) --否--> s12t(否 → 指定 @<tag>？)
- se12tt: s12t(否 → 指定 @<tag>？) --是--> s12tt(是：目標 = @<tag>（不查 registry）)
- se12f: s12t(否 → 指定 @<tag>？) --否--> s12f(否 → CI 為真（frozen）？)
- se12fz: s12f(否 → CI 為真（frozen）？) --是--> s12fz(是：不查 registry、不改第一行 → 續「E(c)（2…)
- se12u: s12f(否 → CI 為真（frozen）？) --否--> s12u(否：查 registry（GHCR）取引擎最新正式版 = 目…)
- se12v: s12u(否：查 registry（GHCR）取引擎最新正式版 = 目…) --(無標籤)--> s12v(目標引擎 ref ≠ 現 ref？)
- se12vn: s12v(目標引擎 ref ≠ 現 ref？) --否--> s12vz(否 → 續「E(c)（2）」頁：薄殼比對與重產)
- se12j: s12v(目標引擎 ref ≠ 現 ref？) --是--> s12jz(是 ↓ 續「E(c)（1′）」頁：建 .tmp.upgrad…)
- se11y: s11n(docker image inspect：本機有？) --有--> s11v(覆寫中且 .Id ≠ 記的 image ID？)
- se12tv: s12tt(是：目標 = @<tag>（不查 registry）) --(無標籤)--> s12v(目標引擎 ref ≠ 現 ref？)
- se11px: s11p(無：docker pull 該引擎) --失敗--> lp(結束前：log_prune（best-effort）)
- se11vx: s11v(覆寫中且 .Id ≠ 記的 image ID？) --是--> lp(結束前：log_prune（best-effort）)
- se12x: s12b(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- se12sx: s12s(相同 → 薄殼 == 上次產物？) --否--> lp(結束前：log_prune（best-effort）)
- se12dx: s12d(是 → @<tag> 舊版且無法無損讀？) --是--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s12bx(1：指紋不同「請重跑」)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s12sx(1 + 6-28：薄殼被改過，列差異不動（零寫入）)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s12dx(3 + 6-10：無法無損讀現有檔（零寫入）)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s11x(1：拉不到／image ID 不符（同 tag 重 buil…)

## terms
- 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- 6-2b: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- 薄殼首行自描述（Q17）／上次產物／相符: 薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「== 上次產物」= 首行 hash 與內容相符，被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- GHCR／registry／引擎 image／引擎 ref: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- image ID／docker image inspect／local 覆寫: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- metadata: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- --protocol P／降版（Q19）／結束碼 3: 薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@<舊版>：目標引擎（image LABEL 的 P／schema）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入）；救援路徑永久可用
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- 6-16／6-23／6-28／6-35: 前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）

## xrefs
- uE2: →「E(c)（1′）」頁
- uE2: →「E(c)（2）」頁
- s10a: 來自「E(a)(b)」頁
- s12fz: 續「E(c)（2）」頁
- s12vz: 續「E(c)（2）」頁
- s12jz: 續「E(c)（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bcx -----
# v1p7bcx  32 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）

nodes 63（不含 v2 小標）／edges 11／terms 14／xrefs 4

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）建日誌 → 改第一行 → 啟動器接手（§3.4、v2.11）
- [note/NOTE] pend: 已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：(a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 啟動器先 pull 新引擎（§3.3 engine 記錄；覆寫時驗 image ID）→ 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎跑 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更；結束 1 = 需要人動作（橙）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] uE2b [v2]: E(c)（1′）目標 ≠ 現 ref（承「E(c)（1）」頁）：建 .tmp.upgrade 日誌 → 只改第一行 → 啟動器 grep 第一行變了 → 用新引擎再跑 upgrade vendor_kit（回「E(c)（1）」頁 docker run 格）
- [entry/ENTRY] s12j0: 來自「E(c)（1）」頁：目標引擎 ref ≠ 現 ref（已拿鎖、重驗；已寫 launcher_start、engine_start）
- [step/SUB] s12j [v2]: 建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）
- [file/F12] s12jf [v2]: ＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）
- [step/SUB] s12w [v2]: 改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動）→ 引擎結束（engine_exit）
- [file/F12] s12wf: version.toml 第一行 = 新引擎 ref（進 git）
- [step/W12] s12h [v2]: 啟動器：apply 後再 grep version.toml 第一行（與 apply 前比；不從 stdout 讀）
- [decision/D12] s12hq [v2]: 第一行變了且 == 計畫的 engine？
- [step/W12] s12hr [v2]: 是：docker run 新引擎 upgrade vendor_kit（同一 TRACEPARENT、append 同一 log 檔）
- [other/TEXT] s12hz: → 續跑：新引擎回到「E(c)（1）」頁「docker run 該引擎」格再跑一次（結束碼原樣傳出，預期 1 + 6-2；第二次第一行又變 → 1 + 6-2b，不再重跑）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_red/R12] s12hx [v2]: 1：第一行未變（引擎未改第一行；印原因，不是 6-2b）
- [other/LEGEND] p7bcx_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bcx_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bcx_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bcx_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bcx_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bcx_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bcx_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bcx_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bcx_lgx_entry [legend]: 虛線橢圓：跨頁入口
- [other/LEGEND] p7bcx_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bcx_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p7bcx_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p7bcx_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p7bcx_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p7bcx_th: 本頁名詞
- [term/TERM_K] p7bcx_tk0: 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）
- [term/TERM_V] p7bcx_tv0: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- [term/TERM_K] p7bcx_tk1: resolve／apply
- [term/TERM_V] p7bcx_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p7bcx_tk2: 6-2b
- [term/TERM_V] p7bcx_tv2: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- [term/TERM_K] p7bcx_tk3: 進度日誌（upgrade vendor_kit；v2.11）
- [term/TERM_V] p7bcx_tv3: upgrade vendor_kit 也建 .tmp.upgrade.<id>.toml（統一規則）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- [term/TERM_K] p7bcx_tk4: gen/.stamp
- [term/TERM_V] p7bcx_tv4: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p7bcx_tk5: gen/tools.just／mod?
- [term/TERM_V] p7bcx_tv5: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- [term/TERM_K] p7bcx_tk6: GHCR／registry／引擎 image／引擎 ref
- [term/TERM_V] p7bcx_tv6: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- [term/TERM_K] p7bcx_tk7: image ID／docker image inspect／local 覆寫
- [term/TERM_V] p7bcx_tv7: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- [term/TERM_K] p7bcx_tk8: metadata
- [term/TERM_V] p7bcx_tv8: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- [term/TERM_K] p7bcx_tk9: flock／指紋／進度日誌
- [term/TERM_V] p7bcx_tv9: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p7bcx_tk10: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p7bcx_tv10: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p7bcx_tk11: config.toml（v2.12／v2.13）
- [term/TERM_V] p7bcx_tv11: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p7bcx_tk12: 6-38
- [term/TERM_V] p7bcx_tv12: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bcx_tk13: 結束狀態 0／1／2／3
- [term/TERM_V] p7bcx_tv13: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- se12je: s12j0(來自「E(c)（1）」頁：目標引擎 ref ≠ 現 ref（…) --(無標籤)--> s12j(建進度日誌 .tmp.upgrade.<id>.toml（記…)
- se12jf: s12j(建進度日誌 .tmp.upgrade.<id>.toml（記…) --寫--> s12jf(＋.vendor_kit/.tmp.upgrade.<id>…)
- se12w: s12j(建進度日誌 .tmp.upgrade.<id>.toml（記…) --(無標籤)--> s12w(改 version.toml 第一行 = 新引擎 ref（單…)
- se12wf: s12w(改 version.toml 第一行 = 新引擎 ref（單…) --寫--> s12wf(version.toml 第一行 = 新引擎 ref（進 g…)
- se12wh: s12w(改 version.toml 第一行 = 新引擎 ref（單…) --(無標籤)--> s12h(啟動器：apply 後再 grep version.toml…)
- se12hq: s12h(啟動器：apply 後再 grep version.toml…) --(無標籤)--> s12hq(第一行變了且 == 計畫的 engine？)
- se12hr: s12hq(第一行變了且 == 計畫的 engine？) --是--> s12hr(是：docker run 新引擎 upgrade vendo…)
- se12hz: s12hr(是：docker run 新引擎 upgrade vendo…) --(無標籤)--> s12hz(→ 續跑：新引擎回到「E(c)（1）」頁「docker ru…)
- se12hx: s12hq(第一行變了且 == 計畫的 engine？) --否--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s12hx(1：第一行未變（引擎未改第一行；印原因，不是 6-2b）)

## terms
- 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- 6-2b: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- 進度日誌（upgrade vendor_kit；v2.11）: upgrade vendor_kit 也建 .tmp.upgrade.<id>.toml（統一規則）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- GHCR／registry／引擎 image／引擎 ref: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- image ID／docker image inspect／local 覆寫: 本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）
- metadata: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs
- uE2b: 其他「E(c)（1）」頁
- uE2b: 回「E(c)（1）」頁
- s12j0: 來自「E(c)（1）」頁
- s12hz: 其他「E(c)（1）」頁

## fills（非圖例）: #FFF4C3 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p7bccc -----
# v1p7bccc  33 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）

nodes 86（不含 v2 小標）／edges 31／terms 15／xrefs 3

## nodes
- [other/TITLE] title: 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）薄殼比對 → 重產（v2.2 A、v2.3 §2、Q17、v2.7 §5）
- [note/NOTE] pend: 已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：(a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 啟動器先 pull 新引擎（§3.3 engine 記錄；覆寫時驗 image ID）→ 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行 → 啟動器 grep 第一行變了 → 用新引擎跑 upgrade vendor_kit；(c) 先查 registry（@<tag>／frozen 不查）→ 有新版／只重產／無變更；結束 1 = 需要人動作（橙）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] uE3 [v2]: E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：第一行未變或已是新 ref）：已是本引擎產物？→ 是 → 0；否 → 無日誌則建 → 重產薄殼五檔 → config.toml 建／三方合併（v2.14-7）→ gen/.stamp → tools.just → 刪 .tmp.upgrade 日誌（v2.11）→ 1
- [entry/ENTRY] s12z0: 來自「E(c)（1）」頁：無新版／不查（第一行未變），或接手續跑（第一行已是新 ref）；已拿鎖、重驗，薄殼 == 上次產物；已寫 launcher_start
- [note/NOTE] s12n [v2]: 「薄殼 == 上次產物」（首行自描述 sha256 與其餘內容相符，Q17）已在「E(c)（1）」頁拿鎖重驗後、任何寫入前驗過（v2.8 §3）；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更（v2.7 §5）
- [decision/D12] s12e [v2]: 首行 engine == 本引擎且 gen/.stamp 相符？
- [decision/D12] s12jq [v2]: 否 → 已有 .tmp.upgrade 日誌（接手續跑中）？
- [step/SUB] s12jn [v2]: 否：建進度日誌 .tmp.upgrade.<id>.toml（第一個寫入前）
- [file/F12] s12jnf [v2]: ＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git）
- [step/SUB] s13 [v2]: 重產薄殼五檔（暫存 → 原子替換）
- [file/FGRP] s13f: 薄殼五檔（進 git）
- [file/F12] s13f_0: .vendor_kit/.gitignore
- [file/F12] s13f_1: .vendor_kit/entry.just
- [file/F12] s13f_2: .vendor_kit/vendor.just
- [file/F12] s13f_3: .vendor_kit/log.sh
- [file/F12] s13f_4: .vendor_kit/ci/check.sh
- [decision/D12] s13gq [v2]: config.toml 存在？
- [step/SUB] s13gn [v2]: 否：建 config.toml（新版範本）
- [step/SUB] s13gy [v2]: 是：三方合併（B = baseline/vendor_kit/config.toml、D = 現況、N = 新版範本；要改先問 6-22，-y 免問）
- [step/SUB] s13gw [v2]: config.toml 原子替換（建或合併的結果）
- [file/F12] s13gf [v2]: config.toml（進 git；三方合併初始檔）
- [step/SUB] s13gb [v2]: baseline/vendor_kit/config.toml 副本推到新版範本
- [file/F12] s13gbf [v2]: baseline/vendor_kit/config.toml（副本；進 git）
- [step/SUB] s13b [v2]: 寫 gen/.stamp（只記本引擎 ref）
- [file/F12] s13bf: gen/.stamp（不進 git）
- [step/SUB] s13c [v2]: 重生 gen/tools.just（用本引擎的規則；mod? 行）
- [file/F12] s13cf: gen/tools.just（不進 git；mod? 行）
- [decision/D12] s13q [v2]: 失敗（任一步）→ 第一行已改（或又變）？
- [step/SUB] s13d [v2]: 成功：刪進度日誌 .tmp.upgrade.<id>.toml（最後一步，由新引擎刪，v2.11）
- [file/F12] s13df [v2]: －.vendor_kit/.tmp.upgrade.<id>.toml（E(a)／E(c)(1) 或本頁建的進度日誌）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] s12z [v2]: 0：無變更（薄殼相符，已是本引擎產物）
- [end_orange/O12] s14 [v2]: 1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令
- [end_red/R12] s13x [v2]: 1 + 6-2b：第一行已改但薄殼重產失敗，請排除錯誤後執行 just vendor_kit upgrade vendor_kit（日誌保留）
- [end_red/R12] s13xn [v2]: 1：第一行未變、重產失敗（印原因；引擎未鎖定新版）
- [other/LEGEND] p7bcd_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p7bcd_lg1 [legend]: 黃：判斷
- [other/LEGEND] p7bcd_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p7bcd_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p7bcd_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p7bcd_lg5 [legend]: 白：步驟
- [other/LEGEND] p7bcd_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p7bcd_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p7bcd_lgx_entry [legend]: 虛線橢圓：跨頁入口
- [other/LEGEND] p7bcd_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p7bcd_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p7bcd_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p7bcd_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p7bcd_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p7bcd_th: 本頁名詞
- [term/TERM_K] p7bcd_tk0: 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）
- [term/TERM_V] p7bcd_tv0: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- [term/TERM_K] p7bcd_tk1: resolve／apply
- [term/TERM_V] p7bcd_tv1: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p7bcd_tk2: 6-2b
- [term/TERM_V] p7bcd_tv2: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- [term/TERM_K] p7bcd_tk3: 進度日誌（upgrade vendor_kit；v2.11）
- [term/TERM_V] p7bcd_tv3: upgrade vendor_kit 也建 .tmp.upgrade.<id>.toml（統一規則）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- [term/TERM_K] p7bcd_tk4: 薄殼首行自描述（Q17）／上次產物／相符
- [term/TERM_V] p7bcd_tv4: 薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「== 上次產物」= 首行 hash 與內容相符，被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更
- [term/TERM_K] p7bcd_tk5: gen/.stamp
- [term/TERM_V] p7bcd_tv5: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- [term/TERM_K] p7bcd_tk6: gen/tools.just／mod?
- [term/TERM_V] p7bcd_tv6: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- [term/TERM_K] p7bcd_tk7: GHCR／registry／引擎 image／引擎 ref
- [term/TERM_V] p7bcd_tv7: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- [term/TERM_K] p7bcd_tk8: metadata
- [term/TERM_V] p7bcd_tv8: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- [term/TERM_K] p7bcd_tk9: flock／指紋／進度日誌
- [term/TERM_V] p7bcd_tv9: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p7bcd_tk10: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p7bcd_tv10: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p7bcd_tk11: config.toml（v2.12／v2.13）
- [term/TERM_V] p7bcd_tv11: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p7bcd_tk12: 6-38
- [term/TERM_V] p7bcd_tv12: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p7bcd_tk13: 結束狀態 0／1／2／3
- [term/TERM_V] p7bcd_tv13: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p7bcd_tk14: 6-22（upgrade 逐檔問句）
- [term/TERM_V] p7bcd_tv14: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問

## edges
- se13: s12z0(來自「E(c)（1）」頁：無新版／不查（第一行未變），或接手…) --(無標籤)--> s12e(首行 engine == 本引擎且 gen/.stamp 相…)
- se15l: s12e(首行 engine == 本引擎且 gen/.stamp 相…) --否--> s12jq(否 → 已有 .tmp.upgrade 日誌（接手續跑中）？)
- se15n: s12jq(否 → 已有 .tmp.upgrade 日誌（接手續跑中）？) --否--> s12jn(否：建進度日誌 .tmp.upgrade.<id>.toml…)
- se15y: s12jq(否 → 已有 .tmp.upgrade 日誌（接手續跑中）？) --是--> s13(重產薄殼五檔（暫存 → 原子替換）)
- se15j: s12jn(否：建進度日誌 .tmp.upgrade.<id>.toml…) --(無標籤)--> s13(重產薄殼五檔（暫存 → 原子替換）)
- se15jf: s12jn(否：建進度日誌 .tmp.upgrade.<id>.toml…) --寫--> s12jnf(＋.vendor_kit/.tmp.upgrade.<id>…)
- se16: s13(重產薄殼五檔（暫存 → 原子替換）) --寫--> s13f(薄殼五檔（進 git）)
- se17: s13(重產薄殼五檔（暫存 → 原子替換）) --(無標籤)--> s13gq(config.toml 存在？)
- se17n: s13gq(config.toml 存在？) --否--> s13gn(否：建 config.toml（新版範本）)
- se17y: s13gq(config.toml 存在？) --是--> s13gy(是：三方合併（B = baseline/vendor_kit…)
- se17w: s13gn(否：建 config.toml（新版範本）) --(無標籤)--> s13gw(config.toml 原子替換（建或合併的結果）)
- se17w2: s13gy(是：三方合併（B = baseline/vendor_kit…) --(無標籤)--> s13gw(config.toml 原子替換（建或合併的結果）)
- se17f: s13gw(config.toml 原子替換（建或合併的結果）) --寫--> s13gf(config.toml（進 git；三方合併初始檔）)
- se17b: s13gw(config.toml 原子替換（建或合併的結果）) --(無標籤)--> s13gb(baseline/vendor_kit/config.tom…)
- se17bf: s13gb(baseline/vendor_kit/config.tom…) --寫--> s13gbf(baseline/vendor_kit/config.tom…)
- se17c: s13gb(baseline/vendor_kit/config.tom…) --(無標籤)--> s13b(寫 gen/.stamp（只記本引擎 ref）)
- se18: s13b(寫 gen/.stamp（只記本引擎 ref）) --寫--> s13bf(gen/.stamp（不進 git）)
- se18b: s13b(寫 gen/.stamp（只記本引擎 ref）) --(無標籤)--> s13c(重生 gen/tools.just（用本引擎的規則；mod?…)
- se18c: s13c(重生 gen/tools.just（用本引擎的規則；mod?…) --寫--> s13cf(gen/tools.just（不進 git；mod? 行）)
- se18cd: s13c(重生 gen/tools.just（用本引擎的規則；mod?…) --(無標籤)--> s13d(成功：刪進度日誌 .tmp.upgrade.<id>.tom…)
- se18df: s13d(成功：刪進度日誌 .tmp.upgrade.<id>.tom…) --刪--> s13df(－.vendor_kit/.tmp.upgrade.<id>…)
- se18x: s13c(重生 gen/tools.just（用本引擎的規則；mod?…) --失敗（任一步）--> s13q(失敗（任一步）→ 第一行已改（或又變）？)
- se15z: s12e(首行 engine == 本引擎且 gen/.stamp 相…) --是--> lp(結束前：log_prune（best-effort）)
- se19: s13q(失敗（任一步）→ 第一行已改（或又變）？) --是--> lp(結束前：log_prune（best-effort）)
- se19n: s13q(失敗（任一步）→ 第一行已改（或又變）？) --否--> lp(結束前：log_prune（best-effort）)
- se18d: s13d(成功：刪進度日誌 .tmp.upgrade.<id>.tom…) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s12z(0：無變更（薄殼相符，已是本引擎產物）)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s14(1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 …)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s13x(1 + 6-2b：第一行已改但薄殼重產失敗，請排除錯誤後執行…)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> s13xn(1：第一行未變、重產失敗（印原因；引擎未鎖定新版）)

## terms
- 自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）: (a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 啟動器先 pull 新引擎（覆寫時驗 ID）→ 舊引擎 apply 只改第一行 → 啟動器 apply 前後 grep 第一行、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@<tag>]：目標 ≠ 現 ref → 建日誌、改第一行、新引擎重產後刪日誌 → 1；無新版 → 薄殼相符 → 0、否則重產 → 1；@舊版無法無損讀 → 3
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- 6-2b: 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）
- 進度日誌（upgrade vendor_kit；v2.11）: upgrade vendor_kit 也建 .tmp.upgrade.<id>.toml（統一規則）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後刪；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 仍 0
- 薄殼首行自描述（Q17）／上次產物／相符: 薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 hash>；「== 上次產物」= 首行 hash 與內容相符，被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更
- gen/.stamp: 只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行
- gen/tools.just／mod?: 不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe
- GHCR／registry／引擎 image／引擎 ref: GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @<tag> 不查）
- metadata: baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-22（upgrade 逐檔問句）: 「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問

## xrefs
- uE3: 其他「E(c)（1）」頁
- s12z0: 來自「E(c)（1）」頁
- s12n: 其他「E(c)（1）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8 -----
# v1p8  34 流程 v2：dev <repo>

nodes 73（不含 v2 小標）／edges 26／terms 13／xrefs 0

## nodes
- [other/TITLE] title: 流程 v2：dev <repo>（§2 dev 列；v2.1 B、v2.2 B、v2.3 §3；<repo> = 工具 repo 名）
- [note/NOTE] pend: 已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/<repo>.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vA [v2]: dev <repo> -p <dir>：工具 path 覆寫（v2.1 B）—— 用本機工具 repo 的 dist/ 取代 image（不進 git；CI 拒絕；工具必須已在 version.toml；單段動詞，不經 docker create/cp）
- [end_ok/G12] d0: just vendor_kit dev <repo> -p <dir>
- [step/W12] d0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [decision/D12] d1q [v2]: <dir>/dist/ 內有 init.toml？
- [step/W12] d1m [v2]: 是：準備掛載 -v <dir>/dist:/dist/<repo>:ro（唯讀）
- [step/W12] d1 [v2]: docker run 引擎 dev <repo> -p <dir>（不經 docker create/cp）
- [step/SUB] d1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不做任何動作）
- [decision/D12] d2a: CI 為真？
- [decision/D12] d2b: 否 → 已接入 <repo>？
- [decision/D12] d2c: 是 → dist 合法？
- [step/SUB] d6a [v2]: 是：flock 專案目錄（60 秒）
- [rule/RULE] d9 [v2]: dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade <repo>／remove <repo> → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋
- [step/SUB] d6 [v2]: 寫 version.local.toml：<repo> = "path:<dir>"（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）
- [file/F12] d6f: ＋version.local.toml（不進 git）：<repo> = "path:<dir>"
- [step/SUB] d7: cache/<repo>/ 改為 symlink → <dir>/dist（本機工具 repo 的 dist/，唯讀）
- [file/F12] d7f: cache/<repo>/ → <dir>/dist（symlink，內容不複製）
- [step/SUB] d7b [v2]: 寫印記 gen/<repo>.stamp 第一行 = path:<dir>（印記不放在 symlink 裡）
- [file/F12] d7bf: gen/<repo>.stamp 第一行：path:<dir>（不進 git）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] d8 [v2]: 0：之後每次 just 用 <dir>
- [end_orange/O12] d1x [v2]: 1：<dir>/dist/init.toml 不存在
- [end_orange/O12] d3a: 1：CI 拒絕 dev（請在本機執行）
- [end_orange/O12] d3b: 1：未接入，請先 add <repo>
- [end_orange/O12] d3c: 1：dist/ 或 init.toml 不合法
- [other/LEGEND] p8_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8_lg5 [legend]: 白：步驟
- [other/LEGEND] p8_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p8_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8_th: 本頁名詞
- [term/TERM_K] p8_tk0: dev／undev
- [term/TERM_V] p8_tv0: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- [term/TERM_K] p8_tk1: 覆寫兩種（v2.1 B）
- [term/TERM_V] p8_tv1: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- [term/TERM_K] p8_tk2: resolve／apply
- [term/TERM_V] p8_tv2: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p8_tk3: version.local.toml
- [term/TERM_V] p8_tv3: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- [term/TERM_K] p8_tk4: symlink／印記／materialize
- [term/TERM_V] p8_tv4: symlink = 指向另一個路徑的捷徑：dev 時 cache/<repo>/ 不放檔案，而是指到 <dir>/dist；印記 gen/<repo>.stamp 在 symlink 外，第一行 path:<dir> 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/<repo>/
- [term/TERM_K] p8_tk5: docker image inspect／掛載 -v
- [term/TERM_V] p8_tv5: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- [term/TERM_K] p8_tk6: 統一提示／gen/.stamp（Q10 (2)）
- [term/TERM_V] p8_tv6: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- [term/TERM_K] p8_tk7: metadata／baseline
- [term/TERM_V] p8_tv7: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- [term/TERM_K] p8_tk8: flock／指紋／進度日誌／CI 為真
- [term/TERM_V] p8_tv8: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- [term/TERM_K] p8_tk9: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8_tv9: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8_tk10: config.toml（v2.12／v2.13）
- [term/TERM_V] p8_tv10: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8_tk11: 6-38
- [term/TERM_V] p8_tv11: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8_tk12: 結束狀態 0／1／2／3
- [term/TERM_V] p8_tv12: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- de1: d0(just vendor_kit dev <repo> -p …) --(無標籤)--> d0l(建 log 檔並寫 launcher_start（失敗 → …)
- de1l: d0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> d1q(<dir>/dist/ 內有 init.toml？)
- de1y: d1q(<dir>/dist/ 內有 init.toml？) --是--> d1m(是：準備掛載 -v <dir>/dist:/dist/<re…)
- de1m: d1m(是：準備掛載 -v <dir>/dist:/dist/<re…) --(無標籤)--> d1(docker run 引擎 dev <repo> -p <d…)
- de2: d1(docker run 引擎 dev <repo> -p <d…) --(無標籤)--> d1e(append engine_start 到同一 log 檔（…)
- de2e: d1e(append engine_start 到同一 log 檔（…) --(無標籤)--> d2a(CI 為真？)
- de4: d2a(CI 為真？) --否--> d2b(否 → 已接入 <repo>？)
- de5: d2b(否 → 已接入 <repo>？) --是--> d2c(是 → dist 合法？)
- de8: d2c(是 → dist 合法？) --是--> d6a(是：flock 專案目錄（60 秒）)
- de8b: d6a(是：flock 專案目錄（60 秒）) --(無標籤)--> d6(寫 version.local.toml：<repo> = …)
- de9: d6(寫 version.local.toml：<repo> = …) --寫--> d6f(＋version.local.toml（不進 git）：<r…)
- de10: d6(寫 version.local.toml：<repo> = …) --(無標籤)--> d7(cache/<repo>/ 改為 symlink → <di…)
- de11: d7(cache/<repo>/ 改為 symlink → <di…) --寫--> d7f(cache/<repo>/ → <dir>/dist（sym…)
- de12: d7(cache/<repo>/ 改為 symlink → <di…) --(無標籤)--> d7b(寫印記 gen/<repo>.stamp 第一行 = pat…)
- de13: d7b(寫印記 gen/<repo>.stamp 第一行 = pat…) --寫--> d7bf(gen/<repo>.stamp 第一行：path:<dir…)
- de1x: d1q(<dir>/dist/ 內有 init.toml？) --否--> lp(結束前：log_prune（best-effort）)
- de3: d2a(CI 為真？) --是--> lp(結束前：log_prune（best-effort）)
- de6: d2b(否 → 已接入 <repo>？) --否--> lp(結束前：log_prune（best-effort）)
- de7: d2c(是 → dist 合法？) --否--> lp(結束前：log_prune（best-effort）)
- de14: d7b(寫印記 gen/<repo>.stamp 第一行 = pat…) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d8(0：之後每次 just 用 <dir>)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d1x(1：<dir>/dist/init.toml 不存在)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d3a(1：CI 拒絕 dev（請在本機執行）)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d3b(1：未接入，請先 add <repo>)
- lxe4: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> d3c(1：dist/ 或 init.toml 不合法)

## terms
- dev／undev: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- 覆寫兩種（v2.1 B）: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- version.local.toml: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- symlink／印記／materialize: symlink = 指向另一個路徑的捷徑：dev 時 cache/<repo>/ 不放檔案，而是指到 <dir>/dist；印記 gen/<repo>.stamp 在 symlink 外，第一行 path:<dir> 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/<repo>/
- docker image inspect／掛載 -v: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- 統一提示／gen/.stamp（Q10 (2)）: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- metadata／baseline: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- flock／指紋／進度日誌／CI 為真: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8ccc -----
# v1p8ccc  35 流程 v2：dev vendor_kit

nodes 75（不含 v2 小標）／edges 28／terms 13／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：dev vendor_kit -i（§2 dev 列；v2.1 B、v2.2 B、v2.6 §1）
- [note/NOTE] pend: 已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/<repo>.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vI [v2]: dev vendor_kit -i <本機 image tag>：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID（由啟動器 docker image inspect 取得後交給引擎，v2.8 §6）；驗收測試用同一機制
- [end_ok/G12] v0: dev vendor_kit -i <本機 image tag>
- [step/W12] v0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] v1i [v2]: docker image inspect <tag> 取 .Id（主機側；tar 請先自己 docker load）
- [decision/D12] v1q [v2]: 本機有此 image？
- [step/W12] v1 [v2]: 是：docker run 引擎 dev vendor_kit -i <tag>，image ID 一併交給引擎（引擎容器內不呼叫 docker）
- [step/SUB] v1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不做任何動作）
- [decision/D12] v2q: CI 為真？
- [step/SUB] v2a [v2]: 否：flock 專案目錄（60 秒）
- [step/SUB] v2b [v2]: 寫 version.local.toml：vendor_kit = "<tag>"（不動薄殼）
- [file/F12] v3: ＋version.local.toml：vendor_kit = "<tag>"（不進 git）
- [step/SUB] v2c [v2]: 寫 version.local.toml：vendor_kit_image_id = 啟動器交來的 image ID
- [file/F12] v3c: version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）
- [other/TEXT] vb: ═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══
- [end_ok/G12] v5: 下次打任何 just
- [step/W12] v6a [v2]: （已寫 launcher_start）grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag
- [decision/D12] v7 [v2]: gen/.stamp 的引擎 ref == 該 tag？
- [decision/D12] v6b [v2]: 是 → docker image inspect <tag> 的 .Id == 記的 image ID？
- [step/W12] v6c [v2]: 是：docker run <tag> resolve sync（不 pull）
- [step/SUB] v6ce [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [other/TEXT] v10: → 正常跑（用該本機 image；「sync（1′）」頁）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] v2z [v2]: 0：之後每次 just 用該本機 image
- [end_orange/O12] v2x [v2]: 1：CI 拒絕 dev（請在本機執行）
- [end_orange/O12] v8 [v2]: 1 + 6-1：vendor_kit 已更新，請執行 just vendor_kit upgrade vendor_kit（「E(c)」頁）
- [end_red/R12] v1x [v2]: 1：本機無此 image（tag 形；tar 請先 docker load）
- [end_red/R12] v6x [v2]: 1：本機 image 已變（同 tag 重 build）或不存在
- [other/LEGEND] p8v_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8v_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8v_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8v_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8v_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8v_lg5 [legend]: 白：步驟
- [other/LEGEND] p8v_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8v_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8v_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8v_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8v_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8v_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8v_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8v_th: 本頁名詞
- [term/TERM_K] p8v_tk0: dev／undev
- [term/TERM_V] p8v_tv0: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- [term/TERM_K] p8v_tk1: 覆寫兩種（v2.1 B）
- [term/TERM_V] p8v_tv1: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- [term/TERM_K] p8v_tk2: resolve／apply
- [term/TERM_V] p8v_tv2: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p8v_tk3: version.local.toml
- [term/TERM_V] p8v_tv3: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- [term/TERM_K] p8v_tk4: image tag／image ID／RepoDigests
- [term/TERM_V] p8v_tv4: tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag
- [term/TERM_K] p8v_tk5: GHCR／tar／docker load
- [term/TERM_V] p8v_tv5: GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i <tag> 指定它
- [term/TERM_K] p8v_tk6: docker image inspect／掛載 -v
- [term/TERM_V] p8v_tv6: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- [term/TERM_K] p8v_tk7: 統一提示／gen/.stamp（Q10 (2)）
- [term/TERM_V] p8v_tv7: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- [term/TERM_K] p8v_tk8: flock／指紋／進度日誌／CI 為真
- [term/TERM_V] p8v_tv8: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- [term/TERM_K] p8v_tk9: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8v_tv9: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8v_tk10: config.toml（v2.12／v2.13）
- [term/TERM_V] p8v_tv10: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8v_tk11: 6-38
- [term/TERM_V] p8v_tv11: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8v_tk12: 結束狀態 0／1／2／3
- [term/TERM_V] p8v_tv12: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- ve1: v0(dev vendor_kit -i <本機 image ta…) --(無標籤)--> v0l(建 log 檔並寫 launcher_start（失敗 → …)
- ve1i: v0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> v1i(docker image inspect <tag> 取 .…)
- ve1q: v1i(docker image inspect <tag> 取 .…) --(無標籤)--> v1q(本機有此 image？)
- ve1y: v1q(本機有此 image？) --是--> v1(是：docker run 引擎 dev vendor_kit…)
- ve2: v1(是：docker run 引擎 dev vendor_kit…) --(無標籤)--> v1e(append engine_start 到同一 log 檔（…)
- ve2e: v1e(append engine_start 到同一 log 檔（…) --(無標籤)--> v2q(CI 為真？)
- ve4: v2q(CI 為真？) --否--> v2a(否：flock 專案目錄（60 秒）)
- ve4b: v2a(否：flock 專案目錄（60 秒）) --(無標籤)--> v2b(寫 version.local.toml：vendor_ki…)
- ve5: v2b(寫 version.local.toml：vendor_ki…) --寫--> v3(＋version.local.toml：vendor_kit…)
- ve5c: v2b(寫 version.local.toml：vendor_ki…) --(無標籤)--> v2c(寫 version.local.toml：vendor_ki…)
- ve5cf: v2c(寫 version.local.toml：vendor_ki…) --寫--> v3c(version.local.toml：＋vendor_kit…)
- ve7: v5(下次打任何 just) --(無標籤)--> v6a(（已寫 launcher_start）grep 引擎 ref…)
- ve8: v6a(（已寫 launcher_start）grep 引擎 ref…) --(無標籤)--> v7(gen/.stamp 的引擎 ref == 該 tag？)
- ve11: v7(gen/.stamp 的引擎 ref == 該 tag？) --是--> v6b(是 → docker image inspect <tag>…)
- ve11c: v6b(是 → docker image inspect <tag>…) --是--> v6c(是：docker run <tag> resolve syn…)
- ve12: v6c(是：docker run <tag> resolve syn…) --(無標籤)--> v6ce(append engine_start 到同一 log 檔（…)
- ve12e: v6ce(append engine_start 到同一 log 檔（…) --(無標籤)--> v10(→ 正常跑（用該本機 image；「sync（1′）」頁）)
- ve1x: v1q(本機有此 image？) --否--> lp(結束前：log_prune（best-effort）)
- ve3: v2q(CI 為真？) --是--> lp(結束前：log_prune（best-effort）)
- ve6: v2c(寫 version.local.toml：vendor_ki…) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- ve9: v7(gen/.stamp 的引擎 ref == 該 tag？) --否--> lp(結束前：log_prune（best-effort）)
- ve11x: v6b(是 → docker image inspect <tag>…) --否--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> v2z(0：之後每次 just 用該本機 image)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> v2x(1：CI 拒絕 dev（請在本機執行）)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> v8(1 + 6-1：vendor_kit 已更新，請執行 jus…)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> v1x(1：本機無此 image（tag 形；tar 請先 dock…)
- lxe4: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> v6x(1：本機 image 已變（同 tag 重 build）或不…)

## terms
- dev／undev: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- 覆寫兩種（v2.1 B）: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- version.local.toml: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- image tag／image ID／RepoDigests: tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag
- GHCR／tar／docker load: GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i <tag> 指定它
- docker image inspect／掛載 -v: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- 統一提示／gen/.stamp（Q10 (2)）: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- flock／指紋／進度日誌／CI 為真: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs
- v10: 其他「sync（1′）」頁
- v8: 其他「E(c)」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8c -----
# v1p8c  36 流程 v2：undev <repo>

nodes 89（不含 v2 小標）／edges 44／terms 14／xrefs 0

## nodes
- [other/TITLE] title: 流程 v2：undev（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §3／§10；<repo> = 工具 repo 名）
- [note/NOTE] pend: 已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/<repo>.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vB [v2]: undev <repo>：回到 version.toml 鎖定版 = resolve → docker → apply（要重新 materialize，v2.3 §5；建日誌後才動，v2.5 §10；失敗 → 1 保留可恢復狀態，v2.2 B）
- [end_ok/G12] u0: just vendor_kit undev <repo>
- [step/W12] u0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] u1 [v2]: docker run 引擎 resolve undev <repo>
- [step/SUB] u1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [decision/D12] u2: 有 path 覆寫？
- [step/SUB] u4 [v2]: 是：resolve（不寫）：計畫 = 拉 <repo>-dist@digest（鎖定版）、重新 materialize
- [step/SUB] u4b [v2]: stdout vk-resolve/1：計畫＋指紋回啟動器
- [decision/D12] u5a [v2]: docker image inspect：本機有？
- [step/W12] u5p [v2]: 無：docker pull
- [other/IMG] u5g: <repo>-dist@digest（鎖定版）
- [step/W12] u5b [v2]: docker create <img> /x
- [step/W12] u5c [v2]: docker cp c:/dist/. <tmp>/<repo>/（主機暫存）
- [step/W12] u5d [v2]: docker rm 該容器
- [step/W12] u5r [v2]: docker run … -v <tmp>:/dist:ro 引擎 apply undev <repo>
- [step/SUB] u5re [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] u6a [v2]: apply：flock 專案目錄（60 秒）
- [step/SUB] u6b [v2]: 重驗指紋
- [step/SUB] u6l [v2]: 相同 → 建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）
- [file/F12] u6lf: ＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）
- [step/SUB] u6c [v2]: 刪 version.local.toml 該行（<repo> = "path:<dir>"）
- [file/F12] u6cf: version.local.toml（少一行）
- [decision/D12] u6ce [v2]: 還有其他覆寫行？
- [step/SUB] u6ced [v2]: 否：刪整個 version.local.toml（最後一個覆寫已撤）
- [file/F12] u6cedf [v2]: －version.local.toml（整個檔）
- [step/SUB] u6d [v2]: 是／已刪：拆掉 cache/<repo>/ 的 symlink
- [file/F12] u6df: cache/<repo>/（不再是 symlink）
- [step/SUB] u6e [v2]: materialize 鎖定版：/dist/<repo> 展開到暫存目錄
- [step/SUB] u6e2 [v2]: 暫存 → cache/<repo>/（原子替換）
- [file/F12] u6ef: cache/<repo>/（重新展開）
- [step/SUB] u6f [v2]: 寫 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）
- [file/F12] u6ff: gen/<repo>.stamp（第一行 index digest）
- [step/SUB] u6g [v2]: 成功：刪進度日誌（最後一步）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] u7: 0：已回到鎖定版
- [end_ok/G12] u3: 0：未啟用 dev（提示）
- [end_orange/O12] u6bx [v2]: 1：指紋不同「請重跑」
- [end_red/R12] u5px [v2]: 1 + 6-24／6-31：pull 失敗／逾時
- [end_red/R12] u6x [v2]: 1：失敗（任一步）→ 保留可恢復狀態（下次可寫動詞先恢復；sync／update 印 6-33）
- [other/LEGEND] p8c_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8c_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8c_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8c_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8c_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8c_lg5 [legend]: 白：步驟
- [other/LEGEND] p8c_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8c_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8c_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8c_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8c_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8c_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8c_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8c_th: 本頁名詞
- [term/TERM_K] p8c_tk0: dev／undev
- [term/TERM_V] p8c_tv0: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- [term/TERM_K] p8c_tk1: 覆寫兩種（v2.1 B）
- [term/TERM_V] p8c_tv1: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- [term/TERM_K] p8c_tk2: resolve／apply
- [term/TERM_V] p8c_tv2: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p8c_tk3: version.local.toml
- [term/TERM_V] p8c_tv3: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- [term/TERM_K] p8c_tk4: symlink／印記／materialize
- [term/TERM_V] p8c_tv4: symlink = 指向另一個路徑的捷徑：dev 時 cache/<repo>/ 不放檔案，而是指到 <dir>/dist；印記 gen/<repo>.stamp 在 symlink 外，第一行 path:<dir> 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/<repo>/
- [term/TERM_K] p8c_tk5: docker image inspect／掛載 -v
- [term/TERM_V] p8c_tv5: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- [term/TERM_K] p8c_tk6: metadata／baseline
- [term/TERM_V] p8c_tv6: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- [term/TERM_K] p8c_tk7: flock／指紋／進度日誌／CI 為真
- [term/TERM_V] p8c_tv7: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- [term/TERM_K] p8c_tk8: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8c_tv8: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8c_tk9: config.toml（v2.12／v2.13）
- [term/TERM_V] p8c_tv9: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8c_tk10: 6-38
- [term/TERM_V] p8c_tv10: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8c_tk11: 結束狀態 0／1／2／3
- [term/TERM_V] p8c_tv11: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p8c_tk12: 6-24／6-31（pull 失敗）
- [term/TERM_V] p8c_tv12: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- [term/TERM_K] p8c_tk13: 6-33（未完成交易）
- [term/TERM_V] p8c_tv13: 唯讀動詞偵測到 .tmp.<verb>.<id>.toml：「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」；sync／update 印後結束 1、不恢復；help 印後仍 0；可寫動詞不印此句而是先恢復

## edges
- u5a_n: u5a(docker image inspect：本機有？) --無--> u5p(無：docker pull)
- u5g_p: u5g(<repo>-dist@digest（鎖定版）) --拉 /dist--> u5p(無：docker pull)
- u5p_x: u5p(無：docker pull) --(無標籤)--> u5b(docker create <img> /x)
- ue1: u0(just vendor_kit undev <repo>) --(無標籤)--> u0l(建 log 檔並寫 launcher_start（失敗 → …)
- ue1l: u0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> u1(docker run 引擎 resolve undev <r…)
- ue1e: u1(docker run 引擎 resolve undev <r…) --(無標籤)--> u1e(append engine_start 到同一 log 檔（…)
- ue2: u1e(append engine_start 到同一 log 檔（…) --(無標籤)--> u2(有 path 覆寫？)
- ue4: u2(有 path 覆寫？) --是--> u4(是：resolve（不寫）：計畫 = 拉 <repo>-di…)
- ue4b: u4(是：resolve（不寫）：計畫 = 拉 <repo>-di…) --(無標籤)--> u4b(stdout vk-resolve/1：計畫＋指紋回啟動器)
- ue5: u4b(stdout vk-resolve/1：計畫＋指紋回啟動器) --(無標籤)--> u5a(docker image inspect：本機有？)
- ue5c: u5b(docker create <img> /x) --(無標籤)--> u5c(docker cp c:/dist/. <tmp>/<rep…)
- ue5d: u5c(docker cp c:/dist/. <tmp>/<rep…) --(無標籤)--> u5d(docker rm 該容器)
- ue7: u5d(docker rm 該容器) --(無標籤)--> u5r(docker run … -v <tmp>:/dist:ro…)
- ue8: u5r(docker run … -v <tmp>:/dist:ro…) --(無標籤)--> u5re(append engine_start 到同一 log 檔（…)
- ue8e: u5re(append engine_start 到同一 log 檔（…) --(無標籤)--> u6a(apply：flock 專案目錄（60 秒）)
- ue8b: u6a(apply：flock 專案目錄（60 秒）) --(無標籤)--> u6b(重驗指紋)
- ue9: u6b(重驗指紋) --(無標籤)--> u6l(相同 → 建進度日誌（.vendor_kit/.tmp.un…)
- ue9f: u6l(相同 → 建進度日誌（.vendor_kit/.tmp.un…) --寫--> u6lf(＋.vendor_kit/.tmp.undev.<id>.t…)
- ue10: u6l(相同 → 建進度日誌（.vendor_kit/.tmp.un…) --(無標籤)--> u6c(刪 version.local.toml 該行（<repo>…)
- ue10f: u6c(刪 version.local.toml 該行（<repo>…) --寫--> u6cf(version.local.toml（少一行）)
- ue10e: u6c(刪 version.local.toml 該行（<repo>…) --(無標籤)--> u6ce(還有其他覆寫行？)
- ue10ed: u6ce(還有其他覆寫行？) --否--> u6ced(否：刪整個 version.local.toml（最後一個覆…)
- ue10edf: u6ced(否：刪整個 version.local.toml（最後一個覆…) --刪--> u6cedf(－version.local.toml（整個檔）)
- ue11: u6ce(還有其他覆寫行？) --是--> u6d(是／已刪：拆掉 cache/<repo>/ 的 symlin…)
- ue11d: u6ced(否：刪整個 version.local.toml（最後一個覆…) --(無標籤)--> u6d(是／已刪：拆掉 cache/<repo>/ 的 symlin…)
- ue11f: u6d(是／已刪：拆掉 cache/<repo>/ 的 symlin…) --寫--> u6df(cache/<repo>/（不再是 symlink）)
- ue12: u6d(是／已刪：拆掉 cache/<repo>/ 的 symlin…) --(無標籤)--> u6e(materialize 鎖定版：/dist/<repo> 展…)
- ue12b: u6e(materialize 鎖定版：/dist/<repo> 展…) --(無標籤)--> u6e2(暫存 → cache/<repo>/（原子替換）)
- ue12f: u6e2(暫存 → cache/<repo>/（原子替換）) --寫--> u6ef(cache/<repo>/（重新展開）)
- ue13: u6e2(暫存 → cache/<repo>/（原子替換）) --(無標籤)--> u6f(寫 gen/<repo>.stamp（第一行 index d…)
- ue13f: u6f(寫 gen/<repo>.stamp（第一行 index d…) --寫--> u6ff(gen/<repo>.stamp（第一行 index dig…)
- ue14: u6f(寫 gen/<repo>.stamp（第一行 index d…) --(無標籤)--> u6g(成功：刪進度日誌（最後一步）)
- ue5y: u5a(docker image inspect：本機有？) --有--> u5b(docker create <img> /x)
- ue3: u2(有 path 覆寫？) --否--> lp(結束前：log_prune（best-effort）)
- ue5px: u5p(無：docker pull) --失敗--> lp(結束前：log_prune（best-effort）)
- ue8x: u6b(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- ue14x: u6f(寫 gen/<repo>.stamp（第一行 index d…) --失敗（任一步）--> lp(結束前：log_prune（best-effort）)
- ue15: u6g(成功：刪進度日誌（最後一步）) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> u7(0：已回到鎖定版)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> u3(0：未啟用 dev（提示）)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> u6bx(1：指紋不同「請重跑」)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> u5px(1 + 6-24／6-31：pull 失敗／逾時)
- lxe4: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> u6x(1：失敗（任一步）→ 保留可恢復狀態（下次可寫動詞先恢復；s…)

## terms
- dev／undev: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- 覆寫兩種（v2.1 B）: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- version.local.toml: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- symlink／印記／materialize: symlink = 指向另一個路徑的捷徑：dev 時 cache/<repo>/ 不放檔案，而是指到 <dir>/dist；印記 gen/<repo>.stamp 在 symlink 外，第一行 path:<dir> 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/<repo>/
- docker image inspect／掛載 -v: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- metadata／baseline: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- flock／指紋／進度日誌／CI 為真: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）
- 6-33（未完成交易）: 唯讀動詞偵測到 .tmp.<verb>.<id>.toml：「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」；sync／update 印後結束 1、不恢復；help 印後仍 0；可寫動詞不印此句而是先恢復

## xrefs

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8cc -----
# v1p8cc  37 流程 v2：undev vendor_kit

nodes 85（不含 v2 小標）／edges 41／terms 13／xrefs 1

## nodes
- [other/TITLE] title: 流程 v2：undev vendor_kit（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §10、v2.6 §1、v2.7 §6；Q10 (2)）
- [note/NOTE] pend: 已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/<repo>.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vB′ [v2]: undev vendor_kit = resolve → apply（無 image 要拉）：建 .tmp.undev.<id>.toml 日誌後才撤 vendor_kit 行（含 image ID）；最後一個覆寫撤掉 → 刪整個 version.local.toml；下次 just：gen/.stamp 不符 → 只回 1 提示（Q10 (2)）
- [end_ok/G12] w0: just vendor_kit undev vendor_kit
- [step/W12] w0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] w1 [v2]: docker run 引擎 resolve undev vendor_kit
- [step/SUB] w1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [decision/D12] w2q [v2]: version.local.toml 有 vendor_kit 行？
- [step/SUB] w2s [v2]: 是：resolve（不寫）：計畫 = 撤 vendor_kit 行（無 image 要拉）
- [step/SUB] w2s2 [v2]: stdout vk-resolve/1：計畫＋指紋（version.local.toml hash）回啟動器
- [step/W12] w1b [v2]: docker run 引擎 apply undev vendor_kit
- [step/SUB] w1be [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] w2a [v2]: apply：flock 專案目錄（60 秒）
- [step/SUB] w2b [v2]: 重驗指紋
- [step/SUB] w2l [v2]: 相同 → 建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）
- [file/F12] w2lf: ＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）
- [step/SUB] w2 [v2]: 刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）
- [file/F12] w2f: version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）
- [decision/D12] w2e [v2]: 還有其他覆寫行？
- [step/SUB] w2ed [v2]: 否：刪整個 version.local.toml（最後一個覆寫已撤）
- [file/F12] w2edf [v2]: －version.local.toml（整個檔）
- [step/SUB] w2g [v2]: 是／已刪：刪進度日誌（最後一步）
- [other/TEXT] wb: ═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══
- [end_ok/G12] w4: 下次打任何 just
- [step/W12] w5a [v2]: （已寫 launcher_start）grep version.toml 第一行取引擎 ref（local 已無覆寫）
- [decision/D12] w6 [v2]: gen/.stamp 的引擎 ref == 第一行？
- [decision/D12] w5b [v2]: 是 → docker image inspect：本機有？
- [step/W12] w5p [v2]: 無：docker pull 該引擎
- [other/IMG] w5g: vendor_kit:vN（version.toml 的引擎）
- [step/W12] w5c [v2]: docker run 該引擎 resolve sync
- [step/SUB] w5ce [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [other/TEXT] w9: → 正常跑（「sync（1′）」頁）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] w2z [v2]: 0：本次結束（下次 just 用 version.toml 的引擎）
- [end_ok/G12] w3: 0：未啟用（提示）
- [end_orange/O12] w2bx [v2]: 1：指紋不同「請重跑」
- [end_orange/O12] w7 [v2]: 1 + 6-1：vendor_kit 已更新，請執行 just vendor_kit upgrade vendor_kit（不重寫）
- [end_red/R12] w2x [v2]: 1：失敗 → 保留可恢復狀態（下次可寫動詞先恢復）
- [end_red/R12] w5px [v2]: 1 + 6-24／6-31：pull 失敗／逾時
- [other/LEGEND] p8cc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8cc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8cc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8cc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8cc_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8cc_lg5 [legend]: 白：步驟
- [other/LEGEND] p8cc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8cc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8cc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8cc_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8cc_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8cc_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8cc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8cc_th: 本頁名詞
- [term/TERM_K] p8cc_tk0: dev／undev
- [term/TERM_V] p8cc_tv0: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- [term/TERM_K] p8cc_tk1: 覆寫兩種（v2.1 B）
- [term/TERM_V] p8cc_tv1: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- [term/TERM_K] p8cc_tk2: resolve／apply
- [term/TERM_V] p8cc_tv2: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- [term/TERM_K] p8cc_tk3: version.local.toml
- [term/TERM_V] p8cc_tv3: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- [term/TERM_K] p8cc_tk4: docker image inspect／掛載 -v
- [term/TERM_V] p8cc_tv4: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- [term/TERM_K] p8cc_tk5: 統一提示／gen/.stamp（Q10 (2)）
- [term/TERM_V] p8cc_tv5: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- [term/TERM_K] p8cc_tk6: metadata／baseline
- [term/TERM_V] p8cc_tv6: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- [term/TERM_K] p8cc_tk7: flock／指紋／進度日誌／CI 為真
- [term/TERM_V] p8cc_tv7: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- [term/TERM_K] p8cc_tk8: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8cc_tv8: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8cc_tk9: config.toml（v2.12／v2.13）
- [term/TERM_V] p8cc_tv9: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8cc_tk10: 6-38
- [term/TERM_V] p8cc_tv10: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8cc_tk11: 結束狀態 0／1／2／3
- [term/TERM_V] p8cc_tv11: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- [term/TERM_K] p8cc_tk12: 6-24／6-31（pull 失敗）
- [term/TERM_V] p8cc_tv12: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）

## edges
- w5b_n: w5b(是 → docker image inspect：本機有？) --無--> w5p(無：docker pull 該引擎)
- w5g_p: w5g(vendor_kit:vN（version.toml 的引擎…) --拉--> w5p(無：docker pull 該引擎)
- w5p_x: w5p(無：docker pull 該引擎) --(無標籤)--> w5c(docker run 該引擎 resolve sync)
- we1: w0(just vendor_kit undev vendor_k…) --(無標籤)--> w0l(建 log 檔並寫 launcher_start（失敗 → …)
- we1l: w0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> w1(docker run 引擎 resolve undev ve…)
- we1e: w1(docker run 引擎 resolve undev ve…) --(無標籤)--> w1e(append engine_start 到同一 log 檔（…)
- we2: w1e(append engine_start 到同一 log 檔（…) --(無標籤)--> w2q(version.local.toml 有 vendor_ki…)
- we2y: w2q(version.local.toml 有 vendor_ki…) --是--> w2s(是：resolve（不寫）：計畫 = 撤 vendor_ki…)
- we2s2: w2s(是：resolve（不寫）：計畫 = 撤 vendor_ki…) --(無標籤)--> w2s2(stdout vk-resolve/1：計畫＋指紋（vers…)
- we2s: w2s2(stdout vk-resolve/1：計畫＋指紋（vers…) --(無標籤)--> w1b(docker run 引擎 apply undev vend…)
- we2a: w1b(docker run 引擎 apply undev vend…) --(無標籤)--> w1be(append engine_start 到同一 log 檔（…)
- we2ae: w1be(append engine_start 到同一 log 檔（…) --(無標籤)--> w2a(apply：flock 專案目錄（60 秒）)
- we2b: w2a(apply：flock 專案目錄（60 秒）) --(無標籤)--> w2b(重驗指紋)
- we2l: w2b(重驗指紋) --(無標籤)--> w2l(相同 → 建進度日誌（.vendor_kit/.tmp.un…)
- we2lf: w2l(相同 → 建進度日誌（.vendor_kit/.tmp.un…) --寫--> w2lf(＋.vendor_kit/.tmp.undev.<id>.t…)
- we2w: w2l(相同 → 建進度日誌（.vendor_kit/.tmp.un…) --(無標籤)--> w2(刪 version.local.toml 的 vendor_…)
- we3: w2(刪 version.local.toml 的 vendor_…) --寫--> w2f(version.local.toml（少 vendor_ki…)
- we2e: w2(刪 version.local.toml 的 vendor_…) --(無標籤)--> w2e(還有其他覆寫行？)
- we2ed: w2e(還有其他覆寫行？) --否--> w2ed(否：刪整個 version.local.toml（最後一個覆…)
- we2edf: w2ed(否：刪整個 version.local.toml（最後一個覆…) --刪--> w2edf(－version.local.toml（整個檔）)
- we2g: w2e(還有其他覆寫行？) --是--> w2g(是／已刪：刪進度日誌（最後一步）)
- we2gd: w2ed(否：刪整個 version.local.toml（最後一個覆…) --(無標籤)--> w2g(是／已刪：刪進度日誌（最後一步）)
- we5: w4(下次打任何 just) --(無標籤)--> w5a(（已寫 launcher_start）grep versio…)
- we6: w5a(（已寫 launcher_start）grep versio…) --(無標籤)--> w6(gen/.stamp 的引擎 ref == 第一行？)
- we8: w6(gen/.stamp 的引擎 ref == 第一行？) --是--> w5b(是 → docker image inspect：本機有？)
- we10: w5c(docker run 該引擎 resolve sync) --(無標籤)--> w5ce(append engine_start 到同一 log 檔（…)
- we10e: w5ce(append engine_start 到同一 log 檔（…) --(無標籤)--> w9(→ 正常跑（「sync（1′）」頁）)
- we8y: w5b(是 → docker image inspect：本機有？) --有--> w5c(docker run 該引擎 resolve sync)
- we2n: w2q(version.local.toml 有 vendor_ki…) --否--> lp(結束前：log_prune（best-effort）)
- we2bx: w2b(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- we3x: w2(刪 version.local.toml 的 vendor_…) --失敗--> lp(結束前：log_prune（best-effort）)
- we4: w2g(是／已刪：刪進度日誌（最後一步）) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- we7: w6(gen/.stamp 的引擎 ref == 第一行？) --否--> lp(結束前：log_prune（best-effort）)
- we8px: w5p(無：docker pull 該引擎) --失敗--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w2z(0：本次結束（下次 just 用 version.toml …)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w3(0：未啟用（提示）)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w2bx(1：指紋不同「請重跑」)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w7(1 + 6-1：vendor_kit 已更新，請執行 jus…)
- lxe4: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w2x(1：失敗 → 保留可恢復狀態（下次可寫動詞先恢復）)
- lxe5: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> w5px(1 + 6-24／6-31：pull 失敗／逾時)

## terms
- dev／undev: 用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image
- 覆寫兩種（v2.1 B）: 工具 path 覆寫 <repo> = "path:<dir>"：cache/<repo>/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = "<tag>"＋image ID：啟動器改用該本機 image
- resolve／apply: 動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④
- version.local.toml: 同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = "path:<dir>" 或 vendor_kit = "<tag>" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1
- docker image inspect／掛載 -v: 啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器
- 統一提示／gen/.stamp（Q10 (2)）: gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼
- metadata／baseline: baseline/<repo>/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）
- flock／指紋／進度日誌／CI 為真: flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.<id>.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）
- 6-24／6-31（pull 失敗）: docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）

## xrefs
- w9: 其他「sync（1′）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8b -----
# v1p8b  38 流程 v2：remove（1）resolve → apply 前置

nodes 75（不含 v2 小標）／edges 28／terms 14／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：remove（1）resolve → apply 前置（§2、§5；v2.2 C／E、v2.3 §5、v2.5 §3／§11）
- [note/NOTE] pend: 已定（v2.3 §1、v2.5 §11、v2.9 §5）：remove／uninstall 只刪原文相同的 append 行，逐行比對 CRLF／LF 視為相同、其餘精確；仍相同 → 刪該行、缺失／被改 → 跳過並 warn（不是全有／全無）。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vC [v2]: remove <repo>（1）：拆掉一個工具（初始檔永不刪、印清單，要刪用 git rm）= resolve（讀 metadata → 刪除清單 → 詢問清單 → 指紋 → stdout）→ apply 前置（拿鎖、重驗、frozen、dry-run）；無 image 要拉；寫入段見「remove（2）」頁
- [end_ok/G12] m0: just vendor_kit remove <repo>（-y、--dry-run）
- [step/W12] m0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] m1 [v2]: docker run <引擎> resolve remove <repo>（不經 docker create/cp）
- [step/SUB] m1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [decision/D12] m2: 已接入 <repo>？
- [decision/D12] m4: 是 → 有 dev path 覆寫？
- [step/SUB] m6 [v2]: 否：resolve（不寫）：讀 metadata（append 過的行、完成標記）
- [step/SUB] m6b [v2]: 產生刪除清單：version.toml 行、cache/<repo>/、gen/<repo>.stamp、baseline/<repo>/、gen/tools.just 的 mod? 行
- [step/SUB] m6c [v2]: 產生詢問清單：metadata 記的 append 行（有才問）
- [step/SUB] m6d [v2]: 產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）
- [step/SUB] m6d2 [v2]: stdout vk-resolve/1：計畫＋指紋回啟動器
- [step/W12] m8 [v2]: docker run <引擎> apply remove <repo>（--dry-run 原樣轉發）
- [step/SUB] m8e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] m9a [v2]: apply：flock 專案目錄（60 秒）
- [step/SUB] m9b [v2]: 重驗指紋
- [decision/D12] m7c [v2]: 相同 → CI 為真（frozen）且需改 tracked 檔？
- [decision/D12] m7: 否 → --dry-run？
- [other/TEXT] m7z: 否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] m7y [v2]: 0：只印清單（會刪什麼、會問什麼）
- [end_ok/G12] m3: 0：未接入（提示）
- [end_orange/O12] m5: 1：請先 undev <repo>（v2.1 B）
- [end_orange/O12] m9x [v2]: 1：指紋不同「請重跑」
- [end_orange/O12] m7cx [v2]: 1：印需改清單（frozen；請在本機執行後 commit 並 push）
- [other/LEGEND] p8b_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8b_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8b_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8b_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8b_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8b_lg5 [legend]: 白：步驟
- [other/LEGEND] p8b_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8b_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8b_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8b_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8b_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8b_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8b_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8b_th: 本頁名詞
- [term/TERM_K] p8b_tk0: remove
- [term/TERM_V] p8b_tv0: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- [term/TERM_K] p8b_tk1: uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）
- [term/TERM_V] p8b_tv1: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- [term/TERM_K] p8b_tk2: resolve／apply／--dry-run
- [term/TERM_V] p8b_tv2: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- [term/TERM_K] p8b_tk3: flock／指紋／進度日誌
- [term/TERM_V] p8b_tv3: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p8b_tk4: baseline／metadata
- [term/TERM_V] p8b_tv4: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- [term/TERM_K] p8b_tk5: append 行／CRLF／逐行比對
- [term/TERM_V] p8b_tv5: add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後逐行比對（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）：仍與紀錄原文相同的行 → 刪；缺失／被改的行 → 跳過並 warn（不是全有／全無；§4.3、v2.9 §5）
- [term/TERM_K] p8b_tk6: 初始檔
- [term/TERM_V] p8b_tv6: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- [term/TERM_K] p8b_tk7: dev 覆寫
- [term/TERM_V] p8b_tv7: version.local.toml 的 <repo> = "path:<dir>"；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋
- [term/TERM_K] p8b_tk8: gen／mod?／import
- [term/TERM_V] p8b_tv8: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- [term/TERM_K] p8b_tk9: CI 為真／frozen
- [term/TERM_V] p8b_tv9: CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）
- [term/TERM_K] p8b_tk10: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8b_tv10: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8b_tk11: config.toml（v2.12／v2.13）
- [term/TERM_V] p8b_tv11: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8b_tk12: 6-38
- [term/TERM_V] p8b_tv12: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8b_tk13: 結束狀態 0／1／2／3
- [term/TERM_V] p8b_tv13: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- me1: m0(just vendor_kit remove <repo>（…) --(無標籤)--> m0l(建 log 檔並寫 launcher_start（失敗 → …)
- me1l: m0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> m1(docker run <引擎> resolve remove…)
- me1e: m1(docker run <引擎> resolve remove…) --(無標籤)--> m1e(append engine_start 到同一 log 檔（…)
- me2: m1e(append engine_start 到同一 log 檔（…) --(無標籤)--> m2(已接入 <repo>？)
- me4: m2(已接入 <repo>？) --是--> m4(是 → 有 dev path 覆寫？)
- me6: m4(是 → 有 dev path 覆寫？) --否--> m6(否：resolve（不寫）：讀 metadata（appen…)
- me6b: m6(否：resolve（不寫）：讀 metadata（appen…) --(無標籤)--> m6b(產生刪除清單：version.toml 行、cache/<r…)
- me6c: m6b(產生刪除清單：version.toml 行、cache/<r…) --(無標籤)--> m6c(產生詢問清單：metadata 記的 append 行（有才…)
- me6d: m6c(產生詢問清單：metadata 記的 append 行（有才…) --(無標籤)--> m6d(產生輸入指紋（version.toml、metadata、要…)
- me6d2: m6d(產生輸入指紋（version.toml、metadata、要…) --(無標籤)--> m6d2(stdout vk-resolve/1：計畫＋指紋回啟動器)
- me7: m6d2(stdout vk-resolve/1：計畫＋指紋回啟動器) --(無標籤)--> m8(docker run <引擎> apply remove <…)
- me8: m8(docker run <引擎> apply remove <…) --(無標籤)--> m8e(append engine_start 到同一 log 檔（…)
- me8e: m8e(append engine_start 到同一 log 檔（…) --(無標籤)--> m9a(apply：flock 專案目錄（60 秒）)
- me8b: m9a(apply：flock 專案目錄（60 秒）) --(無標籤)--> m9b(重驗指紋)
- me9: m9b(重驗指紋) --(無標籤)--> m7c(相同 → CI 為真（frozen）且需改 tracked …)
- me9c: m7c(相同 → CI 為真（frozen）且需改 tracked …) --否--> m7(否 → --dry-run？)
- me11: m7(否 → --dry-run？) --(無標籤)--> m7z(否 ↓ 續「remove（2）」頁：建日誌 → 問 appe…)
- me3: m2(已接入 <repo>？) --否--> lp(結束前：log_prune（best-effort）)
- me5: m4(是 → 有 dev path 覆寫？) --是--> lp(結束前：log_prune（best-effort）)
- me8x: m9b(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- me9x: m7c(相同 → CI 為真（frozen）且需改 tracked …) --是--> lp(結束前：log_prune（best-effort）)
- me10: m7(否 → --dry-run？) --是--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m7y(0：只印清單（會刪什麼、會問什麼）)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m3(0：未接入（提示）)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m5(1：請先 undev <repo>（v2.1 B）)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m9x(1：指紋不同「請重跑」)
- lxe4: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m7cx(1：印需改清單（frozen；請在本機執行後 commit …)

## terms
- remove: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- baseline／metadata: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- append 行／CRLF／逐行比對: add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後逐行比對（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）：仍與紀錄原文相同的行 → 刪；缺失／被改的行 → 跳過並 warn（不是全有／全無；§4.3、v2.9 §5）
- 初始檔: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- dev 覆寫: version.local.toml 的 <repo> = "path:<dir>"；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋
- gen／mod?／import: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- CI 為真／frozen: CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs
- vC: 見「remove（2）」頁
- m7z: 續「remove（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8bccc -----
# v1p8bccc  39 流程 v2：remove（2）寫入段

nodes 74（不含 v2 小標）／edges 30／terms 12／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：remove（2）apply 寫入段（§2、§5；v2.2 C／E、v2.3 §1／§5、v2.5 §3／§11、v2.9 §5）
- [note/NOTE] pend: 已定（v2.3 §1、v2.5 §11、v2.9 §5）：remove／uninstall 只刪原文相同的 append 行，逐行比對 CRLF／LF 視為相同、其餘精確；仍相同 → 刪該行、缺失／被改 → 跳過並 warn（不是全有／全無）。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vC2 [v2]: remove <repo>（2）寫入段（承「remove（1）」頁）：建日誌 → 問 append 行（逐行：仍與紀錄相同 → 刪；缺失／被改 → 跳過 warn）→ 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 tools.just → 刪 version.toml 行 → 刪日誌
- [entry/ENTRY] m9e: 來自「remove（1）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）
- [step/SUB] m9l [v2]: 建進度日誌（.vendor_kit/.tmp.remove.<id>.toml；第一個寫入前）
- [file/F12] m9lf: ＋.vendor_kit/.tmp.remove.<id>.toml（進度日誌，不進 git）
- [decision/D12] m9h [v2]: metadata 有 append 過的行？
- [decision/D12] m9q [v2]: 有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）
- [step/SUB] m9s [v2]: 是：逐行比對紀錄的每一行（CRLF／LF 視為相同、其餘精確）
- [note/NOTE] m9mn [v2]: 逐行比對（§4.3、v2.9 §5）：紀錄的每一行仍與原文相同 → 刪該行；不同／缺失 → 跳過並 warn；不是全有／全無；零命中 → 不動、印清單
- [decision/D12] m9m [v2]: 該行仍與紀錄原文相同？
- [step/SUB] m9w [v2]: 否：跳過該行並 warn
- [step/SUB] m9d: 是：刪該行
- [file/F12] m9f: 初始檔（只移除仍相同的那幾行；其餘不動；永不刪檔）
- [decision/D12] m9l2 [v2]: 還有下一行？
- [step/SUB] m10a [v2]: 否：刪 baseline/<repo>/（含 metadata）
- [file/F12] m10af: －baseline/<repo>/（進 git）
- [step/SUB] m10b [v2]: 刪 cache/<repo>/
- [file/F12] m10bf: －cache/<repo>/（不進 git）
- [step/SUB] m10c [v2]: 刪 gen/<repo>.stamp
- [file/F12] m10cf: －gen/<repo>.stamp（不進 git）
- [step/SUB] m10d [v2]: 重生 gen/tools.just（去掉該工具所有 mod? 行）
- [file/F12] m10df: gen/tools.just（不進 git；mod? 行）
- [step/SUB] m10e [v2]: 最後刪 version.toml 該工具那一行
- [file/F12] m10ef: －version.toml <repo> 行（進 git）
- [step/SUB] m10g [v2]: 成功：刪進度日誌（最後一步）
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] m11: 0：印「以下初始檔保留，若不需要請 git rm：…」
- [end_red/R12] m10x [v2]: 1：寫入失敗，明列已完成／未完成
- [other/LEGEND] p8b2_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8b2_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8b2_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8b2_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8b2_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8b2_lg5 [legend]: 白：步驟
- [other/LEGEND] p8b2_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8b2_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8b2_lgx_entry [legend]: 虛線橢圓：跨頁入口
- [other/LEGEND] p8b2_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8b2_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8b2_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8b2_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8b2_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8b2_th: 本頁名詞
- [term/TERM_K] p8b2_tk0: remove
- [term/TERM_V] p8b2_tv0: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- [term/TERM_K] p8b2_tk1: uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）
- [term/TERM_V] p8b2_tv1: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- [term/TERM_K] p8b2_tk2: resolve／apply／--dry-run
- [term/TERM_V] p8b2_tv2: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- [term/TERM_K] p8b2_tk3: flock／指紋／進度日誌
- [term/TERM_V] p8b2_tv3: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p8b2_tk4: baseline／metadata
- [term/TERM_V] p8b2_tv4: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- [term/TERM_K] p8b2_tk5: append 行／CRLF／逐行比對
- [term/TERM_V] p8b2_tv5: add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後逐行比對（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）：仍與紀錄原文相同的行 → 刪；缺失／被改的行 → 跳過並 warn（不是全有／全無；§4.3、v2.9 §5）
- [term/TERM_K] p8b2_tk6: 初始檔
- [term/TERM_V] p8b2_tv6: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- [term/TERM_K] p8b2_tk7: gen／mod?／import
- [term/TERM_V] p8b2_tv7: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- [term/TERM_K] p8b2_tk8: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8b2_tv8: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8b2_tk9: config.toml（v2.12／v2.13）
- [term/TERM_V] p8b2_tv9: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8b2_tk10: 6-38
- [term/TERM_V] p8b2_tv10: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8b2_tk11: 結束狀態 0／1／2／3
- [term/TERM_V] p8b2_tv11: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- me11e: m9e(來自「remove（1）」頁：apply 檢查通過（非 dr…) --(無標籤)--> m9l(建進度日誌（.vendor_kit/.tmp.remove.…)
- me11f: m9l(建進度日誌（.vendor_kit/.tmp.remove.…) --寫--> m9lf(＋.vendor_kit/.tmp.remove.<id>.…)
- me11h: m9l(建進度日誌（.vendor_kit/.tmp.remove.…) --(無標籤)--> m9h(metadata 有 append 過的行？)
- me11hn: m9h(metadata 有 append 過的行？) --無--> m10a(否：刪 baseline/<repo>/（含 metadat…)
- me11q: m9h(metadata 有 append 過的行？) --有--> m9q(有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問…)
- me12n: m9q(有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問…) --否--> m10a(否：刪 baseline/<repo>/（含 metadat…)
- me12y: m9q(有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問…) --是--> m9s(是：逐行比對紀錄的每一行（CRLF／LF 視為相同、其餘精確…)
- me12m: m9s(是：逐行比對紀錄的每一行（CRLF／LF 視為相同、其餘精確…) --(無標籤)--> m9m(該行仍與紀錄原文相同？)
- me13w: m9m(該行仍與紀錄原文相同？) --否--> m9w(否：跳過該行並 warn)
- me13d: m9m(該行仍與紀錄原文相同？) --是--> m9d(是：刪該行)
- me13f: m9d(是：刪該行) --寫--> m9f(初始檔（只移除仍相同的那幾行；其餘不動；永不刪檔）)
- me14w: m9w(否：跳過該行並 warn) --(無標籤)--> m9l2(還有下一行？)
- me14d: m9d(是：刪該行) --(無標籤)--> m9l2(還有下一行？)
- me14y: m9l2(還有下一行？) --是--> m9m(該行仍與紀錄原文相同？)
- me14n: m9l2(還有下一行？) --否--> m10a(否：刪 baseline/<repo>/（含 metadat…)
- me15a: m10a(否：刪 baseline/<repo>/（含 metadat…) --刪--> m10af(－baseline/<repo>/（進 git）)
- me15b: m10a(否：刪 baseline/<repo>/（含 metadat…) --(無標籤)--> m10b(刪 cache/<repo>/)
- me15bf: m10b(刪 cache/<repo>/) --刪--> m10bf(－cache/<repo>/（不進 git）)
- me15c: m10b(刪 cache/<repo>/) --(無標籤)--> m10c(刪 gen/<repo>.stamp)
- me15cf: m10c(刪 gen/<repo>.stamp) --刪--> m10cf(－gen/<repo>.stamp（不進 git）)
- me15d: m10c(刪 gen/<repo>.stamp) --(無標籤)--> m10d(重生 gen/tools.just（去掉該工具所有 mod?…)
- me15df: m10d(重生 gen/tools.just（去掉該工具所有 mod?…) --寫--> m10df(gen/tools.just（不進 git；mod? 行）)
- me15e: m10d(重生 gen/tools.just（去掉該工具所有 mod?…) --(無標籤)--> m10e(最後刪 version.toml 該工具那一行)
- me15ef: m10e(最後刪 version.toml 該工具那一行) --刪--> m10ef(－version.toml <repo> 行（進 git）)
- me16: m10e(最後刪 version.toml 該工具那一行) --(無標籤)--> m10g(成功：刪進度日誌（最後一步）)
- me16x: m10e(最後刪 version.toml 該工具那一行) --失敗（任一步）--> lp(結束前：log_prune（best-effort）)
- me17: m10g(成功：刪進度日誌（最後一步）) --(無標籤)--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m11(0：印「以下初始檔保留，若不需要請 git rm：…」)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> m10x(1：寫入失敗，明列已完成／未完成)

## terms
- remove: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- baseline／metadata: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- append 行／CRLF／逐行比對: add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後逐行比對（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）：仍與紀錄原文相同的行 → 刪；缺失／被改的行 → 跳過並 warn（不是全有／全無；§4.3、v2.9 §5）
- 初始檔: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- gen／mod?／import: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs
- vC2: 其他「remove（1）」頁
- m9e: 來自「remove（1）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #f8cecc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


----- 頁 v1p8bc -----
# v1p8bc  40 流程 v2：uninstall（1）resolve → apply 前置

nodes 76（不含 v2 小標）／edges 26／terms 14／xrefs 2

## nodes
- [other/TITLE] title: 流程 v2：uninstall（1）resolve → apply 前置（§2；v2.2 E、v2.3 §6、v2.5 §3／§10）
- [note/NOTE] pend: 已定（v2.3 §1、v2.5 §11、v2.9 §5）：remove／uninstall 只刪原文相同的 append 行，逐行比對 CRLF／LF 視為相同、其餘精確；仍相同 → 刪該行、缺失／被改 → 跳過並 warn（不是全有／全無）。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。
- [header/HDR] hdr0: 使用者
- [header/HDR] hdr1: 啟動器（主機 sh）
- [header/HDR] hdr2: 引擎容器
- [header/HDR] hdr3: GHCR
- [header/HDR] hdr4: 專案目錄
- [other/BAND] vD [v2]: uninstall（1）：全部拆掉（install 的反向；bootstrap.sh 的反向也是它）= resolve（預檢 → hash → 保護清單 → 計畫 → 詢問清單 → 指紋 → stdout）→ apply 前置（拿鎖、重驗、frozen、dry-run）；寫入段見「uninstall（2）」頁；不 rm -rf .vendor_kit/
- [end_ok/G12] x0: just vendor_kit uninstall（-y、--dry-run）
- [step/W12] x0l [v2]: 建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）
- [step/W12] x1 [v2]: docker run <引擎> resolve uninstall（不經 docker create/cp）
- [step/SUB] x1e [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）
- [decision/D12] x2 [v2]: 預檢全部工具通過？
- [step/SUB] x2b [v2]: 是：算每個自產檔的 hash（薄殼、version.toml、config.toml、gen/、cache/、baseline/；不動任何東西）
- [step/SUB] x2bb [v2]: 分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）
- [rule/RULE] x2r [v2]: 保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過
- [step/SUB] x2c [v2]: 產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）
- [step/SUB] x2d [v2]: 產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 四行
- [step/SUB] x2e [v2]: 產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）
- [step/SUB] x2e2 [v2]: stdout vk-resolve/1：計畫＋詢問清單＋指紋回啟動器
- [step/W12] x1b [v2]: docker run <引擎> apply uninstall（--dry-run 原樣轉發）
- [step/SUB] x1be [v2]: append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 apply）
- [step/SUB] x4a [v2]: apply：flock 專案目錄（60 秒）
- [step/SUB] x4b [v2]: 重驗指紋
- [decision/D12] x3c [v2]: 相同 → CI 為真（frozen）且需改 tracked 檔？
- [decision/D12] x3: 否 → --dry-run？
- [other/TEXT] x4z: 否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌
- [step/W12] lp [v2]: 結束前：log_prune（best-effort）
- [step/W12] lx [v2]: launcher_exit（記結束碼、耗時）
- [end_ok/G12] x3y [v2]: 0：只印會刪什麼、會問什麼
- [end_orange/O12] x2x [v2]: 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）
- [end_orange/O12] x4bx [v2]: 1：指紋不同「請重跑」
- [end_orange/O12] x3cx [v2]: 1：印需改清單（frozen；請在本機執行後 commit 並 push）
- [other/LEGEND] p8bc_lg0 [legend]: 淺灰：情境分組（無狀態意義）
- [other/LEGEND] p8bc_lg1 [legend]: 黃：判斷
- [other/LEGEND] p8bc_lg2 [legend]: 綠：起點／終點
- [other/LEGEND] p8bc_lg3 [legend]: 紅：失敗終止（拉不到／寫壞）
- [other/LEGEND] p8bc_lg4 [legend]: 橙：需要人動作（1／3 印指令；2 解衝突）
- [other/LEGEND] p8bc_lg5 [legend]: 白：步驟
- [other/LEGEND] p8bc_lg6 [legend]: 虛線框：專案裡的檔案
- [other/LEGEND] p8bc_lgt [legend]: 實線 = 執行順序（指向檔案時 = 寫入／讀取）
- [other/LEGEND] p8bc_lgx_note [legend]: 便條：補充說明
- [other/LEGEND] p8bc_lgx_rule [legend]: 橘框：規則（已定）
- [other/LEGEND] p8bc_lgx_sub [legend]: 藍：引擎子命令（容器內）
- [other/LEGEND] p8bc_lgx_img [legend]: 紫：image（引擎與工具）
- [other/LEGEND] p8bc_lgx_hdr [legend]: 灰底：泳道／表格表頭
- [other/LEGEND] p8bc_lgx_v2 [v2] [legend]: 右上綠標 v2：與 v1 不同處
- [other/TEXT] p8bc_th: 本頁名詞
- [term/TERM_K] p8bc_tk0: remove
- [term/TERM_V] p8bc_tv0: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- [term/TERM_K] p8bc_tk1: uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）
- [term/TERM_V] p8bc_tv1: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- [term/TERM_K] p8bc_tk2: resolve／apply／--dry-run
- [term/TERM_V] p8bc_tv2: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- [term/TERM_K] p8bc_tk3: flock／指紋／進度日誌
- [term/TERM_V] p8bc_tv3: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- [term/TERM_K] p8bc_tk4: baseline／metadata
- [term/TERM_V] p8bc_tv4: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- [term/TERM_K] p8bc_tk5: 初始檔
- [term/TERM_V] p8bc_tv5: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- [term/TERM_K] p8bc_tk6: 保護清單／保護模式
- [term/TERM_V] p8bc_tv6: uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過
- [term/TERM_K] p8bc_tk7: dev 覆寫
- [term/TERM_V] p8bc_tv7: version.local.toml 的 <repo> = "path:<dir>"；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋
- [term/TERM_K] p8bc_tk8: gen／mod?／import
- [term/TERM_V] p8bc_tv8: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- [term/TERM_K] p8bc_tk9: CI 為真／frozen
- [term/TERM_V] p8bc_tv9: CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）
- [term/TERM_K] p8bc_tk10: 操作紀錄檔／log（v2.12）
- [term/TERM_V] p8bc_tv10: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- [term/TERM_K] p8bc_tk11: config.toml（v2.12／v2.13）
- [term/TERM_V] p8bc_tv11: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- [term/TERM_K] p8bc_tk12: 6-38
- [term/TERM_V] p8bc_tv12: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- [term/TERM_K] p8bc_tk13: 結束狀態 0／1／2／3
- [term/TERM_V] p8bc_tv13: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## edges
- xe1: x0(just vendor_kit uninstall（-y、-…) --(無標籤)--> x0l(建 log 檔並寫 launcher_start（失敗 → …)
- xe1l: x0l(建 log 檔並寫 launcher_start（失敗 → …) --(無標籤)--> x1(docker run <引擎> resolve uninst…)
- xe1e: x1(docker run <引擎> resolve uninst…) --(無標籤)--> x1e(append engine_start 到同一 log 檔（…)
- xe2: x1e(append engine_start 到同一 log 檔（…) --(無標籤)--> x2(預檢全部工具通過？)
- xe4: x2(預檢全部工具通過？) --是--> x2b(是：算每個自產檔的 hash（薄殼、version.toml…)
- xe4b: x2b(是：算每個自產檔的 hash（薄殼、version.toml…) --(無標籤)--> x2bb(分類：hash 相符 → 可刪清單；未知或被改的 → 保護清…)
- xe4c: x2bb(分類：hash 相符 → 可刪清單；未知或被改的 → 保護清…) --(無標籤)--> x2c(產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順…)
- xe4d: x2c(產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順…) --(無標籤)--> x2d(產生詢問清單：append 行、根 justfile 那行、…)
- xe4e: x2d(產生詢問清單：append 行、根 justfile 那行、…) --(無標籤)--> x2e(產生輸入指紋（version.toml、各 metadata…)
- xe4e2: x2e(產生輸入指紋（version.toml、各 metadata…) --(無標籤)--> x2e2(stdout vk-resolve/1：計畫＋詢問清單＋指紋…)
- xe5: x2e2(stdout vk-resolve/1：計畫＋詢問清單＋指紋…) --(無標籤)--> x1b(docker run <引擎> apply uninstal…)
- xe5b: x1b(docker run <引擎> apply uninstal…) --(無標籤)--> x1be(append engine_start 到同一 log 檔（…)
- xe5be: x1be(append engine_start 到同一 log 檔（…) --(無標籤)--> x4a(apply：flock 專案目錄（60 秒）)
- xe5c: x4a(apply：flock 專案目錄（60 秒）) --(無標籤)--> x4b(重驗指紋)
- xe5d: x4b(重驗指紋) --(無標籤)--> x3c(相同 → CI 為真（frozen）且需改 tracked …)
- xe5f: x3c(相同 → CI 為真（frozen）且需改 tracked …) --否--> x3(否 → --dry-run？)
- xe7: x3(否 → --dry-run？) --(無標籤)--> x4z(否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具…)
- xe3: x2(預檢全部工具通過？) --否--> lp(結束前：log_prune（best-effort）)
- xe5x: x4b(重驗指紋) --不同--> lp(結束前：log_prune（best-effort）)
- xe5e: x3c(相同 → CI 為真（frozen）且需改 tracked …) --是--> lp(結束前：log_prune（best-effort）)
- xe6: x3(否 → --dry-run？) --是--> lp(結束前：log_prune（best-effort）)
- lpx: lp(結束前：log_prune（best-effort）) --(無標籤)--> lx(launcher_exit（記結束碼、耗時）)
- lxe0: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> x3y(0：只印會刪什麼、會問什麼)
- lxe1: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> x2x(1：預檢失敗（dev 中 → 請先 undev；未完成接入 …)
- lxe2: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> x4bx(1：指紋不同「請重跑」)
- lxe3: lx(launcher_exit（記結束碼、耗時）) --(無標籤)--> x3cx(1：印需改清單（frozen；請在本機執行後 commit …)

## terms
- remove: 拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/<repo>/、cache/<repo>/、gen/<repo>.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單
- uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）: 全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf
- resolve／apply／--dry-run: resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）
- flock／指紋／進度日誌: flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復
- baseline／metadata: baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 建 baseline/.gitkeep 與 baseline/vendor_kit/config.toml 副本（metadata 到 add 才建；根 .dockerignore 的 append 行記於 baseline/.vendor_kit.toml，v2.13 P10）；remove 先讀它再刪整個 baseline/<repo>/
- 初始檔: 工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata
- 保護清單／保護模式: uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過
- dev 覆寫: version.local.toml 的 <repo> = "path:<dir>"；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋
- gen／mod?／import: gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的
- CI 為真／frozen: CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）
- 操作紀錄檔／log（v2.12）: .vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單
- config.toml（v2.12／v2.13）: .vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設
- 6-38: log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log
- 結束狀態 0／1／2／3: 0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）

## xrefs
- vD: 見「uninstall（2）」頁
- x4z: 續「uninstall（2）」頁

## fills（非圖例）: #FFF4C3 #d5e8d4 #dae8fc #e6e6e6 #f5f5f5 #ffe6cc #ffffff
## legend_fills: #FFF4C3 #d5e8d4 #dae8fc #e1d5e7 #e6e6e6 #f5f5f5 #f8cecc #ffe6cc #ffffff none


=== 附件 L：機械 lint（本組頁）===

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
ERROR: Reconnecting... 2/5
ERROR: Reconnecting... 3/5
ERROR: Reconnecting... 4/5
ERROR: Reconnecting... 5/5
warning: Falling back from WebSockets to HTTPS transport. stream disconnected before completion: websocket closed by server before response.completed
codex
以下僅列人工審查發現；不重複附件 L，也不回報舊名／新名問題。

## 跨頁共通問題

- 頁 `v1p7bd`、`v1p7bc`、`v1p7bcc`、`v1p7bcx`、`v1p7bccc`、`v1p8`、`v1p8ccc`、`v1p8c`、`v1p8cc`、`v1p8b`、`v1p8bccc`、`v1p8bc`；元件 `lp → lx → 多個終點`；類別 B；所有成功、失敗與需人處理分支先匯入同一個 `launcher_exit`，再由它無條件分岔至所有終點，讀圖上無法判斷哪條來源對應哪個結束狀態；應在匯流前保留結果碼，或各結果分別接自己的結束序列。必修。
- 同上各頁；各 `docker run`／`engine_start` 區段；類別 A；規格要求每個引擎子命令結束前 append `engine_exit`，圖面普遍只畫 `engine_start`，未畫 `engine_exit`，尤其跨頁接手時無法確認同一紀錄檔內每個容器都有成對事件。必修。
- 同上各頁；名詞表；類別 F；每頁重複十餘條完整契約，許多名詞未在該頁流程使用，反而使真正分支難以閱讀；名詞表宜只保留該頁實際出現且一般人不懂的詞。選修。

## v1p7bd

- `uD`、`d2c2`、`d2c3`；類別 A；頁首及流程宣稱 sync「只把 cache 換回舊版」，但規格要求 sync 在需要時也重生 `gen/tools.just`，本頁完全缺少該判斷與寫入。必修。
- `d2c`：「materialize 舊版：/dist/<repo> 複製到暫存目錄」；類別 C；此格同時描述取件與「初始檔、baseline 不碰」的範圍規則，應把動作縮為「從 `/dist/<repo>` 取件」，限制另作便條。選修。
- `d1px`；類別 B；pull 失敗與逾時共用一個終點，但沒有從失敗分支保存 6-24 或 6-31 的判定，配合共通的 `launcher_exit` 扇出後語意不成立。必修。

## v1p7bc

- `s2a`、`s2dq`；類別 A；「完整預檢」後只畫「含 dev 中工具？」一項；規格要求不帶 repo 的 upgrade 在任何寫入前預檢全部工具，包括撞名、憑證與需要詢問的項目，任一不過整體不動。必修。
- `s2n`；類別 B；「每個工具走 B（1）頁」只是文字，沒有跨頁出口圖形與實線，屬懸空流程；應改為白虛線跨頁出口並標出回傳彙總位置。必修。
- `s2r → s4`；類別 B；接到下一頁的文字不是白虛線跨頁入口／出口，且本頁沒有交代新引擎子命令的 `engine_start` 由下一頁接續。必修。
- `s2lv`；類別 A；把「是否為 local 覆寫」與「image ID 是否不符」合成一個判斷，正常非覆寫路徑也只能沿「否」通過，容易誤讀；應先分 local 覆寫，再只對覆寫檢查 ID。選修。

## v1p7bcc

- `s12a`、`s12b`；類別 A；`upgrade vendor_kit` 是單段動詞，沒有先前 resolve 所產生的指紋可供「重驗」；本頁卻畫成拿鎖後重驗指紋，混入兩段動詞模型。必修。
- `s12a0` 之後；類別 A；缺少偵測與恢復既有 `.tmp.upgrade.<id>.toml` 的分支；規格要求直接執行 `upgrade vendor_kit` 時若有未完成自身升級，本次立即依日誌恢復。必修。
- `s12tt → s12v → s12jz`；類別 A；指定新 `@<tag>` 或 registry 找到新目標後，沒有 inspect／pull「目標引擎」的步驟便直接去改第一行；目前頁首 inspect／pull 的是現行引擎，不是新目標。必修。
- `s11x`；類別 D；「image ID 不符」是無法執行的失敗可用紅色，但「拉不到」應明列 6-24／6-31；目前合併文字遺失逾時及分類訊息。必修。
- `s12d`：「@<tag> 舊版且無法無損讀？」；類別 C；同格同時判斷「是否降版」與「相容性是否通過」，應拆成兩個判斷，否則「指定相同版／新版」與「舊版但可讀」共用同一路徑，讀者難以驗證。選修。

## v1p7bcx

- `s12hr`；類別 A；改完第一行後直接 `docker run 新引擎`，缺少對新 ref 的 `docker image inspect`、必要時 pull，以及 pull／ID 不符時的 6-2b 分支。必修。
- `s12hq --否→ s12hx`；類別 A；判斷是「第一行變了且等於計畫值」，否可能包括「沒變」或「變成非計畫值」；後者屬第二次改變並應走 6-2b，本頁卻一律說「第一行未變、不是 6-2b」。必修。
- `s12hz`；類別 B；跨頁出口以普通文字表示，沒有白虛線橢圓，也沒有明確連到 `v1p7bcc` 的元件 `s11r`。必修。
- `s12w`；類別 C；同格同時包含修改 version.toml、原子替換與寫 `engine_exit` 三件事；至少應把 `engine_exit` 拆出。必修。

## v1p7bccc

- `s13gn`；類別 A；config.toml 不存在時直接建立，少了規格要求的詢問／`-y` 分支。必修。
- `s13gy`、`s13gw`；類別 A；三方合併可能衝突或解析失敗並回 2，但圖上沒有結束碼 2、衝突標記、基準版是否推進等分支，全部直接流向寫檔。必修。
- `s13gb`；類別 A；只推進 `baseline/vendor_kit/config.toml`，漏畫同步更新 `baseline/.vendor_kit.toml` 中 config.toml 的 metadata。必修。
- `s13 → s13gq`；類別 A；薄殼五檔已先原子替換，之後 config 合併若失敗便留下部分重產；圖上沒有用進度檔恢復或暫存整批提交來說明跨檔失敗狀態。必修。
- `s14`；類別 F；無新版但薄殼需修復時也會到此格，文案卻固定寫「已升級引擎 vX → vY」，一般人會誤以為版本真的改變；應區分「換引擎後重產」與「同引擎修復重產」。必修。
- `s13q`；類別 C；「任一步失敗」與「第一行是否已改／又變」揉成一格，且無法表達第二次第一行又變的獨立情況。選修。

## v1p8

- `d6a` 之前；類別 A；dev 是可寫動詞，規格要求第一個寫入前建立 `.tmp.dev.<id>.toml`，記覆寫行、symlink 目標與印記；本頁完全缺少建立、成功刪除及失敗恢復。必修。
- `d6`；類別 A；圖中寫成頂層 `<repo> = "path:<dir>"`；規格要求工具覆寫位於 `[tools].<repo>`。必修。
- `d1q`、`d2c`；類別 F；前者只查 init.toml 是否存在，後者再查「dist 合法」，但未說合法包含哪些最低條件，兩個判斷看似重複；應把前者標成主機掛載前存在性檢查，後者標成引擎完整驗證。選修。
- `d3c`；類別 D；「dist／init.toml 不合法」屬驗證失敗，依顏色規則應為紅色，不是橙色需人處理。必修。

## v1p8ccc

- `v2a` 之後；類別 A；與 v1p8 相同，缺少 `.tmp.dev.<id>.toml` 的建立、內容、成功刪除與恢復路徑。必修。
- `v1i` 至 `v1`；類別 A；缺少依目標 image LABEL 檢查介面版／檔案版；若舊 image 會要求重產 tracked 薄殼，規格要求改檔前回 3，本頁沒有此分支。必修。
- `v2b`、`v2c`；類別 C；兩格分別寫同一個 TOML 的兩行尚可，但對外實際是一個原子更新；目前兩條分開的檔案寫入線會使人以為第一行可以先落盤。應以一個原子替換動作寫兩欄。必修。
- `v5`：「下次打任何 just」；類別 F；不是每個任意 just recipe 都必然進 vendor_kit 啟動器；應寫成「下次執行 vendor_kit 動詞或有 `_sync` 前置的工具 recipe」。必修。

## v1p8c

- `u6l`；類別 A；進度檔文字沒有說明須記錄「要撤的覆寫行與 image ID」，與 undev 的恢復契約不足。必修。
- `u6g`；類別 B；只有「刪進度日誌」動作，沒有對應檔案節點及刪除線，和同頁其他檔案變更表示法不一致。選修。
- `u6c → u6d`；類別 A；先撤 version.local.toml、再拆 symlink、最後重建 cache，任一步失敗時要保留可恢復狀態；圖雖有總括失敗出口，但未畫從 `u6c`、`u6d`、`u6e2` 等各步到失敗處，只有 `u6f` 有「任一步」線，容易被讀成前面寫失敗仍繼續。必修。
- `u6d`：「是／已刪：拆掉 cache/<repo>/ 的 symlink」；類別 F；「是／已刪」指的是前一判斷兩條路，文字脫離箭線後難懂；改成單純「拆掉 cache symlink」。選修。

## v1p8cc

- `w2l`；類別 A；進度檔未標明必須記錄要撤的 `vendor_kit`、`vendor_kit_image_id` 與 image ID，恢復資訊表達不足。必修。
- `w4`：「下次打任何 just」；類別 F；同 v1p8ccc，並非任何 just 都會進 sync；應限縮為 vendor_kit 動詞或有 `_sync` 的工具 recipe。必修。
- `w5b → w5p → w5c`；類別 A；這整段與本頁主題「undev vendor_kit」不是同一次動詞，而是下一次 sync 的流程；依審查標準應移到獨立 sync 頁，本頁只保留跨頁出口。必修。
- `w5p_x`；類別 B；pull 成功的線未標「成功」，而 pull 失敗另繞到底部；在縮圖上兩條長線來源難辨，應直接從 pull 畫成功／失敗兩支。選修。

## v1p8b

- `m6d2`；類別 A；宣稱 vk-resolve/1 stdout 含「計畫」，但規格列出的 kind 沒有刪除清單或詢問清單；啟動器只需保存合法協定並把原 argv 交 apply，不能傳未定義記錄。必修。
- `m6c`；類別 A；resolve 產生詢問清單本身可以是引擎內部計算，但本頁畫成送到啟動器；詢問必須由 apply 引擎執行，不能讓啟動器解讀未定義的問句資料。必修。
- `m7 → m7z`；類別 B；通往下一頁的「否」沒有畫成跨頁出口，且 edge 沒有「否」標籤。必修。
- `m0`；類別 C；起點同格放命令與兩個可選參數，尚可作語法，但括號寫法容易誤認兩者必須成組；建議改成規格形式 `remove <repo> [-y] [--dry-run]`。選修。

## v1p8bccc

- `m9q --否→ m10a`；類別 A；使用者明確拒絕移除 append 行後仍刪 metadata／baseline，將失去這些行的所有權紀錄；規格說明確回答否要在 metadata 記錄，不能隨即刪掉承載紀錄的 metadata 而不交代保留狀態。必修。
- `m9q`；類別 A；缺少無 tty／EOF／Ctrl-C 分支；規格要求無 tty 或 EOF 且無 `-y` 回 1、不套用，Ctrl-C 亦中止且不記 declined。必修。
- `m10d`；類別 A；`gen/tools.just` 必須最後寫並與 cache 同一 apply 原子替換；本頁在它之後仍刪 version.toml，且沒有表達 tools.just 的原子替換要求。若「最後」指所有產生檔的提交點，現順序不符。必修。
- `m10e --失敗（任一步）→ lp`；類別 B；「任一步」的線卻只從最後刪 version.toml 的元件出發，視覺上不能涵蓋前面的 append、baseline、cache、stamp、tools.just 寫入失敗。必修。

## v1p8bc

- `x2e2`；類別 A；同 v1p8b，vk-resolve/1 沒有「執行計畫／詢問清單／保護清單」的協定 kind，不能宣稱這些資料透過 stdout 傳給啟動器。必修。
- `x2`、`x2x`；類別 A；預檢失敗例只列 dev 與未完成接入，漏掉多工具寫入動詞要求的完整預檢項目及「任一不過整體不動、原因全列」。必修。
- `x2b`；類別 C；一格同時列薄殼、version.toml、config.toml、gen、cache、baseline 全部 hash 計算，屬多個最小單元；至少應分成「計算 tracked 自產檔」與「計算本機產物」，或收成一個抽象模組動作。選修。
- `x3 → x4z`；類別 B；跨頁出口未使用白虛線橢圓，且 edge 未標「否」，與同頁 dry-run 的「是」支線不對稱。必修。
- `x2r`；類別 F；規則框位於流程右側但沒有任何連線指明它約束 `x2c` 或下一頁的逐工具 remove；一般讀者會把它當孤立註解。選修。

## 未附完整頁面

附件只有 `uninstall（1）` 的 `v1p8bc`；規格與跨頁引用所稱的 `uninstall（2）` 不在本組附件內，因此無法審查其實際刪除順序、config.toml 保護、根 justfile／`.dockerignore` 逐行詢問、`log/` 保留及進度檔最後刪除。

總評：本組頁面目前不能交給使用者看；核心流程仍有多項規格矛盾、跨頁斷點與結果線歧義，尤其自身升級、dev 進度檔及 vk-resolve/1 內容必須先修正。
tokens used
171,705
以下僅列人工審查發現；不重複附件 L，也不回報舊名／新名問題。

## 跨頁共通問題

- 頁 `v1p7bd`、`v1p7bc`、`v1p7bcc`、`v1p7bcx`、`v1p7bccc`、`v1p8`、`v1p8ccc`、`v1p8c`、`v1p8cc`、`v1p8b`、`v1p8bccc`、`v1p8bc`；元件 `lp → lx → 多個終點`；類別 B；所有成功、失敗與需人處理分支先匯入同一個 `launcher_exit`，再由它無條件分岔至所有終點，讀圖上無法判斷哪條來源對應哪個結束狀態；應在匯流前保留結果碼，或各結果分別接自己的結束序列。必修。
- 同上各頁；各 `docker run`／`engine_start` 區段；類別 A；規格要求每個引擎子命令結束前 append `engine_exit`，圖面普遍只畫 `engine_start`，未畫 `engine_exit`，尤其跨頁接手時無法確認同一紀錄檔內每個容器都有成對事件。必修。
- 同上各頁；名詞表；類別 F；每頁重複十餘條完整契約，許多名詞未在該頁流程使用，反而使真正分支難以閱讀；名詞表宜只保留該頁實際出現且一般人不懂的詞。選修。

## v1p7bd

- `uD`、`d2c2`、`d2c3`；類別 A；頁首及流程宣稱 sync「只把 cache 換回舊版」，但規格要求 sync 在需要時也重生 `gen/tools.just`，本頁完全缺少該判斷與寫入。必修。
- `d2c`：「materialize 舊版：/dist/<repo> 複製到暫存目錄」；類別 C；此格同時描述取件與「初始檔、baseline 不碰」的範圍規則，應把動作縮為「從 `/dist/<repo>` 取件」，限制另作便條。選修。
- `d1px`；類別 B；pull 失敗與逾時共用一個終點，但沒有從失敗分支保存 6-24 或 6-31 的判定，配合共通的 `launcher_exit` 扇出後語意不成立。必修。

## v1p7bc

- `s2a`、`s2dq`；類別 A；「完整預檢」後只畫「含 dev 中工具？」一項；規格要求不帶 repo 的 upgrade 在任何寫入前預檢全部工具，包括撞名、憑證與需要詢問的項目，任一不過整體不動。必修。
- `s2n`；類別 B；「每個工具走 B（1）頁」只是文字，沒有跨頁出口圖形與實線，屬懸空流程；應改為白虛線跨頁出口並標出回傳彙總位置。必修。
- `s2r → s4`；類別 B；接到下一頁的文字不是白虛線跨頁入口／出口，且本頁沒有交代新引擎子命令的 `engine_start` 由下一頁接續。必修。
- `s2lv`；類別 A；把「是否為 local 覆寫」與「image ID 是否不符」合成一個判斷，正常非覆寫路徑也只能沿「否」通過，容易誤讀；應先分 local 覆寫，再只對覆寫檢查 ID。選修。

## v1p7bcc

- `s12a`、`s12b`；類別 A；`upgrade vendor_kit` 是單段動詞，沒有先前 resolve 所產生的指紋可供「重驗」；本頁卻畫成拿鎖後重驗指紋，混入兩段動詞模型。必修。
- `s12a0` 之後；類別 A；缺少偵測與恢復既有 `.tmp.upgrade.<id>.toml` 的分支；規格要求直接執行 `upgrade vendor_kit` 時若有未完成自身升級，本次立即依日誌恢復。必修。
- `s12tt → s12v → s12jz`；類別 A；指定新 `@<tag>` 或 registry 找到新目標後，沒有 inspect／pull「目標引擎」的步驟便直接去改第一行；目前頁首 inspect／pull 的是現行引擎，不是新目標。必修。
- `s11x`；類別 D；「image ID 不符」是無法執行的失敗可用紅色，但「拉不到」應明列 6-24／6-31；目前合併文字遺失逾時及分類訊息。必修。
- `s12d`：「@<tag> 舊版且無法無損讀？」；類別 C；同格同時判斷「是否降版」與「相容性是否通過」，應拆成兩個判斷，否則「指定相同版／新版」與「舊版但可讀」共用同一路徑，讀者難以驗證。選修。

## v1p7bcx

- `s12hr`；類別 A；改完第一行後直接 `docker run 新引擎`，缺少對新 ref 的 `docker image inspect`、必要時 pull，以及 pull／ID 不符時的 6-2b 分支。必修。
- `s12hq --否→ s12hx`；類別 A；判斷是「第一行變了且等於計畫值」，否可能包括「沒變」或「變成非計畫值」；後者屬第二次改變並應走 6-2b，本頁卻一律說「第一行未變、不是 6-2b」。必修。
- `s12hz`；類別 B；跨頁出口以普通文字表示，沒有白虛線橢圓，也沒有明確連到 `v1p7bcc` 的元件 `s11r`。必修。
- `s12w`；類別 C；同格同時包含修改 version.toml、原子替換與寫 `engine_exit` 三件事；至少應把 `engine_exit` 拆出。必修。

## v1p7bccc

- `s13gn`；類別 A；config.toml 不存在時直接建立，少了規格要求的詢問／`-y` 分支。必修。
- `s13gy`、`s13gw`；類別 A；三方合併可能衝突或解析失敗並回 2，但圖上沒有結束碼 2、衝突標記、基準版是否推進等分支，全部直接流向寫檔。必修。
- `s13gb`；類別 A；只推進 `baseline/vendor_kit/config.toml`，漏畫同步更新 `baseline/.vendor_kit.toml` 中 config.toml 的 metadata。必修。
- `s13 → s13gq`；類別 A；薄殼五檔已先原子替換，之後 config 合併若失敗便留下部分重產；圖上沒有用進度檔恢復或暫存整批提交來說明跨檔失敗狀態。必修。
- `s14`；類別 F；無新版但薄殼需修復時也會到此格，文案卻固定寫「已升級引擎 vX → vY」，一般人會誤以為版本真的改變；應區分「換引擎後重產」與「同引擎修復重產」。必修。
- `s13q`；類別 C；「任一步失敗」與「第一行是否已改／又變」揉成一格，且無法表達第二次第一行又變的獨立情況。選修。

## v1p8

- `d6a` 之前；類別 A；dev 是可寫動詞，規格要求第一個寫入前建立 `.tmp.dev.<id>.toml`，記覆寫行、symlink 目標與印記；本頁完全缺少建立、成功刪除及失敗恢復。必修。
- `d6`；類別 A；圖中寫成頂層 `<repo> = "path:<dir>"`；規格要求工具覆寫位於 `[tools].<repo>`。必修。
- `d1q`、`d2c`；類別 F；前者只查 init.toml 是否存在，後者再查「dist 合法」，但未說合法包含哪些最低條件，兩個判斷看似重複；應把前者標成主機掛載前存在性檢查，後者標成引擎完整驗證。選修。
- `d3c`；類別 D；「dist／init.toml 不合法」屬驗證失敗，依顏色規則應為紅色，不是橙色需人處理。必修。

## v1p8ccc

- `v2a` 之後；類別 A；與 v1p8 相同，缺少 `.tmp.dev.<id>.toml` 的建立、內容、成功刪除與恢復路徑。必修。
- `v1i` 至 `v1`；類別 A；缺少依目標 image LABEL 檢查介面版／檔案版；若舊 image 會要求重產 tracked 薄殼，規格要求改檔前回 3，本頁沒有此分支。必修。
- `v2b`、`v2c`；類別 C；兩格分別寫同一個 TOML 的兩行尚可，但對外實際是一個原子更新；目前兩條分開的檔案寫入線會使人以為第一行可以先落盤。應以一個原子替換動作寫兩欄。必修。
- `v5`：「下次打任何 just」；類別 F；不是每個任意 just recipe 都必然進 vendor_kit 啟動器；應寫成「下次執行 vendor_kit 動詞或有 `_sync` 前置的工具 recipe」。必修。

## v1p8c

- `u6l`；類別 A；進度檔文字沒有說明須記錄「要撤的覆寫行與 image ID」，與 undev 的恢復契約不足。必修。
- `u6g`；類別 B；只有「刪進度日誌」動作，沒有對應檔案節點及刪除線，和同頁其他檔案變更表示法不一致。選修。
- `u6c → u6d`；類別 A；先撤 version.local.toml、再拆 symlink、最後重建 cache，任一步失敗時要保留可恢復狀態；圖雖有總括失敗出口，但未畫從 `u6c`、`u6d`、`u6e2` 等各步到失敗處，只有 `u6f` 有「任一步」線，容易被讀成前面寫失敗仍繼續。必修。
- `u6d`：「是／已刪：拆掉 cache/<repo>/ 的 symlink」；類別 F；「是／已刪」指的是前一判斷兩條路，文字脫離箭線後難懂；改成單純「拆掉 cache symlink」。選修。

## v1p8cc

- `w2l`；類別 A；進度檔未標明必須記錄要撤的 `vendor_kit`、`vendor_kit_image_id` 與 image ID，恢復資訊表達不足。必修。
- `w4`：「下次打任何 just」；類別 F；同 v1p8ccc，並非任何 just 都會進 sync；應限縮為 vendor_kit 動詞或有 `_sync` 的工具 recipe。必修。
- `w5b → w5p → w5c`；類別 A；這整段與本頁主題「undev vendor_kit」不是同一次動詞，而是下一次 sync 的流程；依審查標準應移到獨立 sync 頁，本頁只保留跨頁出口。必修。
- `w5p_x`；類別 B；pull 成功的線未標「成功」，而 pull 失敗另繞到底部；在縮圖上兩條長線來源難辨，應直接從 pull 畫成功／失敗兩支。選修。

## v1p8b

- `m6d2`；類別 A；宣稱 vk-resolve/1 stdout 含「計畫」，但規格列出的 kind 沒有刪除清單或詢問清單；啟動器只需保存合法協定並把原 argv 交 apply，不能傳未定義記錄。必修。
- `m6c`；類別 A；resolve 產生詢問清單本身可以是引擎內部計算，但本頁畫成送到啟動器；詢問必須由 apply 引擎執行，不能讓啟動器解讀未定義的問句資料。必修。
- `m7 → m7z`；類別 B；通往下一頁的「否」沒有畫成跨頁出口，且 edge 沒有「否」標籤。必修。
- `m0`；類別 C；起點同格放命令與兩個可選參數，尚可作語法，但括號寫法容易誤認兩者必須成組；建議改成規格形式 `remove <repo> [-y] [--dry-run]`。選修。

## v1p8bccc

- `m9q --否→ m10a`；類別 A；使用者明確拒絕移除 append 行後仍刪 metadata／baseline，將失去這些行的所有權紀錄；規格說明確回答否要在 metadata 記錄，不能隨即刪掉承載紀錄的 metadata 而不交代保留狀態。必修。
- `m9q`；類別 A；缺少無 tty／EOF／Ctrl-C 分支；規格要求無 tty 或 EOF 且無 `-y` 回 1、不套用，Ctrl-C 亦中止且不記 declined。必修。
- `m10d`；類別 A；`gen/tools.just` 必須最後寫並與 cache 同一 apply 原子替換；本頁在它之後仍刪 version.toml，且沒有表達 tools.just 的原子替換要求。若「最後」指所有產生檔的提交點，現順序不符。必修。
- `m10e --失敗（任一步）→ lp`；類別 B；「任一步」的線卻只從最後刪 version.toml 的元件出發，視覺上不能涵蓋前面的 append、baseline、cache、stamp、tools.just 寫入失敗。必修。

## v1p8bc

- `x2e2`；類別 A；同 v1p8b，vk-resolve/1 沒有「執行計畫／詢問清單／保護清單」的協定 kind，不能宣稱這些資料透過 stdout 傳給啟動器。必修。
- `x2`、`x2x`；類別 A；預檢失敗例只列 dev 與未完成接入，漏掉多工具寫入動詞要求的完整預檢項目及「任一不過整體不動、原因全列」。必修。
- `x2b`；類別 C；一格同時列薄殼、version.toml、config.toml、gen、cache、baseline 全部 hash 計算，屬多個最小單元；至少應分成「計算 tracked 自產檔」與「計算本機產物」，或收成一個抽象模組動作。選修。
- `x3 → x4z`；類別 B；跨頁出口未使用白虛線橢圓，且 edge 未標「否」，與同頁 dry-run 的「是」支線不對稱。必修。
- `x2r`；類別 F；規則框位於流程右側但沒有任何連線指明它約束 `x2c` 或下一頁的逐工具 remove；一般讀者會把它當孤立註解。選修。

## 未附完整頁面

附件只有 `uninstall（1）` 的 `v1p8bc`；規格與跨頁引用所稱的 `uninstall（2）` 不在本組附件內，因此無法審查其實際刪除順序、config.toml 保護、根 justfile／`.dockerignore` 逐行詢問、`log/` 保留及進度檔最後刪除。

總評：本組頁面目前不能交給使用者看；核心流程仍有多項規格矛盾、跨頁斷點與結果線歧義，尤其自身升級、dev 進度檔及 vk-resolve/1 內容必須先修正。
