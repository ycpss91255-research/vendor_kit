# Triage 標籤

skills 用五個標準 triage 角色描述 issue 狀態。這個檔把角色對應到本 repo issue tracker 實際使用的標籤字串。

| mattpocock/skills 的標籤 | 本 tracker 的標籤 | 意思 |
| ------------------------ | ------------------ | ---- |
| `needs-triage`           | `needs-triage`     | 等維護者評估；要維護者拍板的問題（設計取捨、契約要不要改）也貼這個 |
| `needs-info`             | `needs-info`       | 等回報者補資料 |
| `ready-for-agent`        | `ready-for-agent`  | 規格完整，可交給 AFK agent 實作 |
| `ready-for-human`        | `ready-for-human`  | 需要人來實作（判斷、外部存取、手動測試） |
| `wontfix`                | `wontfix`          | 不會處理 |

skill 提到某個角色時（例如「apply the AFK-ready triage label」），就用表中對應的標籤字串。

## 已刪除、不再使用

- `backlog`：已刪除。原本掛在已關閉的 #11、#13；刪標籤時 GitHub 自動移除。
- `upstream`：已刪除。
- `needs-decision`：已刪除。原本標「等維護者拍板」，已併入 `needs-triage`；刪之前，掛著它的 open issue 已改標 `needs-triage`（歷史）。

其他標籤（`bug`、`documentation`、`enhancement`）是 GitHub 預設的分類標籤，跟 triage 狀態無關，維持不動。
