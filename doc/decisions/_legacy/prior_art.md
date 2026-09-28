# 前例研究 (B/C/D)：能否用現成工具取代 vendor_kit、動詞命名 —— 雙軌分析（2026-09-18）

狀態：**草案，待使用者拍板**。agy 原始輸出：scratchpad/agy/agy_prior_art.md

## 一致
- 兩位都建議方案 3：vendor_kit 自寫，引擎放在容器內，主機只需 docker+git+just；容器內用 Docker 提取（docker create 不啟動 → docker cp → docker rm）拉 dist image，用 git merge-file / diff3 做文字三方合併。
- 沒有任何現成單一工具或兩件組合能同時滿足「OCI 展開、.version 唯一 digest 來源、初始檔三方合併、即時本機覆寫、主機只三工具、arm64」；容器化只解決主機安裝限制，不解決狀態與語意整合的工作。
- vendir 進引擎容器不值得（第一版不裝）：只省下載/展開這一小塊，卻多一份 vendir.lock.yml（第二份版本真相）、容器內 registry 認證/proxy/CA 路徑、多架構 binary 維護。若要用，也只能當「有驗收門檻、可替換的下載後端」。
- Copier 進容器第一版不值得：它的 update 前提是「帶 tag 的 git 範本 repo + 專案是 git + 工作樹 clean」，OCI 拉下的純目錄無法直接餵；還會多出 .copier-answers.yml 與 .version 形成雙真相，並把工具作者綁在 Jinja/copier.yml 範本格式與 Python 引擎 image 上。
- ORAS 不能當既有 docker-built scratch image 的下載器（oras pull 跳過 unnamed layer / 不還原 rootfs）；scratch image 沒 shell，不能 docker run 拷貝，要用 docker create + docker cp。
- 動詞跟 base：update = 只查不套用、upgrade = 套用（含 Renovate 改版後補合併）、預覽用 upgrade --dry-run、本機開發覆寫維持 dev/undev、ensure 只恢復 ignored 產物不碰使用者初始檔。不新增 check/diff/outdated/link/unlink 別名。
- agy 的「update=套用是壓倒性標準」「link/unlink 是黃金標準」統計偏頗：樣本混了不同層次的工具，Cruft 的 link 是「把專案綁到範本」而非本機覆寫，不能當前例。
- Renovate 改 .version 只是改目標版本，不等於初始檔已完成合併；要靠 upgrade 補做、CI 阻擋未整合狀態。
- 自寫量的主體是狀態與生命週期契約（.version 目標版本、baseline 最後合併版本、實際執行來源/dev override、metadata、就緒檢查、gen/tools.just、平台 uid/rootless/WSL2/Jetson 工程），這部分沒有任何現成工具能省。
- git subtree 只當對照，不符 OCI 發布、lock、工具內容不進下游 git 的需求。

## 分歧與取捨
### 證據強度與可引用性
- Claude：有實際查證（Renovate copier/vendir manager 文件、oras 原始碼 pull.go、kustomize PR #6247、vendir v0.46.2 / imgpkg v0.48.1 release、本機 docker 29.8 實測 docker create/cp、Cruft 與 Earthly 停更狀態），並給出具體修正。
- codex：自我聲明全部僅依附件與記憶，未上網查證、未實測；多處以「依據記憶、無法在此驗證」保留，並批評 agy 的連結不足以支持結論。
- 取捨：以 Claude 的查證為準，因為它有一手來源且與 codex 的記憶方向一致（Renovate 原生 vendir manager、Copier 需 git 範本、ORAS 不等於 rootfs 還原）。codex 的價值在於方法論提醒：附件的 HTTP 200 不等於主張成立。定案文件應引用 Claude 查證的具體來源，不再引用 agy 的 404 連結。

### 自寫量能否量化
- Claude：給出相對估計：vendir/crane 只省 10–30 行、Copier 省 150–250 行合併語意但膠水反增 200 行以上；方案 3 為基準 100%。
- codex：認為目前無法合理給出百分比或行數；自寫量由狀態契約決定，須先定 schema、baseline、恢復機制才能估。
- 取捨：取 codex 的謹慎立場對外表述（不寫百分比），但採 Claude 的量級判斷做內部決策依據：「下載/展開」確實是 docker 一行的事，「合併語意」是中等，「狀態/平台工程」是大頭。這足以支撐「不引入 vendir/Copier」的結論，不需要精確行數。

### vendir 的定位
- Claude：直接判定「不值」，唯一例外是 dist image 全部公開且引擎不掛 docker socket，即使如此仍建議主機用 docker 拉。
- codex：不完全排除，列四項採用門檻（展開現有 scratch image、完全服從 .version、通過私有 GHCR/多架構/Jetson/WSL2 驗收、確實刪掉一整塊自維護程式），未達門檻前不裝。
- 取捨：採 codex 的「門檻式」寫法記入決議（避免日後再爭），但實務結論同 Claude：以現有需求（單一 OCI image 來源、主機已有 docker）幾乎不可能過第四項門檻，因此第一版不裝，也不預留 vendir.yml 生成路徑。

### dist image 由誰拉
- Claude：明確建議由主機薄啟動器用 docker create/cp 拉（與拉引擎 image 同一條認證路徑、享 daemon 快取），引擎容器只做邏輯，不掛 docker socket。
- codex：只提「Docker 負責提取」，未指定主機端或容器端，但強調啟動器必須先讀 .version 找到引擎、且不能偷偷要求主機有 jq/yq/flock。
- 取捨：採 Claude 的分工：主機薄啟動器（純 POSIX sh，只用 docker pull/create/cp/run/rm）負責拉 dist 與引擎 image；引擎容器負責 TOML 解析、合併、metadata、flock。這同時滿足 codex 的「解析在引擎內、主機不加工具」要求。唯一要小心的是薄啟動器需要從 .version 讀引擎 tag@digest，因此啟動器只能用 grep/sed 取這一個 key，不能解析整份 TOML。

### 「update=只查」與 apt 語意的對應是否嚴格
- Claude：把 update=只查、upgrade=套用直接對應到 apt/brew/pacman/dnf 慣例，作為跟 base 的正當性依據。
- codex：指出這只能稱「沿用 base 慣例」：apt update 會刷新本機索引（有寫檔），不等於完全不寫檔。
- 取捨：codex 的細節對，但不影響決策。對外文案寫「與 just base 同義：update 只查、不改任何專案檔」，不再引用 apt 當論據，避免被挑語病。update 若要寫快取（例如記錄最後查詢結果）只能寫在 ignored 的 metadata 目錄。

### 跨架構 digest 與初始檔一致性
- Claude：提出 dist image 單架構（固定 --platform linux/amd64 拉、純資料不需 emulation）或多架構 index 兩條路，指出 Renovate 追的是 index digest。
- codex：進一步要求：若鎖多架構 index digest，必須確認兩個平台的 dist 內容相同，否則同一 .version 可能產生不同初始檔。
- 取捨：採 Claude 的「純資料 image 發單架構 + 固定 --platform linux/amd64」方案：只有一份內容、一個 digest，直接消除 codex 擔心的不一致，也讓 Renovate regex 追的 digest 與實際拉到的 manifest 一致。多架構只保留給引擎 image。

## agy 說法查證（站不住腳處）
- Copier：Renovate 有原生 copier manager（docs.renovatebot.com/modules/manager/copier/），比對 .copier-answers*.yml 並執行 copier update；agy 引用的 discussions/742 已 404，結論錯。
- Copier 真正的障礙不是「無 OCI 來源」，而是 update 要求範本是帶 tag 的 git repo、目標專案是 git repo 且工作樹 clean；且 _commit 不保證是完整 SHA、更不是 OCI digest，answers 檔會成為第二份版本真相。
- Copier 沒有 --dry-run，對應旗標是 -n/--pretend。
- vendir：Renovate 有原生 vendir manager（支援 helmChart/git/githubRelease/http），但不支援 image/imgpkgBundle 來源，所以對本案仍需 regex——agy 結論碰巧對、理由錯。另 imgpkg bundle 與一般 image 是不同契約，不能拿 pull -b 範例證明對 scratch image 相容。
- vendir 無三方合併、有 linux-arm64 release 兩點正確（v0.46.2、imgpkg v0.48.1，2026 年仍活躍），但「每次清空全部目錄」需依設定確認；建目錄預設 0700 需顯式設 permissions；directory 來源是「複製」不是「指向」，不等於即時 dev mode；arm64 binary 存在不等於 Jetson/WSL2 已驗收。
- Kustomize 不支援 oci:// remote resources（PR kubernetes-sigs/kustomize#6247 仍 open、issue #5134/#6130 未關）；那是 Flux OCIRepository 的能力。
- link/unlink 只在 JS 生態（npm/yarn/pnpm/bun）成立，且 npm link 是兩步驟、npm unlink 歷史上等同 uninstall；Cruft 的 cruft link 是「把既有專案綁到範本」，沒有 cruft unlink。其他生態各有命名（go replace、cargo [patch]、nix --override-input、helm file://、dagger install ./path、pre-commit try-repo）。
- Cruft update 沒有 --template-path 選項；Cruft 最後 release 2.16.0（2024-12-25）後無任何 push，不宜當活躍前例。
- ORAS 拉不到 docker-built scratch image（cmd/oras/root/pull.go：無 org.opencontainers.image.title 的 unnamed layer 會被跳過）；ORAS artifact 與 docker image 發布格式二選一。scratch image 無 shell 不能 docker run 拷貝，正確做法是 docker create <img> <dummy-cmd> + docker cp（docker 29.8 實測，需給假 command）。
- pre-commit 與 nix 的 Renovate manager 都是預設停用、需 opt-in；Dependabot 對 pre-commit/helm/devcontainers 只有 version updates、無 security updates。「原生」對，「深度/預設」誇大。
- Dagger 沒有 dagger.lock，pin 記在 dagger.json dependencies；且 dagger update 是「套用新版」，是 agy 漏列的 update=套用前例。
- Earthly 已被原公司放棄維護（2025-07-16 Earthly Cloud 停止、開源只收 critical fix），Renovate 也沒有 earthly manager，不宜當前例。
- 「update=套用是壓倒性標準」統計偏頗：只選了專案級 lockfile 工具，漏掉 apt/brew/pacman/dnf（update=更新索引、upgrade=套用）與 mise upgrade/outdated；且 agy 建議的動詞集（add/sync/update/diff/check/link/unlink/remove）與已定案的「指令極少、dev/undev 以 devmode.md 為準、diff = upgrade --dry-run」相牴觸。
- check/diff/--dry-run 不是同一件事的三個名字：check 可為驗證、diff 是內容差異、dry-run 是某動作的預演；nix flake check 也不是查新版。
- 「主機需 Python/額外 binary 所以淘汰」只適用直接裝主機；放進引擎容器可繞過主機限制，代價轉為 image 大小、依賴維護、認證與跨架構驗證——agy 低估了這條路，但評估後仍不採用。
- 「19 類工具沒有全支援 → 生態不存在替代品」推論過強，正確表述是「已調查的候選中尚未證明有工具能直接滿足全部契約」。
- 「開 PR = 三方合併」「有 lock = OCI digest 鎖定」「本機來源 = dev mode」是整份報告反覆出現的能力混淆，每個前例都要按本案契約重新評估。

## 最終建議
採方案 3：vendor_kit 自寫，但只寫「本案特有的狀態與所有權契約」，成熟工具負責三件事——Docker 負責拉與展開（主機薄啟動器用 docker pull/create/cp/rm，與拉引擎 image 同一條認證路徑、享 daemon 快取；不掛 docker socket）、容器內 git merge-file --diff3（或 diffutils diff3 -m）負責文字三方合併核心、Renovate 一條 regex manager（docker datasource、currentValue+currentDigest）同時追工具 image 與引擎 image。第一版不把 vendir、crane、imgpkg、Copier 放進引擎；vendir 以 codex 的四項驗收門檻記入決議作為日後重評條件。dist image 發單架構純資料 image、固定 --platform linux/amd64 拉，避免多架構 index 帶來的 digest 與內容不一致；引擎 image 才做多架構。動詞跟 base：update 只查（--exit-code 有新版回 2，最後一行固定提示「套用：just vendor_kit upgrade」）、upgrade 套用、upgrade --dry-run 預覽、dev/undev 本機覆寫、ensure 只恢復 ignored 產物；不新增 check/diff/outdated/link/unlink。自寫需明訂的部分：三方合併的檔案層級語意（新增/刪除/使用者已刪/改名/二進位/symlink/多工具同路徑）、baseline 與待完成操作的持久化與恢復、薄啟動器只用 grep/sed 從 .version 讀引擎 key 而不解析整份 TOML、uid/gid 與 rootless/Podman/WSL2/Jetson 的偵測矩陣。決議文件引用 Claude 查證的一手來源，移除 agy 的 404 連結與 apt 類比論據。

## 要問使用者
- dist image 與引擎 image 在 GHCR 是公開還是私有？私有時是否接受主機 docker credential helper 為唯一認證路徑（引擎容器不另傳 token）？
- 「純資料、不含可執行程式」限制是否只適用工具 dist image？引擎 image 含 git（alpine git，只用 merge-file 不碰專案 .git）與 shell 是否可接受？
- dist image 是否同意發單架構（linux/amd64）並固定 --platform 拉？還是必須多架構 index？
- 硬性平台矩陣：一般 docker、rootless docker、Podman、WSL2+Docker Desktop、Jetson（docker.io 或 docker-ce，是否保證 buildx/compose plugin）——哪些必須支援、哪些明確不支援？
- dev 模式是 symlink `.<repo>/ → 本機 checkout` 還是 `.version.local` 路徑覆寫？本機 checkout 是否可能在專案目錄外（含空白路徑、WSL 的 Windows 檔案系統）？這決定 bind-mount 契約。
- 三方合併第一版的支援邊界：二進位、symlink、權限、改名、多工具提供同一路徑——哪些支援、哪些直接報錯？使用者主動刪除的初始檔靠 metadata 記錄還是靠「baseline 有、現況無」推斷？
- Renovate PR 只改 .version，還是要連初始檔合併結果一起產生？若只改版本，由誰跑 upgrade、CI 在哪一步阻擋未整合狀態？
- base 的 update/upgrade 語意是否已固定？若 base 未來改名，是否同意 vendor_kit 同步改、並兩邊加同一行提示文案？
- 「不用自己寫 repo」的目標是減少維護量，還是完全不維護任何整合程式？後者在現有硬限制下無法達成，需確認接受前者。

---
## 附：Claude 分析原文
建議採方案 3：以 Docker 處理既有 scratch image（create 不啟動容器 → docker cp → 清理），以容器內 Git 合併文字初始檔；vendir 作為「有驗收門檻的可替換下載後端」，第一版不預設加入 Copier 或 imgpkg。這不是「所有東西自己寫」：自寫的是本案特有的狀態與所有權契約，成熟工具負責下載、檔案提取及文字合併。

可取代性表（✅ 已有能力；△ 需轉接／自寫／指定平台驗收；❌ 缺少或不符。「digest 鎖定」要求服從 .version；「本機覆寫」要求 checkout 修改即時生效）：

| 組合 | OCI image 展開 | digest 鎖定 | 初始檔三方合併 | 即時本機覆寫 | 主機僅三工具 | arm64 | 缺什麼 | 自寫量 |
|---|---|---|---|---|---|---|---|---|
| 主機 vendir＋必要時 imgpkg | ✅ | △ | ❌ | △ | ❌ | △ | 合併、唯一來源轉接、dev 契約 | 高，且違反主機限制 |
| 容器 vendir＋Git 合併 | ✅ | △ | △ | △ | ✅ | △ | baseline、檔案生命週期、恢復、啟動器 | 中至高 |
| 容器 vendir＋Copier | ✅ | △ | △ | △ | ✅ | △ | OCI→模板版本轉接、雙方狀態整合 | 高 |
| 容器 Copier 單獨 | ❌ | ❌ | ✅ | ❌ | ✅ | △ | OCI、digest、工具 dist 與 dev 管理 | 高 |
| Docker 提取＋容器 Copier | ✅ | △ | △ | △ | ✅ | △ | Copier 版本轉接與整合狀態 | 中至高 |
| ORAS＋just，對既有 scratch image | △ | △ | ❌ | △ | △ | △ | image rootfs 語意、合併、引擎與恢復 | 高 |
| **Docker 提取＋容器 Git＋vendor_kit** | ✅ | △ | △ | △ | ✅ | △ | 本案特有的狀態與生命週期 | **中；責任範圍最直接** |
| git subtree | ❌ | ❌ | ✅ | ❌ | △ | △ | OCI 與本案部署模型 | 要符合就需大改 |

沒有一列目前可以據附件直接宣布「六項全過、不用自己維護 repo」。容器化能消除主機安裝障礙，不能消除語意整合工作。

vendir 放進引擎的採用門檻（四項）：(1) 能展開現有 scratch image，不要求改發行格式；(2) 完全依 .version 的 digest 工作，其設定與 lock 都可重新產生；(3) 通過私有 GHCR、amd64／arm64 index、Jetson／WSL2 實際驗收；(4) 相較 Docker 提取後端確實刪掉一整塊自行維護的程式與錯誤分支。若只支援單一 OCI image 來源且主機本來已有 Docker，vendir 增益可能有限；要多來源、內容篩選或複雜同步才較可能值得。目前不能合理給出省多少百分比或幾行程式。

動詞建議：
| 需求 | 建議 | 理由 |
|---|---|---|
| 只查可用新版 | update | 與同專案的 just base update 一致；明寫「只查、不套用」 |
| 套用或補做待合併版本 | upgrade | 延續附件 3 契約，避免兩個命名空間相同動詞產生相反副作用 |
| 預覽實際升級變更 | upgrade --dry-run | 包含版本、初始檔及 baseline 的操作計畫，不另開 diff |
| 本機開發覆寫 | dev／undev | 表達用途，且已有草案契約；不把實作綁成 symlink |
| 自動恢復 ignored 產物 | ensure | 不解析新版、不寫使用者初始檔 |

outdated 適合全新獨立產品的新版查詢介面，但本案沒有足夠理由新增別名；check 易與完整性／CI 驗證混淆，diff 不等於版本查詢，link/unlink 未被附件證明比 dev/undev 更合適。另外這只能稱作「沿用 base 慣例」：嚴格來說 apt 的 update 會刷新本機套件索引，不等於完全不寫檔。

## 附：codex 分析原文
## 結論：採方案 3（自寫，引擎在容器內），容器內只借 `git merge-file`（或 diffutils `diff3`）當合併核心；**不要**把 vendir/crane/Copier 放進引擎容器。動詞跟 base（apt 語意）：`update`=只查、`upgrade`=套用；本機覆寫維持 `dev`/`undev`。

### (B) 可取代性表（六項：①拉 OCI 純檔案 image 展開到目錄 ②lock 鎖 digest（且 .version 唯一來源）③初始檔三方合併 ④本機路徑覆寫 ⑤主機只需 docker+git+just ⑥arm64）

| 組合 | ① | ② | ③ | ④ | ⑤ | ⑥ | 缺什麼 | 自寫量（相對方案 3） |
|---|---|---|---|---|---|---|---|---|
| 1. vendir(+imgpkg) 裝在主機 | ✓ | △ 有 lock 但是第二份（vendir.lock.yml），.version 要唯一來源就得棄用 | ✗ 全量覆寫 | ✓ directory（複製非指向） | ✗ 要裝 binary | ✓ | 三方合併、初始檔、gen/tools.just、就緒檢查、.version 對映全要自寫；Renovate vendir manager 不吃 image 來源 | 只省 docker create/cp 的 ~10 行；其餘 ≈ 100% |
| 2. Copier + ORAS/docker cp + 膠水 | ✗ ORAS 拉不到 docker-built scratch image（unnamed layer 跳過）；改 docker cp 才 ✓ | ✗ 自寫 .version；Copier 另有 .copier-answers.yml 雙真相 | ✓ 但要求範本是帶 tag 的 git repo、專案 git clean | ✓ | ✗ 需 Python | ✓ | OCI→git repo 偽造、answers↔.version 同步、範本格式改造 | 省合併 ~150–250 行，膠水反而 +200 行以上 |
| 3. 自寫 + 容器內 git merge-file | ✓ docker create+cp（實測） | ✓ .version 唯一 | ✓ 自寫檔案語意，核心用 merge-file | ✓ .version.local | ✓ | ✓（引擎 image 多架構） | 無 | 100%（基準），其中合併演算法不用寫 |
| 3b. 3 + 容器內 vendir/crane 拉 image | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 多綁：容器內 registry 認證/proxy/CA、無 daemon 快取、binary 多架構 | 省 ~10–30 行 |
| 3c. 3 + 容器內 Copier 合併 | ✓ | △ 雙真相 | ✓ | ✓ | ✓ | ✓ | 多綁：Python image、Jinja 範本格式、偽造 git repo、容器內對專案跑 git | 省 ~150–250 行 |
| 4. git subtree（對照） | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | 正是要擺脫的問題 | 0 |

沒有任何現成工具或兩件組合能同時勾①②③⑤（agy 這個結論對）。關鍵新發現：**「拉 OCI 展開」在主機端本來就是 docker 一行的事**（`docker create <img@digest> /x && docker cp c:/dist/. .repo/ && docker rm`，docker 29.8 實測可行，落地檔擁有者為執行者），所以 vendir/crane 在這個架構裡幾乎沒有可省的東西；真正花工的是三方合併的檔案語意、就緒檢查、gen 生成與平台工程（uid、rootless、WSL2、Jetson），這些沒有現成工具能包。

### 「現成工具放進引擎容器」值不值得
- **vendir/crane 進容器：不值。** 省 10–30 行，換來第二條認證/網路路徑（主機 docker credential helper 進不了容器；GHCR 私有 image 要另外傳 token；proxy/CA 要進 image）、失去 daemon image 快取、多一組 binary 的多架構下載與版本追蹤。前提唯一例外：dist image 全部公開且引擎容器不掛 docker socket——那時 `crane export` 是最乾淨的一行；但即使如此，仍建議由主機薄啟動器用 docker 拉，跟拉引擎 image 同一條路徑。
- **Copier 進容器：第一版不值。** 它省的是最容易寫的部分（檔案層級合併語意），綁上的是最難拆的部分（Python image、Jinja 範本格式、範本必須是 git repo+tag、專案必須 git clean、.copier-answers.yml 雙真相）。
- **值得借的只有 `git merge-file --diff3`（或 `diff3 -m`）**：現成、穩定、多架構、alpine 內 20MB，衝突標記與 git 一致，使用者用熟悉的方式解衝突。自寫的部分收斂為：baseline 清單 × 現況 × 新版的四種情況（三方都有→merge-file；新版新增→使用者沒有就建立、有就以空 base 合併並標衝突；新版刪除→使用者未改就刪、改過就保留並警告；使用者已刪→維持刪除並記 metadata）。

### (C) 動詞命名
1. **update/upgrade 跟 base（apt 語意）**：`update` = 只查不動檔（`--exit-code` 有新版回 2，供 CI），`upgrade` = 套用（含 Renovate 之後補合併）。理由：(a) 同一批使用者在同一個 justfile 裡同時打 `just base …` 與 `just vendor_kit …`，兩個命名空間語意相反比偏離生態系更糟；(b) 失誤方向：update=只查時，被生態系慣例帶偏的人打 `update` 只會得到 no-op 加一行提示；反之若 update=套用，被 base 訓練過的人打 `update` 會意外觸發三方合併——寧可錯在安全的一邊；(c) apt/brew/pacman/dnf 都是這個語意，不是 base 獨創；agy 的「壓倒性」只統計了專案級 lockfile 工具。配套：`update` 輸出最後一行固定印「套用：just vendor_kit upgrade」；生態系的 `check`（cruft check）= 我們的 `update --exit-code`，`diff` = `upgrade --dry-run`，`outdated` = `update`，一律不另開動詞。若將來 base 改名，兩邊同步改。
2. **只查不套用的名字**：就是 `update`（同 base）。不加 check/diff/outdated 別名（指令極少）。
3. **dev/undev 優於 link/unlink**：`link/unlink` 的「黃金標準」只在 JS 生態成立，且 npm link 是兩步驟、`npm unlink` 歷史上=uninstall，Cruft 的 `link` 根本是另一件事（把專案綁到範本）。`dev <repo> -p <path>` 直述意圖（我在開發這個工具）、不暴露實作（symlink 或路徑覆寫），與 devmode.md 已定案一致；`undev` 雖非常見英文但無歧義。維持不變。

### (D) agy 站不住腳的說法
見 agy_claims_wrong；最重要的四條：Copier 其實有 Renovate 原生 manager（agy 說沒有，引用的 URL 也 404）；Copier 的真正障礙不是「無 OCI」而是「範本必須是帶 tag 的 git repo、專案必須 git clean」；vendir 無三方合併與 arm64 release 兩點正確（v0.46.2 / imgpkg v0.48.1，2026 年仍活躍），但 Renovate 其實有 vendir manager（只是不吃 image 來源）；ORAS 拉不到 docker-built scratch image、kustomize 不支援 oci://（PR 仍 open）、Cruft 停更 21 個月、Earthly 已被原公司放棄維護。