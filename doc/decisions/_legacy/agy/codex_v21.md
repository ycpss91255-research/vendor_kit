OpenAI Codex v0.153.4
--------
workdir: /home/cyc/Desktop/vendor-kit_ws/src
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a0b546-f8be-7a83-b516-f7602aece01a
--------
user
你是設計審查員。下面 proposal_v2.md 的「v2.1 補充」節有七項 [裁] 裁定，是為了解決雙軌審查發現的規格矛盾而定的，尚未經使用者同意。請逐項獨立判斷：同意／反對／有條件同意，給理由與證據（工具行為、前例、已定案不變量的一致性），反對就提替代方案。特別注意使用者已定的不變量：「vendor_kit 對使用者的檔：可以建（明說建了什麼）、要改先問（-y 免問）、永不刪、永不覆蓋」與「never fail silently」「主機只需 docker+git+just」「指令極少」。
七項：
A. 不變量精確化：「自動化只碰不進 git 的東西」→「自動化不碰使用者的檔」；vendor_kit 自有 tracked 薄殼（.vendor_kit/entry.just、vendor.just、ci/check.sh、.gitignore）由 version.toml 第一行推導，引擎升級時 sync 可重寫（本機），CI frozen 不符→1。替代：(2) 薄殼只能由明確動作 `upgrade vendor_kit` 重寫，sync 只報 1。
   frozen 定義：不寫 tracked、警告變失敗、不查最新版、仍拉鎖定版、可寫 cache/gen；CI 有 version.local.toml 覆寫→1。
B. 覆寫兩種分開：引擎 tag 覆寫（啟動器改用該 image）與工具 path 覆寫（cache symlink，跳過 materialize/verify 仍檢查 metadata/baseline）；dev 中的工具 upgrade/remove→1 先 undev；undev vendor_kit 後下次 just 重寫薄殼並統一提示。
C. 動詞兩段執行：引擎 `resolve`（讀宣告、查 registry、算要拉什麼要問什麼、不寫、stdout 回啟動器）→ 啟動器 docker pull/create/cp → 引擎 `apply`（flock 在引擎、詢問、寫 cache/初始檔/baseline/gen、version.toml 最後寫、失敗丟暫存 1）。理由：容器內叫不到主機 docker。請評估：兩次 docker run 的成本、resolve 與 apply 之間狀態改變（TOCTOU）、stdout 協定的脆弱性、替代方案（引擎掛 docker socket＝拒絕；主機用 `docker pull tag` + `docker image inspect` 取 digest 免 registry API？但列 tag 仍需 API）。
D. upgrade 順序：(0) 衝突中檔案仍含標記→2；(1) 先補待合併；(2) 再查最新（兩者都做）；自身升級兩個觸發點（upgrade 當次停下；別人 pull 後下次 just 停下）。
E. 新增：init.toml 兩工具 dest 撞名→add 報錯；dist/files symlink [待]；`--porcelain` 拿掉；update --exit-code 有新版回 2；tools.just 每個 <ns>.just 一行 mod；install 冪等（已含 import 行不再加）；add/remove/uninstall 都有 --dry-run；uninstall 逐工具 remove 回 1 即中止；Renovate 補合併在 PR 分支。
最後給一張表：項目｜裁定（同意／反對／有條件）｜一句理由｜條件或替代。60 行內。

---

## 附件：proposal_v2.md 全文

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

## 附件：grilling.md 全文

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

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
我會逐項核對已定案紀錄，並查證 Docker、Git 與 just 的相關行為；特別檢查自動重寫、兩階段執行及失敗後的狀態保證。

web search: 
web search: site.docs.docker.com reference cli docker image pull digest platform ...
web search: 
web search: https://git-scm.com/docs/git-merge-file
codex
**不建議整批接受 v2.1；其中「失敗丟暫存即可復原」與「所有 dest 撞名一律拒絕」應退回修改。** `[裁]` 尚未獲同意，不能自行凌駕 `[定]`。
你列出 A–E 五組；以下將 C 拆成編排／提交、E 拆成路徑／其餘，共七項獨立審查。依據附件與官方文件；本機讀取受環境限制，未完成實測。

**① A：有條件同意。**
附件 grilling Q9 已明訂「sync 重寫薄殼＋gen、退出 1」，因此允許自有 tracked 薄殼更新有直接前例；但這是對「sync 不寫 tracked」的**明列例外**，不能只靠改稱「自有」便授權任意覆蓋。
條件：限定四個路徑、內容可重建，且重寫前確認現有內容仍等於上次產物；若被改過，回 1、保留內容並列差異。`install` 修復也須遵守，不能成為覆蓋客製內容的後門。
若不接受此例外，採替代 (2)：sync 只報 1，提示既有 `upgrade vendor_kit`；它不增加動詞，但明確動作仍不等於同意丟棄客製內容。
frozen 定義基本同意，但應是「只准寫指定 cache/gen」，不是依當下 Git 是否追蹤判斷；警告須列舉哪些升為失敗。CI 拒絕任何有效 local 覆寫，須在使用覆寫引擎前執行。`.gitignore` 的 append 例外有 Q6 定案支持。

**② B：有條件同意。**
兩種覆寫確實不同；dev 工具禁止 upgrade/remove 與已有 remove 契約一致，metadata/baseline 檢查也應保留，不能把開發模式當成完成接入。
但 **tag 不是內容身分**：同一 tag 重建後，stamp 不變便漏掉引擎更新。保留使用者輸入 tag，另以解析後的 image ID 記錄／固定本次引擎；缺 image 必須失敗，不能讓 `docker run` 預設自動拉取。[Docker run](https://docs.docker.com/reference/cli/docker/container/run)
工具 path 可能在 repo 外，容器看不到主機 symlink 的目標；啟動器須明確掛載，並驗證 dist 存在。`undev` materialize 失敗應回 1、保留可恢復狀態，不能沿用正文「永遠 0」；自身復原依 A 的保護規則。
不帶 repo 的 upgrade 遇到 dev 工具，須先完整預檢再拒絕，避免改完其他工具才報 1。

**③ C／編排：有條件同意，但 dry-run 流程必須改。**
兩次 `docker run` 符合主機 docker、引擎處理邏輯的分工；成本是兩次容器建立／啟動，實際延遲須量測，不能直接斷言可忽略。每次 just 都 sync，應提供「無變更只跑一次檢查」快路徑。
**尚未取回新版 dist，就不能準確知道會問哪些檔。** registry tag/digest 不提供 init.toml 或範本內容。因此 dry-run 必須容許拉取及暫存展開，再由引擎產生唯讀預覽；不能一律 resolve 完就回 0。
stdout 協定可行，但須版本化、限制欄位與字元、診斷只走 stderr、完整成功後才採用；不得 `eval`。主機不用新增 jq/Python，複雜資料保留給引擎解析。只有互動確認才配置 TTY；CI／`-y` 不加 `-t`。[Docker run](https://docs.docker.com/reference/cli/docker/container/run)
`docker pull tag`＋`image inspect --format` 可作為指定 tag 的 digest 取得候選，沿用主機認證；但須驗證選到正確 repo 的 **index digest**，不能拿 image ID 或任取第一筆 RepoDigest。列版本仍需 registry API，且 `update`「只查」不能偷偷改成 pull。[pull](https://docs.docker.com/reference/cli/docker/image/pull/)、[inspect](https://docs.docker.com/reference/cli/docker/image/inspect/)、[Registry API](https://docs.docker.com/reference/api/registry/latest/)
另須補上私有 registry 查詢的認證途徑：引擎自行查 API，不會自然取得主機 credential helper 能力；否則違反 Q7「主機 docker 拉得到就能用」。不必因此接受掛 docker socket。

**④ C／鎖與失敗保證：反對現文。**
apply 才拿 flock，無法保證 resolve 所讀版本、baseline、使用者檔案仍相同；flock 也擋不住編輯器。更關鍵的是：已寫入使用者檔或 baseline 後，**丟棄暫存並不會復原那些寫入**；version.toml 最後寫只保護一個檔案。
替代：resolve 傳入輸入指紋與鎖定 digest；apply 拿鎖後重新驗證，有變就重新規劃／回 1，不能沿用舊決策；詢問後、提交前也核對相關檔案。所有合併先在暫存完成，再以逐檔原子替換及可恢復日誌提交。
多檔不是單一原子交易；中途失敗須明列已完成／未完成項目，下次操作先恢復，不能宣稱「1 不留半成品」。衝突回 2 是允許保留結果的獨立狀態；自身升級成功後回 1 要求重跑，也須與一般失敗分開描述。

**⑤ D：有條件同意。**
先處理既有衝突、再補 baseline、再查新版本，能避免拿錯祖先合併；自身升級兩個觸發點均有 Q9 支持。但補合併若產生衝突，必須立即回 2，不能接著套下一版。
只找 `<<<<<<<` 不充分：可能留下其他標記，也可能是原有文字。應辨識本次生成的標記，檔案失蹤亦不能直接視為已解；標記消失只代表可繼續，不能保證語意正確。Git 的回傳值是衝突數／錯誤，須映射為契約的 0/1/2。[git merge-file](https://git-scm.com/docs/git-merge-file)
「兩者都做」須限定正常本機 upgrade；CI frozen 的 dry-run **只檢查鎖定版**，不得再查最新，需補合併回 1、既有衝突回 2，不能一律 0。
Renovate PR 補合併須固定 PR 鎖定版本，可沿用 `-t`；否則補 B 時順便追到 C，便偏離該 PR。`-t` 降版可接受，但預覽須明說。

**⑥ E／dest 與 symlink：反對一律撞名拒絕；同意暫禁 symlink。**
兩工具 append 同一個 `.gitignore` 正是 Q6 已允許的使用情境；全拒會使第二個工具無法接入。
替代：copy/copy、copy/append 同目的地拒絕；append/append 允許可獨立識別、互不重疊的貢獻，重疊或歸屬不明先拒絕。add 與 upgrade 都要檢查，且在任何寫入前完成。
目的地須正規化並拒絕越出 repo、指向 vendor_kit 內部狀態及透過父目錄 symlink 越界。第一版禁 dist symlink 可降低複雜度，但不只供應端 lint：消費端也須驗證，不能假設每個 image 都跑過 CI。

**⑦ E／其餘：有條件同意。**
拿掉未定案 porcelain、update 的 2 表示有新版、每個 ns 一行 mod、install 不重複 import、baseline 為歷史、Renovate 在 PR 分支補合併，均合理；2 必須按動詞解讀，多模組仍須通過已定的 just 1.33 fixture。[just modules](https://just.systems/man/en/modules.html)
dry-run 應覆蓋所有刪改與詢問，套用 C 的修正版；uninstall 先預檢全部工具，任一失敗即中止並列出已完成部分，不能暗示整體原子。
**uninstall 不可直接遞迴刪整個 `.vendor_kit/`**：使用者可能放入其他檔案；只能移除確認屬於工具且未客製的產物，遇未知內容保留並回報。問後刪精確 import／append 行有 grilling 明確例外支持，但不是刪整個使用者檔的授權。

| 項目 | 裁定 | 一句理由 | 條件或替代 |
|---|---|---|---|
| A 自有薄殼／frozen | 有條件 | Q9 支持重寫，但不能藉所有權宣告覆蓋客製 | 明列例外、比對舊產物；否則明確 upgrade |
| B 兩種覆寫 | 有條件 | 分工合理，tag 與主機 path 尚不足以確保正確執行 | 固定 image ID、掛載 path、undev 失敗回 1 |
| C 編排 | 有條件 | 兩段可行，未取 dist 不能做完整預覽 | 取回後預覽、嚴格協定、解決私有認證 |
| C 提交／鎖 | 反對 | 晚拿鎖與丟暫存不提供多檔復原 | 指紋重驗、暫存合併、可恢復提交 |
| D 升級順序 | 有條件 | 順序合理，但衝突與 frozen 必須截斷後續 | 衝突即停、CI 不查最新、PR 固定版本 |
| E 路徑規則 | 反對 | 全拒撞名破壞已允許的多工具 append | 按 mode／貢獻判斷，消費端驗證路徑 |
| E 其餘補充 | 有條件 | 多數一致，修復與卸載仍可能破壞使用者內容 | 保護客製／未知檔，明列部分完成狀態 |
tokens used
27,683
**不建議整批接受 v2.1；其中「失敗丟暫存即可復原」與「所有 dest 撞名一律拒絕」應退回修改。** `[裁]` 尚未獲同意，不能自行凌駕 `[定]`。
你列出 A–E 五組；以下將 C 拆成編排／提交、E 拆成路徑／其餘，共七項獨立審查。依據附件與官方文件；本機讀取受環境限制，未完成實測。

**① A：有條件同意。**
附件 grilling Q9 已明訂「sync 重寫薄殼＋gen、退出 1」，因此允許自有 tracked 薄殼更新有直接前例；但這是對「sync 不寫 tracked」的**明列例外**，不能只靠改稱「自有」便授權任意覆蓋。
條件：限定四個路徑、內容可重建，且重寫前確認現有內容仍等於上次產物；若被改過，回 1、保留內容並列差異。`install` 修復也須遵守，不能成為覆蓋客製內容的後門。
若不接受此例外，採替代 (2)：sync 只報 1，提示既有 `upgrade vendor_kit`；它不增加動詞，但明確動作仍不等於同意丟棄客製內容。
frozen 定義基本同意，但應是「只准寫指定 cache/gen」，不是依當下 Git 是否追蹤判斷；警告須列舉哪些升為失敗。CI 拒絕任何有效 local 覆寫，須在使用覆寫引擎前執行。`.gitignore` 的 append 例外有 Q6 定案支持。

**② B：有條件同意。**
兩種覆寫確實不同；dev 工具禁止 upgrade/remove 與已有 remove 契約一致，metadata/baseline 檢查也應保留，不能把開發模式當成完成接入。
但 **tag 不是內容身分**：同一 tag 重建後，stamp 不變便漏掉引擎更新。保留使用者輸入 tag，另以解析後的 image ID 記錄／固定本次引擎；缺 image 必須失敗，不能讓 `docker run` 預設自動拉取。[Docker run](https://docs.docker.com/reference/cli/docker/container/run)
工具 path 可能在 repo 外，容器看不到主機 symlink 的目標；啟動器須明確掛載，並驗證 dist 存在。`undev` materialize 失敗應回 1、保留可恢復狀態，不能沿用正文「永遠 0」；自身復原依 A 的保護規則。
不帶 repo 的 upgrade 遇到 dev 工具，須先完整預檢再拒絕，避免改完其他工具才報 1。

**③ C／編排：有條件同意，但 dry-run 流程必須改。**
兩次 `docker run` 符合主機 docker、引擎處理邏輯的分工；成本是兩次容器建立／啟動，實際延遲須量測，不能直接斷言可忽略。每次 just 都 sync，應提供「無變更只跑一次檢查」快路徑。
**尚未取回新版 dist，就不能準確知道會問哪些檔。** registry tag/digest 不提供 init.toml 或範本內容。因此 dry-run 必須容許拉取及暫存展開，再由引擎產生唯讀預覽；不能一律 resolve 完就回 0。
stdout 協定可行，但須版本化、限制欄位與字元、診斷只走 stderr、完整成功後才採用；不得 `eval`。主機不用新增 jq/Python，複雜資料保留給引擎解析。只有互動確認才配置 TTY；CI／`-y` 不加 `-t`。[Docker run](https://docs.docker.com/reference/cli/docker/container/run)
`docker pull tag`＋`image inspect --format` 可作為指定 tag 的 digest 取得候選，沿用主機認證；但須驗證選到正確 repo 的 **index digest**，不能拿 image ID 或任取第一筆 RepoDigest。列版本仍需 registry API，且 `update`「只查」不能偷偷改成 pull。[pull](https://docs.docker.com/reference/cli/docker/image/pull/)、[inspect](https://docs.docker.com/reference/cli/docker/image/inspect/)、[Registry API](https://docs.docker.com/reference/api/registry/latest/)
另須補上私有 registry 查詢的認證途徑：引擎自行查 API，不會自然取得主機 credential helper 能力；否則違反 Q7「主機 docker 拉得到就能用」。不必因此接受掛 docker socket。

**④ C／鎖與失敗保證：反對現文。**
apply 才拿 flock，無法保證 resolve 所讀版本、baseline、使用者檔案仍相同；flock 也擋不住編輯器。更關鍵的是：已寫入使用者檔或 baseline 後，**丟棄暫存並不會復原那些寫入**；version.toml 最後寫只保護一個檔案。
替代：resolve 傳入輸入指紋與鎖定 digest；apply 拿鎖後重新驗證，有變就重新規劃／回 1，不能沿用舊決策；詢問後、提交前也核對相關檔案。所有合併先在暫存完成，再以逐檔原子替換及可恢復日誌提交。
多檔不是單一原子交易；中途失敗須明列已完成／未完成項目，下次操作先恢復，不能宣稱「1 不留半成品」。衝突回 2 是允許保留結果的獨立狀態；自身升級成功後回 1 要求重跑，也須與一般失敗分開描述。

**⑤ D：有條件同意。**
先處理既有衝突、再補 baseline、再查新版本，能避免拿錯祖先合併；自身升級兩個觸發點均有 Q9 支持。但補合併若產生衝突，必須立即回 2，不能接著套下一版。
只找 `<<<<<<<` 不充分：可能留下其他標記，也可能是原有文字。應辨識本次生成的標記，檔案失蹤亦不能直接視為已解；標記消失只代表可繼續，不能保證語意正確。Git 的回傳值是衝突數／錯誤，須映射為契約的 0/1/2。[git merge-file](https://git-scm.com/docs/git-merge-file)
「兩者都做」須限定正常本機 upgrade；CI frozen 的 dry-run **只檢查鎖定版**，不得再查最新，需補合併回 1、既有衝突回 2，不能一律 0。
Renovate PR 補合併須固定 PR 鎖定版本，可沿用 `-t`；否則補 B 時順便追到 C，便偏離該 PR。`-t` 降版可接受，但預覽須明說。

**⑥ E／dest 與 symlink：反對一律撞名拒絕；同意暫禁 symlink。**
兩工具 append 同一個 `.gitignore` 正是 Q6 已允許的使用情境；全拒會使第二個工具無法接入。
替代：copy/copy、copy/append 同目的地拒絕；append/append 允許可獨立識別、互不重疊的貢獻，重疊或歸屬不明先拒絕。add 與 upgrade 都要檢查，且在任何寫入前完成。
目的地須正規化並拒絕越出 repo、指向 vendor_kit 內部狀態及透過父目錄 symlink 越界。第一版禁 dist symlink 可降低複雜度，但不只供應端 lint：消費端也須驗證，不能假設每個 image 都跑過 CI。

**⑦ E／其餘：有條件同意。**
拿掉未定案 porcelain、update 的 2 表示有新版、每個 ns 一行 mod、install 不重複 import、baseline 為歷史、Renovate 在 PR 分支補合併，均合理；2 必須按動詞解讀，多模組仍須通過已定的 just 1.33 fixture。[just modules](https://just.systems/man/en/modules.html)
dry-run 應覆蓋所有刪改與詢問，套用 C 的修正版；uninstall 先預檢全部工具，任一失敗即中止並列出已完成部分，不能暗示整體原子。
**uninstall 不可直接遞迴刪整個 `.vendor_kit/`**：使用者可能放入其他檔案；只能移除確認屬於工具且未客製的產物，遇未知內容保留並回報。問後刪精確 import／append 行有 grilling 明確例外支持，但不是刪整個使用者檔的授權。

| 項目 | 裁定 | 一句理由 | 條件或替代 |
|---|---|---|---|
| A 自有薄殼／frozen | 有條件 | Q9 支持重寫，但不能藉所有權宣告覆蓋客製 | 明列例外、比對舊產物；否則明確 upgrade |
| B 兩種覆寫 | 有條件 | 分工合理，tag 與主機 path 尚不足以確保正確執行 | 固定 image ID、掛載 path、undev 失敗回 1 |
| C 編排 | 有條件 | 兩段可行，未取 dist 不能做完整預覽 | 取回後預覽、嚴格協定、解決私有認證 |
| C 提交／鎖 | 反對 | 晚拿鎖與丟暫存不提供多檔復原 | 指紋重驗、暫存合併、可恢復提交 |
| D 升級順序 | 有條件 | 順序合理，但衝突與 frozen 必須截斷後續 | 衝突即停、CI 不查最新、PR 固定版本 |
| E 路徑規則 | 反對 | 全拒撞名破壞已允許的多工具 append | 按 mode／貢獻判斷，消費端驗證路徑 |
| E 其餘補充 | 有條件 | 多數一致，修復與卸載仍可能破壞使用者內容 | 保護客製／未知檔，明列部分完成狀態 |
