# r138 doc-edit 審查：doc/contract/04_interface.md

範圍：`diff -u doc/decisions/_backup/doc_contract_04_interface.pre_r138.md doc/contract/04_interface.md`，共三處，都是 `[訊息](03_messages.md#vk0005|#vk0002)` 改成 `[訊息](03_messages.csv)`（第 35、39、181 行）。

## 必改

無。

- 已定案（#78 Decisions so far）：三處只換連結目標，沒有動到結束碼、訊息 code、處置或指令，不違反 #91、#95、#96、#101 等任何一條。
- 對外承諾：訊息內容與結束碼 `2` 不變；VK0002、VK0005 仍在 `doc/contract/03_messages.csv`（各一列），04 引用的訊息都還在。
- 做完沒：ask 第 2 點要求 04 改掉 `#vk0002`／`#vk0005`，已改完；`grep '#vk'` 在 04 無殘留。第 3、4 點的條列與「連結文字＋括號路徑」寫法在 04 沒有出現（`grep '(doc/'`、`grep '後者'` 無結果）；第 1、5 點不涉及 04。
- 連結：`03_messages.csv` 存在；同一行用到的 `03_messages.md#結束碼`，用腳本從 03.md 標題算出的 slug 是 `結束碼`，與錨點相符。寫法與 04 其他處的 `[訊息](03_messages.csv) \`VKnnnn\`` 一致。

## 建議

無。
