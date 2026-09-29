## Agent skills

### Issue tracker
issue 記在 GitHub `ycpss91255-research/vendor_kit`（`gh` 一律帶 `-R ycpss91255-research/vendor_kit`，讓指令自己說出目標 repo，不依賴當下目錄的 remote 設定，也不會打到 fork）；外部 PR 不當需求來源。見 [issue tracker 約定](doc/agents/issue-tracker.md)。

### Triage labels
五個標準狀態 = 同名標籤；另有 `needs-decision`（等維護者拍板）。見 [triage 標籤](doc/agents/triage-labels.md)。

### Domain docs
單一語境：對外契約與承諾見 `doc/decisions/review/01_purpose.md`、名詞見根目錄 `CONTEXT.md`、不變量見 `doc/decisions/review/02_invariants.md`、ADR 見 `doc/adr/`。見 [domain 文件約定](doc/agents/domain.md)。

## 決議與文件流程

- **對外契約放 `doc/decisions/review/`，不放 issue。** 這是刻意偏離 skill 的預設（`to-prd` 會把規格發到 issue）：issue 不好追蹤改動、做不了逐頁審與標示版差異。所以 `01_purpose.md`、`02_invariants.md`、`03_interface.md` 留在 repo，跑 `to-prd` 之類的 skill 時不要把它們搬進 issue。
- 每個設計決議先在 issue 討論（中文）；定案後才寫 ADR。
- **對外文件的審閱流程照[審閱頁說明](doc/decisions/review/README.md)「版本怎麼迭代」做。** 對外文件是根目錄 [README](README.md) 與審閱頁 01～03。重點：
  1. 草稿只改在討論分支並開 PR；`main` 上只放定案版，維護者針對那一頁明確回覆「定案」才 merge。
  2. 改動一律跑 doc-edit workflow；round 名稱是 `rNN`，取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一，不能重用；workflow 開跑時會檢查 round 的格式是不是 `rNN`、是不是最大編號加一，重用或跳號就直接停。
  3. 改完跑 [標示版產生器](script/mark_changes.py)：正式檔檔頭寫入 `> 版本 vN`（N 取本機 `doc/decisions/_marked/.<鍵>.rev` 與正式檔檔頭現有版本號兩者較大的再加一，換電腦或新 clone 不會從 v1 重來），`doc/decisions/_marked/` 產出檔名帶版本號的標示版 `<鍵>.vN.marked.md` 與正文副本 `<鍵>.vN.md`；正式檔名不改。
  4. 這兩個帶版本號的檔一起傳給維護者審，不傳正式檔。
- 其他都是內部文件（本檔、[工具說明](script/README.md)、[決議目錄說明](doc/decisions/README.md)、[workflow 說明](.claude/workflows/README.md)、[審閱頁說明](doc/decisions/review/README.md)、[ADR 規則](doc/adr/README.md) 等）：改完照樣走 doc-edit workflow，但不產標示版、不送審，而且不准留過時的資訊（已不用的做法、已不存在的檔）。只記錄歷史的句子可以留，但要寫明是歷史。
- ADR 放 `doc/adr/NNNN-<slug>.md`，檔案系統是正式登錄；[ADR 規則](doc/adr/README.md)裡的表只是彙整檢視，不是另一份登錄。必要段落規則見 [ADR 規則](doc/adr/README.md)；lint 待寫。
- 每份 ADR 檔頭一行 `> Serves:` 回連它建立或服務的東西：`doc/decisions/review/02_invariants.md` 的不變量、`doc/decisions/design_principles.md` 的設計原則，或 `doc/decisions/scope_roadmap.md` 的範圍項目。沒有回連的 ADR 幾次修改後就跟產品目標脫鉤，而且是靜默的。
- 分工固定：ADR 記機制與理由；不變量頁只記「它必須永遠成立」。
- 架構圖（`.drawio`）不是插圖，是測試的依據：圖上畫的模組邊界與泳道預定由 lint（import-linter、鏡射、黑箱）強制，目前尚未實作。沒有被測試強制的圖，幾次修改後就跟程式脫鉤，同樣是靜默的。
- 決議改動架構圖時，同一個 PR 一起更新圖。

## git 慣例

- **一律 push 到分支，進 `main` 只能走 merge。** 不准直接 push main、更不准 force push main。遠端有 ruleset 擋（要求 PR、禁 non-fast-forward、禁刪分支），本機 `.claude/hooks/guard.py` 也擋一層。CI 按種類分 workflow：文件類在 `.github/workflows/docs.yml`（job `docs-lint`，ruleset 設為必過檢查）；之後的程式碼 lint 放 `lint.yml`、測試放 `test.yml`，一種檢查一個 job。必過的 workflow 不加 paths 過濾，否則被跳過時會一直停在 Pending。
- **一個 commit = 一個最小單元或一次完整修復。** 不要把不相干的東西包成一個 commit。依序討論出來的東西就依序 commit；一次討論定案的就一個 commit。
- `commit` 與 `push` 本身不需要詢問。

## 圖面

- 架構圖與流程圖用 drawio MCP 編輯與匯出，**不要為此引入容器或要求主機裝第三方工具**：那會讓這個 repo 變複雜。注意「主機只需 Docker、Git、just」是 VK 對它的使用者的承諾（不變量 5），不是這個 repo 作者流程的限制，兩者不要混。
- 圖的持久鍵是 `<diagram id>`，不是頁名也不是頁序。
