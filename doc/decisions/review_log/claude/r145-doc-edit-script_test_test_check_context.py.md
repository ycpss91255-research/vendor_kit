# r145 審查：script/test/test_check_context.py

## 必改

無。diff 只新增 HtmlTest（<ins> 失敗、行內程式碼與程式碼區塊不算 HTML），符合 ask 第 5 點；沒有改到對外頁、沒有新增連結；6 個測試全過。

## 建議

1. 位置：script/test/test_check_context.py:64。問題：`assertIn("ins", out)` 太鬆，任何含 "ins" 的字串都能讓它通過。建議：改成 `assertIn("HTML", out)` 或 `assertIn("['ins']", out)`。證據：實跑 check_context 的輸出是「第 8 行用了 HTML ['ins']：不准任何 HTML 標籤…」。
2. 位置：script/test/test_check_context.py:66-68。問題：ask 第 2 點說跳脫的 `\<…\>` 照舊不算 HTML，但沒有測到。建議：再加一個 case，例如 `定義 \<repo\>。` 預期 rc==0。證據：ask 第 2 點；check_context.py:5。
3. 位置：HtmlTest。問題：只測了 `<ins>`，沒測其他標籤（例如 `<br>`）也會失敗，而規則是「不准任何 HTML 標籤」。建議：加一個 `<br>` 或 `<span>` 的失敗 case。證據：check_context.py:5。
