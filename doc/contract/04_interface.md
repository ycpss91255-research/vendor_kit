# 04 使用者介面

[使用者](../../GLOSSARY.md#角色與情境)與自動化都透過 `just vendor_kit` 指令跟 [VK](../../GLOSSARY.md#角色與情境) 打交道；只有首次[導入](../../GLOSSARY.md#角色與情境)，以及[薄殼](../../GLOSSARY.md#vk-組件)的檢查與明確要求的修復，用 `sh bootstrap.sh`。這一頁列出全部指令與必要的參數、選項：少了就不能用、或會影響相容性的才列；其他選項的細節實作時再定。VK 不讀取環境變數 `CI`；同一個 recipe 不論在哪裡執行，行為都一樣。

- 必須永遠成立的規則以 [02 不變量](02_invariants.md) 為準，這一頁只補使用者看得到的介面行為
- [結束碼](../../GLOSSARY.md#執行與結果)的意思與每條訊息見 [03 輸出](03_output.md)
- 名詞見[名詞表](../../GLOSSARY.md)

## 目錄

- [主機需求](#主機需求)
- [registry 與認證](#registry-與認證)
- [入口](#入口)
- [bootstrap.sh](#bootstrapsh)
- [指令](#指令)
- [共同選項](#共同選項)
- [各指令專用選項](#各指令專用選項)
- [追蹤新版](#追蹤新版)
- [輸出](#輸出)
- [使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
- [檢查 (test)](#檢查-test)

## 主機需求

依 [02 不變量第 5 條](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)，支援平台本來就有的這些不算在主機依賴內：

- POSIX sh 與它的內建指令
- 基礎 userland：`grep`、`sed`、`id`、`mktemp`、`mkdir`、`date`、`rm`、`sleep`、`od`、`tr`

除此之外，主機只需要這三個：

| 主機程式 | 最低版本 | 說明 | 版本不足時 |
|---|---|---|---|
| [Docker](https://www.docker.com/) | 19.03 以上 | 不支援 Podman；偵測到 Podman 時由[啟動器](../../GLOSSARY.md#vk-組件)以[結束碼](03_output.md#結束碼) `2` 結束，訊息見 [訊息](03_output.csv) `VK0011` | 由啟動器檢查，首次導入與已有[安裝目錄](../../GLOSSARY.md#工具與出貨)都一樣：在任何寫入之前以[結束碼](03_output.md#結束碼) `2` 結束，訊息見 [訊息](03_output.csv) `VK0012` |
| [Git](https://git-scm.com/) | 不設最低版本 | VK 不在主機上呼叫 git；「安裝目錄在 git [repo](../../GLOSSARY.md#工具與出貨) 裡」由啟動器用 sh 往上找 `.git` 判斷；`.git` 是目錄或檔都算，所以 worktree 與 submodule 也適用 | — |
| [just](https://github.com/casey/just) | 1.33.0 以上 | 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest) | 首次導入：`bootstrap.sh` 以[結束碼](03_output.md#結束碼) `2` 結束，訊息見 [訊息](03_output.csv) `VK0005`。已有安裝目錄：由 just 自己報錯，見下方的註 |

註：just 版本不足時

- 首次導入：`bootstrap.sh` 在任何寫入之前以[結束碼](03_output.md#結束碼) `2` 結束，另印下載與安裝指令，訊息見 [訊息](03_output.csv) `VK0005`
- 已有安裝目錄：justfile 用了 just 1.33.0 才支援的寫法，just 太舊時讀 justfile 就會出錯，輪不到 VK 執行，也就沒機會檢查版本；這時看到的是 just 自己的錯誤訊息與結束碼，VK 不留[執行紀錄](../../GLOSSARY.md#repo-內的檔與狀態)

## registry 與認證

依 [02 不變量第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git)，認證由主機與 CI 各自處理：在支援的 [registry](../../GLOSSARY.md#工具與出貨) 上，主機的 docker 拉得到的 image，VK 就用得了。

- 支援的 registry 目前只有 GitHub 的 image 伺服器 (GHCR)。沒列在這份清單上的 registry（例如 Docker Hub、GitLab、自架）不在承諾內
- [引擎 image](../../GLOSSARY.md#工具與出貨) 公開；[工具 image](../../GLOSSARY.md#工具與出貨) 公開或私有，由[出貨](../../GLOSSARY.md#角色與情境)那個 repo 自己決定
- 沒有給憑證時，不支援需要認證的版本列舉：對那個工具以[結束碼](03_output.md#結束碼) `2` 結束，印出兩條路，訊息見 [訊息](03_output.csv) `VK0001`
  - 設定 `VENDOR_KIT_REGISTRY_TOKEN`（或 `VENDOR_KIT_REGISTRY_TOKEN_FILE`）
  - 直接指定版本 `@<tag>`

## 入口

VK 對外只有兩個入口：

- `sh bootstrap.sh`
  - 首次導入、檢查與修復薄殼，見下方的 [bootstrap.sh](#bootstrapsh)
  - 先從 [VK 的 Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)下載，再到要裝 VK 或已有 VK 的目錄執行
  - 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，Release 頁上目前還沒有這個檔
- `just vendor_kit …`
  - 日常使用的全部指令；CI 也用它，見下面的[檢查 (test)](#檢查-test)
  - 都收在 `vendor_kit` 這個命名空間底下，不佔用 [repo](../../GLOSSARY.md#工具與出貨) 自己的頂層指令名

## bootstrap.sh

`bootstrap.sh` 是啟動器之一；首次導入時取得內嵌那一版[引擎](../../GLOSSARY.md#vk-組件)，再呼叫 `install`（把 VK 裝進目前目錄）。在既有安裝目錄則依[版本鎖定行](../../GLOSSARY.md#版本與來源)指定的引擎模板，檢查或重產薄殼。它不執行 repo 內的薄殼，也不從薄殼讀取版本或模板；薄殼內容只用於逐檔比對。

```text
用法：sh bootstrap.sh [選項]

  （不帶參數）         尚非安裝目錄或未完成的首次導入：首次導入；其他安裝目錄：只檢查薄殼
  -i, --image <image>   使用本機 image 或 image tar 作為引擎來源
  --repair             用鎖定引擎的模板重產薄殼
  -y, --yes            首次導入時傳給 install，代替原本允許的詢問
  -h, --help           單獨使用時印出用法
```

不收位置參數，也沒有 `--version`。短長選項意思相同，選項順序不限；`--repair` 只有長選項。`-h`／`--help` 只准單獨使用，不印內嵌引擎版本；與任何其他參數並用都算用法錯誤。

目前目錄有 `.vendor_kit/` 就是安裝目錄；沒有才首次導入。有 `.vendor_kit/` 卻讀不出恰好一行有效的引擎版本鎖定行時，停下報 `VK0037`，不猜版本，也不改走首次導入；唯一例外是未完成的首次導入：這個安裝目錄最近一筆執行紀錄是首次導入、停在 `VK0002`，且除執行紀錄外未修改任何檔；或最近一筆執行紀錄是首次導入，且在建紀錄之後、寫入引擎版本鎖定行之前就結束（不論是否已寫入其他檔）。符合例外時仍按首次導入處理，允許帶 `-y` 重跑；讀得出恰好一行有效的引擎版本鎖定行時，一律是既有安裝目錄，不套用例外。判定靠執行紀錄，不靠 `.vendor_kit/` 裡有哪些檔；啟動器只用字串相等比對最近一筆執行紀錄裡固定記下的欄位：模式是首次導入，且原因代碼是 `VK0002`、除執行紀錄外未修改任何檔，或結束階段在建紀錄之後、寫入引擎版本鎖定行之前。比對不出來或紀錄不足以唯一判定時，不套用例外。在這個未完成狀態下，用法錯誤或帶 `--repair` 而中途結束的執行不建紀錄，不改變例外判定所用的最近一筆執行紀錄。

既有安裝目錄的檢查與修復一律使用版本鎖定行那一版引擎，不套用[本機覆寫](../../GLOSSARY.md#版本與來源)：`bootstrap.sh` 是在 VK 本身可能壞掉時用的入口，以進 git 的鎖定行為準。`-i` 跟首次導入一樣接受已載入的本機 image 或 image tar；兩者都必須符合引擎版本鎖定行的 [digest](../../GLOSSARY.md#工具與出貨)，缺少必要的 digest 資訊或 digest 不符時報 `VK0031`。以 [image 引用](../../GLOSSARY.md#工具與出貨)指定時，完整引用也必須與鎖定行相同，引用不符但 digest 相符時報 `VK0038`。

`bootstrap.sh` 只保證跟同 X 的鎖定引擎一起用；內嵌引擎與版本鎖定行指定的引擎跨 X 時，在任何寫入之前停下（包括不建執行紀錄），報版本組合不合，以結束碼 `3` 結束，訊息說明要換成與鎖定引擎同 X 的 `bootstrap.sh`。

### 依情況的行為

表中的[原因代碼](../../GLOSSARY.md#執行與結果)見 [03 訊息](03_output.csv)；表中的[診斷](../../GLOSSARY.md#執行與結果)除跨 X 為 `fatal`、結束碼 `3` 外，都是 `error`、結束碼 `2`，印到 stderr，stdout 不印診斷；處置只有[待處理](../../GLOSSARY.md#執行與結果)、[失敗](../../GLOSSARY.md#執行與結果)或留空，用法錯誤的處置留空，見[訊息表](03_output.csv)。成功的用法、差異與結果印到 stdout，不加診斷前綴。

| 情況 | 行為 | 結束碼 | 原因代碼 | stdout／stderr |
|---|---|---|---|---|
| 單獨帶 `-h`／`--help` | 只印用法，不做主機檢查、不寫檔 | `0` | — | stdout：用法 |
| 不認得的選項、多出位置參數，或 `-h`／`--help` 與其他參數並用 | 用法錯誤，不寫檔 | `2` | `VK0026` | stderr：診斷與簡短用法 |
| `-i`／`--image` 缺值 | 用法錯誤，不寫檔 | `2` | `VK0025` | stderr：診斷與簡短用法 |
| 既有安裝目錄帶 `-y`／`--yes`（上述未完成的首次導入例外除外），或任何情況帶 `--repair -y` | 用法錯誤，不寫檔 | `2` | `VK0026` | stderr：診斷與簡短用法 |
| 找不到 docker | 主機前置檢查失敗 | `2` | `VK0033` | stderr：診斷 |
| 偵測到 Podman | 主機前置檢查失敗 | `2` | `VK0011` | stderr：診斷 |
| Docker 低於 19.03 | 主機前置檢查失敗 | `2` | `VK0012` | stderr：診斷 |
| 首次導入找不到 just | 主機前置檢查失敗，附下載與安裝指令 | `2` | `VK0034` | stderr：診斷與下載、安裝指令 |
| 首次導入 just 低於 1.33.0 | 主機前置檢查失敗，附下載與安裝指令 | `2` | `VK0005` | stderr：診斷與下載、安裝指令 |
| 往上找不到 `.git` | 不寫檔，也不建立 repo | `2` | `VK0035` | stderr：診斷 |
| 非安裝目錄帶 `--repair` | 停下，不改走首次導入、不建紀錄、不寫檔 | `2` | `VK0039` | stderr：診斷 |
| 有 `.vendor_kit/`，但讀不出恰好一行有效的引擎版本鎖定行，且不屬上述未完成的首次導入例外；帶 `--repair` 時即使符合例外也同樣處理 | 停下，不改走首次導入、不建紀錄、不寫檔 | `2` | `VK0037` | stderr：診斷 |
| 鎖定引擎與 `bootstrap.sh` 內嵌引擎跨 X | 任何寫入之前停下，指出要換哪個 X 的 `bootstrap.sh` | `3` | `VK0040` | stderr：診斷 |
| 既有安裝目錄帶 `-i`，本機 image 或 image tar 缺必要的 digest 資訊，或 digest 與鎖定行不符 | 停下，不用這個 image | `2` | `VK0031` | stderr：診斷 |
| 既有安裝目錄以 [image 引用](../../GLOSSARY.md#工具與出貨)帶 `-i`，digest 相符但完整 image 引用與鎖定行不同 | 停下，不用這個 image | `2` | `VK0038` | stderr：診斷 |
| 首次導入、只檢查或 `--repair`，建不出執行紀錄 | 停下，不拉 image、不寫檔 | `2` | `VK0010` | stderr：診斷 |
| 取不到要用的引擎 image | 停下，不改用其他版本 | `2` | `VK0036` | stderr：診斷 |
| 首次導入帶 `-i`，缺必要的 digest 資訊 | 停下，不退化成只寫 [tag](../../GLOSSARY.md#工具與出貨) | `2` | `VK0031` | stderr：診斷 |
| 首次導入，上層或下層已有安裝目錄 | 拒絕巢狀安裝，不寫檔 | `2` | `VK0029` | stderr：診斷 |
| 首次導入需要詢問，沒帶 `-y` 且不能互動 | 除執行紀錄外不修改；依紀錄按未完成的首次導入處理，允許帶 `-y` 重跑 | `2` | `VK0002` | stderr：診斷與加上 `-y` 的原指令 |
| 首次導入，其餘情況 | 取得內嵌那版引擎並呼叫 `install` | 照 `install` | 照 `install` | 照 `install` |
| 只檢查或 `--repair`，發現升引擎未完成的[進度檔](../../GLOSSARY.md#repo-內的檔與狀態) | 停下，不報薄殼不符、不重產；下一步是重跑原本的 `upgrade` 指令，保留原 [tag](../../GLOSSARY.md#工具與出貨) 與 `-y` | `2` | `VK0023` | stderr：診斷與完整原指令 |
| 既有安裝目錄，不帶 `--repair`，薄殼一致 | 只檢查 | `0` | — | stdout：一致 |
| 既有安裝目錄，不帶 `--repair`，薄殼被改過或與模板不符 | 停下，不重產 | `2` | `VK0006` | stderr：診斷與逐檔差異續行 |
| `--repair`，薄殼一致 | 不重產 | `0` | — | stdout：已一致，未重產 |
| `--repair`，薄殼不符 | 不詢問；寫入前逐檔列差異，再重產並報告結果 | `0` | — | stdout：差異與完成報告 |

先判定目前目錄是否有 `.vendor_kit/`；有且讀不出恰好一行有效的引擎版本鎖定行時，才依最近一筆既有執行紀錄辨識上述未完成的首次導入例外，以判定是否接受 `-y`；再判用法、做主機前置檢查。往上找 `.git`、首次導入的巢狀檢查、非安裝目錄帶 `--repair` (`VK0039`)，以及上述未完成狀態帶 `--repair` (`VK0037`)，都在建紀錄之前判定，拒絕時不建紀錄、不寫檔。既有安裝目錄在建執行紀錄或取得 image 之前先檢查是否跨 X；只檢查與 `--repair` 都在比對薄殼之前辨識升引擎未完成的進度檔，若有則依表中行為停下，不進入後續薄殼檢查或重產。首次導入、只檢查與修復都檢查 docker；just 只在首次導入檢查，另外兩種模式不經過 just。VK 不在主機呼叫 git，只用 sh 往上找 `.git`；它是目錄或檔都算。

### 寫入範圍與其他指令的關係

- 首次導入的寫入範圍、詢問與輸出照 `install`，見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)。`-y` 只在首次導入傳給 `install`，語意照[共同選項](#共同選項)
- 首次導入、只檢查與 `--repair` 都先建執行紀錄，再拉 image、起引擎；首次導入在呼叫 `install` 之前就建好紀錄，只檢查與修復則在比對前建好。建不出紀錄時報 `VK0010`，不拉 image、不寫檔。用法錯誤、主機前置檢查失敗、跨 X、往上找不到 `.git` (`VK0035`)、拒絕巢狀 (`VK0029`)、非安裝目錄帶 `--repair` (`VK0039`)，以及有 `.vendor_kit/` 卻讀不出有效鎖定行且不套用例外（含上述未完成狀態帶 `--repair`，`VK0037`），都在建紀錄之前判定，不建紀錄、不寫檔。執行紀錄規則見 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)
- `sh bootstrap.sh --repair` 是使用者明確打的指令，寫入薄殼檔符合 [02 不變量第 3 條](02_invariants.md#3-自動化不寫追蹤檔)「使用者明確打的 recipe 才寫得到」的意思。只檢查除執行紀錄外不寫檔。`--repair` 除執行紀錄外只重產 `.vendor_kit/` 下的四檔：`entry.just`、`vendor.just`、`log.sh`、`.gitignore`；已一致則不重產
- 檢查與修復不改版本鎖定行或其他檔，包括 VK 的設定檔、[metadata](../../GLOSSARY.md#初始檔與合併)、[基準版](../../GLOSSARY.md#初始檔與合併)、[納管](../../GLOSSARY.md#初始檔與合併)紀錄、[印記](../../GLOSSARY.md#repo-內的檔與狀態)、[cache/](../../GLOSSARY.md#repo-內的檔與狀態)、[gen/](../../GLOSSARY.md#repo-內的檔與狀態)、[本機覆寫](../../GLOSSARY.md#版本與來源)、[進度檔](../../GLOSSARY.md#repo-內的檔與狀態)、根 `justfile`、根 `.dockerignore`、使用者檔與 `bootstrap.sh` 本身
- `--repair` 不經過 `install`，不建立安裝目錄，也不補做其他安裝步驟；它只恢復鎖定引擎的薄殼，不更換引擎版本
- 首次導入的 `-i <image>` 照[離線導入共通規則](#各指令專用選項)；既有安裝目錄的本機 image 或 image tar 須符合上面的 digest 與引用規則，再照原本的檢查或修復行為執行
- [救援路徑](../../GLOSSARY.md#介面版與契約)分兩類：版本組合不合時用[說明與用法錯誤](#說明與用法錯誤)列出的 just 呼叫；薄殼被改過時用 `sh bootstrap.sh` 檢查、`sh bootstrap.sh --repair` 修復

## 指令

```
用法：just vendor_kit <指令> [參數] [選項]

常用指令：
  add <repo>                  把一個工具納入這個安裝目錄
  add <repo>@<tag>            導入指定版本，不必列出版本
  upgrade <repo>              把鎖定版本換成新版
  upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版
  dev <repo> -p <dir>         讓工具改用本機目錄
  dev --engine -i <image>     讓引擎改用本機 image

進階指令：
  remove <repo>               把一個工具解除。初始檔不刪，只收回當初插入的行
  undev <repo>                回到鎖定版本
  undev --engine              回到鎖定的引擎版本
  upgrade --engine            升引擎
  upgrade --engine=<tag>      換成指定版本的引擎
  update                      只查有沒有新版，不改任何檔
  sync                        使本機的工具內容與版本鎖定行或本機覆寫一致；每次跑工具 recipe 都會自動先跑它
  install                     把 VK 裝進 repo 的一個目錄，使它成為安裝目錄
  uninstall                   把 VK 從那個目錄移除。初始檔不刪
  prune                       清掉 VK 產生、但已不再使用的本機資源
  test                        跑全部檢查；本機與 CI 用同一個
  test dist                   只檢查工具交付的內容
```

清單裡的名詞見名詞表：

- [工具](../../GLOSSARY.md#工具與出貨)
- [\<repo\>](../../GLOSSARY.md#工具與出貨)
- [安裝目錄](../../GLOSSARY.md#工具與出貨)
- [鎖定版本](../../GLOSSARY.md#版本與來源)
- [版本鎖定行](../../GLOSSARY.md#版本與來源)
- [tag](../../GLOSSARY.md#工具與出貨)
- [工具內容](../../GLOSSARY.md#工具與出貨)
- [工具 recipe](../../GLOSSARY.md#工具與出貨)

### 執行位置

依 [02 不變量第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git)：

- [VK recipe](../../GLOSSARY.md#執行與結果) 只准在安裝目錄執行；在別處執行就印出 [訊息](03_output.csv) `VK0028` [診斷](../../GLOSSARY.md#執行與結果)，以[結束碼](03_output.md#結束碼) `2` 拒絕，並印出該切到哪裡。[唯讀 recipe](../../GLOSSARY.md#執行與結果) 也沒有例外
- 工具 recipe 自動觸發的 `sync` 會先回到安裝目錄再呼叫，所以不受影響；工具自己的 recipe 要不要擋，由那個工具決定
- `install` 時上層或下層已經有安裝目錄，就印出 [訊息](03_output.csv) `VK0029` 診斷，以[結束碼](03_output.md#結束碼) `2` 拒絕：安裝目錄不能巢狀

### 命名空間

- 一個工具可以提供多個 [\<ns\> 命名空間](../../GLOSSARY.md#工具與出貨)
- `add` 時 `<ns>` 撞名就印出 [訊息](03_output.csv) `VK0030` 診斷，以[結束碼](03_output.md#結束碼) `2` 拒絕，而且在任何寫入之前檢查。比對的對象是：
  - 其他已裝進 repo 的工具
  - 根 `justfile` 既有的 recipe 或 module
  - 保留名 `vendor_kit`

### 說明與用法錯誤

依 [02 不變量第 8 條](02_invariants.md#8-使用者介面不可取代寫法一致)：

- 各指令都有 `-h`／`--help`：把該指令的用法印到 stdout，以[結束碼](03_output.md#結束碼) `0` 結束；沒有 `help` 指令。只有救援路徑中的 just 呼叫在[薄殼](../../GLOSSARY.md#vk-組件)、[VK 檔](../../GLOSSARY.md#repo-內的檔與狀態)與引擎的版本組合不相符時仍可用，也就是 `install`、`upgrade --engine`、`sync` 的不符判定，以及四種印用法的呼叫：`just vendor_kit`（不帶指令）、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項 `--help` 同）；這些呼叫照各自原本的行為執行。薄殼被改過時的檢查與修復見 [bootstrap.sh](#bootstrapsh)。版本組合不相符時，救援路徑以外的呼叫即使帶 `-h`／`--help`，也以結束碼 `3` 結束：stderr 印出 `fatal` 診斷並附救援指令，stdout 不印用法
- 只打 `just vendor_kit`、不帶指令是用法錯誤，stderr 依序印版本行、[訊息](03_output.csv) `VK0024` 診斷與簡短用法，以[結束碼](03_output.md#結束碼) `2` 結束：

  ```text
  $ just vendor_kit
  stderr: vendor_kit <版本>
  stderr: vendor_kit: error[VK0024]: No command was specified.
  stderr: 用法：just vendor_kit <指令> [參數] [選項]
  exit code: 2
  ```

- `vendor_kit` 後面接的不是 [VK recipe](../../GLOSSARY.md#執行與結果) 名稱，或直接接 `-h`、`--version`，例如 `just vendor_kit foo`、`just vendor_kit -h`，都會被 just 當成 recipe 名稱去找，參數到不了 VK，不在 VK 的承諾內。這時由 just 自己印出不帶 `vendor_kit:` 前綴的錯誤訊息，以結束碼 `1` 結束；只承諾訊息來自 just 與結束碼是 `1`，不承諾訊息原文。以下是 just 1.33.0 的輸出；原文會隨 just 版本改變：

  ```text
  $ just vendor_kit foo
  stderr: error: Justfile does not contain recipe `vendor_kit foo`.
  exit code: 1
  ```

  這個 `1` 是 just 回的，不是 VK 回的，因此不表示 VK 的 `warn`，也不和 [03 的結束碼規則](03_output.md#結束碼)衝突。
- 不支援 just 的 `--allow-missing` 或 `JUST_ALLOW_MISSING`；它們會讓不認得的 recipe 靜默以 `0` 成功，違反 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)
- 用法錯誤：先在 stderr 印出 `error` [診斷](../../GLOSSARY.md#執行與結果)，再接著印簡短用法，以[結束碼](03_output.md#結束碼) `2` 結束。算用法錯誤的有：
  - 缺必要參數：[訊息](03_output.csv) `VK0025`
  - VK recipe 帶了不認得的選項或多出的參數：[訊息](03_output.csv) `VK0026`
  - tag 格式不合：[訊息](03_output.csv) `VK0027`，見下面的[指定版本](#指定版本)

  ```text
  $ just vendor_kit add
  stderr: vendor_kit: error[VK0025]: Required argument is missing: <repo>.
  stderr: 用法：just vendor_kit <指令> [參數] [選項]
  exit code: 2

  $ just vendor_kit sync --bogus
  stderr: vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --bogus.
  stderr: 用法：just vendor_kit <指令> [參數] [選項]
  exit code: 2

  $ just vendor_kit upgrade base@1.2.0
  stderr: vendor_kit: error[VK0027]: Invalid tag format: 1.2.0. Use vX.Y.Z with no leading zeros in X, Y, or Z.
  stderr: 用法：just vendor_kit <指令> [參數] [選項]
  exit code: 2
  ```

- 位置參數只放工具名稱 `<repo>`；其他值都經由選項帶入，例如 `-p <dir>`、`-i <image>`
- 同一個概念一種寫法：對象是引擎一律寫 `--engine`，本機 image 一律寫 `-i <image>`
- 選項的寫法：
  - 有短也有長：`-h`／`--help`、`-y`／`--yes`、`-i`／`--image`、`-p`／`--path`
  - 只有長：`--engine`、`--exit-code`
  - 選項放在位置參數之前或之後都可以，意思相同
  - 單獨的 `--` 結束選項：它之後的參數一律當位置參數，以 `-` 開頭也一樣，例如 `just vendor_kit add -- <repo>`
- `--engine` 是值可帶可不帶的長選項：不帶值時只表示對象是引擎；要帶值只接受 `=` 形式 `--engine=<tag>`，不接受 `--engine <tag>`，例如 `--engine=v1.2.0`。工具的指定版本維持 `<repo>@<tag>`

### 指定版本

`<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../GLOSSARY.md#工具與出貨) 照同一套規則：

```text
接受：
just vendor_kit upgrade <repo>@v1.2.0
just vendor_kit upgrade --engine=v1.2.0

不接受：
just vendor_kit upgrade --engine v1.2.0    值沒有用 = 接在 --engine 後面
just vendor_kit upgrade <repo>@1.2.0       少了 v
just vendor_kit upgrade <repo>@v01.2.0     有前導零
```

- 工具與引擎的 tag 只接受 `vX.Y.Z`，不帶 pre-release、build 後綴，不收前導零
- 最新版是把 X、Y、Z 當非負整數逐欄比數值，取最大的那個，不看字串順序、registry 回傳順序或推送時間；同一個 tag 改指到別的 [digest](../../GLOSSARY.md#工具與出貨) 不算新版
- 寫出格式不合的 tag 是用法錯誤，印出 [訊息](03_output.csv) `VK0027` 診斷，以[結束碼](03_output.md#結束碼) `2` 結束
- `upgrade --engine=<tag>` 指定舊版引擎，而目標引擎無法無損讀取現有 VK 檔時，才用 [訊息](03_output.csv) `VK0007`：`fatal`、結束碼 `3`，這次降版失敗
- `upgrade <repo>@<tag>` 指定舊版工具不做上述引擎相容性判定，也不另設工具降版專用的原因代碼；正常完成時以結束碼 `0` 結束，出錯時依實際原因使用一般訊息與結束碼
- 不加 `init`、`ensure`、`diff`、`accept`、`rollback` 這類別名，也不加 `--purge`（VK 永不刪 [repo 檔](../../GLOSSARY.md#repo-內的檔與狀態)，這個選項沒有對象）。這些用途各自由既有指令的選項或 git 處理
- 工具 repo 的命名空間也照這套寫法，例如 base ([base#1192](https://github.com/ycpss91255-docker/base/issues/1192))

### 成對與無害

- 做得了就反得回：`add` 與 `remove`、`dev` 與 `undev`、`install` 與 `uninstall` 成對。
- 查與套用分開：
  - `update` 只查
  - 真正換版本的是 `upgrade`：裝新版工具內容、做[初始檔](../../GLOSSARY.md#初始檔與合併)的[基準版合併](../../GLOSSARY.md#初始檔與合併)、更新[基準版](../../GLOSSARY.md#初始檔與合併)與[納管](../../GLOSSARY.md#初始檔與合併)紀錄，必要時重產薄殼，最後才寫版本鎖定行
- 沒有反向的 `sync`、`prune` 必須無害：
  - 不改任何[追蹤檔](../../GLOSSARY.md#repo-內的檔與狀態)
  - `prune` 只清本機資源與自己的暫存

### 本機覆寫

`dev` 是使用者明確選擇的具名行為。開著[本機覆寫](../../GLOSSARY.md#版本與來源)時，除 `test` 外的一般 recipe 照常執行；若沒有其他診斷，就以[結束碼](03_output.md#結束碼) `0` 結束。每次執行都要在 stdout 印出用了哪一個本機覆寫，不加診斷前綴。`test` 對本機覆寫的處置見下方的[檢查](#檢查-test)。

## 共同選項

`-y` 只適用於[可寫 recipe](../../GLOSSARY.md#執行與結果)。這一節只定它的語意，不承諾每個可寫 recipe 都接受。已定的組合是 `upgrade <repo> -y` 與 `install -y`；首次導入由 [bootstrap.sh](#bootstrapsh) 傳入。其餘哪個指令接受 `-y`，實作時再定。

- [-y](../../GLOSSARY.md#執行與結果)：可代替原本允許的[詢問](../../GLOSSARY.md#執行與結果)
  - 照樣把改了什麼印到 stdout，不加前綴
  - 只省略詢問，不授權覆蓋使用者既有的檔，依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)
  - 不能把已存在、尚未納管的檔改成 append 納管，見下面的[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)

沒帶 `-y`、又不能互動時（例如在腳本裡），需要詢問的操作：

- 一律不改
- 以[結束碼](03_output.md#結束碼) `2` 結束
- 印出該打的指令，訊息見 [訊息](03_output.csv) `VK0002`
- 讀到輸入結束 (EOF) 不算同意

能互動時，詢問文字印到 stderr，不帶[嚴重度](../../GLOSSARY.md#執行與結果)前綴。使用者明確回答「否」是正常取消：不修改，並在 stdout 說明未變更，以[結束碼](03_output.md#結束碼) `0` 結束。

## 各指令專用選項

- `upgrade --engine` 分兩段執行：第一段換上目標引擎後，若原指令尚未做完，就印出 [訊息](03_output.csv) `VK0023` 的 `error` 診斷，以[結束碼](03_output.md#結束碼) `2` 結束。診斷的 `next_step` 是重跑原指令；原指令在訊息定義中以占位符表示，實際輸出由 VK 填成完整、不需使用者代換的指令，保留原來的 tag 與 `-y`。照它重跑就會接著完成第二段
- `sync` 的判定分階段：
  - 主機前置檢查照共同規則先判
  - 安裝目錄層的零寫入阻擋要在逐工具處理前全部判完：薄殼不符用 [訊息](03_output.csv) `VK0006`，版本組合不合用 `VK0008`；任一成立就不取件，兩者同時成立就兩條都印，結束碼取最大值
  - 沒有安裝目錄層的零寫入阻擋，才逐工具處理。`VK0004`、`VK0013` 只擋各自所屬的工具，其他工具照常同步；`VK0014`、`VK0015` 全部判、全部印
  - 整次執行的結束碼取所有安全判出結果的最大值；同一階段內的判定次序與印出順序不承諾
- `update`：查詢結果印到 stdout，不加前綴；不帶 `--exit-code` 時，查到新版仍以[結束碼](03_output.md#結束碼) `0` 結束。
- `update --exit-code`：給 CI 或腳本判斷有沒有新版；查到新版時 stdout 照樣印查詢結果，stderr 另印 [訊息](03_output.csv) `VK0022` 的 `warn` 診斷，以[結束碼](03_output.md#結束碼) `1` 結束：

  ```text
  $ just vendor_kit update --exit-code
  stdout: base 有新版 v1.3.0（目前為 v1.2.0）。
  stderr: vendor_kit: warn[VK0022]: A newer version of base is available: current v1.2.0; new v1.3.0. Run: just vendor_kit upgrade base
  exit code: 1
  ```

- `add <repo> -i <image>`：離線導入，用本機 image 當工具來源。
- `sh bootstrap.sh -i <image>`：用本機 image 當引擎來源，行為見 [bootstrap.sh](#bootstrapsh)。
- 兩種離線導入共通：
  - `<image>` 可以是已載入的本機 image，或 image tar 檔
  - 寫進的版本鎖定行與線上導入相同
  - 缺少必要的 [digest](../../GLOSSARY.md#工具與出貨) 資訊時印出 [訊息](03_output.csv) `VK0031` 診斷，以[結束碼](03_output.md#結束碼) `2` 結束，不退化成只寫 tag，也不拿 image tar 本身的雜湊代替

VK 沒有限時的選項。要限時就在外層包 `timeout(1)`，或用 CI 的逾時設定。

## 追蹤新版

工具與引擎的新版由 Renovate regex preset 追蹤。Renovate 開的 PR 只改一行版本鎖定行；VK 沒有 bot，不 commit，也不開 PR。

PR 上跑 `just vendor_kit test`。版本鎖定行已更新、基準版尚未更新時，`test` 在 stderr 印出 [訊息](03_output.csv) `VK0014` 的 `warn` 診斷，以[結束碼](03_output.md#結束碼) `1` 結束，CI 因而不通過。使用者要在該 PR 分支的本機執行 `just vendor_kit upgrade <repo> -y`，再自行 commit、push；CI 重跑通過後才 merge。

`update --exit-code` 是給腳本判斷有沒有新版的另一條路，不取代 Renovate；它的行為見[各指令專用選項](#各指令專用選項)。

## 輸出

stdout 與 stderr 怎麼分、訊息的前綴與顏色，見 [03 輸出](03_output.md#輸出)。是否成功依 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)。

## 使用者的檔與 VK 的檔

依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)，這一節列出 VK 會碰到哪些檔、怎麼碰。

使用者的檔：

- 適用的 repo 檔含根 `justfile`、初始檔等
- 屬於追蹤檔的 VK 檔裡，交由使用者維護、受合併保護的只有 VK 的設定檔 `.vendor_kit/config.toml`：它不是初始檔，只沿用初始檔的保護與合併規則，換新版或合併前一樣先問
- 其餘屬於追蹤檔的 VK 檔（`version.toml`、基準版、納管紀錄、薄殼）內容由 VK 擁有，VK 重寫它們不構成覆蓋。版本鎖定行雖由 VK 擁有，使用者仍可以照它的固定格式手改來升版或退版；手改不會讓它變成交由使用者維護的內容。薄殼被改過的處置依 [02 不變量第 6 條](02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)
- 執行紀錄與[進度檔](../../GLOSSARY.md#repo-內的檔與狀態)是 VK 的工作狀態，不是使用者的內容

目標不存在時新建檔（例如第一次導入時整份複製的初始檔）不動到既有的內容。動到既有使用者檔、又不構成覆蓋的寫入，只有這四種明定例外：

- 根 `justfile` 加一行 `import`：沒有這個檔就建，有就詢問後 append
- 根 `.dockerignore` 加四行：同上的 append 規則
- append 型初始檔第一次導入時向既有檔 append 內容，規則見下面「append 型的初始檔」
- 已納管初始檔的基準版合併（VK 的設定檔沿用同一套規則）：
  - 使用者沒改過：詢問是否換新版
  - 雙方都改過：詢問是否合併；[合併衝突](../../GLOSSARY.md#初始檔與合併)留下標記，由使用者解，印出 [訊息](03_output.csv) `VK0021` 的 `warn` 診斷並以[結束碼](03_output.md#結束碼) `1` 結束；這次執行做完，有警告

append 型的初始檔：

- 幾乎一定已經存在的那類初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`
- 沒有這個檔就建，已經有就問過才 append
- 唯一例外是根 `justfile` 不存在時建檔附的 `default`；那個檔建立後就是 repo 檔

移除時收回自己插入的行，只有這三類：

- `uninstall` 移除安裝時加在根 `justfile` 的那一行 `import`
- `uninstall` 移除加在根 `.dockerignore` 的那四行
- `remove` 與 `uninstall` 移除 append 型初始檔當初插進既有檔的那幾行

有紀錄、所以會被收回動作碰到的檔，就是根 `justfile`、根 `.dockerignore`，以及工具宣告為 append 的那些檔。收回時：

- 整份檔裡恰好一處與當初插入的原文相同，才刪那一行
- 一處也沒有、或有兩處以上，都不刪，講出是哪個檔、找到幾處；一處也沒有時印出 [訊息](03_output.csv) `VK0016` [警告](../../GLOSSARY.md#執行與結果)，有兩處以上時印出 [訊息](03_output.csv) `VK0017` 警告，兩者都以[結束碼](03_output.md#結束碼) `1` 結束

其他情況：

- `add` 遇到已存在的檔：不納管、不覆蓋，印出 [訊息](03_output.csv) `VK0018` 警告並以[結束碼](03_output.md#結束碼) `1` 結束
- `remove` 與 `uninstall`：不刪初始檔，只把清單印到 stdout，不加前綴，以[結束碼](03_output.md#結束碼) `0` 結束

## 檢查 (test)

[test](../../GLOSSARY.md#vk-recipe-與用途) 是 VK 的檢查指令，本機與 CI 用同一個。`test` 不寫入追蹤檔。檢查的範圍照這個原則：

- [01 目的與承諾](01_purpose.md)的對外[契約](../../GLOSSARY.md#介面版與契約)中，CI 驗得到的項目百分之百覆蓋
- CI 驗不到的項目由 VK 的驗收測試覆蓋，依 [02 不變量第 9 條](02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)

兩種用法：

- `just vendor_kit test`：跑全部檢查
- `just vendor_kit test dist`：只檢查工具交付的內容，給提供工具的 repo 在自己的 CI 用。幾乎一定已經存在的那類初始檔若不用 append 型、改用整份複製，會被它擋下

`test` 的嚴格規則不因執行環境改變：

- 基準版落後版本鎖定行時，在 stderr 印出 [訊息](03_output.csv) `VK0014` 的 `warn` 診斷，以[結束碼](03_output.md#結束碼) `1` 結束，並指出該執行的 `upgrade` 指令。
- 發現任何本機覆寫時，在 stderr 印出 [訊息](03_output.csv) `VK0032` 的 `error` 診斷，以[結束碼](03_output.md#結束碼) `2` 結束，並指出該執行的 `undev` 指令。

其他結束碼也是 `0`～`3`，意思見 [03 輸出](03_output.md#結束碼)。
