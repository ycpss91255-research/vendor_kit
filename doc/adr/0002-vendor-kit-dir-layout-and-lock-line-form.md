# VK 的狀態全收進 `.vendor_kit/`，版本鎖定行只認一種正規形

每個安裝目錄對「用哪些工具、哪個版本、哪個引擎」只能有一份說法（[不變量 2](../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)），而自動化不寫追蹤檔（[不變量 3](../contract/02_invariants.md#3-自動化不寫追蹤檔)）。所以 VK 的狀態全收進安裝目錄下的 `.vendor_kit/`，由它自己的 `.gitignore` 寫死哪些路徑不進 git；版本鎖定行 `version.toml` 只認一種正規形，讓主機上只有 `grep`／`sed` 的啟動器也讀得準，而同一份內容不會有兩種合法寫法。

## Considered Options

- **引擎版本固定放第一行，啟動器用 `head -1`**：省掉命中數檢查，但有人在檔頭加一行註解或空行就讀錯版本，而且不報錯。
- **寬鬆解析（接受 BOM、重複鍵、`[tools]` 表外的工具項）**：對手改的人友善，但同一份內容有多種寫法，「只有一份說法」退化成「只有一個檔」。重複鍵更糟：TOML 是後鍵蓋前鍵，看檔的人讀到的卻是前面那一行。
- **引擎讀到非正規形時自動改寫**：`version.toml` 進 git，自動改寫等於自動化寫追蹤檔，違反不變量 3。
- **用 `.git/info/exclude` 或使用者根目錄的 `.gitignore` 排除 VK 的本機狀態**：前者不進 git，每個 clone 都要重做，漏做的症狀是 `cache/` 被 commit；後者是使用者的檔，寫它要走詢問流程（[不變量 1](../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)），而且每個安裝目錄都要在同一個檔裡加一段。
- **把 `cache/` 之類的本機狀態放到 repo 外（例如 `~/.cache`）**：不必排除任何路徑，但兩個 clone 或 CI 的每次全新 checkout，狀態就不再跟著安裝目錄走，而不變量 2 的唯一性單位是安裝目錄。

## Consequences

- 啟動器不需要 TOML 解析器；非正規形在引擎讀檔時就擋掉，不帶著半套版本資訊往下跑。
- 使用者手改 `version.toml` 要照正規形；TOML 本身合法、但不是正規形的寫法會被拒。
- 正規形是三處的共同契約：啟動器的 `grep`、引擎的解析、Renovate 的 regex。改格式要同時改這三處。
- `.vendor_kit/.gitignore` 的涵蓋清單要與引擎實際會寫的路徑一致；新增一種產出路徑時漏加，就會有檔跑進使用者的 `git status`。
- 內部機制（之後搬到實作 issue）：
  - 目錄佈局：`version.toml`、`version.local.toml`、`cache/<repo>/`、自有 `.gitignore` 都在 `.vendor_kit/`，每個安裝目錄一份，彼此不共享。
  - 引擎行不靠行號：唯一符合 `^vendor_kit[[:space:]]*=` 的行（POSIX BRE，不用 `\s`）。啟動器以 `grep` 取得，命中數必須恰為 1；0 或 2 以上表示這個檔不是 VK 寫出來的形狀。第一行只是 `install` 寫出的慣例。
  - 介面版列表：`version.toml` 在根層記 `vendor_kit_protocols = "<列表>"`，寫出新檔時緊接在引擎行下面，讀取不靠行號。列表把鎖定引擎的 `[floor, current]` 逐一展開，以一個空白分隔、連續遞增，不接受 0 或前導零（例如 `"2 3 4"`）。鍵名中的 `_` 讓它不被 `^vendor_kit[[:space:]]*=` 當成引擎行；啟動器可據此離線比對介面版。引擎讀檔只檢查列表形狀，不跟本引擎的區間比，因為列表記的是鎖定的那一版引擎接受的區間。`version.local.toml` 不檢查介面版列表。
  - 工具行：`[tools]` 表下每個工具一行；BOM、重複鍵、繞過 `[tools]` 表的寫法都不接受。引擎讀到非正規形就以[結束碼 `2`](../contract/03_output.md#結束碼)結束、列出差異、不動任何檔。
  - `.vendor_kit/.gitignore` 目前涵蓋 `cache/`、`gen/`、`log/`、`version.local.toml`、`.tmp.*`。這份清單就是自動化可以自己寫的界線，清單外的一律要使用者明確打的 recipe。
  - 外部版本追蹤：Renovate 一條 regex manager 追 docker datasource，只改 `version.toml` 的引擎行與工具行，不改 `vendor_kit_protocols`；Renovate、`upgrade` 與人手改的都是同一個 `version.toml`。
  - 兩份版本真相的典型例子是 image tag 加上另一個 lock 檔。digest 才鎖內容；tag 只給人與外部版本追蹤工具看。
  - `version.local.toml` 只覆蓋已存在的版本鎖定行、不進 git，不是第二份真相。本機覆寫的引擎行（符合 `^vendor_kit[[:space:]]*=` 的行）只能有 0 或 1 行：0 行表示引擎沒有本機覆寫；1 行時，值是雙引號包住的本機 image 名稱（例如 `vendor_kit:dev`）或 image ID，不必帶 tag 與 digest，所以不是 image 引用。`vendor_kit_protocols` 不算引擎行。
