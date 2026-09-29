## 必改

1. **位置：`AGENTS.md:17`**
   - **問題：**「必要段落由 lint 管」不是現況。`doc/adr/README.md:11、26` 都明寫 lint「待寫」；現有 `.github/workflows/docs.yml` 也只跑 `check_terms.py`、`check_context.py`。
   - **建議：**改成「必要段落規則見 ADR 規則；lint 待寫」，或實作完成後再寫成已由 lint 強制。
   - **出處：**`doc/adr/README.md`「檔案系統即登錄」「必要段落規則」；`.github/workflows/docs.yml:13-21`。

2. **位置：`AGENTS.md:17`**
   - **問題：**「檔案系統即登錄，不另立索引」和實際文件衝突。`doc/adr/README.md` 標題就是「ADR 索引」，且 `:37-52` 有人工彙整的索引表。
   - **建議：**精確寫成「檔案系統是正式登錄；`doc/adr/README.md` 的表只是彙整檢視，不是另一份登錄」。
   - **出處：**`doc/adr/README.md:1-10、37-52`。

3. **位置：`AGENTS.md:20`**
   - **問題：**把架構圖的 import-linter、鏡射、黑箱 lint 寫成已經強制，但目前沒有這些檢查。`doc/decisions/README.md:57` 直接承認「那個 lint 還沒寫」；現有 docs CI 也沒有相關步驟。
   - **建議：**若這是未來規則，明寫「預定由 lint 強制，目前尚未實作」；不要使用現在式「由 lint 強制」。
   - **出處：**`doc/decisions/README.md:53-59`；`.github/workflows/docs.yml:13-21`。

4. **位置：`doc/decisions/README.md:67`**
   - **問題：**把 `diagram-review-v2` 稱為 skill，並說保留三支腳本才不會把它弄壞；實際上它是已歸檔的 workflow，目前 `.claude/workflows/` 只有 `doc-apply`、`doc-edit`、`doc-review`。
   - **建議：**改成歷史敘述，例如「已歸檔的 `diagram-review-v2` workflow 當時會跑前三支」；不要再把保留腳本描述成現行依賴。
   - **出處：**`.claude/workflows/README.md:162-170`；實際 `.claude/workflows/` 內容。

5. **位置：`.claude/workflows/README.md:88、102`**
   - **問題：**「只有兩邊都指出的才算結論」「`cross.agreed` 才是結論」不符合實作。`doc-review.js` 明確保留經交叉代理查證成立的 `claude_only`、`codex_only`；README 下一句自己也承認這兩類「查證成立」。
   - **建議：**改成「雙軌共同指出的進 `agreed`；單軌提出但查證成立的分別進 `claude_only`／`codex_only`」。
   - **出處：**`.claude/workflows/doc-review.js:162-197、218-223`。

6. **位置：`.claude/workflows/README.md:157`**
   - **問題：**規則要求 workflow 檔尾 JSON 範例與 README 同步，但 `doc-review.js:243` 仍寫「審閱頁只有兩頁」，README 範例已改成三頁。文件宣稱的同步規則目前沒有成立。
   - **建議：**同步更新 `doc-review.js` 檔尾範例；若這條規則不會被檢查，至少不要把同步狀態當成既成事實。
   - **出處：**`.claude/workflows/README.md:106-122、150-160`；`.claude/workflows/doc-review.js:240-254`。

7. **位置：`script/README.md:34`**
   - **問題：**前文已限定只有對外文件產標示版，這裡又寫「所有檔的標示版都輸出到……」，字面上重新擴大成內部文件也會產生，和新規則不一致。
   - **建議：**改成「所有對外文件的標示版」或「上述審閱頁與根 README 的標示版」。
   - **出處：**`AGENTS.md:16`；`doc/decisions/review/README.md:31-35`；`script/README.md:5`。

8. **位置：`doc/decisions/review/README.md:26-27、33`**
   - **問題：**流程層級不清楚。步驟 1 像是要求人工先備份，步驟 2 又執行本身已強制「改前先備份」的 `doc-edit`；照字面執行會做兩次備份。內部文件又被說成「走步驟 1、2」，同樣有此問題。
   - **建議：**明確寫成「執行 `doc-edit`；workflow 在第一次修改前自行備份」，或說明步驟 1 是 workflow 內部階段，不是另一個人工步驟。
   - **出處：**`.claude/workflows/doc-edit.js:46-56、69-101`。

## 建議

1. **位置：五份文件的 Markdown 連結**
   - **問題：**實際 Markdown 連結都有可讀名稱，所有本機目標也存在；未發現空文字連結、以裸路徑作連結文字或壞路徑。不過多處以「見 `路徑`」表達導覽，實際只是 code span，不能點擊。
   - **建議：**至少把明確的「見某文件」改成具名超連結；純粹展示檔名或命令參數的 code span 可保留。
   - **出處：**例如 `AGENTS.md:4、7、10、17`，`doc/decisions/README.md:3、73`。具名連結規則見 `doc/decisions/review/README.md:20`。

2. **位置：`doc/decisions/README.md:3`**
   - **問題：**一句同時說 skill 結構、四種文件、issue 流程、目錄例外及本檔用途，第一次閱讀很難辨認主句。
   - **建議：**拆成三句：skill 預設結構、此 repo 的刻意偏離、這份 README 的用途。
   - **出處：**易讀性審查；不影響 01、02 或 ADR 的事實。

3. **位置：`doc/decisions/README.md:37、44、63、99`**
   - **問題：**`103 MB`、`152 檔 59 MB`、`19 MB／216 個 .py`、單檔數量等工作區統計目前大致成立，但會隨歸檔或新增檔案快速過時，也不是理解分類所必需。
   - **建議：**若沒有自動檢查，刪除精確容量與檔數，或加「截至 YYYY-MM-DD」。
   - **出處：**目前 `du` 顯示 `_legacy/` 103 MB、`script/diagram/` 19 MB，且共有 216 個 `.py`；數字正確但脆弱。

4. **位置：`doc/decisions/README.md:79-81`**
   - **問題：**先說相關 ADR 已全部落地，再說兩份文件仍等「併進相關 ADR」，第一次閱讀容易誤解成 ADR 已經吸收內容。
   - **建議：**區分「ADR 檔已建立」與「設計原則／範圍內容尚未併入 ADR」。
   - **出處：**實際 ADR-0001～0012 均存在；`doc/adr/README.md:3、19` 仍允許 `Serves` 指向這兩份文件。

5. **位置：`doc/decisions/README.md:101-107`**
   - **問題：**「proto 的 ADR-0001、0002」和本 repo 現有 ADR-0001、0002 同號，段落雖有解釋，標題仍容易讓第一次閱讀者以為現行 ADR 已完成某項工作。
   - **建議：**標題直接寫「舊 proto 的兩份同號 ADR」。
   - **出處：**現行 `doc/adr/0001-*`、`0002-*` 與本段描述的是不同文件。

6. **位置：`.claude/workflows/README.md:30、36`**
   - **問題：**新規則要求任何內部文件也走 `doc-edit`，但這裡的適用範圍只列 README、審閱頁、CONTEXT、ADR，容易被讀成封閉清單，沒有明確涵蓋 `AGENTS.md`、workflow 說明及工具說明。
   - **建議：**直接寫「改任何現行文件，包括內部文件」；括號改成例子。
   - **出處：**`AGENTS.md:16`；`doc/decisions/review/README.md:33`。

7. **位置：`script/README.md:3`**
   - **問題：**標題仍叫「審閱頁的改動標示」，內容已擴大到根目錄 README。
   - **建議：**改成「對外文件的改動標示」。
   - **出處：**`script/README.md:5`；`AGENTS.md:16`。

8. **位置：`script/README.md:32`**
   - **問題：**「新建的頁」沒有交代新建對外文件是否在允許範圍；依已定案範圍，對外文件集合固定是根 README 與 01～03，讀者可能誤認任何新頁都能直接套此流程。
   - **建議：**若只是說明工具能力，改成「工具處理沒有基準版的檔時可用 `new`；是否屬對外文件仍依工作約定」。
   - **出處：**`AGENTS.md:16`；`doc/decisions/review/README.md:31-33`。

9. **位置：名詞檢查整體**
   - **問題：**未發現五份文件正文使用未處理的 `_Avoid_` 詞；`check_terms.py` 與 `check_context.py` 都通過。`workflow`、`skill`、`agent`、`ruleset` 等沒有收進 `CONTEXT.md`，但它們是作者流程的一般技術詞，不是 VK 對外領域名詞，不必為此擴充名詞表。
   - **建議：**不改名詞表；只修正 `diagram-review-v2` 被誤稱為 skill 的事實錯誤。
   - **出處：**`CONTEXT.md` 開頭明定「一般技術詞不收」；兩支自檢皆回傳 `OK`。

10. **位置：三處新規則整體**
    - **問題：**`AGENTS.md:16`、`doc/decisions/review/README.md:31-35`、`script/README.md:5` 對「只有根 README 與 01～03 產標示版；內部文件不產、不送審」的核心範圍一致。主要偏差是 `script/README.md:34` 的「所有檔」，以及 `doc-edit` 適用範圍寫得不夠明確。
    - **建議：**以 `AGENTS.md:16` 的集合式寫法作為三處共同句型，其他地方只連結或簡述，避免範圍再次漂移。
    - **出處：**上述三份文件對應段落。