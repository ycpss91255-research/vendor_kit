# r138 審查：script/check_messages.py

diff 來源：`doc/decisions/_backup/script_check_messages.pre_r138.md`（任務指定的 `script_check_messages.py.pre_r138.md` 不存在，實際備份檔名少了 `.py`）。

## 必改

無。

- 已定案（#122、#123、#117、#114）：diff 只拿掉 note／invariant／details 的欄位與檢查，保留「CSV 唯一出處」「需人處理必有 next_step、失敗 next_step 空白」等規則，沒有違反。
- 對外承諾：這支是內部 lint，不動 01～04 的對外介面。
- 做完沒：FIELDS 已是 `code,status,level,disposition,situation,message,next_step`（第 34 行，與 CSV 表頭一致）；RETIRED_KEEP 拿掉 note；invariant_numbers、detail_sections、FENCE、details／invariant 的逐列檢查都已刪；docstring 規則 8～10 併成 8；「指令寫法」一句拿掉 note。`python3 script/check_messages.py` 印 OK。
- 連結：diff 裡沒有新增或改動的 Markdown 連結。

## 建議

1. 位置：check_refs，第 224–225 行。問題：只有連結文字是代碼（如 [`VK0002`](03_messages.md#vk0002)）才擋。新寫法「[訊息](…) `VK0002`」的文字是「訊息」，舊的 `[訊息](03_messages.md#vk0002)` 留在 ADR 不會被擋，而 check_review_pages 的錨點檢查只掃 README 與 doc/contract（check_review_pages.py:89），也不掃 doc/adr。所以 ADR 裡指到已刪的 #vk0002／#vk0005 的死連結會全部 lint 通過。建議：目標是 03_messages.md、錨點符合 `vk\d{4}` 時一律報錯，不管連結文字；並補一個 ADR 的測試。證據：script/check_messages.py:224；script/check_review_pages.py:89；目前 grep 沒有殘留，所以這是防回歸。
2. 位置：check_rows／新增規則。問題：刪掉 detail_sections 後，03_messages.md 重新出現 `### VKnnnn` 節也不會被擋，但「03.md 不放逐碼內容」是這一輪的新規則（docstring 第 17 行自己也寫了）。建議：保留一個小檢查，03_messages.md 出現 `### VK\d{4}` 標題（圍欄外）就報錯，並補測試。證據：script/check_messages.py:15–17；diff 刪掉的 detail_sections。
3. 位置：同一輪的 script/test/test_check_terms.py:42（不是本檔，但 ask 要求測試全過）。問題：`python3 -m unittest discover -s script/test` 目前 FAILED (failures=1)：test_csv_text_fields_scanned 仍期待 `VK0001:note`。check_terms.py 的掃描欄已改，測試沒跟著改，而且 test_check_terms.py 不在這一輪的改動清單裡。建議：期望值改成新欄位掃出的格（disposition、situation、message、next_step 中 fixture 有值的那幾格），並把 test_check_terms.py 列進這一輪。證據：unittest 輸出 `AssertionError: ['VK0001:situation', 'VK0001:message'] != [..., 'VK0001:note']`。
