# 命名 workflow — 任務執行一律走這裡

多步驟、會派子代理的任務不要臨時寫一次性腳本，改用這個目錄下的**命名 workflow**：腳本固定當模板，每次只換一份 `args`。

## 為什麼不是 JSON

看起來「任務流程」應該可以寫成一份 JSON 或 YAML，然後每次換內容就好。做不到，因為 Workflow 工具吃的是 JS 腳本，而腳本裡有兩種東西：

- **不可參數化的部分**：控制流本身。哪幾組並行、誰的輸出餵給誰、哪些條件才進下一階段、結果怎麼彙整成回傳值——這是程式，寫成資料就得再發明一套迷你語言。`meta` 雖然必須是純字面值（不可以有變數、函式呼叫、展開、模板字串插值），但它只是註冊資訊，不是流程。
- **可參數化的部分**：`args`。要改哪些檔、每組子代理的任務描述、備份後綴、跑幾軌、effort 高低——這些每次都不一樣，而 `args` **就是 JSON**。

所以慣例是：**腳本寫一次進 git 當模板，之後每次任務只準備一份 args JSON**。要換的是 args，不是腳本。腳本要改的時機只有一個：流程形狀真的變了。

## 調用方式

```js
Workflow({ name: "doc-edit", args: { /* 這份 JSON 是每次唯一要換的東西 */ } })
```

- 腳本放這個目錄（`.claude/workflows/`），**檔名去掉 `.js` 就是 `name`**。
- 這些腳本已經進 git，跟 repo 一起版本控管；一次性腳本不進 repo。
- `args` 缺必填欄位時腳本會 throw，錯誤訊息會講清楚缺什麼。

## 現有 workflow

| 名字 | 用途 | 什麼時候跑 | args 必填 |
|---|---|---|---|
| `doc-edit` | 改文件的固定流程（每個檔並行）：改寫 → lint 歸零 → 只讀審查並套用必改 → 跨檔一致性 → humanizer-zh-tw 潤稿 → lint；預設 codex 改、Claude 查，`editor` 可對調；`mode: "light"` 給機械式或只改幾行的改動，只用 Claude 子代理、不跑跨檔一致性與潤稿；建議只回報。取代已刪除的 `doc-apply` 與 `doc-review` | 改任何現行文件（README、`doc/contract/`、`GLOSSARY.md`、ADR）時；主對話不自己改 | `round`、`files` |
| `discuss` | codex 與 Claude 各自回答、最多 3 輪比對，未收斂交維護者 | 問維護者之前；結果回報主對話，貼到 #78 對應的 child issue | `round`、`questions`（每項 `{ id, question, context }`） |
| `research` | agy 查 → codex 核對 → Claude 整合 → 貼 issue。brief 放 workspace 的 `reference/research/<issue>/<id>_brief.md`，輸出也放那裡，不放 `/tmp`；整合結論寫到 `claude_review_<id1>_<id2>….md`（依 `briefs` 順序串接 id），同一 issue 換一批 brief 再跑不會覆蓋；agy 一律用最新的 gemini flash-high 模型（自動選），可用 `agyModel` 指定 | 要找外部前例或資料當決策依據時；brief 先寫好 | `issue`、`topic`、`briefs`（每項 `{ id, label }`） |
| `pr` | 依序把每一項做成一個 PR：開 issue 掛成 sub-issue、開 worktree、修改、驗證、commit、開 PR、等 CI，可選 merge | 要開一個或多個「一個 issue 一個 PR」的改動時 | `parent`、`items` |
| `pr-fix` | 在已開 PR 的 worktree 修一個問題：查分支／worktree／issue 並確認乾淨且最新 → 修改 → 全部驗證 → 一個 commit → push → 等 CI；不 merge | PR 已經開了、CI 或審查要求再改時；CI 通過就停 | `pr`、`problem`、`todo`、`commit` |

`doc-edit` 的選填欄位：`repo`（預設 `/home/cyc/Desktop/vendor-kit_ws/src`）、`ask`（不給就跳過「改寫」）、`background`、`codex_focus`（審查額外要看的重點）、`editor`（`codex` 預設｜`claude`）、`mode`（`full` 預設｜`light`）、`effort`（`{ edit, polish, review }`）、`topic`（短主題，例如 `"#121"`）。`discuss` 的選填欄位：`background`（已定案前提）、`repo`（預設 `/home/cyc/Desktop/vendor-kit_ws/src`；要用 PR worktree 時明確帶）。`research` 的選填欄位：`dir`（預設 `/home/cyc/Desktop/vendor-kit_ws/reference/research/<issue>`）、`background`（已定案前提）、`post`（預設 `true`；`false` 就只產檔、不貼 issue）、`agyModel`（指定 agy 模型名；不給就自動選最新的 gemini flash-high 模型）。`research` 每次執行開頭印出識別 `research #<issue>`，子代理的 label 也帶 `#<issue>` 前綴。`pr` 與 `pr-fix` 的參數見下面。

## doc-edit

每次執行開頭會印出識別 `doc-edit <round> <topic>`，子代理的 label 也帶同一個前綴，方便分辨同時跑的幾次。

`round` 是 `rNN`，取兩者的最大值加一：本機 `doc/decisions/_backup/` 裡最大的 `pre_rNN`，與 git log 裡 `Doc-Edit: rNN` footer 的最大值。`_backup/` 不進 git，只看它會在別台機器或清過本機後重用舊編號。

args 範例在 `doc-edit.js` 檔尾，可以直接貼進 `args`。

## pr

清單依序執行，每一項一個子代理，從開 issue 做到等 CI（`merge: true` 時再 merge 與清理）。任何一步失敗就停下：不 merge，後面的項目也不開始。開始時印出 `pr #<parent> <no 清單>`，每個子代理的 label 是 `#<parent>-<no>`。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `parent` | 是 | 父題的 issue 編號。新 issue 第一行 `Part of #<parent>`，並掛成它的 sub-issue |
| `items` | 是 | 陣列，每項 `{ no, branch, title, content, commit, label? }`：編號、分支、issue 標題、要做的內容、commit 訊息（第一行也當 PR 標題）、issue 標籤（預設 `enhancement`） |
| `merge` | 否 | 預設 `false`。`true`＝CI 全過後 `gh pr merge --merge`，再 pull 主 repo、移除 worktree 與本機分支 |
| `repoRoot` | 否 | 主 repo，預設 `/home/cyc/Desktop/vendor-kit_ws/src`。worktree 開在它上一層的 `worktree/branch/<branch>`，本文檔暫放上一層的 `reference/research/pr/` |

每一項的步驟：

1. 開 issue（本文先寫成檔、`body.py check` 自檢、`gh issue create --body-file`），再用 sub_issues API 掛到父題。
2. `script/workflow/worktree.py add <branch>` 從 origin/main 開 worktree。
3. 照 `content` 修改。
4. 驗證：`.github/workflows/docs.yml` 列的每一步原樣跑、每個 `script/*/test` 的 unittest、`check_script_layout.py`、`.claude/hooks/test_guard.py`，全部要過。
5. commit（footer `Refs: #<issue>`，不加 Claude 署名）、push。
6. 開 PR：本文第一行 `[claude] `、含 `Closes #<issue>`，自檢後 `gh pr create --body-file`。
7. `script/workflow/wait_ci.py <pr>` 等 CI。
8. `merge: true` 且 CI 全過才 merge，之後 `worktree.py remove <branch>` 清理。

`pr` 本來就要 commit、push 與開 PR，所以不套下面「共用護欄」的不寫 git 與備份兩條；它自己的規則（只 push 自己的分支、本文先寫檔自檢、不加署名等）同樣組進每個子代理的 prompt。

分工：機械步驟呼叫 [`script/workflow/`](../../script/workflow/README.md) 的腳本；會寫入 GitHub 的 `gh` 指令不包進腳本，由子代理逐一下，hook 才看得到。子代理自己判斷的只有怎麼修改、驗證失敗時要修還是停下。

回傳 `{ parent, merge, results, stopped, skipped }`：`results` 每項有 `issue`、`pr`、`pr_url`、`ci_pass`、`merged`、`cleaned`、`summary`、`error`；`stopped` 是停在哪一項與原因，`skipped` 是沒開始的編號。

args 範例：

```json
{
  "parent": 140,
  "merge": false,
  "items": [
    {
      "no": 1,
      "branch": "feat/check-links",
      "title": "script/doc/check_links.py：檢查 md 的相對連結",
      "content": "新增 script/doc/check_links.py：掃 git ls-files 的 .md，相對連結的目標檔與錨點要解得開；附 script/doc/test/ 的 unittest；docs.yml 的 docs-lint 加一步跑它；script/doc/README.md 補一節。",
      "commit": "feat(doc): check_links 檢查 md 的相對連結",
      "label": "enhancement"
    }
  ]
}
```

## pr-fix

修已開的 PR。開始時印出 `pr-fix #<pr>`，子代理的 label 是 `#<pr> 準備`、`#<pr> 修改`。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `pr` | 是 | PR 編號。分支、worktree、issue 都由 `script/workflow/pr_target.py` 查，不用自己帶 |
| `problem` | 是 | 要修的問題 |
| `todo` | 是 | 要做的事 |
| `commit` | 是 | commit 訊息第一行（`type(scope): 摘要`），只能一行；footer `Refs: #<issue>` 由 workflow 補 |
| `repoRoot` | 否 | 主 repo。不給就用子代理的工作目錄，實際位置以 `pr_target.py` 回報的 `repo` 為準 |

步驟：

1. 準備：`script/workflow/pr_target.py <pr>` 用唯讀的 `gh pr view` 取分支（headRefName）與本文，issue 取本文第一個 `Closes`／`Refs #N`；worktree 在 `worktree/branch/<分支>`，不存在就從 `origin/<分支>` 建；確認乾淨、沒有沒推的 commit，落後遠端就 fast-forward。失敗就停，不進下一步。
2. 照 `problem`、`todo` 在 worktree 修改。
3. 驗證：`script/workflow/verify.py --root <worktree>`，跑 docs.yml 每個 `run:`、每個 `script/*/test`、`check_script_layout.py`、`.claude/hooks/test_guard.py`，並檢查每個 `script/*/test` 都在 docs.yml 裡。
4. 一個 commit（footer `Refs: #<issue>`，不加 Claude 署名），一般 push；只有要 rebase 到 origin/main 時才 `--force-with-lease`，只限這個分支。
5. `script/workflow/wait_ci.py <pr>` 等 CI；失敗且是這次改動造成的就再修、commit、push、再等。CI 全過就停。

不 merge、不開 PR、不碰主 repo（不改檔、不 pull、不動未追蹤檔）。回傳 `{ pr, branch, issue, url, ci_pass, pushed, commit, summary, error }`。

args 範例在 `pr-fix.js` 檔尾。

## 共用護欄

這幾條**寫在腳本裡**，會組進送給每個子代理的 prompt，不靠每次記得講：

- **不 commit、不 push、不跑任何 git 寫入指令**。唯讀的 `git status`／`git diff` 可以。
- **改前先備份**到 `doc/decisions/_backup/`，命名 `<鍵>.pre_<round><副檔名>`（例如 `claude_workflows_README.pre_r146.md`；鍵與副檔名的規則跟 `script/doc/mark_changes.py` 同一套），同名已存在就在副檔名前加序號。
- **不准動** `doc/decisions/_legacy/`、`doc/decisions/_backup/`、`doc/decisions/review_log/`、`doc/decisions/review/_marked/`——歷史快照與本地產物，除非該 task 明說。
- **驗證一律用腳本／grep 算，不要目視**。
- codex 一律帶 `< /dev/null`：省了 codex 會停在等 stdin，整條 workflow 卡死。指令形狀固定：

  ```
  codex exec --skip-git-repo-check -C <repo> -o <輸出檔> "<brief>" < /dev/null
  ```

  不要自己加沙箱旗標——repo 的 `.codex/config.toml` 已設 `danger-full-access`，加了 bubblewrap 會失敗、codex 零修改。
- 成果進 repo，不留 `/tmp`。

## 新增 workflow 的規則

1. 檔案的**第一個語句**是 `export const meta = {...}`，且 meta 是**純字面值**：不可以有變數、函式呼叫、展開運算子、模板字串插值。必填 `name`、`description`；選填 `whenToUse`、`phases`。
2. **純 JavaScript**，不是 TypeScript：沒有型別註記、`interface`、generics。
3. **禁止** `Date.now()`、`Math.random()`、無參數 `new Date()`——會讓 resume 壞掉。腳本裡沒有檔案系統與 Node API（要跑指令是叫子代理用 Bash）。
4. `meta.phases` 的每個 `title` 要和腳本裡 `phase()` 或 `opts.phase` 傳的字串**一字不差**。phase 標題用中文，註解也用繁體中文。
5. `args` 用解構取值並補預設；**缺必填欄位就 throw**，訊息講清楚缺什麼。
6. **檔尾放一份可以直接貼進 `args` 的 JSON 範例**，並同步更新這份 README 的表與範例。
7. 共用護欄要**組進 prompt**，不是只寫在註解裡。

驗語法用 `node --check`，但要先把檔複製成 `.mjs`（直接對 `.js` 跑會被當 CJS，遇到 `export` 就誤報）。

## 已歸檔

以下四個移到 [`../../doc/decisions/_legacy/workflows/`](../../doc/decisions/_legacy/workflows/)：

| 名字 | 為什麼不用了 |
|---|---|
| `diagram-review` | draw.io 圖面雙軌審查（Claude + codex）；架構圖已停在第十五版不再修改 |
| `diagram-review-claude` | 同上的單軌版（codex 不可用時）；同樣理由停用 |
| `diagram-review-v2` | 多頁流程圖的三階段審查（機械抽取＋lint 先跑）；同樣理由停用 |
| `decision-review` | 綁死 agy 前例研究的雙軌分析流程，那條流程已不用，先改由 `doc-review` 取代，`doc-review` 後來也已刪除，由 `doc-edit` 取代 |
