## Agent skills

### Issue tracker
issue 記在 GitHub `ycpss91255-research/vendor_kit`（`gh` 一律帶 `-R ycpss91255-research/vendor_kit`，讓指令自己說出目標 repo，不依賴當下目錄的 remote 設定，也不會打到 fork）；外部 PR 不當需求來源。見 `doc/agents/issue-tracker.md`。

### Triage labels
五個標準狀態 = 同名標籤；另有 `needs-decision`（等維護者拍板）。見 `doc/agents/triage-labels.md`。

### Domain docs
單一語境：對外契約與承諾見 `doc/decisions/review/01_purpose.md`、名詞見根目錄 `CONTEXT.md`、不變量見 `doc/decisions/review/02_invariants.md`、ADR 見 `doc/adr/`。見 `doc/agents/domain.md`。

## 決議與文件流程

- 每個設計決議先在 issue 討論（中文）；定案後才寫 ADR。
- ADR 放 `doc/adr/NNNN-<slug>.md`，檔案系統即登錄，不另立索引；必要段落由 lint 管，規則見 `doc/adr/README.md`。
- 每份 ADR 檔頭一行 `> Serves:` 回連它建立或服務的東西：`doc/decisions/review/02_invariants.md` 的不變量、`doc/decisions/design_principles.md` 的設計原則，或 `doc/decisions/scope_roadmap.md` 的範圍項目。沒有回連的 ADR 幾次修改後就跟產品目標脫鉤，而且是靜默的。
- 分工固定：ADR 記機制與理由；不變量頁只記「它必須永遠成立」。
- 架構圖（`.drawio`）不是插圖，是測試的依據：圖上畫的模組邊界與泳道由 lint（import-linter、鏡射、黑箱）強制。沒有被測試強制的圖，幾次修改後就跟程式脫鉤，同樣是靜默的。
- 決議改動架構圖時，同一個 PR 一起更新圖。
