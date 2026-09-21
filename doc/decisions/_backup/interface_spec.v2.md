# vendor_kit 介面規格（interface reference）v2（2026-09-19）

用途：後續每張票唯一可引用的 input／output 定義。前版存於 `interface_spec.v1.md`。

來源優先序（高 → 低）：
1. `grilling.md` 最晚條目（2026-09-19：Q22 sync 快路徑、Q23 結束碼 3、Q24 vk-resolve 格式與實作層取捨、Q25 選項表、Q26 離線 `.digest`、Q27 多工具彙總、「規格審查 16 條必修」直接採納）。
2. `interface_spec_review.md`「最終建議」一～五節（16 條必修、22 個待定的建議值、vk-resolve/1 骨架、結束碼 3 邊界、F1 定案）與「規格與定案不符」清單——全部套用，除非與 grilling 相衝（grilling 勝）。
3. `proposal_v2.md`：v2.5 → v2.4 → v2.3 → v2.2 → v2.1 → 正文。
4. 其他 decisions／issue（#26、#27、#28、#29、base_pitfalls、compat、isolation、contract）。

每條規格後以 <sub>[來源]</sub> 標注；`[待定]` 集中於 §9；本次每處改動的依據列於 §10；矛盾處理於 §11。占位符：`<repo>` 工具 repo 名、`<ns>` just 命名空間、`<dir>` 目錄、`<tag>`、`<digest>`、`<ref>` = `<image>:<tag>@sha256:<digest>`、`vX`／`vY` 引擎版本、`P` 協定整數、`N` schema 整數、`<org>` GitHub 組織名、`<id>` 交易 id、`<專案根>` = 含 `.vendor_kit/` 的目錄。

## 0. 共通前提（所有動詞）

| 項目 | 規格 |
|---|---|
| 專案根 | = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；不是 git toplevel。第一次 `install` 時尚無 `.vendor_kit/`，候選專案根 = 呼叫目錄。<sub>[grilling Q20 定案（改）；review I-47]</sub> |
| 執行位置 | vendor_kit 動詞只准在專案根執行：recipe 檢查 `invocation_directory() == justfile_directory()`，否則 1 印 6-9。例外：`sync` 豁免此檢查（由工具 recipe 的 `_sync` 自動前置時已 `cd` 回專案根，見 §3.6）。工具自己的 recipe 是否擋由工具決定。<sub>[grilling Q20 修正；review 最終建議五 F1]</sub> |
| git | 專案根須在某 git repo 內（主機側 `git rev-parse --is-inside-work-tree`）；引擎不讀 `.git`、不碰 index；不做 `git init`。禁止巢狀：install 時上層**或下層**已有 `.vendor_kit/` → 1。worktree（`.git` 是檔）與 submodule 同樣適用（後者以 §7.4-20 實測為準）。<sub>[grilling Q20、19條-1、-10；review I-47]</sub> |
| 主機需求 | docker ≥ 19.03（或 Podman ≥ 4.9，見 §3.1）、just ≥ 1.33.0（GitHub release 下載版）、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA → issue v2。主機命令白名單見 §3.1。<sub>[grilling Q4、Q8、19條-2、-13；v2.4-10]</sub> |
| 不變量 | 對使用者的檔：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（= 不用工具版本取代客製內容；例外只有根 justfile 一行、根 `.dockerignore` 三行、已納管初始檔經同意的換版／三方合併）。自動化（sync）只碰不進 git 的東西（cache/、gen/）。never fail silently。<sub>[grilling 隔離題、Q22 補；proposal §1；isolation 最終建議]</sub> |
| 詢問通則 | 需詢問但無 tty／EOF 且無 `-y` → 1 印 6-4；EOF／Ctrl-C = 中止整個 apply 回 1、不套用、**不記 declined**（declined 只記明確回答「否」）。明確回答「否」→ 不寫、metadata 依 §4.3 記錄。`-y` 只省略詢問，不授權覆蓋既有未納管檔、不硬加 append 行、**不解除 frozen**。<sub>[grilling 19條-6、Q13；v2.5-1、v2.5-4；review Claude 原文 12]</sub> |
| frozen | `CI` 真值規則：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ frozen；check.sh 自己 `export CI=1`。frozen = 不寫任何 tracked 檔、不查最新版；升為失敗的警告**明列**：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫、需改 tracked 檔（與 `-y` 無關）；Q15 的「沒納管／拒絕過」提醒**不**紅燈；仍拉鎖定版 image、仍寫 cache/、gen/。`update` 不受 frozen 影響（唯讀、不寫檔）。<sub>[v2.1 A；v2.2 A；v2.5-1；review 必修 4；review I-02、Claude 原文 25]</sub> |
| 進度日誌 | add／upgrade 記 metadata `[progress]`；remove／uninstall／undev／prune 放 `.vendor_kit/.tmp.<verb>.<id>.toml`（§4.6）。可寫動詞（add／remove／upgrade／undev／uninstall／install）開始前偵測到未完成交易 → 先恢復再繼續，失敗明列 6-27；唯讀動詞（sync／update／help）只偵測並印 6-33 提示重跑原動詞，**不自動恢復**、不寫任何檔。<sub>[grilling 進度日誌條、Q24；v2.2 C；review 必修 9]</sub> |
| 引擎環境 | 容器內 `LC_ALL=C.UTF-8`、`TZ=UTC`，時間戳 UTC ISO 8601；HOME 指容器內暫存（實作細節）。使用者身分見 §3.1 `-u` 規則。<sub>[grilling 19條-3、-4]</sub> |
| 路徑 | 啟動器一律引號（含空白、`$`、非 ASCII）；vk-resolve 內自由文字以八進位跳脫（§3.3）。<sub>[grilling 19條-8、Q24]</sub> |
| 多工具彙總 | 不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；`update` 同時遇 1 與 2 → 1；訊息全列。<sub>[grilling Q27]</sub> |
| 結束碼 3 | 版本／協定／schema 不合，須先升級或退回才能繼續；回 3 時**零寫入**；新舊以 P／schema 比較，不用版本字串；floor 檢查先於任何上網。細節 §2。<sub>[grilling Q23]</sub> |

## 1. 使用者動詞

語法：`just vendor_kit <verb> [args]`；所有動詞 recipe 一律 `verb *args` 一行轉發（`set positional-arguments` 只在 vendor.just），各動詞 `--help` 由引擎印。分組 `[group('常用')]`：add、upgrade、dev；`[group('進階')]`：其餘。<sub>[proposal §2]</sub> 不開：init、ensure、diff、accept、rollback、`--repair`（併進 install 冪等修復）、`--purge`（明確不提供，永不刪使用者檔；開 issue 供後續討論）、`--porcelain`、`--tag`。<sub>[proposal §2；v2.1 E；grilling Q25]</sub>

### 1.1 選項總表（Q25）

| 選項 | 短形 | 型別 | 適用 | 說明 |
|---|---|---|---|---|
| `--tool <repo>[@<tag>]` | `-t` | string，可重複 | bootstrap.sh | 接入的工具與版本；`@<tag>` 省略 = 最新正式版 |
| `--yes` | `-y` | bool | bootstrap.sh、install、uninstall、add、remove、upgrade、prune | 免詢問（不解除 frozen） |
| `--path <dir>` | `-p` | string | dev `<repo>` | 本機工具目錄 |
| `--image <tag>` | `-i` | string | dev `vendor_kit` | 本機引擎 image tag（只能 tag） |
| `--help` | `-h` | bool | 全部 | 由引擎印；bootstrap.sh 自印 |
| `--dry-run` | — | bool | uninstall、add、remove、upgrade、prune | 唯讀預覽（仍拉 image 展開） |
| `--source <image>` | — | string | add | image 路徑不符 `<org>/<repo>-dist` 慣例時 |
| `--local <image tag 或 tar>` | — | string | bootstrap.sh、add | 離線：tar 先 `docker load`；值的判別 [待定 B1] |
| `--exit-code` | — | bool | update | 有新版回 2 |
| `--timeout <秒>` | — | 正整數 | bootstrap.sh、add、upgrade、sync、undev | = `VENDOR_KIT_PULL_TIMEOUT`，由啟動器攔截、不轉發引擎；優先於環境變數 |
| `--no-justfile` | — | bool | install | 跳過根 justfile 步驟只印指示 |
| `--protocol P` | — | 整數 | 內部 | 薄殼→引擎全域旗標，不列 help |

版本一律寫在位置參數：`<repo>@<tag>`、`vendor_kit@<tag>`；`@<tag>` 比現版舊 → warn 仍執行。短選項只有 `-t`、`-y`、`-p`、`-i`、`-h`。<sub>[grilling Q25、19條-7]</sub>

### 1.2 動詞表

| 動詞 | 語法 | 位置參數 | 前置檢查 | 副作用（寫哪些檔，見 §4） | 詢問點（`-y`／無 tty） | 結束碼 | stdout／stderr 概要 |
|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag 或 tar>] [--timeout <秒>] [-h]` | 無 | 在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref；floor 檢查（§2）<sub>[grilling Q8、Q18；v2.4-5]</sub> | `docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref → 引擎 `install` → 每個 `-t` 呼叫 `add <repo>[@<tag>]`；`--local` 時 version.toml 仍寫正式 ref（tar 由同名 `.digest` 旁檔取得 index digest，§4.8）、version.local.toml 寫 `vendor_kit = "<tag>"` + `vendor_kit_image_id`，在 install 成功後才寫、失敗清除；不自刪。離線包 = `bootstrap.sh --local`（無獨立 `local_bootstrap.sh`）<sub>[proposal §2；#27；grilling Q26；v2.5-8；review 必修 15]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 | 0；1 失敗不留半成品（只對第一次 install 成立）；3 見 §2 <sub>[proposal §2；v2.2 C]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" -w /repo <引擎 ref> --protocol P install` <sub>[#27；review B7]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 + 6-17 <sub>[codex_verbs]</sub> | 在 git repo 內（否 → 1 + 6-16）；上層與下層皆無 `.vendor_kit/`（否 → 1 + 6-35）；不被 gen/.stamp 比對擋；第一次／修復判定用薄殼自描述首行（§4.5）：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 + 6-28 列差異不動 <sub>[proposal §2；grilling Q20、Q17；v2.5-8]</sub> | 建 `.vendor_kit/`：version.toml（含 schema、written_by）、entry.just、vendor.just、.gitignore、ci/check.sh、baseline/（空、不建 metadata）、gen/.stamp；根 justfile 無 → 建（§4.5 兩段式內容：import 一行 + `default:`／`\t@just --list` 兩行）；有 → 問後加一行；已含那行 → 不再加；根 `.dockerignore`：無 → 建（三行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`）；有 → 問後 append（同 §4.3 append 規則；插入的行記於 `baseline/.vendor_kit.toml`，見 §4.3 註）；再跑 = 用引擎重寫薄殼（hash 相符才重寫）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1]</sub> | 根 justfile 已存在 → 6-20「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示；`.dockerignore` 已存在 → 6-34 <sub>[proposal §2；isolation A1(4)；grilling Q22 補]</sub> | 0／1／3 | 印建立或修改了什麼（含加進根 justfile 的那一行、加進 .dockerignore 的三行） |
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分 <sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；進度日誌 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的三行同 append 規則問後只刪原文相同的；append 行問後只刪原文相同的 <sub>[proposal §2、§5；grilling Q22 補]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留） | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [--dry-run]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；兩段（resolve→apply、重驗指紋）但不經 docker create/cp <sub>[proposal §2；v2.3 §5；review Claude 原文 3]</sub> | 刪 version.toml 該行、cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行；初始檔永不刪，印清單；進度日誌 `.tmp.remove.<id>.toml` <sub>[proposal §2；v2.1 E；grilling 進度日誌]</sub> | append 過的行 → 6-21 問後只刪原文相同的（CRLF/LF 等價）<sub>[proposal §5；grilling Q13]</sub> | 0／1／3 | 初始檔清單 |
| `update [<repo>]` | `update [<repo>] [--exit-code]` | `<repo>` 可省 = 全部含 vendor_kit | 只查 registry（`tags/list` 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 frozen 影響；單段、不經 docker create/cp；無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；不可同時宣稱「已是最新」 <sub>[proposal §2；grilling Q11、Q27；#28]</sub> | 無 | 無 | 0 已列出；1 查詢失敗（任一工具 1 → 整體 1，即使另有新版）；`--exit-code` 有新版 → 2；3 <sub>[proposal §2；v2.1 E；grilling Q27]</sub> | 末行固定 6-15 <sub>[proposal §2]</sub> |
| `upgrade [<repo>[@<tag>]]` | `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 可省 = 全部含 vendor_kit 自身；`vendor_kit[@<tag>]` 為特殊值；`@<tag>` 限單一 repo | 順序：(0) metadata `conflicts` 非空且檔案仍含 `<<<<<<< vendor_kit:baseline` → 2 停（檔案失蹤不算已解）；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 `@<tag>`；frozen 不查）；無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新版新增 `<ns>`／dest 的全域撞名）再動任何東西；不帶 repo 且引擎有新版 → **本次只改第一行、工具不升** <sub>[v2.2 D；v2.1 B；v2.2 B；v2.5-6、-7；proposal §2；review I-20]</sub> | resolve → docker → apply：cache/、gen/<repo>.stamp、初始檔逐檔（§4.3 狀態機，N 讀自 `/dist/<repo>`）、baseline 推到新版（有衝突仍推；解析失敗不推）+ metadata、gen/tools.just；version.toml 最後寫。自身：(a) 不帶 repo 遇引擎新版 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器比對第一行前後（§3.4）→ 用新引擎跑 `upgrade vendor_kit`；(b) `upgrade vendor_kit[@<tag>]`（單段救援路徑）：查 registry（`@<tag>`／frozen 不查）→ 有新版且薄殼 hash 相符 → 改第一行 → 啟動器再以新 ref 跑一次 → 新引擎重產薄殼四檔 + gen/.stamp → 1 + 6-2；無新版且薄殼相符 → 0 無變更；只重產薄殼 → 1 + 6-2；`@<舊版>` 降版：目標引擎（以其 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 + 6-10 <sub>[v2.3 §2；v2.5-7；grilling Q19、Q23；review 必修 6、「自身升級第二次」一致]</sub> | 逐檔 6-22：「X 換成新版？」／「你和新版都改了 X，要三方合併嗎？」／新增檔「要建 X 嗎」（拒絕 → state=declined + declined_hash）／二進位／symlink 未改 → 問後換、改過保留 + warn／append 行找到 → 問後替換、找不到 → 不動印新內容；`-y` 全免問；CI 且需改 tracked 檔 → 1 印清單（與 `-y` 無關）<sub>[proposal §5；grilling Q14、Q6；v2.5-1；review 必修 10]</sub> | 0；1 工具層不動 version.toml（自身升級已改第一行後回 1 是明列例外）；2 有衝突（留標記、印檔名、baseline 仍推到新版、解完重跑直到乾淨；`git merge-file` 衝突數映射為 2，其 I/O／執行錯誤 → 1）；3 <sub>[proposal §2；v2.3 §2；v2.2 D；grilling Q19、Q23；review I-25]</sub> | `--dry-run`：印會問哪些檔、6-6～6-8、metadata 遷移明列；dest 在 CI 路徑時 6-29 <sub>[grilling Q14、Q15]</sub> |
| `dev <repo>` | `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | `<repo>` 必填 | `-p`（工具必填）／`-i`（僅 `vendor_kit`，只能 tag 不能 digest）互斥；工具必須已在 version.toml（否 → 1）；`<dir>/dist/init.toml` 存在（缺 → 1）；CI 拒絕；單段、不經 docker create/cp；`-i` 的 image 以 LABEL P／schema 判定為「舊」時允許但禁止重產 tracked 薄殼（§2 (d)）<sub>[proposal §2；v2.2 B；v2.3 §5；grilling Q19；review Claude 原文 35]</sub> | 工具：version.local.toml `[tools].<repo> = "path:<dir>"`，cache/<repo>/ 改 symlink → `<dir>/dist`（唯讀性只在容器 mount 上成立），gen/<repo>.stamp 第一行 `path:<dir>`。自身：version.local.toml `vendor_kit = "<tag>"` + `vendor_kit_image_id`；之後啟動器用 `docker image inspect` 驗 ID、不 pull <sub>[proposal §2；v2.2 B；review 必修 3、I-42]</sub> | 無 | 0／1／3 | — |
| `undev <repo>` | `undev <repo>`／`undev vendor_kit` | `<repo>` 必填 | 未啟用 = 0 + 提示 | 兩段：建日誌 `.tmp.undev.<id>.toml` 後撤 version.local.toml 該行（`undev vendor_kit` 一併撤 `vendor_kit_image_id`；最後一個覆寫撤掉後刪除整個檔）→ 重新 materialize 鎖定版（經 docker create/cp）；失敗 → 1 保留可恢復狀態。`undev vendor_kit`：下次 just 用 version.toml 引擎，gen/.stamp（`<tag>`）≠ ref → 只提示 6-1、不重寫 <sub>[proposal §2；v2.2 B；v2.3 §5；v2.5-10；review F2、I-31]</sub> | 無 | 0／1／3 | — |
| `sync [<repo>]` | `sync [<repo>]` | `<repo>` 可省 = 全部 | 每次工具 recipe 自動前置（§3.6）；快路徑（§3.6）；引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；未完成交易 → 6-33 不恢復 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9]</sub> | 只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp。每工具順序：覆寫 path → 跳過 materialize/verify（仍查完成標記、baseline 落後）；cache 缺或印記第一行 ≠ 鎖定 digest → materialize；否則 verify sha256 → 失敗 → 重裝 + warn；tools.just 缺或需重生 → 重生。無待辦 → resolve 回 `apply|no` 快路徑 0（不起第二個容器）<sub>[v2.3 §4；v2.2 E；v2.5-9]</sub> | 無 | 0；1：薄殼不符、metadata 無完成標記（6-13）、CI 下 baseline 落後（6-5）、CI 下任何 local 覆寫；3 <sub>[proposal §2；v2.1 A]</sub> | 本機 baseline 落後 → warn 提示 upgrade |
| `prune` | `prune [-y] [--dry-run]` | 無 | 兩段：`resolve prune` 輸出 `keep` 清單（version.toml + version.local.toml 引用的全部 image）；啟動器 `docker {container,image,network,volume} ls --filter label=io.github.<org>.vendor_kit=1` 列出候選、扣掉 keep；image 只刪「帶 label 且本專案未引用」者（共享 daemon 上其他專案的引用不可知 → 文件明寫、`--dry-run` 先看）；活躍（未恢復）的 `.tmp.<verb>.<id>.toml` 不刪、列出提示 6-33 <sub>[grilling 9 修正、9 補充、Q24；review A1、I-33、I-34]</sub> | 啟動器執行 docker rm／image rm／network rm／volume rm（不掛 docker socket）；`apply prune` 刪失效的 `.vendor_kit/.tmp.dist.*/` 與已完成交易殘留的 `.tmp.*` | 列出候選後 6-32「要刪除以上 vendor_kit 資源嗎？」（`-y` 免問） | 0／1／3 | 列出刪了什麼、保留什麼（含原因） |
| `help`／`h` | `help` | 無 | 不觸網、不安裝、不偵測交易以外的任何狀態 | 無 | 無 | 0 | 命名空間層說明；help 明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」<sub>[codex_verbs]</sub> |

## 2. 結束碼總表

| 碼 | 定義 | 動詞例外／特例 |
|---|---|---|
| 0 | 成功（含 warn）；`add` 已接入完成、`remove` 未接、`undev` 未啟用、`upgrade vendor_kit` 無新版且薄殼相符皆 0 + 提示 <sub>[proposal §2；review 一致]</sub> | — |
| 1 | 一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動 <sub>[proposal §2；compat 條 4]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3 <sub>[v2.3 §2；grilling Q23]</sub> |
| 2 | 合併衝突（留 `<<<<<<< vendor_kit:baseline` 標記、印檔名、baseline 仍推到新版）<sub>[proposal §2；v2.2 D]</sub> | `update --exit-code` 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔 baseline 不推、記入 `conflicts` <sub>[v2.1 E；review Claude 原文 29]</sub> |
| 3 | 現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且**零寫入**：(a) 薄殼 P < 引擎 floor_P → 6-18；(b) 引擎讀到 schema > 支援上限 → 6-19；(c) `upgrade vendor_kit@<舊版>` 目標引擎 P／schema 低於現有檔 → 6-10；(d) `dev vendor_kit -i` 的引擎 P／schema 低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 提示先 `upgrade vendor_kit`。「舊」一律以 P／schema 比，不以 SemVer。網路／認證／不存在 → 1，不得偽裝成 3；floor 檢查在任何上網之前（啟動器可先 `docker image inspect` 引擎 LABEL 判 floor）<sub>[grilling Q19、Q23；review 最終建議四；contract 3]</sub> | — |

多工具彙總見 §0；舊薄殼對未知碼原樣傳出、不吞。<sub>[grilling Q27；compat codex 原文]</sub>

## 3. 薄殼 ↔ 引擎協定

### 3.1 啟動器（POSIX sh；本體為 vendor.just 內的 recipe 殼；不解析 TOML、不 eval）<sub>[proposal §6；v2.2 C]</sub>

| 項目 | 規格 |
|---|---|
| 主機命令白名單 | `sh`（含內建 `printf`、`read`、`trap`、`kill`、`cd`）、`grep`、`sed`、`id`、`mktemp`、`rm`、`sleep`、`git rev-parse`、`docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}`；check.sh 另可用 `git ls-files`。lint 擋清單外的命令 <sub>[review 必修 12；grilling Q24]</sub> |
| 引擎 ref 取得 | 以 §4.1 正規行 regex 於 version.local.toml（覆寫優先）→ version.toml 取 `vendor_kit`；命中數 ≠ 1（0 或重複）→ 1 明確訊息 <sub>[base_pitfalls 1-11；v2.1 B；review 必修 11]</sub> |
| 引擎 image 取得 | 一律先 `docker image inspect <ref>`：本機有 → 不 pull（離線可用）；無 → `docker pull <ref>`（逾時 §5）。local 覆寫時：`docker image inspect <tag>` 的 `.Id` 必須 == version.local.toml `vendor_kit_image_id`，否則 1；**不 pull**（不用 `--pull never`，docker 19.03 無此旗標）<sub>[review 必修 3；grilling Q26]</sub> |
| docker run 參數 | `docker run --rm [<使用者旗標>] -v "<專案根>:/repo" -w /repo [-v "<專案根>/.vendor_kit/.tmp.dist.<id>:/dist:ro"] [-v "<dir>/dist:/dist/<repo>:ro"]… [-v "<TOKEN_FILE>:/run/vk-token:ro" -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.<org>.vendor_kit=1 --label io.github.<org>.vendor_kit.project=<專案根絕對路徑> <引擎 ref> --protocol P <子命令> [args]`。`--protocol P` 為全域旗標，一律在子命令之前；`-w /repo` 必給（不依賴 image 的 WORKDIR）；`-it` 只在 apply 且互動（有 tty、無 `-y`、非 frozen），**resolve 永不 `-t`**；啟動器 `trap … EXIT INT TERM` 清容器與 `.tmp.dist.<id>/` <sub>[proposal §6；v2.2 B、C；#27；grilling Q16、19條-5、9 補充、Q24；review 必修 6、B5、B7]</sub> |
| 使用者旗標 | 偵測：`docker info --format '{{.SecurityOptions}}'` 含 `name=rootless` → rootless，不加 `-u`；`docker --version` 含 `podman` → 加 `--userns=keep-id`、不加 `-u`；其餘（rootful docker）加 `-u "$(id -u):$(id -g)"` <sub>[review 必修 6（rootless）、Claude 原文 14；grilling 12 修正]</sub> |
| `-e` 白名單 | 轉發：`CI`（照原值）、`VENDOR_KIT_NO_LOCK`；`VENDOR_KIT_REGISTRY_TOKEN`／`_USER` 只在 update／upgrade 的 resolve 階段；`VENDOR_KIT_REGISTRY_TOKEN_FILE` 改為 `-v <主機檔>:/run/vk-token:ro` 並傳容器內路徑（同階段）。啟動器自讀不轉發：`VENDOR_KIT_PULL_TIMEOUT`。其餘一律不轉發（`HTTP_PROXY` 等 → v2）<sub>[#28；grilling 19條-2；review 必修 5、B2]</sub> |
| 工具 image 展開 | 每工具先 `docker image inspect <ref>` 有則略過 pull → `docker create --label io.github.<org>.vendor_kit=1 --label …project=<專案根> <ref> /x` → `docker cp c:/dist/. "<專案根>/.vendor_kit/.tmp.dist.<id>/<repo>/"` → `docker rm`；不帶 `--platform`（daemon 挑原生）；不執行工具 image <sub>[proposal §6；v2.1 C；#26；grilling Q24、Q26]</sub> |
| 暫存目錄 | 專案內 `.vendor_kit/.tmp.dist.<id>/`（`mktemp -d "<專案根>/.vendor_kit/.tmp.dist.XXXXXX"`；同檔案系統、remote docker context 亦可掛）；trap 刪；自有 .gitignore 擋 <sub>[grilling Q24；review B6]</sub> |
| 兩段編排 | 兩個獨立屬性：**需展開 image**（docker create/cp）= add／upgrade／sync／undev；**兩段**（`resolve <verb>` → 主機 docker → `apply <verb>`，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；**單段** = install／`upgrade vendor_kit`／update／dev／help。`--dry-run` = `apply --dry-run`（也要先拉 image 展開）<sub>[v2.3 §5；v2.2 C；v2.5-10；review 必修 7、Claude 原文 3]</sub> |
| 鎖 | 鎖在引擎 version 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗，印 6-26）；`VENDOR_KIT_NO_LOCK=1` 跳過；啟動器不鎖 <sub>[proposal §6；v2.1 C；base_pitfalls 3-8]</sub> |
| 自身升級編排 | §3.4 |
| pull 失敗 | 印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列為「主機錯誤」）+ 僅在 add／bootstrap 提示 6-24 的「離線可用 `--local`」（upgrade 不支援離線，不提示）；本機已有 image 時不 pull <sub>[base_pitfalls 2-9；review I-37、I-38]</sub> |
| 逾時 | `VENDOR_KIT_PULL_TIMEOUT`／`--timeout`：單次 pull 總經過時間，預設 300 秒，只收正整數（0 或非數字 → 1）；POSIX 實作 = 背景 pull + 每秒輪詢 + `kill`；逾時 → 1 + 6-31 指出 ref <sub>[grilling 19條-14、Q24；review B3]</sub> |

### 3.2 引擎子命令與 argv

| 子命令 | argv | 說明 |
|---|---|---|
| `install`、`update`、`dev`、`help`、`upgrade vendor_kit[@<tag>]` | `--protocol P <verb> [verb args]` | 單段對外動詞，argv 與 §1 相同（`*args` 原樣轉發）<sub>[proposal §6；grilling Q16]</sub> |
| `resolve <verb>` | `--protocol P resolve <verb> [verb args]` | verb ∈ add／remove／upgrade／sync／undev／uninstall／prune。只讀：讀 version.toml／local、查 registry（frozen 不查）、算執行計畫（要拉哪些 image@digest、mount、指紋、apply 與否），stdout 回啟動器（§3.3）；不詢問、不寫任何檔、無 TTY <sub>[v2.1 C；v2.2 C；review 三]</sub> |
| `apply <verb> [--dry-run]` | `--protocol P apply <verb> [--dry-run] [verb args]` | 讀 `/dist/vk-resolve`（啟動器把 resolve 原始 stdout 存成 `.tmp.dist.<id>/vk-resolve` 一起掛入）→ 拿 flock → 重算指紋與計畫中的 `fingerprint` 比對（不同 → 1 + 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 需改 tracked → 1）→ 建進度日誌 → 寫入 → 最後刪日誌；不重新選最新版 <sub>[v2.3 §6；v2.2 C；v2.5-3；review 三]</sub> |
| 內部（不對外） | `materialize`、`verify`、`merge` | 不列入契約 <sub>[proposal §6]</sub> |

`--protocol P`：單一整數，與 release 版號分開，從第一版就有（P=1）；引擎接受 `[floor_P, current_P]` 並以呼叫方的 P 輸出行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1。<sub>[grilling Q16；compat codex 2]</sub>

### 3.3 `vk-resolve/1` stdout 格式

**呼叫**：`docker run --rm [<使用者旗標>] -v "<專案根>:/repo" -w /repo [-e …] <引擎> --protocol P resolve <verb> [args]`，永不 `-t`。resolve 結束碼非 0 → 啟動器不讀 stdout，原碼傳出（1／2／3）。啟動器把 stdout **整份**存到 `.tmp.dist.<id>/vk-resolve`，先驗文法再動任何 docker；之後整份原樣掛進 apply（`/dist/vk-resolve`）供重驗指紋。<sub>[grilling Q24；review 三]</sub>

**文法**（P=1）：
```
vk-resolve/<P>            ← 第一行；P = 呼叫方 --protocol 的值（不是引擎的 current_P）
<kind>|<f1>[|<f2>…]       ← 每行一筆；欄位以單一 `|` 分隔；UTF-8；LF 結尾；無空行、無註解；禁 CR／NUL／BOM
end|<N>                   ← 最後一行，之後立即 EOF；N = 記錄行數（不含首行與 end 行）
```

欄位類別：
- **安全字串**（`<kind>`、`<name>`、`<repo>`、`yes|no`、整數）：`[A-Za-z0-9_.-]+`。
- **ref**：`[A-Za-z0-9_.:/@-]+`，引擎以 image-reference parser 驗證後才輸出。
- **自由文字**（`<dir>` 等路徑；任何 byte）：以 POSIX `printf '%b'` 可解碼的八進位跳脫編碼——凡不在 `[A-Za-z0-9_./:@+=,-]` 的 byte 一律寫成 `\0ooo`（反斜線、`0`、三位八進位；例：空白 `\0040`、`|` `\0174`、`\` `\0134`、非 ASCII 逐 byte）。啟動器一行解碼：`dir=$(printf '%b' "$f2")`，結果只當單一引號 argv 使用、不 eval、不 source。編碼結果不含空白與 `|`，故 `IFS='|' read -r kind f1 f2 f3` 可直接切欄。<sub>[grilling Q24]</sub>

| kind | 欄位 | 筆數 | 啟動器動作 |
|---|---|---|---|
| `pull` | `<name>\|<ref>` | 0..n | `docker image inspect` 有則略，否則 `docker pull <ref>`（逾時／失敗 → 6-24／6-31）。name = `vendor_kit` 或 `<repo>` |
| `extract` | `<repo>\|<ref>` | 0..n | 同 pull 後 `docker create … <ref> /x` → `docker cp c:/dist/. ".tmp.dist.<id>/<repo>/"` → `docker rm`；apply 見 `/dist/<repo>/`。同一 repo 不得同時有 extract 與 mount |
| `mount` | `<repo>\|<dir 八進位跳脫>` | 0..n | dev 覆寫：解碼後驗 `<dir>/dist/init.toml` 存在（缺 → 1）→ `-v "<dir>/dist:/dist/<repo>:ro"` |
| `engine` | `<ref>` | 0..1 | 只在 `upgrade`（不帶 repo）：apply 會把第一行改成此 ref。啟動器先 pull（或 local 覆寫時 inspect 驗 ID）；apply 後依 §3.4 接手。有 engine 時本次不得夾帶工具寫入 |
| `fingerprint` | `<sha256 hex64>` | 恰 1 | 不解析，隨檔交給 apply。算法見下 |
| `apply` | `yes` \| `no` | 恰 1 | `no` → 啟動器驗完文法後直接 exit 0（sync 快路徑，不起第二個容器）；`no` 時不得有 pull／extract／mount／engine 記錄。`yes` → docker 階段後跑 `apply <verb> [--dry-run] [args]` |
| `keep` | `<name>\|<ref>` | 0..n | 只在 `prune`：本專案引用、不可刪的 image（含 local 覆寫的 `<tag>`）。prune 的 `apply` 只處理 `.tmp.*` |
| `end` | `<N>` | 恰 1 | 必為最後一行 |

**啟動器驗證**：首行 ≠ `vk-resolve/<P>`、缺 `end`、N 不符、`end` 後仍有資料、未知 kind、欄位數不對、`fingerprint`／`apply` 不是恰一筆、`no` 卻附動作記錄、安全字串含非法字元 → 1 + 6-30，不得繼續；引擎宣稱的 P 真不支援 → 3。<sub>[review 三、codex C-1]</sub>

**指紋算法**：sha256（hex64）。引擎對下列輸入依路徑 byte 順序排序，串接 `<path>\0<kind>\0<sha256(content) 或 ->\n` 再 sha256：version.toml、version.local.toml（缺記 `-`）、每個 `baseline/*/.vendor_kit.toml`、metadata 中 state=managed／appended 的每個 dest（區分檔案／symlink／缺）、gen/.stamp 第一行、每個 gen/<repo>.stamp 第一行、`.tmp.*` 日誌清單、鎖定 digest、本機引擎 image ID（local 覆寫時）、本次 verb 正規化 argv（含 `--dry-run`／`-y`／frozen）。**不含**新版新增檔（resolve 時 N 未展開；apply 對新檔只建不存在者，已存在 → 不納管 6-11）。apply 拿鎖後重算，不同 → 1 + 6-12；詢問後、替換前對目標檔再查一次前像（flock 擋不住編輯器）。<sub>[review 三、I-12、I-13]</sub>

**範例 1：`upgrade`（不帶 repo）遇引擎新版**（只改第一行、工具不升）
```
vk-resolve/1
pull|vendor_kit|ghcr.io/<org>/vendor_kit:v1.3.0@sha256:aaaa…
engine|ghcr.io/<org>/vendor_kit:v1.3.0@sha256:aaaa…
fingerprint|9f2c…e1
apply|yes
end|4
```
**範例 2：`sync`，一個 cache 過期、一個 dev 工具（路徑含空白）**
```
vk-resolve/1
extract|base|ghcr.io/<org>/base-dist:v2.3.0@sha256:bbbb…
mount|robot_tools|/home/me/robot\0040tools
fingerprint|1c0e…77
apply|yes
end|4
```
**範例 3：`sync` 無待辦（快路徑）**
```
vk-resolve/1
fingerprint|1c0e…77
apply|no
end|2
```
**範例 4：`prune`**
```
vk-resolve/1
keep|vendor_kit|ghcr.io/<org>/vendor_kit:v1.2.0@sha256:…
keep|base|ghcr.io/<org>/base-dist:v2.3.0@sha256:…
fingerprint|77ab…03
apply|yes
end|4
```

**stderr**：診斷（warn、錯誤、問句以外的人看訊息）一律 stderr；apply 的 stdout 不作為協定通道（互動時 TTY 會合流）。**對舊 P**：不得輸出呼叫方不認識的 kind／欄位、不得要求其未提供的 mount／環境變數（缺少時明確拒絕）。<sub>[v2.2 C；compat 條 4；compat codex 2；review 一致]</sub>

### 3.4 自身升級的接手（啟動器）

「引擎已變」**不從 stdout 讀**：啟動器在 apply 前後各 grep 一次 version.toml 的 `vendor_kit` 正規行。apply 結束後 ref 變了（且 == 計畫的 `engine`）→ 以新 ref（local 覆寫有 `vendor_kit=` 則用該 image、驗 ID）跑 `docker run … <新 ref> --protocol P upgrade vendor_kit`，其結束碼原樣傳出（預期 1 + 6-2）；第二次第一行又變 → 1 + 6-2b，不再重跑。第一行已改但新引擎拉取／重產失敗 → 1 + 6-2b。<sub>[grilling Q24；review 必修 6；codex D1]</sub>

### 3.5 救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/，永久保證）

清單：`install`、`upgrade vendor_kit[@<tag>]`、`sync` 的「薄殼不符 → 1 + 6-1」判定、`help`。任何 ≥ floor 的薄殼可經此路徑叫任何引擎重產薄殼；反向（新薄殼叫舊引擎降版）亦然，受 §2 (c)(d) 限制。<sub>[grilling Q16；compat codex 3]</sub>

### 3.6 sync 自動前置（F1 定案）與快路徑（Q22）

| 項目 | 規格 |
|---|---|
| gen/tools.just | 每個 `<ns>.just` 一行 `mod? <ns> '../cache/<repo>/just/<ns>.just'`（`mod?`：cache 缺檔時其他 recipe 與修復入口仍可跑）；零 set 零 recipe <sub>[review 必修 2；grilling 16 條]</sub> |
| 工具模組內 `_sync` | 每個 `dist/just/<ns>.just` 必含私有 recipe，本體逐字：<br>`[private]`<br>`_sync:`<br>`\tcd {{quote(justfile_directory())}} && just vendor_kit sync`<br>（`justfile_directory()` 在模組內 = 根 justfile 所在目錄 = 專案根；用 `quote()` 不直接插字串）<sub>[grilling 16 條、F1；review 五]</sub> |
| 公開 recipe | 工具每個公開 recipe 相依 `_sync`（`build: _sync`）；例外集合：無（工具內全部公開 recipe）。vendor_kit 自身動詞（vendor.just 內全部）**不**自動前置 |
| `--dist` lint | `check.sh --dist` 以 `just --dump --dump-format json` 解析每個 `<ns>.just`：`_sync` 存在、私有、本體逐字相符；每個公開 recipe 的 dependencies 含 `_sync`；違反 → 失敗 <sub>[review F1、F4]</sub> |
| 限制（契約明寫） | just 在執行任何 recipe 前已載入所有模組：同一次 just 呼叫內不會看到 sync 重建後的新 recipe（Q9 契約）；cache 缺檔時 `mod?` 讓 `just vendor_kit sync` 仍可進入；1.33.0 fixture 通過才算結案（§7.4-25）<sub>[grilling Q9；review 五]</sub> |
| 快路徑 | `sync`（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml `vendor_kit` ref；version.toml `[tools]` 每個 `<repo>` 的 ref 之 digest == gen/<repo>.stamp 第一行（或 local 覆寫的 `path:<dir>`）；gen/tools.just 存在；無 `.tmp.<verb>.*.toml`；非 frozen。全相符 → 不起容器、0；任一不符或 frozen → 起引擎 `resolve sync`。每檔 sha256 verify 只在：CI（frozen）、快路徑有差那次（版本變動）、以及 [待定 F5] 的「明確 sync」情境做 <sub>[grilling Q22]</sub> |
| 快路徑前提 | `.vendor_kit/.gitignore` 明列 `cache/`、`gen/`、`version.local.toml`、`.tmp.*`；install 把 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*` 加進根 `.dockerignore`（無則建；有則問後 append、`-y` 免問）；工具契約：build 以專案根當 context 時不得再排除 `.vendor_kit/` 以外的方式繞過 <sub>[grilling Q22、Q22 補]</sub> |

## 4. 檔案 schema

通則：每個 vendor_kit 寫的 TOML 有 `schema = N`（integer）+ `written_by = "<vX>"`（string，純資訊，不作讀取門檻）；讀取門檻只看 `schema`；同 schema 只加不改；**讀時忽略未知欄位、寫時保留**（不能保留則拒絕寫）；只拒絕型別錯、重複宣告 → 1；schema 高於本引擎支援 → 3 + 6-19 零寫入；讀任一舊 schema → 直接寫當前 schema（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。第一版 `schema = 1`。<sub>[grilling 相容性其餘採納、16 條 written_by；review 必修 8、C1；base_pitfalls 1-11]</sub>

### 4.1 `.vendor_kit/version.toml`

| 項目 | 規格 |
|---|---|
| 進 git | 是；唯一來源。寫入者：install／add／upgrade／remove（apply 最後寫）；使用者、Renovate 可手改；sync 只讀。<sub>[proposal §3]</sub> |
| 正規行契約 | `vendor_kit` 行**唯一正規形**：整行 `vendor_kit = "<ref>"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號基本字串、無尾端註解、LF 結尾；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：`^vendor_kit[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$`（POSIX BRE，不用 `\s`）；命中數必須恰為 1（`grep -c`），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 `[tools]` 之前。禁止：BOM、重複鍵、`[vendor_kit]` 表旁路等 regex 讀不到／讀錯的等價寫法。<sub>[grilling 相容性其餘採納、16 條；review 必修 11]</sub> |
| 公開格式 | 工具可讀它寫來源紀錄。<sub>[grilling deploy 定案]</sub> |

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 是 | 引擎 ref `ghcr.io/<org>/vendor_kit:vN@sha256:<digest>`（多架構 index digest）<sub>[proposal §3；#26]</sub> |
| `schema` | integer | 是 | 啟動器不讀、只引擎讀 <sub>[compat codex 5]</sub> |
| `written_by` | string | 是 | 寫入引擎版本，純資訊 <sub>[review C1]</sub> |
| `[tools].<repo>` | string | 每工具 | `ghcr.io/<org>/<repo>-dist:<tag>@sha256:<digest>`（index digest；`add --local` 亦寫正式 index digest，來自 `.digest` 旁檔）<sub>[proposal §3；grilling Q26]</sub> |

```toml
vendor_kit = "ghcr.io/<org>/vendor_kit:v1.0.0@sha256:<digest>"
schema = 1
written_by = "v1.0.0"

[tools]
<repo> = "ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:<digest>"
```

### 4.2 `.vendor_kit/version.local.toml`

不進 git（自有 .gitignore 擋）；與 version.toml **同形**（同一套讀寫器）；寫入者 dev／undev／bootstrap `--local`；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；frozen 下存在任何覆寫 → sync 回 1。啟動器先讀它再退回 version.toml。<sub>[proposal §3；v2.1 A；isolation B(b)；review C3、I-31]</sub>

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 否 | 本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）<sub>[proposal §2；#27]</sub> |
| `vendor_kit_image_id` | string | 有 `vendor_kit` 時必填 | `sha256:<hex64>`，dev 時解析；啟動器每次 `docker image inspect` 比對，同 tag 重 build 才會被發現；`undev vendor_kit` 一併撤 <sub>[v2.2 B；review C2]</sub> |
| `schema`、`written_by` | integer、string | 是 | 同通則 |
| `[tools].<repo>` | string | 否 | `path:<dir>`（絕對路徑）；cache/<repo>/ 為 symlink → `<dir>/dist` <sub>[proposal §2、§3；review C3]</sub> |

```toml
vendor_kit = "vendor_kit:dev"
vendor_kit_image_id = "sha256:<image id>"
schema = 1
written_by = "v1.0.0"

[tools]
<repo> = "path:/home/me/<repo>"
```

### 4.3 `baseline/<repo>/.vendor_kit.toml`（metadata）

進 git；寫入者 add／upgrade；兼作 baseline/<repo>/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 `upgrade vendor_kit` 做並在 dry-run 明列。<sub>[proposal §3；grilling 相容性其餘採納]</sub>

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema`、`written_by` | integer、string | 是 | 同通則 |
| `source` | string | 是 | 這份 baseline 來自哪個工具 image `<ref>`（tag@index digest）= 最後合併版本；≠ version.toml → sync 本機 warn／CI 1 + 6-5；upgrade 先補待合併到該版然後停 <sub>[review C4；v2.2 D]</sub> |
| `local_image_id` | string | `add --local` 時 | `sha256:<hex64>`：本機 image ID ↔ `source` 的 index digest 對照，供離線驗證 <sub>[grilling Q26]</sub> |
| `complete` | bool | 是 | add 走完 materialize → 初始檔 → baseline 才 true；缺或 false → sync 1 + 6-13；true 且再 add → 0 無變更 <sub>[interface；proposal §2]</sub> |
| `conflicts` | array of string | 是（可空） | upgrade 回 2 時留標記或解析失敗的 dest 清單；仍含標籤 → 2 停；解析失敗的 dest 其 baseline 不推；解完重跑才清空 <sub>[v2.2 D；review Claude 原文 29]</sub> |
| `[[file]]` | table array | 每個範本一筆 | `dest`（string，相對專案根）；`state`（string，單一列舉）∈ `managed`（已納管）／`appended`（append 已插入）／`declined`（新增檔被拒、從未納管）／`unmanaged`（本來就有、沒納管）／`deleted`（使用者刪了已納管檔，upgrade 維持刪除）；`declined_hash`（string，選填）= 最近一次被拒絕的那版範本 N 的 sha256（已納管檔拒絕換版／合併時 state 維持 managed 只記此欄；新版 N 的 hash ≠ `declined_hash` → 再問一次，相同 → 不問但 6-6／6-8）；`lines`（array of string，只在 appended）= 實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）<sub>[grilling Q13、Q14、Q15、16 條；review C4、I-21、I-22]</sub> |
| `[progress]` | table | 交易中 | `state = "in-progress"`、`started`（UTC ISO 8601）、`verb`、`id`、`done`／`pending`（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、唯讀動詞 6-33 <sub>[v2.2 C；v2.3 §6；v2.5-3]</sub> |

註：install 對根 `.dockerignore` 的三行 append 不屬任何工具，記於 `baseline/.vendor_kit.toml`（同 schema，只含 `[[file]]` dest=`.dockerignore` state=appended lines=三行），uninstall 讀它刪原文相同行。<sub>[grilling Q22 補；本規格為實作補齊]</sub>

upgrade 逐檔狀態機（B=baseline、D=磁碟、N=新版讀自 `/dist/<repo>`；只對 state=managed、無待解衝突）：D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 `git merge-file --diff3`（標籤 `<<<<<<< vendor_kit:baseline` 等），衝突 → 2；不論結果 baseline 推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → **問後換**、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 `conflicts`、baseline 不推。任何拒絕 → 記 `declined_hash`（新檔 → state=declined）。<sub>[isolation C；proposal §5；v2.5-2、-4；review 必修 10；base_pitfalls 2-12]</sub>

### 4.4 `gen/.stamp`、`gen/<repo>.stamp`、`gen/tools.just`（不進 git）

| 檔 | 寫入者 | 內容 |
|---|---|---|
| `gen/.stamp` | 只由 install／upgrade vendor_kit | 第一行 = 產生薄殼的引擎 ref（local 覆寫時為 `<tag>`），供 sync grep 快速比對；不承擔薄殼 hash；fresh clone 缺此檔時相容判定改用薄殼自描述首行 <sub>[grilling Q17；review I-15]</sub> |
| `gen/<repo>.stamp` | materialize | 第一行 = 多架構 index digest `sha256:<hex64>`（與 version.toml 一致；`add --local` 亦為正式 index digest，本機驗證用 metadata `local_image_id`）或 dev 時 `path:<dir>`；**無 `image:<tag>` 形**；之後每檔一行 `<sha256>  <相對路徑>`（files/…、init.toml、just/<ns>.just）；verify 逐檔比 <sub>[v2.3 §3；#26；grilling Q26；review 必修 15]</sub> |
| `gen/tools.just` | sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換 | 每個 `<ns>.just` 一行 `mod? <ns> '../cache/<repo>/just/<ns>.just'`（一工具可多行），每行上方一行 `# <description>` 註解；零 set 零 recipe <sub>[v2.1 E；v2.3 §3；base_pitfalls 2-4；review 必修 2]</sub> |

### 4.5 薄殼（進 git，vendor_kit 擁有，人不改）

| 檔 | 內容 |
|---|---|
| 自描述首行 | entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：`# vendor_kit-shell/<P> engine=<vX> sha256=<hash>`；hash = 首行（含其換行）之後全部位元組 CRLF→LF 正規化後的 sha256（check.sh 的 shebang 行算進內容）；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 + 6-28 列差異不動（使用者 `git checkout` 還原後再跑）；mode 變更只 warn <sub>[grilling Q17；review Claude 原文 28；base_pitfalls §5 CRLF]</sub> |
| `entry.just` | `mod vendor_kit 'vendor.just'` + `import? 'gen/tools.just'`；零 set 零 recipe <sub>[proposal §2、§3]</sub> |
| `vendor.just` | 動詞 recipe 一行轉發 + 啟動器本體（POSIX sh recipe）；`set positional-arguments` 只放這；若實作把啟動器拆成獨立檔，該檔納入本表並帶自描述首行 <sub>[proposal §2]</sub> |
| `.gitignore` | `cache/`、`gen/`、`version.local.toml`、`.tmp.*` <sub>[proposal §3；grilling Q22]</sub> |
| `ci/check.sh` | §7 |
| 根 justfile（使用者的） | install 只加一行 `import '.vendor_kit/entry.just'`；無檔則建，內容逐字四行：<br>`import '.vendor_kit/entry.just'`<br>（空行）<br>`default:`<br>`\t@just --list`<br>（`default: @just --list` 單行為 just 語法錯誤）；uninstall 只刪完全相同行 <sub>[proposal §2；review 必修 1]</sub> |
| 根 `.dockerignore`（使用者的） | install append 三行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`（無則建；有則問）；uninstall 問後只刪原文相同行 <sub>[grilling Q22 補]</sub> |

### 4.6 `.vendor_kit/.tmp.*`

| 檔 | 規格 |
|---|---|
| `.tmp.<verb>.<id>.toml` | remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；`<id>` = 交易 id（UTC 時間戳 + 隨機，不用 `<repo>` 以免 uninstall 多工具撞名）；內容 = `schema`、`written_by`、`verb`、`id`、`targets`（array）、`started`、`done`／`pending`、`consents`（已取得的同意）；成功結束時刪；未完成 → 可寫動詞恢復、唯讀動詞 6-33；prune 不刪未恢復者 <sub>[grilling 進度日誌、Q24；review C5、I-33]</sub> |
| `.tmp.dist.<id>/` | 啟動器暫存（展開的工具 dist、`vk-resolve`）；trap 刪；prune 清殘留 <sub>[grilling Q24]</sub> |

兩者皆由自有 .gitignore `.tmp.*` 擋。

### 4.7 工具側 `dist/`、`dist/init.toml`、`Dockerfile.dist`、image

| 項目 | 規格 |
|---|---|
| `dist/` 佈局 | `dist/files/`（全部出貨，原樣展開到 cache/<repo>/files/）、`dist/init.toml`、`dist/just/<ns>.just`（每檔一個頂層命名空間，數量工具自決，`<repo>.just` 必須存在，每檔含 §3.6 `_sync`）；symlink／hardlink／特殊檔第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF <sub>[proposal §4；v2.2 E；#29；review I-41]</sub> |
| `Dockerfile.dist` | 逐字三行：`FROM scratch`／`LABEL io.github.<org>.vendor_kit=1`／`COPY dist/ /dist/`；純資料，不承諾可執行、vendor_kit 不檢查 binary；缺 LABEL → check.sh --dist 失敗（image 的 label 只能在 build 時加，pull 無法追加）<sub>[proposal §4；grilling Q21、16 條；review 必修 14]</sub> |
| image 命名 | 工具 `ghcr.io/<org>/<repo>-dist:<tag>`；引擎 `ghcr.io/<org>/vendor_kit:vN`；皆多架構 amd64+arm64（同一次 buildx）；工具 dist COPY-only、CI 驗兩平台位元組一致；引擎 image 只驗兩平台 LABEL（protocol／schema）一致；引擎 image 公開，工具自決（公開不可逆）；已釋出 image／index 子 digest／Release 資產／fixture 永不刪 <sub>[proposal §4；grilling Q4、Q7、相容性；review 必修 16]</sub> |
| label | 鍵前綴 `io.github.<org>.vendor_kit`。啟動器建的容器／network／volume：`…=1`、`….project=<專案根絕對路徑>`；引擎 image（build 時）：`…=1`、`….protocol=<floor_P>-<current_P>`、`….schema=<N>`；工具 image（build 時）：`…=1`。專案路徑 label 不加在 image 上。<sub>[grilling 9 補充、Q24；review B5、必修 14]</sub> |
| 工具契約（初始檔與 recipe） | 初始檔只能引用穩定入口 `just <ns> …`、`.vendor_kit/ci/check.sh`、`.vendor_kit/entry.just`、`.vendor_kit/version.toml`；不得寫死 cache 內部路徑；交付物執行期不得依賴 `.vendor_kit/`、version.toml、GHCR；rename／格式變更不得以 copy/append 假裝完成；工具 recipe 用 `cd {{quote(justfile_directory())}}` 回專案根，禁止相對 working-directory；每個公開 recipe 相依 `_sync`（§3.6）；工具的 build 若以專案根當 context，依賴 install 加進根 `.dockerignore` 的排除 <sub>[grilling Q14、deploy、Q22；base_pitfalls 1-4、2-13；proposal §4]</sub> |

`dist/init.toml`：

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema` | integer | 是 | 建置期契約（同 image 內讀寫），不進執行期矩陣 <sub>[contract 4；base_pitfalls 1-11]</sub> |
| `description` | string | 否 | 頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod 上方 `# <description>`；缺則 `<repo> <tag>` <sub>[review C6；base_pitfalls 2-4]</sub> |
| `[[file]].src` | string | 是 | 相對 `dist/`；正規化、不得越出 dist/ <sub>[review C6]</sub> |
| `[[file]].dest` | string | 是 | 相對專案根；正規化、不得越出 repo、不得指向 `.vendor_kit/`、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；append/append 允許（各工具行分開記，重疊或歸屬不明 → 拒絕）；引擎與 lint 都驗 <sub>[proposal §4；v2.2 E；review I-41]</sub> |
| `[[file]].strategy` | string | 否 | `"copy"`（預設）或 `"append"`，只有這兩值；根 `.gitignore`／`.dockerignore`／`.editorconfig` 類必須用 append，用 copy 指向它們 → check.sh --dist 報錯 <sub>[grilling Q12、Q6]</sub> |

```toml
schema = 1
description = "<repo> 的專案範本與 just recipe"

[[file]]
src = "files/Dockerfile"
dest = "Dockerfile"

[[file]]
src = "files/gitignore.snippet"
dest = ".gitignore"
strategy = "append"
```

### 4.8 離線包（Release 資產）

每個平台 tar（`docker save`）旁附同名 `.digest` 旁檔：`<name>.tar` + `<name>.tar.digest`，內容一行 `sha256:<hex64>` = 該 image 的正式多架構 index digest。`bootstrap.sh --local <tar>`／`add --local <tar>`：`docker load` 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 `local_image_id`；旁檔缺 → 1。離線可用：啟動器先 `docker image inspect`，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1「拉不到」不 hang（逾時）；離線 upgrade 不支援。<sub>[grilling Q26、19條-11]</sub>

## 5. 環境變數與參數

| 名稱 | 讀者 | 規格 |
|---|---|---|
| `VENDOR_KIT_REGISTRY_TOKEN` | 引擎 registry 模組 | registry 讀取憑證（GHCR：PAT classic `read:packages`，細節手動測後定）；只在 update／upgrade 的 resolve 階段以 `-e` 傳；不寫 log／檔、不傳給工具、dry-run 不印 <sub>[grilling Q11；#28]</sub> |
| `VENDOR_KIT_REGISTRY_USER` | 同上 | 換 token 的使用者名（GHCR 任意非空）<sub>[#28]</sub> |
| `VENDOR_KIT_REGISTRY_TOKEN_FILE` | 同上 | 主機檔路徑；啟動器 `-v <file>:/run/vk-token:ro` 並以 `-e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token` 傳容器內路徑；與 `_TOKEN` 同時設定 → 1「只能擇一」<sub>[#28；review 必修 5、I-36]</sub> |
| `VENDOR_KIT_NO_LOCK` | 引擎 version 模組 | `=1` 跳過 flock；啟動器轉發 <sub>[proposal §6；review 必修 5]</sub> |
| `VENDOR_KIT_PULL_TIMEOUT` | 啟動器（不轉發） | 單次 pull 總秒數，預設 `300`，只收正整數（`0`／非數字 → 1）；`--timeout` 優先 <sub>[grilling 19條-14、Q24；review B3]</sub> |
| `CI` | 啟動器（frozen 判定）→ 轉發引擎 | 真值規則：非空且不為 `0`／`false`（大小寫不敏感）→ frozen；check.sh `export CI=1` <sub>[review 必修 4]</sub> |
| `HTTP_PROXY`／`HTTPS_PROXY`／`NO_PROXY` | — | v2（issue），第一版不轉發 <sub>[grilling 19條-2]</sub> |
| 其餘 `VENDOR_KIT_*` | — | 不轉發；README 一節列出全部 `VENDOR_KIT_*` 與 `CI`，lint 擋未列者 <sub>[base_pitfalls 2-6；review B2]</sub> |
| docker label | 啟動器／prune | §4.7 |
| 暫存目錄 | 啟動器 | `.vendor_kit/.tmp.dist.<id>/`（§3.1）；不用 `TMPDIR` |
| 引擎容器內 | 引擎 | `LC_ALL=C.UTF-8`、`TZ=UTC`、`HOME=<容器內暫存>`（實作細節）<sub>[grilling 19條-3、-4]</sub> |

## 6. 訊息文字清單（逐字；`<…>` 為占位符；每句含可直接複製的指令）

| # | 時機 | 文字 | 來源 |
|---|---|---|---|
| 6-1 | sync 發現 gen/.stamp 第一行 ≠ 引擎 ref（含 undev vendor_kit 後） | `vendor_kit 已更新 <vX> → <vY>，請執行：just vendor_kit upgrade vendor_kit`（結束 1；缺 gen/.stamp 時 `<vX>` 讀薄殼自描述首行）| <sub>[review D1；grilling Q10]</sub> |
| 6-2 | `upgrade vendor_kit` 確實重產薄殼後 | `已升級引擎 <vX> → <vY> 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令`（結束 1）| <sub>[v2.3 §2；review D1]</sub> |
| 6-2b | 第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 | `引擎版本已鎖定為 <vY>，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit`（結束 1）| <sub>[review codex D1；§3.4]</sub> |
| 6-3 | update／upgrade／add 無 registry 憑證 | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）` | <sub>[#28；grilling Q11、Q25]</sub> |
| 6-4 | 需詢問但無 tty／EOF 且無 `-y` | `需要確認但沒有終端可互動。請加 -y，或在終端執行。`（結束 1）| <sub>[grilling 19條-6]</sub> |
| 6-5 | CI 下 baseline 落後 version.toml；Renovate PR 需合併 | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push`（結束 1）| <sub>[remaining Q5；proposal §7]</sub> |
| 6-6 | dry-run／check.sh 有拒絕過的範本 | `有 <N> 個範本你拒絕過` | <sub>[grilling Q14]</sub> |
| 6-7 | dry-run／check.sh 未納管檔 | `<X> 沒納管，與範本差 <N> 行` | <sub>[grilling Q15]</sub> |
| 6-8 | dry-run／check.sh 拒絕過且新版有更新 | `<Y> 你拒絕過，<vZ> 有新版` | <sub>[grilling Q15]</sub> |
| 6-9 | 不在專案根執行 | `請到 <dir> 執行`（結束 1）| <sub>[grilling Q20 修正]</sub> |
| 6-10 | `upgrade vendor_kit@<舊版>` 無法無損讀 | `目標引擎 <vY>（協定 <P>、schema <M>）無法無損讀取現有檔（schema <N>）。未修改任何檔。要退回舊版請 git revert 相關 commit。`（結束 3）| <sub>[grilling Q19、Q23]</sub> |
| 6-11 | add 初始檔已存在（copy） | `<X> 已存在，未納管；範本在 .vendor_kit/cache/<repo>/files/ 可自行比對` | <sub>[proposal §2]</sub> |
| 6-12 | apply 重驗指紋不同 | `專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …`（結束 1）| <sub>[v2.2 C]</sub> |
| 6-13 | sync metadata 無完成標記 | `<repo> 未完成接入，請執行：just vendor_kit add <repo>`（結束 1）| <sub>[proposal §2]</sub> |
| 6-14 | upgrade 補完待合併後另有新版 | `已補齊 <repo> 至 <vB>；另有新版 <vX>，再跑一次 just vendor_kit upgrade <repo> 可升` | <sub>[v2.2 D]</sub> |
| 6-15 | update 末行 | `套用：just vendor_kit upgrade` | <sub>[proposal §2]</sub> |
| 6-16 | install 非 git repo | `目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。`（結束 1）| <sub>[review D2 codex 模板]</sub> |
| 6-17 | `install <repo>` 誤用 | `install 不接受工具名稱。接入工具請執行：just vendor_kit add <repo>`（結束 1）| <sub>[review D2]</sub> |
| 6-18 | 薄殼／版本低於 floor | `目前薄殼或引擎低於支援下限 <floor>。請以 bootstrap.sh 重建。`（結束 3、零寫入）| <sub>[review D2；grilling Q23]</sub> |
| 6-19 | 引擎讀到 schema 高於支援上限 | `無法讀取 <file>：schema <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請使用支援此 schema 的引擎，或使用 version.toml 指定的引擎。`（結束 3、寫入前退出）| <sub>[review D2、必修 8；grilling Q23]</sub> |
| 6-20 | 問句：根 justfile | `要在 justfile 加這一行嗎：import '.vendor_kit/entry.just'`／`要從 justfile 刪這一行嗎：import '.vendor_kit/entry.just'` | <sub>[proposal §2]</sub> |
| 6-21 | 問句：append | `要在 <X> 加這幾行嗎`（接列出行）／`要刪我們加在 <X> 的這幾行嗎`（接列出行）| <sub>[proposal §2、§5]</sub> |
| 6-22 | 問句：upgrade 逐檔 | `<X> 換成新版？`／`你和新版都改了 <X>，要三方合併嗎？`／`要建 <X> 嗎`／`<X> 是二進位檔，要換成新版嗎？` | <sub>[proposal §5；grilling Q14；review 必修 10]</sub> |
| 6-23 | bootstrap just 太舊 | `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。` + 固定兩行 `下載：<平台對應 URL>`、`安裝：<不覆蓋既有檔的安裝指令>`（不新增 curl／tar 主機依賴、不覆蓋既有 just）| <sub>[review D2；grilling Q8]</sub> |
| 6-24 | docker pull 失敗 | 原文 + 三分類（網路／認證／不存在；另有「主機錯誤」：daemon 不可用、磁碟滿）；認證類：`<ref> 不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login <host>`；僅 add／bootstrap 追加 `離線可用：--local <tar>` | <sub>[base_pitfalls 2-9；remaining Q7；review I-37、I-38]</sub> |
| 6-25 | Renovate PR body（preset `prBodyNotes`） | 6-5 的指令 + `推 commit 後不要勾 rebase/retry` | <sub>[remaining Q5]</sub> |
| 6-26 | flock 逾時 | `專案目錄被鎖定（PID <pid>，自 <time>）；60 秒內未釋放。確認無其他 vendor_kit 在跑後重試，或設 VENDOR_KIT_NO_LOCK=1。`（結束 1）| <sub>[base_pitfalls 3-8]</sub> |
| 6-27 | 進度日誌恢復失敗 | `未恢復：<檔名>`（逐檔列出，結束 1）| <sub>[base_pitfalls 3-7]</sub> |
| 6-28 | 薄殼被改（install／upgrade vendor_kit） | `偵測到薄殼被修改：<files>。未重產任何薄殼。請先檢視下列差異；確認並手動還原（git checkout -- .vendor_kit/<file>）後，再執行 just vendor_kit upgrade vendor_kit。`（接差異，結束 1）| <sub>[review D2；grilling Q10、Q17]</sub> |
| 6-29 | upgrade 新增初始檔 dest 在 CI 路徑（`.github/workflows/`、`.gitlab-ci.yml`） | `注意：新版範本將建立或修改 CI 設定 <X>。請確認下列內容後再決定是否套用。` | <sub>[review D2；grilling Q14]</sub> |
| 6-30 | 啟動器驗 vk-resolve 失敗 | `引擎輸出不完整或不相容（<原因>），未執行任何動作。`（結束 1）| <sub>[review 三]</sub> |
| 6-31 | pull 逾時 | `拉取 <ref> 超過 <秒> 秒未完成，已中止。可用 --timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整。`（結束 1）| <sub>[grilling 19條-14]</sub> |
| 6-32 | 問句：prune | `要刪除以上 vendor_kit 資源嗎？` | <sub>[review A1]</sub> |
| 6-33 | 唯讀動詞偵測未完成交易 | `偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>`（sync／update 結束 1；help 不受影響；prune 只列出不刪）| <sub>[review 必修 9]</sub> |
| 6-34 | 問句：根 .dockerignore | `要在 .dockerignore 加這三行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.*` | <sub>[grilling Q22 補]</sub> |
| 6-35 | install 巢狀 | `<dir> 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。`（結束 1）| <sub>[grilling Q20]</sub> |
| 6-36 | 舊薄殼跑新 major 一般動詞 | `薄殼協定 <P_shell> 低於引擎 <vY> 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit`（結束 3、零寫入）| <sub>[grilling Q23]</sub> |

## 7. CI 契約

### 7.1 `.vendor_kit/ci/check.sh`（下游 CI 只呼叫它；GitHub／GitLab 一樣；平台無關）

第一行 shebang、第二行自描述、其後第一個動作 `export CI=1`。<sub>[review 必修 4]</sub>

| 步驟 | 內容 | 結束碼 |
|---|---|---|
| ⓪ | `git ls-files --error-unmatch .vendor_kit/version.local.toml` 命中 → 拒絕 | 1 |
| ① | `sync`（frozen） | 1：薄殼不符、未完成接入、baseline 落後、任何 local 覆寫；3 |
| ② | verify（印記 sha256，全部工具） | 1 |
| ③ | `upgrade --dry-run` | CI 且需改 tracked 檔 → 1 印清單（version.toml 不動）；仍有衝突標記 → 2；印 6-6～6-8 但不紅燈 |
| ④ | 工具測試 `just <repo> check`（每個 `[tools]` 工具、該 recipe 存在時；不存在則印「無」跳過；工具 check 不得再呼叫 check.sh） | 工具原碼傳出 |
| ⑤ | 專案測試（`just check` 若存在於根 justfile，否則跳過） | 依專案 |

一關過才下一關；全部通過 → 0。**check.sh 整體結束碼 = 第一個失敗步驟的碼**（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）。<sub>[proposal §7；v2.3 §7；review E1、I-44、I-45]</sub>

### 7.2 `check.sh --dist`（工具 repo CI）

驗：dist 佈局（files/、init.toml、just/<repo>.just 存在）、init.toml 合法（schema、`description` 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗）、以 just 1.33.0 解析每個 `<ns>.just`（並擋比 1.33 新的功能）、§3.6 `_sync` lint（`just --dump --dump-format json`）、`Dockerfile.dist` 含 `LABEL io.github.<org>.vendor_kit=1`、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性。<sub>[v2.1 E；#29；base_pitfalls 1-7、2-13；grilling Q21；review 必修 14、F1]</sub>

### 7.3 Renovate preset（放 vendor_kit repo 根目錄 `default.json`；vendor_kit 自身設定用 `renovate.json`；下游 `extends: ["github>ycpss91255-research/vendor_kit"]`）

regex manager 匹配 `**/.vendor_kit/version.toml`（monorepo 子專案亦命中；`(?m)` 多行，key regex 與 §4.1 正規行契約共用）+ docker datasource，同時擷取 `currentValue`（tag）與 `currentDigest`；PR 只改一行；major 分開 PR（`matchUpdateTypes`）；分組／排程範例；`hostRules` 依 host 不寫死 ghcr.io；`prBodyNotes` = 6-25；不設 `gitIgnoredAuthors`、不改 `rebaseWhen`；postUpgradeTasks 不採（文件附註）。流程：PR CI 以新版跑 §7.1 完整流程；需合併 → 1（6-5）→ 維護者在 PR 分支本機 `upgrade <repo> -y` → commit → push → CI 全部再跑 → 綠了才 merge。<sub>[grilling Q5、CI 平台定案、Q24 E2；remaining Q5；v2.1 E；review 必修 13、I-46]</sub>

### 7.4 驗收矩陣（每條一情境）

1. floor 以來每個已釋出 `bootstrap.sh(r)` + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 + 6-1、零 tracked 寫入）→ `upgrade vendor_kit`（1 + 6-2、薄殼重產）→ sync 0 → 工具 recipe → `upgrade` 全；**第二次 `upgrade vendor_kit` → 0 無變更**；禁止由候選樹複製 fixture、禁 stub 引擎。<sub>[grilling 相容性驗收 F；review I-27]</sub>
2. 每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境（docker 上界、just latest、arm64、WSL2）按世代覆蓋；成本上限當觸發討論條件。<sub>[grilling 相容性]</sub>
3. **升級後 == 全新安裝**：升級後 `.vendor_kit/` tracked 內容 == 用 C 全新 install + add（排除清單：時間戳、digest、`written_by`）。<sub>[grilling 19條-18]</sub>
4. 連續升級 r_i → r_j → C；固定 floor 直接跳升 C。<sub>[compat 矩陣]</sub>
5. 降版 `upgrade vendor_kit@<舊版>`：同 P／schema 成功；跨 schema 改檔前拒絕 3 + 6-10、零寫入。<sub>[grilling Q19、Q23]</sub>
6. `< floor` 太舊：唯一可用 synthetic fixture；任一動詞 → 3 + 6-18、零寫入；floor 檢查發生在任何上網之前（斷網也回 3）。<sub>[compat；grilling Q23]</sub>
7. 舊 bootstrap.sh 在已升級 repo 再跑：用 version.toml 指定引擎，不降版。<sub>[grilling Q18]</sub>
8. 舊引擎（`dev vendor_kit -i`）讀新檔：寫入前拒絕 3 + 6-19；不重產 tracked 薄殼。<sub>[grilling Q19、Q23]</sub>
9. 只改第一行後 `CI=true` sync（模擬 Renovate；驗 CI 真值規則）→ 1 列薄殼不符、零 tracked 寫入。<sub>[grilling 相容性補列；review 必修 4]</sub>
10. fresh clone 無 gen/：`just vendor_kit` 列出 **vendor_kit 命名空間**不觸網（工具命名空間在 sync 後才出現，`mod?` 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行。<sub>[interface 驗收；review I-15、I-19]</sub>
11. 使用者改薄殼／未納管檔／append 零／多命中：不覆蓋、不刪、詢問與結束碼符合契約。<sub>[grilling 相容性補列、Q13]</sub>
12. 中斷與重跑：resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗。<sub>[grilling 相容性；review 必修 9]</sub>
13. 歷史啟動器 parser × 合法／異常 TOML（BOM、空白、重複 `vendor_kit` 行 → 1、schema 位置、local 覆寫、尾端註解）。<sub>[grilling 相容性；review 必修 11]</sub>
14. just 矩陣 1.33.0 + latest（latest 非 required）。<sub>[grilling Q8]</sub>
15. amd64 與 arm64 原生 runner 各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致。<sub>[#26；review 必修 16]</sub>
16. 離線包（Q26）：無法連 GHCR 的機器用 `bootstrap.sh --local <tar>`（旁檔 `.digest`）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 `local_image_id`；旁檔缺 → 1；amd64／arm64 各一次。<sub>[#27；grilling Q26]</sub>
17. 離線可用（Q22／Q26）：本機已有 image 後斷網 → `just <ns> build`（自動 sync 快路徑）與 `just vendor_kit sync` 必須成功且不起 pull；斷網 + 無 image → 1 + 6-31 於 `--timeout 5` 內結束、不 hang。<sub>[grilling Q22、Q26]</sub>
18. 私有工具：`add <repo>@<tag>` 可拉；`add <repo>` 無 token → 1 + 6-3；`update` 無 token → 1 + 6-3 逐字；錯 token → 1；對 token → 列出；`TOKEN_FILE`（驗 `-v` 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token。<sub>[#28；review 必修 5]</sub>
19. append：LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 `.dockerignore` 三行 append → uninstall 刪。<sub>[#29；grilling Q22 補]</sub>
20. 空白路徑：專案根含空白與 `$`、`dev -p "含 空白/路徑"`；vk-resolve `mount` 八進位跳脫往返；`just vendor_kit add --help` 到引擎。<sub>[grilling 19條-8、Q24]</sub>
21. git worktree（`.git` 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）。<sub>[grilling 19條-1、-10]</sub>
22. rootless docker（setup-docker-action `rootless: true`：不加 `-u`、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：`--userns=keep-id`）各跑完整流程；uid 12345 無 passwd 項。<sub>[grilling 12 修正；review 必修 6]</sub>
23. prune：完整流程前後 `docker network ls`／`volume ls` 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊工具 image 刪、version.toml 引用的與 local 覆寫 tag 保留；`--dry-run` 零刪除；未恢復的 `.tmp.*` 不刪。<sub>[grilling 9 修正、9 補充]</sub>
24. 多工具彙總（Q27）：兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1。<sub>[grilling Q27]</sub>
25. F1 fixture（just 1.33.0）：cache 缺檔時 `just vendor_kit sync` 可進入（`mod?`）；`just <ns> build` 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 `_sync` 的模組。<sub>[review 五]</sub>
26. 無 tty／EOF：CI 無 `-y` 需詢問 → 1 + 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑。<sub>[grilling 19條-6；§0]</sub>
27. Renovate：實際 repo 驗證人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中。<sub>[remaining Q5；review I-46]</sub>
28. 驗收動詞集合由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅。<sub>[base_pitfalls 2-18、1-10]</sub>

## 8. 相容性契約條文（12 條）

1. **公開介面集合**：`vendor_kit` 命名空間內 recipe 名與 argv（§1.1 選項表）、結束碼 0/1/2/3、薄殼→引擎 docker run 呼叫方式（子命令、mount、使用者旗標規則、`-w /repo`、`--protocol` 位置、label 鍵）、`vk-resolve/<P>` 文法、§4 各檔格式、根 justfile 那一行、根 `.dockerignore` 三行、救援動詞名稱與 argv 皆列入契約；主機依賴不得新增（§3.1 白名單：docker ≥ 19.03、git、just ≥ 1.33.0、sh、grep、sed、id、mktemp、rm、sleep）。<sub>[compat 條 1；grilling Q8；review 必修 12]</sub>
2. **協定 P**：單一整數、與 release 版號分開；薄殼每次呼叫附 `--protocol P`（第一版起）；引擎接受 `[floor_P, current_P]` 並以呼叫方 P 回應；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1；引擎 image LABEL `….protocol=<floor_P>-<current_P>` 讓啟動器不起容器即可判 floor。<sub>[grilling Q16；review B5]</sub>
3. **floor**：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1）寫在契約，只能經 ADR 提高；低於 floor → 3 + 6-18、零寫入；floor 檢查先於任何上網。<sub>[grilling Q16、Q23]</sub>
4. **永久義務**：任何 ≥ floor 的舊薄殼可呼叫新引擎的救援路徑（§3.5）並得正確提示；舊資料永遠可讀、可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。<sub>[grilling Q16]</sub>
5. **非永久義務**：舊薄殼跑新 major 的一般動詞只保證乾淨回 **3** + 6-36 提示先 `upgrade vendor_kit`（零寫入）；同 major 內保留所有已承諾薄殼的一般呼叫能力。<sub>[grilling Q23；v2.4 §3]</sub>
6. **薄殼自描述**：§4.5 首行；未被改過以重算 hash + image 內模板（含歷史版本模板）二次比對判定，不依賴 gen/；不符 → 1 + 6-28 列差異不動。<sub>[grilling Q17；review I-16]</sub>
7. **檔案 schema**：每檔 `schema = N` + `written_by`（純資訊）；讀取門檻只看 schema；同 schema 只加不改；讀忽略未知欄位、寫保留（不能保留則拒絕）；schema 高於本引擎 → 任何寫入前退出 3 + 6-19；version.toml 契約 = 唯一正規行（§4.1；禁 BOM／重複鍵／表旁路）。<sub>[grilling 相容性其餘採納、Q23；review 必修 8、11、C1]</sub>
8. **新讀舊與遷移**：新引擎在記憶體轉換，只在本來要寫該檔的明確動作寫回；metadata 遷移由 `upgrade vendor_kit` 做並在 dry-run 明列；缺失且無法可靠還原的所有權資訊不得猜，停下報告。<sub>[grilling 相容性其餘採納；compat 條 6]</sub>
9. **讀先出貨、寫延後**：同 major 內 N-1 必能讀 N 寫的檔；tools.just 最後寫且與 cache 同一 apply 內原子替換；跨檔提交點與故障恢復由進度日誌定義（§4.3、§4.6）。<sub>[grilling 相容性其餘採納；review I-14]</sub>
10. **bootstrap.sh 與降版**：已有 version.toml → 用該行引擎跑 install，拉不到即失敗、不得退回內嵌；`upgrade vendor_kit@<舊版>` 只在目標引擎（以 P／schema 比）能無損讀現有檔時成功，否則改檔前拒絕 3 + 6-10；`dev vendor_kit -i <舊 image>` 禁止重產 tracked 薄殼。<sub>[grilling Q18、Q19、Q23]</sub>
11. **使用者檔與失敗恢復**：§0 不變量；`-y` 不授權覆蓋、不解除 frozen；結束碼 3 一律零寫入；遷移與升降版先做可行性檢查，失敗不留無法辨識的混合狀態；衝突（2）與自身升級要求重跑（1）是獨立狀態；唯讀動詞不自動恢復。<sub>[compat 條 10；v2.2 C；v2.5-1；grilling Q23；review 必修 9]</sub>
12. **發行與驗收**：已釋出 GHCR image（含 index 子 digest）、Release 資產（含 tar 與 `.digest` 旁檔）、fixture 永不刪；SemVer：major = 提高 floor 或需手動步驟；Renovate preset 建議 major 分開 PR；驗收 §7.4 條 1–13 缺任一不得出貨；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」。<sub>[grilling 相容性其餘採納、Q11、Q26；base_pitfalls 2-17]</sub>

## 9. [待定] 清單與已定值

### 9.1 仍待定（2 條）

| 編號 | 項目 | 建議值 | 為何仍待定 |
|---|---|---|---|
| B1 | `--local` 值如何判別 image tag 與 tar（bootstrap.sh、add） | 值含 `/` 或以 `.tar` 結尾 → 檔案路徑，必須存在否則 1；其餘視為 tag；兩邊都成立（tag 含 `/` 且存在同名檔）→ 1 提示用 `./` 或完整 ref 消歧（review 取捨）。替代：明確前綴 `image:`／`tar:`（codex） | review 明列「前綴語法要使用者拍板，因它改 proposal/#27 已用的介面」；grilling 仍留「待確認：`--image`／`--image-tar`」，Q25／Q26 未觸及 |
| F5 | Q22「每檔 sha256 verify 只在明確 `just vendor_kit sync`」如何與 F1「工具 `_sync` 逐字呼叫 `just vendor_kit sync`」區分 | `sync`（無參數）走快路徑；`sync <repo>` 與 frozen 一律起引擎 verify 該範圍；人要強制全驗用 `CI=1 just vendor_kit sync` | 兩條定案在 just 層無法區分「人打的」與「工具 recipe 自動呼叫的」同一指令；需使用者選：(a) 上述建議 (b) 在 `_sync` 本體加環境變數旗標 (c) 所有 sync 都走快路徑 |

### 9.2 已定值（本次填入；來源）

| 編號 | 值 | 來源 |
|---|---|---|
| A1 | `prune [-y] [--dry-run]`；兩段：`resolve prune` 出 `keep`，啟動器執行 docker ls／rm（不掛 socket）；image 只刪帶 label 且本專案未引用者；未恢復 `.tmp.*` 不刪；問句 6-32 | grilling Q24（prune 由啟動器執行）、9 修正／補充；review A1 |
| B2 | 轉發 `CI`、`VENDOR_KIT_NO_LOCK`、registry 三變數（resolve 階段；TOKEN_FILE 改 `-v`）；`PULL_TIMEOUT` 啟動器自讀；其餘不轉發 | review 必修 5、B2 |
| B3 | `VENDOR_KIT_PULL_TIMEOUT`／`--timeout`，預設 300，只收正整數 | grilling Q24、Q25；review B3 |
| B4 | vk-resolve/1：`\|` 分隔、八進位跳脫、kind 八種、`end\|<N>`、先收完再驗、整份掛 apply、引擎已變由 grep 第一行判 | grilling Q24；review 三 |
| B5 | 前綴 `io.github.<org>.vendor_kit`；容器等 `=1` + `.project`；引擎 image `=1`／`.protocol`／`.schema`；工具 image `=1`（Dockerfile.dist 必含） | grilling Q24、16 條；review B5、必修 14 |
| B6 | 專案內 `.vendor_kit/.tmp.dist.<id>/`（mktemp）+ trap | grilling Q24；review B6 |
| B7 | `-w /repo`；`--protocol P` 在子命令前 | review B7；grilling 16 條 |
| C1 | `written_by`（純資訊）；讀取門檻只看 `schema`；無 `min_reader` | grilling 16 條；review C1 |
| C2 | `vendor_kit_image_id` | review C2 |
| C3 | version.local.toml 與 version.toml 同形；工具在 `[tools]`；含 schema／written_by；undev vendor_kit 一併撤 ID | review C3 |
| C4 | metadata：`source`、`local_image_id`、`complete`、`conflicts`、`[[file]] dest/state/declined_hash/lines`、`[progress]`；state 單一列舉五值 | grilling Q24、16 條、Q26；review C4 |
| C5 | `.tmp.<verb>.<id>.toml`（交易 id，不用 repo） | grilling Q24；review C5 |
| C6 | 頂層 `description` 單行；`src` 相對 `dist/` | review C6 |
| D1 | 6-1 sync 用「請執行：just vendor_kit upgrade vendor_kit」；6-2 重產完成；6-2b 第一行已改但未重產；Q9 舊句不用 | review D1 |
| D2 | 6-16／17／18／19／23／28／29 採 codex 模板，6-19 改印「schema N 高於本引擎支援的 M」並回 3 | review D2、必修 8；grilling Q23 |
| E1 | check.sh = 第一個失敗步驟的碼；`export CI=1`；local 被 track → 1 | review E1、必修 4 |
| E2 | 根目錄 `default.json`；自身 `renovate.json`；extends 無路徑 | grilling Q24；review 必修 13 |
| F1 | `mod?` + 工具模組私有 `_sync`（逐字本體）+ 公開 recipe 相依 + --dist lint + vendor_kit 自身動詞不前置 + sync 豁免 6-9；1.33 fixture 驗證 | grilling 16 條；review 五 |
| F2 | undev vendor_kit 後只提示 6-1 不重寫 | grilling Q10；review F2 |
| F3 | submodule：契約先寫「已初始化且有工作樹的 submodule 可作專案根」，以 §7.4-21 實測通過為生效條件（非決策題） | review F3 |
| F4 | `just --dump --dump-format json` 取根檔既有 recipe／module／alias 名（不用 `--summary`） | review F4；v2.5-5 |

## 10. 變更紀錄（v1 → v2）

| # | 位置 | 改動 | 依據 |
|---|---|---|---|
| 1 | 導言 | 來源優先序補 review 最終建議、v2.4／v2.5、grilling Q22–Q27 與 16 條；矛盾處理移至 §11 | 任務指示；review 必修 7、I-01 |
| 2 | §0 專案根 | 第一次 install 候選專案根 = 呼叫目錄；巢狀檢查含下層 | review I-47 |
| 3 | §0 執行位置 | sync 豁免 6-9 | review 五（F1） |
| 4 | §0 主機需求 | 白名單指向 §3.1；Podman 納入 | review 必修 12；grilling 12 修正 |
| 5 | §0 不變量 | 例外加根 `.dockerignore` 三行 | grilling Q22 補 |
| 6 | §0 詢問通則 | EOF／Ctrl-C = 中止不記 declined；`-y` 不解除 frozen | review Claude 原文 12；v2.5-1、-4 |
| 7 | §0 frozen | CI 真值規則；升為失敗的明列集合；Q15 提醒不紅燈；update 不受 frozen 影響 | review 必修 4、I-02、Claude 原文 25 |
| 8 | §0 進度日誌 | 唯讀動詞只偵測提示（6-33）不恢復；undev／prune 也用 `.tmp.*` | review 必修 9；grilling Q24 |
| 9 | §0 新增 | 多工具彙總規則；結束碼 3 摘要 | grilling Q27、Q23 |
| 10 | §1 導言 | 不開清單加 `--tag`、`--purge`（開 issue）；`--repair` 併入 install | grilling Q25 |
| 11 | §1.1 新增 | 選項總表：短選項只有 -t/-y/-p/-i/-h；長形 --dry-run／--source／--local／--exit-code／--timeout／--no-justfile；版本 `<repo>@<tag>` | grilling Q25 |
| 12 | §1.2 bootstrap.sh | `-t/--tool <repo>[@<tag>]`；刪 `--tag`；`--timeout`；先 inspect 再 pull；`--local` 用 `.digest`；`local_bootstrap.sh` 併入；替代 docker run 指令加 `-w /repo --protocol P` | grilling Q25、Q26；review 必修 15、B7 |
| 13 | §1.2 install | 巢狀含下層；根 justfile 兩行 default；`.dockerignore` 三行 append；第一次／修復用薄殼首行 | review 必修 1；grilling Q22 補；v2.5-8 |
| 14 | §1.2 uninstall | 兩段＋重驗指紋；保護清單；`-n` → `--dry-run`；.dockerignore 對稱刪 | v2.5-10；review 必修 7；grilling Q25 |
| 15 | §1.2 add | `<repo>@<tag>`、`--source` 長形；repo 名限制；私有無憑證未指定版本 → 6-3；撞名預檢 (a)(b)(c)；`--local` 寫正式 digest + `local_image_id` | grilling Q25、Q26；v2.5-5；review I-35、F4 |
| 16 | §1.2 remove | `--dry-run`；兩段但不展開 image | grilling Q25；review Claude 原文 3 |
| 17 | §1.2 update | 不受 frozen；彙總 1 > 2 | review Claude 原文 25；grilling Q27 |
| 18 | §1.2 upgrade | `<repo>@<tag>`；不帶 repo 遇引擎新版只改第一行工具不升；新增 ns/dest 撞名預檢；N 讀自 /dist；二進位問後換；CI 需改 tracked → 1 與 -y 無關；`upgrade vendor_kit` 查 registry／第二次 0；降版以 P／schema 判 → 3；merge-file 執行錯誤 → 1；解析失敗 baseline 不推 | grilling Q25、Q23；v2.5-1、-2、-7；review 必修 6、10、一致「自身升級」、I-20、I-25、Claude 原文 29 |
| 19 | §1.2 dev | 拿掉 `--pull never` 改 inspect 驗 ID；「舊」以 LABEL P／schema 判；唯讀 symlink 說明 | review 必修 3、Claude 原文 35、I-42 |
| 20 | §1.2 undev | 兩段＋日誌；撤 image ID；最後覆寫撤掉刪檔；只提示不重寫 | v2.5-10；review F2、I-31 |
| 21 | §1.2 sync | 快路徑 `apply\|no`；6-33；tools.just 缺則重生 | grilling Q22；v2.5-9；review 必修 9 |
| 22 | §1.2 prune | 選項、兩段 keep、啟動器執行 docker、共享 image 範圍、未恢復 .tmp 不刪、問句 | grilling Q24、9 修正／補充；review A1、I-33、I-34 |
| 23 | §2 | 0 加 `upgrade vendor_kit` 無變更；1 明列「既定回 1 維持 1」；2 加解析失敗；3 全文改寫為 (a)–(e) + 零寫入 + P／schema 比 + floor 先於上網 | grilling Q23；review 最終建議四 |
| 24 | §3.1 | 主機命令白名單明列；引擎 ref 以正規行 regex 且命中恰 1；inspect 先於 pull；docker run 參數重寫（`-w /repo`、label、TOKEN_FILE `-v`、NO_LOCK、resolve 永不 -t、rootless 不加 -u、Podman keep-id）；暫存改專案內；兩段拆兩屬性；pull 失敗分類加主機錯誤、離線提示限 add；逾時 300 正整數 | review 必修 3、5、6、11、12、B2、B3、B6、B7、I-37、I-38；grilling Q24、Q26、12 修正 |
| 25 | §3.2 | 單段動詞集合改列；resolve 動詞集合含 remove／uninstall／prune；apply 讀 `/dist/vk-resolve`、argv 一致檢查 | v2.5-10；review 三 |
| 26 | §3.3 | 全文改寫：`\|` 分隔、八進位跳脫（`\0ooo`、printf %b）、八種 kind、驗證規則、指紋算法與覆蓋範圍、四個範例、apply stdout 非協定通道 | grilling Q24；review 三 |
| 27 | §3.4 新增 | 引擎已變由 grep 第一行前後判；第二次又變 → 1 + 6-2b | grilling Q24；review 必修 6 |
| 28 | §3.5 | 救援路徑清單明列（原 §3.4） | grilling Q16 |
| 29 | §3.6 新增 | F1 定案全文（`mod?`、`_sync` 逐字本體、相依、lint、例外、限制）＋ Q22 快路徑與前提 | grilling 16 條、Q22、Q22 補；review 五 |
| 30 | §4 通則 | 刪「未知 key → 1」改忽略＋保留；`written_by` 純資訊；schema 高 → 3 | review 必修 8、C1；grilling Q23 |
| 31 | §4.1 | 正規行唯一形＋POSIX BRE regex＋命中恰 1；`written_by` 欄位；第一行改稱慣例；範例更新 | review 必修 11、Claude 原文 27 |
| 32 | §4.2 | 同形；`vendor_kit_image_id`、schema、written_by；`[tools]`；撤除規則 | review C2、C3、I-31 |
| 33 | §4.3 | 欄位全部定名；單一 `state` 五值 + `declined_hash`；`local_image_id`；conflicts 含解析失敗；`[progress]`；.dockerignore 記錄位置；狀態機加問後換、deleted、不推 | grilling 16 條、Q24、Q26；review C4、必修 10、I-21、I-22、Claude 原文 29 |
| 34 | §4.4 | gen/.stamp 缺時用薄殼首行；刪 `image:<tag>`，`add --local` 寫正式 digest；tools.just `mod?` | review 必修 2、15、I-15；grilling Q26 |
| 35 | §4.5 | 薄殼 hash 精確定義；啟動器落點；根 justfile 逐字四行；根 .dockerignore 列 | review 必修 1、Claude 原文 13、28；grilling Q22 補 |
| 36 | §4.6 | `.tmp.<verb>.<id>.toml` 格式＋`.tmp.dist.<id>/` | grilling Q24；review C5 |
| 37 | §4.7 | Dockerfile.dist 三行含 LABEL；引擎 image 只驗 LABEL 一致；label 鍵全表；init.toml `description`／`src` 定案；hardlink／特殊檔；工具契約加 `_sync` 與 .dockerignore | review 必修 14、16、B5、C6、I-41；grilling Q22 |
| 38 | §4.8 新增 | 離線 `.digest` 旁檔與離線可用規則 | grilling Q26 |
| 39 | §5 | `PULL_TIMEOUT` 定案；CI 真值；TOKEN_FILE 掛載與互斥；白名單；刪 TMPDIR | grilling Q24、19條-14；review 必修 4、5、B2、B3、I-36 |
| 40 | §6 | 6-1／6-2 定稿、新增 6-2b；6-3 改 `<repo>@<tag>`；6-4／6-10／6-11／6-12／6-13／6-14／6-20／6-26 補成可複製指令；D2 七則逐字；6-19 改 schema N > M 回 3；6-24 加主機錯誤、離線提示限 add；新增 6-30～6-36 | review D1、D2、必修 8、I-37、I-38；grilling Q23、Q25 |
| 41 | §7.1 | 第二行自描述；`export CI=1`；⓪ local 被 track；④⑤ 發現方式與遞迴禁止；整體碼 = 第一個失敗步驟 | review E1、必修 4、I-44、I-45 |
| 42 | §7.2 | 加 `description` 單行、hardlink、`_sync` lint、LABEL 檢查 | review 必修 14、C6、F1 |
| 43 | §7.3 | 根目錄 `default.json`、自身 `renovate.json`、regex `**/.vendor_kit/version.toml` | grilling Q24；review 必修 13、I-46 |
| 44 | §7.4 | 1 第二次 0；5／6／8 回 3 零寫入；9 用 `CI=true`；10 只列 vendor_kit 命名空間；13 重複行；15 拆兩平台要求；16 改 `bootstrap.sh --local`＋`.digest`；新增 17 離線可用、24 多工具彙總、25 F1 fixture、26 無 tty；18 加 TOKEN_FILE；19 加 .dockerignore；20 八進位往返；22 rootless 細節；23 prune 細節 | grilling Q22、Q23、Q26、Q27；review 必修 4、15、16、I-15、I-19、I-27、五 |
| 45 | §8 | 1 加白名單／label／.dockerignore；2 加 LABEL protocol；3 加零寫入與 floor 先於上網；5 回 3；6 歷史模板；7 written_by／3；9 提交點；11 -y 不解除 frozen、3 零寫入、唯讀不恢復；12 加 `.digest` | grilling Q23、Q26；review 必修 8、9、11、12、B5、C1、I-14、I-16 |
| 46 | §9 | 22 條待定填 20 條（含 F3 改為實測條件）；新增 F5；剩 B1、F5 | grilling Q22–Q27、16 條；review 二～五 |
| 47 | §11 | 保留 v1 二十條矛盾處理，新增 21–27 | 本次 |

共 47 處。

## 11. 矛盾處理

| # | 衝突 | 取捨（依優先序） |
|---|---|---|
| 1 | 舊薄殼跑新 major 一般動詞：grilling Q16 回 1 vs Q19／Q23 回 3 | Q23 正式定案 → 回 3（§2、§8-5） |
| 2 | gen/.stamp 內容：v2.3 §3「引擎 ref + 薄殼各檔 hash」vs grilling Q17「只記引擎 ref」 | Q17 → 只記引擎 ref；hash 移到薄殼首行（§4.4、§4.5） |
| 3 | sync 發現薄殼不符：v2.1 A「本機可重寫」vs grilling Q10「只回 1 提示」 | Q10 → 只提示（§1 sync） |
| 4 | 薄殼被改：isolation「warn 再覆蓋」vs grilling Q10／Q17「1 列差異不動」 | grilling → 1 不動 |
| 5 | 衝突時 baseline：interface.md「不推」vs proposal §5／isolation「推到新版」 | proposal → 推到新版（§4.3）；解析失敗例外不推（review Claude 原文 29） |
| 6 | init.toml required／optional：remaining Q6 建議 vs grilling Q6 定案「不需要」 | grilling → 無此欄位 |
| 7 | uninstall：proposal §2「刪 .vendor_kit/ 全部」vs v2.2 E「不 rm -rf，只刪 hash 相符」 | v2.2 → 只刪自產（§1 uninstall） |
| 8 | 專案根：base_pitfalls 1-15／§6-4「$PWD == toplevel、一 repo 一個」vs grilling Q20 定案（改）monorepo 子專案 | grilling → 含 `.vendor_kit/` 的目錄（§0） |
| 9 | dist binary：base_pitfalls 3-5「check.sh --dist 拒絕 ELF」vs grilling Q21「vendor_kit 不檢查 binary」 | grilling → 不檢查（§7.2） |
| 10 | 自身升級訊息：grilling Q9「請再跑一次剛才的指令」vs Q10「提示 upgrade vendor_kit」vs v2.3 §2「請 commit 並再跑原指令」 | sync 路徑用 Q10（6-1）；`upgrade vendor_kit` 完成用 v2.3（6-2）；Q9 句不再用（review D1） |
| 11 | local 覆寫檔名：base_pitfalls 2-7「version.toml.local」vs grilling／proposal「version.local.toml」 | grilling → `version.local.toml` |
| 12 | bootstrap.sh 第二次跑：interface.md「拒絕 + 提示 add」vs grilling「再跑 = install 修復」＋ Q18 | grilling → 呼叫 install（用既有 version.toml 引擎） |
| 13 | 引擎覆寫記錄：proposal §2「只記 tag」vs v2.2 B「tag + image ID」 | v2.2 → 兩者（§4.2） |
| 14 | 進度日誌：v2.2 C「metadata 進度日誌」vs grilling「remove/uninstall 放 .tmp.*」 | grilling → add/upgrade 用 metadata、remove/uninstall/undev/prune 用 .tmp.*（§0） |
| 15 | Renovate 觸發：remaining「baseline 落後 CI 只警告不紅」vs grilling Q5「需合併 → 1 印指令」 | grilling → CI 下 1（§1 sync、§7.1） |
| 16 | pull 逾時：base_pitfalls §5「列 v2」vs grilling 19條-14「v1.0.0 必做」 | grilling → v1.0.0（§3.1、§5） |
| 17 | proxy：base_pitfalls §5「第一版要定 -e HTTP_PROXY」vs grilling 19條-2「issue v2」 | grilling → v2（§5） |
| 18 | rootless／Podman：base_pitfalls §5「明寫未驗證」vs grilling 12 修正「進驗收矩陣」 | grilling → 進矩陣（§7.4-22） |
| 19 | upgrade 的自身升級接手：v2.1 D vs v2.3 §2 | v2.3，且「引擎已變」改由啟動器 grep 判（Q24）（§1 upgrade、§3.4） |
| 20 | dry-run 範圍：v2.1 C「resolve 到此為止」vs v2.2 C「也要拉 image，apply --dry-run」 | v2.2（§3.1） |
| 21 | `--pull never`：v2.2 B／v2.3 §2／v2.5-7 vs docker 19.03 無此旗標 | review 必修 3 → `docker image inspect` 驗 ID（§3.1、§1 dev） |
| 22 | 版本旗標：proposal／#27／grilling Q11、Q19 的 `-t <tag>` vs Q25「版本一律 `<repo>@<tag>`、拿掉 --tag」 | Q25 較晚 → `<repo>@<tag>`；6-3、6-10 文字同步改 |
| 23 | vk-resolve 分隔符：review 取捨 TAB／路徑原樣 vs grilling Q24「`\|` 分隔（或 TAB）、八進位跳脫」 | grilling 勝 → `\|` + `\0ooo`（§3.3）；「或 TAB」不採以免兩種文法 |
| 24 | 暫存目錄：review B6 `${TMPDIR:-/tmp}` vs grilling Q24「專案內 `.vendor_kit/.tmp.dist.<id>/`」 | grilling 勝（§3.1） |
| 25 | C1：codex「written_by + min_reader 並存」vs review 取捨／grilling 16 條「純資訊 written_by」 | grilling → written_by（§4 通則） |
| 26 | E2：codex「`renovate/default.json` + `//renovate/default`」vs grilling Q24「根目錄 `default.json`」 | grilling（§7.3） |
| 27 | 拒絕記錄：v2.5-4「所有拒絕都記 declined」vs 16 條「單一 state + declined_hash」 | 16 條較晚 → 已納管檔拒絕只記 `declined_hash`、state 不變；新檔拒絕才 state=declined（§4.3） |

共 27 條。
