# vendor_kit

vendor_kit（VK）把一套工具送進很多個 repo，例如開發環境設定、共用腳本、初始檔。它記住每個 repo 用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。

## 使用方式

```
用法：just vendor_kit <指令> [參數] [選項]

常用指令：
  add <repo>                  把一個工具納入這個安裝目錄
  upgrade <repo>[@<tag>]      換成新版；指定 tag 就換成那一版，指定舊 tag 就是退版
  dev <repo> -p <dir>         讓工具改用本機目錄
  dev vendor_kit -i <image>   讓引擎改用本機 image
```

進階指令、選項與結束碼見[使用者介面](doc/decisions/review/03_interface.md)。第一次導入時 repo 裡還沒有 VK，先跑 `bootstrap.sh`。

## 文件

- [目的與承諾](doc/decisions/review/01_purpose.md)：為什麼做 VK，對使用者承諾什麼
- [不變量](doc/decisions/review/02_invariants.md)：任何版本都必須成立的規則
- [使用者介面](doc/decisions/review/03_interface.md)：全部指令、選項與結束碼
- [名詞表](CONTEXT.md)
- [架構決議（ADR）](doc/adr/)

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
