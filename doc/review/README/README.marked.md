<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除，程式碼區塊的改動改成 diff 區塊（+ 新增、- 刪除）；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit 5770e20。正式內容看 /README.md -->

# vendor_kit

vendor_kit ([VK](../../../GLOSSARY.md#角色與情境)) 把一套[工具](../../../GLOSSARY.md#工具與出貨)送進很多個 [repo](../../../GLOSSARY.md#工具與出貨)，例如開發環境設定、共用腳本、[初始檔](../../../GLOSSARY.md#初始檔與合併)。它記住每個[安裝目錄](../../../GLOSSARY.md#工具與出貨)用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。

## 目錄

- [開始之前](#開始之前)
- [使用方式](#使用方式)
- [文件](#文件)

## 開始之前

### 主機需求

除平台本來就有的 shell 與基本指令外，主機只需要這三個（詳見 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)）：

- [Docker](https://www.docker.com/)
  - 19.03 以上
  - 不支援 Podman
- [Git](https://git-scm.com/)
  - 不設最低版本
  - VK 不在主機上呼叫 git
  - <mark style="background-color:#f8c8c8">「安裝目錄在 git repo 裡」由[啟動器](../../../GLOSSARY.md#vk-組件)用 sh 往上找 `.git` 判斷</mark>
  - <mark style="background-color:#c8f0c8">「安裝目錄在 git repo 裡」由[啟動器](../../../GLOSSARY.md#vk-組件)用 bash 往上找 `.git` 判斷</mark>
- [just](https://github.com/casey/just)
  - 1.33.0 以上
  - 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)

版本不足時：

- Docker 版本不足：在任何寫入之前結束
- <mark style="background-color:#f8c8c8">just 版本不足：首次[導入](../../../GLOSSARY.md#角色與情境)時，`bootstrap.sh` 在任何寫入之前結束，並印出下載與安裝指令；已有安裝目錄時，由 just 自己報錯。詳細行為與結束碼見 [04 使用者介面](../../contract/04_interface.md#主機需求)</mark>
- <mark style="background-color:#c8f0c8">just 版本不足：首次[導入](../../../GLOSSARY.md#角色與情境)時，`bootstrap.sh` 在任何寫入之前結束，並印出下載與安裝指令；已有安裝目錄時，由 just 自己報錯。詳細行為見 [04 使用者介面](../../contract/04_interface.md#主機需求)，[診斷](../../../GLOSSARY.md#執行與結果)與[結束碼](../../../GLOSSARY.md#執行與結果)見[訊息表](../../contract/reason_codes.csv)</mark>

### 第一次導入

> <mark style="background-color:#f8c8c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會[失敗](../../../GLOSSARY.md#執行與結果)。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>
> <mark style="background-color:#c8f0c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>

<mark style="background-color:#f8c8c8">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（詳見 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化不寫追蹤檔)）。</mark>
<mark style="background-color:#c8f0c8">發布之後，先在 [VK Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)選版本，把下面的 `vX.Y.Z` 換成選定版號，再在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（詳見 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化不寫追蹤檔)）。</mark>

```diff
-curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh
-sh bootstrap.sh
+vk_version=vX.Y.Z
+wget -O bootstrap.sh "https://github.com/ycpss91255-research/vendor_kit/releases/download/${vk_version}/bootstrap.sh" || exit $?
+chmod +x bootstrap.sh
+./bootstrap.sh
```

<mark style="background-color:#f8c8c8">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載[引擎](../../../GLOSSARY.md#vk-組件)，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>
<mark style="background-color:#c8f0c8">沒有 `wget` 也可以用瀏覽器下載選定版本的同一個網址。`bootstrap.sh` 會下載[引擎](../../../GLOSSARY.md#vk-組件)，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>

## 使用方式

```diff
-Usage: just vendor_kit <command> [arguments] [options]
+Usage: just vendor_kit <cmd> [arguments] [options]

 Common commands:
   add <repo>                  Import a tool into this install directory
   add <repo>@<tag>            Import a specified version without listing versions
   upgrade <repo>              Upgrade the locked version to a newer version
   upgrade <repo>@<tag>        Switch to a specified version; an older tag downgrades the tool
   dev <repo> -p <dir>         Use a local directory for the tool
   dev --engine -i <image>     Use a local image for the engine
```

- 每個指令都支援 `-h`／`--help`，印出該指令的用法
- 進階指令與選項見 [04 使用者介面](../../contract/04_interface.md)
- [結束碼](../../../GLOSSARY.md#執行與結果)與訊息見 [03 輸出](../../contract/03_output.md)

### Renovate 整合
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#c8f0c8">VK 提供 Renovate regex preset。[使用者](../../../GLOSSARY.md#角色與情境)在自己的 Renovate 設定中啟用這份 preset，由 Renovate 追蹤工具與引擎的正式版，並開 PR 修改[版本鎖定行](../../../GLOSSARY.md#版本與來源)。</mark>

> <mark style="background-color:#c8f0c8">尚未可用：preset 尚未發布，Renovate 設定的 `extends` 引用值待發布時提供。進度見 [issue #25](https://github.com/ycpss91255-research/vendor_kit/issues/25)。</mark>

<mark style="background-color:#c8f0c8">Renovate 開出工具的 PR 後，使用者在本機切到該 PR 分支，執行 `just vendor_kit upgrade <repo> -y`，再自行 commit、push；CI 通過後才 merge。引擎 PR 的收尾流程待確認，見 [issue #370](https://github.com/ycpss91255-research/vendor_kit/issues/370)。指令見 [04 使用者介面](../../contract/04_interface.md)；VK 對 preset 的承諾見 [04 使用者介面的追蹤新版](../../contract/04_interface.md#追蹤新版)。</mark>

## 文件

- [01 目的與承諾](../../contract/01_purpose.md)：為什麼做 VK，對使用者承諾什麼
- [02 不變量](../../contract/02_invariants.md)：任何版本都必須成立的規則
- [03 輸出](../../contract/03_output.md)：每個結束碼的意思，與每條[診斷](../../../GLOSSARY.md#執行與結果)的格式
- [04 使用者介面](../../contract/04_interface.md)：全部指令與選項
- [名詞表](../../../GLOSSARY.md)
- [架構決議 (ADR)](../../adr/)

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
