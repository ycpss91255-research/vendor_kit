已完成，未執行 commit、push 或任何 git 寫入指令。

備份已建立：[docs_contract_03_messages.pre_r114.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/docs_contract_03_messages.pre_r114.md)，並以腳本確認與修改前原檔完全相同。

驗證輸出：

```text
old_message_ids_remaining=0
message_ids=M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13
backup_old_message_id_count=13
numbering_rule=present
local_named_links_checked=19
all_local_link_paths_exist=yes
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

改動：

- [docs/contract/03_messages.md：訊息規則](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:43)：補上編號只供文件引用、不印出、不重用且刪除後留空號的規則。
- [docs/contract/03_messages.md：訊息總表](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:53)：用 Python `re` 將 13 個舊 `6-N` 編號依指定映射改為 `M1`～`M13`；訊息本文、結束碼與時機未改。