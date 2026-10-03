<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit 61356db。正式內容看 /doc/contract/03_output.md 與 /doc/contract/reason_codes.csv -->

# 03 輸出

這一頁列出 [VK](../../../GLOSSARY.md#角色與情境) 每個[結束碼](../../../GLOSSARY.md#執行與結果)的意思，以及每條[診斷](../../../GLOSSARY.md#執行與結果)的固定格式。結束碼是[契約](../../../GLOSSARY.md#介面版與契約)，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。

- 名詞見[名詞表](../../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或自動化判斷結果。結束碼表示整次執行的結果，與[嚴重度](../../../GLOSSARY.md#執行與結果)固定對應；VK 以非零碼結束時，至少印出一條對應嚴重度的診斷：

| 結束碼 | 對應嚴重度 | 意思 |
| - | - | - |
| `0` | info | 成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果) |
| `1` | warn | 指令承諾的結果已做完，但有警告 |
| `2` | error | 指令承諾的結果沒做完，可能是[待處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤 |
| `3` | fatal | 只限現有[薄殼](../../../GLOSSARY.md#vk-組件)、[VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、[引擎](../../../GLOSSARY.md#vk-組件)的版本組合不合。以這個碼結束的那次執行不動 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與 VK 檔，[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)除外 |

這張表只列 VK 回的結束碼；指令到不了 VK 時由 just 回的碼不在內。

留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)屬於警告，碼仍是 `1`。`bootstrap.sh` 與每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。

一次處理多個[工具](../../../GLOSSARY.md#工具與出貨)時：

- 結束碼取各工具結果裡數字最大的那個，沒有特例。例如一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`0`，查到新版不是警告)、C 查詢失敗 (`2`)，就以 `2` 結束
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意，省略引擎那一行：

```text
stdout: A current: v1.2.0 latest: v1.2.0
stdout: B current: v1.2.0 latest: v1.3.0
stdout: C current: v2.0.0 latest: none
stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required; pulling still uses the host's Docker credentials. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag>
exit code: 2
```

## 輸出

- <mark style="background-color:#f8c8c8">成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴</mark>
- <mark style="background-color:#c8f0c8">成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`/`--help` 用法只印到 stdout，不加前綴</mark>
- stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行、用法錯誤後附的用法，以及 [update](../../../GLOSSARY.md#vk-recipe-與用途) 印的[本機覆寫](../../../GLOSSARY.md#版本與來源)提醒（不加前綴）
- 只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：

  ```text
  $ just vendor_kit
  stderr: vendor_kit <version>
  stderr: vendor_kit: error[VK0024]: No command was specified.
  stderr: Usage: just vendor_kit <command> [arguments] [options]
  exit code: 2
  ```
- 主機前置檢查（檢查主機上的 Docker 與 just）排在建執行紀錄之前；找不到 docker、Docker 低於 19.03、`docker --version` 的輸出含 Podman、找不到 just 或 just 低於 1.33.0 時，檢查不通過。不通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。各入口檢查哪幾項見 [04 使用者介面](../../contract/04_interface.md#bootstrapsh)
- <mark style="background-color:#f8c8c8">`remove`／`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，沒有其他診斷時以 `0` 結束</mark>
- <mark style="background-color:#c8f0c8">`remove`/`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，沒有其他診斷時以 `0` 結束</mark>
- 詢問時[使用者](../../../GLOSSARY.md#角色與情境)明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - 只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))
  - 給程式讀的輸出永遠不含顏色，例如執行紀錄
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

- 每條診斷都印到 stderr。
- 第一行格式固定如下：

  ```text
  vendor_kit: <level>[VKnnnn]: <message>
  ```
- stderr 的診斷只用 `warn`、`error`、`fatal`；`info` 只用在成功的結果與執行紀錄，不印成 stderr 的診斷。
- <mark style="background-color:#f8c8c8">VK 自己寫的字句（stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問、用法（含 `-h`／`--help` 與用法錯誤後附的簡短用法）、版本行、本機覆寫提醒、執行紀錄、stderr 診斷）目前都用英文；換進占位符的值（路徑、檔名、`<repo>`、[tag](../../../GLOSSARY.md#工具與出貨)、使用者給的參數）照原樣印出。之後若做多語系 (i18n)，診斷以訊息表的語言欄切換，其他字句另議。每條診斷的中文見訊息表的 `message.zh-TW`、`situation.zh-TW` 欄。</mark>
- <mark style="background-color:#c8f0c8">VK 自己寫的字句（stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問、用法（含 `-h`/`--help` 與用法錯誤後附的簡短用法）、版本行、本機覆寫提醒、執行紀錄、stderr 診斷）目前都用英文；換進占位符的值（路徑、檔名、`<repo>`、[tag](../../../GLOSSARY.md#工具與出貨)、使用者給的參數）照原樣印出。之後若做多語系 (i18n)，診斷以訊息表的語言欄切換，其他字句另議。每條診斷的中文見訊息表的 `message.zh-TW`、`situation.zh-TW` 欄。</mark>
- 診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。這些句型規則只適用於診斷本文。
- 多行診斷的續行也印到 stderr。

[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation.<lang>` 欄為唯一意思；發出後永不重用。

每個代碼的嚴重度、處置、情況與本文，只寫在[訊息表](../../contract/reason_codes.csv)，一列一個代碼。訊息表只收 warn、error、fatal 的診斷；不是診斷的字句（stdout 的正常輸出、詢問、用法、版本行、本機覆寫提醒、執行紀錄的一般條目）不登錄。

處置與下一步：

- 處置是診斷的屬性，不是嚴重度。待處理表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令；失敗不承諾可執行的修法，但可以附一般建議；warn 的列與用法錯誤留空
- 下一步指令直接寫在本文句尾，占位符都由 VK 換成實際的值；待處理的本文必須以這條指令結尾，各語言的結尾指令逐字相同；做不到的診斷標失敗
- warn 要指名對象；有辦法處置就在本文寫出下一步

代碼的停用與整理：

- 每個大版本 X（含 v1.0.0）發布時整理訊息表，表內不留 `retired` 的列
- 同一個 X 內的 Y、Z 可能停用代碼。停用的代碼不刪列，`status` 改成 `retired`，只留 `code`、`status` 與 `situation.<lang>`，留作空號；代碼不重用

訊息表怎麼讀：

- 格式
  - UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號
  - 儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字
  - 依首行的欄名讀，不依欄序
- 欄位
  - 左邊五欄給程式讀，只用英文：
    - `code`：原因代碼，依代碼升冪排列；新代碼持續遞增，大版本清理停用列後可留下缺號
    - `status`：`active` 使用中；`retired` 已停用
    - `level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)
    - `exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空
    - `disposition`：處置，`pending`（待處理）、`failed`（失敗）或留空；warn 的列與用法錯誤（`situation.en` 以 `Usage error:` 開頭的列）留空
  - 右邊照語言分組，每組是 `situation.<lang>`、`message.<lang>`，目前有 `en`、`zh-TW`；之後加語言就在最右邊接一組：
    - `situation.<lang>`：什麼情況發出這個代碼，是它唯一的意思，給人閱讀
    - `message.<lang>`：印出的本文，不含前綴；目前只印 `message.en`，逐字照印；多行診斷在同一格內換行，一行對應印出的一行；占位符與換行在各語言一致
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - `situation.<lang>` 註明原樣印出的，由使用者換成要用的值
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - 要依 `level` 或 `disposition` 篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號

---

## reason_codes.csv 的逐碼差異

依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。

CSV 沒有改動。

沒改動的代碼 55 個：VK0001、VK0002、VK0003、VK0004、VK0005、VK0006、VK0007、VK0008、VK0009、VK0010、VK0011、VK0012、VK0013、VK0014、VK0015、VK0016、VK0017、VK0018、VK0019、VK0020、VK0021、VK0022、VK0023、VK0024、VK0025、VK0026、VK0027、VK0028、VK0029、VK0030、VK0031、VK0032、VK0033、VK0034、VK0035、VK0036、VK0037、VK0038、VK0039、VK0040、VK0041、VK0042、VK0043、VK0044、VK0045、VK0046、VK0047、VK0048、VK0049、VK0050、VK0051、VK0052、VK0053、VK0054、VK0055。
