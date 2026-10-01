# 命名 workflow：任務執行一律走這裡

多步驟、會派子代理的任務不要臨時寫一次性腳本，改用這個目錄下的**命名 workflow**：腳本固定當模板，每次只換一份 `args`。

## 為什麼不是 JSON

「任務流程」看似可以寫成一份 JSON 或 YAML、每次只換內容。做不到，因為 Workflow 工具吃的是 JS 腳本，而腳本裡有兩種東西：

- **不可參數化的部分**：控制流本身。哪幾組並行、誰的輸出餵給誰、哪些條件才進下一階段、結果怎麼彙整成回傳值。這些是程式，寫成資料就得再發明一套迷你語言。`meta` 雖然必須是純字面值（不可以有變數、函式呼叫、展開、模板字串插值），但它只是註冊資訊，不是流程。
- **可參數化的部分**：`args`。要改哪些檔、每組子代理的任務描述、備份後綴、跑幾軌、effort 高低。這些每次都不一樣，而 `args` **就是 JSON**。

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
| `research` | 外部資料調查：agy 依 brief 查資料 → codex 逐條核對來源 → Claude 整合審查 → 結果貼到指定 issue。brief 放 workspace 的 `reference/research/<issue>/<id>_brief.md`，輸出也放那裡，不放 `/tmp` | 要找外部前例或資料當決策依據時；brief 先寫好 | `issue`、`topic`、`briefs`（每項 `{ id, label }`） |

選填欄位：

- `doc-edit`：`repo`（預設 `/home/cyc/Desktop/vendor-kit_ws/src`）、`ask`（不給就跳過「改寫」）、`background`、`codex_focus`（審查額外要看的重點）、`editor`（`codex` 預設｜`claude`）、`mode`（`full` 預設｜`light`）、`effort`（`{ edit, polish, review }`）。
- `research`：`dir`（預設 `/home/cyc/Desktop/vendor-kit_ws/reference/research/<issue>`）、`background`（已定案前提）、`post`（預設 `true`；`false` 就只產檔、不貼 issue）。

`round` 是 `rNN`，取兩者的最大值加一：本機 `doc/decisions/_backup/` 裡最大的 `pre_rNN`，與 git log 裡 `Doc-Edit: rNN` footer 的最大值。`_backup/` 不進 git，只看它會在別台機器或清過本機後重用舊編號。

## 共用護欄

這幾條**寫在腳本裡**，會組進送給每個子代理的 prompt，不靠每次記得講：

- **不 commit、不 push、不跑任何 git 寫入指令**。唯讀的 `git status`／`git diff` 可以。
- **改前先備份**到本機的 `doc/decisions/_backup/`（已 gitignore，不進 git），命名 `<鍵>.pre_<round><副檔名>`（例如 `claude_workflows_README.pre_r146.md`；鍵與副檔名的規則跟 `script/doc/mark_changes.py` 同一套），同名已存在就在副檔名前加序號。
- **不准動** `doc/decisions/_backup/`、`doc/decisions/review_log/`（本機產物，已 gitignore）與送審資料夾 `doc/review/`（由 `script/doc/mark_changes.py`、`script/doc/pack_review.py` 產生），除非該 task 明說。審查結論寫進 issue 留言，不留在 repo。
- **驗證一律用腳本／grep 算，不要目視**。
- codex 一律帶 `< /dev/null`：少了它，codex 會停在等 stdin，整條 workflow 卡死。形狀固定：`codex exec --skip-git-repo-check -C <repo> -o <輸出檔>`、不加沙箱旗標、stdin 接 `/dev/null`；brief 先用 heredoc 寫進暫存檔，再用命令替換傳進去：

  ```
  codex exec --skip-git-repo-check -C <repo> -o <輸出檔> "$(cat <暫存檔>)" < /dev/null
  ```

  不要自己加沙箱旗標：repo 的 `.codex/config.toml` 已設 `danger-full-access`，加了 bubblewrap 會失敗、codex 零修改。
- 暫存檔放 scratchpad，不留 `/tmp`。

## 新增 workflow 的規則

1. 檔案的**第一個語句**是 `export const meta = {...}`，且 meta 是**純字面值**：不可以有變數、函式呼叫、展開運算子、模板字串插值。必填 `name`、`description`；選填 `whenToUse`、`phases`。
2. **純 JavaScript**，不是 TypeScript：沒有型別註記、`interface`、generics。
3. **禁止** `Date.now()`、`Math.random()`、無參數 `new Date()`，這些會讓 resume 壞掉。腳本裡沒有檔案系統與 Node API（要跑指令是叫子代理用 Bash）。
4. `meta.phases` 的每個 `title` 要和腳本裡 `phase()` 或 `opts.phase` 傳的字串**一字不差**。phase 標題用中文，註解也用繁體中文。
5. `args` 用解構取值並補預設；**缺必填欄位就 throw**，訊息講清楚缺什麼。
6. **檔尾放一份可以直接貼進 `args` 的 JSON 範例**，並同步更新這份 README 的表與範例。這條沒有腳本檢查，改檔的人要自己對。
7. 共用護欄要**組進 prompt**，不是只寫在註解裡。

驗語法用 `node --check`，但要先把檔複製成 `.mjs`（直接對 `.js` 跑會被當 CJS，遇到 `export` 就誤報）。

## 已歸檔

以下四個已歸檔，跟著原本的 `_legacy` 目錄搬出 repo，只留在維護者本機的 `../reference/_legacy`（`workflows` 子目錄，路徑相對 repo 根目錄），不進 git：

| 名字 | 為什麼不用了 |
|---|---|
| `diagram-review` | draw.io 圖面雙軌審查（Claude + codex）；舊模型的圖已移出 repo，歸檔到 workspace 的 `reference/diagram_legacy/`，之後重畫時另訂流程 |
| `diagram-review-claude` | 同上的單軌版（codex 不可用時）；同樣理由停用 |
| `diagram-review-v2` | 多頁流程圖的三階段審查（機械抽取＋lint 先跑）；同樣理由停用 |
| `decision-review` | 綁死 agy 前例研究的雙軌分析流程，那條流程已不用，先改由 `doc-review` 取代，`doc-review` 後來也已刪除，由 `doc-edit` 取代 |
