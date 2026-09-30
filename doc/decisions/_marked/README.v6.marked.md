<!-- 標示版 v6：綠底 <mark> 是新文字、紅底刪除線 <del> 是被取代的舊文字；底線 <ins> 是名詞標記；本檔只供本地 review，不進 git；基準 pre_r104。正式內容看 /README.md -->

# vendor_kit

> <del style="background:#ffc9c9">版本 v5</del>
<mark style="background:#c8f7c5">vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個安裝目錄用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</mark>

<del style="background:#ffc9c9">vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個安裝目錄用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</del>
## <mark style="background:#c8f7c5">目錄</mark>

- <mark style="background:#c8f7c5">[開始之前](#開始之前)</mark>
- <mark style="background:#c8f7c5">[使用方式](#使用方式)</mark>
- <mark style="background:#c8f7c5">[文件](#文件)</mark>

## 開始之前

### 主機需求

<mark style="background:#c8f7c5">依 [02 不變量](doc/decisions/review/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條，主機只需要這三個：</mark>

- [Docker](https://www.docker.com/)
  - 19.03 以上
  - 不支援 Podman
- [Git](https://git-scm.com/)
  - 不設最低版本
  - VK 不呼叫 git
  - 「安裝目錄在 git repo 裡」由啟動器用 sh 往上找 `.git` 判斷
- [just](https://github.com/casey/just)
  - 1.33.0 以上
  - 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)

版本不足時：

- <del style="background:#ffc9c9">在任何寫入之前以 `1` 結束</del>
- <del style="background:#ffc9c9">印出安裝指令</del>
<del style="background:#ffc9c9">出處：[ADR-0007](doc/adr/0007-host-thin-layer-and-shell-integrity.md) §1；[不變量](doc/decisions/review/02_invariants.md)第 5 條；Git 見 [issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71)。</del>
- <mark style="background:#c8f7c5">Docker 或 just 版本不足，都在任何寫入之前以 `1` 結束</mark>
- <mark style="background:#c8f7c5">只有 just 版本不足時，另外印出下載與安裝指令</mark>

### 第一次導入

> 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會失敗。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

<del style="background:#ffc9c9">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（[不變量](doc/decisions/review/02_invariants.md)第 3 條）。</del>
<mark style="background:#c8f7c5">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡，依 [02 不變量](doc/decisions/review/02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條。</mark>

```sh
curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh
sh bootstrap.sh
```

<del style="background:#ffc9c9">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載引擎，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。下載網址出處：[issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</del>
<mark style="background:#c8f7c5">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載引擎，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>

## 使用方式

```
用法：just vendor_kit <指令> [參數] [選項]

常用指令：
  add <repo>                  把一個工具納入這個安裝目錄
  upgrade <repo>              把鎖定版本換成新版
  upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版
  dev <repo> -p <dir>         讓工具改用本機目錄
  dev --engine -i <image>     讓引擎改用本機 image
```

- 每個指令都支援 `-h`／`--help`，印出該指令的用法
- <del style="background:#ffc9c9">進階指令、選項與結束碼見[使用者介面](doc/decisions/review/03_interface.md)</del>
- <mark style="background:#c8f7c5">進階指令與選項見 [04 使用者介面](doc/decisions/review/04_interface.md)</mark>
- <mark style="background:#c8f7c5">結束碼與訊息見 [03 訊息與錯誤碼總表](doc/decisions/review/03_messages.md)</mark>

## 文件

- <del style="background:#ffc9c9">[目的與承諾](doc/decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</del>
- <del style="background:#ffc9c9">[不變量](doc/decisions/review/02_invariants.md)：任何版本都必須成立的規則</del>
- <del style="background:#ffc9c9">[使用者介面](doc/decisions/review/03_interface.md)：全部指令、選項與結束碼</del>
- <mark style="background:#c8f7c5">[01 目的與承諾](doc/decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</mark>
- <mark style="background:#c8f7c5">[02 不變量](doc/decisions/review/02_invariants.md)：任何版本都必須成立的規則</mark>
- <mark style="background:#c8f7c5">[03 訊息與錯誤碼總表](doc/decisions/review/03_messages.md)：每個結束碼的意思，與要使用者動手處理的訊息</mark>
- <mark style="background:#c8f7c5">[04 使用者介面](doc/decisions/review/04_interface.md)：全部指令與選項</mark>
- [名詞表](CONTEXT.md)
- [架構決議（ADR）](doc/adr/)

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
