已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- `check_terms.py`：OK，掃描 30 個 Markdown、21 個 `_Avoid_` 詞
- `check_context.py`：OK，分群 9、名詞 67
- `check_review_pages.py`：OK，掃描 5 個對外文件
- 三支腳本結束碼皆為 `0`

備份已建立：
`doc/decisions/_backup/docs_contract_03_messages.pre_r113.md`

改動：

- [docs/contract/03_messages.md:60](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:60)：訊息 6-36 移除「其他 recipe 的 `-h`／`--help`」會回結束碼 3 的結論；救援路徑以外 recipe 的既有規則保持不變。