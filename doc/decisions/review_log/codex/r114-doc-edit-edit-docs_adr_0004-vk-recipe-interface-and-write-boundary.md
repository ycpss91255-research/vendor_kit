已完成，未執行任何 git 寫入、commit 或 push。

備份：[docs_adr_0004-vk-recipe-interface-and-write-boundary.pre_r114.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/docs_adr_0004-vk-recipe-interface-and-write-boundary.pre_r114.md)

驗證輸出：

```text
PASS: target matches scripted regex replacement
PASS: no residual 6-number message IDs
PASS: all 18 named relative links resolve to existing paths
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

- [docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19)：訊息 `6-13`、`6-5`、`6-28` 改為 `M5`、`M3`、`M8`。
- [docs/adr/0004-vk-recipe-interface-and-write-boundary.md:24](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:24)：`sync` 情境引用改為 `M5`、`M3`。
- [docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26)：主機前置檢查引用改為 `M11`、`M12`、`M7`。