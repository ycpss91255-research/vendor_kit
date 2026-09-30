# r142 doc-edit 審查：GLOSSARY.md（Claude）

改動範圍：只有 GLOSSARY.md:196「診斷」一行，`<中文本文>` → `<英文本文>`（`diff -u doc/decisions/_backup/GLOSSARY.pre_r142.md GLOSSARY.md`）。

## 必改

無。

- 定案對照：map #78「Decisions so far」逐條看過，這一行沒有碰到任何一條。#114 留言第 251、335 行寫「本文照舊是中文」，這次是維護者明確推翻，屬於 ask 第 1 項，不算違反。前綴格式 `vendor_kit: <level>[VKnnnn]: `（#114）、level 集合與 `info` 只標 `0`（#117）都沒動。01、02 的承諾與不變量沒被削弱。
- 跨檔一致：跟 doc/contract/03_messages.md:62（「訊息本文為英文」）、03_messages.md:85（`message`：英文本文）、03_messages.csv 表頭（`message` 英文、`description` 中文）一致。
- 結束碼、警告兩條（GLOSSARY.md:208、:214）的 warn→1、error→2、fatal→3，跟 03_messages.md:82 新增的 `exit_code` 欄與 CSV 的值一致。
- 連結、_Avoid_ 詞：這一行沒有連結，也沒有 _Avoid_ 詞；check_context、check_terms、check_typography、check_review_pages、check_messages 全部 exit 0。

## 建議

1. 位置：GLOSSARY.md:196「診斷」
   問題：占位符名跟 03 對不上。GLOSSARY 寫 `<英文本文>`，doc/contract/03_messages.md:62 寫 `<message>`。讀者從名詞表跳到 03 時，會以為這是兩個不同的東西。
   建議：改成 `vendor_kit: <level>[VKnnnn]: <message>`，後面補一句「本文為英文」，例如「……`<message>` 的訊息，含續行；本文為英文。」或者保留 `<英文本文>`、03 不動也可以，但兩邊至少要讓人看得出指的是同一個欄位。
   證據：GLOSSARY.md:196；doc/contract/03_messages.md:62、:85。
