# vendor_kit

vendor_kit ([VK](../../../GLOSSARY.md#角色與情境)) 把一套[工具](../../../GLOSSARY.md#工具與出貨)送進很多個 [repo](../../../GLOSSARY.md#工具與出貨)，例如開發環境設定、共用腳本、[初始檔](../../../GLOSSARY.md#初始檔與合併)。它記住每個[安裝目錄](../../../GLOSSARY.md#工具與出貨)用哪一版，可以升版，也可以退版；升版時不會蓋掉你改過的初始檔。主機需求見 04 的[主機需求](../../contract/04_interface.md#主機需求)。

## 目錄

| 章節 | 內容 |
|---|---|
| [快速開始](#快速開始) | 從安裝到工具升版 |
| [常用指令](#常用指令) | 日常呼叫與詳細說明 |
| [Renovate 整合](#renovate-整合) | 新版追蹤與發布進度 |
| [文件](#文件) | [契約](../../../GLOSSARY.md#介面版與契約)與參考資料 |

## 快速開始

> 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，下面的網址目前找不到檔案。進度見 [issue #27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

| 步驟 | 做什麼 | 指令 | 詳見 |
|---|---|---|---|
| 1 | 確認主機符合需求 | — | [主機需求](../../contract/04_interface.md#主機需求) |
| 2 | 依 04 的取得與執行流程，下載 `bootstrap.sh` 到目前目錄，再到目標目錄執行 | 見下方程式碼 | [入口](../../contract/04_interface.md#入口)、[腳本用法](../../contract/04_interface.md#bootstrapsh) |
| 3 | 用 [add](../../../GLOSSARY.md#vk-recipe-與用途) [導入](../../../GLOSSARY.md#角色與情境)工具 | `just vendor_kit add <repo>` | [指令](../../contract/04_interface.md#指令) |
| 4 | 用 [upgrade](../../../GLOSSARY.md#vk-recipe-與用途) 升版工具 | `just vendor_kit upgrade <repo>` | [指令](../../contract/04_interface.md#指令) |

```bash
wget -O bootstrap.sh "https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh" || exit $?
vk_bootstrap="$PWD/bootstrap.sh"
chmod +x "$vk_bootstrap"
cd <目標目錄>
"$vk_bootstrap"
```

## 常用指令

| 呼叫 | 功能 |
|---|---|
| [just vendor_kit add \<repo\>](../../contract/04_interface.md#指令) | 導入工具（最新版） |
| [just vendor_kit upgrade \<repo\>](../../contract/04_interface.md#指令) | 升降工具版本 |
| [just vendor_kit update](../../contract/04_interface.md#update)、[just vendor_kit update \<repo\>](../../contract/04_interface.md#update) | 查新版 |

全部呼叫與選項見 04 的[指令](../../contract/04_interface.md#指令)；`-h`／`--help` 的用法見[說明與用法錯誤](../../contract/04_interface.md#說明與用法錯誤)，[結束碼](../../../GLOSSARY.md#執行與結果)與訊息見 [03 輸出](../../contract/03_output.md)。

## Renovate 整合

Renovate preset 尚未發布，發布進度見 [issue #25](https://github.com/ycpss91255-research/vendor_kit/issues/25)，`extends` 引用值待發布時提供；VK 對 preset 的承諾見 04 的[追蹤新版](../../contract/04_interface.md#追蹤新版)。

Renovate 開出的工具 PR，依下列流程收尾：

| 步驟 | 做什麼 | 指令 |
|---|---|---|
| 1 | 在本機切到 Renovate 開出的 PR 分支 | `git switch <PR 分支>` |
| 2 | 完成工具升版 | `just vendor_kit upgrade <repo> -y` |
| 3 | 自己 commit、push | `git commit`、`git push` |
| 4 | CI 通過才 merge | — |

[引擎](../../../GLOSSARY.md#vk-組件) PR 的收尾流程待確認，見 [issue #370](https://github.com/ycpss91255-research/vendor_kit/issues/370)。

## 文件

| 文件 | 內容 |
|---|---|
| [01 目的與承諾](../../contract/01_purpose.md) | 為什麼做 VK，對使用者承諾什麼 |
| [02 不變量](../../contract/02_invariants.md) | 任何版本都必須成立的規則 |
| [03 輸出](../../contract/03_output.md) | 結束碼與訊息格式 |
| [04 使用者介面](../../contract/04_interface.md) | 全部指令與選項 |
| [訊息表](../../contract/reason_codes.csv) | 逐項診斷、處置與結束碼 |
| [名詞表](../../../GLOSSARY.md) | 專有名詞與用語 |
| [架構決議 (ADR)](../../adr/) | 設計決定與理由 |

每個指令的開發進度見 [issue #47](https://github.com/ycpss91255-research/vendor_kit/issues/47)。
