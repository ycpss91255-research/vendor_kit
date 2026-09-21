OpenAI Codex v0.155.0
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 01a0b9d4-3c9e-74b0-bbd1-e980d7775595
--------
user
你是設計審查員。vendor_kit 是一個工具：下游 repo 把 dist/ 打成純資料容器 image，下游專案用 bootstrap.sh + `just vendor_kit <動詞>` 取得工具、鎖版本、三方合併初始檔。我們正在由外而內審對外契約：附件 A 是全域名詞（第 0 頁）、B 是不變量與三方角色（第 1 頁）、C 是動詞介面表（第 2 頁）；D 是規格正本 §0–§2；E 是最近定案。審閱規則：頁 N 只能用第 0 頁與前面頁定義的詞、不得引用後面的頁；名詞一律用第 0 頁的新名（下游開發者／下游使用者／VK、版本鎖定行、基準版、進度檔、執行紀錄、CI 模式、需人處理／失敗、介面版／檔案版／最低介面版…）。
請逐頁找：(1) 定義不清或互相矛盾（含 A/B/C 之間、以及與 D 規格的矛盾）；(2) 違反「不前引」的地方；(3) 遺漏的重要不變量或動詞行為（對照 D）；(4) 名詞表有沒有漏定義卻被用到的詞；(5) 一般人讀不懂的句子。每條給頁與條目（id 或引文）與一句說明，標必修／選修。
另外請對 C 頁末尾「本頁待拍板」6 點各給一個明確答案與理由（主對話的建議：① CI 模式定義加「update 除外」；② 驗收 harness 明確 CI=0；③ 其餘動詞靠通則不逐一寫死；④ prune 保留清單含本機覆寫引用的 image；⑤ 內部子命令 materialize 改名對齊 fetch；⑥ 第 0 頁 update 改「只寫執行紀錄」——同意或反對都要說理由）。最後一句總評：這三頁能否交給使用者定稿。

請以繁體中文回答，格式：逐條列出 {頁, 條目 id 或引文, 類別（矛盾／定義不清／前引違規／遺漏／建議）, 一句說明, 必修／選修}；接著「6 點判定」每點一行（答案＋理由）；最後一句「總評」。

==================================================
附件 A：00 名詞與縮寫（decisions/review/00_terms.md）
==================================================
# 審閱頁 00：名詞與縮寫

本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。

## 三方與承諾關係

| 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
|---|---|---|---|
| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；本機解合併衝突 | 被承諾方 |
| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |

同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。

## VK 組件（component）

VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。

- **引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。
- **薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`），首行自描述引擎版與內容 hash。
- **啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。

### VK 模組（module）——引擎內的 8 個程式單元

| 中文名 | 英文代號 | 做什麼 |
|---|---|---|
| 版本解析 | `resolve` | 讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔 |
| 取件 | `fetch` | 把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記 |
| 初始檔合併 | `initfile` | 依工具宣告建初始檔、存基準版、升版時做三方合併 |
| 薄殼產生 | `shell` | 產生或重產薄殼五檔與自描述首行，並比對薄殼是否被改 |
| 進度與寫入 | `progress` | 建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續 |
| 設定與格式 | `schema` | 讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml` |
| 紀錄 | `log` | 每次執行寫一份執行紀錄 |
| 清理 | `prune` | 找出版本鎖定行未引用的舊 image、殘留容器與暫存並刪除 |

## 常用詞

| 中文名 | 英文 | 定義 |
|---|---|---|
| **專案檔** | project file | 專案內不是 VK 自產的一切：根 `justfile`、根 `.dockerignore`、建立後的初始檔、其他原有檔 |
| **VK 檔** | VK file | VK 自己建、自己管的檔：`.vendor_kit/` 內的 `version.toml`、`config.toml`、薄殼、基準版、`cache/`、`gen/`、進度檔、執行紀錄 |
| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行 `<repo> = "…:<tag>@sha256:<digest>"`；進 git；只有這行決定裝哪一版 |
| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時複製（copy）或插入幾行（append）進專案的檔；建立後歸下游使用者、進 git |
| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時當三方合併的第三份 |
| **進度檔** | progress file | 可寫動詞的交易紀錄 `.vendor_kit/.tmp.<verb>.<id>.toml`（或記在基準版旁的 metadata）；成功即刪；中斷後下次可寫動詞先恢復再繼續 |
| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞每次執行一檔；不進 git；事後追溯用；寫不進就不做任何事 |
| **CI 模式** | CI mode | 環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版 |
| **需人處理** | needs human | 動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色 |
| **失敗** | failure | 拉不到、寫不進、驗證不過這類無法繼續的結束；結束碼 1；圖上紅色 |
| **專案檔四原則** | four rules | ① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容） |
| **介面版** | protocol version | 薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關 |
| **檔案版** | schema version | VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔 |
| **最低介面版** | floor | 引擎仍支援的最低介面版；固定常數；只能經 ADR 提高 |
| **結束碼** | exit code | `0` 成功（含 warn）；`1` 一般失敗或需人處理；`2` 合併衝突（留標記）；`3` 介面版／檔案版不合，先升級或退回，零寫入 |
| **佔位符** | placeholder | `<repo>` 下游 repo 名；`<ns>` 工具的 just 命名空間；`<tag>` image 版本名；`<digest>` image 內容指紋 `sha256:…` |

### 其他既有詞

| 中文名 | 英文 | 定義 |
|---|---|---|
| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 GHCR |
| **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
| **專案根** | project root | 含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
| **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔 |
| **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest，之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
| **納管** | managed | 初始檔經下游使用者同意建立後，VK 記下它的來源與狀態；拒絕建立也記（拒絕過） |
| **自描述首行** | self-describing header | 薄殼每檔首行 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；引擎重算比對，不符就不動 |
| **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫（install、升引擎、sync 的不符提示、help）；任何 ≥ 最低介面版的薄殼永久可用 |

## 語法記法

動詞表與後頁的指令寫法一律照這張表。

| 記法 | 意思 |
|---|---|
| `<x>` | 必填佔位符 |
| `[x]` | 可省略 |
| `[@<tag>]` | 可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`） |
| `-x <值>`／`--long <值>` | 短／長選項等價；只有常用的才有短的 |
| `-y` | 不帶值的開關 |
| `a／b` | 二選一 |

動詞表用到的選項：

- `-p <dir>`：把工具指到本機目錄。
- `-i <tag>`：把引擎指到本機 image。
- `--exit-code`：有新版時以結束碼 2 回報，而不是只印出來。
- `-y`：省略詢問，視同回答「是」。

## 動詞

寫法：小寫原文，前面省略 `just vendor_kit`。

| 動詞 | 做什麼 |
|---|---|
| `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`，根 `justfile` 加一行；再跑 = 冪等修復；不做 `git init` |
| `uninstall` | 對稱移除 VK 自產的檔與根 `justfile` 那一行；初始檔不刪只印清單；執行紀錄保留 |
| `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
| `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
| `update [<repo>]` | 只查有沒有新版，不寫任何檔；`--exit-code` 有新版回 2 |
| `upgrade [<repo>[@<tag>]]` | 升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行 |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 把工具指到本機目錄（或引擎指到本機 image）；只寫 `version.local.toml`；工具須已在版本鎖定行 |
| `undev <repo>`／`undev vendor_kit` | 撤銷 dev，回到版本鎖定行的版本 |
| `sync [<repo>]` | 依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發 |
| `prune` | 刪版本鎖定行未引用的舊 image、殘留容器／network／volume 與暫存 |
| `help` | 印命名空間層說明；不觸網、不寫檔（執行紀錄除外） |

**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。

---

記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。

## 附錄（將移至他處）

以下兩節原文暫留於此供審閱者參照；定稿時「寫法約定」移到主圖第 0 頁「圖例與記法」，「規則」移到 AGENTS.md。

### 寫法約定

- 「→ 1：X」= 以結束碼 1 結束並印出 X；「→ 0」= 以結束碼 0 結束。「→ 2」「→ 3」同理。
- 圖上顏色：**藍** = 引擎做；**白** = 啟動器做；**綠** = 結束碼 0；**橙** = 需人處理；**紅** = 失敗；**白虛線橢圓** = 來自其他頁的節點。

### 規則

1. 每頁只用本頁定義的詞；本頁沒有的詞不得在後頁出現。
2. 頁 N 不引用之後的頁。
3. 各頁的名詞表只列該頁特有的詞，不重複本頁。


==================================================
附件 B：01 不變量與角色（decisions/review/01_invariants_roles.md）
==================================================
# 審閱頁 01：不變量與角色

本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。

## 一句話目的

下游 repo 把要交付的檔案打成一個純資料的下游 image 公開；下游使用者跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。

## 本頁名詞（第 0 頁沒有的頁內特有詞）

- GHCR：GitHub 的容器 registry；下游 image 與引擎放的地方。
- `config.toml`：`.vendor_kit/config.toml`，VK 的設定檔，進 git；升引擎時比照初始檔三方合併。
- 三方合併／衝突標記：升版對每個納管初始檔拿基準版、現況、新版三份合併；沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 檔內留衝突標記、結束碼 2。
- append 型初始檔：`strategy = append` 的初始檔，`add` 時把幾行插進專案既有檔而不是整檔複製。
- 本機覆寫：`version.local.toml` 內由 dev 寫的那一行；不進 git；有就優先於版本鎖定行。
- 交付物：工具 recipe（`just <ns> …`）產生、要交給別人用的東西（例如 deploy 包）。
- 契約檢查腳本：`.vendor_kit/ci/check.sh`，薄殼之一；下游 CI 只呼叫它。
- 下游 CI：下游使用者專案自己的 CI 平台；不是「方」。
- Renovate：下游使用者自選的版本更新機器人；不是「方」。

## 三方角色與承諾關係

| 名稱 | 是誰 | 負責 | 不負責 | 地位 |
|---|---|---|---|---|
| **下游開發者** | 開發下游 repo 的人 | 維護 `dist/` 與三行 Dockerfile；用契約檢查腳本驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；下游 image 公開與否自決；用 dev／undev 在本機開發工具 | 不碰下游使用者專案的檔；交付物不得依賴 `.vendor_kit/`；binary 可執行性不由 VK 代驗 | 被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了 |
| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；本機跑 `upgrade <repo> -y` 解合併衝突 | 不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼 | 被承諾方：VK 保證不刪、不覆蓋專案檔，失敗必印原因 |
| **VK** | 我們，vendor_kit 開發者 | 維護引擎與薄殼（含啟動器），履行對兩方的承諾 | 不替工具驗可執行；不 commit、不開 PR；引擎不讀 `.git`、不碰 index、不 `git init` | 承諾方：內部怎麼實作不屬於本契約，可自由變更 |

同一人可兼下游開發者與下游使用者兩種身分。

### 兩個自動化角色（不是「方」）

- 下游 CI：下游使用者專案自己的 CI 平台（GitHub、GitLab 都一樣）跑契約檢查腳本；腳本自己把 `CI` 設為 1 進 CI 模式，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。
- Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，major 升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。

## 不變量

- **I1 專案檔四原則**：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（不用工具版本取代客製內容）。
- **I2 自動化只碰不進 git 的東西**：sync（含工具 recipe 執行前自動觸發的那次）只寫 `cache/`、`gen/`（與執行紀錄）；發現薄殼與引擎不符只以 1 結束並提示跑 `upgrade vendor_kit`，不重寫。
- **I3 never fail silently**：每個失敗都印訊息並附可直接複製的指令；warn 也明列條目；印到 tty 的訊息同句進執行紀錄。
- **I4 結束碼語意**：0 成功（含 warn）；1 一般失敗或需人處理（工具層動詞回 1 時版本鎖定行不動）；2 合併衝突（留標記、基準版仍推到新版；update 加 `--exit-code` 時，有新版亦 2）；3 介面版／檔案版不合，須先升級或退回。多工具動詞做得完的做完，最後回最需處理的碼（1 > 2 > 0）。
- **I5 回 3 零寫入**：不寫任何專案檔；新舊一律比介面版／檔案版，不比版本字串；最低介面版檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。唯一例外：執行紀錄在啟動時已寫下的開頭記錄不算寫入。
- **I6 需人處理／失敗語意**：需人處理的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。
- **I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；契約檢查腳本自己把 `CI` 設為 1；本機手設 = 唯讀驗證，允許。`-y` 與 CI 模式為獨立開關：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`。CI 模式下升為失敗的警告明列：薄殼不符、基準版落後、未完成接入、任何本機覆寫、需改進 git 的檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`；update 唯讀不受影響。
- **I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 CI 模式（`-y` 與 CI 模式為獨立開關；CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關）。需詢問但無法互動（無 tty／EOF）又沒給 `-y` → 以 1 結束並印出原因（加 `-y` 或在終端執行）；EOF／Ctrl-C = 中止不套用、不記為拒絕過。
- **I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、GHCR，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。
- **I10 專案根與巢狀**：專案根 = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，sync 亦無例外，否則以 1 結束並印出該到哪個目錄執行（工具 recipe 自動觸發的那次 sync 自己先切到專案根，不受影響）。
- **I11 進度檔**：每個可寫動詞第一個寫入前必建（含第一次 install、`upgrade vendor_kit`），不設例外；可寫動詞開始前遇未完成交易先恢復再繼續；唯讀動詞只偵測不恢復（sync／update 印出未完成交易與恢復指令後以 1 結束，help 印出後仍 0）。
- **I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只試跑不寫的 `--dry-run`）必寫一檔；啟動器在任何其他動作之前建目錄＋建檔＋寫開頭記錄，失敗 → 1、印出無法寫入的原因、零寫入；引擎啟動記錄寫不進亦同；沒有關掉它的選項。
- **I13 薄殼人不改**：自描述首行 hash 不符 → 1 列差異不動；重產只由明確動作（install／`upgrade vendor_kit`）做。
- **I14 兩層相容承諾**：救援路徑（install、`upgrade vendor_kit`、sync 的不符提示、help；單段 docker run，不依賴 `gen/`）對任何 ≥ 最低介面版的薄殼永久可用；舊資料永遠可讀、可遷；舊薄殼跑新 major 的一般動詞只保證乾淨回 3；最低介面版只能經 ADR 提高。

## 例外清單（不變量的明文例外）

- 根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\t@just --list`）；有 → 問後加 import 一行；uninstall 只刪完全相同的行。
- 根 `.dockerignore`：install 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；uninstall 問後逐行只刪原文相同行。
- 初始檔換版／三方合併：已納管初始檔經同意（或 `-y`）換新版或三方合併；衝突留標記回 2、基準版推到新版；`config.toml` 對 `upgrade vendor_kit` 比照。
- append 型初始檔：問後加入並記錄實際插入的行；升版只對可辨識的上次插入行提修改；零命中或多處 → 保留只 warn，`-y` 不硬加。
- 新版刪除的初始檔：只 warn 不刪。
- `log/`：VK 檔，不受專案檔四原則；`bootstrap.sh`／第一次 install 失敗清半成品時 `log/` 保留；uninstall 一律保留 `log/`（`.vendor_kit/` 只剩 `log/`）。
- 進度檔與 `.tmp.*`：同上不受專案檔四原則；成功即刪；prune 不刪活躍者。
- 零寫入的執行紀錄例外：見 I5。

## 本頁待拍板

無；四點已定（2026-09-20）：
1. 禁巢狀：install 時上層或下層已有 `.vendor_kit/` 都以 1 結束（I10）。
2. 執行位置：動詞只准在專案根執行，sync 亦無例外；自動觸發的那次 sync 自己先切到專案根（I10）。
3. `-y` 與 CI 模式是兩個獨立開關：CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關；`-y` 只省略詢問（I7／I8）。
4. 顏色語意：橙 = 需人處理、紅 = 失敗（I6）。

其餘三條原列矛盾（零寫入的執行紀錄例外、根 `.dockerignore` 四行、舊薄殼跑新 major 回 3）維持規格所載。規格仍待定的三項（啟動器讀設定檔的方式、外部 repo 反向採用紀錄腳本、紀錄事件名清單待審）不在本頁範圍。

## 出處對照（條號 → 來源）

來源檔：spec = `decisions/interface_spec.md` v3.2；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`。來源原文用的是舊詞（工具 repo、下游專案、鎖定行、frozen、進度日誌、操作紀錄檔、協定號／schema 號／floor…），對照第 0 頁的新名。

| 條目 | 來源 |
|---|---|
| 一句話目的 | spec 文首、§4.7；grilling Q1、Q21 |
| 三方角色表 | spec §3.1、§4.5、§4.7；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則與名詞定案（2026-09-20） |
| 兩個自動化角色 | spec §7.1、§7.3；grilling CI 平台定案、相容性其餘採納（Renovate major 分開 PR） |
| 名詞：`config.toml`、三方合併、append 型、本機覆寫 | spec §0、§4.6、§4.9；v2.12 L3′；grilling Q6、Q12、Q13 |
| 名詞：交付物、契約檢查腳本 | spec §4.7、§7.1；grilling deploy 包定案 |
| I1 | grilling 隔離題定案；spec §0 |
| I2 | grilling Q10；spec §0、§1.2 sync、§3.6 |
| I3 | spec §0、§4.10、§6；grilling Q6 |
| I4 | grilling Q23、Q27；spec §2 |
| I5 | grilling Q23；spec §0、§2；例外 = v2.13 P12 |
| I6 | grilling 2026-09-20、01 頁拍板 (4)；v2.10-1；spec v3.2 §0「結束的兩種語意」、§6 類別欄 |
| I7 | grilling 16 條必修、Q5、Q15、01 頁拍板 (3)；spec §0；check.sh `export CI=1` = spec §7.1 |
| I8 | grilling 16 條必修、Q13、19 條-6、01 頁拍板 (3)；spec §0（訊息 6-4） |
| I9 | grilling deploy 包定案、Q14；spec §4.7 |
| I10 | grilling Q20 定案（改）、Q20 修正、01 頁拍板 (1)(2)；spec v3.2 §0（訊息 6-9、6-35；sync 豁免已撤回） |
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
| 例外：進度檔與 `.tmp.*` | spec §0、§4.6 |
| 本頁待拍板（四點已定） | grilling「01 頁四點拍板（2026-09-20）」；spec §9.1 P1–P3 |
| 原矛盾 1–7（已解） | 1、2、3、4 = 01 頁四點拍板 2026-09-20（grilling「01 頁四點拍板」；spec v3.2 §0、§2、§6）；5、6、7 維持 spec（v2.13 P12、P13；§2、§8-5） |


==================================================
附件 C：02 動詞介面表（decisions/review/02_verbs.md）
==================================================
# 審閱頁 02：動詞介面表

本頁列 `just vendor_kit <動詞>` 的 11 個動詞、升引擎與 `bootstrap.sh`，只放契約層：語法（照第 0 頁記法）、做什麼、寫哪類檔、結束碼、CI 模式；步驟細節屬於討論圖第 11–39 頁的流程頁，表末欄指過去。只用第 0、1 頁的詞，只摘錄規格、不新增決議，出處在文末。審閱方式：逐列看是否與你認知一致，不一致的寫一句理由。

## 本頁名詞（第 0、1 頁沒有的頁內特有詞）
- 快路徑：`sync` 不起容器的判定——啟動器只比對印記第一行與版本鎖定行、`gen/tools.just` 存在、沒有進度檔、非 CI 模式，全相符就以 0 結束。
- 指紋重驗：兩段式動詞（先算計畫、拉 image，再寫入）在寫入前重算專案狀態的指紋，與計畫不同就不寫、以 1 結束並要求重跑。
- 離線包：release 附的 `docker save` tar 與同名 `.digest` 旁檔（正式 digest）；`--local` 用它。

## 通則（每個動詞都適用，表內不重複）
1. 執行紀錄：每次執行第一件事是建執行紀錄，建不了 → 1 零寫入，沒有關掉它的選項。
2. 專案根：只准在專案根執行，否則 → 1 印出該到哪個目錄；`sync` 被工具 recipe 自動觸發的那次自己先切到專案根。
3. 進度檔：可寫動詞在第一個寫入前建進度檔、成功即刪，開始前遇未完成交易先恢復再繼續；唯讀動詞（`sync`、`update`）遇到只印恢復指令 → 1，`help` 印出仍 0。
4. `-y` 與 CI 模式是兩個獨立開關：`-y` 只省略詢問（需詢問但無終端又沒 `-y` → 1），不授權覆蓋、不硬加；CI 模式 = 不寫任何進 git 的檔、不查最新版，需改進 git 的檔 → 1 印清單（與 `-y` 無關），仍拉鎖定版 image、仍寫 `cache/`、`gen/`。
5. 結束碼 3（介面版／檔案版不合）一律零寫入（執行紀錄除外）；網路、認證、不存在 → 1，不得偽裝成 3；不帶 `<repo>` 的動詞逐工具做完後回最重的碼（失敗 1 > 衝突 2 > 有新版 2 > 0）。

## 動詞表
「寫哪類檔」簡寫：鎖定行＝版本鎖定行、基準版＝基準版與 metadata、cache＝`cache/`、gen＝`gen/`（印記、`tools.just`、`.stamp`）、專案檔＝根 justfile／`.dockerignore`／初始檔／薄殼／`config.toml`、本機覆寫＝`version.local.toml`、進度檔；執行紀錄每列都寫、不列；「（刪）」＝該列只刪不建。

| 語法 | 一句話 | 寫哪類檔 | 結束碼 | CI 模式 | 流程頁 |
|---|---|---|---|---|---|
| `install [-y] [--no-justfile]` | 第一次接入：建 `.vendor_kit/`（引擎鎖定行、`config.toml`、薄殼五檔、空 `baseline/`、`gen/.stamp`），根 justfile 加一行、根 `.dockerignore` 加四行（既有檔先問）；再跑 = 修復（薄殼首行相符才重寫）；`install <repo>` → 1 改用 `add` | 鎖定行、gen、專案檔、進度檔 | 0；1 需人處理（非 git repo、巢狀 `.vendor_kit/`、薄殼被改、需詢問無終端）／失敗（清掉半成品、`log/` 保留）；3 | 同通則 | 約 13–14 |
| `uninstall [-y] [--dry-run]` | 逐工具照 `remove` 做，再只刪 hash 相符的 VK 自產檔與自己加在根 justfile／`.dockerignore` 的行；被改過的保留並列出；初始檔不刪只印清單；`log/` 一律保留；預檢任一工具不過整體不動 | 鎖定行、基準版、cache、gen、本機覆寫、專案檔、進度檔（皆刪） | 0；1 需人處理（dev 中、需詢問無終端、任一工具失敗 → 中止並列出已完成部分）／失敗；3 | 同通則 | 約 36–37 |
| `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | 接入一個工具：解析版本（沒指定 → 最新正式版）、拉展開、指紋重驗，建初始檔（copy 型已存在不納管、`-y` 也不覆蓋；append 型問後加行）、存基準版、重生 `gen/tools.just`，最後寫鎖定行；已接入 → 0；撞名／越出專案／`@<tag>` ≠ 鎖定行／私有無憑證 → 1，全在寫入前檢查 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（撞名、拒絕、沒憑證、需詢問無終端）／失敗（拉不到或逾時、指紋不同；鎖定行一律未動）；3 | 同通則 | 約 15–17 |
| `remove <repo> [-y] [--dry-run]` | 移除該工具的鎖定行、`cache/<repo>/`、基準版、印記與 `tools.just` 內的行；append 過的行問後只刪原文相同的；初始檔不刪只印清單；未接入 → 0；不帶 `<repo>` → 印用法、1 | 鎖定行、基準版、cache、gen、專案檔、進度檔（皆刪） | 0；1 需人處理（dev 中、需詢問無終端）／失敗（指紋不同、寫不進）；3 | 同通則 | 約 34–35 |
| `update [<repo>] [--exit-code]` | 查 registry 最新正式版（預發行排除）與鎖定行比對、逐一列出（不帶 = 全部，含引擎）；私有無憑證 → 該工具 1、其他照查；末行固定印「套用：just vendor_kit upgrade」；不拉 image | －（只寫執行紀錄） | 0；1 需人處理（任一工具查不到 → 整體 1）；`--exit-code` 且有新版 → 2；3 | 不受影響：仍查 registry（待拍板 1） | 約 39 |
| `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | 升到最新（或指定）版：拉展開、指紋重驗、換 `cache/`，初始檔逐檔問（沒改 → 換；只有你改 → 不動；兩邊改 → 三方合併、衝突留標記；新增問建、拒絕記下不再問；刪除只 warn），基準版推到新版（衝突仍推），最後寫鎖定行；先補「鎖定行已新、基準版仍舊」；不帶 `<repo>` 先完整預檢，引擎有新版 → 本次只升引擎；`@<tag>` 只配單一 `<repo>`，比現版舊 → warn 仍做 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（沒基準版先 `add`、dev 中、需詢問無終端）／失敗（拉不到、指紋不同、合併程式出錯）；2 衝突（留標記、基準版仍推，解完重跑）；3 | 同通則；`--dry-run` 就是契約檢查腳本用的那一步 | 約 21–26 |
| `upgrade vendor_kit[@<tag>] [-y] [--dry-run]`（升引擎；`upgrade` 不帶 `<repo>` 遇引擎新版時由啟動器自動接手） | 定目標（指定 `@<tag>` 不查 registry）→ 改引擎鎖定行 → 啟動器改用新引擎重跑 → 重產薄殼五檔與 `gen/.stamp`，`config.toml` 缺則建、有則三方合併 → 1 要求 commit 後再跑原指令；目標 = 現版且薄殼相符 → 0；薄殼被改 → 1 列差異不動；降版須能無損讀現有檔，否則 3 印「請 git revert」 | 鎖定行（引擎那行）、專案檔（薄殼、`config.toml`）、基準版（`config.toml` 副本）、gen、進度檔 | 0 無變更；1 需人處理（重產完成要 commit 再跑、薄殼被改、鎖定行已改但新引擎拉不到）／失敗（首行未變時重產失敗）；3 降版無法無損讀（零寫入） | 沒指定 `@<tag>` 不查、目標 = 現版；其餘同通則 | 約 27–29 |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 寫本機覆寫：工具的 `cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；引擎記 tag 與 image ID，之後只驗 ID、不拉；單段、不拉 image、不建進度檔；工具須已在鎖定行、`<dir>/dist/init.toml` 須存在；`-i` 只能 tag，較舊引擎不得重產薄殼 | 本機覆寫、cache、gen | 0；1 需人處理（不在鎖定行、缺 `init.toml`、CI 模式）；3 | 拒絕 → 1 | 約 30–31 |
| `undev <repo>`／`undev vendor_kit` | 撤本機覆寫那一行（撤的是最後一行則刪整檔），依鎖定行重新拉展開 `cache/`（引擎不展開，下次 `sync` 只提示升引擎）；未啟用 → 0 | 本機覆寫、cache、gen、進度檔 | 0；1 失敗（拉不到、寫不進；保留可恢復狀態）；3 | 規格未載，只寫不進 git 的檔（待拍板 3） | 約 32–33 |
| `sync [<repo>] [--verify]` | 快路徑相符 → 0 不起容器；否則依鎖定行重建 `cache/`、`gen/`：引擎版 ≠ `gen/.stamp` → 1 跑升引擎；本機覆寫的工具跳過；印記 ≠ 鎖定 digest → 重拉；`--verify` 逐檔驗指紋、不符重裝；未完成接入 → 1 跑 `add`；基準版落後 → warn 提示 `upgrade`；工具 recipe 執行前自動觸發 | cache、gen | 0；1 需人處理（薄殼不符、未完成接入、未完成交易）／失敗（拉不到或逾時、寫不進）；3 | 一律逐檔驗指紋；薄殼不符、基準版落後、未完成接入、任何本機覆寫都升為 1 | 約 18–20 |
| `prune [-y] [--dry-run]` | 鎖定行與本機覆寫引用的 image 當保留清單，啟動器依 VK 標籤列出其餘容器／image／network／volume、問後逐一刪；引擎清失效暫存與已完成交易的殘留；未恢復的進度檔只提示、不刪不擋；執行紀錄不歸它清 | 進度檔、暫存；docker 資源 | 0；1 需人處理（需詢問無終端）／失敗（磁碟滿到執行紀錄寫不進）；3 | 規格未載（待拍板 3） | 約 38 |
| `help`（別名 `h`） | 印命名空間層說明，明寫「已接入的專案跑 sync，不是 install」；不觸網、不安裝、不偵測狀態；遇未完成交易印恢復指令仍 0 | －（只寫執行紀錄） | 0；1 只在執行紀錄寫不進 | 無差異 | — |
| `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag／tar>] [--timeout <秒>] [-h]` | 第一次接入的啟動器：檢查 git repo 與 just ≥ 1.33.0，拉（本機有就不拉）引擎 image，跑 `install`，再逐個 `-t` 依序跑 `add`，任一非 0 立即中止、整體 1、列出已完成與未處理；專案已有 `version.toml` 就用那行的引擎，只有第一次才用內嵌版本；`--local` tar 由 `.digest` 旁檔取正式 digest、tag 只驗本機 ID 記成本機覆寫；再跑 = 修復 | 經 `install`、`add` 寫的全部；`--local` 時本機覆寫（`install` 成功後才寫） | 0；1 需人處理（非 git repo、just 太舊、需詢問無終端）／失敗（拉不到、`install` 失敗不留半成品、任一 `add` 失敗）；3 | 同 `install`、`add` | 約 11–12（離線包 46–47） |

## 本頁待拍板（規格與討論紀錄有出入、或兩邊都沒寫清楚；列出不取捨）
1. CI 模式定義「不查最新版」與 `update`「不受 CI 模式影響、仍查 registry」並存：第 0 頁定義寫全稱、規格另給 `update` 例外——定義加「`update` 除外」，還是 `update` 在 CI 模式也不查？
2. 驗收要在 GitHub Actions 跑完整流程（`install` → `add` → `upgrade` → …），而 Actions 預設 `CI=true`，依 CI 模式規則 `add`／`upgrade` 一律 1；規格沒寫驗收如何處理（清掉 `CI`？另設變數？）。
3. `install`、`uninstall`、`undev`、`prune` 在 CI 模式的行為只靠通則、討論紀錄沒提，`dev` 明寫拒絕；要不要逐動詞寫死？
4. `prune` 保留清單：討論紀錄寫「清 `version.toml` 未引用者」，規格把本機覆寫（`version.local.toml`）引用的 image 也列入保留。
5. 引擎內「拉 image 展開」的名字：討論紀錄第 1 頁改名 fetch、codex 建議 materialize、規格內部子命令用 materialize、第 0 頁模組名用「取件 `fetch`」；內部名不對外，但兩份文件要對齊。
6. 第 0 頁 `update` 寫「不寫任何檔」，規格與本頁為「只寫執行紀錄」（`help` 那條第 0 頁有寫例外，`update` 沒有）。

出處（定稿時移除）：通則 spec §0、grilling 01 頁四點拍板 2026-09-20／Q23／Q27／19 條-6；各動詞 spec §1.1 選項總表、§1.2 動詞表、§2 結束碼總表、§2c 動詞×檔案矩陣、§3.4、§3.6、§6 訊息文字；升引擎 spec §1.2 upgrade (a)(b)、§3.4、§3.5、grilling Q9／Q10／Q19／Q23／v2.11-1；bootstrap.sh spec §1.2、§4.8、grilling Q18／Q25／Q26／r9；待拍板 1–3 spec §0／§1.2 update、dev／§7.4，4 grilling 9 ↔ spec §1.2 prune（review A1），5 grilling 第 1 頁、codex_verbs ↔ spec §3.2 ↔ 00_terms 模組表，6 00_terms 動詞表 ↔ spec §2c；流程頁序依 `review_v2_out/pages.json`（第十二版），最終以推送後為準。


==================================================
附件 D：規格 §0–§2（decisions/interface_spec.md 文首至 §3 之前）
==================================================
# vendor_kit 介面規格（interface reference）v3.2（2026-09-20；**v3.2 = 01 頁四點拍板（2026-09-20）+ 名詞定案（第 0 頁）落實，改動見 §10 #117–#130**；v3 併入 proposal_v2 v2.10–v2.12、grilling「2026-09-20 第八～九輪審查後定案」、r9 規格層矛盾，改動見 §10 #58–#95；**v3.1 併入 v2.13（§9.1 P4–P13 結案）與 v2.14（第十輪後圖面落實與小定案），改動見 §10 #96–#116**）

用途：後續每張票唯一可引用的 input／output 定義；`/to-spec` 的原料。前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）、`interface_spec.v2.final.md`（v2 定稿 = v2.7 併入後、v3 併入前）、`interface_spec.v3.0.md`（v3 = v2.13／v2.14 併入前）、`interface_spec.v3.1.md`（v3.1 = 01 頁拍板與名詞定案落實前）。

來源優先序（高 → 低）：
0. v3.1 新併入：`proposal_v2.md` **v2.14 → v2.13**（v2.13 = 主對話依既定原則對 §9.1 P4–P13 的取捨，使用者可否決；v2.14 = 第十輪後圖面落實與兩個小定案）。
0′. v3 併入：`grilling.md`「2026-09-20 第八～九輪審查後定案」；`proposal_v2.md` **v2.12 → v2.11 → v2.10**（v2.11-1 撤回 v2.10-4；衝突以最新為準）；`review_v2r9_findings.md` 中屬**規格層**的矛盾（選項表 `--local` 適用欄拆 bootstrap.sh／add、E(c) 指定 `@tag` 與 CI 模式是兩條分支、help 遇未完成交易印 6-33 仍 0、bootstrap 逐 `-t` 一個失敗即中止）；`decisions/log/agy_summary.md`、`agy_summary2.md`、`draft.md` 只作 §4.10 的設計依據，**只取 v2.12 已定案的部分**。
1. `grilling.md` 2026-09-19 條目（Q22 sync 快路徑、Q23 結束碼 3、Q24 vk-resolve 格式與實作層取捨、Q25 選項表、Q26 離線 `.digest`、Q27 多工具彙總、「規格審查 16 條必修」直接採納）。
2. `interface_spec_review.md`「最終建議」一～五節（16 條必修、22 個待定的建議值、vk-resolve/1 骨架、結束碼 3 邊界、F1 定案）與「規格與定案不符」清單——全部套用，除非與 grilling 相衝（grilling 勝）。
3. `proposal_v2.md`：v2.5 → v2.4 → v2.3 → v2.2 → v2.1 → 正文。
4. 其他 decisions／issue（#26、#27、#28、#29、base_pitfalls、compat、isolation、contract）。

每條規格後以 <sub>[來源]</sub> 標注；`[待定]` 集中於 §9；本次每處改動的依據列於 §10；矛盾處理於 §11。占位符（名詞一律照第 0 頁「00 名詞與縮寫」，`<sub>` 出處註記保留來源原文的舊詞）：`<repo>` 下游 repo 名、`<ns>` just 命名空間、`<dir>` 目錄、`<tag>`、`<digest>`、`<ref>` = `<image>:<tag>@sha256:<digest>`、`vX`／`vY` 引擎版本、`P` 協定整數、`N` schema 整數、`<org>` GitHub 組織名、`<id>` 交易 id（= `<trace_id>`，32 hex）、`<id8>` = trace_id 前 8 碼、`<UTC-ts>` = `YYYYMMDDTHHMMSSZ`、`<verb>` 動詞名、`<專案根>` = 含 `.vendor_kit/` 的目錄。

## 0. 共通前提（所有動詞）

| 項目 | 規格 |
|---|---|
| 專案根 | = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；不是 git toplevel。第一次 `install` 時尚無 `.vendor_kit/`，候選專案根 = 呼叫目錄。<sub>[grilling Q20 定案（改）；review I-47]</sub> |
| 執行位置 | vendor_kit 動詞只准在專案根執行：recipe 檢查 `invocation_directory() == justfile_directory()`，否則 1 印 6-9。**所有動詞一體適用，`sync` 亦無例外**（原 F1「sync 豁免此檢查」撤回）；工具 recipe 自動觸發的 `_sync` 自己先 `cd` 到專案根再呼叫 `just vendor_kit sync`（§3.6），故不受影響。工具自己的 recipe 是否擋由工具決定。<sub>[grilling Q20 修正；01 頁拍板 2026-09-20 (2)]</sub> |
| git | 專案根須在某 git repo 內（主機側 `git rev-parse --is-inside-work-tree`）；引擎不讀 `.git`、不碰 index；不做 `git init`。禁止巢狀：install 時上層**或下層**已有 `.vendor_kit/` → 1 + 6-35（01 頁拍板確認）。worktree（`.git` 是檔）與 submodule 同樣適用（後者以 §7.4-20 實測為準）。<sub>[grilling Q20、19條-1、-10；review I-47]</sub> |
| 主機需求 | docker ≥ 19.03（或 Podman ≥ 4.9，見 §3.1）、just ≥ 1.33.0（GitHub release 下載版）、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA → issue v2。主機命令白名單見 §3.1。<sub>[grilling Q4、Q8、19條-2、-13；v2.4-10]</sub> |
| 不變量 | 對專案檔：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（= 不用工具版本取代客製內容；例外只有根 justfile 一行、根 `.dockerignore` 四行、已納管初始檔（含 `config.toml`）經同意的換版／三方合併）。執行紀錄（§4.10）與進度檔是 vendor_kit 自己的檔，不適用四原則。自動化（sync）只碰不進 git 的東西（cache/、gen/）。never fail silently。<sub>[grilling 隔離題、Q22 補；proposal §1；isolation 最終建議]</sub> |
| 詢問通則 | 需詢問但無 tty／EOF 且無 `-y` → 1 印 6-4；EOF／Ctrl-C = 中止整個 apply 回 1、不套用、**不記 declined**（declined 只記明確回答「否」）。明確回答「否」→ 不寫、metadata 依 §4.3 記錄。`-y` 只省略詢問，不授權覆蓋既有未納管檔、不硬加 append 行、**不解除 CI 模式**（`-y` 與 CI 模式為獨立開關，見下列 CI 模式）。<sub>[grilling 19條-6、Q13；v2.5-1、v2.5-4；review Claude 原文 12；01 頁拍板 2026-09-20 (3)]</sub> |
| CI 模式 | `CI` 真值規則：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；check.sh 自己 `export CI=1`。CI 模式 = 不寫任何 tracked 檔、不查最新版；升為失敗的警告**明列**：薄殼不符、基準版落後、未完成接入、任何 local 覆寫、需改 tracked 檔（與 `-y` 無關）；Q15 的「沒納管／拒絕過」提醒**不**紅燈；仍拉鎖定版 image、仍寫 cache/、gen/。`update` 不受 CI 模式影響（唯讀、不寫檔）。**`-y` 與 CI 模式是兩個獨立開關**：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`；CI 模式下需改進 git 的檔一律 → 1 印清單，與 `-y` 無關。CI 模式由 `CI` 環境變數為真觸發（CI 平台自設或 check.sh 自設；本機手設 = 唯讀驗證，允許）。<sub>[v2.1 A；v2.2 A；v2.5-1；review 必修 4；review I-02、Claude 原文 25；01 頁拍板 2026-09-20 (3)]</sub> |
| 進度檔 | **所有可寫動詞第一個寫入前必建進度檔，不設例外**：add／`upgrade <repo>` 記 metadata `[progress]`；install（**第一次也建**，該日誌同時是「不留半成品」的清除清單，成功後刪；v2.13 P5）／remove／uninstall／undev／prune／`upgrade vendor_kit`（含不帶 repo 時 E(a) 的自身那段）放 `.vendor_kit/.tmp.<verb>.<id>.toml`（§4.6；自身升級 = `.tmp.upgrade.<id>.toml`，在改 version.toml 第一行**之前**建，新引擎重產薄殼完成後由新引擎刪）。`<id>` = trace_id（§4.10）。可寫動詞開始前偵測到未完成交易 → 先恢復再繼續（`upgrade vendor_kit` 的恢復 = 重跑 `upgrade vendor_kit`），失敗明列 6-27；唯讀動詞只偵測、**不自動恢復**、除執行紀錄外不寫任何檔：**sync／update 印 6-33 結束 1，help 印 6-33 仍 0**。prune 特例：遇活躍（未恢復）日誌只列出並印 6-33、不刪、**不視為未完成交易**（不擋 prune、不恢復；差集與 `apply prune` 照做）。第一次 install 也建（v2.13 P5）。<sub>[grilling 進度日誌條、Q24、2026-09-20 定案；v2.2 C；review 必修 9；v2.7-7；v2.9-6、-8；v2.10-6；v2.11-1；v2.12 L5]</sub> |
| 執行紀錄 | 每個動詞每次執行（含 help、update、sync 快路徑、prune、`--dry-run`）除印 tty 外必寫一檔 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）：啟動器在任何其他動作之前 mkdir + 建檔 + 寫 `launcher_start`，失敗 → 1 + 6-38、零寫入；引擎啟動時 append `engine_start`，失敗 → 1 + 6-38、不進 resolve；無 `--no-log`。它是 vendor_kit 自己的檔（不進 git、不進 build context、不適用專案檔四原則），與進度檔分工：進度檔管交易恢復（成功即刪），執行紀錄管事後追溯（保留規則 §4.10）。`trace_id` 同時是進度檔交易 id。凡印到 tty 的訊息一律同句進 `body`。bootstrap.sh 就是第一次接入的啟動器：先 `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`，之後才 pull／install（§1.2 bootstrap.sh）。<sub>[v2.11-3；v2.12 L1–L5；v2.13 P4]</sub> |
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

通則（每個動詞，含 help 與 bootstrap.sh —— 它就是第一次接入的啟動器，v2.13 P4）：啟動器最先建執行紀錄並寫 `launcher_start`（失敗 → 1 + 6-38、零寫入），**再**做下表的前置檢查；**每個**引擎子命令（resolve 容器、apply 容器、單段各一）啟動時先 append `engine_start`（失敗 → 1 + 6-38、不做任何動作）、結束寫 `engine_exit`；啟動器結束前 `log_prune`、`launcher_exit` 記結束碼與耗時（§4.10）。下表不逐格重複；圖面表現法：每頁 resolve 段與 apply 段各一格 `engine_start`、頁尾一格 `launcher_exit`／`log_prune`。<sub>[v2.12 L4；v2.14-2]</sub>

| 動詞 | 語法 | 位置參數 | 前置檢查 | 副作用（寫哪些檔，見 §4） | 詢問點（`-y`／無 tty） | 結束碼 | stdout／stderr 概要 |
|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag 或 tar>] [--timeout <秒>] [-h]` | 無 | **順序**：驗 git repo／just（下列）→ `mkdir -p .vendor_kit/log/bootstrap/`（含目錄內 `.gitignore`）→ 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install（v2.13 P4）。在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref；最低介面版檢查（§2）；`--local` 不論 tar 或 tag 形，以上前置檢查一律先做 <sub>[grilling Q8、Q18；v2.4-5；v2.9-1]</sub> | `docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref（拉不到 → 1 + 6-24／逾時 6-31，**失敗出口**、不退回內嵌；tag 形 `--local` 的 `docker image inspect` 本機無此 image 亦為失敗出口；v2.14-5）→ 引擎 `install`（失敗 → 1：依 `.tmp.install.<id>.toml` 清半成品，**`.vendor_kit/log/` 保留**，訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」；v2.13 P4、P5）→ 逐 `-t` **依序**呼叫 `add <repo>[@<tag>]`，**任一 add 回非 0 → 立即中止**、不處理後續 `-t`、整體回 1 並列出已完成／未處理的工具（已完成的 add 保留；「不留半成品」只對第一次 install 成立）；`--local` 時 version.toml 仍寫正式 ref@digest：tar 形由同名 `.digest` 旁檔取得 index digest（§4.8），tag 形**不讀 `.digest`**、只 `docker image inspect` 本機 image ID，正式 ref 來源 = 專案已有 version.toml → 該行、第一次接入 → bootstrap.sh 內嵌引擎 ref；version.local.toml 寫 `vendor_kit = "<tag>"` + `vendor_kit_image_id`，在 install 成功後才寫、失敗清除；不自刪。離線契約入口 = `bootstrap.sh --local <tar>`（值判別見 §1.1 B1）；離線包內另含 `local_bootstrap.sh` **便利包裝**（偵測 daemon 架構 `docker version --format '{{.Server.Arch}}'`、挑該平台 tar、`exec ./bootstrap.sh --local <tar> "$@"`），不是契約入口、不另定介面 <sub>[proposal §2；#27；grilling Q26；v2.5-8；review 必修 15；v2.7-1；v2.9-1；v2.10-2；r9]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 | 0；1 失敗不留半成品（只對第一次 install 成立）；任一 `-t` 的 add 失敗 → 1（中止）；3 見 §2 <sub>[proposal §2；v2.2 C；r9]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" -w /repo <引擎 ref> --protocol P install` <sub>[#27；review B7]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 + 6-17 <sub>[codex_verbs]</sub> | 在 git repo 內（否 → 1 + 6-16）；上層與下層皆無 `.vendor_kit/`（否 → 1 + 6-35）；不被 gen/.stamp 比對擋；第一次／修復判定用薄殼自描述首行（§4.5）：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 + 6-28 列差異不動 <sub>[proposal §2；grilling Q20、Q17；v2.5-8]</sub> | 建 `.vendor_kit/`：version.toml（含 schema、written_by）、**config.toml**（§4.9，含註解與預設值；修復型缺則建、存在不動）、entry.just、vendor.just、.gitignore（含 `log/`）、ci/check.sh、baseline/（空、不建 metadata）、gen/.stamp；**log/**（含目錄內 `.gitignore`）由**啟動器**在寫 `launcher_start` 前建（第一次接入 = bootstrap.sh 建 `log/bootstrap/`；§4.10、v2.13 P4），引擎不建；根 justfile 無 → 建（§4.5 兩段式內容：import 一行 + `default:`／`\t@just --list` 兩行）；有 → 問後加一行；已含那行 → 不再加；根 `.dockerignore`：無 → 建（四行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；有 → 問後 append（同 §4.3 append 規則；插入的行記於 `baseline/.vendor_kit.toml`，見 §4.3 註）；再跑 = 用引擎重寫薄殼（hash 相符才重寫）；**第一次與修復型都**在第一個寫入前建 `.tmp.install.<id>.toml`（統一規則、無例外；第一次時它同時是「不留半成品」的清除清單，失敗依它移除已寫的檔、`log/` 保留，成功後刪；§4.6、v2.13 P5）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1；v2.9-8；v2.12 L1、L3′；v2.13 P4、P5]</sub> | 根 justfile 已存在 → 6-20「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示；`.dockerignore` 已存在 → 6-34 <sub>[proposal §2；isolation A1(4)；grilling Q22 補]</sub> | 0／1／3 | 印建立或修改了什麼（含加進根 justfile 的那一行、加進 .dockerignore 的四行） |
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分 <sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；**config.toml** 比照初始檔保護模式：hash == `baseline/vendor_kit/config.toml` 副本 → 刪，被下游使用者改過 → 留下並列出（永不刪下游使用者改過的檔）；**`log/` 一律保留**（uninstall 自己也在寫）、不 rmdir `log/`，`.vendor_kit/` 因此保留（只剩 `log/`），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪；進度檔 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12；v2.13 P6；v2.14-6]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的四行同 append 規則問後只刪原文相同的；append 行問後**逐行**比對、只刪仍與紀錄原文相同的行，缺失／被改的行跳過並 warn（不是全有／全無）<sub>[proposal §2、§5；grilling Q22 補；v2.9-5]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留） | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；`--local <v>`：`<v>` 必須是存在的 `.tar` 檔（不收 image tag 形），否則 1 + 6-24（add `--local` 分句）；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`（只收 tar）：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26；v2.10-3]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [--dry-run]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；兩段（resolve→apply、重驗指紋）但不經 docker create/cp <sub>[proposal §2；v2.3 §5；review Claude 原文 3]</sub> | 刪 version.toml 該行、cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行；初始檔永不刪，印清單；進度檔 `.tmp.remove.<id>.toml` <sub>[proposal §2；v2.1 E；grilling 進度日誌]</sub> | append 過的行 → 6-21 問後只刪原文相同的（CRLF/LF 等價）<sub>[proposal §5；grilling Q13]</sub> | 0／1／3 | 初始檔清單 |
| `update [<repo>]` | `update [<repo>] [--exit-code]` | `<repo>` 可省 = 全部含 vendor_kit | 只查 registry（`tags/list` 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 CI 模式影響；單段、不經 docker create/cp；無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；不可同時宣稱「已是最新」；偵測到未完成交易 → 印 6-33 結束 1（不恢復）<sub>[proposal §2；grilling Q11、Q27；#28；v2.10-6]</sub> | 無 | 只寫執行紀錄（§1.2 通則） | 0 已列出；1 查詢失敗（任一工具 1 → 整體 1，即使另有新版）；`--exit-code` 有新版 → 2；3 <sub>[proposal §2；v2.1 E；grilling Q27]</sub> | 末行固定 6-15 <sub>[proposal §2]</sub> |
| `upgrade [<repo>[@<tag>]]` | `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 可省 = 全部含 vendor_kit 自身；`vendor_kit[@<tag>]` 為特殊值；`@<tag>` 限單一 repo | 順序：(0) metadata `conflicts` 非空且檔案仍含 `<<<<<<< vendor_kit:baseline` → 2 停（檔案失蹤不算已解）；(1) 有待合併（version.toml 已 B、基準版仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 `@<tag>`；CI 模式不查）；無基準版 → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新版新增 `<ns>`／dest 的全域撞名）再動任何東西；不帶 repo 且引擎有新版 → **本次只改第一行、工具不升** <sub>[v2.2 D；v2.1 B；v2.2 B；v2.5-6、-7；proposal §2；review I-20]</sub> | resolve → docker → apply：cache/、gen/<repo>.stamp、初始檔逐檔（§4.3 狀態機，N 讀自 `/dist/<repo>`）、基準版推到新版（有衝突仍推；解析失敗不推）+ metadata、gen/tools.just；version.toml 最後寫。自身：(a) 不帶 repo 遇引擎新版 → 舊引擎 apply（拿鎖、重驗、建 `.tmp.upgrade.<id>.toml`：記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending）只改第一行 → 啟動器比對第一行前後（§3.4）→ 用新引擎跑 `upgrade vendor_kit`；(b) `upgrade vendor_kit[@<tag>]`（單段救援路徑）主流程：前置 —— 薄殼被改（hash 不符自描述首行）→ 1 + 6-28 不動；有未完成的 `.tmp.upgrade.<id>.toml` → 本次即恢復（依日誌的目標 ref 續跑）；(1) 目標判定，**三條分支分開**：**指定 `@<tag>`** → 不查 registry，目標 = 指定 tag（≠ 現 ref 仍走「有新版」分支；降版以其 image LABEL 的介面版／檔案版判）；**CI 模式且未指定** → 不查、目標 = 現 ref；**其餘** → 查 registry 取最新正式版；(2) 目標 ≠ 現 ref？**是** → 先建 `.tmp.upgrade.<id>.toml` → 改第一行 → 啟動器再以新 ref 跑一次（§3.4）→ 新引擎重產薄殼五檔（含 log.sh）+ gen/.stamp → **config.toml 缺則建／有則三方合併（6-22 問；B = `baseline/vendor_kit/config.toml`；§4.9）** → 新引擎刪日誌 → **1 + 6-2**（E(c)(2) 圖須有此格與檔案框；v2.14-7）；**否** → 薄殼與現引擎相符？是 → **0 無變更**；否 → 建 `.tmp.upgrade.<id>.toml` → 用現引擎重產薄殼 → 刪日誌 → **1 + 6-2**，重產失敗（第一行未變）→ 1 + 印原因（**不是** 6-2b）；`@<舊版>` 降版：目標引擎（以其 image LABEL 的介面版／檔案版判）能無損讀現有檔才做（同介面版／檔案版 → 依上列 0／1），否則改檔前拒絕 **3 + 6-10** <sub>[v2.3 §2；v2.5-7；grilling Q19、Q23；review 必修 6、「自身升級第二次」一致；v2.7-5；v2.10-5；v2.11-1；v2.12 L3′；r9 E(c)]</sub> | 逐檔 6-22：「X 換成新版？」／「你和新版都改了 X，要三方合併嗎？」／新增檔「要建 X 嗎」（拒絕 → state=declined + declined_hash）／二進位／symlink 未改 → 問後換、改過保留 + warn／append 行找到 → 問後替換、找不到 → 不動印新內容；`-y` 全免問；CI 且需改 tracked 檔 → 1 印清單（與 `-y` 無關）<sub>[proposal §5；grilling Q14、Q6；v2.5-1；review 必修 10]</sub> | 0；1 工具層不動 version.toml（自身升級已改第一行後回 1 是明列例外）；2 有衝突（留標記、印檔名、基準版仍推到新版、解完重跑直到乾淨；`git merge-file` 衝突數映射為 2，其 I/O／執行錯誤 → 1）；3 <sub>[proposal §2；v2.3 §2；v2.2 D；grilling Q19、Q23；review I-25]</sub> | `--dry-run`：印會問哪些檔、6-6～6-8、metadata 遷移明列；dest 在 CI 路徑時 6-29 <sub>[grilling Q14、Q15]</sub> |
| `dev <repo>` | `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | `<repo>` 必填 | `-p`（工具必填）／`-i`（僅 `vendor_kit`，只能 tag 不能 digest）互斥；工具必須已在 version.toml（否 → 1）；`<dir>/dist/init.toml` 存在（缺 → 1）；CI 拒絕；單段、不經 docker create/cp；`-i` 的 image 以 LABEL 介面版／檔案版判定為「舊」時允許但禁止重產 tracked 薄殼（§2 (d)）<sub>[proposal §2；v2.2 B；v2.3 §5；grilling Q19；review Claude 原文 35]</sub> | 工具：version.local.toml `[tools].<repo> = "path:<dir>"`，cache/<repo>/ 改 symlink → `<dir>/dist`（唯讀性只在容器 mount 上成立），gen/<repo>.stamp 第一行 `path:<dir>`。自身：version.local.toml `vendor_kit = "<tag>"` + `vendor_kit_image_id`；之後啟動器用 `docker image inspect` 驗 ID、不 pull <sub>[proposal §2；v2.2 B；review 必修 3、I-42]</sub> | 無 | 0／1／3 | — |
| `undev <repo>` | `undev <repo>`／`undev vendor_kit` | `<repo>` 必填 | 未啟用 = 0 + 提示 | 兩段（`undev <repo>` 與 `undev vendor_kit` 皆走 resolve→apply）：apply 先建日誌 `.tmp.undev.<id>.toml`（記要撤的行，含 image ID）**才**撤 version.local.toml 該行（`undev vendor_kit` 把 `vendor_kit = "<tag>"` 與 `vendor_kit_image_id` 一起撤）；撤掉的是最後一個覆寫 → 刪除整個 version.local.toml；→ 重新 materialize 鎖定版（經 docker create/cp；`undev vendor_kit` 無 materialize）→ 最後刪日誌；失敗 → 1 保留可恢復狀態。`undev vendor_kit`：下次 just 用 version.toml 引擎，gen/.stamp（`<tag>`）≠ ref → 只提示 6-1、不重寫 <sub>[proposal §2；v2.2 B；v2.3 §5；v2.5-10；review F2、I-31]</sub> | 無 | 0／1／3 | — |
| `sync [<repo>]` | `sync [<repo>] [--verify]` | `<repo>` 可省 = 全部 | 每次工具 recipe 自動前置（§3.6）；快路徑（§3.6）；`--verify` 或 CI 為真 → 每檔 sha256 全驗（F5 已定）；引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；`resolve sync` 一開始偵測未完成交易 → 印 6-33 結束 1、不恢復（與 update 同一菱形；快路徑只把「無 `.tmp.*`」當起引擎條件）；下游 image `docker pull` 失敗 → 1 + 6-24／6-31 失敗出口 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9；v2.10-6；v2.14-4、-5]</sub> | 只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp。每工具順序：覆寫 path → 跳過 materialize/verify（仍查完成標記、基準版落後）；cache 缺或印記第一行 ≠ 鎖定 digest → materialize；否則 verify sha256 → 失敗 → 重裝 + warn；tools.just 缺或需重生 → 重生。無待辦 → resolve 回 `apply\|no` 快路徑 0（不起第二個容器）<sub>[v2.3 §4；v2.2 E；v2.5-9]</sub> | 無 | 0；1：薄殼不符、metadata 無完成標記（6-13）、CI 下基準版落後（6-5）、CI 下任何 local 覆寫；3 <sub>[proposal §2；v2.1 A]</sub> | 本機基準版落後 → warn 提示 upgrade |
| `prune` | `prune [-y] [--dry-run]` | 無 | 兩段：`resolve prune` 輸出 `keep` 清單（version.toml + version.local.toml 引用的全部 image）；啟動器 `docker {container,image,network,volume} ls --filter label=io.github.<org>.vendor_kit=1` 列出候選、扣掉 keep；image 只刪「帶 label 且本專案未引用」者（共享 daemon 上其他專案的引用不可知 → 文件明寫、`--dry-run` 先看）；活躍（未恢復）的 `.tmp.<verb>.<id>.toml` 不刪、只列出提示 6-33、不視為未完成交易（不擋 prune、不恢復）<sub>[grilling 9 修正、9 補充、Q24；review A1、I-33、I-34；v2.7-7]</sub> | 啟動器執行 docker rm／image rm／network rm／volume rm（不掛 docker socket）；`apply prune` 先建 `.tmp.prune.<id>.toml` → 刪失效的 `.vendor_kit/.tmp.dist.*/` 與已完成交易殘留的 `.tmp.*` → 刪日誌；執行紀錄的保留清理**不屬** `prune` 動詞（由啟動器每次呼叫 best-effort 做，§4.10）；磁碟滿連 prune 也被 6-38 擋（訊息附清空間提示）<sub>[v2.9-6；v2.12 L3、L4]</sub> | 列出候選後 6-32「要刪除以上 vendor_kit 資源嗎？」（`-y` 免問） | 0／1／3 | 列出刪了什麼、保留什麼（含原因） |
| `help`／`h` | `help` | 無 | 不觸網、不安裝、不偵測交易以外的任何狀態；偵測到未完成交易 → 印 6-33 **仍 0** <sub>[v2.10-6]</sub> | 只寫執行紀錄（§1.2 通則） | 無 | 0（6-33 不影響）；1 只在 6-38 | 命名空間層說明；help 明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」<sub>[codex_verbs]</sub> |

## 2. 結束碼總表

| 碼 | 定義 | 動詞例外／特例 |
|---|---|---|
| 0 | 成功（含 warn）；`add` 已接入完成、`remove` 未接、`undev` 未啟用、`upgrade vendor_kit` 無新版且薄殼相符皆 0 + 提示；`help` 偵測到未完成交易印 6-33 仍 0 <sub>[proposal §2；review 一致；v2.10-6]</sub> | — |
| 1 | 一般失敗、需人處理／重跑；工具層動詞回 1 時 version.toml 不動 <sub>[proposal §2；compat 條 4]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3；所有動詞（含 help／prune）執行紀錄建檔或 `launcher_start`／`engine_start` 寫入失敗 → 1 + 6-38（零寫入）；bootstrap.sh 任一 `-t` 的 add 失敗 → 1 中止 <sub>[v2.3 §2；grilling Q23；v2.12 L4；r9]</sub> |
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
| `dev <repo>` | 讀 | — | — | — | 寫 `[tools].<repo>` | cache/<repo>/ → symlink；gen/<repo>.stamp 第一行 | — | — | 寫 |
| `dev vendor_kit` | 讀 | — | — | — | 寫 `vendor_kit` + `vendor_kit_image_id` | — | — | — | 寫 |
| `undev` | 讀 | — | — | — | 撤行；最後一個 → 刪檔 | 重新 materialize（`undev vendor_kit` 無） | — | `.tmp.undev.<id>.toml` | 寫 |
| `sync` | 讀 | — | 讀（比對 gen/.stamp） | 讀 | 讀 | materialize／verify／重生 tools.just | — | 只偵測（6-33 → 1） | 寫（快路徑亦寫） |
| `prune` | 讀（keep） | — | — | — | 讀（keep） | — | — | `.tmp.prune.<id>.toml`；刪已完成交易殘留 `.tmp.*`、`.tmp.dist.*`；活躍者不刪 | 寫 |
| `help` | — | — | — | — | — | — | — | 只偵測（6-33 仍 0） | 寫 |
| 啟動器（每次呼叫，任何動詞） | grep 版本鎖定行 | grep `keep`／`days` 正規行 | 讀 vendor.just 自身 | — | grep 版本鎖定行 | grep stamp 第一行（sync 快路徑） | — | 偵測 `.tmp.<verb>.*` 存在（快路徑條件） | 建檔、寫啟動器事件、prune 舊檔（best-effort） |




==================================================
附件 E：定案紀錄末段（decisions/grilling.md 最後 60 行）
==================================================
- **Q14 定案 (1)**：upgrade 遇新版新增初始檔 → 問「要建 X 嗎」（-y 建）；拒絕 → metadata 記 declined，之後不再問但 dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑（.github/workflows/、.gitlab-ci.yml）時訊息醒目；工具契約：初始檔只能引用穩定入口（`just <ns> …`），不得引用 cache 內部路徑（base #1078/#1111）。
- 文件位置（skills 查證）：skills 無 PRD.md 概念；spec → issue（可丟棄）、不變量 → ADR、名詞 → CONTEXT.md。doc/PRD.md 為 base 式自家慣例，待使用者選 (a) 全走 ADR／(b) 保留 PRD.md + domain.md 註明。
- **文件與結構定案**：完全照 mattpocock/skills：根 README（入口）、CONTEXT.md（名詞）、ADR 短格式（無索引無模板）、spec → issue → tickets；drawio 只放架構／流程／契約。刪 doc/PRD.md、doc/adr/README.md、TEMPLATE.md（內容拆進 README 與 ADR）。base 只移植決策／政策。使用者確認：路徑改回 skill 預設 `docs/`（docs/adr、docs/agents）。
- **Q15 定案 (1)**：metadata 對每個範本記四種狀態（已納管／拒絕過／本來就有沒納管／使用者刪了）；`upgrade --dry-run` 與 check.sh 印「X 沒納管，與範本差 N 行」「Y 你拒絕過，vZ 有新版」，不動檔、不紅燈；新版有更新時對拒絕過的檔再問一次（base #1093／ADR-32）。
- **Q16 定案 (1) 分兩層相容承諾**：薄殼每次呼叫附 `--protocol P`，引擎依 P 回應。永久：任何舊薄殼可呼叫新引擎的救援路徑（install／upgrade vendor_kit／sync 不符提示，單段 docker run，不依賴 resolve/apply 與 gen）並得正確提示；舊資料永遠可讀、可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。非永久：舊薄殼跑新 major 的一般動詞只保證乾淨回 1 提示先 upgrade vendor_kit。floor = 固定 release 常數（第一個正式版）寫在契約，只能經 ADR 提高。前例：Gradle wrapper（舊 wrapper 可跑新版、跑第二次重產）、Docker Engine API 版本協商。
- **Q17 定案 (1) 薄殼自描述**：entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）寫 `# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化後的 hash>`；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 列差異不動（使用者 git checkout 還原後再跑）。gen/.stamp 不再承擔薄殼 hash（只記引擎 ref 供 sync 快速比對）。
- **Q18 定案 (1)**：bootstrap.sh 遇專案已有 version.toml → 用該行指定的引擎跑 install（不用內嵌引擎；拉不到就失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref。
- **Q19 定案**：降版 `upgrade vendor_kit -t <舊版>`：舊引擎能無損讀現有檔 → 成功；否則在改任何檔前拒絕並印「請 git revert」。結束狀態新增 **3 = 協定不合／版本太舊**（與 1 一般失敗、2 衝突區分）。`dev vendor_kit -i <舊 image>` 禁止重產 tracked 薄殼。
- 相容性其餘採納（機制層，雙軌一致）：每個 vendor_kit 寫的 TOML 有 `schema = N` + 寫入者版本（min_reader），同 schema 只加不改、讀時忽略未知欄位寫時保留；version.toml 契約 = 唯一符合 `^vendor_kit\s*=` 的行（禁 BOM／重複鍵／表旁路），不是行號；新讀舊在記憶體轉換、只在本來要寫該檔的明確動作寫回，跨版直遷不鏈式，metadata 遷移由 upgrade vendor_kit 做並在 dry-run 明列；讀先出貨寫延後（同 major 內 N-1 必能讀 N 寫的檔）；tools.just 最後寫且與 cache 同一 apply 內原子替換；已釋出 GHCR image、Release 資產、fixture 永不刪；Renovate preset 建議 major 分開 PR。驗收 F：floor 以來每個已釋出 bootstrap.sh + image 驅動候選（線性），每版最低環境（docker 19.03、just 1.33）跑完整，其他環境按世代；補列：只改第一行後 frozen sync、fresh clone 無 gen、使用者改薄殼／未納管檔、中斷重跑、歷史 parser × 合法／異常 TOML；成本上限當觸發討論條件。前例只引已查證者（Gradle wrapper、Cargo encode.rs、git repository-layout、K8s Rule #4b、Terraform version/terraform_version、npm arborist、Docker Engine API）。
- **Q21 定案**：vendor_kit 只搬移；dist 內容能否在目標平台執行是工具 repo 的責任（用出貨的 check.sh --dist 驗佈局／init.toml／image 可展開／兩平台一致 + 工具自己的測試）；vendor_kit 不檢查 binary、不承諾可執行（base #1149）。
- Q20 待確認：一 git repo 只有根目錄一個 .vendor_kit/；所有動詞 $PWD 必須 = git toplevel（否則 1 印路徑）；monorepo 多套列 v2（base #1036）。
- **Q20 定案（改）**：第一版支援 monorepo 子專案：專案根 = 含 `.vendor_kit/` 的目錄（recipe 用 justfile_directory() 定位，引擎掛該目錄為 /repo），不是 git toplevel；robot/、sim/ 各自 bootstrap、各自 cache；指令在該層或更深層打（just 向上找 justfile）；在別層打是使用者用錯層。引擎不讀 .git、不碰 index（worktree 的 .git 是檔案也無關）。禁止巢狀：install 時上層已有 .vendor_kit/ → 1。要求目錄在某個 git repo 內。
- Q20 修正：vendor_kit 動詞只准在含 .vendor_kit/ 的那一層執行：recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印「請到 <dir> 執行」（just 向上找 justfile 擋不掉，所以在 recipe 內擋）。工具自己的 recipe 是否擋由工具決定。
- **19 條疑似遺漏定案（2026-09-19）**：1 worktree 引擎不讀 .git（驗收加案例）；2 proxy → issue v2；3 引擎 LC_ALL=C.UTF-8、TZ=UTC、時間戳 UTC ISO 8601；4 容器以 host uid:gid 跑（既定），HOME 設容器內暫存目錄為實作細節；5 啟動器 trap 清容器與暫存、apply 靠進度日誌；6 需詢問但無 tty/EOF → 1 印「加 -y 或在終端執行」；7 -t 指舊版工具允許 warn；8 路徑含空白：啟動器一律引號、驗收加案例；9 舊 image 累積：第一版不處理（待使用者決定是否 v1 做 prune）；10 submodule → 派子代理實測寫進驗收；11 離線 upgrade 不支援，local_bootstrap.sh 只支援 install/add --local；12 rootless/Podman/Docker Desktop **進驗收矩陣**；13 SELinux 不支援；14 pull 逾時 **v1.0.0 必做**：預設逾時 + 可調參數，開 issue；15 引擎基底 EOL 列 v2；16 唯一 publisher 拿掉；17 Renovate currentValue+currentDigest 已定；18 驗收加「升級後 == 全新安裝」比對（排除時間戳、digest）；19 不列。
- remove/uninstall 進度日誌放 `.vendor_kit/.tmp.*`（metadata 會被刪）；add/upgrade 記 metadata state=in-progress。
- 9 修正：**第一版做 `prune`**：容器與 image 打 label；清 version.toml 未引用的舊引擎／工具 image、殘留容器、.vendor_kit/.tmp.*；network/volume 不建，驗收加「完整流程前後 docker network/volume ls 差集為空」。
- 12 修正：rootless docker（docker/setup-docker-action `rootless: true`，已查證）與 Podman（Ubuntu 24.04 runner 內建 4.9.3）進驗收矩陣；Docker Desktop 記 issue 未驗證。
- 14：pull 逾時 v1.0.0 必做，預設值 + 可調參數。
- 9 補充（使用者）：不建 network/volume，但**若意外建立了也要能刪**：所有 docker 資源（容器、image、network、volume）一律帶 vendor_kit label；`prune` 依 label 掃四類資源並刪除 version.toml 未引用者；驗收：故意留一個帶 label 的 network/volume，prune 後必須消失。
- **deploy 包定案**：base（工具）的功能，vendor_kit 不參與打包、不檢查。工具契約加一句：「工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml 或 GHCR；需要的檔打包時複製進去」；保證方式 = 工具 repo 自己在乾淨機器解包驗收；初始檔／recipe 不得寫死 cache 內部路徑（Q14）。version.toml 為公開格式，工具可讀它寫來源紀錄。
- **CI 平台定案**：ci_bridge（#25）短期不會有，第一版以 GitHub 為主：Renovate preset 放 vendor_kit repo（GitHub App 託管版）、GHCR、GitHub Actions 驗收；check.sh 維持平台無關設計；GitLab（PAT、Renovate 自架）留 #25 後續。
- **Q22 定案 (1) sync 快路徑**：啟動器只用 grep 比對 gen/*.stamp 第一行 vs version.toml 各行，全相符 → 不起容器；有差才起引擎。每檔 sha256 verify 只在明確 `just vendor_kit sync`、CI（frozen）、版本變動那次做。條件：`.vendor_kit/cache/`（與 gen/、version.local.toml、.tmp.*）明確列在 `.vendor_kit/.gitignore`；若 cache 會進 docker build context（工具 recipe 的 build 用專案根當 context），工具契約要求 `.dockerignore` 排除 `.vendor_kit/cache/`（或 install 以 append 模式問後加入根 .dockerignore）。
- 介面規格審查 16 條必修（interface_spec_review.md）直接採納：根 justfile default 兩行、tools.just 用 mod?、拿掉 --pull never 改 docker image inspect、CI 真值規則（非空且非 0/false）、resolve 不加 -t、rootless 不加 -u／Podman --userns=keep-id、TOKEN_FILE 用 -v 掛、轉發 NO_LOCK、Dockerfile.dist 必含 LABEL、vendor_kit= 行唯一正規形、-y 不解除 frozen、未知 TOML 欄位忽略、二進位問後換、唯讀動詞不自動恢復、Renovate preset 根目錄 default.json、主機命令白名單明列、min_reader 改純資訊欄 written_by、metadata 單一 state 列舉 + declined_hash、F1 = mod? + 工具模組內私有 _sync recipe + --dist lint。
- Q22 補：install 把 `.vendor_kit/cache/`、`gen/`、`.tmp.*` 加進根 `.dockerignore`（無則建；有則問後加、-y 免問）。
- **Q23 定案**：結束碼 3 = 版本／協定／schema 不合，先升級或退回才能繼續（含舊薄殼叫新 major 一般動詞——Q16 的「回 1」改為 3；舊引擎讀高 schema；< floor；-t 降版無法無損讀）。回 3 時零寫入；新舊以協定號／schema 比較，不用版本字串。既定回 1 的情境（印記不符、薄殼被改、自身升級完成要重跑）維持 1。
- **Q24 定案 vk-resolve/1 格式**：欄位 `|` 分隔（或 TAB），路徑等自由文字以 POSIX `printf '%b'` 可解的 `\ooo` 八進位跳脫編碼（任何 byte 安全，啟動器一行解碼）；首行 `vk-resolve/1`，末行 `end <N>`；啟動器先收完整份、驗首尾與筆數才動 docker；清單原樣掛給 apply 重驗指紋；「引擎已變」由啟動器 apply 前後 grep version.toml 第一行比對，不從 stdout 讀。實作層其餘取捨（暫存目錄放專案內 .vendor_kit/.tmp.dist.<id>/、prune 由啟動器執行 docker 指令、pull 逾時預設 300 秒僅正整數、label 前綴 io.github.<org>.vendor_kit、metadata 單一 state、C5 .tmp.<verb>.<id>.toml、E2 根目錄 default.json）依審查交叉比對結論直接定。
- **Q25 定案 選項表**：短選項只給常用：-t/--tool <repo>[@<tag>]（bootstrap.sh）、-y/--yes、-p/--path、-i/--image、-h/--help；長形限定：--dry-run、--source、--local、--exit-code、--timeout（=VENDOR_KIT_PULL_TIMEOUT）、--no-justfile；--protocol 為內部。版本一律 `<repo>@<tag>`，拿掉 --tag。--repair 併進 install（冪等修復）；--purge 明確不提供（永不刪使用者檔），開 issue 供後續討論。#27 同步改 `-t base@v1.4.0` 語法。
- **Q26 定案 (1)**：離線包每個 tar 附同名 `.digest` 旁檔（正式 index digest）；`add --local` 讀它寫入 version.toml，並在 metadata 記 image ID ↔ digest 對照供離線驗證。**離線可用**：啟動器先 `docker image inspect`，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1「拉不到」不 hang（逾時）。
- **Q27 定案**：多工具動詞做得完的做完，最後回最需要處理的碼（失敗 1 > 衝突 2 > 有新版 2 > 0；update 遇 1 與 2 → 1），訊息全列。
- 規格 v2 剩兩待定定案：`--local` 值含 `/` 或以 .tar 結尾 → 路徑（必須存在），其餘 tag，兩者皆成立 → 1 消歧；`sync`（無參數）= Q22 快路徑，`sync --verify`（長形）或 CI 為真 = 每檔 sha256 全驗。規格子代理補的 9 條小規則採納（EOF/Ctrl-C 不記 declined；合併結果解析失敗 → baseline 不推、記 conflicts；TOKEN 與 TOKEN_FILE 同設 → 1；.dockerignore append 記在 baseline/.vendor_kit.toml；prune image 範圍 = 帶 label 且本專案未引用，--dry-run 先看；vk-resolve 只用 `|`；update 唯讀不受 frozen 限制）。

## 2026-09-20 第八～九輪審查後定案
- `add --local` 只收 tar（tag 形只有 bootstrap.sh：既有 version.toml 或內嵌引擎 ref 才有正式 digest 來源）；不提供 `--digest`。→ v2.10-3、v2.11-2
- `upgrade vendor_kit` 一律建進度日誌 `.tmp.upgrade.<id>.toml`（統一規則、不設例外；撤回 v2.10-4）。→ v2.11-1
- 需人動作的 1 結束一律橙；6-2b 只適用第一行已改；help 偵測未完成交易印 6-33 但仍 0。→ v2.10-1、-5、-6
- 新需求：操作紀錄檔（每動詞每次執行寫檔、資料夾 ignore、格式參考業界／使用者 Notion 筆記「Debug 資訊架構」：JSONL + OTel 欄位 + lnav）。研究中：`decisions/log/`。
- 資料整理方向（使用者要求「確定的資料放到對的位置，不要全在 drawio」）：表格 7 頁 → spec issue；取捨 → ADR；名詞 → CONTEXT.md；圖只留架構／流程／狀態機／契約圖／目錄樹（34 頁）；先轉文字再看圖。
- 操作紀錄檔 L1–L6 定案 → v2.12（L6 事件集合待 codex 審後定）。待議：啟動器讀 config 的方式在鍵變多時重評；base 反向採用 POSIX log.sh（issue）。
- 審閱規則（2026-09-20）：由外而內一頁一頁；頁 N 不得引用頁 N 之後才出現的內容（p1b、p3、出貨、§7.4…）；三方角色（工具 repo／下游專案／vendor_kit 開發者）與「誰對誰承諾」第一頁明寫；出處標記移文末。01 頁圖上的「灰橢圓不對自己承諾」改寫為「vendor_kit 開發者＝承諾方：維護引擎 image 與薄殼，履行對兩方的承諾；內部實作不屬本契約、可變更」。

## 2026-09-20 名詞與縮寫定案（第 0 頁／CONTEXT.md）
- 三方（圖文一律全名、不縮）：**下游開發者**（開發工具 repo 的人；dev／undev、dist/ 出貨契約）、**下游使用者**（在專案裡接入／升級／使用工具的人，含只打 `just <ns> …` 的人）、**VK**（我們，承諾方）。同一人可兼兩種身分。「上游」「工具方」「專案方」「使用者的檔」不再用。
- VK 零件：引擎／薄殼／啟動器；引擎內 **VK 模組** 8 個（中文名＋英文代號＝程式模組名）：版本解析 resolve、取件 fetch、初始檔 initfile、薄殼產生 shell、交易 txn、設定與格式 schema、執行紀錄 log、清理 prune。
- 常用詞：**專案檔**（原使用者的檔）、**VK 檔**、**版本鎖定行**（原鎖定行／正規行）、**初始檔**、**基準版**（baseline）、**進度檔**（原進度日誌／交易日誌，`.tmp.<verb>.<id>.toml`）、**執行紀錄**（原操作紀錄檔，`log/…jsonl`）、**CI 模式**（原 frozen）、**需人處理**（橙）、**失敗**（紅）、**專案檔四原則**、**介面版**（原協定版 P）、**檔案版**（原格式版 schema）、**最低介面版**（原 floor）。
- 動詞小寫原文；`upgrade vendor_kit` = **升引擎**；「→ 1：X」「→ 0」寫法。
- 每個名詞 CONTEXT.md 附英文對照；第 0 頁「00 名詞與縮寫」放 01 之前；之後各頁只用第 0 頁定義的詞，各頁名詞表只留頁內特有詞；頁 N 不得前引頁 N 之後。
- deploy 歸屬（2026-09-20）：維持「deploy 是 base 的 recipe，VK 只搬移」（C「VK 自管 deploy」不做）；「抽成獨立工具 repo（deploy_kit）」的可行性——deploy 包綁 base 的 setup.conf／resolved compose／.env 覆寫軸線（ADR-23），能否剝離、剝離後怎麼接，需 base 那邊評估：**開 issue 給 base repo 徵詢意見**，vendor_kit 這邊同步記 issue 追蹤。VK 對部署包的唯一承諾 = I9（交付物執行期不依賴 .vendor_kit/、version.toml、GHCR）。

## 2026-09-20 第 0 頁定案補充與 registry 定案
- **組件／模組層級**：VK 由三個**組件**（component）組成：引擎／薄殼／啟動器；**模組**（module）是引擎內的程式單元；組件 > 模組。
- **progress 模組**：原「交易 `txn`」改名「**進度與寫入** `progress`」：建／恢復／刪進度檔、鎖、原子替換。
- **下游 repo／下游 image**：原「工具 repo」「工具 image」全面改名；`dist/` = 下游 repo 的出貨目錄；下游開發者 = 開發下游 repo 的人。
- **語法記法**：`<x>` 必填佔位符；`[x]` 可省略；`[@<tag>]` 可省略的版本後綴、緊接 repo 名；`-x <值>`／`--long <值>` 短／長選項等價、只有常用的才有短的；`-y` 不帶值的開關；`a／b` 二選一。第 0 頁在動詞表前列一節，並一句話列 `-p <dir>`、`-i <tag>`、`--exit-code`、`-y`。
- **規則去處**：CONTEXT.md 只放 glossary（每條「是什麼」一到兩句、附英文與 _Avoid_，通用程式概念不收）；記法與顏色進 spec 與主圖第 0 頁「00 圖例與記法」（見 `decisions/review/legend_page.md`）；審閱規則（由外而內、頁 N 不前引、各頁名詞表只列頁內特有詞、頁名帶序號、出處進文末附錄、例子一律 `<repo>`、決策不進 drawio／名詞不進 spec／規則不進 CONTEXT）進 AGENTS.md（草稿 `decisions/review/AGENTS.addition.md`）。
- **registry 定案**：留 GHCR——公開 image 免費、官方無公布 pull 上限；私有目前免費（"currently free"），未來可能套 Packages 額度（Free 500 MB／1 GB·月）。換站以 `crane copy`（不帶 `--platform`）或 `skopeo copy --all` 搬遷，index digest 不變、版本鎖定行只換 host；`docker buildx imagetools create` 不可用於搬遷（digest 有變的風險）。「host 可替換設定點」列待議。依據 `decisions/registry_summary.md`。
- 程式碼不變式（2026-09-20，使用者）：**巢狀迴圈／區塊不超過 3 層；判斷一律以提前返回（guard clause）為優先**。適用引擎 Python 與薄殼／啟動器 sh。落地：進 AGENTS.md 工作約定；lint 層強制（Python：ruff `PLR1702` too-many-nested-blocks 上限 3、`C901` 複雜度；shell：shellcheck + 自寫巢狀深度檢查）；違反 = CI 紅。→ spec §7 lint、ADR 不需要（非取捨）。
- 01 頁四點拍板（2026-09-20）：(1) 禁巢狀：上層或下層已有 .vendor_kit/ 都 → 1；(2) 動詞只准在專案根執行，**sync 亦無例外**（自動觸發的 _sync 自己先 cd 到專案根，不受影響）；撤回 spec F1 豁免；(3) CI 模式下需改進 git 的檔一律 → 1 印清單，與 -y 無關；-y 只省略詢問；CI 模式由 CI 環境變數為真觸發（平台自設／check.sh 自設；本機手設 = 唯讀驗證，允許）；(4) 顏色語意：橙 = 需人處理、紅 = 失敗（error）——補進 spec §2。其餘 3 條矛盾（零寫入的執行紀錄例外、.dockerignore 四行、舊薄殼回 3）維持 spec。01 頁待拍板清空。
  - 補充（使用者原話意）：-y 與 CI 模式是兩個獨立開關；CI 內可帶 -y（省略詢問），但 -y ≠ CI 模式、CI 模式也不隱含 -y。
- CI 架構（2026-09-20，**記錄、後續討論**）：前例研究在 `decisions/ci_summary.md`（agy 逾時，Claude 直接核對 11 個專案 26 個 workflow 原檔）。主流：同一入口檔掛 PR＋push main（靠 `if:`／標籤／changed-files 計畫 job 分流，不分檔）；release 另一檔（tag 觸發或 dispatch+environment）；共用用 `workflow_call` reusable 與 composite action；唯一 required check = 彙總 job；PR 只 build 不 push image；原生 arm runner 跑測試、QEMU 只 build。暫定建議：ci.yml（入口）＋release.yml＋build-image.yml（workflow_call）＋nightly.yml（可選）。**尚未定案，待 codex 雙軌與使用者討論。**
- 審閱頁形式（使用者 2026-09-20）：動詞頁太多文字——動詞是動作，細節屬流程圖；02 頁改成精簡表（動詞｜語法｜一句話｜寫哪類檔｜結束碼｜對應流程頁），步驟細節在對應流程頁審。

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
逐頁審閱

- {頁：00，條目：「薄殼」／「自描述首行」，類別：矛盾，一句說明：本頁稱薄殼五檔都在首行放自描述內容，但 D／E 明定 `ci/check.sh` 第一行是 shebang、自描述在第二行，且 `log.sh` 的表頭位置尚未說清楚，必修／選修：必修}
- {頁：00，條目：「薄殼」五檔，類別：定義不清，一句說明：E 的 Q17 只列 `entry.just`、`vendor.just`、`.gitignore`、`ci/check.sh` 四檔，未交代後來新增的 `log.sh` 是否適用相同 hash 契約，必修／選修：必修}
- {頁：00，條目：「專案檔」，類別：定義不清，一句說明：「不是 VK 自產的一切」容易被理解成初始檔不是 VK 建立；應直接定義為根 justfile、根 `.dockerignore` 與建立後歸下游使用者的初始檔，必修／選修：必修}
- {頁：00，條目：「VK 檔」，類別：遺漏，一句說明：清單漏掉 `version.local.toml` 與基準版旁的 metadata，後兩頁卻把它們當作 VK 管理的檔案使用，必修／選修：必修}
- {頁：00，條目：「版本鎖定行」及「佔位符 `<digest>`」，類別：矛盾，一句說明：格式寫成 `@sha256:<digest>`，但 `<digest>` 又定義為包含 `sha256:` 的值，照字面會得到 `@sha256:sha256:…`，必修／選修：必修}
- {頁：00，條目：「基準版」，類別：定義不清，一句說明：「當三方合併的第三份」無法說明角色，應明寫基準版是共同祖先，另兩份為下游使用者現況與新版初始檔，必修／選修：必修}
- {頁：00，條目：「進度檔」，類別：定義不清，一句說明：把 `.tmp.<verb>.<id>.toml` 與「基準版旁 metadata」合稱一種檔，會掩蓋兩種不同落點與生命週期，應說明哪些動詞各用哪一種，必修／選修：必修}
- {頁：00，條目：「執行紀錄」，類別：定義不清，一句說明：「寫不進就不做任何事」與 D 中 `bootstrap.sh` 先檢查 git／just、之後才建紀錄的順序互斥；需明定前置檢查是否算「做事」並統一規格，必修／選修：必修}
- {頁：00，條目：「CI 模式」，類別：矛盾，一句說明：「不查最新版」未列 `update` 例外，與 B I7、C update 及 D §0 明定 `update` 仍查 registry 衝突，必修／選修：必修}
- {頁：00，條目：「結束碼」／「需人處理」，類別：定義不清，一句說明：同一個碼 1 同時可能是需人處理或失敗，名詞表應明說分類由訊息語意而非只由碼決定，必修／選修：必修}
- {頁：00，條目：「install」，類別：矛盾，一句說明：「根 justfile 加一行」只適用既有 justfile；D 規定不存在時建立 import、空行、`default:` 與 recipe 共四行，必修／選修：必修}
- {頁：00，條目：「uninstall」，類別：定義不清，一句說明：「對稱移除 VK 自產的檔」會讓人預期刪光 `.vendor_kit/`，但 D 明定保留執行紀錄、被改的 `config.toml`／薄殼及非空目錄，必修／選修：必修}
- {頁：00，條目：「update」，類別：矛盾，一句說明：「不寫任何檔」與全域執行紀錄不變量及 D 的「只寫執行紀錄」衝突，必修／選修：必修}
- {頁：00，條目：「dev」，類別：矛盾，一句說明：「只寫 `version.local.toml`」與 D 規定工具 dev 還會改 `cache/<repo>/` symlink 及 `gen/<repo>.stamp` 衝突，必修／選修：必修}
- {頁：00，條目：「救援路徑」，類別：定義不清，一句說明：把 `install` 列為任何舊薄殼的救援路徑，卻沒有區分第一次接入由 `bootstrap.sh` 啟動與既有薄殼修復兩種情境，必修／選修：選修}
- {頁：00，條目：「下游 repo」／「下游使用者」，類別：建議，一句說明：「下游 repo」是提供工具的一方，而下游使用者所在 repo 沒有固定名詞，閱讀時很容易把兩種 repo 混為一談，宜補「下游使用者專案」或等價正式名稱，必修／選修：必修}

- {頁：01，條目：「下游開發者」負責欄，類別：定義不清，一句說明：「用契約檢查腳本驗 `dist/`」與後文該腳本位於下游使用者專案並跑同步、升版及專案測試的描述混在一起，需區分 `--dist` 檢查與下游 CI 驗收入口，必修／選修：必修}
- {頁：01，條目：「下游使用者」負責欄，類別：矛盾，一句說明：「跑 `upgrade <repo> -y` 解合併衝突」不正確，`-y` 只能同意執行三方合併，留下衝突後仍須人工編輯並重跑，必修／選修：必修}
- {頁：01，條目：I3，類別：矛盾，一句說明：「每個失敗都附可直接複製的指令」比 D 的契約更強；拉不到、寫不進或驗證失敗只保證原因，附下一步指令是「需人處理」的定義，必修／選修：必修}
- {頁：01，條目：I4，類別：定義不清，一句說明：「工具層動詞回 1 時版本鎖定行不動」範圍不明，`remove`／`uninstall` 可能已有可恢復的部分寫入，而升引擎又是明列例外，應精確列適用動詞，必修／選修：必修}
- {頁：01，條目：I5，類別：定義不清，一句說明：「回 3 零寫入」隨後只說不寫專案檔，會留下可否寫 `cache/`、`gen/`、進度檔的疑問；應明寫除執行紀錄既有開頭外完全不寫，必修／選修：必修}
- {頁：01，條目：I7，類別：矛盾，一句說明：`update` 唯讀且不受影響的例外與第 0 頁「CI 模式不查最新版」直接衝突，必修／選修：必修}
- {頁：01，條目：I11，類別：矛盾，一句說明：「每個可寫動詞」且「不設例外」會包含會寫本機覆寫、cache 與 gen 的 `dev`，但 D 與 C 明定 `dev` 不建進度檔，必修／選修：必修}
- {頁：01，條目：I11，類別：定義不清，一句說明：「可寫動詞」與「唯讀動詞」沒有在第 0 頁或本頁定義，且 `sync` 其實會寫 cache／gen，不能按一般字義稱唯讀，必修／選修：必修}
- {頁：01，條目：I12 引文「`--dry-run`」，類別：前引違規，一句說明：本頁尚未定義 `--dry-run`，其語法及適用動詞到第 2 頁才出現，必修／選修：必修}
- {頁：01，條目：I12，類別：矛盾，一句說明：「啟動器在任何其他動作之前」與 D 的 `bootstrap.sh` 順序「先驗 git repo／just，再建立執行紀錄」矛盾，必修／選修：必修}
- {頁：01，條目：I14，類別：定義不清，一句說明：「舊資料永遠可讀、可遷」若不限定為新版引擎讀歷史 VK 資料，會與高檔案版回 3 以及舊引擎不能讀新資料衝突，必修／選修：必修}
- {頁：01，條目：I14 引文「新 major」，類別：定義不清，一句說明：`major` 未在第 0 頁或本頁定義，且相容判斷實際依介面版／檔案版而非 SemVer major，必修／選修：必修}
- {頁：01，條目：「根 `.dockerignore`」例外，類別：定義不清，一句說明：這是對「專案檔永不刪」的明文例外，應直接標示只有 uninstall 經詢問且原文相同時可逐行刪，避免看似與 I1 衝突，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 的每個 VK TOML 都有檔案版、未知欄位讀時忽略且寫時保留、跨版直接遷移等資料相容承諾未被列為不變量，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D／E 的版本鎖定行唯一正規形、禁 BOM／重複鍵／表旁路是對外格式核心，但本頁未收錄，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 明定多工具動詞須先完整預檢、任一預檢失敗則整體不動；I4 只寫「做得完的做完」，漏掉這個重要原子性邊界，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 的 `tools.just` 最後寫且與 cache 在同一 apply 內原子替換，是避免半套工具入口的重要不變量，本頁未列，必修／選修：必修}
- {頁：01，條目：全頁用詞，類別：定義不清，一句說明：`metadata`、`hash`、`tty`、`image ID`、`major`、`tracked`／「進 git 的檔」等契約詞被反覆使用但未進第 0 頁或本頁名詞表，必修／選修：必修}

- {頁：02，條目：開頭與「流程頁」欄，類別：前引違規，一句說明：本頁直接引用第 11–39 頁及 46–47 頁的後續流程，違反「頁 N 不引用後面的頁」；審閱版應移除頁碼或改成不具前引性的流程識別碼，必修／選修：必修}
- {頁：02，條目：「寫哪類檔」簡寫，類別：矛盾，一句說明：把薄殼與 `config.toml` 歸入「專案檔」，與第 0 頁明定兩者是 VK 檔衝突，必修／選修：必修}
- {頁：02，條目：通則 1，類別：矛盾，一句說明：「每次執行第一件事」建立執行紀錄與 D 的 `bootstrap.sh` 先驗 git／just 再建紀錄衝突，必修／選修：必修}
- {頁：02，條目：通則 3，類別：矛盾，一句說明：「可寫動詞第一個寫入前建進度檔」與同頁 `dev`「不建進度檔」衝突，應改稱「交易型動詞」並列出集合，必修／選修：必修}
- {頁：02，條目：通則 3 引文「唯讀動詞（`sync`、`update`）」，類別：定義不清，一句說明：`sync` 會重建 cache／gen，所謂唯讀僅指不寫進 git 的檔或不恢復交易，一般人會誤讀，必修／選修：必修}
- {頁：02，條目：通則 5，類別：定義不清，一句說明：「失敗 1 > 衝突 2 > 有新版 2」把語意與數字混排，而且未說同為 1 的需人處理如何彙總，宜沿用 D 的「最需處理的碼」並另列訊息全保留，必修／選修：選修}
- {頁：02，條目：`install` 寫檔欄，類別：矛盾，一句說明：因簡寫錯誤而把薄殼及 `config.toml` 列成專案檔，使用者會誤以為它們受專案檔四原則而非 VK 檔規則管理，必修／選修：必修}
- {頁：02，條目：`install`，類別：遺漏，一句說明：語法列出 `--no-justfile`，一句話卻未說它跳過根 justfile 並只印手動指示，必修／選修：必修}
- {頁：02，條目：`uninstall`，類別：定義不清，一句說明：「預檢任一工具不過整體不動」與結束碼欄「任一工具失敗後中止並列出已完成部分」看似互斥，需區分預檢失敗與 apply 期間失敗，必修／選修：必修}
- {頁：02，條目：`add` 引文「`@<tag>` ≠ 版本鎖定行」，類別：定義不清，一句說明：只有已接入工具才有可比較的版本鎖定行，應寫成「已接入且指定 tag 不同時改用 upgrade」，必修／選修：必修}
- {頁：02，條目：`update` CI 模式欄，類別：矛盾，一句說明：仍查 registry 與第 0 頁 CI 模式定義衝突，不能以「待拍板」狀態交付使用者，必修／選修：必修}
- {頁：02，條目：`upgrade vendor_kit`，類別：定義不清，一句說明：「改版本鎖定行後才由新引擎重跑」但同列又把新引擎拉不到列為需人處理，應明寫此時版本鎖定行已改、進度檔如何恢復及可複製的恢復指令，必修／選修：必修}
- {頁：02，條目：`dev`，類別：矛盾，一句說明：「不建進度檔」與頁 1 I11、頁 2 通則 3 的「所有可寫動詞」不設例外矛盾，必修／選修：必修}
- {頁：02，條目：`undev` 語法，類別：遺漏，一句說明：D §1.1 明定 `--timeout <秒>` 適用 `undev`，本頁語法未列，必修／選修：必修}
- {頁：02，條目：`sync` 語法，類別：遺漏，一句說明：D §1.1 明定 `--timeout <秒>` 適用 `sync`，本頁語法未列，必修／選修：必修}
- {頁：02，條目：`prune`，類別：定義不清，一句說明：「本機覆寫引用的 image」只適用實際以 image tag／ID 覆寫的引擎；工具的 `path:<dir>` 並沒有 image，保留清單需分別表述，必修／選修：必修}
- {頁：02，條目：`bootstrap.sh`，類別：遺漏，一句說明：`--local` 同時接受 tag 或 tar，但一句話未交代含 `/`、`.tar`、檔案存在及兩種判定同時成立時回 1 的消歧規則，必修／選修：必修}
- {頁：02，條目：所有含 `--dry-run` 的列，類別：遺漏，一句說明：除 upgrade 外未說明 dry-run 是唯讀預覽但仍可能拉 image 展開，使用者無法由動詞表判斷副作用，必修／選修：必修}
- {頁：02，條目：全表語法，類別：遺漏，一句說明：D 明定所有動詞都接受 `--help`，本頁語法皆省略卻未設一條共同語法通則，必修／選修：選修}
- {頁：02，條目：全頁用詞，類別：定義不清，一句說明：`metadata`、`tracked`、`hash`、`symlink`、`image ID`、`正式版`、`預檢`、`dry-run` 等反覆出現但未納入第 0–2 頁名詞表，違反共同字典規則，必修／選修：必修}
- {頁：02，條目：本頁名詞「快路徑」，類別：定義不清，一句說明：只比「印記第一行與版本鎖定行」沒有說是逐工具全部相符，且 D／E 還要求檢查 cache、gen、本機覆寫與 `.tmp.*` 等條件，需完整列出，必修／選修：必修}
- {頁：02，條目：`sync` CI 模式欄，類別：遺漏，一句說明：D 還規定 CI 模式下任何本機覆寫與基準版落後均回 1、未納管／拒絕過只提醒不紅燈；本列只列前半，易誤解所有初始檔提醒都失敗，必修／選修：必修}

## 6 點判定

1. 同意：CI 模式定義改成「不查最新版，`update` 除外」；`update` 的唯一用途就是唯讀查詢，禁止查詢會使它在 CI 中失去契約意義，也與 D、E 的既有定案不符。

2. 同意：完整驗收 harness 應明確以 `CI=0` 執行會寫檔的 `install`／`add`／`upgrade` 流程；另開獨立案例設 `CI=1` 驗證唯讀與拒寫行為，不能依賴 GitHub Actions 的環境預設。

3. 同意：`install`、`uninstall`、`undev`、`prune` 以共同 CI 通則為準，不必逐列複寫；表格只寫偏離通則的例外，例如 `dev` 明確拒絕、`update` 仍查詢，並刪除「規格未載／待拍板」字樣。

4. 同意但須精確化：`prune` 保留版本鎖定行及本機覆寫實際引用的 image；工具的 `path:<dir>` 覆寫沒有 image 可保留，引擎 tag／image ID 覆寫才加入保留清單。

5. 同意：內部子命令 `materialize` 改名為 `fetch`，與第 0 頁「取件 `fetch`」模組一致；雖非對外介面，兩套名稱會妨礙文件追蹤與實作對照。

6. 同意：第 0 頁 `update` 改成「不寫任何檔，執行紀錄除外」或直接「只寫執行紀錄」；後者與 `help`、D 的檔案矩陣及全域紀錄不變量最一致。

總評：目前不能交給使用者定稿；至少須先修正 CI／update、進度檔與 dev、檔案分類、自描述首行、缺漏選項及所有前引違規。
tokens used
46,884
逐頁審閱

- {頁：00，條目：「薄殼」／「自描述首行」，類別：矛盾，一句說明：本頁稱薄殼五檔都在首行放自描述內容，但 D／E 明定 `ci/check.sh` 第一行是 shebang、自描述在第二行，且 `log.sh` 的表頭位置尚未說清楚，必修／選修：必修}
- {頁：00，條目：「薄殼」五檔，類別：定義不清，一句說明：E 的 Q17 只列 `entry.just`、`vendor.just`、`.gitignore`、`ci/check.sh` 四檔，未交代後來新增的 `log.sh` 是否適用相同 hash 契約，必修／選修：必修}
- {頁：00，條目：「專案檔」，類別：定義不清，一句說明：「不是 VK 自產的一切」容易被理解成初始檔不是 VK 建立；應直接定義為根 justfile、根 `.dockerignore` 與建立後歸下游使用者的初始檔，必修／選修：必修}
- {頁：00，條目：「VK 檔」，類別：遺漏，一句說明：清單漏掉 `version.local.toml` 與基準版旁的 metadata，後兩頁卻把它們當作 VK 管理的檔案使用，必修／選修：必修}
- {頁：00，條目：「版本鎖定行」及「佔位符 `<digest>`」，類別：矛盾，一句說明：格式寫成 `@sha256:<digest>`，但 `<digest>` 又定義為包含 `sha256:` 的值，照字面會得到 `@sha256:sha256:…`，必修／選修：必修}
- {頁：00，條目：「基準版」，類別：定義不清，一句說明：「當三方合併的第三份」無法說明角色，應明寫基準版是共同祖先，另兩份為下游使用者現況與新版初始檔，必修／選修：必修}
- {頁：00，條目：「進度檔」，類別：定義不清，一句說明：把 `.tmp.<verb>.<id>.toml` 與「基準版旁 metadata」合稱一種檔，會掩蓋兩種不同落點與生命週期，應說明哪些動詞各用哪一種，必修／選修：必修}
- {頁：00，條目：「執行紀錄」，類別：定義不清，一句說明：「寫不進就不做任何事」與 D 中 `bootstrap.sh` 先檢查 git／just、之後才建紀錄的順序互斥；需明定前置檢查是否算「做事」並統一規格，必修／選修：必修}
- {頁：00，條目：「CI 模式」，類別：矛盾，一句說明：「不查最新版」未列 `update` 例外，與 B I7、C update 及 D §0 明定 `update` 仍查 registry 衝突，必修／選修：必修}
- {頁：00，條目：「結束碼」／「需人處理」，類別：定義不清，一句說明：同一個碼 1 同時可能是需人處理或失敗，名詞表應明說分類由訊息語意而非只由碼決定，必修／選修：必修}
- {頁：00，條目：「install」，類別：矛盾，一句說明：「根 justfile 加一行」只適用既有 justfile；D 規定不存在時建立 import、空行、`default:` 與 recipe 共四行，必修／選修：必修}
- {頁：00，條目：「uninstall」，類別：定義不清，一句說明：「對稱移除 VK 自產的檔」會讓人預期刪光 `.vendor_kit/`，但 D 明定保留執行紀錄、被改的 `config.toml`／薄殼及非空目錄，必修／選修：必修}
- {頁：00，條目：「update」，類別：矛盾，一句說明：「不寫任何檔」與全域執行紀錄不變量及 D 的「只寫執行紀錄」衝突，必修／選修：必修}
- {頁：00，條目：「dev」，類別：矛盾，一句說明：「只寫 `version.local.toml`」與 D 規定工具 dev 還會改 `cache/<repo>/` symlink 及 `gen/<repo>.stamp` 衝突，必修／選修：必修}
- {頁：00，條目：「救援路徑」，類別：定義不清，一句說明：把 `install` 列為任何舊薄殼的救援路徑，卻沒有區分第一次接入由 `bootstrap.sh` 啟動與既有薄殼修復兩種情境，必修／選修：選修}
- {頁：00，條目：「下游 repo」／「下游使用者」，類別：建議，一句說明：「下游 repo」是提供工具的一方，而下游使用者所在 repo 沒有固定名詞，閱讀時很容易把兩種 repo 混為一談，宜補「下游使用者專案」或等價正式名稱，必修／選修：必修}

- {頁：01，條目：「下游開發者」負責欄，類別：定義不清，一句說明：「用契約檢查腳本驗 `dist/`」與後文該腳本位於下游使用者專案並跑同步、升版及專案測試的描述混在一起，需區分 `--dist` 檢查與下游 CI 驗收入口，必修／選修：必修}
- {頁：01，條目：「下游使用者」負責欄，類別：矛盾，一句說明：「跑 `upgrade <repo> -y` 解合併衝突」不正確，`-y` 只能同意執行三方合併，留下衝突後仍須人工編輯並重跑，必修／選修：必修}
- {頁：01，條目：I3，類別：矛盾，一句說明：「每個失敗都附可直接複製的指令」比 D 的契約更強；拉不到、寫不進或驗證失敗只保證原因，附下一步指令是「需人處理」的定義，必修／選修：必修}
- {頁：01，條目：I4，類別：定義不清，一句說明：「工具層動詞回 1 時版本鎖定行不動」範圍不明，`remove`／`uninstall` 可能已有可恢復的部分寫入，而升引擎又是明列例外，應精確列適用動詞，必修／選修：必修}
- {頁：01，條目：I5，類別：定義不清，一句說明：「回 3 零寫入」隨後只說不寫專案檔，會留下可否寫 `cache/`、`gen/`、進度檔的疑問；應明寫除執行紀錄既有開頭外完全不寫，必修／選修：必修}
- {頁：01，條目：I7，類別：矛盾，一句說明：`update` 唯讀且不受影響的例外與第 0 頁「CI 模式不查最新版」直接衝突，必修／選修：必修}
- {頁：01，條目：I11，類別：矛盾，一句說明：「每個可寫動詞」且「不設例外」會包含會寫本機覆寫、cache 與 gen 的 `dev`，但 D 與 C 明定 `dev` 不建進度檔，必修／選修：必修}
- {頁：01，條目：I11，類別：定義不清，一句說明：「可寫動詞」與「唯讀動詞」沒有在第 0 頁或本頁定義，且 `sync` 其實會寫 cache／gen，不能按一般字義稱唯讀，必修／選修：必修}
- {頁：01，條目：I12 引文「`--dry-run`」，類別：前引違規，一句說明：本頁尚未定義 `--dry-run`，其語法及適用動詞到第 2 頁才出現，必修／選修：必修}
- {頁：01，條目：I12，類別：矛盾，一句說明：「啟動器在任何其他動作之前」與 D 的 `bootstrap.sh` 順序「先驗 git repo／just，再建立執行紀錄」矛盾，必修／選修：必修}
- {頁：01，條目：I14，類別：定義不清，一句說明：「舊資料永遠可讀、可遷」若不限定為新版引擎讀歷史 VK 資料，會與高檔案版回 3 以及舊引擎不能讀新資料衝突，必修／選修：必修}
- {頁：01，條目：I14 引文「新 major」，類別：定義不清，一句說明：`major` 未在第 0 頁或本頁定義，且相容判斷實際依介面版／檔案版而非 SemVer major，必修／選修：必修}
- {頁：01，條目：「根 `.dockerignore`」例外，類別：定義不清，一句說明：這是對「專案檔永不刪」的明文例外，應直接標示只有 uninstall 經詢問且原文相同時可逐行刪，避免看似與 I1 衝突，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 的每個 VK TOML 都有檔案版、未知欄位讀時忽略且寫時保留、跨版直接遷移等資料相容承諾未被列為不變量，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D／E 的版本鎖定行唯一正規形、禁 BOM／重複鍵／表旁路是對外格式核心，但本頁未收錄，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 明定多工具動詞須先完整預檢、任一預檢失敗則整體不動；I4 只寫「做得完的做完」，漏掉這個重要原子性邊界，必修／選修：必修}
- {頁：01，條目：不變量整體，類別：遺漏，一句說明：D 的 `tools.just` 最後寫且與 cache 在同一 apply 內原子替換，是避免半套工具入口的重要不變量，本頁未列，必修／選修：必修}
- {頁：01，條目：全頁用詞，類別：定義不清，一句說明：`metadata`、`hash`、`tty`、`image ID`、`major`、`tracked`／「進 git 的檔」等契約詞被反覆使用但未進第 0 頁或本頁名詞表，必修／選修：必修}

- {頁：02，條目：開頭與「流程頁」欄，類別：前引違規，一句說明：本頁直接引用第 11–39 頁及 46–47 頁的後續流程，違反「頁 N 不引用後面的頁」；審閱版應移除頁碼或改成不具前引性的流程識別碼，必修／選修：必修}
- {頁：02，條目：「寫哪類檔」簡寫，類別：矛盾，一句說明：把薄殼與 `config.toml` 歸入「專案檔」，與第 0 頁明定兩者是 VK 檔衝突，必修／選修：必修}
- {頁：02，條目：通則 1，類別：矛盾，一句說明：「每次執行第一件事」建立執行紀錄與 D 的 `bootstrap.sh` 先驗 git／just 再建紀錄衝突，必修／選修：必修}
- {頁：02，條目：通則 3，類別：矛盾，一句說明：「可寫動詞第一個寫入前建進度檔」與同頁 `dev`「不建進度檔」衝突，應改稱「交易型動詞」並列出集合，必修／選修：必修}
- {頁：02，條目：通則 3 引文「唯讀動詞（`sync`、`update`）」，類別：定義不清，一句說明：`sync` 會重建 cache／gen，所謂唯讀僅指不寫進 git 的檔或不恢復交易，一般人會誤讀，必修／選修：必修}
- {頁：02，條目：通則 5，類別：定義不清，一句說明：「失敗 1 > 衝突 2 > 有新版 2」把語意與數字混排，而且未說同為 1 的需人處理如何彙總，宜沿用 D 的「最需處理的碼」並另列訊息全保留，必修／選修：選修}
- {頁：02，條目：`install` 寫檔欄，類別：矛盾，一句說明：因簡寫錯誤而把薄殼及 `config.toml` 列成專案檔，使用者會誤以為它們受專案檔四原則而非 VK 檔規則管理，必修／選修：必修}
- {頁：02，條目：`install`，類別：遺漏，一句說明：語法列出 `--no-justfile`，一句話卻未說它跳過根 justfile 並只印手動指示，必修／選修：必修}
- {頁：02，條目：`uninstall`，類別：定義不清，一句說明：「預檢任一工具不過整體不動」與結束碼欄「任一工具失敗後中止並列出已完成部分」看似互斥，需區分預檢失敗與 apply 期間失敗，必修／選修：必修}
- {頁：02，條目：`add` 引文「`@<tag>` ≠ 版本鎖定行」，類別：定義不清，一句說明：只有已接入工具才有可比較的版本鎖定行，應寫成「已接入且指定 tag 不同時改用 upgrade」，必修／選修：必修}
- {頁：02，條目：`update` CI 模式欄，類別：矛盾，一句說明：仍查 registry 與第 0 頁 CI 模式定義衝突，不能以「待拍板」狀態交付使用者，必修／選修：必修}
- {頁：02，條目：`upgrade vendor_kit`，類別：定義不清，一句說明：「改版本鎖定行後才由新引擎重跑」但同列又把新引擎拉不到列為需人處理，應明寫此時版本鎖定行已改、進度檔如何恢復及可複製的恢復指令，必修／選修：必修}
- {頁：02，條目：`dev`，類別：矛盾，一句說明：「不建進度檔」與頁 1 I11、頁 2 通則 3 的「所有可寫動詞」不設例外矛盾，必修／選修：必修}
- {頁：02，條目：`undev` 語法，類別：遺漏，一句說明：D §1.1 明定 `--timeout <秒>` 適用 `undev`，本頁語法未列，必修／選修：必修}
- {頁：02，條目：`sync` 語法，類別：遺漏，一句說明：D §1.1 明定 `--timeout <秒>` 適用 `sync`，本頁語法未列，必修／選修：必修}
- {頁：02，條目：`prune`，類別：定義不清，一句說明：「本機覆寫引用的 image」只適用實際以 image tag／ID 覆寫的引擎；工具的 `path:<dir>` 並沒有 image，保留清單需分別表述，必修／選修：必修}
- {頁：02，條目：`bootstrap.sh`，類別：遺漏，一句說明：`--local` 同時接受 tag 或 tar，但一句話未交代含 `/`、`.tar`、檔案存在及兩種判定同時成立時回 1 的消歧規則，必修／選修：必修}
- {頁：02，條目：所有含 `--dry-run` 的列，類別：遺漏，一句說明：除 upgrade 外未說明 dry-run 是唯讀預覽但仍可能拉 image 展開，使用者無法由動詞表判斷副作用，必修／選修：必修}
- {頁：02，條目：全表語法，類別：遺漏，一句說明：D 明定所有動詞都接受 `--help`，本頁語法皆省略卻未設一條共同語法通則，必修／選修：選修}
- {頁：02，條目：全頁用詞，類別：定義不清，一句說明：`metadata`、`tracked`、`hash`、`symlink`、`image ID`、`正式版`、`預檢`、`dry-run` 等反覆出現但未納入第 0–2 頁名詞表，違反共同字典規則，必修／選修：必修}
- {頁：02，條目：本頁名詞「快路徑」，類別：定義不清，一句說明：只比「印記第一行與版本鎖定行」沒有說是逐工具全部相符，且 D／E 還要求檢查 cache、gen、本機覆寫與 `.tmp.*` 等條件，需完整列出，必修／選修：必修}
- {頁：02，條目：`sync` CI 模式欄，類別：遺漏，一句說明：D 還規定 CI 模式下任何本機覆寫與基準版落後均回 1、未納管／拒絕過只提醒不紅燈；本列只列前半，易誤解所有初始檔提醒都失敗，必修／選修：必修}

## 6 點判定

1. 同意：CI 模式定義改成「不查最新版，`update` 除外」；`update` 的唯一用途就是唯讀查詢，禁止查詢會使它在 CI 中失去契約意義，也與 D、E 的既有定案不符。

2. 同意：完整驗收 harness 應明確以 `CI=0` 執行會寫檔的 `install`／`add`／`upgrade` 流程；另開獨立案例設 `CI=1` 驗證唯讀與拒寫行為，不能依賴 GitHub Actions 的環境預設。

3. 同意：`install`、`uninstall`、`undev`、`prune` 以共同 CI 通則為準，不必逐列複寫；表格只寫偏離通則的例外，例如 `dev` 明確拒絕、`update` 仍查詢，並刪除「規格未載／待拍板」字樣。

4. 同意但須精確化：`prune` 保留版本鎖定行及本機覆寫實際引用的 image；工具的 `path:<dir>` 覆寫沒有 image 可保留，引擎 tag／image ID 覆寫才加入保留清單。

5. 同意：內部子命令 `materialize` 改名為 `fetch`，與第 0 頁「取件 `fetch`」模組一致；雖非對外介面，兩套名稱會妨礙文件追蹤與實作對照。

6. 同意：第 0 頁 `update` 改成「不寫任何檔，執行紀錄除外」或直接「只寫執行紀錄」；後者與 `help`、D 的檔案矩陣及全域紀錄不變量最一致。

總評：目前不能交給使用者定稿；至少須先修正 CI／update、進度檔與 dev、檔案分類、自描述首行、缺漏選項及所有前引違規。
