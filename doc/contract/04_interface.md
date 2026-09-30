# 04 使用者介面

<ins>使用者</ins>與 CI 都透過 `just vendor_kit` 指令跟 <ins>VK</ins> 打交道；只有首次導入用 `bootstrap.sh`。這一頁列出全部指令與必要的參數、<ins>選項</ins>：少了就不能用、或會影響相容性的才列；其他選項的細節實作時再定。

- 必須永遠成立的規則以 [02 不變量](02_invariants.md) 為準，這一頁只補使用者看得到的介面行為
- <ins>結束碼</ins>的意思與每條訊息見 [03 訊息與錯誤碼總表](03_messages.md)
- 名詞見[名詞表](../../GLOSSARY.md)

## 目錄

- [主機需求](#主機需求)
- [registry 與認證](#registry-與認證)
- [入口](#入口)
- [指令](#指令)
- [共同選項](#共同選項)
- [各指令專用選項](#各指令專用選項)
- [輸出](#輸出)
- [使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
- [檢查（test）](#檢查test)
- [CI 模式](#ci-模式)

## 主機需求

依 [02 不變量第 5 條](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)，支援平台本來就有的這些不算在主機依賴內：

- POSIX sh 與它的內建指令
- 基礎 userland：`grep`、`sed`、`id`、`mktemp`、`mkdir`、`date`、`rm`、`sleep`、`od`、`tr`

除此之外，主機只需要這三個：

| 工具 | 最低版本 | 說明 | 版本不足時 |
|---|---|---|---|
| [Docker](https://www.docker.com/) | 19.03 以上 | 不支援 Podman；偵測到 Podman 時由<ins>啟動器</ins>以[結束碼](03_messages.md#結束碼) `2`結束，訊息見 [訊息](03_messages.csv) `VK0011` | 由<ins>啟動器</ins>檢查，首次導入與已有安裝目錄都一樣：在任何寫入之前以[結束碼](03_messages.md#結束碼) `2`結束，訊息見 [訊息](03_messages.csv) `VK0012` |
| [Git](https://git-scm.com/) | 不設最低版本 | VK 不在主機上呼叫 git；「安裝目錄在 git repo 裡」由啟動器用 sh 往上找 `.git` 判斷；`.git` 是目錄或檔都算，所以 worktree 與 submodule 也適用 | — |
| [just](https://github.com/casey/just) | 1.33.0 以上 | 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest) | 首次導入：`bootstrap.sh` 以[結束碼](03_messages.md#結束碼) `2`結束，訊息見 [訊息](03_messages.md#vk0005) `VK0005`。已有安裝目錄：由 just 自己報錯，見下方的註 |

註：just 版本不足時

- 首次導入：`bootstrap.sh` 在任何寫入之前以[結束碼](03_messages.md#結束碼) `2`結束，另印下載與安裝指令，訊息見 [訊息](03_messages.md#vk0005) `VK0005`
- 已有安裝目錄：justfile 用了 just 1.33.0 才支援的寫法，just 太舊時讀 justfile 就會出錯，輪不到 VK 執行，也就沒機會檢查版本；這時看到的是 just 自己的錯誤訊息與結束碼，VK 不留執行紀錄

## registry 與認證

依 [02 不變量第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git)，認證由主機與 CI 各自處理：在支援的 registry 上，主機的 docker 拉得到的 image，VK 就用得了。

- 支援的 registry 目前只有 GitHub 的 image 伺服器（GHCR）。沒列在這份清單上的 registry（例如 Docker Hub、GitLab、自架）不在承諾內
- <ins>引擎 image</ins> 公開；<ins>工具 image</ins> 公開或私有，由出貨那個 repo 自己決定
- 沒有給憑證時，不支援需要認證的版本列舉：對那個工具以[結束碼](03_messages.md#結束碼) `2`結束，印出兩條路，訊息見 [訊息](03_messages.csv) `VK0001`
  - 設定 `VENDOR_KIT_REGISTRY_TOKEN`（或 `VENDOR_KIT_REGISTRY_TOKEN_FILE`）
  - 直接指定版本 `@<tag>`

## 入口

VK 對外只有兩個入口：

- `bootstrap.sh`
  - 第一次<ins>導入</ins>時用
  - 先從 [VK 的 Release 頁](https://github.com/ycpss91255-research/vendor_kit/releases)下載 `bootstrap.sh`，再到要裝 VK 的那個目錄執行
  - 這個目錄必須在某個 git repo 裡，依 [02 不變量第 3 條](02_invariants.md#3-自動化只碰不進-git-的東西)
  - 這時 repo 裡還沒有 VK，所以由它下載<ins>引擎</ins>，再呼叫 `install`
  - 再跑一次就是修復
  - 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，Release 頁上目前還沒有這個檔
- `just vendor_kit …`
  - 日常使用的全部指令；CI 也用它，見下面的[檢查（test）](#檢查test)
  - 都收在 `vendor_kit` 這個<ins>命名空間</ins>底下，不佔用 <ins>repo</ins> 自己的頂層指令名

## 指令

```
用法：just vendor_kit <指令> [參數] [選項]

常用指令：
  add <repo>                  把一個工具納入這個安裝目錄
  add <repo>@<tag>            導入指定版本，不必列出版本
  upgrade <repo>              把鎖定版本換成新版
  upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版
  dev <repo> -p <dir>         讓工具改用本機目錄
  dev --engine -i <image>     讓引擎改用本機 image

進階指令：
  remove <repo>               把一個工具解除。初始檔不刪，只收回當初插入的行
  undev <repo>                回到鎖定版本
  undev --engine              回到鎖定的引擎版本
  upgrade --engine            升引擎
  upgrade --engine=<tag>      換成指定版本的引擎
  update                      只查有沒有新版，不改任何檔
  sync                        使本機的工具內容與版本鎖定行一致；每次跑工具 recipe 都會自動先跑它
  install                     把 VK 裝進 repo 的一個目錄，使它成為安裝目錄
  uninstall                   把 VK 從那個目錄移除。初始檔不刪
  prune                       清掉 VK 產生、但已不再使用的本機資源
  test                        跑全部檢查；本機與 CI 用同一個
  test dist                   只檢查工具交付的內容
```

清單裡的名詞見名詞表：

- [工具](../../GLOSSARY.md#工具與出貨)
- [repository name](../../GLOSSARY.md#工具與出貨) `<repo>`
- [安裝目錄](../../GLOSSARY.md#工具與出貨)
- [鎖定版本](../../GLOSSARY.md#版本與來源)
- [版本鎖定行](../../GLOSSARY.md#版本與來源)
- [tag](../../GLOSSARY.md#工具與出貨)
- [工具內容](../../GLOSSARY.md#工具與出貨)
- [工具 recipe](../../GLOSSARY.md#工具與出貨)

### 執行位置

依 [02 不變量第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git)：

- VK recipe 只准在安裝目錄執行；在別處執行就印出 [訊息](03_messages.csv) `VK0028` 診斷，以[結束碼](03_messages.md#結束碼) `2`拒絕，並印出該切到哪裡。唯讀 recipe 也沒有例外
- 工具 recipe 自動觸發的 `sync` 會先回到安裝目錄再呼叫，所以不受影響；工具自己的 recipe 要不要擋，由那個工具決定
- `install` 時上層或下層已經有安裝目錄，就印出 [訊息](03_messages.csv) `VK0029` 診斷，以[結束碼](03_messages.md#結束碼) `2`拒絕：安裝目錄不能巢狀

### 命名空間

- 一個工具可以提供多個 <ins>`<ns>` 命名空間</ins>
- `add` 時 `<ns>` 撞名就印出 [訊息](03_messages.csv) `VK0030` 診斷，以[結束碼](03_messages.md#結束碼) `2`拒絕，而且在任何寫入之前檢查。比對的對象是：
  - 其他已裝進 repo 的工具
  - 根 `justfile` 既有的 recipe 或 module
  - 保留名 `vendor_kit`

### 說明與用法錯誤

依 [02 不變量第 8 條](02_invariants.md#8-使用者介面不可取代寫法一致)：

- 各指令都有 `-h`／`--help`：把該指令的用法印到 stdout，以[結束碼](03_messages.md#結束碼) `0`結束；沒有 `help` 指令。薄殼、VK 檔與引擎的版本組合不相符時 `-h` 怎麼反應，這一頁不定；一定能用的只有[救援路徑](../../GLOSSARY.md#介面版與契約)列的那幾種
- 只打 `just vendor_kit`、不帶指令：stderr 第一行印 `vendor_kit <版本>`，第二行印 [訊息](03_messages.csv) `VK0024` 診斷 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以[結束碼](03_messages.md#結束碼) `2`結束，屬於用法錯誤
- 沒有頂層的 `just vendor_kit -h` 與 `just vendor_kit --version`：just 會把 `vendor_kit` 後面的 `-h`、`--version` 當成 recipe 名稱去找，參數到不了 VK
- 用法錯誤：先在 stderr 印出 `error` <ins>診斷</ins>，再接著印簡短用法，以[結束碼](03_messages.md#結束碼) `2`結束。算用法錯誤的有：
  - 缺必要參數：[訊息](03_messages.csv) `VK0025`
  - 不認得的指令或選項：[訊息](03_messages.csv) `VK0026`
  - tag 格式不合：[訊息](03_messages.csv) `VK0027`，見下面的[指定版本](#指定版本)
- 位置參數只放工具名稱 `<repo>`；其他值都經由選項帶入，例如 `-p <dir>`、`-i <image>`
- 同一個概念一種寫法：對象是引擎一律寫 `--engine`，本機 image 一律寫 `-i <image>`
- 選項採 GNU 式的長短選項與 `--`（[GNU Coding Standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)），但有兩點刻意不遵循 [POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)：選項放在位置參數之後也可以（不遵循 Guideline 9），`--engine` 的值可帶可不帶（不遵循 Guideline 7）。具體寫法：
  - 有短也有長：`-h`／`--help`、`-y`／`--yes`、`-i`／`--image`、`-p`／`--path`
  - 只有長：`--engine`、`--exit-code`
  - 選項放在位置參數之前或之後都可以，意思相同
  - 單獨的 `--` 結束選項：它之後的參數一律當位置參數，以 `-` 開頭也一樣，例如 `just vendor_kit add -- <repo>`
- `--engine` 是值可帶可不帶的長選項：不帶值時只表示對象是引擎；要帶值只接受 `=` 形式 `--engine=<tag>`，不接受 `--engine <tag>`，例如 `--engine=v1.2.0`。工具的指定版本維持 `<repo>@<tag>`

### 指定版本

`<repo>@<tag>` 與 `--engine=<tag>` 的 [tag](../../GLOSSARY.md#工具與出貨) 照同一套規則：

- 工具與引擎的 tag 只接受 `vX.Y.Z`，不帶 pre-release、build 後綴，不收前導零
- 最新版是把 X、Y、Z 當非負整數逐欄比數值，取最大的那個，不看字串順序、registry 回傳順序或推送時間；同一個 tag 改指到別的 digest 不算新版
- 寫出格式不合的 tag 是用法錯誤，印出 [訊息](03_messages.csv) `VK0027` 診斷，以[結束碼](03_messages.md#結束碼) `2`結束
- 不加 `init`、`ensure`、`diff`、`accept`、`rollback` 這類別名，也不加 `--purge`（VK 永不刪 repo 檔，這個選項沒有對象）。這些用途各自由既有指令的選項或 git 處理
- 工具 repo 的命名空間也照這套寫法，例如 base（[base#1192](https://github.com/ycpss91255-docker/base/issues/1192)）

### 成對與無害

- 做得了就反得回：`add` 與 `remove`、`dev` 與 `undev`、`install` 與 `uninstall` 成對。
- 查與套用分開：
  - `update` 只查
  - 真正換版本的是 `upgrade`：裝新版工具內容、做初始檔的<ins>基準版合併</ins>、更新<ins>基準版</ins>與<ins>納管</ins>紀錄，必要時重產<ins>薄殼</ins>，最後才寫版本鎖定行
- 沒有反向的 `sync`、`prune` 必須無害：
  - 不改任何<ins>進 git 的檔</ins>
  - `prune` 只清本機資源與自己的暫存

## 共同選項

`-y` 只適用於<ins>可寫 recipe</ins>。這一節只定它的語意，不承諾每個可寫 recipe 都接受。已被其他頁依賴的組合：

- `upgrade <repo> -y`：以[結束碼](03_messages.md#結束碼) `2`結束時，訊息會要求使用者照打；訊息見 [訊息](03_messages.csv) `VK0003`

其餘哪個指令接受 `-y`，實作時再定。

- <ins>`-y`</ins>：可代替原本允許的<ins>詢問</ins>
  - 照樣把改了什麼印到 stdout，不加前綴
  - 只省略詢問，不授權覆蓋使用者既有的檔，依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)
  - 不能把已存在、尚未<ins>納管</ins>的檔改成 append 納管，見下面的[使用者的檔與 VK 的檔](#使用者的檔與-vk-的檔)
  - 不解除 <ins>CI 模式</ins>：CI 模式下可以帶 `-y` 省略詢問，但要改進 git 的檔照樣以[結束碼](03_messages.md#結束碼) `2`結束，例如基準版落後時印出 [訊息](03_messages.csv) `VK0003`，與有沒有 `-y` 無關
  - 不隱含 CI 模式

沒帶 `-y`、又不能互動時（例如在腳本裡），需要詢問的操作：

- 一律不改
- 以[結束碼](03_messages.md#結束碼) `2`結束
- 印出該打的指令，訊息見 [訊息](03_messages.md#vk0002) `VK0002`
- 讀到輸入結束（EOF）不算同意

能互動時，詢問文字印到 stderr，不帶 <ins>[level](03_messages.md#結束碼)</ins> 前綴。使用者明確回答「否」是正常取消：不修改，並在 stdout 說明未變更，以[結束碼](03_messages.md#結束碼) `0`結束。

## 各指令專用選項

- `update`：查詢結果印到 stdout，不加前綴；不帶 `--exit-code` 時，查到新版仍以[結束碼](03_messages.md#結束碼) `0`結束。
- `update --exit-code`：查到新版時除了在 stdout 印出查詢結果，也在 stderr 印出 [訊息](03_messages.csv) `VK0022` 警告，以[結束碼](03_messages.md#結束碼) `1`結束，給 CI 或腳本判斷有沒有新版。
- `add <repo> -i <image>`：離線導入，用本機 image 當工具來源。
- `bootstrap.sh -i <image>`：離線導入，用本機 image 當引擎來源。
- 兩種離線導入共通：
  - `<image>` 可以是已載入的本機 image，或 image tar 檔
  - 寫進的版本鎖定行與線上導入相同
  - 缺少必要的 <ins>digest</ins> 資訊時印出 [訊息](03_messages.csv) `VK0031` 診斷，以[結束碼](03_messages.md#結束碼) `2`結束，不退化成只寫 tag，也不拿 image tar 本身的雜湊代替

VK 沒有限時的選項。要限時就在外層包 `timeout(1)`，或用 CI 的逾時設定。

## 輸出

stdout 與 stderr 怎麼分、訊息的前綴與顏色，見 [03 訊息與錯誤碼總表](03_messages.md#輸出)。是否成功依 [02 不變量第 4 條](02_invariants.md#4-永不靜默失敗)。

## 使用者的檔與 VK 的檔

依 [02 不變量第 1 條](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋)，這一節列出 VK 會碰到哪些檔、怎麼碰。

使用者的檔：

- 適用的 repo 檔含根 `justfile`、初始檔等
- 進 git 的 VK 檔裡，交由使用者維護、受合併保護的只有 VK 的設定檔 `.vendor_kit/config.toml`：它不是初始檔，只沿用初始檔的保護與合併規則，換新版或合併前一樣先問
- 其餘進 git 的 VK 檔（版本鎖定行、基準版、納管紀錄、薄殼）內容由 VK 擁有，VK 重寫它們不構成覆蓋。版本鎖定行雖由 VK 擁有，使用者仍可以照它的固定格式手改來升版或退版；手改不會讓它變成交由使用者維護的內容。薄殼被改過的處置依 [02 不變量第 6 條](02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)
- 執行紀錄與進度檔是 VK 的工作狀態，不是使用者的內容

目標不存在時新建檔（例如第一次導入時整份複製的初始檔）不動到既有的內容。動到既有使用者檔、又不構成覆蓋的寫入，只有這四種明定例外：

- 根 `justfile` 加一行 `import`：沒有這個檔就建，有就詢問後 append
- 根 `.dockerignore` 加四行：同上的 append 規則
- append 型初始檔第一次導入時向既有檔 append 內容，規則見下面「append 型的初始檔」
- 已納管初始檔的基準版合併（VK 的設定檔沿用同一套規則）：
  - 使用者沒改過：詢問是否換新版
  - 雙方都改過：詢問是否合併；<ins>合併衝突</ins>留下標記，由使用者解，印出 [訊息](03_messages.csv) `VK0021` 警告並以[結束碼](03_messages.md#結束碼) `1`結束；這次執行做完但要人接手

append 型的初始檔：

- 幾乎一定已經存在的那類初始檔只能用 append 型，例如根 `.gitignore`、`.dockerignore`、`.editorconfig`
- 沒有這個檔就建，已經有就問過才 append
- 唯一例外是根 `justfile` 不存在時建檔附的 `default`；那個檔建立後就是 repo 檔

移除時收回自己插入的行，只有這三類：

- `uninstall` 移除安裝時加在根 `justfile` 的那一行 `import`
- `uninstall` 移除加在根 `.dockerignore` 的那四行
- `remove` 與 `uninstall` 移除 append 型初始檔當初插進既有檔的那幾行

有紀錄、所以會被收回動作碰到的檔，就是根 `justfile`、根 `.dockerignore`，以及工具宣告為 append 的那些檔。收回時：

- 整份檔裡恰好一處與當初插入的原文相同，才刪那一行
- 一處也沒有、或有兩處以上，都不刪，講出是哪個檔、找到幾處；一處也沒有時印出 [訊息](03_messages.csv) `VK0016` 警告，有兩處以上時印出 [訊息](03_messages.csv) `VK0017` 警告，兩者都以[結束碼](03_messages.md#結束碼) `1`結束

其他情況：

- `add` 遇到已存在的檔：不納管、不覆蓋，印出 [訊息](03_messages.csv) `VK0018` 警告並以[結束碼](03_messages.md#結束碼) `1`結束
- `remove` 與 `uninstall`：不刪初始檔，只把清單印到 stdout，不加前綴，以[結束碼](03_messages.md#結束碼) `0`結束

## 檢查（test）

<ins>`test`</ins> 是 VK 的檢查指令，本機與 CI 用同一個。`test` 一律以 CI 模式執行，不寫進 git 的檔。檢查的範圍照這個原則：

- [01 目的與承諾](01_purpose.md)的對外契約中，CI 驗得到的項目百分之百覆蓋
- CI 驗不到的項目由 VK 的驗收測試覆蓋，依 [02 不變量第 9 條](02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)

兩種用法：

- `just vendor_kit test`：跑全部檢查
- `just vendor_kit test dist`：只檢查工具交付的內容，給提供工具的 repo 在自己的 CI 用。幾乎一定已經存在的那類初始檔若不用 append 型、改用整份複製，會被它擋下

結束碼是 `0`～`3`，意思見 [03 訊息與錯誤碼總表](03_messages.md#結束碼)。

## CI 模式

環境變數 `CI` 有值、而且不是 `0` 或 `false`（不分大小寫）時，就是 CI 模式。`just vendor_kit test` 不看環境變數，一律是 CI 模式。CI 模式下：

- 進 git 的檔一律不寫，依 [02 不變量第 3 條](02_invariants.md#3-自動化只碰不進-git-的東西)。
- 遇到非寫不可的情況，以[結束碼](03_messages.md#結束碼) `2`結束並印出清單，例如基準版落後版本鎖定行時印出 [訊息](03_messages.csv) `VK0003` 診斷。
- 有任何<ins>本機覆寫</ins>（`dev` 造成的）就印出 [訊息](03_messages.csv) `VK0032` 診斷，也以[結束碼](03_messages.md#結束碼) `2`結束，依 [02 不變量第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git)。

不在 CI 模式時，基準版落後版本鎖定行會印出 [訊息](03_messages.csv) `VK0014` 警告，以[結束碼](03_messages.md#結束碼) `1`結束。
