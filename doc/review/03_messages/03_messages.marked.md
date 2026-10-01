<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定稿時整個送審資料夾一個 commit 刪除；基準是維護者回覆過的送審 commit ccde94f。正式內容看 /doc/contract/03_messages.md 與 /doc/contract/03_messages.csv -->

# 03 訊息與錯誤碼總表

<mark style="background-color:#f8c8c8">這一頁列出 <ins>VK</ins> 每個<ins>結束碼</ins>的意思，以及每條<ins>診斷</ins>的固定格式。結束碼是契約，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。</mark>
<mark style="background-color:#c8f0c8">這一頁列出 [VK](../../../GLOSSARY.md#角色與情境) 每個[結束碼](../../../GLOSSARY.md#執行與結果)的意思，以及每條[診斷](../../../GLOSSARY.md#執行與結果)的固定格式。結束碼是[契約](../../../GLOSSARY.md#介面版與契約)，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。</mark>

- 名詞見[名詞表](../../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

<mark style="background-color:#f8c8c8">每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：</mark>
<mark style="background-color:#c8f0c8">每個指令結束時回一個數字，給呼叫它的人或自動化判斷結果：</mark>

| <mark style="background-color:#f8c8c8">結束碼</mark> | <mark style="background-color:#f8c8c8"><ins>level</ins></mark> | <mark style="background-color:#f8c8c8">意思</mark> |
| <mark style="background-color:#c8f0c8">結束碼</mark> | <mark style="background-color:#c8f0c8">[level](../../../GLOSSARY.md#執行與結果)</mark> | <mark style="background-color:#c8f0c8">意思</mark> |
|---|---|---|
| <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">info</mark> | <mark style="background-color:#f8c8c8">成功；沒有任何警告，也沒有要人接手的事項</mark> |
| <mark style="background-color:#f8c8c8">`1`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">有<ins>警告</ins>，或做完但要人接手；見表下的結束碼 `1`</mark> |
| <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">沒做完：<ins>需人處理</ins>、<ins>失敗</ins>或用法錯誤</mark> |
| <mark style="background-color:#f8c8c8">`3`</mark> | <mark style="background-color:#f8c8c8">fatal</mark> | <mark style="background-color:#f8c8c8">只限現有<ins>薄殼</ins>、<ins>VK 檔</ins>、<ins>引擎</ins>的版本組合不合。以這個碼結束的那次執行不動 <ins>repo 檔</ins>與 VK 檔，執行紀錄除外</mark> |
| <mark style="background-color:#c8f0c8">`0`</mark> | <mark style="background-color:#c8f0c8">info</mark> | <mark style="background-color:#c8f0c8">成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果)，也沒有要人接手的事項</mark> |
| <mark style="background-color:#c8f0c8">`1`</mark> | <mark style="background-color:#c8f0c8">warn</mark> | <mark style="background-color:#c8f0c8">有警告，或做完但要人接手；見表下的結束碼 `1`</mark> |
| <mark style="background-color:#c8f0c8">`2`</mark> | <mark style="background-color:#c8f0c8">error</mark> | <mark style="background-color:#c8f0c8">沒做完：[需人處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤</mark> |
| <mark style="background-color:#c8f0c8">`3`</mark> | <mark style="background-color:#c8f0c8">fatal</mark> | <mark style="background-color:#c8f0c8">只限現有[薄殼](../../../GLOSSARY.md#vk-組件)、[VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、[引擎](../../../GLOSSARY.md#vk-組件)的版本組合不合。以這個碼結束的那次執行不動 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與 VK 檔，[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)除外</mark> |

結束碼 `1` 有兩種：

- 有警告
- <mark style="background-color:#f8c8c8">做完但要人接手（不算警告）：留下<ins>合併衝突</ins>、`update --exit-code` 查到新版</mark>
- <mark style="background-color:#c8f0c8">做完但要人接手（不算警告）：留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)、`update --exit-code` 查到新版</mark>

<mark style="background-color:#f8c8c8">只有警告也以 `1` 結束。本機與 CI 使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>
<mark style="background-color:#c8f0c8">只有警告也以 `1` 結束。每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>

<mark style="background-color:#f8c8c8">一次處理多個工具時：</mark>
<mark style="background-color:#c8f0c8">一次處理多個[工具](../../../GLOSSARY.md#工具與出貨)時：</mark>

- 結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`1`)、C 查詢失敗 (`2`)，就以 `2` 結束
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意：

```text
stdout: A 已是最新。
stdout: B 有新版 v1.3.0（目前為 v1.2.0）。
<mark style="background-color:#f8c8c8">stderr: vendor_kit: warn[VK0022]: B 有新版：目前為 v1.2.0，新版為 v1.3.0。可執行：just vendor_kit upgrade B</mark>
<mark style="background-color:#f8c8c8">stderr: vendor_kit: error[VK0001]: 無法列舉 C 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade C@<tag>（拉取使用主機 docker 認證）</mark>
<mark style="background-color:#c8f0c8">stderr: vendor_kit: warn[VK0022]: A newer version of B is available: current v1.2.0; new v1.3.0. Run: just vendor_kit upgrade B</mark>
<mark style="background-color:#c8f0c8">stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag> (pulling uses the host's Docker credentials).</mark>
exit code: 2
```

## 輸出

- 成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴
- <mark style="background-color:#f8c8c8">stderr 只放診斷及其續行、<ins>詢問</ins>文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法</mark>
- <mark style="background-color:#f8c8c8">只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以 `2` 結束</mark>
- <mark style="background-color:#c8f0c8">stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法</mark>
- <mark style="background-color:#c8f0c8">只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印下列診斷，接著印簡短用法，以 `2` 結束：</mark>

  <mark style="background-color:#c8f0c8">```text</mark>
  <mark style="background-color:#c8f0c8">vendor_kit: error[VK0024]: No command was specified.</mark>
  <mark style="background-color:#c8f0c8">```</mark>
- 主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷
- <mark style="background-color:#f8c8c8">`remove`／`uninstall` 依契約保留初始檔時，把保留清單印到 stdout，以 `0` 結束</mark>
- <mark style="background-color:#f8c8c8">詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束</mark>
- <mark style="background-color:#c8f0c8">`remove`／`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，以 `0` 結束</mark>
- <mark style="background-color:#c8f0c8">詢問時[使用者](../../../GLOSSARY.md#角色與情境)明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束</mark>
- 顏色照這幾條：
  - 只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))
  - <mark style="background-color:#f8c8c8">給程式讀的輸出永遠不含顏色，例如<ins>執行紀錄</ins></mark>
  - <mark style="background-color:#c8f0c8">給程式讀的輸出永遠不含顏色，例如執行紀錄</mark>
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

<mark style="background-color:#f8c8c8">每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <中文本文>`。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。多行診斷的續行也印到 stderr。</mark>
<mark style="background-color:#c8f0c8">每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <message>`。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。只有診斷本文固定使用英文；stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問與用法不在這條語言規則內。診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。中文說明見訊息表的 `description` 欄。多行診斷的續行也印到 stderr。</mark>

<mark style="background-color:#f8c8c8"><ins>原因代碼</ins>是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。</mark>
<mark style="background-color:#c8f0c8">[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。</mark>

<mark style="background-color:#f8c8c8">每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](../../contract/03_messages.csv)，一列一個代碼；本頁不再列一份。</mark>
<mark style="background-color:#c8f0c8">每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](../../contract/03_messages.csv)，一列一個代碼。</mark>

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
  - <mark style="background-color:#c8f0c8">`exit_code`：該 level 對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空</mark>
  - `disposition`：處置，`需人處理`、`失敗` 或留空；`warn` 一律留空
  - `situation`：什麼情況發出這個代碼，是它唯一的意思
  - <mark style="background-color:#f8c8c8">`message`：本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行</mark>
  - <mark style="background-color:#c8f0c8">`message`：英文本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行</mark>
  - <mark style="background-color:#c8f0c8">`description`：訊息的中文說明，給人閱讀；`active` 列必填</mark>
  - `next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；需人處理必填，失敗與沒有指令的留空；做不到的診斷標失敗
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - `situation` 註明原樣印出的，由使用者換成要用的值
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - 要依 level 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號

---

## 03_messages.csv 的逐碼差異

依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。

- 表頭：<mark style="background-color:#f8c8c8">code,status,level,disposition,situation,message,next_step</mark> → <mark style="background-color:#c8f0c8">code,status,level,exit_code,disposition,situation,message,description,next_step</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `description`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0001

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：<mark style="background-color:#f8c8c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;指令&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark> → <mark style="background-color:#c8f0c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;command&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark>
- `message`：<mark style="background-color:#f8c8c8">無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;指令&gt; &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）</mark> → <mark style="background-color:#c8f0c8">Cannot list versions for &lt;repo&gt;: registry read access is required. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt; (pulling uses the host's Docker credentials).</mark>
- `description`：<mark style="background-color:#c8f0c8">無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0002

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：<mark style="background-color:#f8c8c8">操作需要詢問，但沒帶 -y 又不能互動（沒有終端，或讀到輸入結束）；&lt;加上 -y 的原指令&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後</mark> → <mark style="background-color:#c8f0c8">操作需要詢問，但沒帶 -y 又不能互動（沒有終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後</mark>
- `message`：<mark style="background-color:#f8c8c8">需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;加上 -y 的原指令&gt;</mark> → <mark style="background-color:#c8f0c8">Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;加上 -y 的原指令&gt;</mark> → <mark style="background-color:#c8f0c8">&lt;command_with_y&gt;</mark>

#### VK0003
<mark style="background-color:#f8c8c8">（本碼停用）</mark>

- `status`：<mark style="background-color:#f8c8c8">active</mark> → <mark style="background-color:#c8f0c8">retired</mark>
- `level`：<mark style="background-color:#f8c8c8">error</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation`：<mark style="background-color:#f8c8c8">CI 模式下，基準版落後版本鎖定行</mark> → <mark style="background-color:#c8f0c8">基準版落後版本鎖定行</mark>
- `message`：<mark style="background-color:#f8c8c8">請在本機執行 just vendor_kit upgrade &lt;repo&gt; -y 後 commit 並 push</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade &lt;repo&gt; -y</mark> → <mark style="background-color:#c8f0c8">（空）</mark>

#### VK0004

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：sync 發現某個工具未完成導入
- `message`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 未完成導入，請執行：just vendor_kit add &lt;repo&gt;</mark> → <mark style="background-color:#c8f0c8">Import of &lt;repo&gt; is incomplete. Run: just vendor_kit add &lt;repo&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 未完成導入，請執行：just vendor_kit add &lt;repo&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit add &lt;repo&gt;

#### VK0005

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：<mark style="background-color:#f8c8c8">bootstrap.sh 發現主機的 just 低於 1.33.0；&lt;安裝指令&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark> → <mark style="background-color:#c8f0c8">bootstrap.sh 發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark>
- `message`：<mark style="background-color:#f8c8c8">需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;平台對應的下載網址&gt;<br>安裝：&lt;安裝指令&gt;</mark> → <mark style="background-color:#c8f0c8">just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;安裝指令&gt;</mark> → <mark style="background-color:#c8f0c8">&lt;install_command&gt;</mark>

#### VK0006

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）；&lt;files&gt; 逐檔標出是哪一種，除執行紀錄外不動 repo 檔與其他 VK 檔
- `message`：<mark style="background-color:#f8c8c8">偵測到薄殼跟這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">Shell files do not match this engine version's templates: &lt;files&gt;. No shell files were regenerated. Review the following differences; restore any manual changes, then run: just vendor_kit upgrade --engine</mark>
- `description`：<mark style="background-color:#c8f0c8">偵測到薄殼跟這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0007

- `status`：active
- `level`：fatal
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：upgrade --engine=&lt;tag&gt; 降版，但目標引擎無法無損讀取現有的 VK 檔；本文的 &lt;tag&gt; 原樣印出，由使用者換成能讀取檔案版 &lt;N&gt; 的引擎版本 tag
- `message`：<mark style="background-color:#f8c8c8">目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;</mark> → <mark style="background-color:#c8f0c8">Target engine &lt;vY&gt; (interface version &lt;P&gt;, schema version &lt;M&gt;) cannot read the existing files (schema version &lt;N&gt;) without loss. No files were modified except the run log. Specify a version that can read schema version &lt;N&gt;: just vendor_kit upgrade --engine=&lt;tag&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0008

- `status`：active
- `level`：fatal
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限
- `message`：<mark style="background-color:#f8c8c8">無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">Cannot read &lt;file&gt;: schema version &lt;N&gt; is newer than the maximum supported version &lt;M&gt;; written by vendor_kit &lt;written_by&gt;. Upgrade the engine: just vendor_kit upgrade --engine</mark>
- `description`：<mark style="background-color:#c8f0c8">無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit upgrade --engine

#### VK0009

- `status`：active
- `level`：fatal
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe
- `message`：<mark style="background-color:#f8c8c8">薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine</mark>
- `description`：<mark style="background-color:#c8f0c8">薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit upgrade --engine

#### VK0010

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：任何 VK recipe 建不出執行紀錄（在任何副作用之前結束）
- `message`：<mark style="background-color:#f8c8c8">無法寫入執行紀錄 &lt;path&gt;：&lt;原因&gt;。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。</mark> → <mark style="background-color:#c8f0c8">Cannot write run log &lt;path&gt;: &lt;reason&gt;. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry.</mark>
- `description`：<mark style="background-color:#c8f0c8">無法寫入執行紀錄 &lt;path&gt;：&lt;reason&gt;。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0011

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：docker --version 的輸出含 podman
- `message`：<mark style="background-color:#f8c8c8">偵測到 podman (docker --version)。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。</mark> → <mark style="background-color:#c8f0c8">Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.</mark>
- `description`：<mark style="background-color:#c8f0c8">偵測到 podman (docker --version)。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0012

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：啟動器發現主機的 Docker 低於 19.03
- `message`：<mark style="background-color:#f8c8c8">需要 Docker ≥ 19.03，目前為 &lt;version&gt;。請升級 Docker 後重試。</mark> → <mark style="background-color:#c8f0c8">Docker 19.03 or later is required; the current version is &lt;version&gt;. Upgrade Docker and retry.</mark>
- `description`：<mark style="background-color:#c8f0c8">需要 Docker ≥ 19.03，目前為 &lt;version&gt;。請升級 Docker 後重試。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0013

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：metadata 缺失或損壞，無法可靠還原
- `message`：<mark style="background-color:#f8c8c8">無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。</mark> → <mark style="background-color:#c8f0c8">Cannot process &lt;file&gt;: metadata is missing or corrupt and cannot be restored reliably. vendor_kit does not guess when records are unavailable; no files were modified except the run log. Preserve &lt;file&gt; and run log &lt;path&gt;. If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.</mark>
- `description`：<mark style="background-color:#c8f0c8">無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0014

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：<mark style="background-color:#f8c8c8">本機執行 sync，發現基準版落後版本鎖定行</mark> → <mark style="background-color:#c8f0c8">sync 或 test 發現基準版落後版本鎖定行</mark>
- `message`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y</mark> → <mark style="background-color:#c8f0c8">The baseline for &lt;repo&gt; is behind the lock version line. Run: just vendor_kit upgrade &lt;repo&gt; -y</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit upgrade &lt;repo&gt; -y

#### VK0015

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：sync 發現 cache/ 的逐檔指紋不符，已重新取件
- `message`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。</mark> → <mark style="background-color:#c8f0c8">Per-file digests in cache/ for &lt;repo&gt; did not match; refetched according to the lock version line.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0016

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：收回 append 行時，在檔內找不到當初插入的原文
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; 找不到要收回的原文；未刪除該行，請手動檢查。</mark> → <mark style="background-color:#c8f0c8">Could not find the original text to remove from &lt;file&gt;; the line was not removed. Check it manually.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;file&gt; 找不到要收回的原文；未刪除該行，請手動檢查。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0017

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：收回 append 行時，在檔內找到多處與當初插入的原文相同
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; 找到 &lt;count&gt; 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。</mark> → <mark style="background-color:#c8f0c8">Found &lt;count&gt; occurrences of the original text to remove from &lt;file&gt; and could not attribute one uniquely; the line was not removed. Check it manually.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;file&gt; 找到 &lt;count&gt; 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0018

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：add 遇到已存在、尚未納管的檔
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; 已存在且未納管；未覆蓋，也未納管這個檔。</mark> → <mark style="background-color:#c8f0c8">&lt;file&gt; already exists and is unmanaged; it was neither overwritten nor brought under management.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;file&gt; 已存在且未納管；未覆蓋，也未納管這個檔。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0019

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：檔案沒有納管，本次不處理
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; 沒有納管；本次未處理這個檔。</mark> → <mark style="background-color:#c8f0c8">&lt;file&gt; is unmanaged and was not processed.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;file&gt; 沒有納管；本次未處理這個檔。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0020

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：這個版本先前已由使用者拒絕
- `message`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；本次不再詢問，也未套用。</mark> → <mark style="background-color:#c8f0c8">Version &lt;tag&gt; of &lt;repo&gt; was previously rejected; it was not prompted again or applied.</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；本次不再詢問，也未套用。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0021

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：基準版合併留下合併衝突
- `message`：<mark style="background-color:#f8c8c8">&lt;file&gt; 留下合併衝突，請檢視後解決：git status</mark> → <mark style="background-color:#c8f0c8">&lt;file&gt; contains merge conflicts. Review and resolve them: git status</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;file&gt; 留下合併衝突，請檢視後解決：git status</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：git status

#### VK0022

- `status`：active
- `level`：warn
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：update --exit-code 查到新版
- `message`：<mark style="background-color:#f8c8c8">&lt;repo&gt; 有新版：目前為 &lt;current_tag&gt;，新版為 &lt;new_tag&gt;。可執行：just vendor_kit upgrade &lt;repo&gt;</mark> → <mark style="background-color:#c8f0c8">A newer version of &lt;repo&gt; is available: current &lt;current_tag&gt;; new &lt;new_tag&gt;. Run: just vendor_kit upgrade &lt;repo&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 有新版：目前為 &lt;current_tag&gt;，新版為 &lt;new_tag&gt;。可執行：just vendor_kit upgrade &lt;repo&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit upgrade &lt;repo&gt;

#### VK0023

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：upgrade --engine 換上新引擎後停下，要求重跑
- `message`：<mark style="background-color:#f8c8c8">已換上引擎 &lt;vY&gt;，請再執行一次：just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">Engine &lt;vY&gt; is now installed. Run again: just vendor_kit upgrade --engine</mark>
- `description`：<mark style="background-color:#c8f0c8">已換上引擎 &lt;vY&gt;，請再執行一次：just vendor_kit upgrade --engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：just vendor_kit upgrade --engine

#### VK0024

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：用法錯誤：只打 just vendor_kit、未指定指令
- `message`：<mark style="background-color:#f8c8c8">未指定指令。</mark> → <mark style="background-color:#c8f0c8">No command was specified.</mark>
- `description`：<mark style="background-color:#c8f0c8">未指定指令。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0025

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：用法錯誤：缺少必要參數
- `message`：<mark style="background-color:#f8c8c8">缺少必要參數：&lt;參數&gt;。</mark> → <mark style="background-color:#c8f0c8">Required argument is missing: &lt;argument&gt;.</mark>
- `description`：<mark style="background-color:#c8f0c8">缺少必要參數：&lt;argument&gt;。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0026

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：用法錯誤：不認得指令或選項
- `message`：<mark style="background-color:#f8c8c8">不認得的指令或選項：&lt;值&gt;。</mark> → <mark style="background-color:#c8f0c8">Unknown command or option: &lt;value&gt;.</mark>
- `description`：<mark style="background-color:#c8f0c8">不認得的指令或選項：&lt;value&gt;。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0027

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation`：用法錯誤：tag 格式不合
- `message`：<mark style="background-color:#f8c8c8">tag 格式不合：&lt;tag&gt;；只接受 vX.Y.Z，X、Y、Z 不收前導零。</mark> → <mark style="background-color:#c8f0c8">Invalid tag format: &lt;tag&gt;. Use vX.Y.Z with no leading zeros in X, Y, or Z.</mark>
- `description`：<mark style="background-color:#c8f0c8">tag 格式不合：&lt;tag&gt;；只接受 vX.Y.Z，X、Y、Z 不收前導零。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0028

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：在安裝目錄外執行 VK recipe
- `message`：<mark style="background-color:#f8c8c8">目前不在安裝目錄，請執行：cd &lt;install_dir&gt;</mark> → <mark style="background-color:#c8f0c8">The current directory is not an install directory. Run: cd &lt;install_dir&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">目前不在安裝目錄，請執行：cd &lt;install_dir&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：cd &lt;install_dir&gt;

#### VK0029

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：install 時上層或下層已有安裝目錄
- `message`：<mark style="background-color:#f8c8c8">不能建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。</mark> → <mark style="background-color:#c8f0c8">Cannot create a nested install directory: &lt;existing_install_dir&gt; is already an install directory.</mark>
- `description`：<mark style="background-color:#c8f0c8">不能建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0030

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：add 時 &lt;ns&gt; 撞名
- `message`：<mark style="background-color:#f8c8c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark> → <mark style="background-color:#c8f0c8">Cannot add &lt;repo&gt;: namespace &lt;ns&gt; is already used by &lt;owner&gt;.</mark>
- `description`：<mark style="background-color:#c8f0c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0031

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：失敗
- `situation`：離線導入的 image 缺少必要的 digest 資訊
- `message`：<mark style="background-color:#f8c8c8">無法從 &lt;image&gt; 導入：缺少必要的 digest 資訊。</mark> → <mark style="background-color:#c8f0c8">Cannot import from &lt;image&gt;: required digest information is missing.</mark>
- `description`：<mark style="background-color:#c8f0c8">無法從 &lt;image&gt; 導入：缺少必要的 digest 資訊。</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0032

- `status`：active
- `level`：error
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `disposition`：需人處理
- `situation`：<mark style="background-color:#f8c8c8">CI 模式發現本機覆寫；&lt;解除本機覆寫的指令&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark> → <mark style="background-color:#c8f0c8">test 發現本機覆寫；&lt;undev_command&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark>
- `message`：<mark style="background-color:#f8c8c8">CI 模式不能使用 &lt;target&gt; 的本機覆寫，請在本機執行：&lt;解除本機覆寫的指令&gt;</mark> → <mark style="background-color:#c8f0c8">Test cannot run while a local override of &lt;target&gt; is active. Run: &lt;undev_command&gt;</mark>
- `description`：<mark style="background-color:#c8f0c8">test 發現 &lt;target&gt; 的本機覆寫，請先執行：&lt;undev_command&gt;</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `next_step`：<mark style="background-color:#f8c8c8">&lt;解除本機覆寫的指令&gt;</mark> → <mark style="background-color:#c8f0c8">&lt;undev_command&gt;</mark>

沒改動的代碼 0 個。
