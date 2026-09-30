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
| `1` | warn | 有<ins>警告</ins>，或做完但要人接手，例如留下<ins>合併衝突</ins>、`update --exit-code` 查到新版 |
| `2` | error | 沒做完：<ins>需人處理</ins>、<ins>失敗</ins>或用法錯誤 |
| `3` | fatal | 只限現有<ins>薄殼</ins>、檔案、<ins>引擎</ins>的版本組合不合。以這個碼結束的那次執行不動 <ins>repo 檔</ins>與 <ins>VK 檔</ins>，執行紀錄除外 |

只有警告也以 `1` 結束。本機與 CI 使用同一套規則。是否成功看有沒有做到該指令契約承諾的結果，不看訊息名稱或輸出串流。

一次處理多個工具時：

- 結束碼取各工具結果裡數字最大的那個，沒有特例。例如用 `update --exit-code` 一次查 A、B、C：A 已是最新（`0`）、B 查到新版（`1`）、C 查詢失敗（`2`），就以 `2` 結束
- 每個工具的結果仍然各自印出，不因為只回一個碼就省略

## 輸出

- 成功時改了什麼、查詢結果與各 recipe 的 `-h`／`--help` 用法只印到 stdout，不加前綴
- stderr 只放診斷及其續行、<ins>詢問</ins>文字，以及用法錯誤後附的用法
- 只打 `just vendor_kit`、不帶指令時，stderr 第一行印 `vendor_kit <版本>`，第二行印 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以 `2` 結束
- `remove`／`uninstall` 依契約保留初始檔時，把保留清單印到 stdout，以 `0` 結束
- 詢問時使用者明確回答「否」，是正常取消：不做變更，在 stdout 說明未變更，以 `0` 結束
- 顏色照這幾條：
  - 只在那個輸出串流是終端（TTY）時上色；stdout 與 stderr 各自判斷
  - 環境變數 `NO_COLOR` 有值且不是空字串時，一律不上色（[NO_COLOR](https://no-color.org/)）
  - 給程式讀的輸出永遠不含顏色，例如<ins>執行紀錄</ins>
  - 顏色只是輔助：去掉顏色後，本文一字不變

## 訊息

每條診斷都印到 stderr。第一行格式固定是 `vendor_kit: <level>[VKnnnn]: <中文本文>`；診斷的 level 只有 `warn`、`error`、`fatal`；info 只用來標結束碼 `0`，不印前綴。多行診斷的續行也印到 stderr。

<ins>原因代碼</ins>是 `VK` 加四位數字。每個代碼以表格的「情況」為唯一意思；發出後永不重用，刪掉的代碼留空號。

表格怎麼讀：

- 「訊息本文」欄只有反引號內是本文，逐字照印；反引號外的文字不印出。多行診斷寫成「第一行 `…`；第二行 `…`」
- `<…>` 是占位符。除表格後方的註另有說明外，VK 印出時換成實際的值；註明原樣印出的占位符由使用者自行換成要用的值
- 「處置」是診斷的屬性，不是 level。需人處理表示 VK 停下並要求使用者採取下一步，必須附可以直接複製的指令；失敗只說明原因；不屬於兩者的標「—」
- 「下一步」欄是診斷裡可以直接複製來執行的指令；沒有指令的標「—」
- warn 要指名對象；有辦法處置就列出下一步

| 代碼 | level | 處置 | 情況 | 訊息本文 | 下一步 |
|---|---|---|---|---|---|
| `VK0001` | error | 需人處理 | `update`、`upgrade`、`add` 列版本時沒有 <ins>registry</ins> 憑證 | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit <指令> <repo>@<tag>（拉取使用主機 docker 認證）` | `add` 時是 `just vendor_kit add <repo>@<tag>`；`update`、`upgrade` 時是 `just vendor_kit upgrade <repo>@<tag>` |
| `VK0002` | error | 需人處理 | 操作需要詢問，但沒帶 `-y` 又不能互動（沒有終端，或讀到輸入結束） | `需要確認，但沒有終端可以互動。除執行紀錄外，未修改任何檔。請在終端執行，或加上 -y 重新執行：<加上 -y 的原指令>` | `<加上 -y 的原指令>` |
| `VK0003` | error | 需人處理 | <ins>CI 模式</ins>下，<ins>基準版</ins>落後<ins>版本鎖定行</ins> | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push` | `just vendor_kit upgrade <repo> -y` |
| `VK0004` | error | 需人處理 | `sync` 發現某個工具未完成<ins>導入</ins> | `<repo> 未完成導入，請執行：just vendor_kit add <repo>` | `just vendor_kit add <repo>` |
| `VK0005` | error | 需人處理 | `bootstrap.sh` 發現主機的 just 低於 1.33.0 | 第一行 `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。`；第二行 `下載：<平台對應的下載網址>`；第三行 `安裝：<安裝指令>` | 訊息第三行的 `<安裝指令>` |
| `VK0006` | error | 需人處理 | 薄殼的檔跟這一版引擎的模板比對不符（內容被修改過，或不是這一版引擎的模板） | `偵測到薄殼跟這一版引擎的模板不符：<files>。未重產任何薄殼。請先檢視下列差異；手動修改過的先還原，再執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` |
| `VK0007` | fatal | 需人處理 | `upgrade --engine=<tag>` 降版，但目標引擎無法無損讀取現有的 VK 檔 | `目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。除執行紀錄外，未修改任何檔。請改指定能讀取檔案版 <N> 的版本：just vendor_kit upgrade --engine=<tag>` | `just vendor_kit upgrade --engine=<tag>` |
| `VK0008` | fatal | 需人處理 | 引擎讀到的 VK 檔，<ins>檔案版</ins>高於這個引擎支援的上限 | `無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請升級引擎：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` |
| `VK0009` | fatal | 需人處理 | 舊的薄殼遇上 X 較新的引擎，執行<ins>救援路徑</ins>以外的 recipe | `薄殼介面版 <P_shell> 低於引擎 <vY> 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` |
| `VK0010` | error | 失敗 | 建不出執行紀錄 | `無法寫入執行紀錄 <path>：<原因>。vendor_kit 不在沒有紀錄的情況下執行，未修改任何檔。請清出磁碟空間或修正權限後重試。` | — |
| `VK0011` | error | 失敗 | `docker --version` 的輸出含 `podman` | `偵測到 podman（docker --version）。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。` | — |
| `VK0012` | error | 失敗 | 啟動器發現主機的 Docker 低於 19.03 | `需要 Docker ≥ 19.03，目前為 <version>。請升級 Docker 後重試。` | — |
| `VK0013` | error | 失敗 | <ins>metadata</ins> 缺失或損壞，無法可靠還原 | `無法處理 <file>：metadata 缺失或損壞，無法可靠還原。vendor_kit 不以推測代替紀錄，除執行紀錄外，未修改任何檔。請先保留 <file> 與執行紀錄 <path>；metadata 若曾 commit 進 git，從 git 還原後重試；無法還原時，到 https://github.com/ycpss91255-research/vendor_kit/issues 回報，附上這兩個檔。` | — |
| `VK0014` | warn | — | 本機執行 `sync`，發現基準版落後版本鎖定行 | `<repo> 的基準版落後版本鎖定行。請執行：just vendor_kit upgrade <repo> -y` | `just vendor_kit upgrade <repo> -y` |
| `VK0015` | warn | — | `sync` 發現 `cache/` 的逐檔指紋不符，已重新取件 | `<repo> 的 cache/ 逐檔指紋不符，已依版本鎖定行重新取件。` | — |
| `VK0016` | warn | — | 收回 append 行時，在檔內找不到當初插入的原文 | `<file> 找不到要收回的原文；未刪除該行，請手動檢查。` | — |
| `VK0017` | warn | — | 收回 append 行時，在檔內找到多處與當初插入的原文相同 | `<file> 找到 <count> 處要收回的原文，無法唯一歸因；未刪除該行，請手動檢查。` | — |
| `VK0018` | warn | — | `add` 遇到已存在、尚未納管的檔 | `<file> 已存在且未納管；未覆蓋，也未納管這個檔。` | — |
| `VK0019` | warn | — | 檔案沒有納管，本次不處理 | `<file> 沒有納管；本次未處理這個檔。` | — |
| `VK0020` | warn | — | 這個版本先前已由使用者拒絕 | `<repo> 的版本 <tag> 先前已被拒絕；本次不再詢問，也未套用。` | — |
| `VK0021` | warn | — | 基準版合併留下合併衝突 | `<file> 留下合併衝突，請檢視後解決：git status` | `git status` |
| `VK0022` | warn | — | `update --exit-code` 查到新版 | `<repo> 有新版：目前為 <current_tag>，新版為 <new_tag>。可執行：just vendor_kit upgrade <repo>` | `just vendor_kit upgrade <repo>` |
| `VK0023` | error | 需人處理 | `upgrade --engine` 換上新引擎後停下，要求重跑 | `已換上引擎 <vY>，請再執行一次：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` |
| `VK0024` | error | 失敗 | 只打 `just vendor_kit`、未指定指令 | `未指定指令。` | — |
| `VK0025` | error | 失敗 | 缺少必要參數 | `缺少必要參數：<參數>。` | — |
| `VK0026` | error | 失敗 | 不認得指令或選項 | `不認得的指令或選項：<值>。` | — |
| `VK0027` | error | 失敗 | tag 格式不合 | `tag 格式不合：<tag>；只接受 vX.Y.Z，X、Y、Z 不收前導零。` | — |
| `VK0028` | error | 需人處理 | 在安裝目錄外執行 VK recipe | `目前不在安裝目錄，請執行：cd <install_dir>` | `cd <install_dir>` |
| `VK0029` | error | 失敗 | `install` 時上層或下層已有安裝目錄 | `不能建立巢狀安裝目錄：<existing_install_dir> 已是安裝目錄。` | — |
| `VK0030` | error | 失敗 | `add` 時 `<ns>` 撞名 | `無法加入 <repo>：命名空間 <ns> 已由 <owner> 使用。` | — |
| `VK0031` | error | 失敗 | 離線導入的 image 缺少必要的 digest 資訊 | `無法從 <image> 導入：缺少必要的 digest 資訊。` | — |
| `VK0032` | error | 需人處理 | CI 模式發現本機覆寫 | `CI 模式不能使用 <target> 的本機覆寫，請在本機執行：<解除本機覆寫的指令>` | `<解除本機覆寫的指令>` |

註：

- `VK0001`：`<指令>` 依觸發的指令而定，`add` 時是 `add`，`update`、`upgrade` 時是 `upgrade`；`<tag>` 原樣印出，由使用者換成要安裝的版本 tag，例如 `v1.2.3`
- `VK0002`：一律不改；依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)。`<加上 -y 的原指令>` 由這次執行的參數逐項重組，每一項依 POSIX shell 的規則加引號，`-y` 插在單獨的 `--` 之前；沒有 `--` 時放在最後。不在原指令字串尾端直接接 `-y`
- `VK0003`、`VK0004`：依 [02 不變量第 3 條](02_invariants.md#3-自動化只碰不進-git-的東西)
- `VK0005`：這是主機前置檢查，排在建執行紀錄之前；失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。依 [02 不變量第 5 條](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)。`<安裝指令>` 不覆蓋主機既有的 just，也不要求主機另裝其他工具
- `VK0006`：`<files>` 逐檔標出是哪一種；不重產薄殼；除執行紀錄外，不動 repo 檔與其他 VK 檔。依 [02 不變量第 6 條](02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)
- `VK0007`～`VK0009`：除執行紀錄外，在任何寫入之前結束，不動 repo 檔與 VK 檔；依 [02 不變量第 10 條](02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)。`VK0007` 的 `<tag>` 原樣印出，由使用者換成能讀取檔案版 `<N>` 的引擎版本 tag；`VK0009` 的救援路徑以外 recipe，其 `-h`／`--help` 在版本組合不合時怎麼反應，本頁不定
- `VK0010`：在任何副作用之前結束，所有 VK recipe 都一樣；依 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)
- `VK0011`、`VK0012`：是主機前置檢查，排在建執行紀錄之前；失敗時不建執行紀錄、不動任何 VK 檔，只在 stderr 印診斷。依 [02 不變量第 5 條](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)
- `VK0013`：不猜測；除執行紀錄外，不寫 repo 檔與其他 VK 檔；依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)
- `VK0024`：stderr 第一行先印 `vendor_kit <版本>`，第二行印這條診斷，接著印簡短用法，以 `2` 結束
- `VK0032`：`<解除本機覆寫的指令>` 依對象印成 `just vendor_kit undev <repo>` 或 `just vendor_kit undev --engine`
