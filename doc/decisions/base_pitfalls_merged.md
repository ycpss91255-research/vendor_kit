# base 踩過的坑 × vendor_kit 設計 —— 雙軌合併結論（2026-09-19）

輸入：`base_pitfalls.md`（Claude）、`base_pitfalls_codex.out.md`（codex）；對照 `proposal_v2.md`（v2.1–v2.3）與 `grilling.md`（定案優先）。
查證：兩份引用的 137 條 base issue 全部以 `gh issue view`（含留言）抓回、38 條 ADR + PRD + changelog CONVENTIONS 以 `gh api contents` 抓回，逐句比對。✔ = 原文與狀態（open/closed）核實。ADR = `doc/adr/<n>`；#N = base issue。
層別：**契約**＝要使用者拍板的對外承諾；**ADR**＝機制；**測試**＝驗收／CI；**文件**＝文件治理。

## 1. 雙方一致「未避開」或「部分」、證據成立

| # | 問題 | 證據 | 雙方建議合併版 | 對我們契約要加的條文 | 層 |
|---|---|---|---|---|---|
| 1-1 | 沒有支援下限，也沒寫「Y 可改什麼、相容項何時可刪」；太舊的呼叫端拿到協定錯誤而不是「你太舊」（Claude A1/C5 部分＋未避開；codex A1 部分） | ✔ #1055「The support floor is v0.43.0. Nothing released before it is owed upgradability」；✔ #1049 open「the refusal does not say so」；✔ ADR-6 2026-08-25 修正「lockstep is necessary but NOT sufficient for any path an ALREADY-RELEASED caller names」 | 凍結 bootstrap.sh／薄殼→引擎介面；明列支援下限；Y 不得改介面 | 「引擎子命令與 `vk-resolve/1` stdout 協定對支援下限（第一個正式版）以後所有已出貨的 bootstrap.sh／薄殼保證相容；Y 版不得改此介面、只有 X 可；引擎遇到低於下限的薄殼或 version.toml 印『請以 bootstrap.sh 重建』而非協定錯誤。」 | 契約 |
| 1-2 | 升級測試「新對新」：fixture 從候選樹複製、驗收只用剛 build 的引擎 + 乾淨 fixture，跨版相容永遠沒被測；滑動窗口讓 guard 到期（Claude C4 未避開；codex C1 未避開） | ✔ #1048 open「the test asserted the new layout against itself」；✔ #1041 open「A compatibility obligation is permanent; a sliding window expires」「It goes BLIND, and it also lies」；✔ #1084 open；✔ #772 open | 用**已釋出**薄殼驅動候選引擎、連升兩次、集合＝下限以後全部釋出版（非固定 N） | 「驗收 fixture 由支援下限以後**每個已釋出** `bootstrap.sh` 建立，再升到候選引擎並對任一動詞連續執行兩次；禁止由候選樹複製 fixture。」 | 測試 |
| 1-3 | 升級後的 repo ≠ 全新安裝的 repo，無人比對（Claude C4 建議；codex C 部分） | ✔ #1057 open「is the upgraded repo what a fresh one would be」；✔ #1044 closed（個案） | 收斂檢查 | 「升級到 vN 的 fixture 與用 vN 全新 install 的 fixture，`.vendor_kit/` 內 tracked 內容必須相同；使用者初始檔的差異需有 metadata 紀錄。」 | 測試 |
| 1-4 | 升級悄悄在使用者 CI 目錄建新檔、無法拒絕；write-once 初始檔把內部路徑凍成外部契約（Claude A6 未避開；codex A 部分） | ✔ #1078 open「writing into that directory is not a neutral act」「goes from green to red purely by upgrading」；✔ #1111 open「becomes indefinitely frozen for every repo」；✔ #1082 open | upgrade 新增檔要問、可拒絕、dry-run 明列、CI 路徑醒目；初始檔只可引用穩定公開路徑 | 「§5 加一列：upgrade 遇新版新增的初始檔 → 問『要建 X 嗎』（`-y` 建；拒絕記入 metadata），摘要獨立列『新建』，dest 在 `.github/`、`.gitlab-ci.yml` 等 CI 路徑時 dry-run 與摘要另加醒目行；初始檔內只可引用 `just vendor_kit …` 與 `.vendor_kit/ci/check.sh`、`.vendor_kit/entry.just`、`.vendor_kit/version.toml` 這組宣告為 protocol-stable 的路徑，禁引 `cache/` 內部路徑。」 | 契約 |
| 1-5 | add 時已存在→不納管→永不提醒；「沒認出任何形狀」與「沒事可做」輸出一樣；拒絕一次就永久失聯（Claude C7/E6 部分；codex A/E 部分） | ✔ #1093 open「one stale ancestor, copied once at bootstrap and never re-synced」；✔ #1189 open「'I did not recognise this tree' must be distinguishable from 'nothing here needed changing'」；✔ ADR-32「only its owner can tell an added bringup line from base plumbing」 | 定義 managed／unmanaged／declined／deleted 狀態；dry-run 與 check.sh 印差異一行不動檔；baseline 前推後再提案一次 | 「metadata 記每個初始檔狀態（managed／unmanaged／declined／deleted-by-user）；`upgrade --dry-run` 與 `check.sh` 對 unmanaged／declined 檔各印一行『與範本差異 N 行』但不動檔；被拒絕的變更在下一個新版仍再問一次。」 | 契約 |
| 1-6 | `import` 撞名是硬錯誤、整個 `just` 掛（連 remove 都跑不了）；未檢查使用者根檔既有 recipe／保留名（B1 雙方部分） | ✔ ADR-10「a single `build:` collision would break *every* recipe」「A duplicate recipe name across `import` is a hard error」；✔ #594 | 寫入前用實際根 justfile 驗解析 | 「install／add／upgrade 在任何寫入前以使用者實際根 justfile（just 1.33.0 `--summary`／`--dump`）驗解析；撞到 `vendor_kit` 保留名或工具 namespace → 拒絕並印名單。」 | ADR |
| 1-7 | just 多來源版本漂移；`latest` 臂在沒人動 repo 的日子變紅；工具 repo 的 `<ns>.just` 沒說用哪版驗（B2 雙方部分） | ✔ #948「37 minors across four paths」「A parsing change turns the suite red on a day nobody touched the repo」；grilling Q8：1.42.0–1.42.2 回歸 | dist 用 1.33.0 驗；latest 非 required；ADR 記壞版 | 「`check.sh --dist` 以 just 1.33.0 解析每個 `<ns>.just`；CI `latest` 臂非 required（紅了開 issue）；ADR 列已知壞版（1.42.0–1.42.2），提高下限時跳過。」 | 測試 |
| 1-8 | GHCR package 寫權綁在建立它的 repo；兩 publisher 搶同一 tag；reusable workflow permissions 相交（D3 雙方部分） | ✔ #980 closed「intersecting away the caller's packages: write」；✔ #1176 open「denied: permission_denied: write_package」「two armed publishers of one rolling tag」 | 每 package 唯一 publisher | 「工具 repo 文件：`<repo>-dist` package 由該 repo 首推建立、每 package 唯一 publisher，勿在他處先建同名；引擎 image 同。」 | 文件 |
| 1-9 | fork PR 跑到 self-hosted、guarded skip 讓 required check 空綠（D5 雙方未避開） | ✔ ADR-26「a claim that the commit was fully tested; on a fork PR that claim is false」；✔ #766 closed | 由 `runs-on` 靜態推導 + fork guard + 單一 rollup | 「vendor_kit 自身 CI：required check 只有一個 rollup；self-hosted 資格由 `runs-on` 靜態推導並 lint；fork PR 的 guarded skip 令 rollup 紅。」 | ADR |
| 1-10 | 測試在受測物被刪後仍綠；guard 的 population／subject 手寫；驗收用 stub 而非產品路徑（Claude F7 未避開；codex D 部分＋未避開） | ✔ #953「260 tests pass when their subject is deleted」；✔ #1090 open「DECLARED, not DERIVED」；✔ #1175 open「Three of the four probes … verify nothing」；✔ #1163「paths the tests themselves chose rather than the paths production uses」 | 存在性 fail-closed；刪 subject 必紅；禁 stub | 「驗收固定用真 `bootstrap.sh` + 真引擎 image，禁 stub 引擎；每個 guard 的集合由樹推導，刪掉受測物或破壞產物必須紅。」 | 測試 |
| 1-11 | TOML 讀取失敗被吞、拼錯 key 靜默取預設；version.toml「第一行＝引擎 ref」是隱性格式契約（Claude E2 部分；codex E 部分） | ✔ #1164 open「every value falls back to its default」；✔ #1138 open「a typo … silently produces a default value instead of an error」；✔ #1181 open「load-bearing」 | 四類 TOML 明列 schema；未知 key 拒絕；啟動器取第一行要健壯 | 「version.toml／version.local.toml／init.toml／metadata 四類 TOML 各列 schema，未知 key、型別錯、重複宣告 → 1；啟動器以 `grep -m1 '^vendor_kit *='` 取引擎 ref、找不到 → 1 明確訊息；引擎寫回固定格式並重讀驗證。」 | ADR |
| 1-12 | 派生數字手寫進文件（頁數、模組數、測試數）製造衝突與失真（F3 雙方部分） | ✔ ADR-28「of 65 such merges, 61 conflicted」；✔ #1024、#1034、#1065 open | 只寫規則不寫數量 | 「PRD／ADR 不寫可由樹推導的數量；需要時由 lint 產生。」 | 文件 |
| 1-13 | changelog：BREAKING 含 migration、700 字、跨 RC 切點條目歸錯版（F4 雙方未避開） | ✔ CONVENTIONS「Migration instructions belong inside the BREAKING entry they serve」；✔ #1039 open「the changelog now says rc1 shipped something rc1 does not contain」；✔ #1103 open | 沿用 CONVENTIONS + 歸屬由 tag 驗 | 「沿用 base CONVENTIONS（七類、700 字、BREAKING 內含 migration、每 0.Y 一檔）；entry 歸屬依實際 tag 驗；release notes 與候選產物同源。」 | 文件 |
| 1-14 | release cadence／fanout 噪音；分類看行為不看 label（C6 雙方部分） | ✔ ADR-27「The label is not the signal」「one bug 17 PRs」；✔ ADR-31「A refusal prints nothing on stdout」 | ADR 記 cadence；Renovate 範例含分組 | 「ADR 記：引擎 image 每版一 tag、bootstrap.sh 隨版；Z 不通知、X/Y 才在 changelog 展開 BREAKING；README 的 Renovate 範例含分組／排程與『需人工合併』提示。」 | ADR |
| 1-15 | 從父目錄／巢狀 repo 執行，把整包寫進第三方 index（Claude A9 部分；codex 遺漏表「是」） | ✔ ADR-6 2026-09-04 修正（#1036）「wrote the entire resync into a third-party index」；✔ #719 closed | `$PWD` 必須是 toplevel | 「install／add／upgrade 要求 `$PWD == git rev-parse --show-toplevel`，否則 1；一個 repo 只允許一個 `.vendor_kit/`；子目錄／monorepo 列 v2。」 | 契約 |

## 2. 只有一方提到、證據成立

| # | 來源 | 問題 | 證據 | 建議 | 條文 | 層 |
|---|---|---|---|---|---|---|
| 2-1 | Claude | tag 可打在通過 CI 但不在 main 的 commit（C3 未避開） | ✔ #1143 closed；✔ #1124 closed | tag ruleset + tag-on-main | 「repo 設 `v*` tag ruleset（required = CI rollup）；release job 先驗 `git merge-base --is-ancestor <tag> main`。」 | 測試 |
| 2-2 | Claude | 程式碼註解放 issue 號會腐爛（F2 未避開） | ✔ ADR-13「an inline `#N` is a frozen pointer to a transient artifact」 | 同規則 + lint | 「程式碼註解只留 ADR 引用，lint 擋 `#N`；規格檔不受限。」 | 文件 |
| 2-3 | Claude | ADR 編號無人分配、三分支同拿 30（F1 未避開；codex 列「部分」，見 3-9） | ✔ #1021 open「three parallel branches all took 00000030」 | 編號 = issue 號或「後合者改」 | 「ADR 編號 = 該決議的 issue 號；README lint 擋重複。」 | 文件 |
| 2-4 | Claude | `just --list` 只取 mod 上方緊鄰一行註解（B3 部分） | ✔ #720 closed | gen 每行 mod 上方產註解 | 「gen/tools.just 每行 `mod` 上方產一行註解（init.toml `description`，缺則 `<repo> vX`）。」 | ADR |
| 2-5 | Claude | module recipe 預設 cwd 是 module 檔目錄；`justfile_directory()` 指向未實測（B5 部分） | ✔ ADR-10「a module recipe's default cwd is the module file's own directory」 | 1.33.0 實測寫 ADR | 「以 just 1.33.0 實測 mod 內 `justfile_directory()` 指向並記入 ADR；`check.sh --dist` lint 擋相對 working-directory。」 | 測試 |
| 2-6 | Claude | 未文件化環境變數改變行為（E5 部分） | ✔ #895 closed；✔ ADR-25 §9「a typo'd path silently yielded an EMPTY config」 | README 列全 + lint | 「README 一節列出全部 `VENDOR_KIT_*` 與 `CI`；lint 擋未列者。」 | 文件 |
| 2-7 | Claude | local 檔命名慣例 base 已改 `<name>.toml.local`（E4 部分） | ✔ #1161 closed「Rename setup.local.toml to setup.toml.local」；✔ ADR-3「the standard name is ours; a suffix marks a local variant」 | 對齊 | 「local 覆寫檔名 `version.toml.local`；`.vendor_kit/.gitignore` 與 `check.sh`（拒絕被 track）雙保險。」 | 契約 |
| 2-8 | Claude | Dependabot／Renovate 看不到自訂 pin，`tag@digest` 一行要同時更新兩欄（C9） | ✔ #822 closed | README regex manager 範例 | 「README 附 Renovate regex manager 範例，同時擷取 `currentValue` 與 `currentDigest`。」 | 文件 |
| 2-9 | Claude | 網路間歇失敗被讀成打包錯誤且每次重付；pull 失敗分類未寫（D4 部分） | ✔ #1187 open「The network is not blocked, it is intermittent」；✔ #1008 closed | 錯誤三分類 + 離線提示 | 「啟動器 `docker pull` 失敗印原文 + 三分類（網路／認證／不存在）+『離線可用 `--local`』；cache 與印記相符時不 pull，明寫『無網也能 just』。」 | ADR |
| 2-10 | Claude | 手維護名單腐爛（自有 tracked 檔清單出現在 install／sync／uninstall／check.sh 四處）（F6 部分） | ✔ ADR-26「decayed three separate times」；✔ ADR-33「It was that there were copies」 | 一處定義 | 「自有 tracked 檔清單只在 launcher-gen 模組定義一次，其餘呼叫它。」 | ADR |
| 2-11 | Claude | PRD 衝突優先序要附 worked example（F5 部分） | ✔ PRD「an invariant is not a property that can give way」 | 用 Q10 當例 | 「PRD 衝突優先序附一例：『永不覆蓋 vs 自動化』以 Q10 定案為 worked example。」 | 文件 |
| 2-12 | codex | 通用文字合併 rc=0 但語意壞了 | ✔ #1162 open「BOTH merge functions, a duplicated `main()` body」 | 合併後驗語意 | 「`git merge-file` rc=0 不等於正確：合併後對 TOML／just 類目標重新解析，解析失敗 → 2 並留原檔。」 | ADR |
| 2-13 | codex | rename／格式遷移把資料搬到無 reader 的新檔，舊檔仍在不代表新版會讀 | ✔ #1163 open「Their overrides are no longer applied. Nothing reports the loss」；✔ #1168 open | 工具契約禁假完成 | 「工具契約：初始檔 rename／格式變更不得以 copy/append 假裝完成；`check.sh --dist` 驗遷移後實際生效值。」 | ADR |
| 2-14 | codex | 修復提示指向使用者沒有／被擋的命令 | ✔ #1118 open「Neither command exists in a dist-era consumer」 | 管理命令繞過 sync | 「`install`／`upgrade vendor_kit` 不被 sync 的薄殼檢查擋（v2.3 §2 已寫）；驗收加『gen 缺席／舊薄殼下依提示能修復』案例。」 | 測試 |
| 2-15 | codex | 非互動／EOF／無 tty 無 `-y` 的行為未定 | ✔ #702 closed「bare-read EOF crash」；✔ ADR-7「silently flips the live terminal to JSON」 | 明列退出碼 | 「無 tty 且無 `-y` 又需詢問 → 1 印清單（同 CI）；EOF／Ctrl-C 視為拒絕、不套用；診斷維持 stderr。」 | 契約 |
| 2-16 | codex | 歸屬證據放 gen/.stamp，fresh clone 時不存在 | ✔ #1036 closed；✔ ADR-6「what does a consumer carry … not what did this run write」 | 可重建的歸屬證據 | 「薄殼 hash 由 version.toml 第一行的引擎決定性重算；gen/.stamp 缺席時 `upgrade vendor_kit` 以重算值比對，不視為被改。」 | ADR |
| 2-17 | codex | registry cleanup 刪到 live manifest 子 digest；pin 了 digest 不保證 registry 保留 | ✔ #1089 open「deletes the per-arch children of a LIVE tag」；✔ #813 closed | 保留政策 | 「已發布 index digest 與其子 digest 不刪（供 `git revert` 用）；工具 repo 文件同句。」 | 文件 |
| 2-18 | codex | just 入口沒被任何測試驅動 | ✔ #1042 open「21 of 43 `just` recipes are not driven by any test」 | 由 `just --list` 推導集合 | 「驗收集合由 vendor.just 實際列出的動詞推導，含 help、參數轉發與失敗碼。」 | 測試 |
| 2-19 | codex | completion 到不了 module | ✔ #788 open「returns NOTHING」 | 只承諾實測組合 | 「文件只承諾實測過的 shell × just 補全組合。」 | 文件 |
| 2-20 | codex | 定案、原文、amendment 並存，讀者取到不同契約 | ✔ #1035 open「both now false」；✔ #1121 open | 單一合併規範 | 「proposal 被 grilling 推翻的段落標 superseded；發布單一合併版 PRD。」 | 文件 |
| 2-21 | codex | ADR accepted／issue closed 被讀成已交付 | ✔ #1168 open「The specification is complete; the implementation is absent」；✔ ADR-8 | 分開記錄 | 「每條 [定] 連到行為驗收與可消費 release；決策／實作／發布分開標。」 | 文件 |
| 2-22 | codex | CI 跑到 stale 工具 image；變更偵測漏 COPY 輸入 | ✔ #1166 open；✔ #1171 open；✔ ADR-33 | 所有 build inputs 觸發 | 「工具 repo 的 dist image 重建以 `dist/` 全部檔案為觸發；驗收驗剛 build 的 digest，不靠版本字串。」 | 測試 |

## 3. 雙方判定不同

| # | 問題 | Claude | codex | 裁定與依據 |
|---|---|---|---|---|
| 3-1 | 跨版遷移放錯執行點（#1110、#1097） | 避開：邏輯全在目標版引擎 image，from/to 都在 metadata | 部分：自身升級仍由現有版本啟動；接手點與 schema migration 未定 | **部分**。v2.3 §2 已定「舊引擎只改第一行 → 啟動器同次 pull 新引擎 → 新引擎跑 `upgrade vendor_kit`」，接手點有了；但 metadata／baseline schema 跨多版（vN→vN+3）如何遷移未寫。✔ #1110 open「mutually exclusive by construction」。條文：「metadata 帶 schema 版號；引擎對下限以後任一 schema 皆可讀並就地升級」→ ADR。 |
| 3-2 | 通知機制靠升級本身送達（#927） | 避開：不出 bot、只查不推 | 部分：Renovate 自選、未保證接通 | **避開**。✔ #927 的缺陷是 monitor 隨 init.sh 出貨；我們 update／Renovate 都在升級路徑之外。codex 的「明示未接 bot 就沒有主動通知」採為文件一句，不改判定。 |
| 3-3 | rc／latest 發布順序（#1109、#1012） | 避開：釘 tag@digest、sync 不查最新 | 部分：供應側「驗完再打 tag」未寫 | **部分（供應側）**。下游確實避開；但 ✔ #1109 open「`:latest` moved 5 minutes 58 seconds before that tag's tests had a verdict」是供應側流程，proposal §7 仍是 release→release-test。條文：「候選 digest 先過 release-test，才打正式 tag 與上傳 bootstrap.sh asset；失敗不進可選版本」→ 測試。 |
| 3-4 | bootstrap 用不相關檔判斷新舊 repo（#928） | 避開：解析路徑不硬寫 | 部分：copy 已存在即略過，完成標記不驗交付項 | **部分**。✔ #928 open「Bootstrap itself succeeds … zero dangling symlinks」；metadata 完成標記若只記「add 跑完」，不會知道哪些檔因已存在被略過。條文：「完成標記列每個初始檔的結果（created／skipped-exists／appended／declined）」→ 併入 1-5。 |
| 3-5 | dist 內 binary／glibc（#1149） | 避開：兩平台一致等於不能放 binary；建議明寫 | 部分：dist 可含 binary、執行環境未限 | **部分**。「兩平台內容一致」只是 CI 檢查的副作用，契約沒說。雙方建議同：條文「dist 只放純資料，不承諾可執行；`check.sh --dist` 拒絕 ELF」→ 契約（工具 repo 承諾）。 |
| 3-6 | 暫存／中斷清理（#1015、#995） | 避開；附建議 mktemp 於結束／失敗都刪 | 部分：signal 時 create/cp/tmp 清理未定 | **部分**。v2.2 進度日誌覆蓋 apply 內中斷，但啟動器側 `docker create` 容器與 `<tmp>` 在 SIGINT 時的回收沒寫。✔ #995「468 base- compose networks」。條文：「啟動器 trap EXIT/INT 刪 `<tmp>` 與暫存容器；可恢復 journal 與可刪暫存分開」→ ADR。 |
| 3-7 | 寫檔失敗／假「已恢復」（#700、#187） | 避開；附建議「恢復失敗要印未恢復」 | 部分：mode、父目錄 symlink、disk-full 未定 | **部分**。✔ #187「dst == tpl aliasing」、✔ #700「false 'restored'」。條文：「原子替換同一 filesystem、保留 mode；恢復步驟失敗印『未恢復：檔名』；驗收含 disk-full／rename 失敗」→ 測試。 |
| 3-8 | flock 邊界（ADR-36、#1087） | 避開；建議逾時印持鎖 PID | 部分：工具執行與 cache 更換並行；NO_LOCK 邊界 | **部分**。✔ ADR-36「mutates a shared checkout」。sync 換 cache/ 時另一個 `just <tool>` 正在讀 cache 是可能的。條文：「cache/<repo>/ 以整目錄 rename 原子切換；復原也拿鎖；逾時印持鎖 PID 與時間」→ ADR。 |
| 3-9 | ADR 編號撞號（#1021） | 未避開 | 部分（五角色標籤已定、ADR 併發未處理） | **未避開**。標籤與編號分配是兩件事；vendor_kit doc/adr/README 沒有分配規則。採 2-3。 |
| 3-10 | 容器 uid／HOME（#1188、ADR-24） | 避開（`-u uid:gid`）；附註 HOME 未寫 | 部分 | **部分**。✔ #1188 open「owned by an id the field user does not have」；引擎以任意 uid 跑、無 passwd 項時 git／HOME 行為未寫。條文：「引擎 `-e HOME=/tmp`；只用不需身分的 git 子命令；驗收加 uid 12345 案例」→ 測試。 |
| 3-11 | 自身升級後薄殼 hash 比對（Q10）與 fresh clone | Claude C8 避開（不 stage／不 commit） | codex 部分（hash 在 gen/.stamp，clone 時不存在） | 兩人談不同面向，皆對。C8 避開成立；codex 點採 2-16。 |

## 4. 引用查證失敗或誇大

| 方 | 條 | 實際情況 |
|---|---|---|
| Claude | A3 #1086 引「the population still carrying the old path is exactly the population on v0.41.0 … their vendored driver has never heard of the migration」 | 非原文，是改寫。原文：「A consumer at v0.41.0 -- the population the migration exists for -- runs the v0.41.0 script, which has never heard of it.」語意相同。 |
| Claude | A9 #719 引「silently scaffolds a repo there」 | 非原文。原文：「init.sh then scaffolds a full new repo into that parent」。語意相同。 |
| Claude | A9／§G-3「ADR-6 第四次修正」寫進第三方 index | 編號錯：該段在 2026-09-04 by #1036 的修正（第五次）；第四次是 2026-08-25 by #915（Claude A1 引的「lockstep … NOT sufficient」在此，正確）。 |
| Claude／codex | 同一 #1163 各引不同段：Claude「paths the tests themselves chose」（F7）、codex「Their overrides are no longer applied」（E） | 兩句皆為原文 ✔；issue 標題是「just upgrade silently disables a downstream operator's .env.local overrides」，codex 的用法貼近主旨，Claude 引的是留言中的附帶結論，證據力較弱但成立。 |
| codex | 遺漏表「#1173(a) 已移至 docker_harness#310」 | 實際為 `ycpss91255-docker/dockerharness#310`；細節無誤。 |
| codex | 遺漏表 #1155「air-gapped environments」當離線情境證據 | #1155 是 rename 變數 issue，句子存在但只是提及；codex 自己已標「未見完整離線升級失敗紀錄」，不誇大。 |
| codex | ADR-29 引 worktree `.git` 是檔 | 原文存在 ✔，但 ADR-29 主題是 early-return function shape，該句是其中例子；引用成立、出處不直覺。 |
| 兩方 | 其餘全部引用（issue 原文／狀態、ADR、PRD、CONVENTIONS） | 逐句核實 ✔，無虛構。 |

## 5. 契約疑似遺漏清單（合併去重）

| 情境 | base 是否遇過（證據） | 我們契約目前 | 建議處理 |
|---|---|---|---|
| git worktree：`.git` 是檔、`gitdir:` 指向 `$PWD` 外，容器 bind mount 看不到 | 是 ✔ ADR-29、#893「Two worktrees of the same repo cannot be run at the same time」、#1032 | 沒有 | **第一版要定**：引擎容器內不讀 `.git`（只 `git merge-file`）；git repo 檢查全在主機做 |
| submodule 內安裝（同上 `.git` 檔） | 未見直接事件（#444 只證消費 submodule；#1077 consumer 是 `--recurse-submodules` clone） | 沒有 | **明寫不支援**（v1），同 worktree 條處理後自然可用則移 v2 |
| monorepo／巢狀 repo／子目錄安裝、多個 `.vendor_kit/` | 第三方 index 事件 ✔ ADR-6/#1036、#719；多套 root 未見 | 只有「dest 不得越出 repo」 | **第一版要定**（1-15）：toplevel 限定、一 repo 一個；子目錄列 v2 |
| 同機多專案共用 daemon／image；拉過的工具 image 無回收動詞 | 是 ✔ #828、#887、#995「468 … networks」、#388 | 每專案各自 cache/，不共享 | **明寫**：第一版不共享下載、不回收 image；回收動詞列 v2 |
| 完全離線／air-gapped 的 upgrade | 有情境（ADR-24 `docker save`+`load`；#1155 僅提及） | `--local` 只覆蓋 bootstrap／add | **明寫不支援**：第一版 upgrade 需網路；離線 upgrade 列 v2 |
| proxy／受限 egress／間歇連線／企業 CA／自簽 registry | 受限與間歇 ✔ #1008、#1187；proxy 未見 | `docker pull` 走 daemon；引擎容器內 resolve 直連 registry，proxy env 未談 | **第一版要定**：resolve 階段以 `-e` 傳 `HTTP_PROXY/HTTPS_PROXY/NO_PROXY`；自簽 CA 列 v2 |
| locale／時區／訊息語言 | 是 ✔ #103、#1117、#210、#151 | 沒有 | **第一版要定**：訊息單一語言；metadata 時戳 UTC |
| 非 root／任意 uid、HOME 缺席、rootless docker、Docker Desktop／WSL2 uid 映射 | uid 是 ✔ #1188、#1032；rootless／Desktop 無紀錄 | `-u uid:gid`、WSL2 支援 | **第一版要定** HOME 與無 passwd 案例（3-10）；rootless／Podman **明寫未驗證** |
| SELinux `:z`/`:Z` | 無（兩方 grep 皆零） | 沒有 | **明寫未驗證** |
| `-t` 指舊版（薄殼新、引擎舊；或 `upgrade vendor_kit -t` 比薄殼舊） | 是 ✔ #916「a hardcoded new path breaks bootstrapping an OLD tag」 | 只談向前（1-1） | **第一版要定**：引擎比薄殼舊 → 1 拒絕並印「請用該版 bootstrap.sh」 |
| `.gitattributes`／CRLF／mode bit 在薄殼 hash 比對 | 是 ✔ #990 | #29 已開；hash 是否忽略 mode／CRLF 未寫 | **第一版要定**：hash 只比內容、CRLF/LF 等價（同 Q13）、mode 變更只 warn |
| SIGINT／signal 清理；`docker pull` 卡住逾時 | 是 ✔ #1015、#1014、#1187（240 秒） | 進度日誌覆蓋 apply 中斷 | signal 清理 **第一版要定**（3-6）；pull 逾時列 v2 |
| 非 tty／EOF／無 `-y` 非 CI | 是 ✔ #702、ADR-7 | 只互動加 `-it` | **第一版要定**（2-15） |
| 路徑含空白／metacharacter | metacharacter 是 ✔ #688；空白路徑未見 | 沒有 | 驗收加含空白與 `$` 的 repo 路徑案例（測試） |
| 引擎 image 基底 EOL | 是 ✔ #1030 open（到期 2026-11-02） | 沒有 | 列 v2（時間觸發的 EOL 檢查） |
| 同名 package 由別 repo 先建；公開不可逆 | 是 ✔ #1176 | Q7 只提後者 | 第一版文件加一句（1-8） |
| Renovate 對 `tag@digest` 的更新 | 是 ✔ #822 | 未寫範例 | 第一版 README（2-8） |
| 就地升級與全新安裝收斂 | 是 ✔ #1057 | 沒有 | 第一版測試（1-3） |
| 容器 CPU quota／runner 資源 | 已量測 ✔ ADR-8「--cpus=2 … it still prints 32」 | 不適用（引擎無平行測試） | 不列 |

## 6. 給使用者拍板的題目（契約層、雙方一致）

1. **支援下限與 X/Y 可改範圍**：支援下限 = 第一個正式版；Y 不得改薄殼↔引擎介面；低於下限印「請以 bootstrap.sh 重建」。建議：**採**。依據 ✔ #1055、#1049、ADR-6。
2. **upgrade 遇新版新增初始檔**：問「要建 X 嗎」（`-y` 建）、可拒絕並記錄、dest 在 CI 路徑時醒目；初始檔只可引用 protocol-stable 路徑集合。建議：**採**。依據 ✔ #1078、#1111。
3. **不納管／被拒絕檔的狀態與提醒**：metadata 記四種狀態；dry-run／check.sh 印「與範本差異 N 行」不動檔；新版再問一次。建議：**採**（與不變量「永不覆蓋」相容，只印不動）。依據 ✔ #1093、#1189、ADR-32。
4. **`$PWD` 必須是 toplevel、一 repo 一個 `.vendor_kit/`**；子目錄／monorepo 列 v2。建議：**採**。依據 ✔ ADR-6/#1036、#719。
5. **dist 只放純資料、不承諾可執行**（工具 repo 契約）。建議：**採**。依據 ✔ #1149。

單方提出的契約層題（不在本節）：2-7 `version.toml.local` 檔名（Claude）、2-15 非 tty／EOF（codex）、§5「`-t` 指舊版」（Claude）——建議一併於同次拍板。

**直接採納清單（ADR／測試／文件，不需拍板）**：
- ADR：1-6 根檔撞名預檢；1-11 四類 TOML schema + 第一行 grep；1-14 cadence；2-4 mod 註解；2-9 pull 失敗分類；2-10 清單單一定義；2-12 合併後重解析；2-13 工具遷移不假完成；2-16 hash 可重算；3-1 metadata schema 版號；3-6 signal 清理；3-8 cache 原子切換與鎖邊界。
- 測試：1-2 已釋出薄殼驅動候選引擎、連升兩次；1-3 升級＝全新收斂；1-7 dist 用 1.33.0 驗、latest 非 required；1-9 單一 rollup + fork guard；1-10 真 image 禁 stub、刪 subject 必紅；2-1 tag ruleset；2-5 cwd 實測；2-14 修復路徑案例；2-18 動詞集合推導；2-22 build inputs 觸發；3-3 先驗後 tag；3-7 disk-full／rename 失敗；3-10 uid 12345；§5 空白路徑案例。
- 文件：1-8 唯一 publisher；1-12 不寫派生數字；1-13 CONVENTIONS；2-2 註解不放 issue 號；2-3 ADR 編號 = issue 號；2-6 環境變數列全；2-8 Renovate 範例；2-11 PRD worked example；2-17 digest 保留；2-19 補全承諾；2-20 superseded 標記；2-21 決策／交付分開；§5 各「明寫不支援／未驗證」句。
