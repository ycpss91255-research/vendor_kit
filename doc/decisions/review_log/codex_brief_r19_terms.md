# r19：01 頁「名詞與縮寫」名詞改版 ── 「兩個 repo」→「repo 與角色」，「專案」「下游」全數退場

你在目錄 `/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws2/` 工作（這是 repo 的複本；下面所有相對路徑都相對於這個目錄，不要碰這個目錄以外的任何東西）。你是執行者：直接改檔。**只能動兩個檔**：

1. `doc/decisions/review/terms.md`
2. `script/diagram/disc_v1_a.py` 的 v1p0 區塊（區塊 = `# ================= P0 v1p0` 那行到 `pages_v1_a.append(("v1p0", "名詞與縮寫", p0))` 那行為止；區塊外一個位元組都不能改）

不 commit、不 push、不跑任何 git 指令。不動 `terms_moved.md`，不動其他頁、其他檔。

## 使用者定案（背景）

「兩個 repo」是三方時代的殘留。現在**只有一種 repo**：使用者的 git repo。一個 repo 對 VK 可以扮演兩個角色（出貨、接入），可同時是兩者。「專案」這個詞只保留給「VK 的專案」（vendor_kit 自己這個 repo），不再指使用者的 repo；本頁因此不再出現「專案」。

## 要改的內容（terms.md；逐字照抄下面給的目標文字）

### 1. 「兩方與承諾關係」表的「使用者」列（第 9 行）
這列本輪允許改（名詞變了）。整列改成：

```
| **使用者** | 會跑 VK 動詞的人，兩個場合：①在 repo 裡維護 `dist/`、把工具打成工具 image、用 dev、undev 在本機開發；②在 repo 裡跑 `bootstrap.sh` 接入、add、upgrade、remove、回答詢問或給 `-y`、commit 薄殼與版本鎖定行、升版有衝突就手動編輯再重跑、把 `ci/check.sh` 接進 CI | 直接跑 `just vendor_kit …` | 被承諾方 |
```

（變動只有：「下游 repo」→「repo」、「下游 image」→「工具 image」、「dev／undev」→「dev、undev」、「在本機開發工具」→「在本機開發」、「專案裡」→「repo 裡」、「add／upgrade／remove」→「add、upgrade、remove」。其餘字元不動。）

「VK」列、開頭段、表後句「只打 `just <ns> …` 的人不是『方』……不縮寫。」一字不動。

### 2. 「## 兩個 repo」整節換成「## repo 與角色」
把第 14～21 行（標題、四欄表、表後句）整段換成：

```
## repo 與角色

**repo**：使用者的 git repo（monorepo 裡一個子目錄也可以是一個 repo）。

| 角色 | repo 有什麼、使用者在裡面做什麼 | VK 的承諾 |
|---|---|---|
| **出貨** | 有 `dist/`；使用者把它打成工具 image 推到 registry，用 dev、undev 在本機開發。`<repo>` 是這個 repo 的名字，也是工具名 | 照 `dist/` 契約出貨就搬得到 |
| **接入** | 有 `.vendor_kit/`；使用者在裡面跑 `bootstrap.sh` 接入、跑 VK 動詞、commit 薄殼與版本鎖定行 | 不刪、不覆蓋 repo 裡的檔；鎖得住、升得了；失敗必印原因 |

同一個 repo 可以同時出貨與接入；VK 的承諾分別落在兩個角色。
```

### 3. 「VK 組件（component）」
只改薄殼一條：「隨專案進 git」→「隨 repo 進 git」。整條變成：
```
- **薄殼**：`.vendor_kit/` 內由引擎產生、隨 repo 進 git、供使用者呼叫 VK 的一組檔。
```
引擎、啟動器兩條不動。

### 4. 「常用詞」表：改下面這些列，列的順序、其他列一字不動

```
| **工具** | tool | repo 出貨、供另一個（或同一個）repo 接入的內容單位，名字是 `<repo>`。 |
| **接入根** | install root | repo 內含 `.vendor_kit/` 的目錄。 |
| **`dist/`** | dist | repo 交付給 VK 的工具出貨目錄。 |
| **工具 image** | tool image | 裝載一個工具出貨內容、供 VK 取得該內容的容器 image。 |
| **registry** | registry | 存放並提供工具 image 與引擎 image 的服務。 |
| **repo 檔** | repo file | 位於 repo 內、由使用者擁有及維護的檔。 |
| **進 git 的檔** | tracked file | 預期由 git 追蹤並隨 repo commit 的檔。 |
| **`cache/`** | cache | VK 在 repo 本機保存已展開工具內容的目錄。 |
| **`gen/`** | generated files | VK 在 repo 本機保存生成檔的目錄。 |
| **初始檔** | init file | 由工具提供、VK 接入 repo 後交由使用者維護的 repo 檔。 |
```
（「專案根」列改名為「接入根」、「下游 image」列改名為「工具 image」、「專案檔」列改名為「repo 檔」，都留在原位置。）

### 5. 「動詞」表：改下面這些列，其他列一字不動

```
| `install` | 將 VK 接入 repo，或修復既有接入。 |
| `uninstall` | 從 repo 移除 VK 的接入。 |
| `add` | 將一個工具接入 repo。 |
| `remove` | 從 repo 解除一個工具的接入。 |
| `sync` | 使 repo 本機的工具內容與目前選定的來源一致。 |
| `prune` | 清理由 VK 產生、但已不再被目前 repo 使用的本機資源。 |
```

### 6. 其他條目一字不動
改完後自查：`grep -c "專案" terms.md`、`grep -c "下游"`、`grep -c "／"` 三者都要是 0。

## 產生器 v1p0 區塊（`script/diagram/disc_v1_a.py`）
照新 terms.md **逐字**同步（圖上文字 = md 文字去反引號、去 `**`；之後會用腳本雙向逐字比對，差一個字都算錯）：

- `p0_t1` 表的使用者列字串 → 換成新第 9 行的內容。
- `sec(p0, "p0_s2", Y, "兩個 repo")` → `sec(p0, "p0_s2", Y, "repo 與角色")`。
- 在 `p0_s2` 之後、`p0_t2` 之前插入一段：`Y = para(p0, "p0_t2d", Y, M('**repo**：使用者的 git repo（monorepo 裡一個子目錄也可以是一個 repo）。'))`。
- `p0_t2` 表改三欄，欄寬 `[("角色", 160), ("repo 有什麼、使用者在裡面做什麼", 930), ("VK 的承諾", 490)]`（總寬 1580 不變），兩列內容照新表（表格格文字仍走 `M()`；`<repo>` 照原樣寫）。
- `p0_t2n` 表後句 → `同一個 repo 可以同時出貨與接入；VK 的承諾分別落在兩個角色。`
- `COMP` 薄殼一條、`p0_t3` 常用詞表對應列、`p0_t4` 動詞表對應列 → 逐字照新 md。
- 不新增 helper、不改任何區塊外程式碼（含 `M()`）。id 名維持不變（新增的只有 `p0_t2d`）。
- 改完跑 `python3 /tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws2/script/diagram/gen_disc.py` 確認不報錯（它會寫 `ws2/discussion.drawio`，這是預期的）。

做完在最後輸出：terms.md 改了幾處（逐行列出行號）、產生器改了幾處、grep 三詞結果、有沒有偏離 brief 的地方。
