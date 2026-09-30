已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：[pre_r113 備份](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/docs_adr_0004-vk-recipe-interface-and-write-boundary.pre_r113.md)

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

`git diff --check` 亦通過。

- [ADR-0004 第 26 行](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26)：分開說明 Docker／Podman 與 just 的前置檢查時機、執行者、訊息、結束碼及執行紀錄行為。