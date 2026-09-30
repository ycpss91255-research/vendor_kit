# r140 doc-edit 審查：script/test/test_check_typography.py

比對：`doc/decisions/_backup/script_test_test_check_typography.pre_r140.md`（任務給的檔名 `...typography.py.pre_r140.md` 不存在，實際備份檔名沒有 `.py`）→ `script/test/test_check_typography.py`。
`python3 -m unittest discover -s script/test` 全過（OK）。

## 必改

（無）

- 已定案（map #78 Decisions so far）：diff 只動測試與 docstring，沒有碰到任何一條定案。
- 對外承諾：測試檔不屬於 01～04，沒有改到對外介面。
- 做完沒：ask 1 要求的「測試補正反例」已補上：反例 `以`0`結束`（檢查失敗）與三個 --fix 例（含 ask 舉的 `印`VK0024``）；正例有已空格、全形標點相鄰、未閉合反引號；內容不查（`a的b（c）`）與連結記號透明也有測。ask 2 跟這個檔無關。
- 連結：diff 裡的 `a.md` 只是測試用的暫存資料，不是 repo 裡的連結，不必核對。

## 建議

1. **位置**：`InlineCodeSpacingTest`（第 178～220 行）
   **問題**：規則寫「行內程式碼兩側只查中文，與英數、半形符號相鄰不管」（`script/check_typography.py` 模組說明第 17～18 行），但沒有測試鎖住這個反向行為。之後若有人把行內程式碼當英數處理，`用`a`b`、`x`a`` 這類寫法會開始被報錯，現有測試抓不到。
   **改法**：加一個正例，例如 `"# VK\n\n用 `a`b 與 x`y` 結束\n"`，assert_ok，而且 --fix 之後內容不變。
   **證據**：script/check_typography.py 第 17～18 行、第 339～342 行（`not is_cjk(text[other.start])` 就 continue）；測試檔第 178～220 行沒有這個情況。

2. **位置**：`test_link_markers_are_transparent_fix`（第 208～210 行）
   **問題**：只測了行內程式碼放在連結文字裡（`[`x`](a.md)`），這正好是排版規則要避免的寫法（連結文字不放反引號）。更常見的是行內程式碼緊貼一個中文連結，例如 `見`x`[說明](a.md)`，要跨過 `[` 看到後面的「說」。實測這個情況工具會補成 `見 `x` [說明](a.md)`，但測試沒有鎖住。
   **改法**：加一例 `assert_fix("README.md", "# VK\n\n見`x`[說明](a.md)。\n", "# VK\n\n見 `x` [說明](a.md)。\n")`。
   **證據**：暫存目錄實測 check_typography.py 的輸出（README.md:3 報兩條，--fix 結果如上）；測試檔第 208～210 行。

3. **位置**：`InlineCodeSpacingTest`
   **問題**：模組說明寫 HTML 標籤與 `**` 不算字元（script/check_typography.py 第 16～17 行），這條現在也適用於行內程式碼（`**`x`**的`、`<ins>`x`</ins>的`），但沒有測試。
   **改法**：加一例 `assert_fix` 驗證 `**`x`**的` → `**`x`** 的`。
   **證據**：script/check_typography.py 第 16～18 行；暫存目錄實測 README.md:7、:9。

4. **位置**：`InlineCodeSpacingTest`
   **問題**：CSV 的文字欄（TEXT_FIELDS）也在掃描範圍內，但新規則只測了 md。03_messages.csv 的 message／next_step 如果出現行內程式碼，行為沒有測試保護。
   **改法**：看工具對 CSV 文字欄會不會解析反引號（`tokenize(markdown=False)`）；會的話就用 `write_csv` 加一個反例；不會的話就加一個正例，鎖住「CSV 不套這條規則」。
   **證據**：script/check_typography.py 模組說明第 11～12 行（掃描範圍含 CSV 文字欄）、第 130 行起的 tokenize；測試檔第 178～220 行只有 README.md。
