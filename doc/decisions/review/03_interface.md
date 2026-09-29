# 03 使用者介面

使用者只透過指令跟 VK 打交道。這一頁列出全部指令、共同選項與結束碼。每一項必須永遠成立的規則寫在 [`02_invariants.md`](/doc/decisions/review/02_invariants.md)，這裡只標條號，不重述；名詞見 [`CONTEXT.md`](/CONTEXT.md)。

## 入口

VK 對外只有三個入口：

- `just vendor_kit …`：日常使用的全部指令，都收在 `vendor_kit` 這個命名空間底下，不佔用 repo 自己的頂層指令名。
- `bootstrap.sh`：第一次導入時用。這時 repo 裡還沒有 VK，所以由它下載引擎，再呼叫 `install`。再跑一次就是修復。
- `.vendor_kit/ci/check.sh`：給 CI 呼叫，回報版本、快取、初始檔是否一致。

出處：02 第 8、9 條；[`01_purpose.md`](/doc/decisions/review/01_purpose.md)「VK 做的事」。

## 指令

### 常用

| 指令 | 做什麼 | 反向 |
|---|---|---|
| `just vendor_kit add <repo>` | 把一個工具納入這個<ins>安裝目錄</ins> | `remove` |
| `just vendor_kit upgrade <repo>` | 把鎖定版本換成新版 | — |
| `just vendor_kit upgrade <repo>@<tag>` | 換成指定版本；指定舊 tag 就是退版 | — |
| `just vendor_kit dev <repo> -p <dir>` | 讓工具改用本機目錄 | `undev` |
| `just vendor_kit dev vendor_kit -i <image>` | 讓引擎改用本機 image | `undev` |

### 進階

| 指令 | 做什麼 | 反向 |
|---|---|---|
| `just vendor_kit remove <repo>` | 把一個工具解除。初始檔不刪，只收回當初插入的行 | `add` |
| `just vendor_kit undev <repo>` | 回到鎖定版本 | `dev` |
| `just vendor_kit update` | 只查有沒有新版，不改任何檔 | — |
| `just vendor_kit sync` | 使本機的工具內容與版本鎖定行一致。每次跑 `just` 都會自動先跑它 | — |
| `just vendor_kit install` | 把 VK 裝進 repo 的一個目錄，使它成為安裝目錄 | `uninstall` |
| `just vendor_kit uninstall` | 把 VK 從那個目錄移除。初始檔不刪 | `install` |
| `just vendor_kit prune` | 清掉 VK 產生、但已不再使用的本機資源 | — |
| `just vendor_kit help` | 印出使用說明 | — |

常用三個、進階八個，數量與名稱在同一個大版號 X 之內不變。出處：02 第 8、10 條。

### 成對與無害

- 做得了就反得回：`add` 與 `remove`、`dev` 與 `undev`、`install` 與 `uninstall` 成對。
- 查與套用分開：`update` 只查；真正換版本的是 `upgrade`。
- 沒有反向的 `sync`、`prune`、`help` 必須無害：不改任何進 git 的檔。`prune` 只清本機資源與自己的暫存。

出處：02 第 3、8 條。

## 共同選項

- `-y`：免問，照樣印出改了什麼。它只省略詢問：不授權覆蓋使用者既有的檔，也不解除 CI 模式。
- `--dry-run`：只預覽會做什麼，不寫任何檔。

沒帶 `-y`、又不能互動時（例如在腳本裡），要改檔的指令一律不改，以 `1` 結束，並印出該打的指令。出處：02 第 1、4 條。

## CI 模式

環境變數 `CI` 有值、而且不是 `0` 或 `false` 時，就是 <ins>CI 模式</ins>。CI 模式下：

- 進 git 的檔一律不寫；遇到非寫不可的情況，以 `1` 結束並印出清單。
- 有任何本機覆寫（`dev` 造成的）也以 `1` 結束。

出處：02 第 2、3 條；判定方式見 [ADR-0004](/doc/adr/0004-vk-recipe-interface-and-write-boundary.md) §2。

## 結束碼

每個指令結束時回一個數字，給呼叫它的人或 CI 判斷結果：

| 結束碼 | 意思 |
|---|---|
| `0` | 成功，可能帶 warn |
| `1` | 失敗，或需要人處理。一定印出原因與下一步 |
| `2` | 做完了，但要人接手：有合併衝突要解，或 `update --exit-code` 查到新版 |
| `3` | 現有薄殼、檔案、引擎的版本組合不合，要先升級或退回才能繼續。這種情況不動任何檔 |

一次處理多個工具時只回一個碼，回最需要處理的那個：`1` 優先於 `2`，`2` 優先於 `0`。出處：02 第 4 條。
