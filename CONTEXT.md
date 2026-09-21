# vendor_kit 領域名詞表

> 本檔是專案的專有名詞表，詞彙與定義以圖為準（乙版）。
> 頁碼標記：**主圖** = `dist_distribution.drawio`（12 頁）；**討論圖** = `discussion.drawio`（9 頁：1 對外契約、2 使用方式（乙版）、3 架構圖（乙版重畫）、4 #11 圖解、5 just 與 vendor_kit 怎麼接、6 #6 本地開發模式、7 #11 diff 三方比對、8 #13 並行安裝 lock、9 #12 verify 比什麼）；**notes** = `dist_distribution_notes.md`。
> 標「（待拍板，見討論圖第 1 頁）」的定義來自對外契約頁便條 (a)–(f)，尚未定案，不要當成已定。

## 這個專案在做什麼

工具 repo（例：base）把自己的 `dist/` 打包成一個只放檔案的 image 推上 GHCR。下游專案不再用 `git subtree` 或 symlink 拿工具檔，而是：

1. 第一次跑 release 附的 `bootstrap.sh`，它問你要接哪個工具、哪個版本，寫出 `.version`、根 `justfile` 的一行 import、`.vendor_kit/` 薄殼，然後裝好工具檔與初始檔。
2. 之後每次打 `just`，啟動器自動確認工具檔在、是對的版本、沒被改（ensure）；要跟上新版用 `just vendor_kit upgrade`（或等 Renovate 開 PR、merge 後下次 `just` 自動裝）。
3. 想在本機改工具本身，用 `just vendor_kit dev <repo> -p <dir>` 把工具指到本機目錄。

真正做事的程式是**引擎**（`vendor_kit:vN` image），只在容器裡跑；主機只需要 docker + git + just。工具 image 本身沒有程式，引擎用 `docker create` / `docker cp` 把它的 `/dist` 抓出來再寫進專案。

## 角色

| 角色 | 是誰 | 跟契約的關係 |
| --- | --- | --- |
| **工具 repo 開發者**（供應側） | 維護 base、agent_harness 這類工具 repo 的人 | 照對外契約 §E 出貨 `dist/`、`init.toml`、`Dockerfile.dist`、image |
| **使用者**（下游專案） | 用工具的專案裡的人，**包含每天打 `just` 做 build 的人**、接工具與處理升級的人 | 只需要 `bootstrap.sh` + `just vendor_kit upgrade` + `just vendor_kit dev`；其他一律自動 |
| **vendor_kit 開發者**（我們） | 維護引擎與啟動器 | 契約不對自己承諾 |

**下游一律叫「使用者」，不叫「下游開發者」。** 主圖第 9、12 頁把使用者再拆成使用者／開發者／專案維護者三種，那是指令表的分組，不是新的角色名。

## 名詞

| 名詞 | 定義 | 出現在哪頁 |
| --- | --- | --- |
| **vendor_kit** | 通用安裝工具；程式只以 image 存在、只在容器內跑，主機不用裝 Python。不綁定任何工具（base 只是第一個用它的工具）。 | 主圖 1、2、6；討論圖 3 |
| **工具 repo** | 任何想透過 vendor_kit 出貨的工具的原始碼 repo（例：base）。必須有 `dist/`、`init.toml`、`Dockerfile.dist`、打 tag 就建置上傳的 CI。 | 主圖 2、6、7；討論圖 1（§E） |
| **`<repo>`** | 占位符 = **工具 repo 名**（例：base）。`.<repo>/` = 專案裡裝好的工具檔；`<repo>-dist` = 工具 image 名；`.version` 裡的 key。不再用 `<name>`。 | 全部 |
| **工具 image `<repo>-dist:<tag>`** | 工具 repo 出貨的 image。乙版：`Dockerfile.dist` = `FROM scratch` + `COPY`，只放 `dist/`、`init.toml`、`VERSION`，沒有程式、不會被執行。多架構 amd64 + arm64 同一個 tag。 | 主圖 6、7；討論圖 1（§E）、2、3 |
| **引擎** | `vendor_kit:vN` image。所有真正的工作（install / verify / init / upgrade / bootstrap …）都在它的容器裡跑；一個專案只用 `.version` 指定的那一版。 | 主圖 2、5；討論圖 2、3、5 |
| **啟動器** | 專案裡的 `.vendor_kit/`，在主機上跑的 just recipe：讀 `.version`、用 `docker create` / `docker cp` 抓工具檔、起引擎容器。分兩部分：**薄殼**（進 git、人不改）= `entry.just`、`vendor.just`（只有 ensure + 一行 docker run 契約）、`ci/check.sh`、`baseline/`；**`gen/`**（不進 git）= 引擎每次 ensure 依 `.version` 產生的其餘 recipe（`vendor_kit.just`、`tools.just`），壞了刪掉再跑 `just vendor_kit ensure` 就回來。 | 討論圖 1（§F）、3、5 |
| **根 justfile 一行 import** | 使用者的 `justfile`（進 git），只有一行 `import '.vendor_kit/entry.just'`；使用者自己的指令加在下面。bootstrap 建立，之後歸使用者，升級永遠不動它。 | 討論圖 1（§F）、5 |
| **`just vendor_kit` 命名空間** | 引擎的指令全部放在 `vendor_kit` 命名空間（`just vendor_kit upgrade / dev / ensure …`），不佔頂層；對齊 base 的 layered just entry。`just <repo> …`、`just docker …` 這類是**工具自己帶的**（由工具 `dist/just/` 裡的 just 模組提供，每個 recipe 先跑 ensure），vendor_kit 不定義它們。 | 主圖 9；討論圖 1（§E）、2、5 |
| **專案（下游）** | 使用工具的專案 repo（例：my_robot）。必要條件：`.version`、`justfile`、`.vendor_kit/`；可同時接多個工具，各裝到自己的 `.<repo>/`。 | 主圖 2、6、7；討論圖 2 |
| **`.version`** | 專案裡的版本清單，**唯一來源**。TOML，`[tools]` 下一行一工具 `<repo> = "ghcr.io/…/<repo>-dist:tag@sha256:…"`，另有 `vendor_kit = "…"` 一行記引擎版本。digest 鎖內容、tag 給 Renovate 判斷版本系列；key 決定安裝目錄 `.<repo>/`。由 Renovate 或 `just vendor_kit upgrade` 改，回退 = `git revert` 那個 commit。 | 主圖 2、4、11、12；討論圖 1（§F）、2 |
| **`.version.local`** | 跟 `.version` 同格式的覆蓋檔，不進 git；dev 模式寫它把某個工具改指向本機目錄（`<repo> = "path:../tool"`），有同名那行就優先。檔案不存在 = 沒有人在用本機版（平常狀態）。 | 主圖 2、4；討論圖 1（§F）、6 |
| **`.<repo>/`** | 專案裡裝好的工具檔：`dist/` 全部 + 印記 `.stamp`。install 寫出的快取，不進 git，**使用者不可改**；每次升級整批替換（先寫暫存目錄再改名）。 | 主圖 2、5、7；討論圖 1（§F）、3 |
| **印記 `.stamp`** | `.<repo>/.stamp`：第一行 = 裝的是哪個 image（啟動器用 `--self` 傳進來的 `.version` 字串），之後每檔指紋給人追溯。只是「已裝版本」的快取鍵，不是信任來源、不簽章；ensure 只看第一行判斷要不要重裝，內容以 image 的 `/dist` 為準。 | 主圖 1、5、8；討論圖 3、9 |
| **ensure** | 每次打 `just` 都先跑的自動檢查（工具 recipe 開頭呼叫）：印記第一行 ≠ `.version` 有效版本 → install；相同 → verify；第一次（baseline 不存在）→ install + init；引擎版本變了 → 換啟動器。verify 失敗 → 自動重裝（待拍板 (b)，見討論圖第 1 頁；主圖第 5 頁與 notes #12 目前是「中止、不重裝」）。人不會直接打它，只有復原時用 `just vendor_kit ensure`。 | 主圖 3、9；討論圖 1（§C）、2、5 |
| **install** | 引擎子命令：把工具 image 的 `dist/` 全部寫進 `.<repo>/` 並寫印記。先寫暫存目錄 `.<repo>.tmp.<亂數>/`，最後改名；全程在鎖內。永不建立或修改使用者檔。 | 主圖 1、5；討論圖 3、8 |
| **init** | 引擎子命令：照 `init.toml` 把初始檔複製到專案、並把這版範本存成 baseline；已存在的檔 warn、不覆蓋（仍存基準）。目前提議不再獨立成指令，改由 ensure 在第一次自動做（待拍板 (a)，見討論圖第 1 頁）。 | 主圖 1、5、9；討論圖 1（§C）、2 |
| **verify** | 引擎子命令：兩棵樹比對，拿抓出來的 `/dist` 跟 `.<repo>/` 逐檔比檔案集合（缺、多都失敗，只豁免 `.stamp`）、sha256、執行位（單向）、型別（第一版禁 symlink）；不比 mtime、owner。拿共享鎖。不開放給人單獨打。 | 主圖 1、5；討論圖 3、9 |
| **upgrade** | `just vendor_kit upgrade [<repo>]`：查 GHCR 最新 → 改 `.version`。討論圖第 1 頁的版本接著 install → 三方合併初始檔 → 印摘要，不給 `<repo>` = 全部工具含 vendor_kit 自己，結束狀態 0/1/2（待拍板 (d)，見討論圖第 1 頁；主圖第 11 頁與 notes #15 B 目前是「只改 `.version` 那行就停，不裝、不 diff」）。`--to <tag>` 指定版本（待拍板 (f)，見討論圖第 1 頁）。 | 主圖 9、11；討論圖 1（§B） |
| **bootstrap 子命令** | 引擎子命令：容器內真正寫出 `.vendor_kit/` 薄殼、`justfile`、`.version`、`ci/check.sh`、`renovate.json` 的動作。第一次由 `bootstrap.sh` 呼叫；引擎自身升級時再跑一次重寫薄殼（`baseline/` 不動）。 | 主圖 10、11；討論圖 3 |
| **初始檔** | init 從範本複製到專案的檔（Dockerfile、setup.toml、entrypoint、hooks、.gitignore…）。建立後歸使用者、進 git；升級時三方合併（見下），不自動覆蓋。 | 主圖 2、3、9；討論圖 1（§D）、4 |
| **`init.toml`** | 工具 repo 提供的初始檔清單（TOML）：`[[file]]` 一項一個，`src` 相對 `dist/`、`dest` 相對專案根；目錄可整個複製。`dist/` 本身每次升級整包覆蓋，`init.toml` 列的檔只在 init 建一次。 | 主圖 1、2、5；討論圖 1（§E）；notes §3 |
| **範本（模板）** | 工具 `dist/` 裡給初始檔用的樣板（例 Dockerfile 範本）。目前只複製；渲染（帶入專案名等變數）待定。 | 主圖 1、4；討論圖 4 |
| **baseline（基準）** | `.vendor_kit/baseline/<repo>/`：上次套用的範本副本（進 git、人不改），三方合併的第三份。init 第一次存；upgrade 合併完自動推到新版（待拍板 (d)，見討論圖第 1 頁；主圖目前是 `accept` 更新）。 | 主圖 1、2、5；討論圖 1（§D）、4、7 |
| **第一次** | `baseline/<repo>/` 不存在 = 這個工具還沒初始化過；ensure 看到就自動 install + init（待拍板 (a)，見討論圖第 1 頁）。 | 討論圖 1（§C）、2 |
| **三方合併／衝突標記** | upgrade 對每個初始檔拿 baseline、你現在的檔、新版範本三份 `git merge-file`：你沒改 → 換新版；只有你改 → 不動；兩邊都改 → 檔案裡留 `<<<<<<< ======= >>>>>>>` 衝突標記，upgrade 回 2 並列出檔名，你在編輯器解掉即可；二進位檔無法合併 → 保留你的、印 warn。這是唯一無法自動化的地方。（待拍板 (d)，見討論圖第 1 頁；主圖第 5 頁目前是 `diff` 只顯示不寫回。） | 討論圖 1（§D）、4、7 |
| **dev 模式** | `just vendor_kit dev <repo> -p/--path <dir>`：`.<repo>/` 改指向本機工具 checkout（掛 `<dir>/dist` 與 `<dir>/init.toml`），寫 `.version.local`。dev 模式下一律重裝不 verify、印醒目警告。再打一次 `dev <repo>` 不帶 `-p` = 解除（待拍板 (e)，見討論圖第 1 頁；主圖第 9 頁與 notes #6 目前是獨立的 `undev`）。 | 主圖 4、9；討論圖 1（§B）、6 |
| **`bootstrap.sh`** | vendor_kit release 附的一次性腳本，在主機跑：檢查 docker / git / just（≥ 1.33）→ 詢問式「要接哪個工具、哪個版本」→ 起引擎跑 bootstrap 寫出 `.version`、`justfile`、`.vendor_kit/` → 直接 install + init → 腳本自刪。之後想再接第二個工具：再跑一次，或直接在 `.version` 手動加一行。 | 主圖 10；討論圖 1（§B）、2 |
| **Renovate** | GitHub 上的機器人：發現 GHCR 有新版就自動開 PR 改 `.version`（tag 與 digest 一起換）；merge 後每個人下次打 `just` 自動裝新版，零指令。專案的 `renovate.json` 只含 `extends` 指向 vendor_kit 的共用 preset。 | 主圖 3、4、11；討論圖 1（§C）、2 |
| **結束狀態 0／1／2** | 指令結束時的數字：0 成功、1 失敗（沒有寫任何東西，`.version` 不動）、2 完成但有衝突要你處理。CI 靠它判斷。 | 主圖 1、9、12；討論圖 1（§B） |
| **鎖** | 引擎對**專案目錄本身** `flock`（不建鎖檔）：install 排他、verify 共享；拿到鎖後重讀 `.version` 與印記，已是目標版本就跳過複製仍 verify。逾時預設 60 秒（0 = 立即失敗給 CI）；鎖不支援的檔案系統直接失敗，`VENDOR_KIT_NO_LOCK=1` 才放行。程序被殺系統自動解鎖，沒有殘鎖。 | 主圖 1、5；討論圖 8 |
| **多架構（multi-arch）** | 同一個 image 名稱同時提供 amd64 與 arm64（含 Jetson），Docker 依主機自動選；`.version` 鎖的 digest 是 multi-arch index。平台範圍：Ubuntu／Linux amd64 + arm64；Windows 只在 WSL2 裡用，視同 Linux；macOS 不在範圍。 | 主圖 2、8、12；notes §2 |
| **甲版／乙版** | 甲版：工具 image `FROM vendor_kit`，每個工具 image 內都包一份引擎（已放棄，見 ADR-0002）。**乙版（現行）**：工具 image `FROM scratch` 只放檔案；引擎只有 `vendor_kit:vN` 一份；啟動器 `docker create` / `docker cp` 抓 `/dist` 再唯讀掛進引擎容器。 | 主圖 6；討論圖 2、3；ADR-0002 |
| **暫存目錄（主機）** | 啟動器把工具 image 的檔案 `docker cp` 到主機的暫存資料夾，再唯讀掛進引擎容器當 `/dist`。乙版多的一步（實測約 0.3 秒）。 | 討論圖 2、3 |
| **兩棵樹比對** | verify 的做法：`/dist`（來源）與 `.<repo>/`（裝好的）逐檔比檔案集合、內容、執行位、型別。同一個函式給 install / verify / release-test 用。 | 主圖 1、5；討論圖 3、9 |
| **`dist/`** | 工具 repo 裡要出貨的那批檔案（wrapper、lib、runtime、範本、config、smoke 測試、`just/` 模組），全部寫進 `.<repo>/`；其他內容（doc、test、CI 腳本）不出貨。 | 主圖 1、2、7；討論圖 1（§E） |
| **`Dockerfile.dist`** | 工具 repo 出貨用的食譜：`FROM scratch`，只 `COPY dist/`、`init.toml`、`VERSION`；不 `FROM vendor_kit`、沒有程式。 | 主圖 2、6；討論圖 1（§E） |
| **GHCR** | GitHub Container Registry；工具 image 與引擎 image 放的地方。tag 不覆蓋、仍被任何 `.version` 引用的版本不刪。 | 主圖 2、4、11、12 |
| **tag／digest** | image 的版本名稱（`v0.43.0`）／內容指紋（`sha256:…`）；`.version` 兩者都記，引擎只認 digest。 | 主圖 2、11 |
| **`--self`** | 啟動器傳給引擎的字串 = `.version` 裡那一行的 image，寫進印記第一行。 | 主圖 5、8；討論圖 3 |
| **有效版本** | `.version.local` 有同名那行就用它，否則用 `.version` 的那行。 | 主圖 9 |
| **hooks** | 每個工具指令前（pre）後（post）自動執行的使用者腳本 `script/hooks/pre|post/<指令>.sh`；init 建立空殼，之後歸使用者。 | 主圖 7、9 |
| **契約檢查腳本** | `.vendor_kit/ci/check.sh`：vendor_kit 出貨、bootstrap 寫到專案的平台無關檢查腳本（install → verify → 結束狀態）；GitHub Actions／GitLab CI 檔只負責呼叫它。 | 主圖 8、12；討論圖 1（§F） |
| **對外契約** | 我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告。只對工具 repo 開發者與使用者承諾。 | 主圖 12；討論圖 1 |
| **測試分層** | vendor_kit repo 的 Dockerfile stage 與強制閘門：`env-test`（smoke，環境檢查先於一切）→ `test-base` → `lint`（ruff、import-linter、`mirror_check`、`blackbox_check`）／`unit-test`／`install-test`／`init-test`／`verify-test`／`diff-test`（integration，一個子命令一個 stage）；`release` 只 FROM runtime，`release-test` FROM release 真的 install + verify 一次；`system`（docker run 整個 image）與 `acceptance`（假專案裡真的打 just）在 CI 主機跑。層級名稱依 ISTQB。 | 主圖 7、8；ADR-0001 |
| **鏡射（mirror_check）／黑箱（blackbox_check）** | lint 層的兩個自寫檢查：每個 src 模組必有 `test_<模組>.py`／system、acceptance 測試不准 import vendor_kit，只准 docker run、just 與檔案系統。 | 主圖 7、8 |

## 避免的說法

| 不要寫 | 改寫成 | 原因 |
| --- | --- | --- |
| `<name>` | `<repo>` | 占位符 = 工具 repo 名；notes 還有舊寫法，圖已全改 |
| 「下游開發者」 | 「使用者」 | 下游專案裡的人一律叫使用者，含每天 build 的人 |
| `just vendor_kit add` | 在 `.version` 加一行（手動或再跑 `bootstrap.sh`） | add 併掉；接新工具 = 改 `.version`（待拍板 (a)，見討論圖第 1 頁） |
| `just vendor_kit init` | ensure 第一次自動做 | init 併進 ensure（待拍板 (a)，見討論圖第 1 頁） |
| `just vendor_kit diff` | `just vendor_kit upgrade --dry-run` | diff 併進 upgrade：只印會動哪些檔、不寫（待拍板 (d)，見討論圖第 1 頁） |
| `just vendor_kit accept` | upgrade 合併完自動推進 baseline | accept 併進 upgrade（待拍板 (d)，見討論圖第 1 頁） |
| `just vendor_kit undev` | `just vendor_kit dev <repo>` 不帶 `-p` | undev 併進 dev（待拍板 (e)，見討論圖第 1 頁） |
| 「vendor_kit 綁定 base」 | vendor_kit 不綁定任何工具 | base 只是第一個接上的工具 |
| 「工具 image FROM vendor_kit」 | 工具 image `FROM scratch`，只放檔案 | 那是甲版，已放棄（ADR-0002） |
| 「根 justfile `mod? vendor_kit`」 | 根 justfile 一行 `import '.vendor_kit/entry.just'` | 主圖第 2、9、10 頁還是舊寫法，討論圖與 ADR-0002 已改 |
| 「印記是簽章／信任來源」 | 印記只是已裝版本的快取鍵 | 基準是 `.version` 鎖定的 image 內 `/dist` |

## 尚未拍板（對外契約頁便條 (a)–(f)）

以下六項只是討論圖第 1 頁的提案，跟主圖與 notes 的先前決議不同，表中已標「待拍板」：

- (a) init／add 都不要：接新工具 = `.version` 加一行，ensure 第一次自動 init。
- (b) verify 失敗改成自動重裝（推翻 #12「中止不重裝」）。
- (c) vendor_kit 自身升級自動 re-exec，不停下來要你重跑。
- (d) diff／accept 併進 upgrade（三方合併＋衝突標記，baseline 自動更新）。
- (e) undev 併成 `dev <repo>` 不帶 `-p`。
- (f) upgrade 要不要 `--to <tag>` 選項。
