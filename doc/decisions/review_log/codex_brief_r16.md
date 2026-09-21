你在目錄 <scratchpad>/ 工作。本次只動三個檔：`decisions/review/terms.md`、`disc_v1_a.py`、`lint_pages.py`。其他所有檔一律不碰（特別是 `decisions/review/invariants_roles.md`、`disc_v1_b.py`、`disc_v1_c.py`、`gen_disc.py`）。不要跑 gen_disc.py（它會寫到專案目錄），不要 git 操作。做完只回報改了哪些行。

A. `decisions/review/terms.md`（先備份成 `decisions/review/terms.pre_r16.md`）：
1. 「## 三方與承諾關係」節標題改為「## 兩方與承諾關係」，角色表只剩兩列（表頭四欄不變：名稱｜是誰｜跟 VK 的互動｜地位）：
   - **使用者**｜是誰：會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI｜跟 VK 的互動：直接跑 `just vendor_kit …`｜地位：被承諾方。
   - **VK**｜是誰：我們，vendor_kit 開發者｜跟 VK 的互動：維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更｜地位：承諾方。
   - 表後那一段（原「同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。」）整句改成：「只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。」
2. 全檔「下游使用者」「下游開發者」一律改成「使用者」（含「專案」定義「使用者的 git repo」、下游 repo「由使用者自決」、初始檔／基準版／三方合併／納管／uninstall／專案檔／工具 recipe 等各條）；「三方合併」這個詞**不改**（它是 three-way merge 的譯名，跟角色無關）；「對兩方的承諾」→「對使用者的承諾」。改完 grep 確認檔內不再出現「下游使用者」「下游開發者」「三方與承諾」。
3. 其餘定義文字一律不動（包括附錄）。

B. `disc_v1_a.py`（先備份成 `disc_v1_a.py.pre_r16`）：只動「# ================= P0 v1p0」到「# ================= P1 v1p1」之前這一段（目前約第 476–624 行，下面附全文）。把 v1p0／v1p0c／v1p0b 三頁合併成**一頁 v1p0**：
   - 頁名與 rtitle 標題都改成「名詞與縮寫」（不要「（1）」之類副標）。`pages_v1_a.append(("v1p0", "名詞與縮寫", p0))` 只 append 這一次。
   - 內容順序照 terms.md 從頭到「## 動詞」表結束（含「升引擎 = …」那段與「記法與顏色見主圖第 0 頁…」那句；「附錄」不上圖，跟現況一樣）。所有格子都接在同一個 Y 流上、同一個 list p0 裡；格 id 前綴一律用 `p0_`（原 `p0c_`／`p0b_` 的格改成 `p0_`，例如 `p0b_t1`→`p0_t5`、`p0b_t2`→`p0_t6`、`p0b_t3`→`p0_t7`、`p0b_o*`→`p0_o*`、`p0b_v*`→`p0_v*`、`p0b_s1`→`p0_s4`、`p0b_s2`→`p0_s5`、`p0b_s3`→`p0_s6`、`p0b_n0`→`p0_n0`），確認同一頁內 id 不重複。
   - 常用詞不再拆 T4_SPLIT：`Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)` 一次畫完，刪掉 T4_SPLIT 變數。頁面可以很長，drawio 沒有高度限制。
   - v1p0c／v1p0b 兩個區塊（含它們的 rtitle、append）整段刪除。
   - 圖上文字必須跟改後的 terms.md 逐字相同（定義文字經 M() 去反引號／粗體）：
     * 節標題「三方與承諾關係」→「兩方與承諾關係」。
     * 角色表沿用 mtbl 直排寫法（表頭：名稱｜是誰｜跟 VK 的互動｜地位），只是列數變兩列；欄寬可調（例如 名稱 150、是誰 870、跟 VK 的互動 300、地位 260，合計 1580），內容照 A.1。
     * 表後那句 p0_t1n 改成 A.1 的新句子。
     * 所有含「下游使用者」「下游開發者」「對兩方的承諾」的格文字照 A.2 改成「使用者」「對使用者的承諾」（專案、下游 repo、專案檔、初始檔、基準版、三方合併、納管、工具 recipe、uninstall 等）。「三方合併」不改。
   - 改完用 `grep -n "下游使用者\|下游開發者\|三方與承諾\|v1p0c\|v1p0b\|p0c_\|p0b_\|T4_SPLIT" disc_v1_a.py` 確認全部為 0 筆。
   - 語法檢查：`python3 -c "import ast;ast.parse(open('disc_v1_a.py').read())"`。

C. `lint_pages.py`：審閱頁（page id `v1p0`、`v1p1`、`v1p1i`）豁免 `page-height` 與 `term-count` 兩條規則。小改：加一個常數 `REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']`，在第 418 行 `if on('term-count') and len(d['terms']) > TERM_MAX:` 與第 426 行 `if on('page-height') and nodes:` 兩處條件各加 `and pid not in REVIEW_PAGE_IDS`；並把 `PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']` 改成 `PAGE0_IDS = ['v1p0']`（那兩頁已不存在）。docstring 第 32–33 行可補一句「審閱頁 REVIEW_PAGE_IDS 豁免」。其他規則不變。

---- 現行 decisions/review/terms.md 全文 ----
# 名詞與縮寫

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
| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |

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
| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
| **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
| **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
| **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
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
| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
| **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
| **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
| **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
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
| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
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

---- 現行 disc_v1_a.py 第 476–624 行 ----
# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
Y = 70
Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
# ---- 三方與承諾關係 ----
Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
 ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
 ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
 ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
])
Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
 ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
 ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
])
# ---- VK 組件 ----
Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
Y = para(p0, "p0_c0", Y, M("VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。"))
COMP = [
 M("**引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。"),
 M("**薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。"),
 M("**啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。"),
]
CW = 516; ch = max(hvl(t, CW, RLH) for t in COMP)          # 516×3 + 16×2 = 1580
for i, t in enumerate(COMP):
    p0.append(vb(f"p0_c{i + 1}", "1", rlh(LT12), t, RX + i * (CW + 16), Y, CW, ch))
Y += ch + 10
Y = sec(p0, "p0_s2b", Y, "VK 模組（module）——引擎內的 8 個程式單元")
Y = mtbl(p0, "p0_t3", Y, [("中文名", 150), ("英文代號", 150), ("做什麼", 1280)], [
 ["版本解析", "`resolve`", "讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔"],
 ["取件", "`fetch`", "把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記"],
 ["初始檔合併", "`initfile`", "依工具宣告建初始檔、存基準版、升版時做三方合併"],
 ["薄殼產生", "`shell`", "產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改"],
 ["進度與寫入", "`progress`", "建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續"],
 ["設定與格式", "`schema`", "讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml`"],
 ["紀錄", "`log`", "每次執行寫一份執行紀錄"],
 ["清理", "`prune`", "找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除"],
], bold0=False)
# ---- 常用詞 ----
T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
T4 = [
 ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
 ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
 ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
 ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
 ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
 ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
 ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
 ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
 ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
 ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
 ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
 ["**進度檔**", "progress file", "可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用）"],
 ["**執行紀錄**", "run log", "`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事"],
 ["**CI 模式**", "CI mode", "環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查）"],
 ["**需人處理**", "needs human", "動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色"],
 ["**失敗**", "failure", "拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色"],
 ["**專案檔四原則**", "four rules", "① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容）"],
 ["**預檢**", "precheck", "動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動"],
 ["**resolve／apply（兩段式）**", "two-phase", "兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器"],
 ["**介面版**", "protocol version", "薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關"],
 ["**檔案版**", "schema version", "VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔"],
 ["**最低介面版**", "floor", "引擎仍支援的最低介面版；固定常數；只能經 ADR 提高"],
 ["**結束碼**", "exit code", "`0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入"],
 ["**本機覆寫**", "local override", "`version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行"],
 ["**symlink**", "symlink", "符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄"],
 ["**hash**", "hash", "檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗"],
 ["**image ID**", "image ID", "docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同"],
 ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
 ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
]
T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
Y = sec(p0, "p0_s3", Y, "常用詞")
Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))

# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
Y = 70
Y = sec(p0c, "p0c_s3", Y, "常用詞")
Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))

# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
Y = 70
Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
 ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
 ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
 ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
 ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
 ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
 ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
 ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
 ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
 ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
])
# ---- 語法記法 ----
Y = sec(p0b, "p0b_s2", Y, "語法記法")
Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
 ["`<x>`", "必填佔位符"],
 ["`[x]`", "可省略"],
 ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
 ["`-x <值>`／`--long <值>`", "短／長選項等價；只有常用的才有短的"],
 ["`-y`", "不帶值的開關"],
 ["`a／b`", "二選一"],
], bold0=False)
Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
OPTS = [
 "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
 "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
 "`-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。",
 "`-y`／`--yes`：省略詢問，視同回答「是」。",
 "`--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。",
 "`--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。",
 "`--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。",
 "`--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。",
 "`--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。",
 "`--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。",
 "`--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。",
 "`--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。",
]
for i, t in enumerate(OPTS):
    h = hvl(M(t), RW, RLH, pad=2)
    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
Y += 10
# ---- 動詞 ----
Y = sec(p0b, "p0b_s3", Y, "動詞")
Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
 ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
 ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
 ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
 ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
 ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
 ["`upgrade [<repo>[@<tag>]]`", "升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行"],
 ["`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`", "把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔"],
 ["`undev <repo>`／`undev vendor_kit`", "撤銷 dev，回到版本鎖定行的版本"],
 ["`sync [<repo>]`", "依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發"],
 ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
 ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
], bold0=False)
Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
