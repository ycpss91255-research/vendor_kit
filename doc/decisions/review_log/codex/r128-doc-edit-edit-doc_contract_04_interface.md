已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份已建立為 `doc/decisions/_backup/doc_contract_04_interface.pre_r128.md`，並以 SHA-256 確認與修改前原檔一致。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 68、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

另外 `git diff --check` 通過，未發現 `<u>` 或錯誤的 `warning[...]` 前綴。

修改項目：

- [doc/contract/04_interface.md:129](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:129)：用法錯誤改為先印 `error` 診斷，再附簡短用法。
- [doc/contract/04_interface.md:171](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:171)：補明 `-y` 變更摘要、詢問及回答「否」時的串流與結束碼。
- [doc/contract/04_interface.md:189](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:189)：區分 `update` 與 `update --exit-code`；後者查到新版印 `warn[VKnnnn]`、回 `1`。
- [doc/contract/04_interface.md:200](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:200)：明定 stdout／stderr 分工、診斷格式及成功判定原則。
- [doc/contract/04_interface.md:224](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:224)：合併衝突、收回零／多處、`add` 遇既有檔改為 `warn`／`1`。
- [doc/contract/04_interface.md:248](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:248)：`remove`／`uninstall` 保留初始檔時，清單印 stdout、回 `0`。
- [doc/contract/04_interface.md:269](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:269)：補明本機基準版落後時印 `warn` 診斷、回 `1`。