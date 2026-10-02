# Issue tracker：GitHub

本 repo 的 issue 與實作 ticket（issue 層級的 spec）放在 GitHub `ycpss91255-research/vendor_kit`；對外契約只放 `doc/contract/`，不發成 issue，見[工作約定](../../AGENTS.md#決議與文件流程)。所有操作一律用 `gh` CLI。對外契約與承諾見 `doc/contract/01_purpose.md`、名詞見根 `GLOSSARY.md`、不變量見 `doc/contract/02_invariants.md`、ADR 見 `doc/adr/`。

## 總則：issue 本文與標題開好後不改

issue 的本文與標題開好後就不再修改；補充、進度、結論一律用 `gh issue comment` 留言。

- **留言標記**：agent 發的留言，本文第一行開頭固定是 `[claude]`、`[codex]` 或 `[agy]`，空一格接標題（例如 `[codex] 第 1 輪複驗`、`[claude] 研究結論`）；沒有標記的留言一律視為維護者本人寫的。
- `[codex]`、`[agy]` 只貼該工具的原文，Claude 不代寫；太長就拆成多則，每則都帶標記。
- 舊留言不改，要更正就另發一則。
- 標籤、assignee、關閉 issue 照常可以用 `gh issue edit`／`gh issue close`；只有本文與標題不改。
- `gh issue create`、`gh pr create` 一律用 `--body-file`，issue 要帶標籤；不用 `gh issue close --comment`，先留言再關。

## 為什麼每個 `gh` 都明寫 `-R`

`gh` 不帶 `-R` 時會靠當下目錄的 remote 推出目標 repo：推得出來也是推測，換個目錄、worktree 或 submodule 就換了答案，有 fork 的 remote 時還會打到 fork。所以慣例是**每個指令都明寫 `-R ycpss91255-research/vendor_kit`**，讓指令自己說出目標，跟從哪裡執行無關。

## 慣例

**用腳本寫入**：開 issue、留言、關閉、開 PR、merge 這些寫入，用 `script/github/` 與 `script/workflow/` 的腳本，不要逐一下 `gh`。用法、輸出 JSON 與結束碼見 [script/github/README.md](../../script/github/README.md)，`merge_pr.py` 見它的檔頭說明。

- **開 issue**（可帶父題）：`python3 script/github/issue_open.py create --title "..." --label "..." --body-file <檔> [--parent <N>]`。結束碼 3 表示 issue 已開、只有掛 sub-issue 失敗，用 `python3 script/github/issue_open.py attach --parent <P> --issue <N>` 重試，不要再 `create`。
- **留言**：`python3 script/github/post_comments.py --kind issue|pr --number <N> --body-file <檔> [<檔> …]`。
- **先留言再關 issue**：`python3 script/github/post_comments.py --kind issue --number <N> --body-file <檔> --close`。
- **開 PR**：`python3 script/github/pr_open.py --repo <worktree> --branch <分支> --issue <N> --body-file <檔> --title-from-commit`。
- **等 CI 後 merge**：`python3 script/workflow/merge_pr.py <pr>`。

這些腳本在每個寫入之前，都把即將執行的同一個指令交給 `.claude/settings.json` 註冊的同一批 Bash hook 檢查，被擋就不寫。下面的 `gh` 指令清單照舊：唯讀指令與腳本沒涵蓋的情況照用。

- **建立 issue**：`gh issue create -R ycpss91255-research/vendor_kit --title "..." --body-file <檔> --label "..."`。
- **讀 issue**：`gh issue view <number> -R ycpss91255-research/vendor_kit --comments`；需要時用 `jq` 過濾留言，並一併抓標籤。
- **列 issue**：`gh issue list -R ycpss91255-research/vendor_kit --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，視情況加 `--label`、`--state`。
- **留言**：`gh issue comment <number> -R ycpss91255-research/vendor_kit --body "..."`
- **加／移標籤**：`gh issue edit <number> -R ycpss91255-research/vendor_kit --add-label "..."` ／ `--remove-label "..."`
- **關閉**：先 `gh issue comment <number> -R ycpss91255-research/vendor_kit --body-file <檔>`，再 `gh issue close <number> -R ycpss91255-research/vendor_kit`

## 語言與內容

- issue、PR、留言一律用中文（指令、識別字、檔名保留原文）。
- **設計決議與定案用留言記錄**（見總則）。
- 遇到需要維護者拍板的問題（設計取捨、契約要不要改、方案 A 或 B），貼 `needs-triage`（等維護者評估），不要貼 `needs-info`；`needs-info` 只用在等回報者補資料。

## Pull request 當作需求來源

**PRs as a request surface: no.** _（若本 repo 把外部 PR 當功能需求，改成 `yes`；`/triage` 會讀這個旗標。）_

設為 `yes` 時，PR 走跟 issue 一樣的標籤與狀態，改用 `gh pr` 對應指令：

- **讀 PR**：`gh pr view <number> -R ycpss91255-research/vendor_kit --comments`，diff 用 `gh pr diff <number> -R ycpss91255-research/vendor_kit`。
- **列外部 PR 做 triage**：`gh pr list -R ycpss91255-research/vendor_kit --state open --json number,title,body,labels,author,authorAssociation,comments`，只留 `authorAssociation` 為 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR`、`NONE` 的（丟掉 `OWNER`／`MEMBER`／`COLLABORATOR`）。
- **留言／標籤／關閉**：`gh pr comment`、`gh pr edit --add-label`／`--remove-label`、`gh pr close`，都帶 `-R`。

GitHub 的 issue 與 PR 共用同一個編號空間，光看 `#42` 分不出是哪種：先 `gh pr view 42 -R ycpss91255-research/vendor_kit`，失敗再 `gh issue view 42 -R ycpss91255-research/vendor_kit`。

## 當 skill 說「publish to the issue tracker」

建一個 GitHub issue（帶 `-R`）。

## 當 skill 說「fetch the relevant ticket」

跑 `gh issue view <number> -R ycpss91255-research/vendor_kit --comments`。

## Wayfinding 操作

給 `/wayfinder` 用。**map** 是一個 issue，**child** issue 是它底下的 ticket。

- **Map**：一個貼 `wayfinder:map` 標籤的 issue，本文只放 Destination 與 Notes，開好後不改。「Decisions so far」不寫在本文：新的定案在 map 留言記錄（一句重點＋連結），決策清單以 GitHub 的 sub-issue 面板為準；「Not yet specified」「Out of scope」等其他節也一樣，更新一律用留言。`gh issue create -R ycpss91255-research/vendor_kit --title "..." --body-file <檔> --label wayfinder:map`。
- **Child ticket**：以 GitHub sub-issue 連到 map 的 issue（用 `gh api` 打 sub-issues endpoint）。sub-issue 沒開的話，開 child 時就在 child 本文最上面寫 `Part of #<map>`；開好後才要補的，用留言記錄。標籤：`wayfinder:<type>`（`research`／`prototype`／`grilling`／`task`）。被認領後，ticket 指派給負責的開發者。
- **Blocking**：用 GitHub **原生 issue dependencies**，這是正式、UI 看得到的表示法。加一條邊：`gh api --method POST repos/ycpss91255-research/vendor_kit/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`，`<blocker-db-id>` 是 blocker 的數字 **database id**（`gh api repos/ycpss91255-research/vendor_kit/issues/<n> --jq .id`，_不是_ `#number` 也不是 `node_id`）。GitHub 會回報 `issue_dependencies_summary.blocked_by`（只算還開著的 blocker，這就是即時閘門）。dependencies 不可用時，退回在開 child 時就於本文最上面寫一行 `Blocked by: #<n>, #<n>`；開好後才要補的，用留言記錄。所有 blocker 都關閉，ticket 才算解除封鎖。
- **Frontier query**：列 map 底下還開著的 child（`gh issue list -R ycpss91255-research/vendor_kit --state open`，限定在 map 的 sub-issue／task list 範圍），剔除有開著的 blocker（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 那行有還開著的 issue）或已有 assignee 的；依 map 順序第一個勝出。
- **Claim**：`gh issue edit <n> -R ycpss91255-research/vendor_kit --add-assignee @me`，這是該 session 的第一次寫入。
- **Resolve**：`gh issue comment <n> -R ycpss91255-research/vendor_kit --body "<answer>"`，接著 `gh issue close <n> -R ycpss91255-research/vendor_kit`，再到 map 留言一句重點＋連結。
