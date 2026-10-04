<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除，程式碼區塊的改動改成 diff 區塊（+ 新增、- 刪除）；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit 5770e20。正式內容看 /README.md -->

# vendor_kit

<mark style="background-color:#f8c8c8">vendor_kit ([VK](../../../GLOSSARY.md#角色與情境)) 把一套[工具](../../../GLOSSARY.md#工具與出貨)送進很多個 [repo](../../../GLOSSARY.md#工具與出貨)，例如開發環境設定、共用腳本、[初始檔](../../../GLOSSARY.md#初始檔與合併)。它記住每個[安裝目錄](../../../GLOSSARY.md#工具與出貨)用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。</mark>
<mark style="background-color:#c8f0c8">vendor_kit ([VK](../../../GLOSSARY.md#角色與情境)) 把一套[工具](../../../GLOSSARY.md#工具與出貨)送進很多個 [repo](../../../GLOSSARY.md#工具與出貨)，例如開發環境設定、共用腳本、[初始檔](../../../GLOSSARY.md#初始檔與合併)。它記住每個[安裝目錄](../../../GLOSSARY.md#工具與出貨)用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機需求見 04 的[主機需求](../../contract/04_interface.md#主機需求)。</mark>

## 目錄

- <mark style="background-color:#f8c8c8">[開始之前](#開始之前)</mark>
- <mark style="background-color:#f8c8c8">[使用方式](#使用方式)</mark>
- <mark style="background-color:#f8c8c8">[文件](#文件)</mark>
| <mark style="background-color:#c8f0c8">章節</mark> | <mark style="background-color:#c8f0c8">內容</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">[快速開始](#快速開始)</mark> | <mark style="background-color:#c8f0c8">從安裝到工具升版</mark> |
| <mark style="background-color:#c8f0c8">[常用指令](#常用指令)</mark> | <mark style="background-color:#c8f0c8">日常呼叫與詳細說明</mark> |
| <mark style="background-color:#c8f0c8">[Renovate 整合](#renovate-整合)</mark> | <mark style="background-color:#c8f0c8">新版追蹤與發布進度</mark> |
| <mark style="background-color:#c8f0c8">[文件](#文件)</mark> | <mark style="background-color:#c8f0c8">[契約](../../../GLOSSARY.md#介面版與契約)與參考資料</mark> |

## 快速開始
<mark style="background-color:#f8c8c8">舊標題：開始之前</mark>
<mark style="background-color:#c8f0c8">（標題已修改）</mark>

<mark style="background-color:#f8c8c8">主機需求</mark>
> <mark style="background-color:#c8f0c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>

<mark style="background-color:#f8c8c8">除平台本來就有的 shell 與基本指令外，主機只需要這三個（詳見 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)）：</mark>
| <mark style="background-color:#c8f0c8">步驟</mark> | <mark style="background-color:#c8f0c8">做什麼</mark> | <mark style="background-color:#c8f0c8">指令</mark> | <mark style="background-color:#c8f0c8">詳見</mark> |
|---|---|---|---|
| <mark style="background-color:#c8f0c8">1</mark> | <mark style="background-color:#c8f0c8">確認主機符合需求</mark> | <mark style="background-color:#c8f0c8">—</mark> | <mark style="background-color:#c8f0c8">[主機需求](../../contract/04_interface.md#主機需求)</mark> |
| <mark style="background-color:#c8f0c8">2</mark> | <mark style="background-color:#c8f0c8">依 04 的取得與執行流程，下載 `bootstrap.sh` 到目前目錄，再到目標目錄執行</mark> | <mark style="background-color:#c8f0c8">見下方程式碼</mark> | <mark style="background-color:#c8f0c8">[入口](../../contract/04_interface.md#入口)、[腳本用法](../../contract/04_interface.md#bootstrapsh)</mark> |
| <mark style="background-color:#c8f0c8">3</mark> | <mark style="background-color:#c8f0c8">用 [add](../../../GLOSSARY.md#vk-recipe-與用途) [導入](../../../GLOSSARY.md#角色與情境)工具</mark> | <mark style="background-color:#c8f0c8">`just vendor_kit add <repo>`</mark> | <mark style="background-color:#c8f0c8">[指令](../../contract/04_interface.md#指令)</mark> |
| <mark style="background-color:#c8f0c8">4</mark> | <mark style="background-color:#c8f0c8">用 [upgrade](../../../GLOSSARY.md#vk-recipe-與用途) 升版工具</mark> | <mark style="background-color:#c8f0c8">`just vendor_kit upgrade <repo>`</mark> | <mark style="background-color:#c8f0c8">[指令](../../contract/04_interface.md#指令)</mark> |

- <mark style="background-color:#f8c8c8">[Docker](https://www.docker.com/)</mark>
  - <mark style="background-color:#f8c8c8">19.03 以上</mark>
  - <mark style="background-color:#f8c8c8">不支援 Podman</mark>
- <mark style="background-color:#f8c8c8">[Git](https://git-scm.com/)</mark>
  - <mark style="background-color:#f8c8c8">不設最低版本</mark>
  - <mark style="background-color:#f8c8c8">VK 不在主機上呼叫 git</mark>
  - <mark style="background-color:#f8c8c8">「安裝目錄在 git repo 裡」由[啟動器](../../../GLOSSARY.md#vk-組件)用 sh 往上找 `.git` 判斷</mark>
- <mark style="background-color:#f8c8c8">[just](https://github.com/casey/just)</mark>
  - <mark style="background-color:#f8c8c8">1.33.0 以上</mark>
  - <mark style="background-color:#f8c8c8">用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)</mark>
<mark style="background-color:#f8c8c8">版本不足時：</mark>
- <mark style="background-color:#f8c8c8">Docker 版本不足：在任何寫入之前結束</mark>
- <mark style="background-color:#f8c8c8">just 版本不足：首次[導入](../../../GLOSSARY.md#角色與情境)時，`bootstrap.sh` 在任何寫入之前結束，並印出下載與安裝指令；已有安裝目錄時，由 just 自己報錯。詳細行為與結束碼見 [04 使用者介面](../../contract/04_interface.md#主機需求)</mark>
<mark style="background-color:#f8c8c8">第一次導入</mark>
> <mark style="background-color:#f8c8c8">尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案，照做會[失敗](../../../GLOSSARY.md#執行與結果)。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。</mark>
<mark style="background-color:#f8c8c8">發布之後，在要裝 VK 的那個目錄下載並執行 `bootstrap.sh`。這個目錄必須在某個 git repo 裡（詳見 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化不寫追蹤檔)）。</mark>
```diff
-curl -fsSLO https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh
-sh bootstrap.sh
+wget -O bootstrap.sh "https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh" || exit $?
+vk_bootstrap="$PWD/bootstrap.sh"
+chmod +x "$vk_bootstrap"
+cd <目標目錄>
+"$vk_bootstrap"
```

<mark style="background-color:#f8c8c8">沒有 `curl` 也可以用瀏覽器下載同一個網址。`bootstrap.sh` 會下載[引擎](../../../GLOSSARY.md#vk-組件)，再呼叫 `install`；之後就用下面 `just vendor_kit` 的指令。</mark>
## 常用指令
<mark style="background-color:#c8f0c8">（本節新增）</mark>

<mark style="background-color:#f8c8c8">使用方式</mark>
| <mark style="background-color:#c8f0c8">呼叫</mark> | <mark style="background-color:#c8f0c8">功能</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">[just vendor_kit add \<repo\>](../../contract/04_interface.md#指令)</mark> | <mark style="background-color:#c8f0c8">導入工具（最新版）</mark> |
| <mark style="background-color:#c8f0c8">[just vendor_kit upgrade \<repo\>](../../contract/04_interface.md#指令)</mark> | <mark style="background-color:#c8f0c8">升降工具版本</mark> |
| <mark style="background-color:#c8f0c8">[just vendor_kit update](../../contract/04_interface.md#update)、[just vendor_kit update \<repo\>](../../contract/04_interface.md#update)</mark> | <mark style="background-color:#c8f0c8">查新版</mark> |

```diff
-Usage: just vendor_kit <command> [arguments] [options]
```
<mark style="background-color:#c8f0c8">全部呼叫與選項見 04 的[指令](../../contract/04_interface.md#指令)；`-h`／`--help` 的用法見[說明與用法錯誤](../../contract/04_interface.md#說明與用法錯誤)，[結束碼](../../../GLOSSARY.md#執行與結果)與訊息見 [03 輸出](../../contract/03_output.md)。</mark>

```diff
-Common commands:
-  add <repo>                  Import a tool into this install directory
-  add <repo>@<tag>            Import a specified version without listing versions
-  upgrade <repo>              Upgrade the locked version to a newer version
-  upgrade <repo>@<tag>        Switch to a specified version; an older tag downgrades the tool
-  dev <repo> -p <dir>         Use a local directory for the tool
-  dev --engine -i <image>     Use a local image for the engine
```
## Renovate 整合
<mark style="background-color:#c8f0c8">（本節新增）</mark>

- <mark style="background-color:#f8c8c8">每個指令都支援 `-h`／`--help`，印出該指令的用法</mark>
- <mark style="background-color:#f8c8c8">進階指令與選項見 [04 使用者介面](../../contract/04_interface.md)</mark>
- <mark style="background-color:#f8c8c8">[結束碼](../../../GLOSSARY.md#執行與結果)與訊息見 [03 輸出](../../contract/03_output.md)</mark>
<mark style="background-color:#c8f0c8">Renovate preset 尚未發布，發布進度見 [issue #25](https://github.com/ycpss91255-research/vendor_kit/issues/25)，`extends` 引用值待發布時提供；VK 對 preset 的承諾見 04 的[追蹤新版](../../contract/04_interface.md#追蹤新版)。</mark>

<mark style="background-color:#c8f0c8">Renovate 開出的工具 PR，依下列流程收尾：</mark>

| <mark style="background-color:#c8f0c8">步驟</mark> | <mark style="background-color:#c8f0c8">做什麼</mark> | <mark style="background-color:#c8f0c8">指令</mark> |
|---|---|---|
| <mark style="background-color:#c8f0c8">1</mark> | <mark style="background-color:#c8f0c8">在本機切到 Renovate 開出的 PR 分支</mark> | <mark style="background-color:#c8f0c8">`git switch <PR 分支>`</mark> |
| <mark style="background-color:#c8f0c8">2</mark> | <mark style="background-color:#c8f0c8">完成工具升版</mark> | <mark style="background-color:#c8f0c8">`just vendor_kit upgrade <repo> -y`</mark> |
| <mark style="background-color:#c8f0c8">3</mark> | <mark style="background-color:#c8f0c8">自己 commit、push</mark> | <mark style="background-color:#c8f0c8">`git commit`、`git push`</mark> |
| <mark style="background-color:#c8f0c8">4</mark> | <mark style="background-color:#c8f0c8">CI 通過才 merge</mark> | <mark style="background-color:#c8f0c8">—</mark> |

<mark style="background-color:#c8f0c8">[引擎](../../../GLOSSARY.md#vk-組件) PR 的收尾流程待確認，見 [issue #370](https://github.com/ycpss91255-research/vendor_kit/issues/370)。</mark>

## 文件

- <mark style="background-color:#f8c8c8">[01 目的與承諾](../../contract/01_purpose.md)：為什麼做 VK，對使用者承諾什麼</mark>
- <mark style="background-color:#f8c8c8">[02 不變量](../../contract/02_invariants.md)：任何版本都必須成立的規則</mark>
- <mark style="background-color:#f8c8c8">[03 輸出](../../contract/03_output.md)：每個結束碼的意思，與每條[診斷](../../../GLOSSARY.md#執行與結果)的格式</mark>
- <mark style="background-color:#f8c8c8">[04 使用者介面](../../contract/04_interface.md)：全部指令與選項</mark>
- <mark style="background-color:#f8c8c8">[名詞表](../../../GLOSSARY.md)</mark>
- <mark style="background-color:#f8c8c8">[架構決議 (ADR)](../../adr/)</mark>
| <mark style="background-color:#c8f0c8">文件</mark> | <mark style="background-color:#c8f0c8">內容</mark> |
|---|---|
| <mark style="background-color:#c8f0c8">[01 目的與承諾](../../contract/01_purpose.md)</mark> | <mark style="background-color:#c8f0c8">為什麼做 VK，對使用者承諾什麼</mark> |
| <mark style="background-color:#c8f0c8">[02 不變量](../../contract/02_invariants.md)</mark> | <mark style="background-color:#c8f0c8">任何版本都必須成立的規則</mark> |
| <mark style="background-color:#c8f0c8">[03 輸出](../../contract/03_output.md)</mark> | <mark style="background-color:#c8f0c8">結束碼與訊息格式</mark> |
| <mark style="background-color:#c8f0c8">[04 使用者介面](../../contract/04_interface.md)</mark> | <mark style="background-color:#c8f0c8">全部指令與選項</mark> |
| <mark style="background-color:#c8f0c8">[訊息表](../../contract/reason_codes.csv)</mark> | <mark style="background-color:#c8f0c8">逐項診斷、處置與結束碼</mark> |
| <mark style="background-color:#c8f0c8">[名詞表](../../../GLOSSARY.md)</mark> | <mark style="background-color:#c8f0c8">專有名詞與用語</mark> |
| <mark style="background-color:#c8f0c8">[架構決議 (ADR)](../../adr/)</mark> | <mark style="background-color:#c8f0c8">設計決定與理由</mark> |

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
