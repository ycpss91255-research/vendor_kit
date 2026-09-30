已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：
`doc/decisions/_backup/docs_adr_0008-protocol-and-file-schema-versions.pre_r113.md`

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

`git diff --check` 亦通過。

修改項目：

- `docs/adr/0008-protocol-and-file-schema-versions.md:3`：說明版本組合不合時的零寫入不含執行紀錄，並連結不變量 4。
- `docs/adr/0008-protocol-and-file-schema-versions.md:29`：替檔案版過高的拒絕補上相同限定。
- `docs/adr/0008-protocol-and-file-schema-versions.md:31`：替引擎降版遭拒的零寫入補上相同限定。