# r137 doc-edit 審查：doc/contract/02_invariants.md

範圍：`doc/decisions/_backup/` 沒有 `doc_contract_02_invariants.pre_r137.md`，改用 `git diff HEAD -- doc/contract/02_invariants.md`，結果是空的，這一輪 02 沒有改動。

檢查結果：
- 已定案（#78）：沒有 diff，不可能違反。
- 對外承諾：沒有改動。
- 做完沒：02 共 14 個連結（第 7–18、193、223 行），全都是頁內錨點，連結文字沒有反引號，也沒有 `<…>`；連結旁邊也沒有「[名詞表](…)的 `<名詞>`」這種要改寫的句型。B 案在 02 沒有要改的地方，不改是對的。
- 連結：用腳本照 GitHub 規則算標題 slug 比對，14 個 `#錨點` 全部存在。
- lint：check_context、check_messages、check_review_pages、check_terms、check_typography 都是結束碼 0。

## 必改

無。

## 建議

- 位置：doc/contract/02_invariants.md 第 223 行（第 12 條）。問題：頁內連結文字寫「02 不變量第 4 條」，02 自己引用自己還寫頁號，跟第 193 行「第 4 條「永不靜默失敗」」的寫法不一致。建議：下一輪改 02 時統一成「[第 4 條「永不靜默失敗」](#4-永不靜默失敗)」。這是舊內容，不在這一輪 diff 裡，02 已定案，要改得維護者同意。證據：02_invariants.md:193、:223。
