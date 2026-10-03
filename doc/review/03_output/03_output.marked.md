<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit a49bca0。正式內容看 /doc/contract/03_output.md 與 /doc/contract/reason_codes.csv -->

# 03 輸出
<mark style="background-color:#f8c8c8">舊標題：03 訊息與錯誤碼總表</mark>
<mark style="background-color:#c8f0c8">（標題已修改）</mark>

這一頁列出 [VK](../../../GLOSSARY.md#角色與情境) 每個[結束碼](../../../GLOSSARY.md#執行與結果)的意思，以及每條[診斷](../../../GLOSSARY.md#執行與結果)的固定格式。結束碼是[契約](../../../GLOSSARY.md#介面版與契約)，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。

- 名詞見[名詞表](../../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

<mark style="background-color:#f8c8c8">每個指令結束時回一個數字，給呼叫它的人或自動化判斷結果：</mark>
<mark style="background-color:#c8f0c8">每個指令結束時回一個數字，給呼叫它的人或自動化判斷結果。結束碼表示整次執行的結果，與[嚴重度](../../../GLOSSARY.md#執行與結果)固定對應；VK 以非零碼結束時，至少印出一條對應嚴重度的診斷：</mark>

| <mark style="background-color:#f8c8c8">結束碼</mark> | <mark style="background-color:#f8c8c8">[level](../../../GLOSSARY.md#執行與結果)</mark> | <mark style="background-color:#f8c8c8">意思</mark> |
|---|---|---|
| <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">info</mark> | <mark style="background-color:#f8c8c8">成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果)，也沒有要人接手的事項</mark> |
| <mark style="background-color:#f8c8c8">`1`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">有警告，或做完但要人接手；見表下的結束碼 `1`</mark> |
| <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">沒做完：[需人處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤</mark> |
| <mark style="background-color:#c8f0c8">結束碼</mark> | <mark style="background-color:#c8f0c8">對應嚴重度</mark> | <mark style="background-color:#c8f0c8">意思</mark> |
| - | - | - |
| <mark style="background-color:#c8f0c8">`0`</mark> | <mark style="background-color:#c8f0c8">info</mark> | <mark style="background-color:#c8f0c8">成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果)</mark> |
| <mark style="background-color:#c8f0c8">`1`</mark> | <mark style="background-color:#c8f0c8">warn</mark> | <mark style="background-color:#c8f0c8">指令承諾的結果已做完，但有警告</mark> |
| <mark style="background-color:#c8f0c8">`2`</mark> | <mark style="background-color:#c8f0c8">error</mark> | <mark style="background-color:#c8f0c8">指令承諾的結果沒做完，可能是[待處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤</mark> |
| `3` | fatal | 只限現有[薄殼](../../../GLOSSARY.md#vk-組件)、[VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、[引擎](../../../GLOSSARY.md#vk-組件)的版本組合不合。以這個碼結束的那次執行不動 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與 VK 檔，[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)除外 |

<mark style="background-color:#f8c8c8">結束碼 `1` 有兩種：</mark>
<mark style="background-color:#c8f0c8">這張表只列 VK 回的結束碼；指令到不了 VK 時由 just 回的碼不在內。</mark>

- <mark style="background-color:#f8c8c8">有警告</mark>
- <mark style="background-color:#f8c8c8">做完但要人接手（不算警告）：留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)、`update --exit-code` 查到新版</mark>
<mark style="background-color:#f8c8c8">只有警告也以 `1` 結束。每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>
<mark style="background-color:#c8f0c8">留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)屬於警告，碼仍是 `1`。`bootstrap.sh` 與每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>

一次處理多個[工具](../../../GLOSSARY.md#工具與出貨)時：

- <mark style="background-color:#f8c8c8">結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`1`)、C 查詢失敗 (`2`)，就以 `2` 結束</mark>
- <mark style="background-color:#c8f0c8">結束碼取各工具結果裡數字最大的那個，沒有特例。例如一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`0`，查到新版不是警告)、C 查詢失敗 (`2`)，就以 `2` 結束</mark>
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

<mark style="background-color:#f8c8c8">沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意：</mark>
<mark style="background-color:#c8f0c8">沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意，省略引擎那一行：</mark>

```text
<mark style="background-color:#f8c8c8">stdout: A 已是最新。</mark>
<mark style="background-color:#f8c8c8">stdout: B 有新版 v1.3.0（目前為 v1.2.0）。</mark>
<mark style="background-color:#f8c8c8">stderr: vendor_kit: warn[VK0022]: A newer version of B is available: current v1.2.0; new v1.3.0. Run: just vendor_kit upgrade B</mark>
<mark style="background-color:#f8c8c8">stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag> (pulling uses the host's Docker credentials).</mark>
<mark style="background-color:#c8f0c8">stdout: A current: v1.2.0 latest: v1.2.0</mark>
<mark style="background-color:#c8f0c8">stdout: B current: v1.2.0 latest: v1.3.0</mark>
<mark style="background-color:#c8f0c8">stdout: C current: v2.0.0 latest: none</mark>
<mark style="background-color:#c8f0c8">stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required; pulling still uses the host's Docker credentials. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag></mark>
exit code: 2
```

## 輸出

- <mark style="background-color:#f8c8c8">成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴</mark>
- <mark style="background-color:#f8c8c8">stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法</mark>
- <mark style="background-color:#f8c8c8">只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印下列診斷，接著印簡短用法，以 `2` 結束：</mark>
- <mark style="background-color:#c8f0c8">成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴</mark>
- <mark style="background-color:#c8f0c8">stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行、用法錯誤後附的用法，以及 [update](../../../GLOSSARY.md#vk-recipe-與用途) 印的[本機覆寫](../../../GLOSSARY.md#版本與來源)提醒（不加前綴）</mark>
- <mark style="background-color:#c8f0c8">只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：</mark>

  ```text
  <mark style="background-color:#f8c8c8">vendor_kit: error[VK0024]: No command was specified.</mark>
  <mark style="background-color:#c8f0c8">$ just vendor_kit</mark>
  <mark style="background-color:#c8f0c8">stderr: vendor_kit <version></mark>
  <mark style="background-color:#c8f0c8">stderr: vendor_kit: error[VK0024]: No command was specified.</mark>
  <mark style="background-color:#c8f0c8">stderr: Usage: just vendor_kit <command> [arguments] [options]</mark>
  <mark style="background-color:#c8f0c8">exit code: 2</mark>
  ```
- <mark style="background-color:#f8c8c8">主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷</mark>
- <mark style="background-color:#c8f0c8">主機前置檢查（檢查主機上的 Docker 與 just）排在建執行紀錄之前；找不到 docker、Docker 低於 19.03、`docker --version` 的輸出含 Podman、找不到 just 或 just 低於 1.33.0 時，檢查不通過。不通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。各入口檢查哪幾項見 [04 使用者介面](../../contract/04_interface.md#bootstrapsh)</mark>
- `remove`／`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，以 `0` 結束
- 詢問時[使用者](../../../GLOSSARY.md#角色與情境)明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - 只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))
  - 給程式讀的輸出永遠不含顏色，例如執行紀錄
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

<mark style="background-color:#f8c8c8">每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <message>`。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。只有診斷本文固定使用英文；stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問與用法不在這條語言規則內。診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。中文說明見訊息表的 `description` 欄。多行診斷的續行也印到 stderr。</mark>
- <mark style="background-color:#c8f0c8">每條診斷都印到 stderr。</mark>
- <mark style="background-color:#c8f0c8">第一行格式固定如下：</mark>

<mark style="background-color:#f8c8c8">[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。</mark>
  <mark style="background-color:#c8f0c8">```text</mark>
  <mark style="background-color:#c8f0c8">vendor_kit: <level>[VKnnnn]: <message></mark>
  <mark style="background-color:#c8f0c8">```</mark>
- <mark style="background-color:#c8f0c8">stderr 的診斷只用 `warn`、`error`、`fatal`；`info` 只用在成功的結果與執行紀錄，不印成 stderr 的診斷。</mark>
- <mark style="background-color:#c8f0c8">VK 自己寫的字句（stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問、用法（含 `-h`／`--help` 與用法錯誤後附的簡短用法）、版本行、本機覆寫提醒、執行紀錄、stderr 診斷）目前都用英文；換進占位符的值（路徑、檔名、`<repo>`、[tag](../../../GLOSSARY.md#工具與出貨)、使用者給的參數）照原樣印出。之後若做多語系 (i18n)，診斷以訊息表的語言欄切換，其他字句另議。每條診斷的中文見訊息表的 `message.zh-TW`、`situation.zh-TW` 欄。</mark>
- <mark style="background-color:#c8f0c8">診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。這些句型規則只適用於診斷本文。</mark>
- <mark style="background-color:#c8f0c8">多行診斷的續行也印到 stderr。</mark>

<mark style="background-color:#f8c8c8">每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](../../contract/reason_codes.csv)，一列一個代碼。</mark>
<mark style="background-color:#c8f0c8">[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation.<lang>` 欄為唯一意思；發出後永不重用。</mark>

<mark style="background-color:#c8f0c8">每個代碼的嚴重度、處置、情況與本文，只寫在[訊息表](../../contract/reason_codes.csv)，一列一個代碼。訊息表只收 warn、error、fatal 的診斷；info（stdout 的正常輸出、詢問、用法、執行紀錄的一般條目）不登錄。</mark>

處置與下一步：

- <mark style="background-color:#f8c8c8">處置是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令（不用使用者代換的單一指令）；失敗不承諾可執行的修法，但可以附一般建議；不屬於兩者的留空</mark>
- <mark style="background-color:#f8c8c8">warn 要指名對象；有辦法處置就列出下一步</mark>
- <mark style="background-color:#c8f0c8">處置是診斷的屬性，不是嚴重度。待處理表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令；失敗不承諾可執行的修法，但可以附一般建議；warn 的列與用法錯誤留空</mark>
- <mark style="background-color:#c8f0c8">下一步指令直接寫在本文句尾，占位符都由 VK 換成實際的值；待處理的本文必須以這條指令結尾，各語言的結尾指令逐字相同；做不到的診斷標失敗</mark>
- <mark style="background-color:#c8f0c8">warn 要指名對象；有辦法處置就在本文寫出下一步</mark>

<mark style="background-color:#c8f0c8">代碼的停用與整理：</mark>

- <mark style="background-color:#c8f0c8">每個大版本 X（含 v1.0.0）發布時整理訊息表，表內不留 `retired` 的列</mark>
- <mark style="background-color:#c8f0c8">同一個 X 內的 Y、Z 可能停用代碼。停用的代碼不刪列，`status` 改成 `retired`，只留 `code`、`status` 與 `situation.<lang>`，留作空號；代碼不重用</mark>

訊息表怎麼讀：

- 格式
  - UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號
  - 儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字
  - <mark style="background-color:#c8f0c8">依首行的欄名讀，不依欄序</mark>
- 欄位
  - <mark style="background-color:#f8c8c8">`code`：原因代碼，從 `VK0001` 起逐列加一，不缺列</mark>
  - <mark style="background-color:#f8c8c8">`status`：`active` 使用中；`retired` 已停用，只留 `code`、`status`、`situation`</mark>
  - <mark style="background-color:#f8c8c8">`level`：`warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)</mark>
  - <mark style="background-color:#f8c8c8">`exit_code`：該 level 對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空</mark>
  - <mark style="background-color:#f8c8c8">`disposition`：處置，`需人處理`、`失敗` 或留空；`warn` 一律留空</mark>
  - <mark style="background-color:#f8c8c8">`situation`：什麼情況發出這個代碼，是它唯一的意思</mark>
  - <mark style="background-color:#f8c8c8">`message`：英文本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行</mark>
  - <mark style="background-color:#f8c8c8">`description`：訊息的中文說明，給人閱讀；`active` 列必填</mark>
  - <mark style="background-color:#f8c8c8">`next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；需人處理必填，失敗與沒有指令的留空；做不到的診斷標失敗</mark>
  - <mark style="background-color:#c8f0c8">左邊五欄給程式讀，只用英文：</mark>
    - <mark style="background-color:#c8f0c8">`code`：原因代碼，從 `VK0001` 起逐列加一，不缺列</mark>
    - <mark style="background-color:#c8f0c8">`status`：`active` 使用中；`retired` 已停用</mark>
    - <mark style="background-color:#c8f0c8">`level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)</mark>
    - <mark style="background-color:#c8f0c8">`exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空</mark>
    - <mark style="background-color:#c8f0c8">`disposition`：處置，`pending`（待處理）、`failed`（失敗）或留空；warn 的列與用法錯誤（`situation.en` 以 `Usage error:` 開頭的列）留空</mark>
  - <mark style="background-color:#c8f0c8">右邊照語言分組，每組是 `situation.<lang>`、`message.<lang>`，目前有 `en`、`zh-TW`；之後加語言就在最右邊接一組：</mark>
    - <mark style="background-color:#c8f0c8">`situation.<lang>`：什麼情況發出這個代碼，是它唯一的意思，給人閱讀</mark>
    - <mark style="background-color:#c8f0c8">`message.<lang>`：印出的本文，不含前綴；目前只印 `message.en`，逐字照印；多行診斷在同一格內換行，一行對應印出的一行；占位符與換行在各語言一致</mark>
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - <mark style="background-color:#f8c8c8">`situation` 註明原樣印出的，由使用者換成要用的值</mark>
  - <mark style="background-color:#c8f0c8">`situation.<lang>` 註明原樣印出的，由使用者換成要用的值</mark>
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - <mark style="background-color:#f8c8c8">要依 level 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號</mark>
  - <mark style="background-color:#c8f0c8">要依 `level` 或 `disposition` 篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號</mark>

---

## reason_codes.csv 的逐碼差異

依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。

- 表頭：<mark style="background-color:#f8c8c8">code,status,level,exit_code,disposition,situation,message,description,next_step</mark> → <mark style="background-color:#c8f0c8">code,status,level,exit_code,disposition,situation.en,message.en,situation.zh-TW,message.zh-TW</mark>
- `situation`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0001

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">update, upgrade, or add needs to list versions but has no registry credentials; &lt;command&gt; prints add for add and upgrade for update or upgrade; &lt;tag&gt; is printed literally for the user to replace with the version tag to install</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot list versions for &lt;repo&gt;: registry read access is required; pulling still uses the host's Docker credentials. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;command&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法列出 &lt;repo&gt; 的版本：需要 registry 讀取權限；拉取時仍使用主機的 Docker 認證。請設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;command&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot list versions for &lt;repo&gt;: registry read access is required. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt; (pulling uses the host's Docker credentials).</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0002

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">An operation requires a prompt, but -y was not given and interaction is impossible (stdin or stderr is not a terminal, or end of input was read); &lt;command_with_y&gt; is rebuilt from this run's arguments one by one, each quoted by POSIX shell rules, with -y inserted before a standalone --, or appended at the end if there is no --; during initial import by bootstrap.sh, &lt;command_with_y&gt; starts with the sh and script path ($0) of this invocation, followed by this run's arguments, rebuilt by the same rules</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">操作需要詢問，但沒帶 -y 又不能互動（stdin 或 stderr 不是終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後；bootstrap.sh 首次導入時，&lt;command_with_y&gt; 以這次呼叫的 sh 與腳本路徑 ($0) 開頭，後接這次的參數，依同一規則重組</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">操作需要詢問，但沒帶 -y 又不能互動（沒有終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;command_with_y&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0003

- `status`：retired
- `situation.en`：<mark style="background-color:#c8f0c8">The baseline is behind the lock version line</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">基準版落後版本鎖定行</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">基準版落後版本鎖定行</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0004

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">sync finds a tool whose import is incomplete, or a read-only recipe reads a progress file for that tool's incomplete import</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Import of &lt;repo&gt; is incomplete. Run: just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 發現某個工具未完成導入，或唯讀 recipe 讀到該工具導入未完成的進度檔</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的導入未完成。請執行：just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">sync 發現某個工具未完成導入</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Import of &lt;repo&gt; is incomplete. Run: just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 未完成導入，請執行：just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0005

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">During initial import, bootstrap.sh finds the host's just is older than 1.33.0; &lt;install_command&gt; does not overwrite the host's existing just and does not require the host to install any other tool</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 首次導入時發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">需要 just 1.33.0 或更新版本；目前版本為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">bootstrap.sh 發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;install_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0006

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Shell files do not match this engine version's templates (their content was modified, or they are not this engine version's templates); during a bootstrap.sh check-only run or --repair, if the progress file records an incomplete engine upgrade, VK0023 is reported instead and no shell comparison is made; &lt;files&gt; marks which case applies to each file; no repo files or other VK files are touched except the run log</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Shell files do not match this engine version's templates: &lt;files&gt;. No shell files were regenerated. Review the following differences; download bootstrap.sh again from the Release, then run sh bootstrap.sh --repair in the install directory.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）；bootstrap.sh 只檢查或 --repair 時，若進度檔記錄引擎升級未完成，改報 VK0023，不做薄殼比對；&lt;files&gt; 逐檔標出是哪一種，除執行紀錄外不動 repo 檔與其他 VK 檔</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">薄殼與這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請檢視下列差異；從 Release 重新下載 bootstrap.sh，再到安裝目錄執行 sh bootstrap.sh --repair。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）；&lt;files&gt; 逐檔標出是哪一種，除執行紀錄外不動 repo 檔與其他 VK 檔</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Shell files do not match this engine version's templates: &lt;files&gt;. No shell files were regenerated. Review the following differences; restore any manual changes, then run: just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">偵測到薄殼跟這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0007

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">upgrade --engine=&lt;tag&gt; downgrades, but the target engine cannot read the existing VK files without loss; the &lt;tag&gt; in the message is printed literally for the user to replace with an engine version tag that can read schema version &lt;N&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Target engine &lt;vY&gt; (interface version &lt;P&gt;, schema version &lt;M&gt;) cannot read the existing files (schema version &lt;N&gt;) without loss. No files were modified except the run log. Specify a version that can read schema version &lt;N&gt;: just vendor_kit upgrade --engine=&lt;tag&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">upgrade --engine=&lt;tag&gt; 降版，但目標引擎無法無損讀取現有的 VK 檔；本文的 &lt;tag&gt; 原樣印出，由使用者換成能讀取檔案版 &lt;N&gt; 的引擎版本 tag</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有的檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">upgrade --engine=&lt;tag&gt; 降版，但目標引擎無法無損讀取現有的 VK 檔；本文的 &lt;tag&gt; 原樣印出，由使用者換成能讀取檔案版 &lt;N&gt; 的引擎版本 tag</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Target engine &lt;vY&gt; (interface version &lt;P&gt;, schema version &lt;M&gt;) cannot read the existing files (schema version &lt;N&gt;) without loss. No files were modified except the run log. Specify a version that can read schema version &lt;N&gt;: just vendor_kit upgrade --engine=&lt;tag&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0008

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The engine reads a VK file whose schema version is higher than the maximum this engine supports</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot read &lt;file&gt;: schema version &lt;N&gt; is newer than the maximum supported version &lt;M&gt;; written by vendor_kit &lt;written_by&gt;. Upgrade the engine: just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的最高版本 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot read &lt;file&gt;: schema version &lt;N&gt; is newer than the maximum supported version &lt;M&gt;; written by vendor_kit &lt;written_by&gt;. Upgrade the engine: just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0009

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">An old shell meets an engine with a newer major version X and runs a recipe outside the rescue path</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 一般 recipe 所需的版本。請先執行：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0010

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Any VK recipe, or bootstrap.sh initial import (including an incomplete initial import), check-only run, or --repair, cannot create the run log (it exits before any side effect; initial import creates the log before calling install)</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot write run log &lt;path&gt;: &lt;reason&gt;. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">任何 VK recipe，或 bootstrap.sh 首次導入（含未完成的首次導入）、只檢查、--repair 時，建不出執行紀錄（在任何副作用之前結束，首次導入在呼叫 install 之前先建紀錄）</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法寫入執行紀錄 &lt;path&gt;：&lt;reason&gt;。vendor_kit 不在沒有紀錄的情況下執行；未修改任何檔。請清出磁碟空間或修正權限後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">任何 VK recipe 建不出執行紀錄（在任何副作用之前結束）</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot write run log &lt;path&gt;: &lt;reason&gt;. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法寫入執行紀錄 &lt;path&gt;：&lt;reason&gt;。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0011

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The output of docker --version contains podman</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">docker --version 的輸出含 podman</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">偵測到 Podman (docker --version)。vendor_kit 只支援 Docker。請改用 Docker（rootful 或 rootless）後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">docker --version 的輸出含 podman</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">偵測到 podman (docker --version)。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0012

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The launcher finds the host's Docker is older than 19.03</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Docker 19.03 or later is required; the current version is &lt;version&gt;. Upgrade Docker and retry.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">啟動器發現主機的 Docker 低於 19.03</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">需要 Docker 19.03 或更新版本；目前版本為 &lt;version&gt;。請升級 Docker 後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">啟動器發現主機的 Docker 低於 19.03</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Docker 19.03 or later is required; the current version is &lt;version&gt;. Upgrade Docker and retry.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">需要 Docker ≥ 19.03，目前為 &lt;version&gt;。請升級 Docker 後重試。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0013

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">metadata is missing or corrupt and cannot be restored reliably</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot process &lt;file&gt;: metadata is missing or corrupt and cannot be restored reliably. vendor_kit does not guess when records are unavailable; no files were modified except the run log. Preserve &lt;file&gt; and run log &lt;path&gt;. If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">metadata 缺失或損壞，無法可靠還原</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。紀錄不可用時，vendor_kit 不做推測；除執行紀錄外，未修改任何檔。請保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;。metadata 若曾 commit 進 Git，從 Git 還原後重試；否則到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，並附上這兩個檔。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">metadata 缺失或損壞，無法可靠還原</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot process &lt;file&gt;: metadata is missing or corrupt and cannot be restored reliably. vendor_kit does not guess when records are unavailable; no files were modified except the run log. Preserve &lt;file&gt; and run log &lt;path&gt;. If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0014

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">sync or test finds the baseline is behind the lock version line</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The baseline for &lt;repo&gt; is behind the lock version line. Run: just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 或 test 發現基準版落後版本鎖定行</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">sync 或 test 發現基準版落後版本鎖定行</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">The baseline for &lt;repo&gt; is behind the lock version line. Run: just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0015

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">sync finds the file set or per-file digests in cache/ for a locked tool do not match, and has refetched according to the lock version line; tool directories not in the lock version lines are not covered by this case</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The file set or per-file digests in cache/ for &lt;repo&gt; did not match; refetched according to the lock version line.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 發現已鎖定工具的 cache/ 檔案集合或逐檔指紋不符，已依版本鎖定行重新取件；不在版本鎖定行的工具目錄不屬於這個情況</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 在 cache/ 的檔案集合或逐檔指紋不符；已依版本鎖定行重新取件。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">sync 發現 cache/ 的逐檔指紋不符，已重新取件</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Per-file digests in cache/ for &lt;repo&gt; did not match; refetched according to the lock version line.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0016

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">When removing an appended line, the originally inserted text cannot be found in the file</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Could not find the original text to remove from &lt;file&gt;; the line was not removed. Check it manually.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">收回 append 行時，在檔內找不到當初插入的原文</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">在 &lt;file&gt; 中找不到要移除的原文；未移除該行。請手動檢查。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">收回 append 行時，在檔內找不到當初插入的原文</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Could not find the original text to remove from &lt;file&gt;; the line was not removed. Check it manually.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;file&gt; 找不到要收回的原文；未刪除該行，請手動檢查。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0017

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">When removing an appended line, multiple occurrences identical to the originally inserted text are found in the file</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Found &lt;count&gt; occurrences of the original text to remove from &lt;file&gt; and could not attribute one uniquely; the line was not removed. Check it manually.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">收回 append 行時，在檔內找到多處與當初插入的原文相同</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">在 &lt;file&gt; 中找到 &lt;count&gt; 處要移除的原文，無法唯一歸屬其中一處；未移除該行。請手動檢查。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">收回 append 行時，在檔內找到多處與當初插入的原文相同</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Found &lt;count&gt; occurrences of the original text to remove from &lt;file&gt; and could not attribute one uniquely; the line was not removed. Check it manually.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;file&gt; 找到 &lt;count&gt; 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0018

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">add encounters a file that already exists and is not yet managed</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">&lt;file&gt; already exists and is unmanaged; it was neither overwritten nor brought under management.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">add 遇到已存在、尚未納管的檔</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;file&gt; 已存在且未納管；既未覆蓋，也未納入管理。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">add 遇到已存在、尚未納管的檔</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; already exists and is unmanaged; it was neither overwritten nor brought under management.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;file&gt; 已存在且未納管；未覆蓋，也未納管這個檔。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0019

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">A file is unmanaged and is not processed in this run</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">&lt;file&gt; is unmanaged and was not processed.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">檔案沒有納管，本次不處理</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;file&gt; 未納管，未處理。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">檔案沒有納管，本次不處理</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; is unmanaged and was not processed.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;file&gt; 沒有納管；本次未處理這個檔。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0020

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">This version was previously rejected by the user</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Version &lt;tag&gt; of &lt;repo&gt; was previously rejected; it was not prompted again or applied.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">這個版本先前已由使用者拒絕</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；未再次詢問，也未套用。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">這個版本先前已由使用者拒絕</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Version &lt;tag&gt; of &lt;repo&gt; was previously rejected; it was not prompted again or applied.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；本次不再詢問，也未套用。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0021

- `status`：active
- `level`：warn
- `exit_code`：1
- `situation.en`：<mark style="background-color:#c8f0c8">A baseline merge leaves merge conflicts</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">&lt;file&gt; contains merge conflicts. Review and resolve them: git status</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">基準版合併留下合併衝突</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;file&gt; 含有合併衝突。請檢視並解決：git status</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">基準版合併留下合併衝突</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; contains merge conflicts. Review and resolve them: git status</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;file&gt; 留下合併衝突，請檢視後解決：git status</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">git status</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0022
<mark style="background-color:#f8c8c8">（本碼停用）</mark>

- `status`：<mark style="background-color:#f8c8c8">active</mark> → <mark style="background-color:#c8f0c8">retired</mark>
- `level`：<mark style="background-color:#f8c8c8">warn</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `exit_code`：<mark style="background-color:#f8c8c8">1</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">update found a newer version and was asked to report it as a warning; that option has been removed</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">update 查到新版，並被要求以警告回報；該選項已移除</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">update --exit-code 查到新版</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">A newer version of &lt;repo&gt; is available: current &lt;current_tag&gt;; new &lt;new_tag&gt;. Run: just vendor_kit upgrade &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 有新版：目前為 &lt;current_tag&gt;，新版為 &lt;new_tag&gt;。可執行：just vendor_kit upgrade &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade &lt;repo&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0023

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">After upgrade --engine installs the new engine, the original command has not yet completed, or a read-only recipe reads a progress file for an incomplete engine upgrade; during a bootstrap.sh check-only run or --repair, reading a progress file that records an incomplete engine upgrade also reports this code, with no shell comparison or regeneration; &lt;original_command&gt; is filled in by VK from the progress file as the original full upgrade command, keeping the original tag and -y, with no substitution needed by the user</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Engine &lt;vY&gt; is now installed. Run again: &lt;original_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">upgrade --engine 換上新引擎後原指令尚未做完，或唯讀 recipe 讀到引擎升級未完成的進度檔；bootstrap.sh 只檢查或 --repair 時讀到記錄引擎升級未完成的進度檔，也報此碼，不比對或重產薄殼；&lt;original_command&gt; 由 VK 依進度檔填成原本的完整 upgrade 指令，保留原 tag 與 -y，不需使用者代換</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">已安裝引擎 &lt;vY&gt;。請再執行一次：&lt;original_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">upgrade --engine 換上新引擎後停下，要求重跑</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Engine &lt;vY&gt; is now installed. Run again: just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">已換上引擎 &lt;vY&gt;，請再執行一次：just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0024

- `status`：active
- `level`：error
- `exit_code`：2
- `situation.en`：<mark style="background-color:#c8f0c8">Usage error: only just vendor_kit was entered, with no command specified</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">No command was specified.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">用法錯誤：只打 just vendor_kit、未指定指令</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">未指定指令。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">用法錯誤：只打 just vendor_kit、未指定指令</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">No command was specified.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">未指定指令。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0025

- `status`：active
- `level`：error
- `exit_code`：2
- `situation.en`：<mark style="background-color:#c8f0c8">Usage error: a VK recipe or bootstrap.sh is missing a required argument (including bootstrap.sh -i/--image given without an image)</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Required argument is missing: &lt;argument&gt;.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">用法錯誤：VK recipe 或 bootstrap.sh 缺少必要參數（含 bootstrap.sh 的 -i／--image 沒帶 image）</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">缺少必要參數：&lt;argument&gt;。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">用法錯誤：缺少必要參數</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Required argument is missing: &lt;argument&gt;.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">缺少必要參數：&lt;argument&gt;。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0026

- `status`：active
- `level`：error
- `exit_code`：2
- `situation.en`：<mark style="background-color:#c8f0c8">Usage error: a VK recipe or bootstrap.sh received an unknown option or an extra argument; bootstrap.sh given --repair -y, or -y/--yes in an existing install directory (excluding the incomplete initial import determined from the run log as described in VK0037), or -h/--help combined with other arguments; &lt;value&gt; prints the first unknown or disallowed argument; when -h/--help is combined with other arguments, it prints the first argument that is not -h/--help, or the second argument if all are -h/--help; when a VK recipe's -h/--help is combined with arguments other than --engine, &lt;value&gt; prints the first argument that is neither -h/--help nor --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Unknown, extra, or disallowed argument: &lt;value&gt;.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">用法錯誤：VK recipe 或 bootstrap.sh 帶了不認得的選項或多出的參數；bootstrap.sh 帶 --repair -y，或在既有安裝目錄帶 -y／--yes（排除 VK0037 所述、依執行紀錄判定的未完成首次導入），或 -h／--help 與其他參數並用；&lt;value&gt; 印第一個不認得或不允許的參數；-h／--help 與其他參數並用時，印第一個不是 -h／--help 的參數，若全部都是 -h／--help，則印第二個參數；VK recipe 的 -h／--help 與 --engine 以外的參數並用時，&lt;value&gt; 印第一個不是 -h／--help 或 --engine 的參數</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">不認得、多出或此處不允許的參數：&lt;value&gt;。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">用法錯誤：不認得指令或選項</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Unknown command or option: &lt;value&gt;.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">不認得的指令或選項：&lt;value&gt;。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0027

- `status`：active
- `level`：error
- `exit_code`：2
- `situation.en`：<mark style="background-color:#c8f0c8">Usage error: the tag format is invalid</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Invalid tag format: &lt;tag&gt;. Use vX.Y.Z with no leading zeros in X, Y, or Z.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">用法錯誤：tag 格式不合</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">tag 格式不正確：&lt;tag&gt;。請使用 vX.Y.Z，X、Y、Z 都不可有前導零。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">用法錯誤：tag 格式不合</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Invalid tag format: &lt;tag&gt;. Use vX.Y.Z with no leading zeros in X, Y, or Z.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">tag 格式不合：&lt;tag&gt;；只接受 vX.Y.Z，X、Y、Z 不收前導零。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0028

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A VK recipe is run outside an install directory</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The current directory is not an install directory. Run: cd &lt;install_dir&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">在安裝目錄外執行 VK recipe</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">目前目錄不是安裝目錄。請執行：cd &lt;install_dir&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">在安裝目錄外執行 VK recipe</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">The current directory is not an install directory. Run: cd &lt;install_dir&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">目前不在安裝目錄，請執行：cd &lt;install_dir&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">cd &lt;install_dir&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0029

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">install finds an existing install directory above or below</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot create a nested install directory: &lt;existing_install_dir&gt; is already an install directory.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">install 時上層或下層已有安裝目錄</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">install 時上層或下層已有安裝目錄</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot create a nested install directory: &lt;existing_install_dir&gt; is already an install directory.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">不能建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0030

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">add finds a name collision on &lt;ns&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot add &lt;repo&gt;: namespace &lt;ns&gt; is already used by &lt;owner&gt;.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">add 時 &lt;ns&gt; 撞名</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">add 時 &lt;ns&gt; 撞名</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot add &lt;repo&gt;: namespace &lt;ns&gt; is already used by &lt;owner&gt;.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0031

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">失敗</mark> → <mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The local image or image tar for offline import lacks required digest information; or bootstrap.sh is given -i/--image in an existing install directory and the supplied local image or image tar lacks required digest information, or its digest does not match the engine lock version line; applies to both check-only runs and --repair; &lt;reason&gt; is filled as required digest information is missing or the digest does not match the engine lock version line, as applicable</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot use image &lt;image&gt;: &lt;reason&gt;. The supplied image was not used.</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">離線導入的本機 image 或 image tar 缺少必要的 digest 資訊；或 bootstrap.sh 在既有安裝目錄帶 -i／--image，所提供的本機 image 或 image tar 缺少必要的 digest 資訊，或 digest 與引擎版本鎖定行不符；只檢查與 --repair 都適用；&lt;reason&gt; 依情況填為 required digest information is missing 或 the digest does not match the engine lock version line</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法使用 image &lt;image&gt;：&lt;reason&gt;。未使用所提供的 image。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">離線導入的 image 缺少必要的 digest 資訊</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Cannot import from &lt;image&gt;: required digest information is missing.</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">無法從 &lt;image&gt; 導入：缺少必要的 digest 資訊。</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0032

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test finds a local override; &lt;undev_command&gt; prints as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Test cannot run while a local override of &lt;target&gt; is active. Run: &lt;undev_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test 發現本機覆寫；&lt;undev_command&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;target&gt; 的本機覆寫仍在作用中，無法執行 test。請執行：&lt;undev_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">test 發現本機覆寫；&lt;undev_command&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `message`：<mark style="background-color:#f8c8c8">Test cannot run while a local override of &lt;target&gt; is active. Run: &lt;undev_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `description`：<mark style="background-color:#f8c8c8">test 發現 &lt;target&gt; 的本機覆寫，請先執行：&lt;undev_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;undev_command&gt;</mark> <mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0033
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The launcher cannot find docker on the host (checked by bootstrap.sh initial import, check-only runs, and --repair, and by the shell's launcher)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Docker was not found on the host. Install Docker and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">啟動器找不到主機的 docker（bootstrap.sh 的首次導入、只檢查、--repair，以及薄殼的啟動器都檢查）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">主機上找不到 Docker。請安裝 Docker 後重試。</mark>

#### VK0034
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">During initial import, bootstrap.sh cannot find just on the host; &lt;install_command&gt; is filled in by VK, runs directly with no substitution needed by the user, and does not require the host to install any other tool</mark>
- `message.en`：<mark style="background-color:#c8f0c8">just was not found on the host. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 首次導入時找不到主機的 just；&lt;install_command&gt; 由 VK 填好，可直接執行、不需使用者代換，不要求主機另裝其他工具</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">主機上找不到 just。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;</mark>

#### VK0035
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">bootstrap.sh cannot find .git in the current directory or any parent; it does not call git on the host and does not create a repo for the user</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot find .git in the current directory or any parent directory. Run bootstrap.sh from within a Git repository.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 從目前目錄往上找不到 .git；不在主機呼叫 git，也不替使用者建立 repo</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">在目前目錄與所有上層目錄都找不到 .git。請在 Git repo 內執行 bootstrap.sh。</mark>

#### VK0036
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The launcher cannot obtain the engine image it needs (the embedded version for initial import, including an incomplete initial import; the version specified by the lock version line when one exists); no other version is used instead</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot obtain engine image &lt;image&gt;: &lt;reason&gt;. No alternative engine version was used.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">啟動器取不到要用的引擎 image（首次導入含未完成的首次導入時用內嵌版本；已有版本鎖定行時用它指定的版本）；不改用其他版本</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法取得引擎 image &lt;image&gt;：&lt;reason&gt;。未改用其他引擎版本。</mark>

#### VK0037
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">bootstrap.sh finds .vendor_kit/ in the current directory but cannot read exactly one valid engine lock version line; it stops and does not fall back to initial import; only for initial-import invocations (no arguments, -y, -i, including the corresponding long options and their valid combinations), an incomplete initial import that can be uniquely determined from the run log is excluded: the most recent run log is an initial import, and either (a) it stopped at VK0002 with no files modified except the run log, or (b) it ended after the run log was created and before the engine lock version line was written (whether or not other files were written); these states allow rerunning initial import with -y, the determination does not rely on whether files exist, and it still stops when the state cannot be uniquely determined; --repair still reports VK0037 in these states</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot read exactly one valid engine lock version line from .vendor_kit/version.toml. Initial import was not attempted.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 發現目前目錄有 .vendor_kit/，但讀不到恰好一行有效的引擎版本鎖定行；停下，不改走首次導入；僅首次導入的呼叫（不帶參數、-y、-i，含對應長選項及其合法組合）排除可依執行紀錄唯一判定的未完成首次導入：最近一筆執行紀錄是首次導入，且 (a) 停在 VK0002、除執行紀錄外未修改任何檔，或 (b) 在建執行紀錄之後、寫入引擎版本鎖定行之前結束（不論是否已寫入其他檔）；這些狀態允許帶 -y 重跑首次導入，判定不靠檔案在不在，無法唯一判定時仍停下；--repair 在這些狀態下仍報 VK0037</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法從 .vendor_kit/version.toml 讀取恰好一行有效的引擎版本鎖定行。未嘗試首次導入。</mark>

#### VK0038
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">bootstrap.sh is given -i/--image with an image reference in an existing install directory, and the digest matches the engine lock version line but the full image reference does not; a missing or mismatched digest reports VK0031 instead; applies to both check-only runs and --repair</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Image &lt;image&gt; does not exactly match the engine lock version line &lt;locked_image&gt;. The supplied image was not used.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 在既有安裝目錄以 image 引用帶 -i／--image，digest 與引擎版本鎖定行相符，但完整 image 引用不符；缺少 digest 或 digest 不符改報 VK0031；只檢查與 --repair 都適用</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">image &lt;image&gt; 與引擎版本鎖定行 &lt;locked_image&gt; 不完全相同。未使用所提供的 image。</mark>

#### VK0039
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">bootstrap.sh is given --repair outside an install directory (the current directory has no .vendor_kit/); it does not fall back to initial import</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot repair shell files outside an install directory. Initial import was not attempted.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 在非安裝目錄帶 --repair（目前目錄沒有 .vendor_kit/）；不改走首次導入</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法在安裝目錄外修復薄殼。未嘗試首次導入。</mark>

#### VK0040
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">During a bootstrap.sh check-only run or --repair, the major version X of the script's embedded engine version differs from the X of the version specified by the engine lock version line; it stops before any write, image pull, or engine start; &lt;bootstrap_X&gt; and &lt;engine_X&gt; are filled from the script's embedded version and the engine lock version line, respectively</mark>
- `message.en`：<mark style="background-color:#c8f0c8">This bootstrap.sh is for major version &lt;bootstrap_X&gt;, but the locked engine requires major version &lt;engine_X&gt;. No files were modified. Download bootstrap.sh for major version &lt;engine_X&gt; from the Release and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 只檢查或 --repair 時，腳本內嵌引擎版本的 X 與引擎版本鎖定行指定版本的 X 不同；在任何寫入、拉 image 或起引擎之前停下；&lt;bootstrap_X&gt; 與 &lt;engine_X&gt; 分別由腳本內嵌版本及引擎版本鎖定行填入</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">這份 bootstrap.sh 適用於主版本 &lt;bootstrap_X&gt;，但鎖定的引擎需要主版本 &lt;engine_X&gt;。未修改任何檔。請從 Release 下載主版本 &lt;engine_X&gt; 的 bootstrap.sh 後重試。</mark>

#### VK0041
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A read-only recipe reads a progress file for an incomplete tool upgrade; it does not resume or delete the progress file; &lt;original_command&gt; is rebuilt by VK from the progress file as the full tool upgrade command, keeping the specified tag and -y, each argument quoted by POSIX shell rules, with no substitution needed by the user</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Upgrade of &lt;repo&gt; is incomplete. Run again: &lt;original_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">唯讀 recipe 讀到工具 upgrade 未完成的進度檔；不恢復、不刪進度檔；&lt;original_command&gt; 由 VK 依進度檔重組完整的工具 upgrade 指令，保留指定 tag 與 -y，各參數依 POSIX shell 規則加引號，不需使用者代換</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的 upgrade 未完成。請再執行一次：&lt;original_command&gt;</mark>

#### VK0042
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Waiting for the install directory's shared or exclusive lock times out; the default is 60 seconds; VENDOR_KIT_LOCK_TIMEOUT set to 0 fails immediately, set to -1 waits indefinitely; nothing is written except the run log</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Timed out waiting for the lock in &lt;install_dir&gt;. No files were modified except the run log. Wait for the other execution to finish and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">等待安裝目錄的共享鎖或排他鎖逾時；預設 60 秒，VENDOR_KIT_LOCK_TIMEOUT 設 0 時立即失敗、設 -1 時無限等待；除執行紀錄外不寫入</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">等待 &lt;install_dir&gt; 的鎖逾時。除執行紀錄外，未修改任何檔。請等另一個執行結束後重試。</mark>

#### VK0043
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The tool image content downloaded by sync does not match the digest in the lock version line; this content is not treated as verified tool content, and VK0015 is not reported</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Downloaded image &lt;image&gt; for &lt;repo&gt; does not match locked digest &lt;digest&gt;. Synchronization did not complete.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 下載的工具 image 內容不符版本鎖定行的 digest；不把這份內容當成已驗證的工具內容，不報 VK0015</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 下載的 image &lt;image&gt; 與鎖定的 digest &lt;digest&gt; 不符。同步未完成。</mark>

#### VK0044
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">sync finds the existing stamp for &lt;repo&gt; corrupt, and has refetched according to the lock version line and rebuilt the stamp; a first fetch with no stamp yet is not covered by this case</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The existing stamp for &lt;repo&gt; was corrupt; refetched according to the lock version line and rebuilt the stamp.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 發現 &lt;repo&gt; 的既有印記損壞，已依版本鎖定行重新取件並重建印記；首次取件尚無印記不屬於此情況</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的既有印記損壞；已依版本鎖定行重新取件並重建印記。</mark>

#### VK0045
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">After confirming the tool is fully imported, add receives a tag different from the current locked version; &lt;upgrade_command&gt; is filled in by VK as just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;, using the tag specified this time, with arguments quoted by POSIX shell rules</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot add &lt;repo&gt; at &lt;tag&gt;: it is already imported at &lt;current_tag&gt;. Run: &lt;upgrade_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">add 在確認工具已完整導入後，收到不同於目前鎖定版本的 tag；&lt;upgrade_command&gt; 由 VK 填成 just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;，使用這次指定的 tag，參數依 POSIX shell 規則加引號</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法以 &lt;tag&gt; 加入 &lt;repo&gt;：它已以 &lt;current_tag&gt; 導入。請執行：&lt;upgrade_command&gt;</mark>

#### VK0046
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The tool specified to remove or undev is not in the lock version lines; incomplete progress is identified first, before determining that the target does not exist</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Tool &lt;repo&gt; is not in the lock version lines. The requested operation did not complete.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">remove 或 undev 指定的工具不在版本鎖定行；先辨識未完成進度，再判斷對象不存在</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">版本鎖定行中沒有工具 &lt;repo&gt;。要求的操作未完成。</mark>

#### VK0047
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test cannot complete its checks because files in cache/ or gen/ are missing; it does not fetch, and does not prepare or repair cache/, gen/, or progress files; the run log is still written; whether a fresh CI checkout that has not yet fetched counts as missing files is pending confirmation (see #47, #124)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot complete checks for &lt;target&gt;: required local files are missing: &lt;files&gt;. Run: just vendor_kit sync</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test 因 cache/ 或 gen/ 缺件而無法完成檢查；不取件、不準備或修復 cache/、gen/、進度檔，執行紀錄照寫；CI 全新 checkout 尚未取件時是否算缺件，待確認（見 #47、#124）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法完成 &lt;target&gt; 的檢查：缺少必要的本機檔：&lt;files&gt;。請執行：just vendor_kit sync</mark>

#### VK0048
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test dist runs in a repo with no tool delivery content</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot check tool delivery content: &lt;path&gt; contains no delivery content.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test dist 在沒有工具交付內容的 repo 執行</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法檢查工具交付內容：&lt;path&gt; 沒有交付內容。</mark>

#### VK0049
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test or test dist did not complete its checks because the environment is insufficient; &lt;reason&gt; names the missing environment condition</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot complete checks for &lt;target&gt;: &lt;reason&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test 或 test dist 因環境不足而未完成檢查；&lt;reason&gt; 指明缺少的環境條件</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法完成 &lt;target&gt; 的檢查：&lt;reason&gt;。</mark>

#### VK0050
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">dev specifies a source different from the existing local override; the existing override is not replaced; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target</mark>
- `message.en`：<mark style="background-color:#c8f0c8">A different local override is already active for &lt;target&gt;. Run first: &lt;undev_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">dev 指定不同於現有本機覆寫的來源；不取代現有覆寫；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;target&gt; 已有另一個本機覆寫在作用中。請先執行：&lt;undev_command&gt;</mark>

#### VK0051
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The local directory specified to dev does not exist, or its content does not match the tool's delivery format; relative paths are resolved against the install directory</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot use local source &lt;path&gt; for &lt;repo&gt;: &lt;reason&gt;. The local override was not enabled.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">dev 指定的本機目錄不存在，或內容不符合該工具的交付格式；相對路徑以安裝目錄為準</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法以本機來源 &lt;path&gt; 作為 &lt;repo&gt; 的來源：&lt;reason&gt;。未啟用本機覆寫。</mark>

#### VK0052
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">An action that needs to read a local override source finds the source invalid; only actions that need to read it are blocked; undev can remove the override without reading the source, test still reports VK0032, bootstrap.sh ignores the override, and update checks versions according to the lock version line; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot read the local override source &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. Run: &lt;undev_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">需要讀取本機覆寫來源的動作發現來源失效；只擋需要讀取它的動作；undev 不讀來源即可解除，test 仍報 VK0032，bootstrap.sh 忽略覆寫，update 照版本鎖定行查版本；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法讀取 &lt;target&gt; 的本機覆寫來源 &lt;source&gt;：&lt;reason&gt;。請執行：&lt;undev_command&gt;</mark>

#### VK0053
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Synchronization fails after undev removes an override, or a read-only recipe detects an incomplete undev progress file; sync does not clear the progress file on undev's behalf; &lt;undev_command&gt; is filled from the progress file as the original just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The undev operation for &lt;target&gt; is incomplete. Run again: &lt;undev_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">undev 解除覆寫後同步失敗，或唯讀 recipe 偵測到未完成的 undev 進度檔；sync 不代替 undev 清掉進度檔；&lt;undev_command&gt; 依進度檔填成原本的 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;target&gt; 的 undev 操作未完成。請再執行一次：&lt;undev_command&gt;</mark>

#### VK0054
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A read-only recipe detects a progress file for an incomplete writing recipe other than the four kinds (incomplete import, tool upgrade, engine upgrade, undev), such as remove, install, uninstall, or dev; it does not resume or delete the progress file; bootstrap.sh still follows the existing determinations of VK0037 and VK0023 and does not widen the initial-import exception; &lt;original_command&gt; is rebuilt by VK from the progress file as the original full command, keeping its arguments, quoted by POSIX shell rules</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Operation &lt;operation&gt; in &lt;install_dir&gt; is incomplete. Run again: &lt;original_command&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">唯讀 recipe 偵測到未完成導入、工具 upgrade、引擎 upgrade、undev 這四種以外的可寫 recipe（如 remove、install、uninstall、dev）未完成的進度檔；不恢復、不刪進度檔；bootstrap.sh 仍依 VK0037 與 VK0023 的既有判定，不擴大首次導入例外；&lt;original_command&gt; 由 VK 依進度檔重組原本完整指令，保留參數並依 POSIX shell 規則加引號</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;install_dir&gt; 中的 &lt;operation&gt; 操作未完成。請再執行一次：&lt;original_command&gt;</mark>

#### VK0055
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A network, registry, or authentication error (including timeout) occurs while update, add, upgrade, or sync lists tags or obtains a tool image; missing registry credentials for listing versions still report VK0001; update does not report up-to-date from a stale cache and does not prompt for authentication</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot access &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. The requested operation did not complete.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">update、add、upgrade 或 sync 列 tag 或取得工具 image 時發生網路、registry 或認證錯誤（含逾時）；缺少列版本的 registry 憑證仍報 VK0001；update 不以舊快取回報已是最新版，不跳出認證詢問</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法存取 &lt;target&gt; 的 &lt;source&gt;：&lt;reason&gt;。要求的操作未完成。</mark>

沒改動的代碼 0 個。
