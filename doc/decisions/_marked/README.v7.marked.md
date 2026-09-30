<!-- 標示版 v7：綠底 <mark> 是新增、紅底 <mark> 是刪除；底線 <ins> 是名詞標記；本檔只供本地 review，不進 git；基準是已送審的 v6。正式內容看 /doc/contract/README.md -->

# 審閱頁
<mark style="background-color:#f8c8c8">舊標題：vendor_kit</mark>
<mark style="background-color:#c8f0c8">（標題已修改）</mark>

<mark style="background-color:#f8c8c8">vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個安裝目錄用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</mark>
<mark style="background-color:#c8f0c8">這個目錄放 [VK](../../../GLOSSARY.md#角色與情境) 對外[契約](../../../GLOSSARY.md#介面版與契約)的審閱頁。給第一次來看的人，也給要改這幾頁的 agent。</mark>

## 這個目錄放什麼
<mark style="background-color:#f8c8c8">舊標題：目錄</mark>
<mark style="background-color:#c8f0c8">（標題已修改）</mark>

- <mark style="background-color:#f8c8c8">[開始之前](#開始之前)</mark>
- <mark style="background-color:#f8c8c8">[使用方式](#使用方式)</mark>
- <mark style="background-color:#f8c8c8">[文件](#文件)</mark>
<mark style="background-color:#c8f0c8">一頁一個主題，依序讀：</mark>

<mark style="background-color:#f8c8c8">開始之前</mark>
1. <mark style="background-color:#c8f0c8">[01 目的與承諾](../../contract/01_purpose.md)：為什麼做 VK、對[使用者](../../../GLOSSARY.md#角色與情境)承諾什麼。</mark>
2. <mark style="background-color:#c8f0c8">[02 不變量](../../contract/02_invariants.md)：任何版本都必須成立的性質。</mark>
3. <mark style="background-color:#c8f0c8">[03 訊息與錯誤碼總表](../../contract/03_messages.md)：每個[結束碼](../../../GLOSSARY.md#執行與結果)的意思，與 VK 印出、要使用者動手處理的訊息。</mark>
4. <mark style="background-color:#c8f0c8">[04 使用者介面](../../contract/04_interface.md)：全部 [VK recipe](../../../GLOSSARY.md#vk-recipe-與用途) 與選項。</mark>

<mark style="background-color:#f8c8c8">主機需求</mark>
<mark style="background-color:#c8f0c8">契約放在這裡，不放 issue：issue 不好追蹤改動，也做不了逐頁審與標示版差異。出處：[工作約定](../../../AGENTS.md)「決議與文件流程」。</mark>

<mark style="background-color:#f8c8c8">依 [02 不變量](doc/decisions/review/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條，主機只需要這三個：</mark>
## 寫法規則
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#f8c8c8">[Docker](https://www.docker.com/)</mark>
  - <mark style="background-color:#f8c8c8">19.03 以上</mark>
  - <mark style="background-color:#f8c8c8">不支援 Podman</mark>
- <mark style="background-color:#f8c8c8">[Git](https://git-scm.com/)</mark>
  - <mark style="background-color:#f8c8c8">不設最低版本</mark>
  - <mark style="background-color:#f8c8c8">VK 不呼叫 git</mark>
  - <mark style="background-color:#f8c8c8">「安裝目錄在 git repo 裡」由啟動器用 sh 往上找 `.git` 判斷</mark>
- <mark style="background-color:#f8c8c8">[just](https://github.com/casey/just)</mark>
  - <mark style="background-color:#f8c8c8">1.33.0 以上</mark>
  - <mark style="background-color:#f8c8c8">用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)</mark>
- <mark style="background-color:#c8f0c8">只能向前依賴：頁 N 只能引用前面的頁與[名詞表](../../../GLOSSARY.md)，不引用後面的頁，也不用後面頁才出現的名詞。</mark>
- <mark style="background-color:#c8f0c8">對外頁不寫「出處」。沿用前面頁的規則時，在正文寫「`依 [頁名第 N 條](連結#錨點)`」，連到那一條的標題錨點；不引用 ADR 或 issue。</mark>
- <mark style="background-color:#c8f0c8">以[**名詞表**](../../../GLOSSARY.md)的粗體詞條為準；名詞在每頁正文第一次出現時，連到該名詞所在的名詞表分群標題。同頁後續出現不重複連結。標題、程式碼區塊、行內程式碼與已有連結文字不算正文第一次；名詞先出現在標題時，連結放在標題下第一次出現於正文的位置。</mark>
- <mark style="background-color:#c8f0c8">不用 HTML 標籤標示名詞。錨點一律由標題產生：要連到表格裡的某一列，就連到它所在的標題，連結文字寫出是哪一條，例如「以[結束碼](../../contract/03_messages.md#結束碼) `2` 結束，訊息見[訊息總表](../../contract/03_messages.md#訊息)」。名詞表的名詞沒有個別錨點，連到它所在的分群標題，例如 `[工具](../../GLOSSARY.md#工具與出貨)`。</mark>
- <mark style="background-color:#c8f0c8">規則只寫一次。其他頁要用到，照上面「對外頁不寫出處」那條寫「`依 [頁名第 N 條](…)`」，或連到章節，不重述。</mark>
- <mark style="background-color:#c8f0c8">連結用有名字的超連結，例如 `[不變量](02_invariants.md)`，不要把路徑當連結文字。連結文字不放反引號；程式碼名詞當連結時寫 `[\<repo\>](…)`。</mark>

<mark style="background-color:#f8c8c8">版本不足時：</mark>
## 版本怎麼迭代
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#f8c8c8">Docker 或 just 版本不足，都在任何寫入之前以 `1` 結束</mark>
- <mark style="background-color:#f8c8c8">只有 just 版本不足時，另外印出下載與安裝指令</mark>
<mark style="background-color:#c8f0c8">這一節是對外文件審閱的固定流程，新接手的 agent 照這個順序做。出處：維護者 2026-09-30 定案；[issue #64](https://github.com/ycpss91255-research/vendor_kit/issues/64)。</mark>

<mark style="background-color:#f8c8c8">第一次導入</mark>
1. <mark style="background-color:#c8f0c8">**草稿只改在討論分支。** 對外文件是根目錄 [README](../../../README.md) 與本目錄的審閱頁（目前 01～04）。草稿一律改在討論分支並開 PR，`main` 上只放定案版。定案之後才 merge 進 `main`，定案的條件見下一節。</mark>
2. <mark style="background-color:#c8f0c8">**改動一律跑 [doc-edit workflow](../../../.claude/workflows/doc-edit.js)**。workflow 在第一次修改前自行把原內容備份到 `doc/decisions/_backup/<鍵>.pre_<round>.md`，不用另外手動備份。round 名稱是 `rNN`：取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一（例如最大是 `pre_r100`，round 就是 `r101`），用過的不能重用。doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是最大編號加一，重用或跳號就直接停。目前最大的編號這樣查：</mark>

> <mark style="background-color:#f8c8c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會失敗。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>
   <mark style="background-color:#c8f0c8">```sh</mark>
   <mark style="background-color:#c8f0c8">ls doc/decisions/_backup | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//' | sort -n | tail -1</mark>
   <mark style="background-color:#c8f0c8">```</mark>

<mark style="background-color:#f8c8c8">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡，依 [02 不變量](doc/decisions/review/02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條。</mark>
3. <mark style="background-color:#c8f0c8">**產生標示版與帶版本號的副本。** 改完在 repo 根目錄跑 `python3 script/mark_changes.py <基準後綴> <頁>`（[標示版產生器](../../../script/mark_changes.py)），基準後綴是這一輪的備份後綴，例如 `pre_r101`。審閱頁傳頁名，例如 `02_invariants`；根目錄 README 傳 `README.md`。每跑一次：</mark>
   - <mark style="background-color:#c8f0c8">在 `doc/decisions/_marked/` 產出兩個檔名帶版本號的檔：`<鍵>.vN.marked.md` 是標示版，新增用綠底 `<mark>`、刪除（被取代或拿掉的舊文字）用紅底 `<mark>`；`<鍵>.vN.md` 是同一版的正文副本。產生器會先刪掉同一個鍵的舊版，只留最新一版；每輪把這次刪除與新檔一起 commit。</mark>
   - <mark style="background-color:#c8f0c8">版本號只在 `_marked/` 的檔名：正式檔與正文副本內都不寫版本號。正式檔名不帶版本號，也不改名，其他文件的連結才不會斷。</mark>
   - <mark style="background-color:#c8f0c8">版本號 N 取 [版本號紀錄](../review_log/versions.json)（`doc/decisions/review_log/versions.json`，進 git）裡這個鍵的數字加一並寫回，沒有記錄就是 v1。它跟著 git 走，所以換電腦、新 clone 或清掉 `_marked/` 之後不會從 v1 重來。</mark>

<mark style="background-color:#f8c8c8">```sh</mark>
<mark style="background-color:#f8c8c8">curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh</mark>
<mark style="background-color:#f8c8c8">sh bootstrap.sh</mark>
<mark style="background-color:#f8c8c8">```</mark>
   <mark style="background-color:#c8f0c8">鍵對審閱頁是頁名，對其他檔是攤平後的路徑，規則見[工具說明](../../../script/README.md)。</mark>

<mark style="background-color:#f8c8c8">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載引擎，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>
   <mark style="background-color:#c8f0c8">送審的基準是這一頁上一次送審、維護者已回覆的那一版：用 `python3 script/mark_changes.py --base-version <頁>=<版號>` 產標示版，維護者已經看過並回覆的內容不再標紅綠，只標之後的改動。</mark>
4. <mark style="background-color:#c8f0c8">**送審。** 用 SendUserFile 把 `<鍵>.vN.md` 與 `<鍵>.vN.marked.md` 兩個檔一起傳給維護者。打包用[打包腳本](../../../script/pack_review.py)，檔名 `review_vN.zip`。不傳沒帶版本號的正式檔：看檔名就要知道是哪一版，不用打開才知道。</mark>

<mark style="background-color:#f8c8c8">使用方式</mark>
<mark style="background-color:#c8f0c8">內部文件（本檔、[工作約定](../../../AGENTS.md)、[工具說明](../../../script/README.md)、[ADR 規則](../../adr/README.md) 等，也就是對外文件以外的所有文件）改完照樣走步驟 2 (doc-edit)，但不產標示版、不送審；也不准留過時的資訊。</mark>

<mark style="background-color:#f8c8c8">```</mark>
<mark style="background-color:#f8c8c8">用法：just vendor_kit <指令> [參數] [選項]</mark>
<mark style="background-color:#c8f0c8">`doc/decisions/_marked/` 進 git，每一輪都把標示版與帶版本號的正文副本 commit。定稿那一輪照步驟 3 產生最終版：產生器會刪掉同一個鍵的舊版並產生最終版，把刪除與新檔放在同一個 commit。`doc/decisions/_backup/` 只在本機，不進 git（見[忽略清單](../../../.gitignore)）。</mark>

<mark style="background-color:#f8c8c8">常用指令：</mark>
  <mark style="background-color:#f8c8c8">add <repo>                  把一個工具納入這個安裝目錄</mark>
  <mark style="background-color:#f8c8c8">upgrade <repo>              把鎖定版本換成新版</mark>
  <mark style="background-color:#f8c8c8">upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版</mark>
  <mark style="background-color:#f8c8c8">dev <repo> -p <dir>         讓工具改用本機目錄</mark>
  <mark style="background-color:#f8c8c8">dev --engine -i <image>     讓引擎改用本機 image</mark>
<mark style="background-color:#f8c8c8">```</mark>
## 怎樣才算定案
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#f8c8c8">每個指令都支援 `-h`／`--help`，印出該指令的用法</mark>
- <mark style="background-color:#f8c8c8">進階指令與選項見 [04 使用者介面](doc/decisions/review/04_interface.md)</mark>
- <mark style="background-color:#f8c8c8">結束碼與訊息見 [03 訊息與錯誤碼總表](doc/decisions/review/03_messages.md)</mark>
<mark style="background-color:#f8c8c8">文件</mark>
- <mark style="background-color:#f8c8c8">[01 目的與承諾](doc/decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</mark>
- <mark style="background-color:#f8c8c8">[02 不變量](doc/decisions/review/02_invariants.md)：任何版本都必須成立的規則</mark>
- <mark style="background-color:#f8c8c8">[03 訊息與錯誤碼總表](doc/decisions/review/03_messages.md)：每個結束碼的意思，與要使用者動手處理的訊息</mark>
- <mark style="background-color:#f8c8c8">[04 使用者介面](doc/decisions/review/04_interface.md)：全部指令與選項</mark>
- <mark style="background-color:#f8c8c8">[名詞表](CONTEXT.md)</mark>
- <mark style="background-color:#f8c8c8">[架構決議（ADR）](doc/adr/)</mark>
<mark style="background-color:#f8c8c8">每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。</mark>
<mark style="background-color:#c8f0c8">只有維護者針對那一頁明確回覆「定案」才算定案，定案之後才 merge 進 `main`。對其他頁的回覆不算，沒有意見也不算。</mark>
