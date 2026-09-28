# 02 名詞與縮寫

本頁是所有審閱頁的共同字典：VK 特定的名詞以這裡的定義為準，一般技術詞不收。本頁只定義、不決議。

## VK 組件（component）

| 中文名 | 英文 | 定義 |
|---|---|---|
| 引擎 | engine | 執行 VK recipe 的主程式，以容器 image 發布。 |
| 薄殼 | shell | `.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。 |
| 啟動器 | launcher | 從主機啟動引擎的入口；薄殼內的 POSIX sh 片段與首次導入用的 `bootstrap.sh` 都是啟動器。 |

## 常用詞

### 工具與 image

| 中文名 | 英文 | 定義 |
|---|---|---|
| repo | repo | 使用者的 git repo；一個 repo 可以有多個安裝目錄，例如 monorepo 的各個子目錄。 |
| `<repo>` | repository name | 出貨的那個 repo 的名字，也是工具名。 |
| 工具 | tool | repo 出貨、供另一個（或同一個）repo 導入的內容單位，名字是 `<repo>`。 |
| `<ns>` 命名空間 | namespace | 工具在 just 中提供 recipe 的命名空間。 |
| 工具 recipe | tool recipe | 工具在 `dist/just/<ns>.just` 提供、使用者以 `just <ns> …` 執行的 recipe；相對於 VK 自己的 recipe（`just vendor_kit …`）。 |
| 安裝目錄 | install directory | `.vendor_kit/` 的直接父目錄，也是 VK 的安裝單位。 |
| `dist/` | dist | repo 交付給 VK 的工具出貨目錄，內含 `files/`（要搬給導入的 repo 的檔案內容）、`init.toml`（宣告哪些檔是初始檔）、`just/<ns>.just`（工具提供的 recipe）。 |
| 工具內容 | tool content | 工具在 `dist/files/` 交付、展開後放進 `cache/<repo>/` 的那些檔。 |
| 取件 | fetch | 把工具內容從工具 image 取出、寫進 `cache/` 的動作。 |
| 工具 image | tool image | 封裝單一工具出貨內容、供 VK 取件的純資料容器 image；VK 不把它當程式執行。 |
| 引擎 image | engine image | 裝載 VK 引擎的容器 image。 |
| registry | registry | 存放並提供工具 image 與引擎 image 的服務。 |
| image 引用 | image reference | 唯一指定 registry 上某個 image 版本與內容的字串。<br>• 形式：`<名稱>:<tag>@sha256:<digest>`；`<digest>` 不含 `sha256:` 前綴。 |
| tag | tag | registry 中標示 image 版本的名稱。 |
| digest | digest | registry 用來識別 image 內容的 sha256 指紋。 |
| image ID | image ID | 本機容器引擎用來識別 image 內容的 ID，與 registry 的 digest 不同。 |
| 正式版 | release version | 不是預發行版本的發布版本。 |

### 檔案與本機狀態

| 中文名 | 英文 | 定義 |
|---|---|---|
| `.vendor_kit/` | - | VK 在 repo 內建立與管理的目錄，放薄殼、版本鎖定行、本機狀態與快取。 |
| `version.toml` | - | `.vendor_kit/version.toml`，放全部版本鎖定行的檔；進 git。 |
| repo 檔 | repo file | 位於 repo 內、由使用者擁有及維護，且不屬於 `.vendor_kit/` 的檔。 |
| VK 檔 | VK file | 由 VK 建立及管理、位於 `.vendor_kit/` 的檔。 |
| 進 git 的檔 | tracked file | 隨 repo 一起 commit 進 git 的檔。 |
| `cache/` | cache | VK 在 repo 本機保存已展開工具內容的目錄。 |
| `gen/` | generated files | VK 在 repo 本機的目錄，放 VK 產生、供 just 載入的檔（例如把各工具的 recipe 接起來的入口檔）；不進 git。 |
| 印記 | stamp | 記錄本機工具內容對應的版本與內容指紋的 VK 檔。 |
| 逐檔指紋 | per-file digest | `cache/` 內每個檔的 sha256；取件時逐檔計算並記進印記，寫入前再重驗一次。 |
| 自描述標頭 | self-describing header | 薄殼檔內描述其介面版、引擎版與其餘內容 sha256 值的標頭。 |
| CI 檢查腳本 | CI check script | 薄殼之一 `.vendor_kit/ci/check.sh`，給使用者接進自己 CI 用。 |
| 執行紀錄 | run log | 記錄一次 VK 執行以供事後追溯的 VK 檔。 |
| 進度檔 | progress file | 記錄可寫 recipe 未完成狀態的 VK 檔。 |

### 版本與來源

| 中文名 | 英文 | 定義 |
|---|---|---|
| 版本鎖定行 | lock version line | `version.toml` 中的 TOML 項目。<br>• 內容：把引擎或工具的名稱對應到一個鎖定版本，寫成 image 引用。<br>• 作用：記錄該引擎或工具要用的鎖定版本。 |
| 鎖定版本 | locked version | image 引用用 `tag@digest` 唯一指定的那個版本與內容；沒有本機覆寫時，導入的內容就是它。 |
| 本機覆寫 | local override | 讓引擎或工具暫時改用本機開發來源的 VK 項目。<br>• 內容：記錄本機開發來源。<br>• 作用：有本機覆寫時，優先於版本鎖定行。 |
| 本機開發來源 | local source | 本機覆寫指到的來源：工具是一個本機目錄，引擎是一個本機 image；只在這台機器有效，不進 git。 |

### 初始檔與合併

| 中文名 | 英文 | 定義 |
|---|---|---|
| 初始檔 | init file | 由工具提供、VK 導入 repo 後交由使用者維護的 repo 檔。 |
| 納管 | managed | VK 已記錄某個初始檔的來源，並在後續升級中處理它的狀態。 |
| metadata | metadata | 記錄初始檔來源與 VK 管理狀態的 VK 檔。 |
| 基準版 | baseline | 上次套用的初始檔原版副本，是與目前 repo 檔、新版初始檔合併時的共同祖先。 |
| 基準版合併 | baseline merge | 以基準版、目前 repo 檔與新版初始檔為三份輸入所做的合併（git 的 three-way merge）。 |
| 合併衝突 | merge conflict | 基準版合併無法自動決定合併內容的結果。 |

### 互動、結果與版本號

| 中文名 | 英文 | 定義 |
|---|---|---|
| CI 模式 | CI mode | VK 在 CI 環境中執行時採用的模式。 |
| 詢問 | prompt | VK 在修改 repo 檔前，向使用者取得同意的互動。 |
| `-y` | yes option | 讓使用者預先回答詢問的選項。 |
| VK recipe | VK recipe | VK 自己的指令，寫法 `just vendor_kit <recipe>`；`vendor_kit` 是 just 的 module，每個指令是該 module 下的一個 recipe。全部 recipe 列在本頁最後一節。 |
| 選項 | option | recipe 後面帶的 `-x` 或 `--long` 參數。 |
| 可寫 recipe | writing recipe | 會動進 git 的檔或進度檔的 recipe。<br>• 包含 install、uninstall、add、remove、upgrade、dev、undev、prune。<br>• `prune` 雖清理本機資源，執行時仍會建立進度檔，因此屬於可寫 recipe。 |
| 唯讀 recipe | read-only recipe | 不動進 git 的檔、也不動進度檔的 recipe。<br>• 包含 update、sync、help。<br>• 仍可寫 `cache/`、`gen/`。 |
| 需人處理 | needs human | VK 停下並要求使用者採取下一步的結果。 |
| 失敗 | failure | VK 因無法繼續而結束的結果。 |
| 警告 | warning | 指出非阻斷問題、不使該次執行成為失敗或需人處理的訊息。 |
| 介面版 | interface version | 薄殼與引擎之間公開介面的整數版號。 |
| 檔案版 | schema version | VK 寫入檔案時標示其資料格式的整數版號。 |
| 最低介面版 | floor | 引擎仍支援的最低介面版。 |
| 結束碼 | exit code | VK 程序向呼叫端回報結果的整數。 |
| 契約 | contract | VK 對使用者承諾不會隨意改變的部分：recipe 與選項、版本鎖定行與其他 VK 檔的格式、結束碼、`dist/` 的出貨格式。引擎內部實作不屬契約。 |

## VK recipe

| recipe | 做什麼 |
|---|---|
| `add` / `remove` | 把一個工具裝進 repo；`remove` 解除那個工具。 |
| `dev` / `undev` | 暫時讓引擎或工具用本機開發來源；`undev` 回到鎖定版本。 |
| `help` | 顯示 VK 指令的使用說明。 |
| `install` / `uninstall` | 把 VK 裝進 repo（再跑一次 = 修復）；`uninstall` 移除 VK。 |
| `prune` | 清理由 VK 產生、但已不再被目前 repo 使用的本機資源。 |
| `sync` | 使 repo 本機的工具內容與版本鎖定行或本機覆寫一致。 |
| `update` / `upgrade` | `update` 只查有沒有新版；`upgrade` 換成新版或指定版本。 |

**升引擎**：執行 `upgrade vendor_kit` 更換引擎版本。
