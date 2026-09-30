# r115 doc-edit 審查：docs/contract/README.md

範圍：r114（commit ebe85e3）對本檔只改了第 21 行的範例連結 `[訊息 6-23]` → `[訊息 M7]`。`_backup/docs_contract_README.pre_r115.md` 不存在，`git diff HEAD` 為空，這一輪本檔沒有新改動。

已核對、沒問題：
- 6-23 → M7 對應正確（03_messages.md 第 59 行 M7 就是 just 版本不足那條，與 04_interface.md 第 46 行引用一致）；本檔沒有其他 6-N 殘留（第 27 行的 `2026-09-30` 是日期）。
- 錨點 `03_messages.md#訊息`（03 第 41 行）、`03_messages.md#結束碼`（03 第 15 行）、`GLOSSARY.md#工具與出貨`（GLOSSARY 第 36 行）都存在。
- 已定案 1～29 條：本檔的改動沒有碰到任何一條；第 11 條（對外頁不寫出處）不適用，本檔是內部文件（AGENTS.md「其他都是內部文件（…[審閱頁說明](docs/contract/README.md)…）」）。
- 連結目標 AGENTS.md、script/README.md、docs/adr/README.md、.claude/workflows/doc-edit.js、script/mark_changes.py、doc/decisions/review_log/versions.json、.gitignore、README.md 都存在；`.gitignore` 確實忽略 `_marked/` 與 `_backup/`。
- 02 第 4 條與 ADR-0008 的改寫本檔沒有提及，無跨檔衝突。

## 必改

1. **位置**：docs/contract/README.md 第 30 行（「版本怎麼迭代」第 2 步）
   **問題**：doc-edit 的步驟寫成「改寫 → lint → codex 審查 → 套用必改 → 潤稿」，是過時資訊：漏了「跨檔一致性」與最後一次 lint；而且現行預設是 codex 改、Claude 查（審查方是改稿方的另一方），寫「codex 審查」與現況相反。AGENTS.md 規定內部文件不准留過時資訊。這不是 r114 造成的，但本檔現況就違規。
   **建議**：改成「改寫 → lint 歸零 → 每檔只讀審查（含核對已定案）並套用必改 → 跨檔一致性 → 潤稿 → lint；預設 codex 改、Claude 查」，或只寫「步驟見 [doc-edit workflow](../../.claude/workflows/doc-edit.js)」不重述（照本檔第 22 行「規則只寫一次」）。
   **證據**：.claude/workflows/doc-edit.js 第 3 行（description）、第 6～11 行（各階段）、第 22 行（editor 預設 codex，審查方永遠是另一方）；AGENTS.md「其他都是內部文件…不准留過時的資訊」。

## 建議

1. **位置**：docs/contract/README.md 第 11 行
   **問題**：「每條有固定編號」沒說編號長什麼樣。第一次來看的人看到第 21 行的 `M7` 不知道 M 是什麼；03 已補編號說明（編號只供文件互相引用、不印出、不重用）。
   **建議**：改成「每條有固定編號（M1、M2…）」，細節仍交給 03。
   **證據**：03_messages.md 第 43 行；本檔第 21 行。

2. **位置**：docs/contract/README.md 第 44 行
   **問題**：`[ADR 規則](../adr/README.md)` 的連結名與 AGENTS.md 對同一檔的稱呼「ADR 說明」不同，同一個檔兩個名字。
   **建議**：改成 `[ADR 說明](../adr/README.md)`。
   **證據**：AGENTS.md「決議與文件流程」兩處寫「[ADR 說明](docs/adr/README.md)」。
