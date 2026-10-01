# 取消 CI 模式，嚴格檢查只綁在 test

> Status: accepted
>
> Serves: [不變量 3：自動化只碰不進 git 的東西](../contract/02_invariants.md#3-自動化只碰不進-git-的東西)、[不變量 12：依對外承諾無法唯一判定就停，任何環境一律採最嚴格行為](../contract/02_invariants.md#12-依對外承諾無法唯一判定就停任何環境一律採最嚴格行為)

以環境變數判定 CI 模式，會讓同一個 recipe 在不同地方改變行為；`CI=0`、`CI=false` 等值也容易被不同實作誤判。VK 因此取消 CI 模式、不讀環境變數 `CI`，每個 recipe 在任何環境都採相同且最嚴格的行為；需要集中執行的嚴格檢查只屬於 `just vendor_kit test`，因為穩定性優先於依環境提供不同便利。

## Considered Options

- **保留 CI 模式，依環境變數 `CI` 分流**：自動化流程不必改呼叫方式，但環境偵測讓相同 recipe 的結果不再只由輸入與狀態決定，`CI=0`、`CI=false` 也可能被誤判。
- **保留 CI 模式，但只加強、不放寬行為**：避免在 CI 降低保護程度，卻仍讓同一個 recipe 因執行環境而有兩套結果，無法符合任何環境一律採相同行為的要求。
- **只在 `test` 執行嚴格檢查（採用）**：嚴格與否由使用者明確呼叫的具名 recipe 決定，不靠環境推測；本機與自動化流程呼叫同一個 `just vendor_kit test`，得到相同結果。

## Consequences

- `test` 不寫[追蹤檔](../../GLOSSARY.md#repo-內的檔與狀態)。它發現基準版落後版本鎖定行時印 `warn[VK0014]`、以結束碼 `1` 結束；發現本機覆寫時印 `error[VK0032]`、以結束碼 `2` 結束。
- `dev` 開啟本機覆寫後，一般 recipe 仍照常執行，並在 stdout 記錄採用了本機覆寫；只要該 recipe 的承諾已完成且沒有其他診斷，就以結束碼 `0` 結束。只有 `test` 會因本機覆寫而擋下。
- VK 不另定 CI 專用規則，也不自行追蹤新版、commit 或開 PR。自動化流程要驗證安裝目錄時明確執行 `just vendor_kit test`；新版追蹤交給 Renovate。
- 這項決議取代 [ADR-0004](0004-vk-recipe-interface-and-write-boundary.md) 中的 CI 模式、依 `CI` 分流，以及 CI 模式附加嚴格規則；ADR-0004 的 recipe 介面、寫入邊界與警告結束碼決議仍然有效。
