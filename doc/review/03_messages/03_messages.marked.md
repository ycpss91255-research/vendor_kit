<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除；本檔進 git，定案時刪除該鍵的送審資料夾；基準是維護者回覆過的送審 commit a49bca0。正式內容看 /doc/contract/03_messages.md 與 /doc/contract/03_messages.csv -->

# 03 訊息與錯誤碼總表

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
| <mark style="background-color:#c8f0c8">結束碼</mark> | <mark style="background-color:#c8f0c8">對應嚴重度</mark> | <mark style="background-color:#c8f0c8">意思</mark> |
|---|---|---|
| <mark style="background-color:#f8c8c8">`0`</mark> | <mark style="background-color:#f8c8c8">info</mark> | <mark style="background-color:#f8c8c8">成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果)，也沒有要人接手的事項</mark> |
| <mark style="background-color:#f8c8c8">`1`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">有警告，或做完但要人接手；見表下的結束碼 `1`</mark> |
| <mark style="background-color:#f8c8c8">`2`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">沒做完：[需人處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤</mark> |
| <mark style="background-color:#c8f0c8">`0`</mark> | <mark style="background-color:#c8f0c8">info</mark> | <mark style="background-color:#c8f0c8">成功；沒有任何[警告](../../../GLOSSARY.md#執行與結果)</mark> |
| <mark style="background-color:#c8f0c8">`1`</mark> | <mark style="background-color:#c8f0c8">warn</mark> | <mark style="background-color:#c8f0c8">指令承諾的結果已做完，但有警告</mark> |
| <mark style="background-color:#c8f0c8">`2`</mark> | <mark style="background-color:#c8f0c8">error</mark> | <mark style="background-color:#c8f0c8">指令承諾的結果沒做完，可能是[待處理](../../../GLOSSARY.md#執行與結果)、[失敗](../../../GLOSSARY.md#執行與結果)或用法錯誤</mark> |
| `3` | fatal | 只限現有[薄殼](../../../GLOSSARY.md#vk-組件)、[VK 檔](../../../GLOSSARY.md#repo-內的檔與狀態)、[引擎](../../../GLOSSARY.md#vk-組件)的版本組合不合。以這個碼結束的那次執行不動 [repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與 VK 檔，[執行紀錄](../../../GLOSSARY.md#repo-內的檔與狀態)除外 |

<mark style="background-color:#f8c8c8">結束碼 `1` 有兩種：</mark>
<mark style="background-color:#c8f0c8">這張表只列 VK 回的結束碼；指令到不了 VK 時由 just 回的碼不在內。</mark>

- <mark style="background-color:#f8c8c8">有警告</mark>
- <mark style="background-color:#f8c8c8">做完但要人接手（不算警告）：留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)、`update --exit-code` 查到新版</mark>
<mark style="background-color:#f8c8c8">只有警告也以 `1` 結束。每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>
<mark style="background-color:#c8f0c8">留下[合併衝突](../../../GLOSSARY.md#初始檔與合併)、`update --exit-code` 查到新版都屬於警告，碼仍是 `1`。每個 recipe 不論在哪個環境執行，都使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。</mark>

一次處理多個[工具](../../../GLOSSARY.md#工具與出貨)時：

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
- stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法
- <mark style="background-color:#f8c8c8">只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印下列診斷，接著印簡短用法，以 `2` 結束：</mark>
- <mark style="background-color:#c8f0c8">只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：</mark>

  ```text
  <mark style="background-color:#f8c8c8">vendor_kit: error[VK0024]: No command was specified.</mark>
  <mark style="background-color:#c8f0c8">$ just vendor_kit</mark>
  <mark style="background-color:#c8f0c8">stderr: vendor_kit <版本></mark>
  <mark style="background-color:#c8f0c8">stderr: vendor_kit: error[VK0024]: No command was specified.</mark>
  <mark style="background-color:#c8f0c8">stderr: 用法：just vendor_kit <指令> [參數] [選項]</mark>
  <mark style="background-color:#c8f0c8">exit code: 2</mark>
  ```
- 主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷
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
- <mark style="background-color:#c8f0c8">第一行格式固定如下，診斷使用的嚴重度見[名詞表](../../../GLOSSARY.md#執行與結果)：</mark>

  <mark style="background-color:#c8f0c8">```text</mark>
  <mark style="background-color:#c8f0c8">vendor_kit: <level>[VKnnnn]: <message></mark>
  <mark style="background-color:#c8f0c8">```</mark>
- <mark style="background-color:#c8f0c8">只有診斷本文固定使用英文；stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問與用法不在這條語言規則內。診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。</mark>
- <mark style="background-color:#c8f0c8">中文說明見訊息表的 `description` 欄。</mark>
- <mark style="background-color:#c8f0c8">多行診斷的續行也印到 stderr。</mark>

[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。

<mark style="background-color:#f8c8c8">每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](../../contract/03_messages.csv)，一列一個代碼。</mark>
<mark style="background-color:#c8f0c8">每個代碼的嚴重度、處置、情況、本文與下一步，只寫在[訊息表](../../contract/03_messages.csv)，一列一個代碼。</mark>

處置與下一步：

- <mark style="background-color:#f8c8c8">處置是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令（不用使用者代換的單一指令）；失敗不承諾可執行的修法，但可以附一般建議；不屬於兩者的留空</mark>
- <mark style="background-color:#c8f0c8">處置是診斷的屬性，不是嚴重度。待處理表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令；失敗不承諾可執行的修法，但可以附一般建議；warn 的列與用法錯誤（VK0024～VK0027）留空</mark>
- warn 要指名對象；有辦法處置就列出下一步

訊息表怎麼讀：

- 格式
  - UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號
  - 儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字
- 欄位
  - `code`：原因代碼，從 `VK0001` 起逐列加一，不缺列
  - `status`：`active` 使用中；`retired` 已停用，只留 `code`、`status`、`situation`
  - <mark style="background-color:#f8c8c8">`level`：`warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)</mark>
  - <mark style="background-color:#f8c8c8">`exit_code`：該 level 對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空</mark>
  - <mark style="background-color:#f8c8c8">`disposition`：處置，`需人處理`、`失敗` 或留空；`warn` 一律留空</mark>
  - <mark style="background-color:#c8f0c8">`level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)</mark>
  - <mark style="background-color:#c8f0c8">`exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空</mark>
  - <mark style="background-color:#c8f0c8">`disposition`：處置，`待處理`、`失敗` 或留空；warn 的列與用法錯誤（VK0024～VK0027）留空</mark>
  - `situation`：什麼情況發出這個代碼，是它唯一的意思
  - `message`：英文本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行
  - `description`：訊息的中文說明，給人閱讀；`active` 列必填
  - <mark style="background-color:#f8c8c8">`next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；需人處理必填，失敗與沒有指令的留空；做不到的診斷標失敗</mark>
  - <mark style="background-color:#c8f0c8">`next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；待處理必填，失敗與沒有指令的留空；做不到的診斷標失敗</mark>
- 占位符
  - `<…>` 是占位符，VK 印出時換成實際的值
  - `situation` 註明原樣印出的，由使用者換成要用的值
- 查看
  - GitHub 上看是表格，搜尋框只能全文篩列
  - <mark style="background-color:#f8c8c8">要依 level 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號</mark>
  - <mark style="background-color:#c8f0c8">要依 `level` 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號</mark>

---

## 03_messages.csv 的逐碼差異

依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。

#### VK0002

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：操作需要詢問，但沒帶 -y 又不能互動（沒有終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後
- `message`：Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;
- `description`：需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;
- `next_step`：&lt;command_with_y&gt;

#### VK0004

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：sync 發現某個工具未完成導入
- `message`：Import of &lt;repo&gt; is incomplete. Run: just vendor_kit add &lt;repo&gt;
- `description`：&lt;repo&gt; 未完成導入，請執行：just vendor_kit add &lt;repo&gt;
- `next_step`：just vendor_kit add &lt;repo&gt;

#### VK0005

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：bootstrap.sh 發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具
- `message`：just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;
- `description`：需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;
- `next_step`：&lt;install_command&gt;

#### VK0008

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限
- `message`：Cannot read &lt;file&gt;: schema version &lt;N&gt; is newer than the maximum supported version &lt;M&gt;; written by vendor_kit &lt;written_by&gt;. Upgrade the engine: just vendor_kit upgrade --engine
- `description`：無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine
- `next_step`：just vendor_kit upgrade --engine

#### VK0009

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe
- `message`：Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine
- `description`：薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine
- `next_step`：just vendor_kit upgrade --engine

#### VK0023

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：<mark style="background-color:#f8c8c8">upgrade --engine 換上新引擎後停下，要求重跑</mark> → <mark style="background-color:#c8f0c8">upgrade --engine 換上新引擎後原指令尚未做完；&lt;original_command&gt; 是由 VK 填好的原指令</mark>
- `message`：<mark style="background-color:#f8c8c8">Engine &lt;vY&gt; is now installed. Run again: just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">Engine &lt;vY&gt; is now installed. Run again: &lt;original_command&gt;</mark>
- `description`：<mark style="background-color:#f8c8c8">已換上引擎 &lt;vY&gt;，請再執行一次：just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">已換上引擎 &lt;vY&gt;，請再執行一次原指令：&lt;original_command&gt;</mark>
- `next_step`：<mark style="background-color:#f8c8c8">just vendor_kit upgrade --engine</mark> → <mark style="background-color:#c8f0c8">&lt;original_command&gt;</mark>

#### VK0026

- `status`：active
- `level`：error
- `exit_code`：2
- `situation`：<mark style="background-color:#f8c8c8">用法錯誤：不認得指令或選項</mark> → <mark style="background-color:#c8f0c8">用法錯誤：VK recipe 帶了不認得的選項或多出的參數</mark>
- `message`：<mark style="background-color:#f8c8c8">Unknown command or option: &lt;value&gt;.</mark> → <mark style="background-color:#c8f0c8">Unknown option or extra argument: &lt;value&gt;.</mark>
- `description`：<mark style="background-color:#f8c8c8">不認得的指令或選項：&lt;value&gt;。</mark> → <mark style="background-color:#c8f0c8">不認得的選項或多出的參數：&lt;value&gt;。</mark>

#### VK0028

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：在安裝目錄外執行 VK recipe
- `message`：The current directory is not an install directory. Run: cd &lt;install_dir&gt;
- `description`：目前不在安裝目錄，請執行：cd &lt;install_dir&gt;
- `next_step`：cd &lt;install_dir&gt;

#### VK0032

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：<mark style="background-color:#f8c8c8">需人處理</mark> → <mark style="background-color:#c8f0c8">待處理</mark>
- `situation`：test 發現本機覆寫；&lt;undev_command&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine
- `message`：Test cannot run while a local override of &lt;target&gt; is active. Run: &lt;undev_command&gt;
- `description`：test 發現 &lt;target&gt; 的本機覆寫，請先執行：&lt;undev_command&gt;
- `next_step`：&lt;undev_command&gt;

沒改動的代碼 23 個：VK0001、VK0003、VK0006、VK0007、VK0010、VK0011、VK0012、VK0013、VK0014、VK0015、VK0016、VK0017、VK0018、VK0019、VK0020、VK0021、VK0022、VK0024、VK0025、VK0027、VK0029、VK0030、VK0031。
