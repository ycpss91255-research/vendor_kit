# vendor_kit

vendor_kit (VK) 把工具從一個 repo 送進其他 repo：出貨端把工具打包成容器 image，導入端用一行版本鎖定行決定裝哪一版。這裡只定義這件事用到的專有名詞，一般技術詞不收。

對外承諾見[目的與承諾](../../contract/01_purpose.md)，不變量見[不變量](../../contract/02_invariants.md)，難逆轉的取捨見 [ADR](../../adr/)。

## Language

### 角色與情境

**VK** (vendor_kit)：
vendor_kit 的簡稱；在承諾關係裡指提出承諾的一方，即引擎與薄殼的維護者。

**使用者** (user)：
用 VK 管理工具的人，也就是被承諾的一方。
_Avoid_: 下游使用者、下游開發者、工具 repo 開發者、專案維護者

**導入** (consume)：
使用者把別人做好的工具帶進自己的 repo 並交給 VK 管的那個情境。
_Avoid_: 接入

**出貨** (ship)：
使用者把自己做的工具打包出去、給別的 repo 導入的那個情境。

### VK 組件

**引擎** (engine)：
執行 VK recipe 的主程式，以容器 image 發布。

**薄殼** (shell)：
`.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。

**啟動器** (launcher)：
從主機啟動引擎的入口；薄殼內的啟動片段，與從 VK 的 Release 取得的 `bootstrap.sh`，都是啟動器。後者用於首次導入，以及既有安裝目錄的薄殼檢查與修復。

### 工具與出貨

**repo**：
使用者的 git repo；一個 repo 可以有多個安裝目錄。
_Avoid_: 專案、下游 repo

**`<repo>`** (repository name)：
出貨的那個 repo 的名字，也是工具名。
`vendor_kit` 是保留名稱，不能作為工具名。
_Avoid_: `<name>`

**工具** (tool)：
repo 出貨、供另一個（或同一個）repo 導入的內容單位，名字是 `<repo>`。

**安裝目錄** (install directory)：
`.vendor_kit/` 的直接父目錄，也是 VK 的安裝單位。
_Avoid_: 專案根、導入根

**`<ns>` 命名空間** (namespace)：
工具在 just 中提供工具 recipe 的命名空間。

**工具 recipe** (tool recipe)：
工具自己提供、使用者以 `just <ns> …` 執行的 recipe，相對於 VK recipe。

**`dist/`**：
repo 交付給 VK 的工具出貨目錄。

**工具內容** (tool content)：
工具在 `dist/` 交付、展開後放進 `cache/` 的那些檔。

**取件** (fetch)：
把工具內容從工具 image 取出、寫進 `cache/` 的動作。

**工具 image** (tool image)：
封裝單一工具出貨內容的純資料容器 image；VK 不把它當程式執行。
_Avoid_: 下游 image

**引擎 image** (engine image)：
裝載 VK 引擎的容器 image。

**registry**：
存放並提供工具 image 與引擎 image 的服務。

**image 引用** (image reference)：
唯一指定某個 image 版本與內容的字串 `<registry>/<路徑>:<tag>@sha256:<digest>`；`<registry>` 是存放它的 registry 主機，`<路徑>` 是 image 在那個 registry 裡的路徑。tag 與 digest 一起寫，所以同一行同時說得出版本與內容。

**tag**：
image 引用裡供人與外部版本追蹤工具辨識版本的標籤；格式與版本比較規則見 [04 使用者介面](../../contract/04_interface.md)的[指定版本](../../contract/04_interface.md#指定版本)。

**digest**：
image 引用裡那個 image 內容的 sha256；內容相同才會相同，所以它鎖的是內容，不是版本。

### repo 內的檔與狀態

**`.vendor_kit/`**：
VK 在 repo 內建立與管理的目錄，放薄殼、版本鎖定行、本機狀態與快取。

**`version.toml`**：
`.vendor_kit/version.toml`，放全部版本鎖定行與[介面版列表](#介面版與契約)的檔；進 git。
_Avoid_: `.version`

**repo 檔** (repo file)：
位於 repo 內、由使用者擁有及維護，且不屬於 `.vendor_kit/` 的檔。
_Avoid_: 專案檔

**VK 檔** (VK file)：
由 VK 建立及管理、位於 `.vendor_kit/` 的檔。

**追蹤檔** (tracked file)：
隨 repo 一起由 git 追蹤並 commit 的檔，含還沒建出來、建出來就要 commit 的檔。
_Avoid_: 進 git 的檔、tracked 檔、版控檔

**`cache/`**：
VK 在 repo 本機保存已展開工具內容的目錄。
_Avoid_: `.<repo>/`

**`gen/`**：
VK 在 repo 本機的目錄，放 VK 產生、供 just 載入的檔；不進 git。

**印記** (stamp)：
記錄本機工具內容對應的版本與內容指紋的 VK 檔。
_Avoid_: 簽章、信任來源

**逐檔指紋** (per-file digest)：
`cache/` 內每個檔的 sha256，記在印記裡。

**自描述標頭** (self-describing header)：
薄殼檔開頭描述自身介面版、引擎版與其餘內容指紋的資料；它支援薄殼被改過時的檢查，見 [02 不變量](../../contract/02_invariants.md)的[第 6 條](../../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)。

**執行紀錄** (run log)：
記錄一次 VK 執行以供事後追溯的 VK 檔。

**進度檔** (progress file)：
記錄可寫 recipe 未完成狀態的 VK 檔。

### 版本與來源

**版本鎖定行** (lock version line)：
`version.toml` 裡把一個引擎或工具對應到一個鎖定版本的 TOML 項目。

**鎖定版本** (locked version)：
版本鎖定行以 image 引用指定的版本與內容；相關指令見 [04 使用者介面](../../contract/04_interface.md)的[指令](../../contract/04_interface.md#指令)。

**本機覆寫** (local override)：
讓引擎或工具暫時改用本機開發來源、優先於版本鎖定行的 VK 項目；啟用與解除方式見 [04 使用者介面](../../contract/04_interface.md)的[本機覆寫](../../contract/04_interface.md#本機覆寫)。

**本機開發來源** (local source)：
本機覆寫指到的來源：工具是一個本機目錄，引擎是一個本機 image；不進 git。

### 初始檔與合併

**初始檔** (init file)：
由工具提供、VK 導入 repo 後交由使用者維護的 repo 檔。

**納管** (managed)：
VK 已記錄某個初始檔的來源、並會在後續升級中處理它的狀態。

**metadata**：
記錄初始檔來源與 VK 納管狀態的 VK 檔。

**基準版** (baseline)：
上次套用的初始檔原版副本，也就是合併時的共同祖先。

**基準版合併** (baseline merge)：
以基準版、目前 repo 檔與新版初始檔為輸入所做的合併。
_Avoid_: 三方合併

**合併衝突** (merge conflict)：
基準版合併無法自動決定合併內容的結果；處理方式見 [04 使用者介面](../../contract/04_interface.md)的[使用者的檔與 VK 的檔](../../contract/04_interface.md#使用者的檔與-vk-的檔)。

### 執行與結果

**VK recipe**：
VK 自己提供、收在 `vendor_kit` 命名空間下的 recipe，相對於工具 recipe；`bootstrap.sh` 不是 VK recipe。
_Avoid_: 動詞、子命令、子指令

**可寫 recipe** (writing recipe)：
會動到追蹤檔或進度檔的 VK recipe。

**唯讀 recipe** (read-only recipe)：
不動追蹤檔、也不動進度檔的 VK recipe。

**詢問** (prompt)：
VK 在修改 repo 檔前，向使用者取得同意的互動。

**`-y`** (yes option)：
讓使用者預先回答詢問的選項。
寫法：`-y`，長選項 `--yes`。

**預演** (dry run)：
以 `--dry-run` 啟動、算出完整計畫並列出會改的內容、但不做這些修改的執行；規則見 [04 使用者介面](../../contract/04_interface.md)的[預演](../../contract/04_interface.md#預演)。
寫法：`--dry-run`。

**`--engine`** (engine option)：
讓 VK recipe 的對象改為引擎、而不是工具的選項。
寫法：`--engine`；要帶版本時只接受 `--engine=<tag>`。

**`@<tag>`** (version suffix)：
接在 `<repo>` 後、指定工具版本的寫法。
寫法：`<repo>@<tag>`。

**選項結束標記** (end of options)：
表示選項到此為止的記號。
寫法：單獨的 `--`；它之後的參數一律當位置參數，即使以 `-` 開頭。

**診斷** (diagnostic)：
VK 印到 stderr、說明執行結果與原因的訊息。診斷使用的[嚴重度](#執行與結果)見下個詞條。

**嚴重度** (level)：
診斷的嚴重程度；可用的值以及它和結束碼的對應見 [03 輸出](../../contract/03_output.md)的[結束碼](../../contract/03_output.md#結束碼)。

**正常輸出** (normal output)：
成功時印到 stdout、不加前綴的輸出，例如改了什麼、查詢結果、`-h`/`--help` 的用法。

**待處理** (action required)：
診斷的處置屬性，表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令。
_Avoid_: 待續、需人處理、needs human

**失敗** (failure)：
診斷的處置屬性，表示這次執行沒有做完；不承諾可執行的修法，但可以附一般建議。

**警告** (warning)：
這次指令承諾的結果已做完，但有要使用者知道或確認的事的 `warn` 診斷；可以附下一步指令。

**原因代碼** (reason code)：
每條診斷的固定識別碼；格式與生命週期見 [03 輸出](../../contract/03_output.md)的[訊息](../../contract/03_output.md#訊息)。

**結束碼** (exit code)：
VK recipe 或 `bootstrap.sh` 結束時回給呼叫方、表示整體結果的整數；各碼語意與彙總規則見 [03 輸出](../../contract/03_output.md)的[結束碼](../../contract/03_output.md#結束碼)。

### VK recipe 與用途

**`add` / `remove`**：
`add` 把工具納入安裝目錄，`remove` 將它解除；兩者的介面與保留使用者檔規則見 [04 使用者介面](../../contract/04_interface.md)的[指令](../../contract/04_interface.md#指令)及[使用者的檔與 VK 的檔](../../contract/04_interface.md#使用者的檔與-vk-的檔)。

**`update`、`upgrade`**：
`update` 只查有沒有新版；`upgrade` 把鎖定版本換成新版或指定版本。
介面見 [04 使用者介面](../../contract/04_interface.md)的[指令](../../contract/04_interface.md#指令)；指定版本見 [04 使用者介面](../../contract/04_interface.md)的[指定版本](../../contract/04_interface.md#指定版本)。

**`dev` / `undev`**：
`dev` 讓引擎或工具改用本機開發來源，`undev` 使它回到鎖定版本；兩者的關係見 [04 使用者介面](../../contract/04_interface.md)的[成對與無害](../../contract/04_interface.md#成對與無害)。

**`sync`**：
使本機工具內容與版本鎖定行或本機覆寫一致的 VK recipe；介面見 [04 使用者介面](../../contract/04_interface.md)的[指令](../../contract/04_interface.md#指令)。

**`prune`**：
清除 VK 產生但目前 repo 已不再使用之本機資源的 VK recipe；無害性承諾見 [04 使用者介面](../../contract/04_interface.md)的[成對與無害](../../contract/04_interface.md#成對與無害)。

**`install` / `uninstall`**：
`install` 使 repo 裡的一個目錄成為安裝目錄，`uninstall` 將 VK 從該處移除；兩者的介面與保留使用者檔規則見 [04 使用者介面](../../contract/04_interface.md)的[指令](../../contract/04_interface.md#指令)及[使用者的檔與 VK 的檔](../../contract/04_interface.md#使用者的檔與-vk-的檔)。

**`test`**：
檢查安裝目錄狀態或工具交付內容，且不寫入追蹤檔的 VK recipe。
帶一個安裝目錄底下 `test/` 裡的路徑時，先做完整安裝檢查，成功後依使用者自己的測試設定，跑所選路徑裡使用者自己寫的測試。範圍與用法見 [04 使用者介面](../../contract/04_interface.md)的[檢查](../../contract/04_interface.md#檢查-test)。

### 介面版與契約

**介面版** (interface version)：
薄殼與引擎之間公開介面的整數版號。

**最低介面版** (floor)：
引擎仍支援的最低介面版。

**介面版列表** (protocol list)：
`version.toml` 裡記錄鎖定引擎支援哪些介面版的項目，從最低介面版到目前介面版逐一列出。

**檔案版** (schema version)：
VK 寫入檔案時用來標示該檔資料格式的整數版號。

**救援路徑** (rescue path)：
版本組合不相符或薄殼被改過時，仍可用來檢查、升級或修復的呼叫；兩類的清單見 [04 使用者介面](../../contract/04_interface.md)的[寫入範圍與其他指令的關係](../../contract/04_interface.md#寫入範圍與其他指令的關係)。

**契約** (contract)：
VK 對使用者承諾不會隨意改變的那組介面；引擎內部實作不屬契約。
