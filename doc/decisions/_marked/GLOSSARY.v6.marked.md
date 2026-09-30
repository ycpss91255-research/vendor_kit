<!-- 標示版 v6：綠底 <mark> 是新增、紅底 <mark> 是刪除；底線 <ins> 是名詞標記；本檔只供本地 review，不進 git；基準 base_316a354。正式內容看 /GLOSSARY.md -->

# vendor_kit

<mark style="background-color:#f8c8c8">vendor_kit（VK）把工具從一個 repo 送進其他 repo：出貨端把工具打包成容器 image，導入端用一行版本鎖定行決定裝哪一版。這裡只定義這件事用到的專有名詞，一般技術詞不收。</mark>
<mark style="background-color:#c8f0c8">vendor_kit (VK) 把工具從一個 repo 送進其他 repo：出貨端把工具打包成容器 image，導入端用一行版本鎖定行決定裝哪一版。這裡只定義這件事用到的專有名詞，一般技術詞不收。</mark>

對外承諾見[目的與承諾](../../contract/01_purpose.md)，不變量見[不變量](../../contract/02_invariants.md)，難逆轉的取捨見 [ADR](../../adr/)。

## Language

### 角色與情境

<mark style="background-color:#f8c8c8">**VK**（vendor_kit）：</mark>
<mark style="background-color:#c8f0c8">**VK** (vendor_kit)：</mark>
vendor_kit 的簡稱；在承諾關係裡指提出承諾的一方，即引擎與薄殼的維護者。

<mark style="background-color:#f8c8c8">**使用者**（user）：</mark>
<mark style="background-color:#c8f0c8">**使用者** (user)：</mark>
用 VK 管理工具的人，也就是被承諾的一方。
_Avoid_: 下游使用者、下游開發者、工具 repo 開發者、專案維護者

<mark style="background-color:#f8c8c8">**導入**（consume）：</mark>
<mark style="background-color:#c8f0c8">**導入** (consume)：</mark>
使用者把別人做好的工具帶進自己的 repo 並交給 VK 管的那個情境。
_Avoid_: 接入

<mark style="background-color:#f8c8c8">**出貨**（ship）：</mark>
<mark style="background-color:#c8f0c8">**出貨** (ship)：</mark>
使用者把自己做的工具打包出去、給別的 repo 導入的那個情境。

### VK 組件

<mark style="background-color:#f8c8c8">**引擎**（engine）：</mark>
<mark style="background-color:#c8f0c8">**引擎** (engine)：</mark>
執行 VK recipe 的主程式，以容器 image 發布。

<mark style="background-color:#f8c8c8">**薄殼**（shell）：</mark>
<mark style="background-color:#c8f0c8">**薄殼** (shell)：</mark>
`.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。

<mark style="background-color:#f8c8c8">**啟動器**（launcher）：</mark>
<mark style="background-color:#c8f0c8">**啟動器** (launcher)：</mark>
從主機啟動引擎的入口；薄殼內的 POSIX sh 片段與首次導入用的 `bootstrap.sh` 都是啟動器。

### 工具與出貨

**repo**：
使用者的 git repo；一個 repo 可以有多個安裝目錄。
_Avoid_: 專案、下游 repo

<mark style="background-color:#f8c8c8">**`<repo>`**（repository name）：</mark>
<mark style="background-color:#c8f0c8">**`<repo>`** (repository name)：</mark>
出貨的那個 repo 的名字，也是工具名。
_Avoid_: `<name>`

<mark style="background-color:#f8c8c8">**工具**（tool）：</mark>
<mark style="background-color:#c8f0c8">**工具** (tool)：</mark>
repo 出貨、供另一個（或同一個）repo 導入的內容單位，名字是 `<repo>`。

<mark style="background-color:#f8c8c8">**安裝目錄**（install directory）：</mark>
<mark style="background-color:#c8f0c8">**安裝目錄** (install directory)：</mark>
`.vendor_kit/` 的直接父目錄，也是 VK 的安裝單位。
_Avoid_: 專案根、導入根

<mark style="background-color:#f8c8c8">**`<ns>` 命名空間**（namespace）：</mark>
<mark style="background-color:#c8f0c8">**`<ns>` 命名空間** (namespace)：</mark>
工具在 just 中提供工具 recipe 的命名空間。

<mark style="background-color:#f8c8c8">**工具 recipe**（tool recipe）：</mark>
<mark style="background-color:#c8f0c8">**工具 recipe** (tool recipe)：</mark>
工具自己提供、使用者以 `just <ns> …` 執行的 recipe，相對於 VK recipe。

**`dist/`**：
repo 交付給 VK 的工具出貨目錄。

<mark style="background-color:#f8c8c8">**工具內容**（tool content）：</mark>
<mark style="background-color:#c8f0c8">**工具內容** (tool content)：</mark>
工具在 `dist/` 交付、展開後放進 `cache/` 的那些檔。

<mark style="background-color:#f8c8c8">**取件**（fetch）：</mark>
<mark style="background-color:#c8f0c8">**取件** (fetch)：</mark>
把工具內容從工具 image 取出、寫進 `cache/` 的動作。

<mark style="background-color:#f8c8c8">**工具 image**（tool image）：</mark>
<mark style="background-color:#c8f0c8">**工具 image** (tool image)：</mark>
封裝單一工具出貨內容的純資料容器 image；VK 不把它當程式執行。
_Avoid_: 下游 image

<mark style="background-color:#f8c8c8">**引擎 image**（engine image）：</mark>
<mark style="background-color:#c8f0c8">**引擎 image** (engine image)：</mark>
裝載 VK 引擎的容器 image。

**registry**：
存放並提供工具 image 與引擎 image 的服務。

<mark style="background-color:#f8c8c8">**image 引用**（image reference）：</mark>
<mark style="background-color:#c8f0c8">**image 引用** (image reference)：</mark>
唯一指定某個 image 版本與內容的字串 `<registry>/<路徑>:<tag>@sha256:<digest>`；`<registry>` 是存放它的 registry 主機，`<路徑>` 是 image 在那個 registry 裡的路徑。tag 與 digest 一起寫，所以同一行同時說得出版本與內容。

**tag**：
image 引用裡給人與外部版本追蹤工具看的版本標籤；它可以被重新指到別的內容，所以不鎖內容。
工具與引擎的 tag 只接受 `vX.Y.Z`（不帶 pre-release、build 後綴，不收前導零）；最新版是把 X、Y、Z 當非負整數逐欄比數值取最大的那個，不看字串順序、registry 回傳順序或推送時間；同一個 tag 改指到別的 digest 不算新版。寫出格式不合的 tag 是用法錯誤，以結束碼 `2` 結束。

**digest**：
image 引用裡那個 image 內容的 sha256；內容相同才會相同，所以它鎖的是內容，不是版本。

### repo 內的檔與狀態

**`.vendor_kit/`**：
VK 在 repo 內建立與管理的目錄，放薄殼、版本鎖定行、本機狀態與快取。

**`version.toml`**：
`.vendor_kit/version.toml`，放全部版本鎖定行的檔；進 git。
_Avoid_: `.version`

<mark style="background-color:#f8c8c8">**repo 檔**（repo file）：</mark>
<mark style="background-color:#c8f0c8">**repo 檔** (repo file)：</mark>
位於 repo 內、由使用者擁有及維護，且不屬於 `.vendor_kit/` 的檔。
_Avoid_: 專案檔

<mark style="background-color:#f8c8c8">**VK 檔**（VK file）：</mark>
<mark style="background-color:#c8f0c8">**VK 檔** (VK file)：</mark>
由 VK 建立及管理、位於 `.vendor_kit/` 的檔。

<mark style="background-color:#f8c8c8">**進 git 的檔**（tracked file）：</mark>
<mark style="background-color:#c8f0c8">**進 git 的檔** (tracked file)：</mark>
隨 repo 一起 commit 進 git 的檔。
_Avoid_: tracked 檔、版控檔

**`cache/`**：
VK 在 repo 本機保存已展開工具內容的目錄。
_Avoid_: `.<repo>/`

**`gen/`**：
VK 在 repo 本機的目錄，放 VK 產生、供 just 載入的檔；不進 git。

<mark style="background-color:#f8c8c8">**印記**（stamp）：</mark>
<mark style="background-color:#c8f0c8">**印記** (stamp)：</mark>
記錄本機工具內容對應的版本與內容指紋的 VK 檔。
_Avoid_: 簽章、信任來源

<mark style="background-color:#f8c8c8">**逐檔指紋**（per-file digest）：</mark>
<mark style="background-color:#c8f0c8">**逐檔指紋** (per-file digest)：</mark>
`cache/` 內每個檔的 sha256，記在印記裡。

<mark style="background-color:#f8c8c8">**自描述標頭**（self-describing header）：</mark>
<mark style="background-color:#c8f0c8">**自描述標頭** (self-describing header)：</mark>
薄殼檔開頭描述它自己的介面版、引擎版與其餘內容指紋的那段。

<mark style="background-color:#f8c8c8">**CI 檢查腳本**（CI check script）：</mark>
<mark style="background-color:#f8c8c8">薄殼之一 `.vendor_kit/ci/check.sh`，給使用者接進自己 CI 用。</mark>
<mark style="background-color:#c8f0c8">**`test`**：</mark>
<mark style="background-color:#c8f0c8">跑全部檢查的 VK recipe，本機與 CI 用同一個；`test dist` 只檢查工具在 `dist/` 交付的內容，給出貨的 repo 接進自己的 CI 用。</mark>
<mark style="background-color:#c8f0c8">寫法：`just vendor_kit test`；只檢查交付內容寫 `just vendor_kit test dist`。</mark>

<mark style="background-color:#f8c8c8">**執行紀錄**（run log）：</mark>
<mark style="background-color:#c8f0c8">**執行紀錄** (run log)：</mark>
記錄一次 VK 執行以供事後追溯的 VK 檔。

<mark style="background-color:#f8c8c8">**進度檔**（progress file）：</mark>
<mark style="background-color:#c8f0c8">**進度檔** (progress file)：</mark>
記錄可寫 recipe 未完成狀態的 VK 檔。

### 版本與來源

<mark style="background-color:#f8c8c8">**版本鎖定行**（lock version line）：</mark>
<mark style="background-color:#c8f0c8">**版本鎖定行** (lock version line)：</mark>
`version.toml` 裡把一個引擎或工具對應到一個鎖定版本的 TOML 項目。

<mark style="background-color:#f8c8c8">**鎖定版本**（locked version）：</mark>
<mark style="background-color:#c8f0c8">**鎖定版本** (locked version)：</mark>
image 引用指定的那個版本與內容；沒有本機覆寫時，導入的就是它。

<mark style="background-color:#f8c8c8">**本機覆寫**（local override）：</mark>
<mark style="background-color:#c8f0c8">**本機覆寫** (local override)：</mark>
讓引擎或工具暫時改用本機開發來源的 VK 項目，優先於版本鎖定行。

<mark style="background-color:#f8c8c8">**本機開發來源**（local source）：</mark>
<mark style="background-color:#c8f0c8">**本機開發來源** (local source)：</mark>
本機覆寫指到的來源：工具是一個本機目錄，引擎是一個本機 image；不進 git。

### 初始檔與合併

<mark style="background-color:#f8c8c8">**初始檔**（init file）：</mark>
<mark style="background-color:#c8f0c8">**初始檔** (init file)：</mark>
由工具提供、VK 導入 repo 後交由使用者維護的 repo 檔。

<mark style="background-color:#f8c8c8">**納管**（managed）：</mark>
<mark style="background-color:#c8f0c8">**納管** (managed)：</mark>
VK 已記錄某個初始檔的來源、並會在後續升級中處理它的狀態。

**metadata**：
記錄初始檔來源與 VK 納管狀態的 VK 檔。

<mark style="background-color:#f8c8c8">**基準版**（baseline）：</mark>
<mark style="background-color:#c8f0c8">**基準版** (baseline)：</mark>
上次套用的初始檔原版副本，也就是合併時的共同祖先。

<mark style="background-color:#f8c8c8">**基準版合併**（baseline merge）：</mark>
<mark style="background-color:#c8f0c8">**基準版合併** (baseline merge)：</mark>
以基準版、目前 repo 檔與新版初始檔為輸入所做的合併。
_Avoid_: 三方合併

<mark style="background-color:#f8c8c8">**合併衝突**（merge conflict）：</mark>
<mark style="background-color:#c8f0c8">**合併衝突** (merge conflict)：</mark>
基準版合併無法自動決定合併內容的結果。

### 執行與結果

**VK recipe**：
VK 自己的指令，寫法 `just vendor_kit <recipe>`。
_Avoid_: 動詞、子命令

<mark style="background-color:#f8c8c8">**可寫 recipe**（writing recipe）：</mark>
<mark style="background-color:#c8f0c8">**可寫 recipe** (writing recipe)：</mark>
會動到進 git 的檔或進度檔的 VK recipe。

<mark style="background-color:#f8c8c8">**唯讀 recipe**（read-only recipe）：</mark>
<mark style="background-color:#c8f0c8">**唯讀 recipe** (read-only recipe)：</mark>
不動進 git 的檔、也不動進度檔的 VK recipe。

<mark style="background-color:#f8c8c8">**詢問**（prompt）：</mark>
<mark style="background-color:#c8f0c8">**詢問** (prompt)：</mark>
VK 在修改 repo 檔前，向使用者取得同意的互動。

<mark style="background-color:#f8c8c8">**選項**（option）：</mark>
<mark style="background-color:#c8f0c8">**選項** (option)：</mark>
recipe 後面帶的 `-x` 或 `--long` 參數。

<mark style="background-color:#f8c8c8">**`-y`**（yes option）：</mark>
<mark style="background-color:#c8f0c8">**`-y`** (yes option)：</mark>
讓使用者預先回答詢問的選項。
寫法：`-y`，長選項 `--yes`。

<mark style="background-color:#f8c8c8">**CI 模式**（CI mode）：</mark>
<mark style="background-color:#c8f0c8">**CI 模式** (CI mode)：</mark>
VK 在 CI 環境中執行時採用的模式。

<mark style="background-color:#f8c8c8">**需人處理**（needs human）：</mark>
<mark style="background-color:#f8c8c8">VK 停下並要求使用者採取下一步的結果。</mark>
<mark style="background-color:#c8f0c8">**診斷** (diagnostic)：</mark>
<mark style="background-color:#c8f0c8">VK 印到 stderr、第一行為 `vendor_kit: <level>[VKnnnn]: <中文本文>` 的訊息，含續行。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。</mark>

<mark style="background-color:#f8c8c8">**失敗**（failure）：</mark>
<mark style="background-color:#f8c8c8">VK 因無法繼續而結束的結果。</mark>
<mark style="background-color:#c8f0c8">**正常輸出** (normal output)：</mark>
<mark style="background-color:#c8f0c8">成功時印到 stdout、不加前綴的輸出，例如改了什麼、查詢結果、`-h`／`--help` 的用法。</mark>

<mark style="background-color:#f8c8c8">**警告**（warning）：</mark>
<mark style="background-color:#f8c8c8">指出非阻斷問題的訊息；不會讓這次執行變成失敗或需人處理。</mark>
<mark style="background-color:#c8f0c8">**需人處理** (needs human)：</mark>
<mark style="background-color:#c8f0c8">診斷的處置屬性，表示這次執行沒有做完，而且 VK 知道使用者接下來要做什麼；必須附上可直接複製的下一步指令。</mark>

<mark style="background-color:#f8c8c8">**結束碼**（exit code）：</mark>
<mark style="background-color:#f8c8c8">VK recipe 結束時回給呼叫方的整數。</mark>
<mark style="background-color:#c8f0c8">**失敗** (failure)：</mark>
<mark style="background-color:#c8f0c8">診斷的處置屬性，表示這次執行沒有做完；不承諾可執行的修法，但可以附一般建議。</mark>

<mark style="background-color:#c8f0c8">**警告** (warning)：</mark>
<mark style="background-color:#c8f0c8">level 為 `warn`、指出可能有問題、需要人確認的診斷；只要印出警告就不算成功，以結束碼 `1` 結束。要人接手的事項（例如合併衝突、查到新版）也用 warn level 印、同樣回 `1`，但不算警告。</mark>

<mark style="background-color:#c8f0c8">**原因代碼** (reason code)：</mark>
<mark style="background-color:#c8f0c8">每條診斷的固定識別碼，寫成 `VK` 加四位數字 (`VKnnnn`)；代碼發出後永不改給其他原因，刪除診斷時留下空號、不重用。</mark>

<mark style="background-color:#c8f0c8">**結束碼** (exit code)：</mark>
<mark style="background-color:#c8f0c8">VK recipe 結束時回給呼叫方的整數，由診斷的 level 決定，與處置無關：`0` (info) 只表示成功，沒有任何警告或要人接手的事項；`1` (warn) 表示有警告，或做完但要人接手；`2` (error) 表示沒做完，包括用法錯誤，以及處置為需人處理或失敗的 error 診斷；`3` (fatal) 只表示版本組合不合，這類診斷也可能是需人處理。有診斷時取最高 level 對應的碼，沒有診斷為 `0`；一次處理多個工具時同樣取最高的碼。</mark>

### VK recipe 與用途

**`add` / `remove`**：
`add` 把一個工具納入這個安裝目錄；`remove` 是它的反向，把那個工具解除。
寫法：`just vendor_kit add <repo>`，指定版本寫 `just vendor_kit add <repo>@<tag>`；`just vendor_kit remove <repo>`。

**`update`、`upgrade`**：
`update` 只查有沒有新版；`upgrade` 把鎖定版本換成新版或指定版本。
寫法：`just vendor_kit update`；工具用 `just vendor_kit upgrade <repo>`，指定版本寫 `just vendor_kit upgrade <repo>@<tag>`；引擎用 `just vendor_kit upgrade --engine`，指定版本寫 `just vendor_kit upgrade --engine=<tag>`。

**`dev` / `undev`**：
`dev` 讓引擎或工具改用本機開發來源；`undev` 是它的反向，回到鎖定版本。

**`sync`**：
讓本機的工具內容與版本鎖定行或本機覆寫一致。

**`prune`**：
清掉 VK 產生、但目前 repo 已不再使用的本機資源。

**`install` / `uninstall`**：
`install` 把 VK 裝進 repo 的一個目錄，讓它成為安裝目錄；`uninstall` 是它的反向，把 VK 從那裡移除。

### 介面版與契約

<mark style="background-color:#f8c8c8">**介面版**（interface version）：</mark>
<mark style="background-color:#c8f0c8">**介面版** (interface version)：</mark>
薄殼與引擎之間公開介面的整數版號。

<mark style="background-color:#f8c8c8">**最低介面版**（floor）：</mark>
<mark style="background-color:#c8f0c8">**最低介面版** (floor)：</mark>
引擎仍支援的最低介面版。

<mark style="background-color:#f8c8c8">**檔案版**（schema version）：</mark>
<mark style="background-color:#c8f0c8">**檔案版** (schema version)：</mark>
VK 寫入檔案時用來標示該檔資料格式的整數版號。

<mark style="background-color:#f8c8c8">**救援路徑**（rescue path）：</mark>
<mark style="background-color:#f8c8c8">不論薄殼、VK 檔與引擎的版本組合是否相符，都必須能用的呼叫，只有這些：`install`、`upgrade --engine`、`sync` 的版本不符判定，以及四種印用法呼叫：`just vendor_kit`（不帶指令）、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項 `--help` 同）。本詞條不規定救援路徑以外 recipe 的 `-h`／`--help` 在版本組合不合時的行為。</mark>
<mark style="background-color:#f8c8c8">`just vendor_kit`（不帶指令）第一行印 `vendor_kit <版本>`，接著印用法，輸出到 stderr、以結束碼 `2` 結束。沒有頂層的 `-h`／`--version`：just 會把 `vendor_kit` 後面的 `-h`、`--version` 當成 recipe 名稱。</mark>
<mark style="background-color:#c8f0c8">**救援路徑** (rescue path)：</mark>
<mark style="background-color:#c8f0c8">不論薄殼、VK 檔與引擎的版本組合是否相符，都一定能用的幾種呼叫，用來升級或修復，讓版本組合回到相符。</mark>

<mark style="background-color:#f8c8c8">**契約**（contract）：</mark>
<mark style="background-color:#c8f0c8">**契約** (contract)：</mark>
VK 對使用者承諾不會隨意改變的那組介面；引擎內部實作不屬契約。
