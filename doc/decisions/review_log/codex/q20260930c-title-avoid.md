## 結論

應讓 lint 放行作為頁名引用的完整字串「01 專案目的與承諾」，不要改 01 的標題。`專案` 在這裡指 VK 本身，不是把使用者的 repo 改稱「專案」；問題出在 lint 尚未一致處理合法的頁名引用。

## 理由

- `CONTEXT.md` 禁用「專案」的語境是 **repo 的替代名稱**：`repo` 定義為使用者的 git repo，隨後列 `_Avoid_: 專案、下游 repo`，不是全面禁止這兩個字。[CONTEXT.md:141](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:141)

- 01 的實際標題確實是「01 專案目的與承諾」，而內容談的是「為什麼做 VK」及 VK 對使用者的承諾，不是在命名使用者的 repo。[01_purpose.md:1](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:1) [01_purpose.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:15)

- lint 現有白名單已承認這項語義區分：標題中的「專案」指 VK 本身；`doc/decisions/README.md` 引用標題也基於同一理由放行。[check_terms.py:46](/home/cyc/Desktop/vendor-kit_ws/src/script/check_terms.py:46) 因此只讓部分引用位置通過、迫使其餘位置縮寫，屬於規則施作不一致，而不是標題本身違反名詞表。**「屬於施作不一致」是推論。**

- 定案規則明確要求引用使用頁面的實際標題，並以 01「專案目的與承諾」為例。[discussion_queue.md:24](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:24) 現在根 README 與 04 寫成「01 目的與承諾」，確實違反這項規則。[README.md:65](/home/cyc/Desktop/vendor-kit_ws/src/README.md:65) [04_interface.md:239](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:239)

- 目前 `doc/decisions/README.md` 已能使用實際標題，證明精確放行可與術語檢查並存；現行白名單還會把放行字串移除後再次檢查同一行，並非整檔豁免。[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15) [check_terms.py:67](/home/cyc/Desktop/vendor-kit_ws/src/script/check_terms.py:67)

## 風險或反例

- 若把「專案目的與承諾」在所有位置無條件放行，正文可能利用完整片語逃過檢查。放行應限於 Markdown 連結文字或標題引用的完整字串，而非單純見到該片語就通過。**這是對實作方式的推論。**
- 改標題為「01 目的與承諾」會消除特例，也較簡潔；但它是在改已定案對外頁的名稱，只為遷就 lint，且沒有解決「lint 應能辨認合法專名引用」這個一般問題。**後半是推論。**
- 保留原標題仍有讀者把「專案」誤解成使用者 repo 的可能；不過目前頁碼、連結目標及全文 VK 語境已提供足夠區分。**這是閱讀風險判斷。**