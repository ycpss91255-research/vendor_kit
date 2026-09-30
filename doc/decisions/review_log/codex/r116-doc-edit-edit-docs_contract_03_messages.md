已完成，未執行 commit、push 或任何 git 寫入指令。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
message_number_refs=0
missing_local_link_targets=0
```

改動：

- `doc/decisions/_backup/docs_contract_04_interface.pre_r116.md`：建立修改前備份。
- `docs/contract/04_interface.md:44`：M12 改為「訊息見訊息總表」。
- `docs/contract/04_interface.md:46`：M7 改為「訊息見訊息總表」。
- `docs/contract/04_interface.md:55`：M1 改為「訊息見訊息總表」。
- `docs/contract/04_interface.md:175`：M3 改為直接寫結束碼 `2`，並連到訊息總表。
- `docs/contract/04_interface.md:190`：M2 改為「訊息見訊息總表」。