# r138 審查：script/test/test_check_messages.py

範圍：`diff -u doc/decisions/_backup/script_test_test_check_messages.pre_r138.md script/test/test_check_messages.py`（備份檔名沒有 `.py`）。`python3 -m unittest script/test/test_check_messages.py` 跑 36 個測試，全過。

查過的四項：
1. 已定案：map #78「Decisions so far」裡沒有一條講到 CSV 欄位或測試，diff 沒有違反任何一條。
2. 對外承諾：這個檔是內部測試，沒有改 01～04 的內容。
3. 做完沒：fixture 已拿掉 note、invariant、details；02_invariants.md 與 `### VK0001` 節的 fixture 刪了；欄數改成 6／7；strict parse 那一列改成 7 欄；空白、公式、HTML、Markdown、角括號的測試改用 situation；retired 測試改用 next_step；DetailsTest 與 test_invariant 刪了；連 03_messages.md 的三個舊測試併成 test_code_link_to_md_goes_to_csv，對上 check_messages.py:224；test_good_links 用了 ask 指定的「[訊息](03_messages.csv) `VKnnnn`」寫法。`grep -nE 'note|invariant|details|###'` 沒有結果。
4. 連結：diff 裡的連結都寫在暫存目錄的 fixture 裡。它們對應的 repo 路徑 `doc/contract/03_messages.csv` 存在，從 `doc/adr/` 連過去的 `../contract/03_messages.csv` 也解析得到，而且沒有帶 #錨點，不用算 slug。

## 必改

（無）

## 建議

- 位置：script/test/test_check_messages.py:255-259（RefTest.test_code_link_to_md_goes_to_csv）
  問題：新規則「連結文字是代碼時不准連 03_messages.md」只測了會失敗的情況。連結文字不是代碼的情況，例如 `[訊息表怎麼讀](03_messages.md#訊息表怎麼讀)`，沒有測試證明它會通過。檔頭寫的是「每條一正一反」。
  建議：在 test_good_links 或新的測試裡加一條，把非代碼文字連到 03_messages.md，並 assert_ok。
  證據：script/test/test_check_messages.py:1；script/check_messages.py:224。

- 位置：script/test/test_check_messages.py:117-119（FormatTest.test_header）
  問題：這一輪刪了 note、invariant、details 三欄，但沒有測試直接證明舊的 10 欄表頭會被擋。現在的 test_header 只把最後一欄改名。
  建議：加一個 subTest，用 `HEADER + ["note", "invariant", "details"]` 當表頭，assert_fail("表頭要逐字等於")。
  證據：script/check_messages.py:34、91。
