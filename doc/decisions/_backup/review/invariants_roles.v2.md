# 審閱頁 01：不變量與角色

本頁是契約的第一頁，自足：只用本頁定義的名詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。

## 一句話目的

工具 repo 把要交付的檔案打成一個純資料的容器 image 公開；下游專案跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。vendor_kit 只負責搬移，不承諾搬來的內容可執行。

## 本頁名詞（其餘見 CONTEXT.md）

- 工具 repo：提供工具的 git repo；`<repo>` 是它的名字。它把 `dist/`（要交付的檔案、初始檔宣告、just 命名空間檔 `<ns>.just`，`<ns>` 是工具的 just 命名空間）用三行 Dockerfile 打成 `FROM scratch` 的純資料 image，推到 GHCR（GitHub 的容器 registry）。
- 引擎 image：vendor_kit 的主程式，也是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。
- 專案根：含 `.vendor_kit/` 的目錄；不是 git toplevel。
- 薄殼：`.vendor_kit/` 內進 git、由引擎產、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；首行自描述 `# vendor_kit-shell/<協定號> engine=<引擎版> sha256=<其餘內容的 hash>`。
- 啟動器：薄殼內的 POSIX sh 片段，負責起引擎容器；`bootstrap.sh` = 第一次接入時的啟動器。
- 動詞：`just vendor_kit <動詞>` 的動詞。本頁提到的：install（接入／修復）、add（加工具）、upgrade（升版；`upgrade vendor_kit` = 升引擎與薄殼）、sync（把鎖定的版本同步到本機）、update（只查有沒有新版，不寫檔）、uninstall、prune（清舊 image 與殘留）、help。
- 鎖定行：`.vendor_kit/version.toml` 內每個工具（與引擎）一行 `<tag>@<digest>`；進 git。
- `cache/`、`gen/`：`.vendor_kit/` 內不進 git 的兩個目錄；cache/ 放工具內容的本機副本，gen/ 放引擎產生、供 just 載入的檔。
- 使用者的檔：專案內非 vendor_kit 自產的一切（根 justfile、根 `.dockerignore`、初始檔落點、其他原有檔）。
- 初始檔：工具在 `dist/` 內宣告、`add` 時複製（copy）或插入幾行（append）進專案的檔；vendor_kit 另存一份原版副本（baseline）在 `.vendor_kit/baseline/<repo>/`，升版時拿「舊原版／新原版／使用者現況」做三方合併。
- 納管：初始檔經使用者同意建立後，vendor_kit 記下它的來源與狀態；拒絕建立也會記下（拒絕過）。
- 進度日誌：可寫動詞的交易紀錄（`.vendor_kit/.tmp.<動詞>.<id>.toml` 或記在工具的紀錄檔內），成功即刪；用來中斷後恢復。
- 操作紀錄檔：`.vendor_kit/log/<動詞>/<時間戳>-<id>.jsonl`，每次執行一檔，不進 git，事後追溯用。
- frozen：環境變數 `CI` 為真時的模式：不寫任何進 git 的檔、不查最新版。
- 協定號／schema 號／floor：協定號 = 薄殼與引擎之間的整數版號；schema 號 = vendor_kit 自己寫的每個檔的格式版號；floor = 引擎仍支援的最低協定號，固定常數。三者都與版本字串無關。
- 結束碼：0 成功、1 一般失敗或需人動作、2 合併衝突、3 版本／協定／schema 不合。

## 三方角色與承諾關係

| 角色 | 是誰 | 負責 | 不負責 | 在這份契約裡的地位 |
|---|---|---|---|---|
| 工具 repo | 提供工具的人 | 維護 `dist/` 與三行 Dockerfile；用 vendor_kit 出貨的檢查腳本驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；image 公開與否自決 | 不碰下游專案的檔；交付物不得依賴 `.vendor_kit/`；binary 可執行性不由 vendor_kit 代驗 | 被承諾方：只要照 `dist/` 契約出貨，vendor_kit 保證搬得到、鎖得住、升得了 |
| 下游專案 | 用工具的專案維護者 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與 `version.toml`；本機跑 `upgrade <repo> -y` 解合併衝突 | 不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼 | 被承諾方：vendor_kit 保證不刪、不覆蓋它的檔，失敗必印原因 |
| vendor_kit 開發者（我們） | 維護 vendor_kit 的人 | 維護引擎 image 與薄殼（啟動器） | 不替工具驗可執行；不 commit、不開 PR；引擎不讀 `.git`、不碰 index、不 `git init` | 承諾方：維護引擎 image 與薄殼（啟動器），履行對工具 repo 與下游專案的承諾；內部怎麼實作不屬於本契約，可自由變更 |

### 兩個自動化角色（不是「方」）

- 下游 CI：下游專案自己的 CI 平台（GitHub、GitLab 都一樣）跑薄殼裡那支腳本；腳本自己把 `CI` 設為 1 進 frozen，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。
- Renovate：下游自選的版本更新機器人，用 vendor_kit 提供的設定；它開的 PR 只改鎖定行，major 升版分開 PR。初始檔的合併不由它做——維護者本機補完再 push。vendor_kit 本身沒有機器人。

## 不變量

- **I1 使用者檔四原則**：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（不用工具版本取代客製內容）。
- **I2 自動化只碰不進 git 的東西**：sync（含工具 recipe 執行前自動觸發的那次）只寫 `cache/`、`gen/`（與操作紀錄檔）；發現薄殼與引擎不符只以 1 結束並提示跑 `upgrade vendor_kit`，不重寫。
- **I3 never fail silently**：每個失敗都印訊息並附可直接複製的指令；warn 也明列條目；印到 tty 的訊息同句進操作紀錄檔。
- **I4 結束碼語意**：0 成功（含 warn）；1 一般失敗或需人動作（工具層動詞回 1 時鎖定行不動）；2 合併衝突（留標記、baseline 仍推到新版；update 被要求以結束碼回報時，有新版亦 2）；3 版本／協定／schema 不合，須先升級或退回。多工具動詞做得完的做完，最後回最需處理的碼（1 > 2 > 0）。
- **I5 回 3 零寫入**：不寫任何專案檔；新舊一律比協定號／schema 號，不比版本字串；floor 檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。唯一例外：操作紀錄檔在啟動時已寫下的開頭記錄不算寫入。
- **I6 橙／紅語意**：需人動作的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。
- **I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ frozen；下游 CI 用的那支腳本自己把 `CI` 設為 1。frozen 下升為失敗的警告明列：薄殼不符、baseline 落後、未完成接入、任何本機覆寫、需改進 git 的檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`；update 唯讀不受影響。
- **I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 frozen。需詢問但無法互動（無 tty／EOF）又沒給 `-y` → 以 1 結束並印出原因（加 `-y` 或在終端執行）；EOF／Ctrl-C = 中止不套用、不記為拒絕過。
- **I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、GHCR，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。
- **I10 專案根與巢狀**：專案根 = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，否則以 1 結束並印出該到哪個目錄執行（sync 豁免）。
- **I11 進度日誌**：每個可寫動詞第一個寫入前必建（含第一次 install、`upgrade vendor_kit`），不設例外；可寫動詞開始前遇未完成交易先恢復再繼續；唯讀動詞只偵測不恢復（sync／update 印出未完成交易與恢復指令後以 1 結束，help 印出後仍 0）。
- **I12 操作紀錄檔**：每個動詞每次執行（含 help、沒起容器的 sync、只試跑不寫的 `--dry-run`）必寫一檔；啟動器在任何其他動作之前建目錄＋建檔＋寫開頭記錄，失敗 → 1、印出無法寫入的原因、零寫入；引擎啟動記錄寫不進亦同；沒有關掉它的選項。
- **I13 薄殼人不改**：薄殼首行 hash 不符 → 1 列差異不動；重產只由明確動作（install／`upgrade vendor_kit`）做。
- **I14 兩層相容承諾**：救援路徑（install、`upgrade vendor_kit`、sync 的不符提示、help；單段 docker run，不依賴 `gen/`）對任何 ≥ floor 的薄殼永久可用；舊資料永遠可讀、可遷；舊薄殼跑新 major 的一般動詞只保證乾淨回 3；floor 只能經 ADR 提高。

## 例外清單（不變量的明文例外）

- 根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\t@just --list`）；有 → 問後加 import 一行；uninstall 只刪完全相同的行。
- 根 `.dockerignore`：install 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；uninstall 問後逐行只刪原文相同行。
- 初始檔換版／三方合併：已納管初始檔經同意（或 `-y`）換新版或三方合併；衝突留標記回 2、baseline 推到新版；`.vendor_kit/config.toml`（vendor_kit 的設定檔，進 git）對 `upgrade vendor_kit` 比照。
- append 型初始檔：問後加入並記錄實際插入的行；升版只對可辨識的上次插入行提修改；零命中或多處 → 保留只 warn，`-y` 不硬加。
- 新版刪除的初始檔：只 warn 不刪。
- `log/`：vendor_kit 自己的檔，不受四原則；`bootstrap.sh`／第一次 install 失敗清半成品時 `log/` 保留；uninstall 一律保留 `log/`（`.vendor_kit/` 只剩 `log/`）。
- 進度日誌與 `.tmp.*`：同上不受四原則；成功即刪；prune 不刪活躍者。
- 零寫入的操作紀錄檔例外：見 I5。

## 本頁待拍板

規格仍待定的三項（啟動器讀設定檔的方式、外部 repo 反向採用紀錄腳本、紀錄事件名清單待審）都不在本頁範圍。
提醒：以下四項是主對話依既定原則定案、使用者可否決：失敗與 uninstall 保留 `log/`；第一次 install 也建進度日誌；零寫入的操作紀錄檔例外；根 `.dockerignore` 第四行。

兩份來源有出入、未取捨、請拍板：

| # | 條目 | 討論紀錄 | 規格 |
|---|---|---|---|
| 1 | I6 橙／紅語意 | 「需人動作的 1 結束一律橙；橙 = 1 或 3 且印指令、2 也橙；紅 = 失敗」 | 未載此語意（全文無「橙」） |
| 2 | I10 禁巢狀範圍 | 「install 時**上層**已有 `.vendor_kit/` → 1」 | 「上層**或下層**已有 → 1」 |
| 3 | I10 執行位置 | 「動詞只准在含 `.vendor_kit/` 的那一層執行」，無例外 | 「sync 豁免此檢查」 |
| 4 | I7／I8 CI 與 `-y` | 早期：「CI **無 `-y`** 需改檔 → 1 印清單」 | 「需改進 git 的檔 → 1，**與 `-y` 無關**；`-y` 不解除 frozen」（討論紀錄後期亦如此，前後兩說） |
| 5 | I5 零寫入 | 「回 3 時零寫入」，無例外 | 「操作紀錄檔例外」（主對話結案、可否決） |
| 6 | 例外：`.dockerignore` 行數 | 「三行」 | 四行（加 `.vendor_kit/log/`） |
| 7 | I14 舊薄殼跑新 major | 「回 1」→ 後來改為 3（討論紀錄內已自行更正） | 回 3；列出僅供確認 |

## 出處對照（條號 → 來源）

來源檔：spec = `decisions/interface_spec.md` v3.1；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`。

| 條目 | 來源 |
|---|---|
| 一句話目的 | spec 文首、§4.7；grilling Q1、Q21 |
| 三方角色表 | spec §3.1、§4.5、§4.7；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則（2026-09-20） |
| 兩個自動化角色 | spec §7.1、§7.3；grilling CI 平台定案、相容性其餘採納（Renovate major 分開 PR） |
| 名詞：薄殼五檔、首行 | spec §4.5；grilling Q17；v2.13 P9、v2.14-1 |
| 名詞：進度日誌、操作紀錄檔、config.toml | spec §0、§4.6、§4.9、§4.10；v2.12 L1–L5 |
| 名詞：協定號／schema／floor、結束碼 | spec §2、§8-2、§8-3、§8-7；grilling Q16、Q23 |
| I1 | grilling 隔離題定案；spec §0 |
| I2 | grilling Q10；spec §0、§1.2 sync、§3.6 |
| I3 | spec §0、§4.10、§6；grilling Q6 |
| I4 | grilling Q23、Q27；spec §2 |
| I5 | grilling Q23；spec §0、§2；例外 = v2.13 P12 |
| I6 | grilling 2026-09-20；v2.10-1（spec 未載） |
| I7 | grilling 16 條必修、Q5、Q15；spec §0；check.sh `export CI=1` = spec §7.1 |
| I8 | grilling 16 條必修、Q13、19 條-6；spec §0（訊息 6-4） |
| I9 | grilling deploy 包定案、Q14；spec §4.7 |
| I10 | grilling Q20 定案（改）、Q20 修正；spec §0（訊息 6-9；sync 豁免 = review F1；上下層 = review I-47） |
| I11 | grilling 進度日誌條、2026-09-20（v2.11-1、v2.10-6）；spec §0（訊息 6-33）；第一次 install 也建 = v2.13 P5 |
| I12 | grilling 2026-09-20 新需求、L1–L6 定案；v2.12 L4；spec §0、§4.10（訊息 6-38） |
| I13 | grilling Q10、Q17；spec §4.5、§8-6 |
| I14 | grilling Q16、Q23；spec §3.5、§8-3～5 |
| 例外：根 justfile | grilling 隔離題 A、16 條必修；spec §4.5 |
| 例外：根 `.dockerignore` | grilling Q22 補（三行）；第四行 = v2.13 P13；spec §4.5 |
| 例外：初始檔換版／三方合併 | grilling 隔離題 C；v2.12 L3′；spec §0 |
| 例外：append 型初始檔 | grilling Q6、Q12、Q13 |
| 例外：新版刪除的初始檔 | grilling 第 1 頁便條回覆 |
| 例外：`log/` | v2.12 L1；v2.13 P4、P6；spec §0、§1.2、§4.10 |
| 例外：進度日誌與 `.tmp.*` | spec §0、§4.6 |
| 待拍板：三項待定／可否決四項 | spec §9.1 P1–P3；v2.13 P4、P6、P5、P12、P13 |
| 矛盾 1 | grilling 2026-09-20、v2.10-1 ↔ spec §0／§2 |
| 矛盾 2 | grilling Q20 定案（改）↔ spec §0（review I-47） |
| 矛盾 3 | grilling Q20 修正 ↔ spec §0（review F1） |
| 矛盾 4 | grilling 隔離題 C ↔ spec §0、grilling 16 條必修 |
| 矛盾 5 | grilling Q23 ↔ spec §0／§4.10（v2.13 P12） |
| 矛盾 6 | grilling Q22 補 ↔ spec §4.5（v2.13 P13） |
| 矛盾 7 | grilling Q16 → Q23 ↔ spec §2、§8-5（§11-1） |
