OpenAI Codex v0.153.4
--------
workdir: /home/cyc/Desktop/vendor-kit_ws/src
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a0b577-cc0f-7902-b0e6-649702b48b9a
--------
user
你是架構審查員。附件一是 vendor_kit 的契約與定案，附件二是 base（同一組織的前一個專案，用 git subtree 把共用工具散播到下游，vendor_kit 就是為了取代這個機制而生）的 PRD、全部 ADR、issue（含開著的）與 changelog。
請找出：base 過去踩過（或現在還開著沒解）的問題，哪些在 vendor_kit 的設計裡會再踩、哪些已避開、哪些部分避開。每條要附證據（ADR 編號／issue 編號 + 一句原文摘錄）。
分組：A 傳播機制（subtree／init.sh／upgrade.sh／symlink／使用者改檔）；B just 分層與版本；C 升級／回退／自動 release／Renovate；D CI／runner／多架構／registry 認證；E 檔案格式與設定（TOML、.gitignore、conffile 式處理、原子寫入、lock）；F 文件與流程治理。
輸出表：base 的問題｜證據｜base 狀態（已解／未解 open #N）｜base 怎麼解｜vendor_kit 避開？（避開／未避開／部分）｜若未避開建議加什麼。
最後一節「vendor_kit 契約疑似遺漏」：從 base 經驗推，我們契約還沒談到的情境（worktree、monorepo 多個 .vendor_kit、同機多專案共用 cache、離線、proxy、locale、非 root 容器寫檔權限、SELinux、submodule 內…），只列 base 是否遇過與證據。150 行內。

注意：附件全部貼在本訊息內，不需要也無法讀取本機檔案或網路；請直接依附件內容作答，以繁體中文輸出 Markdown。


---

# 附件一：vendor_kit 目前設計

## decisions/proposal_v2.md

# vendor_kit 對外契約與架構 —— v2（2026-09-18 grilling 定案版；此檔取代 proposal_v1.md）
標記：**[定]** = 使用者已拍板；**[待]** = 仍待拍板（畫成便條）。占位符 `<repo>` = 工具 repo 名（例子一律用 `<repo>`，不要寫 base）。

## 0. 目的與角色 [定]
工具 repo 把 dist/ 打包成 GHCR image；下游專案靠 `bootstrap.sh` + `just vendor_kit add/upgrade/dev` 拿到工具、跟上新版、本機開發工具本身；其餘自動。角色：工具 repo 開發者（供應側）／使用者（下游專案，每天打 just）／vendor_kit 開發者；契約只對前兩者承諾。**自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file（行內合併）；第一版不放 vendir/Copier**（依據：無單一工具全包四項；vendir 只省 docker 三行；Copier 要求範本是帶 tag 的 git repo）。

## 1. 不變量（PRD 層）[定]
**vendor_kit 對使用者的檔：可以建（但要明確說明建立或修改了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋。** 「永不覆蓋」= 不用工具版本取代使用者客製內容。自動化（sync）只碰不進 git 的東西。Never fail silently（結束狀態 0/1/2）。

## 2. 使用者介面 [定]
兩層成對：專案層 `install`↔`uninstall`（vendor_kit 自己），工具層 `add`↔`remove`；`update`（只查）/`upgrade`（套用）跟 base（apt 語意）；`dev`↔`undev`；`sync` 自動前置。codex 已審：install/uninstall、sync 同意。

| 動詞 | 參數 | 反向 | 做什麼 | 結束狀態 | 組 |
|---|---|---|---|---|---|
| `bootstrap.sh` | `--tool <repo>`（可重複）`-t/--tag` `-y/--yes` `--local <image tag 或 tar>` `-h` | （呼叫 `uninstall`） | **薄層**：檢查 git repo、檢查 just ≥ 1.33（不足印下載＋安裝指令）、`docker pull` 內嵌的引擎 ref（`--local` 則用本機 image／先 `docker load`）→ 呼叫引擎 `install` → 對每個 `--tool` 呼叫 `add`。再跑一次 = 呼叫 install（冪等修復）。不自刪。取得方式：README 連 `releases/latest/download/bootstrap.sh`；每版 `releases/download/vN/bootstrap.sh`；離線包見 #27 | 0；1 不留半成品 | 一次性 |
| `install` | `-y` `--no-justfile` | `uninstall` | 把 vendor_kit 裝進**這個** git repo：建 `.vendor_kit/`（version.toml 第一行引擎 ref、entry.just、vendor.just、.gitignore、ci/check.sh、baseline/）；根 justfile：**無 → 建**（`import '.vendor_kit/entry.just'` + `default: @just --list`）、**有 → 問**「要加這一行嗎」（`-y` 直接加並印出）；再跑 = 修復薄殼（冪等）；非 git repo → 1 提示 `git init`（不代做）。`install <repo>` 誤用 → 提示 `add` | 0／1 | 進階（bootstrap 代打） |
| `uninstall` | `-y` `-n/--dry-run` | `install` | 逐工具 remove → 刪 `.vendor_kit/` 全部（含 version.toml、local）→ 根 justfile 那行：**問**「要刪這一行嗎」，只刪與我們寫的完全相同的行；初始檔保留並印清單 | 0／1 | 進階 |
| `add <repo>` | `-t/--tag`（預設最新）`-s/--source <image>` `--local <tar>` `-y` `-n/--dry-run` | `remove` | 寫 version.toml 一行（tag@digest）→ materialize（拉 image、展開到 cache/<repo>/、印記）→ 初始檔：**無 → 建**；**有 → 不納管**（印「已存在，範本在 cache 可自行比對」）；`mode="append"` 的檔（.gitignore 類）：無→建、有→**問**「要加這幾行嗎」→ append 並印出；建 baseline/<repo>/ + metadata（完成標記、append 過的行）→ 重生 gen/tools.just；已接入且完成 → 0 無變更；`-t` 與鎖定不同 → 1 提示 upgrade | 0／1（不動 version.toml） | 常用 |
| `remove <repo>` | `-y` `-n/--dry-run` | `add` | 有 dev 覆寫 → 1 提示先 undev；刪 version.toml 行、cache/<repo>/、baseline/<repo>/、gen recipe；初始檔**永不刪**，印清單；append 過的行：**問**「要刪我們加的這幾行嗎」，只刪原文相同的；未接 = 0 + 提示 | 0／1 | 進階 |
| `update [<repo>]` | `--exit-code` | （upgrade 的前一步） | 只查 GHCR，不動任何檔；末行固定「套用：just vendor_kit upgrade」；拒絕未知參數 | 0；1 查詢失敗；`--exit-code` 有新版 2 | 進階 |
| `upgrade [<repo>]` | `-t/--tag`（限單一）`-y` `-n/--dry-run` | `git revert` 整組 commit | 先補「version.toml 已到 B、baseline 仍 A」的待合併 → 查最新（或 -t）→ 改 version.toml → materialize → **逐檔判斷後詢問**（見 §5）→ 推 baseline + metadata → 摘要。不帶 repo = 全部含 vendor_kit 自身（自身變了：換薄殼 + gen，停下要求重跑）。無 baseline → 1 提示 add | 0；1 不動 version.toml；2 有衝突（留標記、印檔名；baseline 仍推到新版；解完重跑直到乾淨） | 常用 |
| `dev <repo>` | `-p/--path <dir>`；`dev vendor_kit -i/--image <tag>` | `undev` | 工具必須已在 version.toml（否則 1）；寫 version.local.toml `<repo> = "path:<dir>"`；cache/<repo>/ 改 symlink 指向 `<dir>/dist`；印記 `path:<dir>`；sync 看到覆寫就跳過 pull/verify；CI 拒絕。**自身**：`-i <本機 image tag>`（只能 tag 不能 digest：docker load 後無 RepoDigests，實測）→ version.local.toml `vendor_kit = "<tag>"`；驗收測試用同一機制 | 0／1 | 常用 |
| `undev <repo>` | — | `dev` | 刪 version.local.toml 該行 → 重新 materialize；未啟用 = 0 + 提示 | 0 | 進階 |
| `sync [<repo>]` | —（`CI=1` 自動 frozen） | — | 每次 just 自動前置：**只寫 gitignore 路徑**（cache/、gen/）；引擎 ref ≠ gen/.stamp → 用新引擎重寫薄殼 + gen 後**退出 1 統一印「vendor_kit 已更新 vX → vY，請再跑一次剛才的指令」**（不自動續跑：just 一開始即載入定義）；印記 ≠ version.toml → materialize；verify sha256 失敗 → 重裝 + warn；metadata 無完成標記 → 1「請 add」；baseline 落後 → 本機 warn 提示 upgrade、CI → 1 印指令；範圍預設全部工具 | 0／1 | 進階 |
| `help`／`h` | — | — | 命名空間層說明（just 做不到 `just vendor_kit --help`）；各動詞 `--help` 由引擎印 | 0 | — |

不開：`init`（→ install）、`ensure`（→ sync）、`diff`（= `upgrade --dry-run`）、`accept`（解完衝突重跑 upgrade）、`rollback`（git revert）、`--repair`（= 再跑 install）、`--purge`。動詞 recipe 一律 `verb *args` 一行轉發（`set positional-arguments` 在 vendor.just）、放 tracked vendor.just；`[group('常用')]`/`[group('進階')]`；entry.just 與 gen/tools.just **只含 mod/import?，零 set 零 recipe**（實測：被 import 檔的 set 會外溢到根檔）。引擎內部步驟名：materialize（拉 image 展開，非對外）。

## 3. 專案裡的檔 [定]
```
專案/
├── justfile                      # 使用者的；install 只加一行（問／-y）
└── .vendor_kit/                  # 根目錄只多這一個
    ├── version.toml              # 進 git：唯一來源。第一行 vendor_kit = "ghcr.io/…/vendor_kit:vN@sha256:…"；[tools] 一行一工具 tag@digest
    ├── version.local.toml        # 不進 git：dev 覆寫（path:<dir> 或本機 image tag）
    ├── .gitignore                # 進 git，我們自己的：cache/ gen/ version.local.toml .tmp.*
    ├── entry.just                # 進 git：mod vendor_kit 'vendor.just' + import? 'gen/tools.just'（零 set）
    ├── vendor.just               # 進 git：動詞 recipe 一行轉發 + sync 前置
    ├── ci/check.sh               # 進 git：下游 CI 契約檢查
    ├── baseline/<repo>/          # 進 git：上次合併的範本副本
    ├── baseline/<repo>/.vendor_kit.toml   # 進 git：metadata（來源 ref@digest、最後合併版本、完成標記、append 過的行、衝突中檔案）
    ├── gen/                      # 不進 git：tools.just（mod <ns> '../cache/<repo>/just/<ns>.just'）、.stamp（引擎 ref）
    └── cache/<repo>/             # 不進 git、使用者不可改：files/、init.toml、just/<ns>.just、.stamp（第一行 index digest 或 path:）
```
**不碰**：使用者 `.gitignore`、`.git/info/exclude`。「會碰使用者東西」只有：根 justfile 一行、初始檔（§5）。[待] version.toml 檔名（vs lock.toml）— 建議 version.toml。

## 4. 工具 repo 要交的 [定]
`dist/files/`、`dist/init.toml`（`[[file]] src/dest [mode="copy"|"append"]`，dest 相對專案根）、`dist/just/<ns>.just`（每檔一個頂層命名空間，數量工具自決，`<repo>.just` 必須存在；跨工具撞名 add 時報錯）、`Dockerfile.dist`（FROM scratch + COPY dist/ /dist/）。image `ghcr.io/<org>/<repo>-dist:<tag>` **多架構 amd64+arm64（同一次 buildx、COPY-only；CI 驗兩平台內容一致；印記記 index digest）** #26。工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根（禁止相對 working-directory）。初始檔禁止以整檔覆蓋方式指向根 .gitignore/.dockerignore/.editorconfig（要用 mode=append）。公開／私有工具自決 [定 Q7]。

## 5. 初始檔規則（同不變量）[定]
| 時機 | 情況 | 做法 |
|---|---|---|
| add | 檔不存在 | 建（印出建了什麼） |
| add | 檔已存在 | 不納管、不覆蓋，印「已存在，範本在 cache」 |
| add（mode=append） | 檔已存在 | 問「要在 X 加這幾行嗎」→ append，記在 metadata |
| upgrade | 新版沒改／你的檔已等於新版 | 不動 |
| upgrade | 新版改了、你沒改（D==B） | 問「X 換成新版？」→ 換 |
| upgrade | 兩邊都改 | 問「你和新版都改了 X，要三方合併嗎？」→ `git merge-file --diff3`；衝突留 `<<<<<<<`、回 2；baseline 仍推到新版 |
| upgrade | 新版刪除該檔 | 不刪，只 warn |
| upgrade（append） | 找到上次加的行（原文相同）| 問後替換；找不到 → 不動、印新內容 |
| remove/uninstall | 任何 | 永不刪初始檔，印清單；append 行問後只刪原文相同的 |
`upgrade --dry-run` 只印會問哪些檔；CI 無 `-y` 又需改檔 → 1 印清單。二進位／symlink 不合併：使用者未改才換、改過保留 + warn。

## 6. 啟動器 ↔ 引擎 [定]
啟動器（POSIX sh，只用 docker pull/create/cp/run/rm + grep/sed）：grep version.toml 第一行取引擎 ref（local 覆寫優先）→ gen/.stamp 不符 → 用新引擎重寫薄殼+gen → 退出 1 統一提示 → 每工具 `docker create <image> /x` + `docker cp c:/dist/. <tmp>/` + `docker rm`（多架構 index，不帶 --platform，daemon 挑原生；docker ≥ 19.03）→ `docker run --rm -u uid:gid -v $PWD:/repo -v <tmp>:/dist/<repo>:ro <引擎> <子命令> …`。引擎子命令：install/uninstall/add/remove/update/upgrade/dev/undev/sync/help；內部 materialize/verify/merge。flock 專案目錄 60 秒、`VENDOR_KIT_NO_LOCK=1`。引擎 image 公開；多架構。

## 7. CI [定]
下游 CI（GitHub/GitLab 只呼叫）`.vendor_kit/ci/check.sh`：sync（frozen）→ verify → `upgrade --dry-run` → 工具測試（`just <repo> check` 若有）→ 專案測試。**Renovate**（下游自選，vendor_kit 不出 bot）：PR 只改 version.toml 一行；**PR 的 CI 以新版跑完整流程——一行改動本身不可能出錯，不構成通過依據**；需合併 → 1 印「本機 `upgrade <repo> -y` 後 push」→ 人補完 push 後全部再跑（Renovate 預設不動有人推過的分支；PR body 警告勿勾 rebase）。vendor_kit 自身 CI：env-test → test-base → lint/unit/install/merge → release → release-test（amd64、arm64 原生 runner）→ **驗收：剛 build 的引擎 image + 乾淨 fixture repo 跑完整流程**；just 矩陣 1.33.0 + latest；lint 擋比 1.33 新的功能（ADR 記破壞性變更）。

## 8. 架構模組（引擎）[定]
1 version（version.toml/local 讀寫、flock）2 registry（GHCR tag/digest 查詢）3 materialize（展開 image、印記、verify）4 init（初始檔建立／append）5 merge（狀態機 + git merge-file）6 baseline（baseline/ + metadata）7 launcher-gen（薄殼、gen/、check.sh）8 cli（子命令、詢問／-y、0/1/2）。主機側啟動器 = 薄殼，不算引擎模組。

## 9. 待拍板便條 [待]
(1) version.toml 檔名；(2) ensure→sync 範圍（預設全部）已定，畫成註記即可；(3) 引擎 image 也提供 docker save tar（#27 已定）；(4) 初始檔 `mode="append"` 的 init.toml 欄位名；(5) upgrade 對 append 行的「原文比對」在 CRLF／尾端空白時的判定（第一版：嚴格相同）。

---
# v2.1 補充（2026-09-19，依雙軌審查發現的規格矛盾所做的裁定；[裁] = 我裁定、待使用者否決；與上文衝突以本節為準）

## A. 不變量精確化 [裁]
- 「自動化只碰不進 git 的東西」→ **自動化不碰使用者的檔**。vendor_kit 自己擁有的 tracked 檔（`.vendor_kit/entry.just`、`vendor.just`、`ci/check.sh`、`.gitignore`）由 `version.toml` 第一行決定性推導，引擎升級時 sync 可重寫（本機）；**CI（frozen）下薄殼不符 → 1 不寫**。
- 「會碰使用者東西」仍只有兩處：根 justfile 一行、初始檔（含 append 模式經同意加的行）。「不碰使用者 .gitignore」精確為：**除非工具以 mode=append 宣告且你同意，否則不碰**。
- frozen（CI=1）= 不寫任何 tracked 檔、警告變失敗、不查最新版（不呼叫 registry 查 tag）；**仍拉鎖定版 image、仍寫 cache/、gen/**。CI=1 且存在 `version.local.toml` 任何覆寫 → sync 回 1 拒絕。

## B. 覆寫兩種，分開處理 [裁]
- 引擎覆寫 `vendor_kit = "<tag>"`：啟動器改用該 image 起容器（不 pull）；gen/.stamp 記該 tag。
- 工具覆寫 `<repo> = "path:<dir>"`：cache/<repo>/ 為 symlink → `<dir>/dist`；sync 跳過該工具的 materialize／verify，**仍檢查** metadata 完成標記與 baseline 落後。
- 工具在 dev 覆寫中時 `upgrade <repo>`／`remove <repo>` → 1 提示先 `undev`。
- `undev vendor_kit`：刪覆寫行 → 下次 just 用 version.toml 的引擎 → 薄殼／gen 與該引擎不符則重寫並統一提示。

## C. 動詞的兩段執行（啟動器編排）[裁]（取代 §6 的「固定三步」）
每個會動 image 的動詞（add／upgrade／sync）= **引擎 `resolve` → 主機 docker → 引擎 `apply`**：
1. `docker run … <引擎> resolve <動詞> …`：讀 version.toml／local、查 registry（frozen 不查）、算出「要拉哪些 image@digest、要問哪些檔」，**不寫任何檔**，以 stdout（一行一項）回給啟動器。dry-run 到此為止（印清單、退出 0；CI 無 -y 又需改 tracked 檔 → 1，version.toml 不動）。
2. 啟動器對每個要拉的 image：`docker pull`（已有則略）→ `docker create <img> /x` → `docker cp c:/dist/. <tmp>/<repo>/` → `docker rm`。
3. `docker run … -v <tmp>:/dist:ro <引擎> apply <動詞> …`：flock 專案目錄（**鎖在引擎 version 模組，啟動器不鎖**）→ 逐檔詢問（-y 免問；問句經 -it 的 tty）→ 寫 cache/、初始檔、baseline、gen；**version.toml 最後寫**；任一步失敗 → 暫存目錄丟棄、version.toml 不動 → 1。
啟動器仍不解析 TOML（引擎 resolve 的 stdout 就是它的輸入）。

## D. upgrade 順序與重入 [裁]
順序：(0) metadata 有「衝突中檔案」→ 檢查是否仍含 `<<<<<<<`：有 → 2 停；無 → 清除狀態 → (1) 先補待合併（version.toml 已到 B、baseline 仍 A）→ (2) 查最新（或 -t；**兩者都做，不是互斥**；-t 比現版舊 → warn 仍執行）→ resolve/apply 如 C。`--dry-run` 印「會問哪些檔」後 0。
自身升級兩個觸發點都畫：(a) `upgrade` 不帶 repo 當次：apply 改第一行 → 重寫薄殼+gen → 停下統一提示（退出 1）；(b) 別人 pull 後下次 just：sync 發現 gen/.stamp ≠ → 重寫 → 停下統一提示。

## E. 補進 §4／§7 的既定內容
- init.toml 兩個工具的 dest 指到同一路徑 → add 報錯拒絕 [裁]。
- `dist/files/` 是否允許 symlink → [待]（第一版 lint 擋）。
- 工具 repo 的 CI 跑 vendor_kit 出貨的 `check.sh --dist`（dist 佈局、init.toml 合法、image 可展開、兩平台內容一致）[定，沿用 v1 §3]。
- `--porcelain` 旗標：**拿掉**（未定案，v2 候選）。
- `update --exit-code` 有新版回 2（結束狀態 2 不只衝突）。
- gen/tools.just：**每個 `<ns>.just` 一行 mod**（一工具可多行）；remove 刪該工具的所有 mod 行。
- install 冪等：根 justfile 已含那一行 → 不再加；`--no-justfile` → 跳過 justfile 步驟只印指示；「修復」= 用引擎重寫薄殼（不是只補缺）。
- add／remove／uninstall 都有 `-n/--dry-run`（resolve 到此為止）；uninstall 逐工具 remove 任一回 1 → 中止。
- baseline 不是由 version.toml 推導，是「上次合併的歷史狀態」。
- Renovate 補合併在 **PR 分支**上完成、CI 綠後才 merge。
- 架構頁只畫模組／最小單元／模組間傳的資料；流程一律在流程頁。模組間資料：cli→version（讀寫 version.toml）；registry→(tag, index digest)；materialize→(cache 路徑, 印記)；init／merge→(檔案清單, 逐檔決定)；baseline→metadata；launcher-gen→just 檔清單。
- 「sync 不上網」改為「sync 不查最新版；只拉鎖定版」。

## F. 版面
- 流程頁拆：p5 → 「bootstrap.sh + install」「add」；p7 → 「upgrade：Renovate 路徑、手動路徑」「upgrade：逐檔判斷表、回退、自身升級」；p8 → 「dev/undev」「remove/uninstall」。共 11 頁。
- 顏色：「v2 改」統一 #00b050 且只加標籤不改框色（改用小綠角標或格外綠色小字「v2」）以免蓋掉「進 git 綠框／不進 git 灰虛線」；GHCR image 用主圖既有的 image 顏色（PURPLE_LEAF 在主圖 legend = image），流程頁「容器內子命令」另用一色並寫進 legend；待拍板便條、規則框、不變量框三者顏色分開並全部進 legend；灰底表頭、淺灰分組底進 legend。
- 排版：所有檔案框右緣距分組框 ≥ 20px；線上文字不得長於兩端間距（改放線側或縮短）；線不穿標題列。
- 每頁名詞表補：GHCR、image、just、recipe、mod／import、PR／commit／push／rebase、CI、sha256、flock、RepoDigests、index digest、daemon、tar、release、dry-run、regex manager 等該頁用到的詞。

---
# v2.2 修訂（2026-09-19，依 codex 對 v2.1 的批判；agy/codex_v21.md；與 v2.1 衝突以本節為準）
- **A 薄殼重寫（有條件）**：sync／install 重寫 `.vendor_kit/` 自有 tracked 薄殼前，先比對現內容 == 上次產物（hash 記在 gen/.stamp）；相同 → 重寫；被改過 → 1 並列差異、不動。frozen = 只准寫 cache/、gen/；升為失敗的警告明列：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫。Q10 待使用者選 (1) 自動重寫（有比對）或 (2) 只報 1 提示 `upgrade vendor_kit`。
- **B 覆寫**：引擎覆寫記 tag **+ 解析後 image ID**（同 tag 重 build 才會被發現），`docker run --pull never`；工具 path 覆寫由啟動器明確 `-v <dir>/dist:/dist/<repo>:ro` 並驗 dist/init.toml 存在；undev materialize 失敗 → 1 保留可恢復狀態；不帶 repo 的 upgrade 先完整預檢（含 dev 中工具）再動任何東西。
- **C 編排**：dry-run 也要拉 image 展開到暫存，再由引擎 `apply --dry-run` 做唯讀預覽（resolve 只知道 tag/digest，不知道要問哪些檔）。stdout 協定版本化（第一行 `vk-resolve/1`）、只含固定欄位與安全字元、診斷一律 stderr、啟動器不 eval。只有互動才 `-it`；CI／-y 不加 -t。私有 registry 查最新 tag：引擎需 `VENDOR_KIT_REGISTRY_TOKEN`（文件明寫）或改用 `-t` 指定版本（主機 docker pull 走主機認證）。
- **C 鎖與復原（取代 v2.1 C 的「丟暫存即可」）**：resolve 輸出輸入指紋（version.toml、metadata、要動的使用者檔 hash + 鎖定 digest）；apply 拿 flock 後**重驗指紋**，不同 → 1「請重跑」；所有合併在暫存完成 → 逐檔原子替換 + metadata 進度日誌（state=in-progress，列已完成／未完成）；失敗明列，下次任何動詞先恢復；「不留半成品」只對第一次 install 成立。衝突（2）與自身升級後要求重跑（1）是獨立狀態，文件分開描述。
- **D 順序**：(0) 衝突中檔案：用我們自己產的標籤（`<<<<<<< vendor_kit:baseline` 等）偵測，檔案失蹤不視為已解；仍有 → 2。(1) **有待合併 → 只補到 version.toml 那版然後停**，印「另有新版 vX，再跑一次 upgrade 可升」；補合併衝突 → 立刻 2。(2) 沒有待合併才查最新（frozen 不查）。Renovate PR 補合併因此自然固定在 PR 鎖定版。git merge-file 回傳值（衝突數）映射為 2。
- **E 路徑**：dest 撞名：copy/copy、copy/append 同 dest → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查。dest 正規化、不得越出 repo、不得指向 `.vendor_kit/`；消費端（引擎）驗證，不只供應端 lint。dist symlink 第一版禁止，引擎展開時也驗。
- **E 其餘**：uninstall **不 rm -rf `.vendor_kit/`**：先預檢全部工具，逐工具 remove 任一失敗即中止並列出已完成部分；只刪確認是我們產的（hash 相符）檔，未知或被改的保留並回報；最後目錄非空則保留。`-n/--dry-run` 覆蓋所有刪改與詢問。`sync` 無變更時只跑一次檢查的快路徑（不起第二個容器）。


## decisions/grilling.md

# 討論紀錄（grilling，2026-09-18）
- Q1 定案：自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file；第一版不放 vendir/Copier。
- 第 1 頁討論：
  - base 的 update/upgrade 確認對齊 apt（ADR-00000011 §2）；我們跟 base。
  - 專案層動詞 `install`（第一次建立、再跑 = 修復、要求已是 git repo、不做 git init）↔ `uninstall`；bootstrap.sh = 下載引擎 + 呼叫 install；`--repair` 取消。引擎內部「拉 image 展開」改名 fetch。—— 使用者 OK。
  - `ensure` → `sync`：使用者 OK，待 codex 批判確認。
  - codex 批判（agy/codex_verbs.md）：同意 install/uninstall、同意 sync；附帶條件：`install <repo>` 誤用要導向 `add`；help 明寫「已接入的專案跑 sync，不是 install」；sync help =「依 .version 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」；fresh clone 的 sync 入口在 gen/ 不存在時也要能跑（recipe 放 tracked vendor.just 已解）；frozen 模式要明寫多禁止什麼；uninstall 要交代初始檔處理（保留並印清單）。內部展開步驟名：codex 建議 materialize（非 fetch）——內部名，不對外。
- 第 1 頁便條 (3)(4)(6)(11) 回覆：
  - add = 正式使用（GHCR、進 git、共享）；dev = 開發用（本機目錄、.version.local、只在本機）；**dev 要求工具已在 .version**。使用者 OK，要記 issue/ADR。
  - update/upgrade 語意 OK；upgrade 含 install+合併+推 baseline OK。
  - remove 不開 --purge OK；bootstrap 第二次拒絕 → 作廢（bootstrap = 下載 + install，再跑 = 修復）。
  - 「vendor_kit 會碰使用者的東西」只有三處：根 justfile 一行、初始檔（add 建立不覆蓋；upgrade 合併；**永不刪**——新版刪除的檔改為只 warn 不刪）、.git/info/exclude 我們的區塊（不碰 .gitignore）。使用者要求再研究：根 justfile 能否不碰（base 式 symlink？）、.version 改名或收進 .vendor_kit/、初始檔隔離方式 → agy + Claude/codex 雙軌（進行中）。
  - (11) dev 自身：**要支援**（使用者定案）。機制 = .version.local `vendor_kit = "<本機 image tag>"`，`dev vendor_kit -i/--image <tag>`；驗收測試 = 用剛 build 的引擎 image 在乾淨下游 fixture repo 跑完整流程，放 test 分層最後一關。
- 隔離題定案（2026-09-18）：
  - **不變量**：vendor_kit 對使用者的檔——可以建（要明確說明建立或修改了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋。
  - A 根 justfile：無 → 建（import 一行 + default: @just --list）；有 → 詢問加一行，`-y` 直接加並印出；uninstall 對稱詢問，只刪與我們寫的完全相同的行。不接管根檔（base 會對齊我們，共存問題消失）。
  - B 全收進 `.vendor_kit/`：version.toml、version.local.toml、cache/<repo>/、.gitignore（自有）；不碰 .git/info/exclude 與使用者 .gitignore；工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根。
  - C 初始檔：add 建（已存在不納管、不覆蓋）；upgrade 逐檔判斷後**詢問**（沒改→換新版？；都改→三方合併？），`-y` 免問，衝突留標記回 2，baseline 推到新版；remove/uninstall 不刪只印清單；CI 無 -y 需改檔 → 1 印清單。
  - PRD/ADR 一律中文；PRD 結構學 base（不變量／原則／衝突優先序；機制放 ADR）。
- Q3 定案：vendor_kit 只輸出一個命名空間 `vendor_kit`；工具 `dist/just/<ns>.just` 每檔一個頂層命名空間，數量工具自己決定；add 時跨工具撞名報錯拒絕。（proto ADR-0002 §4 與此一致）
- Q4 進行中：工具 image 單架構 amd64 + arm64 CI 驗收守門 vs 多架構 index。實測：amd64 主機（無 qemu）docker create --platform linux/arm64 + docker cp 展開 arm64-only 純資料 image 成功（scratchpad/archtest）。
- PRD 草稿已寫（src/doc/PRD.md 234 行、doc/adr/README.md、TEMPLATE.md）；子代理列出 10 處來源矛盾，除 Q4／just 最低版本／多命名空間（已定）外，一律以 grilling.md 為準；CONTEXT.md 待同步。
- Q4 定案：工具 image **多架構 amd64+arm64**（同一次 buildx、COPY-only、CI 驗兩平台內容一致）；引擎 image 同；平台 Linux amd64 + arm64（Jetson、RPi 64 位元）、WSL2；armv7 不支援；docker 最低 19.03；印記記 index digest（與 version.toml 一致）。多架構測試開 issue 追蹤，做完才關。
- Q5 定案（Renovate）：vendor_kit 本身無 bot、不 commit、不開 PR；Renovate 是下游自選；PR 只改 version.toml 一行，初始檔合併由維護者本機 `upgrade <repo> -y` → commit → push（Renovate 預設不動有人推過的分支，PR body 警告勿勾 rebase）。**PR 的 CI 必須以新版跑完整流程（sync frozen → verify → upgrade --dry-run → 工具測試 → 專案測試），一行改動本身不可能出錯，不構成通過依據；需合併 → 1 印指令；人補完 push 後全部再跑一次。** bot commit／postUpgradeTasks 不採（附註）。
- Q7 定案（雙軌一致）：引擎 image 公開、工具自決、認證是主機的事；公開不可逆要提醒。
- Q8：維持 just ≥ 1.33（來源：[group] 放 mod 上需 1.33 #2263）；CI 用 1.33.0 跑完整 fixture 才定案。
- Q9 定案：自身升級後停下、退出 1、要求重跑；契約「同一次 just 呼叫內不會看到新 recipe」。
- Q6 雙軌一致：只 warn + 明列條目；工具契約禁止初始檔以根 .gitignore/.dockerignore/.editorconfig 為目標（lint）；required/optional 待使用者。
- Q6 定案（使用者：對齊不變量）：init.toml `mode = "append"` 的初始檔——無檔則建；已有則**問**後 append（-y 免問，印出加了什麼）；upgrade 用原文完全比對找上次加的行（記在 baseline），找到→問後替換，找不到→不動只印新內容；remove/uninstall 問後只刪原文相同的行。不用標記區塊；required/optional 不需要。
- Q7 定案：(c) 引擎 image 公開；工具 image 由各工具 repo 自決；認證是主機／CI／Renovate 各自的事，vendor_kit 契約只承諾「主機 docker 拉得到就能用」；文件提醒公開不可逆、denied 分不出不存在／無權限。
- Q8 定案：just ≥ 1.33.0（來源：[group] 放 mod 上 #2263；ADR-0002 理由要改）；一律 GitHub release 下載版；bootstrap.sh 低於即印下載＋安裝指令；CI 矩陣 1.33.0 + latest（不跑中間版）；禁用比 1.33 新的功能由 lint 擋；定案前用 1.33.0 跑完整 fixture。
- Q9 定案：引擎升級後 sync 一次重寫完薄殼＋gen、退出 1、統一印「vendor_kit 已更新 vX → vY，請再跑一次剛才的指令」；不自動續跑（just 一開始即載入定義，續跑會用舊定義）。契約：「同一次 just 呼叫內不會看到新 recipe」。
- Q8 補充：lint 現在擋比 1.33 新的功能；just 有重大功能時允許提高下限（agy 查 1.33 後變更中）。
- Q8 補充（just 1.33→1.58 調查，scratchpad/agy/ 子代理以 gh api + 實測完成，agy 逾時無輸出）：無值得提高下限的功能；候選 1.51 `[working-directory: justfile_directory()]`、1.55 `set minimum-version`。ADR 記破壞性變更：1.53 which() 需 set lists；1.40 --list-submodules 必配 --list；1.42.0–1.42.2 submodule cwd 回歸（提高下限時跳過）；1.52 缺席 mod? 相依 recipe 改 disabled；settings 永遠 per-module（entry.just/tools.just 零 set 規則永久）。
- bootstrap.sh 交付定案：README 連 `releases/latest/download/bootstrap.sh`（GitHub 內建，不需 latest tag，實測 302）；每版 `releases/download/vN/bootstrap.sh`；腳本內嵌所屬引擎 ref；檔名固定。
- 待確認：bootstrap.sh `--image <本機 image>` / `--image-tar <tar>`（version.toml 寫正式 ref、version.local.toml 寫本機覆寫；release 附各平台 docker save tar）。
- 2026-09-19 codex 審三小題（agy/codex_small3.md）：
  - 私有 image 查最新：預設「未提供 registry 憑證時不支援需認證的版本列舉」，update 對該工具回 1 印「可設 VENDOR_KIT_REGISTRY_TOKEN（PAT classic read:packages）或用 upgrade <repo> -t <tag>」；多工具照查其他再彙總；不掛 ~/.docker/config.json。
  - init.toml 欄位：`strategy = "copy" | "append"`（預設 copy；mode 在 Ansible 是權限）；規格明寫 append 首次加入並記錄、重跑不重複、upgrade 只對可辨識的上次插入內容提修改；copy 已存在就跳過，-y 也不覆蓋。
  - append 行比對：CRLF/LF 等價、其餘精確；記錄實際插入片段（原先就存在的相同行不認領）；零命中或多處 → 保留並 warn。
- Q10 待使用者：傾向 (2) 只報 1 提示 `upgrade vendor_kit`（升級者多一個指令；pull 的人 hash 相符無事）。
- **Q10 定案 (2)**：sync 發現薄殼與引擎不符只回 1 提示 `just vendor_kit upgrade vendor_kit`；重產薄殼只由明確動作（upgrade vendor_kit／install）做，做之前比對現內容 == 上次產物（hash 在 gen/.stamp），被改過 → 1 列差異不動。sync 只寫 cache/、gen/（不變量回到「自動化只碰不進 git 的東西」，不需精確化為「不碰使用者的檔」）。
- **Q11 定案 (b)**：未提供 registry 憑證時不支援需認證的版本列舉；update 對該工具回 1 印「可設 VENDOR_KIT_REGISTRY_TOKEN（+ _USER；或 _TOKEN_FILE）或用 upgrade <repo> -t <tag>」；只在 update/upgrade 的 resolve 階段以 -e 傳入引擎；不寫 log/檔、不傳給工具。「查最新」= registry tags/list 取 SemVer 最大正式版。引擎實作 Docker Registry 標準協定（WWW-Authenticate 換 token → /v2/<name>/tags/list 分頁）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」。PAT 種類／權限細節實作時手動測再定。README 要有「私有 image」一節；測試：unit（token 交換、分頁、SemVer）、integration（無 token→1 逐字訊息、錯 token→1、對 token→列出、TOKEN_FILE）、洩漏 grep、驗收 fixture 私有工具案例。
- **Q12 定案**：init.toml 欄位 `strategy = "copy" | "append"`（預設 copy）；規格明寫 append 首次確認後加入並記錄、重跑不重複、upgrade 只對可辨識的上次插入內容提修改；copy 已存在跳過、-y 不覆蓋。
- **Q13 定案 (2)**：append 行比對 CRLF/LF 等價、其餘精確；metadata 記實際插入的行（原本就存在的相同行不認領）；零命中或多處 → 保留只 warn，-y 不硬加。行尾政策（repo 預設 LF、.gitattributes、dist lint）開 issue #29；使用者確認預設 LF。


---

# 附件二：base 語料（base_corpus.md）



# ===== base doc/PRD.md（全文） =====

# base -- Product Requirements (PRD)

> base's north star: the fixed reference every decision is checked against.
> It holds three layers and nothing else: **invariants**, properties that
> must always be true of base and that no ADR may violate; **design
> principles**, the judgement criteria base decides by when two options are
> both available; and the **conflict priority**, which of two legitimate
> properties gives way when a decision cannot have both. It changes only
> when base's **product goals** or the criteria behind them change, not when
> a mechanism changes. Individual decisions live in [`doc/adr/`](adr/); domain
> facts live in [`CONTEXT.md`](../CONTEXT.md); the working contract lives in
> [`CLAUDE.md`](../CLAUDE.md).

## Purpose

base exists to solve one problem: **every repo re-implementing the container
lifecycle, and then drifting from every other.**

What base produces is a **building block**. A block has two properties that must
hold together:

1. **Usable alone.** A downstream repo builds, runs, tests and field-delivers
   without needing to know that any composing layer exists.
2. **Composable.** Any number of blocks can be assembled -- **including several
   instances of the same block**. Who assembles them, and how, is not base's
   concern.

The two are one code path, not two: **using a block alone is N=1, not a special
case** (design principle P5). A block that only works alone is not a block, and
a block that needs an assembler to work at all is not usable.

Concretely, base replaces the hand-written `docker compose` configuration of a
repo that runs a single container -- and adds what hand-writing cannot give:
the lifecycle base owns (invariant 1), field delivery, and composability.

## Scope

### In scope

- The lifecycle of a **single containerised service**: build (Dockerfile
  stages), run (compose generation + wrappers), test (self-test + shipped
  smoke), and field delivery (a self-contained deploy bundle).
- **The generation API itself.** Both generate stages take the caller's
  parameters and write into a directory the caller names, so one repo can be
  instantiated more than once without being modified (ADR-00000036). base owns
  the API; it does not own the orchestration that calls it.

**Completeness, and how it is judged.** Within that scope base must be able to
express every compose field a single-container repo in this org **actually
uses**. The target is deliberately not the whole Compose Specification: most of
that surface is for applications base does not serve, and a repo cannot be
better off for a field nobody needs.

**The population is derived, never listed.** A field is in it when there is
evidence of use: a hand-written compose file in the org, a `setup.conf` key a
repo sets, a request in an issue, or a workaround achieving the capability by
other means -- a raw `docker run` flag, an entrypoint doing the job. That last
class matters most: it is the record of a need base failed to serve, and it is
the one a maintained list would never contain.

The figure is computed from that evidence when it is read, not written down here
(invariant 10). What is recorded is the rule, and one consequence of it: an
absent field cannot generate demand, so a first-principles argument for adding
one is admissible -- but it is an argument, and it does not become evidence by
being reasonable.
- Host detection -> config resolution -> render, where one source
  (`setup.conf` + detection) fans out to every artifact (`compose.yaml`,
  `.env.generated`, the generated `.env`, `deploy.sh`, the baked runtime
  `ENV`).
- The **shared CI mechanism** downstream repos call (reusable build/release
  workers + the `test-tools` image).
- The **propagation mechanism** (subtree + `init.sh` resync) that keeps
  downstream repos in sync with base.
- The **quality gates** that hold base itself to a trustworthy bar (the
  ISTQB-aligned self-test, the lint suite, the coverage gate).

### Deliberately out of scope

- Multiple services inside one container (see invariant 1).
- **Multi-container architectures.** More than one container is more than one
  block: it is split into separate repos and composed by the layer above. That
  splitting rule is what keeps invariant 1 a structural boundary rather than a
  style preference.
- Field orchestrators / manifests (k8s, balena, ...); the deploy bundle targets
  a single-host `docker run` first.
- Non-NVIDIA GPU support (tracked separately).
- Downstream-specific business logic -- that stays in the downstream repo; base
  owns only the shared scaffolding.

## Core Invariants

Each invariant is a property that must hold across the whole of base and that
**no future ADR may violate**. The ADRs listed under each one are the decisions
that established or serve it -- they remain the record of *how* and *why*; this
document states *that it must always hold*.

### 1. One container = one service; base owns the single-service lifecycle

base produces containers that run exactly one service, and base -- not each
downstream -- owns that service's whole lifecycle: process init (PID 1
reaping / signal forwarding), restart policy, health supervision (watchdog),
and log persistence. A downstream gets a correct lifecycle for free; it never
re-implements one.

**A lifecycle capability that presupposes a long-running service applies only
to deployable stages.** A `devel` or `*-test` container is a *session*, not a
service: its life is the interactive shell or the test run, and it is meant to
exit. So the **restart policy is emitted only for deployable stages and the
field bundle -- never for `devel`, never for `*-test`** (which stages are
deployable is invariant 8's rule, not a second definition). Because every
context the policy still reaches is one where a container failing to come back
*is* the footgun, its default is ON.

*Why it is fixed:* auto-restart on a session container makes it impossible to
leave -- `exit` relaunches it forever. Auto-restart on a field service is the
whole point: it must survive a crash and a host reboot unattended. The same
setting is therefore correct in one place and broken in the other, so the scope
is not a tuning choice that a future decision may widen back.

*Serves / established by:* ADR-00000020 (incl. its 2026-08-03 stage-scoping
amendment); realised by restart (#478), init (#792), watchdog (#797), per-start
logs (#805, ADR-00000021).

### 2. Never fail silently

Any error or missing/incompatible configuration fails **loudly and early** --
never a silent skip that still shows green. Contracts self-validate before doing
real work; a violated invariant is caught by base's own CI, not discovered
downstream.

*Why it is fixed:* base is a shared foundation; a silent failure in it
propagates to every downstream undetected. Trustworthiness is the product.

*Serves / established by:* worker preflight self-validation (#800), the
compose overlay guard (#716, ADR-00000022), the ADR-numbering guard (#808), the
doc-count drift gate, the issue-ref / no-emoji lints.

### 3. Composable by construction

**The property (invariant):** a base-generated stack can be instantiated more
than once without a retroactive change to base. Anything base decides at build
time or before the container starts is reachable by the caller; only what is
internal to a running container is outside the contract.

**The mechanisms (swappable, not invariant):** a `.env` overlay carries fields
whose value varies (ADR-00000022); a parameterised generate call carries fields
whose *shape* varies, since an interpolation substitutes into lines that already
exist and cannot add or remove them (ADR-00000036).

*Why the property is fixed:* it is a forward guarantee. A decision that put a
per-instance value out of the caller's reach would re-introduce the wall
silently.

*Why the mechanism is not:* this invariant previously named `${VAR:-<default>}`
interpolation as the mechanism, and in 2026-09 a case arrived that no
interpolation can express. The mechanism had to change; the promise did not.
Invariant 7 already draws this line and this one now follows it.

*Serves / established by:* ADR-00000022 and ADR-00000036, and the guard that
enforces them.

### 4. Fail-safe defaults

When a default carries a "safe vs convenient" tension, base's default falls
toward **safe**, and the riskier/tighter option is opt-in. A convenient default
that could silently break a real deployment is not shipped as the default.

*Why it is fixed:* base's defaults reach every downstream unattended; the cost
of a silently-unsafe default is borne org-wide.

*Serves / established by:* ADR-00000019 (network stays `host`, because a
`bridge` default silently breaks cross-machine ROS); this is the general
principle, of which the network decision is one instance.

### 5. The two-branch default rule, applied to lifecycle knobs

**Invariant 11 is the rule; this is where it was first written down and
what it lands on for a lifecycle knob.** The two questions there --
can enabling it break a working setup, and does forgetting it hurt --
are for a lifecycle knob the two branches this invariant is named for:
"transparent to a correct single-service workload" and "its absence is a
footgun". Both must hold to default ON.

What this invariant adds to invariant 11 is the **landing**: a lifecycle
knob that does not default ON does not default to some third base-chosen
setting, it defaults **OFF -- the no-op**, which is the behaviour an
unconfigured container already had before the knob existed. base owning
the lifecycle (invariant 1) is not a licence to move what an unconfigured
container does; the knob exists so a downstream can ask for more than it
was already getting, never so base can substitute a new behaviour behind
a setting nobody has touched.

Where base had not intervened before, that no-op *is* Docker's own
behaviour, and most of the OFF landings are Docker-native for that
reason: the watchdog's OFF is no supervision at all, and its failure
action's OFF is `restart-container`, which is Docker's restart policy
doing the recovering. The two part in exactly one recorded place, and the
no-op is what wins there. `[network] mode` stays on `host` by decision,
where an unconfigured `docker run` gives `bridge`: `host` is what base
had always run, and ADR-00000019 declined the proposed flip because a
`172.17.x` address is not routable off-box, so cross-machine ROS goes
silently unreachable. That is invariant 4 choosing the safe side of a
safe-versus-clean tension, and it is a divergence this invariant permits
only because it was already the pre-existing behaviour and is recorded in
an ADR -- not a third landing a new knob may reach for.

*Why it is fixed:* invariant 1 makes base the owner of every downstream's
lifecycle, which means a base-chosen default is not one of several
settings a reader might find -- it is the only behaviour that repo has
ever seen. A knob whose OFF is the no-op cannot change any of those repos
on the upgrade that delivers it; a knob whose OFF is a fresh base
preference changes all of them at once, unattended, from a maintainer who
is not in the room.

*Serves / established by:* ADR-00000020 (init defaults ON as the
transparent-and-footgun case; the watchdog's restart-service action as
the workload-semantics-changing case that lands off, and the restart
policy as the case whose answer is scoped per stage); ADR-00000019 for
the network default, which is the one OFF that is not Docker-native;
generalised by invariant 11.

### 6. One source, propagated; downstream is a thin caller

**The property (invariant):** there is one source of truth for the shared
build / test / lifecycle logic, propagated downward -- not N copies maintained
in parallel. The downstream's entrypoints (`main.yaml`, top-level justfile) are
thin forwarders.

**The mechanism (swappable, not invariant):** a `.base/` subtree vendored into
each downstream repo, resynced by `init.sh` (ADR-00000010, ADR-00000011).

*Why the property is fixed:* pushing real logic down into each downstream -- a
fat caller -- would fragment the single source of truth base exists to be.

*Why the mechanism is separated:* it was measured in 2026-09 rather than
assumed. Across 18 vendoring repos, 2217 vendored files were compared by blob
against the tag each repo claims: **one local edit, zero partial upgrades**. The
vendored copy is working, and the alternatives were weighed against that
evidence -- so subtree is a checked choice, not a default. Recording it as a
mechanism keeps the choice reviewable; recording it as an invariant would have
made re-examining it a violation.

*Serves / established by:* ADR-00000010, ADR-00000011; the pull-based version
monitor + `init.sh` resync propagation.

### 7. (Quality) base holds a rigorous, industry-aligned test bar

base is tested to a rigorous, explicitly-levelled standard, and base's own CI
is the gate that proves it. *The commitment* is the invariant; the specific
taxonomy and coverage mechanism are swappable decisions.

*Why it is fixed:* downstreams trust base because base is verifiably correct; a
weaker bar would erode the reason to inherit from base at all.

*Serves / established by (commitment):* ADR-00000018 (the ISTQB-aligned
taxonomy). *Swappable mechanisms (not invariant):* the coverage tooling
(ADR-00000008 / ADR-00000016) and the CI throughput / shard strategy
(ADR-00000017).

### 8. Development and field are cleanly separated, and provisioned by opposite means

base keeps the **development** environment and the **deployable/field**
environment cleanly apart, and provides the same config by opposite means:

- **In development** -- config is bind-mounted into the container; edit it
  directly, re-run to apply.
- **In a deployable stage** -- config is baked into the image (a working
  default), plus an optional "mount a file to override it" hook, so a
  deployment adjusts config **without a rebuild**.

The developer-vs-user split follows **git-tracking**: committed = the
developer's default (baked); gitignored / not in the repo = the
user/operator-editable overlay. The names follow one rule everywhere -- the
standard name is the tool's and is regenerated (`Dockerfile`,
`compose.yaml`, `.setup.conf`, `.env`), a suffix marks the local variant
that is the operator's and is never rewritten (`.setup.conf.local`,
`.env.local`). Only a **deployable stage** deploys; every
downstream repo follows this. `_is_deployable_stage` (`lib/stage.sh`) is the
one predicate that enforces it, and it rejects more than the two obvious
cases: **`devel`** (the interactive shell), **any `*-test` stage** (it exists
to run, assert and exit), **`sys` and `devel-base`** (build intermediates with
no runnable service at all), and the legacy aliases `base` / `test`. The
invariant is whatever that predicate says -- stated here in full so the two
cannot disagree.

*Why fixed:* base's value is that a downstream inherits one correct dev->field
path. A devel/test image is not a field artifact (binds source, carries the
toolchain, expects a live-edit surface); deploying it, or letting field config
need a rebuild, breaks the dev/field split every downstream relies on.

**A field artifact must not silently depend on a config layer that is not
under version control.** The gitignored per-worktree override
(`.setup.conf.local`) is a development convenience by construction: it is
visible on exactly one machine. A bundle built from it cannot be reproduced
from a clean checkout, and nothing about the bundle would say why. So
`setup deploy` REFUSES while that layer exists, and the explicit escape
hatch records in the bundle itself which sections came from it -- because
the person holding the bundle in the field is not the person who chose to
bypass the gate.

**Which config a deployable stage bakes is itself committed, and visible.**
The two means above provision *a* config; they say nothing about which one,
and a repo that ships several curated presets bakes one of them. That choice
is a **repo-root symlink into `config/<component>/`**, read through a build
`ARG` whose default is the symlink's own name -- so one build overrides it
with `--build-arg` and no tracked file moves, while the repo's default
changes by re-pointing one link. The committed target is the **inert**
preset, so a fresh clone builds stock behaviour and a chosen profile is
always something someone recorded (invariant 4). Every `setup` run names each
selector and the preset it resolves to, and refuses to be silent about one
that resolves to nothing (invariant 2). The layout rules that go with it --
group by kind only once a kind has a second file, `<name>.example.<ext>` for
a copy-me template, no audience directory because `deploy.manifest` already
records tunability, and a diff-only upstream baseline is a test fixture
rather than config -- are ADR-00000030's.

*Serves / established by:* ADR-00000003 (env/workload boundary + field
delivery; this generalizes its env-row override to config files); ADR-00000023
(config field-override + field-deploy mechanism); ADR-00000030 (which preset
a build bakes, and the `config/<component>/` layout); ADR-00000011 /
ADR-00000018 (devel/runtime/*-test stage structure); ADR-00000025 (the
untracked-layer refusal).

### 9. Identity and naming are resolved once, from a file

Two properties, one subject -- what a run calls the things it creates:

- **Image identity is a function of build inputs.** Identical inputs
  resolve to one tag; different inputs can never share one. Two builds that
  agree on every input SHOULD share an image (that is a cache hit, and it is
  correct); two that differ must not be able to displace each other's.
- **Divergence in runtime naming between two checkouts comes from an
  explicit, file-recorded override** -- never from an ambient variable, and
  never from an accident of directory naming. If two checkouts run under
  different project names, a file in each says so.

*Why it is fixed:* both failure modes are silent, and both cost work that
already looked finished. A shared tag lets one run displace the image
another is mid-way through using, with no error at all -- a coverage pass
once reported green having lost its instrumentation that way. A project
name derived from a directory basename means two checkouts silently share
containers and networks, and stay isolated only by the accident of being
named apart; the same name derived from an ambient variable is invisible to
anyone reading the repo and does not survive a new terminal. Naming is
infrastructure, so it has to be as reviewable as the rest of the config.

*Serves / established by:* ADR-00000025 (`[project] name` resolved once into
`.env.generated`, read by both the wrapper's `-p` and the emitted
`name:`; the gitignored per-worktree layer that records the divergence);
the content-keyed tooling tag + checkout-keyed test project (#891 / #892).

### 10. Documentation is derived from the code, never duplicated beside it

A figure or a listing that can be computed from the tree is computed when
it is read, not stored in a tracked file that somebody must then keep in
agreement with the tree. What a documentation file holds is what no
generator can produce: intent, rationale, and the reason a thing is shaped
the way it is.

The corollary that decides where derived values live: **a derived figure
that describes the tree is stale from the moment the next commit lands.**
Storing it at a slower cadence than it changes does not fix that -- it
makes the staleness harder to notice, and a number that is only sometimes
right is harder to use than no number, because it must be distrusted every
time. So such a value is not stored at a slower cadence; it is not stored.

What that turns on is the referent, not the storage. A figure that names
what it measured -- a coverage rate labelled with the version it was
measured on -- makes no claim about the moving tree, so it cannot go stale
and it may be committed. The test totals had no referent: `3239 tests`
asserted something about the tree, which is why every branch had to edit
it.

Where a derived value is genuinely wanted by a reader, it is attached to
the thing it describes at the moment it was measured -- a release carries
its own test report -- rather than being maintained in a document that
outlives its own accuracy.

*Why it is fixed:* this is invariant 7's argument applied to the other
half of what base ships. Invariant 7 fixes base's TEST bar on the grounds
that "downstreams trust base because base is verifiably correct"; a
downstream never runs base's suite, it inherits the consequence. The same
holds for the documentation: base is vendored into every downstream, and
what a downstream reads to decide how to use the foundation is base's own
documentation. A document that looks authoritative and is wrong is
invariant 2's silent failure, propagated -- and it is worse than a wrong
figure in a report, because the reader has no way to tell which sentences
are derived and stale from which are authored and current. So how base
stores its documentation is a property of the product on exactly the
footing invariant 7 stands on, not a housekeeping preference.

The duplicate also costs on three measured axes at once (figures measured
2026-09-02). It **rots**: 46% of the per-test
catalogue's hand-written descriptions are placeholders (761 of 1,658 rows
in `doc/test/unit.md`), and where filled they mostly restate the test name
they sit beside. It **collides**: five lines carrying a test total are
edited by every branch, so 61 of the 65 merges of `origin/main` into a
branch since 2026-08-25 conflicted in `doc/test/`, and 35 commits over
that window touched nothing else. And it **misleads**: a committed figure
looks authoritative exactly when it is wrong, which is between every
commit and the sync that follows it.

*Serves / established by:* ADR-00000028 (test statistics live only in the
release, sourced from the run's JUnit XML rather than from a scan of the
source); ADR-00000027 (the release cadence this rides); the
`derived-figures` lint, which enforces the same rule for the named
constants it covers. Invariant 2's guard list KEEPS its doc-count drift
gate entry (amended #978, 2026-09-04: this sentence used to say the entry
drops when ADR-00000028's mechanism lands). That mechanism has landed and
the gate did not go with it. The earlier reasoning assumed the gate
existed to guard the removed figures; since #999 it validates the
GENERATED per-test catalogue -- what keeps a description from silently
vanishing on a rename -- so nothing was removed from under it. See
ADR-00000028's #978 amendment. #952 (the release coverage badge, merged
as PR #974) is the case that fixes where the line falls: it names the
version it measured, so it is stored.

### 11. A default is decided by two questions, not by preference

Every default base ships is settled by asking, in order:

1. **If it is on, can it make something that currently works
   incorrect?** Yes -> it defaults **off**.
2. **If someone forgets to turn it on, does something go wrong?** Yes ->
   it defaults **on**.

Only when **both** hold -- it cannot break a working setup, *and* its
absence is a defect waiting to happen -- does a setting default on.
Every other combination defaults off, including the common one where
neither question has a "yes": a setting nobody is hurt by forgetting is
not worth the blast radius of shipping it enabled to every downstream.

The qualifiers below decide what the two questions are asked *about*,
and they are what make the rule mechanical rather than rhetorical:

- **The unit is a (setting, scope) pair, not a setting.** The same
  setting can be correct on in one scope and correct off in another, and
  asking the questions per scope is what produces that rather than
  forcing one answer everywhere. Restart policy is the worked case: on a
  `devel` or `*-test` container, restart-on makes `exit` incorrect
  (question 1: yes -> off); on a deployable stage it cannot make a
  correct long-running service incorrect and forgetting it means the
  service does not survive a crash or a host reboot (question 1: no,
  question 2: yes -> on). Invariant 1 states that scoping as a fixed
  property; this rule is where it comes from.
- **Question 1 asks about something that *works*, not something that
  *passes*.** A guard that turns a vacuous green into a red has not made
  anything incorrect -- it has stopped something incorrect from
  reporting otherwise, which is invariant 2's whole subject. A check
  whose absence lets a defect ship green answers "no" to question 1 and
  "yes" to question 2, and so defaults on.
- **A "yes" to question 1 has two answers, not one.** Defaulting off is
  the cheap one; removing the way the setting can break a working setup
  is the other, and it is available whenever the breakage is a property
  of the implementation rather than of the feature. The wrapper
  transcript is the recorded case: tee-ing a transcript could re-flip
  single-sink dispatch and change a terminal's output format, which is a
  question-1 yes. Base did not default it off -- it cached TTY-ness at
  startup so the tee cannot re-flip anything, turning the yes into a no
  (ADR-00000007), and `wrapper_transcript` defaults on.
- **The rule adjudicates a toggle, not a magnitude.** A retention count
  such as `container_log_keep` has no "off", so neither question applies
  to it; how large a default number should be is invariant 4's direction
  question, answered by which way the harm falls.

  **Amendment (#994, 2026-09-03): a magnitude that is a THRESHOLD is
  decided by two questions of the same shape.** The exclusion above
  still holds for a retention count, and for the same reason: nothing
  about `container_log_keep = 5` can be called correct or incorrect on
  its own. A threshold is the magnitude where that stops being true.
  It is a *classifier* over a population base can measure -- every
  function in the tree is either past it or not -- so "does this value
  get the answer right" is a question with a fact behind it, which is
  the property the two questions have always been testing for. Where a
  magnitude has that property, it gets the questions; where it does not,
  the paragraph above stands.

  1. **Does this value fail something that is already correct?** Yes ->
     the value is too low. This is question 1 with the same subject: a
     thing that *works*, not a thing that *passes*. A function that is
     hard to split is not an answer to it (ADR-00000029 -- the
     difficulty is a finding about the function), and neither is the
     size of today's violation population: how much code fails a
     threshold says nothing about whether any of it was correct.
  2. **Does this value pass something that is already defective?** Yes
     -> the value is too high. A threshold set at the tree's current
     worst case answers yes to this by construction, which is why "raise
     it until the tree is green" is not available.

  Where a range of values answers no to both, the **lowest** one is
  taken. That is invariant 4's direction applied to the residue: a
  too-high threshold fails silently -- it reports a clean tree it never
  bounded -- while a too-low one fails loudly, on a named function, in
  front of a reviewer who can dispute it. The harm falls on the side of
  the high value, so the low end of the range is the safe one.

  Applied to the three implementation standards ADR-00000029 adopts,
  against the distribution `just test metrics` measured at the start of
  #994 phase 3 (2026-09-03, 803 functions in 93 files; a count is a fact
  about a tree at a date, so what is written here is the evidence the
  decision rested on and not a figure this document keeps true):

  | Threshold | Q1: does it fail correct code? | Q2: does it pass defective code? | Yields |
  |---|---|---|---|
  | nesting depth | at 2, yes -- a scan over files, over lines, that then decides is three enclosing constructs with nothing to remove, and 65 functions sit exactly there. At 3, no function past it has yet been found irreducible; that answer is provisional and each phase-3 slice tests it | at 4, yes -- it admits the 16 functions this tree measures at exactly 4, and the ones inspected so far are unwritten guard clauses rather than irreducible nesting | **3**, the lowest value that clears Q1 |
  | function length | at 50, no -- the count is body CODE lines, so this repo's rationale comments and its heredoc bodies are already excluded, and what is left is 50 statements under one name; the same provisional answer as depth, tested by each slice | at 60, yes -- the distribution has no cliff anywhere above 50 (22 functions in 41-50, 21 in 51-60, 25 in 61-80), so every step up admits a further band of ordinary long functions and reports nothing new | **50**; with no natural cliff the two questions decide it, and Q2 is what stops the number drifting up |
  | positional parameters | at 4, yes -- bash cannot pass an array by value, so a paired in / out API (two arrays in, one out, two scalars) is five positions at its honest minimum, and 15 functions sit exactly at 5. At 5, no: the first slice took three of the eight functions above it to five or fewer, and in each the extra slots turned out to carry nothing a caller decided | at 6, yes -- the population above 5 is 8 functions and their shapes are the argument-shuffling ones the metric exists to find; one of them had four call sites passing the wrong thing in its eighth slot | **5**, the lowest value that clears Q1 |

  The three yields are the numbers the config-manager design document's
  chapter 0 named, which is worth stating plainly: the questions did not
  discover them, they RATIFIED them. That is the outcome the rule is
  for. A borrowed number nobody can re-derive is a preference with a
  citation, and the first person to find it inconvenient has nothing to
  argue with except taste.
- **It is a correctness test, not a risk analysis.** A permissive
  setting breaks nothing that works, so question 1 does not catch it;
  `[security] privileged` reaches `false` through the neither-yes branch,
  which is the right landing but not for the reason that matters. A
  destructive setting slips through the same gap: GHCR cleanup, once the
  manifest-aware action removed the way it could break a live tag, breaks
  nothing that works either, and it too lands off through the neither-yes
  branch. What makes both the right landing is invariant 4 -- the tension
  there is safe-versus-convenient, and the direction is safe: a
  destructive scheduled job nobody has watched run stays dry until
  somebody has. Where the two disagree the answer is still off, because
  both branches only ever license an ON.

Applied to seven of the defaults base ships today -- those chosen for
having a recorded rationale to check the rule against, not by a sweep of
every default in the tree -- it reproduces each. The questions and the
yield are the argument and are authored here; what base actually ships is
a moving fact about the tree, so the last column is where to read it and
not a copy of it. Invariant 10 is why: a literal in this column would be
a tracked duplicate of a settable value, with nothing to notice when the
two stop agreeing.

| Default | Q1: can on break a working setup? | Q2: does forgetting hurt? | Yields | Shipped value is read at |
|---|---|---|---|---|
| `[lifecycle] init` | no -- PID1 reaping is transparent to a correct single-service workload | yes -- zombies accrue and signals are not forwarded | on | `dist/.setup.conf`, `[lifecycle] init` |
| watchdog `restart-service` | yes -- it relaunches a service the workload meant to stop | -- | off | `dist/.setup.conf`, `[lifecycle] watchdog_on_fail` |
| `[network]` bridge (vs `host`) | yes -- a `172.17.x` address is not routable off-box, so cross-machine ROS goes silently unreachable | -- | off | `dist/.setup.conf`, `[network] mode` |
| `[security] privileged` | no -- it is permissive, so nothing that works stops working | no -- a container that does not need it is not hurt by its absence | off (the neither-yes branch) | `dist/.setup.conf`, `[security] privileged` |
| `[logging] wrapper_transcript` | no, once ADR-00000007 removed the re-flip | yes -- the debugging record is missing exactly when it is wanted | on | `dist/.setup.conf`, `[logging] wrapper_transcript` |
| GHCR untagged-image cleanup | no -- the shipped action is manifest-aware, so a child of a live tag is never a delete candidate; the `docker pull` 404 is the other tool's footgun | no -- orphan digests accumulate, but nothing that works stops working | off (the neither-yes branch) | `.github/workflows/ghcr-cleanup.yaml`, the `GHCR_CLEANUP_ENFORCE` gate |
| config mount-override writable | yes -- the container could rewrite the operator's file | -- | off | ADR-00000023, amendment #870 (a decision recorded, not yet a shipped setting) |

*Why it is fixed:* base's defaults are the configuration every downstream
runs before anybody edits anything, and they arrive by subtree upgrade
rather than by choice -- a downstream inherits a moved default in the
same commit that delivers the fix it asked for, from a maintainer who is
not in the room and cannot be asked. So the question a default must
survive is not "which setting do we prefer" but "which setting is safe to
apply, unattended, to a repo we cannot see". Invariant 4 fixes which
*direction* is safe when the tension is safe-versus-convenient; it does
not say whether a given setting is in that tension at all, or when a
default is allowed to move. Without a test the answer is recalled rather
than derived, and recollection does not survive the number of toggles
base already ships: two maintainers, or one maintainer six months apart,
reach opposite conclusions and both sound defensible. Making it two
questions makes a default *reviewable* -- it is challenged by disputing
an answer about the workload, which is a fact, instead of by disputing
taste, which is not. That is the same reason invariant 2 refuses a silent
skip: base is a shared foundation, so its judgement calls have to be
checkable by someone who was not part of them.

*Serves / established by:* invariant 5, which is this rule applied to
lifecycle knobs and where it was first written down (ADR-00000020 -- init
on as the transparent-and-footgun case, watchdog restart-service off as
the workload-semantics-changing one); ADR-00000019 (the network default,
question 1 answered by cross-machine ROS); ADR-00000007 (the case that
fixes the second answer to a question-1 yes); invariant 4, which supplies
the direction this supplies the test for.

## Design Principles

Beneath the invariants and above the individual decisions. An invariant
is a property of the product that no ADR may violate; a design principle
is a **judgement criterion** -- how base decides, when two correct-looking
options are both available. They are weaker than invariants on purpose: a
principle can be departed from in a decision that says why, and the ADR
recording that departure is the artifact. An invariant cannot.

P2 through P9 were **derived from decisions base has already taken**, and
each cites where it is currently written. P1 is the exception and is
labelled as one: it is the principle #994 imports from the config-manager
design document's chapter 0, and ADR-00000029 -- written for this change
-- is base taking that decision rather than a record of one base had
already taken. So this section records eight principles and establishes a
ninth.

Where a principle is already fully stated somewhere, this section points
at it and does not restate it -- duplicating a decision into a second
document is what ADR-00000028 and invariant 10 forbid, and a governance
document is not exempt from its own rule.

### P1. Early return is the default shape of every function

A guard clause at the top -- validate, reject, return -- is how a
function is written here, not a remedy applied once a nesting or length
threshold is breached. Thresholds are a net, not a target: depth 4 is
what happens when the guard was not written, and the number is how base
finds out, not what base is aiming at.

*Where written:* ADR-00000029, written for this change -- this is the one
principle here that base is adopting rather than restating, so the ADR is
the decision itself and not a citation of an older one. The framing it
corrects treated depth as a ranked list of violations to fix, which
produces the fixes and not the shape.
*Serves:* no invariant directly. It is the source shape ADR-00000014's
decomposition already assumes -- a lib is only a seam if its functions
can be read one branch at a time -- and so it stands behind invariant 7's
testability rather than beside it.

### P2. Derive the population; never enumerate it

Where a check, a figure or a roster can be computed from the tree, it is
computed. A hand-kept list is wrong from the first item added elsewhere,
and it is wrong silently -- the list does not know it is short, so the
check it feeds reports clean.

*Where written:* ADR-00000026 (eligibility is computed from each job's
`runs-on`, explicitly "a label-family pattern rather than a roster",
after `_LINT_TOOLS`, the downstream roster and the release archive path
list had each been missed by the next addition); ADR-00000028 (a figure
that can be computed from the tree is computed when it is needed and not
stored -- and the one exception, a figure that names what it measured, is
stated there rather than left to be found); `doc/adr/README.md` ("There is
no database and no manually-curated master list of numbers -- the set of
`doc/adr/NNNNNNNN-<slug>.md` files *is* the registry").
*Serves:* invariants 2 and 10.

### P3. A check that finds nothing must distinguish an empty population from a broken scan

"Zero violations" and "zero files examined" are different results and a
guard has to be able to say which one it got. A scan whose matcher has
stopped matching reports exactly what a clean tree reports, so the
difference has to be measured -- the count of things examined -- and a
zero there is a refusal, not a pass.

*Where written:* ADR-00000026 (anything the lint cannot statically prove
is eligible -- the rule fails closed -- and `ci-rollup` fails a fork PR
rather than collapsing a guarded skip into a green required check).
*Serves:* invariant 2. This is the mechanical half of "never fail
silently": a gate that has quietly stopped gating is the silent failure
that is hardest to notice, because its output is indistinguishable from
success.

### P4. One rule has one owner and many entry points

A rule is implemented once and every caller reaches that implementation.
Two implementations that must agree are a drift with a delay on it, and
the delay is however long it takes for one of them to be edited alone.

*Where written:* ADR-00000011 sec.5, for the OWNER half only -- one driver
per tool, so "adding a tool is a new driver + a folder, the dispatcher is
untouched". That ADR says nothing about CI. The entry points are written
in `.github/workflows/self-test.yaml`, where every `lint-static` matrix
entry runs `./script/test/test.sh --<tool>-only` and the hadolint job's
comment states the property in those terms: "this job now runs the SAME
driver ... that `just test` runs locally ... so local `just test` and this
CI job can never drift". What makes the "many entry points" half hold
rather than be hoped for is neither of those, but the `_LINT_TOOLS`
completeness guard in `test/bats/unit/self_test_yaml_spec.bats`: a lint
can have one owner and still reach only one caller, and four shipped
local-only before that guard existed to fail a `_LINT_TOOLS` entry with no
CI job (the table itself is explicitly not the CI gate -- doc/test/TEST.md,
"Static lints and where they are enforced"). ADR-00000024 (the
mechanical half of the rule is gated by one lint); invariant 8
(`_is_deployable_stage` is "the one predicate", and the invariant is
stated in full precisely "so the two cannot disagree"); the
`doc-counts` gate, described in `test.sh` as one rule with three entry
points of which this is the blocking one.
*Serves:* invariants 2 and 6.

### P5. Zero special cases outranks a shorter invocation

Where a rule can hold without exception at the cost of ergonomics, base
pays the ergonomics. One rule with no exceptions is learnable once and
stays true; a rule with two exceptions has to be recalled with them, and
the third exception is the one nobody remembers.

*Where written:* ADR-00000011 sec.1, in base's own words: "The cost
(longer invocations) is accepted in exchange for one rule with no
exceptions." `just build` became `just docker build`, reversing
ADR-00000010's top-level-docker carve-out.
*Serves:* invariant 6 -- a thin caller can only stay thin if the shape it
forwards has no cases in it.

### P6. Relocate into an existing seam before creating a new one

When code needs a home, the first question is which established seam it
belongs to; a new file is created only for what genuinely has none. A
parallel namespace that duplicates seams already present is how a
decomposition ends up with more surface than it removed.

*Where written:* ADR-00000014 rule 1 ("Relocate into existing libs first;
create new libs only for the homeless ... We do NOT introduce a parallel
`setup_*.sh` namespace that duplicates seams that already exist").
*Serves:* no invariant. It is a source-architecture criterion, and the
seams it applies to are named in `CONTEXT.md`.

### P7. Every escape hatch is explicit, named, and records why it was taken

base ships escape hatches rather than pretending every case fits. What it
does not ship is a silent one: taking the hatch is a visible act, it is
named at the point of use, and where the consequence outlives the person
who chose it, the artifact carries the reason.

*Where written:* ADR-00000001 (compose-native mechanisms are an escape
hatch "reserved for genuinely custom needs", not a second main path);
ADR-00000025 (`setup deploy` refuses while an untracked config layer
exists, and the explicit override records in the bundle which sections
came from it, so the record "travels with the artifact and reaches the
person in the field, who is not the person who chose to bypass the gate"); ADR-00000023 as amended by
#870 (a config mount-override is read-only with an explicit `rw` opt-in);
the `changelog-entry` opt-out, which is a comment pair carrying `<why>`;
the `arch-literal` lint, whose mapping exception "opts out with a stated
reason".
*Serves:* invariant 2.

### P8. Additive first, retirement second

A change that would break a consumer is split so the break is its own
deliberate step. The new path lands beside the old one, both work, and
the removal is a separate decision that can be timed, announced and
reverted independently of the thing that motivated it.

*Where written:* ADR-00000005 ("Rollout is additive first, retirement
second, split so the breaking change is deliberate"); ADR-00000014 rule 3
(one slice = one issue = one PR, behaviour identical, the existing specs
standing as the regression net).
*Serves:* invariant 6. base propagates by subtree upgrade, so every
consumer takes the step at a moment base does not choose; a combined
add-and-remove is a step they cannot take halfway.

### P9. A record lives where its reader will be standing

The same fact is not written into every document that could hold it. It
is written where the person who needs it is already looking, and the
other places link to it. Which document that is follows from who the
reader is and what they are trying to decide.

*Where written:* `script/test/drivers/changelog_entry.sh`'s header, which
states the rule and the placement together -- "this repo already decided
that the PR body is the canonical decision record, enforced by a hook on
`gh pr create` ... A changelog entry answers two questions -- what
changed, and does it affect me. Not why, and not what was rejected";
ADR-00000013 (drop the transient issue number from a code comment, keep
the sentence -- the number's reader is in the tracker, the sentence's
reader is in the file); ADR-00000027 sec.3 (the release classification's
reasoning is recorded so a wrong call is reviewable rather than
invisible).
*Serves:* invariant 10 -- this is its "authored, not derived" half asked
about placement rather than about generation.

### Stated elsewhere, not repeated here

Three principles that belong to this layer by shape are already stated in
full above it or beside it, so they are referenced rather than restated:

- **Naming follows ownership** -- the standard name is base's and is
  regenerated, a suffix marks the operator's and is never rewritten. This
  is part of invariant 8, not a principle beneath it.
- **Test files mirror source; source structure is never decided by
  tests** -- ADR-00000015, which states it and its consequences
  completely.
- **Deep modules: a small interface over a private implementation** --
  ADR-00000014 plus the seam vocabulary in `CONTEXT.md`.

## Conflict Priority

What this order is **for**: two properties base holds are both
legitimate, both wanted, and a particular decision cannot have both. The
order says which one gives way. That is all it says.

What it is **not** for: it is not a licence to rank "this is hard" above
anything. Difficulty is not one of the properties below and never enters
the comparison -- a change that is hard to make safely is a finding about
the code (ADR-00000029), not a competing claim. A decision that reaches
for this order has to name the two properties in tension and show that
having both is genuinely impossible here; if it cannot, the conflict is
imagined and the order does not apply.

Higher wins.

**1. Correctness of what the consumer runs.** The artifact a downstream
builds, runs or ships to the field behaves as its operator has every
reason to expect. *Rests on invariants 1, 2 and 8.*

**2. A defect is loud, and early.** Where something is wrong, the run
says so at the first point a human is present, rather than continuing and
reporting green. *Rests on invariant 2.*

**3. One owner for one rule.** A rule is implemented once, propagated,
and reached through as many entry points as are wanted. *Rests on
invariants 6 and 10; this is P4 as a property rather than as a
criterion.*

**4. Convenience at the point of use.** Fewer steps, shorter
invocations, less to type and less to know. *Rests on no invariant, which
is why it is last -- not because it does not matter.*

### Worked examples, each from a conflict base actually settled

**1 over 2 -- the log-retention clamp (ADR-00000021).**
`container_log_keep` and `container_log_days` are validated as positive
integers by the schema registry, so a bad value in `.setup.conf` is
refused loudly at `just setup`, where a human is standing. The same
values arrive at the container entrypoint a second time through a
hand-editable `compose.yaml`, and there
`dist/script/docker/runtime/logging.sh` **clamps** a non-positive value
back to 20 / 14 without a word. Property 2 taken alone says refuse; the
refusal would mean the container does not start, or starts with a prune
that wipes every log -- so property 1 wins and the clamp is silent. The
order is what makes this a decision rather than an inconsistency with
invariant 2: loud where a human is present, safe where one is not.

**2 over 3 -- the fork-PR rollup (ADR-00000026).** The one-owner answer
to "did CI pass" is a single rollup status summarising the matrix, and a
guarded job that skips contributes a skip to it. base refuses that:
`ci-rollup` **fails** a fork PR rather than let a guarded skip collapse
into a green required check, and the eligibility lint fails closed on
every `runs-on` it cannot statically prove. A vacuous green is the
failure invariant 2 exists to prevent, so the tidier single status gives
way.

**3 over 4 -- namespacing every action (ADR-00000011 sec.1).** Recorded
in the ADR's own words: "The cost (longer invocations) is accepted in
exchange for one rule with no exceptions." `just build` became `just
docker build`, reversing the top-level-docker carve-out ADR-00000010 had
made for exactly the convenience being given up here.

**1 over 4 -- the network default (ADR-00000019) and the `/opt` bake
(ADR-00000024).** #794 proposed flipping `network.mode` to `bridge` on
least-privilege grounds, which is the more idiomatic and more convenient
posture; it was reversed because a bridge's `172.17.x` address is not
routable off-box and cross-machine ROS would go silently unreachable.
Likewise `~/name` is the convenient path to source and `/opt/name` is
not, but `ENV HOME` resolves at build time, so anything sourced through
`$HOME` breaks under a different `USER_NAME`; the symlink stays for
discoverability and nothing sources it.

**2 over 4 -- the deploy refusal (ADR-00000025).** The convenient
outcome of `setup deploy` is a bundle. base refuses to produce one while
a gitignored `.setup.conf.local` exists, because a bundle built from a
layer visible on one machine cannot be reproduced from a clean checkout
and nothing about the bundle would say why.

### When the order does not decide it

Two properties at the same rank do not resolve by this list, and neither
does a conflict between an invariant and anything at all -- an invariant
is not a property that can give way, which is what makes it an invariant.
A decision that finds itself trading one invariant against another has
found a defect in the invariants, and the artifact is an amendment to
this document, not an ADR that picks a winner.

## Product Shape

- **Vendored subtree, thin caller** (invariant 6): base is the shared core;
  downstream calls it.
- **Single-service lifecycle ownership** (invariant 1): base owns build -> run
  -> supervise -> log -> field-deliver for one service.
- **One source, many render targets:** `setup.conf` + host detection resolve
  once and render `compose.yaml`, `.env.generated`, the container-bound
  `.env`, `deploy.sh`, and the baked runtime `ENV` -- so the same configuration is
  correct on the dev host and in a field image (ADR-00000003). The source is
  a layered chain of files -- shipped default, the repo's committed
  override, the operator's gitignored per-worktree override -- resolved
  section-by-section, with no ambient environment variable able to steer it
  (ADR-00000025).

## Roadmap

- **Closing the composability gap.** Invariant 3's property is stated; the
  parameterised generate API that delivers it for shape-varying fields is not
  built yet (#1087). Who consumes it is not base's concern.
- **Field-delivery maturity.** The `deploy.sh` bundle (ADR-00000003) grows a
  richer per-parameter confirmation surface (the graphical TUI page deferred
  from the #497 epic).
- **v1.0.0 cleanups.** Retire the legacy `[deploy] runtime` alias and other
  deprecations; land the full real-flow `just base upgrade` e2e test (#772).
- **Self-hosted CI evaluation.** Guard self-hosted-eligible jobs to same-repo
  events as the prerequisite (#766), then decide on migration.
- **ADR / PRD governance.** This PRD plus the ADR audit (the remainder of #808)
  and the ADR-numbering guard (landed) keep the decision log coherent.


# ===== base doc/adr/*.md（全部 ADR 全文，含 README 索引） =====



## ---- FILE: doc/adr/00000001-setup-conf-vs-compose.md ----

# Responsibility split between setup.conf and compose-native mechanisms

> Serves: mechanism -- the config-resolution boundary (setup.conf vs
> compose-native); serves the one-source-render goal, no invariant.

- **Date:** 2026-05-28
- **Status:** Accepted

## Context

`base` uses `setup.conf` + `setup.sh` to generate `compose.yaml` and
`.env`. This abstraction layer is not the Docker standard -- the
standard approach is to hand-maintain `compose.yaml` plus `.env`,
using `compose.override.yaml` (or `-f overlay.yaml`) for environment
overrides and profiles for variant selection.

setup.conf exists because it provides things plain compose cannot:
system detection (IMAGE_NAME rules, USER_NAME, WS_PATH, GPU, GUI),
TUI editing with input validation, multi-language defaults, and
template-to-repo section-level inheritance.

The question of "what belongs in setup.conf vs. what should go
through compose-native mechanisms" was never written down. It
surfaced concretely while designing per-instance isolation for the
isaac downstream repo (multiple Isaac Sim instances each needing
their own ports and cache directory). Two opposing options emerged:
add the instance-overlay mechanism to setup.conf via section-level
overlay, or use compose-native override yaml (`_compose_project
-f compose.yaml -f config/instances/<name>.yaml`). The first would
require changing setup.conf's existing section-replace semantics to
key-level merge; the second is a per-repo customization that not
every downstream needs.

## Decision

**setup.conf is the main path -- it covers all common / standard
needs. Compose-native mechanisms (`compose.override.yaml` /
`-f overlay.yaml` / profiles) are an escape hatch reserved for
genuinely custom needs.**

setup.conf extension principles:

1. If the need is "common functionality that multiple downstream
   repos will use" -- add it to setup.conf (new section or key),
   have setup.sh emit it into `compose.yaml` / `.env`, and wire up
   TUI editing with input validation.
2. If the need requires system detection (IMAGE_NAME rules,
   USER_NAME, WS_PATH, GPU, GUI, etc. -- things compose.yaml syntax
   alone cannot express) -- it must go through setup.conf.
3. The existing "template-to-repo" section-level inheritance is
   preserved; downstream repos' override expectations stay intact.

When to use compose-native mechanisms (escape hatch):

1. The customization is limited to a single repo or single
   scenario, and pushing it into setup.conf would dilute the
   abstraction's generality -- e.g. isaac's per-instance cache and
   port isolation (an Isaac-Sim-specific problem).
2. Pure runtime value injection that does not affect static
   configuration -- e.g. `--env-file <overlay>.env` injecting
   additional environment variables.
3. Structural overrides that benefit from compose's native
   deep-merge -- write `compose.override.yaml` (compose loads it
   automatically) or a custom overlay yaml used with `-f
   overlay.yaml`.

Decision rule: when asked "should base support this?", first
evaluate generality -- "would N downstream repos use it?". Yes
to N>=2 -> setup.conf. Only one repo -> escape hatch.

## Alternatives

- **Fully align with the Docker standard (drop setup.conf)** --
  loses auto-detection, TUI, and multi-language defaults. Users
  would have to hand-write compose.yaml with placeholders like
  `${USER_NAME}-${IMAGE_NAME}`, breaking the "downstream repo
  works out of the box" core value proposition.
- **Push every overlay mechanism into setup.conf** -- e.g.
  implement per-instance via setup.conf section overlay. Requires
  changing section-replace to key-level merge, re-emitting a
  per-instance compose.yaml, and forces base to handle
  single-repo customization cases. Violates the generality
  principle.
- **Pre-emptively bake every possible need into setup.conf** --
  violates YAGNI; setup.conf bloats into a do-everything mega
  abstraction, and the TUI grows accordingly complex.

## Consequences

- New-feature decision rule: evaluate generality first (do
  multiple downstreams need this?). Common -> full implementation
  in setup.conf; single-repo customization -> compose-native
  mechanism.
- isaac's per-instance isolation is single-repo customization
  (Isaac Sim's cache-lock issue is product-specific). It will be
  implemented via compose override yaml, without extending
  setup.conf's merge semantics.
- setup.conf keeps section-replace semantics. No change to
  key-level merge.

**Amendment (ADR-37 D4 #1130, 2026-09-07): type-aware merge for TOML.**
The `.setup.toml` format introduces type-aware merge semantics: scalar
keys within a `[table]` get key-level merge (upper layer overrides only
the keys it defines; unmentioned keys inherit), while `[[array of
tables]]` entries get array replace (the entire array comes from the
highest layer that defines it). This applies only to TOML layers; the
INI `.setup.conf` chain retains section-replace. The TOML merge runs
in Python inside the containerised bridge (ADR-37), where type
information (dict vs list) is natively available.
- If the same kind of customization appears in 3+ repos later,
  re-evaluate -- it may graduate into setup.conf.
- Downstream repos can still write `compose.override.yaml` for
  local ad-hoc tweaks (compose auto-loads it); no need to detour
  through setup.conf.

**Amendment (#600 / #881, 2026-08-17): the per-instance overlay named
above is historical, not a mechanism to reach for.** `--instance`,
`INSTANCE_SUFFIX` and `config/instances/<name>.{yaml,env}` were removed
by #600; base is **single-instance** -- one fixed-name container /
project per repo, and multi-instance orchestration belongs to the
compose layer. The decision recorded here is unchanged, and this is not
a reversal of it: per-instance isolation was the single-repo case the
generality rule was argued over, and its removal is that rule applied.
Running two *checkouts* of the same repo side by side is a different
problem, and it **is** answered inside setup.conf, by `[project] name`
in `.setup.conf.local` (#893, ADR-00000025) -- read that ADR rather
than the Context paragraph above for a mechanism that exists today.


## ---- FILE: doc/adr/00000002-no-latest-tag.md ----

# No `latest` tag for `base`; resolve newest semver dynamically

> Serves: PRD invariant 6 (base is a subtree; downstream a thin caller)
> -- immutable version pinning of the propagation refs; mechanism.

- **Date:** 2026-05-29
- **Status:** Accepted

## Context

`base` ships as an immutable, semver-tagged source that downstream
repos consume in two build-time-critical ways:

1. **As a `git subtree`** under `.base/`. `upgrade.sh` records the
   exact pulled tag in `.base/.version` and uses `_semver_cmp(local,
   latest)` to decide whether an update is available and to refuse
   implicit downgrades (per SemVer §11).
2. **As reusable GitHub Actions workflows.** Each downstream
   `.github/workflows/main.yaml` pins
   `ycpss91255-docker/base/.github/workflows/build-worker.yaml@vX.Y.Z`
   (and `release-worker.yaml@vX.Y.Z`); `upgrade.sh` Step 4 rewrites
   those refs to the target tag on every upgrade.

The question "should `base` also publish a moving `latest` tag (a ref
that always points at the newest release)?" was never written down,
yet the entire version-tracking machinery silently assumes the answer
is no. This came up while clarifying how `make upgrade` (with no
`VERSION`) resolves "the latest version": it does **not** read a
`latest` ref — `_get_latest_version()` runs
`git ls-remote --tags --sort=-v:refname | grep -oP
'refs/tags/v\d+\.\d+\.\d+$'`, picking the highest stable semver and
excluding `-rcN` prereleases by construction. GitHub's release page
also auto-marks the newest non-prerelease release as `Latest`, which
is a UI label on a release, not a git ref. Neither mechanism is a
physical `latest` tag, and nothing in the repo creates one.

Note this decision is scoped to `base`'s **own version tags** —
i.e. build-time dependency refs. It is deliberately distinct from the
**output Docker images** downstream repos publish, where a rolling
`:latest` (`is_latest` input) and `test-tools:main` are intentionally
supported for opt-in consumers.

## Decision

**`base` will not provide a `latest` tag (nor any moving ref) for its
own releases. The canonical "give me the newest version" path stays
dynamic semver resolution, and all build-time references stay pinned
to immutable `vX.Y.Z` tags.**

"Newest" is already served three ways without a physical `latest`
ref, and these remain the only supported paths:

- `make upgrade` (no `VERSION`) → `_get_latest_version()` resolves the
  highest stable semver tag (currently `v0.39.0`).
- Dependabot watches the `@vX.Y.Z` refs in `main.yaml`, compares
  against the newest tag, and files a bump PR.
- GitHub's auto-applied release `Latest` label points humans at the
  newest non-prerelease release.

## Alternatives

- **Publish and force-move a `latest` git tag on every release**
  (`git tag -f latest && git push -f`). Rejected: maintaining it
  requires force-pushing a tag on every release, which rewrites a ref
  consumers may have already fetched and breaks local clones / CI
  caches — a widely-discouraged practice. It adds maintenance burden
  and footguns for zero new capability, since "newest" is already
  resolvable dynamically.
- **Point downstream `@ref` at a `latest` (or `main`) ref instead of
  `@vX.Y.Z`.** Rejected: a mutable ref means the same downstream
  commit can execute different `base` workflow code on different CI
  runs — non-reproducible "green yesterday, red today" with zero
  downstream diff and no audit trail of which `base` version a build
  ran against. A mutable ref is also a supply-chain hazard: anyone
  able to move the ref silently changes what every downstream CI
  executes. GitHub's own guidance is to pin reusable workflows /
  actions to a release tag (or full SHA), not a moving ref.
- **Keep a `latest` ref purely for the subtree pull (not the
  workflow refs).** Rejected: it would break the version-tracking
  core. `.base/.version` and `_semver_cmp` depend on a concrete pinned
  version to compute "update available" and to block downgrades; a
  `latest` pin makes `local_ver` meaningless and `make upgrade-check`
  unable to tell whether a repo is behind. The repo has already been
  burned by mere `.version`/tag mismatches (e.g. the v0.18.2
  `.version` fix where stale pins made `upgrade-check` loop "upgrade
  available" forever); a `latest` ref would make that class of bug the
  default. It would also lose the automatic `-rcN` exclusion that the
  current regex-based resolution provides for free.

## Consequences

- **Costs avoided:** non-reproducible CI, supply-chain exposure from a
  mutable ref, broken semver comparison / downgrade guards, force-push
  tag churn, and bespoke prerelease-exclusion rules.
- **Cost accepted:** consumers who want the newest version must go
  through one of the three resolution paths above rather than pinning
  to a single stable string like `@latest`. This is intentional — the
  pin-to-an-immutable-version friction is the feature.
- **No follow-up work.** This ADR documents a status quo that was only
  ever encoded in `upgrade.sh` and the pinning conventions; no code
  changes. Future contributors proposing a `latest` tag for `base`
  should treat this as the standing rejection and supersede it only
  with a new ADR if the trade-offs change.
- The separately-supported rolling tags for **output images**
  (`is_latest` → `:latest`, `test-tools:main`) are unaffected; this
  decision does not constrain them.


## ---- FILE: doc/adr/00000003-env-vs-workload-param-boundary.md ----

# Environment vs runtime parameter boundary and field delivery model

> Serves: PRD invariant 3 (composable by construction) via the axis-A
> `.env`-overlay model; also the one-source -> many-render goal (field
> delivery).

- **Date:** 2026-06-02
- **Status:** Accepted
- **Amended:** 2026-07-15 -- the structured-config **Field** cell of the
  parameter-routing table gains a field override channel (baked default +
  optional mount-wins `-v`), making it symmetric with the env row's `-e`; and
  the "compose does not travel" delivery model is refined to "a fully-resolved,
  self-contained compose travels". The general git-tracked provisioning axis
  this makes explicit, and the mechanism, are recorded in ADR-00000023.
- **Amended:** 2026-08-26 (#868) -- **A2's file-role assignment is REVERSED.**
  `.env` is now the tool's generated, container-bound defaults and
  `.env.local` is the user's override layer. See "Amendment: the env-file
  naming rule (2026-08-26)" below; the routing table and the A2 bullet list
  are annotated in place.

## Context

ADR-00000001 established "setup.conf is the main path; compose-native
mechanisms are an escape hatch", and listed "pure runtime value injection
(`--env-file <overlay>.env`)" as one escape-hatch case -- but it never drew
the line between what counts as a stable *environment* parameter and what
counts as a volatile *runtime* parameter.

That gap surfaced concretely: downstream repos keep wanting to push volatile
runtime params (env vars) into `setup.conf`, while `setup.conf` is meant to
hold "set-once, machine-bound" environment params. The intuitive criterion
"rarely adjusted" is subjective -- each maintainer draws it differently, so
the boundary does not hold over time.

Two further problems compounded this:

- Workload env vars are baked into `compose.yaml`'s `[environment]` block.
  Any tweak flips `SETUP_CONF_HASH`, forcing a regenerate (drift); committing
  them churns git history; section-replace forces copying a whole section to
  change one key.
- The field-deployment scenario keeps **only the docker image** -- the
  host-side `setup.conf` / `.env` / `compose.yaml` / wrappers do not travel
  with it. Workload env living in `compose.yaml` vanishes in the field, and
  container flags (`--privileged` / `--device` / `--network` / `--gpus`)
  cannot be baked into any image.

This is not a one-off. The same "per-invocation / one-off / standalone
override that does not belong baked into `setup.conf`" need has recurred and
was each time patched with a different escape hatch:

- #279 -- one-off `--build-arg` overrides, solved with a CLI flag pass-through.
- #338 -- per-invocation `[gui]` / x11-cookie overrides, solved with CLI flags;
  its body notes that editing `setup.conf` then reverting for a single run "is
  awkward".
- #465 -- isaac multi-instance ports / cache isolation, solved with a
  compose-override overlay (see ADR-00000001).
- #462 -- a `runtime.env` mirror so standalone scripts can read `[environment]`.

#497 consolidates that sprawl into one coherent workload-overlay layer. The
relationship to #75 is parallel, not contradictory: #75 consolidated scattered
*static config* (5 conf files) into one `setup.conf`; this decision
consolidates scattered *runtime overrides* into one `.env` overlay. #75's
"`.env` is a derived artifact" property concerned static-config generation; a
runtime overlay is a category #75 never addressed.

The implementation work is tracked in issue #497; this ADR records only the
rationale.

## Decision

**Boundary criterion.** Primary axis A -- *binding target*: "does this value
change when you switch machines?" Yes / machine-capability (GPU, arch, APT
mirror, display, privileged) -> environment, stays in `setup.conf`. Changes
per task (which dataset, which env var) -> workload. Axis C (does it need a
rebuild?) is the tie-breaker for grey cases.

**Three delivery channels** -- only channel 1 reaches the field:

1. Baked into the image (`ENV` / build-arg / COPY'd config + entrypoint).
2. Dev-host run config (`compose.yaml` + env files + wrappers) -- does not
   travel.
3. Field launcher (`docker run` flags) -- supplies what an image cannot carry.

**File roles ("A2").** `setup.conf` (committed source, environment) +
`setup.sh` detection render multiple targets:

- `.env.generated` -- derived interpolation cache (today's `.env`, renamed;
  audited to be a 100% pure cache with no hand-authored content, so
  regeneration is loss-free). Fed to compose via `--env-file` for
  `${VAR}` interpolation only; it is NOT injected into containers, so the
  cache's USER_UID / PRIVILEGED / SETUP_* metadata never leak into the
  runtime env.
- `.env` -- repurposed as the gitignored **user workload overlay**; never
  touched by `setup.sh` (scaffolded once on first apply). Injected into
  each container via the service `env_file: - .env` directive. (Two-role
  split, refined in #502: the interpolation cache and the container
  overlay are distinct files with distinct delivery paths, not a single
  `env_file: [.env.generated, .env]` list. compose precedence is
  `environment:` > `env_file`, so the overlay overriding `[environment]`
  defaults completes in S3, when `[environment]` becomes the
  lowest-precedence baked `ENV`.)
  **REVERSED 2026-08-26 (#868):** `.env` is the tool's generated
  container-env defaults and `.env.local` is the user's overlay. The
  `env_file:` list is `[.env, .env.local]`, later wins. See the amendment
  section at the end of this ADR.
- `compose.yaml` -- dev-host run config.
- `deploy.sh` (new) -- self-contained field launcher: a `docker run` with
  flags inlined, generated by its own generator, with a per-parameter
  confirmation step before generation; the target image tag is a
  repo-selectable stage.
- Runtime stage bakes `[environment]` defaults as `ENV` so the field image
  carries sane defaults on its own.

**Detection stays in `setup.sh`** (code), not expressed as `$()` inside
`setup.conf`.

**Bare `docker compose up` support is dropped** -- everything runs through
`make` / wrappers. This is precisely what frees the `.env` name to be
repurposed.

## Parameter routing (usage)

Where a given parameter lives follows axis A ("does it change when you
switch machines?"). Three channels, distinguished by *kind* of value:

| Parameter kind | Where it lives | Dev host | Field |
|---|---|---|---|
| machine-bound / set-once (GPU, `privileged`, mounts, `IMAGE_NAME`, APT mirror) | `setup.conf` (committed) | rendered into `compose.yaml` | inlined as `docker run` flags in the generated `deploy.sh` |
| volatile workload **env vars** (`ROS_DOMAIN_ID`, `LOG_LEVEL`, tokens) | `.env.local` (hand-authored, gitignored) -- was `.env`, reversed in #868 | injected per service via `env_file: [.env, .env.local]`; the generated `.env` carries the `[environment]` defaults and `.env.local` overrides them | shipped in the bundle as `.env` (defaults, incl. `WATCHDOG_*`) + `.env.local` (operator overrides), on top of the baked `ENV` |
| structured app **config** (bridge topics, pipeline lists) | an app config file/dir (e.g. `config/<repo>/*.yaml`) | bind-mounted into the container (edit + restart, no rebuild) | `COPY`-baked default + optional field `-v` override (mount-wins) |

The third channel is distinct from the `.env` overlay: the overlay
carries flat `KEY=VALUE` env vars only; structured config goes to its own
file and follows the immutable-image bake model of ADR-00000001 (dev
bind-mount for fast iteration, deploy-time bake for a self-contained
field image). Concrete use-case examples (which env var goes where for a
given repo) live in the README, not here -- this records the routing
*decision*, not a tutorial.

## Alternatives

- **A1 -- keep `.env` derived, add a new `env.local` overlay.** Zero
  migration, preserves the "derived = never edit" invariant, and degrades
  gracefully under a bare `docker compose up`. Rejected only because the user
  always uses wrappers and prefers the conventional `.env` as the edit target;
  the convention win drove the choice toward A2.
- **A3 -- single `.env`, both derived and hand-edited, `setup.sh` preserves
  user keys.** Breaks the "derived = never edit" invariant, risks clobbering
  user data on a parser bug, and muddies the drift-hash boundary. Rejected.
- **Detection-as-commands in `setup.conf` (`USER_UID = $(id -u)`).** Turns a
  committed, shared config into arbitrary code execution; does not remove the
  materialized cache (docker needs literal values); discards tested, i18n'd
  detection logic. Rejected.
- **No-file live-inject** (wrapper computes detection each run, no cache
  file). Loses the inspectable cache and the home for `SETUP_*` drift
  metadata, and recomputes every run. Rejected; keep `.env.generated`.
- **`compose.override.yaml` as the workload channel.** Native and powerful,
  but forces hand-written compose syntax -- contradicting the `setup.conf`
  abstraction. Per ADR-00000001 it stays an escape hatch, not the default
  path for workload env.

## Consequences

- Editing `.env` (workload) needs only `make run`: no compose regenerate, no
  `SETUP_CONF_HASH` flip, no git churn, no section-copy.
- 17-repo migration: `.env` -> `.env.generated`, add the new `.env` overlay,
  update gitignore (fanout in the spirit of #201).
- `setup.sh` gains a single flag-resolution layer feeding two thin renderers
  (`compose.yaml` and `deploy.sh`); two output formats to maintain.
- The field image is self-contained for workload env defaults (baked `ENV`);
  container flags are supplied by the generated `deploy.sh` in the field.
- Bare `docker compose up` no longer works (empty interpolation). Accepted
  because the workflow is wrapper-only.
- Refines ADR-00000001: its "pure runtime value injection (`--env-file`
  overlay)" escape-hatch case becomes the blessed primary path for workload
  env, via the `.env` overlay + `env_file:`.
- Consolidates the runtime-override escape hatches (#279 / #338 / #465 /
  #462): future such needs route through the `.env` overlay or the unified
  flag-resolution layer rather than spawning a new per-case mechanism.
  Parallel to #75's static-config consolidation, not a reversal of it.
- **Amended (2026-07-15, ADR-00000023):** the structured-config Field cell is
  no longer bake-only. It is now a `COPY`-baked *default* plus an optional
  field `-v` override (mount-wins) -- the file analog of this ADR's env-row
  `deploy.sh -e`, so both rows are symmetric. The general axis this makes
  explicit is **git-tracking**: a committed config file is the developer's
  baked default; a gitignored / bundle-shipped file is the operator-editable
  overlay that mounts over it in the field without a rebuild. The
  "compose does not travel" delivery constraint (channel 2 above) is likewise
  refined -- a *fully-resolved, self-contained* compose does travel, with no
  `setup.conf` / `.env.generated` dependency. Both the provisioning axis and
  the field-deploy mechanism are recorded in ADR-00000023.
- Open questions deferred to #497: `deploy.sh` confirm-step UX (extend
  `setup_tui.sh` vs new flow), final naming (`deploy.sh` vs `field-run.sh`),
  the fate of `runtime.env` (#462), and interaction with #439 (legacy
  `.env.example` / IMAGE_NAME fallback). The last of those is settled in
  the 2026-08-26 amendment below: `.env.example` has no role and no code
  left reading it.

## Amendment: the env-file naming rule (2026-08-26, #868)

**A2's choice of which file the user edits is reversed.** One rule now
governs every generated name in the repo: **the standard name is ours; a
suffix marks a local variant.**

| file | whose | enters the container | fate |
|---|---|---|---|
| `.env` | ours -- shipped / generated defaults | yes | regenerated on every apply |
| `.env.local` | the user's / operator's overrides | yes | never touched by tooling |
| `.env.generated` | ours -- host-detection interpolation cache | no | unchanged by this amendment |

### Why the reversal

A2 picked `.env` as the user's edit target because that is the
conventional meaning of the name in the dotenv / Laravel tradition. That
reasoning is still true in isolation, and the ecosystem is genuinely split
-- Next.js treats `.env` as shared committed defaults with `.env.local` as
the user's override, which is the other half of the same convention. With
no external authority to defer to, the choice is internal, and internal
consistency decided it: `Dockerfile`, `compose.yaml` and `.setup.conf` are
already ours-and-regenerated under their standard names, and
`.setup.conf.local` is already the operator's local variant under a
suffix. One rule that covers all of them beats a rule for the env family
and a different rule for everything else.

`.env.generated` deliberately keeps its suffix: it exists only to fill
`${VAR}` slots in `compose.yaml` via `--env-file` and never reaches a
container. Renaming it to `.env` would make one name mean two things that
do not arrive at the same place -- the exact confusion the rule removes.
Its suffix marks a category, not ownership, and it also carries the "do
not hand-edit" signal.

### What the reversal forced, beyond the names

A2 acknowledged that compose ranks `environment:` above `env_file` and
deferred the fix to S3. Leaving it deferred is what makes the rename
dangerous rather than cosmetic: an override channel that exists, is
documented, and is silently outranked is worse than no channel at all,
because nothing reports the loss. So the `[environment]` list and the
`[lifecycle] WATCHDOG_*` block moved OUT of every service `environment:`
list and into the generated `.env`, on the dev host and in the field
bundle alike. `environment:` now carries only what cannot move: the X11
passthrough, which interpolates from the running host's own shell.

One shape is exempt, and deliberately: a `[stage:*]` with
`environment.env_inherit = false` asked to DROP the top-level list, so
handing it the shared `.env` would put it straight back. That stage takes
`.env.local` alone and restates its own env plus the lifecycle block
inline. It is the one place a compose `environment:` entry still outranks
the override file, and it is reached only by a conf that opted out.

Moving the list also moved its `${VAR}` expansion. compose used to resolve
those references itself against `.env.generated`; an `env_file` value is
taken literally, so `apply` expands against the cache before writing and
leaves genuinely unknown names visible rather than silently empty. Values
are written single-quoted for the same class of reason -- an unquoted
env_file value is truncated at an inline ` #` and a double-quoted one has
`${...}` expanded, both silently.

### The sub-questions the epic left open

- **Is `.env` committed or gitignored?** Gitignored, and it already was.
  It is generated from `.setup.conf` and host detection, so committing it
  would put a machine-specific render in everyone's tree and churn git on
  every apply. `.env.local` joins it in the canonical gitignore list, for
  the reason `.setup.conf.local` is there: an untracked layer that got
  committed silently becomes everyone's config.
- **Does `.env.example` still have a role?** No, and there is nothing left
  to remove -- the check the epic asked for came back empty. `init.sh`
  stopped generating it, and the `IMAGE_NAME` fallback #439 touched no
  longer reads it: detection resolves the name through `[image] rules`
  with `@default:unknown` as the last resort (`detect_image_name`), and
  two specs already assert the file is NOT created. The generated `.env`
  is the example now: it lists every container-bound value in effect, with
  its resolved value, which is strictly more than a sample file could
  carry. base's only remaining mention is the harness `CLAUDE.md`, which
  is a symlink to a file base cannot change.
- **Suffix wording.** `.env.local`, over `.env.site` / `.env.override`.
  It matches the Next.js precedent this rule is otherwise aligned with,
  and -- more decisive here -- it matches `.setup.conf.local`, which
  already means exactly this in this repo. A second word for one concept
  is a second thing to learn.

### Migration

Every downstream repo has a hand-written, gitignored, unrecoverable `.env`
under the old rule. `_migrate_env_to_local` renames it to `.env.local`
before anything can regenerate, gated on the file's own content (an
auto-gen marker, or no assignment line at all, means there is nothing of
the user's to move) so it fires once and is inert after.

It is called from `init.sh`, not from `upgrade.sh`, and that is the
load-bearing detail: an upgrade is driven by the consumer's OWN vendored
`upgrade.sh`, which shipped in an older release and cannot be changed
retroactively, so a migration added to `upgrade.sh` would first run one
release too late -- after the rename had already taken effect. Every
release's `upgrade.sh` re-runs the freshly pulled `init.sh` as its resync
step, which makes that the earliest point in the upgrade running current
code, and nothing between there and the user's next `just setup` writes
`.env`.


## ---- FILE: doc/adr/00000004-test-category-tool-subdir-layout.md ----

# `test/<category>/<tool>/` subdir layout for multi-tool repos

> Serves: PRD invariant 7 (rigorous test bar) -- test layout; superseded
> by ADR-00000012 (tool-first).

- **Date:** 2026-06-05
- **Status:** Superseded by ADR-00000012

> **Superseded (2026-06-23, ADR-00000012).** The category-first layout
> decided here was reversed to
> **tool-first** (`test/<tool>/<category>/`) in ADR-00000012, to align the
> test tree with the per-tool driver model introduced by ADR-00000011 §5.
> The context and trade-offs below remain accurate; only the chosen
> direction changed.

## Context

`base` itself is single-tool: every test under `test/` is a `.bats`
file, so `test/<category>/` (`smoke` / `unit` / `integration` /
`behavioural`) is unambiguous. But downstream repos that consume `base`
are increasingly multi-tool. Concrete example: `ycpss91255-docker/isaac`
keeps `.bats` smoke tests alongside Python entrypoints, so a
`test/smoke/test_foo.py` lands next to `test/smoke/*.bats`. Both a
`bats` runner and a `pytest` runner then see the same directory and
must pattern-filter to avoid collecting each other's files.

This bit real CI: `ycpss91255/isaac` PR #46 and
`ycpss91255-docker/isaac` PR #63 hit `pytest` collecting 0 tests from a
directory full of `.bats` -> exit 5 -> CI red, even though the workflow
had a skip-empty branch. Skip-checks that use `[ -d test/smoke ]` as
"do we have tests" become wrong the moment a second tool's files mix in.

There was no written convention for where a second tool's tests should
live, so each repo improvised.

## Decision

When a `test/<category>/` directory holds tests from **more than one**
tool/language, segregate by a `<tool>` subdirectory:

```
test/
├── unit/
│   ├── bats/        # *.bats
│   ├── pytest/      # test_*.py
│   └── gtest/       # *_test.cpp
├── smoke/
│   ├── bats/
│   └── pytest/
└── integration/
    └── ...
```

- **Category-first** (`test/unit/pytest/`, not `test/pytest/unit/`):
  keeps the TDD four-axis view (smoke / unit / integration / lint)
  intact so "what unit tests do we have" stays a single directory walk
  and `TEST.md` can organise by category without splitting across tools.
- **Single-tool repos stay flat.** `base` and any pure-bats / pure-pytest
  consumer do not migrate -- `test/unit/*_spec.bats` is fine. The
  sublayer is opt-in, appearing only when ambiguity does.

## Alternatives

- **Tool-first (`test/pytest/unit/`).** Rejected: fragments the
  category axis across tools, so the smoke/unit/integration view (and
  `TEST.md`) has to be reassembled per tool.
- **Flat with pattern-only filtering** (`test/unit/test_*.py` mixed with
  `test/unit/*_spec.bats`). Rejected: pushes tool-pattern knowledge into
  CI YAML skip-checks (`find test -name 'test_*.py' -print -quit`),
  which is easy to get wrong -- this is exactly the failure that
  prompted the convention.
- **Forcing the sublayer on single-tool repos.** Rejected: adds a layer
  of depth with zero benefit for `base` and other shell-only consumers.

## Consequences

- Downstream multi-tool repos have a documented target to migrate to;
  reference adoptions: `ycpss91255-docker/isaac#64`,
  `ycpss91255/isaac#38`/`#39`/`#40`/`#41`.
- `base` itself needs no layout migration; `init.sh` / new-repo
  scaffolding is unchanged.
- If `base` later adopts a `TEST.md` schema shared across downstream, it
  should accept either the flat `test/<category>/` or the sublayered
  `test/<category>/<tool>/` shape.
- An optional lint/hook to warn when a `test/<category>/` mixes runner
  file extensions is tracked separately as a backlog item (#495); it is
  not part of this convention.
- Out of scope: cross-tool shared fixtures (`test/_helpers/`),
  cross-tool coverage merging, and IDE discovery hints
  (`pyproject.toml`'s `[tool.pytest.ini_options].testpaths` handles the
  last per-repo). Defer until needed.


## ---- FILE: doc/adr/00000005-adopt-just-over-makefile.md ----

# Adopt `just` over the Makefile wrapper

> Serves: PRD invariant 6 (base is a subtree; downstream a thin caller)
> -- `just` as the single user-facing entry; mechanism.

- **Date:** 2026-06-08
- **Status:** Accepted

## Amendment (#573, 2026-06-12): `Makefile.ci` also retired

The original decision (below) scoped `Makefile.ci` **out** (per #475):
the base-only CI lint/test wrapper would stay on make because its argv
surface does not hit make's restrictions. That left the repo carrying
**two runners** (make for the CI gate, just for everything else) doing
work at the same level -- redundant tooling whose only effect was a
second dependency to install and keep in sync.

This amendment reverses that scope. `Makefile.ci` is retired for a
base-local `justfile.ci`, invoked as `just ci <recipe>`
(`just` does not auto-discover a `justfile.ci`, so it never collides
with the auto-discovered container-ops `justfile`). The two files stay
deliberately separate -- `justfile.ci` is the template dev / self-test
entry, `script/docker/justfile` is the consumer entry -- because they
assume different repo layouts. make is removed from `ci.sh` and the
test-tools image (the integration tests had already moved to
`just upgrade-check` in #546, so the make install was dead weight).

The "Open questions" and "Consequences" entries for `Makefile.ci` below
are superseded by this amendment.

## Context

RFC #330 introduced `script/docker/Makefile` as a single, discoverable
entry point: thin wrappers (`make build` / `make run` / `make exec` /
...) that forward 1:1 to `./script/*.sh`. The goal was discoverability
(`make help`) and one muscle-memory verb per operation.

The wrapper has not held that line. GNU make's argv handling collides
with the docker-native syntax the wrappers are supposed to expose, and
every new arg pattern that lands forces the Makefile to invent another
escape hatch:

- #414 -- `_check_overrides` inspects `MAKEOVERRIDES` to abort on
  `VAR=VALUE` tokens, because make silently swallows them otherwise.
- #448 -- a mandatory `--` separator before flags, because `--target`
  and friends collide with the wrapper's own `-t/--target`.
- #469 -- an `EXEC_ARGS` env-var passthrough, because `=`-bearing
  tokens get caught by `MAKEOVERRIDES`.

Each hole patched begets the next: a new docker-native token hits
another make-level restriction, the wrapper drifts further from the
docker CLI it is meant to mirror, and users now have to remember which
case takes which escape hatch. The Makefile no longer reads as "thin
forwarder" -- a new reader cannot tell at a glance why it is this
complex.

This was raised right after #469 shipped, while the pain is fresh: the
wrapper's usage keeps getting further from how docker itself works.
The unwind cost is still low (we have not extended into more wrappers
or a third-party runner yet), and all 13 downstream repos symlink this
one Makefile, so any breaking change requires a batch fanout -- the
earlier we decide, the cheaper.

The triggering issue (#475) only captured the decision and the
alternative landscape; it did not pick a direction. This ADR records
the chosen direction and its rationale. The implementation is tracked
in follow-up issues.

## Decision

**Adopt `just` (a `justfile`) as the user-facing entry point**, in
place of the GNU make wrapper.

The root cause is GNU make treating `VAR=VALUE` tokens as variable
overrides and consuming `--`/`-flag` argv for itself. `just` does not:
recipe arguments and trailing arguments pass through cleanly to the
underlying `./script/*.sh`, so the #414 / #448 / #469 workarounds
disappear rather than accreting further. A recipe like

```just
run *args:
    ./script/docker/run.sh {{args}}
```

forwards `just run -t headless --gpus all` verbatim -- no
`MAKEOVERRIDES` guard, no mandatory `--` separator, no `EXEC_ARGS`
shim.

**Rollout is additive first, retirement second**, split so the
breaking change is deliberate:

1. **Additive `justfile` introduction.** Land the `justfile` in
   `base` alongside the existing Makefile. Both work; users and CI can
   migrate on their own schedule. No downstream break.
2. **Makefile retirement + downstream fanout.** Once the `justfile` is
   proven, remove the Makefile wrapper and roll the removal to all 13
   downstream repos via the batch base-tag fanout. The retirement is
   *bound to* that fanout -- it does not ship until the migration path
   is wired -- because the Makefile is symlinked, not copied, so a
   `base` removal would otherwise break every downstream simultaneously.

**External dependency is accepted.** `just` is a third-party runner
that downstream users must install. It is bundled into the CI images,
so the gated path (CI, the docker_harness self-test loop) carries it
without per-user action. For interactive dev hosts, installation is a
one-line documented step. The smaller community vs. make is judged an
acceptable cost against make's structural argv mismatch.

## Open questions (resolved)

- **Is "single entry point" a hard requirement?** Nice-to-have, not
  hard. `just` happens to preserve it (one verb per op, same as
  `make`), but the decision did not hinge on it -- if it had been a
  hard requirement it would only have ruled out option A
  (raw scripts), and `just` keeps the single-entry property regardless.
- **What replaces `make help` discoverability?** `just --list`, which
  enumerates recipes with their doc comments natively -- no
  hand-maintained `help` target.
- **How do the 13 downstream repos migrate?** Via the batch base-tag
  fanout (`/batch-base-upgrade` + `/batch-pr`), bound to the
  Makefile-retirement step above; not a per-repo deprecation grace
  period.
- **Are there `make build` / `make test` callsites in CI / GHA?** Yes,
  assumed -- a grep-and-update sweep across `.github/workflows/` (and
  any helper scripts) is part of the retirement step.
- **Do IDE / editor task configs hardcode `make`?** Where present
  (`.vscode/tasks.json` etc.), they are caught by the same
  grep-and-update sweep and re-pointed at `just`.
- **`Makefile.ci`?** Out of scope (per #475). It is a dev-loop / CI
  lint+test wrapper, not a user-facing container-ops wrapper, and its
  argv surface does not hit the same make restrictions. *(Superseded by
  the 2026-06-12 amendment above: `Makefile.ci` is retired for
  `justfile.ci`.)*

## Alternatives

- **A -- retire to raw `./script/*.sh` directly** (`./build.sh test`,
  `./run.sh -t headless`). Most docker-native and lowest ongoing
  maintenance, and it sidesteps make's argv problem entirely. Rejected
  because it drops the single discoverable entry point and the
  `make help`-style listing, and forces every user to re-learn paths
  and per-script flags. The discoverability win of a runner verb was
  judged worth one external dependency.
- **B -- custom single-dispatcher CLI** (`./bs build`, `./bs run -t
  headless`): one binary that routes to the wrappers with full argv
  control. Keeps single-entry + discoverability and solves the argv
  problem. Rejected because it reinvents exactly the recipe-runner
  parts that `just` already provides as a tested, documented tool --
  new surface to build and maintain, with fresh implementation-bug
  risk, for no capability `just` lacks.
- **D -- keep the Makefile, keep patching.** Cheapest short-term, zero
  migration. Rejected because it is the status quo whose cost this ADR
  exists to stop: every workaround is mental tax, the divergence from
  the docker CLI keeps widening, and each patched hole begets the next.
  The accumulated #414 / #448 / #469 pattern is the evidence that this
  does not converge.

## Consequences

- The #414 / #448 / #469 workarounds are retired with the Makefile, not
  carried forward: clean recipe + trailing-args passthrough replaces
  the `MAKEOVERRIDES` guard, the mandatory `--` separator, and the
  `EXEC_ARGS` shim. (Per #475 these are removed *with* the wrapper, not
  reverted in isolation.)
- An external dependency (`just`) enters the dev-host toolchain. CI
  images bundle it; interactive hosts install it via a documented
  one-liner.
- `make help` is replaced by `just --list` (recipe doc comments),
  removing the hand-maintained help target.
- Two-phase rollout, tracked as two follow-up implementation issues:
  (1) additive `justfile` introduction in `base`; (2) Makefile
  retirement + 13-repo batch fanout. The retirement is gated on the
  fanout because downstream repos symlink the Makefile.
- A grep-and-update sweep is required across CI / GHA workflows and IDE
  task configs (`.vscode/tasks.json` etc.) to re-point `make` callsites
  at `just`.
- Doc churn: README + `README.zh-TW.md` + CHANGELOG across `base` and
  downstream, plus user muscle memory (`make X` -> `just X`).
- `Makefile.ci` is unaffected (out of scope); the CI lint/test entry
  stays on make. *(Superseded by the 2026-06-12 amendment: retired for
  `justfile.ci`; make is fully removed.)*



## ---- FILE: doc/adr/00000006-upgrade-sh-path-contract.md ----

# upgrade.sh hard-coded paths are a protocol-stable contract

> Serves: PRD invariant 6 (base is a subtree; downstream a thin caller)
> -- the upgrade.sh frozen-path contract; mechanism.

- **Date:** 2026-06-08
- **Status:** Accepted
- **Amended:** 2026-06-24 by #654 / ADR-00000011 §8 -- Region A's frozen
  `.base/init.sh` root path is superseded. `init.sh` and `upgrade.sh` now
  live deep at `.base/dist/script/base/` and self-locate the subtree
  root via a walk-up (see the Region A note below); the lockstep discipline
  this ADR mandates is what governed that move.
- **Amended:** 2026-06-26 by #714 -- the shipped-tree directory was renamed
  `downstream/` -> `dist/`, so every frozen interior path moves from
  `.base/downstream/...` to `.base/dist/...` (this supersedes the
  `.base/downstream/` contract introduced by #625 / #654). The rename was a
  lockstep change exactly as this ADR mandates: `upgrade.sh` /
  `init.sh`'s subtree-root marker check, the Region B config-drift paths
  (`${TEMPLATE_REL}/dist/config[/docker/setup.conf]`), the Region A Step-3
  `init.sh` call, and the Region C `dockerfile_migrate` lib all moved in the
  same change. **Consumer migration:** an existing consumer on
  `.base/downstream/` that upgrades gets `.base/dist/` after the subtree
  pull, leaving its repo-level wrapper symlinks
  (`script/build.sh -> .base/downstream/...`) dangling; the upgrade->init
  resync heals them because `init.sh`'s `_symlink` helper `rm -f`s the stale
  link and re-`ln -sf`s it at `.base/dist/...` (so stale `.base/downstream/`
  symlinks are dropped and re-pointed). `dockerfile_migrate` migration 4 was
  widened to match `(downstream/|dist/)?` so a consumer Dockerfile on either
  historical path heals to the `dist/` target.
- **Amended:** 2026-07-15 by #831 -- `setup.conf` is `just setup`-managed,
  not hand-edited, so it left the hand-editable `config/` surface: the
  per-repo override moved from `<repo>/config/docker/setup.conf` to the
  repo-root dotfile `<repo>/.setup.conf`, and the template default from
  `${TEMPLATE_REL}/dist/config/docker/setup.conf` to
  `${TEMPLATE_REL}/dist/.setup.conf`. Per this ADR's discipline the move
  was lockstep: Region B's `_warn_setup_conf_drift` blob-hash path
  re-points to `dist/.setup.conf`, and a new `_migrate_legacy_setup_conf`
  step `git mv`s a legacy override to the root and warns loudly (never
  silently drops it). (Superseded in part by the 2026-09-06 amendment
  below: that step could not reach the downstreams it was written for from
  `upgrade.sh`, and now runs from the `init.sh` resync.) See the
  re-pointed frozen-path list note below.
  This reverses #262, which had nested setup.conf under `config/docker/`
  for layout uniformity.
- **Amended:** 2026-08-25 by #915 -- the 2026-06-24 amendment above was
  wrong on one point, and a consumer paid for it. It records that Region
  A's `init.sh` call "moved in the same change" as the file, which is
  true of THIS repo's copy and irrelevant to the failure: the copy of
  `upgrade.sh` that drives an upgrade is the CONSUMER'S, vendored at
  their current release, and it cannot be updated in lockstep with
  anything because it has already shipped. Every release up to
  `v0.41.0` still names `./${TEMPLATE_REL}/init.sh`, so on the first
  upgrade into a `dist/`-era tree step 3 died with exit 127 -- after
  the pull had committed -- leaving the repo claiming `v0.42.0` with a
  clean `git status` and every wrapper dangling. **The correction to the
  contract:** lockstep is necessary but NOT sufficient for any path an
  ALREADY-RELEASED caller names. Such a path must keep a forwarder at
  the old location for as long as a release that names it is supported.
  A repo-root `init.sh` now forwards to `dist/script/base/init.sh`; it
  is three lines with no logic of its own, so it cannot drift from the
  implementation, and it restores one name rather than the flat layout.
  The regression guard is behavioural rather than remembered:
  `test/bats/integration/prev_release_upgrade_spec.bats` runs the real
  released `upgrade.sh` against the current tree, so the next move of a
  frozen path fails in CI instead of at a consumer's terminal.
- **Amended:** 2026-09-04 by #1036 -- the correction above covers a path an
  already-released caller NAMES. The same asymmetry applies one step
  further, to work an already-released caller DOES. Every released
  `upgrade.sh` stages the migrated files at its own Step 5 by hardcoded
  filename, and v0.41.0's reaches the Dockerfile only down a branch the
  current migration list never takes -- so a cross-version upgrade committed
  the workflow `@tag` bump and the `.gitignore` sync, left the Dockerfile
  the Step-3 resync had just rewritten unstaged, and closed by telling the
  user to `git push`. As with the path, no edit to `upgrade.sh` reaches a
  consumer already sitting on v0.41.0 / v0.42.0. **The addition to the
  contract:** work whose result the CALLER has to commit belongs on the new
  tree's side of the boundary, staged where it is performed. Region A's
  Step-3 `init.sh` now stages what the resync wrote. The caller's Step 5
  stays harmless: the migrations are idempotent and `git add` of an
  already-staged path is a no-op.
- **Amended again:** 2026-09-05 by #1036, before the fix shipped. The
  paragraph above scoped the staging to the migration record
  (`migrated_files` in `dist/script/docker/lib/dockerfile_migrate.sh`) and
  argued that a list of filenames was the wrong shape because it decays the
  first time the work touches one more file. **That argument was right about
  the migrations and wrong about the resync.** The Dockerfile is not the
  only thing Step 3 writes: the same run re-points the wrapper symlinks,
  lands the justfile layering and the monitor workflow, and DELETES the
  pre-relocation root wrappers. Staging only the migration record left every
  one of those out, so the commit still described a tree on a different
  layout -- the defect this amendment was written to close, one file over.
  Two of the three things now staged are therefore lists of names, and the
  reason that is not the decay the earlier paragraph rejected is that
  neither is hand-kept against nothing: `_init_installed_paths` is diffed
  against a REAL resync in both directions by
  `test/bats/integration/init_installed_paths_spec.bats`, so a file added to
  the resync and not to the list fails CI; `_init_retired_root_paths`
  enumerates a closed historical set -- names that already stopped existing
  -- and is the single definition the resync deletes from, restores from and
  stages the deletion of, so it cannot come apart from itself. What stays
  forbidden is the shape the earlier paragraph was really aimed at: a sweep.
  `git add -A` over the tree would commit whatever the user happened to be
  editing, and every path staged here is base's own by the repo's naming
  contract -- shipped or generated, replaced on update, never hand-edited
  per instance -- so none of it is the user's work to review.
- **Amended a third time:** 2026-09-05 by #1036, again before the fix
  shipped. The last sentence above was false as written. The naming
  contract makes those paths base's to SHIP; it does not make them base's
  to REWRITE, and `_init_installed_paths` answers "what does a consumer
  carry", not "what did this run write". EIGHT of the paths behind that
  list are written only under a condition and otherwise left exactly as
  they were found -- the 14 hook stubs (whose entire purpose is that a
  user-authored hook survives every later upgrade), the REPO-OWNED
  `script/local/` pair, `config/.gitkeep`, the monitor workflow, a
  `.hadolint.yaml` the user has customised, `.gitignore` and
  `.dockerignore` (the sync APPENDS only the canonical entries a file is
  missing and returns without a write when none is -- "the common case for
  an up-to-date repo" -- and never touches the hand-maintained region above
  the managed block at all), and `.setup.conf`, which `setup.sh` writes
  only on a first-time bootstrap or a stale-`mount_1` rewrite. Staging the
  published list wholesale therefore committed
  the user's own half-finished hook under a message about a base release:
  the sweep the paragraph above forbids, arriving through the published
  list instead of through `git add -A`. **The correction:** the staged set
  is what THIS RUN WROTE. `_init_conditional_paths` names that subset and
  every write of one is recorded as it happens (`_INIT_WROTE`), because the
  condition it tested is gone by the time the staging step runs and
  re-deriving it from the tree is how the user's content gets classified as
  ours a second time. Three entries cannot be recorded by the writer
  itself: `.setup.conf`, whose writer is a separate process that no shell
  variable crosses, and the two ignore files, which three separate syncs
  write and none of which is asked "did anything change" -- for all three
  the file's CONTENT across the pass answers it instead, in `_call_setup`
  and `_sync_existing_gitignore` respectively. A spec pins the two lists to
  each other, and the integration arm now hands the real upgrade a
  customised hook stub -- a path inside the published list, which the
  earlier anti-sweep arms (both on `NOTES.md`, outside it) could not see.

  This paragraph first said SIX and named neither ignore file. The
  enumeration was drawn from the writers that seed a file when it is
  ABSENT, and the ignore sync does not look like one of those -- it runs on
  every resync and rewrites nothing only because it finds nothing missing.
  That is the same predicate wearing different clothes, which is why the
  list is now called conditional rather than seed-only: "seeded once" was
  a promise about `.gitignore` and `.setup.conf` that was not true, and the
  predicate the staging step needs is the weaker one.
- **Amended a fourth time:** 2026-09-05 by #1036, still before the fix
  shipped, on the two halves the correction above left standing. First,
  the same defect one list over: `_init_retired_root_paths` was staged by
  NAME, and the resync deletes one of those names only where it is a
  SYMLINK -- the `[[ -L ]]` guard is what makes the migration idempotent
  and silent on a fork that never carried the name. So the list enumerates
  what a run MAY delete, and a consumer's own hand-written `Makefile` or
  `run.sh` at the root went into the release commit with whatever they had
  uncommitted in it. It is now recorded where the removal happens, like
  every other conditional write; the index lookup stays, because it is what
  keeps a name this repo never tracked out of a pathspec that would fail
  the whole batch. Second, WHOSE index: the staging step asked `rev-parse
  --is-inside-work-tree`, which answers "is REPO_ROOT inside ANY work
  tree". On the input the function's own docstring is written for -- a repo
  bootstrapped by hand, which may not be a git repo at all -- sitting
  anywhere inside another repository's checkout, that resolved to proceed
  and wrote the entire resync into a third-party index, then reported how
  many paths it had staged. `--show-toplevel` compared against REPO_ROOT is
  the other half of the property `_init_drop_foreign_paths` already
  guarantees: that fence keeps a path outside REPO_ROOT out of `git add`,
  this one keeps `git add` inside REPO_ROOT's own repo. Both corrections
  are the same rule the amendment above states and neither followed all the
  way: the staged set is what THIS RUN WROTE, into THIS repo.
- **Amended:** 2026-09-06 by #1077 -- the 2026-08-25 correction was
  applied to ONE of two sibling paths. It says a path an already-released
  caller names must keep a forwarder at the old location for as long as a
  release that names it is supported, and the `dist/` reorganisation moved
  `init.sh` and `upgrade.sh` together. `init.sh` got the forwarder because
  a released `upgrade.sh` EXECS it and the failure was in front of us;
  `.base/upgrade.sh` got none, and it is named by the callers no code
  change can reach at all -- the person at the terminal following the
  README and the usage text their own vendored copy prints, this repo's
  `enforce_wrapper_first_upgrade.sh` hook, and any downstream runbook
  written in that window. The result was worse-shaped than the v0.42.0
  one: the upgrade REMOVED THE COMMAND THAT PERFORMED IT. The first
  `./.base/upgrade.sh vX.Y.Z` succeeded and the second exited 127, one
  release later, against a repo that was otherwise healthy -- so no run of
  the upgrade could report it. **Nothing in the contract changes**; a
  repo-root `upgrade.sh` forwarder now stands beside `init.sh`, on the
  same three-line no-logic shape.

  The half that does change is the regression guard this ADR named in
  2026-08-25. `prev_release_upgrade_spec.bats` drove the real released
  `upgrade.sh` against the current tree throughout, green, because every
  arm in it asked whether ONE upgrade succeeds and answered it about the
  tree the upgrade STARTED from. A frozen path missing from the tree the
  upgrade PRODUCES is outside what any of them can see: exit status,
  `.version`, dangling symlinks and the Dockerfile's COPY sources are all
  satisfied by a tree nobody asks to upgrade again. So the guard is now
  "upgrade twice" -- run the released driver, then re-run THE SAME COMMAND
  STRING on the tree it produced. Re-resolving the entry point instead
  would ask whether the new tree has SOME upgrade script, which the broken
  tree also answers yes to. It names no file, deliberately: a roster of
  paths that must exist goes stale the day a third frozen path appears,
  and "the tree an upgrade produces can be upgraded from" covers that one
  without an edit.
- **Amended:** 2026-09-06 by #1086 -- the asymmetry a third time, on the
  MIGRATIONS themselves. 2026-08-25 covered a path an already-released
  caller names; 2026-09-04 covered work whose result it has to commit;
  this covers work it has to PERFORM. `_migrate_legacy_setup_conf` was
  added by the 2026-07-15 amendment above, in `upgrade.sh`, so that the
  relocation of a per-repo `setup.conf` out of `config/` would never
  silently drop a downstream's override. It ran in the one script the
  affected downstream never executes: the population still carrying the
  old path is exactly the population on `v0.41.0` or earlier, and their
  vendored driver has never heard of the migration. So the upgrade exited
  0, every gate stayed green, and the repo came out running on the
  template defaults -- named after the directory it was cloned into, with
  an empty `[environment]`. It also disarmed itself, because the hop it
  missed seeds a default `.setup.conf`, and the next upgrade -- which does
  carry the migration -- then saw BOTH files and declined to act.
  **The addition to the contract:** a migration ACROSS a base layout
  change belongs in `init.sh`, never in `upgrade.sh`. `upgrade.sh` may
  only hold a rewrite whose discriminator is the PRE-PULL vendored tree
  (`_migrate_lifecycle_restart_default` is the one such case), because
  that is the one thing Step 3 can no longer see. Everything else runs
  from the resync, which is also the only thing a repo that RE-ESTABLISHES
  its subtree ever runs -- a path `upgrade.sh` cannot reach at all.

  The BOTH-files case stops being a warning at the same time, and merges
  per SECTION: a root section byte-identical to the shipped template's
  says, under the chain's section-replace rule, exactly what leaving it
  out says, so it was never a choice and the legacy file's wins; anything
  else is the user's, both files are kept, and the message names the
  sections. Refusing was the alternative and it is not available here:
  neither `v0.41.0`'s nor `v0.42.0`'s `upgrade.sh` arms an EXIT trap, and
  their one rollback hangs off the Step 2 integrity check, so a non-zero
  exit at Step 3 leaves the subtree pull committed and the wrappers
  restored to a layout the pull deleted -- #1077's shape, with the config
  file kept as a souvenir.

  The guard is behavioural and it is a NEW QUESTION, not a new path:
  `prev_release_upgrade_spec.bats` now asks whether the upgraded consumer
  still carries its own configuration, having only ever asked whether it
  works. Measured on the unfixed tree, the oldest driver's arm fails with
  `IMAGE_NAME=consumer` -- the fixture's directory name -- while every
  other arm stays green.

## Context

`upgrade.sh` runs entirely from the downstream repo root and drives the
`.base/` subtree forward to a target tag. Most of its filesystem
references are derived from a single `TEMPLATE_REL` anchor (the basename
of the directory the script lives in, today `.base`), so renaming the
subtree prefix itself stays cheap. But three regions reach *into* the
subtree at hard-coded sub-paths that `TEMPLATE_REL` does not abstract
away. #477 already hit this wall once: `_verify_subtree_intact` asserted
specific files at fixed paths and broke on the v0.39.0
`script/docker/setup.sh` -> `wrapper/setup.sh` reorg; it was fixed with a
structural invariant (subtree dir non-empty + well-formed `.version` +
target-version match) that no longer names interior paths.

The #477 audit surfaced three *sibling* path-coupling regions in the same
file that were deliberately left out of the structural-invariant fix and
recorded as backlog in #492. Each would hit the same wall on the next
reorg that touches its paths:

- **Region A -- direct `init.sh` invocation.** `_main` Step 3 calls
  `"./${TEMPLATE_REL}/init.sh"` for the symlink / `.gitignore` resync,
  and the `--gen-conf` branch delegates to
  `"./${TEMPLATE_REL}/init.sh" --gen-conf`. If `init.sh` is renamed or
  relocated, Step 3 fails with `No such file or directory` *after* the
  subtree pull has already landed, and the pull is **not rolled back**
  (the rollback path only fires from `_verify_subtree_intact` in Step 2).
  The repo is left half-upgraded: subtree pulled, but symlinks /
  `main.yaml` `@tag` / `.gitignore` not resynced.

  > **Amended 2026-06-24 (#654, ADR-00000011 §8).** `init.sh` was
  > relocated out of the subtree root to
  > `.base/dist/script/base/init.sh` (with `upgrade.sh` alongside).
  > Per this ADR's lockstep discipline the move was done in one slice that
  > also updated Step 3's call to
  > `"./${TEMPLATE_REL}/dist/script/base/init.sh"` (both the resync
  > and `--gen-conf` invocations). Critically, `upgrade.sh` no longer
  > derives `TEMPLATE_REL` from its own directory's basename (which is now
  > `base`, the wrong prefix): it **walks up** from its location to the
  > subtree root -- the dir carrying the `.version` + `dist/` markers
  > -- and `basename`s THAT (`.base`), so the `git subtree pull --prefix=`
  > flag and every interior path stay correct regardless of nesting depth.
  > The new self-location walk-up IS the contract that replaces the frozen
  > `.base/init.sh` root path; an integration test asserts the resolved
  > `--prefix` is the subtree basename, not `base`.

- **Region B -- `config/` drift detection.** The pre-pull snapshot
  (`HEAD:${TEMPLATE_REL}/config` and
  `HEAD:${TEMPLATE_REL}/config/docker/setup.conf`) and the post-pull
  `_warn_config_drift` / `_warn_setup_conf_drift` family compare tree /
  blob hashes at those fixed paths. If `config/` or
  `config/docker/setup.conf` moves, `git rev-parse --verify` returns
  nothing, so the entire drift-warning module silently no-ops (or, if
  only one side moves, emits false positives). The user loses the
  "upstream baseline changed -- reconcile your override" signal with no
  error -- the most dangerous failure mode, because it is silent.

- **Region C -- Dockerfile lint-stage auto-patch.** Step 5 (and the
  sibling #399 wrapper-copy patch) `grep` + `sed` the downstream
  `Dockerfile` to inject `COPY .base/script/docker/lib /lint/lib` and to
  rewrite `COPY *.sh /lint/` -> `COPY script/*.sh /lint/`, healing the
  #284 `lib/` split and the #330 wrapper consolidation. These hard-code
  `.base/script/docker/lib/` and the `script/docker/*.sh` umbrella-loader
  location. If `lib/` is relocated or the umbrella loaders move, the
  sed-generated `COPY` points at a wrong source and the downstream build
  stage fails with `COPY source not found`.

#492 chose to defer the *fix* (no path has an active relocation plan) and
to label it `backlog`, with a trigger checklist requiring any future
reorg of these paths to cross-reference the issue. #492's own body lists
three future-direction options -- ADR-frozen contract, a path-manifest
file, or `find`/glob discovery -- and notes that if the ADR route is
taken, the issue can be closed with a link to it. This ADR is that route.

## Decision

Declare the following `.base/` interior paths **protocol-stable**: they
are part of the contract `upgrade.sh` depends on, and **must not be moved
or renamed without updating `upgrade.sh` in the same change** (and
re-checking #492's trigger checklist):

- `.base/init.sh` -- invoked directly by Region A. *(Superseded
  2026-06-24 by #654: now `.base/dist/script/base/init.sh`, located
  via `upgrade.sh`'s walk-up to the subtree root rather than frozen at the
  root; see the Region A amendment above.)*
- `.base/config/` and `.base/config/docker/setup.conf` -- hashed by
  Region B's drift detection. *(Re-pointed 2026-07-15 by #831: the
  setup.conf blob is now `.base/dist/.setup.conf` (template default) with
  the downstream override at the repo-root `<repo>/.setup.conf`; the
  `.base/dist/config/` tree hash still guards the hand-editable shell
  config. #714 first moved these under `dist/`.)*
- `.base/script/docker/lib/` and the `.base/script/docker/*.sh` umbrella
  loaders -- targeted by Region C's Dockerfile auto-patch.

"Protocol-stable" means: these are not free-to-refactor implementation
details. A reorg may still move them, but only as a deliberate,
`upgrade.sh`-aware change -- the same discipline `TEMPLATE_REL` already
gives the subtree prefix, extended by convention to these interior paths.
The break consequences recorded per region above are the contract's
teeth: A leaves a half-upgraded repo with no rollback, B fails silently,
C breaks the next downstream build.

This closes #492: the issue's "if a future decision freezes these paths
as permanent contract (e.g. via an ADR), this issue can be closed and
replaced with a link to that ADR" condition is now met.

## Alternatives

- **Path-manifest file** (`.base/.path-manifest.txt` listing the actual
  paths; `upgrade.sh` reads from it). Same shape as the R2 design floated
  in the #477 grill, but for path discovery rather than integrity. It
  would let paths move by editing one declarative file -- but it adds a
  new artifact that must itself be kept in sync, ships in every subtree
  pull, and introduces a parse/validation surface. Rejected: it trades a
  remembered convention for a new moving part, for paths that have no
  relocation pressure.
- **`find` / glob discovery** (locate `init.sh` / `config/setup.conf` /
  `lib/` dynamically within `.base/`). Removes the path dependency
  entirely, but makes `upgrade.sh` guess intent: a glob that matches two
  candidates, or zero, has to decide what to do at the worst possible
  moment (mid-upgrade, post-pull). It also masks accidental moves instead
  of surfacing them, which is the opposite of what the silent-failure
  Region B needs. Rejected as over-engineering for a non-problem.
- **Do nothing beyond the #492 backlog note.** Leaves the contract
  implicit -- discoverable only by reading `upgrade.sh` or stumbling onto
  the issue. Rejected: the contract is load-bearing across every
  downstream upgrade and deserves a durable, linkable home.

## Consequences

- The convention must be *remembered*. This ADR plus #492's trigger
  checklist are the memory: any reorg touching the frozen paths is
  expected to cross-reference both and update `upgrade.sh` in lockstep.
  This is the accepted cost of choosing a frozen contract over a manifest
  or discovery -- no new code, no new file, no new parse surface, in
  exchange for a discipline a human (or agent) must hold.
- No code changes. `upgrade.sh` keeps its current hard-coded paths; this
  ADR ratifies them as intentional rather than incidental.
- The three break modes are now documented in one place, so a future
  maintainer who *does* need to move one of these paths knows exactly
  what to repair (Region A: add rollback or move the call; Region B:
  update both pre- and post-pull path pairs; Region C: update the
  grep+sed source paths) rather than rediscovering it from a failed
  upgrade.
- Complements the #477 `_verify_subtree_intact` R1+ structural invariant:
  #477 made the *integrity check* path-agnostic; this ADR freezes the
  *remaining* interior paths that could not be made path-agnostic without
  a manifest or discovery. The two together define the full path-coupling
  posture of `upgrade.sh`.
- #492 is closed with a link to this ADR. Future relocation pressure on
  any frozen path reopens the design question (manifest vs discovery) at
  that time, against a concrete need, rather than speculatively now.



## ---- FILE: doc/adr/00000007-log-tty-cache-and-transcript-layering.md ----

# Cache TTY-ness at startup so a transcript tee cannot re-flip single-sink dispatch

> Serves: mechanism -- wrapper log/transcript single-sink fidelity; no
> invariant.

- **Date:** 2026-06-18
- **Status:** Accepted

## Context

#438 made `log.sh` single-sink: one rendering per record, format chosen
by a live `test -t <fd>` in `_log_dispatch`'s auto branch (text on a TTY,
JSON when piped / redirected), with the same live probe gating colour in
`_log_color_enabled`.

#606 adds a wrapper transcript: a non-interactive verb's combined
stdout + stderr is tee'd to a plaintext log file under
`log/<verb>/<ts>-<traceid8>.log`. A tee inserts a pipe on fd1, so any log
call made *after* the tee is wired sees `test -t 1` = false and silently
flips the live terminal to JSON / no-colour mid-run -- the exact
regression this ADR prevents. The run's real interactivity is known once,
at startup, *before* the tee is layered.

## Decision

Resolve TTY-ness once at startup into `_LOG_IS_TTY` (a shell return code:
`0` = the run is interactive, non-zero = not) and have `log.sh` read it
via `_log_is_tty <fd>`. The auto-format branch and `_log_color_enabled`
consult `_log_is_tty` instead of probing the fd live. When `_LOG_IS_TTY`
is unset, `_log_is_tty` falls back to live `test -t <fd>` -- so sourcing
`log.sh` standalone (ci.sh, a bare `source`) is byte-identical to
pre-#605.

#605 ships only the read + fallback; #606 is the producer that sets
`_LOG_IS_TTY` before tee-ing. Explicit `LOG_FORMAT=text|json` still
short-circuits and never consults the cache.

## Layering: transcript tee over single-sink

The transcript is layered *above* single-sink, not a replacement.
Single-sink still decides format / stream from the cached startup
TTY-ness; the tee then duplicates whatever bytes single-sink emits into
the file. Because the format decision is frozen before the tee exists, an
interactive run keeps coloured text on the terminal *and* in the
transcript; a piped run keeps JSON on both. The transcript never triggers
a second render.

## Best-effort mixed format under LOG_FORMAT=json

If the operator forces `LOG_FORMAT=json` on an interactive run, the
terminal and the transcript both receive JSON (single render, no
dual-emit). We deliberately do **not** dual-render (human text to the
terminal, JSON to the file): that would double every log call, fork the
byte-stream the wrapper-dispatch specs pin, and re-introduce the
format-decision-per-sink coupling #438 removed. The transcript is
therefore a faithful copy of the single chosen rendering -- best-effort,
not a format-translating sink. (The transcript file can still end up
mixed-format in practice because it also captures raw docker child-process
output, which `log.sh` does not render; that is inherent to capturing a
child's stdout and is out of scope for dual-render to "fix".)

## Alternatives considered

- **Keep live `test -t` and special-case the tee.** Rejected: every
  future fd1 consumer (pagers, output captures) would re-hit the flip.
  The bug is the live probe, not the tee.
- **Dual-render text + JSON.** Rejected as above (byte-stream fork +
  double cost + re-coupling the per-sink format decision).
- **Snapshot the format string instead of TTY-ness.** Rejected: TTY-ness
  is the single root input both format and colour derive from; caching it
  keeps one source of truth and leaves explicit `LOG_FORMAT` overrides
  untouched.

## Consequences

- A producer that wants stable format / colour across a tee must set
  `_LOG_IS_TTY` *before* redirecting fd1 (#606 does this in the wrapper
  preamble).
- `_LOG_IS_TTY` is a return code (`0` / non-zero), **not** a `0|1` boolean
  string nor `true|false`: `_log_is_tty` does `return "${_LOG_IS_TTY}"`,
  so the producer must set it via `test -t 1; _LOG_IS_TTY=$?`. Documented
  at the helper and here because it is the single most likely integration
  mistake.
- Standalone `log.sh` users are unaffected (unset -> live fallback).
- Complements #438: #438 made format a per-run decision; this ADR makes
  that decision survive output-stream rewrapping.


## ---- FILE: doc/adr/00000008-coverage-sharded-pr-gate.md ----

# Shard kcov coverage + promote it to an enforced PR gate

> Serves: PRD invariant 7 (rigorous test bar) -- the coverage gate; a
> swappable mechanism, not the invariant.

- **Date:** 2026-06-24
- **Status:** Accepted
- **Amends:** #377 (which made coverage a non-gating, main-push-only
  metric)
- **Relates to:** #615, #613 (kcov env bugs fixed first so the gate is
  not flaky), ADR-00000004 / ADR-00000012 (test layout the shard
  partition walks)

## Context

#377 parallelised the normal test path (GNU `parallel --jobs N` inside
`_run_bats`; `bats-unit` split into a 1/N CI matrix) but left the
**coverage path fully serial**: a single
`kcov ... bats test/bats/unit/ test/bats/integration/` with no `--jobs`
and no matrix shard. The ~8-12 min coverage runtime was therefore
"serial x kcov" (kcov instruments every line and slows bats 2-5x), not
an inherent kcov floor.

#377 sidestepped that cost by making coverage **main-push-only** and
**explicitly non-gating** ("metric, not a gate"):

- `coverage` ran only on `push && ref == refs/heads/main`.
- It was deliberately kept out of `ci-rollup`'s `needs:`.
- Branch protection required only `ci-rollup`; the `codecov/project`
  status was not a required check; kcov never ran on PRs, so there was no
  PR coverage data to check.

Net effect: neither a coverage regression nor a kcov failure could block
any merge. #613 then found and fixed real kcov-env test bugs that had
been making the coverage job intermittently red — clearing the
precondition for letting coverage gate at all.

## Decision

### 1. Shard the kcov run across a CI matrix mirroring `bats-unit`

The `coverage` job becomes a `strategy.matrix` of kcov shards
(`shard: ['1/4', '2/4', '3/4', '4/4']`, `fail-fast: false`) that mirrors
the `bats-unit` matrix. Both matrices select their slice through one
shared primitive, `_shard_unit_files <n>/<total>` (round-robin over
`find test/bats/unit -name '*_spec.bats' | sort`), so coverage shard *k*
kcov's the **identical unit slice** the unit-test matrix runs. The 87
integration specs run on the **last shard only** (not every shard), so
no slice is kcov'd more than once.

Plumbing: a new `test.sh --coverage-shard N/T` flag sets coverage mode
and forwards `COVERAGE_SHARD` into the coverage container, where
`_run_coverage <n>/<total>` wraps kcov over that slice. Bare
`test.sh --coverage` (and `just test coverage`) keeps the full-suite path
for local / release use; `just test coverage 1/4` runs a single shard
locally. The coverage path also **skips the lint phase** unconditionally
(lint is measured by the dedicated lint jobs, so running it once per
coverage shard would be wasted work).

> Amendment (#686): the coverage container is no longer the upstream
> `kcov/kcov` Debian image — kcov is now source-built into the shared
> Alpine `test-tools` image, so the coverage matrix runs on the same
> pre-baked image as `bats-unit` (no per-shard apt-install). This is an
> environment change only; the sharded-matrix + `codecov/project` gate
> MECHANISM this ADR records is unchanged.

Per-shard wall-time lands in the `bats-unit` ballpark (~one shard,
~170s) and runs in parallel with `bats-unit`, so the added PR
critical-path cost is roughly one shard, not the old 8-12 min serial job.

### 2. Merge the shard reports via Codecov

Each shard uploads its partial report (`directory: ./coverage`) under a
distinct `flags: coverage-shard-<index>`. Codecov natively merges
multiple uploads for a commit ("Found N coverage files to report") into
one project coverage figure, so where a slice runs in the matrix does not
affect the merged total — only that every slice runs exactly once
(guaranteed by the exhaustive + disjoint round-robin partition).
`fail_ci_if_error: false` stays: an upload transport hiccup must not fail
a shard; the merge tolerates a missing shard and the *gate* is the
Codecov status, not the upload step.

### 3. Promote coverage to an enforced PR gate

- The `coverage` job now gates on
  `needs.classify.outputs.code_changed == 'true'` (the same output as the
  other PR-check jobs), so it **runs on PRs**, producing PR coverage
  data. The old `if: push && ref == refs/heads/main` is removed.
- `coverage` joins `ci-rollup`'s `needs:` (now 9 jobs), and the rollup
  verifier consumes `needs.coverage.result` with SKIPPED-as-pass for
  doc-only PRs. A **kcov test failure** therefore fails the matrix,
  fails `ci-rollup`, and blocks merge.
- A **coverage regression** is enforced via the `codecov/project` status
  configured in `.codecov.yaml` (`informational: false`), added as a
  required branch-protection check alongside `ci-rollup`.

### 4. Threshold choice

`.codecov.yaml`:

```yaml
coverage:
  status:
    project:
      default: { target: auto, threshold: 1%, informational: false }
    patch:
      default: { target: auto, threshold: 1%, informational: false }
```

- **project** `target: auto` compares against the PR base; `threshold:
  1%` absorbs kcov line-hit noise (the #613 fixes removed the spurious
  reds that previously plagued this path). `informational: false` makes
  the status fail on a real drop so branch protection can block.
- **patch** (new-code coverage) is decided explicitly as `target: auto`
  + `threshold: 1%` rather than a fixed percentage (e.g. 80%). The
  codebase has many intentionally-uncovered bash branches (`case ;;`
  arms, `/lint` fallback blocks, child-bash guards); a fixed patch target
  would make refactor PRs flaky — the exact #613-class brittleness this
  gate must avoid. `auto` keeps the patch status honest (new code should
  not be markedly less covered than the project) without false reds.

## Consequences

- A coverage regression or a kcov failure now blocks PR merge, raising
  merge confidence; this reverses #377's "coverage is a non-gating
  main-only metric" posture.
- GHA-minute cost rises: kcov now runs on every code-touching PR as a
  4-shard matrix instead of only on main push. Accepted — the per-shard
  wall-time is in the `bats-unit` ballpark and runs in parallel, so PR
  feedback latency barely moves while merge confidence improves.
- The coverage matrix and the unit matrix are now coupled through
  `_shard_unit_files`: changing one shard count without the other would
  desynchronise the slices. Documented in the helper; both default to 4.
- The gate's robustness depends on the #613 kcov-env fixes staying in
  place; if kcov flakiness returns, raise the project `threshold` before
  reverting the gate.

## Alternatives

- **Keep coverage main-only + non-gating (#377 status quo).** Rejected:
  it leaves coverage regressions and kcov breakage invisible until after
  merge; #613 already cleared the flakiness that justified the
  non-gating posture.
- **Single (un-sharded) coverage job on PRs.** Rejected: the 8-12 min
  serial kcov run would dominate PR wall-time, the cost #377 set out to
  avoid; sharding brings it down to ~one bats-unit shard.
- **A fixed patch target (e.g. 80%).** Rejected: the intentionally
  uncovered bash branches make a hard per-diff percentage flaky for
  refactor PRs; `target: auto` tracks the project rate instead.

## Amendment (#710): self-hosted, GitLab-portable gate; Codecov removed

- **Date:** 2026-06-25
- **Amendment status:** Accepted -- supersedes the Codecov merge +
  `codecov/project` status decided in sections 2 and 3 above.
- **Resolves:** #709 (`codecov/project` is Pro-only, so the project gate
  never worked on the free plan). **Relates:** #678 (no Codecov status to
  wire -- the gate moves into `ci-rollup` directly), #686, #677.

### Context

This repo is being imported into the company GitLab, where Codecov is
unavailable and uploading coverage to an external SaaS is data leakage.
Separately, #709 found `codecov/project` is a Pro-only status, so the
section-3 branch-protection gate never actually enforced anything on the
free plan. Both push the same way: drop Codecov entirely and enforce the
coverage floor locally, with a mechanism that ports to GitLab CI
unchanged.

### Decision

1. **Remove Codecov.** The `codecov/codecov-action` upload step, the
   `CODECOV_TOKEN` usage, the no-op `flags: coverage-shard-N`, and
   `.codecov.yaml` are deleted. No coverage data leaves CI.

2. **Self-hosted merge + floor gate.** kcov already writes a
   `cobertura.xml` per shard whose root `<coverage>` element carries
   `lines-covered` / `lines-valid`. A new CI-agnostic script,
   `script/test/drivers/coverage_gate.sh`, MERGES the per-shard reports
   into one project line-rate by SUMMING `covered` and `valid` across
   shards -- `SUM(covered) / SUM(valid)`, a line-weighted total -- and
   exits non-zero when it is below `COVERAGE_MIN`. It does NOT average the
   per-shard `line-rate` attributes: shards have different denominators
   (integration runs on the last shard only), so averaging would weight a
   small shard equally with a large one and report a wrong total. The
   script reads files and sets an exit code with no GitHub/GitLab
   coupling, so it gates identically under both.

3. **Threshold = v1 absolute floor.** `COVERAGE_MIN` defaults to **50**
   (percent, env-overridable), set just below the current measured
   project rate (~52.9%) so it does not false-fail today. It is meant to
   **ratchet up** as coverage improves. v2 (a follow-up, NOT built here)
   is regression-vs-main-baseline: store/fetch main's coverage % and fail
   on a drop beyond a threshold -- the original #615 intent. v1 keeps it
   simple with no baseline storage.

4. **Wired through `ci-rollup`.** Each coverage shard uploads its kcov
   report (HTML + cobertura) as a CI artifact (`actions/upload-artifact`,
   keyed by `strategy.job-index`). A new `coverage-gate` job downloads
   every shard artifact (`actions/download-artifact`, `pattern:
   coverage-shard-*`) and runs `coverage_gate.sh` over the merged set.
   `coverage-gate` joins `ci-rollup`'s `needs:` (which branch protection
   already requires), so a sub-floor rate blocks merge with **no
   branch-protection change** and no external SaaS.

5. **Visibility without SaaS.** kcov's HTML + cobertura are kept. On
   GitHub the gate appends a coverage summary table to
   `$GITHUB_STEP_SUMMARY` (built-in, free). Publishing the kcov HTML to
   GitHub Pages is a documented follow-up (deferred to keep this slice
   small).

### GitLab portability mapping (for the future move; mechanical)

The gate script stays CI-agnostic; only the job wrapper changes:

- **MR diff annotations:** point GitLab at kcov's cobertura via
  `artifacts: { reports: { coverage_report: { coverage_format:
  cobertura, path: coverage/**/cobertura.xml } } }`.
- **MR coverage % widget / badge:** add a `coverage:` regex on the
  coverage job, e.g. `coverage: '/merged line rate ([0-9.]+)%/'`, which
  matches the line `coverage_gate.sh` prints to stdout
  (`coverage_gate: merged line rate <N>% ...`).
- **The floor gate itself** is unchanged: GitLab runs the same
  `bash script/test/drivers/coverage_gate.sh coverage/**/cobertura.xml`;
  a non-zero exit fails the pipeline (the merge gate), exactly as the
  GitHub `coverage-gate` job does.

### Consequences (amendment)

- No coverage leaves CI; the gate is enforceable on any plan (the #709
  Pro-only blocker is gone) and ports to GitLab by editing the job
  wrapper, not the gate logic.
- The line-weighted merge is the load-bearing detail; it is unit-tested
  in `test/bats/unit/coverage_gate_spec.bats` (floor pass/fail, the
  sum-not-average math with unequal denominators, and missing/empty/
  malformed report handling).
- The section-2 Codecov merge and the section-3 `codecov/project` status
  are SUPERSEDED; the section-1 sharding and the "coverage is a gating PR
  check via `ci-rollup`" posture remain.

## Amendment (#724 / #725 / #730): shard count is dynamic, the partition is time-balanced, the merge is a per-line union

The section-1 sharding evolved to compress the PR critical path further
without weakening the gate (coverage stays a required PR check):

- **Dynamic shard count (#725).** The matrix is no longer the hardcoded
  `['1/4'..'4/4']`. A `compute-shards` job emits `["1/N",...,"N/N"]` from
  `vars.CI_SHARDS` (default 8, clamped [1,12]); the coverage matrix consumes
  it via `fromJSON`. The count is a repo variable because "shard to runner
  count" is not runtime-detectable on GitHub-hosted (parallelism is bounded
  by the plan's concurrent-job limit); it also generalises to self-hosted
  (set the var to the fleet size). `_shard_unit_files` / `--coverage-shard
  N/T` already accept any total T.

- **Time-balanced, integration-pooled partition (#724).** `_shard_unit_files`
  now partitions unit + integration specs in ONE pool (integration is no
  longer appended whole to the last shard, which made that shard the sole
  bottleneck -- measured 326s vs 87-192s for the others at 8 shards). The
  greedy-LPT weight moves from `@test` count to `_spec_weight` (recorded
  seconds from `SHARD_WEIGHTS_FILE`, else `@test` count as a graceful
  fallback). An automated timings source (so the seconds are real, not a
  count proxy) is a deliberate follow-up.

- **Per-line union merge (#730).** `coverage_gate.sh` now merges the shard
  cobertura reports by per-line UNION (a line is covered if ANY shard ran
  it; valid = distinct source lines), NOT `SUM(covered)/SUM(valid)` over the
  root counters. Every shard's kcov reports the whole tree, so source shared
  across shards was double-counted -- the SUM rate drifted DOWN with the
  shard count (4 shards ~52.9% passed; 8 shards 42.42% false-failed). The
  union is shard-count-invariant (real 8-shard data: 51.42%). This SUPERSEDES
  the section-"MERGE MATH" line-weighted SUM described above.

- **Self-maintaining real-runtime weights (#733).** The "automated timings
  source" the #724 bullet deferred. Each coverage shard runs `kcov ... bats
  --report-formatter junit`, and `_junit_to_timings` converts the per-file
  `<testsuite time=...>` entries into a `coverage/timings.tsv`
  (`<seconds> <basename>`) uploaded in the shard artifact. The coverage-gate
  job (which already downloads every shard artifact) merges them via
  `coverage_gate.sh --merge-timings` and, on main-branch pushes only,
  `actions/cache/save`s the result; every run `actions/cache/restore`s it to
  the in-repo `test/bats/.shard-weights` path `_spec_weight` reads by default,
  so the partition self-balances by REAL seconds. PR runs are read-only (PR-
  runner noise never poisons the shared weights); a cache miss or a brand-new
  spec degrades to the `@test`-count fallback. This is the established
  best-practice shape: runtime-weighted greedy-LPT with a self-maintaining
  cached durations file -- cf. CircleCI ("timings-based test splitting gives
  the most accurate split ... the most recent timings data is always used"),
  Knapsack Pro (balance by time so every node finishes together), and
  pytest-split's `least_duration` (largest-first into the lightest group) fed
  by a stored `.test_durations`. The greedy-LPT partition is provably near-
  optimal: Graham (1969, SIAM J. Appl. Math. 17(2):416-429) bounds LPT
  makespan at `(4/3 - 1/(3m))` x optimal. The hard floor is the single
  longest spec FILE (whole-file granularity); splitting a hot file by example
  is a future refinement, not built here.

The "coverage is a gating PR check via `ci-rollup`" posture is unchanged.

## Amendment (#853 / #855): the floor is re-based to 80

Section 3 set `COVERAGE_MIN` to **50**, "just below the current measured
project rate (~52.9%)", and said it was meant to ratchet up. It is now
**80**.

The ratchet is not the whole story: the measurement itself was wrong. The
per-line union key of the previous amendment was the RAW `<class
filename>` kcov emits, and kcov reports one source file under several
prefix-truncated aliases, so every alias re-counted that file's lines
into the denominator. #853 canonicalises the filename before it becomes
part of the key, which moved the SAME suite from ~51% to **84.72%**
(`5907/6972` lines on `main`, run `30814141976`) -- the project rate had
been understated by roughly 33 points, and a 50 floor against an 85%
reality left about 35 points of dead slack in a required check.

80 leaves **4.72 points** of margin below the measured rate: wide enough
that ordinary per-PR churn does not false-fail the gate, narrow enough
that a real regression trips it instead of being absorbed. The v1
absolute-floor posture is unchanged -- this re-bases the number, it does
not adopt the v2 regression-vs-main-baseline gate, which remains the
documented follow-up.

## Amendment (#952): Decision 5's visibility half -- the figure is published per release, in the release commit

- **Date:** 2026-08-28
- **Amendment status:** Accepted -- completes the visibility half of the
  #710 amendment's Decision 5, which shipped the `$GITHUB_STEP_SUMMARY`
  table and deferred everything durable. **Relates:** #710 (Codecov removed,
  the dynamic badge with it), #709.

### Context

Decision 5 kept kcov's HTML and appended a summary table to
`$GITHUB_STEP_SUMMARY`. Both live for the length of one CI run. When the
Codecov badge was deleted, a **static** shields.io badge took its place:

```markdown
![Coverage](https://img.shields.io/badge/Coverage-Kcov-blueviolet?style=flat-square)
```

It reads `Coverage-Kcov` whatever the number does. The figure is computed
on every coverage run -- `coverage_gate.sh` prints `merged line rate <N>%`
and tabulates it -- and then discarded. A README that shows a badge nobody
can be wrong about is worse than one that shows nothing: it makes a reader
believe someone is watching.

### Decision

**The gate's line rate is rendered into a self-contained SVG committed to
the repo, stamped with the version it belongs to, and regenerated into the
release commit.**

*Status of the release step:* the generator and its refusals shipped with
this amendment; the automatic caller has NOT. Wiring it into the harness
release bump is `docker_harness#289` (see 4). Until that lands, the step
is `just release coverage-badge`, run by hand at bump time, and this ADR
says so rather than describing the end state as if it were built.

1. **A committed SVG, not an endpoint badge.** `doc/badge/coverage.svg` is
   plain markup with no external reference; the README draws it as
   `![Coverage](doc/badge/coverage.svg)`. The shields.io *endpoint*
   pattern (`img.shields.io/endpoint?url=raw.githubusercontent.com/...`)
   was considered and rejected twice over: it needs the repo to be
   **public**, because `raw.githubusercontent.com` will not serve a
   private repo to shields.io and shields.io cannot carry a token -- so it
   could never fan out to the mostly-private downstream repos -- and the
   URL binds to `raw.githubusercontent.com`, which is precisely the
   coupling class this ADR's #710 amendment removed. A committed SVG has
   neither problem and ports to GitLab as a file.

2. **The figure carries its version.** The badge reads
   `coverage vX.Y.Z | 84.7%`, never a bare percentage. The cadence is once
   per release (see 4), so a bare number would be read as the coverage of
   `main` and be wrong for the whole cycle -- the same failure as the
   static badge, differently dressed.

3. **The number comes from the gate's own merge math, re-run locally.**
   `script/release/coverage_badge.sh` SOURCES `coverage_gate.sh` and calls
   `_coverage_gate_run` over the kcov reports in `coverage/` -- the output
   of `just test coverage`. The per-line union and the path-alias
   canonicalisation of the previous amendments are not re-implemented, so
   the badge and the gate cannot disagree about what the project rate is.
   The alternatives were **reading the figure back out of the last CI run**
   (fast, but couples the release to one CI provider's API and to a run
   being findable for the exact commit) and **having CI publish the figure
   into the repo** (a commit per merge whose whole content is one digit).
   Recomputing costs a local kcov run before a release -- minutes, on an
   operation that happens a few times a month -- and costs no coupling at
   all: it is the same script, reading files, on a workstation or under
   either CI.

4. **It will be a step of the release bump, not a new mechanism -- and it
   is not one yet.** `.claude/scripts/release-bump.sh` in the harness
   already owns every mechanical release edit -- `.version`, the
   `[Unreleased]` promotion, the regenerated compare-link block. The badge
   **is to become** the fourth thing it regenerates, so that it rides the
   `chore: release vX.Y.Z` commit: **zero new commits**, no new trigger,
   and nothing anyone maintains by hand. That script's own header is the
   argument: the compare-link block stopped being updated around `v0.6.8`
   and ~90 releases rendered a dangling reference, because a hand-run step
   decays. A hand-maintained percentage would decay identically.

   That wiring could not ship here: `release-bump.sh` lives in
   `docker_harness`, a different repo, so this change can only offer the
   seam. It does -- a standalone script with the same `0` / `1` / `2` exit
   triple `release-bump.sh` itself uses -- and the wiring is
   `docker_harness#289`. **Until that issue lands the figure is one
   hand-run command** (`just release coverage-badge`, before the release
   commit is made), which is precisely the decay mode this decision argues
   against; the honest reading of the interval is that it is a known,
   tracked debt, not a completed mechanism. What it is NOT is silent:
   `coverage_badge_spec` asserts the committed badge names the current
   `.version`, so a release cut without the step turns `main` red.

5. **Refusal, never a carried-over figure.** A release whose coverage
   never ran must not publish a stale or an invented number. The generator
   writes nothing and exits 1 when there is no report under `coverage/`,
   when the reports **do not record the sha they were produced from** or
   that sha **is not `HEAD`**, when they **do not record that the whole
   suite produced them**, when a report is **older than the commit
   being released** (it measured an earlier tree), or when instrumented
   sources are **modified in the worktree** (the reports describe neither
   the commit nor the tree). The recorded sha is the load-bearing one:
   `just test coverage` writes it to `coverage/.head-sha`
   (`_stamp_coverage_head`), because comparing the report's mtime against
   `HEAD`'s commit time only catches reports that are too OLD. Measure
   `main`, check an older tag out, and every timestamp check passes over a
   clean worktree while the reports describe a different tree. The
   release edits themselves -- `.version`, the CHANGELOG, the badge --
   are deliberately not in that pathspec, so the check passes on a
   half-applied bump and fails on a code change.

   The sha alone was not enough, and the gap was reachable by an ordinary
   sequence. `just test coverage <n>/<total>` -- the recipe that proves
   the sharded path locally -- writes its slice into the SAME `coverage/`
   tree the full run uses. A stamp that recorded only the sha then
   certified a partition as `HEAD`'s measurement: matching sha, clean
   worktree, fresh mtimes, and a badge off by a factor of N. So the stamp
   records the SCOPE as well -- `scope=full` or
   `scope=partial <m>/<n> specs` on a second line, truncating any earlier
   stamp -- and the generator publishes only `full`. A stamp carrying no
   scope is refused too: unscoped is unknown, and unknown is not
   evidence. The sha answers WHICH tree; the scope answers WHETHER the
   whole suite ran, and the promise of this amendment needs both.

   **The scope is derived from the measurement, not from the
   invocation**, and that correction came after four attempts to fix it
   the other way. Read off the shard FLAG, the scope described the
   arguments rather than the reports, so every input that narrows the run
   without passing through that flag certified a partition as whole: an
   inherited `COVERAGE_SHARD`, an inherited `COVERAGE_PATH` (which the
   in-container dispatch reads first, and which makes the run write no
   report at all), and whichever selector `_run_via_compose` forwards
   next. Each round closed one door and the next round found another,
   because the inputs to an invocation are not an enumerable set. What
   was MEASURED is: `_measured_coverage_scope` compares
   `coverage/timings.tsv` -- the manifest kcov's bats writes, one line
   per spec file that ran -- against the tree's spec inventory, and a run
   narrowed by anything at all leaves fewer specs in it. The manifest is
   erased with the certificate before every run, so a run that writes no
   manifest ends with no stamp rather than with the previous run's. What
   remains enumerable is bounded and mechanically checked: the kcov
   selectors are the `-e NAME="${NAME:-}"` lines of `_run_via_compose`,
   read out of the source by a spec that fails until the coverage
   dispatch assigns each of them. `--unmeasured` renders
   `coverage vX.Y.Z | not measured` in grey: an explicit statement of
   absence, which is what the badge carried for `v0.42.0`, the last
   release cut before this mechanism existed.

### Cadence -- and why it is written down three times

**The figure refreshes once per release.** Not per merge: nobody acts on
52.9% becoming 52.8%, and a commit per merge whose entire content is one
digit fills `git log` with entries no one will read. "What is the coverage
of v0.43.0" is a fact about a shipped artifact, and that is the question a
README figure should answer.

A reader who does not know the cadence misreads the figure as current, so
it is stated where each kind of reader stands: **on the badge itself** (the
version is in the image), **here**, and **in the tooling** -- the
`coverage-badge` recipe doc in `script/release/justfile.release` and the
generator's own `--help`, both of which state the once-per-release cadence
and the ordering it implies (regenerate on the bump's working tree, before
the release commit; afterwards `HEAD` is no longer the measured commit and
the generator refuses).

The fourth place is the one that matters most and is **not written yet**:
the harness-side `.claude/commands/release.md` / `semver-bump` skill, where
the person cutting the release is actually reading. That lives in
`docker_harness` and is part of `docker_harness#289` along with the wiring.
Recording it as done here would be worse than the gap.

### GitLab portability mapping (mechanical, as above)

- **The badge**: unchanged. A committed SVG referenced by a repo-relative
  path renders in GitLab's Markdown exactly as in GitHub's; nothing
  external is involved.
- **The generator**: unchanged. It reads `coverage/**/cobertura.xml`, the
  same artifact GitLab's `coverage_report` consumes, and shells out only
  to `git` and `awk`.
- **The release step**: the bump is a workstation script in either world.
  Nothing in this mechanism reads a GitHub API, an artifact store or an
  environment variable that only one CI defines.

### Consequences (amendment)

- The README figure is now falsifiable: it names a version, and the number
  next to it was produced by the gate over that version's tree.
- A release now needs a local coverage run first, on the commit being
  released, or the generator refuses. That is the intended trade: the
  alternative to paying minutes is publishing a figure nobody measured.
- `just test coverage` now leaves `coverage/.head-sha` behind, carrying
  the sha and the scope (`full`, or `partial <m>/<n> specs`, derived from
  the run manifest `coverage/timings.tsv`). It is the only local evidence
  of which tree the reports describe and how much of the suite produced
  them; `just test clean` removes it with the rest of `coverage/`.
- A local shard run (`just test coverage 1/4`) can no longer be published
  as a release figure, at any commit. That is a refusal an operator can
  hit while doing nothing wrong -- checking the sharded path and then
  cutting a release -- and the cure is one full `just test coverage`.
- Until `docker_harness#289` lands, the regeneration is a hand-run step,
  and the guard against forgetting it is a red `main` after the tag rather
  than a refused bump. That is the known cost of the repo boundary, and it
  is tracked, not assumed away.
- `v0.42.0`'s badge says `not measured`, honestly: it was cut before this
  existed and no report for its tree survives. The first measured figure
  is `v0.43.0`'s.
- Publishing the kcov **HTML** remains Decision 5's other, still-deferred
  half; it has its own obstacle (Pages on a private repo needs a paid
  plan) and is out of scope here.

## Amendment (#726): coverage has TWO parallel modes -- hosted matrix and local in-job -- over one partition

- **Date:** 2026-09-05
- **Amendment status:** Accepted -- extends Decision 1. The sharded
  hosted matrix is unchanged and remains the PR gate. **Relates:** #724
  (the shared LPT partition both modes slice with), #725 (dynamic shard
  count), #730 (the union merge), #1060 (which measured where `bats
  --jobs` under one kcov holds and where it does not; this amendment is
  the remedy for the case it left serial), ADR-00000017 (the throughput
  ceiling this is measured against), ADR-00000026 (self-hosted
  eligibility is a static property of `runs-on`).

### Context

Decision 1 sharded kcov ACROSS a CI matrix. That is the only parallelism
a GitHub-hosted plan sells: one runner runs one job, so the way to use
eight machines is eight jobs.

Two things it does not cover. **On one fat machine the matrix buys
nothing** -- a single self-hosted runner takes the eight entries one after
another, so `CI_SHARDS` there is a way of making the same work slower.
And the run this repo needs MOST is one the matrix never touches: the
#952 amendment made `just release coverage-badge` publish only a
`scope=full` measurement, so every release pays for a whole-suite local
coverage run. That run was serial, and serial is not a kcov floor -- this
ADR's own Context says the cost is "serial x kcov". kcov's bash engine
parses one xtrace stream per traced process and is single-threaded, so N
concurrent bats jobs under ONE kcov all feed one parser. The #1060
amendment below measured where that costs accuracy and found a BOUNDARY
rather than a blanket: on a SHARD, parallel bats under one kcov reproduces
the serial covered set in seven of eight runs and misses 3 lines of 6207
in the eighth, so shards now run parallel; on the FULL SUITE it does not,
so the full-suite run stays serial. What is lost there is trace, not
execution -- the missing lines belong to subprocess-heavy specs whose
tests PASS -- so the bound is trace VOLUME through the one parser.

That bound does not reach **N independent kcov PROCESSES**: each traces
its own children into its own database, each parser reads only its own
slice's volume, and nothing is shared until the merge. This amendment is
the remedy for the case #1060 could not take -- it gives the full-suite
path the machine by removing the single parser, not by parallelising bats
behind it.

### Decision

**Coverage has two parallel modes. They differ in HOW the slices are
distributed, never in WHAT a slice is.**

1. **Hosted matrix (production, unchanged).** `test.sh --coverage-shard
   N/T`, one slice per GitHub-hosted job, merged by the `coverage-gate`
   job's per-line union over the shard artifacts. This is the PR gate.

2. **Local in-job.** `test.sh --coverage-local [--jobs N]` (default N =
   `nproc`; `just test coverage-local [N]`) runs EVERY slice of the same
   partition as N concurrent kcov processes inside one dispatch, and
   merges them with `kcov --merge` into `coverage/kcov-merged/`. It writes
   the same `coverage/` tree the serial run writes and leaves the same
   `timings.tsv`, so the scope stamp reads `full` and the release badge
   accepts it.

   The scope is the point, not a detail: a mode that measured the whole
   suite and stamped `partial` would be refused by the badge generator and
   the serial run would still be on the release critical path.

3. **ONE partition primitive serves both.** Both call
   `_shard_unit_files <n>/<total>` (#724's greedy LPT over recorded
   seconds). A second partitioner would be a second roster, and the
   failure mode of two rosters is a spec that belongs to neither.

4. **A lost slice is a REFUSAL, not a smaller number.** A slice that
   produced no report -- a kcov that died after its tests passed, leaving
   an empty output directory and a zero status -- fails the run. Merging
   the survivors would publish a smaller line set under a whole-suite
   certificate, which reads as a coverage regression rather than as the
   lost slice it is. The same applies to a job count that is not a
   positive integer and to a slice that matched no spec files (more slices
   than the suite has specs).

5. **The local mode is NOT in the PR gate, and that is deliberate.**
   `self-test.yaml` is untouched; the local mode's CI exposure is an
   opt-in `workflow_dispatch` workflow, `.github/workflows/coverage-local.yaml`,
   on `[self-hosted, gpu]`, carrying the fork guard every
   self-hosted-eligible job in this tree carries (ADR-00000026). One
   self-hosted runner is a single point of failure and a contention point:
   a required check that queues behind another tenant's job can be blocked
   by work unrelated to the PR, and a machine that is down blocks every
   merge. The hosted matrix has neither property. Should the fleet ever
   grow, promoting the mode is a `runs-on` plus a trigger, not a rewrite --
   which is the second reason to build it now rather than at migration
   time.

### Consequences (amendment)

- A full-scope coverage run -- the one every release needs -- can use the
  whole machine instead of one core. The PR gate's latency is unchanged,
  because the PR gate did not move.
- kcov's `--merge` becomes load-bearing for the local mode, where the CI
  path relies on the gate's own per-line union (#730). They are two
  implementations of one property, and the property is checkable against
  the LINE SET rather than the percentage -- a matching rate over a
  different set is not equivalence. The measurement below is that check.
  **It did not come back empty**, and the amendment states what it found
  rather than the equality it set out to claim.
- The self-hosted workflow is authored but, at the time of writing, has
  not been RUN: no self-hosted runner was reachable from where this
  landed. It is stated rather than implied, because a validation nobody
  performed is not a validation.
- `--coverage-local` is refused in combination with `--coverage-shard`,
  `--coverage-path` and `--bats-path`, each by a message naming the flag
  the operator typed.

### Alternatives (amendment)

- **`kcov` over `bats --jobs`.** The obvious in-job parallelism, and the
  one the #1060 amendment measured rather than assumed. It is not rejected
  everywhere -- #1060 turned it ON for shards, where the trace volume
  through the one parser stays inside the bound. It is rejected for THIS
  run: at whole-suite volume the covered set moves (8617 lines serial,
  reproducibly, against 8532 and 8587 parallel), and the full-scope run is
  the one that feeds the release badge, so a figure that shifts a point
  between two runs of one tree is worse than a slow one.
- **Raise `CI_SHARDS` and point the matrix at the self-hosted runner.**
  It does not parallelise anything on ONE runner (the entries serialise),
  and it puts the PR gate on a shared workstation -- the SPOF and
  contention this amendment's Decision 5 refuses.
- **Make the local mode the PR gate outright.** Same objection, plus it
  would delete the hosted matrix's ability to run when the workstation is
  off.
- **Let the coverage-gate union the per-slice reports instead of
  `kcov --merge`.** It would reuse the merge math #730 already proved,
  but it leaves no single HTML report for a human to open, and the badge
  generator's `discover_reports` treats a top-level `kcov-merged/` as THE
  project report -- so the local run would have to be special-cased in the
  release path. Kept as the fallback if the equivalence check ever fails.

### Measurement (amendment)

Four whole-suite runs of ONE tree (`bea6324`, 32 cores, one at a time on
an otherwise idle machine), compared on the canonicalised `(file, line)`
sets of their merged cobertura reports rather than on their rates. The
canonicalisation is the coverage-gate's own longest-path-suffix rule, so
kcov's prefix-truncated aliases are not read as differences.

| run | wall | instrumented | covered | stamp |
|-----|------|--------------|---------|-------|
| `just test coverage` (serial) | 2052 s | 9667 | 8179 | `scope=full` |
| `just test coverage-local` (32 slices) | 299 s | 9667 | 8152 | `scope=full` |
| the same, again | 294 s | 9667 | 8152 | `scope=full` |
| `just test coverage-local 1` (1 slice) | 2022 s | 9667 | 8167 | `scope=full` |

**What holds.**

- **6.9x**, and the release path is the beneficiary: 34 minutes becomes 5.
- The **instrumented set is identical** in all four -- symmetric
  difference 0 over 9667 lines. The denominator does not move with the
  slice count, which is the invariant #730 had to restore for the CI
  path's merge and is the one a sum would break first.
- The mode is **deterministic**: two 32-slice runs agree on every one of
  8152 lines, in both directions.
- Both parallel runs stamp **`scope=full`**, which is the acceptance the
  release badge turns on. The scope is derived from the merged run
  manifest, and both manifests name all 164 specs -- the same 164 the
  serial run names.

**What does not hold, stated rather than rounded away.** The covered sets
are NOT equal. They are strictly nested:

    32-slice (8152)  subset of  1-slice (8167)  subset of  serial (8179)

27 lines, 0.33% of the covered set, in three files:
`dist/script/docker/lib/help.sh` (12), `config_summary.sh` (14),
`bootstrap.sh` (1) -- almost all of them arms of localised `case` lookup
tables, where a line is executed only if something asked for that exact
`<lang>:<key>`.

The 1-slice run is what separates the two candidate causes, and it
acquits the merge. At one slice there is no partition: the whole suite
runs in ONE bats process, exactly as the serial run does, and the report
still goes through `kcov --merge`. It loses 12 of the serial run's lines
and gains none. A merge cannot lose what was never split, so those 12 are
lost BEFORE the merge -- the remaining difference between the two runs is
that the serial runner hands bats the pool DIRECTORIES with `--recursive`
while this one hands it an explicit file list in greedy-LPT order. The
suite therefore covers slightly different lines depending on the order it
runs in. Splitting it 32 ways loses 15 more, which is the same effect
with the processes separated as well.

So the finding is about the SUITE, not about this mode: some spec's
coverage depends on what ran before it in the same bats process. It is
recorded here and left open, because closing it means finding that spec
and giving it its own fixture -- work that belongs to whoever owns the
coupling, not to the runner that exposed it.

**What it costs meanwhile.** A badge published from a parallel run reads
0.33 points lower than one published from a serial run of the same tree,
against a floor of 80 and a rate near 84. Nothing in the gate moves. But
the two modes are not interchangeable to the line, and this amendment does
not claim they are.

Independent of the suite, `kcov --merge` itself is now pinned as a UNION
by `test/bats/integration/kcov_merge_union_spec.bats`, against the real
binary over a subject with two disjoint branches: the merged covered set
equals the union of the slices', and the merged instrumented set equals
the union rather than the sum.

## Amendment (#1060): a shard's bats runs parallel under kcov; the full-suite run does not, and that asymmetry is measured

- **Date:** 2026-09-05
- **Amendment status:** Accepted -- completes the correction this ADR's own
  Context opened and half-applied. Section 1's sharding is unchanged, and so
  is the "coverage is a gating PR check via `ci-rollup`" posture.
  **Relates:** #726 (a kcov process per slice), #1002 (whose thesis this
  supersedes), ADR-00000016, ADR-00000017.

### What was left in place

The Context above reads #377 correctly: it "left the **coverage path fully
serial** ... The ~8-12 min coverage runtime was therefore **serial x kcov**
... **not an inherent kcov floor**." Only one of those two factors was then
addressed. Section 1 divided the kcov half across a CI matrix and left the
serial half running inside every shard, where it stayed for two and a half
months.

The mechanism was a flag with two writers. `script/test/drivers/bats.sh` held
TWO hand-assembled bats invocations, not one: `_run_coverage` and
`_run_system`, each with its own argument list, and `_run_system` with its own
`nproc` probe and its own `--jobs` besides. What was unique to `_run_coverage`
is narrower and is the actual finding -- it was the only bats invocation in
the driver that never received `--jobs` at all. Every other runner --
including `_run_coverage_path`, added later -- takes its arguments from
`_bats_args_with_label`, which appends `--jobs $(nproc)` where GNU parallel
is present and falls back to serial with a message where it is not.
`git log -S'--jobs' -- script/test/drivers/bats.sh` returns only the driver
split: the flag was never removed from the coverage path, it was never added.
That there were two copies is why the decision below is "one writer for the
flag" rather than "add the flag here": a second copy is how the divergence
arose, and a third is what the guard refuses.

### Decision

**`_run_coverage` builds its bats arguments through
`_bats_args_with_label`,** and the helper takes a third argument naming the
caller's jobs policy (`parallel`, the default, or `serial`). Writing
`--jobs` a second time by hand -- which is how the divergence arose -- is
refused by a spec that allows the flag exactly one occurrence in the driver,
inside the helper; `_run_system`, the other hand-rolled copy, is routed
through the helper as well. An unrecognised policy is a `_die`, not a
default, and so is an EMPTY one: the helper reads `${3-parallel}`, so an
omitted third argument takes the documented default while a caller
expanding an unset variable reaches the refusal instead of the parallel
branch.

**The policy is derived from what the run will WALK, not from the
argument it was called with.** The full-suite branch declares `serial`. The
shard branch compares the slice `_shard_unit_files` returns against the
whole pool (`_coverage_pool_files`, one writer for "what the whole suite
is") and declares `serial` when the two are the same set, `parallel`
otherwise. Keying the policy on WHETHER a shard argument was passed is not
enough: `1/1` is a shard by syntax and the entire suite by content, and it
earns `scope=full`, the only scope `coverage_badge.sh` publishes -- so it
would have published the parallel figure this amendment measures as
under-reporting. `just test coverage 1/1` reaches that case, and so does
`vars.CI_SHARDS=1`, which `self-test.yaml` clamps into `[1,12]` and turns
into the matrix `["1/1"]`. This is the same derivation the release
certificate uses (`_measured_coverage_scope` compares the run manifest
against the inventory): an invocation is not evidence of what a run
measured, so neither the scope nor the policy is read off one.

The asymmetry is the finding, not a hedge:

- **A shard's line set holds, and where it does not the miss is 0.05%.**
  Three slices (two different partitions of 1/8, plus 6/8), comparing the
  covered and valid sets the coverage gate merges -- canonical
  `(file, line)` keys, symmetric difference computed in BOTH directions.
  Eight parallel runs: SEVEN reproduce the serial covered set exactly
  (7835/9229, 6373/7360 and 6207/7439 lines, empty difference each way),
  and the eighth was short **3 lines of 6207**, one-directionally.
  Serial runs of a slice agree with each other exactly. Wall time for the
  whole recipe: 147s / 164s serial against 47s-53s (shard 1/8) and 371s
  against 196s (shard 6/8). **The CI matrix runs shards and merges them
  by per-line UNION over a floor with ~4.7 points of margin, so a miss of
  that size cannot reach the gate's verdict -- it is not zero, and it is
  what #726 makes structurally zero.**

- **The full suite's line set does move, so it stays serial.** At ~4500
  tests, two serial runs record the same 8617 covered lines; two parallel
  runs record 8532 and 8587 -- each a strict SUBSET of the serial set (0
  lines covered in parallel that serial missed, twice) and differing from
  each other. `lines-valid` is identical in every run (10194), so only the
  numerator moves: 84.53% against 83.70% and 84.24%. This is the run that
  stamps `scope=full` and feeds the release badge of the #952 amendment,
  and a badge that moves a point between two runs of one tree is the
  falsifiable-figure promise broken from the inside.

- **What is lost is trace, not execution.** The dropped lines cluster in
  subprocess-heavy code (`setup_cmd.sh`, `watchdog.sh`, `prune.sh`,
  `transcript.sh`, `help.sh`, `bootstrap.sh`) whose tests PASS in both runs
  -- `just docker help renders zh-TW recipe summaries` is `ok` in each, and
  its zh-TW `case` arms appear only in the serial report. N parallel bats
  jobs feed their trace streams to ONE kcov process whose parser is
  single-threaded: the miss scales with the volume of trace and never
  reverses sign (no parallel run has ever recorded a line serial missed,
  in ten comparisons), which is a reader losing samples rather than a
  flaky test. That parser is also the share of the runtime `--jobs` cannot
  divide. **Making it scale, and with it the full-suite path, is #726 (a
  kcov process per slice) -- a different change, not a competing one.**

- **The residual is disclosed, not absorbed.** A gate that ever becomes the
  regression-vs-baseline v2 this ADR still lists as a follow-up would be
  comparing figures whose noise floor is now non-zero on the shard path;
  that comparison has to be made against #726 landing first, or against a
  serial policy for the gate too.

### The junit report and the weights it feeds

`_junit_to_timings` reads one `report.xml` and writes `coverage/timings.tsv`,
which the next partition weighs. Under `--jobs` bats still emits ONE coherent
report: after a parallel full run the manifest names all 173 specs and the
run stamps `scope=full`, which is exactly the check that a narrowed or
truncated report would fail.

The per-spec seconds in it are wall-clock under contention, not per-test in
isolation: mean 4.32x the serial figure, median 4.00, min 0.50, max 27.0.
That distortion does not unbalance the partition, because greedy-LPT reads
relative weights and these are recorded in the same regime they will predict.
Driving the real `_shard_unit_files` at 8 shards and weighing each partition
by the parallel durations it must balance: weights from a serial run give
makespan 1446 (loads 754-1446); weights from a parallel run give 1138 (loads
1111-1138). The transition run is the 1446 case -- better than the
`@test`-count fallback, and one run long.

### Consequences (amendment)

- The PR critical path drops by the measured shard figures above, against a
  merged gate rate whose measured movement is at most 3 lines in 6207 on one
  shard of eight, unioned away wherever another shard ran the same line.
- `just test coverage` (full suite) is unchanged in duration -- ~35 min on a
  32-core host for this tree. The parallel version of it exists and is 4x
  faster; it is not adopted because it under-reports. Anyone tempted to
  flip that policy should re-run the comparison above first, and #726 is
  what would make the answer different.
- The helper now carries a policy argument, so "this run must be serial"
  and "this host has no GNU parallel" are distinguishable in the run's own
  first line (`serial by policy` against `serial; parallel not in PATH`).
- `_run_system` gains `--recursive` and the fallback message it never had,
  which is what routing it through the helper means.
- A shard invocation whose slice IS the whole suite (`1/1`, or any
  `<n>/<total>` a small enough tree makes exhaustive) runs serial and says
  `serial by policy` in its first line. It is slower than the argument
  suggests, and that is the point: it is the run that would otherwise
  publish a parallel figure as `scope=full`.

## Amendment (#1068): the job count is a FLOOR on concurrency, and a third policy meters the kcov runners

- **Date:** 2026-09-05
- **Amendment status:** Accepted -- narrows the Decision of the amendment
  above. Section 1's sharding, the one-writer guard, the shard /
  full-suite asymmetry and the `1/1`-is-the-suite rule are all unchanged.
  What changes is the COUNT the one writer derives and the size of the
  policy vocabulary it accepts -- so the two-name enumeration in the
  #1060 Decision (`parallel`, the default, or `serial`) and its
  description of the helper as one that "appends `--jobs $(nproc)`" are
  superseded here rather than left to be read as current.
  **Relates:** #726 (a kcov process per slice), #1002, #1060.

### What the previous amendment did not look at

It routed every bats invocation in the driver through
`_bats_args_with_label` and left the count that helper derives exactly as
it found it: `$(nproc 2>/dev/null || echo 4)`. `nproc` is the right
question for a CPU-BOUND workload and this suite is not one -- a bats
test spends its time waiting on subprocesses, and #1002 measured 1-2 of
32 cores busy for the length of a run. CI's runner has four cores, so
`--jobs $(nproc)` there produced exactly the ratio the flag exists to
remove.

Measured on one real coverage shard, through the production path, under a
4-CPU cpuset, two reps per point: `--jobs 1` (serial control) 108.4s /
108.9s, `--jobs 4` (what CI ran) 113.4s / 104.8s, `--jobs 8` 82.7s /
87.7s, `--jobs 32` 62.2s / 63.1s, `--jobs 64` 61.9s / 62.5s. One rep at 4
is slower than serial and one is faster: indistinguishable. Plain bats on
the same shard and the same four cores is 88.4s / 93.8s at `--jobs 4`
against 42.5s / 42.2s at `--jobs 32`, so the effect belongs to the SUITE
and not to kcov.

Re-measured on a different 22-spec slice under the same 4-CPU cpuset, two
reps per point: plain bats 75.7s / 81.7s serial, 83.8s / 98.9s at
`--jobs 4`, 41.9s / 44.0s at `--jobs 32`; the same slice under kcov
139.3s / 114.6s serial, 111.1s / 122.3s at 4, 67.9s / 70.2s at 32. A
different partition and the same three conclusions: 4 is not
distinguishable from serial, 32 is ~1.8x serial, and the ratio survives
kcov being in the loop.

`nproc 2>/dev/null || echo 4` also answered two different questions with
one number. A failed probe and a genuine four-core machine both printed
`jobs=4`, and on CI both were true at once, so a run's own log could not
say which had happened -- the same shape of silent wrong answer the
policy argument was added to refuse one line above.

### Decision

**1. The count is `max(cores, 32)`: a floor, never `k x nproc`.** 32 is a
KNEE and not a peak, which is what decides the SHAPE of the rule. Four
INTERLEAVED reps per point on a 32-core host, same slice: 16 jobs 43.7s,
32 jobs 26.5s, 64 jobs 25.8s, 128 jobs 25.7s. Below the knee costs 1.65x;
above it the curve is flat out to 4x the core count. (A first two-rep
pass read 128 as worse than 32 -- 60.7s / 47.3s against 49.0s / 47.3s --
and the 60.7s does not survive repetition; that reading is withdrawn, and
with it any claim that a large machine must be held to its cores.)

So the count ABOVE the knee is free, and a floor is chosen for the
property a re-tuner needs rather than for a winner: it is monotone, and
it cannot land BELOW the knee, where `k x cores` lands on any machine
smaller than 32/k -- which is the four-core runner this started on. 32 is
a property of the WORKLOAD, how many waiting tests it takes to keep the
pipe full, not of a machine, which is why nothing here scales it.
Re-derive it by sweeping `--jobs` against one shard on a constrained
cpuset, interleaving the points so one slow rep cannot become the
finding; do not multiply it.

**2. A third policy, `metered`, is one job per core with no floor**, and
the driver's two kcov runners (`_run_coverage`'s shard branch and
`_run_coverage_path`) declare it. The amendment above established why: N
bats jobs drain into ONE single-threaded trace parser, so the share that
does not divide by `--jobs` is the share that decides what the report
says. Measured on one shard: 4 -> 32 jobs is 1.75x and costs a
REPRODUCIBLE hole -- four runs at 16/32 jobs union to 31 lines short of
the serial covered set, 30 of them the compose-lifecycle region of
`dist/script/docker/wrapper/run.sh`, ~0.45 points off the reported rate
-- where two runs at `--jobs 4` union to the serial set exactly. The
re-measurement above reproduces the shape on its own slice: two serial
runs record a byte-identical 3093 covered lines, the union of two
`--jobs 4` runs loses none of them, and the union of two `--jobs 32` runs
is 18 short with 17 of the 18 in one file. Faster while losing lines is
not an improvement for the runner whose output IS the line set.
`metered` is refused-by-default like the other two: an unknown or empty
third argument still `_die`s.

**3. An unreadable core count falls back and LABELS ITSELF one**, where
an unreadable policy still `_die`s, and the two are not in tension. An
unreadable POLICY is a caller's bug and there is no correct run to give
it; an unreadable CORE COUNT is an ENVIRONMENT, the same kind as
`parallel` missing from PATH, which this helper already falls back on and
names. Under `metered` the fallback is 1 rather than the floor: with no
core count there is nothing to meter to, and fewer jobs is the safe
direction for a run whose output is a line set.

### Consequences (amendment)

- Six runners with no kcov in the loop take the floor: unit, integration,
  unit-shard, bats-path, bats-fragile and system. On the four-core CI
  runner the `bats-integration`, `bats-fragile` and `system` jobs go from
  four concurrent bats jobs to 32. On any host with 32 or more cores
  NOTHING CHANGES -- `max(32, 32)` is what `nproc` already returned -- so
  a green gate on a large developer machine is evidence about the tests
  and the docs, not about the floor. The CI jobs are where it is
  confirmed.
- `system` is the runner whose every test waits on `docker`, so it has
  the most to gain and is also the one whose concurrency this widens
  furthest: two of its four spec files pin
  `BATS_NO_PARALLELIZE_WITHIN_FILE`, so up to 13 of its 19 tests can now
  be in flight at once against the four that could before, each one a
  `docker buildx build` on a four-core runner. That is the one behaviour
  here a local gate cannot settle.
- The coverage matrix is unaffected. `metered` resolves to the core
  count, which is what the shard path already ran at, so the reported
  rate and the release badge move by nothing; what the policy buys is
  that the next change to the DEFAULT cannot silently take 0.45 points
  off them.
- The four labels a run prints are mutually distinguishable --
  `(cores, at or above the floor)`, `(floor, over N cores)`,
  `(fallback: nproc gave no core count)`, `(metered to the core count)`
  -- so a run's own first line says which of the four happened, which is
  precisely what `jobs=4` could not.
- `nproc` reports the CPUs a process may be SCHEDULED on, an affinity
  mask, and not a CFS quota: in a container started with `--cpus=2` on a
  32-core host it still prints 32 (measured). The floor does not care --
  it oversubscribes on purpose -- but `metered`'s invariant is stated in
  cores, so in a quota-limited container it is not held and the kcov
  drain is oversubscribed anyway. Nothing base launches is capped that
  way (its own compose services set no CPU limit, and a GitHub-hosted
  runner is a whole VM), so this is a boundary of the policy and not a
  live defect; a self-hosted runner that meters CPU by quota would make
  it one.


## ---- FILE: doc/adr/00000010-justfile-layering-and-base-downstream-split.md ----

# Layered `just` entry + base/downstream directory split

> Serves: PRD invariant 6 (base is a subtree; downstream a thin caller)
> -- established the `dist/` split + layered `just` entry.

- **Date:** 2026-06-22
- **Status:** Accepted
- **Amends:** ADR-00000006 (frozen `.base/` interior paths move; see below)
- **Builds on:** ADR-00000005 (`just` as the user-facing entry)
- **Amended:** 2026-07-15 by #831 -- the tool-managed `setup.conf` leaves
  the config-layer. It is `just setup`-managed, not hand-edited, so the
  per-repo override moves out of `<repo>/config/docker/setup.conf` to the
  repo-root dotfile `<repo>/.setup.conf` (template default
  `dist/config/docker/setup.conf` -> `dist/.setup.conf`). This makes the
  criterion explicit: `config/` is the HAND-EDITABLE surface (shell
  config) only; the tool-managed file is a root dotfile. Region B's
  drift-hash path re-points in the same lockstep slice (see the Region B
  note below), and `upgrade.sh` auto-migrates a legacy override.
  Reverses #262, which had nested it under `config/docker/` for layout
  uniformity.

## Context

Two problems converged:

1. **No extension point for repo-local recipes (#594).** The downstream
   user-facing entry is a single `justfile` symlinked to
   `.base/script/docker/justfile` with a fixed recipe set (`build` /
   `run` / `exec` / `stop` / `prune` / `setup` / `setup-tui` /
   `upgrade`). A repo that wants its own recipe (e.g. a deploy or
   per-repo orchestration command) has no clean path: editing the
   symlink target edits base (overwritten on subtree pull); committing a
   real `justfile` is clobbered back to the symlink by `init.sh`. So
   repo-specific commands fall back to `./script/*.sh`, off the
   `just --list` discovery path.

2. **base mixes two audiences in the same trees.** `script/docker/`,
   `config/`, `dockerfile/`, and `test/smoke/` each contain material that
   is *shipped to consumers* alongside material that is *base's own dev /
   CI tooling*, with no structural line between the two. base's own
   self-test entry (`justfile.ci`) sits at the repo root next to the
   downstream-facing `justfile`.

While designing the extension point, several `just` facts (verified on
`just` 1.52) constrained the solution:

- An `import` path inside a justfile reached **via symlink** resolves
  relative to the *symlink's location* (the repo root), not the symlink
  target's real directory.
- A **duplicate recipe name across `import` is a hard error** (not a
  shadow). So repo-local recipes cannot be imported top-level alongside
  the docker recipes -- a single `build:` collision would break *every*
  recipe.
- `mod?` gives a **sub-command namespace** (`just <ns> <recipe>`); a
  module recipe's default cwd is the module file's own directory.
- `mod?` lines living inside an *imported* file still create **top-level**
  namespaces, and their module paths resolve relative to that imported
  file's own directory.
- `import?` / `mod?` of a missing file is not an error.

## Decision

### 1. Layered entry, docker top-level, everything else namespaced

The downstream entry becomes a thin aggregator:

```just
import  'script/docker/justfile.docker'        # docker recipes -> TOP-LEVEL (just build/run/...)
mod?    ci        'script/ci/justfile.ci'      # just ci ...
mod?    cd        'script/cd/justfile.cd'      # just cd ...
mod?    template  'script/template/justfile.template'   # just template ... (help + new)
import? 'script/local/justfile.local'          # repo-owned registry of user groups
default:
    @just --list
```

Docker recipes stay top-level (`just build`); **every other group is a
`mod?` namespace** (`just ci|cd|template|<group> ...`). This is forced by
the duplicate-name hard error: namespacing via `mod?` is the only
collision-proof mechanism, and it doubles as the add-only guarantee
(`local` can never override `build`).

### 2. base/downstream directory split

Everything shipped to consumers lives under a base-root `dist/`
folder that **mirrors a consumer's layout**; base's own tooling stays in
base-root `script/` + `test/`. The `.base/` subtree carries both, but
consumer symlinks only ever point into `.base/dist/`.

base repo:

```
dist/                 # [SHIPS] consumer side = .base/dist/
  script/
    justfile                # the entry (no suffix)
    docker/   justfile.docker  lib/ runtime/ wrapper/
    ci/       justfile.ci  *.sh
    cd/       justfile.cd  *.sh
    template/ justfile.template  new.sh  skel/
  config/                   # default config layer (consumer overlays per-file)
  dockerfile/Dockerfile     # consumer Dockerfile template (was Dockerfile.example)
  test/smoke/
  .hadolint.yaml
script/                     # [BASE-OWN] dev / CI / release
  ci/  justfile.ci  ci.sh  lint_*.sh
  cd/  justfile.cd
test/  unit/ integration/ behavioural/
dockerfile/Dockerfile.test-tools
```

consumer (after init):

```
<repo>/
  justfile                SYMLINK -> script/justfile
  script/
    justfile              SYMLINK -> .base/dist/script/justfile   (identical to base; auto-flows)
    docker/  justfile.docker + build.sh ... setup_tui.sh   SYMLINK -> .base/dist/script/docker/...
    ci/ cd/ template/      SYMLINK -> .base/dist/script/...
    local/                # REPO-OWNED (seeded once, committed, never clobbered)
      justfile.local      #   registry; entry import?s it; `just template new` appends here
      <name>/ justfile.<name> <name>.sh
```

### 3. Ownership: symlink entry, repo-owned registry

`script/justfile` is a **pure symlink, byte-identical to base** (base
improvements auto-flow). It is never written. New groups register in the
**repo-owned** `script/local/justfile.local` (seeded once by `init.sh`,
committed, never clobbered), which the entry `import?`s. This resolves
the tension between "the entry should track base" and "new-group must
write somewhere persistent": the writable surface is `script/local/`, not
the entry.

### 4. `just template new <name>` scaffolding

`just template new <name>` creates `script/local/<name>/justfile.<name>`
+ `<name>.sh` from `dist/script/template/skel/` and appends a
`mod?` line to `script/local/justfile.local` (idempotent). Bare
`just template` prints help. The mechanism is discoverable out of the box
(a seeded example), replacing #594's original `import?` plan, which the
duplicate-name hard error makes unworkable for an add-only top-level
import.

### 5. Naming

- `Dockerfile` (was `Dockerfile.example`): `.example` only disambiguated
  it from `Dockerfile.test-tools` in a shared folder; the `dist/`
  location now disambiguates, and it maps 1:1 to the consumer
  `Dockerfile`.
- `Dockerfile.test-tools` keeps its suffix: it *names the image it
  builds*, not mere disambiguation.
- Group files align to the group name: `justfile.<name>` + `<name>.sh`.
- `ci` and `cd` are **separate** namespaces/folders (not merged
  `cicd`); CD pipeline *content* is deferred to a future issue, this only
  lays the `cd/` skeleton + wiring.

## Amendment to ADR-00000006

ADR-00000006 froze three `.base/` interior path regions that
`upgrade.sh` hard-codes. This refactor moves two of them, so per that
ADR's own discipline `upgrade.sh` is updated **in lockstep**, region by
region, in the slice that moves each path:

- **Region A (`.base/init.sh`)** -- unchanged. `init.sh` stays at the
  base root.
- **Region B (`config/` drift detection)** -- `config/` moves to
  `dist/config/`. The pre/post-pull snapshot paths
  (`HEAD:${TEMPLATE_REL}/config`,
  `.../config/docker/setup.conf`) move to
  `${TEMPLATE_REL}/dist/config[/docker/setup.conf]` in the same
  slice that relocates `config/`. *(Amended 2026-07-15 by #831: the
  setup.conf blob snapshot further moves to
  `${TEMPLATE_REL}/dist/.setup.conf` and the downstream override to
  `<repo>/.setup.conf`, as setup.conf leaves the config-layer; the
  `config/` tree hash keeps guarding the hand-editable shell config.)*
- **Region C (Dockerfile lint-stage auto-patch)** -- `script/docker/lib/`
  and the `script/docker/*.sh` umbrella loaders move under
  `dist/script/docker/`. The grep+sed source paths
  (`COPY .base/script/docker/lib`, the `script/*.sh` umbrella) move in
  the same slice that relocates `lib/` and the wrappers.

The frozen-path **list** in ADR-00000006 is hereby re-pointed to the
`dist/` locations; the contract (move only as a deliberate,
`upgrade.sh`-aware change) is unchanged and reaffirmed.

## Consequences

- **Breaking for consumers.** Wrappers move from flat `script/*.sh` to
  `script/docker/*.sh`; the entry becomes a symlink chain; `script/local/`
  is seeded. Every downstream repo must subtree-upgrade past this tag and
  re-init (the fanout slice). Direct `./script/build.sh` callers break;
  the `just`-first migration (ADR-00000005) covers this.
- **Subtree dead weight.** The `.base/` subtree carries base's own
  `script/` + `test/` into every consumer. Accepted: it is the subtree
  model's cost, and `dist/` makes the shipped-vs-own line legible.
- **Extensibility without a generator.** `just` has no glob import, so
  auto-discovery is impossible; the fixed base namespaces (`ci`/`cd`/
  `template`) are wired statically and user groups self-register in the
  repo-owned `script/local/justfile.local`. No generated aggregator, no
  re-generation step.
- The work lands as a tracked epic of thin vertical slices (base reorg ->
  justfile mechanism -> consumer fanout -> folded #607), each gated by
  the base self-test; `just`-fact regressions (symlink import resolution,
  duplicate-name) are locked with tests.

## Alternatives

- **`import? 'justfile.local'` top-level (the original #594 plan).**
  Rejected: a repo-local recipe colliding with a base recipe name is a
  hard error that breaks the whole `just`, not a shadow. Namespacing via
  `mod?` is required.
- **Modules with `local::` prefix for everything.** Rejected for the
  docker recipes (`just local::build` is worse UX than `just build`);
  kept only for the genuinely repo-local groups.
- **Keep the flat single justfile, add a second imported file.** Does not
  give the base/downstream audience split, and still hits the
  duplicate-name problem for top-level additions.
- **Path-manifest / glob discovery for upgrade.sh paths.** Already
  rejected in ADR-00000006; unchanged here -- the path move is a
  deliberate lockstep edit, exactly the discipline that ADR ratified.


## ---- FILE: doc/adr/00000011-just-command-model-full-namespace.md ----

# `just` command model: zero-special-case namespaces, generic tooling, min->max coverage

> Serves: PRD invariant 6 (base is a subtree; downstream a thin caller)
> -- established the zero-special-case `just` command model + generic
> runner.

- **Date:** 2026-06-23
- **Status:** Accepted
- **Amends:** ADR-00000010 (docker is no longer top-level; `ci`/`cd`
  namespaces renamed; entry shape) and ADR-00000006 (`init.sh` /
  `upgrade.sh` leave the base root)
- **Builds on:** ADR-00000005 (`just` as the user-facing entry)
- **Amended:** 2026-06-26 by #714 -- the shipped-tree directory `downstream/`
  was renamed to `dist/` (terminology de-overload; `dist` = distribution).
  Every `downstream/script/<ns>/` reference in sec.4 (the origin), sec.5,
  and the §8 relocation now reads `dist/script/<ns>/`; the origin
  single-source-of-truth lives at `dist/script/<ns>/` and a consumer's
  `script/<ns>/` symlinks into `.base/dist/script/<ns>/`. See ADR-00000006's
  #714 amendment for the frozen-path-contract + consumer-migration detail.

## Context

ADR-00000010 shipped the layered entry + base/downstream split, but kept
two asymmetries that turned out to be load-bearing irritants once the
namespaces multiplied:

1. **docker recipes stayed top-level** (`just build`, `just run`) while
   everything else was a `mod?` namespace (`just ci ...`,
   `just template ...`). The top-level docker recipes are a *special
   case*: adding any new top-level verb risks the duplicate-name hard
   error, and the mental model ("some verbs are bare, some are
   namespaced") has to be memorised.

2. **The namespace names described mechanism, not action.** `ci` / `cd`
   are pipeline-stage jargon; a user wanting "run the tests" or "cut a
   release" has to translate. And the natural request "I want every CI
   check under one roof" did not map onto `ci` + a separate top-level
   `lint`.

Three further requirements surfaced while using the layered entry:

- **Coverage from smallest to largest unit.** Every command should scale
  from one file / one check up to the whole suite, *narrowing via
  options* rather than memorising sub-recipes or passing bare positional
  args whose meaning is positional.
- **One generic tool, per-repo content.** base self-tests the template
  (shellcheck + bats over its own scripts/specs); a consumer tests its
  image (build the devel-test stage, run smoke). These were modelled as
  *different* tooling. They are not: the *tools* (shellcheck, bats,
  hadolint) are identical; only the *content* of `test/` differs. Modelling
  them as one generic runner is what lets the whole `script/` tree be a
  single shared origin.
- **`init.sh` / `upgrade.sh` at the base root are an eyesore** and break
  the "every action lives in a namespace" rule.

`just` 1.52 facts from ADR-00000010 still hold (symlink-relative import
resolution; duplicate top-level recipe name = hard error; `mod?` =
namespace; `import?`/`mod?` of a missing file is not an error).
Additionally verified for this decision:

- `just <ns> <recipe> --help` reaches the module: per-recipe help and
  `--lang` are surfaced by the recipe forwarding the flag to its backing
  script (the wrappers already localise via `--lang`). The dashed
  `just <ns> --help` does **not** reach the module -- a dashed name cannot
  be a `just` recipe/alias, so it is parsed as a recipe lookup that errors;
  namespace help is `just <ns>` or the `just <ns> help` recipe instead (see
  §6, reconciled by #789).
- Dynamic shell completion (`clap_complete`, `JUST_COMPLETE=<shell> just`)
  is **module-aware** -- it drills into `just docker <tab>` and
  `just test lint <tab>`. The distro `just.fish` (shipped by the *fish*
  package, not `just`) only lists top-level recipes and does **not**
  drill, which is why an explicit completion installer is needed.

## Decision

### 1. Zero special cases: every action is a namespace

The entry mods every group; **nothing is top-level**. docker joins the
other namespaces:

```just
mod? docker   'script/docker/justfile.docker'
mod? test     'script/test/justfile.test'
mod? release  'script/release/justfile.release'
mod? base     'script/base/justfile.base'
mod? template 'script/template/justfile.template'      # consumer only in practice
import? 'script/local/justfile.local'                  # repo-owned user groups
default:
    @just --list
```

`just build` becomes `just docker build`. The cost (longer invocations)
is accepted in exchange for one rule with no exceptions, and completion
(below) makes the extra token a single `<tab>`.

### 2. Action-named namespaces

| was (ADR-00000010) | now | rationale |
|---|---|---|
| `just build/run/...` (top-level) | `just docker build/run/exec/stop/prune/setup/setup-tui` | docker is the action group, no special case |
| `just ci` | `just test` | the action is "test"; **all** CI checks live here, incl. lint |
| `just cd` | `just release` | the action is "cut a release" |
| `init` / `upgrade` / `upgrade-check` (root scripts) | `just base init` / `just base upgrade [ver]` / `just base update` | manage the `.base` dependency; `update`/`upgrade` mirror apt (refresh-check vs apply) |

`lint` is **not** a top-level peer of `test`; it is `just test lint`
(a sub-action of the test namespace). A new top-level command would need
its own `justfile.<x>` + scripts; lint is part of testing, so it stays
inside `test`.

### 3. min->max coverage via `--option` narrowing

Every command runs the **maximum** scope bare and **narrows** through
`--long` / `-short` options -- never bare positional args whose meaning is
positional:

```
just test                       # everything (shellcheck + bats + ... + coverage as configured)
just test --file <path>         # one spec file
just test --filter <regex>      # specs matching a pattern
just test lint                  # all linters
just test lint --shellcheck [<level>]   # only shellcheck (optionally at a severity level)
just test lint --hadolint               # only hadolint
just docker build                       # default stage
just docker build --stage <name>        # a specific stage (base self-test: --stage test-tools)
just base upgrade                       # latest tag
just base upgrade --tag <vX.Y.Z>        # a specific tag
```

The single-file test mode (previously supported) is preserved as
`--file`. `test-tools` is built explicitly as
`just docker build --stage test-tools`; the test runner invokes it
internally rather than `build` growing a magic `test` argument.

### 4. Generic tooling, per-repo content, single source of truth

The whole `script/<ns>/` tree is **generic tooling with a single source of
truth**; only repo-specific *content* differs. Therefore:

- The **real files live in `dist/script/<ns>/`** (the shipped tree),
  which is the single source of truth. base-own **`script/<ns>/` symlinks
  into `dist/script/<ns>/`** so base uses the very tooling it ships,
  with no duplicate base-own copy. A consumer's **`script/<ns>/` symlinks
  into `.base/dist/script/<ns>/`** -- a **single hop** to the real
  file. (Per-sub symlinks, not a single whole-`script/` symlink, so
  `script/local/` and `script/entrypoint.sh` can stay *inside* `script/`
  and remain repo-owned -- alignment is kept.)
- **Content is per-repo and never symlinked**: `test/` (specs),
  `config/`, `Dockerfile`, `compose.yaml`. base has its own
  (`test/{unit,integration,behavioural}`, `Dockerfile.test-tools`,
  base `compose.yaml`); a consumer has its own (`test/smoke/`, app
  `Dockerfile`).

**Origin-direction is build-verified (corrected 2026-06-23).** The
opposite direction -- real files in base `script/<ns>/`, with
`dist/script/<ns>/` as a *directory* symlink back -- was tested and
rejected: it makes the consumer wrapper symlinks (`<repo>/script/build.sh
-> .base/dist/script/docker/wrapper/build.sh`) a **two-hop** chain
(file symlink through a directory symlink), and BuildKit does **not**
resolve that at `COPY` time. The required lint copy `COPY script/*.sh
/lint/` then fails with `"/script/build.sh": not found`. (A single
directory-symlink path such as `COPY .base/dist/script/docker/lib
/lint/lib` *does* resolve; only the two-hop chain fails.) Keeping the real
bytes at the `dist/` path the consumer references makes every
consumer symlink single-hop -- the shape already proven in CI -- and
leaves the consumer Dockerfile COPY paths and the ADR-00000006 Region C
`upgrade.sh` paths **unchanged**. For docker this is exactly today's
on-disk layout, so #654 is not a file move but the addition of the
base-own `script/<ns>` symlinks plus the consumer per-sub symlinks.

**Amended 2026-06-24 (#654).** The base=origin symlink-unification this
section describes turned out to be **N/A in practice -- there is no
duplicated tooling to unify**. Audit of the tree found: the real docker
files already live single-copy at `dist/script/docker/`; base-own
`script/test/` + `script/release/` are base's OWN self-test / skeleton
tooling (not shipped copies of a downstream original); and the consumer
entry mods only `dist/.../template`. So there is no second copy of
any namespace to collapse into a symlinked origin. What #654 actually did
was the narrow, real change hiding inside this section's premise: relocate
`init.sh` + `upgrade.sh` out of the subtree root into
`dist/script/base/` (the §8 move), with `upgrade.sh`'s self-location
rewritten to a walk-up so the `git subtree pull --prefix=` stays `.base`.
The per-sub symlink wiring for namespaces remains as designed where a
genuine origin/consumer split exists; it was simply not a
deduplication.

### 5. Generic test runner: dispatcher + per-tool drivers

`script/test/` is a dispatcher (`test.sh`) plus one **driver per tool**
(`drivers/{bats,shellcheck,hadolint,...}.sh`); adding a tool is a new
driver + a folder, the dispatcher is untouched. The dispatcher adapts to
the **content present** using the **same** tools everywhere.

The `test/` content is laid out **tool-first** -- `test/<tool>/<category>/`
for specs, `test/lint/<tool>/` for linters -- which **supersedes
ADR-00000004** (category-first); see ADR-00000012 for that decision and
its trade-offs. Detection and execution environment:

- `test/<tool>/<category>/` present -> run that tool's driver. The
  execution environment depends on the **category**:
  - `smoke` -> inside the built `*-test` image stage (devel-test /
    runtime-test) -- it tests the real image;
  - `unit` / `integration` / `behavioural` -> in the test-tools toolchain
    container -- it tests scripts/logic.
- `test/lint/<tool>/` present -> run that linter with its config
  (shellcheck over repo scripts, hadolint over the Dockerfile).
- `--coverage` runs kcov; `--file` / `--filter` narrow the specs.

base (bats unit/integration/behavioural, no app devel-test) runs those in
the toolchain container; a consumer (smoke + a Dockerfile) builds + smokes
in-image. **One dispatcher, the per-tool folders decide.** `just test`
uses the **pinned prebuilt test-tools image** by default and rebuilds it
locally only when missing or explicitly requested, by internally calling
`just docker build --stage test-tools` (no rebuild per run).

### 6. `--help` everywhere; `--lang` for human-facing namespaces only

`just` (1.52) has no native `--lang` and does not pass a flag to a
**namespace** (`just docker --help` / `just docker --lang ja` error -- the
flag is parsed as part of the recipe path, even when the module `default`
takes `*args`). So "`--lang` flag at every level" is not literally
achievable; the mechanism is (verified):

- **recipe** (`just docker build`): `--help` and `--lang <code>` are
  forwarded to the backing script via `{{args}}` and parsed there (the
  docker wrappers already do this).
- **namespace** (`just docker`): help is `just <ns>` (bare invocation runs
  the module `default`, which lists) **or** the explicit `just <ns> help`
  recipe (`just <ns> h` alias) every shipped module now carries (#789). The
  dashed `just <ns> --help` does not work -- a dashed name cannot be a
  recipe/alias, so it is not intercepted; with a `help` recipe present `just`
  emits a `Did you mean 'help'?` hint instead of a bare error.
- **entry** (`just`): `just --list` / a localised overview.
- Language at the namespace/entry level comes from the `SETUP_LANG` /
  `LANG` **env** (which `i18n.sh _resolve_lang` already honours), not a
  flag.

**i18n scope -- "anything human-facing".** Localised strings + `--lang`
apply only to the human-facing namespaces: **`docker`, `base`,
`template`**. **`test` and `release` are English-only** (machine / CI /
automation). Help exists at every level (English baseline) regardless, but
via level-specific forms, not a uniform `--help` flag (#789): recipe help is
`just <ns> <recipe> --help` (forwarded to the backing script); namespace help
is `just <ns>` or the `just <ns> help` recipe (`h` alias) -- the dashed
`just <ns> --help` is a documented `just` dispatch limitation that yields a
`Did you mean 'help'?` hint. Every shipped recipe accepts `-h|--help`; where a
recipe hardcodes its args (e.g. `base update`, which always runs the check) a
small shim forwards `--help` to the backing usage without running the action.

The namespace `default` help and all recipe scripts share **one CLI
runtime lib** -- this is #565's `lib/wrapper.sh` runtime (arg pre-pass,
`--help` rendering, `_resolve_lang`), extended beyond the docker wrappers
to the `test`/`release`/`base`/`template` scripts; its lang/i18n portion
is used only by the human-facing namespaces. **#655 therefore depends on /
shares #565.**

### 7. Opt-in completion installer (no host pollution)

Because the distro `just.fish` lists only top-level recipes and does not
drill into namespaces, base ships `just base completions install [--shell
bash|zsh|fish|all]` and `just base completions uninstall`. It writes the
**dynamic** `clap_complete` loader (not a static snapshot, so it tracks
recipes/namespaces and survives upgrades; `just --completions <shell>`
itself now just emits `eval "$(JUST_COMPLETE=<shell> just)"`). All three
shells share one engine and drill identically -- `just docker::<tab>` ->
`build exec run` (verified); display is each shell's standard (bash plain
list, zsh/fish show recipe descriptions).

Per-shell target (auto-load dir, no rc edit):

- bash: `${XDG_DATA_HOME:-~/.local/share}/bash-completion/completions/just`
- fish: `${XDG_CONFIG_HOME:-~/.config}/fish/completions/just.fish`
- zsh: `~/.local/share/zsh/site-functions/_just`

bash/fish never touch the rc (uninstall removes the file). zsh's
completion must sit in `fpath`; if the target dir is not in `fpath` the
installer **prints** the one line to add it and **never edits `.zshrc`**.
`--shell` defaults to the detected current shell; install/uninstall are
idempotent. README documents this as the prerequisite for namespace tab
completion.

### 8. `init.sh` / `upgrade.sh` leave the root (amends ADR-00000006)

**Done 2026-06-24 (#654).**

`init.sh` and `upgrade.sh` move into the `base` namespace's tooling. Per
§4 the real files live in `dist/script/base/` (the shipped source of
truth) and base-own `script/base/` symlinks into it. They back
`just base init` / `just base upgrade` / `just base update`.

Implementation note: because the scripts no longer sit at the subtree
root, each rewrote its self-location from `dirname $BASH_SOURCE` to a
**walk-up** to the subtree root -- the directory carrying the `.version` +
`dist/` markers. `upgrade.sh` `basename`s that root for the
`git subtree pull --prefix=` flag (resolves to `.base`, NOT the script's
own deep dir `base`); its `_lib.sh` source and the Step-3 `init.sh` call
were repointed to the deep paths in the same slice. An integration test
(`upgrade_spec.bats`) drives a real git-subtree fixture and asserts the
captured `--prefix` is `.base`.

- **Region A** (ADR-00000006/00000010 froze `.base/init.sh` at root) is
  **superseded**: the bootstrap path becomes
  `.base/dist/script/base/init.sh` (a brand-new consumer's documented
  one-time bootstrap command updates accordingly; the wrapper-first rule
  from ADR-00000005 means steady-state users call `just base ...`, not the
  raw script).
- **Regions B/C** keep their ADR-00000010 `dist/` locations.
- `upgrade.sh`'s self-referential and frozen-path constants move in the
  same slice that relocates the script, per ADR-00000006's lockstep
  discipline.

**Amended 2026-06-26 (#719).** The walk-up self-location has a failure mode:
run RAW from inside the base repo itself (`./dist/script/base/init.sh`, not
via a `.base/` subtree), the walk-up resolves base's OWN root as the subtree
root (it carries `.version` + `dist/`), so `REPO_ROOT` becomes base's PARENT
dir and `init.sh` silently scaffolds a repo there. A shared guard
`lib/template_guard.sh` (`_assert_not_template_source`) now refuses when the
resolved subtree root carries `.git`: a vendored `.base/` subtree never does
(the consumer's `.git` lives at the repo root, outside the subtree), but the
base checkout/worktree has `.git` at the subtree root. The discriminator does
NOT hardcode the subtree basename, preserving the rename contract; a
git-remote match (fork/CI/rename-fragile) and a CONTEXT.md sentinel (shipped
into `.base/`, indistinguishable) were rejected. `init.sh` is wired now;
`upgrade.sh` (the symmetric raw-path hole) is tracked in #719's follow-up.

A base-root **convenience bootstrap symlink** (`.base/init.sh` ->
`dist/script/base/init.sh`, to shorten the one-time `./.base/dist/script/base/init.sh`)
was considered and **rejected**: it partially reverts THIS section's
relocation (which removed root-level scripts as "an eyesore" that breaks
the every-action-lives-in-a-namespace rule), the saving is trivial (a
one-time command copy-pasted from the README, not hand-typed), and it makes
accidental in-base self-run easier. The raw bootstrap command stays the deep
path; steady-state stays `just base init`.

## Final command list

```
just                              # list
just docker  build [--stage <s>] | run [-d] | start | exec [-t <svc> -- <cmd>]
             | stop | prune | setup | setup-tui
just test    [--file <f>] [--filter <re>]
just test    lint [--shellcheck [<level>] | --hadolint]
just test    coverage | behavioural
just release [--tag <vX.Y.Z>] [...]
just base    init | update | upgrade [--tag <vX.Y.Z>]
             | completions install [--shell <sh>] | completions uninstall
just template new <name>          # consumer: scaffold a repo-local group
just <group> <recipe>             # consumer repo-local groups
# every level: --help, --lang <code>
```

## Consequences

- **Breaking again for consumers**, on top of ADR-00000010: `just build`
  -> `just docker build`, `just ci` -> `just test`, `just cd` ->
  `just release`, root `init.sh`/`upgrade.sh` -> `just base ...`. The
  fanout slice re-inits every downstream repo; the bootstrap doc path
  changes. Justified: it buys one rule with zero special cases, which is
  cheaper to teach and to extend than the mixed model.
- **Tab completion becomes a documented opt-in step**, not automatic --
  accepted to avoid touching the host shell config without consent.
- **One test runner** removes the base-vs-consumer tooling fork; the cost
  is a content-detecting runner (a branch on what `test/` contains), which
  is deliberately *not* counted as a "special case" because it is one file
  with one interface, not divergent command surfaces.
- Lands as a revision epic of thin slices, each gated by the base
  self-test, superseding the not-yet-fanned-out parts of ADR-00000010's
  epic.

## Alternatives

- **Keep docker top-level for ergonomics.** Rejected: the special case is
  exactly what made the model hard to extend and teach; completion
  recovers most of the ergonomic loss.
- **`lint` as a top-level peer of `test`.** Rejected: lint is a CI check,
  so it belongs under `test`; a top-level peer would re-introduce the
  "which actions are bare" ambiguity and need its own justfile + scripts.
- **Bare positional args (`just test foo.bats`).** Rejected in favour of
  `--file` / `--filter`: explicit options scale uniformly from min to max
  and self-document; positional meaning does not.
- **Separate base-own vs consumer test tooling.** Rejected: the tools are
  identical and only content differs, so a generic runner keeps the whole
  `script/` tree a single symlinked origin (no duplication, no drift).
- **Auto-install completions on `init`.** Rejected: writing to the host
  shell config without explicit consent is host pollution; made an opt-in
  `just base completions install` instead.


## ---- FILE: doc/adr/00000012-tool-first-test-layout.md ----

# Tool-first `test/<tool>/<category>/` layout + per-tool test runner

> Serves: PRD invariant 7 (rigorous test bar) -- tool-first test layout;
> supersedes ADR-00000004.

- **Date:** 2026-06-23
- **Status:** Accepted
- **Supersedes:** ADR-00000004 (category-first `test/<category>/<tool>/`)
- **Relates to:** ADR-00000011 §5 (the generic test runner that consumes
  this layout)

> **Amendment (#781, 2026-06-30):** The *category vocabulary* used below
> (`{smoke, unit, integration, behavioural}`) is superseded by
> ADR-00000018 (ISTQB-aligned taxonomy): `behavioural` -> `system`, a new
> `acceptance` level is added, and `smoke` is reclassified as a build-time
> *type* (it keeps its own directory). The **tool-first** decision of this
> ADR -- `test/<tool>/<category>/` for specs and `test/lint/<tool>/` for
> linters, one driver per tool subtree -- **still stands**; only the set of
> category names *inside* `test/<tool>/` changes. Read the directory
> examples below as `unit / integration / system / acceptance / smoke`.

## Context

ADR-00000004 chose a **category-first** test layout
(`test/<category>/<tool>/`, e.g. `test/unit/bats/`) and explicitly
rejected tool-first, to keep the TDD four-axis view (smoke / unit /
integration / lint) a single directory walk and let `TEST.md` organise by
category.

ADR-00000011 reworks the test entry into a **dispatcher + one driver per
tool** (`script/test/drivers/{bats,shellcheck,hadolint,...}.sh`). With
that structure the natural unit of ownership is the *tool*: each driver
wants one subtree it owns end-to-end. Category-first fragments every
tool's files across the category directories, so a driver must walk every
category to collect its own specs, and the base/consumer shapes diverge
(single-tool repos stay flat, multi-tool repos sublayer). The layout and
the runner pulled in opposite directions.

## Decision

Lay `test/` out **tool-first**: `test/<tool>/<category>/` for specs and
`test/lint/<tool>/` for linters. The tool layer is always present, so base
and consumer shapes match.

```
test/
  bats/
    smoke/  unit/  integration/  behavioural/
  pytest/                 # only if the repo uses it
    smoke/  unit/  ...
  lint/                   # lint group, per-tool
    shellcheck/  .shellcheckrc / scope
    hadolint/    .hadolint.yaml
```

- **One driver, one subtree.** `script/test/drivers/<tool>.sh` owns
  `test/<tool>/` (or `test/lint/<tool>/`), 1:1. Adding a tool = a driver +
  a folder; the dispatcher is untouched.
- **Execution environment is decided by the category, not the tool**
  (per ADR-00000011 §5): `smoke` runs inside the built `*-test` image
  stage (it tests the real image); `unit` / `integration` / `behavioural`
  run in the test-tools toolchain container.
- **Lint is per-tool too.** Each linter has `test/lint/<tool>/` holding
  its config; `just test lint` runs all, `just test lint --shellcheck
  [<level>] | --hadolint` runs one. Lint configs move under
  `test/lint/<tool>/` -- notably `.hadolint.yaml` leaves
  `dist/.hadolint.yaml`, and the consumer Dockerfile lint-stage
  COPY, `self-test.yaml`'s hadolint `config:`, and any init/upgrade
  references update in lockstep.
- **base migrates** `test/{unit,integration,behavioural}` ->
  `test/bats/{unit,integration,behavioural}`.

## Consequences

- The "what unit tests exist" query is now a walk across every tool
  (`test/*/unit`), and `TEST.md` reassembles the category view across
  tools -- the exact cost ADR-00000004 set out to avoid. Accepted: the
  per-tool driver model is the dominant organising force now, and the
  category view is recoverable by a glob.
- base/consumer test trees share one shape (tool layer always present),
  removing ADR-00000004's flat-vs-sublayer divergence.
- `lint_mixed_test_layout.sh` (#495), which warned when a
  `test/<category>/` mixed runner families, is repurposed/retired: under
  tool-first a category dir never holds two tools (the tool is the parent),
  so the mixing it guarded against cannot occur.

## Alternatives

- **Keep category-first (ADR-00000004).** Rejected: it fights the per-tool
  driver model, forcing every driver to walk all categories and keeping
  base/consumer shapes divergent.
- **Linters as top-level tool dirs (`test/shellcheck/`, `test/hadolint/`)
  instead of a `test/lint/` group.** Rejected: grouping the linters under
  `test/lint/` keeps the TDD "lint" axis legible as one place while still
  separating per tool inside it.


## ---- FILE: doc/adr/00000013-no-transient-issue-refs-in-code-comments.md ----

# Strip transient issue numbers from code comments; keep ADR refs + what/why prose

> Serves: PRD invariant 2 (never fail silently) -- the issue-ref comment
> lint is one of its enforcing guards; mechanism.

- **Date:** 2026-06-24
- **Status:** Accepted
- **Relates to:** the `doc/adr/` references that this convention
  deliberately preserves

## Context

The historical convention threaded inline issue numbers (`#440`,
`#216 / #429`, `#414/#448/#469`, `refs|closes|fixes #N`) into code
comments across `base` -- in `.sh`, `justfile*`, `compose.yaml`,
`Dockerfile*`, and the `#`-comments inside `.bats` setup/helper code.
The #573 review surfaced how pervasive this had become and how little it
buys: an inline `#N` is a frozen pointer to a transient artifact. The
issue gets closed, renumbered across a repo move, or superseded, and the
comment now points at stale context while still costing a reader the
mental "go look that up" tax on every pass.

There is a more reliable traceability chain that does not rot:
`git blame -> commit -> PR -> issue`. blame is recomputed against the
live tree on every read, so it never goes stale the way a hard-coded `#N`
does. The comment's job is to say *what* the code does and *why*; the
*which-ticket* dimension is recoverable from history when (rarely) needed.

ADR references are the opposite case. `ADR-0000xxxx` is durable, curated
rationale that we maintain deliberately; an inline ADR anchor is exactly
what makes future code-tracing cheap, so keeping it offsets the cost this
convention otherwise introduces.

## Decision

Code comments in `base`'s shipped code do **not** carry transient issue
numbers. Specifically, in `.sh`, `justfile*`, `compose.yaml`,
`Dockerfile*`, and the `#`-comments of `.bats` files:

- **Strip** inline transient refs from comment text: bare `#NNN`,
  `(#NNN)`, `refs|closes|fixes #NNN`, marker forms
  (`# -- #216 / #429: auto-build gate --` -> `# -- auto-build gate --`),
  and rationale forms (`# #546: the root user entry ...` ->
  `# the root user entry ...` -- drop the number, keep the sentence).
  Collapse separators / double spaces the removal leaves behind.
- **Keep** `ADR-0000xxxx` references anywhere they appear.
- **Keep** all what/why prose; only the bare issue number goes.

The following are explicitly **not** issue references and are left
untouched:

- `@test "..."` description strings -- these are test identities mirrored
  in `TEST.md`; a `(#NNN)` inside a `@test` name is part of the test's
  name, not a comment, and rewriting it would churn `TEST.md` for no
  gain.
- Functional string literals, registered log-event names, hadolint /
  shellcheck directive codes (`DL3007`, `SC1090` -- not issue refs),
  version tags (`v0.41.0`), and URLs.
- Issue references inside non-comment code (e.g. a `#NNN` inside a
  `printf`/`_log_*` string the program emits at runtime).

A lint driver (`script/test/drivers/issueref.sh`, wired into `just test`
and `just test lint`) enforces this so the refs cannot creep back in.

## Out of scope

Issue references stay in commit messages, PR bodies, `CHANGELOG`,
`doc/adr/` prose (including this ADR), and the gh-artifact-format docs --
those artifacts are *about* the tickets and the references are
intentional there. Downstream repos' own comments are handled separately;
base comments propagate into `.base/` via the subtree and ride along with
the upgrade / fanout.

## Consequences

- Tracing a comment back to its originating ticket now costs one extra
  hop (`git blame` the line -> read the commit / PR -> follow to the
  issue) instead of reading an inline `#N`. This is the accepted
  tradeoff: blame does not go stale, inline numbers do, and the everyday
  reader -- who is reading *what/why*, not *which ticket* -- pays nothing.
- Comments are shorter and read as specifications of behaviour rather
  than as change-logs.
- The `issueref` lint makes the convention enforceable rather than
  aspirational; a reintroduced `#N` in a comment fails `just test`.

## Alternatives considered

- **Keep inline `#N` for traceability.** Rejected: the inline pointer
  rots (close / rename / supersede) while `git blame` does not, so the
  "traceability" it offers is the unreliable half of the pair.
- **Strip everything, including ADR refs.** Rejected: ADR anchors are
  durable curated rationale, not transient tickets; the inline anchor is
  the cheap-tracing affordance worth keeping.
- **Convention without a lint.** Rejected: an unenforced style convention
  silently regresses; the lint is what makes the acceptance criterion
  hold over time.


## ---- FILE: doc/adr/00000014-decompose-setup-sh-into-subsystem-libs.md ----

# Decompose setup.sh into subsystem libs (relocate-first, tracer-bullet order)

> Serves: mechanism -- setup.sh decomposition into subsystem libs
> (architecture / testability); no invariant.

- **Date:** 2026-06-27
- **Status:** Accepted
- **Relates to:** epic #745 (slices #746 deploy, #747 compose, #748
  subcommands, #749 infra cleanup); the test-layout audit that surfaced it;
  ADR-00000012 (tool-first test layout); #565 (lib/wrapper.sh extraction
  precedent); #568 (explicit lib load-order)

## Context

`dist/script/docker/wrapper/setup.sh` had grown to 5133 lines and ~90
functions spanning ~10 distinct concerns: host detection, conf access,
name/path resolution, value resolvers, dockerfile/stage handling, the deploy
generator, compose emission, env writing, drift checks, and the user-facing
`set/show/list/add/remove/reset/apply/deploy` subcommands. It is sourced by
every container-ops wrapper.

A 2026-06-27 test-file granularity audit (informed by cross-ecosystem
convention research: Go/pytest/Jest/JUnit/RSpec/bats) found setup.sh is the
ROOT of the suite's structural problems: it is tested by 11 spec files
(~614 tests), produces a name/unit mismatch (`deploy_spec.bats` tests deploy
code that has no `deploy.sh`), and seeds several of the 8 oversized
"god-test-files". A perf symptom landed the same week: `_resolve_deploy_context`
re-parsed the conf 10x per call (#742) -- the kind of issue a god-source hides.

The research consensus: test-file granularity should mirror the UNIT under
test, and when the source is a god-file the principled fix is to split the
SOURCE first (with the existing tests as the safety net); the test split then
falls out one-to-one.

## Decision

Decompose setup.sh into cohesive subsystem libs so it becomes a thin
orchestrator, under these rules:

1. **Relocate into existing libs first; create new libs only for the
   homeless.** `lib/compose.sh`, `lib/conf.sh`, `lib/dockerfile_migrate.sh`,
   and `lib/schema.sh` are already the established seams; the matching code
   that leaked into setup.sh belongs there. New files are created only for
   blocks with no existing home -- `lib/deploy.sh` (deploy generator) and
   `lib/setup_cmd.sh` (subcommands). We do NOT introduce a parallel
   `setup_*.sh` namespace that duplicates seams that already exist.

2. **Tracer-bullet order.** deploy generator first (smallest cohesive block,
   homeless so the cleanest extraction, just-touched in #742, and it fixes the
   deploy_spec name/unit mismatch), then compose emission, then subcommands,
   then a final shared-infra cleanup. The first slice proves the mechanics
   (load-order, spec re-source, this ADR) before the larger, riskier blocks.

3. **One slice = one issue = one PR; behaviour stays identical.** Each slice is
   a pure relocation guarded by the existing specs as a regression net; no
   behaviour change. The spec file follows its source (re-source / rename to
   mirror the new lib). Cross-file function calls resolve at runtime via the
   established load-order (#568), so a moved block does not need to re-source
   its still-resident dependencies; isolated unit specs source the deps they
   need explicitly.

## Consequences

- setup.sh shrinks toward a thin `main` + wiring; each concern gains locality
  (its change/bug/knowledge concentrate in one lib) and a one-to-one mirroring
  spec, shrinking the god-test-files.
- The 11-spec sprawl over setup.sh resolves as the source moves out.
- Short-term churn: several PRs touching a core file; mitigated by the
  one-slice-per-PR discipline and the existing test net.
- Risk: setup.sh is sourced by all wrappers; a botched relocation could break
  every container op. Mitigated by behaviour-identical relocation + full
  `just test` (incl. kcov) green per slice.

## Alternatives considered

- **All-new `setup_*.sh` namespace** (ignore existing libs): rejected -- it
  duplicates seams (`lib/compose.sh` etc. already exist) and fights the #565
  direction.
- **Big-bang single PR**: rejected -- too risky on a core file; no incremental
  proof; unreviewable diff.
- **Split the test files only, leave setup.sh**: rejected -- mirrors the
  physical file, not the units; leaves the god-source (and its perf/locality
  costs) in place. The research is explicit that splitting the source is the
  principled fix when the source is the god-file.
- **Leave setup.sh as-is**: rejected -- it is the measured root of the suite's
  granularity problems and a recurring perf/locality hazard.

## Amendment (#747): compose emission -> lib/compose_emit.sh, not lib/compose.sh

The compose slice found that `lib/compose.sh` is the `docker compose`
INVOCATION wrapper + project naming (`_compose` / `_compose_project` /
`_compute_project_name`), a distinct concern from compose.yaml GENERATION. The
~1200-line emission block (`_emit_*`, `generate_compose_yaml`, the volume/device
classifiers) therefore landed in a NEW `lib/compose_emit.sh` rather than being
merged into the invocation wrapper. This is consistent with the
"new lib only for the homeless" rule -- emission had no existing home, since
compose.sh's home is invocation -- it just refines the slice's earlier
"into lib/compose.sh" wording.

## Amendment (#749): the infra-cleanup slice was delivered as four sub-PRs

The "shared base / infra cleanup" slice (#749) was too large to land as one PR
(it carried setup.sh from ~1949 lines to a thin orchestrator), so it shipped as
four behaviour-identical relocation sub-PRs, each its own issue-less `Refs #749`
PR with the existing specs as the regression net; the last closes #749:

- **749a** -> `lib/setup_detect.sh` (host detection + name/path resolution)
- **749b** -> `lib/setup_conf.sh` (the setup.conf accessors)
- **749c** -> `lib/stage.sh` (multi-stage Dockerfile + per-stage overrides)
- **749d** -> `lib/resolve.sh` (mode+detection resolvers + conf hash),
  `lib/env_emit.sh` (.env generation), `lib/drift.sh` (drift detection)

Two refinements to the original plan, both consistent with the #747 precedent:

- **.env generation -> `lib/env_emit.sh`, not `lib/env.sh`.** `lib/env.sh` is
  the runtime `.env` READER (`_load_env`) every wrapper sources; `write_env` /
  `_scaffold_env_overlay` are the GENERATORS, used only at setup time. Same
  emission-vs-invocation split as compose_emit.sh vs compose.sh -- the
  generators land in a new `lib/env_emit.sh` rather than polluting the reader.
- **setup.sh's final shape.** After 749d it retains only the `_setup_msg*`
  message catalog, `usage`, and `main` (the subcommand dispatcher) -- a thin
  orchestrator over the subsystem libs, exactly the decomposition's goal.


## ---- FILE: doc/adr/00000015-test-files-mirror-source-not-the-reverse.md ----

# Test files mirror source files; source structure never follows tests

> Serves: PRD invariant 7 (rigorous test bar) -- test files mirror
> source; mechanism.

- **Date:** 2026-06-27
- **Status:** Accepted
- **Relates to:** ADR-00000012 (tool-first `test/<tool>/<category>/`
  layout -- this ADR governs file granularity *within* a category dir),
  ADR-00000008 (sharded coverage PR gate -- the per-file shard floor this
  convention helps lower), ADR-00000014 (the setup.sh decomposition that
  produced the libs these specs now mirror)

## Context

ADR-00000012 fixed *where* test files live (`test/<tool>/<category>/`).
It did not fix *how a test file maps to the source it covers*. After the
setup.sh decomposition (ADR-00000014) split one god-source into nine
subsystem libs, the tests still sat in a handful of god-test-files
(`setup_spec` 146 tests, `setup_emit_spec`, `compose_gen_spec`, ...) that
each spanned several libs. Two forces converged on needing a rule:

1. **Navigability / locality.** A reader looking for `resolve.sh`'s tests
   had to grep inside `setup_spec.bats`; a lib and its spec had no name
   correspondence.
2. **The coverage shard floor.** kcov instruments each spec **file** as
   one atomic unit, so a file cannot be split across shards. The longest
   single spec file is therefore the hard floor on the slowest coverage
   shard regardless of shard count (measured: `deploy_spec` 97s set the
   floor; the slowest shard was ~170s = that floor plus packed
   neighbours). Finer, source-aligned files give the partitioner smaller,
   more balanceable units.

The tempting shortcut -- when one source file needs more than one test
file (for granularity or to test distinct sub-units) -- is to split the
**source** so each spec gets a 1:1 source file. That lets tests dictate
source structure. We reject it.

## Decision

**Test files mirror source files. Source structure is decided by design,
never by the number or shape of test files.**

Concretely, within a `test/<tool>/<category>/` directory:

- **One source file (lib) maps to one spec by default**, with name
  correspondence: `lib/<name>.sh` <-> `<name>_spec.bats` (flat, mirroring
  the flat `lib/`).
- **A lib that genuinely needs multiple sub-unit specs gets a `<name>/`
  folder** named after the source file; the sub-specs live inside it
  (`<name>/<subunit>_spec.bats`). The folder -- not a renamed flat file --
  is what restores alignment when a single source file has several test
  units. The folder's *presence* signals "this lib has multiple test
  units"; single-spec libs stay flat (no over-structuring), exactly as
  pytest / RSpec only foliate a module when it has multiple test files.
- **Never split a source `.sh` to achieve 1:1 test alignment.** Source
  structure follows the deep-module principle (a small interface over its
  private implementation helpers; see the architecture LANGUAGE). Splitting
  a generator's private `_emit_*` helpers into their own file just to give
  them their own spec exposes implementation across a file seam and makes
  the module shallower -- the tail wagging the dog.
- **Integration / end-to-end tests live with the orchestrator they
  exercise, not with a leaf lib.** A test that drives a whole pipeline
  (e.g. `setup apply`: detect -> resolve -> write_env -> drift) belongs in
  the orchestrator's spec (`setup_spec`), because that *is* what it tests.
  Only isolated single-unit tests move out to the leaf lib's spec.

The shard partitioner globs specs recursively (`test/<tool>/<cat>/**/*_spec.bats`)
so foldered sub-specs are first-class shard units -- a `<lib>/` folder
costs nothing for balancing; each file inside is still its own kcov unit.

## Consequences

- Every subsystem lib has a name-corresponding spec (or `<lib>/` folder),
  so "where are X's tests" is answerable from the lib name alone.
- The coverage shard floor drops as god-test-files split into
  source-aligned units; foldering (not source-splitting) handles libs that
  need several specs, so coverage granularity never pressures source
  cohesion.
- A mild asymmetry remains -- most libs have a flat `<lib>_spec.bats`, a
  few have a `<lib>/` folder. This is intentional and meaningful (folder ==
  multiple test units), matching the pytest / RSpec norm.
- Future test work, in base and downstream, must align to this rule. A
  lint check that flags a spec whose name matches no source file (or a
  source file with no spec) is a natural follow-up enforcement.

## Alternatives

- **Split the source file so every spec is 1:1 with a `.sh`.** Rejected:
  lets test-file count drive source structure, exposing private
  implementation helpers across file seams and shallowing deep modules.
  Industry frameworks (pytest, RSpec) explicitly do not require 1:1
  source<->test and instead foliate a module into a folder of specs when
  needed -- which is the accepted form of this ADR.
- **Keep multi-concern god-test-files, balance shards by count/time
  only.** Rejected: a single oversized file is an irreducible shard floor
  under kcov's per-file atomicity (ADR-00000008), and the files stay
  un-navigable (no lib<->spec correspondence). Better partitioning cannot
  beat the longest-single-file floor.
- **Always foliate every lib into a `<lib>/` folder for uniformity.**
  Rejected: over-structuring -- most libs have one cohesive test unit and a
  flat `<lib>_spec.bats` is clearer. Folder only when multiplicity is real.


## ---- FILE: doc/adr/00000016-coverage-tooling-evaluation.md ----

# Coverage tooling: evaluate kcov alternatives to lift the per-file shard floor

> Serves: PRD invariant 7 (rigorous test bar) -- coverage tooling (a
> swappable mechanism); spike Rejected, kcov kept.

- **Date:** 2026-06-27
- **Decided:** 2026-06-29
- **Status:** Rejected
- **Relates to:** ADR-00000008 (sharded coverage PR gate, built on kcov),
  ADR-00000015 (test files mirror source -- the symptom-level lever),
  issue #758 (lower the coverage critical path)

> **Rejected (2026-06-29).** The time-boxed spike below disproved this
> ADR's central premise -- kcov's cost is not the ptrace tax the proposal
> assumed -- so no tool change is adopted and kcov stays. The Context and
> Decision below are the proposal as written; the Spike result section is
> what actually happened.

## Context

Coverage is an enforced PR gate run under **kcov** (ADR-00000008). kcov
collects coverage via **ptrace**, single-stepping the traced process. That
has two costs measured in this repo:

1. **Per-run overhead.** kcov roughly +60% wall-clock over plain bats
   (`deploy_spec` 57s plain -> 92s under kcov).
2. **Per-file atomicity for sharding.** Because each spec file is run as
   one kcov invocation (to amortise the ptrace launch cost), a file cannot
   be split across shards. The longest single spec file is the hard floor
   on the slowest coverage shard, which sits on the PR critical path.

The dynamic + time-weighted + cached shard work (#725/#724/#733) and the
conf parse-once perf (#742) halved the critical path (~409s -> ~208s total;
slowest shard ~381s -> ~176s). ADR-00000015 lowers the per-file floor by
splitting god-test-files into source-aligned units. Both treat the
**symptom**. The **root** is the tool: if coverage overhead were near
zero, coverage could fold back into the normal test pass and the whole
separate-sharded-coverage architecture could be retired.

## Candidate tools

| tool | mechanism | note |
|---|---|---|
| **kcov** (current) | ptrace | cobertura native; language-agnostic; the +60% / per-file constraint above |
| **bashcov** | bash xtrace (`DEBUG` trap / `PS4` via `BASH_XTRACEFD`), no ptrace | works with bats; auto-merges; SimpleCov-based, so cobertura needs `simplecov-cobertura`; DEBUG-trap has its own per-command overhead and known correctness edges around `set -e`, subshells |
| **DIY `PS4` + `BASH_XTRACEFD`** | own `DEBUG` trap recording line hits | lightest, fully in our control; must write our own report emitter |
| **ShellSpec** | own BDD framework with built-in parallelism | its coverage is itself kcov under the hood -- does not remove the root |

## Decision (pending -- this ADR is Proposed)

Before committing to any tool change, run a **time-boxed throwaway spike**
(the prototype workflow) measuring **bashcov** and a **DIY PS4** tracer
against kcov on 2-3 representative specs (the heavy `deploy_spec`, a light
one). The spike must answer three gating questions with numbers:

1. **Speed** -- is it materially faster than kcov's ptrace?
2. **Reporting** -- can it emit cobertura the existing gate / timings cache
   consume, or what replaces them?
3. **Fidelity** -- does it stay accurate under our `set -u`, subshells, and
   `local -n` patterns (no false coverage gaps / no crashes)?

Decide only on the spike's evidence:

- If a lighter tracer clears all three: adopt it, and re-evaluate whether
  the separate sharded-coverage job (ADR-00000008) can collapse into the
  normal test pass.
- If none clears the bar: keep kcov; ADR-00000015's source-aligned splits
  remain the available lever, and this ADR is marked Rejected with the
  spike numbers recorded.

This is intentionally sequenced **after** ADR-00000015's P1 (the
source-aligned re-split), which is low-regret regardless of the tool
outcome.

## Spike result (2026-06-29) -- REJECTED

Ran the time-boxed spike. It disproved the ADR's central premise.

**Environment / versions compared** (the baked `test-tools:main` image):

- image: `ghcr.io/ycpss91255-docker/test-tools:main`
- `kcov v43`, `Bats 1.13.0`, `GNU bash 5.2.37(1)` (x86_64-alpine-linux-musl)
- bashcov / DIY-PS4 not benchmarked: the image has **no ruby/gem**, and the
  mechanism finding below made the benchmark moot.

**Method.** Same test set both ways (`COVERAGE=1` so identical tests run),
kcov invoked exactly as `_run_coverage` does (`--include-path=<repo>`, the
same `--exclude-path` set). Single run per cell. plain = `bats --recursive
<spec>`; kcov = `kcov ... bats --recursive <spec>`.

**Data (kcov tax per spec):**

| spec | plain bats | kcov | overhead |
|---|---|---|---|
| `deploy_spec.bats` | 29.7s | 47.4s | **+60%** |
| `setup_detect_spec.bats` | 15.5s | 23.2s | **+50%** |

- Reporting: `cobertura.xml` is produced fine (Q2 satisfied -- but moot).
- **Key finding (Q1 answer):** kcov's output dir contained
  `bash-helper-debug-trap.sh` / `bash-helper.sh` -- **kcov v43 already
  instruments bash via a `DEBUG` trap, not ptrace.** That is the *same*
  mechanism bashcov and the DIY-PS4 tracer use. The ADR's framing ("kcov =
  heavy ptrace, bashcov = light xtrace") is wrong for the bash case.

**Conclusion.** The +50-60% is the intrinsic cost of per-line bash coverage
(a trap firing on every command), not a kcov-specific ptrace penalty. A
DEBUG-trap-based alternative (bashcov) runs the same mechanism, would not
materially beat it, and would add a ruby dependency to the test-tools image
-- net negative. A DIY-PS4 tracer shares the mechanism and would need a
hand-written cobertura emitter for single-digit-percent upside -- not worth
it. **Coverage is at its structural floor; kcov stays.** The remaining
total-CI lever is the arm64 `integration-e2e` QEMU pole (native runners,
refs #587/#579), not the coverage tool.

## Consequences (if adopted)

- A coverage tool swap touches the test-tools image (currently bakes
  kcov), the gate's cobertura parser, and the `.shard-weights` timings
  cache -- an ADR-00000008-level change, hence the spike-first gate.
- A near-zero-overhead tracer could remove the dedicated coverage shards
  entirely, simplifying `self-test.yaml` and erasing the per-file floor as
  a concern -- the largest available structural win, but the riskiest.

## Alternatives

- **Do nothing; live with kcov.** Viable -- the symptom-level levers
  (sharding + ADR-00000015) already keep the gate within budget. This ADR
  exists because the user asked whether the constraint can be removed at
  the root, not because the gate is currently failing.
- **Skip the spike, swap to bashcov directly.** Rejected: bashcov's
  DEBUG-trap overhead and `set -e`/subshell fidelity are unproven for our
  code; swapping blind risks a slower or less accurate gate.


## ---- FILE: doc/adr/00000017-ci-throughput-ceiling-and-shard-runner-strategy.md ----

# CI throughput ceiling (free + public) and the shard / runner strategy

> Serves: PRD invariant 7 (rigorous test bar) -- CI throughput / shard
> strategy; a swappable mechanism, not the invariant.

- **Date:** 2026-06-29
- **Status:** Accepted
- **Relates to:** ADR-00000008 (sharded coverage PR gate), ADR-00000016
  (coverage tooling kept as kcov), issue #758 (CI-squeeze work), issue #766
  (self-hosted same-repo guard)

## Context

The self-test PR critical path is ~3m. A throughput grill set out to "push CI
to the limit" and to decide how the coverage shard count should be managed
(today a static `vars.CI_SHARDS`, default 8). The investigation produced
hard, API-verified constraints that bound what is achievable, so they are
recorded here to stop the topic being re-litigated.

### Verified constraints (measured / API-checked, not assumed)

- **Plan = GitHub Free -> 20 concurrent jobs, org-wide** (shared across every
  repo in the org). Observed peak in one self-test run: 15 concurrent (8
  coverage shards + ~7 other jobs).
- **GitHub-hosted exposes NO capacity / idle / remaining-slot API.** Direct
  checks: `…/actions/runner-limits` -> 404 (the field-returning endpoint some
  blogs cite does not exist), `…/actions/hosted-runners` -> 404 "not supported
  for this organization" (that is the paid larger-runner feature),
  `…/settings/billing/actions` -> 410 Gone. The 20-cap is enforced
  server-side and cannot be queried at runtime.
- **kcov coverage is serial / single-threaded per process.** Measured: a full
  unsharded `just test coverage` on the org's 32-core self-hosted runner took
  **522s (~8.7 min)** for the same 2135 tests. Extra cores do not speed a
  serial kcov run. Therefore **sharding is not removable** -- dropping it
  returns CI to ~8.7 min (~3x slower than the sharded ~3 min).

  > Corrected (#1060): the CONCLUSION holds, the reason given for it does
  > not. That run was serial for a second reason nobody had noticed -- the
  > bats underneath kcov had no `--jobs`, because `_run_coverage` was the
  > one bats invocation in the driver that never received the flag
  > (ADR-00000008's #1060 amendment). A
  > coverage SHARD is now parallel underneath its kcov and 1.9x-3.1x
  > faster with a byte-identical line set, so "extra cores do not speed a
  > serial kcov run" describes the invocation of the day, not the tool.
  > Sharding stays non-removable on a different and stronger ground: the
  > full-suite run must stay serial, because at that volume the single
  > kcov parser drops trace data and the reported figure moves (measured;
  > see the amendment). Per-process single-threadedness -- what #726
  > addresses -- is unaffected by either finding.
- **The two co-equal poles.** Slowest coverage shard ~155s and native arm64
  `integration-e2e` ~154s run in parallel; total is bounded by the larger.
  Cutting only one pole does not move the total (the other still sits at
  ~155s) -- they must be cut together.
- **Self-hosted reality.** The org has ONE self-hosted runner (32-core, GPU,
  org-level, currently unused by CI). Self-hosted `status`/`busy` ARE
  queryable. base is a PUBLIC repo with `fork-pr-contributor-approval =
  all_external_contributors` and zero fork PRs in history.

## Decision

1. **Shard count is auto-derived by ONE mechanism, not a hand-maintained
   number and not per-environment parameters.** `compute-shards` emits a
   single N consumed by a single matrix:
   - GitHub-hosted: `N = concurrency_budget = cap (20) - reserved_other_jobs
     (~7) ~= 12`. A *derived constant* -- it does not float (the cap pins it),
     but no human tunes it; it only shifts if the cap or the job set changes.
   - Self-hosted: `N = idle-runner / core budget` -- genuinely dynamic and
     queryable.
   - `vars.CI_SHARDS` remains the SINGLE optional override (applies in any
     environment, highest precedence). Operators manage zero parameters by
     default, one at most. There is deliberately NOT a separate hosted vs
     self-hosted parameter -- the environment branch lives inside the one
     compute-shards mechanism.
   - Sharding itself stays (removing it -> 522s serial, per the measurement).

2. **The free + public PR-CI ceiling is ~135s and that is a platform limit,
   not a process defect.** Reaching it needs BOTH levers (shard count at the
   hosted budget AND the e2e build cached); the specific e2e-build-cache
   mechanism is decided separately. Below ~135s is not reachable on free +
   public because the 20-cap caps shard parallelism and kcov's per-line cost
   is irreducible (ADR-00000016).

3. **Self-hosted is the only escape from the 20-cap, but it is gated for a
   public repo and deferred.** Using the self-hosted runner for PR CI would
   let coverage shard as parallel processes across its 32 cores (est.
   ~35-50s) and dodge the 20-cap, but a public repo must first land the
   same-repo guard (#766) so fork-PR code never executes on the machine, and
   must accept single-machine SPOF + contention with the owner's other work.
   Not scheduled.

4. **No paid GitHub runners** (owner decision). The escape paths beyond the
   free ceiling are: self-hosted (per decision 3) or a third-party runner
   provider -- both separate budget/ops decisions, out of scope here.

## Consequences

- The shard count stops being a maintained magic number; it self-sizes to the
  environment, generalising cleanly when/if self-hosted runners are adopted.
- "Why is CI ~3m and not faster?" has a recorded, evidence-backed answer: the
  free + public 20-cap plus serial-kcov cost. Speed work below ~135s is
  explicitly a runner-budget decision, not a workflow-tuning one.
- The self-hosted escape is documented but blocked on #766 + the SPOF
  trade-off, so it cannot be adopted accidentally.

## Alternatives

- **Keep a hardcoded `CI_SHARDS`.** Rejected: a maintained magic number the
  owner has to remember to bump; the budget/idle derivation removes it.
- **Remove sharding entirely (one coverage job).** Rejected by measurement:
  522s serial even on a 32-core machine; ~3x slower.
- **Move CI to the existing self-hosted runner now.** Rejected for now:
  public-repo fork-PR code-execution risk (needs #766 first) and
  single-machine SPOF / owner-workstation contention. Left as a documented,
  gated future path.
- **Buy concurrency (GitHub Team/Enterprise or third-party runners).**
  Rejected for now (owner decision); recorded as the other escape path.

## Amendment (2026-06-29): two CI principles make ~185s the irreducible floor; e2e caching and self-hosted-for-speed are both retracted

The original decision floated "~135s with both levers (shards + e2e build cache)"
and a "self-hosted escape ~80s". Both presupposed caching the e2e build. Two
governing principles, made explicit after the fact, rule that out:

1. **CI must align with the real `just docker build` flow.** A real user's
   build caches via the local docker daemon, never via a CI-injected
   `cache_from`. Any CI-only cache wiring (e.g. ghcr `cache_from` spliced into
   the generated compose) diverges from what users actually run -- rejected
   (same reason the prebuilt `base-env` image was rejected: it changes the
   real build).
2. **Every CI run must be clean and reproducible.** No state is retained
   between runs -- on self-hosted runners too (they must be kept stateless to
   match GitHub-hosted, or a cached run stops matching a clean run and CI
   loses reproducibility).

Together these forbid caching the e2e build by ANY mechanism: a CI-only cache
violates (1); a retained daemon cache violates (2). Therefore:

- **The e2e build is a clean build every run on every platform.** It is
  apt/network-bound and sequential (sys -> devel-base -> devel), so it is
  ~platform-independent (~154s arm64); extra cores do not speed it. This is
  the binding pole.
- **Irreducible CI floor ~= e2e-arm64 clean (~154s) + serial pre/post chain
  (classify + compute-shards + gate + rollup, ~30s) ~= 185s**, on BOTH
  GitHub-hosted and self-hosted.
- **Self-hosted is NOT a speed lever** under principle 2: a stateless
  self-hosted run pays the same ~154s clean e2e, and although it could shard
  coverage across more cores (no 20-cap), coverage is already below the e2e
  floor, so total does not move. The "~80s self-hosted" figure is retracted.
  Self-hosted retains only the non-speed considerations (and #766 guard) and
  is not pursued for performance.
- **`CI_SHARDS` increase is not pursued**: total is e2e-bound, so cutting
  coverage below the e2e floor yields no total-time win. The existing shard
  count stays (it keeps coverage at/under the e2e pole; removing sharding
  returns to the 522s serial run).

**~185s is therefore the accepted floor -- a deliberate choice of fidelity +
reproducibility over raw speed, not a process defect.** Going below it would
require violating principle (1) or (2), or dropping covered work (e.g. the
arm64 e2e, which has real value since the org ships arm64). The CI-squeeze
effort's remaining scope is the quality wins (broader e2e command coverage,
stale-comment + dead-package cleanup), not speed.

## Sources / provenance (every figure above is reproducible)

All measured / queried on 2026-06-29 unless noted. Recorded so future
re-examination can re-derive, not trust, the numbers.

- **Plan = free; 20 concurrent-job cap.** `gh api orgs/ycpss91255-docker
  --jq .plan.name` -> `free`. The 20-job (5 macOS) concurrency limit is the
  documented GitHub Free tier limit (GitHub Docs: Actions limits).
- **No hosted capacity / idle API.** `gh api
  orgs/ycpss91255-docker/actions/runner-limits` -> HTTP 404;
  `.../actions/hosted-runners` -> HTTP 404 "GitHub hosted runners are not
  supported for this organization"; `.../settings/billing/actions` -> HTTP
  410 Gone.
- **Peak concurrency 15.** Job-overlap analysis over `gh api
  repos/ycpss91255-docker/base/actions/runs/28347066279/jobs` (max count of
  jobs whose [started_at, completed_at) span a common instant).
- **Serial (unsharded) coverage = 522s.** `just test coverage` (full kcov, no
  shard) run on the org self-hosted runner host `C01013328` (32 vCPU, 125 GiB,
  GPU; `nproc`=32), wall-clock 522s, 2135 ok / 0 not-ok. The runner identity:
  `gh api orgs/ycpss91255-docker/actions/runners` -> 1 runner
  `C01013328-ycpss91255-docker-org`, labels `self-hosted,Linux,X64,gpu`,
  `status=online busy=false`.
- **Per-job times (e2e arm64 ~154s, amd64 ~114s, slowest coverage shard
  ~155-170s, total ~197-200s).** `gh api .../actions/runs/<id>/jobs` job
  durations for self-test main-push runs: `28347066279` (commit 32d9847,
  post-P1), `28279526244` (390ef9e, pre-P1 baseline), `28282248067` (cd20b1e,
  P1a). e2e step breakdown ("Build test stage" 93s arm64) from the per-step
  timings of the `Integration E2E (linux/arm64)` job in run 28347066279.
- **Per-spec kcov seconds (e.g. deploy_spec ~97-107s).** Merged
  `coverage-shard-*/timings.tsv` artifacts (max-dedup per spec) downloaded
  from runs `28279526244` and `28347066279`.
- **kcov tax +50-60% and the DEBUG-trap mechanism.** Spike on
  `ghcr.io/ycpss91255-docker/test-tools:main` (kcov v43, Bats 1.13.0, bash
  5.2.37): `deploy_spec` plain 29.7s vs kcov 47.4s (+60%); `setup_detect_spec`
  15.5s vs 23.2s (+50%); kcov output carried `bash-helper-debug-trap.sh`.
  Recorded in ADR-00000016.
- **e2e build is a clean (uncached) build.** The `integration-e2e` job uses
  the docker driver and rebuilds the example image each run; verified in
  `.github/workflows/self-test.yaml` (the "Set up Docker Buildx (driver:
  docker)" + "Build test stage" steps) and the per-step timings above.
- **Public repo + fork-PR gating.** `gh api
  repos/ycpss91255-docker/base/actions/permissions/fork-pr-contributor-approval`
  -> `{"approval_policy":"all_external_contributors"}`; `gh repo view` ->
  `visibility=PUBLIC`; `gh pr list --state all` fork-origin count = 0.


## ---- FILE: doc/adr/00000018-istqb-test-taxonomy.md ----

# ISTQB-aligned test taxonomy (levels / types / static analysis)

> Serves: PRD invariant 7 (rigorous, industry-aligned test bar) --
> established the commitment via the ISTQB-aligned taxonomy.

- **Date:** 2026-06-30
- **Status:** Accepted
- **Amends:** ADR-00000012 (supersedes only its category vocabulary
  `{smoke, unit, integration, behavioural}`; keeps its tool-first
  `test/<tool>/<category>/` + `test/lint/<tool>/` decision)
- **Relates to:** ADR-00000011 §5 (the generic test runner / per-tool
  driver model that walks this layout), ADR-00000015 (test files mirror
  source), issue #780 (epic), issue #781 (this ADR + the 12 amendment)

## Context

The test taxonomy was self-defined and mixed incompatible axes:

- The "4-category" matrix (base / docker_harness CONTEXT) is **Smoke /
  Unit / Integration / Lint**. That list mixes three different axes:
  Unit and Integration are *levels* (scope), Smoke is a *type*
  (purpose), and Lint is *static analysis* (not a dynamic test at all).
- base's `doc/test/TEST.md` "by type" index used a *different* 4-tuple:
  **unit / integration / behavioural / smoke** (Lint absent because it
  is not bats; `behavioural` present).
- So there were two "4"s that did not match, plus orphans: `behavioural`
  is not in any standard taxonomy, the full-image `integration-e2e` work
  had no category home, and smoke was misclassified as a level.

The mixed model left real gaps -- no Acceptance level, no clear home for
end-to-end -- and produced the QA defects that triggered this work
(broken downstream completion, empty `base/` dir, hardcoded/stale
`TEST.md` counts: all consumer-facing failures that no acceptance-level
test guards).

## Decision

Re-baseline to the industry-standard model -- ISTQB test levels plus the
Test Pyramid -- kept lightweight: take the spine of levels, the few
types actually used, and static analysis, not the whole certification
body. The taxonomy has three orthogonal axes.

### Axis 1 -- Static analysis (static testing)

Lint: ShellCheck (`.sh`) + Hadolint (Dockerfile). Not a dynamic test
level. Lives at `test/lint/<tool>/` (established by ADR-00000012, which
this ADR keeps).

### Axis 2 -- Levels (scope ladder)

| Level | Scope | Verifies against |
|-------|-------|------------------|
| **Unit** (Component) | one function / script in isolation | technical |
| **Integration** | several scripts / components together (init, upgrade, dispatch) | technical |
| **System** | the whole built image end-to-end (build to run to exec to stop); the build-gate mechanism | technical specs |
| **Acceptance** | what the downstream consumer receives -- the scaffolded framework + its UX (just commands, help, completion, generated layout), from the consumer's chair | user/operator expectations (UAT + OAT) |

Top level is **System** (ISTQB). "End-to-end" is a *type* performed at
the System / Acceptance level, not a level name.

### Axis 3 -- Types (purpose; applied at a level)

- **Smoke** -- build-verification: the critical "does it even come up"
  subset, run at build time inside each `-test` Dockerfile stage.
- **End-to-end** -- a complete workflow start to finish.
- **Regression** -- guards a previously-fixed defect (e.g. the
  build-gate-fires check, formerly `behavioural`).
- **Reserved (non-functional)** -- Performance / Security / Usability /
  Reliability: kept as empty placeholders in the framework, filled
  per-project when needed.

### Baseline + Extension model

The framework fixes the axes (the vocabulary). Each project = framework
**baseline** (provided / required) + project **extension** (its own
specs at each level / type). Unused slots are *reserved* (empty dirs +
`.gitkeep`) so the structure is complete and self-documenting without
reading this ADR.

### Key reclassifications (current -> standard)

- `behavioural` (drives buildx to prove the smoke gate fires) ->
  **System level + Regression type**. The non-standard term
  `behavioural` is retired.
- `e2e` as a *level* label -> **System** (e2e demoted to a type).
- `Lint` as the 4th "category" -> **Static analysis** axis (no longer a
  peer of the dynamic levels).
- **Acceptance** -> new explicit level (consumer framework + UX; UAT +
  OAT).
- Smoke -> a *type*, but keeps its own category directory because it is
  shipped + build-time.

### Directory layout (base and dist mirror 1:1, tool-first, zero exception)

```
test/bats/
  unit/          integration/
  system/        # was test/bats/behavioural/ (gate = Regression type) + image e2e
  acceptance/    # new: scaffold downstream + UX (UAT/OAT)
  smoke/         # build-time type, per Dockerfile -test stage
    shared/  devel-test/  runtime-test/
test/lint/{shellcheck,hadolint}/
```

- dist ships a 1:1 mirror:
  `dist/test/bats/smoke/{shared,devel-test,runtime-test}/` (replaces the
  tool-layer-skipping `dist/test/smoke/`).
- Each `-test` Dockerfile stage uses explicit selective COPY (only
  `shared/` + its own `<stage>/`, from both `.base/dist/...` and the
  repo) + `RUN bats /smoke_test/`. Adding a stage = a folder + that COPY
  block. Keeps the `-test` image small (only that stage's specs).
- Reserved / unused level or type slots: created as empty dirs with
  `.gitkeep` (not ADR-only), so the full taxonomy is visible in the tree.

## Consequences

- The taxonomy is now industry-standard and explainable by reference
  (ISTQB + Test Pyramid) instead of by repo lore. New contributors can
  place a test by its level and type without reading repo-specific
  category definitions.
- A new **Acceptance** level gives the consumer-facing checks (scaffold
  downstream, just / UX, generated layout) an explicit home -- the gap
  that produced the triggering QA defects.
- `behavioural` is retired across the codebase: the CI job, the runner
  driver, the doc catalogs, and `dist` all move to `system`. This is a
  rename with downstream reach, sequenced in the #780 sub-issues (this
  ADR is doc-only; no code / dir changes land here).
- The tool-first decision (ADR-00000012) is unchanged: `test/<tool>/`
  stays the unit of driver ownership, and `test/lint/<tool>/` keeps the
  linter configs. Only the *category vocabulary inside* `test/<tool>/`
  changes (`behavioural` -> `system`, `+ acceptance`, smoke kept as a
  shipped build-time type dir).
- The structure is self-documenting: reserved empty slots make the full
  level x type grid visible in the filesystem, so a missing
  non-functional or acceptance test is an obvious gap, not a silent one.

## Alternatives

- **Keep the self-defined 4-category model.** Rejected: it mixes three
  axes (level / type / static), has two non-matching "4"s, leaves
  `behavioural` and full-image e2e homeless, and has no Acceptance level
  -- the exact gaps behind the triggering QA defects.
- **Adopt the full ISTQB body (all levels, all functional /
  non-functional types, formal test-design techniques).** Rejected as
  too heavy for a container-template framework: only the level spine,
  three real types, and static analysis are used; the rest are kept as
  reserved placeholders rather than mandated.
- **Treat end-to-end as its own top level.** Rejected: ISTQB models
  end-to-end as a *type* run at the System / Acceptance level, so it is
  classified as a type, with System as the top level.

## Sources

- ISTQB test levels (Component / Integration / System / Acceptance):
  https://astqb.org/what-are-the-levels-of-testing/
- ISTQB Glossary -- acceptance / system / end-to-end testing:
  https://glossary.istqb.org/en_US/term/acceptance-testing/1 ,
  https://glossary.istqb.org/en_US/term/system-testing-3-2 ,
  https://glossary.istqb.org/en_US/term/end-to-end-testing
- Test Pyramid (Fowler):
  https://martinfowler.com/articles/practical-test-pyramid.html
- Acceptance sub-types incl. OAT / UAT:
  https://en.wikipedia.org/wiki/Acceptance_testing


## ---- FILE: doc/adr/00000019-network-host-default-bridge-optin.md ----

# Network mode: keep `host` as the default, ship `bridge` as a usable opt-in

> Serves: PRD invariant 4 (fail-safe defaults) -- established; the
> network host default is the general principle's instance.

- **Date:** 2026-07-07
- **Status:** Accepted
- **Relates to:** issue #794 (this decision, recorded in the issue's
  "Decision update (grilled): keep host as the default" comment), issue
  #466 (privileges / features are opt-in), the follow-up opt-back guidance
  in `ros1_distro#36` / `ros2_distro#35`

## Context

The `[network] mode` scalar in `setup.conf` defaults to `host`. Issue #794
originally proposed **flipping the default to `bridge`** (with `ipc =
private`) on least-privilege grounds: an app / AI-tooling container has no
reason to share the host's network namespace, and bridge is the
docker-idiomatic, more-isolated posture.

Empirical testing (local + a physical-machine run, captured in the issue's
`RESULTS.md`) surfaced two findings that reframed the trade-off:

- **Local GUI under bridge breaks X11 auth.** On a pure-Xorg host the X11
  MIT-MAGIC-COOKIE is keyed to the host's hostname. Under bridge the
  container is assigned a random hostname, so `libX11` looks the cookie up
  under the wrong name and authentication fails. Pinning the container's
  hostname to the host's name (`--hostname=<host>` / compose `hostname:`)
  fixes it reliably (verified on Wayland and simulated Xorg).
- **Cross-machine ROS under bridge fails, unfixably.** For BOTH ROS 1 and
  ROS 2, cross-machine discovery / transport fails under bridge and stays
  broken even with the hostname fix, because the container sits on the
  `172.17.x` docker network, which is **not routable off the box**. There
  is no in-container knob that makes a bridge address reachable from
  another machine. Multi-machine robots MUST keep `host`.

The decisive factor is **risk asymmetry**, not which posture is "cleaner":

- Guessing the default wrong toward `host` on a single-machine app
  container costs only a layer of defence-in-depth. It is a dev container
  the user controls; the loss is bounded and non-catastrophic.
- Guessing the default wrong toward `bridge` on a cross-machine ROS robot
  makes a safety scanner / LiDAR **silently unreachable across machines,
  with CI still green**. The failure is silent, catastrophic, and
  safety-relevant.

The org is also ROS-plurality, so a generic default serves the majority
best by staying `host`.

## Decision

**Reverse the flip. Keep `host` as the default and make `bridge` a usable
opt-in instead.**

1. **Nothing is flipped.** The seeded `setup.conf` stays `network.mode =
   host` / `network.ipc = host`, and the code-level key-absent fallbacks
   (`deploy.sh` resolved-config, `compose_emit.sh` context defaults and the
   `generate_compose_yaml` positional defaults) also stay `host`. Template
   and code agree.
2. **Make the opt-in usable, not a trap.** When the GUI is enabled AND
   `network.mode = bridge`, the compose emitter injects `hostname: <host>`
   on the service (shared `_emit_hostname_line` helper, gated on effective
   `gui == true && net == bridge`, resolved from `HOSTNAME` with a `uname
   -n` fallback and threaded to both the devel service and every per-stage
   standalone block). Under `host` networking or with the GUI off, nothing
   is injected.
3. **Document the opt-in with a hard warning.** README "Network mode"
   subsection + a `setup.conf [network]` header note carry the recipe
   (`setup.sh set network.mode bridge && setup.sh set network.ipc private
   && setup.sh apply`) and state plainly that cross-machine ROS must stay
   `host`. A commented `port_1 = 8080:80` example is seeded, since ports
   only take effect under bridge.

## Alternatives considered

- **Flip the default to `bridge` (the original #794 proposal).** Rejected:
  under the risk asymmetry above, the default must fail safe toward the
  catastrophic case. Flipping globally and hoping every ROS repo remembers
  to opt back re-introduces exactly the silent-failure mode the default is
  meant to prevent.
- **Flip only for non-ROS templates.** Rejected as fragile: "is this repo
  cross-machine ROS?" is not reliably knowable at template-default time,
  and the classification would drift. Least-privilege for confirmed
  single-machine repos is better delivered by an explicit, documented
  opt-in the repo owner makes deliberately.
- **Ship bridge opt-in without the hostname pin.** Rejected: a bridge
  opt-in that silently breaks local GUI is a broken trap. The pin is what
  makes the opt-in actually usable.

## Consequences

- The default posture is unchanged, so every existing downstream repo and
  the ROS-plurality majority are unaffected — no fan-out migration, no
  silent breakage.
- Single-machine app / AI-tooling repos get a documented, one-command path
  to a more isolated bridge posture, with local GUI preserved.
- The compose emitter carries a small GUI+bridge-conditional branch in both
  emit paths (devel + per-stage), covered by `hostname_spec.bats` and the
  updated `#505` golden master.
- **Deferred acceptance items (need physical display hardware):** verifying
  that a GUI window actually *renders* under bridge (not just that X11 auth
  succeeds), the real `just run` GUI path end-to-end, and the `--hostname`
  side-effect on ROS node naming. These are `RESULTS.md` gaps that a CI /
  headless environment cannot close.


## ---- FILE: doc/adr/00000020-base-owns-single-service-lifecycle.md ----

# `base` container is one service; `base` owns the common single-service lifecycle

> Serves: PRD invariant 1 (base owns the single-service lifecycle) --
> established; also PRD invariant 5 (the two-branch default rule).

- **Date:** 2026-07-07
- **Status:** Accepted
- **Amended:** 2026-08-03 -- the restart policy is scoped to *deployable*
  stages only; `devel` and `*-test` never carry one, and its default flips
  to ON (`unless-stopped`). See "Lifecycle capabilities are not uniform
  across stages" below.
- **Relates to:** issues #478 (restart policy), #792 (init / PID1
  reaping), #797 (generic watchdog / supervised restart), #805 (durable
  log persistence), and ADR-00000019 (network host default + usable
  bridge opt-in) as a sibling lifecycle-defaults decision

## Context

`base`'s container model is **"one container = one service"**: a
`base`-built image runs a single service. This is the foundational axiom
every downstream repo inherits — a downstream is a `base` image plus one
app, not an orchestration of several co-tenant processes.

Several capabilities that every single-service container needs have been
surfacing as separate issues, each initially framed as a per-repo
concern:

- **restart policy** (#478) — what Docker should do when the one service
  exits.
- **init / PID1 reaping** (#792) — a proper init as PID 1 so signals are
  forwarded and zombie children are reaped.
- **generic watchdog / supervised restart** (#797) — detect that the
  service is unhealthy and take a restart action.
- **durable log persistence** (#805) — the one service's logs survive
  container recreation.

These are not app features; they are properties of *running a single
service in a container well*. The recurring question was whether
consolidating them into `base` is premature abstraction, given that the
first concrete consumer of any given capability is often a single repo.

This premise was explicitly grilled. The conclusion: because the
one-service model is `base`'s axiom, the **common single-service
lifecycle is exactly what `base` exists to own**. Wrapping the
one-service-container model for downstream *is* `base`'s purpose;
providing these capabilities is fulfilling that purpose, not speculative
generalisation — even when the first concrete consumer is a single repo.
The alternative (each downstream re-implements restart / init / watchdog
/ log persistence) is the actual anti-pattern: N divergent, partially
correct copies of a concern that is identical across the fleet.

## Decision

**Adopt as a design axiom: a `base` container is one service, and `base`
owns the common single-service lifecycle capabilities that every
downstream needs.** New lifecycle capabilities of the one-service model
land in `base` by default, exposed as configuration, rather than being
pushed down to individual repos.

The lifecycle umbrella currently comprises restart policy (#478), init /
PID1 reaping (#792), the generic watchdog / supervised restart (#797),
and durable log persistence (#805). ADR-00000019 (network host default,
usable bridge opt-in) is a sibling decision in the same
lifecycle-defaults family.

This ADR records the *axiom and ownership rationale*. The concrete
mechanism for each capability is specified in its own issue (the
watchdog's design lives in #797, not here).

### Lifecycle capabilities are not uniform across stages (amendment, 2026-08-03)

The umbrella above treats the lifecycle as a property of "the one
service". That holds for init, the watchdog, and log persistence, but
**not** for the restart policy: whether a stopped container should come
back depends on whether the container is a *service* or a *session*.

A `devel` container is a session. Its life *is* the interactive shell, so
a restart policy means typing `exit` immediately relaunches it — there is
no way to leave. A `*-test` stage is likewise designed to exit, and an
exit-0 stage inheriting devel's policy is precisely the restart loop
#493 hit. A deployable stage and a field bundle are the opposite: they
run a service that is meant never to stop, so coming back — after a
crash, and after a host reboot — is exactly right.

Decision:

- **The restart policy applies only to deployable stages and the field
  bundle.** `devel` and any `*-test` stage never emit one. The previous
  mechanism (emit on `devel`, let `extends: devel` stages inherit) is
  removed; qualifying stage services emit it themselves.
- **"Deployable" is not a second definition.** It binds to the existing
  rule in ADR-00000023 sec.4 (`deployable = not devel and not *-test`),
  hoisted into a single shared predicate so there is one place to change.
- **The default flips from `no` to `unless-stopped`**, and is shipped
  literally in the template so it is visible rather than implicit. Once
  the key no longer straddles dev and field, the two consumers no longer
  want opposite defaults, so no absent-vs-explicit distinction is needed:
  an explicit value is honoured verbatim wherever the key applies.

This refines, and does not contradict, the "default ON only where absence
is a footgun" rule in Consequences: after the rescope, every context the
key still reaches is one where a container that fails to come back *is*
the footgun.

Note that the ownership axiom is unchanged — `base` still owns the
restart policy. What changed is the recognition that a lifecycle
capability can be stage-scoped, which is the first case where the
umbrella needed qualifying.

## Alternatives considered

- **Push each capability down to the consuming downstream repo.**
  Rejected: the one-service lifecycle is identical across the fleet, so
  per-repo implementations produce N divergent, partially correct copies
  and drift. Ownership in `base` is the point of `base`.
- **Defer consolidation until there are multiple consumers ("rule of
  three").** Rejected here specifically because the shared substrate is
  `base`'s stated purpose, not an incidental commonality discovered
  across unrelated call sites. The grill accepted that "first consumer
  is one repo" does not make this premature — the abstraction boundary
  is the one-service model itself, which is already universal.
- **Bake fixed lifecycle behavior into `base` (non-configurable).**
  Rejected: it would change behavior for every existing downstream
  unconditionally and remove Docker-native escape hatches. Configuration
  with a principled default (see the default-rule consequence below) is
  the middle path: safe defaults where absence is a footgun, opt-in where
  semantics could change.

## Consequences

- **Every lifecycle capability is exposed as configuration, and its
  DEFAULT is the safest correct behavior for a well-run single-service
  container — decided by a principled two-branch rule, not per-capability
  taste:**
  1. **When enabling the capability is transparent to a correct workload
     AND running without it is a footgun, the default is ON.** Concrete
     instance: init / PID1 reaping (#792) defaults **ON**. With the app
     running as PID 1 there is no zombie reaping and no signal
     forwarding, so `stop` can hang until `SIGKILL` and orphaned children
     accumulate — "app as PID 1" is itself the latent bug. `init: true`
     is transparent to a correct single process and fixes both, so it is
     the safe default even though it is a (beneficial, low-risk) behavior
     change on the next compose regeneration.
  2. **When enabling the capability could change a workload's semantics,
     the default is OFF / the Docker-native no-op, and enabling is
     opt-in.** Concrete instances: network / ipc mode (ADR-00000019, host
     default), the watchdog's restart-service action (#797, restart the
     whole container is the default), and the restart policy (#478).

     **Amendment (#994, 2026-09-03):** "OFF / the Docker-native no-op"
     conflates two things that are usually the same and are not always.
     What OFF means is the **no-op** — the behavior an unconfigured
     container already had before the knob existed. That is Docker's own
     behavior wherever `base` had not already intervened, which is why
     the phrase held for the watchdog and the restart policy. It does not
     hold for the network instance listed here: `host` is `base`'s
     pre-existing default, where an unconfigured `docker run` gives
     `bridge`, and ADR-00000019 kept `host` on PRD invariant 4 grounds.
     The no-op is the rule; Docker-native is what it usually coincides
     with. See PRD invariant 5.

  The double condition — *transparent to correct workloads* AND *absence
  is a footgun* — is what prevents an "everything defaults ON" slippery
  slope: an unset knob is a no-op only where the capability is genuinely
  optional; where its absence is a latent bug, the default fixes it. New
  lifecycle features are documented in the README.
- **Where a capability has a non-trivial failure action, the action is
  itself configurable, with the Docker-native option as the default, so
  the simple case pays no complexity.** Concretely for the watchdog
  (#797): the default action is to restart the whole container (the
  Docker-native behavior), and restarting only the in-container service
  is an opt-in.
- **`base` owns the mechanism; app-specific policy is plugged in.** For
  the watchdog, the health-check command and the notify command are
  pluggable and supplied by the app / operator; `base` provides the
  supervision loop, not the app's definition of "healthy".
- Downstream repos get correct single-service lifecycle behavior for
  free as `base` gains each capability, via the normal `.base` subtree
  upgrade — no per-repo re-implementation.
- This ADR is a rationale record and changes no behavior on its own; the
  behavior arrives with each capability's own issue and PR.


## ---- FILE: doc/adr/00000021-per-start-container-logs-shared-logrotate.md ----

# Per-start container log files + stable symlink + shared rotate/prune helper

> Serves: PRD invariant 1 (base owns the single-service lifecycle) --
> per-start container logs (#805) realise it; mechanism.

- **Date:** 2026-07-07
- **Status:** Accepted
- **Relates to:** issue #805 (this decision), ADR-00000007 (wrapper
  transcript, the glog-style precedent this reuses), the `[logging]
  local_path` feature (#310 / #328 / #368), and the #797 watchdog design
  discussion that raised the need for a durable, bounded on-disk log.

## Context

The `[logging] local_path` container-log tee (`runtime/logging.sh`) wrote a
single file per service (`/var/log/<repo>/<svc>.log`) and TRUNCATED it on
each container start (`: > $LOG_FILE_PATH`). Two footguns: within one run
the file grows unbounded, and on restart the previous run's log is wiped.

The wrapper transcript (`lib/transcript.sh`, ADR-00000007) already solved
exactly this shape well: a per-run timestamped real file plus a stable
`latest.log` symlink pointing at the newest, with config-driven keep/days
pruning that skips the symlink. This ADR records applying that same
glog-style design to the container-log tee, and extracting the shared
mechanism so the two producers do not carry parallel implementations.

## Decision

1. **Per-start real file + stable symlink.** On each container start the
   tee writes a per-start real file `log/<svc>/<svc>_<ts>.log` and repoints
   a stable symlink `log/<svc>/<svc>.log` (= the emitted `LOG_FILE_PATH`)
   at it. `tail <svc>.log` always follows the current run; earlier runs
   stay on disk. This replaces truncate-on-restart, so run history is
   retained instead of wiped. `docker logs` parity is unchanged (the tee
   still echoes to the daemon's stdout).

2. **Configurable retention.** Two new `[logging]` keys,
   `container_log_keep` (default 20) and `container_log_days` (default 14),
   registered in `schema.sh` and validated as positive integers, exactly
   mirroring `wrapper_transcript_keep` / `wrapper_transcript_days`. Old
   per-start files are pruned by keep-count AND age (stricter wins), never
   the symlink. A non-positive hand-edit clamps back to the default so
   prune can never wipe every log.

3. **One shared helper (DRY).** The "repoint the stable symlink + prune old
   per-start files by keep/days, skipping the symlink" logic is extracted
   into `runtime/logrotate.sh` (`_logrotate_repoint` + `_logrotate_prune`),
   parameterized on symlink name / dir / keep / days. Both producers use
   it: `transcript.sh`'s `_transcript_prune` and its `latest.log` repoint
   now delegate to it (its symlink stays `latest.log`), and the
   container-log tee calls it with `<svc>.log`.

## Consequences / trade-offs

- **Placement across two execution contexts.** `transcript.sh` runs
  host-side (`lib/`); `logging.sh` runs in-image (`runtime/`, sourced from
  `/usr/local/lib/base/`). They share no source graph. The shared helper
  therefore lives under `runtime/` and is COPY'd into the image alongside
  `logging.sh`; the host lib sources it via the sibling `../runtime/` path.
  Both source it DEFENSIVELY (readable-check + `declare -F` guards) so the
  shellcheck `/lint` image stage, which flattens `lib/` without a `runtime/`
  sibling, degrades gracefully instead of aborting under `set -e`.

- **Retention crosses the container boundary via env.** The prune runs
  in-container (co-located with the tee, so it also covers auto-restarts),
  but the retention values live in the host-side `setup.conf`. `compose_emit`
  reads `container_log_keep` / `container_log_days` from the conf layer and
  emits them as `CONTAINER_LOG_KEEP` / `CONTAINER_LOG_DAYS` env alongside
  `LOG_FILE_PATH`; `logging.sh` reads the env with the same fallback +
  clamp. This mirrors how `LOG_FILE_PATH` itself already crosses the
  boundary, at the cost of baking the values into `compose.yaml` at setup
  time (a re-`setup` re-reads them, same as every other emitted value).

- **Downstream propagation.** A downstream Dockerfile that COPYs
  `logging.sh` but predates the split needs the `logrotate.sh` sibling COPY,
  or the tee degrades to no rotation/prune. A `logrotate_copy`
  `dockerfile_migrate` migration adds the sibling COPY on `just upgrade`.

- **Same-second collision guard.** The per-start filename is second-granular
  (`<svc>_<ts>.log`). Two starts in the same wall-clock second (a crash-loop
  restart with sub-second backoff) would otherwise resolve to the same path
  and the second would truncate the first -- the exact footgun this issue
  removes. `logging.sh` guards it by probing a `-<n>` suffix when the
  timestamped name is already taken, so each start keeps its own file (the
  disambiguator the transcript gets from its `<ts>-<traceid8>` shape).

- **Prune is symlink-safe, but keep is pooled (known limitation).** Both
  prune passes exclude symlinks (`find -type f` in the age pass, an `-h`
  test in the count pass), so neither the caller's own stable symlink nor a
  sibling service's `<other>.log` symlink sharing `/var/log/<repo>/` is ever
  deleted -- symlink safety does not depend on the symlink's name. However,
  both passes glob every `*.log` real file in the dir, so the `keep` / `days`
  caps are POOLED across services when multiple services tee into one dir,
  not per-service. Under the one-service-per-repo model this is rare and is
  left out of scope here; revisit if a repo runs many services into the
  same log dir.

## Scope note

This issue changes only HOW container logs are stored (per-start + symlink
+ retention). Whether `local_path` should default ON is a SEPARATE decision
and stays out of scope here: the default remains opt-in (empty). With the
unbounded-growth footgun removed, that default can be revisited later.

## Alternatives

**Amendment (#994, 2026-09-03):** this section was added when
`adr_structure.sh` made Alternatives a required part of the format. It is
reconstructed from the options this decision's own Context, Decision and
Scope note already weigh -- it is not a later re-deliberation, and nothing
below changes what was decided.

**Keep truncate-on-restart and cap growth with `logrotate(8)`.** Rejected:
it needs a second long-running process inside a container that runs
exactly one service (invariant 1), and the host-side variant cannot see a
container start at all -- it rotates on a byte or time boundary, which is
not the boundary a reader is looking for. "Show me the previous run" is
the question being answered, and only the start boundary answers it.

**Rely on the daemon's `json-file` driver with `max-size` / `max-file`.**
Rejected: same boundary mismatch, plus the rotated files sit at
daemon-owned paths a downstream cannot bind-mount or `tail`. `docker logs`
parity is preserved by the tee regardless (Decision 1), so this would
replace nothing that is missing.

**A second implementation of repoint-and-prune, local to the container
tee.** Rejected by Decision 3. `lib/transcript.sh` had already solved this
shape; two implementations of one rule drift as soon as either is edited
alone, and the extraction into `runtime/logrotate.sh` is what makes the
transcript's and the tee's retention behaviour the same behaviour rather
than two that happen to agree today.

**Refuse a non-positive retention value at runtime rather than clamp it.**
Rejected. The schema registry already refuses it loudly at `just setup`,
where a human is present; the runtime read is a second arrival of the same
values through a hand-editable `compose.yaml`, at PID 1, where a refusal
means the container does not start. Clamping back to 20 / 14 keeps the
service correct, which is the trade the PRD's conflict priority makes
(property 1 over property 2) and the reason the clamp is not a violation
of invariant 2.

**Per-service `keep` / `days` instead of a pooled per-directory cap.**
Not rejected -- deferred, and recorded as a known limitation in
Consequences. Both prune passes glob every `*.log` real file in the
directory, so the caps pool across services that share one log dir. Under
the one-service-per-repo model that case is rare; it is revisited if a
repo runs several services into the same directory.

**Default `local_path` ON as part of this change.** Explicitly out of
scope (see the Scope note). This decision changes only how container logs
are stored; whether the tee is on by default is a separate question, now
answered by the two-question test in PRD invariant 11.


## ---- FILE: doc/adr/00000022-compose-multirun-overlay-contract.md ----

# base<->multi_run compose contract: per-instance isolation is an overlay, enforced by a guard

> Serves: PRD invariant 3 (composable by construction) --
> established by the overlay contract + guard; also invariant 2 (a loud
> self-check).

- **Date:** 2026-07-08
- **Status:** Accepted
- **Relates to:** issue #716 (this decision), issue #25 (multi_run),
  ADR-00000001 (setup.conf is the main path, compose-native mechanisms are
  the escape hatch), ADR-00000003 (environment vs workload parameter
  boundary; the `.env` overlay + `env_file:` channel), ADR-00000019
  (network host default / bridge opt-in, the `ports` / `hostname` fields),
  ADR-00000020 (base owns the single-service lifecycle). Enforced by
  `test/bats/unit/compose_emit/overlay_guard_spec.bats`.

## Context

`multi_run` (issue #25) runs the same base-generated stack in three
scenarios: (1) one repo / many instances, (2) many repos / one instance,
(3) many repos / many instances. `docker compose` has **no native
instance axis** -- it models project, service, and `replicas`, but not
"the same service run N times with per-instance parameters". So any field
that must vary per instance, if base emits it into the generated
`compose.yaml` as a **hardcoded literal**, becomes a wall: two co-located
instances collide on host ports / writable paths / DDS domain, and
`multi_run` cannot isolate them without a retroactive change to base's
emitter.

The core mechanism -- "per-instance isolation = a `.env` overlay" -- was
already decided in the v0.42 docker-namespace epic. What was missing was
(a) an explicit resolution of the fields ADR-00000003 left in the axis-A
grey zone (`ports` / `network_mode`: machine-bound *environment* or
per-task *workload*?), and (b) any guarantee that a future emitter change
would not silently bake a fresh per-instance literal and re-erect the
wall. Discipline is not a guarantee; the v0.41 Dockerfile drift and the
#800 worker-contract gaps are the same failure class -- a latent blocker
that stays green until someone downstream hits it.

## Decision

### 1. Per-instance isolation is a `.env` overlay, never a compose regenerate

> **Amended 2026-09-06 by ADR-00000036 (#1087).** The rejection of per-instance
> regeneration is withdrawn, and the reason it was right has stopped applying.
> It rested on generation being able to write only into the repo, so
> regenerating meant mutating a shared checkout and two instances would fight
> over one file. Once a call names its own output directory, that objection is
> gone. Per-instance generation is now the supported path for parameters that
> change the emitted file's SHAPE -- build args, image rules, conditional blocks
> -- which an interpolation cannot reach at all: `${VAR}` substitutes into lines
> that already exist. **The overlay is not withdrawn.** It remains correct and
> cheaper for values that do not change the file's shape, and every channel in
> section 3's table keeps working unchanged.

An instance is isolated by supplying **overlay values**, not by
regenerating `compose.yaml`. `compose.yaml` stays a single committed-shape
artifact; the per-instance delta lives entirely in overlay inputs
`multi_run` controls. This preserves ADR-00000003's two-role split:
`.env.generated` feeds compose `${VAR}` interpolation via `--env-file`,
and the container's env comes through `env_file:`.

**Amendment (2026-08-26, #868): the per-instance env file is `.env.local`.**
ADR-00000003's A2 was reversed -- `.env` is now the tool's generated
defaults and is rewritten by every apply, so an instance delta written there
would be destroyed. `env_file:` is now the ordered pair `[.env, .env.local]`
and a later file wins, so the channel this contract depends on is intact and
only its name moved. The interpolation half is unchanged.

### 2. Environment-default / per-instance-overridable (the axis-A resolution)

Every field that can vary per instance is emitted as an
**overlay-overridable interpolation** (`${VAR:-<default>}` or `${VAR}`),
never a hardcoded literal. The default may stay machine-bound (resolved
from `setup.conf` as before), but an overlay-override path **always
exists**. A field is thus simultaneously an environment default (single
run: the overlay var is unset, compose substitutes the default, behaviour
is byte-equivalent) and per-instance-overridable (multi_run: the overlay
sets the var). This is the explicit resolution of the ADR-00000003 axis-A
grey zone for `ports` / `network_mode` and the rest: they are *both*, and
the interpolation form is what lets one emission serve both roles.

### 3. Override channel by field kind

> **Amended 2026-09-06 by ADR-00000036 (#1087).** The last row of this table --
> GPU, `runtime` and `hostname` recorded as correctly shared -- is narrowed to a
> statement about the host, not about the contract. Three co-located instances
> do share one GPU device tree; it does not follow that they must claim it
> identically, and an assembler may want instance 1 on GPU 0, instance 2 on
> GPU 1 and instance 3 with none. These become caller-reachable. The row's
> reasoning about the X11 cookie and the host's timezone is unaffected.
>
> The paragraph above this table -- "the audit is a starting point, not an
> exhaustive allowlist" -- is superseded by a stronger rule: anything base
> decides at build time or before the container starts must be reachable by the
> caller, and only what is internal to a running container is outside the
> contract.

The audit is a **starting point, not an exhaustive allowlist** -- ANY
field that can collide across instances must have an override path. The
channel differs by kind:

| Field kind | Per-instance override channel | Emitted form |
|---|---|---|
| project `name:` | compose interpolation from `--env-file` | `${PROJECT_NAME}` (was `${DOCKER_HUB_USER}-${IMAGE_NAME}`; see the 2026-08-05 amendment below) |
| `container_name:` | interpolated **and** removable (non-load-bearing, see §4) | `${USER_NAME}-<repo>[-<svc>]` -- **no longer emitted by the dev stack; the field-deploy bundle (`just docker setup deploy`) still bakes one. See the 2026-08-26 amendment below** |
| `network_mode:` | compose interpolation | `${NETWORK_MODE}` |
| `privileged` / `ipc` / `pid` | compose interpolation | `${PRIVILEGED}` / `${IPC_MODE}` / `${PID_MODE}` |
| **`ports:`** | compose interpolation, **per published port** | `${PORT_<n>:-<default>}` (n = **1-based** index within the service's port list -- `PORT_1` = first port, matching base's 1-based indexed-key convention `port_1` / `mount_1` / `arg_1`) |
| workload env (`ROS_DOMAIN_ID`, tokens) | `.env.local` via `env_file:` + generated `.env` / baked ENV default (ADR-00000003 S3, renamed by #868) | default in the generated `.env`; `.env.local` loads after it and wins |
| writable volume topology | compose-merge overlay (a mount is a topology decision, not a flat scalar) | bind/named mount string |
| `runtime` / `hostname` / GPU | **not per-instance** -- host-bound, correctly *shared* across co-located instances (all instances on a host share the runtime, the X11-cookie hostname, and the GPU) | literal / host-resolved |

**Amendment (2026-08-05, ADR-00000025): the project `name:` row's emitted
form, and the stage this ADR does NOT cover.** The row above is unchanged in
substance -- project `name:` is still an interpolation from `--env-file`, and
multi_run still overrides it by setting that variable in its runtime overlay.
What changed is *which* variable: the emitter used to re-assemble
`${DOCKER_HUB_USER}-${IMAGE_NAME}` while the wrapper computed the same string
in bash, two answerers to one question, and both now read the single
`PROJECT_NAME` that `setup apply` resolves into `.env.generated`. The
interpolation form -- the thing this ADR's forward invariant and its guard
actually pin -- is preserved deliberately: emitting the resolved literal would
have been simpler and would have re-erected the wall.

ADR-00000025 also adds a per-worktree `.setup.conf.local` config layer, and it
is worth being explicit that it is **not** this contract's mechanism, because
the resemblance invites the mistake. That layer acts BEFORE `compose.yaml` is
generated and yields one `compose.yaml` per worktree; per-instance isolation
here acts at interpolation time on ONE already-generated `compose.yaml`, which
is precisely why sec. 1 rejects a per-instance regenerate. A developer's
second worktree and multi_run's Nth instance are different stages of the
pipeline, and neither mechanism can do the other's job. ADR-00000025 sec. 5
carries the full division of labour.

**Amendment (2026-08-26, issue #920): the dev-stack emitter stopped
emitting `container_name:` itself, and the field-deploy bundle
(`just docker setup deploy`) did not.** §4 below records that the field is
removable and that `multi_run` *may* drop it; `generate_compose_yaml` has
now dropped it, so there is no `container_name:` line in the dev
`compose.yaml` a repo runs for an overlay to override or remove, while
`_generate_resolved_compose` still writes one. Scope: this is the dev stack, the only emission an
overlay ever expands. The field-deploy bundle (`_generate_resolved_compose`,
`just docker setup deploy`) still bakes one, deliberately -- it is a fully
resolved single-device artifact, one stack per device, never co-located,
and its operator wants a stable name to `docker logs`. Two emitters, two
rules; the co-location argument below is the dev stack's.

The reason the weaker form was not enough: the guard
asked only that the value carry an interpolation, and `${USER_NAME}-<repo>`
satisfied that -- yet a container name is namespaced by the DAEMON, not by
the project, and `${USER_NAME}` is one string for all of a user's instances.
Two co-located stacks under distinct project names therefore still collided
at `up` (`name ... is already in use`), and compose refuses `--scale` while
any container_name is present. No value of the field can be per-instance
safe, so the guard now asserts its ABSENCE rather than its shape.

Per-host isolation moved entirely into the project name as a consequence,
and it holds there with NO second mechanism. The derivation is unchanged --
`${DOCKER_HUB_USER}-<image>` -- and that prefix is already per-OS-user with
nothing configured, because `detect_docker_hub_user` falls back to
`${USER:-$(id -un)}` when `docker info` reports no login and is the only
writer of the key. A configured `[project] name` still wins, and remains
the answer for the one case the derivation cannot separate: two OS users
sharing ONE Docker Hub login, which hands both the same prefix.

*Correction (same amendment).* A first cut of this change added an OS-user
rung to `_resolve_project_name` itself, on the belief that
`DOCKER_HUB_USER` is frequently unset and that such consumers were deriving
`local-<image>`. Both halves were wrong: detection cannot yield an empty
key, so no recorded `.env.generated` was ever in that state, and the rung
was unreachable regardless -- `detect_user_info` ends in the same
`${USER:-$(id -un)}`, so a host that leaves the hub user empty leaves
`USER_NAME` empty too. The rung was removed rather than documented, and
this paragraph stays so that a reader chasing a changed project name is not
sent to a condition that cannot occur.

A derived project name can nevertheless change under a deployed consumer,
without anyone asking for it -- and dropping `container_name` is what makes
that dangerous rather than untidy, since the second stack used to die
loudly on the baked name and now starts alongside the first. The trigger is
`just upgrade`: `upgrade.sh` runs `init.sh`, which runs `setup apply` during
the upgrade itself. (Not the drift re-apply on the next `build` / `run`:
`_check_setup_drift` hashes `setup.conf`, the Dockerfile stage list,
GPU/GUI detection and `USER_UID` -- nothing about the `.base` version or
`DOCKER_HUB_USER` -- so a subtree upgrade alone leaves check-drift green.) That apply re-detects
`DOCKER_HUB_USER` from `docker info`, so any repo whose recorded prefix no
longer matches what detection now yields -- a `docker logout`, a login as
a different account, CI versus a workstation -- resolves a different name
than the one its containers carry.

The population that made this urgent is the one still on the release
BEFORE the project name became a recorded value. Those `.env.generated`
files carry no `PROJECT_NAME` key at all: the emitter interpolated
`name: ${DOCKER_HUB_USER}-${IMAGE_NAME}` and the wrapper assembled the
same string for `-p`. Read naively, a missing key looks like a fresh
checkout, and a fresh checkout is exactly the case that renames without
deferring -- so the whole mechanism below would have skipped precisely the
repos it was written for. `_recorded_project_name` (lib/compose.sh)
reconstructs the old name from the two keys that ARE in the file.

The project name is the key compose looks its own containers up by, so
renaming while a stack is up would hide the stack from every wrapper at
once -- `stop` would tear down the new, empty project and `run` would
start a second copy over the first's bind mounts, host network and
devices, with the original reachable only by raw `docker`. Compose cannot
relabel a running container, so a rename can only take effect on an EMPTY
project.

**Decision: defer, do not skip.** While anything of the user's exists
under the recorded name, `setup apply` keeps `.env.generated` on it and
records the resolved one as `PROJECT_NAME_PENDING`
(`_carry_project_name`, lib/compose.sh); the first `build` / `run` that
finds the old project empty adopts it. The split is deliberate -- the
side that resolves the configuration decides to DEFER, the side that can
ask the daemon ADOPTS (see the reconciliation paragraph at the end of
this section) -- and the wrapper has no direction that records a pending
name. Both steps are reported, so the name a checkout runs under never
changes silently. "Empty" counts containers AND named volumes, because
both are keyed by the project name
and only one of them is recoverable afterwards: `stop` runs `compose down`
without `-v`, so a torn-down stack routinely leaves its volumes, and
adopting on a container-only probe would hand the user a fresh EMPTY
volume under the new name while the data sat in an orphan `prune
--volumes` later deletes. Project networks and built images are NOT
counted -- `compose down` removes the network, and an image is named
`<hub>/<repo>:<stage>` rather than by the project, so neither can be
orphaned by a rename. `stop` is therefore the whole migration for a repo
without named volumes -- it needs no new flag and addresses the stack the
user actually has, because `stop` / `exec` never regenerate and so read
the recorded name. A repo WITH named volumes keeps its old name until
someone moves or removes the data or pins `[project] name`, and is told
which of the two it is. The costs, accepted: a consumer who never stops keeps the
old (colliding) name indefinitely -- one working stack rather than two --
and while a stack is up the recorded `PROJECT_NAME` is deliberately not
the one `setup apply` just resolved. `PROJECT_NAME_PENDING` is what keeps
that divergence visible and self-clearing; it is re-derived by the next
apply, so nothing depends on it surviving. An unreachable daemon defers
too: deferring costs a cycle, renaming on a guess costs the stack.

A CONFIGURED `[project] name` is the exception and takes effect at once.
Deferring it would defeat the setting it is: its whole use is a second
worktree that must not share the first's derived name, and the containers
under that shared name are the OTHER checkout's -- occupancy there is the
reason to rename, not a reason to wait. A rename someone typed is also an
act they can sequence around, unlike a changed default. `setup apply` says
so when it displaces a recorded name, so that path is not silent either.

The reconciliation lives in the wrapper, not in `setup.sh`, because
whether a project is occupied is a question only the daemon can answer and
`setup.sh` resolves configuration on hosts where docker need not be
reachable at all.

The concrete change this decision required was `ports`: they were baked
literals and are now `${PORT_<n>:-<default>}`, `n` 1-based per the
convention above (a human who configured `[network] port_1` overrides
`PORT_1`, not `PORT_0` -- the off-by-one would be a footgun). The other
interpolation-
channel fields (`name` / `container_name` / `network_mode` / `ipc` /
`privileged` / `pid`) were already compliant; the guard locks them.
(`container_name` is since gone from the dev-stack emitter entirely --
see the 2026-08-26 amendment above; the field-deploy bundle keeps one.)

### 4. Contract `multi_run` depends on (held, verified)

- `compose.yaml` resolves via `docker compose --env-file .env.generated
  config` -- interpolation defaults keep it resolvable with no overlay.
- `container_name` is **removable** without breaking the service: no
  service references it, and the top-level project `name:` namespaces the
  container, so `multi_run` may drop it entirely to let compose auto-name
  `<project>-<service>-<n>` per instance. (Verified, and then taken: base
  itself stopped emitting it from the dev stack -- 2026-08-26 amendment
  in §3. The wrapper prechecks that used to rebuild the name now ask
  `compose ps` for the service inside `-p <project>`.)
- Stage / service identity is **not tied to the literal name `devel`**:
  each service carries `build.target: <stage>`, `image: .../<stage>`, and
  `profiles: [<stage>]`, so `multi_run` extracts the stage stage-
  agnostically from `build.target` rather than matching the string
  `devel`.

### 5. Forward invariant + guard (the core deliverable)

**Forward invariant:** base's compose emission never emits a hardcoded
per-instance literal over the interpolation-channel field set. base-
generated stacks are composable *by construction*.

**Guard:** `overlay_guard_spec.bats` emits a compose that exercises the
per-instance fields and asserts each is an overlay interpolation, never a
baked literal -- and its predicate self-check proves it *discriminates* a
baked literal from a `${VAR:-default}` interpolation, so it fails
immediately if a future change hardcodes a per-instance field. This turns
"multi_run will not be blocked later" from a hope maintained by discipline
into a machine-enforced guarantee, caught in base's own CI rather than
discovered when multi_run tries to expand -- the same self-validation
spirit as the #800 worker preflight.

## Alternatives

- **Regenerate `compose.yaml` per instance.** Rejected: makes the
  committed artifact per-instance, defeats the single-shape contract, and
  re-flips `SETUP_CONF_HASH` on every instance (ADR-00000003's exact
  anti-goal for workload params).
- **A `compose.override.yaml` merge for every per-instance field.**
  Native and powerful, but forces hand-written compose per instance for
  scalars a flat `${VAR}` handles cleanly; kept as the channel only for
  volume *topology*, where a mount genuinely is structured (ADR-00000001's
  escape-hatch positioning).
- **Convert `runtime` / `hostname` to interpolations too.** Rejected as
  incorrect: they are host-bound and *should* be shared across co-located
  instances (a per-instance hostname would break the local X11 cookie all
  instances share; a per-instance runtime is meaningless on one host).
  Recording them as "shared, not per-instance" is the audit result, not an
  omission.

## Consequences

- `multi_run` can isolate an instance by supplying overlay `${PORT_<n>}` /
  `${NETWORK_MODE}` values (interpolation) and a per-instance `.env.local`
  (env_file; `.env` before #868), with no base change and no compose
  regenerate.
- A future emitter change that bakes a per-instance literal fails
  `overlay_guard_spec.bats` in base's own CI.
- `ports` emission changed shape (now `${PORT_<n>:-<default>}`); downstream
  repos pick it up on their next `just setup` regenerate, with identical
  resolved behaviour (the `:-` default reproduces the prior literal).
- The `#505` golden master and `gen_spec` port assertions were updated to
  the interpolation form; no runtime behaviour changed.
- A consumer upgrading with its stack UP keeps that stack and its old
  project name until the next `stop`, and is told so on every `build` /
  `run`; no container and no named volume is orphaned or duplicated
  (2026-08-26 amendment).
- A consumer whose project holds named volumes keeps its old project name
  indefinitely -- `stop` does not clear them -- and is told, on every
  `build` / `run`, that this is why and what would clear it. The accepted
  cost of never orphaning data is a repeated notice and a project name
  that stays on the pre-upgrade derivation.
- A CONFIGURED `[project] name` still takes effect at once, so it remains
  the one path that CAN strand an old project's containers and volumes;
  `setup apply` says so when it renames.


## ---- FILE: doc/adr/00000023-config-field-override-and-field-deploy-contract.md ----

# Config field-override + self-contained field-deploy contract

> Serves: PRD invariant 8 (development and field are cleanly separated,
> and provisioned by opposite means) -- established (with ADR-00000003);
> also the one-source -> many-render / field-delivery goal.

- **Date:** 2026-07-15
- **Status:** Accepted
- **Relates to:** issue #830 (this decision, the epic anchor), the
  implementing issues #831 (relocate `setup.conf` out of `config/`), #832
  (self-contained resolved-compose deploy bundle), #833 (per-component
  tunable-config manifest + field override); the downstream conventions it
  governs, #826 / #827; ADR-00000003 (env vs workload parameter boundary +
  field delivery -- this ADR amends its structured-config Field cell and its
  "compose does not travel" constraint), ADR-00000001 (setup.conf is the main
  path, compose-native mechanisms are the escape hatch), ADR-00000011 /
  ADR-00000018 (the devel / runtime / `*-test` stage structure),
  ADR-00000022 (compose<->multi_run overlay contract -- reconciled below).

## Context

ADR-00000003 drew the env-var vs structured-config line and gave the **env-var**
row a field override channel (baked `ENV` default + optional `deploy.sh -e`),
but left the **structured-config** row (its routing-table line 115) **bake-only**:
in the field a config file was `COPY`-baked into the image with no override, so
adjusting it required a rebuild. That asymmetry is the concrete gap this ADR
closes, and the epic (#830) needs three related facts written down that were
never stated as a single contract:

- **Who provisions what, and how the dev and field environments stay apart.**
  base has a development environment (binds source, live-edit config, carries
  the toolchain) and a deployable/field environment (a self-contained image).
  The rule for which files a developer owns vs which an operator may edit, and
  the rule for which stages are even eligible to deploy, were unwritten.
- **What travels to the field.** ADR-00000003 said the host-side compose does
  *not* travel (only the image does), which pushed all field-launch config into
  `deploy.sh` `docker run` flags. A resolved compose that carries its own values
  is a cleaner field artifact than a hand-maintained `docker run` line.
- **How a per-component config is made field-tunable** without base having to
  know each downstream's config schema.

This is a doc-only decision (PRD invariant 8 + this ADR + the ADR-00000003
amendment); the mechanism lands in #831 / #832 / #833.

## Decision

### 1. The provisioning axis is git-tracking

The developer-vs-operator split follows a single, checkable axis -- **is the
file committed to the repo?**

- **Committed = the developer's default**, baked into the image at build
  (`COPY`). It is the working default a fresh deploy runs with.
- **Gitignored / not-in-repo / bundle-shipped = the operator overlay**, editable
  in the field. It is mounted over the baked default at launch.

This is the general axis ADR-00000003 made concrete only for env vars (committed
`[environment]` default vs gitignored user overlay); this ADR names it as the
axis for **structured config files** too.

**Amendment (#868): which file is the env overlay changed name, the axis did
not.** The overlay is `.env.local`, not `.env` -- ADR-00000003's A2 was
reversed so one rule (the standard name is ours, a suffix marks a local
variant) covers `Dockerfile` / `compose.yaml` / `.setup.conf` and the env
family alike. The axis this section states is untouched: `.env.local` is
gitignored, so it is still "not in the repo = the operator's".

### 2. Baked default + optional mount-override (mount-wins)

A field config file is a **`COPY`-baked default** in a deployable stage, plus an
**optional field `-v` override** that mounts a file over it. When the operator
mounts a file, the mount wins; when they mount nothing, the baked default is
used. This is the exact file analog of ADR-00000003's env-row `deploy.sh -e`:
a self-contained default that a deployment can adjust **without a rebuild**,
restoring the symmetry between the two routing-table rows.

**Amendment (#870): the override mount is read-only by default, `rw` is
declared.** As first written this section said nothing about writability, and
the implementation defaulted to a writable bind. That default was wrong in
both directions. Nothing in "the operator retunes a value" requires the
*container* to write -- the operator edits the copy in the bundle on the host
and the container reads it -- and a writable bind quietly makes the mount
depend on the container's build-time user id matching whoever unpacked the
bundle on the field host: reads work under any id, writes fail, months later,
on the one machine that matters. So each `deploy.manifest` path mounts `:ro`
unless it declares `rw`, which makes the exception reviewable data rather than
a blanket grant, and an unrecognised token on a manifest line is a malformed
manifest that fails loud naming file and line -- never a silent skip, never a
silent downgrade. An absent access record can only tighten a mount, never
loosen one.

### 3. Deploy travels as a fully-resolved, self-contained compose

ADR-00000003 said "the compose does not travel" -- only the image did, and the
field launcher was a `docker run` (`deploy.sh`) with flags inlined. This ADR
**amends that**: a *fully-resolved, self-contained* compose **does** travel. The
deploy bundle (#832) ships a compose whose values are already resolved -- it has
**no dependency on `setup.conf` or `.env.generated`** (the host-side
generation inputs), so it runs on a field host that never had base's
detection / render toolchain. "Compose does not travel" was true of the
*generated, interpolation-dependent* compose; a resolved compose is a distinct,
self-contained artifact and is the field launcher.

**Amendment (#868):** that compose does carry an `env_file:` naming `.env` +
`.env.local`, and both travel INSIDE the bundle. Self-containment is about
not depending on the BUILD host; a file shipped in the folder is part of the
artifact. It is what gives the operator an env channel at all -- the old raw
`docker run` launcher had `deploy.sh -e` and nothing replaced it when the
resolved compose took over.

### 4. `deployable = not devel and not *-test`

Only field-oriented stages are deploy targets. The **`devel` stage and any
`*-test` stage are never deploy targets** -- a devel image binds source and
carries the toolchain, and a test image exists to be tested, not shipped.
Formally, `deployable = not devel and not *-test`; every downstream repo binds
to this rule (it is the stage-eligibility half of PRD invariant 8, and the
convention #826 / #827 make downstream-explicit).

**Amendment (#841 / #874): the implementing predicate rejects two more
names.** `_is_deployable_stage` (`lib/stage.sh`) also rejects **`sys` and
`devel-base`** -- build intermediates with no runnable service, so a bundle
built from one is simply broken, not merely inadvisable -- alongside the
legacy aliases `base` / `test` the v0.21.x transition still accepts. The
formula above was the reasoning; the predicate is the rule, and PRD invariant
8 now states it in full so prose and predicate cannot disagree.

### 5. Per-stage tunability via `config/<component>/deploy.manifest`

A component declares which of its config files are field-tunable in a
`config/<component>/deploy.manifest`. **base delivers the files** named by the
manifest into the deploy bundle (as baked defaults + the mount-override hook of
§2); **the repo's entrypoint consumes them**. base does not need to understand
any downstream's config schema -- it moves the files the manifest lists and
wires the override hook; the semantics stay with the repo. This keeps base the
thin mechanism and the downstream the owner of its own config meaning
(consistent with invariant 6).

### 6. Reconciliation with ADR-00000022 (not a contradiction)

ADR-00000022 routes **writable-volume topology** through a **compose-merge
overlay** (a mount is a structured topology decision, not a flat scalar). This
ADR's §2 single-file config `-v` on the **field launcher** is a **distinct
concern** and does **not** reopen that: it is one config file overriding one
baked default on the deploy launcher, not a general volume-topology channel.
General writable-volume topology stays compose-merge per ADR-00000022; the
field-launcher config `-v` is a narrow, single-file override of a baked default.
Stated explicitly so the two `-v` uses do not read as a conflict.

## Alternatives

- **Keep structured config bake-only (status quo).** Rejected: it is the exact
  asymmetry that forces a rebuild to change one field value in the field, and it
  leaves the env row and the config row inconsistent for no principled reason.
- **Route field config through the env overlay too.** Rejected: the env
  overlay (ADR-00000003; `.env.local` since #868) carries flat `KEY=VALUE`
  entries only; a structured config file (topics, pipeline lists, YAML) is not
  a flat scalar and belongs in its own file with its own mount-override, not
  smuggled through env.
- **Ship the generated, interpolation-dependent compose to the field.**
  Rejected: it depends on `setup.conf` / `.env.generated` being present on the
  field host, which is exactly what a field host does not have. A resolved,
  self-contained compose is the artifact that travels (§3).
- **Let each downstream hand-roll its own field-override wiring.** Rejected:
  duplicates the mechanism N times and drifts (the fat-caller anti-pattern of
  invariant 6). base delivers the files + hook once, driven by the per-component
  manifest (§5).

## Consequences

- The structured-config Field cell of ADR-00000003's routing table becomes
  symmetric with the env row: baked default + optional mount-wins `-v` (recorded
  as an amendment on ADR-00000003).
- A field deploy adjusts config without a rebuild (mount a file), and runs on a
  host with no base toolchain (the resolved compose is self-contained).
- The git-tracking axis becomes the single checkable rule for "developer default
  vs operator overlay" across both env vars (already) and config files (now).
- `deployable = not devel and not *-test` is a downstream-binding rule; #826 /
  #827 make it explicit in the downstream `config/<component>/` convention.
- Implemented by #831 (relocate `setup.conf` out of `config/`), #832
  (self-contained resolved-compose deploy bundle), #833 (per-component tunable
  `deploy.manifest` + field override). This ADR records the rationale; those
  issues carry the mechanism.


## ---- FILE: doc/adr/00000024-bake-artifacts-at-opt-not-home.md ----

# Bake self-built artifacts at absolute `/opt`, not under `$HOME`

> Serves: PRD invariant 8 (dev/field separation, provisioned by opposite
> means) -- mechanism; also invariant 2 (never fail silently), through the
> `home-literal` lint that gates its mechanical half.

- **Date:** 2026-08-03
- **Status:** Accepted
- **Relates to:** issue #799 (this decision), issue
  `realsense_ros2#97` (the design that surfaced it: build librealsense +
  realsense-ros from source and choose where the SDK and the colcon overlay
  land), ADR-00000023 (field deploy: the image travels, the build host does
  not)

## Context

The template bakes the container user at **build** time. The `sys` stage
takes the `USER_NAME` / `USER_UID` / `USER_GID` build args (injected by
compose and by CI), creates that user, and the `devel` stage then sets

```dockerfile
ENV HOME="/home/${USER_NAME}"
```

So `$HOME` inside the image is not a deploy-time property; it is frozen to
whichever `USER_NAME` the build received. `just build` injects the local
host's user. CI and the release path bake `user` (UID 1000). Two images
built from the same commit can therefore have two different `$HOME` values.

That makes any artifact baked **under `$HOME`** -- a self-built workspace at
`~/some_ws`, an SDK, a compiled tool -- coupled to the build-time username.
The coupling only bites at deploy time, which is exactly where it is
hardest to see:

- A consumer runs a **prebuilt / GHCR / `docker save`+`load`** image baked
  as `user:1000` on a host whose user differs, or rebuilds with a different
  `USER_NAME`. Every path that goes through the home directory -- a
  Dockerfile `COPY` destination, entrypoint sourcing, a bashrc line --
  now points at a **different, empty** `/home/<other>/...`. The baked
  workspace is invisible and `source ~/some_ws/install/setup.bash` fails.
- A single **hardcoded literal** home path is worse: it does not even track
  `USER_NAME`, so it breaks the moment the build arg changes. This repo has
  already hit the neighbouring class of bug ("image `HOME` != compose
  mount", healed by the `ARG USER` migration in `lib/dockerfile_migrate.sh`).

Content baked at an **absolute, username-agnostic** path (`/opt/...`) is
immune to all three -- username change, UID mismatch, tar load -- because
there is no `$HOME` indirection left to resolve. This is also what the
ecosystem already does: `/opt/ros/<distro>` is where every upstream ROS
image puts its install tree, and nothing sources it through a home
directory.

The decision was forced by `realsense_ros2#97`, which had to choose where a
self-built librealsense plus a colcon overlay live. It generalises: it is a
property of how the template bakes users, not of that repo.

## Decision

**Images bake self-built artifacts at absolute `/opt/<name>` paths.
`$HOME` is reserved for dotfiles and convenience symlinks.**

1. **Artifacts at `/opt`.** Self-built workspaces, SDKs and compiled tools
   install at absolute `/opt/<name>`. Nothing whose survival matters is
   baked under `$HOME`.
2. **Sourcing names the absolute path.** The entrypoint / bashrc sources
   `/opt/<name>/...`, never `~` or `$HOME`. A per-user
   `~/<name> -> /opt/<name>` symlink created in the per-user `RUN` block is
   *encouraged* for interactive discoverability -- it is the only
   user-coupled bit and is cheap to recreate -- but it must never be the
   path anything **sources**.
3. **No concrete username in a path.** Where a home path is genuinely
   needed, it uses `${HOME}` / `${USER_NAME}` so it tracks the build arg.

Rule 3 is mechanical, so it is **gated**: `script/test/drivers/home_literal.sh`
(`just test lint --home-literal`, CI job `lint-static (home-literal)`) fails
on a concrete username in a home path anywhere under `dist/` or
`dockerfile/` -- the trees that reach an image. A narrative mention (the
`dockerfile_migrate.sh` note that must name the *wrong* home directory in
order to explain the mismatch it heals) opts out through an explicit,
region-delimited allowlist, not a file exclusion, so a new literal in the
same file is still caught.

Rules 1 and 2 are **judgement**, not a mechanical property: whether a given
artifact belongs under `/opt` cannot be decided by a grep, and the lint does
not pretend otherwise. They are carried where a downstream author meets them
-- the commentary in the shipped `dist/dockerfile/Dockerfile`, which
`init.sh` seeds as every repo's own `Dockerfile` -- plus the README section
for readers who never open the Dockerfile, and this record for the why.

## Consequences

- **Deploy-robust by construction.** A `docker save` / `load` or a GHCR
  pull onto a machine with a different user keeps working: nothing the image
  needs is behind a username.
- **The build-arg user stays a dev-ergonomics knob**, which is all it was
  ever for (matching host UID so bind-mounted files are writable). It stops
  being load-bearing for image content.
- **Two paths for the same thing.** `/opt/some_ws` and `~/some_ws` both
  exist, and a reader has to know the symlink is for humans while the
  absolute path is for machines. That is the accepted cost of rule 2; the
  alternative (no symlink) trades an interactive convenience the team
  actually uses for one less concept.
- **Downstream repos need a fanout**, not just base. base ships no
  self-built artifact of its own -- the audit found zero live violations in
  its shipped tree -- so the convention lands here as guidance plus a lint
  over base's own tree. Repos that bake a workspace (starting with
  `realsense_ros2`, and any repo with a `~/*_ws` build) adopt it in their
  own Dockerfile / entrypoint, and pick up the lint automatically as they
  upgrade the `.base` subtree.
- **The lint sees only what `.base` carries.** A downstream literal in the
  repo's OWN `Dockerfile` / `script/entrypoint.sh` is outside the scanned
  trees. Extending the scan to a consumer's root is a separate decision
  (it needs the lint to run from a downstream `just test`, which base does
  not own today); until then rule 3 is enforced in base and reviewed
  downstream.

## Alternatives

**Amendment (#994, 2026-09-03):** this section was added when
`adr_structure.sh` made Alternatives a required part of the format. It is
reconstructed from the options this decision's own Context and
Consequences already weigh -- it is not a later re-deliberation, and
nothing below changes what was decided.

**Keep artifacts under `$HOME`, but always spell the path
`${HOME}` / `${USER_NAME}` so it tracks the build arg.** This is the
narrower fix, and it is the one rule 3 keeps for the cases where a home
path is genuinely wanted. Rejected as the general answer because tracking
the build arg is not the problem: a path that correctly resolves to
`/home/<other>/some_ws` on a `docker save`+`load` or a GHCR pull is
pointing at a different, empty directory, and it fails the same way a
literal does. The indirection has to go, not be spelled better.

**Fix it at deploy time -- pass the right `USER_NAME` when running a
prebuilt image.** Rejected: `ENV HOME` resolves at BUILD time, so the
value is already frozen in the image the consumer pulled. There is
nothing a run-time flag can change, and the failure surfaces as an empty
directory rather than an error, which is invariant 2's silent failure in
the place it is hardest to diagnose.

**Drop the `~/<name> -> /opt/<name>` symlink** and have exactly one path
for one thing. Rejected in Consequences: it buys one less concept at the
cost of an interactive convenience the team actually uses. The symlink is
kept, and rule 2 draws the line that makes it safe -- it exists for humans
at a prompt, and nothing may `source` through it.

**Extend the `home-literal` lint to a consumer's own `Dockerfile` and
`script/entrypoint.sh`.** Not rejected -- deferred, and recorded in
Consequences. It needs the lint to run from a downstream `just test`,
which base does not own today; until then rule 3 is gated inside base's
shipped trees and reviewed downstream.

**Ship this as guidance only, with no lint.** Rejected. Rule 3 is
mechanical -- a concrete username in a path is decidable by inspection --
and base's own experience is that a non-gating convention is followed for
as long as somebody remembers it. The rules that need judgement (1 and 2)
stay guidance; the one that does not is gated.


## ---- FILE: doc/adr/00000025-per-worktree-setup-conf-local-override.md ----

# Per-worktree `.setup.conf.local` override, and one resolved project name

> Serves: PRD invariant 9 (runtime-name divergence comes from an explicit,
> file-recorded override) -- established by this decision; also invariant 2
> (never fail silently: the shadowed-write warning, the deploy refusal, the
> config-summary row) and invariant 8 (dev/field separation: the field
> refusal).

- **Date:** 2026-08-05
- **Status:** Accepted
- **Relates to:** issue #893 (this decision), #891 / #892 (the same
  collision on the test path, fixed there), #600 (removal of
  `--instance` / `INSTANCE_SUFFIX` / `config/instances/` -- NOT reversed
  here, see sec. 6), #201 (removal of the earlier committed
  `setup.conf.local` -- sec. 2), #879 (retired the leftover `.gitignore`
  line -- sec. 7), #875 (one question, several answerers -- sec. 4);
  ADR-00000001 (setup.conf is the main path), ADR-00000003 (env vs
  workload boundary), ADR-00000011 (naming convention / `dist` layout),
  **ADR-00000022** (compose<->multi_run overlay contract -- amended
  in-file with a pointer to sec. 5's division of labour),
  ADR-00000023 (config field-override + field-deploy contract -- sec. 8
  extends its dev/field split to an untracked config layer).

## Context

Two worktrees of one repo could not be run at the same time, and there was
no way to make them differ.

This is verified rather than assumed. `run.sh` loads `.env.generated` and
then calls `_compute_project_name`, which assigned unconditionally:

```bash
PROJECT_NAME="${DOCKER_HUB_USER:-local}-${IMAGE_NAME:-$(basename -- "${FILE_PATH:-${PWD}}")}"
```

There was no `${PROJECT_NAME:-...}`, so exporting `PROJECT_NAME` was
overwritten. `COMPOSE_PROJECT_NAME` was ignored because `_compose_project`
passes `-p` explicitly and an explicit `-p` beats the environment. And
`.env.local` was never loaded on that path. The only lever left was
`IMAGE_NAME` or `DOCKER_HUB_USER` -- which also moves the **image tag**,
coupling two things that should be independent: which containers a run
owns, and which image it built.

Underneath the missing lever sat a second problem. The compose emitter
wrote `name: ${DOCKER_HUB_USER}-${IMAGE_NAME}` into `compose.yaml` while
the wrapper assembled the same string in bash, and the CLI `-p` silently
won over the file. Two independent answerers to one question that happened
to agree -- the #875 shape.

## Decision

### 1. A gitignored `<repo>/.setup.conf.local`, overriding any section

The conf chain becomes three files, lowest precedence first:

| Layer | Tracked | Whose | Serves |
|---|---|---|---|
| `<template>/.setup.conf` | shipped in `.base` | base's | the default |
| `<repo>/.setup.conf` | committed | the repo's | what CI and every checkout use |
| `<repo>/.setup.conf.local` | gitignored | the operator's | this worktree, this machine |

The repo's own file-naming convention already says this: the standard name
is ours (shipped or generated, replaced on update, never hand-edited per
instance); a suffix marks the operator's local variant, never touched by
tooling. `.setup.conf.local` is exactly that shape, and it is the same
relationship `.env.local` has to `.env`.

It may override **any** section, not a whitelist. multi_run-era work is
expected to need many per-worktree variations, and adding them one section
at a time is churn with no safety benefit -- the layer is already
operator-owned and machine-local.

### 2. Why this is not a relapse into what #201 removed

#201 deleted a **committed** `setup.conf.local` that sat inside a redundant
three-file chain whose third file was a derived snapshot nobody read. Its
stated complaint was that the `.local` suffix *looked* gitignored while it
was not. The convention adopted since makes `.local` mean precisely what
#201 said it did not, and the file is now genuinely gitignored (sec. 7).
The chain is also two layers of real config plus this one, not a config
file plus a stale snapshot of itself.

### 3. Section-replace, matching the layer below

Not per-key merge. The decisive reason is structural rather than
aesthetic: **eight of the fifteen sections are `<prefix>_N` ordered
lists** (`[image] rule_N`, `[build] arg_N`, `[network] port_N`,
`[security] cap_add_N` / `security_opt_N`, `[devices] device_N`,
`[volumes] mount_N`, `[tmpfs]`, `[additional_contexts]`). A per-key merge
over an ordered list is not merely inconsistent, it is broken:

- overriding `rule_2` alone yields the repo's `rule_1` + the local
  `rule_2` + the repo's `rule_3` -- one ordered list assembled out of two
  layers, describing a configuration neither layer wrote;
- an item cannot be **removed** at all;
- adding one requires knowing the highest `N` in a layer the author of the
  upper layer cannot see.

Keys within a section also gate each other -- `[network] mode` decides
whether `port_N` is emitted at all, `[deploy] gpu_mode` gates the rest of
the GPU keys -- so a partial override produces incoherent combinations.

The layer below already worked this way. One rule for the whole chain.

**Amendment (ADR-37 D4 #1130, 2026-09-07): type-aware merge for TOML
layers.** The ordered-list argument above remains correct and is the
basis for the array-replace half of the TOML merge rule. When the
chain is `.setup.toml` (TOML format), the merge becomes type-aware:
scalar keys within a `[table]` get key-level merge (upper layer
overrides only the keys it defines; unmentioned keys inherit from the
lower layer), while `[[array of tables]]` get array replace (the
entire array comes from the highest layer that defines it). This
resolves the "eight ordered-list sections" concern by replacing only
whole arrays, while allowing scalar sections (e.g. `[gui]`, `[deploy]`)
to benefit from key-level override. The INI `.setup.conf` chain retains
blanket section-replace unchanged.

### 4. `[project] name`, and one resolved project name

`[project]` is a real section of the shipped template with one key,
`name`, and it **ships empty**, meaning "derive as before". Upgrading
therefore changes nothing for any existing repo.

It must exist in `.setup.conf` and not only in `.setup.conf.local`:
`.setup.conf.local` is the local *variant* of `.setup.conf` and shares its
grammar. A section that appeared only in `.local` would be a second schema.

The resolution has exactly one producer, `_resolve_project_name` in
`lib/compose.sh`. `setup apply` calls it once and records the result in
`.env.generated` as `PROJECT_NAME`; **both** consumers then read that one
value:

- the wrapper's `-p`, via `_load_env`;
- the emitted `compose.yaml`'s `name: ${PROJECT_NAME}`, interpolated from
  the same `--env-file`.

`template_spec` fails if any other shipped file assembles a project name.
The emitted form stays an interpolation, not the resolved literal, so
ADR-00000022's overlay contract for project `name:` continues to hold
(its guard is unchanged).

Two names remain deliberately distinct. The **image tag**
(`<hub>/<image>:<stage>`) is a separate axis -- that separation is the
whole reason moving `IMAGE_NAME` was the wrong lever. And the **field
bundle's** project stays `<name>-<stage>` per ADR-00000023: it is a
different artifact, on a different host, deliberately stage-qualified.

### 5. Division of labour with the ADR-00000022 overlay

These are different stages of the pipeline and neither substitutes for the
other:

| | `.setup.conf.local` (this ADR) | ADR-00000022 `.env` overlay |
|---|---|---|
| serves | a developer's worktree | multi_run's Nth instance |
| acts | **before** `compose.yaml` is generated | at interpolation time on an already-generated one |
| `compose.yaml` count | one per worktree | one, shared |

Recording this is part of the decision. Without it a future reader
reasonably assumes this is how multi_run isolates instances -- and it
cannot be, because multi_run runs N instances off **one** generated
`compose.yaml`, which a per-worktree config layer by construction does not
produce. multi_run overriding `PROJECT_NAME` in its runtime overlay
continues to work unchanged; that is ADR-00000022's table row.

### 6. Why this is not a reversal of #600

> **Amended 2026-09-06 by ADR-00000036 (#1087).** The per-worktree / per-instance
> line this section draws was a consequence of `.setup.conf.local` having exactly
> one location: "another parameter set" could only mean "another checkout". The
> file's path now becomes caller-supplied, and the same layer serves both axes --
> a developer still gets the per-worktree file at the default path, an
> orchestrator passes its own. The layer's semantics are unchanged:
> section-replace, overrides any section, gitignored at the default path. What
> changes is only that the address is an argument rather than a constant.

#600 removed `--instance` / `INSTANCE_SUFFIX` / `config/instances/<name>`
from base on layering grounds: base is `docker` (single instance),
multi_run is `docker compose` (orchestration). That stands. A **named
project override is configuration** -- one name, for this checkout,
recorded in a file, resolved by the same machinery as every other key --
not a multi-instance orchestration surface. base still emits one project
per checkout; it simply no longer forces every checkout to pick the same
name.

### 7. `.setup.conf.local` is canonically gitignored

#879 moved the leftover `.gitignore` line to the RETIRED list, which does
not merely stop emitting it -- it actively **prunes** it from every
downstream `.gitignore` on each sync. That was correct while nothing read
the file. It is now exactly wrong, so the entry is canonical again and the
retired list is empty.

Both halves had to move in one edit: an entry present in *both* lists is
retracted and re-appended on every sync, forever, in every downstream at
once. A standing spec now asserts the two lists are disjoint. That
retirement was also **unreleased** (it sat in the commits after
`v0.42.0-rc3`), so no downstream ever saw the line disappear.

`.dockerignore` shares the canonical list and gains the entry too:
untracked machine-local config inside a build context is how an
unversioned value ends up baked into an image.

### 8. Writes: `--local`, warned-not-refused, and the field refusal

`set` / `add` / `remove` keep writing the committed `.setup.conf`.
`--local` targets `.setup.conf.local`.

Writing the committed file while `.setup.conf.local` defines that section
is **warned, not refused**, and the asymmetry is the decision. Under
section-replace the write is provably inert *on this machine*, so the
warning is stated as a certainty rather than a possibility, names the
shadowing section, and points at `--local`. But the value is still the
committed, shared setting that CI and every other checkout use, so
refusing would block a legitimate write on the grounds that one machine
cannot observe its effect. This is the failure mode the earlier committed
`setup.conf.local` died of -- a write landing where the read path does not
look -- which is why it is a hard requirement and not a nicety.

`setup deploy` **refuses** while `.setup.conf.local` exists, before the
preview and before any build side effect, so even `--dry-run` reports the
refusal rather than previewing a plan that would not be allowed to run.
`--allow-local-override` is the escape hatch, and the bundle's own README
records which untracked sections it was built from -- written by the
bundle *generator*, so the record travels with the artifact and reaches
the person in the field, who is not the person who chose to bypass the
gate.

### 9. `SETUP_CONF` is removed

`SETUP_CONF` was an undocumented env var that replaced the **whole**
config resolution with one path ("only read from it, no merge"). It was
introduced as a test seam -- its own first comment said
`SETUP_CONF env var (test override)` -- and then spread by five mechanical
refactors that each copied it verbatim, including its inconsistent
existence-checking: the two `setup_conf.sh` readers did **not** check the
file existed (a typo'd path silently yielded an EMPTY config), while
`conf_logging.sh` and `stage.sh` did, and degraded differently. It was
also folded into the drift hash by *concatenation* with the template and
repo files even though resolution used it alone, so `SETUP_CONF_HASH` did
not describe the config that was actually resolved.

Nothing but one spec set it, and roughly 120 spec `setup()` bodies
explicitly `unset` it -- the suite already treated an ambient value as a
hazard. Users are not meant to relocate the conf: the fixed pair
`<repo>/.setup.conf` + `<repo>/.setup.conf.local` is the whole surface.
The specs that used it as a fixture now drive real files at the paths the
resolver reads.

## Alternatives

- **A `PROJECT_NAME` / `COMPOSE_PROJECT_NAME` environment variable.**
  Rejected, and it is what PRD invariant 9 forbids: an ambient value is
  invisible to anyone reading the repo, does not survive a new terminal,
  and cannot be reviewed. Divergence in runtime naming between two
  checkouts has to be *recorded in a file*.
- **Deriving the project name from the checkout path.** Rejected for the
  same reason #892 stopped `docker compose` doing it on the test path: a
  name that changes when a directory is renamed or moved is an accident,
  not a decision, and two checkouts that happen to share a basename
  silently share containers.
- **Per-key merge for the local layer.** Rejected on the ordered-list
  argument in sec. 3. Someone will propose it again; the answer is that
  eight of the fifteen sections cannot express a removal or a
  well-defined insertion under it.
- **A whitelist of overridable sections.** Rejected: the layer is
  operator-owned and machine-local, so a whitelist adds churn (a PR per
  new key) without adding a safety property that the deploy refusal does
  not already provide.
- **Refusing a shadowed write instead of warning.** Rejected in sec. 8.
- **Reusing the ADR-00000022 `.env` overlay for worktree isolation.**
  Rejected as a category error (sec. 5): the overlay acts on an
  already-generated `compose.yaml` and cannot change what gets generated.

## Consequences

- Two worktrees of one repo run concurrently after
  `./setup.sh set --local project.name <x>` in one of them, through the
  wrappers alone -- no hand-edited derived artifact, no environment
  variable.
- With no `.setup.conf.local` present, behaviour is unchanged: the
  resolved project name is the same `<hub>-<image>` string as before, and
  the template's new `[project] name` ships empty.
- `.env.generated` gains `PROJECT_NAME`; `compose.yaml`'s `name:` changes
  from `${DOCKER_HUB_USER}-${IMAGE_NAME}` to `${PROJECT_NAME}`. Downstream
  repos pick both up on their next regenerate, which the conf-hash drift
  check triggers automatically because the template gained a section.
- An `.env.generated` written before this change carries no
  `PROJECT_NAME`; the wrapper says so and derives one for that run rather
  than silently inventing a name whose source the user cannot trace.
- Adding a fifteenth section pulls in `SCHEMA_SECTIONS`, a
  `SCHEMA_VALIDATOR` (`_validate_project_name`: docker compose's own rule
  -- lowercase letters, digits, `-`, `_`, beginning with a letter or a
  digit; deliberately tighter than the network-name rule, which permits
  uppercase and dots) and a `SCHEMA_I18N` row. That row is the explicit
  no-editor opt-out: the TUI edits the *committed* `.setup.conf`, while a
  per-worktree name belongs in `.setup.conf.local`, so a menu row would
  edit the wrong file by default.
- `SETUP_CONF` no longer exists. Any out-of-tree script that set it was
  silently replacing the whole config; it now has no effect at all, which
  is the intended outcome.


## ---- FILE: doc/adr/00000026-self-hosted-eligibility-is-a-static-property-of-runs-on.md ----

# Self-hosted eligibility is a static property of `runs-on`, and the guard is linted rather than remembered

> Serves: PRD invariant 7 (rigorous test bar) -- the CI gate must be
> trustworthy, which includes not executing untrusted code on the org's
> own hardware and not reporting a partial run as a full one.

- **Date:** 2026-08-26
- **Status:** Accepted
- **Relates to:** ADR-00000017 (CI throughput ceiling; names this guard as
  the hard prerequisite for any self-hosted migration), ADR-00000008
  (sharded coverage PR gate / ci-rollup as the single required check),
  issue #766

## Context

`base` is a **public** repo. The org registers **one org-level self-hosted
runner**, and the settings that matter were checked rather than assumed:

- `GET /orgs/ycpss91255-docker/actions/runners` -> one runner,
  `C01013328-ycpss91255-docker-org`, `status=online`, labels
  `self-hosted, Linux, X64, gpu`.
- `GET /orgs/ycpss91255-docker/actions/runner-groups` -> a single `Default`
  group, `visibility: all`, **`allows_public_repositories: true`**,
  `restricted_to_workflows: false`.
- `GET /repos/ycpss91255-docker/base` -> `visibility: public`.
- `GET /repos/.../actions/permissions/fork-pr-contributor-approval` ->
  `all_external_contributors`.

The runner is a developer workstation (`hostname` = `C01013328`) that also
hosts unrelated tenants -- a second runner tree for `ycpss91255-research`,
a GitLab runner container, long-running GPU workloads. So "the machine a
fork PR could reach" is not a hypothetical future box; it is the machine
the maintainer works on.

ADR-00000017 recorded self-hosted as a documented-but-gated path and named
this guard as its prerequisite. The remaining question was not *what* the
condition should be -- the issue already wrote it -- but **how to make
"every eligible job carries it" survive the next person who adds a job.**

That question has a track record in this repo. A hand-maintained roster of
"the things that must all be listed" has decayed three separate times: the
`_LINT_TOOLS` table (lints landed local-only because nothing forced a CI
join), the downstream repo roster, and the release archive's hardcoded
path list (which shipped the same class of break twice, on a different
path each time). A guard applied by hand to today's N jobs is the same
shape and would fail the same way at job N+1.

## Decision

### 1. Eligibility is computed from `runs-on`, not from a list of job names

A job is **self-hosted-eligible** unless a lint can PROVE, statically, that
every label its `runs-on` can resolve to is a **reserved GitHub-hosted
label** (`ubuntu-*`, `windows-*`, `macos-*`). Anything unproven defaults to
eligible -- the rule fails closed.

Resolution follows, in order: a literal scalar or literal sequence; then
`${{ matrix.<key> }}` resolved against the job's **own literal**
`strategy.matrix` (both the `include:` form and the bare list form).
Everything else is eligible: a `group:` child (a runner group has no
hosted reading), a `matrix: ${{ fromJSON(...) }}` whose label set is
computed at runtime, `${{ inputs.runner }}` or any other expression, and a
job with no `runs-on` that calls a **remote** reusable workflow (a local
`uses: ./...` is exempt, because the callee's own jobs are checked where
they are defined).

**Why a label-family pattern rather than a roster.** Those three families
are reserved by GitHub and cannot be claimed by a self-hosted runner, so
membership is a property of the label decided by GitHub -- not a list this
repo maintains and must remember to update. The rule therefore survives a
migration untouched: the day any `runs-on` stops naming one of those
families, that job needs the guard, whether it was written today or years
from now. Note that the org runner's own `Linux` and `X64` labels fall
outside the allow-list too, which is the intended reading.

### 2. The guard is enforced by a lint in `_LINT_TOOLS`, not by review

`script/test/drivers/self_hosted_guard.sh` scans `.github/workflows/` --
the directory, not a file list -- classifies every job by the rule above,
and fails naming each eligible job that lacks the condition, printing the
condition verbatim so it can be pasted. It is registered in `_LINT_TOOLS`,
which (via the existing completeness guard in `self_test_yaml_spec`)
*forces* it to have a CI job; it runs as a `lint-static` matrix entry and
in the local `just test` lint phase. Like the other drivers it carries its
own non-vacuity checks: a missing workflow directory, an empty one, or a
parse that yields zero jobs is a failure, not a pass.

### 3. The condition is a FORK test, not a PR test

```yaml
if: >-
  github.event_name != 'pull_request' ||
  github.event.pull_request.head.repo.full_name == github.repository
```

A same-repo PR passes on the second disjunct. A branch push, a **tag
push**, `schedule` and `workflow_dispatch` pass on the **first** disjunct
without ever reading the `pull_request` payload -- which is `null` for
those events, so the second disjunct alone would be wrong and would
silently disable the release path. Under `workflow_call` the `github`
context is the **caller's**, so inside a reusable worker the condition
reads "the calling repo's run was not started by a fork PR against that
repo" -- the correct question, since it is the caller's fork PR whose code
the worker would build.

A job may AND the guard with its own gate; what the lint requires is that
the canonical expression appear verbatim in the normalised `if:` text, so
`<existing> && (<guard>)` satisfies it and a reworded near-miss does not.
`github.repository_owner`-style rewrites are the specific trap: they pass
for every fork inside the same org, which is not the property being
asserted.

### 4. A guarded skip must never make `ci-rollup` vacuously green

This is the half that is more dangerous than the risk being closed. The
guard's effect is a **skip**, and `ci-rollup` treats SKIPPED as
pass-equivalent for conditionally-gated jobs (it has to, or doc-only PRs
could not merge). `worker-selftest` calls `build-worker.yaml`, whose
`build` job now carries the guard: on a fork PR that job skips while the
worker's other jobs succeed, so `needs.worker-selftest.result` is
`success` and the rollup would report a build that never ran as a green
**required** check -- for precisely the untrusted PR.

So `ci-rollup` carries an explicit fork-PR branch that sets `fail=1` with a
named reason. A required check is a claim that the commit was fully
tested; on a fork PR that claim is false, and the honest answer is red with
an explanation, not green. The maintainer's path for an external
contribution is to re-push it as a same-repository branch, which is the
standard posture for a public repo whose org owns a self-hosted runner.

## Consequences

- Today's eligible set is exactly three jobs -- `build-worker`'s `build`,
  `publish-worker`'s `publish`, `release-test-tools`'s `build` -- all three
  eligible for the same reason (a `fromJSON` runtime matrix). Every other
  job in the tree resolves statically to a reserved hosted label and is
  deliberately **not** guarded, so fork PRs keep getting real CI on
  GitHub-hosted runners for everything the lint can prove is safe.
- The change is operationally inert on every event that exists today:
  `release-test-tools` has no `pull_request` trigger at all, `publish-worker`
  is called from tag-push release flows, and `build-worker`'s only changed
  behaviour is that a **fork** PR of a consuming repo no longer builds.
  There are zero fork PRs in this repo's history.
- A self-hosted migration cannot silently land unguarded: pointing any
  `runs-on` at a non-hosted label, or adding a self-hosted entry to a
  literal matrix (which does not change the `runs-on` line at all), turns
  the lint red until the condition is added.
- The eligible **count** is pinned in the spec, so a change to the eligible
  set is a deliberate edit rather than a silent drift.
- Cost: three jobs whose runner label is genuinely hosted today carry a
  condition they do not yet need. That is the price of the fail-closed
  default, and it is paid where the migration would start anyway.

## Alternatives

- **Apply the condition to every job.** Rejected: it would skip the whole
  suite for a fork PR, and with the rollup's SKIPPED=pass rule that
  converts the required check into a vacuous green -- the exact class this
  cycle has been clearing out. It also removes any CI signal from external
  contributions for a risk that only attaches to some jobs.
- **Apply it only to jobs whose `runs-on` literally says `self-hosted`.**
  Rejected: that is a *detector for the migration having already happened*,
  not a prerequisite for it. It cannot see a self-hosted entry added to a
  matrix, a runner group, or a runtime-computed label set.
- **A hand-maintained list of guarded jobs, checked by a spec.** Rejected
  on this repo's own record: `_LINT_TOOLS`, the downstream roster and the
  release archive path list all decayed exactly this way. The list has to
  be derived from the file, not written beside it.
- **Solve it by runner selection instead (force fork PRs onto hosted
  runners).** Attractive because fork PRs would keep full CI, but it
  requires every job's `runs-on` to become an expression -- which, under
  the rule above, makes every job unprovable and therefore eligible, and
  moves the safety property into a computed value no static check can
  read. Rejected as strictly harder to verify than the `if:`.
- **Rely on `fork-pr-contributor-approval = all_external_contributors`
  alone.** Rejected: it is a human gate, and the residual risk this ADR
  closes is exactly the day a maintainer approves an external PR without
  realising a job now runs on the workstation. It remains a useful second
  layer, not the mechanism.
- **Restrict the runner group instead (`allows_public_repositories:
  false`, or `restricted_to_workflows`).** Not rejected -- a genuinely good
  complementary control, and cheaper than this one. But it is org
  configuration, invisible in the repo, unversioned and untestable from
  here; a repo-local guard that CI enforces is the part that belongs in
  the repo. Worth doing as well, not instead.


## ---- FILE: doc/adr/00000027-release-cadence-and-fanout-trigger.md ----

# Release cadence and fanout trigger: Z is automatic and per-bug, X/Y are human, and only X/Y fans out

> Serves: PRD invariant 6 (base is a subtree; downstream is a thin
> caller) -- this is the cadence at which the single source of truth
> actually propagates, and who decides each step; also invariant 2 (never
> fail silently) via the recorded classification reasoning, which is what
> makes a mis-classified release reviewable instead of invisible.

- **Date:** 2026-08-28
- **Status:** Accepted
- **Amended:** 2026-09-03 (ADR-00000031) -- sections 1 and 3 gain a
  third actor. A Z may also be cut by a GATE, with no person and no
  agent in the loop, in the one case a gate can decide: a downstream
  repo's ABI-safe dependency bump. See the amendment section at the
  end of this record.
- **Relates to:** the `semver-bump` skill and `/release`
  (`.claude/commands/release.md`) -- the operational procedure this is the
  policy behind; issue **#927** (the fanout mechanism whose *trigger* this
  constrains -- #927 decides how a release reaches downstream, this decides
  which releases do), **#926** (the locked changelog category set and
  per-`0.Y` files the PR-body extraction depends on), **#952** (the coverage
  figure rides in the release commit); ADR-00000008 (precedent for
  amending an ADR in place, beside the mechanism it governs -- its
  amendments, #710's included, all record mechanism, and the cadence
  clause #952 requires of it has not landed), ADR-00000002 (immutable
  version pinning -- there is no `latest` to drift onto, so a
  downstream's position is always a named tag),
  ADR-00000006 / ADR-00000011 (the `upgrade.sh` path contract the
  "nothing is skipped" argument rests on)

## Context

The release procedure is fully mechanised. *Deciding and cutting* a tag is
harness-side, outside this repo: the `semver-bump` skill, `/release`, and
the `release-bump.sh` / `release-tag.sh` primitives, with
`batch-base-upgrade.sh` on the fanout side. What a tag then *triggers* is
in this repo, and the two workflows that do it are not the same path --
conflating them is easy and this record did it once:

- A **base** tag push runs the `release` job in
  `.github/workflows/self-test.yaml`, whose `on:` block carries
  `tags: ['v*']`. That job still assembles its archive from a hardcoded
  `cp -r` operand list of its own; the declared payload #914 introduced
  never reached it.
- `.github/workflows/release-worker.yaml` is `on: workflow_call` only, so
  no base tag reaches it. It is what a **downstream** repo's release
  calls, through the `uses:` line `init.sh` writes into that repo's
  `main.yaml`, and it is the half that assembles the payload declared in
  `script/ci/release/archive.manifest` through
  `script/ci/release-archive.sh`.

(`script/release/justfile.release` is still a skeleton and says as much in
its header.) Both are purely mechanical: each acts on whatever tag reaches
it and states no cadence of its own. What none of them state is **when** a
release is cut and **who** decides -- the procedure answers "how", and the
cadence was carried in habit instead.

Two things made that gap start to cost something.

**The ACK rule had already been decided, and was being misread.**
`semver-bump`'s bump-classification table settles it. Quoting its three
bump rows -- the table opens with a `vX.Y.Z-rcN` row covering the RC tag
itself, which nothing here touches:

| Tag shape | Bump | Requires |
|---|---|---|
| `vX.Y.Z` where `Z>0` | Z (bug fix) | tag + push (no RC, no ACK) |
| `vX.Y.0` where `Y > prev_Y` | Y (feature / behaviour / break) | prior `vX.Y.0-rcN` with CI all `success`/`skipped` |
| `vX.0.0` where `X > prev_X` | X (ceremonial) | above PLUS `RELEASE_X_BUMP_ACK=<tag>` |

A Z tag needs no approval and never did. During the v0.42.x cycle this was
over-read as "every final tag needs approval", which is the X row's rule
applied to all three.

**The mechanism now has a blast radius.** #927 settled how a base release
reaches downstream: base's release fans an upgrade PR out directly, scope
**discovered by scanning** for a default branch carrying `.base/.version`
rather than read off an allowlist, and the PR is **opened and left open --
CI going green does not merge it**. Scanning the org today returns
**exactly 17 repos**: `ai_agent`, `claude_code`, `codex_cli`, `gemini_cli`,
`isaac`, `jetson_sdk_manager`, `omniverse_web_viewer`, `realsense_ros1`,
`realsense_ros2`, `ros1_bridge`, `ros2_distro`, `ros_distro`,
`sick_humble`, `sick_noetic`, `template`, `urg_node_humble`,
`urg_node_noetic`. Every one of them is a PR a human has to read.

So "when do we release" stopped being a matter of taste. Bound to the
wrong trigger it is 17 PRs; bound to the wrong approver it is either a
maintainer pressing a button on every bug fix, or an agent imposing a
breaking migration on 17 repos unattended.

## Decision

### 1. A Z release is cut by the agent without asking, one per bug

`vX.Y.Z` with `Z > 0` is tagged and pushed on the agent's own initiative.
This is not new policy -- it restores what the table above already said.

**One bug fixed = one Z release.** Not a batch. The property being bought
is that a downstream can name the release that carries the fix it needs;
a batch destroys exactly that, and cannot be recovered from the tag
afterwards.

### 2. An X or Y release is cut by a human, always

`vX.Y.0` and `vX.0.0` are the maintainer's to cut. No exception and no
standing authorization: an agent may prepare the RC, run the gate and say
the tree is ready, and then stops. X additionally keeps the
`RELEASE_X_BUMP_ACK` gate the script already enforces.

### 3. The judgement that matters is the classification, not the tagging

**An issue whose fix changes behaviour is not a Z, whatever it is filed
as.** It is a Y, and a Y returns to the human. `semver-bump` already says
"if you're unsure whether a change is Y or Z, lean Y"; this ADR makes that
binding rather than advisory, because with §1 in force the agent's
classification is the only gate left before a tag exists.

The v0.42.1 episode is why this clause is written down. That release was
**not** cut, because its content was not Z-shaped:

- `c6b53ea2` (closes **#914**) replaced the hardcoded `cp -r` operand list
  in `.github/workflows/release-worker.yaml` -- the reusable workflow a
  downstream repo's release calls -- with a declared payload,
  `script/ci/release/archive.manifest` plus a `release-archive.sh`
  assembler. The archive's payload contract changed shape for every
  consumer. (base's own `release` job was not part of that change and
  still carries its own list; see Context.)
- `3a36f8b4` (closes **#915**) put an EXIT trap over the whole post-pull
  window of `upgrade.sh`, so a failure after the subtree pull now undoes
  it. That is a rollback mechanism that did not previously exist.
- `7a36cf1a` (**PR #929**, refs #915) added `dockerfile_migrate.sh`
  migrations that `init.sh` applies to `${REPO_ROOT}/Dockerfile` -- base
  **rewrites a file the consumer tracks in git**.
- `d67b6aae` (closes **#882**) added `_report_verification_run` to
  `dist/script/docker/wrapper/build.sh`, wired as
  `_report_verification_run "${TARGET}" "${_VERIFY_LOG}" || exit 1`. A
  build that exited 0 before can now exit 1, in a wrapper every consumer
  vendors.

A consumer taking that content would meet a rewritten Dockerfile and a new
failure mode. None of it is a bug fix in the sense Z means.

Two details of that set are worth stating precisely, because the tempting
short version of this rule is wrong. **The label is not the signal:** the
four were labelled unevenly -- #915 carries `bug`, #914 and #882 carry
`triage`, and **#929 is not an issue at all**, it is the PR that landed the
Dockerfile migration as a follow-up to #915. What actually read as Z was
the uniform `fix(...)` commit type and the bug-report framing, not a label.
So the rule cannot be implemented as "check the label"; it is read off what
the change *does*.

**The reasoning is stated, not asked.** When cutting a Z the agent records
its classification and why in the release, so the call is reviewable after
the fact. That is a report, not a request for approval. The maintainer
retains a veto on the classification -- not a button on each release.

### 4. Fanout is triggered by X and Y only; a Z does not fan out

Under §1 a bug is a release, and this cycle produced six bug issues in two
days. Binding #927's fanout to every release would make one bug 17 PRs,
each of which a human must read because #927 forbids auto-merging them.

**So a Z is tagged and does not fan out.** A downstream that urgently needs
a particular Z tracks it itself.

This costs nothing in completeness, and the reason is not obvious enough to
leave unwritten: **`just base upgrade <tag>` is a subtree pull *to* that
tag, not a sequential application of the releases in between.** In
`dist/script/base/upgrade.sh`, `_upgrade`'s "Step 1/5" is a single

```bash
git subtree pull --prefix="${TEMPLATE_REL}" \
  "${TEMPLATE_REMOTE}" "${target_ver}" --squash \
  -m "chore: upgrade ${TEMPLATE_REL} subtree to ${target_ver}"
```

There is no loop over intermediate tags: the tree that lands is the tree at
`target_ver`. A downstream upgrading to the next Y therefore receives every
Z cut in between, in full, whether or not it ever saw them announced.
**Nothing is skipped; only the notification is batched.**

The gap this does create is real and is accepted deliberately: a downstream
currently hitting a bug that a Z has already fixed gets no signal until the
next Y. The tree still *generates* a path that would have covered exactly
that case -- `init.sh`'s `_sync_base_monitor_workflow` writes a per-repo
`base-version-monitor.yaml` that polls `releases/latest` weekly and opens
an upgrade-reminder issue when the pin is behind, which a Z would trip --
so the gap has to be stated against it, not around it. It is not a live
counter-argument on two counts #927 establishes: adoption is zero (404 for
that workflow on all seven repos checked, because a monitor delivered by
`init.sh` only reaches a repo that already ran an `init.sh` carrying it),
and #927 deletes it in favour of the fanout this section triggers. The
alternative -- a notification per Z across 17 repos -- converts
notification into noise, and noise is not read, which costs more than the
gap. A genuinely urgent fix is a case where the maintainer directs a
one-off fanout by hand. **The normal path is batched; the exception is
human.** Building a mechanism for the exception is the part being rejected.

### 5. What a Y fanout PR body must carry

Because a Y now spans every Z since the last fanout, its PR body is the
only place a downstream maintainer sees those Zs at all. It must carry:

- **BREAKING entries expanded, at the top, never collapsed** -- settled by
  #927's design comment, not decided here; it is restated because the
  release-span table below builds on it. The reader is scanning 17
  PRs and must be able to tell "routine bump" from "this one rewrites my
  Dockerfile" without opening each.
- **The fixes that affect the receiving repo**, in the body proper.
- **Base-internal changes in a collapsed `<details>`, explicitly labelled
  as not affecting this repo.** Omitting them is dishonest -- they ARE in
  the subtree being pulled -- and listing them flat is noise.
- **A table of the releases spanned**, each marked Z or Y and automatic or
  human, so this cadence rule is visible from the PR rather than
  remembered.
- **A statement that the PR is not auto-merged** (#927's rule): CI proves
  the upgrade builds; whether to take it is the receiving repo's call.

The extraction depends on **#926** (locked category set, per-`0.Y`
changelog files). Until #926 lands, pulling clean sections out of the
single changelog file is not reliable enough to generate this body from.

### Follow-ups this ADR does not perform

`semver-bump`'s SKILL.md and `/release` state the *procedure* and are
silent on cadence; they need to carry §1-§3 so an agent reading only the
skill reaches the same answer. Both live in the harness at the workspace
root, outside this repo, and are deliberately left untouched here. The
in-repo workflows named in Context need no follow-up: each runs off
whatever tag reaches it and carries no cadence text to keep in sync.

## Consequences

- **Release frequency rises substantially.** The per-run cost of the
  release procedure becomes load-bearing in a way it was not when releases
  were monthly; a slow or manual step in it now repeats per bug.
- `release-bump.sh` runs far more often, so everything it regenerates --
  the compare-link block, and per #952 the coverage figure -- is exercised
  continuously rather than once a cycle. That is a benefit: a stale
  generator now fails early instead of on release day.
- **The tag-triggered workflows run per Z**, so their CI cost is now
  per-bug rather than per-cycle.
- A downstream can name the exact release carrying the fix it needs, which
  is the whole point of not batching.
- **A mis-classified Z reaches downstream only at the next Y**, which
  leaves a window to catch it and re-classify before anyone receives it.
  That is a mild safety property, and it is a consequence of batching the
  fanout rather than a reason for it.
- The maintainer's remaining release work is the two decisions that carry
  judgement -- cutting X/Y, and vetoing a wrong Z classification -- rather
  than acknowledging tags.

## Alternatives

- **Batch several bug fixes into one Z.** Rejected: a downstream can then
  no longer name the release that carries its fix. The batch also tends to
  accumulate behaviour changes until it is really a Y, which is the
  failure §3 exists to prevent, arriving by a different road.
- **Fan out on every release, including Z.** Rejected on volume: 17 PRs per
  bug, each requiring a human read under #927's no-auto-merge rule. The
  reviewing cost is linear in bugs times repos and nothing about it
  amortises.
- **Open an issue rather than a PR in each repo per Z.** Rejected: the same
  volume problem one notch quieter. 17 issues per bug is still a stream
  nobody reads, and an unread notification is worse than a batched one
  because it looks like coverage.
- **Let the agent cut X and Y too, once CI is green.** Rejected: green CI
  proves the tree builds, not that imposing a behaviour change or a
  BREAKING migration on 17 repos is the right call today. That decision is
  the maintainer's, and it is not a property of the test suite.
- **Keep requiring approval for Z as well** -- the status quo during
  v0.42.x. Rejected: it makes the maintainer a button-presser on releases
  whose content is, by definition, only fixes, while the judgement that
  actually matters (is this really a Z?) is one the agent has to make
  either way. It buys ceremony at the point of least risk and nothing at
  the point of most.

## Amendment (ADR-00000031): a Z may be cut by a gate, and only a Z

- **Amendment status:** Accepted -- extends sections 1 and 3; reverses
  nothing. Section 2 (X and Y are the maintainer's) is untouched and is
  what the extension is bounded by.

Sections 1 and 3 were written with two actors in mind: an agent that cuts a
Z on its own initiative, and a maintainer who cuts X and Y. Section 3 makes
the agent's *classification* the last gate before a tag exists, and requires
it to record the reasoning so a wrong call is reviewable afterwards.

ADR-00000031 adds a third actor for one narrow case. A downstream repo that
bumps a pinned dependency can auto-release the result **when a gate proves
the bump ABI-safe**, with no agent and no person in the loop. Three things
keep that inside this record rather than around it:

- **The classification is still the gate before the tag** -- it is simply
  performed mechanically rather than by judgement, over a question narrow
  enough to have a mechanical answer (did the dependency's declared ABI
  component move). Everything the gate cannot decide is refused and returns
  to a person, who classifies it under section 3 as before.
- **A gate may cut a Z and nothing else.** A bump that moves a dependency's
  interface is very often a Y, and section 2 keeps every Y human. The gate
  has no path that produces one.
- **The reasoning is recorded the same way.** The gate prints the rule that
  approved the bump, and names the rule that refused it. Section 3's "the
  reasoning is stated, not asked" holds unchanged; the author of the
  sentence is a script.

Section 4 is untouched and does real work here: an auto-released Z does not
fan out, so this cannot turn one dependency bump into seventeen upgrade PRs.


## ---- FILE: doc/adr/00000028-documentation-is-derived-not-duplicated.md ----

# Documentation is derived from code, never duplicated beside it: test statistics live only in the release

> Serves: PRD invariant 10 (documentation is derived, not duplicated) --
> this is the decision that established it, and the first place it is
> applied. Also invariant 2 (never fail silently): a figure that is
> maintained by hand goes stale silently, and a catalogue 46% of whose
> descriptions are placeholders looks authoritative while saying nothing.

- **Date:** 2026-09-02
- **Status:** Accepted
- **Relates to:** **#922** (the catalogue Description column this
  supersedes -- the question "is the column required, optional or
  dropped" is answered here by removing the table it lives in); **#924**
  and PR **#943** (the hand-built release archive that PR deleted -- the
  reason recorded there is narrower than it reads, see sec. 4);
  **#952** (the coverage figure in the release -- the sibling case that
  fixes where the line falls, merged as PR #974, see sec. 3);
  ADR-00000018 (the ISTQB taxonomy whose level directories the report
  groups by); ADR-00000027 (release cadence -- this rides the release
  commit that cadence already produces); docker_harness **#287** (the
  mechanical merge conflict this removes the cause of).

## Context

`doc/test/TEST.md` and `doc/test/unit.md` carry two kinds of content, and
only one of them is written by a person. Every figure below was measured
against this repo on 2026-09-02 and names the command that reproduces it.

**Derived content.** A grand total (`Template self-tests: **3239 tests**
total (3090 unit + 149 integration).`), a per-spec count
(`### test/bats/unit/lib_spec.bats (54)`), and a table with one row per
`@test` listing that test's name. Every one of these is
`grep -c '^@test'` or a copy of a string already in a `.bats` file.

**Authored content.** One prose paragraph per spec file saying what that
file covers and why it is tested the way it is. No generator writes that
paragraph -- but it is not independent of the source either: in this repo
most of it restates the spec file's own header comment. The reason
`transcript_lnav_spec` checks the lnav format structurally with `grep` --
that the CI image ships no jq or lnav -- is stated in both
`test/bats/unit/transcript_lnav_spec.bats` and `doc/test/unit.md`. What
separates the two halves is therefore not novelty but derivability: a
generator can produce the counts and the table exactly, and can produce
neither paragraph. Whether the prose should in turn move into the spec
headers it echoes is a separate question, and is not decided here.

The derived half cost more than it returned, measured rather than
asserted:

**The grand total is five lines that every branch must edit.**
`TEST.md:3`, `TEST.md:7`, `TEST.md:23`, `TEST.md:29` and `unit.md:3`
(`grep -n '3239\|3090' doc/test/*.md`). Adding one test changes all
five, so two branches that each add a test collide there. Replaying
every merge of `origin/main` into a branch since 2026-08-25 with
`git merge-tree --write-tree --name-only`: of 65 such merges, 61
conflicted, and all 61 conflicted in `doc/test/` -- 50 of them there and
nowhere else. Over the same window 35 commits touched nothing outside
`doc/test/`, 23 of them carrying the identical subject
`docs(test): re-sync the suite counts after merging origin/main`.
docker_harness#287 -- an issue asking for the mechanical conflict to be
auto-resolved -- exists only because of these five lines.

**The per-test table duplicates the `.bats` files.** `unit.md` carries
1,981 table lines, of which 1,658 are per-test rows whose left column is
copied from the spec file. The right-hand Description column is
hand-written, and **761 of those 1,658 rows (46%) hold the placeholder
`-`** (`grep -c '| - |$' doc/test/unit.md`). Where it is filled it
usually restates the test name (`_lib.sh is idempotent when sourced
twice` -> `Double-source guard`). The table is also not an index of the
suite: 104 sections cover the unit specs, 74 with a
`| Test | Description |` table, 12 with a hand-made `| Category | Tests |`
grouping and 18 with prose alone, so 1,658 rows stand against 3,090 unit
`@test`s -- 54% of the suite has a row and the rest has none. Which
shape a section gets is a documented editorial choice (`unit.md`, "How
this catalogue is maintained"), so the unevenness is deliberate; what it
costs is that no reader can use the table to answer "what is tested".

**The counts describe the tree, and a person is asked to keep them true.**
`check_test_md_drift.sh` re-derives every figure on every run and fails
the gate when the committed docs disagree -- which is what forces every
branch to run `just test sync-docs` and produce the resync commit. The
checker is correct; it is the storage that is wrong.

## Decision

**Documentation is derived from the code, not duplicated beside it.**

A figure or a listing that can be computed from the tree is computed when
it is needed. It is not stored in a tracked file that a person, a hook, or
a gate must then keep in agreement with the tree. Prose that a machine
cannot derive -- intent, rationale, the reason a check is shaped the way
it is -- is authored, and it is the only thing a documentation file
should hold.

This is the living-documentation position: documentation is extracted
from the code and the tests rather than duplicated into a separate
document, so it cannot drift out of agreement with them.

The corollary that decides where the numbers go: **a derived figure that
describes the tree is stale from the moment the next commit lands.** Storing
it at a slower cadence than it changes does not fix that -- it only makes the
staleness harder to notice. So it is not stored at a slower cadence; it is
not stored at all.

What that turns on is the referent, not the storage. A figure that names the
thing it measured -- a coverage rate labelled with the version it was measured
on -- does not describe the moving tree and cannot go stale, so it may be
stored. Section 3 works this through on the case that forced it.

### 1. No test statistic is committed to the tree

The five grand-total lines and the 1,658 per-test rows leave
`doc/test/*.md`, together with the table scaffolding around them --
1,981 table lines in `unit.md` in total. The per-spec count in each
`### <path> (N)` heading goes with them: it is the same class of figure,
and keeping it would reintroduce the sync step this removes.

What remains in `doc/test/*.md` is the authored prose -- one section per
spec file, saying what it covers and why -- with no number in it.

**Amendment (#999, 2026-09-03): the per-test table is KEPT and GENERATED;
the removal of the five grand-total lines stands.**

The decision this section records is that a listing a machine can produce
must not be stored where a person has to keep it true. Deleting the table
was one way to satisfy that. Generating it from the code is another, and
it is the one taken: the per-test descriptions moved into the `.bats`
files as `# why:` marker blocks on the lines above each `@test`, and
`sync-doc-counts.sh` renders `doc/test/*.md` from them into an explicitly
fenced region that is replaced wholesale on every run. Nothing reads a
description back out of the catalogue.

What that changes about this record, precisely:

- The **five grand-total lines** and the per-spec `### <path> (N)` count
  are untouched by this amendment. They are still a figure about a moving
  tree with no referent, they still cost 61 conflicts in 65 merges, and
  §1's decision to remove them stands.
- The **per-test table** is not that. Its rows are no longer stored beside
  the code they describe -- they are derived from it, on every run, and a
  row deleted from the document is restored byte-for-byte by the next one.
  It costs nobody a sync step, so the reason to delete it is gone.

Why the reasoning under "Alternatives" flipped. The last alternative below
already named this end state and called it "a reasonable end state",
declining it on one ground: that the table adds nothing over the test
names it copies, evidenced by the 46% of rows nobody filled and the
near-synonyms among the rest. That evidence measured the wrong thing. Both
symptoms were caused by WHERE the description lived: a row in a
4000-line document, reachable only after running a generator, which a
rename silently emptied (the catalogue documented that loss as a rule).
With the sentence authored on the line above the test the author is
already writing, the cost of filling one falls to nothing and a rename
carries it. Deleting was cheaper than relocating only while relocating
meant hand-relocating; #999 relocated 1209 descriptions and 106 section
blurbs with a script, and proved by set comparison that none was lost or
invented.

The consequence recorded below -- "**#922 is answered by removal**" -- is
therefore answered by RELOCATION instead. The Description column is
required, at its new site, under a transition ceiling that is one number
in `script/test/drivers/catalog_description.sh` and no roster.


`check_test_md_drift.sh` and the count half of `sync-doc-counts.sh` are
removed with the figures they served. Nothing in a branch's normal work
touches `doc/test/` any more, so the file stops being a merge surface.
PRD invariant 2 lists the doc-count drift gate among the guards that
establish it; that one entry drops from invariant 2 when this mechanism
lands, and the invariant itself is untouched.

**Amendment (#978, 2026-09-04): the five lines are GONE. The per-spec
`### <path> (N)` count is KEPT, the drift gate is KEPT, and the paragraph
directly above is wrong on both.**

This is the mechanism half of section 1, and it landed against a record
that #999 had already moved underneath. What holds, item by item:

- **The five lines are removed**, as decided. `TEST.md`'s
  `**N tests** total (...)`, the "not in the N figure" prose, the
  "System (N) and smoke (N)" pair and the index table's `Count` column;
  `unit.md`'s `**N tests**` header. `_sync_test_md_index` -- the
  generator pass that maintained every one of them -- is deleted, and
  `test/bats/unit/doc_counts_spec.bats` fails if a shape is typed back
  into either document or if the generator starts writing one again.
- **The per-spec `### <path> (N)` count is KEPT**, so the sentence above
  grouping it with the grand total no longer holds. It was grouped there
  while both were maintained by hand. Since #999 it is rendered from the
  spec file on every run inside the fenced region, so it costs no sync
  step -- the same ground on which the amendment above keeps the per-test
  rows. It is also not an aggregate: it describes exactly the one file
  whose heading it is, and it is regenerated where it is read.
- **The per-level total at a catalogue's own head is KEPT** in
  `integration.md`, `system.md`, `acceptance.md` and `smoke.md`, by the
  same generator (`_sync_type_total`) and for the same reason. `unit.md`
  loses its one because it is the figure every branch that adds a unit
  test rewrites. That property -- who has to edit it -- is what made the
  five lines cost what they cost, not the presence of a number.
- **`check_test_md_drift.sh` and `sync-doc-counts.sh` STAY.** The
  paragraph above has them "removed with the figures they served"; they
  are not, because since #999 they serve the generated catalogue, which
  is what keeps a description from silently vanishing on a rename. Only
  `_sync_test_md_index` went. PRD invariant 2's guard list keeps its
  doc-count drift gate entry for the same reason: the gate did not go
  away, so nothing drops from the invariant.

**What this does NOT achieve, recorded because section 1 claims it.**
"Nothing in a branch's normal work touches `doc/test/` any more, so the
file stops being a merge surface" was false the moment #999 made the
per-test rows generated, and it stays false now. Replaying
`git merge-tree --write-tree --name-only origin/main <head>` over the 64
PRs opened since 2026-08-25, measured 2026-09-04 against `cb79382e`: 60
conflict, and 57 of those conflict in `doc/test/`. `TEST.md` conflicts in
57, and in 52 of them the conflict is confined to the lines this change
removes -- so `TEST.md` very nearly stops being a merge surface.
`unit.md` conflicts in 56, but in only 5 on its header: the other 51 are
in the generated per-test rows, which every branch that adds a test
writes. `doc/test/` therefore remains a merge surface by design, and
`script/test/resolve-doc-counts.sh` is the answer to it rather than a
transitional tool. The measurement the issue was filed on holds; the
inference drawn from it -- that removing the five lines ends the
conflicts -- does not.

### 2. Test statistics exist only in the release, and come from the run

A tag push already runs the full suite. `classify` returns
`code_changed=true` and `system_relevant=true` unconditionally for any
non-`pull_request` event, and the `release` job in `self-test.yaml`
needs `shellcheck`, `doc-counts`, `lint-static`, `hadolint`,
`bats-fragile`, `bats-integration`, `coverage`, `acceptance`, `system`
and `worker-selftest`, so all of them have finished before the Release
is created. Unit specs run inside the sharded `coverage` matrix and in
`bats-fragile`; there is no job named `unit` or `integration`. The
release gate is already what the industry calls a quality gate; what was
missing was collecting its result.

So the report is **the output of that run**, not a scan of the source:

- each test job emits JUnit XML (`bats --report-formatter junit -o <dir>`,
  which bats supports natively and which `script/test/drivers/bats.sh`
  already runs to collect per-spec timings) and uploads it as an artifact;
- the `release` job collects every artifact, merges them, and renders a
  per-suite summary into the Release body;
- the merged JUnit XML is attached to the Release as an asset, so the
  per-test detail is available to a machine without putting 1,981 lines
  in front of a human.

**Why the run and not the source.** Counting `@test` in the tree yields a
name and a number. The run yields pass / fail / skip, duration, the
failure message, and the suite structure -- and it cannot disagree with
reality, because it *is* reality. It also needs no maintenance: the test
framework produces it.

**Why JUnit XML and not CTRF.** CTRF describes itself as an open standard
for JSON test reports and publishes a schema, which JUnit XML -- a
de-facto format with no owning specification -- has never had. That is
the case for preferring CTRF eventually. It is not preferred now because
bats emits JUnit natively and this repo already consumes it, while CTRF
would need a conversion layer and nothing here aggregates across tools
yet. JUnit XML now; CTRF when a second producer appears.

### 3. There is no information gap, because there is nothing to be stale

The alternative considered and rejected was to keep the total in
`TEST.md` and let only the release commit write it. That removes the
conflict but creates a worse property: `main` would show the previous
release's figure while carrying a different one, and a reader has no way
to see which. A number that is *sometimes* right is harder to use than no
number, because it must be distrusted every time.

Removing it entirely means the only place a test statistic appears is the
place where it was measured, attached to the artifact it describes.

The coverage badge is the case that shows where the line falls, and it landed
while this record was being written. #952 merged as PR #974 on 2026-09-02 and
commits `doc/badge/coverage.svg`: a figure derived from a coverage run,
written into a tracked file and refreshed at release cadence. Read against the
paragraph above it looks like the arrangement this section rejects. It is not,
and the reason is the discriminator this record needs:

**A derived figure may be stored when it names what it measured.**

`doc/badge/coverage.svg` renders `coverage v0.42.0: not measured` -- the
version is inside the artefact, and `coverage_badge_spec` asserts it matches
the current `.version`. So the badge is not a claim about the working tree
that goes stale; it is a claim about v0.42.0, and it stays true forever. The
objection above -- "a reader has no way to see which" -- has no purchase,
because the artefact answers it. The five grand-total lines had no referent:
`3239 tests` asserted something about *the tree*, which is why it was wrong
between every commit and its resync, and why every branch had to edit it.

The two costs separate the same way. The counts had a merge surface of 61
conflicts in 65 merges and a gate that forced every branch to run a
regenerator. The badge is written by one commit per release and by nothing
else, so it has no merge surface at all.

What does not survive review is the badge's *cadence enforcement*, and it is
recorded here because it is invariant 2's failure mode rather than this
record's. `script/release/justfile.release` states that the write is a
hand-run step today -- the bump that should call it lives in the harness repo,
tracked as docker_harness#289 -- and that forgetting it "is caught by
coverage_badge_spec ... but only after the tag, as a red main". A guard that
fires after the artefact it guards has shipped is a late failure, not a
prevented one. Storing the figure is fine; requiring a person to remember to
write it is not.

### 4. What PR #943 actually decided

PR #943 (closing #924) deleted the `release` job's whole "Create release
archive" step -- the `mkdir` / `cp -r` / `tar` / `zip` -- and with it the
`files:` input that attached the result. Read as a blanket rule against
release assets it would forbid this decision's XML asset, so the
distinction is recorded here.

What #943 removed was a **hand-built source archive that GitHub already
produces** -- a strictly worse subset of the tarball GitHub attaches to
every release, assembled from a hardcoded nine-operand `cp -r` list that
had silently omitted seven of the sixteen tracked top-level entries,
`.version`, `CONTEXT.md` and the repo-root `init.sh` among them
(measured at `db264975`, the last commit before #943 landed), because
`cp` says nothing about a path nobody listed. The related failure where a
multi-operand `cp -r` under `bash -e` lost a release outright, twice,
belongs to the downstream archive #914 replaced with a declared manifest
-- a different artifact, which #943 explicitly left alone. #943's
objection is to duplicating an artifact the platform already provides.

A JUnit XML report is not something GitHub produces. It is evidence of
the run, it exists nowhere else, and attaching it therefore duplicates
nothing. One consequence has to be stated rather than discovered: #943
also wrote into `README.md` that a base release carries GitHub's source
archives "and no other asset". That sentence is amended when this
decision's mechanism lands, so that the two records reconcile instead of
contradicting each other.

## Consequences

**A branch stops touching `doc/test/` unless it changed the prose.** The
61-conflicts-in-65-merges rate and the 35 commits per cycle whose entire
content is `doc/test/` both go away. docker_harness#287 can be closed as
no-longer-reachable rather than implemented.

**#922 is answered by removal.** The question was whether the Description
column is required, optional or dropped. The table it belongs to is
deleted, so the column has no owner to under-serve: 46% placeholders
become zero rows.

**The per-test listing improves rather than disappears.** It stops being
a 1,658-row hand-synced table that covers 54% of the suite and records
what the tests are *called*, and becomes a machine-readable record of
what every test *did*, per release, permanently attached to the tag it
describes.

**A reader of `main` cannot see a test count.** This is deliberate. The
count of a moving branch has no stable meaning, and the previous design
answered the question with a figure that was wrong between every commit
and its resync. Someone who needs the number for the working tree runs
`just test`; someone who needs it for a version reads that version's
release.

**The prose becomes load-bearing.** With no table beneath it, the
paragraph per spec file is the whole of `doc/test/`. It must say why the
file exists and why it tests the way it does -- which is what it already
does well, and is the half no generator can write.

## Alternatives

**Keep the total, update it only at release.** Rejected in sec. 3: it
trades a merge conflict for a figure that is silently wrong most of the
time.

**Auto-resolve the conflict with a git merge driver.** A `.gitattributes`
driver could regenerate the count during a merge. It removes the conflict
but not the cause, needs a `git config` line in every clone (a driver
cannot be committed), and silently degrades to a conflict in a fresh clone
that has not run it. It also leaves the figure still needing to be right
in every commit.

**Move the counts to an orphan branch.** An append-only metrics branch
never conflicts with `main`. Rejected because it is unnecessary here: the
tests are already in git at every commit, so any historical figure is
derivable with `git grep -c '^@test' <rev>` without storing anything, and
each release's report is attached to its own tag. A second store would be
a second thing to keep true.

**Move the per-test descriptions into the `.bats` files and generate the
table.** This satisfies the principle and is a reasonable end state. It is
not taken now because the table adds nothing over the test names it
copies -- the evidence is the 46% that nobody filled and the near-synonyms
among those that were. Deleting is cheaper than relocating, and if a
per-test description turns out to be wanted later it belongs beside the
test, not in a document.

> **Amendment (#999, 2026-09-03):** this alternative was TAKEN. See the
> amendment in sec. 1 for why the evidence above measured the storage
> site rather than the table, and what the relocation cost in practice.


## ---- FILE: doc/adr/00000029-early-return-is-the-default-function-shape.md ----

# Early return is the default shape of every function, not a remedy applied when a threshold is breached

> Serves: PRD design principle P1 (early return is the default shape of
> every function) -- this is the decision that established it. It serves
> no invariant directly: it is the source shape ADR-00000014's
> decomposition already assumes, and so it stands behind invariant 7's
> testability rather than beside it.

- **Date:** 2026-09-03
- **Status:** Accepted
- **Relates to:** **#994** (the epic this is decision 1 of; the
  implementation thresholds, the design-principle layer and the ADR
  structure lint land under it); ADR-00000014 (the decomposition into
  subsystem libs whose seams this is the function-level shape of);
  ADR-00000015 (test files mirror source -- the reason a split is decided
  by design and never by test convenience); PRD invariant 7 (the test bar
  a splittable function is what makes reachable).

## Context

base's shipped code is 809 functions. Measured across them:

| threshold | value | today |
|---|---|---|
| nesting depth | <= 3 | 44 at >= 4, 7 at 5, 1 at 6 |
| function length | <= 50 lines | 151 over (18%), worst 515 |
| positional parameters | <= 5 | 7 over, worst 31 |

The numbers are not the subject of this ADR. What they are evidence of
is: those functions were not written with a guard clause at the top and
then grew past a limit -- they were written body-first, with the
validation folded into the branch structure, and depth 4 is simply what
that produces. No threshold was breached; a shape was never chosen.

An earlier audit of the nesting figure treated it the other way round: as
a list of 44 violations, to be ranked by severity and fixed. That framing
is what this ADR corrects. It yields 44 fixes and then, some months
later, 44 more, because nothing in it reaches the next function anybody
writes. The 44 are a symptom that was measured; the thing to change is
the default shape, and the measurement's job is to tell us when the
default was not applied.

The objection this had to survive is real and was argued on its merits:
splitting `compose_emit.sh::generate_compose_yaml` -- 31 positional
parameters -- or a 515-line function is a risky change to make against
code that currently works, and the risk is borne by every downstream that
vendors it. The answer, from the repo owner:

> A function that is hard to split correctly is already defective; the
> difficulty is the finding, not an exemption from it.

That is the load-bearing sentence, and it is not rhetorical. A function
that cannot be split correctly is one whose pieces are not separable --
its branches share mutable state, its parameters are positional because
no group of them has a name, and no part of it can be exercised without
the whole. Every one of those is the same property stated differently,
and every one of them is what makes the function untestable, unreviewable
and unsafe to change for any other reason too. The difficulty of the
split is a measurement of that property. Declining the split on the
grounds that it is difficult keeps precisely the code the difficulty was
telling us about, and leaves it where the next person to need a change
there will find it, with no record that anyone looked.

## Decision

**Early return is the default shape of every function in base. A guard
clause at the top -- validate the precondition, reject, return -- is how
a function is written here. It is not a remedy applied to a function that
has crossed a threshold.**

Three consequences of stating it that way rather than as a limit:

1. **The thresholds are a net, not a target.** Depth <= 3, length <= 50,
   parameters <= 5. A function at depth 3 is not thereby correct and a
   function at depth 1 is not thereby exemplary; the numbers exist to
   report where the default shape was not applied, and they are set where
   an unguarded function reliably lands. Aiming at a threshold produces
   code shaped to pass it, which is the failure mode the earlier audit
   framing had built in.

2. **Difficulty is a finding, and it is recorded as one.** Where a
   function resists a correct split, the resistance is the result: the
   change that follows is a design change to the code that resists, and
   the reason it resisted is written down. "This one is too risky to
   split" is not an outcome this ADR admits; "this one shares mutable
   state across four branches, so the split is the extraction of that
   state" is.

3. **The gate lands on a clean tree.** The thresholds are wired into
   `just test` and CI only once the tree passes them (#994 phase 4). A
   gate that lands red is a gate that is muted on the day it lands, and a
   muted gate is a gate that has been removed with the maintenance cost
   left in.

   **Amendment (#994, 2026-09-03): a clean tree is what the gate needed
   to land GREEN, and an adoption ceiling supplies that without one.**
   The reason above is intact and it is the reason: a gate must not be
   red on the day it lands. What phase 3 found is that "the tree is
   clean" was one way to get there and not the property being asked for.
   Each lint now judges by a per-metric CEILING -- the count of functions
   still past the threshold, one readonly integer in
   `script/test/drivers/shell_metrics.sh`, which may only ever go down --
   so a RUN of the lint is green on arrival, fails the moment a change
   adds a violation, and tightens as each slice lands. The thresholds
   themselves do not move; that is the distinction the next section
   turns on.

   **This amendment records a precondition falling away, not
   enforcement arriving.** The three lints are still absent from
   `script/test/test.sh`'s `_LINT_TOOLS`, from `just test` and from
   every workflow under `.github/`, so a new function written at depth 5
   still lands green in the gate exactly as it did before phase 3. What
   the original wording got wrong was the ORDERING: it made the whole
   108-function flattening a prerequisite of any enforcement at all, and
   that flattening is measured in months of slices. That prerequisite is
   gone -- a lint with a ceiling can be wired into a gate on the tree as
   it stands. The blocker that remains is structural and belongs to
   phase 4: `_LINT_TOOLS` runs INSIDE the ci container while this lint's
   population comes from the git index, and a `git worktree` checkout's
   `.git` is a file naming a path outside the bind mount, so joining the
   lint phase means giving it a host-direct leg rather than adding three
   strings to a table. Until that lands the entry points are
   `just test metrics` and `test.sh --<metric>-only`, run by hand.

## Consequences

- The three metric lints (nesting, length, parameters) are written before
  the tree is clean and are deliberately **not** gating on arrival
  (#994 phase 2). They report, and their own specs prove each can fail by
  mutation, so what they measure is trustworthy before anything depends
  on it.
- The flattening happens in reviewable slices ordered by leverage rather
  than by file (#994 phase 3): the 7 parameter violations first, since
  they are the smallest and most localised, then depth, then length. Each
  slice is a PR with its own review, per ADR-00000014 rule 3 -- behaviour
  identical, the existing specs standing as the regression net.
- A split that changes behaviour is a bug in the split, not an accepted
  cost. This is the same rule ADR-00000014's relocate-first slices ran
  under, and it is what makes the slices reviewable at all.
- Cyclomatic complexity stays out of scope. No shell tool measures it and
  writing one is more work than it adds while depth and length are
  unbounded; it is revisited once the flattening lands.
- Some functions will get more, smaller functions with names, and the
  file-level line count will rise in places. That is accepted, and the
  unit is the point: every threshold here is per-function, because file
  size points at the wrong target. base's largest shipped file
  (`setup_tui.sh`, 2862 lines) averages 53 lines across 54 named
  functions; `wrapper/run.sh`, a quarter its size, averages 73 across 9.
  The bigger file is the better-shaped one, and a per-file limit would
  have ranked them the other way round. Nothing here is a limit on a
  file.

## Alternatives

**A baseline file listing today's violations, gating only new code.**
Rejected, and it is the alternative that most needed rejecting because it
is the standard answer. A baseline is a hand-kept roster: it has to be
regenerated when a file moves, it drifts against the tree silently (PRD
design principle P2 -- derive the population, never enumerate it), and
nothing in it distinguishes "this was fixed" from "this line no longer
matches". Worse than the maintenance is what it does to the gate's
meaning: a gate with a baseline no longer says "base holds this
standard", it says "base holds this standard except in the 202 places
recorded here", and that file is a permanent, tracked, growing record of
what we decided not to do. It converts a quality bar into an inventory of
debt with an accountant attached. The tree is made clean instead, and the
gate lands on a clean tree.

> **Amendment (#994, 2026-09-03): the single-integer CEILING phase 3
> adopted is not this alternative, and here is the test that separates
> them.** Every reason above is a property of a per-SITE roster, and
> each fails to attach to one number. It has to be regenerated when a
> file moves -- a count does not know what a file is. It drifts silently
> against the tree -- a count is recomputed from the tree on every run.
> Nothing in it distinguishes "fixed" from "no longer matches" -- a
> count has no entries to be stale about. It says "the standard holds
> except in these 108 places" -- a count names no place, so it can
> excuse no particular function; what it says is "the standard holds,
> and 108 functions have not been brought to it yet", which is a true
> statement about a migration rather than a permanent exemption. P2 is
> the sharpest of these and it comes out the same way: the population is
> still derived from the git index every run, and the only hand-kept
> figure is how far the migration has got.
>
> The concession, stated because an amendment that only argues its own
> side is worth nothing: a ceiling has SLACK. Flatten one function
> without lowering the number and a new violation can land green in the
> room that opens. A per-site baseline would have caught that. What
> bounds it is that the slack is printed on every run, clean or not, and
> that lowering the number is a one-line change any reviewer can ask
> for; what makes it acceptable is that the alternative on offer was not
> a per-site baseline but no enforcement for the length of the
> migration.
>
> The instrument is not new here. `drivers/catalog_description.sh` (#999)
> carries the same one-number transition ceiling for the same reason,
> with the same argument and the same disclosed cost -- so this is base
> applying a mechanism it had already settled, not inventing an
> exception for its own metrics.

**Gate new and changed code only, with no baseline file** -- compute the
violation set against the merge base and fail only on additions. Rejected
for the same reason with a different mechanism: the exemption is now
implicit rather than tracked, which is worse, not better. It also makes
the gate's result depend on which commit you are branched from, so the
same file passes on one branch and fails on another, and it rewards
touching a bad function as little as possible -- exactly backwards from
what a function that resists change needs.

**Raise the thresholds to where the tree already sits** (depth 6, length
515, parameters 31). This is the honest version of doing nothing, and
saying it plainly is what disqualifies it: thresholds set to the current
worst case cannot report anything, because nothing can exceed them
without first becoming the new worst case.

**Keep the thresholds as advisory, reported but never failing.** Rejected
by base's own experience with the coverage figure: a non-gating metric
(#377 made coverage exactly that) was ignored for as long as it was
non-gating, and it took ADR-00000008 promoting it to an enforced PR gate
before anything moved. An advisory threshold is a threshold whose only
consumer is somebody who was already going to comply.

**Treat this as a style guide entry rather than an ADR.** Rejected
because the thing being decided is not a formatting preference that a
reader can take or leave -- it is the answer to "what do we do about a
function that is hard to split", and that answer had a defensible
alternative that was argued and lost. A decision with a rejected
alternative is an ADR by definition; a style guide entry would record the
conclusion and lose the argument, which is the half a future reader needs.


## ---- FILE: doc/adr/00000030-config-component-layout-and-preset-selector.md ----

# The `config/<component>/` layout, and the selector that says which preset a build bakes

> Serves: PRD invariant 8 (development and field are cleanly separated, and
> provisioned by opposite means) -- the half ADR-00000023 left open, namely
> WHICH config a build bakes; also invariant 4 (the committed preset is the
> inert one), invariant 2 (a selector that resolves to nothing is reported,
> not discovered inside `docker build`), and invariant 10 / ADR-00000028
> (one record per fact, which is why audience is not a directory).

- **Date:** 2026-09-03
- **Status:** Accepted
- **Relates to:** issues #826 (the runtime/deploy config convention, ask 1)
  and #827 (the `config/<component>/` directory architecture, all five
  asks); ADR-00000023 (the field-override + field-deploy contract this
  completes -- its sec. 4 forward-references these two issues as what makes
  the rule downstream-explicit); ADR-00000003 (env vs workload parameter
  boundary); ADR-00000001 (`.setup.conf` is the main path, compose-native
  mechanisms the escape hatch -- why the selector is NOT a conf key);
  ADR-00000028 (documentation is derived, not duplicated -- why an audience
  directory is refused); issue #1000, which made `config/*/` the unit both
  halves of invariant 8 provision and is what this builds on.

## Context

ADR-00000023 settled how a field operator retunes a **baked** config file
without a rebuild: a `COPY`-baked default plus an optional mount that wins,
declared per stage in `config/<component>/deploy.manifest`. It assumed an
answer to two questions it never wrote down, and #826 and #827 are exactly
those two:

- **Which config gets baked in the first place.** A repo that ships eight
  camera profiles bakes one of them. `deploy.manifest` names paths *inside
  the image*; it cannot name the profile that became that path, and it runs
  at deploy, long after the build chose.
- **What the inside of `config/<component>/` looks like.** #1000 made that
  directory the unit both halves of invariant 8 provision. It said nothing
  about its contents.

An earlier audit recorded that ADR-00000023 already closes both. Re-checked
against the file: it answers **one** of #826's three asks -- ask 2, the
no-rebuild override -- and **none** of #827's five. Its only mention of
either issue is the forward pointer in sec. 4 and in its Consequences,
which says these issues are what make the deployable-stage rule
downstream-explicit. That is an ADR naming an open question, not answering
it. Nothing under `doc/adr/`, `doc/PRD.md` or `CONTEXT.md` used the words
"preset", "type-first" or "upstream-baseline" before this record.

**What the org actually has**, surveyed 2026-09-03 over the 23 non-archived
repos under `ycpss91255-docker` with `gh api repos/<r>/contents/config` and
the git trees behind it -- because a convention no repo can adopt without a
migration has to say what the migration is, and the last convention written
without that survey (`deploy.manifest`) has 0 of 23 adoption:

- **Six component directories exist, across five repos**, and their shapes
  do not agree. `realsense_ros1/config/realsense/` and
  `realsense_ros2/config/realsense/` group their files into subdirectories
  (`yaml/`, `launch/`, `filters/`, `udev/`, `json/`); the other four --
  `ros1_bridge/config/ros1_bridge/` (five yaml files),
  `jetson_sdk_manager/config/jetson/` (eight), the same repo's
  `config/packages/` (two) and `isaac/config/ros2/` (one) -- are flat.
- **The audience split #827 was filed against is already gone.** Neither
  realsense repo still carries `custom/ official/ internal/ example/`, and
  `realsense_ros2` has moved its diff-only upstream baseline to
  `.github/upstream-baseline/`. realsense is the reference implementation
  now, not the counterexample.
- **Preset selection has already converged on one shape, in three repos.**
  `realsense_ros1` (`camera.yaml`, `filters.yaml`), `realsense_ros2`
  (`camera.yaml`) and `jetson_sdk_manager` (`jetson.yaml`) each commit a
  repo-root symlink -- mode `120000`, whose whole content is a path --
  pointing into `config/<component>/`. The two realsense repos read it
  through a build ARG whose default is the symlink's own name
  (`ARG CAMERA_CONFIG="camera.yaml"`, then `COPY "${CAMERA_CONFIG}"`), and
  both point at an empty `none.yaml`.
- **The one repo that picks a preset WITHOUT a symlink shows what the
  symlink buys.** `ros1_bridge` has `ARG BRIDGE_FILE="bridge.yaml"` and no
  `bridge.yaml` in the tree, so the default names nothing; its Dockerfile
  carries a three-branch `if / elif / else` around the install, twice, once
  per stage, to survive that.
- **Two spellings of "copy me" are live**, and they are not equivalent:
  `.example.` with the real extension last (`rs_camera_remap.example.launch`,
  `sensor_options.example.yaml`) and `.example` appended after it
  (`host.yaml.example`, in `isaac` and `omniverse_web_viewer`). Both of the
  latter also sit directly under `config/`, which is the population #1000
  already WARNs about as provisioned by neither half.

## Decision

### 1. A preset lives in its component directory; a repo-root symlink says which one is baked

Curated presets are ordinary files inside `config/<component>/`. They need
no home of their own: that directory is already bind-mounted at
`/opt/app/config/<component>` in development and `COPY`-baked at the same
path for deploy, so a preset library is provisioned by the channel that
exists.

Which preset **this repo** bakes is declared by a **committed repo-root
symlink into `config/<component>/`**, and the build reads it through a
build `ARG` whose default is that symlink's name. Three properties follow,
and together they are the reason this beats the alternatives below:

- The repo's default is one file whose entire content is the chosen path,
  so changing it is a one-line diff that a reviewer reads without opening
  anything else.
- A single build overrides it with `--build-arg` and touches no tracked
  file -- the same "no committed change" property ADR-00000023 sec. 2 gives
  the deploy side, applied one moment earlier.
- The ARG default names a file that **exists**, so the `COPY` is
  unconditional. That is the whole of what `ros1_bridge`'s duplicated
  three-branch fallback is working around.

The selector is a repo-root file and not a `.setup.conf` key on purpose.
It must be resolvable by `COPY` **inside the build context**, and base
cannot render a conf key into a build arg generically because it does not
know the repo's ARG name -- knowing it would make base the owner of a
downstream's config schema, which ADR-00000023 sec. 5 refuses. It is also
the one form of this choice that is visible from `ls -l`.

base derives the selectors rather than being told: a root entry that is a
symlink AND whose link text names a path under `config/`. That excludes
base's own root symlinks (`justfile`, `.hadolint.yaml`, which point into
`.base/`) with no filename rule and no list to fall off (PRD design
principle P2). Every `setup` run names each selector and the preset it
currently resolves to, and WARNs by name about one that resolves to
nothing.

### 2. The committed target is the inert preset

The preset a fresh clone builds is the one that changes nothing -- an empty
`none.yaml`, upstream's own defaults. Choosing a profile is then an act
someone performed and recorded, never something a clone inherited by
accident. This is invariant 4 applied to the config row, and both realsense
repos already do it.

### 3. Group by kind only once a kind has a second file

Inside `config/<component>/`, files stay flat until a kind has more than
one member; the second `*.launch` is what creates `launch/`. Not
"type-first always".

The measurement decided this. The rule as written describes **6 of 6**
component directories in the org today and costs zero migration; a
mandatory type level would move **4 of the 6**, one of them a directory
holding a single file. #827's own argument against the audience split --
that a level does not earn its keep when a category has one or two files --
is a general argument, and applying it to the type level too is the only
consistent reading of it.

### 4. A copy-me template is a filename, not a directory

`<name>.example.<ext>`, sitting at the top of the component directory where
it is seen. The real extension stays **last**, so tooling that selects by
extension still finds it. The live case: `realsense_ros1` copies
`config/realsense/filters/` into its test stage at `/lint/filters/` and its
smoke suite iterates `"${SHIPPED_FILTERS_DIR}"/*.yaml`, parsing each shipped
profile -- which reaches `sensor_options.example.yaml` and would not reach
the same file spelled `sensor_options.yaml.example`. `example/` as a
directory is refused for the reason in sec. 6.

### 5. A file kept only to be diffed against upstream is not config

The discriminator is one question: **does the container read it at run
time?** If yes it is config, whoever wrote it -- vendored upstream data a
node loads stays in `config/<component>/`. If it exists only to be compared
against a pinned upstream tag, it is a test fixture; it belongs with the
tests (`realsense_ros2` uses `.github/upstream-baseline/`), and leaving it
under `config/` gets it bind-mounted and baked into every field image for
nothing, while suggesting to a user that it is a file they may edit.

### 6. Audience is not a directory

No `official/ custom/ internal/ example/` level. Which files a field
operator may retune is already recorded, per deployable stage, in
`config/<component>/deploy.manifest` (ADR-00000023 sec. 5); everything
unlisted is baked-only. A directory that says it too is a second record of
one fact, and the two can only disagree -- which is invariant 10, and the
same argument ADR-00000028 makes about test statistics.

## Alternatives

- **Select the preset with a `.setup.conf` key.** Rejected: the value has
  to reach `COPY` inside the build context, and base would have to know the
  downstream's ARG name to render it there. ADR-00000001 makes `.setup.conf`
  the main path for what base itself resolves; the preset is a downstream's
  own build input, and ADR-00000023 sec. 5 already draws that line ("base
  delivers files; the repo consumes them").
- **A build ARG naming the preset path directly, with no symlink.**
  Rejected on the measurement: it is `ros1_bridge`'s shape, its default
  names a file that is not in the repo, and the cost is a three-branch
  fallback duplicated across two stages plus a repo default that is invisible
  until you read the Dockerfile.
- **Bake every preset and choose one at run time.** Rejected: it moves a
  build-time choice into the runtime image for the sake of choice a field
  operator already has -- ADR-00000023's mount-wins override is exactly that
  channel, and it does not require carrying seven unused profiles into a
  field artifact.
- **Mandatory type-first grouping, as #827 proposed it.** Rejected: it
  migrates 4 of the 6 component directories that exist, including one
  holding a single file, and buys nothing the "second file creates the
  directory" rule does not already buy on the two directories that are
  genuinely mixed.
- **Keep the audience sub-split for repos that want it.** Rejected: an
  optional second record of the tunability fact is still a second record,
  and "optional" means the drift appears only in the repos that opted in.
- **A top-level `preset/` tree, outside `config/`.** Rejected: it would be
  provisioned by neither half of invariant 8's channel, which is precisely
  the shape #1000 taught us to WARN about.

## Consequences

- **base states the choice it used to hide.** Every `setup` run -- both the
  dev-bind half and the deploy-bake half, from one call site -- names each
  selector and the preset it resolves to, and WARNs about one that resolves
  to nothing. That failure used to surface as a `docker build` dying on a
  `COPY` whose message names neither the symlink nor the missing file, after
  the layers above it had rebuilt.
- **A new repo is told the convention.** The `config/.gitkeep` base seeds
  now states both channels that directory feeds and the rules above. It
  reaches **new repos only**: `_populate_config` preserves an existing
  `config/`, deliberately, because that directory is the user's.
- **The migration is small and it is not zero.** Sections 1, 2, 3 and 6 cost
  nothing: no component directory in the org contradicts them today. Section
  4 renames two files (`isaac` and `omniverse_web_viewer`'s
  `host.yaml.example`), both of which also have to move under a component
  directory to be provisioned at all. Section 5 is already done in
  `realsense_ros2` and untested elsewhere. `ros1_bridge` adopting section 1
  is a symlink plus deleting a fallback branch in two stages.
- **Three repos keep app config where neither half reaches it.** `seggpt`,
  `urg_node_humble` and the two `host.yaml.example` repos hold regular files
  directly under `config/`. They are WARNed by name at every run and are the
  fanout's real work; this record does not move them.
- **`config/docker/` survives in 15 of the 23 repos**, holding the
  `setup.conf` that #831 relocated to the repo root. Under the derived
  population it is a component directory like any other, so it is
  bind-mounted and baked -- inert, but it means a stale copy of a
  tool-managed file travels into images. Naming it here; retiring it is its
  own change.
- **The convention is written but not enforced downstream.** base can check
  what base can see -- the selectors in the tree it is run against. Nothing
  gates a downstream's directory shape, and a lint that could would have to
  live in the repos being linted. Adoption is 0 of 23 until a release
  carries this and the fanout runs.


## ---- FILE: doc/adr/00000031-abi-gated-dependency-bump-auto-release.md ----

# A dependency bump auto-releases only when a gate can prove it ABI-safe, and a gate never cuts anything but a Z

> Serves: PRD invariant 6 (base is a subtree; downstream is a thin caller)
> -- one convention in base rather than seventeen repo-local definitions of
> "safe to release"; also invariant 4 (fail-safe defaults -- "cannot
> determine" resolves to not releasing) and invariant 2 (never fail
> silently -- the gate states which rule refused, by name).

- **Date:** 2026-09-03
- **Status:** Accepted
- **Relates to:** ADR-00000027 (release cadence -- **amended in place** by
  this record, which adds a non-human, non-agent actor to its section 1 and
  a mechanical classifier to its section 3), ADR-00000002 (immutable
  version pinning -- why a resolved version has to be a `vX.Y.Z` tag and
  not a moving name), issue **#829** (the downstream ask this answers, and
  its decided mechanism), issue **#1012** (the defect class this design is
  written against: a version decision read off a ref that carries none, and
  an unrecognised input resolving to the most-consumed name)

## Context

A downstream repo that pins an upstream dependency -- `realsense_ros2`
pinning librealsense and realsense-ros is the case that raised this --
wants the bump flow hands-off: notice a new upstream tag, move the pin,
write the changelog entry, merge on green, release. Every step of that is
mechanical except the last, and the last one is where the judgement lives:
**releasing a bump says the thing downstream consumers can rebuild against
did not change.**

Three facts shaped what could be built.

**A bot cannot re-enter the tag path.** An event created with the default
`GITHUB_TOKEN` starts no new workflow run. A repo that pushes `vX.Y.Z` from
a workflow therefore gets no run from it, and
`.github/workflows/release-worker.yaml` is `on: workflow_call` only -- it is
reached by a downstream repo's `call-release` job, which today is gated on
`startsWith(github.ref, 'refs/tags/')`. So an auto-release either carries a
PAT to make the push look human, or it calls the worker directly from the
post-merge run. #829 settled on the direct call; the worker's version then
has to come from an input, because on that path `github.ref_name` is a
branch.

**A version decision read off the wrong source is this repo's live defect
class.** #1012: `release-test-tools.yaml` writes `:latest` from a `tags:
'v*'` trigger, so `v0.42.0-rc4` moved the tag every unpinned consumer
builds from -- four times. Its unrecognised-input branch resolves to the
same `:latest`. Both are the same mistake in different clothes: a decision
about a version taken from something that does not carry one, and an input
the code could not read resolving to the most permissive answer. An
auto-release gate written the same way would industrialise it.

**Nobody can define "ABI-safe" once for every dependency.** librealsense's
SONAME carries its minor; plenty of libraries carry only their major; a 0.x
version promises nothing at either level. A gate with a built-in answer is
a base-wide guess that silently releases somebody's break.

## Decision

### 1. The gate decides one thing, and refuses everything it cannot decide

`script/ci/abi-gate.sh` answers exactly one question -- is this
`old -> new` pin change ABI-safe by the convention this dependency itself
follows. It refuses, by name and with the reason on stderr:

- a version it cannot read on either side, including a suffixed one
- an ABI axis that is undeclared, or declared as something it does not
  recognise
- a 0.x pin declared with a major-only axis (the fix is in the message:
  declare `major.minor`; it is not silently re-read as that, because a
  declaration nobody corrects goes on meaning something other than what it
  says)
- a downgrade, and an unchanged pin
- a pair the upstream's own compatibility declaration does not sanction

A refusal prints **nothing on stdout**, so a caller appending stdout to
`GITHUB_OUTPUT` is left with no `decision` key: the
`outputs.decision == 'release'` wiring and the bare exit status both read a
refusal as "do not release". There is no arrangement of the caller in which
an unanswerable bump releases itself.

### 2. The ABI axis is declared per dependency, and has no default

`ABI_AXIS=major` or `ABI_AXIS=major.minor`, supplied by the repo doing the
bumping. Which component is a dependency's ABI is a fact about that
dependency, so base does not hold an opinion about it; a repo that declares
nothing gets no auto-release, which is the correct default rather than a
gap.

### 3. Follow the upstream's declared compatibility

Where a wrapper declares the dependency version it was built against, the
new pin must agree with that declaration on the ABI axis (`UPSTREAM_COMPAT`).
Two dependencies each bumped to their own newest is a combination the
upstream never shipped, and each half being ABI-clean on its own does not
make the pair tested.

### 4. A gate may cut a Z. It may never cut a Y or an X

An ABI-safe dependency bump is a patch release. Anything the gate refuses
is not released by machine at all: it goes to a person, who classifies it
under ADR-00000027 section 3 -- and a bump that moves a dependency's
interface is very often a Y, which section 2 keeps human. This is the
boundary that makes an automatic release compatible with a cadence whose
whole point is that behaviour changes are somebody's decision.

### 5. The release is cut by calling the worker, not by pushing a tag

`release-worker.yaml` takes an optional `version` input, resolves it
through `script/ci/release-version.sh`, and sets the release's `tag_name`
from the result, creating that tag at the commit being released. So the
post-merge run calls the worker directly and no tag event is needed. The
resolver applies the same fail-closed rule as the gate: a version it cannot
read is refused rather than resolved to the ref, to a default, or to any
name something already consumes. The prerelease flag is derived from the
resolved version, never from `github.ref_name`, which is `main` on this
path and would have published every RC as a full release.

### 6. The reasoning is recorded, not requested

The gate prints `reason=` beside its approval, and its refusals name the
rule that fired. ADR-00000027 section 3 requires an automatic Z to carry
the classification that justified it so the call is reviewable after the
fact; for a machine-cut Z that record is the gate's own line, and it is a
report rather than a request for approval.

### What this record does NOT decide

- **Whether a compatibility declaration is mandatory.** It is honoured when
  supplied and absent otherwise. Making it required for every repo is a
  cross-repo policy call, and extracting it from a given upstream (parsing
  a `CMakeLists.txt`, say) is repo-specific work that does not belong in a
  shared gate.
- **The shape of the downstream bump workflow.** The trigger, the changelog
  edit and the next-version computation live in the repo doing the bump.
  base supplies the gate and the release entry point; it does not supply
  the workflow, and a shared reusable one is a separate decision with its
  own evidence.

## Consequences

- A repo gets auto-release by declaring an ABI axis per pinned dependency
  and wiring two steps. A repo that declares nothing keeps releasing by
  hand, silently and correctly.
- **A refusal is loud.** The gate exits non-zero, so a post-merge run that
  refuses shows as a failed step rather than a green run that quietly did
  nothing. It blocks no merge -- the bump is already in -- and a caller that
  prefers a refusal to be a normal outcome runs the step with
  `continue-on-error: true` and gates on its `outcome`.
- **The gate trusts the declared axis; it cannot see a SONAME.** A
  dependency that breaks its ABI without moving the component its repo
  declared will pass. That residual risk is accepted knowingly: the
  alternative is base deciding per dependency, which is the guess this
  record exists to refuse. It is bounded by the axis being a per-repo
  declaration a human wrote once and can tighten.
- `release-worker.yaml` -- `on: workflow_call` only, so no tag reaches it
  directly -- now has a second way in: a caller that passes a version rather
  than one whose own job is gated on a tag ref. The tag path is unchanged:
  the input defaults to empty and the resolver falls back to the ref.
- The worker now refuses a tag that is not `vX.Y.Z[-suffix]`. Any repo that
  released under a differently-shaped tag fails at the resolve step with the
  expected shape in the message, instead of publishing a release nothing can
  pin (ADR-00000002). Measured before landing: the resolver accepts all 242
  tags the org's 17 downstream repos and base carry today -- 130 of them
  base's own, 157 distinct names across the set -- refusing none, so the
  rule costs nothing already shipped and only constrains what is cut next.
- An auto-released Z does not fan out, by ADR-00000027 section 4, so this
  cannot turn one dependency bump into seventeen upgrade PRs.

## Alternatives

- **Give the gate a default ABI axis.** Rejected: any default is wrong for
  some dependency, and wrong in the direction that releases a break. The
  librealsense case (SONAME carrying the minor) and a plain
  major-only library disagree, and both are ordinary.
- **Release unless the bump is proven breaking.** Rejected: it inverts the
  burden of proof onto the case that costs the most. It is also #1012's
  unrecognised-input branch restated as a policy.
- **Push the tag with a PAT so the existing tag path fires.** Rejected in
  #829: every downstream repo would have to create, scope and rotate a
  secret to get a behaviour the direct call gives with the default token.
- **Let a gate cut a Y when the bump is breaking.** Rejected: a breaking
  dependency change is precisely the case a person is for, and it
  contradicts ADR-00000027 section 2.
- **Leave the rule to each downstream repo.** Rejected: seventeen
  definitions of ABI-safe, of which the fail-open ones are the invisible
  ones. A shared gate is also a shared place to fix a rule.
- **Make a refusal a silent green no-op.** Rejected: a run that decided not
  to release and said nothing is indistinguishable from one that never
  looked (PRD invariant 2).


## ---- FILE: doc/adr/00000032-base-owns-the-container-entry-point.md ----

# The container entry point is base's; the repo's entrypoint is a bringup it sources

> Serves: PRD invariant 6 (base is a subtree, a downstream repo is a thin
> caller) -- the mechanism half of it. Anything base must be able to change
> later has to SHIP from `.base/`; a file seeded into a repo and then owned
> by it is, by construction, a place base can never change again.

- **Date:** 2026-09-03
- **Status:** Accepted
- **Relates to:** **#945** (the issue this implements); ADR-00000006 (the
  frozen `.base` path contract -- this ADDS `/usr/local/lib/base/entrypoint.sh`
  and changes no frozen path); ADR-00000020 (base owns the single-service
  lifecycle -- the watchdog step this ordering arms); ADR-00000021 (per-start
  container logs -- the tee step it opens first)

## Context

`init.sh` seeds `dist/dockerfile/entrypoint.sh` into a new repo as
`script/entrypoint.sh`, the Dockerfile installs it at `/entrypoint.sh`, and
`ENTRYPOINT ["/entrypoint.sh"]` runs it. That seeded file carried base's own
plumbing: `. /usr/local/lib/base/logging.sh`, `. /usr/local/lib/base/watchdog.sh`,
and the final `exec "$@"`.

From the moment it lands, the file is the repo's. A subtree pull does not
rewrite a repo-owned file, so every change base made to that plumbing
reached NEW repos only. Adding a third runtime helper, or reordering the two
it already had, was not a change to base -- it was a change to seventeen
consumer repos, exactly the class of breakage the v0.41.0 Dockerfile drift
was.

What makes it a defect rather than a design is the asymmetry with the
helpers themselves. `logging.sh`, `logrotate.sh` and `watchdog.sh` ship
correctly: one `COPY .base/dist/script/docker/runtime/ /usr/local/lib/base/`
brings the whole directory into the image, so they DO update with a subtree
pull (ADR trail: #971 collapsed the per-file COPYs for this reason). Only
the file that SOURCED them was stuck in a seeded copy.

## Decision

**Split the entrypoint by ownership, and put base's half where base's other
runtime files already ship from.**

1. **The orchestrator** -- base-owned. It lives at
   `dist/script/docker/runtime/entrypoint.sh` and therefore lands in the
   image at `/usr/local/lib/base/entrypoint.sh` through the directory COPY
   that is already in every consumer Dockerfile. It is the container
   `ENTRYPOINT`. It owns the ordering:

       logging.sh  ->  the repo bringup  ->  watchdog.sh  ->  exec "$@"

   Each step needs the one before it: the tee rebinds stdout/stderr and so
   wraps everything after it; the bringup sets the environment both the
   health check and the workload read; the watchdog may take over the
   process (`on_fail = restart-service`) and never return, so it arms last,
   around the real exec. Every source is readability-guarded, because the
   runtime stage's COPY is opt-in and a repo need not have a bringup.

2. **The bringup** -- repo-owned. It keeps its name (`script/entrypoint.sh`)
   and its image path (`/entrypoint.sh`), holds only the repo's own bringup,
   and is **sourced, not executed**: env it sets has to persist into the
   workload, and control has to return for the watchdog and the exec. It
   therefore carries no `exec` and none of base's plumbing.

**base does not migrate existing repos.** Each repo flips its own
`ENTRYPOINT` and cleans its own bringup, in one commit, in its own PR. base
ships a warn-only detector in the migration list that names the shape and
writes nothing.

The two edits are coupled in one direction: flipping `ENTRYPOINT` before
cleaning the bringup breaks the container, because the un-removed `exec`
fires mid-source. Cleaning first is inert. Doing neither is also inert --
an un-migrated repo runs exactly as before.

## Consequences

- base can add a runtime source line to the orchestrator and every migrated
  repo picks it up on its next subtree pull. That is the whole point.
- A new repo gets the model from the template with no migration at all.
- An existing repo is UNCHANGED by this release: its `ENTRYPOINT` still
  names its own file, which still execs. The orchestrator does land in its
  image on the next rebuild -- through the directory COPY -- where it sits
  inert until the repo flips the `ENTRYPOINT`.
- "Unchanged" has to hold for the `-test` stages too, and it does not come
  for free: the shipped smoke baseline runs inside every one of them and
  asserts the orchestrator, while the runtime stage's helper-directory COPY
  is opt-in. So that assertion is guarded on the model -- it skips where
  /entrypoint.sh still execs, i.e. where that file is the entry point --
  and only bites once a repo has adopted the split, where a missing
  orchestrator is a container that will not start.
- `docker inspect` now records the fact: the `ENTRYPOINT` visibly names a
  `/usr/local/lib/base/` path, so "the entry point is base's" is in the
  image rather than only in this file.
- The bringup being sourced has a real edge: a `set -euo pipefail` in it
  applies to the orchestrator shell from that point on. That is the same
  strict mode the orchestrator already runs under, so the effect is nil
  today, but a bringup that turns an option OFF and does not restore it
  leaks into the exec.
- That edge runs the OTHER way too, and there it is not nil: the
  orchestrator's `set -euo pipefail` now applies to a bringup that never
  set it. The file `init.sh` seeded before this release carries no `set`
  line, so a repo migrating one that sources a ROS overlay runs that source
  under nounset for the first time and dies on ROS's unbound
  `AMENT_TRACE_SETUP_FILES` before the workload starts. The existing
  nounset-source migration is the guard for exactly that, so it now reads
  the ENTRYPOINT as a second source of nounset rather than only the `set`
  line in the file, and README's migration steps carry the `set +u` bracket
  -- the migration can only heal the upgrade AFTER the flip, so the flip
  commit has to carry it itself.
- Two shapes are now footguns the warn-only detector names rather than
  prevents: a bringup that still execs (the watchdog never arms) and one
  that still sources a helper (a second per-start log, or a second
  watchdog). base sees both only at upgrade time, not at build time.
- The notice fires on every upgrade of every un-migrated repo until it
  migrates. That is intended -- it is the fanout's own progress bar -- but
  it is noise for a repo that has decided not to migrate yet.

## Alternatives

- **Keep one file and have `upgrade.sh` rewrite it.** Rejected. The file has
  been hand-edited in every repo for a year; only its owner can tell an
  added bringup line from base plumbing. A parser that guessed would be the
  exact fragility this split exists to leave behind -- and it would be
  guessing on the one file whose failure mode is "the container does not
  start".
- **Swap the paths: orchestrator at `/entrypoint.sh`, bringup somewhere
  else.** Rejected. It moves the repo-owned file in-image (breaking the
  shipped smoke assertion and every repo's own reference to it) and hides
  the ownership change behind an unchanged `ENTRYPOINT ["/entrypoint.sh"]`
  literal, which is precisely the fact worth recording.
- **Rename the repo file to `bringup.sh`.** Rejected: it is the repo's entry
  point conceptually, and the rename would cost every consumer a Dockerfile
  edit to buy a word. The "called by base" fact is recorded in the file's
  own header and in the `ENTRYPOINT` line instead.
- **An `/etc/entrypoint.d/*.sh` drop-in directory.** Rejected as
  over-design: a repo has one bringup, and a drop-in directory is ordering
  machinery for a problem no repo in this org has.
- **Leave it.** Rejected by the measurement: the plumbing had already been
  changed twice (the `_entrypoint_logging.sh` rename, the watchdog source
  line), and each time the fix had to be carried into every repo by hand.


## ---- FILE: doc/adr/00000033-ci-image-provisioning-is-a-script-not-a-job.md ----

# The tooling image is obtained by one script every job calls, not published by one job every job waits for

> Serves: PRD invariant 2 (never fail silently) -- a job that cannot tell
> whether its image corresponds to its checkout must not report on the run;
> and invariant 4 (fail-safe defaults -- an image that cannot be verified is
> rebuilt, never used).

- **Date:** 2026-09-04
- **Status:** Accepted
- **Relates to:** issue **#1010** (the defect this answers, and the
  different remedy it proposed), ADR-00000008 (the sharded coverage gate
  whose eight shards are the jobs the artifact alternative would have
  serialised), ADR-00000018 (ISTQB levels -- why `acceptance` is a distinct
  job from `system`, which is why it was a distinct copy)

## Context

Six jobs of `self-test.yaml` run inside
`ghcr.io/ycpss91255-docker/test-tools`. A pull request that leaves
`dockerfile/Dockerfile.test-tools` alone pulls the rolling `:main` tag
rather than rebuilding a multi-arch image; `:main` is republished only by a
push to main that touches that file. So there is always a window, and after
a failed republish an open-ended one, in which a suite runs inside an image
that does not correspond to its own checkout.

The mitigation for that window was a block of shell pasted into each
consuming job: pull, re-tag under the run's name, probe the result, rebuild
from source if the probe refuses. Five copies did all four steps. The
sixth, `acceptance`, pulled, re-tagged and `exit 0`-ed.

That job is the one the mitigation was written for. It scaffolds a
downstream repo and runs `just docker build test`, whose lint stage is
`FROM ${TEST_TOOLS_IMAGE}`. The exclusion even had a written rationale --
"acceptance executes none of the baked tools, it only uses the image as a
`FROM` base" -- and the rationale was false: the stage that image becomes
runs those tools.

Nothing could have caught it. A test over the workflow could assert "five
jobs probe" and be green with any five; a test naming the six would have
been a roster somebody had to keep. The defect was not in any copy. It was
that there were copies.

## Decision

**The provisioning decision is one script, `script/ci/obtain_test_tools.sh`,
and every consuming job calls it.** The script weighs the three ways to have
the image -- this PR changed the Dockerfile so `:main` is stale by
definition; `:main` corresponds to the checkout and is used; it does not, or
could not be pulled, and the image is built from source -- and always
probes what it pulled.

A job whose buildx runs `driver: docker` passes `--local-build inline`, so
the fallback build happens inside the call and resolves against the host
daemon its later `docker compose build` reads; a job whose build runs
through `docker/build-push-action` (for the GHA layer cache) passes
`delegate` and gates that step on the script's `build_local` output. That
is the only difference between the callers, and it is one word. No count of
either group is written here: which jobs sit on which side is read out of
`self-test.yaml`, and a figure in this record would be a second place to
keep it true.

**The roster the probe asserts is derived from the Dockerfile's final
stage**, not restated: its packages from the stage's `apk add`, its binaries
from what the stage COPYs or symlinks into `/usr/local/bin`. A tool added to
the image is a tool the probe asserts, with nobody in the loop.

**The guard is that no workflow run block names the rolling tag at all.**
That is the assertion a copy cannot satisfy, whoever writes the seventh job.

## Alternatives

**Hoist obtain-and-probe into one job that publishes the image as an
artifact the consumers download.** This is what #1010 proposed, and it does
remove both defects at once -- there is one obtain, so there is no sixth
call site to forget. It was rejected on three counts.

It serialises. Every consumer currently starts as soon as `classify`
finishes; behind a publishing job they start after it, and the coverage
shards ADR-00000008 exists to parallelise are the ones that wait.

It cannot serve the two-arch `acceptance` matrix from one artifact. That
job runs on `ubuntu-latest` and `ubuntu-24.04-arm`, so the artifact job
becomes a matrix too, and the "one obtain" it was bought for is two.

And it is slower on the hot path even ignoring both. `docker save` of this
image, an upload, and a `docker load` per job replaces a GHCR pull that
runs against a warm registry -- for an image whose whole point is that it
is already published.

**Declare the roster explicitly but assert it against the Dockerfile in a
test.** A test comparing two lists keeps both, and the failure lands on
whoever next edits the Dockerfile rather than on the code that was wrong.
Deriving has one list and no failure to route.

**Keep the copies and add a lint that every consuming job probes.** The
lint has to know which jobs consume the image, which is the roster problem
again one level up. It also leaves five copies of a decision that will
diverge in some other dimension next.

## Consequences

The seventh consuming job gets the probe by construction: there is nothing
to remember, and a hand-rolled pull fails the suite by name.

The probe now starts two containers per call instead of five to eight (one
package check, one binary check, plus the pinned-version reads), so the
wider roster costs less than the narrow one did.

A tool added to the Dockerfile immediately becomes something every pulled
`:main` is asserted to carry. Between that commit and the republish, every
job takes the from-source build. That is the intended cost -- it is what
"the image corresponds to this checkout" means -- but it is a real one, and
it lands on the merge that adds the tool rather than on a later PR.

The Dockerfile's final stage is now load-bearing text: a package moved into
a builder stage, or a binary installed somewhere other than
`/usr/local/bin`, changes what the probe requires. The reader is comment-
stripped and stage-scoped for exactly that reason, and both properties are
asserted in `probe_test_tools_spec.bats` rather than left to hold by
accident.


## ---- FILE: doc/adr/00000035-compose-at-the-root-and-the-two-test-axes.md ----

# `compose.yaml` lives at the repo root, and a test has a level AND a type

> Serves: PRD invariant 2 (never fail silently) -- both halves are questions
> whose wrong answer is silent: a compose file Compose cannot find changes the
> project name rather than erroring, and a taxonomy read as one axis makes a
> live test category look retired.

- **Date:** 2026-09-05
- **Status:** Accepted
- **Relates to:** ADR-00000011 (`just` is the single control surface, and the
  compose services it drives), ADR-00000018 (the ISTQB taxonomy this records
  the read-back of), ADR-00000022 (per-instance compose contract -- the
  project-name derivation this depends on)

## Context

Two questions asked on 2026-09-05, both from a reasonable reading of the tree,
both answered wrong by that reading. Neither had a record to point at.

**1. "`compose.yaml` at the repo root is CI's, so should it be under
`.github/`?"** The premise is that it is CI-only. It is not:
`script/test/drivers/../test.sh` names `-f "${REPO_ROOT}/compose.yaml"` on the
path `just test` takes locally, and no workflow file names it at all -- CI
reaches it the same way a developer does, through `just`. The file defines six
services (`test-tools`, `smoke`, `ci`, `ci-system`, `coverage`, `default`), not
one CI service.

That correction does not settle the location question, because "`just test` IS
the local half of CI" is also true. The location has its own reasons.

**2. "We no longer have smoke, only unit and integration -- is there rotted
doc or code?"** There is not. 17 tracked files under `smoke`, and two changes
landed on 2026-09-05 alone (#1045 moved the tree, #1050 protected it from a
half-applied rollback). The reading came from ADR-00000018's model being
remembered as one axis.

Checked while answering: `behavioural`, the category ADR-00000018 retired,
appears 88 times in the tree. Every live occurrence is the adjective ("the
behavioural half", as against the static half), not the category. The changelog
occurrences are history and stay. No rot.

## Decision

### 1. `compose.yaml` stays at the repo root

Three reasons, in order of how expensive it is to get wrong:

**The project name is derived from the file's directory.** Compose's documented
fallback is "the `basename` of the project directory containing the config
file". This repo computes its own project name (`base-<sha256(repo root)[0:12]>`,
stamped as the `base.checkout.path` label so ownership is provable), so moving
the file would not break `just` -- but it would make a bare `docker compose`
disagree with `just` about which project it is in. The file's own header
records what a previous divergence of exactly this shape cost: two different
defaults for the tooling image meant `docker compose build` tagged one image
while `docker compose run` pulled another, the suite ran against the published
image, and nothing warned.

**Discovery is designed for the root.** Compose "traverses the working directory
and its parent directories looking for a `compose.yaml`". At the root, every
subdirectory of the repo finds it. Under `.github/`, nothing does, and every
invocation needs `-f`.

**`.github/` is GitHub's namespace.** Workflows, issue templates, CODEOWNERS,
FUNDING -- read by GitHub. A Docker toolchain file there is findable only by
someone who already knows it moved.

### 2. A test has a LEVEL and a TYPE, and they are different questions

ADR-00000018 established this. It is recorded again here because the model is
routinely read as a single list, and reading it that way makes `smoke` look
retired.

| axis | question | values here |
|---|---|---|
| **Level** | how much of the system is under test | Unit, Integration, System, Acceptance |
| **Type** | what property is being checked | smoke, e2e, regression |
| **Static** | not a test at all | lint |

Every test has both. They are orthogonal, not a hierarchy, and `smoke` is a
**type** -- ADR-00000018's own words are that it "was misclassified as a
level".

**Why smoke still looks like a level, and why that is not a defect.** It has
its own directory, `dist/test/bats/smoke/`, because of *when* it runs rather
than *how much* it covers: those specs are COPYed into every Dockerfile
`-test` stage and executed during `docker build` -- "the does-it-even-come-up
baseline that runs inside EVERY `-test` stage". They are not in the `just test`
bats loop. The directory reflects an execution point, not a fifth scope.

`test/bats/acceptance/` holds no specs today. That is deliberate (a CI-only
level) and tracked by #1046 -- but an empty directory reads as an abandoned one,
which is the other half of why this record exists.

## Alternatives

**Move `compose.yaml` under `.github/`.** The argument is coherent and is the
one that prompted this record: the file is only ever executed by CI or by
`just test`, which is CI's local half, so "it is infrastructure, put it with
the infrastructure" follows. Rejected on the project-name derivation, which is
a mechanism rather than a preference -- Compose names the project after the
directory holding the config file, so a bare `docker compose` would disagree
with `just` about which project it is in, and this file's own header records
what a divergence of exactly that shape already cost once. Discovery and the
`.github/` convention are the second and third reasons, not the first.

**Move it and pass `-f` everywhere.** Removes the discovery objection and none
of the others; adds a flag to every invocation, including the ones a person
types by hand while debugging, which is where the divergence would show up
last.

**Say nothing and let the taxonomy be re-derived each time.** What happened
until now. The cost is measured rather than supposed: the question "we no
longer have smoke, is there rotted doc or code?" was asked on 2026-09-05 about
a category with 17 tracked files that had been modified twice that same day.
Answering it took an audit; the audit found no rot. A record is cheaper than
repeating the audit.

## Consequences

- The location question has an answer to point at, with the mechanism (project
  name from the config file's directory) rather than the convention.
- Anyone reading `doc/test/` and finding four level catalogues plus a smoke
  catalogue has the two-axis model to read them with.
- **Not settled here:** whether `dist/test/bats/smoke/` should be split
  per-stage now that every repo is on the layout (#1046), and whether the
  acceptance level gets content (#1046 again). This record says what the axes
  are, not what should be in each cell.
- If the project name ever stops being self-computed, the compose location
  becomes load-bearing rather than merely conventional, and this record's first
  reason gets stronger rather than weaker.


## ---- FILE: doc/adr/00000036-parameterised-generate-api.md ----

# base is a building block: both generate stages are parameterised APIs

> Serves: PRD invariant 3 (composable by construction) -- restated.
> The overlay contract ADR-00000022 built to serve that invariant turned out to
> serve it only for values, not for shapes.

- **Date:** 2026-09-06
- **Status:** Accepted
- **Relates to:** issue #1087 (this decision), issues #1051 / #1056 / #1062 /
  #1064 (the gaps that produced it), issue #25 (multi_run), issue #600 (the
  division of labour), ADR-00000022 (amended by this -- sections 1 and 3),
  ADR-00000025 (amended by this -- the `.setup.conf.local` axis),
  ADR-00000003 (environment vs workload parameter boundary)

## Context

`multi_run` is being rebuilt as the composition layer #600 describes: base
downstream repos are modules, and multi_run instantiates them -- **including
several instances of the same repo at once**, three lidar units being three
instances of one lidar repo -- and wires them together.

That makes "one repo, many instances" the primary case rather than an edge one,
and four issues filed from the consuming side each found the same wall from a
different angle:

- **#1051** -- fields that collide across instances with no override channel at
  all: `[logging] local_path` (two instances write the same `devel.log`),
  `devices:`, the `config/<c>` binds, stage-level overrides of
  `network_mode` / `privileged` / `ipc` / `pid`.
- **#1056** -- asking for a per-section verdict across all 15 sections, because
  the limits are undiscoverable: "the cost of the current situation is not the
  limits themselves; it is that they are undiscoverable."
- **#1062** -- values the emitter decides that have no config key at all:
  `container_name`, `hostname`, `profiles:`, `stdin_open` / `tty`, `env_file:`,
  and a shipped `[tmpfs]` section the validator does not know about.
- **#1064** -- two field-deploy bundles from one repo cannot co-exist, because
  the project name and the container name are the same baked string.

ADR-00000022 answered the same question in 2026-07 with an **overlay**: one
generated `compose.yaml` per repo, per-instance variation carried by `${VAR}`
interpolation from a per-instance `.env`, and an explicit rejection (its section
1) of regenerating `compose.yaml` per instance. Its section 3 additionally
recorded GPU, `runtime` and `hostname` as *correctly shared* -- co-located
instances share one host's GPU and one X11 cookie -- and therefore deliberately
outside the per-instance contract.

Two things about that answer did not survive contact with the composition case.

**An interpolation carries a value; it cannot carry a shape.** `[build] arg_N`,
`[image] rule_N`, `[gui] mode`, `[additional_contexts]`, an extra
`deploy.resources` block -- these change *which lines exist* in the emitted
file. No amount of `${VAR}` substitution reaches them, so under an overlay-only
contract they are permanently per-repo. #1056 grouped exactly these as "group 3,
where the boundary is undecided", and the honest answer under ADR-00000022 was
"never per-instance".

**"Shares a host" was conflated with "shares an assignment."** Three instances
on one host do share one GPU device tree. It does not follow that they must all
claim it identically: an assembler may want instance 1 on GPU 0, instance 2 on
GPU 1, and instance 3 with no GPU at all. Section 3's row is correct about the
hardware and wrong about the contract.

Underneath both is a framing question, and it is the one that actually decides
this: **is base a configurable application that happens to be reusable, or a
building block that an assembler drives?** ADR-00000022 assumed the first --
base owns the generated artifact, and multi_run adjusts it from outside. The
composition design requires the second.

## Decision

**base is a building block. Both of its generation stages -- devel
(`just docker setup`) and deploy (`just docker setup deploy`) -- are APIs an
orchestrator calls N times against one repo, each call carrying that instance's
parameters and writing a complete result into a directory the caller names. The
repo is not mutated by a call.**

The rule that follows, and the one that replaces #1056's request for a
15-section table:

> Anything base decides at build time or before the container starts must be
> reachable by the caller. Only what is internal to a running container is
> outside the contract.

A value the assembler cannot reach is a defect in the block, not a documented
limit. There is no list of exempt sections.

Two mechanisms carry it.

### 1. The `.setup.conf.local` layer takes a caller-supplied path

The conf chain is `<template>/.setup.conf` -> repo `.setup.conf` ->
`.setup.conf.local`, section-replace at each step. The third layer is already
the right shape: ADR-00000025 section 1 gave it the power to override **any**
section rather than a whitelist. What it lacks is an address -- its path is
fixed at `<repo>/.setup.conf.local`, so two concurrent instances cannot hold two
parameter sets without writing into the repo and racing each other.

A call names the file it wants read as that layer. Two calls, two files, no
write to the repo's own.

### 2. Generation takes an output directory

`deploy` already has `--output`. `devel` writes `compose.yaml` and `.env` into
the repo root with no alternative, so a second instance's generation overwrites
the first's. devel gains the same parameter, and a call emits a complete
self-contained set into the caller's directory.

### What this does to the four issues

- **#1051**: every field it lists is pre-start, so every one becomes reachable.
  The `[logging] local_path` case in particular no longer needs to survive as an
  interpolation -- the value is resolved per call, before emission.
- **#1056**: answered by the rule above rather than by a table. Group 3 is
  reachable; group 1's GPU row is reopened.
- **#1062**: every emitter-decided value becomes a key with today's behaviour as
  its default, `container_name` included (default: emit nothing).
- **#1064**: yes -- the bundle's project and container names become parameters
  with the current baked value as the default, which preserves the stable
  `docker logs` name that motivated baking them.

### Amendments this makes to existing ADRs

**ADR-00000022 section 1** rejected per-instance regeneration. That reasoning
held while generation could only write into the repo: regenerating meant
mutating a shared checkout, and two instances would fight over one file. Once a
call writes to a caller-named directory outside the repo, the objection does not
apply. Per-instance generation is now the supported path for shape-changing
parameters. The `.env` overlay is **not** withdrawn -- it remains correct and
cheaper for values that do not change the emitted file's shape, and every
channel in section 3's table keeps working.

**ADR-00000022 section 3's last row** -- GPU, `runtime`, `hostname` as correctly
shared -- is narrowed to a statement about the host, not about the contract.
These become caller-reachable.

**ADR-00000025 section 6** drew the line that `.setup.conf.local` is a
per-worktree axis and not a per-instance one. That line was drawn because the
file had one fixed location, which made "another parameter set" mean "another
checkout". With a caller-supplied path the same layer serves both axes: a
developer still gets the per-worktree file at the default location, and an
orchestrator passes its own. The layer's semantics -- section-replace, overrides
any section, gitignored at the default path -- are unchanged.

## Alternatives

**Widen the interpolation channel until everything is a `${VAR}`.** Rejected:
it cannot work. Build args, image rules and conditional blocks change which
lines exist, and interpolation substitutes into lines that already exist. This
was the actual finding, not a preference -- #1056's "group 3" is precisely the
set that proved it.

**Publish the 15-section boundary table #1056 asked for and keep the current
limits.** Rejected. It is a coherent answer and it was seriously considered: it
costs nothing to write and it would end the undiscoverability the issue
complains about. It was rejected because the limits it would document are
artifacts of where the generator writes its output, not properties of the
domain. Documenting an accident as a contract makes it permanent.

**Let multi_run generate compose files itself.** Rejected. It would duplicate
the schema, the validators, the stage resolution and the Dockerfile-stage
discovery, and the two implementations would drift -- the failure mode
`resolve_compose.py` already demonstrated before multi_run#26 removed it. It
also loses the two things base solves that multi_run cannot: packing each repo's
image, and keeping `env_file:` indirection so secrets are not inlined into a
resolved artifact.

**Per-instance regeneration into the repo, coordinated by locking.** Rejected:
it mutates a shared checkout, serialises what should be parallel, and leaves the
repo in whichever instance's state was generated last.

## Consequences

**The generated artifact stops being a repo-owned file.** A call's output is the
caller's. `compose.yaml` in the repo root becomes the default output of the
default call rather than the only place generation can land, and `.gitignore`'s
managed block keeps covering it for the developer path.

**The emitter loses the right to decide anything silently.** Every literal it
carries -- `build.context`, `dockerfile`, `networks: driver: bridge`,
`deploy.resources.reservations.devices[0].driver: nvidia`, the X11 passthrough
list, the `devel-test` -> `test` service rename -- is either a key with a
default or is documented as emitter-owned with the reason. #1062 is the
inventory.

**A second guard obligation.** `overlay_guard_spec.bats` today passes because
its fixture avoids every violating branch (#1051 section C). The guard now has
to prove the stronger property: that two calls differing only in their
parameters produce two results differing in exactly those parameters. A fixture
that exercises no divergent branch is worse than no guard, and this repo has
already paid for that shape more than once.

**The support surface grows.** Every newly reachable parameter is a parameter
someone can set wrongly, and the validators, the TUI and the docs all widen with
it. This is the real cost of the decision and it is accepted deliberately: the
alternative is an assembler that accumulates a list of things it cannot do.

**Compatibility.** Nothing a consumer runs today changes behaviour. The default
call with no new arguments reads `<repo>/.setup.conf.local` and writes to the
repo root, exactly as now. The new parameters are additive.

**multi_run#26 changes shape.** Its current design takes the repo's already
generated `compose.yaml` and drives it with `-p` plus an overlay. Under this
decision it calls base to generate per instance instead. That is a real cost on
the consuming side and was accepted with the decision.

**Follow-ups unblocked:** #1051, #1056, #1062, #1064 all resolve through #1087
rather than each needing its own mechanism. **Still open:** #1052 (whether a
module declares a dataflow interface at all) is untouched -- this decision is
about how a block is parameterised, not about what one block offers another.


## ---- FILE: doc/adr/00000037-toml-config-format-unification.md ----

# Unify human-edited config to TOML with typed merge semantics

> Serves: PRD invariant 3 (composable by construction) via a
> machine-parsable, type-safe config format; also the
> one-source-many-render goal and ADR-00000036 (parameterised generate
> API).

- **Date:** 2026-09-06
- **Status:** Accepted
- **Relates to:** ADR-00000001 (setup.conf is the main path),
  ADR-00000003 (env vs workload param boundary),
  ADR-00000025 (per-worktree `.setup.conf.local` override),
  ADR-00000036 (parameterised generate API)

## Context

The current configuration pipeline uses two human-edited formats that
serve Docker container infrastructure:

1. **`.setup.conf`** -- a custom INI dialect parsed by a hand-written
   bash tokenizer (`_ini_tokenize`). 15 sections, 8 of which encode
   ordered lists via numbered keys (`mount_1`, `arg_1`, `device_1`,
   ...). Three-layer override: template `.setup.conf` -> repo
   `.setup.conf` -> `.setup.conf.local`.

2. **`.env.local`** -- a flat `KEY=VALUE` file for container service
   runtime env vars (ADR-00000003). Two-layer: generated `.env`
   (defaults) + `.env.local` (user overrides).

Three problems drove this decision:

- **Format weakness.** INI has no type system -- `true`, `1`, `yes`
  are all valid booleans to different parsers; no arrays, no nested
  structure. The numbered-key workaround (`mount_1`, `mount_2`, ...)
  is fragile: no validation, ordering is implicit, adding/removing
  requires manual renumbering.

- **Merge granularity mismatch.** ADR-00000025 sec. 3 adopted
  section-replace (the entire section is replaced by the upper
  layer) because numbered-key lists cannot be key-level merged
  without producing incoherent combinations neither layer wrote.
  This forced scalar sections (`[gui]`, `[network]`, ...) to also
  be section-replaced even though key-level merge is safe for them
  -- a user who wants to override only `[gui] mode` must copy the
  entire section.

- **Two formats for one concern.** `.setup.conf` and `.env.local`
  both serve Docker but use different formats, different parsers,
  and different merge rules. The split criterion (ADR-00000003 axis
  A: machine-bound vs task-volatile) is correct but could be
  expressed within one format with separate files.

The org has precedent: multi_run#26 chose TOML + Python `tomllib` for
its own config. The config-manager design document (v0.16, 2026-09-02)
independently chose TOML for its config manifest (`config-list.toml`)
with the reasoning: strictness ranking TOML > JSON > YAML (no `no`/`08`
ambiguity, mandatory type distinction, no indentation semantics).

Industry survey of merge strategies across 8 systems (Podman, Docker
Compose, Helm, Kustomize, NixOS, Ansible, Git config, toml-merge)
found a clear consensus: **scalar fields -> key-level merge; array
fields -> replace.** 6/8 systems use this pattern. The two that append
arrays (Docker Compose, NixOS) both needed escape mechanisms (`!reset`,
`mkForce`) to handle the cases where append is wrong.

## Decision

**Unify all human-edited Docker config files to TOML.** Four files,
split by service boundary (ADR-00000003 axis A):

| File | Whose | Concern | Layering |
|---|---|---|---|
| `setup.toml` | the repo's (committed) | Docker infrastructure: how the container is assembled | template -> repo -> (caller-supplied per ADR-36) |
| `setup.local.toml` | the operator's (gitignored) | Per-instance Docker infrastructure override | overrides `setup.toml` |
| `.env.toml` | the repo's (committed) | Container service runtime env defaults | template -> repo |
| `.env.local.toml` | the operator's (gitignored) | Per-instance service env override | overrides `.env.toml` |

**Split criterion.** The boundary is the **service boundary**, not
lifecycle (build vs run):

- `setup.toml` = Docker infrastructure (how the container is built and
  run): image rules, build args, GPU, GUI, network, volumes, devices,
  security, lifecycle, logging, deploy, additional contexts.
- `.env.toml` = service runtime env (how the application inside the
  container behaves): `ROS_MASTER_URI`, `ROS_DOMAIN_ID`, `LOG_LEVEL`,
  `WATCHDOG_ENABLED`, application-level parameters.

The two have **zero intersection** at the service level. If overlap
is discovered, `.env.toml` takes precedence because its purpose is
the container-internal service. The current `[environment]` section
splits along the service boundary: infrastructure env vars
(`DISPLAY`, `NVIDIA_VISIBLE_DEVICES`, `PULSE_SERVER` -- host
interfaces the container needs to function) stay in `setup.toml`;
service runtime env vars (`ROS_MASTER_URI`, `LOG_LEVEL`,
`WATCHDOG_ENABLED`) move to `.env.toml`.

**TOML structure.** Scalar sections use standard `[table]` syntax;
list-shaped sections use `[[array of tables]]`:

```toml
# scalar section -- key-level merge in overlay
[gui]
mode = "auto"

[network]
mode = "host"
ipc = "host"

# array section -- array replace in overlay
[[volumes]]
source = "./src"
target = "/opt/workspace"
mode = "rw"

[[volumes]]
source = "/dev/shm"
target = "/dev/shm"

[[build.args]]
key = "APT_MIRROR_UBUNTU"
value = "tw.archive.ubuntu.com"

[[devices]]
path = "/dev/video0"

[[image.rules]]
pattern = "jetson*"
tag = "l4t"
```

**Merge semantics.** Type-aware, matching the industry consensus:

- **Scalar keys within a `[table]`**: key-level merge. The upper layer
  overrides only the keys it defines; unmentioned keys inherit from
  the lower layer.
- **`[[array of tables]]`**: array replace. If the upper layer defines
  any `[[volumes]]` entry, the entire volumes array replaces the lower
  layer's. No append, no index-based merge.

This resolves ADR-00000025 sec. 3's concern: the numbered-key ordered
lists that forced section-replace are gone. Scalar sections that were
collateral damage of the blanket section-replace rule can now be
key-level merged safely.

**Generated outputs remain Docker-native format:**

```
compose.yaml     <- from setup.toml (infrastructure)
.env             <- from setup.toml (infra env) + .env.toml (service env)
.env.local       <- from .env.local.toml
.env.generated   <- interpolation cache (unchanged)
```

**Containerised parsing.** TOML is parsed before `docker compose up`
-- the parse results ARE its inputs. The parser runs in a dedicated
container image (`toml-bridge`), not on the host: the host contract
is Docker + Git + `just` and nothing else, and a host-side Python or
binary would add a fourth dependency whose version the project cannot
control across Ubuntu 16.04--24.04 machines. Docker is already
required, so invoking the parser via `docker run` adds no new
prerequisite. Inside the container the parser is Python with vendored
`tomli` (the backport accepted into the stdlib as `tomllib` via
PEP 680), which is zero-dependency, ~1000 lines, MIT-licensed, and
supports Python 3.6+. The merge logic (type-aware: scalar key-level,
array replace) also runs in Python where the type information is
native (`dict` vs `list`). The `toml-bridge` image is a standalone
Dockerfile (`dockerfile/Dockerfile.toml-bridge`); `test-tools` pulls
from it via `COPY --from` so downstream repos inherit the capability
through the existing `test-tools-stage` pattern.

## Alternatives

- **A1 -- Stay with INI + flat `.env`.** Zero migration cost, but
  preserves the numbered-key fragility, the section-replace
  collateral damage on scalar sections, and the two-format
  maintenance burden. The hand-written `_ini_tokenize` parser has
  known edge cases. Rejected because the problems compound as
  sections grow.

- **A2 -- YAML for everything.** Rich type system, native in Docker
  Compose. Rejected because: YAML has well-documented parsing
  ambiguities (`no` as boolean, `08` as string vs int depending on
  YAML version), indentation-significant syntax is error-prone for
  hand-editing, and the config-manager project already chose TOML
  over YAML with the same reasoning.

- **A3 -- JSON for everything.** Strict and unambiguous. Rejected
  because: no comments (unacceptable for human-edited config files),
  trailing-comma errors, verbose syntax for the kind of config
  humans write by hand.

- **A4 -- Single file (setup.toml only) with `[environment]` section
  for service env.** Simpler, but violates the service boundary:
  `setup.toml` is Docker infrastructure, and forcing users to edit
  Docker config to change application-level env vars conflates two
  concerns. The realsense_ros1 repo demonstrates the split is real
  and practiced: its `setup.conf [environment]` is empty; all
  service runtime env vars (`ROS_MASTER_URI`, `ROS_IP`,
  `WATCHDOG_ENABLED`) come via `.env.local`.

- **A5 -- Terraform-style `.tf` + `.tfvars` split.** Rejected
  because `setup.conf` drives both build and run; the lifecycle
  boundary that Terraform splits on (declaration vs values) does not
  map to our structure.

- **A6 -- Array append instead of replace.** Rejected by industry
  evidence: 6/8 surveyed systems use array replace; the two that
  append (Docker Compose, NixOS) both needed escape mechanisms.
  Append also reintroduces the inability to remove items that
  ADR-00000025 sec. 3 identified as broken for ordered lists.

## Consequences

- The `[environment]` section splits along the service boundary:
  infrastructure env vars (host interfaces like `DISPLAY`, GPU
  visibility) stay in `setup.toml`; service runtime env vars
  (application parameters) move to `.env.toml`. `setup.toml` has
  zero application-level env vars.

- Scalar-section overrides become lighter: an operator who wants only
  `[gui] mode = "wayland"` writes one key, not the entire section.

- Array-section overrides remain explicit: writing any `[[volumes]]`
  replaces the full list, preserving the "what you see is what you
  get" property.

- The `_ini_tokenize` bash parser is replaced by a containerised
  TOML bridge (`toml-bridge` image). The bash shim calls
  `docker run` and receives the merged result. The host contract
  (Docker + Git + `just`) does not grow.

- `setup_tui.sh` (2975 lines + 691-line backend) is frozen until the
  TOML migration completes. The TUI's INI-aware editor functions
  (`_edit_section_*`) cannot operate on TOML structure. A rebuild or
  replacement (possibly by the config-manager Web UI) follows the
  migration.

- Migration path for downstream repos: a one-time converter
  (`setup.conf` -> `setup.toml`, `.env.local` -> `.env.local.toml`)
  runs during the first `init.sh` resync after upgrade, gated on
  file existence (same pattern as the `.env` -> `.env.local` migration
  in ADR-00000003's 2026-08-26 amendment).

- Amends ADR-00000025 sec. 3: section-replace is no longer blanket.
  The merge rule is now type-aware (scalar key-level, array replace).
  The reasoning in sec. 3 (ordered lists cannot be key-merged) remains
  correct and is the basis for the array-replace half of the new rule.

- Amends ADR-00000001: "setup.conf keeps section-replace semantics"
  is refined to type-aware merge semantics for `setup.toml`.

- Timing: this migration is internal to the generate API (ADR-36).
  The TOML files are inputs to the same pipeline that currently reads
  `.setup.conf`; generated outputs (`compose.yaml`, `.env`) are
  unchanged. ADR-36's parameterised API accepts `setup.local.toml` as
  the caller-supplied layer.

- The 15 sections (`[project]`, `[gui]`, `[gpu]`, ...) keep their
  current TUI-oriented structure in phase 1 (format migration). A
  future phase restructures sections to align with the Docker Compose
  spec, at which point the TUI owns its own grouping/view layer
  instead of the config structure mirroring TUI screens.

- JSON Schema validation of the parsed TOML structure (as practiced by
  the config-manager project, sec. 6.2) is a natural follow-up but not
  part of this decision.


## ---- FILE: doc/adr/00000038-architecture-diagrams-in-doc-arch.md ----

# Architecture diagrams live in doc/arch/ as self-contained HTML

> Serves: PRD invariant 10 (documentation is derived, not duplicated)
> -- visual architecture artifacts parallel to prose ADRs, one
> convention across all repos.

- **Date:** 2026-09-06
- **Status:** Accepted
- **Relates to:** ADR-00000037 (toml-config-format-unification),
  ADR-00000036 (parameterised generate API)

## Context

The project accumulates architectural decisions in `doc/adr/` as
prose Markdown. ADRs record **why** a decision was made, but the
resulting structure -- file relationships, data flow, merge
semantics, phase dependencies -- is hard to convey in prose alone.

ADR-00000037 (TOML config unification) demonstrated the gap: six
inline SVG diagrams, four tables, and two before/after comparisons
were needed to make the four-file structure, type-aware merge
semantics, and generation pipeline legible. Embedding that volume
of visual content inside a Markdown ADR would degrade readability
of the decision record itself.

The project has no static site generator, no documentation build
pipeline, and no external diagram hosting. Diagrams must be
viewable by opening a file in a browser -- nothing to install,
nothing to build.

Multiple repos under the org need to follow the same convention so
that cross-repo architecture references are predictable.

## Decision

**Architecture diagrams go in `doc/arch/<topic>.html` as
self-contained HTML files.** Convention:

- **Location:** `doc/arch/`, parallel to `doc/adr/`. ADRs record
  decisions; arch diagrams record the resulting structure.

- **Format:** Single `.html` file, no build step. Open in any
  browser. All CSS in `<style>`, all diagrams as inline SVG, no
  external images. The only permitted external dependency is Google
  Fonts (`fonts.googleapis.com`) with a real fallback stack -- the
  page remains fully legible offline when fonts fall back.

- **Naming:** `<topic>.html` in kebab-case. No numeric prefix
  (unlike ADR filenames) because diagrams have no sequence
  semantics. Examples: `config-pipeline.html`,
  `entrypoint-flow.html`, `ci-matrix.html`.

- **Theme:** CSS custom properties with light/dark support via
  `prefers-color-scheme` media query and `data-theme` attribute.
  Every colour defined as a token on `:root`.

- **Language:** Descriptive text in Traditional Chinese. Technical
  terms (TOML, Docker, ADR, key-level merge, array replace, etc.)
  remain in English. `<title>` in Chinese.

- **Cross-reference:** ADRs reference diagrams with a relative
  path: `See [config architecture](../arch/config-pipeline.html)`.
  Diagrams reference their parent ADR(s) in a subtitle or ref line.

- **Downstream repos:** Create `doc/arch/` and follow the same
  convention. Do not copy base's diagrams into downstream repos --
  base decisions stay in base. Downstream ADRs reference base
  diagrams by repo name: "See base `doc/arch/config-pipeline.html`".

## Alternatives

- **A1 -- Embed diagrams in ADR Markdown.** Zero new files. Rejected
  because Mermaid fences are limited (no fine-grained positioning,
  no semantic colour tokens, no dark-theme control), and large
  inline SVG blocks destroy ADR readability. The ADR becomes a
  diagram document instead of a decision record.

- **A2 -- External diagram tool (draw.io, Figma, Miro).** Richer
  editing. Rejected because: requires an account, diagrams are not
  version-controlled alongside the code, offline access depends on
  export discipline, and cross-repo convention enforcement is
  impossible.

- **A3 -- Generated diagrams from code (Structurizr, D2, PlantUML).**
  Source is plain text, diffable. Rejected because: adds a build
  dependency (the project has none), and the diagrams needed here
  are bespoke visual explanations with precise layout and semantic
  colouring, not auto-layout boxes-and-arrows.

- **A4 -- Put diagrams in `doc/adr/` alongside their ADR.**
  Co-locates decision and visual. Rejected because: one ADR may
  need multiple diagrams (ADR-37 needs six), and mixing `.md` and
  `.html` in the ADR directory blurs the "one ADR = one Markdown
  file" convention that `new-adr.sh` and the ADR index rely on.

- **A5 -- PNG / SVG image files referenced from Markdown.** Simple.
  Rejected because: binary PNGs are not diffable, standalone SVG
  files cannot carry their own CSS theming, and neither format
  supports interactive elements if needed later.

## Consequences

- `doc/arch/` is a new directory in the repo tree. The
  `check-claude-md-tree.sh` lint (if it covers `doc/`) needs to
  include it.

- Architecture diagrams are first-class artifacts: committed,
  reviewed in PRs, versioned with the code. No external dependency
  beyond a browser.

- ADRs stay focused on prose rationale. The "see diagram" link is
  one line, not 200 lines of embedded SVG.

- Downstream repos that adopt `doc/arch/` get a predictable
  location for their own diagrams without inheriting base's content.

- HTML files are slightly harder to diff than Markdown in a PR
  review. Mitigated by: (a) SVG is text, so line-level diffs work;
  (b) the file is opened in a browser for visual review anyway.

- First diagram: `doc/arch/config-pipeline.html` (ADR-37 TOML
  config architecture, 11 sections, 883 lines).


## ---- FILE: doc/adr/README.md ----

# ADR index + PRD audit

This is the index of base's Architecture Decision Records **and** the
audit that maps each ADR onto [`doc/PRD.md`](../PRD.md) -- base's north
star. Every ADR now carries a one-line `> Serves:` back-reference to the
PRD invariant (1-11), goal, or scope item it upholds; this table is the
consolidated view.

**The filesystem is the ADR registry.** There is no database and no
manually-curated master list of numbers -- the set of `doc/adr/NNNNNNNN-<slug>.md`
files *is* the registry. The ADR-numbering lint
(`script/test/drivers/adr_numbering.sh`, wired into `just test`; landed
with the PRD work under #808 / #823) guards it: a duplicate ADR number or
a malformed filename **fails** CI, while a numbering **gap** is warned,
not failed. This `README.md` is deliberately *not* an ADR file (its name
does not match `NNNNNNNN-<slug>.md`), so it does not perturb that lint.

**Authoring rule.** The ADR-structure lint
(`script/test/drivers/adr_structure.sh`) requires exactly one occurrence of
each required part -- `> Serves:`, `## Context`, `## Decision`,
`## Consequences`, `## Alternatives`, `- **Status:**` -- at column 0, so an
ADR that illustrates one of those lines indents the illustration out of
column 0, and an amendment that restates a section or a status uses a `###`
heading or a different key (`- **Amendment status:**`). The rule is about
column 0 and nothing else -- the lint does not know what a fence is -- so a
parked or commented-out copy of one of those lines counts exactly like a
live one and is indented too.

## Anomalies (resolved)

- **`00000009` is an intentional gap.** There is no ADR-9 and none will
  be back-filled; the number was skipped. The numbering lint warns on it
  and passes. Do not invent a `00000009`.
- **`ADR-00000020` is a single canonical record.** A parallel-authoring
  incident once produced two files both numbered `ADR-00000020` (the very
  case the #823 numbering lint now catches). The canonical
  `00000020-base-owns-single-service-lifecycle.md` is the foundational
  "base owns the single-service lifecycle" axiom; the separate
  init-default-toggle content was **folded into** it (init defaults ON is
  ADR-20's two-branch-rule example, see its Consequences). There is no
  second ADR-20.

## Verdict vocabulary

| Verdict | Meaning |
|---|---|
| `keep` | Accurate as written; no change needed (inline amendments, where present, are already recorded in the file). |
| `amend` | A factual detail is now stale and should be refreshed (tracked as a follow-up, not edited here). |
| `supersede` | Replaced by a later ADR (named). |
| `merge` | Overlaps another ADR and could be consolidated (named). |
| `elevates-invariant` | Established a PRD Core Invariant (named 1-11). |
| `elevates-principle` | Established a PRD Design Principle (named P1-P9). |

The eleven PRD Core Invariants: **1** one container = one service / base
owns the single-service lifecycle; **2** never fail silently; **3**
composable by construction; **4** fail-safe defaults; **5** the
two-branch default rule; **6** base is a subtree / downstream a thin
caller; **7** rigorous, industry-aligned test bar; **8** development and
field are cleanly separated, provisioned by opposite means; **9** identity
and naming are resolved once, from a file; **10** documentation is
derived from the code, never duplicated beside it; **11** a default is
decided by two questions, not by preference. ADRs that are pure
*mechanisms* serve a goal but map to no invariant -- the table says so
explicitly. Below the invariants the PRD also carries **Design
Principles** (P1-P9) and a **Conflict Priority** order; an ADR that
establishes one of those is `elevates-principle`.

## Audit table

| ADR | Verdict | Serves | Note |
|---|---|---|---|
| 00000001 -- setup.conf vs compose-native boundary | keep | mechanism (config-resolution boundary; serves the one-source-render goal), no invariant | The escape-hatch/`--env-file` case was refined into a primary path by ADR-00000003. |
| 00000002 -- no `latest` tag for base | keep | invariant 6 (subtree / propagation) -- mechanism | Immutable version pinning of subtree + workflow refs keeps propagation reproducible. Dated example `v0.39.0` is self-dating. |
| 00000003 -- env vs workload boundary + field delivery | keep (amended by 00000023) | invariant 3 (axis-A `.env` overlay model) + goal (one source -> many render; field delivery); also invariant 8 (its env-row override generalizes to config files) | Foundational to the PRD Product Shape; refines ADR-00000001; the overlay model is the seed ADR-00000022 later elevates. **Amended 2026-07-15 (ADR-00000023):** its structured-config Field cell gains a mount-wins `-v` override and "compose does not travel" is refined to "a resolved compose travels" (in-file amendment note). |
| 00000004 -- category-first test layout | supersede (by 00000012) | invariant 7 (test bar) -- mechanism | Category-first reversed to tool-first; Status already records the supersession. |
| 00000005 -- adopt `just` over the Makefile | keep | invariant 6 (thin-caller entrypoint) -- mechanism | The single discoverable user entry ADR-00000010/00000011 build on. Dated `13 downstream repos` / `v0.39.0` are self-dating. |
| 00000006 -- upgrade.sh path contract | keep | invariant 6 (subtree upgrade path) -- mechanism | Frozen interior paths; already carries forward-pointers to ADR-00000010/00000011's `dist/` moves. |
| 00000007 -- log TTY cache + transcript layering | keep | mechanism (wrapper log/transcript single-sink fidelity), no invariant | Ensures a transcript tee cannot silently flip terminal output format. |
| 00000008 -- sharded coverage PR gate | keep | invariant 7 (coverage gate -- a *swappable* mechanism, not the invariant) | Heavily amended inline (Codecov removed, dynamic shards, per-line union merge); all recorded in-file. |
| 00000010 -- layered `just` entry + base/downstream split | elevates-invariant (6) | invariant 6 (subtree / thin caller) | Established the `dist/` split + layered entry. Its docker-top-level decision was superseded-in-part by ADR-00000011 sec.1 -- recommend a forward-pointer (follow-up). |
| 00000011 -- zero-special-case `just` command model | elevates-invariant (6) | invariant 6 (subtree / thin caller) | The current command model + generic test runner; amends ADR-00000010 and ADR-00000006. |
| 00000012 -- tool-first test layout | keep (supersedes 00000004) | invariant 7 (test bar) -- mechanism | Its category *vocabulary* was later amended by ADR-00000018; forward-pointer already present. |
| 00000013 -- strip transient issue refs from comments | keep | invariant 2 (never fail silently) -- the issue-ref lint | PRD invariant 2 names the issue-ref lint as one of its enforcing guards. |
| 00000014 -- decompose setup.sh into subsystem libs | keep | mechanism (source architecture / testability), no invariant | Deep-module decomposition; underpins invariant 7's testability but is an architecture decision. |
| 00000015 -- test files mirror source | keep | invariant 7 (test bar) -- mechanism | Lowers the per-file coverage shard floor; complements ADR-00000008/00000012. |
| 00000016 -- coverage tooling evaluation | keep | invariant 7 (swappable coverage mechanism) | Status is **Rejected**: the spike disproved the "kcov = heavy ptrace" premise; kcov stays. Accurate record. |
| 00000017 -- CI throughput ceiling + shard strategy | keep | invariant 7 (swappable CI/shard mechanism) | PRD explicitly lists this as a swappable mechanism under invariant 7. |
| 00000018 -- ISTQB test taxonomy | elevates-invariant (7) | invariant 7 (rigorous, industry-aligned test bar) | The *commitment* establisher; supersedes only ADR-00000012's category vocabulary. |
| 00000019 -- network host default, bridge opt-in | elevates-invariant (4) | invariant 4 (fail-safe defaults) | The general principle's instance; a sibling lifecycle-defaults decision to ADR-00000020. |
| 00000020 -- base owns the single-service lifecycle | elevates-invariant (1) | invariant 1 (single-service lifecycle); also invariant 5 (two-branch default rule) | Canonical single ADR-20; init-toggle content folded in (see Anomalies). |
| 00000021 -- per-start container logs + shared logrotate | keep | invariant 1 (single-service lifecycle) -- mechanism | The #805 log-persistence lifecycle capability realising invariant 1. |
| 00000022 -- compose<->multi_run overlay contract | keep (amended by 00000025) | invariant 3 (composable by construction); also invariant 2 (the overlay guard) | The overlay contract + `overlay_guard_spec.bats`; PRD names it under both invariants 2 and 3. **Amended 2026-08-05 (ADR-00000025):** the project `name:` row's emitted form is now `${PROJECT_NAME}` (still an interpolation, so the forward invariant and its guard are untouched), plus an explicit statement that a per-worktree `.setup.conf.local` is NOT this contract's mechanism -- it acts before `compose.yaml` is generated (in-file amendment note). |
| 00000023 -- config field-override + self-contained field-deploy contract | elevates-invariant (8) | invariant 8 (dev/field separation, provisioned by opposite means) -- established with ADR-00000003 | The git-tracked provisioning axis, baked-default + mount-wins `-v` override (file analog of ADR-3's env `-e`), deploy-as-resolved-self-contained-compose (amends ADR-3's "compose does not travel"), the deployable-stage rule, and the `config/<component>/deploy.manifest` tunability channel. Reconciled with ADR-00000022 (single-file config `-v` != general volume topology). Mechanism in #831 / #832 / #833. **Amended twice in-file (#874):** sec. 2 now states the mount-override is read-only by default with an explicit `rw` opt-in (#870), and sec. 4's `deployable = not devel and not *-test` is restated as what `_is_deployable_stage` actually enforces (it also rejects `sys` / `devel-base` and the legacy aliases). |
| 00000024 -- bake self-built artifacts at `/opt`, not `$HOME` | keep | invariant 8 (dev/field separation) -- mechanism; also invariant 2 via the `home-literal` lint | `ENV HOME` resolves at BUILD time, so anything baked under `$HOME` is coupled to the build-time `USER_NAME` and breaks on a rebuild / GHCR pull / `docker save`+`load` under a different user. Artifacts go to absolute `/opt`; `~/x -> /opt/x` is a discoverability symlink nothing sources. Its mechanical rule (no concrete username in a path) is gated by the `home-literal` lint. |
| 00000025 -- per-worktree `.setup.conf.local` override + one resolved project name | elevates-invariant (9) | invariant 9 (runtime-name divergence is a file-recorded override) -- established; also invariant 2 (shadowed-write warning, deploy refusal, config-summary row) and invariant 8 (the field refusal) | Third conf layer (`.setup.conf.local`, gitignored, section-replace like the two below it), `[project] name` shipped empty, and `_resolve_project_name` as the single producer both `-p` and compose's `name:` read via `.env.generated`. Un-retires the `.gitignore` entry #879 retired. Removes `SETUP_CONF`. Explicitly NOT a reversal of #600 (configuration, not orchestration) and NOT ADR-00000022's channel (acts before compose.yaml is generated) -- **amends ADR-00000022 in-file** with that division of labour and the `${PROJECT_NAME}` row. |
| 00000026 -- self-hosted eligibility is a static property of `runs-on` | keep | invariant 7 (rigorous test bar) -- mechanism; also invariant 2 (the `self-hosted-guard` lint, and the fork-PR rollup failure instead of a vacuous green) | The org runs ONE org-level self-hosted runner in a `visibility: all` / `allows_public_repositories: true` group, on a shared workstation, and this repo is public. Eligibility is computed from `runs-on` (anything that does not statically resolve to a reserved `ubuntu-*` / `windows-*` / `macos-*` label is eligible and fails closed), so the guard cannot be missed by job N+1 the way `_LINT_TOOLS` / the downstream roster / the release archive path list each were. Enforced by the `self-hosted-guard` lint; `ci-rollup` fails a fork PR rather than collapsing a guarded skip into a green required check. Prerequisite named by ADR-00000017. |
| 00000027 -- release cadence + fanout trigger (Z automatic/per-bug, X/Y human, only X/Y fans out) | keep | invariant 6 (subtree / propagation) -- the cadence at which the single source of truth propagates, and who decides each step; also invariant 2 (the classification reasoning is recorded, so a wrong call is reviewable rather than invisible) | Policy behind the `semver-bump` / `/release` procedure, not a new mechanism. A `vX.Y.Z` (Z>0) is cut by the agent without asking -- restoring `semver-bump`'s own table -- and **one bug = one Z**, so a downstream can name the release carrying its fix; `vX.Y.0` / `vX.0.0` stay the maintainer's. The binding half is classification: an issue whose fix changes behaviour is a Y no matter what it is labelled (the v0.42.1 content -- #914, #915, PR #929, #882 -- is the recorded case). #927's fanout is triggered by X/Y **only**: `just base upgrade <tag>` is one `git subtree pull` to that tag, so a Y delivers every Z in between and nothing is skipped -- only the notification is batched. PR-body requirements depend on #926. **Amended 2026-09-03 (ADR-00000031):** sections 1 and 3 gain a third actor -- a Z may also be cut by a GATE, with no person and no agent in the loop, in the one case a gate can decide (a downstream repo's ABI-safe dependency bump); section 2 is untouched and bounds it, and section 4 keeps such a Z from fanning out (in-file amendment section). |
| 00000028 -- documentation is derived, not duplicated (test statistics live only in the release) | elevates-invariant (10) | invariant 10 (documentation is derived, not duplicated) -- established; also invariant 2 (a hand-maintained figure goes stale silently) | A figure a machine can compute is computed when it is needed, not stored where a person keeps it true; the statistics belong to a release, rendered from the JUnit XML the tag-push run emits. Records the distinction from PR #943 (which deleted a hand-built *source* archive GitHub already produces, not run evidence) and names #952's committed coverage SVG as the open case the invariant decides. **Amended twice, both in sec. 1.** #999 (2026-09-03): the per-test rows are KEPT and GENERATED from `# why:` markers beside each test -- deleting was cheaper than relocating only while relocating meant doing it by hand. #978 (2026-09-04): the five grand-total lines are GONE and `_sync_test_md_index` with them, but the per-spec `### <path> (N)` count, the per-level catalogue totals and the doc-count drift gate all STAY, so invariant 2's guard list is unchanged. Sec. 2's release report is still unbuilt. |
| 00000029 -- early return is the default function shape | elevates-principle | PRD design principle P1 (early return is the default shape of every function) -- established; no invariant directly (it is the function-level shape ADR-00000014's seams assume, so it stands behind invariant 7's testability) | Decision 1 of the #994 quality epic. States the shape rather than the limit: the depth/length/parameter thresholds are a net that reports where the shape was not applied, not a target. Records the rejection of a baseline file (a hand-kept roster that decays and converts a gate into an inventory of debt) and of gating new code only, and the framing error it corrects -- an earlier nesting audit read depth as 44 violations to rank and fix, which buys 44 fixes and then 44 more because it never reaches the next function written. |
| 00000035 -- `compose.yaml` lives at the repo root, and a test has a level AND a type | keep | invariant 2 (never fail silently) -- both halves are questions whose wrong answer is SILENT: a compose file Compose cannot find changes the project name rather than erroring, and a taxonomy read as one axis makes a live test category look retired | Answers two questions asked on 2026-09-05 that had no record to point at. The compose half: the file is not CI-only (`test.sh` names it on the local `just test` path and no workflow names it at all), and it stays at the root because Compose derives the project name from the config file's DIRECTORY, because discovery traverses parents from the root, and because `.github/` is GitHub's namespace. The counter-case is recorded rather than dismissed. The taxonomy half re-states ADR-00000018's two axes because the model is routinely read as one list, which makes `smoke` look retired: it is a TYPE, its own directory reflects WHEN it runs (COPYed into every `-test` stage, executed during `docker build`) not how much it covers, and 17 files plus two changes on 2026-09-05 say it is live. `behavioural` was checked for rot: 88 mentions, every live one the adjective, not the retired category. |
| 00000036 -- base is a building block: both generate stages are parameterised APIs | elevates-invariant (3) | invariant 3 (composable by construction) -- restated. The overlay ADR-00000022 built to serve invariant 3 serves it only for VALUES; an assembler composing several instances of one repo needs SHAPES too, and could not get them | Four issues filed from the consuming side (#1051 colliding fields with no channel, #1056 the undiscoverable 15-section boundary, #1062 emitter decisions with no key, #1064 two bundles from one repo colliding) turned out to be one wall: `${VAR}` substitutes into lines that already exist, so build args, image rules and conditional blocks were permanently per-repo. The rule replacing the per-section table: anything decided at build time or before the container starts must be caller-reachable; only what is internal to a running container is outside. Two mechanisms -- a caller-supplied path for the `.setup.conf.local` layer, and an output directory for devel generation. ADR-00000022 s1 (no per-instance regenerate) and s3 (GPU/runtime/hostname correctly shared) and ADR-00000025 s6 (the worktree-vs-instance line) are amended in place, not superseded: the overlay stays correct for value-shaped fields, and s1's reasoning was sound while generation could only write into the repo. Accepted cost: a wider support surface, and multi_run#26 changes shape (it calls base to generate per instance instead of driving one pre-generated file with `-p`). |
| 00000032 -- the container entry point is base's; the repo's entrypoint is a bringup it sources | elevates-invariant (6) | invariant 6 (base is a subtree, downstream a thin caller) -- the mechanism half: anything base must be able to change later has to ship from `.base/`, so it cannot live in a file seeded into a repo and owned by it from then on | base's plumbing moved out of the seeded `script/entrypoint.sh` into an orchestrator shipped in the runtime helper directory. Records why base does NOT rewrite existing entrypoints (only the owner can tell a bringup line from base plumbing), and why the two per-repo edits -- flip `ENTRYPOINT`, clean the bringup -- must land together. Adds `/usr/local/lib/base/entrypoint.sh`; changes no path ADR-00000006 freezes. |
| 00000031 -- ABI-gated dependency-bump auto-release | keep (amends 00000027) | invariant 6 (one convention in base rather than seventeen repo-local definitions of "safe to release") -- mechanism; also invariant 4 ("cannot determine" resolves to not releasing) and invariant 2 (the gate names the rule that refused) | The answer to #829's second half. `script/ci/abi-gate.sh` decides one question -- did this dependency's declared ABI component move -- and refuses everything else: an unreadable version, an undeclared or unrecognised axis, a 0.x pin declared major-only, a downgrade, an unchanged pin, a pair the upstream compat declaration does not sanction. No default ABI axis, deliberately: librealsense's SONAME carries its minor and a plain major-only library disagrees, so any default is wrong for somebody in the direction that releases a break. A gate may cut a Z and nothing else, which is what keeps it inside ADR-00000027 section 2. The release goes through the new `version` input of `release-worker.yaml` (`on: workflow_call` only, reached by a caller's job) rather than a bot-pushed tag, because an event created with the default `GITHUB_TOKEN` starts no workflow run. Written against #1012's defect class. |
| 00000030 -- the `config/<component>/` layout + the preset selector | keep | invariant 8 (dev/field separation) -- completes ADR-00000023 with the half it left open, WHICH config a build bakes; also invariant 4 (the committed preset is the inert one), invariant 2 (a selector resolving to nothing is reported, not found inside `docker build`) and invariant 10 (audience is not a second record of tunability) | Answers #826 ask 1 and all five of #827, which ADR-00000023 only forward-referenced. The org was surveyed first: preset selection had already converged on one shape in three repos (a repo-root symlink into `config/<component>/` read through an `ARG` whose default is its own name), so the decision writes down what works rather than inventing a mechanism -- and the one repo choosing a preset without the symlink pays for it with a three-branch `COPY` fallback duplicated per stage. Grouping is by count, not taxonomy (`launch/` exists once there is a second `*.launch`), which describes 6 of 6 component directories today where mandatory type-first would migrate 4. Audience directories are refused as a second record of what `deploy.manifest` already says. Enforcement reaches only what base can see: base reports the selectors in the tree it runs against, and nothing gates a downstream's directory shape. |

## Audit conclusion

- **keep:** 18 (00000001, 00000002, 00000003, 00000005, 00000006,
  00000007, 00000008, 00000012, 00000013, 00000014, 00000015, 00000016,
  00000017, 00000021, 00000024, 00000026, 00000027, 00000031) -- 00000003
  is `keep (amended by 00000023)` and 00000031 is `keep (amends 00000027)`,
  both amendments recorded inline in-file. 00000024, 00000026, 00000027 and
  00000031 postdate the audit itself and are listed for index
  completeness.
- **supersede:** 1 (00000004, by 00000012 -- already recorded)
- **elevates-invariant:** 9 (00000010, 00000011 -> inv 6; 00000018 -> inv
  7; 00000019 -> inv 4; 00000020 -> inv 1; 00000022 -> inv 3; 00000023 ->
  inv 8; 00000025 -> inv 9; 00000028 -> inv 10). Invariant 11 was not
  established by an ADR: it is invariant 5 generalised in the PRD itself,
  and ADR-00000020 / ADR-00000019 / ADR-00000007 are the instances it
  reads back.
- **elevates-principle:** 1 (00000029 -> P1). Postdates the audit; listed
  for index completeness.
- 00000030 -> invariant 6. Postdates the audit; listed for index
  completeness.
- **00000030** postdates the audit and is listed for index completeness;
  its verdict column reads `keep` because it is a mechanism decision under
  invariant 8, which ADR-00000023 already established.
- **amend:** 0 in the verdict column; 1 recommended follow-up (a
  forward-pointer on 00000010 -- see below)
- **merge:** 0

The decision log is already internally coherent: every ADR that was
reversed or refined by a later one carries its own inline
amendment/supersession note. The audit's net additions are the per-ADR
`> Serves:` invariant back-references and this index. The only structural
gap found is that ADR-00000010's now-reversed "docker top-level" decision
has no forward-pointer to ADR-00000011; it is listed as a follow-up for a
maintainer to close, not edited here (per the "no technical-content edits
in this slice" rule).


# ===== base issues -- 開著的（109 條；body 全文或截到 1500 字；留言各取前 400 字） =====



### #230 [OPEN] tooling: build an MCP server exposing base operations to AI agents
labels: backlog

## Context

The original direction for this issue was a static `AGENT.md` -- a markdown context file that AI agents (Claude Code, Copilot Workspace, etc.) read to learn how this repo works. After more thought, a static doc has structural limits:

- Agents have to **read** instructions, then **translate** them into bash / `gh` / `git` invocations. Every translation step is a chance to drift from the documented intent.
- Cross-repo operations (e.g. "for each of the 13 downstream repos, check `template/.version`, surface drift") require the agent to invoke `gh repo` / `curl` / `grep` itself, repeatedly. A documented procedure does not actually run.
- A static doc cannot enforce invariants (e.g. "downstream `setup.conf` overrides must be section-replace valid against the template schema"). The agent reads the rule, then either trusts itself to obey it or skips the check.

A more capable alternative: ship an **MCP (Model Context Protocol) server** that exposes `base`-level operations as agent-callable tools. The agent stops reading instructions and starts calling them.

(MCP is already in active use in this workspace -- `.mcp.json` at the docker_harness workspace root configures servers for Notion, Gmail, etc. Adding a base-specific one is a natural extension.)

## Proposal

Build an MCP server that exposes base / template operations to AI agents over MCP stdio (or SSE if a hosted variant becomes useful).

### Tools to expose (initial set)

| Tool | Purpose |
|---|---|
| `base.ver
[...截斷，原長 5988 字]

> 留言 (ycpss91255, 2026-05-13): ## Discussion notes — current direction, not final conclusion

This comment captures the architecture discussion to date. **Not a finalized plan** — directions and open questions both below. Deferring implementation; recording state so we can pick up later without re-doing the analysis.

---

## Decision summary

1. **Separate repo** `ycpss91255-docker/base-mcp` (not inside `base` repo). Reasons: 
[...截斷，原長 21383 字]

> 留言 (ycpss91255, 2026-05-15): Not picked up this sprint — this is a cross-repo project (needs a new `ycpss91255-docker/base-mcp` repo + subtree scaffolding).

Current sprint focus is base's own CI / setup track: #344 (2D dispatcher), #362 (`build.sh --apply`), env/* upgrade rollout.

Possible future triggers to revisit:

- env/* fully migrated to `multi-distro-build-worker` (after #344 lands) → agent-side demand for base opera
[...截斷，原長 1223 字]


### #327 [OPEN] dockerfile(example): apt + pip BuildKit cache mount pattern (deferred — follow-up to #317 / #325)
labels: backlog

## Status: deferred / low priority

Filing this for tracking. **Do NOT implement now** — the bigger CI levers (#317, #325) must ship and be measured first. This is a follow-up to revisit only if those leave noticeable remaining wall time.

## Proposal

Add `RUN --mount=type=cache` to apt and pip steps in `dockerfile/Dockerfile.example` so downstream Dockerfiles inherit the pattern. Mount points:

| Step | Target paths | sharing mode |
|---|---|---|
| apt (sys, devel-base) | `/var/cache/apt`, `/var/lib/apt` | `locked` |
| pip (pip/setup.sh) | `${HOME}/.cache/pip` | `locked` |

Concrete `devel-base` diff for reference:

```diff
 RUN apt-get update && \
+RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
+    --mount=type=cache,target=/var/lib/apt,sharing=locked \
+    rm -f /etc/apt/apt.conf.d/docker-clean && \
+    apt-get update && \
     apt-get install -y --no-install-recommends \
         -o Dpkg::Options::="--force-confdef" \
         -o Dpkg::Options::="--force-confold" \
         sudo git vim tmux terminator curl wget python3 python3-pip \
-        && \
-    apt-get clean && \
-    rm -rf /var/lib/apt/lists/*
+
```

Three mandatory changes per apt RUN:
1. Add two `--mount=type=cache` lines (archives + lists, both `sharing=locked`)
2. Add `rm -f /etc/apt/apt.conf.d/docker-clean` — Debian/Ubuntu base images include a config that auto-deletes `/var/cache/apt/archives/*.deb` on every apt invocation, which would defeat the cache mount
3. Remove `apt-get clean && r
[...截斷，原長 6108 字]

> 留言 (ycpss91255, 2026-05-15): Not picked up this sprint — issue body already self-tags as deferred / low priority.

Decision precondition not met: wait for #317 + #325 to ship, then measure CI wall time before evaluating whether cache mounts are worth adopting.

Possible future triggers to revisit:

- #317 + #325 shipped and remaining CI wall time is still material.
- A downstream repo appears whose Dockerfile package list chu
[...截斷，原長 855 字]

> 留言 (ycpss91255, 2026-09-03): ## The deferral condition is met

This issue defers itself explicitly: "the bigger CI levers (#317, #325) must
ship and be measured first. This is a follow-up to revisit only if those leave
noticeable remaining wall time."

**Both are closed.** #317 (buildx cache, doc-only short-circuit, GHCR rolling
tag, behavioural conditional) and #325 (pr_distros / tag_distros split).

So the question is no lo
[...截斷，原長 2082 字]


### #740 [OPEN] track: org-wide node20 -> node24 action bump (fan out base #737/#739 to downstream repos)
labels: enhancement

## Problem

GitHub deprecated the Node 20 runtime; node20-declared actions warn ("forced to
run on Node.js 24") on every run across the org. `base` cleared its own
warnings in #737 (GitHub-owned actions) + #739 (`extractions/setup-just`). The
other `ycpss91255-docker` repos still emit the warning and need the same bump.

## Confirmed version set (verify each action.yml `runs.using` == node24)

| action | -> node24 target | note |
|---|---|---|
| `actions/upload-artifact` | **@v7** | v5 is STILL node20; needs v6+ |
| `actions/download-artifact` | **@v8** | |
| `actions/cache` (incl. `/save`, `/restore`) | **@v6** | |
| `actions/checkout` | already node24 at v4+ (org uses v6) | |
| `extractions/setup-just` | **@v4** | third-party; v3 was node20 |

Node 24 is the ceiling: every latest GitHub-owned action (checkout@v7,
cache@v6, upload@v7, download@v8, setup-node@v5, even checkout@main) declares
`using: node24`. There is no node26 Actions runtime, so node24 is the target.

## What to do

For each downstream repo with workflows referencing the above at node20
versions, bump to the version set above. The bulk of repos likely only use
`actions/checkout` (already fine) + `docker/*` (not affected) + the per-repo
build action; the artifact/cache bumps mostly matter for repos that upload
artifacts or cache.

Suggested flow: a `/batch` sweep -- per repo, grep workflows for the node20
refs, bump, open a PR, auto-merge on green. Skip repos with no matching refs.

## Acceptance criteria

- 
[...截斷，原長 1927 字]


### #772 [OPEN] test(e2e): full real-flow e2e for just base upgrade (defer to v1.0.0)
labels: backlog

## What to build

Add a full real-flow e2e for `just base upgrade`: stand up the example repo with an OLDER `.base` tag, run the real `upgrade` (real `git subtree pull` to the current tag), and assert the upgrade + migration applied correctly end-to-end. This complements #769 (which covers the other commands) but is split out because it needs a from-old-tag scenario.

DEFERRED to v1.0.0 / repo stability. While the architecture, API, and config are still iterating rapidly, an older-tag-based upgrade e2e would churn constantly. The upgrade LOGIC is already covered today at integration level by `upgrade_spec` (real subtree pull + migration assertions); this issue is only about adding the full downstream-repo real-flow layer on top, once the surface stabilizes.

## Acceptance criteria

- [ ] e2e inits the example from an older base tag, runs the real `just base upgrade` to current, and asserts files/migrations updated.
- [ ] Runs on both amd64 and arm64; green.
- [ ] Does not duplicate what `upgrade_spec` already asserts -- adds the full-repo real-flow layer only.

## Blocked by

None to author, but intentionally DEFERRED to v1.0.0 (repo-surface stability). Builds naturally on the e2e command-coverage structure from #769.



### #788 [OPEN] just completion: namespace/module recipes do not space-drill (upstream-blocked, tracking)
labels: backlog, upstream

## Summary

`just` shell tab-completion does not usefully drill into namespace (module) recipes with a space. This is an upstream `just` limitation, currently in progress but blocked further upstream in `clap`. This issue parks QA items 1 and 2 with full reference data so we can re-verify and act when upstream ships a fix. Do NOT build our own completion in the meantime (it would be throwaway).

## Symptom (QA items 1 / 2)

Reproduced empirically with the repo's shipped dynamic completer (`eval "$(JUST_COMPLETE=bash just)"`) on `just 1.52.0`, in a scaffolded downstream repo, using the real bash completion function (`_clap_complete_just` with real `COMP_WORDS`/`COMP_CWORD`/`COMP_WORDBREAKS`):

- `just base <TAB>` (space) does NOT drill. It returns the full flat list: `base::completions base::default ... docker::build ... template::new` plus filesystem entries plus every `--flag`.
- `just base u<TAB>` (space, partial) returns NOTHING, because the candidates are the full paths `base::update` / `base::upgrade`, which do not start with `u`. So you cannot type-then-complete-then-run with a space.
- `just base::<TAB>` (colon) DOES drill cleanly: `base::completions base::default base::init base::update base::upgrade`.
- Top-level `just <TAB>` is noisy: flattened `namespace::recipe`, filesystem entries (including the stray empty `base/` dir, see item 4), and all of just's `--flags`.

Note: invocation works with BOTH forms (`just base update` and `just base::update` both run). Only tab
[...截斷，原長 4157 字]

> 留言 (ycpss91255, 2026-09-03): ## The premise this was parked on has moved six minor versions

This was measured against `just 1.52.0`. `dockerfile/Dockerfile.test-tools:22`
now reads:

```
ARG JUST_VERSION=1.58.0
```

The issue says the upstream work was "in progress but blocked further upstream
in `clap`". Six minor releases later, that is a question with an answer, and
the answer is obtainable by running the same reproductio
[...截斷，原長 1508 字]


### #927 [OPEN] fix(ci): the base-version monitor has never reached a single downstream repo, and nothing checks delivery
labels: bug

## The mechanism exists and has never reached a single repo

#777 / PR #778 built a pull-based upgrade monitor: `check-base-version.sh` holds
the logic, and `init.sh:437` writes
`.github/workflows/base-version-monitor.yaml` into a consumer on resync.

Checked every repo on the remote, which is authoritative:

```
realsense_ros2  ros1_bridge  claude_code  ros_distro
sick_noetic     template     omniverse_web_viewer
    -> 404 for .github/workflows/base-version-monitor.yaml, all seven
```

Zero adoption.

## Why: the delivery vehicle is the thing being monitored

```
monitor is written only by init.sh
    -> init.sh runs only during `just upgrade`
        -> upgrade is broken for every repo on v0.41.0 (#915, and #925/F1 after it)
```

So a mechanism whose purpose is "tell you a new base release is available" can
only arrive on a repo that is already able to upgrade. It cannot reach the repos
that need it, by construction.

That is a design property, not an accident of timing, and it will recur: **any
file added to a consumer via `init.sh` inherits the upgrade path's availability.**
The same is true of the `.gitignore` / `.dockerignore` canonical sync and every
future generated file.

## Nothing verifies delivery

`check-template-versions.sh` fetches `.base/.version` from each repo and stops
there. It answers "which release is this repo on", never "did the files that
release was supposed to install actually arrive". It is also run by hand during
release verification, not on a sc
[...截斷，原長 3766 字]

> 留言 (ycpss91255, 2026-08-26): Design settled 2026-08-26. This replaces both the "what is the monitor for"
question in the issue body and the mechanism #822 proposed.

## The weekly bot is removed; a release fans out

The per-repo `base-version-monitor.yaml` is dropped. base's release fans PRs out
directly instead. The bot's pull-based design was chosen to avoid a cross-org
credential; that credential now exists deliberately (b
[...截斷，原長 6071 字]

> 留言 (ycpss91255, 2026-09-04): ## Half of this landed: the delivery check exists now

`check-base-delivery.sh`, in docker_harness#304 (merged). It reports, per
repo, the release the subtree claims **and** which of the files `init.sh`
installs are actually present -- which is the "nothing checks delivery" half
of this issue.

### The first real run found what the issue predicted, plus one it did not

**The declared consumer set 
[...截斷，原長 1826 字]


### #928 [OPEN] fix(init): _create_new_repo is unreachable via bootstrap, so a new repo gets no CI, changelog or smoke scaffold
labels: bug

## The propagation mechanism exists and is unreachable

`init.sh` has `_create_new_repo` (line 332). It is what installs the things a
new repo needs and cannot get anywhere else:

- `.github/workflows/main.yaml` -- the build + release CI, wired to base's
  reusable `build-worker.yaml` / `release-worker.yaml` at the pinned tag
- `doc/changelog/CHANGELOG.md`
- `test/bats/smoke/{shared,devel-test,runtime-test}/` scaffolding

The entry condition (line 872) is:

```bash
if [[ -f Dockerfile ]]; then
  _init_existing_repo
else
  _create_new_repo "${template_version:-main}"
  _create_symlinks
fi
```

**The template ships a `Dockerfile`.** So when `bootstrap.sh` runs `init.sh` on a
freshly created repo, `Dockerfile` already exists, init takes the *existing-repo*
branch, and `_create_new_repo` never executes.

## Measured

Created a repo through the sanctioned path -- template clone shaped as
`gh repo create --template` produces, then `./bootstrap.sh` against base `main`.
Bootstrap itself succeeds (`exit=0`, `just --list` OK, zero dangling symlinks).
What the repo contains:

```
.github/workflows/base-version-monitor.yaml    HAS
.github/workflows/main.yaml                    MISSING
doc/changelog/CHANGELOG.md                     MISSING
test/bats/smoke/                               MISSING
```

`.github/` holds exactly one file. **A repo created today has no build CI and no
release workflow at all.**

Existing downstream repos have `main.yaml` because they were created under an
earlie
[...截斷，原長 4509 字]

> 留言 (ycpss91255, 2026-08-26): The template-side half is filed as ycpss91255-docker/template#13, and it is the
better place for the immediate fix.

`bootstrap.sh`'s "remove template-specific files" list
(`README.md` / `doc/` / `.github/` / `test/`) is simply **missing `Dockerfile`**.
The template's copy is redundant -- `init.sh:339` installs one from the target
base tag via `cp "${TEMPLATE_DIR}/dist/dockerfile/Dockerfile" Docke
[...截斷，原長 1719 字]

> 留言 (ycpss91255, 2026-08-26): Scope settled 2026-08-26, and it is smaller than the issue assumed.

## The self-heal half has no subject

The issue asks what happens to repos already created through the broken flow --
the ones with no `main.yaml`. Measured across every `.base` consumer:

```
REPO                     .base      main.yaml
ai_agent                 v0.41.0    present
claude_code              v0.41.0    present
code
[...截斷，原長 3362 字]

> 留言 (ycpss91255, 2026-09-02): ## Where the remaining criteria went

The PR on `fix/928-batch` does not deliver acceptance criteria 1 and 2 (the
spec pinning the discriminator). They now live in
ycpss91255-docker/template#18, and this issue stays open until that lands.

**Why they moved.** The property is "no file the template ships is a file
`init.sh` uses as its new-vs-existing discriminator". Checking it needs both
halves on
[...截斷，原長 1720 字]


### #994 [OPEN] epic(quality): adopt the four implementation thresholds, the design-principle layer and the ADR structure lint
labels: enhancement

## Context

base is the upstream that defines these properties; the config-manager design
document derives its invariants from base's template, and every downstream repo
vendors base. So a standard base adopts propagates outward, and a standard base
leaves unwritten stays unwritten everywhere.

That document's chapter 0 carries four things base does not have. This epic
adds them.

## Decisions taken

**1. All four implementation thresholds are gated. No baseline file.**

| threshold | value | base today (809 functions) |
|---|---|---|
| nesting depth | <= 3 | **44 at >= 4**, 7 at 5, 1 at 6 |
| function length | <= 50 lines | **151 over (18%)**, worst 515 |
| positional parameters | <= 5 | **7 over**, worst 31 |
| cyclomatic complexity | <= 10 | not measured (no shell tool) |

The objection considered and rejected: that splitting a 515-line function is
riskier than leaving it. **A function that is hard to split correctly is
already defective; the difficulty is the finding, not an exemption from it.**

A baseline file listing the current violations was also rejected. A baseline is
a hand-kept roster: it decays, it needs maintenance, and it converts a gate into
a record of what we have given up on. The tree is made clean instead, and the
gate lands on a clean tree.

**2. Coverage floor 80% -> 85%, tests added first.**

The order matters: the tests come first and the floor moves after, so the gate
never lands red. Note that chapter 0's 85% applies to a `core/` layer with
`io/` an
[...截斷，原長 4838 字]

> 留言 (ycpss91255, 2026-09-03): ## The violation counts in this epic's table are wrong, and phase 2 measured the real ones

The table was built with an ad-hoc counter written for the survey. Phase 2's reader
is a character-level tokenizer with quote state, heredoc state, a construct stack
and command-position tracking, and it disagrees:

| metric | this epic | measured | why they differ |
|---|---|---|---|
| nesting depth > 3 | 
[...截斷，原長 2702 字]


### #1021 [OPEN] fix(adr): nothing allocates an ADR number, so three parallel branches all took 00000030 and every gate stayed green
labels: bug

## What happened

Three branches in flight today each created `doc/adr/00000030-*.md`:

| branch | record |
|---|---|
| `docs/826-827-config-convention` | config component layout and preset selector |
| `feat/829-dep-bump-automation` | ABI-gated dependency-bump auto-release |
| `refactor/945-entrypoint-orchestrator` | base owns the container entry point |

Each read the tree, saw `00000029` as the highest, and took the next free
number. **Every one of them was right**, by the only rule there is. Nothing
allocates the number, so parallel work collides by construction rather than by
mistake.

## Why the lint does not save you

`adr_structure.sh` and the numbering check run against **one tree**. On each
branch alone the number is unique and every gate is green. The collision only
exists in the union, and the union first exists when the second PR merges --
at which point the fix is a renumber under a red required check, on a branch
whose author has moved on.

Today that cost was paid by hand: `#829` renumbered to `00000031` across 4
files, `#945` to `00000032` across **14** -- `CONTEXT.md`, `doc/adr/README.md`
(index row, the audit keep-list, two "postdate the audit" notes), the
changelog, an amended ADR's pointer, six spec files, three catalogue
documents, a lib, and a workflow. Every one of those is a place a renumber can
be done incompletely and stay green, because a stale `ADR-00000030` in prose
is not something any gate reads.

## The shape

This is the repo's recurring defe
[...截斷，原長 3691 字]

> 留言 (ycpss91255, 2026-09-05): ## It has happened again, and this time one of the colliding records is this issue's own fix

Measured just now across the unlanded worktrees:

```
base-numbers  00000034-adr-numbers-collide-and-the-repair-is-a-verb.md
base-927m     00000034-release-fanout-is-pushed-and-membership-is-scanned.md
```

`origin/main` is at 00000033. Both branches read the tree, saw 33 as the
highest, and took 34. **Bo
[...截斷，原長 1930 字]


### #1022 [OPEN] fix(tooling): the land queue is complete except for three joins, so every stale PR still needs an operator
labels: bug

## The queue exists end to end and still stops at every stale PR

Landing eleven branches today exercised the whole chain for the first time.
It is complete except for three joins, and each one turns an automatic step
back into a manual one.

```
serial-merge.sh  ->  auto-merge-on-green.sh  ->  [DIRTY]  ->  ??? 
                                                              update-stale-pr.sh
```

Observed, verbatim:

```
[serial-merge] landing PR1019 on ycpss91255-docker/base ...
PR1019: state=OPEN merge=DIRTY ci=pending
FAIL conflict (mergeStateStatus=DIRTY). Merge origin/main into the branch
(no rebase) and resolve: .claude/scripts/update-stale-pr.sh <pr> --repo <repo>,
then re-run.
[serial-merge] summary: merged=0 failed=2
```

`update-stale-pr.sh` gained exactly the resolution that case needs
(docker_harness#287, PR #297). Nothing calls it.

## Gap 1 -- `auto-merge-on-green.sh` prints the command instead of running it

On `DIRTY` it exits 1 with a suggestion. `BEHIND` it already handles itself by
calling `gh pr update-branch`, so the shape is established; `DIRTY` is the
same shape with a different repair, and the repair now exists.

Note the sibling failure this must not reintroduce: `update-stale-pr.sh` is
all-or-nothing by design and exits 2 when any hunk is not the regenerated
class. Calling it must propagate that refusal, not retry or fall through.

## Gap 2 -- base's generator does not answer `--list-outputs`

`update-stale-pr.sh` asked, correctly, and refused when n
[...截斷，原長 4507 字]

> 留言 (ycpss91255, 2026-09-04): ## Gap 3 confirmed, in the tool's own repo

`update-stale-pr.sh` was run against docker_harness#304, where the generator
**does** answer `--list-outputs` -- so gaps 1 and 2 are out of the way and
only the classification is under test. Verbatim:

```
doc/test/unit.md: owned=yes hunks=3 regenerated=1 real=2

not auto-resolvable: doc/test/unit.md has 2 conflict hunk(s) that are not count drift
```

E
[...截斷，原長 2624 字]


### #1024 [OPEN] fix(test): the undescribed ceiling is a number every branch edits, so every merge conflicts on it and neither side is right
labels: bug

## The ceiling is now the thing every branch edits

`_CATALOG_DESC_UNDESCRIBED_CEILING` in
`script/test/drivers/catalog_description.sh` is a single `readonly`, and the
policy is that it only goes down. Both are right. The consequence is that
**every branch that describes a test lowers it**, so every branch changes the
same line, and every merge conflicts on it.

Observed while landing one branch this cycle, twice in a row:

```
merge 1: ceiling 2622 -> 2617   (5 slack, lowered)
merge 2: conflict on catalog_description.sh
         ceiling 2614 (main) vs 2617 (branch)
         merged tree actually produces 2609
```

Neither side's number was right after the merge. That is the same shape
ADR-00000028 removed for the test-count totals -- "a figure about a moving
tree with no referent" -- and the same measured cost: five self-declared
totals every branch edited caused **61 conflicts in 65 merges**, which is why
they went.

The ceiling reintroduced it with a different name.

## What is different, and why it is not simply the same mistake

The ceiling is not a *statistic*. It is a **bound**, and a bound has to be
stored somewhere or it bounds nothing. #999 chose one number over a roster of
per-test exemptions deliberately, and that choice is still right: a roster
would be worse in every way this repo has already measured.

So the defect is not "there is a stored number". It is that the number is
stored in a form where two branches lowering it produce a conflict whose
correct resolut
[...截斷，原長 3485 字]


### #1030 [OPEN] fix(coverage): kcov's bash engine discards lines under bash 5.3, which blocks the Alpine 3.23 bump due 2026-11-02
labels: bug

## Deadline: 2026-11-02

Not a guess. `dockerfile/Dockerfile.test-tools` pins `ALPINE_VERSION=3.22`,
whose EOL is **2027-05-01**, and `alpine_eol_spec.bats` fails at a 180-day
lead -- so the alarm re-arms on **2026-11-02**, one day after 3.21's own EOL.

The next series is **3.23**, and 3.23 is on the far side of the bash boundary.
So the next EOL bump cannot be taken without solving this. It is not "before
3.22's EOL"; it is about two months.

## The defect, measured

kcov's bash engine defaults to the PS4/xtrace method, so the traced command's
text rides on the same line as the `kcov@FILE@LINE@` marker. To cope with
values spanning physical lines it tracks single-quote parity and **discards
every line it reads, marker included, while it believes it is mid-quote**
(`getInputType`, `src/engines/bash-engine.cc`):

```c
if (str[i] == '\\' && out == INPUT_NORMAL) i++;
else if (str[i] == '\'') out = (out == INPUT_NORMAL ? INPUT_SINGLE_QUOTE : INPUT_NORMAL);
```

A backslash escape counts only **outside** a quote. bash 5.3 emits a
newline-containing value as one ANSI-C line, `$'a\nb'`, writing an embedded
quote as `\'`; bash 5.2 emits it as several physical lines in plain `'...'`
form, writing an embedded quote as `'\''`.

Under that rule every `\'` inside an ANSI-C string flips parity a net **odd**
number of times, so even an even count leaves the line "inside a quote" and
everything after is discarded until parity happens to flip back.

| ALPINE_VERSION | bash | coverage |
|---|
[...截斷，原長 3979 字]


### #1034 [OPEN] fix(release): the completeness count shares its section boundary with the merge, so a mid-section link definition shortens the page silently
labels: bug

## The completeness count and the merge still share their section boundary

`script/release/release_notes.sh` counts the entries its sources hold and the
entries its page carries, and refuses when they disagree. That count exists to
turn "a section shape this file was not written for" into a refusal at tag push
rather than a release page nobody knows is short.

base#926 made the WITHIN-section parsing independent: `_count_entries` carries
no fence state, so a `- ` at column 0 is an entry wherever it stands, and a
lead the count calls entry-carrying is never a lead the merge drops. That
closed the unclosed-fence case.

What both still share is where a section ENDS. `_ends_section` ends a section
body at any column-0 link definition, and both readers take their spans from
`_section_body`, so content after a mid-section reference definition is
subtracted from BOTH sides -- and the counts agree while the page is short.

## Reproduced

`v0.9.md`:

```markdown
## [v0.9.0] - 2026-01-01

### Added
- the entry above the link definition (#30, PR #31)

[the-adr]: https://example.invalid/adr

### Fixed
- the entry below the link definition (#32, PR #33)
```

```
$ script/release/release_notes.sh v0.9.0 <root>
### Added
- the entry above the link definition (#30, PR #31)
exit=0
```

One entry in, one entry out, no refusal. The `### Fixed` entry is gone from the
release page and nothing says so.

## Latent, not live -- and that is the reason to fix it now rather than later

Checked all 44 
[...截斷，原長 2920 字]


### #1035 [OPEN] docs: the README ADR range is eight records stale and the PRD promises a retirement that did not happen
labels: documentation

## Two assertions in the docs that nothing re-derives, both now false

Both are the shape ADR-00000028 exists to end -- a figure or a promise about a
moving tree, with no referent -- and both are in the files that describe that
rule.

### 1. README's ADR range is eight records stale and hides a gap

`README.md:1845`, in the directory tree:

```
│   ├── adr/                            # Architecture Decision Records (00000001 … 00000024)
```

Measured on `origin/main`:

```
$ git ls-tree --name-only origin/main doc/adr/ | grep -cE '^doc/adr/[0-9]{8}'
31
$ ... | grep -oE '[0-9]{8}' | sort -u | tail -1
00000032
```

**31 records, highest number 00000032, and 00000009 does not exist.** So the
line is wrong twice: the upper bound is eight behind, and writing it as the
continuous range `00000001 … 00000024` asserts there is no gap when there is
one.

Nothing recomputes it. `derived_figures.sh` enforces exactly this rule for the
constants it covers, and a comment inside a README directory tree is not one of
them.

The three localized READMEs carry their own copy of the tree, so whatever is
done here is done four times or derived once.

### 2. PRD promises a retirement that did not happen

`doc/PRD.md:349`:

> Invariant 2's guard list names the doc-count drift gate, which
> ADR-00000028 removes along with the figures it guarded; **that entry drops
> from invariant 2 when that mechanism lands.**

The mechanism landed -- #999 / PR #1017 made `doc/test/*.md` generated from
`# why:` mark
[...截斷，原長 3944 字]


### #1039 [OPEN] fix(changelog): a branch open across an RC cut files its entry under the release it did not ship in
labels: bug

## A branch open across an RC cut files its entry under the RC it did not ship in

Observed on `origin/main` right now:

```
$ grep -n 'record no suite total\|^## \[' doc/changelog/CHANGELOG.md | head -3
155:## [Unreleased]
200:## [v0.43.0-rc1] - 2026-09-04
203:- **`doc/test/TEST.md` and `doc/test/unit.md` record no suite total any more
```

`v0.43.0-rc1` was tagged at `26abad24`. #978 merged as PR #1038 **after** that
tag. Its entry is nevertheless inside the `[v0.43.0-rc1]` section, so the
changelog now says rc1 shipped something rc1 does not contain.

## Why it happens, and why it will keep happening

`release-bump.sh` promotes the live section by **renaming the heading**: the
existing `## [Unreleased]` becomes `## [vX.Y.Z] - <date>` and a fresh empty
`## [Unreleased]` is inserted above it.

A branch opened before the cut wrote its entry under a heading that said
`[Unreleased]` at the time. After the cut, that same block of lines is the RC
section. git merges the entry into the block it was written against -- which is
now labelled with a release the branch never shipped in. **Nothing conflicts**,
because the branch added lines and main renamed a heading well above them.

So the failure is silent and it fires for **every** branch open across a cut.
The RC window is exactly when several branches are in flight, which is when it
fires most.

## It has already been paid for once, by hand

PR #1037's branch hit the same thing and fixed it for itself -- commit
`001ac873`, "fix(ch
[...截斷，原長 3206 字]


### #1041 [OPEN] test(upgrade): nothing drives tag N to tag N+1, and the window goes vacuous when v0.43.0 ships
labels: bug

## The cross-version upgrade test is about to stop testing anything

`test/bats/integration/prev_release_upgrade_spec.bats` exists, runs in the
required-gated `bats-integration` job, and passed on the last run on main
(run 33864736774, `ok 115/116/117`, `1..163`). This is not "there is no test".

It is two narrower problems, and the second has a date on it.

### 1. Nothing exercises a tag against the NEXT tag

The design is "the last two release tags, each driving the WORKING TREE",
never "tag N against tag N+1". Resolved by running the real resolver rather
than reading the comment:

```
$ bash -c 'source script/test/prepare-prev-release.sh >/dev/null 2>&1; _window_tags'
v0.42.0
v0.41.0
```

The spec rewrites the target's `.version` to a synthetic `v99.0.0`, so the two
pairs actually exercised are `v0.42.0 -> working tree` and
`v0.41.0 -> working tree`. The v0.42→v0.43 path is covered only as an accident
of where `main` happens to be standing while v0.43.0 is unreleased. After the
tag it is covered by nothing.

`test/bats/integration/upgrade_spec.bats` does not fill the gap: its synthetic
remote ships the CURRENT `upgrade.sh` at both `v0.9.5` and `v0.9.7`
(spec lines 60-72), so the version numbers are labels on identical code.

### 2. The window goes vacuous the moment v0.43.0 ships

Measured, not inferred:

```
$ git show v0.41.0:upgrade.sh | grep -c apply_migrations
0
$ git show v0.42.0:dist/script/base/upgrade.sh | grep -c apply_migrations
1
$ grep -c apply_migrations dist
[...截斷，原長 3986 字]

> 留言 (ycpss91255, 2026-09-05): ## Measured: this is worse than "goes vacuous". It goes BLIND, and it also lies.

The vacuousness above was reasoned from reading the drivers. It has now been
run, and the result is stronger than the prediction.

Method: planted a synthetic `refs/tags/v0.43.0` at HEAD in a throwaway clone,
which makes `prepare-prev-release.sh` resolve the window to `{v0.43.0,
v0.42.0}` (confirmed in `.prev-release
[...截斷，原長 2955 字]

> 留言 (ycpss91255, 2026-09-05): ## Decision: the window becomes "floor-onward", not a bigger N

Settled. The fix is not to widen `PREV_RELEASE_WINDOW` from 2 to some larger
constant -- that is the same shape with a different number, and the shape is
what is wrong. A compatibility obligation is permanent; a sliding window
expires.

**The set becomes: every release from the support floor onward.**

The support floor is **v0.43.0**
[...截斷，原長 2679 字]


### #1042 [OPEN] test(just): 21 of 43 recipes are driven by no test, and nothing enforces the bar
labels: bug

## 21 of 43 `just` recipes are not driven by any test

`just` is this repo's only control surface (ADR-00000011), and complete recipe
coverage has been a stated bar. Measured against `just --summary` per module
rather than by grepping, so aliases and `mod?` nesting are handled the way
`just` handles them:

- **43 recipes** across 8 live justfiles
- **22** are driven by something that actually runs them
- **21** are not, and **13 of those have no test of any kind** — not even a
  grep of the recipe body

## The gap is not spread evenly, and that is the finding

Every **consumer-facing** recipe is executed for real: docker / base /
template / skel, **21 of 21**. The uncovered set is almost exactly base's own
self-development surface:

```
root::    default
test::    default, lint, coverage, coverage-path, metrics, system, smoke,
          clean, sync-docs, sync-docs-check, resolve-docs, sync-readme,
          sync-readme-check
release:: default, coverage-badge
watch::   default, pins, value, bump, uncovered
```

No test of any kind: `root::default`, `test::{metrics, clean, sync-docs,
sync-docs-check, resolve-docs, sync-readme, sync-readme-check}`,
`watch::{default, pins, value, bump, uncovered}`.

The whole `watch` namespace — five recipes, added 2026-09-04 with #987 — has
nothing. And the scheduled workflow that is meant to make "what CI runs is what
a maintainer runs by hand" true **bypasses the recipes and calls the scripts
directly**, so even that is not incidental coverage
[...截斷，原長 3738 字]


### #1043 [OPEN] test(coverage): 84.12% and falling, 86 lines short of the 85 floor #994 phase 4 wants
labels: enhancement

## 84.12%, and the number is falling on its own

Measured from the last CI run on main (run 33864736774, sha 7b4b7ebd), and
reproduced locally by downloading that run's eight shard artifacts and
re-running the repo's own gate over them — byte for byte:

```
coverage_gate: merged line rate 84.12%  (8224/9776 lines), floor 80% -> PASS
```

The **84.6%** on `doc/badge/coverage.svg` is stale and was never the CI figure.
The rc1 tag's own run measured **84.47% (8165/9666)**.

### The trend is the part to act on

```
v0.43.0-rc1  (2026-09-04 08:11)   84.47%   8165/9666
main         (2026-09-04 10:45)   84.12%   8224/9776
```

In one day the denominator grew **110** lines while covered grew **59**. The
rate fell 0.35 points and **nobody removed a test**. New code is landing below
the current rate, so the debt grows without anyone doing anything wrong.

### Distance to 85 — in lines, because a percentage is not actionable

```
$ awk 'BEGIN{v=9776;c=8224;need=int(v*0.85);if(need<v*0.85)need++;
             printf "need=%d delta=%d\n",need,need-c}'
need=8310 delta=86
```

**86 additional covered lines**, and the target moves: at rc1's 9666-line
denominator the same gap was 52 lines. Four days of ordinary churn added 34
lines to the debt.

### Where the uncovered lines are — 1552 across 68 files

Decomposed from the gate's own union + path-alias canonicalisation, with the
per-file numbers verified to sum back to `uncovered=1552 covered=8224
valid=9776 rate=84.12`, so this is the same me
[...截斷，原長 3634 字]


### #1046 [OPEN] track(test): decide the per-stage smoke split now that every repo is on the layout
labels: enhancement

## Context

#1044 migrated every downstream repo's smoke tree from the flat `test/smoke/`
onto the per-stage `test/bats/smoke/` layout. That migration is deliberately
mechanical: it puts **every** spec in `shared/`, because `shared/` runs on
every `-test` stage and so does the flat tree it replaced. Nothing any repo
tests changed.

What it could not do is decide which specs belong to one stage rather than
all of them. That is a per-repo judgement about what each spec asserts, and
it is the reason the split exists.

## Problem

A spec in `shared/` runs on every `-test` stage the repo has. Today most
repos have only `devel-test`, so a devel-specific assertion sitting in
`shared/` costs nothing. The moment a repo enables the opt-in `runtime-test`
stage, every one of those assertions runs against a runtime image that was
never built to satisfy them.

The repos where this is worth looking at, by spec count:

| repo | specs now in `shared/` |
|---|---|
| `jetson_sdk_manager` | 11 |
| `realsense_ros1` | 6 |
| `realsense_ros2` | 6 |
| `ai_agent`, `claude_code`, `codex_cli`, `gemini_cli` | 1 each |
| `ros1_bridge`, `ros2_distro`, `ros_distro` | 1 each |
| `sick_humble`, `sick_noetic` | 1 each |
| `urg_node_humble`, `urg_node_noetic` | 1 each |
| `template` | 1 |

`isaac` and `omniverse_web_viewer` were already on the per-stage layout and
are not part of this.

## Proposal

Per repo, read each spec in `test/bats/smoke/shared/` and ask what it
asserts about:

- the universal surface -- 
[...截斷，原長 2653 字]


### #1047 [OPEN] track(release): v0.42.0 is not upgradable-to, and rc1 predates main
labels: enhancement

## Context

A two-stage upgrade verification was run on 2026-09-05: bootstrap a repo
fresh from a tag, upgrade another from `v0.41.0` to the same tag, compare the
two. It turned up two things that anyone cutting `v0.43.0` or planning a
downstream fanout needs before they act. Everything below was **reproduced by
running it**, not inferred from reading; the commands are included so it can
be re-checked rather than taken on trust.

This issue is a handoff. It asks for no code change of its own.

## Problem

### 1. `v0.42.0` is not a viable upgrade target, and it is the current `latest`

Upgrading a `v0.41.0` consumer to `v0.42.0` does not fail cleanly -- it
bricks the repo.

`v0.41.0`'s `upgrade.sh:303` runs `"./${TEMPLATE_REL}/init.sh"`. `v0.42.0`
relocated `init.sh` to `dist/script/base/`, leaving that path empty. The
upgrade dies at Step 3/5 with exit 127 **after Step 1 has already committed
the subtree pull**, so the repo is left:

- `.base/.version` claiming `v0.42.0` (it looks upgraded)
- 9 dangling symlinks: `justfile`, `.hadolint.yaml`, and all 7 wrappers
- `just --list` failing outright -- so the user cannot even re-run
  `just upgrade` to recover
- `main.yaml` still on `@v0.41.0`, no `base-version-monitor.yaml`

Escape hatch, verified to fully recover the repo:
`./.base/dist/script/base/init.sh`.

This was already found and fixed -- #915 / PR #919 added the root
compatibility forwarder, and its commit message describes this exact failure.
**That fix merged after `v0.4
[...截斷，原長 5068 字]

> 留言 (ycpss91255, 2026-09-05): ## Clarification: "15 repos on the old layout" is not the fanout scope

The table above is accurate about *state* -- 15 repos do carry the
pre-`v0.42.0` smoke layout. It is easy to read it as the size of a fanout,
and that would be wrong.

`docker_harness`'s `.claude/scripts/lib/roster.tsv` scopes the `.base` fanout
per repo, and `batch-base-upgrade.sh --list-repos` resolves it to **three**:

```

[...截斷，原長 1261 字]

> 留言 (ycpss91255, 2026-09-05): ## The seventeen consumer issues are open, ahead of the tag

Filed now rather than at tag time, so the list cannot be lost between the
decision and the release. Each says explicitly that it is acted on when v0.43.0
is tagged.

Versions read from each repo's `.base/.version` today, not from an earlier
note:

| version | repo | issue |
|---|---|---|
| v0.41.0 | **template** | ycpss91255-docker/templ
[...截斷，原長 2412 字]


### #1048 [OPEN] test(upgrade): the release that bricked every consumer was green because the upgrade fixture is copied from the candidate tree
labels: bug

## v0.42.0 bricked every released consumer and 36 of 36 CI jobs were green

The shallow answer is that `prev_release_upgrade_spec.bats` did not exist yet
-- true, and it landed 3h07m AFTER the tag, in the PR that fixed the bug
(3a36f8b4 vs db16b472). That answer does not prevent the next one.

The real answer: **an end-to-end upgrade test DID exist, DID run on the tag,
and was structurally incapable of failing for this reason.**

`git show v0.42.0:test/bats/integration/upgrade_spec.bats` builds a fake
template remote with two tags and calls the older one "the previous release".
Every byte of that older side is copied from the CANDIDATE tree:

```
line 51:  cp "${UPGRADE}" "${TMPL_WORK}/dist/script/base/upgrade.sh"   # ${UPGRADE}=/source/dist/...
line 55:  cp /source/dist/script/base/upstream.sh ...
line 60:  cp /source/dist/script/docker/lib/* ...
line 49:  printf '#!/usr/bin/env bash\nexit 0\n' > "${TMPL_WORK}/dist/script/base/init.sh"
```

The "old release" is the NEW driver, and the `init.sh` it calls is an `exit 0`
stub **written at the new path**. And the PR that moved `init.sh` moved the
fixture with it, in the same commit:

```
$ git log -S'dist/script/base/init.sh' -- test/bats/integration/upgrade_spec.bats
f3ffd106
ded9f90d
```

So the test asserted the new layout against itself. Seventeen `@test`s driving
upgrade end to end, and not one of them could notice that the path a released
consumer invokes had stopped existing.

**The class:** every test in this suite runs 
[...截斷，原長 4817 字]

> 留言 (ycpss91255, 2026-09-05): ## Decision: the parse-the-released-driver lint is DROPPED. Here is what replaces it.

The issue above recommends extracting the invoked-path set from every released
`upgrade.sh` and failing when the candidate tree does not provide one. That
recommendation is withdrawn, on two principles that it violates:

1. **It requires human maintenance.** "Extract the paths" means a set of
   syntax rules som
[...截斷，原長 3473 字]


### #1049 [OPEN] fix(upgrade): a consumer older than v0.41.0 can reach no current release, and the refusal does not say so
labels: bug

## jetson_sdk_manager is on v0.39.0 and can reach neither v0.42.0 nor v0.43.0

Measured by running the REAL released `upgrade.sh` of v0.40.0, v0.39.0 and
v0.38.0 against the v0.43.0-rc1 tree in a throwaway harness -- not by reading
them. All three refuse:

```
Step 2/5: verify .base/ subtree integrity
ERROR: post-pull integrity check failed -- '.base/script/docker/wrapper/setup.sh' missing.
ERROR: Likely cause: git-subtree fast-forwarded destructively.
INFO : Rolling back to <sha> ...
ERROR: upgrade aborted; repo restored to pre-upgrade state
```

**This is the good failure mode.** Their own Step 2 marker check
(`v0.40.0:upgrade.sh` L87-91) fires and rolls back cleanly, so the repo is
intact -- refused, not bricked. That is the difference between these and
v0.42.0, which has no such refusal on the path that breaks.

But the consequence is that one repo is pinned:

| repo | `.base/.version` | to v0.42.0 | to v0.43.0 |
|---|---|---|---|
| `jetson_sdk_manager` | **v0.39.0** | bricks | refuses at Step 2 |
| `isaac` | v0.42.0 | -- | ok |
| 15 repos | v0.41.0 | bricks | ok (proven by running) |

(Org-wide `.base/.version` survey over all 24 repos; the 15 at v0.41.0 are
ai_agent, template, codex_cli, gemini_cli, ros_distro, claude_code,
ros1_bridge, ros2_distro, sick_humble, sick_noetic, realsense_ros1,
realsense_ros2, urg_node_humble, urg_node_noetic, omniverse_web_viewer.)

## The route out

`jetson_sdk_manager` must step through **v0.41.0** first, then to the next
stable. Two hop
[...截斷，原長 2744 字]


### #1051 [OPEN] fix(compose): baked literals break the ADR-22 per-instance contract
labels: bug

## Context

`multi_run` (issue #25) is being redesigned. Its purpose is not "launch several
containers" but composition: base downstream repos are modules, and multi_run
instantiates them -- including **several instances of the SAME repo at once**
(e.g. three lidar units, each an instance of the lidar repo), then wires them
together. So scenario (1) of ADR-00000022's Context -- "one repo / many
instances" -- is the primary case, not an edge case.

ADR-00000022 s3 states the rule that scenario depends on:

> The audit is a **starting point, not an exhaustive allowlist** -- ANY field
> that can collide across instances must have an override path.

and s5 states the forward invariant:

> base's compose emission never emits a hardcoded per-instance literal over the
> interpolation-channel field set.

An audit of `dist/script/docker/lib/compose_emit.sh` at v0.43.0-rc1 against that
rule found the invariant is not currently held, and that
`overlay_guard_spec.bats` structurally cannot observe the violations.

This issue reports the gap only. **The mechanism for closing it is deliberately
not proposed here** -- how base wants to widen (or re-scope) the contract is
base's decision.

## Problem

### A. Colliding fields with NO override path at all

| Field | Emitter | Emitted form |
|---|---|---|
| `[logging] local_path` host mount | `_logging_svc_local_path_mount` `compose_emit.sh:541-578`; emitted `:1302`, `:701-702`, `:961` | `_llp_out="${_raw}:/var/log/${_name}"`, `_raw` forced abso
[...截斷，原長 6467 字]

> 留言 (ycpss91255, 2026-09-06): ## Decision

Both A and B are guaranteed, not documented away.

The rule base is adopting is that anything decided at build time or before the
container starts must be reachable by the caller. `[logging] local_path`,
`devices:`, the `config/<c>` binds, `[volumes] mount_N` for N>1, and the
stage-level overrides of `network_mode` / `privileged` / `ipc` / `pid` are all
pre-start, so all of them get a
[...截斷，原長 1363 字]


### #1052 [OPEN] track(contract): modules have no declared interface for topic namespacing
labels: enhancement

## Context

`multi_run` (issue #25) is being redesigned around composition: base downstream
repos are modules, and multi_run instantiates them -- including several
instances of the SAME repo at once (three lidar units = three instances of the
lidar repo) -- and then wires them together into a pipeline
(lidar x N -> preprocessing -> postprocessing). An assembly is itself intended
to be composable again.

The rebuild has deliberately scoped the wiring OUT of this round: multi_run
will first do instantiation, per-instance isolation and unified configuration,
using the channels ADR-00000022 already defines. Wiring waits.

This issue exists so base knows the gap is there when it becomes relevant. It
is not a request to act now.

## Problem

base's contract covers **how a container runs** -- GPU, mounts, network mode,
privileged, ports. Nothing in it describes **what a module offers to other
modules, or how that surface can be renamed per instance.**

Concretely, N instances of the same ROS repo all publish to the same topic
names, and there is no configuration entry point to separate them. A grep
across the ROS downstream checkouts (`urg_node_humble`, `urg_node_noetic`,
`sick_humble`, `realsense_ros2`) for `ROS_NAMESPACE`, `remap`, `__ns` or any
topic-related key found nothing. Every hit was either a container-level
namespace (IPC / PID, from `setup_tui.sh`) or the generic
`ROS_DOMAIN_ID=7` example in the env-var prompt text.

`ROS_DOMAIN_ID` is the only ROS-aware knob that exists
[...截斷，原長 3149 字]


### #1054 [OPEN] track(upgrade): three defects from one unwritten compatibility contract
labels: enhancement

## Context

A two-stage upgrade verification on 2026-09-05 -- bootstrap a repo fresh from
a tag, upgrade another from `v0.41.0` to the same tag, compare the two --
turned up three defects in a row. They are not three unrelated bugs; they are
three symptoms of one thing base has never written down.

Reproduced by running, not inferred. Details and commands are in the linked
issues.

1. **`v0.42.0` cannot be upgraded to from `v0.41.0`.** It relocated
   `init.sh`, the released `upgrade.sh` names the old path, and the upgrade
   dies *after* the subtree pull commits -- leaving `.base/.version` claiming
   the new release while `justfile` and all seven wrappers dangle and `just`
   itself stops working. Already fixed by #915 / PR #919's forwarder, which
   landed after `v0.42.0` shipped. Reported separately in #1047.

2. **An upgraded repo's own smoke tree never migrated**, so a repo upgraded
   from `v0.41.0` and a repo bootstrapped fresh at the same tag produced
   different trees. #1044 / PR #1045, merged.

3. **The fix for (2) added a mutation that the resync's rollback does not
   protect**, because `_init_protected_paths` is a hand-maintained list and
   the spec named `covers every root the resync writes into` only asserts six
   hardcoded lines. Found within a day of (2) landing.

## Problem

Every one of those is the same shape: **a change moved something, and nothing
was in a position to notice.** (1) moved a path a released caller names. (2)
moved a tree the existing-r
[...截斷，原長 3813 字]

> 留言 (ycpss91255, 2026-09-05): ## Sub-issues

- [ ] #1055 -- declare what a Y may change and how far back repair reaches
      (the contract; sizes everything else)
- [ ] #1057 -- assert an upgraded repo equals a freshly bootstrapped one
      (the gate; useful whichever way #1055 goes)

Related, opened from the same session and tracked separately:

- #1047 -- `v0.42.0` is not upgradable-to, and `rc1` predates `main`. The
  rel
[...截斷，原長 561 字]

> 留言 (ycpss91255, 2026-09-09): ## Sub-issue status

- [x] #1055 -- CLOSED. The support floor is `v0.43.0`; pre-floor consumers are
      re-established rather than upgraded. Its one unsettled axis moved to
      #1189.
- [ ] #1057 -- still open, and unaffected by the floor decision: it asserts
      that an upgraded repo equals a freshly bootstrapped one, which matters
      forward from the floor as much as behind it.

Spun ou
[...截斷，原長 876 字]


### #1056 [OPEN] track(contract): per-instance override for all config sections
labels: enhancement

## Context

`multi_run` (issue #25) is being redesigned as the compose layer described in
#600: base operates a single instance, multi_run owns all multi-instance
orchestration including per-instance naming, ports and isolation.

Working through what that actually requires, the consuming side reached a
position worth putting to base directly:

> Everything a repo can configure should be adjustable per instance, so the
> orchestration layer does not accumulate a list of things it cannot do.

This issue asks base to **evaluate that position across the whole
`setup.conf` surface** and state the boundary explicitly. It is not a request
to implement a particular mechanism.

## Problem

`dist/.setup.conf` has 15 sections: `[project]` `[image]` `[build]`
`[deploy]` `[lifecycle]` `[gui]` `[network]` `[security]` `[resources]`
`[environment]` `[tmpfs]` `[devices]` `[volumes]` `[additional_contexts]`
`[logging]`.

Auditing them against ADR-00000022's overlay channels, roughly four are
per-instance overridable today:

| Overridable now | Channel |
|---|---|
| project `name:` | `${PROJECT_NAME}` (v0.43+ emission) / compose `-p` |
| `[volumes] mount_1` | `${WS_PATH}` |
| `[network] mode`, `ports` | `${NETWORK_MODE}`, `${PORT_<n>:-default}` |
| `[security]` privileged / ipc / pid (devel service only) | same-named interpolations |
| `[environment]` workload env | `.env.local` via `env_file:` |

The remainder splits three ways, and only the third needs a decision:

**1. Correctly shared, sho
[...截斷，原長 4377 字]

> 留言 (ycpss91255, 2026-09-05): ## The consumer requirement, stated plainly

The position on the `multi_run` side has firmed up since this issue was opened,
and it is worth stating because it changes how the answer here should be judged:

> `multi_run` needs to be able to adjust everything a repo can configure.
> Without that it has no reason to exist — a tool that starts N stacks but
> cannot vary them is barely more than a she
[...截斷，原長 3602 字]

> 留言 (ycpss91255, 2026-09-06): ## Decision

The boundary is not a per-section table. It is a rule:

> **Anything base decides at build time or before the container starts must be
> reachable by the caller. Only what is internal to a running container is
> outside the contract.**

base is a building block and the orchestration layer is the assembler, so a
value the assembler cannot reach is a defect in the block, not a documente
[...截斷，原長 1596 字]


### #1057 [OPEN] track(test): assert an upgraded repo equals a freshly bootstrapped one
labels: enhancement

Part of #1054.

## Context

`prev_release_upgrade_spec.bats` already drives a **released** `upgrade.sh`
against a downstream-shaped consumer and asserts exit code, `.version`,
dangling symlinks (path-agnostically), `just --list`, and that every
Dockerfile COPY source resolves. Two arms, newest release and N-1, per PR.
It is thorough, and it exists because of the `v0.42.0` incident.

It answers **"does the upgraded repo work"**.

Nothing answers **"is the upgraded repo what a fresh one would be"**. #1044
lived exactly in that gap: every assertion above passed on a repo whose smoke
tree was still in the pre-`v0.42.0` layout, because a flat `test/smoke/` is
perfectly functional -- it is just not what `init.sh` produces from scratch,
so the repo silently never gained the per-stage split.

`smoke_layout_convergence_spec.bats` (PR #1045) is the only fresh-vs-migrated
comparison in the tree, and it is narrow on purpose: it compares `init.sh`'s
two internal paths, over the smoke subtree only, and never invokes
`upgrade.sh`.

## Problem

The composition -- **a consumer upgraded from vN-1 by its own released
`upgrade.sh` is indistinguishable from one bootstrapped at vN** -- is
asserted nowhere.

That matters beyond the smoke tree because `upgrade.sh` does things `init.sh`
does not, so an `init.sh`-level comparison structurally cannot see them:

- Step 4 rewrites `main.yaml`'s `@tag` references; `init.sh` deliberately
  never rewrites an existing repo's `main.yaml`
- `_migrate_legacy_se
[...截斷，原長 5078 字]


### #1061 [OPEN] test(isolation): the suite's coverage depends on the order its specs run in, and the 1-slice control proves it is not the merge
labels: bug

## The suite's coverage depends on the order its specs run in

Four whole-suite runs of one tree (`bea63246`, 32-core host, one at a time,
`scope=full` on every one):

| run | wall | instrumented | covered |
|---|---|---|---|
| serial (`_run_coverage`) | 2052s | 9667 | **8179** |
| parallel, 32 slices | 299s | 9667 | **8152** |
| parallel, 32 slices (repeat) | 294s | 9667 | 8152 |
| parallel, **1 slice** | 2022s | 9667 | **8167** |

Instrumented sets: symmetric difference **0** across all four -- the same lines
are considered measurable. The covered sets are **strictly nested**:
32-slice (8152) subset 1-slice (8167) subset serial (8179).

27 lines, 0.33%, in `help.sh` (12), `config_summary.sh` (14), `bootstrap.sh`
(1) -- almost all arms of localised `case` lookup tables.

## The 1-slice run is the control, and it acquits the merge

At one slice there is no partition: the whole suite runs in one bats process,
exactly as the serial run does. It still loses **12** of the serial run's lines
and gains none. **A merge cannot lose what was never split.**

So the only remaining difference between those two runs is how bats is invoked:

- serial hands bats the pool **directories** with `--recursive`
- the parallel runner hands it a **file list in LPT order**

Same specs, same count, different order. Splitting 32 ways loses 15 more on top.

**Conclusion: some spec's coverage depends on what ran before it in the same
bats process.** That is a property of the suite, not of any coverage m
[...截斷，原長 3423 字]


### #1062 [OPEN] track(schema): emitter decisions that have no config key
labels: enhancement

## Context

`multi_run` is being rebuilt as the compose layer #600 describes, and the
consuming side arrived at a principle worth putting to base:

> Anything the emitter decides should be visible and controllable in
> `setup.conf`, not fixed in the emitter. If a field is not explicitly
> represented in the config, it should be added and documented.

The concrete case that surfaced it is `container_name`, and it is a good
illustration because base already made the right call by accident of design
rather than by exposing a knob.

**[measured, Compose v5.5.0]** For a compose file that bakes a literal
`container_name`, a second instance under a different project fails and leaves
debris:

    docker compose -p gen_a ... up -d     -> my-fixed-web + gen_a-worker-1 running
    docker compose -p gen_b ... up -d     -> gen_b-worker-1 created, then
       Conflict. The container name "/my-fixed-web" is already in use ... (rc=1)

leaving `gen_b-worker-1` stranded in `created`. `-p` cannot override it, because
a container name is namespaced by the daemon rather than by the project — which
is exactly the reasoning `compose_emit.sh:14-27` already records.

Whereas an **interpolated** `container_name` is fully controllable:

    (unset)                     -> container_name: my-web     image: fallback:latest
    CONTAINER_NAME=web_alpha    -> container_name: web_alpha   image: myimg:v1

and two such instances start and run side by side, rc=0.

base's current dev-stack answer is to emit no `
[...截斷，原長 4563 字]

> 留言 (ycpss91255, 2026-09-06): ## Decision

Every one of them becomes reachable by the caller. The principle this issue
states is adopted as written:

> Anything the emitter decides should be visible and controllable in
> `setup.conf`, not fixed in the emitter.

So `container_name`, `hostname`, `profiles:`, `stdin_open` / `tty`, `env_file:`
and the `[tmpfs]` section without schema keys are all in scope, along with the
adjacent 
[...截斷，原長 1791 字]


### #1064 [OPEN] track(deploy): a co-locatable field-deploy bundle mode
labels: enhancement

## Context

`multi_run` is being rebuilt as the compose layer #600 describes. Its deploy
phase is meant to align with base's `just docker setup deploy` rather than
invent a second bundle format, and the natural shape is **a bundle of bundles**:
each downstream repo produces its own base deploy bundle, and `multi_run` wraps N
of them with a top-level launcher.

That composition would let base keep solving the two problems `multi_run` cannot
solve on its own:

- **Images.** `multi_run` cannot pack N repos' images itself, but each base
  bundle already carries its own `image.tar.xz`.
- **Secrets.** Naively resolving a compose file bakes secrets in.
  **[measured]** `docker compose config` inlines `env_file:` contents into
  `environment:` — a repo whose env file holds a token would have that token
  written into the artifact. base's bundle deliberately avoids this by keeping
  the `env_file:` indirection pointing at bundle-local `.env` / `.env.local`
  (`deploy.sh` comment: "costs the bundle none of its self-containment"), which
  is also what keeps the field operator able to override.

Both are already solved correctly in base. Reimplementing either in `multi_run`
would be strictly worse.

## Problem

The bundle is deliberately single-device, so N of them cannot be stacked when any
two come from the same repo.

`_generate_resolved_compose` (`dist/script/docker/lib/deploy.sh`) emits:

    # Fully resolved (no variable interpolation, no setup.conf/.env dep);
    name: <container>
[...截斷，原長 4994 字]

> 留言 (ycpss91255, 2026-09-05): ## Sharpening the ask: not "make it floating", but "let the fixed name be supplied"

The original text framed this as wanting the bundle to behave more like the dev
stack. That framing was imprecise, and the distinction is worth stating properly
because it is one base already implements correctly:

| | base today | |
|---|---|---|
| dev stack | emits no `container_name`; project name derived | **f
[...截斷，原長 1932 字]

> 留言 (ycpss91255, 2026-09-06): ## Decision

Yes. The bundle gets a co-locatable mode.

Two bundles generated from the same repo must be able to run on one host, which
means the project name and the container name stop being one baked string
(`deploy.sh:1166`, emitted at `:553` and `:557`). Adding the parameter is the
whole change -- the image tarball, the `.env` / `.env.local` layering, the
launcher and the README are already w
[...截斷，原長 873 字]


### #1065 [OPEN] docs(prd): base's layout is recorded nowhere and checked by nothing, and an enumerated record would collide every time a directory is added
labels: enhancement

## base's own directory layout is recorded nowhere and checked by nothing

Measured:

- `doc/PRD.md` has 11 invariants; none is about where things live. The nearest,
  invariant 8, covers `config/<component>/` only.
- ADR-00000006 freezes `.base/` interior paths -- the downstream protocol, not
  base's own tree.
- `CONTEXT.md` has Domain / Schema / Logging / Architecture-seams sections and
  **no directory section**.
- `check-claude-md-tree.sh` exists in docker_harness and audits a markdown tree
  listing against the filesystem. `grep -rn 'tree-check\|check-claude-md-tree'`
  over base's `script/` and `.github/` returns **nothing** -- base does not use
  it.

So "why is `compose.yaml` at the root", "why does `dist/test/bats/smoke/` have
its own directory", "what may go in `script/` versus `dist/script/`" have no
answer to point at. Two of those were asked on 2026-09-05; answering them took
an audit each. ADR-00000035 records those two answers; it does not establish
the rule.

## The constraint that shapes the fix

The repo is in rapid iteration. A layout record that **enumerates** directories
costs an edit every time one is added -- and worse, it collides. Measured today
while merging `fix/1021-1024-shared-numbers`: `CONTEXT.md` conflicted because it
lists `script/`'s children by name and two branches each added one.

```
ours   : `script/test`, `script/release`, `script/adr` (real directories, no
theirs : `script/test`, `script/release`, `script/watch` (real directories, no

[...截斷，原長 4101 字]


### #1069 [OPEN] perf(ci): the coverage matrix uses eight of twenty slots for seven of the run's ten minutes
labels: enhancement

## The run uses eight of its twenty slots for seven of its ten minutes

Measured on run 33965580692 (main, 46 jobs, all successful). Concurrency
sampled every 60s from each job's own start / completion timestamps:

| t+ | jobs running |
|---|---|
| 0:00 | 1 (actionlint) |
| 1:00 | 18 |
| 2:00 | 12 |
| 3:00 | 8 |
| 4:00 | 8 |
| 5:00 | 8 |
| 6:00 | 8 |
| 7:00 | 8 |
| 8:00 | 7 |
| 9:00 | 5 |
| 10:00 | 1 |

Peak concurrency was 19. Two coverage shards (4/8 and 5/8) started 36s and 40s
after their six siblings, which is what hitting the cap looks like from the
inside.

After minute three the only thing still running is the eight-shard coverage
matrix, and the whole run's wall clock is the slowest shard in it. Twelve
slots sit idle for seven minutes.

## Two things are set independently and they fight

**The shard count is 8 and the code will not let it past 12.**
`compute-shards` in `.github/workflows/self-test.yaml` reads `vars.CI_SHARDS`
(unset today, so the default 8 applies) and clamps to `[1, 12]`. The clamp's
own comment gives the reason:

> a backstop so an over-large value cannot push the matrix far past the
> concurrent-job budget (excess shards just queue, wasting per-shard
> image-pull + kcov startup ~30-60s fixed overhead)

The reasoning is right and the number is a guess. The budget is about 20, not
12, and -- the part the comment does not account for -- **every other job has
finished by minute three**, so from then on the matrix could use every slot
there is.

**At t
[...截斷，原長 4311 字]

> 留言 (ycpss91255, 2026-09-05): ## Two of the four open items, measured

**The per-shard fixed cost is 21s, not the 30-60s the clamp's comment assumes.**

From the `coverage (1/8)` job of run 33969173216, read from its own log:

```
13:32:31.697  Current runner version          <- job starts
13:32:34.156  Run actions/checkout@v7
13:32:35.601  Run docker/setup-buildx-action@v4
13:32:49.700  --- Running Tests with Kcov Coverage (s
[...截斷，原長 2438 字]

> 留言 (ycpss91255, 2026-09-05): ## Scope correction: the target is not GitHub's 20 slots

The repo is moving to a self-hosted runner. That makes "tune the shard count to
the free plan's concurrency budget" the wrong fix -- it optimises against a
number that is about to be replaced, and the idle capacity would come straight
back in a different shape.

The invariant worth building is the one underneath: **the run should saturate
w
[...截斷，原長 3384 字]

> 留言 (ycpss91255, 2026-09-05): ## Correction: the self-hosted target is a scale set, not one runner, so sharding stays right

My previous comment said a self-hosted runner takes one job at a time, so the
shard matrix would serialise and base#726's shape (one job, N processes inside)
is what a self-hosted regime wants. That is true of ONE REGISTERED RUNNER
INSTANCE, and it is exactly the problem `github_runner`#159 was opened to
[...截斷，原長 3349 字]

> 留言 (ycpss91255, 2026-09-05): ## Correction: "twenty sequential lint jobs on self-hosted" is wrong, and it is the same error twice

An earlier comment here argued for consolidating the 20-job `lint-static`
matrix partly on the grounds that "on a single self-hosted runner it is worse:
twenty sequential jobs, each paying its own startup."

That is true of the org's CURRENT state -- one statically registered runner
instance, whic
[...截斷，原長 2244 字]


### #1070 [OPEN] track(ci): one pipeline, two runner profiles -- parallelism inside the job on GitHub-hosted, across jobs on self-hosted
labels: enhancement

## Two pools, two shapes, one pipeline

base's CI has to work on GitHub-hosted runners and on the org's self-hosted
fleet. The two want genuinely different shapes, because **the scarce resource
is the opposite one in each**:

| | GitHub-hosted | self-hosted |
|---|---|---|
| scarce | **slots** -- 20 concurrent, org-wide, free plan | **CPU** -- slots are created on demand, the host meters them |
| a slot is | a whole 4-CPU machine you already have | a container the listener provisions per job |
| so parallelism belongs | **inside the job** (oversubscribe `--jobs` on 4 cores) | **across jobs** (many shards, each near one core) |
| shard count | at most the free slots at t=0 | work divided by a target shard duration, uncapped |
| kcov fidelity | worse: one parser, high trace rate | **better: one parser per shard, low trace rate** |

That last row is not a side note. base#1060 established that the coverage line
set moves when trace volume through kcov's single-threaded parser gets high --
the full suite loses 30 to 85 covered lines under `bats --jobs`, non
deterministically, while a shard mostly does not. The self-hosted shape puts
the LEAST load on each parser, so it is the faster arrangement and the more
accurate one at the same time.

## What must NOT happen: two pipeline definitions

Exactly three values differ between the two shapes:

1. `runs-on`
2. the shard count
3. `--jobs` inside a shard

The container, the command, the weight-balanced partition, the `kcov --merge`,
the
[...截斷，原長 5876 字]


### #1078 [OPEN] fix(upgrade): upgrading writes a new file into the consumer's .github/workflows, announced as one INFO line
labels: needs-triage

`upgrade.sh` writes a new file into the consumer's `.github/workflows/`. The
workflow itself is benign, but writing into that directory is not a neutral
act, and a consumer that asserts on its own workflow set goes from green to
red purely by upgrading.

## Reproduce

    git clone --recurse-submodules https://github.com/ycpss91255-docker/omniverse_web_viewer
    cd omniverse_web_viewer                # green at .base v0.41.0
    ./.base/upgrade.sh v0.43.0-rc2         # exit 0, tree healthy, 0 dangling symlinks
    ./script/build.sh test                 # FAILS

    not ok 84 gates: /workflows/ holds exactly the workflows the checker was run against
    -- output differs --
    expected (1 lines):  main.yaml
    actual   (2 lines):  base-version-monitor.yaml
                         main.yaml

The upgrade announces it as one INFO line among about twenty:

    Created .github/workflows/base-version-monitor.yaml

## Why that assertion exists

owv's release invariant is "no version publishes without the picture gate
having passed on that commit". `check_release_gates.py` enumerates
`/workflows/` rather than trusting a single filename, precisely so a SECOND
workflow cannot publish outside the gate. That check was added after a review
demonstrated the hole by adding a `sneaky.yaml` with `packages: write`.

So the guard fired correctly. It cannot distinguish "base added a monitor"
from "someone added a publisher" -- that is the point of enumerating.

## The injected workflow is ben
[...截斷，原長 3799 字]


### #1082 [OPEN] feat(ci): give consumers a publish-capability check over their whole workflow set, not just the gated one
labels: needs-triage

Every base consumer that gates its releases has the same exposure, and base
ships nothing that covers it. Filed with a working implementation behind it
rather than as an idea -- `omniverse_web_viewer` landed this today
(ycpss91255-docker/omniverse_web_viewer#81) and the shape held up.

## The exposure

A repo's release invariant lives in one workflow. Anything that can publish
from a SECOND workflow is outside it -- `needs:` does not cross files, so a
second workflow cannot be made to stand behind the first one's gate. Nothing
in base notices a second workflow appearing, and nothing tells a consumer to
look.

owv found this the expensive way. Its checker read `main.yaml` and used a
blunt stand-in for the analysis it did not have:

    find /workflows -mindepth 1   ->   must equal exactly "main.yaml"

That is not a workflow-set policy; it is "everything I have not read is
forbidden", which holds only until something legitimate arrives.

## What made it concrete: base's own upgrade

`v0.43.0`'s `upgrade.sh` creates `base-version-monitor.yaml` in the consumer's
`.github/workflows/` (#1078). Upgrading a throwaway owv clone turned a green
build red with nothing actually wrong -- the monitor is `schedule` /
`workflow_dispatch`, `contents: read` + `issues: write`, and pushes nothing.

So base is already, correctly, adding workflows to consumers. That is fine.
What is missing is any way for a consumer to tell base's benign workflow from
a publishing one, other than by trusting the fi
[...截斷，原長 3852 字]


### #1083 [OPEN] test(coverage): raise the coverage floor from 80 to 90
labels: enhancement

## Decision

`COVERAGE_MIN` goes from **80 to 90**. Not 95.

`script/test/drivers/coverage_gate.sh:44` has carried 80 since it was written,
with a comment saying it is "set just under the current rate so it ratchets up
as coverage climbs" -- and nothing ever climbed it. The tree reports 84.5%
today, so the floor has been more than four points of dead slack.

## Why 90 rather than the 95 that was asked for

95 is not reachable on the figure kcov reports, and the two ways to make it
reachable were both rejected on their merits. base#1073 carries the full
investigation; the short version:

Of 1577 uncovered lines, **534 can never receive a hit** -- they are not bash
statements. Array element rows, `done < file` terminators, `} > file` group
closes, empty `case` arms. bash emits one execution event for a whole multi-line
command, so the other lines have nothing to attribute; kcov's line scanner marks
them coverable anyway. Verified against a synthetic file in which every line
executes, and the classification of the tree was done with a real bash parser
(`mvdan/shfmt --to-json`), not a hand-written scanner.

Those 534 sit in the denominator permanently, which caps the tree at

    (10194 - 534) / 10194 = 94.76%

"100% coverage" here means "everything creditable is credited", and that state
is 94.8%. And 534 is a **lower** bound on the uncreditable lines, so 94.8 is an
optimistic ceiling, not a target.

The two ways past it were rejected:

- **Correcting the denominator.** Reaching
[...截斷，原長 4286 字]


### #1084 [OPEN] fix(test): the frozen-path guard goes quiet one release after it was written
labels: bug

## The guard for base#1077 protects it for exactly one more release

`test/bats/integration/prev_release_upgrade_spec.bats` now drives a released
`upgrade.sh` into the current tree and then upgrades **again** from the tree that
produced -- which is what catches a frozen path missing from the *result* rather
than from the input. It found base#1077 and goes red on it (verified by
deleting the forwarder: `status 127`, `env: './.base/upgrade.sh': No such file
or directory`).

Its scope is `PREV_RELEASE_WINDOW`, which is **2**, with no override anywhere in
the repo or CI. So the arms cover `{v0.42.0, v0.41.0}`, and only v0.41.0 names
`./.base/upgrade.sh` -- v0.42.0 already names the `dist/` path. **One arm of
seven carries base#1077.**

**When v0.43.0 is tagged the window becomes `{v0.43.0, v0.42.0}`.** Both are
`dist`-era, so `_released_entry` returns the deep path in both arms, and
**deleting the repo-root `upgrade.sh` AND the repo-root `init.sh` would leave
all seven arms green.** v0.43.0-rc2 is already cut, so this is days away, not
hypothetical.

The evidence for the mechanism is direct: with the forwarder deleted, arm 1
(newest release) passed and only arm 2 (N-1) failed. The claim that both slots
will have that shape after the tag is read off `_stable_release_tags` rather
than run, since minting a tag to prove it is not worth it.

## Why this is not just the support boundary moving

That reading is available and it is wrong, which is why this issue exists.

ADR-00000006 tie
[...截斷，原長 3790 字]


### #1087 [OPEN] feat(setup): parameterise both generate APIs so an orchestrator can drive one repo N times
labels: enhancement, ready-for-agent

## Decision

base is a building block; `multi_run` is the assembler. Both of base's
generation stages -- **devel** (`just docker setup`) and **deploy**
(`just docker setup deploy`) -- become APIs an orchestrator can call N times
against ONE repo, each call carrying that instance's parameters and writing to
a directory the caller names. The repo itself is not mutated by a call.

Nothing base emits may be a value the caller cannot reach. Where a value is
fixed today, that is a defect to be closed, not a property to be documented.

## The two changes this needs

### 1. The `.setup.conf.local` layer takes a path

The conf chain is `<template>/.setup.conf` -> repo `.setup.conf` ->
`.setup.conf.local`, section-replace at each step (`CONTEXT.md:148-155`,
`resolve.sh:147`, `stage.sh:370`). The third layer is the right one for
per-instance parameters -- it already overrides **any** section, not a
whitelist (ADR-00000025:68).

What is missing is that its path is fixed. An orchestrator cannot say "use
THIS file as the local layer for this call", so two instances cannot have two
parameter sets without writing into the repo and racing each other.

Add a way to name the file. The flag/env spelling is an implementation detail;
the requirement is that one call reads a caller-supplied local layer and
another call reads a different one, concurrently, with no write to the repo's
own `.setup.conf.local`.

### 2. Generation takes an output directory

`deploy` already has `--output` (`setup_cmd.sh
[...截斷，原長 3379 字]


### #1089 [OPEN] fix(test): deleting the GHCR cleanup workflow leaves its 22-case guard reporting green
labels: bug, ready-for-agent

## The defect

`test/bats/unit/ghcr_cleanup_yaml_spec.bats` guards the scheduled workflow that
deletes GHCR package versions. Its `setup()` ends with:

```bash
WF="/source/.github/workflows/ghcr-cleanup.yaml"
[[ -f "${WF}" ]] || skip "ghcr-cleanup.yaml not at expected path"
```

**Delete the entire workflow and the spec reports `1..22, 22 ok, 0 not ok,
EXIT=0`** -- all 22 cases carrying `# skip ghcr-cleanup.yaml not at expected
path`. Nothing asserts the file exists. Measured by reverting base#935's
production change (a `git rm` of the file it created, which is the honest
reversal) and re-running; confirmed independently in a second worktree. The
control run is 22 ok with 0 skips.

Renaming or moving the workflow has the same effect as deleting it: every
assertion passes.

## Why this one matters more than a normal fail-open

base#813, the issue that motivated the workflow, is explicit that the naive
implementation is dangerous: `actions/delete-package-versions` with
`delete-only-untagged-versions` deletes the per-arch children of a LIVE tag,
which turns every consumer's `docker pull` into a 404. The spec exists to keep
that shape gated. base#935's body claims it makes "a catastrophic edit fail in
CI rather than on ghcr.io".

The 22 assertions do pin that shape correctly **while the file is present**.
The hole is only the precondition -- but the precondition is the one thing that
turns the whole guard off silently.

## The fix

**Minimum:** turn the precondition into the firs
[...截斷，原長 2680 字]


### #1090 [OPEN] fix(test): nine guards whose population or subject is declared, not derived
labels: bug, ready-for-agent

## The pattern

A retrospective over the 63 PRs of the v0.43.0 cycle -- revert each PR's
production change, keep its tests, run them -- found 60 GUARDED, 1 PARTIAL and
2 FAIL-OPEN. The headline number is healthy. The mechanism behind the failures
is not, because it is one mechanism wearing three costumes:

> **The guard's population or subject is DECLARED, not DERIVED.**

This repo already knows this (`P2. Derive the population; never enumerate it`,
and the recorded lesson that guards must derive rather than restate). These are
the places where it did not hold. **9 PRs, 10 assertion groups.**

### A. The subject is absent, so the guard skips (3)

| where | what happens when the subject is gone |
|---|---|
| `ghcr_cleanup_yaml_spec.bats` | 22 of 22 skip; filed separately as its own issue |
| `template_spec.bats` (two payload guards, base#918) | `# skip archive.manifest not present` |
| `reproducibility.bats` adoption guard (base#981) | `# skip image predates the manifest template revision` |

### B. The feature is absent, so the assertion is vacuously true (4)

| where | why it passes with the feature gone |
|---|---|
| `ci_spec.bats` #30 (base#1081) | "an out-of-range group spec is refused" -- with the option gone, everything is refused |
| `coverage_handback_spec.bats` #9 (base#1079) | "no host-side rm decides the outcome" -- equally true when the code does not exist |
| base#1026 unit 1 + integration ok 1 | same shape |
| `ci_spec.bats` (base#1074) | `refute_output --regexp
[...截斷，原長 3558 字]

> 留言 (ycpss91255, 2026-09-06): ## Two more mechanism-D instances, from the 2026-09-06 base audit

Both are the same shape as the three already listed under "The population is
hand-listed": the guard runs, and its population came from somewhere other than
the thing it claims to cover. Adding them here rather than opening separate issues.

---

### 1. `schema_spec` -- two tables titled "every registered key" cover 40 of 47

`test
[...截斷，原長 7063 字]


### #1091 [OPEN] feat(tdd): break the behaviour once, to prove the test was pinning it
labels: enhancement, ready-for-agent

## The gap the retrospective could not see

The v0.43.0-cycle retrospective audited every PR by **removing** the production
change and re-running its tests. That move detects a test that does not notice
absence. It cannot detect a test that notices absence but would miss a **wrong
answer** -- because a guard that only greps for a string still turns red when
the file carrying that string is deleted, and so scores identically to a
behavioural guard.

Four assertion groups are known to be in that blind spot (mechanism E in the
report): `reclaim_wiring`'s 9 `code_grep` cases, base#988's version-declaration
grep, base#1023's 6 `code_grep -F` cases on release-worker (the resolver being
wired up passes even if it returns the wrong version), and base#943's refutation
of four named constructs (`cp -r`, `tar czf`, `zip -r`, `files:`) which a switch
to `7z` or a composite action walks straight past.

A further 10 PRs' tests catch only deletion -- every failure on revert was
`command not found` or `No such file`. Those are one refactor away from
fail-open.

## The move that closes it, already validated twice this cycle

**Mutation probe.** Put the production code back, then break its behaviour in
place -- the cheapest version is inserting `return 0` at the top of the driver so
it always reports clean -- and run the spec. It must go red.

Used twice during the audit, both times conclusive:

- **base#986**: driver restored, `return 0` inserted. Spec still `4 ok /
  17 not ok`, proving it p
[...截斷，原長 2559 字]


### #1092 [OPEN] fix(upgrade): a squashed subtree pull cannot see a local edit upstream did not touch
labels: bug, ready-for-agent

## Measured

Every vendored `.base/` tree in the org was compared file-by-file against what
base shipped at the tag that repo's `.base/.version` claims, by git blob SHA and
mode -- byte-exact, so a whitespace or line-ending variant would have shown.

**2217 files across 18 repos. One local edit. Zero partial upgrades.**

The pipeline was negative-controlled: pointed at the wrong tag it reports
14 only-in-consumer / 2 only-in-base / 49 content-differs, so the zeros are real
rather than a broken comparison.

That is a good result. This issue is about the one exception, and specifically
about *why nothing noticed it*.

## The edit, and how it rode through an upgrade

`ros2_distro`, `.base/test/unit/bashrc_spec.bats`, commit `4c8aaec`
(2026-06-07, single-parent, not a subtree merge):
`fix(bashrc): re-point swc at colcon install/ paths (#28) (#29)` appended 48
lines -- five bats tests for the `swc` helper. Purely additive. The same commit
also edited the repo's own `config/shell/bashrc`, so a repo-local fix reached
across into the vendored tree to put its tests there instead of in the repo's
own `test/`.

The repo was on v0.34.0 at the time. Later, `109e368` upgraded the subtree to
v0.41.0 -- and the edit survived silently:

> Upstream's copy of that path is byte-identical from **v0.34.0 through
> v0.41.0**. The squash merge saw a change on the local side and no change on
> the upstream side, so it kept the local version with no conflict and no
> warning.

**`git subtree pull --sq
[...截斷，原長 3646 字]


### #1093 [OPEN] fix(config): ten repos share one setup.conf ancestor that predates the template rename
labels: bug, ready-for-agent

## Measured

Ten repos share one **identical** `setup.conf` blob (`d360e728`) that matches
**no base tag at any version**:

`ai_agent`, `claude_code`, `codex_cli`, `gemini_cli`, `ros2_distro`,
`ros_distro`, `sick_humble`, `sick_noetic`, `urg_node_humble`, `urg_node_noetic`

Its header still reads:

```
Template default lives at <template>/setup.conf
```

-- wording from before the `template/` to `.base/` rename. So this is not ten
repos each customising their config. It is **one stale ancestor, copied once at
bootstrap and never re-synced**, now roughly 202% divergent from the `.base/`
copy sitting next to it in the same checkout.

Found while measuring vendored-tree drift across the org. The vendored `.base/`
trees themselves are clean -- 1 edited file in 2217 -- so this is the opposite
finding: the file base does *not* own has drifted, silently, in a correlated
way that says it came from a common ancestor rather than from ten decisions.

## Why it matters

`setup.conf` is the input to everything base generates: the resolved config
fans out to `compose.yaml`, `.env`, `.env.generated`, the baked runtime `ENV`
and the deploy bundle. A template that predates the rename predates every key
added since, so these ten repos are being resolved against a schema surface that
has moved underneath them -- and base#1086 has just shown what a silently-wrong
`setup.conf` costs (an image renamed after its directory, an empty
`[environment]`, exit 0 throughout).

Note also that base#1086's mi
[...截斷，原長 2834 字]


### #1094 [OPEN] fix(config): five keys that validate and then never reach the emitted file
labels: bug, ready-for-agent

## Five keys that validate, and then do nothing

Measured while auditing base's coverage of the Compose Specification. Each of
these is accepted by `_schema_validate`, several are offered in the TUI, and
each fails to reach the emitted file -- silently, which is what invariant 2
exists to forbid. Paths are relative to `dist/`.

### 1. `[network] pid = container:<name>` never reaches any file

`_validate_pid_mode` accepts it (`lib/_tui_conf.sh:276-284`) and the TUI offers
it. Both emitters write `pid:` **only when the value is exactly `host`**
(`lib/compose_emit.sh:1194`, `:816`; `lib/deploy.sh:572`). A user who sets
`container:foo` gets a green config and a compose file with no `pid:` line at
all.

**Fix:** emit the value the config carries. If `container:<name>` is genuinely
unsupportable, the validator must reject it -- but it is a legal Compose value,
so emitting it is the answer.

### 2. `[resources] shm_size` is inert under the shipped default

Validated at `lib/_tui_conf.sh:133-143`, dropped by every emitter unless
`ipc` is not `host` (`lib/compose_emit.sh:1329`, `:989`; `lib/deploy.sh:664`).
The shipped template sets `ipc = host` (`.setup.conf:189`).

So **the default configuration makes this key do nothing**, and the only key in
the entire `[resources]` section is the one that is off by default.

`ports` has exactly the same situation under `mode = host` and prints a
diagnostic for it (`lib/compose_emit.sh:84-92`). `shm_size` prints nothing.

**Fix:** the same diagnos
[...截斷，原長 3578 字]


### #1095 [OPEN] fix(schema): tmpfs is the one section with no validator, and it reaches compose
labels: bug, ready-for-agent

## `[tmpfs]` accepts any value, including one that changes the YAML

base#1062 reports that `[tmpfs]` ships in the template with no schema keys.
Confirmed, and the consequence is sharper than "undocumented".

- The template ships the section with a header and an empty body
  (`dist/.setup.conf:246-247`).
- `SCHEMA_SECTIONS` lists `tmpfs` (`lib/schema.sh:112`), so
  `setup.sh set tmpfs.tmpfs_1 ...` dispatches.
- `SCHEMA_VALIDATOR` (`lib/schema.sh:45-95`) has **zero** `tmpfs.*` rows, so
  `_schema_validate` falls through to its free-form branch
  (`lib/schema.sh:359`) and **accepts anything** -- including a value
  containing a newline or leading whitespace.
- The value reaches the emitted file: `_conf_list_sorted` at
  `lib/deploy.sh:353` -> `_emit_tmpfs_block` (`lib/compose_emit.sh:424-433`),
  called at `:1327`, `:986` and `deploy.sh:662`.

`[volumes]` guards the identical shape: `_validate_mount`
(`lib/_tui_conf.sh:45-49`) rejects exactly this class of input. `[tmpfs]` is
the same kind of value -- a container path plus options -- with none of the
guard.

`SCHEMA_FREEFORM` is empty (`lib/schema.sh:239`), so `tmpfs` is not even a
*declared* opt-out. It is an omission.

## A stale comment that hides it

`lib/schema.sh:106-108` names "image / gui / tmpfs" as the free-form-only
sections. That is out of date: `image.rule_` has a validator
(`lib/schema.sh:84`) and so does `gui.mode` (`:54`). **`tmpfs` is the only
genuinely keyless section of the fifteen**, and the comment makes it
[...截斷，原長 1965 字]


### #1096 [OPEN] track(compose): base expresses 33 percent of the compose service surface
labels: enhancement

## The measurement

base's purpose, as stated: it replaces the hand-written `docker compose`
configuration of a repo that runs a single container, and within that scope it
must be able to express everything a hand-written compose file can express.

That completeness claim had never been measured. It is now, against the Compose
Specification's own field list (fetched from `compose-spec/compose-spec` at
`main`, 92 service-level fields extracted mechanically from the headings, not
from memory):

| class | count | share |
|---|---|---|
| **A** -- has a `setup.conf` key | 21 | 23% |
| **B** -- emitter-decided, a reader could predict it | 6 | 7% |
| **C** -- emitter-decided, not predictable | 2 | 2% |
| **D** -- cannot be expressed at all | **58** | **63%** |
| **E** -- out of scope under the single-container rule | 5 | 5% |

**Reachable at all: 29 of 92 (32%).** Against the in-scope denominator
(92 − 5): **33%**. The field-deploy bundle is lower still at 24%, because it
additionally drops `build`, `logging`, `stdin_open`, `tty`, `profiles`,
`hostname`, `extends` and top-level `volumes:`.

The five E fields are named with their reasons so the exclusion is auditable:
`depends_on`, `links`, `external_links`, `volumes_from`, `scale` -- each is
about a second service, which the single-container rule places in a separate
repo. Swarm-only `deploy.*` sub-keys likewise.

## The gap, ordered by how likely a single-container repo is to need it

1. **`healthcheck`** -- and the substitute we t
[...截斷，原長 4927 字]

> 留言 (ycpss91255, 2026-09-06): ## Correction: the target is six fields, and this issue's ordering was wrong

The decision taken on this issue was that the target is not the Compose
Specification but **the fields a single-container repo in this org actually
uses**, with the population derived by measurement. That measurement is done,
and it corrects two things this issue asserted.

### The population

Evidence was gathered in fo
[...截斷，原長 4670 字]


### #1097 [OPEN] feat(upgrade): let init.sh run the migrations between the version it came from and the one it is
labels: enhancement, ready-for-agent

## The pattern behind base#919, #1077 and #1086

Three consumer-facing failures this cycle, one mechanism: **on a cross-version
upgrade the consumer's own vendored driver runs, and it only does what its
generation knew about.** Anything the new release needs done is unreachable
unless the new code gets to run.

Each was fixed by moving that one thing into `init.sh`. That works, and it is
the recorded rule -- `init.sh` is the only point in an already-shipped upgrade
flow that executes current code. But it is being applied **one incident at a
time**, and the cost of each discovery is a consumer.

This issue is to stop discovering them.

## The handoff point already exists, and already runs new code

Measured from the released v0.41.0 driver (`git show v0.41.0:upgrade.sh`), which
is what fifteen of the org's repos will actually execute:

```
Step 1/5  git subtree pull       -> .base/ is now the NEW tree, and committed
Step 2/5  post-pull integrity check
Step 3/5  ./.base/init.sh        <- the NEW init.sh runs here
Step 4/5  update main.yaml @tag references     <- old code
Step 5/5  patch Dockerfile lint stage          <- old code
```

So there is nothing to fetch and no newer copy to look for: by Step 3 the new
tree is in place and the file being executed is already the current one. What is
missing is only that it does a symlink resync and hands control back.

## The from-version is recoverable, which makes version-bound migrations possible

The obstacle everyone would expect is
[...截斷，原長 4690 字]


### #1099 [OPEN] fix(test): a random temp-path suffix can satisfy a version refutation
labels: bug, ready-for-agent

## The flake

`test/bats/unit/generated_workflow_actions_lint_spec.bats:435` asserts:

```bash
refute_output --partial 'v1'
refute_output --partial 'v2'
```

against output that embeds a scratch directory created at line 56:

```bash
SCRATCH="$(mktemp -d)"
```

`mktemp -d` names the directory from a random suffix. When that suffix happens to
contain `v1` or `v2`, the refutation fires on the path rather than on the thing
under test.

Observed during a gate run: the directory was `/tmp/tmp.fFby7v1xul`, and the
spec failed on the `v1` inside `fFby7v1xul`.

## Rate

Roughly **0.47%** -- about 1 gate run in 214. Low enough to be dismissed as
noise, frequent enough that it will be dismissed as noise repeatedly.

It cost one full gate cycle on base#1080's branch, where it read as a failure of
that change.

## Why it matters beyond the cost

A flake that fires on a *substring of a temp path* teaches the reader that a red
gate might be nothing. That is the expensive part: the next real failure in this
file gets a re-run before it gets a diagnosis.

## The fix

The assertion means "the emitted output must not name version `v1` or `v2`". It
should be scoped to where a version can appear, not to the whole output --
anchored to the field being checked, or matched with a boundary so a path
component cannot satisfy it.

Keeping the scratch path out of the captured output would also work and may be
simpler; the spec does not need the path in what it asserts against.

**Verification:** force 
[...截斷，原長 1766 字]


### #1103 [OPEN] feat(changelog): fold the duplicate category heading a merge produces, instead of only refusing it
labels: enhancement, ready-for-agent

## The toil

Every branch that appended to `## [Unreleased]` and then merges `origin/main`
produces a duplicate category heading. Git resolves it without a conflict --
both sides added lines to the same section, so both survive -- and
`changelog-entry` then refuses the result:

```
1 over-long entry / duplicate entry / repeated category heading / ... in '## [Unreleased]'
```

The lint's own message names the cause exactly:

> merging origin/main into a branch that appended to '## [Unreleased]' keeps
> both sides without conflicting, so a duplicate lands with nothing to review

Hit **three times in one afternoon** while landing a serial queue (base#1080,
base#1086, the setup_tui coverage branch), and it will recur on every remaining
branch in that queue. Each occurrence costs a full gate cycle -- roughly eight
minutes -- to discover something that is mechanical to fix.

## Why this is not the lint being wrong

The lint is correct to refuse. Two `### Fixed` blocks in one release block is a
real defect: a reader scanning for what was fixed finds half of it, and the
release-notes generator has no reason to prefer one over the other.

What is missing is that the repair is deterministic and nobody does it
automatically. The category roster is already declared in one place
(`script/release/changelog_categories.sh`), which is exactly what a
normaliser needs.

## The fix

A normaliser that reads the roster, groups every entry under its category, emits
each category once in roster orde
[...截斷，原長 2707 字]


### #1108 [OPEN] fix(test): six specs a PR edited that cannot fail on anything that PR changed
labels: bug, ready-for-agent

## Six specs a PR edited that guard nothing it changed

The v0.43.0-cycle retrospective reverted each PR's production change, kept its
tests and re-ran them. At least 30 specs a PR touched stayed fully green.

Most of those have a legitimate reason -- the diff was comments only, or the
spec asserts behaviour the PR deliberately left alone. **These six do not.**
Each was edited by the PR named, and none of its assertions can fail on
anything that PR changed:

| spec | result on revert | PR |
|---|---|---|
| `smoke_helper_spec.bats` | 33 ok / 0 not ok | base#1031 |
| `self_test_yaml_spec.bats` | 113 ok / 0 | base#1031 |
| `kcov_bash_instrumentation_spec.bats` | fully green | base#983 |
| `yaml_permission_surface_spec.bats` | 36 ok / 0 | base#982 |
| `readme_file_table_spec.bats` | fully green | base#982 |
| `self_test_yaml_spec.bats` | 106 ok / 0 | base#966 |

Two are worth naming individually:

- **`yaml_permission_surface_spec` is the spec base#982's own body says it
  rewrote.** The rewrite landed and the file cannot fail on the change.
- **base#966 bumped a workflow version v6 -> v7** and
  `self_test_yaml_spec.bats` carries no assertion about it at all, despite
  being the spec the PR edited.
- **base#957's README half has no failing witness either** --
  `readme_file_table_spec` is green with the change reverted.

## What this is and is not

It is **not** a claim these specs are worthless. Each may assert something real
about code the PR did not touch. What is missing is 
[...截斷，原長 2473 字]


### #1109 [OPEN] fix(ci): the shared test-tools latest tag moves before the smoke test that is its only check
labels: bug, ready-for-agent

## The defect

`.github/workflows/release-test-tools.yaml` is triggered by `push` on tag `v*`
(`:45-52`). Its three jobs (`compute-matrix` `:85`, `build` `:127`, `merge`
`:193`) chain to each other and have no `needs:` on `self-test.yaml`, nor any
other dependency on it.

In the `merge` job the tag set is resolved at `:269-277` and, for a
non-prerelease, `${IMAGE}:latest` is appended. `docker buildx imagetools create`
publishes it at `:311`. The only step that validates the image, `Smoke test
pushed image`, runs at `:313` -- **after** the manifest has been created.
`grep -n 'failure()\|rollback\|imagetools rm'` over the whole file returns
nothing, so a failing smoke leaves the moved `:latest` in place.

## Evidence

- Ordering: `release-test-tools.yaml:293-311` (`imagetools create`) precedes
  `:313` (smoke). No rollback anywhere in the file.
- Timing, measured on the real v0.42.0 tag: run `32804287362` (Release
  test-tools) completed at `2026-08-25T03:14:09Z`. Run `32804287445` (CI,
  carrying the full gate and the `release` job) did not finish until
  `03:20:07Z`. `:latest` moved **5 minutes 58 seconds** before that tag's tests
  had a verdict. Per-job data: bats-integration ended 03:15:51, the coverage
  shards ran to 03:19:42.
- Blast radius, measured across 22 org repos: `build-worker.yaml:34-37` defaults
  `test_tools_version` to `"latest"`, and the downstream `main.yaml` generated by
  `dist/script/base/init.sh:536-539` passes only `image_name`. Of the 19 repos
  that
[...截斷，原長 4819 字]


### #1110 [OPEN] fix(upgrade): the restart-default migration gates on the tree the pull replaces, so no consumer can reach it
labels: bug, ready-for-agent

## The defect

`upgrade.sh` carries a migration that rewrites a stale `restart = no` out of a
downstream `.setup.conf`. It runs **before** `git subtree pull` (call site
`upgrade.sh:639`, the pull at `:692`) and needs two things at once:

- (a) the running driver contains the function, and
- (b) the **vendored** template at `${_root}/${TEMPLATE_REL}/dist/.setup.conf`,
  as it exists before the pull, still says `restart = no` (gate at
  `upgrade.sh:227`).

The driver is always the consumer's own vendored copy. The function and the new
template value arrived in the **same commit** (`694a0459`). The two conditions
are therefore mutually exclusive by construction. This is not "rarely fires" --
it is **can never fire**.

## Evidence

- `upgrade.sh:218` (the function), `:225-227` (gate b), `:639` (call site),
  `:692` (the pull).
- The driver is always the vendored copy: the root forwarder `upgrade.sh:44-48`
  execs `dist/script/base/upgrade.sh`, and `dist/script/base/justfile.base:44`
  hardcodes `./.base/dist/script/base/upgrade.sh`.
- Tag matrix, exhaustively checked: only `v0.42.0-rc4`, `v0.42.0`, `v0.43.0-rc1`
  and `v0.43.0-rc2` ship `dist/.setup.conf`, and every one of them already says
  `restart = unless-stopped` and already carries the function.
  `git log --all -S'restart = no' -- dist/.setup.conf` returns only `694a0459`
  and `a02bbe42`, neither of which is tagged.
- v0.41.0 dies one step earlier: that tag has no `dist/` at all (the template
  lives at `config/docker/se
[...截斷，原長 5290 字]

> 留言 (ycpss91255, 2026-09-08): ## Dependency, not visible in the four `ready-for-agent` sections

This issue's step 1 -- move the `restart = no` rewrite into `init.sh` -- is the same move #1097 (open, `ready-for-agent`) generalises: let `init.sh` run the migrations between the version it came from and the one it is. The issue body already names that relationship; recording it here because the label's required sections cannot ex
[...截斷，原長 893 字]


### #1111 [OPEN] fix(init): the generated monitor workflow freezes a base-internal path in every consumer repo
labels: bug, ready-for-agent

## The defect

`_sync_base_monitor_workflow` returns immediately when the file already exists
(`init.sh:1573-1574`, `[[ -e "${_wf}" ]] && return 0`), and its heredoc bakes

```
run: ./${TEMPLATE_REL}/dist/script/base/check-base-version.sh run
```

into the consumer's `.github/workflows/` (`init.sh:1606`).

Never-overwrite is deliberate and is pinned by tests. The consequence is that
base writes a file into a consumer's repo and then promises never to touch it
again -- so `dist/script/base/check-base-version.sh`, a base-internal path,
becomes **indefinitely frozen** for every repo that has ever been bootstrapped.
ADR-00000006's protocol-stable list does not contain it.

## Evidence

- `init.sh:1573-1574` (early return), `:1606` (the baked `run:`), `:1601`
  (`actions/checkout@v7`).
- Both guards are string greps against the file `init.sh` has just written:
  `test/bats/unit/init_spec.bats:591-596` and
  `test/bats/integration/init_new_repo_spec.bats:174`. Nothing asks whether the
  path resolves.
- Never-overwrite is pinned: `init_spec.bats:598-605` ("never clobbers a
  user-tuned file") and `:934-947`.
- The repo already records this write-once property elsewhere, but only for the
  `uses:` ref: `script/test/drivers/generated_workflow_actions.sh:26-28` --
  "`init.sh` skips when the file exists, so the subtree upgrade that refreshes
  everything else never refreshes it".
- Lockstep rename experiment, run in a temporary worktree: renaming
  `check-base-version.sh` and updating
[...截斷，原長 5195 字]

> 留言 (ycpss91255, 2026-09-08): ## Dependency, not visible in the four `ready-for-agent` sections

Part 2 of this issue rewrites `_sync_base_monitor_workflow` (`init.sh:1573-1606`) -- the generated `run:` line and, by implication, the never-overwrite early return. #1078 (open) is about the same function: it asks for a louder announcement when that file is created, a `setup.conf` key letting a consumer decline it, and a CHANGELOG
[...截斷，原長 819 字]


### #1112 [OPEN] fix(upgrade): two of the four shipped reusable workers keep their old ref, and the commit message claims otherwise
labels: bug, ready-for-agent

## The defect

`upgrade.sh:726-727` rewrites exactly two `uses:` refs -- `build-worker.yaml@`
and `release-worker.yaml@` -- while the commit message at `:763`
unconditionally claims `main.yaml: workflow @tag updated to ${target_ver}`.

Base ships **four** reusable workers
(`grep -l workflow_call .github/workflows/*.yaml`: build-worker, release-worker,
publish-worker, multi-distro-build-worker). The other two are never touched by
any upgrade, and the commit message says they were.

## Evidence

- `dist/script/base/upgrade.sh:726-727` (the two `sed` calls), `:763` (the
  claim).
- Org state, read via the GitHub API from each repo's `main.yaml` and
  `.base/.version`: `ros_distro` and `ros2_distro` are both on `.base=v0.41.0`
  and carry `build-worker.yaml@v0.41.0`, `release-worker.yaml@v0.41.0` and
  `publish-worker.yaml@v0.20.0` -- **21 minors behind**, and every subsequent
  `just base upgrade` leaves it alone. `ros_distro`'s caller grants that job
  `packages: write`.
- The fixture cannot see it: `test/bats/integration/upgrade_spec.bats:109-124`
  builds a `main.yaml` containing only the two workers the `sed` handles, and
  `:138-139` asserts only those two.
  `grep -rn 'publish-worker.yaml@\|multi-distro-build-worker.yaml@' test/bats/`
  returns nothing. The population is declared, not derived from the set of
  workers base ships.
- Base's own pin lint exempts this class of ref on a premise that is false:
  `script/test/drivers/generated_workflow_actions.sh:157-159` and `:5
[...截斷，原長 3869 字]


### #1113 [OPEN] fix(lint): two hand-written rosters, so a shipped script and any new lint driver are scanned by nothing
labels: bug, ready-for-agent

## The pattern

Two lint rosters in this repo are hand-written where the tree could be asked
directly. Design principle P2 ("Derive the population, never enumerate it")
covers both, and both have the same failure shape: something real is scanned by
nothing, and every spec stays green.

They are filed together because the fix is the same move in both places --
replace the literal list with a directory-derived one plus a short, reasoned,
fail-closed exemption array.

---

## A. ShellCheck's `dist/` targets are a hand-written list, and two shipped scripts are in no scan at all

**Defect.** `_run_shellcheck` (`script/test/drivers/shellcheck.sh:16-71`)
enumerates its `dist/` targets by name. `find dist -name '*.sh'` returns 55-56
files. Two of them are in no pass: `dist/deploy/cd-guard.sh` and
`dist/config/shell/bashrc.d/30-name-host-groups.sh`.

**Evidence.**

- Mutation, verified: appending `probe_unquoted() { local f="a b"; ls $f; }`
  (SC2086) to **both** files, `./script/test/test.sh --shellcheck-only` prints
  `--- Running ShellCheck ---` and exits 0. Control: the same line added to
  `dist/script/docker/lib/hook.sh` produces `SC2086 (info)` and a non-zero exit.
- CI shares the hole rather than backstopping it:
  `.github/workflows/self-test.yaml:283` runs that same
  `./script/test/test.sh --shellcheck-only`, and a whole-repo grep finds no
  second target list (the other two hits are a consumer's `/lint/*.sh` pass and a
  version probe).
- Both files really ship: `dist/depl
[...截斷，原長 7250 字]

> 留言 (ycpss91255, 2026-09-08): ## Dependency, not visible in the four `ready-for-agent` sections

Part B's fix depends on getting the exemption set right, and this issue's own text says where that set comes from: `test.sh:455-466` keeps four lints (nesting-depth, function-length, positional-params, shell-metrics) deliberately out of `_LINT_TOOLS` because their population comes from the git index while `_LINT_TOOLS` runs inside 
[...截斷，原長 1067 字]


### #1114 [OPEN] fix(ci): each of the twelve coverage shards looks the weights cache up separately, so the partition may not be one
labels: bug, ready-for-agent

## The defect

`self-test.yaml:876-889` restores `test/bats/.shard-weights` with
`key: shard-weights-${{ github.run_id }}` plus `restore-keys: shard-weights-`.
The only writer is the coverage-gate step (`:983-992`), using the same run-id key,
only on a push to main, and only **after** coverage has run.

So the exact key can never hit while this run's shards are executing. All 12
shards fall through to the **prefix** lookup, and each issues its own lookup when
its own job starts.

`script/test/drivers/bats.sh:303-360` recomputes the **entire** greedy-LPT
partition from `_spec_weight` on every invocation and prints only the slice it
was asked for. The union of those twelve slices is a partition **only if all
twelve read an identical blob**.

## Evidence

- `self-test.yaml:876-889` (restore), `:983-992` (the sole write). `.gitignore:33`
  keeps the file out of the tree, so the cache blob is the only input.
- `bats.sh:303-360` (full recompute per call), `:217-236` (`_spec_weight`, which
  falls back to counting `@test` when the file is unreadable).
- Reproduced for real against the real repo and the real functions: shards 1-6
  with no weights file (falling back to `@test` counts) and shards 7-12 with a
  synthetic seconds file, over a population of 176 files, produce a union of 127
  distinct specs -- **49 specs in zero shards** and 49 run twice. Every slice was
  non-empty, so `_die ci_empty_shard` (`bats.sh:355`) never fires.
- No detector: `coverage_gate.sh:213-236`'s `_merge
[...截斷，原長 4724 字]


### #1115 [OPEN] fix(test): six mutations that ship green because the guard never observes the property
labels: bug, ready-for-agent

## The pattern

Six mutations were applied to production code, the suite was run, and it stayed
green. Every one of these was measured, not reasoned about: the work was done on a
detached worktree of origin/main, reverted afterwards.

Individually none is large. Together they are one shape -- **production and the
guard that is supposed to hold it are unrelated, so either side can move
freely** -- and that shape has already bitten twice (#1032, #1071).

This is the audit's "if you only do three things" item. Related but distinct
buckets already filed: #1090 (guards whose population or subject is declared) and
#1089 (a precondition that turns a guard off). The mechanism here is different:
the guard runs, and never observes the property.

Each section states its own mutation. **The fix is proven by re-applying that
mutation and requiring the suite red.**

---

## 1. The compose and deploy emitters are checked with text only -- 155 greps, no parser (#6)

**Mutation.** Change `dist/script/docker/lib/deploy.sh:568` from
`printf '    privileged: true\n'` to `printf '  privileged: true\n'` -- two
columns less, so the key becomes a service named `privileged`.
`docker compose config` rejects the shape outright
(`services.privileged must be a mapping`). `deploy_spec.bats` stays **66/66
green**, and `network_ports_inert_spec.bats`, `deploy_hint_spec.bats`,
`compose_emit/overlay_guard_spec.bats` and integration's
`deploy_bundle_flow_spec.bats` all report zero failures. The whole deploy-em
[...截斷，原長 22111 字]

> 留言 (ycpss91255, 2026-09-08): ## Item 2 is already done; the live scope is five items, not six

**Item 2 (`just docker setup-tui` Save and Exit has no coverage at all)** was fixed by #1104 (`6cc5dd04`, merged 2026-09-06T07:14Z), 68 minutes before this issue was filed. #1104 carried no closing keyword, so nothing here noticed.

Verified on `origin/main`:

- `_commit_and_setup` is now driven directly by four tests in `test/bats/
[...截斷，原長 2682 字]

> 留言 (ycpss91255, 2026-09-08): ## Item 1 contradicts #1123, which covers the same assertions and prescribes the thing item 1 forbids

#1123 ("refactor(test): replace 155 grep assertions in emitter specs with yq
parser validation") is pointed at item 1's population and prescribes the
opposite guard.

**The overlap is exact, not approximate.**

- Same assertion population: the 155 is
  `grep -c 'run grep\|grep -'` over `test/bats
[...截斷，原長 3795 字]


### #1116 [OPEN] chore(ci): self-test declares no permissions and sets up a builder its only consumer always skips
labels: enhancement, ready-for-agent

## Two workflow-level defects in `self-test.yaml`

Both are low, neither is user-facing, and both are one-file edits in the same
workflow. Filed together because they land in the same place.

---

## A. `self-test.yaml` declares no `permissions:` at all (#26)

Reported independently by two auditors and merged into one finding.

**Defect.** `grep '^permissions:'` over `.github/workflows/` finds a
workflow-level block in coverage-local, ghcr-cleanup, release-test-tools,
tool-version-watch and triage-label. `self-test.yaml` has none. Of its 16 jobs
only two declare their own (`worker-selftest` `:1581`, `contents: read`;
`release` `:1736`, `contents: write`); the other 14 inherit the repository
default. The posture is correct today -- both the repo and the org report
`{"default_workflow_permissions":"read"}` -- but that correctness is held
entirely by a UI setting, and nothing in the tree asserts it.

**Evidence.**

- `self-test.yaml`'s top level is only `name`, `on:10`, `concurrency:66`,
  `env:70`, `jobs:75`. No `permissions:`.
- The tree's least-privilege guard,
  `test/bats/unit/reusable_worker_permissions_spec.bats:205-231`, draws its
  population from `reusable_workflow_files` -- workflows whose `on:` declares
  `workflow_call` -- so `self-test.yaml` is outside it by construction.
- `grep -n permission test/bats/unit/self_test_yaml_spec.bats` (2188 lines, 116
  assertions) returns nothing. `ci_spec.bats`'s permission hits are all
  `_fix_permissions` (chown), unrelated.
- T
[...截斷，原長 7817 字]


### #1117 [OPEN] refactor(test): four families that restate what a sibling already proves, and one that proves nothing
labels: enhancement, ready-for-agent

## Context: the ratio table this comes from

The audit measured every test family as tests divided by distinguishable
properties (a property = one production decision a test can tell apart), using
timings from CI run `34013117272` (main, all green, 2026-09-06; 3980 tests
timestamped, median 490 ms per test).

| family | files | tests | properties | tests per property |
|---|---|---|---|---|
| wrapper i18n | 6 | 50 | 18 | **2.78** |
| `run.sh` xhost branch | 4 | 13 | 4 | **3.25** |
| wrapper CLI surface | 8 | 124 | 41 | 3.02 |
| CI-workflow YAML specs | 9 | 309 | ~214 | 1.44 |
| TUI | 5 | 298 | ~247 | 1.21 |
| upgrade/init | 5 | 240 | ~206 | 1.17 |
| compose/env emission | 7 | 177 | ~155 | 1.14 |
| lint-driver | 28 | 707 | ~556 | 1.27 |

**The table is mostly healthy.** Every family except the first two sits between
1.1 and 1.5. So this issue is about **signal, not wall clock** -- the time saved
by all four items below is under a second of critical path, and the cost argument
should not be used to justify any of them.

Four items, all measured by mutation.

---

## 1. wrapper i18n: 20 tests share one assertion token that cannot tell the locales apart (#19)

**Defect.** The zh-TW and zh-CN usage heredocs both **begin with the same two
characters** meaning "Usage" (`dist/script/docker/wrapper/stop.sh:34` and `:54`;
same in `build.sh:73/:124`, `run.sh:107/:150`, `exec.sh:62/:101`,
`prune.sh:72/:138`). Every zh-CN test asserts exactly that token, byte-identical
to its zh-TW siblin
[...截斷，原長 15722 字]


### #1118 [OPEN] fix(setup): the shipped tree tells users to run two commands they do not have, and drops three log bodies
labels: bug, ready-for-agent

## Two defects in the shipped lib, at the moment the user is looking at it

Both live in `dist/script/docker/lib`, both reach every downstream repo, and both
are one-line-per-site fixes plus a cheap derived check and a spec that is
currently pinning the wrong thing.

---

## A. Four `next:` hints name two commands a consumer does not have (#16)

**Defect.** `setup_cmd.sh:305`, `:727`, `:897` and `:1003` all print:

```
[setup] next: run 'just build' (auto-applies) or './setup.sh apply' to regenerate .env / .env.generated / compose.yaml
```

Neither command exists in a dist-era consumer.

**Evidence.**

- Verified by running it: after sourcing
  `dist/script/docker/wrapper/setup.sh`,
  `main set --base-path <tmp> build.arg_4 ROS2_DISTRO=jazzy` prints that line
  verbatim.
- There is no top-level `just build`: the shipped entry justfile defines only
  `default` plus four modules (`dist/script/justfile:15-32`), and
  `justfile.docker:7` says so outright ("no top-level `just build`").
  Reconstructing the consumer symlink layout and running `just build` gives
  `error: justfile does not contain recipe 'build'`. `script/local/justfile.local`,
  as written by `init.sh:277-293`, contains only comments.
- There is no root `./setup.sh`: it is listed in `_init_retired_root_paths`
  (`init.sh:937`) and deleted by the resync loop (`init.sh:115-121`). A real
  consumer checkout has no root `setup.sh`, only `script/setup.sh`.
- **Tests are protecting the wrong string.**
  `test/bats/unit/s
[...截斷，原長 6722 字]


### #1119 [OPEN] fix(gitignore): a gitignore pattern is handed to git as a pathspec and the fatal is swallowed
labels: bug, ready-for-agent

## The defect

`_untrack_canonical_in_repo` strips only the **trailing** slash
(`gitignore.sh:472`, `_path="${_entry%/}"`) and hands the result to
`git ls-files -- "${_path}"` with stderr swallowed (`:475`). The one entry in the
canonical set (`gitignore.sh:34-47`) with a leading slash, `/deploy/`, therefore
becomes the pathspec `/deploy`, and git fails outright.

## Evidence

- Verified live (git 2.55.0, a temp repo tracking `deploy/a`, `log/b`,
  `coverage/c`, `compose.yaml`): the function untracks three and leaves
  `deploy/a`. Running `git ls-files -- /deploy` directly gives
  `fatal: /deploy: '/deploy' is outside repository`, exit 128.
- `2>/dev/null` swallows the fatal, `[[ -n ... ]]` is false, and the entry is
  skipped silently.
- The spec is roster-shaped: `test/bats/unit/gitignore_spec.bats:458` is titled
  "untracks **all** canonical entries that match" and names four.
- **A second, opposite mismatch:** `log/` and `coverage/` are **unanchored**
  gitignore patterns, so they ignore `sub/log/` too, but the derived pathspec
  matches from the repo root and does not match a nested copy. Force-adding
  `sub/log/z` and `sub/coverage/z` and re-running leaves both in the index. So 3 of
  12 canonical entries are treated incorrectly.
- The same defect exists symmetrically in `_init_snapshot_index`
  (`init.sh:981-990`).

## Why it matters -- today, it does not

The original narrative (a repo committed a bundle before the entry existed, and
this is the only remedy) was overt
[...截斷，原長 3950 字]


### #1120 [OPEN] fix(build): an unrecognised leading-dash token becomes the build target
labels: bug, ready-for-agent

## The defect

`dist/script/docker/wrapper/build.sh`'s argument loop ends with
`*) TARGET="$1"` (`build.sh:416-418`), so **any** unrecognised token -- including
one starting with a dash -- becomes the build target. A typo such as
`./build.sh --no-cahce` asks compose to build a service literally named
`--no-cahce`.

## Evidence

Verified by running the wrapper against a tree extracted from origin/main:

- `--dry-run --stage test-tools` emits `docker compose ... build test-tools`. Wrong
  flag, right result, exit 0 -- because `--stage` is swallowed as TARGET and then
  overwritten by `test-tools` (last one wins).
- `--dry-run --stage` with no value emits `docker compose ... build --stage`, plus
  `docker rmi <old-id-of local/local:--stage>`, and the wrapper reports **no
  error**.
- `--stage devel --target runtime` yields `build runtime`; the reverse order yields
  `build devel`. Undocumented last-one-wins.

`build.sh` is the only one of the four wrappers that fails open this way, and the
contrast is what makes it a defect rather than a convention: `run.sh:468` and
`exec.sh:295` **break** out of the loop to do CMD pass-through, and `stop.sh:216`
forwards the remainder to `docker compose down`. All three are deliberate, because
they accept a command or pass-through. `build.sh` captures the token as a **named
target** instead.

## Why it matters

This is a PRD invariant 2 item -- a wrong input accepted silently and turned into
a different action. A mistyped flag becomes a build o
[...截斷，原長 3185 字]


### #1121 [OPEN] docs: five README and doc statements the tree contradicts
labels: documentation, ready-for-agent

## Five documentation statements the tree contradicts

All five were verified against the code or the renderer. None has a behavioural
effect; all five are read by someone deciding what to do next. Grouped because the
fix is the same class of work and three of them need the same
`just test sync-readme` re-stamp of the three translations.

---

## 1. The README "What's included" table is broken in half, and 12 rows render as literal pipes (#20)

**Defect.** `README.md:140` (`| File | Description |`) plus the separator at `:141`
opens a table that runs to `:177`. `:179-187` inserts a paragraph ("Test content
is laid out **tool-first** ..."). The table then continues at `:189-200` with **12
more rows and no header and no separator row**.

**Evidence.**

- POSTing `README.md:138-200` to GitHub's own markdown API
  (`gh api -X POST /markdown`, mode gfm) returns exactly **one** `<table>`, and
  those 12 rows come back as
  `<p dir="auto">| <code>.hadolint.yaml</code> | Shared Hadolint rules |<br>...` --
  literal pipe characters, from GitHub itself. python-markdown with the tables
  extension agrees.
- The 12 affected rows are the entry-point documentation: `justfile` (pointing at
  `script/justfile`), the `docker` and `base` namespace rows,
  `dist/script/base/init.sh`, `dist/script/base/upgrade.sh`,
  `script/test/justfile.test`, `script/release/justfile.release`,
  `script/watch/justfile.watch`, `dist/dockerfile/Dockerfile`,
  `dockerfile/Dockerfile.test-tools`, `.github/workflo
[...截斷，原長 18817 字]


### #1122 [OPEN] fix(ci): test-tools image version has two independent sources of truth
labels: ready-for-agent

## Problem

The test-tools image version has two independent sources of truth:

1. build-worker.yaml input `test_tools_version` (default: `latest`)
2. The GHCR registry (published tags matching base releases)

15 of 19 downstream repos use the default `latest`, meaning they consume
whichever image was most recently published rather than the version matching
their pinned `.base/.version`. The `@ref` on the `uses:` line already pins
the base version, but the test-tools image consumed during build is decoupled.

ADR-00000002 exempts output images from the pin-to-immutable rule, but the
exemption was written before upgrade.sh could automate pinning. Now that it
can, the exemption creates a needless drift vector.

## Decision (from grilling 2026-09-06)

**Option A**: Remove the `test_tools_version` input entirely. Hardcode the
version inside build-worker.yaml itself. The release flow updates it when
cutting a release (same mechanism that updates the workflow file on disk).

This makes the version source singular: the build-worker.yaml file, which
travels with the `@ref` tag.

## Fix

1. In build-worker.yaml: replace `test_tools_version` input with a hardcoded
   env or local variable set to the current version
2. In upgrade.sh: remove any sed that rewrites `test_tools_version` in
   downstream main.yaml (there is none today, but prevent future addition)
3. In the release flow: add a step that updates the hardcoded version in
   build-worker.yaml before tagging
4. Amend ADR-0000000
[...截斷，原長 1854 字]


### #1123 [OPEN] refactor(test): replace 155 grep assertions in emitter specs with yq parser validation
labels: ready-for-agent

## Problem

The compose and deploy emitter test suites use 155 grep assertions and zero
parser-based validation. Both yq and docker compose are available in the test
image but unused by these specs.

A mutation that produces syntactically invalid YAML (e.g. wrong indentation
that makes a key appear as a top-level service name instead of a nested
property) passes all 66 deploy tests and all 83 compose gen tests. The same
repo's workflow-permission specs already use yq with documented rationale:
"parser buys two properties grep cannot express: the key is at the correct
level, and the value is the complete value."

## Decision (from grilling 2026-09-06)

Full replacement (Option B), using /tdd approach:

1. **Phase 1 (red)**: Add a smoke guard that runs `docker compose config`
   on every emitter output path. This single test catches the entire class
   of "syntactically broken YAML that grep cannot see." It will fail on
   the indentation mutation described above, proving the gap.

2. **Phase 2 (green)**: Replace grep assertions with yq queries, one spec
   file at a time. Priority order:
   - deploy_spec.bats (66 tests, highest severity mutation)
   - gen_spec.bats (83 tests, 155 greps)
   - overlay_guard_spec.bats, blocks_spec.bats, hostname_spec.bats

3. **Phase 3 (refactor)**: Remove the private awk extractors that specs use
   to work around grep limitations (gen_spec.bats:372, :403, :538).

## Scope

- compose_emit/ specs: gen, blocks, hostname, overlay_guard
- deploy_spe
[...截斷，原長 1845 字]

> 留言 (ycpss91255, 2026-09-08): ## Sequence this after #1148, and it is an ordering hazard rather than a blocker

Nothing here is blocked by a missing file: all eight target specs exist on `origin/main` (`compose_emit/{gen,blocks,hostname,overlay_guard}_spec.bats`, `deploy_spec.bats`, `setup_cmd_spec.bats`, `compose_logging_spec.bats`, `compose_watchdog_spec.bats`). The hazard is a moving target.

**Open PR #1148 (`feat/toml-con
[...截斷，原長 2865 字]

> 留言 (ycpss91255, 2026-09-08): ## This contradicts #1115 item 1, which covers the same assertions and forbids Phase 1

#1115 item 1 ("The compose and deploy emitters are checked with text only --
155 greps, no parser") and this issue are pointed at the same population and
prescribe opposite things.

**The overlap is exact, not approximate.**

- Same assertion population: the 155 is
  `grep -c 'run grep\|grep -'` over `test/bats
[...截斷，原長 3804 字]


### #1126 [OPEN] tracking: Docker CLI coverage through the just recipe layer
labels: enhancement

Long-lived tracking issue. Measures how much of the Docker / Docker
Compose CLI surface base covers through the just recipe layer.

Baseline snapshot taken 2026-09-06 against Docker Engine 27.x /
Compose v2.32+.

## Current state

| Category | Official | Used internally | Has just recipe |
|---|---|---|---|
| Container commands | 25 | 11 (44%) | 5 (20%) |
| Image commands | 13 | 6 (46%) | 2 (15%) |
| Compose subcommands | 30 | 8 (27%) | 4 (13%) |
| **Total** | **68** | **25 (37%)** | **11 (16%)** |

## Tier 1 -- daily development workflow (should have just recipe)

These are commands a developer reaches for every day. Missing a just
entry means falling back to raw docker, which breaks the
single-control-surface principle.

- [ ] `docker compose logs` -- view container output (deploy.sh has it
  internally; no just entry for general use)
- [ ] `docker compose ps` -- list containers in the project (internal
  only, no just entry)
- [ ] `docker compose pull` -- pull updated service images before build
- [ ] `docker compose restart` -- restart without full down/up cycle
- [ ] `docker compose top` -- show running processes inside container
- [ ] `docker logs` -- view logs of a specific container (not just the
  compose project)
- [ ] `docker ps` -- list all containers (internal only in stop.sh)
- [ ] `docker inspect` -- low-level info (internal only, useful for
  debugging)
- [ ] `docker stats` -- live resource usage (CPU / memory / network)
- [ ] `docker kill` -- force-stop a hun
[...截斷，原長 4904 字]


### #1127 [OPEN] epic: TOML config format unification (ADR-37)
labels: enhancement

Epic tracking the TOML config format unification (ADR-00000037).

Replaces the current INI `.setup.conf` + flat `.env.local` pipeline
with four TOML files split by service boundary, type-aware merge
semantics, and a containerised TOML parser (`toml-bridge`).

## Architecture reference

- Decision: `doc/adr/00000037-toml-config-format-unification.md`
- Visual: `doc/arch/overview.html`
- Convention: `doc/adr/00000038-architecture-diagrams-in-doc-arch.md`

## Baseline (2026-09-06)

| Component | Size | Key file |
|---|---|---|
| INI tokenizer + accessors | 747 lines, 18 functions | conf.sh |
| Template .setup.conf | 322 lines, 15 sections | dist/.setup.conf |
| Compose emitter | 1,476 lines, ~30 helpers | compose_emit.sh |
| Env emitter | 445 lines, 4 functions | env_emit.sh |
| Overlay/merge (section-replace) | 70 lines | `_conf_load_layers()` |
| TUI | 2,930 lines, 16 `_edit_section_*` | setup_tui.sh |
| Files referencing .setup.conf | 24 files | across dist/ |
| Existing migration functions | 36 `_migrate_*` | 2,233 lines |

## Dependency chain

```
D9  containerised TOML parser (toml-bridge + vendored tomli)
 └─> D3  conf.sh -> TOML parser bridge
      ├─> D4  type-aware merge (scalar key-level, array replace)
      ├─> D8  [environment] service boundary split
      ├─> D1  .setup.conf -> setup.toml + setup.local.toml
      │    └─> D5  compose_emit.sh reads TOML
      ├─> D2  .env.local -> .env.toml + .env.local.toml
      │    └─> D6  env_emit.sh reads TOML
      └─> D7  2
[...截斷，原長 5499 字]

> 留言 (ycpss91255, 2026-09-06): ## Grilling Q8 decision: section structure reorganization

### Question

setup.toml's 15 sections are TUI-oriented (each maps to a `_edit_section_*` screen). From Docker's perspective, these categories don't exist — compose spec has its own field structure. Should the TOML migration also reorganize sections to align with Docker?

### Decision: phased approach (option C)

**Phase 1 (this epic, D1-D
[...截斷，原長 1432 字]


### #1133 [OPEN] D2: migrate .env.local to .env.toml + .env.local.toml (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** mechanical (once D3/D8 are done).

## What

Migrate `.env.local` (flat KEY=VALUE) to `.env.local.toml` (typed
TOML). Create new `.env.toml` for committed service env defaults.

## Current state

- `.env.local`: operator overrides, gitignored, flat KEY=VALUE
- `.env`: generated defaults (from setup.conf [environment] +
  [lifecycle] watchdog), committed to .gitignore
- `.env.generated`: interpolation cache, never enters container

## Target state (ADR-37)

| File | Purpose | Committed |
|---|---|---|
| `.env.toml` | Service runtime env defaults | Yes |
| `.env.local.toml` | Operator service env overrides | No (gitignored) |

## Acceptance criteria

- [ ] `.env.toml` template with typed service env sections
- [ ] `.env.local.toml` replaces `.env.local` for operator overrides
- [ ] Generated `.env` output unchanged (combines setup.toml infra
  env + .env.toml service env)
- [ ] `_scaffold_env_local()` updated to create `.env.local.toml`

## Blocked by

D3, D8.

## Blocks

D6 (env_emit reads TOML).



### #1134 [OPEN] D5: update compose_emit.sh to read TOML (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** mechanical.

## What

Update compose_emit.sh (1,476 lines, ~30 emitter helpers) to read
from TOML accessors instead of INI conf.sh accessors. Output
(compose.yaml) is unchanged.

## Scope

- `generate_compose_yaml()` (line 1013, 31 positional parameters)
  currently receives values from `_conf_get` calls on the INI handle
- All `_emit_*_block` / `_emit_*_line` helpers that read config
- `_emit_env_file_block()` needs update for the new .env.toml path

## Acceptance criteria

- [ ] compose_emit.sh reads from TOML parser API (D3)
- [ ] Generated compose.yaml is byte-identical to current output
  given the same config values
- [ ] All ~30 emitter helpers updated
- [ ] No residual `_conf_get` calls on INI handles

## Blocked by

D1 (setup.toml must exist), D3 (TOML parser bridge).

## Blocks

D7 (reference cleanup).



### #1135 [OPEN] D6: update env_emit.sh to read TOML (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** mechanical.

## What

Update env_emit.sh (445 lines, 4 functions) to read from TOML
accessors instead of INI conf.sh accessors. Output (.env /
.env.local / .env.generated) is unchanged.

## Scope

- `write_env()`: generates .env.generated (drift metadata)
- `write_container_env()`: generates .env from [environment] +
  [lifecycle] watchdog -- now reads from both setup.toml (infra env)
  and .env.toml (service env)
- `_scaffold_env_local()`: creates .env.local.toml (new format)
- `_migrate_env_to_local()`: may need update for .env.local.toml

## Acceptance criteria

- [ ] env_emit.sh reads from TOML parser API (D3)
- [ ] Generated .env merges setup.toml infra env + .env.toml service
  env (the service boundary split from D8)
- [ ] .env.generated format unchanged
- [ ] No residual `_conf_get` calls on INI handles

## Blocked by

D2 (.env.toml must exist), D3 (TOML parser bridge).

## Blocks

D7 (reference cleanup).



### #1136 [OPEN] D7: clean up 24-file .setup.conf reference list (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** mechanical.

## What

Clean up all 24 files under dist/ that reference `.setup.conf` by
string literal. Each reference must be updated to the TOML filename
or removed if the reference is to INI-specific logic.

## File list (2026-09-06 baseline)

1. upgrade.sh
2. compose.sh
3. .refute_probe.sh
4. conf.sh
5. env.sh
6. dockerfile_migrate.sh
7. resolve.sh
8. init.sh
9. wrapper.sh
10. transcript.sh
11. gitignore.sh
12. setup_cmd.sh
13. schema.sh
14. setup_conf_migrate.sh
15. setup_conf.sh
16. env_emit.sh
17. drift.sh
18. deploy.sh
19. build.sh
20. stage.sh
21. compose_emit.sh
22. config_summary.sh
23. setup_detect.sh
24. setup.sh (wrapper)

Plus setup_tui.sh (frozen, tracked separately).

## Acceptance criteria

- [ ] `grep -r '.setup.conf' dist/` returns zero hits (excluding
  migration/compat code gated behind version checks)
- [ ] Each file tested after migration
- [ ] No functional regression in compose.yaml / .env generation

## Blocked by

D1, D2, D5, D6 (all input/output paths migrated first).

## Blocks

D10 (downstream migration -- needs stable TOML interface).



### #1137 [OPEN] D10: downstream one-time INI-to-TOML migration converter (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** needs design discussion.

## What

One-time migration converter for downstream repos:
- `.setup.conf` -> `setup.toml`
- `.setup.conf.local` -> `setup.local.toml`
- `.env.local` -> `.env.local.toml`

Runs during the first `init.sh` resync after base upgrade, gated
on file existence (same pattern as the `.env -> .env.local`
migration in ADR-00000003's 2026-08-26 amendment).

## Design questions

1. Where does the converter live? Recommend: `init.sh` inline
   (like existing `_migrate_env_to_local`), calling the Python
   TOML writer for output.
2. Is the conversion lossy? INI comments are lost (TOML gets new
   comments). Numbered-key ordering is preserved by array order.
3. Rollback: keep `.setup.conf.bak` for one upgrade cycle?

## Existing migration precedent

36 `_migrate_*` functions already exist (2,233 lines). The pattern
is well-established: detect old state, transform, gate on file
existence, idempotent.

## Acceptance criteria

- [ ] Converter handles all 15 INI sections
- [ ] Numbered keys correctly become `[[array of tables]]`
- [ ] [environment] split applied (infra vs service per D8)
- [ ] Tested on >= 3 real downstream repos
- [ ] Idempotent (running twice is safe)
- [ ] Old files backed up (`.setup.conf.bak`)

## Blocked by

D7 (stable TOML interface on base side).

## Blocks

Nothing -- this is the leaf of the dependency chain.


> 留言 (ycpss91255, 2026-09-06): ## Grilling Q7 decision: downstream INI-to-TOML converter

### Decision

Auto-conversion in init.sh, same pattern as the `.env` -> `.env.local` migration (ADR-3 amendment).

### Mechanism

1. **Trigger:** init.sh resync detects `.setup.conf` exists but `setup.toml` does not
2. **Converter:** `docker run --rm -v "$PWD:/w" toml-bridge:pinned convert /w/.setup.conf /w/setup.toml`
3. **On success:** `
[...截斷，原長 1039 字]


### #1138 [OPEN] D11: TOML config schema validation (refs #1127)
labels: enhancement

Part of #1127 (TOML config format unification epic).
**Type:** needs design discussion.
**Not on critical path** -- do after D10 (#1137).

## What

Define a JSON Schema (or TOML-native validation) for the TOML
config files (setup.toml, .env.toml). Validates which tables/keys
are legal, their types, and constraints.

## Why

ADR-37 Consequences: "JSON Schema validation of the parsed TOML
structure (as practiced by the config-manager project, sec. 6.2)
is a natural follow-up but not part of this decision."

Without schema validation, a typo in a key name
(`[newtork]` instead of `[network]`) silently produces a default
value instead of an error. The current INI format has the same
problem; TOML + schema eliminates it.

## Precedent

config-manager design document (v0.16) uses JSON Schema for its
`config-list.toml`. The same approach applies here.

## Scope

- Define schema for setup.toml (15 sections -> TOML tables/arrays)
- Define schema for .env.toml (service env sections)
- Validation runs during `just setup` / compose generation
- IDE support: schema enables TOML language server completion

## Blocked by

D10 (#1137) -- stable TOML format must exist first.



### #1149 [OPEN] fix(test-tools): kcov binary is musl-linked and cannot execute on Ubuntu/glibc downstreams
labels: needs-triage

## Context

Base's test-tools image (`ghcr.io/ycpss91255-docker/test-tools`) ships kcov v43
compiled on Alpine (musl libc). Downstream repos whose `devel-test` stage is
Ubuntu-based (glibc) cannot execute the binary:

```
/usr/local/bin/kcov: cannot execute: required file not found
```

The binary links to `ld-musl-x86_64.so.1`, which does not exist on Ubuntu.

Affected downstreams: `omniverse_web_viewer` (FROM ubuntu:24.04).
Unaffected: `realsense_ros1`, `realsense_ros2`, `isaac` -- these repos COPY
shellcheck/hadolint/bats from test-tools but never COPY kcov.

shellcheck and hadolint are unaffected because they are downloaded as static
binaries from upstream GitHub releases. bats is a pure bash script. kcov is the
only tool compiled from source inside the Alpine image.

## Verification

```bash
# On host (linux/amd64)
docker run --rm ghcr.io/ycpss91255-docker/test-tools:latest \
  ldd /usr/local/bin/kcov | head -1
# Output: /lib/ld-musl-x86_64.so.1

docker run --rm ubuntu:24.04 bash -c "
  apt-get update -qq >/dev/null 2>&1
  # copy kcov from test-tools into ubuntu
  echo 'ld-musl-x86_64.so.1 does not exist on ubuntu:24.04'
"
```

## Workaround (owv)

owv will build kcov from source inside an Ubuntu-based builder stage
(`FROM ubuntu:24.04 AS kcov-builder`) and COPY the glibc-linked binary.
This adds ~90s build time and duplicates the kcov build.

## Proposed fix

One of:

1. **Static link**: build kcov with `-static` or `-DBUILD_SHARED_LIBS=OFF`
   in the existing Alpine kc
[...截斷，原長 2166 字]


### #1150 [OPEN] feat(ci): publish toml-bridge image to GHCR for downstream reuse
labels: enhancement

## Context

The multi_run rebuild (#26 in multi_run) requires a containerised
Python + tomllib environment for its assembly phase — parsing
`.multi.toml` and emitting an invocation plan.

base already ships `dockerfile/Dockerfile.toml-bridge` (Python 3.13
alpine + vendored tomli), used locally as `toml-bridge:local`. The
image is also embedded in test-tools via a multi-stage copy, and
test-tools is published to GHCR — but the full test-tools image is
far too heavy for just TOML parsing.

## Problem

multi_run needs a Python 3.11+ container base image. Current options:

1. Maintain its own `FROM python:3.13-alpine` — duplicates base's
   existing image, Python version drifts independently
2. `FROM toml-bridge:local` — implicit dependency on base being
   built locally first
3. `FROM ghcr.io/.../test-tools` — too heavy

None are satisfactory.

## Proposal

Publish `dockerfile/Dockerfile.toml-bridge` output to GHCR:

- Image: `ghcr.io/ycpss91255-docker/toml-bridge`
- Publish on tag/release via existing CI or a new lightweight workflow
- Downstream consumers (multi_run) can then
  `FROM ghcr.io/ycpss91255-docker/toml-bridge` and COPY their own
  Python modules in, without maintaining a Python version pin

## Acceptance criteria

- [ ] `ghcr.io/ycpss91255-docker/toml-bridge` is pullable
- [ ] Image contains Python 3.11+ with tomllib (stdlib) / tomli
      (vendored fallback)
- [ ] multi_run can `FROM` this image and successfully
      `import tomllib`

## Out of scope

- multi_run
[...截斷，原長 1645 字]


### #1152 [OPEN] docs: record setup.toml parameter creation gate (ADR-37 follow-up)
labels: documentation, enhancement

## Context

During the TOML config format unification work (ADR-37), a full audit of every
`setup.toml` key was performed. The audit confirmed that all existing parameters
pass a two-criteria gate, but the gate itself is not recorded anywhere. This
issue tracks writing it down so future contributors apply the same bar.

## Principle

Every key in `setup.toml` must satisfy **one** of two criteria:

1. **Docker compose spec mapping** -- the key directly maps to a field in the
   Docker Compose specification (e.g. `restart`, `privileged`, `shm_size`,
   `logging.driver`). These keys use bare section names that mirror the compose
   structure.

2. **Base extension with auto-detect default** -- the key controls base-specific
   orchestration logic that has no compose equivalent, but its default value is
   `auto` (or empty = auto-derived), so the common case requires zero
   configuration. The config knob exists solely as an escape hatch for edge
   cases (e.g. `force`/`off` overrides). These keys live under the `[base.*]`
   namespace.

Pure convenience parameters -- knobs that exist only to save the user a step
that could be handled automatically -- are **not accepted**. If it can be
derived, derive it; if the override is never needed, don't ship the knob.

## Current audit classification

### Docker-native (bare section names)

| Section | Keys |
|---------|------|
| `[build]` | `target_arch`, `network` |
| `[build.args]` | flat table: `KEY = "value"` (e.g. `APT_MIRROR_UBUNTU`,
[...截斷，原長 4325 字]


### #1153 [OPEN] feat: show resolved config summary with auto-detect diff before build
labels: enhancement

## Problem

All `auto` mode resolve functions silently change behavior based on host
detection. The user has no visibility into what was detected, what decision
was made, or how to override.

For example, on Jetson `build.network = auto` silently resolves to `host`
with zero log output. The L4T kernel lacks iptables modules for bridge NAT
(compiled out, not installable), so the switch is correct -- but invisible.

The resolve functions involved:

| Function | File | Logging |
|---|---|---|
| `_resolve_build_network` | `resolve.sh:130` | **none** |
| `_resolve_gpu` | `resolve.sh:25` | **none** |
| `_resolve_runtime` | `resolve.sh:100` | **none** |
| `_resolve_gui` | `resolve.sh:42` | **none** |
| `_detect_dri_groups` | `resolve.sh:74` | **none** |

All five are pure resolvers that write to an output variable via nameref
and produce no user-visible output.

## Affected auto-detect parameters

- `build.network`: `auto` -> `host` on Jetson (L4T kernel lacks iptables
  modules for Docker bridge NAT)
- `deploy.gpu_mode`: `auto` -> `true` when `nvidia-container-toolkit`
  detected via dpkg
- `deploy.gpu_runtime`: `auto` -> `nvidia` on Jetson (csv-mode toolkit
  requires explicit runtime)
- `deploy.dri_groups`: `auto` -> host `/dev/dri` GIDs for Intel/AMD iGPU
  hardware GL
- `gui.mode`: `auto` -> `true` when `$DISPLAY` or `$WAYLAND_DISPLAY`
  present

## Proposed solution

Show a **resolved config summary** at a visible stage (before build, or
during `just setup`) that presents a di
[...截斷，原長 2751 字]


### #1154 [OPEN] test: comprehensive input validation for all setup.toml parameters
labels: enhancement

## Problem

Each `setup.toml` parameter accepts specific values (e.g. `auto`/`force`/`off`, empty/non-empty, numeric ranges, regex patterns), but not all valid/invalid input combinations are tested. Missing coverage means invalid config can silently produce wrong compose output or crash at runtime.

## Scope

Every parameter in `setup.toml` must have tests covering:

1. **All documented valid values** (e.g. `gpu_mode`: `auto`, `force`, `off`)
2. **Edge cases**: empty string, missing key (inherits default), whitespace
3. **Invalid values**: wrong type, out-of-range, typos -- must produce a clear error, not silent misbehavior
4. **Auto-detect parameters** (`gpu_mode`, `gpu_runtime`, `dri_groups`, `gui.mode`, `build_network`): mock the detection source and verify the resolved value matches expectations

## Parameters to cover

### base extensions

| Parameter | Valid inputs | Notes |
|-----------|-------------|-------|
| `base.project.name` | empty (auto-derive), explicit string | |
| `base.image.rules[].rule` | `prefix:<str>`, `suffix:<str>`, `@basename` | Also: empty array, invalid syntax |
| `base.build.build_network` | `auto`, `host`, `bridge`, `none`, `default`, `off` | Auto-detect: mock Jetson via `SETUP_DETECT_JETSON` |
| `base.build.target_arch` | empty, architecture string (e.g. `arm64`, `amd64`) | |
| `base.deploy.gpu_mode` | `auto`, `force`, `off` | Auto-detect: mock `nvidia-container-toolkit` |
| `base.deploy.gpu_count` | `"all"`, numeric string | |
| `base.deploy.gp
[...截斷，原長 3973 字]


### #1155 [OPEN] refactor: rename DOCKER_HUB_USER to USER_NAME -- misleading variable name
labels: enhancement

## Problem

`DOCKER_HUB_USER` implies the value always comes from Docker Hub, but the actual detection logic (`detect_docker_hub_user()` in `dist/script/docker/lib/setup_detect.sh`) has a 3-tier fallback:

1. `docker info` Username field (Docker Hub login)
2. `$USER` (OS local username) -- when no Docker Hub login exists
3. `id -un` -- when `$USER` is unset

On machines without Docker Hub login (common in CI, air-gapped environments, local dev), the value is the OS username, not a Docker Hub user. The current name is misleading.

## Proposed change

- Rename `DOCKER_HUB_USER` to `USER_NAME` (or similar) across the codebase
- Rename `detect_docker_hub_user()` to `detect_user_name()`
- Update `.env.generated` output: `USER_NAME=<value>`
- Update all consumers: image tagging (`<user>/<image>:<tag>`), project name derivation, config summary, compose project name reconstruction
- Document the 3-tier detection logic clearly in the function comment

## Affected files

- `dist/script/docker/lib/setup_detect.sh` -- detection function definition
- `dist/script/docker/lib/env_emit.sh` -- writes `DOCKER_HUB_USER=` to `.env.generated`
- `dist/script/docker/lib/compose.sh` -- project name derivation uses `DOCKER_HUB_USER`
- `dist/script/docker/lib/setup_cmd.sh` -- orchestrator passes value through
- `dist/script/docker/wrapper/run.sh` -- image tagging: `${DOCKER_HUB_USER}/${IMAGE_NAME}:${TARGET}`
- `dist/script/docker/lib/deploy.sh` -- deploy image tagging
- `dist/script/docker/lib/config_
[...截斷，原長 1882 字]

> 留言 (ycpss91255, 2026-09-07): Clarification on naming convention:

The rename target should be `user_name` (lowercase), not `USER_NAME`:

- setup.toml config keys use lowercase with underscores: `network_name`, `gpu_mode`, `target_arch`
- Function name: `detect_user_name()` (lowercase)
- .env.generated output: follows existing env var convention for that file (to be decided -- may stay uppercase for backward compatibility or a
[...截斷，原長 482 字]

> 留言 (ycpss91255, 2026-09-07): Correction on naming convention:

The rename target for the env variable is `USER_NAME` (uppercase), not `user_name`. The previous comment about lowercase was an error.

- Environment variable in `.env.generated`: `USER_NAME` (uppercase, follows env var convention — same as `IMAGE_NAME`, `BUILD_NETWORK`, etc.)
- Function name: `detect_user_name()` (lowercase, follows shell function convention)
- I
[...截斷，原長 571 字]


### #1156 [OPEN] setup.toml documentation style: enforce behavioral comments, no history, aligned inlines
labels: documentation

## Context

ADR-37 TOML config unification is redesigning the setup.toml structure. Three documentation/style rules were established during design that must be verified during code review of the actual migration PR.

These rules are setup.toml-specific, but the underlying principles (behavioral descriptions over dictionary definitions, no history in code comments) are general code quality standards.

## Rules

### 1. Behavioral descriptions over dictionary definitions

Comments should describe how parameter combinations interact and what behavior they produce together, not define each parameter individually in isolation.

Example: the `[base.deploy]` section should explain that gpu_mode + gpu_runtime + dri_groups together determine the GPU access strategy, not list each parameter's possible values separately.

Bad (dictionary style):
```toml
# gpu_mode: one of nvidia / intel / none
# gpu_runtime: one of nvidia / ...
# dri_groups: comma-separated list of groups
```

Good (behavioral style):
```toml
# GPU access strategy: gpu_mode selects the vendor stack,
# gpu_runtime names the OCI runtime, and dri_groups grants
# /dev/dri access to the listed supplementary groups.
# Set gpu_mode = "none" to disable GPU passthrough entirely.
```

### 2. No historical references in file comments

The file header and section comments describe what the file IS now, not what it replaced or what changed. Historical context (e.g. "replacement for .setup.conf", issue/ADR numbers) belongs in PR bodie
[...截斷，原長 2464 字]


### #1157 [OPEN] feat(stage): replace auto-discovery with explicit opt-in via setup.toml [[stage]]
labels: enhancement

## Problem

Every `FROM ... AS <stage>` in the Dockerfile currently auto-generates a compose service, unless the stage name appears in a hardcoded baseline blocklist (`sys`/`devel-base`/`devel`/`runtime-test`/`base`/`test`). Per-stage property overrides use the `["stage:<name>"]` quoted-table syntax.

Two problems with this:

1. **Default-open**: any new stage automatically generates a service -- users cannot control which stages are exposed, nor silence stages they do not need.
2. **Non-idiomatic TOML syntax**: `["stage:<name>"]` is valid TOML but breaks convention; override keys also use string form (`"gui.mode"`) instead of TOML dotted keys.

## Proposal

Invert the model. `setup.toml` explicitly lists which stages to generate via `[[stage]]` array-of-tables. Only listed stages get compose services. Unlisted stages are not generated.

### New syntax

```toml
[[stage]]
name = "runtime"

[[stage]]
name = "deploy"
gui.mode = "off"
network.mode = "bridge"
```

### Design details

1. `[[stage]]` replaces `["stage:<name>"]` -- standard TOML array-of-tables with a `name` field, not quoted colon table names.
2. Override keys use TOML dotted keys (e.g., `gui.mode`) instead of quoted string keys (e.g., `"gui.mode"`).
3. Top-level config sections (`[base.deploy]`, `[base.gui]`, `[network]`, etc.) are the defaults; per-stage entries inherit and override.
4. Stages NOT listed in any `[[stage]]` entry do NOT get compose services, even if they exist in the Dockerfile.
5. Baseline stages 
[...截斷，原長 2343 字]


### #1158 [OPEN] rename base.log / base.transcript to base.container_log / base.host_log in setup.toml (refs #1127)
labels: enhancement

## Summary

Rename `[base.log]` and `[base.transcript]` in setup.toml to `[base.container_log]` and `[base.host_log]` respectively. The current names are ambiguous -- both sound like "logging" but serve fundamentally different purposes:

- **`[base.container_log]`** (was `[base.log]`) -- container service stdout/stderr retained on host via bind mount
- **`[base.host_log]`** (was `[base.transcript]`) -- host-side wrapper command output (`just build`/`run`/`stop`) transcript

The rename aligns the section names with what each section actually configures (container-side vs host-side), eliminating the confusion between "log" (generic) and "transcript" (non-obvious that it means host-side wrapper output).

## Scope of changes

1. **dist/setup.toml** -- rename the section headers
2. **Shell code that reads these sections** -- `setup_cmd.sh`, `compose_emit.sh`, and any other reader that parses `base.log` or `base.transcript` keys
3. **Schema validation** -- update section name checks in `_tui_conf.sh` or wherever the TOML schema is validated
4. **Tests** -- update all bats fixtures and assertions referencing the old section names
5. **TUI i18n strings** -- update menu labels / descriptions that mention these sections

## Acceptance criteria

- [ ] `[base.log]` no longer appears in dist/setup.toml or any shell source
- [ ] `[base.transcript]` no longer appears in dist/setup.toml or any shell source
- [ ] All tests pass with the new names
- [ ] TUI displays the renamed sections correc
[...截斷，原長 1575 字]


### #1159 [OPEN] change gpu_capabilities from string to TOML array (refs #1127)
labels: enhancement

## Summary

Change `gpu_capabilities` in setup.toml from a space-separated string to a native TOML array.

**Before:**
```toml
gpu_capabilities = "gpu compute utility graphics"
```

**After:**
```toml
gpu_capabilities = ["gpu", "compute", "utility", "graphics"]
```

A TOML array is the idiomatic representation for a list of discrete values. The current space-separated string requires shell-level word splitting to parse, which is fragile and inconsistent with TOML semantics.

## Scope of changes

1. **toml_bridge.py** -- add handling for plain list values. Currently the bridge outputs Python `repr()` for lists, not space-separated strings. Simplest fix: detect list type and `" ".join()`, or add to `_ARRAY_SPEC` so the bridge knows this key produces a list
2. **dist/setup.toml** -- change the default value format from string to array
3. **Schema validation** -- update `_validate_gpu_capabilities` in `_tui_conf.sh` (or equivalent) to accept array input
4. **Tests** -- update fixtures that use the old `"gpu compute utility graphics"` string format

## Acceptance criteria

- [ ] `gpu_capabilities` value in dist/setup.toml is a TOML array
- [ ] toml_bridge.py correctly serializes the array for shell consumption (space-separated output for docker `--gpus` flag)
- [ ] Schema validation accepts the array format and rejects malformed values
- [ ] All tests pass with the new format

## References

- Part of the setup.toml redesign (ADR-37, epic #1127)



### #1160 [OPEN] fix(init): a rolled-back resync leaves the smoke-tree rename staged in the index
labels: bug

## Context

Split out of #1050 / PR #1058, which promised it separate triage.

`_migrate_smoke_tree` (`dist/script/docker/lib/smoke_migrate.sh`) ends by
staging its own rename, so the move rides the caller's upgrade commit:

```
git -C "${_root}" add -A -- test/smoke test/bats/smoke
```

It is called from `_init_existing_repo`, INSIDE the rollback bracket
(`_init_arm_rollback` ... `_init_disarm_rollback`) and before
`_migrate_dockerfile`. The general staging pass #1053 added runs after the
bracket closes, so this is the one stager the rollback can observe.

## Problem

The rollback restores the working TREE (`_init_restore_tree`) and, for the
index, only re-adds entries it recorded being removed
(`_init_restore_index`, sourced from `_canonical_gitignore_entries`). No
path removes an index entry the run ADDED.

So after `_migrate_dockerfile` fails, the working tree is correct -- #1058
made `test/smoke` and `test/bats/smoke` protected roots -- but the index
still describes the migrated shape: `test/smoke/<spec>` staged as deleted,
`test/bats/smoke/shared/<spec>` and the two `.gitkeep`s staged as added,
none of it matching what is on disk.

`git status` nets out to nothing against HEAD, which is what hides it. A
subsequent bare `git commit` commits the INDEX, so the consumer commits a
migration that was rolled back, referencing blobs for files the restore
removed. The rollback's own contract -- "the consumer's files are back as
they were" -- is then true of the tree and false of
[...截斷，原長 2786 字]


### #1162 [OPEN] fix(toml-bridge): --merge always exits 1 and conf.sh swallows it
labels: bug

## Context

On branch `feat/toml-config-unification` (epic #1127), the merge commit
`1567b8d2` ("Merge branch 'main' into feat/toml-config-unification")
resolved the conflict in `dockerfile/toml_bridge.py` by a line-level
union instead of picking a side.

Function inventory of the two parents:

| revision | lines | contents |
|---|---|---|
| `5cc9fb9b` (main side) | 107 | naive `_emit_kv`, `_merge_toml`, `main` |
| `ff53be6a` (feature side) | 108 | `_ARRAY_SPEC`, `_format_value`, `_emit_array`, array-aware `_emit_kv`, `_merge_layers`, `main` |
| `1567b8d2` (merge) | 176 | BOTH merge functions, a duplicated `main()` body, and the feature side's `_emit_kv` body displaced |

The feature side is exactly the shape #1130 (D4: type-aware merge
semantics for TOML layers) landed. After the union the file is the
concatenation of both sides: the D4 type handling is still physically
present but no longer reachable from any live call path. The branch tip
`195b5976` is still 176 lines, so the defect is live, not historical.

This class of failure -- a line-level union merge producing a file that
is the concatenation of both sides -- is the same shape as
previously-recorded incidents in this repo; see #1103 (a merge producing
a duplicate CHANGELOG category heading). What is different here is that
nobody noticed: see the downstream impact under Defect 1.

## Problem

### Defect 1: `--merge` mode always exits 1

In the merged file, `_merge_toml()` (line 69) lost its `return merged`.
Lines 99-
[...截斷，原長 5200 字]


### #1163 [OPEN] release blocker: just upgrade silently disables a downstream operator's .env.local overrides (refs #1127)
labels: bug, needs-triage

Branch: `feat/toml-config-unification` (PR #1148). Epic #1127, ADR-00000037. Sibling defect on the same branch: #1162.

## What an operator sees

A downstream operator has `ROS_DOMAIN_ID=42` in `.env.local`. It works today. They run `just upgrade` onto a release cut from this branch. The upgrade reports success, the container comes up, and the log line says their values "were converted".

Their overrides are no longer applied. Nothing reports the loss, and the one log line that mentions the file says the opposite of what happened.

## The chain, end to end

1. **Works today.** `_emit_env_file_block` (`dist/script/docker/lib/compose_emit.sh:326-331`) lists `- .env` then `- .env.local` under `env_file:`. Later file wins, so the operator's flat dotenv overrides the generated defaults.

2. **`just upgrade` runs `init.sh` Step 3 resync**, which calls `_migrate_env_local_to_toml "${REPO_ROOT}"` at `dist/script/base/init.sh:1190`, inside `_init_existing_repo`.

3. **The migration removes the live file.** `_migrate_env_local_to_toml` (`dist/script/docker/lib/ini_to_toml_migrate.sh:264-308`) writes `.env.local.toml`, then at line 305 does `mv -- "${_env}" "${_env}.bak"`. The working `.env.local` is gone.

4. **The scaffold puts back a file with no values in it.** The subsequent apply calls `_scaffold_env_local` (`dist/script/docker/lib/setup_cmd.sh:1511`, with `_env_local_file="${_base_path}/.env.local"`). The scaffold body (`dist/script/docker/lib/env_emit.sh:374-395`) is entirely co
[...截斷，原長 6802 字]

> 留言 (ycpss91255, 2026-09-08): ## Done on `feat/toml-config-unification` (PR #1148)

Two commits, pushed:

- `b03dd96b` fix(init): stop the resync converting .env.local into a file nothing reads
- `17f33285` docs(changelog): record the .env.local data loss and its removal

### The change

Removed the `_migrate_env_local_to_toml "${REPO_ROOT}"` call from `_init_existing_repo` (`dist/script/base/init.sh`, was line 1190). `_migrat
[...截斷，原長 3949 字]


### #1164 [OPEN] test: fixtures named setup.toml contain INI, so their assertions were never exercised (refs #1127)
labels: bug, ready-for-agent

Part of #1127 (TOML config format unification epic). Surfaced by #1162.

## Background

#1162 fixed two defects that had been covering for each other:
`dockerfile/toml_bridge.py`'s `--merge` mode exited 1 unconditionally
after a botched merge, and `_conf_load_layers` in
`dist/script/docker/lib/conf.sh` read the bridge's output through a
process substitution, which put the exit status out of reach, and
returned 0 regardless. Together they turned a total config-load failure
into "empty config handle, every value falls back to its default" --
silently.

That silence hid two things. This issue is the first.

## The problem

A large number of test fixtures are named `setup.toml` but contain INI:
bare `key = value` with unquoted string values, bare `[section]`
headers, and `mount_1 = ...` style numbered keys instead of
`[[volumes]]`. With the bridge fixed, these make it report

```
toml-bridge: <fixture>/setup.toml: Invalid value
```

Before the fix they passed only because the swallowed error left an
empty handle and every value fell back to exactly the default the test
asserted. So these tests were not testing what their names claim.

A test that passes because an error was swallowed is worse than a
failing one. A failing test tells you something. A test green for this
reason tells you a path is guarded when nothing is guarding it.

## Measurement (static, the full suite was not run)

Measured on the `feat/toml-config-unification` branch. Every fixture
body written to a `setup.to
[...截斷，原長 4585 字]

> 留言 (ycpss91255, 2026-09-08): Sibling filed in the same round, on the other consequence of the same swallowed error: #1165 (the config writers still emit INI into `setup.toml`). The writer defect keeps producing new instances of the fixture defect, so #1165 lands first.



### #1165 [OPEN] fix(conf): the config writers still emit INI into setup.toml (refs #1127)
labels: bug, ready-for-agent

Part of #1127 (TOML config format unification epic). Surfaced by #1162.

## Background

#1162 fixed two defects that had been covering for each other:
`dockerfile/toml_bridge.py`'s `--merge` mode exited 1 unconditionally
after a botched merge, and `_conf_load_layers` in
`dist/script/docker/lib/conf.sh` returned 0 without ever checking the
bridge's exit status. Together they turned a total config-load failure
into "empty config handle, every value falls back to its default" --
silently.

That silence hid two things. This issue is the second, and it is the
largest single component of the remaining failures on
`feat/toml-config-unification`.

## The problem

Both config writers in `dist/script/docker/lib/conf.sh` still emit INI.

`_write_setup_conf` (lines 584-755):

- `dist/script/docker/lib/conf.sh:646`
- `dist/script/docker/lib/conf.sh:671`
- `dist/script/docker/lib/conf.sh:686`
- `dist/script/docker/lib/conf.sh:741`

  each `printf '%s = %s\n' ...` -- unquoted value.

- `dist/script/docker/lib/conf.sh:734` --
  `printf '\n[%s]\n' "${__ns}"`, a bare section header.

`_upsert_conf_value` (lines 767-872):

- `dist/script/docker/lib/conf.sh:805`
- `dist/script/docker/lib/conf.sh:845`
- `dist/script/docker/lib/conf.sh:855`

  each `printf '%s = %s\n' ...` -- unquoted value.

- `dist/script/docker/lib/conf.sh:861` --
  `printf '\n[%s]\n%s = %s\n' ...`, a bare section header plus an
  unquoted value.

Consequence: every `setup.sh set`, `setup.sh add`, `setup.sh remove`,
TUI Save, a
[...截斷，原長 4480 字]

> 留言 (ycpss91255, 2026-09-08): Sibling referenced above as "filed in the same round" is #1164 (test fixtures named `setup.toml` that contain INI).



### #1166 [OPEN] fix(test): the test-tools tag misses the files its Dockerfile COPYs
labels: bug, ready-for-agent

## Context

Surfaced while fixing #1162. The bridge under test was already repaired in
the working tree, and `just test` kept reporting 119 failures carrying the
*pre-fix* error `name 'entries' is not defined`. Several hours went into
looking for a second defect in the bridge; there was none. The suite was
running an image built before the fix, because the tag it resolves had not
moved.

## Problem

`script/test/test.sh --test-tools-image` derives the local tooling tag as a
content hash of `dockerfile/Dockerfile.test-tools` **alone**
(`_compute_test_tools_hash`, `script/test/test.sh:1545`, delegating to
`_reclaim_tool_dockerfile_hash`, `dist/script/docker/lib/project_reclaim.sh:202`).
The invariant the derivation exists to hold is *same tag implies same image
contents*. That invariant is broken.

The premise is written down at `script/test/test.sh:1530-1542`:

> The tooling Dockerfile is the only build input of the test-tools image.
> The compose service passes `context: .`, but the Dockerfile never reads
> it: every COPY in it is `COPY --from=<stage>` (bats-src /
> bats-extensions / lint-tools / kcov-builder) and it has no ADD, so no
> file of the checkout can reach a layer.

The premise is false as of the toml-bridge stage.
`dockerfile/Dockerfile.test-tools:267` is a plain build-context COPY:

```
COPY dockerfile/toml_bridge.py /usr/local/bin/toml-bridge
```

and the comment's enumerated stage list does not even mention the
`toml-bridge-src` stage that carries it. Every *ot
[...截斷，原長 5802 字]


### #1167 [OPEN] Rename the TOML config sources to env.toml / env.local.toml, dropping the leading dot
labels: enhancement, ready-for-agent

## Summary

Rename `.env.local.toml` to `.env.toml.local`.

This repo's file-naming convention is "the standard name is ours; a suffix marks a local variant" (workspace `CLAUDE.md`, and section 1 of the workspace-root `CONTEXT.md`). `.env` takes `.env.local`. `setup.toml` therefore takes `setup.toml.local` -- that is #1161. By the same rule `.env.toml` takes **`.env.toml.local`**, not `.env.local.toml`.

`.env.local.toml` reads as a different file FORMAT (a `.toml` whose stem happens to be `.env.local`) rather than as a local variant OF `.env.toml`. That is exactly the defect #1161 fixes on the setup side. This issue is its sibling for the env file: same convention, different file. Neither folds into the other -- they touch disjoint filenames and can land independently, in either order.

Note that the convention is already cited, incorrectly, inside the tree: `_scaffold_env_local`'s doc comment (`dist/script/docker/lib/env_emit.sh:364-366`) justifies the current name with "The `.local.` infix marks it as the LOCAL variant, the same way `setup.local.toml` does". Once #1161 lands, that precedent no longer exists, and the comment argues for a spelling nothing else in the tree uses.

## Occurrences

Verified against `feat/toml-config-unification` (PR #1148). `grep -rn 'env\.local\.toml'`, whole tree.

### Code

- `dist/script/docker/lib/gitignore.sh:38` -- the canonical gitignore entry
- `dist/script/docker/lib/gitignore.sh:26` -- the comment above `_canonical_gitignore_entries` 
[...截斷，原長 4447 字]

> 留言 (ycpss91255, 2026-09-08): Cross-link: the sibling feature issue referenced in the body above is #1168 -- "The `.env.toml` / `.env.toml.local` layer is specified by ADR-37 but not implemented".

Division of labour:

- **This issue (#1167)** is the naming fix only. It renames a file that nothing currently reads, so it is safe to land at any time and does not depend on #1168.
- **#1168** builds the layer: installs the templat
[...截斷，原長 1115 字]

> 留言 (ycpss91255, 2026-09-08): ## Scope correction: the target names change, and the scope widens

The repo owner has settled the naming. The TOML config **sources** drop
their leading dot, for consistency with `setup.toml`:

```
setup.toml    setup.toml.local
env.toml      env.toml.local
```

The leading dot came from `.env`'s dotenv convention. It does not belong
on a TOML config source -- `setup.toml` never had one, and ther
[...截斷，原長 4988 字]

> 留言 (ycpss91255, 2026-09-08): ## Correction: the local variant is `env.local.toml`, not `env.toml.local`

Retitled. The earlier title placed the variant marker after the
extension; it belongs before it.

### What changed

Wrong: `env.toml.local`
Right: `env.local.toml`

### Why

The suffix form was reasoned from `.env` -> `.env.local`. That
precedent does not transfer: `.env` has no `name.extension` structure,
so the whole fil
[...截斷，原長 1805 字]


### #1168 [OPEN] The env.toml / env.local.toml layer is specified by ADR-37 but not implemented (refs #1163)
labels: enhancement, needs-triage

## Summary

ADR-00000037 specifies a second config file pair -- `.env.toml` (the repo's, committed) and its local variant (the operator's, gitignored) -- as the channel for service runtime env. The specification is complete; the implementation is absent. No code reads either file, neither is in any layer chain, the template is never installed into a repo, and no deploy bundle carries one.

`doc/adr/00000037-toml-config-format-unification.md:145-152`:

```
compose.yaml     <- from setup.toml (infrastructure)
.env             <- from setup.toml (infra env) + .env.toml (service env)
.env.local       <- from .env.local.toml
.env.generated   <- interpolation cache (unchanged)
```

Neither of the two middle generations exists.

## Relationship to #1163

#1163 is the release blocker: on `just upgrade`, `_migrate_env_local_to_toml` moves a downstream operator's working `.env.local` into a file nothing reads, and the log line reports success. #1163 lists three fix options; option (a) was "implement the `.env.toml` readers so the migration's destination is live".

**This issue IS option (a), scoped as the feature work.** The two are not alternatives to each other and they are not duplicates: #1163 stops the bleeding (whichever of its three options is chosen, including a revert), and this issue builds the channel the design intends. #1163 can and should land first and on its own timescale -- it is a release gate; this one is not.

## Evidence

Verified against `feat/toml-config-unificat
[...截斷，原長 7727 字]

> 留言 (ycpss91255, 2026-09-08): ## Scope addition: restore the migration call

The scope list above covers installing the template, the layer chain, `write_container_env`'s 5th argument, generating from the local file, the bundle, and the operator-facing text. It does not name the step that closes the loop:

**Restore the `_migrate_env_local_to_toml "${REPO_ROOT}"` call in `dist/script/base/init.sh`.**

That call was removed und
[...截斷，原長 2900 字]

> 留言 (ycpss91255, 2026-09-08): ## Name correction: the sources lose the dot, the generated files keep it

The repo owner has settled the naming. This issue's body spells the TOML
config sources with a leading dot throughout; that spelling is now wrong.
The corrected names are:

```
setup.toml    setup.toml.local
env.toml      env.toml.local
```

The dot came from `.env`'s dotenv convention and does not belong on a
TOML config s
[...截斷，原長 3891 字]

> 留言 (ycpss91255, 2026-09-08): ## Correction: the local variant is `env.local.toml`, not `env.toml.local`

Retitled. Naming only -- the gap this issue reports is unchanged.

### What changed

Wrong: `env.toml.local`
Right: `env.local.toml`

### Why

The suffix form was reasoned from `.env` -> `.env.local`, and that
precedent does not transfer. `.env` has no `name.extension` structure,
so appending `.local` is the only placement
[...截斷，原長 1312 字]


### #1170 [OPEN] Align triage labels with the skills vocabulary vendor_kit now uses
labels: enhancement, needs-triage

`ycpss91255-research/vendor_kit` — the extracted vendoring engine whose first
consumer is this repo — now runs the `mattpocock/skills` engineering skills
(`/to-spec`, `/to-tickets`, `/triage`, `/wayfinder`). Those skills speak in
five canonical triage roles and read them from a per-repo config file. In
vendor_kit each label string equals its role name, so nothing has to be
translated:

```
needs-triage  needs-info  ready-for-agent  ready-for-human  wontfix
```

This repo already uses the same state machine, but names two of the roles
differently, and is missing a third. Since the two repos will cross-reference
issues constantly (base is the tree vendor_kit installs), an agent reading an
issue here and writing one there has to hold a mapping table in its head. That
is one more thing to get wrong, and the failure is silent: a label applied
under the wrong name simply drops the issue out of the frontier query.

## Current state

| Canonical role    | Label here      | Issues carrying it |
| ----------------- | --------------- | ------------------ |
| `needs-triage`    | `triage`        | 20                 |
| `needs-info`      | `question`      | 1 (#765, closed)   |
| `ready-for-agent` | `ready-for-agent` ✅ | 30            |
| `ready-for-human` | *missing*       | —                  |
| `wontfix`         | `wontfix` ✅     | 0                  |

Category labels (`bug` 131, `enhancement` 245, `documentation` 15) already
match the convention and need no change.

Four GitHub defa
[...截斷，原長 3974 字]


### #1171 [OPEN] fix(ci): the tooling image's change signal names only its Dockerfile
labels: bug, github_actions, ready-for-agent

## Context

One invariant -- *same tag implies same image contents* -- is broken in
three places by the same premise, that `dockerfile/Dockerfile.test-tools`
is the only input of the test-tools image. #1166 / PR #1169 fixed the
first: the LOCAL tag derivation. This issue is the second: CI's rebuild
and republish decision. The third is the downstream `just build`, filed
separately.

The premise stopped holding when the toml-bridge stage arrived.
`dockerfile/Dockerfile.test-tools:264-267` is

```
FROM python:${TOML_BRIDGE_PYTHON} AS toml-bridge-src
ARG TOML_BRIDGE_TOMLI
RUN pip install --no-cache-dir "tomli==${TOML_BRIDGE_TOMLI}"
COPY dockerfile/toml_bridge.py /usr/local/bin/toml-bridge
```

a plain build-context COPY, and `Dockerfile.test-tools:349` bakes the
result into the final image:

```
COPY --from=toml-bridge-src /usr/local/bin/toml-bridge /usr/local/bin/toml-bridge
```

Every OTHER input of that image is pinned by a literal inside the
Dockerfile's own text (`BATS_VERSION`, `ALPINE_VERSION`, `KCOV_VERSION`,
the shellcheck / hadolint release URLs), so `dockerfile/toml_bridge.py`
is the one file whose content can change without the Dockerfile moving.

## Problem

Two workflows decide, from the Dockerfile's path alone, whether the
tooling image needs rebuilding.

**1. `.github/workflows/self-test.yaml` -- `testtools_changed`.** The
`classify` job computes it with two diffs, both naming one pathspec:

- `self-test.yaml:193-198` (non-PR events, the push arm):
  ```
  if [[ "
[...截斷，原長 6449 字]

> 留言 (ycpss91255, 2026-09-08): ## Interaction with #1176 (toml-bridge migrating to its own repo)

#1176 proposes moving the parser out of this repo and consuming the
published image instead. That changes what this issue is *about*, but
does not close what it is an *instance of*. The distinction decides how
this issue should be re-read rather than whether it should be closed.

### The specific gap closes by removal, conditionall
[...截斷，原長 4243 字]


### #1172 [OPEN] fix(build): the downstream tooling build COPYs a path that exists only in base
labels: bug, needs-triage

## Context

The third site of the invariant #1166 fixed. One premise --
`dockerfile/Dockerfile.test-tools` is the only input of the test-tools
image, and every COPY in it is `COPY --from=<stage>` -- broken in three
places by the arrival of the toml-bridge stage:

1. the local tag derivation -- **fixed** by #1166 / PR #1169;
2. CI's rebuild and republish decision -- filed separately;
3. the downstream `just build`, **this issue**.

Sites 1 and 2 are stale-image bugs: a wrong answer, quietly. Site 3 is
not. It is a hard build failure in every consumer repo, and it fires on
the first fanout that carries the toml-bridge stage.

## Problem

`dist/script/docker/wrapper/build.sh` builds the tooling image with the
DOWNSTREAM repo root as the build context.

`build.sh:495` names the Dockerfile inside the vendored subtree:

```
local _tools_dockerfile="${FILE_PATH}/.base/dockerfile/Dockerfile.test-tools"
```

and `build.sh:533-536` hands `${FILE_PATH}` -- the downstream repo root --
as the context:

```
docker build "${_tools_args[@]}" \
  -t "${_test_tools_image}" \
  -f "${_tools_dockerfile}" \
  "${FILE_PATH}" -q >/dev/null
```

`dockerfile/Dockerfile.test-tools:267` is

```
COPY dockerfile/toml_bridge.py /usr/local/bin/toml-bridge
```

resolved relative to the CONTEXT, not to the Dockerfile. In base's own
checkout the context is base's root and `dockerfile/toml_bridge.py` is
there. In a downstream repo the context is the downstream root, where the
path resolves to `<downstream>/doc
[...截斷，原長 7903 字]

> 留言 (ycpss91255, 2026-09-08): ## Interaction with #1176 (toml-bridge migrating to its own repo)

#1176 proposes moving the parser out of this repo and consuming the
published image instead. Read against this issue, the two are not
independent: one of them may remove this defect rather than fix it. But
only on some of its branches, and the deadline that governs both belongs
to neither.

Everything below is checked against the t
[...截斷，原長 4936 字]


### #1173 [OPEN] feat(test): no just entry for running a single spec, so the TDD inner loop reaches past just
labels: enhancement, needs-triage

Two small, independent tooling papercuts found while working on #1166.
Neither is related to that issue's subject; both are recorded here so they
are not lost. They can be fixed in either order, or by two people.

---

## (a) `enforce_local_full_ci_before_pr.sh` gates the wrong repository

**Ownership note first:** the hook is tracked in
`ycpss91255-docker/docker_harness` at
`.claude/hooks/enforce_local_full_ci_before_pr.sh`, not in this repo. It
is filed here because it was found here and it gates PRs to this repo; the
fix belongs in `docker_harness` and the issue may want transferring.

### Problem

The hook resolves the repository from the tool call's `cwd`, which is the
parent `docker` checkout rather than the git worktree the work is
happening in.

`enforce_local_full_ci_before_pr.sh:62`:

```
cwd="$(printf '%s' "${input}" | jq -r '.cwd // empty' 2>/dev/null)"
```

then `:69-72`:

```
[[ -z "${cwd}" ]] && cwd="${PWD}"
root="$(git -C "${cwd}" rev-parse --show-toplevel 2>/dev/null)" || return 0
head="$(git -C "${root}" rev-parse HEAD 2>/dev/null)" || return 0
```

`root` decides both halves of the check: the HEAD that must be attested,
and where the marker is looked for (`:31` `MARKER_SUBDIR=".claude/state/local-ci-pass"`,
`:89` `local marker_dir="${root}/${MARKER_SUBDIR}"`).

Work in this project is done in git worktrees under
`<workspace>/worktree/<repo>-<N>/`, and shell calls do not `cd` into them
-- the project convention is `git -C` / relative paths, so the session cw
[...截斷，原長 5795 字]

> 留言 (ycpss91255, 2026-09-08): ## Scope change: part (a) moved out, this issue is now part (b) only

Part (a) -- `enforce_local_full_ci_before_pr.sh` resolving the repository
from the tool call's `cwd`, and therefore gating the wrong repository when
the work is in a git worktree -- has been moved to
`ycpss91255-docker/docker_harness#310`, where the hook actually lives.

The body's own ownership note was right, and it checks out
[...截斷，原長 1945 字]


### #1174 [OPEN] docs(setup.conf): gpu_capabilities comment omits video, display, ngx, compat32 and all
labels: documentation, needs-triage

## Problem

The `gpu_capabilities` comment in `.setup.conf` documents four values:

```
# gpu_capabilities  Space-separated GPU capabilities to request:
#                     gpu         Basic (default, most cases).
#                     compute     CUDA compute.
#                     utility     nvidia-smi etc.
#                     graphics    OpenGL/Vulkan rendering.
#                   Combine by space: "compute utility graphics"
```

The validator in `script/docker/lib/_tui_conf.sh:554` accepts nine:

```bash
gpu|all|compute|compat32|graphics|utility|video|display|ngx) ;;
```

`all`, `compat32`, `video`, `display` and `ngx` are all valid but undocumented.

## Impact

A consumer reading only the comment cannot discover `ngx`, and would
reasonably assume `graphics` covers GPU rendering support in full. It does
not: `nvidia-container-toolkit` treats `ngx` as a separate capability, and
without it `libnvidia-ngx.so.*` and `/usr/share/nvidia/nvoptix.bin` are never
injected into the container.

This is not hypothetical. A downstream repo configured
`gpu_capabilities = gpu compute utility graphics video`, so the NGX and OptiX
runtime never reached its containers. On Isaac Sim 6.0.1 the default render
mode path-traces one sample per pixel and depends on the NGX denoiser, so
every rendered and streamed frame came out heavily speckled, and every render
setting tried against it appeared inert because the runtime backing those
settings was absent.

The counter-intuitive part is worth
[...截斷，原長 1922 字]

> 留言 (ycpss91255, 2026-09-08): Confirmed the validator, but the picture in `base` itself differs from the
issue in two ways worth recording before anyone fixes this. Checked against
`feat/toml-config-unification` (post-`dist/` layout).

## Validator: confirmed

`_validate_gpu_capabilities` has moved to
`dist/script/docker/lib/_tui_conf.sh:517-530`; the `case` arm is line 525 and
still accepts the same nine names. The count in t
[...截斷，原長 3212 字]

> 留言 (ycpss91255, 2026-09-08): Sibling issue #1179 proposes defaulting `gpu_capabilities` to `all`, which would
make the values missing from this comment less costly to miss.

The documentation gap is worth closing either way: a consumer who chooses to
enumerate still needs to know `ngx` exists and is not implied by `graphics`.



### #1175 [OPEN] fix(ci): the toml-bridge smoke test feeds its probes to the entrypoint, so three of four cannot fail
labels: bug, ready-for-agent

## Context

`.github/workflows/release-toml-bridge.yaml` ends with a **Smoke test
pushed image** step (`release-toml-bridge.yaml:210-237`) whose stated job
is, in its own comment at `:212-215`:

> Pull the just-pushed image and verify the three things downstream
> consumers rely on: Python runs, tomllib is importable (stdlib 3.11+),
> and the toml-bridge entrypoint parses a TOML document to JSON.

Three of the four probes in that step verify nothing. They exercise the
bridge's TOML parser with arguments it discards, and report its exit
status as though it were the probe's. The image is fine; the test is not.

## Problem

`dockerfile/Dockerfile.toml-bridge:31` makes the parser the entrypoint:

```
ENTRYPOINT ["python3", "/usr/local/bin/toml-bridge"]
```

so `docker run IMAGE python3 --version` does not run `python3 --version`.
It runs

```
python3 /usr/local/bin/toml-bridge python3 --version
```

and `dockerfile/toml_bridge.py:86-99` swallows the rest:

```python
def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    kv_mode = "--kv" in sys.argv
    merge_mode = "--merge" in sys.argv

    if merge_mode:
        data = _merge_layers(argv)
    else:
        raw = sys.stdin.buffer.read()
```

`--version`, `-c` and the `-c` payload are neither `--kv` nor `--merge`,
so control falls to the stdin arm. `docker run` without `-i` binds stdin
to `/dev/null`, `tomllib.loads("")` is a valid empty document, and
`json.dump({}, ...)` at `:104` prints `{}` and exits 0.

[...截斷，原長 8809 字]

> 留言 (ycpss91255, 2026-09-08): ## Heads-up: the file this issue fixes is being deleted right now

This issue's whole subject is the **Smoke test pushed image** step inside
`.github/workflows/release-toml-bridge.yaml`. #1180 **Phase A** deletes
that entire workflow.

That work is in flight, not hypothetical: branch
`chore/retire-toml-bridge-publisher`, two commits on top of `main@ec1651d5` --
`8c8d4282` (red: assert this repo pu
[...截斷，原長 2491 字]


### #1176 [OPEN] Migrate toml-bridge to its own repo and consume the published image
labels: enhancement, needs-triage

## Context

The containerised TOML parser now has a repo of its own:
**https://github.com/ycpss91255-docker/toml-bridge** (public, `main`
pushed). It carries a faithful copy of what lives here —
`dockerfile/toml_bridge.py` **byte for byte identical** (`diff` is
empty), `dockerfile/Dockerfile.toml-bridge` as `Dockerfile` (differs
only in the header comment and the `COPY` path, same
`PYTHON_VERSION=3.13.13-alpine3.22` / `TOMLI_VERSION=2.4.1` pins and the
same `tool-pin:` markers), a copy of `release-toml-bridge.yaml`, and a
README that writes down the CLI contract.

It exists because more than one project in the org needs the image.
`ycpss91255-research/vendor_kit` — the extracted vendoring engine, which
reads a consumer's manifest — is the second; #1150 already recorded
`multi_run` as another, and rejected `FROM toml-bridge:local` there as
"implicit dependency on base being built locally first".

That extraction is done. What is not done is this side of it, and the
reason to do it now is that the two repos are already colliding.

## What the investigation found

### 1. Two repos publish the same package, and the other one already won the tag

`.github/workflows/release-toml-bridge.yaml:48-49` pushes
`ghcr.io/ycpss91255-docker/toml-bridge` on push to `main` (paths-filtered
to the Dockerfile, the parser, and the workflow) and on `v*` tags. The
new repo's workflow is the same file with its own paths, and it pushes
the same name.

GHCR ties a package's Actions write access to the 
[...截斷，原長 10542 字]

> 留言 (ycpss91255, 2026-09-08): ## Consolidated from #1178

#1178 ("Retire base's toml-bridge publisher") asked for exactly what item 4
of the proposal above already lists -- deleting
`.github/workflows/release-toml-bridge.yaml` -- so it is closed in favour of
this issue. It was not a pure duplicate, and the part this issue does not
already carry is recorded here so it does not close with it: **the `v*` arm
of that workflow, and
[...截斷，原長 8989 字]

> 留言 (ycpss91255, 2026-09-08): ## Ownership transferred: the open decision is settled

The repo owner has stated that responsibility for `toml-bridge` has
transferred — `ycpss91255-docker/toml-bridge` owns it. Recording that
here as reported fact from the owner, not as an inference drawn from the
registry state.

That answers the **"Open decision for a human"** above: **one publisher,
and it is `ycpss91255-docker/toml-bridge`.*
[...截斷，原長 4173 字]


### #1177 [OPEN] fix(setup_tui): GPU capability screen destroys values it cannot show
labels: bug, needs-triage

## Context

#1174 reports that the `gpu_capabilities` documentation lists four of the nine
values the validator accepts, and proposes extending a comment. Verifying that
report against the tree turned up two things it did not cover.

First, the comment #1174 quotes does not exist in `base`. It is not in
`dist/.setup.conf`, not in `dist/setup.toml`, and not on `origin/main`
(`git grep 'Space-separated GPU capabilities' origin/main` returns nothing).
It lives in a downstream consumer: `isaac/.setup.conf:122-127`, tracked in that
repo. The `_tui_conf.sh:554` line number #1174 cites is likewise the downstream
vendored copy's line; in `base` the same case arm sits at
`dist/script/docker/lib/_tui_conf.sh:525`.

Second, and the reason this is a separate issue rather than a comment on #1174:
there is a third site, and it does not merely fail to document the set. It
destroys values silently. It is also the site that would actually produce the
symptom #1174 describes, because it undoes a hand-edited value without saying so.

All line references below are against `feat/toml-config-unification` at
`17f33285`, and were re-read while writing this.

## Problem

`_edit_section_deploy`'s GPU capability screen
(`dist/script/docker/wrapper/setup_tui.sh:1639-1654`) can express four of the
nine capabilities the validator accepts, and it writes its result back
unconditionally:

```bash
  _cur="$(_override_get "deploy.gpu_capabilities" "gpu")"
  local _on_gpu=off _on_compute=off _on_utility=off _on
[...截斷，原長 9920 字]

> 留言 (ycpss91255, 2026-09-08): ## Correction: "no separate save confirmation" is true on one route, not both

The body (under "How far it reaches, stated precisely") says `main` calls
`_commit_and_setup` unconditionally after `_edit_section_${_subcmd}` returns,
and that there is no separate save confirmation. That holds on the
direct-section route only. As written it overstates the defect, so this
comment narrows it. Line refer
[...截斷，原長 3248 字]


### #1179 [OPEN] feat(setup.conf): default gpu_capabilities to all -- omitting ngx fails silently
labels: enhancement, needs-triage

## Proposal

Make `all` the default for `gpu_capabilities`, rather than the current
`gpu compute utility graphics`.

## Why

The enumerated default is a list a consumer has to get exactly right, and
getting it wrong fails silently. A downstream repo hit this: it configured

```
gpu_capabilities = gpu compute utility graphics video
```

which looks complete and covers rendering, but omits `ngx`. `ngx` is a separate
capability in nvidia-container-toolkit and is **not implied by `graphics`**, so
`libnvidia-ngx.so` and `/usr/share/nvidia/nvoptix.bin` never reached the
container.

That mattered because Isaac Sim 6.0.1 boots `RealTimePathTracing`, which
path-traces one sample per pixel and depends on the NGX denoiser to clean the
result, while `/rtx/rendermode` rejects the older `RaytracedLighting`. With no
NGX, every rendered and streamed frame came out heavily speckled. There was no
error message pointing at the capability list -- only `Failed to create NGX
context` in the Kit log, which reads as a driver or hardware problem. The
investigation that eventually found it had first tried and ruled out every
render setting, because those settings are all inert without the runtime behind
them.

## Measured cost of `all`

On an RTX 5090 host (driver 610.43.02), comparing what actually lands in the
container:

| `NVIDIA_DRIVER_CAPABILITIES` | NGX libs | Total files in `/usr/lib/x86_64-linux-gnu` |
|---|---|---|
| `compute,utility,graphics,video` | 0 | — |
| `compute,utility,graphics,vide
[...截斷，原長 2880 字]

> 留言 (ycpss91255, 2026-09-08): The proposal is sound -- the measurement is convincing and the failure mode it
removes is real. This is only an ordering note against #1177, because landing
`all` as the default before #1177 is fixed produces the same *class* of silent
failure this issue exists to eliminate.

All references verified against `feat/toml-config-unification` at `17f33285`.

## The mechanism

`_edit_section_deploy` (`d
[...截斷，原長 4439 字]


### #1180 [OPEN] chore(toml-bridge): retire this repo's copies now that toml-bridge owns the package
labels: enhancement, github_actions, ready-for-agent

## Context

The repo owner has stated that responsibility for `toml-bridge` has
transferred: `ycpss91255-docker/toml-bridge` owns it. That settles the
"Open decision for a human" recorded at the end of #1176 — **one
publisher, and it is the new repo**, not this one. The alternative
recorded there (this repo keeps owning the package while the new repo is
source-of-truth but never publishes) is closed off.

That unblocks #1176's **item 4**, "Retire this repo's copies once the
shared repo publishes". This issue carries item 4 out on its own so it
can be worked independently of the rest of the migration. #1176 stays
open for items 1, 2, 3 and 5.

## Inventory: what item 4 names, and where each one actually is

Item 4's list was checked against two trees, because they differ. `HEAD`
below is the epic worktree branch `feat/toml-config-unification`; it is
**behind** `origin/main` (merge-base `ff53be6a`, `origin/main` at
`ec1651d5`).

| Item 4 names | `origin/main` | `feat/toml-config-unification` |
|---|---|---|
| `dockerfile/Dockerfile.toml-bridge` | present | present (31 lines) |
| `dockerfile/toml_bridge.py` | present | present (152 lines) |
| `.github/workflows/release-toml-bridge.yaml` | **present** | **absent** |
| `script/test/drivers/hadolint.sh:35` | present | present |
| `test/bats/unit/toml_bridge_spec.bats` Seam 1 | present | present (`:32-67`) |

**Nothing on the list is already gone.** The one asymmetry is the
workflow, and it is not a deletion: `release-toml-bridge.ya
[...截斷，原長 10819 字]

> 留言 (ycpss91255, 2026-09-08): ## #1181 adds a second gate to Phase B

**Phase A is unaffected.** It stays unblocked and keeps its deadline (the
next tag cut from `main`). Re-verified in the epic worktree
(`feat/toml-config-unification`, `17f33285`):
`.github/workflows/release-toml-bridge.yaml` is present on `origin/main`
and absent on the branch, and `git grep
'ghcr.io/ycpss91255-docker/toml-bridge' origin/main` still finds on
[...截斷，原長 4294 字]

> 留言 (ycpss91255, 2026-09-08): > *This was generated by AI during triage.*

## Phase A is ready for an agent; Phase B is not, and the label covers both

This issue carries `ready-for-agent`, and **Phase A genuinely is**: delete
`.github/workflows/release-toml-bridge.yaml`, a writer with no reader, with a
deadline of the next tag cut from `main`. Nothing below disputes that half.

**Phase B is a different thing wearing the same 
[...截斷，原長 3998 字]

> 留言 (ycpss91255, 2026-09-08): > *This was generated by AI during triage.*

## Phase B's state, stated in words because the label does not exist here

`ready-for-human` — a judgment call, not work an agent can pick up.

This repo's label set has `triage`, `question`, `ready-for-agent`,
`backlog` and `upstream`, and no `ready-for-human`, so the state Phase B
is actually in cannot be applied. #1170 is the issue that would add it.
[...截斷，原長 1210 字]


### #1181 [OPEN] base is the only consumer of toml-bridge's baked-in CLI: if the parser leaves the image, base needs its own reader or its own image
labels: enhancement, needs-triage, upstream

## Context

The mirror of
https://github.com/ycpss91255-docker/toml-bridge/issues/1, filed here
because the exposure is on this side.

That issue records an open question in the image's repo: is
`ghcr.io/ycpss91255-docker/toml-bridge` a **runtime** — a pinned Python
plus a TOML library — that currently happens to carry `base`'s parser,
or does the parser ship there permanently? It does not propose an
answer. This issue records what the answer costs *here*, so that if it
lands on "runtime", the work it implies for `base` is already written
down rather than discovered at the break.

`base` is the only repo that runs the image's baked-in CLI. The other
consumer, `ycpss91255-research/vendor_kit`, overrides the entrypoint and
runs its own reader; `multi_run` (#1150) wants the image to `FROM` and
`COPY` its own modules into, which is the same runtime usage. So on the
question of whether the parser stays, `base` is the entire constituency
for "yes".

## What this repo depends on, exactly

Not "the toml-bridge image". The **entrypoint**. Verified on
`main@ec1651d5`:

```bash
# dist/script/docker/lib/toml_bridge.sh:27
docker run --rm -i "${_image}" "$@" < "${_file}"

# dist/script/docker/lib/toml_bridge.sh:58-59
docker run --rm "${_mount_args[@]}" "${_image}" \
  --merge ${_kv} "${_container_paths[@]}"
```

Neither call passes `--entrypoint`, and both pass parser flags
positionally. The image's

```dockerfile
ENTRYPOINT ["python3", "/usr/local/bin/toml-bridge"]
```

is therefore load-
[...截斷，原長 4026 字]

> 留言 (ycpss91255, 2026-09-08): > *This was generated by AI during triage.*

## Added the `upstream` label

This issue is not waiting on anything in this repo. Its own Scope says so:
"Recording only. No change is proposed here and none is due until
toml-bridge#1 is answered." The thing it waits on is a decision in another
project — https://github.com/ycpss91255-docker/toml-bridge/issues/1, whether
`ghcr.io/ycpss91255-docker/toml
[...截斷，原長 1629 字]


### #1182 [OPEN] chore(labels): adopt the canonical five-role triage vocabulary
labels: needs-triage

## Context

Two repos in the org already implement a canonical five-role triage label
vocabulary, where every label string is exactly its role name:

- `ycpss91255-research/vendor_kit`
- `ycpss91255-docker/agent_harness`

`agent_harness` documents the vocabulary and its rationale in
`doc/agents/triage-labels.md`. The point of the vocabulary is that skills and
agents can name a role (`needs-triage`, `needs-info`, `ready-for-agent`,
`ready-for-human`, `wontfix`) and have it resolve to the same label string in
every repo, with no per-repo translation table.

This repo is partway there. Live label state, observed with
`gh label list -R ycpss91255-docker/base`:

| label | colour | description |
| --- | --- | --- |
| `ready-for-agent` | `#0E8A16` | Spec is fully specified and ready for an agent to implement |
| `wontfix` | `#ffffff` | This will not be worked on |
| `triage` | `#fbca04` | Newly filed; awaiting review / categorization (needs a maintainer or bot to sort) |
| `upstream` | `#d4c5f9` | Blocked on / tracking an upstream project fix |
| `backlog` | `#666666` | Tracked for later; deferred - not actively worked on right now |
| `bug`, `documentation`, `enhancement` | | org category labels |
| `dependencies`, `github_actions` | | Dependabot's own PR labels |
| `duplicate`, `invalid`, `question`, `good first issue`, `help wanted` | | GitHub stock defaults, never customised |

## Problem

Three of the five roles have no label at all here: `needs-triage`,
`needs-info` and `ready
[...截斷，原長 6526 字]


### #1183 [OPEN] labels: no label says an issue is blocked on a decision rather than triage
labels: enhancement, needs-triage

> *This was generated by AI during a label alignment pass.*

## Context

`ycpss91255-docker/base#1182` is open and asks this repo to adopt the
canonical five-role triage vocabulary: rename `triage` to `needs-triage` with
`gh label edit --name` rather than delete-and-recreate, create `needs-info`
and `ready-for-human`, and decide deliberately what happens to the undeleted
GitHub defaults. **This issue does not repeat any of that.** #1182 covers the
five roles completely and should land first; what follows is only the part it
could not cover, because the part did not exist when #1182 was written.

Since #1182 was filed, two repos have added a **sixth** state role and put it
into use:

- `ycpss91255-docker/agent_harness` added it first. Verified live with
  `gh label list -R ycpss91255-docker/agent_harness --json name,color,description`:
  name `needs-decision`, colour `006b75`, description
  "Waiting on a maintainer decision, not more information". It carries two
  issues there today (#9, #11).
- `ycpss91255-research/vendor_kit` created it byte-identically on 2026-09-09
  and applied it to 13 of its 16 open issues, documenting the role and its
  boundary in `doc/agents/triage-labels.md`.

The role exists because of a title rule the two repos agreed: **undecidedness
is carried in a label, never in the title**. A title states the problem, so
the fact that an issue's deliverable is a judgement rather than an
implementation has nowhere else to live.

## Problem

Verified live with 
[...截斷，原長 6517 字]


### #1184 [OPEN] refactor(setup.toml): split [lifecycle] into service + base.watchdog
labels: enhancement

## Context

The TOML redesign draft for `setup.toml` relocates every setting that lives
under `[lifecycle]` today into two new tables. No child of epic #1127 records
that relocation, so it is currently a fait accompli in a draft rather than a
tracked piece of work.

`[lifecycle]` mixed three unrelated concerns under one name: two keys that map
straight onto compose service fields (`restart`, `init`), and a base-only
supervision loop (the watchdog). The split puts the compose-mapped pair under a
bare section name, `[service]`, and the base extension under the `base.*`
namespace, `[base.watchdog]` -- the convention #1152 writes down and the
redesign follows throughout.

## Problem

Verified against the tree.

Relocation map:

| Today | Draft |
|---|---|
| `[lifecycle] restart` | `[service] restart` |
| `[lifecycle] init` | `[service] init` |
| `[lifecycle] watchdog_check` | `[base.watchdog] check` |
| `[lifecycle] watchdog_start_period` | `[base.watchdog] start_period` |
| `[lifecycle] watchdog_interval` | `[base.watchdog] interval` |
| `[lifecycle] watchdog_timeout` | `[base.watchdog] timeout` |
| `[lifecycle] watchdog_failures` | `[base.watchdog] failures` |
| `[lifecycle] watchdog_on_fail` | `[base.watchdog] on_fail` |
| `[lifecycle] watchdog_max_restarts` | `[base.watchdog] max_restarts` |
| `[lifecycle] watchdog_notify` | `[base.watchdog] notify` |

What the move touches:

1. **The reader.** `_resolve_deploy_context`
   (`dist/script/docker/lib/deploy.sh`) is the consolida
[...截斷，原長 6208 字]


### #1185 [OPEN] fix(conf): _conf_split_nskey hard-codes logging as the only sub-sectioned name, blocking the whole base.* namespace (refs #1152)
labels: bug, enhancement

Part of #1127 (TOML config format unification epic). Blocks #1152 and #1184.

## The problem

`_conf_split_nskey` (`dist/script/docker/lib/conf.sh:188-225`) is the single
owner of the rule that turns a `<section>.<key>` namespace key back into its
two halves. It hard-codes that `[logging.<svc>]` is the only name with a dot
in it:

```bash
if [[ "${_nskey}" == logging.*.* ]]; then
  _csn_section="${_nskey%.*}"     # rightmost dot
  _csn_key="${_nskey##*.}"
else
  _csn_section="${_nskey%%.*}"    # first dot
  _csn_key="${_nskey#*.}"
fi
```

Its own docstring states the assumption as a fact about the schema:

> The join is lossy -- either half may contain a dot -- so the split
> leans on the one rule the config schema fixes: the per-service
> `[logging.<svc>]` block is the only sub-sectioned name, so
> `logging.<svc>.<key>` splits at the RIGHTMOST dot and everything else
> splits at the first (`stage:headless.gui.mode` -> section
> `stage:headless`, key `gui.mode`).

The function documents the very constraint that the redesign removes.

Measured on the tree (function extracted and driven directly):

```
base.watchdog.check            -> section=base               key=watchdog.check
base.container_log.driver      -> section=base               key=container_log.driver
base.project.name              -> section=base               key=project.name
logging.web.driver             -> section=logging.web        key=driver
logging.max_size               -> section=logging            key=m
[...截斷，原長 10959 字]


### #1187 [OPEN] fix(test): the tooling image's egress failure reports a packaging mistake, and is re-paid on every invocation
labels: bug

## What the operator reads, and what actually happened

A local `just test` on this host failed while building the tooling image.
What reached the operator was a packaging error, twenty-odd times over:

```
#19 [stage-7 1/10] RUN apk add --no-cache bash parallel git git-subtree ...
#19   0.175 fetch https://dl-cdn.alpinelinux.org/alpine/v3.22/main/x86_64/APKINDEX.tar.gz
#19 240.4 fetch https://dl-cdn.alpinelinux.org/alpine/v3.22/community/x86_64/APKINDEX.tar.gz
#19 240.4 WARNING: fetching https://dl-cdn.alpinelinux.org/alpine/v3.22/main: Permission denied
#19 241.2 ERROR: unable to select packages:
#19 241.2   bash (no such package):
#19 241.2     required by: world[bash]
#19 241.2   ca-certificates (no such package):
...
failed to solve: process "/bin/sh -c apk add --no-cache bash parallel ..." exit code: 21
2026-09-07T14:55:50Z [build] INFO : transcript_complete exit_code=1 duration=244s
```

Full transcript:
`worktree/base-toml-epic/log/build/20260907T145146Z-77ada917.log`.

**The network is not blocked, it is intermittent.** Eight minutes later, the
same build on the same host over the same Dockerfile reached the same index in
0.259s and finished in 11s
(`log/build/20260907T145944Z-f0d5b87f.log`, tag `test-tools:34692a1baea2`). So
this is not a machine that needs to be configured once and then works; it is a
failure the gate can hit on any invocation.

## `Dockerfile.test-tools` predicted this reader, exactly

The `alpine-apk` stage comment (added by #1008) says it in as 
[...截斷，原長 5096 字]


### #1188 [OPEN] track(deploy): the container's user identity is fixed at build time, so a field operator's UID never matches
labels: bug, backlog

## Problem

The identity the container runs as is decided when the image is built, and it is
decided from the **build host**. Nothing resolves it again on the machine the
image is deployed to.

The operator-visible consequence on a field machine whose user is not uid 1000
(or not the developer's uid):

- files the container writes into a bind-mounted host directory land owned by an
  id the field user does not have, so the field user cannot read, edit or delete
  them;
- files the field user places on the host for the container to read are owned by
  an id the container's user does not have, so the container cannot read them;
- the `config/<basename>` override binds that ADR-00000023 gives the operator
  are mounted `ro` by default, which hides half of the above until someone
  declares one `rw`.

This is a **deployment-time** identity problem, not a build-time one. The same
image is correct on the machine that built it and wrong everywhere else. There
is no bug to see in CI, on the developer's host, or in any test that builds and
runs on one machine.

`dist/script/docker/lib/deploy.sh` already states the gap in a comment, and
defers it to a follow-up that was never filed:

> `<mode>` ... is `ro` for anything the manifest did not explicitly declare `rw`
> -- the operator writes on the host, the container reads, so a container write
> fails at once in development instead of on a field host whose UIDs happen not
> to line up. **host-user (`USER_UID`) handling is unchanged (a se
[...截斷，原長 6899 字]


### #1189 [OPEN] fix(upgrade): a migration that recognises nothing is silent, same as one with nothing to do
labels: bug

Split out of #1055, which settled the support floor and explicitly left this
open: "the failure mode this issue names -- a shape no detector recognises is
skipped SILENTLY rather than reported -- is a live defect regardless of how
far back repair reaches."

## Context

`apply_migrations` walks `_MIGRATIONS` in order. Each entry is a
`<name>_detect` / `<name>_apply` pair, and the dispatcher's contract is: a
detector that matches applies, a detector that does not match is passed over.
Passing over is silent by design -- most migrations do not apply to most
trees, so reporting every non-match would be noise.

The consequence is that "this migration does not apply here" and "this
migration should have applied here and did not recognise the shape" produce
identical output: nothing.

## Problem

Base has been bitten by this at least twice.

**`downstream_to_dist`.** It matched `.base/downstream/`, a layout that only
ever shipped as a prerelease. No stable consumer was ever on it, so on every
real tree the detector returned false and the dispatcher moved on without a
word. The migration that the deployed population actually needed,
`flat_to_dist`, had to be written afterwards -- and the gap was found by
someone noticing, not by anything failing.

**The repo-owned smoke COPY (#1044).** `smoke_copy` heals the shipped tree's
path. The sibling COPY reading the repo's own tree was outside every
detector's scope, so an upgraded Dockerfile kept the pre-`v0.42.0` spelling
and nothing said s
[...截斷，原長 4077 字]


# ===== base issues -- 已關閉（419 條；body 前 0 字） =====


### #70 [CLOSED 2026-04-17] Bats BW01/BW02 warnings in unit test output
labels: 


### #75 [CLOSED 2026-04-21] refactor: consolidate config/setup/ into single setup.conf + --setup flag + drift detection
labels: enhancement


### #101 [CLOSED 2026-04-27] bug: _msg() shadowed after source setup.sh — drift_regen / err_no_env messages print as blank lines
labels: bug


### #102 [CLOSED 2026-04-24] enhancement: auto-detect Jetson / L4T and default [build] network=host
labels: enhancement


### #103 [CLOSED 2026-04-24] bug: _lib.sh _detect_lang returns "zh" for zh_TW locale (inconsistent with build.sh/run.sh/i18n.sh)
labels: bug


### #104 [CLOSED 2026-04-24] cleanup: deduplicate _detect_lang across build.sh / run.sh / _lib.sh / i18n.sh
labels: enhancement


### #106 [CLOSED 2026-04-24] migration: downstream repo Dockerfiles still use pre-test-tools inline stages with hardcoded x86_64
labels: enhancement


### #108 [CLOSED 2026-04-24] enhancement: setup.sh should emit runtime service in compose.yaml when build_runtime is enabled
labels: enhancement


### #118 [CLOSED 2026-04-24] feat: align run.sh positional arg semantics with exec.sh (command passthrough + -t for target)
labels: 


### #124 [CLOSED 2026-04-24] feat: --reset-conf flag to restore setup.conf defaults in one step
labels: enhancement


### #125 [CLOSED 2026-04-27] test-tools v0.9.13 multi-arch image: arm64 manifest contains x86_64 binaries
labels: 


### #136 [CLOSED 2026-04-27] setup_tui.sh broken on whiptail-only systems: '--ok-label: unknown option'
labels: 


### #150 [CLOSED 2026-04-28] setup_tui: empty setup.conf creates a save deadlock (越救越空)
labels: 


### #151 [CLOSED 2026-04-28] Upgrade 15 stale downstream repos: --lang zh-TW silently falls back to English
labels: 


### #156 [CLOSED 2026-04-28] upgrade.sh --check uses string equality, not semver — reports prerelease as 'needing downgrade'
labels: 


### #157 [CLOSED 2026-04-28] v0.12.0-rc1: empty setup.conf still silent on build/run drift-check path (#153 incomplete)
labels: 


### #164 [CLOSED 2026-04-28] ci.sh: kcov/kcov compose runner can't reach deb.debian.org from networks where the TW mirror is reachable
labels: 


### #165 [CLOSED 2026-04-28] Dockerfile.test-tools: bats unusable in published image (missing bash + PATH symlink)
labels: 


### #168 [CLOSED 2026-04-28] compose.yaml: switch `ci` service to ghcr test-tools image, drop `_install_deps` apt-install path
labels: 


### #172 [CLOSED 2026-04-29] feat(init/upgrade): sync .gitignore on both new-repo init and template upgrade so derived artifacts stay untracked
labels: enhancement


### #174 [CLOSED 2026-04-29] feat(setup): treat setup.conf as derived (gitignore) + introduce setup.conf.local for user overrides
labels: enhancement


### #175 [CLOSED 2026-04-29] bug: make upgrade-check returns exit 1 when update is available
labels: 


### #177 [CLOSED 2026-04-29] bug(setup_tui): image rules are not compacted after deletion (sparse indices)
labels: 


### #178 [CLOSED 2026-04-29] feat(setup_tui): unify Save & Exit position across dialog/whiptail backends
labels: 


### #186 [CLOSED 2026-04-29] feat(setup): elevate template-default fallback notice from INFO to WARN
labels: 


### #187 [CLOSED 2026-04-29] bug(setup_tui): saving wipes <repo>/setup.conf to 0 bytes (dst == tpl aliasing in _write_setup_conf)
labels: 


### #189 [CLOSED 2026-04-29] test: raise setup_tui.sh coverage from 18% to >=70% via tui_flow.bats
labels: enhancement


### #195 [CLOSED 2026-04-30] feat(build-worker): support Dockerfile in subdirectory via context_path / dockerfile_path inputs
labels: enhancement


### #198 [CLOSED 2026-04-30] bug(build-worker): build-args USER/GROUP/UID/GID disagree with Dockerfile.example USER_NAME/... — useradd creates wrong user, USER switch fails in CI
labels: bug


### #199 [CLOSED 2026-04-30] feat(setup): setup.conf [build] context + additional_contexts for subdirectory-layout repos
labels: 


### #201 [CLOSED 2026-04-30] refactor(setup): collapse setup.conf.local + snapshot to single repo override (fixes bootstrap writeback)
labels: 


### #202 [CLOSED 2026-04-30] test(setup): per-section end-to-end coverage for setup.conf parameters
labels: 


### #207 [CLOSED 2026-05-04] feat(build-worker): forward additional_contexts to docker/build-push-action (CI gap left by #199)
labels: 


### #210 [CLOSED 2026-05-04] Dockerfile.example: evaluate adding ENV TZ and ENV LANGUAGE to align with downstream fleet
labels: 


### #215 [CLOSED 2026-05-06] feat(setup): auto-emit any non-baseline Dockerfile stage as a compose service (generalize #108)
labels: 


### #216 [CLOSED 2026-05-06] run.sh: image-missing path uses Compose auto-build, silently skips lint and Bats smoke from build.sh
labels: 


### #220 [CLOSED 2026-05-06] feat(setup): per-stage `setup.conf` overrides for runtime knobs (gui / gpu_capabilities / network / volumes)
labels: 


### #221 [CLOSED 2026-05-07] discussion: revisit setup_tui main menu vs Advanced menu split
labels: 


### #222 [CLOSED 2026-05-06] build/run/exec/stop.sh: --help ignores --lang when --help comes first
labels: 


### #231 [CLOSED 2026-05-11] docs(setup.conf): add top-of-file header explaining edit flow and derived-file warning
labels: 


### #232 [CLOSED 2026-05-08] feat(workflows): add publish-worker.yaml reusable workflow (opt-in, GHCR push)
labels: 


### #236 [CLOSED 2026-05-08] setup.conf [environment] env_N values silently fail ${VAR} cross-reference
labels: 


### #239 [CLOSED 2026-05-11] feat(Dockerfile.example): concrete builder/devel/runtime pattern (lift ros1_bridge #60 lessons back into template)
labels: 


### #240 [CLOSED 2026-05-08] refactor: remove ROS-specific content from template (move helpers + neutralise examples)
labels: 


### #243 [CLOSED 2026-05-08] feat(build-worker): runtime-test stage smoke + devel-base/devel-test rename for v0.21.0
labels: 


### #246 [CLOSED 2026-05-08] License: migrate to Apache 2.0 + add CI/License badges
labels: 


### #248 [CLOSED 2026-05-11] feat(build.sh): generic script/pre-build.sh hook for repo-specific context validation
labels: 


### #249 [CLOSED 2026-05-11] test: comprehensive behavioural integration coverage for build-worker.yaml + runtime-test + setup.conf parameter variations
labels: 


### #253 [CLOSED 2026-05-08] feat(config/shell): bashrc.d drop-in directory + downstream <repo>/script/bashrc.d/ extension point
labels: 


### #254 [CLOSED 2026-05-08] feat(config): layered file-level override (template default + <repo> overlay) + relocate pip/ out of config/ + bashrc.d drop-in
labels: 


### #261 [CLOSED 2026-05-11] refactor(config): relocate pip/setup.sh out of config/ (build-time scaffolding, not user-facing config) -- deferred from #254
labels: 


### #262 [CLOSED 2026-05-11] Move setup.conf into config/docker/ to align with config/ subdirectory convention
labels: 


### #263 [CLOSED 2026-05-13] Rename repo template -> base and use .base/ as subtree folder in downstream repos
labels: 


### #272 [CLOSED 2026-05-12] CI: refine BuildKit cache scope to per-(repo, distro, arch) to avoid shard cross-invalidation
labels: 


### #273 [CLOSED 2026-05-13] CI: skip heavy build matrix for doc-only PRs (paths-ignore + synthetic ci-summary)
labels: 


### #275 [CLOSED 2026-05-12] convention: <repo>/script/docker/ for Dockerfile-internal build helpers (separate from runtime script/)
labels: 


### #277 [CLOSED 2026-05-11] scripts: add set -euo pipefail to init.sh, ci.sh, setup.sh (3 top-level entry points missing the project convention)
labels: 


### #278 [CLOSED 2026-05-11] scripts: add log helpers (_log_err/_log_warn/_log_info) with ANSI color and NO_COLOR honored
labels: 


### #279 [CLOSED 2026-05-11] build.sh: add --build-arg KEY=VALUE pass-through for one-off overrides (avoid raw docker build / docker compose in downstream READMEs)
labels: 


### #280 [CLOSED 2026-05-12] build.sh: accept -t / --target as alias for positional TARGET (consistent with run.sh -t)
labels: 


### #282 [CLOSED 2026-05-11] wrapper scripts: stale template/ path references after v0.25.0 .base/ rename (fresh clone build.sh broken)
labels: 


### #283 [CLOSED 2026-05-11] refactor(scripts): separate _msg() i18n body from log helper level/tag prefix
labels: 


### #284 [CLOSED 2026-05-13] refactor(scripts): split _lib.sh into focused sub-libs under script/docker/lib/
labels: 


### #285 [CLOSED 2026-05-13] setup.sh CLI: print success confirmation + next-step hint after set/add/remove/reset/apply (and add --quiet)
labels: 


### #289 [CLOSED 2026-05-13] exec.sh: support -- separator before CMD (consistent with run.sh)
labels: 


### #290 [CLOSED 2026-05-13] refactor(setup.sh): split _setup_msg by category + route via _log_*
labels: 


### #291 [CLOSED 2026-05-13] wrappers: coordinated pass to unify positional/flag UX across build/run/exec/stop/setup
labels: 


### #305 [CLOSED 2026-05-13] ci(self-test): add actionlint to PR CI to catch workflow-validator regressions before tagging
labels: 


### #309 [CLOSED 2026-05-13] lib(config_summary): apply ANSI color via _log_color_enabled to dividers/headers (#278 follow-up)
labels: 


### #310 [CLOSED 2026-05-13] setup.conf: add [logging] section with json-file driver rotation defaults
labels: 


### #311 [CLOSED 2026-05-13] wrappers: add -v / --verbose flag (BUILDKIT_PROGRESS=plain) to surface hung builds
labels: 


### #317 [CLOSED 2026-05-14] ci(self-test): wall-time + CI-minute optimization plan (buildx cache, doc-only short-circuit, GHCR rolling tag, behavioural conditional)
labels: 


### #319 [CLOSED 2026-05-13] scripts: prune.sh wrapper + stop.sh --prune flag for docker garbage cleanup
labels: 


### #321 [CLOSED 2026-05-14] setup(gui): X11 forwarding broken under SSH inside container (xauth cookie not rewritten, localhost:N unreachable on bridge net)
labels: 


### #322 [CLOSED 2026-05-14] setup(compose): container_name collides between users on the same host (no $USER_NAME prefix)
labels: 


### #325 [CLOSED 2026-05-14] ci(build-worker): allow pr_distros / tag_distros split for downstream multi-distro matrix subset
labels: 


### #328 [CLOSED 2026-05-14] setup.conf [logging] local_path: host-side file + TUI / CLI orphan fix
labels: enhancement


### #330 [CLOSED 2026-05-14] structure: consolidate user-facing wrappers under script/ + promote root Makefile as the user entry
labels: enhancement


### #334 [CLOSED 2026-05-14] Dockerfile.example: WORKDIR "${HOME}/work" silently collapses to /work (HOME undeclared)
labels: 


### #335 [CLOSED 2026-05-14] exec.sh: -t <non-devel> precheck looks for wrong container name (always ${IMAGE_NAME}, never ${IMAGE_NAME}-<stage>)
labels: 


### #337 [CLOSED 2026-05-19] ci(branch-protection): expand required status checks to cover integration-e2e + behavioural + actionlint (auto-merge race)
labels: backlog


### #338 [CLOSED 2026-05-14] feat(setup): CLI flags for [gui] mode override, x11-cookie skip, and resolved-config inspection
labels: enhancement


### #341 [CLOSED 2026-05-14] stop.sh: docker compose down without --profile silently skips profile-gated services (headless / gui / test)
labels: 


### #344 [CLOSED 2026-05-15] ci(dispatcher): extend multi-distro-build-worker to 2D matrix (distro × variant) for env/ros{,2}_distro
labels: enhancement


### #345 [CLOSED 2026-05-14] stop.sh: -v / --verbose is a no-op (BUILDKIT_PROGRESS=plain has no effect on compose down)
labels: 


### #348 [CLOSED 2026-05-14] feat(upgrade): auto-patch downstream Dockerfile lib drift on subtree pull
labels: enhancement


### #362 [CLOSED 2026-05-15] build.sh -s: add --apply / -Y flag for non-interactive setup on TTY (TUI bypass)
labels: enhancement


### #364 [CLOSED 2026-05-15] feat(init,docs): default-source [logging] helper in init.sh entrypoint + README
labels: enhancement


### #365 [CLOSED 2026-05-15] fix(scripts): build.sh/run.sh usage claims "warn on drift" but auto-regenerates since #88
labels: bug


### #367 [CLOSED 2026-05-15] setup: [logging] LOG_FILE_PATH not emitted on extends-based compose services
labels: 


### #368 [CLOSED 2026-05-15] dockerfile(example) or doc: [logging] source-line example crashes downstream build-time smoke ($USER unset + helper missing in image)
labels: 


### #376 [CLOSED 2026-05-19] ci(self-test): split shellcheck + hadolint into dedicated parallel jobs
labels: enhancement


### #377 [CLOSED 2026-05-19] ci(self-test): split bats unit/integration + move kcov coverage to main-push job
labels: enhancement


### #378 [CLOSED 2026-05-20] track(ci): buildx cache scope cascade invalidates from-source builder layers
labels: enhancement


### #382 [CLOSED 2026-05-20] fix(exec.sh): one-shot CMD inherits TTY → terminal escape sequences leak into output
labels: bug


### #386 [CLOSED 2026-05-20] feat(run.sh): auto compose-down on foreground exit (--rm-like)
labels: enhancement


### #387 [CLOSED 2026-05-20] feat(build.sh): auto-prune predecessor image after successful build
labels: enhancement


### #388 [CLOSED 2026-05-20] feat(prune.sh): clean up stale tagged images from removed worktrees
labels: enhancement


### #390 [CLOSED 2026-05-21] [logging] singular naming + apply prunes stale gitignore entries
labels: enhancement


### #399 [CLOSED 2026-05-25] feat(upgrade.sh): auto-patch Dockerfile COPY *.sh /lint/ → script/*.sh /lint/ post-#330 drift
labels: enhancement


### #402 [CLOSED 2026-05-29] [logging] rethink local_path gitignore lifecycle (runtime append vs canonical sync)
labels: enhancement


### #403 [CLOSED 2026-05-25] fix(upgrade.sh): #399 idempotency regex false-positive on COPY script/*.sh /lint/script/
labels: 


### #405 [CLOSED 2026-05-27] refactor(dockerfile): hadolint ignore cleanup -- pin versions, remove dead rules, fix DL3046
labels: enhancement


### #406 [CLOSED 2026-05-27] refactor(script): reorganize script/docker/ into role-based subdirectories
labels: enhancement


### #407 [CLOSED 2026-05-27] refactor(dockerfile): remove pip/setup scaffolding -- downstream repos handle pip independently
labels: enhancement


### #408 [CLOSED 2026-06-02] refactor(script): extract bootstrap.sh, unify output via log.sh, standardize exit codes
labels: enhancement


### #409 [CLOSED 2026-05-25] feat(hooks,instincts): PostToolUse hook + instincts for shell output via log.sh convention
labels: enhancement


### #410 [CLOSED 2026-06-02] refactor(setup): extract compose.yaml generation + unify devel/per-stage emit path
labels: enhancement


### #411 [CLOSED 2026-06-05] refactor(setup): extract INI parser into shared lib/confparse.sh
labels: enhancement


### #412 [CLOSED 2026-05-26] feat(setup.conf): add [pid] section for pid namespace mode (host/private)
labels: 


### #414 [CLOSED 2026-05-26] Makefile forwarding breaks on VAR=VALUE args + absolute container paths
labels: bug


### #415 [CLOSED 2026-05-26] feat(build-worker): support building/testing extra Dockerfile stages via extra_stages input
labels: 


### #420 [CLOSED 2026-05-27] fix(setup): next-step hint should mention 'make build' as alternative to 'setup.sh apply'
labels: bug


### #423 [CLOSED 2026-05-27] track(lib): OTel-aligned log.sh contract -- 5-level, JSON-only, body enum, TRACEPARENT
labels: enhancement


### #424 [CLOSED 2026-05-27] chore: rename workflow name to CI
labels: enhancement


### #428 [CLOSED 2026-05-27] feat: add combined build+run make target for quick start
labels: enhancement


### #429 [CLOSED 2026-05-27] run.sh: delegate to build.sh when target image missing (first-run gate)
labels: enhancement


### #430 [CLOSED 2026-05-28] runtime-test: default RUNTIME_SMOKE_CMD too weak to catch missing shared libs
labels: bug


### #437 [CLOSED 2026-06-08] docs: README.md out of date — full rewrite needed against current codebase
labels: enhancement


### #438 [CLOSED 2026-05-27] refactor(lib): log.sh single-sink tty-detect + strict body (#423)
labels: enhancement


### #439 [CLOSED 2026-06-05] chore: remove legacy .env.example from all downstream repos
labels: enhancement


### #440 [CLOSED 2026-05-29] feat(script): support repo-local pre/post hooks for wrapper scripts
labels: enhancement


### #444 [CLOSED 2026-05-27] build-worker: add submodules input for repos with git submodule source
labels: 


### #448 [CLOSED 2026-05-27] feat(run.sh): support passing arbitrary CMD to container
labels: enhancement


### #450 [CLOSED 2026-05-28] feat(setup): support mount propagation modes (rslave, rshared) in volumes
labels: enhancement


### #453 [CLOSED 2026-05-28] feat(setup): warn when device propagation used without privileged mode (refs #450 P2)
labels: enhancement


### #454 [CLOSED 2026-05-28] feat(setup): per-stage device propagation redirect (refs #450 P3)
labels: enhancement


### #455 [CLOSED 2026-05-28] feat(setup): detect duplicate device/volume target paths after propagation redirect (refs #450 P4)
labels: enhancement


### #458 [CLOSED 2026-05-28] fix(run.sh): non-devel stages use compose run, bypassing container_name
labels: bug


### #461 [CLOSED 2026-05-28] feat(tui): mount mode picker for devices/volumes (refs #450)
labels: enhancement


### #462 [CLOSED 2026-05-28] Emit runtime.env for [environment] entries (enables standalone scripts to share config)
labels: 


### #465 [CLOSED 2026-05-29] feat(run.sh): per-instance compose override overlay for multi-instance isolation
labels: enhancement


### #466 [CLOSED 2026-06-02] compose.yaml: cap_add / security_opt / devices should be opt-in (not template defaults)
labels: 


### #469 [CLOSED 2026-05-29] Make exec UX for repos whose CLI uses '=' natively (Isaac Sim Kit args)
labels: 


### #470 [CLOSED 2026-05-29] build-worker: add free_disk_space input for large BASE_IMAGE repos (Isaac Sim CI)
labels: 


### #472 [CLOSED 2026-06-02] compose.yaml: emit top-level name: to align with _compose_project -p
labels: 


### #473 [CLOSED 2026-06-02] convention: test/<category>/<tool>/ subdir layout for multi-tool repos
labels: 


### #475 [CLOSED 2026-06-08] refactor(make): evaluate retiring Makefile wrapper — divergence from docker-native UX, escalating workarounds
labels: backlog


### #477 [CLOSED 2026-05-30] upgrade.sh integrity marker hard-codes pre-v0.39.0 path script/docker/setup.sh — breaks upgrades to v0.39.0+
labels: bug


### #478 [CLOSED 2026-06-02] feat(setup.conf): add [lifecycle] section with restart policy key, default off
labels: enhancement


### #481 [CLOSED 2026-06-02] refactor(setup.conf): disambiguate the overloaded "runtime" keyword
labels: enhancement


### #482 [CLOSED 2026-06-01] feat(setup): top-level `volumes:` declaration for named-volume mounts
labels: 


### #490 [CLOSED 2026-06-02] refactor(test): centralize wrapper-callsite greps in template_spec.bats to avoid rename churn
labels: enhancement


### #491 [CLOSED 2026-06-01] upgrade.sh: integrity check fails across script/docker/ reorg (#406) when crossing v0.39.0
labels: 


### #492 [CLOSED 2026-06-08] chore(upgrade.sh): document hard-coded path fragility (init.sh / config/ / lib/)
labels: enhancement, backlog


### #493 [CLOSED 2026-06-01] fix(compose-gen): -test / tooling stages have wrong + uncontrollable runtime config (GPU, devices, X11)
labels: 


### #495 [CLOSED 2026-06-08] feat(lint): detect mixed-tool flat test layout (warn when test/<category>/ mixes runner extensions)
labels: enhancement, backlog


### #496 [CLOSED 2026-06-02] feat(deploy): support non-NVIDIA GPU (Intel/AMD iGPU) — grant /dev/dri access via render/video group_add
labels: 


### #497 [CLOSED 2026-09-03] feat(setup): split env/runtime params; gen self-contained deploy.sh
labels: enhancement


### #499 [CLOSED 2026-06-05] chore(docker): add .dockerignore to base to trim build context
labels: enhancement


### #501 [CLOSED 2026-06-05] feat(setup): clarify env vs workload parameter boundary in setup.conf (S1 of #497)
labels: enhancement


### #502 [CLOSED 2026-06-05] feat(setup): .env -> .env.generated + repurpose .env as workload overlay (S2 of #497, A2 core)
labels: enhancement


### #503 [CLOSED 2026-06-05] feat(dockerfile): bake [environment] defaults as ENV in runtime stage (S3 of #497)
labels: enhancement


### #504 [CLOSED 2026-06-05] feat(setup): structured app-config channel (bind-mount dev / COPY-bake deploy) (S4 of #497)
labels: enhancement


### #505 [CLOSED 2026-06-05] refactor(setup): single flag-resolution layer feeding compose + deploy renderers (S5 of #497)
labels: enhancement


### #506 [CLOSED 2026-06-08] feat(deploy): generate self-contained deploy.sh + tar.xz field bundle (S6 of #497)
labels: enhancement


### #507 [CLOSED 2026-06-08] refactor(setup): retire runtime.env (#462), migrate consumers to .env.generated/.env (S7 of #497)
labels: enhancement


### #514 [CLOSED 2026-06-08] feat(setup_tui): add [lifecycle] restart TUI page (fast-follow of #478)
labels: enhancement


### #517 [CLOSED 2026-06-08] feat(setup_tui): legacy runtime->gpu_runtime migration prompt (fast-follow of #481)
labels: enhancement


### #523 [CLOSED 2026-06-08] feat(ci): add single-file mode to ci.sh (--bats-path + --filter)
labels: enhancement


### #526 [CLOSED 2026-06-08] feat(setup): extend per-stage override allowlist to security.cap_* / security_opt_*
labels: enhancement


### #537 [CLOSED 2026-06-08] fix(run): repo-local post/run hook skipped in detached mode (-d) -- foreground-only EXIT trap
labels: bug


### #545 [CLOSED 2026-06-08] feat(justfile): introduce justfile alongside Makefile (phase 1 of #475, ADR-00000005)
labels: enhancement


### #546 [CLOSED 2026-06-10] refactor(make): retire Makefile wrapper + downstream fanout (phase 2 of #475, ADR-00000005)
labels: enhancement


### #549 [CLOSED 2026-06-11] ci(test-tools): harden release-binary download against transient github CDN 5xx (504 stalls all code PRs)
labels: enhancement


### #550 [CLOSED 2026-06-08] ci(test-tools): harden release-CDN download against transient 504 (retry/backoff)
labels: enhancement


### #558 [CLOSED 2026-06-16] release-worker: archive step copies root-level wrappers that no longer exist post-#330 (cp fails on first tag push)
labels: 


### #559 [CLOSED 2026-06-15] feat(setup): single source of truth for the setup.conf schema (lib/schema.sh registry)
labels: enhancement


### #560 [CLOSED 2026-06-12] feat(schema): lib/schema.sh registry + _schema_validate unifying setup.sh and _tui_conf validation
labels: enhancement


### #561 [CLOSED 2026-06-12] refactor(setup): derive setup.sh section-load + setup_tui dispatch/menu from schema registry
labels: enhancement


### #562 [CLOSED 2026-06-15] test(schema): coverage assertion — every section/key has validator + i18n in all locales
labels: enhancement


### #563 [CLOSED 2026-06-12] refactor(setup): canonical resolved-config seam — resolve once, compose + deploy.sh consume the same value
labels: enhancement


### #564 [CLOSED 2026-06-15] refactor(conf): opaque accessor interface for conf.sh — hide parallel-array + namespacing representation
labels: enhancement


### #565 [CLOSED 2026-06-24] refactor(wrapper): cohesive lib/wrapper.sh runtime — collapse ~250 duplicated lines across the 5 wrappers
labels: enhancement


### #566 [CLOSED 2026-06-12] refactor(compose): extract a per-service compose emitter consuming a resolved-stage value
labels: enhancement


### #567 [CLOSED 2026-06-24] refactor(upgrade): declarative Dockerfile-migration list + fixtures (replace ad-hoc Step-5 seds)
labels: enhancement


### #568 [CLOSED 2026-06-12] refactor(lib): explicit load-order (self-sourced deps) + remove i18n load-time _LANG global
labels: enhancement


### #569 [CLOSED 2026-06-12] refactor(setup): extract testable WS_PATH reconciler seam + cohesive host-probe module
labels: enhancement


### #570 [CLOSED 2026-06-15] docs: add CONTEXT.md glossary (domain vocab + architecture-review concepts)
labels: documentation


### #573 [CLOSED 2026-06-12] refactor(ci): retire Makefile.ci for just, drop make as second runner
labels: enhancement


### #576 [CLOSED 2026-06-25] refactor(comments): strip transient issue refs from code comments, keep ADR refs
labels: enhancement


### #579 [CLOSED 2026-06-17] test(ci): harden integration-e2e into a real runnability gate (assert identity/liveness + native multi-arch)
labels: bug


### #580 [CLOSED 2026-06-12] feat(run): don't surface a clean interactive exit as a recipe failure (just run exit code 130)
labels: enhancement


### #582 [CLOSED 2026-06-12] fix(gui): XAUTHORITY mount materializes a confusing duplicate ~/workspace tree in container HOME
labels: bug


### #586 [CLOSED 2026-06-16] detect_ws_path has no case for a repo's own CI checkout (_work/<repo>/<repo>)
labels: 


### #587 [CLOSED 2026-06-16] ci(release-test-tools): build arm64 on a native runner instead of QEMU
labels: enhancement


### #589 [CLOSED 2026-06-16] fix: group_add device GIDs have no name in the container (groups: cannot find name for group ID N)
labels: bug


### #591 [CLOSED 2026-06-24] test(schema): i18n/kind/default coverage — every key has an i18n key in all locales (deferred from #562)
labels: enhancement


### #594 [CLOSED 2026-06-23] feat(justfile): support repo-local recipes via import? + seed justfile.local scaffold
labels: 


### #596 [CLOSED 2026-06-16] feat(gui): mount /dev/dri in the GUI block so least-privilege repos keep iGPU GL without a broad /dev:/dev
labels: enhancement


### #600 [CLOSED 2026-06-24] refactor(run.sh): remove --instance from base -- base is single-instance only (multi belongs to the compose layer)
labels: 


### #602 [CLOSED 2026-06-18] publish-worker: multi-platform publish pushes the same tag per shard -> last-shard-wins single-arch (no manifest merge)
labels: bug


### #603 [CLOSED 2026-06-18] test(ci): add native arm64 matrix to integration-e2e (#579 A2, deferred)
labels: enhancement


### #604 [CLOSED 2026-06-18] feat: establish .dockerignore canonical sync mechanism
labels: enhancement


### #605 [CLOSED 2026-06-18] feat: single-sink TTY-cache revision (#438) + ADR 00000007
labels: enhancement


### #606 [CLOSED 2026-06-18] feat: wrapper transcript for non-interactive verbs (core)
labels: enhancement


### #607 [CLOSED 2026-06-24] feat(init): host preflight for just — warn on missing runner (+ opt-in bootstrap), don't vendor the binary
labels: 


### #608 [CLOSED 2026-06-18] feat: interactive verb orchestration capture (_transcript_detach)
labels: enhancement


### #609 [CLOSED 2026-06-22] feat: transcript lnav regex format
labels: enhancement


### #613 [CLOSED 2026-06-22] fix(ci): coverage (kcov) job red on main — two kcov-environment test bugs
labels: bug


### #615 [CLOSED 2026-06-24] feat(ci): shard kcov + promote coverage to enforced PR gate (amends #377)
labels: enhancement


### #622 [CLOSED 2026-06-24] test: sandbox FILE_PATH in wrapper specs + fix prune --worktree-orphans parallel flake
labels: enhancement


### #624 [CLOSED 2026-06-23] test: prune_sh_spec #644 flaky under parallel suite — stdout/stderr interleaving in dry-run assertion
labels: bug


### #625 [CLOSED 2026-06-25] refactor(structure): justfile layering + base/downstream directory split (epic)
labels: enhancement


### #626 [CLOSED 2026-06-23] [done in #639] refactor(layout): move config/ to downstream/config/
labels: enhancement


### #627 [CLOSED 2026-06-23] [done in #640] refactor(layout): move script/docker lib/runtime/wrapper to downstream/script/docker/
labels: enhancement


### #628 [CLOSED 2026-06-23] [done in #641] refactor(layout): move dockerfile/Dockerfile.example to downstream/dockerfile/Dockerfile
labels: enhancement


### #629 [CLOSED 2026-06-23] [done in #642] refactor(layout): move test/smoke and .hadolint.yaml into downstream/
labels: enhancement


### #630 [CLOSED 2026-06-23] [done in #643] refactor(layout): base self-use justfile.ci to script/ci/justfile.ci + add script/cd/ skeleton
labels: enhancement


### #631 [CLOSED 2026-06-23] [done in #645] feat(justfile): split layered entry + justfile.docker
labels: enhancement


### #632 [CLOSED 2026-06-23] [done in #646] feat(justfile): script/local registry via entry optional import + seed
labels: enhancement


### #633 [CLOSED 2026-06-23] [done in #648] feat(justfile): template namespace + new.sh scaffolder (just template new)
labels: enhancement


### #634 [CLOSED 2026-06-23] [superseded by #650-653] feat(justfile): ci/cd namespaces wired into entry
labels: enhancement


### #635 [CLOSED 2026-06-23] [superseded by #654] refactor(init): consumer wrappers script/*.sh to script/docker/*.sh + migration hygiene
labels: enhancement


### #636 [CLOSED 2026-06-23] [superseded by #497] chore(fanout): roll the new layout to the downstream repos
labels: enhancement


### #637 [CLOSED 2026-06-23] [superseded by #653] feat(init): just host preflight folded into new init.sh — closes #607
labels: enhancement


### #644 [CLOSED 2026-06-23] [superseded by #656] docs: holistic refresh of README structure-tree + mermaid diagrams post base/downstream reorg (#625)
labels: documentation


### #647 [CLOSED 2026-06-24] refactor(dockerfile): generalize the COPY --from=test-tools pattern to all -test stages (runtime-test Bats + ros-test-tools)
labels: enhancement


### #650 [CLOSED 2026-06-24] refactor(justfile): ci namespace -> test, generic content-detecting runner (ADR-00000011)
labels: enhancement


### #651 [CLOSED 2026-06-24] refactor(justfile): cd namespace -> release (ADR-00000011)
labels: enhancement


### #652 [CLOSED 2026-06-24] refactor(justfile): docker as a namespace, no top-level special case; build --stage (ADR-00000011)
labels: enhancement


### #653 [CLOSED 2026-06-24] feat(justfile): base namespace (init/update/upgrade/completions); relocate init.sh/upgrade.sh (ADR-00000011, closes #607 #637)
labels: enhancement


### #654 [CLOSED 2026-06-24] refactor(layout): unify base=origin per-sub symlink for the script tree (ADR-00000011, supersedes #635)
labels: enhancement


### #655 [CLOSED 2026-06-24] feat(justfile): --help and --lang at every just level (ADR-00000011)
labels: enhancement


### #656 [CLOSED 2026-06-24] chore(fanout+docs): roll the full namespace command model to downstream + README/CLAUDE refresh (ADR-00000011, supersedes #636 #644)
labels: enhancement


### #657 [CLOSED 2026-06-24] feat(dockerfile): runtime stage should apply devel's bashrc + ~/.bashrc.d/ init so docker-exec'd interactive shells get the repo env (e.g. ROS)
labels: enhancement


### #677 [CLOSED 2026-06-25] ci: dynamic / weight-balanced shard strategy for bats + coverage (self-hosted vs hosted runners)
labels: enhancement


### #678 [CLOSED 2026-06-25] ops: review main branch-protection settings (merge queue, codecov gate, linear history, ...)
labels: enhancement


### #679 [CLOSED 2026-06-24] fix(run.sh): foreground CMD-override on non-devel targets uses 'up -d + exec', bypassing the ENTRYPOINT (no ROS) and double-launching the default CMD
labels: 


### #686 [CLOSED 2026-06-25] ci: bake coverage tooling into the common test-tools image; stop rebuilding the coverage env every run
labels: enhancement


### #687 [CLOSED 2026-06-25] test(schema/tui): cover input-rejection gaps (newline/injection/malformed) in validator + TUI specs
labels: enhancement


### #688 [CLOSED 2026-06-25] test(setup): cover apply/emit trust-boundary + metacharacter/quoting gaps
labels: enhancement


### #689 [CLOSED 2026-06-25] test(conf/lib): cover dirty-input + error-path gaps in conf accessor + lib
labels: enhancement


### #690 [CLOSED 2026-06-25] test(wrappers): cover exit-code propagation + error-path gaps (run/exec/build/prune/stop)
labels: enhancement


### #691 [CLOSED 2026-06-25] test(transcript/logging): cover error-path + edge-case gaps
labels: enhancement


### #692 [CLOSED 2026-06-25] test(init/ci/gitignore/misc): cover error-path + missing-edge gaps incl. lint_bare_stderr (no spec)
labels: enhancement


### #695 [CLOSED 2026-06-25] docs(test): split TEST.md by test type (unit/integration/behavioural/smoke) with TEST.md as index
labels: documentation


### #697 [CLOSED 2026-06-25] ci: self-test races release-test-tools on a Dockerfile.test-tools change -> stale :main pull fails coverage (kcov not found)
labels: bug


### #698 [CLOSED 2026-06-25] fix(setup): quote compose environment entries + validate network.mode/ipc/pid (unhardened sinks)
labels: bug


### #699 [CLOSED 2026-06-25] test(prune): cover --worktree-orphans interactive confirm gate (destructive rmi + read EOF under set -e)
labels: enhancement


### #700 [CLOSED 2026-06-25] fix(error-path): guard conf-writer mktemp failure + surface failed upgrade rollback (silent clobber / false 'restored')
labels: bug


### #702 [CLOSED 2026-06-25] fix(wrappers): bare-read EOF crash in prune --volumes + build --reset-conf prompts (unfixed #700 siblings) + conf mv-failure cleanup
labels: bug


### #706 [CLOSED 2026-06-25] test: tui_flow.bats (105 tests) excluded from the coverage partition (not *_spec.bats)
labels: bug


### #709 [CLOSED 2026-06-25] ci(codecov): codecov/project status never posted -> #615 coverage gate produces no signal (only codecov/patch posts)
labels: bug


### #710 [CLOSED 2026-06-25] ci(coverage): replace Codecov with a self-hosted, GitLab-portable coverage gate + visibility (no external SaaS)
labels: enhancement


### #713 [CLOSED 2026-06-26] feat(test): first-class local test-tools image build, aligned with the consumer 'just docker build' interface
labels: enhancement


### #714 [CLOSED 2026-06-26] refactor: rename downstream/ -> dist/ + lock the domain glossary (terminology alignment)
labels: enhancement


### #716 [CLOSED 2026-07-08] chore(compose): audit emitter for per-instance overlay-overridability + base<->multi_run contract ADR
labels: enhancement


### #718 [CLOSED 2026-07-08] feat: language-aware just --list / namespace help (i18n) — backlog
labels: enhancement


### #719 [CLOSED 2026-06-26] fix: init.sh refuses self-run inside the base template source (.git-presence guard)
labels: bug


### #720 [CLOSED 2026-06-26] fix: just --list shows broken module descriptions (docker empty, base truncated)
labels: bug


### #721 [CLOSED 2026-07-08] hardening: extend self-run guard to upgrade.sh + raw wrapper scripts
labels: enhancement


### #724 [CLOSED 2026-06-26] perf(ci): time-weighted LPT coverage shard partition (replace @test-count weight)
labels: enhancement


### #725 [CLOSED 2026-06-26] perf(ci): dynamic coverage shard count via CI_SHARDS + fromJSON matrix
labels: enhancement


### #726 [CLOSED 2026-09-05] feat(ci): local in-job nproc-parallel kcov coverage mode (gpu-validated, not production)
labels: enhancement


### #727 [CLOSED 2026-06-26] perf(test): auto-generate doc/test count figures from specs (stop hand-editing)
labels: enhancement


### #730 [CLOSED 2026-06-26] fix(ci): coverage-gate merge must be per-line union, not SUM (drifts with shard count)
labels: bug


### #732 [CLOSED 2026-06-26] fix(ci): build test-tools image once per run, not N parallel rebuilds racing the GHA cache
labels: bug


### #733 [CLOSED 2026-06-26] perf(ci): feed real kcov timings into a self-maintaining shard-weights cache (time-balance the coverage matrix)
labels: 


### #734 [CLOSED 2026-06-26] fix(ci): PR-path test-tools rebuild fires spuriously when PR does not change Dockerfile.test-tools
labels: 


### #737 [CLOSED 2026-06-26] ci: bump node20 actions (upload-artifact/download-artifact/cache) to node24 majors
labels: enhancement


### #742 [CLOSED 2026-06-27] perf(setup): _resolve_deploy_context re-parses conf 10x per call; migrate to the parse-once accessor
labels: enhancement


### #743 [CLOSED 2026-07-08] perf(setup): migrate remaining per-section _load_setup_conf re-parse sites to the parse-once accessor
labels: enhancement


### #745 [CLOSED 2026-06-27] epic: decompose setup.sh (5133-line god-source) into subsystem libs
labels: enhancement


### #746 [CLOSED 2026-06-27] refactor(setup): extract deploy generator to lib/deploy.sh (tracer)
labels: enhancement


### #747 [CLOSED 2026-06-27] refactor(setup): relocate compose emission into lib/compose.sh
labels: enhancement


### #748 [CLOSED 2026-06-27] refactor(setup): extract set/show/list/add/remove/apply subcommands to lib/setup_cmd.sh
labels: enhancement


### #749 [CLOSED 2026-06-27] refactor(setup): relocate shared infra; setup.sh becomes a thin orchestrator
labels: enhancement


### #758 [CLOSED 2026-06-27] Split shard-floor god-test-files along the new lib boundaries to lower the coverage critical path
labels: enhancement


### #760 [CLOSED 2026-06-27] Legitimize SETUP_DETECT_JETSON / SETUP_DETECT_DRI_GROUPS as documented operator detection overrides
labels: enhancement


### #765 [CLOSED 2026-06-29] Decide whether to adopt automated issue triage (bot auto-label)
labels: 


### #766 [CLOSED 2026-08-26] Guard self-hosted-eligible CI jobs to same-repo events (prereq for any self-hosted migration)
labels: backlog


### #769 [CLOSED 2026-06-29] test(e2e): exercise remaining downstream just commands with real execution
labels: enhancement


### #770 [CLOSED 2026-06-29] chore(ci): remove stale QEMU comments now that all runners are native arm64
labels: documentation


### #771 [CLOSED 2026-06-29] chore(docker): drop python3 from the base example devel-base apt list
labels: enhancement


### #777 [CLOSED 2026-06-29] feat(base): per-repo base version monitor workflow (pull-based, shipped via subtree)
labels: enhancement


### #779 [CLOSED 2026-07-01] fix(just): stale test init/upgrade recipes + leaky docker start --help
labels: bug


### #780 [CLOSED 2026-07-01] Epic: re-baseline test taxonomy to ISTQB standard (levels / types / static analysis)
labels: enhancement


### #781 [CLOSED 2026-06-30] S1: ADR for ISTQB test taxonomy + ADR-00000012 amendment
labels: enhancement


### #782 [CLOSED 2026-06-30] S2: restructure test/bats to ISTQB levels (behavioural->system, +acceptance) + scanner
labels: enhancement


### #783 [CLOSED 2026-07-01] S3: smoke per-stage layout + dist tool-first alignment (dist/test/bats/smoke)
labels: enhancement


### #784 [CLOSED 2026-07-01] S4: align init.sh downstream scaffold to new taxonomy (test/bats, TEST.md auto-count, script/local template)
labels: enhancement


### #785 [CLOSED 2026-07-01] S5: formalize Acceptance level + close coverage gaps (just template new e2e, setup-tui doc)
labels: enhancement


### #789 [CLOSED 2026-07-01] just --help coverage for shipped subcommands + reconcile ADR-00000011 drift
labels: enhancement


### #792 [CLOSED 2026-07-07] feat(setup.conf/compose): add an init (PID1 reaper / signal forwarder) toggle
labels: enhancement


### #794 [CLOSED 2026-07-07] feat(setup): keep network/ipc host default; ship usable bridge opt-in (reversed from flip; refs #466)
labels: enhancement


### #797 [CLOSED 2026-07-08] feat(lifecycle): generic watchdog -- supervised restart with a pluggable health-check command
labels: enhancement


### #799 [CLOSED 2026-08-04] docs/convention: bake self-built artifacts under /opt, not $HOME (deploy-time username/UID coupling)
labels: needs-triage


### #800 [CLOSED 2026-07-07] feat(ci): build worker self-validates caller contract (fail early, never silent)
labels: enhancement


### #801 [CLOSED 2026-07-07] feat(ci): registry cache backend option for the shared build worker
labels: enhancement


### #802 [CLOSED 2026-07-08] test(ci): system-level self-test for the shared build worker
labels: enhancement


### #805 [CLOSED 2026-07-07] feat(logging): per-start container log files + stable symlink + configurable retention (glog-style)
labels: enhancement


### #808 [CLOSED 2026-07-09] docs(adr/prd): full review + convergence of base ADRs into a coherent PRD (future grill)
labels: enhancement, ready-for-agent


### #813 [CLOSED 2026-08-26] Add safe multi-arch-aware GHCR cleanup for the test-tools package
labels: needs-triage


### #815 [CLOSED 2026-07-08] sync-doc-counts skips level-4 (####) headings -> counts silently drift
labels: bug


### #816 [CLOSED 2026-07-08] ci_spec system-setup guard tests race on shared /var/run/docker.sock under parallel jobs
labels: bug


### #822 [CLOSED 2026-08-26] Provide a downstream base-release notification/tracking mechanism
labels: needs-triage


### #826 [CLOSED 2026-09-03] docs/convention: canonical devel/runtime/deploy config + launch override mechanism for downstream repos
labels: needs-triage


### #827 [CLOSED 2026-09-03] docs/convention: standardize downstream config/<component>/ directory architecture (flatten audience over-split, vendored baselines out of config/)
labels: needs-triage


### #828 [CLOSED 2026-07-16] bug: local :local image tags (test-tools:local) are not version-scoped -> collide across repos/versions
labels: needs-triage


### #829 [CLOSED 2026-09-04] convention: downstream dep-bump full automation (setup.conf build-arg single-source + ABI-gated auto-release)
labels: needs-triage


### #830 [CLOSED 2026-07-15] docs(prd/adr): PRD invariant #8 (dev/field config split) + ADR-3 amendment + field-deploy ADR
labels: enhancement


### #831 [CLOSED 2026-07-15] refactor(layout): relocate setup.conf to repo root .setup.conf (tool-managed out of config/)
labels: enhancement


### #832 [CLOSED 2026-07-15] feat(deploy): self-contained resolved-compose deploy bundle + deploy.sh up/down
labels: enhancement


### #833 [CLOSED 2026-07-15] feat(deploy): per-component tunable-config manifest + field override (base#826 mechanism)
labels: enhancement


### #840 [CLOSED 2026-08-03] fix(deploy): field compose drops watchdog / restart / non-runtime ENV
labels: bug


### #841 [CLOSED 2026-08-03] fix(deploy): reject non-deployable stages (baseline + *-test)
labels: bug


### #842 [CLOSED 2026-08-03] fix(scripts): entrypoint guard, commit scope, stale setup.conf refs
labels: bug


### #843 [CLOSED 2026-08-03] docs(readme): re-align localized READMEs to the new deploy model
labels: documentation


### #844 [CLOSED 2026-08-03] test(deploy): cover tagless version fallback + versioned e2e identity
labels: enhancement


### #845 [CLOSED 2026-08-03] feat(lint): guard stale config/docker/setup.conf references
labels: enhancement


### #846 [CLOSED 2026-08-04] track(docs): drift guard for localized README translations
labels: enhancement, backlog


### #847 [CLOSED 2026-08-04] track(deploy): field-tunable watchdog thresholds
labels: enhancement, backlog


### #848 [CLOSED 2026-08-04] fix(test): check_test_md_drift.sh reports bogus 0 counts on a relative root
labels: bug


### #853 [CLOSED 2026-08-03] fix(coverage): gate double-counts kcov path aliases, so adding a spec moves the rate
labels: bug


### #855 [CLOSED 2026-08-03] chore(coverage): re-base COVERAGE_MIN to 80 now the rate is measured correctly
labels: enhancement


### #857 [CLOSED 2026-08-04] chore(test): doc-count merges are a hand-repeated recipe with an ungated trap
labels: enhancement


### #859 [CLOSED 2026-08-04] chore(test): per-test catalog rows in unit.md rot silently, no gate checks them
labels: enhancement


### #864 [CLOSED 2026-08-04] fix(test): the doc-count drift gate runs in neither just test nor CI
labels: bug


### #866 [CLOSED 2026-08-04] fix(ci): the just test lint phase runs in no CI job, so four lints gate nothing
labels: bug


### #868 [CLOSED 2026-08-28] EPIC: unify the env-file naming rule -- standard name is ours, suffix is local
labels: enhancement


### #869 [CLOSED 2026-08-05] fix(scripts): unguarded BASH_SOURCE makes every wrapper unsourceable under kcov
labels: bug


### #870 [CLOSED 2026-08-04] feat(deploy): mount manifest config read-only by default, rw only when declared
labels: enhancement


### #873 [CLOSED 2026-08-05] fix(readme): the i18n sync guard is green over stale translations, a re-stamp blesses drift
labels: bug


### #874 [CLOSED 2026-08-05] docs: several documents now state the opposite of what the code does
labels: documentation


### #875 [CLOSED 2026-08-05] fix(stage): three regexes disagree on which line is a stage FROM line
labels: bug


### #876 [CLOSED 2026-08-05] fix: five silent-acceptance defects found by audit
labels: bug


### #877 [CLOSED 2026-08-05] fix(test): shipped smoke specs are tautological and the CD guard is untested
labels: bug


### #879 [CLOSED 2026-08-05] docs/ux: six surfaces where the tool teaches the wrong model
labels: documentation


### #881 [CLOSED 2026-08-17] docs(i18n): five more stale README sections found while fixing the sync guard
labels: documentation


### #882 [CLOSED 2026-08-25] fix(build): a cached test stage reports success without running any check
labels: needs-triage


### #885 [CLOSED 2026-08-25] test(tooling): no just entry runs the shipped smoke specs, so they get hand-rolled with raw docker
labels: enhancement


### #887 [CLOSED 2026-08-25] fix(test-tooling): shared test-tools tag collides between runs, and no just entry runs one spec under kcov
labels: bug


### #891 [CLOSED 2026-08-24] fix(test): concurrent runs share one image tag and one compose project by accident
labels: bug


### #893 [CLOSED 2026-08-05] feat(setup): per-worktree .setup.conf.local override layer and a real project-name key
labels: enhancement


### #895 [CLOSED 2026-08-24] chore: nine undocumented environment variables that change behaviour
labels: enhancement


### #896 [CLOSED 2026-08-17] fix(test): one variable with two defaults means the tag you build is not the tag you run
labels: bug


### #898 [CLOSED 2026-08-24] fix(test): ADR-numbering lint intermittently exits 141 and blocks the stamp
labels: bug


### #900 [CLOSED 2026-08-24] fix(ci): every name CI creates is constant across concurrent runs
labels: bug


### #902 [CLOSED 2026-08-25] test(i18n): the sync guard is blind to a mechanism documented only in a translation
labels: enhancement


### #905 [CLOSED 2026-08-25] fix(scripts): nine more early-closing readers, and one class inverts the result
labels: bug


### #914 [CLOSED 2026-08-25] release-worker archive step hard-fails on any standard path a consumer lacks (second instance)
labels: needs-triage


### #915 [CLOSED 2026-08-25] fix(upgrade): a v0.41.0 consumer half-upgrades to v0.42.0 and loses just entirely
labels: bug


### #916 [CLOSED 2026-08-25] fix(bootstrap): a new repo cannot bootstrap against v0.42.0 (template bootstrap.sh names the pre-dist init.sh)
labels: bug


### #917 [CLOSED 2026-08-25] test(changelog): cap Unreleased entry length with a lint, entries have grown into PR bodies
labels: enhancement


### #920 [CLOSED 2026-09-02] compose emitter bakes container_name -> co-hosted instances collide + can't scale (vs Docker guidance + ADR-00000022)
labels: bug, needs-triage


### #922 [CLOSED 2026-09-03] docs(test): 40 percent of catalog rows carry a placeholder description and nobody decided whether the column is required
labels: needs-triage


### #924 [CLOSED 2026-08-28] fix(ci): base's own release archive is a second hardcoded payload that #914 did not reach
labels: bug


### #925 [CLOSED 2026-08-26] fix(build): a new repo is born with a red CI job because build_runtime defaults true while the runtime stage ships commented out
labels: bug


### #926 [CLOSED 2026-09-05] docs(changelog): split per 0.Y series behind an index, lock the category set, and make a release page show the curated notes
labels: documentation


### #937 [CLOSED 2026-08-26] fix(init): the Dockerfile and .env migrations rewrite consumer files with no rollback on the repos that will run them
labels: bug


### #939 [CLOSED 2026-08-28] fix(dockerfile): multi-platform builds hardcode one architecture, and nothing reports which literals leaked
labels: bug


### #940 [CLOSED 2026-08-28] fix(ci): the shard-balance guard asserts @test counts while the partitioner weighs seconds, so it only fails in CI
labels: bug


### #945 [CLOSED 2026-09-04] refactor(entrypoint): auto-updating base orchestrator so downstream entrypoints stop drifting
labels: enhancement


### #946 [CLOSED 2026-09-04] chore(docker): alpine 3.21 in test-tools reaches EOL 2026-11-01
labels: enhancement


### #947 [CLOSED 2026-09-04] chore(ci): bump the stale hadolint 2.12.0 / shellcheck 0.10.0 gates
labels: enhancement


### #948 [CLOSED 2026-09-02] fix(docker): just has four provenance paths and no shared version
labels: bug


### #949 [CLOSED 2026-08-28] fix(ci): build-push-action stuck on v6 at 5 self-test call sites
labels: bug


### #950 [CLOSED 2026-09-02] chore(ci): close dependabot coverage gaps beyond uses: refs
labels: enhancement


### #951 [CLOSED 2026-09-02] fix(template): shipped Dockerfile builds from a moving ubuntu:24.04
labels: bug


### #952 [CLOSED 2026-09-02] docs(coverage): the README claims coverage and shows no number, so publish the release figure without a SaaS
labels: documentation


### #953 [CLOSED 2026-08-28] fix(test): 260 tests pass when their subject is deleted, because 56 existence guards fail open
labels: bug


### #954 [CLOSED 2026-08-28] fix(test): YAML specs assert against comments, so several guards pass while the property is broken
labels: bug


### #955 [CLOSED 2026-09-02] fix(setup): setup.conf upsert/emit data-correctness bugs (dup key, dotted-section, stage env, completions loop)
labels: bug


### #956 [CLOSED 2026-09-03] fix(upgrade): migration + wrapper failure-path robustness (pip_helper delete, post-hook skip, subtree trap)
labels: bug


### #957 [CLOSED 2026-09-02] fix(ci): worker/seed least-privilege gaps + README .setup.conf drift
labels: bug, documentation


### #959 [CLOSED 2026-08-28] fix(changelog): a duplicated entry and a repeated category heading survive the lint
labels: bug


### #960 [CLOSED 2026-08-28] chore(tooling): update-stale-pr exits on the one conflict shape that is always mechanical
labels: enhancement


### #961 [CLOSED 2026-08-28] chore(tooling): a pushed branch with a green stamp and no PR is invisible
labels: enhancement


### #962 [CLOSED 2026-09-02] fix(test): three guards are narrower than the property they are named for
labels: bug


### #965 [CLOSED 2026-09-02] fix(test): two specs lose a race against the parallel suite, so the gate fails about one run in three
labels: bug


### #969 [CLOSED 2026-09-02] fix(upgrade): the dist/ rename migration misses the .base/script layout every v0.41.0 consumer actually has
labels: needs-triage


### #971 [CLOSED 2026-09-03] refactor(runtime): one directory COPY for base's runtime libs, so adding one is not a change to seventeen repos
labels: enhancement


### #978 [CLOSED 2026-09-04] refactor(doc): remove the derived test figures and report from the run instead (implements ADR-00000028)
labels: enhancement


### #980 [CLOSED 2026-09-04] build-worker: cache_backend: registry unusable -- preflight/build jobs declare permissions: contents: read, intersecting away the caller's packages: write
labels: needs-triage


### #989 [CLOSED 2026-09-03] fix(test): errexit-bang operator fold swallows a '!' line inside an untracked heredoc
labels: bug


### #990 [CLOSED 2026-09-03] fix(test): CRLF disarms the errexit-bang backslash continuation and its splice
labels: bug


### #991 [CLOSED 2026-09-03] fix(test): errexit-bang reports a '!' that ends an if/while/case body as non-final
labels: bug


### #992 [CLOSED 2026-09-03] fix(test): errexit-bang tests the live-'||' exemption before the ';' rule, so a hand-off behind an '||' is silent
labels: bug


### #993 [CLOSED 2026-09-03] fix(test): yaml_step_id_for inherits an earlier step id when a job's first dash is shallower than its steps
labels: bug


### #995 [CLOSED 2026-09-03] fix(docker): base leaves its own litter, and the collector nobody runs is not a collector
labels: bug


### #997 [CLOSED 2026-09-03] convention: a resource a flow creates is reclaimed by the verb that ends the flow, not by one the operator must remember
labels: enhancement


### #999 [CLOSED 2026-09-03] refactor(test): the catalogue's descriptions live beside their tests, and the document is generated
labels: enhancement


### #1000 [CLOSED 2026-09-03] fix(config): the dev-bind is hardcoded to config/app, which no repo in the org has, while two documents promise config/<component>/
labels: bug


### #1002 [CLOSED 2026-09-09] perf(coverage): a spec costs 4-5x more inside the full run than alone -- the cause was a missing --jobs, not the bind-mounted output directory (fixed by #1060, #726)
labels: bug


### #1003 [CLOSED 2026-09-04] convention: a review loop that can only refuse to land has no fixed point, and holding finished work is not a report
labels: enhancement


### #1008 [CLOSED 2026-09-04] fix(docker): Dockerfile.test-tools has no Alpine mirror override, so the gate image is unbuildable where dl-cdn is blocked
labels: bug


### #1009 [CLOSED 2026-09-04] fix(ci): compute-shards and coverage-gate gate nothing, because no needs list names them
labels: bug


### #1010 [CLOSED 2026-09-04] fix(ci): the test-tools staleness guard misses its sixth call site, and its roster names 5 of 15 tools
labels: bug


### #1011 [CLOSED 2026-09-04] fix(ci): system_relevant omits the files the system specs are about, the shipped runtime and every justfile
labels: bug


### #1012 [CLOSED 2026-09-04] fix(ci): an RC tag moves test-tools:latest, and the unrecognised-input branch picks it too
labels: bug


### #1013 [CLOSED 2026-09-04] fix(ci): build-worker reads its diff through an unchecked producer, so a failed diff builds nothing and reports green
labels: bug


### #1014 [CLOSED 2026-09-04] fix(ci): a cleanup failure reddens a good build, a fork PR reddens with no reason, and nothing declares concurrency or timeouts
labels: bug


### #1015 [CLOSED 2026-09-03] fix(test): nothing in just stops what just test started, and an interrupted run reddens the next one with no failing test
labels: bug


### #1032 [CLOSED 2026-09-05] fix(test): a coverage run leaves reports the next run cannot erase, so the second run in a worktree never starts
labels: bug


### #1036 [CLOSED 2026-09-05] fix(upgrade): the migrated Dockerfile is left uncommitted, then the user is told to push
labels: needs-triage


### #1044 [CLOSED 2026-09-05] fix(upgrade): the repo-owned smoke tree is never migrated, so upgraded repos diverge from fresh ones
labels: bug


### #1050 [CLOSED 2026-09-05] fix(init): the rollback does not know about the smoke tree #1045 moves
labels: bug


### #1055 [CLOSED 2026-09-09] track(upgrade): declare what a Y may change and how far back repair reaches
labels: enhancement


### #1059 [CLOSED 2026-09-05] test(ci): the lint phase stops at the first failing driver, so N violations cost N gate cycles
labels: bug


### #1060 [CLOSED 2026-09-05] perf(test): the coverage run is the one bats invocation without --jobs, and that is 73 percent of a shard
labels: bug


### #1068 [CLOSED 2026-09-05] perf(test): the coverage shard runs --jobs 4 on CI because nproc is the wrong question for a latency-bound gate
labels: enhancement


### #1071 [CLOSED 2026-09-05] refactor(ci): group the lint-static matrix instead of one job per lint
labels: enhancement


### #1073 [CLOSED 2026-09-05] track(coverage): what the coverage figure measures, and what 95 would require
labels: enhancement


### #1075 [CLOSED 2026-09-06] perf(ci): one bats test is 66 percent of the coverage matrix critical path
labels: enhancement


### #1077 [CLOSED 2026-09-05] fix(upgrade): upgrade.sh has no compatibility forwarder, so the command that just worked exits 127
labels: needs-triage


### #1080 [CLOSED 2026-09-06] fix(ci): the shellcheck job runs an unpinned binary, so the local gate cannot predict it
labels: bug


### #1086 [CLOSED 2026-09-06] fix(upgrade): the setup.conf relocation migration cannot reach a v0.41.0 consumer, and disarms itself after the hop it missed
labels: needs-triage


### #1105 [CLOSED 2026-09-08] fix(tui): a schema section with no editor is accepted as a subcommand and then not found
labels: bug, ready-for-agent


### #1106 [CLOSED 2026-09-08] fix(tui): _assemble_mount_value lost its only caller and kept six passing specs
labels: bug, ready-for-agent


### #1124 [CLOSED 2026-09-07] Add tag ruleset: require CI for v* tags
labels: needs-triage


### #1128 [CLOSED 2026-09-07] D9: build toml-bridge container image with vendored tomli (refs #1127)
labels: enhancement


### #1129 [CLOSED 2026-09-07] D3: replace conf.sh INI parser with TOML bridge (refs #1127)
labels: enhancement


### #1130 [CLOSED 2026-09-07] D4: type-aware merge semantics for TOML layers (refs #1127)
labels: enhancement


### #1131 [CLOSED 2026-09-07] D8: split environment section by service boundary (refs #1127)
labels: enhancement


### #1132 [CLOSED 2026-09-07] D1: migrate .setup.conf to setup.toml (refs #1127)
labels: enhancement


### #1143 [CLOSED 2026-09-07] fix(release): a release can be cut from a commit that passed CI but is not on main
labels: bug


### #1161 [CLOSED 2026-09-08] Rename setup.local.toml to setup.toml.local for naming consistency
labels: enhancement


### #1178 [CLOSED 2026-09-08] Retire base's toml-bridge publisher: a v* release here would move :latest off the image toml-bridge shipped
labels: enhancement



# ===== base doc/changelog/CONVENTIONS.md（全文） =====

# Writing a changelog entry

Part of the [changelog index](CHANGELOG.md).

An entry answers two questions: **what changed**, and **does it affect me**.
Not why, not what was rejected -- the PR body is this repo's canonical
decision record, the entry already links to it by number, and prose pasted
into both places leaves the argument living twice with the changelog copy the
unreadable one.

```markdown
- **One sentence on what changed** (#NNN) -- who is affected, and whether it
  breaks anything.
```

## Categories

An entry goes under exactly one of these headings, and no other. The lint
refuses anything else in `[Unreleased]`; released sections keep whatever
they shipped with, because rewriting a shipped heading falsifies the record.

<!-- changelog-categories: begin -- generated-by-hand mirror of script/release/changelog_categories.sh; the changelog-entry lint compares the two -->

- `BREAKING`
- `Added`
- `Changed`
- `Deprecated`
- `Removed`
- `Fixed`
- `Security`

<!-- changelog-categories: end -->

`BREAKING` sorts first and is first-class because this project's dominant
risk is breaking the downstream repos that carry `.base/`. **Migration
instructions belong inside the BREAKING entry they serve**, not in a
parallel `Migration` section a reader can miss.

Conventional-commit types (`feat` / `fix` / `test` / `chore` / `refactor`)
were considered and rejected as the axis. They answer *what kind of work was
this* -- the author's view -- where a changelog answers *what changed for me*
-- the reader's. Filing by commit type institutionalises putting `test:` /
`chore:` / `refactor:` work into the changelog, which is part of how this
file passed 680 KiB. A refactor a reader must know about, such as a new
lint that can fail their CI, is `Added`; one they need not know about is
not an entry at all.

The roster is defined once, in `script/release/changelog_categories.sh`. The
lint and the release-notes assembler source it; the list above is a
rendering of it, and the lint fails if the two stop agreeing.

**An `[Unreleased]` entry is capped at 700 characters**, enforced by the
`changelog-entry` lint (`just test lint --changelog-entry`). Two things about
how it measures, because they decide what you can and cannot do about a
failure:

- The unit is the **whole entry** -- the lead bullet plus every continuation
  line and sub-bullet, up to the next top-level bullet or heading. Rewrapping
  the prose or splitting it into a nested list does not reduce the count.
- **Whitespace is collapsed first**, so wrapping at 79 columns and indenting a
  sub-list cost nothing. A short lead plus a four-item migration sub-list
  measures about 450 and fits comfortably.
- The count is in **characters**, the same number on every machine -- quoting
  a path or a heading from the ja / zh-TW / zh-CN guides costs one per
  character, not three.

An entry opens with a `- ` bullet **at column 0**. `*`, `+` and an indented
`-` render the same but are refused by name, because a line that opens no
entry is a line the cap never applies to. Inside a fenced code block nothing
is structure, so an example may safely show a heading or a bullet.

The cap is not the median of past entries; it is set above what a complete
entry actually needs. Ten entries written in this style for the v0.42.0 cycle's
real changes -- including two BREAKING migrations -- measured 210-543. If an
entry does not fit, the part that does not fit is almost always the reasoning,
and it belongs in the PR.

Inside one release block an entry may not repeat another entry's lead bullet,
and a `### <category>` heading may not open twice. That pair is what a serial
merge leaves behind: two branches that both append to `[Unreleased]` do not
conflict, so git keeps both sides and nothing prompts a human. Either one is
refused naming BOTH lines; fold the second copy into the first.

Released sections are **never** checked: they are a historical record, and
rewriting a shipped entry falsifies it. A genuinely exceptional entry opts out
by bracketing it with `<!-- changelog-entry-lint: allow-begin -- <why> -->` and
`<!-- changelog-entry-lint: allow-end -->`.

## The paragraph above the first category

A section may open with prose before its first `### ` heading. For the tag
being released that paragraph is **published as written**, at the top of the
GitHub release page above the merged entries, so write what a reader of that
page needs -- what the release is for, what to do before their next build --
or write nothing.

Do not write it to point at the RC sections. A promoted final's notes are the
union of its own section and every `-rcN` section under it
(`script/release/release_notes.sh`), so "the entries stay under the RC
headings that introduced them" is a sentence about this directory's layout,
printed on a page that already carries those entries. The assembler cannot
tell it from a release summary -- both are prose under a section with no
categories of its own -- and it publishes rather than guesses, because the
alternative deletes the summary too.

An `-rcN` section's own lead is dropped unless it carries a `- ` entry: it
says which candidate this is, which the reader of the final tag is not being
told. A bullet under no heading is an entry that happens to sit above the
first category, and travels to the page with the sentence introducing it.


# ===== base doc/changelog/v0.39.md（截到 6000 字） =====

# base changelog -- v0.39

Part of the [changelog index](CHANGELOG.md).

## [v0.39.0] - 2026-05-28

### Added
- **`[devices]` mount propagation support** — device entries like `device_1 = /dev:/dev:rslave` are auto-redirected from compose `devices:` to `volumes:` long-form bind mount (compose `devices:` does not support propagation). Plain devices without propagation emit to `devices:` as before. Validator (`_validate_mount`) extended to accept `rslave|rshared|rprivate|slave|shared|private` modes, combinable with `ro|rw` (e.g. `rw,rslave`). Warns when propagation is used without `[security] privileged = true` (P2, #453). Warns on duplicate target paths between `[devices]` and `[volumes]` (P4, #455). Per-stage emit supports propagation (P3, #454). Closes #450, closes #453, closes #454, closes #455.

### Changed
- **`run.sh` CMD separator `--` + positional stop** — first positional arg now stops run.sh flag parsing so CMD flags like `--target` no longer collide with run.sh's own `-t/--target`. Explicit `--` separator documented in usage (4 languages). Closes #448.
- **`script/docker/` reorganized into role-based subdirectories** — wrappers move to `wrapper/`, all libs consolidate into `lib/`, container-side helpers move to `runtime/`. `_entrypoint_logging.sh` renamed to `runtime/logging.sh` (container path `/usr/local/lib/base/logging.sh`). New `runtime/entrypoint.sh` template replaces init.sh heredoc. Breaking: downstream symlink paths change; `make upgrade` handles migration automatically. Closes #406.

[v0.39.0]: https://github.com/ycpss91255-docker/base/compare/v0.38.0...v0.39.0


# ===== base doc/changelog/v0.40.md（截到 6000 字） =====

# base changelog -- v0.40

Part of the [changelog index](CHANGELOG.md).

## [v0.40.0] - 2026-05-30

### Added
- **`EXEC_ARGS` env var passthrough for `make exec`** — Kit-style args containing `=` (e.g. `--/app/livestream/port=49100`) historically tripped the #414 `MAKEOVERRIDES` guard, forcing users to call `./script/exec.sh` directly. Setting `EXEC_ARGS='--/app/k=v ...'` in the env now forwards those tokens to `exec.sh` via `$(EXEC_ARGS)`, bypassing make's variable-override interception. Existing `make exec -- -t target cmd` invocations are unaffected; EXEC_ARGS is appended after the `--`-forwarded args. Documented in README + zh-TW/zh-CN/ja translations. Closes #469.
- **Per-instance compose overlay for `run.sh --instance NAME`** — `run.sh --instance NAME` now also auto-detects `config/instances/<NAME>.yaml` (compose `-f` overlay) and `config/instances/<NAME>.env` (compose `--env-file` overlay) on top of the existing `INSTANCE_SUFFIX`-only behaviour. Either file may exist alone; missing files are silently skipped. Yaml handles structural overrides (per-instance ports, volumes, cache dirs); env handles pure `${VAR}` overrides shared with `compose.yaml`. `NAME` is validated against `^[a-z0-9][a-z0-9_-]*$` (lowercase alphanumeric + `_-`) for path safety -- `--instance ../etc/passwd` and similar are rejected up front. New `lib/compose.sh::_compose_project_with_overlay` wraps the underlying invocation; `lib/compose.sh::_validate_instance_name` enforces the rule. README + 3 translations updated. Closes #465.
- **Per-wrapper `pre`/`post` hooks for downstream host-side customisation** — every wrapper (`run` / `build` / `exec` / `stop` / `prune` / `setup` / `setup_tui`) now sources `lib/hook.sh` via `lib/_lib.sh` and calls `_run_pre_hook <name>` after env validation and `_run_post_hook <name>` at the end of main (run.sh's renamed `_app_cleanup` EXIT trap covers Ctrl-C too). Hooks live at `script/hooks/{pre,post}/<wrapper>.sh`; `init.sh` creates 14 executable stubs on new-repo (idempotent on existing-repo / upgrade so pre-#440 templates pick up scaffolding). Pre-hook non-zero exit aborts the wrapper; post-hook non-zero overrides the wrapper exit code but `compose down` still runs (strict + cleanup). `--dry-run` skips both hooks per the no-side-effects contract. Non-executable hook files hard-fail with a clear `chmod +x` hint. Solves `jetson_sdk_manager`'s need to register `qemu-aarch64` binfmt on the host before run.sh launches the ARM64 container, without breaking the upstream-symlink upgrade chain. Closes #440.
- **`build-worker.yaml` `free_disk_space` opt-in input** — pre-build cleanup step that runs `jlumbroso/free-disk-space@main` to remove ~30 GB of pre-installed runner tooling (Android SDK, .NET, GHC, tool-cache) so repos whose `BASE_IMAGE` exceeds ubuntu-latest's ~14 GB free disk (Isaac Sim ~15 GB extracted) stop deterministically hitting `no space left on device` during the BuildKit COPY phase. Default `false` preserves zero behavior change for existing small-image callers; downstream opts in with `with: free_disk_space: true`. Step is positioned before `Set up Docker Buildx` so the overlayfs snapshot dir lands on the freed space. Closes #470.
- **`runtime.env` emitted by `setup.sh apply`** — `[environment] env_*` entries land in a new `runtime.env` file alongside `.env` / `compose.yaml`, with the same cross-ref expansion as compose. Standalone scripts that bypass compose (e.g. `docker run` wrappers, host-side helpers like `isaac/script/run_instance.sh`) can now `source runtime.env` and see the same values compose injects, instead of getting empty `PUBLIC_IP` (WebRTC ICE fell back to 127.0.0.1). Backwards compatible: `.env` and `compose.yaml` unchanged; opt-in for callers that need it. Added to `_canonical_gitignore_entries` so downstream repos pick it up via the next `make upgrade`. Closes #462.
- **TUI mount mode picker for `[devices]`/`[volumes]`** — new `_prompt_mount_with_picker` walks the user through host path, container path, access mode (`ro`/`rw`/none), and propagation mode (`rslave`/`rshared`/`rprivate`/`slave`/`shared`/`private`/none) via separate radiolist prompts. Pure `_assemble_mount_value` helper builds the final `host:container[:mode]` string. Lets users discover propagation modes from #450 without reading docs. Closes #461.
- **`runtime/smoke.sh` ldd-based missing-dep check** — new helper script scans `.so` files under given roots (default `/usr/local/lib` + `/opt/ros/*/lib`) and fails if any has a "not found" dependency. Default `RUNTIME_SMOKE_CMD` in `Dockerfile.example` now invokes it, catching missing shared-library installs that the old `whoami && bash --version` default silently passed (e.g. `libboost_regex.so` absent in ros1_bridge#123). Downstream repos that uncomment the runtime-test stage get the stronger check automatically. Closes #430.

### Changed
- **`[logging] local_path` gitignore sync moved to init/upgrade lifecycle** — previously fired on every `setup.sh apply` (so the `.gitignore` managed block was only refreshed when a wrapper ran). New `lib/gitignore.sh::_sync_logging_gitignore` is called from `init.sh` (both new-repo and existing-repo paths), and `upgrade.sh` re-runs `init.sh`, so the file stays in step across template versions even when no wrapper has fired since the last `setup.conf` edit. Behaviour-equivalent: same marker block, same prune logic. `_parse_ini_section` also relocates from `setup.sh` to `lib/conf.sh` so `init.sh` can reach the parser without sourcing `setup.sh`. Closes #402.
- **`[logging]` parsers extracted to `lib/conf_logging.sh`** — `_parse_logging_svc_sections` and `_collect_logging` moved out of `script/docker/wrapper/setup.sh` into a new shared lib, wired via `lib/_lib.sh`. Internal refactor only; no behaviour change. Sets up PR-B (#402) where `lib/gitignore.sh` will reuse the same parsers to take over the `[logging] local_path` gitignore sync from `setup.sh apply`. Refs #402.

### Fixed
- **`run.sh` non-devel stages now 
[...截斷，原長 6456 字]

# ===== base doc/changelog/v0.41.md（截到 6000 字） =====

# base changelog -- v0.41

Part of the [changelog index](CHANGELOG.md).

## [v0.41.0] - 2026-06-10

### Added
- **`justfile` user-facing entry point, additive alongside the Makefile (#545, ADR-00000005 phase 1)** — new `script/docker/justfile` (symlinked from the downstream repo root as `justfile` by `init.sh`) provides `just <verb>` recipes (`build` / `run` / `start` / `exec` / `stop` / `prune` / `setup` / `setup-tui` / `upgrade` / `upgrade-check`) that forward 1:1 to `./script/<wrapper>.sh` with full `{{args}}` passthrough. Because `just` does not treat `VAR=VALUE` as overrides or consume `--`/`-flag` argv for itself, the make-era workarounds (`MAKEOVERRIDES` guard #414, mandatory `--` separator #448, `EXEC_ARGS` shim #469) are simply unnecessary: `just exec -t cli --/app/k=v` passes through verbatim. Bare `just` runs `just --list` (replaces `make help`). This is the **additive** phase -- the Makefile stays; its retirement + the downstream fanout is #546. `Makefile.ci` is unrelated and stays on make. Closes #545. Refs ADR-00000005, #475.
- **TUI runtime-env (`.env`) info page (#497 acceptance: TUI points at the `.env` overlay)** — `setup_tui.sh`'s Runtime sub-menu gains a `workload env (.env)` entry whose page is **informational only**: it explains the #502 two-role split -- volatile per-task env vars (ROS_DOMAIN_ID, LOG_LEVEL, tokens) go in the hand-edited, gitignored `.env` overlay (taking effect with `make run` alone, no regenerate / no hash drift), while set-once defaults live in `[environment]` (baked as image `ENV`, emitted into compose, overridden by `.env` at runtime). Per the S2 (#502) invariant that `setup.sh` / the TUI never write `.env`, this is a guidance msgbox, not an editor. i18n in all four locales (en / zh-TW / zh-CN / ja). Refs #497, #502 (does not close #497 -- the remaining acceptance item is the 17-repo downstream migration tracked separately).
- **TUI legacy `runtime` -> `gpu_runtime` migration prompt (#517, fast-follow of #481)** — `setup_tui.sh`'s deploy page now detects when the per-repo `setup.conf` still carries the legacy `[deploy] runtime` key (and no `gpu_runtime`) and surfaces a migration suggestion msgbox -- it never silently rewrites the user's `setup.conf`. The deploy page reads the runtime value honouring both keys (gpu_runtime preferred, legacy `runtime` as fallback for the radiolist pre-selection) and writes the canonical `gpu_runtime` key on save, so editing via the TUI migrates the config forward; the user then removes the old line themselves. The per-stage scalar override prompt text now says `gpu_runtime (legacy runtime)` instead of `runtime`. i18n in all four locales (en / zh-TW / zh-CN / ja). Closes #517. Refs #481.
- **`[lifecycle]` restart TUI page (#514, fast-follow of #478)** — `setup_tui.sh` gains a Lifecycle page (under the Runtime sub-menu) for the `[lifecycle] restart` policy added by #478. A radiolist picks `no` / `always` / `unless-stopped` / `on-failure`; choosing `on-failure` adds a two-step optional integer retry count (>= 1; empty falls back to bare `on-failure`, assembling `on-failure:N`). Reuses `_validate_restart` from `lib/_tui_conf.sh`. i18n in all four locales (en / zh-TW / zh-CN / ja), including the value descriptions and the `always` / `unless-stopped` infinite-restart caveat (a stage that extends devel and exits 0 would loop). The feature was already usable via `setup.sh set lifecycle.restart` / editing `setup.conf`; this closes the interactive gap. Closes #514. Refs #478.
- **`lint_mixed_test_layout.sh` -- advisory lint for mixed-runner test layout (#495)** — new `script/ci/lint_mixed_test_layout.sh` warns when a `test/<category>/` directory holds files from more than one test runner at the same level (e.g. `.bats` + `test_*.py`), suggesting the `test/<category>/<tool>/` subdir split that ADR-00000004 (#473) defines. WARNING-only and non-blocking (it always exits 0): a mixed state is sometimes a legitimate mid-migration intermediate, so it surfaces the drift via `_log_warn` without failing CI. Wired into `ci.sh`'s `_run_shellcheck` lint phase (so it runs on the local `make test` path and the dedicated `--shellcheck-only` GHA job) and shellchecked itself. Downstream repos inherit the guard via the `.base/` subtree. Closes #495.
- **`ci.sh --bats-path <file|dir>` + `--filter <regex>` single-path test mode (#523)** — the test engine gains a fast TDD inner loop: `--bats-path` runs one spec FILE or DIRECTORY (repo-root-relative, resolved inside the `ci` container) and `--filter` passes a `bats -f` name filter (usable with or without `--bats-path`). Both run via the `ci` container reusing the existing env plumbing (`BATS_FILE` / `BATS_FILTER` / `BATS_ONLY=1`), skipping ShellCheck (covered by `--shellcheck-only` / full `test`) and kcov so iterating on one spec no longer forces the whole `test/unit/` + `test/integration/` suite. Guards: a path under `test/behavioural/` exits with a hint to use `make test-behavioural` (the host `ci.sh` cannot launch the `ci-behavioural` service); a non-existent path exits `ci_bats_path_not_found`; `--bats-path` + `--coverage` is rejected (single-path is the fast no-kcov loop). `Makefile.ci` stays a thin forwarder and is out of scope (#475). Closes #523.
- **Per-stage `[security]` cap_add / cap_drop / security_opt overrides (#526)** — the per-stage `[stage:<name>]` override allowlist (`_validate_stage_override_key`) is extended to `security.cap_add_<N>`, `security.cap_drop_<N>`, `security.security_opt_<N>` plus the matching `*_inherit` toggles, resolved through the same `_resolve_docker_flags` list layer as `volumes` / `ports` / `environment` (append-by-default; `<list>_inherit = false` replaces/clears). This lets a downstream drop capabilities / `security_opt` for individual stages instead of only image-wide: e.g. `ycpss91255-docker/jetson_sdk_manager` keeps `SYS_ADMIN` + `seccomp:unconfined` on its `flash` stage but a read-only `probe` stage sets `security.cap_add_inherit = false` (+ `security
[...截斷，原長 39409 字]

# ===== base doc/changelog/v0.42.md（截到 6000 字） =====

# base changelog -- v0.42

Part of the [changelog index](CHANGELOG.md).

## [v0.42.0] - 2026-08-25

`v0.42.0-rc4` promoted unchanged -- the tree is identical apart from this
version bump, so the entries stay under the RC headings that introduced them
rather than being duplicated here. The release is the sum of `v0.42.0-rc1`
through `-rc4`; the compare links at the foot of this file walk it.

## [v0.42.0-rc4] - 2026-08-25

### Fixed
- **nine more early-closing readers, and the class that inverted the answer rather than losing it (closes #905)** -- #898 fixed one `| sort | head` that died 141 under `pipefail`; confirming it turned up nine more instances of the same mechanism, one class of which is worse than the bug that was fixed. A reader that stops reading (`grep -q` leaves on its first match, `head -n1` after one line) strands a writer that is still writing: SIGPIPE, exit 141, `pipefail` promotes 141 to the PIPELINE's status, and an `if` reads that as false. **A successful match is reported as "not found"** -- the status is not lost, it is inverted, and nothing fails loudly; the caller simply takes the other branch. Whether the race is lost is environment-dependent, measured during #898 at **0 failures in 20000 host iterations** (glibc, bash 5.1) against **6.4% inside the alpine test-tools image** (musl, coreutils 9.5, bash 5.2), so "I ran it and it was fine" is not evidence here -- and five of these ship in `dist/`, which every downstream repo executes on whatever host it has. **Class B, the inverted answer (5 sites).** `run.sh`'s already-running guard reported a LIVE container as not running and started a second one over it, instead of refusing; `exec.sh` took the same test negated and refused a container that WAS running, telling the user to start it; `detect_gpu` reported an installed `nvidia-container-toolkit` as missing, so `setup` wrote a GPU-less `.env` on a GPU host; `completions.sh` re-printed the `fpath` hint for a directory already on `$fpath`; and the base-version monitor's dedupe gate read an already-open tracking issue as absent and filed a duplicate -- weekly, in every downstream repo, until someone upgraded. **Class A, the status thrown away (3 sites).** `upgrade.sh:_get_latest_version`, `init.sh:_detect_template_version` and `gitignore.sh:_prune_retired_entries` each met the abort and answered with `|| true`, which stops the crash by discarding the status -- including a genuine failure of the pipeline -- and leaves a quieter defect: an EMPTY answer that reads as a legitimate "nothing found" (no newer release when there is one; a repo stamped with no template version; a retired entry never retracted from the downstream `.gitignore` the template was trying to clean). #898 deliberately did not take that route, and neither does this. **Class C (1 site).** `_tui_conf.sh:_detect_mig` had no suppression at all: 141 straight out of a bare assignment. The live caller is `if _detect_mig; then`, and `if` suspends errexit for the whole function body, so it misreported rather than aborting -- a MIG-enabled host told it had no slices, withholding the UUIDs the user needs for `NVIDIA_VISIBLE_DEVICES`; called outside a condition the same 141 kills setup outright (pinned at status 141, no output). **Every fix removes the dependency rather than the symptom**: each site drains its stream with a `while IFS= read -r` loop over a process substitution and compares in-shell, so no exit status depends on how two processes were scheduled. No `|| true` survives and `pipefail` is untouched. `run.sh` and `exec.sh` asked the identical question with the identical spelling, so the probe is hoisted to `lib/wrapper.sh:_wrapper_container_running`, the module that already owns what the five docker wrappers share. Dropping `grep -oP` from the two tag scans also drops a PCRE dependency that does not exist on a BSD / macOS host, where both had been silently returning `""` behind the `|| true`. **Testing is deterministic, not repeated**: two shared helpers in `test/bats/unit/test_helper.bash` pin the losing interleaving with PATH shims -- a reader that exits without reading a byte, a writer that writes only after it has gone -- so a reintroduced pipeline fails on EVERY run instead of a few percent, the technique `adr_numbering_spec` established in #898. Nine specs gained a case (`run_sh` 67, `exec_sh` 58, `setup_detect` 50, `completions` 14, `base_version_monitor` 13, `upgrade` 48, `init` 53, `gitignore` 47, `tui` 135). `upgrade_spec`'s errexit/pipefail case is rewritten rather than deleted -- it pinned a real contract (rc=0 and an empty answer on an unreachable remote, so `_check`'s guard is what reports it) while describing `|| true` as the mechanism -- and its strict shell became a script FILE, which un-skips it under `COVERAGE`: `bash -c '...'` leaves `${BASH_SOURCE}` empty at top level, so kcov's `PS4` killed it under `set -u` before the code ran, and it had been skipping in precisely the environment where this defect reproduces. **Recurrence guard, with the false-positive count measured before building it.** A naive whole-tree rule is worthless: bats test bodies run with errexit ON and pipefail OFF (measured -- `false | true` yields 0 there), so all ~65 `| head` / `| grep -q` lines under `test/bats/**` are structurally incapable of the inversion, giving ~65 candidates and 0 true positives. Scoped to `dist/` + `script/`, the shell that actually runs under `set -euo pipefail`, the same rule flagged **exactly the nine defects and nothing else** -- and replaying it over every release from v0.30.0 to v0.41.0 flags the same six lines (the nine, before the tree was reorganised) and never anything else, i.e. **zero false positives across twelve releases**. That is the opposite of #895's rejected rule (68 candidates, ~11 true positives, >80% false positive), so this one is built: new `early-close-reader` lint (`script/test/drivers/early_close_reader.sh`, `just test lint --early-close-reader`, `test.sh --early-
[...截斷，原長 326840 字]

# ===== base doc/changelog/v0.43.md（截到 6000 字） =====

# base changelog -- v0.43

Part of the [changelog index](CHANGELOG.md). Entries for the release
being written land here; the format is in
[CONVENTIONS.md](CONVENTIONS.md).

## [Unreleased]

### Added

- **publish toml-bridge image to GHCR (refs #1150)** --
  `release-toml-bridge.yaml` publishes the containerised TOML parser to
  `ghcr.io/ycpss91255-docker/toml-bridge` as a multi-arch image
  (linux/amd64 + linux/arm64). Triggers on release tags (`v*`), main
  push (paths-filtered to Dockerfile and script changes), and manual
  dispatch. Tag resolver reuses `release-ref.sh` for prerelease
  classification, matching `release-test-tools.yaml`. Downstream
  consumers -- primarily multi\_run -- can `FROM` the published image
  instead of building locally.

- **containerised TOML parser: toml-bridge image, bash shim, and
  test-tools integration (refs #1128)** -- ADR-37 delivers TOML config
  parsing without adding host dependencies. `Dockerfile.toml-bridge`
  builds a standalone image (Python 3.13 alpine + vendored tomli 2.4.1)
  that reads TOML from stdin and writes JSON to stdout.
  `toml_bridge.sh` is the host-side bash shim calling `docker run`.
  `Dockerfile.test-tools` gains a `COPY --from=toml-bridge-src` stage
  so downstream repos inherit the parser. Nine unit tests across three
  seams (Dockerfile structure, bash shim with mocked docker, test-tools
  COPY integration).
- **conf.sh TOML bridge integration (refs #1129)** -- `_conf_load`
  auto-dispatches to the containerised TOML parser for `.toml` files
  while preserving the INI path for existing `.conf` files. The bridge
  gains a `--kv` output mode (tab-separated `section\tkey\tvalue`
  lines) and a new `_toml_tokenize` function fills the same four
  parallel arrays as `_ini_tokenize`. Five unit tests with mocked
  docker verify the KV format, array population, accessor API
  compatibility, and INI backward compatibility.
- **type-aware merge semantics for TOML layers (refs #1130)** --
  `toml_bridge.py` gains a `--merge` mode that reads multiple TOML
  files in precedence order and merges them type-aware: scalar keys
  within `[table]` sections get key-level merge (upper overrides only
  defined keys; unmentioned keys inherit), while `[[array of tables]]`
  entries get array replace. `toml_bridge.sh` gains `toml_bridge_merge`
  shim function. `_conf_load_layers` auto-dispatches to the bridge when
  all files are `.toml`, replacing bash section-replace with Python
  type-aware merge in a single `docker run`. ADR-00000001 and
  ADR-00000025 sec. 3 amended. Six unit tests with mocked docker.
- **setup.toml template: migrate .setup.conf to TOML (refs #1132)** --
  `dist/setup.toml` replaces the 321-line INI template. All 15 sections
  migrate: scalar sections as `[table]`, eight numbered-key sections
  (`mount_N`, `arg_N`, `rule_N`, etc.) become `[[array of tables]]` with
  typed fields. `toml_bridge.py` `_emit_kv` gains `_ARRAY_SPEC` to
  serialize arrays back to numbered-key KV format for backward compat
  with existing emitter consumers. Five unit tests.
- **a lint refusing the next whole-tree scan in the coverage suite (refs #1075)**
  -- `spec-repo-root` fails any spec under the coverage pools that points a
  `*REPO_ROOT` at the live checkout, resolving one hop of indirection inside
  the file so a name holding the mount counts as the mount. Nothing in it is
  a roster: the files come from `_COVERAGE_FULL_SUITE_POOLS`, the refused
  roots from `compose.yaml`'s bind for `.` plus the live `${REPO_ROOT}`. It
  dies rather than reporting clean on any of six vacuous states, the
  blind-detector case among them, and runs in a `lint-static` group like
  every other computed member.

### Changed

- **the coverage suite tests a lint against fixtures; the tree is the lint
  job's (closes #1075)** -- 23 specs pointed a driver's `REPO_ROOT` at the
  live checkout, so they ran the LINT, under kcov, on the coverage matrix's
  critical path. One was 331s of a 501s shard against a 211s median: 66% of
  that path in a single test, the atom no partition splits. All 23 go; each
  duplicated a `lint-static` job. Coverage was measured first -- they were
  worth 11 lines, all `changelog_index.sh` branches only the live changelog
  reaches, and four new fixture cases now state what that route merely ran,
  so the covered set is unchanged at 8591/10195. The slowest of 12 shards
  falls 268.2s to 190.6s.

- **the test-description ceiling follows the removals down (refs #1075)** --
  twelve of the twenty-three deleted cases were undescribed, so the tree's
  undescribed count falls 2578 to 2566. `_CATALOG_DESC_UNDESCRIBED_CEILING`
  goes down with it rather than keeping the difference as slack: a ceiling
  left where it stood would let twelve undescribed tests land green on the
  strength of a deletion. Slack is back to 0.
- **a lint for CI jobs that run undeclared tools (refs #1080)** --
  `tool-provenance` asks, of every workflow job, whether every pinned tool it
  reaches comes from the tooling image or from the one declaration. Demand is
  read from the job's shell, substitutions included, and from the source of
  the driver a host-direct `--<lint>-only` / `--lint-group` selector names; a
  comment is neither. Tools come from the pin roster and jobs from the
  workflow directory, so neither a new pin nor a new job joins in silence.
  What it cannot resolve it REFUSES instead of scoring as no demand: a
  job-level line that is no job key, a file it read no job out of, a
  dispatcher that will not name a group's members.

- **the PRD says how completeness is judged, without saying the number
  (refs #1096)** -- base must express every compose field a single-container
  repo in this org actually uses, and that population is derived from evidence
  (a hand-written compose file, a set key, a request, a workaround) rather than
  maintained as a list. Measured against the whole spec base sits at 29 of 92;
  against what is used, 28 of 38. The rule is recorde
[...截斷，原長 88574 字]
warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
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
tokens used
228,913
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
