# r142 審查：script/test/test_check_typography.py

範圍：跟 `doc/decisions/_backup/script_test_test_check_typography.pre_r142.md` 比對的 diff。`python3 -m unittest script/test/test_check_typography.py`：36 個測試全過。

## 已定案（#78 Decisions so far、01、02）

沒有違反。這個檔是內部測試，不碰 01、02 的承諾與不變量，也不動 03、04 的對外介面。FIELDS 的順序跟 ask 一致；good_rows 的 exit_code 對應（error→2、warn→1）符合 #117；message 是英文、description 是中文，符合維護者「本文寫英文、CSV 多一欄中文說明」的要求。

## 必改

1. **位置**：`script/test/test_check_typography.py:270`（CsvTest docstring）、`:272-278`（`test_chinese_text_columns_scanned`）
   - **問題**：這一輪把 `disposition` 從掃描欄的測試拿掉了（原本的迴圈是 `["disposition", "situation", "message", "next_step"]`），但工具還在掃它：`script/check_typography.py:43` 是 `TEXT_FIELDS = ("disposition", "situation", "message", "description", "next_step")`。`script/README.md:156` 也寫明 CSV 的文字欄包含 `disposition`。結果是 disposition 的掃描沒有測試保護，docstring 寫的「中文文字欄 situation、description」也跟工具和 README 對不上。之後有人從 TEXT_FIELDS 刪掉 disposition，測試抓不到。
   - **建議**：迴圈改成 `["disposition", "situation", "description"]`，docstring 改成「CSV 的中文文字欄 disposition、situation、description，以及英文 message、next_step。」
   - **證據**：`script/check_typography.py:43`；`script/README.md:156`；`doc/decisions/_backup/script_test_test_check_typography.pre_r142.md` 裡原本的 `test_text_columns_scanned`。

## 建議

1. **位置**：`script/test/test_check_typography.py:280-285`（`test_english_message_and_next_step_pass`）
   - **問題**：這個測試只驗「英文不誤報」（檢查回 0），沒驗 `--fix` 不會動英文的 message 與 next_step。ask 要的是「照掃但不得誤報」，而對 CSV 誤改比誤報更危險：改了 message 會讓 next_step 不再逐字出現在 message 裡。另外，`script/README.md:156` 寫「英文的 message 與 next_step 仍會掃描」，但沒有任何測試能證明這兩欄確實在掃描。
   - **建議**：（a）比照 `ExcludeTest.test_csv_fixed_columns`，跑 `--fix` 後比對 CSV 的位元組沒變。（b）加一個反例：在 message 或 next_step 放中英相鄰的字串（例如 `VK設定`），預期工具報錯。它證明兩欄仍在掃描。如果不想讓測試依賴 message 可以有中文（check_messages 禁止），至少要做 (a)。
   - **證據**：`script/check_typography.py:43`；`script/README.md:156`；`script/check_messages.py:184`。

2. **位置**：`script/test/test_check_typography.py:282`
   - **問題**：測試值 `"Run command2 (test): <next_step>."` 用了 `<next_step>` 這個占位符名稱。03 的 CSV 並沒有這個占位符，而欄名跟占位符同名，第一次讀的人不容易分清楚。
   - **建議**：改用 03 實際有的占位符形式，例如 `"Run again (test): <command_with_y>"`，next_step 同步改成 `<command_with_y>`。
   - **證據**：`doc/contract/03_messages.csv` 第 3 行（VK0002 的 next_step 是 `<command_with_y>`）。
