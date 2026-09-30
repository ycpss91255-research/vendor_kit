# r141 doc-edit 審查：doc/contract/README.md

## 必改

（無）

- 已定案：這三處改動只動內部文件的寫法範例與規則句，沒碰 map #78 的決定。
- 對外承諾：沒動 01～04。
- 做完沒：第 21 行範例已改成「以[結束碼](03_messages.md#結束碼) `2` 結束」。第 23 行補上「連結文字不放反引號；程式碼名詞當連結時寫 `[\<repo\>](…)`」。第 42 行把 [`script/pack_review.py`] 改成 [打包腳本]，連結文字不再含反引號。第 19、22 行的「依 [頁名第 N 條](…)」本來就跟現行規則一致。
- 連結：03_messages.md 的 `## 結束碼`（第 13 行）與 `## 訊息`（第 60 行）、GLOSSARY.md 的 `### 工具與出貨`（第 36 行）、script/pack_review.py 都存在。五支 check_*.py 都以 0 結束。

## 建議

- 位置：doc/contract/README.md 第 23 行。問題：同樣的規則在 script/check_review_pages.py 第 17–21 行的 docstring 裡也寫了一次，違反第 22 行的「規則只寫一次」。建議：第 23 行改成連到 [審閱頁檢查](../../script/check_review_pages.py) 第 8、9 條，或者接受重複，但要確保兩處措辭一致。證據：script/check_review_pages.py:17-21。
