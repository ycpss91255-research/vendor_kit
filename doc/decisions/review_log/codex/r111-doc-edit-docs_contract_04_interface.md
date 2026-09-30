## 必改

1. **位置：`docs/contract/04_interface.md:220-228`，「使用者的檔與 VK 的檔」**
   - **問題：** 「只有這四種明定例外」漏掉一般 copy 型初始檔在目標不存在時的新建。照現文，VK 第一次導入普通初始檔反而沒有合法寫入路徑，與既定承諾不一致。
   - **建議：** 把範圍改成「動到既有使用者檔」；或補列「目標不存在時建立 copy 型初始檔」。前者較精確，因為新建不屬於修改既有內容。
   - **證據：** `docs/contract/01_purpose.md:28` 明定初始檔第一次會複製；`docs/contract/02_invariants.md:23-28` 明定「可以建」；`docs/contract/04_interface.md:248` 也只交代 `add` 遇到「已存在」檔時的處理，未涵蓋不存在時。

2. **位置：`docs/contract/04_interface.md:143-146`，「說明與用法錯誤」**
   - **問題：** 本段宣稱採 GNU 式選項，但 `-p` 是唯一沒有長選項的短選項，也沒有交代偏離理由。GNU Coding Standards 明確要求單字母選項應有等價長選項。這不涉及已定案的頂層 `-h`／`--version` 限制。
   - **建議：** 若 `-p` 尚未形成相容性承諾，改成單一寫法 `--path <dir>`；若必須保留 `-p`，補上 `--path`，或明文說明為何刻意偏離 GNU 慣例。考量不變量 8 的「一個概念一種寫法」，較建議只保留 `--path`。
   - **證據：** `docs/contract/04_interface.md:86,141,145`；`docs/contract/02_invariants.md:156-162`。[GNU Command-Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)要求為 Unix 式單字母選項提供等價長選項。

3. **位置：`docs/contract/04_interface.md:5`，以及 `:167-169`、`:179-184`、`:211-249`、`:269-271`**
   - **問題：** 第 5 行宣稱本頁對永久規則「只寫依第 N 條，不重述」，後面卻大量重述不變量，有些還改成更窄或更具體的版本。例如 `sync`／`prune` 不改進 git 的檔、`-y` 不授權覆蓋、CI 不寫進 git 的檔、收回內容的歸因規則。這讓同一條契約出現兩份正文；第一項遺漏 copy 型初始檔正是已經發生的漂移。
   - **建議：** 刪掉第 5 行的絕對宣告，改成「永久性質以 02 為準，本頁只補可觀察的介面行為」；或刪除後文所有純重述，只保留指令寫法、必要參數及使用者可觀察結果。不要保留目前互相矛盾的說法。
   - **證據：** `docs/contract/02_invariants.md:23-49,76-82`；`docs/contract/04_interface.md:5,167-169,179-184,211-249,269-271`；`AGENTS.md:26` 規定不變量頁負責記錄「必須永遠成立」的性質。

4. **位置：`docs/contract/04_interface.md:196-201`，「各指令專用選項」**
   - **問題：** 工具離線導入明定缺 digest 以 `2` 結束，但引擎離線導入只列 `bootstrap.sh -i <image>`，沒有交代相同的 digest 要求。這使 04 看起來允許引擎 tar 在沒有正式 digest 時繼續，與「離線與線上寫出相同版本鎖定行」的承諾不完整。
   - **建議：** 在兩種離線入口的共同段落明定：image tar 必須附正式 digest 資訊；缺少時以 `2` 結束，不退化成 tag 或平台 tar 雜湊。若已載入 image 的 digest 取得條件不同，也要分開寫清楚。
   - **證據：** `docs/contract/01_purpose.md:70-71`；`docs/contract/02_invariants.md:59-66,74`；`docs/adr/0009-release-assets-and-offline-import.md:3,18-20`；`docs/contract/04_interface.md:196-201`。

## 建議

1. **位置：`docs/contract/04_interface.md:143-149`，「說明與用法錯誤」**
   - **問題：** 一個項目同時解釋 GNU、POSIX Guideline 7、Guideline 9、長短選項、`--` 和 `--engine` 的特殊解析，第一次閱讀很難分辨哪些是通則、哪些是例外。
   - **建議：** 拆成「一般解析規則」與「刻意例外」兩段；把 `--engine` 的完整規則只留在例外段，不要在第 142、146、149 行分三次交代。
   - **證據：** `docs/contract/04_interface.md:142-149`。POSIX 原文分別規定 option-argument 不應可省略、選項應先於 operands、`--` 結束選項解析；目前條號引用本身正確。[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)

2. **位置：`docs/contract/04_interface.md:163`，「成對與無害」**
   - **問題：** 「做得了就反得回」容易被理解成完整復原，但 `remove`／`uninstall` 明定不刪初始檔，只收回可可靠歸因的插入行，因此並非一般意義上的反操作。
   - **建議：** 改成「每個建立關係的指令都有解除關係的指令；解除不保證還原檔案內容」，避免讀者預期 uninstall 後回到安裝前狀態。
   - **證據：** `docs/contract/04_interface.md:90,98,163,235-249`；`docs/contract/02_invariants.md:36-42`。

3. **位置：`docs/contract/04_interface.md:216-218`，「使用者的檔與 VK 的檔」**
   - **問題：** 三個不同判準塞在兩個長句中：檔案所有權、哪些內容受合併保護、使用者手改是否改變所有權。第一次閱讀很難判斷 `.vendor_kit/config.toml`、版本鎖定行和薄殼各由誰維護。
   - **建議：** 改成小表格，欄位至少包含「檔／內容、誰維護、VK 能否重寫、使用者能否手改、改前是否詢問」。
   - **證據：** `docs/contract/04_interface.md:216-218`；`docs/contract/02_invariants.md:30-49`。

4. **位置：`docs/contract/04_interface.md:68`，「入口」**
   - **問題：** 「尚未可用」是會迅速過期的發布狀態，混在長期契約頁中；release 一發布，這句就成為錯誤資訊。
   - **建議：** 移到 README 的目前狀態或 release 說明；04 只保留穩定入口契約。
   - **證據：** `docs/contract/04_interface.md:62-68`。目前 GitHub release 清單確實為空，所以這不是現時事實錯誤，而是易過期資訊。

5. **位置：`docs/contract/04_interface.md:144`**
   - **問題：** `--yes`、`--image` 是非必要別名；它們與定案第 26 條「04 只列指令與必要參數」的邊界不清楚。`-y` 已被 03 的訊息依賴、`-i` 是離線承諾所需，但其長別名目前沒有其他契約依賴。
   - **建議：** 若第 26 條的「必要」是指完成用途所必需，刪除 `--yes`、`--image`，留待實作決定；若是刻意承諾 GNU 長選項，則應寫明它們因相容性而列入，並一併解決 `-p` 缺長選項。
   - **證據：** `docs/contract/04_interface.md:3,144-146,173-201`；`docs/contract/03_messages.md:53-54` 只依賴 `-y`；`GLOSSARY.md:187-189` 目前另有 `--yes` 定義，刪除時需同步處理，但問題仍記在 04。

其餘檢查結果：所有 Markdown 連結都有名稱，目標路徑與錨點存在；「依 02 第 N 條」的條號與錨點相符；04 沒有「出處：」行或 `_Avoid_` 詞；03 與 04 未殘留 `--engine@<tag>`、頂層 `-h`／`--version`、`--timeout` 等已刪寫法；`check_review_pages.py` 與 `check_terms.py` 均通過；03 的指令寫法符合 `check_review_pages` 前置定義規則；01 的離線承諾只寫概念，沒有選項名稱。