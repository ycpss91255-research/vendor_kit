# 03 訊息與錯誤碼總表

> 目前列出 13 條：待審 13

這一頁列出 <ins>VK</ins> 每個結束碼的意思，以及 VK 會印出、要<ins>使用者</ins>動手處理的訊息，目前列出 13 條，都待審。結束碼是契約，依 [02 不變量](02_invariants.md#4-永不靜默失敗) 第 4 條；列出的訊息各有固定編號，其他文件用這個編號引用它。

- 名詞見[名詞表](../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：

| 結束碼 | 意思 |
|---|---|
| `0` | 成功，可能帶<ins>警告</ins> |
| `1` | 做完了，但要人接手：有<ins>合併衝突</ins>要解，或 `update --exit-code` 查到新版 |
| `2` | <ins>失敗</ins>、需要人處理，或用法錯誤。一定印出原因；需要人處理的另附可以直接複製的指令 |
| `3` | 現有<ins>薄殼</ins>、檔案、<ins>引擎</ins>的版本組合不合，要先升級或退回才能繼續。這種情況不動 <ins>repo 檔</ins>與 <ins>VK 檔</ins>，執行紀錄除外 |

一次處理多個工具時只回一個碼：

- 取各結果裡數字最大的那個，沒有特例
- 結束碼只有一個，每個工具的結果仍逐一印出

## 輸出

- 正常結果印到 stdout，含各 recipe 的 `-h`／`--help` 印出的用法
- 錯誤、警告、提示印到 stderr，用法錯誤時印的用法也是；下面[訊息](#訊息)列出的每一條都印到 stderr，格式與前綴見該節
- 顏色照這幾條：
  - 只在那個輸出串流是終端（TTY）時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色（[NO_COLOR](https://no-color.org/)）
  - 給程式讀的輸出永遠不含顏色，例如<ins>執行紀錄</ins>
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

- 「編號」欄只供文件之間互相引用，不會印在訊息裡；編號一旦發出就不重用，刪掉的訊息留空號
- 「類別」欄只分三種：<ins>需人處理</ins>、失敗、警告；完整的結果分類與各自的結束碼見上面的[結束碼](#結束碼)
- 每條訊息都印到 stderr，第一行開頭固定加 `vendor_kit: <類別>: `，`<類別>` 是「類別」欄的值，例如 `vendor_kit: 需人處理: `；多行的訊息整條印在同一個串流
- 警告要指名對象（哪個檔、哪個工具、哪個 image）；能處置就列出下一步
- 「意思」欄只有反引號內是訊息本文，逐字照印；反引號外的文字不印出。`<…>` 是占位符，印出時換成實際的值；占位符怎麼換寫在「時機」欄。多行的訊息寫成「第一行 `…`；第二行 `…`」
- 「下一步」欄是訊息裡可以直接複製來執行的指令；訊息裡沒有指令的標「—」
- 狀態只有兩種：待審（還沒送維護者定案）、定案

| 編號 | 結束碼 | 類別 | 時機 | 意思 | 下一步 | 狀態 |
|---|---|---|---|---|---|---|
| M1 | `2` | 需人處理 | `update`、`upgrade`、`add` 要列出某個<ins>工具</ins>有哪些版本，但沒有給 <ins>registry</ins> 憑證，而那個 registry 要求認證；訊息裡的 `<指令>` 依觸發的指令而定：`add` 時是 `add`，`update`、`upgrade` 時是 `upgrade` | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit <指令> <repo>@<tag>（拉取使用主機 docker 認證）` | `add` 時是 `just vendor_kit add <repo>@<tag>`；`update`、`upgrade` 時是 `just vendor_kit upgrade <repo>@<tag>` | 待審 |
| M2 | `2` | 需人處理 | 操作需要<ins>詢問</ins>，但沒帶 `-y`，又不能互動（沒有終端，或讀到輸入結束）；一律不改；依 [02 不變量](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋) 第 1 條 | `需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：<加上 -y 的原指令>` | `<加上 -y 的原指令>`：由這次執行的參數逐項重組，每一項依 POSIX shell 的規則加引號，`-y` 插在單獨的 `--` 之前；沒有 `--` 時放在最後。不在原指令字串尾端直接接 `-y` | 待審 |
| M3 | `2` | 需人處理 | <ins>CI 模式</ins>下，<ins>基準版</ins>落後<ins>版本鎖定行</ins>（本機不印這條：本機只印警告、結束碼 `0`）；依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條 | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push` | `just vendor_kit upgrade <repo> -y` | 待審 |
| M4 | `3` | 需人處理 | `upgrade --engine=<tag>` 降版，但目標引擎無法無損讀取現有的 VK 檔；除執行紀錄外，在任何寫入之前結束；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 <N> 的版本：just vendor_kit upgrade --engine=<tag>` | `just vendor_kit upgrade --engine=<tag>` | 待審 |
| M5 | `2` | 需人處理 | `sync` 發現某個工具未完成<ins>導入</ins>；本機與 CI 模式都一樣；依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條 | `<repo> 未完成導入，請執行：just vendor_kit add <repo>` | `just vendor_kit add <repo>` | 待審 |
| M6 | `3` | 需人處理 | 引擎讀到的 VK 檔，<ins>檔案版</ins>高於這個引擎支援的上限；除執行紀錄外，在任何寫入之前結束；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請升級引擎：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | 待審 |
| M7 | `2` | 需人處理 | `bootstrap.sh` 發現主機的 just 低於 1.33.0；這項檢查排在建執行紀錄之前，失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印這條；依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條 | 第一行 `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。`；第二行 `下載：<平台對應的下載網址>`；第三行 `安裝：<安裝指令>` | 訊息第三行的 `<安裝指令>`（安裝指令不覆蓋主機既有的 just，也不要求主機另裝其他工具） | 待審 |
| M8 | `2` | 需人處理 | 薄殼的檔跟這一版引擎的模板比對不符：內容被修改過，或不是這一版引擎的模板；訊息裡的 `<files>` 逐檔標出是哪一種；不重產薄殼；除執行紀錄外，不動 repo 檔與其他 VK 檔；依 [02 不變量](02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義) 第 6 條 | `偵測到薄殼跟這一版引擎的模板不符：<files>。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | 待審 |
| M9 | `3` | 需人處理 | 舊的薄殼遇上 X 較新的引擎，執行<ins>救援路徑</ins>以外的 recipe；除執行紀錄外，不動 repo 檔與 VK 檔；救援路徑以外 recipe 的 `-h`／`--help` 在版本組合不合時怎麼反應，本頁不定；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `薄殼介面版 <P_shell> 低於引擎 <vY> 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | 待審 |
| M10 | `2` | 失敗 | 建不出執行紀錄；在任何副作用之前結束，所有 VK recipe 都一樣；依 [02 不變量](02_invariants.md#4-永不靜默失敗) 第 4 條 | `無法寫入執行紀錄 <path>：<原因>。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。` | — | 待審 |
| M11 | `2` | 失敗 | `docker --version` 的輸出含 `podman`；這項檢查排在建執行紀錄之前，失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印這條；依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條 | `偵測到 podman（docker --version）。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。` | — | 待審 |
| M12 | `2` | 失敗 | 啟動器發現主機的 Docker 低於 19.03；這項檢查排在建執行紀錄之前，失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印這條；依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條 | `需要 Docker ≥ 19.03，目前為 <version>。請升級 Docker 後重試。` | — | 待審 |
| M13 | `2` | 失敗 | <ins>metadata</ins> 缺失或損壞，無法可靠還原；不猜測；除執行紀錄外，不寫 repo 檔與其他 VK 檔；依 [02 不變量](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋) 第 1 條 | `無法處理 <file>：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 <file> 與執行紀錄 <path>；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。` | — | 待審 |
