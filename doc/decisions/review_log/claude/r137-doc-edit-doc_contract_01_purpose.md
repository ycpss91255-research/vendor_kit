# r137 doc-edit 審查：doc/contract/01_purpose.md

範圍：`doc/decisions/_backup/doc_contract_01_purpose.pre_r137.md` 不存在（這一輪 _backup 只有 README、04、兩支 script、一支 test 的 pre_r137），改用 `git diff HEAD -- doc/contract/01_purpose.md`，結果為空。這一輪 01 沒有改動。

## 必改

無。

- 已定案（#78）：沒有 diff，不可能違反。
- 對外承諾：沒有 diff，01 的承諾不變。
- 做完沒：01 全檔（92 行）只有 7 個連結：第 3 行 `[名詞表](../../GLOSSARY.md)`、第 7～10 行目錄錨點、第 21 行 Git／Docker／just 外部連結。連結文字都不是程式碼名詞，也沒有反引號或 `<…>`（`grep -nE '\[[^]]*(`|<|>)[^]]*\]\('` 零命中）。程式碼名詞（第 14 行 `git subtree`、`symlink`，第 30 行 `just vendor_kit test`，第 86 行 `X.Y.Z`）都不是連結，照規則維持反引號。ask 在 01 沒有該改的地方，不改是對的。
- 連結：沒有新增或改動的連結。

## 建議

無。

證據：`python3 script/check_review_pages.py` → `OK: 掃 5 個對外文件`；`python3 script/check_typography.py` → `OK: 檢查 8 個檔`。
