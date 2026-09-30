已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份：
`doc/decisions/_backup/doc_contract_03_messages.pre_r128.md`

驗證輸出：

```text
custom checks: PASS (22 reason codes; table widths, HTML, named local links, and output terminology valid)
contract table checks: PASS (levels, dispositions, and required next-step commands valid)
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 68、_Avoid_ 詞 21
OK: 掃 5 個對外文件
```

- [doc/contract/03_messages.md:13](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:13)：更新 `0`～`3` 的 info／warn／error／fatal 結束碼契約及取最大值規則。
- [doc/contract/03_messages.md:31](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:31)：重寫 stdout／stderr 分工、正常取消及保留初始檔清單行為。
- [doc/contract/03_messages.md:43](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:43)：改用 `vendor_kit: <level>[VKnnnn]: <中文本文>` 格式及原因代碼規則。
- [doc/contract/03_messages.md:57](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:57)：合併成單一訊息表；現有 13 條編為 `VK0001`～`VK0013`，新增 9 條 warn 診斷至 `VK0022`。
- [doc/contract/03_messages.md:84](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:84)：補明 `VK0001` 的 `<tag>` 替換方式，保留各診斷的不變量依據。