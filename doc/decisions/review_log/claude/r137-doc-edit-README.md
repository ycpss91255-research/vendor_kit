# r137 doc-edit 審查：README.md

`diff -u doc/decisions/_backup/README.pre_r137.md README.md` 沒有輸出，`git diff HEAD -- README.md` 也是空的：這一輪 README 沒有改動。

## 必改

無。

- 已定案（map #78）：沒有 diff，所以沒有違反。
- 對外承諾：沒有 diff，所以沒有改動。
- 做完沒：README 裡的連結（第 3、7–9、15、17、20、24、26、35、37、60–61、65–70、72 行）的連結文字都不是程式碼名詞，沒有反引號，也沒有 `<…>`；「[…](…) 的 `名詞`」這種寫法 grep 也找不到。B 案在 README 沒有要改的地方，所以不改是對的。
- 連結：沒有新增或改動的連結。
- lint：check_review_pages（5 個對外文件）、check_typography、check_terms、check_context 都過。

## 建議

無。
