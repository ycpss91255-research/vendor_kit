# 04 使用者介面

[使用者](../../../GLOSSARY.md#角色與情境)與自動化平常用 `just vendor_kit` 操作 [VK](../../../GLOSSARY.md#角色與情境)。`bootstrap.sh` 只用於首次[導入](../../../GLOSSARY.md#角色與情境)，以及[薄殼](../../../GLOSSARY.md#vk-組件)的檢查與明確要求的修復。

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
| [Docker](https://www.docker.com/) | 19.03 | 不支援 Podman；[啟動器](../../../GLOSSARY.md#vk-組件)在首次導入與既有[安裝目錄](../../../GLOSSARY.md#工具與出貨)都檢查 |
| [Git](https://git-scm.com/) | 不設最低版本 | VK 不在主機呼叫 git；啟動器往上找 `.git`，確認位於 git [repo](../../../GLOSSARY.md#工具與出貨) 內；目錄或檔都算，適用 worktree 與 submodule |
| [just](https://github.com/casey/just) | 1.33.0 | 首次導入檢查；使用 [just Release 下載頁](https://github.com/casey/just/releases/latest)的版本 |

主機前置檢查不通過時的處置見[訊息表](../../contract/reason_codes.csv)。已有安裝目錄若使用太舊的 just，會在讀取 justfile 時由 just 自己報錯，尚未進入 VK，也不留[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)。

## registry 與認證

[工具 image](../../../GLOSSARY.md#工具與出貨) 與[引擎 image](../../../GLOSSARY.md#工具與出貨) 的 [registry](../../../GLOSSARY.md#工具與出貨) 支援範圍：

- 支援：GitHub Container Registry (GHCR)
- 不支援：Docker Hub、Quay、GitLab Container Registry、自架 registry、其他

引擎 image 公開；工具 image 是否公開，由[出貨](../../../GLOSSARY.md#角色與情境)的 repo 決定。測試用 image 的範圍另見[檢查 (test)](#檢查-test)。

| 動作 | 用誰的憑證 | 沒有或不夠時 |
|---|---|---|
| 查版本清單 (`update`、`add`、`upgrade <repo>`) | 公開不必設定；私有用 `--registry-token-file <path>`，帳號須有讀取權限 | 沒有憑證時，可加選項重跑，或用 `<repo>@<tag>` 直接指定版本 |
| 下載 image (`add`、`upgrade`、`sync`、啟動器) | 主機或 CI 的 Docker；私有 image 先 `docker login ghcr.io` | Docker 沒有足夠讀取權限就無法下載 |

- 兩邊憑證不互通
- `@<tag>` 只省掉查版本清單，不省掉下載認證
- VK 不在執行中要求帳號、密碼或 token
- 認證與存取失敗的訊息見[訊息表](../../contract/reason_codes.csv)；token 被拒後不改走匿名重試
- 網路逾時與重試細節留到實作時定

## 共同選項

兩個入口共用的選項先列在這裡；是否接受仍依各入口與指令的規則。

| 選項 | 用途 |
|---|---|
| `-h` / `--help` | 顯示該入口或指令的用法；實際 help 輸出是唯一來源 |
| `-i` / `--image <image>` | 指定本機 image 或 image tar；可用組合見[離線導入](#離線導入)及[本機覆寫](#本機覆寫) |
| `-y` / `--yes` | 預先回答允許的[詢問](../../../GLOSSARY.md#執行與結果)，適用範圍見下方 |

[-y](../../../GLOSSARY.md#執行與結果) 只適用於[可寫 recipe](../../../GLOSSARY.md#執行與結果)。已定組合為 `upgrade <repo> -y`、`upgrade --engine -y`（含 `--engine=<tag>`）、`install -y`，以及由 `bootstrap.sh` 首次導入時傳給 `install`；只檢查與修復不接受。

- 授權界線依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)；它只省略詢問，改動仍印到 stdout
- 其餘指令是否依「可能詢問才接受」收斂，待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)
- stdin 與 stderr 都是終端 (TTY) 才能互動；管線不算，不另從 `/dev/tty` 讀答案
- 提示為 `[y/N]`，印到 stderr；答案從 stdin 讀，空白 Enter 等於否，EOF 不算同意
- 沒帶 `-y` 又不能互動時，不做需詢問的修改；重跑方式、[診斷](../../../GLOSSARY.md#執行與結果)與[結束碼](../../../GLOSSARY.md#執行與結果)見[訊息表](../../contract/reason_codes.csv)
- 每次呼叫先問完所有問題，全部同意才寫入（執行紀錄除外），含恢復舊操作；答否的正常取消輸出見 [03 輸出](../../contract/03_output.md#輸出)
- 詢問前[取件](../../../GLOSSARY.md#工具與出貨)的內容只放在 repo 外的暫存處，全部同意後才寫進 [cache/](../../../GLOSSARY.md#repo-內的檔與狀態)、[印記](../../../GLOSSARY.md#repo-內的檔與狀態)與 [gen/](../../../GLOSSARY.md#repo-內的檔與狀態)。
- 詢問中 Ctrl-C 不算同意；最終碼受 just 與外層訊號處理影響
- 拒絕記錄的保存方式仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)

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
2. 判用法、檢查主機；首次導入、只檢查、`--repair` 都檢查 Docker，just 只在首次導入檢查，git 位置見[主機需求](#主機需求)
3. 建紀錄前判定跨 vX、git 位置、首次導入的巢狀安裝、非安裝目錄的 `--repair`，以及不適用例外的無效鎖定行；被拒絕時不建紀錄、不寫檔
4. 依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)建執行紀錄，再取得 image、啟動引擎；首次導入在呼叫 `install` 前建好，只檢查與修復在比對前建好
5. 只檢查與修復先辨識升引擎未完成的[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)；有就依訊息表的下一步重跑原 `upgrade`，不比對或重產薄殼

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
| `add <repo>`、`add <repo>@<tag>`、`add <repo> -i <image>` | 導入工具，可指定版本或離線來源 |
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

判定順序：主機前置檢查 → 辨識救援呼叫 → 版本組合 → 用法。VK recipe 的用法只有引擎判得出，引擎要在主機前置檢查、辨識救援呼叫與[介面版](../../../GLOSSARY.md#介面版與契約)判定之後才啟動；[檔案版](../../../GLOSSARY.md#介面版與契約)由引擎在判用法之前判定。版本組合判定依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。

版本組合不合又有用法錯誤時（如 `upgrade --engine --bogus`），先報版本組合不合，不因此擴充救援清單。

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
| 只有長 | `--engine`、`--registry-token-file`、`--repair` |

### 指定版本

指令中 `<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../../GLOSSARY.md#工具與出貨) 規則：

- 只收 `vX.Y.Z`，三個數值不收前導零，不帶 pre-release 或 build 後綴
- 最新版把 X、Y、Z 當非負整數逐欄比數值，取最大者；不看字串順序、回傳順序或推送時間，沒有 channel 或撤回標記
- 同一 tag 改指別的 digest 不算新版；最新版不限目前工具的 vX
- 工具功能與工具間相容性的範圍見 [01 目的與承諾](../../contract/01_purpose.md#vk-不做的事)；交付格式與引擎相容性依 [02 不變量第 7 條](../../contract/02_invariants.md#7-工具-image-只承載交付資料引擎與工具不互相綁發版)
- `upgrade <repo>@<tag>` 可指定舊版工具；`upgrade --engine=<tag>` 可指定舊版引擎，但須能無損讀取現有 [VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)，拒絕結果見[訊息表](../../contract/reason_codes.csv)
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

## 各指令專用選項

### registry token 檔案

`--registry-token-file <path>`：

- 只有長選項，只收檔案路徑，不收 token 字串；不從 stdin 讀，單獨的 `-` 算用法錯誤；相對路徑以安裝目錄為準
- 只有 `update`、`add`、`upgrade <repo>` 接受，不適用引擎升版
- 只有真的要查版本清單時才讀檔；指定 tag 或離線導入而不查清單時不讀
- 憑證用途見 [registry 與認證](#registry-與認證)，讀檔與認證問題見[訊息表](../../contract/reason_codes.csv)

### upgrade --engine

1. 第一段換上目標引擎，尚未完成的結果見[訊息表](../../contract/reason_codes.csv)
2. 按診斷句尾的完整指令手動重跑，由新引擎完成剩餘步驟；保留原 tag 與 `-y`

第二次呼叫答否，不撤回第一次已完成的換引擎。

### sync

1. 做主機前置檢查
2. 在逐工具處理前判薄殼與版本組合；任一阻擋就不取件，兩者皆不符時都報告，結果依[訊息表](../../contract/reason_codes.csv)與 [03 結束碼](../../contract/03_output.md#結束碼)
3. 再逐工具同步；跨工具寫入界線依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)，同階段判定與輸出順序不承諾

| 同步對象 | 行為 |
|---|---|
| 已鎖定工具 | 判定 cache 檔案集合與[逐檔指紋](../../../GLOSSARY.md#repo-內的檔與狀態)，包括多出的檔案；不一致則重新取件 |
| 既有[印記](../../../GLOSSARY.md#repo-內的檔與狀態)損壞 | 重新取件並重建；首次取件原本沒有印記不算損壞 |
| 未列在鎖定行的工具目錄 | 留給 `prune` |
| 初始檔的基準版落後 | 不自動合併，改用 `upgrade` |

[取件](../../../GLOSSARY.md#工具與出貨)、[metadata](../../../GLOSSARY.md#初始檔與合併) 或未完成導入等問題的診斷與下一步見[訊息表](../../contract/reason_codes.csv)。修復快取後仍報告原本問題，診斷與結果見訊息表。工具 recipe 前的自動 `sync` 帶警告完成時，本體是否執行及整次回碼仍待確認，見[自動同步與結果討論](https://github.com/ycpss91255-research/vendor_kit/issues/120)。

### update

- 不帶工具參數查全部工具與引擎；`update <repo>` 只查指定已安裝工具，沒裝的工具拒絕，見[訊息表](../../contract/reason_codes.csv)
- 每次即時查 tag，不用舊查詢快取，沒有 `--exit-code` 選項
- 查詢結果是可解析的固定格式：`<repo> current: <tag> latest: <tag>`
- 每個查詢對象一行，已最新也印，順序不承諾；引擎的工具名欄用 `vendor_kit`
- 欄位以單一 ASCII 空白分隔，欄名以半形冒號結尾，值緊接下一欄；靠欄名取值，不靠欄號，同一個 vX 內只會新增「欄名: 值」成對欄位
- `current:` 是鎖定版本的 tag；`latest:` 是依[指定版本](#指定版本)算出的最新 tag，可能比 current 舊
- 查詢失敗時該行 `latest: none`；registry 有 tag 卻無合法 `vX.Y.Z` 也如此。`none` 只是顯示值，診斷與結束碼見[訊息表](../../contract/reason_codes.csv)
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

- 可用已載入的本機 image 或 image tar；離線交付須附多架構 image index digest 資訊，例如 tar 旁的同名 `.digest` 檔
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

前兩個欄位是頂層設定。設定在第一次取鎖前讀取；任一設定無效時所有入口一律停下，修法與結束碼見[訊息表](../../contract/reason_codes.csv)，不以預設值繼續。

### 鎖與逾時

鎖的可用值與無效設定處置見[設定](#設定)。

- 所有取鎖入口（含自動 `sync`、bootstrap 啟動的引擎）用同一設定；首次導入固定等 60 秒
- 寫入持排他鎖，讀取持共享鎖；會取件的 `sync` 屬寫入端，實際寫檔程序在其生命週期持鎖
- 等不到鎖的處置見訊息表
- VK 沒有整次執行限時選項；需要時在外層用 `timeout(1)` 或 CI 逾時設定，外層中斷的碼不承諾是 VK 結束碼
- 殺掉主機等待程序不代表容器已停止寫入；恢復前仍須取得鎖，下次執行依紀錄與進度檔辨識未完成操作

## 追蹤新版

VK 提供 Renovate regex preset 追蹤工具與引擎的正式版 `vX.Y.Z`；VK 寫出的版本鎖定行必須能由它辨識與修改。

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
| 根 `justfile` 的一行 `import` | 有檔先詢問再 append |
| 根 `.dockerignore` 的四行 | 同上 |
| append 型初始檔的首次導入 | 有檔先詢問再 append |
| 已納管初始檔的基準版合併（設定檔同） | 未改過也先問是否換版；雙方都改過則先問是否合併，衝突留標記給使用者解 |

[合併衝突](../../../GLOSSARY.md#初始檔與合併)的診斷與結束碼見[訊息表](../../contract/reason_codes.csv)。

- 幾乎一定已存在的初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`
- 根 `justfile` 不存在時建檔附的 `default` 是例外，建立後按 repo 檔處理
- 已存在但尚未納管的檔，`-y` 不能改成 append 納管
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

`remove` 收回該工具的鎖定行、`cache/<repo>/`、基準版、印記、納管紀錄、[gen/](../../../GLOSSARY.md#repo-內的檔與狀態) 的命名空間載入行，以及同意且符合判準的 append 行；初始檔保留。工具開著覆寫時的處置仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)。

`uninstall` 的收回範圍與紀錄保存政策仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)；目前介面為：

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

安裝檢查：

- 檢查版本、快取與初始檔的一致性，不準備或修復 cache、gen、進度檔，不寫追蹤檔；執行紀錄照 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)
- 本機覆寫仍會擋下；基準版落後、缺件、環境不足等結果與下一步見[訊息表](../../contract/reason_codes.csv)
- 全新 checkout 缺 cache 的處理仍待確認，見[嚴格檢查決議](https://github.com/ycpss91255-research/vendor_kit/issues/124)

### test 路徑與 runner

- 一次只收一個 path，寫成 `test/...`，從安裝目錄算起；指定檔案只跑該檔；指定資料夾含子資料夾。安裝目錄不在 repo 根目錄時，repo 根目錄的 `test/` 不屬於它
- 依 VK 紀錄判定工具交付的測試；使用者改過也算。選中範圍含工具交付的內容（整份初始檔或插入行）就整次不跑；工具移除後才可按使用者測試處理
- 完整安裝檢查的結果不是 `0` 就不啟動 runner，整次以 `max(檢查碼, 2)` 結束；結果與下一步見訊息表
- 使用者依[設定](#設定)在 `[test]` 指定 `image` 與 `command`，VK 不內建 runner
- 通過檢查後，在該 image 容器執行 command 並在最後加上 path，不經 shell；工作目錄為安裝目錄，repo 唯讀掛載，以空目錄遮住 `.vendor_kit/`，runner 另有容器內的可寫暫存空間，結束即丟，寫不進 repo
- 測試 image 不限 registry，由主機 Docker 取得，也可用本機 image；image 與 command 實際執行什麼由使用者負責
- runner 的 stdout、stderr 原樣轉出，格式界線見 [03 輸出](../../contract/03_output.md#輸出)
- path 無效、未選到測試、選到工具交付檔、runner 起不來或測試未通過的處置與結束碼，見[訊息表](../../contract/reason_codes.csv)

