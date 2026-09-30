# r140 doc-edit 審查：script/README.md

範圍：`diff -u doc/decisions/_backup/script_README.pre_r140.md script/README.md`（第 143、147、149 行三處）。

## 必改

（無）

- 已定案（map #78）：diff 沒碰任何一條。例子裡的 `VK0024` 是 03_messages.csv 第 27 行現有的代碼，也照原樣印在訊息裡（03_messages.md 第 50 行），跟 #101「訊息不編號」不衝突。
- 對外承諾：script/README.md 是內部文件，diff 沒動 01～04 的承諾或介面。
- 做完沒：ask 1 要求 script/README.md「同步一句」。第 147 行補了規則，第 143 行「兩條」改成「三條」，第 149 行「不查行內程式碼」改成「不查行內程式碼的內容」。ask 2 跟這個檔無關。
- 連結：diff 沒有新增或改動連結。

## 建議

1. 位置：script/README.md 第 143 行「三條規則」、第 147 行。
   問題：README 說是三條規則，check_typography.py 卻還寫兩條：docstring 第 2 行寫「維護者定案的兩條規則」，第 8～9 行把行內程式碼寫在規則 2 底下，用法說明寫「只動上面兩條規則的字元」，`--fix` 的 help 寫「只動規則 1、2 的字元」，`find_issues` 的註解也寫「規則 2：中文與英數相鄰；中文與行內程式碼相鄰」。內部文件不准留過時的資訊，兩邊要講同一套。
   建議：二選一。(a) README 回到「兩條規則」，把第 147 行併進第 146 行那條，當成它的補充句（跟 docstring 的結構一樣）。(b) 保留三條，改 check_typography.py 的 docstring、用法說明、`--help` 與註解，讓它們也寫三條。(a) 改動比較少。
   證據：script/README.md:143、147；script/check_typography.py:2、8-9、「用法」段的「只動上面兩條規則的字元」、main() 裡 `--fix` 的 help、find_issues 的「# 規則 2」註解。

2. 位置：這一輪的 lint 結果（不在這個檔，不過跟第 147 行的新規則直接相關）。
   問題：`python3 script/check_typography.py` 回 1：`doc/contract/README.md:21: 行內程式碼與中文之間要空一格：「d#結束碼)結束，訊息見」→「d#結束碼) 結束，訊息見」`。審閱頁說明第 21 行的範例「以[結束碼 `2`](03_messages.md#結束碼)結束」跟新規則衝突，而 ask 要求五支 lint 全過。
   建議：doc/contract/README.md 第 21 行改成「以[結束碼 `2`](03_messages.md#結束碼) 結束」（跑 `--fix` 那個檔也可以），並列入這一輪的改檔清單。
   證據：doc/contract/README.md:21；script/check_typography.py 的 targets() 會掃 doc/contract/*.md。

3. 位置：script/README.md 第 147 行。
   問題：只寫了連結記號不算字元。實作裡 HTML 標籤（例如 `<ins>`）和粗體記號 `**`／`__` 也不算字元，行內程式碼跟英數或半形符號相鄰也不查，這些都要讀 docstring 才知道。
   建議：「連結記號不算字元」改成「連結記號、HTML 標籤與粗體記號不算字元；與英數、半形符號相鄰不管」。
   證據：script/check_typography.py docstring 第 17～21 行。
