# r137 doc-edit 審查：script/check_typography.py

範圍：`diff -u doc/decisions/_backup/script_check_typography.pre_r137.md script/check_typography.py`（任務寫的 `script_check_typography.py.pre_r137.md` 不存在，實際備份檔名少了 `.py`）。這一輪只改 docstring 第 17～18 行，程式碼沒動。

## 必改

（無）

- 已定案：diff 只補 docstring 說明，沒碰 map #78「Decisions so far」任何一條；docstring 仍只舉 `<ins>`，符合 #87。
- 對外承諾：lint 工具的內部說明，不動 01～04 的承諾、不變量或介面。
- 做完沒：ask 第 2 步對 check_typography 的要求是「確認不把 `\<repo\>` 當 HTML 標籤，需要才調整」。實測 tokenizer 第 119 行在 `<` 判斷（第 138 行）之前就把 `\<`、`\>` 收成 `brk` token，TAG 不會匹配；`見[\<repo\>](…)的說明`、`見\<repo\>的說明` 都不報錯，`檢查（\<repo\>）` 的規則 1 照常轉半形。不需改程式，docstring 的描述與實際行為一致。全庫 `python3 script/check_typography.py` → `OK: 檢查 8 個檔`；`python3 -m unittest discover -s script/test` → OK。
- 連結：diff 沒有新增真的連結；`[\<repo\>](…)` 在行內程式碼裡，是寫法示例。

## 建議

1. 位置：script/test/test_check_typography.py（整檔）。問題：docstring 第 17～18 行現在把「反斜線跳脫的 `\<`、`\>` 不是 HTML 標籤、兩側不檢查規則 2」寫成行為說明，但 test_check_typography.py 裡沒有任何含 `\<` 的測試案例（grep `\\\\` 無結果），之後有人改 tokenizer 第 119 行或 TAG 的順序時，不會有測試擋下。建議：補一個正例（`見[\<repo\>](../GLOSSARY.md#x)的說明`、`[\<ns\>/\<repo\>](a.md)` 不報錯）與一個規則 1 例（`檢查（\<repo\>）` → `檢查 (\<repo\>)`）。證據：script/check_typography.py:119-122、:138-152；script/test/test_check_typography.py 沒有這類案例。
2. 位置：script/check_typography.py:17-18。問題：「兩側也不檢查規則 2」對 `<`、`>` 其實沒作用：`<`、`>` 不是英數，就算當成普通字元，規則 2 也不會在它兩側觸發；真正有作用的是「不當 HTML 標籤」這半句。另外對照 B 案：連結文字改成不帶反引號後（`[dist/](…)`），連結文字裡的英數仍照規則 2 檢查（實測 `見[dist/](a.md)的說明` 報「見[dist/」要空格），而 `\<repo\>` 開頭的連結文字因為第一個 token 是 brk 不會報，兩者結果不同但 docstring 沒點出來。建議：把句子改成「反斜線跳脫的字元（例如程式碼名詞當連結文字時寫的 `[\\<repo\\>](…)` 裡的 `\\<`、`\\>`）照 Markdown 當成普通字元，不當 HTML 標籤；它不算英數，兩側不觸發規則 2。連結文字本身的英數照常檢查（`見[dist/](…)` 要寫成 `見 [dist/](…)`）。」證據：script/check_typography.py:119-122、:240-248（_neighbors 遇 brk 即停）；實測結果如上。
3. 位置：任務說明的備份路徑。問題：任務給的 `doc/decisions/_backup/script_check_typography.py.pre_r137.md` 不存在，實際是 `script_check_typography.pre_r137.md`。建議：doc-edit workflow 產生備份檔名與審查指令的規則對齊（`.py` 檔的備份名要嘛保留副檔名、要嘛指令不帶），否則審查端會退回 `git diff HEAD`，範圍可能包含非本輪改動。證據：`ls doc/decisions/_backup/ | grep typography` → `script_check_typography.pre_r137.md`。
