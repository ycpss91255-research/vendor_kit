# 03 訊息與錯誤碼總表

這一頁列出 [VK](../../GLOSSARY.md#角色與情境) 每個[結束碼](../../GLOSSARY.md#執行與結果)的意思，以及每條[診斷](../../GLOSSARY.md#執行與結果)的固定格式。結束碼是[契約](../../GLOSSARY.md#介面版與契約)，依 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)。

- 名詞見[名詞表](../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或自動化判斷結果。結束碼表示整次執行的結果，與[嚴重度](../../GLOSSARY.md#執行與結果)固定對應；VK 以非零碼結束時，至少印出一條對應嚴重度的診斷：

| 結束碼 | 對應嚴重度 | 意思 |
|---|---|---|
| `0` | info | 成功；沒有任何[警告](../../GLOSSARY.md#執行與結果) |
| `1` | warn | 指令承諾的結果已做完，但有警告 |
| `2` | error | 指令承諾的結果沒做完，可能是[待處理](../../GLOSSARY.md#執行與結果)、[失敗](../../GLOSSARY.md#執行與結果)或用法錯誤 |
| `3` | fatal | 只限現有[薄殼](../../GLOSSARY.md#vk-組件)、[VK 檔](../../GLOSSARY.md#repo-內的檔與狀態)、[引擎](../../GLOSSARY.md#vk-組件)的版本組合不合。以這個碼結束的那次執行不動 [repo 檔](../../GLOSSARY.md#repo-內的檔與狀態)與 VK 檔，[執行紀錄](../../GLOSSARY.md#repo-內的檔與狀態)除外 |

這張表只列 VK 回的結束碼；指令到不了 VK 時由 just 回的碼不在內。

留下[合併衝突](../../GLOSSARY.md#初始檔與合併)、`update --exit-code` 查到新版都屬於警告，碼仍是 `1`。每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。

一次處理多個[工具](../../GLOSSARY.md#工具與出貨)時：

- 結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`1`)、C 查詢失敗 (`2`)，就以 `2` 結束
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意：

```text
stdout: A 已是最新。
stdout: B 有新版 v1.3.0（目前為 v1.2.0）。
stderr: vendor_kit: warn[VK0022]: A newer version of B is available: current v1.2.0; new v1.3.0. Run: just vendor_kit upgrade B
stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag> (pulling uses the host's Docker credentials).
exit code: 2
```

## 輸出

- 成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴
- stderr 只放診斷及其續行、[詢問](../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法
- 只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：

  ```text
  $ just vendor_kit
  stderr: vendor_kit <版本>
  stderr: vendor_kit: error[VK0024]: No command was specified.
  stderr: 用法：just vendor_kit <指令> [參數] [選項]
  exit code: 2
  ```
- 主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷
- `remove`／`uninstall` 依契約保留[初始檔](../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，以 `0` 結束
- 詢問時[使用者](../../GLOSSARY.md#角色與情境)明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - 只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))
  - 給程式讀的輸出永遠不含顏色，例如執行紀錄
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

- 每條診斷都印到 stderr。
- 第一行格式固定如下，診斷使用的嚴重度見[名詞表](../../GLOSSARY.md#執行與結果)：

  ```text
  vendor_kit: <level>[VKnnnn]: <message>
  ```
- 只有診斷本文固定使用英文；stdout 的[正常輸出](../../GLOSSARY.md#執行與結果)、詢問與用法不在這條語言規則內。診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。
- 中文說明見訊息表的 `description` 欄。
- 多行診斷的續行也印到 stderr。

[原因代碼](../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。

每個代碼的嚴重度、處置、情況、本文與下一步，只寫在[訊息表](03_messages.csv)，一列一個代碼。

處置與下一步：

- 處置是診斷的屬性，不是嚴重度。待處理表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令；失敗不承諾可執行的修法，但可以附一般建議；warn 的列與用法錯誤（VK0024～VK0027）留空
- warn 要指名對象；有辦法處置就列出下一步

訊息表怎麼讀：

- 格式
  - UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號
  - 儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字
- 欄位
  - `code`：原因代碼，從 `VK0001` 起逐列加一，不缺列
  - `status`：`active` 使用中；`retired` 已停用，只留 `code`、`status`、`situation`
  - `level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)
  - `exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空
  - `disposition`：處置，`待處理`、`失敗` 或留空；warn 的列與用法錯誤（VK0024～VK0027）留空
  - `situation`：什麼情況發出這個代碼，是它唯一的意思
  - `message`：英文本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行
  - `description`：訊息的中文說明，給人閱讀；`active` 列必填
  - `next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；待處理必填，失敗與沒有指令的留空；做不到的診斷標失敗
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - `situation` 註明原樣印出的，由使用者換成要用的值
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - 要依 `level` 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號
