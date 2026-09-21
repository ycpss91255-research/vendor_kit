# 隔離題（A 根 justfile／B 命名位置／C 初始檔）—— 雙軌分析（2026-09-18）

狀態：**草案，待使用者拍板**。

## 一致
- A 題兩邊都選 A1（使用者擁有根 justfile，install 只加一行 import），且都認定「與 base 共存不需要 vendor_kit 接管根檔（A2）」——根檔一行 import → entry.just → gen/tools.just 的 mod 就夠，base 遷移後走同一條路。
- A1 必備防護兩邊一致：根檔是 symlink（現在的 base 專案）就不能寫，因為 append 會寫穿到 .base/dist/script/justfile；要辨識 justfile/.justfile 與大小寫變體，多候選就拒絕；A4 只是 A1 的 --no-justfile 備援，不是獨立方案。
- A3 兩邊都否決：兩套所有權與卸載規則並存，symlink 分支沒換到任何好處，還繼承 WSL2 Windows 檔系與 base 打架的問題。
- B 題兩邊都選 B(b)（全收進 .vendor_kit/：version.toml、version.local.toml、cache/<repo>/），理由相同：B(a)/(c) 的 .<repo>/ = .base/ 會撞 base 下游已有的 subtree，install「整批替換」會刪 tracked 檔，違反永不刪；.version 又是 base 自己的版本檔名。
- B(b) 內部要分三類（進 git：version.toml/entry.just/vendor.just/baseline；可再生：cache/、gen/、暫存；僅本機：version.local.toml、dev symlink），不能把整個 .vendor_kit/ 當可刪快取。
- C 題兩邊都選 C1 + C2 + C5：baseline 全文 + merge-file 當基礎，dpkg 四條 hash 比對當快速路徑，靜態標頭（不含版本號、由工具作者寫進範本、不注入既有檔）當提示。
- C3（.new 旁檔）兩邊都不作預設：與 git 工作流不合、旁檔本身也要防撞、升級狀態沒真正推進。
- C4 對 GitLab CI include:local 兩邊都判不可行：CI 設定在 job 前由伺服器從 git tree 解析，快取不進 git 就讀不到；agy 完全沒看到這個前提。Compose include 也不是「本地任意疊加覆蓋」。
- C 的兩個關鍵修正兩邊一致：(1) add 時已存在的檔只 warn、不納管、日後 upgrade 絕不偷偷合併進去（adopted=false）；(2) 使用者刪掉的初始檔視為本地變更，不復活；上游刪檔只 warn。
- 「vendor_kit 會碰使用者東西」的清單兩邊都同意不能只說三處，要列成完整表；.gitignore 兩邊都主張不碰。
- agy 錯誤的共同認定：同層 import 覆蓋順序說反、`just <module> --list` 語法錯、GitHub Actions symlink「官方不支援」沒有官方來源、dpkg 非 TTY「會卡住」不正確、conda/cargo/git-lfs 引用不能當依據、Compose include 與 GitLab include 的能力被高估。

## 分歧與取捨
### A2 是否「符合硬性限制」
- Claude：fits_constraints=false：symlink 進 git 在 WSL2 Windows 檔系不保證，且與 base init.sh 的 rm -f justfile 互搶。
- codex：fits_constraints=true：在支援 symlink 的檔系上可用，只要不強制接管既有根檔；但不作預設。
- 取捨：以「WSL2 Windows 掛載也要能用」為前提時 Claude 對；結論其實一樣（不採 A2），差別只在標籤。建議正式把 WSL2 支援範圍寫進限制，讓這個標籤不再有歧義。

### uninstall 刪那一行的依據
- Claude：只刪與我們寫入「文字完全相同」的那一行；整檔內容等於我們建的才刪檔。
- codex：文字相同不夠，要記錄「這行是否由本次 install 加入」，才能避免刪掉使用者自己寫的同樣 import。
- 取捨：兩者結合：文字相同 AND metadata 記錄「install 寫入過」才刪；只要兩個條件之一不成立就印指示不動。這只多存一個布林值，成本極低，而且刪檔的規則同理（記錄「檔由我們建立」）。

### C2 比對次序與 hash 工具
- Claude：四條規則直接可用（D==B→寫 N；B==N→不動；D==N→不動；都不同→merge），順序沒特別強調。
- codex：順序應為 disk==new 先、再 old==new、再 disk==old、最後才三方合併；且既然有 baseline 全文，直接比位元組即可，不需要引入 hash 工具。
- 取捨：codex 對：D==N 放第一可避免「使用者已手動更新到新版」被誤判為要寫入或要合併；直接比位元組比 sha 簡單。採 codex 的次序。

### 衝突時 baseline 要不要推進
- Claude：實測 merge-file：衝突不推 baseline 會讓使用者解完標記後重跑再衝突（無限迴圈）。主張合併當下就把 baseline 推到 N，metadata 記待解檔清單，重跑只檢查檔內有無 <<<<<<<。
- codex：衝突時保留 old/new 與待解狀態，可先保存新版候選 baseline，但不能「假裝已成功完成更新」；禁止重跑後把標記當普通本地修改。
- 取捨：兩者可相容：baseline 推到 N（避免迴圈，Copier 前例）+ metadata 標該檔 state=conflict + upgrade 結果碼仍回 2 直到標記清完。這正是 Claude 提的做法，codex 的顧慮（不能宣稱成功）由 state 與退出碼涵蓋。

### .git/info/exclude 是否還要碰
- Claude：選 B(b) 後可以整項刪掉：所有 untracked 東西都在 .vendor_kit/ 內，用 tracked 的 .vendor_kit/.gitignore + cache/gen 內的 `*` 就夠，fresh clone/worktree/CI 不再有時間窗。
- codex：仍列在清單裡，並要求用 git 解析出的位置（.git 可能是檔案）、只維護可辨識的工具區塊、worktree 共用要避免互拆。
- 取捨：Claude 對，而且是 B(b) 最大的紅利：能不碰 git 內部設定就不碰。codex 的顧慮（.git 是檔案、worktree 共用）恰恰是不碰它的理由。採 Claude，清單直接刪掉此項。

### C4 對 just/Compose 是否局部開放
- Claude：第一版全不採：justfile 已由 gen/tools.just 的 mod 解決（不是初始檔）；compose 不能覆寫同名資源且 docker compose up 直跑時快取可能不存在；要做也是 v2 新增 tracked 目錄的機制。
- codex：just/Compose 路徑經個別驗證後可條件採用；GitLab 暫不採。
- 取捨：第一版不採（Claude）。Compose 冷啟動（未經 ensure 直接 docker compose up）與 include 不可覆寫的限制在現行「快取不進 git」下沒解；等 v2 有 tracked 的 .vendor_kit/files/<repo>/ 再談。

### 是否需要在 just 1.33（最低版本）重驗
- Claude：以 just 1.53 實測為依據，未提最低版本。
- codex：1.53 實測不能反推 1.33 全部可用：mod、import?、--list 子模組、set 外溢等都要在 1.33 核對。
- 取捨：codex 對，這是驗收缺口。最低版本要定案並在 CI 用該版本跑一次全部 just 實測（含 justfile_directory() 在模組內恆為專案根、set 外溢、只有 import 的 root 報 no recipes）。

### `.vendor_kit/entry.just`、tracked 啟動器升級時能不能整檔換
- Claude：整個 .vendor_kit/ 屬 vendor_kit、使用者不改，升級整檔換或重生。
- codex：只更新「符合上次工具內容」的檔；遇修改或同名既有檔就停止，不以「位於工具目錄」推定可覆寫。
- 取捨：折衷：契約明寫 .vendor_kit/ 內 tracked 薄殼是 vendor_kit 擁有、使用者改了不保證保留；但 upgrade 若偵測到與上次發行內容不同，印 warn 再覆蓋（不停止）。停止會讓引擎升級卡住，warn 足夠。

### 「永不覆蓋」的定義
- Claude：視為既有前提，直接用；A1 append 一行、C1 合併都不算違反。
- codex：字面解讀時 A1/C1/C2 全都不符，必須正式把「入口一行 + 已納管初始檔的更新流程」寫成契約例外。
- 取捨：codex 的提醒有價值：文件要把「永不覆蓋」精確定義為「不用工具版本取代使用者客製內容；只允許明定入口一行與已納管初始檔的三方合併」，否則之後每次審查都會被字面咬。

## agy 說法查證
- 同層 import 重複 recipe：本機 just 1.53 實測先 import 者勝，不是「在後覆蓋在先」；且預設禁止重複 recipe，需 set allow-duplicate-recipes。
- 列模組內 recipe 是 `just --list <module>` 或 `--list-submodules`，不是 `just <module> --list`。
- rustup#2040 與 --no-modify-path 無關（該旗標早已存在，issue 只要求把 HOME 不可寫的錯誤降為警告）。
- GitHub Actions workflow symlink「官方不支援」沒有官方文件依據，只有社群回報（orgs/community#109744、actions/runner#3195）；可保守設計但不能寫成官方限制。
- dpkg 雙方皆改在非 TTY 不是「卡住」，是讀到 EOF 立即失敗；--force-confdef/confold/confnew 會跳過提示。結論（vendor_kit 需自訂非互動結果）不變。
- Renovate 預設 ignorePaths 只有 node_modules 與 bower_components；vendor 來自 config:recommended preset。agy 提的 `(^|/)\.version$` regex 會掃到 .base/.version，正是撞名實證。
- GitLab CI include:local 不能引用未進 git 的快取；C4 對 GitLab 在現行設計下不可行。
- Compose include 同名資源不合併、不能在根 compose 覆寫；相對路徑以被 include 檔目錄解析；「同 repo 支援 symlink」無來源。
- base 的根 justfile 是兩層 symlink（justfile → script/justfile → ../.base/dist/script/justfile），init.sh 的 _symlink() 會 rm -f 既有一般檔（會覆蓋使用者根檔）；script/local/justfile.local 是 repo-owned 進 git 的檔，不是本機檔。
- 「工具在使用者檔加一行」的缺點「升級要三方合併」對 vendor_kit 不成立：那一行永不變。
- pre-commit「官方明確拒絕 include」無憑據，只有功能請求 issue。
- conda#8836、cargo#1877、git-lfs#4174 為錯引；Husky v5 blog、devenv.local.nix、projen、just chapter_NN 等連結 404，不能當來源。
- 漏掉的關鍵 just 行為：被 import 檔內的 `set` 會外溢到 root（實測）；只有 import 的 root 會報 no recipes；模組內 justfile_directory() 恆為專案根但 set working-directory 不吃 {{}} 運算式。這決定 entry.just/gen/tools.just 只能放 mod/import?，零 set 零 recipe。
- Bazel/devenv/pre-commit/devcontainer 不是「工具擁有根設定檔」或「永不改寫」的前例：規定位置格式不等於擁有內容，pre-commit autoupdate 也會改設定。
- `auto_activate_base false` 不等於 conda 不再改 shell 設定；git config include 不是單純字典覆蓋；`merge=ours` 需另設 custom merge driver，不是內建。
- 只記 image tag/commit 不保證能重現 baseline（tag 可變、遠端可刪）；已定案的完整 baseline 全文才是依據。
- C5 標頭、唯讀權限、專屬目錄都不能當「檔案歸工具所有」的判定依據，只能提示。

## 最終建議
A = A1（強化版）、B = B(b)、C = C1 + C2 + C5 + adopted 旗標；C3、C4 第一版不採。兩位審查員的結論完全一致，差異只在細節，合併後的規則如下。

A1 具體規則：(1) 用 just 的規則找候選（justfile/.justfile，大小寫不敏感），多候選 → 拒絕；(2) 無檔 → 建檔，內容 = `import '.vendor_kit/entry.just'` + `default: @just --list`，metadata 記「檔由我們建立」；(3) 一般檔且沒那行 → 檔尾 append（先確保結尾換行），metadata 記「行由我們加入」；(4) 是 symlink（現在的 base 專案）→ 不寫、印一次性遷移指示，或用 `--justfile script/local/justfile.local`（實測 `import '../../.vendor_kit/entry.just'` 可用）；(5) `--no-justfile` 只印指示；(6) uninstall：文字相同 AND metadata 記錄過 才刪行；檔內容等於我們建的 AND 記錄過 才刪檔；(7) entry.just、gen/tools.just 只含 mod/import?，零 set 零 recipe；(8) 最低 just 版本（1.33?）要在 CI 重跑所有實測。

B(b)：根目錄只剩 .vendor_kit/ + 一行。目錄內三類：tracked（version.toml、entry.just、vendor.just、.gitignore、ci/check.sh、baseline/<repo>/、納管清單）；可再生（cache/、gen/、.tmp.*）；僅本機（version.local.toml、dev symlink）。用 tracked 的 .vendor_kit/.gitignore 取代 .git/info/exclude，清單整項刪除。Renovate 只匹配 `/^\.vendor_kit/version\.toml$/`，且 version.local.toml 不交 Renovate。啟動器欄位格式受限（`vendor_kit = "..."` 一行，先讀 local 再退回共享檔），文件明寫「version.toml 是唯一共享宣告；local 是明示開發覆寫」。工具契約 §E 新增：工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根，禁止相對 working-directory（base 的 `set working-directory := '../..'` 要改）。

C：upgrade 逐檔狀態機（B=baseline、D=磁碟、N=新版），只對「已納管、baseline 有效、一般文字檔、無待解衝突」的檔執行：D 缺 → 維持刪除；D==N → 不動；B==N → 不動；D==B → 寫 N（含 mode）；三者皆異 → git merge-file --diff3，乾淨就寫，衝突留標記、state=conflict、退出碼 2；不論結果 baseline 推到 N（避免重跑再衝突），重跑只檢查標記清完沒。add 時已存在 → adopted=false、只 warn、印 cache 內新版路徑，永不寫。N 缺 → 保留 + warn 一次。二進位（含 NUL）→ 只走比對規則，雙方皆改保留 + warn。多工具同路徑 → add 時報錯。C5 標頭為靜態文字不含版本、工具作者寫進範本（shebang 檔第 2 行、JSON 不加）、check.sh --dist 只 lint。

文件要正式定義「永不覆蓋」= 不用工具版本取代使用者客製內容；例外只有 (a) 根 justfile 的那一行、(b) 已納管初始檔的三方合併。「會碰使用者東西」清單以 Claude 版為基礎，加入 codex 的 metadata 記錄要求，並刪除 .git/info/exclude 一項。

## 要問使用者
- B(b) 改名後圖、CONTEXT.md、grilling 決議裡的 .version/.version.local/.<repo>/ 全要換：檔名定 version.toml 還是 lock.toml？version.local.toml 可接受？
- A1 的 append 是否接受？uninstall 採「文字相同 + metadata 記錄過」雙條件才刪，OK 嗎？
- 現有 base 專案（根檔是 symlink）：接受「install 不寫、印一次性遷移指示 / 用 --justfile script/local/justfile.local」嗎？遷移 base subtree 退場由誰負責、何時？
- WSL2 支援範圍是否包含 Windows 掛載檔系（/mnt/c）？包含的話所有必要流程都不能依賴 symlink（dev 模式的 cache/<repo> symlink 要改成別的機制嗎）？
- 最低 just 版本定多少（1.33？），是否同意 CI 用該版本重跑全部 just 實測再定案？
- 工具契約 §E：一個工具可否輸出多個 just 命名空間（base 現在有 docker/base/template）？不允許則 `just docker build` 變 `just base docker build`。
- 「永不覆蓋」是否接受上述正式定義（只有根檔一行與已納管初始檔合併兩個例外）？
- 衝突時 baseline 推到 N + state=conflict + 退出碼 2 直到標記清完：確認取代 proposal_v1 的「衝突不推 baseline」？
- add 時已存在的檔永久 adopted=false 只 warn，還是 v2 提供 `upgrade --adopt <file>`？
- .gitignore/.dockerignore 作為初始檔幾乎一定已存在 → base 的 ignore 條目永遠進不去。接受只 warn，還是加第四種動詞「標記區塊 append」？
- renovate.json 算不算 vendor_kit 會建的檔（無檔才建、有檔只印）？GitLab 專案要建嗎？preset 走 github> 路徑需 GITHUB_COM_TOKEN 可接受嗎？
- CRLF 政策：第一版只在 warn 提示行尾不同、不做正規化，可以嗎？
- vendor_kit 自身是否出貨初始檔（GitHub Actions caller、.gitlab-ci.yml 片段）？
- monorepo 是否允許多個 .vendor_kit/？工具識別碼如何避免跨組織同名 repo 碰撞（只用 repo 短名還是 org/repo）？

---
## 附：Claude 分析原文
**codex 建議選 A1、B(b)、C1＋C2＋C5；C4 僅經個別驗證後開放，C3 不作預設。** A1 必須加入「不跟隨既有根 symlink 編輯」的規則，舊 base 專案需一次性入口遷移。

前置定義衝突：若「永不覆蓋」指絕不改寫既有使用者檔案的任何位元組，A1 加行、C1 三方合併、C2 快進及原地衝突標記都不符合。codex 依既有決策解讀為：**不以工具版本直接取代使用者客製內容；僅允許明定的入口編輯及已納管初始檔的更新流程。** 這個例外必須正式寫進契約，否則無法宣稱整體符合硬限制。

### A. 根 justfile

| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| A1 | 一次加入 import；無檔則建立 | vendor_kit 換內部入口；根檔歸使用者 | 遷移舊 symlink 後可共存 | 誤跟隨 symlink、命名空間碰撞 | **採用，加所有權防護** |
| A2 | 既有根檔需搬移，採 symlink | vendor_kit 換目標入口 | 可共存，但不是必要條件 | 平台限制、搬移語意、誤改目標 | 不作預設 |
| A3 | 隨專案現況採不同規則 | 依安裝模式而異 | 舊 base 仍需特殊遷移 | 相對路徑、兩套所有權與卸載 | 不採 |
| A4 | 手動加入口 | 使用者維護入口；工具換內部檔 | 仍須處理舊 base symlink | 漏接入口、操作步驟增加 | 手動整合備援 |

**base 共存不要求 A2。** 採 A1 後，結構可以是：

```
justfile                        使用者擁有，一行 import
.vendor_kit/entry.just          工具入口
.vendor_kit/vendor.just         已追蹤的啟動／sync 能力
.vendor_kit/gen/tools.just      可再生的工具模組宣告
.vendor_kit/cache/<tool-id>/... 工具內容，包括未來的 base
.base/                          遷移期間保留的舊 subtree
```

根 justfile 只需 import entry，entry 再載入工具模組，並不要求根檔由 vendor_kit 擁有。`docker`／`base` 的具體命名空間需由生成規則固定，且不能讓舊入口與新模組同時註冊同名內容。對目前指向 `.base/dist/script/justfile` 的根 symlink，install 應停止入口修改並給出一次性遷移步驟。**不能追加進 symlink 目標，也不能把 symlink 自動改名為 local 就算完成。** 遷移須先確認舊入口提供的功能，再由專案明確改成自有根檔；保留 `.base/`，其 subtree 退場另行處理。

### B. 版本檔與目錄命名／位置

| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| B(a) | 根版本檔及多個點目錄 | 工具更新版本與快取 | `.base/` 直接撞名 | 誤認 subtree 為快取 | 不採 |
| B(b) | 集中於一個點目錄 | 工具依子區域規則更新 | 避開 `.base/` | 追蹤／忽略混淆、短名稱碰撞 | **採用** |
| B(c) | 根專屬版本檔及多個點目錄 | 同 B(a) | `.base/` 衝突仍在 | 只解了一半問題 | 不採 |

B(b) 應把資料分成三類，而非把整個目錄視為可刪快取：需提交（`version.toml`、啟動入口、baseline、跨 clone 判定納管所需的清單）；可再生（`cache/`、`gen/`、暫存檔）；僅本機（`version.local.toml`、dev 對應及本機操作狀態）。Renovate 只匹配約定位置的 `.vendor_kit/version.toml`，並明定依賴欄位格式；monorepo 是否允許多個此檔另行決定。啟動器只讀受限格式的引擎欄位，不引入第二份引擎版本檔。

待解矛盾：「version 唯一來源」與已定案的 local 引擎 image override 無法同時按字面成立。建議正式定義為「version.toml 是唯一共享版本宣告；local 是明示的開發覆寫」，啟動器至多先讀 local 的引擎行，再退回共享檔。若不接受這個例外，就必須修改 `dev vendor_kit --image` 的既有決策。

### C. 初始檔隔離

| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| C1 | 建立初始檔；日後可能合併 | 工具合併，使用者解衝突 | 須保證每個目標只有一個來源 | 誤納管、刪檔復活、語意衝突 | **採用作基礎** |
| C2 | 相同內容不寫；未改內容快進 | 工具按三方比較處理 | 同 C1 | 缺 baseline、未解衝突重入 | **採用** |
| C3 | 保留原檔，增加旁檔 | 使用者搬入新版 | 可共存但需人工追蹤 | 旁檔碰撞、升級未完成 | 不作預設 |
| C4 | 建立薄入口，內容改由引用取得 | 工具換被引用內容 | 可共用 base 模組 | CI 不可見快取、冷啟動、引用語意 | just／Compose 條件採用；GitLab 暫不採 |
| C5 | 範本增加適當註解 | 隨 C1/C2 處理 | 無額外所有權效果 | 註解位置、版本標示失真 | **採用穩定標頭** |

C2 的短路可直接借用**比較邏輯**，不能直接借用完整生命週期。只有「曾成功建立或明確納管、baseline 有效、一般文字檔、沒有待解衝突」才進入比較。完整次序：`disk==new` 不寫；否則 `old==new` 保留；否則 `disk==old` 更新；其餘才三方合併。使用者刪除的檔不自動復活；add 曾跳過的既有檔不自動納管；上游刪除僅警告。

merge-file 應在引擎內先產出結果，再確認目的檔未在操作期間改變後寫回。其原生退出狀態不能直接當成產品的「衝突回 2」；必須區分合併成功、內容衝突及執行錯誤，再映射退出碼。衝突時保留 old/new 與待解狀態，禁止重跑後把標記當成普通本地修改；可先保存新版候選 baseline，但不能假裝已成功完成更新。

### 最終版「vendor_kit 會碰使用者東西的完整清單」（不再宣稱只有三處）

| 檔 | 動詞 | 規則 |
|---|---|---|
| 實際選用的根 justfile／`.justfile`／大小寫變體 | install、uninstall | 唯一一般檔才可加一行；無檔才建立。多候選或 symlink 停止自動修改。記錄是否由工具插入；卸載僅移除可確定屬本次安裝且未變的行，不整檔刪除 |
| `justfile.local` | 無自動寫入 | A1 不要求建立；使用者自行組織 recipe，工具不搬移、不覆寫 |
| 舊根 symlink、`.base/**` | 無自動寫入 | 不跟隨編輯、不當快取、不刪 subtree；根入口遷移是獨立且明確的專案變更 |
| `.vendor_kit/version.toml` | install、add、remove、upgrade | 無檔才初始化；只修改契約所定欄位，保留其他內容。sync 不改；update 不提升鎖定版本；uninstall 預設保留 |
| `.vendor_kit/version.local.toml` | dev、undev | 只修改指定工具的本機覆寫；工具須已在共享宣告中。引擎 image override 同規則；不提交、不交 Renovate，不整檔清空 |
| `.vendor_kit/entry.just`、tracked 啟動器等 | install、upgrade、修復 | 只更新已確認受管且符合上次工具內容的檔案；遇修改或同名既有檔停止，不以「位於工具目錄」推定可覆寫。sync 不更新 tracked 檔 |
| `.vendor_kit/baseline/<tool-id>/**`、納管清單 | add、upgrade；必要時 remove | 保存上游範本全文與來源、目標、狀態；跳過的既有檔不列為已納管。衝突保存待解資料；remove 停止管理，保留追溯資料 |
| 各工具宣告的初始檔 | add、upgrade | add 僅建立不存在的目標；既有則警告且不納管。upgrade 僅對已納管檔執行 C2/C1；缺檔、型別異常、來源重疊則保留並報告 |
| 初始檔，包括新版不再提供的檔 | remove、uninstall、upgrade | 永不刪除；列出保留檔。新版不再提供者停止自動更新並保留紀錄 |
| 薄 include 初始檔 | add、upgrade | 仍是使用者檔；目標引用不變時不寫。wrapper 本身需改時照 C1/C2，不以 C4 為由整檔取代 |
| `.vendor_kit/cache/**`、`gen/**`、工具暫存 | install、sync、add、remove、upgrade、dev、undev、uninstall | 僅重建或清理可證明由工具生成的內容；不跟隨 dev symlink 刪除來源。未知或改動內容保留並報告，不對整個 `.vendor_kit/` 遞迴刪除 |
| Git 實際解析出的 `info/exclude` | install、sync、uninstall | 用 Git 解析位置，不能假設 `.git` 是目錄；只維護可辨識且未被修改的工具區塊，模式限縮至本機／可再生資料；worktree 共用情況須避免互相拆除 |
| `.gitignore` | 無 | 保持「不碰」承諾：禁止初始檔機制以它為目標，否則既有說法自相矛盾 |
| `.gitattributes`、CI、Compose、Dockerfile 等其他專案檔 | 僅明示初始檔流程 | 不存在隱含特例；若列入初始化清單，完全遵守 C1/C2/C5，否則不碰 |
| Git index、提交、其他 Git 設定，以及專案外檔案 | 無隱含操作 | 不自動 stage／commit、不順手設定 merge driver；拒絕越界路徑與經父層 symlink 寫出專案的目標 |

（備註：codex 在唯讀 sandbox 中未另行連網查證；附件的 HTTP 200 只能證明網址可存取，不能證明內文支持主張。）

## 附：codex 分析原文
## 裁定總覽
**A = A1（強化版）／B = (b)／C = C1 + C2 + C5（靜態標頭）+ `adopted` 旗標；C3、C4 第一版不採（C4 若做，目標必須是 tracked 目錄，v2）。**
三題互相扣住：選 (b) 之後 `.git/info/exclude` 這項可以整個從清單消失；選 A1 之後根檔永遠不需要「升級時換」；C 的規則改兩處（衝突時推 baseline、add 時已存在的檔標 adopted=false）才真正做到「永不覆蓋」。

回答草稿的關鍵疑問：**vendor_kit 不必也不該接管根檔才能與 base 共存。** 現在（base = subtree）根檔是 base 的兩層 symlink，`just base init` 會無條件 `rm -f justfile` 重建，A2 只會輪流搶檔；正確做法是 vendor_kit 看到根檔是 symlink 就不寫，讓使用者用 `--justfile script/local/justfile.local`（base 的 repo-owned 擴充點，實測 `import '../../.vendor_kit/entry.just'` 可用，`just vendor_kit …` 與 `just docker …`/`just base …` 並存）。未來 base 改由 vendor_kit 發行後，base 的命名空間走 gen/tools.just 的 mod，根檔完全不需要屬於誰；使用者把 symlink 換成一行 import 的一般檔即可（這是 base 遷移指南的事）。

## A. 根 justfile
| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| A1 加一行（強化） | 一次 append 一行；無檔則建（import + `default: @just --list`） | 沒人換（那行永遠不變；entry.just 由 vendor_kit 整檔換） | 根檔是 symlink → 不寫，`--justfile <path>` 指到 base 的 `script/local/justfile.local` | 寫穿 symlink（已用 `-L` 檢查擋掉）；imported 檔的 `set` 外溢（entry/tools.just 禁 set/recipe） | **採用** |
| A2 base 式 symlink + justfile.local | 已有 justfile 要改名；學 justfile.local | vendor_kit 整檔換（但沒東西可換） | 與 `just base init` 互搶根檔 | symlink 進 git（WSL2 Windows 檔系）；Justfile/.justfile 變體 | 否 |
| A3 混合 | 兩種模式兩份文件 | 同上 | symlink 分支同 A2 | 同 A2 | 否 |
| A4 只印指示 | 零編輯、多一個手動步驟 | 沒人換 | 無衝突 | 漏做時錯誤訊息不是我們的 | 併成 A1 的 `--no-justfile` 旗標 |

A1 具體規則：(1) 用 just 同樣的規則找候選（`justfile`/`.justfile`，大小寫不敏感），多於一個候選 → 1；(2) 沒有 → 建檔，內容 = `import '.vendor_kit/entry.just'` 一行 + `default:\n    @just --list`，建好即歸使用者；(3) 一般檔且沒那行 → 檔尾 append 一行（前留空行；trailing `# vendor_kit` 註解實測合法）；已有 → 不動；(4) 是 symlink → 不寫，印「加這一行到你的擴充檔，或 `install --justfile <path>`」；(5) `--justfile <path>` 對任一檔做 (3)，import 路徑以該檔目錄為基準計算；(6) uninstall：只刪與我們寫入完全相同的那一行；檔案內容與 (2) 完全相同才刪檔；否則印指示；(7) entry.just、gen/tools.just 只含 `mod`/`import?`，零 `set`、零 recipe（否則外溢到使用者 root、改變其 default）。

## B. 命名與位置
| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| (a) `.version` + `.<repo>/` | 根目錄 2 檔 + N 目錄 + `.git/info/exclude` | version 由 Renovate/upgrade 改一行 | `.base/` 撞 subtree（install 整批替換會刪 tracked 檔，違反永不刪）；`.version` 是 base 自己的版本檔名 | Renovate regex 掃到 `.base/.version`；根目錄暫存目錄 | 否 |
| (b) 全收 `.vendor_kit/`：`version.toml`、`version.local.toml`、`cache/<repo>/` | 根目錄只剩 `.vendor_kit/` + 一行；**不碰 `.git/info/exclude`**（`.vendor_kit/.gitignore` tracked：`cache/`、`gen/`、`version.local.toml`；cache/gen 內再自寫 `*`） | version.toml 一行；cache 整批換；薄殼整檔換 | 零撞名 | 工具模組 cwd 深度／dev symlink → 契約規定用 `justfile_directory()`（實測在模組內恆為專案根） | **採用** |
| (c) `.vendor_kit_version` + `.<repo>/` | 根目錄 1–2 檔 + N 目錄 + exclude | 同 (a) | `.base/` 仍撞 | 同 (a) 一半 | 否 |

(b) 細節：Renovate `managerFilePatterns: ["/^\\.vendor_kit/version\\.toml$/"]`（不要 `(^|/)`）；啟動器 `sed -n 's/^vendor_kit *= *"\([^"]*\)".*/\1/p' .vendor_kit/version.toml | head -1`（`version.local.toml` 同名 key 優先，同一句 sed 先查 local）；gen/tools.just 產 `mod <repo> '../cache/<repo>/just/<repo>.just'`；install 暫存目錄 `.vendor_kit/cache/.tmp.<亂數>/`；dev 模式 `cache/<repo>` → symlink 到 `<dir>/dist`（在 ignored 目錄內，git 無感）。

## C. 初始檔
| 選項 | 對使用者的侵入 | 升級時誰換 | 與 base 共存 | 風險 | 裁定 |
|---|---|---|---|---|---|
| C1 複製 + baseline + merge-file | add 建檔（已存在不碰）；upgrade 可能寫入 | upgrade 三方合併 | base 現在用 symlink/overlay，遷移後改走初始檔 | 衝突不推 baseline 會再衝突；已存在檔被塞標記 | **採用（含兩處修正）** |
| C2 dpkg 短路 | 無新增侵入 | 同上，未改的檔直接換新 | — | hash 不管 mode/CRLF | **採用**（四條規則直接可用；雙方皆改走 merge-file） |
| C3 `.new` 殘留檔 | 殘留檔 | 使用者手動 | — | 與 git 工作流不合 | 否（新版已在 cache，warn 印路徑即可） |
| C4 薄 include | 根檔一行 | 快取換 | — | GitLab include 不能指快取；compose 不能覆寫；Actions 不行 | 否（v2：需 tracked `.vendor_kit/files/<repo>/`） |
| C5 靜態標頭 | 無 | 無 | — | 含版本號會製造衝突 | **採用**（工具作者寫，不含版本，check.sh lint） |

upgrade 逐檔狀態機（B=baseline、D=磁碟、N=新版）：D 缺 → 維持刪除；D==B → 寫 N（含 mode）；B==N → 不動；D==N → 不動；三者皆異 → `git merge-file --diff3`，乾淨就寫、衝突留標記回 2；**不論結果 baseline 都推到 N**，metadata 記待解檔；D 內已有 `<<<<<<<` → 不合併、回 2；B 缺 & D 有 → `adopted=false` 永不寫只 warn；B 缺 & D 缺 → 建檔；N 缺 → 保留 + warn（baseline 移除，只 warn 一次）；二進位（含 NUL）→ 只走 hash 規則，雙方皆改保留 + warn；多工具同路徑 → add 時 1。

## 最終版：vendor_kit 會碰使用者東西的完整清單
| 檔 | 動詞 | 規則 |
|---|---|---|
| 根 `justfile`（或 `--justfile <path>` 指定檔） | install：建 / append 一行；uninstall：刪那行 | 無檔→建（import + default，建後歸使用者）；一般檔→檔尾 append `import '.vendor_kit/entry.just'`，已有不動；symlink 或多候選→不寫、印指示；`--no-justfile` 只印；uninstall 只刪完全相同的那一行、內容等於我們建的才刪檔；其餘任何時候（upgrade/add/remove/sync）不讀不寫 |
| 初始檔（各工具 init.toml 列的路徑） | add：建；upgrade：依上述狀態機寫入；remove/uninstall：不刪、印清單 | 已存在→不碰、`adopted=false`、永遠只 warn；建立後歸使用者；upgrade 只在「你沒改」或「三方合併」時寫，衝突留標記回 2 並推 baseline；新版刪除只 warn；二進位不合併 |
| `renovate.json`（若採用） | install：建 | 無檔才建（只含 `extends`）；已有→印 snippet 不改；uninstall 不刪 |
| `.vendor_kit/`（全屬 vendor_kit，使用者不改） | install/upgrade/sync：整檔換或重生 | tracked：`entry.just`、`vendor.just`、`.gitignore`、`ci/check.sh`（引擎升級整檔換）、`version.toml`（只由 add/remove/upgrade/Renovate 改對應那一行）、`baseline/<repo>/`（upgrade 整組推進）；untracked：`cache/`、`gen/`、`version.local.toml`、`.tmp.*`（隨時重生）；uninstall 整個目錄刪除 |
| `.git/info/exclude` | — | **不碰**（由 `.vendor_kit/.gitignore` 取代） |
| `.gitignore`、`.dockerignore`、其他根檔 | — | 不碰；工具若把它們列為初始檔則走初始檔規則（已存在 = adopted=false） |