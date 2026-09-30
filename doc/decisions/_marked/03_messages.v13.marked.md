<!-- 標示版 v13：綠底 <mark> 是新增、紅底 <mark> 是刪除；底線 <ins> 是名詞標記；本檔只供本地 review，不進 git；基準 base_b4f3627。正式內容看 /doc/contract/03_messages.md 與 /doc/contract/03_messages.csv -->

# 03 訊息與錯誤碼總表

這一頁列出 <ins>VK</ins> 每個<ins>結束碼</ins>的意思，以及每條<ins>診斷</ins>的固定格式。結束碼是契約，依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)。

- 名詞見[名詞表](../../../GLOSSARY.md)

## 目錄

- [結束碼](#結束碼)
- [輸出](#輸出)
- [訊息](#訊息)

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：

| 結束碼 | <ins>level</ins> | 意思 |
|---|---|---|
| `0` | info | 成功；沒有任何警告，也沒有要人接手的事項 |
| <mark style="background-color:#f8c8c8">`1`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">有<ins>警告</ins>，或做完但要人接手，例如留下<ins>合併衝突</ins>、`update --exit-code` 查到新版</mark> |
| <mark style="background-color:#c8f0c8">`1`</mark> | <mark style="background-color:#c8f0c8">warn</mark> | <mark style="background-color:#c8f0c8">有<ins>警告</ins>，或做完但要人接手；見表下的結束碼 `1`</mark> |
| `2` | error | 沒做完：<ins>需人處理</ins>、<ins>失敗</ins>或用法錯誤 |
| <mark style="background-color:#f8c8c8">`3`</mark> | <mark style="background-color:#f8c8c8">fatal</mark> | <mark style="background-color:#f8c8c8">只限現有<ins>薄殼</ins>、檔案、<ins>引擎</ins>的版本組合不合。以這個碼結束的那次執行不動 <ins>repo 檔</ins>與 <ins>VK 檔</ins>，執行紀錄除外</mark> |
| <mark style="background-color:#c8f0c8">`3`</mark> | <mark style="background-color:#c8f0c8">fatal</mark> | <mark style="background-color:#c8f0c8">只限現有<ins>薄殼</ins>、<ins>VK 檔</ins>、<ins>引擎</ins>的版本組合不合。以這個碼結束的那次執行不動 <ins>repo 檔</ins>與 VK 檔，執行紀錄除外</mark> |

<mark style="background-color:#c8f0c8">結束碼 `1` 有兩種：</mark>

- <mark style="background-color:#c8f0c8">有警告</mark>
- <mark style="background-color:#c8f0c8">做完但要人接手（不算警告）：留下<ins>合併衝突</ins>、`update --exit-code` 查到新版</mark>

只有警告也以 `1` 結束。本機與 CI 使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。

一次處理多個工具時：

- <mark style="background-color:#f8c8c8">結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新（`0`）、B 查到新版（`1`）、C 查詢失敗（`2`），就以 `2` 結束</mark>
- <mark style="background-color:#c8f0c8">結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新 (`0`)、B 查到新版 (`1`)、C 查詢失敗 (`2`)，就以 `2` 結束</mark>
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

<mark style="background-color:#c8f0c8">沿用 A、B、C 的例子，三個工具都會印出結果。以下是輸出示意：</mark>

<mark style="background-color:#c8f0c8">```text</mark>
<mark style="background-color:#c8f0c8">stdout: A 已是最新。</mark>
<mark style="background-color:#c8f0c8">stdout: B 有新版 v1.3.0（目前為 v1.2.0）。</mark>
<mark style="background-color:#c8f0c8">stderr: vendor_kit: warn[VK0022]: B 有新版：目前為 v1.2.0，新版為 v1.3.0。可執行：just vendor_kit upgrade B</mark>
<mark style="background-color:#c8f0c8">stderr: vendor_kit: error[VK0001]: 無法列舉 C 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade C@<tag>（拉取使用主機 docker 認證）</mark>
<mark style="background-color:#c8f0c8">exit code: 2</mark>
<mark style="background-color:#c8f0c8">```</mark>

## 輸出

- 成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴
- stderr 只放診斷及其續行、<ins>詢問</ins>文字、不帶指令時第一行的版本行，以及用法錯誤後附的用法
- 只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以 `2` 結束
- <mark style="background-color:#c8f0c8">主機前置檢查（檢查主機的 just 與 Docker）排在建執行紀錄之前；沒通過時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷</mark>
- `remove`／`uninstall` 依契約保留初始檔時，把保留清單印到 stdout，以 `0` 結束
- 詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - <mark style="background-color:#f8c8c8">只在那個輸出串流是終端（TTY）時上色；stdout 與 stderr 各自判斷</mark>
  - <mark style="background-color:#f8c8c8">環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色（[NO_COLOR](https://no-color.org/)）</mark>
  - <mark style="background-color:#c8f0c8">只在那個輸出串流是終端 (TTY) 時上色；stdout 與 stderr 各自判斷</mark>
  - <mark style="background-color:#c8f0c8">環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色 ([NO_COLOR](https://no-color.org/))</mark>
  - 給程式讀的輸出永遠不含顏色，例如<ins>執行紀錄</ins>
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <中文本文>`。診斷的 level 只有 `warn`、`error`、`fatal`；`info` 只用來標結束碼 `0`，不印前綴。多行診斷的續行也印到 stderr。

<mark style="background-color:#f8c8c8"><ins>原因代碼</ins>是 `VK` 加四位數字。每個代碼以表格的「情況」為唯一意思；發出後永不重用，刪掉的代碼留空號。</mark>
<mark style="background-color:#c8f0c8"><ins>原因代碼</ins>是 `VK` 加四位數字。每個代碼以訊息表的 `situation` 欄為唯一意思；發出後永不重用。停用的代碼不刪列，`status` 改成 `retired`，留作空號。</mark>

<mark style="background-color:#f8c8c8">表格怎麼讀：</mark>
<mark style="background-color:#c8f0c8">每個代碼的 level、處置、情況、本文與下一步，只寫在[訊息表](../../contract/03_messages.csv)，一列一個代碼；本頁不再列一份。</mark>

- <mark style="background-color:#f8c8c8">「訊息本文」欄只有反引號內是本文，逐字照印；反引號外的文字不印出。多行診斷寫成「第一行 `…`；第二行 `…`」</mark>
- <mark style="background-color:#f8c8c8">`<…>` 是占位符。除表格後方的註另有說明外，VK 印出時換成實際的值；註明原樣印出的占位符由使用者自行換成要用的值</mark>
- <mark style="background-color:#f8c8c8">「處置」是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令；失敗只說明原因；不屬於兩者的標「—」</mark>
- <mark style="background-color:#f8c8c8">「下一步」欄是診斷裡可以直接複製來執行的指令；沒有指令的標「—」</mark>
<mark style="background-color:#c8f0c8">處置與下一步：</mark>

- <mark style="background-color:#c8f0c8">處置是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令（不用使用者代換的單一指令）；失敗不承諾可執行的修法，但可以附一般建議；不屬於兩者的留空</mark>
- warn 要指名對象；有辦法處置就列出下一步

| <mark style="background-color:#f8c8c8">代碼</mark> | <mark style="background-color:#f8c8c8">level</mark> | <mark style="background-color:#f8c8c8">處置</mark> | <mark style="background-color:#f8c8c8">情況</mark> | <mark style="background-color:#f8c8c8">訊息本文</mark> | <mark style="background-color:#f8c8c8">下一步</mark> |
|---|---|---|---|---|---|
| <mark style="background-color:#f8c8c8">`VK0001`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">`update`、`upgrade`、`add` 列版本時沒有 <ins>registry</ins> 憑證</mark> | <mark style="background-color:#f8c8c8">`無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit <指令> <repo>@<tag>（拉取使用主機 docker 認證）`</mark> | <mark style="background-color:#f8c8c8">`add` 時是 `just vendor_kit add <repo>@<tag>`；`update`、`upgrade` 時是 `just vendor_kit upgrade <repo>@<tag>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0002`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">操作需要詢問，但沒帶 `-y` 又不能互動（沒有終端，或讀到輸入結束）</mark> | <mark style="background-color:#f8c8c8">`需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：<加上 -y 的原指令>`</mark> | <mark style="background-color:#f8c8c8">`<加上 -y 的原指令>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0003`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8"><ins>CI 模式</ins>下，<ins>基準版</ins>落後<ins>版本鎖定行</ins></mark> | <mark style="background-color:#f8c8c8">`請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade <repo> -y`</mark> |
| <mark style="background-color:#f8c8c8">`VK0004`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">`sync` 發現某個工具未完成<ins>導入</ins></mark> | <mark style="background-color:#f8c8c8">`<repo> 未完成導入，請執行：just vendor_kit add <repo>`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit add <repo>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0005`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">`bootstrap.sh` 發現主機的 just 低於 1.33.0</mark> | <mark style="background-color:#f8c8c8">第一行 `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。`；第二行 `下載：<平台對應的下載網址>`；第三行 `安裝：<安裝指令>`</mark> | <mark style="background-color:#f8c8c8">訊息第三行的 `<安裝指令>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0006`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）</mark> | <mark style="background-color:#f8c8c8">`偵測到薄殼跟這一版引擎的模板不符：<files>。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade --engine`</mark> |
| <mark style="background-color:#f8c8c8">`VK0007`</mark> | <mark style="background-color:#f8c8c8">fatal</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">`upgrade --engine=<tag>` 降版，但目標引擎無法無損讀取現有的 VK 檔</mark> | <mark style="background-color:#f8c8c8">`目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 <N> 的版本：just vendor_kit upgrade --engine=<tag>`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade --engine=<tag>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0008`</mark> | <mark style="background-color:#f8c8c8">fatal</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">引擎讀到的 VK 檔，<ins>檔案版</ins>高於這個引擎支援的上限</mark> | <mark style="background-color:#f8c8c8">`無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請升級引擎：just vendor_kit upgrade --engine`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade --engine`</mark> |
| <mark style="background-color:#f8c8c8">`VK0009`</mark> | <mark style="background-color:#f8c8c8">fatal</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">舊的薄殼遇上 X 較新的引擎，執行<ins>救援路徑</ins>以外的 recipe</mark> | <mark style="background-color:#f8c8c8">`薄殼介面版 <P_shell> 低於引擎 <vY> 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade --engine`</mark> |
| <mark style="background-color:#f8c8c8">`VK0010`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">建不出執行紀錄</mark> | <mark style="background-color:#f8c8c8">`無法寫入執行紀錄 <path>：<原因>。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0011`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">`docker --version` 的輸出含 `podman`</mark> | <mark style="background-color:#f8c8c8">`偵測到 podman（docker --version）。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0012`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">啟動器發現主機的 Docker 低於 19.03</mark> | <mark style="background-color:#f8c8c8">`需要 Docker ≥ 19.03，目前為 <version>。請升級 Docker 後重試。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0013`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8"><ins>metadata</ins> 缺失或損壞，無法可靠還原</mark> | <mark style="background-color:#f8c8c8">`無法處理 <file>：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 <file> 與執行紀錄 <path>；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0014`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">本機執行 `sync`，發現基準版落後版本鎖定行</mark> | <mark style="background-color:#f8c8c8">`<repo> 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade <repo> -y`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade <repo> -y`</mark> |
| <mark style="background-color:#f8c8c8">`VK0015`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">`sync` 發現 `cache/` 的逐檔指紋不符，已重新取件</mark> | <mark style="background-color:#f8c8c8">`<repo> 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0016`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">收回 append 行時，在檔內找不到當初插入的原文</mark> | <mark style="background-color:#f8c8c8">`<file> 找不到要收回的原文；未刪除該行，請手動檢查。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0017`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">收回 append 行時，在檔內找到多處與當初插入的原文相同</mark> | <mark style="background-color:#f8c8c8">`<file> 找到 <count> 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0018`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">`add` 遇到已存在、尚未納管的檔</mark> | <mark style="background-color:#f8c8c8">`<file> 已存在且未納管；未覆蓋，也未納管這個檔。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0019`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">檔案沒有納管，本次不處理</mark> | <mark style="background-color:#f8c8c8">`<file> 沒有納管；本次未處理這個檔。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0020`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">這個版本先前已由使用者拒絕</mark> | <mark style="background-color:#f8c8c8">`<repo> 的版本 <tag> 先前已被拒絕；本次不再詢問，也未套用。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0021`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">基準版合併留下合併衝突</mark> | <mark style="background-color:#f8c8c8">`<file> 留下合併衝突，請檢視後解決：git status`</mark> | <mark style="background-color:#f8c8c8">`git status`</mark> |
| <mark style="background-color:#f8c8c8">`VK0022`</mark> | <mark style="background-color:#f8c8c8">warn</mark> | <mark style="background-color:#f8c8c8">—</mark> | <mark style="background-color:#f8c8c8">`update --exit-code` 查到新版</mark> | <mark style="background-color:#f8c8c8">`<repo> 有新版：目前為 <current_tag>，新版為 <new_tag>。可執行：just vendor_kit upgrade <repo>`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade <repo>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0023`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">`upgrade --engine` 換上新引擎後停下，要求重跑</mark> | <mark style="background-color:#f8c8c8">`已換上引擎 <vY>，請再執行一次：just vendor_kit upgrade --engine`</mark> | <mark style="background-color:#f8c8c8">`just vendor_kit upgrade --engine`</mark> |
| <mark style="background-color:#f8c8c8">`VK0024`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">只打 `just vendor_kit`、未指定指令</mark> | <mark style="background-color:#f8c8c8">`未指定指令。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0025`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">缺少必要參數</mark> | <mark style="background-color:#f8c8c8">`缺少必要參數：<參數>。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0026`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">不認得指令或選項</mark> | <mark style="background-color:#f8c8c8">`不認得的指令或選項：<值>。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0027`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">tag 格式不合</mark> | <mark style="background-color:#f8c8c8">`tag 格式不合：<tag>；只接受 vX.Y.Z，X、Y、Z 不收前導零。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0028`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">在安裝目錄外執行 VK recipe</mark> | <mark style="background-color:#f8c8c8">`目前不在安裝目錄，請執行：cd <install_dir>`</mark> | <mark style="background-color:#f8c8c8">`cd <install_dir>`</mark> |
| <mark style="background-color:#f8c8c8">`VK0029`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">`install` 時上層或下層已有安裝目錄</mark> | <mark style="background-color:#f8c8c8">`不能建立巢狀安裝目錄：<existing_install_dir> 已是安裝目錄。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0030`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">`add` 時 `<ns>` 撞名</mark> | <mark style="background-color:#f8c8c8">`無法加入 <repo>：命名空間 <ns> 已由 <owner> 使用。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0031`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">失敗</mark> | <mark style="background-color:#f8c8c8">離線導入的 image 缺少必要的 digest 資訊</mark> | <mark style="background-color:#f8c8c8">`無法從 <image> 導入：缺少必要的 digest 資訊。`</mark> | <mark style="background-color:#f8c8c8">—</mark> |
| <mark style="background-color:#f8c8c8">`VK0032`</mark> | <mark style="background-color:#f8c8c8">error</mark> | <mark style="background-color:#f8c8c8">需人處理</mark> | <mark style="background-color:#f8c8c8">CI 模式發現本機覆寫</mark> | <mark style="background-color:#f8c8c8">`CI 模式不能使用 <target> 的本機覆寫，請在本機執行：<解除本機覆寫的指令>`</mark> | <mark style="background-color:#f8c8c8">`<解除本機覆寫的指令>`</mark> |
<mark style="background-color:#c8f0c8">訊息表怎麼讀：</mark>

<mark style="background-color:#f8c8c8">註：</mark>
- <mark style="background-color:#f8c8c8">`VK0001`：`<指令>` 依觸發的指令而定，`add` 時是 `add`，`update`、`upgrade` 時是 `upgrade`；`<tag>` 原樣印出，由使用者換成要安裝的版本 tag，例如 `v1.2.3`</mark>
- <mark style="background-color:#f8c8c8">`VK0002`：一律不改；依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)。`<加上 -y 的原指令>` 由這次執行的參數逐項重組，每一項依 POSIX shell 的規則加引號，`-y` 插在單獨的 `--` 之前；沒有 `--` 時放在最後。不在原指令字串尾端直接接 `-y`</mark>
- <mark style="background-color:#f8c8c8">`VK0003`、`VK0004`：依 [02 不變量第 3 條](../../contract/02_invariants.md#3-自動化只碰不進-git-的東西)</mark>
- <mark style="background-color:#f8c8c8">`VK0005`：這是主機前置檢查，排在建執行紀錄之前；失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。依 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)。`<安裝指令>` 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark>
- <mark style="background-color:#f8c8c8">`VK0006`：`<files>` 逐檔標出是哪一種；不重產薄殼；除執行紀錄外，不動 repo 檔與其他 VK 檔。依 [02 不變量第 6 條](../../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)</mark>
- <mark style="background-color:#f8c8c8">`VK0007`～`VK0009`：除執行紀錄外，在任何寫入之前結束，不動 repo 檔與 VK 檔；依 [02 不變量第 10 條](../../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。`VK0007` 的 `<tag>` 原樣印出，由使用者換成能讀取檔案版 `<N>` 的引擎版本 tag；`VK0009` 的救援路徑以外 recipe，其 `-h`／`--help` 在版本組合不合時怎麼反應，本頁不定</mark>
- <mark style="background-color:#f8c8c8">`VK0010`：在任何副作用之前結束，所有 VK recipe 都一樣；依 [02 不變量第 4 條](../../contract/02_invariants.md#4-永不靜默失敗)</mark>
- <mark style="background-color:#f8c8c8">`VK0011`、`VK0012`：是主機前置檢查，排在建執行紀錄之前；失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。依 [02 不變量第 5 條](../../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)</mark>
- <mark style="background-color:#f8c8c8">`VK0013`：不猜測；除執行紀錄外，不寫 repo 檔與其他 VK 檔；依 [02 不變量第 1 條](../../contract/02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)</mark>
- <mark style="background-color:#f8c8c8">`VK0024`：輸出順序見[輸出](#輸出)。</mark>
- <mark style="background-color:#f8c8c8">`VK0032`：`<解除本機覆寫的指令>` 依對象印成 `just vendor_kit undev <repo>` 或 `just vendor_kit undev --engine`</mark>
- <mark style="background-color:#c8f0c8">格式</mark>
  - <mark style="background-color:#c8f0c8">UTF-8 加 BOM、LF 換行、逗號分隔，照 RFC 4180 加引號</mark>
  - <mark style="background-color:#c8f0c8">儲存格裡沒有 HTML 與 Markdown，寫的就是要印的字</mark>
- <mark style="background-color:#c8f0c8">欄位</mark>
  - <mark style="background-color:#c8f0c8">`code`：原因代碼，從 `VK0001` 起逐列加一，不缺列</mark>
  - <mark style="background-color:#c8f0c8">`status`：`active` 使用中；`retired` 已停用，只留 `code`、`status`、`situation`</mark>
  - <mark style="background-color:#c8f0c8">`level`：`warn`、`error`、`fatal`，對應的結束碼見[結束碼](#結束碼)</mark>
  - <mark style="background-color:#c8f0c8">`disposition`：處置，`需人處理`、`失敗` 或留空；`warn` 一律留空</mark>
  - <mark style="background-color:#c8f0c8">`situation`：什麼情況發出這個代碼，是它唯一的意思</mark>
  - <mark style="background-color:#c8f0c8">`message`：本文，逐字照印，不含前綴；多行診斷在同一格內換行，一行對應印出的一行</mark>
  - <mark style="background-color:#c8f0c8">`next_step`：可以直接複製執行的單一指令，逐字出現在 `message` 裡，占位符都由 VK 換成實際的值；需人處理必填，失敗與沒有指令的留空；做不到的診斷標失敗</mark>
- <mark style="background-color:#c8f0c8">占位符</mark>
  - <mark style="background-color:#c8f0c8">`<…>` 是占位符，VK 印出時換成實際的值</mark>
  - <mark style="background-color:#c8f0c8">`situation` 註明原樣印出的，由使用者換成要用的值</mark>
- <mark style="background-color:#c8f0c8">查看</mark>
  - <mark style="background-color:#c8f0c8">GitHub 上看是表格，搜尋框只能全文篩列</mark>
  - <mark style="background-color:#c8f0c8">要依 level 或處置篩選，用 Excel 開或請 agent 查；Excel 只看不存回，另存會改掉換行與引號</mark>

---

## 03_messages.csv 的逐碼差異

依 code 對齊、逐欄比較，只列有改動的代碼；綠底是新值、紅底是舊值，沒改的欄照原樣列出。

- 表頭：<mark style="background-color:#f8c8c8">code,status,level,disposition,situation,message,next_step,note,invariant,details</mark> → <mark style="background-color:#c8f0c8">code,status,level,disposition,situation,message,next_step</mark>
- `note`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `invariant`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>
- `details`：<mark style="background-color:#f8c8c8">（本欄刪除）</mark>

#### VK0001
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">update、upgrade、add 列版本時沒有 registry 憑證；&lt;指令&gt; 在 add 時印 add，update、upgrade 時印 upgrade，&lt;tag&gt; 原樣印出，由使用者換成要安裝的版本 tag</mark>
- `message`：<mark style="background-color:#c8f0c8">無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit &lt;指令&gt; &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）</mark>

#### VK0002
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">操作需要詢問，但沒帶 -y 又不能互動（沒有終端，或讀到輸入結束）；&lt;加上 -y 的原指令&gt; 由這次執行的參數逐項重組、每項依 POSIX shell 的規則加引號，-y 插在單獨的 -- 之前，沒有 -- 時放在最後</mark>
- `message`：<mark style="background-color:#c8f0c8">需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：&lt;加上 -y 的原指令&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">&lt;加上 -y 的原指令&gt;</mark>

#### VK0003
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">CI 模式下，基準版落後版本鎖定行</mark>
- `message`：<mark style="background-color:#c8f0c8">請在本機執行 just vendor_kit upgrade &lt;repo&gt; -y 後 commit 並 push</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade &lt;repo&gt; -y</mark>

#### VK0004
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">sync 發現某個工具未完成導入</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 未完成導入，請執行：just vendor_kit add &lt;repo&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit add &lt;repo&gt;</mark>

#### VK0005
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">bootstrap.sh 發現主機的 just 低於 1.33.0；&lt;安裝指令&gt; 不覆蓋主機既有的 just，也不要求主機另裝其他工具</mark>
- `message`：<mark style="background-color:#c8f0c8">需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。<br>下載：&lt;平台對應的下載網址&gt;<br>安裝：&lt;安裝指令&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">&lt;安裝指令&gt;</mark>

#### VK0006
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板）；&lt;files&gt; 逐檔標出是哪一種，除執行紀錄外不動 repo 檔與其他 VK 檔</mark>
- `message`：<mark style="background-color:#c8f0c8">偵測到薄殼跟這一版引擎的模板不符：&lt;files&gt;。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine</mark>

#### VK0007
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">upgrade --engine=&lt;tag&gt; 降版，但目標引擎無法無損讀取現有的 VK 檔；本文的 &lt;tag&gt; 原樣印出，由使用者換成能讀取檔案版 &lt;N&gt; 的引擎版本 tag</mark>
- `message`：<mark style="background-color:#c8f0c8">目標引擎 &lt;vY&gt;（介面版 &lt;P&gt;、檔案版 &lt;M&gt;）無法無損讀取現有檔（檔案版 &lt;N&gt;）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 &lt;N&gt; 的版本：just vendor_kit upgrade --engine=&lt;tag&gt;</mark>

#### VK0008
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">引擎讀到的 VK 檔，檔案版高於這個引擎支援的上限</mark>
- `message`：<mark style="background-color:#c8f0c8">無法讀取 &lt;file&gt;：檔案版 &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請升級引擎：just vendor_kit upgrade --engine</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade --engine</mark>

#### VK0009
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">fatal</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">舊的薄殼遇上 X 較新的引擎，執行救援路徑以外的 recipe</mark>
- `message`：<mark style="background-color:#c8f0c8">薄殼介面版 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade --engine</mark>

#### VK0010
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">任何 VK recipe 建不出執行紀錄（在任何副作用之前結束）</mark>
- `message`：<mark style="background-color:#c8f0c8">無法寫入執行紀錄 &lt;path&gt;：&lt;原因&gt;。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。</mark>

#### VK0011
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">docker --version 的輸出含 podman</mark>
- `message`：<mark style="background-color:#c8f0c8">偵測到 podman (docker --version)。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。</mark>

#### VK0012
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">啟動器發現主機的 Docker 低於 19.03</mark>
- `message`：<mark style="background-color:#c8f0c8">需要 Docker ≥ 19.03，目前為 &lt;version&gt;。請升級 Docker 後重試。</mark>

#### VK0013
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">metadata 缺失或損壞，無法可靠還原</mark>
- `message`：<mark style="background-color:#c8f0c8">無法處理 &lt;file&gt;：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 &lt;file&gt; 與執行紀錄 &lt;path&gt;；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。</mark>

#### VK0014
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">本機執行 sync，發現基準版落後版本鎖定行</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade &lt;repo&gt; -y</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade &lt;repo&gt; -y</mark>

#### VK0015
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">sync 發現 cache/ 的逐檔指紋不符，已重新取件</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。</mark>

#### VK0016
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">收回 append 行時，在檔內找不到當初插入的原文</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;file&gt; 找不到要收回的原文；未刪除該行，請手動檢查。</mark>

#### VK0017
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">收回 append 行時，在檔內找到多處與當初插入的原文相同</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;file&gt; 找到 &lt;count&gt; 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。</mark>

#### VK0018
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">add 遇到已存在、尚未納管的檔</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;file&gt; 已存在且未納管；未覆蓋，也未納管這個檔。</mark>

#### VK0019
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">檔案沒有納管，本次不處理</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;file&gt; 沒有納管；本次未處理這個檔。</mark>

#### VK0020
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">這個版本先前已由使用者拒絕</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 的版本 &lt;tag&gt; 先前已被拒絕；本次不再詢問，也未套用。</mark>

#### VK0021
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">基準版合併留下合併衝突</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;file&gt; 留下合併衝突，請檢視後解決：git status</mark>
- `next_step`：<mark style="background-color:#c8f0c8">git status</mark>

#### VK0022
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">warn</mark>
- `situation`：<mark style="background-color:#c8f0c8">update --exit-code 查到新版</mark>
- `message`：<mark style="background-color:#c8f0c8">&lt;repo&gt; 有新版：目前為 &lt;current_tag&gt;，新版為 &lt;new_tag&gt;。可執行：just vendor_kit upgrade &lt;repo&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade &lt;repo&gt;</mark>

#### VK0023
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">upgrade --engine 換上新引擎後停下，要求重跑</mark>
- `message`：<mark style="background-color:#c8f0c8">已換上引擎 &lt;vY&gt;，請再執行一次：just vendor_kit upgrade --engine</mark>
- `next_step`：<mark style="background-color:#c8f0c8">just vendor_kit upgrade --engine</mark>

#### VK0024
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `situation`：<mark style="background-color:#c8f0c8">用法錯誤：只打 just vendor_kit、未指定指令</mark>
- `message`：<mark style="background-color:#c8f0c8">未指定指令。</mark>

#### VK0025
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `situation`：<mark style="background-color:#c8f0c8">用法錯誤：缺少必要參數</mark>
- `message`：<mark style="background-color:#c8f0c8">缺少必要參數：&lt;參數&gt;。</mark>

#### VK0026
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `situation`：<mark style="background-color:#c8f0c8">用法錯誤：不認得指令或選項</mark>
- `message`：<mark style="background-color:#c8f0c8">不認得的指令或選項：&lt;值&gt;。</mark>

#### VK0027
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `situation`：<mark style="background-color:#c8f0c8">用法錯誤：tag 格式不合</mark>
- `message`：<mark style="background-color:#c8f0c8">tag 格式不合：&lt;tag&gt;；只接受 vX.Y.Z，X、Y、Z 不收前導零。</mark>

#### VK0028
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">在安裝目錄外執行 VK recipe</mark>
- `message`：<mark style="background-color:#c8f0c8">目前不在安裝目錄，請執行：cd &lt;install_dir&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">cd &lt;install_dir&gt;</mark>

#### VK0029
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">install 時上層或下層已有安裝目錄</mark>
- `message`：<mark style="background-color:#c8f0c8">不能建立巢狀安裝目錄：&lt;existing_install_dir&gt; 已是安裝目錄。</mark>

#### VK0030
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">add 時 &lt;ns&gt; 撞名</mark>
- `message`：<mark style="background-color:#c8f0c8">無法加入 &lt;repo&gt;：命名空間 &lt;ns&gt; 已由 &lt;owner&gt; 使用。</mark>

#### VK0031
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">失敗</mark>
- `situation`：<mark style="background-color:#c8f0c8">離線導入的 image 缺少必要的 digest 資訊</mark>
- `message`：<mark style="background-color:#c8f0c8">無法從 &lt;image&gt; 導入：缺少必要的 digest 資訊。</mark>

#### VK0032
<mark style="background-color:#c8f0c8">（本碼新增）</mark>

- `status`：<mark style="background-color:#c8f0c8">active</mark>
- `level`：<mark style="background-color:#c8f0c8">error</mark>
- `disposition`：<mark style="background-color:#c8f0c8">需人處理</mark>
- `situation`：<mark style="background-color:#c8f0c8">CI 模式發現本機覆寫；&lt;解除本機覆寫的指令&gt; 依對象印成 just vendor_kit undev &lt;repo&gt; 或 just vendor_kit undev --engine</mark>
- `message`：<mark style="background-color:#c8f0c8">CI 模式不能使用 &lt;target&gt; 的本機覆寫，請在本機執行：&lt;解除本機覆寫的指令&gt;</mark>
- `next_step`：<mark style="background-color:#c8f0c8">&lt;解除本機覆寫的指令&gt;</mark>

沒改動的代碼 0 個。
