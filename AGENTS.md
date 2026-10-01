## Agent skills

### Issue tracker
issue 記在 GitHub `ycpss91255-research/vendor_kit`（`gh` 一律帶 `-R ycpss91255-research/vendor_kit`，讓指令自己說出目標 repo，不依賴當下目錄的 remote 設定，也不會打到 fork）；外部 PR 不當需求來源。見 `doc/agents/issue-tracker.md`。

### Triage labels
五個標準狀態 = 同名標籤，沒有其他狀態標籤；要維護者拍板的貼 `needs-triage`（等維護者評估）。見 [triage 標籤](doc/agents/triage-labels.md)。

### Domain docs
單一語境：對外契約與承諾見 `doc/decisions/review/01_purpose.md`、名詞見根目錄 `CONTEXT.md`、不變量見 `doc/decisions/review/02_invariants.md`、ADR 見 `doc/adr/`。見 `doc/agents/domain.md`。

## 決議與文件流程

- **對外契約放 `doc/decisions/review/`，不放 issue。** 這是刻意偏離 skill 的預設（`to-prd` 會把規格發到 issue）：issue 不好追蹤改動、做不了逐頁審與標示版差異。所以 `01_purpose.md`、`02_invariants.md` 留在 repo，跑 `to-prd` 之類的 skill 時不要把它們搬進 issue。
- 每個設計決議先在 issue 討論（中文）；定案後才寫 ADR。
- ADR 放 `doc/adr/NNNN-<slug>.md`，檔案系統即登錄，不另立索引；必要段落由 lint 管，規則見 `doc/adr/README.md`。
- 每份 ADR 檔頭一行 `> Serves:` 回連它建立或服務的東西：`doc/decisions/review/02_invariants.md` 的不變量、`doc/decisions/design_principles.md` 的設計原則，或 `doc/decisions/scope_roadmap.md` 的範圍項目。沒有回連的 ADR 幾次修改後就跟產品目標脫鉤，而且是靜默的。
- 分工固定：ADR 記機制與理由；不變量頁只記「它必須永遠成立」。
- 架構圖（`.drawio`）不是插圖，是測試的依據：圖上畫的模組邊界與泳道由 lint（import-linter、鏡射、黑箱）強制。沒有被測試強制的圖，幾次修改後就跟程式脫鉤，同樣是靜默的。
- 決議改動架構圖時，同一個 PR 一起更新圖。

## git 慣例

- **一律 push 到分支，進 `main` 只能走 merge。** 不准直接 push main、更不准 force push main。遠端有 ruleset 擋（要求 PR、禁 non-fast-forward、禁刪分支），本機 `.claude/hooks/guard.py` 也擋一層。CI 按種類分 workflow：文件類在 `.github/workflows/docs.yml`（job `docs-lint`，ruleset 設為必過檢查）；之後的程式碼 lint 放 `lint.yml`、測試放 `test.yml`，一種檢查一個 job。`script/` 依類型分子目錄（規則見 [script/README.md](script/README.md)），工具自己的測試放該類別的 `test/`（目前有 `script/doc/test/`、`script/repo/test/`），由 `docs.yml` 的 job `docs-tool-test` 跑；根目錄 `test/` 只放 VK 程式碼的測試，由 `test.yml` 跑。必過的 workflow 不加 paths 過濾，否則被跳過時會一直停在 Pending。
- **一個 commit = 一個最小單元或一次完整修復。** 不要把不相干的東西包成一個 commit。依序討論出來的東西就依序 commit；一次討論定案的就一個 commit。
- `commit` 與 `push` 本身不需要詢問。

## 圖面

- 架構圖與流程圖用 drawio MCP 編輯與匯出，**不要為此引入容器或要求主機裝第三方工具** —— 那會讓這個 repo 變複雜。注意「主機只需 Docker、Git、just」是 VK 對它的使用者的承諾（不變量 5），不是這個 repo 作者流程的限制，兩者不要混。
- 圖的持久鍵是 `<diagram id>`，不是頁名也不是頁序。
