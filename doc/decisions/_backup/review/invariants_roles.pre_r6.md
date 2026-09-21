# 審閱頁 01：不變量與角色

本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。

## 一句話目的

下游 repo 把要交付的檔案打成一個純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）；下游使用者在專案裡跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。

## 本頁名詞（第 0 頁沒有的頁內特有詞）

- GHCR：GitHub 的容器 registry；引擎放的地方，也是下游 image 的預設落點（下游 image 公開或私有由下游開發者自決）。
- `config.toml`：`.vendor_kit/config.toml`，VK 的設定檔，進 git；升引擎時比照初始檔三方合併。
- 衝突標記：三方合併合不起來時留在檔內的 `<<<<<<<`／`>>>>>>>` 標記；升版逐檔的結果：沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 三方合併，合不起來就留衝突標記、結束碼 2。
- 交付物：工具 recipe（`just <ns> …`）產生、要交給別人用的東西（例如 deploy 包）。
- 契約檢查腳本：`.vendor_kit/ci/check.sh`，薄殼之一，兩種用法分開：不帶參數 = 下游 CI 的唯一入口（在專案裡跑同步、驗證、試跑升版、工具與專案測試）；`--dist` = 下游開發者在下游 repo 裡驗 `dist/` 佈局與兩平台一致。
- 下游 CI：專案自己的 CI 平台；不是「方」。
- Renovate：下游使用者自選的版本更新機器人；不是「方」。

## 三方角色與承諾關係

| 名稱 | 是誰 | 負責 | 不負責 | 地位 |
|---|---|---|---|---|
| **下游開發者** | 開發下游 repo 的人 | 維護 `dist/` 與三行 Dockerfile；在下游 repo 的 CI 用契約檢查腳本 `--dist` 驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；把下游 image 推到 registry（公開或私有自決；私有時下游使用者要備憑證）；用 dev／undev 在本機開發工具 | 不碰專案的檔；交付物不得依賴 `.vendor_kit/`；交付物的可執行性不由 VK 代驗 | 被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了 |
| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版時 `-y` 只是同意做三方合併，合併後仍有衝突就要手動編輯、再重跑 `upgrade <repo>` 直到乾淨；把契約檢查腳本接進下游 CI | 不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼 | 被承諾方：VK 保證不刪、不覆蓋專案檔，失敗必印原因 |
| **VK** | 我們，vendor_kit 開發者 | 維護引擎與薄殼（含啟動器），履行對兩方的承諾 | 不替工具驗可執行；不 commit、不開 PR；引擎不讀 `.git`、不碰 index、不 `git init` | 承諾方：內部怎麼實作不屬於本契約，可自由變更 |

同一人可兼下游開發者與下游使用者兩種身分。

### 兩個自動化角色（不是「方」）

- 下游 CI：專案自己的 CI 平台（GitHub、GitLab 都一樣）只呼叫契約檢查腳本；腳本自己把 `CI` 設為 1 進 CI 模式，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。
- Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，大版本升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。

## 不變量

- **I1 專案檔四原則**：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（不用工具版本取代客製內容）。
- **I2 自動化只碰不進 git 的東西**：sync（含工具 recipe 執行前自動觸發的那次）只寫 `cache/`、`gen/`（與執行紀錄）；發現薄殼與引擎不符只以 1 結束並提示跑 `upgrade vendor_kit`，不重寫。
- **I3 never fail silently**：失敗一定印原因；需人處理另附可直接複製的下一步指令；warn 也明列條目；印到 tty 的訊息同句進執行紀錄。
- **I4 結束碼語意**：0 成功（含 warn）；1 需人處理或失敗；2 合併衝突（留標記、基準版仍推到新版；update 加 `--exit-code` 時，有新版亦 2）；3 介面版／檔案版不合，須先升級或退回。「回 1 時版本鎖定行不動」適用 add、`upgrade <repo>`、remove、uninstall（寫入前檢查；鎖定行最後才寫／最後才刪）；remove／uninstall 回 1 時留下的狀態 = 該工具仍鎖定、`cache/` 等其餘檔可能部分已刪，進度檔保留、下次可寫動詞先恢復（uninstall 已做完的工具已整個移除、未處理的原樣）；升引擎是唯一例外（引擎那一行已改後才回 1 要求重跑）。多工具動詞的失敗策略依各動詞：upgrade 逐工具做得完的做完；uninstall apply 期間任一工具失敗就中止並列出已完成與未處理的工具；最後都回最需處理的碼（1 > 2 > 0）。
- **I5 回 3 零寫入**：除執行紀錄在啟動時已寫下的開頭記錄外完全不寫——不寫專案檔、不寫 `cache/`、`gen/`、進度檔；新舊一律比介面版／檔案版，不比版本字串；最低介面版檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。
- **I6 需人處理／失敗語意**：需人處理的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。
- **I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；契約檢查腳本自己把 `CI` 設為 1；本機手設 = 唯讀驗證，允許。`-y` 與 CI 模式為獨立開關：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`。CI 模式下升為失敗的警告明列：薄殼不符、基準版落後、未完成接入、任何本機覆寫、需改進 git 的檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`。唯一例外：`update` 在 CI 模式仍查最新版（它是唯讀動詞，查詢就是它的用途）。
- **I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 CI 模式（CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關）。需詢問但無法互動（無 tty／EOF）又沒給 `-y` → 以 1 結束並印出原因（加 `-y` 或在終端執行）；EOF／Ctrl-C = 中止不套用、不記為拒絕過。
- **I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、registry，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。
- **I10 專案根與巢狀**：專案根 = 專案內含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，sync 亦無例外，否則以 1 結束並印出該到哪個目錄執行（工具 recipe 自動觸發的那次 sync 自己先切到專案根，不受影響）。
- **I11 進度檔**：所有可寫動詞（含 dev、第一次 install、升引擎）在第一個寫入前必建進度檔，不設例外；可寫動詞開始前遇未完成交易先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋——它不碰進 git 的檔）；唯讀動詞只偵測不恢復（sync／update 印出未完成交易與恢復指令後以 1 結束，help 印出後仍 0）。
- **I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只預覽不寫的執行）及每次 `bootstrap.sh` 執行（寫在 `log/bootstrap/`）必寫一檔。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可以在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄（不是 git 目錄時也無處可寫）；建目錄＋建檔＋寫開頭記錄失敗 → 1、印出無法寫入的原因、零寫入；引擎啟動記錄寫不進亦同；沒有關掉它的選項。
- **I13 薄殼人不改**：自描述標頭 hash 不符 → 1 列差異不動；重產只由明確動作（install／`upgrade vendor_kit`）做。
- **I14 兩層相容承諾**：救援路徑對任何 ≥ 最低介面版的薄殼永久可用；新版引擎讀歷史 VK 資料永遠可讀、可遷（讀到舊檔案版直接寫成當前檔案版）；舊薄殼呼叫介面版不合的新引擎跑一般動詞，只保證乾淨回 3；最低介面版只能經 ADR 提高。
- **I15 檔案版與未知欄位**：VK 寫的每個 TOML 都有檔案版；讀時忽略未知欄位、重寫仍存在的 TOML 時保留未知欄位（不能保留就拒絕寫；uninstall／remove 合法刪掉整個檔或整個工具項目時不適用）；檔案版高於本引擎支援 → 3 零寫入；讀任一舊檔案版直接寫成當前檔案版，不鏈式遷移。
- **I16 多工具動詞先完整預檢**：會寫檔且一次處理多個工具的動詞（不帶 `<repo>` 的 upgrade、uninstall）先對全部工具預檢完才動任何東西；任一預檢不過 → 整體不動、以 1 結束並列出原因。預檢過了才開始寫，寫的過程中失敗適用 I4（失敗策略依各動詞、進度檔保留）。
- **I17 `gen/tools.just` 與 `cache/` 同次原子替換**：`tools.just` 在同一次寫入裡最後寫，並與 `cache/` 一起原子替換，任何時刻都不會出現「工具入口指向不存在或半套的 cache」。
- **I18 版本鎖定行唯一正規形**：形式照第 0 頁「版本鎖定行」：引擎行在頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`、工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。`<repo>` 照第 0 頁名稱規則（小寫、不含句點，能作未加引號的 TOML 鍵），與頂層 `schema`／`written_by`／`vendor_kit` 不同層、不撞名。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。

## 例外清單（不變量的明文例外）

- 根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\t@just --list`）；有 → 問後加 import 一行；uninstall 只刪完全相同的行。
- 根 `.dockerignore`（I1「永不刪」的明文例外）：install 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；只有 uninstall、經詢問、且該行原文仍與 VK 當初寫的相同時，才逐行刪；被改過或缺失的行跳過並 warn。
- 初始檔換版／三方合併：已納管初始檔經同意（或 `-y`）換新版或三方合併；衝突留標記回 2、基準版推到新版；`config.toml` 對 `upgrade vendor_kit` 比照。
- append 型初始檔：問後加入並記錄實際插入的行；升版只對可辨識的上次插入行提修改；零命中或多處 → 保留只 warn，`-y` 不硬加。
- 新版刪除的初始檔：只 warn 不刪。
- `log/`：VK 檔，不受專案檔四原則；`bootstrap.sh`／第一次 install 失敗清半成品時 `log/` 保留；uninstall 一律保留 `log/`（`.vendor_kit/` 只剩 `log/`）。
- 進度檔與 `.tmp.*`：同上不受專案檔四原則；成功即刪；prune 遇活躍者只列出提示、不刪、不恢復、不阻擋（I11 的明文例外）。
- 零寫入的執行紀錄例外：見 I5。

## 本頁待拍板

無；四點已定（2026-09-20）：
1. 禁巢狀：install 時上層或下層已有 `.vendor_kit/` 都以 1 結束（I10）。
2. 執行位置：動詞只准在專案根執行，sync 亦無例外；自動觸發的那次 sync 自己先切到專案根（I10）。
3. `-y` 與 CI 模式是兩個獨立開關：CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關；`-y` 只省略詢問（I7／I8）。
4. 顏色語意：橙 = 需人處理、紅 = 失敗（I6）。

其餘三條原列矛盾（零寫入的執行紀錄例外、根 `.dockerignore` 四行、舊薄殼跑介面版不合的新引擎回 3）維持規格所載。規格仍待定的三項（啟動器讀設定檔的方式、外部 repo 反向採用紀錄腳本、紀錄事件名清單待審）不在本頁範圍。

## 出處對照（條號 → 來源）

來源檔：spec = `decisions/interface_spec.md` v3.5；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`；codex = `decisions/review/codex_findings_00_02.md`；codex r2 = `decisions/review/codex_findings_00_02_r2.md`；codex r3 = `decisions/review/codex_findings_00_02_r3.md`；codex r4 = `decisions/review/codex_findings_00_02_r4.md`。來源原文用的是舊詞（工具 repo、下游專案、鎖定行、frozen、進度日誌、操作紀錄檔、協定號／schema 號／floor…），對照第 0 頁的新名。

| 條目 | 來源 |
|---|---|
| 一句話目的 | spec 文首、§4.7；grilling Q1、Q21；公開或私有自決 = codex r2 N1 |
| 三方角色表 | spec §3.1、§4.5、§4.7、§7.1、§7.2、§7.3；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則與名詞定案（2026-09-20）；`--dist` 與下游 CI 入口分開 = codex #17；衝突要手動編輯再重跑 = codex #18、spec §1.2 upgrade 結束碼 2；「交付物的可執行性」= codex r3 R4 |
| 兩個自動化角色 | spec §7.1、§7.3；grilling CI 平台定案、相容性其餘採納（Renovate major 分開 PR） |
| 名詞：`config.toml`、衝突標記 | spec §0、§4.6、§4.9；v2.12 L3′；grilling Q6、Q12、Q13（append 型／copy 型初始檔已移至第 0 頁「初始檔」= codex r4 S5） |
| 名詞：交付物、契約檢查腳本 | spec §4.7、§7.1、§7.2；grilling deploy 包定案 |
| I1 | grilling 隔離題定案；spec §0 |
| I2 | grilling Q10；spec §0、§1.2 sync、§3.6 |
| I3 | spec §0、§4.10、§6；grilling Q6；失敗只保證原因 = codex #19 |
| I4 | grilling Q23、Q27、「codex 修正後的 12 個疑慮取捨」（remove／uninstall 鎖定行最後刪）；spec §1.2 remove／uninstall、§2；適用動詞明列 = codex #20；失敗策略依各動詞 = codex r2 N8 |
| I5 | grilling Q23；spec §0、§2；例外 = v2.13 P12；完全不寫 = codex #21 |
| I6 | grilling 2026-09-20、01 頁拍板 (4)；v2.10-1；spec §0「結束的兩種語意」、§6 類別欄 |
| I7 | grilling 16 條必修、Q5、Q15、01 頁拍板 (3)、02 頁 6 點定案 ①；spec §0；check.sh `export CI=1` = spec §7.1；update 例外 = codex #22 |
| I8 | grilling 16 條必修、Q13、19 條-6、01 頁拍板 (3)；spec §0（訊息 6-4） |
| I9 | grilling deploy 包定案、Q14；spec §4.7 |
| I10 | grilling Q20 定案（改）、Q20 修正、01 頁拍板 (1)(2)；spec §0（訊息 6-9、6-35；sync 豁免已撤回） |
| I11 | grilling 進度日誌條、2026-09-20（v2.11-1、v2.10-6）、新規則 (b)；spec §0（訊息 6-33）；第一次 install 也建 = v2.13 P5；dev 也建 = codex #23／#47；prune 例外 = spec §0 進度檔「prune 特例」、codex r2 N7 |
| I12 | grilling 2026-09-20 新需求、L1–L6 定案、新規則 (a)；v2.12 L4；spec §0、§4.10（訊息 6-38）；順序 = codex #8／#26；含 bootstrap.sh = codex r3 R9、spec §4.10 |
| I13 | grilling Q10、Q17；spec §4.5、§8-6；「自描述標頭」= codex r4 S2 |
| I14 | grilling Q16、Q23；spec §3.5、§8-3～5；限定語 = codex #27／#28 |
| I15 | spec §4 通則、§8-7；grilling 補三條不變量；codex #30；限定「重寫仍存在的 TOML」= codex r2 N9 |
| I16 | spec §1.2 upgrade（不帶 repo 先完整預檢）、§1.2 uninstall（先預檢全部工具）；grilling 補三條不變量；codex #32 |
| I17 | spec §4.4 `gen/tools.just`、§8-9；grilling 補三條不變量；codex #33 |
| I18 | spec §4.1 版本鎖定行契約；codex #31（r2 判未修）、codex r2 #31；引用第 0 頁、`[tools]` 表與 `<repo>` 名稱規則 = codex r3 R1–R3、grilling「00–02 codex 三審新定案」 |
| 例外：根 justfile | grilling 隔離題 A、16 條必修；spec §4.5 |
| 例外：根 `.dockerignore` | grilling Q22 補（三行）；第四行 = v2.13 P13；spec §4.5；標明只在 uninstall 逐行刪 = codex #29 |
| 例外：初始檔換版／三方合併 | grilling 隔離題 C；v2.12 L3′；spec §0 |
| 例外：append 型初始檔 | grilling Q6、Q12、Q13 |
| 例外：新版刪除的初始檔 | grilling 第 1 頁便條回覆 |
| 例外：`log/` | v2.12 L1；v2.13 P4、P6；spec §0、§1.2、§4.10 |
| 例外：進度檔與 `.tmp.*` | spec §0、§4.6；prune 例外 = codex r2 N7 |
| 本頁待拍板（四點已定） | grilling「01 頁四點拍板（2026-09-20）」；spec §9.1 P1–P3 |
| 原矛盾 1–7（已解） | 1、2、3、4 = 01 頁四點拍板 2026-09-20（grilling「01 頁四點拍板」；spec §0、§2、§6）；5、6、7 維持 spec（v2.13 P12、P13；§2、§8-5） |
