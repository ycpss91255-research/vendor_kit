修正完成，未 commit、未 push，也未執行任何 git 寫入指令。

- 已改：`doc/contract/03_messages.csv` VK0022、VK0024～VK0027，英文本文已與 03／04 範例一致。
- 已改：`doc/contract/03_messages.csv` VK0001、VK0002、VK0005、VK0010、VK0025、VK0026、VK0032，四個相關欄位的占位符統一改為英文。
- 已改：`doc/contract/03_messages.csv` 其餘 active 訊息，依規則修正句首大小寫與句尾標點；指令結尾不加句點。
- 已改：`doc/contract/03_messages.md` 診斷本文規則，加入占位符／小寫指令名開頭與指令結尾的例外。
- 已改：`script/check_messages.py` 新增規則 10，並處理完整 `just` 指令名及含版本句點的指令。
- 已改：`script/test/test_check_messages.py` 補上規則 9 的四類測試，以及規則 10 的正反例和邊界案例。
- 已改：`script/test/test_check_review_pages.py` 指令錯誤訊息期待值改為在 `and retry.` 前停止。
- 已改：`script/test/test_mark_changes.py` 新增欄測試改為期待綠色新值及「本欄新增」。
- 已改：`script/mark_changes.py` `diff_csv` docstring 補上新增欄的標示規則。
- 已改：`script/README.md` CSV 逐碼差異段補上新表頭順序與新增欄標示規則。
- 已改：`script/README.md` message 欄位約定改為明列規則 4 會禁止中文。
- 已改：`script/README.md` 規則清單補上診斷範例與 CSV 一致性檢查。
- 已改：`script/README.md` CSV 指令擷取範圍同步目前的終止條件。
- 已改：`doc/contract/04_interface.md` `update --exit-code` 的 stdout 改回中文查詢結果。
- 已改：`GLOSSARY.md`「診斷」格式統一為 `<message>`。
- 未改：`doc/adr/0004-vk-recipe-interface-and-write-boundary.md` 不在硬性規則允許修改的檔案清單內。
- 已改：`GLOSSARY.md` 新增 **level** 詞條及結束碼對應。
- 已改：`doc/contract/04_interface.md` `vendor_kit` 的一般用語「命名空間」移除 `<ins>`。
- 已改：`script/check_typography.py`、`script/test/test_check_typography.py`、`script/README.md`，將 `disposition` 改列固定值域，不再掃描排版。

驗證結果：

- 指定的四支檢查全部 `OK`
- `check_typography.py`：`OK`
- 完整測試：151 項全部通過
- `git diff --check`：通過
- 雙軸 review：規範面無問題；spec reviewer 找到的規則 10 邊界問題已修正並重新驗證
- 修改前備份已依規則建立；因同名備份已存在，本次使用下一個序號版本。