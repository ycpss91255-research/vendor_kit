# r138 doc-edit 審查：script/mark_changes.py

範圍：`diff -u doc/decisions/_backup/script_mark_changes.pre_r138.md script/mark_changes.py`（任務寫的 `script_mark_changes.py.pre_r138.md` 不存在，實際備份檔名是 `script_mark_changes.pre_r138.md`，內容與 `git diff HEAD` 相同）。

## 必改

無。

- 已定案（#78 Decisions so far）：這支是內部工具，diff 只動 CSV 逐碼差異的表頭／刪欄標示，不碰版本號位置（#79）、不碰 `<ins>` 規則（#87）。沒有違反。
- 對外承諾：沒動 01～04 的內容。
- 做完沒：ask 要 mark_changes 的 CSV 標示照新欄位。`diff_csv` 本來就照表頭逐欄比較、沒寫死欄名；這次補上刪欄／新增欄的標示。拿實際的 `pre_r138.csv` 對現行 CSV 跑 `diff_csv`：表頭列出 `code,…,note,invariant,details` → `code,…,next_step`，三欄都標「（本欄刪除）」，VK0001 的 note 與 VK0002 的 invariant／details 舊值標紅。已做到。
- 連結：diff 沒有新增或改動連結。

## 建議

1. 位置：script/test/test_mark_changes.py 的 CsvTest（對應 script/mark_changes.py:325-336、365-368）
   問題：這次加的新邏輯（`removed`／`added`、表頭行、`（本欄刪除）`／`（本欄新增）`、只刪欄的代碼不算沒改動）完全沒有測試。現有測試的 OLD 與 NEW 用同一個 HEAD，這些分支一條都沒跑到。
   建議：加一個 OLD 多一欄（例如 `note`）、NEW 沒有這欄的案例，斷言三件事：出現表頭行、`- \`note\`：（本欄刪除）`；只有 note 有值的代碼成段，列出紅底舊值加上「（本欄刪除）」；note 為空的代碼仍列在「沒改動的代碼」。再加一個 NEW 多一欄的案例，斷言有「（本欄新增）」。
   證據：script/test/test_mark_changes.py:274-280（OLD 與 NEW 共用 HEAD）；script/mark_changes.py:325-336、365-368。

2. 位置：script/mark_changes.py:332-336
   問題：表頭行與每欄的「本欄刪除／新增」行不算進 `ins`／`dele`。如果只改表頭、所有被刪欄在每一列都是空的，回傳的新增數與刪除數都是 0，後面還會印「CSV 沒有改動。」（第 377 行的判斷只看代碼），跟開頭的表頭差異互相矛盾。
   建議：有 `removed` 或 `added` 時把表頭算一筆改動（`ins += 1; dele += 1`），而且「CSV 沒有改動。」的條件改成 `not (removed or added) and len(same) == …`。
   證據：script/mark_changes.py:332-336、377-378。

3. 位置：script/mark_changes.py:328-329、332
   問題：只有欄位順序變了、欄名集合沒變時，`removed` 與 `added` 都是空的，不會出表頭行，順序的改動就看不出來（CSV 的欄序也是檔案格式的一部分）。
   建議：條件改成 `if old_text is not None and old_fields != new_fields:`。
   證據：script/mark_changes.py:328-332。

4. 位置：script/test/test_check_terms.py:42（同一輪別的檔，不在本檔範圍，順手記下）
   問題：`python3 -m unittest discover -s script/test` 目前有 1 個失敗：`test_csv_text_fields_scanned` 還預期會掃到 `VK0001:note`，但 check_terms 已經改成不掃 note。ask 要求全部測試過，這一條沒過。test_check_terms.py 不在這一輪的改檔清單裡，像是漏改。
   建議：把預期改成新的文字欄（disposition、situation、message、next_step），測試資料的表頭也照新欄位。
   證據：跑 unittest 的輸出 `FAIL: test_csv_text_fields_scanned … ['VK0001:situation', 'VK0001:message'] != [..., 'VK0001:note']`。

5. 位置：模組說明 script/mark_changes.py:31
   問題：「刪掉的欄在各碼照樣列出舊值並標紅」少了條件：只有舊值不為空的代碼才會列出。舊值是空的代碼仍算沒改動（第 342 行）。
   建議：改成「刪掉的欄有舊值的代碼照樣成段，舊值標紅」。
   證據：script/mark_changes.py:31、342、365-368。
