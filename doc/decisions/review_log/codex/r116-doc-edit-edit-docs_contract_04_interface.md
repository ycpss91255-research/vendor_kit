已完成，未 commit、未 push，也未執行任何 Git 寫入指令。

備份已建立：`doc/decisions/_backup/docs_contract_04_interface.pre_r116.md`

驗證輸出：

```text
訊息 Mn: PASS
（Mn）: PASS
Mn、Mm: PASS
任何 M 編號: PASS
路徑作為連結文字: PASS
本機連結目標存在: PASS
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

- `docs/contract/04_interface.md:44`：Docker 版本不足的 M12 引用改為訊息總表。
- `docs/contract/04_interface.md:46`：just 版本不足的 M7 引用改為訊息總表。
- `docs/contract/04_interface.md:55`：registry 認證的 M1 引用改為訊息總表。
- `docs/contract/04_interface.md:175`：M3 引用改為結束碼 `2` 與訊息總表。
- `docs/contract/04_interface.md:190`：無法互動時的 M2 引用改為訊息總表。