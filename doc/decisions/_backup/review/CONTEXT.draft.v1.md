# vendor_kit

工具 repo 把要交付的檔案打成純資料的容器 image；下游專案用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。本檔只放名詞；決議在 `docs/adr/`，規格在 issue。

## 三方

**下游開發者（downstream developer）**：開發工具 repo 的人；照 `dist/` 出貨契約打包工具 image，用 dev／undev 在本機開發工具。被承諾方。
_避免_：工具方、上游、工具 repo 開發者、供應側

**下游使用者（downstream user）**：在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人。被承諾方。
_避免_：使用者、專案方、下游專案、專案維護者

**VK（vendor_kit）**：我們，vendor_kit 開發者；維護引擎 image 與薄殼，履行對兩方的承諾。承諾方。
_避免_：vendor_kit 開發者（三方語境時）

**承諾方／被承諾方（promisor / promisee）**：VK 對兩個下游承諾「照契約用一定可以、不會隨便改」；同一人可兼下游開發者與下游使用者兩種身分。

## VK 的零件

**引擎（engine）**：VK 的主程式，是容器 image `ghcr.io/<org>/vendor_kit:vN`；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根；主機不用裝引擎的語言環境。

**薄殼（shell）**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔：`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`。

**啟動器（launcher）**：薄殼內的 POSIX sh 片段；拉 image、展開工具內容、起引擎容器；不解析 TOML、不 eval。

**`bootstrap.sh`（bootstrap script）**：release 附的腳本，第一次接入時的啟動器；下載引擎後呼叫 `install`，再逐一 `add` 指定的工具。

**自描述首行（self-describing header）**：薄殼每檔首行 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；引擎重算比對，不符就不動。

**救援路徑（rescue path）**：不依賴 `gen/` 的單段引擎呼叫（install、升引擎、sync 的不符提示、help）；任何 ≥ 最低介面版的薄殼永久可用。

**暫存目錄（scratch dir）**：啟動器把工具 image 內容 `docker cp` 到專案內 `.vendor_kit/.tmp.dist.<id>/`，再唯讀掛進引擎容器當 `/dist`；結束即刪。

### VK 模組（引擎內的程式模組）

**版本解析（resolve）**：讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔。

**取件（fetch）**：把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記。

**初始檔合併（initfile）**：依工具宣告建初始檔、存基準版、升版時做三方合併。

**薄殼產生（shell）**：產生或重產薄殼五檔與自描述首行，並比對薄殼是否被改。

**交易（txn）**：建、恢復、刪進度檔，讓可寫動詞中斷後能接續。

**設定與格式（schema）**：讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml`。

**紀錄（log）**：每次執行寫一份執行紀錄。

**清理（prune）**：找出版本鎖定行未引用的舊 image、殘留容器與暫存並刪除。

## 專案裡的檔案

**專案根（project root）**：含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套；動詞只准在這一層執行。

**專案檔（project file）**：專案內不是 VK 自產的一切：根 `justfile`、根 `.dockerignore`、建立後的初始檔、其他原有檔。
_避免_：使用者的檔、使用者檔

**專案檔四原則（four rules for project files）**：① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容）。
_避免_：使用者檔四原則、不變量 I1

**VK 檔（VK file）**：VK 自己建、自己管的檔：`.vendor_kit/` 內的 `version.toml`、`config.toml`、薄殼、基準版、`cache/`、`gen/`、進度檔、執行紀錄；不受專案檔四原則。

**版本鎖定行（lock line）**：`.vendor_kit/version.toml` 內每個工具（與引擎）各一行 `<repo> = "…:<tag>@sha256:<digest>"`；進 git；只有這行決定裝哪一版；由 `add`／`upgrade`／`remove` 或 Renovate 改，回退 = `git revert`。
_避免_：鎖定行、正規行、`.version`

**`version.toml`（lock file）**：`.vendor_kit/version.toml`，放版本鎖定行的檔，專案的唯一版本來源；公開格式，工具可讀它寫來源紀錄。
_避免_：`.version`

**`version.local.toml`（local override）**：與 `version.toml` 同格式的覆寫檔，不進 git；dev 寫它把工具指向本機目錄或引擎指向本機 image；有同名那行就優先；檔不存在 = 沒人在用本機版。
_避免_：`.version.local`

**有效版本（effective version）**：`version.local.toml` 有同名那行就用它，否則用版本鎖定行。

**`config.toml`（config file）**：`.vendor_kit/config.toml`，VK 的設定檔，進 git；下游使用者可手改；升引擎時比照初始檔三方合併。

**`cache/`（cache）**：`.vendor_kit/cache/<repo>/`，工具內容的本機副本；不進 git、下游使用者不可改；每次升版整批替換；dev 時改為指向本機目錄。
_避免_：`.<repo>/`

**`gen/`（generated）**：`.vendor_kit/gen/`，引擎產生、供 just 載入的檔（`.stamp`、`<repo>.stamp`、`tools.just`）；不進 git；壞了刪掉再跑 `sync` 就回來。

**印記（stamp）**：`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest，之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源、不簽章。`gen/.stamp` 記產生薄殼的引擎版本。

**初始檔（init file）**：工具在 `dist/init.toml` 宣告、`add` 時複製（copy）或插入幾行（append）進專案的檔；建立後歸下游使用者、進 git；升版時三方合併，不自動覆蓋。

**範本（template）**：工具 `dist/` 裡給初始檔用的樣板；只複製，不渲染。

**基準版（baseline）**：`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；三方合併的第三份；升版合併完自動推到新版。
_避免_：baseline（中文語境）、基準

**納管（managed）**：初始檔經下游使用者同意建立後，VK 記下它的來源與狀態；拒絕建立也記（拒絕過）；本來就有的檔不納管。

**三方合併／衝突標記（three-way merge / conflict marker）**：升版對每個納管初始檔拿基準版、現況、新版三份 `git merge-file`：沒改 → 換新版；只有你改 → 不動；兩邊都改 → 檔內留 `<<<<<<< vendor_kit:baseline` 標記、結束碼 2；二進位檔不合併。

**進度檔（progress file）**：可寫動詞的交易紀錄 `.vendor_kit/.tmp.<verb>.<id>.toml`（或記在基準版旁的 metadata）；成功即刪；中斷後下次可寫動詞先恢復再繼續。
_避免_：進度日誌、交易日誌、交易紀錄

**執行紀錄（run log）**：`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞每次執行一檔；不進 git；事後追溯用；寫不進就不做任何事。
_避免_：操作紀錄檔、操作紀錄、log 檔

**根 justfile 一行 import（root justfile import line）**：下游使用者的 `justfile` 內唯一與 VK 有關的一行 `import '.vendor_kit/entry.just'`；`install` 建或問後加，`uninstall` 只刪完全相同的行。

**`just vendor_kit` 命名空間（namespace）**：VK 的動詞全部放在 `vendor_kit` 命名空間，不佔頂層；`just <ns> …` 是工具自己帶的，VK 不定義。

**鎖（lock）**：引擎對專案目錄本身 `flock`（不建鎖檔）；逾時 60 秒失敗；`VENDOR_KIT_NO_LOCK=1` 才放行；程序被殺系統自動解鎖。

## 工具側

**工具 repo（tool repo）**：提供工具的 git repo，`<repo>` 是它的名字；把 `dist/` 用三行 Dockerfile 打成工具 image 推到 GHCR。

**`dist/`（dist）**：工具 repo 裡要出貨的那批檔案：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨。

**`init.toml`（init manifest）**：`dist/init.toml`，工具提供的初始檔清單：`[[file]]` 一項一個，`src` 相對 `dist/`、`dest` 相對專案根、`strategy` 為 copy（預設）或 append。

**`Dockerfile.dist`（dist Dockerfile）**：工具 repo 出貨用的食譜，逐字三行：`FROM scratch`、`LABEL`、`COPY dist/ /dist/`；沒有程式。

**工具 image（tool image）**：`ghcr.io/<org>/<repo>-dist:<tag>`；`FROM scratch` 只放檔案，沒有程式、不會被執行；多架構 amd64 + arm64；VK 只搬移，不承諾內容可執行。

**兩棵樹比對（two-tree compare）**：取件的驗法：展開的 `/dist` 與 `cache/<repo>/` 逐檔比檔案集合、sha256、執行位；不比 mtime、owner。

**GHCR（GitHub Container Registry）**：工具 image 與引擎 image 放的地方；已釋出的版本永不刪。

**tag／digest（tag / digest）**：image 的版本名稱（`v1.2.0`）／內容指紋（`sha256:…`）；版本鎖定行兩者都記，引擎只認 digest。

**多架構（multi-arch）**：同一個 image 名稱同時提供 amd64 與 arm64，Docker 依主機自動選；版本鎖定行鎖的 digest 是 multi-arch index。平台：Linux amd64 + arm64、WSL2；armv7 不支援。

**甲版／乙版（variant A / variant B）**：甲版 = 工具 image `FROM vendor_kit`，每個工具 image 內都包引擎（已放棄）；乙版（現行）= 工具 image `FROM scratch` 只放檔案，引擎只有一份。

## 動詞

**動詞（verb）**：`just vendor_kit <動詞>` 的動詞；小寫原文書寫。共 11 個。

**`install`**：第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`，根 `justfile` 加一行；再跑 = 冪等修復；不做 `git init`。
_避免_：`--repair`、bootstrap 子命令

**`uninstall`**：對稱移除 VK 自產的檔與根 `justfile` 那一行；初始檔不刪只印清單；執行紀錄保留。
_避免_：`--purge`

**`add <repo>[@<tag>]`**：接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行。
_避免_：init、在 `.version` 手動加一行

**`remove <repo>`**：移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單。

**`update [<repo>]`**：只查有沒有新版，不寫任何檔；`--exit-code` 有新版回 2。

**`upgrade [<repo>[@<tag>]]`**：升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行。
_避免_：diff、accept、`--to <tag>`

**`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`**：把工具指到本機目錄（或引擎指到本機 image）；只寫 `version.local.toml`；工具須已在版本鎖定行。
_避免_：dev 模式（指狀態時寫「dev 覆寫中」）

**`undev <repo>`／`undev vendor_kit`**：撤銷 dev，回到版本鎖定行的版本。
_避免_：`dev <repo>` 不帶 `-p`

**`sync [<repo>]`**：依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發。
_避免_：ensure

**`prune`**：刪版本鎖定行未引用的舊 image、殘留容器／network／volume 與暫存。

**`help`**：印命名空間層說明；不觸網、不寫檔（執行紀錄除外）。

**升引擎（engine upgrade）**：`upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。
_避免_：自身升級、vendor_kit 自我更新

## 執行結果

**結束碼（exit code）**：`0` 成功（含 warn）；`1` 一般失敗或需人處理；`2` 合併衝突（留標記）；`3` 介面版／檔案版不合，先升級或退回，零寫入。
_避免_：結束狀態、退出碼

**需人處理（needs human）**：動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色。

**失敗（failure）**：拉不到、寫不進、驗證不過這類無法繼續的結束；結束碼 1；圖上紅色。

**CI 模式（CI mode）**：環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版。
_避免_：frozen

**「→ 1：X」／「→ 0」（exit notation）**：以結束碼 1 結束並印出 X／以結束碼 0 結束。

## 相容性

**介面版（protocol version）**：薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關。
_避免_：協定版、協定號、protocol P

**檔案版（schema version）**：VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔。
_避免_：格式版、schema 號

**最低介面版（floor）**：引擎仍支援的最低介面版；固定常數；只能經 ADR 提高。
_避免_：floor（中文語境）

**對外契約（public contract）**：VK 承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告；只對下游開發者與下游使用者承諾。

## 自動化角色

**下游 CI（downstream CI）**：下游專案自己的 CI 平台，只呼叫契約檢查腳本；不是「方」。

**契約檢查腳本（check script）**：`.vendor_kit/ci/check.sh`，薄殼之一；自設 `CI=1` 進 CI 模式，依序同步、驗證、試跑升版、跑工具與專案測試；`--dist` 給工具 repo 驗 `dist/` 佈局。

**Renovate（Renovate）**：下游自選的版本更新機器人，用 VK 提供的設定；PR 只改版本鎖定行，major 分開 PR；初始檔合併由下游使用者本機補完。VK 本身沒有機器人。

## VK 自己的 repo

**測試分層（test layers）**：VK repo 的 Dockerfile stage 與強制閘門：環境檢查 → lint／unit → integration（一個模組一個 stage）→ release → system → acceptance（假專案裡真的打 just）。

**鏡射／黑箱（mirror check / blackbox check）**：lint 層的兩個自寫檢查：每個引擎模組必有對應測試檔；system、acceptance 測試不准 import 引擎程式碼，只准 docker run、just 與檔案系統。

## 佔位符

**`<repo>`**：工具 repo 名。
_避免_：`<name>`

**`<ns>`**：工具的 just 命名空間；一個工具可有多個。

**`<tag>`**：image 版本名。

**`<digest>`**：image 內容指紋 `sha256:…`。

**`<verb>`**：動詞名。

**`<id>`**：一次執行的交易 id，進度檔與執行紀錄共用。
