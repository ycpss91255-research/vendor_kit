## 結論

要拿掉 `needs-decision`。刪除前，將目前 8 個 open issues（#42、#41、#35、#34、#31、#30、#25、#14）改標 `needs-triage`；13 個 closed issues 不補任何狀態標籤，直接隨標籤刪除而移除。這由既定原則即可推出，不需要再問維護者。

## 理由

- 新版 triage skill 封閉地定義五種 state，且要求每個受 triage 的 issue 恰有一種 state；其中 `needs-triage` 的語意就是「維護者需要評估」。[`triage/SKILL.md`](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/triage/SKILL.md:31) 列五種狀態，[同檔第 41 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/triage/SKILL.md:41) 要求恰好一種 state，[第 45 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/triage/SKILL.md:45) 定義完整轉移。`needs-decision` 不在其中。

- 新版 tracker mapping 同樣只有五個一對一標籤，`needs-triage` 明定為「Maintainer needs to evaluate this issue」。[`setup-matt-pocock-skills/triage-labels.md`](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/setup-matt-pocock-skills/triage-labels.md:3)、[第 7–11 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/setup-matt-pocock-skills/triage-labels.md:7)。既定前提又要求非對外契約一律對齊新版 skill，因此沒有保留第六種 repo-local state 的餘地。

- 現行文件承認 `needs-decision`「無對應」，但其意思只是「等維護者做設計決定」。[`docs/agents/triage-labels.md`](/home/cyc/Desktop/vendor-kit_ws/src/docs/agents/triage-labels.md:12)。這與 canonical `needs-triage` 的「維護者需要評估」是同一工作狀態的兩種寫法；依「一個概念一種寫法」應收斂。該原則已由 [issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71) 定案；[issue #65 的追加決議](https://github.com/ycpss91255-research/vendor_kit/issues/65#issuecomment-5893277424)也明定能共用的寫法就共用。

- `needs-info` 不適合替代：skill 明定它是「等待回報者補資料」，而 `needs-decision` 現行定義特別說不是這件事。[新版 skill](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/triage/SKILL.md:34)、[現行 mapping](/home/cyc/Desktop/vendor-kit_ws/src/docs/agents/triage-labels.md:12)。因此 open issues 唯一無歧義的對應是 `needs-triage`。這是依兩份定義作出的推論。

- 現有實例共 21 件：8 open、13 closed。[GitHub `needs-decision` 查詢](https://github.com/ycpss91255-research/vendor_kit/issues?q=label%3Aneeds-decision)。open issues 尚在等待維護者或外部決議，例如 [#31](https://github.com/ycpss91255-research/vendor_kit/issues/31) 與 [#25](https://github.com/ycpss91255-research/vendor_kit/issues/25)，所以先統一映射為 `needs-triage`，再個別 triage；不能批次猜成 `ready-for-human` 或 `wontfix`。

- closed issues 不應批次補 `wontfix`：新版 skill 將 `wontfix` 定義為「不會處理」，不等於「已完成或已有決議」。[`triage/SKILL.md`](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/triage/SKILL.md:37)。現行文件已有刪除 `backlog` 時讓 GitHub 自動從 closed issues 移除、而不另補狀態的 repo 先例。[`docs/agents/triage-labels.md`](/home/cyc/Desktop/vendor-kit_ws/src/docs/agents/triage-labels.md:16)。

- 決策內容本來就留在 issue，不需要靠 `needs-decision` 保存其歷史意義。[`docs/adr/README.md`](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/README.md:30) 規定先在 issue 討論，定案後才寫 ADR；discussion queue 也規定定案後落到對應文件或 ADR。[`discussion_queue.md`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:3)。

## 風險或反例

- `needs-triage` 的名稱可能讓人誤以為「完全尚未看過」，但 skill 的正式語意是較廣的「maintainer needs to evaluate」，足以涵蓋已蒐證但仍待拍板的議題；這是接受 canonical vocabulary 的代價。

- 不能把 8 個 open issues 視為內容完全同質。像 [#30](https://github.com/ycpss91255-research/vendor_kit/issues/30) 已有第一版決議，只是保留未來重開條件；換標後應再依內容判斷要維持 `needs-triage`、轉 `wontfix` 或直接關閉。那是後續逐票 triage，不是保留第六種狀態的理由。

- 直接刪標籤而未先遷移 open issues，會讓它們失去「需要維護者注意」的 discovery surface；因此順序應是先替換 8 個 open issues，再刪除 `needs-decision`。