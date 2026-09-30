已修改 [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:19)，未 commit、未 push。

- 已改：`script/check_messages.py` 新增規則 9，核對文件診斷範例的 level 與 CSV message 第一行，並支援 `<…>` 萬用字元；其他指定文件未改：屬於別的檔，交給跨檔一致性。
- 已改：`script/check_messages.py:23` 將指令檢查欄位更新為 `situation、message、next_step`。
- 未改：`doc/adr/0004-vk-recipe-interface-and-write-boundary.md` 屬於別的檔，交給跨檔一致性。

備份建立於 `doc/decisions/_backup/script_check_messages.pre_r142.2.md`。

驗證結果：

- `test_check_messages`：41 項通過。
- 規則 9 的 4 個程式化案例：通過。
- `check_terms.py`、`check_context.py`、`check_review_pages.py`：通過。
- `check_messages.py`：攔到另一檔尚未修正的問題：`doc/contract/03_messages.md:50` 的 VK0024 本文仍不是 CSV 的 `No command was specified.`。依檔案限制未修改。