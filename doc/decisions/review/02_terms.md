# 02 名詞與縮寫

本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。第 01 頁「專案目的與承諾」已出現的詞，這裡給正式定義。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。

## VK 組件（component）

- **引擎**：執行 VK 動詞的主程式，以容器 image 發布。
- **薄殼**：`.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。
- **啟動器**：從主機啟動引擎的入口；薄殼內的 POSIX sh 片段與首次導入用的 `bootstrap.sh` 都是啟動器。

## 常用詞

### 工具與 image

| 中文名 | 英文 | 定義 |
|---|---|---|
| **repo** | repo | 使用者的 git repo；一個 repo 可以有多個導入根，例如 monorepo 的各個子目錄。 |
| **`<repo>`** | repository name | 出貨角色的 repo 名，也是該 repo 所出貨工具的名稱。 |
| **工具** | tool | repo 出貨、供另一個（或同一個）repo 導入的內容單位，名字是 `<repo>`。 |
| **`<ns>` 命名空間** | namespace | 工具在 just 中提供 recipe 的命名空間。 |
| **工具 recipe** | tool recipe | 工具提供、使用者以 `just <ns> …` 執行的 just 指令。 |
| **導入根** | install root | `.vendor_kit/` 的直接父目錄，也是 VK 的導入單位。 |
| **`dist/`** | dist | repo 交付給 VK 的工具出貨目錄。 |
| **工具 image** | tool image | 封裝單一工具出貨內容、供 VK 取出且不作為程式執行的純資料容器 image。 |
| **引擎 image** | engine image | 裝載 VK 引擎的容器 image。 |
| **registry** | registry | 存放並提供工具 image 與引擎 image 的服務。 |
| **image 引用** | image reference | 唯一指定 registry 上某個 image 版本與內容的字串。<br>• 形式：`<名稱>:<tag>@sha256:<digest>`；`<digest>` 不含 `sha256:` 前綴。 |
| **tag** | tag | registry 中標示 image 版本的名稱。 |
| **digest** | digest | registry 用來識別 image 內容的 sha256 指紋。 |
| **image ID** | image ID | 本機容器引擎用來識別 image 內容的 ID，與 registry 的 digest 不同。 |
| **正式版** | release version | 不是預發行版本的發布版本。 |

### 檔案與本機狀態

| 中文名 | 英文 | 定義 |
|---|---|---|
| **repo 檔** | repo file | 位於 repo 內、由使用者擁有及維護，且不屬於 `.vendor_kit/` 的檔。 |
| **VK 檔** | VK file | 由 VK 建立及管理、位於 `.vendor_kit/` 的檔。 |
| **進 git 的檔** | tracked file | 預期由 git 追蹤並隨 repo commit 的檔。 |
| **`cache/`** | cache | VK 在 repo 本機保存已展開工具內容的目錄。 |
| **`gen/`** | generated files | VK 在 repo 本機保存生成檔的目錄。 |
| **印記** | stamp | 描述本機工具內容所對應版本與內容的 VK 檔。 |
| **自描述標頭** | self-describing header | 薄殼檔內描述其介面版、引擎版與其餘內容 sha256 值的標頭。 |
| **執行紀錄** | run log | 記錄一次 VK 執行以供事後追溯的 VK 檔。 |
| **進度檔** | progress file | 記錄可寫動詞未完成狀態的 VK 檔。 |

### 版本與來源

| 中文名 | 英文 | 定義 |
|---|---|---|
| **版本鎖定行** | lock version line | `version.toml` 中的 TOML 項目。<br>• 內容：把引擎或工具名稱對應到確切 image 版本。<br>• 作用：決定引擎或工具使用的鎖定版本。 |
| **本機覆寫** | local override | 讓引擎或工具暫時改用本機開發來源的 VK 項目。<br>• 內容：記錄本機開發來源。<br>• 作用：有本機覆寫時，優先於版本鎖定行。 |

### 初始檔與合併

| 中文名 | 英文 | 定義 |
|---|---|---|
| **初始檔** | init file | 由工具提供、VK 導入 repo 後交由使用者維護的 repo 檔。 |
| **納管** | managed | VK 已記錄某個初始檔的來源，並在後續升級中處理它的狀態。 |
| **metadata** | metadata | 記錄初始檔來源與 VK 管理狀態的 VK 檔。 |
| **基準版** | baseline | 上次套用的初始檔原版副本，作為與目前 repo 檔、新版初始檔合併時的共同祖先。 |
| **基準版合併** | baseline merge | 以基準版、目前 repo 檔與新版初始檔為三份輸入所做的合併（git 的 three-way merge）。 |
| **合併衝突** | merge conflict | 基準版合併無法自動決定合併內容的結果。 |

### 互動、結果與版本號

| 中文名 | 英文 | 定義 |
|---|---|---|
| **CI 模式** | CI mode | VK 在 CI 環境中執行時採用的模式。 |
| **詢問** | prompt | VK 在修改 repo 檔前，向使用者取得同意的互動。 |
| **`-y`** | yes option | 讓使用者預先回答詢問的選項。 |
| **可寫動詞** | writing verb | 會動進 git 的檔或進度檔的動詞。<br>• 包含 install、uninstall、add、remove、upgrade、dev、undev、prune。<br>• `prune` 雖清理本機資源，執行時仍會建立進度檔，因此屬於可寫動詞。 |
| **唯讀動詞** | read-only verb | 不動進 git 的檔、也不動進度檔的動詞。<br>• 包含 update、sync、help。<br>• 仍可寫 `cache/`、`gen/`。 |
| **需人處理** | needs human | VK 停下並要求使用者採取下一步的結果。 |
| **失敗** | failure | VK 因無法繼續而結束的結果。 |
| **警告** | warning | 指出非阻斷問題、不使該次執行成為失敗或需人處理的訊息。 |
| **介面版** | interface version | 薄殼與引擎之間公開介面的整數版號。 |
| **檔案版** | schema version | VK 寫入檔案時標示其資料格式的整數版號。 |
| **最低介面版** | floor | 引擎仍支援的最低介面版。 |
| **結束碼** | exit code | VK 程序向呼叫端回報結果的整數。 |

## 動詞

| 動詞 | 做什麼 |
|---|---|
| `install` | 將 VK 導入 repo，或修復既有導入。 |
| `uninstall` | 從 repo 移除 VK 的導入。 |
| `add` | 將一個工具導入 repo。 |
| `remove` | 從 repo 解除一個工具的導入。 |
| `update` | 查詢已導入的引擎或工具是否有可用新版。 |
| `upgrade` | 將已導入的引擎或工具改為另一個版本。 |
| `dev` | 暫時讓已導入的引擎或工具使用本機開發來源。 |
| `undev` | 取消本機開發來源，恢復使用鎖定版本。 |
| `sync` | 使 repo 本機的工具內容與版本鎖定行或本機覆寫一致。 |
| `prune` | 清理由 VK 產生、但已不再被目前 repo 使用的本機資源。 |
| `help` | 顯示 VK 指令的使用說明。 |

**升引擎**：執行 `upgrade vendor_kit` 更換引擎版本。
