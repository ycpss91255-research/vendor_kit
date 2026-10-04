# 審閱頁

這個目錄放 [VK](../../GLOSSARY.md#角色與情境) 對外[契約](../../GLOSSARY.md#介面版與契約)的審閱頁。給第一次來看的人，也給要改這幾頁的 agent。

## 這個目錄放什麼

一頁一個主題，依序讀：

1. [01 目的與承諾](01_purpose.md)：為什麼做 VK、對[使用者](../../GLOSSARY.md#角色與情境)承諾什麼。
2. [02 不變量](02_invariants.md)：任何版本都必須成立的性質。
3. [03 輸出](03_output.md)：每個[結束碼](../../GLOSSARY.md#執行與結果)的意思，與 VK 印出、要使用者動手處理的訊息。
4. [04 使用者介面](04_interface.md)：全部 [VK recipe](../../GLOSSARY.md#vk-recipe-與用途) 與選項。

契約放在這裡，不放 issue：issue 不好追蹤改動，也做不了逐頁審與標示版差異。出處：[工作約定](../../AGENTS.md)「決議與文件流程」。

## 寫法規則

- 內容（論據、名詞、選項）只能往前依賴：頁 N 只能用前面的頁與[名詞表](../../GLOSSARY.md)。
- 導覽指標（例如「詳見 04」，只告訴讀者去哪裡看、不當論據）可以往後指，前提是拿掉連結後那一段仍讀得懂。
- 根目錄 README 暫時移除，之後重寫時只做導覽與快速流程（見 [issue #375](https://github.com/ycpss91255-research/vendor_kit/issues/375)）。
- 對外頁不寫「出處」。沿用前面頁的規則時，在正文寫「`依 [頁名第 N 條](連結#錨點)`」，連到那一條的標題錨點；不引用 ADR 或 issue。
- 以[**名詞表**](../../GLOSSARY.md)的粗體詞條為準；名詞在每頁正文第一次出現時，連到該名詞所在的名詞表分群標題。同頁後續出現不重複連結。標題、程式碼區塊、行內程式碼與已有連結文字不算正文第一次；名詞先出現在標題時，連結放在標題下第一次出現於正文的位置。
- 不用 HTML 標籤標示名詞。錨點一律由標題產生：要連到表格裡的某一列，就連到它所在的標題，連結文字寫出是哪一條，例如「以[結束碼](03_output.md#結束碼) `2` 結束，訊息見 [03 輸出](03_output.md#訊息)」。名詞表的名詞沒有個別錨點，連到它所在的分群標題，例如 `[工具](../../GLOSSARY.md#工具與出貨)`。
- 術語集中在名詞表，同一條規則只寫一次。同一份內容寫在多頁（重複來源）違反的是這一條，不算往後依賴，另外處理。其他頁要用到，照上面「對外頁不寫出處」那條寫「`依 [頁名第 N 條](…)`」，或連到章節，不重述。
- 連結用有名字的超連結，例如 `[不變量](02_invariants.md)`，不要把路徑當連結文字。連結文字不放反引號；程式碼名詞當連結時寫 `[\<repo\>](…)`。

## 版本怎麼迭代

這一節是對外文件審閱的固定流程，新接手的 agent 照這個順序做。出處：維護者 2026-09-30 定案；[issue #64](https://github.com/ycpss91255-research/vendor_kit/issues/64)。

1. **草稿只改在討論分支。** 對外文件是本目錄的審閱頁（目前 01～04）。草稿一律改在討論分支並開 PR，`main` 上只放定案版。定案之後才 merge 進 `main`，定案的條件見下一節。
2. **改動一律跑 [doc-edit workflow](../../.claude/workflows/doc-edit.js)**。workflow 在第一次修改前自行把原內容備份到本機的 `doc/decisions/_backup/<鍵>.pre_<round>.md`，不用另外手動備份；`_backup/` 只在本機，不進 git（見[忽略清單](../../.gitignore)）。round 名稱是 `rNN`：取本機 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 與 git log 裡 `Doc-Edit: rNN` footer 最大的編號，兩者取大再加一（例如最大是 `r100`，round 就是 `r101`），用過的不能重用。doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是最大編號加一，重用或跳號就直接停。目前最大的編號這樣查：

   ```sh
   { ls doc/decisions/_backup 2>/dev/null | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//'; git log --format=%B | grep -oE '^Doc-Edit: r[0-9]+' | sed 's/^Doc-Edit: r//'; } | sort -n | tail -1
   ```

3. **產生標示版與正文副本。** 改完在 repo 根目錄跑 `python3 script/doc/mark_changes.py <頁>`（[標示版產生器](../../script/doc/mark_changes.py)）。審閱頁傳頁名，例如 `02_invariants`；本檔要傳路徑 `doc/contract/README.md`，鍵是 `doc_contract_README`。基準有三種：
   - 不帶後綴：[版本號紀錄](../review/versions.json) (`doc/review/versions.json`) 裡這個鍵最後一筆 `replied: true` 的紀錄，也就是維護者最後回覆過的版本；回覆過的內容不再標紅綠，只標之後的改動。沒有這種紀錄就整份標新增。鍵已標成定案時，如果正式檔內容仍與定案版本相同，就不產生送審檔，並刪除仍存在的送審資料夾；如果定案後正式檔又有改動，就以定案版本為基準重新產生，並註明「定案後又有改動，回到待審」。
   - `--base-version <鍵>=<N>`：用版本號紀錄裡這個鍵版本 N 的紀錄當基準，不看 `replied`。

   每筆紀錄有 `v`、`commit`、`replied`，選填 `path`、`csv_path`、`raw_links`；版本號紀錄頂層另有 `finalized`，以鍵為索引記 `{"v": N, "commit": "<sha>"}`：定案版本與該版本紀錄的 commit；那筆送審紀錄有 `path`、`csv_path`、`raw_links` 時一併照抄。沒有任何鍵定案時沒有這個欄位。基準用 `git show <commit>:<路徑>` 取：有 `path`（CSV 看 `csv_path`）就取那個路徑，用於舊的 `_marked/` 副本，副本裡的相對連結比對前改寫回正式檔位置；副本連結沒改寫過（照正式檔位置寫）時帶 `raw_links: true`。沒有 `path` 就取正式檔路徑。
   - `<基準後綴>`（例如 `pre_r101`）：讀本機 `_backup/` 裡這一輪的改前快照當基準。

   產出放在送審資料夾 `doc/review/<鍵>/`，檔名固定、每次產生就覆蓋：`<鍵>.md` 是正文副本，`<鍵>.marked.md` 是標示版（新增用綠底 `<mark>`、刪除（被取代或拿掉的舊文字）用紅底 `<mark>`），有 CSV 的頁再加 `<鍵>.csv`。repo 裡的檔名與檔內都不寫版本號；正式檔名不帶版本號，也不改名，其他文件的連結才不會斷。產生器只讀版本號紀錄，不寫、不取號。

   鍵對審閱頁是頁名，對其他檔是攤平後的路徑，規則見[工具說明](../../script/doc/README.md)。
4. **送審與定案。** 先把正式檔與送審資料夾 commit，再用[打包腳本](../../script/doc/pack_review.py)打包 `doc/review/<鍵>/`，產出 `review_vN.zip`，用 SendUserFile 傳給維護者。版本號只在 zip 裡的檔名（`<鍵>.v<N>.md`、`<鍵>.v<N>.marked.md`、`<鍵>.v<N>.csv`）：看檔名就要知道是哪一版，不用打開才知道。打包腳本送審時把 `{v, commit, replied: false}` 追加進版本號紀錄、zip 編號加一；正式檔有未 commit 的改動，或送審資料夾的副本跟正式檔不一致（沒重跑產生器），就停下不打包。維護者回覆後跑 `python3 script/doc/pack_review.py --replied <鍵>=<N> [...]` 把那筆標成 `replied: true`：只改 `replied`，不打包、不取號，不用 `--out`。維護者明確定案後，跑 `python3 script/doc/pack_review.py --finalized <鍵>=<N> [...]`：版本 N 必須已送審且已回覆，否則整批不處理；成功時記錄定案版本及其 commit，並刪除該鍵的送審資料夾，不打包、不取號，也不用 `--out`；接著把版本號紀錄的改動與資料夾刪除一起 commit。定案版就是正式檔，之後隨 PR merge 進 `main`。

內部文件（本檔、[工作約定](../../AGENTS.md)、[工具說明](../../script/README.md)、[ADR 規則](../adr/README.md) 等，也就是對外文件以外的所有文件）改完照樣走步驟 2 (doc-edit)，但不產標示版、不送審；也不准留過時的資訊。

`doc/review/` 進 git；只有待審頁保留各自的送審資料夾，已定案頁不保留。定案後正式檔若再改動，重新產生送審檔並照步驟 4 打包，會成為新一輪送審。審查與調查的結論寫進 issue 留言；`doc/decisions/review_log/` 與 `doc/research/` 跟 `_backup/` 一樣只在本機、不進 git。

## 怎樣才算定案

只有維護者針對那一頁明確回覆「定案」才算定案，定案之後才 merge 進 `main`。對其他頁的回覆不算，沒有意見也不算。
