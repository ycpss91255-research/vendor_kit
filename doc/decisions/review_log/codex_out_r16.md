Reading additional input from stdin...
OpenAI Codex v0.155.1
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: low
reasoning summaries: none
session id: 01a0c44f-c420-7142-b1ec-73b95b2857d7
--------
user
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
codex
我會嚴格限制在指定三檔與兩個備份檔；先核對實際內容和行界，再以補丁修改，最後只做指定的 grep 與 AST 檢查。
exec
/usr/bin/bash -lc "sed -n '1,220p' decisions/review/terms.md && sed -n '450,660p' disc_v1_a.py && sed -n '1,70p' lint_pages.py && sed -n '390,445p' lint_pages.py" in <scratchpad>
 succeeded in 0ms:
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
def rlh(st):
    return st + f"lineHeight={RLH};"
def sec(out, pid, y, title, w=None):
    """節標題（LBL）。回傳結束 y。"""
    out.append(v(pid, "1", LBL, title, RX, y, w or RW, 28)); return y + 32
def para(out, pid, y, text, style=None, w=None, x=RX, pad=6):
    """一段文字一格（白底 12pt、行距 RLH）。回傳結束 y（含 10px 間距）。"""
    w = w or RW; st = rlh(style or LT12)
    h = hvl(text, w, RLH, pad=pad)
    out.append(vb(pid, "1", st, text, x, y, w, h)); return y + h + 10
def mtbl(out, prefix, y, cols, rows, x=RX, bold0=True):
    """md 表格 → tbl()（表頭灰底、第一欄粗體、行距 RLH）；rows 內每格先過 M()。回傳結束 y（含 14px 間距）。"""
    return tbl(out, prefix, "1", x, y, cols, [[M(c) for c in r] for r in rows], bold0=bold0, lh=RLH) + 14
def kvblock(out, prefix, y, rows, kw=130, x=RX, w=None):
    """直排的「標籤｜內容」表：一列一格對（第 0 列灰底當該組標題）；rows: [(標籤, 內容)]，內容先過 M()。回傳結束 y（含 14px 間距）。"""
    w = w or RW
    for r, (k, val) in enumerate(rows):
        val = M(val); fill = "#e6e6e6" if r == 0 else "#ffffff"
        h = max(hvl(k, kw, RLH, pad=2), hvl(val, w - kw, RLH, pad=2))
        out.append(vb(f"{prefix}_r{r}c0", "1", rlh(tbl_style(fill, bold=True)), k, x, y, kw, h))
        out.append(vb(f"{prefix}_r{r}c1", "1", rlh(tbl_style(fill, bold=(r == 0))), val, x + kw, y, w - kw, h))
        y += h
    return y + 14
def rtitle(pid, title):
    return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]

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

# ================= P1 v1p1：審閱頁 01 不變量與角色 =================
p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
Y = 70
Y = para(p1, "p1_intro", Y, M("本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。"))
Y = sec(p1, "p1_s0", Y, "一句話目的")
Y = para(p1, "p1_goal", Y, M("下游 repo 把要交付的檔案打成一個純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）；下游使用者在專案裡跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。"), style=RULE)
Y = sec(p1, "p1_s1", Y, "本頁名詞（第 0 頁沒有的頁內特有詞）")
Y = mtbl(p1, "p1_tm", Y, [("名詞", 170), ("定義", 1410)], [
 ["GHCR", "GitHub 的容器 registry；引擎放的地方，也是下游 image 的預設落點（下游 image 公開或私有由下游開發者自決）。"],
 ["`config.toml`", "`.vendor_kit/config.toml`，VK 的設定檔，進 git；升引擎時比照初始檔三方合併。"],
 ["衝突標記", "三方合併合不起來時留在檔內的 `<<<<<<<`／`>>>>>>>` 標記；升版逐檔的結果：沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 三方合併，合不起來就留衝突標記、結束碼 2。"],
 ["交付物", "工具 recipe（`just <ns> …`）產生、要交給別人用的東西（例如 deploy 包）。"],
 ["契約檢查腳本", "`.vendor_kit/ci/check.sh`，薄殼之一，兩種用法分開：不帶參數 = 下游 CI 的唯一入口（在專案裡跑同步、驗證、試跑升版、工具與專案測試）；`--dist` = 下游開發者在下游 repo 裡驗 `dist/` 佈局與兩平台一致。"],
 ["下游 CI", "專案自己的 CI 平台；不是「方」。"],
 ["Renovate", "下游使用者自選的版本更新機器人；不是「方」。"],
])
# ---- 三方角色表 ----
Y = sec(p1, "p1_s2", Y, "三方角色與承諾關係")
ROLES = [                                        # md 五欄表 → 一個角色一組直排（名稱列灰底＋是誰／負責／不負責／地位）
 ["**下游開發者**", "開發下游 repo 的人", "維護 `dist/` 與三行 Dockerfile；在下游 repo 的 CI 用契約檢查腳本 `--dist` 驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；把下游 image 推到 registry（公開或私有自決；私有時下游使用者要備憑證）；用 dev／undev 在本機開發工具", "不碰專案的檔；交付物不得依賴 `.vendor_kit/`；交付物的可執行性不由 VK 代驗", "被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了"],
 ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版時 `-y` 只是同意做三方合併，合併後仍有衝突就要手動編輯、再重跑 `upgrade <repo>` 直到乾淨；把契約檢查腳本接進下游 CI", "不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼", "被承諾方：VK 保證不刪、不覆蓋專案檔，失敗必印原因"],
 ["**VK**", "我們，vendor_kit 開發者", "維護引擎與薄殼（含啟動器），履行對兩方的承諾", "不替工具驗可執行；不 commit、不開 PR；引擎不讀 `.git`、不碰 index、不 `git init`", "承諾方：內部怎麼實作不屬於本契約，可自由變更"],
]
for i, row in enumerate(ROLES):
    Y = kvblock(p1, f"p1_tr{i}", Y, list(zip(["名稱", "是誰", "負責", "不負責", "地位"], row)))
Y = para(p1, "p1_trn", Y, M("同一人可兼下游開發者與下游使用者兩種身分。"))
Y = sec(p1, "p1_s3", Y, "兩個自動化角色（不是「方」）")
AUTO = [
 M("下游 CI：專案自己的 CI 平台（GitHub、GitLab 都一樣）只呼叫契約檢查腳本；腳本自己把 `CI` 設為 1 進 CI 模式，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。"),
 M("Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，大版本升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。"),
]
AW = 782; ah = max(hvl(t, AW, RLH) for t in AUTO)          # 782×2 + 16 = 1580
for i, t in enumerate(AUTO):
    p1.append(vb(f"p1_auto{i}", "1", rlh(LT12), t, RX + i * (AW + 16), Y, AW, ah))
Y += ah + 10
"""三階段 draw.io 審查工具鏈 ─ 第 2 步：機械 lint。
用法: python3 lint_pages.py <outdir>            （<outdir> = extract_pages.py 的輸出目錄）
輸出 <outdir>/lint.md（依頁分組，每條含 id、規則代號、等級 warn/info）與 <outdir>/lint.json（同內容，機器用）。

規則（代號）：
  dangling   懸空：流程頁（頁名符合 FLOW_PAGE_RE）上 step／decision 要有進邊＋出邊；end_* 只需進邊（綠橢圓沒進邊但有出邊 = 起點，不報）；
             entry 只需出邊；IMG（紫 image 框）至少一條線（info）。非流程頁略過（info 一行）。
  decision   判斷菱形出邊數 ≠ 2（warn）；出邊標籤不以「是」「否」開頭（info；「失敗」「成功」「是：…」「否 →…」都算列出）；兩條出邊標籤相同（warn）。
  endcolor   終點顏色 vs 文字：含「→ 0」「0：」但不是綠（warn）；含「→ 1／2／3」或以「1：／2：／3：」開頭但是綠（warn）；
             含「請」「先」「手動」「重跑」「解決」而是紅（info：候選改橙）。
  xref       文字引用的頁名在頁名清單找不到（warn）；只靠拆字模糊比對到（info）。
  term-diff  跨頁：同一名詞 name 在不同頁 text 不一致 → 列版本與差異摘要（放在最後「跨頁」段；warn）。
  base       文字出現 \\bbase\\b（排除 BASE_ALLOW 內的片語；warn）。
  color      頁內 fillColor 不在該頁圖例（warn；白／none 不算）；沒有圖例的頁 info。
  termcov    名詞覆蓋：node 文字出現 KEYWORDS 的關鍵字，名詞表沒有對應條：名詞 name 或 text 含 → 過（text-only 的只彙總成一行 info）；都沒有 → warn。
  onething   一格一事候選：step／end 節點文字中「→」「並」「然後」「再」「、」「；」總數 ≥ 2 → info（交第 3 階段代理判定）。

v2 新增（每條可在 ENABLED 關閉；等級都是 warn）：
  event-name      node／edge 文字出現 launcher_started|…|_completed 等舊事件名 → 「事件名須用 spec 註冊表：launcher_start/exit、engine_start/exit」。
  resolve-3way    流程頁上文字含「docker run」且含「resolve」的 step：沿出邊走（藍 SUB／file／note 不計步；「續「X」頁」出口會接到 X 頁的「來自」入口）
                  ≤ RESOLVE_3WAY_DEPTH 步內，須同時有 (A) decision 文字含「回 0」「結束碼 0」「非 0」，(B) 另一個 decision／step 文字含「6-30」或「文法」（A≠B）。
  precheck-recover 頁名含 install|add|remove|upgrade|dev|undev|uninstall|升引擎 的第一頁（頁名含「（1）」或不含全形括號，且頁上有起點綠橢圓）
                  須有 decision 文字含「未完成」「既有進度檔」「恢復」；頁名含 sync|update 的第一頁須有節點文字含「6-33」；prune 頁只要有「只列出」。
  end-color-text  end 節點：文字含「→ 0」或以「0：」開頭 → 須 end_ok；含 6-24|6-31|6-38|6-30|寫不進|拉不到 → 須 end_red；
                  含 請|先 |手動|重跑|→ 3|6-4|6-33 且不含紅關鍵字 → 須 end_orange（舊 endcolor 保留）。
  xref-forward    xrefs 指到的頁序號（頁名前綴數字；沒有就用 pages.json 順序）大於本頁 → 「前引」；「續「X」頁」出口允許向後，排除。
  write-line      step 文字（去掉「是：」「否 →」前綴後）以 寫|建|刪|原子替換|append 開頭或含「→ 檔」，頁內有 file 節點，但沒有出邊指到 file 節點。
                  例外詞 WRITE_LINE_EXEMPT（印、印出…；「印記」只在「寫印記」時算寫入）。
  write-fail-edge 同上寫入 step：必須有一條「可見」出邊滿足其一：target 是 end_red／end_orange、target 文字含「失敗匯流」、label 含「失敗」；
                  否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
  hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
  term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
  merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
"""
import re, json, os, sys, glob, difflib
from collections import defaultdict, Counter

# ---------- 可調參數 ----------
FLOW_PAGE_RE = re.compile(r'^(?:\d+ )?(流程|狀態機)')   # 頁名可帶序號前綴「NN 」
KEYWORDS = [                      # (顯示名, regex)。名詞表的 name 或 text 含到 regex 命中的原字串就算覆蓋
    ('訊息碼 6-xx', r'\b6-\d+[a-z]?\b'),
    ('.tmp.*', r'\.tmp\.[A-Za-z_]+'),
    ('gen/…', r'\bgen/[\w.]*'),
    ('version.local.toml', r'version\.local\.toml'),
    ('version.toml', r'(?<!local\.)\bversion\.toml'),
    ('config.toml', r'config\.toml'),
    ('log/', r'\blog/'),
    ('baseline/', r'baseline/'),
    ('cache/', r'\bcache/'),
    ('metadata', r'metadata'),
    ('frozen', r'\bfrozen\b'),
    ('flock', r'\bflock\b'),
    ('digest', r'\bdigest\b'),
    ('--local', r'--local\b'),
    ('resolve／apply', r'\b(resolve|apply)\b'),
    ('Renovate', r'\bRenovate\b'),
    ('薄殼', r'薄殼'),
    ('進度日誌', r'進度日誌'),
]
BASE_ALLOW = ['對齊 base 的 just 慣例', 'test-base', 'base_raw', 'base_ref']   # 這些片語裡的 base 不算實例
COLOR_WHITELIST = {'#ffffff', 'none', '-', ''}
ONETHING_TOKENS = ['→', '並', '然後', '再', '、', '；']
ONETHING_MIN = 2
YESNO_RE = re.compile(r'^(是|否)')
NEEDS_HUMAN = ['請', '先', '手動', '重跑', '解決']

# ---------- v2 新規則的開關與參數 ----------
HIDDEN_EDGE = True   # 隱形邊（visible=0）視為不存在；並另報 hidden-edge warn
ENABLED = {                       # False = 關掉該條
                m = re.match(r'([A-Za-z_.]+|離線包|升引擎)', n); return m.group(1).lower() if m else n
            same = any(_series(page_names[i]) == _series(page_names[ctx['page_ids'].index(pid)]) for i in tis) if tis else False
            if same and _series(page_names[ctx['page_ids'].index(pid)]) in ('bootstrap.sh', 'install', 'add', 'sync', 'upgrade', 'dev', 'undev', 'remove', 'uninstall', 'prune', 'update', '離線包'):
                continue
            if _series(page_names[ctx['page_ids'].index(pid)]) == 'bootstrap.sh' and tis and all(_series(page_names[i]) in ('install', 'add') for i in tis):
                continue   # bootstrap 呼叫 install／add 是它的定義，允許往後見
            if seqs and min(seqs) > cur:
                add('xref-forward', 'warn', x['id'], f'前引：頁 {cur} 只能引用序號更小的頁，卻{x["kind"] if x["kind"] != "其他" else "引用"}「{x["ref"]}」頁（序號 {min(seqs)}）')

    # ---- hidden-edge ----
    if on('hidden-edge'):
        for e in d['edges']:
            if e.get('hidden'):
                add('hidden-edge', 'warn', e['id'], f'隱形邊（visible=0）：{e["source"]} → {e["target"]}；lint 視為不存在，請改成可見線或刪掉')

    # ---- write-line / write-fail-edge ----
    if WRITE_PAGE_RE.search(name):
        for n in nodes:
            if not is_write_step(n): continue
            o = outs[n['id']]
            if on('write-line') and file_nodes and not any(e['target'] in file_nodes for e in o):
                add('write-line', 'warn', n['id'], f'寫入格缺到檔案框的線：「{n["text"][:40]}」')
            if on('write-fail-edge'):   # 只看可見出邊（graph() 已排除隱形邊）
                has_fail = any(byid[e['target']]['kind'] in ('end_red', 'end_orange') or WRITE_FAIL_HUB_RE.search(byid[e['target']]['text']) or '失敗' in e['label'] for e in o)
                if not has_fail:
                    add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')

    # ---- term-count / term-dup-page0 ----
    if on('term-count') and len(d['terms']) > TERM_MAX:
        add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
    if on('term-dup-page0') and pid not in PAGE0_IDS:
        for t in d['terms']:
            if term_key(t['name']) in ctx['page0_terms']:
                add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')

    # ---- page-height / edge-font ----
    if on('page-height') and nodes:
        bottom = max(n['y'] + n['h'] for n in nodes)
        if bottom > PAGE_MAX_H:
            low = max(nodes, key=lambda n: n['y'] + n['h'])
            add('page-height', 'warn', low['id'], f'頁高 {bottom} > {PAGE_MAX_H}（最低格 {low["id"]}「{low["text"][:20]}」）')
    if on('edge-font'):
        bad = [e for e in d['edges'] if e.get('fontSize') not in (None, EDGE_FONT)]
        for e in bad: add('edge-font', 'warn', e['id'], f'線標籤 fontSize={e["fontSize"]} ≠ {EDGE_FONT}：「{e["label"][:30]}」')

    # ---- merge-fanout ----
    if on('merge-fanout') and is_flow:
        for n in nodes:
            if n['kind'] != 'step': continue
            o = outs[n['id']]
            if len(o) >= MERGE_FANOUT_MIN and all(byid[e['target']]['kind'] in END_KINDS for e in o):
                add('merge-fanout', 'warn', n['id'], f'終點扇出：分支來源不可辨（{len(o)} 條出邊全到終點）：「{n["text"][:40]}」')

def lint_terms(pages, out):
    by = defaultdict(lambda: defaultdict(list))     # name -> text -> [pid]
    for d in pages:

exec
/usr/bin/bash -lc 'cp decisions/review/terms.md decisions/review/terms.pre_r16.md
cp disc_v1_a.py disc_v1_a.py.pre_r16' in <scratchpad>
 succeeded in 0ms:
apply patch
patch: completed
<scratchpad>/decisions/review/terms.md
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..899ffe568655ada231dcb64759a3e0ab095b4c06
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,15 +2,14 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..899ffe568655ada231dcb64759a3e0ab095b4c06
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,15 +2,14 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 

apply patch
patch: completed
<scratchpad>/decisions/review/terms.md
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |

apply patch
patch: completed
<scratchpad>/disc_v1_a.py
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..9c2f247a6eaf2dfd6f987e7058ce381feb1579c5
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..9c2f247a6eaf2dfd6f987e7058ce381feb1579c5
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],

apply patch
patch: completed
<scratchpad>/disc_v1_a.py
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")

exec
/usr/bin/bash -lc 'rg -n "PAGE0_IDS|TERM_MAX|PAGE_MAX_H|term-count|page-height" lint_pages.py' in <scratchpad>
 succeeded in 0ms:
32:  term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
33:  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
72:    'write-line': True, 'write-fail-edge': True, 'term-count': True, 'term-dup-page0': True,
73:    'page-height': True, 'edge-font': True, 'merge-fanout': True, 'hidden-edge': True,
96:TERM_MAX = 8
97:PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
98:PAGE_MAX_H = 2400
417:    # ---- term-count / term-dup-page0 ----
418:    if on('term-count') and len(d['terms']) > TERM_MAX:
419:        add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
420:    if on('term-dup-page0') and pid not in PAGE0_IDS:
425:    # ---- page-height / edge-font ----
426:    if on('page-height') and nodes:
428:        if bottom > PAGE_MAX_H:
430:            add('page-height', 'warn', low['id'], f'頁高 {bottom} > {PAGE_MAX_H}（最低格 {low["id"]}「{low["text"][:20]}」）')
501:        page0_terms=page0_term_names([by_id[pid0] for pid0 in PAGE0_IDS if pid0 in by_id]),

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")

apply patch
patch: completed
<scratchpad>/lint_pages.py
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
diff --git a/lint_pages.py b/lint_pages.py
index cae6ee89a3f5385b774468b2a89ce3e48d1460e9..9e1ab1e2ef9d2a15b435c38e414af8b5d135c789
--- a/lint_pages.py
+++ b/lint_pages.py
@@ -30,7 +30,7 @@
                   否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
   hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
   term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
-  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
+  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
   merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
 """
 import re, json, os, sys, glob, difflib
@@ -94,7 +94,8 @@
 WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
 WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
 TERM_MAX = 8
-PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
+PAGE0_IDS = ['v1p0']
+REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
 PAGE_MAX_H = 2400
 EDGE_FONT = '12'
 MERGE_FANOUT_MIN = 3
@@ -415,7 +416,7 @@
                     add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
 
     # ---- term-count / term-dup-page0 ----
-    if on('term-count') and len(d['terms']) > TERM_MAX:
+    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
         add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
     if on('term-dup-page0') and pid not in PAGE0_IDS:
         for t in d['terms']:
@@ -423,7 +424,7 @@
                 add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
 
     # ---- page-height / edge-font ----
-    if on('page-height') and nodes:
+    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
         bottom = max(n['y'] + n['h'] for n in nodes)
         if bottom > PAGE_MAX_H:
             low = max(nodes, key=lambda n: n['y'] + n['h'])

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
diff --git a/lint_pages.py b/lint_pages.py
index cae6ee89a3f5385b774468b2a89ce3e48d1460e9..9e1ab1e2ef9d2a15b435c38e414af8b5d135c789
--- a/lint_pages.py
+++ b/lint_pages.py
@@ -30,7 +30,7 @@
                   否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
   hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
   term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
-  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
+  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
   merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
 """
 import re, json, os, sys, glob, difflib
@@ -94,7 +94,8 @@
 WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
 WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
 TERM_MAX = 8
-PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
+PAGE0_IDS = ['v1p0']
+REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
 PAGE_MAX_H = 2400
 EDGE_FONT = '12'
 MERGE_FANOUT_MIN = 3
@@ -415,7 +416,7 @@
                     add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
 
     # ---- term-count / term-dup-page0 ----
-    if on('term-count') and len(d['terms']) > TERM_MAX:
+    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
         add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
     if on('term-dup-page0') and pid not in PAGE0_IDS:
         for t in d['terms']:
@@ -423,7 +424,7 @@
                 add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
 
     # ---- page-height / edge-font ----
-    if on('page-height') and nodes:
+    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
         bottom = max(n['y'] + n['h'] for n in nodes)
         if bottom > PAGE_MAX_H:
             low = max(nodes, key=lambda n: n['y'] + n['h'])

codex
三個修改已套用；我正在核對單頁 ID 唯一性與禁詞。這裡會依你「disc_v1_a.py 只動 P0～P1 前」的範圍限制，不改 P1 以後既有文字。
exec
/usr/bin/bash -lc "grep -n \"下游使用者\\|下游開發者\\|三方與承諾\" decisions/review/terms.md || true
grep -n \"下游使用者\\|下游開發者\\|三方與承諾\\|v1p0c\\|v1p0b\\|p0c_\\|p0b_\\|T4_SPLIT\" disc_v1_a.py || true
python3 -c \"import ast;ast.parse(open('disc_v1_a.py').read())\"
python3 -c \"import ast;ast.parse(open('lint_pages.py').read())\"
sed -n '470,640p' disc_v1_a.py | rg -o '\"p0_[A-Za-z0-9_{} +]+\"|f\"p0_[A-Za-z0-9_{} +]+\"' | sort | uniq -d
rg -n \""'^(# ================= P0|pages_v1_a.append'"\\(\\(\\\"v1p0|# ================= P1)|PAGE0_IDS|REVIEW_PAGE_IDS|if on\\('term-count'\\)|if on\\('page-height'\\)\" disc_v1_a.py lint_pages.py" in <scratchpad>
 succeeded in 0ms:
5:第十四輪（備份 .v15）：新增審閱頁 00 v1p0／v1p0b「名詞與縮寫」（decisions/review/terms.md 逐字）、v1p1 重排為審閱頁 01「不變量與角色」（decisions/review/invariants_roles.md 逐字；出處對照不上圖）。
6:第十五輪（r13_codex/findings_00_01.md；備份 .v16）：審閱頁去掉 md 沒有的圖例／續頁句／「寫法約定」；常用詞拆到 v1p0c、不變量拆到 v1p1i；三方角色表改直排；審閱頁內容寬 1580、行距 1.4。
337: "state5": ("初始檔五態（state）", "metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（下游使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"),
431: "initfile": ("初始檔", "init.toml 複製到專案的檔（歸下游使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"),
435: "semver": ("SemVer", "版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高最低介面版或需要下游使用者手動步驟；minor = 新功能（含介面版 +1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR"),
617:Y = para(p1, "p1_goal", Y, M("下游 repo 把要交付的檔案打成一個純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）；下游使用者在專案裡跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。"), style=RULE)
620: ["GHCR", "GitHub 的容器 registry；引擎放的地方，也是下游 image 的預設落點（下游 image 公開或私有由下游開發者自決）。"],
622: ["衝突標記", "三方合併合不起來時留在檔內的 `<<<<<<<`／`>>>>>>>` 標記；升版逐檔的結果：沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 三方合併，合不起來就留衝突標記、結束碼 2。"],
624: ["契約檢查腳本", "`.vendor_kit/ci/check.sh`，薄殼之一，兩種用法分開：不帶參數 = 下游 CI 的唯一入口（在專案裡跑同步、驗證、試跑升版、工具與專案測試）；`--dist` = 下游開發者在下游 repo 裡驗 `dist/` 佈局與兩平台一致。"],
626: ["Renovate", "下游使用者自選的版本更新機器人；不是「方」。"],
631: ["**下游開發者**", "開發下游 repo 的人", "維護 `dist/` 與三行 Dockerfile；在下游 repo 的 CI 用契約檢查腳本 `--dist` 驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；把下游 image 推到 registry（公開或私有自決；私有時下游使用者要備憑證）；用 dev／undev 在本機開發工具", "不碰專案的檔；交付物不得依賴 `.vendor_kit/`；交付物的可執行性不由 VK 代驗", "被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了"],
632: ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版時 `-y` 只是同意做三方合併，合併後仍有衝突就要手動編輯、再重跑 `upgrade <repo>` 直到乾淨；把契約檢查腳本接進下游 CI", "不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼", "被承諾方：VK 保證不刪、不覆蓋專案檔，失敗必印原因"],
637:Y = para(p1, "p1_trn", Y, M("同一人可兼下游開發者與下游使用者兩種身分。"))
641: M("Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，大版本升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。"),
706:p1b = head("p1b", "契約① 下游使用者介面（2／3）── 動詞介面表（interface_spec §1.2；just vendor_kit <verb> [args]）", 1200)
802:p1b.append(v("p1B", "1", SW(NEUTRAL), "2. 契約① 下游使用者介面：常用 3 + 進階 8 + 一次性 1 + help（綠底常用、白底進階、藍底一次性；一列一動詞、「做什麼」欄一格一件事；6-N = §6 訊息編號）", 40, Y, 1560, bh))
810:p1c = head("p1c", "契約① 下游使用者介面（3／3）── 規則、選項表（Q25）、結束碼（Q23／Q27）、不開的動詞、訊息文字（§6）", 1200)
962:ty = tnode("t_root", 0, "<b>專案/</b>（下游使用者的；專案根）", F_USER, ty)
964:ty = tnode("t_di", 1, "<b>.dockerignore</b> ── 下游使用者的；install 加四行 .vendor_kit/cache/、gen/、.tmp.*、log/（無 → 建；有 → 問 6-34／-y）\n寫：install（記於 baseline/.vendor_kit.toml）｜改：下游使用者隨意；uninstall 問後只刪原文相同行", F_USER, ty, True)
966:ty = tnode("t_ver", 2, "<b>version.toml</b> ── 進 git：唯一來源。vendor_kit = \"<ref>\" 版本鎖定行（唯一）、schema、written_by、[tools] 一行一工具 tag@digest\n寫：install／add／upgrade／remove（apply 最後才寫）｜改：下游使用者可手改、Renovate PR 改；sync 只讀", F_GIT, ty, True)
969:ty = tnode("t_cfg", 2, "<b>config.toml</b> ── 進 git：schema = 1、[log] keep = 50、days = 30（含註解與預設值；缺檔或缺鍵 = 預設；非正整數 → 預設 + 警告）\n寫：install 建；upgrade 當初始檔三方合併｜改：下游使用者隨意；引擎用 TOML parser 讀，啟動器只 grep 固定寫法的 ^keep *= *[0-9]+ *$", F_GIT, ty, True)
984:ty = tnode("t_repo", 2, "<b>cache/<repo>/</b> ── 不進 git、下游使用者不可改；只放從暫存 /dist 展開的內容（dev 時是 symlink → <dir>/dist）\n寫：引擎 fetch（apply 決定套用之後）｜改：不可改（verify 失敗 → 重裝並 warn）", F_NOGIT, ty, True)
990:ty = tnode("t_user", 1, "<b>初始檔</b>（例 Dockerfile…；路徑由 init.toml 的 dest 決定）── 專案檔；進 git；state 記在 metadata（五態）\n寫：add 建（已存在不納管；append 問後加行）、upgrade 逐檔問後換／三方合併／建新檔｜改：下游使用者隨意；remove／uninstall 永不刪，印清單", F_USER, ty, True)
1023:ry = rex("p2_jf", "根 justfile（下游使用者的；install 新建時逐字四行；已有時只加第一行）",
1026:ry = rex("p2_di", "根 .dockerignore（下游使用者的；install append 四行；uninstall 問後只刪原文相同行）",
1073:VER_META = "進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；下游使用者、Renovate 可手改；sync 只讀"
1094: ["根 justfile（下游使用者的）", "install 只加一行 import '.vendor_kit/entry.just'；無檔則建，內容逐字四行：import 一行／空行／default:／\\t@just --list；uninstall 只刪完全相同行"],
1095: ["根 .dockerignore（下游使用者的）", "install append 四行 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*、.vendor_kit/log/（無則建；有則問 6-34）；uninstall 問後只刪原文相同行"],
1106: ["[[file]].state", "string（單一列舉）", "managed（已納管）／appended（append 已插入）／declined（新增檔被拒、從未納管）／unmanaged（本來就有、沒納管）／deleted（下游使用者刪了已納管檔，upgrade 維持刪除）"],
1153:p2c = head("p2c", "契約② 專案裡的檔（3／3）── 動詞 × 檔案矩陣、會碰／不碰下游使用者東西、version.toml 怎麼被讀", 1200)
1163:y = rbox(tmp, "p2c_not", "p2C", RULE, "<b>不碰</b>：下游使用者的 .gitignore（除非工具以 strategy=append 宣告且你同意）、.git/info/exclude（dev 也不寫）、.git 本身（引擎不讀 .git、不碰 index、不做 git init）；我們要忽略的路徑全放 .vendor_kit/.gitignore；-y 不授權覆蓋既有未納管檔、不硬加 append 行", 20, y, 1520, tagged=True)
1589: ["11", "下游使用者改薄殼／未納管檔／append", "不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn"],
1686: ["檔案與路徑", "10、11、13、19、20、21", "fresh clone 無 gen/；下游使用者改薄殼／未納管檔／append；異常 TOML；append 換行；空白路徑；worktree／submodule"],
1819:H0 = "下游使用者\n打 just vendor_kit <動詞> …\n或 just <ns> …"
1852:p4.append(v("p4H", "1", GRPB(NEUTRAL), "主機（下游使用者電腦／CI runner）── just 載入鏈與目錄（線 = 誰載入誰）", HXo, LY, HW, LH))
1863:# 主機側載入鏈（codex v1p4 #3）：下游使用者 → 根 justfile → entry.just → vendor.just／tools.just → 工具 recipe；vendor.just source log.sh；工具 recipe 的 _sync 回叫 just vendor_kit sync
1950:c, Y = lgd("p4", 40, Y, ["v3img", "v4mod", "v4unit", "v4host", "v4hgrp", "v4egrp", "v4pgrp", "v2git", "v2no", "v2usr", "v2code", "v2tag", "v4other", "notep", "pendq"], "實線 = 資料流（線上文字 = 傳什麼）\n雙箭頭 = 讀寫都有；黃橢圓 = 下游使用者", maxw=1300)
lint_pages.py:32:  term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
lint_pages.py:33:  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
lint_pages.py:97:PAGE0_IDS = ['v1p0']
lint_pages.py:98:REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
lint_pages.py:419:    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
lint_pages.py:421:    if on('term-dup-page0') and pid not in PAGE0_IDS:
lint_pages.py:427:    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
lint_pages.py:502:        page0_terms=page0_term_names([by_id[pid0] for pid0 in PAGE0_IDS if pid0 in by_id]),
disc_v1_a.py:476:# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
disc_v1_a.py:610:pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
disc_v1_a.py:612:# ================= P1 v1p1：審閱頁 01 不變量與角色 =================
disc_v1_a.py:649:# ================= P1i v1p1i：審閱頁 01 不變量與角色（2）=================
disc_v1_a.py:705:# ================= P1b v1p1b：契約① 動詞介面表 =================
disc_v1_a.py:809:# ================= P1c v1p1c：契約① 規則、選項表、不開的動詞 =================

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
diff --git a/lint_pages.py b/lint_pages.py
index cae6ee89a3f5385b774468b2a89ce3e48d1460e9..9e1ab1e2ef9d2a15b435c38e414af8b5d135c789
--- a/lint_pages.py
+++ b/lint_pages.py
@@ -30,7 +30,7 @@
                   否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
   hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
   term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
-  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
+  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
   merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
 """
 import re, json, os, sys, glob, difflib
@@ -94,7 +94,8 @@
 WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
 WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
 TERM_MAX = 8
-PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
+PAGE0_IDS = ['v1p0']
+REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
 PAGE_MAX_H = 2400
 EDGE_FONT = '12'
 MERGE_FANOUT_MIN = 3
@@ -415,7 +416,7 @@
                     add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
 
     # ---- term-count / term-dup-page0 ----
-    if on('term-count') and len(d['terms']) > TERM_MAX:
+    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
         add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
     if on('term-dup-page0') and pid not in PAGE0_IDS:
         for t in d['terms']:
@@ -423,7 +424,7 @@
                 add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
 
     # ---- page-height / edge-font ----
-    if on('page-height') and nodes:
+    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
         bottom = max(n['y'] + n['h'] for n in nodes)
         if bottom > PAGE_MAX_H:
             low = max(nodes, key=lambda n: n['y'] + n['h'])

exec
/usr/bin/bash -lc "sed -n '476,611p' disc_v1_a.py | grep -n \"下游使用者\\|下游開發者\\|三方與承諾\\|v1p0c\\|v1p0b\\|p0c_\\|p0b_\\|T4_SPLIT\" || true
nl -ba decisions/review/terms.md | sed -n '1,135p'
nl -ba disc_v1_a.py | sed -n '476,615p'
nl -ba lint_pages.py | sed -n '28,36p;92,102p;414,431p'" in <scratchpad>
 succeeded in 0ms:
     1	# 名詞與縮寫
     2	
     3	本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
     4	
     5	## 兩方與承諾關係
     6	
     7	| 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
     8	|---|---|---|---|
     9	| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
    10	| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
    11	
    12	只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
    13	
    14	兩種 repo 要分清楚：
    15	
    16	| 中文名 | 英文 | 定義 |
    17	|---|---|---|
    18	| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
    19	| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
    20	
    21	## VK 組件（component）
    22	
    23	VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。
    24	
    25	- **引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。
    26	- **薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。
    27	- **啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。
    28	
    29	### VK 模組（module）——引擎內的 8 個程式單元
    30	
    31	| 中文名 | 英文代號 | 做什麼 |
    32	|---|---|---|
    33	| 版本解析 | `resolve` | 讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔 |
    34	| 取件 | `fetch` | 把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記 |
    35	| 初始檔合併 | `initfile` | 依工具宣告建初始檔、存基準版、升版時做三方合併 |
    36	| 薄殼產生 | `shell` | 產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改 |
    37	| 進度與寫入 | `progress` | 建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續 |
    38	| 設定與格式 | `schema` | 讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml` |
    39	| 紀錄 | `log` | 每次執行寫一份執行紀錄 |
    40	| 清理 | `prune` | 找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除 |
    41	
    42	## 常用詞
    43	
    44	| 中文名 | 英文 | 定義 |
    45	|---|---|---|
    46	| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
    47	| **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
    48	| **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
    49	| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
    50	| **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
    51	| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
    52	| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
    53	| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
    54	| **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
    55	| **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
    56	| **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
    57	| **進度檔** | progress file | 可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用） |
    58	| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事 |
    59	| **CI 模式** | CI mode | 環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查） |
    60	| **需人處理** | needs human | 動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色 |
    61	| **失敗** | failure | 拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色 |
    62	| **專案檔四原則** | four rules | ① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容） |
    63	| **預檢** | precheck | 動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動 |
    64	| **resolve／apply（兩段式）** | two-phase | 兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器 |
    65	| **介面版** | protocol version | 薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關 |
    66	| **檔案版** | schema version | VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔 |
    67	| **最低介面版** | floor | 引擎仍支援的最低介面版；固定常數；只能經 ADR 提高 |
    68	| **結束碼** | exit code | `0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入 |
    69	| **本機覆寫** | local override | `version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行 |
    70	| **symlink** | symlink | 符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄 |
    71	| **hash** | hash | 檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗 |
    72	| **image ID** | image ID | docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同 |
    73	| **tty** | tty | 互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束 |
    74	| **佔位符** | placeholder | `<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id |
    75	
    76	### 其他既有詞
    77	
    78	| 中文名 | 英文 | 定義 |
    79	|---|---|---|
    80	| **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
    81	| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
    82	| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
    83	| **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
    84	| **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
    85	| **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
    86	| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
    87	| **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
    88	| **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
    89	
    90	## 語法記法
    91	
    92	動詞表與後頁的指令寫法一律照這張表。
    93	
    94	| 記法 | 意思 |
    95	|---|---|
    96	| `<x>` | 必填佔位符 |
    97	| `[x]` | 可省略 |
    98	| `[@<tag>]` | 可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`） |
    99	| `-x <值>`／`--long <值>` | 短／長選項等價；只有常用的才有短的 |
   100	| `-y` | 不帶值的開關 |
   101	| `a／b` | 二選一 |
   102	
   103	動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）：
   104	
   105	- `-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。
   106	- `-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。
   107	- `-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。
   108	- `-y`／`--yes`：省略詢問，視同回答「是」。
   109	- `--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。
   110	- `--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。
   111	- `--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。
   112	- `--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。
   113	- `--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。
   114	- `--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。
   115	- `--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。
   116	- `--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。
   117	
   118	## 動詞
   119	
   120	寫法：小寫原文，前面省略 `just vendor_kit`。
   121	
   122	| 動詞 | 做什麼 |
   123	|---|---|
   124	| `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
   125	| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
   126	| `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
   127	| `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
   128	| `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
   129	| `upgrade [<repo>[@<tag>]]` | 升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行 |
   130	| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔 |
   131	| `undev <repo>`／`undev vendor_kit` | 撤銷 dev，回到版本鎖定行的版本 |
   132	| `sync [<repo>]` | 依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發 |
   133	| `prune` | 刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋 |
   134	| `help` | 印命名空間層說明；不觸網、只寫執行紀錄 |
   135	
   476	# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
   477	p0 = rtitle("p0", "名詞與縮寫")
   478	Y = 70
   479	Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
   480	# ---- 兩方與承諾關係 ----
   481	Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
   482	Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
   483	 ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
   484	 ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
   485	])
   486	Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
   487	Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
   488	Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
   489	 ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
   490	 ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
   491	])
   492	# ---- VK 組件 ----
   493	Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
   494	Y = para(p0, "p0_c0", Y, M("VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。"))
   495	COMP = [
   496	 M("**引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。"),
   497	 M("**薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。"),
   498	 M("**啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。"),
   499	]
   500	CW = 516; ch = max(hvl(t, CW, RLH) for t in COMP)          # 516×3 + 16×2 = 1580
   501	for i, t in enumerate(COMP):
   502	    p0.append(vb(f"p0_c{i + 1}", "1", rlh(LT12), t, RX + i * (CW + 16), Y, CW, ch))
   503	Y += ch + 10
   504	Y = sec(p0, "p0_s2b", Y, "VK 模組（module）——引擎內的 8 個程式單元")
   505	Y = mtbl(p0, "p0_t3", Y, [("中文名", 150), ("英文代號", 150), ("做什麼", 1280)], [
   506	 ["版本解析", "`resolve`", "讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔"],
   507	 ["取件", "`fetch`", "把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記"],
   508	 ["初始檔合併", "`initfile`", "依工具宣告建初始檔、存基準版、升版時做三方合併"],
   509	 ["薄殼產生", "`shell`", "產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改"],
   510	 ["進度與寫入", "`progress`", "建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續"],
   511	 ["設定與格式", "`schema`", "讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml`"],
   512	 ["紀錄", "`log`", "每次執行寫一份執行紀錄"],
   513	 ["清理", "`prune`", "找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除"],
   514	], bold0=False)
   515	# ---- 常用詞 ----
   516	T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
   517	T4 = [
   518	 ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
   519	 ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
   520	 ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
   521	 ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
   522	 ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
   523	 ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
   524	 ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
   525	 ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
   526	 ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
   527	 ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
   528	 ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
   529	 ["**進度檔**", "progress file", "可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用）"],
   530	 ["**執行紀錄**", "run log", "`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事"],
   531	 ["**CI 模式**", "CI mode", "環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查）"],
   532	 ["**需人處理**", "needs human", "動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色"],
   533	 ["**失敗**", "failure", "拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色"],
   534	 ["**專案檔四原則**", "four rules", "① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容）"],
   535	 ["**預檢**", "precheck", "動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動"],
   536	 ["**resolve／apply（兩段式）**", "two-phase", "兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器"],
   537	 ["**介面版**", "protocol version", "薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關"],
   538	 ["**檔案版**", "schema version", "VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔"],
   539	 ["**最低介面版**", "floor", "引擎仍支援的最低介面版；固定常數；只能經 ADR 提高"],
   540	 ["**結束碼**", "exit code", "`0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入"],
   541	 ["**本機覆寫**", "local override", "`version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行"],
   542	 ["**symlink**", "symlink", "符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄"],
   543	 ["**hash**", "hash", "檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗"],
   544	 ["**image ID**", "image ID", "docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同"],
   545	 ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
   546	 ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
   547	]
   548	Y = sec(p0, "p0_s3", Y, "常用詞")
   549	Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
   550	Y = sec(p0, "p0_s4", Y, "其他既有詞")
   551	Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
   552	 ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
   553	 ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
   554	 ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
   555	 ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
   556	 ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
   557	 ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
   558	 ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
   559	 ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
   560	 ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
   561	])
   562	# ---- 語法記法 ----
   563	Y = sec(p0, "p0_s5", Y, "語法記法")
   564	Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
   565	Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
   566	 ["`<x>`", "必填佔位符"],
   567	 ["`[x]`", "可省略"],
   568	 ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
   569	 ["`-x <值>`／`--long <值>`", "短／長選項等價；只有常用的才有短的"],
   570	 ["`-y`", "不帶值的開關"],
   571	 ["`a／b`", "二選一"],
   572	], bold0=False)
   573	Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
   574	OPTS = [
   575	 "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
   576	 "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
   577	 "`-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。",
   578	 "`-y`／`--yes`：省略詢問，視同回答「是」。",
   579	 "`--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。",
   580	 "`--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。",
   581	 "`--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。",
   582	 "`--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。",
   583	 "`--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。",
   584	 "`--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。",
   585	 "`--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。",
   586	 "`--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。",
   587	]
   588	for i, t in enumerate(OPTS):
   589	    h = hvl(M(t), RW, RLH, pad=2)
   590	    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
   591	Y += 10
   592	# ---- 動詞 ----
   593	Y = sec(p0, "p0_s6", Y, "動詞")
   594	Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
   595	Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
   596	 ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
   597	 ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
   598	 ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
   599	 ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
   600	 ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
   601	 ["`upgrade [<repo>[@<tag>]]`", "升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行"],
   602	 ["`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`", "把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔"],
   603	 ["`undev <repo>`／`undev vendor_kit`", "撤銷 dev，回到版本鎖定行的版本"],
   604	 ["`sync [<repo>]`", "依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發"],
   605	 ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
   606	 ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
   607	], bold0=False)
   608	Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
   609	Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
   610	pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
   611	
   612	# ================= P1 v1p1：審閱頁 01 不變量與角色 =================
   613	p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
   614	Y = 70
   615	Y = para(p1, "p1_intro", Y, M("本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。"))
    28	                  例外詞 WRITE_LINE_EXEMPT（印、印出…；「印記」只在「寫印記」時算寫入）。
    29	  write-fail-edge 同上寫入 step：必須有一條「可見」出邊滿足其一：target 是 end_red／end_orange、target 文字含「失敗匯流」、label 含「失敗」；
    30	                  否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
    31	  hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
    32	  term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
    33	  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
    34	  merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
    35	"""
    36	import re, json, os, sys, glob, difflib
    92	WRITE_LINE_EXEMPT = ['印出', '印記', '印', '執行紀錄', 'launcher_', 'engine_', 'sync_fast_path']   # 寫入動詞後緊接這些詞就不算寫檔（「寫印記」例外，仍算；執行紀錄／事件 = 圖例約定隱含，不畫 log/ 框）
    93	WRITE_LINE_EXEMPT_ANY = ['到暫存', '暫存副本']      # 文字含這些 = 寫到暫存（不是專案裡的檔），不算
    94	WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
    95	WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
    96	TERM_MAX = 8
    97	PAGE0_IDS = ['v1p0']
    98	REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
    99	PAGE_MAX_H = 2400
   100	EDGE_FONT = '12'
   101	MERGE_FANOUT_MIN = 3
   102	
   414	                has_fail = any(byid[e['target']]['kind'] in ('end_red', 'end_orange') or WRITE_FAIL_HUB_RE.search(byid[e['target']]['text']) or '失敗' in e['label'] for e in o)
   415	                if not has_fail:
   416	                    add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
   417	
   418	    # ---- term-count / term-dup-page0 ----
   419	    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
   420	        add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
   421	    if on('term-dup-page0') and pid not in PAGE0_IDS:
   422	        for t in d['terms']:
   423	            if term_key(t['name']) in ctx['page0_terms']:
   424	                add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
   425	
   426	    # ---- page-height / edge-font ----
   427	    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
   428	        bottom = max(n['y'] + n['h'] for n in nodes)
   429	        if bottom > PAGE_MAX_H:
   430	            low = max(nodes, key=lambda n: n['y'] + n['h'])
   431	            add('page-height', 'warn', low['id'], f'頁高 {bottom} > {PAGE_MAX_H}（最低格 {low["id"]}「{low["text"][:20]}」）')

diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
diff --git a/lint_pages.py b/lint_pages.py
index cae6ee89a3f5385b774468b2a89ce3e48d1460e9..9e1ab1e2ef9d2a15b435c38e414af8b5d135c789
--- a/lint_pages.py
+++ b/lint_pages.py
@@ -30,7 +30,7 @@
                   否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
   hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
   term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
-  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
+  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
   merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
 """
 import re, json, os, sys, glob, difflib
@@ -94,7 +94,8 @@
 WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
 WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
 TERM_MAX = 8
-PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
+PAGE0_IDS = ['v1p0']
+REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
 PAGE_MAX_H = 2400
 EDGE_FONT = '12'
 MERGE_FANOUT_MIN = 3
@@ -415,7 +416,7 @@
                     add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
 
     # ---- term-count / term-dup-page0 ----
-    if on('term-count') and len(d['terms']) > TERM_MAX:
+    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
         add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
     if on('term-dup-page0') and pid not in PAGE0_IDS:
         for t in d['terms']:
@@ -423,7 +424,7 @@
                 add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
 
     # ---- page-height / edge-font ----
-    if on('page-height') and nodes:
+    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
         bottom = max(n['y'] + n['h'] for n in nodes)
         if bottom > PAGE_MAX_H:
             low = max(nodes, key=lambda n: n['y'] + n['h'])

codex
- `decisions/review/terms.md`：第 5、9–12、18–19、46、51–53、82、86、125 行。
- `disc_v1_a.py`：第 476–610 行。
- `lint_pages.py`：第 33、97–98、419、427 行。
- 已建立：`decisions/review/terms.pre_r16.md`、`disc_v1_a.py.pre_r16`。
diff --git a/decisions/review/terms.md b/decisions/review/terms.md
index 634a56a0f2f1cba5f53155b93806b22a1284fada..61b2351bb0bb00802184cf9c7c443a5735b2c610
--- a/decisions/review/terms.md
+++ b/decisions/review/terms.md
@@ -2,22 +2,21 @@
 
 本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。
 
-## 三方與承諾關係
+## 兩方與承諾關係
 
 | 名稱 | 是誰 | 跟 VK 的互動 | 地位 |
 |---|---|---|---|
-| **下游開發者** | 開發下游 repo 的人 | 照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具 | 被承諾方 |
-| **下游使用者** | 在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人 | 跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑 | 被承諾方 |
-| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更 | 承諾方 |
+| **使用者** | 會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
+| **VK** | 我們，vendor_kit 開發者 | 維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更 | 承諾方 |
 
-同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。
+只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。
 
 兩種 repo 要分清楚：
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案** | project | 下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
-| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字 |
+| **專案** | project | 使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 |
+| **下游 repo** | downstream repo | 提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 |
 
 ## VK 組件（component）
 
@@ -44,14 +43,14 @@
 
 | 中文名 | 英文 | 定義 |
 |---|---|---|
-| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
+| **專案檔** | project file | 根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 |
 | **VK 檔** | VK file | VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 |
 | **進 git 的檔** | tracked file | 會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 |
 | **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |
 | **正式版** | release version | registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 |
-| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git |
-| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔） |
-| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
+| **初始檔** | init file | 工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git |
+| **基準版** | baseline | `.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） |
+| **三方合併** | three-way merge | 升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 |
 | **metadata** | metadata | 基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git |
 | **可寫動詞** | writing verb | 會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune |
 | **唯讀動詞** | read-only verb | 不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） |
@@ -80,11 +79,11 @@
 |---|---|---|
 | **下游 image** | downstream image | `FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 |
 | **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |
-| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
+| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |
 | **專案根** | project root | 專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 |
 | **`cache/`、`gen/`** | — | `.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） |
 | **印記** | stamp | `gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 |
-| **納管** | managed | 初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
+| **納管** | managed | 初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） |
 | **自描述標頭** | self-describing header | 薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） |
 | **救援路徑** | rescue path | 不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help |
 
@@ -123,7 +122,7 @@
 | 動詞 | 做什麼 |
 |---|---|
 | `install` | 第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` |
-| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄 |
+| `uninstall` | 移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 |
 | `add <repo>[@<tag>]` | 接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 |
 | `remove <repo>` | 移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 |
 | `update [<repo>]` | 只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 |
diff --git a/disc_v1_a.py b/disc_v1_a.py
index ca063da8651f285895a0dfc05e0ef0e44e124c42..d57876c7a2f7bfa150ace400414322a4e75266f1
--- a/disc_v1_a.py
+++ b/disc_v1_a.py
@@ -473,22 +473,21 @@
 def rtitle(pid, title):
     return [v("title", "1", TITLE, title, RX, 20, 1400, 34)]
 
-# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
-p0 = rtitle("p0", "名詞與縮寫（1）三方／組件／模組／常用詞")
+# ================= P0 v1p0：審閱頁 00 名詞與縮寫 =================
+p0 = rtitle("p0", "名詞與縮寫")
 Y = 70
 Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
-# ---- 三方與承諾關係 ----
-Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
-Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 870), ("地位", 260)], [
- ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
- ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
- ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
+# ---- 兩方與承諾關係 ----
+Y = sec(p0, "p0_s1", Y, "兩方與承諾關係")
+Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 870), ("跟 VK 的互動", 300), ("地位", 260)], [
+ ["**使用者**", "會跑 VK 動詞的人，兩個場合：①在下游 repo 裡維護 `dist/`、把工具打成下游 image、用 dev／undev 在本機開發工具；②在專案裡跑 `bootstrap.sh` 接入、add／upgrade／remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI", "直接跑 `just vendor_kit …`", "被承諾方"],
+ ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對使用者的承諾；內部實作不屬契約、可變更", "承諾方"],
 ])
-Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
+Y = para(p0, "p0_t1n", Y, M("只打 `just <ns> …` 的人不是『方』：VK 在他背後只做工具 recipe 前的自動 `sync`；sync 失敗的訊息要寫清楚該找誰、做什麼，但那是對使用者的承諾內容，不是另一個角色。圖文一律寫全名，不縮寫。"))
 Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
 Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1230)], [
- ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
- ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
+ ["**專案**", "project", "使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
+ ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字"],
 ])
 # ---- VK 組件 ----
 Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
@@ -516,14 +515,14 @@
 # ---- 常用詞 ----
 T4_COLS = [("中文名", 190), ("英文", 170), ("定義", 1220)]
 T4 = [
- ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
+ ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
  ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
  ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
  ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
  ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
- ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
- ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
- ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
+ ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git"],
+ ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔）"],
+ ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
  ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
  ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
  ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
@@ -546,37 +545,24 @@
  ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
  ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
 ]
-T4_SPLIT = 9                                    # 常用詞 29 條：前 9 條留本頁，其餘到 v1p0c
 Y = sec(p0, "p0_s3", Y, "常用詞")
-Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4[:T4_SPLIT])
-pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／模組／常用詞", p0))
-
-# ================= P0c v1p0c：審閱頁 00 名詞與縮寫（2）常用詞（續）=================
-p0c = rtitle("p0c", "名詞與縮寫（2）常用詞（續）")
-Y = 70
-Y = sec(p0c, "p0c_s3", Y, "常用詞")
-Y = mtbl(p0c, "p0c_t4", Y, T4_COLS, T4[T4_SPLIT:])
-pages_v1_a.append(("v1p0c", "名詞與縮寫（2）常用詞（續）", p0c))
-
-# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
-p0b = rtitle("p0b", "名詞與縮寫（3）既有詞／記法／動詞")
-Y = 70
-Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
-Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
+Y = mtbl(p0, "p0_t4", Y, T4_COLS, T4)
+Y = sec(p0, "p0_s4", Y, "其他既有詞")
+Y = mtbl(p0, "p0_t5", Y, [("中文名", 190), ("英文", 190), ("定義", 1200)], [
  ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
  ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
- ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
+ ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
  ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
  ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
  ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
- ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
+ ["**納管**", "managed", "初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
  ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
  ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
 ])
 # ---- 語法記法 ----
-Y = sec(p0b, "p0b_s2", Y, "語法記法")
-Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
-Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1320)], [
+Y = sec(p0, "p0_s5", Y, "語法記法")
+Y = para(p0, "p0_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
+Y = mtbl(p0, "p0_t6", Y, [("記法", 260), ("意思", 1320)], [
  ["`<x>`", "必填佔位符"],
  ["`[x]`", "可省略"],
  ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
@@ -584,7 +570,7 @@
  ["`-y`", "不帶值的開關"],
  ["`a／b`", "二選一"],
 ], bold0=False)
-Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
+Y = para(p0, "p0_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
 OPTS = [
  "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
  "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
@@ -601,14 +587,14 @@
 ]
 for i, t in enumerate(OPTS):
     h = hvl(M(t), RW, RLH, pad=2)
-    p0b.append(vb(f"p0b_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
+    p0.append(vb(f"p0_o{i + 1}", "1", rlh(LT12), M(t), RX, Y, RW, h)); Y += h
 Y += 10
 # ---- 動詞 ----
-Y = sec(p0b, "p0b_s3", Y, "動詞")
-Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
-Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1250)], [
+Y = sec(p0, "p0_s6", Y, "動詞")
+Y = para(p0, "p0_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
+Y = mtbl(p0, "p0_t7", Y, [("動詞", 330), ("做什麼", 1250)], [
  ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
- ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
+ ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄"],
  ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
  ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
  ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
@@ -619,9 +605,9 @@
  ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
  ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
 ], bold0=False)
-Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
-Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
-pages_v1_a.append(("v1p0b", "名詞與縮寫（3）既有詞／記法／動詞", p0b))
+Y = para(p0, "p0_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
+Y = para(p0, "p0_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
+pages_v1_a.append(("v1p0", "名詞與縮寫", p0))
 
 # ================= P1 v1p1：審閱頁 01 不變量與角色 =================
 p1 = rtitle("p1", "不變量與角色（1）目的／名詞／角色")
diff --git a/lint_pages.py b/lint_pages.py
index cae6ee89a3f5385b774468b2a89ce3e48d1460e9..9e1ab1e2ef9d2a15b435c38e414af8b5d135c789
--- a/lint_pages.py
+++ b/lint_pages.py
@@ -30,7 +30,7 @@
                   否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
   hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
   term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
-  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。
+  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
   merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
 """
 import re, json, os, sys, glob, difflib
@@ -94,7 +94,8 @@
 WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
 WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
 TERM_MAX = 8
-PAGE0_IDS = ['v1p0', 'v1p0c', 'v1p0b']
+PAGE0_IDS = ['v1p0']
+REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
 PAGE_MAX_H = 2400
 EDGE_FONT = '12'
 MERGE_FANOUT_MIN = 3
@@ -415,7 +416,7 @@
                     add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')
 
     # ---- term-count / term-dup-page0 ----
-    if on('term-count') and len(d['terms']) > TERM_MAX:
+    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
         add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
     if on('term-dup-page0') and pid not in PAGE0_IDS:
         for t in d['terms']:
@@ -423,7 +424,7 @@
                 add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')
 
     # ---- page-height / edge-font ----
-    if on('page-height') and nodes:
+    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
         bottom = max(n['y'] + n['h'] for n in nodes)
         if bottom > PAGE_MAX_H:
             low = max(nodes, key=lambda n: n['y'] + n['h'])

tokens used
69,630
- `decisions/review/terms.md`：第 5、9–12、18–19、46、51–53、82、86、125 行。
- `disc_v1_a.py`：第 476–610 行。
- `lint_pages.py`：第 33、97–98、419、427 行。
- 已建立：`decisions/review/terms.pre_r16.md`、`disc_v1_a.py.pre_r16`。
