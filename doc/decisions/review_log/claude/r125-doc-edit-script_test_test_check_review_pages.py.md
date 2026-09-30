# r125 審查：script/test/test_check_review_pages.py

## 必改

無。ask 第 5 項要的正例（第 74–78 行）、反例（第 80–85 行）、反引號內不擋（第 87–90 行）都有；`python3 -m unittest discover -s script/test` 26 項全過。diff 沒有新增連結，不違反 #78 已定案決定，不動對外承諾。

## 建議

1. 位置：第 85 行。問題：反例只斷言「依 [頁名第 N 條](連結#錨點)」，這段字串「出處」行的錯誤訊息也有（script/check_review_pages.py 第 85 行），分不出是哪條規則擋的。建議：改斷言舊寫法規則專有的字串，例如 `self.assertIn("引用條目的舊寫法", out)`。證據：script/check_review_pages.py 第 85、90 行。
2. 位置：第 74–90 行。問題：ask 第 4 項說 README.md 也要檢查，測試只覆蓋 doc/contract/0N_*.md。建議：加一個 README.md 寫舊寫法、預期 code 1 的案例。證據：ask 第 4 項；setUp 第 28 行只寫了乾淨的 README。
3. 位置：第 90–92 行。問題：類別結尾與 `if __name__` 之間只空一行，本檔其他地方都照 PEP 8 空兩行。建議：補一行空行。證據：第 91 行。
