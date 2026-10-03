# script/doc — 文件工具

## 對外文件的改動標示（`mark_changes.py`）

對外文件（審閱頁 `doc/contract/0N_*.md` 與根目錄 `README.md`）每改一輪，就產一份標示版讓人只看差異：新增用綠底 `<mark>`，刪除（被取代或拿掉的舊文字）用紅底 `<mark>`。標示版放在送審資料夾 `doc/review/<鍵>/`，只給審閱用，所以可以用 GitHub 會濾掉的 `<mark>` 內嵌樣式；定案後送審資料夾不再保留那一頁，只留正式檔。整套審閱流程（討論分支、定案才 merge、送審給哪兩個檔）見[審閱頁說明](../../doc/contract/README.md)「版本怎麼迭代」，這裡只講工具。內部文件（本檔、`AGENTS.md`、各目錄的 README、ADR 規則等）改完不產標示版、不送審。

### 一輪的流程

1. **改之前先備份**。改動一律走 doc-edit workflow，由 workflow 在第一次修改前自動備份，不手動建 `*.pre_rNN.md`：手動建的檔會被當成已用掉的 round，也可能蓋掉 workflow 保證為「修改前原檔」的那份備份。`_backup/` 已移出 git（#128），只留在本機、已 gitignore。workflow 中途失敗就換下一個 round 重跑，不手動補備份。每輪一個 round，寫成 `rNN`：取本機 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 與 git log 裡 `Doc-Edit: rNN` footer 兩者的最大編號再加一，不能重用；doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是這個最大值加一，重用或跳號就直接停。下一個 round 由 `python3 script/doc/round.py next` 算，`python3 script/doc/round.py check rNN` 檢查給定的 round 對不對（見下面的「輪次編號」）。這一輪的基準後綴（也就是備份尾碼）是 `pre_<round>`，例如 round `r65` 的基準後綴是 `pre_r65`。

   備份檔名是 `<鍵>.pre_<round>.md`，鍵是**把路徑攤平**（去掉 `.md`、`/` 換成 `_`、去掉開頭的點）。所有檔都用這套命名，不限審閱頁。審閱頁 `doc/contract/01_purpose.md` 的備份是 `doc_contract_01_purpose.pre_<round>.md`；`docs/` 併進 `doc/` 之前的備份是舊鍵 `docs_contract_…`（歷史），`mark_changes.py` 兩種都認。

   鍵、備份檔名、序號與「這一輪的基準」的規則以 `backup.py` 為準，見下面的「doc-edit 的備份與範圍檢查（`backup.py`）」。

2. **改**：由 [doc-edit workflow](../../.claude/workflows/doc-edit.js) 的改寫階段派子代理修改（各 workflow 的說明見 [workflow 說明](../../.claude/workflows/README.md)）；本工具不改內容，只在修改完成後產生標示版。

3. **產標示版與正文副本**：

   ```sh
   python3 script/doc/mark_changes.py 01_purpose 02_invariants
   ```

   要在 repo 根目錄執行。審閱頁傳頁名（不含 `.md`）；根目錄 README 傳相對 repo 根目錄的路徑 `README.md`：

   ```sh
   python3 script/doc/mark_changes.py README.md
   ```

   不帶後綴時，基準是這個鍵在 `doc/review/versions.json` 最後一筆 `replied: true` 的紀錄，也就是維護者最後回覆過的那一版（用 `git show` 從紀錄的 commit 取檔）；沒有這樣的紀錄就整份標新增，`versions.json` 還不存在時也一樣，而且不會建立這個檔。鍵已標成定案而且正式檔仍與定案 commit 相同時，不產生送審檔；若送審資料夾還存在就刪掉並印出。正式檔在定案後又有改動時，改用定案版為基準重新產生，並印出「定案後又有改動，回到待審」。要拿本機的改前快照當基準，在頁名前加後綴，例如 `python3 script/doc/mark_changes.py pre_r65 01_purpose`，讀本機 `doc/decisions/_backup/` 裡照步驟 1 命名的備份（例如 `doc_contract_01_purpose.pre_r65.md`）；本機沒有 `_backup/`（換電腦、新 clone）就報錯。新建的頁沒有舊版，後綴寫 `new`，整份標新增。

   輸出到送審資料夾 `doc/review/<鍵>/`，檔名固定、不帶版本號，每次產生就覆蓋：

   - 標示版 `<鍵>.marked.md`。
   - 正文副本 `<鍵>.md`，內容跟正式檔一樣，只差相對連結。

   版本號不在 repo 的檔名裡、也不寫進檔內，只出現在送審 zip 裡的檔名（`<鍵>.v<N>.…`，見下面的「送審打包」）。`doc/review/versions.json` 記每次送審的版號與 commit，進 git，所以換電腦或新 clone 之後版號不會從 v1 重來。每筆紀錄有 `v`、`commit`、`replied`（維護者回覆過沒有），選填 `path`／`csv_path`：有這欄時基準改從 `git show <commit>:<path>` 取，用於舊的 `_marked/` 副本，從副本取時相對連結會先改寫回正式檔位置再比對；副本的連結沒改寫過（照正式檔位置寫）時帶 `raw_links: true`。沒寫 `replied` 的紀錄當成還沒回覆。正式檔改過名時（`mark_changes.py` 的 `RENAMED`：`03_messages` 改名為 `03_output`；訊息表 `03_messages.csv` → `03_output.csv` → `reason_codes.csv`，#137），鍵跟著改名，舊紀錄不補 `path`：沒寫 `path`／`csv_path` 而紀錄的 commit 裡還沒有新路徑時，基準由新到舊依序改取改名前的路徑（`reason_codes.csv` 找不到就試 `03_output.csv`，再試 `03_messages.csv`）；所有基準（含其他頁、本機備份）裡連到改名前路徑的連結也先換成新路徑再比對，只因改名而不同的行不標成改動。`versions.json` 頂層另有 `finalized` 物件，`finalized.<鍵>` 是 `{"v": N, "commit": "<sha>"}`，那一版的送審紀錄有 `path`、`csv_path`、`raw_links` 時一併照抄；沒有任何鍵定案時沒有這個欄位。`mark_changes.py` 只讀 `versions.json`、不寫、不取號，也不改正式檔。

   標示版裡的相對連結會改寫成從送審資料夾出發（正文副本也一樣）：以原檔所在目錄解析成 repo 內的實際路徑，再換成從 `doc/review/<鍵>/` 出發的相對路徑，錨點照留；指到其他審閱頁的連結指正式檔 `doc/contract/<頁>.md`，不指副本。外部網址、純錨點、行內程式碼與程式碼區塊裡的字樣不改，正式檔也不動。

   正式檔名不帶版本號、不改名，其他文件的連結才不會斷。鍵對審閱頁是頁名（例如 `04_interface`），對其他檔是攤平後的路徑（`/` 換成 `_`、去掉 `.md` 與開頭的點，所以 `README.md` 的鍵是 `README`）。鍵 `README` 一律對到根目錄的 `README.md`；`doc/contract/README.md` 要傳路徑，鍵是 `doc_contract_README`。

   基準選擇、輸出檔名與連結改寫這些行為由 [mark_changes 測試](test/test_mark_changes.py) 涵蓋，在 repo 根目錄跑 `python3 -m unittest discover -s script/doc/test`。

4. **基準是維護者最後回覆過的那一版；定案後又有改動時是定案版**，不是最舊的那一版，也不是最後送出、還沒回覆的那一版。不帶後綴時自動選擇；要指定別的送審版本，用 `--base-version` 指定版號（不看 `replied`）：

   ```sh
   python3 script/doc/mark_changes.py --base-version 03_output=13 04_interface=18 GLOSSARY=6
   ```

   基準是 `versions.json` 裡這個鍵版本 `<N>` 記的 commit，用 `git show` 取當時的正式檔，有附屬 CSV 時也一起取；那個 commit 裡沒有那份 CSV 時視為新建、整份標新增。左邊寫頁名、路徑或鍵都行（`GLOSSARY`、`README` 對到根目錄的檔；`doc/contract/README.md` 要寫路徑）。任何一個指定版號在 `versions.json` 裡找不到就停下報錯，整批都不產。已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **用 `pack_review.py` 打包送審**（見下面的「送審打包」）：zip 裡放 `<鍵>.v<N>.md` 與 `<鍵>.v<N>.marked.md`，版本號是打包時取的。不交正式檔。維護者回覆後，用 `python3 script/doc/pack_review.py --replied <鍵>=<N>` 把那一版標成回覆過，下一輪的預設基準才會前進到那一版。定案後又有改動的鍵照常取下一個版號；再次打包時清掉這個鍵的 `finalized`，回到待審。

6. **草稿 commit 在討論分支，定案才 merge 進 `main`**。維護者定案後，用 `python3 script/doc/pack_review.py --finalized <鍵>=<N>` 記下定案版本並刪除該鍵的送審資料夾；定案版就是正式檔，之後隨 PR merge 進 `main`。下一輪從 `main` 開新的討論分支，再跑 doc-edit workflow，由它自動備份當時的正式檔，不手動從 `main` 取檔建備份。

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題行（`#` 開頭）保持原樣、不加任何標籤：檢視器用標題文字產生錨點，標籤混進去錨點就變了，目錄連結跳不過去。新增的標題在下一行註記綠底「（本節新增）」；改過的標題在下一行標紅底「舊標題：<舊文字>」，再接一行綠底「（標題已修改）」；刪掉的標題去掉 `#`，以紅底呈現在普通文字行，不產生錨點。
- 清單、引言的行首記號留在標籤外，否則會變成普通文字。
- 粗體留給結構標籤、名詞第一次出現於正文時連到 `GLOSSARY.md` 的所屬分群、綠底與紅底的 `<mark>` 留給改動，三者互不衝突。

### 審閱頁的附屬 CSV（`03_output` ↔ `reason_codes.csv`）

審閱頁的附屬 CSV 明列在 `mark_changes.py` 的 `COMPANION_CSV`，不靠同名推：目前只有 03 頁 `03_output` ↔ 訊息表 `doc/contract/reason_codes.csv`（#137）。傳頁名 `03_output`（或路徑 `doc/contract/reason_codes.csv`，改名前的 `doc/contract/03_output.csv` 也認，效果相同）會一起處理 `.md` 與 `.csv`，兩個檔共用 `versions.json` 裡同一個鍵 `03_output`，送審時一次只加一號。在 `doc/review/03_output/` 輸出三個檔：

- `03_output.md`：03 頁的正文副本（03 頁這一輪沒改也照樣輸出）。
- `reason_codes.csv`：CSV 的副本，檔名照正式檔，逐位元組照抄（BOM、LF 都保留）。改名前產的 `03_output.csv` 副本重產時刪掉。
- `03_output.marked.md`：合併的標示版。前半是 03 頁的逐行差異，規則同上；後半是「reason_codes.csv 的逐碼差異」。

CSV 的逐碼差異：新舊兩版依 `code` 對齊、逐欄比較，每個有改動的代碼寫成一段 `#### VKnnnn`，依新表頭的欄位順序列出這個代碼的各欄。改過的欄寫成紅底舊值 → 綠底新值，沒改的欄照原樣列出、不加標記。新增的代碼在標題下一行註記綠底「（本碼新增）」、各欄標綠；改成 `retired` 的註記紅底「（本碼停用）」；從 CSV 拿掉的列註記紅底「（本列刪除）」、各欄標紅。表頭改了（例如刪掉欄）時，逐碼差異開頭先標出新舊表頭，並逐欄註記紅底「（本欄刪除）」或綠底「（本欄新增）」；新增的欄照新表頭的位置列出，各碼標綠新值並註記綠底「（本欄新增）」，新值是空的不算改動；刪掉的欄排在新表頭各欄之後，列出舊值並標紅，所以只刪欄的代碼也算有改動。沒改動的代碼不成段，最後用一行列出有幾個、是哪些。欄位值裡的 `<`、`>` 會跳脫，占位符照原樣看得到；格內換行改成 `<br>`。

不帶後綴或用 `--base-version` 時，CSV 的基準跟 `.md` 一樣從送審紀錄的 commit 取（紀錄有 `csv_path` 就取那個路徑）。帶後綴時，CSV 的基準版是本機 `doc/decisions/_backup/doc_contract_reason_codes.<後綴>.csv`（CSV 自己路徑的攤平鍵，跟 `backup.py` 同一套），找不到再依改名紀錄找舊名的 `doc_contract_03_output.<後綴>.csv`；以下是後綴模式的規則。兩個檔只有一個有基準版時，另一個視為這一輪沒改；CSV 沒有基準版、也不在 git 的 `HEAD` 裡時，視為新建、整份標新增。這兩種情況都會印在輸出，也寫在標示版開頭。兩個都沒有基準版就停下。基準後綴寫 `new` 時，兩個檔都整份標新增。

## doc-edit 的備份與範圍檢查（`backup.py`）

doc-edit 的備份、改前快照、備份檢查、範圍外檢查與這一輪的 diff 由這支做，規則只寫在這裡（#139）。以前由子代理照 workflow 的文字步驟做，r152 因此誤判（#133）。每種用法都在 stdout 印一行 JSON，成功與失敗都有 `ok`；全過結束碼 0，有問題 1，用法錯（參數、輪次格式、repo 不是 git repo、檔案不在 repo 裡）2。檔案一律寫相對 repo 根目錄的路徑。

```sh
python3 script/doc/backup.py key <檔>...
python3 script/doc/backup.py save --repo <repo> --round <rNN> <檔>...
python3 script/doc/backup.py base --repo <repo> --round <rNN> <檔>
python3 script/doc/backup.py diff --repo <repo> --round <rNN> <檔>
python3 script/doc/backup.py snapshot --repo <repo> --out <json> [--files <檔>...]
python3 script/doc/backup.py verify --repo <repo> --round <rNN> --before <json> --scope <檔>... --round-files <檔>...
```

- **鍵**（`key` → `{ok, keys: [{file, backup_key, run_key}]}`）：`backup_key` 是上面「一輪的流程」第 1 步的攤平鍵（去掉 `.md` 或 `.csv`、`/` 換成 `_`、去掉開頭的點），跟 `mark_changes.py` 同一套，備份檔名用它。`run_key` 在 `.md`、`.csv` 檔的 `backup_key` 後面接 `_md` 或 `_csv`（`doc/contract/reason_codes.csv` → `doc_contract_reason_codes_csv`），給暫存目錄與 review_log 檔名用：同名的 `.md` 與 `.csv`（例如改名前的 `03_output.md` 與 `03_output.csv`）`backup_key` 相同，備份靠副檔名分開，暫存檔與 review_log 不分開就會互相覆蓋（r163）。其他檔的 `run_key` 等於 `backup_key`。
- **備份**（`save` → `{ok, results: [{file, backup, created, seq, md5, missing}]}`）：備份到 `doc/decisions/_backup/<backup_key>.pre_<round><ext>`，`<ext>` 對 `.csv` 檔是 `.csv`、其他一律 `.md`。這一輪的基準（不帶序號，`seq` 為 1）不存在就建它；已存在時，目前內容的 md5 等於這一輪任何一份既有備份就不另存、回報那一份；否則另存 `.pre_<round>.<N><ext>`，N 從 2 起、取現有最大加一。檔案不存在（這一輪新建的檔）不備份，`missing` 為 true。不手動 `cp`、不自己編序號。
- **基準**（`base` → `{ok, file, base, exists}`）：這一輪不帶序號的那份備份的路徑與它在不在。
- **這一輪的 diff**（`diff` → `{ok, file, base, base_kind, empty, diff}`）：基準優先用這一輪的基準備份（`base_kind` 為 `backup`），不存在就用 `git show HEAD:<檔>`（`HEAD`），都沒有就整份算新增（`none`）。`diff` 是 unified diff 文字，`empty` 為 true 表示這一輪沒改這個檔。
- **改前快照**（`snapshot` → `{ok, out, paths}`）：記下 `git status` 的每個路徑（含未追蹤的檔）與 md5、`--files` 每個檔的 md5、`_backup/` 的檔名清單，寫進 `--out`。`--out` 放在 scratchpad，不放 repo 裡，否則它自己會被當成變動。
- **比對**（`verify` → `{ok, changed, new_backups, backup_problems, out_of_scope, parallel, diffstat}`）：重做一次快照，跟 `--before` 比。
  - `changed`：改前或現在的 `git status` 有的路徑、以及快照記過的檔，md5 變了的。快照沒記到的路徑，改前內容當成 `HEAD` 的版本。
  - `backup_problems`（#133）：`--scope` 裡變了、改前就存在的檔，這一輪的基準必須存在，而且改前的 md5 必須等於這一輪某一份既有備份（基準或帶序號的），也就是改前狀態能從既有備份還原。基準已經等於改前內容時，不必另存備份。
  - `out_of_scope`：變了、不在 `--round-files`、也不在 `doc/decisions/` 底下的路徑。只回報，不還原。
  - `parallel`：在 `--round-files`、不在 `--scope` 的變動，是同一輪並行的子代理造成的，不算錯。
  - `new_backups`：快照之後 `_backup/` 新出現的檔；`diffstat`：`git diff --stat -- <scope>`。
  - `backup_problems` 或 `out_of_scope` 不是空的，`ok` 就是 false、結束碼 1。

鍵跟 `mark_changes.py` 一致、序號、重現 r152、範圍外與 diff 退回 `HEAD` 這些行為由 [backup 測試](test/test_backup.py) 涵蓋。

## 輪次編號（`round.py`）

算 doc-edit 一輪的 round，取代以前照抄的一行 shell（那行用了 bash 的大括號群組，換 shell 結果就不固定）：

```sh
python3 script/doc/round.py next [--repo <R>]
python3 script/doc/round.py check r66 [--repo <R>]
```

`--repo` 不給時用目前目錄所在 git repo 的根目錄。已用過的編號有兩個來源：`<R>/doc/decisions/_backup/` 檔名裡的 `pre_rNN`（只看這個目錄本身；帶序號的備份 `….pre_r12.2.md` 也算 12），與 `git log --format=%B` 裡行首的 `Doc-Edit: rNN` footer。輸出一行 JSON：

- `next`：`{"ok": true, "max", "next", "backup_max", "footer_max"}`。`backup_max`、`footer_max` 是各來源的最大編號，沒有就是 `null`（`_backup/` 不存在也是 `null`）；`max` 取兩者最大，都沒有是 `0`；`next` 是 `r<max+1>`。
- `check`：同上，再加 `round`（給的值）與 `expected`（等於 `next`）。格式不是 `rNN`，或編號不等於 `max+1`（重用或跳號）時 `ok` 是 `false`、附 `error`，結束碼 1。

結束碼：0 成功（`check` 時 round 正確）；1 是 `check` 不通過；2 是執行失敗（不是 git repo、git 失敗），輸出 `{"ok": false, "error"}`。各種來源組合與 `check` 的重用、跳號由 [round 測試](test/test_round.py) 涵蓋。

## 送審打包（`pack_review.py`）

把送審資料夾 `doc/review/<鍵>/` 打包成一個 zip，檔名一律是 `review_v<N>.zip`：

```sh
python3 script/doc/pack_review.py --note <審閱說明.md> --out <目錄> 03_output 04_interface GLOSSARY.md
```

在 repo 根目錄執行，頁鍵的寫法跟 `mark_changes.py` 相同。每個鍵取 `doc/review/<鍵>/` 裡的 `<鍵>.marked.md`、`<鍵>.md`，有附屬 CSV（例如 `reason_codes.csv`）也一起放；zip 內檔名帶版本號：`<鍵>.v<N>.marked.md`、`<鍵>.v<N>.md`，CSV 用它自己的檔名 `<CSV 名>.v<N>.csv`（例如 `reason_codes.v17.csv`，版號跟所屬的頁共用），N 是這個鍵在 `versions.json` 最後送審的版號加一（從沒送審過是 1）。打包前先檢查：正式檔（與附屬 CSV）有未 commit 的改動、送審資料夾的正文副本跟正式檔不一致（沒重跑 `mark_changes.py`）、或缺檔，就停下報錯，不取號、不寫 `versions.json`。都過了才打包，並把 `{"v": N, "commit": HEAD, "replied": false}` 追加進各鍵的紀錄、`review_zip` 加一；這個鍵若已定案，同時刪掉它的 `finalized` 紀錄。zip 的 N 是新的 `review_zip`。zip 內檔名不帶目錄，有 `--note` 時審閱說明排第一個。`--out` 必填，沒給就以結束碼 2 停下：送審 zip 是送審版本號唯一的出處（#128），要放在 workspace 裡的固定目錄（例如 `vendor-kit_ws/reference/review_sent/`），不放系統暫存目錄；目錄不存在就建立。跑完印出 zip 路徑與內容清單。本工具只打包，標示版照舊由 `mark_changes.py` 產生。

維護者回覆之後，標記他回覆的版本：

```sh
python3 script/doc/pack_review.py --replied 03_output=14 README=3
```

只把 `versions.json` 裡那幾筆的 `replied` 改成 `true`，不打包、不取號，不用給 `--out`。鍵的寫法同 `--base-version`；任何一筆找不到就停下報錯，整批不改。`mark_changes.py` 的預設基準：已定案的鍵用定案版本，其餘用各鍵最後一筆 `replied: true` 的紀錄。

維護者定案之後，標記定案版本並移除該頁的送審資料夾：

```sh
python3 script/doc/pack_review.py --finalized 03_output=14 README=3
```

指定的版本必須已送審且已標成 `replied: true`；任何一筆不存在或尚未回覆就停下，整批不改、不刪。成功時在各鍵記下 `finalized` 的版本與該版本紀錄的 commit（紀錄有 `path`、`csv_path`、`raw_links` 也照抄），並刪除 `doc/review/<鍵>/`。這個模式不打包、不取號、不用給 `--out`。正式檔若之後又有改動，`mark_changes.py` 會以這個定案版本為基準重建送審資料夾；再次打包時照常取下一個版號，並清掉這個鍵的 `finalized`，回到待審。

版號遞增、內容、缺檔報錯（含還沒有 `doc/review/` 的情況：三種模式都報錯停下，不建 `versions.json`）與定案處理由 [pack_review 測試](test/test_pack_review.py) 涵蓋。

## 送審副本路徑與版本表（`review_paths.py`）

給 `review-pack` workflow 用：列出每頁送審副本的本機路徑、這次打包的版號與基準，以及送審 zip 的內容，都印成一行 JSON。

```sh
python3 script/doc/review_paths.py pages --repo <repo> 02_invariants 03_output 04_interface GLOSSARY.md
python3 script/doc/review_paths.py zip <review_vN.zip>
```

`pages` 在 `--repo` 讀 `doc/review/versions.json` 與 `doc/review/<鍵>/`，頁鍵寫法跟 `mark_changes.py` 相同；鍵、送審資料夾、版號與基準都呼叫 `mark_changes.py` 的函式算。輸出的 `zip_next` 是這次打包會用的 zip 號（`review_zip`＋1）；`pages` 每筆有送審資料夾的絕對路徑 `dir`、相對路徑 `rel_dir`、資料夾裡 `.md`、`.marked.md`、`.csv` 的絕對路徑 `files`、這次的版號 `version`（最後送審的版號＋1），以及 `mark_changes.py` 預設的基準 `base`（`kind` 是 `finalized` 定案版、`replied` 維護者最後回覆的版本、或 `none` 整份標新增）；`dirty` 是送審資料夾裡未 commit 的 `git status --porcelain` 行。版號與基準要在 `pack_review.py` 打包之前取：打包會追加這一版的紀錄並清掉 `finalized`。`zip` 印出 zip 內的檔名（照 zip 內順序）。成功結束碼 0；找不到檔或不是 git repo 時結束碼 1，JSON 的 `ok` 是 false、`error` 寫原因。

版號、三種基準、附屬 CSV、絕對路徑與 zip 清單由 [review_paths 測試](test/test_review_paths.py) 涵蓋。

## 名詞表自檢（`check_context.py`）

根 `CONTEXT.md` 每改一次就跑，不要目視：

```sh
python3 script/doc/check_context.py
```

查四件事，全過印 `OK` 回 0，任一不過逐條印出回 1：

- `## 目錄` 的分群與 `## Language` 下的 `###` 分群一字不差、順序一致。
- 每個目錄條目的 `#term-xxx` 對得上一個 `<a id="term-xxx"></a>`，兩邊數量、分群歸屬與順序都一致，錨點不重複。
- 每個錨點的下一行是 `**名詞**（english）：` 格式，且目錄寫的名詞與正文一致。
- 所有 `_Avoid_` 列出的詞都沒出現在正文（`_Avoid_:` 那行本身除外）——改名沒改乾淨會在這裡被擋下。

## 舊名殘留自檢（`check_terms.py`）

`check_context.py` 只管 `CONTEXT.md` 自己；改名改到一半、舊詞留在某一頁，要靠這支抓：

```sh
python3 script/doc/check_terms.py
```

每筆殘留印 `<檔>:<行號>  <詞>  <該行內容>`，全乾淨印 `OK` 加統計（掃了幾個檔、幾個 `_Avoid_` 詞）。有殘留回 1，乾淨回 0。

- **詞從哪裡來**：每次跑都從根 `CONTEXT.md` 的 `_Avoid_:` 行現抽，不寫死清單。名詞表會長大，寫死的清單幾次改名之後就跟名詞表脫鉤，而且是靜默的。
- **掃哪些檔**：`git ls-files -co --exclude-standard` 取得的現行 `.md` 檔。`doc/decisions/_backup/`、`doc/decisions/review_log/`、`doc/research/` 已移出 git 並 gitignore，本來就不在清單裡。排除 `doc/decisions/review/_marked/`（本地產物）、`.claude/skills/`（vendored 的第三方 skill）、`script/diagram/`（圖面工具，等 #138 重做），以及 index 裡還留著但已刪除的檔。
- **不算殘留的行**：`_Avoid_:` 行本身；以及帶「舊名」「已廢止」「已移除」「之名作廢」「舊審閱頁」「改名」這類引述標記的行——講改名史本來就得同時寫出新舊兩個詞。標記清單是 `check_terms.py` 頂端的 `QUOTE_MARKERS` 常數，要放行新的講法就加在那裡。
- **逐行白名單**：已定案要保留舊詞的**個別一行**登記在 `check_terms.py` 頂端的 `WHITELIST`，每筆是 `(檔案路徑, 該行必須包含的字串, 理由)`。三個欄位都要對上才放行，而且只放行「那段字串裡面」的舊詞：把字串從該行挖掉之後還搜得到舊詞，照樣算殘留。所以同一個檔的其他行、同一行的其他位置、別的檔抄同一段字，全都還是會被抓到。只比對詞會讓那個詞全域失效、只比對檔案會讓整個檔失效，白名單就變成漏洞——這是刻意不做的兩種寫法。白名單筆數印在 `OK`／`FAIL` 那行，悄悄長大會看得見。
- **目前的兩筆**：`doc/decisions/review/01_purpose.md` 的 `# 01 專案目的與承諾` 與 `doc/decisions/README.md` 裡引用這個標題的那一列。使用者定案：標題保留這個舊名，因為那裡指的是 VK 這個專案本身，不是名詞表裡指使用者 repo 的那個詞；`README.md` 那一列是在引用頁標題，同一個道理。（這一行自己帶「舊名」標記，靠上面的引述規則過關，不再多開一筆白名單。）
- **「數位簽章」例外**：「簽章」是名詞「印記」的舊名，但「數位簽章」是密碼學的標準術語（digital signature），跟印記無關——講 registry 或 image 的簽章時本來就該這樣寫。所以用負向前瞻 `(?<!數位)簽章` 只抓單獨的「簽章」，否則這支腳本會逼著大家把正確的詞改掉。

## 中英排版自檢（`check_typography.py`）

改了 `README.md`、`doc/contract/*.md`、`doc/contract/*.csv` 或 `GLOSSARY.md` 就跑，CI 的 docs-lint job 也跑這支：

```sh
python3 script/doc/check_typography.py
python3 script/doc/check_typography.py --fix
```

在 repo 根目錄執行。全過印 `OK` 回 0；有違規逐條印 `<檔>:<行>: <問題與建議寫法>` 回 1。加 `--fix` 直接改檔，只動下面三條規則涉及的空白與括號，其他字元不動。規則是維護者定案的：

- 括號裡全是 ASCII（英文、數字、符號）時用半形括號，半形括號與中文之間空一格：「檢查（test）」寫成「檢查 (test)」。括號裡有中文就維持全形「（…）」。
- 中文與英文字母或阿拉伯數字相鄰時中間空一格：「VK的recipe」寫成「VK 的 recipe」、「第12條」寫成「第 12 條」。全形標點（，。、：；「」（）等）與英數之間不加空白。
- 行內程式碼（反引號包住的）與前後的中文相鄰時也空一格：「`0`結束」寫成「`0` 結束」、「印`VK0024`」寫成「印 `VK0024`」。與全形標點相鄰不加空白；隔著連結的 `[` 或 `](…)` 時照上一條，連結記號不算字元。

不查行內程式碼的內容、程式碼區塊、URL、Markdown 連結目標（括號裡的路徑與錨點）與 HTML 標籤。CSV 只查文字欄（`situation`、`message`、`description`、`next_step`），`code`、`status`、`level`、`exit_code`、`disposition` 是固定值域，不查；英文的 `message` 與 `next_step` 仍會掃描，但不會因英文排版本身誤報。`--fix` 改到 CSV 時，若 `next_step` 不再逐字出現在 `message` 裡，這支照樣報錯，要手動把兩欄對齊；改到標題時 GitHub 產生的錨點跟著變，連到舊錨點的連結不會自動改，要另外改。

各條規則的正反例與排除範圍在 [check_typography 測試](test/test_check_typography.py)。

## 訊息表自檢（`check_messages.py`）

`doc/contract/reason_codes.csv` 是每個原因代碼的唯一出處（#122）。改了 CSV，或其他頁引用代碼的地方就跑：

```sh
python3 script/doc/check_messages.py
```

在 repo 根目錄執行。全過印 `OK` 回 0，任一不過逐條印出回 1。CSV 還不存在時印 `OK` 並跳過。CSV 與 03 頁的路徑只寫在 `check_messages.py` 頂端的 `CSV_PATH`、`MD_PATH` 兩個常數（#137：CSV 從 `03_output.csv` 改名為 `reason_codes.csv`）。錯誤位置報 `<檔>:<代碼>:<欄名>`，例如 `doc/contract/reason_codes.csv:VK0003:message.zh-TW`，不報實體行號。

表頭（#343）：`code,status,level,exit_code,disposition,situation.en,message.en,situation.zh-TW,message.zh-TW`。前五欄給程式讀、用英文；給人看的欄照語言分組放右邊，以後加語言就在最右邊接一組 `situation.<lang>,message.<lang>`。`en` 是基準語言：VK 印出的字句目前都用英文，其他語言的欄跟 `message.en` 比對。查這幾件事：

- 格式：UTF-8 開頭恰好一個 BOM、只准 LF、檔尾恰好一個換行；用 `csv` 模組以 strict 照 RFC 4180 解析，每列欄數與表頭相同。格內換行（雙引號包住的 LF）解析得過。欄位頭尾不准空白，不准以 `=`、`+`、`-`、`@`、Tab、CR 開頭（Excel 會當成公式）。
- 表頭：讀表依首行欄名，不依欄序。首行必須以 `code,status,level,exit_code,disposition` 開頭，其後是一組組 `situation.<lang>,message.<lang>`（同一語言成組、`situation` 在前）；必須有 `en` 與 `zh-TW` 兩組（`REQUIRED_LANGS`）。其他欄名（包括舊的 `situation`、`message`、`description`、`next_step`）報錯。
- 代碼：`VK` 加四位數字，從 `VK0001` 起逐列加一，所以唯一、遞增、不缺列；停用的代碼留列。
- `status` 只准 `active`、`retired`。每列每個語言的 `situation.<lang>` 都必填；`retired` 列只留 `code`、`status` 與所有 `situation.<lang>`，其餘欄要空白。
- `active` 列：`level` 只准 `warn`、`error`、`fatal`；`exit_code` 必須依序對應 `1`、`2`、`3`；每個語言的 `message.<lang>` 必填。
- `disposition` 只准 `pending`、`failed` 或空白；`warn` 一律空白，只有 `warn` 與用法錯誤可留空，其他 `error`、`fatal` 的 `active` 列必填。用法錯誤看 `situation.en` 是否以 `Usage error:` 開頭（大小寫照此）；其他語言的 `situation` 不參與判斷。
- 結尾指令：`message.en` 最後一行最後一個 `: ` 之後的片段，是單一占位符（例如 `<original_command>`），或以 `just `、`git `、`sh `、`cd ` 開頭，就算以指令結尾。`pending` 列的 `message.en` 必須以指令結尾；`failed` 列不限。`message.en` 以指令結尾時，其他語言的 `message.<lang>` 必須逐字包含同一個指令字串。
- 語言欄：`message.en`、`situation.en` 不准含中文字元；其他語言欄不限。`message.<lang>` 的 `<…>` 占位符集合與換行數要與 `message.en` 相同。
- 欄位不准 HTML（有屬性的標籤、結束標籤、`<ins>`、`<br>` 這類常見標籤名、`<!--`）與 Markdown（反引號、粗體、刪除線、連結、行首的標題、清單或引言記號）；不帶屬性的 `<…>`（例如 `<repo>`、`<P>`）算占位符。`<`、`>` 要成對、不巢狀。
- 引用：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡出現的每個 `VKnnnn` 都要在 CSV 裡、而且是 `active`；`doc/adr/*.md` 只要求在 CSV 裡，可以是 `retired`。連到 `reason_codes.csv` 不准帶 `#`；連結文字是代碼時不准連 `03_output.md`（03 頁不放逐碼內容），一律連 CSV。01、02 不准連 CSV。
- 診斷範例：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡的 `vendor_kit: <level>[VKnnnn]: <本文>`，level 要等於 CSV，本文要符合 `message.en` 第一行，`<…>` 占位符可以對應任意文字。
- `active` 列的 `message.en` 句首要大寫，或以占位符、小寫指令名 `just` 開頭；結尾要是句點，或以指令結尾（上面的結尾指令，或 `just vendor_kit` 指令）。這條只套用在 `message.en`。

欄位約定：`message.<lang>` 是印出的本文，不含 `vendor_kit: <level>[VKnnnn]: ` 前綴；下一步指令寫在 message 句尾，不另開欄。`situation.<lang>` 是這個代碼的唯一意思，給人讀。

CSV 的 `situation.<lang>`、`message.<lang>` 裡的指令寫法（`just vendor_kit …`）不在這支的範圍，由 `check_review_pages.py` 的 L4 檢查。

各條規則的正反例在 [check_messages 測試](test/test_check_messages.py)。

## 對外頁寫法自檢（`check_review_pages.py`）

改了根目錄 `README.md`、`doc/contract/0N_*.md` 或訊息表 `reason_codes.csv` 就跑，CI 的 docs-lint job 也跑這支：

```sh
python3 script/doc/check_review_pages.py
```

在 repo 根目錄執行。全過印 `OK: 掃 N 個對外文件` 回 0；有違規逐條印 `<檔>:<行>: <問題>` 回 1，CSV 的位置報 `<檔>:<代碼>:<欄名>`。掃描範圍是根目錄 `README.md` 與 `doc/contract/0N_*.md`，另掃訊息表 `doc/contract/reason_codes.csv` 的指令欄（明列檔名，不掃其他 `03_*.csv`）。檔案還不存在就少掃那些，不算錯誤。查這幾件事：

- 每頁有 `## 目錄`；不寫「出處：」行，也不寫 `> 版本 vN`。
- 不准任何 HTML 標籤，`<ins>`、`<a id>`、`<br>` 也不行；行內程式碼裡的、反斜線跳脫的 `\<repo\>` 不算。
- 相對連結的檔案與錨點都要存在，錨點照 GitHub 的標題轉換規則算；不准以 `/` 開頭。
- 引用別頁條目寫「依 [頁名第 N 條](連結#錨點)」，不寫舊寫法「[名字](連結) 第 N 條」。
- 連結文字不得含反引號：碼放在連結外，例如「[結束碼](03_output.md#結束碼) `2`」。連結文字裡的 `<…>` 要跳脫成 `\<…\>`。
- **L1**：01、02 不准原因代碼 `VKnnnn`，行內程式碼照掃，程式碼區塊不掃。
- **L2**：01、02 的「結束碼」前後 10 字內不准反引號包住的單位數字，也不准 `exit code <數字>`。
- **L3**：內容只能往前依賴，導覽可以往後指。審閱頁 N 以「依」或「依照」連到後面的頁就擋；README 是入口不是第 0 頁，以「依」連到審閱頁也擋。只是導覽就寫「詳見」。
- **L4**：README 與 03 的行內程式碼、訊息表 `reason_codes.csv` 所有以 `situation.`、`message.` 開頭的欄（依首行欄名找，不寫死語言，例如 `situation.en`、`message.zh-TW`），以 VK recipe 名或 `just vendor_kit <recipe>` 開頭的片段，用到的選項 token（含單獨的 `--` 與 `@<tag>`）都要先在 `GLOSSARY.md`、01、02 的行內程式碼出現過，逐 token 完整比對。還沒有 `GLOSSARY.md` 時整條跳過。

頂端的 `TEMP_ALLOWLIST` 放暫時豁免的個別錯誤（整行原文完全相同才放行），目前是空的；輸出第一行會印筆數與命中數，悄悄長大看得見。

各條規則的正反例在 [check_review_pages 測試](test/test_check_review_pages.py)。

## 潤稿越界檢查（`polish_check.py`）

doc-edit 的潤稿只准改這一輪改過的行。這支比「潤稿前」與「潤稿後」，找出落在範圍外的變動，帶 `--fix` 就把那些段還原成潤稿前的原文：

```sh
python3 script/doc/polish_check.py <基準> <潤稿前> <潤稿後> [--fix]
python3 script/doc/polish_check.py --repo <R> --round <rNN> <file> <潤稿前> [--fix]
```

- 第二種用法自己取基準，doc-edit 的潤稿改用它，子代理不再自己準備基準檔：`<file>` 是相對 repo 的檔，潤稿後就是 `<R>/<file>`；基準跟 `backup.py diff` 同一套順序，這一輪的基準備份存在就用它，否則用 `git show HEAD:<file>`，都沒有就是空內容（整份算這一輪的新增）。判定直接 import [`backup.py`](backup.py) 的函式，基準只在記憶體裡比，不寫暫存檔。輸出多 `base_kind`（`backup`／`HEAD`／`none`）與 `base`（`backup` 時是基準備份的路徑，其他是 `null`）。

- 範圍：`<基準>`（這一輪改之前的原檔）→ `<潤稿前>` 的新增或修改行。
- 等長的替換逐行判斷；其他變動整段判斷，整段都要在範圍內；純插入只要緊鄰的前一行或後一行在範圍內就保留。
- `<基準>` 與 `<潤稿前>` 相同（這一輪沒改這個檔）時，任何變動都算越界。

輸出一行 JSON `{"ok", "round_changed_lines", "violations", "reverted"}`；`violations` 每筆有 `pre_lines`、`post_lines`（從 1 起算，含迄）與 `post_text`。結束碼：沒有越界回 0；有越界且已 `--fix` 還原回 0（`reverted` 為 `true`，再不帶 `--fix` 跑一次確認 `violations` 為空）；有越界沒還原回 1；讀不到檔回 2，第二種用法的參數不對（輪次格式、repo 不是 git repo、檔案不在 repo 裡）也回 2。

各種情況的正反例在 [polish_check 測試](test/test_polish_check.py)。
