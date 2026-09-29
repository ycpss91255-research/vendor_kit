## 必改

1. **位置：** [script/README.md:5](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:5)  
   **問題：** 說舊文字使用 `<del>`，實作其實新舊文字都用 `<mark style="…">`，只以綠底、紅底區分，完全不產生 `<del>`。  
   **建議：** 改成「新文字用綠底 `<mark>`，被取代的舊文字用紅底 `<mark>`」。  
   **出處：** [script/mark_changes.py:28](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/mark_changes.py:28)、同檔第 99–110 行。

2. **位置：** [script/README.md:42](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:42)  
   **問題：** 範例寫成 `## <ins>目錄</ins>`，實際輸出是 `## <mark style="…">目錄</mark>`；`<ins>` 在本文件中是名詞底線，不是改動標籤。  
   **建議：** 換成實際輸出，或只說行首記號留在標籤外。  
   **出處：** [script/mark_changes.py:37](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/mark_changes.py:37)。

3. **位置：** [script/README.md:57](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:57)  
   **問題：** 說下一行必須是 `**名詞**（english）：`，但檢查器只要求「以粗體起頭、以全形冒號結尾」，英文括號不是必要條件；現有 `**repo**：` 等合法條目也沒有英文括號。  
   **建議：** 按實際檢查範圍描述。  
   **出處：** [script/check_context.py:47](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/check_context.py:47)、[CONTEXT.md:142](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/CONTEXT.md:142)。

4. **位置：** [script/README.md:71](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:71)  
   **問題：** 排除清單漏了 `doc/decisions/review/research/`、`doc/decisions/research/`、`.agents/skills/`。另一方面，程式只收 `.md`，所以 `discussion.drawio` 本來就不會被掃，並非有效的排除案例。  
   **建議：** 列全實際排除目錄；把 drawio 改述為「不在 `.md` 掃描範圍」。  
   **出處：** [script/check_terms.py:18](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/check_terms.py:18)、同檔第 96–118 行。

5. **位置：** [script/README.md:73](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:73)  
   **問題：** 「三個欄位都要對上才放行」不實。執行時只比檔案路徑和字串；理由欄 `_reason` 不參與判定。  
   **建議：** 改成「三欄均須登記；執行時以路徑與字串判定，理由供人審閱」。  
   **出處：** [script/check_terms.py:43](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/check_terms.py:43)、同檔第 67–80 行。

6. **位置：** [script/README.md:75](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:75)  
   **問題：** `(?<!數位)` 是負向後顧（negative lookbehind），不是負向前瞻。  
   **建議：** 更正正規表示式術語。  
   **出處：** [script/check_terms.py:59](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/check_terms.py:59)。

7. **位置：** [script/README.md:79](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:79)、第 87–91 行  
   **問題：** 「有動靜就通知」寫得像不漏事件，但兩個請求都固定 `per_page=50`，沒有分頁；單輪超過 50 筆便可能漏報。  
   **建議：** 腳本使用 `--paginate`；否則 README 必須明載每類每輪只取首 50 筆、可能漏報。  
   **出處：** [script/watch_github.sh:17](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:17)、第 22 行；[`gh api --paginate` 說明](https://cli.github.com/manual/gh_api)。

8. **位置：** [script/README.md:79](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:79)、第 89–93 行  
   **問題：** API 錯誤會被 `2>/dev/null || true` 完全吞掉，但 `last` 仍然前推；失敗期間的事件永久漏報，README 卻沒有說這只是 best-effort。  
   **建議：** API 失敗要印錯誤且不得前推游標；若保留現況，文件必須明示靜默遺漏風險。  
   **出處：** [script/watch_github.sh:17](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:17)、同檔第 22–29 行；issue #68「有下面三種事就印一行」。

9. **位置：** [script/README.md:90](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:90)  
   **問題：** 「PR 上的新留言」範圍過大。`issues/comments` 只取得 PR 對話區的一般留言，不包含 review 與行內 review comment。  
   **建議：** 若需求只有一般留言，改成「issue 或 PR 對話區的新留言」；若 issue #68 的「新留言」包含 code review，腳本還缺相應 endpoint。  
   **出處：** [script/watch_github.sh:16](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:16)；[GitHub issue comments 文件](https://docs.github.com/en/rest/issues/comments)、[PR reviews 文件](https://docs.github.com/en/rest/pulls/reviews)。

10. **位置：** [script/README.md:89](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:89)、第 91 行  
    **問題：** 同一輪詢窗內新開後又關閉／merge 的項目，只會印「新開」。程式使用 `if created … elif closed`，不會同時報「關閉」。  
    **建議：** 兩項判斷獨立；否則 README 應明示這個優先規則。  
    **出處：** [script/watch_github.sh:21](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:21)；issue #68 同時要求新開與關閉／merge 事件。

11. **位置：** [script/README.md:89](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:89)「這段時間」  
    **問題：** 秒級時間游標不足以保證恰好一次。`now` 在 API 呼叫前取得，而 GitHub 的 `since` 是依更新時間篩選；同秒邊界可能漏報或重報。  
    **建議：** 文件明載「可能漏報／重報、不是持久事件佇列」，或由實作採重疊查詢加事件 ID 去重。  
    **出處：** [script/watch_github.sh:10](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:10)、同檔第 14–29 行；[GitHub issue comments 的 `since` 定義](https://docs.github.com/en/rest/issues/comments)。

## 建議

1. **位置：** [script/README.md:16](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:16)、第 23 行  
   **問題：** 「後綴」含義混用：workflow 接受 `r65` 並產生 `.pre_r65`，`mark_changes.py` 接受的卻已是 `pre_r65`。此外 README 說所有檔都用相同攤平規則，但 `doc-apply` 範例會去掉 `doc/decisions/` 前綴。  
   **建議：** 分開定義「輪次 `r65`」「檔名後綴 `pre_r65`」「傳給腳本的參數」，並分述兩套實際檔名。  
   **出處：** [script/mark_changes.py:71](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/mark_changes.py:71)、[.claude/workflows/doc-apply.js:13](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/.claude/workflows/doc-apply.js:13)、同檔第 50–55 行。

2. **位置：** [script/README.md:26](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:26)  
   **問題：** 「舊的那份」不夠準確；實作會刪除同頁名下所有既有 `v*.marked.md`，但保留 `.rev`。  
   **建議：** 改成「同頁名既有的所有標示版會先刪除」。  
   **出處：** [script/mark_changes.py:62](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/mark_changes.py:62)、同檔第 113–116 行。

3. **位置：** [script/README.md:68](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:68)  
   **問題：** 「該行內容」容易理解為完整內容；實作超過 60 字會截斷並加省略號。  
   **建議：** 改成「該行內容摘要（最多 60 字）」。  
   **出處：** [script/check_terms.py:152](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/check_terms.py:152)。

4. **位置：** [script/README.md:73](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:73)  
   **問題：** 一句塞入登記格式、比對方式、殘餘搜尋、兩種反例和設計理由，第一次讀很難掌握白名單邊界。  
   **建議：** 拆成「登記格式」「判定條件」「仍會被抓的情況」「為何不做寬白名單」四句。

5. **位置：** [script/README.md:82](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:82)  
   **問題：** 沒有限定間隔參數。`0` 會高頻輪詢；負數或非數字會讓 `sleep` 報錯，但迴圈仍持續呼叫 API。  
   **建議：** 至少寫明「正整數秒」；較可靠的作法是腳本驗證參數。  
   **出處：** [script/watch_github.sh:9](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/watch_github.sh:9)、同檔第 12–14 行。

6. **位置：** [script/README.md:85](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/script/README.md:85)  
   **問題：** 「timeout 最長 30 分鐘」沒有 issue #68、腳本、01、02、CONTEXT 或 ADR 作為出處，而且是容易隨外部工具版本改變的限制。  
   **建議：** 補有名字的官方說明連結與版本前提，或不要宣稱「最長」。

7. **位置：** 全檔連結與名詞  
   **問題：** 沒有壞連結或匿名 Markdown 連結；唯一的 Markdown 連結 [`diagram/README.md`](script/diagram/README.md) 有名稱且目標存在。`check_terms.py` 實跑為 `OK`，沒有未豁免的 `_Avoid_` 詞。`issue`、`PR`、`Monitor`、`API` 屬一般技術詞；依 [CONTEXT.md:3](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/wt-watch/CONTEXT.md:3)，不要求收入專有名詞表。  
   **建議：** 無。README 本身也沒有引用 ADR，因此沒有 ADR 編號或章節標錯。