# r142 審查：script/check_terms.py

## 必改

1. **位置**：script/check_terms.py:112-113（`CSV_TEXT_FIELDS`）
   - **問題**：這一輪把 `message`、`next_step` 從掃描欄拿掉，連帶讓 `line_hits` 的 `<u>` 檢查（#87「只准 `<ins>`」的強制點，程式第 138-140 行）不再覆蓋這兩欄；check_typography、check_messages、check_review_pages 都沒有 `<u>` 檢查，所以 CSV 的 message／next_step 出現 `<u>` 會靜默通過。另外 GLOSSARY 的 _Avoid_ 詞有 ASCII 詞（GLOSSARY.md:44 `<name>`、:95 `.version`、:110 `.<repo>/`），英文 message 正是最可能用到佔位符 `<name>` 的地方，拿掉後也擋不到。註解「其餘欄位的值域與語言由 check_messages.py 管」不成立：check_messages.py 只管 message 不含中文（check_messages.py:12、:184），不查 _Avoid_ 詞也不查 `<u>`。ask 只要求「掃描的 CSV 文字欄」跟著新欄位改，沒要求縮小 message／next_step 的覆蓋。
   - **建議**：還原成掃 message 與 next_step，並加上 description：`CSV_TEXT_FIELDS = ("situation", "message", "description", "next_step")`（disposition 已由 check_messages.py:186 限定值域，可不掃）；註解改成「CSV 裡會寫出文字的欄；code、status、level、exit_code、disposition 是固定值域，由 check_messages.py 管」。實測四欄全掃目前 0 殘留，不會製造誤報。同步改 script/test/test_check_terms.py:43 的預期欄位與 script/README.md:135 的欄位清單。
   - **證據**：#87；script/check_terms.py:138-140；GLOSSARY.md:44、:95、:110；script/check_messages.py:12、:184；script/test/test_check_terms.py:43；script/README.md:135。

## 建議

1. **位置**：script/check_terms.py:113 與 script/README.md:135、:156
   - **問題**：check_terms 掃 CSV 的欄位集合跟 check_typography（check_typography.py:43 掃 disposition、situation、message、description、next_step）不同，README 兩處各寫一套，讀的人會以為是刻意差異。
   - **建議**：照必改 1 修完後，在 check_terms.py 註解寫一句為何不掃 disposition（固定值域），讓兩支的差異只剩這一欄且有理由。
   - **證據**：script/check_typography.py:43；script/README.md:135、:156。
