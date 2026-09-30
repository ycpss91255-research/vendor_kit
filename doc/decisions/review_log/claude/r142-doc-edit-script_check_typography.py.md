# r142 審查：script/check_typography.py

對照範圍：map #78「Decisions so far」、01、02、GLOSSARY.md、03_messages.csv 表頭、check_messages.py、script/README.md、test_check_typography.py。
實測：`python3 script/check_typography.py` → OK（8 個檔）；`python3 -m unittest discover -s script/test` 全過。

## 必改

無。這一輪只改 docstring 的固定欄清單（加 exit_code）、CSV_FIELDS、TEXT_FIELDS（加 description），跟 03_messages.csv 第 1 行表頭、check_messages.py 第 5–16 行、script/README.md 第 93、156 行一致；沒有違反 #78 任何定案，也沒動 01／02／03／04 的對外介面。message 不准含中文（check_messages.py 第 11–12 行、README 第 98 行），規則 1、2 都要有中文字元才會觸發，所以英文 message／next_step 不會誤報，`--fix` 也不會動它們。

## 建議

1. 位置：script/check_typography.py 第 40–42 行 `CSV_FIELDS`
   問題：整支程式沒有任何地方用到 `CSV_FIELDS`（`grep -n CSV_FIELDS script/` 只命中定義本身）；表頭的唯一出處是 check_messages.py 的 FIELDS。這一輪照樣手動同步一份死常數，下次加欄時容易漏改而不會有任何測試發現。
   建議：刪掉 `CSV_FIELDS`；要保留就改成 `from check_messages import FIELDS`，不要自己抄一份。
   證據：script/check_typography.py 第 40–42、452 行（第 452 行只用 TEXT_FIELDS）。

2. 位置：script/check_typography.py 第 11–14 行 docstring
   問題：script/README.md 第 156 行寫了「英文的 message 與 next_step 仍會掃描，但不會因英文排版本身誤報」，docstring 沒寫；第一次看 TEXT_FIELDS 含 message、next_step 的人會以為英文欄也要照中英混排規則改。
   建議：第 14 行後補一句：「message、next_step 是英文（check_messages.py 不准含中文），規則 1、2 只在有中文字元時觸發，所以照掃不會誤報。」
   證據：script/README.md 第 156 行；script/check_messages.py 第 11–12 行。

3. 位置：script/check_typography.py 第 29 行 docstring、第 469–473 與 489–491 行的 next_step 對齊檢查
   問題：message 已不准含中文，`--fix` 不可能再改動 message 或 next_step，這段檢查實際上只有在 check_messages.py 已經報錯的 CSV 才會觸發。留著無害，但 docstring 第 29 行讀起來像是日常情況。
   建議：保留程式碼（當防線），docstring 第 29 行改成「message 與 next_step 是英文，--fix 照理不會動到；萬一修正後 next_step 不再逐字出現在 message 裡，照樣報錯（check_messages.py 的規則 6）。」
   證據：script/check_messages.py 第 14 行（規則 6）、第 11–12 行。

4. 位置：TEXT_FIELDS（第 43 行）與 script/test/test_check_typography.py 的 `CsvTest.test_chinese_text_columns_scanned`
   問題：TEXT_FIELDS 有 5 欄，但測試這一輪從「disposition、situation、message、next_step 都掃」縮成只測 situation、description；disposition（中文值「需人處理」「失敗」）是否仍被掃描已沒有測試保護，把它從 TEXT_FIELDS 拿掉也不會有測試失敗。message、next_step 仍被掃描這件事同樣只剩「英文不誤報」的反例，沒有正例。
   建議：測試迴圈改成 `["disposition", "situation", "description"]`（中文欄正例），另外保留一個 message 放中文混排時仍會被報的正例（跟英文不誤報的反例成對）。
   證據：script/test/test_check_typography.py CsvTest（`git diff HEAD` 中 `test_text_columns_scanned` 被改名並縮減欄位）；script/check_typography.py 第 43 行。
