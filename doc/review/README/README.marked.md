<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit ccde94f。正式內容看 /README.md -->

# vendor_kit

<mark style="background-color:#f8c8c8">vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個安裝目錄用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</mark>
<mark style="background-color:#c8f0c8">vendor_kit ([VK](../../../GLOSSARY.md#角色與情境)) 把一套[工具](../../../GLOSSARY.md#工具與出貨)送進很多個 [repo](../../../GLOSSARY.md#工具與出貨)，例如開發環境設定、共用腳本、[初始檔](../../../GLOSSARY.md#初始檔與合併)。它記住每個[安裝目錄](../../../GLOSSARY.md#工具與出貨)用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</mark>

## 目錄

- [開始之前](#開始之前)
- [使用方式](#使用方式)
- [文件](#文件)

## 開始之前

### 主機需求

<mark style="background-color:#f8c8c8">依 [02 不變量](../../decisions/review/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條，主機只需要這三個：</mark>
<mark style="background-color:#c8f0c8">除平台本來就有的 shell 與基本指令外，主機只需要這三個（詳見 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)）：</mark>

- [Docker](https://www.docker.com/)
  - 19.03 以上
  - 不支援 Podman
- [Git](https://git-scm.com/)
  - 不設最低版本
  - <mark style="background-color:#f8c8c8">VK 不呼叫 git</mark>
  - <mark style="background-color:#f8c8c8">「安裝目錄在 git repo 裡」由啟動器用 sh 往上找 `.git` 判斷</mark>
  - <mark style="background-color:#c8f0c8">VK 不在主機上呼叫 git</mark>
  - <mark style="background-color:#c8f0c8">「安裝目錄在 git repo 裡」由[啟動器](../../../GLOSSARY.md#vk-組件)用 sh 往上找 `.git` 判斷</mark>
- [just](https://github.com/casey/just)
  - 1.33.0 以上
  - 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)

版本不足時：

- <mark style="background-color:#f8c8c8">Docker 或 just 版本不足，都在任何寫入之前以 `1` 結束</mark>
- <mark style="background-color:#f8c8c8">只有 just 版本不足時，另外印出下載與安裝指令</mark>
- <mark style="background-color:#c8f0c8">Docker 版本不足：在任何寫入之前結束</mark>
- <mark style="background-color:#c8f0c8">just 版本不足：首次[導入](../../../GLOSSARY.md#角色與情境)時，`bootstrap.sh` 在任何寫入之前結束，並印出下載與安裝指令；已有安裝目錄時，由 just 自己報錯。詳細行為與結束碼見 [04 使用者介面](../../contract/04_interface.md#主機需求)</mark>

### 第一次導入

> <mark style="background-color:#f8c8c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會失敗。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>
> <mark style="background-color:#c8f0c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會[失敗](../../../GLOSSARY.md#執行與結果)。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>

<mark style="background-color:#f8c8c8">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡，依 [02 不變量](../../decisions/review/02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條。</mark>
<mark style="background-color:#c8f0c8">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（詳見 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化不寫追蹤檔)）。</mark>

```sh
curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh
sh bootstrap.sh
```

<mark style="background-color:#f8c8c8">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載引擎，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>
<mark style="background-color:#c8f0c8">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載[引擎](../../../GLOSSARY.md#vk-組件)，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>

## 使用方式

```
<mark style="background-color:#f8c8c8">用法：just vendor_kit <指令> [參數] [選項]</mark>
<mark style="background-color:#c8f0c8">Usage: just vendor_kit <command> [arguments] [options]</mark>

<mark style="background-color:#f8c8c8">常用指令：</mark>
  <mark style="background-color:#f8c8c8">add <repo>                  把一個工具納入這個安裝目錄</mark>
  <mark style="background-color:#f8c8c8">upgrade <repo>              把鎖定版本換成新版</mark>
  <mark style="background-color:#f8c8c8">upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版</mark>
  <mark style="background-color:#f8c8c8">dev <repo> -p <dir>         讓工具改用本機目錄</mark>
  <mark style="background-color:#f8c8c8">dev --engine -i <image>     讓引擎改用本機 image</mark>
<mark style="background-color:#c8f0c8">Common commands:</mark>
  <mark style="background-color:#c8f0c8">add <repo>                  Import a tool into this install directory</mark>
  <mark style="background-color:#c8f0c8">add <repo>@<tag>            Import a specified version without listing versions</mark>
  <mark style="background-color:#c8f0c8">upgrade <repo>              Upgrade the locked version to a newer version</mark>
  <mark style="background-color:#c8f0c8">upgrade <repo>@<tag>        Switch to a specified version; an older tag downgrades the tool</mark>
  <mark style="background-color:#c8f0c8">dev <repo> -p <dir>         Use a local directory for the tool</mark>
  <mark style="background-color:#c8f0c8">dev --engine -i <image>     Use a local image for the engine</mark>
```

- 每個指令都支援 `-h`／`--help`，印出該指令的用法
- <mark style="background-color:#f8c8c8">進階指令與選項見 [04 使用者介面](../../decisions/review/04_interface.md)</mark>
- <mark style="background-color:#f8c8c8">結束碼與訊息見 [03 訊息與錯誤碼總表](../../decisions/review/03_messages.md)</mark>
- <mark style="background-color:#c8f0c8">進階指令與選項見 [04 使用者介面](../../contract/04_interface.md)</mark>
- <mark style="background-color:#c8f0c8">[結束碼](../../../GLOSSARY.md#執行與結果)與訊息見 [03 輸出](../../contract/03_output.md)</mark>

## 文件

- <mark style="background-color:#f8c8c8">[01 目的與承諾](../../decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</mark>
- <mark style="background-color:#f8c8c8">[02 不變量](../../decisions/review/02_invariants.md)：任何版本都必須成立的規則</mark>
- <mark style="background-color:#f8c8c8">[03 訊息與錯誤碼總表](../../decisions/review/03_messages.md)：每個結束碼的意思，與要使用者動手處理的訊息</mark>
- <mark style="background-color:#f8c8c8">[04 使用者介面](../../decisions/review/04_interface.md)：全部指令與選項</mark>
- <mark style="background-color:#f8c8c8">[名詞表](../../../CONTEXT.md)</mark>
- <mark style="background-color:#f8c8c8">[架構決議（ADR）](../../adr/)</mark>
- <mark style="background-color:#c8f0c8">[01 目的與承諾](../../contract/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</mark>
- <mark style="background-color:#c8f0c8">[02 不變量](../../contract/02_invariants.md)：任何版本都必須成立的規則</mark>
- <mark style="background-color:#c8f0c8">[03 輸出](../../contract/03_output.md)：每個結束碼的意思，與每條[診斷](../../../GLOSSARY.md#執行與結果)的格式</mark>
- <mark style="background-color:#c8f0c8">[04 使用者介面](../../contract/04_interface.md)：全部指令與選項</mark>
- <mark style="background-color:#c8f0c8">[名詞表](../../../GLOSSARY.md)</mark>
- <mark style="background-color:#c8f0c8">[架構決議 (ADR)](../../adr/)</mark>

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
