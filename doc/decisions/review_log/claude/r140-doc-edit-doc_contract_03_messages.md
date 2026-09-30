# r140 doc-edit 審查：doc/contract/03_messages.md

範圍：`diff -u doc/decisions/_backup/doc_contract_03_messages.pre_r140.md doc/contract/03_messages.md`，只有一處改動：第 82 行 `` `失敗`或留空 `` → `` `失敗` 或留空 ``。

## 必改

（無）

- 已定案（map #78）：只補一個空白，沒有碰任何定案項。
- 對外承諾：`disposition` 的值（`需人處理`、`失敗`、留空）沒變，只動了反引號外的空白；介面不變。
- 做完沒：`check_typography.py doc/contract/03_messages.md` 回 OK（rc=0）。用 regex 掃反引號外側緊鄰漢字的地方，只剩內容本身含中文的行內程式碼（第 62 行 `<中文本文>`、第 82 行 `需人處理`），不是邊界缺空白。ask 第 2 項只動 04，03 沒有要做的。
- 連結：diff 沒有新增或改動連結。

## 建議

（無）
