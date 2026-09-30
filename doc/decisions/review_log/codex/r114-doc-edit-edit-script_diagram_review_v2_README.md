已完成，未執行任何 git 寫入、commit 或 push。

備份：`doc/decisions/_backup/script_diagram_review_v2_README.pre_r114.md`

驗證輸出：

```text
legacy_message_like_tokens=NONE
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

修改：

- [script/diagram/review_v2_README.md:83](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:83)：移除 `resolve-3way` 中失效的舊訊息代號，保留「文法不合」語意。
- [script/diagram/review_v2_README.md:84](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:84)：將 `precheck-recover` 的 `6-33` 改成「未完成」語意。
- [script/diagram/review_v2_README.md:85](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:85)：以 Python `re` 將 `6-38→M10`、`6-4→M2`，其餘失效舊號改成原有語意詞。
- [script/diagram/review_v2_README.md:96](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:96)：將已知誤報範例的 `6-33` 改為「未完成訊息」。