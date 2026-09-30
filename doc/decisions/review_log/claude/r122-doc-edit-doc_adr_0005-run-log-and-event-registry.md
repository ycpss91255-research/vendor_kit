# r122 doc-edit 審查：doc/adr/0005-run-log-and-event-registry.md

diff 範圍：只有第 3 行一處，「CI 檢查腳本」→ `just vendor_kit test`。

## 必改

（無）

- 已定案：改法符合 discussion_queue.md 定案第 32 條（第 58 行），沒有違反其他條。
- 對外承諾：只換了名稱，沒有動 01／02 的承諾或 03／04 的介面。
- 做完沒：用 grep 查過全檔，沒有殘留 `check.sh`、「CI 檢查腳本」、`ci/`、「五檔」；本檔沒有薄殼檔清單，不用拿掉 `ci/check.sh`。
- 連結：diff 沒有新增或改動連結（第 3 行的兩個連結 `02_invariants.md#4-永不靜默失敗`、`03_messages.md#結束碼` 跟改前一樣）。

## 建議

1. 位置：第 3 行「後續檢查（`sync`、`just vendor_kit test`、下一個可寫 recipe）」。
   問題：同一個括號裡，`sync` 只寫子命令名，`test` 卻寫完整指令，寫法不一致（不變量 8：一個概念一種寫法）。
   建議：改成「（`sync`、`test`、下一個可寫 recipe）」；或兩個都寫完整的 `just vendor_kit sync`、`just vendor_kit test`。
   證據：doc/adr/0005-run-log-and-event-registry.md:3；GLOSSARY.md:220 的條目名是 `sync`，GLOSSARY 新條目也叫 `test`。
