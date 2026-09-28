# policy

## 一致
- 六項傾向的方向都可以採用（#3 引用保留、#4 共用 Docker cache、#7 直跳、#9 納入 agent_harness、#10 不做 --migrate、#14 純複製），沒有結構性矛盾。
- #3 的核心是「什麼會被錯刪」：兩邊都指出 multi-arch 陷阱——.version 鎖的是 index digest，底下的 amd64/arm64 子 manifest 在 GHCR 看起來是 untagged，用一般的 delete-untagged（尤其是 GHCR UI 手動或 actions/delete-package-versions）會把還在用的 release 砍掉一個平台。
- #3 兩邊都要求 release tag 不可覆寫、不可移除；已被下游採用的 release image 第一版永久保留；GHCR 30 天可還原只能當退路，不能當回退機制。
- #3 與 #4 不矛盾：GHCR 負責「還拉得到」，本地 cache 負責「少下載」；vendor_kit 不自動 prune，離線缺 image 要明確失敗、不能偷換版本。
- #4 「每 repo 隔離」在只有 Docker+git+just 的主機上沒有可行實作，應寫成排除；範圍要寫準為「同一個 Docker daemon 的 image store」（rootless、不同 context 各有一份）。
- #7 直跳能省掉 v0.42/v0.43 subtree 過渡（避開 ADR-0006 記錄過的事故），但省不掉相容性修改（Dockerfile 路徑、.setup.conf→setup.toml、hooks、workflow）；舊 .base/ 是 git 追蹤的 subtree，要 git rm + .gitignore；跨機制的回退是 revert migration commit，不是改 .version。
- #7 首次 init 對既有檔存的基準是「新模板」，不是 v0.41 的真正祖先，第一次 diff 會退化成 2-way；試點要含全新 clone 驗證。
- #9 agent_harness 是驗證通用性最便宜的第二個工具，但它的檔案分類不能照「Markdown 就是使用者檔」——要按所有權分：隨 image 整批更新的 skills/hooks 留在 .<name>/，AGENTS.md 這類下游會改的走 init 初次複製後只 diff/accept；agent 實際讀哪個路徑要先驗證。
- #10 vendor_kit 不提供 --migrate，也不留空殼旗標；install/init/ensure/diff/accept 永不改寫使用者檔。
- #14 第一版純複製，模板與 baseline 保持位元組一致；需要寫死在靜態檔（如 GitHub Actions 欄位）的值由使用者手動改。
- agy 的 upgrade 研究對本題只有「回退」段可用，且它完全沒研究 image 保留政策，不能拿來當 #3 的依據；報告中 .installed_version、頂層 just init 等說法與已定案的 .stamp、命名空間不符。

## 分歧（含判斷）
- #3 保留規則要不要「掃 downstream 的 .version 歷史」：Claude 的機制更對：把保護根從「引用」換成「tag」，一條規則就涵蓋所有引用，還消掉 codex 擔心的掃描不完整問題。codex 的「第一版不自動刪」我不贊成——把 untagged 清理留給人手才是最危險的操作（base 自己的 ghcr-cleanup.yaml 註解就點名這件事）；但 codex 「刪之前再確認」的精神可以保留為「排程預設 dry-run、看過清單後才用 repo 變數 enforce」。RC tag 第一版一律不刪，不需要 90 天規則。
- #3 清理的動機：Claude 對。public package 免費，版本列表變長只是觀感；決策文字不要用「儲存成本」當理由，免得日後有人為了省錢去刪 tagged。
- #4 digest pull 下來的 image 會不會被一般 prune 清掉：Claude 抓到的這點影響所有 repo 日常，要寫進定案：pull 後補 `docker tag`（tag 不可變所以安全），並在 amd64/arm64、containerd image store 各驗一次。codex 的補充「Docker 不讀 .version、vendor_kit 不自動 prune」也一起寫進去。
- #7 直跳後的人手工作量與一次性遷移腳本：兩者不衝突：腳本產出 migration PR，人審。要把 seed baseline 這招寫進去，因為 v0.41 的舊模板就在 git 裡，是直跳獨有的優勢；codex 說得對的是「seed 的是 v0.41 模板，不是每個 repo 真正的起點」，所以要標明 baseline 來源。另外 codex 提醒的 arm64/Jetson 實機驗收要加進試點驗收。
- #7 遺漏的 `.base/dist/` 路徑契約：這是草稿真正的漏洞，必須先定才能談 #7 和 #10。我偏向 Claude 的 (a) 落到 `.<name>/dist/`：改原型一處，換來 14 個 repo 不用改 COPY，且不違反 ADR-0006 的 forwarder 規則（verify 又禁 symlink，補不了）。
- #10 base 的 migrate 程式碼何去何從：兩者可並存：vendor_kit 契約寫死「永不改使用者檔」（codex），遷移知識歸擁有模板的工具（Claude）。顯式 recipe 不是「自動遷移」，不違反硬限制，還能承接 #7 的一次性遷移，不必扔掉 base 已有的 declarative migrate 程式碼。是否提供由 base 決定，不進 vendor_kit 契約。
- #9 agent_harness 固定路徑檔案的承載方式：codex 的分類原則對，但落地會卡在 Claude 指出的問題：Claude Code 只讀 `.claude/skills/`，東西只放 `.harness/` 讀不到。所以要嘛加 link entry，要嘛 #9 延後。這要問使用者。同時要修正：紀錄 §9 的 image org 寫 ycpss91255-research，repo 在 ycpss91255-docker。
- 回退承諾的定義：codex 這條是必要補強，兩邊合起來寫：回退＝工具版本回退，前提是舊 image 還在（由 #3 的 tag 不刪保證），且要顯示有效版本來源。另外 codex 提的「bootstrap 寫進既有 .gitignore」與「不改使用者檔」的衝突要處理：既有 .gitignore/justfile 只報告缺少內容，不存在時才建。

## 對前例資料的更正
- §1.2 引用的 jdx/mise PR #6258 不存在（GitHub API 404）；同型 Renovate PR 確實存在（如 jdx/mise #13205、#13206），結論方向對，但引用要換成真實編號。
- §1.3 Renovate：regex custom manager 只要 matchStrings 同時抓到 currentValue 與 currentDigest 就會原位一起替換，`autoReplaceStringTemplate` 是可選覆寫；`pinDigests` 是給原本沒 digest 的情況補上用的；docker datasource 預設 versioning 就是 docker。三項都是「可選」被寫成「必須」。
- §1.3 Renovate 範例用 `^` 逐行匹配：regex manager 預設對整份檔案匹配，`^` 不會逐行；.version 第一行是 [tools]，範例可能抓不到；要處理換行邊界並限定只掃 .version，避免更新 baseline metadata。
- Dependabot「只支援 Dockerfile 與 docker-compose.yml」已過時，官方也列出 Kubernetes manifests／Helm charts；「不能更新這份自訂 TOML」的結論仍成立，但理由過度概括。
- §3 Batect `--upgrade` 前例：repo 已 archived、標明 NOT MAINTAINED，最後 push 2023-10；可當歷史前例，不能當「主流工具現況」；#upgrading-batect 錨點無法確認。
- §2 Gradle：「升級必須跑兩次 wrapper」說太滿（官方說一次通常足夠，第二次是為了完整更新 Wrapper 本身）；表格說 `wrapper --gradle-version` 可帶 `-m` dry-run 顯示改動也不對（-m 只是不執行 task action）。該表是推論非實測，引用要打折。
- §4(3) Terraform 回退：還原 `.terraform.lock.hcl` 後只要約束仍允許舊版，跑一般 `terraform init` 就會照 lock 裝舊版；`-upgrade` 反而是忽略 lock 重選最新版。不要把「回退需要額外指令」套到 vendor_kit。
- §4／§5 回退「只改 .version 即生效」漏了前提：舊 image 必須還在 registry（或本機快取）。這正是 #3 要保證的東西，agy 研究完全沒碰 image 保留政策，草稿不能拿它當 #3 依據。
- §5 路徑一／三用的 `.<name>/.installed_version`、`.vendor_kit/.installed_version` 不存在；已定案（issue #20、#23）是 `.<name>/.stamp` 第一行 = --self 傳入的 image 字串。頂層 `just init`、直接調用三方 diff 工具的說法也與命名空間、第一版檔案層級 diff 的決策不符。
- 「覆寫 recipe 後自動由新 recipe 接管」缺機制證明：執行中的 just 不會重新載入已改寫的 justfile，要明確安排刷新後重新啟動 just；升級與降級都要驗。
- 報告內部口徑不一：前面說升級只改版本、延遲安裝，後面手動 upgrade 卻立即 install，兩者不是同一流程，要統一。
- §9 image 名寫 ghcr.io/ycpss91255-research/agent_harness-dist，但 repo 在 ycpss91255-docker org；另外附件的遷移清單是 14 個 v0.41 + jetson_sdk_manager + isaac = 16 個，與題目說的 15 個不符。

## 最終建議
六項傾向都可定案，但 #3 要換機制、#10 要換說法，另外要補兩條草稿沒列的共同契約。建議定案文字：

【#3 image 清理】保護根從「被引用」改為「tag」：GHCR release tag（vX.Y.Z）不可覆寫、不可刪除，release workflow 在 push 前檢查 tag 不存在；清理永不刪 tagged 版本。因此任何 .version（含歷史）與 baseline metadata 指到的 digest 自動保留，回退＝改回 .version 永遠成立，不需要掃 downstream 歷史（也就避開 codex 說的「掃不完整」）。自動清理只做一件事：直接複製 base 的 ghcr-cleanup.yaml（dataaxiom/ghcr-cleanup-action SHA pin、只開 delete-untagged、exclude-tags latest,main,v*、older-than 14 天、validate），排程預設 dry-run，人看過清單後以 repo 變數 enforce，每個 *-dist package 一份。禁止用 actions/delete-package-versions 的 delete-only-untagged 與 GHCR UI 手動清 untagged（會砍 multi-arch 子 manifest）。RC tag 第一版也不刪，人不得把 RC 手寫進 .version。決策理由寫「整潔」不寫「成本」（public package 免費）。誤刪退路：GHCR 30 天可 restore，僅為退路。

【#4 cache】用目前 Docker daemon 的預設 image store 共用（範圍寫準為「同一個 daemon」，rootless 即 per-user）；「每 repo 隔離」寫成排除，不是傾向。啟動器 pull 後必須補本地 tag（`docker tag <ref> <name>:<tag>`），因為 `name:tag@sha256` pull 下來 tag 顯示 <none>，會被不加 -a 的 `docker image prune` 清掉；amd64/arm64 與 containerd image store 各驗一次。vendor_kit 不自動 prune；離線缺 image 明確失敗、不偷換版本；文件寫明 prune -a 後下一個指令會重新 pull，離線用 docker save/load。

【#7 遷移順序】16 個 repo（先確認數量）從現況直接跳新機制，不先走 subtree 升級。遷移由 base 首個 image 版附的一次性腳本（同 bootstrap.sh 模式）產出 migration PR、人工審查：git rm -r .base、加 .gitignore、寫 .version 與 .vendor_kit/、用舊 subtree 的 .base/dist/ 模板 seed baseline（標明來源是 v0.41 模板、非各 repo 真實起點）、印出必改清單。試點：urg_node_humble（v0.41）→ isaac（v0.42）→ jetson_sdk_manager（v0.39，arm64/Jetson 實機）→ 其餘。驗收含：全新 clone 的 install/verify/build/smoke；migration commit 的 git revert（先 rm -rf .base）能回到 subtree 狀態；reusable workflow @tag 更新後 CI 綠。

【#9 agent_harness】納入，作為 base 之後的第二個工具。分類按所有權：隨 image 整批更新的 skills/hooks 留在 .<name>/，AGENTS.md／CLAUDE.md／.claude/settings.json 走 copy、之後只 diff/accept，第一版不做區塊合併。前提：先驗證 Claude Code/codex 實際讀取路徑；若必須在 `.claude/skills/` 等固定路徑，init.toml 需加 `link` 型 entry（進 git 的是 link，verify 禁 symlink 只管 .<name>/ 內部），否則 #9 延到 v2。廢止其自有 init.sh/upgrade.sh；其純字串 .version 改名；image org 改為 repo 所在的 ycpss91255-docker；不得靠 host Python/Node 補安裝。

【#10 --migrate】vendor_kit 永不提供 --migrate、不留空殼旗標；install/init/ensure/diff/accept 永不改寫使用者檔（init 只建不存在的檔；既有 .gitignore/justfile 只報告缺少內容）。遷移知識歸擁有模板的工具：base 可把 dockerfile_migrate.sh／setup_conf_migrate.sh 留在 dist/，以顯式 recipe（如 `just docker migrate`，不掛自動流程、跑前印 diff、使用者主動觸發）提供，要不要提供由 base 決定，不在 vendor_kit 契約內。accept 只代表更新比較基準，不代表已採納變更。

【#14 模板變數】第一版純複製、不渲染、不做條件與可變目的路徑；專案值由工具執行期讀 setup.toml。相容規則同時寫死：baseline 永遠存未渲染字面模板；日後若加渲染，必須是只吃 setup.toml 的純函數，diff/accept 兩邊套同一函數再比，setup.toml 自身不渲染；setup.toml 格式要讓舊版工具可讀（降級才不會炸）。必須寫死在靜態檔的值列清單、由使用者手改。

【補的共同契約 A：.base/ 落地路徑】新機制把 image /dist 直接落到 `.base/`，打破 ADR-0006 的 `.base/dist/…` COPY 契約。建議 vendor_kit 落到 `.<name>/dist/`（改原型 repo_fs 一處，14 個 repo 零 COPY 改動）；否則要寫 ADR 廢止 ADR-0006 該段並在遷移腳本處理 COPY 行。這條要先定，#7 與 #10 的工作量都看它。

【補的共同契約 B：回退定義】「在新機制與受支援契約版本內，改回 .version 後下一次工具指令會安裝並使用該版本；前提是該 digest 仍在 GHCR（由 #3 保證）；不還原使用者檔、baseline、外部狀態或產生物；.version.local 覆蓋時須先解除，指令要顯示有效版本來源；launcher 與 baseline 格式訂雙向相容範圍並驗證升級後再降級。」

## 要問使用者
- `.base/` 落地路徑：vendor_kit 落到 `.<name>/`（現行原型）還是 `.<name>/dist/`（保住 ADR-0006 的 COPY 契約、14 個 repo 不用改 Dockerfile）？這決定 #7 與 #10 的工作量，要最先定。
- 回退承諾接受「只保證工具版本回退，不還原使用者檔／baseline／產生物」這個定義嗎？若要求改回 .version 就整個專案可用，就得另外要求設定向後相容。
- 遷移清單到底是 15 還是 16 個（附件 14 個 v0.41 + jetson_sdk_manager + isaac）？哪些要 Jetson/arm64 實機驗收？
- base 首個 image 版是 v0.43.0 還是 v0.44.0？dockerfile_migrate.sh 的 16 個遷移是否全都在該版模板裡？
- release workflow 要加「tag 已存在就失敗」的檢查嗎？歸 base 的 release-worker 還是 vendor_kit 提供共用 reusable workflow？
- 一次性遷移腳本歸誰附（base release 或 vendor_kit release）？要不要順手做 .setup.conf→setup.toml？
- agent_harness 的 skills/hooks：Claude Code/codex 實際讀哪個路徑？若必須在 `.claude/skills/`，init.toml 的 `link` entry 要列入 v1，還是 #9 延到 v2？
- agent_harness 與 vendor_kit 的 image 放哪個 org（ycpss91255-docker 或 ycpss91255-research）？影響 packages: write 權限與 ghcr-cleanup 的 owner 設定。
- ros_distro／ros2_distro 混用 @v0.41.0／@v0.20.0 的 reusable workflow：base 新版 workflow 還接受舊 layout 嗎？直跳時 Renovate 一起推 @tag 會不會先讓 CI 紅？
- 最低執行環境：Docker（含 containerd image store、rootless）、Compose、just 的最低版本各是多少？Jetson 舊 Docker 是否在支援範圍？
- #14 若日後渲染，變數來源只認 setup.toml 嗎？非 base 工具（如 agent_harness 的 AGENTS.md）也讀 setup.toml？哪些靜態檔（如 GitHub Actions 欄位）的值確定接受人工改？