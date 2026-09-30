# r137 審查：script/test/test_check_review_pages.py

範圍：diff pre_r137 → 現行，新增 `test_escaped_angle_link_text_passes`、`test_unescaped_angle_in_link_text_fails`（第 138–162 行）。`python3 -m unittest discover -s script/test` 120 個測試全過。

## 必改

無。
- 已定案：跟 #87（只准 `<ins>`）一致，把 `\<repo\>` 當字面文字、不當標籤，沒有違反 map #78 的任何一條。
- 對外承諾：只動測試，沒碰 01～04。
- 做完沒：ask 第 2、3 步在這個檔要做的是「`\<repo\>` 不算 HTML」的正例和「未跳脫 `<…>` 要擋」的反例，兩個都補了。
- 連結：測試用的 `../../GLOSSARY.md#工具與出貨`、`GLOSSARY.md#工具與出貨`、`01_a.md#第一節` 指向測試自己在暫存目錄建的檔與標題（第 140、146、151 行），而且檢查器（script/check_review_pages.py 第 155 行起）算過錨點，回傳 0。repo 的 GLOSSARY.md 第 36 行確實有 `### 工具與出貨`。

## 建議

1. 位置：test_unescaped_angle_in_link_text_fails（第 150–162 行）
   問題：只斷言訊息裡有 `\<`，沒驗證提示的改法對不對。`fixed` 就算算錯（例如變成 `\<repo>`），或換成別的訊息，這個測試還是會過。另外只用 `len(hits)==1` 過濾，沒釘住規則的專屬字樣。
   建議：斷言完整字串，例如 `"doc/contract/01_a.md:7: 連結文字裡的 <repo> 沒跳脫：[<repo>](01_a.md#第一節)；改成 \\<repo\\>"` 和 `"README.md:5: 連結文字裡的 <ns> 沒跳脫：[用 <ns> 分](doc/contract/01_a.md)；改成 \\<ns\\>"`，再用 `out.count("沒跳脫") == 2` 確認每個連結只報一次。寫法比照同檔的 test_backtick_in_link_text_fails（第 111–123 行）。
   證據：script/test/test_check_review_pages.py 第 159 行 `"\\<" in l`；script/check_review_pages.py 第 151–152 行。

2. 位置：新增測試整體
   問題：`raw_angle_link_texts` 放行 `<ins>`、`</ins>`（script/check_review_pages.py 第 77–84 行、docstring 第 20–21 行寫「<ins> 不算」），但沒有測試覆蓋。01 的名詞底線用 `<ins>`（#60、#87），名詞當連結文字時很可能出現 `[<ins>引擎</ins>](…)`，放行壞掉的話對外頁的 lint 會誤報。
   建議：在 test_escaped_angle_link_text_passes 或新測試加一條 `[<ins>引擎</ins>](01_a.md#第一節)`，斷言回傳 0、輸出沒有「沒跳脫」。
   證據：script/check_review_pages.py 第 82 行 `if m.group(2) != "ins"`；實測 `[<ins>x</ins>](01_a.md#第一節)` 不報錯，但沒有測試守住。

3. 位置：test_unescaped_angle_in_link_text_fails
   問題：未跳脫的 `<repo>` 會同時觸發 HTML 規則（`用了 HTML ['repo']`）和新規則，一行報兩個錯。測試沒寫明這是預期行為，之後有人把 HTML 規則改成跳過連結文字，也不會有測試發現。
   建議：斷言 HTML 規則也照樣報（`"用了 HTML ['repo']"` 在 out 裡），或在註解寫明兩條規則都會報。
   證據：實測輸出 `doc/contract/01_a.md:7: 用了 HTML ['repo']…` 加 `doc/contract/01_a.md:7: 連結文字裡的 <repo> 沒跳脫…`；script/check_review_pages.py 第 143–152 行。
