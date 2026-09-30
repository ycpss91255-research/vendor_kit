已完成，未執行 commit、push 或任何 git 寫入指令。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
OK: 無舊訊息編號 6-數字殘留
OK: 本檔所有相對路徑連結的目標都存在
```

備份：[docs_contract_02_invariants.pre_r114.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/docs_contract_02_invariants.pre_r114.md)

- [docs/contract/02_invariants.md：第 4 條](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:94)：限定零寫入為「版本組合不合並以結束碼 3 結束的該次執行」，並說明救援路徑仍可照原有行為寫入。