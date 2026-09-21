# vendor_kit

下游 repo 把要交付的檔案打成純資料的容器 image；下游使用者用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。本檔只放名詞；決議在 `doc/adr/`，規格在 issue。

## 三方

**下游開發者（downstream developer）**：開發下游 repo 的人；被承諾方。
_Avoid_：工具方、上游、工具 repo 開發者、供應側

**下游使用者（downstream user）**：在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人；被承諾方。
_Avoid_：使用者、專案方、下游專案、專案維護者

**VK（vendor_kit）**：我們，vendor_kit 開發者；承諾方。
_Avoid_：vendor_kit 開發者（三方語境時）

**承諾方／被承諾方（promisor / promisee）**：VK 對兩個下游承諾「照契約用一定可以、不會隨便改」的關係；同一人可兼下游開發者與下游使用者兩種身分。

## VK 組件

VK 由三個組件組成；組件是對外可見的最大單位，模組是引擎內的程式單元（組件 > 模組）。

**引擎（engine）**：VK 的主程式，是容器 image `ghcr.io/<org>/vendor_kit:vN`；只透過掛入的 `/repo` 看專案根。

**薄殼（shell）**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔：`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`。

**啟動器（launcher）**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器。

**`bootstrap.sh`（bootstrap script）**：release 附的腳本，第一次接入時的啟動器。

**自描述首行（self-describing header）**：薄殼每檔首行 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`。

**救援路徑（rescue path）**：不依賴 `gen/` 的單段引擎呼叫（install、升引擎、sync 的不符提示、help）；任何 ≥ 最低介面版的薄殼永久可用。

**暫存目錄（scratch dir）**：專案內的 `.vendor_kit/.tmp.dist.<id>/`，啟動器展開下游 image 內容的落點；結束即刪。

### VK 模組

**版本解析（resolve）**：引擎內決定要拉哪些 image、寫哪些檔的模組。

**取件（fetch）**：引擎內把工具內容寫進 `cache/` 並驗指紋的模組。

**初始檔合併（initfile）**：引擎內建初始檔、存基準版、做三方合併的模組。

**薄殼產生（shell）**：引擎內產生薄殼五檔並比對薄殼是否被改的模組。

**進度與寫入（progress）**：引擎內管進度檔、鎖與原子替換的模組。
_Avoid_：交易、txn

**設定與格式（schema）**：引擎內讀寫 VK 檔 TOML 與檢查檔案版的模組。

**紀錄（log）**：引擎內寫執行紀錄的模組。

**清理（prune）**：引擎內找出並刪除版本鎖定行未引用的舊 image、殘留容器與暫存的模組。

## 專案裡的檔案

**專案根（project root）**：含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套。

**專案檔（project file）**：專案內不是 VK 自產的一切：根 `justfile`、根 `.dockerignore`、建立後的初始檔、其他原有檔。
_Avoid_：使用者的檔、使用者檔

**專案檔四原則（four rules for project files）**：VK 對專案檔的四條承諾：① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋。
_Avoid_：使用者檔四原則、不變量 I1

**VK 檔（VK file）**：VK 自己建、自己管的檔：`.vendor_kit/` 內的 `version.toml`、`config.toml`、薄殼、基準版、`cache/`、`gen/`、進度檔、執行紀錄；不受專案檔四原則。

**版本鎖定行（lock line）**：`.vendor_kit/version.toml` 內每個工具（與引擎）各一行 `<repo> = "…:<tag>@sha256:<digest>"`；進 git；唯一決定裝哪一版的地方，引擎只認 digest。
_Avoid_：鎖定行、正規行、`.version`

**`version.toml`（lock file）**：`.vendor_kit/version.toml`，放版本鎖定行的檔，專案的唯一版本來源；公開格式。
_Avoid_：`.version`

**`version.local.toml`（local override）**：與 `version.toml` 同格式、不進 git 的覆寫檔；dev 寫它把工具指向本機目錄或引擎指向本機 image。
_Avoid_：`.version.local`

**有效版本（effective version）**：`version.local.toml` 有同名那行就用它，否則用版本鎖定行。

**`config.toml`（config file）**：`.vendor_kit/config.toml`，VK 的設定檔，進 git；下游使用者可手改。

**`cache/`（cache）**：`.vendor_kit/cache/<repo>/`，工具內容的本機副本；不進 git、下游使用者不可改。
_Avoid_：`.<repo>/`

**`gen/`（generated）**：`.vendor_kit/gen/`，引擎產生、供 just 載入的檔（`.stamp`、`<repo>.stamp`、`tools.just`）；不進 git。

**印記（stamp）**：`gen/<repo>.stamp`，已裝版本的快取鍵：第一行是 digest，之後每檔一行指紋；不是信任來源。

**初始檔（init file）**：工具在 `dist/init.toml` 宣告、`add` 時複製（copy）或插入幾行（append）進專案的檔；建立後歸下游使用者、進 git。

**範本（template）**：下游 repo `dist/` 裡給初始檔用的樣板；只複製，不渲染。

**基準版（baseline）**：`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；三方合併的第三份。
_Avoid_：baseline（中文語境）、基準

**納管（managed）**：初始檔經下游使用者同意建立後，VK 記下它的來源與狀態；拒絕建立也記（拒絕過）。

**三方合併（three-way merge）**：升版時對每個納管初始檔拿基準版、現況、新版三份做的合併；衝突時檔內留 `<<<<<<< vendor_kit:baseline` 標記。
_Avoid_：diff 三方比對

**進度檔（progress file）**：可寫動詞的交易紀錄 `.vendor_kit/.tmp.<verb>.<id>.toml`（或記在基準版旁的 metadata）；成功即刪；中斷後恢復用。
_Avoid_：進度日誌、交易日誌、交易紀錄

**執行紀錄（run log）**：`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞每次執行一檔；不進 git。
_Avoid_：操作紀錄檔、操作紀錄、log 檔

**根 justfile 一行 import（root justfile import line）**：下游使用者的 `justfile` 內唯一與 VK 有關的一行 `import '.vendor_kit/entry.just'`。

**`just vendor_kit` 命名空間（namespace）**：VK 的動詞所在的 just 命名空間，不佔頂層；`just <ns> …` 是工具自己帶的，VK 不定義。

## 下游 repo 側

**下游 repo（downstream repo）**：提供工具的 git repo，`<repo>` 是它的名字。
_Avoid_：工具 repo

**`dist/`（dist）**：下游 repo 的出貨目錄：`files/`、`init.toml`、`just/<ns>.just`；其他內容不出貨。

**`init.toml`（init manifest）**：`dist/init.toml`，下游 repo 提供的初始檔清單：`[[file]]` 一項一個，`src`、`dest`、`strategy`（copy 或 append）。

**`Dockerfile.dist`（dist Dockerfile）**：下游 repo 出貨用的食譜，逐字三行：`FROM scratch`、`LABEL`、`COPY dist/ /dist/`。

**下游 image（downstream image）**：`ghcr.io/<org>/<repo>-dist:<tag>`；`FROM scratch` 只放檔案，沒有程式、不會被執行；多架構 amd64 + arm64；VK 只搬移，不承諾內容可執行。
_Avoid_：工具 image

**兩棵樹比對（two-tree compare）**：取件的驗法：展開的 `/dist` 與 `cache/<repo>/` 逐檔比檔案集合、sha256、執行位。

**GHCR（GitHub Container Registry）**：下游 image 與引擎放的地方；已釋出的版本永不刪。

**甲版／乙版（variant A / variant B）**：甲版 = 下游 image `FROM vendor_kit`，每個下游 image 內都包引擎（已放棄）；乙版（現行）= 下游 image `FROM scratch` 只放檔案，引擎只有一份。

## 動詞

**動詞（verb）**：`just vendor_kit <動詞>` 的動詞；小寫原文書寫；共 11 個。

**`install`**：第一次接入的動詞；再跑 = 冪等修復。
_Avoid_：`--repair`、bootstrap 子命令

**`uninstall`**：對稱移除 VK 自產檔的動詞；初始檔與執行紀錄不刪。
_Avoid_：`--purge`

**`add <repo>[@<tag>]`**：接入一個工具的動詞；最後才寫版本鎖定行。
_Avoid_：init、在 `.version` 手動加一行

**`remove <repo>`**：移除一個工具的動詞；初始檔不刪。

**`update [<repo>]`**：只查有沒有新版、不寫任何檔的動詞。

**`upgrade [<repo>[@<tag>]]`**：升到最新（或指定）版的動詞；初始檔三方合併。
_Avoid_：diff、accept、`--to <tag>`

**`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`**：把工具指到本機目錄（或引擎指到本機 image）的動詞；只寫 `version.local.toml`。
_Avoid_：dev 模式（指狀態時寫「dev 覆寫中」）

**`undev <repo>`／`undev vendor_kit`**：撤銷 dev 的動詞。
_Avoid_：`dev <repo>` 不帶 `-p`

**`sync [<repo>]`**：依版本鎖定行重建本機副本的動詞；不改任何進 git 的檔。
_Avoid_：ensure

**`prune`**：刪版本鎖定行未引用的舊 image、殘留容器／network／volume 與暫存的動詞。

**`help`**：印命名空間層說明的動詞；不觸網、不寫檔（執行紀錄除外）。

**升引擎（engine upgrade）**：`upgrade vendor_kit[@<tag>]`，換引擎並重產薄殼的動詞。
_Avoid_：自身升級、vendor_kit 自我更新

## 執行結果

**結束碼（exit code）**：`0` 成功（含 warn）；`1` 一般失敗或需人處理；`2` 合併衝突；`3` 介面版／檔案版不合。
_Avoid_：結束狀態、退出碼

**需人處理（needs human）**：動詞停下並印出下一步指令的結束；結束碼 1 或 3 且附指令，衝突 2 亦同。

**失敗（failure）**：拉不到、寫不進、驗證不過這類無法繼續的結束；結束碼 1。

**CI 模式（CI mode）**：環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版。
_Avoid_：frozen

## 相容性

**介面版（protocol version）**：薄殼與引擎之間的整數版號 `P`；與 release 版號無關。
_Avoid_：協定版、協定號、protocol P

**檔案版（schema version）**：VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔。
_Avoid_：格式版、schema 號

**最低介面版（floor）**：引擎仍支援的最低介面版；固定常數；只能經 ADR 提高。
_Avoid_：floor（中文語境）

**對外契約（public contract）**：VK 承諾「這樣用一定可以、不會隨便改」的介面清單；只對下游開發者與下游使用者承諾。

## 自動化角色

**下游 CI（downstream CI）**：下游使用者專案自己的 CI 平台；只呼叫契約檢查腳本；不是「方」。

**契約檢查腳本（check script）**：`.vendor_kit/ci/check.sh`，薄殼之一；自設 `CI=1` 進 CI 模式；`--dist` 給下游 repo 驗 `dist/` 佈局。

**Renovate（Renovate）**：下游使用者自選的版本更新機器人，用 VK 提供的設定；PR 只改版本鎖定行。VK 本身沒有機器人。

## VK 自己的 repo

**測試分層（test layers）**：VK repo 的 Dockerfile stage 與強制閘門：環境檢查 → lint／unit → integration → release → system → acceptance。

**鏡射／黑箱（mirror check / blackbox check）**：lint 層的兩個自寫檢查：每個引擎模組必有對應測試檔；system、acceptance 測試不准 import 引擎程式碼。

## 佔位符

**`<repo>`**：下游 repo 名。
_Avoid_：`<name>`

**`<ns>`**：工具的 just 命名空間；一個工具可有多個。

**`<tag>`**：image 版本名。

**`<digest>`**：image 內容指紋 `sha256:…`。

**`<verb>`**：動詞名。

**`<id>`**：一次執行的交易 id，進度檔與執行紀錄共用。
