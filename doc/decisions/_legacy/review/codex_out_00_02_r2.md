OpenAI Codex v0.155.0
--------
workdir: <scratchpad>/decisions
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 01a0b9ee-1fdc-76b1-9b4c-8c48617cdb8c
--------
user
你是設計審查員（第二輪）。vendor_kit 是一個工具：下游 repo 把 dist/ 打成純資料容器 image，下游使用者的專案用 bootstrap.sh + `just vendor_kit <動詞>` 取得工具、鎖版本、三方合併初始檔。我們正在由外而內審對外契約。附件 A/B/C 是修正後的三頁（A = 第 0 頁名詞與縮寫、B = 第 1 頁不變量與角色、C = 第 2 頁動詞介面表），D 是規格 §0–§2（正本文首至 §3 之前），E 是你第一輪的 56 條發現（已全部採納並修正）。
請 (1) 逐條核對 56 條是否已修、有無改壞——每條標「已修／未修／改壞」，未修或改壞的給一句說明；(2) 再找新的矛盾、前引、未定義名詞、遺漏、讀不懂的句子（規則同第一輪：頁 N 只用第 0 頁與前面頁的詞、不得引用後面的頁；名詞一律用第 0 頁的新名；也要對照 D 規格找 A/B/C 之間及與 D 的矛盾）；(3) 最後一句總評：三頁能否交給使用者定稿。

請以繁體中文回答，格式：
第一段「56 條核對」：每條一行 {#, 已修／未修／改壞, 一句說明（已修者可留空）}。
第二段「新發現」：逐條列出 {頁, 條目 id 或引文, 類別（矛盾／定義不清／前引違規／遺漏／建議）, 一句說明, 必修／選修}。
最後一句「總評」。

==================================================
附件 A：00 名詞與縮寫（decisions/review/00_terms.md）
==================================================
# 審閱頁 00：名詞與縮寫

本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。

## 三方與承諾關係

| 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
|---|---|---|---|
| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |

同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。

兩種 repo 要分清楚：

| 中文名 | 英文 | 定義 |
|---|---|---|
| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 GHCR。`<repo>` 是它的名字 |

## VK 組件（component）

VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。

- **引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。
- **薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述首行與 hash 契約。
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
| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
| **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
| **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行 `<repo> = "…:<tag>@sha256:<digest>"`；進 git；只有這行決定裝哪一版 |
| **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時複製（copy）或插入幾行（append）進專案的檔；建立後歸下游使用者、進 git |
| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
| **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
| **可寫動詞** | writing verb | 會寫進 git 的檔、或會恢復進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、undev、prune、dev |
| **唯讀動詞** | read-only verb | 不寫進 git 的檔、也不恢復進度檔的動詞：update、sync、help。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
| **進度檔** | progress file | 可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用） |
| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞每次執行一檔；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事 |
| **CI 模式** | CI mode | 環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查） |
| **需人處理** | needs human | 動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色 |
| **失敗** | failure | 拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色 |
| **專案檔四原則** | four rules | ① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容） |
| **預檢** | precheck | 動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動 |
| **介面版** | protocol version | 薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關 |
| **檔案版** | schema version | VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔 |
| **最低介面版** | floor | 引擎仍支援的最低介面版；固定常數；只能經 ADR 提高 |
| **結束碼** | exit code | `0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記）；`3` 介面版／檔案版不合，先升級或退回，零寫入 |
| **本機覆寫** | local override | `version.local.toml` 內由 dev 寫的那一行：工具指到本機目錄、或引擎指到本機 image；不進 git；有就優先於版本鎖定行 |
| **symlink** | symlink | 符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄 |
| **hash** | hash | 檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述首行、印記、指紋重驗 |
| **image ID** | image ID | docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同 |
| **tty** | tty | 互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束 |
| **佔位符** | placeholder | `<repo>` 下游 repo 名；`<ns>` 工具的 just 命名空間；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id |

### 其他既有詞

| 中文名 | 英文 | 定義 |
|---|---|---|
| **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
| **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
| **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔 |
| **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
| **自描述首行** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；放首行，檔案有 shebang 時（`ci/check.sh`）放第二行；引擎重算比對，不符就不動 |
| **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |

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
- `--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔；但仍會拉 image 展開（要看到新版內容才算得出）。
- `--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。
- `--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。

## 動詞

寫法：小寫原文，前面省略 `just vendor_kit`。

| 動詞 | 做什麼 |
|---|---|
| `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；再跑 = 冪等修復；不做 `git init` |
| `uninstall` | 移除 VK 自產的檔與根 `justfile` 那一行；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
| `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
| `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
| `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
| `upgrade [<repo>[@<tag>]]` | 升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行 |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔 |
| `undev <repo>`／`undev vendor_kit` | 撤銷 dev，回到版本鎖定行的版本 |
| `sync [<repo>]` | 依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發 |
| `prune` | 刪版本鎖定行未引用的舊 image、殘留容器／network／volume 與暫存 |
| `help` | 印命名空間層說明；不觸網、只寫執行紀錄 |

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

### 出處對照（本次修訂依據）

來源：`decisions/review/codex_findings_00_02.md`（00 頁 #1–#16、用詞 #34／#54）、`decisions/grilling.md`「02 頁 6 點定案」「兩條新規則」「補三條不變量」「專案定名」（2026-09-20）、`decisions/interface_spec.md` v3.3 §0、§1.1、§1.2、§4.1–§4.6。

==================================================
附件 B：01 不變量與角色（decisions/review/01_invariants_roles.md）
==================================================
# 審閱頁 01：不變量與角色

本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。

## 一句話目的

下游 repo 把要交付的檔案打成一個純資料的下游 image 公開；下游使用者在專案裡跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。

## 本頁名詞（第 0 頁沒有的頁內特有詞）

- GHCR：GitHub 的容器 registry；下游 image 與引擎放的地方。
- `config.toml`：`.vendor_kit/config.toml`，VK 的設定檔，進 git；升引擎時比照初始檔三方合併。
- 衝突標記：三方合併合不起來時留在檔內的 `<<<<<<<`／`>>>>>>>` 標記；升版逐檔的結果：沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 三方合併，合不起來就留衝突標記、結束碼 2。
- append 型初始檔：`strategy = append` 的初始檔，`add` 時把幾行插進專案既有檔而不是整檔複製。
- 交付物：工具 recipe（`just <ns> …`）產生、要交給別人用的東西（例如 deploy 包）。
- 契約檢查腳本：`.vendor_kit/ci/check.sh`，薄殼之一，兩種用法分開：不帶參數 = 下游 CI 的唯一入口（在專案裡跑同步、驗證、試跑升版、工具與專案測試）；`--dist` = 下游開發者在下游 repo 裡驗 `dist/` 佈局與兩平台一致。
- 下游 CI：專案自己的 CI 平台；不是「方」。
- Renovate：下游使用者自選的版本更新機器人；不是「方」。

## 三方角色與承諾關係

| 名稱 | 是誰 | 負責 | 不負責 | 地位 |
|---|---|---|---|---|
| **下游開發者** | 開發下游 repo 的人 | 維護 `dist/` 與三行 Dockerfile；在下游 repo 的 CI 用契約檢查腳本 `--dist` 驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；下游 image 公開與否自決；用 dev／undev 在本機開發工具 | 不碰專案的檔；交付物不得依賴 `.vendor_kit/`；binary 可執行性不由 VK 代驗 | 被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了 |
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
- **I4 結束碼語意**：0 成功（含 warn）；1 需人處理或失敗；2 合併衝突（留標記、基準版仍推到新版；update 加 `--exit-code` 時，有新版亦 2）；3 介面版／檔案版不合，須先升級或退回。「回 1 時版本鎖定行不動」適用 add、`upgrade <repo>`、remove、uninstall（寫入前檢查；鎖定行最後才寫／最後才刪）；remove／uninstall 回 1 時留下的狀態 = 該工具仍鎖定、`cache/` 等其餘檔可能部分已刪，進度檔保留、下次可寫動詞先恢復（uninstall 已做完的工具已整個移除、未處理的原樣）；升引擎是唯一例外（引擎那一行已改後才回 1 要求重跑）。多工具動詞做得完的做完，最後回最需處理的碼（1 > 2 > 0）。
- **I5 回 3 零寫入**：除執行紀錄在啟動時已寫下的開頭記錄外完全不寫——不寫專案檔、不寫 `cache/`、`gen/`、進度檔；新舊一律比介面版／檔案版，不比版本字串；最低介面版檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。
- **I6 需人處理／失敗語意**：需人處理的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。
- **I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；契約檢查腳本自己把 `CI` 設為 1；本機手設 = 唯讀驗證，允許。`-y` 與 CI 模式為獨立開關：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`。CI 模式下升為失敗的警告明列：薄殼不符、基準版落後、未完成接入、任何本機覆寫、需改進 git 的檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`。唯一例外：`update` 在 CI 模式仍查最新版（它是唯讀動詞，查詢就是它的用途）。
- **I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 CI 模式（CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關）。需詢問但無法互動（無 tty／EOF）又沒給 `-y` → 以 1 結束並印出原因（加 `-y` 或在終端執行）；EOF／Ctrl-C = 中止不套用、不記為拒絕過。
- **I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、GHCR，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。
- **I10 專案根與巢狀**：專案根 = 專案內含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，sync 亦無例外，否則以 1 結束並印出該到哪個目錄執行（工具 recipe 自動觸發的那次 sync 自己先切到專案根，不受影響）。
- **I11 進度檔**：所有可寫動詞（含 dev、第一次 install、升引擎）在第一個寫入前必建進度檔，不設例外；可寫動詞開始前遇未完成交易先恢復再繼續；唯讀動詞只偵測不恢復（sync／update 印出未完成交易與恢復指令後以 1 結束，help 印出後仍 0）。
- **I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只預覽不寫的執行）必寫一檔。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可以在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄（不是 git 目錄時也無處可寫）；建目錄＋建檔＋寫開頭記錄失敗 → 1、印出無法寫入的原因、零寫入；引擎啟動記錄寫不進亦同；沒有關掉它的選項。
- **I13 薄殼人不改**：自描述首行 hash 不符 → 1 列差異不動；重產只由明確動作（install／`upgrade vendor_kit`）做。
- **I14 兩層相容承諾**：救援路徑對任何 ≥ 最低介面版的薄殼永久可用；新版引擎讀歷史 VK 資料永遠可讀、可遷（讀到舊檔案版直接寫成當前檔案版）；舊薄殼呼叫介面版不合的新引擎跑一般動詞，只保證乾淨回 3；最低介面版只能經 ADR 提高。
- **I15 檔案版與未知欄位**：VK 寫的每個 TOML 都有檔案版；讀時忽略未知欄位、寫時保留（不能保留就拒絕寫）；檔案版高於本引擎支援 → 3 零寫入；讀任一舊檔案版直接寫成當前檔案版，不鏈式遷移。
- **I16 多工具動詞先完整預檢**：會寫檔且一次處理多個工具的動詞（不帶 `<repo>` 的 upgrade、uninstall）先對全部工具預檢完才動任何東西；任一預檢不過 → 整體不動、以 1 結束並列出原因。預檢過了才開始寫，寫的過程中失敗適用 I4（做得完的做完、進度檔保留）。
- **I17 `gen/tools.just` 與 `cache/` 同次原子替換**：`tools.just` 在同一次寫入裡最後寫，並與 `cache/` 一起原子替換，任何時刻都不會出現「工具入口指向不存在或半套的 cache」。

## 例外清單（不變量的明文例外）

- 根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\t@just --list`）；有 → 問後加 import 一行；uninstall 只刪完全相同的行。
- 根 `.dockerignore`（I1「永不刪」的明文例外）：install 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；只有 uninstall、經詢問、且該行原文仍與 VK 當初寫的相同時，才逐行刪；被改過或缺失的行跳過並 warn。
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

其餘三條原列矛盾（零寫入的執行紀錄例外、根 `.dockerignore` 四行、舊薄殼跑介面版不合的新引擎回 3）維持規格所載。規格仍待定的三項（啟動器讀設定檔的方式、外部 repo 反向採用紀錄腳本、紀錄事件名清單待審）不在本頁範圍。

## 出處對照（條號 → 來源）

來源檔：spec = `decisions/interface_spec.md` v3.3；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`；codex = `decisions/review/codex_findings_00_02.md`。來源原文用的是舊詞（工具 repo、下游專案、鎖定行、frozen、進度日誌、操作紀錄檔、協定號／schema 號／floor…），對照第 0 頁的新名。

| 條目 | 來源 |
|---|---|
| 一句話目的 | spec 文首、§4.7；grilling Q1、Q21 |
| 三方角色表 | spec §3.1、§4.5、§4.7、§7.1、§7.2、§7.3；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則與名詞定案（2026-09-20）；`--dist` 與下游 CI 入口分開 = codex #17；衝突要手動編輯再重跑 = codex #18、spec §1.2 upgrade 結束碼 2 |
| 兩個自動化角色 | spec §7.1、§7.3；grilling CI 平台定案、相容性其餘採納（Renovate major 分開 PR） |
| 名詞：`config.toml`、衝突標記、append 型 | spec §0、§4.6、§4.9；v2.12 L3′；grilling Q6、Q12、Q13 |
| 名詞：交付物、契約檢查腳本 | spec §4.7、§7.1、§7.2；grilling deploy 包定案 |
| I1 | grilling 隔離題定案；spec §0 |
| I2 | grilling Q10；spec §0、§1.2 sync、§3.6 |
| I3 | spec §0、§4.10、§6；grilling Q6；失敗只保證原因 = codex #19 |
| I4 | grilling Q23、Q27、「codex 修正後的 12 個疑慮取捨」（remove／uninstall 鎖定行最後刪）；spec §1.2 remove／uninstall、§2；適用動詞明列 = codex #20 |
| I5 | grilling Q23；spec §0、§2；例外 = v2.13 P12；完全不寫 = codex #21 |
| I6 | grilling 2026-09-20、01 頁拍板 (4)；v2.10-1；spec §0「結束的兩種語意」、§6 類別欄 |
| I7 | grilling 16 條必修、Q5、Q15、01 頁拍板 (3)、02 頁 6 點定案 ①；spec §0；check.sh `export CI=1` = spec §7.1；update 例外 = codex #22 |
| I8 | grilling 16 條必修、Q13、19 條-6、01 頁拍板 (3)；spec §0（訊息 6-4） |
| I9 | grilling deploy 包定案、Q14；spec §4.7 |
| I10 | grilling Q20 定案（改）、Q20 修正、01 頁拍板 (1)(2)；spec §0（訊息 6-9、6-35；sync 豁免已撤回） |
| I11 | grilling 進度日誌條、2026-09-20（v2.11-1、v2.10-6）、新規則 (b)；spec §0（訊息 6-33）；第一次 install 也建 = v2.13 P5；dev 也建 = codex #23／#47 |
| I12 | grilling 2026-09-20 新需求、L1–L6 定案、新規則 (a)；v2.12 L4；spec §0、§4.10（訊息 6-38）；順序 = codex #8／#26 |
| I13 | grilling Q10、Q17；spec §4.5、§8-6 |
| I14 | grilling Q16、Q23；spec §3.5、§8-3～5；限定語 = codex #27／#28 |
| I15 | spec §4 通則、§8-7；grilling 補三條不變量；codex #30 |
| I16 | spec §1.2 upgrade（不帶 repo 先完整預檢）、§1.2 uninstall（先預檢全部工具）；grilling 補三條不變量；codex #32 |
| I17 | spec §4.4 `gen/tools.just`、§8-9；grilling 補三條不變量；codex #33 |
| 例外：根 justfile | grilling 隔離題 A、16 條必修；spec §4.5 |
| 例外：根 `.dockerignore` | grilling Q22 補（三行）；第四行 = v2.13 P13；spec §4.5；標明只在 uninstall 逐行刪 = codex #29 |
| 例外：初始檔換版／三方合併 | grilling 隔離題 C；v2.12 L3′；spec §0 |
| 例外：append 型初始檔 | grilling Q6、Q12、Q13 |
| 例外：新版刪除的初始檔 | grilling 第 1 頁便條回覆 |
| 例外：`log/` | v2.12 L1；v2.13 P4、P6；spec §0、§1.2、§4.10 |
| 例外：進度檔與 `.tmp.*` | spec §0、§4.6 |
| 本頁待拍板（四點已定） | grilling「01 頁四點拍板（2026-09-20）」；spec §9.1 P1–P3 |
| 原矛盾 1–7（已解） | 1、2、3、4 = 01 頁四點拍板 2026-09-20（grilling「01 頁四點拍板」；spec §0、§2、§6）；5、6、7 維持 spec（v2.13 P12、P13；§2、§8-5） |

==================================================
附件 C：02 動詞介面表（decisions/review/02_verbs.md）
==================================================
# 審閱頁 02：動詞介面表

本頁列 `just vendor_kit <動詞>` 的 11 個動詞、升引擎與 `bootstrap.sh`，只放契約層：語法（照第 0 頁記法）、做什麼、寫哪類檔、結束碼、CI 模式；步驟細節屬於各流程圖，表末「流程」欄只寫流程名。只用第 0、1 頁的詞，只摘錄規格、不新增決議，出處在文末。審閱方式：逐列看是否與你認知一致，不一致的寫一句理由。

## 本頁名詞（第 0、1 頁沒有的頁內特有詞）
- 快路徑：`sync` 不帶參數（含工具 recipe 自動觸發的那次）時，啟動器不起容器就判定「沒事做」的條件，要**全部**成立：① `gen/.stamp` 第一行 = 引擎的版本鎖定行；② 每個工具的印記第一行 = 該工具版本鎖定行的 digest（或本機覆寫的 `path:<dir>`）；③ `gen/tools.just` 存在；④ 沒有任何進度檔；⑤ 非 CI 模式。全成立 → 0；任一不成立 → 起引擎。
- 指紋重驗：兩段式動詞（先算計畫、拉 image，再寫入）在寫入前重算專案狀態的指紋，與計畫不同就不寫、以 1 結束並要求重跑。
- 離線包：release 附的 `docker save` tar 與同名 `.digest` 旁檔（正式 digest）；`--local` 用它。

## 通則（每個動詞都適用，表內不重複）
1. 執行紀錄：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；建不了 → 1 零寫入，沒有關掉它的選項。
2. 專案根：只准在專案根執行，否則 → 1 印出該到哪個目錄；`sync` 被工具 recipe 自動觸發的那次自己先切到專案根。
3. 進度檔：可寫動詞（含 dev）在第一個寫入前建進度檔、成功即刪，開始前遇未完成交易先恢復再繼續；唯讀動詞遇到只印恢復指令：`sync`、`update` → 1，`help` 印出仍 0。
4. `-y` 與 CI 模式是兩個獨立開關：`-y` 只省略詢問（需詢問但無 tty 又沒 `-y` → 1），不授權覆蓋、不硬加；CI 模式 = 不寫任何進 git 的檔、不查最新版（`update` 除外），需改進 git 的檔 → 1 印清單（與 `-y` 無關），仍拉鎖定版 image、仍寫 `cache/`、`gen/`；下表 CI 模式欄只寫偏離此通則的例外。
5. 結束碼 3（介面版／檔案版不合）一律零寫入（執行紀錄開頭除外）；網路、認證、不存在 → 1，不得偽裝成 3；不帶 `<repo>` 的動詞逐工具做完後回最需處理的碼：有任何 1 → 1，否則有 2 → 2，否則 0；每個工具的訊息全部保留列出。
6. `--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；但仍拉 image 展開（要有新版內容才算得出）；CI 模式下需改進 git 的檔 → 1 印清單。
7. `--help`：所有動詞都接受，印用法後 0；語法欄不重複列。

## 動詞表
「寫哪類檔」簡寫：鎖定行＝版本鎖定行、基準版＝基準版與 metadata、cache＝`cache/`、gen＝`gen/`（印記、`tools.just`）、薄殼＝薄殼五檔與 `gen/.stamp`、`config.toml`、本機覆寫＝`version.local.toml`、進度檔、專案檔＝根 justfile／`.dockerignore`／初始檔（薄殼與 `config.toml` 是 VK 檔，不歸專案檔）；執行紀錄每列都寫、不列；「（皆刪）」＝該列只刪不建。

| 語法 | 一句話 | 寫哪類檔 | 結束碼 | CI 模式 | 流程 |
|---|---|---|---|---|---|
| `install [-y] [--no-justfile]` | 第一次接入：建 `.vendor_kit/`（引擎鎖定行、`config.toml`、薄殼五檔、空 `baseline/`、`gen/.stamp`），根 justfile 無 → 建四行、有 → 問後加一行，根 `.dockerignore` 無 → 建四行、有 → 問後加四行；`--no-justfile` = 跳過根 justfile 那一步、只印手動加那一行的指示；再跑 = 修復（薄殼首行相符才重寫）；`install <repo>` → 1 改用 `add` | 鎖定行、`config.toml`、薄殼、專案檔、進度檔 | 0；1 需人處理（非 git repo、巢狀 `.vendor_kit/`、薄殼被改、需詢問無 tty）／失敗（清掉半成品、`log/` 保留）；3 | 同通則 | install(1)(2) |
| `uninstall [-y] [--dry-run]` | 先對全部工具預檢（任一在 dev 中或不可移除 → 整體不動、1）；過了才逐工具照 `remove` 做（各工具的鎖定行在該工具其餘檔刪完後才刪），再只刪 hash 相符的 VK 自產檔與自己加在根 justfile／`.dockerignore` 的行；被改過的保留並列出；初始檔不刪只印清單；`log/` 一律保留 | 鎖定行、基準版、cache、gen、薄殼、`config.toml`、本機覆寫、專案檔、進度檔（皆刪） | 0；1 需人處理（預檢失敗：dev 中、需詢問無 tty → 整體不動）／失敗（開始刪之後任一工具失敗 → 中止、列出已完成與未處理的部分；該工具鎖定行不動、進度檔保留）；3 | 同通則 | uninstall(1)(2) |
| `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | 接入一個工具：解析版本（沒指定 → 最新正式版）、拉展開、指紋重驗，建初始檔（copy 型已存在不納管、`-y` 也不覆蓋；append 型問後加行）、存基準版、重生 `gen/tools.just`，最後寫鎖定行；已接入且沒指定 tag（或 tag 相同）→ 0；已接入且指定的 tag 與鎖定行不同 → 1 改用 `upgrade`；撞名／越出專案／私有無憑證 → 1，全在寫入前檢查 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（撞名、拒絕、沒憑證、需詢問無 tty）／失敗（拉不到或逾時、指紋不同；鎖定行一律未動）；3 | 同通則 | add(1)(2)(3) |
| `remove <repo> [-y] [--dry-run]` | 移除該工具的 `cache/<repo>/`、基準版、印記與 `tools.just` 內的行，最後才刪鎖定行；append 過的行問後只刪原文相同的；初始檔不刪只印清單；未接入 → 0；不帶 `<repo>` → 印用法、1 | 鎖定行、基準版、cache、gen、專案檔、進度檔（皆刪） | 0；1 需人處理（dev 中、需詢問無 tty）／失敗（指紋不同、寫不進；鎖定行不動、進度檔保留，工具仍鎖定而 `cache/` 可能部分缺）；3 | 同通則 | remove(1)(2) |
| `update [<repo>] [--exit-code]` | 查 registry 最新正式版與鎖定行比對、逐一列出（不帶 = 全部，含引擎）；私有無憑證 → 該工具 1、其他照查；末行固定印「套用：just vendor_kit upgrade」；不拉 image | －（只寫執行紀錄） | 0；1 需人處理（任一工具查不到 → 整體 1）；`--exit-code` 且有新版 → 2；3 | 例外：仍查 registry（唯讀，本來就不寫進 git 的檔） | update |
| `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | 升到最新（或指定）版：拉展開、指紋重驗、換 `cache/`，初始檔逐檔問（沒改 → 換；只有你改 → 不動；兩邊改 → 三方合併、衝突留標記；新增問建、拒絕記下不再問；刪除只 warn），基準版推到新版（衝突仍推），最後寫鎖定行；先補「鎖定行已新、基準版仍舊」；不帶 `<repo>` 先對全部工具完整預檢，引擎有新版 → 本次只升引擎；`@<tag>` 只配單一 `<repo>`，比現版舊 → warn 仍做 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（沒基準版先 `add`、dev 中、需詢問無 tty）／失敗（拉不到、指紋不同、合併程式出錯）；2 衝突（留標記、基準版仍推，手動編輯後重跑直到乾淨）；3 | 同通則；`--dry-run` 就是契約檢查腳本用的那一步 | upgrade(1)–(6) |
| `upgrade vendor_kit[@<tag>] [-y] [--dry-run]`（升引擎；`upgrade` 不帶 `<repo>` 遇引擎新版時由啟動器自動接手） | 定目標（指定 `@<tag>` 不查 registry）→ 建進度檔 → 改引擎鎖定行 → 啟動器改用新引擎重跑 → 重產薄殼五檔與 `gen/.stamp`，`config.toml` 缺則建、有則三方合併 → 刪進度檔 → 1 要求 commit 後再跑原指令；目標 = 現版且薄殼相符 → 0；薄殼被改 → 1 列差異不動；鎖定行已改但新引擎拉不到、ID 不符或重產失敗 → 1，進度檔保留、印可複製的恢復指令 `just vendor_kit upgrade vendor_kit`（下次任何可寫動詞也會先恢復）；降版須能無損讀現有檔，否則 3 印「請 git revert」 | 鎖定行（引擎那行）、薄殼、`config.toml`、基準版（`config.toml` 副本）、進度檔 | 0 無變更；1 需人處理（重產完成要 commit 再跑、薄殼被改、鎖定行已改但新引擎拉不到）／失敗（鎖定行未變時重產失敗）；3 降版無法無損讀（零寫入） | 沒指定 `@<tag>` → 不查、目標 = 現版 | 升引擎(1)–(3) |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 寫本機覆寫：工具的 `cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；引擎記 tag 與 image ID，之後只驗 ID、不拉；單段、不拉 image；建進度檔；工具須已在鎖定行、`<dir>/dist/init.toml` 須存在；`-i` 只能 tag，較舊引擎不得重產薄殼 | 本機覆寫、cache、gen、進度檔 | 0；1 需人處理（不在鎖定行、缺 `init.toml`、CI 模式）；3 | 例外：一律拒絕 → 1 | dev(1)(2) |
| `undev <repo> [--timeout <秒>]`／`undev vendor_kit [--timeout <秒>]` | 撤本機覆寫那一行（撤的是最後一行則刪整檔），依鎖定行重新拉展開 `cache/`（引擎不展開，下次 `sync` 只提示升引擎）；未啟用 → 0 | 本機覆寫、cache、gen、進度檔 | 0；1 失敗（拉不到、寫不進；進度檔保留）；3 | 同通則 | undev(1)(2) |
| `sync [<repo>] [--verify] [--timeout <秒>]` | 快路徑全成立 → 0 不起容器；否則依鎖定行重建 `cache/`、`gen/`：引擎版 ≠ `gen/.stamp` → 1 跑升引擎；本機覆寫的工具跳過；印記 ≠ 鎖定 digest → 重拉；`--verify` 逐檔驗指紋、不符重裝；未完成接入 → 1 跑 `add`；基準版落後 → warn 提示 `upgrade`；工具 recipe 執行前自動觸發 | cache、gen | 0；1 需人處理（薄殼不符、未完成接入、未完成交易）／失敗（拉不到或逾時、寫不進）；3 | 一律逐檔驗指紋；薄殼不符、基準版落後、未完成接入、任何本機覆寫都升為 1；「未納管／拒絕過」只提醒、不紅燈 | sync(1)–(3) |
| `prune [-y] [--dry-run]` | 保留清單 = 鎖定行引用的 image ＋ 本機覆寫中引擎的 tag／image ID 覆寫實際引用的 image（工具的 `path:<dir>` 覆寫沒有 image、不列）；啟動器依 VK 標籤列出其餘容器／image／network／volume、問後逐一刪；引擎清失效暫存與已完成交易的殘留；未恢復的進度檔只提示、不刪不擋；執行紀錄不歸它清 | 進度檔、暫存；docker 資源 | 0；1 需人處理（需詢問無 tty）／失敗（磁碟滿到執行紀錄寫不進）；3 | 同通則 | prune |
| `help`（別名 `h`） | 印命名空間層說明，明寫「已接入的專案跑 sync，不是 install」；不觸網、不安裝、不偵測狀態；遇未完成交易印恢復指令仍 0 | －（只寫執行紀錄） | 0；1 只在執行紀錄寫不進 | 無差異 | — |
| `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag／tar>] [--timeout <秒>] [-h]` | 第一次接入的啟動器：檢查 git repo 與 just ≥ 1.33.0，建執行紀錄，拉（本機有就不拉）引擎 image，跑 `install`，再逐個 `-t` 依序跑 `add`，任一非 0 立即中止、整體 1、列出已完成與未處理；專案已有 `version.toml` 就用那行的引擎，只有第一次才用內嵌版本；`--local` 的值：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在），其餘 → image tag，兩者都成立 → 1 要求改寫；tar 由 `.digest` 旁檔取正式 digest、tag 只驗本機 ID 記成本機覆寫；再跑 = 修復 | 經 `install`、`add` 寫的全部；`--local` 時本機覆寫（`install` 成功後才寫） | 0；1 需人處理（非 git repo、just 太舊、需詢問無 tty）／失敗（拉不到、`install` 失敗不留半成品、任一 `add` 失敗）；3 | 同 `install`、`add` | bootstrap(1)(2)；離線包(1)(2) |

## 本頁待拍板

無；六點已定（2026-09-20，codex 一致）：
1. CI 模式定義加「`update` 除外」（第 0 頁、通則 4、update 列）。
2. 驗收 harness 明確設 `CI=0` 跑完整流程；另設 `CI=1` 案例驗唯讀與拒寫。
3. `install`、`uninstall`、`undev`、`prune` 在 CI 模式靠通則；表只寫偏離通則的例外（`dev` 拒絕、`update` 仍查）。
4. `prune` 保留清單 = 鎖定行 ＋ 本機覆寫實際引用的 image（引擎 tag／ID 覆寫有；工具 `path:<dir>` 無）。
5. 引擎內「拉 image 展開」的內部子命令改名 `fetch`，與第 0 頁模組名一致（內部名、不對外）。
6. 第 0 頁 `update` 改「只寫執行紀錄」。

## 出處（定稿時移除）

通則：spec §0、§1.1（`--dry-run`、`--help`、`--timeout` 適用欄）、§1.2 通則；grilling 01 頁四點拍板 2026-09-20／Q23／Q27／19 條-6、新規則 (a)(b)；codex #37–#40、#52、#53。各動詞：spec §1.1 選項總表、§1.2 動詞表、§2 結束碼總表、§2c 動詞×檔案矩陣、§3.4、§3.6 快路徑、§6 訊息文字；install `--no-justfile` = codex #42；uninstall 兩種失敗 = codex #43、spec §1.2 uninstall；add `@<tag>` = codex #44；update CI 例外 = codex #45、6 點定案 ①③；升引擎恢復 = codex #46、spec §3.4（6-2b）；dev 進度檔 = codex #47、新規則 (b)；undev／sync `--timeout` = codex #48／#49、spec §1.1；prune 保留清單 = codex #50、6 點定案 ④；bootstrap `--local` 消歧 = codex #51、spec §1.1 B1；快路徑條件 = codex #55、spec §3.6；sync CI 欄 = codex #56、spec §0 CI 模式；「流程」欄改流程名 = codex #35；簡寫歸類 = codex #36／#41。流程名對應主圖頁序見 `review_v2_out/pages.json`（最終以推送後為準）。

==================================================
附件 D：規格 §0–§2（decisions/interface_spec.md 文首至 §3 之前）
==================================================
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
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分（該工具鎖定行不動，見 remove；已完成的工具已整個移除）<sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7；grilling 12 個疑慮取捨]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；**config.toml** 比照初始檔保護模式：hash == `baseline/vendor_kit/config.toml` 副本 → 刪，被下游使用者改過 → 留下並列出（永不刪下游使用者改過的檔）；**`log/` 一律保留**（uninstall 自己也在寫）、不 rmdir `log/`，`.vendor_kit/` 因此保留（只剩 `log/`），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪；進度檔 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12；v2.13 P6；v2.14-6]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的四行同 append 規則問後只刪原文相同的；append 行問後**逐行**比對、只刪仍與紀錄原文相同的行，缺失／被改的行跳過並 warn（不是全有／全無）<sub>[proposal §2、§5；grilling Q22 補；v2.9-5]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留） | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；`--local <v>`：`<v>` 必須是存在的 `.tar` 檔（不收 image tag 形），否則 1 + 6-24（add `--local` 分句）；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`（只收 tar）：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26；v2.10-3]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
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
| 1 | 一般失敗、需人處理／重跑；「工具層動詞回 1 時 version.toml 不動」適用 add／`upgrade <repo>`／remove／uninstall（寫入前檢查；鎖定行最後才寫／最後才刪）；remove／uninstall 回 1 時其餘檔（cache/、baseline/、gen/）可能已部分刪除（工具仍鎖定），進度檔保留、下次可寫動詞先恢復 <sub>[proposal §2；compat 條 4；codex 00–02 #20；grilling 12 個疑慮取捨]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3；所有動詞（含 help／prune）執行紀錄建檔或 `launcher_start`／`engine_start` 寫入失敗 → 1 + 6-38（零寫入）；bootstrap.sh 任一 `-t` 的 add 失敗 → 1 中止 <sub>[v2.3 §2；grilling Q23；v2.12 L4；r9]</sub> |
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



==================================================
附件 E：第一輪 56 條發現（decisions/review/codex_findings_00_02.md）
==================================================
# codex 獨立審查結論（00／01／02 頁 vs 規格 §0–§2）

來源：`decisions/review/codex_out_00_02.md`（codex exec, sandbox read-only, brief = `codex_brief_00_02.txt`）。以下為 codex 原意的結構化整理，未加入整理者意見。

## 逐條清單

| # | 頁 | 條目 id／引文 | 類別 | 說明 | 必修？ |
|---|---|---|---|---|---|
| 1 | 00 | 「薄殼」／「自描述首行」 | 矛盾 | 本頁稱薄殼五檔都在首行放自描述，但 D／E 明定 `ci/check.sh` 第一行是 shebang、自描述在第二行，且 `log.sh` 表頭位置未說清楚 | 必修 |
| 2 | 00 | 「薄殼」五檔 | 定義不清 | E 的 Q17 只列 `entry.just`、`vendor.just`、`.gitignore`、`ci/check.sh` 四檔，未交代新增的 `log.sh` 是否適用相同 hash 契約 | 必修 |
| 3 | 00 | 「專案檔」 | 定義不清 | 「不是 VK 自產的一切」易被理解成初始檔不是 VK 建立；應直接定義為根 justfile、根 `.dockerignore` 與建立後歸下游使用者的初始檔 | 必修 |
| 4 | 00 | 「VK 檔」 | 遺漏 | 清單漏掉 `version.local.toml` 與基準版旁的 metadata，後兩頁卻把它們當 VK 管理的檔案使用 | 必修 |
| 5 | 00 | 「版本鎖定行」及佔位符 `<digest>` | 矛盾 | 格式寫成 `@sha256:<digest>`，但 `<digest>` 又定義為含 `sha256:` 的值，照字面會得到 `@sha256:sha256:…` | 必修 |
| 6 | 00 | 「基準版」 | 定義不清 | 「當三方合併的第三份」無法說明角色，應明寫基準版是共同祖先，另兩份為下游使用者現況與新版初始檔 | 必修 |
| 7 | 00 | 「進度檔」 | 定義不清 | 把 `.tmp.<verb>.<id>.toml` 與「基準版旁 metadata」合稱一種檔，掩蓋兩種不同落點與生命週期；應說明哪些動詞各用哪一種 | 必修 |
| 8 | 00 | 「執行紀錄」 | 定義不清 | 「寫不進就不做任何事」與 D 中 `bootstrap.sh` 先檢查 git／just、之後才建紀錄的順序互斥；需明定前置檢查是否算「做事」並統一 | 必修 |
| 9 | 00 | 「CI 模式」 | 矛盾 | 「不查最新版」未列 `update` 例外，與 B I7、C update 及 D §0 明定 `update` 仍查 registry 衝突 | 必修 |
| 10 | 00 | 「結束碼」／「需人處理」 | 定義不清 | 同一個碼 1 同時可能是需人處理或失敗，名詞表應明說分類由訊息語意而非只由碼決定 | 必修 |
| 11 | 00 | 「install」 | 矛盾 | 「根 justfile 加一行」只適用既有 justfile；D 規定不存在時建立 import、空行、`default:` 與 recipe 共四行 | 必修 |
| 12 | 00 | 「uninstall」 | 定義不清 | 「對稱移除 VK 自產的檔」會讓人預期刪光 `.vendor_kit/`，但 D 明定保留執行紀錄、被改的 `config.toml`／薄殼及非空目錄 | 必修 |
| 13 | 00 | 「update」 | 矛盾 | 「不寫任何檔」與全域執行紀錄不變量及 D 的「只寫執行紀錄」衝突 | 必修 |
| 14 | 00 | 「dev」 | 矛盾 | 「只寫 `version.local.toml`」與 D 規定工具 dev 還會改 `cache/<repo>/` symlink 及 `gen/<repo>.stamp` 衝突 | 必修 |
| 15 | 00 | 「救援路徑」 | 定義不清 | 把 `install` 列為任何舊薄殼的救援路徑，卻沒區分第一次接入由 `bootstrap.sh` 啟動與既有薄殼修復兩種情境 | 選修 |
| 16 | 00 | 「下游 repo」／「下游使用者」 | 建議 | 「下游 repo」是提供工具的一方，而下游使用者所在 repo 沒有固定名詞，易把兩種 repo 混為一談；宜補「下游使用者專案」或等價正式名 | 必修 |
| 17 | 01 | 「下游開發者」負責欄 | 定義不清 | 「用契約檢查腳本驗 `dist/`」與後文該腳本位於下游使用者專案並跑同步、升版及專案測試的描述混在一起，需區分 `--dist` 檢查與下游 CI 驗收入口 | 必修 |
| 18 | 01 | 「下游使用者」負責欄 | 矛盾 | 「跑 `upgrade <repo> -y` 解合併衝突」不正確：`-y` 只能同意執行三方合併，留下衝突後仍須人工編輯並重跑 | 必修 |
| 19 | 01 | I3 | 矛盾 | 「每個失敗都附可直接複製的指令」比 D 契約更強；拉不到、寫不進或驗證失敗只保證原因，附下一步指令是「需人處理」的定義 | 必修 |
| 20 | 01 | I4 | 定義不清 | 「工具層動詞回 1 時版本鎖定行不動」範圍不明，`remove`／`uninstall` 可能已有可恢復的部分寫入，升引擎又是明列例外；應精確列適用動詞 | 必修 |
| 21 | 01 | I5 | 定義不清 | 「回 3 零寫入」隨後只說不寫專案檔，留下可否寫 `cache/`、`gen/`、進度檔的疑問；應明寫除執行紀錄既有開頭外完全不寫 | 必修 |
| 22 | 01 | I7 | 矛盾 | `update` 唯讀且不受影響的例外與第 0 頁「CI 模式不查最新版」直接衝突 | 必修 |
| 23 | 01 | I11 | 矛盾 | 「每個可寫動詞」且「不設例外」會包含會寫本機覆寫、cache 與 gen 的 `dev`，但 D 與 C 明定 `dev` 不建進度檔 | 必修 |
| 24 | 01 | I11 | 定義不清 | 「可寫動詞」與「唯讀動詞」沒有在第 0 頁或本頁定義，且 `sync` 其實會寫 cache／gen，不能按一般字義稱唯讀 | 必修 |
| 25 | 01 | I12 引文「`--dry-run`」 | 前引違規 | 本頁尚未定義 `--dry-run`，其語法及適用動詞到第 2 頁才出現 | 必修 |
| 26 | 01 | I12 | 矛盾 | 「啟動器在任何其他動作之前」與 D 的 `bootstrap.sh` 順序「先驗 git repo／just，再建立執行紀錄」矛盾 | 必修 |
| 27 | 01 | I14 | 定義不清 | 「舊資料永遠可讀、可遷」若不限定為新版引擎讀歷史 VK 資料，會與高檔案版回 3 以及舊引擎不能讀新資料衝突 | 必修 |
| 28 | 01 | I14 引文「新 major」 | 定義不清 | `major` 未在第 0 頁或本頁定義，且相容判斷實際依介面版／檔案版而非 SemVer major | 必修 |
| 29 | 01 | 「根 `.dockerignore`」例外 | 定義不清 | 這是對「專案檔永不刪」的明文例外，應直接標示只有 uninstall 經詢問且原文相同時可逐行刪，避免看似與 I1 衝突 | 必修 |
| 30 | 01 | 不變量整體 | 遺漏 | D 的每個 VK TOML 都有檔案版、未知欄位讀時忽略且寫時保留、跨版直接遷移等資料相容承諾未列為不變量 | 必修 |
| 31 | 01 | 不變量整體 | 遺漏 | D／E 的版本鎖定行唯一正規形、禁 BOM／重複鍵／表旁路是對外格式核心，本頁未收錄 | 必修 |
| 32 | 01 | 不變量整體 | 遺漏 | D 明定多工具動詞須先完整預檢、任一預檢失敗則整體不動；I4 只寫「做得完的做完」，漏掉這個原子性邊界 | 必修 |
| 33 | 01 | 不變量整體 | 遺漏 | D 的 `tools.just` 最後寫且與 cache 在同一 apply 內原子替換，是避免半套工具入口的重要不變量，本頁未列 | 必修 |
| 34 | 01 | 全頁用詞 | 定義不清 | `metadata`、`hash`、`tty`、`image ID`、`major`、`tracked`／「進 git 的檔」等契約詞反覆使用但未進第 0 頁或本頁名詞表 | 必修 |
| 35 | 02 | 開頭與「流程頁」欄 | 前引違規 | 本頁直接引用第 11–39 頁及 46–47 頁的後續流程，違反「頁 N 不引用後面的頁」；審閱版應移除頁碼或改成不具前引性的流程識別碼 | 必修 |
| 36 | 02 | 「寫哪類檔」簡寫 | 矛盾 | 把薄殼與 `config.toml` 歸入「專案檔」，與第 0 頁明定兩者是 VK 檔衝突 | 必修 |
| 37 | 02 | 通則 1 | 矛盾 | 「每次執行第一件事」建立執行紀錄與 D 的 `bootstrap.sh` 先驗 git／just 再建紀錄衝突 | 必修 |
| 38 | 02 | 通則 3 | 矛盾 | 「可寫動詞第一個寫入前建進度檔」與同頁 `dev`「不建進度檔」衝突，應改稱「交易型動詞」並列出集合 | 必修 |
| 39 | 02 | 通則 3 引文「唯讀動詞（`sync`、`update`）」 | 定義不清 | `sync` 會重建 cache／gen，所謂唯讀僅指不寫進 git 的檔或不恢復交易，一般人會誤讀 | 必修 |
| 40 | 02 | 通則 5 | 定義不清 | 「失敗 1 > 衝突 2 > 有新版 2」把語意與數字混排，且未說同為 1 的需人處理如何彙總；宜沿用 D 的「最需處理的碼」並另列訊息全保留 | 選修 |
| 41 | 02 | `install` 寫檔欄 | 矛盾 | 因簡寫錯誤把薄殼及 `config.toml` 列成專案檔，使用者會誤以為它們受專案檔四原則而非 VK 檔規則管理 | 必修 |
| 42 | 02 | `install` | 遺漏 | 語法列出 `--no-justfile`，一句話卻未說它跳過根 justfile 並只印手動指示 | 必修 |
| 43 | 02 | `uninstall` | 定義不清 | 「預檢任一工具不過整體不動」與結束碼欄「任一工具失敗後中止並列出已完成部分」看似互斥，需區分預檢失敗與 apply 期間失敗 | 必修 |
| 44 | 02 | `add` 引文「`@<tag>` ≠ 版本鎖定行」 | 定義不清 | 只有已接入工具才有可比較的版本鎖定行，應寫成「已接入且指定 tag 不同時改用 upgrade」 | 必修 |
| 45 | 02 | `update` CI 模式欄 | 矛盾 | 仍查 registry 與第 0 頁 CI 模式定義衝突，不能以「待拍板」狀態交付使用者 | 必修 |
| 46 | 02 | `upgrade vendor_kit` | 定義不清 | 「改版本鎖定行後才由新引擎重跑」但同列又把新引擎拉不到列為需人處理；應明寫此時版本鎖定行已改、進度檔如何恢復及可複製的恢復指令 | 必修 |
| 47 | 02 | `dev` | 矛盾 | 「不建進度檔」與頁 1 I11、頁 2 通則 3 的「所有可寫動詞」不設例外矛盾 | 必修 |
| 48 | 02 | `undev` 語法 | 遺漏 | D §1.1 明定 `--timeout <秒>` 適用 `undev`，本頁語法未列 | 必修 |
| 49 | 02 | `sync` 語法 | 遺漏 | D §1.1 明定 `--timeout <秒>` 適用 `sync`，本頁語法未列 | 必修 |
| 50 | 02 | `prune` | 定義不清 | 「本機覆寫引用的 image」只適用實際以 image tag／ID 覆寫的引擎；工具的 `path:<dir>` 沒有 image，保留清單需分別表述 | 必修 |
| 51 | 02 | `bootstrap.sh` | 遺漏 | `--local` 同時接受 tag 或 tar，但一句話未交代含 `/`、`.tar`、檔案存在及兩種判定同時成立時回 1 的消歧規則 | 必修 |
| 52 | 02 | 所有含 `--dry-run` 的列 | 遺漏 | 除 upgrade 外未說明 dry-run 是唯讀預覽但仍可能拉 image 展開，使用者無法由動詞表判斷副作用 | 必修 |
| 53 | 02 | 全表語法 | 遺漏 | D 明定所有動詞都接受 `--help`，本頁語法皆省略卻未設一條共同語法通則 | 選修 |
| 54 | 02 | 全頁用詞 | 定義不清 | `metadata`、`tracked`、`hash`、`symlink`、`image ID`、`正式版`、`預檢`、`dry-run` 等反覆出現但未納入第 0–2 頁名詞表 | 必修 |
| 55 | 02 | 本頁名詞「快路徑」 | 定義不清 | 只比「印記第一行與版本鎖定行」沒說是逐工具全部相符，且 D／E 還要求檢查 cache、gen、本機覆寫與 `.tmp.*` 等條件，需完整列出 | 必修 |
| 56 | 02 | `sync` CI 模式欄 | 遺漏 | D 還規定 CI 模式下任何本機覆寫與基準版落後均回 1、未納管／拒絕過只提醒不紅燈；本列只列前半，易誤解所有初始檔提醒都失敗 | 必修 |

統計：56 條（00 頁 16、01 頁 18、02 頁 22）；必修 53、選修 3（#15、#40、#53）。前引違規 2 條（#25、#35）。

## 6 點判定（codex 答案＋理由）

1. ① CI 模式加「update 除外」：**同意**。`update` 唯一用途就是唯讀查詢，禁止查詢會使它在 CI 中失去契約意義，也與 D、E 既有定案不符。
2. ② 驗收 harness 明確 CI=0：**同意**。完整驗收應以 `CI=0` 跑會寫檔的 `install`／`add`／`upgrade` 流程；另開獨立案例設 `CI=1` 驗證唯讀與拒寫行為，不能依賴 GitHub Actions 的環境預設。
3. ③ 其餘動詞靠通則不逐一寫死：**同意**。`install`、`uninstall`、`undev`、`prune` 以共同 CI 通則為準；表格只寫偏離通則的例外（如 `dev` 明確拒絕、`update` 仍查詢），並刪除「規格未載／待拍板」字樣。
4. ④ prune 保留清單含本機覆寫引用的 image：**同意但須精確化**。保留版本鎖定行及本機覆寫「實際引用」的 image；工具的 `path:<dir>` 覆寫沒有 image 可保留，只有引擎 tag／image ID 覆寫才加入保留清單。
5. ⑤ 內部子命令 materialize 改名對齊 fetch：**同意**。與第 0 頁「取件 `fetch`」模組一致；雖非對外介面，兩套名稱會妨礙文件追蹤與實作對照。
6. ⑥ 第 0 頁 update 改「只寫執行紀錄」：**同意**。改成「不寫任何檔，執行紀錄除外」或直接「只寫執行紀錄」；後者與 `help`、D 的檔案矩陣及全域紀錄不變量最一致。

## 總評

目前不能交給使用者定稿；至少須先修正 CI／update、進度檔與 dev、檔案分類、自描述首行、缺漏選項及所有前引違規。

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
我會先把 56 條逐一做「原問題 → A/B/C 修正文句 → D 規格」三向核對，再另外掃一次跨頁用詞、前引與規格差異。這輪我會使用 `codebase-design` 的介面審查框架，因為重點正是對外契約的邊界與一致性。
codex
`codebase-design` 的指示檔目前因工作環境的唯讀沙箱初始化失敗而無法讀取；我會依附件本身的審閱規則繼續，不讓這個環境問題中斷核對。
codex
第一段「56 條核對」

{#1, 已修, }  
{#2, 已修, }  
{#3, 已修, }  
{#4, 已修, }  
{#5, 已修, }  
{#6, 已修, }  
{#7, 已修, }  
{#8, 已修, }  
{#9, 已修, }  
{#10, 已修, }  
{#11, 已修, }  
{#12, 已修, }  
{#13, 已修, }  
{#14, 已修, }  
{#15, 已修, }  
{#16, 已修, }  
{#17, 已修, }  
{#18, 已修, }  
{#19, 已修, }  
{#20, 已修, }  
{#21, 已修, }  
{#22, 已修, }  
{#23, 已修, }  
{#24, 已修, }  
{#25, 已修, }  
{#26, 已修, }  
{#27, 已修, }  
{#28, 已修, }  
{#29, 已修, }  
{#30, 已修, }  
{#31, 未修, A「版本鎖定行」仍未寫明唯一正規形，以及禁 BOM、重複鍵與 TOML 表旁路。}  
{#32, 已修, }  
{#33, 已修, }  
{#34, 已修, }  
{#35, 已修, }  
{#36, 已修, }  
{#37, 已修, }  
{#38, 已修, }  
{#39, 已修, }  
{#40, 已修, }  
{#41, 已修, }  
{#42, 已修, }  
{#43, 已修, }  
{#44, 已修, }  
{#45, 已修, }  
{#46, 已修, }  
{#47, 已修, }  
{#48, 已修, }  
{#49, 已修, }  
{#50, 已修, }  
{#51, 已修, }  
{#52, 改壞, C 通則斷言所有 `--dry-run`「仍會拉 image 展開」，但 uninstall、remove、prune 不需要也不應因此拉 image；應改成「需要新版內容的動詞仍會拉 image 展開」。}  
{#53, 已修, }  
{#54, 已修, }  
{#55, 未修, 快路徑仍未檢查各工具 `cache/<repo>/` 是否存在且完整；印記存在但 cache 被刪時仍可能誤判為無事可做。}  
{#56, 已修, }

第二段「新發現」

{00, 「一句話目的／下游 image」與 01 下游開發者角色, 矛盾, 01 開頭說下游 image「公開」，角色表卻說「公開與否自決」；須統一是否公開為契約前提。, 必修}

{00, 「可寫動詞」, 定義不清, 定義只涵蓋「寫進 git」或「恢復進度檔」，但 prune 不寫進 git，且依 D 明定不恢復活躍交易；應改以「會建立進度檔或恢復交易」等可涵蓋完整集合的條件定義。, 必修}

{00, 「prune」, 矛盾, 寫成刪除「版本鎖定行未引用的舊 image」，漏掉本機覆寫實際引用的引擎 image 也必須保留，與 C prune 及 D §1.2 衝突。, 必修}

{00, 「install」, 遺漏, 動詞摘要只交代根 justfile，漏掉 install 也會建立或詢問追加根 `.dockerignore` 四行。, 必修}

{00, 「uninstall」, 遺漏, 動詞摘要只說移除根 justfile 那一行，漏掉經詢問逐行移除仍與原文相同的 `.dockerignore` 四行。, 必修}

{00, 「動詞表用到的選項」, 遺漏, 清單漏定義 C 使用的 `-t`／`--tool`、`--source`、`--local`、`--verify`、`--no-justfile`，與「動詞表用到的選項」的自我宣告不符。, 必修}

{01, I11 與「進度檔與 `.tmp.*`」例外, 矛盾, I11 說所有可寫動詞開始前一律先恢復未完成交易，但 D 明定 prune 遇活躍交易不恢復、不阻擋，B 的例外只說不刪，未解除「先恢復」要求。, 必修}

{01, I4「多工具動詞做得完的做完」, 定義不清, uninstall 在 apply 期間任一工具失敗會中止並留下未處理工具，並非繼續把其餘「做得完的做完」；應限定為各動詞既定的失敗策略或直接引用逐動詞規則。, 必修}

{01, I15「VK 寫的每個 TOML」, 定義不清, 「寫時保留未知欄位」未說明刪除整個檔案或整個工具項目時是否仍適用，容易與 uninstall/remove 的合法刪除行為衝突；宜限定為重寫仍存在的 TOML 文件。, 選修}

{02, 通則 3 與 prune 列, 矛盾, 通則要求可寫動詞先恢復未完成交易，prune 列卻依 D 說活躍進度檔只提示、不擋、不恢復；須在通則 3 明列 prune 例外。, 必修}

{02, 「寫哪類檔」的「（皆刪）」及 uninstall/remove 列, 矛盾, 兩列把進度檔也標為「只刪不建」，但兩動詞都必須先建立自己的進度檔，成功後才刪除。, 必修}

{02, install「寫哪類檔」, 遺漏, 一句話明列建立空 `baseline/`，D 的檔案矩陣也列為建立，但寫檔欄漏列基準版類別。, 必修}

{02, bootstrap.sh「任一非 0…整體 1」, 矛盾, 此句會把 install 的介面版／檔案版不合碼 3 也壓成 1，卻又在同列結束碼列出 3；應只把 `-t` 的 add 非 0 定義為整體 1，或明列 3 的傳遞規則。, 必修}

{02, `upgrade vendor_kit`「薄殼被改」, 定義不清, 同一句把「薄殼被改 → 1 列差異不動」放在已改引擎鎖定行並恢復交易的敘述之後，未清楚區分首次執行的前置拒絕與既有升引擎交易的恢復順序。, 選修}

{02, 本頁名詞「指紋重驗」及表內「apply」, 前引違規, 本頁定義「兩段式動詞」但未定義 resolve／apply 兩階段的契約名稱；`apply` 也不在第 0、1 頁字典，卻在 uninstall 的失敗說明與出處語境中使用。, 必修}

{02, `sync` 快路徑與通則 1, 定義不清, 快路徑宣稱「0 不起容器」，但仍必須先建立執行紀錄；應直接寫成「寫完執行紀錄後不起引擎容器」，避免被讀成完全零副作用。, 選修}

總評：三頁目前仍不能交給使用者定稿；至少須修正 #31、#52、#55，以及上述公開性、prune 交易例外、`（皆刪）`、bootstrap 結束碼等必修矛盾。
tokens used
57,924
第一段「56 條核對」

{#1, 已修, }  
{#2, 已修, }  
{#3, 已修, }  
{#4, 已修, }  
{#5, 已修, }  
{#6, 已修, }  
{#7, 已修, }  
{#8, 已修, }  
{#9, 已修, }  
{#10, 已修, }  
{#11, 已修, }  
{#12, 已修, }  
{#13, 已修, }  
{#14, 已修, }  
{#15, 已修, }  
{#16, 已修, }  
{#17, 已修, }  
{#18, 已修, }  
{#19, 已修, }  
{#20, 已修, }  
{#21, 已修, }  
{#22, 已修, }  
{#23, 已修, }  
{#24, 已修, }  
{#25, 已修, }  
{#26, 已修, }  
{#27, 已修, }  
{#28, 已修, }  
{#29, 已修, }  
{#30, 已修, }  
{#31, 未修, A「版本鎖定行」仍未寫明唯一正規形，以及禁 BOM、重複鍵與 TOML 表旁路。}  
{#32, 已修, }  
{#33, 已修, }  
{#34, 已修, }  
{#35, 已修, }  
{#36, 已修, }  
{#37, 已修, }  
{#38, 已修, }  
{#39, 已修, }  
{#40, 已修, }  
{#41, 已修, }  
{#42, 已修, }  
{#43, 已修, }  
{#44, 已修, }  
{#45, 已修, }  
{#46, 已修, }  
{#47, 已修, }  
{#48, 已修, }  
{#49, 已修, }  
{#50, 已修, }  
{#51, 已修, }  
{#52, 改壞, C 通則斷言所有 `--dry-run`「仍會拉 image 展開」，但 uninstall、remove、prune 不需要也不應因此拉 image；應改成「需要新版內容的動詞仍會拉 image 展開」。}  
{#53, 已修, }  
{#54, 已修, }  
{#55, 未修, 快路徑仍未檢查各工具 `cache/<repo>/` 是否存在且完整；印記存在但 cache 被刪時仍可能誤判為無事可做。}  
{#56, 已修, }

第二段「新發現」

{00, 「一句話目的／下游 image」與 01 下游開發者角色, 矛盾, 01 開頭說下游 image「公開」，角色表卻說「公開與否自決」；須統一是否公開為契約前提。, 必修}

{00, 「可寫動詞」, 定義不清, 定義只涵蓋「寫進 git」或「恢復進度檔」，但 prune 不寫進 git，且依 D 明定不恢復活躍交易；應改以「會建立進度檔或恢復交易」等可涵蓋完整集合的條件定義。, 必修}

{00, 「prune」, 矛盾, 寫成刪除「版本鎖定行未引用的舊 image」，漏掉本機覆寫實際引用的引擎 image 也必須保留，與 C prune 及 D §1.2 衝突。, 必修}

{00, 「install」, 遺漏, 動詞摘要只交代根 justfile，漏掉 install 也會建立或詢問追加根 `.dockerignore` 四行。, 必修}

{00, 「uninstall」, 遺漏, 動詞摘要只說移除根 justfile 那一行，漏掉經詢問逐行移除仍與原文相同的 `.dockerignore` 四行。, 必修}

{00, 「動詞表用到的選項」, 遺漏, 清單漏定義 C 使用的 `-t`／`--tool`、`--source`、`--local`、`--verify`、`--no-justfile`，與「動詞表用到的選項」的自我宣告不符。, 必修}

{01, I11 與「進度檔與 `.tmp.*`」例外, 矛盾, I11 說所有可寫動詞開始前一律先恢復未完成交易，但 D 明定 prune 遇活躍交易不恢復、不阻擋，B 的例外只說不刪，未解除「先恢復」要求。, 必修}

{01, I4「多工具動詞做得完的做完」, 定義不清, uninstall 在 apply 期間任一工具失敗會中止並留下未處理工具，並非繼續把其餘「做得完的做完」；應限定為各動詞既定的失敗策略或直接引用逐動詞規則。, 必修}

{01, I15「VK 寫的每個 TOML」, 定義不清, 「寫時保留未知欄位」未說明刪除整個檔案或整個工具項目時是否仍適用，容易與 uninstall/remove 的合法刪除行為衝突；宜限定為重寫仍存在的 TOML 文件。, 選修}

{02, 通則 3 與 prune 列, 矛盾, 通則要求可寫動詞先恢復未完成交易，prune 列卻依 D 說活躍進度檔只提示、不擋、不恢復；須在通則 3 明列 prune 例外。, 必修}

{02, 「寫哪類檔」的「（皆刪）」及 uninstall/remove 列, 矛盾, 兩列把進度檔也標為「只刪不建」，但兩動詞都必須先建立自己的進度檔，成功後才刪除。, 必修}

{02, install「寫哪類檔」, 遺漏, 一句話明列建立空 `baseline/`，D 的檔案矩陣也列為建立，但寫檔欄漏列基準版類別。, 必修}

{02, bootstrap.sh「任一非 0…整體 1」, 矛盾, 此句會把 install 的介面版／檔案版不合碼 3 也壓成 1，卻又在同列結束碼列出 3；應只把 `-t` 的 add 非 0 定義為整體 1，或明列 3 的傳遞規則。, 必修}

{02, `upgrade vendor_kit`「薄殼被改」, 定義不清, 同一句把「薄殼被改 → 1 列差異不動」放在已改引擎鎖定行並恢復交易的敘述之後，未清楚區分首次執行的前置拒絕與既有升引擎交易的恢復順序。, 選修}

{02, 本頁名詞「指紋重驗」及表內「apply」, 前引違規, 本頁定義「兩段式動詞」但未定義 resolve／apply 兩階段的契約名稱；`apply` 也不在第 0、1 頁字典，卻在 uninstall 的失敗說明與出處語境中使用。, 必修}

{02, `sync` 快路徑與通則 1, 定義不清, 快路徑宣稱「0 不起容器」，但仍必須先建立執行紀錄；應直接寫成「寫完執行紀錄後不起引擎容器」，避免被讀成完全零副作用。, 選修}

總評：三頁目前仍不能交給使用者定稿；至少須修正 #31、#52、#55，以及上述公開性、prune 交易例外、`（皆刪）`、bootstrap 結束碼等必修矛盾。
