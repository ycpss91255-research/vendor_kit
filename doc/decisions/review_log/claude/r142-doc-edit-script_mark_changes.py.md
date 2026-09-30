# r142 doc-edit 審查：script/mark_changes.py

範圍：這一輪只改了兩段 docstring（模組 docstring 第 32–33 行、`diff_csv` docstring 第 330–331 行），程式邏輯沒動。定案對照（#78 Decisions so far：#79 版本號只在檔名、#87 只准 `<ins>`、#122 CSV 唯一出處等）：沒有違反；01、02、03／04 對外介面不受本檔影響。`test_mark_changes.py` 40 項全過。

## 必改

1. **位置**：`script/mark_changes.py` 第 373–384 行（`diff_csv` 逐欄迴圈），以及第 32–33 行新加的 docstring
   **問題**：這一輪新增的 `exit_code`、`description` 兩欄，在每個代碼底下都印成紅底「（空）」→ 綠底新值，並把刪除數加一。舊版根本沒有這兩欄，紅底的意思卻是「被取代或拿掉的舊文字」（第 2 行），讀者會以為原本有值、被清掉了。拿實際的 `_backup/doc_contract_03_messages.pre_r142.csv` 對現行 CSV 跑 `diff_csv`，得到 103 ins／103 del，其中大約 2 × 活躍碼數的刪除是這兩欄憑空算出來的。刪掉的欄有逐碼補「（本欄刪除）」（第 373–376 行），新增的欄卻沒有對應處理，兩邊不對稱。ask 第 4 點要求「mark_changes.py 的 CSV 標示跟著改」，第 32–33 行的 docstring 也宣稱新增欄已經列進逐碼差異，但實際標出來的結果是錯的。
   **建議**：在 `elif f in removed:` 之後加一個 `elif f in added:` 分支，`b` 有值時輸出 ``- `f`：<綠>b</mark> （本欄新增）``（`COLUMN_ADDED`），只加 `ins`，不加 `dele`；`b` 空白就不列。`script/test/test_mark_changes.py` 第 396 行（表頭新增 `next_step` 的案例）現在斷言的是紅底「（空）」→ 新值，要改成新行為並加一條 `dele` 不增加的斷言。`script/README.md` 第 67 行補一句：新增欄在各碼只列綠底新值並註記「（本欄新增）」。
   **證據**：`script/mark_changes.py:336`（有算出 `added`，但只用在表頭）、`:373-384`；`script/test/test_mark_changes.py:396`；實跑 `diff_csv(pre_r142.csv, 03_messages.csv)` 的輸出是 VK0001 `exit_code`：紅「（空）」→ 綠「2」，`description`：紅「（空）」→ 綠「…」。

2. **位置**：`script/mark_changes.py` 第 330 行（`diff_csv` docstring）
   **問題**：「（包含新加的 exit_code、description）」只在這一輪成立。merge 之後，這兩欄就是固定表頭的一部分，不再是「新加的」，這句話會變成過時資訊；CLAUDE.md 規定內部文件不准留過時資訊。
   **建議**：還原成原文「欄位照新表頭的順序，新表頭拿掉的欄接在後面：刪掉的欄在表頭與各碼都標紅，否則只刪欄的代碼會被當成沒改動。」如果要講新增欄，就寫成通則，例如「新表頭多出的欄照它在新表頭的位置列出」，不點名具體欄位。
   **證據**：`script/mark_changes.py:330`；CLAUDE.md「決議與文件流程」中「不准留過時的資訊」。

## 建議

1. **位置**：`script/mark_changes.py` 第 31–33 行（模組 docstring）
   **問題**：第 31 行已經寫了「表頭改了……先標出新舊表頭」，第 32–33 行又另起一句講新增欄。例子綁定這一輪（「在 level 後新增 exit_code、在 message 後新增 description」），一句話拖得長；「已刪欄位才接在最後」跟第 331 行重複。
   **建議**：把兩句合成一句通則：「表頭改了（加欄或刪欄）時，後半開頭先標出新舊表頭；欄位照新表頭的順序列，刪掉的欄接在最後、各碼列出舊值並標紅，新增的欄各碼只標綠。」（最後一段跟必改第 1 條的行為一起改。）
   **證據**：`script/mark_changes.py:31-33`、`:330-331`。

2. **位置**：`script/mark_changes.py` 第 314–316 行（`show`）
   **問題**：`（空）` 同時用來表示「舊值是空字串」和（目前）「舊版沒有這一欄」，兩種意思在標示版上看不出差別。
   **建議**：必改第 1 條修好後，`（空）` 就只剩「欄位存在但沒填」這一種意思。docstring 寫明這一點即可，不需要另加記號。
   **證據**：`script/mark_changes.py:315`。
