# r140 審查：script/check_typography.py

diff 基準：`doc/decisions/_backup/script_check_typography.pre_r140.md`（task 寫的 `script_check_typography.py.pre_r140.md` 不存在，實際備份檔名沒有 `.py`）。

## 必改

1. **位置**：doc/contract/README.md 第 21 行（check_typography.py 預設掃描範圍 `doc/contract/*.md` 內）
   - **問題**：新規則讓預設跑法 `python3 script/check_typography.py` 失敗（rc=1）：「以[結束碼 `2`](03_messages.md#結束碼)結束」行內程式碼經 `](…)` 緊貼「結」。ask 要求五支 lint 全過，這支沒過；此檔不在本輪改檔清單，--fix 只跑了 README、01～04、GLOSSARY，漏了同樣在掃描範圍內的審閱頁說明。
   - **建議**：對 doc/contract/README.md 跑 `python3 script/check_typography.py --fix doc/contract/README.md`（該行改成「以[結束碼 `2`](03_messages.md#結束碼) 結束」），把這個內部文件納入本輪；或在規則說明舉例時避開。不要為此放寬 check_typography.py 的規則（ask 明定 `](…)` 相鄰照中文規則）。
   - **證據**：`python3 script/check_typography.py` 輸出「doc/contract/README.md:21: 行內程式碼與中文之間要空一格：「d#結束碼)結束，訊息見」→「d#結束碼) 結束，訊息見」」；script/check_typography.py 第 11 行起的掃描範圍與 `default_files` 的 `doc/contract` glob。

## 建議

1. **位置**：script/check_typography.py 規則 2（第 333～353 行）
   - **問題**：規則 2 也套在 Markdown 標題行；標題裡行內程式碼緊貼中文時 --fix 會補空格，GitHub slug 隨之改變（空格變 `-`），既有 `#錨點` 連結會靜默失效。目前 README、01～04、GLOSSARY 的標題都沒有行內程式碼，所以本輪沒出事，但規則新增後風險變大。
   - **建議**：--fix 遇到標題行只報錯不改，或在 fix 後由 check_links／check_review_pages 驗錨點；至少在 docstring 註明「標題會改到錨點」。
   - **證據**：`grep -nE '^#+ .*\`' README.md GLOSSARY.md doc/contract/*.md` 無結果；新規則在第 340～344 行不分標題與內文。

2. **位置**：script/check_typography.py 第 340～342 行
   - **問題**：`other = right if t.code else t` 後只看 `text[other.start]`；左側是 visible 時取的是 `t.start`，visible 一律單字元所以正確，但這個前提沒寫出來，之後若 visible 改成多字元 token 會取錯邊（該看 `text[t.end-1]`）。
   - **建議**：左側改用 `text[t.end - 1]`，或加一行註解說 visible 是單字元。
   - **證據**：tokenize 第 185 行 `Tok("visible", i, i + 1, ch)`。

3. **位置**：script/check_typography.py 第 12 行（docstring 掃描範圍）
   - **問題**：CSV 用 `markdown=False` 斷詞，反引號不會被認成行內程式碼，所以新規則在 CSV 文字欄不生效；docstring 沒說。目前 `doc/contract/03_messages.csv` 沒有反引號，無實害。
   - **建議**：docstring 補一句「CSV 文字欄不認行內程式碼」。
   - **證據**：第 124 行 `if not markdown:` 分支早於反引號判斷；`grep -c '\`' doc/contract/03_messages.csv` = 0。

## 其他核對結果（無問題）

- map #78「Decisions so far」：本檔改動只涉排版 lint，未觸及任何定案（#79～#103 等）。
- 對外承諾：本檔不是對外文件，未改 01～04 內容。
- 做完沒：規則（行內程式碼與中文相鄰要空格、全形標點不加、`[`／`](…)` 看外側字元、內容不檢查）與 --fix 都已實作；實測「`0`結束」「印`VK0024`」「中**`x`**文」「見[`x`](a)說」「<ins>`x`</ins>的」「「`x`」」「第`1`、`2`條」結果都符合 ask。
- 連結：本檔 diff 無新增或改動的連結。
- `python3 -m unittest discover -s script/test`：OK；check_terms、check_context、check_messages、check_review_pages：rc=0；check_typography：rc=1（見必改 1）。
