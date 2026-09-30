# r121 doc-edit 審查：doc/contract/03_messages.md

範圍：`diff -u doc/decisions/_backup/doc_contract_03_messages.pre_r121.md doc/contract/03_messages.md`

腳本核對結果：
- 訊息本文：改前、改後各 13 列，每列「訊息」欄反引號內的字串逐字相同（排序後比對為 True）
- 「下一步」欄：只有兩列不同，差在說明文字搬進註（`<加上 -y 的原指令>` 的重組規則、`<安裝指令>` 不覆蓋既有 just）；指令本身沒變
- 連結：diff 裡的 12 個錨點（本頁 6 個、02 共 6 個）用 GitHub slug 規則算，全部存在
- `script/check_review_pages.py`：OK
- 13 條分配：需人處理 6、版本組合不合 3、失敗 4。ask 寫「7 列」是算錯，原表結束碼 2 且類別為需人處理的就是 6 列

## 必改

（無）

## 建議

1. 位置：03_messages.md 第 65 行（薄殼不符那列）、第 78 行（版本組合不合表上方）
   問題：新加的 `<ins>薄殼</ins>`、`<ins>引擎</ins>`、`<ins>repo 檔</ins>`、`<ins>VK 檔</ins>` 在第 27 行（結束碼表）已經加過底線。審閱頁規則是名詞第一次出現時才加 `<ins>`。
   建議：這四處拿掉 `<ins>`，改回純文字。
   證據：doc/contract/03_messages.md:27、:65、:78；doc/contract/README.md:20

2. 位置：03_messages.md 第 78 行
   問題：「三條都是除執行紀錄外，在任何寫入之前結束」讓薄殼那列也承諾「在任何寫入之前結束」，比原本「除執行紀錄外，不動 repo 檔與 VK 檔」稍微強一點；降版、檔案版兩列則多了「不動 repo 檔與 VK 檔」。這兩種說法跟結束碼 3 的定義（第 27 行）一致，ask 也給了這個寫法，所以不列必改。不過這是把原本逐列的說法合成一句。
   建議：保留，送審時點出這句是合併後的共同說法；或改成只照抄第 27 行的定義：「以這個碼結束的那次執行不動 repo 檔與 VK 檔，執行紀錄除外」，降版與檔案版兩列的「在任何寫入之前結束」放進註。
   證據：doc/decisions/_backup/doc_contract_03_messages.pre_r121.md 表格第 4、6、9 列；doc/contract/03_messages.md:27、:78

3. 位置：03_messages.md 第 92 行
   問題：表上方講的是 podman 與 Docker 兩條，句尾卻寫「只在 stderr 印這條」，「這條」沒有明確指哪一條。
   建議：改成「只在 stderr 印對應的訊息」。
   證據：doc/contract/03_messages.md:92

4. 位置：03_messages.md 第 73 行（註：just 太舊）與第 92 行
   問題：主機前置檢查（just、podman、Docker）的共同說明寫了兩次：一次在需人處理表的註，一次在失敗表上方。第 23 條定案是把這三項當成同一組處理。
   建議：兩處用同一句話，例如都寫「主機前置檢查：排在建執行紀錄之前……」，讓讀者看得出這是同一條規則。不改也行。
   證據：doc/contract/03_messages.md:73、:92；discussion_queue.md「已定案」第 23 條

5. 位置：03_messages.md 註的清單（第 69～74、88、103～104 行）
   問題：每條註開頭的標籤（例如「沒有 registry 憑證」「基準版落後」「just 太舊」）跟該列「情況」欄的文字不一樣，讀者要自己把註對回某一列。
   建議：標籤改用情況欄的開頭幾個字，或者在情況欄的句尾加一樣的短名。
   證據：doc/contract/03_messages.md:60-65、:69-74
