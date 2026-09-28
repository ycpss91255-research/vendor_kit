**vendor_kit 已避開 subtree 的直接耦合，但尚未完整避開「舊入口無法修自己、版本已鎖但交付不完整、測試綠卻沒驗到升級」三類問題。** 最需補的是跨版本相容契約、fresh clone 的薄殼修復入口，以及發布前驗收。

以下只依附件；vendor_kit 以 v2.2 加 grilling 最終 Q10–Q13 為準。「避開」指設計已處理，不代表已實作驗證。base 的 OPEN 依附件保留，即使留言稱部分已修；閉單只有標題者，以標題摘錄，不推測實作。ADR 編號省略前導零。

### A　傳播機制（subtree／init.sh／upgrade.sh／symlink／使用者改檔）

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| 搬路徑只更新新程式，已發布的舊入口斷掉；第一次升級成功、第二次命令消失 | ADR-6／#1077：「the upgrade REMOVED THE COMMAND THAT PERFORMED IT.」 | 已解 #915、#1077 | 舊路徑留 forwarder；同一命令字串連升兩次 | **部分**：固定薄殼、版本化 resolve 協定；未定舊 launcher 支援期限 | 凍結 bootstrap／launcher→engine 介面；列支援版本下限，驗舊入口→新版→再次升級 |
| 新版 migration 放在舊 driver，不可能觸及需要它的使用者 | #1110：「The two conditions are therefore mutually exclusive by construction.」 | 未解 open #1097、#1110；個案 #1086 已解 | 個案移至新版 init；通用版本區間 migration 未完成 | **部分**：引擎集中邏輯，但自身升級仍由現有版本啟動 | 定義新引擎接手點、metadata/schema migration 與可跨越版本範圍 |
| symlink 根 justfile 不給下游擴充，init 還會把實體檔改回 symlink | ADR-10：「committing a real `justfile` is clobbered back to the symlink」 | 已解 #594、#625 | 分離工具入口與 repo-owned local registry | **避開**：根檔歸使用者，只經同意加入 import | — |
| 兩跳 symlink 在 BuildKit COPY 失敗 | ADR-11：「BuildKit does **not** resolve that at `COPY` time.」 | 已解，ADR-11 記錄採用單跳佈局 | 真實內容放 dist；下游單跳引用 | **避開**：正式工具展開實體檔；dist symlink 消費端也拒絕 | — |
| subtree 默默保留使用者對 vendored 內容的修改 | #1092：「it kept the local version with no conflict and no warning.」 | 未解 open #1092 | 已量測，尚未提供完成修法 | **避開**：cache verify 失敗重裝並警告；明確 dev 另走覆寫 | — |
| 初次複製後不再維護，公共邏輯／設定永久停在舊版 | ADR-32：「every change base made to that plumbing reached NEW repos only.」；#1093：「one stale ancestor, copied once at bootstrap and never re-synced」 | 公共入口已解 #945；設定未解 open #1093 | 公共 orchestrator 改為隨工具更新；設定漂移另追 | **部分**：baseline 合併可追新；add 已存在檔永不納管 | 規定公共執行邏輯留 cache；補既存檔自願納管／可追蹤的範本差異通知 |
| 用不相關檔案判斷新舊 repo，bootstrap 成功卻少 CI／測試 | #928：「Bootstrap itself succeeds (`exit=0`, `just --list` OK, zero dangling symlinks).」 | 未解 open #928，剩跨 repo discriminator 測試 | template 端調整；guard 移至 template#18 | **部分**：明確 install/add、完成標記；但 copy 已存在即略過 | 完成標記須驗交付項目及略過理由；驗「有部分檔案」的接入案例 |
| 通知升級的機制必須先升級才能收到 | #927：「the delivery vehicle is the thing being monitored」 | 未解 open #927；交付檢查已部分落地 | 改外部 release fanout；已有 delivery checker | **部分**：Renovate 獨立於工具升級，但下游自選且未保證接通 | 提供可驗證的 Renovate 接入範例；明示未接 bot 就沒有主動通知 |
| 升級新增 workflow，使下游原本正確的政策檢查失敗 | #1078：「a consumer … goes from green to red purely by upgrading.」 | 未解 open #1078、#1082 | 追蹤可拒絕安裝及全 workflow 發布能力檢查 | **部分**：修改先問，但新建初始檔只印出；同意不證明政策相容 | dry-run 明列 workflow 新增與權限；新增後必跑下游政策測試 |
| write-once 初始檔把內部路徑永久變成外部契約 | #1111：「becomes **indefinitely frozen** for every repo」 | 未解 open #1111 | 尚待修正生成入口與既存檔處理 | **部分**：可合併，但使用者可拒絕、既存檔可不納管 | 初始檔只呼叫穩定公開命令；禁止引用 cache 內部實作路徑 |

### B　just 分層與版本

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| runner 吞 argv；import 撞名讓全部命令無法解析 | ADR-5：「make silently swallows them」；ADR-10：「A **duplicate recipe name across `import` is a hard error**」 | 已解 #546、#652 | 改 just、全部動作 namespace 化 | **部分**：positional arguments＋跨工具撞名檢查；未涵蓋使用者 namespace／保留名 | add/upgrade 前用實際根 justfile 驗解析，包含 `vendor_kit` 保留名及工具改名 |
| just 多來源版本漂移 | #948 標題：「just has four provenance paths and no shared version」 | 已解 #948 | 已收斂來源；附件未附實作正文 | **部分**：GitHub release、最低 1.33＋latest 矩陣；已知中間版回歸仍可能被接受 | 明列已知壞版本的拒絕／警告及測試政策，尤其 1.42.0–1.42.2 |
| namespace `--help`／completion 和文件承諾不一致 | ADR-11：「`just docker --help` … error」；#788：「`just base u<TAB>` … returns NOTHING」 | help 已解 #789；completion 未解 open #788 | help/h；completion 暫用 `::`，等待上游 | **部分**：help 已對齊；completion 未談 | 文件區分呼叫與補全形式；只承諾實測過的 shell×just 組合 |
| 腳本有測試，just 入口仍沒被執行 | #1042：「21 of 43 `just` recipes are not driven by any test」 | 未解 open #1042、#1173 | 已盤點，入口覆蓋仍待補 | **部分**：完整 fixture 已要求，未定每個動詞／轉發行為的覆蓋 | 從 just 實際列出的命令推導驗收集合，包含 help、參數引用及失敗碼 |

### C　升級／回退／自動 release／Renovate

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| 舊版測試其實用新版 driver；滑動窗口讓歷史相容性自動失去保護 | #1048：「the test asserted the new layout against itself.」；#1041：「A compatibility obligation is permanent; a sliding window expires.」 | 未解 open #772、#1041、#1048、#1084 | 已有真實 released-driver 測試；定案改 support-floor onward | **未避開**：乾淨 fixture＋剛 build image 不等於真實跨版本升級 | 加所有受支援已發布引擎→候選版、連升兩次、跨多版及降版驗收 |
| 升級後能跑，但少了 fresh install 才有的內容 | #1057：「Nothing answers **“is the upgraded repo what a fresh one would be”**.」 | 未解 open #1057；smoke 個案已解 #1044 | 個別樹做 convergence；整體仍缺 | **部分**：決定性薄殼與 gen 有利比較；初始檔允許保留差異 | 比較工具自有產物等價；使用者檔則驗客製保留及未採用變更有紀錄 |
| rollback 還原 working tree，卻把錯誤 migration 留在 index | #1160：「true of the tree and false of」〔後文截斷；正文明述 index 未還原〕 | 未解 open #1160 | working tree 保護已補；index 缺口仍開 | **避開**：vendor_kit 不 stage、不 commit | — |
| 半完成升級／復原失敗，卻宣稱已還原 | #700 標題：「surface failed upgrade rollback (silent clobber / false 'restored')」；#1054：「a mutation that the resync's rollback does not protect」 | 個案已解 #700、#1050；整體追蹤 open #1054 | EXIT trap、保護新增受影響路徑 | **部分**：v2.2 進度日誌＋逐檔原子替換；「git revert 整組」仍未定完整集合 | 定義 journal 耐久性、復原時保護後續手改、commit 必含清單及 revert 後重建驗收 |
| 多處版本不同步；moving tag 使同 commit 執行不同工具 | #1112：「two of the four shipped reusable workers keep their old ref」；#1122：「test-tools image version has two independent sources of truth」 | 未解 open #1112、#1122 | 提案由 pinned worker 自帶工具版本 | **避開**：version.toml tag@digest 單一來源；gen/cache 由此推導 | — |
| prerelease 或未知輸入被當 stable/latest | ADR-31／#1012：「an unrecognised input resolving to the most-consumed name」 | 已解 #1012、#829 | 嚴格 version resolver；未知拒絕、RC 分類 | **部分**：Q11 查 SemVer 最大正式版已避開選版問題；供應側發布規則未完整 | 明列 stable/RC 發布條件、tag 不可覆寫、未知版本拒絕 |
| image 已發布才測試，失敗仍被消費 | #1109：「a failing smoke leaves the moved `:latest` in place.」 | 未解 open #1109；tag ruleset #1124 已關 | 已加 tag gate；image promotion 缺口仍開 | **部分**：不用 latest 限縮漂移，但 §7 仍是 release→release-test | 候選 digest 先驗收，再開放正式 tag／bootstrap asset；失敗不進可選正式版 |
| bot push tag 不觸發發布；green 也不代表相容 | ADR-31：「An event created with the default `GITHUB_TOKEN` starts no new workflow run.」 | 已解 #829 | 直接呼叫 release worker；ABI gate 只准 Z | **避開**：vendor_kit 無 bot、不 commit、不自動 release 下游；Renovate PR 必以新版完整測試 | — |
| 每個小修大量 fanout，通知變噪音；變更分類被 `fix` 字樣誤導 | ADR-27：「one bug 17 PRs」；「An issue whose fix changes behaviour is not a Z」 | 政策已定；機制未解 open #927 | Z 不 fanout；X/Y 人決定；BREAKING 展開 | **部分**：外包 Renovate 不會自動解決頻率與破壞性提示 | 提供分組／排程建議、跨版本 changelog 與 BREAKING／人工合併提示範本 |

### D　CI／runner／多架構／registry 認證

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| arm64 manifest 裝 x86 binary；多 shard 搶同 tag 最後只剩單架構 | #125 標題：「arm64 manifest contains x86_64 binaries」；#602：「last-shard-wins single-arch」 | 已解 #125、#602、#587、#603 | 原生 arm64 build/test；修多平台發布 | **避開**：工具 COPY-only、同次 buildx、兩平台內容一致；引擎原生雙架構驗收 | — |
| 拷貝出的 binary 架構對了，libc 仍不相容 | #1149：「kcov binary is musl-linked and cannot execute on Ubuntu/glibc downstreams」 | 未解 open #1149 | 下游暫自行 build glibc 版本 | **部分**：引擎容器隔離；dist 可含 binary，而 recipe 執行環境未限 | 定義 dist 可執行內容的 host/runtime 契約；平台內容一致不當作可執行證明 |
| CI 跑了 stale 工具 image；hash／變更偵測漏 COPY 輸入 | ADR-33：「an image that does not correspond to its own checkout」；#1166：「the tag … had not moved」 | 共用 provisioning 已解 #1010；本機修正有 #1169 記錄，CI 未解 open #1171 | 一個 obtain/probe script；local hash 已補，CI 仍追 | **部分**：正式 digest 與 dev image ID 已處理識別；供應 CI 重建觸發未定 | 所有 build inputs 變動均觸發；驗收實際剛 build digest，不靠版本字串 |
| base 自己能 build，下游 context 找不到 COPY 來源 | #1172：「COPYs a path that exists only in base」 | 未解 open #1172 | 遷出共用 parser 可能移除缺陷，尚未結案 | **避開**：下游只拉／展開工具 image；乾淨 fixture 驗收實際消費路徑 | — |
| fork 執行到自架 workstation；guard skip 被 rollup 算綠 | ADR-26：「a guarded skip … a green **required** check」 | 已解 #766 | 靜態推導 eligible jobs、fork guard、rollup 明確失敗 | **未避開**：原生 runner 未等於 hosted runner；事件與權限政策未定 | 明列 runner 信任邊界、fork／secrets 規則、required rollup 與缺席測試拒絕 |
| 認證／權限分層不同；兩 repo 同時發布同 package | #980 標題：「intersecting away the caller's packages: write」；#1176：「Two repos publish the same package」 | #980 已解；未解 open #1176、#1180 | 修 worker 權限；定案單一 publisher，退休工作尚開 | **部分**：Q11 區分主機 pull 與引擎 tag 查詢；package 寫入所有權未定 | 每 package 唯一 publisher；驗 host／CI／Renovate 各自私有讀取及 publisher 權限 |
| 多架構 cleanup 刪到 live manifest 的子 digest | #1089 引 #813：「deletes the per-arch children of a LIVE tag」 | cleanup 已解 #813；guard 未解 open #1089 | manifest-aware cleanup，預設 dry-run | **未避開**：pin index digest 不能保證 registry 保留它 | 訂已發布 index／children 保留政策，含供 git revert 使用的歷史 digest |
| guard 無 subject、漏 population、entrypoint 吃掉 probe，仍綠 | #1090：「The guard's population or subject is DECLARED, not DERIVED.」；#1175：「Three of the four probes … verify nothing.」 | 未解 open #1089、#1090、#1091、#1175 | 已提出非空檢查、推導集合、mutation probe | **部分**：check.sh／dist 驗收有入口，未定非空與反例證明 | 刪 subject、破壞產物必紅；正確覆寫 entrypoint；確認工具測試實際執行，不能只存在 recipe |
| 共用 cache 在一次 CI 內變動，各 shard 漏測／重測 | #1114：「49 specs in zero shards and 49 run twice」 | 未解 open #1114 | 尚待固定同一份 partition 輸入 | **部分**：resolve 鎖 digest＋apply 重驗指紋；CI 共用輸入與測試分片未談 | 若分片，先固定輸入快照／partition manifest，再驗完整且互斥 |
| 暫存資源／權限殘留讓下一次執行壞掉 | #1015 標題：「an interrupted run reddens the next one」；#1032：「reports the next run cannot erase」 | 已解 #995、#997、#1015、#1032 | 結束動詞負責回收；修報告清理／權限 | **部分**：有 docker rm、uid:gid；中斷時 create/cp/tmp 清理未明定 | 所有退出／signal 的清理契約、唯一暫存名稱；保留可恢復 journal 與可刪暫存須區分 |

### E　檔案格式與設定（TOML、.gitignore、conffile 式處理、原子寫入、lock）

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| TOML 讀取失敗被吞；writer／fixture 仍寫 INI，默默回 default | #1164：「empty config handle, every value falls back to its default」；#1165：「Both config writers … still emit INI.」 | 未解 open #1162、#1164、#1165；正文稱 bridge 個案已修 | 修 producer exit 傳遞；writers／fixtures 待改 | **部分**：引擎集中 TOML；stdout 協定安全；未定 parser/writer round-trip | 使用 TOML writer；每次寫後重讀驗證；parser／docker 任一非零不得當空設定 |
| TOML 合法不代表 schema 合法；拼錯 key 默默無效 | #1138：「a typo … silently produces a default value instead of an error」 | 未解 open #1138、#1154 | schema 為待辦 | **部分**：init.toml 合法性、dest 有驗證；version/local／未知欄位未完整定義 | 四類 TOML 明列 schema、未知 key／型別／重複宣告拒絕；保留 first-line 引擎 ref 特殊契約 |
| 通用文字合併成功，語意卻壞了 | #1162：「BOTH merge functions, a duplicated `main()` body」 | 未解 open #1162 | 個案修復；不能靠無 conflict 判正確 | **未避開**：git merge-file 只判文字衝突 | 明示 rc=0 不等於格式／語意正確；合併後解析設定、驗 just，完整下游測試作提交前 gate |
| rename／格式 migration 把資料搬到無 reader 的新檔 | #1163：「Their overrides are no longer applied. Nothing reports the loss」 | 未解 open #1163；分支已停用 migration，功能 open #1168 | 先撤危險 conversion；reader 完成後才恢復 | **部分**：永不刪保住原檔，但舊檔仍在不代表新版會讀 | 工具契約明列 rename／格式變更不可用 copy/append 假裝完成；migration 驗實際生效值 |
| conffile 式「保留客製」和「收到更新」難兼得 | #1093：「the file base does *not* own has drifted, silently」；ADR-32：「only its owner can tell … base plumbing」 | 未解 open #1093；入口分離已解 #945 | 公共機制與客製分離；設定仍漂移 | **部分**：baseline 三方合併更完整；拒絕更新、使用者刪檔、新版新增檔的狀態未全定 | 定義 declined／deleted／unmanaged 狀態、baseline 前推後如何再提案，避免拒絕一次便永久無提醒 |
| 自有薄殼靠被忽略的 hash 判斷歸屬，fresh clone／revert 缺證據 | ADR-6／#1036：「what does a consumer carry … not what did this run write」〔歸屬判斷的同類教訓〕 | 已解 #1036 | 記錄實際 write set，不按檔名認領 | **部分**：hash 比對正確，但 hash 放 gen/.stamp，clone 時不存在 | 歸屬證據改 tracked metadata，或能由舊 ref 重建；定義 stamp 缺失時安全修復 |
| .gitignore pattern 被誤當 pathspec，且把使用者內容認領為工具的 | #1119：「a gitignore pattern is handed to git as a pathspec and the fatal is swallowed」；ADR-25：「present in *both* lists … forever」 | 未解 open #1119；雙名單問題已解 #893 | canonical／retired disjoint；pathspec 缺陷仍開 | **避開**：不 untrack、不操作 index；Q13 只認領實際插入片段，歧義保留 | — |
| 寫檔 alias、mktemp/mv 失敗造成清空 | #187 標題：「saving wipes … to 0 bytes (dst == tpl aliasing …)」；#700：「guard conf-writer mktemp failure」 | 已解 #187、#700、#702 | 修 alias／錯誤路徑及清理 | **部分**：暫存合併＋原子替換；檔案 mode、目的父目錄 symlink 未完整定 | 同 filesystem 暫存；保留必要 mode；寫入前實際路徑檢查；disk-full／rename 失敗驗收 |
| 共享 checkout 併發產生互相覆寫；lock 不能解所有共享状态 | ADR-36：「mutates a shared checkout … leaves the repo in whichever instance's state was generated last」 | 未解 open #1087 | 定案 caller-supplied input/output；尚待實作 | **部分**：flock＋指紋重驗處理合作寫入；工具執行可能與 cache 更換並行 | 規定讀取／materialize 生命週期、cache 原子切換；NO_LOCK 邊界及復原也須受鎖保護 |
| 非互動／EOF 被當 shell crash，輸出重包裝改變 TTY 判斷 | #702 標題：「bare-read EOF crash」；ADR-7：「silently flips the live terminal to JSON」 | 已解 #702、#605 | EOF 處理、啟動時快取 TTY 狀態 | **部分**：v2.2 只互動加 -it；非 CI、無 tty、無 -y 未定 | 明列無 tty／EOF／Ctrl-C 的退出碼與不套用規則；診斷維持 stderr |

### F　文件與流程治理

| base 的問題 | 證據 | base 狀態（已解／未解 open #N） | base 怎麼解 | vendor_kit 避開？（避開／未避開／部分） | 若未避開建議加什麼 |
|---|---|---|---|---|---|
| 定案、原文、amendment 並存，讀者／實作者取到不同契約 | #1035：「Two assertions … both now false」；#1121 標題：「five README and doc statements the tree contradicts」 | 未解 open #1035、#1121；部分 PRD 已修 | ADR amendment、生成／drift guard；仍有缺口 | **未避開**：proposal 仍留 sync 重寫、mode、嚴格 CRLF 等被 Q10–Q13 推翻文字 | 發布單一合併後規範；grilling 留 rationale，舊條文只標 superseded |
| ADR accepted／issue closed 被讀成已交付，跨 repo 接線沒完成 | ADR-8／#952：「the automatic caller has NOT」；#1168：「The specification is complete; the implementation is absent.」 | 未解 open #1168；badge 接線另追 harness#289 | 明列手動替代與外部 issue | **部分**：有 fixture／CI 要求，但 [定] 沒有對應交付證明 | 決策、實作、發布、下游採用分開記錄；每承諾連到行為驗收及可消費 release |
| ADR 平行編號撞號、triage 詞彙無法表達真正阻塞 | #1021：「three parallel branches all took 00000030」；#1180：「Phase B is a different thing wearing the same」 | 未解 open #1021、#1182、#1183 | 編號修復待辦；標籤對齊待辦 | **部分**：五角色＋needs-decision 已定；ADR 併發仍未處理 | ADR 編號配置／合併前修復與引用檢查；不同 readiness 的工作拆票 |
| 衍生數字／清單製造衝突，guard 與實作共用錯誤假設 | ADR-28：「61 conflicted … in `doc/test/`」；#1034：「the counts agree while the page is short」 | 部分已解 #978、#999；未解 open #1024、#1034、#1065 | 從來源生成；移除總數；殘餘仍追 | **部分**：gen 不 tracked 有利；文件、release 完整性規則未定 | 可推導清單不手抄；完整性測試需獨立反例，不能重用同一錯誤 parser |
| 跨 RC 合併把 changelog entry 放進從未出貨的 release | #1039：「the changelog now says rc1 shipped something rc1 does not contain」 | 未解 open #1039、#1103 | 已有重複 heading lint；歸屬與 normalizer 待補 | **未避開**：發布／changelog 整併契約未談 | 依實際 commit/tag 驗 entry 歸屬；release notes 與候選產物同源 |
| 修復提示指向不存在的命令，使用者無法自救 | #1118：「Neither command exists in a dist-era consumer.」 | 未解 open #1118 | 已要求由 consumer 實際命令集合驗提示 | **部分**：Q10 提示 `upgrade vendor_kit`，但該命令自身可能先被 sync 擋住 | 定義管理命令繞過阻塞 sync 的救援路徑；驗 gen 缺席／舊薄殼時能依提示修復 |

### vendor_kit 契約疑似遺漏

此節只列 base 是否遇過及證據；「未見」限附件可見內容，不等於從未發生。離線與 uid:gid 在 vendor_kit 已部分談到，列的是尚未完整界定的情境。

| 情境 | base 是否遇過與證據 |
|---|---|
| git worktree 的 `.git` 是外部路徑檔，容器 bind mount 看不到 | **是**。ADR-29：「a `git worktree` checkout's `.git` is a file naming a path outside the bind mount」。 |
| 從父 repo／子目錄執行，誤判要操作的 repo | **是**。ADR-6／#1036：「wrote the entire resync into a third-party index」；#1173(a) 已移至 docker_harness#310。 |
| monorepo 內多個 `.vendor_kit` 的 root／lock／namespace 邊界 | **未見同型事件**。#195、#199 僅證明 subdirectory build/context 需求，不足證明多套 vendoring root。 |
| 同機多專案共用 Docker daemon／cache／image tag | **是，鄰近同型**。#828 標題：「local :local image tags … collide across repos/versions」；#272：「cache scope to per-(repo, distro, arch)」。未見共用 `.vendor_kit/cache` 的事件。 |
| 完全離線、tar 載入後如何識別／重建 | **有使用情境，未見完整離線升級失敗紀錄**。ADR-24 明列「`docker save`+`load`」；#1155 明列「air-gapped environments」。 |
| proxy／受限 egress／mirror／間歇連線 | **受限 egress 遇過；proxy 本身未見**。#1008 標題：「unbuildable where dl-cdn is blocked」；#1187：「The network is not blocked, it is intermittent.」 |
| locale、語系解析及語系測試失真 | **是**。#103 標題：「returns "zh" for zh_TW locale」；#1117：「one assertion token that cannot tell the locales apart」。 |
| 非 root 容器写入 bind mount、UID／GID／檔案權限 | **是**。open #1188：「files … land owned by an id the field user does not have」；#1032 記錄下一次無法刪除 coverage 產物。 |
| SELinux label／`:z`／`:Z` | **未見直接證據**。#450 的 mount propagation 與 #1188 的 UID 問題不能當作 SELinux 事件。 |
| 在 submodule 內安裝、gitdir 在 superproject 外部位置 | **未見直接事件**。#444 僅有「add submodules input for repos with git submodule source」，證明消費 submodule，未證明工具安裝於其內。 |
| CRLF、特殊字元、路徑空白 | **CRLF 與特殊字元遇過**。#990 標題：「CRLF disarms … backslash continuation」；#688：「metacharacter/quoting gaps」。未見附件直接證明空白 repo 路徑故障。 |
| 容器 CPU quota、shared runner 的資源限制 | **已量測邊界，未稱 live defect**。ADR-8／#1068：「in a container started with `--cpus=2` … it still prints 32」。 |
