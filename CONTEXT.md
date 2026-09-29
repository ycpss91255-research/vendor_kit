# vendor_kit

vendor_kit（VK）把工具從一個 repo 送進其他 repo：出貨端把工具打包成容器 image，導入端用一行版本鎖定行決定裝哪一版。這裡只定義這件事用到的專有名詞，一般技術詞不收。

對外承諾見[目的與承諾](doc/decisions/review/01_purpose.md)，不變量見[不變量](doc/decisions/review/02_invariants.md)，難逆轉的取捨見 [ADR](doc/adr/)。

## 目錄

**角色與情境**

- [VK（vendor_kit）](#term-vk)
- [使用者（user）](#term-user)
- [導入（consume）](#term-consume)
- [出貨（ship）](#term-ship)

**VK 組件**

- [引擎（engine）](#term-engine)
- [薄殼（shell）](#term-shell)
- [啟動器（launcher）](#term-launcher)

**工具與出貨**

- [repo](#term-repo)
- [`<repo>`（repository name）](#term-repo-name)
- [工具（tool）](#term-tool)
- [安裝目錄（install directory）](#term-install-directory)
- [`<ns>` 命名空間（namespace）](#term-namespace)
- [工具 recipe（tool recipe）](#term-tool-recipe)
- [`dist/`](#term-dist)
- [工具內容（tool content）](#term-tool-content)
- [取件（fetch）](#term-fetch)
- [工具 image（tool image）](#term-tool-image)
- [引擎 image（engine image）](#term-engine-image)
- [registry](#term-registry)
- [image 引用（image reference）](#term-image-reference)
- [tag](#term-tag)
- [digest](#term-digest)

**repo 內的檔與狀態**

- [`.vendor_kit/`](#term-vendor-kit-dir)
- [`version.toml`](#term-version-toml)
- [repo 檔（repo file）](#term-repo-file)
- [VK 檔（VK file）](#term-vk-file)
- [進 git 的檔（tracked file）](#term-tracked-file)
- [`cache/`](#term-cache)
- [`gen/`](#term-gen)
- [印記（stamp）](#term-stamp)
- [逐檔指紋（per-file digest）](#term-per-file-digest)
- [自描述標頭（self-describing header）](#term-self-describing-header)
- [CI 檢查腳本（CI check script）](#term-ci-check-script)
- [執行紀錄（run log）](#term-run-log)
- [進度檔（progress file）](#term-progress-file)

**版本與來源**

- [版本鎖定行（lock version line）](#term-lock-version-line)
- [鎖定版本（locked version）](#term-locked-version)
- [本機覆寫（local override）](#term-local-override)
- [本機開發來源（local source）](#term-local-source)

**初始檔與合併**

- [初始檔（init file）](#term-init-file)
- [納管（managed）](#term-managed)
- [metadata](#term-metadata)
- [基準版（baseline）](#term-baseline)
- [基準版合併（baseline merge）](#term-baseline-merge)
- [合併衝突（merge conflict）](#term-merge-conflict)

**執行與結果**

- [VK recipe](#term-vk-recipe)
- [可寫 recipe（writing recipe）](#term-writing-recipe)
- [唯讀 recipe（read-only recipe）](#term-read-only-recipe)
- [詢問（prompt）](#term-prompt)
- [選項（option）](#term-option)
- [`-y`（yes option）](#term-yes-option)
- [CI 模式（CI mode）](#term-ci-mode)
- [需人處理（needs human）](#term-needs-human)
- [失敗（failure）](#term-failure)
- [警告（warning）](#term-warning)
- [結束碼（exit code）](#term-exit-code)

**VK recipe 與用途**

- [`add` / `remove`](#term-recipe-add-remove)
- [`update`、`upgrade`](#term-recipe-update-upgrade)
- [`dev` / `undev`](#term-recipe-dev-undev)
- [`sync`](#term-recipe-sync)
- [`prune`](#term-recipe-prune)
- [`install` / `uninstall`](#term-recipe-install-uninstall)

**介面版與契約**

- [介面版（interface version）](#term-interface-version)
- [最低介面版（floor）](#term-floor)
- [檔案版（schema version）](#term-schema-version)
- [救援路徑（rescue path）](#term-rescue-path)
- [契約（contract）](#term-contract)

## Language

### 角色與情境

<a id="term-vk"></a>
**VK**（vendor_kit）：
vendor_kit 的簡稱；在承諾關係裡指提出承諾的一方，即引擎與薄殼的維護者。

<a id="term-user"></a>
**使用者**（user）：
用 VK 管理工具的人，也就是被承諾的一方。
_Avoid_: 下游使用者、下游開發者、工具 repo 開發者、專案維護者

<a id="term-consume"></a>
**導入**（consume）：
使用者把別人做好的工具帶進自己的 repo 並交給 VK 管的那個情境。
_Avoid_: 接入

<a id="term-ship"></a>
**出貨**（ship）：
使用者把自己做的工具打包出去、給別的 repo 導入的那個情境。

### VK 組件

<a id="term-engine"></a>
**引擎**（engine）：
執行 VK recipe 的主程式，以容器 image 發布。

<a id="term-shell"></a>
**薄殼**（shell）：
`.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。

<a id="term-launcher"></a>
**啟動器**（launcher）：
從主機啟動引擎的入口；薄殼內的 POSIX sh 片段與首次導入用的 `bootstrap.sh` 都是啟動器。

### 工具與出貨

<a id="term-repo"></a>
**repo**：
使用者的 git repo；一個 repo 可以有多個安裝目錄。
_Avoid_: 專案、下游 repo

<a id="term-repo-name"></a>
**`<repo>`**（repository name）：
出貨的那個 repo 的名字，也是工具名。
_Avoid_: `<name>`

<a id="term-tool"></a>
**工具**（tool）：
repo 出貨、供另一個（或同一個）repo 導入的內容單位，名字是 `<repo>`。

<a id="term-install-directory"></a>
**安裝目錄**（install directory）：
`.vendor_kit/` 的直接父目錄，也是 VK 的安裝單位。
_Avoid_: 專案根、導入根

<a id="term-namespace"></a>
**`<ns>` 命名空間**（namespace）：
工具在 just 中提供工具 recipe 的命名空間。

<a id="term-tool-recipe"></a>
**工具 recipe**（tool recipe）：
工具自己提供、使用者以 `just <ns> …` 執行的 recipe，相對於 VK recipe。

<a id="term-dist"></a>
**`dist/`**：
repo 交付給 VK 的工具出貨目錄。

<a id="term-tool-content"></a>
**工具內容**（tool content）：
工具在 `dist/` 交付、展開後放進 `cache/` 的那些檔。

<a id="term-fetch"></a>
**取件**（fetch）：
把工具內容從工具 image 取出、寫進 `cache/` 的動作。

<a id="term-tool-image"></a>
**工具 image**（tool image）：
封裝單一工具出貨內容的純資料容器 image；VK 不把它當程式執行。
_Avoid_: 下游 image

<a id="term-engine-image"></a>
**引擎 image**（engine image）：
裝載 VK 引擎的容器 image。

<a id="term-registry"></a>
**registry**：
存放並提供工具 image 與引擎 image 的服務。

<a id="term-image-reference"></a>
**image 引用**（image reference）：
唯一指定某個 image 版本與內容的字串 `<registry>/<路徑>:<tag>@sha256:<digest>`；`<registry>` 是存放它的 registry 主機，`<路徑>` 是 image 在那個 registry 裡的路徑。tag 與 digest 一起寫，所以同一行同時說得出版本與內容。

<a id="term-tag"></a>
**tag**：
image 引用裡給人與外部版本追蹤工具看的版本標籤；它可以被重新指到別的內容，所以不鎖內容。

<a id="term-digest"></a>
**digest**：
image 引用裡那個 image 內容的 sha256；內容相同才會相同，所以它鎖的是內容，不是版本。

### repo 內的檔與狀態

<a id="term-vendor-kit-dir"></a>
**`.vendor_kit/`**：
VK 在 repo 內建立與管理的目錄，放薄殼、版本鎖定行、本機狀態與快取。

<a id="term-version-toml"></a>
**`version.toml`**：
`.vendor_kit/version.toml`，放全部版本鎖定行的檔；進 git。
_Avoid_: `.version`

<a id="term-repo-file"></a>
**repo 檔**（repo file）：
位於 repo 內、由使用者擁有及維護，且不屬於 `.vendor_kit/` 的檔。
_Avoid_: 專案檔

<a id="term-vk-file"></a>
**VK 檔**（VK file）：
由 VK 建立及管理、位於 `.vendor_kit/` 的檔。

<a id="term-tracked-file"></a>
**進 git 的檔**（tracked file）：
隨 repo 一起 commit 進 git 的檔。
_Avoid_: tracked 檔、版控檔

<a id="term-cache"></a>
**`cache/`**：
VK 在 repo 本機保存已展開工具內容的目錄。
_Avoid_: `.<repo>/`

<a id="term-gen"></a>
**`gen/`**：
VK 在 repo 本機的目錄，放 VK 產生、供 just 載入的檔；不進 git。

<a id="term-stamp"></a>
**印記**（stamp）：
記錄本機工具內容對應的版本與內容指紋的 VK 檔。
_Avoid_: 簽章、信任來源

<a id="term-per-file-digest"></a>
**逐檔指紋**（per-file digest）：
`cache/` 內每個檔的 sha256，記在印記裡。

<a id="term-self-describing-header"></a>
**自描述標頭**（self-describing header）：
薄殼檔開頭描述它自己的介面版、引擎版與其餘內容指紋的那段。

<a id="term-ci-check-script"></a>
**CI 檢查腳本**（CI check script）：
薄殼之一 `.vendor_kit/ci/check.sh`，給使用者接進自己 CI 用。

<a id="term-run-log"></a>
**執行紀錄**（run log）：
記錄一次 VK 執行以供事後追溯的 VK 檔。

<a id="term-progress-file"></a>
**進度檔**（progress file）：
記錄可寫 recipe 未完成狀態的 VK 檔。

### 版本與來源

<a id="term-lock-version-line"></a>
**版本鎖定行**（lock version line）：
`version.toml` 裡把一個引擎或工具對應到一個鎖定版本的 TOML 項目。

<a id="term-locked-version"></a>
**鎖定版本**（locked version）：
image 引用指定的那個版本與內容；沒有本機覆寫時，導入的就是它。

<a id="term-local-override"></a>
**本機覆寫**（local override）：
讓引擎或工具暫時改用本機開發來源的 VK 項目，優先於版本鎖定行。

<a id="term-local-source"></a>
**本機開發來源**（local source）：
本機覆寫指到的來源：工具是一個本機目錄，引擎是一個本機 image；不進 git。

### 初始檔與合併

<a id="term-init-file"></a>
**初始檔**（init file）：
由工具提供、VK 導入 repo 後交由使用者維護的 repo 檔。

<a id="term-managed"></a>
**納管**（managed）：
VK 已記錄某個初始檔的來源、並會在後續升級中處理它的狀態。

<a id="term-metadata"></a>
**metadata**：
記錄初始檔來源與 VK 納管狀態的 VK 檔。

<a id="term-baseline"></a>
**基準版**（baseline）：
上次套用的初始檔原版副本，也就是合併時的共同祖先。

<a id="term-baseline-merge"></a>
**基準版合併**（baseline merge）：
以基準版、目前 repo 檔與新版初始檔為輸入所做的合併。
_Avoid_: 三方合併

<a id="term-merge-conflict"></a>
**合併衝突**（merge conflict）：
基準版合併無法自動決定合併內容的結果。

### 執行與結果

<a id="term-vk-recipe"></a>
**VK recipe**：
VK 自己的指令，寫法 `just vendor_kit <recipe>`。
_Avoid_: 動詞、子命令

<a id="term-writing-recipe"></a>
**可寫 recipe**（writing recipe）：
會動到進 git 的檔或進度檔的 VK recipe。

<a id="term-read-only-recipe"></a>
**唯讀 recipe**（read-only recipe）：
不動進 git 的檔、也不動進度檔的 VK recipe。

<a id="term-prompt"></a>
**詢問**（prompt）：
VK 在修改 repo 檔前，向使用者取得同意的互動。

<a id="term-option"></a>
**選項**（option）：
recipe 後面帶的 `-x` 或 `--long` 參數。

<a id="term-yes-option"></a>
**`-y`**（yes option）：
讓使用者預先回答詢問的選項。

<a id="term-ci-mode"></a>
**CI 模式**（CI mode）：
VK 在 CI 環境中執行時採用的模式。

<a id="term-needs-human"></a>
**需人處理**（needs human）：
VK 停下並要求使用者採取下一步的結果。

<a id="term-failure"></a>
**失敗**（failure）：
VK 因無法繼續而結束的結果。

<a id="term-warning"></a>
**警告**（warning）：
指出非阻斷問題的訊息；它不會讓該次執行變成失敗或需人處理。

<a id="term-exit-code"></a>
**結束碼**（exit code）：
VK recipe 結束時回給呼叫方的整數。

### VK recipe 與用途

<a id="term-recipe-add-remove"></a>
**`add` / `remove`**：
`add` 把一個工具納入這個安裝目錄；`remove` 是它的反向，把那個工具解除。

<a id="term-recipe-update-upgrade"></a>
**`update`、`upgrade`**：
`update` 只查有沒有新版；`upgrade` 把鎖定版本換成新版或指定版本。

<a id="term-recipe-dev-undev"></a>
**`dev` / `undev`**：
`dev` 讓引擎或工具改用本機開發來源；`undev` 是它的反向，回到鎖定版本。

<a id="term-recipe-sync"></a>
**`sync`**：
讓本機的工具內容與版本鎖定行或本機覆寫一致。

<a id="term-recipe-prune"></a>
**`prune`**：
清掉 VK 產生、但目前 repo 已不再使用的本機資源。

<a id="term-recipe-install-uninstall"></a>
**`install` / `uninstall`**：
`install` 把 VK 裝進 repo 的一個目錄，使它成為安裝目錄；`uninstall` 是它的反向，把 VK 從那裡移除。

### 介面版與契約

<a id="term-interface-version"></a>
**介面版**（interface version）：
薄殼與引擎之間公開介面的整數版號。

<a id="term-floor"></a>
**最低介面版**（floor）：
引擎仍支援的最低介面版。

<a id="term-schema-version"></a>
**檔案版**（schema version）：
VK 寫入檔案時用來標示該檔資料格式的整數版號。

<a id="term-rescue-path"></a>
**救援路徑**（rescue path）：
不論薄殼、VK 檔與引擎的版本組合是否相符，都必須能用的呼叫，只有這些：`install`、`upgrade --engine`、`sync` 的版本不符判定，以及四種印用法呼叫：`just vendor_kit`（不帶指令）、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項 `--help` 同）。其他 recipe 的 `-h`／`--help` 不屬救援路徑。

<a id="term-contract"></a>
**契約**（contract）：
VK 對使用者承諾不會隨意改變的那組介面；引擎內部實作不屬契約。
