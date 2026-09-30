已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份：`doc/decisions/_backup/GLOSSARY.pre_r128.md`，內容確認等於修改前原檔。

- `GLOSSARY.md／執行與結果／需人處理`：改為診斷的處置屬性，並要求附可直接複製的下一步指令。
- `GLOSSARY.md／執行與結果／失敗`：定義為未完成且只說明原因，不承諾處置方式。
- `GLOSSARY.md／執行與結果／警告`：明定有警告不算成功，結束碼為 `1`。
- `GLOSSARY.md／執行與結果／原因代碼`：新增 `VKnnnn`、發出後永不重用及刪除後留空號的規則。
- `GLOSSARY.md／執行與結果／結束碼`：加入 `0`～`3` 的 info／warn／error／fatal 定義及多結果取最大值。
- `GLOSSARY.md／提示`：原檔沒有「提示」詞條，無需刪除。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 68、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```