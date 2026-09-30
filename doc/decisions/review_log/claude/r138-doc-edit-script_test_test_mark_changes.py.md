# r138 審查：script/test/test_mark_changes.py

基準：`doc/decisions/_backup/script_test_test_mark_changes.pre_r138.md`（任務寫的 `script_test_test_mark_changes.py.pre_r138.md` 不存在；這份跟 `git show HEAD:script/test/test_mark_changes.py` 逐字相同）。
`python3 -m unittest test_mark_changes`（在 script/test 下）全過。整包 `unittest discover -s script/test` 有 1 個失敗，在 test_check_terms.py，不在本檔。

map #78「Decisions so far」：本檔的改動沒有違反任何一條。對外承諾：本檔是測試，沒有改 01～04 的介面。連結：diff 裡沒有新增或改動的連結。

## 必改

1. **位置**：`CsvTest`（script/test/test_mark_changes.py 第 269 行起）
   **問題**：ask 要「mark_changes.py 的 CSV 標示照新欄位」並且「測試跟著改」。這一輪 mark_changes.py 新增了表頭改動的處理：`removed`／`added` 欄、表頭那一行、`COLUMN_REMOVED`／`COLUMN_ADDED`，還有刪掉的欄在各碼列出舊值並標紅。這些是這一輪真正要跑的情況（03_messages.csv 從 10 欄刪成 7 欄），本檔卻沒有測試覆蓋。OLD 與 NEW 用的是同一個 HEAD，所以這幾條分支一條都沒跑到。第 336～339 行的 `assertNotIn` 也等於空測：fixture 從頭就沒有 note、invariant、details 欄。
   **建議**：新增 `test_removed_column`。舊版 CSV 用帶 `note` 欄的表頭（例如 `code,status,level,disposition,situation,message,next_step,note`，VK0001 的 note 有值、VK0002 的 note 是空的），新版用現在的 HEAD。要斷言：(a) 出現 `- 表頭：{RED}舊表頭</mark> → {GREEN}新表頭</mark>`；(b) 出現 `` - `note`：{RED}（本欄刪除）</mark> ``；(c) `#### VK0001` 段裡有 `` - `note`：{RED}舊值</mark> {RED}（本欄刪除）</mark> ``；(d) 只刪了空欄的 VK0002 列在「沒改動的代碼」。再加一個新增欄的案例，斷言 `（本欄新增）`。第 336～339 行的 `assertNotIn` 要嘛刪掉，要嘛改寫成「舊版有這三欄、新版沒有」的斷言，不能留著空測。
   **證據**：script/mark_changes.py 第 327～336、365～368 行（新分支）；script/test/test_mark_changes.py 第 274～280 行（OLD 與 NEW 共用 HEAD）、第 336～339 行；手動用帶 note 欄的舊表頭呼叫 `diff_csv`，確認分支會輸出上面這些行，但沒有任何測試鎖住這些輸出。

## 建議

1. **位置**：第 274～275 行
   **問題**：註解寫「表頭照 check_messages.FIELDS」，但表頭是手寫的字串。以後 FIELDS 改了，這裡不會跟著壞，註解就成了過時資訊。
   **建議**：改成 `HEAD = ",".join(check_messages.FIELDS) + "\n"`，並 import check_messages。不 import 的話，就把註解改成只描述現況，不要引 FIELDS。
   **證據**：script/check_messages.py 第 34 行；script/test/test_mark_changes.py 第 274～275 行。

2. **位置**：`test_per_code_per_field`（第 330 行起）
   **問題**：原本斷言 `level` 從 error 變 fatal，改稿後 level 沒變，只斷言照原樣列出。欄位值改動仍然由 disposition、situation、message、next_step 覆蓋，功能上沒有損失。但從空值變成有值的 next_step 用了 `（空）` 標示，這個行為之前沒測過，現在有測到，這是好事，保留。
   **建議**：不用改；這條只是確認覆蓋沒有縮水。
   **證據**：diff 第 328～335 行。

3. **位置**：script/test/test_check_terms.py 第 42 行（不在本檔，但跟本檔同一輪）
   **問題**：整包測試有 1 個失敗。test_check_terms 還期望掃到 `VK0001:note`，跟 ask「掃描欄改成 disposition、situation、message、next_step」衝突。ask 要求全部測試都過，所以這一輪還不算完成。
   **建議**：把期望值改成新欄位的結果，由負責 test_check_terms.py 的審查處理。
   **證據**：`python3 -m unittest discover -s script/test` → FAIL test_csv_text_fields_scanned。
