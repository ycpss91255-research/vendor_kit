# 命名 workflow — 任務執行一律走這裡

多步驟、會派子代理的任務不要臨時寫一次性腳本，改用這個目錄下的**命名 workflow**：腳本固定當模板，每次只換一份 `args`。

## 為什麼不是 JSON

看起來「任務流程」應該可以寫成一份 JSON 或 YAML，然後每次換內容就好。做不到，因為 Workflow 工具吃的是 JS 腳本，而腳本裡有兩種東西：

- **不可參數化的部分**：控制流本身。哪幾組並行、誰的輸出餵給誰、哪些條件才進下一階段、結果怎麼彙整成回傳值——這是程式，寫成資料就得再發明一套迷你語言。`meta` 雖然必須是純字面值（不可以有變數、函式呼叫、展開、模板字串插值），但它只是註冊資訊，不是流程。
- **可參數化的部分**：`args`。要改哪些檔、每組子代理的任務描述、備份後綴、跑幾軌、effort 高低——這些每次都不一樣，而 `args` **就是 JSON**。

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
| `doc-edit` | 改文件的固定流程（每個檔並行）：改寫 → lint 歸零 → 只讀審查（含核對已定案）→ 套用必改 → 跨檔一致性 → `humanizer-zh-tw` 潤稿 → lint；預設 codex 改、Claude 查，可用 `editor` 切換；`mode: light` 只跑 Claude 改寫、lint、Claude 審查與套用必改；建議只回報 | 改任何現行文件（README、`doc/contract/`、`GLOSSARY.md`、ADR） | `round`、`files` |

兩個都有選填的 `repo`（預設 `/home/cyc/Desktop/vendor-kit_ws/src`）、`background`（共用背景／已定案前提）與 `effort`。

## doc-edit

改文件一律走這個流程，順序固定。分工用 `editor` 切換：預設 `codex`，由 codex 改寫、套用必改、修跨檔不一致，Claude 只讀審查與做跨檔檢查；`editor` 給 `claude` 就對調，Claude 改、codex 只讀審查（跨檔一致性由一個 Claude 子代理檢查並修）。審查方永遠是改稿方的另一方。codex 一律由包裝子代理啟動，改完由包裝子代理用指令驗證備份在、沒有動到範圍外的檔。

1. **改寫**：先查 `round` 是不是 `_backup` 最大編號加一，不對就停。每個檔一條並行，改稿方照 `ask` 改；沒給 `ask` 就跳過（檔已經改好，只跑後面幾段）。
2. **lint**：一個 Claude 子代理跑 `check_terms`、`check_context`、`check_review_pages`、`check_messages`（`doc/contract/03_messages.csv` 還不存在時它自己跳過），只修 lint 指出的地方，直到全部通過。
3. **審查**：每個檔一條並行，審查方只讀。最重要的一項是先讀 wayfinder map issue 的已定案決定（`gh issue view 78 -R ycpss91255-research/vendor_kit` 本文的「Decisions so far」，每條連到 child issue；細節用 `gh issue view <child> -R ycpss91255-research/vendor_kit --comments` 看留言），逐條核對這一輪的改動有沒有違反定案、改變 01 的承諾、削弱 02 的不變量、或改動 03／04 的對外介面而 `ask` 沒要求；有就列必改，改法是還原。其餘對照 01、02、`GLOSSARY.md`、ADR 查正確性、連結、名詞、易讀性，對外頁另查 CLI 慣例；分必改與建議。
4. **套用必改**：審完的檔立刻由改稿方套用，不問維護者；先對照證據確認審查沒看錯，跟定案衝突（註明「未改：跟定案 #<child> 衝突」）、改到對外承諾、屬於別的檔的不改，逐條寫已改或未改的理由。建議不改，只回報。
5. **跨檔一致性**：全部套用完後比對各檔之間的結束碼、編號、名詞、連結；有要修的交給改稿方，最後 lint 要全部通過。
6. **潤稿**：每個檔一個 Claude 子代理用 `humanizer-zh-tw` 潤稿，只准改這一輪改過的行（對這一輪備份的 diff 裡新增或修改的行），只修 `humanizer-zh-tw` 列的 AI 寫作模式，沒有明確問題就不改；不改意思、不動程式碼與連結。改完用腳本比對潤稿前後，落在這一輪範圍外的變動還原；這一輪沒改的檔跳過。最後再跑一次 lint。

上面是 `mode: full`（預設）。`mode: light` 給機械式改動（換詞、改連結、改編號）、只改幾行、對齊已定案內容的補句；對外頁的新內容或重寫用 `full`。light 不管 `editor`，全程只用 Claude 子代理、不叫 codex：

1. **改寫**：輪次檢查照舊；每個檔一個 Claude 子代理並行改，護欄與備份規則同上，機械式改動用腳本做、改完用腳本驗證。
2. **lint**：同上。
3. **審查**：每個檔另一個 Claude 子代理只讀審查，只看這一輪的 diff（`_backup/<鍵>.pre_<round>.md` 對現行檔；`.csv` 檔是 `.pre_<round>.csv`），只查有沒有違反 map #78 的已定案決定、有沒有改到 01 承諾／削弱 02／動到 03、04 介面而 `ask` 沒要求、`ask` 做完沒、連結與錨點存不存在；結果寫到 `review_log/claude/<round>-doc-edit-<鍵>.md`。
4. **套用必改**：有必改才由 Claude 子代理照同樣的規則修，修完跑 lint；指到別的檔的必改只回報。
5. 不跑跨檔一致性與潤稿，最後再跑一次 lint。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `round` | 是 | 備份檔後綴與審查輸出檔名，例如 `r90`；必須是 `_backup` 最大編號加一 |
| `files` | 是 | 這次只准動的檔，相對 repo 根目錄 |
| `ask` | 否 | 要怎麼改；不給就跳過改寫 |
| `background` | 否 | 已定案的前提 |
| `codex_focus` | 否 | 審查額外要看的重點（不論審查方是誰） |
| `editor` | 否 | `codex`（預設）或 `claude`：誰改；審查方是另一方；其他值直接停 |
| `mode` | 否 | `full`（預設）或 `light`：light 只給機械式或只改幾行的改動，全程 Claude、不跑跨檔一致性與潤稿；其他值直接停 |
| `effort` | 否 | `{ edit, polish, review }`；`edit`／`review` 只作用在 Claude 子代理，codex 那一方作用在包裝子代理；light 時 `edit`（含套用必改）與 `review` 預設 `low` |

輸出檔依產生者放 `doc/decisions/review_log/codex/` 或 `doc/decisions/review_log/claude/`：審查是 `<round>-doc-edit-<鍵>.md`；codex 改稿時另有 `<round>-doc-edit-edit-<鍵>.md`、`<round>-doc-edit-apply-<鍵>.md`、`<round>-doc-edit-consistency.md`。回傳 `{ round, mode, edited, linted, review, applied, consistency, polished, finalLint }`；light 的 `consistency` 與 `polished` 是 `null`。args 範例在腳本檔尾。

## doc-apply

N 組子代理並行改檔，再跑一組驗證。形狀是「改 + 查」，取代以前每輪手寫的 apply 腳本。

args 欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| `round` | 是 | 字串，備份檔後綴。`r87` → `doc/decisions/_backup/<路徑攤平>.pre_r87.md`（`.csv` 檔是 `.pre_r87.csv`） |
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
  "background": "已定案的改名：專案→repo、動詞→recipe。這些 _Avoid_ 詞不得出現在現行檔正文（_Avoid_ 行本身除外）。名詞表是根 CONTEXT.md，審閱頁只剩 review/01_purpose.md 與 review/02_invariants.md。",
  "tasks": [
    {
      "key": "purpose",
      "label": "01_purpose.md",
      "ask": "改 doc/decisions/review/01_purpose.md：1. 全檔掃 _Avoid_ 詞，有殘留就改。2. 第 3 行指向名詞表的相對路徑改指根 CONTEXT.md（驗證過可解再寫）。回報改了哪幾行與掃描結果。",
      "files": ["doc/decisions/review/01_purpose.md"]
    },
    {
      "key": "adr",
      "label": "doc/adr/（README、TEMPLATE）",
      "ask": "改 doc/adr/README.md 與 TEMPLATE.md：把已改名的舊說法換成 recipe，並把兩檔的相對路徑連結驗證一次，壞的修掉。回報每檔改了哪幾行。",
      "files": ["doc/adr/README.md", "doc/adr/TEMPLATE.md"]
    }
  ],
  "verify": [
    {
      "key": "residue",
      "label": "驗證：_Avoid_ 詞殘留",
      "ask": "以根 CONTEXT.md 的 _Avoid_ 行為準，grep 現行 md 的正文（_Avoid_ 行本身除外），列出每個殘留的位置與詞，並回報掃了幾個檔。"
    }
  ],
  "effort": { "verify": "low" }
}
```

## doc-review

Claude 軌（多面向並行）與 codex 軌**同時**跑同一批 angle，最後一個代理交叉比對，只有兩邊都指出的才算結論。

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

codex 每個 angle 的原始輸出寫到 `doc/decisions/review_log/codex/<round>-<key>.md`（這是「不動 `review_log/`」的明示例外）。回傳 `{ round, tracks, claude, codex, cross }`；`cross.agreed` 才是結論，`claude_only`／`codex_only` 是單軌提出但查證成立的，`rejected` 附駁回理由。

args 範例：

```json
{
  "round": "r87",
  "background": "審閱頁只有兩頁：01_purpose.md（目的與承諾）、02_invariants.md（不變量）；名詞全在根 CONTEXT.md。",
  "angles": [
    {
      "key": "terms",
      "label": "CONTEXT.md 名詞完整性",
      "ask": "審 CONTEXT.md：定義是否一兩句、有沒有寫進規則或實作細節、目錄錨點是否都解得開（自己算 slug 比對）。"
    },
    {
      "key": "consistency",
      "label": "01 與 02 的一致性",
      "ask": "審 doc/decisions/review/01_purpose.md 與 02_invariants.md：01 每條承諾在 02 是否有對應性質；兩頁有沒有用 CONTEXT.md 沒定義的詞。"
    }
  ]
}
```

## 共用護欄

這幾條**寫在腳本裡**，會組進送給每個子代理的 prompt，不靠每次記得講：

- **不 commit、不 push、不跑任何 git 寫入指令**。唯讀的 `git status`／`git diff` 可以。
- **改前先備份**到 `doc/decisions/_backup/`，命名 `<路徑攤平>.pre_<round>.<ext>`（例如 `agents_domain.pre_r86.md`），同名已存在就加序號。路徑攤平時去掉 `.md` 或 `.csv`；`<ext>` 對 `.csv` 檔是 `csv`（`doc/contract/03_messages.csv` → `doc_contract_03_messages.pre_<round>.csv`），其他檔一律 `md`。
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
| `decision-review` | 綁死 agy 前例研究的雙軌分析流程，那條流程已不用，改由 `doc-review` 取代 |
