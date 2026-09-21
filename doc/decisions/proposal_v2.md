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

---
# v2.3 修訂（2026-09-19，第二輪審查後；Q10=(2)、Q11=(b)、Q12=strategy、Q13=(2) 已定；與前文衝突以本節為準）
1. **init.toml 欄位**：`strategy = "copy" | "append"`（預設 copy）；全部圖文不得再出現 mode。append：首次確認後加入並記在 metadata（實際插入的行）、重跑不重複、upgrade 只對可辨識的上次插入行提修改；比對 CRLF/LF 等價、其餘精確；零命中或多處 → 保留只 warn。
2. **自身升級（統一版）**：
   - `upgrade`（不帶 repo）遇引擎有新版：舊引擎 apply 只改 version.toml 第一行，回報「引擎已變」→ **啟動器在同一次指令內** `docker pull` 新引擎 → 用新引擎跑 `upgrade vendor_kit`（比對現薄殼 == 上次產物 hash → 重產薄殼 + gen/.stamp）→ 結束 1 印「已升級引擎 vX→vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」。
   - `upgrade vendor_kit`：啟動器讀第一行（local 覆寫優先、`--pull never`）→ 該引擎跑 → 比對 hash → 重產 → 1 同上（被改過 → 1 列差異不動）。
   - 別人 pull 後 sync 發現 gen/.stamp ≠ 第一行 → 只回 1 提示 `upgrade vendor_kit`；**install／upgrade vendor_kit 本身不被這關擋**（啟動器對這兩個動詞跳過該檢查）。
   - 結束狀態 1 的「不動 version.toml」只對工具層動詞成立；自身升級已改第一行後回 1 是明列例外。
3. **印記位置**：每工具印記 `.vendor_kit/gen/<repo>.stamp`（第一行 index digest 或 path:/image:，之後每檔 sha256）；cache/<repo>/ 只放展開內容（dev 時為唯讀 symlink）。`gen/.stamp` = 引擎 ref + 薄殼各檔 hash，只由 install／upgrade vendor_kit 寫。gen/tools.just 由 sync／add／remove／upgrade 重生（每個 <ns>.just 一行 mod）。
4. **sync 判斷順序**：對每工具：覆寫 path → 跳過 materialize/verify（仍查 metadata/baseline）；cache 缺 或 印記第一行 ≠ 鎖定 digest → materialize（不 verify 舊 cache）；否則 verify sha256 → 失敗 → 重裝 + warn。第一段（resolve）結束後：無待辦 → 快路徑 0；有待辦 → 啟動器 docker → apply。
5. **動 image 的動詞** = add／upgrade／sync／undev（undev 要重新 materialize 鎖定版）；install／remove／uninstall／update／dev 不經 docker create/cp。
6. **apply 通則**：拿 flock → 重驗指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 才做任何寫入；衝突狀態清除、append 行修改、baseline 刪除等都在 apply 內、拿鎖後；進度日誌（metadata state=in-progress）在第一個寫入前建立、最後一步刪除。uninstall：先預檢（hash 相符清單）→ 再逐工具 remove → 再刪自產檔；未知／被改的保留。
7. **dry-run**：所有頁一致——本機：唯讀預覽 → 0；CI=1 且需改 tracked 檔 → 1 印清單。
8. **架構頁**：只留模組／最小單元／資料流，不留任何順序鏈；根 justfile（使用者的）與自有薄殼分開兩類；GHCR 拉取條件 = cache 缺／鎖定 digest 變／verify 失敗。
9. **圖面**：每格一件事（動作／判斷／檔案／單元）；橢圓、菱形內文字以形狀內接矩形估算（橢圓 ×0.707、菱形 ×0.5）；不出現「v1 叫…」對照；名詞表覆蓋 resolve／apply／stdout／stderr／flock／materialize／image ID／VENDOR_KIT_REGISTRY_TOKEN／symlink／import／CRLF／metadata／baseline 等該頁用到的詞。

---
# v2.4 補充（2026-09-19 grilling Q14–Q21、相容性、19 條、deploy；全部 [定]）
1. **Q14 新版新增初始檔**：upgrade 問「要建 X 嗎」（-y 建）；拒絕 → metadata 記 declined，之後不問但 dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑時訊息醒目；工具契約：初始檔只引用穩定入口 `just <ns> …`，不得寫死 cache 內部路徑。
2. **Q15 不納管／拒絕過的檔**：metadata 四種狀態（已納管／拒絕過／本來就有沒納管／使用者刪了）；dry-run 與 check.sh 印「X 沒納管，與範本差 N 行」「Y 你拒絕過，vZ 有新版」；不動檔不紅燈；新版有更新對拒絕過的檔再問一次。
3. **Q16 相容承諾兩層**：薄殼每次呼叫附 `--protocol P`（從第一版就有），引擎依 P 回應。永久：任何舊薄殼可呼叫新引擎的救援路徑（install／upgrade vendor_kit／sync 不符提示；單段 docker run，不依賴 resolve/apply 與 gen）；舊資料永遠可讀可遷（讀任一舊 schema → 直接寫當前 schema）。非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 **3** 提示先 upgrade vendor_kit。floor = 固定 release 常數（第一個正式版），只能經 ADR 提高。
4. **Q17 薄殼自描述**：entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：`# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>`；引擎重算 + 對 image 內模板二次比對；不符 → 1 列差異不動。gen/.stamp 只記引擎 ref。
5. **Q18 舊 bootstrap.sh 再跑**：專案已有 version.toml → 用該行引擎跑 install（不用內嵌；拉不到即失敗）。
6. **Q19 降版**：`upgrade vendor_kit -t 舊版`：舊引擎能無損讀現有檔 → 成功；否則改檔前拒絕印「請 git revert」。結束狀態 **3 = 協定不合／版本太舊**。`dev vendor_kit -i 舊 image` 禁止重產 tracked 薄殼。
7. **相容性機制**：每個 vendor_kit 寫的 TOML 有 `schema = N` + 寫入者版本；同 schema 只加不改、讀忽略未知寫保留；version.toml 契約 = 唯一符合 `^vendor_kit\s*=` 的行（禁 BOM／重複鍵／表旁路）；新讀舊記憶體轉換、只在本來要寫該檔的明確動作寫回；讀先出貨寫延後；tools.just 最後寫、與 cache 同一 apply 內原子替換；已釋出 image／Release 資產／fixture 永不刪；Renovate preset 建議 major 分開 PR。驗收：floor 以來每個已釋出 bootstrap.sh + image 驅動候選（線性）、每版最低環境（docker 19.03、just 1.33）跑完整、其他環境按世代；補列只改第一行後 frozen sync、fresh clone 無 gen、使用者改薄殼／未納管檔、中斷重跑、歷史 parser × 異常 TOML、升級後 == 全新安裝比對（排除時間戳／digest）。
8. **Q20 專案根**：= 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印路徑）；引擎不讀 .git、不碰 index；禁止巢狀（install 時上層已有 .vendor_kit/ → 1）；目錄須在某 git repo 內。
9. **Q21**：vendor_kit 只搬移；dist 可執行性是工具 repo 責任（check.sh --dist + 自己的測試）。
10. **19 條**：引擎 LC_ALL=C.UTF-8、TZ=UTC、時間戳 UTC ISO 8601；容器以 host uid:gid 跑、HOME 指容器內暫存（實作細節）；啟動器 trap 清容器與暫存；需詢問但無 tty/EOF → 1 印「加 -y 或在終端執行」；路徑含空白一律引號；**prune 第一版做**：所有 docker 資源（容器／image／network／volume）帶 vendor_kit label，prune 依 label 刪 version.toml 未引用者，驗收含故意留 network/volume；不建 network/volume（驗收差集為空）；**pull 逾時 v1.0.0 必做**（預設 + 可調參數）；rootless docker（setup-docker-action rootless）與 Podman（runner 內建）進驗收；Docker Desktop／proxy／自簽 CA／引擎基底 EOL → issue v2；SELinux 不支援；離線 upgrade 不支援（local_bootstrap.sh 只涵蓋 install/add --local）；submodule 派子代理實測；worktree 驗收加案例。
11. **deploy**：工具契約一句「交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR」；vendor_kit 不檢查；version.toml 公開格式可供來源紀錄。
12. **remove/uninstall 進度日誌**放 `.vendor_kit/.tmp.*`；add/upgrade 記 metadata state=in-progress。
13. **文件位置（照 skills）**：根 README（入口）、CONTEXT.md（名詞）、`docs/adr/` 短格式、`docs/agents/`；spec → issue → tickets；不建 PRD.md／ADR 索引／模板；圖上不放決策便條與 ADR 編號（整合進主圖時全部拿掉）。

---
# v2.5 澄清（2026-09-19 第三輪審查後；只澄清、不改決策）
1. **CI 與 -y**：`CI=1` = frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，**與 -y 無關**（-y 只在本機免詢問）。所有頁的判斷格寫「CI=1 且需改 tracked 檔？」，不寫「無 -y」。
2. **N（新版範本）的來源**：啟動器把目標版 image 展開到**暫存目錄**並掛進引擎 `/dist/<repo>:ro`；逐檔判斷（B/D/N）與 dry-run 都讀 `/dist/<repo>`，**不是 cache**；materialize 到 `cache/<repo>/` 在 apply 決定套用之後才做。名詞表：N = 目標版範本（暫存 /dist/<repo>）。
3. **apply 順序（所有動詞）**：拿 flock → 重驗指紋 → dry-run 分支（唯讀：本機 0；CI 需改 tracked → 1）→ **建進度日誌（第一個寫入前）** → 其後所有寫入（含清除衝突狀態、append、baseline、metadata、cache、tools.just、version.toml）→ **最後一步刪日誌**（uninstall 在根 justfile 那行之後）。remove/uninstall 日誌在 `.vendor_kit/.tmp.*`。
4. **詢問一律有拒絕分支**：拒絕 → 不寫、metadata 記 declined（append／新檔／換新版／合併皆同）。
5. **add 前置檢查**加：工具 `dist/just/<ns>.just` 的命名空間與（a）其他已接工具（b）根 justfile 既有 recipe／module（c）保留名 `vendor_kit` 撞名 → 1 拒絕（base ADR-10 撞名整個 just 掛）。
6. **upgrade 前置檢查**加：目標工具在 dev 覆寫中 → 1 提示先 undev（與 remove 同）。
7. **自身升級 (a)**：resolve 先判斷「引擎有新版？」否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 回報引擎已變 → 啟動器：local 覆寫有 `vendor_kit=` → 用該 image `--pull never`，否則 pull 新引擎 → 新引擎 `upgrade vendor_kit`。結束 1 的顏色：**「需要人動作」用橙色橢圓**（含自身升級後重跑、協定太舊 3），紅色只給失敗。
8. **install 的「第一次／修復」判定**用薄殼自描述首行（Q17），不用 gen/.stamp：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 列差異。`--local` 的 version.local.toml 在 install 成功後才寫，失敗清除。install 建 `baseline/`（空）+ 不建 metadata（add 時才建）。
9. **sync 可寫範圍** = `cache/<repo>/`、`gen/tools.just`、`gen/<repo>.stamp`；快路徑前要判斷 tools.just 是否缺或需重生。gen/ 有三種檔：tools.just、.stamp（引擎 ref）、<repo>.stamp。
10. **undev**：撤覆寫行含 image ID 欄位；建日誌後才動。**uninstall**：resolve→apply 兩段、重驗指紋、保護清單（hash 相符）在任何 remove 之前生效，逐工具 remove 走「保護模式」（未知／被改的檔保留）。
11. **append 行多處命中** → 保留並 warn（Q13），圖上三分支：唯一命中／零命中／多處。
12. **架構頁**：箭頭只標「傳遞的資料」（不標動作）；讀寫用雙箭頭；version → local 方向依讀寫；紫 = 兩種 image 都算（legend 改「image：引擎與工具」）。
13. **check.sh --dist 擋 CRLF**：已定於 issue #29（dist 文字檔一律 LF），圖上標 [#29] 而非 v2.3。
14. **檔案框一格一檔**（多檔用一個標題容器內排多個小框）。
15. **橢圓文字**：draw.io 以外框寬換行 → 橢圓一律加 `spacingLeft=spacingRight=w×0.146`、`spacingTop=spacingBottom=h×0.146`，check_overflow 對橢圓改用「w−2×spacing」估；菱形同理 ×0.25。

---
# v2.6（2026-09-19 規格審查 16 條必修 + Q22–Q27；圖面全部要套；與前文衝突以本節為準）
1. 引擎覆寫／本機 image：**不用 `--pull never`**（docker 19.03 無此旗標）；啟動器先 `docker image inspect --format '{{.Id}}' <ref>` 驗本機存在（並比對 metadata 記的 image ID），存在就直接 `docker run`（預設不 pull），不存在 → 1。主機命令白名單：sh、grep、sed、id、mktemp、rm、git rev-parse、docker {pull,create,cp,run,rm,inspect,load,ls,image rm,network rm,volume rm}。
2. **CI 真值規則**：`CI` 非空且不為 `0`/`false` 即為 frozen（GitHub/GitLab 都設 `CI=true`）；圖上一律寫「CI 為真（frozen）」，名詞表定義真值；check.sh 自己 `export CI=1`；`-y` 不解除 frozen。
3. `gen/tools.just` 一律 **`mod?`**（`mod` 指向缺檔會讓所有 just 呼叫掛掉）。
4. 根 justfile 新建時兩行：`import '.vendor_kit/entry.just'` + `default:`／`\t@just --list`（`default: @just --list` 一行是語法錯誤）。
5. `VENDOR_KIT_REGISTRY_TOKEN_FILE` 以 `-v <file>:/run/vk-token:ro` 掛進引擎；`VENDOR_KIT_NO_LOCK` 要轉發；resolve 永不加 `-t`；apply 互動時才 `-it`；「引擎已變」由啟動器 apply 前後 grep version.toml 第一行比對。
6. rootless docker 偵測到（`docker info` SecurityOptions 含 name=rootless）不加 `-u`；Podman 用 `--userns=keep-id`。
7. 工具契約：`Dockerfile.dist` 必含 `LABEL io.github.<org>.vendor_kit=1`（+ protocol/schema label），`check.sh --dist` 擋；容器類資源加 `.project` label；prune 依 label。
8. 二進位／symlink：你沒改 → **問「X 換成新版？」** 後才換（不再「未改直接換」）。
9. 未知 TOML 欄位：讀時忽略、寫時保留（不回 1）；只拒絕型別錯／重複宣告。唯讀動詞（sync/update/help）遇未完成交易只提示重跑原動詞，不自動恢復。
10. `vendor_kit =` 行唯一正規形：整行 `vendor_kit = "<ref>"`（雙引號、無註解），regex `^vendor_kit[[:space:]]*=`；重複行 → 1。
11. 空 `baseline/`：install 建 `baseline/.gitkeep`（git 不追蹤空目錄）；metadata 由 add 建。
12. Renovate preset 放 vendor_kit repo 根目錄 `default.json`（下游 `extends: ["github>ycpss91255-research/vendor_kit"]`）。
13. Q22 sync 快路徑；Q23 結束碼 3 邊界（零寫入、schema/P 比較）；Q24 vk-resolve 格式（`|` 分隔、`\ooo` 八進位跳脫、首尾行、先收完再動）；Q25 選項表（-t/--tool <repo>[@tag]、-y、-p、-i、-h 有短；其餘長形；無 --tag/--repair/--purge）；Q26 離線 `.digest` 旁檔 + image ID 對照 + 斷網已有 image 必成功；Q27 多工具結束碼合併。install 加 `.dockerignore` 行（問後加）。
14. F1：工具模組內私有 `_sync` recipe（`cd {{quote(justfile_directory())}} && just vendor_kit sync`），公開 recipe 相依它；vendor_kit 自身動詞不前置；`--dist` lint 檢查。
15. 顏色：**橙 = 需要人動作（結束 1 或 3 且印指令）**：請先 undev／請先 add／請先 git init／請重跑／請 upgrade vendor_kit／解衝突（2 也橙）；**紅 = 失敗**（拉不到、寫入失敗、驗證失敗）。跨頁連接：每個「接 X 頁」的出口與入口都標頁名，入口用專用形狀（白底虛線橢圓「來自 p.X」）。
16. 拆頁：p1 → 「不變量與角色」「動詞介面表」「規則與不開的動詞」（名詞表隨頁）；p2 → 「目錄樹與檔案範例」「schema：version／metadata／印記／薄殼首行」「動詞×檔案矩陣」；p3 → 「工具 repo 契約③」「啟動器↔引擎契約④」「CI 契約⑤ + 驗收矩陣」。
17. **新增頁**：流程 prune；流程 update；狀態機：初始檔五態（managed/appended/declined/unmanaged/deleted）與轉移；狀態機：交易與進度日誌（in-progress → 完成／失敗 → 下次恢復）；相容性矩陣（舊薄殼×新引擎、舊引擎×新檔 → 0/1/3，floor）；結束碼決策表（動詞×情況 → 0/1/2/3）；流程：vendor_kit release（tag → 多架構 build → release-test → 驗收（已釋出版驅動候選）→ 發 bootstrap.sh／tar／.digest）；流程：離線包（local_bootstrap.sh → docker load → add --local → .digest）。

---
# v2.7 澄清（2026-09-20 第五輪審查後）
1. 離線包內含 `local_bootstrap.sh` 便利包裝（偵測 daemon 架構、挑 tar、`exec ./bootstrap.sh --local <tar> "$@"`），**不是契約入口**；契約入口 = `bootstrap.sh --local`。規格 §1.2 措辭改為此；release 頁與離線包頁可畫 local_bootstrap.sh 但標「便利包裝」。
2. B1（`--local` 判別）與 F5（`sync --verify`）已定（grilling 2026-09-19 末條），規格 §9.1 清空；圖上不再標待拍板。
3. **declined 語意**：`state=declined` 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新 → state 不變、只記 `declined_hash`（新版再變才再問）。二進位拒絕同。逐檔判斷表、五態狀態機、B(2)(2′)、名詞表一致。
4. 結束碼 3 零寫入，無任何例外（矩陣頁「救援路徑例外」刪）。
5. `upgrade vendor_kit[@tag]` 主流程：(1) @tag／frozen 不查，否則查 registry → (2) 有新版？是 → 改第一行 → 用新引擎重產 → 1；否 → 薄殼相符？是 → 0 無變更；否 → 重產 → 1；@舊版無法無損讀 → 3。
6. `undev vendor_kit` 走 resolve→apply，建 `.tmp.undev.<id>.toml` 日誌後才撤覆寫（含 image ID）；最後一個覆寫撤掉 → 刪整個 version.local.toml。
7. 交易狀態機：prune 特例分支——遇活躍日誌只列出不刪、不視為未完成交易。
8. update 頁：registry 查詢步驟不是 image，用白／藍（引擎子命令）不用紫；結束碼表 update「查詢失敗（無憑證 6-3）」為橙（需人動作）。
9. **逐字範例框**（根 justfile、`_sync`、Dockerfile.dist、TOML）一律 `whiteSpace=pre` 等寬、不置中、縮排用真 tab 或 `&nbsp;` 保留；不得用 html wrap（會吃掉行首空白）。
10. 一格一件事再細：`docker image inspect` 與 `docker pull` 分格；「讀 .digest」與「inspect image ID」分格；「建檔」與「印出」分格；「append」與「記 metadata」分格；四類資源逐類一格；判斷格只放一個問句（文字檔／二進位分開）；metadata 寫入拆欄位群；release 頁 v3/v4/v5/v8/v10/v11 拆。
11. 架構頁：pull_dist 線不穿泳道標頭；模組標題兩行時最小單元下移；名詞表 check.sh 步數統一「⓪–⑤ 六步」。
12. XML id 唯一（p12 重複 id 修）；頁名 `<repo>` 不要雙重跳脫。

---
# v2.8 澄清（2026-09-20 第六輪審查後）
1. uninstall 刪除集合補：專案層 `baseline/.gitkeep`、`baseline/.vendor_kit.toml`（記根 .dockerignore append 行）；刪完 baseline/ 目錄本身；目錄空才 rmdir .vendor_kit/。
2. install 進度日誌：第一次 install（薄殼不存在）不建日誌，失敗整包丟棄（不留半成品）；修復型 install 建 `.tmp.install.<id>.toml`。交易狀態機頁明列。
3. `upgrade vendor_kit`：「薄殼 == 上次產物？」檢查在拿鎖重驗之後、任何寫入（含改第一行）之前；不符 → 1 列差異，零寫入。
4. `--local` 判別三分支：含 `/` 或 .tar 結尾 → 檔案（**先驗存在，否則 1**）→ docker load；否則 tag；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37。bootstrap.sh 與離線包頁都畫。
5. 離線包：`bootstrap.sh --local <引擎 tar>` 只涉及引擎；`-t <repo>` 仍走 registry（需網路）。離線接工具 = 使用者另備工具 tar，`add <repo> --local <工具 tar>`（工具 tar 由工具 repo 提供，不在 vendor_kit 離線包內）。離線包頁改畫；名詞表說明工具 tar 來源。
6. dev vendor_kit：`docker image inspect` 由**啟動器**做（主機側），image ID 交給引擎。
7. 顏色：CI 拒絕 dev／local 覆寫屬需要人動作 → 橙。相容性矩陣降版列：無損 → 重產薄殼 → 1（非 0）。`--porcelain` 在不開清單標「不做（v2 候選）」而非「未定案」。update 無憑證分支不進 SemVer 解析，直接記失敗進下一目標。
8. 排版：prune apply 拆 flock／重驗／清理；add(2) 逐檔加迴圈「還有下一個 [[file]]？」；dev 起點與菱形留間距；uninstall(2) 交叉線；release 便條溢出；菱形入口用頂點；分支線上標「是／否」；install(2) 「兩行」改「四行」且用 pre 真 tab（同 p2）。

---
# v2.9 澄清（2026-09-20 第七輪後；全部為既有規格的圖面落實）
1. bootstrap.sh `--local`：不論值是 tar 還是 tag，前置檢查（git repo？just ≥ 1.33？）一律先做；tag 形**不讀 .digest**（只 inspect 本機 image ID，digest 從 metadata／version.toml 既有值）；tar 形才讀 `.digest`。
2. add：resolve 線上解析加分支「私有 image、未指定 @tag、無憑證 → 1 + 6-3」；dest 不合法／命名空間撞名 → 橙（需人動作）。
3. sync：逐檔 sha256 全驗條件 = `sync --verify` 或 CI 為真 **或 快路徑判定版本變動的那次**；sync(1′)、sync(2) 與便條一致。
4. upgrade B(2)(2′)：合併結果先在暫存**解析**（TOML／just 等可解析格式）→ 解析失敗 → 保留原檔、記 conflicts、該檔 baseline 不推 → 才對通過的檔原子替換；b15c 不接回「推 baseline」。
5. uninstall append 行：逐行比對，只刪仍與紀錄原文相同的行，缺失／被改的行跳過並 warn（不是全有／全無）。
6. prune：apply 建 `.tmp.prune.<id>.toml` → 清理 → 刪日誌；移除繞過 apply 的直達線。
7. 結束碼表：任何動詞（含 help、救援路徑）在 P < floor → 3 + 6-18、零寫入。
8. 動詞×檔案矩陣與目錄樹：修復型 install 寫 `.tmp.install.<id>.toml`。
9. 排版：離線包 o3t 與菱形重疊；bootstrap ae8n 標籤；dev 起點與菱形間距 ≥ 40（上輪反而重疊）；交易狀態機 t5 拆三格；update 加「還有下一個目標？」迴圈；離線包(2) o10p/o10e 拆；B(1) be7 少折；B(1′) 菱形對齊；sync(1′) te14 頂點。

# v2.10 澄清（2026-09-20 第八輪後；除 3、4 為明確化既有規格，其餘為圖面落實）
1. 顏色：「需要人動作」的 1 結束一律橙（dest 不合法／命名空間撞名／CI 拒絕 dev／dist/init.toml 不存在或不合法／--local 路徑不存在／6-37／.digest 旁檔缺）；紅只給拉取／寫入失敗。upgrade B(1′) b10dx、b10nx；離線包(1) o3bx、o3cx、o4x；dev <repo> d3a、d1x、d3c 全改橙。
2. `bootstrap.sh --local <tag>`（tag 形）寫入 version.toml 的正式 ref@digest 來源：專案已有 version.toml → 用該行；第一次接入 → 用 **bootstrap.sh 內嵌引擎 ref**（本機 image ID 只記到 version.local.toml）。離線包(1) o8e 明寫這兩個來源。
3. `add --local` **只收 tar**（新工具沒有既有 digest 可用；tag 形只有 bootstrap.sh 有意義）：值不是存在的 `.tar` 檔 → 1 + 6-24 類提示。§1.1 選項表的「tag 形」只適用 bootstrap.sh；離線包(2) o10q 不再宣稱 tag 三分支，改為「值是存在的 .tar？否 → 1」。
4. `upgrade vendor_kit`（E(c)）**不建進度日誌**，是進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）。圖上「apply（拿鎖、重驗、建日誌）」字樣改為「apply（拿鎖、重驗；不建日誌）」，名詞表同步。
5. 6-2b 只適用「第一行已改（或第二次又變）」；無新版、第一行未變而薄殼重產失敗 → 1 + 印原因（不是 6-2b）。E(c)(2) s13x 分兩個結束。E(a) s2lx：第一行已改後拉不到／ID 不符 → 1 + 6-2b（與 §3.4 一致）。
6. help 偵測未完成交易：印 6-33 但結束仍 0（§1.2 help「不偵測交易以外的任何狀態」+ 6-33「help 不受影響」）；p1 名詞表改寫「sync／update 印 6-33 結束 1；help 印 6-33 仍 0」。
7. 文字修正：B(2′) b18 加「除解析失敗檔外」；update bU 結束碼 0／1／2／3。
8. 一格一事：install(2) igx／igz 的「修復型先刪進度日誌」拆成獨立步驟格（與「是」分支同型）；prune q12c／q12d 各拆「刪 X」+「日誌 done」；sync(2) m3v 拆「逐檔 sha256 驗證」與「失敗 → 重裝 + warn」；目錄樹 t_tmp 拆 `.tmp.<verb>.<id>.toml` 與 `.tmp.dist.<id>/` 兩格；schema 表 version.local／metadata 的 schema、written_by 各一列。
9. 排版：架構圖 f_user 標題兩行被內框蓋（內框下移或容器加高）；bootstrap(1) ae11b 與 ae6y 交叉；install(2) ie13 少折；add(2) ce28n／ce28y 標籤離開框緣；i4ld「否」標籤；T 接改各自入口（sync(1) ne5x／ne5y、E(a) se6px／se6vx、E(c)(1) se11px／se11vx）；離線包(2) o10a／o10c 寬度統一；契約④ d2_in 線上「③」改標到群組標題或移除；迴圈菱形：bootstrap(2) a10l「還有下一個 -t？」、sync(1′)「還有工具？」；install(1) i4en 不再匯入 i4ld（第一次 = 全新建直接接建檔步驟）。

# v2.11 澄清（2026-09-20 使用者定案）
1. **撤回 v2.10-4**：`upgrade vendor_kit`（E(c)，以及 E(a) 的自身那段）**一律建進度日誌** `.tmp.upgrade.<id>.toml`（記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending），在改 version.toml 第一行之前建；新引擎重產薄殼完成後由新引擎刪。未完成 → 可寫動詞先恢復（＝重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 印 6-33 仍 0。理由：規則統一（所有可寫動詞第一個寫入前必有進度日誌），不設例外。E(c) 兩頁、E(a)、名詞表、目錄樹、矩陣同步。
2. v2.10-3 維持：`add --local` 只收 tar；**不提供 `--digest` 選項**（使用者：想不到用途）。
3. 新需求（待 agy → 雙軌 → 定案）：**操作紀錄檔**——每個動詞每次執行除了印 tty 還要寫檔（做了什麼、哪些執行過）；log 資料夾明確 ignore（.gitignore／.dockerignore）；格式參考業界推薦與使用者筆記（JSONL、OTel Logs Data Model 欄位、jq／lnav）。見 `decisions/log/`。

# v2.12 操作紀錄檔（2026-09-20 使用者逐題定案 L1–L5；L6 依建議先行、**待 codex 審過才最後定案**）
- L1 位置與切割：`.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`，一次執行一檔（前例 npm `_logs/`；base `log/<verb>/<ts>-<traceid8>.log`）。`.gitignore`／`.dockerignore` 由 install 加 `.vendor_kit/log/`；目錄內自帶 `.gitignore`（`*`／`!.gitignore`）。不做 latest symlink。
- L2 格式：JSON Lines；欄位 `timestamp`（ISO 8601 UTC 微秒）、`severity_text`、`event_name`（有限集合，對齊現行 OTel Logs Data Model 的 EventName）、`body`（人讀一句話，選填；凡印到 tty 的訊息一律同句進 body）、`trace_id`（32 hex）、`attributes{component: launcher|engine, verb, …}`。使用者 Notion 筆記已同步改為 event_name。
- L3 保留：每個動詞目錄各自「最近 30 天且最多 50 檔」（stricter wins；base 為 20／14）；年齡用檔名時間戳、計數用檔名排序；啟動器結束時 prune、best-effort。
- L3′ 設定：新檔 `.vendor_kit/config.toml`（進 git；install 建立含註解與預設值；缺檔或缺鍵 = 預設）`schema = 1`、`[log] keep = 50`、`days = 30`；非正整數 → 預設 + 警告。upgrade 對它 = 三方合併初始檔。引擎用 TOML parser 讀（**parser 以 stage 明確帶進引擎 image**：`COPY --from=ghcr.io/ycpss91255-docker/toml-bridge:<tag>@sha256:…`，不依賴基底 Python 的 tomllib）；啟動器 grep 正規行 `^keep *= *[0-9]+ *$`（**待議**：config 鍵變多時改由引擎產啟動器專用平面檔或其他方式）。
- L4 寫失敗：**先確認能寫才開始**——啟動器 mkdir + 建檔 + 寫 `launcher_start` 失敗 → 1 + 6-38、零寫入；引擎 append `engine_start` 失敗 → 1 + 6-38、不進 resolve。所有動詞一致（含 help／prune），無 `--no-log`。磁碟滿連 prune 也擋：6-38 附清空間提示；紀錄以備追責。
- L5 實作：移植 base `dist/script/docker/lib/log.sh`（API `_log_<level> <event> [k=v]…`、事件註冊表 `log-events.txt` 未註冊即 FATAL、lnav format、bats）到 POSIX sh：跳脫改 `decisions/log/json_escape_fixed.sh`（dash＋busybox 實測）、`body`→`event_name`、`service.name`→`component`＋`verb`。啟動器 `launcher_start` 記**完整原始 argv**（逐項跳脫，不論合法與否）；引擎 `engine_start` 再記一次收到的 argv；引擎 Python `logging` + JSON formatter（`json.dumps`）append 同一檔，不引 OTel SDK。trace_id 由啟動器產（`/proc/sys/kernel/random/uuid` 去 `-`，缺則 `od -An -N16 -tx1 /dev/urandom`；啟動器工具清單加 `od`、`tr`），同值 = 進度日誌交易 id，`TRACEPARENT` 傳給引擎。驗收：每個 log 檔逐行 `json.loads`；bats 餵 `"`、`\`、換行、`[`、非 ASCII argv。開 issue：base 反向採用 vendor_kit 的 POSIX log.sh（單一 owner）。
- L6 事件集合（先依建議；待 codex）：啟動器 `launcher_start`（argv、verb、engine_ref、cwd、launcher 版本、CI 真值）、`config_read`、`docker_pull_start/finish`、`docker_extract`、`engine_spawn`、`sync_fast_path`、`log_prune`、`launcher_exit`（exit_code、duration_ms、reason）；引擎 `engine_start`、`journal_recovered`／`journal_detected`、`resolve_finish`、`lock_acquired`、`fingerprint_verified`、`journal_created/deleted`、`prompt_asked/answered`（auto:true 表 -y）、`file_created/modified/appended/deleted`、`merge_conflict`、`declined`、`version_written`、`registry_query`、`prune_candidate/removed`、`engine_exit`（exit_code、message_id、duration_ms、summary）。通用：6-xx 訊息同句進 body + `message_id`；憑證永不記、URL 去 userinfo。
- 架構：log 與 ci 為輔助模組，核心只透過 `log_event()` 一個介面呼叫（不是 sidecar 容器）；sync 快路徑維持不起引擎（實測 grep 0.00 s vs 引擎容器 0.42 s，且不依賴 daemon）。
- 新訊息 6-38；新檔 config.toml、log/ 進目錄樹、schema 表、動詞×檔案矩陣；架構圖加 log 模組。

# v2.13 spec v3 待議 P4–P13 的取捨（2026-09-20 主對話依既定原則決定；使用者可否決）
- P4 bootstrap.sh：它就是第一次接入的啟動器。順序：驗 git repo／just → `mkdir -p .vendor_kit/log/bootstrap/` → 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install。install 失敗「不留半成品」的例外：**`.vendor_kit/log/` 保留**（使用者 L4：紀錄以備追責）；訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」。
- P5 第一次 install 也建 `.tmp.install.<id>.toml`（統一規則、無例外，v2.11 精神）；該日誌同時是「不留半成品」的清除清單，成功後刪。
- P6 uninstall：`config.toml` 比照初始檔保護模式——hash == baseline 副本 → 刪；被使用者改過 → 留下並列出（永不刪使用者改過的檔）。`log/` 一律保留（uninstall 自己也在寫），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪。
- P7 啟動器白名單加 `mkdir`、`date`（連同 `od`、`tr`）。啟動器 timestamp：試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級；引擎一律微秒。
- P8 引擎定位檔：`-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>`（進 `-e` 白名單與 §5），與 `TRACEPARENT` 並用。
- P9 事件註冊表：真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌一份啟動器事件白名單（case），release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（同 base）。薄殼由四檔改**五檔**：`entry.just`、`vendor.just`、`log.sh`、`ci/check.sh`（+ version.toml）；`log.sh` 從 base log.sh 移植（POSIX），由引擎重產、hash 記在 gen/.stamp。
- P10 config.toml 的 baseline 副本：`baseline/vendor_kit/config.toml`，metadata 記在 `baseline/.vendor_kit.toml`（與根 .dockerignore 同表）；config.toml **不寫 `written_by`／`schema` 以外的機器欄位**（使用者可編輯、含註解），`schema = 1` 保留。
- P11 6-38／6-24 文案先採草擬，待 codex／使用者審。
- P12「零寫入」= 不寫任何專案檔，**操作紀錄檔例外**（launcher_start／engine_start 已寫屬預期）。
- P13 根 `.dockerignore` 四行（加 `.vendor_kit/log/`），與 Q22 cache 同理。
- 低風險推論照子代理所寫（upgrade vendor_kit 對 config.toml 走狀態機＋6-22；grep 命中 0 → 預設不警告、重複／非正整數 → 預設＋警告；log prune 不刪本次檔與 .gitignore；啟動器一律自產 TRACEPARENT）。

# v2.14（2026-09-20 第十輪後；圖面落實與兩個小定案）
1. `log.sh` 與其他薄殼檔同規則：**帶自描述首行** `# vendor_kit-shell/<P> engine=<vX> sha256=…`；`gen/.stamp` 維持只記引擎 ref（§4.4 不變）。撤回第十版「gen/.stamp 記 log.sh hash」的畫法。
2. 引擎每個子命令（resolve 容器、apply 容器）啟動都先 append `engine_start`，結束寫 `engine_exit`；啟動器結束寫 `log_prune`、`launcher_exit`。圖上表現法統一：每頁 resolve 段與 apply 段各一格「append engine_start（失敗 → 1 + 6-38）」，頁尾一格「launcher_exit／log_prune」（可與結束橢圓相鄰、一格）。
3. 步驟格顏色規則統一：**藍 = 引擎（容器內）做的**、白 = 啟動器（主機）做的；同一動作各頁一致（install(2) 的建 justfile／append／刪日誌都是引擎 → 藍）。
4. sync resolve 加「偵測未完成交易？→ 是：印 6-33 結束 1」菱形（與 update 同）。
5. 工具 image `docker pull` 失敗（6-24／6-31）一律畫紅色出口（add(1)、B(1)、sync(2)、回退、undev）；bootstrap(1) 引擎 pull 失敗與 tag 形 inspect 失敗加紅出口。
6. uninstall(2)：不 rmdir `log/`，`.vendor_kit/` 保留（只剩 log/），訊息說明；config.toml 依 v2.13 P6。
7. E(c)(2) 加「config.toml：缺則建／有則三方合併（6-22 問）」一格與檔案框。
8. VENDOR_KIT_LOG_FILE 已定（v2.13 P8）→ spec §3.1／§5 白名單同步；契約④ 白名單加 od、tr、mkdir、date；快路徑前提加 log/。
9. 驗收矩陣頁（v1p3c）同步到 35 條。

# v2.15 第十三輪圖面規則（2026-09-20；依 codex 第十二版 4 組 245 條 + 名詞定案）
1. **名詞全面換新**（依 `decisions/review/00_terms.md`）：下游開發者／下游使用者／VK／專案／下游 repo／下游 image、版本鎖定行、基準版、進度檔、執行紀錄、CI 模式、需人處理／失敗、介面版／檔案版／最低介面版、模組名（resolve／fetch／initfile／shell／progress／schema／log／prune）；「使用者」一律「下游使用者」；「使用者的檔」→「專案檔」。各頁名詞表刪掉第 0 頁已有的詞，只留頁內特有詞。
2. **執行紀錄事件改用圖例約定，不逐格畫**：圖例加兩條——「每個終點橢圓隱含：啟動器結束前已寫 log_prune、launcher_exit」「每個『docker run 引擎』格隱含：容器開始寫 engine_start、結束寫 engine_exit」。因此**移除**第十二版加的 launcher_exit 扇出格與各段 engine_start 格（codex：扇出讓終點來源歧義）；只保留啟動器起點的「建執行紀錄、寫 launcher_start（失敗 → 1 + 6-38）」一格（它有真實分支）。事件名改為 codex L6 定案的 `launcher_started`／`engine_started`／`launcher_completed|failed`／`engine_completed|failed`。
3. **跨頁出入口一律白虛線橢圓**（入口「來自「X」頁」、出口「續「X」頁」），不用純文字。
4. **vk-resolve/1 只傳協定定義的東西**：pull／extract 清單、`apply|yes/no`、指紋；圖上不得寫「計畫／詢問清單／保護清單以 stdout 回啟動器」——apply 引擎自己重算；resolve 非 0 → 啟動器不讀 stdout、不跑 docker／apply（畫分支）。
5. **dev 建進度檔** `.tmp.dev.<id>.toml`（記覆寫行、symlink 目標、印記第一行）；本機覆寫在 `[tools].<repo>`。
6. **詢問格一律三出口**：是／否／無 tty 或 EOF（→ 1 + 6-4；Ctrl-C 中止不記拒絕）——可用共用小圖示或一條「無 tty」出口到橙終點。
7. **升引擎（E(c)）**：單段動詞，無指紋重驗；先偵測既有 `.tmp.upgrade.*` → 恢復；目標 ≠ 現版時先 inspect／pull **目標引擎**（失敗 → 1 + 6-24／6-31）再改第一行；E(c)(1′) 第一行變成非計畫值 → 6-2b；E(c)(2) config.toml 缺則問後建（`-y` 免問）、有則三方合併（衝突 → 2、留標記、metadata 更新）；成功文案分「換引擎 vX→vY」與「同引擎修復重產」。
8. **remove／uninstall**：版本鎖定行**最後刪**；`gen/tools.just` 與 cache 同次原子替換；使用者拒絕刪 append 行 → metadata 記錄保留（不刪 metadata 那條）。
9. **release(1)**：候選驗收在正式 release 之前（發布不可刪資產後不得再判定不合格）。
10. **契約④**：`gen/.stamp = 引擎 ref？` 只屬 sync 路徑；「查 registry」只在 add／update／upgrade 且未指定 @tag；inspect 後「本機已有 → 跳過 pull」；只有 extract kind 才 create／cp。
11. **install**：進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata `state=managed`）、存在不動；`.dockerignore` 是 symlink → 不寫只印指示（同 justfile）。
12. **架構圖**：主機側載入鏈（下游使用者 → 根 justfile → entry.just → vendor.just／tools.just → 工具 recipe）要有連線；`log.sh` 是獨立檔被 vendor.just source；config.toml 由 schema 模組讀、log 模組只記事件；進度檔兩種落點分別歸 progress 模組（.tmp）與 initfile 模組（metadata [progress]）。
13. 其餘 codex 逐條（`r12_codex/findings1–4.md`）全部處理；名詞表瘦身；顏色：驗證失敗紅、需人處理橙（例如 dist/init.toml 不合法 → 紅）。
14. `baseline/.gitkeep`：**保留**，定義為 VK 自產 tracked 檔（install 建、uninstall 刪、hash 固定為空檔）；spec §4.0 補明（codex 說規格未定義 → 補定義，不是刪）。
15. release：候選 image 先推 **候選 tag**（`vN-rc.<n>` 或 `candidate-<sha>`），驗收矩陣全過才 `imagetools create` 打正式 `vN`（不重 build，digest 不變）；Git tag 與 GHCR image tag 在圖上分開標。
16. update：末行固定印 6-15「套用：just vendor_kit upgrade」（含未完成交易出口）；`_TOKEN` 與 `_TOKEN_FILE` 同時設 → 1；registry 查詢失敗分類（認證／網路／回應／解析）各記該目標 1 並繼續彙總。
17. sync(2) verify：`--verify`／CI 模式／版本變動那次 → 先驗既有 cache，不符才重裝一次；重裝後再驗仍不符 → 失敗（紅），不無限重裝。
18. 逐檔判斷（upgrade B(2)）改成**依 state 分流的狀態機**：managed／appended／declined／unmanaged／deleted 各自路徑；二進位／symlink 改過 → 保留 warn，不進三方合併；append 命中分唯一／零／多處；新版新增但 dest 已有 → 不納管 + 6-11；declined_hash 相同不再問、N 變才問；解析失敗檔基準版不推。

# v2.16 第十四輪規則（2026-09-20；依第十三版 codex 4 組：R 已修 ≈232／未修 12／改壞 7，新發現 56）
1. **共通前置格**（每個可寫動詞頁的啟動器起點之後、resolve 之前）：「偵測既有進度檔？→ 是：先恢復（失敗 → 1 + 6-27）」（prune 例外：只列出）。唯讀動詞（sync／update）：偵測 → 6-33 → 1。
2. **resolve 結果分流一律三叉**：resolve 非 0 → 原碼傳出（不讀 stdout）；回 0 但 vk-resolve/1 文法不合 → 1 + 6-30；合法 → 繼續。四頁同型（add(1′)、sync(2)、B(1′)、E(a)）＋ prune(1)。
3. **事件名回歸 spec 註冊表**：圖例約定與圖上一律用 spec 名 `launcher_start／launcher_exit／engine_start／engine_exit`（L6 codex 提的 `*_started／*_completed` 改名**不採**，避免圖與註冊表不一致；改名若要做，先改 spec §4.10 註冊表再改圖——列待議）。
4. `--local` 判別依 v3.5 順序（`.tar` 結尾 → 檔案必須存在；否則含 `/` 且存在同名檔 → 6-37「檔案請改成以 .tar 結尾；image 請移走或改名同名檔」；否則 tag）：bootstrap(1) a8q／a8e／a8t、離線包(1) o3／o3n／o3cx、契約④ p3_fast。
5. bootstrap.sh 結束碼 = 失敗那一步原碼（install／add 回 2／3 照傳）；最低介面版 LABEL 檢查在任何 pull 之前（本機有 image 先 inspect LABEL；沒有才 pull 後檢查——spec 明寫「先於任何上網」，故：無本機 image 時允許 pull 後立即檢查、失敗 → 3 且不寫任何檔）。
6. install 自己執行時：先驗 git repo（主機側）再建執行紀錄（同 bootstrap）。
7. install(2) `.dockerignore`「已含這四行？」改逐行辨識，只加缺的行、只記實際新增的行。
8. 升引擎 E(c)(1)：先薄殼完整性檢查，再偵測 `.tmp.upgrade` 恢復。E(c)(2)：config.toml 拒絕建 → 不寫檔只記狀態；衝突 → 留標記、推基準版；解析失敗 → 留原檔、不推；config 建／替換／推副本各自失敗線。
9. remove(2) 拒絕刪 append 行：**仍完成移除**（版本鎖定行、cache、印記、基準版都刪），只在 metadata 之外另留一筆「孤兒 append 行」紀錄於 `baseline/.vendor_kit.toml`（同 .dockerignore append 記錄那張表）——不留 `baseline/<repo>/` 孤兒目錄。spec §1.2 remove 同步。
10. remove／uninstall／add(2) 的「任一步失敗」線：用一條共通失敗匯流（每個寫入格右側短線進匯流排）而不是只從三格拉。
11. sync：快路徑條件加「每個 `cache/<repo>/` 存在」；sync(2) 多 extract 迴圈「還有下一個 extract？」；tools.just 「在待辦？」菱形；斷網 sync 驗證相符後仍要「tools.just 缺 → 重生」；重裝成功後最後原子重生 tools.just。
12. upgrade B(1)：目標 == 現鎖定版且無待合併 → apply|no／0；本頁加共通前置格（規則 1）。E(a)：本機覆寫判斷在 pull 前；`s2h` 只比較正式 version.toml 引擎行前後。回退 D：apply 前置（flock、指紋、argv）、版本變動後全檔驗證＋失敗出口。
13. prune(1)：`q0l` 6-38 紅終點；resolve 三叉；prune(2)：每次刪除記成功／失敗，全部成功才刪進度檔；跨頁出口帶「有刪除失敗？」狀態。
14. 離線包(1′) install 失敗判斷在刪進度檔**之前**；離線包(3) 本機覆寫驗過就用本機 tag、不再 inspect 正式 ref；交易狀態機 `t1x` 拆兩橙終點、`t6x` 區分第一次 install 清半成品。
15. Renovate 頁：check.sh 步驟 ⓪ `git ls-files` 拒絕納管的 version.local.toml；④⑤ 原碼傳出（含 1）。
16. dev vendor_kit `v1lq` 文字：「image LABEL 的介面版 ≥ 薄殼自描述標頭的介面版，且 LABEL 檔案版 ≥ 現有 VK 檔的檔案版？」。dev／undev 進度檔記 image ID。
17. 名詞：remove／uninstall 的 `--dry-run` 不拉 image；6-33 條寫「sync／update 結束 1、help 仍 0」；B(1′) 名詞表「add 回 1」→「upgrade 回 1」；契約④ `s2b` 只在 add／upgrade（未指定 tag、非 CI）的 resolve 查 registry，update 是單段另畫；架構圖 pull timeout 歸啟動器；目錄樹 `p2_ver_n` 改「頂層 vendor_kit 行在 [tools] 前」；驗收詳表 18 補 URL 去 userinfo、19 補 .dockerignore 改一行的驗收。
18. 名詞表瘦身第二輪（G4／共通未修）：每頁名詞表 ≤ 8 條、只留本頁流程用到且第 0 頁沒有的詞；沿革便條全刪。
19.（Claude 三階段補充）啟動器起點「建執行紀錄」「寫 launcher_start」拆兩格（各頁）；install 就地執行也要 grep 引擎 ref → inspect → pull 段；add(1) `--local` 讀到的 digest 要有線進 resolve、離線不查 registry；flock 逾時 6-26 出口每個 apply 頁都要；契約④ `s4x` 終點顏色改依結束碼分、`p3_self` 補 E(c) 新接手路徑；契約⑤ `c_d` 拆三格、名詞對齊候選流程；架構圖便條不壓契約列、`w_cfg_l` 標籤位置、啟動器 grep version.toml／進度檔的線、掛載路徑一致（`.tmp.dist.<id>/ → /dist`、下有 `<repo>/`）；bootstrap(1′) 十字交叉、install 回 3 出口、清半成品歸屬（引擎寫入失敗自清；引擎異常結束由 bootstrap.sh 補清）；6-24 一律紅；其餘見 `review_v2r13_claude.md`。

# v2.17 第十五輪（最後一輪修圖；codex 執行、Claude 檢查；剩餘寫頁面清單）
1. 共通前置「偵測既有進度檔→先恢復」是**引擎**做的：放在 `docker run 引擎 <resolve|單段>` 之後、flock 之後、任何讀計畫／寫入之前（藍格）；啟動器不做恢復。sync／update 的 6-33 偵測同樣在引擎 resolve 內。
2. 契約④：快路徑條件補 cache 存在；resolve 三叉補文法出口；apply 結束碼分色 1＝失敗（紅）、2／3＝需人處理（橙）；update 單段線不繞；沿革便條刪。
3. 頁內失敗匯流終點文字不得宣稱「版本鎖定行不動」若有路徑在寫完鎖定行後才失敗（add(2) 刪進度檔失敗 → 另一終點「已寫入完成；進度檔留待下次刪」）。
4. bootstrap(2) 中止終點分色：6-24／6-30／寫入失敗 → 紅；原碼傳出（2／3）→ 橙。
5. install：`grep 命中 ≠ 1` 出口；`install <repo>` 誤用 6-17 出口；flock 逾時標籤不壓箭頭。
6. sync(1)：本機覆寫判斷在 inspect／pull 之前（覆寫中且本機無 image → 失敗，不 pull）；sync(1′)：`apply|no?` 判斷在三叉之後（非 0／文法不合先出）。
7. sync(2)：docker 段補 mount 記錄處理（dev 覆寫工具 `-v <dir>/dist:/dist/<repo>:ro`）；指紋重驗畫法統一為菱形「相同？」；sync(2′) 取件／重裝格失敗線進匯流。
8. Renovate 頁：⓪ 納管 → 1 停 加終點。B(1)：目標==現版判斷順序、長折線不貼綠終點。
9. 排版：所有標籤不壓線／不擠短線（ce2ll、ce3、ne5x、te7、me4vn、run_cli/ret_cli 等）；建檔格後續線從底或右側出。
10. lint 22 條（term-count v1p2b／v1p3、term-dup-page0 ×3、write-fail-edge prune(2)／離線包(2′)(3′)、end-color-text o3tx、term-diff ×2）全清。
11. 其餘 `review_v2r14_claude.md` 必修＋選修逐條處理；改不了的（幾何限制、頁序固有）不改，寫進該頁「待處理問題」便條（黃底、右下角、條列 id＋一句）。
