## 必改

- `doc/decisions/review/02_invariants.md:1`：標題仍是「03 不變量」，應改成「02 不變量」。
- `doc/decisions/review/02_invariants.md:396`：「照 01–03 的名詞寫」仍沿用三頁結構，應改成引用根 `CONTEXT.md`。
- `doc/decisions/review/02_invariants.md:93`：「專案檔」是舊詞，應改成「repo 檔」。
- `doc/decisions/review/01_purpose.md:1`：「專案目的與承諾」仍用舊詞，應改成「repo 目的與承諾」或不含「專案」的標題。
- `CONTEXT.md:94`：「本專案的簡稱」仍用舊詞，應改成「本 repo 的簡稱」。
- `doc/agents/domain.md:8,20`：「專案的專有名詞表／專案沒在用的語言」應統一改成「repo」。
- `doc/decisions/design_principles.md:13,23,27,28,60`：現行原則仍使用「介面動詞／明確動詞／動詞改名」，應統一改成「recipe」。
- `doc/decisions/scope_roadmap.md:18`：「引擎子命令與九個動詞」應改成 VK recipe 的現行說法。
- `doc/adr/README.md:42,51,52`：「專案鎖定／介面動詞／專案根」應分別改成「repo 鎖定／介面 recipe／安裝目錄」。
- `doc/adr/TEMPLATE.md:33`：「工具 repo 開發者」是 `_Avoid_` 詞，應改成現行角色名稱「使用者」。
- `doc/adr/0003-why-not-existing-tools.md:47`：「三方合併」應改成「基準版合併」。
- `doc/decisions/README.md:15`：「專案目的與承諾」應與改名後的 `01_purpose.md` 標題同步。
- `doc/decisions/README.md:16,76`：實際已有 11 條不變量，應把「八條不變量」改為「十一條不變量」。
- `doc/decisions/README.md:29,30,96,102`：實際有 49 個 `review_log` 檔與 143 個 `_backup` 檔，應更新仍寫成 48 與 126 的盤點數字。
- `doc/decisions/README.md:114-120`：所稱 `domain.md` 的「檔案結構」區塊實際已不存在，整個待處理項目應移除或改寫為已完成。
- `doc/decisions/review/_marked/`：仍留有 `.02_terms.rev`、`.03_invariants.rev`、`02_terms.v4.marked.md`、`03_invariants.v7.marked.md`，應清理或重產為目前兩頁的名稱。
- `AGENTS.md:4`、`doc/agents/issue-tracker.md:7`：兩處都宣稱本目錄沒有 remote，但實際已有指向 `ycpss91255-research/vendor_kit` 的 `origin`，應更新結構描述並重新說明強制 `-R` 的理由。
- `doc/decisions/README.md:5,29,32,34,36,42,66,92,100,118`：新內容直接引用 `_legacy/` 或 `grilling.md`，依「新內容不得引用」規則應移除這些引用或只保留不帶路徑的歸檔狀態。
- `doc/agents/domain.md:14`、`doc/agents/issue-tracker.md:49`：仍出現 `/grill-with-docs` 與 `grilling` 類型，若禁用範圍涵蓋所有 grilling 名稱，應一併移除或改名。

## 建議

- `doc/decisions/README.md:40,44-45,56`：這些舊詞是在描述歸檔內容或舊模型，建議明確加上「僅為歷史名稱，不得沿用」，避免被認作現行語言。
- `doc/decisions/README.md:31`：既然 `_marked/` 被定義為可重產產物，建議補充改名或移除審閱頁時必須同步清掉舊名稱產物。
- `doc/agents/domain.md:12`、`doc/decisions/README.md:104-112`：proto 的 ADR-0001、0002 路徑目前存在且互相一致，建議搬回時把兩處說明放在同一變更中刪除。
- `CONTEXT.md:93-336`：多數名詞沒有格式要求的 `_Avoid_` 行，建議補上 `_Avoid_: 無` 或明確同義詞，使每個名詞都符合指定格式。

## 沒問題

- `AGENTS.md:10,16`：目的、根 `CONTEXT.md`、`02_invariants.md` 與 `doc/adr/` 的現行位置均正確。
- `doc/agents/domain.md:7-10`、`doc/agents/issue-tracker.md:3`：領域文件的四個現行位置與實際檔案一致。
- `doc/decisions/README.md:44`：`02_terms.md` 確實已移至 `doc/decisions/_legacy/review/02_terms.md`，且內容已重寫進根 `CONTEXT.md`。
- `script/README.md:12-32`、`script/mark_changes.py:9-25`：範例與程式都已使用 `02_invariants`，沒有殘留 `03_invariants` 或 `02_terms`。
- `CONTEXT.md:99,104,129,143,168,192,271,282`：舊詞只出現在 `_Avoid_`，符合改名規則，不算殘留誤用。
- 所有指定範圍內的 Markdown 相對路徑連結：目標均存在，沒有壞連結。