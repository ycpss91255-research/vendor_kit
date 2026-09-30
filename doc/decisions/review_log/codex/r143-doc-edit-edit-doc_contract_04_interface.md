已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份已建立：

`doc/decisions/_backup/doc_contract_04_interface.pre_r143.md`  
SHA-256：`e81852444d3500161862ca5d948db650f03c67834c0aefb71c8bfc39c6ee45e6`

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- 單元測試：151 項全數通過
- `git diff --check`：通過
- 殘留檢查：無「CI 模式」、`VK0003`、`<ins>選項</ins>` 或 `<u>`

修改清單：

- [doc/contract/04_interface.md:3](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:3)：移除 CI 模式語意，明定不讀取 `CI`、recipe 行為不隨環境改變。
- [doc/contract/04_interface.md:9](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:9)：目錄移除「CI 模式」，加入「追蹤新版」。
- [doc/contract/04_interface.md:200](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:200)：新增本機覆寫行為，明定一般 recipe 正常執行、回 0 並於 stdout 印出採用紀錄。
- [doc/contract/04_interface.md:204](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:204)：刪除 `-y` 與 CI 模式、`VK0003` 的舊規則。
- [doc/contract/04_interface.md:243](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:243)：新增 Renovate、PR 單行更新、人工 upgrade／commit／push 與 CI 重跑流程。
- [doc/contract/04_interface.md:297](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:297)：改寫 `test` 契約，明定不寫進 git、基準版落後用 `VK0014`／結束碼 1、本機覆寫用 `VK0032`／結束碼 2。