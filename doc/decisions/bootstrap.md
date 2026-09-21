# bootstrap

## 一致
- `import?` 和 `mod?` 不是同一件事：agy 只分析 import，定案卻改用 mod。mod 會建立獨立命名空間，根 justfile 無法覆寫模組內 recipe；agy 說的「頂層覆蓋底層」還需要 `set allow-duplicate-recipes`，預設是報錯。兩位都認定這條優點在定案下不成立。
- 根 justfile 只放一行 `mod? vendor_kit` 做不到「工具自動出現在頂層」：tools.just 若在 vendor.just 內接，工具會變成 `vendor_kit::docker`，`just docker build` 找不到。要讓工具佔頂層，tools.just 必須由根層級匯入。
- 模組 recipe 的工作目錄是模組檔所在目錄（`.vendor_kit/`），不能把 `$PWD` 當專案根；原型內所有相對路徑（`.version`、`.$name/.stamp`）在 mod 下會壞。
- 工具模組不能直接依賴 `vendor_kit::ensure`（兄弟模組之間不能互用），定案寫的「工具 recipe 呼叫 just vendor_kit ensure」在 just 依賴語法上不存在，要另外設計轉接方式。
- fresh clone 時 `.base/` 不存在，`mod? docker` 會被略過，`just docker build` 直接「找不到 recipe」，根本不會進到 recipe 去觸發 ensure。所以第一個指令一定得是 `just vendor_kit ensure`（或薄殼提供代理）。
- 已經在跑的 just 不會因 ensure 重寫檔案而重新解析：舊 recipe 會用舊邏輯走完（Gradle 要跑兩次 wrapper 的同一問題）。ensure 更新啟動器後必須中止提示重跑或 `exec just` 重跑，並防無限重入。
- 「啟動器進 git、Renovate 只改 .version、日常 ensure 自動更新啟動器」三者合在一起必定讓工作樹髒：不只 tools.just，vendor.just 和 .stamp 一樣會髒。必須二選一：升級 PR 同步提交全部產物，或者只有穩定薄入口進 git、可更新的部分放 gitignore 的目錄。
- bootstrap.sh 預設自刪是錯的：對 `curl | sh` 無意義（`$0` 是 sh，`set -e` 下 rm 失敗會把成功變失敗）、對下載檔是替使用者刪檔。應改 opt-in 或拿掉，並支援非互動模式（`--yes`、`--tool name=ref`）。
- bootstrap 的 docker run 呼叫要凍結成最小協定（mount 路徑、工作目錄、UID/GID、`--name`、`--self`、子命令、結束碼），並帶契約版本號；舊薄殼呼叫新 image 時 image 要能辨識並給升級指示。release 時必須把完整 `ghcr.io/…:vX@sha256:…` 烙進腳本，否則 `.version` 第一行沒 digest、Renovate 鎖不住。
- just 最低版本必須明定並檢查，不能只檢查指令存在（模組 1.31 才穩定、`set working-directory` 1.33 才有；Ubuntu 24.04 apt 的 1.21 直接拒絕 mod）。
- 世代目錄不是必要：真正要解的是「install 的 rmtree 不能波及 baseline/」，用 cli 拒絕 `--name vendor_kit install` 加逐檔原子寫入（tmp+rename）就能守住；git / .version 本身就是回退機制。
- agy 的前例有幾條站不住：Renovate 的 `renovate-config-validator` 只驗證設定，不會產生 onboarding PR，兩件事被混在一起；Batect 不能當「符合主機限制」的前例；`just --list` 與 IDE 補全「完全不變」是沒查證的斷言。
- `.stamp` 的定位要對齊 issue #23：它是快取鍵，不是信任來源；啟動器壞掉時可能在自我檢查前就解析失敗，要有不依賴根 justfile 的逃生口（Claude 實測 `just --justfile .vendor_kit/vendor.just ensure` 可行，前提是 vendor.just 不 import tools.just）。

## 分歧（含判斷）
- tools.just 要不要存在？工具清單是產生的還是手寫的？：採 Claude 的形狀但收斂範圍：tools.just 放 gitignore 的 gen/、由 ensure 從 .version 決定性產生，這樣「接新工具只改 .version」的目標才成立，而且沒有 tracked 髒檔。codex 的擔心（產出取決於安裝狀態、排序、.version.local）要用「只從 .version 的 [tools] key 排序產生、不看安裝狀態」來封住。若使用者接受手改根 justfile 加 mod 行，codex 方案更簡單，但那就等於每接一個工具都要動使用者檔。
- ensure 跨模組怎麼接：第一版採 codex 的子程序寫法：它不需要工具 image 知道 ensure.just 的相對路徑（那條路徑本身就是另一個要凍結的契約），而且 ensure 天然變成公開介面。Claude 的 `set working-directory := '..'` 修 cwd 這一點兩案都要做。Claude 的「只檢查被呼叫的工具、vendor_kit 自身用 shell sha256 對 stamp、不起容器」也應納入，避免 N+1 次 docker run。
- Batect 前例哪裡錯：兩條都對、不衝突，要一起更正：Batect 既已廢棄、又不符主機限制，只能借「啟動器進 git」這一個概念。
- Gradle 前例的教訓：兩者互補：agy 一邊過度推論（禁改）、一邊漏掉真正該學的（兩次執行 = 舊程式跑新版問題）。Gradle 真正的結構是 gradlew 少變、properties 記版本、distribution 不進 git，這正是 Claude C-2 的形狀。
- 整體推薦方案：兩案本質一致：進 git 的縮到「非凍結不可的契約」，其餘由 image 決定性產生到 ignored 目錄。差別只在要不要世代目錄——第一版不要，用單目錄 gen/ + 逐檔原子寫入即可；若日後真有並行升級或中斷恢復需求再加。
- bootstrap 如何從 .version 找到 vendor_kit image：codex 這條是 Claude 漏掉的真問題。建議正式限制：`.version` 第一行固定為 `vendor_kit = "<ref>@sha256:…"`，薄殼只用 grep 讀這一行（文件化為契約），其餘 TOML 一律由容器解析。Claude 的 `add` 子命令則負責所有寫入，讓主機側永遠不需要寫 TOML。

## 對前例資料的更正
- Batect：專案 2023-10-22 已封存、不再維護，且官方需求含 Java/Bash/curl；不能當「符合主機限制」與「自帶 --upgrade」的主要前例，只能借「啟動器進 git」的概念。
- just 覆寫模型：根 justfile 覆寫 import 內同名 recipe 需要 `set allow-duplicate-recipes`，預設直接報錯；定案改用 mod 後模組是獨立命名空間，根本無法覆寫，這條優點作廢。
- `import?` 對啟動器是反模式：`.vendor_kit/vendor.just` 進 git 必定存在，缺了代表 repo 壞掉，可選匯入會靜默變成「沒有任何 recipe」。
- agy 完全沒分析 mod 的語意：模組 cwd = 模組檔目錄、兄弟模組不能互相依賴、import/mod 路徑只能是字面字串（不能執行期讀 .version 拼路徑）。
- Dev Container CLI 的 `docker run ghcr.io/devcontainers/cli … templates apply` 在官方 README 查不到，疑似拼湊，不採用。
- Renovate：`renovate-config-validator` 只驗證設定，onboarding PR 是完整 run（需 token）的行為，兩者被混在一起；不能當「容器寫出初始檔」前例。
- Gradle：一邊過度推論「嚴格禁止手改 wrapper」（官方沒這樣說），一邊漏掉真正的教訓——wrapper task 由舊版執行所以要跑兩次，這正是 `_ensure` 舊 recipe 呼叫新 image 的結構問題。
- Maven Wrapper：目前預設 distributionType 是 only-script，不必然含 jar；Wrapper 版本與 Maven 版本要分開看。
- 比較表「不改使用者檔風險：無」過度陳述：bootstrap 會寫 justfile 與 .version，upgrade 持續改 .version（規則允許，但不是「無」）。「Shell/IDE 補全完整支援」是未查證斷言，也沒考慮模組在 --list 只顯示摺疊列。
- 「工具擁有 vendor.just 所以升級零衝突零負擔」不成立：所有權只消除人工合併責任，消不掉 git 衝突、更新中斷、契約相容與並行問題。
- mkdocs/jekyll/hugo/terraform 等容器 init 案例只證明容器能透過掛載寫檔，不證明自我升級、雙架構、非互動、不改既有檔的完整契約。
- 整份報告沒覆蓋：just 最低版本（Ubuntu 24.04 apt 是 1.21，mod 直接被拒）、CI/非互動 bootstrap 行為、bootstrap image 該用 digest 鎖定、tracked 產生物的髒檔與 merge conflict、Renovate 託管版無法在 PR 內重產生啟動器、amd64/arm64 要鎖同一 image index digest。

## 最終建議
定案 D5 需要修訂，方向兩位審查員其實一致：把「進 git 的部分」縮到剛好等於「非凍結不可的契約」，其餘由 image 決定性產生到 gitignore 目錄（Claude 的 C-2、codex 的「薄入口 + ignored 程式集合」是同一個形狀）。具體修法：

1. 進 git 的只有：`.vendor_kit/vendor.just`（模組 vendor_kit，只含 `ensure` 與一行 docker run bootstrap 契約，帶 `launcher-contract = 1`）、`.vendor_kit/entry.just`（`mod vendor_kit` + `import? 'gen/tools.just'`）、`.vendor_kit/baseline/`。根 justfile 一行 `import '.vendor_kit/entry.just'`（非可選）。init/diff/accept/upgrade/dev recipe、ensure 轉接、tools.just、.stamp 全放 gitignore 的 `.vendor_kit/gen/`，由 ensure 從 `.version` 決定性產生（只看 .version 的 key 排序，不看安裝狀態）。這樣 Renovate 託管版只改 .version 也不會留髒檔、分支不衝突。

2. vendor.just 與工具模組檔加 `set working-directory := '..'` / `'../..'`；宣告 just ≥ 1.33 為硬性下限，bootstrap.sh 檢查版本並在 README 明說不要用 Ubuntu apt 的 1.21。

3. ensure 跨模組第一版用子程序（codex 寫法）：工具模組內 `_ensure: @{{quote(just_executable())}} --justfile {{quote(justfile())}} --working-directory {{quote(justfile_directory())}} vendor_kit ensure <tool>`，`build: _ensure`。只檢查被呼叫的工具；vendor_kit 自身用 shell sha256sum 對 stamp，不起容器。ensure 若重寫了啟動器，必須中止並提示重跑（或 exec just 重跑並防重入）。子程序失敗必須阻止 build；ensure 不得反向呼叫工具 recipe。

4. 把 bootstrap 呼叫寫成 ADR「launcher ABI v1」：mount /repo、工作目錄、-u、--name、--self、子命令 bootstrap、exit code、以及「`.version` 第一行固定 `vendor_kit = \"ref@sha256:…\"`、薄殼只 grep 這一行」。CI 的 bootstrap-test 改成「上一版薄殼 × 新 image」相容矩陣；image 要能辨識過舊薄殼並給升級指示。

5. bootstrap.sh：不自刪（或 opt-in）、支援 `curl | sh`、`--yes`、`--tool name=ref`、非互動不提問且 EOF 不當同意；檢查 `git rev-parse --show-toplevel` == `$PWD`；release 時烙入完整 `ghcr.io/…:vX@sha256:…`（雙架構鎖 index digest）；偵測 pull 失敗提示 docker login。所有寫入逐檔 tmp+rename；cli 拒絕 `--name vendor_kit install`；新增 `just vendor_kit add <name> <ref>` 由容器內 resolve digest 寫 .version，取代互動手打。

6. 不採世代目錄；第一版單目錄 gen/ 加原子寫入即可。

7. `.vendor_kit/` 的 verify 規則另訂：gen/ 走 stamp 快取鍵（依 #23 定位，不是信任來源），tracked 薄殼由 git review 把關；保留 `just --justfile .vendor_kit/vendor.just ensure` 逃生口。

原型下一輪要驗的是：全新 clone、只改 vendor_kit digest、工具 recipe 搬路徑、非互動 bootstrap、升級中斷後恢復——不是再跑一次 init → build。註：Claude 有實測 just 1.33/1.53，codex 聲明未讀原型；語意層面的結論以 Claude 實測為準，但 codex 補上的 TOML 循環、非互動細節、雙架構 digest 是 Claude 漏掉的。

## 要問使用者
- just 最低版本定 1.33 可以嗎？接受「主機不得用 Ubuntu apt 的 just，一律從 GitHub release 裝」？Jetson（arm64、Ubuntu 22.04）上誰負責裝 just？
- Renovate 是 Mend 託管 app 還是自架？（自架可用 postUpgradeTasks 重產生檔案；託管不行，這直接決定 tracked 產物方案是否可行）
- 根 justfile 的「一行」要保哪種：`import '.vendor_kit/entry.just'`（一行、非 mod）還是 `mod vendor_kit` + `import? tools`（兩行、對齊 base 的 mod? 風格）？或者接受 codex 的手寫 `mod? docker`、`mod? base`（每接工具改一次使用者檔）？
- fresh clone 後第一個指令一定是 `just vendor_kit ensure`，`just docker build` 在未安裝時只會說找不到 recipe——接受這個 UX，還是薄殼要提供代理 recipe？
- 工具命名空間誰決定：工具自己在 tool.just 宣告（可能撞使用者 recipe 或其他工具），還是 vendor_kit 依 .version key 產生（不撞，但 base 變成 `just base build`）？撞名時政策？
- 日常指令（ensure）是否允許改 tracked 檔？若不允許就確定走「薄殼 + gen/」；若允許，升級 PR 必須同步提交全部產物。
- ensure 範圍：每個指令前檢查 .version 全部工具（N 次 docker run），還是只檢查被呼叫的工具 + vendor_kit 自身 shell 檢查？
- 是否新增 `just vendor_kit add <name> <ref>` 取代 bootstrap.sh 的互動提問？bootstrap.sh 要不要保留？若保留，release 流程誰把 digest 烙進去？私有 GHCR 要不要做 docker login 提示？
- bootstrap 讀 .version 找 image：接受「第一行固定格式、薄殼只 grep 那一行」的契約限制嗎？還是要固定 seed image 由容器解析？
- Linux 基本 shell / curl 算不算主機基線？若連 curl 都不能要求，bootstrap 只能靠 docker 一行指令取得。
- launcher ABI v1 是否就此凍結寫 ADR？CI 相容矩陣要回溯幾個版本？舊工具 image 內嵌的安裝引擎要相容多久（baseline/stamp 格式、更新 launcher 的權限）？
- vendor_kit 自身是否支援 .version.local？它涉及引擎 bootstrap，不能直接套普通工具的開發模式。
- ensure 重寫啟動器後：中止提示重跑，還是 `exec just` 原參數重跑？
## 使用者定案（2026-09-17）
- just 一律用 GitHub release 下載的版本，不用 apt 的（所以最低版本可以定在 ≥ 1.33，bootstrap.sh 與 ensure 檢查版本）。
