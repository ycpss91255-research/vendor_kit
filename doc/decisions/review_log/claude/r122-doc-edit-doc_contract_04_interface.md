# r122 doc-edit 審查：doc/contract/04_interface.md

範圍：`diff -u doc/decisions/_backup/doc_contract_04_interface.pre_r122.md doc/contract/04_interface.md`

四項檢查的結果：
- 已定案：沒有違反。第 5 條（入口含 `check.sh`）已被第 32 條取代。
- 對外承諾：01、02 沒動；04 只改了 ask 要求的部分；`--dist` 從「只有長」清單拿掉，這是 `check.sh` 改成 `test dist` 必然跟著改的。
- 做完沒：ask 的 1～4 項都做了（開頭句逐字相符；入口剩兩個；節名、兩種用法、覆蓋原則、結束碼句、目錄連結、指令清單都改了；just 列兩句與註的原因都補了）。04 內 `check.sh`、「CI 檢查腳本」、`--dist` 殘留數為 0。
- 連結：`#檢查test`、`#ci-模式`、`03_messages.md#結束碼`、`03_messages.md#訊息`、`02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口` 用腳本算 slug 比對過，全部存在。repo 內沒有現行文件還連到舊錨點 `#ci-檢查腳本`（只在 doc/research 的歷史檔）。check_terms、check_context、check_review_pages 都 OK。

## 必改

（無）

## 建議

1. **位置**：04「## CI 模式」（第 257–263 行）、「## 檢查（test）」（第 243–255 行）
   **問題**：這一輪 ADR-0004 第 22 行改成「`just vendor_kit test` 自己開啟 CI 模式」，但 04 的 CI 模式只寫「環境變數 `CI` 有值…就是 CI 模式」。本機不設 `CI` 跑 `just vendor_kit test`：照 04 不是 CI 模式，照 ADR-0004 是（例如有本機覆寫時會以 `2` 結束）。這是使用者看得到的行為，對外頁與 ADR 對不上。另外，定案第 32 條寫的是「CI 模式照舊由環境變數 `CI` 判斷」，跟「test 自己開啟」字面上也有落差。
   **建議**：在「## 檢查（test）」或「## CI 模式」補一句「`test` 一律以 CI 模式執行」（或等效寫法），讓 04 與 ADR-0004 一致；如果維護者的意思只是「照環境變數」，就改回 ADR-0004 那句，別動 04。
   **證據**：doc/adr/0004-vk-recipe-interface-and-write-boundary.md:22；doc/contract/04_interface.md:259；discussion_queue.md 已定案第 32 條（第 52 行）

2. **位置**：04「## 指令」底下的「清單裡的名詞見名詞表」（第 95–104 行）
   **問題**：指令清單新增了 `test`／`test dist`，GLOSSARY 也有 `test` 條目（GLOSSARY.md:125），但名詞連結清單沒有它；第 245 行 `<ins>`test`</ins>` 標了底線卻沒有連結可以查。
   **建議**：在清單補 `- [`test`](../../GLOSSARY.md#repo-內的檔與狀態)`（連到條目目前所在的分群）。
   **證據**：doc/contract/04_interface.md:91-92、95-104、245；GLOSSARY.md:88、125

3. **位置**：04 第 252–253 行 vs GLOSSARY.md:126
   **問題**：04 寫「只檢查工具交付的內容」，GLOSSARY 寫「只檢查工具在 `dist/` 交付的內容」。兩邊範圍的寫法不一樣，讀者會不確定是不是只看 `dist/`。另外「跑全部檢查」到底包不包含 `dist` 那一種檢查，兩邊都沒講。
   **建議**：兩處用同一種寫法（例如都寫「工具在 `dist/` 交付的內容」），並講明「全部」包不包含 `dist` 的檢查。
   **證據**：doc/contract/04_interface.md:252-253；GLOSSARY.md:126-127

4. **位置**：discussion_queue.md 已定案第 5 條（第 17 行）
   **問題**：第 5 條還寫著入口有 `check.sh`，已經被第 32 條取代，但沒有標出來。第 27 條被取代時有標「（已由第 28 條取代）」，這裡的標法不一致；之後的審查可能會拿第 5 條來擋 04。
   **建議**：第 5 條補「（入口的 `check.sh` 已由第 32 條取代）」。這個改動不在本檔，交給主對話處理。
   **證據**：doc/decisions/review_log/discussion_queue.md:17、44、52
