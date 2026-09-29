## 必改

- **位置：`doc/decisions/review/README.md:18`**
  - **問題：**「GitHub 與 GitLab 都會把 `<u>` 標籤刪掉」的出處只證明 GitHub 的行為。issue #60 沒有 GitLab 的測試或資料，無法支持後半句。
  - **建議：**刪掉「與 GitLab」，或另外補上能直接證明 GitLab 行為的出處。
  - **出處：**[issue #60](https://github.com/ycpss91255-research/vendor_kit/issues/60) 的內容只記錄 GitHub Markdown API 實測。

- **位置：`doc/decisions/review/README.md:19`**
  - **問題：**「其他頁要用到，標條號引用」說得過窄。現有 03 頁不只引用 02 的條號，也引用 01 的章節名稱及 ADR 的節號；例如 03 第 13 行引用 01「VK 做的事」，第 58–59 行引用 ADR §2、§6。不是所有來源都有可標的「條號」。
  - **建議：**改成「標明來源的條號或章節，不重述」，或明確限定「引用不變量時標條號」。
  - **出處：**`doc/decisions/review/03_interface.md:13,58-59`；`AGENTS.md:17-18` 也把不變量與 ADR 分成「性質」和「機制與理由」兩種來源。

- **位置：`doc/decisions/review/README.md:26`**
  - **問題：**「會自動備份」「由 doc-edit workflow 負責」高估了實作保證。workflow 本身沒有執行複製或檢查備份是否真的建立；它只是把備份規則寫進各子代理的 prompt，回傳 schema 雖要求 `backups` 欄位，卻未驗證陣列非空或檔案存在。
  - **建議：**如實寫成「doc-edit workflow 會要求執行者在改檔前備份」；若要保留「自動備份」，workflow 必須自行建立並驗證備份。
  - **出處：**`.claude/workflows/doc-edit.js:46-54,58-67,69-105,168-209`；`script/README.md:9-18` 把備份列為人工／子代理執行的獨立步驟。

- **位置：`doc/decisions/review/README.md:28`**
  - **問題：**「紅底是被取代的舊文字」不完整。產生器會把所有不再出現在新版的非空舊行標紅，包括單純刪除、沒有替代文字的行。
  - **建議：**改成「紅底是刪除或被取代的舊文字」。
  - **出處：**`script/mark_changes.py:93-106` 對所有 `old[i1:i2]` 非空行套用紅底；不限定 diff opcode 必須是 replace。

## 建議

- **位置：`doc/decisions/review/README.md:17`**
  - **問題：**「每頁只用前面頁與名詞表的名詞」容易被第一次閱讀的人理解為所有用詞都必須收錄於 `CONTEXT.md`。但 `CONTEXT.md` 明說只收 VK 專有名詞，不收一般技術詞。
  - **建議：**改成「每頁使用的 VK 專有名詞，只能來自前面頁或名詞表」，並說清楚這項順序規則適用於 01–03 契約頁，不包含本 README。
  - **出處：**`CONTEXT.md:3`；README 本身也使用 `agent`、workflow、lint、codex 等未收錄的一般流程詞。

- **位置：`doc/decisions/review/README.md:27`**
  - **問題：**流程箭頭看似每次都完整執行，但實作中「改寫」可省略、「套用必改」在沒有必改時會省略；Codex 審查失敗時仍會繼續潤稿。
  - **建議：**標出條件，例如「改寫（可略）→ lint → Codex 審查 → 套用必改（如有）→ 潤稿」。另應決定是否真的允許審查失敗後繼續潤稿；目前 README 沒有讓讀者知道這個分支。
  - **出處：**`.claude/workflows/doc-edit.js:69-71,168-171,193-218`。

- **位置：`doc/decisions/review/README.md:27`**
  - **問題：**連結直接指向 JavaScript 實作，沒有說明如何啟動 workflow；第一次來的人只能讀程式猜使用方式。
  - **建議：**補一句最短的啟動方式或連到操作說明；不必在 README 展開 workflow 內部細節。
  - **出處：**`.claude/workflows/doc-edit.js:14-30` 只在原始碼註解中說明參數，README 沒有入口說明。

- **位置：`doc/decisions/review/README.md:28`**
  - **問題：**`<頁>` 容易被理解為檔名，實際參數只能傳不含 `.md` 的頁名；命令也依賴從 repo 根目錄執行。傳入 `03_interface.md` 會組成 `03_interface.md.md`。
  - **建議：**改成 `python3 script/mark_changes.py <舊版後綴> <不含 .md 的頁名>`，並註明從 repo 根目錄執行，或直接給一個實例。
  - **出處：**`script/mark_changes.py:23-25,71-90,120-126`；`script/README.md:20-26`。

- **位置：`doc/decisions/review/README.md:26-28`**
  - **問題：**備份路徑中的 `<頁>` 與命令參數中的 `<頁>` 表面相同，實際格式不同：備份使用完整路徑攤平後的名稱，命令使用單純頁名。
  - **建議：**分別命名為 `<攤平路徑>` 與 `<頁名>`，避免使用者把其中一種格式套到另一處。
  - **出處：**`.claude/workflows/doc-edit.js:51`；`script/mark_changes.py:77-78,89-90`；`script/README.md:16,23-26`。

連結檢查沒有其他問題：10 個 Markdown 連結都有名稱；9 個 repo 內目標全部存在，issue #60 也存在。`_marked/`、`_backup/` 確實受 `.gitignore:4,8` 忽略。README 未使用 `CONTEXT.md` 的任何 `_Avoid_` 詞，也沒有直接引用 ADR，因此沒有 ADR 編號或章節引用可核對。