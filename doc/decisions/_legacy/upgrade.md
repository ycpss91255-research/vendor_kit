# upgrade

## 一致
- B 走「甲」：just upgrade 只改 .version 就停，不裝、不 diff；成功訊息要明講「尚未安裝，下一步 just diff <name>」。乙（一路做到 install+diff）兩邊都否決，理由一致：部分成功難表達、--dry-run 語意糊掉、且 Renovate 路徑不會經過它。
- 「最新」不能靠 tag 清單順序或 latest 名稱；要自訂規則（semver 過濾、預發行版政策），而且手動 upgrade 與 Renovate 的規則必須一致，否則兩條路會互相回滾。
- digest 一律取頂層 index digest，並檢查 index 內同時有 linux/amd64 與 linux/arm64。
- 容器內查 registry 的憑證和主機 docker login 是兩回事；掛 ~/.docker/config.json 遇到 credsStore/credHelper 只會拿到 helper 名字沒有密文。GHCR 用 read:packages PAT、GitLab 用 read_registry token、CI job token 有專案範圍限制。
- 有 .version.local 的 path: 覆蓋時，upgrade/diff/accept/回退的訊息都要揭露覆蓋狀態。
- C 走「先換自己」，但兩邊都強調：順序本身不保證相容，必須有一個凍結的最小啟動契約（舊啟動器呼叫新 image 的 bootstrap）、協定版本號與相容性矩陣測試（issue #14 用協定版本判斷，不用 release 版本判斷）。
- just 在執行 recipe 前就把 justfile 與 import 整個解析進記憶體，recipe 中途改寫 .vendor_kit/vendor.just 對本次執行無效；agy 寫的「自動用新 recipe 續跑」不成立，必須重新起一個 just 程序。
- Renovate 只改 .version，.vendor_kit/ 的程式檔重寫落在每台機器 merge 後才發生，這是結構性缺口，不是最後一步「使用者 git commit」就能帶過。
- D 不強制 accept 與 .version 同 commit（工具不碰 git、Renovate 路徑天生分兩個 commit，強制等於逼人改寫歷史）；回退 = git revert 版本變更，baseline 與使用者檔由人決定；baseline 落後 .version 是正常中間狀態，工具不可自動改 baseline。
- Renovate preset：不寫死 ghcr.io（要支援 GitLab registry 含自架 domain/port）、不靠 autoReplaceStringTemplate 重建整行、不用 pinDigests 當正確性證明、要明定 versioning 與預發行版政策、同 tag 換 digest 的 PR 視為需調查事件不自動合併、要用 fixture 測試而非只驗 JSON 合法。
- agy 的前例研究品質不足：mise PR #6258 連結錯誤、Gradle「必跑兩次」與「自動寫 SHA256」錯誤、Batect 已停維護、pre-commit/terraform 的「只查不下載」類比不成立。

## 分歧（含判斷）
- 容器內查 registry 用什麼實作：先用 urllib。理由：已有實測、不多帶二進位、不多一個要 Renovate 追的版本。crane 的好處（credential helper、企業 CA、代理、各家 registry 的怪癖）要等真的踩到才值得付出；把「換成 crane」列為已知的替代方案，並在 acceptance 測試把 ghcr.io 與 gitlab.com 的 fixture 固定下來，換實作時有東西可比。
- just upgrade 不給 name 時的行為：採 codex。vendor_kit 自身升級會觸發 C 路徑的重寫與重跑，把它混在「順手全升」裡風險太高；第一版要 name 或 --all，--all 是否包含 vendor_kit 行另用 --self 或明講。Claude 提的 --check（退出碼 0/1 給 CI 當過期提醒）與 [version] 指定 tag 值得留。
- C 路徑：重寫 .vendor_kit/ 之後怎麼接回原本的指令：第一版採 codex 的「停下來要求重跑」。just 的 recipe 拿不到使用者原始完整 argv（多 recipe、位置參數、--set 等），"$@" 只是那條 recipe 的參數，re-exec 容易漏；先把「印出建議指令並以非零退出」做對，續跑列為後續改善。
- C 路徑：重寫 .vendor_kit/ 的原子性與範圍：兩邊互補，都收。codex 解決「重寫過程被打斷」，Claude 解決「重寫結果誰提交、會不會一直髒」。落地形狀：.vendor_kit/ 拆成「程式集合（可整個替換）」與「baseline/（持久）」；程式集合用世代目錄 + 一個很小的固定入口檔做切換點；重寫必須決定性；CI 做 git diff --exit-code。注意 Claude 提的 tools.just 改為只由工具名衍生，要先確認第 10 頁原型是否相容。
- C-3（工具 image 改純資料 + docker create/cp，永遠只跑一個 vendor_kit）：同意 Claude 把它列為備案，但不現在做。它推翻 #23（verify 在工具容器內跑）與「工具 FROM vendor_kit」兩個已定決策；先看 #14 的相容矩陣能不能在一頁內寫清楚，寫不清楚再做原型。
- D：回退後 baseline 比 .version 新，CI 要不要紅：採 D-2 的 metadata 與方向標示（兩邊其實都要記來源 ref），但 CI 對「baseline 比 .version 新」預設只警告、不紅：codex 說得對，這可能是使用者故意的降級；Claude 想擋的是「忘了退 baseline」，用 diff 輸出把方向講白就夠了，硬紅會擋掉合法的回退 PR。要不要升級成紅燈留給專案設定。
- Renovate versioning 要不要明設：沒有真的衝突：明設 versioningTemplate=semver-coerced，並在 preset 註解寫「不要改成 docker」的原因，避免之後有人看 docker datasource 就順手改。
- Renovate regex 的逐行比對問題：codex 對，這是 agy 範例真的會壞的點。matchStrings 要用 (^|\n) 當行首，或每行一個 matchString 搭配 g 旗標，並用含多工具列、註解、CRLF 的 fixture 測。

## 對前例資料的更正
- §1.2 mise PR #6258 不是 Renovate 更新 tag@digest 的 PR（實際是 aqua backend 裝錯架構的討論）；agy 沒有找到任何真實案例，應標為「未查到」。
- §1.3 regex 範例用 ^ 當行首在 Renovate 整檔比對下只會抓到第一行；要用 (^|\n) 或逐 matchString。
- §1.3 autoReplaceStringTemplate 不是必要：只要 matchStrings 同時捕獲 currentValue 與 currentDigest，Renovate 會就地各自替換（lib/workers/repository/update/branch/auto-replace.ts）；多寫反而多一個會壞的東西（#10993 的失敗案例就是 template 相關）。
- §1.3 pinDigests 是「原本沒 digest 時幫你補」，.version 永遠有 digest 用不到；regex manager 預設 pinDigests:false，agy 引用的 #10993、#24942 恰好是不要開的反證。
- §1.3 currentDigestTemplate 在官方設定文件查不到，不可當現成 API；用 currentDigest 捕獲群組即可（實作前再確認一次）。
- §1.3 versioningTemplate 不可設 docker：docker versioning 把第一個連字號後的字當平台後綴，v0.43.0-rc2 會被當成另一個系列；regex manager 預設是 semver-coerced，明設它。
- §1.3 regex 不可寫死 ghcr.io：硬性限制說 image 倉庫可能是 GitLab registry（含自架 domain/port）。
- §1.2 PR 標題「chore(deps): update <image> docker digest to …」是 dockerfile manager 的樣貌；regex custom manager 預設 commitMessageTopic 是「dependency <depName>」。PR body「固定開頭、一定有 release notes」也是過度斷言。
- §1.4 Dependabot #1290 頁面沒有「官方表示暫無規劃」的陳述；結論對、理由是推測。Dependabot 也支援 Docker Compose 等，不是「只寫死兩個檔名」。
- §2 Batect 查最新版打的是 https://updates.batect.dev/v1/latest（UpdateInfoDownloader.kt），不是 GitHub API；且 Batect 已於 2023-10 封存停維護，只能當歷史前例；它覆寫 wrapper 而非只改獨立版本檔；tutorial#upgrading-batect 連結是猜的。
- §2/§3 Gradle：SHA256 只有帶 --gradle-distribution-sha256-sum 才寫入；第二次執行是可選的「把所有 wrapper 檔一起更新」，不是要求。這個前例反而說明「舊啟動器通常能啟動新版本」。
- §2 pre-commit autoupdate 現行實作用暫存 repo + git fetch + git describe，不是單純 ls-remote；「不建 hook 環境」不等於「完全不下載」。
- §2/§4 terraform providers lock 為了算 hash 仍會抓套件，「只查不下載」類比不成立；且它不是「升級版本但不安裝」的替代品。回退時若只 git 還原 .terraform.lock.hcl，普通 terraform init 就會照 lock 重裝，-upgrade 反而會忽略 lock，是回退時最不該下的指令；新版 provider 寫過的 state 也不一定能退。
- §4 Nix：inputs 改變時 lock 也可能被更新，不是只有顯式 flake update 才會改；舊 lock 要仍適用於目前 flake.nix。
- §4 回退用 HEAD~1 不可靠：accept 拆成多個 commit 後 HEAD~1 不一定是升級前版本。
- §5 路徑三第 5 步「啟動器自動用新載入的 recipe 續跑」不成立：just 啟動時整個解析 import，改檔對本次執行無效，必須重新起 just 程序。
- §5 路徑四第 3 步「偵測本機版本高於 .version」：印記比對只有相等/不等，沒有方向性。
- §5「把最終 image digest 寫進 image 自己的 /dist/VERSION」做不到：內容定址自我參照，multi-arch index 在子 image 完成後才組成；應由啟動器以 --self 傳入 .version 的精確 reference。
- §5「baseline 留在新版時 reverse diff 代表 baseline 壞掉」不對：那可能正是在描述一次降級。
- 整份報告對 GitLab 隻字未提：Renovate 在 GitLab 無免費 hosted app，需自架（gitlab.com/renovate-bot/renovate-runner，RENOVATE_PLATFORM=gitlab + api 範圍 token）；GitLab registry 用 read_registry PAT / deploy token / CI_JOB_TOKEN（限同專案或 allowlist）。
- §5 四條路徑都沒處理「Renovate 只改 .version，.vendor_kit/ 程式檔在每台機器 merge 後各自重寫、各自髒」的結構性問題（Mend hosted 的 postUpgradeTasks 預設封鎖，自架才可用）。
- §2「先換自己就保證相容」不成立：Batect/Gradle 的 wrapper+引擎不能類比「獨立 vendor_kit image + 各工具 image 內嵌不同版 vendor_kit」，換新啟動器後舊工具 image 裡的 engine 不會變新。

## 最終建議
B：採甲。介面 `just upgrade <name> [version] [--dry-run|--check]`，第一版要 name 或顯式 --all（vendor_kit 自身那行是否納入 --all 另外明定），只改 .version 就停，失敗不改檔，成功訊息明說「尚未安裝，下一步 just diff <name>」。upgrade 不經過會改專案的 _ensure（可拉 vendor_kit image，但不裝目標工具、不改專案檔）。寫入前重讀 .version 確認沒被別的程序改過、保留 TOML 註解與排版。registry 查詢在 vendor_kit 容器內用 Python 標準庫走 OCI token-challenge（一套通 GHCR、gitlab.com、自架 GitLab），crane 列為已知替代;「最新」規則：只認 ^v\\d+\\.\\d+\\.\\d+(-rc\\d+)?$，semver 排序，預設略過 prerelease、除非目前就在 prerelease（對齊 Renovate semver-coerced + ignoreUnstable）；digest 取 index digest 並驗證含 amd64+arm64；憑證：唯讀掛 ~/.docker/config.json 為主，credsStore 時改用 VENDOR_KIT_REGISTRY_TOKEN；錯誤訊息區分「沒有這個 image」與「沒權限」。

C：採「先換自己」，並補齊硬條件：(1) 舊啟動器呼叫新 image 的 bootstrap 呼叫宣告為凍結契約，之後新增能力只走環境變數或檔案；(2) .vendor_kit/ 拆成「程式集合」與「baseline/」，程式集合用世代目錄 + 單一固定入口檔切換，流程為預檢 → 暫存區生成 → 排他鎖內重讀 .version 未變才切換；(3) 重寫結果對 (vendor_kit 版本, .version 內容) 位元組決定性；(4) 第一版更新完成後明確停止、印出建議指令要求重跑，不做 re-exec；(5) image LABEL 帶協定版本號，啟動器用 docker image inspect 比對，協定版本與 release 版本分離；vendor_kit 與工具的發布 CI 各自跑相容矩陣（舊啟動器×新 image、新啟動器×舊 engine、新 engine×舊印記/baseline、降級舊 engine×新 baseline）；(6) CI 契約檢查對 .vendor_kit/ 做 git diff --exit-code，自架 Renovate（GitLab 必然）用 postUpgradeTasks 把重寫檔放進 MR；(7) 提供不依賴已壞 just import 的固定 Docker 呼叫作為恢復入口。C-3（工具 image 純資料 + docker cp）保留為備案，等 #14 矩陣寫不清楚時再做原型量測。

D：不強制 accept 與 .version 同 commit（同 PR 只是建議）。baseline/<name>/ 的 metadata 記來源 ref（tag+digest）、格式版本；diff 偵測 baseline 與 .version 不一致並印出方向（落後=尚未 accept、超前=可能是回退），結束狀態新增或明確歸類這一種；accept 允許雙向、在鎖內確認模板仍對應目前目標，第一版拒絕把 .version.local 覆蓋中的工具 accept 成正式 baseline。CI 對「baseline 比 .version 新」預設只警告。文件寫清楚：回退 = revert .version（Renovate merge commit 要 -m 1），vendor_kit 自身回退還要一併退 .vendor_kit/ 程式集合，baseline 與使用者檔由人決定；舊 image 保留規則要涵蓋所有仍被引用的版本。

Renovate：採 R1，bootstrap 寫出只含 extends 的 renovate.json 指向 vendor_kit repo 內的共用 preset（GitLab 自架用 renovate-runner）。preset：customManagers regex、只匹配根目錄 .version 並排除 .version.local、行首用 (^|\\n)、捕獲 depName（任意 host）/currentValue/currentDigest、datasourceTemplate=docker、明設 versioningTemplate=semver-coerced、不開 pinDigests、不寫 autoReplaceStringTemplate；packageRules 讓 vendor_kit 那行單獨成 PR 並在標題標明「需重寫 .vendor_kit/」；同 tag 換 digest 的 PR 保留但不自動合併；hostRules 依 GHCR/GitLab 分別設 token；用含多工具列、註解、CRLF、GitLab port、新 tag+新 digest、同 tag 換 digest 的 fixture 測試。

## 要問使用者
- image 是公開還是私有？vendor_kit（ycpss91255-research）與 base-dist（ycpss91255-docker）跨 org，若私有，下游 GITHUB_TOKEN、Renovate、GitLab 跨專案各要哪種 token（PAT / deploy token / CI_JOB_TOKEN allowlist）？
- just upgrade 在容器內的憑證來源：唯讀掛 ~/.docker/config.json 可接受嗎？主機用 credsStore 時只提供 VENDOR_KIT_REGISTRY_TOKEN 夠不夠？企業 CA、代理、自架 GitLab 要不要第一版就支援？
- 「最新」的規則：是否完全複製 Renovate 的 ignoreUnstable（在 rc 上才給 rc）？允不允許跨 major？tag 命名是否保證 ^v\d+\.\d+\.\d+(-rc\d+)?$，其他 tag（main、latest、sha）一律忽略？要不要 --pre 旗標？
- 第一版 upgrade 是否接受「要 name 或顯式 --all」？--all 是否包含 vendor_kit 自身那行？
- 第一版 C 路徑是否接受「更新啟動器後停下來、要求重跑一次」而非透明續跑？
- 能否調整 .vendor_kit/ 內部布局成「程式世代目錄 + 單一切換入口 + 持久 baseline/」？tools.just 改成只由工具名衍生、執行期讀 .version，是否與第 10 頁原型相容？
- 協定版本號（contract）的定義範圍：只含 bootstrap CLI 參數，還是也含印記格式、init.toml 格式、baseline metadata 格式？新啟動器支援幾個舊 contract、降級範圍是否相同？bump 規則誰定？
- bootstrap 呼叫要凍結成什麼（目前 docker run … --name vendor_kit --self <img> bootstrap）？之後新增能力一律走環境變數或檔案、不加必要參數，可接受嗎？
- C 的 .vendor_kit/ 重寫由誰提交：只靠 CI 紅燈提示人手 push，還是 GitHub 也自架 Renovate 用 postUpgradeTasks？
- 要不要現在就做 C-3 的原型量測 _ensure 多出的秒數，還是等 #14 矩陣寫不清楚再說？
- D-2 的 baseline metadata 在 dev 模式（path: 來源）下記什麼？diff 的結束狀態要新增「baseline 與 .version 不一致」一類，還是歸入 2？CI 對「baseline 比 .version 新」要警告還是紅燈？
- Renovate PR 的合併方式（merge commit / squash / rebase）各專案一致嗎？這決定回退文件寫 git revert 還是 git revert -m 1。
- 同 tag 換 digest 的 Renovate PR 要保留當違規警報，還是關掉 digest 更新以免噪音？
- 舊 image 保留多久？「仍被引用」是否包含 Git 歷史、舊分支與 baseline metadata，而不只是預設分支當前的 .version？
- CI 契約檢查在 PR 上要不要順便跑 just upgrade --check 當過期提醒（給沒有 Renovate 的專案）？
- issue #14 的原文是否有兩位審查員沒看到的額外條件？
## 使用者定案／待決（2026-09-17）
- renovate.json 名稱由 Renovate 固定；**放置方式待 ci_bridge 專案定案**：若機器人設定是通用的 → 放通用資料夾、symlink 到平台要的位置；若 GitHub／GitLab 各有自己格式 → 兩個都生成、放對應位置。原型暫放專案根目錄。
- bootstrap.sh 改為詢問式（要接哪個工具、版本），引擎自動寫 .version + install + init；之後接工具用 `just vendor_kit add <repo>`。bootstrap.sh 的對外契約明列（doc/contract/bootstrap.md）。
