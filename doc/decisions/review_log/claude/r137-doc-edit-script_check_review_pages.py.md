# r137 doc-edit 審查：script/check_review_pages.py

範圍：`diff -u doc/decisions/_backup/script_check_review_pages.pre_r137.md script/check_review_pages.py`（任務給的備份檔名 `script_check_review_pages.py.pre_r137.md` 不存在，實際備份是 `script_check_review_pages.pre_r137.md`）。

核對結果：
- 已定案（map #78）：沒有牴觸。#87「只准 `<ins>`」：新 `TAG` 只把反斜線跳脫的 `\<repo\>` 當字面文字排除，真正的標籤照擋。
- 對外承諾：這支是 lint，沒動 01～04 的承諾或介面。
- 做完沒：ask 第 3 項要的都做了（新 `raw_angle_link_texts`、錯誤訊息提示 `\<…\>`、`<ins>` 放行）；第 2 項 HTML 規則（`TAG` 加 `(?<!\\)`）與 slug 也都照顧到了。單元測試 OK，五支 lint 都以 0 結束。
- 連結：docstring 與錯誤訊息裡的 `../../GLOSSARY.md#工具與出貨` 用腳本算過（從 doc/contract/ 出發指到根目錄 GLOSSARY.md，`slug('工具與出貨')` = `工具與出貨`，GLOSSARY.md:36 有這個標題）。

## 必改

（無）

## 建議

1. 位置：script/check_review_pages.py `raw_angle_link_texts`（約 77–85 行）與 150–152 行的錯誤訊息
   - 問題：連結文字的反引號裡的 `<…>` 也會被 `RAW_ANGLE` 抓到。`` [`<repo>`](a.md) `` 會同時報「不得含反引號」和「改成 \<repo\>」。只照第二條改，會變成 `` [`\<repo\>`](a.md) ``：反斜線在行內程式碼裡照字面顯示，而且反引號錯誤還在。HTML 規則（144 行）會先拿掉反引號再比對，兩條規則的處理方式不一致。
   - 建議：`RAW_ANGLE` 比對前先拿掉連結文字裡的反引號段落（和 144 行一樣用 `re.sub(r"`[^`]*`", "", text)`）；或者連結文字含反引號時，改報一條合併的提示「拿掉反引號並寫 \<repo\>」。
   - 證據：實測 `raw_angle_link_texts('[`<repo>`](a.md)')` → `[('[`<repo>`](a.md)', '<repo>')]`；`backtick_link_texts` 也會回報同一個連結。

2. 位置：script/check_review_pages.py 143–152 行
   - 問題：`[<repo>](a.md)` 會同時報 HTML 規則（「用了 HTML ['repo']…錨點用標題產生」）和第 9 條。HTML 規則的提示方向是錯的：這裡不是錨點，是沒跳脫。
   - 建議：第 9 條抓到的 `<…>` 不要再算進 HTML 規則（例如 `tags` 扣掉 `raw_angle_link_texts` 抓到的名稱）；或者在 HTML 規則的訊息補一句「要寫字面的 <…> 就用 \<…\>」。
   - 證據：實測 `TAG.findall('[<repo>](a.md)')` → `['repo']`，`raw_angle_link_texts` 也會回報同一個連結。

3. 位置：script/check_review_pages.py `slug`（94 行）
   - 問題：這一行本輪有改，但標題裡反引號內的 `<repo>` 還是會被當成標籤刪掉。GitHub 算出來是 `repo-是什麼`，這裡算出 `-是什麼`。現在沒有這種標題（grep `^#+ .*<` 在 README、01～04、GLOSSARY 都沒有結果），不會馬上出錯；但要是之後有人寫出這種標題，第 4 條錨點檢查會算錯。
   - 建議：刪標籤前先保留反引號段落的內容；或者只刪反引號外的 `<…>`。
   - 證據：實測 `slug('`<repo>` 是什麼')` → `-是什麼`；`slug('\<repo\> 是什麼')` → `repo-是什麼`（跳脫寫法正確）。

4. 位置：script/check_review_pages.py docstring 第 3 行「規則見 doc/contract/README.md「寫法規則」」
   - 問題：新的第 8 條補充（程式碼名詞直接寫）和第 9 條（連結文字的 <…> 要跳脫），在 doc/contract/README.md「寫法規則」裡都沒寫。那一節 21 行的例子還是 `[結束碼 `2`](03_messages.md#結束碼)`，本身就違反第 8 條。docstring 指到的規則來源已經過時。doc/contract/README.md 不在這一輪的檔案清單裡，不過它是內部文件，照 CLAUDE.md 不准留過時資訊。
   - 建議：另開一輪 doc-edit，把 doc/contract/README.md「寫法規則」補上 B 案（連結文字不放反引號、程式碼名詞直接寫、<…> 跳脫），並把 21 行的例子改成 `[結束碼](03_messages.md#結束碼) `2``。
   - 證據：doc/contract/README.md:20–21。

5. 位置：script/check_review_pages.py 150–151 行 `fixed = "\\<" + raw[1:-1] + "\\>"`
   - 問題：只跳脫了一半的 `<repo\>` 也會被抓到，但提示會變成 `\<repo\\>`（多一個反斜線）。
   - 建議：組 `fixed` 前先把內容結尾的反斜線去掉（`raw[1:-1].rstrip("\\")`）。
   - 證據：實測 `raw_angle_link_texts('[<repo\>](a.md)')` → raw 是 `<repo\>`。
