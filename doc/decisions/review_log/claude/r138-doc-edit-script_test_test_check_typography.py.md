# r138 審查：script/test/test_check_typography.py

範圍：`doc/decisions/_backup/script_test_test_check_typography.pre_r138.md`（任務寫的 `...check_typography.py.pre_r138.md` 不存在；這份內容跟 `git show HEAD:` 一致）對現行檔的 diff。

## 必改

無。

- 已定案（map #78）：diff 只改測試夾具與測試，沒碰對外文件，也沒有違反任何定案。
- 對外承諾：沒動 01／02／03／04。
- 做完沒：`FIELDS`（第 21 行）已對齊新表頭 `code,status,level,disposition,situation,message,next_step`，和 `script/check_typography.py:37` 的 `CSV_FIELDS` 一致；`good_rows`（第 29–35 行）拿掉了 invariant／details／note；`test_csv_fixed_columns`（第 207–216 行）刪了 details／invariant 兩行；`CsvTest` 的 docstring 與 `test_text_columns_scanned`（第 220–223 行）改成四個文字欄，和 `TEXT_FIELDS`（check_typography.py:38）一致；`test_csv_fix_keeps_format`（第 230–245 行）把 note 換成 situation。檔內已經沒有 note／invariant／details（grep 無結果）。`python3 -m unittest script/test/test_check_typography.py`：26 個測試全過。
- 連結：diff 沒有新增或改動連結。

## 建議

1. 位置：`CsvTest`（第 219 行起）。問題：拿掉 note 之後，沒有測試能擋住有人把 note（或其他非文字欄）加回 `TEXT_FIELDS`，也沒有測試確認表頭多出舊欄時工具的行為。建議：加一個測試，寫一份多了 `note` 欄、欄內有違規字串的 CSV，斷言 check_typography 不報這一欄（或斷言報表頭錯，看工具預定的行為），把「只掃四個文字欄」鎖住。證據：`script/check_typography.py:433` 用 `header.index(f) for f in TEXT_FIELDS if f in header` 挑欄，多出的欄會被默默略過。
2. 位置：`test_csv_fix_keeps_format`（第 233、243 行）。問題：原本 note 和 message 是兩個不同的文字欄，現在改到 situation，會蓋掉 `good_rows` 裡 VK0002 原本的 situation「第 2 次重試」。意思沒錯，只是讀的人要回頭看夾具才知道原值被覆寫。建議：可以改用 `disposition` 或 `next_step`，這兩欄在 VK0002 原本是空的，就不必覆寫既有值；維持現狀也可以。證據：`script/test/test_check_typography.py:33-34`。
