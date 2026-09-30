# 03 訊息與錯誤碼總表

這一頁列出 <ins>VK</ins> 每個<ins>結束碼</ins>的意思，以及每條<ins>診斷</ins>的固定格式。結束碼是契約，依 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)。

- 名詞見[名詞表](../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：

| 結束碼 | <ins>level</ins> | 意思 |
|---|---|---|
| `0` | info | 成功；沒有任何警告，也沒有要人接手的事項 |
| `1` | warn | 有<ins>警告</ins>，或做完但要人接手；見表下的結束碼 `1` |
| `2` | error | 沒做完：<ins>需人處理</ins>、<ins>失敗</ins>或用法錯誤 |
| `3` | fatal | 只限現有<ins>薄殼</ins>、<ins>VK 檔</ins>、<ins>引擎</ins>的版本組合不合。以這個碼結束的那次執行不動 <ins>repo 檔</ins>與 VK 檔，執行紀錄除外 |

結束碼 `1` 有兩種：

- 有警告
- 做完但要人接手（不算警告）：留下<ins>合併衝突</ins>、`update --exit-code` 查到新版

只有警告也以 `1` 結束。本機與 CI 使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。

一次處理多個工具時：

- 結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`1`)、C 查詢失敗 (`2`)，就以 `2` 結束
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意：

```text
stdout: A 已是最新。
stdout: B 有新版 v1.3.0（目前為 v1.2.0）。
stderr: vendor_kit: warn[VK0022]: B 有新版：目前為 v1.2.0，新版為 v1.3.0。可執行：just vendor_kit upgrade B
stderr: vendor_kit: error[VK0001]: 無法列舉 C 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade C@<tag>（拉取使用主機 docker 認證）
exit code: 2
```

## 輸出

- 成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴
- stderr 只放診斷及其續行、<ins>詢問</ins>文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法
- 只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以 `2` 結束
- 主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷
- `remove`／`uninstall` 依契約保留初始檔時，把保留清單印到 stdout，以 `0` 結束
- 詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - 只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))
  - 給程式讀的輸出永遠不含顏色，例如<ins>執行紀錄</ins>
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <中文本文>`。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。多行診斷的續行也印到 stderr。

<ins>原因代碼</ins>是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。

每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](03_messages.csv)，一列一個代碼；本頁不再列一份。

處置與下一步：

- 處置是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令（不用使用者代換的單一指令）；失敗不承諾可執行的修法，但可以附一般建議；不屬於兩者的留空
- warn 要指名對象；有辦法處置就列出下一步

訊息表怎麼讀：

- 格式
  - UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號
  - 儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字
- 欄位
  - `code`：原因代碼，從 `VK0001` 起逐列加一，不缺列
  - `status`：`active` 使用中；`retired` 已停用，只留 `code`、`status`、`situation`
  - `level`：`warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)
  - `disposition`：處置，`需人處理`、`失敗` 或留空；`warn` 一律留空
  - `situation`：什麼情況發出這個代碼，是它唯一的意思
  - `message`：本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行
  - `next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；需人處理必填，失敗與沒有指令的留空；做不到的診斷標失敗
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - `situation` 註明原樣印出的，由使用者換成要用的值
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - 要依 level 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號
