完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
exit_codes check_terms=0 check_context=0 check_review_pages=0
```

額外腳本確認：舊 `6-數字` 殘留 0、9 個命名連結目標都存在、`<u>` 標籤 0、備份與修改前原檔完全一致。

- [docs/adr/0008-protocol-and-file-schema-versions.md](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:1)：標題限定為「判定不合的執行」零寫入回 `3`。
- [docs/adr/0008-protocol-and-file-schema-versions.md](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:3)：釐清零寫入範圍與執行紀錄例外，補明救援路徑仍可照原有行為寫入。
- [docs/adr/0008-protocol-and-file-schema-versions.md](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:29)：訊息 `6-19` 以腳本換為 `M6`。
- [docs/adr/0008-protocol-and-file-schema-versions.md](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:31)：訊息 `6-10` 以腳本換為 `M4`。
- `doc/decisions/_backup/docs_adr_0008-protocol-and-file-schema-versions.pre_r114.md`：已建立修改前備份。