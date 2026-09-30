# r142 doc-edit 審查：script/README.md

已定案對照：#78 的 Decisions so far 逐條看過。本輪 script/README.md 只改工具說明，沒動 01／02 的承諾與不變量，也沒改 03／04 的對外介面；exit_code 對應（warn→1、error→2、fatal→3）跟 #91／#117 一致，前綴寫法跟 #114 一致。沒有違反定案的地方。

## 必改

1. **位置**：script/README.md:135（check_terms「掃哪些檔」）
   **問題**：「其他欄的值域與語言由 `check_messages.py` 管」不對。check_messages.py 不查 `_Avoid_` 詞。`message`、`next_step` 從掃描範圍拿掉後，英文本文裡的 ASCII `_Avoid_` 詞（GLOSSARY.md:44 `<name>`、:95 `.version`、:110 `.<repo>/`）不會再被任何工具抓到。改動前 message、next_step 有掃（`_backup/script_check_terms.pre_r142.md` 的 `CSV_TEXT_FIELDS`）。
   **建議**：二擇一。(a) check_terms.py:113 把 `message`、`next_step` 加回 `CSV_TEXT_FIELDS`（英文欄照樣比對 ASCII 的 `_Avoid_` 詞），README 改成「`situation`、`message`、`description`、`next_step`」；(b) 保留現狀，README 寫明「`message`、`next_step` 不掃；英文本文裡的 `<name>` 這類 ASCII 舊詞目前沒有工具擋」，並刪掉「由 `check_messages.py` 管」。建議選 (a)。
   **證據**：script/check_terms.py:112-113；script/check_messages.py 沒有任何 _Avoid_ 相關程式；GLOSSARY.md:44、95、110。

2. **位置**：script/README.md:98
   **問題**：這一條列在「查這幾件事」底下，但只有「不准含中文字元」有檢查。「不含 `vendor_kit: <level>[VKnnnn]: ` 前綴」與「`description` 是中文說明」check_messages.py 都沒查（grep 找不到 `vendor_kit:`、前綴相關程式）。讀的人會以為有擋。
   **建議**：拆開寫。檢查項只留「`message` 不准含中文字元（中文說明放 `description`）」；前綴與 description 的語言改寫成欄位約定，並註明「不檢查」。要不然就在 check_messages.py 加一條 message 不得以 `vendor_kit:` 開頭的檢查，連同測試。
   **證據**：script/check_messages.py:62、183-184（只有 CHINESE 檢查）；doc/contract/03_messages.md:85-86。

## 建議

1. **位置**：script/README.md:96
   **問題**：「`exit_code` 必須依序對應 `1`、`2`、`3`」裡的「依序」要回頭對 level 的列舉順序才看得懂。
   **建議**：直接寫「`exit_code` 對應 level：`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`」，用詞跟 03_messages.md:82 一樣。
   **證據**：doc/contract/03_messages.md:82；script/check_messages.py:40。

2. **位置**：script/README.md:98、103
   **問題**：「中文字元」實際只比對 CJK 漢字（U+3400–4DBF、U+4E00–9FFF、U+F900–FAFF），全形標點（`：`、`，`）照樣過。第 103 行又把「中文」和「全形標點」並列成兩種非 ASCII 字，兩句放在一起會讓人以為全形標點也擋。
   **建議**：第 98 行改成「不准含漢字」，或把全形標點也加進檢查（message 是英文，本來就不該出現全形標點）。後者比較一致。
   **證據**：script/check_messages.py:62。

3. **位置**：script/README.md:103
   **問題**：message 改成英文之後，指令範圍「到第一個非 ASCII 字或欄尾」會把後面的英文句子一起吃進來，例如 VK0003 抓到的是 `just vendor_kit upgrade <repo> -y locally; then commit and push.`。以後英文句子裡只要出現前面帶空白的 `-x`／`--xxx`，就會被當成選項報錯。README 沒說這件事，碰到誤報的人不知道原因。
   **建議**：補一句「英文欄沒有非 ASCII 字，範圍通常一路到欄尾，後面的英文句子也算在內」。更好的做法是讓 CMD_CSV 停在 `;`、`.` 加空白或 `(` 這類句子邊界。
   **證據**：script/check_review_pages.py:175；doc/contract/03_messages.csv VK0003。

4. **位置**：script/README.md:103
   **問題**：`description` 也寫了完整指令（VK0001、0003、0004、0006～0009、0014、0022、0023），但指令檢查欄位不含 `description`。中文說明裡寫錯選項不會被抓到。
   **建議**：check_review_pages.py:176 的 `CSV_COMMAND_FIELDS` 加上 `description`，README 同步寫成「`situation`、`message`、`description`、`next_step`」。
   **證據**：script/check_review_pages.py:176；doc/contract/03_messages.csv 各列 description。

5. **位置**：script/README.md:156
   **問題**：「英文的 `message` 與 `next_step` 仍會掃描，但不會因英文排版本身誤報」說得太虛，看不出為什麼不會誤報。
   **建議**：改成「三條規則都只在中文旁邊生效，純英文的 `message`、`next_step` 掃了也不會報錯」。
   **證據**：script/check_typography.py:1-9；script/test/test_check_typography.py:270、280。

6. **位置**：script/README.md:103 與 script/check_messages.py:20（跨檔）
   **問題**：README 寫指令檢查涵蓋 `situation`、`message`、`next_step`；check_messages.py docstring 第 20 行還寫「CSV 的 message、next_step」，漏了 situation。這一段 docstring 本輪沒有跟著改。
   **建議**：check_messages.py:20 改成「situation、message、next_step」（採建議 4 的話再加 description）。
   **證據**：script/check_review_pages.py:13、176；script/check_messages.py:20。

7. **位置**：script/README.md:13（這個問題本輪之前就存在）
   **問題**：連結 `../.claude/workflows/doc-edit.js` 在這個 worktree 裡不存在。它在主 checkout 還是未追蹤檔（`?? .claude/workflows/doc-edit.js`），所以在 GitHub 上是斷的。
   **建議**：doc-edit.js 要進 git，否則這個連結改指 [workflow 說明](../.claude/workflows/README.md)。
   **證據**：`test -e .claude/workflows/doc-edit.js` 回報找不到檔。

8. **位置**：script/README.md:150（這個問題本輪之前就存在）
   **問題**：README 寫「只動下面三條規則」，check_typography.py docstring 寫「兩條規則」，程式把行內程式碼那條算成規則 2 的一部分。兩邊講法不一樣。
   **建議**：統一條數，例如 README 改成「只動下面這些規則涉及的空白與括號」。
   **證據**：script/check_typography.py:2、28。
