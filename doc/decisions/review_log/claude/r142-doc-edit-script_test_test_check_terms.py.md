# r142 審查：script/test/test_check_terms.py

定案對照：逐條看過 map #78「Decisions so far」，這個測試檔沒有碰 01、02 的承諾與不變量，也沒有改 03／04 的對外介面。沒有違反定案。`python3 -m unittest script/test/test_check_terms.py` 過，`check_terms.py` 輸出 OK。

## 必改

1. **位置**：script/test/test_check_terms.py:43（`fields = ["VK0001:situation", "VK0001:description"]`），連帶 script/check_terms.py:113 與 script/README.md「掃哪些檔」那一條
   - **問題**：測試把「`message`、`next_step` 不掃」寫成預期行為，理由是這兩欄改成英文了。但 `_Avoid_` 詞並不都是中文：GLOSSARY.md:44 的 `<name>`、:95 的 `.version`、:110 的 `.<repo>/` 都是 ASCII。英文 `message` 照 ask 要保留占位符原名，占位符正是 `<name>` 這類詞最容易出現的地方。改完之後，`message` 裡出現 `<name>` 或 `.version` 時，哪支 lint 都擋不到：check_messages.py 只管 HTML、Markdown 與中文字元，不管 `_Avoid_` 詞。這一輪把檢查範圍縮小了，而 ask 要的只是「訊息改英文、加一欄 description」，並沒有要縮小名詞檢查。另外，同一輪 check_typography.py:43 的 `TEXT_FIELDS` 還是掃 `message`、`next_step`，兩支 lint 對「哪幾欄算文字欄」的定義也跟著分岔。
   - **建議**：`CSV_TEXT_FIELDS` 改成 `("situation", "message", "description", "next_step")`；`disposition` 是固定值域，可以不掃。測試的 `fields` 改成 `["VK0001:situation", "VK0001:message", "VK0001:description", "VK0001:next_step"]`，並在 `message` 或 `next_step` 放一個 ASCII 的 `_Avoid_` 詞（例如用 `(".version", re.compile(re.escape(".version")))` 當 pattern），斷言命中；英文欄沒有中文舊詞時斷言不命中。README 的「掃哪些檔」也改回「文字欄（`situation`、`message`、`description`、`next_step`）」。
   - **證據**：GLOSSARY.md:44、:95、:110；script/check_terms.py:113；script/check_typography.py:43；script/README.md（check_terms「掃哪些檔」那一條）；script/check_messages.py:50（只擋 HTML 標籤名，不擋 `_Avoid_` 詞）。

## 建議

1. **位置**：script/test/test_check_terms.py:32（註解「固定值域的欄不掃」）
   - **問題**：照目前的實作，沒被掃的欄除了固定值域的 `status`、`level`、`exit_code`、`disposition` 之外，還有 `message`、`next_step`，而這兩欄不是固定值域，註解跟實際行為不符。如果照必改 1 修，這句就又對了。
   - **建議**：照必改 1 修完之後保留原句；如果不改掃描範圍，就改成「只掃 situation、description；其餘欄是固定值域或英文」。
   - **證據**：script/test/test_check_terms.py:32、:43；script/check_terms.py:112。

2. **位置**：script/test/test_check_terms.py:37–39（測試資料）
   - **問題**：`exit_code` 填的是「舊詞」，不是真實會出現的值（`1`／`2`／`3`）。英文 `message` 是 `Old term message`，裡面沒有任何 pattern 會命中，所以這份資料證明不了「英文欄不會誤報」：它只驗了欄位清單。
   - **建議**：`exit_code` 填 `2`、`level` 填 `error`，只在「應該被掃」與「應該被排除」的欄各放一個會命中的詞，讓排除與命中都有實際的斷言。
   - **證據**：script/test/test_check_terms.py:37–47；script/check_messages.py（exit_code 只准 1、2、3，見 script/README.md 的 check_messages 規則）。
