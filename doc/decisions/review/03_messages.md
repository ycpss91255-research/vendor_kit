# 03 訊息與錯誤碼總表

> 目前列出 8 條：待審 8；還沒列齊

這一頁列出 <ins>VK</ins> 每個結束碼的意思，以及 VK 會印出、要<ins>使用者</ins>動手處理的訊息，目前待審 8 條；其他有固定編號的訊息還沒列進來。結束碼是契約，依 [02 不變量](02_invariants.md#4-永不靜默失敗) 第 4 條；列出的訊息各有固定編號，其他文件用這個編號引用它。

- 名詞見[名詞表](../../../CONTEXT.md)

## 目錄

- [結束碼](#結束碼)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：

| 結束碼 | 意思 |
|---|---|
| <a id="exit-0"></a>`0` | 成功，可能帶<ins>警告</ins> |
| <a id="exit-1"></a>`1` | <ins>失敗</ins>，或需要人處理。一定印出原因；需要人處理的另附可以直接複製的指令 |
| <a id="exit-2"></a>`2` | 做完了，但要人接手：有<ins>合併衝突</ins>要解，或 `update --exit-code` 查到新版 |
| <a id="exit-3"></a>`3` | 現有<ins>薄殼</ins>、檔案、<ins>引擎</ins>的版本組合不合，要先升級或退回才能繼續。這種情況不動 <ins>repo 檔</ins>與 <ins>VK 檔</ins>，執行紀錄除外 |

一次處理多個工具時只回一個碼，回最需要處理的那個：

- `1` 優先於 `2`
- `2` 優先於 `0`
- `update` 同時遇到查詢失敗與有新版時回 `1`
- 只回一個碼，但每個工具的結果都照樣印出，不因此省略

## 訊息

- 類別用名詞表裡的三種結果：<ins>需人處理</ins>、失敗、警告
- 警告要指名對象（哪個檔、哪個工具、哪個 image）；有辦法處置就列出下一步
- 「意思」欄是訊息本文，逐字照印；`<…>` 是占位符，印出時換成實際的值
- 「下一步」欄是訊息裡可以直接複製來執行的指令；訊息裡沒有指令的標「—」
- 狀態只有兩種：待審（還沒送維護者定案）、定案

| 編號 | 結束碼 | 類別 | 時機 | 意思 | 下一步 | 狀態 |
|---|---|---|---|---|---|---|
| <a id="msg-6-3"></a>6-3 | `1` | 需人處理 | `update`、`upgrade`、`add` 要列出某個<ins>工具</ins>有哪些版本，但沒有給 <ins>registry</ins> 憑證，而那個 registry 要求認證 | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）` | `just vendor_kit upgrade <repo>@<tag>` | 待審 |
| <a id="msg-6-5"></a>6-5 | `1` | 需人處理 | <ins>CI 模式</ins>下，<ins>基準版</ins>落後<ins>版本鎖定行</ins>（本機不印這條：本機只印警告、結束碼 `0`）；依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條 | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push` | `just vendor_kit upgrade <repo> -y` | 待審 |
| <a id="msg-6-10"></a>6-10 | `3` | 需人處理 | `upgrade <repo>@<tag>` 或 `upgrade --engine@<tag>` 降版，但目標引擎無法無損讀取現有的 VK 檔；在任何寫入之前結束；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。未修改任何檔。請改指定能讀取檔案版 <N> 的版本：just vendor_kit upgrade <對象>@<tag>` | `just vendor_kit upgrade <對象>@<tag>`（`<對象>` 是這次降版的 `<repo>` 或 `--engine`） | 待審 |
| <a id="msg-6-13"></a>6-13 | `1` | 需人處理 | `sync` 發現某個工具未完成<ins>導入</ins>；本機與 CI 模式都一樣；依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條 | `<repo> 未完成導入，請執行：just vendor_kit add <repo>` | `just vendor_kit add <repo>` | 待審 |
| <a id="msg-6-19"></a>6-19 | `3` | 需人處理 | 引擎讀到的 VK 檔，<ins>檔案版</ins>高於這個引擎支援的上限；在任何寫入之前結束；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請升級引擎：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | 待審 |
| <a id="msg-6-23"></a>6-23 | `1` | 需人處理 | `bootstrap.sh` 發現主機的 just 低於 1.33.0；在任何寫入之前結束；依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條 | `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。`<br>`下載：<平台對應的下載網址>`<br>`安裝：<安裝指令>`<br>（安裝指令不覆蓋主機既有的 just，也不要求主機另裝其他工具） | 訊息第三行的 `<安裝指令>` | 待審 |
| <a id="msg-6-36"></a>6-36 | `3` | 需人處理 | 舊的薄殼遇上 X 較新的引擎，執行<ins>救援路徑</ins>以外的 recipe（含其他 recipe 的 `-h`／`--help`）；不動 repo 檔與 VK 檔；依 [02 不變量](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告) 第 10 條 | `薄殼介面版 <P_shell> 低於引擎 <vY> 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | 待審 |
| <a id="msg-6-39"></a>6-39 | `1` | 失敗 | `docker --version` 的輸出含 `podman`；在任何寫入之前結束；依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條 | `偵測到 podman（docker --version）。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。` | — | 待審 |
