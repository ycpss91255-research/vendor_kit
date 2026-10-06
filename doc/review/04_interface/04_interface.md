# 04 使用者介面

[使用者](../../../GLOSSARY.md#角色與情境)與自動化平常用 `just vendor_kit` 操作 [VK](../../../GLOSSARY.md#角色與情境)。`bootstrap.sh` 只用於首次[導入](../../../GLOSSARY.md#角色與情境)，以及[薄殼](../../../GLOSSARY.md#vk-組件)的檢查、明確要求的修復與完成未完成的 [uninstall](../../../GLOSSARY.md#vk-recipe-與用途) (待確認 (N8b)，選項名及所用引擎版本未定)。

這一頁列必要的參數、選項與操作流程；其他選項細節留到實作時定。

## 目錄

- [主機需求](#主機需求)
- [registry 與認證](#registry-與認證)
- [共同選項](#共同選項)
- [入口](#入口)
- [bootstrap.sh](#bootstrapsh)
- [指令](#指令)
- [各指令專用選項](#各指令專用選項)
- [追蹤新版](#追蹤新版)
- [輸出](#輸出)
- [使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
- [檢查 (test)](#檢查-test)

## 主機需求

依 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)，bash 是支援平台既有的 shell。主機另需：

| 主機程式 | 最低版本 | 使用方式 |
|---|---|---|
| [Docker](https://www.docker.com/) | 19.03 | 不支援 Podman；[啟動器](../../../GLOSSARY.md#vk-組件)在首次導入與既有[安裝目錄](../../../GLOSSARY.md#工具與出貨)都檢查；daemon 形態見下方 |
| [Git](https://git-scm.com/) | 不設最低版本 | VK 不在主機呼叫 git；啟動器往上找 `.git`，確認位於 git [repo](../../../GLOSSARY.md#工具與出貨) 內；目錄或檔都算，適用 worktree 與 submodule |
| [just](https://github.com/casey/just) | 1.33.0 | 首次導入檢查；使用 [just Release 下載頁](https://github.com/casey/just/releases/latest)的版本 |

待確認 (N6b)：支援本機 rootful (不開 userns-remap)、同一使用者的 rootless；WSL2 Docker Desktop 是候選，實機驗收通過才算支援。snap、遠端、DinD、userns-remap 不承諾支援。daemon 形態屬主機前置檢查，首次導入與既有安裝目錄都由啟動器檢查，不通過時不建[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)；建執行紀錄後另做能力檢查，失敗走一般[失敗](../../../GLOSSARY.md#執行與結果)。[診斷](../../../GLOSSARY.md#執行與結果)見[訊息表](../../contract/reason_codes.csv)。

主機前置檢查不通過時的處置見[訊息表](../../contract/reason_codes.csv)。已有安裝目錄若使用太舊的 just，會在讀取 justfile 時由 just 自己報錯，尚未進入 VK，也不留[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)。

## registry 與認證

[工具 image](../../../GLOSSARY.md#工具與出貨) 與[引擎 image](../../../GLOSSARY.md#工具與出貨) 的 [registry](../../../GLOSSARY.md#工具與出貨) 支援範圍：

- 支援：GitHub Container Registry (GHCR)
- 不支援：Docker Hub、Quay、GitLab Container Registry、自架 registry、其他

引擎 image 公開；工具 image 是否公開，由[出貨](../../../GLOSSARY.md#角色與情境)的 repo 決定。測試用 image 的範圍另見[檢查 (test)](#檢查-test)。

| 動作 | 用誰的憑證 | 沒有或不夠時 |
|---|---|---|
| 查版本清單 (`update`、`add`、`upgrade <repo>`) | 公開不必設定；私有用 `--registry-token-file <path>`，帳號須有讀取權限 | 沒有憑證時，可加選項重跑，或用 `<repo>@<tag>` 直接指定版本；待確認 (D7)：私有 package 在本機沒有 image 時，這條路目前停在 VK0055 |
| 下載 image (`add`、`upgrade`、`sync`、啟動器) | 主機或 CI 的 Docker；私有 image 先 `docker login ghcr.io` | Docker 沒有足夠讀取權限就無法下載 |

- 兩邊憑證不互通
- `@<tag>` 只省掉查版本清單，不省掉下載認證
- VK 不在執行中要求帳號、密碼或 token
- 認證與存取失敗的訊息見[訊息表](../../contract/reason_codes.csv)；token 被拒後不改走匿名重試
- registry 連線逾時 10 秒、單一請求逾時 30 秒；連線失敗、逾時、429、5xx 才重試，最多 3 次，間隔從 1 秒起倍增；401、403、404 不重試，不跟隨轉址
- token 用 Basic 認證換 bearer，帳號固定為 `vendor_kit`
- 啟動器 pull 引擎 image 使用 `timeout`，逾時為 600 秒

## 共同選項

兩個入口共用的選項先列在這裡；是否接受仍依各入口與指令的規則。

| 選項 | 用途 |
|---|---|
| `-h` / `--help` | 顯示該入口或指令的用法；實際 help 輸出是唯一來源 |
| `-i` / `--image <image>` | 指定本機 image 或 image tar；可用組合見[離線導入](#離線導入)及[本機覆寫](#本機覆寫) |
| `-y` / `--yes` | 預先回答允許的[詢問](../../../GLOSSARY.md#執行與結果)，適用範圍見下方 |

[-y](../../../GLOSSARY.md#執行與結果) 只適用於[可寫 recipe](../../../GLOSSARY.md#執行與結果)。可能詢問的指令就接受，這次沒有問到也接受：`add`、`upgrade <repo>`、`upgrade --engine` (含 `--engine=<tag>`)、`remove`、`install`、`uninstall`，以及由 `bootstrap.sh` 首次導入時傳給 `install`；只檢查與修復不接受。

- 授權界線依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)；它只省略詢問，改動仍印到 stdout
- `dev`、`undev`、`update`、`sync`、`prune`、`test` 不接受 `-y`，收到時回 VK0026；本段的 `-y`／`--yes` 與下節的 `--dry-run` 都不接受重複給定 (如 `-y --yes` 或兩次 `--dry-run`)，第二個算不允許的參數；依 [02 不變量第 12 條](../../contract/02_invariants.md#12-依對外承諾無法唯一判定就停任何環境一律採最嚴格行為)，對重複給定採最嚴格的解讀
- stdin 與 stderr 都是終端 (TTY) 才能互動；管線不算，不另從 `/dev/tty` 讀答案
- 提示為 `[y/N]`，印到 stderr；答案從 stdin 讀，空白 Enter 等於否，EOF 不算同意
- 沒帶 `-y` 又不能互動時，不做需詢問的修改；重跑方式、[診斷](../../../GLOSSARY.md#執行與結果)與[結束碼](../../../GLOSSARY.md#執行與結果)見[訊息表](../../contract/reason_codes.csv)
- 每次呼叫先問完所有問題，全部同意才寫入（執行紀錄除外；答否時若需記下拒絕，只寫 [metadata](../../../GLOSSARY.md#初始檔與合併)，見 [03 輸出](../../contract/03_output.md#輸出)），含恢復舊操作
- 詢問中 Ctrl-C 不算同意；最終碼受 just 與外層訊號處理影響

### 預演

待確認 (D1)：`--dry-run` 只有長選項；本節的預演規則尚待確認。`add`、`upgrade <repo>`、`upgrade --engine`、`remove`、`uninstall`、`install`、`dev`、`undev`、`prune` 接受；`update`、`test`、`test dist`、`sync` 不接受。

- 算出完整計畫，輸出格式見 [03 輸出](../../contract/03_output.md#輸出)
- 不詢問，不能互動也不報 VK0002；接受 `-y` 的指令可與 `-y` 並用，`-y` 沒有作用
- 除執行紀錄外不寫檔、不建[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)。殘留進度檔照留，只印會一併完成哪些操作
- 持共享鎖；算計畫所需的 image 照常取得（下載或載入），不刪除容器
- 算計畫時遇到阻擋，照各自的碼停下；[警告](../../../GLOSSARY.md#執行與結果)與結束碼見 [03 輸出](../../contract/03_output.md#輸出)
- `upgrade --engine --dry-run` 第一段只解析目標、判降版，印會換上的[版本鎖定行](../../../GLOSSARY.md#版本與來源)與「第二段要等重跑時由新引擎做」，不報 VK0023；沒有警告或其他失敗時以 `0` 結束；第二段列出會重產的薄殼、會升級的 [VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與 `config.toml` 的動作
- `prune` 預演列出會刪的容器；共享鎖下只是預估
- `--dry-run` 重複給定依上節的最嚴格解讀處理；給兩次、寫成 `--dry-run=…`、與 `-h` 並用或放在 `--` 之後，都回 VK0026
- [救援路徑](../../../GLOSSARY.md#介面版與契約)接受 `install --dry-run [-y]`、`upgrade --engine[=<tag>] --dry-run [-y]`；`sync` 不接受

## 入口

| 入口 | 用途 |
|---|---|
| `bootstrap.sh` | 首次導入、薄殼檢查與修復 |
| `just vendor_kit <cmd>` | 日常與 CI 操作；`<cmd>` 換成要執行的 [VK recipe](../../../GLOSSARY.md#執行與結果) 名稱，例如 `update`、`add`、`upgrade` |

`bootstrap.sh` 是啟動器，檔名固定，每個 Release 各附一份；下面的網址預設取最新 Release。要指定版本時，把網址的 `latest/download` 換成 `download/vX.Y.Z`；本頁的 `vX` 指 `vX.Y.Z` 的 X。含此資產的 Release 尚未發布前，流程尚不可用。取得與執行流程：

1. 從最新 Release 下載 `bootstrap.sh` 到目前目錄；下載失敗時以非零結束，不繼續執行後續步驟。

   ```bash
   wget -O bootstrap.sh "https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh" || exit $?
   vk_bootstrap="$PWD/bootstrap.sh"
   ```

2. 賦予執行權限。

   ```bash
   chmod +x "$vk_bootstrap"
   ```

3. 把 `<目標目錄>` 換成要導入或已有 VK 的目錄，再執行。

   ```bash
   cd <目標目錄>
   "$vk_bootstrap"
   ```

## bootstrap.sh

| 呼叫 | 正常行為 |
|---|---|
| 首次導入（可帶 `-i`、`-y`），或未完成的首次導入 | 取得內嵌那版[引擎](../../../GLOSSARY.md#vk-組件)（帶 `-i` 時改用指定的本機 image），呼叫 `install` 導入目前目錄 |
| 不帶選項，既有安裝目錄 | 只檢查薄殼；一致時報告一致 |
| `--repair`，既有安裝目錄 | 一致則不重產；不符則先逐檔列差異，再重產並報告結果，不詢問 |
| 完成未完成的 uninstall (待確認 (N8b)) | 完成移除；選項名及所用引擎版本未定 |
| 單獨 `-h` / `--help` | 只印用法，不做主機檢查、不寫檔，不印內嵌引擎版本 |

- 不收位置參數，沒有 `--version`；短長選項同義，順序不限，`--repair` 只有長選項
- `-h` / `--help` 只准單獨使用；`-y` 只在首次導入傳給 `install`，任何情況都不接受 `--repair -y`
- 首次導入的寫入、詢問與檔案處理見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
- 用法、主機條件、鎖定行、引擎取得與薄殼不符的診斷及結束碼，統一見[訊息表](../../contract/reason_codes.csv)的 `source` 含 `bootstrap` 的列

### 首次導入還是既有安裝目錄

目前目錄沒有 `.vendor_kit/` 才是首次導入；有就按既有安裝目錄處理。讀不出恰好一行有效的引擎[版本鎖定行](../../../GLOSSARY.md#版本與來源)時，不猜版本或改走首次導入，處置見[訊息表](../../contract/reason_codes.csv)。

唯一例外是未完成的首次導入：允許重跑首次導入，也可帶 `-y`；條件是最近一筆執行紀錄是首次導入，且符合任一條件：

- 因需詢問、沒帶 `-y` 又不能互動（含 EOF）而停下，除紀錄外未修改任何檔
- 建紀錄後、寫入引擎版本鎖定行前結束，不論是否已寫入其他檔

例外判定：

- 讀得出有效引擎版本鎖定行，就不套用例外
- 依最近一筆執行紀錄判定是否符合上述條件，不靠目錄內有哪些檔
- 紀錄不足以唯一判定就不套用；此狀態的用法錯誤或 `--repair` 呼叫不建紀錄，不改變判定用的最近一筆紀錄

### 用哪一版引擎

| 模式 | 引擎來源 |
|---|---|
| 首次導入 | 腳本內嵌那一版；`-i <image>` 可改用離線交付 |
| 既有安裝目錄的檢查、修復 | 引擎版本鎖定行那一版，不套用[本機覆寫](../../../GLOSSARY.md#版本與來源) |

既有安裝目錄帶 `-i` 可用本機 image 或 image tar，但 [digest](../../../GLOSSARY.md#工具與出貨) 必須符合鎖定行；以 [image 引用](../../../GLOSSARY.md#工具與出貨)指定時，完整引用也須相同。

腳本只保證與同一個 vX 的鎖定引擎一起用；跨 vX 時須換用對應 vX 的腳本。拒絕結果見[訊息表](../../contract/reason_codes.csv)。

### 判定順序

1. 先看 `.vendor_kit/` 與有效鎖定行，必要時依既有執行紀錄辨識未完成首次導入，以判定是否接受 `-y`
2. 判用法、檢查主機；首次導入、只檢查、`--repair` 都檢查 Docker 與 daemon 形態（待確認 (N6b)），just 只在首次導入檢查，git 位置見[主機需求](#主機需求)
3. 建紀錄前判定跨 vX、git 位置、首次導入的巢狀安裝、非安裝目錄的 `--repair`，以及不適用例外的無效鎖定行；被拒絕時不建紀錄、不寫檔
4. 依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)建執行紀錄，再取得 image、啟動引擎；首次導入在呼叫 `install` 前建好，只檢查與修復在比對前建好
5. 只檢查與修復先辨識升引擎未完成的進度檔；有就依訊息表的下一步重跑原 `upgrade`，不比對或重產薄殼。待確認 (N8b)：也辨識 uninstall 進度檔，以 VK0083 停下，下一步為完成模式指令；選項名及所用引擎版本未定

### 寫入範圍與其他指令的關係

除執行紀錄外：

| 模式 | 寫入範圍 |
|---|---|
| 只檢查 | 不寫檔 |
| `--repair` | 只重產 `.vendor_kit/` 下的 `entry.just`、`vendor.just`、`log.sh`、`.gitignore`；一致則不重產 |

- 不執行 repo 內的薄殼，也不從薄殼讀版本或模板；薄殼只用於逐檔比對
- `--repair` 不經過 `install`，不補其他安裝步驟，不改鎖定行、設定、根目錄檔或其他狀態，也不改腳本本身
- [救援路徑](../../../GLOSSARY.md#介面版與契約)分兩類：薄殼被改過用此入口檢查或修復；版本組合不合用[說明與用法錯誤](#說明與用法錯誤)列出的 just 呼叫

## 指令

v1.0.0 的 `add`、`upgrade`、`remove`、`dev`、`undev` 一次只處理一個[工具](../../../GLOSSARY.md#工具與出貨)，或明確指定引擎，不提供批次或「全部」操作。`update`、`sync`、`test` 則處理全部工具。

| 呼叫（前面加 `just vendor_kit`） | 功能 |
|---|---|
| `add <repo>`、`add <repo>@<tag>`、`add <repo> --image-path <registry>/<path>`、`add <repo> -i <image>` | 導入工具，可指定版本、image 路徑或離線來源；`--image-path` 名稱待確認 (N2b) |
| `upgrade <repo>`、`upgrade <repo>@<tag>` | 升降工具版本 |
| `upgrade --engine`、`upgrade --engine=<tag>` | 升降引擎版本 |
| `dev <repo> -p <dir>`、`dev --engine -i <image>` | 改用[本機開發來源](../../../GLOSSARY.md#版本與來源) |
| `undev <repo>`、`undev --engine` | 回到[鎖定版本](../../../GLOSSARY.md#版本與來源) |
| `remove <repo>` | 解除工具，保留[初始檔](../../../GLOSSARY.md#初始檔與合併) |
| `update`、`update <repo>` | 查新版 |
| `sync`；每個[工具 recipe](../../../GLOSSARY.md#工具與出貨) 前也會自動執行 | 同步[工具內容](../../../GLOSSARY.md#工具與出貨) |
| `install`、`uninstall`；首次導入由啟動器呼叫 `install` | 補做安裝或移除 VK |
| `prune` | 清理不再使用的本機資源 |
| `test`、`test <path>`、`test dist` | 檢查安裝、執行使用者測試或檢查交付 |

### 執行位置

- VK recipe 只准在安裝目錄執行，[唯讀 recipe](../../../GLOSSARY.md#執行與結果) 也一樣；檢查使用者打指令時所在目錄，不是 just 切換後的位置
- `just vendor_kit install` 用於已有入口的安裝目錄；未安裝目錄的首次導入由 `bootstrap.sh` 呼叫引擎的 `install`
- 工具 recipe 自動觸發的 `sync` 先回安裝目錄；工具自身的執行位置由工具決定
- 非安裝目錄與巢狀安裝的拒絕結果見[訊息表](../../contract/reason_codes.csv)；安裝單位依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)

### 命名空間

```text
just vendor_kit <cmd> [arguments] [options]
```

`vendor_kit` 是 VK 的命名空間，`<cmd>` 是 VK recipe 名稱。工具 recipe 的呼叫則為 `just <ns> …`。

- 一個工具可提供多個 [\<ns\> 命名空間](../../../GLOSSARY.md#工具與出貨)
- `vendor_kit` 是保留名稱，不接受 `add vendor_kit`
- `add` 在任何寫入前檢查 `<ns>` 是否與已裝工具、根 `justfile` 的 recipe 或 module、保留名 `vendor_kit` 撞名；拒絕結果見[訊息表](../../contract/reason_codes.csv)

### 說明與用法錯誤

判定順序：用法 → 主機前置檢查 → 辨識走救援路徑的呼叫 → 版本組合（判定順序待 [判定順序討論](https://github.com/ycpss91255-research/vendor_kit/issues/497)定案）。版本組合判定依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。

以下現行實作行為跟 [判定順序討論](https://github.com/ycpss91255-research/vendor_kit/issues/497)一起送審，尚未定案：版本組合不合又有用法錯誤時，先報版本組合不合，以 `3` 結束；救援候選解析失敗 (如 `upgrade --engine --bogus`) 也如此，不因此擴充救援清單。合文法的救援照舊可用；`install -h`、`upgrade --engine -h`、`sync -h` 在[介面版](../../../GLOSSARY.md#介面版與契約)不合時照印用法。

| 版本組合不合時仍可用的類別 | 呼叫 |
|---|---|
| 操作 | `install`、`upgrade --engine`、`sync` |
| 用法 | `just vendor_kit`、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項同） |

- 各指令的 `-h` / `--help` 印該指令用法，沒有 `help` 指令；只准與決定印哪份用法的 `--engine` 並用，`<repo>` 不算
- 救援清單以外的 help 不另開相容性例外；拒絕結果見[訊息表](../../contract/reason_codes.csv)
- 只打 `just vendor_kit` 的版本行與用法錯誤輸出，見 [03 輸出](../../contract/03_output.md#輸出)
- 不認得的名稱、直接接 `-h` 或 `--version`（如 `just vendor_kit foo`）由 just 找 recipe，參數到不了 VK；這時由 just 自己印出不帶 `vendor_kit:` 前綴的錯誤訊息並以非零結束 (just 1.33.0 起為 `1`)；這個碼是 just 回的，不表示 VK 的 `warn`，也不在 [03 結束碼](../../contract/03_output.md#結束碼)的範圍內。
- 不支援 `--allow-missing` 或 `JUST_ALLOW_MISSING`
- 缺必要參數、不認得或多出的參數、help 混用、[tag](../../../GLOSSARY.md#工具與出貨) 格式不合等用法錯誤，見[訊息表](../../contract/reason_codes.csv)

參數與選項：

- 位置參數只放工具名稱 [\<repo\>](../../../GLOSSARY.md#工具與出貨)；`test <path>` 是例外。`test dist` 是完整指令名，`dist` 不是工具名或 path
- 其他值以選項帶入，例如 `-p <dir>`、`-i <image>`；選項可放位置參數前或後
- 引擎一律用 `--engine`；帶版本只收 `--engine=<tag>`，不收 `--engine <tag>`；工具用 `<repo>@<tag>`
- [選項結束標記](../../../GLOSSARY.md#執行與結果)為單獨的 `--`；之後一律當位置參數，即使以 `-` 開頭

| 形式 | 選項 |
|---|---|
| 短長都有 | `-h` / `--help`、`-y` / `--yes`、`-i` / `--image`、`-p` / `--path` |
| 只有長 | `--engine`、`--registry-token-file`、`--repair`、`--image-path` (只有 [add](../../../GLOSSARY.md#vk-recipe-與用途) 接受，名稱待確認 (N2b))、`--dry-run` |

### 指定版本

指令中 `<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../../GLOSSARY.md#工具與出貨) 規則：

- 只收 `vX.Y.Z`，三個數值不收前導零，不帶 pre-release 或 build 後綴
- 最新版把 X、Y、Z 當非負整數逐欄比數值，取最大者；不看字串順序、回傳順序或推送時間，沒有 channel 或撤回標記
- 同一 tag 改指別的 digest 不算新版；最新版不限目前工具的 vX
- 工具功能與工具間相容性的範圍見 [01 目的與承諾](../../contract/01_purpose.md#vk-不做的事)；交付格式與引擎相容性依 [02 不變量第 7 條](../../contract/02_invariants.md#7-工具-image-只承載交付資料引擎與工具不互相綁發版)
- `upgrade <repo>@<tag>` 可指定舊版工具；`upgrade --engine=<tag>` 可指定舊版引擎，但須能無損讀取現有 [VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)，拒絕結果見[訊息表](../../contract/reason_codes.csv)
- 待確認 (D7)：`add`、`upgrade` 指定 `@<tag>` 時，本機有該 image 就不連 registry；沒有才匿名取 digest，再 `pull <路徑>@<digest>`，不讀 token 檔；私有 package 在本機沒有 image 時，這條路目前停在 VK0055。不帶 tag 才讀 token 檔、列 tag 取最新版；本機有 image 時，拿 registry 的 digest 比對
- 工具有逐檔紀錄時，在讀 token 檔、連 registry 前就停下；目前無法判定基準版是否落後
- 不另加 `init`、`ensure`、`diff`、`accept`、`rollback` 等別名或 `--purge`；用途由既有指令、選項或 git 處理

### 成對與無害

| 操作 | 對應操作 |
|---|---|
| `add` | `remove` |
| `dev` | `undev` |
| `install` | `uninstall` |

工具升版的流程：

1. `update` 只查；真正換版本用 `upgrade`
2. 裝工具內容，做[基準版合併](../../../GLOSSARY.md#初始檔與合併)，更新[基準版](../../../GLOSSARY.md#初始檔與合併)與[納管](../../../GLOSSARY.md#初始檔與合併)紀錄，必要時重產薄殼；檔案詢問與保留見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
3. 由此次工具 `upgrade` 換版時，最後才寫版本鎖定行；寫入與恢復原則依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)

工具的版本鎖定行已更新，不代表初始檔合併已完成。鎖定行比基準版新時，不帶 tag 的 `upgrade <repo>` 只完成鎖定行那一版的合併，不再查最新版。

- 可寫 recipe 先恢復進度檔中的未完成操作，再判是否重複；唯讀 recipe 只偵測，下一步見[訊息表](../../contract/reason_codes.csv)
- `bootstrap.sh --repair` 只修薄殼，不套用一般恢復規則補做安裝
- 已完整且一致的 `add`、`install`、`upgrade`，stdout 說明未變更；`add` 要換 tag 時改用 `upgrade`，見訊息表
- `remove` 後再 `add`：留下的初始檔照既有檔處理；已收回的 append 行重新詢問才加，未收回的內容不得無條件再 append
- `sync`、`prune` 不改[追蹤檔](../../../GLOSSARY.md#repo-內的檔與狀態)
- 待確認 (D14)：`prune` 成功後，啟動器清理容器已被這次 [prune](../../../GLOSSARY.md#vk-recipe-與用途) 刪光的殘留 session 目錄；stdout 不列、執行紀錄不記，判斷不出歸屬的目錄不清
- `prune` 不詢問，stdout 列出清理內容：本安裝目錄 [cache/](../../../GLOSSARY.md#repo-內的檔與狀態) 中未鎖定的工具目錄、VK 暫存、VK 建立且可證明不再使用的已停止容器；image 無法證明無人使用就不刪

### 本機覆寫

| 呼叫 | 行為 |
|---|---|
| `dev <repo> -p <dir>` | 工具改用存在且符合交付格式的本機目錄；相對路徑以安裝目錄為準 |
| `dev --engine -i <image>` | 引擎改用本機 image |
| `undev <repo>`、`undev --engine` | 解除覆寫，隨即同步到當下鎖定版本；不需讀原來源 |

- 覆寫只作用於此工作目錄，worktree 各自一份，不跨 clone
- 每次報告用了哪個覆寫，不加診斷前綴：`update` 到 stderr，其餘到 stdout
- 除 `test` 外的一般 recipe 照常執行；覆寫來源失效只擋需讀它的動作，`update` 仍照鎖定行查，bootstrap 忽略覆寫
- 重複 `dev` 同來源、或工具存在但無覆寫與未完成操作的 `undev`，stdout 說明未變更；不同來源、工具不存在等拒絕結果見[訊息表](../../contract/reason_codes.csv)
- `undev` 同步未完成時，覆寫已解除，須重跑原 `undev`；`sync` 不代替完成或清掉其進度檔

- 工具來源可以在安裝目錄外：`-p` 接受以 `..` 開頭的相對路徑或其他絕對路徑；啟動器複製進 session 後再驗，保存的值保留使用者寫法。值不是 UTF-8、含單引號、雙引號、反斜線或控制字元，或正規化後為 `/`，就停下
- `sync`、`upgrade`、`add`、`remove` 重產入口檔時也讀安裝目錄外的覆寫；`add`、`remove` 套用其他工具的覆寫並在 stdout 報告，答否也報
- `dev --engine -i <image>` 只用本機 image，不 pull；先讀 LABEL，確認引擎支援的介面版範圍（[最低介面版](../../../GLOSSARY.md#介面版與契約)到目前介面版）包含薄殼的[介面版](../../../GLOSSARY.md#介面版與契約)才寫覆寫，不含時回 VK0085。範圍包含薄殼介面版的較舊引擎也接受；同一 image 回未變更，不同 image 回 VK0050，入口檔不動
- 待確認 (D18)：啟動器套用引擎覆寫時，本機必須已有 image，不 pull、不讀[介面版列表](../../../GLOSSARY.md#介面版與契約)；LABEL 所載引擎支援的介面版範圍（最低介面版到目前介面版）不含薄殼的介面版時回 VK0086。走救援路徑的呼叫也用覆寫 image，不判介面版；`undev --engine` 用鎖定引擎，bootstrap.sh 不套用覆寫
- 用了引擎覆寫時，由引擎在輸出中報告
- 待確認 (O1)：覆寫存在、版本鎖定行卻沒有對應工具時，`add`、`remove`、`sync`、`upgrade` 目前都先以 VK0056 停下，`test` 報 VK0071；是否允許修復未定
- 待確認 (O2)：`add` 先讀全部覆寫，任一來源失效時，即使該工具已加入且未變更，也報 VK0052

## 各指令專用選項

### add 的 image 路徑

待確認 (N2b)：選項名為 `--image-path <registry>/<path>`，只收 `ghcr.io/<路徑>`，不帶 tag 或 digest；值不合或與 `-i` 並用回 VK0026。沒有鎖定行又沒給此選項時回 VK0025，`<argument>` 印 `--image-path`。

待確認 (T2)：已有鎖定行時一律用鎖定行的路徑，給了不同值也忽略；不帶 tag 或指定同一 tag 時，stdout 說明未變更，不連 registry。

### registry token 檔案

`--registry-token-file <path>`：

- 只有長選項，只收檔案路徑，不收 token 字串；不從 stdin 讀，單獨的 `-` 算用法錯誤；相對路徑以安裝目錄為準
- 只有 `update`、`add`、`upgrade <repo>` 接受，不適用引擎升版
- 只有真的要查版本清單時才讀檔，一次執行只讀一次；指定 tag 或離線導入而不查清單時不讀。安裝目錄外的 token 檔由啟動器複製進 session
- 憑證用途見 [registry 與認證](#registry-與認證)，讀檔與認證問題見[訊息表](../../contract/reason_codes.csv)

### upgrade --engine

1. 第一段換上目標引擎，尚未完成的結果見[訊息表](../../contract/reason_codes.csv)
2. 按診斷句尾的完整指令手動重跑，由新引擎完成剩餘步驟；保留原 tag 與 `-y`

第二次呼叫答否，不撤回第一次已完成的換引擎，第一段的鎖定行與進度檔不動。

- 鎖定行已是目標版、沒有進度檔，但薄殼或 VK 檔仍是舊版時，直接做第二段；全部已是這一版才回未變更
- 第二段重產不一致的薄殼；`gen/.stamp` 不同才寫；VK 檔升到本引擎的[檔案版](../../../GLOSSARY.md#介面版與契約)上限，[介面版列表](../../../GLOSSARY.md#介面版與契約)改為本引擎支援的介面版範圍（最低介面版到目前介面版）
- `config.toml` 換版在第二段：新版等於基準版就不動、不問；使用者沒改過先問換版，雙方都改過先問合併；使用者刪了就不重建、記 `deleted`。題目併入第二段的一次問完；解析失敗的例外見[寫入既有檔的例外](#寫入既有檔的例外)
- 第一段在進度檔已建、鎖定行未換時中斷，重跑原指令照進度檔的目標重做第一段，再報 VK0023；不帶 tag 也不列 registry
- 引擎升版不讀 token 檔

### sync

1. 做主機前置檢查
2. 在逐工具處理前判薄殼與版本組合；任一阻擋就不取件，兩者皆不符時都報告，結果依[訊息表](../../contract/reason_codes.csv)與 [03 結束碼](../../contract/03_output.md#結束碼)。待確認 (D4)：目前實作在薄殼的介面版不在引擎支援的介面版範圍（最低介面版到目前介面版）且薄殼為別版模板時，引擎只報 VK0006；這與兩者皆不符時都報告的定案不一致
3. 再逐工具同步；跨工具寫入界線依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)，同階段判定與輸出順序不承諾

| 同步對象 | 行為 |
|---|---|
| 已鎖定工具 | 判定 cache 檔案集合與[逐檔指紋](../../../GLOSSARY.md#repo-內的檔與狀態)，包括多出的檔案；不一致則重新取件 |
| 既有[印記](../../../GLOSSARY.md#repo-內的檔與狀態)損壞 | 重新取件並重建；首次取件原本沒有印記不算損壞 |
| 未列在鎖定行的工具目錄 | 留給 `prune` |
| 初始檔的基準版落後 | 不自動合併，改用 `upgrade` |

[取件](../../../GLOSSARY.md#工具與出貨)、[metadata](../../../GLOSSARY.md#初始檔與合併) 或未完成導入等問題的診斷與下一步見[訊息表](../../contract/reason_codes.csv)。修復快取後仍報告原本問題，診斷與結果見訊息表。工具 recipe 前的自動 `sync` 帶警告完成時，本體是否執行及整次回碼待確認 (N15)，見[自動同步與結果討論](https://github.com/ycpss91255-research/vendor_kit/issues/120)。

### update

- 不帶工具參數查全部工具與引擎；`update <repo>` 只查指定已安裝工具，沒裝的工具拒絕，見[訊息表](../../contract/reason_codes.csv)
- 每次即時查 tag，不用舊查詢快取，沒有 `--exit-code` 選項
- 查詢結果是可解析的固定格式：`<repo> current: <tag> latest: <tag>`
- 每個查詢對象一行，已最新也印，順序不承諾；引擎的工具名欄用 `vendor_kit`
- 欄位以單一 ASCII 空白分隔，欄名以半形冒號結尾，值緊接下一欄；靠欄名取值，不靠欄號，同一個 vX 內只會新增「欄名: 值」成對欄位
- `current:` 是鎖定版本的 tag；`latest:` 是依[指定版本](#指定版本)算出的最新 tag，可能比 current 舊
- 一個對象查詢失敗不擋其他對象；失敗的行印 `latest: none`、各報一條診斷，結束碼取最大。token 檔讀不到時每個對象各報一條 VK0055；registry 一個 tag 都沒有也報 VK0055。有 tag 卻無合法 `vX.Y.Z` 也印 `latest: none`。`none` 只是顯示值，診斷與結束碼見[訊息表](../../contract/reason_codes.csv)
- stdout 只有結果行，不加表頭、進度、顏色或前綴；其他訊息到 stderr
- 目前輸出一律英文，設不設 `LC_ALL=C` 結果相同；日後若做 i18n，要穩定解析的腳本請設 `LC_ALL=C`

正常結果示例：

```text
base current: v1.2.0 latest: v1.2.0
lint current: v1.0.0 latest: v1.3.0
vendor_kit current: v1.4.0 latest: v1.4.0
```

### 離線導入

| 呼叫 | 本機 image 用途 |
|---|---|
| `add <repo> -i <image>` | 工具來源 |
| `bootstrap.sh -i <image>` | 引擎來源 |

- 待確認 (D3)：`-i` 的值以 `.tar` 結尾時當 image tar，其他當 image 引用；離線交付須附多架構 image index digest 資訊，tar 旁檔把 `.tar` 換成 `.digest`，例如 `foo.tar` 對應 `foo.digest`
- 待確認 (B1)：classic image store 載入 tar 後沒有 RepoDigests，之後的 recipe 找不到鎖定引用會去 pull，離線時回 VK0036
- 不要求 tar 本身保存 digest；不拿 tar 雜湊代替，也不退化成只寫 tag；線上與離線的鎖定行關係依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)
- digest 缺失或不符的結果見[訊息表](../../contract/reason_codes.csv)；既有安裝的額外核對見[用哪一版引擎](#用哪一版引擎)
- v1.0.0 不承諾離線升版入口

### 設定

`.vendor_kit/config.toml` 的設定：

| 欄位 | 可用值 | 未設定時 |
|---|---|---|
| `lock_timeout_seconds` | 大於等於 `-1` 的整數：正數為等待秒數；`0` 不等；`-1` 一直等 | 60 秒 |
| `lock_enabled` | 布林值；`false` 只給不支援檔案鎖的檔案系統，每次執行都[警告](../../../GLOSSARY.md#執行與結果) | `true` |
| `[test]` | `image` 為非空字串；`command` 為由非空字串組成的非空陣列 | 無預設 runner；`test <path>` 停下並指名缺少的欄位；不帶 path 的 `test` 不需要 |

`install` 按隨引擎出貨的模板新建 `config.toml`，記 `managed` 紀錄，基準版副本放 `baseline/.vendor_kit/config.toml`。已納管的檔被使用者刪掉時不重建；待確認 (D5)：檔已存在但沒有紀錄時，實作不碰、不記，也不停下。`uninstall` 保留它，在 stdout 只列一次。模板全文：

```toml
# vendor_kit settings for this install directory.
# Every setting is commented out; an unset setting uses the value shown.
# An invalid value stops every vendor_kit command; the default is not used instead.

# How long to wait for the install directory lock, in seconds:
# a positive number waits that long, 0 does not wait, -1 waits forever.
# lock_timeout_seconds = 60

# File locking. Set to false only on file systems without file lock support;
# every run then prints a warning.
# lock_enabled = true

# Runner for `test <path>`. There is no default runner: `test <path>` stops
# and names the missing setting; `test` without a path does not need it.
# image is a non-empty string; command is a non-empty array of non-empty strings.
# [test]
# image = "<image>"
# command = ["<program>", "<argument>"]
```

前兩個欄位是頂層設定。設定在第一次取鎖前讀取；任一設定無效時所有入口一律停下，修法與結束碼見[訊息表](../../contract/reason_codes.csv)，不以預設值繼續。

### 鎖與逾時

鎖的可用值與無效設定處置見[設定](#設定)。

- 所有取鎖入口（含自動 `sync`、bootstrap 啟動的引擎）用同一設定；首次導入固定等 60 秒
- 寫入持排他鎖，讀取與預演持共享鎖；bootstrap.sh 只檢查持共享鎖，`--repair` 持排他鎖；會取件的 `sync` 屬寫入端，實際寫檔程序在其生命週期持鎖
- 等不到鎖的處置見訊息表
- VK 沒有整次執行限時選項；需要時在外層用 `timeout(1)` 或 CI 逾時設定，外層中斷的碼不承諾是 VK 結束碼
- 殺掉主機等待程序不代表容器已停止寫入；恢復前仍須取得鎖，下次執行依紀錄與進度檔辨識未完成操作

## 追蹤新版

VK 提供 Renovate regex preset 追蹤工具與引擎的正式版 `vX.Y.Z`；VK 寫出的版本鎖定行必須能由它辨識與修改。

- `customType: "regex"`；`managerFilePatterns` 只比對 `.vendor_kit/version.toml`，不含 `version.local.toml`
- `matchStrings` 一條抓行首裸鍵及 `"ghcr.io/<路徑>:vX.Y.Z@sha256:<64 hex>"`，群組為 `depName`、`currentValue`、`currentDigest`；不抓[介面版列表](../../../GLOSSARY.md#介面版與契約)（`vendor_kit_protocols` 那一行）
- `datasourceTemplate: "docker"`；versioning 只收沒有前導零的 `vX.Y.Z`
- preset 目前放在 [Renovate preset](../../../test/renovate/preset.json)，正式發布位置未定
- 引擎 PR 在 PR 分支跑 `just vendor_kit upgrade --engine=<鎖定行 tag> -y`，commit 後 CI 通過才 merge

## 輸出

串流、前綴、顏色與結果彙總見 [03 輸出](../../contract/03_output.md)；逐項診斷、處置與結束碼只見[訊息表](../../contract/reason_codes.csv)。這些承諾適用於已進入 VK 的呼叫。

## 使用者的檔與 VK 的檔

檔案權屬依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)與 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、VK 檔的定義；這裡只列操作。

| 檔案 | 操作規則 |
|---|---|
| 根 `justfile`、初始檔等 repo 檔 | 見下面的既有檔寫入與收回規則 |
| `.vendor_kit/config.toml` | 使用者維護，不是初始檔；換版與合併沿用初始檔的保護規則，先詢問 |
| `version.toml`、基準版、納管紀錄、薄殼 | 依各自完整性與恢復規則處理；鎖定行可按固定格式手改升降版 |
| 執行紀錄、進度檔 | 保存操作與恢復所需資訊，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗) |

### 寫入既有檔的例外

目標不存在就新建；既有使用者檔的寫入只有下列例外：

| 寫入 | 操作 |
|---|---|
| 根 `justfile` 的一行 `import '.vendor_kit/entry.just'` | 有檔先詢問再 append |
| 根 `.dockerignore` 的四行 | 同上 |
| append 型初始檔的首次導入 | 有檔先詢問再 append |
| 已納管初始檔的基準版合併（設定檔同；TOML 與 just 的例外見下） | 未改過也先問是否換版；雙方都改過則先問是否合併，衝突留標記給使用者解 |

[合併衝突](../../../GLOSSARY.md#初始檔與合併)的診斷與結束碼見[訊息表](../../contract/reason_codes.csv)。例外：基準版合併結果是 TOML (`*.toml`) 且解析不過，或是 just 檔（`justfile`、`.justfile`，檔名不分大小寫；`*.just`）且留下衝突標記時，留原檔、不詢問、基準版不推進，記進 metadata 的 `conflicts`；`config.toml` 記在 `baseline/.vendor_kit.toml`。之後換版或合併成功才拿掉。`config.toml` 一律適用此例外，不留衝突標記、不報 VK0021。這時的輸出、診斷與結束碼見 [03 輸出](../../contract/03_output.md#輸出)（待確認 (D2)）。

- 幾乎一定已存在的初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`
- 根 `justfile` 不存在時，以下全文中的 `default` 是例外，建立後按 repo 檔處理：

  ```just
  import '.vendor_kit/entry.just'

  default:
      @just --list
  ```

- 根 `.dockerignore` 加入的四行逐字為：

  ```text
  .vendor_kit/cache/
  .vendor_kit/gen/
  .vendor_kit/log/
  .vendor_kit/version.local.toml
  ```
- 待確認 (Y1)：`add` 要 append 進已存在、未納管的檔時，實作的 `-y` 不代答這幾題；有終端只問這幾題，答否為正常取消，沒有終端以 VK0084 停下。另一做法是 `-y` 照常代答這一題，或 `VK0002` 改給別的下一步；尚未選定方案
- `add` 遇到不適用 append 的既有檔不納管、不覆蓋；v1.0.0 不提供改為納管的選項，後續不做基準版合併，結果見訊息表
- `upgrade` 遇到新版不再提供的初始檔或使用者已刪的納管初始檔，不刪、不重建，只在 stdout 列清單
- `remove`、`uninstall` 保留初始檔，保留清單印到 stdout

### 收回插入的行

| 呼叫 | 有紀錄才考慮收回的行 |
|---|---|
| `uninstall` | 根 `justfile` 的一行 `import`、根 `.dockerignore` 的四行 |
| `remove`、`uninstall` | append 型初始檔插進既有檔的行 |

- 整份檔依紀錄的整檔 hash 與 VK 上次寫入後相同（CRLF／LF 視為相同，只改行尾不算改過），且原文恰好一處，才先詢問、同意後刪
- 其他情況只列不刪：列出檔名、紀錄原文與目前相符行號；警告與結束碼見[訊息表](../../contract/reason_codes.csv)
- 舊紀錄沒有 hash 也只列不刪；未登記的檔不碰

### remove 與 uninstall 的收回範圍

`remove` 收回該工具的鎖定行、`cache/<repo>/`、基準版、印記、納管紀錄、[gen/](../../../GLOSSARY.md#repo-內的檔與狀態) 的命名空間載入行，以及同意且符合判準的 append 行；初始檔保留。工具開著覆寫時，先拿掉 `version.local.toml` 中該工具的行，不讀來源，來源失效也不阻擋；保留本機開發來源、其他工具與引擎的覆寫。全部解除後 `version.local.toml` 照留；stdout 報告解除的覆寫，再照常 [remove](../../../GLOSSARY.md#vk-recipe-與用途)。未完成的狀態重跑同一指令就補完。

`uninstall` 的收回範圍與紀錄保存政策（下列）待確認 (N18)，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)；目前介面為：

- 收回鎖定行、基準版、納管紀錄、印記、薄殼、cache、gen、進度檔，以及符合判準的根目錄與工具 append 行；未收回的位置列清單
- 解除覆寫紀錄，不要求先 `undev`，保留本機開發來源
- 保留 `.vendor_kit/config.toml`、使用者檔、未登記檔與 `.vendor_kit/` 目錄，stdout 列出留下的內容
- 先建紀錄與進度，保留恢復證據，最後處理鎖定行與完成的進度檔；殘留與真正中斷的結果見訊息表
- 舊紀錄與本次紀錄留在 `.vendor_kit/`，不另定期限；使用者移走目錄時，紀錄跟著走

重新導入：

1. 把整個 `.vendor_kit/` 移到安裝位置之外
2. 在原位置執行 `bootstrap.sh`
3. 完成後從移走的 `config.toml` 手動搬回自訂內容，不自動承接舊設定

這不擴大[未完成首次導入例外](#首次導入還是既有安裝目錄)。

## 檢查 (test)

[test](../../../GLOSSARY.md#vk-recipe-與用途) 給本機與 CI 共用，檢查目前安裝或交付狀態；帶 path 時，安裝檢查通過後跑使用者自己的測試。VK 自身的出貨驗收另依 [02 不變量第 9 條](../../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)。

| 呼叫 | 用途 |
|---|---|
| `just vendor_kit test` | 只做完整安裝檢查；沒有工具也檢查薄殼與引擎 |
| `just vendor_kit test <path>` | 先做完整安裝檢查，通過才跑所選的使用者測試 |
| `just vendor_kit test dist` | 只檢查工具交付內容，給提供工具的 repo 在 CI 用；檢查 append 型等交付規則，不能混用 path |

安裝檢查列完全部問題才停，除執行紀錄外零寫入，不準備或修復 cache、gen、進度檔：

- 薄殼問題報 VK0006；版本檔檔案版過高報 VK0008，不合正規形報 VK0070
- 本機覆寫各報 VK0032；覆寫有但鎖定行沒有對應工具時報 VK0071
- 殘留進度檔依種類報 VK0004、VK0041、VK0023、VK0053、VK0054
- cache、印記、`gen/tools.just` 缺件或不一致報 VK0047；全新 checkout 缺 cache 也算缺件，CI 先跑 [sync](../../../GLOSSARY.md#vk-recipe-與用途)
- 初始檔的基準版落後報 VK0014；待確認 (N3)：目前實作受 `init.toml` 規則未定影響，無法判定基準版是否落後
- 環境不足報 VK0049
- 沒有工具仍檢查薄殼與引擎，`gen/tools.just` 不在算一致

### test dist

固定讀安裝目錄的 [dist/](../../../GLOSSARY.md#工具與出貨)，不收 path、不往上找；安裝目錄須與 dist/ 在同一層。提供工具的 repo 要先導入 VK，但不必導入自己出貨的工具。

- dist/ 不存在或底下沒有檔時回 VK0048
- 每個 `dist/just/<ns>.just` 提供一個頂層命名空間；不檢查 `<repo>.just` 是否存在
- 只收一般檔與目錄；文字檔 (不含 NUL) 須為 LF，含 CR 就不合格
- 不合格項目逐條列完才以 VK0075 停下；通過印 `Delivery check passed.`
- 待確認 (N3)：`init.toml` 的交付規則

### test 路徑與 runner

- 一次只收一個 path，第一段必須是 `test`，從安裝目錄算起；不收絕對路徑、以 `.` 開頭或含 `..` 的路徑。單獨 `test` 選整個 `test/`；指定檔案只跑該檔，指定資料夾含子資料夾。指向資料夾的符號連結只檢查指向位置，不往下走；FIFO、socket 算無效選取檔。安裝目錄不在 repo 根目錄時，repo 根目錄的 `test/` 不屬於它
- 依 VK 紀錄判定工具交付的測試；使用者改過也算。選中範圍含工具交付的內容（整份初始檔或插入行）就整次不跑；工具移除後才可按使用者測試處理
- 完整安裝檢查的結果不是 `0` 就不啟動 runner，先列出每一項，再補 VK0062，整次以 `max(檢查碼, 2)` 結束；結果與下一步見訊息表
- 使用者依[設定](#設定)在 `[test]` 指定 `image` 與 `command`，VK 不內建 runner
- 通過檢查後，在該 image 容器執行 command 並在最後加上 path，不經 shell；工作目錄為安裝目錄，repo 唯讀掛載，以空目錄遮住 `.vendor_kit/`，runner 另有容器內的可寫暫存空間，結束即丟，寫不進 repo
- 測試 image 不限 registry，由主機 Docker 取得，也可用本機 image；image 與 command 實際執行什麼由使用者負責
- 待確認 (D16)：image 引用帶不進協定 (例如 tag 含大寫) 時回 VK0066，續行印 `unavailable`
- 待確認 (T1)：`lock_enabled = false` 時，VK0060 不算安裝檢查結果；整次結束碼取 1 與 runner 結果的較大者
- runner 的 stdout、stderr 原樣轉出，格式界線見 [03 輸出](../../contract/03_output.md#輸出)
- path 無效、未選到測試、選到工具交付檔、runner 起不來或測試未通過的處置與結束碼，見[訊息表](../../contract/reason_codes.csv)
