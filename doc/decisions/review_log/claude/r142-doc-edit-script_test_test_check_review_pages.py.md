# r142 審查：script/test/test_check_review_pages.py

對照：`diff -u doc/decisions/_backup/script_test_test_check_review_pages.pre_r142.md script/test/test_check_review_pages.py`（ask 指定的 `.py.pre_r142.md` 不存在，實際備份檔名是 `script_test_test_check_review_pages.pre_r142.md`）。`python3 -m unittest discover -s script/test` 全過；`check_review_pages.py` 對現行頁 OK。

定案核對（map #78 Decisions so far）：這是內部測試檔，沒動 01／02 承諾、沒動 03／04 對外介面；沒有違反任何一條定案。

## 必改

1. **位置**：`test_messages_csv_commands_must_be_defined_earlier`，fixture 第 80、82 行（`VK0001,active,warn,1,needs_human,…`、`VK0002,active,error,2,needs_human,…`）
   **問題**：fixture 用新表頭，但 `disposition` 值 `needs_human` 不是合法值；warn 列的 disposition 也不准有值。fixture 表示的是一份按 check_messages.py 不合法的訊息表，跟真正的訊息表格式對不上。
   **建議**：VK0001（warn）的 disposition 改成空白：`VK0001,active,warn,1,,開發模式中…`；VK0002 改成 `需人處理`：`VK0002,active,error,2,需人處理,…`（它有 next_step，符合「需人處理必有 next_step」）。
   **證據**：script/check_messages.py:13（「disposition 只准『需人處理』『失敗』或空白；warn 一律空白」）、:41（`DISPOSITIONS = {"需人處理", "失敗", ""}`）、:185-188；doc/contract/03_messages.csv:2-3（實際用 `失敗`、`需人處理`）。

## 建議

1. **位置**：同一個測試，第 89-92 行的斷言 ``指令 `just vendor_kit upgrade <repo> -z and retry.` 用了 -z``
   **問題**：message 改英文後，`CMD_CSV`（`just vendor_kit [ -~]*`）會一直取到欄尾，把後面的英文句子也當成指令。這個測試把「指令」後面接著 ` and retry.` 寫成預期輸出，等於把這個取錯的行為固定下來。現行 CSV 已經出現同樣的情況：VK0001 取到 `… <repo>@<tag> (pulling uses the host's Docker credentials).`，VK0003 取到 `… -y locally; then commit and push.`。只要英文句子裡出現前面是空白的 `-x`／`--xxx` 字樣，就會誤報；錯誤訊息裡的指令也不對。check_review_pages.py:193 的註解（「取到第一個非 ASCII 字（中文、全形標點）或欄尾」）是在 message 還是中文時寫的，現在已經不準。
   **建議**：一種做法是在 check_review_pages.py 讓 CSV 指令停在第一個不是選項、占位符、`@<tag>` 或指令詞的字（或停在 `.`、`;`、`,`、`(` 之類的句中標點），測試斷言改成 ``指令 `just vendor_kit upgrade <repo> -z` 用了 -z``，再補一列英文句子，確認指令後面接像 ` then rerun -- see logs` 這類文字時不會誤報。另一種做法是先保留現行行為，但在測試加註解，寫明取到欄尾是已知限制。不論選哪一種，都要一起更新 check_review_pages.py:193 的註解。
   **證據**：script/check_review_pages.py:193-194；doc/contract/03_messages.csv 的 VK0001、VK0003 的 message 欄（用 `c.CMD_CSV` 對 CSV 實跑，看得到取出的文字）。

2. **位置**：同一個測試，第 83 行的 `description` 值（`中文說明 just vendor_kit test --description-only`）與第 99 行 `assertNotIn("--description-only", out)`
   **問題**：這個斷言的意思是「description 欄不掃指令」，但只有註解第 72 行從反面說「掃 situation、message、next_step 三欄」，沒寫明 description 是刻意不掃的。第一次讀的人會以為漏掃。
   **建議**：把第 72 行註解改成「掃 situation、message、next_step 三欄（description 是給人讀的中文說明，不掃）；錯誤位置報 <檔>:<代碼>:<欄名>」。
   **證據**：script/test/test_check_review_pages.py:72、83、99；script/check_review_pages.py:195（`CSV_COMMAND_FIELDS`）。
