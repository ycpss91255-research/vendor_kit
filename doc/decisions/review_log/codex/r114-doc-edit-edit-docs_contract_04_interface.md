已完成，未執行任何 git 寫入、commit 或 push。

備份：
`doc/decisions/_backup/docs_contract_04_interface.pre_r114.md`

修改：

- `docs/contract/04_interface.md:44`：訊息 `6-40` 改為 `M12`
- `docs/contract/04_interface.md:46`：訊息 `6-23` 改為 `M7`
- `docs/contract/04_interface.md:55`：訊息 `6-3` 改為 `M1`
- `docs/contract/04_interface.md:175`：訊息 `6-5` 改為 `M3`
- `docs/contract/04_interface.md:190`：訊息 `6-4` 改為 `M2`

腳本確認舊式 `6-數字` 訊息編號殘留：`[]`

指定檢查輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```