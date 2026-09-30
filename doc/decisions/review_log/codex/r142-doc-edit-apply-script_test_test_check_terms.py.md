已完成，未 commit、未 push、未執行 git 寫入。

- 已改：`script/test/test_check_terms.py` 改為檢查 `situation`、`message`、`description`、`next_step` 四欄，並加入 `message` 內 `.version` 的 `_Avoid_` 命中斷言。
- 未改：`script/check_terms.py:113` 屬於別的檔，交給跨檔一致性。
- 未改：`script/README.md` 的掃描欄位說明屬於別的檔，交給跨檔一致性。

改前版本已備份至 `doc/decisions/_backup/script_test_test_check_terms.pre_r142.2.md`；未覆寫既有的無序號備份。

驗證全部通過：

- `python3 -m unittest script.test.test_check_terms`：4 tests OK
- `python3 script/check_terms.py`：OK
- `python3 script/check_context.py`：OK
- `python3 script/check_review_pages.py`：OK
- `python3 script/check_messages.py`：OK