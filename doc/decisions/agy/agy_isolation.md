本份調查針對 **vendor_kit 如何將「自己的檔案（工具檔）」與「使用者的檔案」明確切割** 進行全網路資料研析。依指令嚴格使用純網路檢索，未執行任何本機指令與讀寫。

---

# 目錄
- [A. 根 justfile 怎麼不碰使用者的](#a-根-justfile-怎麼不碰使用者的)
  - [1. just 的檔案尋找規則與語法規範](#1-just-的檔案尋找規則與語法規範)
  - [2. 前例：工具「擁有」根入口檔、使用者放擴充檔的做法](#2-前例工具擁有根入口檔使用者放擴充檔的做法)
  - [3. 反過來：工具在使用者檔中「加一行」的痛點與演變](#3-反過來工具在使用者檔中加一行的痛點與演變)
- [B. 版本檔與工具目錄的命名／位置慣例](#b-版本檔與工具目錄的命名位置慣例)
  - [4. 工具狀態檔放置位置與命名慣例（點目錄 vs 根單檔）](#4-工具狀態檔放置位置與命名慣例點目錄-vs-根單檔)
  - [5. 三個候選結構具體評估](#5-三個候選結構具體評估)
- [C. 初始檔怎麼明確隔離](#c-初始檔怎麼明確隔離)
  - [6. 生成／範本工具如何標示工具給的檔案與變更權責](#6-生成範本工具如何標示工具給的檔案與變更權責)
  - [7. 三方合併與 baseline 記錄前例（dpkg 規則適用性）](#7-三方合併與-baseline-記錄前例dpkg-規則適用性)
  - [8. 初始檔收進子目錄、專案根只留 symlink/include 的可行性矩陣](#8-初始檔收進子目錄專案根只留-symlinkinclude-的可行性矩陣)
- [總結比較表（A、B、C）](#總結比較表abc)

---

# A. 根 justfile 怎麼不碰使用者的

## 1. just 的檔案尋找規則與語法規範

引用自 [Just 官方手冊（Just Programmer's Manual）](https://just.systems/man/en/) 與 [casey/just 原始碼庫](https://github.com/casey/just)：

### (1) 搜尋檔名、大小寫與優先順序
* **候選檔名與大小寫**：`just` 在未指定檔案時，預設搜尋 `justfile` 與 `.justfile`（以點開頭作為隱藏檔）。此比對為**大小寫不敏感（case-insensitive）**，即 `Justfile`、`JUSTFILE`、`JuStFiLe` 均為合法檔名。
  * *手冊章節*：[1.1 Quick start](https://just.systems/man/en/chapter_1.html#quick-start)
* **同目錄多個候選檔衝突（Precedence）**：若同一目錄下同時存在多個候選檔（例如同時存在 `justfile` 與 `.justfile`，或在大小寫區分的 Linux 檔案系統中同時存在 `Justfile` 與 `justfile`），`just` **不會**自動挑選，而是直接報錯中斷：`SearchError::MultipleCandidates`（訊息形如 `Multiple candidate justfiles found in <dir>: 'justfile' and '.justfile'`）。
  * *程式碼與手冊來源*：[src/search.rs](https://github.com/casey/just/blob/master/src/search.rs)、[src/search_error.rs](https://github.com/casey/just/blob/master/src/search_error.rs)
* **往上層目錄搜尋規則（Upward Search）**：從當前執行指令的工作目錄（Invocation Directory）開始找，若當前目錄沒有候選檔，則遞迴往父目錄（`..`）查找，直到檔案系統根目錄 `/` 或遇到 `--ceiling <DIR>` 邊界為止。

### (2) `JUST_JUSTFILE` 與 `--justfile`
* **旗標與環境變數**：可以使用 `-f <PATH>` / `--justfile <PATH>` 旗標，或設定環境變數 `JUST_JUSTFILE=<PATH>`。兩者效果相同，會**完全跳過**向上遍歷搜尋邏輯，強制直接載入該檔案。
  * *手冊章節*：[1.1 Quick start](https://just.systems/man/en/chapter_1.html#quick-start)、[Debian just manpage](https://manpages.debian.org/unstable/just/just.1.en.html)

### (3) `set fallback`
* **語法與行為**：在 justfile 頂部設定 `set fallback := true`（亦可寫成 `set fallback`）。若在當前 justfile 中找不到使用者呼叫的 recipe，`just` 會自動向上層父目錄繼續搜尋父 justfile，若父 justfile 有該 recipe 則執行之。此向上搜尋會在遇到未啟用 fallback 或根目錄時停止。
  * *手冊章節*：[1.11.4 Fallback to parent justfiles](https://just.systems/man/en/chapter_11.html#fallback-to-parent-justfiles)、[Settings](https://just.systems/man/en/chapter_12.html#settings)

### (4) `import` / `import?` / `mod` / `mod?` 的語意與相對路徑解析
* **`import 'PATH'`**：將目標 justfile 的所有 recipe、變數、alias **展平（flatten）** 併入當前 justfile 的 namespace。
  * **相對路徑解析**：路徑是相對於「**包含該 import 陳述式的 justfile 所在目錄**」，而非指令執行的目錄。支援以 `~/` 開頭表示家目錄。
  * **覆蓋規則**：頂層（當前檔案）定義優先於 import 進來的定義；同層若有重複且開啟了 `set allow-duplicate-recipes`，在後的 import 覆蓋在先的。
  * *手冊章節*：[1.11.1 Imports](https://just.systems/man/en/chapter_11.html#imports)
* **`import? 'PATH'`**：**選擇性載入（Optional Import）**。若目標檔案不存在，不會報錯，直接忽略跳過。
  * *手冊章節*：[1.11.1 Imports](https://just.systems/man/en/chapter_11.html#imports)
* **`mod NAME 'PATH'`**：建立**子模組（Submodule）**命名空間。
  * 呼叫方式為 `just <module>::<recipe>`。
  * **執行目錄語意**：子模組內的 recipe 預設其執行工作目錄為「該子模組檔案所在目錄」（與根 justfile 預設在根目錄不同），除非加上 `[no-cd]` 屬性。
  * 若未指定 `'PATH'`，則預設尋找 `NAME.just`、`NAME/mod.just`、`NAME/justfile`、`NAME/.justfile`。
  * *手冊章節*：[1.11.2 Modules](https://just.systems/man/en/chapter_11.html#modules)
* **`mod? NAME 'PATH'`**：**選擇性模組（Optional Module）**。若路徑不存在不報錯；相依於此 missing module 的 recipe 會自動變成 disabled，呼叫時才報錯。
  * *手冊章節*：[1.11.2 Modules](https://just.systems/man/en/chapter_11.html#modules)

### (5) `[group]` 屬性
* **語法**：`[group('NAME')]` 可標註於 recipe、alias 或 mod 上。支援多個群組標籤。
* **效果**：在執行 `just --list` 或 `just --summary` 時，輸出會自動以該 group 分區段呈現（如 `[build]`、`[test]`、`[vendor_kit]`），大幅改善大型或 import 多檔案時的指令可讀性。
  * *手冊章節*：[Groups / Attributes](https://just.systems/man/en/chapter_49.html)

### (6) `set positional-arguments`
* **語法與效果**：設定 `set positional-arguments := true`（或 recipe 級別標註 `[positional-arguments]`）。
* **行為**：將傳遞給 recipe 的參數直接作為 shell 腳本的位置參數（`$1`、`$2`、`"$@"`）傳入，而非由 just 做文字插值替換（text interpolation），能避免引號與空白切詞的逃逸漏洞。
  * *手冊章節*：[Positional Arguments](https://just.systems/man/en/chapter_12.html#positional-arguments)

### (7) `just --list` 對 import 進來的 recipe 怎麼顯示
* **import 的顯示**：因為 import 是展平合併，import 進來的 recipe 會與根 justfile 自身的 recipe 混在同一個清單中顯示。若該 recipe 帶有 `[group('...')]`，則顯示在對應群組標題下方；若未標註群組，則顯示在全域列表中。
* **mod 的顯示**：若使用 `mod`，根目錄 `just --list` 會顯示該 module 名稱與其 doc-comment；若要查看該模組內部 recipe，需執行 `just <module> --list`。
  * *手冊章節*：[Listing Available Recipes](https://just.systems/man/en/chapter_11.html#modules)

---

## 2. 前例：工具「擁有」根入口檔、使用者放擴充檔的做法

常見於「專案必須遵循工具骨架」的強規範型專案。

### (1) `ycpss91255-docker/base` 的 symlink 模式
* **做法**：在工具 repo 的安裝腳本（`init.sh`）中，將 base 工具目錄下的 `dist/script/justfile` 建立軟連結（symlink）到下游專案根目錄的 `justfile`；根 justfile 內寫死以 `import? "script/local/justfile.local"` 引入使用者的自訂指令。
* **誰擁有根檔**：工具（base）擁有，根檔實質為指向 base 快取/子模組的 symlink。
* **使用者擴充放哪**：專屬本機擴充檔 `script/local/justfile.local`。
* **升級時根檔怎麼換**：重新執行工具的初始化/更新指令，若 symlink 損壞或指向舊路徑，自動更新 symlink 目標指向新的工具 dist 快取目錄。
* *案例與來源*：[ycpss91255-docker/base ADR-00000010（Layered-entry refactor）](https://github.com/ycpss91255-docker/base)、[ADR-00000011](https://github.com/ycpss91255-docker/base)

### (2) Makefile 的 `-include local.mk` / `include`
* **做法**：GNU Make 支援 `-include`（忽略不存在的檔案）。工具託管專案標準 `Makefile`，在最末行寫入 `-include local.mk` 或 `-include Makefile.local`。
* **誰擁有根檔**：工具／框架擁有 `Makefile`。
* **使用者擴充放哪**：`local.mk`（通常在 `.gitignore` 中忽略，或作為本地覆蓋專用）。
* **升級時根檔怎麼換**：直接覆蓋或由框架套件管理工具更新 `Makefile`，使用者在 `local.mk` 中的 target 與變數不受影響。
* *案例與來源*：[GNU Make Manual: 3.3 Including Other Makefiles](https://www.gnu.org/software/make/manual/html_node/Include.html)

### (3) Taskfile 的 `includes:`
* **做法**：Taskfile 支援 `includes:` 區段，並可設定 `optional: true`。例如工具提供預設 `Taskfile.yml`，裡面宣告引入 `Taskfile.local.yml`。
* **誰擁有根檔**：工具擁有根 `Taskfile.yml`。
* **使用者擴充放哪**：`Taskfile.local.yml`。
* **升級時根檔怎麼換**：覆蓋根 `Taskfile.yml`。
* *案例與來源*：[Taskfile Documentation: Including other Taskfiles](https://taskfile.dev/usage/#including-other-taskfiles)

### (4) Earthly 的 `IMPORT`
* **做法**：Earthfile 透過 `IMPORT <repo/path> AS <alias>` 引入外部可重用 targets（例如官方 Earthly Lib）。
* **誰擁有根檔**：使用者擁有根 `Earthfile`，工具以 library 形式由使用者主動 import。
* **使用者擴充放哪**：根 `Earthfile` 內直接撰寫。
* **升級時根檔怎麼換**：使用者修改根 `Earthfile` 內的 `IMPORT` 版本 tag。
* *案例與來源*：[Earthly Hacker Guide: Importing](https://docs.earthly.dev/docs/hacker-guide/importing)

### (5) mise 的 `mise.toml` + `mise.local.toml`
* **做法**：mise 具有分層設定機制（Hierarchy）。專案根目錄提交 `mise.toml`（或 `.mise.toml`），而個人環境或專案局部覆蓋則放 `mise.local.toml`（自動被 mise 慣例列入 gitignore）。
* **誰擁有根檔**：團隊／專案維護者擁有 `mise.toml`。
* **使用者擴充放哪**：`mise.local.toml`。
* **升級時根檔怎麼換**：更新 `mise.toml` 的 tool 版本，不干擾各開發者私有的 `mise.local.toml`。
* *案例與[agy] print timeout after 9m0s with turn in progress; returning partial output
