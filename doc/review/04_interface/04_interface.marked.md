<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除，程式碼區塊的改動改成 diff 區塊（+ 新增、- 刪除）；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit 5770e20。正式內容看 /doc/contract/04_interface.md -->

# 04 使用者介面

<mark style="background-color:#f8c8c8">[使用者](../../../GLOSSARY.md#角色與情境)與自動化都透過 `just vendor_kit` 指令跟 [VK](../../../GLOSSARY.md#角色與情境) 打交道；只有首次[導入](../../../GLOSSARY.md#角色與情境)，以及[薄殼](../../../GLOSSARY.md#vk-組件)的檢查與明確要求的修復，用 `sh bootstrap.sh`。這一頁列出全部指令與必要的參數、選項：少了就不能用、或會影響相容性的才列；其他選項的細節實作時再定。VK 不讀取環境變數 `CI`；同一個 recipe 不論在哪裡執行，行為都一樣。這是 VK 自己的規則：環境只影響主機條件與能否回答詢問，不改變檢查或保護程度。</mark>
<mark style="background-color:#c8f0c8">[使用者](../../../GLOSSARY.md#角色與情境)與自動化平常用 `just vendor_kit` 操作 [VK](../../../GLOSSARY.md#角色與情境)。`bootstrap.sh` 只用於首次[導入](../../../GLOSSARY.md#角色與情境)，以及[薄殼](../../../GLOSSARY.md#vk-組件)的檢查與明確要求的修復。</mark>

- <mark style="background-color:#f8c8c8">必須永遠成立的規則以 [02 不變量](../../contract/02_invariants.md) 為準，這一頁只補使用者看得到的介面行為</mark>
- <mark style="background-color:#f8c8c8">[結束碼](../../../GLOSSARY.md#執行與結果)的意思與每條訊息見 [03 輸出](../../contract/03_output.md)</mark>
- <mark style="background-color:#f8c8c8">名詞見[名詞表](../../../GLOSSARY.md)</mark>
<mark style="background-color:#c8f0c8">這一頁列必要的參數、選項與操作流程；其他選項細節留到實作時定。</mark>

## 目錄

- [主機需求](#主機需求)
- [registry 與認證](#registry-與認證)
- <mark style="background-color:#c8f0c8">[共同選項](#共同選項)</mark>
- [入口](#入口)
- [bootstrap.sh](#bootstrapsh)
- [指令](#指令)
- <mark style="background-color:#f8c8c8">[共同選項](#共同選項)</mark>
- [各指令專用選項](#各指令專用選項)
- [追蹤新版](#追蹤新版)
- [輸出](#輸出)
- [使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
- [檢查 (test)](#檢查-test)

## 主機需求

<mark style="background-color:#f8c8c8">依 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)，支援平台本來就有的這些不算在主機依賴內：</mark>
<mark style="background-color:#c8f0c8">依 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)，bash 是支援平台既有的 shell。主機另需：</mark>

- <mark style="background-color:#f8c8c8">POSIX sh 與它的內建指令</mark>
- <mark style="background-color:#f8c8c8">基礎 userland：`grep`、`sed`、`id`、`mktemp`、`mkdir`、`date`、`rm`、`sleep`、`od`、`tr`</mark>
| <mark style="background-color:#c8f0c8">主機程式</mark> | <mark style="background-color:#c8f0c8">最低版本</mark> | <mark style="background-color:#c8f0c8">使用方式</mark> |
|---|---|---|
| <mark style="background-color:#c8f0c8">[Docker](https://www.docker.com/)</mark> | <mark style="background-color:#c8f0c8">19.03</mark> | <mark style="background-color:#c8f0c8">不支援 Podman；[啟動器](../../../GLOSSARY.md#vk-組件)在首次導入與既有[安裝目錄](../../../GLOSSARY.md#工具與出貨)都檢查</mark> |
| <mark style="background-color:#c8f0c8">[Git](https://git-scm.com/)</mark> | <mark style="background-color:#c8f0c8">不設最低版本</mark> | <mark style="background-color:#c8f0c8">VK 不在主機呼叫 git；啟動器往上找 `.git`，確認位於 git [repo](../../../GLOSSARY.md#工具與出貨) 內；目錄或檔都算，適用 worktree 與 submodule</mark> |
| <mark style="background-color:#c8f0c8">[just](https://github.com/casey/just)</mark> | <mark style="background-color:#c8f0c8">1.33.0</mark> | <mark style="background-color:#c8f0c8">首次導入檢查；使用 [just Release 下載頁](https://github.com/casey/just/releases/latest)的版本</mark> |

<mark style="background-color:#f8c8c8">除此之外，主機只需要這三個：</mark>
| <mark style="background-color:#f8c8c8">主機程式</mark> | <mark style="background-color:#f8c8c8">最低版本</mark> | <mark style="background-color:#f8c8c8">說明</mark> | <mark style="background-color:#f8c8c8">版本不足時</mark> |
|---|---|---|---|
| <mark style="background-color:#f8c8c8">[Docker](https://www.docker.com/)</mark> | <mark style="background-color:#f8c8c8">19.03 以上</mark> | <mark style="background-color:#f8c8c8">不支援 Podman；偵測到 Podman 時由[啟動器](../../../GLOSSARY.md#vk-組件)以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，訊息見 [訊息](../../contract/reason_codes.csv) `VK0011`</mark> | <mark style="background-color:#f8c8c8">由啟動器檢查，首次導入與已有[安裝目錄](../../../GLOSSARY.md#工具與出貨)都一樣：在任何寫入之前以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，訊息見 [訊息](../../contract/reason_codes.csv) `VK0012`</mark> |
| <mark style="background-color:#f8c8c8">[Git](https://git-scm.com/)</mark> | <mark style="background-color:#f8c8c8">不設最低版本</mark> | <mark style="background-color:#f8c8c8">VK 不在主機上呼叫 git；「安裝目錄在 git [repo](../../../GLOSSARY.md#工具與出貨) 裡」由啟動器用 sh 往上找 `.git` 判斷；`.git` 是目錄或檔都算，所以 worktree 與 submodule 也適用</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">[just](https://github.com/casey/just)</mark> | <mark style="background-color:#f8c8c8">1.33.0 以上</mark> | <mark style="background-color:#f8c8c8">用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)</mark> | <mark style="background-color:#f8c8c8">首次導入：`bootstrap.sh` 以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，訊息見 [訊息](../../contract/reason_codes.csv) `VK0005`。已有安裝目錄：由 just 自己報錯，見下方的註</mark> |
<mark style="background-color:#f8c8c8">註：just 版本不足時</mark>
- <mark style="background-color:#f8c8c8">首次導入：`bootstrap.sh` 在任何寫入之前以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，另印下載與安裝指令，訊息見 [訊息](../../contract/reason_codes.csv) `VK0005`</mark>
- <mark style="background-color:#f8c8c8">已有安裝目錄：justfile 用了 just 1.33.0 才支援的寫法，just 太舊時讀 justfile 就會出錯，輪不到 VK 執行，也就沒機會檢查版本；這時看到的是 just 自己的錯誤訊息與結束碼，VK 不留[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)</mark>
<mark style="background-color:#c8f0c8">主機前置檢查不通過時的處置見[訊息表](../../contract/reason_codes.csv)。已有安裝目錄若使用太舊的 just，會在讀取 justfile 時由 just 自己報錯，尚未進入 VK，也不留[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)。</mark>

## registry 與認證

<mark style="background-color:#f8c8c8">依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)，認證由主機與 CI 各自處理：在支援的 [registry](../../../GLOSSARY.md#工具與出貨) 上，主機的 docker 拉得到的 image，VK 就用得了。</mark>
<mark style="background-color:#c8f0c8">[工具 image](../../../GLOSSARY.md#工具與出貨) 與[引擎 image](../../../GLOSSARY.md#工具與出貨) 的 [registry](../../../GLOSSARY.md#工具與出貨) 支援範圍：</mark>

- <mark style="background-color:#f8c8c8">支援的 registry 目前只有 GitHub 的 image 伺服器 (GHCR)。沒列在這份清單上的 registry（例如 Docker Hub、GitLab、自架）不在承諾內</mark>
- <mark style="background-color:#f8c8c8">[引擎 image](../../../GLOSSARY.md#工具與出貨) 公開；[工具 image](../../../GLOSSARY.md#工具與出貨) 公開或私有，由[出貨](../../../GLOSSARY.md#角色與情境)那個 repo 自己決定</mark>
- <mark style="background-color:#f8c8c8">沒有給憑證時，不支援需要認證的版本列舉：對那個工具以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，印出兩條路，訊息見 [訊息](../../contract/reason_codes.csv) `VK0001`</mark>
  - <mark style="background-color:#f8c8c8">設定 `VENDOR_KIT_REGISTRY_TOKEN`（或 `VENDOR_KIT_REGISTRY_TOKEN_FILE`）</mark>
  - <mark style="background-color:#f8c8c8">直接指定版本 `@<tag>`</mark>
- <mark style="background-color:#c8f0c8">支援：GitHub Container Registry (GHCR)</mark>
- <mark style="background-color:#c8f0c8">不支援：Docker Hub、Quay、GitLab Container Registry、自架 registry、其他</mark>

<mark style="background-color:#f8c8c8">這是 VK 自己的認證規則：`@<tag>` 只省掉列版本，拉 image 仍使用主機 Docker 的憑證，不保證免認證。VK 不在執行中要求輸入帳號、密碼或 token；網路逾時與重試細節留到實作時定。`update`、`add`、`upgrade` 列 [tag](../../../GLOSSARY.md#工具與出貨) 或取工具 image 時，逾時或其他存取失敗以 `VK0055`／`2` 結束；`sync` 取工具 image 的網路、registry 或認證失敗也用 `VK0055`／`2`。啟動器取不到引擎 image 照 `VK0036`／`2`，缺少列版本憑證仍照 `VK0001`。</mark>
<mark style="background-color:#c8f0c8">引擎 image 公開；工具 image 是否公開，由[出貨](../../../GLOSSARY.md#角色與情境)的 repo 決定。測試用 image 的範圍另見[檢查 (test)](#檢查-test)。</mark>

| <mark style="background-color:#c8f0c8">動作</mark> | <mark style="background-color:#c8f0c8">用誰的憑證</mark> | <mark style="background-color:#c8f0c8">沒有或不夠時</mark> |
|---|---|---|
| <mark style="background-color:#c8f0c8">查版本清單 (`update`、`add`、`upgrade <repo>`)</mark> | <mark style="background-color:#c8f0c8">公開不必設定；私有用 `--registry-token-file <path>`，帳號須有讀取權限</mark> | <mark style="background-color:#c8f0c8">沒有憑證時，可加選項重跑，或用 `<repo>@<tag>` 直接指定版本</mark> |
| <mark style="background-color:#c8f0c8">下載 image (`add`、`upgrade`、`sync`、啟動器)</mark> | <mark style="background-color:#c8f0c8">主機或 CI 的 Docker；私有 image 先 `docker login ghcr.io`</mark> | <mark style="background-color:#c8f0c8">Docker 沒有足夠讀取權限就無法下載</mark> |

- <mark style="background-color:#c8f0c8">兩邊憑證不互通</mark>
- <mark style="background-color:#c8f0c8">`@<tag>` 只省掉查版本清單，不省掉下載認證</mark>
- <mark style="background-color:#c8f0c8">VK 不在執行中要求帳號、密碼或 token</mark>
- <mark style="background-color:#c8f0c8">認證與存取失敗的訊息見[訊息表](../../contract/reason_codes.csv)；token 被拒後不改走匿名重試</mark>
- <mark style="background-color:#c8f0c8">網路逾時與重試細節留到實作時定</mark>

## 共同選項
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#c8f0c8">兩個入口共用的選項先列在這裡；是否接受仍依各入口與指令的規則。</mark>

| <mark style="background-color:#c8f0c8">選項</mark> | <mark style="background-color:#c8f0c8">用途</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`-h` / `--help`</mark> | <mark style="background-color:#c8f0c8">顯示該入口或指令的用法；實際 help 輸出是唯一來源</mark> |
| <mark style="background-color:#c8f0c8">`-i` / `--image <image>`</mark> | <mark style="background-color:#c8f0c8">指定本機 image 或 image tar；可用組合見[離線導入](#離線導入)及[本機覆寫](#本機覆寫)</mark> |
| <mark style="background-color:#c8f0c8">`-y` / `--yes`</mark> | <mark style="background-color:#c8f0c8">預先回答允許的[詢問](../../../GLOSSARY.md#執行與結果)，適用範圍見下方</mark> |

<mark style="background-color:#c8f0c8">[-y](../../../GLOSSARY.md#執行與結果) 只適用於[可寫 recipe](../../../GLOSSARY.md#執行與結果)。已定組合為 `upgrade <repo> -y`、`upgrade --engine -y`（含 `--engine=<tag>`）、`install -y`，以及由 `bootstrap.sh` 首次導入時傳給 `install`；只檢查與修復不接受。</mark>

- <mark style="background-color:#c8f0c8">授權界線依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)；它只省略詢問，改動仍印到 stdout</mark>
- <mark style="background-color:#c8f0c8">其餘指令是否依「可能詢問才接受」收斂，待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)</mark>
- <mark style="background-color:#c8f0c8">stdin 與 stderr 都是終端 (TTY) 才能互動；管線不算，不另從 `/dev/tty` 讀答案</mark>
- <mark style="background-color:#c8f0c8">提示為 `[y/N]`，印到 stderr；答案從 stdin 讀，空白 Enter 等於否，EOF 不算同意</mark>
- <mark style="background-color:#c8f0c8">沒帶 `-y` 又不能互動時，不做需詢問的修改；重跑方式、[診斷](../../../GLOSSARY.md#執行與結果)與[結束碼](../../../GLOSSARY.md#執行與結果)見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">每次呼叫先問完所有問題，全部同意才寫入（執行紀錄除外），含恢復舊操作；答否的正常取消輸出見 [03 輸出](../../contract/03_output.md#輸出)</mark>
- <mark style="background-color:#c8f0c8">詢問中 Ctrl-C 不算同意；最終碼受 just 與外層訊號處理影響</mark>
- <mark style="background-color:#c8f0c8">拒絕記錄的保存方式仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)</mark>

## 入口

<mark style="background-color:#f8c8c8">VK 對外只有兩個入口：</mark>
| <mark style="background-color:#c8f0c8">入口</mark> | <mark style="background-color:#c8f0c8">用途</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`bootstrap.sh`</mark> | <mark style="background-color:#c8f0c8">首次導入、薄殼檢查與修復</mark> |
| <mark style="background-color:#c8f0c8">`just vendor_kit <cmd>`</mark> | <mark style="background-color:#c8f0c8">日常與 CI 操作；`<cmd>` 換成要執行的 [VK recipe](../../../GLOSSARY.md#執行與結果) 名稱，例如 `update`、`add`、`upgrade`</mark> |

- <mark style="background-color:#f8c8c8">`sh bootstrap.sh`</mark>
  - <mark style="background-color:#f8c8c8">首次導入、檢查與修復薄殼，見下方的 [bootstrap.sh](#bootstrapsh)</mark>
  - <mark style="background-color:#f8c8c8">先從 [VK 的 Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)下載，再到要裝 VK 或已有 VK 的目錄執行</mark>
  - <mark style="background-color:#f8c8c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，Release 頁上目前還沒有這個檔</mark>
- <mark style="background-color:#f8c8c8">`just vendor_kit …`</mark>
  - <mark style="background-color:#f8c8c8">日常使用的全部指令；CI 也用它，見下面的[檢查 (test)](#檢查-test)</mark>
  - <mark style="background-color:#f8c8c8">都收在 `vendor_kit` 這個命名空間底下，不佔用 [repo](../../../GLOSSARY.md#工具與出貨) 自己的頂層指令名</mark>
<mark style="background-color:#c8f0c8">`bootstrap.sh` 是啟動器，每個 Release 各附一份，檔名固定，版本在下載路徑。取得與執行流程：</mark>

1. <mark style="background-color:#c8f0c8">在 [VK Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)選版本；把下面的 `vX.Y.Z` 換成選定版號；本頁的 `vX` 指 `vX.Y.Z` 的 X。含此資產的 Release 尚未發布前，流程尚不可用。</mark>

   ```diff
   +vk_version=vX.Y.Z
   ```

2. <mark style="background-color:#c8f0c8">從該版 Release 下載 `bootstrap.sh` 到目前目錄；下載失敗時以非零結束，不繼續執行後續步驟。</mark>

   ```diff
   +wget -O bootstrap.sh "https://github.com/ycpss91255-research/vendor_kit/releases/download/${vk_version}/bootstrap.sh" || exit $?
   +vk_bootstrap="$PWD/bootstrap.sh"
   ```

3. <mark style="background-color:#c8f0c8">賦予執行權限。</mark>

   ```diff
   +chmod +x "$vk_bootstrap"
   ```

4. <mark style="background-color:#c8f0c8">把 `<目標目錄>` 換成要導入或已有 VK 的目錄，再執行。腳本以 `#!/usr/bin/env bash` 開頭。</mark>

   ```diff
   +cd <目標目錄>
   +"$vk_bootstrap"
   ```

## bootstrap.sh

<mark style="background-color:#f8c8c8">`bootstrap.sh` 是啟動器之一；首次導入時取得內嵌那一版[引擎](../../../GLOSSARY.md#vk-組件)，再呼叫 `install`（把 VK 裝進目前目錄）。在既有安裝目錄則依[版本鎖定行](../../../GLOSSARY.md#版本與來源)指定的引擎模板，檢查或重產薄殼。它不執行 repo 內的薄殼，也不從薄殼讀取版本或模板；薄殼內容只用於逐檔比對。</mark>
| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">正常行為</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">首次導入（可帶 `-i`、`-y`），或未完成的首次導入</mark> | <mark style="background-color:#c8f0c8">取得內嵌那版[引擎](../../../GLOSSARY.md#vk-組件)（帶 `-i` 時改用指定的本機 image），呼叫 `install` 導入目前目錄</mark> |
| <mark style="background-color:#c8f0c8">不帶選項，既有安裝目錄</mark> | <mark style="background-color:#c8f0c8">只檢查薄殼；一致時報告一致</mark> |
| <mark style="background-color:#c8f0c8">`--repair`，既有安裝目錄</mark> | <mark style="background-color:#c8f0c8">一致則不重產；不符則先逐檔列差異，再重產並報告結果，不詢問</mark> |
| <mark style="background-color:#c8f0c8">單獨 `-h` / `--help`</mark> | <mark style="background-color:#c8f0c8">只印用法，不做主機檢查、不寫檔，不印內嵌引擎版本</mark> |

```diff
-Usage: sh bootstrap.sh [options]
```
- <mark style="background-color:#c8f0c8">不收位置參數，沒有 `--version`；短長選項同義，順序不限，`--repair` 只有長選項</mark>
- <mark style="background-color:#c8f0c8">`-h` / `--help` 只准單獨使用；`-y` 只在首次導入傳給 `install`，任何情況都不接受 `--repair -y`</mark>
- <mark style="background-color:#c8f0c8">首次導入的寫入、詢問與檔案處理見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)</mark>
- <mark style="background-color:#c8f0c8">用法、主機條件、鎖定行、引擎取得與薄殼不符的診斷及結束碼，統一見[訊息表](../../contract/reason_codes.csv)的 `source` 含 `bootstrap` 的列</mark>

```diff
-  (no arguments)       Perform initial import outside an install directory or when initial import is incomplete; otherwise, check shell files only
-  -i, --image <image>  Use a local image or image tar as the engine source
-  --repair             Regenerate shell files from the locked engine's templates
-  -y, --yes            Pass to install during initial import to answer permitted prompts
-  -h, --help           Print usage when used alone
```
### 首次導入還是既有安裝目錄
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#f8c8c8">不收位置參數，也沒有 `--version`；依 [VK 的 Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)版號選擇 `bootstrap.sh`，沿用 [bootstrap 介面決議](https://github.com/ycpss91255-research/vendor_kit/issues/107)的作業前提。短長選項意思相同，選項順序不限；`--repair` 只有長選項。`-h`／`--help` 只准單獨使用，不印內嵌引擎版本；與任何其他參數並用都算用法錯誤。這是 VK 自己的規則：並用時不替使用者選擇要執行還是只看用法。只檢查與修復都不詢問，因此不接受 `-y`，避免把它誤當成寫入授權。</mark>
<mark style="background-color:#c8f0c8">目前目錄沒有 `.vendor_kit/` 才是首次導入；有就按既有安裝目錄處理。讀不出恰好一行有效的引擎[版本鎖定行](../../../GLOSSARY.md#版本與來源)時，不猜版本或改走首次導入，處置見[訊息表](../../contract/reason_codes.csv)。</mark>

<mark style="background-color:#f8c8c8">目前目錄有 `.vendor_kit/` 就是安裝目錄；沒有才首次導入。有 `.vendor_kit/` 卻讀不出恰好一行有效的引擎版本鎖定行時，停下報 `VK0037`，不猜版本，也不改走首次導入；唯一例外是未完成的首次導入：這個安裝目錄最近一筆執行紀錄是首次導入、停在 `VK0002`，且除執行紀錄外未修改任何檔；或最近一筆執行紀錄是首次導入，且在建紀錄之後、寫入引擎版本鎖定行之前就結束（不論是否已寫入其他檔）。符合例外時仍按首次導入處理，允許帶 `-y` 重跑；讀得出恰好一行有效的引擎版本鎖定行時，一律是既有安裝目錄，不套用例外。判定靠執行紀錄，不靠 `.vendor_kit/` 裡有哪些檔；啟動器只用字串相等比對最近一筆執行紀錄裡固定記下的欄位：模式是首次導入，且原因代碼是 `VK0002`、除執行紀錄外未修改任何檔，或結束階段在建紀錄之後、寫入引擎版本鎖定行之前。比對不出來或紀錄不足以唯一判定時，不套用例外。這是 VK 自己的規則：只看檔案在不在，會把檔被刪掉的舊安裝目錄誤認成首次導入。在這個未完成狀態下，用法錯誤或帶 `--repair` 而中途結束的執行不建紀錄，不改變例外判定所用的最近一筆執行紀錄。</mark>
<mark style="background-color:#c8f0c8">唯一例外是未完成的首次導入：允許重跑首次導入，也可帶 `-y`；條件是最近一筆執行紀錄是首次導入，且符合任一條件：</mark>

<mark style="background-color:#f8c8c8">既有安裝目錄的檢查與修復一律使用版本鎖定行那一版引擎，不套用[本機覆寫](../../../GLOSSARY.md#版本與來源)：`bootstrap.sh` 是在 VK 本身可能壞掉時用的入口，以進 git 的鎖定行為準。`-i` 跟首次導入一樣接受已載入的本機 image 或 image tar；兩者都必須符合引擎版本鎖定行的 [digest](../../../GLOSSARY.md#工具與出貨)，缺少必要的 digest 資訊或 digest 不符時報 `VK0031`。以 [image 引用](../../../GLOSSARY.md#工具與出貨)指定時，完整引用也必須與鎖定行相同，引用不符但 digest 相符時報 `VK0038`。</mark>
- <mark style="background-color:#c8f0c8">因需詢問、沒帶 `-y` 又不能互動（含 EOF）而停下，除紀錄外未修改任何檔</mark>
- <mark style="background-color:#c8f0c8">建紀錄後、寫入引擎版本鎖定行前結束，不論是否已寫入其他檔</mark>

<mark style="background-color:#f8c8c8">`bootstrap.sh` 只保證跟同 X 的鎖定引擎一起用；內嵌引擎與版本鎖定行指定的引擎跨 X 時，在任何寫入之前停下（包括不建執行紀錄），報版本組合不合，以結束碼 `3` 結束，訊息說明要換成與鎖定引擎同 X 的 `bootstrap.sh`。這是 VK 自己的保守規則：跨 X 不代表一定不相容，但不能假定原本的啟動流程仍有效。</mark>
<mark style="background-color:#c8f0c8">例外判定：</mark>

<mark style="background-color:#f8c8c8">依情況的行為</mark>
- <mark style="background-color:#c8f0c8">讀得出有效引擎版本鎖定行，就不套用例外</mark>
- <mark style="background-color:#c8f0c8">依最近一筆執行紀錄判定是否符合上述條件，不靠目錄內有哪些檔</mark>
- <mark style="background-color:#c8f0c8">紀錄不足以唯一判定就不套用；此狀態的用法錯誤或 `--repair` 呼叫不建紀錄，不改變判定用的最近一筆紀錄</mark>

<mark style="background-color:#f8c8c8">表中的[原因代碼](../../../GLOSSARY.md#執行與結果)見 [03 訊息](../../contract/reason_codes.csv)；表中的[診斷](../../../GLOSSARY.md#執行與結果)除跨 X 為 `fatal`、結束碼 `3` 外，都是 `error`、結束碼 `2`，印到 stderr，stdout 不印診斷；處置值只有 `pending`（[待處理](../../../GLOSSARY.md#執行與結果)）、`failed`（[失敗](../../../GLOSSARY.md#執行與結果)）或留空，用法錯誤的處置留空，見[訊息表](../../contract/reason_codes.csv)。成功的用法、差異與結果印到 stdout，不加診斷前綴。</mark>
### 用哪一版引擎
<mark style="background-color:#c8f0c8">（本節新增）</mark>

| <mark style="background-color:#f8c8c8">情況</mark> | <mark style="background-color:#f8c8c8">行為</mark> | <mark style="background-color:#f8c8c8">結束碼</mark> | <mark style="background-color:#f8c8c8">原因代碼</mark> | <mark style="background-color:#f8c8c8">stdout／stderr</mark> |
|---|---|---|---|---|
| <mark style="background-color:#f8c8c8">單獨帶 `-h`／`--help`</mark> | <mark style="background-color:#f8c8c8">只印用法，不做主機檢查、不寫檔</mark> | <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">stdout：用法</mark> |
| <mark style="background-color:#f8c8c8">不認得的選項、多出位置參數，或 `-h`／`--help` 與其他參數並用</mark> | <mark style="background-color:#f8c8c8">用法錯誤，不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0026`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與簡短用法</mark> |
| <mark style="background-color:#f8c8c8">`-i`／`--image` 缺值</mark> | <mark style="background-color:#f8c8c8">用法錯誤，不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0025`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與簡短用法</mark> |
| <mark style="background-color:#f8c8c8">既有安裝目錄帶 `-y`／`--yes`（上述未完成的首次導入例外除外），或任何情況帶 `--repair -y`</mark> | <mark style="background-color:#f8c8c8">用法錯誤，不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0026`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與簡短用法</mark> |
| <mark style="background-color:#f8c8c8">找不到 docker</mark> | <mark style="background-color:#f8c8c8">主機前置檢查失敗</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0033`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">偵測到 Podman</mark> | <mark style="background-color:#f8c8c8">主機前置檢查失敗</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0011`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">Docker 低於 19.03</mark> | <mark style="background-color:#f8c8c8">主機前置檢查失敗</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0012`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">首次導入找不到 just</mark> | <mark style="background-color:#f8c8c8">主機前置檢查失敗，附下載與安裝指令</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0034`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與下載、安裝指令</mark> |
| <mark style="background-color:#f8c8c8">首次導入 just 低於 1.33.0</mark> | <mark style="background-color:#f8c8c8">主機前置檢查失敗，附下載與安裝指令</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0005`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與下載、安裝指令</mark> |
| <mark style="background-color:#f8c8c8">往上找不到 `.git`</mark> | <mark style="background-color:#f8c8c8">不寫檔，也不建立 repo</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0035`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">非安裝目錄帶 `--repair`</mark> | <mark style="background-color:#f8c8c8">停下，不改走首次導入、不建紀錄、不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0039`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">有 `.vendor_kit/`，但讀不出恰好一行有效的引擎版本鎖定行，且不屬上述未完成的首次導入例外；帶 `--repair` 時即使符合例外也同樣處理</mark> | <mark style="background-color:#f8c8c8">停下，不改走首次導入、不建紀錄、不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0037`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">鎖定引擎與 `bootstrap.sh` 內嵌引擎跨 X</mark> | <mark style="background-color:#f8c8c8">任何寫入之前停下，指出要換哪個 X 的 `bootstrap.sh`</mark> | <mark style="background-color:#f8c8c8">`3`</mark> | <mark style="background-color:#f8c8c8">`VK0040`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">既有安裝目錄帶 `-i`，本機 image 或 image tar 缺必要的 digest 資訊，或 digest 與鎖定行不符</mark> | <mark style="background-color:#f8c8c8">停下，不用這個 image</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0031`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">既有安裝目錄以 [image 引用](../../../GLOSSARY.md#工具與出貨)帶 `-i`，digest 相符但完整 image 引用與鎖定行不同</mark> | <mark style="background-color:#f8c8c8">停下，不用這個 image</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0038`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">首次導入、只檢查或 `--repair`，建不出執行紀錄</mark> | <mark style="background-color:#f8c8c8">停下，不拉 image、不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0010`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">取不到要用的引擎 image</mark> | <mark style="background-color:#f8c8c8">停下，不改用其他版本</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0036`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">首次導入帶 `-i`，缺必要的 digest 資訊</mark> | <mark style="background-color:#f8c8c8">停下，不退化成只寫 [tag](../../../GLOSSARY.md#工具與出貨)</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0031`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">首次導入，上層或下層已有安裝目錄</mark> | <mark style="background-color:#f8c8c8">拒絕巢狀安裝，不寫檔</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0029`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷</mark> |
| <mark style="background-color:#f8c8c8">首次導入需要詢問，沒帶 `-y` 且不能互動</mark> | <mark style="background-color:#f8c8c8">除執行紀錄外不修改；依紀錄按未完成的首次導入處理，允許帶 `-y` 重跑</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0002`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與加上 `-y` 的原指令</mark> |
| <mark style="background-color:#f8c8c8">首次導入，其餘情況</mark> | <mark style="background-color:#f8c8c8">取得內嵌那版引擎並呼叫 `install`</mark> | <mark style="background-color:#f8c8c8">照 `install`</mark> | <mark style="background-color:#f8c8c8">照 `install`</mark> | <mark style="background-color:#f8c8c8">照 `install`</mark> |
| <mark style="background-color:#f8c8c8">只檢查或 `--repair`，發現升引擎未完成的[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)</mark> | <mark style="background-color:#f8c8c8">停下，不報薄殼不符、不重產；下一步是重跑原本的 `upgrade` 指令，保留原 [tag](../../../GLOSSARY.md#工具與出貨) 與 `-y`</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0023`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與完整原指令</mark> |
| <mark style="background-color:#f8c8c8">既有安裝目錄，不帶 `--repair`，薄殼一致</mark> | <mark style="background-color:#f8c8c8">只檢查</mark> | <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">stdout：一致</mark> |
| <mark style="background-color:#f8c8c8">既有安裝目錄，不帶 `--repair`，薄殼被改過或與模板不符</mark> | <mark style="background-color:#f8c8c8">停下，不重產</mark> | <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">`VK0006`</mark> | <mark style="background-color:#f8c8c8">stderr：診斷與逐檔差異續行</mark> |
| <mark style="background-color:#f8c8c8">`--repair`，薄殼一致</mark> | <mark style="background-color:#f8c8c8">不重產</mark> | <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">stdout：已一致，未重產</mark> |
| <mark style="background-color:#f8c8c8">`--repair`，薄殼不符</mark> | <mark style="background-color:#f8c8c8">不詢問；寫入前逐檔列差異，再重產並報告結果</mark> | <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">stdout：差異與完成報告</mark> |
| <mark style="background-color:#c8f0c8">模式</mark> | <mark style="background-color:#c8f0c8">引擎來源</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">首次導入</mark> | <mark style="background-color:#c8f0c8">腳本內嵌那一版；`-i <image>` 可改用離線交付</mark> |
| <mark style="background-color:#c8f0c8">既有安裝目錄的檢查、修復</mark> | <mark style="background-color:#c8f0c8">引擎版本鎖定行那一版，不套用[本機覆寫](../../../GLOSSARY.md#版本與來源)</mark> |

<mark style="background-color:#f8c8c8">先判定目前目錄是否有 `.vendor_kit/`；有且讀不出恰好一行有效的引擎版本鎖定行時，才依最近一筆既有執行紀錄辨識上述未完成的首次導入例外，以判定是否接受 `-y`；再判用法、做主機前置檢查。往上找 `.git`、首次導入的巢狀檢查、非安裝目錄帶 `--repair` (`VK0039`)，以及上述未完成狀態帶 `--repair` (`VK0037`)，都在建紀錄之前判定，拒絕時不建紀錄、不寫檔。既有安裝目錄在建執行紀錄或取得 image 之前先檢查是否跨 X；只檢查與 `--repair` 都在比對薄殼之前辨識升引擎未完成的進度檔，若有則依表中行為停下，不進入後續薄殼檢查或重產。首次導入、只檢查與修復都檢查 docker；just 只在首次導入檢查，另外兩種模式不經過 just。VK 不在主機呼叫 git，只用 sh 往上找 `.git`；它是目錄或檔都算。</mark>
<mark style="background-color:#c8f0c8">既有安裝目錄帶 `-i` 可用本機 image 或 image tar，但 [digest](../../../GLOSSARY.md#工具與出貨) 必須符合鎖定行；以 [image 引用](../../../GLOSSARY.md#工具與出貨)指定時，完整引用也須相同。</mark>

<mark style="background-color:#c8f0c8">腳本只保證與同一個 vX 的鎖定引擎一起用；跨 vX 時須換用對應 vX 的腳本。拒絕結果見[訊息表](../../contract/reason_codes.csv)。</mark>

### 判定順序
<mark style="background-color:#c8f0c8">（本節新增）</mark>

1. <mark style="background-color:#c8f0c8">先看 `.vendor_kit/` 與有效鎖定行，必要時依既有執行紀錄辨識未完成首次導入，以判定是否接受 `-y`</mark>
2. <mark style="background-color:#c8f0c8">判用法、檢查主機；首次導入、只檢查、`--repair` 都檢查 Docker，just 只在首次導入檢查，git 位置見[主機需求](#主機需求)</mark>
3. <mark style="background-color:#c8f0c8">建紀錄前判定跨 vX、git 位置、首次導入的巢狀安裝、非安裝目錄的 `--repair`，以及不適用例外的無效鎖定行；被拒絕時不建紀錄、不寫檔</mark>
4. <mark style="background-color:#c8f0c8">依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)建執行紀錄，再取得 image、啟動引擎；首次導入在呼叫 `install` 前建好，只檢查與修復在比對前建好</mark>
5. <mark style="background-color:#c8f0c8">只檢查與修復先辨識升引擎未完成的[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)；有就依訊息表的下一步重跑原 `upgrade`，不比對或重產薄殼</mark>

### 寫入範圍與其他指令的關係

- <mark style="background-color:#f8c8c8">首次導入的寫入範圍、詢問與輸出照 `install`，見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)。`-y` 只在首次導入傳給 `install`，語意照[共同選項](#共同選項)</mark>
- <mark style="background-color:#f8c8c8">首次導入、只檢查與 `--repair` 都先建執行紀錄，再拉 image、起引擎；首次導入在呼叫 `install` 之前就建好紀錄，只檢查與修復則在比對前建好。建不出紀錄時報 `VK0010`，不拉 image、不寫檔。用法錯誤、主機前置檢查失敗、跨 X、往上找不到 `.git` (`VK0035`)、拒絕巢狀 (`VK0029`)、非安裝目錄帶 `--repair` (`VK0039`)，以及有 `.vendor_kit/` 卻讀不出有效鎖定行且不套用例外（含上述未完成狀態帶 `--repair`，`VK0037`），都在建紀錄之前判定，不建紀錄、不寫檔。執行紀錄規則見 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark>
- <mark style="background-color:#f8c8c8">`sh bootstrap.sh --repair` 是使用者明確打的指令，寫入薄殼檔符合 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化不寫追蹤檔)「使用者明確打的 recipe 才寫得到」的意思。只檢查除執行紀錄外不寫檔。`--repair` 除執行紀錄外只重產 `.vendor_kit/` 下的四檔：`entry.just`、`vendor.just`、`log.sh`、`.gitignore`；已一致則不重產</mark>
- <mark style="background-color:#f8c8c8">檢查與修復不改版本鎖定行或其他檔，包括 VK 的設定檔、[metadata](../../../GLOSSARY.md#初始檔與合併)、[基準版](../../../GLOSSARY.md#初始檔與合併)、[納管](../../../GLOSSARY.md#初始檔與合併)紀錄、[印記](../../../GLOSSARY.md#repo-內的檔與狀態)、[cache/](../../../GLOSSARY.md#repo-內的檔與狀態)、[gen/](../../../GLOSSARY.md#repo-內的檔與狀態)、[本機覆寫](../../../GLOSSARY.md#版本與來源)、[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)、根 `justfile`、根 `.dockerignore`、使用者檔與 `bootstrap.sh` 本身</mark>
- <mark style="background-color:#f8c8c8">`--repair` 不經過 `install`，不建立安裝目錄，也不補做其他安裝步驟；它只恢復鎖定引擎的薄殼，不更換引擎版本。這是 VK 自己的規則：既有安裝目錄的預設用途是救援檢查，要重產必須明確帶 `--repair`</mark>
- <mark style="background-color:#f8c8c8">首次導入的 `-i <image>` 照[離線導入共通規則](#各指令專用選項)；既有安裝目錄的本機 image 或 image tar 須符合上面的 digest 與引用規則，再照原本的檢查或修復行為執行</mark>
- <mark style="background-color:#f8c8c8">[救援路徑](../../../GLOSSARY.md#介面版與契約)分兩類：版本組合不合時用[說明與用法錯誤](#說明與用法錯誤)列出的 just 呼叫；薄殼被改過時用 `sh bootstrap.sh` 檢查、`sh bootstrap.sh --repair` 修復</mark>
<mark style="background-color:#c8f0c8">除執行紀錄外：</mark>

| <mark style="background-color:#c8f0c8">模式</mark> | <mark style="background-color:#c8f0c8">寫入範圍</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">只檢查</mark> | <mark style="background-color:#c8f0c8">不寫檔</mark> |
| <mark style="background-color:#c8f0c8">`--repair`</mark> | <mark style="background-color:#c8f0c8">只重產 `.vendor_kit/` 下的 `entry.just`、`vendor.just`、`log.sh`、`.gitignore`；一致則不重產</mark> |

- <mark style="background-color:#c8f0c8">不執行 repo 內的薄殼，也不從薄殼讀版本或模板；薄殼只用於逐檔比對</mark>
- <mark style="background-color:#c8f0c8">`--repair` 不經過 `install`，不補其他安裝步驟，不改鎖定行、設定、根目錄檔或其他狀態，也不改腳本本身</mark>
- <mark style="background-color:#c8f0c8">[救援路徑](../../../GLOSSARY.md#介面版與契約)分兩類：薄殼被改過用此入口檢查或修復；版本組合不合用[說明與用法錯誤](#說明與用法錯誤)列出的 just 呼叫</mark>

## 指令

<mark style="background-color:#f8c8c8">第一版的 `add`、`upgrade`、`remove`、`dev`、`undev` 一次只處理一個工具，或明確指定引擎；不提供批次或「全部」操作。這是 VK 自己的規則：[詢問](../../../GLOSSARY.md#執行與結果)、失敗範圍與下一步各自清楚；`update`、`sync`、`test` 已處理全部工具，追蹤全部新版則交給 Renovate。之後增加批次入口可以相容地擴充。</mark>
<mark style="background-color:#c8f0c8">v1.0.0 的 `add`、`upgrade`、`remove`、`dev`、`undev` 一次只處理一個[工具](../../../GLOSSARY.md#工具與出貨)，或明確指定引擎，不提供批次或「全部」操作。`update`、`sync`、`test` 則處理全部工具。</mark>

```diff
-Usage: just vendor_kit <command> [arguments] [options]
-
-Common commands:
-  add <repo>                  Import a tool into this install directory
-  add <repo>@<tag>            Import a specified version without listing versions
-  upgrade <repo>              Upgrade the locked version to a newer version
-  upgrade <repo>@<tag>        Switch to a specified version; an older tag downgrades the tool
-  dev <repo> -p <dir>         Use a local directory for the tool
-  dev --engine -i <image>     Use a local image for the engine
-
-Advanced commands:
-  remove <repo>               Remove a tool. Preserve init files; remove only previously inserted lines
-  undev <repo>                Return to the locked version
-  undev --engine              Return to the locked engine version
-  upgrade --engine            Upgrade the engine
-  upgrade --engine=<tag>      Switch to a specified engine version
-  update                      Check for new versions without modifying any files
-  update <repo>               Check only the specified tool for a new version
-  sync                        Synchronize local tool content with lock version lines or local overrides; runs automatically before each tool recipe
-  install                     Install VK in a directory within a repo, making it an install directory
-  uninstall                   Remove VK from the install directory. Preserve init files
-  prune                       Remove local resources created by VK that are no longer in use
-  test                        Run all checks; use the same command locally and in CI
-  test dist                   Check only tool delivery content
```
<mark style="background-color:#f8c8c8">清單裡的名詞見名詞表：</mark>
- <mark style="background-color:#f8c8c8">[工具](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">[\<repo\>](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">[安裝目錄](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">[鎖定版本](../../../GLOSSARY.md#版本與來源)</mark>
- <mark style="background-color:#f8c8c8">[版本鎖定行](../../../GLOSSARY.md#版本與來源)</mark>
- <mark style="background-color:#f8c8c8">[tag](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">[工具內容](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">[工具 recipe](../../../GLOSSARY.md#工具與出貨)</mark>
| <mark style="background-color:#c8f0c8">功能</mark> | <mark style="background-color:#c8f0c8">呼叫（前面加 `just vendor_kit`）</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">導入工具，可指定版本或離線來源</mark> | <mark style="background-color:#c8f0c8">`add <repo>`、`add <repo>@<tag>`、`add <repo> -i <image>`</mark> |
| <mark style="background-color:#c8f0c8">升降工具版本</mark> | <mark style="background-color:#c8f0c8">`upgrade <repo>`、`upgrade <repo>@<tag>`</mark> |
| <mark style="background-color:#c8f0c8">升降引擎版本</mark> | <mark style="background-color:#c8f0c8">`upgrade --engine`、`upgrade --engine=<tag>`</mark> |
| <mark style="background-color:#c8f0c8">改用[本機開發來源](../../../GLOSSARY.md#版本與來源)</mark> | <mark style="background-color:#c8f0c8">`dev <repo> -p <dir>`、`dev --engine -i <image>`</mark> |
| <mark style="background-color:#c8f0c8">回到[鎖定版本](../../../GLOSSARY.md#版本與來源)</mark> | <mark style="background-color:#c8f0c8">`undev <repo>`、`undev --engine`</mark> |
| <mark style="background-color:#c8f0c8">解除工具，保留[初始檔](../../../GLOSSARY.md#初始檔與合併)</mark> | <mark style="background-color:#c8f0c8">`remove <repo>`</mark> |
| <mark style="background-color:#c8f0c8">查新版</mark> | <mark style="background-color:#c8f0c8">`update`、`update <repo>`</mark> |
| <mark style="background-color:#c8f0c8">同步[工具內容](../../../GLOSSARY.md#工具與出貨)</mark> | <mark style="background-color:#c8f0c8">`sync`；每個[工具 recipe](../../../GLOSSARY.md#工具與出貨) 前也會自動執行</mark> |
| <mark style="background-color:#c8f0c8">補做安裝或移除 VK</mark> | <mark style="background-color:#c8f0c8">`install`、`uninstall`；首次導入由啟動器呼叫 `install`</mark> |
| <mark style="background-color:#c8f0c8">清理不再使用的本機資源</mark> | <mark style="background-color:#c8f0c8">`prune`</mark> |
| <mark style="background-color:#c8f0c8">檢查安裝、執行使用者測試或檢查交付</mark> | <mark style="background-color:#c8f0c8">`test`、`test <path>`、`test dist`</mark> |

### 執行位置

<mark style="background-color:#f8c8c8">依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)：</mark>
- <mark style="background-color:#f8c8c8">[VK recipe](../../../GLOSSARY.md#執行與結果) 只准在安裝目錄執行；檢查的是使用者打指令時所在的目錄，不是 just 切換後的 recipe 工作目錄。這是 VK 自己的規則：第一版先維持較窄的呼叫範圍，之後開放子目錄呼叫可以相容地擴充；在別處執行就印出 [訊息](../../contract/reason_codes.csv) `VK0028` [診斷](../../../GLOSSARY.md#執行與結果)，以[結束碼](../../contract/03_output.md#結束碼) `2` 拒絕，並印出該切到哪裡。[唯讀 recipe](../../../GLOSSARY.md#執行與結果) 也沒有例外</mark>
- <mark style="background-color:#f8c8c8">工具 recipe 自動觸發的 `sync` 會先回到安裝目錄再呼叫，所以不受影響；工具自己的 recipe 要不要擋，由那個工具決定</mark>
- <mark style="background-color:#f8c8c8">`install` 時上層或下層已經有安裝目錄，就印出 [訊息](../../contract/reason_codes.csv) `VK0029` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 拒絕：安裝目錄不能巢狀。這是 VK 自己的規則：每個安裝目錄各有獨立狀態、互不包含</mark>
- <mark style="background-color:#c8f0c8">VK recipe 只准在安裝目錄執行，[唯讀 recipe](../../../GLOSSARY.md#執行與結果) 也一樣；檢查使用者打指令時所在目錄，不是 just 切換後的位置</mark>
- <mark style="background-color:#c8f0c8">`just vendor_kit install` 用於已有入口的安裝目錄；未安裝目錄的首次導入由 `bootstrap.sh` 呼叫引擎的 `install`</mark>
- <mark style="background-color:#c8f0c8">工具 recipe 自動觸發的 `sync` 先回安裝目錄；工具自身的執行位置由工具決定</mark>
- <mark style="background-color:#c8f0c8">非安裝目錄與巢狀安裝的拒絕結果見[訊息表](../../contract/reason_codes.csv)；安裝單位依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)</mark>

### 命名空間

- <mark style="background-color:#f8c8c8">一個工具可以提供多個 [\<ns\> 命名空間](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#f8c8c8">`add` 時 `<ns>` 撞名就印出 [訊息](../../contract/reason_codes.csv) `VK0030` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 拒絕，而且在任何寫入之前檢查。比對的對象是：</mark>
  - <mark style="background-color:#f8c8c8">其他已裝進 repo 的工具</mark>
  - <mark style="background-color:#f8c8c8">根 `justfile` 既有的 recipe 或 module</mark>
  - <mark style="background-color:#f8c8c8">保留名 `vendor_kit`</mark>
```diff
+just vendor_kit <cmd> [arguments] [options]
```

<mark style="background-color:#c8f0c8">`vendor_kit` 是 VK 的命名空間，`<cmd>` 是 VK recipe 名稱。工具 recipe 的呼叫則為 `just <ns> …`。</mark>

- <mark style="background-color:#c8f0c8">一個工具可提供多個 [\<ns\> 命名空間](../../../GLOSSARY.md#工具與出貨)</mark>
- <mark style="background-color:#c8f0c8">`vendor_kit` 是保留名稱，不接受 `add vendor_kit`</mark>
- <mark style="background-color:#c8f0c8">`add` 在任何寫入前檢查 `<ns>` 是否與已裝工具、根 `justfile` 的 recipe 或 module、保留名 `vendor_kit` 撞名；拒絕結果見[訊息表](../../contract/reason_codes.csv)</mark>

### 說明與用法錯誤

<mark style="background-color:#f8c8c8">依 [02 不變量第 8 條](../../contract/02_invariants.md#8-使用者介面不可取代寫法一致)：</mark>
<mark style="background-color:#c8f0c8">判定順序：用法 → 主機前置檢查 → 辨識救援呼叫 → 版本組合。版本組合判定依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。</mark>

<mark style="background-color:#f8c8c8">先判用法（含 `bootstrap.sh` 單獨帶 `-h` 不做主機檢查的例外），再做適用的主機前置檢查，接著辨識下面封閉清單中的救援呼叫，最後判版本組合（版本組合不合又有用法錯誤時除外，見下）。版本組合判定排在執行紀錄以外的所有副作用之前，包含拉 image 與取件；`bootstrap.sh` 跨 X 連執行紀錄也不建，照它自己的規則。一般 recipe 的 `-h`／`--help` 只准與決定印哪份用法的 `--engine` 並用，例如 `upgrade --engine -h`；只有 `--engine` 會影響印哪份用法，`<repo>` 不算。與其他參數並用算用法錯誤，這是 VK 自己的規則：並用時不替使用者選擇要執行還是只看用法。版本組合不合又有用法錯誤時（例如 `upgrade --engine --bogus`），兩種拒絕的優先次序待確認（見 [介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)），不以此擴充救援清單。</mark>
<mark style="background-color:#c8f0c8">版本組合不合又有用法錯誤時（如 `upgrade --engine --bogus`），拒絕優先次序仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)，不因此擴充救援清單。</mark>

<mark style="background-color:#f8c8c8">這是 VK 自己的規則：`3` 只表示版本組合不合，救援清單以外的 help 不另開相容性例外；封閉清單讓舊薄殼遇到新引擎時仍有不必手改檔的出口。</mark>
| <mark style="background-color:#c8f0c8">版本組合不合時仍可用的類別</mark> | <mark style="background-color:#c8f0c8">呼叫</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">操作</mark> | <mark style="background-color:#c8f0c8">`install`、`upgrade --engine`、`sync`</mark> |
| <mark style="background-color:#c8f0c8">用法</mark> | <mark style="background-color:#c8f0c8">`just vendor_kit`、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項同）</mark> |

- <mark style="background-color:#f8c8c8">各指令都有 `-h`／`--help`：把該指令的用法印到 stdout，以[結束碼](../../contract/03_output.md#結束碼) `0` 結束；沒有 `help` 指令。只有救援路徑中的 just 呼叫在[薄殼](../../../GLOSSARY.md#vk-組件)、[VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與引擎的版本組合不相符時仍可用，也就是 `install`、`upgrade --engine`、`sync` 的不符判定，以及四種印用法的呼叫：`just vendor_kit`（不帶指令）、`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項 `--help` 同）；這些呼叫照各自原本的行為執行。薄殼被改過時的檢查與修復見 [bootstrap.sh](#bootstrapsh)。版本組合不相符時，救援路徑以外的呼叫即使帶 `-h`／`--help`，也以結束碼 `3` 結束：stderr 印出 `fatal` 診斷並附救援指令，stdout 不印用法</mark>
- <mark style="background-color:#f8c8c8">只打 `just vendor_kit`、不帶指令是用法錯誤，stderr 依序印版本行、[訊息](../../contract/reason_codes.csv) `VK0024` 診斷與簡短用法，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束：</mark>
- <mark style="background-color:#c8f0c8">各指令的 `-h` / `--help` 印該指令用法，沒有 `help` 指令；只准與決定印哪份用法的 `--engine` 並用，`<repo>` 不算</mark>
- <mark style="background-color:#c8f0c8">救援清單以外的 help 不另開相容性例外；拒絕結果見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">只打 `just vendor_kit` 的版本行與用法錯誤輸出，見 [03 輸出](../../contract/03_output.md#輸出)</mark>
- <mark style="background-color:#c8f0c8">不認得的名稱、直接接 `-h` 或 `--version`（如 `just vendor_kit foo`）由 just 找 recipe，參數到不了 VK；這時由 just 自己印出不帶 `vendor_kit:` 前綴的錯誤訊息並以非零結束 (just 1.33.0 起為 `1`)；這個碼是 just 回的，不表示 VK 的 `warn`，也不在 [03 結束碼](../../contract/03_output.md#結束碼)的範圍內。</mark>
- <mark style="background-color:#c8f0c8">不支援 `--allow-missing` 或 `JUST_ALLOW_MISSING`</mark>
- <mark style="background-color:#c8f0c8">缺必要參數、不認得或多出的參數、help 混用、[tag](../../../GLOSSARY.md#工具與出貨) 格式不合等用法錯誤，見[訊息表](../../contract/reason_codes.csv)</mark>

  ```diff
  -$ just vendor_kit
  -stderr: vendor_kit <version>
  -stderr: vendor_kit: error[VK0024]: No command was specified.
  -stderr: Usage: just vendor_kit <command> [arguments] [options]
  -exit code: 2
  ```
<mark style="background-color:#c8f0c8">參數與選項：</mark>

- <mark style="background-color:#f8c8c8">`vendor_kit` 後面接的不是 [VK recipe](../../../GLOSSARY.md#執行與結果) 名稱，或直接接 `-h`、`--version`，例如 `just vendor_kit foo`、`just vendor_kit -h`，都會被 just 當成 recipe 名稱去找，參數到不了 VK，不在 VK 的承諾內。這時由 just 自己印出不帶 `vendor_kit:` 前綴的錯誤訊息，以結束碼 `1` 結束；只承諾訊息來自 just 與結束碼是 `1`，不承諾訊息原文。以下是 just 1.33.0 的輸出；原文會隨 just 版本改變：</mark>
- <mark style="background-color:#c8f0c8">位置參數只放工具名稱 [\<repo\>](../../../GLOSSARY.md#工具與出貨)；`test <path>` 是例外。`test dist` 是完整指令名，`dist` 不是工具名或 path</mark>
- <mark style="background-color:#c8f0c8">其他值以選項帶入，例如 `-p <dir>`、`-i <image>`；選項可放位置參數前或後</mark>
- <mark style="background-color:#c8f0c8">引擎一律用 `--engine`；帶版本只收 `--engine=<tag>`，不收 `--engine <tag>`；工具用 `<repo>@<tag>`</mark>
- <mark style="background-color:#c8f0c8">[選項結束標記](../../../GLOSSARY.md#執行與結果)為單獨的 `--`；之後一律當位置參數，即使以 `-` 開頭</mark>

  ```diff
  -$ just vendor_kit foo
  -stderr: error: Justfile does not contain recipe `vendor_kit foo`.
  -exit code: 1
  ```
  <mark style="background-color:#f8c8c8">這個 `1` 是 just 回的，不是 VK 回的，因此不表示 VK 的 `warn`，也不和 [03 的結束碼規則](../../contract/03_output.md#結束碼)衝突。</mark>
- <mark style="background-color:#f8c8c8">不支援 just 的 `--allow-missing` 或 `JUST_ALLOW_MISSING`；它們會讓不認得的 recipe 靜默以 `0` 成功，違反 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark>
- <mark style="background-color:#f8c8c8">用法錯誤：先在 stderr 印出 `error` [診斷](../../../GLOSSARY.md#執行與結果)，再接著印簡短用法，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束。算用法錯誤的有：</mark>
  - <mark style="background-color:#f8c8c8">缺必要參數：[訊息](../../contract/reason_codes.csv) `VK0025`</mark>
  - <mark style="background-color:#f8c8c8">VK recipe 帶了不認得的選項或多出的參數，或 `-h`／`--help` 與 `--engine` 以外的參數並用：[訊息](../../contract/reason_codes.csv) `VK0026`</mark>
  - <mark style="background-color:#f8c8c8">tag 格式不合：[訊息](../../contract/reason_codes.csv) `VK0027`，見下面的[指定版本](#指定版本)</mark>
| <mark style="background-color:#c8f0c8">形式</mark> | <mark style="background-color:#c8f0c8">選項</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">短長都有</mark> | <mark style="background-color:#c8f0c8">`-h` / `--help`、`-y` / `--yes`、`-i` / `--image`、`-p` / `--path`</mark> |
| <mark style="background-color:#c8f0c8">只有長</mark> | <mark style="background-color:#c8f0c8">`--engine`、`--registry-token-file`、`--repair`</mark> |
  ```diff
  -$ just vendor_kit add
  -stderr: vendor_kit: error[VK0025]: Required argument is missing: <repo>.
  -stderr: Usage: just vendor_kit <command> [arguments] [options]
  -exit code: 2
-
  -$ just vendor_kit sync --bogus
  -stderr: vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --bogus.
  -stderr: Usage: just vendor_kit <command> [arguments] [options]
  -exit code: 2
-
  -$ just vendor_kit upgrade base@1.2.0
  -stderr: vendor_kit: error[VK0027]: Invalid tag format: 1.2.0. Use vX.Y.Z with no leading zeros in X, Y, or Z.
  -stderr: Usage: just vendor_kit <command> [arguments] [options]
  -exit code: 2
  ```
- <mark style="background-color:#f8c8c8">位置參數只放工具名稱 `<repo>`；其他值都經由選項帶入，例如 `-p <dir>`、`-i <image>`。`test dist` 是完整指令名，`dist` 不是位置參數，也不會被當成工具名</mark>
- <mark style="background-color:#f8c8c8">同一個概念一種寫法：對象是引擎一律寫 `--engine`，本機 image 一律寫 `-i <image>`。管理工具自身有局部前例，統一用選項是 VK 自己的規則：`upgrade`、`dev`、`undev` 共用 `--engine`，工具名留在位置參數，也避免與名叫 engine 的工具混淆</mark>
- <mark style="background-color:#f8c8c8">選項的寫法：</mark>
  - <mark style="background-color:#f8c8c8">有短也有長：`-h`／`--help`、`-y`／`--yes`、`-i`／`--image`、`-p`／`--path`</mark>
  - <mark style="background-color:#f8c8c8">只有長：`--engine`</mark>
  - <mark style="background-color:#f8c8c8">選項放在位置參數之前或之後都可以，意思相同</mark>
  - <mark style="background-color:#f8c8c8">單獨的 `--` 結束選項：它之後的參數一律當位置參數，以 `-` 開頭也一樣，例如 `just vendor_kit add -- <repo>`</mark>
- <mark style="background-color:#f8c8c8">`--engine` 是值可帶可不帶的長選項：不帶值時只表示對象是引擎；要帶值只接受 `=` 形式 `--engine=<tag>`，不接受 `--engine <tag>`，例如 `--engine=v1.2.0`。工具的指定版本維持 `<repo>@<tag>`</mark>

### 指定版本

<mark style="background-color:#f8c8c8">`<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../../GLOSSARY.md#工具與出貨) 照同一套規則：</mark>
<mark style="background-color:#c8f0c8">指令中 `<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../../GLOSSARY.md#工具與出貨) 規則：</mark>

```diff
-接受：
-just vendor_kit upgrade <repo>@v1.2.0
-just vendor_kit upgrade --engine=v1.2.0
-
-不接受：
-just vendor_kit upgrade --engine v1.2.0    值沒有用 = 接在 --engine 後面
-just vendor_kit upgrade <repo>@1.2.0       少了 v
-just vendor_kit upgrade <repo>@v01.2.0     有前導零
```
- <mark style="background-color:#f8c8c8">工具與引擎的 tag 只接受 `vX.Y.Z`，不帶 pre-release、build 後綴，不收前導零。這是 VK 自己的規則：相容性承諾以 `X.Y.Z` 定義，未定義 pre-release 的相容語意，Renovate 也只追正式版</mark>
- <mark style="background-color:#f8c8c8">最新版是把 X、Y、Z 當非負整數逐欄比數值，取最大的那個，不看字串順序、registry 回傳順序或推送時間；VK 沒有 channel 或撤回標記。最新版不限於目前工具的 X；VK 不保證或驗證工具內容的功能相容，也不維護工具之間的相容矩陣，這不改變交付格式的相容性承諾；同一個 tag 改指到別的 [digest](../../../GLOSSARY.md#工具與出貨) 不算新版</mark>
- <mark style="background-color:#f8c8c8">寫出格式不合的 tag 是用法錯誤，印出 [訊息](../../contract/reason_codes.csv) `VK0027` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束</mark>
- <mark style="background-color:#f8c8c8">`upgrade --engine=<tag>` 指定舊版引擎，而目標引擎無法無損讀取現有 VK 檔時，才用 [訊息](../../contract/reason_codes.csv) `VK0007`：`fatal`、結束碼 `3`，這次降版失敗</mark>
- <mark style="background-color:#f8c8c8">`upgrade <repo>@<tag>` 指定舊版工具不做上述引擎相容性判定，也不另設工具降版專用的原因代碼；正常完成時以結束碼 `0` 結束，出錯時依實際原因使用一般訊息與結束碼。這是 VK 自己的規則：同 X 退得回，以同一個 `upgrade` 入口指定舊版；不另維護工具之間的相容矩陣</mark>
- <mark style="background-color:#f8c8c8">不加 `init`、`ensure`、`diff`、`accept`、`rollback` 這類別名，也不加 `--purge`（VK 永不刪 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)，這個選項沒有對象）。這些用途各自由既有指令的選項或 git 處理</mark>
- <mark style="background-color:#f8c8c8">工具 repo 的命名空間也照這套寫法，例如 base ([base#1192](https://github.com/ycpss91255-docker/base/issues/1192))</mark>
- <mark style="background-color:#c8f0c8">只收 `vX.Y.Z`，三個數值不收前導零，不帶 pre-release 或 build 後綴</mark>
- <mark style="background-color:#c8f0c8">最新版把 X、Y、Z 當非負整數逐欄比數值，取最大者；不看字串順序、回傳順序或推送時間，沒有 channel 或撤回標記</mark>
- <mark style="background-color:#c8f0c8">同一 tag 改指別的 digest 不算新版；最新版不限目前工具的 vX</mark>
- <mark style="background-color:#c8f0c8">工具功能與工具間相容性的範圍見 [01 目的與承諾](../../contract/01_purpose.md#vk-不做的事)；交付格式與引擎相容性依 [02 不變量第 7 條](../../contract/02_invariants.md#7-工具-image-只承載交付資料引擎與工具不互相綁發版)</mark>
- <mark style="background-color:#c8f0c8">`upgrade <repo>@<tag>` 可指定舊版工具；`upgrade --engine=<tag>` 可指定舊版引擎，但須能無損讀取現有 [VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)，拒絕結果見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">不另加 `init`、`ensure`、`diff`、`accept`、`rollback` 等別名或 `--purge`；用途由既有指令、選項或 git 處理</mark>

### 成對與無害

- <mark style="background-color:#f8c8c8">做得了就反得回：`add` 與 `remove`、`dev` 與 `undev`、`install` 與 `uninstall` 成對。</mark>
- <mark style="background-color:#f8c8c8">查與套用分開：</mark>
  - <mark style="background-color:#f8c8c8">`update` 只查</mark>
  - <mark style="background-color:#f8c8c8">真正換版本的是 `upgrade`：裝新版工具內容、做[初始檔](../../../GLOSSARY.md#初始檔與合併)的[基準版合併](../../../GLOSSARY.md#初始檔與合併)、更新[基準版](../../../GLOSSARY.md#初始檔與合併)與[納管](../../../GLOSSARY.md#初始檔與合併)紀錄，必要時重產薄殼；由這次工具 `upgrade` 換版時，最後才寫版本鎖定行</mark>
- <mark style="background-color:#f8c8c8">沒有反向的 `sync`、`prune` 必須無害：</mark>
  - <mark style="background-color:#f8c8c8">不改任何[追蹤檔](../../../GLOSSARY.md#repo-內的檔與狀態)</mark>
  - <mark style="background-color:#f8c8c8">`prune` 只清本機資源與自己的暫存：本安裝目錄 `cache/` 裡未列在版本鎖定行的工具目錄、VK 自己的暫存與 VK 建立、且能證明已不再使用的已停止容器。不詢問，stdout 列出清了什麼；VK 拉取的 image 若不能證明無人使用就不刪，因為可能被其他安裝目錄或離線機器使用。這是 VK 自己的保守規則</mark>
| <mark style="background-color:#c8f0c8">操作</mark> | <mark style="background-color:#c8f0c8">對應操作</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`add`</mark> | <mark style="background-color:#c8f0c8">`remove`</mark> |
| <mark style="background-color:#c8f0c8">`dev`</mark> | <mark style="background-color:#c8f0c8">`undev`</mark> |
| <mark style="background-color:#c8f0c8">`install`</mark> | <mark style="background-color:#c8f0c8">`uninstall`</mark> |

<mark style="background-color:#f8c8c8">寫入與未完成狀態：</mark>
<mark style="background-color:#c8f0c8">工具升版的流程：</mark>

- <mark style="background-color:#f8c8c8">所有 recipe 都依共同規則先建執行紀錄；不可關閉，建不出就以 `VK0010`／`2` 停下。先記錄才執行有局部前例，完整保證是 VK 自己的規則：任何副作用之前都必須可追溯；辨識未完成狀態也會用進度檔，不只靠執行紀錄</mark>
- <mark style="background-color:#f8c8c8">工具層的[可寫 recipe](../../../GLOSSARY.md#執行與結果) 先留下進度，最後才改該工具的版本鎖定行；中途停下不撤回已做的步驟。這是 VK 自己的規則，不是交易、不回滾，靠進度檔辨識及恢復未完成狀態。Renovate 預先改鎖定行時不代表合併已完成；升引擎先換鎖定行則是明列例外</mark>
- <mark style="background-color:#f8c8c8">先辨識進度檔所記的未完成操作，再判是否為重複操作；可寫 recipe 先恢復，唯讀 recipe 只偵測並以 `2` 報出可直接執行的下一步，不改進度檔。唯讀 recipe 讀到工具 `upgrade` 未完成時，診斷指名工具並要求重跑原 `upgrade` 指令，保留指定 tag 與 `-y`；不借用未完成 `add` 或升引擎的代碼，見[訊息表](../../contract/reason_codes.csv) `VK0041`。唯讀 recipe 依進度檔所記的操作報出：未完成導入報 `VK0004`、工具 `upgrade` 報 `VK0041`、引擎 `upgrade` 報 `VK0023`、`undev` 報 `VK0053`；這四種以外的可寫 recipe（如 `remove`、`install`、`uninstall`、`dev`）未完成時報 `VK0054`，下一步重跑原指令，保留參數。都不恢復、不刪進度檔。`bootstrap.sh` 仍只依 `VK0037` 與 `VK0023` 判定，見[訊息表](../../contract/reason_codes.csv)。</mark>
- <mark style="background-color:#f8c8c8">詢問與恢復寫入的關係照[共同選項](#共同選項)；`bootstrap.sh --repair` 只修薄殼，不套用一般恢復規則補做安裝</mark>
1. <mark style="background-color:#c8f0c8">`update` 只查；真正換版本用 `upgrade`</mark>
2. <mark style="background-color:#c8f0c8">裝工具內容，做[基準版合併](../../../GLOSSARY.md#初始檔與合併)，更新[基準版](../../../GLOSSARY.md#初始檔與合併)與[納管](../../../GLOSSARY.md#初始檔與合併)紀錄，必要時重產薄殼；檔案詢問與保留見[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)</mark>
3. <mark style="background-color:#c8f0c8">由此次工具 `upgrade` 換版時，最後才寫版本鎖定行；寫入與恢復原則依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark>

<mark style="background-color:#f8c8c8">重複與再次操作：</mark>
<mark style="background-color:#c8f0c8">工具的版本鎖定行已更新，不代表初始檔合併已完成。鎖定行比基準版新時，不帶 tag 的 `upgrade <repo>` 只完成鎖定行那一版的合併，不再查最新版。</mark>

- <mark style="background-color:#f8c8c8">`add`：已導入且完整時，不重做，stdout 說明未變更，回 `0`；指定與現有鎖定行不同的 tag 時，以 `VK0045`／`2` 報待處理，下一步填成完整的 `just vendor_kit upgrade <repo>@<tag>`。換版本由 `upgrade` 負責，這是 VK 自己的規則</mark>
- <mark style="background-color:#f8c8c8">`remove`：工具不在版本鎖定行時，以 `VK0046`／`2` 報失敗並指名工具，不把拼錯名字當成移除成功</mark>
- <mark style="background-color:#f8c8c8">`install`：已完整導入且一致時，不重做，stdout 說明並回 `0`；薄殼不符時報 `VK0006`／`2`，指向 `sh bootstrap.sh --repair`，不把修薄殼當成補做全部安裝</mark>
- <mark style="background-color:#f8c8c8">`remove` 後再 `add`：留下的初始檔照已存在的檔處理 (`VK0018`)；已成功收回的 append 行重新詢問後才加入。上次零處或多處命中留下的內容不得無條件再 append，以免重複</mark>
- <mark style="background-color:#f8c8c8">`upgrade`：鎖定行已是目標版而基準版落後時，仍做基準版合併；全部一致時，stdout 說明未變更，回 `0`</mark>
- <mark style="background-color:#c8f0c8">可寫 recipe 先恢復進度檔中的未完成操作，再判是否重複；唯讀 recipe 只偵測，下一步見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">`bootstrap.sh --repair` 只修薄殼，不套用一般恢復規則補做安裝</mark>
- <mark style="background-color:#c8f0c8">已完整且一致的 `add`、`install`、`upgrade`，stdout 說明未變更；`add` 要換 tag 時改用 `upgrade`，見訊息表</mark>
- <mark style="background-color:#c8f0c8">`remove` 後再 `add`：留下的初始檔照既有檔處理；已收回的 append 行重新詢問才加，未收回的內容不得無條件再 append</mark>
- <mark style="background-color:#c8f0c8">`sync`、`prune` 不改[追蹤檔](../../../GLOSSARY.md#repo-內的檔與狀態)</mark>
- <mark style="background-color:#c8f0c8">`prune` 不詢問，stdout 列出清理內容：本安裝目錄 [cache/](../../../GLOSSARY.md#repo-內的檔與狀態) 中未鎖定的工具目錄、VK 暫存、VK 建立且可證明不再使用的已停止容器；image 無法證明無人使用就不刪</mark>

### 本機覆寫

<mark style="background-color:#f8c8c8">`dev` 是使用者明確選擇的具名行為。開著[本機覆寫](../../../GLOSSARY.md#版本與來源)時，除 `test` 外的一般 recipe 照常執行；若沒有其他診斷，就以[結束碼](../../contract/03_output.md#結束碼) `0` 結束。每次執行都要印出用了哪一個本機覆寫，不加診斷前綴；`update` 印到 stderr，其餘印到 stdout。覆寫提醒有局部前例；每次都報告所用覆寫，是 VK 自己的保證，因為這是使用者主動選擇的例外。`test` 對本機覆寫的處置見下方的[檢查](#檢查-test)。</mark>
| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">行為</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`dev <repo> -p <dir>`</mark> | <mark style="background-color:#c8f0c8">工具改用存在且符合交付格式的本機目錄；相對路徑以安裝目錄為準</mark> |
| <mark style="background-color:#c8f0c8">`dev --engine -i <image>`</mark> | <mark style="background-color:#c8f0c8">引擎改用本機 image</mark> |
| <mark style="background-color:#c8f0c8">`undev <repo>`、`undev --engine`</mark> | <mark style="background-color:#c8f0c8">解除覆寫，隨即同步到當下鎖定版本；不需讀原來源</mark> |

<mark style="background-color:#f8c8c8">本機覆寫的範圍與解除：</mark>
- <mark style="background-color:#f8c8c8">`dev --engine -i <image>` 與 `undev --engine` 成對，開發 VK 自身與驗收共用同一套指定引擎的方式。替換本機開發元件有局部類比，替換自身引擎的完整機制是 VK 自己的規則</mark>
- <mark style="background-color:#f8c8c8">覆寫只作用於這個工作目錄，worktree 各自一份，不跨 clone</mark>
- <mark style="background-color:#f8c8c8">`dev <repo> -p <dir>` 的目錄須存在，內容須符合該工具的交付格式，否則以 `VK0051`／`2` 報失敗；相對路徑以安裝目錄為準</mark>
- <mark style="background-color:#f8c8c8">重複 `dev` 指向同一來源時，stdout 說明未變更，回 `0`；指向不同來源時以 `VK0050`／`2` 報待處理，列出先執行的 `undev` 指令，不默默取代來源</mark>
- <mark style="background-color:#f8c8c8">`undev` 先辨識未完成操作；工具存在且沒有覆寫或未完成操作時，stdout 說明未變更，回 `0`。工具不在版本鎖定行時，以 `VK0046`／`2` 報失敗</mark>
- <mark style="background-color:#f8c8c8">`undev` 不必讀原來源也能解除覆寫，隨即同步到執行當下的鎖定版本；同步失敗時覆寫已解除，以 `VK0053`／`2` 報待處理，下一步是重跑原 `undev`。`sync` 不代替它完成或清掉它的進度檔</mark>
- <mark style="background-color:#f8c8c8">覆寫來源失效只阻擋需要讀它的動作，以 `VK0052`／`2` 診斷並指向 `undev`；`update` 仍照鎖定行查版本，`test` 照 `VK0032`，bootstrap 照自己的規則忽略覆寫。能同步其他工具不表示其 recipe 本體必定執行，自動前置 `sync` 非零時的處置仍見下面的待確認項</mark>
<mark style="background-color:#f8c8c8">共同選項</mark>
<mark style="background-color:#f8c8c8">`-y` 只適用於[可寫 recipe](../../../GLOSSARY.md#執行與結果)。這一節只定它的語意，不承諾每個可寫 recipe 都接受。已定的組合是 `upgrade <repo> -y` 與 `install -y`；首次導入由 [bootstrap.sh](#bootstrapsh) 傳入。其餘指令是否依「這個 recipe 可能詢問就接受 `-y`、不可能詢問就不接受」收斂，待確認（涉及 [詢問選項決議](https://github.com/ycpss91255-research/vendor_kit/issues/103)，見 [介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)）；判準是 recipe 可能詢問，不是這次有沒有詢問。</mark>
- <mark style="background-color:#f8c8c8">[-y](../../../GLOSSARY.md#執行與結果)：可代替原本允許的[詢問](../../../GLOSSARY.md#執行與結果)</mark>
  - <mark style="background-color:#f8c8c8">照樣把改了什麼印到 stdout，不加前綴</mark>
  - <mark style="background-color:#f8c8c8">只省略詢問，不授權覆蓋使用者既有的檔，依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)</mark>
  - <mark style="background-color:#f8c8c8">不能把已存在、尚未納管的檔改成 append 納管，見下面的[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)</mark>
<mark style="background-color:#f8c8c8">沒帶 `-y`、又不能互動時（例如在腳本裡），需要詢問的操作：</mark>
- <mark style="background-color:#f8c8c8">一律不改</mark>
- <mark style="background-color:#f8c8c8">以[結束碼](../../contract/03_output.md#結束碼) `2` 結束</mark>
- <mark style="background-color:#f8c8c8">印出該打的指令，訊息見 [訊息](../../contract/reason_codes.csv) `VK0002`</mark>
- <mark style="background-color:#f8c8c8">讀到輸入結束 (EOF) 不算同意</mark>
<mark style="background-color:#f8c8c8">stdin 與 stderr 都是終端 (TTY) 才算能互動；管線輸入不算，不另從 `/dev/tty` 讀答案。這是 VK 自己的規則：詢問印到 stderr，答案只從 stdin 讀；stdin 不是終端就不算能互動。能互動時，詢問文字印到 stderr，不帶[嚴重度](../../../GLOSSARY.md#執行與結果)前綴，提示為 `[y/N]`，空白 Enter 等於否。</mark>
<mark style="background-color:#f8c8c8">使用者明確回答「否」是正常取消：不修改，並在 stdout 說明未變更，以[結束碼](../../contract/03_output.md#結束碼) `0` 結束。拒絕記在哪裡待確認（三種做法見 [介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)），尚未選擇停用 `VK0020`、允許修改 metadata，或寫入執行紀錄；這三種做法都涉及已定文件。為保留取消的行為，每次呼叫先把該次所有問題問完，全部同意才做寫入（執行紀錄除外），包含恢復舊操作的寫入；這是 VK 自己的規則。詢問中 Ctrl-C 不算同意，不做被詢問的寫入，最終結束碼受 just 與外層訊號處理影響，不承諾固定回 `2`。升引擎第二次呼叫答否，不撤回第一次已完成的換引擎。</mark>
- <mark style="background-color:#c8f0c8">覆寫只作用於此工作目錄，worktree 各自一份，不跨 clone</mark>
- <mark style="background-color:#c8f0c8">每次報告用了哪個覆寫，不加診斷前綴：`update` 到 stderr，其餘到 stdout</mark>
- <mark style="background-color:#c8f0c8">除 `test` 外的一般 recipe 照常執行；覆寫來源失效只擋需讀它的動作，`update` 仍照鎖定行查，bootstrap 忽略覆寫</mark>
- <mark style="background-color:#c8f0c8">重複 `dev` 同來源、或工具存在但無覆寫與未完成操作的 `undev`，stdout 說明未變更；不同來源、工具不存在等拒絕結果見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">`undev` 同步未完成時，覆寫已解除，須重跑原 `undev`；`sync` 不代替完成或清掉其進度檔</mark>

## 各指令專用選項

- <mark style="background-color:#f8c8c8">`upgrade --engine` 分兩段執行：第一段換上目標引擎後，若原指令尚未做完，就印出 [訊息](../../contract/reason_codes.csv) `VK0023` 的 `error` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束。這是 VK 自己的兩段規則：換引擎後剩餘步驟由新引擎處理，手動重跑讓中間狀態可見；不是由重新載入薄殼必然推出的做法。診斷本文句尾的下一步指令是重跑原指令；原指令在訊息定義中以占位符表示，實際輸出由 VK 填成完整、不需使用者代換的指令，保留原來的 tag 與 `-y`。照它重跑就會接著完成第二段</mark>
- <mark style="background-color:#f8c8c8">`sync` 的判定分階段：</mark>
  - <mark style="background-color:#f8c8c8">主機前置檢查照共同規則先判</mark>
  - <mark style="background-color:#f8c8c8">安裝目錄層的零寫入阻擋要在逐工具處理前全部判完：薄殼不符用 [訊息](../../contract/reason_codes.csv) `VK0006`，版本組合不合用 `VK0008`；任一成立就不取件，兩者同時成立就兩條都印，結束碼取最大值</mark>
  - <mark style="background-color:#f8c8c8">沒有安裝目錄層的零寫入阻擋，才逐工具處理。`VK0004`、`VK0013` 只擋各自所屬的工具，其他工具照常同步；`VK0014`、`VK0015` 全部判、全部印</mark>
  - <mark style="background-color:#f8c8c8">整次執行的結束碼取所有安全判出結果的最大值；同一階段內的判定次序與印出順序不承諾。安裝目錄層的阻擋先判完，是 VK 自己的規則，確保除了執行紀錄外零寫入</mark>
  - <mark style="background-color:#f8c8c8">不刪未列在版本鎖定行的工具目錄，交給 `prune`；已鎖定工具的快取多出檔案則屬不一致，須修復。檢查涵蓋檔案集合與[逐檔指紋](../../../GLOSSARY.md#repo-內的檔與狀態)</mark>
  - <mark style="background-color:#f8c8c8">本機內容被改過時重新取件，照 `VK0015`／`1`；既有印記損壞時重新取件並重建印記，印 `VK0044` 的 `warn` 並回 `1`。首次取件原本沒有印記不算損壞，不因此警告；下載內容不符鎖定 digest 時以 `VK0043` 的 `error`／`2` 報失敗，不借用表示已修好的 `VK0015`</mark>
  - <mark style="background-color:#f8c8c8">cache 是可重建工作狀態，自動修復而保留警告有局部前例，完整行為是 VK 自己的規則：修好也要讓使用者知道。基準版合併需要寫追蹤檔，`sync` 只印 `VK0014` 並指向 `upgrade`，不自動合併</mark>
  - <mark style="background-color:#f8c8c8">工具 recipe 前自動觸發的 `sync` 回 `1` 時是否執行本體、整次呼叫如何回碼，待確認（依 [延期決議](https://github.com/ycpss91255-research/vendor_kit/issues/119)，留到 [自動同步與結果討論](https://github.com/ycpss91255-research/vendor_kit/issues/120)）</mark>
- <mark style="background-color:#f8c8c8">`update`：不帶工具參數時查全部工具與引擎；`update <repo>` 只查指定工具。每次即時列 tag，不用舊查詢快取；開著覆寫仍以版本鎖定行查詢，所用覆寫的提醒印到 stderr。已是最新或查到新版、沒有其他診斷時以[結束碼](../../contract/03_output.md#結束碼) `0` 結束；任何查詢失敗，整次以 `2` 結束。沒有 `--exit-code` 選項。</mark>
  - <mark style="background-color:#f8c8c8">查詢結果的 stdout 是[契約](../../../GLOSSARY.md#介面版與契約)明定、可以解析的固定格式，呼應 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。每個查詢的工具與引擎各印一行，已是最新的也印；不論查全部或指定工具、不論終端或管線、不論查詢結果，都用同一格式：`<repo> current: <tag> latest: <tag>`。查詢失敗時，`latest:` 的值是字面的 `none`；行的順序不承諾。</mark>
  - <mark style="background-color:#f8c8c8">第一欄是工具名；引擎用 `vendor_kit`。之後是「欄名: 值」成對；欄位以單一 ASCII 空白分隔。欄名以半形冒號結尾、不含空白，值是緊接的下一個欄位。腳本靠欄名取值，不靠欄號；同一個 X 內只會增加新的成對，不改既有欄名的意思。</mark>
  - <mark style="background-color:#f8c8c8">`current:` 的值是鎖定版本的 tag。`latest:` 一律印依[指定版本](#指定版本)算出的最新 tag，可能比 `current:` 舊。查詢失敗時，同時在 stderr 印出錯誤診斷，整次以 `2` 結束，不報已最新。判斷查詢是否失敗看結束碼與 stderr，不看 `none`；`none` 只是顯示值，tag 只接受 `vX.Y.Z`，不會與它撞名。</mark>
  - <mark style="background-color:#f8c8c8">stdout 只有這些行，不加表頭、進度、顏色或前綴；其他訊息都走 stderr。做 i18n 之前輸出一律英文，設不設 `LC_ALL=C` 結果相同。以後若做 i18n 可能翻譯欄名，比照 apt：腳本要穩定解析就設 `LC_ALL=C`，固定格式以 C locale 下的輸出為準。</mark>
  - <mark style="background-color:#f8c8c8">工具名能不能叫 `vendor_kit`，待確認（見 [update 固定格式討論](https://github.com/ycpss91255-research/vendor_kit/issues/342)）。</mark>
  - <mark style="background-color:#f8c8c8">`update <repo>` 指定的工具不在版本鎖定行時回什麼，待確認（見 [update 固定格式討論](https://github.com/ycpss91255-research/vendor_kit/issues/342)）。</mark>
  - <mark style="background-color:#f8c8c8">registry 列得到 tag、但沒有任何合格 `vX.Y.Z` 時怎麼印、回什麼結束碼，待確認（見 [update 固定格式討論](https://github.com/ycpss91255-research/vendor_kit/issues/342)）。</mark>
### registry token 檔案
<mark style="background-color:#c8f0c8">（本節新增）</mark>

  <mark style="background-color:#f8c8c8">示例：`base` 已是最新，`lint` 有新版，`format` 查詢失敗，引擎已是最新。下列 `stdout:`、`stderr:` 與 `exit code:` 是示例的串流與結束碼標示，不是實際輸出內容；行的排列只是示例。</mark>
<mark style="background-color:#c8f0c8">`--registry-token-file <path>`：</mark>

  ```diff
  -$ LC_ALL=C just vendor_kit update
  -stdout: base current: v1.2.0 latest: v1.2.0
  -stdout: lint current: v1.0.0 latest: v1.3.0
  -stdout: format current: v2.0.0 latest: none
  -stdout: vendor_kit current: v1.4.0 latest: v1.4.0
  -stderr: vendor_kit: error[VK0055]: Cannot access registry for format: request timed out. The requested operation did not complete.
  -exit code: 2
  ```
- <mark style="background-color:#f8c8c8">`add <repo> -i <image>`：離線導入，用本機 image 當工具來源。</mark>
- <mark style="background-color:#f8c8c8">`sh bootstrap.sh -i <image>`：用本機 image 當引擎來源，行為見 [bootstrap.sh](#bootstrapsh)。</mark>
- <mark style="background-color:#f8c8c8">兩種離線導入共通：</mark>
  - <mark style="background-color:#f8c8c8">`<image>` 可以是已載入的本機 image，或 image tar 檔</mark>
  - <mark style="background-color:#f8c8c8">寫進的版本鎖定行與線上導入相同，鎖的是 registry 的多架構 image index digest；離線交付須提供必要的 index digest 資訊，可以是 image tar 旁的同名 `.digest` 檔，不要求 tar 本身保存這些資訊</mark>
  - <mark style="background-color:#f8c8c8">保留內容身份與 digest 有局部前例；Docker 本機入口、相同鎖定行與缺資訊拒收的完整組合是 VK 自己的規則，讓別台機器取得同一份內容</mark>
  - <mark style="background-color:#f8c8c8">缺少必要的 [digest](../../../GLOSSARY.md#工具與出貨) 資訊時印出 [訊息](../../contract/reason_codes.csv) `VK0031` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，不退化成只寫 tag，也不拿 image tar 本身的雜湊代替</mark>
- <mark style="background-color:#c8f0c8">只有長選項，只收檔案路徑，不收 token 字串；不從 stdin 讀，單獨的 `-` 算用法錯誤；相對路徑以安裝目錄為準</mark>
- <mark style="background-color:#c8f0c8">只有 `update`、`add`、`upgrade <repo>` 接受，不適用引擎升版</mark>
- <mark style="background-color:#c8f0c8">只有真的要查版本清單時才讀檔；指定 tag 或離線導入而不查清單時不讀</mark>
- <mark style="background-color:#c8f0c8">憑證用途見 [registry 與認證](#registry-與認證)，讀檔與認證問題見[訊息表](../../contract/reason_codes.csv)</mark>

<mark style="background-color:#f8c8c8">第一版不承諾離線升版入口。其他未列的選項（例如強制重取、詳細度與平行數）仍留到實作時定；執行紀錄的結構是內部協定，不承諾供第三方直接解析。</mark>
### upgrade --engine
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#f8c8c8">同一安裝目錄的寫入須持有排他鎖，讀取須持有共享鎖；會取件的 `sync` 是寫入端。持鎖的是真正在寫檔的程序，鎖涵蓋它的生命週期。另一個執行等待取得鎖，預設 60 秒；`VENDOR_KIT_LOCK_TIMEOUT` 可改等待秒數，`0` 是立即失敗，`-1` 是無限等待。等不到鎖時以 `VK0042` 的 `error`／`2` 結束，除執行紀錄外不寫檔，並指名安裝目錄。</mark>
1. <mark style="background-color:#c8f0c8">第一段換上目標引擎，尚未完成的結果見[訊息表](../../contract/reason_codes.csv)</mark>
2. <mark style="background-color:#c8f0c8">按診斷句尾的完整指令手動重跑，由新引擎完成剩餘步驟；保留原 tag 與 `-y`</mark>

<mark style="background-color:#f8c8c8">VK 沒有整次執行限時的命令列選項；上面的鎖等待逾時是另一件事。要限時就在外層包 `timeout(1)`，或用 CI 的逾時設定。外層中斷時的最終碼不承諾是 VK 的 `0`～`3`；殺掉主機等待程序不表示容器已停止寫入，恢復前須取得鎖，確保舊寫入者不會與新執行並行。下次執行依執行紀錄與進度檔辨識未完成狀態並說出下一步。</mark>
<mark style="background-color:#c8f0c8">第二次呼叫答否，不撤回第一次已完成的換引擎。</mark>

### sync
<mark style="background-color:#c8f0c8">（本節新增）</mark>

1. <mark style="background-color:#c8f0c8">做主機前置檢查</mark>
2. <mark style="background-color:#c8f0c8">在逐工具處理前判薄殼與版本組合；任一阻擋就不取件，兩者皆不符時都報告，結果依[訊息表](../../contract/reason_codes.csv)與 [03 結束碼](../../contract/03_output.md#結束碼)</mark>
3. <mark style="background-color:#c8f0c8">再逐工具同步；跨工具寫入界線依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)，同階段判定與輸出順序不承諾</mark>

| <mark style="background-color:#c8f0c8">同步對象</mark> | <mark style="background-color:#c8f0c8">行為</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">已鎖定工具</mark> | <mark style="background-color:#c8f0c8">判定 cache 檔案集合與[逐檔指紋](../../../GLOSSARY.md#repo-內的檔與狀態)，包括多出的檔案；不一致則重新取件</mark> |
| <mark style="background-color:#c8f0c8">既有[印記](../../../GLOSSARY.md#repo-內的檔與狀態)損壞</mark> | <mark style="background-color:#c8f0c8">重新取件並重建；首次取件原本沒有印記不算損壞</mark> |
| <mark style="background-color:#c8f0c8">未列在鎖定行的工具目錄</mark> | <mark style="background-color:#c8f0c8">留給 `prune`</mark> |
| <mark style="background-color:#c8f0c8">初始檔的基準版落後</mark> | <mark style="background-color:#c8f0c8">不自動合併，改用 `upgrade`</mark> |

<mark style="background-color:#c8f0c8">[取件](../../../GLOSSARY.md#工具與出貨)、[metadata](../../../GLOSSARY.md#初始檔與合併) 或未完成導入等問題的診斷與下一步見[訊息表](../../contract/reason_codes.csv)。修復快取後仍報告原本問題，診斷與結果見訊息表。工具 recipe 前的自動 `sync` 帶警告完成時，本體是否執行及整次回碼仍待確認，見[自動同步與結果討論](https://github.com/ycpss91255-research/vendor_kit/issues/120)。</mark>

### update
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#c8f0c8">不帶工具參數查全部工具與引擎；`update <repo>` 只查指定已安裝工具，沒裝的工具拒絕，見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">每次即時查 tag，不用舊查詢快取，沒有 `--exit-code` 選項</mark>
- <mark style="background-color:#c8f0c8">查詢結果是可解析的固定格式：`<repo> current: <tag> latest: <tag>`</mark>
- <mark style="background-color:#c8f0c8">每個查詢對象一行，已最新也印，順序不承諾；引擎的工具名欄用 `vendor_kit`</mark>
- <mark style="background-color:#c8f0c8">欄位以單一 ASCII 空白分隔，欄名以半形冒號結尾，值緊接下一欄；靠欄名取值，不靠欄號，同一個 vX 內只會新增「欄名: 值」成對欄位</mark>
- <mark style="background-color:#c8f0c8">`current:` 是鎖定版本的 tag；`latest:` 是依[指定版本](#指定版本)算出的最新 tag，可能比 current 舊</mark>
- <mark style="background-color:#c8f0c8">查詢失敗時該行 `latest: none`；registry 有 tag 卻無合法 `vX.Y.Z` 也如此。`none` 只是顯示值，診斷與結束碼見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">stdout 只有結果行，不加表頭、進度、顏色或前綴；其他訊息到 stderr</mark>
- <mark style="background-color:#c8f0c8">目前輸出一律英文，設不設 `LC_ALL=C` 結果相同；日後若做 i18n，要穩定解析的腳本請設 `LC_ALL=C`</mark>

<mark style="background-color:#c8f0c8">正常結果示例：</mark>

```diff
+base current: v1.2.0 latest: v1.2.0
+lint current: v1.0.0 latest: v1.3.0
+vendor_kit current: v1.4.0 latest: v1.4.0
```

### 離線導入
<mark style="background-color:#c8f0c8">（本節新增）</mark>

| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">本機 image 用途</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`add <repo> -i <image>`</mark> | <mark style="background-color:#c8f0c8">工具來源</mark> |
| <mark style="background-color:#c8f0c8">`bootstrap.sh -i <image>`</mark> | <mark style="background-color:#c8f0c8">引擎來源</mark> |

- <mark style="background-color:#c8f0c8">可用已載入的本機 image 或 image tar；離線交付須附多架構 image index digest 資訊，例如 tar 旁的同名 `.digest` 檔</mark>
- <mark style="background-color:#c8f0c8">不要求 tar 本身保存 digest；不拿 tar 雜湊代替，也不退化成只寫 tag；線上與離線的鎖定行關係依 [02 不變量第 2 條](../../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)</mark>
- <mark style="background-color:#c8f0c8">digest 缺失或不符的結果見[訊息表](../../contract/reason_codes.csv)；既有安裝的額外核對見[用哪一版引擎](#用哪一版引擎)</mark>
- <mark style="background-color:#c8f0c8">v1.0.0 不承諾離線升版入口</mark>

### 設定
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#c8f0c8">`.vendor_kit/config.toml` 的設定：</mark>

| <mark style="background-color:#c8f0c8">欄位</mark> | <mark style="background-color:#c8f0c8">可用值</mark> | <mark style="background-color:#c8f0c8">未設定時</mark> |
|---|---|---|
| <mark style="background-color:#c8f0c8">`lock_timeout_seconds`</mark> | <mark style="background-color:#c8f0c8">大於等於 `-1` 的整數：正數為等待秒數；`0` 不等；`-1` 一直等</mark> | <mark style="background-color:#c8f0c8">60 秒</mark> |
| <mark style="background-color:#c8f0c8">`lock_enabled`</mark> | <mark style="background-color:#c8f0c8">布林值；`false` 只給不支援檔案鎖的檔案系統，每次執行都[警告](../../../GLOSSARY.md#執行與結果)</mark> | <mark style="background-color:#c8f0c8">`true`</mark> |
| <mark style="background-color:#c8f0c8">`[test]`</mark> | <mark style="background-color:#c8f0c8">`image` 為非空字串；`command` 為由非空字串組成的非空陣列</mark> | <mark style="background-color:#c8f0c8">無預設 runner；`test <path>` 停下並指名缺少的欄位；不帶 path 的 `test` 不需要</mark> |

<mark style="background-color:#c8f0c8">前兩個欄位是頂層設定。設定在第一次取鎖前讀取；任一設定無效時所有入口一律停下，修法與結束碼見[訊息表](../../contract/reason_codes.csv)，不以預設值繼續。</mark>

### 鎖與逾時
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#c8f0c8">鎖的可用值與無效設定處置見[設定](#設定)。</mark>

- <mark style="background-color:#c8f0c8">所有取鎖入口（含自動 `sync`、bootstrap 啟動的引擎）用同一設定；首次導入固定等 60 秒</mark>
- <mark style="background-color:#c8f0c8">寫入持排他鎖，讀取持共享鎖；會取件的 `sync` 屬寫入端，實際寫檔程序在其生命週期持鎖</mark>
- <mark style="background-color:#c8f0c8">等不到鎖的處置見訊息表</mark>
- <mark style="background-color:#c8f0c8">VK 沒有整次執行限時選項；需要時在外層用 `timeout(1)` 或 CI 逾時設定，外層中斷的碼不承諾是 VK 結束碼</mark>
- <mark style="background-color:#c8f0c8">殺掉主機等待程序不代表容器已停止寫入；恢復前仍須取得鎖，下次執行依紀錄與進度檔辨識未完成操作</mark>

## 追蹤新版

<mark style="background-color:#f8c8c8">工具與引擎的新版由 Renovate regex preset 追蹤。Renovate 開的 PR 只改一行版本鎖定行；VK 沒有 bot，不 commit，也不開 PR。</mark>
<mark style="background-color:#f8c8c8">以下流程假設 cache 已備妥；CI 全新 checkout 缺 cache 的處理見[檢查 (test)](#檢查-test) 的待確認項。PR 上跑 `just vendor_kit test`。版本鎖定行已更新、基準版尚未更新時，`test` 在 stderr 印出 [訊息](../../contract/reason_codes.csv) `VK0014` 的 `warn` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `1` 結束，CI 因而不通過。使用者要在該 PR 分支的本機執行 `just vendor_kit upgrade <repo> -y`，再自行 commit、push；CI 重跑通過後才 merge。鎖定行比基準版新時，不帶指定 tag 的 `upgrade <repo>` 只完成鎖定行指定版本的合併，不再查最新版，避免升過 PR 提出的版本。警告在本機與 CI 都非零，這是 VK 自己的規則。</mark>
<mark style="background-color:#c8f0c8">VK 提供 Renovate regex preset 追蹤工具與引擎的正式版 `vX.Y.Z`；VK 寫出的版本鎖定行必須能由它辨識與修改。</mark>

## 輸出

<mark style="background-color:#f8c8c8">stdout 與 stderr 怎麼分、訊息的前綴與顏色，見 [03 輸出](../../contract/03_output.md#輸出)。是否成功依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。這些輸出承諾只適用於已進到 VK 的呼叫，just 的 quiet 與 just 自己的錯誤不在內。</mark>
<mark style="background-color:#f8c8c8">一次處理多個工具時，依固定結果碼取最大值，仍印出每個工具的結果；取最大值的算法有局部前例，完整的結果契約是 VK 自己的規則，見 [03 結束碼](../../contract/03_output.md#結束碼)。</mark>
<mark style="background-color:#c8f0c8">串流、前綴、顏色與結果彙總見 [03 輸出](../../contract/03_output.md)；逐項診斷、處置與結束碼只見[訊息表](../../contract/reason_codes.csv)。這些承諾適用於已進入 VK 的呼叫。</mark>

## 使用者的檔與 VK 的檔

<mark style="background-color:#f8c8c8">依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)，這一節列出 VK 會碰到哪些檔、怎麼碰。</mark>
<mark style="background-color:#c8f0c8">檔案權屬依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)與 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、VK 檔的定義；這裡只列操作。</mark>

<mark style="background-color:#f8c8c8">使用者的檔：</mark>
| <mark style="background-color:#c8f0c8">檔案</mark> | <mark style="background-color:#c8f0c8">操作規則</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">根 `justfile`、初始檔等 repo 檔</mark> | <mark style="background-color:#c8f0c8">見下面的既有檔寫入與收回規則</mark> |
| <mark style="background-color:#c8f0c8">`.vendor_kit/config.toml`</mark> | <mark style="background-color:#c8f0c8">使用者維護，不是初始檔；換版與合併沿用初始檔的保護規則，先詢問</mark> |
| <mark style="background-color:#c8f0c8">`version.toml`、基準版、納管紀錄、薄殼</mark> | <mark style="background-color:#c8f0c8">依各自完整性與恢復規則處理；鎖定行可按固定格式手改升降版</mark> |
| <mark style="background-color:#c8f0c8">執行紀錄、進度檔</mark> | <mark style="background-color:#c8f0c8">保存操作與恢復所需資訊，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark> |

- <mark style="background-color:#f8c8c8">適用的 repo 檔含根 `justfile`、初始檔等</mark>
- <mark style="background-color:#f8c8c8">屬於追蹤檔的 VK 檔裡，交由使用者維護、受合併保護的只有 VK 的設定檔 `.vendor_kit/config.toml`：它不是初始檔，只沿用初始檔的保護與合併規則，換新版或合併前一樣先問</mark>
- <mark style="background-color:#f8c8c8">其餘屬於追蹤檔的 VK 檔（`version.toml`、基準版、納管紀錄、薄殼）內容由 VK 擁有，VK 重寫它們不構成覆蓋。版本鎖定行雖由 VK 擁有，使用者仍可以照它的固定格式手改來升版或退版；手改不會讓它變成交由使用者維護的內容。其他 VK 檔依各自的完整性與恢復規則處理，不概括為同一種拒絕或修復行為。薄殼被改過的處置依 [02 不變量第 6 條](../../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)</mark>
- <mark style="background-color:#f8c8c8">執行紀錄與[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)是 VK 的工作狀態，不是使用者的內容</mark>
### 寫入既有檔的例外
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#f8c8c8">目標不存在時新建檔（例如第一次導入時整份複製的初始檔）不動到既有的內容。動到既有使用者檔、又不構成覆蓋的寫入，只有這四種明定例外：</mark>
<mark style="background-color:#c8f0c8">目標不存在就新建；既有使用者檔的寫入只有下列例外：</mark>

- <mark style="background-color:#f8c8c8">根 `justfile` 加一行 `import`：沒有這個檔就建，有就詢問後 append</mark>
- <mark style="background-color:#f8c8c8">根 `.dockerignore` 加四行：同上的 append 規則</mark>
- <mark style="background-color:#f8c8c8">append 型初始檔第一次導入時向既有檔 append 內容，規則見下面「append 型的初始檔」</mark>
- <mark style="background-color:#f8c8c8">已納管初始檔的基準版合併（VK 的設定檔沿用同一套規則）：</mark>
  - <mark style="background-color:#f8c8c8">使用者沒改過：詢問是否換新版。這是 VK 自己的規則，未修改不等於同意更換</mark>
  - <mark style="background-color:#f8c8c8">雙方都改過：詢問是否合併；[合併衝突](../../../GLOSSARY.md#初始檔與合併)留下標記，由使用者解，印出 [訊息](../../contract/reason_codes.csv) `VK0021` 的 `warn` 診斷並以[結束碼](../../contract/03_output.md#結束碼) `1` 結束；這次執行做完，有警告</mark>
| <mark style="background-color:#c8f0c8">寫入</mark> | <mark style="background-color:#c8f0c8">操作</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">根 `justfile` 的一行 `import`</mark> | <mark style="background-color:#c8f0c8">有檔先詢問再 append</mark> |
| <mark style="background-color:#c8f0c8">根 `.dockerignore` 的四行</mark> | <mark style="background-color:#c8f0c8">同上</mark> |
| <mark style="background-color:#c8f0c8">append 型初始檔的首次導入</mark> | <mark style="background-color:#c8f0c8">有檔先詢問再 append</mark> |
| <mark style="background-color:#c8f0c8">已納管初始檔的基準版合併（設定檔同）</mark> | <mark style="background-color:#c8f0c8">未改過也先問是否換版；雙方都改過則先問是否合併，衝突留標記給使用者解</mark> |

<mark style="background-color:#f8c8c8">append 型的初始檔：</mark>
<mark style="background-color:#c8f0c8">[合併衝突](../../../GLOSSARY.md#初始檔與合併)的診斷與結束碼見[訊息表](../../contract/reason_codes.csv)。</mark>

- <mark style="background-color:#f8c8c8">幾乎一定已經存在的那類初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`</mark>
- <mark style="background-color:#f8c8c8">沒有這個檔就建，已經有就問過才 append</mark>
- <mark style="background-color:#f8c8c8">唯一例外是根 `justfile` 不存在時建檔附的 `default`；那個檔建立後就是 repo 檔</mark>
- <mark style="background-color:#c8f0c8">幾乎一定已存在的初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`</mark>
- <mark style="background-color:#c8f0c8">根 `justfile` 不存在時建檔附的 `default` 是例外，建立後按 repo 檔處理</mark>
- <mark style="background-color:#c8f0c8">已存在但尚未納管的檔，`-y` 不能改成 append 納管</mark>
- <mark style="background-color:#c8f0c8">`add` 遇到不適用 append 的既有檔不納管、不覆蓋；v1.0.0 不提供改為納管的選項，後續不做基準版合併，結果見訊息表</mark>
- <mark style="background-color:#c8f0c8">`upgrade` 遇到新版不再提供的初始檔或使用者已刪的納管初始檔，不刪、不重建，只在 stdout 列清單</mark>
- <mark style="background-color:#c8f0c8">`remove`、`uninstall` 保留初始檔，保留清單印到 stdout</mark>

<mark style="background-color:#f8c8c8">移除時收回自己插入的行，只有這三類：</mark>
### 收回插入的行
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#f8c8c8">`uninstall` 移除安裝時加在根 `justfile` 的那一行 `import`</mark>
- <mark style="background-color:#f8c8c8">`uninstall` 移除加在根 `.dockerignore` 的那四行</mark>
- <mark style="background-color:#f8c8c8">`remove` 與 `uninstall` 移除 append 型初始檔當初插進既有檔的那幾行</mark>
| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">有紀錄才考慮收回的行</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`uninstall`</mark> | <mark style="background-color:#c8f0c8">根 `justfile` 的一行 `import`、根 `.dockerignore` 的四行</mark> |
| <mark style="background-color:#c8f0c8">`remove`、`uninstall`</mark> | <mark style="background-color:#c8f0c8">append 型初始檔插進既有檔的行</mark> |

<mark style="background-color:#f8c8c8">有紀錄、所以會被收回動作碰到的檔，就是根 `justfile`、根 `.dockerignore`，以及工具宣告為 append 的那些檔；未登記的檔不碰。收回行之前一樣先詢問。收回時：</mark>
- <mark style="background-color:#f8c8c8">整份檔裡恰好一處與當初插入的原文相同，才刪那一行</mark>
- <mark style="background-color:#f8c8c8">一處也沒有、或有兩處以上，都不刪，講出是哪個檔、找到幾處；一處也沒有時印出 [訊息](../../contract/reason_codes.csv) `VK0016` [警告](../../../GLOSSARY.md#執行與結果)，有兩處以上時印出 [訊息](../../contract/reason_codes.csv) `VK0017` 警告，兩者都以[結束碼](../../contract/03_output.md#結束碼) `1` 結束</mark>
<mark style="background-color:#f8c8c8">這是 VK 自己的收回規則：以紀錄的原文在整份檔唯一命中作為操作判準，零處或多處都不動並警告。殘餘風險是：VK 插的行被刪，使用者又在別處寫同一行時，這個判準分不出作者，會刪到使用者那行；唯一命中不保證可靠歸因。判準重審見 [收回判準重審](https://github.com/ycpss91255-research/vendor_kit/issues/341)。</mark>
<mark style="background-color:#f8c8c8">其他情況：</mark>
- <mark style="background-color:#f8c8c8">`add` 遇到已存在的檔：不納管、不覆蓋，印出 [訊息](../../contract/reason_codes.csv) `VK0018` 警告並以[結束碼](../../contract/03_output.md#結束碼) `1` 結束。這是 VK 自己的規則：這次 `add` 不接管該檔，後續升版不會替它做基準版合併；第一版不提供把既有檔改為納管的選項</mark>
- <mark style="background-color:#f8c8c8">`upgrade` 遇到上游不再提供的初始檔，或使用者已刪掉的納管初始檔：不刪、不重建，只列清單到 stdout；沒有其他診斷時回 `0`。這是 VK 自己的保護規則</mark>
- <mark style="background-color:#f8c8c8">`remove` 與 `uninstall`：不刪初始檔，只把保留清單印到 stdout，不加前綴；沒有其他診斷時以[結束碼](../../contract/03_output.md#結束碼) `0` 結束，有 `VK0016`／`VK0017` 殘留時則是做完但有警告，回 `1`</mark>
- <mark style="background-color:#c8f0c8">整份檔依紀錄的整檔 hash 與 VK 上次寫入後相同（CRLF／LF 視為相同，只改行尾不算改過），且原文恰好一處，才先詢問、同意後刪</mark>
- <mark style="background-color:#c8f0c8">其他情況只列不刪：列出檔名、紀錄原文與目前相符行號；警告與結束碼見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">舊紀錄沒有 hash 也只列不刪；未登記的檔不碰</mark>

### remove 與 uninstall 的收回範圍

<mark style="background-color:#f8c8c8">`remove` 收回該工具的版本鎖定行、`cache/<repo>/`、基準版、印記、納管紀錄、`gen/` 中的命名空間載入行，以及問過且符合上面判準的 append 行；初始檔保留。開著該工具的本機覆寫時如何處理覆寫紀錄，待確認（見 [介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)）。</mark>
<mark style="background-color:#c8f0c8">`remove` 收回該工具的鎖定行、`cache/<repo>/`、基準版、印記、納管紀錄、[gen/](../../../GLOSSARY.md#repo-內的檔與狀態) 的命名空間載入行，以及同意且符合判準的 append 行；初始檔保留。工具開著覆寫時的處置仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)。</mark>

<mark style="background-color:#f8c8c8">`uninstall` 的收回範圍與紀錄保存政策待確認（見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)）；目前寫法如下：</mark>
<mark style="background-color:#c8f0c8">`uninstall` 的收回範圍與紀錄保存政策仍待確認，見[介面修改討論](https://github.com/ycpss91255-research/vendor_kit/issues/47)；目前介面為：</mark>

- <mark style="background-color:#f8c8c8">收回 VK 擁有的版本鎖定行、基準版、納管紀錄、印記、薄殼、cache、gen 與進度檔，以及根 `justfile` 的 import、根 `.dockerignore` 四行、工具 append 行；涉及使用者檔的行仍先詢問、依上面判準逐處收回，沒收回的位置列清單</mark>
- <mark style="background-color:#f8c8c8">解除 VK 的本機覆寫紀錄，保留[本機開發來源](../../../GLOSSARY.md#版本與來源)；不要求先 `undev`。這是 VK 自己的規則：解除的是 VK 的選擇紀錄，使用者的來源不屬收回範圍</mark>
- <mark style="background-color:#f8c8c8">一律保留 `.vendor_kit/config.toml`、使用者檔、未登記的檔與 `.vendor_kit/` 目錄，stdout 列出留下的內容；連未修改過的設定檔也不刪</mark>
- <mark style="background-color:#f8c8c8">先建本次執行紀錄，寫入前留下進度，收回途中保留恢復所需證據；最後才處理鎖定行與完成的進度檔。真正中斷時回 `2`，未完成狀態須可辨識、可恢復；不能把 `VK0016`／`VK0017` 的已完成但有殘留當成中斷</mark>
- <mark style="background-color:#f8c8c8">舊執行紀錄與本次 `uninstall` 的紀錄留在 `.vendor_kit/`，不另定保存期限；使用者移走目錄時，舊紀錄跟著走。這是 VK 自己的保存政策</mark>
- <mark style="background-color:#c8f0c8">收回鎖定行、基準版、納管紀錄、印記、薄殼、cache、gen、進度檔，以及符合判準的根目錄與工具 append 行；未收回的位置列清單</mark>
- <mark style="background-color:#c8f0c8">解除覆寫紀錄，不要求先 `undev`，保留本機開發來源</mark>
- <mark style="background-color:#c8f0c8">保留 `.vendor_kit/config.toml`、使用者檔、未登記檔與 `.vendor_kit/` 目錄，stdout 列出留下的內容</mark>
- <mark style="background-color:#c8f0c8">先建紀錄與進度，保留恢復證據，最後處理鎖定行與完成的進度檔；殘留與真正中斷的結果見訊息表</mark>
- <mark style="background-color:#c8f0c8">舊紀錄與本次紀錄留在 `.vendor_kit/`，不另定期限；使用者移走目錄時，紀錄跟著走</mark>

<mark style="background-color:#f8c8c8">重新導入時，使用者先把整個 `.vendor_kit/` 移到安裝位置之外，再在原位置執行 `sh bootstrap.sh`；新導入完成後，從移走的 `config.toml` 手動搬回自訂內容，不自動承接舊設定。這是 VK 自己的重新導入路徑，不擴大 bootstrap 的未完成首次導入例外。目錄尚在且缺有效鎖定行時仍照 `VK0037` 停下，不猜成首次導入，也不把缺鎖定行一律歸因於 `uninstall`。</mark>
<mark style="background-color:#c8f0c8">重新導入：</mark>

1. <mark style="background-color:#c8f0c8">把整個 `.vendor_kit/` 移到安裝位置之外</mark>
2. <mark style="background-color:#c8f0c8">在原位置執行 `bootstrap.sh`</mark>
3. <mark style="background-color:#c8f0c8">完成後從移走的 `config.toml` 手動搬回自訂內容，不自動承接舊設定</mark>

<mark style="background-color:#c8f0c8">這不擴大[未完成首次導入例外](#首次導入還是既有安裝目錄)。</mark>

## 檢查 (test)

<mark style="background-color:#f8c8c8">[test](../../../GLOSSARY.md#vk-recipe-與用途) 是 VK 給本機與 CI 共用的完整檢查指令，涵蓋 CI 驗得到的所有對外承諾。這是 VK 自己的檢查範圍。CI 全新 checkout 時缺 cache 的處理（先跑 `sync`，或照報 `test` 仍判得出的檢查）待確認，涉及[嚴格檢查決議](https://github.com/ycpss91255-research/vendor_kit/issues/124)。`test` 不寫入追蹤檔，不準備或修復 cache、gen 與進度檔；依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)照寫執行紀錄。執行紀錄與 [嚴格檢查決議](https://github.com/ycpss91255-research/vendor_kit/issues/124)「一律不寫檔」的字面對齊待確認；不以此放寬為允許取件。檢查的範圍照這個原則：</mark>
<mark style="background-color:#c8f0c8">[test](../../../GLOSSARY.md#vk-recipe-與用途) 給本機與 CI 共用，檢查目前安裝或交付狀態；帶 path 時，安裝檢查通過後跑使用者自己的測試。VK 自身的出貨驗收另依 [02 不變量第 9 條](../../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)。</mark>

- <mark style="background-color:#f8c8c8">[01 目的與承諾](../../contract/01_purpose.md)的對外[契約](../../../GLOSSARY.md#介面版與契約)中，CI 驗得到的項目百分之百覆蓋</mark>
- <mark style="background-color:#f8c8c8">CI 驗不到的項目由 VK 的驗收測試覆蓋，依 [02 不變量第 9 條](../../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)</mark>
| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">用途</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">`just vendor_kit test`</mark> | <mark style="background-color:#c8f0c8">只做完整安裝檢查；沒有工具也檢查薄殼與引擎</mark> |
| <mark style="background-color:#c8f0c8">`just vendor_kit test <path>`</mark> | <mark style="background-color:#c8f0c8">先做完整安裝檢查，通過才跑所選的使用者測試</mark> |
| <mark style="background-color:#c8f0c8">`just vendor_kit test dist`</mark> | <mark style="background-color:#c8f0c8">只檢查工具交付內容，給提供工具的 repo 在 CI 用；檢查 append 型等交付規則，不能混用 path</mark> |

<mark style="background-color:#f8c8c8">兩種用法：</mark>
<mark style="background-color:#c8f0c8">安裝檢查：</mark>

- <mark style="background-color:#f8c8c8">`just vendor_kit test`：跑全部檢查</mark>
- <mark style="background-color:#f8c8c8">`just vendor_kit test dist`：只檢查工具交付的內容，給提供工具的 repo 在自己的 CI 用。幾乎一定已經存在的那類初始檔若不用 append 型、改用整份複製，會被它擋下</mark>
- <mark style="background-color:#c8f0c8">檢查版本、快取與初始檔的一致性，不準備或修復 cache、gen、進度檔，不寫追蹤檔；執行紀錄照 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark>
- <mark style="background-color:#c8f0c8">本機覆寫仍會擋下；基準版落後、缺件、環境不足等結果與下一步見[訊息表](../../contract/reason_codes.csv)</mark>
- <mark style="background-color:#c8f0c8">全新 checkout 缺 cache 的處理仍待確認，見[嚴格檢查決議](https://github.com/ycpss91255-research/vendor_kit/issues/124)</mark>

<mark style="background-color:#f8c8c8">沒有工具的安裝目錄仍檢查薄殼與引擎，通過就回 `0`；`test dist` 沒有交付內容時以 `VK0048`／`2` 結束。環境不足使檢查做不完時，以 `VK0049`／`2` 指名原因；cache 或 gen 缺件時以 `VK0047`／`2` 報待處理，下一步指向 `sync`，不先修復再把異常當成通過。檢查完成而報出異常時，依 [03 結束碼](../../contract/03_output.md#結束碼)分級。</mark>
### test 路徑與 runner
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#f8c8c8">`test` 的嚴格規則不因執行環境改變：</mark>
- <mark style="background-color:#c8f0c8">一次只收一個 path，寫成 `test/...`，從安裝目錄算起；指定檔案只跑該檔；指定資料夾含子資料夾。安裝目錄不在 repo 根目錄時，repo 根目錄的 `test/` 不屬於它</mark>
- <mark style="background-color:#c8f0c8">依 VK 紀錄判定工具交付的測試；使用者改過也算。選中範圍含工具交付的內容（整份初始檔或插入行）就整次不跑；工具移除後才可按使用者測試處理</mark>
- <mark style="background-color:#c8f0c8">完整安裝檢查的結果不是 `0` 就不啟動 runner，整次以 `max(檢查碼, 2)` 結束；結果與下一步見訊息表</mark>
- <mark style="background-color:#c8f0c8">使用者依[設定](#設定)在 `[test]` 指定 `image` 與 `command`，VK 不內建 runner</mark>
- <mark style="background-color:#c8f0c8">通過檢查後，在該 image 容器執行 command 並在最後加上 path，不經 shell；工作目錄為安裝目錄，repo 唯讀掛載，以空目錄遮住 `.vendor_kit/`，runner 另有容器內的可寫暫存空間，結束即丟，寫不進 repo</mark>
- <mark style="background-color:#c8f0c8">測試 image 不限 registry，由主機 Docker 取得，也可用本機 image；image 與 command 實際執行什麼由使用者負責</mark>
- <mark style="background-color:#c8f0c8">runner 的 stdout、stderr 原樣轉出，格式界線見 [03 輸出](../../contract/03_output.md#輸出)</mark>
- <mark style="background-color:#c8f0c8">path 無效、未選到測試、選到工具交付檔、runner 起不來或測試未通過的處置與結束碼，見[訊息表](../../contract/reason_codes.csv)</mark>

- <mark style="background-color:#f8c8c8">基準版落後版本鎖定行時，在 stderr 印出 [訊息](../../contract/reason_codes.csv) `VK0014` 的 `warn` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `1` 結束，並指出該執行的 `upgrade` 指令。</mark>
- <mark style="background-color:#f8c8c8">發現任何本機覆寫時，在 stderr 印出 [訊息](../../contract/reason_codes.csv) `VK0032` 的 `error` 診斷，以[結束碼](../../contract/03_output.md#結束碼) `2` 結束，並指出該執行的 `undev` 指令。這是 VK 自己的規則：覆寫期間內容不由版本鎖定行決定，不在決定性重建的承諾內。</mark>
<mark style="background-color:#f8c8c8">其他結束碼也是 `0`～`3`，意思見 [03 輸出](../../contract/03_output.md#結束碼)。</mark>
