# r145 doc-edit 審查：script/README.md

## 必改

1. 位置：script/README.md 第 123 行（check_context.py 一節）
   - 問題：新寫的「跳脫的 `\<…\>` 不算」跟 check_context.py 的實際行為不符。`TAG = <(/?)([a-zA-Z][\w-]*)[^>]*>` 沒有排除前面的反斜線，`a \<repo\> b` 會被抓成標籤 `repo`（實測 `TAG.findall(r'a \<repo\> b')` → `[('', 'repo')]`）。只有 check_review_pages.py 第 93 行用 `(?<!\\)` 排除了跳脫。
   - 建議：改 check_context.py，讓 TAG 加 `(?<!\\)`（ask 第 2 點要求「跳脫的 `\<…\>` 照舊不算」，兩支要一致），README 不動；如果不改工具，就把 README 的「與跳脫的 `\<…\>`」刪掉。
   - 證據：script/check_context.py 第 20、44 行；script/check_review_pages.py 第 39、93 行。

## 建議

1. 位置：script/README.md 第 123 行
   - 問題：「連結文字裡未跳脫的 `<…>` 一樣算違規」在 check_context 這節是多餘的：check_context 對整行一律擋標籤，沒有連結文字的特殊檢查（那是 check_review_pages 第 9 條）。寫在這裡會讓人以為 check_context 有另一條規則。
   - 建議：刪掉這半句，或改成「連結文字裡也一樣」。
   - 證據：script/check_context.py 第 38–46 行。

已定案、對外承諾、連結三項：diff 只改內部工具說明的一行，沒新增連結，沒碰 01–04，也沒有牴觸 #78 的決定。
