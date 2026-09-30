已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份已建立：
`doc/decisions/_backup/script_test_test_check_terms.pre_r144.md`

驗證結果：

- `check_terms.py`：FAIL，其他並行文件尚有 4 個錯誤：
  - `doc/contract/02_invariants.md:12`：`repo` 分群錯誤
  - `doc/contract/02_invariants.md:13`：`工具 image` 分群錯誤
  - `doc/contract/04_interface.md:12`：`registry` 分群錯誤
  - `doc/contract/04_interface.md:19`：`test` 分群錯誤
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `python3 -m unittest discover -s script/test`：157 tests，全部通過
- `git diff --check`：通過

改動：

- `script/test/test_check_terms.py:2-3`：加入輸出擷取工具。
- `script/test/test_check_terms.py:70`：將 `<u>` 的預期提示更新為「名詞改用連結」。
- `script/test/test_check_terms.py:73-165`：新增正確連結、漏連、錯誤分群、不存在錨點、`<ins>` 殘留，以及標題與程式碼不計首次出現的測試。