# VK recipe 一行轉發，寫入邊界與 CI 紅燈清單封閉

同一個 `justfile` 裡會載入好幾個工具的命名空間，recipe 的語意一改，寫進使用者 CI 的呼叫不會報錯、只會靜默做另一件事；而 CI 裡沒有人能回答詢問，需要寫進 git 的檔只能紅燈（[不變量 3](../contract/02_invariants.md#3-自動化只碰不進-git-的東西)、[不變量 8](../contract/02_invariants.md#8-使用者介面不可取代寫法一致)）。所以每個 VK recipe 在進 git 的 `vendor.just` 裡只是一行轉發，規則全在引擎；CI 模式下一定紅燈的情境是一份封閉清單，往裡面加一項要改本檔，不由實作臨時決定。多工具、逐檔合併都會在中途失敗，守得住的是混合狀態可辨識（[不變量 4](../contract/02_invariants.md#4-永不靜默失敗)），所以可寫 recipe 的寫入時序固定。

## Considered Options

- **CI 模式只看 `CI` 有沒有設**：`CI=0`、`CI=false` 的環境會被誤判，本機習慣導出這個變數的人會突然失去詢問。
- **CI 模式下連 `update` 也停掉**：`update` 不寫任何檔，停掉它就沒辦法在 CI 查有沒有新版，而那正是它存在的理由。
- **紅燈條件改成開放式（CI 下任何警告都紅燈）**：「這個檔沒納管」「這個版本你拒絕過」都會擋下 pipeline，而它們都不是錯，使用者只會學會忽略 VK 的結束碼。
- **`gen/tools.just` 與 `cache/` 分兩次寫**：兩次之間中斷，就留下入口檔指著舊快取、看起來卻是好的 repo。
- **加 `init`／`diff`／`accept`／`rollback` 這類別名**：語意與既有 recipe 重疊，`diff`、`accept`、`rollback` 三件事 git 本來就做得到；不變量 8 要求每個介面都不可取代。
- **轉發行不進 git，改由啟動器現產**：fresh clone 在跑過啟動器之前沒有任何 `just` 入口，使用者第一步要打的就不是 `just`。

## Consequences

- `vendor.just` 進 git，fresh clone 直接有入口；代價是改轉發行等於改進 git 的檔，要走 `upgrade --engine` 重產薄殼。
- CI 紅燈只有五項，可以逐項寫成測試；清單外的警告不擋別人的 pipeline，也就不會被 `|| true` 整批關掉。
- `CI` 由 CI 服務自己設，使用者不必額外配置；本機把 `CI` 留在環境裡的人會拿到 CI 行為。
- 需要寫進 git 的情境各有固定訊息編號，改號等於改介面。[03 訊息與錯誤碼總表](../contract/03_messages.md)列了未完成導入（[訊息 6-13](../contract/03_messages.md#訊息)）、基準版落後（[訊息 6-5](../contract/03_messages.md#訊息)）與薄殼不符（[訊息 6-28](../contract/03_messages.md#訊息)）。
- 內部機制（之後搬到實作 issue）：
  - 轉發形狀：每個 recipe 一行 `<recipe> *args`，以 `[group('常用')]` 與 `[group('進階')]` 分段；轉發行不解讀參數、不判斷狀態。`vendor.just` 屬於進 git 的薄殼五檔（[不變量 6](../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)）。
  - `check.sh` 自己設 `CI=1`。`update` 在 CI 模式下仍然查 registry：它是唯讀 recipe，查詢就是它的用途。
  - CI 模式下一定以[結束碼 `2`](../contract/03_messages.md#結束碼)結束的封閉清單：薄殼不符、基準版落後、未完成導入、任何本機覆寫、需要改進 git 的檔。「這個檔沒納管」「這個版本你拒絕過」只提醒、不紅燈。
  - `sync` 的三種情境：未完成導入回 `2`（[訊息 6-13](../contract/03_messages.md#訊息)）；基準版落後版本鎖定行在本機只警告、CI 下回 `2`（[訊息 6-5](../contract/03_messages.md#訊息)）；快取逐檔指紋驗不過就重裝並警告，這完全落在 VK 自己的 `cache/`，不違反寫入邊界。
  - 可寫 recipe 的時序：
    1. 建執行紀錄。早於任何寫入、拉 image、起引擎；只有不寫檔、不拉 image、不起容器的前置檢查可以排在它之前。
    2. 建進度檔（`.tmp.<verb>.<id>.toml`、metadata 的 `[progress]`），早於第一個 repo 檔或 VK 狀態檔的寫入；`--dry-run` 不建。
    3. 不帶工具名、一次處理多個工具時，先對全部工具做完整預檢；任一項不過就整體不動，以 `2` 結束並列出每一個原因。
    4. 寫入。中途失敗照不變量 4 處理。
    5. 最後才改版本鎖定行：工具層的可寫 recipe 回 `2` 時，該工具的版本鎖定行不動。升引擎是明列例外，見 [ADR-0007](0007-host-thin-layer-and-shell-integrity.md)。
  - 可寫 recipe 開始前發現未完成的進度檔，先恢復再繼續；唯讀 recipe 只偵測、不自動恢復。
  - 入口檔 `gen/tools.just` 最後才寫，與 `cache/` 在同一個 apply 內原子替換，不會出現快取換了、入口檔還指著舊的；實作要多一層暫存目錄與替換步驟。
  - 工具交付的 `dist/just/<ns>.just` 每檔一個頂層命名空間，數量由工具自決，`<repo>.just` 必須存在；`gen/tools.just` 每個 `<ns>` 一行。`add` 在任何寫入之前檢查 `<ns>` 撞名（比對對象見 [04 使用者介面](../contract/04_interface.md#命名空間)）。
