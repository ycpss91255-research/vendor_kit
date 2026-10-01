# r145 審查：script/check_context.py

## 必改

（無）diff 只動第 5、44、46 行：拿掉 `name != "ins"` 放行、改 docstring 與錯誤訊息，符合 ask 第 2 點；沒有新增連結；不涉 01／02 承諾與 map #78 定案。

## 建議

- 第 5 行 docstring：「不寫 HTML 錨點」與「不准任何 HTML 標籤」語意重疊，可合併成「不寫目錄；不准任何 HTML 標籤（含 `<ins>`，名詞改連 GLOSSARY.md 分群）」。證據：script/check_context.py:5。
