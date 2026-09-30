# r134 doc-edit 審查：doc/contract/03_messages.csv

對照：#123 最後一則 `[claude] 定案`、map #78 Decisions so far、02 第 4、6、10 條、03_messages.md、04_interface.md、GLOSSARY.md。`python3 script/check_messages.py`、check_terms、check_context、check_review_pages 都是 0。

逐列核對 #123 判準（next_step 必須是不用使用者自行代換的單一指令）：VK0001（`<tag>` 原樣印出）、VK0007（`<tag>` 原樣印出）改失敗正確；VK0006 改失敗可成立（指令要先手動還原才能跑，是半手動）；VK0002～0005、0008、0009、0023、0028、0032 的 next_step 都不含原樣印出的占位符，維持需人處理正確；VK0024～0027 處置留空、situation 寫明用法錯誤，照 #123 第 4 條。沒有違反 #78 任何一條定案，也沒有削弱 02 第 4 條（需人處理仍必附指令）。

## 必改

1. **位置**：VK0001 列的 `note`（`update、upgrade 時是 upgrade`），跟 doc/contract/03_messages.md 第 36 行對不上。
   **問題**：03.md 結束碼一節新補的示意把 C 的 VK0001 本文印成 `just vendor_kit update C@<tag>`。CSV 的 note 規定觸發指令是 update 時 `<指令>` 印 `upgrade`；04 的指令清單也只有 `add <repo>@<tag>`、`upgrade <repo>@<tag>`，沒有 `update <repo>@<tag>`（04_interface.md 第 73～76 行）。示意本身印出一條不存在的指令。
   **建議**：03.md 第 36 行改成 `…或直接指定版本：just vendor_kit upgrade C@<tag>（拉取使用主機 docker 認證）`，跟 CSV 的 note 一致。
   **證據**：03_messages.csv VK0001 的 note；03_messages.md 第 36 行；04_interface.md 第 73～76 行。

## 建議

1. **位置**：03_messages.csv 的判準沒有寫進 03_messages.md（第 63、75、79 行）與 GLOSSARY.md 第 201～202 行。
   **問題**：這輪 VK0001、VK0007 改失敗的理由是「next_step 含原樣印出的占位符，要使用者自己代換」（#123 定案第 2 條）。但 03.md 第 75 行只寫「可以直接複製來執行的指令」，第 79 行又允許原樣印出的占位符由使用者自行換；照 03.md 字面讀，含 `<tag>` 的 next_step 看不出不合規。下次有人加新代碼，可能又把含原樣占位符的指令填進 next_step 並標需人處理。
   **建議**：03.md 第 75 行 `next_step` 補一句「不得含原樣印出的占位符」（或「VK 印出時已換成實際值，使用者不用自行代換」）；check_messages.py 可以擋「需人處理列的 next_step 對應到 note 裡標原樣印出的占位符」。這條 ask 沒有要求，列建議。
   **證據**：#123 最後一則 `[claude] 定案` 第 2 條；03_messages.md 第 75、79 行。

2. **位置**：VK0006 列的 `note`。
   **問題**：VK0006 的 next_step 字面上（`just vendor_kit upgrade --engine`）不用代換，照 #123 判準的字面讀可能被下一輪改回需人處理。改失敗的真正理由（要先檢視差異、手動還原後才能跑）只記在 #123 的結論留言，CSV 看不到。
   **建議**：note 後面補「指令要在手動還原之後才能執行，不算可直接執行的下一步，所以列失敗」。
   **證據**：03_messages.csv VK0006；#123 `[claude] 需人處理與失敗：結論` 表格 VK0006 列。

3. **位置**：VK0006 的 `message`「請先檢視下列差異」。
   **問題**：note 只說 `<files>` 逐檔標出是哪一種，沒說會印出差異內容；「下列差異」指向的東西在本文與 note 裡都沒有定義，第一次看的人不知道差異在哪。這不是這輪改的字，但這輪改了這列的處置。
   **建議**：若 VK 會印出差異，note 寫明印在哪（續行或執行紀錄）；不印就把「下列差異」改成「下列檔的差異」並指明怎麼看。
   **證據**：03_messages.csv VK0006 的 message 與 note。

4. **位置**：VK0001 的 `message` 在觸發指令是 update 時。
   **問題**：update 的目的是查有沒有新版；本文建議的「直接指定版本：just vendor_kit upgrade <repo>@<tag>」會直接換版，不是查詢，對 update 的使用者是不同的動作。03.md 第 36 行的新示意（update --exit-code）剛好把這個落差放到最顯眼的位置。
   **建議**：note 補一句 update 時這條路是「直接換到指定版本，不做查詢」，或 update 觸發時只印設定憑證那條路。屬於內容調整，ask 沒要求，列建議。
   **證據**：03_messages.csv VK0001；03_messages.md 第 28、36 行；04_interface.md 第 189 行。

5. **位置**：VK0024～VK0027 的 `situation` 前綴「用法錯誤：」。
   **問題**：「用法錯誤」現在是 CSV 裡區分處置留空的分類（error 列處置留空只因為它），但 GLOSSARY.md 沒有這個詞條，只在第 83、214 行順帶提到。
   **建議**：GLOSSARY 補「用法錯誤」詞條（缺必要參數、不認得指令或選項、tag 格式不合、未指定指令；以結束碼 `2` 結束、處置留空、後附簡短用法），跟 04 第 122～132 行一致。慣例上 argparse 與 GNU grep、diff 用法錯誤都回 `2`，目前的結束碼沒有問題。
   **證據**：03_messages.csv VK0024～VK0027；GLOSSARY.md 第 83、214 行；04_interface.md 第 122～132 行。
