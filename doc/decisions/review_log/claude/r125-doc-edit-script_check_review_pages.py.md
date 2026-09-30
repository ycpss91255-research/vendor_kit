# r125 審查：script/check_review_pages.py

備份 `_backup/script_check_review_pages.py.pre_r125.md` 不存在，改用 `git diff HEAD`。

## 必改

無。
- 已定案：只加一條 lint，沒碰 #78 的任何決定；它強制的正是 #85 定的「依 [頁名第 N 條](連結#錨點)」。
- 對外承諾：沒改 01～04。
- 做完沒：ask 第 4 項做了。OLD_CITE 用 ask 給的 regex（第 28 行）；check_page 先去掉反引號內容再比對（第 89 行）；pages() 涵蓋 README.md 與 0N_*.md（第 32 行）；fence 內的行由 body_lines 排除。docstring 第 13–14 行也補了規則 7。
- 連結：diff 沒有新增或改動連結。
- 實測：`python3 -m unittest discover -s script/test` 26 個測試全過；`python3 script/check_review_pages.py` 輸出「OK: 掃 5 個對外文件」。

## 建議

1. 位置：script/check_review_pages.py 第 89 行（逐行比對）。問題：舊寫法如果斷在兩行，例如行尾是 `](連結)`、下一行開頭是 `第 N 條`，就漏抓。建議：另外對整份去掉 fence 的文字跑一次 `\]\([^)]+\)\s*第`，或至少在 docstring 寫明只抓同一行。證據：第 89 行 `OLD_CITE.search(...line)`。
2. 位置：script/check_review_pages.py 第 28 行。問題：`\d+` 只抓阿拉伯數字，`第一條` 或全形數字漏抓。建議：看實際頁面有沒有這種寫法再決定；需要就改成 `[\d０-９一二三四五六七八九十]+`。證據：第 28 行。
3. 位置：第 86、89 行。問題：`re.sub(r"`[^`]*`", "", line)` 重複寫了兩次。建議：抽成一個變數 `plain` 共用。證據：第 86、89 行。
