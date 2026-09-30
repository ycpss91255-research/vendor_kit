# r138 審查：script/check_typography.py

範圍：`diff -u doc/decisions/_backup/script_check_typography.pre_r138.md script/check_typography.py`（任務指定的 `script_check_typography.py.pre_r138.md` 不存在，實際備份檔名沒有 `.py`）。改動只有 3 行：docstring 的固定欄清單（第 12 行）、`CSV_FIELDS`（第 37 行）、`TEXT_FIELDS`（第 38 行）。

## 必改

無。

- 已定案（map #78）：這次改動只是跟著 CSV 欄位精簡縮小掃描欄，沒有碰到 #78「Decisions so far」任何一條。
- 對外承諾：沒有改 01／02／03／04 的內容。
- 做完沒：ask 對本檔的要求是「掃描的 CSV 文字欄改成 disposition、situation、message、next_step」。第 38 行 `TEXT_FIELDS` 已經是這四欄；docstring 第 12 行的固定欄已經拿掉 invariant、details；檔內 grep `note|invariant` 沒有殘留（第 54 行的 `details` 是 HTML 標籤 `<details>`，跟 CSV 欄位無關）。docstring 第 26 行引用的「check_messages.py 的規則 6」在新版 check_messages.py 第 13 行還是 next_step 那條，編號沒錯。
- 連結：diff 沒有新增或改動連結。
- 本機執行 `python3 script/check_typography.py` 結束碼是 0。

## 建議

1. 位置：script/check_typography.py 第 37 行 `CSV_FIELDS`。
   問題：這個常數在整個 script/ 和 script/test/ 裡都沒人用（grep `CSV_FIELDS` 只找到定義這一行）；`_csv_rows` 是從實際的表頭找 `TEXT_FIELDS` 的位置。這次跟著改了內容，但它是死碼，而且跟 check_messages.py 的 `FIELDS` 是兩份表頭，之後可能一份改了另一份沒改。
   建議：刪掉這個常數；要檢查表頭就留給 check_messages.py 的 `FIELDS`（它是唯一的檢查點）。
   證據：script/check_typography.py:37；script/check_messages.py:34；`grep -n CSV_FIELDS script/*.py script/test/*.py` 只命中 check_typography.py:37。

2. 位置：script/test/test_check_terms.py 第 42 行（不是這一輪列出的改檔，但 ask 要求「跑 unittest 全部要過」）。
   問題：`python3 -m unittest discover -s script/test` 有 1 個失敗：`test_check_terms.CsvTest.test_csv_text_fields_scanned` 還期望會掃到 `VK0001:note`，但 check_terms.py 第 113 行的 `CSV_TEXT_FIELDS` 已經拿掉 note。這個失敗不在本檔，但會讓 ask 的驗收條件不成立。
   建議：把這支測試加進這一輪的改檔，期望值改成 `["VK0001:situation", "VK0001:message"]`，fixture 也拿掉 note 欄。
   證據：script/test/test_check_terms.py:42；script/check_terms.py:113；unittest 輸出 `FAILED (failures=1)`。
