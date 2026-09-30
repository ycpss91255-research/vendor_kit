已完成，未 commit、未 push、未執行任何 git 寫入指令。

備份：`doc/decisions/_backup/GLOSSARY.pre_r113.md`，已用腳本確認與修改前原檔完全一致。

檢查輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

- `GLOSSARY.md:239`：保留全部救援路徑呼叫，改為明確說明不規定救援路徑以外 recipe 的 `-h`／`--help` 在版本組合不合時的行為。