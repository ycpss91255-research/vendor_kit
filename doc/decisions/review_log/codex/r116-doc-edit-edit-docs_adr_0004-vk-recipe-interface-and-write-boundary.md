已完成，未執行任何 git 寫入、commit 或 push。

備份：
`doc/decisions/_backup/docs_adr_0004-vk-recipe-interface-and-write-boundary.pre_r116.md`，已用 `cmp` 確認與修改前原檔完全相同。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

額外腳本檢查全部通過：無 `M` 加數字、無 `_Avoid_`、無 `<u>`、所有本機連結路徑存在。

改動清單：

- `docs/adr/0004-vk-recipe-interface-and-write-boundary.md`＋Consequences 第四點＋將 M5、M3、M8 改為結束碼 `2` 與訊息總表連結。
- `docs/adr/0004-vk-recipe-interface-and-write-boundary.md`＋`sync` 三種情境＋移除 M5、M3，保留既有結束碼並連到訊息總表。
- `docs/adr/0004-vk-recipe-interface-and-write-boundary.md`＋可寫 recipe 時序第 1 點＋移除 M11、M12、M7，保留結束碼 `2` 並連到訊息總表。