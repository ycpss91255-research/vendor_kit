# 04 使用者介面

<ins>使用者</ins>只透過指令跟 <ins>VK</ins> 打交道。這一頁列出全部指令與<ins>選項</ins>（共同選項與各指令專用的選項）。

- 每一項必須永遠成立的規則寫在 [02 不變量](02_invariants.md)，這裡只寫「依第 N 條」，不重述
- <ins>結束碼</ins>的意思與每條訊息見 [03 訊息與錯誤碼總表](03_messages.md)
- 名詞見[名詞表](../../../CONTEXT.md)

## 目錄

- [主機需求](#主機需求)
- [入口](#入口)
- [指令](#指令)
- [共同選項](#共同選項)
- [各指令專用選項](#各指令專用選項)
- [CI 檢查腳本](#ci-檢查腳本)
- [CI 模式](#ci-模式)

## 主機需求

依 [02 不變量](02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust) 第 5 條，主機只需要這三個：

- [Docker](https://www.docker.com/)
  - 19.03 以上
  - 不支援 Podman
- [Git](https://git-scm.com/)
  - 不設最低版本
  - VK 不呼叫 git
  - 「安裝目錄在 git repo 裡」由<ins>啟動器</ins>用 sh 往上找 `.git` 判斷
- [just](https://github.com/casey/just)
  - 1.33.0 以上
  - 用 GitHub release 下載的版本：[just 最新版下載頁](https://github.com/casey/just/releases/latest)

版本不足時：

- 在任何寫入之前以[結束碼 `1`](03_messages.md#exit-1)結束
- just 版本不足時另印下載與安裝指令，訊息見 [03 訊息與錯誤碼總表](03_messages.md#msg-6-23)

## 入口

依 [02 不變量](02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口) 第 9 條，VK 對外只有三個入口：

- `bootstrap.sh`
  - 第一次<ins>導入</ins>時用
  - 先[下載 bootstrap.sh](https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh)，再到要裝 VK 的那個目錄執行
  - 這個目錄必須在某個 git repo 裡，依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條
  - 這時 repo 裡還沒有 VK，所以由它下載<ins>引擎</ins>，再呼叫 `install`
  - 再跑一次就是修復
  - 尚未可用：含 `bootstrap.sh` 的 release 還沒發布，這個網址目前找不到檔案
- `just vendor_kit …`
  - 日常使用的全部指令
  - 都收在 `vendor_kit` 這個<ins>命名空間</ins>底下，不佔用 <ins>repo</ins> 自己的頂層指令名，依 [02 不變量](02_invariants.md#8-使用者介面極少寫法一致recipe-語意固定) 第 8 條
- `.vendor_kit/ci/check.sh`
  - 給 CI 呼叫
  - 檢查什麼見下面的 [CI 檢查腳本](#ci-檢查腳本)

## 指令

```
用法：just vendor_kit <指令> [參數] [選項]

常用指令：
  add <repo>                  把一個工具納入這個安裝目錄
  upgrade <repo>              把鎖定版本換成新版
  upgrade <repo>@<tag>        換成指定版本；指定舊 tag 就是退版
  dev <repo> -p <dir>         讓工具改用本機目錄
  dev --engine -i <image>     讓引擎改用本機 image

進階指令：
  remove <repo>               把一個工具解除。初始檔不刪，只收回當初插入的行
  undev <repo>                回到鎖定版本
  undev --engine              回到鎖定的引擎版本
  upgrade --engine            升引擎
  upgrade --engine@<tag>      換成指定版本的引擎
  update                      只查有沒有新版，不改任何檔
  sync                        使本機的工具內容與版本鎖定行一致；每次跑工具 recipe 都會自動先跑它
  install                     把 VK 裝進 repo 的一個目錄，使它成為安裝目錄
  uninstall                   把 VK 從那個目錄移除。初始檔不刪
  prune                       清掉 VK 產生、但已不再使用的本機資源
```

清單裡的名詞見名詞表：

- [工具](../../../CONTEXT.md#term-tool)
- [`<repo>`](../../../CONTEXT.md#term-repo-name)
- [安裝目錄](../../../CONTEXT.md#term-install-directory)
- [鎖定版本](../../../CONTEXT.md#term-locked-version)
- [版本鎖定行](../../../CONTEXT.md#term-lock-version-line)
- [tag](../../../CONTEXT.md#term-tag)
- [工具內容](../../../CONTEXT.md#term-tool-content)
- [工具 recipe](../../../CONTEXT.md#term-tool-recipe)

### 說明與用法錯誤

依 [02 不變量](02_invariants.md#8-使用者介面極少寫法一致recipe-語意固定) 第 8 條：

- 每個指令都支援 `-h`／`--help`，印出該指令的用法
- 只輸入 `just vendor_kit`、不帶指令，算錯誤：印出用法，以[結束碼 `1`](03_messages.md#exit-1)結束
- 缺必要參數也算錯誤：印出用法，以[結束碼 `1`](03_messages.md#exit-1)結束
- 選項照 GNU 慣例：
  - 常用的有短也有長：`-h`／`--help`、`-y`／`--yes`、`-p`／`--path`、`-i`／`--image`
  - 不常用的只有長：`--engine`、`--dry-run`、`--timeout`、`--exit-code`

### 成對與無害

依 [02 不變量](02_invariants.md#8-使用者介面極少寫法一致recipe-語意固定) 第 8 條：

- 做得了就反得回：`add` 與 `remove`、`dev` 與 `undev`、`install` 與 `uninstall` 成對。
- 查與套用分開：
  - `update` 只查
  - 真正換版本的是 `upgrade`
- 沒有反向的 `sync`、`prune` 必須無害：
  - 不改任何<ins>進 git 的檔</ins>
  - `prune` 只清本機資源與自己的暫存

## 共同選項

`-y` 與 `--dry-run` 只適用於<ins>可寫 recipe</ins>。這一節只定兩個選項的語意，不承諾每個可寫 recipe 都接受；哪個指令接受哪個選項，實作時再定。

- <ins>`-y`</ins>：免問
  - 照樣印出改了什麼
  - 只省略<ins>詢問</ins>，不授權覆蓋使用者既有的檔，依 [02 不變量](02_invariants.md#1-使用者寫的內容歸使用者可以建要改先問永不刪永不覆蓋) 第 1 條
  - 不解除 <ins>CI 模式</ins>
- `--dry-run`：只預覽會做什麼
  - 不寫 <ins>repo 檔</ins>與 <ins>VK 檔</ins>
  - 不建<ins>進度檔</ins>
  - <ins>執行紀錄</ins>照寫，依 [02 不變量](02_invariants.md#4-永不靜默失敗) 第 4 條

沒帶 `-y`、又不能互動時（例如在腳本裡），需要詢問的操作：

- 一律不改
- 以[結束碼 `1`](03_messages.md#exit-1)結束
- 印出該打的指令

## 各指令專用選項

- `update --exit-code`：查到新版時以[結束碼 `2`](03_messages.md#exit-2)結束，給 CI 或腳本判斷有沒有新版。
- `add <repo> -i <image>`：離線導入，用本機 image 當工具來源。
  - `<image>` 可以是已載入的本機 image，或 image tar 檔
  - 寫進的版本鎖定行與線上導入相同
  - 缺少必要的 <ins>digest</ins> 資訊時以[結束碼 `1`](03_messages.md#exit-1)結束，不退化成只寫 tag
- `bootstrap.sh -t <repo>[@<tag>]`（長選項 `--tool`）：導入時一併把工具納入。
  - 可重複，一次一個工具
  - 不寫 `@<tag>` 就取最新版
- `bootstrap.sh -i <image>`：離線導入，用本機 image 當引擎來源。
  - `<image>` 可以是已載入的本機 image，或 image tar 檔
- `--timeout`：限制等待的時間。
  - 由啟動器在主機這一側處理，不交給引擎

## CI 檢查腳本

`.vendor_kit/ci/check.sh` 是 <ins>CI 檢查腳本</ins>，檢查的範圍照這個原則：

- [01 目的與承諾](01_purpose.md)的對外契約中，CI 驗得到的項目百分之百覆蓋
- CI 驗不到的項目由 VK 的驗收測試覆蓋，依 [02 不變量](02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口) 第 9 條

兩種用法：

- 不帶參數：檢查安裝目錄
- `--dist`：檢查工具 repo 交付的內容，給提供工具的 repo 在自己的 CI 用

結束碼是 `0`～`3`，意思見 [03 訊息與錯誤碼總表](03_messages.md#結束碼)。

## CI 模式

環境變數 `CI` 有值、而且不是 `0` 或 `false`（不分大小寫）時，就是 CI 模式。CI 模式下：

- 進 git 的檔一律不寫，依 [02 不變量](02_invariants.md#3-自動化只碰不進-git-的東西) 第 3 條。
- 遇到非寫不可的情況，以[結束碼 `1`](03_messages.md#exit-1)結束並印出清單。
- 有任何<ins>本機覆寫</ins>（`dev` 造成的）也以[結束碼 `1`](03_messages.md#exit-1)結束，依 [02 不變量](02_invariants.md#2-一個來源版本鎖定行只有一份進-git) 第 2 條。
