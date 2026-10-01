# VK recipe 一行轉發，寫入邊界與警告紅燈

> Status: accepted；CI 模式與依執行環境改變行為的部分由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代。

同一個 `justfile` 裡會載入好幾個工具的命名空間，recipe 的語意一改，寫進使用者自動化流程的呼叫不會報錯、只會靜默做另一件事。所以每個 VK recipe 在追蹤檔 `vendor.just` 裡只是一行轉發，規則全在引擎；任何警告都以 `warn`、結束碼 `1` 讓本機與自動化流程看見（依 [不變量頁第 3 條](../contract/02_invariants.md#3-自動化只碰不進-git-的東西)、[不變量頁第 8 條](../contract/02_invariants.md#8-使用者介面不可取代寫法一致)）。多工具、逐檔合併都會在中途失敗，守得住的是混合狀態可辨識（依 [不變量頁第 4 條](../contract/02_invariants.md#4-永不靜默失敗)），所以可寫 recipe 的寫入時序固定。原決議曾另設 CI 模式，將兩類無法依契約完成的情境列為 `error`、結束碼 `2`；這部分已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代，不再是現行規則。

選項寫法採 GNU 式的長短選項與 `--` ([GNU Coding Standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html))，有兩點刻意不遵循 [POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)：選項放在位置參數之後也可以（不遵循 Guideline 9），`--engine` 的值可帶可不帶（不遵循 Guideline 7）。值可帶可不帶，所以帶值只接受 `--engine=<tag>`：寫成 `--engine <tag>` 時，分不出後面那個字是 tag 還是位置參數。

## Considered Options

- **CI 模式只看 `CI` 有沒有設（歷史選項）**：`CI=0`、`CI=false` 的環境會被誤判，本機習慣導出這個變數的人會突然失去詢問。CI 模式本身已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取消。
- **CI 模式下連 `update` 也停掉（歷史選項）**：原決議保留 `update` 查 registry 的能力，因為它不動追蹤檔、也不動進度檔；CI 模式本身已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取消。
- **只有 CI 或部分警告紅燈（歷史選項）**：同一個警告在本機回成功、在 CI 才回非零，會讓兩邊採用不同判準；只挑部分警告回非零，也會讓已知異常混進成功。任何警告都統一回 `1` 的決定仍有效；依環境分流的部分已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代。
- **`gen/tools.just` 與 `cache/` 分兩次寫**：兩次之間中斷，就留下入口檔指著舊快取、看起來卻是好的 repo。
- **加 `init`／`diff`／`accept`／`rollback` 這類別名**：語意與既有 recipe 重疊，`diff`、`accept`、`rollback` 三件事 git 本來就做得到；依 [不變量頁第 8 條](../contract/02_invariants.md#8-使用者介面不可取代寫法一致)，每個介面都不可取代。
- **轉發行不進 git，改由啟動器現產**：fresh clone 在跑過啟動器之前沒有任何 `just` 入口，使用者第一步要打的就不是 `just`。

## Consequences

- `vendor.just` 進 git，fresh clone 直接有入口；代價是改轉發行等於改追蹤檔，要走 `upgrade --engine` 重產薄殼。
- 結束碼固定為 `0` info（成功）、`1` warn（做完了，但有警告）、`2` error（沒做完：待續、失敗或用法錯誤）、`3` fatal（只限版本組合不合）；一次有多個結果時取最大值。是否成功只看有沒有做到該 VK recipe 的契約承諾，不看診斷名稱或輸出串流。
- 所有警告都回 `1`。原決議另設 CI 模式的兩條附加規則；該分流已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代，僅作歷史記錄。
- 原決議以環境變數 `CI` 判定 CI 模式；該判定已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取消，VK 不再據此改變行為。
- 需要寫追蹤檔的情境各有固定的訊息與結束碼，改訊息或結束碼等於改介面。原決議曾讓基準版落後依執行環境回不同結束碼；該分流已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代。現行訊息與結束碼以[訊息與錯誤碼頁的總表](../contract/03_messages.csv)為準。
- 內部機制（之後搬到實作 issue）：
  - 轉發形狀：每個 recipe 一行 `<recipe> *args`，以 `[group('常用')]` 與 `[group('進階')]` 分段；轉發行不解讀參數、不判斷狀態。`vendor.just` 屬於四個薄殼追蹤檔之一（依 [不變量頁第 6 條](../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)）。
  - 原決議讓 `just vendor_kit test` 自己開啟 CI 模式，並讓 `update` 在 CI 模式下仍然查 registry；CI 模式已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取消，這段只記錄歷史。
  - 原決議的 CI 模式附加 `error` 規則是封閉清單：需要改追蹤檔時一律不寫，以及有任何本機覆寫；兩者都以結束碼 `2` 結束。這組附加規則已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代，不再是現行規則。現行結果依[訊息與錯誤碼頁的結束碼表](../contract/03_messages.md#結束碼)：任何警告回 `1`，版本組合不合回 `3`，其他沒做完的結果（待續、失敗或用法錯誤）回 `2`，多個結果取最大值。
  - `sync` 的未完成導入回 `2`；快取逐檔指紋驗不過就重裝並以 `warn` 回 `1`，重裝只動 VK 自己的 `cache/`，不違反寫入邊界。原決議曾讓基準版落後版本鎖定行依執行環境回不同結束碼，該分流已由 [ADR-0013](0013-no-ci-mode-strict-checks-in-test.md) 取代。現行訊息與結束碼以[訊息與錯誤碼頁的總表](../contract/03_messages.csv)為準。
  - 可寫 recipe 的時序：
    1. 主機前置檢查依 [ADR-0007 主機薄層決議](0007-host-thin-layer-and-shell-integrity.md)與 [使用者介面頁的主機需求](../contract/04_interface.md#主機需求)執行。Docker 版本不足與偵測到 Podman，首次導入與已有安裝目錄都由啟動器檢查；檢查沒有副作用，排在建執行紀錄之前，失敗時不留執行紀錄、不動任何 VK 檔，只在 stderr 印 `vendor_kit: error[VKnnnn]: <message>` 診斷、以 `2` 結束，訊息依 [訊息與錯誤碼頁的總表](../contract/03_messages.csv)。just 版本不足只有首次導入由 `bootstrap.sh` 檢查，失敗時同樣不留執行紀錄、不動任何 VK 檔，只在 stderr 印 `vendor_kit: error[VKnnnn]: <message>` 診斷、以 `2` 結束，訊息依 [訊息與錯誤碼頁的總表](../contract/03_messages.csv)；已有安裝目錄時由 just 解析 justfile 時自己拒絕，不承諾 VK 的訊息與結束碼，也不留執行紀錄。
    2. 建執行紀錄，早於任何寫入、拉 image、起引擎。
    3. 建進度檔（`.tmp.<verb>.<id>.toml`、metadata 的 `[progress]`），早於第一個 repo 檔或 VK 檔的寫入。
    4. 一次處理多個工具時，先對全部工具做完整預檢；任一項不過就整體不動，列出每一個原因，結束碼依各原因的結束碼取最大值。
    5. 寫入。中途失敗依 [不變量頁第 4 條](../contract/02_invariants.md#4-永不靜默失敗)處理。
    6. 最後才改版本鎖定行：工具層的可寫 recipe 回 `2` 時，該工具的版本鎖定行不動。升引擎是明列例外，見 [ADR-0007](0007-host-thin-layer-and-shell-integrity.md)。
  - 可寫 recipe 開始前發現未完成的進度檔，先恢復再繼續；唯讀 recipe 只偵測、不自動恢復。
  - `cache/` 與 `gen/` 是兩個目錄，不是一次原子替換。先換好 `cache/`，入口檔 `gen/tools.just` 最後才寫，兩者都寫完才刪進度檔；刪進度檔是這次 apply 唯一的完成點。完成點之前中斷，進度檔還在：可寫 recipe 先恢復，唯讀 recipe 報出未完成，入口檔與快取一新一舊的狀態不會被當成好的。
  - 工具交付的 `dist/just/<ns>.just` 每檔一個頂層命名空間，數量由工具自決，`<repo>.just` 必須存在；`gen/tools.just` 每個 `<ns>` 一行。`add` 在任何寫入之前檢查 `<ns>` 撞名（比對對象依 [使用者介面頁的命名空間](../contract/04_interface.md#命名空間)）。
