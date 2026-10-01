## Agent skills

### Issue tracker
issue 記在 GitHub `ycpss91255-research/vendor_kit`（`gh` 一律帶 `-R ycpss91255-research/vendor_kit`，讓指令自己說出目標 repo，不依賴當下目錄的 remote 設定，也不會打到 fork）；外部 PR 不當需求來源。見 [issue tracker 約定](doc/agents/issue-tracker.md)。

### Triage labels
五個標準狀態 = 同名標籤，沒有其他狀態標籤；要維護者拍板的貼 `needs-triage`（等維護者評估）。見 [triage 標籤](doc/agents/triage-labels.md)。

### Domain docs
單一語境：對外契約與承諾見 `doc/contract/01_purpose.md`、名詞見根目錄 `GLOSSARY.md`、不變量見 `doc/contract/02_invariants.md`、ADR 見 `doc/adr/`。見 [domain 文件約定](doc/agents/domain.md)。

### 工作區
repo 上一層的 `vendor-kit_ws/` 是工作區：`src/` 是這個 repo；`worktree/` 放 git worktree（`pr/<N>`、`issue/<N>`、`branch/<名>`）；`reference/`、`demo/` 是本機參考資料，不進 git。

## 決議與文件流程

- **對外契約放 `doc/contract/`，不放 issue。** 這是刻意偏離 skill 的預設（`to-prd` 會把規格發到 issue）：issue 不好追蹤改動、做不了逐頁審與標示版差異。所以 `01_purpose.md`、`02_invariants.md`、`03_messages.md`、`04_interface.md` 留在 repo，跑 `to-prd` 之類的 skill 時不要把它們搬進 issue。
- **目錄一律用 `doc/`，不用 `docs/`。** 這是刻意偏離 skill 的預設：`.agents/skills/` 是外部引入的 skill，內文寫的 `docs/adr/`、`docs/agents/` 等一律讀成 `doc/adr/`、`doc/agents/`。skill 本身不改，改了以後同步上游會衝突；根目錄出現 `docs/` 時 [check_terms.py](script/check_terms.py) 會擋下來。
- 每個設計決議先在 issue 討論（中文）；定案後才寫 ADR。
- **issue 本文與標題開好後不改，一律留言。** 這是刻意偏離 skill 的預設（wayfinder 會改 map 本文的「Decisions so far」）：新定案改在 map 留言記錄，map 本文的 Decisions so far、Not yet specified、Out of scope 等節的更新也一律留言，決策清單看 GitHub 的 sub-issue 面板。改本文、標題，或 agent 留言沒帶 `[claude]`／`[codex]`／`[agy]` 標記，會被 `.claude/hooks/` 的 hook 擋下。做法見 [issue tracker 約定](doc/agents/issue-tracker.md)。
- **對外文件的審閱流程照[審閱頁說明](doc/contract/README.md)「版本怎麼迭代」做。** 對外文件是根目錄 [README](README.md) 與審閱頁 01～04。重點：
  1. 草稿只改在討論分支並開 PR；`main` 上只放定案版，維護者針對那一頁明確回覆「定案」才 merge。
  2. 改動一律跑 doc-edit workflow；round 名稱是 `rNN`，取本機 `doc/decisions/_backup/`（已移出 git、只留本機）裡最大的 `pre_rNN` 與 git log 裡 `Doc-Edit: rNN` footer 兩者的最大編號再加一，不能重用；workflow 開跑時會檢查 round 的格式是不是 `rNN`、是不是最大編號加一，重用或跳號就直接停。
  3. 改完跑 [標示版產生器](script/mark_changes.py)：在送審資料夾 `doc/review/<鍵>/` 產出固定檔名的正文副本 `<鍵>.md` 與標示版 `<鍵>.marked.md`，有 CSV 的頁再加 `<鍵>.csv`，每次產生就覆蓋。基準預設是該鍵最後一次送審的版本。版本號不在 repo 的檔名或檔內，只在送審 zip 裡的檔名（`<鍵>.v<N>.…`）：[打包工具](script/pack_review.py)打包送審資料夾時取號，並把這次送審的版號與 commit 追加進 `doc/review/versions.json`；正式檔有未 commit 的改動或副本過期就停下。正式檔名不改。定稿時把整個送審資料夾在同一個 commit 刪掉。
  4. 把送審 zip 傳給維護者審，不傳正式檔。審查與調查結論寫進 issue 留言；`doc/decisions/review_log/`、`doc/research/` 已移出 git，只留本機。
- 其他都是內部文件（本檔、[工具說明](script/README.md)、[決議目錄說明](doc/decisions/README.md)、[workflow 說明](.claude/workflows/README.md)、[審閱頁說明](doc/contract/README.md)、[ADR 說明](doc/adr/README.md) 等）：改完照樣走 doc-edit workflow，但不產標示版、不送審，而且不准留過時的資訊（已不用的做法、已不存在的檔）。只記錄歷史的句子可以留，但要寫明是歷史。
- ADR 放 `doc/adr/NNNN-<slug>.md`，格式照 domain-modeling skill 的 [ADR 格式](.agents/skills/domain-modeling/ADR-FORMAT.md)（見 [ADR 說明](doc/adr/README.md)）。只有三項都成立才寫 ADR：難逆轉、沒背景會令人意外、確實取捨過。
- 分工固定：ADR 記決定與理由；不變量頁只記「它必須永遠成立」。
- 架構圖（`.drawio`）不是插圖，是測試的依據：repo 裡目前沒有架構圖（舊模型的圖已移出 repo）；之後依新名詞重畫的圖，圖上畫的模組邊界與泳道由 lint（import-linter、鏡射、黑箱）強制，lint 在重畫時一起實作。沒有被測試強制的圖，幾次修改後就會靜默地跟程式脫鉤。
- 決議改動架構圖時，同一個 PR 一起更新圖。

## git 慣例

- **一律 push 到分支，進 `main` 只能走 merge。** 不准直接 push main、更不准 force push main。遠端有 ruleset 擋（要求 PR、禁 non-fast-forward、禁刪分支），本機 `.claude/hooks/guard.py` 也擋一層。CI 按種類分 workflow：文件類在 `.github/workflows/docs.yml`（job `docs-lint`，ruleset 設為必過檢查）；之後的程式碼 lint 放 `lint.yml`、測試放 `test.yml`，一種檢查一個 job。文件工具的測試放 `script/test/`，由 `docs.yml` 的 job `docs-tool-test` 跑；根目錄 `test/` 只放 VK 程式碼的測試，由 `test.yml` 跑。必過的 workflow 不加 paths 過濾，否則被跳過時會一直停在 Pending。
- **一個 commit = 一個最小單元或一次完整修復。** 不要把不相干的東西包成一個 commit。依序討論出來的東西就依序 commit；一次討論定案的就一個 commit。
- `commit` 與 `push` 本身不需要詢問。

## 圖面

- 架構圖與流程圖用 drawio MCP 編輯與匯出，**不要為此引入容器或要求主機裝第三方工具**：那會讓這個 repo 變複雜。「主機只需 Docker、Git、just」是 VK 對它的使用者的承諾（不變量 5），不是這個 repo 作者流程的限制，兩者不要混。
- 圖的持久鍵是 `<diagram id>`，不是頁名也不是頁序。
