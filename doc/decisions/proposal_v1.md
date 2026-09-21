# vendor_kit 對外契約與架構 —— 提案 v1（2026-09-18，全部為「建議、待使用者拍板」；已定案：Q1 自寫 + docker + git merge-file）

占位符：`<repo>` = 工具 repo 名（例 base）。角色：工具 repo 開發者（供應側）／使用者（下游專案，每天打 just）／vendor_kit 開發者。契約只對前兩者承諾。

## 0. 目的
工具 repo 把 dist/ 打包成 GHCR image；下游專案靠 `bootstrap.sh` + `just vendor_kit add/upgrade/dev` 拿到工具、跟上新版、在本機開發工具本身；其餘自動。

## 1. 使用者介面（常用 3 + 進階 5 + 一支腳本）
| 動詞 | 參數 | 反向 | 做什麼 | 結束狀態 | 組 |
|---|---|---|---|---|---|
| `bootstrap.sh` | `--tool <repo>`（可重複）`-t/--tag <tag>` `-s/--source <image>` `-y/--yes` `--repair` `-h/--help` | `uninstall` | 第一次接入：詢問（或用參數）→ 寫 `.version`、根 justfile 一行 `import '.vendor_kit/entry.just'`、`.vendor_kit/` 薄殼 → 對每個 `--tool` 跑 add。偵測到已有 `.version` 且無 `--repair` → 1 並提示 `just vendor_kit add`。`--repair`：用 `.version` 鎖的引擎重寫薄殼，不動 `.version`/初始檔/baseline；拉不到鎖定引擎就失敗，不得用腳本內建引擎。非互動缺參數就失敗、EOF 不算同意。不自刪。 | 0；1 不留半成品 | 一次性 |
| `add <repo>` | `-t/--tag`（預設最新）`-s/--source <image>`（不符 `ghcr.io/<org>/<repo>-dist` 慣例時）`-n/--dry-run` | `remove` | 寫 `.version`（tag@digest）→ install `.<repo>/` → 複製初始檔（已存在只 warn）→ 建 `baseline/<repo>/` + metadata。對已接入工具：只續作「可辨識的未完成接入」（metadata 無完成標記），不補使用者刻意刪的檔；指定版本與鎖定不同 → 1 提示用 upgrade | 0（含 warn）；1 不動 `.version` | 常用 |
| `upgrade [<repo>]` | `-t/--tag`（限單一 repo；比現版舊時警告仍執行）`-n/--dry-run`（= 舊 diff） | `git revert` 整組 commit | 先補「`.version` 已到 B、baseline 仍 A」的待合併（Renovate merge 後）→ 查 GHCR 最新（或 --tag）→ 改 `.version` → install → 三方合併 → 推 baseline + metadata → 摘要。不帶 repo = 全部含 vendor_kit 自身：自身變了先換薄殼、停下要求重跑（不自動 re-exec）。無 baseline → 1 提示先 add | 0；1 不動 `.version`；2 有衝突（不推 baseline、留標記與檔名清單） | 常用 |
| `dev <repo>` | `-p/--path <dir>`（必填） | `undev` | `.version.local`（不進 git）記 `<repo> = "path:<dir>"`；`.<repo>/` 改指向該目錄；印記第一行 `path:<dir>`；upgrade 的合併來源不受影響；CI 下拒絕；第一版不支援 vendor_kit 自身 | 0；1（缺 dist/ 或 init.toml） | 常用 |
| `remove <repo>` | `-n/--dry-run` | `add` | 刪 `.version` 行、`.<repo>/`、`baseline/<repo>/`、gen 內該工具 recipe；**保留初始檔並印清單**（第一版不開 `--purge`，用 git 刪）。有 dev 覆寫 → 1 提示先 undev。未接 = 0 + 提示 | 0／1 | 進階 |
| `undev <repo>` | — | `dev` | 移除 `.version.local` 該行 → 重裝 `.version` 版。未啟用 = 0 + 提示 | 0／1 | 進階 |
| `update [<repo>]` | `--exit-code` | （upgrade 的前一步，不算反向） | 只查 GHCR，不動任何專案檔；最後一行固定「套用：just vendor_kit upgrade」；拒絕未知參數 | 0；1 查詢失敗；`--exit-code` 有新版 2 | 進階 |
| `ensure [<repo>]` | —（CI=1 自動 frozen） | — | 每次 just 自動前置：印記 ≠ `.version` → install；verify 失敗 → 重裝並 warn；**只寫 gitignore 路徑**（`.<repo>/`、`gen/`）；「從未完成接入」→ 1 提示 add；「baseline 落後 `.version`」→ 本機 warn 提示 upgrade、CI 下 1 | 0／1 | 進階 |
| `uninstall` | `-y/--yes` `-n/--dry-run` | `bootstrap.sh` | 逐工具 remove → 刪 `.vendor_kit/`、`.version`、`.version.local`；根 justfile 那行只在與 bootstrap 寫入完全相同時才刪，否則印指示 | 0／1 | 進階 |
| `help` / `h` | — | — | 命名空間層說明（just 做不到 `just vendor_kit --help`）；各動詞 `--help` 由引擎印 | 0 | — |

不開：`init`（快取壞→ensure；未完成接入→add；薄殼壞→`bootstrap.sh --repair`）、`sync`（=upgrade 補待合併）、`diff`（=`upgrade --dry-run`）、`accept`（解完衝突重跑 upgrade）、`rollback`（git revert）、`clean`（`git clean -fdX`）、`install`/`verify`（引擎內部）。
動詞語意跟 base（`just base update/upgrade`）：update 只查、upgrade 套用；不加 check/diff/outdated/link/unlink 別名。
所有動詞 recipe 一行 `verb *args` 轉發（`set positional-arguments`，引擎解析），放 tracked 的 `vendor.just`，clone 後命名空間即完整；`[group('常用')]`/`[group('進階')]` 分段。

## 2. 專案裡的檔（契約③）
```
專案/
├── justfile                 # 使用者的；bootstrap 只加一行 import '.vendor_kit/entry.just'
├── .version                 # 唯一來源（進 git）
├── .version.local           # dev 覆寫（不進 git；由 dev 寫 .git/info/exclude）
├── .vendor_kit/             # 啟動器
│   ├── entry.just           # 進 git：mod vendor_kit 'vendor.just' + import? 'gen/tools.just'
│   ├── vendor.just          # 進 git：動詞 recipe（一行轉發）+ ensure 前置
│   ├── ci/check.sh          # 進 git：下游 CI 呼叫的契約檢查（隨 upgrade 更新）
│   ├── baseline/<repo>/     # 進 git：上次合併的範本副本
│   ├── baseline/<repo>/.vendor_kit.toml   # 進 git：metadata（來源 image@digest、最後合併版本、接入完成標記；兼作空目錄佔位）
│   └── gen/                 # 不進 git：引擎產生
│       ├── tools.just       # mod <repo> '../../.<repo>/just/<repo>.just' 一行一工具
│       └── .stamp           # 薄殼印記（引擎 image@digest）
└── .<repo>/                 # 不進 git、使用者不可改；install 從 image /dist 展開
    ├── .stamp               # 第一行 image@digest（或 path:<dir>），之後每檔 sha256
    ├── files/ …             # 工具檔案
    ├── init.toml
    └── just/<repo>.just     # 工具自己的 just 模組（just <repo> …、just docker …）
```
`.version` 格式（建議）：
```toml
vendor_kit = "ghcr.io/ycpss91255-research/vendor_kit:v3@sha256:…"   # 第一行固定；啟動器 grep 讀
[tools]
base = "ghcr.io/ycpss91255-docker/base-dist:v1.4.0@sha256:…"
```

## 3. 工具 repo 要交的（契約④）
`dist/files/`（全部出貨，不含 symlink）、`dist/init.toml`（`[[file]] src/dest`，dest 相對專案根）、`dist/just/<repo>.just`（工具自己的 recipe；第一行可 `just vendor_kit ensure`）、`Dockerfile.dist`（`FROM scratch` + `COPY dist/ /dist/`）。image `ghcr.io/<org>/<repo>-dist:<tag>`，**單架構 linux/amd64 純資料**（啟動器固定 `--platform linux/amd64` 拉；一份內容一個 digest）。引擎 image `vendor_kit:vN` 多架構 amd64+arm64。工具 repo 的 CI 跑 vendor_kit 出貨的 `check.sh`（dist 佈局、init.toml 合法、image 可展開）。

## 4. 啟動器 ↔ 引擎（契約②）
啟動器（POSIX sh，只用 docker pull/create/cp/run/rm + grep/sed）：
1. grep `.version` 第一行 → 引擎 ref；`gen/.stamp` ≠ 引擎 ref → 用新引擎跑 `bootstrap --repair-shell`（重寫 gen/ 與薄殼）→ 印「已更新 vendor_kit，請重跑」→ exit 1。
2. 對每個要處理的工具：`docker create --platform linux/amd64 <image@digest> /x` → `docker cp c:/dist/. <tmp>/` → `docker rm`。
3. `docker run --rm -u $(id -u):$(id -g) -v $PWD:/repo -v <tmp>:/dist/<repo>:ro [-v <devdir>:/dist/<repo>:ro] <引擎> <子命令> --repo <repo> …`（rootless docker 偵測到就不加 -u）。
引擎子命令：`install | init | verify | merge | add | remove | upgrade | update | dev | undev | uninstall | bootstrap`，結束狀態 0/1/2；stdout 人類可讀、`--porcelain` 機器可讀（留給 CI）。專案目錄 flock（60 秒、`VENDOR_KIT_NO_LOCK=1`）。

## 5. 流程
### 5a bootstrap（第一次）
使用者下載 release 的 bootstrap.sh → 執行 → 詢問工具與版本（或 --tool/--tag/--yes）→ 拉引擎 image → 引擎 `bootstrap` 寫 `.version`（先只有 vendor_kit 行）、根 justfile 一行、`.vendor_kit/` 薄殼 → 對每個工具跑 add（見 5b）→ 印摘要與「git add .version justfile .vendor_kit/ 與初始檔」。失敗：什麼都不留（暫存目錄原子替換）。
### 5b add
flock → 查 GHCR tag（或 --tag）與 digest → 寫 `.version`（tag@digest）→ install（拉 image、展開到 `.<repo>/`、寫印記）→ init（init.toml 逐檔複製，已存在 warn）→ 寫 `baseline/<repo>/` + metadata（完成標記）→ 重生 gen/tools.just → 摘要。已接入且完成標記在 → 「已接入，無變更」0。
### 5c ensure（每次 just）
讀 `.version`（+ `.version.local` 覆寫）→ 對每個工具：無 `.<repo>/` 或印記第一行 ≠ → install；verify（sha256）失敗 → 重裝 + warn；metadata 無完成標記 → 1「請 just vendor_kit add <repo>」；metadata 最後合併版本 ≠ `.version` → warn「請 just vendor_kit upgrade <repo>」（CI=1 → 1）→ 重生 gen/。ensure 範圍：預設全部工具（便宜：只比對印記）。
### 5d upgrade（含 Renovate 路徑）
路徑 A（Renovate）：機器人 PR 改 `.version` 一行（regex manager、docker datasource、currentValue+currentDigest）→ CI 跑 `check.sh`（ensure frozen → 1「baseline 落後」）→ **PR 作者在本機 `just vendor_kit upgrade <repo>` 補合併並 commit** → CI 綠 → merge。
路徑 B（手動）：`just vendor_kit upgrade <repo>` → 查最新 → 改 `.version` → install → 三方合併 → 推 baseline → 摘要。
三方合併（每個 init.toml 檔）：baseline 有／現況有／新版有 → `git merge-file --diff3`（衝突留 `<<<<<<<`，回 2）；新版新增 → 使用者沒有就建、有就以空 base 合併並標衝突；新版刪除 → 使用者沒改就刪、改過就保留 + warn；使用者已刪（baseline 有、現況無）→ 維持刪除。二進位／symlink：不合併，新版覆蓋前先確認使用者未改，改過就保留 + warn。多工具同一路徑 → 報錯。
回退：`git revert` 該 commit（`.version` + 初始檔 + baseline 同一 commit）。
vendor_kit 自身：`.version` 第一行變 → 下次 just 啟動器換薄殼、要求重跑（5-4 步 1）。
### 5e dev / undev
`dev base -p ~/src/base` → 檢查 `<dir>/dist/init.toml` 存在 → `.version.local` 加 `base = "path:…"`（並確保 git 忽略）→ `.<repo>/` 指向 `<dir>/dist`（symlink）→ 印記 `path:…`。ensure 看到 path 覆寫就跳過 install/verify。`undev base` → 刪該行 → 重裝 `.version` 版。
### 5f remove / uninstall
remove：flock → 有 dev 覆寫 → 1 → 刪 `.version` 行、`.<repo>/`、`baseline/<repo>/`、gen recipe → 印「以下初始檔保留，若不需要請 git rm：…」。
uninstall：逐工具 remove → 刪 `.vendor_kit/`、`.version`、`.version.local`、`.git/info/exclude` 內我們加的行 → 根 justfile 那行相同才刪 → 印摘要。

## 6. CI（契約⑤）
下游專案 CI（GitHub/GitLab 都只呼叫）：`.vendor_kit/ci/check.sh` = ensure（frozen）+ verify + 工具 smoke（工具 just 模組自帶的 `just <repo> check` 若有）。GitLab 拉 GHCR 私有 image：bot classic PAT（docker login）。工具 repo CI：`check.sh --dist`（dist 佈局、init.toml、image 可展開、amd64 builder）。vendor_kit 自身 CI：env-test → test-base → lint/unit/install/init/merge → release → release-test（amd64、arm64 原生 runner）。

## 7. 架構模組（引擎，容器內）
1 version（.version/.version.local 讀寫，flock）2 registry（GHCR tag/digest 查詢，只 update/add/upgrade 用）3 install（/dist 展開到 .<repo>/、印記、verify）4 init（init.toml 複製）5 merge（三方合併檔案語意 + git merge-file）6 baseline（baseline/ + metadata）7 launcher-gen（entry/vendor.just、gen/tools.just、check.sh 產生）8 cli（子命令、結束狀態、--porcelain）。主機側：啟動器（薄殼，非引擎模組）。模組間不可依賴工作目錄；import-linter 管。

## 8. 待使用者拍板清單（畫成便條）
(1) `.version` 頂層 key（vs 全放 [tools]）(2) dist image 單架構 amd64（vs 多架構 index）(3) update=只查／upgrade=套用（跟 base）(4) upgrade 含 install+合併+推 baseline（推翻「只改 .version 就停」）(5) 自身升級停下要求重跑（vs 自動 re-exec）(6) remove 不開 --purge、bootstrap 第二次拒絕、uninstall 動根 justfile 那行的例外 (7) Renovate 路徑要 PR 作者本機補 upgrade（vs CI bot commit）(8) 三方合併第一版邊界（二進位/symlink 不合併）(9) ensure 範圍 = 全部工具 (10) image 公開/私有 (11) dev 支援 vendor_kit 自身：第一版不做。
