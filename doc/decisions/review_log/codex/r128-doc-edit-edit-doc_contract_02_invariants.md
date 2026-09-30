已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 68、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

額外腳本檢查備份、錨點、連結與 HTML 限制均為 `PASS`。備份已建立：[doc_contract_02_invariants.pre_r128.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/doc_contract_02_invariants.pre_r128.md)。

改動：

- [doc/contract/02_invariants.md：目錄](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:6)：加入第 12 條。
- [doc/contract/02_invariants.md：第 4 條](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:88)：警告與需人接手不再算成功，並補上依契約結果判定的原則。
- [doc/contract/02_invariants.md：第 12 條](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:213)：加入無法唯一判定就停止、不猜測、不自動降低保護、具名例外與黑箱驗證規則。
- [doc/contract/02_invariants.md：編號沿革](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:231)：記錄第 12 條附加於末尾、既有編號未重排。

`git status` 顯示的其他文件變更來自並行代理，我未修改。