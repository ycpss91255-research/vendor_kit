# r124 審查：script/check_review_pages.py

備份 `doc/decisions/_backup/script_check_review_pages.py.pre_r124.md` 不存在，改用 `git diff HEAD`。改動只有兩處說明文字（第 5 行 docstring、第 82 行錯誤訊息）。

## 必改

（無）已定案、對外承諾、連結三項都沒問題：diff 沒有新增連結，只改了說明字串；unittest 23 項全過。

## 建議

- 位置：script/check_review_pages.py 第 79–82 行附近的 check_page 迴圈
  - 問題：原檔本來就沒有 regex 在比對引用格式，所以舊寫法「依 [頁名](連結#錨點) 第 N 條」現在仍然會通過 lint。ask 寫「若有 regex 才改」，嚴格說不算漏做；但定案是「整段都是超連結」，沒有 lint 擋的話，舊寫法之後會再冒出來（記憶規則：重複出現的問題寫進 lint）。
  - 建議：新增檢查 `re.search(r"\]\([^)]+\)\s*第\s*\d+\s*條", line)`，命中就報「引用條目時『頁名第 N 條』整段放進連結：依 [頁名第 N 條](連結#錨點)」；再到 script/test/ 加一個正例、一個反例。
  - 證據：script/check_review_pages.py:81-82（只檢查「出處：」行）；grep 找不到任何比對「第 N 條」的 regex。
