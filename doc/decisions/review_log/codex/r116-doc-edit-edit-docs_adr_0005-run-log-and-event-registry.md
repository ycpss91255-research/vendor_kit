已完成，未執行 commit、push 或任何 git 寫入指令。

備份：`doc/decisions/_backup/docs_adr_0005-run-log-and-event-registry.pre_r116.md`，已用 `cmp` 與 SHA-256 驗證為修改前原檔。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
exit_codes terms=0 context=0 review_pages=0
message_id_check: PASS
link_target_check: PASS
backup_exists: PASS
```

改動：

- `docs/adr/0005-run-log-and-event-registry.md:23`：將「訊息 M7、M11、M12」改為「訊息見[訊息總表]」，保留原句既有的結束碼 `2`。