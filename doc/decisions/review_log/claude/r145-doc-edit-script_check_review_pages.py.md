# r145 審查：script/check_review_pages.py

基準：備份 pre_r145 不存在，用 `git diff HEAD -- script/check_review_pages.py`。實跑 `python3 script/check_review_pages.py` 結果是 OK（掃 5 個檔），`test_check_review_pages` 14 個測試全過。

## 必改

無。ask 第 2 點列的行（8、21、41、78、94、145）都改了：TAG 與 RAW_ANGLE 不再放行 `<ins>`，行內程式碼仍然排除，`\<…\>` 仍然靠 `(?<!\\)` 排除。diff 沒動對外頁、不變量或 03／04 介面，也沒新增或改動連結。

## 建議

- 第 21 行 docstring 第 9 條「<ins> 也一樣要跳脫」：這句會讓人以為把 `<ins>` 寫成 `\<ins\>` 就能用。實際上 `<ins>` 是 3a 禁的標籤，名詞要改連到 GLOSSARY。建議改成「連結文字裡任何沒跳脫的 <…> 都會報錯（含 <ins>）」，或者直接刪掉這句。證據：script/check_review_pages.py:21、:8。
- 第 142 行 `sorted({t for t in TAG.findall(...)})`：拿掉過濾以後，這個 comprehension 已經沒有作用。建議改成 `sorted(set(TAG.findall(...)))`。證據：script/check_review_pages.py:142。
