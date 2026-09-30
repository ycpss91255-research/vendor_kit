# r137 doc-edit 審查：doc/contract/04_interface.md

範圍：`diff -u doc/decisions/_backup/doc_contract_04_interface.pre_r137.md doc/contract/04_interface.md`，只有一處改動（第 98 行）：
`[名詞表](../../GLOSSARY.md#工具與出貨)的 \`<repo>\`` → `[\<repo\>](../../GLOSSARY.md#工具與出貨)`。

## 必改

無。

- 已定案（map #78 Decisions so far）：沒有牴觸任何一條；#85（引用寫法）、#87（只准 `<ins>`）與此改動無關。
- 對外承諾：只改連結寫法，名詞與連結目標不變，沒有改動 04 的對外介面。
- 做完沒：04 裡所有連結（`grep -n '\](' doc/contract/04_interface.md`）只有第 98 行的連結是在指程式碼名詞；其餘連結文字都是一般詞（工具、tag、訊息、結束碼…），沒有反引號，也沒有其他「[名詞表](…)的 `X`」寫法。ask 在 04 該做的都做了。
- 連結：`../../GLOSSARY.md#工具與出貨` 用腳本算 GLOSSARY 標題的 slug，`### 工具與出貨`（GLOSSARY.md:36）存在；`<repo>` 條目就在這一節（GLOSSARY.md:42）。`python3 script/check_review_pages.py` 通過。

## 建議

無。
