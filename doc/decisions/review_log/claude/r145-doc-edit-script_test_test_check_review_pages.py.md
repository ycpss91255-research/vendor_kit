# r145 審查：script/test/test_check_review_pages.py

## 必改

無。diff 只有 test_html_other_than_ins_fails 改名為 test_any_html_fails_including_ins，並把 assertNotIn("'ins'") 改成 assertIn（第 56、62 行），符合 ask 第 5 點；這輪沒有新增或改動連結，不碰 01–04 的對外介面，也沒違反 #78 的定案。單檔測試 14 個全部通過。

## 建議

- 位置：test_unescaped_angle_in_link_text_fails（第 159–170 行）附近。問題：ask 第 2 點說連結文字裡未跳脫的 `<…>` 不再特別放行 `<ins>`，但沒有測試涵蓋這點；現在只測了 `<repo>`、`<ns>`，連結檢查要是回頭放行 `<ins>`，測試抓不到。建議：在這支測試加一筆 `[<ins>VK</ins>](01_a.md#第一節)`，斷言該行有一筆含 `\<` 的錯誤。證據：script/check_review_pages.py 第 20–21 行（「<ins> 也一樣要跳脫」）；這支測試檔沒有任何連結文字含 `<ins>` 的案例。
- 位置：第 18 行 `c.slug("<ins>引擎</ins> 版本")`。問題：slug 測試還拿 `<ins>` 當輸入。功能上沒錯（標題裡的標籤要剝掉），但這是舊用法的範例。建議：可以留著；要換的話改成其他標籤，例如 `<b>`。證據：script/test/test_check_review_pages.py 第 18 行。
