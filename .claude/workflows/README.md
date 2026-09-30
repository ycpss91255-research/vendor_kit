# 命名 workflow：任務執行一律走這裡

多步驟、會派子代理的任務不要臨時寫一次性腳本，改用這個目錄下的**命名 workflow**：腳本固定當模板，每次只換一份 `args`。

## 為什麼不是 JSON

「任務流程」看似可以寫成一份 JSON 或 YAML、每次只換內容。做不到，因為 Workflow 工具吃的是 JS 腳本，而腳本裡有兩種東西：

- **不可參數化的部分**：控制流本身。哪幾組並行、誰的輸出餵給誰、哪些條件才進下一階段、結果怎麼彙整成回傳值。這些是程式，寫成資料就得再發明一套迷你語言。`meta` 雖然必須是純字面值（不可以有變數、函式呼叫、展開、模板字串插值），但它只是註冊資訊，不是流程。
- **可參數化的部分**：`args`。要改哪些檔、每組子代理的任務描述、備份後綴、跑幾軌、effort 高低。這些每次都不一樣，而 `args` **就是 JSON**。

所以慣例是：**腳本寫一次進 git 當模板，之後每次任務只準備一份 args JSON**。要換的是 args，不是腳本。腳本要改的時機只有一個：流程形狀真的變了。

## 調用方式

```js
Workflow({ name: "doc-apply", args: { /* 這份 JSON 是每次唯一要換的東西 */ } })
```

- 腳本放這個目錄（`.claude/workflows/`），**檔名去掉 `.js` 就是 `name`**。
- 這些腳本已經進 git，跟 repo 一起版本控管；一次性腳本不進 repo。
- `args` 缺必填欄位時腳本會 throw，錯誤訊息會講清楚缺什麼。

## 現有 workflow

| 名字 | 用途 | 什麼時候跑 | args 必填 |
|---|---|---|---|
| `doc-apply` | 分組並行套用文件改動，然後驗證（含備份與禁止 git 寫入的護欄） | 一輪審查定案後要動多個檔時；單一檔的小改不用 | `round`、`tasks` |
| `doc-review` | Claude 與 codex 雙軌審查文件，交叉比對後只留一致的結論 | 對外契約、名詞表、不變量這類文件改完之後、定案之前 | `round`、`angles` |
| `doc-edit` | 改文件的固定流程：改寫 → lint 歸零 → codex 只讀審查 → 套用必改 → humanizer-zh-tw 潤稿；codex 的建議只回報 | 改任何現行文件（README、`docs/contract/`、`GLOSSARY.md`、ADR）時；主對話不自己改 | `round`、`files` |

選填欄位：

- `doc-apply`：`repo`（預設 `/home/cyc/Desktop/vendor-kit_ws/src`）、`background`、`verify`、`effort`（`{ apply, verify }`）。
- `doc-review`：`repo`（同上預設）、`background`、`tracks`、`cross_check`、`effort`（`{ review, cross }`）。
- `doc-edit`：`repo`（同上預設）、`ask`（不給就跳過「改寫」）、`background`、`codex_focus`（codex 額外要看的重點）、`effort`（`{ edit, polish, review }`）。

## doc-apply

N 組子代理並行改檔，再跑一組驗證。形狀是「改 + 查」，取代以前每輪手寫的 apply 腳本。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `round` | 是 | 字串，備份檔後綴。`r87` → `doc/decisions/_backup/<路徑攤平>.pre_r87.md` |
| `tasks` | 是 | 陣列，每項 `{ key, label, ask, files? }`。`ask` 是給子代理的任務描述；`files` 是這組只准動的檔 |
| `repo` | 否 | 預設 repo 根 |
| `background` | 否 | 共用背景：已定案的事實、改名史、不要重做的事 |
| `verify` | 否 | 陣列，每項 `{ key, label, ask }`。**不給**就用內建的預設三組（`links` 壞連結、`residue` 舊說法殘留、`gap` 宣稱 vs `git diff` 落差）；**給空陣列**＝跳過驗證 |
| `effort` | 否 | `{ apply, verify }`，值為 `low`｜`medium`｜`high`｜`xhigh`｜`max`。`verify` 預設 `low`，`apply` 不給則繼承 session |

回傳 `{ round, applied, verified, unresolved }`。`unresolved` 把「宣稱沒改成的」與「驗證沒過的」併成一份，主對話可以直接轉述。

args 範例：

```json
{
  "round": "r87",
  "background": "已定案的改名：專案→repo、動詞→recipe。這些 _Avoid_ 詞不得出現在現行檔正文（_Avoid_ 行本身除外）。名詞表是根 GLOSSARY.md，審閱頁是 docs/contract/01_purpose.md、docs/contract/02_invariants.md、docs/contract/03_messages.md、docs/contract/04_interface.md。",
  "tasks": [
    {
      "key": "purpose",
      "label": "01_purpose.md",
      "ask": "改 docs/contract/01_purpose.md：1. 全檔掃 _Avoid_ 詞，有殘留就改。2. 第 3 行指向名詞表的相對路徑改指根 GLOSSARY.md（驗證過可解再寫）。回報改了哪幾行與掃描結果。",
      "files": ["docs/contract/01_purpose.md"]
    },
    {
      "key": "adr",
      "label": "docs/adr/（README、TEMPLATE）",
      "ask": "改 docs/adr/README.md 與 TEMPLATE.md：把已改名的舊說法換成 recipe，並把兩檔的相對路徑連結驗證一次，壞的修掉。回報每檔改了哪幾行。",
      "files": ["docs/adr/README.md", "docs/adr/TEMPLATE.md"]
    }
  ],
  "verify": [
    {
      "key": "residue",
      "label": "驗證：_Avoid_ 詞殘留",
      "ask": "以根 GLOSSARY.md 的 _Avoid_ 行為準，grep 現行 md 的正文（_Avoid_ 行本身除外），列出每個殘留的位置與詞，並回報掃了幾個檔。"
    }
  ],
  "effort": { "verify": "low" }
}
```

## doc-review

Claude 軌（多面向並行）與 codex 軌**同時**跑同一批 angle，最後一個代理交叉比對：雙軌共同指出的進 `agreed`；單軌提出但查證成立的分別進 `claude_only`／`codex_only`。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `round` | 是 | 字串，用來命名 codex 的輸出檔 |
| `angles` | 是 | 陣列，每項 `{ key, label, ask }`，一個 angle 就是一個審查面向 |
| `repo` | 否 | 預設 repo 根 |
| `background` | 否 | 已定案的前提，prompt 裡會明寫「不要質疑」 |
| `tracks` | 否 | 預設 `["claude", "codex"]`。codex 不可用時給 `["claude"]` |
| `cross_check` | 否 | 預設 `true`。只跑一軌時沒有交叉比對 |
| `effort` | 否 | `{ review, cross }` |

codex 每個 angle 的原始輸出寫到 `doc/decisions/review_log/codex/<round>-<key>.md`（這是「不動 `review_log/`」的明示例外）。回傳 `{ round, tracks, claude, codex, cross }`；雙軌共同指出的進 `cross.agreed`；單軌提出但查證成立的分別進 `cross.claude_only`／`cross.codex_only`；`rejected` 附駁回理由。

args 範例：

```json
{
  "round": "r87",
  "background": "審閱頁有四頁：01_purpose.md（目的與承諾）、02_invariants.md（不變量）、03_messages.md（訊息與錯誤碼總表）、04_interface.md（使用者介面）；名詞全在根 GLOSSARY.md。",
  "angles": [
    {
      "key": "terms",
      "label": "GLOSSARY.md 名詞完整性",
      "ask": "審 GLOSSARY.md：定義是否一兩句、有沒有寫進規則或實作細節、目錄錨點是否都解得開（自己算 slug 比對）。"
    },
    {
      "key": "consistency",
      "label": "01 與 02 的一致性",
      "ask": "審 docs/contract/01_purpose.md 與 02_invariants.md：01 每條承諾在 02 是否有對應性質；兩頁有沒有用 GLOSSARY.md 沒定義的詞。"
    }
  ]
}
```

## 共用護欄

這幾條**寫在腳本裡**，會組進送給每個子代理的 prompt，不靠每次記得講：

- **不 commit、不 push、不跑任何 git 寫入指令**。唯讀的 `git status`／`git diff` 可以。
- **改前先備份**到 `doc/decisions/_backup/`，命名 `<路徑攤平>.pre_<round>.<ext>`（例如 `agents_domain.pre_r86.md`），同名已存在就加序號。
- **不准動** `doc/decisions/_backup/`、`doc/decisions/review_log/`、`doc/decisions/_marked/`：這些是歷史快照與本機產物，除非該 task 明說。
- **驗證一律用腳本／grep 算，不要目視**。
- codex 一律帶 `< /dev/null`：少了它，codex 會停在等 stdin，整條 workflow 卡死。固定的部分是 `codex exec --skip-git-repo-check -C <repo> -o <輸出檔>`、不加沙箱旗標、stdin 接 `/dev/null`。prompt 的傳法兩個 workflow 不同：

  - `doc-review`：brief 直接當引號參數傳。

    ```
    codex exec --skip-git-repo-check -C <repo> -o <輸出檔> "<brief>" < /dev/null
    ```

  - `doc-edit`：brief 先用 heredoc 寫進暫存檔，再用命令替換傳進去。

    ```
    codex exec --skip-git-repo-check -C <repo> -o <輸出檔> "$(cat <暫存檔>)" < /dev/null
    ```

  不要自己加沙箱旗標：repo 的 `.codex/config.toml` 已設 `danger-full-access`，加了 bubblewrap 會失敗、codex 零修改。
- 成果進 repo，不留 `/tmp`。

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
| `diagram-review` | draw.io 圖面雙軌審查（Claude + codex）；架構圖已停在第十五版不再修改 |
| `diagram-review-claude` | 同上的單軌版（codex 不可用時）；同樣理由停用 |
| `diagram-review-v2` | 多頁流程圖的三階段審查（機械抽取＋lint 先跑）；同樣理由停用 |
| `decision-review` | 綁死 agy 前例研究的雙軌分析流程，那條流程已不用，改由 `doc-review` 取代 |
