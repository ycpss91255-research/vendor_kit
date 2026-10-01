# r145 審查：script/test/test_mark_changes.py

這一輪沒有備份檔（pre_r145 不存在），`git diff HEAD -- script/test/test_mark_changes.py` 為空：本檔這輪沒改。ask 第 5 點針對的是「<ins> 放行」的測試，那類測試在 test_check_context.py／test_check_review_pages.py，本檔不需要改。本檔 grep 不到 `<ins>`、「名詞標記」或「不進 git」。`python3 -m unittest script/test/test_mark_changes.py` 通過。

## 必改

（無）

## 建議

- 位置：script/test/test_mark_changes.py（缺少檔頭的測試）
  - 問題：mark_changes.py 這輪改了產出檔頭註解（第 448、521 行附近：拿掉「底線 <ins> 是名詞標記」、「不進 git」改成「本檔進 git，定稿時一個 commit 刪除」），但沒有任何測試鎖住檔頭文字，之後退回舊說法也不會失敗。
  - 建議：加一個測試，對 build 產出的檔頭斷言不含 `<ins>`、不含「不進 git」。
  - 證據：`git diff HEAD -- script/mark_changes.py`；本檔 grep 不到「檔頭」相關斷言。
