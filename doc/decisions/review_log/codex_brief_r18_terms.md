# r18：改寫審閱頁 01「名詞與縮寫」（`doc/decisions/review/terms.md`）＋同步產生器 v1p0 區塊

你在目錄 `/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/` 工作（這是 repo 的複本，路徑結構相同；下面所有相對路徑都相對於這個目錄，不要碰這個目錄以外的任何東西）。你是執行者：直接改檔（不是只給意見）。**只能動這三個檔**（其他頁、其他檔一律不碰）：
1. `doc/decisions/review/terms.md`（改前先 `cp` 到 `doc/decisions/_backup/review/terms.pre_r18.md`）
2. `doc/decisions/review/terms_moved.md`（新建；標題「# 01 頁移出待歸位」）
3. `script/diagram/disc_v1_a.py` 的 v1p0 區塊（改前先 `cp` 到 `script/diagram/_backup/disc_v1_a.py.pre_r18`；區塊 = `# ================= P0 v1p0` 到 `pages_v1_a.append(("v1p0", "名詞與縮寫", p0))` 那行為止；區塊外一個位元組都不能改）

不 commit、不 push、不跑 git add。做完後在最後輸出：改了什麼、terms.md 前後條數、terms_moved.md 條數、有沒有偏離 brief 的地方。

## 判準（每條都要照）

- 本頁是所有審閱頁的共同字典，只定義「使用者在對外契約會遇到的 VK 詞」；一條只講「是什麼」。
- 規則、指令語法、內部實作、圖面約定不留。通用技術詞（git、docker、TOML、just、容器、registry 這類）不定義；但 registry 因後頁反覆指涉要留一句。
- 定義超過一句就用條列：表格內用 `<br>• ` 換行（第一行不加 `•`，之後每點 `<br>• `）。
- 例子一律 `<repo>`。
- **已定案不可改一字**：「兩方與承諾關係」一段（開頭段落、使用者／VK 兩列表、表後句「只打 `just <ns> …` 的人不是『方』……不縮寫。」）。
- 全檔不得出現「下游使用者」「下游開發者」「三方」「／」（全形斜線）；二選一用 `|`（表格內寫 `\|`），路徑用 `/`。
- 從 01 頁移出的內容**不要**加進其他頁，一律寫進 `terms_moved.md`：每條格式「- 原文（可整段引用）→ 去向頁」；去向頁用編號（02 不變量、04 動詞介面表、05 規則、07 schema、10 契約④、14 架構圖、57 狀態機、59 結束碼、主圖第 0 頁）。末尾一節「## 附錄原文」放原附錄整段。

## 逐段要求

### 0. 開頭段
保留原文第一段（「本頁是所有審閱頁的共同字典……不貼切的寫一句理由。」）。

### 1. 「兩方與承諾關係」
原文不動。接著把「兩種 repo 要分清楚：」改成標題 `## 兩個 repo`，表改四欄：`repo｜誰的｜使用者在裡面做什麼｜VK 對它的承諾`，兩列：

| repo | 誰的 | 使用者在裡面做什麼 | VK 對它的承諾 |
|---|---|---|---|
| **專案** | 使用者的 git repo（或 monorepo 的子專案） | 跑 `bootstrap.sh` 接入、跑 VK 動詞、commit 薄殼與版本鎖定行 | 不刪、不覆蓋專案檔；鎖得住、升得了；失敗必印原因 |
| **下游 repo** | 使用者的 git repo，提供一個工具 | 維護 `dist/`、打成下游 image 推到 registry、用 dev、undev 在本機開發 | 照 `dist/` 契約出貨就搬得到；`<repo>` 是它的名字 |

表後一句：「同一個使用者在兩個 repo 裡做不同的事；VK 的承諾分別落在兩邊。」

### 2. 「VK 組件（component）」
刪「VK 由三個組件組成……組件 > 模組」句與整張「VK 模組」表（原文 → terms_moved.md，去向 14 架構圖）。三條各一句：
- **引擎**：執行 VK 動詞的主程式，以容器 image 發布。
- **薄殼**：`.vendor_kit/` 內由引擎產生、隨專案進 git、供使用者呼叫 VK 的一組檔。
- **啟動器**：薄殼內從主機起引擎的 POSIX sh 片段；`bootstrap.sh` 是第一次接入用的啟動器。

### 3. 「常用詞」：常用詞 + 其他既有詞合成**一張表**（標題 `## 常用詞`，三欄 中文名｜英文｜定義），順序固定如下（分組只是順序，不加子標題）：
1. repo 與工具：工具、`<ns>` 命名空間、工具 recipe、專案根、`dist/`
2. image 與版本：下游 image、引擎 image、registry、image 引用、tag、digest、image ID、正式版
3. 檔案分類：專案檔、VK 檔、進 git 的檔、`cache/`、`gen/`（各一條）、印記、自描述標頭、執行紀錄、進度檔
4. 版本鎖定：版本鎖定行（英文 lock version line）、本機覆寫
5. 初始檔：初始檔、納管、metadata、基準版、基準版合併（英文 baseline merge）、合併衝突
6. 執行模式與結果：CI 模式、詢問、`-y`、可寫動詞、唯讀動詞、需人處理、失敗、警告
7. 版號：介面版（英文 interface version）、檔案版（schema version）、最低介面版、結束碼

每條規定：
- 縮成「是什麼」；規則細節（正規形、禁項、順序、結束碼對照、prune 例外、判別順序、路徑格式、欄位格式）全移 terms_moved.md 並標去向頁（版本鎖定行正規形／metadata 欄位／印記格式／自描述標頭格式／檔案版 → 07 schema；正式版預設規則／CI 判定／tty／`-y` 語意 → 05 規則；結束碼對照 → 59；進度檔恢復與 prune 例外 → 57 狀態機；執行紀錄順序、resolve/apply 兩段式、救援路徑 → 10 契約④；專案檔四原則、預檢 → 02 不變量；佔位符 → 主圖第 0 頁，`<repo>` 名稱規則 → 07）。
- 可寫動詞／唯讀動詞名稱保留；定義寫明「指會不會動進 git 的檔與進度檔；唯讀動詞仍可寫 `cache/`、`gen/`」（動詞清單留在定義裡可以，但不要寫進度檔落點）。
- 三方合併 → 改名「基準版合併」｜baseline merge：以基準版為共同祖先、拿使用者現況與新版做的合併（做法是 git 的 three-way merge）。
- 刪：symlink、tty、hash、專案檔四原則（→ 02）、預檢（→ 05）、resolve／apply 兩段式（→ 10）、救援路徑（→ 10）、佔位符（→ 主圖第 0 頁；`<repo>` 名稱規則 → 07）。刪掉的每條原文都要進 terms_moved.md。
- 需人處理／失敗只留「是什麼」，顏色與結束碼移走（→ 主圖第 0 頁／59）。
- 新增條目：工具（下游 repo 出貨、專案接入的內容單位，名字 `<repo>`）、引擎 image、registry、image 引用（`<image>:<tag>@sha256:<digest>`）、tag、digest、合併衝突、詢問、警告。

### 4. 「語法記法」整段與選項清單：**刪除**
記法表改寫成 POSIX 版放 terms_moved.md → 主圖第 0 頁，列：`<x>` 佔位符、`[x]` 可省略、`x...` 可重複、`a|b` 二選一、`[a|b]` 可省略的二選一、`(a|b)` 必選其一、`<repo>[@<tag>]` 可省略的版本後綴、`-x <值>`／`--long <值>` 短長等價；附出處（附檔 agy_out_syntax.md 查到的來源：POSIX.1-2017 XBD §12.1、man-pages(7)、docopt、GNU Coding Standards；只列來源名與 URL）。選項清單原文 → 04（語意 → 05）。

### 5. 「動詞」表
保留「寫法：小寫原文，前面省略 `just vendor_kit`。」表兩欄 動詞｜做什麼，動詞欄只寫名稱（`install`、`uninstall`、`add`、`remove`、`update`、`upgrade`、`dev`、`undev`、`sync`、`prune`、`help`），每個動詞一句「做什麼」，不寫語法、不寫寫檔細節（原文細節 → terms_moved.md → 04／流程頁 15+）。表後一句：「**升引擎**：以 `upgrade vendor_kit` 更換引擎版本。」

### 6. 刪「記法與顏色見主圖第 0 頁……」與整個「附錄」（附錄內容 → terms_moved.md 末尾「## 附錄原文」）。

## 產生器 v1p0 區塊
照新 terms.md **逐字**排版（圖上文字 = md 文字去反引號、去 `**`；之後會用腳本雙向逐字比對，差一個字都算錯）。結構：頁標題 `rtitle("p0", "名詞與縮寫")` → 開頭段 → `sec` 兩方與承諾關係 → 兩方表（原樣不動）→ 表後句（不動）→ `sec` 兩個 repo → 四欄表 `mtbl`（欄寬自訂，總寬 1580）→ 表後句 → `sec` VK 組件（component）→ 三條各一格（照現在的 COMP 三欄排法）→ `sec` 常用詞 → 單表 `mtbl` → `sec` 動詞 → 「寫法：…」段 → 動詞表 → 升引擎句。頁名維持 `pages_v1_a.append(("v1p0", "名詞與縮寫", p0))`。

技術細節：
- 表格格文字經 `M()`；`M()` 要能處理 md 的 `<br>• ` 與 `\|`：把 `M` 改成 `s = s.replace("`", "").replace("<br>", "\n").replace("\\|", "|")` 後再做粗體替換（`v()` 會把 `\n` 變成圖上的 `<br>`）。`M` 定義在區塊外一點（約 442 行）——**這是唯一允許改的區塊外程式碼**，且只能加這兩個 replace。
- 多句定義的格：md 是 `第一句<br>• 第二點<br>• 第三點`，圖上就是三行。
- 不要新增 helper；用現有 `para`、`sec`、`mtbl`、`vb`、`hvl`、`rlh`、`LT12`、`RX`、`RW`、`RLH`。
- 刪掉的節（模組表、其他既有詞、語法記法、選項清單、p0_v2 句）在產生器裡也要刪，不要留註解掉的程式碼。
- 改完跑 `python3 /tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/script/diagram/gen_disc.py` 確認不報錯（它會寫 `/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/discussion.drawio`，這是預期的）。

---
# 附檔 1：目前的 `doc/decisions/review/terms.md` 全文
# 名詞與縮寫

本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。

## 兩方與承諾關係

| 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
|---|---|---|---|
| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |

只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。

兩種 repo 要分清楚：

| 中文名 | 英文 | 定義 |
|---|---|---|
| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |

## VK 組件（component）

VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。

- **引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。
- **薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。
- **啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。

### VK 模組（module）——引擎內的 8 個程式單元

| 中文名 | 英文代號 | 做什麼 |
|---|---|---|
| 版本解析 | `resolve` | 讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔 |
| 取件 | `fetch` | 把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記 |
| 初始檔合併 | `initfile` | 依工具宣告建初始檔、存基準版、升版時做三方合併 |
| 薄殼產生 | `shell` | 產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改 |
| 進度與寫入 | `progress` | 建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續 |
| 設定與格式 | `schema` | 讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml` |
| 紀錄 | `log` | 每次執行寫一份執行紀錄 |
| 清理 | `prune` | 找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除 |

## 常用詞

| 中文名 | 英文 | 定義 |
|---|---|---|
| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
| **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
| **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
| **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
| **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
| **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
| **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
| **進度檔** | progress file | 可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用） |
| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事 |
| **CI 模式** | CI mode | 環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查） |
| **需人處理** | needs human | 動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色 |
| **失敗** | failure | 拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色 |
| **專案檔四原則** | four rules | ① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容） |
| **預檢** | precheck | 動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動 |
| **resolve／apply（兩段式）** | two-phase | 兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器 |
| **介面版** | protocol version | 薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關 |
| **檔案版** | schema version | VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔 |
| **最低介面版** | floor | 引擎仍支援的最低介面版；固定常數；只能經 ADR 提高 |
| **結束碼** | exit code | `0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入 |
| **本機覆寫** | local override | `version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行 |
| **symlink** | symlink | 符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄 |
| **hash** | hash | 檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗 |
| **image ID** | image ID | docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同 |
| **tty** | tty | 互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束 |
| **佔位符** | placeholder | `<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id |

### 其他既有詞

| 中文名 | 英文 | 定義 |
|---|---|---|
| **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
| **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
| **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
| **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
| **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
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

動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）：

- `-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。
- `-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。
- `-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。
- `-y`／`--yes`：省略詢問，視同回答「是」。
- `--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。
- `--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。
- `--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。
- `--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。
- `--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。
- `--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。
- `--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。
- `--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。

## 動詞

寫法：小寫原文，前面省略 `just vendor_kit`。

| 動詞 | 做什麼 |
|---|---|
| `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
| `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
| `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
| `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
| `upgrade [<repo>[@<tag>]]` | 升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行 |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔 |
| `undev <repo>`／`undev vendor_kit` | 撤銷 dev，回到版本鎖定行的版本 |
| `sync [<repo>]` | 依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發 |
| `prune` | 刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋 |
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

來源：`decisions/review/codex_findings_00_02.md`（00 頁 #1–#16、用詞 #34／#54）、`decisions/review/codex_findings_00_02_r2.md`（#31、#52、N1–N6、N15；進度檔的 prune 例外 = N7）、`decisions/review/codex_findings_00_02_r3.md`（R1 正規形寫全於本頁、R2／R3 `<repo>` 名稱規則與 `[tools]` 表、R5 工具 recipe、R6 `--local` 判別順序、R9 執行紀錄含 bootstrap.sh）、`decisions/review/codex_findings_00_02_r4.md`（S2 自描述標頭、S3 本機覆寫含引擎 tag ＋ image ID、S5 初始檔 copy 型／append 型、S6 `gen/tools.just`）、`decisions/review/codex_findings_00_02_r5.md`（T1 結束碼 2 含解析不過）、`decisions/grilling.md`「02 頁 6 點定案」「兩條新規則」「補三條不變量」「專案定名」「00–02 codex 三審新定案」（2026-09-20）、`decisions/interface_spec.md` v3.5 §0、§1.1、§1.2、§4.1–§4.6。


---
# 附檔 2：你上一輪（r17）對本頁的判斷 `doc/decisions/review_log/codex_out_r17_terms.md`（參考用；本 brief 的指示優先）
# 總判斷

目前這頁混了五種不同東西：共同詞彙、對外介面、行為規則、內部架構、圖面記法。字典應只留下後頁會反覆使用、而且使用者在對外契約中確實會遇到的名詞；定義只回答「它是什麼」。

另外，題目所列數量與正文不一致：

- 「常用詞」實際是 **29 條**，不是 30 條。
- 「其他既有詞」實際是 **9 條**，不是 10 條。

## A.「兩種 repo 要分清楚」

| 條目 | 判斷 | 理由 |
|---|---|---|
| 專案 | **改寫後留在字典** | 是整套契約的基本作用域，但現文混入「接入後有哪些檔」及「動詞在哪裡跑」等規則。 |
| 下游 repo | **改寫後留在字典** | 是工具來源與出貨端的核心名詞，但打 image、registry 可見性及私有憑證屬 12–13 CI 契約或 15+ 出貨流程。 |

建議定義：

- **專案**：使用者接入 VK、安裝並使用工具的 git repo；在 monorepo 中也可以是一個獨立接入 VK 的子專案。
- **下游 repo**：維護並出貨一個工具的 git repo；字典與指令範例以 `<repo>` 表示其名稱。

「兩種 repo 要分清楚」可改成中性的「repo 種類」。目前標題帶有審閱提示語氣，不像定義。

## B.「VK 組件」三條

開頭的「組件 > 模組」是分類／架構約定，移到第 14 頁；字典不需要先定義一個只為容納內部模組而存在的階層。

| 條目 | 判斷 | 理由 |
|---|---|---|
| 引擎 | **改寫後留在字典** | 使用者會拉取、鎖定、升級或以本機 image 覆寫引擎，是對外可見實體；「所有判斷與寫檔都在裡面」是架構規則。 |
| 薄殼 | **改寫後留在字典** | 使用者會 commit、檢查及修復薄殼，是下游 repo 契約的一部分；五檔清單與標頭規則應分到 06、09、10–11。 |
| 啟動器 | **改寫後留在字典** | 是使用者實際執行或由薄殼呼叫的對外邊界；拉 image、展開、起容器的步驟屬 10–11。 |

建議定義：

- **引擎**：以容器 image 發布、執行 VK 動詞的 VK 主程式。
- **薄殼**：存放於專案 `.vendor_kit/`、隨專案進 git、供使用者呼叫 VK 的一組檔案。
- **啟動器**：負責從主機端啟動 VK 引擎的 POSIX sh 程式；`bootstrap.sh` 是首次接入使用的啟動器。

「人不改」「五檔」「掛 `/repo`」「標頭與 hash 契約」都不要留在這三條定義內。

## C.「VK 模組」八條

整節 **移到第 14 頁「架構圖」**。這八個名稱都是引擎內部程式單元，不是使用者對外契約中的詞。

| 模組 | 判斷 | 理由 |
|---|---|---|
| `resolve` | **移到 14** | 內部責任分割；不要與對外流程階段 `resolve` 混成字典詞。 |
| `fetch` | **移到 14** | 內部取件實作。 |
| `initfile` | **移到 14** | 內部模組名；對外只需要「初始檔」「三方合併」。 |
| `shell` | **移到 14** | 內部產生器，不是「薄殼」的同義詞。 |
| `progress` | **移到 14** | 內部交易／寫入模組。 |
| `schema` | **移到 14** | 內部 TOML 處理模組；容易與對外「檔案版」的 `schema` 欄位混淆。 |
| `log` | **移到 14** | 內部紀錄模組。 |
| `prune` | **移到 14** | 此處是模組；對外 `prune` 動詞另留。 |

如果第 14 頁沒有呈現實作模組的需求，整節可以直接刪掉；不應為了保留八個內部名稱而污染共同字典。

## D.「常用詞」逐條判斷

### D1–D9：檔案、版本與合併

| 條目 | 判斷 | 理由 |
|---|---|---|
| 專案檔 | **改寫後留** | 是 09 契約與各動詞流程反覆使用的檔案所有權分類；四原則不要塞進定義。 |
| VK 檔 | **改寫後留** | 是對外可見的另一個檔案所有權分類；完整清單與 git 狀態移到 06、08、09。 |
| 進 git 的檔 | **改寫後留** | 後頁會以此描述是否允許修改，屬使用者可觀察的契約分類；逐檔清單移到 08。英文建議用 `tracked file`，中文可改為較自然的「追蹤檔」。 |
| 版本鎖定行 | **改寫後留** | 是使用者會 commit、審查、解衝突的核心契約物；正規形、空白、BOM、旁路語法、錯誤處理全部移到 07。 |
| 正式版 | **留，略改寫** | 是版本選擇語意中的必要詞；「省略 tag 就取最新正式版」是規則，移到 05。 |
| 初始檔 | **改寫後留** | 是工具安裝後交給使用者維護的核心產物；copy／append 的行為細節移到 07 或 09。兩種類型若後頁反覆使用，可另立「copy 型初始檔」「append 型初始檔」。 |
| 基準版 | **改寫後留** | 使用者解三方合併及理解進 git 內容時會遇到；精確路徑移到 06。 |
| 三方合併 | **改寫後留** | 是升級契約的核心概念；衝突標記與失敗處理移到 15+、56–57、59。 |
| metadata | **改寫後留** | 是進 git、可在衝突或審查中被看見的契約檔；欄位與進度格式移到 07。建議給中文主名「初始檔 metadata」，避免裸英文過泛。 |

建議縮短：

- **專案檔**：位於專案內、由使用者擁有及維護的檔案。
- **VK 檔**：由 VK 建立及管理、位於 `.vendor_kit/` 的檔案。
- **追蹤檔**：預期由 git 追蹤並隨專案 commit 的檔案。
- **版本鎖定行**：在 `version.toml` 中把引擎或工具名稱對應到確切 image 版本的 TOML 項目。
- **正式版**：不是預發行版本的發布版本。
- **初始檔**：由工具提供、VK 接入專案後交由使用者維護的專案檔。
- **基準版**：VK 保存的上次已套用初始檔內容，用作下一次三方合併的共同祖先。
- **三方合併**：以共同祖先、使用者現況及新版內容三份輸入產生合併結果的作業。
- **初始檔 metadata**：記錄初始檔來源及 VK 管理狀態的 VK 檔。

### D10–D19：動詞分類、狀態與流程

| 條目 | 判斷 | 理由 |
|---|---|---|
| 可寫動詞 | **改寫後留** | 若 02–03、56–57 會以此作共同分類，就需要字典定義；動詞清單移到 04。名稱最好改成「交易動詞」，因 `sync` 也會寫非追蹤檔，「可寫／唯讀」容易誤導。 |
| 唯讀動詞 | **改寫後留** | 同上；現定義其實不是字面上的唯讀，因 `sync` 會寫檔，建議改名「非交易動詞」。 |
| 進度檔 | **改寫後留** | 使用者中斷、重跑及排障時會遇到；恢復規則、prune 例外與兩種落點移到 56–57，格式移到 07。 |
| 執行紀錄 | **改寫後留** | 是使用者可查閱的對外診斷產物；建立時序與失敗原子性移到 02–03 或 09，路徑移到 06。 |
| CI 模式 | **改寫後留** | 是使用者明確啟用／遭 CI 環境啟用的對外模式；真假判定及限制移到 05、12–13。 |
| 需人處理 | **改寫後留** | 可作所有流程圖共用的結果類別；結束碼移到 59，橙色移到第 0 頁。名稱可改成「待使用者處理」以對齊兩方模型。 |
| 失敗 | **改寫後留** | 可作共同結果類別；原因分類及結束碼移到 59，紅色移到第 0 頁。 |
| 專案檔四原則 | **移到 09** | 整條是規則，不是「是什麼」的定義；若後頁需要簡稱，可在字典只留「專案檔」而直接引用第 09 頁的四項契約。 |
| 預檢 | **改寫後移到 02–03** | 是跨動詞不變量／流程階段，不是使用者需要先學的對象；各動詞的具體預檢放 15+。若圖中大量使用，字典最多留一句「動詞改變狀態前的檢查階段」。 |
| resolve／apply（兩段式） | **移到 10–11 與 14** | 是啟動器↔引擎的執行協定及架構；哪些動詞單段／兩段、容器數量、拉 image 時機都是規則。不要與內部 `resolve` 模組共用一條字典定義。 |

「唯讀動詞」尤其應處理。既然 `sync` 寫 `cache/`、`gen/`，它不是一般工程語意上的 read-only。推薦分類：

- **交易動詞**：會以進度狀態保護其中斷與恢復的 VK 動詞。
- **非交易動詞**：不建立或恢復進度狀態的 VK 動詞。

這兩個名稱描述真正差異，不會暗示完全不寫檔。

### D20–D29：相容性、結果與執行環境

| 條目 | 判斷 | 理由 |
|---|---|---|
| 介面版 | **改寫後留** | 使用者可能從薄殼標頭、錯誤及相容性表看到，是公開契約版本。薄殼如何傳遞移到 10–11。英文建議 `interface version`，不要寫 `protocol version` 造成雙名。 |
| 檔案版 | **改寫後留** | 使用者會在 TOML 與相容性錯誤看到；可讀範圍與錯誤處理移到 07、58。英文用 `schema version` 可保留。 |
| 最低介面版 | **改寫後留** | 是 58 相容性矩陣的重要軸；「固定常數、只能 ADR 提高」移到 58 或工程治理文件。 |
| 結束碼 | **改寫後留** | 是 CLI 對外詞，字典只定義它是程序回報結果的整數；完整 `0–3` 對照移到 59。 |
| 本機覆寫 | **改寫後留** | 使用者執行 dev、排障或檢視未追蹤狀態時會遇到；格式、優先級、image ID 驗證移到 05、07、15+。 |
| symlink | **刪** | 通用作業系統詞，而且只是 dev 的實作手段；若 dev 契約保證它必須是 symlink，再在 dev 流程頁就地說明。中文應寫「符號連結」，不必列為共同領域詞。 |
| hash | **改寫後留** | 薄殼標頭、印記及重驗都會出現；只定義為內容雜湊值。演算法與用途移到 07、10–11。中文主名建議「內容雜湊」。 |
| image ID | **改寫後留** | 使用者會在本機引擎覆寫與錯誤訊息看到，且必須和 registry digest 區分。驗證規則移到 10–11、15+。 |
| tty | **刪或移到 05** | 是通用執行環境概念，不是 VK 領域詞；「何時可詢問、沒 tty 怎麼結束」明確屬選項與詢問規則。 |
| 佔位符 | **拆開並移到第 0 頁／05／07** | `<x>` 是圖文語法記法，名稱規則是 schema／驗證規則；整條不是對外名詞定義。`<repo>` 等各自代表什麼應放第 0 頁，`<repo>` 字元規則與保留名放 05 或 07。 |

其中 `hash` 若後頁一律改用更精確的「digest」「內容雜湊」，可取消 `hash` 這個泛稱，避免 registry digest、image ID、檔案 sha256 三者混淆。

## E.「其他既有詞」逐條判斷

| 條目 | 判斷 | 理由 |
|---|---|---|
| 下游 image | **改寫後留** | 是 add、upgrade、出貨及 registry 契約的核心對象；`FROM scratch`、多架構要求移到 12–13 或下游出貨契約。 |
| `dist/` | **改寫後留** | 是下游 repo 與 VK 交接的公開目錄；內容樹移到 06，哪些內容出貨是 09 或 12–13 的規則。 |
| 工具 recipe | **改寫後留** | 使用者會直接執行，且必須與 VK 動詞區分；自動 `sync` 規則移到 04、09 或 10–11。 |
| 專案根 | **改寫後留** | 所有路徑都需要共同基準；「不是 git toplevel」及 monorepo 規則移到 05 或 09。 |
| `cache/`、`gen/` | **拆成兩條，改寫後留** | 兩個目錄生命週期與用途不同，不應共用一個字典條目；完整樹與 `tools.just` 格式移到 06、08。 |
| 印記 | **改寫後留** | 使用者在排障及檔案矩陣會看到；內容格式與信任規則移到 07、08。建議名稱改成「工具印記」，避免過泛。 |
| 納管 | **改寫後留** | 是初始檔狀態機的公開狀態；「拒絕過」應另有正式狀態名稱，不要塞在納管定義裡。 |
| 自描述標頭 | **改寫後留** | 使用者會在薄殼檔及被修改錯誤中看到；精確格式、所在行及不符處理移到 07、10–11。 |
| 救援路徑 | **移到 10–11** | 是啟動器協定／恢復架構，不是使用者管理的對象；「永久可用」更是契約規則。若後頁流程反覆把它當正式模式，可留一條極短定義。 |

建議定義：

- **下游 image**：裝載一個工具之出貨內容、供 VK 取得該內容的容器 image。
- **`dist/`**：下游 repo 中交付給 VK 的工具出貨目錄。
- **工具 recipe**：由工具提供、以其 just 命名空間供人執行的 recipe。
- **專案根**：一套 VK 接入所屬專案的根目錄。
- **工具快取**（`cache/`）：VK 在專案本機保存已展開工具內容的目錄。
- **生成檔目錄**（`gen/`）：VK 在專案本機保存生成檔的目錄。
- **工具印記**：描述本機工具快取所對應版本及內容的 VK 檔。
- **納管**：VK 已為某個初始檔記錄來源，並在後續升級中處理它的狀態。
- **自描述標頭**：薄殼檔內描述其介面版、引擎版及內容雜湊的標頭。

## F.「語法記法」表與選項清單

### 語法記法表

**整表移到主圖第 0 頁「圖例與記法」**。

理由：`<x>`、`[x]`、`a／b` 是文件元語法，不是使用者在契約中遇到的領域詞。`-x`／`--long` 也只是 CLI 表示法。

需要修正兩點：

1. `<repo>` 例子規則應統一由第 0 頁宣告，所有頁都只用 `<repo>`。
2. `[@<tag>]` 可在第 0 頁只解釋括號語法；「省略時選最新正式版」移到第 05 頁。

### 選項清單

**選項名稱與適用動詞移到第 04 頁；選項語意與限制移到第 05 頁。**

| 選項 | 主要去向 | 理由 |
|---|---|---|
| `-t`／`--tool` | **04；預設規則到 05** | 是 `bootstrap.sh` 介面；可重複、tag 預設是規則。 |
| `-p`／`--path` | **04** | 是 dev 指令介面。 |
| `-i`／`--image` | **04；只收 tag 到 05** | 是 dev 指令介面及輸入限制。 |
| `-y`／`--yes` | **04；詢問語意到 05** | 選項存在屬介面；如何代答屬共通規則。 |
| `--exit-code` | **04；回 2 的條件到 05／59** | 選項屬介面，碼義屬結束碼決策。 |
| `--dry-run` | **04；寫入／拉取規則到 05** | 現文幾乎整段是行為規則。 |
| `--source` | **04；命名慣例到 05** | 是 add 介面。 |
| `--local` | **04；判別順序到 05** | 參數形式屬介面，消歧演算法與失敗條件屬規則。 |
| `--verify` | **04；CI 隱含行為到 05、12–13** | 是 sync 介面。 |
| `--no-justfile` | **04；跳過後的行為到 05／install 流程** | 是 install 介面。 |
| `--help`／`-h` | **04** | 是所有動詞共有的介面。 |
| `--timeout` | **04；適用拉取及計時規則到 05** | 是共通選項。 |

字典不應保留任何完整 CLI 語法。

## G.「動詞」表與「升引擎」

動詞名稱是後面所有頁的共同語言，因此**應留在字典，但全部改成一句純語義定義**。語法、選項、詢問、檔案細節、結束碼及恢復規則移走。

| 動詞 | 判斷 | 字典應保留的定義 | 其餘內容去向 |
|---|---|---|---|
| install | **改寫後留** | 將 VK 接入專案，或修復既有接入。 | 語法到 04；檔案與詢問規則到 05、06、09；流程到 15+。 |
| uninstall | **改寫後留** | 從專案移除 VK 的接入。 | 保留／刪除清單及相同原文判定到 05、09、15+。 |
| add | **改寫後留** | 將一個工具接入專案。 | 語法到 04；具體寫入與順序到 15+。 |
| remove | **改寫後留** | 從專案解除一個工具的接入。 | 不刪初始檔等規則到 09、15+。 |
| update | **改寫後留** | 查詢已接入的引擎或工具是否有可用新版。 | `--exit-code` 與只寫紀錄到 04、05、59。 |
| upgrade | **改寫後留** | 將已接入的引擎或工具改為另一個版本。 | 最新版選擇、三方合併及寫入順序到 05、15+。 |
| dev | **改寫後留** | 暫時讓已接入的引擎或工具使用本機開發來源。 | 兩種語法到 04；symlink、image ID、進度規則到 07、15+。 |
| undev | **改寫後留** | 取消本機開發來源，恢復使用鎖定版本。 | 流程到 15+。 |
| sync | **改寫後留** | 使專案本機的工具內容與目前選定的來源一致。 | 寫哪些目錄、自動觸發及驗證規則到 05、08、10–11、15+。 |
| prune | **改寫後留** | 清理由 VK 產生、但已不再被目前專案使用的本機資源。 | 資源種類、進度例外到 05、15+、56–57。 |
| help | **改寫後留** | 顯示 VK 指令的使用說明。 | 不觸網、紀錄行為到 05 或 help 流程。 |

### 「升引擎」

**改寫後留在字典**，前提是後頁確實把它當固定簡稱使用。

建議：

- **升引擎**：以 `upgrade` 更換 VK 引擎版本的操作。

下列內容移走：

- `upgrade vendor_kit[@<tag>]`：第 04 頁。
- 修改鎖定行、以新引擎重產薄殼：升引擎流程頁。
- 回 1 並要求重跑：第 59 頁及升引擎流程頁。

如果後頁可以一律寫「upgrade 引擎」，則「升引擎」可刪，避免同一動作有兩個正式名稱。

## H. 字典目前缺的詞

只從本頁已經暴露、而且後頁高度可能反覆使用的詞看，至少缺以下項目。

| 建議補詞 | 為什麼需要 |
|---|---|
| **工具** | 幾乎每一節都在使用，卻沒有定義它是由下游 repo 出貨、供專案接入的內容單位。 |
| **工具內容** | `dist/`、下游 image、`cache/`、sync 都使用這個概念，目前邊界不清。 |
| **引擎 image** | 已定義「下游 image」，卻沒有與之對稱的引擎 image；後面鎖定、拉取、升級、dev 都會使用。 |
| **image 引用** | `<image>:<tag>@sha256:<digest>` 是核心識別形式，需要一個總稱，否則每頁都得重述。 |
| **tag** | 正式版、指定版本、本機 image 都依賴它；目前只藏在「佔位符」。 |
| **digest** | 必須明確區別 registry digest、檔案內容雜湊及 image ID。 |
| **工具名** | `<repo>` 同時被當下游 repo 名、工具鍵與 cache 目錄名；應明定是否為同一識別碼。 |
| **just 命名空間** | `<ns>` 與工具 recipe 反覆使用，但目前只藏在佔位符條目。 |
| **鎖定版本** | `undev`、sync、升級與本機覆寫都會使用，應定義為版本鎖定行選定的版本。 |
| **有效來源** | 版本鎖定行與本機覆寫有優先關係；後面流程若反覆使用「目前來源」，應建立正式詞。 |
| **本機開發來源** | `dev` 後到底選到什麼，可作工具目錄或本機引擎 image 的共同上位詞。 |
| **合併衝突** | 三方合併、狀態機與結束碼表會反覆使用；應定義為不能自動決定合併內容的結果，不在字典寫碼。 |
| **詢問** | `-y`、tty、CI、專案檔修改都依賴同一概念；應定義為 VK 在改動前向使用者要求確認的互動。 |
| **警告** | 結束碼 0「含 warn」，但 `warn` 沒有正式名稱或定義。 |
| **活躍進度** | prune 與恢復流程使用，但沒有說什麼狀態算活躍。若只是狀態機判定，可只放 56–57，不必進共同字典。 |
| **拒絕過** | metadata 把它當正式狀態使用，卻沒有穩定名稱與定義；應在 56–57 決定正式狀態名。 |
| **容器資源** | prune 一再列 container／network／volume；若後頁合稱它們，應先定義上位詞。 |
| **registry** | 下游 image、正式版、digest、憑證與 update 都依賴它；若視為讀者已知的標準技術詞，可以不納入，但文件的「每頁只能用已定義詞」規則會迫使它進字典。 |

最重要的四個缺口是：**工具、引擎 image、image 引用、digest**。沒有它們，鎖定行、add、upgrade、dev 與相容性頁都很難精確書寫。

另有一個結構問題：目前「每頁只用本頁定義的詞」若連 Docker、TOML、git、registry、container、recipe 等通用技術名詞都算，字典會無限膨脹。建議把規則改成：

> 後頁使用的 VK 領域詞與文件專用簡稱，必須先在本頁定義；通用技術詞不受此限。

否則字典無法同時保持精簡與形式上的封閉。

## I. 建議最終字典內容與順序

以下是我建議第 01 頁最後留下的骨架。順序採「參與者 → 工作空間 → 出貨物 → VK 執行物 → 檔案所有權 → 版本與來源 → 初始檔 → 執行狀態 → 相容性 → 動詞」，讓每條定義只依賴前面已出現的詞。

### 1. 兩方

1. 使用者
2. VK

保留既有定案內容，不重審。

### 2. Repo 與工作單位

3. 專案  
4. 專案根  
5. 下游 repo  
6. 工具  
7. 工具名  
8. just 命名空間  
9. 工具 recipe  

### 3. 出貨物與 image

10. `dist/`  
11. 工具內容  
12. 下游 image  
13. 引擎 image  
14. image 引用  
15. tag  
16. digest  
17. 正式版  
18. image ID  

### 4. VK 的對外組件

19. 引擎  
20. 薄殼  
21. 啟動器  
22. 自描述標頭  

不保留「組件 > 模組」與八個內部模組。

### 5. 檔案分類與本機產物

23. 專案檔  
24. VK 檔  
25. 追蹤檔  
26. 工具快取（`cache/`）  
27. 生成檔目錄（`gen/`）  
28. 工具印記  
29. 執行紀錄  
30. 進度檔  

### 6. 版本選擇與開發來源

31. 版本鎖定行  
32. 鎖定版本  
33. 本機覆寫  
34. 本機開發來源  
35. 有效來源  

### 7. 初始檔與合併

36. 初始檔  
37. 納管  
38. 初始檔 metadata  
39. 基準版  
40. 三方合併  
41. 合併衝突  

### 8. 執行模式與結果

42. CI 模式  
43. 詢問  
44. 交易動詞  
45. 非交易動詞  
46. 待使用者處理  
47. 失敗  
48. 警告  

如果「交易／非交易動詞」沒有在多頁反覆使用，兩條都可刪，直接在 04、56–57 分類即可。

### 9. 相容性與驗證

49. 介面版  
50. 最低介面版  
51. 檔案版  
52. 內容雜湊  
53. 結束碼  

這裡只下定義；支援範圍在 58，碼表在 59。

### 10. VK 動詞

54. install  
55. uninstall  
56. add  
57. remove  
58. update  
59. upgrade  
60. dev  
61. undev  
62. sync  
63. prune  
64. help  
65. 升引擎——僅在它確實是跨頁固定簡稱時保留。

### 不應留在字典的內容

- 八個引擎內部模組
- 專案檔四原則
- 完整鎖定行正規形
- 進度恢復規則
- resolve／apply 容器流程
- 所有結束碼對照
- tty 詢問規則
- symlink 實作
- `<x>`、`[x]` 等語法記法
- 選項清單與參數消歧
- 動詞的完整指令語法
- 動詞逐步寫檔行為
- 顏色、形狀與跨頁節點記法
- 「升引擎後回 1 重跑」等流程決策

依這個切法，第 01 頁仍足以讓任何後頁自足地使用共同領域詞，但不再代替介面表、schema、契約、流程圖與結束碼決策表。

---
# 附檔 3：語法記法來源查證 `doc/decisions/review_log/agy_out_syntax.md`
本整理基於 **POSIX.1-2017 / The Open Group Base Specifications**、**Linux man-pages(7)**、**GNU Coding Standards**、**docopt 規範**以及主流 CLI 工具官方文件。

---

### 一、POSIX / Open Group「Utility Argument Syntax」（Chapter 12）

POSIX 標準在 IEEE Std 1003.1 / The Open Group Base Definitions 第 12 章（[12.1 Utility Argument Syntax](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) 與 [12.2 Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html#tag_12_02)）中正式規範了指令列參數的語法表示法（SYNOPSIS）：

1. **必填（Mandatory / Required）**：
   - 項目**不加中括號 `[ ]`** 即代表必填。
   - POSIX 12.1 第 8 點明訂：「當選項未被 `[` 與 `]` 包夾時，代表在該 SYNOPSIS 版本中該選項為必填（When an option is shown without the '[' and ']' brackets, it means that option is required for that version of the SYNOPSIS）。」
2. **可省略（Optional）**：
   - 使用**中括號 `[ ]`**（brackets）包夾。
   - POSIX 12.1 第 7 點：「被 `[` 與 `]` 包夾的參數或選項參數為可選（optional），可以被省略。符合標準的應用程式在實際輸入時不得包含 `[` 與 `]` 符號。」
3. **互斥二選一（Mutually Exclusive）**：
   - 使用**垂直線 `|`（vertical-line）** 分隔。
   - POSIX 12.1 第 8 點：「以 `|` 分隔的參數表示彼此互斥（mutually-exclusive）。此外，互斥的選項與運算元也可以透過列出**多行 SYNOPSIS** 來表示。」
   - 範例：`[-d|-e]` 或拆成多行展示彼此不相容的語法分支。
4. **可重複（Repeatable）**：
   - 使用**省略號 `...`（ellipses）**。
   - POSIX 12.1 第 9 點：「`...` 表示其前方的運算元允許出現一次或多次。若選項或運算元後面跟著 `...` 且整體被中括號 `[ ]` 包夾（如 `[-g arg]...` 或 `[operand...]`），則表示可以出現零次或多次；若未加括號（如 `utility -f arg [-f arg]...`），則代表至少必須出現一次。」
5. **佔位符（Placeholders / Parameters）**：
   - POSIX 12.1 第 4 點明訂：需要被實際數值替換的參數名稱，通常使用**內嵌底線**表示（例如 `option_argument`、`parameter_name`），在排版上通常使用*斜體（italics）*；另一種替代方式是使用**尖括號 `<>`**（例如 `<parameter name>`）。標準特別強調：尖括號僅是用於表示單一參數詞組的符號分組（symbolic grouping），實際輸入時不得打出 `<>`。

*來源：[The Open Group Base Specifications Issue 7 - Chapter 12 Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)*

---

### 二、GNU / man page（man-pages(7)、docopt、help2man）的慣例

在 Linux 與 GNU 開發生態中，SYNOPSIS 的慣例延續了 POSIX，並在終端機純文字展示、巨集格式化及解析器自動化上進行了細化：

1. **佔位符的呈現：`<x>` vs 斜體 vs 全大寫**：
   - **man-pages(7)**（roff/groff 格式）：依據 [man-pages(7) SYNOPSIS 段落規範](https://man7.org/linux/man-pages/man7/man-pages.7.html)，原樣輸入的指令與選項使用**粗體（boldface）**，可替換的參數/佔位符一律使用**斜體（italics）**（在 groff 原始碼中使用 `.I`、`.BI` 巨集；在終端機中可能渲染為底線或斜體）。
   - **GNU `--help` / help2man**：依據 [GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html) 與 [help2man 規範](https://www.gnu.org/software/help2man/)，在不具備富文本格式的終端機純文字輸出中，佔位符通常使用**全大寫字母（UPPERCASE）**表示，例如：
     `Usage: grep [OPTION]... PATTERNS [FILE]...`
     `help2man [OPTION]... executable`
   - **docopt 規範**：依據 [docopt.org 規格說明](http://docopt.org/)，位置參數（positional argument）允許兩種等價形式：以尖括號包夾的單詞（如 `<file>`、`<host>`）或是全大寫單詞（如 `FILE`、`HOST`）。
2. **`[x]`（可省略）**：
   - 在 man-pages(7) 與 docopt 中，中括號 `[ ]` 均表示 optional，與 POSIX 定義完全一致。
3. **必選其一：`{a|b}` vs `(a|b)`**：
   - **`docopt` 標準規範**：明確規定使用**圓括號 `( )`** 來表示必填群組（required elements）。當互斥元素必須二選一時，寫為 `(a | b)` 或 `(a|b)`。docopt 說明：「當互斥情況必須擇一時，使用圓括號 `( )` 進行分組（Use parens ( ) to group elements when one of the mutually exclusive cases is required）。」
   - **man page / EBNF 大括號流派 `{a|b}`**：在擴展巴科斯範式（EBNF）及許多 Unix/Linux man pages、RFC 和 Cisco/PowerShell 規範中，使用**大括號 `{ }`** 代表必選群組（mandatory group），因此 `{a|b}` 常用來代表「必須在 a 與 b 之中擇一」，與表示可選二選一的 `[a|b]` 形成直觀對比。
   - **POSIX 傳統做法**：POSIX 標準本身不傾向在行內增加 `{}` 或 `()`，而是傾向直接將互斥分支拆寫為多行 SYNOPSIS。
4. **可省略的其一：`[a|b]`**：
   - 由中括號與垂直線組合，表示「可從中選一個，或者都不選（zero or one）」。
5. **選項與參數等價語法（GNU getopt / getopt_long 規則）**：
   - **旗標（boolean flag，無參數）**：`--flag` 或 `-f`。
   - **短選項帶參數**：`-x VALUE` 與 `-xVALUE` 等價。
   - **長選項帶參數**：`--long=VALUE` 與 `--long VALUE` 等價。
     - *重要特例*：若參數為「可選參數（optional argument）」，依據 GNU `getopt_long(3)` 規則，長選項必須使用等號（`--long=VALUE`），短選項必須緊接（`-xVALUE`），不可留空格，否則解析器無法判斷下一個 token 是該選項的參數還是獨立的位置參數。
   - **說明清單中的簡寫**：在 `--help` 輸出中常以逗號並列，如 `-x, --long=VALUE`，表示兩者為長短選項對應關係。

*來源：[Linux man-pages: man-pages(7)](https://man7.org/linux/man-pages/man7/man-pages.7.html) | [docopt 語言標準](http://docopt.org/) | [GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html)*

---

### 三、主流工具 Usage 行實例剖析

#### 1. Git（以 `git-branch` 為例）
來源：[git-scm.com/docs/git-branch](https://git-scm.com/docs/git-branch)

**原文節錄**：
```text
git branch ( -m | -M ) [<old-branch>] <new-branch>
git branch ( -d | -D ) [ -r ] <branch-name>…​
git branch [ --track [ = ( direct | inherit )] | --no-track ] [ -f ] [ --recurse-submodules ] <branch-name> [<start-point>]
```

**解析**：
- **必選其一互斥**：採用圓括號配垂直線 `( -m | -M )` 與 `( -d | -D )`，代表重命名或刪除時必須明確指定其中一種強度旗標。
- **可選互斥**：`[ --track [ = ( direct | inherit )] | --no-track ]`，最外層以 `[ ... | ... ]` 表示追蹤模式互斥且可選。
- **可選內嵌參數與預設值選項**：`[ = ( direct | inherit )]` 展示了可選的 `=` 符號，等號後以 `( direct | inherit )` 規範了枚舉值的必選二選一。

#### 2. Docker（以 `docker image tag` 與 `docker run` 為例）
來源：[Docker Documentation: docker image tag](https://docs.docker.com/reference/cli/docker/image/tag/)、[Docker Documentation: docker run](https://docs.docker.com/reference/cli/docker/container/run/)

**原文節錄**：
```text
Usage:  docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**解析**：
- **佔位符風格**：使用 GNU 風格的純大寫英文單詞（`SOURCE_IMAGE`、`TARGET_IMAGE`、`IMAGE`）。
- **可選版本/標籤後綴**：`SOURCE_IMAGE[:TAG]`。在佔位符後直接緊貼 `[:TAG]`，外圍中括號代表該部分可省略，但若要指定 tag，前綴冒號 `:` 為語法的一部分。

#### 3. npm（以 `npm install` 為例）
來源：[npm Docs: npm-install](https://docs.npmjs.com/cli/commands/npm-install)

**原文節錄**：
```text
npm install [<@scope>/]<name>
npm install [<@scope>/]<name>@<tag>
npm install [<@scope>/]<name>@<version>
```
*(在綜合手冊與通用 CLI 文件中通常合寫為：`npm install [<@scope>/]<name>[@<version>]`)*

**解析**：
- **佔位符風格**：採用 `<name>`、`<version>`、`<tag>` 角括號佔位符。
- **可選前綴與可選版本後綴**：
  - `[<@scope>/]`：可選的組織作用域前綴，包含結尾的 `/`。
  - `[@<version>]`：可選的版本後綴，中括號內包含版本識別前綴 `@`，表示若省略版本則安裝最新預設版本。

---

### 四、結論

#### 1. POSIX / GNU / docopt 通用記法對照表

| 記法 (Notation) | 語法意義 (Meaning) | 典型範例 | 規範來源 |
| :--- | :--- | :--- | :--- |
| **`literal`** (粗體 / 直接書寫) | 原樣輸入的指令、子命令或旗標名稱 | `git`、`install`、`-v` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)、[man-pages(7)](https://man7.org/linux/man-pages/man7/man-pages.7.html) |
| **`[ ... ]`** | **可選（Optional）**：內容可省略，可出現 0 或 1 次 | `[-f]`、`[<file>]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`...`** (Ellipsis) | **可重複（Repeatable）**：前一項可出現 1 次或多次 | `FILE...`、`[ARG...]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`[ ... ]...`** | **可重複可選**：可出現 0 次或多次 | `[OPTION]...`、`[FILE...]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`\|`** (Pipe) | **互斥（Mutually Exclusive）**：二選一或多選一 | `a \| b` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`[ a \| b ]`** | **可選互斥**：從 a 與 b 中最多選一個，亦可都不選 | `[-a \| -b]` | [docopt](http://docopt.org/)、[POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`( a \| b )`** 或 **`{ a \| b }`** | **必選互斥**：必須嚴格二選一 | `(-m \| -M)`、`{start\|stop}` | [docopt](http://docopt.org/)、[Git docs](https://git-scm.com/docs/git-branch) |
| **`*name*`** / **`<name>`** / **`NAME`** | **參數佔位符**：由使用者替換為實際值 | `<branch-name>`、`FILE` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)、[GNU Standards](https://www.gnu.org/prep/standards/standards.html) |
| **`name[delimiter<suffix>]`** | **可選後綴**：相鄰黏合的可選標籤/版本 | `IMAGE[:TAG]`、`<pkg>[@<ver>]` | 主流套件管理與容器慣例 |

---

#### 2. 特別解答：「二選一」在 Linux 慣例中的符號與流派

1. **二選一符號一律為 `|`（垂直線），絕對不是 `a／b`**：
   - **語法規範標準**：無論是 POSIX.1-2017（12.1 第 8 條）、Linux man-pages(7)、GNU Coding Standards、還是 docopt，**表示互斥選擇的標準符號只有垂直線 `|`（vertical bar）**。
   - **為什麼不能用斜線 `/`**：
     - **路徑衝突**：在 Unix/Linux 架構中，正斜線 `/` 是根目錄與路徑分隔符（Path separator）。若在參數語法中使用 `a/b`，會與檔案路徑（如 `path/to/file`）或帶作用域的名稱（如 `@scope/pkg`）產生嚴重的語法歧義。
     - **形式文法傳承**：`|` 自 1960 年代 BNF（巴科斯範式）開始就是形式文法中表示「選擇/Alternation」的公認符號，正則表達式（Regex）亦同。
     - **少數非標準特例**：日常非正式討論、簡易 README、或是早期 MS-DOS / Windows 命令行手冊（因 DOS 早期使用 `/` 作為選項前綴，如 `/s /q`）偶爾會見到 `y/n` 或 `-y/--yes`，但在任何 Linux / POSIX 官方規範中均屬非正式寫法。

2. **「必選二選一」的括號流派差異**：
   - **`docopt` 與 Git 流派——圓括號 `(a|b)`**：
     `docopt` 正式定義中，中括號代表 optional，圓括號代表 required grouping。因此 `(a|b)` 是現代 CLI 解析器與 Git 等工具官方手冊中標註「必選二選一」最常見的寫法。
   - **EBNF 與系統服務手冊流派——大括號 `{a|b}`**：
     源自標準 EBNF 文法與部分 Unix/Linux init 腳本（例如 `/etc/init.d/service {start|stop|restart}`）以及網通設備（Cisco/Juniper）手冊。在這些文件中，大括號代表必選集合（required set），與代表可選的中括號 `[a|b]` 形成對稱。
   - **POSIX 原生流派——拆分多行 SYNOPSIS**：
     POSIX 官方標準在遇到頂層必填互斥時，傾向不依賴額外括號，而是直接列出多行獨立的 SYNOPSIS（如 `utility_name -d ...` 與 `utility_name -e ...`），以最嚴謹的方式消除括號巢狀帶來的歧義。
