# 01 頁移出待歸位

- 【名稱】圖文中的名稱一律寫全名，不使用縮寫。 → 主圖第 0 頁（圖例與記法）
- 【寫法】寫法：小寫原文，前面省略 `just vendor_kit`。 → 主圖第 0 頁（圖例與記法）
- 【組件與模組】VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。 → 14 架構圖
- 【專案（舊表列）】**專案**｜project｜使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑 → 09 下游 repo 契約③（接入後含 `.vendor_kit/`）；→ 05 規則（動詞都在專案裡跑）
- 【下游 repo（舊表列）】**下游 repo**｜downstream repo｜提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由使用者自決；私有需憑證）。`<repo>` 是它的名字 → 09 下游 repo 契約③（三行 Dockerfile、純資料 image）；→ 12 CI 契約⑤（公開或私有、私有需憑證）
- 【引擎（舊定義）】**引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。 → 14 架構圖（所有判斷與寫檔都在裡面）；→ 10 契約④（只透過掛入的 `/repo` 看專案根）
- 【薄殼（舊定義）】**薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。 → 06 目錄樹（五個檔）；→ 07 schema（自描述標頭與 hash 契約）
- 【啟動器（舊定義）】**啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。 → 10 契約④（拉 image、展開工具內容、起引擎容器）
- 【版本解析】版本解析｜`resolve`｜讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔 → 14 架構圖
- 【取件】取件｜`fetch`｜把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記 → 14 架構圖
- 【初始檔合併】初始檔合併｜`initfile`｜依工具宣告建初始檔、存基準版、升版時做三方合併 → 14 架構圖
- 【薄殼產生】薄殼產生｜`shell`｜產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改 → 14 架構圖
- 【進度與寫入】進度與寫入｜`progress`｜建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續 → 14 架構圖
- 【設定與格式】設定與格式｜`schema`｜讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml` → 14 架構圖
- 【紀錄】紀錄｜`log`｜每次執行寫一份執行紀錄 → 14 架構圖
- 【清理】清理｜`prune`｜找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除 → 14 架構圖
- 【專案檔】**專案檔**｜project file｜根 `justfile`、根 `.dockerignore`、建立後歸使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則 → 02 不變量
- 【VK 檔】**VK 檔**｜VK file｜VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄 → 07 schema
- 【進 git 的檔】**進 git 的檔**｜tracked file｜會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔 → 07 schema
- 【版本鎖定行】**版本鎖定行**｜lock line｜`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = "<image>:<tag>@sha256:<digest>"`；工具行在 `[tools]` 表下 `<repo> = "<image>:<tag>@sha256:<digest>"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 → 07 schema（正規形）；→ 07 schema（`<repo>` 名稱規則）
- 【正式版】**正式版**｜release version｜registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版 → 05 規則
- 【初始檔】**初始檔**｜init file｜工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸使用者、進 git → 07 schema
- 【基準版】**基準版**｜baseline｜`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是使用者的現況與新版初始檔） → 07 schema
- 【三方合併】**三方合併**｜three-way merge｜升版時對每個納管初始檔拿基準版（共同祖先）、使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記 → 05 規則
- 【metadata】**metadata**｜metadata｜基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git → 07 schema
- 【可寫動詞】**可寫動詞**｜writing verb｜會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune → 57 狀態機
- 【唯讀動詞】**唯讀動詞**｜read-only verb｜不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git） → 57 狀態機
- 【進度檔】**進度檔**｜progress file｜可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用） → 57 狀態機
- 【執行紀錄】**執行紀錄**｜run log｜`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事 → 10 契約④
- 【CI 模式】**CI 模式**｜CI mode｜環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查） → 05 規則
- 【需人處理】**需人處理**｜needs human｜動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色 → 主圖第 0 頁（顏色）；→ 59 結束碼（結束碼）
- 【失敗】**失敗**｜failure｜拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色 → 主圖第 0 頁（顏色）；→ 59 結束碼（結束碼）
- 【專案檔四原則】**專案檔四原則**｜four rules｜① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容） → 02 不變量
- 【預檢】**預檢**｜precheck｜動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動 → 05 規則
- 【resolve／apply（兩段式）】**resolve／apply（兩段式）**｜two-phase｜兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器 → 10 契約④
- 【介面版】**介面版**｜protocol version｜薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關 → 10 契約④
- 【檔案版】**檔案版**｜schema version｜VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔 → 07 schema
- 【最低介面版】**最低介面版**｜floor｜引擎仍支援的最低介面版；固定常數；只能經 ADR 提高 → 10 契約④
- 【結束碼】**結束碼**｜exit code｜`0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入 → 59 結束碼
- 【本機覆寫】**本機覆寫**｜local override｜`version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行 → 07 schema
- 【symlink】**symlink**｜symlink｜符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄 → 05 規則
- 【hash】**hash**｜hash｜檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗 → 05 規則
- 【image ID】**image ID**｜image ID｜docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同 → 07 schema
- 【tty】**tty**｜tty｜互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束 → 05 規則
- 【佔位符】**佔位符**｜placeholder｜`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id → 主圖第 0 頁（文件記法）；→ 07 schema（`<repo>` 名稱規則）
- 【下游 image】**下游 image**｜downstream image｜`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64 → 05 規則
- 【`dist/`】**`dist/`**｜dist｜下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 → 07 schema
- 【工具 recipe】**工具 recipe**｜tool recipe｜工具的 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` → 05 規則
- 【專案根】**專案根**｜project root｜專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套 → 05 規則
- 【`cache/`、`gen/`】**`cache/`、`gen/`**｜—｜`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入） → 07 schema
- 【印記】**印記**｜stamp｜`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源 → 07 schema
- 【納管】**納管**｜managed｜初始檔經使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過） → 07 schema
- 【自描述標頭】**自描述標頭**｜self-describing header｜薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」） → 07 schema
- 【救援路徑】**救援路徑**｜rescue path｜不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help → 10 契約④
- 【語法記法：`<x>`】`<x>`｜必填佔位符 → 主圖第 0 頁
- 【語法記法：`[x]`】`[x]`｜可省略 → 主圖第 0 頁
- 【語法記法：`[@<tag>]`】`[@<tag>]`｜可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`） → 主圖第 0 頁
- 【語法記法：`-x <值>`／`--long <值>`】`-x <值>`／`--long <值>`｜短／長選項等價；只有常用的才有短的 → 主圖第 0 頁
- 【語法記法：`-y`】`-y`｜不帶值的開關 → 主圖第 0 頁
- 【語法記法：`a／b`】`a／b`｜二選一 → 主圖第 0 頁
- 【語法記法（POSIX 版改寫）】`<x>` 佔位符、`[x]` 可省略、`x...` 可重複、`a|b` 二選一、`[a|b]` 可省略的二選一、`(a|b)` 必選其一、`<repo>[@<tag>]` 可省略的版本後綴、`-x <值>`|`--long <值>` 短長等價。來源：[POSIX.1-2017 XBD §12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)、[man-pages(7)](https://man7.org/linux/man-pages/man7/man-pages.7.html)、[docopt](http://docopt.org/)、[GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html) → 主圖第 0 頁
- 【選項清單：-t】`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：-p】`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：-i】`-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--yes】`-y`／`--yes`：省略詢問，視同回答「是」。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--exit-code】`--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--dry-run】`--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：選項】`--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：選項】`--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--verify】`--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--no-justfile】`--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：--help】`--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。 → 04 動詞介面表（語意移至 05 規則）
- 【選項清單：選項】`--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。 → 04 動詞介面表（語意移至 05 規則）
- 【動詞：`install`】`install`｜第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init` → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`uninstall`】`uninstall`｜移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被使用者改過的 `config.toml` 與薄殼、非空目錄 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`add <repo>[@<tag>]`】`add <repo>[@<tag>]`｜接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`remove <repo>`】`remove <repo>`｜移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`update [<repo>]`】`update [<repo>]`｜只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`upgrade [<repo>[@<tag>]]`】`upgrade [<repo>[@<tag>]]`｜升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`】`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`｜把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`undev <repo>`／`undev vendor_kit`】`undev <repo>`／`undev vendor_kit`｜撤銷 dev，回到版本鎖定行的版本 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`sync [<repo>]`】`sync [<repo>]`｜依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`prune`】`prune`｜刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋 → 04 動詞介面表；→ 流程頁 15 以後
- 【動詞：`help`】`help`｜印命名空間層說明；不觸網、只寫執行紀錄 → 04 動詞介面表；→ 流程頁 15 以後
- 【升引擎】**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。 → 04 動詞介面表；→ 流程頁 15 以後
- 【記法與顏色】記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。 → 主圖第 0 頁

## 附錄原文

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
