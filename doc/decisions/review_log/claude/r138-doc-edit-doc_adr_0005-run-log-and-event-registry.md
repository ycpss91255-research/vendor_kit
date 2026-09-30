# r138 doc-edit 審查：doc/adr/0005-run-log-and-event-registry.md

範圍：備份 `doc/decisions/_backup/doc_adr_0005-run-log-and-event-registry.pre_r138.md` 不存在，改用 `git diff HEAD -- doc/adr/0005-run-log-and-event-registry.md`，結果是空的：這一輪沒動本檔。

逐項核對：
1. 已定案（map #78）：沒有 diff，所以沒有違反。
2. 對外承諾：沒有 diff，01／02／03／04 的承諾都沒改。
3. 做完沒：ask 裡跟本檔有關的只有第 2 點，也就是把連到 `03_messages.md#vk0002`／`#vk0005` 的連結改成連 CSV。用 grep 查 `vk0002|vk0005|VK0002|VK0005`，本檔一處都沒有，所以不用改；`csv`、`invariant`、`details`、`note` 也都沒出現。本檔沒有該做而漏掉的部分。
4. 連結：沒有新增或改動的連結。現有的錨點也用 `script/check_review_pages.py` 的 `slug()` 比對過，都還在：`03_messages.md#結束碼`、`03_messages.md#訊息`（03 現在的標題 slug 是 03-訊息與錯誤碼總表／目錄／結束碼／輸出／訊息）、`02_invariants.md#4-永不靜默失敗`，`0004-vk-recipe-interface-and-write-boundary.md` 檔案也在。

## 必改

（無）

## 建議

- 位置：doc/adr/0005-run-log-and-event-registry.md 第 24 行「訊息見[訊息總表](../contract/03_messages.md#訊息)」
  - 問題：現在 03 的 `## 訊息` 節不再逐碼列內容（03_messages.md 第 66 行：「只寫在[訊息表](03_messages.csv)…本頁不再列一份」）。讀者照連結點過去，還要再跳一次才看得到 just／Docker／Podman 的前置檢查訊息。連結文字「訊息總表」和 03 的標題「訊息與錯誤碼總表」也不一樣。
  - 建議：這不是 ask 要求的項目，錨點也還有效，可以不改。要改的話，改成「訊息見[訊息表](../contract/03_messages.csv)」，跟 ask 第 2、4 點的寫法一致。
  - 證據：doc/adr/0005-run-log-and-event-registry.md:24；doc/contract/03_messages.md:66
