已完成，未 commit、未 push，也未執行任何 git 寫入指令。改前備份已建立並經 `cmp` 驗證一致：

[pre_r128 備份](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/doc_adr_0004-vk-recipe-interface-and-write-boundary.pre_r128.md)

驗證結果：

- `check_terms.py`：通過，掃描 29 個 Markdown、21 個 `_Avoid_` 詞。
- `check_context.py`：失敗；並行中的 `doc/contract/03_messages.md` 目前被刪除，造成 40 個斷鏈。
- `check_review_pages.py`：同樣因上述 40 個斷鏈失敗。
- `git diff --check`：通過。
- 本檔的結束碼、診斷格式與禁用 `<u>` 腳本檢查：全部通過。

修改清單：

- [ADR-0004 第 1–3 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:1)：標題與決策摘要改為所有警告均以 `warn`／結束碼 `1` 紅燈。
- [ADR-0004 第 9 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:9)：將原先否決「警告紅燈」的取捨改為採用穩定性優先。
- [ADR-0004 第 17–25 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:17)：加入完整結束碼表、最大值規則，並校正 CI、基準版落後、快取重裝等結果。
- [ADR-0004 第 27 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:27)：前置檢查改為 `error[VKnnnn]` 診斷格式及結束碼 `2`。
- [ADR-0004 第 31–35 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:31)：相關引用改為具名連結與「依頁名第 N 條」寫法。