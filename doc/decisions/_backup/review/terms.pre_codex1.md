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
