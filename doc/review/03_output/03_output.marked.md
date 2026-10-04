<!-- 標示版：綠底 <mark> 是新增、紅底 <mark> 是刪除，程式碼區塊的改動改成 diff 區塊（+ 新增、- 刪除）；本檔進 git，定案時刪除該鍵的送審資料夾；基準是定案 commit 480f5c2。正式內容看 /doc/contract/03_output.md 與 /doc/contract/reason_codes.csv -->

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

```diff
 stdout: A current: v1.2.0 latest: v1.2.0
 stdout: B current: v1.2.0 latest: v1.3.0
 stdout: C current: v2.0.0 latest: none
-stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required; pulling still uses the host's Docker credentials. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit upgrade C@<tag>
+stderr: vendor_kit: error[VK0001]: Cannot list versions for C: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file <path> and rerun, or specify a version directly: just vendor_kit upgrade C@<tag>
 exit code: 2
```

## 輸出

- <mark style="background-color:#f8c8c8">成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`/`--help` 用法只印到 stdout，不加前綴</mark>
- <mark style="background-color:#f8c8c8">stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行、用法錯誤後附的用法，以及 [update](../../../GLOSSARY.md#vk-recipe-與用途) 印的[本機覆寫](../../../GLOSSARY.md#版本與來源)提醒（不加前綴）</mark>
- <mark style="background-color:#c8f0c8">成功時改了什麼、查詢或檢查結果，以及 `bootstrap.sh` 與各 recipe 的 `-h`/`--help` 用法只印到 stdout（[test](../../../GLOSSARY.md#vk-recipe-與用途) 帶路徑時轉出的測試輸出除外），不加前綴</mark>
- <mark style="background-color:#c8f0c8">stderr 只放診斷及其續行、[詢問](../../../GLOSSARY.md#執行與結果)文字、不帶指令時第一行的版本行、用法錯誤後附的用法，以及 [update](../../../GLOSSARY.md#vk-recipe-與用途) 印的[本機覆寫](../../../GLOSSARY.md#版本與來源)提醒（不加前綴；test 帶路徑時轉出的測試輸出除外）</mark>
- <mark style="background-color:#c8f0c8">`just vendor_kit test` 帶路徑、跑[使用者](../../../GLOSSARY.md#角色與情境)自己的測試時，測試程式 (runner) 的 stdout 轉到 VK 的 stdout、stderr 轉到 VK 的 stderr，原樣轉出、不加前綴；這些輸出不是 VK 的固定格式，不承諾可解析，依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)</mark>
- 只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、下列診斷與簡短用法，以 `2` 結束：

  ```diff
   $ just vendor_kit
   stderr: vendor_kit <version>
   stderr: vendor_kit: error[VK0024]: No command was specified.
  -stderr: Usage: just vendor_kit <command> [arguments] [options]
  +stderr: Usage: just vendor_kit <cmd> [arguments] [options]
   exit code: 2
  ```
- 主機前置檢查（檢查主機上的 Docker 與 just）排在建執行紀錄之前；找不到 docker、Docker 低於 19.03、`docker --version` 的輸出含 Podman、找不到 just 或 just 低於 1.33.0 時，檢查不通過。不通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。各入口檢查哪幾項見 [04 使用者介面](../../contract/04_interface.md#bootstrapsh)
- `remove`/`uninstall` 依契約保留[初始檔](../../../GLOSSARY.md#初始檔與合併)時，把保留清單印到 stdout，沒有其他診斷時以 `0` 結束
- <mark style="background-color:#f8c8c8">詢問時[使用者](../../../GLOSSARY.md#角色與情境)明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束</mark>
- <mark style="background-color:#f8c8c8">顏色照這幾條：</mark>
- <mark style="background-color:#c8f0c8">詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束</mark>
- <mark style="background-color:#c8f0c8">VK 自己印的字句，顏色照這幾條：</mark>
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

<mark style="background-color:#c8f0c8">`bootstrap.sh` 用到的訊息在發布時由訊息表產生並內嵌進 `bootstrap.sh`。</mark>

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
  - <mark style="background-color:#f8c8c8">左邊五欄給程式讀，只用英文：</mark>
  - <mark style="background-color:#c8f0c8">左邊六欄給程式讀，只用英文；加上目前兩組語言欄，共十欄：</mark>
    - `code`：原因代碼，依代碼升冪排列；新代碼持續遞增，大版本清理停用列後可留下缺號
    - `status`：`active` 使用中；`retired` 已停用
    - `level`：現行值為 `warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)
    - `exit_code`：該 `level` 欄對應的結束碼；`warn` 為 `1`、`error` 為 `2`、`fatal` 為 `3`；`retired` 列留空
    - `disposition`：處置，`pending`（待處理）、`failed`（失敗）或留空；warn 的列與用法錯誤（`situation.en` 以 `Usage error:` 開頭的列）留空
    - <mark style="background-color:#c8f0c8">`source`：發出診斷的入口，放在 `disposition` 之後、語言欄之前；值為 `bootstrap` (`bootstrap.sh`)、`engine`（引擎）、`launcher`（薄殼的[啟動器](../../../GLOSSARY.md#vk-組件)）、`test` (test)；列出所有會印出這條診斷的入口；`test` 表示由 test recipe 印出，與 `engine` 並列；可有多個值，以單一空白分隔，依 `bootstrap`、`engine`、`launcher`、`test` 的順序排列；`retired` 列留空</mark>
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

- 表頭：<mark style="background-color:#f8c8c8">code,status,level,exit_code,disposition,situation.en,message.en,situation.zh-TW,message.zh-TW</mark> → <mark style="background-color:#c8f0c8">code,status,level,exit_code,disposition,source,situation.en,message.en,situation.zh-TW,message.zh-TW</mark>
- `source`：<mark style="background-color:#c8f0c8">（本欄新增）</mark>

#### VK0001

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">update, upgrade, or add needs to list versions but has no registry credentials; &lt;command&gt; prints add for add and upgrade for update or upgrade; &lt;tag&gt; is printed literally for the user to replace with the version tag to install</mark> → <mark style="background-color:#c8f0c8">update, upgrade, or add needs to list versions, the registry requires read access, and this invocation did not supply --registry-token-file; &lt;cmd&gt; prints add for add and upgrade for update or upgrade; &lt;path&gt; and &lt;tag&gt; are printed literally for the user to replace with the token file path and the version tag to install</mark>
- `message.en`：<mark style="background-color:#f8c8c8">Cannot list versions for &lt;repo&gt;: registry read access is required; pulling still uses the host's Docker credentials. Set VENDOR_KIT_REGISTRY_TOKEN (or VENDOR_KIT_REGISTRY_TOKEN_FILE), or specify a version directly: just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;</mark> → <mark style="background-color:#c8f0c8">Cannot list versions for &lt;repo&gt;: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file &lt;path&gt; and rerun, or specify a version directly: just vendor_kit &lt;cmd&gt; &lt;repo&gt;@&lt;tag&gt;</mark>
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;command&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark> → <mark style="background-color:#c8f0c8">update、upgrade、add 需要列版本，registry 要求讀取權限，而這次沒有帶 --registry-token-file；&lt;cmd&gt; 在 add 時印 add，update、upgrade 時印 upgrade；&lt;path&gt; 與 &lt;tag&gt; 原樣印出，由使用者換成 token 檔路徑與要安裝的版本 tag</mark>
- `message.zh-TW`：<mark style="background-color:#f8c8c8">無法列出 &lt;repo&gt; 的版本：需要 registry 讀取權限；拉取時仍使用主機的 Docker 認證。請設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;command&gt; &lt;repo&gt;@&lt;tag&gt;</mark> → <mark style="background-color:#c8f0c8">無法列出 &lt;repo&gt; 的版本：需要 registry 讀取權限；拉取時仍使用主機的 Docker 認證。請加上 --registry-token-file &lt;path&gt; 重新執行，或直接指定版本：just vendor_kit &lt;cmd&gt; &lt;repo&gt;@&lt;tag&gt;</mark>

#### VK0002

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：An operation requires a prompt, but -y was not given and interaction is impossible (stdin or stderr is not a terminal, or end of input was read); &lt;command_with_y&gt; is rebuilt from this run's arguments one by one, each quoted by POSIX shell rules, with -y inserted before a standalone --, or appended at the end if there is no --; during initial import by bootstrap.sh, &lt;command_with_y&gt; starts with the script path ($0) of this invocation, followed by this run's arguments, rebuilt by the same rules
- `message.en`：Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: &lt;command_with_y&gt;
- `situation.zh-TW`：操作需要詢問，但沒帶 -y 又不能互動（stdin 或 stderr 不是終端，或讀到輸入結束）；&lt;command_with_y&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後；bootstrap.sh 首次導入時，&lt;command_with_y&gt; 以這次呼叫的腳本路徑 ($0) 開頭，後接這次的參數，依同一規則重組
- `message.zh-TW`：需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;command_with_y&gt;

#### VK0004

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：sync finds a tool whose import is incomplete, or a read-only recipe reads a progress file for that tool's incomplete import
- `message.en`：Import of &lt;repo&gt; is incomplete. Run: just vendor_kit add &lt;repo&gt;
- `situation.zh-TW`：sync 發現某個工具未完成導入，或唯讀 recipe 讀到該工具導入未完成的進度檔
- `message.zh-TW`：&lt;repo&gt; 的導入未完成。請執行：just vendor_kit add &lt;repo&gt;

#### VK0005

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：During initial import, bootstrap.sh finds the host's just is older than 1.33.0; &lt;install_command&gt; does not overwrite the host's existing just and does not require the host to install any other tool
- `message.en`：just 1.33.0 or later is required; the current version is &lt;version&gt;. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;
- `situation.zh-TW`：bootstrap.sh 首次導入時發現主機的 just 低於 1.33.0；&lt;install_command&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具
- `message.zh-TW`：需要 just 1.33.0 或更新版本；目前版本為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;

#### VK0006

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：During the engine's startup check or a bootstrap.sh check-only run, shell files do not match this engine version's templates (their content was modified, or they are not this engine version's templates); when --repair finds a mismatch, it regenerates the shell files and reports the result instead of this diagnostic; during a bootstrap.sh check-only run or --repair, if the progress file records an incomplete engine upgrade, VK0023 is reported instead and no shell comparison is made; &lt;files&gt; marks which case applies to each file; no repo files or other VK files are touched except the run log
- `message.en`：Shell files do not match this engine version's templates: &lt;files&gt;. No shell files were regenerated. Review the following differences; download bootstrap.sh again from the Release, run chmod +x bootstrap.sh, then run ./bootstrap.sh --repair in the install directory.
- `situation.zh-TW`：引擎啟動檢查或 bootstrap.sh 只檢查時，薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）；--repair 發現不符時改為重產薄殼並報告結果，不報這個診斷；bootstrap.sh 只檢查或 --repair 時，若進度檔記錄引擎升級未完成，改報 VK0023，不做薄殼比對；&lt;files&gt; 逐檔標出是哪一種，除執行紀錄外不動 repo 檔與其他 VK 檔
- `message.zh-TW`：薄殼與這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請檢視下列差異；從 Release 重新下載 bootstrap.sh，執行 chmod +x bootstrap.sh，再到安裝目錄執行 ./bootstrap.sh --repair。

#### VK0007

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：upgrade --engine=&lt;tag&gt; downgrades, but the target engine cannot read the existing VK files without loss; the &lt;tag&gt; in the message is printed literally for the user to replace with an engine version tag that can read schema version &lt;N&gt;
- `message.en`：Target engine &lt;vY&gt; (interface version &lt;P&gt;, schema version &lt;M&gt;) cannot read the existing files (schema version &lt;N&gt;) without loss. No files were modified except the run log. Specify a version that can read schema version &lt;N&gt;: just vendor_kit upgrade --engine=&lt;tag&gt;
- `situation.zh-TW`：upgrade --engine=&lt;tag&gt; 降版，但目標引擎無法無損讀取現有的 VK 檔；本文的 &lt;tag&gt; 原樣印出，由使用者換成能讀取檔案版 &lt;N&gt; 的引擎版本 tag
- `message.zh-TW`：目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有的檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;

#### VK0008

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The engine reads a VK file whose schema version is higher than the maximum this engine supports
- `message.en`：Cannot read &lt;file&gt;: schema version &lt;N&gt; is newer than the maximum supported version &lt;M&gt;; written by vendor_kit &lt;written_by&gt;. Upgrade the engine: just vendor_kit upgrade --engine
- `situation.zh-TW`：引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限
- `message.zh-TW`：無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的最高版本 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine

#### VK0009

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">launcher</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：An old shell meets an engine with a newer major version X and runs a recipe outside the rescue path
- `message.en`：Shell interface version &lt;P_shell&gt; is older than required for general recipes in engine &lt;vY&gt;. Run first: just vendor_kit upgrade --engine
- `situation.zh-TW`：舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe
- `message.zh-TW`：薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 一般 recipe 所需的版本。請先執行：just vendor_kit upgrade --engine

#### VK0010

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine launcher test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：Any VK recipe, or bootstrap.sh initial import (including an incomplete initial import), check-only run, or --repair, cannot create the run log (it exits before any side effect; initial import creates the log before calling install)
- `message.en`：Cannot write run log &lt;path&gt;: &lt;reason&gt;. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry.
- `situation.zh-TW`：任何 VK recipe，或 bootstrap.sh 首次導入（含未完成的首次導入）、只檢查、--repair 時，建不出執行紀錄（在任何副作用之前結束，首次導入在呼叫 install 之前先建紀錄）
- `message.zh-TW`：無法寫入執行紀錄 &lt;path&gt;：&lt;reason&gt;。vendor_kit 不在沒有紀錄的情況下執行；未修改任何檔。請清出磁碟空間或修正權限後重試。

#### VK0011

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The output of docker --version contains podman
- `message.en`：Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.
- `situation.zh-TW`：docker --version 的輸出含 podman
- `message.zh-TW`：偵測到 Podman (docker --version)。vendor_kit 只支援 Docker。請改用 Docker（rootful 或 rootless）後重試。

#### VK0012

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The launcher finds the host's Docker is older than 19.03
- `message.en`：Docker 19.03 or later is required; the current version is &lt;version&gt;. Upgrade Docker and retry.
- `situation.zh-TW`：啟動器發現主機的 Docker 低於 19.03
- `message.zh-TW`：需要 Docker 19.03 或更新版本；目前版本為 &lt;version&gt;。請升級 Docker 後重試。

#### VK0013

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：metadata is missing or corrupt and cannot be restored reliably
- `message.en`：Cannot process &lt;file&gt;: metadata is missing or corrupt and cannot be restored reliably. vendor_kit does not guess when records are unavailable; no files of the tool that &lt;file&gt; belongs to were modified. Preserve &lt;file&gt; and run log &lt;path&gt;. If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.
- `situation.zh-TW`：metadata 缺失或損壞，無法可靠還原
- `message.zh-TW`：無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。紀錄不可用時，vendor_kit 不做推測；&lt;file&gt; 所屬工具的檔都未修改。請保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;。metadata 若曾 commit 進 Git，從 Git 還原後重試；否則到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，並附上這兩個檔。

#### VK0014

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：sync or test finds the baseline is behind the lock version line
- `message.en`：The baseline for &lt;repo&gt; is behind the lock version line. Run: just vendor_kit upgrade &lt;repo&gt; -y
- `situation.zh-TW`：sync 或 test 發現基準版落後版本鎖定行
- `message.zh-TW`：&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y

#### VK0015

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：sync finds the file set or per-file digests in cache/ for a locked tool do not match, and has refetched according to the lock version line; tool directories not in the lock version lines are not covered by this case
- `message.en`：The file set or per-file digests in cache/ for &lt;repo&gt; did not match; refetched according to the lock version line.
- `situation.zh-TW`：sync 發現已鎖定工具的 cache/ 檔案集合或逐檔指紋不符，已依版本鎖定行重新取件；不在版本鎖定行的工具目錄不屬於這個情況
- `message.zh-TW`：&lt;repo&gt; 在 cache/ 的檔案集合或逐檔指紋不符；已依版本鎖定行重新取件。

#### VK0016
<mark style="background-color:#f8c8c8">（本碼停用）</mark>

- `status`：<mark style="background-color:#f8c8c8">active</mark> → <mark style="background-color:#c8f0c8">retired</mark>
- `level`：<mark style="background-color:#f8c8c8">warn</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `exit_code`：<mark style="background-color:#f8c8c8">1</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation.en`：When removing an appended line, the originally inserted text cannot be found in the file
- `message.en`：<mark style="background-color:#f8c8c8">Could not find the original text to remove from &lt;file&gt;; the line was not removed. Check it manually.</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation.zh-TW`：收回 append 行時，在檔內找不到當初插入的原文
- `message.zh-TW`：<mark style="background-color:#f8c8c8">在 &lt;file&gt; 中找不到要移除的原文；未移除該行。請手動檢查。</mark> → <mark style="background-color:#c8f0c8">（空）</mark>

#### VK0017
<mark style="background-color:#f8c8c8">（本碼停用）</mark>

- `status`：<mark style="background-color:#f8c8c8">active</mark> → <mark style="background-color:#c8f0c8">retired</mark>
- `level`：<mark style="background-color:#f8c8c8">warn</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `exit_code`：<mark style="background-color:#f8c8c8">1</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation.en`：When removing an appended line, multiple occurrences identical to the originally inserted text are found in the file
- `message.en`：<mark style="background-color:#f8c8c8">Found &lt;count&gt; occurrences of the original text to remove from &lt;file&gt; and could not attribute one uniquely; the line was not removed. Check it manually.</mark> → <mark style="background-color:#c8f0c8">（空）</mark>
- `situation.zh-TW`：收回 append 行時，在檔內找到多處與當初插入的原文相同
- `message.zh-TW`：<mark style="background-color:#f8c8c8">在 &lt;file&gt; 中找到 &lt;count&gt; 處要移除的原文，無法唯一歸屬其中一處；未移除該行。請手動檢查。</mark> → <mark style="background-color:#c8f0c8">（空）</mark>

#### VK0018

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：add encounters a file that already exists and is not yet managed
- `message.en`：&lt;file&gt; already exists and is unmanaged; it was neither overwritten nor brought under management.
- `situation.zh-TW`：add 遇到已存在、尚未納管的檔
- `message.zh-TW`：&lt;file&gt; 已存在且未納管；既未覆蓋，也未納入管理。

#### VK0019

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：A file is unmanaged and is not processed in this run
- `message.en`：&lt;file&gt; is unmanaged and was not processed.
- `situation.zh-TW`：檔案沒有納管，本次不處理
- `message.zh-TW`：&lt;file&gt; 未納管，未處理。

#### VK0020

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：This version was previously rejected by the user
- `message.en`：Version &lt;tag&gt; of &lt;repo&gt; was previously rejected; it was not prompted again or applied.
- `situation.zh-TW`：這個版本先前已由使用者拒絕
- `message.zh-TW`：&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；未再次詢問，也未套用。

#### VK0021

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：A baseline merge leaves merge conflicts
- `message.en`：&lt;file&gt; contains merge conflicts. Review and resolve them: git status
- `situation.zh-TW`：基準版合併留下合併衝突
- `message.zh-TW`：&lt;file&gt; 含有合併衝突。請檢視並解決：git status

#### VK0023

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：After upgrade --engine installs the new engine, the original command has not yet completed, or a read-only recipe reads a progress file for an incomplete engine upgrade; during a bootstrap.sh check-only run or --repair, reading a progress file that records an incomplete engine upgrade also reports this code, with no shell comparison or regeneration; &lt;original_command&gt; is filled in by VK from the progress file as the original full upgrade command, keeping the original tag and -y, with no substitution needed by the user
- `message.en`：Engine &lt;vY&gt; is now installed. Run again: &lt;original_command&gt;
- `situation.zh-TW`：upgrade --engine 換上新引擎後原指令尚未做完，或唯讀 recipe 讀到引擎升級未完成的進度檔；bootstrap.sh 只檢查或 --repair 時讀到記錄引擎升級未完成的進度檔，也報此碼，不比對或重產薄殼；&lt;original_command&gt; 由 VK 依進度檔填成原本的完整 upgrade 指令，保留原 tag 與 -y，不需使用者代換
- `message.zh-TW`：已安裝引擎 &lt;vY&gt;。請再執行一次：&lt;original_command&gt;

#### VK0024

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：Usage error: only just vendor_kit was entered, with no command specified
- `message.en`：No command was specified.
- `situation.zh-TW`：用法錯誤：只打 just vendor_kit、未指定指令
- `message.zh-TW`：未指定指令。

#### VK0025

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：Usage error: a VK recipe or bootstrap.sh is missing a required argument (including bootstrap.sh -i/--image given without an image)
- `message.en`：Required argument is missing: &lt;argument&gt;.
- `situation.zh-TW`：用法錯誤：VK recipe 或 bootstrap.sh 缺少必要參數（含 bootstrap.sh 的 -i／--image 沒帶 image）
- `message.zh-TW`：缺少必要參數：&lt;argument&gt;。

#### VK0026

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">Usage error: a VK recipe or bootstrap.sh received an unknown option or an extra argument; bootstrap.sh given --repair -y, or -y/--yes in an existing install directory (excluding the incomplete initial import determined from the run log as described in VK0037), or -h/--help combined with other arguments; &lt;value&gt; prints the first unknown or disallowed argument; when -h/--help is combined with other arguments, it prints the first argument that is not -h/--help, or the second argument if all are -h/--help; when a VK recipe's -h/--help is combined with arguments other than --engine, &lt;value&gt; prints the first argument that is neither -h/--help nor --engine</mark> → <mark style="background-color:#c8f0c8">Usage error: a VK recipe or bootstrap.sh received an unknown option or an extra argument; bootstrap.sh given --repair -y, or -y/--yes in an existing install directory (excluding the incomplete initial import determined from the run log as described in VK0037), or -h/--help combined with other arguments; &lt;value&gt; prints the first unknown or disallowed argument; when -h/--help is combined with other arguments, it prints the first argument that is not -h/--help, or the second argument if all are -h/--help; when a VK recipe's -h/--help is combined with arguments other than --engine, &lt;value&gt; prints the first argument that is neither -h/--help nor --engine; this includes test given more than one path, or a path combined with test dist; for multiple paths, &lt;value&gt; prints the second path (the first extra argument); for a path combined with test dist, &lt;value&gt; prints the given path; this includes a --registry-token-file value that is a lone - (VK does not read stdin), where &lt;value&gt; prints -; usage is appended to stderr</mark>
- `message.en`：Unknown, extra, or disallowed argument: &lt;value&gt;.
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">用法錯誤：VK recipe 或 bootstrap.sh 帶了不認得的選項或多出的參數；bootstrap.sh 帶 --repair -y，或在既有安裝目錄帶 -y／--yes（排除 VK0037 所述、依執行紀錄判定的未完成首次導入），或 -h／--help 與其他參數並用；&lt;value&gt; 印第一個不認得或不允許的參數；-h／--help 與其他參數並用時，印第一個不是 -h／--help 的參數，若全部都是 -h／--help，則印第二個參數；VK recipe 的 -h／--help 與 --engine 以外的參數並用時，&lt;value&gt; 印第一個不是 -h／--help 或 --engine 的參數</mark> → <mark style="background-color:#c8f0c8">用法錯誤：VK recipe 或 bootstrap.sh 帶了不認得的選項或多出的參數；bootstrap.sh 帶 --repair -y，或在既有安裝目錄帶 -y／--yes（排除 VK0037 所述、依執行紀錄判定的未完成首次導入），或 -h／--help 與其他參數並用；&lt;value&gt; 印第一個不認得或不允許的參數；-h／--help 與其他參數並用時，印第一個不是 -h／--help 的參數，若全部都是 -h／--help，則印第二個參數；VK recipe 的 -h／--help 與 --engine 以外的參數並用時，&lt;value&gt; 印第一個不是 -h／--help 或 --engine 的參數；包含 test 一次給兩個以上 path，或 path 與 test dist 混用；給兩個以上 path 時，&lt;value&gt; 印第二個 path（第一個多出的參數）；path 與 test dist 混用時，&lt;value&gt; 印所給的 path；包含 --registry-token-file 的值是單獨的 -（VK 不從 stdin 讀），此時 &lt;value&gt; 印 -；在 stderr 附上用法</mark>
- `message.zh-TW`：不認得、多出或此處不允許的參數：&lt;value&gt;。

#### VK0027

- `status`：active
- `level`：error
- `exit_code`：2
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：Usage error: the tag format is invalid
- `message.en`：Invalid tag format: &lt;tag&gt;. Use vX.Y.Z with no leading zeros in X, Y, or Z.
- `situation.zh-TW`：用法錯誤：tag 格式不合
- `message.zh-TW`：tag 格式不正確：&lt;tag&gt;。請使用 vX.Y.Z，X、Y、Z 都不可有前導零。

#### VK0028

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：A VK recipe is run outside an install directory
- `message.en`：The current directory is not an install directory. Run: cd &lt;install_dir&gt;
- `situation.zh-TW`：在安裝目錄外執行 VK recipe
- `message.zh-TW`：目前目錄不是安裝目錄。請執行：cd &lt;install_dir&gt;

#### VK0029

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：install finds an existing install directory above or below
- `message.en`：Cannot create a nested install directory: &lt;existing_install_dir&gt; is already an install directory.
- `situation.zh-TW`：install 時上層或下層已有安裝目錄
- `message.zh-TW`：無法建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。

#### VK0030

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：add finds a name collision on &lt;ns&gt;
- `message.en`：Cannot add &lt;repo&gt;: namespace &lt;ns&gt; is already used by &lt;owner&gt;.
- `situation.zh-TW`：add 時 &lt;ns&gt; 撞名
- `message.zh-TW`：無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。

#### VK0031

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The local image or image tar for offline import lacks required digest information; or bootstrap.sh is given -i/--image in an existing install directory and the supplied local image or image tar lacks required digest information, or its digest does not match the engine lock version line; applies to both check-only runs and --repair; &lt;reason&gt; is filled as required digest information is missing or the digest does not match the engine lock version line, as applicable
- `message.en`：Cannot use image &lt;image&gt;: &lt;reason&gt;. The supplied image was not used.
- `situation.zh-TW`：離線導入的本機 image 或 image tar 缺少必要的 digest 資訊；或 bootstrap.sh 在既有安裝目錄帶 -i／--image，所提供的本機 image 或 image tar 缺少必要的 digest 資訊，或 digest 與引擎版本鎖定行不符；只檢查與 --repair 都適用；&lt;reason&gt; 依情況填為 required digest information is missing 或 the digest does not match the engine lock version line
- `message.zh-TW`：無法使用 image &lt;image&gt;：&lt;reason&gt;。未使用所提供的 image。

#### VK0032

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：test finds a local override; &lt;undev_command&gt; prints as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target
- `message.en`：Test cannot run while a local override of &lt;target&gt; is active. Run: &lt;undev_command&gt;
- `situation.zh-TW`：test 發現本機覆寫；&lt;undev_command&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine
- `message.zh-TW`：&lt;target&gt; 的本機覆寫仍在作用中，無法執行 test。請執行：&lt;undev_command&gt;

#### VK0033

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The launcher cannot find docker on the host (checked by bootstrap.sh initial import, check-only runs, and --repair, and by the shell's launcher)
- `message.en`：Docker was not found on the host. Install Docker and retry.
- `situation.zh-TW`：啟動器找不到主機的 docker（bootstrap.sh 的首次導入、只檢查、--repair，以及薄殼的啟動器都檢查）
- `message.zh-TW`：主機上找不到 Docker。請安裝 Docker 後重試。

#### VK0034

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：During initial import, bootstrap.sh cannot find just on the host; &lt;install_command&gt; is filled in by VK, runs directly with no substitution needed by the user, and does not require the host to install any other tool
- `message.en`：just was not found on the host. Use the GitHub release.<br>Download: &lt;download_url&gt;<br>Install: &lt;install_command&gt;
- `situation.zh-TW`：bootstrap.sh 首次導入時找不到主機的 just；&lt;install_command&gt; 由 VK 填好，可直接執行、不需使用者代換，不要求主機另裝其他工具
- `message.zh-TW`：主機上找不到 just。請使用 GitHub release 版。<br>下載：&lt;download_url&gt;<br>安裝：&lt;install_command&gt;

#### VK0035

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：bootstrap.sh cannot find .git in the current directory or any parent; it does not call git on the host and does not create a repo for the user
- `message.en`：Cannot find .git in the current directory or any parent directory. Run bootstrap.sh from within a Git repository.
- `situation.zh-TW`：bootstrap.sh 從目前目錄往上找不到 .git；不在主機呼叫 git，也不替使用者建立 repo
- `message.zh-TW`：在目前目錄與所有上層目錄都找不到 .git。請在 Git repo 內執行 bootstrap.sh。

#### VK0036

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap launcher</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The launcher cannot obtain the engine image it needs (the embedded version for initial import, including an incomplete initial import; the version specified by the lock version line when one exists); no other version is used instead
- `message.en`：Cannot obtain engine image &lt;image&gt;: &lt;reason&gt;. No alternative engine version was used.
- `situation.zh-TW`：啟動器取不到要用的引擎 image（首次導入含未完成的首次導入時用內嵌版本；已有版本鎖定行時用它指定的版本）；不改用其他版本
- `message.zh-TW`：無法取得引擎 image &lt;image&gt;：&lt;reason&gt;。未改用其他引擎版本。

#### VK0037

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：bootstrap.sh finds .vendor_kit/ in the current directory but cannot read exactly one valid engine lock version line; it stops and does not fall back to initial import; only for initial-import invocations (no arguments, -y, -i, including the corresponding long options and their valid combinations), an incomplete initial import that can be uniquely determined from the run log is excluded: the most recent run log is an initial import, and either (a) it stopped at VK0002 with no files modified except the run log, or (b) it ended after the run log was created and before the engine lock version line was written (whether or not other files were written); these states allow rerunning initial import with -y, the determination does not rely on whether files exist, and it still stops when the state cannot be uniquely determined; --repair still reports VK0037 in these states
- `message.en`：Cannot read exactly one valid engine lock version line from .vendor_kit/version.toml. Initial import was not attempted.
- `situation.zh-TW`：bootstrap.sh 發現目前目錄有 .vendor_kit/，但讀不到恰好一行有效的引擎版本鎖定行；停下，不改走首次導入；僅首次導入的呼叫（不帶參數、-y、-i，含對應長選項及其合法組合）排除可依執行紀錄唯一判定的未完成首次導入：最近一筆執行紀錄是首次導入，且 (a) 停在 VK0002、除執行紀錄外未修改任何檔，或 (b) 在建執行紀錄之後、寫入引擎版本鎖定行之前結束（不論是否已寫入其他檔）；這些狀態允許帶 -y 重跑首次導入，判定不靠檔案在不在，無法唯一判定時仍停下；--repair 在這些狀態下仍報 VK0037
- `message.zh-TW`：無法從 .vendor_kit/version.toml 讀取恰好一行有效的引擎版本鎖定行。未嘗試首次導入。

#### VK0038

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：bootstrap.sh is given -i/--image with an image reference in an existing install directory, and the digest matches the engine lock version line but the full image reference does not; a missing or mismatched digest reports VK0031 instead; applies to both check-only runs and --repair
- `message.en`：Image &lt;image&gt; does not exactly match the engine lock version line &lt;locked_image&gt;. The supplied image was not used.
- `situation.zh-TW`：bootstrap.sh 在既有安裝目錄以 image 引用帶 -i／--image，digest 與引擎版本鎖定行相符，但完整 image 引用不符；缺少 digest 或 digest 不符改報 VK0031；只檢查與 --repair 都適用
- `message.zh-TW`：image &lt;image&gt; 與引擎版本鎖定行 &lt;locked_image&gt; 不完全相同。未使用所提供的 image。

#### VK0039

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：bootstrap.sh is given --repair outside an install directory (the current directory has no .vendor_kit/); it does not fall back to initial import
- `message.en`：Cannot repair shell files outside an install directory. Initial import was not attempted.
- `situation.zh-TW`：bootstrap.sh 在非安裝目錄帶 --repair（目前目錄沒有 .vendor_kit/）；不改走首次導入
- `message.zh-TW`：無法在安裝目錄外修復薄殼。未嘗試首次導入。

#### VK0040

- `status`：active
- `level`：fatal
- `exit_code`：3
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">bootstrap</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：During a bootstrap.sh check-only run or --repair, the major version X of the script's embedded engine version differs from the X of the version specified by the engine lock version line; it stops before any write, image pull, or engine start; &lt;bootstrap_X&gt; and &lt;engine_X&gt; are filled from the script's embedded version and the engine lock version line, respectively
- `message.en`：This bootstrap.sh is for major version &lt;bootstrap_X&gt;, but the locked engine requires major version &lt;engine_X&gt;. No files were modified. Download bootstrap.sh for major version &lt;engine_X&gt; from the Release and retry.
- `situation.zh-TW`：bootstrap.sh 只檢查或 --repair 時，腳本內嵌引擎版本的 X 與引擎版本鎖定行指定版本的 X 不同；在任何寫入、拉 image 或起引擎之前停下；&lt;bootstrap_X&gt; 與 &lt;engine_X&gt; 分別由腳本內嵌版本及引擎版本鎖定行填入
- `message.zh-TW`：這份 bootstrap.sh 適用於主版本 &lt;bootstrap_X&gt;，但鎖定的引擎需要主版本 &lt;engine_X&gt;。未修改任何檔。請從 Release 下載主版本 &lt;engine_X&gt; 的 bootstrap.sh 後重試。

#### VK0041

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：A read-only recipe reads a progress file for an incomplete tool upgrade; it does not resume or delete the progress file; &lt;original_command&gt; is rebuilt by VK from the progress file as the full tool upgrade command, keeping the specified tag and -y, each argument quoted by POSIX shell rules, with no substitution needed by the user
- `message.en`：Upgrade of &lt;repo&gt; is incomplete. Run again: &lt;original_command&gt;
- `situation.zh-TW`：唯讀 recipe 讀到工具 upgrade 未完成的進度檔；不恢復、不刪進度檔；&lt;original_command&gt; 由 VK 依進度檔重組完整的工具 upgrade 指令，保留指定 tag 與 -y，各參數依 POSIX shell 規則加引號，不需使用者代換
- `message.zh-TW`：&lt;repo&gt; 的 upgrade 未完成。請再執行一次：&lt;original_command&gt;

#### VK0042

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">Waiting for the install directory's shared or exclusive lock times out; the default is 60 seconds; VENDOR_KIT_LOCK_TIMEOUT set to 0 fails immediately, set to -1 waits indefinitely; nothing is written except the run log</mark> → <mark style="background-color:#c8f0c8">The shared or exclusive lock could not be acquired within this execution's lock wait deadline; nothing is written except the run log</mark>
- `message.en`：Timed out waiting for the lock in &lt;install_dir&gt;. No files were modified except the run log. Wait for the other execution to finish and retry.
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">等待安裝目錄的共享鎖或排他鎖逾時；預設 60 秒，VENDOR_KIT_LOCK_TIMEOUT 設 0 時立即失敗、設 -1 時無限等待；除執行紀錄外不寫入</mark> → <mark style="background-color:#c8f0c8">未能在這次執行的等鎖期限內取得共享鎖或排他鎖；除執行紀錄外不寫入</mark>
- `message.zh-TW`：等待 &lt;install_dir&gt; 的鎖逾時。除執行紀錄外，未修改任何檔。請等另一個執行結束後重試。

#### VK0043

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The tool image content downloaded by sync does not match the digest in the lock version line; this content is not treated as verified tool content, and VK0015 is not reported
- `message.en`：Downloaded image &lt;image&gt; for &lt;repo&gt; does not match locked digest &lt;digest&gt;. Synchronization did not complete.
- `situation.zh-TW`：sync 下載的工具 image 內容不符版本鎖定行的 digest；不把這份內容當成已驗證的工具內容，不報 VK0015
- `message.zh-TW`：&lt;repo&gt; 下載的 image &lt;image&gt; 與鎖定的 digest &lt;digest&gt; 不符。同步未完成。

#### VK0044

- `status`：active
- `level`：warn
- `exit_code`：1
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：sync finds the existing stamp for &lt;repo&gt; corrupt, and has refetched according to the lock version line and rebuilt the stamp; a first fetch with no stamp yet is not covered by this case
- `message.en`：The existing stamp for &lt;repo&gt; was corrupt; refetched according to the lock version line and rebuilt the stamp.
- `situation.zh-TW`：sync 發現 &lt;repo&gt; 的既有印記損壞，已依版本鎖定行重新取件並重建印記；首次取件尚無印記不屬於此情況
- `message.zh-TW`：&lt;repo&gt; 的既有印記損壞；已依版本鎖定行重新取件並重建印記。

#### VK0045

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：After confirming the tool is fully imported, add receives a tag different from the current locked version; &lt;upgrade_command&gt; is filled in by VK as just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;, using the tag specified this time, with arguments quoted by POSIX shell rules
- `message.en`：Cannot add &lt;repo&gt; at &lt;tag&gt;: it is already imported at &lt;current_tag&gt;. Run: &lt;upgrade_command&gt;
- `situation.zh-TW`：add 在確認工具已完整導入後，收到不同於目前鎖定版本的 tag；&lt;upgrade_command&gt; 由 VK 填成 just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;，使用這次指定的 tag，參數依 POSIX shell 規則加引號
- `message.zh-TW`：無法以 &lt;tag&gt; 加入 &lt;repo&gt;：它已以 &lt;current_tag&gt; 導入。請執行：&lt;upgrade_command&gt;

#### VK0046

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">The tool specified to remove or undev is not in the lock version lines; incomplete progress is identified first, before determining that the target does not exist</mark> → <mark style="background-color:#c8f0c8">The tool specified to remove, undev, or update &lt;repo&gt; is not in the lock version lines; incomplete progress is identified first, before determining that the target does not exist</mark>
- `message.en`：Tool &lt;repo&gt; is not in the lock version lines. The requested operation did not complete.
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">remove 或 undev 指定的工具不在版本鎖定行；先辨識未完成進度，再判斷對象不存在</mark> → <mark style="background-color:#c8f0c8">remove、undev 或 update &lt;repo&gt; 指定的工具不在版本鎖定行；先辨識未完成進度，再判斷對象不存在</mark>
- `message.zh-TW`：版本鎖定行中沒有工具 &lt;repo&gt;。要求的操作未完成。

#### VK0047

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：test cannot complete its checks because files in cache/ or gen/ are missing; it does not fetch, and does not prepare or repair cache/, gen/, or progress files; the run log is still written; whether a fresh CI checkout that has not yet fetched counts as missing files is pending confirmation (see #47, #124)
- `message.en`：Cannot complete checks for &lt;target&gt;: required local files are missing: &lt;files&gt;. Run: just vendor_kit sync
- `situation.zh-TW`：test 因 cache/ 或 gen/ 缺件而無法完成檢查；不取件、不準備或修復 cache/、gen/、進度檔，執行紀錄照寫；CI 全新 checkout 尚未取件時是否算缺件，待確認（見 #47、#124）
- `message.zh-TW`：無法完成 &lt;target&gt; 的檢查：缺少必要的本機檔：&lt;files&gt;。請執行：just vendor_kit sync

#### VK0048

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：test dist runs in a repo with no tool delivery content
- `message.en`：Cannot check tool delivery content: &lt;path&gt; contains no delivery content.
- `situation.zh-TW`：test dist 在沒有工具交付內容的 repo 執行
- `message.zh-TW`：無法檢查工具交付內容：&lt;path&gt; 沒有交付內容。

#### VK0049

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：test or test dist did not complete its checks because the environment is insufficient; &lt;reason&gt; names the missing environment condition
- `message.en`：Cannot complete checks for &lt;target&gt;: &lt;reason&gt;.
- `situation.zh-TW`：test 或 test dist 因環境不足而未完成檢查；&lt;reason&gt; 指明缺少的環境條件
- `message.zh-TW`：無法完成 &lt;target&gt; 的檢查：&lt;reason&gt;。

#### VK0050

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：dev specifies a source different from the existing local override; the existing override is not replaced; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target
- `message.en`：A different local override is already active for &lt;target&gt;. Run first: &lt;undev_command&gt;
- `situation.zh-TW`：dev 指定不同於現有本機覆寫的來源；不取代現有覆寫；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine
- `message.zh-TW`：&lt;target&gt; 已有另一個本機覆寫在作用中。請先執行：&lt;undev_command&gt;

#### VK0051

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：The local directory specified to dev does not exist, or its content does not match the tool's delivery format; relative paths are resolved against the install directory
- `message.en`：Cannot use local source &lt;path&gt; for &lt;repo&gt;: &lt;reason&gt;. The local override was not enabled.
- `situation.zh-TW`：dev 指定的本機目錄不存在，或內容不符合該工具的交付格式；相對路徑以安裝目錄為準
- `message.zh-TW`：無法以本機來源 &lt;path&gt; 作為 &lt;repo&gt; 的來源：&lt;reason&gt;。未啟用本機覆寫。

#### VK0052

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：An action that needs to read a local override source finds the source invalid; only actions that need to read it are blocked; undev can remove the override without reading the source, test still reports VK0032, bootstrap.sh ignores the override, and update checks versions according to the lock version line; &lt;undev_command&gt; is filled as just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine, depending on the target
- `message.en`：Cannot read the local override source &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. Run: &lt;undev_command&gt;
- `situation.zh-TW`：需要讀取本機覆寫來源的動作發現來源失效；只擋需要讀取它的動作；undev 不讀來源即可解除，test 仍報 VK0032，bootstrap.sh 忽略覆寫，update 照版本鎖定行查版本；&lt;undev_command&gt; 依對象填成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine
- `message.zh-TW`：無法讀取 &lt;target&gt; 的本機覆寫來源 &lt;source&gt;：&lt;reason&gt;。請執行：&lt;undev_command&gt;

#### VK0053

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：Synchronization fails after undev removes an override, or a read-only recipe detects an incomplete undev progress file; sync does not clear the progress file on undev's behalf; &lt;undev_command&gt; is filled from the progress file as the original just vendor_kit undev &lt;repo&gt; or just vendor_kit undev --engine
- `message.en`：The undev operation for &lt;target&gt; is incomplete. Run again: &lt;undev_command&gt;
- `situation.zh-TW`：undev 解除覆寫後同步失敗，或唯讀 recipe 偵測到未完成的 undev 進度檔；sync 不代替 undev 清掉進度檔；&lt;undev_command&gt; 依進度檔填成原本的 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine
- `message.zh-TW`：&lt;target&gt; 的 undev 操作未完成。請再執行一次：&lt;undev_command&gt;

#### VK0054

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：pending
- `source`：<mark style="background-color:#c8f0c8">engine test</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：A read-only recipe detects a progress file for an incomplete writing recipe other than the four kinds (incomplete import, tool upgrade, engine upgrade, undev), such as remove, install, uninstall, or dev; it does not resume or delete the progress file; bootstrap.sh still follows the existing determinations of VK0037 and VK0023 and does not widen the initial-import exception; &lt;original_command&gt; is rebuilt by VK from the progress file as the original full command, keeping its arguments, quoted by POSIX shell rules
- `message.en`：Operation &lt;operation&gt; in &lt;install_dir&gt; is incomplete. Run again: &lt;original_command&gt;
- `situation.zh-TW`：唯讀 recipe 偵測到未完成導入、工具 upgrade、引擎 upgrade、undev 這四種以外的可寫 recipe（如 remove、install、uninstall、dev）未完成的進度檔；不恢復、不刪進度檔；bootstrap.sh 仍依 VK0037 與 VK0023 的既有判定，不擴大首次導入例外；&lt;original_command&gt; 由 VK 依進度檔重組原本完整指令，保留參數並依 POSIX shell 規則加引號
- `message.zh-TW`：&lt;install_dir&gt; 中的 &lt;operation&gt; 操作未完成。請再執行一次：&lt;original_command&gt;

#### VK0055

- `status`：active
- `level`：error
- `exit_code`：2
- `disposition`：failed
- `source`：<mark style="background-color:#c8f0c8">engine</mark> <mark style="background-color:#c8f0c8">（本欄新增）</mark>
- `situation.en`：<mark style="background-color:#f8c8c8">A network, registry, or authentication error (including timeout) occurs while update, add, upgrade, or sync lists tags or obtains a tool image; missing registry credentials for listing versions still report VK0001; update does not report up-to-date from a stale cache and does not prompt for authentication</mark> → <mark style="background-color:#c8f0c8">A network, registry, or authentication error (including timeout) occurs while update, add, upgrade, or sync lists tags or obtains a tool image; this includes failure to read the file specified by --registry-token-file (missing, unreadable, or empty), or the registry rejecting the supplied token; a rejected token is not retried anonymously; listing versions when registry read access is required and --registry-token-file was not supplied still reports VK0001; update does not report up-to-date from a stale cache and does not prompt for authentication</mark>
- `message.en`：Cannot access &lt;source&gt; for &lt;target&gt;: &lt;reason&gt;. The requested operation did not complete.
- `situation.zh-TW`：<mark style="background-color:#f8c8c8">update、add、upgrade 或 sync 列 tag 或取得工具 image 時發生網路、registry 或認證錯誤（含逾時）；缺少列版本的 registry 憑證仍報 VK0001；update 不以舊快取回報已是最新版，不跳出認證詢問</mark> → <mark style="background-color:#c8f0c8">update、add、upgrade 或 sync 列 tag 或取得工具 image 時發生網路、registry 或認證錯誤（含逾時）；包括讀 --registry-token-file 指定的檔失敗（不存在、讀不到、空的），或 registry 拒絕帶入的 token；被拒後不改走匿名重試；列版本時 registry 要求讀取權限而沒有帶 --registry-token-file 仍報 VK0001；update 不以舊快取回報已是最新版，不跳出認證詢問</mark>
- `message.zh-TW`：無法存取 &lt;target&gt; 的 &lt;source&gt;：&lt;reason&gt;。要求的操作未完成。

#### VK0056
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">bootstrap engine launcher test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">VK encounters an internal error, including an event name absent from the event registry; this is a VK bug</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Internal vendor_kit error: &lt;reason&gt;. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log &lt;path&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">VK 發生內部錯誤，包括事件名未登錄於事件註冊表；這是 VK 的 bug</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">vendor_kit 內部錯誤：&lt;reason&gt;。這是 VK 的 bug。請到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，並附上執行紀錄 &lt;path&gt;。</mark>

#### VK0057
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">add vendor_kit is requested; vendor_kit is a reserved tool name; &lt;repo&gt; = vendor_kit is checked before namespace collisions; VK0030 is not reported</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot add vendor_kit: vendor_kit is a reserved name. Use a different tool name.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">執行 add vendor_kit；vendor_kit 是保留的工具名稱；&lt;repo&gt; 為 vendor_kit 時先判定，不報 VK0030</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法 add vendor_kit：vendor_kit 是保留名稱。請使用其他工具名稱。</mark>

#### VK0058
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">update finds tags in the registry for the queried tool or engine, but none is a valid vX.Y.Z tag; the corresponding result line prints latest: none</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot determine the latest version of &lt;repo&gt;: the registry has tags, but none is a valid vX.Y.Z tag. The query did not complete.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">update 查到 registry 有所查工具或引擎的 tag，但沒有合法的 vX.Y.Z tag；對應結果行印 latest: none</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法判定 &lt;repo&gt; 的最新版本：registry 有 tag，但沒有合法的 vX.Y.Z tag。查詢未完成。</mark>

#### VK0059
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">engine test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">A value in .vendor_kit/config.toml is invalid: lock_timeout_seconds must be an integer greater than or equal to -1, lock_enabled must be a boolean, and [test].image must be a nonempty string and [test].command a nonempty array of nonempty strings; test &lt;path&gt; also reports this code when [test] or a required field is missing; all entry points, including rescue paths and the engine invoked by bootstrap.sh, stop; &lt;field&gt; names the field, &lt;value&gt; prints the invalid value or missing, and &lt;fix&gt; gives the required correction</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Invalid configuration in .vendor_kit/config.toml: &lt;field&gt; = &lt;value&gt;. The requested operation did not complete. Fix &lt;field&gt;: &lt;fix&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">.vendor_kit/config.toml 的設定值無效：lock_timeout_seconds 必須是大於等於 -1 的整數，lock_enabled 必須是布林值，[test].image 必須是非空字串，[test].command 必須是由非空字串組成的非空陣列；test &lt;path&gt; 缺少 [test] 或必要欄位也報此碼；所有入口（含救援路徑及 bootstrap.sh 帶出的引擎）一律停下；&lt;field&gt; 指名欄位，&lt;value&gt; 印錯誤值或 missing，&lt;fix&gt; 給出修法</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">.vendor_kit/config.toml 的設定無效：&lt;field&gt; = &lt;value&gt;。要求的操作未完成。請修正 &lt;field&gt;：&lt;fix&gt;。</mark>

#### VK0060
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark>
- `source`：<mark style="background-color:#c8f0c8">engine test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">lock_enabled = false in .vendor_kit/config.toml disables locking for a filesystem that does not support file locks; every execution reports this warning, including automatic sync and the engine invoked by bootstrap.sh</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Locking is disabled in &lt;install_dir&gt; by lock_enabled = false in .vendor_kit/config.toml. Concurrent executions are not protected by shared or exclusive locks. Use this setting only on filesystems without file lock support; otherwise set lock_enabled = true.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">.vendor_kit/config.toml 的 lock_enabled = false 關閉檔案鎖，只給不支援檔案鎖的檔案系統用；每次執行都印此警告，包括自動 sync 與 bootstrap.sh 帶出的引擎</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;install_dir&gt; 的 .vendor_kit/config.toml 設定 lock_enabled = false，已關閉檔案鎖。同時執行時沒有共享鎖或排他鎖保護。此設定只給不支援檔案鎖的檔案系統用；其他情況請設 lock_enabled = true。</mark>

#### VK0061
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">1</mark>
- `source`：<mark style="background-color:#c8f0c8">engine</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">remove or uninstall cannot reclaim inserted lines whenever the following condition is not met: the whole-file hash matches the hash recorded after VK last wrote the file and the original text occurs exactly once; failure cases include the hash differs, the record has no hash, or the original text occurs zero or multiple times; the lines are left untouched; the diagnostic lists the file, original text, and all currently matching line numbers (none when there are no matches)</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot reclaim inserted lines from &lt;file&gt;: the recorded whole-file hash is missing or differs from the current hash, or the original text does not occur exactly once. The lines were not removed. Handle them manually.<br>Original text: &lt;text&gt;<br>Currently matching line numbers: &lt;line_numbers&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">remove 或 uninstall 收回插入行時，不符合「整檔 hash 與 VK 上次寫入後記錄的 hash 相同，而且原文恰好一處」的所有情況：hash 不同、紀錄沒有 hash、原文零處或多處；這幾行不動；診斷列出檔名、原文與目前所有相符的行號（沒有相符行時印 none）</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法收回 &lt;file&gt; 的插入行：紀錄缺少整檔 hash、記錄的 hash 與目前不同，或原文不是恰好一處。這幾行未收回，請手動處理。<br>原文：&lt;text&gt;<br>目前相符的行號：&lt;line_numbers&gt;。</mark>

#### VK0062
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test &lt;path&gt; completes the full installation checks with a nonzero check exit code; no tests are started; the execution ends with max(check exit code, 2), so a check exit code of 3 is preserved in addition to this error/2 diagnostic</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Installation checks returned &lt;check_exit_code&gt;. No tests were started for &lt;path&gt;. Resolve the check diagnostics and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test &lt;path&gt; 的完整安裝檢查結束碼不是 0；測試沒跑；整次以 max(檢查碼, 2) 結束，因此檢查碼為 3 時，除了此 error/2 診斷仍保留整次的結束碼 3</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">安裝檢查回傳 &lt;check_exit_code&gt;。&lt;path&gt; 的測試沒跑。請處理檢查診斷後重試。</mark>

#### VK0063
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The path selected by test or any selected file is invalid or outside the install directory's test/ after resolving symbolic links, points into .vendor_kit/, or does not use the test/... form; directories include subdirectories; no tests are started</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Invalid test path &lt;path&gt;: &lt;reason&gt;. No tests were started. Specify one file or directory under the install directory's test/ and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test 選取路徑或任一選取檔無效、解析符號連結後不在安裝目錄的 test/ 內、指到 .vendor_kit/，或沒有寫成 test/...；資料夾包含子資料夾；整次測試不跑</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">測試路徑 &lt;path&gt; 無效：&lt;reason&gt;。整次測試沒跑。請指定安裝目錄 test/ 內的一個檔案或資料夾後重試。</mark>

#### VK0064
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The scope selected by test &lt;path&gt; includes a test recorded by VK as delivered by a tool, whether as a whole initial file or inserted lines; user edits do not remove that attribution; no tests in the selected scope are started</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot run &lt;path&gt;: VK recorded this test as delivered by tool &lt;repo&gt;. No tests were started. Select a scope containing only user-maintained tests that were not delivered by tools.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test &lt;path&gt; 選取範圍含 VK 紀錄為工具交付的測試（整份初始檔或插入行）；使用者改過也算；選取範圍的整次測試不跑</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法執行 &lt;path&gt;：VK 紀錄此測試由工具 &lt;repo&gt; 交付。整次測試沒跑。請選擇只含使用者維護、且不是工具交付測試的範圍。</mark>

#### VK0065
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">test &lt;path&gt; selects no tests; the runner is not started</mark>
- `message.en`：<mark style="background-color:#c8f0c8">No tests were selected under &lt;path&gt;. No tests were started. Specify a path containing tests and retry.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test &lt;path&gt; 沒選到任何測試；runner 不啟動</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;path&gt; 內沒選到任何測試。測試沒跑。請指定含測試的路徑後重試。</mark>

#### VK0066
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The runner for test &lt;path&gt; cannot be started or is stopped by VK (for example, when VK receives an interruption); any available original runner exit code is printed on a diagnostic continuation line, or unavailable if no runner exit code exists</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Cannot complete the test runner for &lt;path&gt;: &lt;reason&gt;. Check the test image and command in .vendor_kit/config.toml and retry.<br>Runner exit code: &lt;runner_exit_code&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test &lt;path&gt; 的 runner 無法啟動，或被 VK 停止（例如 VK 收到中斷）；runner 原始結束碼印在診斷續行，沒有 runner 結束碼時印 unavailable</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">無法完成 &lt;path&gt; 的測試 runner：&lt;reason&gt;。請檢查 .vendor_kit/config.toml 的測試 image 與 command 後重試。<br>Runner 結束碼：&lt;runner_exit_code&gt;。</mark>

#### VK0067
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `exit_code`：<mark style="background-color:#c8f0c8">2</mark>
- `disposition`：<mark style="background-color:#c8f0c8">failed</mark>
- `source`：<mark style="background-color:#c8f0c8">test</mark>
- `situation.en`：<mark style="background-color:#c8f0c8">The runner for test &lt;path&gt; ends on its own with a nonzero exit code (including codes greater than 128); VK exits with 2 and prints the original runner exit code on a diagnostic continuation line</mark>
- `message.en`：<mark style="background-color:#c8f0c8">Tests failed for &lt;path&gt;. Review the runner output, fix the failing tests, and retry.<br>Runner exit code: &lt;runner_exit_code&gt;.</mark>
- `situation.zh-TW`：<mark style="background-color:#c8f0c8">test &lt;path&gt; 的 runner 自行結束且結束碼非 0（含大於 128 的碼）；VK 以 2 結束，runner 原始結束碼印在診斷續行</mark>
- `message.zh-TW`：<mark style="background-color:#c8f0c8">&lt;path&gt; 的測試失敗。請查看 runner 輸出、修正失敗的測試後重試。<br>Runner 結束碼：&lt;runner_exit_code&gt;。</mark>

沒改動的代碼 2 個：VK0003、VK0022。
