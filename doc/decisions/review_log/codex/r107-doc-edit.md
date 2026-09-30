## 必改

1. **位置：README.md 第 22 行**
   - **問題：**「VK 不呼叫 git」範圍過廣。定案內容只保證「VK 在主機上不呼叫 git」；引擎容器內仍使用 `git merge-file`。目前句子與 ADR 不符。
   - **建議：**改成「VK 不在主機上呼叫 git」。
   - **證據：**`doc/decisions/review/02_invariants.md:114`；`doc/adr/0007-host-thin-layer-and-shell-integrity.md:94`；`doc/decisions/review/04_interface.md:35`。

2. **位置：doc/decisions/review/04_interface.md「registry 與認證」第 48、54 行**
   - **問題：**同一節互相衝突。第 48 行依 02 第 2 條承諾「主機的 docker 拉得到就能用」；第 54 行又說非 GHCR 出問題不在承諾內。前者沒有 registry 限制，後者縮小了承諾。
   - **建議：**在 Q10 定案前不能把本頁視為正確；應先決定承諾範圍，再讓第 48、54 行與 02 第 2 條只保留一種說法。
   - **證據：**`doc/decisions/review/02_invariants.md:70`；`doc/decisions/review_log/discussion_queue.md:84-88`。

3. **位置：doc/decisions/review/04_interface.md「使用者的檔與 VK 的檔」第 205–216 行**
   - **問題：**第 205 行宣稱動到使用者檔的寫入「只有三種明定例外」，但列出的第三種只有「已納管初始檔的基準版合併」；第 213–216 行另外允許第一次導入時向既有 append 型初始檔加入內容。這不屬於前述三種。
   - **建議：**把 append 型初始檔納入例外清單，或取消「只有三種」的封閉數量說法，改按「加入可歸因內容／不損失內容的合併」兩類整理。
   - **證據：**`doc/decisions/review/04_interface.md:205-216`；`doc/decisions/review/02_invariants.md:44-47`。

4. **位置：doc/decisions/review/04_interface.md「CI 檢查腳本」第 237–240 行**
   - **問題：**本頁把腳本範圍寫成「01 對外契約中，CI 驗得到的項目百分之百覆蓋」，比 01 已定義的腳本責任更廣。01 只承諾它回報版本、快取、初始檔是否一致；例如 release 不可變性、逐檔相同等承諾雖可能由 CI 驗證，01 沒說都由這支腳本負責。
   - **建議：**按 01 收窄為版本、快取、初始檔一致性；若確實要擴大腳本責任，須先同步修改 01 的承諾。
   - **證據：**`doc/decisions/review/01_purpose.md:30`；`doc/decisions/review/01_purpose.md:59-60,80`；`doc/decisions/review/04_interface.md:237-240`。

5. **位置：doc/decisions/review/03_messages.md「訊息」第 36、47 行**
   - **問題：**第 36 行規定「意思」欄是逐字訊息本文，但 6-23 的儲存格包含「印三行。第一行……第二行……」等文件敘述，不是程式逐字照印的訊息。
   - **建議：**把 6-23 改成真正的三行訊息本文；或修改欄位規則，明確允許此列只描述訊息格式。兩者不能同時成立。
   - **證據：**`doc/decisions/review/03_messages.md:36,47`。

6. **位置：doc/adr/0007-host-thin-layer-and-shell-integrity.md「Consequences」第 100 行**
   - **問題：**句子說版本不足或 Podman 的錯誤訊息都有「可以照做的指令」，但 6-39 沒有指令，下一步欄也是「—」。而且 6-39 被分類為「失敗」，依 02 第 4 條只要求講出原因，不強制附可複製指令。
   - **建議：**改成只有版本不足的情況附指令；Podman 僅說明原因與處置。
   - **證據：**`doc/adr/0007-host-thin-layer-and-shell-integrity.md:100`；`doc/decisions/review/03_messages.md:49`；`doc/decisions/review/02_invariants.md:104`。

## 建議

1. **位置：doc/decisions/review/03_messages.md 第 40–49 行**
   - **問題：**表格一列同時塞入時機、規則依據、逐字訊息、下一步與狀態，6-10、6-23 特別難讀；第一次閱讀很難分辨哪些文字會真的印給使用者。
   - **建議：**保留欄位，但將多行訊息移到表格後的編號小節；表格只留短摘要與連結。
   - **證據：**`doc/decisions/review/03_messages.md:36-49`。

2. **位置：doc/decisions/review/03_messages.md 第 44、46、48 行**
   - **問題：**`<vY>`、`<P>`、`<M>`、`<N>`、`<P_shell>`、`<written_by>`、`<對象>` 沒有在 CONTEXT.md 定義，也沒有本頁圖例。熟悉 ADR 的人猜得到，第一次看的人不知道各自是版本字串、介面版、檔案版或命令片段。
   - **建議：**在「訊息」規則下補一份占位符說明，或改成能直接讀懂的名稱，例如 `<引擎版本>`、`<薄殼介面版>`。
   - **證據：**`doc/decisions/review/03_messages.md:36,44,46,48`；`CONTEXT.md:227-239`。

3. **位置：doc/decisions/review/04_interface.md「成對與無害」第 143 行**
   - **問題：**「做得了就反得回」容易被理解成操作後狀態完全還原；但 `remove`／`uninstall` 明確不刪初始檔，只收回可歸因的行。
   - **建議：**改成「介面成對，但反向操作只收回 VK 能可靠歸因的內容」，避免把命令成對誤寫成狀態可逆。
   - **證據：**`doc/decisions/review/04_interface.md:143,219-233`；`doc/decisions/review/02_invariants.md:36-42`。

4. **位置：doc/decisions/review/04_interface.md 第 201 行**
   - **問題：**`.vendor_kit/config.toml` 是新的領域檔案與特殊權限邊界，但 CONTEXT.md 沒有定義；讀者也無法從「VK 檔」的一般定義得知它是唯一交給使用者修改的 VK 檔。
   - **建議：**在 CONTEXT.md 定義這個檔，或避免把檔名當成未介紹的契約名詞。
   - **證據：**`doc/decisions/review/04_interface.md:201`；`CONTEXT.md:89-105`。

5. **位置：doc/adr/0007-host-thin-layer-and-shell-integrity.md 第 30–33、89–96 行**
   - **問題：**有效白名單被拆在原 Decision、後來修訂與 04 三處。只讀原 Decision 會以為只有 `grep`、`sed`；要一路讀到後面才知道還有 `id`、`mktemp` 等。
   - **建議：**在 Decision 加一句醒目的有效版本指引，直接連到第 89–96 行或 04「主機需求」，避免讀者採用已被補充的舊清單。
   - **證據：**`doc/adr/0007-host-thin-layer-and-shell-integrity.md:30-33,89-96`。

連結核查結果：待審範圍內的實際 Markdown 連結都有名稱，本機目標路徑存在；對外頁沒有「出處：」行；所有「依 02 第 N 條」的條號與標題錨點相符。`check_context.py`、`check_review_pages.py`、`check_terms.py` 目前也全部通過。