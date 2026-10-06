<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除，程式碼區塊的改動改成 diff 區塊（+ 新增、- 刪除）；本檔進 git，定案時刪除該鍵的送審資料夾；基準是定案 commit 2425feb。正式內容看 /doc/contract/03_output.md 與 /doc/contract/reason_codes.csv -->

> 注意：定案後又有改動，回到待審

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
stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file <path> and rerun, or specify a version directly: just vendor_kit upgrade C@<tag>
exit code: 2
```

## 輸出

- 成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`/`--help` 用法只印到 stdout（[test](../../../GLOSSARY.md#vk-recipe-與用途) 帶路徑時轉出的測試輸出除外），不加前綴
- stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行、用法錯誤後附的用法，以及 [update](../../../GLOSSARY.md#vk-recipe-與用途) 印的[本機覆寫](../../../GLOSSARY.md#版本與來源)提醒（不加前綴；test 帶路徑時轉出的測試輸出除外）
- `just vendor_kit test` 帶路徑、跑[使用者](../../../GLOSSARY.md#角色與情境)自己的測試時，測試程式 (runner) 的 stdout 轉到 VK 的 stdout、stderr 轉到 VK 的 stderr，原樣轉出、不加前綴；這些輸出不是 VK 的固定格式，不承諾可解析，依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)
- 只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：

  ```text
  $ just vendor_kit
  stderr: vendor_kit <version>
  stderr: vendor_kit: error[VK0024]: No command was specified.
  stderr: Usage: just vendor_kit <cmd> [arguments] [options]
  exit code: 2
  ```
- <mark style="background-color:#f8c8c8">主機前置檢查（檢查主機上的 Docker 與 just）排在建執行紀錄之前；找不到 docker、Docker 低於 19.03、`docker --version` 的輸出含 Podman、找不到 just 或 just 低於 1.33.0 時，檢查不通過。不通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。各入口檢查哪幾項見 [04 使用者介面](../../contract/04_interface.md#bootstrapsh)</mark>
- <mark style="background-color:#c8f0c8">主機前置檢查（檢查主機上的 Docker、Docker daemon 形態與 just）排在建執行紀錄之前；找不到 docker、Docker 低於 19.03、`docker --version` 的輸出含 Podman、偵測到不支援的 Docker daemon 形態（待確認 (N6b)）、找不到 just 或 just 低於 1.33.0 時，檢查不通過。不通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。建執行紀錄之後、業務操作之前的能力檢查失敗走一般失敗（待確認 (N6b)）。支援清單見 [04 主機需求](../../contract/04_interface.md#主機需求)；各入口檢查哪幾項見 [04 使用者介面](../../contract/04_interface.md#bootstrapsh)</mark>
- `remove`/`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，沒有其他診斷時以 `0` 結束
- <mark style="background-color:#f8c8c8">詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束</mark>
- <mark style="background-color:#c8f0c8">詢問時使用者明確回答「否」，是正常取消，以 `0` 結束；一般在 stdout 說明未變更。若需記下拒絕，只在 [metadata](../../../GLOSSARY.md#初始檔與合併) 記錄 `state=declined`、`declined_hash` 與必要的檔案識別，執行紀錄照寫，stdout 說明「未變更，已記下這次拒絕」。[repo 檔](../../../GLOSSARY.md#repo-內的檔與狀態)與工具不動，不推進[版本鎖定行](../../../GLOSSARY.md#版本與來源)或[基準版](../../../GLOSSARY.md#初始檔與合併)，不套用同一次呼叫裡已答允的項目，也不把還沒回答的題記成拒絕</mark>
- <mark style="background-color:#c8f0c8">`--dry-run`（哪些指令接受見 [04 預演](../../contract/04_interface.md#預演)）在 stdout 用「Would …」字句列出會改的內容，一行一句，例如 `Would add …`、`Would create <file>`、`Would append to <file>`、`Would update <file>`、`Would merge <file>`、`Would lock …`、`Would write …`、`Would install …`。殘留[進度檔](../../../GLOSSARY.md#repo-內的檔與狀態)只印 `Would complete the interrupted <verb> of …`，不完成該次操作；最後一行固定是 `Dry run: no changes were made.`，未變更時也印。警告照常印到 stderr，結束碼依警告決定；沒有警告或其他失敗時以 `0` 結束（待確認 (D1)）</mark>
- <mark style="background-color:#c8f0c8">[基準版合併](../../../GLOSSARY.md#初始檔與合併)的結果是 TOML (`*.toml`) 且解析不過，或是 just 檔（`justfile`、`.justfile`，檔名不分大小寫；`*.just`）且留下衝突標記時，保留原檔、不詢問、不推進基準版，記進 metadata 的 `conflicts`。待確認 (D2)，兩個方案尚未選定：(a) 現行實作只在 stdout 說明保留的檔案、合併結果無效的原因與已記入 `conflicts`，不印診斷，沒有其他警告或失敗時以 `0` 結束；此案與本頁「留下合併衝突，碼仍是 `1`」及 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)不一致。(b) 照 `VK0021` 的前例報 `VK0087` warn 診斷，沒有其他失敗時以 `1` 結束；stdout 說明是否保留也待確認。兩案都不報 `VK0021`</mark>
- VK 自己印的字句，顏色照這幾條：
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
- VK 自己寫的字句（stdout 的[正常輸出](../../../GLOSSARY.md#執行與結果)、詢問、用法（含 `-h`/`--help` 與用法錯誤後附的簡短用法）、版本行、本機覆寫提醒、執行紀錄、stderr 診斷）目前都用英文；換進占位符的值（路徑、檔名、`<repo>`、[tag](../../../GLOSSARY.md#工具與出貨)、使用者給的參數）照原樣印出。之後若做多語系 (i18n)，診斷以訊息表的語言欄切換，其他字句另議。每條診斷的中文見訊息表的 `message.zh-TW`、`situation.zh-TW` 欄。
- 診斷本文以完整英文句子書寫，句首大寫並以句點結尾；以占位符或小寫的指令名開頭時照原樣，以指令結尾時不加句點，免得複製到句點。本文可能同時包含原因與下一步，需要保留完整句子的邊界。這些句型規則只適用於診斷本文。
- 多行診斷的續行也印到 stderr。

[原因代碼](../../../GLOSSARY.md#執行與結果)是 `VK` 加四位數字。每個代碼以訊息表的 `situation.<lang>` 欄為唯一意思；發出後永不重用。

每個代碼的嚴重度、處置、情況與本文，只寫在[訊息表](../../contract/reason_codes.csv)，一列一個代碼。訊息表只收 warn、error、fatal 的診斷；不是診斷的字句（stdout 的正常輸出、詢問、用法、版本行、本機覆寫提醒、執行紀錄的一般條目）不登錄。

`bootstrap.sh` 用到的訊息在發布時由訊息表產生並內嵌進 `bootstrap.sh`。

處置與下一步：

- 處置是診斷的屬性，不是嚴重度。待處理表示這次執行沒有做完，而且 VK 已附上一條可直接執行、不需使用者代換的下一步指令；失敗不承諾可執行的修法，但可以附一般建議；warn 的列與用法錯誤留空
- 下一步指令直接寫在本文句尾，占位符都由 VK 換成實際的值；待處理的本文必須以這條指令結尾，各語言的結尾指令逐字相同；做不到的診斷標失敗
  - <mark style="background-color:#c8f0c8">待確認 (Y1)：[add](../../../GLOSSARY.md#vk-recipe-與用途) 要附加內容到既有、未[納管](../../../GLOSSARY.md#初始檔與合併)的檔時，[-y](../../../GLOSSARY.md#執行與結果) 不代答這些詢問。有終端時仍詢問，答否是正常取消；不能互動時，`VK0002` 給的下一步加上 `-y` 後仍會停下，草稿以 `VK0084` 表示這種情況，其處置也待確認 (Y1)；在無法提供可直接執行的下一步時，應標失敗，在終端重跑僅屬一般建議。另一個待確認方案是讓 `-y` 代答這些詢問，或讓 `VK0002` 改給別的下一步；尚未選定方案</mark>
  - <mark style="background-color:#c8f0c8">待確認 (B2)：`bootstrap.sh` 起的 [install](../../../GLOSSARY.md#vk-recipe-與用途) 遇到 `VK0002` 時，`<command_with_y>` 目前是引擎重組的 `just vendor_kit install …`，不是以 `$0` 開頭的呼叫，且未保留 `-i`；要改引擎與協定，或調整訊息表的情況欄，尚待確認</mark>
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
  - 左邊六欄給程式讀，只用英文；加上目前兩組語言欄，共十欄：
    - `code`：原因代碼，依代碼升冪排列；新代碼持續遞增，大版本清理停用列後可留下缺號
    - `status`：`active` 使用中；`retired` 已停用
    - `level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)
    - `exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空
    - `disposition`：處置，`pending`（待處理）、`failed`（失敗）或留空；warn 的列與用法錯誤（`situation.en` 以 `Usage error:` 開頭的列）留空
    - `source`：發出診斷的入口，放在 `disposition` 之後、語言欄之前；值有四個：

      | 值 | 入口 |
      | --- | --- |
      | `bootstrap` | Release 附的 `bootstrap.sh` |
      | `engine` | 引擎 |
      | `launcher` | [薄殼](../../../GLOSSARY.md#vk-組件)內的啟動片段，不含 `bootstrap.sh` |
      | `test` | test recipe 帶路徑時的測試流程，與 `engine` 並列 |

      列出所有會印出這條診斷的入口；可有多個值，以單一空白分隔，依 `bootstrap`、`engine`、`launcher`、`test` 的順序排列；`retired` 列留空
  - 右邊照語言分組，每組是 `situation.<lang>`、`message.<lang>`，目前有 `zh-TW`、`en`；之後加語言就在最右邊接一組：
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

#### VK0001

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">update、upgrade、add 需要列版本，registry 要求讀取權限，而這次沒有帶 --registry-token-file；&lt;cmd&gt; 在 add 時印 add，update、upgrade 時印 upgrade；&lt;path&gt; 與 &lt;tag&gt; 原樣印出，由使用者換成 token 檔路徑與要安裝的版本 tag</mark> → <mark style="background-color:#c8f0c8">update、upgrade、add 需要列版本，registry 要求讀取權限，而這次沒有帶 --registry-token-file；&lt;cmd&gt; 在 add 時印 add，update、upgrade 時印 upgrade；&lt;path&gt; 與 &lt;tag&gt; 原樣印出，由使用者換成 token 檔路徑與要安裝的版本 tag；不含 upgrade --engine：引擎升版不收 token 檔，registry 要求認證時報 VK0055</mark>
- `message.zh-TW`：無法列出 &lt;repo&gt; 的版本：需要 registry 讀取權限；拉取時仍使用主機的 Docker 認證。請加上 --registry-token-file &lt;path&gt; 重新執行，或直接指定版本：just vendor_kit &lt;cmd&gt; &lt;repo&gt;@&lt;tag&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">update, upgrade, or add needs to list versions, the registry requires read access, and this invocation did not supply --registry-token-file; &lt;cmd&gt; prints add for add and upgrade for update or upgrade; &lt;path&gt; and &lt;tag&gt; are printed literally for the user to replace with the token file path and the version tag to install</mark> → <mark style="background-color:#c8f0c8">update, upgrade, or add needs to list versions, the registry requires read access, and this invocation did not supply --registry-token-file; &lt;cmd&gt; prints add for add and upgrade for update or upgrade; &lt;path&gt; and &lt;tag&gt; are printed literally for the user to replace with the token file path and the version tag to install; upgrade --engine is excluded: engine upgrades do not accept a token file and report VK0055 when the registry requires authentication</mark>
- `message.en`：Cannot list versions for &lt;repo&gt;: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file &lt;path&gt; and rerun, or specify a version directly: just vendor_kit &lt;cmd&gt; &lt;repo&gt;@&lt;tag&gt;

#### VK0002

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：bootstrap engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">操作需要詢問，但沒帶 -y 又不能互動（stdin 或 stderr 不是終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後；bootstrap.sh 首次導入時，&lt;command_with_y&gt; 以這次呼叫的腳本路徑 ($0) 開頭，後接這次的參數，依同一規則重組</mark> → <mark style="background-color:#c8f0c8">操作需要詢問，但沒帶 -y 又不能互動（stdin 或 stderr 不是終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後；bootstrap.sh 首次導入時，&lt;command_with_y&gt; 以這次呼叫的腳本路徑 ($0) 開頭，後接這次的參數，依同一規則重組；目前 bootstrap.sh 起的 install 由引擎重組 just vendor_kit install 指令、未保留 -i；待確認 (B2)</mark>
- `message.zh-TW`：需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">An operation requires a prompt, but -y was not given and interaction is impossible (stdin or stderr is not a terminal, or end of input was read); &lt;command_with_y&gt; is rebuilt from this run's arguments one by one, each quoted by POSIX shell rules, with -y inserted before a standalone --, or appended at the end if there is no --; during initial import by bootstrap.sh, &lt;command_with_y&gt; starts with the script path ($0) of this invocation, followed by this run's arguments, rebuilt by the same rules</mark> → <mark style="background-color:#c8f0c8">An operation requires a prompt, but -y was not given and interaction is impossible (stdin or stderr is not a terminal, or end of input was read); &lt;command_with_y&gt; is rebuilt from this run's arguments one by one, each quoted by POSIX shell rules, with -y inserted before a standalone --, or appended at the end if there is no --; during initial import by bootstrap.sh, &lt;command_with_y&gt; starts with the script path ($0) of this invocation, followed by this run's arguments, rebuilt by the same rules; currently, install started by bootstrap.sh uses a just vendor_kit install command rebuilt by the engine, and does not preserve -i; Pending confirmation (B2)</mark>
- `message.en`：Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;

#### VK0005

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：bootstrap
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">bootstrap.sh 首次導入時發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark> → <mark style="background-color:#c8f0c8">bootstrap.sh 首次導入時發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具；目前實作用 just 官方 install.sh（需要 curl），與此不符；待確認 (J1)</mark>
- `message.zh-TW`：需要 just 1.33.0 或更新版本；目前版本為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">During initial import, bootstrap.sh finds the host's just is older than 1.33.0; &lt;install_command&gt; does not overwrite the host's existing just and does not require the host to install any other tool</mark> → <mark style="background-color:#c8f0c8">During initial import, bootstrap.sh finds the host's just is older than 1.33.0; &lt;install_command&gt; does not overwrite the host's existing just and does not require the host to install any other tool; the current implementation uses the official just install.sh (requiring curl), which does not meet this requirement; Pending confirmation (J1)</mark>
- `message.en`：just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;

#### VK0009

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：pending
- `source`：<mark style="background-color:#f8c8c8">launcher</mark> → <mark style="background-color:#c8f0c8">engine launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe</mark> → <mark style="background-color:#c8f0c8">舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe；離線判定時，&lt;vY&gt; 取 pinned 引用的 tag，沒有 tag 時印 unknown；本機覆寫的引擎不使用此碼，改報 VK0086</mark>
- `message.zh-TW`：薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 一般 recipe 所需的版本。請先執行：just vendor_kit upgrade --engine
- `situation.en`：<mark style="background-color:#f8c8c8">An old shell meets an engine with a newer major version X and runs a recipe outside the rescue path</mark> → <mark style="background-color:#c8f0c8">An old shell meets an engine with a newer major version X and runs a recipe outside the rescue path; for offline checks, &lt;vY&gt; comes from the tag of the pinned reference, or prints unknown if there is no tag; locally overridden engines use VK0086 instead</mark>
- `message.en`：Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine

#### VK0011

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：bootstrap launcher
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">docker --version 的輸出含 podman</mark> → <mark style="background-color:#c8f0c8">docker --version 的輸出含 podman；待確認 (N6b)</mark>
- `message.zh-TW`：偵測到 Podman (docker --version)。vendor_kit 只支援 Docker。請改用 Docker（rootful 或 rootless）後重試。
- `situation.en`：<mark style="background-color:#f8c8c8">The output of docker --version contains podman</mark> → <mark style="background-color:#c8f0c8">The output of docker --version contains podman; Pending confirmation (N6b)</mark>
- `message.en`：Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.

#### VK0013

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">metadata 缺失或損壞，無法可靠還原</mark> → <mark style="background-color:#c8f0c8">metadata 缺失或損壞，無法可靠還原；remove、uninstall 收回時遇到自相矛盾的逐檔紀錄（非 appended 卻有 lines，或 appended 卻沒有 lines）也報此碼；每份有矛盾的紀錄檔各報一則，&lt;file&gt; 是該紀錄檔，在詢問與寫入之前停下</mark>
- `message.zh-TW`：無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。紀錄不可用時，vendor_kit 不做推測；&lt;file&gt; 所屬工具的檔都未修改。請保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;。metadata 若曾 commit 進 Git，從 Git 還原後重試；否則到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，並附上這兩個檔。
- `situation.en`：<mark style="background-color:#f8c8c8">metadata is missing or corrupt and cannot be restored reliably</mark> → <mark style="background-color:#c8f0c8">metadata is missing or corrupt and cannot be restored reliably; remove or uninstall also reports this code when reclamation finds contradictory per-file records (lines on a non-appended record, or no lines on an appended record); one diagnostic is emitted for each contradictory record file, &lt;file&gt; is that record file, and processing stops before prompts or writes</mark>
- `message.en`：Cannot process &lt;file&gt;: metadata is missing or corrupt and cannot be restored reliably. vendor_kit does not guess when records are unavailable; no files of the tool that &lt;file&gt; belongs to were modified. Preserve &lt;file&gt; and run log &lt;path&gt;. If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.

#### VK0015

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">sync 發現已鎖定工具的 cache/ 檔案集合或逐檔指紋不符，已依版本鎖定行重新取件；不在版本鎖定行的工具目錄不屬於這個情況</mark> → <mark style="background-color:#c8f0c8">sync 發現已鎖定工具的 cache/ 檔案集合或逐檔指紋不符，已依版本鎖定行重新取件；不在版本鎖定行的工具目錄不屬於這個情況；cache/&lt;repo&gt;/ 本身或底下的 symlink、socket、FIFO 等非一般檔視為多出的檔，重新取件</mark>
- `message.zh-TW`：&lt;repo&gt; 在 cache/ 的檔案集合或逐檔指紋不符；已依版本鎖定行重新取件。
- `situation.en`：<mark style="background-color:#f8c8c8">sync finds the file set or per-file digests in cache/ for a locked tool do not match, and has refetched according to the lock version line; tool directories not in the lock version lines are not covered by this case</mark> → <mark style="background-color:#c8f0c8">sync finds the file set or per-file digests in cache/ for a locked tool do not match, and has refetched according to the lock version line; tool directories not in the lock version lines are not covered by this case; a symlink, socket, FIFO, or other non-regular entry at cache/&lt;repo&gt;/ itself or below it is treated as an extra file and triggers refetching</mark>
- `message.en`：The file set or per-file digests in cache/ for &lt;repo&gt; did not match; refetched according to the lock version line.

#### VK0021

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">基準版合併留下合併衝突</mark> → <mark style="background-color:#c8f0c8">基準版合併留下合併衝突；結果是 TOML 或 just 檔而解析不過時不報此碼（含 config.toml），見 VK0087</mark>
- `message.zh-TW`：&lt;file&gt; 含有合併衝突。請檢視並解決：git status
- `situation.en`：<mark style="background-color:#f8c8c8">A baseline merge leaves merge conflicts</mark> → <mark style="background-color:#c8f0c8">A baseline merge leaves merge conflicts; this code is not reported when the result is a TOML or just file that fails parsing (including config.toml); see VK0087</mark>
- `message.en`：&lt;file&gt; contains merge conflicts. Review and resolve them: git status

#### VK0023

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：bootstrap engine test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">upgrade --engine 換上新引擎後原指令尚未做完，或唯讀 recipe 讀到引擎升級未完成的進度檔；bootstrap.sh 只檢查或 --repair 時讀到記錄引擎升級未完成的進度檔，也報此碼，不比對或重產薄殼；&lt;original_command&gt; 由 VK 依進度檔填成原本的完整 upgrade 指令，保留原 tag 與 -y，不需使用者代換</mark> → <mark style="background-color:#c8f0c8">upgrade --engine 換上新引擎後原指令尚未做完，或唯讀 recipe 讀到引擎升級未完成的進度檔；bootstrap.sh 只檢查或 --repair 時讀到記錄引擎升級未完成的進度檔，也報此碼，不比對或重產薄殼；&lt;original_command&gt; 由 VK 依進度檔填成原本的完整 upgrade 指令，保留原 tag 與 -y，不需使用者代換；&lt;vY&gt; 取自進度檔 [upgrade] image 的 tag，update、sync、test、bootstrap.sh 只檢查與 --repair 都相同；第一段中斷後重做完成也報此碼</mark>
- `message.zh-TW`：已安裝引擎 &lt;vY&gt;。請再執行一次：&lt;original_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">After upgrade --engine installs the new engine, the original command has not yet completed, or a read-only recipe reads a progress file for an incomplete engine upgrade; during a bootstrap.sh check-only run or --repair, reading a progress file that records an incomplete engine upgrade also reports this code, with no shell comparison or regeneration; &lt;original_command&gt; is filled in by VK from the progress file as the original full upgrade command, keeping the original tag and -y, with no substitution needed by the user</mark> → <mark style="background-color:#c8f0c8">After upgrade --engine installs the new engine, the original command has not yet completed, or a read-only recipe reads a progress file for an incomplete engine upgrade; during a bootstrap.sh check-only run or --repair, reading a progress file that records an incomplete engine upgrade also reports this code, with no shell comparison or regeneration; &lt;original_command&gt; is filled in by VK from the progress file as the original full upgrade command, keeping the original tag and -y, with no substitution needed by the user; &lt;vY&gt; comes from the tag of [upgrade] image in the progress file, identically for update, sync, test, bootstrap.sh check-only runs and --repair; this code is also reported after completing a retry of an interrupted first stage</mark>
- `message.en`：Engine &lt;vY&gt; is now installed. Run again: &lt;original_command&gt;

#### VK0025

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：bootstrap engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">用法錯誤：VK recipe 或 bootstrap.sh 缺少必要參數（含 bootstrap.sh 的 -i／--image 沒帶 image）</mark> → <mark style="background-color:#c8f0c8">用法錯誤：VK recipe 或 bootstrap.sh 缺少必要參數（含 bootstrap.sh 的 -i／--image 沒帶 image）；add 沒有版本鎖定行且沒給 --image-path 時也報此碼，&lt;argument&gt; 印 --image-path；待確認 (N2b)</mark>
- `message.zh-TW`：缺少必要參數：&lt;argument&gt;。
- `situation.en`：<mark style="background-color:#f8c8c8">Usage error: a VK recipe or bootstrap.sh is missing a required argument (including bootstrap.sh -i/--image given without an image)</mark> → <mark style="background-color:#c8f0c8">Usage error: a VK recipe or bootstrap.sh is missing a required argument (including bootstrap.sh -i/--image given without an image); When --image-path is absent and there is no lock version line, add also reports this code; &lt;argument&gt; prints --image-path; Pending confirmation (N2b)</mark>
- `message.en`：Required argument is missing: &lt;argument&gt;.

#### VK0026

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：bootstrap engine test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">用法錯誤：VK recipe 或 bootstrap.sh 帶了不認得的選項或多出的參數；bootstrap.sh 帶 --repair -y，或在既有安裝目錄帶 -y／--yes（排除 VK0037 所述、依執行紀錄判定的未完成首次導入），或 -h／--help 與其他參數並用；&lt;value&gt; 印第一個不認得或不允許的參數；-h／--help 與其他參數並用時，印第一個不是 -h／--help 的參數，若全部都是 -h／--help，則印第二個參數；VK recipe 的 -h／--help 與 --engine 以外的參數並用時，&lt;value&gt; 印第一個不是 -h／--help 或 --engine 的參數；包含 test 一次給兩個以上 path，或 path 與 test dist 混用；給兩個以上 path 時，&lt;value&gt; 印第二個 path（第一個多出的參數）；path 與 test dist 混用時，&lt;value&gt; 印所給的 path；包含 --registry-token-file 的值是單獨的 -（VK 不從 stdin 讀），此時 &lt;value&gt; 印 -；在 stderr 附上用法</mark> → <mark style="background-color:#c8f0c8">用法錯誤：VK recipe 或 bootstrap.sh 帶了不認得的選項或多出的參數；bootstrap.sh 帶 --repair -y，或在既有安裝目錄帶 -y／--yes（排除 VK0037 所述、依執行紀錄判定的未完成首次導入），或 -h／--help 與其他參數並用；&lt;value&gt; 印第一個不認得或不允許的參數；-h／--help 與其他參數並用時，印第一個不是 -h／--help 的參數，若全部都是 -h／--help，則印第二個參數；VK recipe 的 -h／--help 與 --engine 以外的參數並用時，&lt;value&gt; 印第一個不是 -h／--help 或 --engine 的參數；包含 test 一次給兩個以上 path，或 path 與 test dist 混用；給兩個以上 path 時，&lt;value&gt; 印第二個 path（第一個多出的參數）；path 與 test dist 混用時，&lt;value&gt; 印所給的 path；包含 --registry-token-file 的值是單獨的 -（VK 不從 stdin 讀），此時 &lt;value&gt; 印 -；在 stderr 附上用法；dev、undev、upgrade 的 &lt;repo&gt; 不是合法的 just 名稱時，&lt;value&gt; 印整個參數（含 @&lt;tag&gt;），先於 VK0027 判定；這一版 add、remove、update 不檢查工具名；待確認 (D17)；--image-path 的值不合或與 -i 並用；-y 給了不接受它的指令；--dry-run 給了不接受它的指令、給兩次、帶值或與 -h／--help 並用；待確認 (D1)</mark>
- `message.zh-TW`：不認得、多出或此處不允許的參數：&lt;value&gt;。
- `situation.en`：<mark style="background-color:#f8c8c8">Usage error: a VK recipe or bootstrap.sh received an unknown option or an extra argument; bootstrap.sh given --repair -y, or -y/--yes in an existing install directory (excluding the incomplete initial import determined from the run log as described in VK0037), or -h/--help combined with other arguments; &lt;value&gt; prints the first unknown or disallowed argument; when -h/--help is combined with other arguments, it prints the first argument that is not -h/--help, or the second argument if all are -h/--help; when a VK recipe's -h/--help is combined with arguments other than --engine, &lt;value&gt; prints the first argument that is neither -h/--help nor --engine; this includes test given more than one path, or a path combined with test dist; for multiple paths, &lt;value&gt; prints the second path (the first extra argument); for a path combined with test dist, &lt;value&gt; prints the given path; this includes a --registry-token-file value that is a lone - (VK does not read stdin), where &lt;value&gt; prints -; usage is appended to stderr</mark> → <mark style="background-color:#c8f0c8">Usage error: a VK recipe or bootstrap.sh received an unknown option or an extra argument; bootstrap.sh given --repair -y, or -y/--yes in an existing install directory (excluding the incomplete initial import determined from the run log as described in VK0037), or -h/--help combined with other arguments; &lt;value&gt; prints the first unknown or disallowed argument; when -h/--help is combined with other arguments, it prints the first argument that is not -h/--help, or the second argument if all are -h/--help; when a VK recipe's -h/--help is combined with arguments other than --engine, &lt;value&gt; prints the first argument that is neither -h/--help nor --engine; this includes test given more than one path, or a path combined with test dist; for multiple paths, &lt;value&gt; prints the second path (the first extra argument); for a path combined with test dist, &lt;value&gt; prints the given path; this includes a --registry-token-file value that is a lone - (VK does not read stdin), where &lt;value&gt; prints -; usage is appended to stderr; an invalid just name for &lt;repo&gt; in dev, undev, or upgrade prints the entire argument (including @&lt;tag&gt;) as &lt;value&gt; and is checked before VK0027; this version does not check tool names in add, remove, or update; Pending confirmation (D17); an invalid --image-path value or --image-path combined with -i; -y given to a command that does not accept it; --dry-run given to a command that does not accept it, repeated, given a value, or combined with -h/--help; Pending confirmation (D1)</mark>
- `message.en`：Unknown, extra, or disallowed argument: &lt;value&gt;.

#### VK0030

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">add 時 &lt;ns&gt; 撞名</mark> → <mark style="background-color:#c8f0c8">add 的 &lt;ns&gt; 撞名；dev 的本機開發來源交付保留名或其他工具的 &lt;ns&gt;；upgrade 新版撞名或覆寫來源交付 vendor_kit；sync 的本機開發來源或取到的內容交付 vendor_kit，或兩個工具交付同一個 &lt;ns&gt;；sync 依工具名排序，&lt;repo&gt; 是後者、&lt;owner&gt; 是前者，全部列完才停</mark>
- `message.zh-TW`：<mark style="background-color:#f8c8c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark> → <mark style="background-color:#c8f0c8">&lt;repo&gt; 的命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">add finds a name collision on &lt;ns&gt;</mark> → <mark style="background-color:#c8f0c8">add encounters a namespace collision on &lt;ns&gt;; a local source for dev delivers a reserved name or another tool's &lt;ns&gt;; a new version for upgrade collides or an override source delivers vendor_kit; a local source or fetched content for sync delivers vendor_kit, or two tools deliver the same &lt;ns&gt;; sync sorts tools by name, with &lt;repo&gt; the later tool and &lt;owner&gt; the earlier tool, and lists all collisions before stopping</mark>
- `message.en`：<mark style="background-color:#f8c8c8">Cannot add &lt;repo&gt;: namespace &lt;ns&gt; is already used by &lt;owner&gt;.</mark> → <mark style="background-color:#c8f0c8">Namespace &lt;ns&gt; for &lt;repo&gt; is already used by &lt;owner&gt;.</mark>

#### VK0031

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：bootstrap engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">離線導入的本機 image 或 image tar 缺少必要的 digest 資訊；或 bootstrap.sh 在既有安裝目錄帶 -i／--image，所提供的本機 image 或 image tar 缺少必要的 digest 資訊，或 digest 與引擎版本鎖定行不符；只檢查與 --repair 都適用；&lt;reason&gt; 依情況填為 required digest information is missing 或 the digest does not match the engine lock version line</mark> → <mark style="background-color:#c8f0c8">離線導入的本機 image 或 image tar 缺少必要的 digest 資訊；或 bootstrap.sh 在既有安裝目錄帶 -i／--image，所提供的本機 image 或 image tar 缺少必要的 digest 資訊，或 digest 與引擎版本鎖定行不符；只檢查與 --repair 都適用；&lt;reason&gt; 依情況填為 required digest information is missing 或 the digest does not match the engine lock version line；add、upgrade 使用的本機 image 缺少這個路徑的 RepoDigest 時，&lt;reason&gt; 填 required digest information is missing；add 以 -i &lt;tar&gt; 導入時，旁檔取不到或格式不合也報此碼</mark>
- `message.zh-TW`：無法使用 image &lt;image&gt;：&lt;reason&gt;。未使用所提供的 image。
- `situation.en`：<mark style="background-color:#f8c8c8">The local image or image tar for offline import lacks required digest information; or bootstrap.sh is given -i/--image in an existing install directory and the supplied local image or image tar lacks required digest information, or its digest does not match the engine lock version line; applies to both check-only runs and --repair; &lt;reason&gt; is filled as required digest information is missing or the digest does not match the engine lock version line, as applicable</mark> → <mark style="background-color:#c8f0c8">The local image or image tar for offline import lacks required digest information; or bootstrap.sh is given -i/--image in an existing install directory and the supplied local image or image tar lacks required digest information, or its digest does not match the engine lock version line; applies to both check-only runs and --repair; &lt;reason&gt; is filled as required digest information is missing or the digest does not match the engine lock version line, as applicable; for add or upgrade, a local image missing a RepoDigest for this image path fills &lt;reason&gt; as required digest information is missing; For offline import with -i &lt;tar&gt;, add also reports this code when the companion digest file is unavailable or malformed</mark>
- `message.en`：Cannot use image &lt;image&gt;: &lt;reason&gt;. The supplied image was not used.

#### VK0034

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：bootstrap
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">bootstrap.sh 首次導入時找不到主機的 just；&lt;install_command&gt; 由 VK 填好，可直接執行、不需使用者代換，不要求主機另裝其他工具</mark> → <mark style="background-color:#c8f0c8">bootstrap.sh 首次導入時找不到主機的 just；&lt;install_command&gt; 由 VK 填好，可直接執行、不需使用者代換，不要求主機另裝其他工具；目前實作用 just 官方 install.sh（需要 curl），與此不符；待確認 (J1)</mark>
- `message.zh-TW`：主機上找不到 just。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">During initial import, bootstrap.sh cannot find just on the host; &lt;install_command&gt; is filled in by VK, runs directly with no substitution needed by the user, and does not require the host to install any other tool</mark> → <mark style="background-color:#c8f0c8">During initial import, bootstrap.sh cannot find just on the host; &lt;install_command&gt; is filled in by VK, runs directly with no substitution needed by the user, and does not require the host to install any other tool; the current implementation uses the official just install.sh (requiring curl), which does not meet this requirement; Pending confirmation (J1)</mark>
- `message.en`：just was not found on the host. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;

#### VK0036

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：bootstrap launcher
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">啟動器取不到要用的引擎 image（首次導入含未完成的首次導入時用內嵌版本；已有版本鎖定行時用它指定的版本）；不改用其他版本</mark> → <mark style="background-color:#c8f0c8">啟動器取不到要用的引擎 image（首次導入含未完成的首次導入時用內嵌版本；已有版本鎖定行時用它指定的版本）；不改用其他版本；啟動器套用引擎本機覆寫時，本機沒有指定的 image 也報此碼，不 pull</mark>
- `message.zh-TW`：無法取得引擎 image &lt;image&gt;：&lt;reason&gt;。未改用其他引擎版本。
- `situation.en`：<mark style="background-color:#f8c8c8">The launcher cannot obtain the engine image it needs (the embedded version for initial import, including an incomplete initial import; the version specified by the lock version line when one exists); no other version is used instead</mark> → <mark style="background-color:#c8f0c8">The launcher cannot obtain the engine image it needs (the embedded version for initial import, including an incomplete initial import; the version specified by the lock version line when one exists); no other version is used instead; when applying an engine local override, the launcher also reports this code if the specified image is not present locally, without pulling it</mark>
- `message.en`：Cannot obtain engine image &lt;image&gt;: &lt;reason&gt;. No alternative engine version was used.

#### VK0037

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：bootstrap
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">bootstrap.sh 發現目前目錄有 .vendor_kit/，但讀不到恰好一行有效的引擎版本鎖定行；停下，不改走首次導入；僅首次導入的呼叫（不帶參數、-y、-i，含對應長選項及其合法組合）排除可依執行紀錄唯一判定的未完成首次導入：最近一筆執行紀錄是首次導入，且 (a) 停在 VK0002、除執行紀錄外未修改任何檔，或 (b) 在建執行紀錄之後、寫入引擎版本鎖定行之前結束（不論是否已寫入其他檔）；這些狀態允許帶 -y 重跑首次導入，判定不靠檔案在不在，無法唯一判定時仍停下；--repair 在這些狀態下仍報 VK0037</mark> → <mark style="background-color:#c8f0c8">bootstrap.sh 發現目前目錄有 .vendor_kit/，但讀不到恰好一行有效的引擎版本鎖定行；停下，不改走首次導入；僅首次導入的呼叫（不帶參數、-y、-i，含對應長選項及其合法組合）排除可依執行紀錄唯一判定的未完成首次導入：最近一筆執行紀錄是首次導入，且 (a) 停在 VK0002、除執行紀錄外未修改任何檔，或 (b) 在建執行紀錄之後、寫入引擎版本鎖定行之前結束（不論是否已寫入其他檔）；這些狀態允許帶 -y 重跑首次導入，判定不靠檔案在不在，無法唯一判定時仍停下；--repair 在這些狀態下仍報 VK0037；偵測到 uninstall 未完成時，不走首次導入例外，改報 VK0083 並給完成模式指令；待確認 (N8b)</mark>
- `message.zh-TW`：無法從 .vendor_kit/version.toml 讀取恰好一行有效的引擎版本鎖定行。未嘗試首次導入。
- `situation.en`：<mark style="background-color:#f8c8c8">bootstrap.sh finds .vendor_kit/ in the current directory but cannot read exactly one valid engine lock version line; it stops and does not fall back to initial import; only for initial-import invocations (no arguments, -y, -i, including the corresponding long options and their valid combinations), an incomplete initial import that can be uniquely determined from the run log is excluded: the most recent run log is an initial import, and either (a) it stopped at VK0002 with no files modified except the run log, or (b) it ended after the run log was created and before the engine lock version line was written (whether or not other files were written); these states allow rerunning initial import with -y, the determination does not rely on whether files exist, and it still stops when the state cannot be uniquely determined; --repair still reports VK0037 in these states</mark> → <mark style="background-color:#c8f0c8">bootstrap.sh finds .vendor_kit/ in the current directory but cannot read exactly one valid engine lock version line; it stops and does not fall back to initial import; only for initial-import invocations (no arguments, -y, -i, including the corresponding long options and their valid combinations), an incomplete initial import that can be uniquely determined from the run log is excluded: the most recent run log is an initial import, and either (a) it stopped at VK0002 with no files modified except the run log, or (b) it ended after the run log was created and before the engine lock version line was written (whether or not other files were written); these states allow rerunning initial import with -y, the determination does not rely on whether files exist, and it still stops when the state cannot be uniquely determined; --repair still reports VK0037 in these states; an incomplete uninstall is excluded from the initial-import exception and instead reports VK0083 with a completion-mode command; Pending confirmation (N8b)</mark>
- `message.en`：Cannot read exactly one valid engine lock version line from .vendor_kit/version.toml. Initial import was not attempted.

#### VK0043

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">sync 下載的工具 image 內容不符版本鎖定行的 digest；不把這份內容當成已驗證的工具內容，不報 VK0015</mark> → <mark style="background-color:#c8f0c8">sync 下載的工具 image 內容不符版本鎖定行的 digest；不把這份內容當成已驗證的工具內容，不報 VK0015；add、upgrade 下載的內容不符版本鎖定行的 digest 也屬此情況</mark>
- `message.zh-TW`：&lt;repo&gt; 下載的 image &lt;image&gt; 與鎖定的 digest &lt;digest&gt; 不符。同步未完成。
- `situation.en`：<mark style="background-color:#f8c8c8">The tool image content downloaded by sync does not match the digest in the lock version line; this content is not treated as verified tool content, and VK0015 is not reported</mark> → <mark style="background-color:#c8f0c8">The tool image content downloaded by sync does not match the digest in the lock version line; this content is not treated as verified tool content, and VK0015 is not reported; content downloaded by add or upgrade that does not match the digest in the lock version line is also covered</mark>
- `message.en`：Downloaded image &lt;image&gt; for &lt;repo&gt; does not match locked digest &lt;digest&gt;. Synchronization did not complete.

#### VK0046

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">remove、undev 或 update &lt;repo&gt; 指定的工具不在版本鎖定行；先辨識未完成進度，再判斷對象不存在</mark> → <mark style="background-color:#c8f0c8">remove、dev、undev、upgrade 或 update &lt;repo&gt; 指定的工具不在版本鎖定行；先辨識未完成進度，再判斷對象不存在</mark>
- `message.zh-TW`：版本鎖定行中沒有工具 &lt;repo&gt;。要求的操作未完成。
- `situation.en`：<mark style="background-color:#f8c8c8">The tool specified to remove, undev, or update &lt;repo&gt; is not in the lock version lines; incomplete progress is identified first, before determining that the target does not exist</mark> → <mark style="background-color:#c8f0c8">The tool specified to remove, dev, undev, upgrade, or update &lt;repo&gt; is not in the lock version lines; incomplete progress is identified first, before determining that the target does not exist</mark>
- `message.en`：Tool &lt;repo&gt; is not in the lock version lines. The requested operation did not complete.

#### VK0047

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">test 因 cache/ 或 gen/ 缺件而無法完成檢查；不取件、不準備或修復 cache/、gen/、進度檔，執行紀錄照寫；CI 全新 checkout 尚未取件時是否算缺件，待確認（見 #47、#124）</mark> → <mark style="background-color:#c8f0c8">test 因 cache/ 或 gen/ 缺件或不一致而無法完成檢查；&lt;files&gt; 逐檔標出缺少、多出、內容不同、印記損壞或印記版本不同；全新 checkout 尚未取件也算缺件；不取件、不準備或修復 cache/、gen/、進度檔，執行紀錄照寫</mark>
- `message.zh-TW`：無法完成 &lt;target&gt; 的檢查：缺少必要的本機檔：&lt;files&gt;。請執行：just vendor_kit sync
- `situation.en`：<mark style="background-color:#f8c8c8">test cannot complete its checks because files in cache/ or gen/ are missing; it does not fetch, and does not prepare or repair cache/, gen/, or progress files; the run log is still written; whether a fresh CI checkout that has not yet fetched counts as missing files is pending confirmation (see #47, #124)</mark> → <mark style="background-color:#c8f0c8">test cannot complete its checks because files in cache/ or gen/ are missing or inconsistent; &lt;files&gt; identifies missing files, extra files, content differences, corrupt stamps, or stamp version mismatches individually; a fresh checkout that has not fetched also counts as missing files; it does not fetch or prepare or repair cache/, gen/, or progress files, but still writes the run log</mark>
- `message.en`：Cannot complete checks for &lt;target&gt;: required local files are missing: &lt;files&gt;. Run: just vendor_kit sync

#### VK0048

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">test dist 在沒有工具交付內容的 repo 執行</mark> → <mark style="background-color:#c8f0c8">test dist 在沒有工具交付內容的 repo 執行；dist/ 不在或底下沒有任何檔</mark>
- `message.zh-TW`：無法檢查工具交付內容：&lt;path&gt; 沒有交付內容。
- `situation.en`：<mark style="background-color:#f8c8c8">test dist runs in a repo with no tool delivery content</mark> → <mark style="background-color:#c8f0c8">test dist runs in a repo with no tool delivery content; dist/ does not exist or contains no files</mark>
- `message.en`：Cannot check tool delivery content: &lt;path&gt; contains no delivery content.

#### VK0052

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">需要讀取本機覆寫來源的動作發現來源失效；只擋需要讀取它的動作；undev 不讀來源即可解除，test 仍報 VK0032，bootstrap.sh 忽略覆寫，update 照版本鎖定行查版本；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark> → <mark style="background-color:#c8f0c8">需要讀取本機覆寫來源的動作發現來源失效；只擋需要讀取它的動作；undev 不讀來源即可解除，test 仍報 VK0032，bootstrap.sh 忽略覆寫，update 照版本鎖定行查版本；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine；包括 add、remove 重產入口檔時讀取其他工具的覆寫來源；sync、upgrade 讀安裝目錄外的覆寫時，啟動器複製不了、內容格式不符或路徑形式不接受；救援路徑上無法送出 stage-dir 也報此碼</mark>
- `message.zh-TW`：無法讀取 &lt;target&gt; 的本機覆寫來源 &lt;source&gt;：&lt;reason&gt;。請執行：&lt;undev_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">An action that needs to read a local override source finds the source invalid; only actions that need to read it are blocked; undev can remove the override without reading the source, test still reports VK0032, bootstrap.sh ignores the override, and update checks versions according to the lock version line; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target</mark> → <mark style="background-color:#c8f0c8">An action that needs to read a local override source finds the source invalid; only actions that need to read it are blocked; undev can remove the override without reading the source, test still reports VK0032, bootstrap.sh ignores the override, and update checks versions according to the lock version line; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target; this includes add or remove reading other tools' override sources to regenerate entry files; for sync or upgrade reading overrides outside the install directory, the launcher cannot copy the source, its content format is invalid, or the path form is unsupported; failure to send stage-dir on a rescue path also reports this code</mark>
- `message.en`：Cannot read the local override source &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. Run: &lt;undev_command&gt;

#### VK0053

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：engine test
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">undev 解除覆寫後同步失敗，或唯讀 recipe 偵測到未完成的 undev 進度檔；sync 不代替 undev 清掉進度檔；&lt;undev_command&gt; 依進度檔填成原本的 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark> → <mark style="background-color:#c8f0c8">undev 解除覆寫後同步失敗，或唯讀 recipe 偵測到未完成的 undev 進度檔；sync 不代替 undev 清掉進度檔；&lt;undev_command&gt; 依進度檔填成原本的 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine；dev、undev 遇到對象不同的 undev 殘留也報此碼；undev 取件因 docker 動作失敗或 digest 不符而失敗時，覆寫照留</mark>
- `message.zh-TW`：&lt;target&gt; 的 undev 操作未完成。請再執行一次：&lt;undev_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">Synchronization fails after undev removes an override, or a read-only recipe detects an incomplete undev progress file; sync does not clear the progress file on undev's behalf; &lt;undev_command&gt; is filled from the progress file as the original just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine</mark> → <mark style="background-color:#c8f0c8">Synchronization fails after undev removes an override, or a read-only recipe detects an incomplete undev progress file; sync does not clear the progress file on undev's behalf; &lt;undev_command&gt; is filled from the progress file as the original just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine; dev or undev also reports this code when it encounters incomplete undev progress for a different target; if fetching for undev fails because of a Docker operation failure or a digest mismatch, the override is retained</mark>
- `message.en`：The undev operation for &lt;target&gt; is incomplete. Run again: &lt;undev_command&gt;

#### VK0054

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#f8c8c8">engine test</mark> → <mark style="background-color:#c8f0c8">bootstrap engine test</mark>
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">唯讀 recipe 偵測到未完成導入、工具 upgrade、引擎 upgrade、undev 這四種以外的可寫 recipe（如 remove、install、uninstall、dev）未完成的進度檔；不恢復、不刪進度檔；bootstrap.sh 仍依 VK0037 與 VK0023 的既有判定，不擴大首次導入例外；&lt;original_command&gt; 由 VK 依進度檔重組原本完整指令，保留參數並依 POSIX shell 規則加引號</mark> → <mark style="background-color:#c8f0c8">唯讀 recipe 偵測到未完成導入、工具 upgrade、引擎 upgrade、undev 這四種以外的可寫 recipe（如 remove、install、uninstall、dev）未完成的進度檔，或 dev、undev 遇到對象不同的 dev 或其他可寫 recipe 殘留；待確認 (D17)；不恢復、不刪進度檔；bootstrap.sh 偵測引擎升級 (VK0023) 與 uninstall (VK0083) 以外的其他未完成操作時也報此碼；首次導入例外仍依 VK0037 判定；&lt;original_command&gt; 由 VK 依進度檔重組原本完整指令，保留參數並依 POSIX shell 規則加引號；待確認 (N8b)</mark>
- `message.zh-TW`：&lt;install_dir&gt; 中的 &lt;operation&gt; 操作未完成。請再執行一次：&lt;original_command&gt;
- `situation.en`：<mark style="background-color:#f8c8c8">A read-only recipe detects a progress file for an incomplete writing recipe other than the four kinds (incomplete import, tool upgrade, engine upgrade, undev), such as remove, install, uninstall, or dev; it does not resume or delete the progress file; bootstrap.sh still follows the existing determinations of VK0037 and VK0023 and does not widen the initial-import exception; &lt;original_command&gt; is rebuilt by VK from the progress file as the original full command, keeping its arguments, quoted by POSIX shell rules</mark> → <mark style="background-color:#c8f0c8">A read-only recipe detects incomplete progress for a writing recipe other than incomplete import, tool upgrade, engine upgrade, or undev (such as remove, install, uninstall, or dev), or dev or undev encounters incomplete dev or other writing-recipe progress for a different target; Pending confirmation (D17); it does not resume or delete progress files; bootstrap.sh also reports this code for other incomplete operations except engine upgrades (VK0023) and uninstall (VK0083); the initial-import exception still follows VK0037; &lt;original_command&gt; is rebuilt by VK from the progress file as the original full command, preserving arguments and quoting by POSIX shell rules; Pending confirmation (N8b)</mark>
- `message.en`：Operation &lt;operation&gt; in &lt;install_dir&gt; is incomplete. Run again: &lt;original_command&gt;

#### VK0055

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">update、add、upgrade 或 sync 列 tag 或取得工具 image 時發生網路、registry 或認證錯誤（含逾時）；包括讀 --registry-token-file 指定的檔失敗（不存在、讀不到、空的），或 registry 拒絕帶入的 token；被拒後不改走匿名重試；列版本時 registry 要求讀取權限而沒有帶 --registry-token-file 仍報 VK0001；update 不以舊快取回報已是最新版，不跳出認證詢問</mark> → <mark style="background-color:#c8f0c8">update、add、upgrade 或 sync 列 tag 或取得工具 image 時發生網路、registry 或認證錯誤（含逾時）；包括讀 --registry-token-file 指定的檔失敗（不存在、讀不到、空的），或 registry 拒絕帶入的 token；被拒後不改走匿名重試；列版本時 registry 要求讀取權限而沒有帶 --registry-token-file 仍報 VK0001；update 不以舊快取回報已是最新版，不跳出認證詢問；upgrade --engine 列 tag 或取 digest 失敗（含要求認證）、update 查引擎失敗、registry 回 404 或回應不合協定也報此碼；tag 清單為空時，&lt;reason&gt; 填 the registry lists no tags；引擎升版不使用 VK0001；本機 docker 操作與外部程序失敗不屬此碼，改報 VK0077</mark>
- `message.zh-TW`：無法存取 &lt;target&gt; 的 &lt;source&gt;：&lt;reason&gt;。要求的操作未完成。
- `situation.en`：<mark style="background-color:#f8c8c8">A network, registry, or authentication error (including timeout) occurs while update, add, upgrade, or sync lists tags or obtains a tool image; this includes failure to read the file specified by --registry-token-file (missing, unreadable, or empty), or the registry rejecting the supplied token; a rejected token is not retried anonymously; listing versions when registry read access is required and --registry-token-file was not supplied still reports VK0001; update does not report up-to-date from a stale cache and does not prompt for authentication</mark> → <mark style="background-color:#c8f0c8">A network, registry, or authentication error (including timeout) occurs while update, add, upgrade, or sync lists tags or obtains a tool image; this includes failure to read the file specified by --registry-token-file (missing, unreadable, or empty), or the registry rejecting the supplied token; a rejected token is not retried anonymously; listing versions when registry read access is required and --registry-token-file was not supplied still reports VK0001; update does not report up-to-date from a stale cache and does not prompt for authentication; this also covers upgrade --engine failing to list tags or obtain a digest (including required authentication), update failing to query the engine, a registry returning 404, or a response violating the protocol; an empty tag list fills &lt;reason&gt; as the registry lists no tags; engine upgrades do not use VK0001; local Docker operations and external-process failures use VK0077 instead</mark>
- `message.en`：Cannot access &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. The requested operation did not complete.

#### VK0058

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：engine
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">update 查到 registry 有所查工具或引擎的 tag，但沒有合法的 vX.Y.Z tag；對應結果行印 latest: none</mark> → <mark style="background-color:#c8f0c8">update、add、upgrade &lt;repo&gt; 或 upgrade --engine 查到 registry 有所查工具或引擎的 tag，但沒有合法的 vX.Y.Z tag；update 時對應結果行印 latest: none</mark>
- `message.zh-TW`：無法判定 &lt;repo&gt; 的最新版本：registry 有 tag，但沒有合法的 vX.Y.Z tag。查詢未完成。
- `situation.en`：<mark style="background-color:#f8c8c8">update finds tags in the registry for the queried tool or engine, but none is a valid vX.Y.Z tag; the corresponding result line prints latest: none</mark> → <mark style="background-color:#c8f0c8">update, add, upgrade &lt;repo&gt;, or upgrade --engine finds tags in the registry for the queried tool or engine, but none is a valid vX.Y.Z tag; for update, the corresponding result line prints latest: none</mark>
- `message.en`：Cannot determine the latest version of &lt;repo&gt;: the registry has tags, but none is a valid vX.Y.Z tag. The query did not complete.

#### VK0068
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">其他已裝工具的 cache/&lt;repo&gt;/ 不在；全部工具合成一則，&lt;repos&gt; 逐一指名</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">已裝工具缺少 cache/：&lt;repos&gt;。請執行：just vendor_kit sync</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The cache/&lt;repo&gt;/ directory of another installed tool is missing; all affected tools are combined into one diagnostic, with &lt;repos&gt; naming each tool</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Installed tools are missing cache/ directories: &lt;repos&gt;. Run: just vendor_kit sync</mark>

#### VK0069
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">寫檔寫到一半失敗，&lt;file&gt; 指名未完成的檔；含 bootstrap.sh --repair 重產薄殼到一半；&lt;original_command&gt; 由 VK 重組原本完整指令，可直接重跑</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">寫入 &lt;file&gt; 未完成：&lt;reason&gt;。請再執行一次：&lt;original_command&gt;</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A write fails partway through; &lt;file&gt; names the incomplete file, including shell regeneration by bootstrap.sh --repair; VK rebuilds &lt;original_command&gt; as the original full command, ready to rerun</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Writing &lt;file&gt; did not complete: &lt;reason&gt;. Run again: &lt;original_command&gt;</mark>

#### VK0070
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine launcher test</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">版本檔不合正規形：version.toml 讀不到、引擎行數不是 1、值不是 pinned 引用、介面版列表缺少或格式錯；bootstrap.sh 讀不到恰好一行有效的引擎版本鎖定行時依 VK0037 判定，不報此碼；version.local.toml 的引擎覆寫行超過 1 行、值不是雙引號裡的 image 引用或檔讀不到；含 test 讀到不合正規形的版本檔</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">版本檔 &lt;file&gt; 不合正規形：&lt;reason&gt;。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A version file is not canonical: version.toml cannot be read, does not have exactly one engine line, its value is not a pinned reference, or the interface version list is missing or malformed; when bootstrap.sh cannot read exactly one valid engine lock version line, VK0037 determines the outcome and this code is not reported; version.local.toml has more than one engine override line, its value is not a double-quoted image reference, or the file cannot be read; this includes test reading a noncanonical version file</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Version file &lt;file&gt; is not canonical: &lt;reason&gt;. The requested operation did not complete.</mark>

#### VK0071
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine test</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">本機覆寫指到不在版本鎖定行的工具；add、remove、sync、upgrade 是否也使用此碼及能否修復仍待確認；待確認 (O1)</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">工具 &lt;repo&gt; 的本機覆寫沒有對應的版本鎖定行。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A local override refers to a tool absent from the lock version lines; use by add, remove, sync, and upgrade and whether repair is possible remain unresolved; Pending confirmation (O1)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Local override for tool &lt;repo&gt; has no corresponding lock version line. The requested operation did not complete.</mark>

#### VK0072
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine test</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">.vendor_kit/config.toml 語法錯，無法解析；無法填出 VK0059 的欄位與設定值，另報此碼；讀不到檔屬 VK0073</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法解析 .vendor_kit/config.toml：&lt;reason&gt;。請修正語法後重試。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Syntax errors prevent parsing .vendor_kit/config.toml; the field and value required by VK0059 cannot be supplied, so this code is used instead; an unreadable file uses VK0073</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot parse .vendor_kit/config.toml: &lt;reason&gt;. Fix the syntax and retry.</mark>

#### VK0073
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">VK 管理的檔不是一般檔或讀不到；含其他工具的 cache/&lt;repo&gt;/ 讀不到或損壞，每個工具各報一則，&lt;reason&gt; 附實際原因；版本檔（version.toml、version.local.toml）讀不到報 VK0070</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法讀取 &lt;file&gt;：&lt;reason&gt;。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A VK-managed file is not a regular file or cannot be read; this includes unreadable or corrupt cache/&lt;repo&gt;/ content for other tools, with one diagnostic per tool and the actual cause in &lt;reason&gt;; unreadable version files (version.toml and version.local.toml) report VK0070</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot read &lt;file&gt;: &lt;reason&gt;. The requested operation did not complete.</mark>

#### VK0074
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">sync 以外的取件發現同一個版本的內容跟既有印記不符，含 undev 重新取件</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 版本 &lt;tag&gt; 的內容與既有印記不符。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Fetching outside sync finds that content for the same version differs from the existing stamp, including refetching by undev</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Content for &lt;repo&gt; at version &lt;tag&gt; differs from the existing stamp. The requested operation did not complete.</mark>

#### VK0075
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine test</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">工具交付內容不合格式，&lt;reason&gt; 附違反的規則：dist/just/&lt;ns&gt;.just 每檔一個頂層命名空間、只准一般檔或目錄、文字檔不得含 CR；含 undev 取到不合格式的內容</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的工具交付內容不合格式：&lt;reason&gt;。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Tool delivery content violates its format; &lt;reason&gt; identifies the rule: each dist/just/&lt;ns&gt;.just file has one top-level namespace, only regular files and directories are permitted, and text files must not contain CR; this includes invalid content fetched by undev</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Invalid tool delivery format for &lt;repo&gt;: &lt;reason&gt;. The requested operation did not complete.</mark>

#### VK0076
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">engine launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">薄殼介面版 P 高於鎖定引擎接受的介面版上限；本機覆寫的引擎另報 VK0086</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">薄殼介面版 &lt;P_shell&gt; 高於引擎 &lt;vY&gt; 接受的上限 &lt;P_current&gt;。請執行：just vendor_kit upgrade --engine</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">Shell interface version P is higher than the maximum accepted by the locked engine; a locally overridden engine uses VK0086 instead</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Shell interface version &lt;P_shell&gt; exceeds the maximum &lt;P_current&gt; accepted by engine &lt;vY&gt;. Run: just vendor_kit upgrade --engine</mark>

#### VK0077
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">本機 docker 操作或外部程序失敗，含 pull、inspect、load、extract；&lt;operation&gt; 指名動作，&lt;reason&gt; 附實際原因；有專屬碼的不用此碼：啟動器取不到引擎 image 報 VK0036、test runner 報 VK0066</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;operation&gt; 失敗：&lt;reason&gt;。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A local Docker operation or external process fails, including pull, inspect, load, or extract; &lt;operation&gt; names the action and &lt;reason&gt; gives the actual cause; cases with a dedicated code do not use this code: a launcher that cannot obtain the engine image reports VK0036, and test runner failures report VK0066</mark>
- `message.en`：<mark style="background-color:#c8f0c8">&lt;operation&gt; failed: &lt;reason&gt;. The requested operation did not complete.</mark>

#### VK0078
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">同一個 tag 指向不同 digest：本機有兩個 digest、本機與 registry 不同，或引擎升級第一段重做時與進度檔記錄不同</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的 tag &lt;tag&gt; 指向不同 digest：&lt;digests&gt;。要求的操作未完成。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The same tag resolves to different digests: two local digests, a local digest differing from the registry, or a digest differing from the progress file when retrying the first stage of an engine upgrade</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Tag &lt;tag&gt; for &lt;repo&gt; resolves to different digests: &lt;digests&gt;. The requested operation did not complete.</mark>

#### VK0079
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">薄殼是較舊引擎的模板；&lt;upgrade_command&gt; 由 VK 填成 just vendor_kit upgrade --engine=&lt;tag&gt; -y，&lt;tag&gt; 是應重跑的引擎版本</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">薄殼是較舊引擎的模板。請執行：&lt;upgrade_command&gt;</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The shell matches an older engine template; VK fills &lt;upgrade_command&gt; as just vendor_kit upgrade --engine=&lt;tag&gt; -y, with &lt;tag&gt; the engine version to rerun</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Shell files match an older engine template. Run: &lt;upgrade_command&gt;</mark>

#### VK0080
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">引擎 image 的 LABEL 介面版區間 [floor, current] 與 version.toml 旁記的介面版列表頭尾不符</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">引擎 image &lt;image&gt; 的介面版區間與 version.toml 的介面版列表不符。未啟動引擎。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The interface version range [floor, current] in engine image labels differs from the endpoints of the interface version list recorded in version.toml</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The interface version range of engine image &lt;image&gt; differs from the interface version list in version.toml. The engine was not started.</mark>

#### VK0081
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">Docker daemon 形態不支援，包括 userns-remap；不建立執行紀錄；待確認 (N6b)</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">不支援 Docker daemon 形態 &lt;mode&gt;。請改用支援的 rootful 或 rootless Docker 後重試。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The Docker daemon configuration is unsupported, including userns-remap; no run log is created; Pending confirmation (N6b)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Docker daemon configuration &lt;mode&gt; is unsupported. Switch to supported rootful or rootless Docker and retry.</mark>

#### VK0082
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">建立執行紀錄後的能力檢查失敗；&lt;reason&gt; 指明缺少的能力；待確認 (N6b)</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">Docker 能力檢查失敗：&lt;reason&gt;。請修正環境後重試。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A capability check fails after creating the run log; &lt;reason&gt; identifies the missing capability; Pending confirmation (N6b)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Docker capability check failed: &lt;reason&gt;. Fix the environment and retry.</mark>

#### VK0083
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">bootstrap.sh 偵測到 uninstall 未完成；&lt;completion_command&gt; 由 VK 填成可直接執行的完成模式指令，選項名與所用引擎版本尚未定；待確認 (N8b)</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">uninstall 未完成。請執行：&lt;completion_command&gt;</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">bootstrap.sh detects an incomplete uninstall; VK fills &lt;completion_command&gt; as an executable completion-mode command; the option name and engine version are unresolved; Pending confirmation (N8b)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Uninstall is incomplete. Run: &lt;completion_command&gt;</mark>

#### VK0084
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">add 帶 -y 又不能互動，卻需要 append 進已存在、未納管的檔；-y 不代答這些詢問；&lt;original_command&gt; 由 VK 重組原本完整指令，需在終端重跑；處置待確認 (Y1)，disposition 欄的 pending 只算暫填</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">需要確認附加到既有未納管檔 &lt;file&gt; 的內容，但 -y 不代答且無法互動。請在終端執行：&lt;original_command&gt;</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">add receives -y and cannot interact, but needs to append to an existing unmanaged file; -y does not answer these prompts; VK rebuilds &lt;original_command&gt; as the original full command to rerun from a terminal; disposition is pending confirmation (Y1), and the disposition column is provisional</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Appending to existing unmanaged file &lt;file&gt; requires confirmation, but -y does not answer this prompt and interaction is unavailable. Run from a terminal: &lt;original_command&gt;</mark>

#### VK0085
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">dev --engine 以 -i 指定的本機 image 介面版區間不含薄殼的 P（P 高於 current 或低於 floor）；不寫本機覆寫，下一步改用區間包含 P 的 image</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">本機引擎 image &lt;image&gt; 的介面版區間 &lt;P_floor&gt;～&lt;P_current&gt; 不含薄殼介面版 &lt;P_shell&gt;。未啟用本機覆寫。請換用區間包含 &lt;P_shell&gt; 的 image。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The local image specified with -i for dev --engine has an interface version range that does not include shell version P (P is above current or below floor); no local override is written; use an image whose range includes P</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Local engine image &lt;image&gt; accepts interface versions &lt;P_floor&gt; through &lt;P_current&gt;, excluding shell version &lt;P_shell&gt;. The local override was not enabled. Use an image whose range includes &lt;P_shell&gt;.</mark>

#### VK0086
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">3</mark>
- `disposition`：<mark style="background-color:#c8f0c8">pending</mark>
- `source`：<mark style="background-color:#c8f0c8">launcher</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">啟動器套用引擎本機覆寫時，覆寫 image 的介面版區間不含薄殼 P（P 高於 current 或低於 floor）；解除覆寫或換用區間包含 P 的 image</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">本機覆寫 image &lt;image&gt; 的介面版區間 &lt;P_floor&gt;～&lt;P_current&gt; 不含薄殼介面版 &lt;P_shell&gt;。請解除覆寫後換用相容的 image：just vendor_kit undev --engine</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">When applying an engine local override, the launcher finds that the override image accepts a range excluding shell interface version P (P is above current or below floor); remove the override or use an image whose range includes P</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Local override image &lt;image&gt; accepts interface versions &lt;P_floor&gt; through &lt;P_current&gt;, excluding shell version &lt;P_shell&gt;. Remove the override before selecting a compatible image: just vendor_kit undev --engine</mark>

#### VK0087
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">基準版合併結果是 TOML 或 just 卻解析不過：TOML 依 TOML 規格解析，不是 UTF-8 也算解析不過；just 檔（justfile、.justfile，檔名不分大小寫；*.just） 只檢查衝突標記；留原檔、基準版不推，路徑記進 metadata 的 conflicts；待確認 (D2)：目前實作不印此診斷、以 0 結束；嚴重度與結束碼未定，level 與 exit_code 欄只算暫填</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;file&gt; 的基準版合併結果無法解析。已保留原檔與基準版，並記入 conflicts。請手動處理。</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A baseline merge result is TOML or just but fails parsing: TOML is parsed per the TOML specification and non-UTF-8 also fails parsing; just files (justfile and .justfile, both filenames case-insensitive; *.just) are checked only for conflict markers; the original file and baseline are retained and the path is recorded in metadata conflicts; Pending confirmation (D2): the current implementation does not emit this diagnostic and exits with 0; severity and exit code are undecided, and the level and exit_code columns are provisional</mark>
- `message.en`：<mark style="background-color:#c8f0c8">The baseline merge result for &lt;file&gt; cannot be parsed. The original file and baseline were retained, and the path was recorded in conflicts. Handle it manually.</mark>

沒改動的代碼 42 個：VK0003、VK0004、VK0006、VK0007、VK0008、VK0010、VK0012、VK0014、VK0016、VK0017、VK0018、VK0019、VK0020、VK0022、VK0024、VK0027、VK0028、VK0029、VK0032、VK0033、VK0035、VK0038、VK0039、VK0040、VK0041、VK0042、VK0044、VK0045、VK0049、VK0050、VK0051、VK0056、VK0057、VK0059、VK0060、VK0061、VK0062、VK0063、VK0064、VK0065、VK0066、VK0067。
