# r137 doc-edit 審查：GLOSSARY.md

範圍：`doc/decisions/_backup/GLOSSARY.pre_r137.md` 不存在，改用 `git diff HEAD -- GLOSSARY.md`：diff 為空，這一輪 GLOSSARY.md 沒有改動。

## 必改

（無）

- 已定案（#78）：沒有改動，不可能違反。
- 對外承諾：沒有改動。
- 做完沒：GLOSSARY.md 全檔只有一個 markdown 連結（第 5 行：[目的與承諾]、[不變量]、[ADR]），連結文字都不是程式碼名詞、也沒有反引號或 `<…>`；沒有 reference-style 連結。ask 在 GLOSSARY 裡沒有要改的地方，不改是對的。
- 連結：第 5 行目標 doc/contract/01_purpose.md、doc/contract/02_invariants.md、doc/adr/ 都存在。其他檔連進來的錨點 #工具與出貨（GLOSSARY.md:36）、#版本與來源（:135）、#介面版與契約（:238）都對得上標題（中文標題的 GitHub slug 等於標題本身）。

## 建議

（無）

證據：`git diff HEAD --stat` 只列 04_interface.md 與三支 script；`grep -n '](' GLOSSARY.md` 只有第 5 行；五支 lint（check_context、check_messages、check_review_pages、check_terms、check_typography）結束碼都是 0。
