# vendor_kit

vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個安裝目錄用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。

## 開始之前

### 主機需求

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

- 在任何寫入之前以 `1` 結束
- 印出安裝指令

出處：[ADR-0007](doc/adr/0007-host-thin-layer-and-shell-integrity.md) §1；[不變量](doc/decisions/review/02_invariants.md)第 5 條；Git 見 [issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71)。

### 第一次導入

> 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會失敗。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（[不變量](doc/decisions/review/02_invariants.md)第 3 條）。

```sh
curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh
sh bootstrap.sh
```

沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載引擎，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。下載網址出處：[issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

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
- 進階指令、選項與結束碼見[使用者介面](doc/decisions/review/03_interface.md)

## 文件

- [目的與承諾](doc/decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼
- [不變量](doc/decisions/review/02_invariants.md)：任何版本都必須成立的規則
- [使用者介面](doc/decisions/review/03_interface.md)：全部指令、選項與結束碼
- [名詞表](CONTEXT.md)
- [架構決議（ADR）](doc/adr/)

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
