# r140 doc-edit 審查：GLOSSARY.md

受審範圍：`diff -u doc/decisions/_backup/GLOSSARY.pre_r140.md GLOSSARY.md`。結果：兩檔逐位元組相同（`cmp` 無差異），`git diff HEAD -- GLOSSARY.md` 也是空的。這一輪 GLOSSARY 沒有改動。

## 必改

（無）

- 已定案（map #78）：沒有 diff，所以不會違反。
- 對外承諾：沒有 diff，01／02／03／04 的承諾與介面不受 GLOSSARY 影響。
- 做完沒：ask 對 GLOSSARY 的要求只有「跑 --fix」。複製一份跑 `python3 script/check_typography.py --fix`，產出與原檔相同（沒有要修的地方）；`check_typography.py GLOSSARY.md` 回 OK、rc=0。用 grep 抓「漢字緊貼反引號」共 9 行（47、127、173、190、196、199、208、220、222），全是反引號內的中文（例如 `<中文本文>`，規則不檢查）或行內程式碼緊貼全形標點（規則不加空白），沒有漏改。第 2 項（04 第 126 行）不需要改 GLOSSARY。
- 連結：GLOSSARY 沒有新增或改動的連結。附帶查了 04 第 126 行連到的 `GLOSSARY.md#介面版與契約`：標題 `### 介面版與契約` 在 GLOSSARY 第 238 行，slug 相同，錨點存在。

## 建議

（無）
