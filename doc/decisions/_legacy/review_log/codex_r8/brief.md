# 第八輪獨立審查 brief（codex）

你是獨立審查者。請依下列審查標準，對照附件「決策紀錄」（interface_spec.md）與附件 PNG（共 47 頁，依附加順序對應下列頁次）及 drawio XML，逐頁審查。

## 審查標準（使用者定的）
1. 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。
2. 顏色要有明確一致的意義，以各頁底部圖例為準；沒有的顏色不可出現。
3. 字要少，一般人（非工程師）也看得懂；專有名詞要在該頁底部「本頁名詞」表裡。
4. 線段：不穿無關方框、不交叉、不壓字、不裁切、不懸空、不該折的不折。
5. 線上文字 12pt。
6. 內容要跟 notes 的決策一致，且不可出現任何特定工具名（如 base）當實例，一律用 <repo>。
7. 每個方塊只放一件事（一個動作、一個判斷、一個檔案、一個最小單元）；一格裡有兩件事（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）就是問題，要拆成兩格。

## 本輪改動
第八輪：依第七輪 6 項必修＋5 項選修與 v2.9 澄清（--local tag 形不讀 .digest、前置檢查不分型別；add 私有無憑證分支、dest／撞名→橙；sync 版本變動那次全驗；upgrade B(2) 先解析再原子替換、解析失敗保留原檔；uninstall append 逐行比對；prune 進日誌走 apply；help 低於 floor 回 3；矩陣／目錄樹 install .tmp 欄；排版：離線包 o3t、bootstrap ae8n、dev 起點間距、t5 拆三格、update 迴圈、o10p/o10e 拆、be7 少折、be17 對齊、te14 頂點）。共 47 頁。

## 特別注意
對照 interface_spec.md 逐頁找：(1) 第七輪 6 項必修＋5 項選修是否修掉；(2) 頁間入口出口；(3) 每格一件事（只算真的兩個獨立動作）；(4) legend／名詞表。只回報真正的問題；已接受的設計不要再質疑。若某頁沒有問題請明說。最後給一句總評：這 47 頁能否交給使用者看（允許少量選修）。

## 要你回答的格式
逐頁列出 (A) 排版問題 (B) 顏色不符圖例 (C) 一般人看不懂的點與名詞表遺漏 (D) 與 notes 矛盾之處，每項給元件／線段 id（找不到 id 就寫元件上的文字）與一句說明，並標明是否必修（必須修才可交付）。最後一行明確寫「可以交付」或「還不行」。

## 附件 PNG 的頁次（依附加順序）
1. 契約 v2：不變量與角色
2. 契約 v2：動詞介面表
3. 契約 v2：規則、選項表、不開的動詞
4. 契約 v2：目錄樹與檔案範例
5. 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
6. 契約 v2：動詞 × 檔案矩陣
7. 契約 v2：工具 repo 契約③
8. 契約 v2：啟動器 ↔ 引擎契約④
9. 契約 v2：CI 契約⑤ 與驗收矩陣
10. 架構圖 v2
11. 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install
12. 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
13. 流程 v2：install（1）薄殼
14. 流程 v2：install（2）根 justfile 與 .dockerignore
15. 流程 v2：add（1）resolve → docker
16. 流程 v2：add（1′）apply 前置
17. 流程 v2：add（2）apply 寫入段
18. 流程 v2：sync（1）啟動器快路徑
19. 流程 v2：sync（1′）引擎 resolve
20. 流程 v2：sync（2）apply
21. 流程 v2：upgrade ── A. Renovate 路徑
22. 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
23. 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
24. 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
25. 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
26. 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退
27. 流程 v2：upgrade ── E. 自身升級 (a)(b)
28. 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
29. 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
30. 流程 v2：dev <repo>
31. 流程 v2：dev vendor_kit
32. 流程 v2：undev <repo>
33. 流程 v2：undev vendor_kit
34. 流程 v2：remove（1）resolve → apply 前置
35. 流程 v2：remove（2）寫入段
36. 流程 v2：uninstall（1）resolve → apply 前置
37. 流程 v2：uninstall（2）寫入段
38. 流程 v2：prune
39. 流程 v2：update
40. 狀態機 v2：初始檔五態
41. 狀態機 v2：交易與進度日誌
42. 相容性矩陣 v2
43. 結束碼決策表 v2
44. 流程 v2：vendor_kit release（1）build 與驗收
45. 流程 v2：vendor_kit release（2）推 image 與資產
46. 流程 v2：離線包（1）bootstrap.sh --local
47. 流程 v2：離線包（2）add --local 與斷網 sync


## 附件：決策紀錄（interface_spec.md 全文）

# vendor_kit 介面規格（interface reference）v2（2026-09-19；2026-09-20 併入 proposal_v2 v2.7 澄清，改動見 §10 #48–#57）

用途：後續每張票唯一可引用的 input／output 定義。前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）。

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
| 進度日誌 | add／upgrade 記 metadata `[progress]`；remove／uninstall／undev／prune 放 `.vendor_kit/.tmp.<verb>.<id>.toml`（§4.6）。可寫動詞（add／remove／upgrade／undev／uninstall／install）開始前偵測到未完成交易 → 先恢復再繼續，失敗明列 6-27；唯讀動詞（sync／update／help）只偵測並印 6-33 提示重跑原動詞，**不自動恢復**、不寫任何檔。prune 特例：遇活躍（未恢復）日誌只列出並印 6-33、不刪、**不視為未完成交易**（不擋 prune、不恢復；差集與 `apply prune` 照做）。<sub>[grilling 進度日誌條、Q24；v2.2 C；review 必修 9；v2.7-7]</sub> |
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
| `--local <image tag 或 tar>` | — | string | bootstrap.sh、add | 離線：tar 先 `docker load`；值的判別（B1 已定）：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立（tag 含 `/` 且存在同名檔）→ 1 + 6-37 消歧 <sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |
| `--verify` | — | bool | sync | 每檔 sha256 全驗（F5 已定；CI 為真時等同、不必加）<sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |
| `--exit-code` | — | bool | update | 有新版回 2 |
| `--timeout <秒>` | — | 正整數 | bootstrap.sh、add、upgrade、sync、undev | = `VENDOR_KIT_PULL_TIMEOUT`，由啟動器攔截、不轉發引擎；優先於環境變數 |
| `--no-justfile` | — | bool | install | 跳過根 justfile 步驟只印指示 |
| `--protocol P` | — | 整數 | 內部 | 薄殼→引擎全域旗標，不列 help |

版本一律寫在位置參數：`<repo>@<tag>`、`vendor_kit@<tag>`；`@<tag>` 比現版舊 → warn 仍執行。短選項只有 `-t`、`-y`、`-p`、`-i`、`-h`。<sub>[grilling Q25、19條-7]</sub>

### 1.2 動詞表

| 動詞 | 語法 | 位置參數 | 前置檢查 | 副作用（寫哪些檔，見 §4） | 詢問點（`-y`／無 tty） | 結束碼 | stdout／stderr 概要 |
|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag 或 tar>] [--timeout <秒>] [-h]` | 無 | 在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗、不得退回內嵌）；只有第一次接入才用內嵌引擎 ref；floor 檢查（§2）<sub>[grilling Q8、Q18；v2.4-5]</sub> | `docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref → 引擎 `install` → 每個 `-t` 呼叫 `add <repo>[@<tag>]`；`--local` 時 version.toml 仍寫正式 ref（tar 由同名 `.digest` 旁檔取得 index digest，§4.8）、version.local.toml 寫 `vendor_kit = "<tag>"` + `vendor_kit_image_id`，在 install 成功後才寫、失敗清除；不自刪。離線契約入口 = `bootstrap.sh --local <tar>`（值判別見 §1.1 B1）；離線包內另含 `local_bootstrap.sh` **便利包裝**（偵測 daemon 架構 `docker version --format '{{.Server.Arch}}'`、挑該平台 tar、`exec ./bootstrap.sh --local <tar> "$@"`），不是契約入口、不另定介面 <sub>[proposal §2；#27；grilling Q26；v2.5-8；review 必修 15；v2.7-1]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 | 0；1 失敗不留半成品（只對第一次 install 成立）；3 見 §2 <sub>[proposal §2；v2.2 C]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" -w /repo <引擎 ref> --protocol P install` <sub>[#27；review B7]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 + 6-17 <sub>[codex_verbs]</sub> | 在 git repo 內（否 → 1 + 6-16）；上層與下層皆無 `.vendor_kit/`（否 → 1 + 6-35）；不被 gen/.stamp 比對擋；第一次／修復判定用薄殼自描述首行（§4.5）：薄殼不存在 → 第一次；存在且 hash 相符 → 修復可重產；存在但不符 → 1 + 6-28 列差異不動 <sub>[proposal §2；grilling Q20、Q17；v2.5-8]</sub> | 建 `.vendor_kit/`：version.toml（含 schema、written_by）、entry.just、vendor.just、.gitignore、ci/check.sh、baseline/（空、不建 metadata）、gen/.stamp；根 justfile 無 → 建（§4.5 兩段式內容：import 一行 + `default:`／`\t@just --list` 兩行）；有 → 問後加一行；已含那行 → 不再加；根 `.dockerignore`：無 → 建（三行 `.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`）；有 → 問後 append（同 §4.3 append 規則；插入的行記於 `baseline/.vendor_kit.toml`，見 §4.3 註）；再跑 = 用引擎重寫薄殼（hash 相符才重寫）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1]</sub> | 根 justfile 已存在 → 6-20「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示；`.dockerignore` 已存在 → 6-34 <sub>[proposal §2；isolation A1(4)；grilling Q22 補]</sub> | 0／1／3 | 印建立或修改了什麼（含加進根 justfile 的那一行、加進 .dockerignore 的三行） |
| `uninstall` | `uninstall [-y] [--dry-run]` | 無 | resolve→apply 兩段、重驗指紋；先預檢全部工具（hash 相符的保護清單在任何 remove 之前生效；每個工具的 dev 覆寫 → 1 提示先 undev）；任一工具 remove 回 1 → 中止並列出已完成部分 <sub>[v2.2 E；v2.3 §6；v2.5-10；review 必修 7]</sub> | 逐工具 remove（保護模式）→ 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單；進度日誌 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2]</sub> | 根 justfile 那行：6-20「要刪這一行嗎」，只刪與我們寫的完全相同的行；根 `.dockerignore` 我們加的三行同 append 規則問後只刪原文相同的；append 行問後只刪原文相同的 <sub>[proposal §2、§5；grilling Q22 補]</sub> | 0／1／3 | 初始檔清單、保留檔清單 |
| `add <repo>[@<tag>]` | `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留） | 已接入且完成 → 0 無變更；`@<tag>` 與鎖定不同 → 1 提示 upgrade；私有 image 且無憑證又未指定 `@<tag>` → 1 + 6-3；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；`<ns>` 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（以 `just --dump --dump-format json` 取得）(c) 保留名 `vendor_kit` 撞名 → 1 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；v2.5-5；grilling Q3；review I-35、F4]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管 state=unmanaged 印 6-11）、baseline/<repo>/ + metadata（§4.3）、gen/tools.just 重生；version.toml 最後寫。`--local <tar>`：`docker load` 後由同名 `.digest` 旁檔取正式 index digest 寫 version.toml，metadata 記 `local_image_id` 供離線驗證 <sub>[proposal §2、§5；v2.1 C；v2.3 §3；grilling Q26]</sub> | `strategy="append"` 且檔已存在 → 6-21（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗）；3 | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [--dry-run]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；兩段（resolve→apply、重驗指紋）但不經 docker create/cp <sub>[proposal §2；v2.3 §5；review Claude 原文 3]</sub> | 刪 version.toml 該行、cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行；初始檔永不刪，印清單；進度日誌 `.tmp.remove.<id>.toml` <sub>[proposal §2；v2.1 E；grilling 進度日誌]</sub> | append 過的行 → 6-21 問後只刪原文相同的（CRLF/LF 等價）<sub>[proposal §5；grilling Q13]</sub> | 0／1／3 | 初始檔清單 |
| `update [<repo>]` | `update [<repo>] [--exit-code]` | `<repo>` 可省 = 全部含 vendor_kit | 只查 registry（`tags/list` 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 frozen 影響；單段、不經 docker create/cp；無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；不可同時宣稱「已是最新」 <sub>[proposal §2；grilling Q11、Q27；#28]</sub> | 無 | 無 | 0 已列出；1 查詢失敗（任一工具 1 → 整體 1，即使另有新版）；`--exit-code` 有新版 → 2；3 <sub>[proposal §2；v2.1 E；grilling Q27]</sub> | 末行固定 6-15 <sub>[proposal §2]</sub> |
| `upgrade [<repo>[@<tag>]]` | `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | `<repo>` 可省 = 全部含 vendor_kit 自身；`vendor_kit[@<tag>]` 為特殊值；`@<tag>` 限單一 repo | 順序：(0) metadata `conflicts` 非空且檔案仍含 `<<<<<<< vendor_kit:baseline` → 2 停（檔案失蹤不算已解）；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 `@<tag>`；frozen 不查）；無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新版新增 `<ns>`／dest 的全域撞名）再動任何東西；不帶 repo 且引擎有新版 → **本次只改第一行、工具不升** <sub>[v2.2 D；v2.1 B；v2.2 B；v2.5-6、-7；proposal §2；review I-20]</sub> | resolve → docker → apply：cache/、gen/<repo>.stamp、初始檔逐檔（§4.3 狀態機，N 讀自 `/dist/<repo>`）、baseline 推到新版（有衝突仍推；解析失敗不推）+ metadata、gen/tools.just；version.toml 最後寫。自身：(a) 不帶 repo 遇引擎新版 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器比對第一行前後（§3.4）→ 用新引擎跑 `upgrade vendor_kit`；(b) `upgrade vendor_kit[@<tag>]`（單段救援路徑）主流程，三種結果：前置 —— 薄殼被改（hash 不符自描述首行）→ 1 + 6-28 不動；(1) `@<tag>`／frozen 不查，否則查 registry；(2) 有新版？**是** → 改第一行 → 啟動器再以新 ref 跑一次 → 新引擎重產薄殼四檔 + gen/.stamp → **1 + 6-2**；**否** → 薄殼與現引擎相符？是 → **0 無變更**；否 → 用現引擎重產薄殼 → **1 + 6-2**；`@<舊版>` 降版：目標引擎（以其 image LABEL 的 P／schema 判）能無損讀現有檔才做（同 P／schema → 依上列 0／1），否則改檔前拒絕 **3 + 6-10** <sub>[v2.3 §2；v2.5-7；grilling Q19、Q23；review 必修 6、「自身升級第二次」一致；v2.7-5]</sub> | 逐檔 6-22：「X 換成新版？」／「你和新版都改了 X，要三方合併嗎？」／新增檔「要建 X 嗎」（拒絕 → state=declined + declined_hash）／二進位／symlink 未改 → 問後換、改過保留 + warn／append 行找到 → 問後替換、找不到 → 不動印新內容；`-y` 全免問；CI 且需改 tracked 檔 → 1 印清單（與 `-y` 無關）<sub>[proposal §5；grilling Q14、Q6；v2.5-1；review 必修 10]</sub> | 0；1 工具層不動 version.toml（自身升級已改第一行後回 1 是明列例外）；2 有衝突（留標記、印檔名、baseline 仍推到新版、解完重跑直到乾淨；`git merge-file` 衝突數映射為 2，其 I/O／執行錯誤 → 1）；3 <sub>[proposal §2；v2.3 §2；v2.2 D；grilling Q19、Q23；review I-25]</sub> | `--dry-run`：印會問哪些檔、6-6～6-8、metadata 遷移明列；dest 在 CI 路徑時 6-29 <sub>[grilling Q14、Q15]</sub> |
| `dev <repo>` | `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | `<repo>` 必填 | `-p`（工具必填）／`-i`（僅 `vendor_kit`，只能 tag 不能 digest）互斥；工具必須已在 version.toml（否 → 1）；`<dir>/dist/init.toml` 存在（缺 → 1）；CI 拒絕；單段、不經 docker create/cp；`-i` 的 image 以 LABEL P／schema 判定為「舊」時允許但禁止重產 tracked 薄殼（§2 (d)）<sub>[proposal §2；v2.2 B；v2.3 §5；grilling Q19；review Claude 原文 35]</sub> | 工具：version.local.toml `[tools].<repo> = "path:<dir>"`，cache/<repo>/ 改 symlink → `<dir>/dist`（唯讀性只在容器 mount 上成立），gen/<repo>.stamp 第一行 `path:<dir>`。自身：version.local.toml `vendor_kit = "<tag>"` + `vendor_kit_image_id`；之後啟動器用 `docker image inspect` 驗 ID、不 pull <sub>[proposal §2；v2.2 B；review 必修 3、I-42]</sub> | 無 | 0／1／3 | — |
| `undev <repo>` | `undev <repo>`／`undev vendor_kit` | `<repo>` 必填 | 未啟用 = 0 + 提示 | 兩段（`undev <repo>` 與 `undev vendor_kit` 皆走 resolve→apply）：apply 先建日誌 `.tmp.undev.<id>.toml`（記要撤的行，含 image ID）**才**撤 version.local.toml 該行（`undev vendor_kit` 把 `vendor_kit = "<tag>"` 與 `vendor_kit_image_id` 一起撤）；撤掉的是最後一個覆寫 → 刪除整個 version.local.toml；→ 重新 materialize 鎖定版（經 docker create/cp；`undev vendor_kit` 無 materialize）→ 最後刪日誌；失敗 → 1 保留可恢復狀態。`undev vendor_kit`：下次 just 用 version.toml 引擎，gen/.stamp（`<tag>`）≠ ref → 只提示 6-1、不重寫 <sub>[proposal §2；v2.2 B；v2.3 §5；v2.5-10；review F2、I-31]</sub> | 無 | 0／1／3 | — |
| `sync [<repo>]` | `sync [<repo>] [--verify]` | `<repo>` 可省 = 全部 | 每次工具 recipe 自動前置（§3.6）；快路徑（§3.6）；`--verify` 或 CI 為真 → 每檔 sha256 全驗（F5 已定）；引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；未完成交易 → 6-33 不恢復 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9]</sub> | 只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp。每工具順序：覆寫 path → 跳過 materialize/verify（仍查完成標記、baseline 落後）；cache 缺或印記第一行 ≠ 鎖定 digest → materialize；否則 verify sha256 → 失敗 → 重裝 + warn；tools.just 缺或需重生 → 重生。無待辦 → resolve 回 `apply|no` 快路徑 0（不起第二個容器）<sub>[v2.3 §4；v2.2 E；v2.5-9]</sub> | 無 | 0；1：薄殼不符、metadata 無完成標記（6-13）、CI 下 baseline 落後（6-5）、CI 下任何 local 覆寫；3 <sub>[proposal §2；v2.1 A]</sub> | 本機 baseline 落後 → warn 提示 upgrade |
| `prune` | `prune [-y] [--dry-run]` | 無 | 兩段：`resolve prune` 輸出 `keep` 清單（version.toml + version.local.toml 引用的全部 image）；啟動器 `docker {container,image,network,volume} ls --filter label=io.github.<org>.vendor_kit=1` 列出候選、扣掉 keep；image 只刪「帶 label 且本專案未引用」者（共享 daemon 上其他專案的引用不可知 → 文件明寫、`--dry-run` 先看）；活躍（未恢復）的 `.tmp.<verb>.<id>.toml` 不刪、只列出提示 6-33、不視為未完成交易（不擋 prune、不恢復）<sub>[grilling 9 修正、9 補充、Q24；review A1、I-33、I-34；v2.7-7]</sub> | 啟動器執行 docker rm／image rm／network rm／volume rm（不掛 docker socket）；`apply prune` 刪失效的 `.vendor_kit/.tmp.dist.*/` 與已完成交易殘留的 `.tmp.*` | 列出候選後 6-32「要刪除以上 vendor_kit 資源嗎？」（`-y` 免問） | 0／1／3 | 列出刪了什麼、保留什麼（含原因） |
| `help`／`h` | `help` | 無 | 不觸網、不安裝、不偵測交易以外的任何狀態 | 無 | 無 | 0 | 命名空間層說明；help 明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」<sub>[codex_verbs]</sub> |

## 2. 結束碼總表

| 碼 | 定義 | 動詞例外／特例 |
|---|---|---|
| 0 | 成功（含 warn）；`add` 已接入完成、`remove` 未接、`undev` 未啟用、`upgrade vendor_kit` 無新版且薄殼相符皆 0 + 提示 <sub>[proposal §2；review 一致]</sub> | — |
| 1 | 一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動 <sub>[proposal §2；compat 條 4]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）、自身升級完成要重跑——這些**既定回 1 的情境維持 1**，不因提示含 upgrade 而改 3 <sub>[v2.3 §2；grilling Q23]</sub> |
| 2 | 合併衝突（留 `<<<<<<< vendor_kit:baseline` 標記、印檔名、baseline 仍推到新版）<sub>[proposal §2；v2.2 D]</sub> | `update --exit-code` 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔 baseline 不推、記入 `conflicts` <sub>[v2.1 E；review Claude 原文 29]</sub> |
| 3 | 現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且**零寫入（無任何例外；救援路徑亦同）**：(a) 薄殼 P < 引擎 floor_P → 6-18；(b) 引擎讀到 schema > 支援上限 → 6-19；(c) `upgrade vendor_kit@<舊版>` 目標引擎 P／schema 低於現有檔 → 6-10；(d) `dev vendor_kit -i` 的引擎 P／schema 低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 提示先 `upgrade vendor_kit`。「舊」一律以 P／schema 比，不以 SemVer。網路／認證／不存在 → 1，不得偽裝成 3；floor 檢查在任何上網之前（啟動器可先 `docker image inspect` 引擎 LABEL 判 floor）<sub>[grilling Q19、Q23；review 最終建議四；contract 3]</sub> | — |

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
| 快路徑 | `sync`（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml `vendor_kit` ref；version.toml `[tools]` 每個 `<repo>` 的 ref 之 digest == gen/<repo>.stamp 第一行（或 local 覆寫的 `path:<dir>`）；gen/tools.just 存在；無 `.tmp.<verb>.*.toml`；非 frozen。全相符 → 不起容器、0；任一不符或 frozen → 起引擎 `resolve sync`。每檔 sha256 verify 只在：CI（frozen）、快路徑有差那次（版本變動）、以及 `sync --verify`（長形；F5 已定）做；`sync`（無參數，含工具 `_sync` 自動呼叫）一律快路徑 <sub>[grilling Q22、2026-09-19 末條；v2.7-2]</sub> |
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
| `[[file]]` | table array | 每個範本一筆 | `dest`（string，相對專案根）；`state`（string，單一列舉）∈ `managed`（已納管）／`appended`（append 已插入）／`declined`（新增檔被拒、從未納管）／`unmanaged`（本來就有、沒納管）／`deleted`（使用者刪了已納管檔，upgrade 維持刪除）；`declined_hash`（string，選填）= 最近一次被拒絕的那版範本 N 的 sha256。**declined 語意（v2.7-3）**：`state=declined` 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新（換版、三方合併、append 行替換、二進位換版）→ state 不變、只記 `declined_hash`（新版再變才再問）；add 時 `strategy=append` 檔已存在且拒絕 → `unmanaged`（只記 `declined_hash`）；新版 N 的 hash ≠ `declined_hash` → 再問一次，相同 → 不問但 6-6／6-8；`lines`（array of string，只在 appended）= 實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）<sub>[grilling Q13、Q14、Q15、16 條；review C4、I-21、I-22]</sub> |
| `[progress]` | table | 交易中 | `state = "in-progress"`、`started`（UTC ISO 8601）、`verb`、`id`、`done`／`pending`（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、唯讀動詞 6-33 <sub>[v2.2 C；v2.3 §6；v2.5-3]</sub> |

註：install 對根 `.dockerignore` 的三行 append 不屬任何工具，記於 `baseline/.vendor_kit.toml`（同 schema，只含 `[[file]]` dest=`.dockerignore` state=appended lines=三行），uninstall 讀它刪原文相同行。<sub>[grilling Q22 補；本規格為實作補齊]</sub>

upgrade 逐檔狀態機（B=baseline、D=磁碟、N=新版讀自 `/dist/<repo>`；只對 state=managed、無待解衝突）：D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 `git merge-file --diff3`（標籤 `<<<<<<< vendor_kit:baseline` 等），衝突 → 2；不論結果 baseline 推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → **問後換**、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 `conflicts`、baseline 不推。任何拒絕 → 記 `declined_hash`；只有「新檔從未建立」的拒絕才 state=declined，已納管檔拒絕 state 不變（v2.7-3）。<sub>[isolation C；proposal §5；v2.5-2、-4；review 必修 10；base_pitfalls 2-12；v2.7-3]</sub>

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
| `.tmp.<verb>.<id>.toml` | remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；`<id>` = 交易 id（UTC 時間戳 + 隨機，不用 `<repo>` 以免 uninstall 多工具撞名）；內容 = `schema`、`written_by`、`verb`、`id`、`targets`（array）、`started`、`done`／`pending`、`consents`（已取得的同意）；成功結束時刪；未完成 → 可寫動詞恢復、唯讀動詞 6-33；prune 遇未恢復者只列出（6-33）、不刪、不視為未完成交易（v2.7-7）；`undev`（含 `undev vendor_kit`）的日誌記要撤的覆寫行與 image ID <sub>[grilling 進度日誌、Q24；review C5、I-33；v2.7-6、-7]</sub> |
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

每個平台 tar（`docker save`）旁附同名 `.digest` 旁檔：`<name>.tar` + `<name>.tar.digest`，內容一行 `sha256:<hex64>` = 該 image 的正式多架構 index digest。`bootstrap.sh --local <tar>`／`add --local <tar>`：`docker load` 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 `local_image_id`；旁檔缺 → 1。離線包 `vendor_kit-vN-local.tar.gz` = bootstrap.sh + 各平台 tar + `.digest`，另附 `local_bootstrap.sh` 便利包裝（非契約，見 §1.2 bootstrap.sh）。離線可用：啟動器先 `docker image inspect`，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1「拉不到」不 hang（逾時）；離線 upgrade 不支援。<sub>[grilling Q26、19條-11]</sub>

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
| 6-33 | 唯讀動詞偵測未完成交易 | `偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>`（sync／update 結束 1；help 不受影響；prune 只列出不刪、不視為未完成交易）| <sub>[review 必修 9；v2.7-7]</sub> |
| 6-34 | 問句：根 .dockerignore | `要在 .dockerignore 加這三行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.*` | <sub>[grilling Q22 補]</sub> |
| 6-35 | install 巢狀 | `<dir> 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。`（結束 1）| <sub>[grilling Q20]</sub> |
| 6-36 | 舊薄殼跑新 major 一般動詞 | `薄殼協定 <P_shell> 低於引擎 <vY> 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit`（結束 3、零寫入）| <sub>[grilling Q23]</sub> |
| 6-37 | `--local` 值既是存在的檔案也像 image tag（B1 兩者皆成立） | `--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請寫 ./<v>，要指定 image 請寫完整 ref（<host>/<org>/<name>:<tag>）。`（結束 1、零寫入）| <sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |

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

### 9.1 仍待定（0 條）

無。B1、F5 已依 grilling 2026-09-19 末條定案（見 §9.2 B1、F5 與 §10 #49、#50）；圖上不再標「待拍板」。<sub>[v2.7-2]</sub>

### 9.2 已定值（本次填入；來源）

| 編號 | 值 | 來源 |
|---|---|---|
| A1 | `prune [-y] [--dry-run]`；兩段：`resolve prune` 出 `keep`，啟動器執行 docker ls／rm（不掛 socket）；image 只刪帶 label 且本專案未引用者；未恢復 `.tmp.*` 不刪；問句 6-32 | grilling Q24（prune 由啟動器執行）、9 修正／補充；review A1 |
| B1 | `--local` 值：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立 → 1 + 6-37 消歧；不加前綴語法 | grilling 2026-09-19 末條；v2.7-2 |
| F5 | `sync`（無參數，含工具 `_sync` 自動呼叫）= Q22 快路徑；`sync --verify`（長形）或 CI 為真 = 每檔 sha256 全驗 | grilling 2026-09-19 末條；v2.7-2 |
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
| 48 | §1.2 bootstrap.sh、§4.8 | 離線契約入口 = `bootstrap.sh --local <tar>`；離線包內含 `local_bootstrap.sh` 便利包裝（偵測架構、挑 tar、`exec ./bootstrap.sh --local`），非契約 | v2.7-1（2026-09-20） |
| 49 | §1.1 `--local`、§9 B1、§6 6-37 | B1 定案：含 `/` 或 `.tar` 結尾 → 路徑必須存在；其餘 tag；皆成立 → 1 + 6-37；§9.1 清空、移入 §9.2 | grilling 2026-09-19 末條；v2.7-2 |
| 50 | §1.1 `--verify`、§1.2 sync、§3.6、§9 F5 | F5 定案：`sync` 快路徑（含 `_sync` 自動呼叫）；`sync --verify` 或 CI 為真全驗 | grilling 2026-09-19 末條；v2.7-2 |
| 51 | §4.3 | declined 語意明寫：只用於新檔被拒從未建立；已納管拒絕 state 不變只記 `declined_hash`；add append 已存在且拒絕 → unmanaged | v2.7-3 |
| 52 | §2 結束碼 3 | 零寫入無任何例外（救援路徑亦同） | v2.7-4 |
| 53 | §1.2 upgrade (b) | `upgrade vendor_kit[@tag]` 主流程改寫為三種結果：有新版 → 改第一行重產 → 1；無新版且薄殼相符 → 0；無新版薄殼不符 → 重產 → 1；@舊版無法無損讀 → 3 | v2.7-5 |
| 54 | §1.2 undev、§4.6 | `undev vendor_kit` 走 resolve→apply，建 `.tmp.undev.<id>.toml`（含 image ID）後才撤覆寫；最後一個覆寫撤掉 → 刪整個 version.local.toml | v2.7-6 |
| 55 | §0 進度日誌、§1.2 prune、§4.6、§6 6-33 | prune 特例：活躍日誌只列出不刪、不視為未完成交易 | v2.7-7 |
| 56 | §6 | 新增 6-37（B1 消歧，逐字） | v2.7-2 |
| 57 | 導言 | 標題註明併入 v2.7；備份 `interface_spec.v2.md` | 本次 |

共 57 處。

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


## 附件：drawio XML（v2_only.drawio；因輸入長度上限，已去掉版面樣式與線段折點，只保留 id／value／顏色／非 12 的字級／source／target／vertex 的 geo=x,y,w,h；線上文字以 parent=線段 id 標示。版面問題請以 PNG 為準）

```xml
<mxfile>
<diagram id="v1p1" name="契約 v2：不變量與角色">
<mxCell id="title" value="契約① 使用者介面（1／3）── 目的、角色、不變量（interface_spec v2；&amp;lt;repo&amp;gt; = 工具 repo 名）" style="fontSize=18" geo="40,20,960,34"/>
<mxCell id="p1_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p1_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;本頁只有目的、角色、不變量與初始檔規則；動詞表在 p1b、選項／結束碼／規則在 p1c" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p1A" value="0. 目的與角色（契約只對兩個黃橢圓承諾）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,234"/>
<mxCell id="p1A_goal" value="目的（一句話）：工具 repo 把 dist/ 打包成 GHCR image；下游專案靠 bootstrap.sh + just vendor_kit add／upgrade／dev 拿到工具、跟上新版、在本機開發工具本身；其餘自動。&lt;br&gt;契約只對兩個黃橢圓承諾；我們（灰橢圓）不對自己承諾。" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1A" geo="20,50,740,106"/>
<mxCell id="p1A_r1" value="工具 repo 開發者（供應側）&lt;br&gt;照契約③ p3 出貨 dist 與 image" style="fillColor=#FFF4C3;strokeColor=#000000" parent="p1A" geo="790,50,240,106"/>
<mxCell id="p1A_r2" value="使用者（下游專案）&lt;br&gt;每天打 just 的人；用 p1b 的動詞" style="fillColor=#FFF4C3;strokeColor=#000000" parent="p1A" geo="1050,50,240,106"/>
<mxCell id="p1A_r3" value="vendor_kit 開發者（我們）&lt;br&gt;維護引擎與啟動器；不對自己承諾" style="fillColor=#CCCCCC;strokeColor=#000000" parent="p1A" geo="1310,50,230,106"/>
<mxCell id="p1A_tech" value="&lt;b&gt;技術路線 [定]&lt;/b&gt;：自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file（行內合併）；&lt;b&gt;第一版不放 vendir／Copier&lt;/b&gt;。依據：無單一工具全包四項（拉、鎖、初始檔、合併）；vendir 只省 docker 三行；Copier 要求範本是帶 tag 的 git repo" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1A" geo="20,168,1520,46"/>
<mxCell id="p1A_tech_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1A" geo="1508,170,30,20"/>
<mxCell id="p1B" value="1. 不變量（ADR；一列一主題，規則／條件／動作／結束碼分格）＋ 初始檔規則（§5；B = baseline、D = 磁碟上你的檔、N = 目標版範本 /dist/&amp;lt;repo&amp;gt;）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,350,1560,1123"/>
<mxCell id="p1B_inv" value="&lt;b&gt;1. 不變量（ADR）[定]：vendor_kit 對使用者的檔 ── 可以建（明說建了什麼）、要改先問（-y 免問）、永不刪、永不覆蓋。&lt;/b&gt;&lt;br&gt;「永不覆蓋」= 不用工具版本取代使用者客製內容；例外只有三處：根 justfile 一行、根 .dockerignore 三行、已納管初始檔經同意的換版／三方合併。never fail silently（結束碼 0／1／2／3）。" style="fillColor=#ffffff;strokeColor=#b85450" parent="p1B" geo="20,50,1520,48"/>
<mxCell id="p1B_inv_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="1508,52,30,20"/>
<mxCell id="p1B_t_h0" value="主題" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="20,114,170,30"/>
<mxCell id="p1B_t_h1" value="規則（一格一件事）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="190,114,430,30"/>
<mxCell id="p1B_t_h2" value="條件" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="620,114,300,30"/>
<mxCell id="p1B_t_h3" value="動作" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="920,114,340,30"/>
<mxCell id="p1B_t_h4" value="結束碼／訊息" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="1260,114,280,30"/>
<mxCell id="p1B_t_r0c0" value="&lt;b&gt;自動化（sync）只碰不進 git 的東西&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,144,170,57"/>
<mxCell id="p1B_t_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,146,30,20"/>
<mxCell id="p1B_t_r0c1_0" value="可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,144,430,26"/>
<mxCell id="p1B_t_r0c1_1" value="不碰使用者的檔、不寫薄殼四檔、不寫 gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,170,430,31"/>
<mxCell id="p1B_t_r0c2" value="引擎 ref ≠ gen/.stamp 第一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,144,300,57"/>
<mxCell id="p1B_t_r0c3" value="不重寫薄殼，只提示" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,144,340,57"/>
<mxCell id="p1B_t_r0c4" value="1 印 6-1「vendor_kit 已更新 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt;，請執行：just vendor_kit upgrade vendor_kit」" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,144,280,57"/>
<mxCell id="p1B_t_r1c0" value="&lt;b&gt;薄殼重產只由 install／upgrade vendor_kit 做&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,201,170,68"/>
<mxCell id="p1B_t_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,203,30,20"/>
<mxCell id="p1B_t_r1c1_0" value="薄殼四檔與 gen/.stamp 只由 install／upgrade vendor_kit 重產" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,201,430,26"/>
<mxCell id="p1B_t_r1c1_1" value="重產前先比對薄殼自描述首行（# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=…）：引擎重算 hash + 對 image 內模板二次比對" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,227,430,42"/>
<mxCell id="p1B_t_r1c2_0" value="首行 hash 相符" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,201,300,26"/>
<mxCell id="p1B_t_r1c2_1" value="首行 hash 不符（薄殼被改過）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,227,300,42"/>
<mxCell id="p1B_t_r1c3_0" value="重產" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,201,340,26"/>
<mxCell id="p1B_t_r1c3_1" value="不動任何薄殼、列出差異（使用者 git checkout 還原後再跑）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,227,340,42"/>
<mxCell id="p1B_t_r1c4_0" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,201,280,26"/>
<mxCell id="p1B_t_r1c4_1" value="1 印 6-28" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,227,280,42"/>
<mxCell id="p1B_t_r2c0" value="&lt;b&gt;CI 為真（frozen）與 -y 無關&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,269,170,83"/>
<mxCell id="p1B_t_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,271,30,20"/>
<mxCell id="p1B_t_r2c1_0" value="frozen = 不寫任何 tracked 檔、不查最新版" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,269,430,26"/>
<mxCell id="p1B_t_r2c1_1" value="仍拉鎖定版 image、仍寫 cache/、gen/" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,295,430,26"/>
<mxCell id="p1B_t_r2c1_2" value="-y 只在本機免詢問、不解除 frozen；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,321,430,31"/>
<mxCell id="p1B_t_r2c2_0" value="環境變數 CI 非空且不為 0／false（GitHub／GitLab 都設 CI=true；check.sh 自己 export CI=1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,269,300,57"/>
<mxCell id="p1B_t_r2c2_1" value="frozen 下需要寫 tracked 檔" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,326,300,26"/>
<mxCell id="p1B_t_r2c3_0" value="進 frozen" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,269,340,57"/>
<mxCell id="p1B_t_r2c3_1" value="不寫，印需改的檔清單（與 -y 無關）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,326,340,26"/>
<mxCell id="p1B_t_r2c4_0" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,269,280,57"/>
<mxCell id="p1B_t_r2c4_1" value="1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,326,280,26"/>
<mxCell id="p1B_t_r3c0" value="&lt;b&gt;「會碰使用者東西」只有三處&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,352,170,84"/>
<mxCell id="p1B_t_r3c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,354,30,20"/>
<mxCell id="p1B_t_r3c1_0" value="根 justfile 一行（問後加／刪）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,352,430,26"/>
<mxCell id="p1B_t_r3c1_1" value="根 .dockerignore 三行（問後 append／刪）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,378,430,26"/>
<mxCell id="p1B_t_r3c1_2" value="初始檔（init.toml 的 dest；含 strategy=append 經同意加的行）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,404,430,32"/>
<mxCell id="p1B_t_r3c2_0" value="使用者 .gitignore：工具以 strategy=append 宣告且你同意" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,352,300,42"/>
<mxCell id="p1B_t_r3c2_1" value="其餘：未宣告的使用者 .gitignore、.git/info/exclude、.git 本身" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,394,300,42"/>
<mxCell id="p1B_t_r3c3_0" value="才加行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,352,340,42"/>
<mxCell id="p1B_t_r3c3_1" value="不碰" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,394,340,42"/>
<mxCell id="p1B_t_r3c4_0" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,352,280,42"/>
<mxCell id="p1B_t_r3c4_1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,394,280,42"/>
<mxCell id="p1B_t_r4c0" value="&lt;b&gt;詢問通則&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,436,170,110"/>
<mxCell id="p1B_t_r4c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,438,30,20"/>
<mxCell id="p1B_t_r4c1_0" value="詢問一律有拒絕分支" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,436,430,26"/>
<mxCell id="p1B_t_r4c1_1" value="-y 只省略詢問：不授權覆蓋既有未納管檔、不硬加 append 行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,462,430,84"/>
<mxCell id="p1B_t_r4c2_0" value="明確回答「否」" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,436,300,42"/>
<mxCell id="p1B_t_r4c2_1" value="需詢問但無 tty／EOF 且無 -y" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,478,300,42"/>
<mxCell id="p1B_t_r4c2_2" value="EOF／Ctrl-C 中途中斷" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,520,300,26"/>
<mxCell id="p1B_t_r4c3_0" value="不寫；新檔（從未建立）→ state=declined；已納管檔 → state 不變、只記 declined_hash" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,436,340,42"/>
<mxCell id="p1B_t_r4c3_1" value="不寫" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,478,340,42"/>
<mxCell id="p1B_t_r4c3_2" value="中止整個 apply、不套用、不記 declined" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,520,340,26"/>
<mxCell id="p1B_t_r4c4_0" value="繼續（該檔略過）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,436,280,42"/>
<mxCell id="p1B_t_r4c4_1" value="1 印 6-4「需要確認但沒有終端可互動。請加 -y，或在終端執行。」" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,478,280,42"/>
<mxCell id="p1B_t_r4c4_2" value="1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,520,280,26"/>
<mxCell id="p1B_t_r5c0" value="&lt;b&gt;失敗恢復與零寫入&lt;/b&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,546,170,120"/>
<mxCell id="p1B_t_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="158,548,30,20"/>
<mxCell id="p1B_t_r5c1_0" value="所有合併在暫存完成 → 逐檔原子替換" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,546,430,26"/>
<mxCell id="p1B_t_r5c1_1" value="apply 進度日誌在第一個寫入前建立、最後一步刪除" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,572,430,26"/>
<mxCell id="p1B_t_r5c1_2" value="結束碼 3 一律零寫入（無例外）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,598,430,26"/>
<mxCell id="p1B_t_r5c1_3" value="「不留半成品」只對第一次 install 成立；衝突（2）與自身升級要求重跑（1）是獨立狀態" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="190,624,430,42"/>
<mxCell id="p1B_t_r5c2_0" value="寫入中途失敗" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,546,300,26"/>
<mxCell id="p1B_t_r5c2_1" value="下次可寫動詞遇到未完成日誌" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,572,300,26"/>
<mxCell id="p1B_t_r5c2_2" value="唯讀動詞（sync／update／help）遇到未完成日誌" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="620,598,300,68"/>
<mxCell id="p1B_t_r5c3_0" value="明列已完成／未完成" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,546,340,26"/>
<mxCell id="p1B_t_r5c3_1" value="先恢復再繼續" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,572,340,26"/>
<mxCell id="p1B_t_r5c3_2" value="不恢復，只提示" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="920,598,340,68"/>
<mxCell id="p1B_t_r5c4_0" value="1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,546,280,26"/>
<mxCell id="p1B_t_r5c4_1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,572,280,26"/>
<mxCell id="p1B_t_r5c4_2" value="1 印 6-33（help 不受影響）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1260,598,280,68"/>
<mxCell id="p1I_l" value="初始檔規則（同不變量；每列一種情況、一格一件事）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p1B" geo="20,682,900,28"/>
<mxCell id="p1I_h0" value="時機" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="20,714,150,30"/>
<mxCell id="p1I_h1" value="情況" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="170,714,360,30"/>
<mxCell id="p1I_h2" value="做法（逐字問句見 6-20～6-22）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="530,714,1010,30"/>
<mxCell id="p1I_r0c0" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,744,150,26"/>
<mxCell id="p1I_r0c1" value="檔不存在" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,744,360,26"/>
<mxCell id="p1I_r0c2" value="建（印出建了什麼）；state=managed" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,744,1010,26"/>
<mxCell id="p1I_r1c0" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,770,150,26"/>
<mxCell id="p1I_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="138,772,30,20"/>
<mxCell id="p1I_r1c1" value="檔已存在（strategy=copy）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,770,360,26"/>
<mxCell id="p1I_r1c2" value="不納管、不覆蓋（-y 也不覆蓋），印 6-11「&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對」；state=unmanaged" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,770,1010,26"/>
<mxCell id="p1I_r2c0" value="add（strategy=append）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,796,150,57"/>
<mxCell id="p1I_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="138,798,30,20"/>
<mxCell id="p1I_r2c1" value="檔已存在" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,796,360,57"/>
<mxCell id="p1I_r2c2" value="問 6-21「要在 &amp;lt;X&amp;gt; 加這幾行嗎」→ append，實際插入的行記在 metadata lines（原本就有的相同行不認領）；state=appended；重跑不重複；拒絕 → 不加行、不納管（state=unmanaged）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,796,1010,57"/>
<mxCell id="p1I_r3c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,853,150,26"/>
<mxCell id="p1I_r3c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="138,855,30,20"/>
<mxCell id="p1I_r3c1" value="D 缺（使用者刪了已納管檔）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,853,360,26"/>
<mxCell id="p1I_r3c2" value="state=deleted，維持刪除、不重建" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,853,1010,26"/>
<mxCell id="p1I_r4c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,879,150,26"/>
<mxCell id="p1I_r4c1" value="D==N 或 B==N（新版沒改／你的檔已等於新版）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,879,360,26"/>
<mxCell id="p1I_r4c2" value="不動" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,879,1010,26"/>
<mxCell id="p1I_r5c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,905,150,26"/>
<mxCell id="p1I_r5c1" value="D==B（新版改了、你沒改）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,905,360,26"/>
<mxCell id="p1I_r5c2" value="問 6-22「&amp;lt;X&amp;gt; 換成新版？」→ 換；拒絕 → state 仍 managed、只記 declined_hash（N 的 hash 變了才再問）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,905,1010,26"/>
<mxCell id="p1I_r6c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,931,150,42"/>
<mxCell id="p1I_r6c1" value="三者皆異（兩邊都改）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,931,360,42"/>
<mxCell id="p1I_r6c2" value="問 6-22「你和新版都改了 &amp;lt;X&amp;gt;，要三方合併嗎？」→ git merge-file --diff3；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline、回 2；baseline 仍推到新版（合併結果解析失敗 → 2 留原檔、baseline 不推、記 conflicts）；拒絕 → state 不變、只記 declined_hash" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,931,1010,42"/>
<mxCell id="p1I_r7c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,973,150,26"/>
<mxCell id="p1I_r7c1" value="N 缺（新版刪除該檔）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,973,360,26"/>
<mxCell id="p1I_r7c2" value="不刪，只 warn" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,973,1010,26"/>
<mxCell id="p1I_r8c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,999,150,26"/>
<mxCell id="p1I_r8c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="138,1001,30,20"/>
<mxCell id="p1I_r8c1" value="新版新增初始檔（Q14）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,999,360,26"/>
<mxCell id="p1I_r8c2" value="問 6-22「要建 &amp;lt;X&amp;gt; 嗎」（-y 建）；拒絕 → 從未建立，state=declined + declined_hash，之後不問；新版 N 的 hash 變了才再問；dest 在 CI 路徑時先印 6-29" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,999,1010,26"/>
<mxCell id="p1I_r9c0" value="upgrade（append）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1025,150,26"/>
<mxCell id="p1I_r9c1" value="找到上次加的行（原文相同；CRLF／LF 等價）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,1025,360,26"/>
<mxCell id="p1I_r9c2" value="問後替換；拒絕 → state 仍 appended、只記 declined_hash；零命中或多處命中 → 保留只 warn、印新內容" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,1025,1010,26"/>
<mxCell id="p1I_r10c0" value="upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1051,150,26"/>
<mxCell id="p1I_r10c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="138,1053,30,20"/>
<mxCell id="p1I_r10c1" value="二進位／symlink（不合併）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,1051,360,26"/>
<mxCell id="p1I_r10c2" value="你沒改 → 問 6-22「&amp;lt;X&amp;gt; 是二進位檔，要換成新版嗎？」後才換（拒絕 → state 不變、只記 declined_hash）；改過 → 保留 + warn" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,1051,1010,26"/>
<mxCell id="p1I_r11c0" value="remove／uninstall" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1077,150,26"/>
<mxCell id="p1I_r11c1" value="任何" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="170,1077,360,26"/>
<mxCell id="p1I_r11c2" value="永不刪初始檔，印清單；append 行問 6-21「要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎」後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="530,1077,1010,26"/>
<mxCell id="p1_lg0" value="黃橢圓：契約承諾的角色" style="fillColor=#FFF4C3;strokeColor=#000000" geo="40,1497,260,52"/>
<mxCell id="p1_lg1" value="灰橢圓：不承諾（我們）" style="fillColor=#CCCCCC;strokeColor=#000000" geo="320,1497,260,52"/>
<mxCell id="p1_lg2" value="白底紅粗框：不變量" style="fillColor=#ffffff;strokeColor=#b85450" geo="600,1503,160,40"/>
<mxCell id="p1_lg3" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="780,1503,190,40"/>
<mxCell id="p1_lg4" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="990,1503,110,40"/>
<mxCell id="p1_lgt" value="橢圓／方框顏色只在本頁有效&lt;br&gt;動詞表 p1b；選項、結束碼、規則 p1c；流程細節一律在流程頁" style="fillColor=none;strokeColor=none" geo="1120,1493,300,60"/>
<mxCell id="p1_lg5" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="40,1569,200,40"/>
<mxCell id="p1_lg6" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="260,1569,200,40"/>
<mxCell id="p1_lg6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="428,1571,30,20"/>
<mxCell id="p1_lg7" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="480,1569,220,40"/>
<mxCell id="p1_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1625,300,28"/>
<mxCell id="p1_tk0" value="&amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1659,150,40"/>
<mxCell id="p1_tv0" value="工具 repo 名（占位符）；.vendor_kit/cache/&amp;lt;repo&amp;gt;/ = 專案裡展開的工具檔；ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist = 它的 image；&amp;lt;ns&amp;gt; = 工具 just 模組的命名空間" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1659,610,40"/>
<mxCell id="p1_tk1" value="不變量（ADR）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1699,150,40"/>
<mxCell id="p1_tv1" value="整個專案最高優先的四句：可以建、要改先問、永不刪、永不覆蓋；記在 docs/adr/（短格式 ADR），每個決議都對照它；不另建 PRD.md" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1699,610,40"/>
<mxCell id="p1_tk2" value="ADR" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1739,150,40"/>
<mxCell id="p1_tv2" value="Architecture Decision Record：一份記錄「為什麼這樣決定」的短文件（docs/adr/）；破壞性變更、提高 floor 都要記一筆" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1739,610,40"/>
<mxCell id="p1_tk3" value="tracked 檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1779,150,40"/>
<mxCell id="p1_tv3" value="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1779,610,40"/>
<mxCell id="p1_tk4" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1819,150,55"/>
<mxCell id="p1_tv4" value="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1819,610,55"/>
<mxCell id="p1_tk5" value="CI／runner" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1874,150,40"/>
<mxCell id="p1_tv5" value="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1874,610,40"/>
<mxCell id="p1_tk6" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1914,150,55"/>
<mxCell id="p1_tv6" value="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1914,610,55"/>
<mxCell id="p1_tk7" value="sync" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1969,150,55"/>
<mxCell id="p1_tv7" value="每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1969,610,55"/>
<mxCell id="p1_tk8" value="薄殼自描述首行" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2024,150,55"/>
<mxCell id="p1_tv8" value="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2024,610,55"/>
<mxCell id="p1_tk9" value="strategy = &quot;append&quot;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2079,150,55"/>
<mxCell id="p1_tv9" value="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2079,610,55"/>
<mxCell id="p1_tk10" value="CRLF／LF" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2134,150,40"/>
<mxCell id="p1_tv10" value="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2134,610,40"/>
<mxCell id="p1_tk11" value="三方合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2174,150,40"/>
<mxCell id="p1_tv11" value="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2174,610,40"/>
<mxCell id="p1_tk12" value="baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1659,150,40"/>
<mxCell id="p1_tv12" value=".vendor_kit/baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1659,610,40"/>
<mxCell id="p1_tk13" value="N（目標版範本）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1699,150,40"/>
<mxCell id="p1_tv13" value="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&amp;lt;id&amp;gt;/、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（唯讀），不是 cache；cache/&amp;lt;repo&amp;gt;/ 在 apply 決定套用後才 materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1699,610,40"/>
<mxCell id="p1_tk14" value="初始檔五態（state）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1739,150,55"/>
<mxCell id="p1_tv14" value="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1739,610,55"/>
<mxCell id="p1_tk15" value="declined／declined_hash" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1794,150,55"/>
<mxCell id="p1_tv15" value="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1794,610,55"/>
<mxCell id="p1_tk16" value="conflicts（衝突中檔案）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1849,150,55"/>
<mxCell id="p1_tv16" value="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1849,610,55"/>
<mxCell id="p1_tk17" value="進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1904,150,71"/>
<mxCell id="p1_tv17" value="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1904,610,71"/>
<mxCell id="p1_tk18" value="tty／trap" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1975,150,40"/>
<mxCell id="p1_tv18" value="tty = 互動終端（能問問題）；沒有 tty（管線、CI）又需詢問且無 -y → 1 印 6-4；trap = shell 的收尾勾子，啟動器用它在中斷時清容器與 .tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1975,610,40"/>
<mxCell id="p1_tk19" value="根 .dockerignore 三行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2015,150,71"/>
<mxCell id="p1_tv19" value="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2015,610,71"/>
<mxCell id="p1_tk20" value="根 justfile 四行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2086,150,55"/>
<mxCell id="p1_tv20" value="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2086,610,55"/>
<mxCell id="p1_tk21" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2141,150,55"/>
<mxCell id="p1_tv21" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2141,610,55"/>
</diagram>
<diagram id="v1p1b" name="契約 v2：動詞介面表">
<mxCell id="title" value="契約① 使用者介面（2／3）── 動詞介面表（interface_spec §1.2；just vendor_kit &amp;lt;verb&amp;gt; [args]）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p1b_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p1b_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;選項總表（Q25）、結束碼、不開的動詞在 p1c；每個動詞的流程在流程頁 p5～" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p1B" value="2. 契約① 使用者介面：常用 3 + 進階 8 + 一次性 1 + help（綠底 常用、白底 進階、藍底 一次性；一列一動詞、「做什麼」欄一格一件事；6-N = interface_spec §6 訊息編號）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,1822"/>
<mxCell id="p1B_h0" value="動詞＋語法" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="20,50,220,30"/>
<mxCell id="p1B_h1" value="反向" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="240,50,84,30"/>
<mxCell id="p1B_h2" value="做什麼（一格一件事；細節見流程頁）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="324,50,980,30"/>
<mxCell id="p1B_h3" value="結束碼" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="1304,50,180,30"/>
<mxCell id="p1B_h4" value="組" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1B" geo="1484,50,56,30"/>
<mxCell id="p1B_r0c0" value="bootstrap.sh&lt;br&gt;sh bootstrap.sh [-t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]… [-y] [--local &amp;lt;image tag 或 tar&amp;gt;] [--timeout &amp;lt;秒&amp;gt;] [-h]" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="20,80,220,182"/>
<mxCell id="p1B_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,82,30,20"/>
<mxCell id="p1B_r0c1" value="uninstall（反向呼叫）" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="240,80,84,182"/>
<mxCell id="p1B_r0c2_0" value="前置：在 git repo 內（否 → 1 印 6-16）；just ≥ 1.33.0（不足 → 1 印 6-23）；floor 檢查；已有 version.toml → 用該行引擎（不用內嵌）" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,80,980,26"/>
<mxCell id="p1B_r0c2_1" value="docker image inspect 引擎 image：本機有 → 不 pull（離線可用）" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,106,980,26"/>
<mxCell id="p1B_r0c2_2" value="本機無 → docker pull 引擎 ref（逾時 → 1 印 6-31）；--local &amp;lt;tar&amp;gt;：改 docker load，再讀 .digest 旁檔" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,132,980,26"/>
<mxCell id="p1B_r0c2_3" value="呼叫引擎 install" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,158,980,26"/>
<mxCell id="p1B_r0c2_4" value="對每個 -t 呼叫 add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（轉發 -y；EOF 不算同意）" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,184,980,26"/>
<mxCell id="p1B_r0c2_5" value="--local：version.local.toml（vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id）在 install 成功後才寫、失敗清除；version.toml 仍寫正式 ref" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,210,980,26"/>
<mxCell id="p1B_r0c2_6" value="再跑一次 = 呼叫 install（冪等修復）；不自刪；離線包 = bootstrap.sh --local；取得：releases/latest/download/bootstrap.sh" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="324,236,980,26"/>
<mxCell id="p1B_r0c3" value="0；1 失敗不留半成品（只對第一次 install 成立）；3" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="1304,80,180,182"/>
<mxCell id="p1B_r0c4" value="一次性" style="fillColor=#dae8fc;strokeColor=#999999" parent="p1B" geo="1484,80,56,182"/>
<mxCell id="p1B_r1c0" value="install&lt;br&gt;install [-y] [--no-justfile]&lt;br&gt;install &amp;lt;repo&amp;gt; 誤用 → 1 印 6-17" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,262,220,146"/>
<mxCell id="p1B_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,264,30,20"/>
<mxCell id="p1B_r1c1" value="uninstall" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,262,84,146"/>
<mxCell id="p1B_r1c2_0" value="前置：在 git repo 內（否 → 1 印 6-16）；上層與下層皆無 .vendor_kit/（否 → 1 印 6-35）；不被 gen/.stamp 關卡擋" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,262,980,26"/>
<mxCell id="p1B_r1c2_1" value="第一次／修復判定用薄殼自描述首行：不存在 → 第一次；hash 相符 → 重產；不符 → 1 印 6-28 列差異不動" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,288,980,26"/>
<mxCell id="p1B_r1c2_2" value="建 .vendor_kit/：version.toml（schema、written_by）、薄殼四檔、baseline/.gitkeep（不建 metadata）、gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,314,980,26"/>
<mxCell id="p1B_r1c2_3" value="根 justfile：無 → 建逐字四行（import &#x27;.vendor_kit/entry.just&#x27;／空行／default:／\t@just --list）；有 → 問 6-20（-y 直接加）；已含 → 不再加；--no-justfile 只印指示" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,340,980,42"/>
<mxCell id="p1B_r1c2_4" value="根 .dockerignore：無 → 建三行（.vendor_kit/cache/、gen/、.tmp.*）；有 → 問 6-34 後 append，記於 baseline/.vendor_kit.toml；印建立或修改了什麼" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,382,980,26"/>
<mxCell id="p1B_r1c3" value="0／1／3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,262,180,146"/>
<mxCell id="p1B_r1c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,262,56,146"/>
<mxCell id="p1B_r2c0" value="uninstall&lt;br&gt;uninstall [-y] [--dry-run]" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,408,220,156"/>
<mxCell id="p1B_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,410,30,20"/>
<mxCell id="p1B_r2c1" value="install" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,408,84,156"/>
<mxCell id="p1B_r2c2_0" value="前置：預檢全部工具（有 dev 覆寫 → 1 提示先 undev）；hash 相符的保護清單在任何 remove 之前生效" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,408,980,26"/>
<mxCell id="p1B_r2c2_1" value="apply：拿鎖、重驗指紋 → 建日誌 .tmp.uninstall.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,434,980,26"/>
<mxCell id="p1B_r2c2_2" value="逐工具 remove（保護模式）：只刪自產（hash 相符）的檔；未知或被改的保留並回報；目錄非空則保留；不 rm -rf" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,460,980,26"/>
<mxCell id="p1B_r2c2_3" value="任一工具回 1 → 中止並列出已完成部分；初始檔一律保留並印清單" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,486,980,26"/>
<mxCell id="p1B_r2c2_4" value="根 justfile 那行：問 6-20「要從 justfile 刪這一行嗎」只刪完全相同的行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,512,980,26"/>
<mxCell id="p1B_r2c2_5" value="根 .dockerignore 三行與 append 行：問後只刪原文相同的 → 最後刪日誌" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,538,980,26"/>
<mxCell id="p1B_r2c3" value="0／1／3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,408,180,156"/>
<mxCell id="p1B_r2c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,408,56,156"/>
<mxCell id="p1B_r3c0" value="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]&lt;br&gt;add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] [--source &amp;lt;image&amp;gt;] [--local &amp;lt;tar&amp;gt;] [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]&lt;br&gt;&amp;lt;repo&amp;gt;：[A-Za-z0-9_][A-Za-z0-9_.-]*、不得為 vendor_kit" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="20,564,220,182"/>
<mxCell id="p1B_r3c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,566,30,20"/>
<mxCell id="p1B_r3c1" value="remove" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="240,564,84,182"/>
<mxCell id="p1B_r3c2_0" value="前置：已接入且完成 → 0 無變更；@&amp;lt;tag&amp;gt; 與鎖定不同 → 1 提示 upgrade；私有 image 無憑證又未指定 @&amp;lt;tag&amp;gt; → 1 印 6-3；dest 撞名／越界 → 拒絕" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,564,980,26"/>
<mxCell id="p1B_r3c2_1" value="前置：&amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（just --dump）(c) 保留名 vendor_kit 撞名 → 1 拒絕" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,590,980,26"/>
<mxCell id="p1B_r3c2_2" value="resolve → 主機 docker 展開到 .tmp.dist.&amp;lt;id&amp;gt;/&amp;lt;repo&amp;gt;/ → apply：拿鎖、重驗指紋、建日誌（metadata [progress]）；逐檔讀 /dist" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,616,980,26"/>
<mxCell id="p1B_r3c2_3" value="初始檔：無 → 建；有 → 不納管（unmanaged，印 6-11；-y 也不覆蓋）；strategy=&quot;append&quot; 且已存在 → 問 6-21（-y 免問，印出加了什麼）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,642,980,26"/>
<mxCell id="p1B_r3c2_4" value="收尾①：materialize → cache/&amp;lt;repo&amp;gt;/ + gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,668,980,26"/>
<mxCell id="p1B_r3c2_5" value="收尾②：baseline/&amp;lt;repo&amp;gt;/ + metadata（complete=true；--local &amp;lt;tar&amp;gt;：.digest 旁檔取正式 index digest、記 local_image_id）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,694,980,26"/>
<mxCell id="p1B_r3c2_6" value="收尾③：gen/tools.just 重生 → version.toml 最後寫 → 刪日誌" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,720,980,26"/>
<mxCell id="p1B_r3c3" value="0；1（version.toml 一律未動：dest 不合法、CI 為真需改 tracked、指紋不同、失敗）；3" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1304,564,180,182"/>
<mxCell id="p1B_r3c4" value="常用" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1484,564,56,182"/>
<mxCell id="p1B_r4c0" value="remove &amp;lt;repo&amp;gt;&lt;br&gt;remove &amp;lt;repo&amp;gt; [-y] [--dry-run]&lt;br&gt;裸跑 → 用法 + 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,746,220,78"/>
<mxCell id="p1B_r4c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,748,30,20"/>
<mxCell id="p1B_r4c1" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,746,84,78"/>
<mxCell id="p1B_r4c2_0" value="前置：有 dev 覆寫 → 1 提示先 undev；未接 = 0 + 提示；兩段（resolve → apply、重驗指紋）但不經 docker create/cp" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,746,980,26"/>
<mxCell id="p1B_r4c2_1" value="建日誌 .tmp.remove.&amp;lt;id&amp;gt;.toml 後刪：version.toml 該行、cache/&amp;lt;repo&amp;gt;/、baseline/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just 該工具所有 mod? 行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,772,980,26"/>
<mxCell id="p1B_r4c2_2" value="初始檔永不刪，印清單；append 過的行 → 問 6-21「要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎」只刪原文相同的（CRLF/LF 等價）→ 刪日誌" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,798,980,26"/>
<mxCell id="p1B_r4c3" value="0／1／3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,746,180,78"/>
<mxCell id="p1B_r4c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,746,56,78"/>
<mxCell id="p1B_r5c0" value="update [&amp;lt;repo&amp;gt;]&lt;br&gt;update [&amp;lt;repo&amp;gt;] [--exit-code]&lt;br&gt;&amp;lt;repo&amp;gt; 可省 = 全部含 vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,824,220,88"/>
<mxCell id="p1B_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,826,30,20"/>
<mxCell id="p1B_r5c1" value="（upgrade 的前一步）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,824,84,88"/>
<mxCell id="p1B_r5c2_0" value="只查 registry（tags/list 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 frozen 影響；單段、不經 docker create/cp" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,824,980,26"/>
<mxCell id="p1B_r5c2_1" value="無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；末行固定 6-15「套用：just vendor_kit upgrade」" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,850,980,62"/>
<mxCell id="p1B_r5c3" value="0 已列出；1 查詢失敗（任一工具 1 → 整體 1）；--exit-code 有新版 → 2；3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,824,180,88"/>
<mxCell id="p1B_r5c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,824,56,88"/>
<mxCell id="p1B_r6c0" value="upgrade &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（工具）&lt;br&gt;upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]] [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]&lt;br&gt;@&amp;lt;tag&amp;gt; 限單一 repo；比現版舊 → warn 仍執行" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="20,912,220,188"/>
<mxCell id="p1B_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,914,30,20"/>
<mxCell id="p1B_r6c1" value="git revert 整組 commit" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="240,912,84,188"/>
<mxCell id="p1B_r6c2_0" value="前置：無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新增 &amp;lt;ns&amp;gt;／dest 撞名）再動任何東西" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,912,980,26"/>
<mxCell id="p1B_r6c2_1" value="(0) conflicts 非空且檔案仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 @&amp;lt;tag&amp;gt;；frozen 不查）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,938,980,42"/>
<mxCell id="p1B_r6c2_2" value="resolve → 主機 docker → apply（拿鎖、重驗、建日誌）→ 逐檔狀態機（p1 表；N 讀自 /dist/&amp;lt;repo&amp;gt;）問 6-22；拒絕 → 已納管檔 state 不變只記 declined_hash、新檔 state=declined；CI 為真且需改 tracked 檔 → 1 印清單（與 -y 無關）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,980,980,42"/>
<mxCell id="p1B_r6c2_3" value="baseline 推到新版（有衝突仍推；解析失敗不推）+ metadata" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1022,980,26"/>
<mxCell id="p1B_r6c2_4" value="materialize cache/、gen/&amp;lt;repo&amp;gt;.stamp；gen/tools.just 重生" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1048,980,26"/>
<mxCell id="p1B_r6c2_5" value="version.toml 最後寫 → 刪日誌；--dry-run：只印會問哪些檔與 6-6～6-8、不寫" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1074,980,26"/>
<mxCell id="p1B_r6c3" value="0；1 工具層不動 version.toml；2 有衝突（留標記、印檔名、baseline 仍推；解完重跑；merge-file I/O 錯誤 → 1）；3" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1304,912,180,188"/>
<mxCell id="p1B_r6c4" value="常用" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1484,912,56,188"/>
<mxCell id="p1B_r7c0" value="upgrade（不帶 repo：全部含自身）&lt;br&gt;upgrade [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="20,1100,220,126"/>
<mxCell id="p1B_r7c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1102,30,20"/>
<mxCell id="p1B_r7c1" value="git revert 整組 commit" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="240,1100,84,126"/>
<mxCell id="p1B_r7c2_0" value="resolve 先判斷「引擎有新版？」：否 → 只升全部工具（同上列；Q27 彙總）；是 → 本次只改第一行、工具不升：舊引擎 apply（拿鎖、重驗、建日誌）只改 vendor_kit 正規行" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1100,980,42"/>
<mxCell id="p1B_r7c2_1" value="啟動器 apply 前後各 grep 一次正規行：ref 變了 → local 覆寫有 vendor_kit= 則 docker image inspect 驗 ID 用該 image，否則 docker pull 新 ref → 用新引擎跑 upgrade vendor_kit（下一列）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1142,980,42"/>
<mxCell id="p1B_r7c2_2" value="第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b「引擎版本已鎖定為 &amp;lt;vY&amp;gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」，不再重跑" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1184,980,42"/>
<mxCell id="p1B_r7c3" value="1 印 6-2「已升級引擎 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」（已改第一行後回 1 是明列例外）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1304,1100,180,126"/>
<mxCell id="p1B_r7c4" value="常用" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1484,1100,56,126"/>
<mxCell id="p1B_r8c0" value="upgrade vendor_kit[@&amp;lt;tag&amp;gt;]&lt;br&gt;upgrade vendor_kit[@&amp;lt;tag&amp;gt;] [-y]&lt;br&gt;單段救援路徑（不依賴 resolve/apply 與 gen/）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="20,1226,220,104"/>
<mxCell id="p1B_r8c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1228,30,20"/>
<mxCell id="p1B_r8c1" value="git revert 整組 commit" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="240,1226,84,104"/>
<mxCell id="p1B_r8c2_0" value="啟動器讀正規行（local 覆寫優先：docker image inspect 驗 vendor_kit_image_id、不 pull）→ 該引擎跑；不被 gen/.stamp 關卡擋" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1226,980,26"/>
<mxCell id="p1B_r8c2_1" value="查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版且薄殼首行 hash 相符 → 改第一行 → 啟動器再以新 ref 跑一次 → 新引擎重產薄殼四檔 + gen/.stamp → 1 印 6-2；無新版且相符 → 0；只重產薄殼 → 1 印 6-2；被改 → 1 印 6-28" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1252,980,42"/>
<mxCell id="p1B_r8c2_2" value="@&amp;lt;舊版&amp;gt; 降版：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（要退回請 git revert）" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1294,980,36"/>
<mxCell id="p1B_r8c3" value="0 無變更；1 印 6-2；3 印 6-10" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1304,1226,180,104"/>
<mxCell id="p1B_r8c4" value="常用" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1484,1226,56,104"/>
<mxCell id="p1B_r9c0" value="dev &amp;lt;repo&amp;gt;&lt;br&gt;dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;／dev vendor_kit -i &amp;lt;tag&amp;gt;&lt;br&gt;-p（工具必填）與 -i（僅 vendor_kit，只能 tag）互斥" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="20,1330,220,110"/>
<mxCell id="p1B_r9c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1332,30,20"/>
<mxCell id="p1B_r9c1" value="undev" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="240,1330,84,110"/>
<mxCell id="p1B_r9c2_0" value="前置：工具必須已在 version.toml（否 → 1）；&amp;lt;dir&amp;gt;/dist/init.toml 存在（缺 → 1）；CI 為真 → 拒絕；單段、不經 docker create/cp" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1330,980,26"/>
<mxCell id="p1B_r9c2_1" value="工具：version.local.toml [tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；cache/&amp;lt;repo&amp;gt;/ 改 symlink → &amp;lt;dir&amp;gt;/dist；gen/&amp;lt;repo&amp;gt;.stamp 第一行 path:&amp;lt;dir&amp;gt;；之後啟動器掛 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro，sync 跳過 materialize／verify" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1356,980,42"/>
<mxCell id="p1B_r9c2_2" value="自身：version.local.toml vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；之後啟動器每次 docker image inspect 驗 ID、不 pull；-i 的 image 以 LABEL P／schema 判為「舊」→ 允許但禁止重產 tracked 薄殼" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="324,1398,980,42"/>
<mxCell id="p1B_r9c3" value="0／1／3" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1304,1330,180,110"/>
<mxCell id="p1B_r9c4" value="常用" style="fillColor=#d5e8d4;strokeColor=#999999" parent="p1B" geo="1484,1330,56,110"/>
<mxCell id="p1B_r10c0" value="undev &amp;lt;repo&amp;gt;&lt;br&gt;undev &amp;lt;repo&amp;gt;／undev vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1440,220,84"/>
<mxCell id="p1B_r10c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1442,30,20"/>
<mxCell id="p1B_r10c1" value="dev" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,1440,84,84"/>
<mxCell id="p1B_r10c2_0" value="未啟用 = 0 + 提示；兩段：建日誌 .tmp.undev.&amp;lt;id&amp;gt;.toml → 撤 version.local.toml 該行（undev vendor_kit 一併撤 vendor_kit_image_id；最後一個覆寫撤掉後刪整個檔）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1440,980,42"/>
<mxCell id="p1B_r10c2_1" value="工具：重新 materialize 鎖定版（經 docker create/cp）；失敗 → 1 保留可恢復狀態。undev vendor_kit：下次 just 用 version.toml 引擎；gen/.stamp ≠ ref → 只提示 6-1、不重寫" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1482,980,42"/>
<mxCell id="p1B_r10c3" value="0／1／3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,1440,180,84"/>
<mxCell id="p1B_r10c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,1440,56,84"/>
<mxCell id="p1B_r11c0" value="sync [&amp;lt;repo&amp;gt;]&lt;br&gt;sync [&amp;lt;repo&amp;gt;]／sync --verify&lt;br&gt;&amp;lt;repo&amp;gt; 可省 = 全部；--verify = 每檔 sha256 全驗" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1524,220,152"/>
<mxCell id="p1B_r11c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1526,30,20"/>
<mxCell id="p1B_r11c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,1524,84,152"/>
<mxCell id="p1B_r11c2_0" value="每次工具 recipe 自動前置（_sync）；快路徑（無參數）：啟動器只用 grep 比 gen/*.stamp 第一行 vs version.toml、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1524,980,42"/>
<mxCell id="p1B_r11c2_1" value="引擎 ref ≠ gen/.stamp 第一行 → 1 印 6-1 不重寫（install／upgrade vendor_kit 跳過此關）；未完成交易 → 1 印 6-33 不恢復；CI 為真下任何 local 覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1566,980,42"/>
<mxCell id="p1B_r11c2_2" value="只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp。每工具：覆寫 path → 跳過（仍查完成標記、落後）；cache 缺或印記 ≠ 鎖定 digest → materialize；否則 verify（--verify／CI 為真／版本變動時）→ 失敗 → 重裝 + warn；tools.just 缺 → 重生" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1608,980,42"/>
<mxCell id="p1B_r11c2_3" value="無待辦 → resolve 回 apply|no 快路徑 0（不起第二個容器）；baseline 落後：本機 warn 提示 upgrade、CI 為真 → 1 印 6-5" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1650,980,26"/>
<mxCell id="p1B_r11c3" value="0；1：薄殼不符、無完成標記（6-13）、CI 為真下 baseline 落後（6-5）或任何 local 覆寫；3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,1524,180,152"/>
<mxCell id="p1B_r11c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,1524,56,152"/>
<mxCell id="p1B_r12c0" value="prune&lt;br&gt;prune [-y] [--dry-run]" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1676,220,84"/>
<mxCell id="p1B_r12c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1B" geo="208,1678,30,20"/>
<mxCell id="p1B_r12c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,1676,84,84"/>
<mxCell id="p1B_r12c2_0" value="兩段：resolve prune 輸出 keep 清單（version.toml + version.local.toml 引用的全部 image）→ 啟動器 docker {container,image,network,volume} ls --filter label=io.github.&amp;lt;org&amp;gt;.vendor_kit=1 列候選、扣掉 keep" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1676,980,42"/>
<mxCell id="p1B_r12c2_1" value="問 6-32「要刪除以上 vendor_kit 資源嗎？」（-y 免問）→ docker rm／image rm／network rm／volume rm；image 只刪「帶 label 且本專案未引用」者（--dry-run 先看）；活躍的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml 不刪、列出提示 6-33；apply prune 刪失效的 .tmp.dist.*" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1718,980,42"/>
<mxCell id="p1B_r12c3" value="0／1／3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,1676,180,84"/>
<mxCell id="p1B_r12c4" value="進階" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,1676,56,84"/>
<mxCell id="p1B_r13c0" value="help／h&lt;br&gt;help" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="20,1760,220,42"/>
<mxCell id="p1B_r13c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="240,1760,84,42"/>
<mxCell id="p1B_r13c2" value="命名空間層說明（just 做不到 just vendor_kit --help）；各動詞 --help 由引擎印；不觸網、不安裝；明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="324,1760,980,42"/>
<mxCell id="p1B_r13c3" value="0" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1304,1760,180,42"/>
<mxCell id="p1B_r13c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1B" geo="1484,1760,56,42"/>
<mxCell id="p1b_lg0" value="綠底：常用動詞" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" geo="40,1948,130,40"/>
<mxCell id="p1b_lg1" value="白底：進階動詞" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="190,1948,130,40"/>
<mxCell id="p1b_lg2" value="藍底：一次性（bootstrap.sh）" style="fillColor=#dae8fc;strokeColor=light-dark(#000000,#9577A3)" geo="340,1948,210,40"/>
<mxCell id="p1b_lg3" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="570,1948,190,40"/>
<mxCell id="p1b_lg4" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="780,1948,110,40"/>
<mxCell id="p1b_lg5" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="910,1948,200,40"/>
<mxCell id="p1b_lgt" value="一列 = 一個動詞；「做什麼」欄一格一件事&lt;br&gt;「反向」= 收回它做的事的動詞" style="fillColor=none;strokeColor=none" geo="1130,1938,300,60"/>
<mxCell id="p1b_lg6" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="40,2014,200,40"/>
<mxCell id="p1b_lg6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="208,2016,30,20"/>
<mxCell id="p1b_lg7" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="260,2014,220,40"/>
<mxCell id="p1b_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,2070,300,28"/>
<mxCell id="p1b_tk0" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2104,150,40"/>
<mxCell id="p1b_tv0" value="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2104,610,40"/>
<mxCell id="p1b_tk1" value="N（目標版範本）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2144,150,40"/>
<mxCell id="p1b_tv1" value="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&amp;lt;id&amp;gt;/、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（唯讀），不是 cache；cache/&amp;lt;repo&amp;gt;/ 在 apply 決定套用後才 materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2144,610,40"/>
<mxCell id="p1b_tk2" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2184,150,55"/>
<mxCell id="p1b_tv2" value="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2184,610,55"/>
<mxCell id="p1b_tk3" value="docker image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2239,150,55"/>
<mxCell id="p1b_tv3" value="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2239,610,55"/>
<mxCell id="p1b_tk4" value=".digest 旁檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2294,150,55"/>
<mxCell id="p1b_tv4" value="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2294,610,55"/>
<mxCell id="p1b_tk5" value="初始檔五態（state）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2104,150,55"/>
<mxCell id="p1b_tv5" value="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2104,610,55"/>
<mxCell id="p1b_tk6" value="救援路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2159,150,55"/>
<mxCell id="p1b_tv6" value="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2159,610,55"/>
<mxCell id="p1b_tk7" value="「引擎已變」" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2214,150,55"/>
<mxCell id="p1b_tv7" value="不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行；ref 變了且 == 計畫的 engine → 用新 ref（local 覆寫時 inspect 驗 ID）跑 upgrade vendor_kit；第二次又變 → 1 印 6-2b" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2214,610,55"/>
</diagram>
<diagram id="v1p1c" name="契約 v2：規則、選項表、不開的動詞">
<mxCell id="title" value="契約① 使用者介面（3／3）── 規則、選項表（Q25）、結束碼（Q23／Q27）、不開的動詞、訊息文字（§6）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p1c_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p1c_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;選項與結束碼以 interface_spec §1.1／§2 為準；訊息文字 §6 逐字（本頁只列 p1／p1b 引用到的）" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p1C" value="3. 規則、選項總表（Q25）、結束碼總表（Q23／Q27）、不開的動詞、訊息文字（interface_spec §6 逐字）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,1777"/>
<mxCell id="p1C_pair_t" value="兩層成對（反向）" style="fillColor=none;strokeColor=none" parent="p1C" geo="20,50,200,24"/>
<mxCell id="p1C_pd0" value="專案層（vendor_kit 自己）" style="fillColor=none;strokeColor=none" parent="p1C" geo="20,74,200,30"/>
<mxCell id="p1C_pa0" value="install" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="225,74,110,30"/>
<mxCell id="p1C_pb0" value="uninstall" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="410,74,110,30"/>
<mxCell id="p1C_pe0" edge="1" source="p1C_pa0" target="p1C_pb0"/>
<mxCell id="p1C_pd1" value="工具層" style="fillColor=none;strokeColor=none" parent="p1C" geo="20,112,200,30"/>
<mxCell id="p1C_pa1" value="add" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="225,112,110,30"/>
<mxCell id="p1C_pb1" value="remove" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="410,112,110,30"/>
<mxCell id="p1C_pe1" edge="1" source="p1C_pa1" target="p1C_pb1"/>
<mxCell id="p1C_pd2" value="本機開發" style="fillColor=none;strokeColor=none" parent="p1C" geo="20,150,200,30"/>
<mxCell id="p1C_pa2" value="dev" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="225,150,110,30"/>
<mxCell id="p1C_pb2" value="undev" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="410,150,110,30"/>
<mxCell id="p1C_pe2" edge="1" source="p1C_pa2" target="p1C_pb2"/>
<mxCell id="p1C_pd3" value="只查 → 套用（apt 語意）" style="fillColor=none;strokeColor=none" parent="p1C" geo="20,188,200,30"/>
<mxCell id="p1C_pa3" value="update" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="225,188,110,30"/>
<mxCell id="p1C_pb3" value="upgrade" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" parent="p1C" geo="410,188,110,30"/>
<mxCell id="p1C_pe3" value="前一步" edge="1" source="p1C_pa3" target="p1C_pb3"/>
<mxCell id="p1C_no" value="&lt;b&gt;不開的動詞與理由&lt;/b&gt;&lt;br&gt;init（→ install）／ensure（→ sync）／diff（= upgrade --dry-run）／accept（解完衝突重跑 upgrade）／rollback（git revert）／--repair（併進 install 冪等修復）／--purge（明確不提供：永不刪使用者檔；開 issue）／--porcelain（不做；v2 候選，本版無待拍板）／--tag（版本一律 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;）／materialize、verify、merge（引擎內部步驟，不對外）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,236,740,92"/>
<mxCell id="p1C_no_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="728,238,30,20"/>
<mxCell id="p1C_s1" value="&lt;b&gt;recipe 規則&lt;/b&gt;&lt;br&gt;動詞 recipe 一律 verb *args 一行轉發（set positional-arguments 只在 vendor.just）、放 tracked 的 vendor.just；[group(&#x27;常用&#x27;)]／[group(&#x27;進階&#x27;)]；每次呼叫引擎附 --protocol P（在子命令之前）；entry.just 與 gen/tools.just 只含 mod／mod?／import?，零 set 零 recipe（被 import 檔的 set 會外溢到根檔）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,342,740,77"/>
<mxCell id="p1C_s1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="728,344,30,20"/>
<mxCell id="p1C_s2" value="&lt;b&gt;執行位置（Q20）&lt;/b&gt;&lt;br&gt;專案根 = 含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在專案根執行：recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免（工具 _sync 已 cd 回專案根）；須在某 git repo 內；禁止巢狀（上層或下層已有 → 1 印 6-35）；引擎不讀 .git、不碰 index、不做 git init" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,433,740,92"/>
<mxCell id="p1C_s2_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="728,435,30,20"/>
<mxCell id="p1C_s3" value="&lt;b&gt;兩段編排的兩個獨立屬性（p3b 契約④）&lt;/b&gt;&lt;br&gt;需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve → 主機 docker → apply，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,539,740,77"/>
<mxCell id="p1C_s3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="728,541,30,20"/>
<mxCell id="p1C_dry" value="&lt;b&gt;--dry-run（所有頁一致）&lt;/b&gt;&lt;br&gt;唯讀預覽（仍拉 image 展開到暫存，讀 /dist/&amp;lt;repo&amp;gt;）：印會建／會問哪些檔、6-6～6-8、metadata 遷移；本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單（version.toml 不動；與 -y 無關）；-y 也不覆蓋既有未納管檔、不硬加 append 行；EOF 不算同意" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,630,740,77"/>
<mxCell id="p1C_dry_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="728,632,30,20"/>
<mxCell id="p1C_opt_l" value="選項總表（Q25；短選項只給常用）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p1C" geo="790,50,700,28"/>
<mxCell id="p1C_opt_h0" value="選項" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="790,82,170,30"/>
<mxCell id="p1C_opt_h1" value="短形" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="960,82,50,30"/>
<mxCell id="p1C_opt_h2" value="型別" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="1010,82,90,30"/>
<mxCell id="p1C_opt_h3" value="適用" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="1100,82,200,30"/>
<mxCell id="p1C_opt_h4" value="說明" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="1300,82,240,30"/>
<mxCell id="p1C_opt_r0c0" value="--tool &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,112,170,42"/>
<mxCell id="p1C_opt_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="928,114,30,20"/>
<mxCell id="p1C_opt_r0c1" value="-t" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,112,50,42"/>
<mxCell id="p1C_opt_r0c2" value="string，可重複" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,112,90,42"/>
<mxCell id="p1C_opt_r0c3" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,112,200,42"/>
<mxCell id="p1C_opt_r0c4" value="接入的工具與版本；@&amp;lt;tag&amp;gt; 省略 = 最新正式版" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,112,240,42"/>
<mxCell id="p1C_opt_r1c0" value="--yes" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,154,170,57"/>
<mxCell id="p1C_opt_r1c1" value="-y" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,154,50,57"/>
<mxCell id="p1C_opt_r1c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,154,90,57"/>
<mxCell id="p1C_opt_r1c3" value="bootstrap.sh、install、uninstall、add、remove、upgrade、prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,154,200,57"/>
<mxCell id="p1C_opt_r1c4" value="免詢問（不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,154,240,57"/>
<mxCell id="p1C_opt_r2c0" value="--path &amp;lt;dir&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,211,170,26"/>
<mxCell id="p1C_opt_r2c1" value="-p" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,211,50,26"/>
<mxCell id="p1C_opt_r2c2" value="string" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,211,90,26"/>
<mxCell id="p1C_opt_r2c3" value="dev &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,211,200,26"/>
<mxCell id="p1C_opt_r2c4" value="本機工具目錄" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,211,240,26"/>
<mxCell id="p1C_opt_r3c0" value="--image &amp;lt;tag&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,237,170,26"/>
<mxCell id="p1C_opt_r3c1" value="-i" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,237,50,26"/>
<mxCell id="p1C_opt_r3c2" value="string" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,237,90,26"/>
<mxCell id="p1C_opt_r3c3" value="dev vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,237,200,26"/>
<mxCell id="p1C_opt_r3c4" value="本機引擎 image tag（只能 tag）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,237,240,26"/>
<mxCell id="p1C_opt_r4c0" value="--help" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,263,170,26"/>
<mxCell id="p1C_opt_r4c1" value="-h" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,263,50,26"/>
<mxCell id="p1C_opt_r4c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,263,90,26"/>
<mxCell id="p1C_opt_r4c3" value="全部" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,263,200,26"/>
<mxCell id="p1C_opt_r4c4" value="由引擎印；bootstrap.sh 自印" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,263,240,26"/>
<mxCell id="p1C_opt_r5c0" value="--dry-run" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,289,170,42"/>
<mxCell id="p1C_opt_r5c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,289,50,42"/>
<mxCell id="p1C_opt_r5c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,289,90,42"/>
<mxCell id="p1C_opt_r5c3" value="uninstall、add、remove、upgrade、prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,289,200,42"/>
<mxCell id="p1C_opt_r5c4" value="唯讀預覽（仍拉 image 展開）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,289,240,42"/>
<mxCell id="p1C_opt_r6c0" value="--source &amp;lt;image&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,331,170,42"/>
<mxCell id="p1C_opt_r6c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,331,50,42"/>
<mxCell id="p1C_opt_r6c2" value="string" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,331,90,42"/>
<mxCell id="p1C_opt_r6c3" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,331,200,42"/>
<mxCell id="p1C_opt_r6c4" value="image 路徑不符 &amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist 慣例時" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,331,240,42"/>
<mxCell id="p1C_opt_r7c0" value="--local &amp;lt;image tag 或 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,373,170,57"/>
<mxCell id="p1C_opt_r7c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="928,375,30,20"/>
<mxCell id="p1C_opt_r7c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,373,50,57"/>
<mxCell id="p1C_opt_r7c2" value="string" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,373,90,57"/>
<mxCell id="p1C_opt_r7c3" value="bootstrap.sh、add" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,373,200,57"/>
<mxCell id="p1C_opt_r7c4" value="離線：tar 先 docker load；值的判別已定（含 / 或 .tar 結尾 → 檔案，其餘 → tag；見名詞表）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,373,240,57"/>
<mxCell id="p1C_opt_r8c0" value="--exit-code" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,430,170,26"/>
<mxCell id="p1C_opt_r8c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,430,50,26"/>
<mxCell id="p1C_opt_r8c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,430,90,26"/>
<mxCell id="p1C_opt_r8c3" value="update" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,430,200,26"/>
<mxCell id="p1C_opt_r8c4" value="有新版回 2" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,430,240,26"/>
<mxCell id="p1C_opt_r9c0" value="--timeout &amp;lt;秒&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,456,170,42"/>
<mxCell id="p1C_opt_r9c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="928,458,30,20"/>
<mxCell id="p1C_opt_r9c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,456,50,42"/>
<mxCell id="p1C_opt_r9c2" value="正整數" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,456,90,42"/>
<mxCell id="p1C_opt_r9c3" value="bootstrap.sh、add、upgrade、sync、undev" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,456,200,42"/>
<mxCell id="p1C_opt_r9c4" value="= VENDOR_KIT_PULL_TIMEOUT，由啟動器攔截、不轉發引擎；優先於環境變數" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,456,240,42"/>
<mxCell id="p1C_opt_r10c0" value="--no-justfile" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,498,170,26"/>
<mxCell id="p1C_opt_r10c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,498,50,26"/>
<mxCell id="p1C_opt_r10c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,498,90,26"/>
<mxCell id="p1C_opt_r10c3" value="install" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,498,200,26"/>
<mxCell id="p1C_opt_r10c4" value="跳過根 justfile 步驟只印指示" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,498,240,26"/>
<mxCell id="p1C_opt_r11c0" value="--protocol P" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,524,170,26"/>
<mxCell id="p1C_opt_r11c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,524,50,26"/>
<mxCell id="p1C_opt_r11c2" value="整數" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,524,90,26"/>
<mxCell id="p1C_opt_r11c3" value="內部" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,524,200,26"/>
<mxCell id="p1C_opt_r11c4" value="薄殼→引擎全域旗標，不列 help" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,524,240,26"/>
<mxCell id="p1C_opt_r12c0" value="--verify" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,550,170,42"/>
<mxCell id="p1C_opt_r12c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="928,552,30,20"/>
<mxCell id="p1C_opt_r12c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="960,550,50,42"/>
<mxCell id="p1C_opt_r12c2" value="bool" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,550,90,42"/>
<mxCell id="p1C_opt_r12c3" value="sync" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1100,550,200,42"/>
<mxCell id="p1C_opt_r12c4" value="每檔 sha256 全驗（= CI 為真時的行為）；無參數 sync 走快路徑" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1300,550,240,42"/>
<mxCell id="p1C_opt_n" value="版本一律寫在位置參數：&amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;、vendor_kit@&amp;lt;tag&amp;gt;；@&amp;lt;tag&amp;gt; 比現版舊 → warn 仍執行。短選項只有 -t、-y、-p、-i、-h。" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="790,602,750,46"/>
<mxCell id="p1C_opt_n_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="1508,604,30,20"/>
<mxCell id="p1C_ex_l" value="結束碼總表（§2；多工具彙總見下框）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p1C" geo="20,723,700,28"/>
<mxCell id="p1C_ex_h0" value="碼" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="20,755,50,30"/>
<mxCell id="p1C_ex_h1" value="定義" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="70,755,700,30"/>
<mxCell id="p1C_ex_h2" value="動詞例外／特例" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="770,755,770,30"/>
<mxCell id="p1C_ex_r0c0" value="0" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,785,50,42"/>
<mxCell id="p1C_ex_r0c1" value="成功（含 warn）；add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符皆 0 + 提示" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,785,700,42"/>
<mxCell id="p1C_ex_r0c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="770,785,770,42"/>
<mxCell id="p1C_ex_r1c0" value="1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,827,50,42"/>
<mxCell id="p1C_ex_r1c1" value="一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,827,700,42"/>
<mxCell id="p1C_ex_r1c2" value="自身升級：已改 version.toml 第一行後回 1（明列例外）；upgrade vendor_kit 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）——既定回 1 的情境維持 1，不因提示含 upgrade 而改 3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="770,827,770,42"/>
<mxCell id="p1C_ex_r2c0" value="2" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,869,50,26"/>
<mxCell id="p1C_ex_r2c1" value="合併衝突（留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,869,700,26"/>
<mxCell id="p1C_ex_r2c2" value="update --exit-code 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔 baseline 不推、記入 conflicts" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="770,869,770,26"/>
<mxCell id="p1C_ex_r3c0" value="3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,895,50,57"/>
<mxCell id="p1C_ex_r3c1" value="現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且零寫入；「舊」一律以 P／schema 比，不以 SemVer；網路／認證／不存在 → 1，不得偽裝成 3；floor 檢查在任何上網之前" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,895,700,57"/>
<mxCell id="p1C_ex_r3c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="738,897,30,20"/>
<mxCell id="p1C_ex_r3c2" value="(a) 薄殼 P &amp;lt; 引擎 floor_P → 6-18；(b) 引擎讀到 schema &amp;gt; 支援上限 → 6-19；(c) upgrade vendor_kit@&amp;lt;舊版&amp;gt; 目標引擎 P／schema 低於現有檔 → 6-10；(d) dev vendor_kit -i 的引擎 P／schema 低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 6-36 提示先 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="770,895,770,57"/>
<mxCell id="p1C_multi" value="&lt;b&gt;多工具彙總（Q27）&lt;/b&gt;：不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p1C" geo="20,966,1520,30"/>
<mxCell id="p1C_multi_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p1C" geo="1508,968,30,20"/>
<mxCell id="p1C_msg_l" value="訊息文字清單（§6 逐字；每句含可直接複製的指令）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p1C" geo="20,1010,900,28"/>
<mxCell id="p1C_mL_h0" value="#" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="20,1042,50,30"/>
<mxCell id="p1C_mL_h1" value="時機" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="70,1042,170,30"/>
<mxCell id="p1C_mL_h2" value="文字（逐字；&amp;lt;…&amp;gt; 占位符）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="240,1042,530,30"/>
<mxCell id="p1C_mL_r0c0" value="6-1" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1072,50,42"/>
<mxCell id="p1C_mL_r0c1" value="sync：gen/.stamp 第一行 ≠ 引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1072,170,42"/>
<mxCell id="p1C_mL_r0c2" value="vendor_kit 已更新 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt;，請執行：just vendor_kit upgrade vendor_kit（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1072,530,42"/>
<mxCell id="p1C_mL_r1c0" value="6-2" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1114,50,42"/>
<mxCell id="p1C_mL_r1c1" value="upgrade vendor_kit 重產薄殼後" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1114,170,42"/>
<mxCell id="p1C_mL_r1c2" value="已升級引擎 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1114,530,42"/>
<mxCell id="p1C_mL_r2c0" value="6-2b" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1156,50,42"/>
<mxCell id="p1C_mL_r2c1" value="第一行已改但未重產／第二次又變" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1156,170,42"/>
<mxCell id="p1C_mL_r2c2" value="引擎版本已鎖定為 &amp;lt;vY&amp;gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1156,530,42"/>
<mxCell id="p1C_mL_r3c0" value="6-3" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1198,50,57"/>
<mxCell id="p1C_mL_r3c1" value="update／upgrade／add 無 registry 憑證" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1198,170,57"/>
<mxCell id="p1C_mL_r3c2" value="無法列舉 &amp;lt;repo&amp;gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;（拉取使用主機 docker 認證）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1198,530,57"/>
<mxCell id="p1C_mL_r4c0" value="6-4" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1255,50,42"/>
<mxCell id="p1C_mL_r4c1" value="需詢問但無 tty／EOF 且無 -y" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1255,170,42"/>
<mxCell id="p1C_mL_r4c2" value="需要確認但沒有終端可互動。請加 -y，或在終端執行。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1255,530,42"/>
<mxCell id="p1C_mL_r5c0" value="6-5" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1297,50,42"/>
<mxCell id="p1C_mL_r5c1" value="CI 下 baseline 落後；Renovate PR 需合併" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1297,170,42"/>
<mxCell id="p1C_mL_r5c2" value="請在本機執行 just vendor_kit upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1297,530,42"/>
<mxCell id="p1C_mL_r6c0" value="6-6／6-7／6-8" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1339,50,57"/>
<mxCell id="p1C_mL_r6c1" value="dry-run／check.sh 提醒（不紅燈）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1339,170,57"/>
<mxCell id="p1C_mL_r6c2" value="有 &amp;lt;N&amp;gt; 個範本你拒絕過／&amp;lt;X&amp;gt; 沒納管，與範本差 &amp;lt;N&amp;gt; 行／&amp;lt;Y&amp;gt; 你拒絕過，&amp;lt;vZ&amp;gt; 有新版" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1339,530,57"/>
<mxCell id="p1C_mL_r7c0" value="6-9" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1396,50,26"/>
<mxCell id="p1C_mL_r7c1" value="不在專案根執行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1396,170,26"/>
<mxCell id="p1C_mL_r7c2" value="請到 &amp;lt;dir&amp;gt; 執行（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1396,530,26"/>
<mxCell id="p1C_mL_r8c0" value="6-10" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1422,50,42"/>
<mxCell id="p1C_mL_r8c1" value="upgrade vendor_kit@&amp;lt;舊版&amp;gt; 無法無損讀" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1422,170,42"/>
<mxCell id="p1C_mL_r8c2" value="目標引擎 &amp;lt;vY&amp;gt;（協定 &amp;lt;P&amp;gt;、schema &amp;lt;M&amp;gt;）無法無損讀取現有檔（schema &amp;lt;N&amp;gt;）。未修改任何檔。要退回舊版請 git revert 相關 commit。（結束 3）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1422,530,42"/>
<mxCell id="p1C_mL_r9c0" value="6-11" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1464,50,26"/>
<mxCell id="p1C_mL_r9c1" value="add 初始檔已存在（copy）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1464,170,26"/>
<mxCell id="p1C_mL_r9c2" value="&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1464,530,26"/>
<mxCell id="p1C_mL_r10c0" value="6-12" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1490,50,26"/>
<mxCell id="p1C_mL_r10c1" value="apply 重驗指紋不同" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1490,170,26"/>
<mxCell id="p1C_mL_r10c2" value="專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit &amp;lt;verb&amp;gt; …（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1490,530,26"/>
<mxCell id="p1C_mL_r11c0" value="6-13" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1516,50,42"/>
<mxCell id="p1C_mL_r11c1" value="sync metadata 無完成標記" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1516,170,42"/>
<mxCell id="p1C_mL_r11c2" value="&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1516,530,42"/>
<mxCell id="p1C_mL_r12c0" value="6-14" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1558,50,42"/>
<mxCell id="p1C_mL_r12c1" value="upgrade 補完待合併後另有新版" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1558,170,42"/>
<mxCell id="p1C_mL_r12c2" value="已補齊 &amp;lt;repo&amp;gt; 至 &amp;lt;vB&amp;gt;；另有新版 &amp;lt;vX&amp;gt;，再跑一次 just vendor_kit upgrade &amp;lt;repo&amp;gt; 可升" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1558,530,42"/>
<mxCell id="p1C_mL_r13c0" value="6-15" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1600,50,26"/>
<mxCell id="p1C_mL_r13c1" value="update 末行" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1600,170,26"/>
<mxCell id="p1C_mL_r13c2" value="套用：just vendor_kit upgrade" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1600,530,26"/>
<mxCell id="p1C_mL_r14c0" value="6-16" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1626,50,42"/>
<mxCell id="p1C_mL_r14c1" value="install 非 git repo" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1626,170,42"/>
<mxCell id="p1C_mL_r14c2" value="目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1626,530,42"/>
<mxCell id="p1C_mL_r15c0" value="6-17" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1668,50,26"/>
<mxCell id="p1C_mL_r15c1" value="install &amp;lt;repo&amp;gt; 誤用" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1668,170,26"/>
<mxCell id="p1C_mL_r15c2" value="install 不接受工具名稱。接入工具請執行：just vendor_kit add &amp;lt;repo&amp;gt;（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1668,530,26"/>
<mxCell id="p1C_mL_r16c0" value="6-18" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="20,1694,50,26"/>
<mxCell id="p1C_mL_r16c1" value="薄殼／版本低於 floor" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="70,1694,170,26"/>
<mxCell id="p1C_mL_r16c2" value="目前薄殼或引擎低於支援下限 &amp;lt;floor&amp;gt;。請以 bootstrap.sh 重建。（結束 3、零寫入）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="240,1694,530,26"/>
<mxCell id="p1C_mR_h0" value="#" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="790,1042,50,30"/>
<mxCell id="p1C_mR_h1" value="時機" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="840,1042,170,30"/>
<mxCell id="p1C_mR_h2" value="文字（逐字；&amp;lt;…&amp;gt; 占位符）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p1C" geo="1010,1042,530,30"/>
<mxCell id="p1C_mR_r0c0" value="6-19" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1072,50,57"/>
<mxCell id="p1C_mR_r0c1" value="引擎讀到 schema 高於支援上限" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1072,170,57"/>
<mxCell id="p1C_mR_r0c2" value="無法讀取 &amp;lt;file&amp;gt;：schema &amp;lt;N&amp;gt; 高於本引擎支援的 &amp;lt;M&amp;gt;；寫入者為 vendor_kit &amp;lt;written_by&amp;gt;。請使用支援此 schema 的引擎，或使用 version.toml 指定的引擎。（結束 3）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1072,530,57"/>
<mxCell id="p1C_mR_r1c0" value="6-20" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1129,50,42"/>
<mxCell id="p1C_mR_r1c1" value="問句：根 justfile" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1129,170,42"/>
<mxCell id="p1C_mR_r1c2" value="要在 justfile 加這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;／要從 justfile 刪這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1129,530,42"/>
<mxCell id="p1C_mR_r2c0" value="6-21" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1171,50,26"/>
<mxCell id="p1C_mR_r2c1" value="問句：append" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1171,170,26"/>
<mxCell id="p1C_mR_r2c2" value="要在 &amp;lt;X&amp;gt; 加這幾行嗎（接列出行）／要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎（接列出行）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1171,530,26"/>
<mxCell id="p1C_mR_r3c0" value="6-22" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1197,50,42"/>
<mxCell id="p1C_mR_r3c1" value="問句：upgrade 逐檔" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1197,170,42"/>
<mxCell id="p1C_mR_r3c2" value="&amp;lt;X&amp;gt; 換成新版？／你和新版都改了 &amp;lt;X&amp;gt;，要三方合併嗎？／要建 &amp;lt;X&amp;gt; 嗎／&amp;lt;X&amp;gt; 是二進位檔，要換成新版嗎？" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1197,530,42"/>
<mxCell id="p1C_mR_r4c0" value="6-23" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1239,50,42"/>
<mxCell id="p1C_mR_r4c1" value="bootstrap just 太舊" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1239,170,42"/>
<mxCell id="p1C_mR_r4c2" value="需要 just ≥ 1.33.0，目前為 &amp;lt;version&amp;gt;。請使用 GitHub release 版。+ 固定兩行 下載：&amp;lt;平台對應 URL&amp;gt;、安裝：&amp;lt;不覆蓋既有檔的安裝指令&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1239,530,42"/>
<mxCell id="p1C_mR_r5c0" value="6-24" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1281,50,57"/>
<mxCell id="p1C_mR_r5c1" value="docker pull 失敗" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1281,170,57"/>
<mxCell id="p1C_mR_r5c2" value="原文 + 三分類（網路／認證／不存在；另「主機錯誤」：daemon 不可用、磁碟滿）；認證類：&amp;lt;ref&amp;gt; 不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login &amp;lt;host&amp;gt;；僅 add／bootstrap 追加 離線可用：--local &amp;lt;tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1281,530,57"/>
<mxCell id="p1C_mR_r6c0" value="6-26" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1338,50,42"/>
<mxCell id="p1C_mR_r6c1" value="flock 逾時" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1338,170,42"/>
<mxCell id="p1C_mR_r6c2" value="專案目錄被鎖定（PID &amp;lt;pid&amp;gt;，自 &amp;lt;time&amp;gt;）；60 秒內未釋放。確認無其他 vendor_kit 在跑後重試，或設 VENDOR_KIT_NO_LOCK=1。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1338,530,42"/>
<mxCell id="p1C_mR_r7c0" value="6-28" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1380,50,57"/>
<mxCell id="p1C_mR_r7c1" value="薄殼被改（install／upgrade vendor_kit）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1380,170,57"/>
<mxCell id="p1C_mR_r7c2" value="偵測到薄殼被修改：&amp;lt;files&amp;gt;。未重產任何薄殼。請先檢視下列差異；確認並手動還原（git checkout -- .vendor_kit/&amp;lt;file&amp;gt;）後，再執行 just vendor_kit upgrade vendor_kit。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1380,530,57"/>
<mxCell id="p1C_mR_r8c0" value="6-29" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1437,50,42"/>
<mxCell id="p1C_mR_r8c1" value="新增初始檔 dest 在 CI 路徑" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1437,170,42"/>
<mxCell id="p1C_mR_r8c2" value="注意：新版範本將建立或修改 CI 設定 &amp;lt;X&amp;gt;。請確認下列內容後再決定是否套用。" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1437,530,42"/>
<mxCell id="p1C_mR_r9c0" value="6-30" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1479,50,42"/>
<mxCell id="p1C_mR_r9c1" value="啟動器驗 vk-resolve 失敗" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1479,170,42"/>
<mxCell id="p1C_mR_r9c2" value="引擎輸出不完整或不相容（&amp;lt;原因&amp;gt;），未執行任何動作。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1479,530,42"/>
<mxCell id="p1C_mR_r10c0" value="6-31" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1521,50,42"/>
<mxCell id="p1C_mR_r10c1" value="pull 逾時" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1521,170,42"/>
<mxCell id="p1C_mR_r10c2" value="拉取 &amp;lt;ref&amp;gt; 超過 &amp;lt;秒&amp;gt; 秒未完成，已中止。可用 --timeout &amp;lt;秒&amp;gt; 或 VENDOR_KIT_PULL_TIMEOUT 調整。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1521,530,42"/>
<mxCell id="p1C_mR_r11c0" value="6-32" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1563,50,26"/>
<mxCell id="p1C_mR_r11c1" value="問句：prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1563,170,26"/>
<mxCell id="p1C_mR_r11c2" value="要刪除以上 vendor_kit 資源嗎？" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1563,530,26"/>
<mxCell id="p1C_mR_r12c0" value="6-33" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1589,50,42"/>
<mxCell id="p1C_mR_r12c1" value="唯讀動詞偵測未完成交易" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1589,170,42"/>
<mxCell id="p1C_mR_r12c2" value="偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;（sync／update 結束 1；help 不受影響；prune 只列出不刪）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1589,530,42"/>
<mxCell id="p1C_mR_r13c0" value="6-34" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1631,50,42"/>
<mxCell id="p1C_mR_r13c1" value="問句：根 .dockerignore" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1631,170,42"/>
<mxCell id="p1C_mR_r13c2" value="要在 .dockerignore 加這三行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.*" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1631,530,42"/>
<mxCell id="p1C_mR_r14c0" value="6-35" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1673,50,42"/>
<mxCell id="p1C_mR_r14c1" value="install 巢狀" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1673,170,42"/>
<mxCell id="p1C_mR_r14c2" value="&amp;lt;dir&amp;gt; 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。（結束 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1673,530,42"/>
<mxCell id="p1C_mR_r15c0" value="6-36" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="790,1715,50,42"/>
<mxCell id="p1C_mR_r15c1" value="舊薄殼跑新 major 一般動詞" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="840,1715,170,42"/>
<mxCell id="p1C_mR_r15c2" value="薄殼協定 &amp;lt;P_shell&amp;gt; 低於引擎 &amp;lt;vY&amp;gt; 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit（結束 3、零寫入）" style="fillColor=#ffffff;strokeColor=#999999" parent="p1C" geo="1010,1715,530,42"/>
<mxCell id="p1c_lg0" value="綠底：常用動詞" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" geo="40,1903,130,40"/>
<mxCell id="p1c_lg1" value="白底：進階動詞" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="190,1903,130,40"/>
<mxCell id="p1c_lg2" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="340,1903,190,40"/>
<mxCell id="p1c_lg3" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="550,1903,110,40"/>
<mxCell id="p1c_lg4" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="680,1903,200,40"/>
<mxCell id="p1c_lg5" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="900,1903,200,40"/>
<mxCell id="p1c_lg5_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1068,1905,30,20"/>
<mxCell id="p1c_lgt" value="「反向」= 收回它做的事的動詞&lt;br&gt;表格：一列一個選項／結束碼／訊息" style="fillColor=none;strokeColor=none" geo="1120,1893,300,60"/>
<mxCell id="p1c_lg6" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1969,220,40"/>
<mxCell id="p1c_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,2025,300,28"/>
<mxCell id="p1c_tk0" value="組（常用／進階／一次性）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2059,150,40"/>
<mxCell id="p1c_tv0" value="常用 = 每天會打的（add／upgrade／dev）；進階 = 偶爾才用；一次性 = 只在第一次接入跑的 bootstrap.sh（release 附的腳本，不是 just 動詞）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2059,610,40"/>
<mxCell id="p1c_tk1" value="反向" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2099,150,40"/>
<mxCell id="p1c_tv1" value="把該動詞做的事收回的動詞（install↔uninstall、add↔remove、dev↔undev）；upgrade 沒有動詞反向，靠 git revert（把整組升級 commit 反做一次的 git 指令）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2099,610,40"/>
<mxCell id="p1c_tk2" value="apt 語意" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2139,150,28"/>
<mxCell id="p1c_tv2" value="跟 Debian 的 apt 一樣分兩步：update 只查有沒有新版、不動檔；upgrade 才真的套用" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2139,610,28"/>
<mxCell id="p1c_tk3" value="--local 值的判別" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2167,150,40"/>
<mxCell id="p1c_tv3" value="已定：--local &amp;lt;值&amp;gt; 含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立（tag 含 / 且存在同名檔）→ 1 提示用 ./ 或完整 ref 消歧" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2167,610,40"/>
<mxCell id="p1c_tk4" value="pull 逾時" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2207,150,40"/>
<mxCell id="p1c_tv4" value="VENDOR_KIT_PULL_TIMEOUT／--timeout &amp;lt;秒&amp;gt;：單次 pull 總秒數，預設 300、只收正整數；逾時 → 1 印 6-31；啟動器自讀、不轉發引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2207,610,40"/>
<mxCell id="p1c_tk5" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2247,150,55"/>
<mxCell id="p1c_tv5" value="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2247,610,55"/>
<mxCell id="p1c_tk6" value="--protocol P" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2059,150,40"/>
<mxCell id="p1c_tv6" value="薄殼每次呼叫引擎都附的協定整數（第一版 P=1，在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 回應；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2059,610,40"/>
<mxCell id="p1c_tk7" value="floor" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2099,150,40"/>
<mxCell id="p1c_tv7" value="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2099,610,40"/>
<mxCell id="p1c_tk8" value="mod／mod?／import／import?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2139,150,55"/>
<mxCell id="p1c_tv8" value="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2139,610,55"/>
<mxCell id="p1c_tk9" value="專案根" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2194,150,71"/>
<mxCell id="p1c_tv9" value="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2194,610,71"/>
</diagram>
<diagram id="v1p2" name="契約 v2：目錄樹與檔案範例">
<mxCell id="title" value="契約② 專案裡的檔（1／3）── 目錄樹與檔案範例（interface_spec §4；誰寫它、誰可以改、進不進 git）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p2_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p2_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;檔名 version.toml 已定（§4.1：它是「該裝哪版」的宣告，不是 lock 產物）；右欄範例框逐字（等寬、保留縮排），說明一律放框外" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,81"/>
<mxCell id="p2_lbl" value="3. 目錄樹（專案根 = 含 .vendor_kit/ 的目錄；每格：用途｜寫：誰產生｜改：誰可改）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,109,620,28"/>
<mxCell id="t_root" value="&lt;b&gt;專案/&lt;/b&gt;（使用者的；專案根）" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="40,143,200,46"/>
<mxCell id="t_just" value="&lt;b&gt;justfile&lt;/b&gt; ── 使用者的 just 入口；install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;（無 → 建四行；有 → 問／-y；已含 → 不再加）&lt;br&gt;寫：install｜改：使用者隨意；uninstall 問後只刪完全相同的那行；add 只讀它查撞名" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="70,197,560,77"/>
<mxCell id="t_just_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,199,30,20"/>
<mxCell id="t_di" value="&lt;b&gt;.dockerignore&lt;/b&gt; ── 使用者的；install 加三行 .vendor_kit/cache/、gen/、.tmp.*（無 → 建；有 → 問 6-34／-y）&lt;br&gt;寫：install（記於 baseline/.vendor_kit.toml）｜改：使用者隨意；uninstall 問後只刪原文相同行" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="70,282,560,77"/>
<mxCell id="t_di_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,284,30,20"/>
<mxCell id="t_vk" value="&lt;b&gt;.vendor_kit/&lt;/b&gt; ── 根目錄只多這一個；薄殼 + 狀態 + 快取都在裡面；上層或下層不得再有一個（禁止巢狀）&lt;br&gt;寫：install、upgrade vendor_kit 重產薄殼（先比對薄殼首行）｜改：人不改；uninstall 只刪 hash 相符的自產檔" style="fillColor=#ffffff;strokeColor=#82b366" geo="70,367,560,77"/>
<mxCell id="t_vk_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,369,30,20"/>
<mxCell id="t_ver" value="&lt;b&gt;version.toml&lt;/b&gt; ── 進 git：唯一來源。vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot; 正規行（唯一）、schema、written_by、[tools] 一行一工具 tag@digest&lt;br&gt;寫：install／add／upgrade／remove（apply 最後才寫）｜改：使用者可手改、Renovate PR 改；sync 只讀" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,452,530,77"/>
<mxCell id="t_ver_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,454,30,20"/>
<mxCell id="t_vl" value="&lt;b&gt;version.local.toml&lt;/b&gt; ── 不進 git（自有 .gitignore 擋）；與 version.toml 同形：工具覆寫 path:&amp;lt;dir&amp;gt;；引擎覆寫 tag + vendor_kit_image_id&lt;br&gt;寫：dev／undev（含 image ID）；bootstrap --local 在 install 成功後才寫｜改：不建議手改；uninstall hash 相符才刪；CI 為真下有任何覆寫 → sync 回 1" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="100,537,530,108"/>
<mxCell id="t_vl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,539,30,20"/>
<mxCell id="t_gi" value="&lt;b&gt;.gitignore&lt;/b&gt; ── 進 git，我們自己的：cache/ gen/ version.local.toml .tmp.*；第一行自描述&lt;br&gt;寫：install／upgrade vendor_kit 重產｜改：人不改" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,653,530,61"/>
<mxCell id="t_gi_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,655,30,20"/>
<mxCell id="t_entry" value="&lt;b&gt;entry.just&lt;/b&gt; ── 進 git：mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;（零 set 零 recipe）；第一行自描述&lt;br&gt;寫：引擎 launcher-gen（install／upgrade vendor_kit）｜改：人不改" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,722,530,61"/>
<mxCell id="t_entry_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,724,30,20"/>
<mxCell id="t_vj" value="&lt;b&gt;vendor.just&lt;/b&gt; ── 進 git：動詞 recipe 一行轉發 + 啟動器本體（POSIX sh；set positional-arguments 只放這；附 --protocol P）；第一行自描述&lt;br&gt;寫：引擎 launcher-gen｜改：人不改" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,791,530,77"/>
<mxCell id="t_vj_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,793,30,20"/>
<mxCell id="t_ci" value="&lt;b&gt;ci/check.sh&lt;/b&gt; ── 進 git：下游 CI 呼叫的契約檢查（⓪–⑤ 六步，契約⑤ p3c）；第一行 shebang、第二行自描述、之後 export CI=1&lt;br&gt;寫：引擎 launcher-gen｜改：人不改" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,876,530,61"/>
<mxCell id="t_ci_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,878,30,20"/>
<mxCell id="t_bl" value="&lt;b&gt;baseline/&lt;/b&gt; ── 進 git：install 建 .gitkeep（git 不追蹤空目錄）；&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；.vendor_kit.toml = install 對根 .dockerignore 的 append 記錄&lt;br&gt;寫：install（.gitkeep）；add 建 &amp;lt;repo&amp;gt;/、upgrade 推進（有衝突仍推）｜改：人不改（改了合併就錯）" style="fillColor=#ffffff;strokeColor=#82b366" geo="100,945,530,92"/>
<mxCell id="t_bl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,947,30,20"/>
<mxCell id="t_meta" value="&lt;b&gt;&amp;lt;repo&amp;gt;/.vendor_kit.toml&lt;/b&gt; ── 進 git：metadata（欄位見 p2b）；兼作該目錄佔位&lt;br&gt;寫：add／upgrade（install 不建）｜改：人不改" style="fillColor=#ffffff;strokeColor=#82b366" geo="130,1045,500,61"/>
<mxCell id="t_meta_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1047,30,20"/>
<mxCell id="t_gen" value="&lt;b&gt;gen/&lt;/b&gt; ── 不進 git：引擎產生的三種檔（下列三格），各自由不同動詞寫&lt;br&gt;寫：引擎｜改：人不改（會被覆蓋）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="100,1114,530,46"/>
<mxCell id="t_gen_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1116,30,20"/>
<mxCell id="t_tools" value="&lt;b&gt;tools.just&lt;/b&gt; ── 每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;（上方一行 # &amp;lt;description&amp;gt;；零 set 零 recipe）&lt;br&gt;寫：sync／add／remove／upgrade 重生（最後寫、與 cache 同一 apply 內原子替換）｜改：人不改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1168,500,92"/>
<mxCell id="t_tools_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1170,30,20"/>
<mxCell id="t_gstamp" value="&lt;b&gt;.stamp&lt;/b&gt; ── 只記產生薄殼的引擎 ref（一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1（不重寫）&lt;br&gt;寫：只由 install／upgrade vendor_kit｜改：人不改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1268,500,61"/>
<mxCell id="t_gstamp_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1270,30,20"/>
<mxCell id="t_rstamp" value="&lt;b&gt;&amp;lt;repo&amp;gt;.stamp&lt;/b&gt; ── 每工具一個印記：第一行 index digest（dev 時 path:&amp;lt;dir&amp;gt;），之後每檔 sha256；sync 用它決定要不要 materialize&lt;br&gt;寫：引擎 materialize｜改：不可改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1337,500,61"/>
<mxCell id="t_rstamp_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1339,30,20"/>
<mxCell id="t_repo" value="&lt;b&gt;cache/&amp;lt;repo&amp;gt;/&lt;/b&gt; ── 不進 git、使用者不可改；只放從暫存 /dist 展開的內容（dev 時是 symlink → &amp;lt;dir&amp;gt;/dist）&lt;br&gt;寫：引擎 materialize（apply 決定套用之後）｜改：不可改（verify 失敗 → 重裝並 warn）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="100,1406,530,77"/>
<mxCell id="t_repo_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1408,30,20"/>
<mxCell id="t_files" value="&lt;b&gt;files/ …&lt;/b&gt; ── 工具檔案（dist/files/ 全部；無 symlink，展開時驗）｜寫：materialize｜改：不可改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1491,500,46"/>
<mxCell id="t_init" value="&lt;b&gt;init.toml&lt;/b&gt; ── 初始檔清單（[[file]] src／dest／strategy = &quot;copy&quot;|&quot;append&quot;；schema；description）｜寫：materialize｜改：不可改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1545,500,61"/>
<mxCell id="t_init_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1547,30,20"/>
<mxCell id="t_rjust" value="&lt;b&gt;just/&amp;lt;ns&amp;gt;.just&lt;/b&gt; ── 工具的 just 模組，每檔一個頂層命名空間（&amp;lt;repo&amp;gt;.just 必有；含私有 _sync）｜寫：materialize｜改：不可改" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="130,1614,500,46"/>
<mxCell id="t_rjust_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1616,30,20"/>
<mxCell id="t_tmp" value="&lt;b&gt;.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml&lt;/b&gt;、&lt;b&gt;.tmp.dist.&amp;lt;id&amp;gt;/&lt;/b&gt; ── 不進 git：修復型 install／remove／uninstall／undev／prune 的進度日誌；啟動器暫存（展開的 dist、vk-resolve）&lt;br&gt;寫：apply 第一個寫入前建、最後一步刪；啟動器 mktemp、trap 刪｜改：人不改；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="100,1668,530,92"/>
<mxCell id="t_tmp_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1670,30,20"/>
<mxCell id="t_user" value="&lt;b&gt;初始檔&lt;/b&gt;（例 Dockerfile…；路徑由 init.toml 的 dest 決定）── 使用者的；進 git；state 記在 metadata（五態）&lt;br&gt;寫：add 建（已存在不納管；append 問後加行）、upgrade 逐檔問後換／三方合併／建新檔｜改：使用者隨意；remove／uninstall 永不刪，印清單" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="70,1768,560,77"/>
<mxCell id="t_user_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="598,1770,30,20"/>
<mxCell id="te1" edge="1" source="t_root" target="t_just"/>
<mxCell id="te21" edge="1" source="t_root" target="t_di"/>
<mxCell id="te2" edge="1" source="t_root" target="t_vk"/>
<mxCell id="te3" edge="1" source="t_vk" target="t_ver"/>
<mxCell id="te4" edge="1" source="t_vk" target="t_vl"/>
<mxCell id="te5" edge="1" source="t_vk" target="t_gi"/>
<mxCell id="te6" edge="1" source="t_vk" target="t_entry"/>
<mxCell id="te7" edge="1" source="t_vk" target="t_vj"/>
<mxCell id="te8" edge="1" source="t_vk" target="t_ci"/>
<mxCell id="te9" edge="1" source="t_vk" target="t_bl"/>
<mxCell id="te10" edge="1" source="t_bl" target="t_meta"/>
<mxCell id="te11" edge="1" source="t_vk" target="t_gen"/>
<mxCell id="te12" edge="1" source="t_gen" target="t_tools"/>
<mxCell id="te13" edge="1" source="t_gen" target="t_gstamp"/>
<mxCell id="te15" edge="1" source="t_gen" target="t_rstamp"/>
<mxCell id="te14" edge="1" source="t_vk" target="t_repo"/>
<mxCell id="te16" edge="1" source="t_repo" target="t_files"/>
<mxCell id="te17" edge="1" source="t_repo" target="t_init"/>
<mxCell id="te18" edge="1" source="t_repo" target="t_rjust"/>
<mxCell id="te20" edge="1" source="t_vk" target="t_tmp"/>
<mxCell id="te19" edge="1" source="t_root" target="t_user"/>
<mxCell id="p2_ver_l" value=".vendor_kit/version.toml（進 git；schema = 1）── 啟動器只靠 grep 讀正規行" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,109,940,28"/>
<mxCell id="p2_ver" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:v1.0.0@sha256:&amp;lt;digest&amp;gt;&quot;&lt;br&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;&lt;br&gt;[tools]&lt;br&gt;&amp;lt;repo&amp;gt; = &quot;ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:v2.3.0@sha256:&amp;lt;digest&amp;gt;&quot;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,141,497,108"/>
<mxCell id="p2_ver_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1125,143,30,20"/>
<mxCell id="p2_ver_n" value="第 1 行 = 唯一正規行：行首無空白、鍵後一空白、=、一空白、雙引號、&lt;b&gt;無尾端註解&lt;/b&gt;、LF（regex 讀不到就是 1）&lt;br&gt;schema：格式版本，引擎讀、啟動器不讀；written_by：寫入引擎版本，純資訊&lt;br&gt;[tools]：每工具一行 tag@digest（多架構 index digest）" style="fillColor=#ffffff;strokeColor=#999999" geo="1169,141,431,108"/>
<mxCell id="p2_vl_l" value=".vendor_kit/version.local.toml（不進 git；與 version.toml 同形）── dev 寫、undev 刪、bootstrap --local 寫" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,263,940,28"/>
<mxCell id="p2_vl" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;vendor_kit:dev&quot;&lt;br&gt;vendor_kit_image_id = &quot;sha256:&amp;lt;image id&amp;gt;&quot;&lt;br&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;&lt;br&gt;[tools]&lt;br&gt;&amp;lt;repo&amp;gt; = &quot;path:/home/me/&amp;lt;repo&amp;gt;&quot;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,295,346,124"/>
<mxCell id="p2_vl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="974,297,30,20"/>
<mxCell id="p2_vl_n" value="vendor_kit：dev vendor_kit -i &amp;lt;tag&amp;gt; 寫的本機引擎 image，只能 tag（docker load 後無 RepoDigests）；同樣是正規行、無尾端註解&lt;br&gt;vendor_kit_image_id：啟動器每次 docker image inspect 比對、不 pull；同 tag 重 build 才會被發現；undev 一併撤&lt;br&gt;[tools].&amp;lt;repo&amp;gt;：dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt; 寫 path:&amp;lt;dir&amp;gt;；cache/&amp;lt;repo&amp;gt;/ 變 symlink → &amp;lt;dir&amp;gt;/dist；啟動器掛 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro" style="fillColor=#ffffff;strokeColor=#999999" geo="1018,295,582,124"/>
<mxCell id="p2_jf_l" value="根 justfile（使用者的；install 新建時逐字四行；已有時只加第一行）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,433,940,28"/>
<mxCell id="p2_jf" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;br&gt;&lt;br&gt;default:&lt;br&gt;&#9;@just --list&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,465,300,77"/>
<mxCell id="p2_jf_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="928,467,30,20"/>
<mxCell id="p2_jf_n" value="第 4 行行首是&lt;b&gt;真 tab&lt;/b&gt;（recipe 本體必須縮排；default: @just --list 寫成單行是 just 語法錯誤，所以拆兩行）&lt;br&gt;已有 justfile → 問 6-20 只加第 1 行；uninstall 只刪完全相同的那行" style="fillColor=#ffffff;strokeColor=#999999" geo="972,465,628,77"/>
<mxCell id="p2_di_l" value="根 .dockerignore（使用者的；install append 三行；uninstall 問後只刪原文相同行）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,556,940,28"/>
<mxCell id="p2_di" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,588,300,61"/>
<mxCell id="p2_di_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="928,590,30,20"/>
<mxCell id="p2_di_n" value="無 → 建；有 → 問 6-34 後 append（-y 免問）；插入的行記於 baseline/.vendor_kit.toml&lt;br&gt;工具以專案根當 build context 時靠它排除 cache" style="fillColor=#ffffff;strokeColor=#999999" geo="972,588,628,61"/>
<mxCell id="p2_tj_l" value=".vendor_kit/gen/tools.just（不進 git；每個 &amp;lt;ns&amp;gt;.just 一行 mod?；零 set 零 recipe）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,663,940,28"/>
<mxCell id="p2_tj" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# &amp;lt;description&amp;gt;&lt;br&gt;mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,695,353,46"/>
<mxCell id="p2_tj_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="981,697,30,20"/>
<mxCell id="p2_tj_n" value="# &amp;lt;description&amp;gt;：來自 init.toml 頂層 description；缺則 &amp;lt;repo&amp;gt; &amp;lt;tag&amp;gt;&lt;br&gt;mod?：cache 缺檔時其他 recipe 與 just vendor_kit sync 仍可跑" style="fillColor=#ffffff;strokeColor=#999999" geo="1025,695,575,46"/>
<mxCell id="p2_sh_l" value="薄殼自描述首行（entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,755,940,28"/>
<mxCell id="p2_sh" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# vendor_kit-shell/1 engine=v1.0.0 sha256=&amp;lt;hash&amp;gt;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,787,396,61"/>
<mxCell id="p2_sh_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1024,789,30,20"/>
<mxCell id="p2_sh_n" value="&amp;lt;P&amp;gt; = 協定版本（1）、engine = 產生它的引擎；&amp;lt;hash&amp;gt; = 其餘內容 CRLF→LF 正規化後的 sha256&lt;br&gt;引擎重算 hash + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" style="fillColor=#ffffff;strokeColor=#999999" geo="1068,787,532,61"/>
<mxCell id="p2_st_l" value=".vendor_kit/gen/&amp;lt;repo&amp;gt;.stamp（每工具印記；materialize 寫）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,862,940,28"/>
<mxCell id="p2_st" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;sha256:&amp;lt;hex64&amp;gt;&lt;br&gt;&amp;lt;sha256&amp;gt;  files/…&lt;br&gt;&amp;lt;sha256&amp;gt;  init.toml&lt;br&gt;&amp;lt;sha256&amp;gt;  just/&amp;lt;ns&amp;gt;.just&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,894,300,77"/>
<mxCell id="p2_st_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="928,896,30,20"/>
<mxCell id="p2_st_n" value="第 1 行：多架構 index digest（add --local 亦為正式 digest）；dev 時 path:&amp;lt;dir&amp;gt;；無 image:&amp;lt;tag&amp;gt; 形&lt;br&gt;之後每檔一行 &amp;lt;sha256&amp;gt;  &amp;lt;相對路徑&amp;gt;；verify 逐檔比；檔內沒有註解" style="fillColor=#ffffff;strokeColor=#999999" geo="972,894,628,77"/>
<mxCell id="p2_gs_l" value=".vendor_kit/gen/.stamp（只由 install／upgrade vendor_kit 寫）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,985,940,28"/>
<mxCell id="p2_gs" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:v1.0.0@sha256:&amp;lt;digest&amp;gt;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1017,389,46"/>
<mxCell id="p2_gs_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1017,1019,30,20"/>
<mxCell id="p2_gs_n" value="唯一一行：產生薄殼的引擎 ref（local 覆寫時為 &amp;lt;tag&amp;gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1" style="fillColor=#ffffff;strokeColor=#999999" geo="1061,1017,539,46"/>
<mxCell id="p2_tv_l" value=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（修復型 install／remove／uninstall／undev／prune 進度日誌；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機）" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,1077,940,28"/>
<mxCell id="p2_tv" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;verb = &quot;remove&quot;&lt;br&gt;id = &quot;&amp;lt;id&amp;gt;&quot;&lt;br&gt;targets = [&quot;&amp;lt;repo&amp;gt;&quot;]&lt;br&gt;started = &quot;&amp;lt;UTC ISO 8601&amp;gt;&quot;&lt;br&gt;done = [...]&lt;br&gt;pending = [...]&lt;br&gt;consents = [...]&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1109,300,155"/>
<mxCell id="p2_tv_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="928,1111,30,20"/>
<mxCell id="p2_tv_n" value="consents = 已取得的同意；done／pending = 已完成／未完成步驟&lt;br&gt;第一個寫入前建、成功結束時整個檔刪除；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33" style="fillColor=#ffffff;strokeColor=#999999" geo="972,1109,628,155"/>
<mxCell id="p2_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="660,1284,200,28"/>
<mxCell id="p2_tk0" value="唯一來源" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1318,150,30"/>
<mxCell id="p2_tv0" value="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1318,790,30"/>
<mxCell id="p2_tk1" value="vendor_kit = 正規行" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1348,150,57"/>
<mxCell id="p2_tv1" value="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1348,790,57"/>
<mxCell id="p2_tk2" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1405,150,42"/>
<mxCell id="p2_tv2" value="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1405,790,42"/>
<mxCell id="p2_tk3" value="image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1447,150,42"/>
<mxCell id="p2_tv3" value="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1447,790,42"/>
<mxCell id="p2_tk4" value="薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1489,150,42"/>
<mxCell id="p2_tv4" value=".vendor_kit/ 進 git、vendor_kit 擁有、人不改的四檔：entry.just、vendor.just、.gitignore、ci/check.sh；只轉發、不做事；每檔自描述首行；只由 install／upgrade vendor_kit 重產" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1489,790,42"/>
<mxCell id="p2_tk5" value="薄殼自描述首行" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1531,150,42"/>
<mxCell id="p2_tv5" value="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1531,790,42"/>
<mxCell id="p2_tk6" value="gen/" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1573,150,42"/>
<mxCell id="p2_tv6" value="引擎產生的檔，不進 git，三種：tools.just（sync／add／remove／upgrade 重生）、.stamp（只由 install／upgrade vendor_kit 寫）、&amp;lt;repo&amp;gt;.stamp（materialize 寫）" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1573,790,42"/>
<mxCell id="p2_tk7" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1615,150,42"/>
<mxCell id="p2_tv7" value="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1615,790,42"/>
<mxCell id="p2_tk8" value="印記 gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1657,150,42"/>
<mxCell id="p2_tv8" value="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&amp;lt;dir&amp;gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1657,790,42"/>
<mxCell id="p2_tk9" value="mod／mod?／import／import?" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1699,150,57"/>
<mxCell id="p2_tv9" value="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1699,790,57"/>
<mxCell id="p2_tk10" value="cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1756,150,42"/>
<mxCell id="p2_tv10" value="工具 image 的 /dist 展開副本，收在 .vendor_kit/ 裡；不進 git、不可改；dev 時是 symlink → &amp;lt;dir&amp;gt;/dist；印記不在這裡（在 gen/&amp;lt;repo&amp;gt;.stamp）" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1756,790,42"/>
<mxCell id="p2_tk11" value="初始檔" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1798,150,42"/>
<mxCell id="p2_tv11" value="工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1798,790,42"/>
<mxCell id="p2_tk12" value="初始檔五態（state）" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1840,150,42"/>
<mxCell id="p2_tv12" value="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1840,790,42"/>
<mxCell id="p2_tk13" value="baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1882,150,42"/>
<mxCell id="p2_tv13" value=".vendor_kit/baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1882,790,42"/>
<mxCell id="p2_tk14" value="baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1924,150,42"/>
<mxCell id="p2_tv14" value="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 兼作該工具目錄的佔位）" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1924,790,42"/>
<mxCell id="p2_tk15" value="進度日誌檔 .tmp.*" style="fillColor=#ffffff;strokeColor=#999999" geo="660,1966,150,57"/>
<mxCell id="p2_tv15" value="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" style="fillColor=#ffffff;strokeColor=#999999" geo="810,1966,790,57"/>
<mxCell id="p2_tk16" value="暫存 .tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="660,2023,150,42"/>
<mxCell id="p2_tv16" value="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" style="fillColor=#ffffff;strokeColor=#999999" geo="810,2023,790,42"/>
<mxCell id="p2_tk17" value="根 justfile 四行" style="fillColor=#ffffff;strokeColor=#999999" geo="660,2065,150,42"/>
<mxCell id="p2_tv17" value="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" style="fillColor=#ffffff;strokeColor=#999999" geo="810,2065,790,42"/>
<mxCell id="p2_tk18" value="根 .dockerignore 三行" style="fillColor=#ffffff;strokeColor=#999999" geo="660,2107,150,57"/>
<mxCell id="p2_tv18" value="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" style="fillColor=#ffffff;strokeColor=#999999" geo="810,2107,790,57"/>
<mxCell id="p2_tk19" value="專案根" style="fillColor=#ffffff;strokeColor=#999999" geo="660,2164,150,57"/>
<mxCell id="p2_tv19" value="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git" style="fillColor=#ffffff;strokeColor=#999999" geo="810,2164,790,57"/>
<mxCell id="p2_lg0" value="綠框：進 git" style="fillColor=#ffffff;strokeColor=#82b366" geo="40,2251.0,120,40"/>
<mxCell id="p2_lg1" value="灰虛線：不進 git（可重建）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="180,2251.0,200,40"/>
<mxCell id="p2_lg2" value="黃底綠框：使用者的檔（進 git）" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="400,2251.0,230,40"/>
<mxCell id="p2_lg3" value="等寬字：檔案內容範例" style="fillColor=#ffffff;strokeColor=#999999" geo="650,2251.0,170,40"/>
<mxCell id="p2_lg4" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="840,2251.0,200,40"/>
<mxCell id="p2_lg4_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1008,2253.0,30,20"/>
<mxCell id="p2_lg5" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="1060,2251.0,220,40"/>
<mxCell id="p2_lgt" value="樹線 = 目錄包含；範例框右邊 = 框外說明&lt;br&gt;綠標籤 = v2 改；schema 表 p2b、矩陣 p2c" style="fillColor=none;strokeColor=none" geo="1300,2241.0,300,60"/>
</diagram>
<diagram id="v1p2b" name="契約 v2：schema：version.toml／local／metadata／印記／薄殼首行">
<mxCell id="title" value="契約② 專案裡的檔（2／3）── schema：version.toml／version.local.toml／metadata／印記／薄殼首行（interface_spec §4）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p2b_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p2b_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;欄位名、型別、必填以 interface_spec §4 為準；範例見 p2；動詞 × 檔案矩陣見 p2c" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p2B" value="4. 檔案 schema（欄位／型別／必填／說明；一列一欄位）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,1362"/>
<mxCell id="p2b_gen" value="&lt;b&gt;TOML 通則（所有 vendor_kit 寫的檔）&lt;/b&gt;&lt;br&gt;每檔 schema = N（integer）+ written_by = &quot;&amp;lt;vX&amp;gt;&quot;（string，純資訊，不作讀取門檻）；讀取門檻只看 schema；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯、重複宣告 → 1；schema 高於本引擎支援 → 3 印 6-19 零寫入；讀任一舊 schema → 直接寫當前 schema（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。第一版 schema = 1" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2B" geo="20,50,750,92"/>
<mxCell id="p2b_gen_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="738,52,30,20"/>
<mxCell id="p2b_ver_l" value="4.1 .vendor_kit/version.toml" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="20,156,750,28"/>
<mxCell id="p2b_ver_m" value="進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；使用者、Renovate 可手改；sync 只讀" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p2B" geo="20,188,750,30"/>
<mxCell id="p2b_canon" value="&lt;b&gt;version.toml 正規行契約&lt;/b&gt;&lt;br&gt;vendor_kit 行唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號基本字串、無尾端註解、LF 結尾）；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：^vendor_kit[[:space:]]*=[[:space:]]*&quot;\([^&quot;]*\)&quot;[[:space:]]*$（POSIX BRE，不用 \s）；命中數必須恰為 1（grep -c），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 [tools] 之前。禁止：BOM、重複鍵、[vendor_kit] 表旁路等 regex 讀不到／讀錯的等價寫法。公開格式：工具可讀它寫來源紀錄" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2B" geo="20,232,750,108"/>
<mxCell id="p2b_canon_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="738,234,30,20"/>
<mxCell id="p2b_ver_h0" value="欄位" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="20,354,190,30"/>
<mxCell id="p2b_ver_h1" value="型別／必填" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="210,354,130,30"/>
<mxCell id="p2b_ver_h2" value="說明" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="340,354,430,30"/>
<mxCell id="p2b_ver_r0c0" value="vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,384,190,42"/>
<mxCell id="p2b_ver_r0c1" value="string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,384,130,42"/>
<mxCell id="p2b_ver_r0c2" value="引擎 ref ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;digest&amp;gt;（多架構 index digest）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,384,430,42"/>
<mxCell id="p2b_ver_r1c0" value="schema" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,426,190,26"/>
<mxCell id="p2b_ver_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="178,428,30,20"/>
<mxCell id="p2b_ver_r1c1" value="integer／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,426,130,26"/>
<mxCell id="p2b_ver_r1c2" value="啟動器不讀、只引擎讀" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,426,430,26"/>
<mxCell id="p2b_ver_r2c0" value="written_by" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,452,190,26"/>
<mxCell id="p2b_ver_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="178,454,30,20"/>
<mxCell id="p2b_ver_r2c1" value="string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,452,130,26"/>
<mxCell id="p2b_ver_r2c2" value="寫入引擎版本，純資訊" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,452,430,26"/>
<mxCell id="p2b_ver_r3c0" value="[tools].&amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,478,190,57"/>
<mxCell id="p2b_ver_r3c1" value="string／每工具" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,478,130,57"/>
<mxCell id="p2b_ver_r3c2" value="ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;@sha256:&amp;lt;digest&amp;gt;（index digest；add --local 亦寫正式 index digest，來自 .digest 旁檔）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,478,430,57"/>
<mxCell id="p2b_vl_l" value="4.2 .vendor_kit/version.local.toml" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="20,549,750,28"/>
<mxCell id="p2b_vl_m" value="不進 git（自有 .gitignore 擋）；與 version.toml 同形（同一套讀寫器）；寫入者 dev／undev／bootstrap --local；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；frozen 下存在任何覆寫 → sync 回 1；啟動器先讀它再退回 version.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p2B" geo="20,581,750,61"/>
<mxCell id="p2b_vl_m_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="738,583,30,20"/>
<mxCell id="p2b_vl_h0" value="欄位" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="20,656,190,30"/>
<mxCell id="p2b_vl_h1" value="型別／必填" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="210,656,130,30"/>
<mxCell id="p2b_vl_h2" value="說明" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="340,656,430,30"/>
<mxCell id="p2b_vl_r0c0" value="vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,686,190,26"/>
<mxCell id="p2b_vl_r0c1" value="string／否" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,686,130,26"/>
<mxCell id="p2b_vl_r0c2" value="本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,686,430,26"/>
<mxCell id="p2b_vl_r1c0" value="vendor_kit_image_id" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,712,190,57"/>
<mxCell id="p2b_vl_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="178,714,30,20"/>
<mxCell id="p2b_vl_r1c1" value="string／有 vendor_kit 時必填" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,712,130,57"/>
<mxCell id="p2b_vl_r1c2" value="sha256:&amp;lt;hex64&amp;gt;，dev 時解析；啟動器每次 docker image inspect 比對，同 tag 重 build 才會被發現；undev vendor_kit 一併撤" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,712,430,57"/>
<mxCell id="p2b_vl_r2c0" value="schema、written_by" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,769,190,42"/>
<mxCell id="p2b_vl_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="178,771,30,20"/>
<mxCell id="p2b_vl_r2c1" value="integer、string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,769,130,42"/>
<mxCell id="p2b_vl_r2c2" value="同通則" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,769,430,42"/>
<mxCell id="p2b_vl_r3c0" value="[tools].&amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,811,190,42"/>
<mxCell id="p2b_vl_r3c1" value="string／否" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="210,811,130,42"/>
<mxCell id="p2b_vl_r3c2" value="path:&amp;lt;dir&amp;gt;（絕對路徑）；cache/&amp;lt;repo&amp;gt;/ 為 symlink → &amp;lt;dir&amp;gt;/dist" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="340,811,430,42"/>
<mxCell id="p2b_gen_l" value="4.4 gen/.stamp、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just（不進 git）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="20,867,750,28"/>
<mxCell id="p2b_gn_h0" value="檔" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="20,899,180,30"/>
<mxCell id="p2b_gn_h1" value="寫入者" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="200,899,180,30"/>
<mxCell id="p2b_gn_h2" value="內容" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="380,899,390,30"/>
<mxCell id="p2b_gn_r0c0" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,929,180,57"/>
<mxCell id="p2b_gn_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="168,931,30,20"/>
<mxCell id="p2b_gn_r0c1" value="只由 install／upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="200,929,180,57"/>
<mxCell id="p2b_gn_r0c2" value="第一行 = 產生薄殼的引擎 ref（local 覆寫時為 &amp;lt;tag&amp;gt;），供 sync grep 快速比對；不承擔薄殼 hash；fresh clone 缺此檔時相容判定改用薄殼自描述首行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="380,929,390,57"/>
<mxCell id="p2b_gn_r1c0" value="gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,986,180,88"/>
<mxCell id="p2b_gn_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="168,988,30,20"/>
<mxCell id="p2b_gn_r1c1" value="materialize" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="200,986,180,88"/>
<mxCell id="p2b_gn_r1c2" value="第一行 = 多架構 index digest sha256:&amp;lt;hex64&amp;gt;（與 version.toml 一致；add --local 亦為正式 index digest，本機驗證用 metadata local_image_id）或 dev 時 path:&amp;lt;dir&amp;gt;；無 image:&amp;lt;tag&amp;gt; 形；之後每檔一行 &amp;lt;sha256&amp;gt;  &amp;lt;相對路徑&amp;gt;；verify 逐檔比" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="380,986,390,88"/>
<mxCell id="p2b_gn_r2c0" value="gen/tools.just" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,1074,180,73"/>
<mxCell id="p2b_gn_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="168,1076,30,20"/>
<mxCell id="p2b_gn_r2c1" value="sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="200,1074,180,73"/>
<mxCell id="p2b_gn_r2c2" value="每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;（一工具可多行），每行上方一行 # &amp;lt;description&amp;gt;；零 set 零 recipe" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="380,1074,390,73"/>
<mxCell id="p2b_tmp_l" value="4.6 .vendor_kit/.tmp.*（皆由自有 .gitignore 的 .tmp.* 擋）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="20,1161,750,28"/>
<mxCell id="p2b_tmp_h0" value="檔" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="20,1193,170,30"/>
<mxCell id="p2b_tmp_h1" value="內容" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="190,1193,580,30"/>
<mxCell id="p2b_tmp_r0c0" value=".tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,1223,170,73"/>
<mxCell id="p2b_tmp_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="158,1225,30,20"/>
<mxCell id="p2b_tmp_r0c1" value="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機，不用 &amp;lt;repo&amp;gt; 以免 uninstall 多工具撞名）；內容 = schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪；未完成 → 可寫動詞恢復、唯讀動詞印 6-33；prune 不刪未恢復者" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="190,1223,580,73"/>
<mxCell id="p2b_tmp_r1c0" value=".tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="20,1296,170,42"/>
<mxCell id="p2b_tmp_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="158,1298,30,20"/>
<mxCell id="p2b_tmp_r1c1" value="啟動器暫存（展開的工具 dist、vk-resolve）；mktemp -d &quot;&amp;lt;專案根&amp;gt;/.vendor_kit/.tmp.dist.XXXXXX&quot;；trap 刪；prune 清殘留" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="190,1296,580,42"/>
<mxCell id="p2b_mt_l" value="4.3 baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（metadata）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="790,50,750,28"/>
<mxCell id="p2b_mt_m" value="進 git；寫入者 add／upgrade；兼作 baseline/&amp;lt;repo&amp;gt;/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列。註：install 對根 .dockerignore 的三行 append 不屬任何工具，記於 baseline/.vendor_kit.toml（同 schema，只含 [[file]] dest=.dockerignore state=appended lines=三行），uninstall 讀它刪原文相同行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p2B" geo="790,82,750,77"/>
<mxCell id="p2b_mt_m_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="1508,84,30,20"/>
<mxCell id="p2b_mt_h0" value="欄位" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="790,173,190,30"/>
<mxCell id="p2b_mt_h1" value="型別／必填" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="980,173,130,30"/>
<mxCell id="p2b_mt_h2" value="說明" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="1110,173,430,30"/>
<mxCell id="p2b_mt_r0c0" value="schema、written_by" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,203,190,42"/>
<mxCell id="p2b_mt_r0c1" value="integer、string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,203,130,42"/>
<mxCell id="p2b_mt_r0c2" value="同通則" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,203,430,42"/>
<mxCell id="p2b_mt_r1c0" value="source" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,245,190,57"/>
<mxCell id="p2b_mt_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,247,30,20"/>
<mxCell id="p2b_mt_r1c1" value="string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,245,130,57"/>
<mxCell id="p2b_mt_r1c2" value="這份 baseline 來自哪個工具 image &amp;lt;ref&amp;gt;（tag@index digest）= 最後合併版本；≠ version.toml → sync 本機 warn／CI 為真 1 印 6-5；upgrade 先補待合併到該版然後停" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,245,430,57"/>
<mxCell id="p2b_mt_r2c0" value="local_image_id" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,302,190,42"/>
<mxCell id="p2b_mt_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,304,30,20"/>
<mxCell id="p2b_mt_r2c1" value="string／add --local 時" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,302,130,42"/>
<mxCell id="p2b_mt_r2c2" value="sha256:&amp;lt;hex64&amp;gt;：本機 image ID ↔ source 的 index digest 對照，供離線驗證" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,302,430,42"/>
<mxCell id="p2b_mt_r3c0" value="complete" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,344,190,42"/>
<mxCell id="p2b_mt_r3c1" value="bool／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,344,130,42"/>
<mxCell id="p2b_mt_r3c2" value="add 走完 materialize → 初始檔 → baseline 才 true；缺或 false → sync 1 印 6-13；true 且再 add → 0 無變更" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,344,430,42"/>
<mxCell id="p2b_mt_r4c0" value="conflicts" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,386,190,42"/>
<mxCell id="p2b_mt_r4c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,388,30,20"/>
<mxCell id="p2b_mt_r4c1" value="array of string／是（可空）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,386,130,42"/>
<mxCell id="p2b_mt_r4c2" value="upgrade 回 2 時留標記或解析失敗的 dest 清單；仍含標籤 → 2 停；解析失敗的 dest 其 baseline 不推；解完重跑才清空" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,386,430,42"/>
<mxCell id="p2b_mt_r5c0" value="[[file]].dest" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,428,190,26"/>
<mxCell id="p2b_mt_r5c1" value="string" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,428,130,26"/>
<mxCell id="p2b_mt_r5c2" value="相對專案根" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,428,430,26"/>
<mxCell id="p2b_mt_r6c0" value="[[file]].state" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,454,190,57"/>
<mxCell id="p2b_mt_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,456,30,20"/>
<mxCell id="p2b_mt_r6c1" value="string（單一列舉）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,454,130,57"/>
<mxCell id="p2b_mt_r6c2" value="managed（已納管）／appended（append 已插入）／declined（新增檔被拒、從未納管）／unmanaged（本來就有、沒納管）／deleted（使用者刪了已納管檔，upgrade 維持刪除）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,454,430,57"/>
<mxCell id="p2b_mt_r7c0" value="[[file]]&lt;br&gt;.declined_hash" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,511,190,73"/>
<mxCell id="p2b_mt_r7c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,513,30,20"/>
<mxCell id="p2b_mt_r7c1" value="string／選填" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,511,130,73"/>
<mxCell id="p2b_mt_r7c2" value="最近一次被拒絕的那版範本 N 的 sha256。已納管檔（managed／appended，含二進位）拒絕本次更新 → state 不變、只記此欄；新檔（從未建立）被拒 → state=declined + 此欄；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,511,430,73"/>
<mxCell id="p2b_mt_r8c0" value="[[file]].lines" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,584,190,42"/>
<mxCell id="p2b_mt_r8c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,586,30,20"/>
<mxCell id="p2b_mt_r8c1" value="array of string／只在 appended" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,584,130,42"/>
<mxCell id="p2b_mt_r8c2" value="實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,584,430,42"/>
<mxCell id="p2b_mt_r9c0" value="[progress]" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,626,190,57"/>
<mxCell id="p2b_mt_r9c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="948,628,30,20"/>
<mxCell id="p2b_mt_r9c1" value="table／交易中" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="980,626,130,57"/>
<mxCell id="p2b_mt_r9c2" value="state = &quot;in-progress&quot;、started（UTC ISO 8601）、verb、id、done／pending（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、唯讀動詞印 6-33" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="1110,626,430,57"/>
<mxCell id="p2b_sm" value="&lt;b&gt;upgrade 逐檔狀態機（B = baseline、D = 磁碟、N = 新版讀自 /dist/&amp;lt;repo&amp;gt;；只對 state=managed、無待解衝突）&lt;/b&gt;&lt;br&gt;D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 git merge-file --diff3（標籤 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 等），衝突 → 2；不論結果 baseline 推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → 問後換、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 conflicts、baseline 不推。拒絕：已納管檔 state 不變、只記 declined_hash；新增檔（從未建立）→ state=declined + declined_hash。五態轉移圖見狀態機頁" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2B" geo="790,697,750,124"/>
<mxCell id="p2b_sm_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="1508,699,30,20"/>
<mxCell id="p2b_sh_l" value="4.5 薄殼（進 git，vendor_kit 擁有，人不改）與使用者的兩個根檔" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2B" geo="790,835,750,28"/>
<mxCell id="p2b_sh_h0" value="檔" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="790,867,170,30"/>
<mxCell id="p2b_sh_h1" value="內容" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2B" geo="960,867,580,30"/>
<mxCell id="p2b_sh_r0c0" value="自描述首行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,897,170,73"/>
<mxCell id="p2b_sh_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="928,899,30,20"/>
<mxCell id="p2b_sh_r0c1" value="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;hash&amp;gt;；hash = 首行（含其換行）之後全部位元組 CRLF→LF 正規化後的 sha256；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 印 6-28 列差異不動；mode 變更只 warn" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,897,580,73"/>
<mxCell id="p2b_sh_r1c0" value="entry.just" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,970,170,26"/>
<mxCell id="p2b_sh_r1c1" value="mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;；零 set 零 recipe" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,970,580,26"/>
<mxCell id="p2b_sh_r2c0" value="vendor.just" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,996,170,42"/>
<mxCell id="p2b_sh_r2c1" value="動詞 recipe 一行轉發 + 啟動器本體（POSIX sh recipe）；set positional-arguments 只放這" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,996,580,42"/>
<mxCell id="p2b_sh_r3c0" value=".gitignore" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,1038,170,26"/>
<mxCell id="p2b_sh_r3c1" value="cache/、gen/、version.local.toml、.tmp.*" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,1038,580,26"/>
<mxCell id="p2b_sh_r4c0" value="ci/check.sh" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,1064,170,26"/>
<mxCell id="p2b_sh_r4c1" value="契約⑤ p3c：shebang、自描述、export CI=1、⓪–⑤ 六步" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,1064,580,26"/>
<mxCell id="p2b_sh_r5c0" value="根 justfile（使用者的）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,1090,170,42"/>
<mxCell id="p2b_sh_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="928,1092,30,20"/>
<mxCell id="p2b_sh_r5c1" value="install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;；無檔則建，內容逐字四行：import 一行／空行／default:／\t@just --list；uninstall 只刪完全相同行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,1090,580,42"/>
<mxCell id="p2b_sh_r6c0" value="根 .dockerignore（使用者的）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="790,1132,170,42"/>
<mxCell id="p2b_sh_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2B" geo="928,1134,30,20"/>
<mxCell id="p2b_sh_r6c1" value="install append 三行 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34）；uninstall 問後只刪原文相同行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2B" geo="960,1132,580,42"/>
<mxCell id="p2b_lg0" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="40,1488,190,40"/>
<mxCell id="p2b_lg1" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="250,1488,110,40"/>
<mxCell id="p2b_lg2" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="380,1488,200,40"/>
<mxCell id="p2b_lg3" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="600,1488,200,40"/>
<mxCell id="p2b_lg3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="768,1490,30,20"/>
<mxCell id="p2b_lg4" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="820,1488,220,40"/>
<mxCell id="p2b_lgt" value="一列一個欄位；「型別／必填」照 interface_spec §4&lt;br&gt;範例（等寬字）見 p2" style="fillColor=none;strokeColor=none" geo="1060,1478,300,60"/>
<mxCell id="p2b_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1544,300,28"/>
<mxCell id="p2b_tk0" value="schema／written_by" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1578,150,55"/>
<mxCell id="p2b_tv0" value="每個 vendor_kit 寫的 TOML 都有 schema = N（integer，讀取門檻只看它）+ written_by = &quot;&amp;lt;vX&amp;gt;&quot;（純資訊）；同 schema 只加不改；讀時忽略未知欄位、寫時保留；只拒絕型別錯／重複宣告 → 1；schema 高於本引擎 → 3 印 6-19 零寫入" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1578,610,55"/>
<mxCell id="p2b_tk1" value="vendor_kit = 正規行" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1633,150,55"/>
<mxCell id="p2b_tv1" value="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1633,610,55"/>
<mxCell id="p2b_tk2" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1688,150,55"/>
<mxCell id="p2b_tv2" value="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1688,610,55"/>
<mxCell id="p2b_tk3" value="image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1743,150,55"/>
<mxCell id="p2b_tv3" value="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1743,610,55"/>
<mxCell id="p2b_tk4" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1798,150,55"/>
<mxCell id="p2b_tv4" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1798,610,55"/>
<mxCell id="p2b_tk5" value="初始檔五態（state）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1853,150,55"/>
<mxCell id="p2b_tv5" value="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1853,610,55"/>
<mxCell id="p2b_tk6" value="declined／declined_hash" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1908,150,55"/>
<mxCell id="p2b_tv6" value="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1908,610,55"/>
<mxCell id="p2b_tk7" value="conflicts（衝突中檔案）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1963,150,55"/>
<mxCell id="p2b_tv7" value="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1963,610,55"/>
<mxCell id="p2b_tk8" value="進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2018,150,71"/>
<mxCell id="p2b_tv8" value="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2018,610,71"/>
<mxCell id="p2b_tk9" value="三方合併" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1578,150,40"/>
<mxCell id="p2b_tv9" value="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1578,610,40"/>
<mxCell id="p2b_tk10" value="印記 gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1618,150,40"/>
<mxCell id="p2b_tv10" value="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&amp;lt;dir&amp;gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1618,610,40"/>
<mxCell id="p2b_tk11" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1658,150,55"/>
<mxCell id="p2b_tv11" value="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1658,610,55"/>
<mxCell id="p2b_tk12" value="薄殼自描述首行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1713,150,55"/>
<mxCell id="p2b_tv12" value="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1713,610,55"/>
<mxCell id="p2b_tk13" value="mod／mod?／import／import?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1768,150,55"/>
<mxCell id="p2b_tv13" value="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1768,610,55"/>
<mxCell id="p2b_tk14" value="進度日誌檔 .tmp.*" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1823,150,55"/>
<mxCell id="p2b_tv14" value="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1823,610,55"/>
<mxCell id="p2b_tk15" value="暫存 .tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1878,150,40"/>
<mxCell id="p2b_tv15" value="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1878,610,40"/>
<mxCell id="p2b_tk16" value="多架構 index／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1918,150,40"/>
<mxCell id="p2b_tv16" value="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1918,610,40"/>
<mxCell id="p2b_tk17" value=".digest 旁檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1958,150,55"/>
<mxCell id="p2b_tv17" value="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1958,610,55"/>
</diagram>
<diagram id="v1p2c" name="契約 v2：動詞 × 檔案矩陣">
<mxCell id="title" value="契約② 專案裡的檔（3／3）── 動詞 × 檔案矩陣、會碰／不碰使用者東西、version.toml 怎麼被讀" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p2c_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p2c_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;寫 = 產生／覆蓋；刪 = 移除；— = 不碰；依 interface_spec §1.2 副作用欄與 §4 寫入者" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p2C" value="5. 動詞 × 檔案（一列一動詞、一欄一檔；細節見 p1b 與流程頁）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,1516"/>
<mxCell id="p2c_tc_l" value="「會碰使用者東西」只有三處（不變量：可以建、要改先問、永不刪、永不覆蓋；拒絕 → 不寫：新檔 state=declined、已納管檔只記 declined_hash）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2C" geo="20,50,1300,28"/>
<mxCell id="p2c_tc_h0" value="東西" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="20,82,200,30"/>
<mxCell id="p2c_tc_h1" value="怎麼碰" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="220,82,1320,30"/>
<mxCell id="p2c_tc_r0c0" value="根 justfile 一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,112,200,42"/>
<mxCell id="p2c_tc_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="188,114,30,20"/>
<mxCell id="p2c_tc_r0c1" value="install：無 → 建四行（import + 空行 + default: + \t@just --list）；有 → 問 6-20（-y 直接加並印出）；已含 → 不再加；根檔是 symlink → 不寫、印遷移指示｜uninstall：問 6-20，只刪與我們寫的完全相同的行｜add：只讀它做撞名檢查（just --dump --dump-format json）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="220,112,1320,42"/>
<mxCell id="p2c_tc_r1c0" value="根 .dockerignore 三行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,154,200,26"/>
<mxCell id="p2c_tc_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="188,156,30,20"/>
<mxCell id="p2c_tc_r1c1" value="install：無 → 建；有 → 問 6-34 後 append（-y 免問），插入的行記於 baseline/.vendor_kit.toml｜uninstall：問後只刪原文相同的行｜工具 build 以專案根當 context 時靠它排除 cache" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="220,154,1320,26"/>
<mxCell id="p2c_tc_r2c0" value="初始檔（init.toml 的 dest）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,180,200,42"/>
<mxCell id="p2c_tc_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="188,182,30,20"/>
<mxCell id="p2c_tc_r2c1" value="add：無 → 建；有 → 不納管、不覆蓋（unmanaged，印 6-11）；strategy=append 問 6-21 後加行｜upgrade：逐檔狀態機後問 6-22（換／三方合併／建新檔／二進位）；拒絕 → declined_hash（新檔 state=declined）；N 變了才再問｜remove／uninstall：永不刪，印清單；append 行問後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="220,180,1320,42"/>
<mxCell id="p2c_not" value="&lt;b&gt;不碰&lt;/b&gt;：使用者的 .gitignore（除非工具以 strategy=append 宣告且你同意）、.git/info/exclude（dev 也不寫）、.git 本身（引擎不讀 .git、不碰 index、不做 git init）；我們要忽略的路徑全放 .vendor_kit/.gitignore；-y 不授權覆蓋既有未納管檔、不硬加 append 行" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2C" geo="20,236,1520,46"/>
<mxCell id="p2c_not_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,238,30,20"/>
<mxCell id="p2c_mx_l" value="表 A：進 git 的宣告、使用者的兩個根檔、薄殼、gen/.stamp（動詞 × 檔案）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2C" geo="20,296,1200,28"/>
<mxCell id="p2c_mx_h0" value="動詞" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="20,328,130,30"/>
<mxCell id="p2c_mx_h1" value="version.toml" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="150,328,210,30"/>
<mxCell id="p2c_mx_h2" value="version.local.toml" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="360,328,240,30"/>
<mxCell id="p2c_mx_h3" value="根 justfile" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="600,328,210,30"/>
<mxCell id="p2c_mx_h4" value="根 .dockerignore" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="810,328,200,30"/>
<mxCell id="p2c_mx_h5" value="薄殼（tracked 四檔）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="1010,328,300,30"/>
<mxCell id="p2c_mx_h6" value="gen/.stamp" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="1310,328,230,30"/>
<mxCell id="p2c_mx_r0c0" value="install" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,358,130,42"/>
<mxCell id="p2c_mx_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,360,30,20"/>
<mxCell id="p2c_mx_r0c1" value="寫（schema、written_by、正規行）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,358,210,42"/>
<mxCell id="p2c_mx_r0c2" value="—（bootstrap --local 成功後才寫 tag + image ID）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,358,240,42"/>
<mxCell id="p2c_mx_r0c3" value="無 → 建四行；有 → 問加一行；已含 → 不再加" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,358,210,42"/>
<mxCell id="p2c_mx_r0c4" value="無 → 建三行；有 → 問後 append" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,358,200,42"/>
<mxCell id="p2c_mx_r0c5" value="首行 hash 相符才重產；不符 → 1 印 6-28" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,358,300,42"/>
<mxCell id="p2c_mx_r0c6" value="寫（引擎 ref）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,358,230,42"/>
<mxCell id="p2c_mx_r1c0" value="uninstall" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,400,130,26"/>
<mxCell id="p2c_mx_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,402,30,20"/>
<mxCell id="p2c_mx_r1c1" value="hash 相符才刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,400,210,26"/>
<mxCell id="p2c_mx_r1c2" value="hash 相符才刪；否則保留並回報" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,400,240,26"/>
<mxCell id="p2c_mx_r1c3" value="問後只刪相同的行（之後才刪日誌）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,400,210,26"/>
<mxCell id="p2c_mx_r1c4" value="問後只刪原文相同三行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,400,200,26"/>
<mxCell id="p2c_mx_r1c5" value="只刪 hash 相符的自產檔；未知或被改的保留並回報" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,400,300,26"/>
<mxCell id="p2c_mx_r1c6" value="刪（自產）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,400,230,26"/>
<mxCell id="p2c_mx_r2c0" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,426,130,26"/>
<mxCell id="p2c_mx_r2c1" value="最後加 [tools] 一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,426,210,26"/>
<mxCell id="p2c_mx_r2c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,426,240,26"/>
<mxCell id="p2c_mx_r2c3" value="—（只讀：撞名檢查）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,426,210,26"/>
<mxCell id="p2c_mx_r2c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,426,200,26"/>
<mxCell id="p2c_mx_r2c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,426,300,26"/>
<mxCell id="p2c_mx_r2c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,426,230,26"/>
<mxCell id="p2c_mx_r3c0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,452,130,26"/>
<mxCell id="p2c_mx_r3c1" value="刪一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,452,210,26"/>
<mxCell id="p2c_mx_r3c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,452,240,26"/>
<mxCell id="p2c_mx_r3c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,452,210,26"/>
<mxCell id="p2c_mx_r3c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,452,200,26"/>
<mxCell id="p2c_mx_r3c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,452,300,26"/>
<mxCell id="p2c_mx_r3c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,452,230,26"/>
<mxCell id="p2c_mx_r4c0" value="upgrade（工具）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,478,130,26"/>
<mxCell id="p2c_mx_r4c1" value="最後改一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,478,210,26"/>
<mxCell id="p2c_mx_r4c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,478,240,26"/>
<mxCell id="p2c_mx_r4c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,478,210,26"/>
<mxCell id="p2c_mx_r4c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,478,200,26"/>
<mxCell id="p2c_mx_r4c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,478,300,26"/>
<mxCell id="p2c_mx_r4c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,478,230,26"/>
<mxCell id="p2c_mx_r5c0" value="upgrade（不帶 repo）遇引擎新版" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,504,130,57"/>
<mxCell id="p2c_mx_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,506,30,20"/>
<mxCell id="p2c_mx_r5c1" value="只改正規行（舊引擎）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,504,210,57"/>
<mxCell id="p2c_mx_r5c2" value="—（覆寫時啟動器 docker image inspect 驗 ID）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,504,240,57"/>
<mxCell id="p2c_mx_r5c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,504,210,57"/>
<mxCell id="p2c_mx_r5c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,504,200,57"/>
<mxCell id="p2c_mx_r5c5" value="接手：新引擎跑 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,504,300,57"/>
<mxCell id="p2c_mx_r5c6" value="同下列" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,504,230,57"/>
<mxCell id="p2c_mx_r6c0" value="upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,561,130,42"/>
<mxCell id="p2c_mx_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,563,30,20"/>
<mxCell id="p2c_mx_r6c1" value="有新版才改正規行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,561,210,42"/>
<mxCell id="p2c_mx_r6c2" value="—（覆寫優先，inspect 驗 ID、不 pull）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,561,240,42"/>
<mxCell id="p2c_mx_r6c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,561,210,42"/>
<mxCell id="p2c_mx_r6c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,561,200,42"/>
<mxCell id="p2c_mx_r6c5" value="首行 hash 相符才重產四檔；降版讀不了 → 3 不動" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,561,300,42"/>
<mxCell id="p2c_mx_r6c6" value="寫（引擎 ref）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,561,230,42"/>
<mxCell id="p2c_mx_r7c0" value="dev" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,603,130,42"/>
<mxCell id="p2c_mx_r7c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,605,30,20"/>
<mxCell id="p2c_mx_r7c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,603,210,42"/>
<mxCell id="p2c_mx_r7c2" value="加行（工具 path:／引擎 tag + vendor_kit_image_id）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,603,240,42"/>
<mxCell id="p2c_mx_r7c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,603,210,42"/>
<mxCell id="p2c_mx_r7c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,603,200,42"/>
<mxCell id="p2c_mx_r7c5" value="—（-i 舊 image 禁止重產）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,603,300,42"/>
<mxCell id="p2c_mx_r7c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,603,230,42"/>
<mxCell id="p2c_mx_r8c0" value="undev" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,645,130,42"/>
<mxCell id="p2c_mx_r8c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,647,30,20"/>
<mxCell id="p2c_mx_r8c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,645,210,42"/>
<mxCell id="p2c_mx_r8c2" value="刪行（含 image ID；建日誌後；最後一個覆寫撤掉刪整檔）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,645,240,42"/>
<mxCell id="p2c_mx_r8c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,645,210,42"/>
<mxCell id="p2c_mx_r8c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,645,200,42"/>
<mxCell id="p2c_mx_r8c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,645,300,42"/>
<mxCell id="p2c_mx_r8c6" value="—（undev vendor_kit 後不符只印 6-1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,645,230,42"/>
<mxCell id="p2c_mx_r9c0" value="sync" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,687,130,26"/>
<mxCell id="p2c_mx_r9c1" value="—（只讀）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,687,210,26"/>
<mxCell id="p2c_mx_r9c2" value="—（只讀；CI 為真下有覆寫 → 1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,687,240,26"/>
<mxCell id="p2c_mx_r9c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,687,210,26"/>
<mxCell id="p2c_mx_r9c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,687,200,26"/>
<mxCell id="p2c_mx_r9c5" value="不寫（不符 → 1 印 6-1）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,687,300,26"/>
<mxCell id="p2c_mx_r9c6" value="不寫（只比對）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,687,230,26"/>
<mxCell id="p2c_mx_r10c0" value="update" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,713,130,26"/>
<mxCell id="p2c_mx_r10c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,713,210,26"/>
<mxCell id="p2c_mx_r10c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,713,240,26"/>
<mxCell id="p2c_mx_r10c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,713,210,26"/>
<mxCell id="p2c_mx_r10c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,713,200,26"/>
<mxCell id="p2c_mx_r10c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,713,300,26"/>
<mxCell id="p2c_mx_r10c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,713,230,26"/>
<mxCell id="p2c_mx_r11c0" value="prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,739,130,26"/>
<mxCell id="p2c_mx_r11c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,741,30,20"/>
<mxCell id="p2c_mx_r11c1" value="—（只讀：哪些 image 仍被引用）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,739,210,26"/>
<mxCell id="p2c_mx_r11c2" value="—（只讀：keep 含覆寫 tag）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,739,240,26"/>
<mxCell id="p2c_mx_r11c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,739,210,26"/>
<mxCell id="p2c_mx_r11c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,739,200,26"/>
<mxCell id="p2c_mx_r11c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,739,300,26"/>
<mxCell id="p2c_mx_r11c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,739,230,26"/>
<mxCell id="p2c_mx_r12c0" value="任何動詞（結束碼 3）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,765,130,42"/>
<mxCell id="p2c_mx_r12c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,767,30,20"/>
<mxCell id="p2c_mx_r12c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,765,210,42"/>
<mxCell id="p2c_mx_r12c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="360,765,240,42"/>
<mxCell id="p2c_mx_r12c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="600,765,210,42"/>
<mxCell id="p2c_mx_r12c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="810,765,200,42"/>
<mxCell id="p2c_mx_r12c5" value="零寫入（無任何例外；救援路徑回 3 也零寫入）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,765,300,42"/>
<mxCell id="p2c_mx_r12c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1310,765,230,42"/>
<mxCell id="p2c_my_l" value="表 B：baseline／gen 兩檔／cache／初始檔／.tmp.*" style="fillColor=none;strokeColor=none;fontSize=13" parent="p2C" geo="20,821,1200,28"/>
<mxCell id="p2c_my_h0" value="動詞" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="20,853,130,30"/>
<mxCell id="p2c_my_h1" value="baseline/ + metadata" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="150,853,250,30"/>
<mxCell id="p2c_my_h2" value="gen/tools.just" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="400,853,190,30"/>
<mxCell id="p2c_my_h3" value="gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="590,853,190,30"/>
<mxCell id="p2c_my_h4" value="cache/&amp;lt;repo&amp;gt;/" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="780,853,230,30"/>
<mxCell id="p2c_my_h5" value="初始檔" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="1010,853,320,30"/>
<mxCell id="p2c_my_h6" value=".tmp.*" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p2C" geo="1330,853,210,30"/>
<mxCell id="p2c_my_r0c0" value="install" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,883,130,73"/>
<mxCell id="p2c_my_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,885,30,20"/>
<mxCell id="p2c_my_r0c1" value="建 baseline/.gitkeep（不建 metadata）；.dockerignore 記錄寫 baseline/.vendor_kit.toml" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,883,250,73"/>
<mxCell id="p2c_my_r0c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,883,190,73"/>
<mxCell id="p2c_my_r0c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,883,190,73"/>
<mxCell id="p2c_my_r0c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,883,230,73"/>
<mxCell id="p2c_my_r0c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,883,320,73"/>
<mxCell id="p2c_my_r0c6" value="修復型 install：.tmp.install.&amp;lt;id&amp;gt;.toml（第一次 install 不建日誌，失敗整包丟棄）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,883,210,73"/>
<mxCell id="p2c_my_r1c0" value="uninstall" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,956,130,42"/>
<mxCell id="p2c_my_r1c1" value="先預檢（hash 相符清單）→ 逐工具 remove；未知或被改的保留" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,956,250,42"/>
<mxCell id="p2c_my_r1c2" value="刪（自產）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,956,190,42"/>
<mxCell id="p2c_my_r1c3" value="刪（自產）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,956,190,42"/>
<mxCell id="p2c_my_r1c4" value="刪（未知檔保留並回報）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,956,230,42"/>
<mxCell id="p2c_my_r1c5" value="永不刪；append 行問後刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,956,320,42"/>
<mxCell id="p2c_my_r1c6" value=".tmp.uninstall.&amp;lt;id&amp;gt;.toml（最後刪）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,956,210,42"/>
<mxCell id="p2c_my_r1c6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,958,30,20"/>
<mxCell id="p2c_my_r2c0" value="add" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,998,130,42"/>
<mxCell id="p2c_my_r2c1" value="建 &amp;lt;repo&amp;gt;/ + metadata（complete、五態、lines、source）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,998,250,42"/>
<mxCell id="p2c_my_r2c2" value="重生" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,998,190,42"/>
<mxCell id="p2c_my_r2c3" value="materialize 寫" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,998,190,42"/>
<mxCell id="p2c_my_r2c4" value="materialize" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,998,230,42"/>
<mxCell id="p2c_my_r2c5" value="無 → 建；有 → 不納管；append 問後加" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,998,320,42"/>
<mxCell id="p2c_my_r2c6" value="—（日誌在 metadata [progress]）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,998,210,42"/>
<mxCell id="p2c_my_r2c6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,1000,30,20"/>
<mxCell id="p2c_my_r3c0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1040,130,26"/>
<mxCell id="p2c_my_r3c1" value="刪 &amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1040,250,26"/>
<mxCell id="p2c_my_r3c2" value="刪該工具所有 mod? 行" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1040,190,26"/>
<mxCell id="p2c_my_r3c3" value="刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1040,190,26"/>
<mxCell id="p2c_my_r3c4" value="刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1040,230,26"/>
<mxCell id="p2c_my_r3c5" value="永不刪；append 行問後刪（原文相同）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1040,320,26"/>
<mxCell id="p2c_my_r3c6" value=".tmp.remove.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1040,210,26"/>
<mxCell id="p2c_my_r3c6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,1042,30,20"/>
<mxCell id="p2c_my_r4c0" value="upgrade（工具）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1066,130,42"/>
<mxCell id="p2c_my_r4c1" value="推到新版（衝突仍推；解析失敗不推）+ metadata" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1066,250,42"/>
<mxCell id="p2c_my_r4c2" value="重生" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1066,190,42"/>
<mxCell id="p2c_my_r4c3" value="materialize 寫" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1066,190,42"/>
<mxCell id="p2c_my_r4c4" value="materialize" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1066,230,42"/>
<mxCell id="p2c_my_r4c5" value="逐檔問：換／三方合併／append 行替換／建新檔／二進位" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1066,320,42"/>
<mxCell id="p2c_my_r4c6" value="—（日誌在 metadata [progress]）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1066,210,42"/>
<mxCell id="p2c_my_r4c6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,1068,30,20"/>
<mxCell id="p2c_my_r5c0" value="upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1108,130,42"/>
<mxCell id="p2c_my_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,1110,30,20"/>
<mxCell id="p2c_my_r5c1" value="schema 遷移（dry-run 明列）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1108,250,42"/>
<mxCell id="p2c_my_r5c2" value="重生" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1108,190,42"/>
<mxCell id="p2c_my_r5c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1108,190,42"/>
<mxCell id="p2c_my_r5c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1108,230,42"/>
<mxCell id="p2c_my_r5c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1108,320,42"/>
<mxCell id="p2c_my_r5c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1108,210,42"/>
<mxCell id="p2c_my_r6c0" value="dev" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1150,130,26"/>
<mxCell id="p2c_my_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,1152,30,20"/>
<mxCell id="p2c_my_r6c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1150,250,26"/>
<mxCell id="p2c_my_r6c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1150,190,26"/>
<mxCell id="p2c_my_r6c3" value="寫 path:&amp;lt;dir&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1150,190,26"/>
<mxCell id="p2c_my_r6c4" value="改成 symlink → &amp;lt;dir&amp;gt;/dist" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1150,230,26"/>
<mxCell id="p2c_my_r6c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1150,320,26"/>
<mxCell id="p2c_my_r6c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1150,210,26"/>
<mxCell id="p2c_my_r7c0" value="undev" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1176,130,26"/>
<mxCell id="p2c_my_r7c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,1178,30,20"/>
<mxCell id="p2c_my_r7c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1176,250,26"/>
<mxCell id="p2c_my_r7c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1176,190,26"/>
<mxCell id="p2c_my_r7c3" value="重寫（materialize）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1176,190,26"/>
<mxCell id="p2c_my_r7c4" value="重新 materialize（經 docker）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1176,230,26"/>
<mxCell id="p2c_my_r7c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1176,320,26"/>
<mxCell id="p2c_my_r7c6" value=".tmp.undev.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1176,210,26"/>
<mxCell id="p2c_my_r8c0" value="sync" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1202,130,42"/>
<mxCell id="p2c_my_r8c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,1204,30,20"/>
<mxCell id="p2c_my_r8c1" value="—（只讀 complete、source 落後）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1202,250,42"/>
<mxCell id="p2c_my_r8c2" value="缺或需重生 → 重生" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1202,190,42"/>
<mxCell id="p2c_my_r8c3" value="materialize 時寫" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1202,190,42"/>
<mxCell id="p2c_my_r8c4" value="materialize／重裝（只拉鎖定版）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1202,230,42"/>
<mxCell id="p2c_my_r8c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1202,320,42"/>
<mxCell id="p2c_my_r8c6" value="—（有未完成 → 1 印 6-33 不恢復）" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1202,210,42"/>
<mxCell id="p2c_my_r9c0" value="update" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1244,130,26"/>
<mxCell id="p2c_my_r9c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1244,250,26"/>
<mxCell id="p2c_my_r9c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1244,190,26"/>
<mxCell id="p2c_my_r9c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1244,190,26"/>
<mxCell id="p2c_my_r9c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1244,230,26"/>
<mxCell id="p2c_my_r9c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1244,320,26"/>
<mxCell id="p2c_my_r9c6" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1244,210,26"/>
<mxCell id="p2c_my_r10c0" value="prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="20,1270,130,57"/>
<mxCell id="p2c_my_r10c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="118,1272,30,20"/>
<mxCell id="p2c_my_r10c1" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="150,1270,250,57"/>
<mxCell id="p2c_my_r10c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="400,1270,190,57"/>
<mxCell id="p2c_my_r10c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="590,1270,190,57"/>
<mxCell id="p2c_my_r10c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="780,1270,230,57"/>
<mxCell id="p2c_my_r10c5" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1010,1270,320,57"/>
<mxCell id="p2c_my_r10c6" value=".tmp.prune.&amp;lt;id&amp;gt;.toml；刪失效 .tmp.dist.*、已完成殘留；活躍的不刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p2C" geo="1330,1270,210,57"/>
<mxCell id="p2c_reno" value="&lt;b&gt;version.toml 怎麼被讀&lt;/b&gt;&lt;br&gt;・啟動器（sh）：以正規行 regex 於 version.local.toml（覆寫優先）→ version.toml 取 vendor_kit；命中數 ≠ 1 → 1；不解析 TOML（resolve 的 vk-resolve 才是它的輸入）；快路徑用 grep 比 gen/*.stamp&lt;br&gt;・引擎 version 模組：TOML 讀寫（schema 轉換）+ version.local.toml 覆寫；flock；apply 最後才寫 version.toml&lt;br&gt;・Renovate preset：regex manager（**/.vendor_kit/version.toml；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR&lt;br&gt;・deploy：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（工具契約一句；vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2C" geo="20,1341,750,155"/>
<mxCell id="p2c_reno_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="738,1343,30,20"/>
<mxCell id="p2c_rule" value="&lt;b&gt;規則摘要&lt;/b&gt;&lt;br&gt;・version.toml 是唯一來源：sync 拿它對印記，不一致就 materialize（只拉鎖定版）；apply 拿鎖後先重驗 resolve 給的輸入指紋，不同 → 1 印 6-12&lt;br&gt;・自動化（sync）只碰 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp：不碰使用者的檔、不寫薄殼、不寫 gen/.stamp；薄殼 ≠ 引擎 ref → 1 印 6-1（install／upgrade vendor_kit 不被擋）&lt;br&gt;・baseline 是上次合併的歷史狀態，不由 version.toml 推導（待合併時 version 已 B、baseline 仍 A）&lt;br&gt;・進 git 的只有：根 justfile 那行、根 .dockerignore 三行、.vendor_kit/（不含 cache/、gen/、version.local.toml、.tmp.*）、初始檔；人只改：justfile、初始檔、version.toml（手動升版）&lt;br&gt;・舊薄殼（--protocol P 太舊）跑新 major 引擎的一般動詞 → 3 零寫入（6-36）；救援路徑永遠可用" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p2C" geo="790,1341,750,155"/>
<mxCell id="p2c_rule_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p2C" geo="1508,1343,30,20"/>
<mxCell id="p2c_lg0" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="40,1642,190,40"/>
<mxCell id="p2c_lg1" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="250,1642,110,40"/>
<mxCell id="p2c_lg2" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="380,1642,200,40"/>
<mxCell id="p2c_lg3" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="600,1642,200,40"/>
<mxCell id="p2c_lg3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="768,1644,30,20"/>
<mxCell id="p2c_lg4" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="820,1642,220,40"/>
<mxCell id="p2c_lgt" value="表格：一列一動詞、一欄一檔&lt;br&gt;目錄樹與範例 p2、schema p2b" style="fillColor=none;strokeColor=none" geo="1060,1632,300,60"/>
<mxCell id="p2c_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1698,300,28"/>
<mxCell id="p2c_tk0" value="唯一來源" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1732,150,40"/>
<mxCell id="p2c_tv0" value="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1732,610,40"/>
<mxCell id="p2c_tk1" value="tracked 檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1772,150,40"/>
<mxCell id="p2c_tv1" value="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1772,610,40"/>
<mxCell id="p2c_tk2" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1812,150,55"/>
<mxCell id="p2c_tv2" value="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1812,610,55"/>
<mxCell id="p2c_tk3" value="輸入指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1867,150,55"/>
<mxCell id="p2c_tv3" value="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1867,610,55"/>
<mxCell id="p2c_tk4" value="進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1922,150,71"/>
<mxCell id="p2c_tv4" value="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1922,610,71"/>
<mxCell id="p2c_tk5" value="進度日誌檔 .tmp.*" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1993,150,55"/>
<mxCell id="p2c_tv5" value="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1993,610,55"/>
<mxCell id="p2c_tk6" value="救援路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2048,150,55"/>
<mxCell id="p2c_tv6" value="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2048,610,55"/>
<mxCell id="p2c_tk7" value="Renovate preset" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1732,150,55"/>
<mxCell id="p2c_tv7" value="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1732,610,55"/>
<mxCell id="p2c_tk8" value="deploy" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1787,150,40"/>
<mxCell id="p2c_tv8" value="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1787,610,40"/>
<mxCell id="p2c_tk9" value="根 justfile 四行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1827,150,55"/>
<mxCell id="p2c_tv9" value="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1827,610,55"/>
<mxCell id="p2c_tk10" value="根 .dockerignore 三行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1882,150,71"/>
<mxCell id="p2c_tv10" value="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1882,610,71"/>
<mxCell id="p2c_tk11" value="baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1953,150,40"/>
<mxCell id="p2c_tv11" value="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 兼作該工具目錄的佔位）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1953,610,40"/>
<mxCell id="p2c_tk12" value="declined／declined_hash" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1993,150,55"/>
<mxCell id="p2c_tv12" value="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1993,610,55"/>
</diagram>
<diagram id="v1p3" name="契約 v2：工具 repo 契約③">
<mxCell id="title" value="契約③ 工具 repo 要交的（供應側；interface_spec §4.7、§4.8、§3.6；改了要升 major 並公告）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p3_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p3_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;dist/files/ 的 symlink 已定禁止；dist 文字檔一律 LF、check.sh --dist 擋 CRLF 已定於 issue #29；Dockerfile.dist 必含 LABEL（16 條必修）" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,81"/>
<mxCell id="p3L4" value="契約③ 工具 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,109,1560,1120"/>
<mxCell id="p3_dist" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;&amp;lt;repo&amp;gt;/                  # 工具 repo&lt;br&gt;├─ dist/&lt;br&gt;│  ├─ files/…            # 全部出貨（原樣展開）&lt;br&gt;│  ├─ init.toml          # 初始檔清單（下表）&lt;br&gt;│  └─ just/&amp;lt;ns&amp;gt;.just     # 一檔一命名空間（含 _sync）&lt;br&gt;└─ Dockerfile.dist       # 逐字三行（下框）&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,50,440,108"/>
<mxCell id="p3_dock_l" value="Dockerfile.dist（逐字三行；純資料 image）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L4" geo="20,170,440,28"/>
<mxCell id="p3_dock" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;FROM scratch&lt;br&gt;LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1&lt;br&gt;COPY dist/ /dist/&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,202,440,61"/>
<mxCell id="d4_1" value="&lt;b&gt;dist/files/&lt;/b&gt;&lt;br&gt;全部出貨；materialize 原樣展開到 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/；symlink／hardlink／特殊檔第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF [#29]" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="480,50,253,155"/>
<mxCell id="d4_1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="701,52,30,20"/>
<mxCell id="d4_2" value="&lt;b&gt;dist/init.toml&lt;/b&gt;&lt;br&gt;schema、description（單行）、[[file]] src／dest／strategy=&quot;copy&quot;|&quot;append&quot;（預設 copy），dest 相對專案根；用 copy 指向根 .gitignore／.dockerignore／.editorconfig → --dist 報錯（要用 append）；欄位表見下" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="749,50,253,155"/>
<mxCell id="d4_2_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="970,52,30,20"/>
<mxCell id="d4_3" value="&lt;b&gt;dist/just/&amp;lt;ns&amp;gt;.just&lt;/b&gt;&lt;br&gt;每檔一個頂層命名空間，數量工具自決，&amp;lt;repo&amp;gt;.just 必須存在；每檔含私有 _sync（F1，見下）；撞名 → add 拒絕；recipe 用 cd {{quote(justfile_directory())}} 回專案根（禁止相對 working-directory）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="1018,50,253,155"/>
<mxCell id="d4_3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1239,52,30,20"/>
<mxCell id="d4_4" value="&lt;b&gt;Dockerfile.dist&lt;/b&gt;&lt;br&gt;逐字三行：FROM scratch／LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1／COPY dist/ /dist/；純資料，不承諾可執行、vendor_kit 不檢查 binary（Q21：只搬移）；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加，pull 無法追加）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="1287,50,253,155"/>
<mxCell id="d4_4_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1508,52,30,20"/>
<mxCell id="d4_5" value="&lt;b&gt;工具 image&lt;/b&gt;&lt;br&gt;ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;&lt;br&gt;多架構 amd64 + arm64（同一次 buildx、COPY-only；CI 驗兩平台位元組一致）；version.toml 與印記記 index digest（#26）；公開／私有自決（公開不可逆）；已釋出 image／index 子 digest 永不刪；LABEL …vendor_kit=1" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="p3L4" geo="480,221,253,186"/>
<mxCell id="d4_5_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="701,223,30,20"/>
<mxCell id="d4_6" value="&lt;b&gt;引擎 image&lt;/b&gt;&lt;br&gt;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN&lt;br&gt;公開；多架構（只驗兩平台 LABEL 一致）；LABEL …vendor_kit=1、.protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、.schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）；每平台 docker save tar + .digest 旁檔；Release 資產永不刪" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="p3L4" geo="749,221,253,186"/>
<mxCell id="d4_6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="970,223,30,20"/>
<mxCell id="d4_7" value="&lt;b&gt;工具 repo 的 CI&lt;/b&gt;&lt;br&gt;跑 vendor_kit 出貨的 check.sh --dist：dist 佈局、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink、LF、just 1.33.0 解析每個 &amp;lt;ns&amp;gt;.just、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台一致" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="1018,221,253,186"/>
<mxCell id="d4_7_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1239,223,30,20"/>
<mxCell id="d4_8" value="&lt;b&gt;deploy（一句話契約）&lt;/b&gt;&lt;br&gt;工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml、GHCR（需要的檔打包時複製進去）；vendor_kit 不檢查；保證方式 = 工具 repo 自己在乾淨機器解包驗收；version.toml 公開格式可供來源紀錄" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L4" geo="1287,221,253,186"/>
<mxCell id="d4_8_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1508,223,30,20"/>
<mxCell id="p3_dest" value="&lt;b&gt;dest 規則（引擎在任何寫入前驗，不只供應端 lint）&lt;/b&gt;：src 相對 dist/、正規化、不得越出 dist/；dest 相對專案根、正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；兩工具同 dest：copy/copy、copy/append → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查（含新版新增 &amp;lt;ns&amp;gt;／dest 的全域撞名）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L4" geo="20,423,1520,46"/>
<mxCell id="p3_dest_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1508,425,30,20"/>
<mxCell id="p3_init_l" value="dist/init.toml（逐字範例；欄位說明在下表）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L4" geo="20,483,700,28"/>
<mxCell id="p3_sync_l" value="dist/just/&amp;lt;ns&amp;gt;.just 的 _sync（逐字，行首真 tab）與 label 表" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L4" geo="790,483,700,28"/>
<mxCell id="p3_init" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1&lt;br&gt;description = &quot;&amp;lt;repo&amp;gt; 的專案範本與 just recipe&quot;&lt;br&gt;&lt;br&gt;[[file]]&lt;br&gt;src = &quot;files/Dockerfile&quot;&lt;br&gt;dest = &quot;Dockerfile&quot;&lt;br&gt;&lt;br&gt;[[file]]&lt;br&gt;src = &quot;files/gitignore.snippet&quot;&lt;br&gt;dest = &quot;.gitignore&quot;&lt;br&gt;strategy = &quot;append&quot;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,515,750,186"/>
<mxCell id="p3_sync" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;[private]&lt;br&gt;_sync:&lt;br&gt;&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; just vendor_kit sync&lt;br&gt;&lt;br&gt;build: _sync&lt;br&gt;&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; …&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="790,515,750,108"/>
<mxCell id="p3_initf_h0" value="欄位" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L4" geo="20,711,170,30"/>
<mxCell id="p3_initf_h1" value="型別／必填" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L4" geo="190,711,110,30"/>
<mxCell id="p3_initf_h2" value="說明" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L4" geo="300,711,470,30"/>
<mxCell id="p3_initf_r0c0" value="schema" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,741,170,26"/>
<mxCell id="p3_initf_r0c1" value="integer／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="190,741,110,26"/>
<mxCell id="p3_initf_r0c2" value="建置期契約（同 image 內讀寫），不進執行期矩陣" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="300,741,470,26"/>
<mxCell id="p3_initf_r1c0" value="description" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,767,170,42"/>
<mxCell id="p3_initf_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="158,769,30,20"/>
<mxCell id="p3_initf_r1c1" value="string／否" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="190,767,110,42"/>
<mxCell id="p3_initf_r1c2" value="頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod? 上方 # &amp;lt;description&amp;gt;；缺則 &amp;lt;repo&amp;gt; &amp;lt;tag&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="300,767,470,42"/>
<mxCell id="p3_initf_r2c0" value="[[file]].src" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,809,170,26"/>
<mxCell id="p3_initf_r2c1" value="string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="190,809,110,26"/>
<mxCell id="p3_initf_r2c2" value="相對 dist/；正規化、不得越出 dist/" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="300,809,470,26"/>
<mxCell id="p3_initf_r3c0" value="[[file]].dest" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,835,170,42"/>
<mxCell id="p3_initf_r3c1" value="string／是" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="190,835,110,42"/>
<mxCell id="p3_initf_r3c2" value="相對專案根；正規化、不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；跨工具撞 dest 規則見左" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="300,835,470,42"/>
<mxCell id="p3_initf_r4c0" value="[[file]].strategy" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="20,877,170,42"/>
<mxCell id="p3_initf_r4c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="158,879,30,20"/>
<mxCell id="p3_initf_r4c1" value="string／否" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="190,877,110,42"/>
<mxCell id="p3_initf_r4c2" value="&quot;copy&quot;（預設）或 &quot;append&quot;，只有這兩值；根 .gitignore／.dockerignore／.editorconfig 類必須用 append" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="300,877,470,42"/>
<mxCell id="p3_lbl_h0" value="資源" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L4" geo="790,633,200,30"/>
<mxCell id="p3_lbl_h1" value="label（鍵前綴 io.github.&amp;lt;org&amp;gt;.vendor_kit）" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L4" geo="990,633,540,30"/>
<mxCell id="p3_lbl_r0c0" value="啟動器建的容器／network／volume" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="790,663,200,42"/>
<mxCell id="p3_lbl_r0c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="958,665,30,20"/>
<mxCell id="p3_lbl_r0c1" value="…=1、….project=&amp;lt;專案根絕對路徑&amp;gt;（專案路徑 label 不加在 image 上）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="990,663,540,42"/>
<mxCell id="p3_lbl_r1c0" value="引擎 image（build 時）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="790,705,200,26"/>
<mxCell id="p3_lbl_r1c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="958,707,30,20"/>
<mxCell id="p3_lbl_r1c1" value="…=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="990,705,540,26"/>
<mxCell id="p3_lbl_r2c0" value="工具 image（build 時）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="790,731,200,26"/>
<mxCell id="p3_lbl_r2c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="958,733,30,20"/>
<mxCell id="p3_lbl_r2c1" value="…=1（Dockerfile.dist 必含）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="990,731,540,26"/>
<mxCell id="p3_lbl_r3c0" value="prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="790,757,200,42"/>
<mxCell id="p3_lbl_r3c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="958,759,30,20"/>
<mxCell id="p3_lbl_r3c1" value="依 label 掃四類資源；image 只刪帶 label 且本專案未引用者；vendor_kit 不建 network／volume（驗收差集為空，故意留的也要能刪）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L4" geo="990,757,540,42"/>
<mxCell id="p3_syncr" value="&lt;b&gt;sync 自動前置（F1 定案）&lt;/b&gt;：每個 dist/just/&amp;lt;ns&amp;gt;.just 必含上列私有 _sync（本體逐字、行首真 tab；justfile_directory() 在模組內 = 專案根；用 quote() 不直接插字串）；工具每個公開 recipe 相依它（例 build: _sync；例外集合：無）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump --dump-format json 檢查：_sync 存在、私有、本體逐字相符、每個公開 recipe 的 dependencies 含 _sync。限制（契約明寫）：just 在執行前已載入所有模組，同一次呼叫內看不到 sync 重建後的新 recipe；cache 缺檔時 mod? 讓 just vendor_kit sync 仍可進入；1.33.0 fixture 通過才算結案" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L4" geo="20,933,1520,61"/>
<mxCell id="p3_syncr_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1508,935,30,20"/>
<mxCell id="p3_con" value="&lt;b&gt;工具契約（初始檔與 recipe）&lt;/b&gt;：初始檔只能引用穩定入口 just &amp;lt;ns&amp;gt; …、.vendor_kit/ci/check.sh、.vendor_kit/entry.just、.vendor_kit/version.toml；不得寫死 cache 內部路徑（Q14）；rename／格式變更不得以 copy/append 假裝完成；工具的 build 若以專案根當 context，依賴 install 加進根 .dockerignore 的排除，不得再以其他方式繞過 .vendor_kit/；dist 可執行性是工具 repo 責任（check.sh --dist + 自己的測試）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L4" geo="20,1008,750,92"/>
<mxCell id="p3_con_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="738,1010,30,20"/>
<mxCell id="p3_off" value="&lt;b&gt;離線包（Release 資產；Q26）&lt;/b&gt;：每個平台 tar（docker save）旁附同名 .digest 旁檔：&amp;lt;name&amp;gt;.tar + &amp;lt;name&amp;gt;.tar.digest，內容一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；bootstrap.sh --local &amp;lt;tar&amp;gt;／add --local &amp;lt;tar&amp;gt;：docker load 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 local_image_id；旁檔缺 → 1。離線可用：啟動器先 docker image inspect，本機有就不 pull；斷網 + 已有 image → sync／build 必須成功；斷網 + 無 image → 1 印 6-31 不 hang；離線 upgrade 不支援" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L4" geo="790,1008,750,92"/>
<mxCell id="p3_off_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L4" geo="1508,1010,30,20"/>
<mxCell id="p3_lg0" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="40,1259,170,40"/>
<mxCell id="p3_lg1" value="等寬字：檔案內容範例" style="fillColor=#ffffff;strokeColor=#999999" geo="230,1259,170,40"/>
<mxCell id="p3_lg2" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="420,1259,190,40"/>
<mxCell id="p3_lg3" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="630,1259,110,40"/>
<mxCell id="p3_lg4" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="760,1259,200,40"/>
<mxCell id="p3_lg5" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="980,1259,200,40"/>
<mxCell id="p3_lg5_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1148,1261,30,20"/>
<mxCell id="p3_lgt" value="紫 = image（工具／引擎）&lt;br&gt;淺灰底容器 = 契約③ 全部" style="fillColor=none;strokeColor=none" geo="1200,1249,300,60"/>
<mxCell id="p3_lg6" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1325,220,40"/>
<mxCell id="p3_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1381,300,28"/>
<mxCell id="p3_tk0" value="dist/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1415,150,40"/>
<mxCell id="p3_tv0" value="工具 repo 出貨的目錄：files/（展開到 cache/&amp;lt;repo&amp;gt;/ 的全部）、init.toml（初始檔清單）、just/&amp;lt;ns&amp;gt;.just（工具自己的 recipe，每檔含 _sync）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1415,610,40"/>
<mxCell id="p3_tk1" value="Dockerfile.dist" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1455,150,55"/>
<mxCell id="p3_tv1" value="逐字三行：FROM scratch／LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1455,610,55"/>
<mxCell id="p3_tk2" value="label" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1510,150,55"/>
<mxCell id="p3_tv2" value="docker 資源上的鍵值標籤，鍵前綴 io.github.&amp;lt;org&amp;gt;.vendor_kit：容器／network／volume = 1 + .project=&amp;lt;專案根絕對路徑&amp;gt;；引擎 image = 1 + .protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt; + .schema=&amp;lt;N&amp;gt;；工具 image = 1；prune 依 label 掃" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1510,610,55"/>
<mxCell id="p3_tk3" value="dest" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1565,150,55"/>
<mxCell id="p3_tv3" value="init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1565,610,55"/>
<mxCell id="p3_tk4" value="strategy = &quot;append&quot;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1620,150,55"/>
<mxCell id="p3_tv4" value="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1620,610,55"/>
<mxCell id="p3_tk5" value="CRLF／LF" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1675,150,40"/>
<mxCell id="p3_tv5" value="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1675,610,40"/>
<mxCell id="p3_tk6" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1715,150,40"/>
<mxCell id="p3_tv6" value="指向另一個路徑的捷徑檔；dev 時 cache/&amp;lt;repo&amp;gt;/ 就是指向 &amp;lt;dir&amp;gt;/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1715,610,40"/>
<mxCell id="p3_tk7" value="_sync recipe（F1）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1755,150,55"/>
<mxCell id="p3_tv7" value="每個 dist/just/&amp;lt;ns&amp;gt;.just 必含的私有 recipe（逐字：[private] / _sync: / \tcd {{quote(justfile_directory())}} &amp;&amp; just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1755,610,55"/>
<mxCell id="p3_tk8" value="just 的兩個目錄函式" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1415,150,55"/>
<mxCell id="p3_tv8" value="justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1415,610,55"/>
<mxCell id="p3_tk9" value="buildx" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1470,150,28"/>
<mxCell id="p3_tv9" value="docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1470,610,28"/>
<mxCell id="p3_tk10" value="多架構 index／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1498,150,40"/>
<mxCell id="p3_tv10" value="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1498,610,40"/>
<mxCell id="p3_tk11" value="check.sh --dist" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1538,150,55"/>
<mxCell id="p3_tv11" value="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1538,610,55"/>
<mxCell id="p3_tk12" value=".digest 旁檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1593,150,55"/>
<mxCell id="p3_tv12" value="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1593,610,55"/>
<mxCell id="p3_tk13" value="離線可用（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1648,150,40"/>
<mxCell id="p3_tv13" value="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1648,610,40"/>
<mxCell id="p3_tk14" value="deploy" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1688,150,40"/>
<mxCell id="p3_tv14" value="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1688,610,40"/>
<mxCell id="p3_tk15" value="命名空間" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1728,150,40"/>
<mxCell id="p3_tv15" value="just &amp;lt;ns&amp;gt; &amp;lt;recipe&amp;gt; 前面那個 &amp;lt;ns&amp;gt;；每個工具的 just/&amp;lt;ns&amp;gt;.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1728,610,40"/>
<mxCell id="p3_tk16" value="SemVer／正式版" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1768,150,40"/>
<mxCell id="p3_tv16" value="版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高 floor 或需手動步驟" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1768,610,40"/>
</diagram>
<diagram id="v1p3b" name="契約 v2：啟動器 ↔ 引擎契約④">
<mxCell id="title" value="契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p3b_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p3b_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;vk-resolve/1 文法（Q24）；主機命令白名單（16 條必修）；規則框逐條對應 interface_spec §3、§5，皆已定" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,65"/>
<mxCell id="p3L2" value="契約④ 啟動器 ↔ 引擎（每格一件事；① 啟動器 grep → ② resolve → ③ 主機 docker → ④ apply；規則框 = §3、§5 逐條）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,96,1560,1725.5"/>
<mxCell id="s1" value="① 以正規行 regex grep 引擎 ref&lt;br&gt;（version.local.toml 覆寫優先；命中 ≠ 1 → 1）&lt;br&gt;下一格 install／upgrade vendor_kit 跳過" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L2" geo="30,60.5,190,108"/>
<mxCell id="d1" value="gen/.stamp&lt;br&gt;= 引擎 ref？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="p3L2" geo="244,56.5,180,116"/>
<mxCell id="d1_e" edge="1" source="s1" target="d1"/>
<mxCell id="g2" value="② docker run 引擎 resolve &amp;lt;動詞&amp;gt;（只讀、不寫檔、無 TTY；診斷走 stderr）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" parent="p3L2" geo="448,50.0,650,103"/>
<mxCell id="s2a" value="讀 version.toml／local&lt;br&gt;（CI 為真 → frozen）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g2" geo="8,34.0,160,61"/>
<mxCell id="s2b" value="查 registry 最新 tag／digest&lt;br&gt;（frozen／@&amp;lt;tag&amp;gt; 不查）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g2" geo="184,34.0,180,61"/>
<mxCell id="s2c" value="stdout vk-resolve/1&lt;br&gt;（pull／extract／mount／engine／fingerprint／apply／end）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g2" geo="380,34.0,250,61"/>
<mxCell id="s2a_e" value="是" edge="1" source="d1" target="s2a"/>
<mxCell id="s2b_e" edge="1" source="s2a" target="s2b"/>
<mxCell id="s2c_e" edge="1" source="s2b" target="s2c"/>
<mxCell id="p3_err" value="否 → 1 印 6-1&lt;br&gt;（請 upgrade vendor_kit；不重寫薄殼）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L2" geo="204.0,212.5,260,84"/>
<mxCell id="p3_err_e" value="否" edge="1" source="d1" target="p3_err"/>
<mxCell id="d2" value="apply|yes？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="p3L2" geo="488.0,250.0,180,85"/>
<mxCell id="g3" value="③ 主機 docker（每筆 pull／extract；不帶 --platform；先收完 vk-resolve 驗文法才動）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" parent="p3L2" geo="692.0,212.5,622,134"/>
<mxCell id="s3a" value="docker image inspect&lt;br&gt;（有 → 不 pull）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g3" geo="8,41.5,110,77"/>
<mxCell id="s3b" value="docker pull&lt;br&gt;（逾時 → 1 印 6-31）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g3" geo="134,49.5,100,61"/>
<mxCell id="s3c" value="docker create&lt;br&gt;（帶 label）&amp;lt;ref&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g3" geo="250,41.5,100,77"/>
<mxCell id="s3d" value="docker cp c:/dist/.&lt;br&gt;→ .tmp.dist.&amp;lt;id&amp;gt;/&lt;br&gt;&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g3" geo="366,34.0,130,92"/>
<mxCell id="s3e" value="docker rm&lt;br&gt;（trap 也清）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="g3" geo="512,49.5,90,61"/>
<mxCell id="s4" value="④ docker run 引擎&lt;br&gt;apply &amp;lt;動詞&amp;gt;（掛 /dist:ro）&lt;br&gt;→ 結束碼 0／1／2／3 回 just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L2" geo="1338.0,246.5,180,92"/>
<mxCell id="s3b_e" edge="1" source="s3a" target="s3b"/>
<mxCell id="s3c_e" edge="1" source="s3b" target="s3c"/>
<mxCell id="s3d_e" edge="1" source="s3c" target="s3d"/>
<mxCell id="s3e_e" edge="1" source="s3d" target="s3e"/>
<mxCell id="s4_e" edge="1" source="s3e" target="s4"/>
<mxCell id="d2_e" value="是" edge="1" source="d2" target="s3a"/>
<mxCell id="d2_in" value="③" edge="1" source="s2c" target="d2"/>
<mxCell id="p3_ok" value="否（apply|no）→ 0 快路徑&lt;br&gt;不起第二個容器" style="fillColor=#d5e8d4;strokeColor=#000000" parent="p3L2" geo="448.0,370.5,260,62"/>
<mxCell id="p3_ok_e" value="否" edge="1" source="d2" target="p3_ok"/>
<mxCell id="p3_sh" value="&lt;b&gt;主機命令白名單（16 條必修；lint 擋清單外）&lt;/b&gt;：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files。啟動器 = POSIX sh（vendor.just 內的 recipe 殼）：不裝 python、不解析 TOML、不 eval；路徑含空白、$、非 ASCII 一律引號" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,456.5,750,92"/>
<mxCell id="p3_sh_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="748,458.5,30,20"/>
<mxCell id="p3_uf" value="&lt;b&gt;使用者旗標（rootless 不加 -u／Podman keep-id）&lt;/b&gt;：docker info --format &#x27;{{.SecurityOptions}}&#x27; 含 name=rootless → rootless，不加 -u；docker --version 含 podman → 加 --userns=keep-id、不加 -u；其餘（rootful docker）加 -u &quot;$(id -u):$(id -g)&quot;" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="790,456.5,750,92"/>
<mxCell id="p3_uf_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,458.5,30,20"/>
<mxCell id="p3_run" value="&lt;b&gt;docker run 參數&lt;/b&gt;：docker run --rm [&amp;lt;使用者旗標&amp;gt;] -v &quot;&amp;lt;專案根&amp;gt;:/repo&quot; -w /repo [-v &quot;&amp;lt;專案根&amp;gt;/.vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;:/dist:ro&quot;] [-v &quot;&amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro&quot;]… [-v &quot;&amp;lt;TOKEN_FILE&amp;gt;:/run/vk-token:ro&quot; -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.&amp;lt;org&amp;gt;.vendor_kit=1 --label io.github.&amp;lt;org&amp;gt;.vendor_kit.project=&amp;lt;專案根絕對路徑&amp;gt; &amp;lt;引擎 ref&amp;gt; --protocol P &amp;lt;子命令&amp;gt; [args]。--protocol P 一律在子命令之前；-w /repo 必給；-it 只在 apply 且互動（有 tty、無 -y、非 frozen），resolve 永不 -t；trap … EXIT INT TERM 清容器與 .tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,562.5,750,124"/>
<mxCell id="p3_run_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="748,564.5,30,20"/>
<mxCell id="p3_envw" value="&lt;b&gt;環境變數與 -e 白名單（§5）&lt;/b&gt;：轉發 CI（照原值；真值規則：非空且不為 0／false → frozen）、VENDOR_KIT_NO_LOCK（=1 跳過 flock）；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update／upgrade 的 resolve 階段以 -e 傳（不寫 log／檔、不傳給工具、dry-run 不印）；VENDOR_KIT_REGISTRY_TOKEN_FILE 改為 -v &amp;lt;主機檔&amp;gt;:/run/vk-token:ro 並以 -e …_TOKEN_FILE=/run/vk-token 傳容器內路徑（與 _TOKEN 同設 → 1「只能擇一」）；啟動器自讀不轉發：VENDOR_KIT_PULL_TIMEOUT（預設 300，--timeout 優先）；其餘一律不轉發（HTTP_PROXY 等 → v2）；README 列出全部 VENDOR_KIT_* 與 CI，lint 擋未列者；引擎容器內 LC_ALL=C.UTF-8、TZ=UTC、HOME=&amp;lt;容器內暫存&amp;gt;" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="790,562.5,750,124"/>
<mxCell id="p3_envw_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,564.5,30,20"/>
<mxCell id="p3_img" value="&lt;b&gt;引擎 image 取得&lt;/b&gt;：一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull &amp;lt;ref&amp;gt;（逾時）。local 覆寫時：docker image inspect &amp;lt;tag&amp;gt; 的 .Id 必須 == version.local.toml vendor_kit_image_id，否則 1；不 pull（不用 docker run 的 pull 旗標：docker 19.03 沒有）。&lt;b&gt;引擎子命令&lt;/b&gt;：單段 install／update／dev／help／upgrade vendor_kit[@&amp;lt;tag&amp;gt;] = --protocol P &amp;lt;verb&amp;gt; [args]；resolve &amp;lt;verb&amp;gt;（只讀、不詢問、不寫檔、無 TTY）；apply &amp;lt;verb&amp;gt; [--dry-run]；內部 materialize／verify／merge 不對外" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,700.5,750,139"/>
<mxCell id="p3_img_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="748,702.5,30,20"/>
<mxCell id="p3_two" value="&lt;b&gt;兩段編排的兩個獨立屬性&lt;/b&gt;：需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve &amp;lt;verb&amp;gt; → 主機 docker → apply &amp;lt;verb&amp;gt;，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）。&lt;b&gt;鎖&lt;/b&gt;：鎖在引擎 version 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗印 6-26；VENDOR_KIT_NO_LOCK=1 跳過；啟動器不鎖）。&lt;b&gt;pull 失敗&lt;/b&gt;：印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列「主機錯誤」）+ 僅 add／bootstrap 提示 6-24 的「離線可用 --local」；&lt;b&gt;逾時&lt;/b&gt;：VENDOR_KIT_PULL_TIMEOUT／--timeout，預設 300 秒，只收正整數（0 或非數字 → 1）；背景 pull + 每秒輪詢 + kill；逾時 → 1 印 6-31" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="790,700.5,750,139"/>
<mxCell id="p3_two_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,702.5,30,20"/>
<mxCell id="p3_lock" value="&lt;b&gt;apply 通則（所有動詞）&lt;/b&gt;：讀 /dist/vk-resolve（啟動器把 resolve 原始 stdout 存成 .tmp.dist.&amp;lt;id&amp;gt;/vk-resolve 一起掛入）→ 拿 flock → 重算指紋與計畫中的 fingerprint 比對（不同 → 1 印 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 為真需改 tracked → 1 印清單）→ 建進度日誌（第一個寫入前）→ 其後所有寫入（清除衝突狀態、append、baseline、metadata、cache、tools.just；version.toml 最後）→ 最後一步刪日誌（uninstall 在根 justfile 那行之後）；不重新選最新版；詢問後、替換前對目標檔再查一次前像；所有合併在暫存完成 → 逐檔原子替換；失敗明列已完成／未完成" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,853.5,1510,61"/>
<mxCell id="p3_lock_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,855.5,30,20"/>
<mxCell id="p3_vk_l" value="vk-resolve/1 stdout 文法（Q24；P=1）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L2" geo="30,928.5,700,28"/>
<mxCell id="p3_vkt_l" value="kind 一覽（啟動器動作）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L2" geo="790,928.5,700,28"/>
<mxCell id="p3_vk" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vk-resolve/&amp;lt;P&amp;gt;&lt;br&gt;&amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]&lt;br&gt;end|&amp;lt;N&amp;gt;&lt;br&gt;&lt;br&gt;vk-resolve/1&lt;br&gt;extract|&amp;lt;repo&amp;gt;|ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:v2.3.0@sha256:bbbb…&lt;br&gt;fingerprint|1c0e…77&lt;br&gt;apply|yes&lt;br&gt;end|3&lt;br&gt;&lt;br&gt;vk-resolve/1&lt;br&gt;mount|&amp;lt;repo&amp;gt;|/home/me/my\0040tools&lt;br&gt;fingerprint|9a2f…c1&lt;br&gt;apply|yes&lt;br&gt;end|3&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="30,960.5,750,248"/>
<mxCell id="p3_vk_n" value="上段 = 文法骨架：第一行 vk-resolve/&amp;lt;P&amp;gt;（P = 呼叫方 --protocol 的值）；每行一筆 &amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]（欄位以單一 | 分隔；UTF-8；LF；無空行、無註解；禁 CR／NUL／BOM）；最後一行 end|&amp;lt;N&amp;gt;（N = 記錄行數，之後立即 EOF）&lt;br&gt;中段範例 = sync，&amp;lt;repo&amp;gt; 的 cache 過期（extract）；下段範例 = sync，&amp;lt;repo&amp;gt; 在 dev 覆寫中（mount；路徑含空白 → \0040）。範例工具名一律 &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="30,1216.5,750,77"/>
<mxCell id="p3_vkt_h0" value="kind" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L2" geo="790,960.5,100,30"/>
<mxCell id="p3_vkt_h1" value="欄位" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L2" geo="890,960.5,180,30"/>
<mxCell id="p3_vkt_h2" value="筆數" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L2" geo="1070,960.5,50,30"/>
<mxCell id="p3_vkt_h3" value="啟動器動作" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L2" geo="1120,960.5,420,30"/>
<mxCell id="p3_vkt_r0c0" value="pull" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,990.5,100,42"/>
<mxCell id="p3_vkt_r0c1" value="&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,990.5,180,42"/>
<mxCell id="p3_vkt_r0c2" value="0..n" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,990.5,50,42"/>
<mxCell id="p3_vkt_r0c3" value="docker image inspect 有則略，否則 docker pull &amp;lt;ref&amp;gt;（逾時／失敗 → 6-24／6-31）；name = vendor_kit 或 &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,990.5,420,42"/>
<mxCell id="p3_vkt_r1c0" value="extract" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1032.5,100,57"/>
<mxCell id="p3_vkt_r1c1" value="&amp;lt;repo&amp;gt;|&amp;lt;ref&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1032.5,180,57"/>
<mxCell id="p3_vkt_r1c2" value="0..n" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1032.5,50,57"/>
<mxCell id="p3_vkt_r1c3" value="同 pull 後 docker create … &amp;lt;ref&amp;gt; /x → docker cp c:/dist/. &quot;.tmp.dist.&amp;lt;id&amp;gt;/&amp;lt;repo&amp;gt;/&quot; → docker rm；同一 repo 不得同時有 extract 與 mount" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1032.5,420,57"/>
<mxCell id="p3_vkt_r2c0" value="mount" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1089.5,100,42"/>
<mxCell id="p3_vkt_r2c1" value="&amp;lt;repo&amp;gt;|&amp;lt;dir 八進位跳脫&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1089.5,180,42"/>
<mxCell id="p3_vkt_r2c2" value="0..n" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1089.5,50,42"/>
<mxCell id="p3_vkt_r2c3" value="dev 覆寫：解碼後驗 &amp;lt;dir&amp;gt;/dist/init.toml 存在（缺 → 1）→ -v &quot;&amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro&quot;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1089.5,420,42"/>
<mxCell id="p3_vkt_r3c0" value="engine" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1131.5,100,57"/>
<mxCell id="p3_vkt_r3c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="858,1133.5,30,20"/>
<mxCell id="p3_vkt_r3c1" value="&amp;lt;ref&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1131.5,180,57"/>
<mxCell id="p3_vkt_r3c2" value="0..1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1131.5,50,57"/>
<mxCell id="p3_vkt_r3c3" value="只在 upgrade（不帶 repo）：apply 會把正規行改成此 ref；啟動器先 pull（或 local 覆寫時 inspect 驗 ID）；有 engine 時本次不得夾帶工具寫入" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1131.5,420,57"/>
<mxCell id="p3_vkt_r4c0" value="fingerprint" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1188.5,100,26"/>
<mxCell id="p3_vkt_r4c1" value="&amp;lt;sha256 hex64&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1188.5,180,26"/>
<mxCell id="p3_vkt_r4c2" value="恰 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1188.5,50,26"/>
<mxCell id="p3_vkt_r4c3" value="不解析，隨檔交給 apply" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1188.5,420,26"/>
<mxCell id="p3_vkt_r5c0" value="apply" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1214.5,100,57"/>
<mxCell id="p3_vkt_r5c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="858,1216.5,30,20"/>
<mxCell id="p3_vkt_r5c1" value="yes | no" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1214.5,180,57"/>
<mxCell id="p3_vkt_r5c2" value="恰 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1214.5,50,57"/>
<mxCell id="p3_vkt_r5c3" value="no → 驗完文法後直接 exit 0（sync 快路徑）；no 時不得有 pull／extract／mount／engine；yes → docker 階段後跑 apply &amp;lt;verb&amp;gt; [--dry-run] [args]" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1214.5,420,57"/>
<mxCell id="p3_vkt_r6c0" value="keep" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1271.5,100,42"/>
<mxCell id="p3_vkt_r6c0_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="858,1273.5,30,20"/>
<mxCell id="p3_vkt_r6c1" value="&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1271.5,180,42"/>
<mxCell id="p3_vkt_r6c2" value="0..n" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1271.5,50,42"/>
<mxCell id="p3_vkt_r6c3" value="只在 prune：本專案引用、不可刪的 image（含 local 覆寫的 &amp;lt;tag&amp;gt;）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1271.5,420,42"/>
<mxCell id="p3_vkt_r7c0" value="end" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="790,1313.5,100,26"/>
<mxCell id="p3_vkt_r7c1" value="&amp;lt;N&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="890,1313.5,180,26"/>
<mxCell id="p3_vkt_r7c2" value="恰 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1070,1313.5,50,26"/>
<mxCell id="p3_vkt_r7c3" value="必為最後一行" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L2" geo="1120,1313.5,420,26"/>
<mxCell id="p3_vkr" value="&lt;b&gt;欄位與驗證&lt;/b&gt;：安全字串 [A-Za-z0-9_.-]+；ref [A-Za-z0-9_.:/@-]+（引擎以 image-reference parser 驗證後才輸出）；自由文字（路徑）凡不在 [A-Za-z0-9_./:@+=,-] 的 byte 一律寫成 \0ooo（例：空白 \0040、| \0174、\ \0134），啟動器一行解碼 dir=$(printf &#x27;%b&#x27; &quot;$f2&quot;)、不 eval、不 source；IFS=&#x27;|&#x27; read -r 直接切欄。啟動器先收完整份存到 .tmp.dist.&amp;lt;id&amp;gt;/vk-resolve、驗文法才動 docker：首行 ≠ vk-resolve/&amp;lt;P&amp;gt;、缺 end、N 不符、end 後仍有資料、未知 kind、欄位數不對、fingerprint／apply 不是恰一筆、no 卻附動作記錄、安全字串含非法字元 → 1 印 6-30；引擎宣稱的 P 真不支援 → 3。resolve 結束碼非 0 → 不讀 stdout、原碼傳出。stderr 一律診斷；apply 的 stdout 不作為協定通道。指紋算法見名詞表" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,1353.5,1510,77"/>
<mxCell id="p3_vkr_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,1355.5,30,20"/>
<mxCell id="p3_self" value="&lt;b&gt;自身升級的接手（§3.4）&lt;/b&gt;：「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行。apply 結束後 ref 變了（且 == 計畫的 engine）→ 以新 ref（local 覆寫有 vendor_kit= 則用該 image、inspect 驗 ID）跑 docker run … &amp;lt;新 ref&amp;gt; --protocol P upgrade vendor_kit，結束碼原樣傳出（預期 1 印 6-2）；第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b，不再重跑。&lt;b&gt;救援路徑（§3.5）&lt;/b&gt;：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help = 單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼永遠可經此叫任何引擎重產薄殼" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,1444.5,750,139"/>
<mxCell id="p3_self_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="748,1446.5,30,20"/>
<mxCell id="p3_fast" value="&lt;b&gt;sync 快路徑（Q22）與 sync --verify&lt;/b&gt;：sync（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml vendor_kit ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 frozen → 起引擎 resolve sync。每檔 sha256 verify 只在：CI 為真（frozen）、快路徑有差那次（版本變動）、sync --verify（長形）；sync &amp;lt;repo&amp;gt; 一律起引擎驗該範圍。前提：.vendor_kit/.gitignore 明列 cache/、gen/、version.local.toml、.tmp.*；install 把 .vendor_kit/cache/、gen/、.tmp.* 加進根 .dockerignore。&lt;b&gt;--local 值的判別&lt;/b&gt;：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立 → 1 提示用 ./ 或完整 ref 消歧" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="790,1444.5,750,139"/>
<mxCell id="p3_fast_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,1446.5,30,20"/>
<mxCell id="p3_compat" value="&lt;b&gt;相容承諾（Q16／Q19／Q23）&lt;/b&gt;：薄殼每次呼叫附 --protocol P（第一版就有），引擎依 P 回應。永久：任何 ≥ floor 的舊薄殼可呼叫新引擎的救援路徑並得正確提示；舊資料永遠可讀可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 3 印 6-36 零寫入。floor = 固定 release 常數（v1.0.0、P=1、schema=1），只能經 ADR 提高；引擎 image LABEL …protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt; 讓啟動器不起容器即可判 floor。降版 upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 P／schema 比）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10；dev vendor_kit -i &amp;lt;舊 image&amp;gt; 禁止重產 tracked 薄殼" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="30,1597.5,750,108"/>
<mxCell id="p3_compat_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="748,1599.5,30,20"/>
<mxCell id="p3_env" value="&lt;b&gt;執行環境（19 條）與主機需求&lt;/b&gt;：docker ≥ 19.03（或 Podman ≥ 4.9）、just ≥ 1.33.0、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA、引擎基底 EOL → issue v2。時間戳 UTC ISO 8601；需詢問但無 tty／EOF → 1 印 6-4；所有 docker 資源帶 vendor_kit label；不建 network／volume；離線 upgrade 不支援；worktree 進驗收；submodule 以實測為生效條件" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L2" geo="790,1597.5,750,108"/>
<mxCell id="p3_env_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L2" geo="1508,1599.5,30,20"/>
<mxCell id="p3b_lg0" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="40,1851.5,200,40"/>
<mxCell id="p3b_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000;fontSize=14" geo="260,1841.5,150,66"/>
<mxCell id="p3b_lg2" value="橙橢圓：需要人動作（1／3 印指令、2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="430,1843.5,400,56"/>
<mxCell id="p3b_lg3" value="綠橢圓：成功終點（exit 0）" style="fillColor=#d5e8d4;strokeColor=#000000" geo="850,1845.5,270,52"/>
<mxCell id="p3b_lg4" value="白：步驟／說明" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1140,1851.5,130,40"/>
<mxCell id="p3b_lgt" value="實線 = 執行順序；線上文字 = 條件／接續編號&lt;br&gt;淺灰底容器 = ②③ 的分組（標題 = 該段做的事）" style="fillColor=none;strokeColor=none" geo="1290,1841.5,300,60"/>
<mxCell id="p3b_lg5" value="等寬字：檔案內容範例" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1917.5,170,40"/>
<mxCell id="p3b_lg6" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="230,1917.5,190,40"/>
<mxCell id="p3b_lg7" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="440,1917.5,110,40"/>
<mxCell id="p3b_lg8" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="570,1917.5,200,40"/>
<mxCell id="p3b_lg8_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="738,1919.5,30,20"/>
<mxCell id="p3b_lg9" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="790,1917.5,220,40"/>
<mxCell id="p3b_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1973.5,300,28"/>
<mxCell id="p3b_tk0" value="啟動器" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2007.5,150,55"/>
<mxCell id="p3b_tv0" value=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2007.5,610,55"/>
<mxCell id="p3b_tk1" value="主機命令白名單" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2062.5,150,71"/>
<mxCell id="p3b_tv1" value="啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files；lint 擋清單外" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2062.5,610,71"/>
<mxCell id="p3b_tk2" value="docker image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2133.5,150,55"/>
<mxCell id="p3b_tv2" value="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2133.5,610,55"/>
<mxCell id="p3b_tk3" value="docker create／cp" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2188.5,150,55"/>
<mxCell id="p3b_tv3" value="不執行容器，只建一個容器殼（docker create &amp;lt;ref&amp;gt; /x）再把 /dist 複製出來（docker cp c:/dist/. …）→ docker rm；純資料 image 沒有程式所以不能 docker run；不帶 --platform（daemon 挑原生）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2188.5,610,55"/>
<mxCell id="p3b_tk4" value="暫存 .tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2243.5,150,40"/>
<mxCell id="p3b_tv4" value="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2243.5,610,40"/>
<mxCell id="p3b_tk5" value="使用者旗標（-u）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2007.5,150,55"/>
<mxCell id="p3b_tv5" value="rootful docker 加 -u &quot;$(id -u):$(id -g)&quot;（寫出的檔才不會變 root 的）；rootless docker（docker info SecurityOptions 含 name=rootless）不加 -u；Podman（docker --version 含 podman）改加 --userns=keep-id、不加 -u" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2007.5,610,55"/>
<mxCell id="p3b_tk6" value="REGISTRY_TOKEN／&lt;br&gt;_TOKEN_FILE" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2062.5,150,55"/>
<mxCell id="p3b_tv6" value="私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v &amp;lt;file&amp;gt;:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt; 指定版本（主機 docker pull 走主機認證）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2062.5,610,55"/>
<mxCell id="p3b_tk7" value="vk-resolve/1" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2117.5,150,55"/>
<mxCell id="p3b_tv7" value="resolve 的 stdout 文法：首行 vk-resolve/&amp;lt;P&amp;gt;、每行 &amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]（欄位以單一 | 分隔）、末行 end|&amp;lt;N&amp;gt;；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \0ooo 八進位跳脫（printf &#x27;%b&#x27; 可解）；啟動器先收完整份、驗文法才動 docker" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2117.5,610,55"/>
<mxCell id="p3b_tk8" value="輸入指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2172.5,150,55"/>
<mxCell id="p3b_tv8" value="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2172.5,610,55"/>
</diagram>
<diagram id="v1p3c" name="契約 v2：CI 契約⑤ 與驗收矩陣">
<mxCell id="title" value="契約⑤ CI 與驗收矩陣（interface_spec §7；下游 check.sh；工具 repo check.sh --dist；自身分層 + 驗收 28 條）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p3c_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p3c_pend" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 每條一情境" style="fillColor=#ffffff;strokeColor=#999999" geo="1260,12,340,81"/>
<mxCell id="p3L5" value="契約⑤ CI（下游 check.sh 六步 + Renovate；工具 repo check.sh --dist；vendor_kit 自身分層 + 驗收矩陣）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,109,1560,1547"/>
<mxCell id="p3_k0" value="下游專案 CI：只呼叫 .vendor_kit/ci/check.sh，一關過才下一關（每格一步）" style="fillColor=none;strokeColor=none" parent="p3L5" geo="20,50,200,60"/>
<mxCell id="k0" value="⓪ version.local.toml 被 git track？" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="240,50,190,60"/>
<mxCell id="k1" value="① sync（frozen）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="446,50,120,60"/>
<mxCell id="k1_e" edge="1" source="k0" target="k1"/>
<mxCell id="k2" value="② verify（印記 sha256，全部工具）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="582,50,170,60"/>
<mxCell id="k2_e" edge="1" source="k1" target="k2"/>
<mxCell id="k3" value="③ upgrade --dry-run" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="768,50,150,60"/>
<mxCell id="k3_e" edge="1" source="k2" target="k3"/>
<mxCell id="k4" value="④ 工具測試 just &amp;lt;repo&amp;gt; check（若有；不得再呼叫 check.sh）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="934,50,250,60"/>
<mxCell id="k4_e" edge="1" source="k3" target="k4"/>
<mxCell id="k5" value="⑤ 專案測試（just check 若有）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="1200,50,170,60"/>
<mxCell id="k5_e" edge="1" source="k4" target="k5"/>
<mxCell id="k6" value="全部通過 → 0" style="fillColor=#d5e8d4;strokeColor=#000000" parent="p3L5" geo="1386,50,130,60"/>
<mxCell id="k6_e" edge="1" source="k5" target="k6"/>
<mxCell id="k0f" value="命中 → 1 拒絕&lt;br&gt;（請勿把 local 覆寫提交）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L5" geo="235.0,150,200,84"/>
<mxCell id="k0f_e" value="命中" edge="1" source="k0" target="k0f"/>
<mxCell id="k1f" value="1：薄殼不符（6-1）、未完成接入（6-13）、baseline 落後（6-5）、任何 local 覆寫；3" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L5" geo="416.0,254,300,84"/>
<mxCell id="k1f_e" value="升為失敗" edge="1" source="k1" target="k1f"/>
<mxCell id="k3f" value="CI 為真且需改 tracked 檔&lt;br&gt;→ 1 印清單（version.toml 不動；與 -y 無關）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L5" geo="763.0,150,280,84"/>
<mxCell id="k3f_e" value="需改檔" edge="1" source="k3" target="k3f"/>
<mxCell id="k3g" value="仍有衝突標記 → 2；印 6-6～6-8 但不紅燈" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L5" geo="1063.0,150,260,62"/>
<mxCell id="k3g_e" value="衝突" edge="1" source="k3" target="k3g"/>
<mxCell id="p3_kr" value="&lt;b&gt;check.sh（§7.1）&lt;/b&gt;：第一行 shebang、第二行自描述、其後第一個動作 export CI=1；GitHub／GitLab 一樣、平台無關；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L5" geo="20,362,1520,46"/>
<mxCell id="p3_kr_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="1508,364,30,20"/>
<mxCell id="p3_rn_l" value="Renovate 路徑（PR 需合併時；補合併在 PR 分支完成、CI 綠後才 merge）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L5" geo="20,422,1000,28"/>
<mxCell id="rn1" value="Renovate PR 改 version.toml 一行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="20,454,170,64"/>
<mxCell id="rn2" value="PR 的 CI 以新版跑 check.sh 完整流程（一行改動本身不構成通過依據）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="206,454,260,64"/>
<mxCell id="rn2_e" edge="1" source="rn1" target="rn2"/>
<mxCell id="rn3" value="需合併 → 1 印 6-5" style="fillColor=#ffe6cc;strokeColor=#000000" parent="p3L5" geo="482,454,140,64"/>
<mxCell id="rn3_e" edge="1" source="rn2" target="rn3"/>
<mxCell id="rn4" value="維護者在 PR 分支本機 upgrade &amp;lt;repo&amp;gt; -y → commit → push" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="638,454,240,64"/>
<mxCell id="rn4_e" edge="1" source="rn3" target="rn4"/>
<mxCell id="rn5" value="CI 全部再跑（Renovate 不動有人推過的分支）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="894,454,220,64"/>
<mxCell id="rn5_e" edge="1" source="rn4" target="rn5"/>
<mxCell id="rn6" value="綠了才 merge" style="fillColor=#d5e8d4;strokeColor=#000000" parent="p3L5" geo="1130,454,110,64"/>
<mxCell id="rn6_e" edge="1" source="rn5" target="rn6"/>
<mxCell id="p3_c2" value="&lt;b&gt;Renovate preset（§7.3；下游自選，vendor_kit 不出 bot）&lt;/b&gt;：放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；下游 extends: [&quot;github&amp;gt;ycpss91255-research/vendor_kit&quot;]；regex manager 匹配 **/.vendor_kit/version.toml（monorepo 子專案亦命中；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR（matchUpdateTypes）；hostRules 依 host 不寫死 ghcr.io；prBodyNotes = 6-25（6-5 的指令 + 「推 commit 後不要勾 rebase/retry」）；不設 gitIgnoredAuthors、不改 rebaseWhen；postUpgradeTasks 不採" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L5" geo="20,534,1000,155"/>
<mxCell id="p3_c2_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="988,536,30,20"/>
<mxCell id="p3_c3" value="&lt;b&gt;工具 repo 的 CI：check.sh --dist（§7.2）&lt;/b&gt;：dist 佈局（files/、init.toml、just/&amp;lt;repo&amp;gt;.just 存在）、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗 [#29]）、以 just 1.33.0 解析每個 &amp;lt;ns&amp;gt;.just（並擋比 1.33 新的功能）、_sync lint（just --dump --dump-format json）、Dockerfile.dist 含 LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L5" geo="1040,534,500,155"/>
<mxCell id="p3_c3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="1508,536,30,20"/>
<mxCell id="p3_c0" value="vendor_kit 自身 CI（分層，一關過才下一關；每格一個檢查）" style="fillColor=none;strokeColor=none" parent="p3L5" geo="20,713,180,60"/>
<mxCell id="c_a" value="env-test" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="210,713,84,60"/>
<mxCell id="c_b" value="test-base" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="310,713,84,60"/>
<mxCell id="c_b_e" edge="1" source="c_a" target="c_b"/>
<mxCell id="c_c1" value="lint" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="410,713,84,60"/>
<mxCell id="c_c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="462,715,30,20"/>
<mxCell id="c_c1_e" edge="1" source="c_b" target="c_c1"/>
<mxCell id="c_c2" value="unit" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="510,713,84,60"/>
<mxCell id="c_c2_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="562,715,30,20"/>
<mxCell id="c_c2_e" edge="1" source="c_c1" target="c_c2"/>
<mxCell id="c_c3" value="install" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="610,713,96,60"/>
<mxCell id="c_c3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="674,715,30,20"/>
<mxCell id="c_c3_e" edge="1" source="c_c2" target="c_c3"/>
<mxCell id="c_c4" value="merge" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="722,713,96,60"/>
<mxCell id="c_c4_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="786,715,30,20"/>
<mxCell id="c_c4_e" edge="1" source="c_c3" target="c_c4"/>
<mxCell id="c_d" value="release（image、bootstrap.sh、tar + .digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="834,713,200,60"/>
<mxCell id="c_d_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="1002,715,30,20"/>
<mxCell id="c_d_e" edge="1" source="c_c4" target="c_d"/>
<mxCell id="c_e" value="release-test（amd64、arm64 原生 runner）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="1050,713,190,60"/>
<mxCell id="c_e_e" edge="1" source="c_d" target="c_e"/>
<mxCell id="c_f" value="驗收：已釋出版驅動候選 + 乾淨 fixture repo 跑完整流程" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p3L5" geo="1256,713,250,60"/>
<mxCell id="c_f_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="1474,715,30,20"/>
<mxCell id="c_f_e" edge="1" source="c_e" target="c_f"/>
<mxCell id="p3_jm" value="just 矩陣 1.33.0 + latest（latest 非 required）；lint 擋比 1.33 新的功能與白名單外主機命令（ADR 記破壞性變更）；驗收用 dev vendor_kit -i &amp;lt;剛 build 的 tag&amp;gt; 同一機制；每版最低環境（docker 19.03、just 1.33.0）跑完整、其他環境（docker 上界、just latest、arm64、WSL2）按世代；驗收 §7.4 條 1–13 缺任一不得出貨；已釋出 image／Release 資產／fixture 永不刪；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p3L5" geo="20,789,1520,46"/>
<mxCell id="p3_jm_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="1508,791,30,20"/>
<mxCell id="p3_acc_l" value="驗收矩陣（§7.4；每列一個情境；左右兩表接續）" style="fillColor=none;strokeColor=none;fontSize=13" parent="p3L5" geo="20,849,900,28"/>
<mxCell id="p3_acc_h0" value="#" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="20,881,40,30"/>
<mxCell id="p3_acc_h1" value="情境" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="60,881,150,30"/>
<mxCell id="p3_acc_h2" value="驗什麼" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="210,881,560,30"/>
<mxCell id="p3_acc_r0c0" value="1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,911,40,73"/>
<mxCell id="p3_acc_r0c1" value="已釋出版驅動候選" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,911,150,73"/>
<mxCell id="p3_acc_r0c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,913,30,20"/>
<mxCell id="p3_acc_r0c2" value="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1、零 tracked 寫入）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁止由候選樹複製 fixture、禁 stub 引擎" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,911,560,73"/>
<mxCell id="p3_acc_r1c0" value="2" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,984,40,42"/>
<mxCell id="p3_acc_r1c1" value="最低環境 × 世代" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,984,150,42"/>
<mxCell id="p3_acc_r1c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,986,30,20"/>
<mxCell id="p3_acc_r1c2" value="每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境按世代覆蓋；成本上限當觸發討論條件" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,984,560,42"/>
<mxCell id="p3_acc_r2c0" value="3" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1026,40,42"/>
<mxCell id="p3_acc_r2c1" value="升級後 == 全新安裝" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1026,150,42"/>
<mxCell id="p3_acc_r2c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1028,30,20"/>
<mxCell id="p3_acc_r2c2" value="升級後 .vendor_kit/ tracked 內容 == 用 C 全新 install + add（排除時間戳、digest、written_by）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1026,560,42"/>
<mxCell id="p3_acc_r3c0" value="4" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1068,40,26"/>
<mxCell id="p3_acc_r3c1" value="連續升級" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1068,150,26"/>
<mxCell id="p3_acc_r3c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1070,30,20"/>
<mxCell id="p3_acc_r3c2" value="r_i → r_j → C；固定 floor 直接跳升 C" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1068,560,26"/>
<mxCell id="p3_acc_r4c0" value="5" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1094,40,42"/>
<mxCell id="p3_acc_r4c1" value="降版" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1094,150,42"/>
<mxCell id="p3_acc_r4c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1096,30,20"/>
<mxCell id="p3_acc_r4c2" value="upgrade vendor_kit@&amp;lt;舊版&amp;gt;：同 P／schema 成功；跨 schema 改檔前拒絕 3 印 6-10、零寫入" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1094,560,42"/>
<mxCell id="p3_acc_r5c0" value="6" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1136,40,42"/>
<mxCell id="p3_acc_r5c1" value="&amp;lt; floor 太舊" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1136,150,42"/>
<mxCell id="p3_acc_r5c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1138,30,20"/>
<mxCell id="p3_acc_r5c2" value="唯一可用 synthetic fixture；任一動詞 → 3 印 6-18、零寫入；floor 檢查在任何上網之前（斷網也回 3）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1136,560,42"/>
<mxCell id="p3_acc_r6c0" value="7" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1178,40,57"/>
<mxCell id="p3_acc_r6c1" value="舊 bootstrap.sh 再跑" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1178,150,57"/>
<mxCell id="p3_acc_r6c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1180,30,20"/>
<mxCell id="p3_acc_r6c2" value="在已升級 repo 再跑：用 version.toml 指定引擎，不降版" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1178,560,57"/>
<mxCell id="p3_acc_r7c0" value="8" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1235,40,26"/>
<mxCell id="p3_acc_r7c1" value="舊引擎讀新檔" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1235,150,26"/>
<mxCell id="p3_acc_r7c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1237,30,20"/>
<mxCell id="p3_acc_r7c2" value="dev vendor_kit -i 舊 image：寫入前拒絕 3 印 6-19；不重產 tracked 薄殼" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1235,560,26"/>
<mxCell id="p3_acc_r8c0" value="9" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1261,40,42"/>
<mxCell id="p3_acc_r8c1" value="只改第一行後 CI=true sync" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1261,150,42"/>
<mxCell id="p3_acc_r8c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1263,30,20"/>
<mxCell id="p3_acc_r8c2" value="模擬 Renovate、驗 CI 真值規則 → 1 列薄殼不符、零 tracked 寫入" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1261,560,42"/>
<mxCell id="p3_acc_r9c0" value="10" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1303,40,42"/>
<mxCell id="p3_acc_r9c1" value="fresh clone 無 gen/" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1303,150,42"/>
<mxCell id="p3_acc_r9c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1305,30,20"/>
<mxCell id="p3_acc_r9c2" value="just vendor_kit 列出 vendor_kit 命名空間不觸網（工具命名空間 sync 後才出現，mod? 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1303,560,42"/>
<mxCell id="p3_acc_r10c0" value="11" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1345,40,42"/>
<mxCell id="p3_acc_r10c1" value="使用者改薄殼／未納管檔／append" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1345,150,42"/>
<mxCell id="p3_acc_r10c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1347,30,20"/>
<mxCell id="p3_acc_r10c2" value="不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1345,560,42"/>
<mxCell id="p3_acc_r11c0" value="12" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1387,40,42"/>
<mxCell id="p3_acc_r11c1" value="中斷與重跑" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1387,150,42"/>
<mxCell id="p3_acc_r11c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1389,30,20"/>
<mxCell id="p3_acc_r11c2" value="resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1387,560,42"/>
<mxCell id="p3_acc_r12c0" value="13" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1429,40,42"/>
<mxCell id="p3_acc_r12c1" value="歷史 parser × 異常 TOML" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1429,150,42"/>
<mxCell id="p3_acc_r12c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1431,30,20"/>
<mxCell id="p3_acc_r12c2" value="BOM、空白、重複 vendor_kit 行 → 1、schema 位置、local 覆寫、尾端註解" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1429,560,42"/>
<mxCell id="p3_acc_r13c0" value="14" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="20,1471,40,26"/>
<mxCell id="p3_acc_r13c1" value="just 矩陣" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="60,1471,150,26"/>
<mxCell id="p3_acc_r13c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="178,1473,30,20"/>
<mxCell id="p3_acc_r13c2" value="1.33.0 + latest（latest 非 required）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="210,1471,560,26"/>
<mxCell id="p3_accb_h0" value="#" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="790,881,40,30"/>
<mxCell id="p3_accb_h1" value="情境" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="830,881,150,30"/>
<mxCell id="p3_accb_h2" value="驗什麼" style="fillColor=#e6e6e6;strokeColor=#999999" parent="p3L5" geo="980,881,560,30"/>
<mxCell id="p3_accb_r0c0" value="15" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,911,40,42"/>
<mxCell id="p3_accb_r0c1" value="amd64 與 arm64 原生 runner" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,911,150,42"/>
<mxCell id="p3_accb_r0c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,913,30,20"/>
<mxCell id="p3_accb_r0c2" value="各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,911,560,42"/>
<mxCell id="p3_accb_r1c0" value="16" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,953,40,57"/>
<mxCell id="p3_accb_r1c1" value="離線包（Q26）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,953,150,57"/>
<mxCell id="p3_accb_r1c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,955,30,20"/>
<mxCell id="p3_accb_r1c2" value="無法連 GHCR 的機器用 bootstrap.sh --local &amp;lt;tar&amp;gt;（旁檔 .digest）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 local_image_id；旁檔缺 → 1；amd64／arm64 各一次" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,953,560,57"/>
<mxCell id="p3_accb_r2c0" value="17" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1010,40,57"/>
<mxCell id="p3_accb_r2c1" value="離線可用（Q22／Q26）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1010,150,57"/>
<mxCell id="p3_accb_r2c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1012,30,20"/>
<mxCell id="p3_accb_r2c2" value="本機已有 image 後斷網 → just &amp;lt;ns&amp;gt; build（自動 sync 快路徑）與 just vendor_kit sync 必須成功且不起 pull；斷網 + 無 image → 1 印 6-31 於 --timeout 5 內結束、不 hang" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1010,560,57"/>
<mxCell id="p3_accb_r3c0" value="18" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1067,40,57"/>
<mxCell id="p3_accb_r3c1" value="私有工具" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1067,150,57"/>
<mxCell id="p3_accb_r3c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1069,30,20"/>
<mxCell id="p3_accb_r3c2" value="add &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt; 可拉；add &amp;lt;repo&amp;gt; 無 token → 1 印 6-3；update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1067,560,57"/>
<mxCell id="p3_accb_r4c0" value="19" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1124,40,42"/>
<mxCell id="p3_accb_r4c1" value="append" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1124,150,42"/>
<mxCell id="p3_accb_r4c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1126,30,20"/>
<mxCell id="p3_accb_r4c2" value="LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 .dockerignore 三行 append → uninstall 刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1124,560,42"/>
<mxCell id="p3_accb_r5c0" value="20" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1166,40,42"/>
<mxCell id="p3_accb_r5c1" value="空白路徑" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1166,150,42"/>
<mxCell id="p3_accb_r5c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1168,30,20"/>
<mxCell id="p3_accb_r5c2" value="專案根含空白與 $、dev -p &quot;含 空白/路徑&quot;；vk-resolve mount 八進位跳脫往返；just vendor_kit add --help 到引擎" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1166,560,42"/>
<mxCell id="p3_accb_r6c0" value="21" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1208,40,42"/>
<mxCell id="p3_accb_r6c1" value="worktree／submodule" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1208,150,42"/>
<mxCell id="p3_accb_r6c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1210,30,20"/>
<mxCell id="p3_accb_r6c2" value="git worktree（.git 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1208,560,42"/>
<mxCell id="p3_accb_r7c0" value="22" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1250,40,42"/>
<mxCell id="p3_accb_r7c1" value="rootless docker／Podman" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1250,150,42"/>
<mxCell id="p3_accb_r7c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1252,30,20"/>
<mxCell id="p3_accb_r7c2" value="setup-docker-action rootless: true（不加 -u、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：--userns=keep-id）各跑完整流程；uid 12345 無 passwd 項" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1250,560,42"/>
<mxCell id="p3_accb_r8c0" value="23" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1292,40,57"/>
<mxCell id="p3_accb_r8c1" value="prune" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1292,150,57"/>
<mxCell id="p3_accb_r8c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1294,30,20"/>
<mxCell id="p3_accb_r8c2" value="完整流程前後 docker network ls／volume ls 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊工具 image 刪、version.toml 引用的與 local 覆寫 tag 保留；--dry-run 零刪除；未恢復的 .tmp.* 不刪" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1292,560,57"/>
<mxCell id="p3_accb_r9c0" value="24" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1349,40,42"/>
<mxCell id="p3_accb_r9c1" value="多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1349,150,42"/>
<mxCell id="p3_accb_r9c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1351,30,20"/>
<mxCell id="p3_accb_r9c2" value="兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1349,560,42"/>
<mxCell id="p3_accb_r10c0" value="25" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1391,40,42"/>
<mxCell id="p3_accb_r10c1" value="F1 fixture（just 1.33.0）" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1391,150,42"/>
<mxCell id="p3_accb_r10c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1393,30,20"/>
<mxCell id="p3_accb_r10c2" value="cache 缺檔時 just vendor_kit sync 可進入（mod?）；just &amp;lt;ns&amp;gt; build 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 _sync 的模組" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1391,560,42"/>
<mxCell id="p3_accb_r11c0" value="26" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1433,40,26"/>
<mxCell id="p3_accb_r11c1" value="無 tty／EOF" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1433,150,26"/>
<mxCell id="p3_accb_r11c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1435,30,20"/>
<mxCell id="p3_accb_r11c2" value="CI 無 -y 需詢問 → 1 印 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1433,560,26"/>
<mxCell id="p3_accb_r12c0" value="27" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1459,40,42"/>
<mxCell id="p3_accb_r12c1" value="Renovate 實際 repo" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1459,150,42"/>
<mxCell id="p3_accb_r12c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1461,30,20"/>
<mxCell id="p3_accb_r12c2" value="人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1459,560,42"/>
<mxCell id="p3_accb_r13c0" value="28" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="790,1501,40,26"/>
<mxCell id="p3_accb_r13c1" value="驗收動詞集合" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="830,1501,150,26"/>
<mxCell id="p3_accb_r13c1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p3L5" geo="948,1503,30,20"/>
<mxCell id="p3_accb_r13c2" value="由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅" style="fillColor=#ffffff;strokeColor=#999999" parent="p3L5" geo="980,1501,560,26"/>
<mxCell id="p3c_lg0" value="橙橢圓：需要人動作（1／3 印指令、2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="40,1678,400,56"/>
<mxCell id="p3c_lg1" value="綠橢圓：成功終點（exit 0）" style="fillColor=#d5e8d4;strokeColor=#000000" geo="460,1680,270,52"/>
<mxCell id="p3c_lg2" value="白：步驟／說明" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="750,1686,130,40"/>
<mxCell id="p3c_lg3" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="900,1686,190,40"/>
<mxCell id="p3c_lg4" value="灰底：表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1110,1686,110,40"/>
<mxCell id="p3c_lgt" value="實線 = 執行順序；線上文字 = 條件&lt;br&gt;驗收表：一列一個情境" style="fillColor=none;strokeColor=none" geo="1240,1676,300,60"/>
<mxCell id="p3c_lg5" value="淺灰底：分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="40,1752,200,40"/>
<mxCell id="p3c_lg6" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="260,1752,200,40"/>
<mxCell id="p3c_lg6_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="428,1754,30,20"/>
<mxCell id="p3c_lg7" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="480,1752,220,40"/>
<mxCell id="p3c_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1808,300,28"/>
<mxCell id="p3c_tk0" value="check.sh 六步（⓪–⑤）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1842,150,55"/>
<mxCell id="p3c_tv0" value="vendor_kit 出貨、進 git 的腳本（第二行自描述、第一個動作 export CI=1）：⓪ local 被 track → 1；① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；整體結束碼 = 第一個失敗步驟的碼" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1842,610,55"/>
<mxCell id="p3c_tk1" value="check.sh --dist" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1897,150,55"/>
<mxCell id="p3c_tv1" value="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1897,610,55"/>
<mxCell id="p3c_tk2" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1952,150,55"/>
<mxCell id="p3c_tv2" value="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1952,610,55"/>
<mxCell id="p3c_tk3" value="CI／runner" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2007,150,40"/>
<mxCell id="p3c_tv3" value="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2007,610,40"/>
<mxCell id="p3c_tk4" value="Renovate preset" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2047,150,55"/>
<mxCell id="p3c_tv4" value="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2047,610,55"/>
<mxCell id="p3c_tk5" value="Renovate／PR／rebase" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2102,150,40"/>
<mxCell id="p3c_tv5" value="Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2102,610,40"/>
<mxCell id="p3c_tk6" value="env-test／test-base" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2142,150,55"/>
<mxCell id="p3c_tv6" value="vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後 lint／unit／install／merge 各測試 stage 的共同基底，環境不對就沒有任何測試會跑" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2142,610,55"/>
<mxCell id="p3c_tk7" value="lint／unit／測試矩陣" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1842,150,40"/>
<mxCell id="p3c_tv7" value="lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1842,610,40"/>
<mxCell id="p3c_tk8" value="release／release-test" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1882,150,40"/>
<mxCell id="p3c_tv8" value="release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1882,610,40"/>
<mxCell id="p3c_tk9" value="fixture repo" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1922,150,40"/>
<mxCell id="p3c_tv9" value="驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1922,610,40"/>
<mxCell id="p3c_tk10" value="floor" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1962,150,40"/>
<mxCell id="p3c_tv10" value="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1962,610,40"/>
<mxCell id="p3c_tk11" value="rootless／Podman" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2002,150,40"/>
<mxCell id="p3c_tv11" value="rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2002,610,40"/>
<mxCell id="p3c_tk12" value="worktree／submodule" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2042,150,40"/>
<mxCell id="p3c_tv12" value="git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2042,610,40"/>
<mxCell id="p3c_tk13" value="離線可用（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2082,150,40"/>
<mxCell id="p3c_tv13" value="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2082,610,40"/>
<mxCell id="p3c_tk14" value="多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2122,150,40"/>
<mxCell id="p3c_tv14" value="不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2122,610,40"/>
</diagram>
<diagram id="v1p4" name="架構圖 v2">
<mxCell id="title" value="架構圖 v2 ── 主機、引擎 8 模組、registry（只畫模組、最小單元、模組間傳的資料）" style="fontSize=18" geo="40,20,1200,34"/>
<mxCell id="p4_num" value="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" style="fillColor=none;strokeColor=none" geo="40,56,1200,26"/>
<mxCell id="p4_np" value="&lt;b&gt;本頁無待拍板&lt;/b&gt;：本頁只畫模組、最小單元、模組間傳的資料（箭頭只標傳什麼，不標動作；雙箭頭 = 讀寫都有）；載入順序／操作順序／sync 判斷／拉取條件／退出流程一律見流程頁（p5～）。啟動器不算引擎模組（主機側薄殼）" style="fillColor=#ffffff;strokeColor=#999999" geo="1000,12,600,65"/>
<mxCell id="p4G" value="GHCR（ghcr.io）── 兩種 image 都多架構；拉取都由主機上的啟動器執行，引擎容器內不呼叫 docker" style="fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=18" geo="40,96,1560,162"/>
<mxCell id="g_eng" value="&lt;b&gt;引擎 image ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN（公開）&lt;/b&gt;&lt;br&gt;多架構 amd64 + arm64；LABEL …vendor_kit=1、.protocol、.schema；一個專案用 version.toml 正規行那一版；引擎覆寫 vendor_kit=&amp;lt;tag&amp;gt;（version.local.toml）時啟動器 docker image inspect 驗 ID 後直接用本機 image、不 pull；也出 docker save tar + .digest（#27）；已釋出永不刪" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="p4G" geo="20,50,520,92"/>
<mxCell id="g_eng_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4G" geo="508,52,30,20"/>
<mxCell id="g_dist" value="&lt;b&gt;工具 image ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;&lt;/b&gt;&lt;br&gt;多架構 amd64 + arm64（同一次 buildx、COPY-only）；純資料 FROM scratch 只有 /dist；LABEL …vendor_kit=1；version.toml 與印記記 index digest" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="p4G" geo="560,50,500,92"/>
<mxCell id="g_dist_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4G" geo="1028,52,30,20"/>
<mxCell id="g_note" value="&lt;b&gt;registry 模組只查 tag／index digest&lt;/b&gt;（update／add／upgrade 用；私有 registry 用 VENDOR_KIT_REGISTRY_TOKEN 或 TOKEN_FILE（-v 掛 /run/vk-token），或改用 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;）&lt;br&gt;sync 不查最新版；只拉鎖定版；拉取由主機上的啟動器執行，先 docker image inspect 再 pull（逾時）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="p4G" geo="1080,50,460,92"/>
<mxCell id="g_note_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4G" geo="1508,52,30,20"/>
<mxCell id="p4H" value="主機（使用者電腦／CI runner）" style="fillColor=#f5f5f5;strokeColor=#000000;fontSize=18" geo="40,328,520,1328"/>
<mxCell id="h0" value="使用者&lt;br&gt;打 just vendor_kit &amp;lt;動詞&amp;gt; …&lt;br&gt;或 just &amp;lt;ns&amp;gt; …" style="fillColor=#FFF4C3;strokeColor=#000000" parent="p4H" geo="20,50,220,106"/>
<mxCell id="h1" value="根 justfile（使用者的，進 git）&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="p4H" geo="20,186,220,61"/>
<mxCell id="h1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4H" geo="208,188,30,20"/>
<mxCell id="h2" value=".vendor_kit/entry.just（進 git）&lt;br&gt;mod vendor_kit &#x27;vendor.just&#x27;&lt;br&gt;import? &#x27;gen/tools.just&#x27;" style="fillColor=#ffffff;strokeColor=#82b366" parent="p4H" geo="20,277,220,108"/>
<mxCell id="h3" value=".vendor_kit/vendor.just（進 git）&lt;br&gt;動詞 recipe（一行轉發）&lt;br&gt;+ 啟動器本體（POSIX sh）" style="fillColor=#ffffff;strokeColor=#82b366" parent="p4H" geo="20,415,220,79"/>
<mxCell id="h3_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4H" geo="208,417,30,20"/>
<mxCell id="h4" value="&lt;b&gt;啟動器&lt;/b&gt;（主機側薄殼，非引擎模組；主機需 docker ≥ 19.03、sh、just ≥ 1.33.0）&lt;br&gt;下列為責任單元；命令步驟見流程頁與 p3b" style="fillColor=#f8cecc;strokeColor=#b85450" parent="p4H" geo="20,524,220,296"/>
<mxCell id="h4_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4H" geo="208,526,30,20"/>
<mxCell id="h4_u0_0" value="讀引擎 ref" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,632,72,24"/>
<mxCell id="h4_u0_1" value="取得引擎／工具 image" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="104,632,124,24"/>
<mxCell id="h4_u1_0" value="展開 /dist 到暫存" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,662,110,24"/>
<mxCell id="h4_u1_1" value="起引擎容器" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="142,662,68,24"/>
<mxCell id="h4_u2_0" value="vk-resolve 驗文法" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,692,114,24"/>
<mxCell id="h4_u3_0" value="協定旗標 --protocol" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,722,124,24"/>
<mxCell id="h4_u4_0" value="清理（trap）" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,752,82,24"/>
<mxCell id="h4_u4_1" value="pull 逾時" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="114,752,68,24"/>
<mxCell id="h4_u5_0" value="資源 label" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4H" geo="26,782,74,24"/>
<mxCell id="h_vk" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/            # 契約② p2，根目錄只多這個&lt;br&gt;├─ version.toml        # 進 git：唯一來源&lt;br&gt;├─ version.local.toml  # 不進 git：dev 覆寫&lt;br&gt;├─ .gitignore          # 進 git：我們自己的&lt;br&gt;├─ entry.just          # 進 git：mod + import?&lt;br&gt;├─ vendor.just         # 進 git：動詞 + 啟動器&lt;br&gt;├─ ci/check.sh         # 進 git：CI 六步（⓪–⑤）&lt;br&gt;├─ baseline/           # 進 git：.gitkeep、&amp;lt;repo&amp;gt;/ 範本 + metadata&lt;br&gt;├─ gen/                # 不進 git：tools.just、.stamp、&lt;br&gt;│                      #   &amp;lt;repo&amp;gt;.stamp（印記）&lt;br&gt;├─ .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml  # 不進 git：進度日誌&lt;br&gt;├─ .tmp.dist.&amp;lt;id&amp;gt;/     # 不進 git：啟動器暫存&lt;br&gt;└─ cache/&amp;lt;repo&amp;gt;/       # 不進 git：工具檔展開&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p4H" geo="20,840,480,217"/>
<mxCell id="tmp" value="暫存 .vendor_kit/&lt;br&gt;.tmp.dist.&amp;lt;id&amp;gt;/（專案內）&lt;br&gt;工具 /dist 展開副本 + vk-resolve&lt;br&gt;（唯讀掛進引擎當 /dist）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p4H" geo="260,50,200,94"/>
<mxCell id="g1" value=".vendor_kit/gen/tools.just（不進 git）&lt;br&gt;mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/&lt;br&gt;just/&amp;lt;ns&amp;gt;.just&#x27;&lt;br&gt;一行一命名空間" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="p4H" geo="260,277,240,108"/>
<mxCell id="g1_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4H" geo="468,279,30,20"/>
<mxCell id="g2" value="工具命名空間 just &amp;lt;ns&amp;gt; …&lt;br&gt;= cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&lt;br&gt;裡的 recipe" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="p4H" geo="260,415,240,79"/>
<mxCell id="g2_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4H" geo="468,417,30,20"/>
<mxCell id="p4E" value="引擎容器 vendor_kit:vN（8 個模組；每個模組列最小單元，一格一個）" style="fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=16" geo="600,328,560,1328"/>
<mxCell id="m_reg" value="&lt;b&gt;registry&lt;/b&gt;：查 GHCR" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="290,164,250,128"/>
<mxCell id="m_reg_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="508,166,30,20"/>
<mxCell id="m_reg_u0_0" value="查 tag（SemVer 最大正式版）" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,194,164,24"/>
<mxCell id="m_reg_u1_0" value="查 index digest" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,224,106,24"/>
<mxCell id="m_reg_u1_1" value="token／token file" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="408,224,118,24"/>
<mxCell id="m_reg_u2_0" value="逾時" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,254,38,24"/>
<mxCell id="m_ver" value="&lt;b&gt;version&lt;/b&gt;：version.toml／local 讀寫" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="290,314,250,144"/>
<mxCell id="m_ver_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="508,316,30,20"/>
<mxCell id="m_ver_u0_0" value="讀 toml（正規行）" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,360,108,24"/>
<mxCell id="m_ver_u0_1" value="寫 toml" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="410,360,58,24"/>
<mxCell id="m_ver_u1_0" value="schema 轉換" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,390,80,24"/>
<mxCell id="m_ver_u1_1" value="flock" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="382,390,48,24"/>
<mxCell id="m_ver_u1_2" value="指紋" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="436,390,38,24"/>
<mxCell id="m_ver_u2_0" value="進度日誌" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,420,58,24"/>
<mxCell id="m_ver_u2_1" value="label／keep" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="360,420,82,24"/>
<mxCell id="m_mat" value="&lt;b&gt;materialize&lt;/b&gt;：/dist → cache/&amp;lt;repo&amp;gt;/" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="290,480,250,158"/>
<mxCell id="m_mat_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="508,482,30,20"/>
<mxCell id="m_mat_u0_0" value="展開 /dist" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,526,74,24"/>
<mxCell id="m_mat_u0_1" value="路徑驗證" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="376,526,58,24"/>
<mxCell id="m_mat_u1_0" value="印記 gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,556,140,24"/>
<mxCell id="m_mat_u2_0" value="verify sha256" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,586,96,24"/>
<mxCell id="m_bl" value="&lt;b&gt;baseline&lt;/b&gt;：baseline/&amp;lt;repo&amp;gt;/ + metadata" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="290,660,250,114"/>
<mxCell id="m_bl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="508,662,30,20"/>
<mxCell id="m_bl_u0_0" value="範本副本" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,706,58,24"/>
<mxCell id="m_bl_u0_1" value="metadata" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="360,706,66,24"/>
<mxCell id="m_bl_u0_2" value="五態 state" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="432,706,74,24"/>
<mxCell id="m_bl_u1_0" value="declined_hash" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,736,96,24"/>
<mxCell id="m_bl_u1_1" value="conflicts" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="398,736,72,24"/>
<mxCell id="m_lg" value="&lt;b&gt;launcher-gen&lt;/b&gt;：薄殼、gen/、根 justfile 一行、根 .dockerignore 三行" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="290,952,250,354"/>
<mxCell id="m_lg_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="508,954,30,20"/>
<mxCell id="m_lg_u0_0" value="薄殼四檔" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,1013,58,24"/>
<mxCell id="m_lg_u0_1" value="自描述首行" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="360,1013,68,24"/>
<mxCell id="m_lg_u1_0" value="tools.just（mod?）" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,1043,122,24"/>
<mxCell id="m_lg_u1_1" value="check.sh" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="424,1043,66,24"/>
<mxCell id="m_lg_u2_0" value=".stamp" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="296,1073,54,24"/>
<mxCell id="m_lg_u2_1" value="justfile 四行" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="356,1073,92,24"/>
<mxCell id="m_mg" value="&lt;b&gt;merge&lt;/b&gt;：逐檔合併" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="296,806,116,114"/>
<mxCell id="m_mg_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="380,808,30,20"/>
<mxCell id="m_mg_u0_0" value="狀態機" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="302,852,48,24"/>
<mxCell id="m_mg_u1_0" value="merge-file" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="302,882,78,24"/>
<mxCell id="m_init" value="&lt;b&gt;init&lt;/b&gt;：初始檔" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="422,806,116,114"/>
<mxCell id="m_init_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4E" geo="506,808,30,20"/>
<mxCell id="m_init_u0_0" value="建檔" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="428,852,38,24"/>
<mxCell id="m_init_u0_1" value="append" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="472,852,54,24"/>
<mxCell id="m_init_u1_0" value="新檔詢問" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="428,882,58,24"/>
<mxCell id="grp_im" style="fillColor=none;strokeColor=#666666;dashed=1" parent="p4E" geo="290,796,250,134"/>
<mxCell id="m_cli" value="&lt;b&gt;cli&lt;/b&gt;" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" parent="p4E" geo="20,50,140,1256"/>
<mxCell id="m_cli_u0" value="子命令解析" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,80,120,24"/>
<mxCell id="m_cli_u1" value="--protocol P" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,110,120,24"/>
<mxCell id="m_cli_u2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,140,120,24"/>
<mxCell id="m_cli_u3" value="詢問／-y／tty" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,170,120,24"/>
<mxCell id="m_cli_u4" value="結束碼 0/1/2/3" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,200,120,24"/>
<mxCell id="m_cli_u5" value="呼叫其他模組" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" parent="p4E" geo="30,230,120,24"/>
<mxCell id="d_reg" value="tag, index digest" edge="1" source="m_reg" target="m_cli"/>
<mxCell id="d_ver" value="version.toml 內容&lt;br&gt;指紋" edge="1" source="m_cli" target="m_ver"/>
<mxCell id="d_mat" value="/dist 路徑、&amp;lt;repo&amp;gt;" edge="1" source="m_cli" target="m_mat"/>
<mxCell id="d_bl" value="metadata" edge="1" source="m_bl" target="m_cli"/>
<mxCell id="d_im" value="檔案清單&lt;br&gt;逐檔決定" edge="1" source="m_cli" target="grp_im"/>
<mxCell id="d_lg" value="引擎 ref、動詞清單" edge="1" source="m_cli" target="m_lg"/>
<mxCell id="d_mat_bl" value="cache 路徑、印記" edge="1" source="m_mat" target="m_bl"/>
<mxCell id="d_im_bl" value="檔案清單、逐檔決定" edge="1" source="grp_im" target="m_bl"/>
<mxCell id="p4P" value="專案根（掛載為 /repo）" style="fillColor=#d5e8d4;strokeColor=#000000;fontSize=18" geo="1320,328,280,1328"/>
<mxCell id="f_note" value="整個專案根 -v &amp;lt;專案根&amp;gt;:/repo -w /repo 掛進引擎（可寫）；引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.&amp;lt;id&amp;gt;/ 唯讀掛 /dist/&amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" parent="p4P" geo="15,50,240,94"/>
<mxCell id="f_ver" value="version.toml（進 git）" style="fillColor=#ffffff;strokeColor=#82b366" parent="p4P" geo="15,314,240,36"/>
<mxCell id="f_ver_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,316,30,20"/>
<mxCell id="f_vl" value="version.local.toml（dev 覆寫）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="p4P" geo="15,358,240,36"/>
<mxCell id="f_vl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,360,30,20"/>
<mxCell id="f_repo" value="cache/&amp;lt;repo&amp;gt;/（不進 git，不可改）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="p4P" geo="15,480,240,118"/>
<mxCell id="f_repo_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,482,30,20"/>
<mxCell id="f_repo_f0" value="files/…" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="f_repo" geo="10,30,210,24"/>
<mxCell id="f_repo_f1" value="init.toml" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="f_repo" geo="10,58,210,24"/>
<mxCell id="f_repo_f2" value="just/&amp;lt;ns&amp;gt;.just" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="f_repo" geo="10,86,210,24"/>
<mxCell id="f_stamp" value="gen/&amp;lt;repo&amp;gt;.stamp（印記）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="p4P" geo="15,606,240,32"/>
<mxCell id="f_stamp_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,608,30,20"/>
<mxCell id="f_bl" value="baseline/&amp;lt;repo&amp;gt;/（進 git）" style="fillColor=#ffffff;strokeColor=#82b366" parent="p4P" geo="15,660,240,90"/>
<mxCell id="f_bl_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,662,30,20"/>
<mxCell id="f_bl_f0" value="範本副本（上次合併的）" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_bl" geo="10,30,210,24"/>
<mxCell id="f_bl_f1" value="metadata .vendor_kit.toml" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_bl" geo="10,58,210,24"/>
<mxCell id="f_user" value="初始檔（使用者的，進 git；永不刪、永不覆蓋）" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="p4P" geo="15,796,240,90"/>
<mxCell id="f_user_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,798,30,20"/>
<mxCell id="f_user_f0" value="Dockerfile 等（copy）" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="f_user" geo="10,30,210,24"/>
<mxCell id="f_user_f1" value="根 .gitignore 幾行（append）" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="f_user" geo="10,58,210,24"/>
<mxCell id="f_just" value="根 justfile（使用者的，進 git）&lt;br&gt;import 一行；新檔另有 default 兩行" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="p4P" geo="15,952,240,50"/>
<mxCell id="f_just_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,954,30,20"/>
<mxCell id="f_di" value="根 .dockerignore（使用者的）&lt;br&gt;三行（問後 append）" style="fillColor=#FFF4C3;strokeColor=#82b366" parent="p4P" geo="15,1010,240,44"/>
<mxCell id="f_di_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,1012,30,20"/>
<mxCell id="f_shell" value="自有薄殼（進 git；首行自描述）" style="fillColor=#ffffff;strokeColor=#82b366" parent="p4P" geo="15,1062,240,146"/>
<mxCell id="f_shell_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,1064,30,20"/>
<mxCell id="f_shell_f0" value="entry.just" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_shell" geo="10,30,210,24"/>
<mxCell id="f_shell_f1" value="vendor.just" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_shell" geo="10,58,210,24"/>
<mxCell id="f_shell_f2" value=".gitignore" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_shell" geo="10,86,210,24"/>
<mxCell id="f_shell_f3" value="ci/check.sh" style="fillColor=#ffffff;strokeColor=#82b366" parent="f_shell" geo="10,114,210,24"/>
<mxCell id="f_gen" value="gen/（不進 git）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="p4P" geo="15,1216,240,90"/>
<mxCell id="f_gen_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" parent="p4P" geo="223,1218,30,20"/>
<mxCell id="f_gen_f0" value="tools.just（mod? 行）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="f_gen" geo="10,30,210,24"/>
<mxCell id="f_gen_f1" value=".stamp（只記引擎 ref）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" parent="f_gen" geo="10,58,210,24"/>
<mxCell id="w_ver" value="version.toml 內容" edge="1" source="m_ver" target="f_ver"/>
<mxCell id="w_vl" value="覆寫行（path:／&lt;br&gt;tag + image ID）" edge="1" source="m_ver" target="f_vl"/>
<mxCell id="w_repo" value="展開的工具檔&lt;br&gt;（整批替換）" edge="1" source="m_mat" target="f_repo"/>
<mxCell id="w_stamp" value="index digest&lt;br&gt;+ 每檔 sha256" edge="1" source="m_mat" target="f_stamp"/>
<mxCell id="w_bl" value="範本副本、metadata" edge="1" source="m_bl" target="f_bl"/>
<mxCell id="w_user" value="初始檔內容&lt;br&gt;（現況／結果）" edge="1" source="grp_im" target="f_user"/>
<mxCell id="w_just" value="import 那一行" edge="1" source="m_lg" target="f_just"/>
<mxCell id="w_di" value=".dockerignore&lt;br&gt;三行" edge="1" source="m_lg" target="f_di"/>
<mxCell id="w_shell" value="薄殼四檔內容&lt;br&gt;（首行／模板）" edge="1" source="m_lg" target="f_shell"/>
<mxCell id="w_gen" value="tools.just、&lt;br&gt;.stamp 內容" edge="1" source="m_lg" target="f_gen"/>
<mxCell id="run_cli" value="動詞、參數、--protocol P →&lt;br&gt;← 結束碼、vk-resolve 清單" edge="1" source="h4" target="m_cli"/>
<mxCell id="mount_dist" value="/dist/&amp;lt;repo&amp;gt;&lt;br&gt;（唯讀）" edge="1" source="tmp" target="p4E"/>
<mxCell id="pull_eng" value="引擎 image&lt;br&gt;（覆寫時本機 image）" edge="1" source="g_eng" target="p4H"/>
<mxCell id="pull_dist" value="工具 image 的 /dist 層&lt;br&gt;→ .tmp.dist.&amp;lt;id&amp;gt;/" edge="1" source="g_dist" target="p4H"/>
<mxCell id="q_reg" value="tag、index digest" edge="1" source="p4E" target="g_dist"/>
<mxCell id="p4_lg0" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="40,1696,170,40"/>
<mxCell id="p4_lg1" value="紅：引擎模組" style="fillColor=#f8cecc;strokeColor=light-dark(#000000,#9577A3)" geo="230,1696,130,40"/>
<mxCell id="p4_lg2" value="白小框：最小單元" style="fillColor=#ffffff;strokeColor=#666666;fontSize=10" geo="380,1696,140,40"/>
<mxCell id="p4_lg3" value="紅底紅粗框：啟動器（主機側薄殼）" style="fillColor=#f8cecc;strokeColor=#b85450" geo="540,1696,240,40"/>
<mxCell id="p4_lg4" value="淺灰底：主機分組" style="fillColor=#f5f5f5;strokeColor=light-dark(#000000,#9577A3)" geo="800,1696,150,40"/>
<mxCell id="p4_lg5" value="綠底：專案目錄分組" style="fillColor=#d5e8d4;strokeColor=light-dark(#000000,#9577A3)" geo="970,1696,160,40"/>
<mxCell id="p4_lgt" value="實線 = 資料流（線上文字 = 傳什麼）&lt;br&gt;雙箭頭 = 讀寫／來回都有；黃橢圓 = 使用者；載入／執行順序與判斷見流程頁" style="fillColor=none;strokeColor=none" geo="1150,1686,300,60"/>
<mxCell id="p4_lg6" value="淺橘底：規則／摘要（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="40,1762,190,40"/>
<mxCell id="p4_lg7" value="綠框：進 git" style="fillColor=#ffffff;strokeColor=#82b366" geo="250,1762,120,40"/>
<mxCell id="p4_lg8" value="灰虛線：不進 git（可重建）" style="fillColor=#ffffff;strokeColor=#999999;fontColor=#333333;dashed=1" geo="390,1762,200,40"/>
<mxCell id="p4_lg9" value="黃底綠框：使用者的檔（進 git）" style="fillColor=#FFF4C3;strokeColor=#82b366" geo="610,1762,230,40"/>
<mxCell id="p4_lg10" value="等寬字：檔案內容範例" style="fillColor=#ffffff;strokeColor=#999999" geo="860,1762,170,40"/>
<mxCell id="p4_lg11" value="右上角綠標籤：v2 改" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1050,1762,200,40"/>
<mxCell id="p4_lg11_v2" value="v2" style="fillColor=#00b050;strokeColor=#00b050;fontColor=#ffffff;fontSize=9" geo="1218,1764,30,20"/>
<mxCell id="p4_lg12" value="點線框：init／merge 共用箭頭" style="fillColor=none;strokeColor=#666666;dashed=1" geo="40,1828,200,40"/>
<mxCell id="p4_lg13" value="白底黑框：主機上的目錄／命名空間（不是檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="260,1828,300,40"/>
<mxCell id="p4_lg14" value="便條：說明（含「本頁無待拍板」）" style="fillColor=#ffffff;strokeColor=#999999" geo="580,1828,220,40"/>
<mxCell id="p4_th" value="本頁名詞（只列本頁用到的）" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1884,300,28"/>
<mxCell id="p4_tk0" value="引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1918,150,40"/>
<mxCell id="p4_tv0" value="vendor_kit 的程式本體：只以 image 存在（公開、多架構）、只在容器內跑；8 個模組見紫色容器；一個專案用 version.toml 正規行那一版（version.local.toml 可覆寫成本機 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1918,610,40"/>
<mxCell id="p4_tk1" value="啟動器" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1958,150,55"/>
<mxCell id="p4_tv1" value=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1958,610,55"/>
<mxCell id="p4_tk2" value="模組／最小單元" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2013,150,40"/>
<mxCell id="p4_tv2" value="模組 = 引擎裡一塊獨立責任的程式（紅框）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2013,610,40"/>
<mxCell id="p4_tk3" value="cli" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2053,150,40"/>
<mxCell id="p4_tv3" value="引擎的入口模組：解析子命令與參數（含 --protocol P）、負責所有詢問（-y 免問；無 tty → 1）、決定結束碼 0／1／2／3，並呼叫其他模組" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2053,610,40"/>
<mxCell id="p4_tk4" value="version" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2093,150,40"/>
<mxCell id="p4_tv4" value="讀寫 version.toml／version.local.toml（schema 轉換）；apply 拿 flock；產生／重驗輸入指紋；寫 metadata [progress]；算 docker 資源 label（prune 用）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2093,610,40"/>
<mxCell id="p4_tk5" value="registry" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2133,150,40"/>
<mxCell id="p4_tv5" value="查 GHCR 的 tag 與 index digest（update／add／upgrade 用；私有 registry 用 TOKEN／TOKEN_FILE；查詢有逾時）；sync 不查最新版，只拉鎖定版" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2133,610,40"/>
<mxCell id="p4_tk6" value="materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2173,150,40"/>
<mxCell id="p4_tv6" value="引擎內部步驟（不對外）：把主機掛進來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/、寫印記 gen/&amp;lt;repo&amp;gt;.stamp、verify sha256；在 apply 決定套用之後才做" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2173,610,40"/>
<mxCell id="p4_tk7" value="init／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2213,150,40"/>
<mxCell id="p4_tv7" value="init 建初始檔、append 幾行或問「要建 X 嗎」；merge 在 upgrade 時對每個檔跑狀態機（D==B → 問後換、三者皆異 → 問後三方合併）+ git merge-file；兩者都把檔案清單與逐檔決定交給 baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2213,610,40"/>
<mxCell id="p4_tk8" value="baseline（模組）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2253,150,40"/>
<mxCell id="p4_tv8" value="維護 baseline/&amp;lt;repo&amp;gt;/ 範本副本與 .vendor_kit.toml metadata（complete、五態、declined_hash、lines、conflicts、[progress]）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2253,610,40"/>
<mxCell id="p4_tk9" value="launcher-gen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1918,150,55"/>
<mxCell id="p4_tv9" value="產生 .vendor_kit/ 自有薄殼四檔（含自描述首行）、gen/tools.just（mod? 行）、gen/.stamp、根 justfile 那一行（新檔時四行）、根 .dockerignore 三行；薄殼與 gen/.stamp 只由 install／upgrade vendor_kit 重產（先比首行 hash）；tools.just 由 sync／add／remove／upgrade 重生" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1918,610,55"/>
<mxCell id="p4_tk10" value="多架構 index／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1973,150,40"/>
<mxCell id="p4_tv10" value="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1973,610,40"/>
<mxCell id="p4_tk11" value="暫存目錄 &amp;lt;tmp&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2013,150,40"/>
<mxCell id="p4_tv11" value="啟動器把工具 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;/，再唯讀掛進引擎當 /dist/&amp;lt;repo&amp;gt;（逐檔判斷讀這裡，不是 cache）；dev 時改掛 &amp;lt;dir&amp;gt;/dist；trap 清掉" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2013,610,40"/>
<mxCell id="p4_tk12" value="掛載（-v）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2053,150,40"/>
<mxCell id="p4_tv12" value="docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/&amp;lt;repo&amp;gt; = dev 覆寫的 &amp;lt;dir&amp;gt;/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2053,610,40"/>
<mxCell id="p4_tk13" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2093,150,40"/>
<mxCell id="p4_tv13" value="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2093,610,40"/>
<mxCell id="p4_tk14" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2133,150,55"/>
<mxCell id="p4_tv14" value="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2133,610,55"/>
<mxCell id="p4_tk15" value="CI／runner" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2188,150,40"/>
<mxCell id="p4_tv15" value="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2188,610,40"/>
<mxCell id="p4_tk16" value="docker image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2228,150,55"/>
<mxCell id="p4_tv16" value="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2228,610,55"/>
</diagram>
<diagram id="v1p5" name="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install">
<mxCell id="title" value="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install（§2／§3、v2.2 B／C、Q17／Q18、v2.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,108"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,128,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,128,460,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="760,128,260,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1040,128,180,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,128,360,28"/>
<mxCell id="bA" value="5a bootstrap.sh 前半：檢查 git／just → 決定引擎 ref（Q18：不退回內嵌）→ --local 三分支（檔案先驗存在；既是檔又是 tag → 1 + 6-37；只有 tar 形讀 .digest，v2.9 §1）→ inspect → 無才 pull → install（失敗即中止）；後半見「bootstrap.sh（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,172,1600,1493"/>
<mxCell id="bA_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="1556,5,30,20"/>
<mxCell id="a0" value="執行 bootstrap.sh -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]…" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bA" geo="20,36,220,58"/>
<mxCell id="a2" value="1：請先 git init（不代做）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bA" geo="20,126,220,58"/>
<mxCell id="a1" value="是 git repo？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="390,114,200,81"/>
<mxCell id="a4" value="1：印 just 下載＋安裝指令" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bA" geo="20,226,220,58"/>
<mxCell id="a3" value="just ≥ 1.33.0？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="390,215,200,81"/>
<mxCell id="a1v" value="專案已有 version.toml？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="370,316,240,81"/>
<mxCell id="a1v_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="586,306,30,20"/>
<mxCell id="a1r" value="Q18（v2.4 §5）：舊 bootstrap.sh 在已裝過的 repo 再跑 → 用 version.toml 第一行的引擎跑 install（不降版、不用內嵌）；該引擎拉不到 → 1 失敗，不得退回內嵌；只有第一次接入才用內嵌 ref" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bA" geo="1220,317,360,79"/>
<mxCell id="a1r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="1556,307,30,20"/>
<mxCell id="a1vy" value="是：引擎 ref = version.toml 第一行（拉不到 → 1，不退回內嵌）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="260,417,200,63"/>
<mxCell id="a1vy_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="436,407,30,20"/>
<mxCell id="a1vn" value="否：引擎 ref = 內嵌引擎 ref（第一次接入）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="520,424,200,48"/>
<mxCell id="a1vn_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="696,414,30,20"/>
<mxCell id="a5" value="--local？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="420,500,140,81"/>
<mxCell id="a8q" value="是：值含 / 或以 .tar 結尾？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="260,601,230,81"/>
<mxCell id="a8q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,591,30,20"/>
<mxCell id="a6i" value="否：docker image inspect &amp;lt;引擎 ref&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="540,618,180,48"/>
<mxCell id="a6i_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="696,608,30,20"/>
<mxCell id="a8ex" value="否 → 1：--local 指定的檔案不存在（請檢查路徑）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bA" geo="20,702,220,80"/>
<mxCell id="a8ex_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="216,692,30,20"/>
<mxCell id="a8e" value="是：該檔案存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="260,717,230,50"/>
<mxCell id="a8e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,707,30,20"/>
<mxCell id="a6q" value="本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="540,717,160,50"/>
<mxCell id="a6q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="676,707,30,20"/>
<mxCell id="a8tx" value="是 → 1：印 6-37（值既是既存檔案也可解讀為本機 image tag，請消歧）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bA" geo="20,802,220,102"/>
<mxCell id="a8tx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="216,792,30,20"/>
<mxCell id="a8t" value="是：本機也有同名 image tag？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="260,812,230,81"/>
<mxCell id="a8t_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,802,30,20"/>
<mxCell id="a6p" value="無：docker pull &amp;lt;引擎 ref&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="550,829,170,48"/>
<mxCell id="a6p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="696,819,30,20"/>
<mxCell id="a7" value="ghcr.io/…/vendor_kit:vN&lt;br&gt;（引擎 image；多架構 amd64+arm64）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bA" geo="1019,824,182,57"/>
<mxCell id="a8l" value="否：docker load &amp;lt;tar&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="260,924,230,40"/>
<mxCell id="a8l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,914,30,20"/>
<mxCell id="a8d" value="tar 形才讀同名 .digest 旁檔 = 正式 index digest（旁檔缺 → 1）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="260,984,230,48"/>
<mxCell id="a8d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,974,30,20"/>
<mxCell id="a8i" value="docker image inspect 取 image ID（tag 形 = 值即本機 image tag，不讀 .digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="260,1052,230,63"/>
<mxCell id="a8i_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="466,1042,30,20"/>
<mxCell id="a9" value="docker run &amp;lt;引擎&amp;gt; install（-y 轉發；本機 image 直接 run）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA" geo="340,1206,300,48"/>
<mxCell id="a9_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="616,1196,30,20"/>
<mxCell id="a9e" value="install（見「install（1）（2）」頁）：建／重寫 .vendor_kit/ 薄殼、根 justfile、根 .dockerignore" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bA" geo="740,1201,260,57"/>
<mxCell id="a9f" value="install 寫（見「install（1）（2）」頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bA" geo="1220,1135,360,189"/>
<mxCell id="a9f_0" value=".vendor_kit/ 薄殼四檔（首行自描述）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="8,26,169,42"/>
<mxCell id="a9f_1" value="version.toml 第一行（引擎 ref）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="183,26,169,42"/>
<mxCell id="a9f_2" value="gen/.stamp（引擎 ref）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="8,74,169,26"/>
<mxCell id="a9f_3" value="baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="183,74,169,26"/>
<mxCell id="a9f_4" value="根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="8,106,169,73"/>
<mxCell id="a9f_5" value="根 .dockerignore 三行（有 → 問後加）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a9f" geo="183,106,169,73"/>
<mxCell id="a9x" value="是 → 1：中止（第一次不留半成品；--local 檔未寫）" style="fillColor=#f8cecc;strokeColor=#000000" parent="bA" geo="20,1344,220,80"/>
<mxCell id="a9x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA" geo="216,1334,30,20"/>
<mxCell id="a9q" value="install 失敗？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA" geo="390,1344,200,81"/>
<mxCell id="a9z" value="否 ↓ 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add → 彙總" style="fillColor=none;strokeColor=none" parent="bA" geo="260,1445,460,42"/>
<mxCell id="ae1" edge="1" source="a0" target="a1"/>
<mxCell id="ae2" value="否" edge="1" source="a1" target="a2"/>
<mxCell id="ae3" value="是" edge="1" source="a1" target="a3"/>
<mxCell id="ae4" value="否" edge="1" source="a3" target="a4"/>
<mxCell id="ae5" value="是" edge="1" source="a3" target="a1v"/>
<mxCell id="ae5y" value="是" edge="1" source="a1v" target="a1vy"/>
<mxCell id="ae5n" value="否" edge="1" source="a1v" target="a1vn"/>
<mxCell id="ae5a" edge="1" source="a1vy" target="a5"/>
<mxCell id="ae5b" edge="1" source="a1vn" target="a5"/>
<mxCell id="ae6" value="是" edge="1" source="a5" target="a8q"/>
<mxCell id="ae7" value="否" edge="1" source="a5" target="a6i"/>
<mxCell id="ae8" value="是" edge="1" source="a8q" target="a8e"/>
<mxCell id="ae8n" value="否" edge="1" source="a8q" target="a8i"/>
<mxCell id="ae8e" value="否" edge="1" source="a8e" target="a8ex"/>
<mxCell id="ae8ey" value="是" edge="1" source="a8e" target="a8t"/>
<mxCell id="ae8t" value="是" edge="1" source="a8t" target="a8tx"/>
<mxCell id="ae8tn" value="否" edge="1" source="a8t" target="a8l"/>
<mxCell id="ae9" edge="1" source="a8l" target="a8d"/>
<mxCell id="ae9d" edge="1" source="a8d" target="a8i"/>
<mxCell id="ae6q" edge="1" source="a6i" target="a6q"/>
<mxCell id="ae6p" value="無" edge="1" source="a6q" target="a6p"/>
<mxCell id="ae10" value="拉" edge="1" source="a7" target="a6p"/>
<mxCell id="ae6y" value="有" edge="1" source="a6q" target="a9"/>
<mxCell id="ae11" edge="1" source="a8i" target="a9"/>
<mxCell id="ae11b" edge="1" source="a6p" target="a9"/>
<mxCell id="ae12" edge="1" source="a9" target="a9e"/>
<mxCell id="ae12f" value="寫" edge="1" source="a9e" target="a9f"/>
<mxCell id="ae13" edge="1" source="a9" target="a9q"/>
<mxCell id="ae14" value="是" edge="1" source="a9q" target="a9x"/>
<mxCell id="ae15" value="否" edge="1" source="a9q" target="a9z"/>
<mxCell id="p5_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1681,200,60"/>
<mxCell id="p5_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1681,140,64"/>
<mxCell id="p5_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1689,140,44"/>
<mxCell id="p5_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1683,190,56"/>
<mxCell id="p5_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1683,210,56"/>
<mxCell id="p5_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1691,88,40"/>
<mxCell id="p5_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1691,170,40"/>
<mxCell id="p5_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1681,300,60"/>
<mxCell id="p5_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1749,120,36"/>
<mxCell id="p5_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1749,150,36"/>
<mxCell id="p5_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1749,190,36"/>
<mxCell id="p5_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1749,170,36"/>
<mxCell id="p5_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1749,170,36"/>
<mxCell id="p5_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1749,200,36"/>
<mxCell id="p5_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1739,30,20"/>
<mxCell id="p5_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1787,200,28"/>
<mxCell id="p5_tk0" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1821,150,71"/>
<mxCell id="p5_tv0" value="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1821,610,71"/>
<mxCell id="p5_tk1" value="release／tar／.digest／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1892,150,55"/>
<mxCell id="p5_tv1" value="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1892,610,55"/>
<mxCell id="p5_tk2" value="--local &amp;lt;image tag 或 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1947,150,71"/>
<mxCell id="p5_tv2" value="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1947,610,71"/>
<mxCell id="p5_tk3" value="GHCR／image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2018,150,40"/>
<mxCell id="p5_tv3" value="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2018,610,40"/>
<mxCell id="p5_tk4" value="docker image inspect／image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2058,150,71"/>
<mxCell id="p5_tv4" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2058,610,71"/>
<mxCell id="p5_tk5" value="install／uninstall" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2129,150,55"/>
<mxCell id="p5_tv5" value="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2129,610,55"/>
<mxCell id="p5_tk6" value="冪等" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2184,150,40"/>
<mxCell id="p5_tv6" value="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2184,610,40"/>
<mxCell id="p5_tk7" value="薄殼 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2224,150,55"/>
<mxCell id="p5_tv7" value=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2224,610,55"/>
<mxCell id="p5_tk8" value="薄殼首行自描述（Q17）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2279,150,55"/>
<mxCell id="p5_tv8" value="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2279,610,55"/>
<mxCell id="p5_tk9" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1821,150,40"/>
<mxCell id="p5_tv9" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1821,610,40"/>
<mxCell id="p5_tk10" value="暫存目錄／原子替換" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1861,150,40"/>
<mxCell id="p5_tv10" value="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1861,610,40"/>
<mxCell id="p5_tk11" value="version.toml／version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1901,150,55"/>
<mxCell id="p5_tv11" value="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1901,610,55"/>
<mxCell id="p5_tk12" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1956,150,40"/>
<mxCell id="p5_tv12" value="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1956,610,40"/>
<mxCell id="p5_tk13" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1996,150,55"/>
<mxCell id="p5_tv13" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1996,610,55"/>
<mxCell id="p5_tk14" value="just／recipe／import／default" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2051,150,55"/>
<mxCell id="p5_tv14" value="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2051,610,55"/>
<mxCell id="p5_tk15" value="docker pull／run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2106,150,40"/>
<mxCell id="p5_tv15" value="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2106,610,40"/>
<mxCell id="p5_tk16" value="flock／-y" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2146,150,40"/>
<mxCell id="p5_tv16" value="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2146,610,40"/>
<mxCell id="p5_tk17" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2186,150,55"/>
<mxCell id="p5_tv17" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2186,610,55"/>
</diagram>
<diagram id="v1p5ccc" name="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add">
<mxCell id="title" value="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add → 彙總（§2、v2.2 C、v2.5 §8、v2.6 Q26／Q27）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,108"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,128,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,128,460,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="760,128,260,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1040,128,180,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,128,360,28"/>
<mxCell id="bA2" value="5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add（resolve → docker → apply；一個失敗即中止）→ 彙總結束碼；不自刪" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,172,1600,941"/>
<mxCell id="bA2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="1556,5,30,20"/>
<mxCell id="a9e2" value="來自「bootstrap.sh（1）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bA2" geo="340,36,300,102"/>
<mxCell id="a8q2" value="--local？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA2" geo="410,158,160,50"/>
<mxCell id="a8q2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="546,148,30,20"/>
<mxCell id="a8b" value="是：寫 version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋vendor_kit_image_id（install 成功後才寫）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA2" geo="520,228,200,79"/>
<mxCell id="a8b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="696,218,30,20"/>
<mxCell id="a8f" value="＋version.local.toml（不進 git；引擎覆寫：image tag + image ID；離線包 Q26）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bA2" geo="1220,246,360,42"/>
<mxCell id="a10" value="呼叫 add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y 轉發）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA2" geo="340,336,300,40"/>
<mxCell id="a10l" value="← 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 重複；一個失敗即中止" style="fillColor=none;strokeColor=none" parent="bA2" geo="1020,327,180,57"/>
<mxCell id="a10r" value="docker run &amp;lt;引擎&amp;gt; resolve add &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA2" geo="340,405,300,40"/>
<mxCell id="a10r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="616,395,30,20"/>
<mxCell id="a10re" value="resolve add（不寫任何檔；見「add（1）」頁）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bA2" geo="740,404,260,42"/>
<mxCell id="a10d" value="啟動器 docker 段：拉工具 image、展開 /dist 到暫存（步驟見「add（1）」頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA2" geo="340,466,300,48"/>
<mxCell id="a10d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="616,456,30,20"/>
<mxCell id="a10g" value="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（工具 image）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bA2" geo="1020,469,180,42"/>
<mxCell id="a10a" value="docker run &amp;lt;引擎&amp;gt; apply add &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bA2" geo="340,625,300,40"/>
<mxCell id="a10a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="616,615,30,20"/>
<mxCell id="a10ae" value="apply add（拿鎖、重驗、建日誌後寫入；見「add（2）」頁）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bA2" geo="740,624,260,42"/>
<mxCell id="a10f" value="add 寫（每個工具；見「add（2）」頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bA2" geo="1220,534,360,222"/>
<mxCell id="a10f_0" value="version.toml [tools] 行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,26,344,26"/>
<mxCell id="a10f_1" value="cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,58,344,26"/>
<mxCell id="a10f_2" value="gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,90,344,26"/>
<mxCell id="a10f_3" value="初始檔（init.toml 的 dest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,122,344,26"/>
<mxCell id="a10f_4" value="baseline/&amp;lt;repo&amp;gt;/ + .vendor_kit.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,154,344,26"/>
<mxCell id="a10f_5" value="gen/tools.just（重生，mod? 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="a10f" geo="8,186,344,26"/>
<mxCell id="a12" value="是 → 1：明列已完成／未完成（多工具彙總：1 &amp;gt; 2 &amp;gt; 0）" style="fillColor=#f8cecc;strokeColor=#000000" parent="bA2" geo="20,776,220,80"/>
<mxCell id="a12_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bA2" geo="216,766,30,20"/>
<mxCell id="a11" value="任一 add 失敗？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bA2" geo="390,776,200,81"/>
<mxCell id="a13" value="0：印摘要與要 git add 的清單" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bA2" geo="20,877,220,58"/>
<mxCell id="ae16" edge="1" source="a9e2" target="a8q2"/>
<mxCell id="ae17" value="是" edge="1" source="a8q2" target="a8b"/>
<mxCell id="ae17f" value="寫" edge="1" source="a8b" target="a8f"/>
<mxCell id="ae17n" value="否" edge="1" source="a8q2" target="a10"/>
<mxCell id="ae18" edge="1" source="a8b" target="a10"/>
<mxCell id="ae19" edge="1" source="a10" target="a10r"/>
<mxCell id="ae19e" edge="1" source="a10r" target="a10re"/>
<mxCell id="ae20" edge="1" source="a10r" target="a10d"/>
<mxCell id="ae20g" value="拉 /dist" edge="1" source="a10g" target="a10d"/>
<mxCell id="ae21" edge="1" source="a10d" target="a10a"/>
<mxCell id="ae21e" edge="1" source="a10a" target="a10ae"/>
<mxCell id="ae21f" value="寫" edge="1" source="a10ae" target="a10f"/>
<mxCell id="ae22" edge="1" source="a10a" target="a11"/>
<mxCell id="ae23" value="是" edge="1" source="a11" target="a12"/>
<mxCell id="ae24" value="否" edge="1" source="a11" target="a13"/>
<mxCell id="p5d_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1129,200,60"/>
<mxCell id="p5d_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1129,140,64"/>
<mxCell id="p5d_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1137,140,44"/>
<mxCell id="p5d_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1131,190,56"/>
<mxCell id="p5d_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1131,210,56"/>
<mxCell id="p5d_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1139,88,40"/>
<mxCell id="p5d_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1139,170,40"/>
<mxCell id="p5d_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1129,300,60"/>
<mxCell id="p5d_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1197,200,36"/>
<mxCell id="p5d_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1197,120,36"/>
<mxCell id="p5d_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1197,190,36"/>
<mxCell id="p5d_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1197,170,36"/>
<mxCell id="p5d_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1197,170,36"/>
<mxCell id="p5d_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1197,200,36"/>
<mxCell id="p5d_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1187,30,20"/>
<mxCell id="p5d_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1235,200,28"/>
<mxCell id="p5d_tk0" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1269,150,71"/>
<mxCell id="p5d_tv0" value="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1269,610,71"/>
<mxCell id="p5d_tk1" value="release／tar／.digest／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1340,150,55"/>
<mxCell id="p5d_tv1" value="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1340,610,55"/>
<mxCell id="p5d_tk2" value="--local &amp;lt;image tag 或 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1395,150,71"/>
<mxCell id="p5d_tv2" value="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1395,610,71"/>
<mxCell id="p5d_tk3" value="GHCR／image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1466,150,40"/>
<mxCell id="p5d_tv3" value="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1466,610,40"/>
<mxCell id="p5d_tk4" value="docker image inspect／image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1506,150,71"/>
<mxCell id="p5d_tv4" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1506,610,71"/>
<mxCell id="p5d_tk5" value="install／uninstall" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1577,150,55"/>
<mxCell id="p5d_tv5" value="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1577,610,55"/>
<mxCell id="p5d_tk6" value="冪等" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1632,150,40"/>
<mxCell id="p5d_tv6" value="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1632,610,40"/>
<mxCell id="p5d_tk7" value="薄殼 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1672,150,55"/>
<mxCell id="p5d_tv7" value=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1672,610,55"/>
<mxCell id="p5d_tk8" value="薄殼首行自描述（Q17）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1727,150,55"/>
<mxCell id="p5d_tv8" value="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1727,610,55"/>
<mxCell id="p5d_tk9" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1269,150,40"/>
<mxCell id="p5d_tv9" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1269,610,40"/>
<mxCell id="p5d_tk10" value="暫存目錄／原子替換" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1309,150,40"/>
<mxCell id="p5d_tv10" value="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1309,610,40"/>
<mxCell id="p5d_tk11" value="version.toml／version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1349,150,55"/>
<mxCell id="p5d_tv11" value="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1349,610,55"/>
<mxCell id="p5d_tk12" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1404,150,40"/>
<mxCell id="p5d_tv12" value="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1404,610,40"/>
<mxCell id="p5d_tk13" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1444,150,55"/>
<mxCell id="p5d_tv13" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1444,610,55"/>
<mxCell id="p5d_tk14" value="just／recipe／import／default" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1499,150,55"/>
<mxCell id="p5d_tv14" value="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1499,610,55"/>
<mxCell id="p5d_tk15" value="docker pull／run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1554,150,40"/>
<mxCell id="p5d_tv15" value="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1554,610,40"/>
<mxCell id="p5d_tk16" value="flock／-y" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1594,150,40"/>
<mxCell id="p5d_tv16" value="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1594,610,40"/>
<mxCell id="p5d_tk17" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1634,150,55"/>
<mxCell id="p5d_tv17" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1634,610,55"/>
</diagram>
<diagram id="v1p5c" name="流程 v2：install（1）薄殼">
<mxCell id="title" value="流程 v2：install ── 專案層動詞（§2／§3、v2.2 A／C、v2.4 Q17／Q20、v2.5 §8、v2.6 §4／§11／Q22 補）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,108"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,128,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,128,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,128,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,128,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,128,360,28"/>
<mxCell id="bI" value="5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.&amp;lt;id&amp;gt;.toml（v2.8 §2）；禁止巢狀（Q20）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,172,1600,1466"/>
<mxCell id="bI_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="1556,5,30,20"/>
<mxCell id="i0" value="just vendor_kit install（-y、--no-justfile）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bI" geo="20,36,220,80"/>
<mxCell id="i1" value="docker run &amp;lt;引擎&amp;gt; install …&lt;br&gt;（啟動器不鎖；鎖在引擎）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI" geo="260,55,280,42"/>
<mxCell id="i3" value="1：請先 git init（不代做）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bI" geo="20,136,220,58"/>
<mxCell id="i2" value="是 git repo？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI" geo="560,140,220,50"/>
<mxCell id="i2x" value="是 → 1：&amp;lt;dir&amp;gt; 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bI" geo="20,219,220,102"/>
<mxCell id="i2x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="216,209,30,20"/>
<mxCell id="i2n" value="上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI" geo="560,214,300,112"/>
<mxCell id="i2n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="836,204,30,20"/>
<mxCell id="i4a" value="否：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,346,400,40"/>
<mxCell id="i4a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,336,30,20"/>
<mxCell id="i4" value="產 .gitignore 到暫存（首行自描述）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,438,400,40"/>
<mxCell id="i4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,428,30,20"/>
<mxCell id="i4n" value="第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫到正式位置的檔，專案不留任何檔 → 1（「不留半成品」只對第一次成立，v2.2 C）；修復型 install：建 .vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾（install（2））後刪（v2.8 §2）" style="fillColor=#ffffff;strokeColor=#999999" parent="bI" geo="1220,406,360,104"/>
<mxCell id="i4_2" value="產 entry.just 到暫存（首行自描述）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,530,400,40"/>
<mxCell id="i4_2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,520,30,20"/>
<mxCell id="i4_3" value="產 vendor.just 到暫存（首行自描述）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,590,400,40"/>
<mxCell id="i4_3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,580,30,20"/>
<mxCell id="i4_4" value="產 ci/check.sh 到暫存（自描述在第二行）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,650,400,40"/>
<mxCell id="i4_4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,640,30,20"/>
<mxCell id="i4e" value="薄殼已存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI" geo="560,710,240,50"/>
<mxCell id="i4e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="776,700,30,20"/>
<mxCell id="i4en" value="否：第一次 = 全新建" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI" geo="830,711,130,48"/>
<mxCell id="i4en_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,701,30,20"/>
<mxCell id="i4x" value="否 → 1：被改過，列差異不動（git checkout 還原後再跑）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bI" geo="20,796,220,80"/>
<mxCell id="i4x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="216,786,30,20"/>
<mxCell id="i4q" value="薄殼 == 上次產物？（首行自描述 hash）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI" geo="560,780,240,112"/>
<mxCell id="i4q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="776,770,30,20"/>
<mxCell id="i4qn" value="自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）" style="fillColor=#ffffff;strokeColor=#999999" parent="bI" geo="1220,796,360,79"/>
<mxCell id="i4qn_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="1556,786,30,20"/>
<mxCell id="i4ld" value="第一次 install（薄殼原本不存在）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI" geo="560,912,240,112"/>
<mxCell id="i4ld_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="776,902,30,20"/>
<mxCell id="i4l" value="否（修復型）：建進度日誌 .tmp.install.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI" geo="785,944,175,48"/>
<mxCell id="i4l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,934,30,20"/>
<mxCell id="i4lf" value="＋.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI" geo="1220,936,360,63"/>
<mxCell id="i4lf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="1556,926,30,20"/>
<mxCell id="i4b" value="是：薄殼四檔逐檔原子替換（暫存 → 正式位置）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,1103,400,40"/>
<mxCell id="i4b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,1093,30,20"/>
<mxCell id="i4f" value="＋薄殼四檔（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI" geo="1220,1044,360,158"/>
<mxCell id="i4f_0" value=".vendor_kit/.gitignore" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="i4f" geo="8,26,344,26"/>
<mxCell id="i4f_1" value=".vendor_kit/entry.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="i4f" geo="8,58,344,26"/>
<mxCell id="i4f_2" value=".vendor_kit/vendor.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="i4f" geo="8,90,344,26"/>
<mxCell id="i4f_3" value=".vendor_kit/ci/check.sh" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="i4f" geo="8,122,344,26"/>
<mxCell id="i4c" value="寫 version.toml：第一行 = 引擎 ref（＋schema、written_by；已有則不動）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,1222,400,48"/>
<mxCell id="i4c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,1212,30,20"/>
<mxCell id="i4cf" value="＋version.toml（第一行引擎 ref、schema、written_by；進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI" geo="1220,1225,360,42"/>
<mxCell id="i4d" value="寫 gen/.stamp（只記引擎 ref）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,1290,400,40"/>
<mxCell id="i4d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,1280,30,20"/>
<mxCell id="i4df" value="＋gen/.stamp（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI" geo="1220,1290,360,40"/>
<mxCell id="i4g" value="建 baseline/.gitkeep（git 不追蹤空目錄；metadata 到 add 才建）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI" geo="560,1350,400,48"/>
<mxCell id="i4g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI" geo="936,1340,30,20"/>
<mxCell id="i4gf" value="＋baseline/.gitkeep（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI" geo="1220,1354,360,40"/>
<mxCell id="i5z" value="↓ 續「install（2）」頁：根 justfile 與根 .dockerignore" style="fillColor=none;strokeColor=none" parent="bI" geo="560,1418,300,42"/>
<mxCell id="ie1" edge="1" source="i0" target="i1"/>
<mxCell id="ie2" edge="1" source="i1" target="i2"/>
<mxCell id="ie3" value="否" edge="1" source="i2" target="i3"/>
<mxCell id="ie2n" value="是" edge="1" source="i2" target="i2n"/>
<mxCell id="ie2x" value="是" edge="1" source="i2n" target="i2x"/>
<mxCell id="ie4" value="否" edge="1" source="i2n" target="i4a"/>
<mxCell id="ie4b" edge="1" source="i4a" target="i4"/>
<mxCell id="ie4c" edge="1" source="i4" target="i4_2"/>
<mxCell id="ie4d" edge="1" source="i4_2" target="i4_3"/>
<mxCell id="ie4e" edge="1" source="i4_3" target="i4_4"/>
<mxCell id="ie5" edge="1" source="i4_4" target="i4e"/>
<mxCell id="ie5n" value="否" edge="1" source="i4e" target="i4en"/>
<mxCell id="ie5y" value="是" edge="1" source="i4e" target="i4q"/>
<mxCell id="ie5x" value="否" edge="1" source="i4q" target="i4x"/>
<mxCell id="ie6" value="是" edge="1" source="i4q" target="i4ld"/>
<mxCell id="ie6n" edge="1" source="i4en" target="i4ld"/>
<mxCell id="ie6l" value="否" edge="1" source="i4ld" target="i4l"/>
<mxCell id="ie6lf" value="寫" edge="1" source="i4l" target="i4lf"/>
<mxCell id="ie6ly" value="是" edge="1" source="i4ld" target="i4b"/>
<mxCell id="ie6ln" edge="1" source="i4l" target="i4b"/>
<mxCell id="ie6f" value="寫" edge="1" source="i4b" target="i4f"/>
<mxCell id="ie6c" edge="1" source="i4b" target="i4c"/>
<mxCell id="ie6cf" value="寫" edge="1" source="i4c" target="i4cf"/>
<mxCell id="ie6d" edge="1" source="i4c" target="i4d"/>
<mxCell id="ie6df" value="寫" edge="1" source="i4d" target="i4df"/>
<mxCell id="ie6g" edge="1" source="i4d" target="i4g"/>
<mxCell id="ie6gf" value="寫" edge="1" source="i4g" target="i4gf"/>
<mxCell id="ie7" edge="1" source="i4g" target="i5z"/>
<mxCell id="p5c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1654,200,60"/>
<mxCell id="p5c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1654,140,64"/>
<mxCell id="p5c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1662,140,44"/>
<mxCell id="p5c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1656,190,56"/>
<mxCell id="p5c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1656,210,56"/>
<mxCell id="p5c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1664,88,40"/>
<mxCell id="p5c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1664,170,40"/>
<mxCell id="p5c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1654,300,60"/>
<mxCell id="p5c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1722,120,36"/>
<mxCell id="p5c_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1722,190,36"/>
<mxCell id="p5c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1722,170,36"/>
<mxCell id="p5c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1722,170,36"/>
<mxCell id="p5c_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1722,200,36"/>
<mxCell id="p5c_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1712,30,20"/>
<mxCell id="p5c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1760,200,28"/>
<mxCell id="p5c_tk0" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1794,150,71"/>
<mxCell id="p5c_tv0" value="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1794,610,71"/>
<mxCell id="p5c_tk1" value="release／tar／.digest／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1865,150,55"/>
<mxCell id="p5c_tv1" value="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1865,610,55"/>
<mxCell id="p5c_tk2" value="--local &amp;lt;image tag 或 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1920,150,71"/>
<mxCell id="p5c_tv2" value="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1920,610,71"/>
<mxCell id="p5c_tk3" value="GHCR／image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1991,150,40"/>
<mxCell id="p5c_tv3" value="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1991,610,40"/>
<mxCell id="p5c_tk4" value="docker image inspect／image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2031,150,71"/>
<mxCell id="p5c_tv4" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2031,610,71"/>
<mxCell id="p5c_tk5" value="install／uninstall" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2102,150,55"/>
<mxCell id="p5c_tv5" value="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2102,610,55"/>
<mxCell id="p5c_tk6" value="冪等" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2157,150,40"/>
<mxCell id="p5c_tv6" value="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2157,610,40"/>
<mxCell id="p5c_tk7" value="薄殼 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2197,150,55"/>
<mxCell id="p5c_tv7" value=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2197,610,55"/>
<mxCell id="p5c_tk8" value="薄殼首行自描述（Q17）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2252,150,55"/>
<mxCell id="p5c_tv8" value="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2252,610,55"/>
<mxCell id="p5c_tk9" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1794,150,40"/>
<mxCell id="p5c_tv9" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1794,610,40"/>
<mxCell id="p5c_tk10" value="暫存目錄／原子替換" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1834,150,40"/>
<mxCell id="p5c_tv10" value="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1834,610,40"/>
<mxCell id="p5c_tk11" value="version.toml／version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1874,150,55"/>
<mxCell id="p5c_tv11" value="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1874,610,55"/>
<mxCell id="p5c_tk12" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1929,150,40"/>
<mxCell id="p5c_tv12" value="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1929,610,40"/>
<mxCell id="p5c_tk13" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1969,150,55"/>
<mxCell id="p5c_tv13" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1969,610,55"/>
<mxCell id="p5c_tk14" value="just／recipe／import／default" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2024,150,55"/>
<mxCell id="p5c_tv14" value="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2024,610,55"/>
<mxCell id="p5c_tk15" value="docker pull／run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2079,150,40"/>
<mxCell id="p5c_tv15" value="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2079,610,40"/>
<mxCell id="p5c_tk16" value="flock／-y" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2119,150,40"/>
<mxCell id="p5c_tv16" value="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2119,610,40"/>
<mxCell id="p5c_tk17" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2159,150,55"/>
<mxCell id="p5c_tv17" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2159,610,55"/>
</diagram>
<diagram id="v1p5cc" name="流程 v2：install（2）根 justfile 與 .dockerignore">
<mxCell id="title" value="流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22 補）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,108"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,128,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,128,140,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="440,128,560,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1020,128,200,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,128,360,28"/>
<mxCell id="bI2" value="5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建三行；有 → 問後 append）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,172,1600,1270"/>
<mxCell id="bI2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,5,30,20"/>
<mxCell id="i5e" value="來自「install（1）」頁：薄殼與 .vendor_kit/ 各檔已寫" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bI2" geo="420,70,300,58"/>
<mxCell id="i5" value="--no-justfile？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,148,300,50"/>
<mxCell id="i5_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="696,138,30,20"/>
<mxCell id="i6" value="否 → 有根 justfile？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,224,300,81"/>
<mxCell id="i7" value="無：建 justfile（四行，逐字見右）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI2" geo="860,236,120,57"/>
<mxCell id="i7f" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋justfile（新建，逐字四行；recipe 本體以 tab 縮排）&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;br&gt;&lt;br&gt;default:&lt;br&gt;&#9;@just --list&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#666666;dashed=1" parent="bI2" geo="1220,218,360,94"/>
<mxCell id="i7f_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,208,30,20"/>
<mxCell id="i8" value="有 → 已含 import 那行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,332,300,81"/>
<mxCell id="i8_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="696,322,30,20"/>
<mxCell id="i12" value="否 → 問「要在 justfile 加這一行嗎」同意？（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,433,300,112"/>
<mxCell id="i11" value="是：append 那一行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI2" geo="860,468,120,42"/>
<mxCell id="i11f" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;justfile（尾端＋一行）：&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#666666;dashed=1" parent="bI2" geo="1220,465,360,48"/>
<mxCell id="i11f_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,455,30,20"/>
<mxCell id="im" value="印 justfile 結果（建了／加了一行／跳過／已含不再加／拒絕不動）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI2" geo="360,565,360,42"/>
<mxCell id="ig" value="有根 .dockerignore？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,627,250,81"/>
<mxCell id="ig_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="646,617,30,20"/>
<mxCell id="ign" value="無：建 .dockerignore（三行，逐字見右）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI2" geo="860,628,120,79"/>
<mxCell id="ign_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="956,618,30,20"/>
<mxCell id="ignf" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋.dockerignore（新建，三行）：&lt;br&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#666666;dashed=1" parent="bI2" geo="1220,628,360,79"/>
<mxCell id="ignf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,618,30,20"/>
<mxCell id="igx" value="否 → 0：不寫 .dockerignore、印指示（含 justfile 結果；修復型先刪進度日誌）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bI2" geo="20,764,220,102"/>
<mxCell id="igx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="216,754,30,20"/>
<mxCell id="igq" value="有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bI2" geo="420,728,250,174"/>
<mxCell id="igq_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="646,718,30,20"/>
<mxCell id="igz" value="0：印建立了什麼（含 justfile 結果；修復型先刪進度日誌）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bI2" geo="860,742,120,146"/>
<mxCell id="igz_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="956,732,30,20"/>
<mxCell id="igy" value="是：append 三行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bI2" geo="420,942,250,40"/>
<mxCell id="igy_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="646,932,30,20"/>
<mxCell id="igyf" value="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.dockerignore（尾端＋三行；Q22 補）：&lt;br&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;" style="fillColor=#ffffff;strokeColor=#666666;dashed=1" parent="bI2" geo="1220,922,360,79"/>
<mxCell id="igyf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,912,30,20"/>
<mxCell id="igm" value="插入的行記在 baseline/.vendor_kit.toml（lines）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI2" geo="420,1021,250,63"/>
<mxCell id="igm_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="646,1011,30,20"/>
<mxCell id="igmf" value="baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI2" geo="1220,1028,360,48"/>
<mxCell id="igmf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,1018,30,20"/>
<mxCell id="idl" value="刪進度日誌 .tmp.install.&amp;lt;id&amp;gt;.toml（修復型才有；最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bI2" geo="420,1104,250,48"/>
<mxCell id="idl_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="646,1094,30,20"/>
<mxCell id="idlf" value="－.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml（修復型才有）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bI2" geo="1220,1108,360,40"/>
<mxCell id="idlf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bI2" geo="1556,1098,30,20"/>
<mxCell id="iz" value="0：印建立／修改了什麼（含加的行）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bI2" geo="20,1172,220,58"/>
<mxCell id="ie7" edge="1" source="i5e" target="i5"/>
<mxCell id="ie8" value="是" edge="1" source="i5" target="im"/>
<mxCell id="ie9" value="否" edge="1" source="i5" target="i6"/>
<mxCell id="ie10" value="無" edge="1" source="i6" target="i7"/>
<mxCell id="ie11" value="寫" edge="1" source="i7" target="i7f"/>
<mxCell id="ie12" value="有" edge="1" source="i6" target="i8"/>
<mxCell id="ie13" edge="1" source="i7" target="im"/>
<mxCell id="ie13b" value="是" edge="1" source="i8" target="im"/>
<mxCell id="ie14" value="否" edge="1" source="i8" target="i12"/>
<mxCell id="ie17" value="是" edge="1" source="i12" target="i11"/>
<mxCell id="ie18" value="否" edge="1" source="i12" target="im"/>
<mxCell id="ie16f" value="寫" edge="1" source="i11" target="i11f"/>
<mxCell id="ie19d" edge="1" source="i11" target="im"/>
<mxCell id="ie19" edge="1" source="im" target="ig"/>
<mxCell id="ie20" value="無" edge="1" source="ig" target="ign"/>
<mxCell id="ie20f" value="寫" edge="1" source="ign" target="ignf"/>
<mxCell id="ie21" value="有" edge="1" source="ig" target="igq"/>
<mxCell id="ie20z" edge="1" source="ign" target="igz"/>
<mxCell id="ie22" value="否" edge="1" source="igq" target="igx"/>
<mxCell id="ie23" value="是" edge="1" source="igq" target="igy"/>
<mxCell id="ie23f" value="寫" edge="1" source="igy" target="igyf"/>
<mxCell id="ie23m" edge="1" source="igy" target="igm"/>
<mxCell id="ie23mf" value="寫" edge="1" source="igm" target="igmf"/>
<mxCell id="ie24" edge="1" source="igm" target="idl"/>
<mxCell id="ie24f" value="刪" edge="1" source="idl" target="idlf"/>
<mxCell id="ie25" edge="1" source="idl" target="iz"/>
<mxCell id="p5cc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1458,200,60"/>
<mxCell id="p5cc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1458,140,64"/>
<mxCell id="p5cc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1466,140,44"/>
<mxCell id="p5cc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1460,190,56"/>
<mxCell id="p5cc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1460,210,56"/>
<mxCell id="p5cc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1468,88,40"/>
<mxCell id="p5cc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1468,170,40"/>
<mxCell id="p5cc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1458,300,60"/>
<mxCell id="p5cc_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1526,200,36"/>
<mxCell id="p5cc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1526,120,36"/>
<mxCell id="p5cc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1526,190,36"/>
<mxCell id="p5cc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1526,170,36"/>
<mxCell id="p5cc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1526,170,36"/>
<mxCell id="p5cc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1526,200,36"/>
<mxCell id="p5cc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1516,30,20"/>
<mxCell id="p5cc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1564,200,28"/>
<mxCell id="p5cc_tk0" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1598,150,71"/>
<mxCell id="p5cc_tv0" value="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1598,610,71"/>
<mxCell id="p5cc_tk1" value="release／tar／.digest／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1669,150,55"/>
<mxCell id="p5cc_tv1" value="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1669,610,55"/>
<mxCell id="p5cc_tk2" value="--local &amp;lt;image tag 或 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1724,150,71"/>
<mxCell id="p5cc_tv2" value="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1724,610,71"/>
<mxCell id="p5cc_tk3" value="GHCR／image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1795,150,40"/>
<mxCell id="p5cc_tv3" value="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1795,610,40"/>
<mxCell id="p5cc_tk4" value="docker image inspect／image ID" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1835,150,71"/>
<mxCell id="p5cc_tv4" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1835,610,71"/>
<mxCell id="p5cc_tk5" value="install／uninstall" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1906,150,55"/>
<mxCell id="p5cc_tv5" value="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1906,610,55"/>
<mxCell id="p5cc_tk6" value="冪等" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1961,150,40"/>
<mxCell id="p5cc_tv6" value="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1961,610,40"/>
<mxCell id="p5cc_tk7" value="薄殼 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2001,150,55"/>
<mxCell id="p5cc_tv7" value=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2001,610,55"/>
<mxCell id="p5cc_tk8" value="薄殼首行自描述（Q17）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2056,150,55"/>
<mxCell id="p5cc_tv8" value="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2056,610,55"/>
<mxCell id="p5cc_tk9" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1598,150,40"/>
<mxCell id="p5cc_tv9" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1598,610,40"/>
<mxCell id="p5cc_tk10" value="暫存目錄／原子替換" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1638,150,40"/>
<mxCell id="p5cc_tv10" value="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1638,610,40"/>
<mxCell id="p5cc_tk11" value="version.toml／version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1678,150,55"/>
<mxCell id="p5cc_tv11" value="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1678,610,55"/>
<mxCell id="p5cc_tk12" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1733,150,40"/>
<mxCell id="p5cc_tv12" value="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1733,610,40"/>
<mxCell id="p5cc_tk13" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1773,150,55"/>
<mxCell id="p5cc_tv13" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1773,610,55"/>
<mxCell id="p5cc_tk14" value="just／recipe／import／default" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1828,150,55"/>
<mxCell id="p5cc_tv14" value="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1828,610,55"/>
<mxCell id="p5cc_tk15" value="docker pull／run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1883,150,40"/>
<mxCell id="p5cc_tv15" value="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1883,610,40"/>
<mxCell id="p5cc_tk16" value="flock／-y" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1923,150,40"/>
<mxCell id="p5cc_tv16" value="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1923,610,40"/>
<mxCell id="p5cc_tk17" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1963,150,55"/>
<mxCell id="p5cc_tv17" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1963,610,55"/>
</diagram>
<diagram id="v1p5b" name="流程 v2：add（1）resolve → docker">
<mxCell id="title" value="流程 v2：add &amp;lt;repo&amp;gt;（1）resolve → 啟動器 docker（§2／§5、v2.2 C／E、v2.5 §2／§3／§5）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="bB" value="5b add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（bootstrap.sh 對每個 -t 呼叫；使用者也直接打）= 引擎 resolve（不寫；私有 image 未指定 @&amp;lt;tag&amp;gt; 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；續「add（1′）」「add（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1257"/>
<mxCell id="bB_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="1556,5,30,20"/>
<mxCell id="c0" value="just vendor_kit add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y、--dry-run…）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bB" geo="20,36,220,80"/>
<mxCell id="c1" value="docker run &amp;lt;引擎&amp;gt; resolve add &amp;lt;repo&amp;gt;（--local：tar 先 docker load，讀同名 .digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="260,44,280,63"/>
<mxCell id="c1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="516,34,30,20"/>
<mxCell id="c2a" value="resolve（不寫任何檔）：讀 version.toml" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB" geo="560,56,400,40"/>
<mxCell id="c2a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="936,46,30,20"/>
<mxCell id="c2b" value="查 tag（預設最新正式版／@&amp;lt;tag&amp;gt;）與 index digest（--source 改來源）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB" geo="560,140,400,48"/>
<mxCell id="c2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="936,130,30,20"/>
<mxCell id="c3" value="ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist&lt;br&gt;（工具 image；多架構 index digest）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bB" geo="980,136,220,57"/>
<mxCell id="c2px" value="是 → 1：印 6-3（私有 image：請指定 @&amp;lt;tag&amp;gt; 或提供 registry 憑證）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB" geo="20,213,220,102"/>
<mxCell id="c2px_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="216,203,30,20"/>
<mxCell id="c2pq" value="私有 image 且未指定 @&amp;lt;tag&amp;gt; 且無憑證？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB" geo="560,224,310,81"/>
<mxCell id="c2pq_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="846,214,30,20"/>
<mxCell id="c4" value="已接入 &amp;lt;repo&amp;gt;？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB" geo="560,335,310,50"/>
<mxCell id="c5" value="metadata 有完成標記？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB" geo="560,405,310,50"/>
<mxCell id="c6x" value="是 → 1：@&amp;lt;tag&amp;gt; 與鎖定不同，請改用 upgrade" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB" geo="20,486,220,58"/>
<mxCell id="c6x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="216,476,30,20"/>
<mxCell id="c5t" value="@&amp;lt;tag&amp;gt; 與鎖定不同？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB" geo="605,475,220,81"/>
<mxCell id="c8" value="否：續作，只做缺的步驟（不補刻意刪的檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="840,487,120,57"/>
<mxCell id="c6" value="否 → 0：已接入且完成，無變更" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bB" geo="20,576,220,58"/>
<mxCell id="c2c" value="resolve 完 → 產生執行計畫（要拉的 image@digest、mount、apply 與否）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB" geo="560,654,400,48"/>
<mxCell id="c2c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="936,644,30,20"/>
<mxCell id="c2d" value="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 計畫＋指紋以 stdout 回啟動器" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB" geo="560,722,400,48"/>
<mxCell id="c2d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="936,712,30,20"/>
<mxCell id="c9a" value="docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB" geo="260,790,170,143"/>
<mxCell id="c9a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="406,780,30,20"/>
<mxCell id="c9p" value="無：docker pull" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="440,953,100,48"/>
<mxCell id="c9p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="516,943,30,20"/>
<mxCell id="c9g" value="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（鎖定的那一版）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bB" geo="980,956,220,42"/>
<mxCell id="c9b" value="docker create &amp;lt;image&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="260,1021,280,40"/>
<mxCell id="c9b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="516,1011,30,20"/>
<mxCell id="c9c" value="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="260,1081,280,48"/>
<mxCell id="c9c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="516,1071,30,20"/>
<mxCell id="c9d" value="docker rm 該容器" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB" geo="260,1149,280,40"/>
<mxCell id="c9d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB" geo="516,1139,30,20"/>
<mxCell id="c9z" value="↓ 續「add（1′）」頁：docker run 引擎 apply add → 前置檢查" style="fillColor=none;strokeColor=none" parent="bB" geo="260,1209,280,42"/>
<mxCell id="cf_l" value="add 前 → 後（專案目錄，一格一檔；＋ = add 新增）" style="fillColor=none;strokeColor=none" parent="bB" geo="1220,40,340,26"/>
<mxCell id="cf0" value="add 前（install 後）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB" geo="1220,72,170,365"/>
<mxCell id="cf0_0" value="justfile（＋import 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,26,154,42"/>
<mxCell id="cf0_1" value=".dockerignore（＋三行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,74,154,42"/>
<mxCell id="cf0_2" value="version.toml（vendor_kit 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,122,154,42"/>
<mxCell id="cf0_3" value="version.local.toml（--local 時）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,170,154,42"/>
<mxCell id="cf0_4" value="薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,218,154,73"/>
<mxCell id="cf0_5" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,297,154,26"/>
<mxCell id="cf0_6" value="baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf0" geo="8,329,154,26"/>
<mxCell id="cf1" value="add 後（＋ = 新增）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB" geo="1410,81,170,347"/>
<mxCell id="cf1_0" value="＋version.toml [tools] &amp;lt;repo&amp;gt; 行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,26,154,42"/>
<mxCell id="cf1_1" value="＋cache/&amp;lt;repo&amp;gt;/（不進 git：files/、init.toml、just/）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,74,154,57"/>
<mxCell id="cf1_2" value="＋gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,137,154,26"/>
<mxCell id="cf1_3" value="＋初始檔（init.toml 的 dest；append 問後加）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,169,154,57"/>
<mxCell id="cf1_4" value="＋baseline/&amp;lt;repo&amp;gt;/ + .vendor_kit.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,232,154,42"/>
<mxCell id="cf1_5" value="＋gen/tools.just（每個 &amp;lt;ns&amp;gt;.just 一行 mod?）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="cf1" geo="8,280,154,57"/>
<mxCell id="ce1" edge="1" source="c0" target="c1"/>
<mxCell id="ce2" edge="1" source="c1" target="c2a"/>
<mxCell id="ce2b" edge="1" source="c2a" target="c2b"/>
<mxCell id="ce3" value="查" edge="1" source="c2b" target="c3"/>
<mxCell id="ce4p" edge="1" source="c2b" target="c2pq"/>
<mxCell id="ce4px" value="是" edge="1" source="c2pq" target="c2px"/>
<mxCell id="ce4" value="否" edge="1" source="c2pq" target="c4"/>
<mxCell id="ce5" value="是" edge="1" source="c4" target="c5"/>
<mxCell id="ce7" value="是" edge="1" source="c5" target="c5t"/>
<mxCell id="ce7b" value="否" edge="1" source="c5" target="c8"/>
<mxCell id="ce8" value="是" edge="1" source="c5t" target="c6x"/>
<mxCell id="ce9" value="否" edge="1" source="c5t" target="c6"/>
<mxCell id="ce10" value="否" edge="1" source="c4" target="c2c"/>
<mxCell id="ce11" edge="1" source="c8" target="c2c"/>
<mxCell id="ce12" edge="1" source="c2c" target="c2d"/>
<mxCell id="ce12a" edge="1" source="c2d" target="c9a"/>
<mxCell id="ce12n" value="無" edge="1" source="c9a" target="c9p"/>
<mxCell id="ce12g" value="拉 /dist" edge="1" source="c9g" target="c9p"/>
<mxCell id="ce12y" value="有" edge="1" source="c9a" target="c9b"/>
<mxCell id="ce12p" edge="1" source="c9p" target="c9b"/>
<mxCell id="ce12c" edge="1" source="c9b" target="c9c"/>
<mxCell id="ce12d" edge="1" source="c9c" target="c9d"/>
<mxCell id="ce13" edge="1" source="c9d" target="c9z"/>
<mxCell id="cfe" edge="1" source="cf0" target="cf1"/>
<mxCell id="p5b_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1414,200,60"/>
<mxCell id="p5b_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1414,140,64"/>
<mxCell id="p5b_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1422,140,44"/>
<mxCell id="p5b_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1416,190,56"/>
<mxCell id="p5b_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1416,210,56"/>
<mxCell id="p5b_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1424,88,40"/>
<mxCell id="p5b_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1424,170,40"/>
<mxCell id="p5b_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1414,300,60"/>
<mxCell id="p5b_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1482,120,36"/>
<mxCell id="p5b_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1482,150,36"/>
<mxCell id="p5b_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1482,190,36"/>
<mxCell id="p5b_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1482,170,36"/>
<mxCell id="p5b_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1482,170,36"/>
<mxCell id="p5b_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1482,200,36"/>
<mxCell id="p5b_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1472,30,20"/>
<mxCell id="p5b_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1520,200,28"/>
<mxCell id="p5b_tk0" value="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1554,150,71"/>
<mxCell id="p5b_tv0" value="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1554,610,71"/>
<mxCell id="p5b_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1625,150,40"/>
<mxCell id="p5b_tv1" value="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1625,610,40"/>
<mxCell id="p5b_tk2" value="stdout／stderr" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1665,150,40"/>
<mxCell id="p5b_tv2" value="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1665,610,40"/>
<mxCell id="p5b_tk3" value="輸入指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1705,150,40"/>
<mxCell id="p5b_tv3" value="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1705,610,40"/>
<mxCell id="p5b_tk4" value="GHCR／image／index digest／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1745,150,55"/>
<mxCell id="p5b_tv4" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1745,610,55"/>
<mxCell id="p5b_tk5" value="--local／tar／.digest（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1800,150,55"/>
<mxCell id="p5b_tv5" value="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1800,610,55"/>
<mxCell id="p5b_tk6" value="/dist/&amp;lt;repo&amp;gt;（暫存）／N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1855,150,40"/>
<mxCell id="p5b_tv6" value="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1855,610,40"/>
<mxCell id="p5b_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1895,150,40"/>
<mxCell id="p5b_tv7" value="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1895,610,40"/>
<mxCell id="p5b_tk8" value="初始檔／strategy" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1935,150,55"/>
<mxCell id="p5b_tv8" value="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1935,610,55"/>
<mxCell id="p5b_tk9" value="dest 撞名" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1990,150,40"/>
<mxCell id="p5b_tv9" value="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1990,610,40"/>
<mxCell id="p5b_tk10" value="命名空間撞名（v2.5 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1554,150,40"/>
<mxCell id="p5b_tv10" value="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1554,610,40"/>
<mxCell id="p5b_tk11" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1594,150,71"/>
<mxCell id="p5b_tv11" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1594,610,71"/>
<mxCell id="p5b_tk12" value="續作" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1665,150,28"/>
<mxCell id="p5b_tv12" value="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1665,610,28"/>
<mxCell id="p5b_tk13" value="gen／mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1693,150,71"/>
<mxCell id="p5b_tv13" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1693,610,71"/>
<mxCell id="p5b_tk14" value="CI 為真／frozen／dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1764,150,55"/>
<mxCell id="p5b_tv14" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1764,610,55"/>
<mxCell id="p5b_tk15" value="flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1819,150,28"/>
<mxCell id="p5b_tv15" value="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1819,610,28"/>
<mxCell id="p5b_tk16" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1847,150,28"/>
<mxCell id="p5b_tv16" value="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1847,610,28"/>
<mxCell id="p5b_tk17" value="CRLF" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1875,150,40"/>
<mxCell id="p5b_tv17" value="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1875,610,40"/>
<mxCell id="p5b_tk18" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1915,150,55"/>
<mxCell id="p5b_tv18" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1915,610,55"/>
</diagram>
<diagram id="v1p5bcc" name="流程 v2：add（1′）apply 前置">
<mxCell id="title" value="流程 v2：add &amp;lt;repo&amp;gt;（1′）apply 前置：拿鎖 → 重驗 → 檢查 → frozen → dry-run（v2.2 E、v2.5 §3／§5）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="bB1" value="5b′ add &amp;lt;repo&amp;gt; 的 apply 前置（承「add（1）」頁：工具 image 已展開到主機暫存）：docker run 引擎 apply → 拿鎖 → 重驗指紋 → dest 合法？→ 命名空間撞名？→ frozen → dry-run 分支；寫入段見「add（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,726"/>
<mxCell id="bB1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="1556,5,30,20"/>
<mxCell id="c9e" value="來自「add（1）」頁：/dist/&amp;lt;repo&amp;gt; 已在主機暫存" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bB1" geo="260,36,280,58"/>
<mxCell id="c10" value="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply add &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB1" geo="260,114,280,48"/>
<mxCell id="c10_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="516,104,30,20"/>
<mxCell id="c11a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB1" geo="560,118,400,40"/>
<mxCell id="c11a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="936,108,30,20"/>
<mxCell id="c11b" value="重驗 resolve 的輸入指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB1" geo="560,191,240,40"/>
<mxCell id="c11b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="776,181,30,20"/>
<mxCell id="c11x" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB1" geo="820,182,140,58"/>
<mxCell id="c11x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="936,172,30,20"/>
<mxCell id="c12x" value="否 → 1：dest 不合法（請修 init.toml／dest；需人動作）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB1" geo="20,260,220,80"/>
<mxCell id="c12x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="216,250,30,20"/>
<mxCell id="c12" value="init.toml 的 dest 全部合法？（任何寫入前檢查）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB1" geo="560,260,400,81"/>
<mxCell id="c12_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="936,250,30,20"/>
<mxCell id="c12r" value="dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/；dist 含 symlink → 拒絕" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bB1" geo="1220,261,360,79"/>
<mxCell id="c12r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="1556,251,30,20"/>
<mxCell id="c12bx" value="是 → 1：命名空間撞名（請改名／移除撞名者；需人動作）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB1" geo="20,377,220,80"/>
<mxCell id="c12bx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="216,367,30,20"/>
<mxCell id="c12b" value="just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB1" geo="560,361,400,112"/>
<mxCell id="c12b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="936,351,30,20"/>
<mxCell id="c12br" value="命名空間撞名（v2.5 §5）：&amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bB1" geo="1220,386,360,63"/>
<mxCell id="c12br_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="1556,376,30,20"/>
<mxCell id="c14x" value="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bB1" geo="20,494,220,80"/>
<mxCell id="c14x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="216,484,30,20"/>
<mxCell id="c14" value="CI 為真（frozen）且需改 tracked 檔？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB1" geo="590,493,340,81"/>
<mxCell id="c14_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="906,483,30,20"/>
<mxCell id="c13y" value="是 → 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/&amp;lt;repo&amp;gt;）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bB1" geo="20,594,220,80"/>
<mxCell id="c13y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB1" geo="216,584,30,20"/>
<mxCell id="c13" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB1" geo="640,609,240,50"/>
<mxCell id="c13z" value="否 ↓ 續「add（2）」頁：apply 寫入段" style="fillColor=none;strokeColor=none" parent="bB1" geo="560,694,300,26"/>
<mxCell id="ce13e" edge="1" source="c9e" target="c10"/>
<mxCell id="ce14" edge="1" source="c10" target="c11a"/>
<mxCell id="ce14b" edge="1" source="c11a" target="c11b"/>
<mxCell id="ce15" edge="1" source="c11b" target="c11x"/>
<mxCell id="ce16" edge="1" source="c11b" target="c12"/>
<mxCell id="ce17" value="否" edge="1" source="c12" target="c12x"/>
<mxCell id="ce18" value="是" edge="1" source="c12" target="c12b"/>
<mxCell id="ce18x" value="是" edge="1" source="c12b" target="c12bx"/>
<mxCell id="ce18b" value="否" edge="1" source="c12b" target="c14"/>
<mxCell id="ce19" value="是" edge="1" source="c14" target="c14x"/>
<mxCell id="ce20" value="否" edge="1" source="c14" target="c13"/>
<mxCell id="ce21" value="是" edge="1" source="c13" target="c13y"/>
<mxCell id="ce22" edge="1" source="c13" target="c13z"/>
<mxCell id="p5bp_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,883,200,60"/>
<mxCell id="p5bp_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,883,140,64"/>
<mxCell id="p5bp_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,891,140,44"/>
<mxCell id="p5bp_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,885,190,56"/>
<mxCell id="p5bp_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,885,210,56"/>
<mxCell id="p5bp_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,893,88,40"/>
<mxCell id="p5bp_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,893,170,40"/>
<mxCell id="p5bp_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,883,300,60"/>
<mxCell id="p5bp_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,951,200,36"/>
<mxCell id="p5bp_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,951,120,36"/>
<mxCell id="p5bp_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,951,150,36"/>
<mxCell id="p5bp_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="570,951,190,36"/>
<mxCell id="p5bp_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="780,951,170,36"/>
<mxCell id="p5bp_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,951,170,36"/>
<mxCell id="p5bp_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1160,951,200,36"/>
<mxCell id="p5bp_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1336,941,30,20"/>
<mxCell id="p5bp_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,989,200,28"/>
<mxCell id="p5bp_tk0" value="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1023,150,71"/>
<mxCell id="p5bp_tv0" value="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1023,610,71"/>
<mxCell id="p5bp_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1094,150,40"/>
<mxCell id="p5bp_tv1" value="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1094,610,40"/>
<mxCell id="p5bp_tk2" value="stdout／stderr" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1134,150,40"/>
<mxCell id="p5bp_tv2" value="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1134,610,40"/>
<mxCell id="p5bp_tk3" value="輸入指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1174,150,40"/>
<mxCell id="p5bp_tv3" value="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1174,610,40"/>
<mxCell id="p5bp_tk4" value="GHCR／image／index digest／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1214,150,55"/>
<mxCell id="p5bp_tv4" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1214,610,55"/>
<mxCell id="p5bp_tk5" value="--local／tar／.digest（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1269,150,55"/>
<mxCell id="p5bp_tv5" value="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1269,610,55"/>
<mxCell id="p5bp_tk6" value="/dist/&amp;lt;repo&amp;gt;（暫存）／N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1324,150,40"/>
<mxCell id="p5bp_tv6" value="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1324,610,40"/>
<mxCell id="p5bp_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1364,150,40"/>
<mxCell id="p5bp_tv7" value="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1364,610,40"/>
<mxCell id="p5bp_tk8" value="初始檔／strategy" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1404,150,55"/>
<mxCell id="p5bp_tv8" value="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1404,610,55"/>
<mxCell id="p5bp_tk9" value="dest 撞名" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1459,150,40"/>
<mxCell id="p5bp_tv9" value="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1459,610,40"/>
<mxCell id="p5bp_tk10" value="命名空間撞名（v2.5 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1023,150,40"/>
<mxCell id="p5bp_tv10" value="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1023,610,40"/>
<mxCell id="p5bp_tk11" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1063,150,71"/>
<mxCell id="p5bp_tv11" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1063,610,71"/>
<mxCell id="p5bp_tk12" value="續作" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1134,150,28"/>
<mxCell id="p5bp_tv12" value="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1134,610,28"/>
<mxCell id="p5bp_tk13" value="gen／mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1162,150,71"/>
<mxCell id="p5bp_tv13" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1162,610,71"/>
<mxCell id="p5bp_tk14" value="CI 為真／frozen／dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1233,150,55"/>
<mxCell id="p5bp_tv14" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1233,610,55"/>
<mxCell id="p5bp_tk15" value="flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1288,150,28"/>
<mxCell id="p5bp_tv15" value="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1288,610,28"/>
<mxCell id="p5bp_tk16" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1316,150,28"/>
<mxCell id="p5bp_tv16" value="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1316,610,28"/>
<mxCell id="p5bp_tk17" value="CRLF" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1344,150,40"/>
<mxCell id="p5bp_tv17" value="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1344,610,40"/>
<mxCell id="p5bp_tk18" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1384,150,55"/>
<mxCell id="p5bp_tv18" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1384,610,55"/>
</diagram>
<diagram id="v1p5bc" name="流程 v2：add（2）apply 寫入段">
<mxCell id="title" value="流程 v2：add &amp;lt;repo&amp;gt;（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="bB2" value="5b″ add &amp;lt;repo&amp;gt; 的 apply 寫入段（承「add（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → materialize → 印記 → 初始檔逐檔（每個 [[file]] 迴圈）→ baseline → metadata → tools.just → version.toml → 刪日誌" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1460"/>
<mxCell id="bB2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="1556,5,30,20"/>
<mxCell id="c13c" value="來自「add（1′）」頁：apply 檢查通過（非 dry-run）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bB2" geo="610,36,300,58"/>
<mxCell id="c15a" value="建進度日誌（metadata state=in-progress；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,115,400,40"/>
<mxCell id="c15a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,105,30,20"/>
<mxCell id="c15af" value="＋baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（state=in-progress）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,114,360,42"/>
<mxCell id="c15" value="materialize：/dist/&amp;lt;repo&amp;gt; 複製到暫存目錄" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,176,400,40"/>
<mxCell id="c15_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,166,30,20"/>
<mxCell id="c15c" value="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,236,400,40"/>
<mxCell id="c15c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,226,30,20"/>
<mxCell id="c15f" value="＋cache/&amp;lt;repo&amp;gt;/（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,236,360,40"/>
<mxCell id="c15b" value="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,296,400,48"/>
<mxCell id="c15b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,286,30,20"/>
<mxCell id="c15bf" value="＋gen/&amp;lt;repo&amp;gt;.stamp（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,300,360,40"/>
<mxCell id="cl" value="↓ 初始檔逐檔（init.toml 每個 [[file]]；範本讀 /dist/&amp;lt;repo&amp;gt;）" style="fillColor=none;strokeColor=none" parent="bB2" geo="680,364,280,42"/>
<mxCell id="c16" value="初始檔已存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB2" geo="560,440,200,50"/>
<mxCell id="c17" value="無：建該檔（state=managed）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB2" geo="810,444,150,42"/>
<mxCell id="cr" value="復原（v2.2 C、v2.5 §3）：進度日誌在第一個寫入前建立、最後一步刪除；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復（唯讀動詞只提示重跑）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bB2" geo="1220,426,360,79"/>
<mxCell id="cr_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="1556,416,30,20"/>
<mxCell id="c18" value="strategy = append？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB2" geo="560,525,200,81"/>
<mxCell id="c18_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="736,515,30,20"/>
<mxCell id="c19" value="否：不納管（state=unmanaged）、不覆蓋，印「已存在，範本在 cache」" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB2" geo="780,529,180,73"/>
<mxCell id="c20q" value="問「要在 X 加這幾行嗎」？（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB2" geo="560,626,320,81"/>
<mxCell id="c20q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="856,616,30,20"/>
<mxCell id="c20n" value="否：不寫；state=unmanaged 只記 declined_hash" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB2" geo="560,727,150,63"/>
<mxCell id="c20n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="686,717,30,20"/>
<mxCell id="c20" value="是：append 那幾行（state=appended；實際插入的行之後記進 metadata）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bB2" geo="750,730,210,57"/>
<mxCell id="c20l" value="還有下一個 [[file]]？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bB2" geo="610,810,300,81"/>
<mxCell id="c20l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="886,800,30,20"/>
<mxCell id="c21" value="否：寫 baseline/&amp;lt;repo&amp;gt;/（範本副本）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,911,400,40"/>
<mxCell id="c21f" value="＋baseline/&amp;lt;repo&amp;gt;/（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,911,360,40"/>
<mxCell id="c21b" value="寫 metadata：來源 ref@digest、最後合併版本（--local 另記 local_image_id）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,971,400,48"/>
<mxCell id="c21b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,961,30,20"/>
<mxCell id="c21bf" value="＋baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,975,360,40"/>
<mxCell id="c21c" value="寫 metadata：每個 dest 的 state（managed／appended／unmanaged；新檔被拒才 declined）、declined_hash、append 行（lines）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,1039,400,63"/>
<mxCell id="c21c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,1029,30,20"/>
<mxCell id="c21cf" value=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,1050,360,42"/>
<mxCell id="c21d" value="寫 metadata：完成標記（complete）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,1122,400,40"/>
<mxCell id="c21d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,1112,30,20"/>
<mxCell id="c21df" value=".vendor_kit.toml（complete = true）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,1122,360,40"/>
<mxCell id="c22" value="重生 gen/tools.just（每個 &amp;lt;ns&amp;gt;.just 一行 mod?；一工具可多行）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,1182,400,48"/>
<mxCell id="c22_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,1172,30,20"/>
<mxCell id="c22f" value="gen/tools.just（不進 git；mod? 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,1186,360,40"/>
<mxCell id="c23" value="最後寫 version.toml [tools]：&amp;lt;repo&amp;gt; = &quot;…:&amp;lt;tag&amp;gt;@sha256:…&quot;" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,1250,400,48"/>
<mxCell id="c23_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,1240,30,20"/>
<mxCell id="c23f" value="＋version.toml [tools] 行（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bB2" geo="1220,1254,360,40"/>
<mxCell id="c23x" value="失敗 → 1：明列已完成／未完成" style="fillColor=#f8cecc;strokeColor=#000000" parent="bB2" geo="20,1318,220,58"/>
<mxCell id="c23x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="216,1308,30,20"/>
<mxCell id="c23b" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bB2" geo="560,1327,400,40"/>
<mxCell id="c23b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bB2" geo="936,1317,30,20"/>
<mxCell id="c24" value="成功 → 0：印摘要，提示 git add" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bB2" geo="20,1396,220,58"/>
<mxCell id="ce23a" edge="1" source="c13c" target="c15a"/>
<mxCell id="ce23b" value="寫" edge="1" source="c15a" target="c15af"/>
<mxCell id="ce23c" edge="1" source="c15a" target="c15"/>
<mxCell id="ce23cc" edge="1" source="c15" target="c15c"/>
<mxCell id="ce23" value="寫" edge="1" source="c15c" target="c15f"/>
<mxCell id="ce23d" edge="1" source="c15c" target="c15b"/>
<mxCell id="ce23e" value="寫" edge="1" source="c15b" target="c15bf"/>
<mxCell id="ce24" edge="1" source="c15b" target="c16"/>
<mxCell id="ce25" value="無" edge="1" source="c16" target="c17"/>
<mxCell id="ce26" value="有" edge="1" source="c16" target="c18"/>
<mxCell id="ce27" value="否" edge="1" source="c18" target="c19"/>
<mxCell id="ce28" value="是" edge="1" source="c18" target="c20q"/>
<mxCell id="ce28n" value="否" edge="1" source="c20q" target="c20n"/>
<mxCell id="ce28y" value="是" edge="1" source="c20q" target="c20"/>
<mxCell id="ce29" edge="1" source="c17" target="c20l"/>
<mxCell id="ce30" edge="1" source="c19" target="c20l"/>
<mxCell id="ce31" edge="1" source="c20" target="c20l"/>
<mxCell id="ce31n" edge="1" source="c20n" target="c20l"/>
<mxCell id="ce31y" value="是" edge="1" source="c20l" target="c16"/>
<mxCell id="ce31l" value="否" edge="1" source="c20l" target="c21"/>
<mxCell id="ce32" value="寫" edge="1" source="c21" target="c21f"/>
<mxCell id="ce32b" edge="1" source="c21" target="c21b"/>
<mxCell id="ce32f" value="寫" edge="1" source="c21b" target="c21bf"/>
<mxCell id="ce32c" edge="1" source="c21b" target="c21c"/>
<mxCell id="ce32cf" value="寫" edge="1" source="c21c" target="c21cf"/>
<mxCell id="ce32d" edge="1" source="c21c" target="c21d"/>
<mxCell id="ce32df" value="寫" edge="1" source="c21d" target="c21df"/>
<mxCell id="ce33" edge="1" source="c21d" target="c22"/>
<mxCell id="ce34" value="寫" edge="1" source="c22" target="c22f"/>
<mxCell id="ce35" edge="1" source="c22" target="c23"/>
<mxCell id="ce36" value="寫" edge="1" source="c23" target="c23f"/>
<mxCell id="ce37" value="成功" edge="1" source="c23" target="c23b"/>
<mxCell id="ce38" value="失敗" edge="1" source="c23" target="c23x"/>
<mxCell id="ce39" edge="1" source="c23b" target="c24"/>
<mxCell id="p5bc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1617,200,60"/>
<mxCell id="p5bc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1617,140,64"/>
<mxCell id="p5bc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1625,140,44"/>
<mxCell id="p5bc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1619,190,56"/>
<mxCell id="p5bc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1619,210,56"/>
<mxCell id="p5bc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1627,88,40"/>
<mxCell id="p5bc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1627,170,40"/>
<mxCell id="p5bc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1617,300,60"/>
<mxCell id="p5bc_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1685,200,36"/>
<mxCell id="p5bc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1685,120,36"/>
<mxCell id="p5bc_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,1685,150,36"/>
<mxCell id="p5bc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="570,1685,190,36"/>
<mxCell id="p5bc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="780,1685,170,36"/>
<mxCell id="p5bc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,1685,170,36"/>
<mxCell id="p5bc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1160,1685,200,36"/>
<mxCell id="p5bc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1336,1675,30,20"/>
<mxCell id="p5bc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1723,200,28"/>
<mxCell id="p5bc_tk0" value="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1757,150,71"/>
<mxCell id="p5bc_tv0" value="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1757,610,71"/>
<mxCell id="p5bc_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1828,150,40"/>
<mxCell id="p5bc_tv1" value="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1828,610,40"/>
<mxCell id="p5bc_tk2" value="stdout／stderr" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1868,150,40"/>
<mxCell id="p5bc_tv2" value="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1868,610,40"/>
<mxCell id="p5bc_tk3" value="輸入指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1908,150,40"/>
<mxCell id="p5bc_tv3" value="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1908,610,40"/>
<mxCell id="p5bc_tk4" value="GHCR／image／index digest／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1948,150,55"/>
<mxCell id="p5bc_tv4" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1948,610,55"/>
<mxCell id="p5bc_tk5" value="--local／tar／.digest（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2003,150,55"/>
<mxCell id="p5bc_tv5" value="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2003,610,55"/>
<mxCell id="p5bc_tk6" value="/dist/&amp;lt;repo&amp;gt;（暫存）／N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2058,150,40"/>
<mxCell id="p5bc_tv6" value="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2058,610,40"/>
<mxCell id="p5bc_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2098,150,40"/>
<mxCell id="p5bc_tv7" value="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2098,610,40"/>
<mxCell id="p5bc_tk8" value="初始檔／strategy" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2138,150,55"/>
<mxCell id="p5bc_tv8" value="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2138,610,55"/>
<mxCell id="p5bc_tk9" value="dest 撞名" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2193,150,40"/>
<mxCell id="p5bc_tv9" value="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2193,610,40"/>
<mxCell id="p5bc_tk10" value="命名空間撞名（v2.5 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1757,150,40"/>
<mxCell id="p5bc_tv10" value="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1757,610,40"/>
<mxCell id="p5bc_tk11" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1797,150,71"/>
<mxCell id="p5bc_tv11" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1797,610,71"/>
<mxCell id="p5bc_tk12" value="續作" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1868,150,28"/>
<mxCell id="p5bc_tv12" value="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1868,610,28"/>
<mxCell id="p5bc_tk13" value="gen／mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1896,150,71"/>
<mxCell id="p5bc_tv13" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1896,610,71"/>
<mxCell id="p5bc_tk14" value="CI 為真／frozen／dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1967,150,55"/>
<mxCell id="p5bc_tv14" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1967,610,55"/>
<mxCell id="p5bc_tk15" value="flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2022,150,28"/>
<mxCell id="p5bc_tv15" value="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2022,610,28"/>
<mxCell id="p5bc_tk16" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2050,150,28"/>
<mxCell id="p5bc_tv16" value="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2050,610,28"/>
<mxCell id="p5bc_tk17" value="CRLF" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2078,150,40"/>
<mxCell id="p5bc_tv17" value="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2078,610,40"/>
<mxCell id="p5bc_tk18" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2118,150,55"/>
<mxCell id="p5bc_tv18" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2118,610,55"/>
</diagram>
<diagram id="v1p6" name="流程 v2：sync（1）啟動器快路徑">
<mxCell id="title" value="流程 v2：sync（1）啟動器：gen/.stamp 比對 → 快路徑（Q22）→ 起引擎（§6、v2.3 §2、v2.5 §9、v2.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="eA" value="sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 0 不起容器；有差 → docker image inspect → 引擎 resolve sync（見「sync（1′）」頁）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,857"/>
<mxCell id="eA_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="1556,5,30,20"/>
<mxCell id="n0" value="打工具 recipe（_sync 自動前置）或 just vendor_kit sync" style="fillColor=#d5e8d4;strokeColor=#000000" parent="eA" geo="20,51,220,80"/>
<mxCell id="n1" value="grep version.toml 第一行取引擎 ref（version.local.toml 的 vendor_kit 覆寫優先）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA" geo="260,60,280,63"/>
<mxCell id="n1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="516,50,30,20"/>
<mxCell id="n2" value="讀" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="eA" geo="1220,36,360,110"/>
<mxCell id="n2_0" value=".vendor_kit/version.toml（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="n2" geo="8,26,344,26"/>
<mxCell id="n2_1" value=".vendor_kit/version.local.toml（不進 git，dev 用）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="n2" geo="8,58,344,42"/>
<mxCell id="n3n" value="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="eA" geo="20,166,220,124"/>
<mxCell id="n3n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="216,156,30,20"/>
<mxCell id="n3" value="gen/.stamp 的引擎 ref ＝ 第一行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA" geo="260,172,260,112"/>
<mxCell id="n3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="496,162,30,20"/>
<mxCell id="n6" value="統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／upgrade vendor_kit 不受此關" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="eA" geo="1220,181,360,94"/>
<mxCell id="n6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="1556,171,30,20"/>
<mxCell id="nq0" value="是 → 0：不起容器，接著跑原本的 recipe（快路徑）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="eA" geo="20,325,220,80"/>
<mxCell id="nq0_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="216,315,30,20"/>
<mxCell id="nq" value="快路徑：grep 全相符且非 frozen？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA" geo="260,324,260,81"/>
<mxCell id="nq_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="496,314,30,20"/>
<mxCell id="nqr" value="快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；CI 不為真；sync 無參數。全相符 → 0；否則起引擎；每檔 sha256 只在 sync --verify、CI 為真、或版本變動的那次才做（§3.6）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="eA" geo="1220,310,360,110"/>
<mxCell id="nqr_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="1556,300,30,20"/>
<mxCell id="n1i" value="docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA" geo="280,440,220,112"/>
<mxCell id="n1i_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="476,430,30,20"/>
<mxCell id="n6b" value="薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與 upgrade vendor_kit 做；做之前比對現內容 == 上次產物（首行自描述 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="eA" geo="1220,456,360,79"/>
<mxCell id="n6b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="1556,446,30,20"/>
<mxCell id="n1p" value="無：docker pull &amp;lt;引擎 ref&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA" geo="460,572,80,79"/>
<mxCell id="n1p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="516,562,30,20"/>
<mxCell id="n1g" value="vendor_kit:vN@sha256:…&lt;br&gt;（引擎 image）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="eA" geo="980,590,220,42"/>
<mxCell id="n1v" value="覆寫中且 .Id ≠ 記的 image ID？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA" geo="280,671,220,112"/>
<mxCell id="n1v_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="476,661,30,20"/>
<mxCell id="n1x" value="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" style="fillColor=#f8cecc;strokeColor=#000000" parent="eA" geo="560,687,240,80"/>
<mxCell id="n1x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="776,677,30,20"/>
<mxCell id="n1b" value="否：docker run &amp;lt;引擎&amp;gt; resolve sync（永不 -t）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA" geo="260,803,280,48"/>
<mxCell id="n1b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA" geo="516,793,30,20"/>
<mxCell id="n1z" value="→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）" style="fillColor=none;strokeColor=none" parent="eA" geo="560,806,300,42"/>
<mxCell id="ne1" edge="1" source="n0" target="n1"/>
<mxCell id="ne2" value="讀" edge="1" source="n1" target="n2"/>
<mxCell id="ne3" edge="1" source="n1" target="n3"/>
<mxCell id="ne4" value="否" edge="1" source="n3" target="n3n"/>
<mxCell id="ne5" value="是" edge="1" source="n3" target="nq"/>
<mxCell id="ne5q" value="是" edge="1" source="nq" target="nq0"/>
<mxCell id="ne5n" value="否" edge="1" source="nq" target="n1i"/>
<mxCell id="ne5p" value="無" edge="1" source="n1i" target="n1p"/>
<mxCell id="ne5g" value="拉" edge="1" source="n1g" target="n1p"/>
<mxCell id="ne5v" value="有" edge="1" source="n1i" target="n1v"/>
<mxCell id="ne5pv" edge="1" source="n1p" target="n1v"/>
<mxCell id="ne5x" value="失敗" edge="1" source="n1p" target="n1x"/>
<mxCell id="ne5y" value="是" edge="1" source="n1v" target="n1x"/>
<mxCell id="ne5i" value="否" edge="1" source="n1v" target="n1b"/>
<mxCell id="ne6" edge="1" source="n1b" target="n1z"/>
<mxCell id="p6_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1029,200,60"/>
<mxCell id="p6_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1029,140,64"/>
<mxCell id="p6_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1037,140,44"/>
<mxCell id="p6_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1031,190,56"/>
<mxCell id="p6_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1031,210,56"/>
<mxCell id="p6_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1039,88,40"/>
<mxCell id="p6_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1039,170,40"/>
<mxCell id="p6_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1029,300,60"/>
<mxCell id="p6_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1097,120,36"/>
<mxCell id="p6_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1097,150,36"/>
<mxCell id="p6_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1097,190,36"/>
<mxCell id="p6_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1097,170,36"/>
<mxCell id="p6_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1097,170,36"/>
<mxCell id="p6_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1097,200,36"/>
<mxCell id="p6_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1087,30,20"/>
<mxCell id="p6_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1135,200,28"/>
<mxCell id="p6_tk0" value="sync" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1169,150,55"/>
<mxCell id="p6_tv0" value="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1169,610,55"/>
<mxCell id="p6_tk1" value="快路徑（Q22）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1224,150,71"/>
<mxCell id="p6_tv1" value="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1224,610,71"/>
<mxCell id="p6_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1295,150,55"/>
<mxCell id="p6_tv2" value="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1295,610,55"/>
<mxCell id="p6_tk3" value="stdout／stderr／指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1350,150,40"/>
<mxCell id="p6_tv3" value="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1350,610,40"/>
<mxCell id="p6_tk4" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1390,150,71"/>
<mxCell id="p6_tv4" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1390,610,71"/>
<mxCell id="p6_tk5" value="統一提示（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1461,150,55"/>
<mxCell id="p6_tv5" value="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1461,610,55"/>
<mxCell id="p6_tk6" value="薄殼／引擎 ref／hash" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1516,150,55"/>
<mxCell id="p6_tv6" value="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1516,610,55"/>
<mxCell id="p6_tk7" value="gen/ 三種檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1571,150,55"/>
<mxCell id="p6_tv7" value="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1571,610,55"/>
<mxCell id="p6_tk8" value="materialize／印記／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1626,150,55"/>
<mxCell id="p6_tv8" value="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1626,610,55"/>
<mxCell id="p6_tk9" value="image tag／digest／image ID／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1169,150,71"/>
<mxCell id="p6_tv9" value="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1169,610,71"/>
<mxCell id="p6_tk10" value="verify／sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1240,150,55"/>
<mxCell id="p6_tv10" value="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1240,610,55"/>
<mxCell id="p6_tk11" value="metadata／完成標記／落後" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1295,150,55"/>
<mxCell id="p6_tv11" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1295,610,55"/>
<mxCell id="p6_tk12" value="mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1350,150,55"/>
<mxCell id="p6_tv12" value="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1350,610,55"/>
<mxCell id="p6_tk13" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1405,150,40"/>
<mxCell id="p6_tv13" value="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1405,610,40"/>
<mxCell id="p6_tk14" value="覆寫兩種（v2.1 B／v2.2 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1445,150,55"/>
<mxCell id="p6_tv14" value="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1445,610,55"/>
<mxCell id="p6_tk15" value="GHCR／image／daemon／flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1500,150,40"/>
<mxCell id="p6_tv15" value="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1500,610,40"/>
<mxCell id="p6_tk16" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1540,150,55"/>
<mxCell id="p6_tv16" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1540,610,55"/>
</diagram>
<diagram id="v1p6cc" name="流程 v2：sync（1′）引擎 resolve">
<mxCell id="title" value="流程 v2：sync（1′）引擎 resolve sync（逐工具；§6、v2.2 A／B／E、v2.3 §3／§4、v2.5 §9、v2.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="eA2" value="sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 逐工具算待辦 → 無待辦（apply|no）→ 0；有待辦 → 第 2 段見「sync（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,1523"/>
<mxCell id="eA2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="1556,5,30,20"/>
<mxCell id="n1e" value="來自「sync（1）」頁：docker run &amp;lt;引擎&amp;gt; resolve sync" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="eA2" geo="610,36,300,58"/>
<mxCell id="ncx" value="是 → 1：CI 拒絕本機覆寫（frozen；請先 undev 或勿在 CI 用 local 覆寫）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="eA2" geo="20,114,220,102"/>
<mxCell id="ncx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="216,104,30,20"/>
<mxCell id="nc" value="CI 為真（frozen）且有 local 覆寫？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,124,330,81"/>
<mxCell id="nc_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="866,114,30,20"/>
<mxCell id="nf" value="frozen（CI 為真 = CI 非空且不為 0／false；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；任何需要寫 tracked 檔 → 1（-y 不解除）；升為失敗的警告：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="eA2" geo="1220,126,360,79"/>
<mxCell id="nf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="1556,116,30,20"/>
<mxCell id="nl" value="← 對每個工具重複&lt;br&gt;（範圍 = 全部；先比印記，便宜）" style="fillColor=none;strokeColor=none" parent="eA2" geo="980,262,220,42"/>
<mxCell id="t0" value="path 覆寫（dev 中）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,242,250,81"/>
<mxCell id="t0_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="786,232,30,20"/>
<mxCell id="t0s" value="是：跳過 materialize／verify，仍查 metadata、baseline ↓" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="830,236,130,94"/>
<mxCell id="t0s_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,226,30,20"/>
<mxCell id="t0r" value="覆寫兩種（v2.1 B）：引擎 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache/&amp;lt;repo&amp;gt;/ 是 symlink，跳過 materialize／verify" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="eA2" geo="1220,244,360,79"/>
<mxCell id="t0r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="1556,234,30,20"/>
<mxCell id="t1" value="cache 缺或印記 ≠ 鎖定 digest？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,350,250,81"/>
<mxCell id="t1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="786,340,30,20"/>
<mxCell id="t1y" value="是：列待辦「materialize 鎖定版」（不 verify 舊 cache）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="830,351,130,79"/>
<mxCell id="t1y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,341,30,20"/>
<mxCell id="t2q" value="否 → sync --verify、CI 為真、版本變動那次？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,451,250,112"/>
<mxCell id="t2q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="786,441,30,20"/>
<mxCell id="t2qn" value="否：不逐檔驗（快）↓" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="830,483,130,48"/>
<mxCell id="t2qn_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,473,30,20"/>
<mxCell id="t2" value="是 → verify：每檔 sha256 ＝ 印記？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,583,250,112"/>
<mxCell id="t2n" value="否：列待辦「重裝 + warn（cache 被改過）」" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="830,610,130,57"/>
<mxCell id="t3a" value="否 → 1：「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="eA2" geo="20,715,220,102"/>
<mxCell id="t3" value="metadata 有完成標記？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,726,250,81"/>
<mxCell id="t3r" value="不變量（v2.1 A、v2.5 §9）：自動化不碰使用者的檔 —— sync 不寫 version.toml、初始檔、baseline、薄殼、gen/.stamp；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=#b85450" parent="eA2" geo="1220,726,360,79"/>
<mxCell id="t3r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="1556,716,30,20"/>
<mxCell id="t4" value="最後合併版本 ＝ version.toml？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,837,250,81"/>
<mxCell id="t4r" value="是 → 1：baseline 落後，印「請在本機執行 just vendor_kit upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="eA2" geo="20,938,220,124"/>
<mxCell id="t4c" value="否（落後）→ CI 為真（frozen）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,960,250,81"/>
<mxCell id="t5" value="否：warn「baseline 落後，請 just vendor_kit upgrade &amp;lt;repo&amp;gt;」（繼續）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="560,1082,300,42"/>
<mxCell id="t6" value="gen/tools.just 缺或與工具清單不符？（全部工具看完後）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eA2" geo="560,1144,270,143"/>
<mxCell id="t6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="806,1134,30,20"/>
<mxCell id="t6y" value="是：列待辦「重生 gen/tools.just」" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eA2" geo="843,1184,117,63"/>
<mxCell id="t6y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,1174,30,20"/>
<mxCell id="z0" value="resolve 完：產生待辦清單（要拉的 image、要重裝、要重生 gen/tools.just）→ 空 = apply|no" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eA2" geo="560,1307,400,48"/>
<mxCell id="z0_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,1297,30,20"/>
<mxCell id="z2" value="無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe" style="fillColor=#d5e8d4;strokeColor=#000000" parent="eA2" geo="20,1375,220,80"/>
<mxCell id="z2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="216,1365,30,20"/>
<mxCell id="z1" value="產生輸入指紋（version.toml、metadata、印記 hash）→ 清單＋指紋＋apply|yes／no 以 stdout 回啟動器" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eA2" geo="560,1391,400,48"/>
<mxCell id="z1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eA2" geo="936,1381,30,20"/>
<mxCell id="mb" value="有待辦 ↓ 續「sync（2）」頁：啟動器 docker → 引擎 apply sync" style="fillColor=none;strokeColor=none" parent="eA2" geo="560,1475,400,42"/>
<mxCell id="ne6" edge="1" source="n1e" target="nc"/>
<mxCell id="ne7" value="是" edge="1" source="nc" target="ncx"/>
<mxCell id="ne8" value="否" edge="1" source="nc" target="t0"/>
<mxCell id="te0" value="是" edge="1" source="t0" target="t0s"/>
<mxCell id="te1" value="否" edge="1" source="t0" target="t1"/>
<mxCell id="te2" edge="1" source="t0s" target="t3"/>
<mxCell id="te3" value="是" edge="1" source="t1" target="t1y"/>
<mxCell id="te4" value="否" edge="1" source="t1" target="t2q"/>
<mxCell id="te5" edge="1" source="t1y" target="t3"/>
<mxCell id="te3q" value="否" edge="1" source="t2q" target="t2qn"/>
<mxCell id="te4q" value="是" edge="1" source="t2q" target="t2"/>
<mxCell id="te5q" edge="1" source="t2qn" target="t3"/>
<mxCell id="te6" value="否" edge="1" source="t2" target="t2n"/>
<mxCell id="te7" value="是" edge="1" source="t2" target="t3"/>
<mxCell id="te8" edge="1" source="t2n" target="t3"/>
<mxCell id="te9" value="否" edge="1" source="t3" target="t3a"/>
<mxCell id="te10" value="是" edge="1" source="t3" target="t4"/>
<mxCell id="te11" value="否" edge="1" source="t4" target="t4c"/>
<mxCell id="te12" value="是" edge="1" source="t4c" target="t4r"/>
<mxCell id="te13" value="否" edge="1" source="t4c" target="t5"/>
<mxCell id="te14" value="是" edge="1" source="t4" target="t6"/>
<mxCell id="te15" edge="1" source="t5" target="t6"/>
<mxCell id="te16" value="是" edge="1" source="t6" target="t6y"/>
<mxCell id="te17" value="否" edge="1" source="t6" target="z0"/>
<mxCell id="te18" edge="1" source="t6y" target="z0"/>
<mxCell id="ze0" edge="1" source="z0" target="z1"/>
<mxCell id="ze1" value="無待辦" edge="1" source="z1" target="z2"/>
<mxCell id="ze2" edge="1" source="z1" target="mb"/>
<mxCell id="p6r_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1695,200,60"/>
<mxCell id="p6r_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1695,140,64"/>
<mxCell id="p6r_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1703,140,44"/>
<mxCell id="p6r_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1697,190,56"/>
<mxCell id="p6r_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1697,210,56"/>
<mxCell id="p6r_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1705,88,40"/>
<mxCell id="p6r_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1705,170,40"/>
<mxCell id="p6r_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1695,300,60"/>
<mxCell id="p6r_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1763,200,36"/>
<mxCell id="p6r_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1763,120,36"/>
<mxCell id="p6r_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,1763,150,36"/>
<mxCell id="p6r_lgx_inv" value="紅粗框：不變量" style="fillColor=#ffffff;strokeColor=#b85450" geo="570,1763,130,36"/>
<mxCell id="p6r_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="720,1763,190,36"/>
<mxCell id="p6r_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="930,1763,170,36"/>
<mxCell id="p6r_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,1763,170,36"/>
<mxCell id="p6r_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1310,1763,200,36"/>
<mxCell id="p6r_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1486,1753,30,20"/>
<mxCell id="p6r_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1801,200,28"/>
<mxCell id="p6r_tk0" value="sync" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1835,150,55"/>
<mxCell id="p6r_tv0" value="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1835,610,55"/>
<mxCell id="p6r_tk1" value="快路徑（Q22）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1890,150,71"/>
<mxCell id="p6r_tv1" value="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1890,610,71"/>
<mxCell id="p6r_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1961,150,55"/>
<mxCell id="p6r_tv2" value="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1961,610,55"/>
<mxCell id="p6r_tk3" value="stdout／stderr／指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2016,150,40"/>
<mxCell id="p6r_tv3" value="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2016,610,40"/>
<mxCell id="p6r_tk4" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2056,150,71"/>
<mxCell id="p6r_tv4" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2056,610,71"/>
<mxCell id="p6r_tk5" value="統一提示（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2127,150,55"/>
<mxCell id="p6r_tv5" value="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2127,610,55"/>
<mxCell id="p6r_tk6" value="薄殼／引擎 ref／hash" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2182,150,55"/>
<mxCell id="p6r_tv6" value="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2182,610,55"/>
<mxCell id="p6r_tk7" value="gen/ 三種檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2237,150,55"/>
<mxCell id="p6r_tv7" value="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2237,610,55"/>
<mxCell id="p6r_tk8" value="materialize／印記／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2292,150,55"/>
<mxCell id="p6r_tv8" value="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2292,610,55"/>
<mxCell id="p6r_tk9" value="image tag／digest／image ID／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1835,150,71"/>
<mxCell id="p6r_tv9" value="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1835,610,71"/>
<mxCell id="p6r_tk10" value="verify／sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1906,150,55"/>
<mxCell id="p6r_tv10" value="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1906,610,55"/>
<mxCell id="p6r_tk11" value="metadata／完成標記／落後" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1961,150,55"/>
<mxCell id="p6r_tv11" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1961,610,55"/>
<mxCell id="p6r_tk12" value="mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2016,150,55"/>
<mxCell id="p6r_tv12" value="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2016,610,55"/>
<mxCell id="p6r_tk13" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2071,150,40"/>
<mxCell id="p6r_tv13" value="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2071,610,40"/>
<mxCell id="p6r_tk14" value="覆寫兩種（v2.1 B／v2.2 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2111,150,55"/>
<mxCell id="p6r_tv14" value="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2111,610,55"/>
<mxCell id="p6r_tk15" value="GHCR／image／daemon／flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2166,150,40"/>
<mxCell id="p6r_tv15" value="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2166,610,40"/>
<mxCell id="p6r_tk16" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2206,150,55"/>
<mxCell id="p6r_tv16" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2206,610,55"/>
</diagram>
<diagram id="v1p6c" name="流程 v2：sync（2）apply">
<mxCell id="title" value="流程 v2：sync（2）第 2 段 apply（§6、v2.3 §3／§4、v2.5 §9）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="eB" value="sync 第 2 段（承「sync（1′）」頁：有待辦才跑）：啟動器對每個要拉的 image inspect → 無才 pull → create → cp → rm → 引擎 apply sync；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；版本變動那次逐檔 sha256 全驗（§3.6）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,1092"/>
<mxCell id="eB_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="1556,5,30,20"/>
<mxCell id="m00" value="來自「sync（1′）」頁：有待辦（resolve 的 stdout 清單，apply|yes）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="eB" geo="260,36,280,80"/>
<mxCell id="m0a" value="對每個要拉的 image：docker image inspect 本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="eB" geo="260,136,170,206"/>
<mxCell id="m0a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="406,126,30,20"/>
<mxCell id="m0p" value="無：docker pull" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eB" geo="440,362,100,48"/>
<mxCell id="m0p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="516,352,30,20"/>
<mxCell id="m0g" value="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（鎖定版；多架構 index）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="eB" geo="980,365,220,42"/>
<mxCell id="m0b" value="docker create &amp;lt;img&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eB" geo="260,430,280,40"/>
<mxCell id="m0b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="516,420,30,20"/>
<mxCell id="m0c" value="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eB" geo="260,490,280,48"/>
<mxCell id="m0c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="516,480,30,20"/>
<mxCell id="m0d" value="docker rm 該容器" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eB" geo="260,558,280,40"/>
<mxCell id="m0d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="516,548,30,20"/>
<mxCell id="m1" value="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply sync" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="eB" geo="260,618,280,48"/>
<mxCell id="m1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="516,608,30,20"/>
<mxCell id="m2a" value="apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,622,400,40"/>
<mxCell id="m2a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,612,30,20"/>
<mxCell id="m2b" value="重驗 resolve 的輸入指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,695,240,40"/>
<mxCell id="m2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="776,685,30,20"/>
<mxCell id="m2x" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="eB" geo="820,686,140,58"/>
<mxCell id="m2x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,676,30,20"/>
<mxCell id="m3" value="materialize／重裝（每個待辦工具）：/dist/&amp;lt;repo&amp;gt; 展開到暫存目錄" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,764,400,48"/>
<mxCell id="m3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,754,30,20"/>
<mxCell id="m3c" value="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,832,400,40"/>
<mxCell id="m3c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,822,30,20"/>
<mxCell id="m3f" value="cache/&amp;lt;repo&amp;gt;/（重寫，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="eB" geo="1220,832,360,40"/>
<mxCell id="m3b" value="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,892,400,48"/>
<mxCell id="m3b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,882,30,20"/>
<mxCell id="m3bf" value="gen/&amp;lt;repo&amp;gt;.stamp（重寫，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="eB" geo="1220,896,360,40"/>
<mxCell id="m3v" value="版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 全驗 cache/&amp;lt;repo&amp;gt;/ ＝ 印記（§3.6；不符 → 重裝 + warn）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,960,400,48"/>
<mxCell id="m3v_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,950,30,20"/>
<mxCell id="m7" value="0：接著跑原本的 recipe" style="fillColor=#d5e8d4;strokeColor=#000000" parent="eB" geo="20,1028,220,58"/>
<mxCell id="m5" value="重生 gen/tools.just（待辦有它時；每個 &amp;lt;ns&amp;gt;.just 一行 mod?）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="eB" geo="560,1033,400,48"/>
<mxCell id="m5_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="eB" geo="936,1023,30,20"/>
<mxCell id="m5f" value="gen/tools.just（不進 git；gen/.stamp 不動）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="eB" geo="1220,1037,360,40"/>
<mxCell id="me0" edge="1" source="m00" target="m0a"/>
<mxCell id="me0n" value="無" edge="1" source="m0a" target="m0p"/>
<mxCell id="me0g" value="拉 /dist" edge="1" source="m0g" target="m0p"/>
<mxCell id="me0y" value="有" edge="1" source="m0a" target="m0b"/>
<mxCell id="me0p" edge="1" source="m0p" target="m0b"/>
<mxCell id="me0c" edge="1" source="m0b" target="m0c"/>
<mxCell id="me0d" edge="1" source="m0c" target="m0d"/>
<mxCell id="me1" edge="1" source="m0d" target="m1"/>
<mxCell id="me2" edge="1" source="m1" target="m2a"/>
<mxCell id="me2b" edge="1" source="m2a" target="m2b"/>
<mxCell id="me2x" edge="1" source="m2b" target="m2x"/>
<mxCell id="me3" edge="1" source="m2b" target="m3"/>
<mxCell id="me3c" edge="1" source="m3" target="m3c"/>
<mxCell id="me4" value="寫" edge="1" source="m3c" target="m3f"/>
<mxCell id="me4b" edge="1" source="m3c" target="m3b"/>
<mxCell id="me4f" value="寫" edge="1" source="m3b" target="m3bf"/>
<mxCell id="me4v" edge="1" source="m3b" target="m3v"/>
<mxCell id="me5" edge="1" source="m3v" target="m5"/>
<mxCell id="me12" value="寫" edge="1" source="m5" target="m5f"/>
<mxCell id="me15" edge="1" source="m5" target="m7"/>
<mxCell id="p6c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1264,200,60"/>
<mxCell id="p6c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1264,140,64"/>
<mxCell id="p6c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1272,140,44"/>
<mxCell id="p6c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1266,190,56"/>
<mxCell id="p6c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1266,210,56"/>
<mxCell id="p6c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1274,88,40"/>
<mxCell id="p6c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1274,170,40"/>
<mxCell id="p6c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1264,300,60"/>
<mxCell id="p6c_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1332,200,36"/>
<mxCell id="p6c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1332,120,36"/>
<mxCell id="p6c_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1332,190,36"/>
<mxCell id="p6c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1332,170,36"/>
<mxCell id="p6c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1332,170,36"/>
<mxCell id="p6c_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1332,200,36"/>
<mxCell id="p6c_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1322,30,20"/>
<mxCell id="p6c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1370,200,28"/>
<mxCell id="p6c_tk0" value="sync" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1404,150,55"/>
<mxCell id="p6c_tv0" value="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1404,610,55"/>
<mxCell id="p6c_tk1" value="快路徑（Q22）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1459,150,71"/>
<mxCell id="p6c_tv1" value="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1459,610,71"/>
<mxCell id="p6c_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1530,150,55"/>
<mxCell id="p6c_tv2" value="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1530,610,55"/>
<mxCell id="p6c_tk3" value="stdout／stderr／指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1585,150,40"/>
<mxCell id="p6c_tv3" value="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1585,610,40"/>
<mxCell id="p6c_tk4" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1625,150,71"/>
<mxCell id="p6c_tv4" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1625,610,71"/>
<mxCell id="p6c_tk5" value="統一提示（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1696,150,55"/>
<mxCell id="p6c_tv5" value="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1696,610,55"/>
<mxCell id="p6c_tk6" value="薄殼／引擎 ref／hash" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1751,150,55"/>
<mxCell id="p6c_tv6" value="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1751,610,55"/>
<mxCell id="p6c_tk7" value="gen/ 三種檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1806,150,55"/>
<mxCell id="p6c_tv7" value="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1806,610,55"/>
<mxCell id="p6c_tk8" value="materialize／印記／index digest" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1861,150,55"/>
<mxCell id="p6c_tv8" value="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1861,610,55"/>
<mxCell id="p6c_tk9" value="image tag／digest／image ID／image inspect" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1404,150,71"/>
<mxCell id="p6c_tv9" value="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1404,610,71"/>
<mxCell id="p6c_tk10" value="verify／sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1475,150,55"/>
<mxCell id="p6c_tv10" value="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1475,610,55"/>
<mxCell id="p6c_tk11" value="metadata／完成標記／落後" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1530,150,55"/>
<mxCell id="p6c_tv11" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1530,610,55"/>
<mxCell id="p6c_tk12" value="mod?／recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1585,150,55"/>
<mxCell id="p6c_tv12" value="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1585,610,55"/>
<mxCell id="p6c_tk13" value="symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1640,150,40"/>
<mxCell id="p6c_tv13" value="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1640,610,40"/>
<mxCell id="p6c_tk14" value="覆寫兩種（v2.1 B／v2.2 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1680,150,55"/>
<mxCell id="p6c_tv14" value="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1680,610,55"/>
<mxCell id="p6c_tk15" value="GHCR／image／daemon／flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1735,150,40"/>
<mxCell id="p6c_tv15" value="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1735,610,40"/>
<mxCell id="p6c_tk16" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1775,150,55"/>
<mxCell id="p6c_tv16" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1775,610,55"/>
</diagram>
<diagram id="v1p7" name="流程 v2：upgrade ── A. Renovate 路徑">
<mxCell id="title" value="流程 v2：upgrade ── A. Renovate 路徑（§2／§7、v2.2 D、v2.3 §7、v2.5 §1／§7）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,97,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,97,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,97,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,97,280,28"/>
<mxCell id="uA" value="A. Renovate 路徑（下游自選，vendor_kit 不出 bot）：機器人只改 version.toml 一行；PR 的 CI 以新版跑完整流程；baseline 落後 → PR 紅（需要人補合併）；補合併在 PR 分支上完成、CI 綠後才 merge" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,920"/>
<mxCell id="uA_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uA" geo="1556,5,30,20"/>
<mxCell id="a0" value="Renovate 定期查 GHCR" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uA" geo="270,36,160,58"/>
<mxCell id="a1" value="&amp;lt;repo&amp;gt;-dist&lt;br&gt;出新 tag@digest" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="uA" geo="1100,44,180,42"/>
<mxCell id="a2" value="開 PR（獨立分支）：只改 version.toml 該工具一行（tag@digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="270,114,160,57"/>
<mxCell id="a3" value="version.toml（PR 分支）&lt;br&gt;&amp;lt;repo&amp;gt; 行 = 新 tag@digest" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uA" geo="1300,122,280,42"/>
<mxCell id="a4a" value="PR 的 CI 呼叫 .vendor_kit/ci/check.sh（以新版跑完整流程）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,191,220,57"/>
<mxCell id="a4r" value="一行改動本身不可能出錯，不構成通過依據&lt;br&gt;→ PR 的 CI 必須以新版跑完整流程" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="uA" geo="720,198,360,42"/>
<mxCell id="a4b" value="check.sh ①：sync（CI 為真 → frozen；export CI=1）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,268,220,42"/>
<mxCell id="a5" value="1 → PR 紅：需要人補合併（印「本機 upgrade &amp;lt;repo&amp;gt; -y 後 push」）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uA" geo="20,330,220,102"/>
<mxCell id="a5_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uA" geo="216,320,30,20"/>
<mxCell id="a4q" value="baseline 落後？（最後合併版本 ≠ version.toml）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uA" geo="720,340,360,81"/>
<mxCell id="a4q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uA" geo="1056,330,30,20"/>
<mxCell id="a4c" value="否：check.sh ②：verify" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,452,220,40"/>
<mxCell id="a4d" value="check.sh ③：upgrade --dry-run" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,512,220,42"/>
<mxCell id="a4e1" value="check.sh ④：工具測試" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,582,220,40"/>
<mxCell id="a6a" value="PR 作者本機：切到 PR 分支" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="20,582,220,40"/>
<mxCell id="a6a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uA" geo="216,572,30,20"/>
<mxCell id="a9" value="Renovate 預設不動有人推過的分支；PR body 加警告：勿勾 rebase（會蓋掉人補的合併 commit）。vendor_kit 無 bot。" style="fillColor=#ffffff;strokeColor=#999999" parent="uA" geo="1300,574,280,57"/>
<mxCell id="a4e2" value="check.sh ⑤：專案測試" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="470,662,220,40"/>
<mxCell id="a6b" value="upgrade &amp;lt;repo&amp;gt; -y（走「B. 手動路徑（1）」頁，固定補到 PR 鎖定版）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="20,651,220,63"/>
<mxCell id="a6b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uA" geo="216,641,30,20"/>
<mxCell id="a6c" value="commit（合併結果）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="20,734,220,40"/>
<mxCell id="a6d" value="push 到 PR 分支" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="20,795,220,40"/>
<mxCell id="a7" value="PR 分支 CI 再跑完整流程（同上）→ 綠" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uA" geo="460,794,150,42"/>
<mxCell id="a8" value="merge PR（CI 綠後才 merge）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uA" geo="260,856,180,58"/>
<mxCell id="ae1" value="查" edge="1" source="a0" target="a1"/>
<mxCell id="ae2" value="有新版" edge="1" source="a1" target="a2"/>
<mxCell id="ae3" value="改一行" edge="1" source="a2" target="a3"/>
<mxCell id="ae4" edge="1" source="a2" target="a4a"/>
<mxCell id="ae4b" edge="1" source="a4a" target="a4b"/>
<mxCell id="ae4q" edge="1" source="a4b" target="a4q"/>
<mxCell id="ae5" value="是" edge="1" source="a4q" target="a5"/>
<mxCell id="ae5n" value="否" edge="1" source="a4q" target="a4c"/>
<mxCell id="ae5c" edge="1" source="a4c" target="a4d"/>
<mxCell id="ae5d" edge="1" source="a4d" target="a4e1"/>
<mxCell id="ae5e" edge="1" source="a4e1" target="a4e2"/>
<mxCell id="ae6" edge="1" source="a5" target="a6a"/>
<mxCell id="ae6b" edge="1" source="a6a" target="a6b"/>
<mxCell id="ae6c" edge="1" source="a6b" target="a6c"/>
<mxCell id="ae6d" edge="1" source="a6c" target="a6d"/>
<mxCell id="ae7" edge="1" source="a6d" target="a7"/>
<mxCell id="ae8" value="綠" edge="1" source="a4e2" target="a8"/>
<mxCell id="ae9" value="綠" edge="1" source="a7" target="a8"/>
<mxCell id="p7_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1077,200,60"/>
<mxCell id="p7_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1077,140,64"/>
<mxCell id="p7_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1085,140,44"/>
<mxCell id="p7_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1079,190,56"/>
<mxCell id="p7_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1079,210,56"/>
<mxCell id="p7_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1087,88,40"/>
<mxCell id="p7_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1087,170,40"/>
<mxCell id="p7_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1077,300,60"/>
<mxCell id="p7_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1145,120,36"/>
<mxCell id="p7_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1145,150,36"/>
<mxCell id="p7_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1145,190,36"/>
<mxCell id="p7_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1145,170,36"/>
<mxCell id="p7_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1145,170,36"/>
<mxCell id="p7_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1145,200,36"/>
<mxCell id="p7_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1135,30,20"/>
<mxCell id="p7_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1183,200,28"/>
<mxCell id="p7_tk0" value="Renovate／regex manager" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1217,150,40"/>
<mxCell id="p7_tv0" value="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1217,610,40"/>
<mxCell id="p7_tk1" value="PR／commit／push／rebase／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1257,150,40"/>
<mxCell id="p7_tv1" value="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1257,610,40"/>
<mxCell id="p7_tk2" value="check.sh／CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1297,150,55"/>
<mxCell id="p7_tv2" value="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1297,610,55"/>
<mxCell id="p7_tk3" value="baseline 落後／待合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1352,150,40"/>
<mxCell id="p7_tv3" value="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1352,610,40"/>
<mxCell id="p7_tk4" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1392,150,55"/>
<mxCell id="p7_tv4" value="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1392,610,55"/>
<mxCell id="p7_tk5" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1447,150,40"/>
<mxCell id="p7_tv5" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1447,610,40"/>
<mxCell id="p7_tk6" value="dev 覆寫／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1487,150,40"/>
<mxCell id="p7_tv6" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1487,610,40"/>
<mxCell id="p7_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1527,150,40"/>
<mxCell id="p7_tv7" value="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1527,610,40"/>
<mxCell id="p7_tk8" value="B／D／N、逐檔判斷後詢問" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1567,150,86"/>
<mxCell id="p7_tv8" value="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1567,610,86"/>
<mxCell id="p7_tk9" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1217,150,71"/>
<mxCell id="p7_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1217,610,71"/>
<mxCell id="p7_tk10" value="gen／mod?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1288,150,40"/>
<mxCell id="p7_tv10" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1288,610,40"/>
<mxCell id="p7_tk11" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1328,150,55"/>
<mxCell id="p7_tv11" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1328,610,55"/>
<mxCell id="p7_tk12" value="CRLF／append 行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1383,150,40"/>
<mxCell id="p7_tv12" value="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1383,610,40"/>
<mxCell id="p7_tk13" value="GHCR／image／tag@digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1423,150,40"/>
<mxCell id="p7_tv13" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1423,610,40"/>
<mxCell id="p7_tk14" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1463,150,55"/>
<mxCell id="p7_tv14" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1463,610,55"/>
</diagram>
<diagram id="v1p7c" name="流程 v2：upgrade ── B. 手動路徑（1）resolve → docker">
<mxCell id="title" value="流程 v2：upgrade ── B. 手動路徑（1）前置（§2、v2.2 C／D、v2.5 §2／§3／§6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,97,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,97,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,97,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,97,280,28"/>
<mxCell id="uB" value="B. 手動路徑：just vendor_kit upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]（不帶 repo = 全部含 vendor_kit 自身，先完整預檢再動；@&amp;lt;tag&amp;gt; 限單一 repo）= resolve（不寫）→ 啟動器 docker；apply 前置見「B（1′）」頁、寫入段見「B（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1511"/>
<mxCell id="uB_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1556,5,30,20"/>
<mxCell id="b0" value="just vendor_kit upgrade &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y、--dry-run）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uB" geo="20,36,220,102"/>
<mxCell id="b1" value="docker run &amp;lt;引擎&amp;gt; resolve upgrade &amp;lt;repo&amp;gt;&lt;br&gt;（啟動器不鎖）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="460,56,240,63"/>
<mxCell id="b1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="676,46,30,20"/>
<mxCell id="b1x" value="是 → 1：請先 undev &amp;lt;repo&amp;gt;" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB" geo="20,170,220,58"/>
<mxCell id="b1x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="216,160,30,20"/>
<mxCell id="b1q" value="&amp;lt;repo&amp;gt; 在 dev 覆寫中？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="720,158,280,81"/>
<mxCell id="b1q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="976,148,30,20"/>
<mxCell id="b2c" value="是 → 2：先解完衝突再重跑" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB" geo="20,266,220,58"/>
<mxCell id="b2c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="216,256,30,20"/>
<mxCell id="b2" value="(0) 衝突檔仍含我們的標籤？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="720,270,360,50"/>
<mxCell id="b2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1056,260,30,20"/>
<mxCell id="b2n" value="標籤 = 我們自己產的 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建日誌之後（v2.5 §3）" style="fillColor=#ffffff;strokeColor=#999999" parent="uB" geo="1300,259,280,73"/>
<mxCell id="b5" value="否 → 1：無 baseline，請先 add &amp;lt;repo&amp;gt;" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB" geo="20,352,220,58"/>
<mxCell id="b4" value="有 baseline/&amp;lt;repo&amp;gt;/？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="730,356,340,50"/>
<mxCell id="b6" value="(1) 有待合併？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="720,430,170,81"/>
<mxCell id="b6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="866,420,30,20"/>
<mxCell id="b6y" value="是：目標版 = B（version.toml 那版），補到就停，不查最新" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="910,531,170,63"/>
<mxCell id="b6y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1056,521,30,20"/>
<mxCell id="b7a" value="否 → @&amp;lt;tag&amp;gt; 指定？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="720,614,170,112"/>
<mxCell id="b7a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="866,604,30,20"/>
<mxCell id="b7t" value="是：目標版 = @&amp;lt;tag&amp;gt;（比現版舊 → warn 仍執行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="910,646,170,48"/>
<mxCell id="b7t_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1056,636,30,20"/>
<mxCell id="b7b" value="否 → CI 為真（frozen）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="720,746,170,112"/>
<mxCell id="b7b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="866,736,30,20"/>
<mxCell id="b7z" value="是：不查最新；目標版 = 鎖定版（無事可做）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="910,778,170,48"/>
<mxCell id="b7z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1056,768,30,20"/>
<mxCell id="b7c" value="否：(2) 查 registry 最新正式版 = 目標版" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="720,878,170,48"/>
<mxCell id="b7c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="866,868,30,20"/>
<mxCell id="b7s" value="resolve 完 → stdout：目標 tag@digest ＋ 輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB" geo="720,946,360,63"/>
<mxCell id="b7s_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="1056,936,30,20"/>
<mxCell id="b8a" value="docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB" geo="460,1029,170,143"/>
<mxCell id="b8a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="606,1019,30,20"/>
<mxCell id="b8p" value="無：docker pull" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="630,1192,70,63"/>
<mxCell id="b8p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="676,1182,30,20"/>
<mxCell id="b8g" value="&amp;lt;repo&amp;gt;-dist&lt;br&gt;目標 tag@digest" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="uB" geo="1100,1202,180,42"/>
<mxCell id="b8b" value="docker create &amp;lt;img&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="460,1275,240,40"/>
<mxCell id="b8b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="676,1265,30,20"/>
<mxCell id="b8c" value="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="460,1335,240,48"/>
<mxCell id="b8c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="676,1325,30,20"/>
<mxCell id="b8d" value="docker rm 該容器" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB" geo="460,1403,240,40"/>
<mxCell id="b8d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB" geo="676,1393,30,20"/>
<mxCell id="b8z" value="↓ 續「B（1′）」頁：docker run 引擎 apply upgrade → 前置檢查" style="fillColor=none;strokeColor=none" parent="uB" geo="460,1463,240,42"/>
<mxCell id="be1" edge="1" source="b0" target="b1"/>
<mxCell id="be1q" edge="1" source="b1" target="b1q"/>
<mxCell id="be1x" value="是" edge="1" source="b1q" target="b1x"/>
<mxCell id="be2" value="否" edge="1" source="b1q" target="b2"/>
<mxCell id="be3" value="是" edge="1" source="b2" target="b2c"/>
<mxCell id="be4" value="否" edge="1" source="b2" target="b4"/>
<mxCell id="be5" value="否" edge="1" source="b4" target="b5"/>
<mxCell id="be6" value="是" edge="1" source="b4" target="b6"/>
<mxCell id="be7" value="是" edge="1" source="b6" target="b6y"/>
<mxCell id="be8" value="否" edge="1" source="b6" target="b7a"/>
<mxCell id="be8t" value="是" edge="1" source="b7a" target="b7t"/>
<mxCell id="be8b" value="否" edge="1" source="b7a" target="b7b"/>
<mxCell id="be8z" value="是" edge="1" source="b7b" target="b7z"/>
<mxCell id="be8c" value="否" edge="1" source="b7b" target="b7c"/>
<mxCell id="be9" edge="1" source="b6y" target="b7s"/>
<mxCell id="be9t" edge="1" source="b7t" target="b7s"/>
<mxCell id="be9z" edge="1" source="b7z" target="b7s"/>
<mxCell id="be10" edge="1" source="b7c" target="b7s"/>
<mxCell id="be11" edge="1" source="b7s" target="b8a"/>
<mxCell id="be11n" value="無" edge="1" source="b8a" target="b8p"/>
<mxCell id="be12" value="拉 /dist" edge="1" source="b8g" target="b8p"/>
<mxCell id="be11y" value="有" edge="1" source="b8a" target="b8b"/>
<mxCell id="be11p" edge="1" source="b8p" target="b8b"/>
<mxCell id="be12c" edge="1" source="b8b" target="b8c"/>
<mxCell id="be12d" edge="1" source="b8c" target="b8d"/>
<mxCell id="be13" edge="1" source="b8d" target="b8z"/>
<mxCell id="p7c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1668,200,60"/>
<mxCell id="p7c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1668,140,64"/>
<mxCell id="p7c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1676,140,44"/>
<mxCell id="p7c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1670,190,56"/>
<mxCell id="p7c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1670,210,56"/>
<mxCell id="p7c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1678,88,40"/>
<mxCell id="p7c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1678,170,40"/>
<mxCell id="p7c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1668,300,60"/>
<mxCell id="p7c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1736,120,36"/>
<mxCell id="p7c_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1736,190,36"/>
<mxCell id="p7c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1736,170,36"/>
<mxCell id="p7c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1736,170,36"/>
<mxCell id="p7c_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1736,200,36"/>
<mxCell id="p7c_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1726,30,20"/>
<mxCell id="p7c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1774,200,28"/>
<mxCell id="p7c_tk0" value="Renovate／regex manager" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1808,150,40"/>
<mxCell id="p7c_tv0" value="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1808,610,40"/>
<mxCell id="p7c_tk1" value="PR／commit／push／rebase／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1848,150,40"/>
<mxCell id="p7c_tv1" value="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1848,610,40"/>
<mxCell id="p7c_tk2" value="check.sh／CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1888,150,55"/>
<mxCell id="p7c_tv2" value="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1888,610,55"/>
<mxCell id="p7c_tk3" value="baseline 落後／待合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1943,150,40"/>
<mxCell id="p7c_tv3" value="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1943,610,40"/>
<mxCell id="p7c_tk4" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1983,150,55"/>
<mxCell id="p7c_tv4" value="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1983,610,55"/>
<mxCell id="p7c_tk5" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2038,150,40"/>
<mxCell id="p7c_tv5" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2038,610,40"/>
<mxCell id="p7c_tk6" value="dev 覆寫／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2078,150,40"/>
<mxCell id="p7c_tv6" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2078,610,40"/>
<mxCell id="p7c_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2118,150,40"/>
<mxCell id="p7c_tv7" value="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2118,610,40"/>
<mxCell id="p7c_tk8" value="B／D／N、逐檔判斷後詢問" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2158,150,86"/>
<mxCell id="p7c_tv8" value="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2158,610,86"/>
<mxCell id="p7c_tk9" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1808,150,71"/>
<mxCell id="p7c_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1808,610,71"/>
<mxCell id="p7c_tk10" value="gen／mod?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1879,150,40"/>
<mxCell id="p7c_tv10" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1879,610,40"/>
<mxCell id="p7c_tk11" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1919,150,55"/>
<mxCell id="p7c_tv11" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1919,610,55"/>
<mxCell id="p7c_tk12" value="CRLF／append 行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1974,150,40"/>
<mxCell id="p7c_tv12" value="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1974,610,40"/>
<mxCell id="p7c_tk13" value="GHCR／image／tag@digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2014,150,40"/>
<mxCell id="p7c_tv13" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2014,610,40"/>
<mxCell id="p7c_tk14" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2054,150,55"/>
<mxCell id="p7c_tv14" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2054,610,55"/>
</diagram>
<diagram id="v1p7ccc" name="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置">
<mxCell id="title" value="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置（§2、v2.2 C／D、v2.5 §2／§3／§5、v2.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,97,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,97,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,97,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,97,280,28"/>
<mxCell id="uB1" value="B（1′）apply 前置（承「B（1）」頁：目標版 image 已展開到暫存）：拿鎖 → 重驗指紋 → dest／命名空間檢查 → 逐檔判斷 → frozen → dry-run 分支；寫入段見「B（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,901"/>
<mxCell id="uB1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1556,5,30,20"/>
<mxCell id="b8e" value="來自「B（1）」頁：目標版 /dist 已在主機暫存" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="uB1" geo="460,36,240,58"/>
<mxCell id="b9" value="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply upgrade &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB1" geo="460,114,240,63"/>
<mxCell id="b9_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="676,104,30,20"/>
<mxCell id="b10a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB1" geo="720,126,360,40"/>
<mxCell id="b10a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1056,116,30,20"/>
<mxCell id="b10b" value="重驗 resolve 的輸入指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB1" geo="720,206,220,40"/>
<mxCell id="b10b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="916,196,30,20"/>
<mxCell id="b10x" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB1" geo="950,197,130,58"/>
<mxCell id="b10x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1056,187,30,20"/>
<mxCell id="b10dx" value="否 → 1：dest 不合法" style="fillColor=#f8cecc;strokeColor=#000000" parent="uB1" geo="20,311,220,40"/>
<mxCell id="b10dx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="216,301,30,20"/>
<mxCell id="b10d" value="新版 init.toml 的 dest 全部合法？（任何寫入前；規則同「add（1）」頁）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB1" geo="720,275,340,112"/>
<mxCell id="b10d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1036,265,30,20"/>
<mxCell id="b10nx" value="是 → 1：命名空間撞名" style="fillColor=#f8cecc;strokeColor=#000000" parent="uB1" geo="20,474,220,40"/>
<mxCell id="b10nx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="216,464,30,20"/>
<mxCell id="b10n" value="是 → 新版 just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB1" geo="720,407,340,174"/>
<mxCell id="b10n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1036,397,30,20"/>
<mxCell id="b10c" value="否 → 逐檔判斷（B baseline／D 現況／N = 暫存 /dist/&amp;lt;repo&amp;gt;，見「逐檔判斷」頁）→ 詢問清單" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB1" geo="720,601,360,48"/>
<mxCell id="b10c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1056,591,30,20"/>
<mxCell id="b12x" value="是 → 1：印需改清單（frozen；請在本機 upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB1" geo="20,669,220,102"/>
<mxCell id="b12x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="216,659,30,20"/>
<mxCell id="b12" value="CI 為真（frozen）且需改 tracked 檔？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB1" geo="720,680,340,81"/>
<mxCell id="b12_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="1036,670,30,20"/>
<mxCell id="b11y" value="是 → 0：唯讀預覽（印會問哪些檔）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uB1" geo="20,791,220,58"/>
<mxCell id="b11y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB1" geo="216,781,30,20"/>
<mxCell id="b11" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB1" geo="770,795,240,50"/>
<mxCell id="b11z" value="否 ↓ 續「B（2）」頁：apply 寫入段" style="fillColor=none;strokeColor=none" parent="uB1" geo="720,869,300,26"/>
<mxCell id="be13e" edge="1" source="b8e" target="b9"/>
<mxCell id="be14" edge="1" source="b9" target="b10a"/>
<mxCell id="be15" edge="1" source="b10a" target="b10b"/>
<mxCell id="be15x" edge="1" source="b10b" target="b10x"/>
<mxCell id="be15b" edge="1" source="b10b" target="b10d"/>
<mxCell id="be15d" value="否" edge="1" source="b10d" target="b10dx"/>
<mxCell id="be15n" value="是" edge="1" source="b10d" target="b10n"/>
<mxCell id="be15nx" value="是" edge="1" source="b10n" target="b10nx"/>
<mxCell id="be15c" value="否" edge="1" source="b10n" target="b10c"/>
<mxCell id="be15e" edge="1" source="b10c" target="b12"/>
<mxCell id="be16" value="是" edge="1" source="b12" target="b12x"/>
<mxCell id="be17" value="否" edge="1" source="b12" target="b11"/>
<mxCell id="be18" value="是" edge="1" source="b11" target="b11y"/>
<mxCell id="be19" edge="1" source="b11" target="b11z"/>
<mxCell id="p7cp_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1058,200,60"/>
<mxCell id="p7cp_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1058,140,64"/>
<mxCell id="p7cp_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1066,140,44"/>
<mxCell id="p7cp_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1060,190,56"/>
<mxCell id="p7cp_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1060,210,56"/>
<mxCell id="p7cp_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1068,88,40"/>
<mxCell id="p7cp_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1068,170,40"/>
<mxCell id="p7cp_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1058,300,60"/>
<mxCell id="p7cp_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1126,200,36"/>
<mxCell id="p7cp_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1126,120,36"/>
<mxCell id="p7cp_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1126,190,36"/>
<mxCell id="p7cp_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1126,170,36"/>
<mxCell id="p7cp_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1126,170,36"/>
<mxCell id="p7cp_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1126,200,36"/>
<mxCell id="p7cp_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1116,30,20"/>
<mxCell id="p7cp_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1164,200,28"/>
<mxCell id="p7cp_tk0" value="Renovate／regex manager" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1198,150,40"/>
<mxCell id="p7cp_tv0" value="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1198,610,40"/>
<mxCell id="p7cp_tk1" value="PR／commit／push／rebase／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1238,150,40"/>
<mxCell id="p7cp_tv1" value="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1238,610,40"/>
<mxCell id="p7cp_tk2" value="check.sh／CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1278,150,55"/>
<mxCell id="p7cp_tv2" value="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1278,610,55"/>
<mxCell id="p7cp_tk3" value="baseline 落後／待合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1333,150,40"/>
<mxCell id="p7cp_tv3" value="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1333,610,40"/>
<mxCell id="p7cp_tk4" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1373,150,55"/>
<mxCell id="p7cp_tv4" value="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1373,610,55"/>
<mxCell id="p7cp_tk5" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1428,150,40"/>
<mxCell id="p7cp_tv5" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1428,610,40"/>
<mxCell id="p7cp_tk6" value="dev 覆寫／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1468,150,40"/>
<mxCell id="p7cp_tv6" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1468,610,40"/>
<mxCell id="p7cp_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1508,150,40"/>
<mxCell id="p7cp_tv7" value="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1508,610,40"/>
<mxCell id="p7cp_tk8" value="B／D／N、逐檔判斷後詢問" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1548,150,86"/>
<mxCell id="p7cp_tv8" value="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1548,610,86"/>
<mxCell id="p7cp_tk9" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1198,150,71"/>
<mxCell id="p7cp_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1198,610,71"/>
<mxCell id="p7cp_tk10" value="gen／mod?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1269,150,40"/>
<mxCell id="p7cp_tv10" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1269,610,40"/>
<mxCell id="p7cp_tk11" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1309,150,55"/>
<mxCell id="p7cp_tv11" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1309,610,55"/>
<mxCell id="p7cp_tk12" value="CRLF／append 行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1364,150,40"/>
<mxCell id="p7cp_tv12" value="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1364,610,40"/>
<mxCell id="p7cp_tk13" value="GHCR／image／tag@digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1404,150,40"/>
<mxCell id="p7cp_tv13" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1404,610,40"/>
<mxCell id="p7cp_tk14" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1444,150,55"/>
<mxCell id="p7cp_tv14" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1444,610,55"/>
</diagram>
<diagram id="v1p7cc" name="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併">
<mxCell id="title" value="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併（§5、v2.2 D、v2.5 §2～§4、v2.6 §8／Q14）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,97,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,97,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,97,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,97,280,28"/>
<mxCell id="uB2" value="B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔詢問（四種情況各一問）→ 暫存合併 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換（§4.3）；收尾見「B（2′）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1603"/>
<mxCell id="uB2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1556,5,30,20"/>
<mxCell id="b10z" value="來自「B（1′）」頁：apply 檢查通過（非 dry-run）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="uB2" geo="750,36,300,58"/>
<mxCell id="b10e" value="建進度日誌（metadata state=in-progress；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="720,114,360,48"/>
<mxCell id="b10e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,104,30,20"/>
<mxCell id="b10ef" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（state=in-progress）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB2" geo="1300,117,280,42"/>
<mxCell id="b10f" value="(0) 判定已解 → 清除 metadata 的衝突狀態（有的話）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="720,182,360,40"/>
<mxCell id="b10f_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,172,30,20"/>
<mxCell id="b10ff" value=".vendor_kit.toml（衝突中檔案清單清空）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB2" geo="1300,182,280,40"/>
<mxCell id="b13a" value="materialize 目標版：/dist/&amp;lt;repo&amp;gt; → 暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="720,242,360,48"/>
<mxCell id="b13a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,232,30,20"/>
<mxCell id="b13f" value="cache/&amp;lt;repo&amp;gt;/（目標版，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB2" geo="1300,246,280,40"/>
<mxCell id="b13b" value="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="720,310,360,48"/>
<mxCell id="b13b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,300,30,20"/>
<mxCell id="b13bf" value="gen/&amp;lt;repo&amp;gt;.stamp（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB2" geo="1300,314,280,40"/>
<mxCell id="bl" value="↓ 逐檔（每檔恰一種情況，依「逐檔判斷」頁；不是該情況就看下一格；-y 免問）" style="fillColor=none;strokeColor=none" parent="uB2" geo="720,378,360,42"/>
<mxCell id="b14q1" value="文字檔：你沒改、新版改了 → 問「X 換成新版？」" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="720,440,240,112"/>
<mxCell id="b14q1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="936,430,30,20"/>
<mxCell id="b14a" value="是：換新版（在暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="990,472,90,48"/>
<mxCell id="b14a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,462,30,20"/>
<mxCell id="b14q1b" value="二進位／symlink：你沒改、新版改了 → 問「X 是二進位檔，要換成新版嗎？」" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="720,572,240,174"/>
<mxCell id="b14q1b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="936,562,30,20"/>
<mxCell id="b14ab" value="是：換新版（在暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="990,635,90,48"/>
<mxCell id="b14ab_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,625,30,20"/>
<mxCell id="b14q2" value="兩邊都改 → 問「你和新版都改了 X，要三方合併嗎？」" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="720,766,240,143"/>
<mxCell id="b14q2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="936,756,30,20"/>
<mxCell id="b14b" value="是：git merge-file --diff3（在暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="990,798,90,79"/>
<mxCell id="b14b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,788,30,20"/>
<mxCell id="b14q3" value="append 行找到上次插入的行 → 問「要替換嗎？」" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="720,929,240,112"/>
<mxCell id="b14q3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="936,919,30,20"/>
<mxCell id="b14c" value="是：append 行替換（在暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="990,954,90,63"/>
<mxCell id="b14c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,944,30,20"/>
<mxCell id="b14q4" value="新版新增（B 無）→ 問「要建 X 嗎」" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="720,1076,240,112"/>
<mxCell id="b14q4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="936,1066,30,20"/>
<mxCell id="b14d" value="是：建新檔（已有同名 → 不納管）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="990,1100,90,63"/>
<mxCell id="b14d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,1090,30,20"/>
<mxCell id="b14r" value="Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined 從未建立；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑（.github/workflows/、.gitlab-ci.yml）時訊息醒目" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="uB2" geo="1300,1061,280,141"/>
<mxCell id="b14r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1556,1051,30,20"/>
<mxCell id="b14n" value="否：不動該檔；已納管檔 state 不變只記 declined_hash，新檔被拒 → state=declined（新版再更新時再問）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="620,1222,280,63"/>
<mxCell id="b14n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="876,1212,30,20"/>
<mxCell id="b14m" value="暫存合併完成（每檔已定：換新版／合併／替換／建新／不動；都還在暫存）→ TOML／just 等可解析格式先重新解析" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="720,1305,360,48"/>
<mxCell id="b14m_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,1295,30,20"/>
<mxCell id="b14pc" value="是：留原檔、記 conflicts（baseline 不推）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uB2" geo="720,1373,90,94"/>
<mxCell id="b14pc_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="786,1363,30,20"/>
<mxCell id="b14pq" value="可解析格式：重新解析失敗？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB2" geo="840,1380,240,81"/>
<mxCell id="b14pq_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,1370,30,20"/>
<mxCell id="b14w" value="否：通過的檔逐檔原子替換（暫存 → 正式位置）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB2" geo="840,1487,240,48"/>
<mxCell id="b14w_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB2" geo="1056,1477,30,20"/>
<mxCell id="b14f" value="初始檔（合併後；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB2" geo="1300,1490,280,42"/>
<mxCell id="b14z" value="↓ 續「B（2′）」頁：baseline（解析失敗的檔不推）→ metadata → tools.just → version.toml → 刪日誌" style="fillColor=none;strokeColor=none" parent="uB2" geo="720,1555,360,42"/>
<mxCell id="be20" edge="1" source="b10z" target="b10e"/>
<mxCell id="be20f" value="寫" edge="1" source="b10e" target="b10ef"/>
<mxCell id="be20b" edge="1" source="b10e" target="b10f"/>
<mxCell id="be20ff" value="寫" edge="1" source="b10f" target="b10ff"/>
<mxCell id="be21" edge="1" source="b10f" target="b13a"/>
<mxCell id="be21f" value="寫" edge="1" source="b13a" target="b13f"/>
<mxCell id="be21b" edge="1" source="b13a" target="b13b"/>
<mxCell id="be21bf" value="寫" edge="1" source="b13b" target="b13bf"/>
<mxCell id="be22" edge="1" source="b13b" target="bl"/>
<mxCell id="be22a" edge="1" source="bl" target="b14q1"/>
<mxCell id="be22y1" value="是" edge="1" source="b14q1" target="b14a"/>
<mxCell id="be22n1" edge="1" source="b14q1" target="b14q1b"/>
<mxCell id="be22x1" value="否" edge="1" source="b14q1" target="b14n"/>
<mxCell id="be22y1b" value="是" edge="1" source="b14q1b" target="b14ab"/>
<mxCell id="be22n1b" edge="1" source="b14q1b" target="b14q2"/>
<mxCell id="be22x1b" value="否" edge="1" source="b14q1b" target="b14n"/>
<mxCell id="be22y2" value="是" edge="1" source="b14q2" target="b14b"/>
<mxCell id="be22n2" edge="1" source="b14q2" target="b14q3"/>
<mxCell id="be22x2" value="否" edge="1" source="b14q2" target="b14n"/>
<mxCell id="be22y3" value="是" edge="1" source="b14q3" target="b14c"/>
<mxCell id="be22n3" edge="1" source="b14q3" target="b14q4"/>
<mxCell id="be22x3" value="否" edge="1" source="b14q3" target="b14n"/>
<mxCell id="be22y4" value="是" edge="1" source="b14q4" target="b14d"/>
<mxCell id="be22x4" value="否" edge="1" source="b14q4" target="b14n"/>
<mxCell id="be23a" edge="1" source="b14a" target="b14m"/>
<mxCell id="be23ab" edge="1" source="b14ab" target="b14m"/>
<mxCell id="be23b" edge="1" source="b14b" target="b14m"/>
<mxCell id="be23c" edge="1" source="b14c" target="b14m"/>
<mxCell id="be23d" edge="1" source="b14d" target="b14m"/>
<mxCell id="be23n" edge="1" source="b14n" target="b14m"/>
<mxCell id="be23m" edge="1" source="b14m" target="b14pq"/>
<mxCell id="be23pc" value="是" edge="1" source="b14pq" target="b14pc"/>
<mxCell id="be23pw" value="否" edge="1" source="b14pq" target="b14w"/>
<mxCell id="be22f" value="寫" edge="1" source="b14w" target="b14f"/>
<mxCell id="be23z" edge="1" source="b14w" target="b14z"/>
<mxCell id="be23pz" edge="1" source="b14pc" target="b14z"/>
<mxCell id="p7cc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1760,200,60"/>
<mxCell id="p7cc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1760,140,64"/>
<mxCell id="p7cc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1768,140,44"/>
<mxCell id="p7cc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1762,190,56"/>
<mxCell id="p7cc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1762,210,56"/>
<mxCell id="p7cc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1770,88,40"/>
<mxCell id="p7cc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1770,170,40"/>
<mxCell id="p7cc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1760,300,60"/>
<mxCell id="p7cc_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1828,200,36"/>
<mxCell id="p7cc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1828,120,36"/>
<mxCell id="p7cc_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,1828,150,36"/>
<mxCell id="p7cc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="570,1828,190,36"/>
<mxCell id="p7cc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="780,1828,170,36"/>
<mxCell id="p7cc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,1828,170,36"/>
<mxCell id="p7cc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1160,1828,200,36"/>
<mxCell id="p7cc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1336,1818,30,20"/>
<mxCell id="p7cc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1866,200,28"/>
<mxCell id="p7cc_tk0" value="Renovate／regex manager" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1900,150,40"/>
<mxCell id="p7cc_tv0" value="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1900,610,40"/>
<mxCell id="p7cc_tk1" value="PR／commit／push／rebase／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1940,150,40"/>
<mxCell id="p7cc_tv1" value="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1940,610,40"/>
<mxCell id="p7cc_tk2" value="check.sh／CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1980,150,55"/>
<mxCell id="p7cc_tv2" value="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1980,610,55"/>
<mxCell id="p7cc_tk3" value="baseline 落後／待合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2035,150,40"/>
<mxCell id="p7cc_tv3" value="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2035,610,40"/>
<mxCell id="p7cc_tk4" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2075,150,55"/>
<mxCell id="p7cc_tv4" value="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2075,610,55"/>
<mxCell id="p7cc_tk5" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2130,150,40"/>
<mxCell id="p7cc_tv5" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2130,610,40"/>
<mxCell id="p7cc_tk6" value="dev 覆寫／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2170,150,40"/>
<mxCell id="p7cc_tv6" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2170,610,40"/>
<mxCell id="p7cc_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2210,150,40"/>
<mxCell id="p7cc_tv7" value="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2210,610,40"/>
<mxCell id="p7cc_tk8" value="B／D／N、逐檔判斷後詢問" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2250,150,86"/>
<mxCell id="p7cc_tv8" value="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2250,610,86"/>
<mxCell id="p7cc_tk9" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1900,150,71"/>
<mxCell id="p7cc_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1900,610,71"/>
<mxCell id="p7cc_tk10" value="gen／mod?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1971,150,40"/>
<mxCell id="p7cc_tv10" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1971,610,40"/>
<mxCell id="p7cc_tk11" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2011,150,55"/>
<mxCell id="p7cc_tv11" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2011,610,55"/>
<mxCell id="p7cc_tk12" value="CRLF／append 行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2066,150,40"/>
<mxCell id="p7cc_tv12" value="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2066,610,40"/>
<mxCell id="p7cc_tk13" value="GHCR／image／tag@digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2106,150,40"/>
<mxCell id="p7cc_tv13" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2106,610,40"/>
<mxCell id="p7cc_tk14" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2146,150,55"/>
<mxCell id="p7cc_tv14" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2146,610,55"/>
</diagram>
<diagram id="v1p7cccc" name="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入">
<mxCell id="title" value="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入（§5、v2.2 D、v2.5 §3／§4、v2.6 Q27）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,97,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,97,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,97,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,97,280,28"/>
<mxCell id="uB3" value="B（2′）apply 寫入段後半（承「B（2）」頁：通過解析的檔已替換；解析失敗的檔留原檔、已記 conflicts）：推 baseline（解析失敗的檔不推）→ metadata（版本／conflicts；state／lines）→ 重生 tools.just → 寫 version.toml → 刪日誌 → 0／2" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,816"/>
<mxCell id="uB3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1556,5,30,20"/>
<mxCell id="b15z" value="來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原檔、已記 conflicts" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="uB3" geo="750,36,300,80"/>
<mxCell id="b15a" value="推 baseline/&amp;lt;repo&amp;gt;/ 到目標版：逐檔，通過的檔推到 N（有衝突標記也推）；解析失敗的檔跳過不推（該檔 baseline 留上一版；v2.9 §4）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,136,360,63"/>
<mxCell id="b15a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,126,30,20"/>
<mxCell id="b15f" value="baseline/&amp;lt;repo&amp;gt;/（目標版範本副本，進 git；解析失敗的檔留上一版）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB3" geo="1300,146,280,42"/>
<mxCell id="b15b" value="寫 metadata：最後合併版本 = 目標版、衝突中檔案（conflicts）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,219,360,48"/>
<mxCell id="b15b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,209,30,20"/>
<mxCell id="b15bf" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB3" geo="1300,222,280,42"/>
<mxCell id="b15d" value="寫 metadata：每個 dest 的 state／declined_hash／append 行（lines）—— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,287,360,63"/>
<mxCell id="b15d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,277,30,20"/>
<mxCell id="b15df" value=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB3" geo="1300,298,280,42"/>
<mxCell id="b15g" value="重生 gen/tools.just（新版的 just/&amp;lt;ns&amp;gt;.just 可能增減；每個一行 mod?）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,370,360,48"/>
<mxCell id="b15g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,360,30,20"/>
<mxCell id="b15gf" value="gen/tools.just（不進 git；mod? 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB3" geo="1300,374,280,40"/>
<mxCell id="b16" value="寫 version.toml &amp;lt;repo&amp;gt; 行 → 目標 tag@digest（待合併：已是 B，不動）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,438,360,48"/>
<mxCell id="b16_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,428,30,20"/>
<mxCell id="b16f" value="version.toml（&amp;lt;repo&amp;gt; 行，進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uB3" geo="1300,442,280,40"/>
<mxCell id="b16x" value="失敗 → 1：明列已完成／未完成" style="fillColor=#f8cecc;strokeColor=#000000" parent="uB3" geo="20,506,220,58"/>
<mxCell id="b16x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="216,496,30,20"/>
<mxCell id="b16b" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uB3" geo="720,515,360,40"/>
<mxCell id="b16b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1056,505,30,20"/>
<mxCell id="b17" value="否 → 0：印摘要 → commit" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uB3" geo="20,611,220,58"/>
<mxCell id="b17_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="216,601,30,20"/>
<mxCell id="b16q" value="有衝突（conflicts 非空）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uB3" geo="720,584,240,112"/>
<mxCell id="b16q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="936,574,30,20"/>
<mxCell id="b18" value="是 → 2：印衝突檔名（含解析失敗的檔；解完再跑直到乾淨；baseline 已在目標版）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uB3" geo="720,734,360,58"/>
<mxCell id="b18r" value="多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；訊息全列；待合併補完後另有新版 → 印「已補齊 &amp;lt;repo&amp;gt; 至 vB；另有新版 vX，再跑一次可升」" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="uB3" geo="1300,716,280,94"/>
<mxCell id="b18r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uB3" geo="1556,706,30,20"/>
<mxCell id="be23" edge="1" source="b15z" target="b15a"/>
<mxCell id="be24" value="寫" edge="1" source="b15a" target="b15f"/>
<mxCell id="be24b" edge="1" source="b15a" target="b15b"/>
<mxCell id="be24bf" value="寫" edge="1" source="b15b" target="b15bf"/>
<mxCell id="be24d" edge="1" source="b15b" target="b15d"/>
<mxCell id="be24df" value="寫" edge="1" source="b15d" target="b15df"/>
<mxCell id="be25" edge="1" source="b15d" target="b15g"/>
<mxCell id="be25f" value="寫" edge="1" source="b15g" target="b15gf"/>
<mxCell id="be25g" edge="1" source="b15g" target="b16"/>
<mxCell id="be27" value="寫" edge="1" source="b16" target="b16f"/>
<mxCell id="be26" value="成功" edge="1" source="b16" target="b16b"/>
<mxCell id="be26x" value="失敗" edge="1" source="b16" target="b16x"/>
<mxCell id="be28q" edge="1" source="b16b" target="b16q"/>
<mxCell id="be28" value="否" edge="1" source="b16q" target="b17"/>
<mxCell id="be29" value="是" edge="1" source="b16q" target="b18"/>
<mxCell id="p7cq_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,973,200,60"/>
<mxCell id="p7cq_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,973,140,64"/>
<mxCell id="p7cq_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,981,140,44"/>
<mxCell id="p7cq_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,975,190,56"/>
<mxCell id="p7cq_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,975,210,56"/>
<mxCell id="p7cq_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,983,88,40"/>
<mxCell id="p7cq_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,983,170,40"/>
<mxCell id="p7cq_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,973,300,60"/>
<mxCell id="p7cq_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1041,200,36"/>
<mxCell id="p7cq_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1041,120,36"/>
<mxCell id="p7cq_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,1041,150,36"/>
<mxCell id="p7cq_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="570,1041,190,36"/>
<mxCell id="p7cq_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="780,1041,170,36"/>
<mxCell id="p7cq_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,1041,170,36"/>
<mxCell id="p7cq_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1160,1041,200,36"/>
<mxCell id="p7cq_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1336,1031,30,20"/>
<mxCell id="p7cq_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1079,200,28"/>
<mxCell id="p7cq_tk0" value="Renovate／regex manager" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1113,150,40"/>
<mxCell id="p7cq_tv0" value="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1113,610,40"/>
<mxCell id="p7cq_tk1" value="PR／commit／push／rebase／merge" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1153,150,40"/>
<mxCell id="p7cq_tv1" value="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1153,610,40"/>
<mxCell id="p7cq_tk2" value="check.sh／CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1193,150,55"/>
<mxCell id="p7cq_tv2" value="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1193,610,55"/>
<mxCell id="p7cq_tk3" value="baseline 落後／待合併" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1248,150,40"/>
<mxCell id="p7cq_tv3" value="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1248,610,40"/>
<mxCell id="p7cq_tk4" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1288,150,55"/>
<mxCell id="p7cq_tv4" value="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1288,610,55"/>
<mxCell id="p7cq_tk5" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1343,150,40"/>
<mxCell id="p7cq_tv5" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1343,610,40"/>
<mxCell id="p7cq_tk6" value="dev 覆寫／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1383,150,40"/>
<mxCell id="p7cq_tv6" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1383,610,40"/>
<mxCell id="p7cq_tk7" value="materialize／印記" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1423,150,40"/>
<mxCell id="p7cq_tv7" value="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1423,610,40"/>
<mxCell id="p7cq_tk8" value="B／D／N、逐檔判斷後詢問" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1463,150,86"/>
<mxCell id="p7cq_tv8" value="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1463,610,86"/>
<mxCell id="p7cq_tk9" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1113,150,71"/>
<mxCell id="p7cq_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1113,610,71"/>
<mxCell id="p7cq_tk10" value="gen／mod?" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1184,150,40"/>
<mxCell id="p7cq_tv10" value="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1184,610,40"/>
<mxCell id="p7cq_tk11" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1224,150,55"/>
<mxCell id="p7cq_tv11" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1224,610,55"/>
<mxCell id="p7cq_tk12" value="CRLF／append 行" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1279,150,40"/>
<mxCell id="p7cq_tv12" value="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1279,610,40"/>
<mxCell id="p7cq_tk13" value="GHCR／image／tag@digest" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1319,150,40"/>
<mxCell id="p7cq_tv13" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1319,610,40"/>
<mxCell id="p7cq_tk14" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1359,150,55"/>
<mxCell id="p7cq_tv14" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1359,610,55"/>
</diagram>
<diagram id="v1p7b" name="流程 v2：upgrade ── 逐檔判斷、衝突重入、回退">
<mxCell id="title" value="流程 v2：upgrade ── C. 逐檔判斷表、C′ 衝突重入、D. 回退（§5、v2.2 D、v2.3 §1、v2.5 §1／§2／§4）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1）：append 行比對 CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.2 E）：dist/files/ 第一版禁止 symlink。已定（v2.5 §2）：N 讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用之後。自身升級見「E. 自身升級」頁。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,61"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,81,220,28"/>
<mxCell id="hdr1" value="Renovate（GitHub 上）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,81,180,28"/>
<mxCell id="hdr2" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="480,81,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="740,81,360,28"/>
<mxCell id="hdr4" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1120,81,180,28"/>
<mxCell id="hdr5" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,81,280,28"/>
<mxCell id="uC" value="C. 逐檔判斷後詢問（每個 init.toml 檔；引擎 merge 模組；§5 表；在 apply 內、拿到 flock、建日誌後）＋ C′ 衝突重入（v2.2 D (0)、v2.5 §3）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,125,1600,905"/>
<mxCell id="uC_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uC" geo="1556,5,30,20"/>
<mxCell id="c_in0" value="B = baseline/&amp;lt;repo&amp;gt;/&amp;lt;檔&amp;gt;（上次合併的範本）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uC" geo="1300,50,280,42"/>
<mxCell id="c_in1" value="D = 專案裡的 &amp;lt;檔&amp;gt;（現況，你可能改過）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uC" geo="1300,106,280,40"/>
<mxCell id="c_in2" value="N = 目標版範本：暫存 /dist/&amp;lt;repo&amp;gt;/&amp;lt;檔&amp;gt;（不是 cache）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uC" geo="1300,162,280,42"/>
<mxCell id="c_in2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uC" geo="1556,152,30,20"/>
<mxCell id="c_m" value="引擎 merge 模組：三份比對，逐檔判斷（左表）→ 要改的先問（-y 免問；拒絕 → 不動、記 declined_hash；新檔才 state=declined）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uC" geo="730,54,340,60"/>
<mxCell id="c_h0" value="情況" style="fillColor=#e6e6e6;strokeColor=#999999" parent="uC" geo="20,70,170,28"/>
<mxCell id="c_h1" value="做法" style="fillColor=#e6e6e6;strokeColor=#999999" parent="uC" geo="190,70,290,28"/>
<mxCell id="c_h2" value="結果" style="fillColor=#e6e6e6;strokeColor=#999999" parent="uC" geo="480,70,230,28"/>
<mxCell id="c_r0c0" value="新版沒改／你的檔已等於新版（N==B 或 D==N）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,98,170,44"/>
<mxCell id="c_r0c1" value="不動" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,98,290,44"/>
<mxCell id="c_r0c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,98,230,44"/>
<mxCell id="c_r1c0" value="你刪了已納管的檔（D 缺）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,142,170,40"/>
<mxCell id="c_r1c1" value="不問、不重建" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,142,290,40"/>
<mxCell id="c_r1c2" value="state=deleted，維持刪除（§4.3）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,142,230,40"/>
<mxCell id="c_r2c0" value="新版改了、你沒改（D==B、N≠B）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,182,170,59"/>
<mxCell id="c_r2c1" value="問「X 換成新版？」" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,182,290,59"/>
<mxCell id="c_r2c2" value="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（目標新版再次更新時再問）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,182,230,59"/>
<mxCell id="c_r3c0" value="兩邊都改（D≠B、N≠B）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,241,170,122"/>
<mxCell id="c_r3c1" value="問「你和新版都改了 X，要三方合併嗎？」" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,241,290,122"/>
<mxCell id="c_r3c2" value="同意 → git merge-file --diff3（在暫存做）：乾淨 → 原子替換寫入；衝突 → 留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、回 2；baseline 仍推到目標版；解完重跑直到乾淨；拒絕 → 不動、state 不變只記 declined_hash" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,241,230,122"/>
<mxCell id="c_r4c0" value="新版新增（B 無）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,363,170,106"/>
<mxCell id="c_r4c1" value="問「要建 X 嗎」（-y 建）；已有同名 → 不納管；dest 在 CI 路徑時訊息醒目" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,363,290,106"/>
<mxCell id="c_r4c2" value="拒絕 → 不建、state=declined（唯一會用 declined 的情況；之後不再問；目標新版再次更新時重新詢問；dry-run／check.sh 印「有 N 個範本你拒絕過」）；不覆蓋、印「已存在，範本在 cache」" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,363,230,106"/>
<mxCell id="c_r5c0" value="新版刪除該檔（N 無）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,469,170,40"/>
<mxCell id="c_r5c1" value="不刪，只 warn" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,469,290,40"/>
<mxCell id="c_r5c2" value="你的檔留著" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,469,230,40"/>
<mxCell id="c_r6c0" value="append 行（strategy=append）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,509,170,75"/>
<mxCell id="c_r6c1" value="找到上次插入的行（CRLF／LF 視為相同，其餘精確）→ 問後替換" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,509,290,75"/>
<mxCell id="c_r6c2" value="唯一命中 → 替換；零命中或多處 → 保留只 warn、印新內容；拒絕 → 不動、state 維持 appended 只記 declined_hash" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,509,230,75"/>
<mxCell id="c_r7c0" value="二進位／symlink" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,584,170,59"/>
<mxCell id="c_r7c1" value="不合併：你未改（D==B）→ 問「X 是二進位檔，要換成新版嗎？」（-y 免問）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,584,290,59"/>
<mxCell id="c_r7c2" value="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（新版再更新時再問）；改過 → 保留 + warn" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,584,230,59"/>
<mxCell id="c_r8c0" value="CI 為真（frozen）且需改 tracked 檔" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="20,643,170,59"/>
<mxCell id="c_r8c1" value="apply 印清單 → 1（version.toml 未動；-y 不解除 frozen）" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="190,643,290,59"/>
<mxCell id="c_r8c2" value="--dry-run 也一樣：CI 為真且需改 tracked 檔 → 1；本機 → 0 只印清單" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="480,643,230,59"/>
<mxCell id="c_note" value="--dry-run = 唯讀預覽，只印會問哪些檔。衝突解完 → 再跑一次 upgrade 直到乾淨（2 = 需要人解衝突，橙）。dest 撞名規則見「add（1）」頁；四種詢問各一格見「B（2）」頁。" style="fillColor=#ffffff;strokeColor=#999999" parent="uC" geo="1300,218,280,73"/>
<mxCell id="cx_l" value="C′ 衝突重入（解完衝突後再跑 upgrade；v2.2 D (0)）—— 偵測在 resolve，清除在 apply（拿鎖、建日誌後）" style="fillColor=none;strokeColor=none" parent="uC" geo="20,732,700,26"/>
<mxCell id="cx0" value="解完衝突後再跑 upgrade &amp;lt;repo&amp;gt;" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uC" geo="20,772.0,220,58"/>
<mxCell id="cx1" value="衝突檔仍含我們的標籤？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uC" geo="730,776.0,340,50"/>
<mxCell id="cx1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uC" geo="1046,766,30,20"/>
<mxCell id="cx2" value="是 → 2：停（先解完標記再重跑）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uC" geo="1100,772.0,200,58"/>
<mxCell id="cx3" value="否：apply 拿鎖、建日誌後清除衝突狀態 → 接「B. 手動路徑（1）」頁的 (1)(2)（version.toml、baseline 已在目標版 → 通常「不動」）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uC" geo="730,842,340,57"/>
<mxCell id="cx3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uC" geo="1046,832,30,20"/>
<mxCell id="c_e0" edge="1" source="c_in0" target="c_m"/>
<mxCell id="c_e1" edge="1" source="c_in1" target="c_m"/>
<mxCell id="c_e2" edge="1" source="c_in2" target="c_m"/>
<mxCell id="c_e3" edge="1" source="c_m" target="c_h2"/>
<mxCell id="cx_e0" edge="1" source="cx0" target="cx1"/>
<mxCell id="cx_e1" value="是" edge="1" source="cx1" target="cx2"/>
<mxCell id="cx_e2" value="否" edge="1" source="cx1" target="cx3"/>
<mxCell id="uD" value="D. 回退 ＝ git revert 該升級 commit（version.toml + 初始檔 + baseline 同一 commit）；下次 just 的 sync 只把 cache/ 換回舊版" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,1046,1600,615"/>
<mxCell id="d0" value="git revert 該升級 commit" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uD" geo="20,36,220,58"/>
<mxCell id="d1a" value="下次 just：docker run 引擎 resolve sync" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="460,44,240,42"/>
<mxCell id="d2" value="sync resolve：gen/&amp;lt;repo&amp;gt;.stamp 第一行 ≠ version.toml 鎖定 digest → 待辦「materialize 舊版」" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uD" geo="720,36,360,57"/>
<mxCell id="d3b" value="初始檔、baseline/&amp;lt;repo&amp;gt;/、version.toml（由 git revert 還原，不是 sync 寫）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uD" geo="20,172,220,57"/>
<mxCell id="d1b" value="docker image inspect：舊版本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uD" geo="460,114,170,174"/>
<mxCell id="d1p" value="無：docker pull" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="630,308,70,57"/>
<mxCell id="d1g" value="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（version.toml 還原後的舊版）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="uD" geo="1100,308,180,57"/>
<mxCell id="d1c" value="docker create &amp;lt;img&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="460,385,240,40"/>
<mxCell id="d1d" value="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="460,445,240,42"/>
<mxCell id="d1e" value="docker rm 該容器" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="460,507,240,40"/>
<mxCell id="d1f" value="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro 引擎 apply sync" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uD" geo="460,567,240,42"/>
<mxCell id="d2c" value="materialize 舊版 → cache/&amp;lt;repo&amp;gt;/、寫印記（只寫 cache/、gen/；初始檔與 baseline 不碰）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uD" geo="720,567,360,42"/>
<mxCell id="d3" value="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp（舊版；sync 寫）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uD" geo="1300,567,280,42"/>
<mxCell id="de1" edge="1" source="d0" target="d1a"/>
<mxCell id="de2" edge="1" source="d1a" target="d2"/>
<mxCell id="de2b" edge="1" source="d2" target="d1b"/>
<mxCell id="de2n" value="無" edge="1" source="d1b" target="d1p"/>
<mxCell id="de2g" value="拉 /dist" edge="1" source="d1g" target="d1p"/>
<mxCell id="de2y" value="有" edge="1" source="d1b" target="d1c"/>
<mxCell id="de2p" edge="1" source="d1p" target="d1c"/>
<mxCell id="de2d" edge="1" source="d1c" target="d1d"/>
<mxCell id="de2e" edge="1" source="d1d" target="d1e"/>
<mxCell id="de2f" edge="1" source="d1e" target="d1f"/>
<mxCell id="de2h" edge="1" source="d1f" target="d2c"/>
<mxCell id="de3" value="寫" edge="1" source="d2c" target="d3"/>
<mxCell id="de4" edge="1" source="d0" target="d3b"/>
<mxCell id="p7b_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1677,200,60"/>
<mxCell id="p7b_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1677,140,64"/>
<mxCell id="p7b_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1685,140,44"/>
<mxCell id="p7b_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1679,190,56"/>
<mxCell id="p7b_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1679,210,56"/>
<mxCell id="p7b_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1687,88,40"/>
<mxCell id="p7b_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1687,170,40"/>
<mxCell id="p7b_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1677,300,60"/>
<mxCell id="p7b_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1745,120,36"/>
<mxCell id="p7b_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1745,190,36"/>
<mxCell id="p7b_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1745,170,36"/>
<mxCell id="p7b_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1745,170,36"/>
<mxCell id="p7b_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1745,200,36"/>
<mxCell id="p7b_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1735,30,20"/>
<mxCell id="p7b_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1783,200,28"/>
<mxCell id="p7b_tk0" value="B／D／N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1817,150,55"/>
<mxCell id="p7b_tv0" value="B = baseline（上次合併時的範本副本，進 git）；D = 現況（專案裡你的那份檔）；N = 目標版範本 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（不是 cache；v2.5 §2）；「D==B」= 你沒改過" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1817,610,55"/>
<mxCell id="p7b_tk1" value="逐檔判斷後詢問／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1872,150,71"/>
<mxCell id="p7b_tv1" value="apply = 動詞的第二段（拿到 flock、重驗指紋、建日誌後才寫檔）；三份比：N 改了才問「換成新版？」，兩邊都改才問「三方合併？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash，新檔（B 無）被拒才 state=declined；全部在暫存完成再逐檔原子替換；materialize 到 cache 在決定套用之後" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1872,610,71"/>
<mxCell id="p7b_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1943,150,40"/>
<mxCell id="p7b_tv2" value="同一動詞兩段：resolve 只讀只算（查目標版、輸出要拉的 image 與輸入指紋，不寫檔）→ 啟動器 docker 拉 image、展開到暫存 → apply 拿 flock 後重驗指紋才寫" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1943,610,40"/>
<mxCell id="p7b_tk3" value="flock／指紋" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1983,150,40"/>
<mxCell id="p7b_tv3" value="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1983,610,40"/>
<mxCell id="p7b_tk4" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2023,150,55"/>
<mxCell id="p7b_tv4" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行、衝突中檔案清單、進度日誌 state；衝突重入靠它的「衝突中檔案」清單" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2023,610,55"/>
<mxCell id="p7b_tk5" value="git merge-file --diff3" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2078,150,40"/>
<mxCell id="p7b_tv5" value="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤）；回傳衝突數 → 映射為結束狀態 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2078,610,40"/>
<mxCell id="p7b_tk6" value="衝突重入（v2.2 D (0)）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2118,150,40"/>
<mxCell id="p7b_tv6" value="再跑 upgrade 時 resolve 先看 metadata 的「衝突中檔案」：檔內仍有我們的標籤 → 2 停；檔案失蹤不算已解；都乾淨 → apply 拿鎖、建日誌後清除狀態再往下" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2118,610,40"/>
<mxCell id="p7b_tk7" value="--dry-run／CI 為真" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1817,150,55"/>
<mxCell id="p7b_tv7" value="apply --dry-run 唯讀預覽：只印會問哪些檔（哪些要換／合併／append 替換；讀 /dist/&amp;lt;repo&amp;gt;），不動任何檔；本機 → 0；CI 為真（CI 非空且不為 0／false = frozen）且需改 tracked 檔 → 1（-y 不解除）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1817,610,55"/>
<mxCell id="p7b_tk8" value="append 行／CRLF" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1872,150,40"/>
<mxCell id="p7b_tv8" value="strategy=append 的初始檔：upgrade 找上次插入的行（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）→ 問後替換；零命中或多處 → 保留只 warn" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1872,610,40"/>
<mxCell id="p7b_tk9" value="二進位／symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1912,150,55"/>
<mxCell id="p7b_tv9" value="二進位 = 不是文字的檔（圖片等）；symlink = 指向另一個路徑的捷徑；兩者不做行內合併：你沒改 → 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過保留 + warn；dist/files/ 第一版禁止 symlink" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1912,610,55"/>
<mxCell id="p7b_tk10" value="回退／git revert" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1967,150,40"/>
<mxCell id="p7b_tv10" value="git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、baseline 同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 只把 cache/&amp;lt;repo&amp;gt;/ 換回舊版" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1967,610,40"/>
<mxCell id="p7b_tk11" value="GHCR／image／印記／declined／declined_hash" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2007,150,71"/>
<mxCell id="p7b_tv11" value="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；印記 = gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（= 被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2007,610,71"/>
<mxCell id="p7b_tk12" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2078,150,55"/>
<mxCell id="p7b_tv12" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2078,610,55"/>
</diagram>
<diagram id="v1p7bc" name="流程 v2：upgrade ── E. 自身升級 (a)(b)">
<mxCell id="title" value="流程 v2：upgrade ── E. vendor_kit 自身升級 (a)(b)（v2.2 A／B、v2.3 §2、v2.5 §7、v2.6 §5）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,124"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,144,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,144,320,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="620,144,380,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1020,144,200,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,144,360,28"/>
<mxCell id="uE" value="E. vendor_kit 自身升級（v2.3 §2 統一版、v2.5 §7、v2.6 §5）：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit 見「E(c)」頁；install 修復也走同樣比對" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,188,1600,1565"/>
<mxCell id="uE_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="1556,5,30,20"/>
<mxCell id="s0" value="(a) upgrade 不帶 repo（含 vendor_kit 自身）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE" geo="20,36,220,80"/>
<mxCell id="s0_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,26,30,20"/>
<mxCell id="s1" value="docker run 舊引擎 resolve upgrade（全部）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE" geo="280,52,280,48"/>
<mxCell id="s1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="536,42,30,20"/>
<mxCell id="s2a" value="resolve：先完整預檢（含 dev 中工具 → 1 提示 undev）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,56,360,40"/>
<mxCell id="s2a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,46,30,20"/>
<mxCell id="s2n" value="否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE" geo="20,136,220,80"/>
<mxCell id="s2n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,126,30,20"/>
<mxCell id="s2q" value="引擎有新版？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE" geo="600,151,240,50"/>
<mxCell id="s2q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="816,141,30,20"/>
<mxCell id="s2b" value="是：apply（舊引擎）：flock 專案目錄" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,236,360,40"/>
<mxCell id="s2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,226,30,20"/>
<mxCell id="s2c" value="重驗指紋（不同 → 1「請重跑」，橙）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,296,360,40"/>
<mxCell id="s2c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,286,30,20"/>
<mxCell id="s2d" value="建進度日誌（第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,356,360,40"/>
<mxCell id="s2d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,346,30,20"/>
<mxCell id="s2e" value="只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,416,360,48"/>
<mxCell id="s2e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,406,30,20"/>
<mxCell id="s2f" value="version.toml 第一行 = 新引擎 ref" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uE" geo="1260,420,280,40"/>
<mxCell id="s2g" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE" geo="610,484,360,40"/>
<mxCell id="s2g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="946,474,30,20"/>
<mxCell id="s2h" value="apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE" geo="280,544,280,63"/>
<mxCell id="s2h_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="536,534,30,20"/>
<mxCell id="s2hx" value="否 → 1：apply 未改第一行（印 apply 的錯誤）" style="fillColor=#f8cecc;strokeColor=#000000" parent="uE" geo="20,628,220,80"/>
<mxCell id="s2hx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,618,30,20"/>
<mxCell id="s2h2" value="第一行變了且 == 計畫的 engine？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE" geo="300,627,240,81"/>
<mxCell id="s2h2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="516,617,30,20"/>
<mxCell id="s2ln" value="是 → docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE" geo="310,728,220,112"/>
<mxCell id="s2ln_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="506,718,30,20"/>
<mxCell id="s2lp" value="無：docker pull 新引擎" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE" geo="500,860,80,79"/>
<mxCell id="s2lp_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="556,850,30,20"/>
<mxCell id="s2gi" value="vendor_kit:vY&lt;br&gt;（新引擎）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="uE" geo="1000,878,200,42"/>
<mxCell id="s2lv" value="覆寫中且 .Id ≠ 記的 image ID？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE" geo="310,959,220,112"/>
<mxCell id="s2lv_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="506,949,30,20"/>
<mxCell id="s2lx" value="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" style="fillColor=#f8cecc;strokeColor=#000000" parent="uE" geo="600,975,240,80"/>
<mxCell id="s2lx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="816,965,30,20"/>
<mxCell id="s4" value="→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE" geo="20,1091,220,146"/>
<mxCell id="s4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,1081,30,20"/>
<mxCell id="s2r" value="docker run 新引擎 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE" geo="260,1144,320,40"/>
<mxCell id="s2r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="556,1134,30,20"/>
<mxCell id="s5" value="(b) 別人 pull 後（第一行已變）打任何 just" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE" geo="20,1257,220,58"/>
<mxCell id="s5_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,1247,30,20"/>
<mxCell id="s6a" value="啟動器：grep version.toml 第一行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE" geo="280,1266,280,40"/>
<mxCell id="s6a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="536,1256,30,20"/>
<mxCell id="s8" value="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE" geo="20,1335,220,146"/>
<mxCell id="s8_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="216,1325,30,20"/>
<mxCell id="s6q" value="gen/.stamp 的引擎 ref == 第一行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE" geo="300,1352,240,112"/>
<mxCell id="s6q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE" geo="516,1342,30,20"/>
<mxCell id="s6y" value="是 → 正常跑（「sync（1）」頁）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE" geo="300,1501,240,58"/>
<mxCell id="se1" edge="1" source="s0" target="s1"/>
<mxCell id="se2" edge="1" source="s1" target="s2a"/>
<mxCell id="se2q" edge="1" source="s2a" target="s2q"/>
<mxCell id="se2n" value="否" edge="1" source="s2q" target="s2n"/>
<mxCell id="se3" value="是" edge="1" source="s2q" target="s2b"/>
<mxCell id="se3c" edge="1" source="s2b" target="s2c"/>
<mxCell id="se3d" edge="1" source="s2c" target="s2d"/>
<mxCell id="se3e" edge="1" source="s2d" target="s2e"/>
<mxCell id="se4" value="寫" edge="1" source="s2e" target="s2f"/>
<mxCell id="se3g" edge="1" source="s2e" target="s2g"/>
<mxCell id="se5" edge="1" source="s2g" target="s2h"/>
<mxCell id="se5h" edge="1" source="s2h" target="s2h2"/>
<mxCell id="se5x" value="否" edge="1" source="s2h2" target="s2hx"/>
<mxCell id="se5l" value="是" edge="1" source="s2h2" target="s2ln"/>
<mxCell id="se6p" value="無" edge="1" source="s2ln" target="s2lp"/>
<mxCell id="se6" value="拉" edge="1" source="s2gi" target="s2lp"/>
<mxCell id="se6y" value="有" edge="1" source="s2ln" target="s2lv"/>
<mxCell id="se6pv" edge="1" source="s2lp" target="s2lv"/>
<mxCell id="se6px" value="失敗" edge="1" source="s2lp" target="s2lx"/>
<mxCell id="se6vx" value="是" edge="1" source="s2lv" target="s2lx"/>
<mxCell id="se6vr" value="否" edge="1" source="s2lv" target="s2r"/>
<mxCell id="se7" edge="1" source="s2r" target="s4"/>
<mxCell id="se8" edge="1" source="s5" target="s6a"/>
<mxCell id="se8q" edge="1" source="s6a" target="s6q"/>
<mxCell id="se9" value="否" edge="1" source="s6q" target="s8"/>
<mxCell id="se9y" value="是" edge="1" source="s6q" target="s6y"/>
<mxCell id="p7bc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1769,200,60"/>
<mxCell id="p7bc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1769,140,64"/>
<mxCell id="p7bc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1777,140,44"/>
<mxCell id="p7bc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1771,190,56"/>
<mxCell id="p7bc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1771,210,56"/>
<mxCell id="p7bc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1779,88,40"/>
<mxCell id="p7bc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1779,170,40"/>
<mxCell id="p7bc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1769,300,60"/>
<mxCell id="p7bc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1837,120,36"/>
<mxCell id="p7bc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1837,190,36"/>
<mxCell id="p7bc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1837,170,36"/>
<mxCell id="p7bc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1837,170,36"/>
<mxCell id="p7bc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1837,200,36"/>
<mxCell id="p7bc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1827,30,20"/>
<mxCell id="p7bc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1875,200,28"/>
<mxCell id="p7bc_tk0" value="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1909,150,86"/>
<mxCell id="p7bc_tv0" value="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1909,610,86"/>
<mxCell id="p7bc_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1995,150,55"/>
<mxCell id="p7bc_tv1" value="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1995,610,55"/>
<mxCell id="p7bc_tk2" value="薄殼首行自描述（Q17）／上次產物／相符" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2050,150,55"/>
<mxCell id="p7bc_tv2" value="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2050,610,55"/>
<mxCell id="p7bc_tk3" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2105,150,40"/>
<mxCell id="p7bc_tv3" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2105,610,40"/>
<mxCell id="p7bc_tk4" value="GHCR／registry／引擎 image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2145,150,55"/>
<mxCell id="p7bc_tv4" value="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2145,610,55"/>
<mxCell id="p7bc_tk5" value="image ID／docker image inspect／local 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2200,150,55"/>
<mxCell id="p7bc_tv5" value="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2200,610,55"/>
<mxCell id="p7bc_tk6" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1909,150,55"/>
<mxCell id="p7bc_tv6" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1909,610,55"/>
<mxCell id="p7bc_tk7" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1964,150,40"/>
<mxCell id="p7bc_tv7" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1964,610,40"/>
<mxCell id="p7bc_tk8" value="dev 覆寫／undev／多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2004,150,40"/>
<mxCell id="p7bc_tv8" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2004,610,40"/>
<mxCell id="p7bc_tk9" value="--protocol P／降版（Q19）／結束碼 3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2044,150,71"/>
<mxCell id="p7bc_tv9" value="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2044,610,71"/>
<mxCell id="p7bc_tk10" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2115,150,55"/>
<mxCell id="p7bc_tv10" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2115,610,55"/>
</diagram>
<diagram id="v1p7bcc" name="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）">
<mxCell id="title" value="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）啟動器 → 查 registry → 改第一行（v2.7 §5）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,124"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,144,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,144,320,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="620,144,380,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1020,144,200,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,144,360,28"/>
<mxCell id="uE2" value="E(c)（1）upgrade vendor_kit[@&amp;lt;tag&amp;gt;]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗 → 薄殼 == 上次產物？（否 → 1 零寫入，v2.8 §3）→ @舊版無法無損讀 → 3 → 查 registry → 有新版 → 改第一行 → 用新引擎再跑；否則見「E(c)（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,188,1600,1442"/>
<mxCell id="uE2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="1556,5,30,20"/>
<mxCell id="s10" value="(c) just vendor_kit upgrade vendor_kit[@&amp;lt;tag&amp;gt;]（(b) 提示後由使用者打；也可直接打）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE2" geo="20,36,220,124"/>
<mxCell id="s10_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="216,26,30,20"/>
<mxCell id="s11a" value="grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE2" geo="280,66,280,63"/>
<mxCell id="s11a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="536,56,30,20"/>
<mxCell id="s11n" value="docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="280,180,220,112"/>
<mxCell id="s11n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="476,170,30,20"/>
<mxCell id="s11p" value="無：docker pull 該引擎" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE2" geo="500,312,80,79"/>
<mxCell id="s11p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="556,302,30,20"/>
<mxCell id="s11g" value="vendor_kit:vN&lt;br&gt;（第一行指到的引擎）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="uE2" geo="1000,330,200,42"/>
<mxCell id="s11v" value="覆寫中且 .Id ≠ 記的 image ID？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="280,411,220,112"/>
<mxCell id="s11v_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="476,401,30,20"/>
<mxCell id="s11x" value="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" style="fillColor=#f8cecc;strokeColor=#000000" parent="uE2" geo="600,427,240,80"/>
<mxCell id="s11x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="816,417,30,20"/>
<mxCell id="s10a" value="來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="uE2" geo="20,543,220,102"/>
<mxCell id="s11r" value="否：docker run 該引擎 upgrade vendor_kit" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE2" geo="260,574,320,40"/>
<mxCell id="s11r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="556,564,30,20"/>
<mxCell id="s12a" value="flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE2" geo="610,574,360,40"/>
<mxCell id="s12a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="946,564,30,20"/>
<mxCell id="s12b" value="重驗指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE2" geo="600,674,220,40"/>
<mxCell id="s12b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="796,664,30,20"/>
<mxCell id="s12bx" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE2" geo="850,665,130,58"/>
<mxCell id="s12bx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="956,655,30,20"/>
<mxCell id="s12sx" value="否 → 1：偵測到薄殼被修改，列差異不動（零寫入；git checkout 還原後再跑）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE2" geo="20,748,220,102"/>
<mxCell id="s12sx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="216,738,30,20"/>
<mxCell id="s12s" value="薄殼 == 上次產物？（首行自描述 hash、未被改）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="600,743,260,112"/>
<mxCell id="s12s_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="836,733,30,20"/>
<mxCell id="s12sn" value="「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入（含改第一行）之前檢查，不符 → 1 列差異、零寫入（v2.8 §3）" style="fillColor=#ffffff;strokeColor=#999999" parent="uE2" geo="1220,760,360,79"/>
<mxCell id="s12sn_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="1556,750,30,20"/>
<mxCell id="s12dx" value="是 → 3：印 6-10「目標引擎無法無損讀取現有檔；未修改任何檔；要退回請 git revert」（零寫入）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE2" geo="20,875,220,124"/>
<mxCell id="s12dx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="216,865,30,20"/>
<mxCell id="s12d" value="是 → @&amp;lt;tag&amp;gt; 為舊版且無法無損讀現有檔（P／schema）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="600,881,260,112"/>
<mxCell id="s12d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="836,871,30,20"/>
<mxCell id="s12t" value="否 → @&amp;lt;tag&amp;gt; 指定或 CI 為真（frozen）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="600,1019,260,112"/>
<mxCell id="s12t_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="836,1009,30,20"/>
<mxCell id="s12tn" value="是：不查 registry" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE2" geo="880,1051,100,48"/>
<mxCell id="s12tn_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="956,1041,30,20"/>
<mxCell id="s12u" value="否：查 registry（GHCR）取引擎最新正式版" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE2" geo="600,1151,260,48"/>
<mxCell id="s12u_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="836,1141,30,20"/>
<mxCell id="s12v" value="有新版？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE2" geo="600,1230,200,50"/>
<mxCell id="s12v_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="776,1220,30,20"/>
<mxCell id="s12vz" value="否／不查 → 續「E(c)（2）」頁：薄殼比對與重產" style="fillColor=none;strokeColor=none" parent="uE2" geo="870,1219,110,73"/>
<mxCell id="s12hz" value="→ 用新引擎從本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE2" geo="20,1312,220,124"/>
<mxCell id="s12hz_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="216,1302,30,20"/>
<mxCell id="s12h" value="啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="uE2" geo="270,1342,300,63"/>
<mxCell id="s12h_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="546,1332,30,20"/>
<mxCell id="s12w" value="是：改 version.toml 第一行 = 新引擎 ref（其餘不動）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE2" geo="600,1350,260,48"/>
<mxCell id="s12w_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE2" geo="836,1340,30,20"/>
<mxCell id="s12wf" value="version.toml 第一行 = 新引擎 ref（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uE2" geo="1220,1354,360,40"/>
<mxCell id="se11" edge="1" source="s10" target="s11a"/>
<mxCell id="se11q" edge="1" source="s11a" target="s11n"/>
<mxCell id="se11p" value="無" edge="1" source="s11n" target="s11p"/>
<mxCell id="se11g" value="拉" edge="1" source="s11g" target="s11p"/>
<mxCell id="se11v" value="有" edge="1" source="s11n" target="s11v"/>
<mxCell id="se11pv" edge="1" source="s11p" target="s11v"/>
<mxCell id="se11px" value="失敗" edge="1" source="s11p" target="s11x"/>
<mxCell id="se11vx" value="是" edge="1" source="s11v" target="s11x"/>
<mxCell id="se11vr" value="否" edge="1" source="s11v" target="s11r"/>
<mxCell id="se11e" edge="1" source="s10a" target="s11r"/>
<mxCell id="se12" edge="1" source="s11r" target="s12a"/>
<mxCell id="se12b" edge="1" source="s12a" target="s12b"/>
<mxCell id="se12x" edge="1" source="s12b" target="s12bx"/>
<mxCell id="se12s" edge="1" source="s12b" target="s12s"/>
<mxCell id="se12sx" value="否" edge="1" source="s12s" target="s12sx"/>
<mxCell id="se12d" value="是" edge="1" source="s12s" target="s12d"/>
<mxCell id="se12dx" value="是" edge="1" source="s12d" target="s12dx"/>
<mxCell id="se12t" value="否" edge="1" source="s12d" target="s12t"/>
<mxCell id="se12tn" value="是" edge="1" source="s12t" target="s12tn"/>
<mxCell id="se12u" value="否" edge="1" source="s12t" target="s12u"/>
<mxCell id="se12v" edge="1" source="s12u" target="s12v"/>
<mxCell id="se12vn" value="否" edge="1" source="s12v" target="s12vz"/>
<mxCell id="se12tv" edge="1" source="s12tn" target="s12vz"/>
<mxCell id="se12w" value="是" edge="1" source="s12v" target="s12w"/>
<mxCell id="se12wf" value="寫" edge="1" source="s12w" target="s12wf"/>
<mxCell id="se12wh" edge="1" source="s12w" target="s12h"/>
<mxCell id="se12hz" edge="1" source="s12h" target="s12hz"/>
<mxCell id="p7bcc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1646,200,60"/>
<mxCell id="p7bcc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1646,140,64"/>
<mxCell id="p7bcc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1654,140,44"/>
<mxCell id="p7bcc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1648,190,56"/>
<mxCell id="p7bcc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1648,210,56"/>
<mxCell id="p7bcc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1656,88,40"/>
<mxCell id="p7bcc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1656,170,40"/>
<mxCell id="p7bcc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1646,300,60"/>
<mxCell id="p7bcc_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1714,200,36"/>
<mxCell id="p7bcc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1714,120,36"/>
<mxCell id="p7bcc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1714,190,36"/>
<mxCell id="p7bcc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1714,170,36"/>
<mxCell id="p7bcc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1714,170,36"/>
<mxCell id="p7bcc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1714,200,36"/>
<mxCell id="p7bcc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1704,30,20"/>
<mxCell id="p7bcc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1752,200,28"/>
<mxCell id="p7bcc_tk0" value="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1786,150,86"/>
<mxCell id="p7bcc_tv0" value="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1786,610,86"/>
<mxCell id="p7bcc_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1872,150,55"/>
<mxCell id="p7bcc_tv1" value="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1872,610,55"/>
<mxCell id="p7bcc_tk2" value="薄殼首行自描述（Q17）／上次產物／相符" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1927,150,55"/>
<mxCell id="p7bcc_tv2" value="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1927,610,55"/>
<mxCell id="p7bcc_tk3" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1982,150,40"/>
<mxCell id="p7bcc_tv3" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1982,610,40"/>
<mxCell id="p7bcc_tk4" value="GHCR／registry／引擎 image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2022,150,55"/>
<mxCell id="p7bcc_tv4" value="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2022,610,55"/>
<mxCell id="p7bcc_tk5" value="image ID／docker image inspect／local 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2077,150,55"/>
<mxCell id="p7bcc_tv5" value="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2077,610,55"/>
<mxCell id="p7bcc_tk6" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1786,150,55"/>
<mxCell id="p7bcc_tv6" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1786,610,55"/>
<mxCell id="p7bcc_tk7" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1841,150,40"/>
<mxCell id="p7bcc_tv7" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1841,610,40"/>
<mxCell id="p7bcc_tk8" value="dev 覆寫／undev／多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1881,150,40"/>
<mxCell id="p7bcc_tv8" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1881,610,40"/>
<mxCell id="p7bcc_tk9" value="--protocol P／降版（Q19）／結束碼 3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1921,150,71"/>
<mxCell id="p7bcc_tv9" value="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1921,610,71"/>
<mxCell id="p7bcc_tk10" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1992,150,55"/>
<mxCell id="p7bcc_tv10" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1992,610,55"/>
</diagram>
<diagram id="v1p7bccc" name="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）">
<mxCell id="title" value="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）薄殼比對 → 重產（v2.2 A、v2.3 §2、Q17、v2.7 §5）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,124"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,144,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,144,320,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="620,144,380,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1020,144,200,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,144,360,28"/>
<mxCell id="uE3" value="E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 拿鎖重驗後驗過，v2.8 §3）：已是本引擎產物？→ 是 → 0 無變更；否 → 建日誌 → 重產薄殼四檔 + gen/.stamp + tools.just → 刪日誌 → 1" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,188,1600,900"/>
<mxCell id="uE3_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="1556,5,30,20"/>
<mxCell id="s12z0" value="來自「E(c)（1）」頁：無新版／不查（第一行未變；已拿鎖、重驗，且薄殼 == 上次產物）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="uE3" geo="610,36,360,80"/>
<mxCell id="s12n" value="「薄殼 == 上次產物」（首行自描述 sha256 與其餘內容相符，Q17）已在「E(c)（1）」頁拿鎖重驗後、任何寫入前驗過（v2.8 §3）；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更（v2.7 §5）" style="fillColor=#ffffff;strokeColor=#999999" parent="uE3" geo="1220,152,360,79"/>
<mxCell id="s12n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="1556,142,30,20"/>
<mxCell id="s12z" value="是 → 0：無變更（薄殼相符，已是本引擎產物）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="uE3" geo="20,163,220,58"/>
<mxCell id="s12z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="216,153,30,20"/>
<mxCell id="s12e" value="首行 engine == 本引擎且 gen/.stamp 相符？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="uE3" geo="600,136,300,112"/>
<mxCell id="s12e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="876,126,30,20"/>
<mxCell id="s12l" value="否：建進度日誌（第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE3" geo="610,268,360,40"/>
<mxCell id="s12l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="946,258,30,20"/>
<mxCell id="s13" value="重產薄殼四檔（暫存 → 原子替換）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE3" geo="610,387,360,40"/>
<mxCell id="s13_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="946,377,30,20"/>
<mxCell id="s13f" value="薄殼四檔（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uE3" geo="1220,328,360,158"/>
<mxCell id="s13f_0" value=".vendor_kit/.gitignore" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="s13f" geo="8,26,344,26"/>
<mxCell id="s13f_1" value=".vendor_kit/entry.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="s13f" geo="8,58,344,26"/>
<mxCell id="s13f_2" value=".vendor_kit/vendor.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="s13f" geo="8,90,344,26"/>
<mxCell id="s13f_3" value=".vendor_kit/ci/check.sh" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="s13f" geo="8,122,344,26"/>
<mxCell id="s13b" value="寫 gen/.stamp（本引擎 ref）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE3" geo="610,506,360,40"/>
<mxCell id="s13b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="946,496,30,20"/>
<mxCell id="s13bf" value="gen/.stamp（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uE3" geo="1220,506,360,40"/>
<mxCell id="s13c" value="重生 gen/tools.just（用本引擎的規則；mod? 行）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE3" geo="610,566,360,40"/>
<mxCell id="s13c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="946,556,30,20"/>
<mxCell id="s13cf" value="gen/tools.just（不進 git；mod? 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="uE3" geo="1220,566,360,40"/>
<mxCell id="s13x" value="失敗 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE3" geo="20,626,220,146"/>
<mxCell id="s13x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="216,616,30,20"/>
<mxCell id="s13d" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="uE3" geo="610,679,360,40"/>
<mxCell id="s13d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="946,669,30,20"/>
<mxCell id="s14" value="1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="uE3" geo="20,792,220,102"/>
<mxCell id="s14_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="uE3" geo="216,782,30,20"/>
<mxCell id="se13" edge="1" source="s12z0" target="s12e"/>
<mxCell id="se15z" value="是" edge="1" source="s12e" target="s12z"/>
<mxCell id="se15l" value="否" edge="1" source="s12e" target="s12l"/>
<mxCell id="se15s" edge="1" source="s12l" target="s13"/>
<mxCell id="se16" value="寫" edge="1" source="s13" target="s13f"/>
<mxCell id="se17" edge="1" source="s13" target="s13b"/>
<mxCell id="se18" value="寫" edge="1" source="s13b" target="s13bf"/>
<mxCell id="se18b" edge="1" source="s13b" target="s13c"/>
<mxCell id="se18c" value="寫" edge="1" source="s13c" target="s13cf"/>
<mxCell id="se18d" value="成功" edge="1" source="s13c" target="s13d"/>
<mxCell id="se18x" value="失敗" edge="1" source="s13c" target="s13x"/>
<mxCell id="se19" edge="1" source="s13d" target="s14"/>
<mxCell id="p7bcd_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1104,200,60"/>
<mxCell id="p7bcd_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1104,140,64"/>
<mxCell id="p7bcd_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1112,140,44"/>
<mxCell id="p7bcd_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1106,190,56"/>
<mxCell id="p7bcd_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1106,210,56"/>
<mxCell id="p7bcd_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1114,88,40"/>
<mxCell id="p7bcd_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1114,170,40"/>
<mxCell id="p7bcd_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1104,300,60"/>
<mxCell id="p7bcd_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1172,200,36"/>
<mxCell id="p7bcd_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1172,120,36"/>
<mxCell id="p7bcd_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1172,190,36"/>
<mxCell id="p7bcd_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1172,170,36"/>
<mxCell id="p7bcd_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1172,170,36"/>
<mxCell id="p7bcd_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1172,200,36"/>
<mxCell id="p7bcd_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1162,30,20"/>
<mxCell id="p7bcd_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1210,200,28"/>
<mxCell id="p7bcd_tk0" value="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1244,150,86"/>
<mxCell id="p7bcd_tv0" value="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1244,610,86"/>
<mxCell id="p7bcd_tk1" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1330,150,55"/>
<mxCell id="p7bcd_tv1" value="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1330,610,55"/>
<mxCell id="p7bcd_tk2" value="薄殼首行自描述（Q17）／上次產物／相符" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1385,150,55"/>
<mxCell id="p7bcd_tv2" value="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1385,610,55"/>
<mxCell id="p7bcd_tk3" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1440,150,40"/>
<mxCell id="p7bcd_tv3" value="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1440,610,40"/>
<mxCell id="p7bcd_tk4" value="GHCR／registry／引擎 image／引擎 ref" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1480,150,55"/>
<mxCell id="p7bcd_tv4" value="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1480,610,55"/>
<mxCell id="p7bcd_tk5" value="image ID／docker image inspect／local 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1535,150,55"/>
<mxCell id="p7bcd_tv5" value="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1535,610,55"/>
<mxCell id="p7bcd_tk6" value="metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1244,150,55"/>
<mxCell id="p7bcd_tv6" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1244,610,55"/>
<mxCell id="p7bcd_tk7" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1299,150,40"/>
<mxCell id="p7bcd_tv7" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1299,610,40"/>
<mxCell id="p7bcd_tk8" value="dev 覆寫／undev／多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1339,150,40"/>
<mxCell id="p7bcd_tv8" value="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1339,610,40"/>
<mxCell id="p7bcd_tk9" value="--protocol P／降版（Q19）／結束碼 3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1379,150,71"/>
<mxCell id="p7bcd_tv9" value="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1379,610,71"/>
<mxCell id="p7bcd_tk10" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1450,150,55"/>
<mxCell id="p7bcd_tv10" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1450,610,55"/>
</diagram>
<diagram id="v1p8" name="流程 v2：dev &lt;repo&gt;">
<mxCell id="title" value="流程 v2：dev &amp;lt;repo&amp;gt;（§2 dev 列；v2.1 B、v2.2 B、v2.3 §3；&amp;lt;repo&amp;gt; = 工具 repo 名）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="vA" value="dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;：工具 path 覆寫（v2.1 B）—— 用本機工具 repo 的 dist/ 取代 image（不進 git；CI 拒絕；工具必須已在 version.toml；不經 docker create/cp）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,872"/>
<mxCell id="vA_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="1556,5,30,20"/>
<mxCell id="d0" value="just vendor_kit dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vA" geo="20,48,220,58"/>
<mxCell id="d1q" value="&amp;lt;dir&amp;gt;/dist/ 內有 init.toml？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vA" geo="300,36,240,81"/>
<mxCell id="d1q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="516,26,30,20"/>
<mxCell id="d1x" value="否 → 1：&amp;lt;dir&amp;gt;/dist/init.toml 不存在" style="fillColor=#f8cecc;strokeColor=#000000" parent="vA" geo="16,137,227,80"/>
<mxCell id="d1x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="219,127,30,20"/>
<mxCell id="d1m" value="是：準備掛載 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro（唯讀）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vA" geo="336,146,204,63"/>
<mxCell id="d1m_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="516,136,30,20"/>
<mxCell id="d1" value="docker run 引擎 dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;（不經 docker create/cp）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vA" geo="340,237,200,63"/>
<mxCell id="d1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="516,227,30,20"/>
<mxCell id="d3a" value="是 → 1：CI 拒絕 dev" style="fillColor=#f8cecc;strokeColor=#000000" parent="vA" geo="20,340,220,40"/>
<mxCell id="d2a" value="CI 為真？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vA" geo="560,320,130,81"/>
<mxCell id="d2b" value="已接入 &amp;lt;repo&amp;gt;？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vA" geo="720,336,240,50"/>
<mxCell id="d3c" value="否 → 1：dist/ 或 init.toml 不合法" style="fillColor=#f8cecc;strokeColor=#000000" parent="vA" geo="20,421,220,58"/>
<mxCell id="d2c" value="dist 合法？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vA" geo="560,425,180,50"/>
<mxCell id="d3b" value="否 → 1：未接入，請先 add &amp;lt;repo&amp;gt;" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vA" geo="770,421,190,58"/>
<mxCell id="d6a" value="是：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vA" geo="560,499,400,40"/>
<mxCell id="d6a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="936,489,30,20"/>
<mxCell id="d6" value="寫 version.local.toml：&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vA" geo="560,559,400,63"/>
<mxCell id="d6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="936,549,30,20"/>
<mxCell id="d6f" value="＋version.local.toml（不進 git）：&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vA" geo="1220,570,360,42"/>
<mxCell id="d7" value="cache/&amp;lt;repo&amp;gt;/ 改為 symlink → &amp;lt;dir&amp;gt;/dist（本機工具 repo 的 dist/，唯讀）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vA" geo="560,642,400,42"/>
<mxCell id="d7f" value="cache/&amp;lt;repo&amp;gt;/ → &amp;lt;dir&amp;gt;/dist（symlink，內容不複製）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vA" geo="1220,643,360,40"/>
<mxCell id="d7b" value="寫印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = path:&amp;lt;dir&amp;gt;（印記不放在 symlink 裡）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vA" geo="560,704,400,48"/>
<mxCell id="d7b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="936,694,30,20"/>
<mxCell id="d7bf" value="gen/&amp;lt;repo&amp;gt;.stamp 第一行：path:&amp;lt;dir&amp;gt;（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vA" geo="1220,708,360,40"/>
<mxCell id="d8" value="0：之後每次 just 用 &amp;lt;dir&amp;gt;" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vA" geo="20,790,220,58"/>
<mxCell id="d8_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="216,780,30,20"/>
<mxCell id="d9" value="dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="vA" geo="660,772,300,94"/>
<mxCell id="d9_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vA" geo="936,762,30,20"/>
<mxCell id="de1" edge="1" source="d0" target="d1q"/>
<mxCell id="de1x" value="否" edge="1" source="d1q" target="d1x"/>
<mxCell id="de1y" value="是" edge="1" source="d1q" target="d1m"/>
<mxCell id="de1m" edge="1" source="d1m" target="d1"/>
<mxCell id="de2" edge="1" source="d1" target="d2a"/>
<mxCell id="de3" value="是" edge="1" source="d2a" target="d3a"/>
<mxCell id="de4" value="否" edge="1" source="d2a" target="d2b"/>
<mxCell id="de5" value="是" edge="1" source="d2b" target="d2c"/>
<mxCell id="de6" value="否" edge="1" source="d2b" target="d3b"/>
<mxCell id="de7" value="否" edge="1" source="d2c" target="d3c"/>
<mxCell id="de8" value="是" edge="1" source="d2c" target="d6a"/>
<mxCell id="de8b" edge="1" source="d6a" target="d6"/>
<mxCell id="de9" value="寫" edge="1" source="d6" target="d6f"/>
<mxCell id="de10" edge="1" source="d6" target="d7"/>
<mxCell id="de11" value="寫" edge="1" source="d7" target="d7f"/>
<mxCell id="de12" edge="1" source="d7" target="d7b"/>
<mxCell id="de13" value="寫" edge="1" source="d7b" target="d7bf"/>
<mxCell id="de14" edge="1" source="d7b" target="d8"/>
<mxCell id="p8_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1044,200,60"/>
<mxCell id="p8_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1044,140,64"/>
<mxCell id="p8_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1052,140,44"/>
<mxCell id="p8_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1046,190,56"/>
<mxCell id="p8_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1046,210,56"/>
<mxCell id="p8_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1054,88,40"/>
<mxCell id="p8_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1054,170,40"/>
<mxCell id="p8_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1044,300,60"/>
<mxCell id="p8_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1112,120,36"/>
<mxCell id="p8_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1112,150,36"/>
<mxCell id="p8_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1112,190,36"/>
<mxCell id="p8_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1112,170,36"/>
<mxCell id="p8_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1112,170,36"/>
<mxCell id="p8_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1112,200,36"/>
<mxCell id="p8_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1102,30,20"/>
<mxCell id="p8_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1150,200,28"/>
<mxCell id="p8_tk0" value="dev／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1184,150,40"/>
<mxCell id="p8_tv0" value="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1184,610,40"/>
<mxCell id="p8_tk1" value="覆寫兩種（v2.1 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1224,150,55"/>
<mxCell id="p8_tv1" value="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1224,610,55"/>
<mxCell id="p8_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1279,150,40"/>
<mxCell id="p8_tv2" value="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1279,610,40"/>
<mxCell id="p8_tk3" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1319,150,55"/>
<mxCell id="p8_tv3" value=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1319,610,55"/>
<mxCell id="p8_tk4" value="symlink／印記／materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1374,150,55"/>
<mxCell id="p8_tv4" value="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1374,610,55"/>
<mxCell id="p8_tk5" value="image tag／image ID／RepoDigests" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1429,150,55"/>
<mxCell id="p8_tv5" value="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1429,610,55"/>
<mxCell id="p8_tk6" value="GHCR／tar／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1184,150,40"/>
<mxCell id="p8_tv6" value="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1184,610,40"/>
<mxCell id="p8_tk7" value="docker image inspect／掛載 -v" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1224,150,55"/>
<mxCell id="p8_tv7" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1224,610,55"/>
<mxCell id="p8_tk8" value="統一提示／gen/.stamp（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1279,150,55"/>
<mxCell id="p8_tv8" value="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1279,610,55"/>
<mxCell id="p8_tk9" value="metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1334,150,40"/>
<mxCell id="p8_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1334,610,40"/>
<mxCell id="p8_tk10" value="flock／指紋／進度日誌／CI 為真" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1374,150,55"/>
<mxCell id="p8_tv10" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1374,610,55"/>
<mxCell id="p8_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1429,150,55"/>
<mxCell id="p8_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1429,610,55"/>
</diagram>
<diagram id="v1p8ccc" name="流程 v2：dev vendor_kit">
<mxCell id="title" value="流程 v2：dev vendor_kit -i（§2 dev 列；v2.1 B、v2.2 B、v2.6 §1）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="vI" value="dev vendor_kit -i &amp;lt;本機 image tag&amp;gt;：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID（由啟動器 docker image inspect 取得後交給引擎，v2.8 §6）；驗收測試用同一機制" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,966"/>
<mxCell id="vI_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="1556,5,30,20"/>
<mxCell id="v0" value="dev vendor_kit -i &amp;lt;本機 image tag&amp;gt;" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vI" geo="20,38,220,58"/>
<mxCell id="v1i" value="docker image inspect &amp;lt;tag&amp;gt; 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vI" geo="260,36,280,63"/>
<mxCell id="v1i_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="516,26,30,20"/>
<mxCell id="v1" value="docker run 引擎 dev vendor_kit -i &amp;lt;tag&amp;gt;，image ID 一併交給引擎（引擎容器內不呼叫 docker）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vI" geo="260,119,280,63"/>
<mxCell id="v1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="516,109,30,20"/>
<mxCell id="v2x" value="是 → 1：CI 拒絕 dev（請在本機執行）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vI" geo="20,214,220,58"/>
<mxCell id="v2x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="216,204,30,20"/>
<mxCell id="v2q" value="CI 為真？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vI" geo="560,202,130,81"/>
<mxCell id="v2a" value="否：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vI" geo="560,303,400,40"/>
<mxCell id="v2a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="936,293,30,20"/>
<mxCell id="v2b" value="寫 version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;（不動薄殼）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vI" geo="560,364,400,40"/>
<mxCell id="v2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="936,354,30,20"/>
<mxCell id="v3" value="＋version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vI" geo="1220,363,360,42"/>
<mxCell id="v2c" value="寫 version.local.toml：vendor_kit_image_id = 啟動器交來的 image ID" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vI" geo="560,430,400,48"/>
<mxCell id="v2c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="936,420,30,20"/>
<mxCell id="v3c" value="version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vI" geo="1220,433,360,42"/>
<mxCell id="v2z" value="0：之後每次 just 用該本機 image" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vI" geo="20,425,220,58"/>
<mxCell id="v2z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="216,415,30,20"/>
<mxCell id="v5" value="下次打任何 just" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vI" geo="20,553,220,40"/>
<mxCell id="v6a" value="grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vI" geo="260,549,280,48"/>
<mxCell id="v6a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="516,539,30,20"/>
<mxCell id="vb" value="═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══" style="fillColor=none;strokeColor=none" parent="vI" geo="260,503,560,26"/>
<mxCell id="v8" value="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vI" geo="20,617,220,102"/>
<mxCell id="v8_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="216,607,30,20"/>
<mxCell id="v7" value="gen/.stamp 的引擎 ref == 該 tag？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vI" geo="265,628,270,81"/>
<mxCell id="v7_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="511,618,30,20"/>
<mxCell id="v9" value="→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vI" geo="20,760,220,102"/>
<mxCell id="v9_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="216,750,30,20"/>
<mxCell id="v6b" value="是：docker image inspect &amp;lt;tag&amp;gt; 的 .Id == 記的 image ID？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vI" geo="265,739,270,143"/>
<mxCell id="v6b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="511,729,30,20"/>
<mxCell id="v6x" value="否 → 1：本機 image 已變（同 tag 重 build）或不存在" style="fillColor=#f8cecc;strokeColor=#000000" parent="vI" geo="560,770,240,80"/>
<mxCell id="v6x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="776,760,30,20"/>
<mxCell id="v6c" value="是：docker run &amp;lt;tag&amp;gt; resolve sync（不 pull）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vI" geo="260,907,280,48"/>
<mxCell id="v6c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vI" geo="516,897,30,20"/>
<mxCell id="v10" value="0：正常跑（用該本機 image）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vI" geo="560,902,240,58"/>
<mxCell id="ve1" edge="1" source="v0" target="v1i"/>
<mxCell id="ve1i" edge="1" source="v1i" target="v1"/>
<mxCell id="ve2" edge="1" source="v1" target="v2q"/>
<mxCell id="ve3" value="是" edge="1" source="v2q" target="v2x"/>
<mxCell id="ve4" value="否" edge="1" source="v2q" target="v2a"/>
<mxCell id="ve4b" edge="1" source="v2a" target="v2b"/>
<mxCell id="ve5" value="寫" edge="1" source="v2b" target="v3"/>
<mxCell id="ve5c" edge="1" source="v2b" target="v2c"/>
<mxCell id="ve5cf" value="寫" edge="1" source="v2c" target="v3c"/>
<mxCell id="ve6" edge="1" source="v2c" target="v2z"/>
<mxCell id="ve7" edge="1" source="v5" target="v6a"/>
<mxCell id="ve8" edge="1" source="v6a" target="v7"/>
<mxCell id="ve9" value="否" edge="1" source="v7" target="v8"/>
<mxCell id="ve10" edge="1" source="v8" target="v9"/>
<mxCell id="ve11" value="是" edge="1" source="v7" target="v6b"/>
<mxCell id="ve11x" value="否" edge="1" source="v6b" target="v6x"/>
<mxCell id="ve11c" value="是" edge="1" source="v6b" target="v6c"/>
<mxCell id="ve12" edge="1" source="v6c" target="v10"/>
<mxCell id="p8v_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1138,200,60"/>
<mxCell id="p8v_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1138,140,64"/>
<mxCell id="p8v_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1146,140,44"/>
<mxCell id="p8v_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1140,190,56"/>
<mxCell id="p8v_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1140,210,56"/>
<mxCell id="p8v_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1148,88,40"/>
<mxCell id="p8v_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1148,170,40"/>
<mxCell id="p8v_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1138,300,60"/>
<mxCell id="p8v_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1206,120,36"/>
<mxCell id="p8v_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1206,190,36"/>
<mxCell id="p8v_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1206,170,36"/>
<mxCell id="p8v_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1206,170,36"/>
<mxCell id="p8v_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1206,200,36"/>
<mxCell id="p8v_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1196,30,20"/>
<mxCell id="p8v_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1244,200,28"/>
<mxCell id="p8v_tk0" value="dev／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1278,150,40"/>
<mxCell id="p8v_tv0" value="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1278,610,40"/>
<mxCell id="p8v_tk1" value="覆寫兩種（v2.1 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1318,150,55"/>
<mxCell id="p8v_tv1" value="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1318,610,55"/>
<mxCell id="p8v_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1373,150,40"/>
<mxCell id="p8v_tv2" value="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1373,610,40"/>
<mxCell id="p8v_tk3" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1413,150,55"/>
<mxCell id="p8v_tv3" value=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1413,610,55"/>
<mxCell id="p8v_tk4" value="symlink／印記／materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1468,150,55"/>
<mxCell id="p8v_tv4" value="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1468,610,55"/>
<mxCell id="p8v_tk5" value="image tag／image ID／RepoDigests" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1523,150,55"/>
<mxCell id="p8v_tv5" value="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1523,610,55"/>
<mxCell id="p8v_tk6" value="GHCR／tar／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1278,150,40"/>
<mxCell id="p8v_tv6" value="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1278,610,40"/>
<mxCell id="p8v_tk7" value="docker image inspect／掛載 -v" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1318,150,55"/>
<mxCell id="p8v_tv7" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1318,610,55"/>
<mxCell id="p8v_tk8" value="統一提示／gen/.stamp（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1373,150,55"/>
<mxCell id="p8v_tv8" value="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1373,610,55"/>
<mxCell id="p8v_tk9" value="metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1428,150,40"/>
<mxCell id="p8v_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1428,610,40"/>
<mxCell id="p8v_tk10" value="flock／指紋／進度日誌／CI 為真" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1468,150,55"/>
<mxCell id="p8v_tv10" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1468,610,55"/>
<mxCell id="p8v_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1523,150,55"/>
<mxCell id="p8v_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1523,610,55"/>
</diagram>
<diagram id="v1p8c" name="流程 v2：undev &lt;repo&gt;">
<mxCell id="title" value="流程 v2：undev（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §3／§10；&amp;lt;repo&amp;gt; = 工具 repo 名）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="vB" value="undev &amp;lt;repo&amp;gt;：回到 version.toml 鎖定版 = resolve → docker → apply（要重新 materialize，v2.3 §5；建日誌後才動，v2.5 §10；失敗 → 1 保留可恢復狀態，v2.2 B）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,1292"/>
<mxCell id="vB_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="1556,5,30,20"/>
<mxCell id="u0" value="just vendor_kit undev &amp;lt;repo&amp;gt;" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB" geo="20,36,220,58"/>
<mxCell id="u1" value="docker run 引擎 resolve undev &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="260,45,280,40"/>
<mxCell id="u3" value="否 → 0：未啟用 dev（提示）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB" geo="20,116,220,58"/>
<mxCell id="u2" value="有 path 覆寫？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB" geo="560,120,220,50"/>
<mxCell id="u4" value="是：resolve：要拉 &amp;lt;repo&amp;gt;-dist@digest（鎖定版）；輸出指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="800,114,160,63"/>
<mxCell id="u4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,104,30,20"/>
<mxCell id="u5a" value="docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB" geo="260,197,170,143"/>
<mxCell id="u5a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="406,187,30,20"/>
<mxCell id="u5p" value="無：docker pull" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="440,360,100,48"/>
<mxCell id="u5p_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="516,350,30,20"/>
<mxCell id="u5g" value="&amp;lt;repo&amp;gt;-dist@digest（鎖定版）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="vB" geo="980,364,220,40"/>
<mxCell id="u5b" value="docker create &amp;lt;img&amp;gt; /x" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="260,428,280,40"/>
<mxCell id="u5b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="516,418,30,20"/>
<mxCell id="u5c" value="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="260,488,280,48"/>
<mxCell id="u5c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="516,478,30,20"/>
<mxCell id="u5d" value="docker rm 該容器" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="260,556,280,40"/>
<mxCell id="u5d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="516,546,30,20"/>
<mxCell id="u5r" value="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro 引擎 apply undev &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB" geo="260,616,280,48"/>
<mxCell id="u5r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="516,606,30,20"/>
<mxCell id="u6a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,620,400,40"/>
<mxCell id="u6a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,610,30,20"/>
<mxCell id="u6b" value="重驗指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,693,240,40"/>
<mxCell id="u6b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="776,683,30,20"/>
<mxCell id="u6bx" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vB" geo="820,684,140,58"/>
<mxCell id="u6bx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,674,30,20"/>
<mxCell id="u6l" value="建進度日誌（.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,762,400,48"/>
<mxCell id="u6l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,752,30,20"/>
<mxCell id="u6lf" value="＋.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB" geo="1220,765,360,42"/>
<mxCell id="u6c" value="刪 version.local.toml 該行（&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；最後一個覆寫 → 刪整個檔）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,830,400,48"/>
<mxCell id="u6c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,820,30,20"/>
<mxCell id="u6cf" value="version.local.toml（少一行；空了就刪檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB" geo="1220,834,360,40"/>
<mxCell id="u6d" value="拆掉 cache/&amp;lt;repo&amp;gt;/ 的 symlink" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,898,400,40"/>
<mxCell id="u6d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,888,30,20"/>
<mxCell id="u6df" value="cache/&amp;lt;repo&amp;gt;/（不再是 symlink）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB" geo="1220,898,360,40"/>
<mxCell id="u6e" value="materialize 鎖定版：/dist/&amp;lt;repo&amp;gt; 展開到暫存目錄" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,958,400,40"/>
<mxCell id="u6e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,948,30,20"/>
<mxCell id="u6e2" value="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,1018,400,40"/>
<mxCell id="u6e2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,1008,30,20"/>
<mxCell id="u6ef" value="cache/&amp;lt;repo&amp;gt;/（重新展開）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB" geo="1220,1018,360,40"/>
<mxCell id="u6f" value="寫 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,1078,400,48"/>
<mxCell id="u6f_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,1068,30,20"/>
<mxCell id="u6ff" value="gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB" geo="1220,1082,360,40"/>
<mxCell id="u6x" value="失敗（任一步）→ 1：保留可恢復狀態（下次任何動詞先恢復）" style="fillColor=#f8cecc;strokeColor=#000000" parent="vB" geo="20,1146,220,80"/>
<mxCell id="u6x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="216,1136,30,20"/>
<mxCell id="u6g" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB" geo="560,1166,400,40"/>
<mxCell id="u6g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB" geo="936,1156,30,20"/>
<mxCell id="u7" value="成功 → 0" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB" geo="20,1246,220,40"/>
<mxCell id="ue1" edge="1" source="u0" target="u1"/>
<mxCell id="ue2" edge="1" source="u1" target="u2"/>
<mxCell id="ue3" value="否" edge="1" source="u2" target="u3"/>
<mxCell id="ue4" value="是" edge="1" source="u2" target="u4"/>
<mxCell id="ue5" edge="1" source="u4" target="u5a"/>
<mxCell id="ue5n" value="無" edge="1" source="u5a" target="u5p"/>
<mxCell id="ue6" value="拉 /dist" edge="1" source="u5g" target="u5p"/>
<mxCell id="ue5y" value="有" edge="1" source="u5a" target="u5b"/>
<mxCell id="ue5p" edge="1" source="u5p" target="u5b"/>
<mxCell id="ue5c" edge="1" source="u5b" target="u5c"/>
<mxCell id="ue5d" edge="1" source="u5c" target="u5d"/>
<mxCell id="ue7" edge="1" source="u5d" target="u5r"/>
<mxCell id="ue8" edge="1" source="u5r" target="u6a"/>
<mxCell id="ue8b" edge="1" source="u6a" target="u6b"/>
<mxCell id="ue8x" edge="1" source="u6b" target="u6bx"/>
<mxCell id="ue9" edge="1" source="u6b" target="u6l"/>
<mxCell id="ue9f" value="寫" edge="1" source="u6l" target="u6lf"/>
<mxCell id="ue10" edge="1" source="u6l" target="u6c"/>
<mxCell id="ue10f" value="寫" edge="1" source="u6c" target="u6cf"/>
<mxCell id="ue11" edge="1" source="u6c" target="u6d"/>
<mxCell id="ue11f" value="寫" edge="1" source="u6d" target="u6df"/>
<mxCell id="ue12" edge="1" source="u6d" target="u6e"/>
<mxCell id="ue12b" edge="1" source="u6e" target="u6e2"/>
<mxCell id="ue12f" value="寫" edge="1" source="u6e2" target="u6ef"/>
<mxCell id="ue13" edge="1" source="u6e2" target="u6f"/>
<mxCell id="ue13f" value="寫" edge="1" source="u6f" target="u6ff"/>
<mxCell id="ue14" value="成功" edge="1" source="u6f" target="u6g"/>
<mxCell id="ue14x" value="失敗" edge="1" source="u6f" target="u6x"/>
<mxCell id="ue15" edge="1" source="u6g" target="u7"/>
<mxCell id="p8c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1464,200,60"/>
<mxCell id="p8c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1464,140,64"/>
<mxCell id="p8c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1472,140,44"/>
<mxCell id="p8c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1466,190,56"/>
<mxCell id="p8c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1466,210,56"/>
<mxCell id="p8c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1474,88,40"/>
<mxCell id="p8c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1474,170,40"/>
<mxCell id="p8c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1464,300,60"/>
<mxCell id="p8c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1532,120,36"/>
<mxCell id="p8c_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1532,190,36"/>
<mxCell id="p8c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1532,170,36"/>
<mxCell id="p8c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1532,170,36"/>
<mxCell id="p8c_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1532,200,36"/>
<mxCell id="p8c_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1522,30,20"/>
<mxCell id="p8c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1570,200,28"/>
<mxCell id="p8c_tk0" value="dev／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1604,150,40"/>
<mxCell id="p8c_tv0" value="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1604,610,40"/>
<mxCell id="p8c_tk1" value="覆寫兩種（v2.1 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1644,150,55"/>
<mxCell id="p8c_tv1" value="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1644,610,55"/>
<mxCell id="p8c_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1699,150,40"/>
<mxCell id="p8c_tv2" value="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1699,610,40"/>
<mxCell id="p8c_tk3" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1739,150,55"/>
<mxCell id="p8c_tv3" value=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1739,610,55"/>
<mxCell id="p8c_tk4" value="symlink／印記／materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1794,150,55"/>
<mxCell id="p8c_tv4" value="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1794,610,55"/>
<mxCell id="p8c_tk5" value="image tag／image ID／RepoDigests" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1849,150,55"/>
<mxCell id="p8c_tv5" value="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1849,610,55"/>
<mxCell id="p8c_tk6" value="GHCR／tar／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1604,150,40"/>
<mxCell id="p8c_tv6" value="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1604,610,40"/>
<mxCell id="p8c_tk7" value="docker image inspect／掛載 -v" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1644,150,55"/>
<mxCell id="p8c_tv7" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1644,610,55"/>
<mxCell id="p8c_tk8" value="統一提示／gen/.stamp（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1699,150,55"/>
<mxCell id="p8c_tv8" value="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1699,610,55"/>
<mxCell id="p8c_tk9" value="metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1754,150,40"/>
<mxCell id="p8c_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1754,610,40"/>
<mxCell id="p8c_tk10" value="flock／指紋／進度日誌／CI 為真" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1794,150,55"/>
<mxCell id="p8c_tv10" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1794,610,55"/>
<mxCell id="p8c_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1849,150,55"/>
<mxCell id="p8c_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1849,610,55"/>
</diagram>
<diagram id="v1p8cc" name="流程 v2：undev vendor_kit">
<mxCell id="title" value="流程 v2：undev vendor_kit（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §10、v2.6 §1、v2.7 §6；Q10 (2)）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,112,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,112,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,112,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,112,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,112,360,28"/>
<mxCell id="vB′" value="undev vendor_kit = resolve → apply（無 image 要拉）：建 .tmp.undev.&amp;lt;id&amp;gt;.toml 日誌後才撤 vendor_kit 行（含 image ID）；最後一個覆寫撤掉 → 刪整個 version.local.toml；下次 just：gen/.stamp 不符 → 只回 1 提示（Q10 (2)）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,156,1600,1436"/>
<mxCell id="vB′_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="1556,5,30,20"/>
<mxCell id="w0" value="just vendor_kit undev vendor_kit" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB′" geo="20,36,220,58"/>
<mxCell id="w1" value="docker run 引擎 resolve undev vendor_kit" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="260,41,280,48"/>
<mxCell id="w1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="516,31,30,20"/>
<mxCell id="w3" value="否 → 0：未啟用（提示）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB′" geo="20,134,220,40"/>
<mxCell id="w2q" value="version.local.toml 有 vendor_kit 行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB′" geo="560,114,300,81"/>
<mxCell id="w2q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="836,104,30,20"/>
<mxCell id="w2s" value="是：resolve（不寫）：無 image 要拉；輸出輸入指紋（version.local.toml hash）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,215,400,48"/>
<mxCell id="w2s_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,205,30,20"/>
<mxCell id="w1b" value="docker run 引擎 apply undev vendor_kit" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="260,283,280,48"/>
<mxCell id="w1b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="516,273,30,20"/>
<mxCell id="w2a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,287,400,40"/>
<mxCell id="w2a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,277,30,20"/>
<mxCell id="w2b" value="重驗指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,360,240,40"/>
<mxCell id="w2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="776,350,30,20"/>
<mxCell id="w2bx" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vB′" geo="820,351,140,58"/>
<mxCell id="w2bx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,341,30,20"/>
<mxCell id="w2l" value="建進度日誌（.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,429,400,48"/>
<mxCell id="w2l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,419,30,20"/>
<mxCell id="w2lf" value="＋.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB′" geo="1220,432,360,42"/>
<mxCell id="w2x" value="失敗 → 1：保留可恢復狀態（下次可寫動詞先恢復）" style="fillColor=#f8cecc;strokeColor=#000000" parent="vB′" geo="20,497,220,80"/>
<mxCell id="w2x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="216,487,30,20"/>
<mxCell id="w2" value="刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,513,400,48"/>
<mxCell id="w2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,503,30,20"/>
<mxCell id="w2f" value="version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB′" geo="1220,516,360,42"/>
<mxCell id="w2e" value="還有其他覆寫行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB′" geo="560,597,200,81"/>
<mxCell id="w2e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="736,587,30,20"/>
<mxCell id="w2ed" value="否：刪整個 version.local.toml（最後一個覆寫已撤）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="790,606,170,63"/>
<mxCell id="w2ed_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,596,30,20"/>
<mxCell id="w2edf" value="－version.local.toml（整個檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vB′" geo="1220,618,360,40"/>
<mxCell id="w2edf_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="1556,608,30,20"/>
<mxCell id="w2g" value="是／已刪：刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vB′" geo="560,698,400,40"/>
<mxCell id="w2g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="936,688,30,20"/>
<mxCell id="w2z" value="0：本次結束（下次 just 用 version.toml 的引擎）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB′" geo="20,758,220,80"/>
<mxCell id="w2z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="216,748,30,20"/>
<mxCell id="wb" value="═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══" style="fillColor=none;strokeColor=none" parent="vB′" geo="260,858,560,26"/>
<mxCell id="w4" value="下次打任何 just" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB′" geo="20,908,220,40"/>
<mxCell id="w5a" value="grep version.toml 第一行取引擎 ref（local 已無覆寫）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="260,904,280,48"/>
<mxCell id="w5a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="516,894,30,20"/>
<mxCell id="w7" value="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」（不重寫）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vB′" geo="20,972,220,124"/>
<mxCell id="w7_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="216,962,30,20"/>
<mxCell id="w6" value="gen/.stamp 的引擎 ref == 第一行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB′" geo="260,994,270,81"/>
<mxCell id="w6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="506,984,30,20"/>
<mxCell id="w5b" value="是 → docker image inspect：本機有？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vB′" geo="260,1116,170,174"/>
<mxCell id="w5b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vB′" geo="406,1106,30,20"/>
<mxCell id="w5p" value="無：docker pull 該引擎" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="440,1310,100,42"/>
<mxCell id="w5g" value="vendor_kit:vN（version.toml 的引擎）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="vB′" geo="980,1310,220,42"/>
<mxCell id="w5c" value="docker run 該引擎 resolve sync" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vB′" geo="260,1381,280,40"/>
<mxCell id="w9" value="0：正常跑（「sync（1）」頁）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vB′" geo="560,1372,200,58"/>
<mxCell id="we1" edge="1" source="w0" target="w1"/>
<mxCell id="we2" edge="1" source="w1" target="w2q"/>
<mxCell id="we2n" value="否" edge="1" source="w2q" target="w3"/>
<mxCell id="we2y" value="是" edge="1" source="w2q" target="w2s"/>
<mxCell id="we2s" edge="1" source="w2s" target="w1b"/>
<mxCell id="we2a" edge="1" source="w1b" target="w2a"/>
<mxCell id="we2b" edge="1" source="w2a" target="w2b"/>
<mxCell id="we2bx" edge="1" source="w2b" target="w2bx"/>
<mxCell id="we2l" edge="1" source="w2b" target="w2l"/>
<mxCell id="we2lf" value="寫" edge="1" source="w2l" target="w2lf"/>
<mxCell id="we2w" edge="1" source="w2l" target="w2"/>
<mxCell id="we3" value="寫" edge="1" source="w2" target="w2f"/>
<mxCell id="we3x" value="失敗" edge="1" source="w2" target="w2x"/>
<mxCell id="we2e" edge="1" source="w2" target="w2e"/>
<mxCell id="we2ed" value="否" edge="1" source="w2e" target="w2ed"/>
<mxCell id="we2edf" value="刪" edge="1" source="w2ed" target="w2edf"/>
<mxCell id="we2g" value="是" edge="1" source="w2e" target="w2g"/>
<mxCell id="we2gd" edge="1" source="w2ed" target="w2g"/>
<mxCell id="we4" edge="1" source="w2g" target="w2z"/>
<mxCell id="we5" edge="1" source="w4" target="w5a"/>
<mxCell id="we6" edge="1" source="w5a" target="w6"/>
<mxCell id="we7" value="否" edge="1" source="w6" target="w7"/>
<mxCell id="we8" value="是" edge="1" source="w6" target="w5b"/>
<mxCell id="we8n" value="無" edge="1" source="w5b" target="w5p"/>
<mxCell id="we8g" value="拉" edge="1" source="w5g" target="w5p"/>
<mxCell id="we8y" value="有" edge="1" source="w5b" target="w5c"/>
<mxCell id="we8p" edge="1" source="w5p" target="w5c"/>
<mxCell id="we10" edge="1" source="w5c" target="w9"/>
<mxCell id="p8cc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1608,200,60"/>
<mxCell id="p8cc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1608,140,64"/>
<mxCell id="p8cc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1616,140,44"/>
<mxCell id="p8cc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1610,190,56"/>
<mxCell id="p8cc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1610,210,56"/>
<mxCell id="p8cc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1618,88,40"/>
<mxCell id="p8cc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1618,170,40"/>
<mxCell id="p8cc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1608,300,60"/>
<mxCell id="p8cc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1676,120,36"/>
<mxCell id="p8cc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1676,190,36"/>
<mxCell id="p8cc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1676,170,36"/>
<mxCell id="p8cc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1676,170,36"/>
<mxCell id="p8cc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1676,200,36"/>
<mxCell id="p8cc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1666,30,20"/>
<mxCell id="p8cc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1714,200,28"/>
<mxCell id="p8cc_tk0" value="dev／undev" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1748,150,40"/>
<mxCell id="p8cc_tv0" value="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1748,610,40"/>
<mxCell id="p8cc_tk1" value="覆寫兩種（v2.1 B）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1788,150,55"/>
<mxCell id="p8cc_tv1" value="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1788,610,55"/>
<mxCell id="p8cc_tk2" value="resolve／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1843,150,40"/>
<mxCell id="p8cc_tv2" value="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1843,610,40"/>
<mxCell id="p8cc_tk3" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1883,150,55"/>
<mxCell id="p8cc_tv3" value=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1883,610,55"/>
<mxCell id="p8cc_tk4" value="symlink／印記／materialize" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1938,150,55"/>
<mxCell id="p8cc_tv4" value="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1938,610,55"/>
<mxCell id="p8cc_tk5" value="image tag／image ID／RepoDigests" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1993,150,55"/>
<mxCell id="p8cc_tv5" value="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1993,610,55"/>
<mxCell id="p8cc_tk6" value="GHCR／tar／docker load" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1748,150,40"/>
<mxCell id="p8cc_tv6" value="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1748,610,40"/>
<mxCell id="p8cc_tk7" value="docker image inspect／掛載 -v" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1788,150,55"/>
<mxCell id="p8cc_tv7" value="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1788,610,55"/>
<mxCell id="p8cc_tk8" value="統一提示／gen/.stamp（Q10 (2)）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1843,150,55"/>
<mxCell id="p8cc_tv8" value="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1843,610,55"/>
<mxCell id="p8cc_tk9" value="metadata／baseline" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1898,150,40"/>
<mxCell id="p8cc_tv9" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1898,610,40"/>
<mxCell id="p8cc_tk10" value="flock／指紋／進度日誌／CI 為真" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1938,150,55"/>
<mxCell id="p8cc_tv10" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1938,610,55"/>
<mxCell id="p8cc_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1993,150,55"/>
<mxCell id="p8cc_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1993,610,55"/>
</diagram>
<diagram id="v1p8b" name="流程 v2：remove（1）resolve → apply 前置">
<mxCell id="title" value="流程 v2：remove（1）resolve → apply 前置（§2、§5；v2.2 C／E、v2.3 §5、v2.5 §3／§11）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="vC" value="remove &amp;lt;repo&amp;gt;（1）：拆掉一個工具（初始檔永不刪、印清單，要刪用 git rm）= resolve（讀 metadata → 刪除清單 → 詢問清單 → 計畫＋指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；無 image 要拉；寫入段見「remove（2）」頁" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,928"/>
<mxCell id="vC_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="1556,5,30,20"/>
<mxCell id="m0" value="just vendor_kit remove &amp;lt;repo&amp;gt;（-y、--dry-run）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vC" geo="20,36,220,80"/>
<mxCell id="m1" value="docker run &amp;lt;引擎&amp;gt; resolve remove &amp;lt;repo&amp;gt;（不經 docker create/cp）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC" geo="260,52,280,48"/>
<mxCell id="m1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="516,42,30,20"/>
<mxCell id="m3" value="否 → 0：未接入（提示）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vC" geo="20,141,220,40"/>
<mxCell id="m2" value="已接入 &amp;lt;repo&amp;gt;？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC" geo="560,136,280,50"/>
<mxCell id="m5" value="是 → 1：請先 undev &amp;lt;repo&amp;gt;（v2.1 B）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vC" geo="20,206,220,58"/>
<mxCell id="m4" value="有 dev path 覆寫？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC" geo="560,210,280,50"/>
<mxCell id="m6" value="否：resolve（不寫）：讀 metadata（append 過的行、完成標記）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,284,400,40"/>
<mxCell id="m6_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,274,30,20"/>
<mxCell id="m6b" value="產生刪除清單：version.toml 行、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、baseline/&amp;lt;repo&amp;gt;/、gen/tools.just 的 mod? 行" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,344,400,63"/>
<mxCell id="m6b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,334,30,20"/>
<mxCell id="m6c" value="產生詢問清單：metadata 記的 append 行（有才問）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,427,400,40"/>
<mxCell id="m6c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,417,30,20"/>
<mxCell id="m6d" value="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）→ 計畫＋指紋以 stdout 回啟動器" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,487,400,48"/>
<mxCell id="m6d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,477,30,20"/>
<mxCell id="m8" value="docker run &amp;lt;引擎&amp;gt; apply remove &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC" geo="260,555,280,48"/>
<mxCell id="m8_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="516,545,30,20"/>
<mxCell id="m9a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,559,400,40"/>
<mxCell id="m9a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,549,30,20"/>
<mxCell id="m9b" value="重驗指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC" geo="560,632,240,40"/>
<mxCell id="m9b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="776,622,30,20"/>
<mxCell id="m9x" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vC" geo="820,623,140,58"/>
<mxCell id="m9x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="936,613,30,20"/>
<mxCell id="m7cx" value="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vC" geo="20,702,220,80"/>
<mxCell id="m7cx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="216,692,30,20"/>
<mxCell id="m7c" value="CI 為真（frozen）且需改 tracked 檔？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC" geo="560,701,340,81"/>
<mxCell id="m7c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="876,691,30,20"/>
<mxCell id="m7y" value="是 → 0：只印清單（會刪什麼、會問什麼）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vC" geo="20,802,220,58"/>
<mxCell id="m7y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC" geo="216,792,30,20"/>
<mxCell id="m7" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC" geo="610,806,240,50"/>
<mxCell id="m7z" value="否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌" style="fillColor=none;strokeColor=none" parent="vC" geo="560,880,400,42"/>
<mxCell id="me1" edge="1" source="m0" target="m1"/>
<mxCell id="me2" edge="1" source="m1" target="m2"/>
<mxCell id="me3" value="否" edge="1" source="m2" target="m3"/>
<mxCell id="me4" value="是" edge="1" source="m2" target="m4"/>
<mxCell id="me5" value="是" edge="1" source="m4" target="m5"/>
<mxCell id="me6" value="否" edge="1" source="m4" target="m6"/>
<mxCell id="me6b" edge="1" source="m6" target="m6b"/>
<mxCell id="me6c" edge="1" source="m6b" target="m6c"/>
<mxCell id="me6d" edge="1" source="m6c" target="m6d"/>
<mxCell id="me7" edge="1" source="m6d" target="m8"/>
<mxCell id="me8" edge="1" source="m8" target="m9a"/>
<mxCell id="me8b" edge="1" source="m9a" target="m9b"/>
<mxCell id="me8x" edge="1" source="m9b" target="m9x"/>
<mxCell id="me9" edge="1" source="m9b" target="m7c"/>
<mxCell id="me9x" value="是" edge="1" source="m7c" target="m7cx"/>
<mxCell id="me9c" value="否" edge="1" source="m7c" target="m7"/>
<mxCell id="me10" value="是" edge="1" source="m7" target="m7y"/>
<mxCell id="me11" value="否" edge="1" source="m7" target="m7z"/>
<mxCell id="p8b_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1085,200,60"/>
<mxCell id="p8b_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1085,140,64"/>
<mxCell id="p8b_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1093,140,44"/>
<mxCell id="p8b_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1087,190,56"/>
<mxCell id="p8b_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1087,210,56"/>
<mxCell id="p8b_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1095,88,40"/>
<mxCell id="p8b_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1095,170,40"/>
<mxCell id="p8b_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1085,300,60"/>
<mxCell id="p8b_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1153,120,36"/>
<mxCell id="p8b_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1153,190,36"/>
<mxCell id="p8b_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="390,1153,170,36"/>
<mxCell id="p8b_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,1153,170,36"/>
<mxCell id="p8b_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="770,1153,200,36"/>
<mxCell id="p8b_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="946,1143,30,20"/>
<mxCell id="p8b_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1191,200,28"/>
<mxCell id="p8b_tk0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1225,150,55"/>
<mxCell id="p8b_tv0" value="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1225,610,55"/>
<mxCell id="p8b_tk1" value="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1280,150,71"/>
<mxCell id="p8b_tv1" value="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1280,610,71"/>
<mxCell id="p8b_tk2" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1351,150,55"/>
<mxCell id="p8b_tv2" value="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1351,610,55"/>
<mxCell id="p8b_tk3" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1406,150,71"/>
<mxCell id="p8b_tv3" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1406,610,71"/>
<mxCell id="p8b_tk4" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1477,150,55"/>
<mxCell id="p8b_tv4" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1477,610,55"/>
<mxCell id="p8b_tk5" value="append 行／CRLF／三分支" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1532,150,55"/>
<mxCell id="p8b_tv5" value="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1532,610,55"/>
<mxCell id="p8b_tk6" value="初始檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1225,150,40"/>
<mxCell id="p8b_tv6" value="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1225,610,40"/>
<mxCell id="p8b_tk7" value="保護清單／保護模式" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1265,150,40"/>
<mxCell id="p8b_tv7" value="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1265,610,40"/>
<mxCell id="p8b_tk8" value="dev 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1305,150,40"/>
<mxCell id="p8b_tv8" value="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1305,610,40"/>
<mxCell id="p8b_tk9" value="gen／mod?／import" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1345,150,71"/>
<mxCell id="p8b_tv9" value="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1345,610,71"/>
<mxCell id="p8b_tk10" value="CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1416,150,55"/>
<mxCell id="p8b_tv10" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1416,610,55"/>
<mxCell id="p8b_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1471,150,55"/>
<mxCell id="p8b_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1471,610,55"/>
</diagram>
<diagram id="v1p8bccc" name="流程 v2：remove（2）寫入段">
<mxCell id="title" value="流程 v2：remove（2）apply 寫入段（§2、§5；v2.2 C／E、v2.3 §1／§5、v2.5 §3／§11）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="vC2" value="remove &amp;lt;repo&amp;gt;（2）寫入段（承「remove（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 問 append 行（找行 → 命中幾處？）→ 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1128"/>
<mxCell id="vC2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="1556,5,30,20"/>
<mxCell id="m9e" value="來自「remove（1）」頁：apply 檢查通過（非 dry-run）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="vC2" geo="610,36,300,58"/>
<mxCell id="m9l" value="建進度日誌（.vendor_kit/.tmp.remove.&amp;lt;id&amp;gt;.toml；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,114,400,48"/>
<mxCell id="m9l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,104,30,20"/>
<mxCell id="m9lf" value="＋.vendor_kit/.tmp.remove.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,117,360,42"/>
<mxCell id="m9h" value="metadata 有 append 過的行？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC2" geo="590,182,300,81"/>
<mxCell id="m9h_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="866,172,30,20"/>
<mxCell id="m9q" value="有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC2" geo="590,283,300,112"/>
<mxCell id="m9q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="866,273,30,20"/>
<mxCell id="m9s" value="是：找上次插入的行（CRLF／LF 視為相同、其餘精確）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC2" geo="640,415,200,48"/>
<mxCell id="m9s_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="816,405,30,20"/>
<mxCell id="m9mn" value="找行（v2.3 §1）：CRLF／LF 視為相同、其餘精確；唯一命中 → 刪；零命中 → 不刪印清單；多處 → 保留並 warn（Q13）" style="fillColor=#ffffff;strokeColor=#999999" parent="vC2" geo="1220,418,360,42"/>
<mxCell id="m9z" value="零命中：不刪、印清單" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC2" geo="560,495,70,57"/>
<mxCell id="m9m" value="命中幾處？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vC2" geo="670,483,140,81"/>
<mxCell id="m9m_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="786,473,30,20"/>
<mxCell id="m9d" value="唯一：刪那幾行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC2" geo="860,504,100,40"/>
<mxCell id="m9f" value="初始檔（只移除我們 append 的行；其餘不動；永不刪檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,504,360,40"/>
<mxCell id="m9w" value="多處：保留＋warn" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vC2" geo="670,604,140,40"/>
<mxCell id="m9w_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="786,594,30,20"/>
<mxCell id="m10a" value="刪 baseline/&amp;lt;repo&amp;gt;/（含 metadata）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="530,664,400,40"/>
<mxCell id="m10a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="906,654,30,20"/>
<mxCell id="m10af" value="－baseline/&amp;lt;repo&amp;gt;/（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,664,360,40"/>
<mxCell id="m10b" value="刪 cache/&amp;lt;repo&amp;gt;/" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,724,400,40"/>
<mxCell id="m10b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,714,30,20"/>
<mxCell id="m10bf" value="－cache/&amp;lt;repo&amp;gt;/（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,724,360,40"/>
<mxCell id="m10c" value="刪 gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,784,400,40"/>
<mxCell id="m10c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,774,30,20"/>
<mxCell id="m10cf" value="－gen/&amp;lt;repo&amp;gt;.stamp（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,784,360,40"/>
<mxCell id="m10d" value="重生 gen/tools.just（去掉該工具所有 mod? 行）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,844,400,40"/>
<mxCell id="m10d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,834,30,20"/>
<mxCell id="m10df" value="gen/tools.just（不進 git；mod? 行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,844,360,40"/>
<mxCell id="m10e" value="最後刪 version.toml 該工具那一行" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,904,400,40"/>
<mxCell id="m10e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,894,30,20"/>
<mxCell id="m10ef" value="－version.toml &amp;lt;repo&amp;gt; 行（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vC2" geo="1220,904,360,40"/>
<mxCell id="m10x" value="失敗 → 1：明列已完成／未完成" style="fillColor=#f8cecc;strokeColor=#000000" parent="vC2" geo="20,964,220,58"/>
<mxCell id="m10x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="216,954,30,20"/>
<mxCell id="m10g" value="刪進度日誌（最後一步）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vC2" geo="560,973,400,40"/>
<mxCell id="m10g_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vC2" geo="936,963,30,20"/>
<mxCell id="m11" value="0：印「以下初始檔保留，若不需要請 git rm：…」" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vC2" geo="20,1042,220,80"/>
<mxCell id="me11e" edge="1" source="m9e" target="m9l"/>
<mxCell id="me11f" value="寫" edge="1" source="m9l" target="m9lf"/>
<mxCell id="me11h" edge="1" source="m9l" target="m9h"/>
<mxCell id="me11hn" value="無" edge="1" source="m9h" target="m10a"/>
<mxCell id="me11q" value="有" edge="1" source="m9h" target="m9q"/>
<mxCell id="me12n" value="否" edge="1" source="m9q" target="m10a"/>
<mxCell id="me12y" value="是" edge="1" source="m9q" target="m9s"/>
<mxCell id="me12m" edge="1" source="m9s" target="m9m"/>
<mxCell id="me13z" value="零" edge="1" source="m9m" target="m9z"/>
<mxCell id="me13d" value="唯一" edge="1" source="m9m" target="m9d"/>
<mxCell id="me13w" value="多處" edge="1" source="m9m" target="m9w"/>
<mxCell id="me13f" value="寫" edge="1" source="m9d" target="m9f"/>
<mxCell id="me14z" edge="1" source="m9z" target="m10a"/>
<mxCell id="me14w" edge="1" source="m9w" target="m10a"/>
<mxCell id="me14d" edge="1" source="m9d" target="m10a"/>
<mxCell id="me15a" value="刪" edge="1" source="m10a" target="m10af"/>
<mxCell id="me15b" edge="1" source="m10a" target="m10b"/>
<mxCell id="me15bf" value="刪" edge="1" source="m10b" target="m10bf"/>
<mxCell id="me15c" edge="1" source="m10b" target="m10c"/>
<mxCell id="me15cf" value="刪" edge="1" source="m10c" target="m10cf"/>
<mxCell id="me15d" edge="1" source="m10c" target="m10d"/>
<mxCell id="me15df" value="寫" edge="1" source="m10d" target="m10df"/>
<mxCell id="me15e" edge="1" source="m10d" target="m10e"/>
<mxCell id="me15ef" value="刪" edge="1" source="m10e" target="m10ef"/>
<mxCell id="me16" value="成功" edge="1" source="m10e" target="m10g"/>
<mxCell id="me16x" value="失敗" edge="1" source="m10e" target="m10x"/>
<mxCell id="me17" edge="1" source="m10g" target="m11"/>
<mxCell id="p8b2_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1285,200,60"/>
<mxCell id="p8b2_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1285,140,64"/>
<mxCell id="p8b2_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1293,140,44"/>
<mxCell id="p8b2_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1287,190,56"/>
<mxCell id="p8b2_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1287,210,56"/>
<mxCell id="p8b2_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1295,88,40"/>
<mxCell id="p8b2_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1295,170,40"/>
<mxCell id="p8b2_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1285,300,60"/>
<mxCell id="p8b2_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1353,200,36"/>
<mxCell id="p8b2_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1353,120,36"/>
<mxCell id="p8b2_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="400,1353,190,36"/>
<mxCell id="p8b2_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="610,1353,170,36"/>
<mxCell id="p8b2_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,1353,170,36"/>
<mxCell id="p8b2_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="990,1353,200,36"/>
<mxCell id="p8b2_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1166,1343,30,20"/>
<mxCell id="p8b2_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1391,200,28"/>
<mxCell id="p8b2_tk0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1425,150,55"/>
<mxCell id="p8b2_tv0" value="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1425,610,55"/>
<mxCell id="p8b2_tk1" value="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1480,150,71"/>
<mxCell id="p8b2_tv1" value="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1480,610,71"/>
<mxCell id="p8b2_tk2" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1551,150,55"/>
<mxCell id="p8b2_tv2" value="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1551,610,55"/>
<mxCell id="p8b2_tk3" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1606,150,71"/>
<mxCell id="p8b2_tv3" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1606,610,71"/>
<mxCell id="p8b2_tk4" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1677,150,55"/>
<mxCell id="p8b2_tv4" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1677,610,55"/>
<mxCell id="p8b2_tk5" value="append 行／CRLF／三分支" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1732,150,55"/>
<mxCell id="p8b2_tv5" value="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1732,610,55"/>
<mxCell id="p8b2_tk6" value="初始檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1425,150,40"/>
<mxCell id="p8b2_tv6" value="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1425,610,40"/>
<mxCell id="p8b2_tk7" value="保護清單／保護模式" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1465,150,40"/>
<mxCell id="p8b2_tv7" value="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1465,610,40"/>
<mxCell id="p8b2_tk8" value="dev 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1505,150,40"/>
<mxCell id="p8b2_tv8" value="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1505,610,40"/>
<mxCell id="p8b2_tk9" value="gen／mod?／import" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1545,150,71"/>
<mxCell id="p8b2_tv9" value="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1545,610,71"/>
<mxCell id="p8b2_tk10" value="CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1616,150,55"/>
<mxCell id="p8b2_tv10" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1616,610,55"/>
<mxCell id="p8b2_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1671,150,55"/>
<mxCell id="p8b2_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1671,610,55"/>
</diagram>
<diagram id="v1p8bc" name="流程 v2：uninstall（1）resolve → apply 前置">
<mxCell id="title" value="流程 v2：uninstall（1）resolve → apply 前置（§2；v2.2 E、v2.3 §6、v2.5 §3／§10）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="vD" value="uninstall（1）：全部拆掉（install 的反向；bootstrap.sh 的反向也是它）= resolve（預檢 → hash → 保護清單 → 計畫 → 詢問清單 → 指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；寫入段見「uninstall（2）」頁；不 rm -rf .vendor_kit/" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,941"/>
<mxCell id="vD_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="1556,5,30,20"/>
<mxCell id="x0" value="just vendor_kit uninstall（-y、--dry-run）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vD" geo="20,36,220,80"/>
<mxCell id="x1" value="docker run &amp;lt;引擎&amp;gt; resolve uninstall（不經 docker create/cp）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD" geo="260,52,280,48"/>
<mxCell id="x1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="516,42,30,20"/>
<mxCell id="x2x" value="否 → 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vD" geo="20,136,220,80"/>
<mxCell id="x2x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="216,126,30,20"/>
<mxCell id="x2" value="預檢全部工具通過？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD" geo="560,151,250,50"/>
<mxCell id="x2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="786,141,30,20"/>
<mxCell id="x2b" value="是：算每個自產檔的 hash（薄殼、version.toml、gen/、cache/、baseline/；不動任何東西）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,236,400,48"/>
<mxCell id="x2b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,226,30,20"/>
<mxCell id="x2bb" value="分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,304,400,48"/>
<mxCell id="x2bb_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,294,30,20"/>
<mxCell id="x2r" value="保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="vD" geo="1220,304,360,48"/>
<mxCell id="x2r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="1556,294,30,20"/>
<mxCell id="x2c" value="產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,372,400,40"/>
<mxCell id="x2c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,362,30,20"/>
<mxCell id="x2d" value="產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 三行" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,432,400,48"/>
<mxCell id="x2d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,422,30,20"/>
<mxCell id="x2e" value="產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）→ 計畫＋詢問清單＋指紋以 stdout 回啟動器" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,500,400,48"/>
<mxCell id="x2e_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,490,30,20"/>
<mxCell id="x1b" value="docker run &amp;lt;引擎&amp;gt; apply uninstall（--dry-run 原樣轉發）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD" geo="260,568,280,48"/>
<mxCell id="x1b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="516,558,30,20"/>
<mxCell id="x4a" value="apply：flock 專案目錄（60 秒）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,572,400,40"/>
<mxCell id="x4a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,562,30,20"/>
<mxCell id="x4b" value="重驗指紋" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD" geo="560,645,240,40"/>
<mxCell id="x4b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="776,635,30,20"/>
<mxCell id="x4bx" value="不同 → 1「請重跑」" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vD" geo="820,636,140,58"/>
<mxCell id="x4bx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="936,626,30,20"/>
<mxCell id="x3cx" value="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="vD" geo="20,714,220,80"/>
<mxCell id="x3cx_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="216,704,30,20"/>
<mxCell id="x3c" value="CI 為真（frozen）且需改 tracked 檔？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD" geo="560,714,340,81"/>
<mxCell id="x3c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="876,704,30,20"/>
<mxCell id="x3y" value="是 → 0：只印會刪什麼、會問什麼" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vD" geo="20,815,220,58"/>
<mxCell id="x3y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD" geo="216,805,30,20"/>
<mxCell id="x3" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD" geo="610,819,240,50"/>
<mxCell id="x4z" value="否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌" style="fillColor=none;strokeColor=none" parent="vD" geo="560,893,400,42"/>
<mxCell id="xe1" edge="1" source="x0" target="x1"/>
<mxCell id="xe2" edge="1" source="x1" target="x2"/>
<mxCell id="xe3" value="否" edge="1" source="x2" target="x2x"/>
<mxCell id="xe4" value="是" edge="1" source="x2" target="x2b"/>
<mxCell id="xe4b" edge="1" source="x2b" target="x2bb"/>
<mxCell id="xe4c" edge="1" source="x2bb" target="x2c"/>
<mxCell id="xe4d" edge="1" source="x2c" target="x2d"/>
<mxCell id="xe4e" edge="1" source="x2d" target="x2e"/>
<mxCell id="xe5" edge="1" source="x2e" target="x1b"/>
<mxCell id="xe5b" edge="1" source="x1b" target="x4a"/>
<mxCell id="xe5c" edge="1" source="x4a" target="x4b"/>
<mxCell id="xe5x" edge="1" source="x4b" target="x4bx"/>
<mxCell id="xe5d" edge="1" source="x4b" target="x3c"/>
<mxCell id="xe5e" value="是" edge="1" source="x3c" target="x3cx"/>
<mxCell id="xe5f" value="否" edge="1" source="x3c" target="x3"/>
<mxCell id="xe6" value="是" edge="1" source="x3" target="x3y"/>
<mxCell id="xe7" value="否" edge="1" source="x3" target="x4z"/>
<mxCell id="p8bc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1098,200,60"/>
<mxCell id="p8bc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1098,140,64"/>
<mxCell id="p8bc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1106,140,44"/>
<mxCell id="p8bc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1100,190,56"/>
<mxCell id="p8bc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1100,210,56"/>
<mxCell id="p8bc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1108,88,40"/>
<mxCell id="p8bc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1108,170,40"/>
<mxCell id="p8bc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1098,300,60"/>
<mxCell id="p8bc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1166,120,36"/>
<mxCell id="p8bc_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1166,150,36"/>
<mxCell id="p8bc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1166,190,36"/>
<mxCell id="p8bc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1166,170,36"/>
<mxCell id="p8bc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1166,170,36"/>
<mxCell id="p8bc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="940,1166,200,36"/>
<mxCell id="p8bc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1116,1156,30,20"/>
<mxCell id="p8bc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1204,200,28"/>
<mxCell id="p8bc_tk0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1238,150,55"/>
<mxCell id="p8bc_tv0" value="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1238,610,55"/>
<mxCell id="p8bc_tk1" value="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1293,150,71"/>
<mxCell id="p8bc_tv1" value="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1293,610,71"/>
<mxCell id="p8bc_tk2" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1364,150,55"/>
<mxCell id="p8bc_tv2" value="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1364,610,55"/>
<mxCell id="p8bc_tk3" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1419,150,71"/>
<mxCell id="p8bc_tv3" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1419,610,71"/>
<mxCell id="p8bc_tk4" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1490,150,55"/>
<mxCell id="p8bc_tv4" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1490,610,55"/>
<mxCell id="p8bc_tk5" value="append 行／CRLF／三分支" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1545,150,55"/>
<mxCell id="p8bc_tv5" value="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1545,610,55"/>
<mxCell id="p8bc_tk6" value="初始檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1238,150,40"/>
<mxCell id="p8bc_tv6" value="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1238,610,40"/>
<mxCell id="p8bc_tk7" value="保護清單／保護模式" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1278,150,40"/>
<mxCell id="p8bc_tv7" value="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1278,610,40"/>
<mxCell id="p8bc_tk8" value="dev 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1318,150,40"/>
<mxCell id="p8bc_tv8" value="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1318,610,40"/>
<mxCell id="p8bc_tk9" value="gen／mod?／import" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1358,150,71"/>
<mxCell id="p8bc_tv9" value="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1358,610,71"/>
<mxCell id="p8bc_tk10" value="CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1429,150,55"/>
<mxCell id="p8bc_tv10" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1429,610,55"/>
<mxCell id="p8bc_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1484,150,55"/>
<mxCell id="p8bc_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1484,610,55"/>
</diagram>
<diagram id="v1p8bcc" name="流程 v2：uninstall（2）寫入段">
<mxCell id="title" value="流程 v2：uninstall（2）apply 寫入段（§2；v2.2 E、v2.3 §6、v2.5 §3／§10、v2.6 Q22 補、v2.8 §1）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,77"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,97,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,97,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,97,400,28"/>
<mxCell id="hdr3" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,97,220,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1240,97,360,28"/>
<mxCell id="vD2" value="uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（含 baseline/ 根檔，v2.8 §1）→ justfile 那行、.dockerignore 行問後逐行刪（只刪仍相同的）→ 刪日誌 → 空才 rmdir" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,141,1600,1673"/>
<mxCell id="vD2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="1556,5,30,20"/>
<mxCell id="x4e" value="來自「uninstall（1）」頁：apply 檢查通過（非 dry-run）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="vD2" geo="610,36,300,58"/>
<mxCell id="x4l" value="建進度日誌（.vendor_kit/.tmp.uninstall.&amp;lt;id&amp;gt;.toml；第一個寫入前）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,114,400,48"/>
<mxCell id="x4l_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,104,30,20"/>
<mxCell id="x4lf" value="＋.vendor_kit/.tmp.uninstall.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,117,360,42"/>
<mxCell id="x4x" value="任一失敗 → 1 中止，列出已完成部分" style="fillColor=#f8cecc;strokeColor=#000000" parent="vD2" geo="20,182,220,58"/>
<mxCell id="x4x_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="216,172,30,20"/>
<mxCell id="x4" value="逐工具 remove（保護模式；步驟同「remove（2）」頁）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,191,400,40"/>
<mxCell id="x4_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,181,30,20"/>
<mxCell id="x5a" value="全部成功：刪薄殼四檔（hash 相符者）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,287,400,40"/>
<mxCell id="x5a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,277,30,20"/>
<mxCell id="x5af" value="－.vendor_kit/ 薄殼四檔（保護清單內的保留）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,260,360,94"/>
<mxCell id="x5af_0" value=".gitignore" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5af" geo="8,26,169,26"/>
<mxCell id="x5af_1" value="entry.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5af" geo="183,26,169,26"/>
<mxCell id="x5af_2" value="vendor.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5af" geo="8,58,169,26"/>
<mxCell id="x5af_3" value="ci/check.sh" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5af" geo="183,58,169,26"/>
<mxCell id="x5b" value="刪 version.toml（hash 相符者）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,374,400,40"/>
<mxCell id="x5b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,364,30,20"/>
<mxCell id="x5bf" value="－version.toml（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,374,360,40"/>
<mxCell id="x5c" value="刪 version.local.toml（有的話；hash 相符者）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,434,400,40"/>
<mxCell id="x5c_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,424,30,20"/>
<mxCell id="x5cf" value="－version.local.toml（不進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,434,360,40"/>
<mxCell id="x5d" value="刪 gen/ 與 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,517,400,48"/>
<mxCell id="x5d_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,507,30,20"/>
<mxCell id="x5df" value="－gen/ 兩檔（不進 git）、baseline/ 根檔（進 git）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,494,360,94"/>
<mxCell id="x5df_0" value="gen/.stamp" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5df" geo="8,26,140,26"/>
<mxCell id="x5df_1" value="gen/tools.just" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5df" geo="154,26,198,26"/>
<mxCell id="x5df_2" value="baseline/.gitkeep" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5df" geo="8,58,140,26"/>
<mxCell id="x5df_3" value="baseline/.vendor_kit.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="x5df" geo="154,58,198,26"/>
<mxCell id="x5dd" value="刪已空的子目錄 baseline/（gen/、cache/、ci/ 亦同；rmdir，不 rm -rf）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,608,400,48"/>
<mxCell id="x5dd_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,598,30,20"/>
<mxCell id="x6" value="根 justfile 有我們寫的那一行（完全相同）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="700,676,260,112"/>
<mxCell id="x5r" value="初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="vD2" geo="1220,700,360,63"/>
<mxCell id="x5r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="1556,690,30,20"/>
<mxCell id="x8" value="無／否：印指示（請自行移除 import 那行）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD2" geo="560,828,100,73"/>
<mxCell id="x7" value="有 → 問「要刪這一行嗎」同意？（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="700,808,260,112"/>
<mxCell id="x7_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,798,30,20"/>
<mxCell id="x7y" value="是：只刪那一行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD2" geo="760,941,140,40"/>
<mxCell id="x7f" value="justfile（少一行：import &#x27;.vendor_kit/entry.just&#x27;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,940,360,42"/>
<mxCell id="x9a" value="根 .dockerignore 存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="680,1002,260,81"/>
<mxCell id="x9a_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="916,992,30,20"/>
<mxCell id="x9b" value="有 → 逐行比對：仍有與紀錄原文相同的行？（CRLF／LF 等價）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="680,1103,260,143"/>
<mxCell id="x9b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="916,1093,30,20"/>
<mxCell id="x9r" value="append 行逐行比對（§4.3、v2.9 §5）：對紀錄的每一行 —— 仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="vD2" geo="1220,1143,360,63"/>
<mxCell id="x9r_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="1556,1133,30,20"/>
<mxCell id="x9q" value="有 → 問「要刪這幾行嗎」同意？（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="680,1266,260,112"/>
<mxCell id="x9q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="916,1256,30,20"/>
<mxCell id="x9z" value="無／否：不動 .dockerignore" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD2" geo="560,1398,110,48"/>
<mxCell id="x9z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="646,1388,30,20"/>
<mxCell id="x9y" value="是：逐行只刪仍相同的行；不同／缺的行跳過 warn" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="vD2" geo="730,1398,230,48"/>
<mxCell id="x9y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,1388,30,20"/>
<mxCell id="x9f" value=".dockerignore（只少仍相同的那幾行；其餘不動）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="vD2" geo="1220,1402,360,40"/>
<mxCell id="x9f_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="1556,1392,30,20"/>
<mxCell id="x5z" value="刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,1466,400,40"/>
<mxCell id="x5z_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,1456,30,20"/>
<mxCell id="x5n" value="否 → 0：保留目錄與保護清單內的檔並回報；印摘要" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vD2" geo="20,1526,220,80"/>
<mxCell id="x5n_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="216,1516,30,20"/>
<mxCell id="x5q" value=".vendor_kit/ 已空？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="vD2" geo="560,1526,205,81"/>
<mxCell id="x5q_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="741,1516,30,20"/>
<mxCell id="x5y" value="0：印摘要" style="fillColor=#d5e8d4;strokeColor=#000000" parent="vD2" geo="20,1627,220,40"/>
<mxCell id="x5y_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="216,1617,30,20"/>
<mxCell id="x5t" value="是：刪空目錄（rmdir；不 rm -rf）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="vD2" geo="560,1627,400,40"/>
<mxCell id="x5t_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="vD2" geo="936,1617,30,20"/>
<mxCell id="xe7" edge="1" source="x4e" target="x4l"/>
<mxCell id="xe7f" value="寫" edge="1" source="x4l" target="x4lf"/>
<mxCell id="xe8" edge="1" source="x4l" target="x4"/>
<mxCell id="xe9" value="失敗" edge="1" source="x4" target="x4x"/>
<mxCell id="xe10" edge="1" source="x4" target="x5a"/>
<mxCell id="xe10f" value="刪" edge="1" source="x5a" target="x5af"/>
<mxCell id="xe10b" edge="1" source="x5a" target="x5b"/>
<mxCell id="xe10bf" value="刪" edge="1" source="x5b" target="x5bf"/>
<mxCell id="xe10c" edge="1" source="x5b" target="x5c"/>
<mxCell id="xe10cf" value="刪" edge="1" source="x5c" target="x5cf"/>
<mxCell id="xe10d" edge="1" source="x5c" target="x5d"/>
<mxCell id="xe10df" value="刪" edge="1" source="x5d" target="x5df"/>
<mxCell id="xe10e" edge="1" source="x5d" target="x5dd"/>
<mxCell id="xe12" edge="1" source="x5dd" target="x6"/>
<mxCell id="xe13" value="無" edge="1" source="x6" target="x8"/>
<mxCell id="xe14" value="有" edge="1" source="x6" target="x7"/>
<mxCell id="xe14n" value="否" edge="1" source="x7" target="x8"/>
<mxCell id="xe14y" value="是" edge="1" source="x7" target="x7y"/>
<mxCell id="xe15" value="寫" edge="1" source="x7y" target="x7f"/>
<mxCell id="xe16z" edge="1" source="x8" target="x9a"/>
<mxCell id="xe16y" edge="1" source="x7y" target="x9a"/>
<mxCell id="xe16a" value="有" edge="1" source="x9a" target="x9b"/>
<mxCell id="xe16b" value="有" edge="1" source="x9b" target="x9q"/>
<mxCell id="xe16q" value="是" edge="1" source="x9q" target="x9y"/>
<mxCell id="xe16f" value="寫" edge="1" source="x9y" target="x9f"/>
<mxCell id="xe16an" value="無" edge="1" source="x9a" target="x9z"/>
<mxCell id="xe16bn" value="無" edge="1" source="x9b" target="x9z"/>
<mxCell id="xe16qn" value="否" edge="1" source="x9q" target="x9z"/>
<mxCell id="xe16v" edge="1" source="x9y" target="x5z"/>
<mxCell id="xe16w" edge="1" source="x9z" target="x5z"/>
<mxCell id="xe17" edge="1" source="x5z" target="x5q"/>
<mxCell id="xe18" value="否" edge="1" source="x5q" target="x5n"/>
<mxCell id="xe19" value="是" edge="1" source="x5q" target="x5t"/>
<mxCell id="xe20" edge="1" source="x5t" target="x5y"/>
<mxCell id="p8bcc_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1830,200,60"/>
<mxCell id="p8bcc_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1830,140,64"/>
<mxCell id="p8bcc_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1838,140,44"/>
<mxCell id="p8bcc_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1832,190,56"/>
<mxCell id="p8bcc_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1832,210,56"/>
<mxCell id="p8bcc_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1840,88,40"/>
<mxCell id="p8bcc_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1840,170,40"/>
<mxCell id="p8bcc_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1830,300,60"/>
<mxCell id="p8bcc_lgx_entry" value="虛線橢圓：跨頁入口" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="40,1898,200,36"/>
<mxCell id="p8bcc_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="260,1898,120,36"/>
<mxCell id="p8bcc_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="400,1898,150,36"/>
<mxCell id="p8bcc_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="570,1898,190,36"/>
<mxCell id="p8bcc_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="780,1898,170,36"/>
<mxCell id="p8bcc_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,1898,170,36"/>
<mxCell id="p8bcc_lgx_v2" value="右上綠標 v2：與 v1 不同處" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1160,1898,200,36"/>
<mxCell id="p8bcc_lgx_v2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" geo="1336,1888,30,20"/>
<mxCell id="p8bcc_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1936,200,28"/>
<mxCell id="p8bcc_tk0" value="remove" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1970,150,55"/>
<mxCell id="p8bcc_tv0" value="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1970,610,55"/>
<mxCell id="p8bcc_tk1" value="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2025,150,71"/>
<mxCell id="p8bcc_tv1" value="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2025,610,71"/>
<mxCell id="p8bcc_tk2" value="resolve／apply／--dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2096,150,55"/>
<mxCell id="p8bcc_tv2" value="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2096,610,55"/>
<mxCell id="p8bcc_tk3" value="flock／指紋／進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2151,150,71"/>
<mxCell id="p8bcc_tv3" value="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2151,610,71"/>
<mxCell id="p8bcc_tk4" value="baseline／metadata" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2222,150,55"/>
<mxCell id="p8bcc_tv4" value="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2222,610,55"/>
<mxCell id="p8bcc_tk5" value="append 行／CRLF／三分支" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2277,150,55"/>
<mxCell id="p8bcc_tv5" value="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2277,610,55"/>
<mxCell id="p8bcc_tk6" value="初始檔" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1970,150,40"/>
<mxCell id="p8bcc_tv6" value="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1970,610,40"/>
<mxCell id="p8bcc_tk7" value="保護清單／保護模式" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2010,150,40"/>
<mxCell id="p8bcc_tv7" value="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2010,610,40"/>
<mxCell id="p8bcc_tk8" value="dev 覆寫" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2050,150,40"/>
<mxCell id="p8bcc_tv8" value="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2050,610,40"/>
<mxCell id="p8bcc_tk9" value="gen／mod?／import" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2090,150,71"/>
<mxCell id="p8bcc_tv9" value="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2090,610,71"/>
<mxCell id="p8bcc_tk10" value="CI 為真／frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2161,150,55"/>
<mxCell id="p8bcc_tv10" value="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2161,610,55"/>
<mxCell id="p8bcc_tk11" value="結束狀態 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2216,150,55"/>
<mxCell id="p8bcc_tv11" value="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2216,610,55"/>
</diagram>
<diagram id="v1p9" name="流程 v2：prune">
<mxCell id="title" value="流程 v2：prune ── 依 label 清未引用的 docker 資源（interface_spec §1.2、§3.3 keep、§4.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.4-10、grilling 9 修正／補充、Q24、Q25、interface_spec A1、v2.7-7）：prune 第一版做；所有 vendor_kit 建的 docker 資源帶 label；prune 依 label 掃四類資源、刪 version.toml／local 未引用者；docker 指令由啟動器執行（不掛 socket）；image 只刪帶 label 且本專案未引用者（共享 daemon 提醒）；活躍的 .tmp.* 只列出不刪、不視為未完成交易；prune 自己的 apply 也走進度日誌（建 .tmp.prune.&amp;lt;id&amp;gt;.toml → 清理 → 刪日誌；v2.9-6）；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run（無 -n）。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,132"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,152,200,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="260,152,300,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,152,340,28"/>
<mxCell id="hdr3" value="docker daemon" style="fillColor=#e6e6e6;strokeColor=#999999" geo="940,152,300,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1260,152,330,28"/>
<mxCell id="bP" value="prune [-y] [--dry-run]：引擎 resolve 算保留清單（不寫）→ 啟動器依 label 列四類資源 → 差集 → 問後逐類刪 → 引擎 apply（flock → 重驗指紋 → 建 .tmp.prune.&amp;lt;id&amp;gt;.toml → 清 .tmp.dist.* → 清殘留 .tmp.* → 刪日誌）→ 摘要" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,196,1590,1667"/>
<mxCell id="bP_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bP" geo="1546,5,30,20"/>
<mxCell id="q0" value="just vendor_kit prune（-y／--dry-run）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bP" geo="20,36,200,80"/>
<mxCell id="q1" value="docker run &amp;lt;引擎&amp;gt; resolve prune（永不 -t）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,55,300,42"/>
<mxCell id="q2" value="resolve（不寫任何檔）：讀 version.toml、version.local.toml" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,55,340,42"/>
<mxCell id="q3" value="算保留清單 keep：引擎 ref、[tools] 每個工具 ref、local 覆寫的 vendor_kit &amp;lt;tag&amp;gt;" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,162,340,42"/>
<mxCell id="q3f" value="只讀（不寫）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,136,330,94"/>
<mxCell id="q3f_0" value="version.toml（引擎 ref、[tools]）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="q3f" geo="8,26,314,26"/>
<mxCell id="q3f_1" value="version.local.toml（vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="q3f" geo="8,58,314,26"/>
<mxCell id="q4" value="偵測活躍（未恢復）的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml → 只列出、印 6-33（不刪、不視為未完成交易）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,250,340,42"/>
<mxCell id="q4f" value=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（活躍交易：保留）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,250,330,42"/>
<mxCell id="q5" value="stdout vk-resolve/1：keep|&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;…、fingerprint、apply|yes、end|N" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,312,340,42"/>
<mxCell id="q6" value="收完整份、驗首尾與筆數（不合 → 1 + 6-30，不動 docker）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,374,300,42"/>
<mxCell id="q7" value="docker container／image／network／volume ls --filter label=io.github.&amp;lt;org&amp;gt;.vendor_kit=1" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,452,300,57"/>
<mxCell id="q7d" value="列出帶 label 的四類資源：容器、image、network、volume" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="920,459,300,42"/>
<mxCell id="q7n" value="所有 vendor_kit 建的資源都帶 label（容器／network／volume 另加 .project=&amp;lt;專案根&amp;gt;）；不建 network／volume，若意外建立也要能刪（驗收 §7.4-23：故意留一個帶 label 的 network／volume，prune 後必須消失）" style="fillColor=#ffffff;strokeColor=#999999" parent="bP" geo="1240,436,330,88"/>
<mxCell id="q8" value="差集 = 候選 − keep（image：帶 label 且本專案未引用；容器／network／volume：帶 label 者）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,552,300,57"/>
<mxCell id="q8n" value="共享 daemon 提醒：image 沒有 .project label，其他專案是否引用同一 image 不可知 → 只刪帶 label 且本專案未引用者；先 --dry-run 看；被刪的 image 下次 sync 會再拉" style="fillColor=#ffffff;strokeColor=#999999" parent="bP" geo="920,544,300,73"/>
<mxCell id="q9y" value="是 → 0：只列出會刪什麼（零刪除）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bP" geo="20,637,200,58"/>
<mxCell id="q9" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bP" geo="290,641,200,50"/>
<mxCell id="q10n" value="否 → 0：不刪、印清單" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bP" geo="20,771,200,40"/>
<mxCell id="q10" value="問 6-32「要刪除以上 vendor_kit 資源嗎？」（-y 免問）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bP" geo="240,735,300,112"/>
<mxCell id="q11l" value="是 ↓ 對四類資源逐類刪（失敗的記下、續刪其餘）" style="fillColor=none;strokeColor=none" parent="bP" geo="240,867,300,26"/>
<mxCell id="q11a" value="docker rm &amp;lt;差集內的容器&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,913,300,40"/>
<mxCell id="q11ad" value="容器被刪" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="920,913,300,40"/>
<mxCell id="q11b" value="docker image rm &amp;lt;差集內的 image&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,973,300,40"/>
<mxCell id="q11bd" value="image 被刪（keep 內的 image 保留）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="920,973,300,40"/>
<mxCell id="q11c" value="docker network rm &amp;lt;差集內的 network&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,1033,300,40"/>
<mxCell id="q11cd" value="network 被刪" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="920,1033,300,40"/>
<mxCell id="q11d" value="docker volume rm &amp;lt;差集內的 volume&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,1093,300,40"/>
<mxCell id="q11dd" value="volume 被刪" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="920,1093,300,40"/>
<mxCell id="q12" value="docker run &amp;lt;引擎&amp;gt; apply prune" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bP" geo="240,1154,300,40"/>
<mxCell id="q12a" value="apply prune：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1153,340,42"/>
<mxCell id="q12b" value="重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1215,340,42"/>
<mxCell id="q12j" value="建進度日誌 .tmp.prune.&amp;lt;id&amp;gt;.toml（第一個寫入前；state=in-progress、done／pending）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1277,340,42"/>
<mxCell id="q12jf" value="＋.vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（prune 自己的交易日誌）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,1277,330,42"/>
<mxCell id="q12c" value="刪失效的啟動器暫存 .tmp.dist.*／（trap 沒清到的）→ 日誌 done" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1339,340,42"/>
<mxCell id="q12cf" value=".vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;/（刪）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,1340,330,40"/>
<mxCell id="q12d" value="刪已完成交易殘留的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（活躍的不刪，只列出）→ 日誌 done" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1401,340,42"/>
<mxCell id="q12df" value=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（殘留：刪；活躍：保留）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,1401,330,42"/>
<mxCell id="q12k" value="刪進度日誌 .tmp.prune.&amp;lt;id&amp;gt;.toml（最後一步）= 交易完成" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bP" geo="560,1463,340,42"/>
<mxCell id="q12kf" value="－.vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（刪）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bP" geo="1240,1464,330,40"/>
<mxCell id="q13x" value="是 → 1：摘要全列，失敗的標出" style="fillColor=#f8cecc;strokeColor=#000000" parent="bP" geo="20,1525,200,58"/>
<mxCell id="q13" value="有刪除失敗？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bP" geo="290,1529,200,50"/>
<mxCell id="q14" value="否 → 0：印刪了什麼、保留什麼（含原因）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bP" geo="20,1603,200,58"/>
<mxCell id="qe0" edge="1" source="q0" target="q1"/>
<mxCell id="qe1" edge="1" source="q1" target="q2"/>
<mxCell id="qe2" edge="1" source="q2" target="q3"/>
<mxCell id="qe3" value="讀" edge="1" source="q3" target="q3f"/>
<mxCell id="qe4" edge="1" source="q3" target="q4"/>
<mxCell id="qe5" edge="1" source="q4" target="q4f"/>
<mxCell id="qe6" edge="1" source="q4" target="q5"/>
<mxCell id="qe7" edge="1" source="q5" target="q6"/>
<mxCell id="qe8" edge="1" source="q6" target="q7"/>
<mxCell id="qe9" value="ls" edge="1" source="q7" target="q7d"/>
<mxCell id="qe10" edge="1" source="q7" target="q8"/>
<mxCell id="qe11" edge="1" source="q8" target="q9"/>
<mxCell id="qe12" value="是" edge="1" source="q9" target="q9y"/>
<mxCell id="qe13" value="否" edge="1" source="q9" target="q10"/>
<mxCell id="qe14" value="否" edge="1" source="q10" target="q10n"/>
<mxCell id="qe15" edge="1" source="q10" target="q11l"/>
<mxCell id="qe15a" edge="1" source="q11l" target="q11a"/>
<mxCell id="qe16a" value="rm" edge="1" source="q11a" target="q11ad"/>
<mxCell id="qe16b" edge="1" source="q11a" target="q11b"/>
<mxCell id="qe16c" value="rm" edge="1" source="q11b" target="q11bd"/>
<mxCell id="qe16d" edge="1" source="q11b" target="q11c"/>
<mxCell id="qe16e" value="rm" edge="1" source="q11c" target="q11cd"/>
<mxCell id="qe16f" edge="1" source="q11c" target="q11d"/>
<mxCell id="qe16g" value="rm" edge="1" source="q11d" target="q11dd"/>
<mxCell id="qe17" edge="1" source="q11d" target="q12"/>
<mxCell id="qe18" edge="1" source="q12" target="q12a"/>
<mxCell id="qe18a" edge="1" source="q12a" target="q12b"/>
<mxCell id="qe18j" edge="1" source="q12b" target="q12j"/>
<mxCell id="qe19j" value="建" edge="1" source="q12j" target="q12jf"/>
<mxCell id="qe18b" edge="1" source="q12j" target="q12c"/>
<mxCell id="qe19" value="刪" edge="1" source="q12c" target="q12cf"/>
<mxCell id="qe18c" edge="1" source="q12c" target="q12d"/>
<mxCell id="qe19d" value="刪" edge="1" source="q12d" target="q12df"/>
<mxCell id="qe18k" edge="1" source="q12d" target="q12k"/>
<mxCell id="qe19k" value="刪" edge="1" source="q12k" target="q12kf"/>
<mxCell id="qe20" edge="1" source="q12k" target="q13"/>
<mxCell id="qe21" value="是" edge="1" source="q13" target="q13x"/>
<mxCell id="qe22" value="否" edge="1" source="q13" target="q14"/>
<mxCell id="p9_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1879,200,60"/>
<mxCell id="p9_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1879,140,64"/>
<mxCell id="p9_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1887,140,44"/>
<mxCell id="p9_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1881,190,56"/>
<mxCell id="p9_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1881,210,56"/>
<mxCell id="p9_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1889,88,40"/>
<mxCell id="p9_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1889,170,40"/>
<mxCell id="p9_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1879,280,60"/>
<mxCell id="p9_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1947,120,36"/>
<mxCell id="p9_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="180,1947,190,36"/>
<mxCell id="p9_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="390,1947,170,36"/>
<mxCell id="p9_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1985,200,28"/>
<mxCell id="p9_tk0" value="prune" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2019,150,55"/>
<mxCell id="p9_tv0" value="清掉本專案不再引用的 docker 資源與殘留暫存：兩段（resolve prune 出 keep 清單 → 啟動器 docker ls／rm → apply prune 清 .tmp.*）；-y 免問、--dry-run 只列出零刪除（無短形）；結束 0／1／3" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2019,610,55"/>
<mxCell id="p9_tk1" value="keep 清單" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2074,150,40"/>
<mxCell id="p9_tv1" value="vk-resolve 的 keep|&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt; 記錄：version.toml 引擎 ref、[tools] 每個工具 ref、version.local.toml 覆寫的 vendor_kit &amp;lt;tag&amp;gt;；這些 image 不可刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2074,610,40"/>
<mxCell id="p9_tk2" value="docker label" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2114,150,55"/>
<mxCell id="p9_tv2" value="啟動器建的每個 docker 資源都帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1；容器／network／volume 另加 ….project=&amp;lt;專案根絕對路徑&amp;gt;；工具 image 由 Dockerfile.dist 的 LABEL 帶（check.sh --dist 擋缺 LABEL）；引擎 image 另帶 ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2114,610,55"/>
<mxCell id="p9_tk3" value="差集" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2169,150,55"/>
<mxCell id="p9_tv3" value="候選（依 label 列出的四類資源）扣掉 keep：image 只刪「帶 label 且本專案未引用」者；容器／network／volume 依 label 刪；vendor_kit 不建 network／volume，若意外建立也要能刪（驗收 §7.4-23）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2169,610,55"/>
<mxCell id="p9_tk4" value="共享 daemon" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2224,150,40"/>
<mxCell id="p9_tv4" value="一台 docker daemon 被多個專案共用：image 上沒有 .project label，其他專案是否引用同一 image 不可知 → 文件明寫、先 --dry-run 看；被刪的 image 下次 sync 會再拉（已釋出 image 永不刪）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2224,610,40"/>
<mxCell id="p9_tk5" value=".tmp.* 日誌／.tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2264,150,71"/>
<mxCell id="p9_tv5" value="前者 = 修復型 install／remove／uninstall／undev／prune 的進度日誌，未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；prune 自己的交易也建 .tmp.prune.&amp;lt;id&amp;gt;.toml（清理前建、清理後刪；v2.9-6）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2264,610,71"/>
<mxCell id="p9_tk6" value="resolve／apply（兩段）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2019,150,55"/>
<mxCell id="p9_tv6" value="同一動詞分兩段：引擎 resolve 只讀只算，stdout 回 vk-resolve/1 清單（永不 -t）；啟動器先收完整份、驗首尾與筆數才動 docker；apply 拿 flock、重驗指紋後才寫；--dry-run（無短形）= apply 的唯讀預覽" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2019,610,55"/>
<mxCell id="p9_tk7" value="指紋／flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2074,150,55"/>
<mxCell id="p9_tv7" value="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2074,610,55"/>
<mxCell id="p9_tk8" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2129,150,55"/>
<mxCell id="p9_tv8" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2129,610,55"/>
<mxCell id="p9_tk9" value="docker ls／rm（主機命令白名單）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2184,150,55"/>
<mxCell id="p9_tv9" value="啟動器只用白名單命令：docker {container,image,network,volume} ls --filter label=…、docker rm／image rm／network rm／volume rm；逐類資源一次一個命令；不把 docker socket 掛進引擎（引擎不碰 daemon）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2184,610,55"/>
<mxCell id="p9_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2239,150,71"/>
<mxCell id="p9_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2239,610,71"/>
</diagram>
<diagram id="v1p10" name="流程 v2：update">
<mxCell id="title" value="流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q11、Q27、v2.6-5、v2.7-8、v2.8-7、interface_spec §1.2 update）：無憑證時不支援需認證的版本列舉，該工具直接記失敗 1 + 6-3（不進 SemVer 解析；需人動作 → 橙），其他工具照查再彙總；token 只在 update／upgrade 的 resolve 階段以 -e 傳（TOKEN_FILE 用 -v 掛）；update 唯讀、不受 frozen 限制；有新版只在 --exit-code 時回 2；末行固定印 6-15。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,100"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,120,220,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,120,280,28"/>
<mxCell id="hdr2" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="580,120,400,28"/>
<mxCell id="hdr3" value="registry（GHCR）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1000,120,290,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1310,120,280,28"/>
<mxCell id="bU" value="update [&amp;lt;repo&amp;gt;] [--exit-code]：引擎查 registry（公開／有 token → 解析 SemVer；無憑證 → 直接記該目標失敗 6-3）→ 每個目標彙總（Q27）→ 末行 6-15 → 結束碼 0／1／2" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,164,1590,1325"/>
<mxCell id="bU_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bU" geo="1546,5,30,20"/>
<mxCell id="u0" value="just vendor_kit update [&amp;lt;repo&amp;gt;] [--exit-code]" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bU" geo="20,36,220,80"/>
<mxCell id="u1" value="組 docker run 引數：-e VENDOR_KIT_REGISTRY_TOKEN／_USER，或 -v &amp;lt;TOKEN_FILE&amp;gt;:/run/vk-token:ro（只在 update／upgrade 的 resolve 傳）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bU" geo="260,40,280,73"/>
<mxCell id="u1r" value="docker run &amp;lt;引擎&amp;gt; update（單段、不經 create/cp）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bU" geo="260,136,280,42"/>
<mxCell id="u2" value="update（唯讀；不受 frozen 限制）：讀 version.toml 現版" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bU" geo="560,137,400,40"/>
<mxCell id="u2f" value="version.toml（只讀：引擎 ref、[tools]）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bU" geo="1290,137,280,40"/>
<mxCell id="u3x" value="是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bU" geo="20,214,220,80"/>
<mxCell id="u3" value="有未完成交易（.tmp.&amp;lt;verb&amp;gt;.*.toml／[progress]）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="560,198,400,112"/>
<mxCell id="u4l" value="否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）" style="fillColor=none;strokeColor=none" parent="bU" geo="560,330,400,42"/>
<mxCell id="u5" value="registry 不要求認證（公開）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="606,392,300,81"/>
<mxCell id="u5g" value="是：GET /v2/&amp;lt;name&amp;gt;/tags/list（分頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bU" geo="1110,404,160,57"/>
<mxCell id="u6" value="有 VENDOR_KIT_REGISTRY_TOKEN／_TOKEN_FILE？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="560,513,392,112"/>
<mxCell id="u6g" value="是：WWW-Authenticate 換 token → tags/list" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bU" geo="980,532,132,73"/>
<mxCell id="u6r" value="已定（Q11）：無憑證時不支援需認證的版本列舉；token 只在 update／upgrade 的 resolve 階段以 -e 傳，不寫 log、不傳給工具；GHCR 已測試，其他 registry 依標準協定可用但未驗證" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bU" geo="1290,525,280,88"/>
<mxCell id="u7" value="否：無憑證、不查 → 該目標記「查詢失敗 1 + 6-3」（不進 SemVer 解析）→ 下一目標／彙總" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bU" geo="560,645,240,57"/>
<mxCell id="u8a" value="取 SemVer 最大正式版（排除預發行）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bU" geo="810,722,150,42"/>
<mxCell id="u8b" value="與現版比較 → 記「現版 → 最新」" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bU" geo="810,784,150,42"/>
<mxCell id="u8q" value="還有下一個目標？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="610,846,300,50"/>
<mxCell id="u9" value="否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的 6-3）；訊息全列" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bU" geo="560,916,400,42"/>
<mxCell id="u10" value="末行固定印 6-15：「套用：just vendor_kit upgrade」" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bU" geo="560,978,400,40"/>
<mxCell id="u11x" value="是 → 1：查詢失敗（6-3：設 token 或指定 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;；即使另有新版）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bU" geo="20,1038,220,102"/>
<mxCell id="u11" value="任一目標查詢失敗（1）？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="560,1048,300,81"/>
<mxCell id="u12y" value="是 → 2：有新版（給 CI 用）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bU" geo="20,1172,220,58"/>
<mxCell id="u12" value="有新版且 --exit-code？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bU" geo="560,1160,300,81"/>
<mxCell id="u13" value="否 → 0：已列出（有新版也 0）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bU" geo="20,1261,220,58"/>
<mxCell id="ue0" edge="1" source="u0" target="u1"/>
<mxCell id="ue0b" edge="1" source="u1" target="u1r"/>
<mxCell id="ue1" edge="1" source="u1r" target="u2"/>
<mxCell id="ue2" value="讀" edge="1" source="u2" target="u2f"/>
<mxCell id="ue3" edge="1" source="u2" target="u3"/>
<mxCell id="ue4" value="是" edge="1" source="u3" target="u3x"/>
<mxCell id="ue5" edge="1" source="u3" target="u4l"/>
<mxCell id="ue6" edge="1" source="u4l" target="u5"/>
<mxCell id="ue7" value="是" edge="1" source="u5" target="u5g"/>
<mxCell id="ue8" value="否" edge="1" source="u5" target="u6"/>
<mxCell id="ue9" value="是" edge="1" source="u6" target="u6g"/>
<mxCell id="ue10" value="否" edge="1" source="u6" target="u7"/>
<mxCell id="ue11" edge="1" source="u5g" target="u8a"/>
<mxCell id="ue12" edge="1" source="u6g" target="u8a"/>
<mxCell id="ue13" value="記失敗" edge="1" source="u7" target="u8q"/>
<mxCell id="ue13b" edge="1" source="u8a" target="u8b"/>
<mxCell id="ue14" edge="1" source="u8b" target="u8q"/>
<mxCell id="ue14y" value="是：下一個目標" edge="1" source="u8q" target="u5"/>
<mxCell id="ue14n" value="否" edge="1" source="u8q" target="u9"/>
<mxCell id="ue15" edge="1" source="u9" target="u10"/>
<mxCell id="ue16" edge="1" source="u10" target="u11"/>
<mxCell id="ue17" value="是" edge="1" source="u11" target="u11x"/>
<mxCell id="ue18" value="否" edge="1" source="u11" target="u12"/>
<mxCell id="ue19" value="是" edge="1" source="u12" target="u12y"/>
<mxCell id="ue20" value="否" edge="1" source="u12" target="u13"/>
<mxCell id="p10_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1505,200,60"/>
<mxCell id="p10_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1505,140,64"/>
<mxCell id="p10_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1513,140,44"/>
<mxCell id="p10_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1507,190,56"/>
<mxCell id="p10_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1507,210,56"/>
<mxCell id="p10_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1515,88,40"/>
<mxCell id="p10_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1515,170,40"/>
<mxCell id="p10_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1505,280,60"/>
<mxCell id="p10_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1573,120,36"/>
<mxCell id="p10_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1573,150,36"/>
<mxCell id="p10_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1573,190,36"/>
<mxCell id="p10_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="560,1573,170,36"/>
<mxCell id="p10_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1611,200,28"/>
<mxCell id="p10_tk0" value="update" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1645,150,55"/>
<mxCell id="p10_tv0" value="只查 registry 有沒有新版、不動任何檔（唯讀，不受 frozen 限制）；單段 docker run（不經 docker create/cp）；[&amp;lt;repo&amp;gt;] 省略 = 全部工具 + vendor_kit 自身；--exit-code：有新版回 2（給 CI 用）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1645,610,55"/>
<mxCell id="p10_tk1" value="查最新" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1700,150,55"/>
<mxCell id="p10_tv1" value="對 registry 走 Docker Registry 標準協定：需要時以 WWW-Authenticate 換 token → GET /v2/&amp;lt;name&amp;gt;/tags/list（分頁）→ 取 SemVer 最大正式版（排除預發行）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」；查詢步驟畫白格（不是 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1700,610,55"/>
<mxCell id="p10_tk2" value="registry 憑證（Q11）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1755,150,55"/>
<mxCell id="p10_tv2" value="VENDOR_KIT_REGISTRY_TOKEN（+ _USER）或 VENDOR_KIT_REGISTRY_TOKEN_FILE（啟動器 -v &amp;lt;file&amp;gt;:/run/vk-token:ro 掛入；兩者同設 → 1）；只在 update／upgrade 的 resolve 階段以 -e 傳入引擎；不寫 log／檔、不傳給工具、dry-run 不印；不掛 ~/.docker/config.json" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1755,610,55"/>
<mxCell id="p10_tk3" value="6-3" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1810,150,55"/>
<mxCell id="p10_tv3" value="無法列舉 &amp;lt;repo&amp;gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;（拉取使用主機 docker 認證）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1810,610,55"/>
<mxCell id="p10_tk4" value="多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1865,150,40"/>
<mxCell id="p10_tv4" value="做得完的做完；最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1865,610,40"/>
<mxCell id="p10_tk5" value="6-15（末行固定）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1645,150,28"/>
<mxCell id="p10_tv5" value="update 最後一行永遠印「套用：just vendor_kit upgrade」" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1645,610,28"/>
<mxCell id="p10_tk6" value="未完成交易（6-33）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1673,150,55"/>
<mxCell id="p10_tv6" value="唯讀動詞（sync／update／help）偵測到 .tmp.&amp;lt;verb&amp;gt;.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;」，不自動恢復、不寫檔；update 結束 1" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1673,610,55"/>
<mxCell id="p10_tk7" value="frozen" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1728,150,40"/>
<mxCell id="p10_tv7" value="CI 非空且不為 0／false → frozen：不寫 tracked 檔、不查最新版；update 是唯讀動詞，不受 frozen 影響（CI 裡也能查）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1728,610,40"/>
<mxCell id="p10_tk8" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1768,150,55"/>
<mxCell id="p10_tv8" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1768,610,55"/>
<mxCell id="p10_tk9" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1823,150,71"/>
<mxCell id="p10_tv9" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1823,610,71"/>
</diagram>
<diagram id="v1p11" name="狀態機 v2：初始檔五態">
<mxCell id="title" value="狀態機 v2：初始檔五態 ── metadata [[file]].state 與轉移（interface_spec §4.3、Q14／Q15、v2.7-3）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q14、Q15、v2.6 16 條、v2.7-3、interface_spec §4.3）：metadata 對每個範本記單一 state（五值）+ declined_hash + lines；declined 只用於新檔被拒、從未建立；已納管檔拒絕換版／合併時 state 不變只記 declined_hash（自環）；add 時 append 檔已存在且拒絕 → unmanaged；新版 hash 不同才再問；unmanaged／declined 只在 dry-run／check.sh 提醒、不動檔不紅燈；使用者刪了已納管檔 → deleted、upgrade 維持刪除。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,100"/>
<mxCell id="bS" value="初始檔五態：每個範本一筆 state；箭頭 = 動詞：條件（自環 = 拒絕但狀態不變，只記 declined_hash）；每格一件事（狀態 → 轉入條件 → upgrade 時 → dry-run／check.sh 印什麼）；remove／uninstall 一律到終點" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,164,1590,1441"/>
<mxCell id="bS_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bS" geo="1546,5,30,20"/>
<mxCell id="s0" value="起點：範本存在於工具 dist/init.toml 的 [[file]]（src／dest／strategy）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="645,36,280,102"/>
<mxCell id="st_d" value="deleted&lt;br&gt;使用者刪了已納管檔" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="20,268,160,57"/>
<mxCell id="st_m" value="managed&lt;br&gt;已納管（vendor_kit 建的 copy 檔）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="330,268,160,57"/>
<mxCell id="st_c" value="declined&lt;br&gt;新檔被拒、從未建立" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="640,268,160,57"/>
<mxCell id="st_a" value="appended&lt;br&gt;已插入行（strategy=append）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="950,268,160,57"/>
<mxCell id="st_u" value="unmanaged&lt;br&gt;本來就有、沒納管" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="1260,268,160,57"/>
<mxCell id="in_d" value="轉入：upgrade 逐檔判斷發現 D 缺（使用者刪了已納管檔）→ state=deleted" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="120,478,190,57"/>
<mxCell id="in_m" value="轉入：add 時 dest 不存在 → 建；upgrade 新版新增檔、問「要建 X 嗎」同意 → 建；declined 再問後同意 → 建" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="430,470,190,73"/>
<mxCell id="in_c" value="轉入：upgrade 新版新增檔、問「要建 X 嗎」後明確答否（EOF／Ctrl-C 不算）→ 從未建立、記 declined_hash" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="740,470,190,73"/>
<mxCell id="in_a" value="轉入：add 時 strategy=append 且檔已存在、問「要在 X 加這幾行嗎」同意 → 插入並記 lines（原本就有的相同行不認領）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="1050,463,190,88"/>
<mxCell id="in_u" value="轉入：add 時 copy 檔已存在 → 不納管、不覆蓋（-y 也不覆蓋），印 6-11；add 時 append 檔已存在、問後拒絕 → 同樣 unmanaged（只記 declined_hash）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="1360,455,190,104"/>
<mxCell id="up_d" value="upgrade 時：維持刪除（不重建、不合併）；baseline 仍推到 N" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="120,712,190,57"/>
<mxCell id="up_m" value="upgrade 時（仍 managed）：D==N／B==N 不動；D==B 問後寫 N；皆異問後三方合併（衝突 → 2）；拒絕 → 只記 declined_hash（自環）；baseline 推到 N" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="430,689,190,104"/>
<mxCell id="up_c" value="upgrade 時：N 的 hash ≠ declined_hash → 再問；相同 → 不問（仍 declined）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="740,712,190,57"/>
<mxCell id="up_a" value="upgrade 時（仍 appended）：原文比對找 lines：唯一命中 → 問後替換（拒絕 → 只記 declined_hash，自環）；零命中 → 不動只印新內容；多處 → 保留並 warn" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="1050,689,190,104"/>
<mxCell id="up_u" value="upgrade 時：永遠不動（不合併、不覆蓋）；仍 unmanaged" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bS" geo="1360,720,190,42"/>
<mxCell id="pr_d" value="dry-run／check.sh 印：維持刪除（不重建）；不紅燈" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="120,946,190,42"/>
<mxCell id="pr_m" value="dry-run／check.sh 印：會問哪些檔（換新版／三方合併）；有 declined_hash 且新版相同 → 6-6；CI 需改 tracked 檔 → 1 印清單" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="430,923,190,88"/>
<mxCell id="pr_c" value="dry-run／check.sh 印：6-6「有 N 個範本你拒絕過」；新版有更新 → 6-8「Y 你拒絕過，vZ 有新版」；不紅燈" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="740,930,190,73"/>
<mxCell id="pr_a" value="dry-run／check.sh 印：找到 lines → 會問替換；找不到 → 印新內容；多處 → warn" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="1050,938,190,57"/>
<mxCell id="pr_u" value="dry-run／check.sh 印：6-7「X 沒納管，與範本差 N 行」；不紅燈" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="1360,938,190,57"/>
<mxCell id="end_d" value="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="20,1141,160,124"/>
<mxCell id="end_m" value="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="330,1141,160,124"/>
<mxCell id="end_c" value="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="640,1141,160,124"/>
<mxCell id="end_a" value="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="950,1141,160,124"/>
<mxCell id="end_u" value="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bS" geo="1260,1141,160,124"/>
<mxCell id="s_endn" value="終點（任一狀態皆同）：remove &amp;lt;repo&amp;gt;／uninstall → 初始檔保留並印清單（append 行問後只刪原文相同的）；metadata 隨 baseline/&amp;lt;repo&amp;gt;/ 刪除 → 狀態消失；要刪初始檔請自行 git rm" style="fillColor=#ffffff;strokeColor=#999999" parent="bS" geo="20,1395,1530,40"/>
<mxCell id="sl_m_l" value="upgrade：拒絕換版／三方合併 → 只記 declined_hash（仍 managed）" style="fillColor=none;strokeColor=none" parent="bS" geo="430,347.0,200,57"/>
<mxCell id="sl_c_l" value="upgrade：再問後仍拒絕 → 更新 declined_hash（仍 declined）" style="fillColor=none;strokeColor=none" parent="bS" geo="740,347.0,200,57"/>
<mxCell id="sl_a_l" value="upgrade：拒絕替換 lines → 只記 declined_hash（仍 appended）" style="fillColor=none;strokeColor=none" parent="bS" geo="1050,347.0,200,57"/>
<mxCell id="sl_u_l" value="upgrade：永遠不動（仍 unmanaged）" style="fillColor=none;strokeColor=none" parent="bS" geo="1360,347.0,200,42"/>
<mxCell id="se_c" value="upgrade：拒絕建新檔" edge="1" source="s0" target="st_c"/>
<mxCell id="se_m" value="add：建；upgrade：新增檔同意建" edge="1" source="s0" target="st_m"/>
<mxCell id="se_a" value="add：append 檔已存在、同意插入" edge="1" source="s0" target="st_a"/>
<mxCell id="se_u" value="add：copy 已存在；append 已存在但拒絕" edge="1" source="s0" target="st_u"/>
<mxCell id="se_md" value="upgrade：D 缺" edge="1" source="st_m" target="st_d"/>
<mxCell id="se_cm" value="upgrade：再問→同意建" edge="1" source="st_c" target="st_m"/>
<mxCell id="se_end_d" edge="1" source="st_d" target="end_d"/>
<mxCell id="se_end_m" edge="1" source="st_m" target="end_m"/>
<mxCell id="se_end_c" edge="1" source="st_c" target="end_c"/>
<mxCell id="se_end_a" edge="1" source="st_a" target="end_a"/>
<mxCell id="se_end_u" edge="1" source="st_u" target="end_u"/>
<mxCell id="sl_m" edge="1" source="st_m" target="st_m"/>
<mxCell id="sl_c" edge="1" source="st_c" target="st_c"/>
<mxCell id="sl_a" edge="1" source="st_a" target="st_a"/>
<mxCell id="sl_u" edge="1" source="st_u" target="st_u"/>
<mxCell id="p11_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1621,200,60"/>
<mxCell id="p11_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1621,140,64"/>
<mxCell id="p11_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1629,140,44"/>
<mxCell id="p11_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1623,190,56"/>
<mxCell id="p11_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1623,210,56"/>
<mxCell id="p11_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1631,88,40"/>
<mxCell id="p11_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1631,170,40"/>
<mxCell id="p11_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1621,280,60"/>
<mxCell id="p11_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1689,120,36"/>
<mxCell id="p11_lgx_state" value="粗框白格：狀態（state 值）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="180,1689,200,36"/>
<mxCell id="p11_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1727,200,28"/>
<mxCell id="p11_tk0" value="初始檔／範本" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1761,150,40"/>
<mxCell id="p11_tv0" value="工具 dist/init.toml 每個 [[file]]（src、dest、strategy = copy｜append）：add 時建到專案（dest）、upgrade 時逐檔判斷；歸使用者、進 git" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1761,610,40"/>
<mxCell id="p11_tk1" value="metadata [[file]].state（Q15、16 條）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1801,150,55"/>
<mxCell id="p11_tv1" value="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 對每個範本一筆：state 單一列舉 managed／appended／declined／unmanaged／deleted；declined_hash（選填）= 最近一次被拒絕的那版範本 N 的 sha256；lines（只在 appended）= 實際插入的行原文" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1801,610,55"/>
<mxCell id="p11_tk2" value="declined 語意（v2.7-3）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1856,150,55"/>
<mxCell id="p11_tv2" value="state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新 → state 不變、只記 declined_hash（畫成自環）；add 時 append 檔已存在且拒絕 → unmanaged（本來就有、沒納管）；二進位拒絕同" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1856,610,55"/>
<mxCell id="p11_tk3" value="B／D／N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1911,150,40"/>
<mxCell id="p11_tv3" value="B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/&amp;lt;repo&amp;gt;，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1911,610,40"/>
<mxCell id="p11_tk4" value="upgrade 逐檔判斷（managed）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1951,150,55"/>
<mxCell id="p11_tv4" value="D 缺 → deleted；D==N 或 B==N → 不動；D==B → 問「X 換成新版？」；三者皆異 → 問後 git merge-file --diff3（衝突 → 2）；不論結果 baseline 推到 N（解析失敗除外）；二進位／symlink 未改 → 問後換、改過保留 + warn；拒絕 → 記 declined_hash、state 維持 managed" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1951,610,55"/>
<mxCell id="p11_tk5" value="declined 再問規則（Q14／Q15）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2006,150,55"/>
<mxCell id="p11_tv5" value="新版 N 的 hash ≠ declined_hash → 再問一次「要建 X 嗎」（同意 → 建 → managed；拒絕 → 仍 declined、更新 declined_hash）；相同 → 不問，只印 6-6／6-8；EOF／Ctrl-C 不算拒絕、不記 declined" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2006,610,55"/>
<mxCell id="p11_tk6" value="append 行（Q6／Q12／Q13）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1761,150,55"/>
<mxCell id="p11_tv6" value="strategy=append 的檔已存在 → 問「要在 X 加這幾行嗎」；同意 → 插入並記 lines；upgrade 用原文比對（CRLF／LF 等價）找上次插入的行：唯一命中 → 問後替換、零命中 → 不動只印新內容、多處 → 保留並 warn；remove／uninstall 問後只刪原文相同的行" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1761,610,55"/>
<mxCell id="p11_tk7" value="dry-run／check.sh 印什麼" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1816,150,40"/>
<mxCell id="p11_tv7" value="upgrade --dry-run 與 ci/check.sh ③ 印 6-6「有 N 個範本你拒絕過」、6-7「X 沒納管，與範本差 N 行」、6-8「Y 你拒絕過，vZ 有新版」；不動檔、不紅燈（CI 需改 tracked 檔才 1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1816,610,40"/>
<mxCell id="p11_tk8" value="6-11" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1856,150,40"/>
<mxCell id="p11_tv8" value="add 遇 copy 檔已存在：「&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對」" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1856,610,40"/>
<mxCell id="p11_tk9" value="永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1896,150,40"/>
<mxCell id="p11_tv9" value="不變量：vendor_kit 對使用者的檔可以建、要改先問、永不刪、永不覆蓋；remove／uninstall 只印初始檔清單（要刪用 git rm）；新版刪除的檔（N 缺）只 warn 不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1896,610,40"/>
<mxCell id="p11_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1936,150,71"/>
<mxCell id="p11_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1936,610,71"/>
</diagram>
<diagram id="v1p12" name="狀態機 v2：交易與進度日誌">
<mxCell id="title" value="狀態機 v2：交易與進度日誌（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（v2.2 C、v2.4-12、v2.5-3、v2.6-9、v2.7-7、v2.8-2、interface_spec §0 進度日誌、§4.3 [progress]、§4.6）：apply 順序 = flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 寫入 → 最後一步刪日誌（uninstall 在根 justfile 那行之後）；中斷 → 1 明列已完成／未完成；下次可寫動詞先恢復（失敗 6-27）、唯讀動詞只提示 6-33 不恢復；prune 特例：活躍日誌只列出不刪、不視為未完成交易；install 例外：第一次 install 不建日誌、失敗整包丟棄，修復型 install 建 .tmp.install.&amp;lt;id&amp;gt;.toml。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,116"/>
<mxCell id="hdr0" value="使用者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,136,240,28"/>
<mxCell id="hdr1" value="引擎容器（apply 段）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="300,136,480,28"/>
<mxCell id="hdr2" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="800,136,380,28"/>
<mxCell id="hdr3" value="規則／說明" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1200,136,390,28"/>
<mxCell id="bT1" value="交易生命週期（所有可寫動詞的 apply 段；第一次 install 例外：不建日誌、失敗整包丟棄）：拿鎖 → 重驗指紋 → dry-run 分支 → 建日誌 → 逐步寫入（每步 ① 寫暫存 ② 原子替換 ③ 日誌 done）→ 刪日誌；中斷 → 1、日誌留著" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,180,1590,953"/>
<mxCell id="bT1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bT1" geo="1546,5,30,20"/>
<mxCell id="t0" value="來自各動詞頁：resolve → 啟動器 docker 之後，apply &amp;lt;verb&amp;gt;" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bT1" geo="20,36,240,80"/>
<mxCell id="t1" value="拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26；VENDOR_KIT_NO_LOCK=1 跳過）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,55,480,42"/>
<mxCell id="t1i" value="不變量：回 3 一律零寫入（無任何例外）；工具層回 1 時 version.toml 不動；日誌在第一個寫入前建、最後一步刪；never fail silently" style="fillColor=#ffffff;strokeColor=#b85450" parent="bT1" geo="1180,48,390,57"/>
<mxCell id="t2" value="重驗指紋（與 /dist/vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」，零寫入）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,132,480,42"/>
<mxCell id="t3y" value="是 → 0：唯讀預覽（CI 為真且需改 tracked 檔 → 1）；不建日誌" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT1" geo="20,190,240,80"/>
<mxCell id="t3" value="--dry-run？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT1" geo="280,205,200,50"/>
<mxCell id="t4" value="建進度日誌（第一個寫入前）：state=in-progress、verb、id、started、targets、done[]／pending[]、consents" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,368,480,42"/>
<mxCell id="t4f" value="日誌位置（依動詞）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT1" geo="780,286,380,206"/>
<mxCell id="t4f_0" value="add／upgrade：baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml [progress]" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="t4f" geo="8,26,364,42"/>
<mxCell id="t4f_1" value="remove／uninstall／undev／prune：.vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="t4f" geo="8,74,364,42"/>
<mxCell id="t4f_2" value="修復型 install：.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="t4f" geo="8,122,364,42"/>
<mxCell id="t4f_3" value="第一次 install（薄殼不存在）：不建日誌" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="t4f" geo="8,170,364,26"/>
<mxCell id="t4n" value="已定（v2.8-2）install 例外：第一次 install（薄殼不存在）不建日誌，失敗整包丟棄、不留半成品，下次直接重跑；修復型 install（薄殼已存在）建 .tmp.install.&amp;lt;id&amp;gt;.toml，同其他可寫動詞走恢復。其餘兩種位置：remove／uninstall 會刪 metadata、undev／prune 沒有工具 metadata → 放 .vendor_kit/.tmp.*（自有 .gitignore 擋）；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bT1" geo="1180,329,390,120"/>
<mxCell id="t5" value="逐步寫入 ①：寫暫存檔（合併也在暫存完成；詢問取得的同意先記進 consents）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,524,480,40"/>
<mxCell id="t5af" value="暫存檔（目標檔旁；未換上前目標檔不動）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT1" geo="780,524,380,40"/>
<mxCell id="t5n" value="每一步都是 ①②③ 三個可獨立失敗的動作；步驟順序固定：清除衝突狀態 → append／初始檔 → baseline → metadata → cache → gen/tools.just（最後寫、與 cache 同一 apply 內原子替換）→ version.toml 最後" style="fillColor=#ffffff;strokeColor=#999999" parent="bT1" geo="1180,508,390,73"/>
<mxCell id="t5b" value="逐步寫入 ②：原子替換（rename 暫存檔 → 目標檔；一檔一次換上）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,597,480,40"/>
<mxCell id="t5bf" value="目標檔（換上；中斷只會留下「已換上」「未換上」兩種）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT1" geo="780,597,380,40"/>
<mxCell id="t5c" value="逐步寫入 ③：更新日誌 done += 步驟（pending 移出）；還有步驟 → 回 ①" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,653,480,40"/>
<mxCell id="t5f" value="日誌 done[]／pending[] 每步更新" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT1" geo="780,653,380,40"/>
<mxCell id="t6x" value="是 → 1：明列已完成／未完成；日誌留著（state 仍 in-progress）；第一次 install：整包丟棄、無日誌" style="fillColor=#f8cecc;strokeColor=#000000" parent="bT1" geo="20,709,240,124"/>
<mxCell id="t6" value="中斷？（寫入失敗／Ctrl-C／斷電）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT1" geo="280,730,300,81"/>
<mxCell id="t7" value="否：最後一步刪日誌（uninstall：在根 justfile 那行之後才刪）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT1" geo="280,850,480,40"/>
<mxCell id="t7f" value="日誌刪除 = 交易完成（.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml 刪／[progress] 移除）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT1" geo="780,849,380,42"/>
<mxCell id="t8" value="0（或 2 有衝突）：印摘要" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT1" geo="20,907,240,40"/>
<mxCell id="te0" edge="1" source="t0" target="t1"/>
<mxCell id="te1" edge="1" source="t1" target="t2"/>
<mxCell id="te2" edge="1" source="t2" target="t3"/>
<mxCell id="te3" value="是" edge="1" source="t3" target="t3y"/>
<mxCell id="te4" value="否" edge="1" source="t3" target="t4"/>
<mxCell id="te5" value="建" edge="1" source="t4" target="t4f"/>
<mxCell id="te6" edge="1" source="t4" target="t5"/>
<mxCell id="te7a" value="寫" edge="1" source="t5" target="t5af"/>
<mxCell id="te6b" edge="1" source="t5" target="t5b"/>
<mxCell id="te7b" value="換" edge="1" source="t5b" target="t5bf"/>
<mxCell id="te6c" edge="1" source="t5b" target="t5c"/>
<mxCell id="te7" value="寫" edge="1" source="t5c" target="t5f"/>
<mxCell id="te8" edge="1" source="t5c" target="t6"/>
<mxCell id="te9" value="是" edge="1" source="t6" target="t6x"/>
<mxCell id="te10" value="否" edge="1" source="t6" target="t7"/>
<mxCell id="te11" value="刪" edge="1" source="t7" target="t7f"/>
<mxCell id="te12" edge="1" source="t7" target="t8"/>
<mxCell id="bT2" value="中斷後的下一次執行（任何動詞開始前先偵測未完成交易）：可寫動詞先恢復再繼續；唯讀動詞只提示重跑原動詞；prune 特例只列出" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,1149,1590,694"/>
<mxCell id="bT2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bT2" geo="1546,5,30,20"/>
<mxCell id="r0" value="打任何 vendor_kit 動詞" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT2" geo="20,37,240,40"/>
<mxCell id="r1" value="偵測未完成交易：.vendor_kit/.tmp.&amp;lt;verb&amp;gt;.*.toml（含 .tmp.install.*）或任一 metadata [progress] state=in-progress" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT2" geo="280,36,480,42"/>
<mxCell id="r1f" value="讀日誌（verb、id、targets、done／pending、consents）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT2" geo="780,37,380,40"/>
<mxCell id="r2n" value="否 → 正常執行本次動詞" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT2" geo="20,99,240,40"/>
<mxCell id="r2" value="有未完成交易？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT2" geo="370,94,220,50"/>
<mxCell id="r2px" value="是 → prune 特例：只列出活躍日誌、印 6-33（不刪、不恢復）→ 繼續 prune（接 prune 頁）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT2" geo="20,176,240,102"/>
<mxCell id="r2p" value="本動詞是 prune？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT2" geo="370,186,220,81"/>
<mxCell id="r2pn" value="已定（v2.7-7）：prune 遇活躍日誌不擋、不恢復、不刪；只列出提示重跑原動詞；差集與 apply prune 照做" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bT2" geo="1180,206,390,42"/>
<mxCell id="r3x" value="否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bT2" geo="20,326,240,80"/>
<mxCell id="r3" value="本動詞可寫？（修復型 install／add／remove／upgrade／undev／uninstall）" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT2" geo="280,310,400,112"/>
<mxCell id="r3n" value="已定（v2.6-9）：唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復；help 不受影響" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bT2" geo="1180,345,390,42"/>
<mxCell id="r4" value="是：恢復 = 依日誌把上次交易走完（done 略過；pending 逐步補做；consents 已記的不再問）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT2" geo="280,438,480,42"/>
<mxCell id="r4f" value="補做 pending 的寫入（暫存 → 原子替換）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT2" geo="780,439,380,40"/>
<mxCell id="r5x" value="否 → 1 + 6-27「未恢復：&amp;lt;檔名&amp;gt;」逐檔列出；日誌留著" style="fillColor=#f8cecc;strokeColor=#000000" parent="bT2" geo="20,496,240,80"/>
<mxCell id="r5" value="恢復成功？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bT2" geo="280,511,220,50"/>
<mxCell id="r6" value="是：刪日誌 → 繼續本次動詞（resolve 會重算指紋）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bT2" geo="280,592,480,40"/>
<mxCell id="r6f" value="日誌刪除" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bT2" geo="780,592,380,40"/>
<mxCell id="r7" value="→ 繼續本次動詞" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bT2" geo="20,648,240,40"/>
<mxCell id="re0" edge="1" source="r0" target="r1"/>
<mxCell id="re1" value="讀" edge="1" source="r1" target="r1f"/>
<mxCell id="re2" edge="1" source="r1" target="r2"/>
<mxCell id="re3" value="否" edge="1" source="r2" target="r2n"/>
<mxCell id="re4" value="是" edge="1" source="r2" target="r2p"/>
<mxCell id="re4p" value="是" edge="1" source="r2p" target="r2px"/>
<mxCell id="re4n" value="否" edge="1" source="r2p" target="r3"/>
<mxCell id="re5" value="否" edge="1" source="r3" target="r3x"/>
<mxCell id="re6" value="是" edge="1" source="r3" target="r4"/>
<mxCell id="re7" value="寫" edge="1" source="r4" target="r4f"/>
<mxCell id="re8" edge="1" source="r4" target="r5"/>
<mxCell id="re9" value="否" edge="1" source="r5" target="r5x"/>
<mxCell id="re10" value="是" edge="1" source="r5" target="r6"/>
<mxCell id="re11" value="刪" edge="1" source="r6" target="r6f"/>
<mxCell id="re12" edge="1" source="r6" target="r7"/>
<mxCell id="p12_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1859,200,60"/>
<mxCell id="p12_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1859,140,64"/>
<mxCell id="p12_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1867,140,44"/>
<mxCell id="p12_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1861,190,56"/>
<mxCell id="p12_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1861,210,56"/>
<mxCell id="p12_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1869,88,40"/>
<mxCell id="p12_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1869,170,40"/>
<mxCell id="p12_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1859,280,60"/>
<mxCell id="p12_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1927,120,36"/>
<mxCell id="p12_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1927,150,36"/>
<mxCell id="p12_lgx_inv" value="紅粗框：不變量" style="fillColor=#ffffff;strokeColor=#b85450" geo="350,1927,130,36"/>
<mxCell id="p12_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="500,1927,190,36"/>
<mxCell id="p12_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="710,1927,170,36"/>
<mxCell id="p12_lgx_entry" value="虛線橢圓：來自其他頁" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="900,1927,200,36"/>
<mxCell id="p12_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1965,200,28"/>
<mxCell id="p12_tk0" value="交易／apply" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1999,150,40"/>
<mxCell id="p12_tv0" value="一次會寫檔的動詞執行 = 一筆交易：apply 拿 flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 逐步寫入 → 最後一步刪日誌；回 3 一律零寫入；工具層回 1 時 version.toml 不動" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1999,610,40"/>
<mxCell id="p12_tk1" value="進度日誌" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2039,150,40"/>
<mxCell id="p12_tv1" value="記錄交易進度的 TOML：state=&quot;in-progress&quot;、verb、id、started（UTC ISO 8601）、targets、done／pending（步驟清單）、consents（已取得的同意）；存在 = 上次沒走完" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2039,610,40"/>
<mxCell id="p12_tk2" value="兩種位置" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2079,150,55"/>
<mxCell id="p12_tv2" value="add／upgrade 記在 metadata baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 的 [progress]；remove／uninstall／undev／prune／修復型 install 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（因為 metadata 會被刪或不存在）；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機（不用 &amp;lt;repo&amp;gt;，uninstall 多工具才不撞）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2079,610,55"/>
<mxCell id="p12_tk3" value="install 的日誌（v2.8-2）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2134,150,55"/>
<mxCell id="p12_tv3" value="第一次 install（薄殼不存在）不建日誌：失敗整包丟棄、不留半成品（bootstrap.sh 的 1 失敗不留半成品只對它成立），下次直接重跑；修復型 install（薄殼已存在、冪等修復）建 .vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml，與其他可寫動詞一樣走恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2134,610,55"/>
<mxCell id="p12_tk4" value="恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2189,150,55"/>
<mxCell id="p12_tv4" value="可寫動詞（修復型 install／add／remove／upgrade／undev／uninstall）開始前偵測到未完成交易 → 先依日誌把交易走完（done 略過、pending 補做、consents 不再問）再繼續本次；失敗 → 1 印 6-27「未恢復：&amp;lt;檔名&amp;gt;」逐檔列出、日誌留著；第一次 install 沒有日誌可恢復（整包丟棄後重跑）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2189,610,55"/>
<mxCell id="p12_tk5" value="唯讀動詞不恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2244,150,40"/>
<mxCell id="p12_tv5" value="sync／update 偵測到未完成交易只印 6-33「偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;」→ 1，不寫任何檔；help 不受影響" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2244,610,40"/>
<mxCell id="p12_tk6" value="prune 特例（v2.7-7）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2284,150,55"/>
<mxCell id="p12_tv6" value="prune 遇活躍（未恢復）日誌：只列出並印 6-33、不刪、不視為未完成交易（不擋 prune、不恢復）；prune 自己的 apply 也建 .tmp.prune.&amp;lt;id&amp;gt;.toml（清理前建、清理後刪；v2.9-6），與其他可寫動詞一樣走恢復" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2284,610,55"/>
<mxCell id="p12_tk7" value="原子替換／暫存" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1999,150,40"/>
<mxCell id="p12_tv7" value="每個寫入先寫到暫存（合併也在暫存完成），確認沒問題再逐檔一次換上（rename）；gen/tools.just 最後寫、與 cache 同一 apply 內原子替換；中斷只會留下「已換上」與「未換上」兩種檔，不留半寫的檔" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1999,610,40"/>
<mxCell id="p12_tk8" value=".tmp.dist.&amp;lt;id&amp;gt;/" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2039,150,40"/>
<mxCell id="p12_tv8" value="啟動器暫存（展開的工具 dist、vk-resolve）；不是交易日誌；啟動器 trap … EXIT INT TERM 清容器與此目錄；殘留由 prune 清" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2039,610,40"/>
<mxCell id="p12_tk9" value="dry-run" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2079,150,40"/>
<mxCell id="p12_tv9" value="apply --dry-run：唯讀預覽（本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單）；不建日誌、不寫檔；也要先拉 image 展開才知道會問哪些檔" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2079,610,40"/>
<mxCell id="p12_tk10" value="指紋／flock" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2119,150,55"/>
<mxCell id="p12_tv10" value="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2119,610,55"/>
<mxCell id="p12_tk11" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2174,150,55"/>
<mxCell id="p12_tv11" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2174,610,55"/>
<mxCell id="p12_tk12" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2229,150,71"/>
<mxCell id="p12_tv12" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2229,610,71"/>
</diagram>
<diagram id="v1p13" name="相容性矩陣 v2">
<mxCell id="title" value="相容性矩陣 v2：舊薄殼 × 新引擎、舊引擎 × 新檔 → 0／1／3（interface_spec §2、§8；Q16／Q19／Q23）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q16、Q19、Q23、v2.4-3／-6／-7、v2.6 16 條、v2.7-4、interface_spec §2、§4 通則、§8）：相容承諾兩層（永久：救援路徑 + 舊資料可讀可遷；非永久：舊薄殼跑新 major 一般動詞回 3）；floor = 固定 release 常數；新舊以 P／schema 比較不用版本字串；回 3 零寫入、無任何例外（救援路徑亦同）；written_by 純資訊欄、無 min_reader；同 schema 未知欄位讀忽略寫保留。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="l13a" value="(a) 舊薄殼 P × 新引擎（接受 [floor_P, current_P]）：一般動詞／救援路徑各回什麼" style="fillColor=none;strokeColor=none" geo="40,120,900,24"/>
<mxCell id="ta_h0" value="薄殼 P 的情況" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,150,330,30"/>
<mxCell id="ta_h1" value="一般動詞（add／remove／upgrade &amp;lt;repo&amp;gt;／sync 寫入／undev／uninstall／prune／dev／update）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="370,150,640,30"/>
<mxCell id="ta_h2" value="救援路徑（install／upgrade vendor_kit／sync 不符提示／help；單段）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1010,150,590,30"/>
<mxCell id="ta_r0c0" value="P &amp;lt; floor_P（太舊）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,180,330,30"/>
<mxCell id="ta_r0c1" value="3 + 6-18「請以 bootstrap.sh 重建」；零寫入；floor 檢查先於任何上網（斷網也回 3）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="370,180,640,30"/>
<mxCell id="ta_r0c2" value="3 + 6-18（救援路徑也不接、同樣零寫入；唯一可用 synthetic fixture 驗收）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1010,180,590,30"/>
<mxCell id="ta_r1c0" value="floor_P ≤ P &amp;lt; 引擎需求（舊薄殼 × 新 major）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,210,330,42"/>
<mxCell id="ta_r1c1" value="3 + 6-36「薄殼協定 &amp;lt;P_shell&amp;gt; 低於引擎 &amp;lt;vY&amp;gt; 的一般動詞需求，請先 upgrade vendor_kit」；零寫入" style="fillColor=#ffe6cc;strokeColor=#999999" geo="370,210,640,42"/>
<mxCell id="ta_r1c2" value="0／1 正常（永久保證）：install／upgrade vendor_kit 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」；sync 不符 → 1 + 6-1；help → 0" style="fillColor=#d5e8d4;strokeColor=#999999" geo="1010,210,590,42"/>
<mxCell id="ta_r2c0" value="同 major（P 在引擎支援範圍內）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,252,330,42"/>
<mxCell id="ta_r2c1" value="0／1／2 正常：引擎以呼叫方 P 輸出 vk-resolve/P 與結束碼語意；不輸出呼叫方不認識的 kind、不要求其未提供的 mount／環境變數" style="fillColor=#d5e8d4;strokeColor=#999999" geo="370,252,640,42"/>
<mxCell id="ta_r2c2" value="0／1 正常；upgrade vendor_kit 無新版且薄殼相符 → 0 無變更" style="fillColor=#d5e8d4;strokeColor=#999999" geo="1010,252,590,42"/>
<mxCell id="ta_r3c0" value="P &amp;gt; current_P（新薄殼 × 舊引擎：降版／dev -i 舊 image）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,294,330,73"/>
<mxCell id="ta_r3c1" value="3：P 不在引擎的 [floor_P, current_P]；零寫入" style="fillColor=#ffe6cc;strokeColor=#999999" geo="370,294,640,73"/>
<mxCell id="ta_r3c2" value="降版 upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎能無損讀現有檔（同 P／schema）→ 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前 3 + 6-10「請 git revert」（零寫入）；dev vendor_kit -i 舊 image 禁止重產 tracked 薄殼 → 3" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1010,294,590,73"/>
<mxCell id="l13b" value="(b) 舊引擎 × 檔案 schema（每檔各自 schema = N；讀取門檻只看 schema）" style="fillColor=none;strokeColor=none" geo="40,391,900,24"/>
<mxCell id="tb_h0" value="檔 vs 引擎" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,421,300,30"/>
<mxCell id="tb_h1" value="讀" style="fillColor=#e6e6e6;strokeColor=#999999" geo="340,421,420,30"/>
<mxCell id="tb_h2" value="寫" style="fillColor=#e6e6e6;strokeColor=#999999" geo="760,421,560,30"/>
<mxCell id="tb_h3" value="結束碼" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1320,421,280,30"/>
<mxCell id="tb_r0c0" value="同 schema、有未知欄位" style="fillColor=#ffffff;strokeColor=#999999" geo="40,451,300,30"/>
<mxCell id="tb_r0c1" value="讀時忽略未知欄位" style="fillColor=#ffffff;strokeColor=#999999" geo="340,451,420,30"/>
<mxCell id="tb_r0c2" value="寫時保留未知欄位（不能保留 → 拒絕寫）；只拒絕型別錯／重複宣告" style="fillColor=#ffffff;strokeColor=#999999" geo="760,451,560,30"/>
<mxCell id="tb_r0c3" value="0（型別錯／重複宣告 → 1）" style="fillColor=#d5e8d4;strokeColor=#999999" geo="1320,451,280,30"/>
<mxCell id="tb_r1c0" value="檔 schema &amp;lt; 引擎（舊檔）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,481,300,42"/>
<mxCell id="tb_r1c1" value="可讀：記憶體轉換（讀任一舊 schema → 當前 schema，不鏈式）" style="fillColor=#ffffff;strokeColor=#999999" geo="340,481,420,42"/>
<mxCell id="tb_r1c2" value="只在本來要寫該檔的明確動作才寫回當前 schema；metadata 遷移由 upgrade vendor_kit 做、dry-run 明列；同一專案短暫混合 schema 合法" style="fillColor=#ffffff;strokeColor=#999999" geo="760,481,560,42"/>
<mxCell id="tb_r1c3" value="0" style="fillColor=#d5e8d4;strokeColor=#999999" geo="1320,481,280,42"/>
<mxCell id="tb_r2c0" value="檔 schema &amp;gt; 引擎支援上限（新檔）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,523,300,42"/>
<mxCell id="tb_r2c1" value="拒絕讀：3 + 6-19「schema &amp;lt;N&amp;gt; 高於本引擎支援的 &amp;lt;M&amp;gt;；寫入者為 vendor_kit &amp;lt;written_by&amp;gt;」" style="fillColor=#ffffff;strokeColor=#999999" geo="340,523,420,42"/>
<mxCell id="tb_r2c2" value="任何寫入前退出（零寫入）；dev vendor_kit -i 舊 image 亦同" style="fillColor=#ffffff;strokeColor=#999999" geo="760,523,560,42"/>
<mxCell id="tb_r2c3" value="3" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1320,523,280,42"/>
<mxCell id="tb_r3c0" value="降版目標引擎（upgrade vendor_kit@&amp;lt;舊版&amp;gt;）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,565,300,42"/>
<mxCell id="tb_r3c1" value="以目標 image LABEL 的 P／schema 判：能無損讀現有檔 → 讀" style="fillColor=#ffffff;strokeColor=#999999" geo="340,565,420,42"/>
<mxCell id="tb_r3c2" value="無損 → 重產薄殼 → 1 + 6-2（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前拒絕 3 + 6-10「請 git revert」" style="fillColor=#ffffff;strokeColor=#999999" geo="760,565,560,42"/>
<mxCell id="tb_r3c3" value="1（無損 → 重產薄殼）／3（否則）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1320,565,280,42"/>
<mxCell id="k13a" value="floor 常數（已定）：第一個正式版 v1.0.0、P=1、schema=1；寫在契約，只能經 ADR + major 提高；引擎 image LABEL ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt; 讓啟動器不起容器即可判 floor；低於 floor → 3 + 6-18 零寫入" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="40,631,500,57"/>
<mxCell id="k13b" value="--protocol 協商（已定，Q16）：薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎接受 [floor_P, current_P]，以呼叫方 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1；引擎宣稱的 P 真不支援 → 3" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="560,631,520,73"/>
<mxCell id="k13c" value="Q16 兩層承諾（已定）：永久 —— 任何 ≥ floor 的舊薄殼可叫新引擎的救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/）並得正確提示；舊資料永遠可讀可遷。非永久 —— 舊薄殼跑新 major 一般動詞只保證乾淨回 3 + 6-36（零寫入）；同 major 內保留已承諾薄殼的一般呼叫" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="1100,631,490,73"/>
<mxCell id="k13d" value="written_by：每個 vendor_kit 寫的 TOML 都有 written_by = &quot;&amp;lt;vX&amp;gt;&quot;（寫入引擎版本），純資訊欄、不作讀取門檻（無 min_reader）；6-19 印出它供人判斷該用哪個引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="40,720,500,57"/>
<mxCell id="k13e" value="新舊怎麼比：一律以 P／schema 比較，不用 SemVer 版本字串；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1 的情境（印記不符、薄殼被改 6-28、自身升級完成要重跑 6-2）維持 1，不因訊息含 upgrade 而改 3；回 3 零寫入無任何例外（v2.7-4）" style="fillColor=#ffffff;strokeColor=#999999" geo="560,720,520,57"/>
<mxCell id="k13f" value="驗收（§7.4-1～8）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 驅動候選 C（線性）；連升 r_i → r_j → C；floor 直接跳升；降版同 P／schema 成功（重產薄殼 → 1）、跨 schema 3；&amp;lt; floor 唯一 synthetic；舊引擎讀新檔 3 零寫入；舊 bootstrap.sh 再跑不降版；已釋出 image／資產／fixture 永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="1100,720,490,73"/>
<mxCell id="p13_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,823,200,60"/>
<mxCell id="p13_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,823,140,64"/>
<mxCell id="p13_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,831,140,44"/>
<mxCell id="p13_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,825,190,56"/>
<mxCell id="p13_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,825,210,56"/>
<mxCell id="p13_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,833,88,40"/>
<mxCell id="p13_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,833,170,40"/>
<mxCell id="p13_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,823,280,60"/>
<mxCell id="p13_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,891,120,36"/>
<mxCell id="p13_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,891,150,36"/>
<mxCell id="p13_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="350,891,170,36"/>
<mxCell id="p13_lgx_c0" value="綠格：結束碼 0" style="fillColor=#d5e8d4;strokeColor=#999999" geo="540,891,110,36"/>
<mxCell id="p13_lgx_cx" value="橙格：需要人動作（1／2／3）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="670,891,190,36"/>
<mxCell id="p13_lgx_cell" value="白格：表格內容" style="fillColor=#ffffff;strokeColor=#999999" geo="880,891,110,36"/>
<mxCell id="p13_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,929,200,28"/>
<mxCell id="p13_tk0" value="薄殼 P／引擎 [floor_P, current_P]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,963,150,55"/>
<mxCell id="p13_tv0" value="薄殼 = 進 git 的 .vendor_kit/ 四檔（entry.just、vendor.just、.gitignore、ci/check.sh），首行自描述帶協定號 P；引擎 image 接受 [floor_P, current_P]（LABEL ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;，啟動器不起容器即可判 floor）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,963,610,55"/>
<mxCell id="p13_tk1" value="--protocol P" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1018,150,55"/>
<mxCell id="p13_tv1" value="薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎以呼叫方的 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1018,610,55"/>
<mxCell id="p13_tk2" value="floor" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1073,150,40"/>
<mxCell id="p13_tv2" value="固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1）；只能經 ADR + major 提高；低於 floor → 3 + 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1073,610,40"/>
<mxCell id="p13_tk3" value="救援路徑（永久）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1113,150,55"/>
<mxCell id="p13_tv3" value="install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 + 6-1」判定、help：單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼都能經此叫任何引擎重產薄殼（反向降版亦然，受 3 (c)(d) 限制）；救援路徑回 3 時同樣零寫入" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1113,610,55"/>
<mxCell id="p13_tk4" value="一般動詞（非永久）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1168,150,55"/>
<mxCell id="p13_tv4" value="add／remove／upgrade &amp;lt;repo&amp;gt;／sync 寫入／undev／uninstall／prune／dev／update：舊薄殼跑新 major 只保證乾淨回 3 + 6-36 提示先 upgrade vendor_kit（零寫入）；同 major 內保留所有已承諾薄殼的一般呼叫" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1168,610,55"/>
<mxCell id="p13_tk5" value="schema N" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1223,150,55"/>
<mxCell id="p13_tv5" value="每個 vendor_kit 寫的 TOML（version.toml、version.local.toml、metadata、.tmp.*）有 schema = N（integer）：讀取門檻只看它；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯／重複宣告 → 1；讀任一舊 schema → 直接寫當前 schema（不鏈式）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1223,610,55"/>
<mxCell id="p13_tk6" value="written_by" style="fillColor=#ffffff;strokeColor=#999999" geo="840,963,150,40"/>
<mxCell id="p13_tv6" value="寫入引擎版本（string），純資訊欄、不作讀取門檻（無 min_reader）；6-19 訊息印出它供人判斷該用哪個引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="990,963,610,40"/>
<mxCell id="p13_tk7" value="6-18／6-19／6-36／6-10" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1003,150,55"/>
<mxCell id="p13_tv7" value="6-18 薄殼／引擎低於 floor「請以 bootstrap.sh 重建」；6-19 schema N 高於本引擎支援的 M；6-36 薄殼協定低於引擎一般動詞需求「請先 upgrade vendor_kit」；6-10 降版目標引擎無法無損讀「請 git revert」；四者皆 3、零寫入" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1003,610,55"/>
<mxCell id="p13_tk8" value="降版" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1058,150,55"/>
<mxCell id="p13_tv8" value="upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以其 image LABEL 的 P／schema 判）能無損讀現有檔才做（做 = 重產薄殼 → 1 + 6-2），否則改檔前拒絕 3 + 6-10；dev vendor_kit -i &amp;lt;舊 image&amp;gt; 允許但禁止重產 tracked 薄殼" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1058,610,55"/>
<mxCell id="p13_tk9" value="驗收（§7.4）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1113,150,55"/>
<mxCell id="p13_tv9" value="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture 驅動候選（線性，非兩兩相乘）；連升 r_i → r_j → C；floor 直接跳升；降版；&amp;lt; floor 用唯一 synthetic；舊引擎讀新檔 3 零寫入；已釋出 image／Release 資產／fixture 永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1113,610,55"/>
<mxCell id="p13_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1168,150,71"/>
<mxCell id="p13_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1168,610,71"/>
</diagram>
<diagram id="v1p14" name="結束碼決策表 v2">
<mxCell id="title" value="結束碼決策表 v2：動詞 × 情況 → 0／1／2／3（interface_spec §1.2、§2、§7.1；Q23／Q27）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q23、Q27、v2.6-15、v2.7-4／-8、interface_spec §1.2 每動詞結束碼欄、§2 結束碼總表、§7.1）：3 = 版本／協定／schema 不合且零寫入（無任何例外；P &amp;lt; floor 時任何動詞含 help 都回 3 + 6-18，v2.9-7）；既定回 1 的情境維持 1；多工具做得完的做完再回最需要處理的碼；CI 動作：0 過、1 修、2 解衝突、3 換版本；顏色：0 綠、需要人動作 1／2／3 橙（含 update 無憑證 6-3）、失敗 1 紅。" style="fillColor=#ffffff;strokeColor=#999999" geo="1080,12,520,92"/>
<mxCell id="te_h0" value="動詞" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,120,170,30"/>
<mxCell id="te_h1" value="0 成功（綠）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="210,120,250,30"/>
<mxCell id="te_h2" value="1 需要人動作（橙：印指令）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="460,120,420,30"/>
<mxCell id="te_h3" value="1 失敗（紅）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="880,120,260,30"/>
<mxCell id="te_h4" value="2 衝突／有新版（橙）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1140,120,240,30"/>
<mxCell id="te_h5" value="3 版本不合（橙；零寫入）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1380,120,210,30"/>
<mxCell id="te_r0c0" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,150,170,42"/>
<mxCell id="te_r0c1" value="install 與每個 -t 的 add 都完成" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,150,250,42"/>
<mxCell id="te_r0c2" value="非 git repo（6-16）；just &amp;lt; 1.33.0（6-23）；需問但無 tty（6-4）；任一 add 失敗（明列已完成／未完成）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,150,420,42"/>
<mxCell id="te_r0c3" value="pull 失敗／逾時（6-24／6-31）；install 失敗（第一次不留半成品）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,150,260,42"/>
<mxCell id="te_r0c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,150,240,42"/>
<mxCell id="te_r0c5" value="薄殼／引擎 &amp;lt; floor（6-18）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,150,210,42"/>
<mxCell id="te_r1c0" value="install" style="fillColor=#ffffff;strokeColor=#999999" geo="40,192,170,57"/>
<mxCell id="te_r1c1" value="建立或修復完成；已含 import 行不再加；--no-justfile 只印指示；問後拒絕加行 → 不動、印指示" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,192,250,57"/>
<mxCell id="te_r1c2" value="非 git（6-16）；巢狀（6-35）；install &amp;lt;repo&amp;gt; 誤用（6-17）；薄殼被改（6-28，列差異不動）；無 tty 需問（6-4）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,192,420,57"/>
<mxCell id="te_r1c3" value="寫入失敗（第一次不留半成品）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,192,260,57"/>
<mxCell id="te_r1c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,192,240,57"/>
<mxCell id="te_r1c5" value="P &amp;lt; floor（6-18）；檔 schema 高於支援（6-19）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,192,210,57"/>
<mxCell id="te_r2c0" value="uninstall" style="fillColor=#ffffff;strokeColor=#999999" geo="40,249,170,42"/>
<mxCell id="te_r2c1" value="完成（初始檔保留印清單；未知或被改的檔保留並回報）；dry-run 本機" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,249,250,42"/>
<mxCell id="te_r2c2" value="任一工具在 dev 覆寫中（先 undev）；CI 需改 tracked 檔；指紋不同（6-12）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,249,420,42"/>
<mxCell id="te_r2c3" value="任一工具 remove 失敗 → 中止、列已完成部分" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,249,260,42"/>
<mxCell id="te_r2c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,249,240,42"/>
<mxCell id="te_r2c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,249,210,42"/>
<mxCell id="te_r3c0" value="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,291,170,57"/>
<mxCell id="te_r3c1" value="接入完成；已接入且完成 → 無變更；dry-run 本機" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,291,250,57"/>
<mxCell id="te_r3c2" value="@&amp;lt;tag&amp;gt; 與鎖定不同（改用 upgrade）；私有且無憑證又未指定 @&amp;lt;tag&amp;gt;（6-3）；dest 不合法／撞名；&amp;lt;ns&amp;gt; 撞名；CI 需改 tracked；指紋不同（6-12）；未完成交易恢復失敗（6-27）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,291,420,57"/>
<mxCell id="te_r3c3" value="pull 失敗／逾時；dist 含 symlink；寫入失敗（version.toml 一律未動）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,291,260,57"/>
<mxCell id="te_r3c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,291,240,57"/>
<mxCell id="te_r3c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,291,210,57"/>
<mxCell id="te_r4c0" value="remove &amp;lt;repo&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="40,348,170,42"/>
<mxCell id="te_r4c1" value="完成（初始檔永不刪、印清單）；未接 → 提示" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,348,250,42"/>
<mxCell id="te_r4c2" value="dev 覆寫中（先 undev）；CI 需改 tracked；指紋不同" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,348,420,42"/>
<mxCell id="te_r4c3" value="寫入失敗（可恢復狀態）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,348,260,42"/>
<mxCell id="te_r4c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,348,240,42"/>
<mxCell id="te_r4c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,348,210,42"/>
<mxCell id="te_r5c0" value="update [&amp;lt;repo&amp;gt;]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,390,170,42"/>
<mxCell id="te_r5c1" value="已列出（有新版也 0；末行 6-15）" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,390,250,42"/>
<mxCell id="te_r5c2" value="未完成交易（6-33）；任一目標查詢失敗（含無憑證 6-3：設 token 或 upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;；即使另有新版）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,390,420,42"/>
<mxCell id="te_r5c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="880,390,260,42"/>
<mxCell id="te_r5c4" value="--exit-code 且有新版" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1140,390,240,42"/>
<mxCell id="te_r5c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,390,210,42"/>
<mxCell id="te_r6c0" value="upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,432,170,73"/>
<mxCell id="te_r6c1" value="完成；無新版；(1) 補齊待合併後停（6-14）；dry-run 本機" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,432,250,73"/>
<mxCell id="te_r6c2" value="無 baseline（先 add）；dev 覆寫中（先 undev）；CI 需改 tracked（6-5）；指紋不同；自身升級後「請 commit 並再跑原指令」（6-2；已改第一行是明列例外）；6-2b" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,432,420,73"/>
<mxCell id="te_r6c3" value="pull 失敗；git merge-file I/O 錯誤；寫入失敗（工具層 version.toml 不動）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,432,260,73"/>
<mxCell id="te_r6c4" value="合併衝突（留標記、baseline 仍推）；合併結果 TOML／just 解析失敗（留原檔、baseline 不推）；(0) 仍有衝突標記" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1140,432,240,73"/>
<mxCell id="te_r6c5" value="@&amp;lt;舊版&amp;gt; 無法無損讀（6-10）；6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,432,210,73"/>
<mxCell id="te_r7c0" value="dev &amp;lt;repo&amp;gt;／vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="40,505,170,57"/>
<mxCell id="te_r7c1" value="覆寫寫入 version.local.toml" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,505,250,57"/>
<mxCell id="te_r7c2" value="工具不在 version.toml；缺 &amp;lt;dir&amp;gt;/dist/init.toml；CI 拒絕；-p／-i 互斥用錯" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,505,420,57"/>
<mxCell id="te_r7c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="880,505,260,57"/>
<mxCell id="te_r7c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,505,240,57"/>
<mxCell id="te_r7c5" value="6-18／6-19；-i 舊引擎 P／schema 低於薄殼首行且要重產 tracked 薄殼 → 拒絕" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,505,210,57"/>
<mxCell id="te_r8c0" value="undev &amp;lt;repo&amp;gt;／vendor_kit" style="fillColor=#ffffff;strokeColor=#999999" geo="40,562,170,42"/>
<mxCell id="te_r8c1" value="完成；未啟用 → 提示" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,562,250,42"/>
<mxCell id="te_r8c2" value="指紋不同" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,562,420,42"/>
<mxCell id="te_r8c3" value="重新 materialize 失敗（保留可恢復狀態）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,562,260,42"/>
<mxCell id="te_r8c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,562,240,42"/>
<mxCell id="te_r8c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,562,210,42"/>
<mxCell id="te_r9c0" value="sync [&amp;lt;repo&amp;gt;] [--verify]" style="fillColor=#ffffff;strokeColor=#999999" geo="40,604,170,42"/>
<mxCell id="te_r9c1" value="快路徑（不起容器）；materialize／verify 完成" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,604,250,42"/>
<mxCell id="te_r9c2" value="薄殼不符（6-1，不重寫）；未完成接入（6-13）；CI 下 baseline 落後（6-5）；CI 下任何 local 覆寫；未完成交易（6-33）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,604,420,42"/>
<mxCell id="te_r9c3" value="pull 失敗／逾時；verify 失敗且重裝失敗" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,604,260,42"/>
<mxCell id="te_r9c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,604,240,42"/>
<mxCell id="te_r9c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,604,210,42"/>
<mxCell id="te_r10c0" value="prune" style="fillColor=#ffffff;strokeColor=#999999" geo="40,646,170,42"/>
<mxCell id="te_r10c1" value="完成（印刪了什麼、保留什麼；活躍 .tmp.* 只列出）；dry-run 零刪除" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,646,250,42"/>
<mxCell id="te_r10c2" value="vk-resolve 不合（6-30）；無 tty 需問（6-4）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,646,420,42"/>
<mxCell id="te_r10c3" value="任一 docker rm／image rm／network rm／volume rm 失敗（摘要全列）" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,646,260,42"/>
<mxCell id="te_r10c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,646,240,42"/>
<mxCell id="te_r10c5" value="6-18／6-19" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,646,210,42"/>
<mxCell id="te_r11c0" value="help／h" style="fillColor=#ffffff;strokeColor=#999999" geo="40,688,170,57"/>
<mxCell id="te_r11c1" value="印說明（不觸網、不安裝）" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,688,250,57"/>
<mxCell id="te_r11c2" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="460,688,420,57"/>
<mxCell id="te_r11c3" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="880,688,260,57"/>
<mxCell id="te_r11c4" value="—" style="fillColor=#ffffff;strokeColor=#999999" geo="1140,688,240,57"/>
<mxCell id="te_r11c5" value="P &amp;lt; floor → 3 + 6-18（零寫入；任何動詞含 help、救援路徑皆同）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,688,210,57"/>
<mxCell id="te_r12c0" value="ci/check.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="40,745,170,42"/>
<mxCell id="te_r12c1" value="⓪～⑤ 全過" style="fillColor=#d5e8d4;strokeColor=#999999" geo="210,745,250,42"/>
<mxCell id="te_r12c2" value="⓪ version.local.toml 被 track；① sync 的 1；② verify 印記不符；③ upgrade --dry-run 需改 tracked 檔（印清單）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="460,745,420,42"/>
<mxCell id="te_r12c3" value="④⑤ 工具／專案測試原碼傳出" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,745,260,42"/>
<mxCell id="te_r12c4" value="③ 仍有衝突標記" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1140,745,240,42"/>
<mxCell id="te_r12c5" value="① 的 3（P &amp;lt; floor 6-18／6-19）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="1380,745,210,42"/>
<mxCell id="k14a" value="多工具彙總（已定，Q27）：不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）→ 做得完的做完 → 最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="40,811,500,57"/>
<mxCell id="k14b" value="結束碼 3 邊界（已定，Q23、v2.7-4）：版本／協定／schema 不合，須先升級或退回才能繼續；P &amp;lt; floor → 任何動詞（含 help、救援路徑）都回 3 + 6-18；回 3 時零寫入、無任何例外；新舊以 P／schema 比較，不用版本字串；floor 檢查先於任何上網；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1（印記不符、薄殼被改、自身升級完成要重跑）維持 1" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="560,811,520,88"/>
<mxCell id="k14c" value="CI 對應動作（已定）：0 → 過（merge）；1 → 修（照訊息裡的指令：本機 upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push／add／undev／git checkout 還原薄殼／加 -y／設 token）；2 → 解衝突（編輯檔案去掉 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記 → 重跑 upgrade 直到乾淨）；3 → 換版本（upgrade vendor_kit／git revert／bootstrap.sh 重建）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="1100,811,490,88"/>
<mxCell id="k14d" value="圖上顏色對應（v2.6-15、v2.7-8）：0 = 綠橢圓；1 需要人動作（印指令：請先 undev／請先 add／請先 git init／請重跑／請 upgrade vendor_kit／請設 token 或指定 @&amp;lt;tag&amp;gt;）= 橙橢圓；2 = 橙；3 = 橙；1 失敗（拉不到、寫入失敗、驗證失敗）= 紅橢圓" style="fillColor=#ffffff;strokeColor=#999999" geo="40,915,500,73"/>
<mxCell id="k14e" value="check.sh 整體結束碼 = 第一個失敗步驟的碼：⓪ local 被 track → 1；① sync 1／3；② verify 1；③ upgrade --dry-run：需改 tracked → 1、仍有衝突標記 → 2；④⑤ 原碼傳出（1／2／3 語意只對 vendor_kit 自身步驟成立）；⓪–⑤ 六步、一關過才下一關" style="fillColor=#ffffff;strokeColor=#999999" geo="560,915,520,57"/>
<mxCell id="k14f" value="「—」= 該動詞沒有這個結束碼；表內 6-N = interface_spec §6 逐字訊息編號；dry-run 在本機一律 0（CI 為真且需改 tracked 檔 → 1）；EOF／Ctrl-C 中止 apply → 1、不套用、不記 declined；sync --verify（F5 已定）= 每檔 sha256 全驗，結束碼同 sync" style="fillColor=#ffffff;strokeColor=#999999" geo="1100,915,490,73"/>
<mxCell id="p14_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1018,200,60"/>
<mxCell id="p14_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1018,140,64"/>
<mxCell id="p14_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1026,140,44"/>
<mxCell id="p14_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1020,190,56"/>
<mxCell id="p14_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1020,210,56"/>
<mxCell id="p14_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1028,88,40"/>
<mxCell id="p14_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1028,170,40"/>
<mxCell id="p14_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1018,280,60"/>
<mxCell id="p14_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1086,120,36"/>
<mxCell id="p14_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1086,150,36"/>
<mxCell id="p14_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="350,1086,170,36"/>
<mxCell id="p14_lgx_c0" value="綠格：結束碼 0" style="fillColor=#d5e8d4;strokeColor=#999999" geo="540,1086,110,36"/>
<mxCell id="p14_lgx_cx" value="橙格：需要人動作（1／2／3）" style="fillColor=#ffe6cc;strokeColor=#999999" geo="670,1086,190,36"/>
<mxCell id="p14_lgx_c1" value="紅格：失敗 1" style="fillColor=#f8cecc;strokeColor=#999999" geo="880,1086,110,36"/>
<mxCell id="p14_lgx_cell" value="白格：表格內容" style="fillColor=#ffffff;strokeColor=#999999" geo="1010,1086,110,36"/>
<mxCell id="p14_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1124,200,28"/>
<mxCell id="p14_tk0" value="結束碼 0" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1158,150,40"/>
<mxCell id="p14_tv0" value="成功（含 warn）：add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符、update 已列出（有新版也 0）、dry-run 本機皆 0 + 提示" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1158,610,40"/>
<mxCell id="p14_tk1" value="結束碼 1" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1198,150,55"/>
<mxCell id="p14_tv1" value="一般失敗或需使用者處理／重跑：工具層動詞回 1 時 version.toml 不動；例外：自身升級已改第一行後回 1、upgrade vendor_kit 重產薄殼後回 1（6-2）；圖上：印指令要人動作 = 橙、拉不到／寫入失敗／驗證失敗 = 紅" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1198,610,55"/>
<mxCell id="p14_tk2" value="結束碼 2" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1253,150,55"/>
<mxCell id="p14_tv2" value="合併衝突（留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版；解完重跑直到乾淨）；合併結果 TOML／just 解析失敗 → 2 留原檔、dest 入 conflicts、baseline 不推；update --exit-code 有新版 → 2" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1253,610,55"/>
<mxCell id="p14_tk3" value="結束碼 3（Q23）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1308,150,71"/>
<mxCell id="p14_tv3" value="現有薄殼／檔案／引擎的組合需先升級或退回：(a) P &amp;lt; floor 6-18 (b) schema 高於支援 6-19 (c) 降版無法無損讀 6-10 (d) dev -i 舊引擎要重產薄殼 (e) 舊薄殼跑新 major 一般動詞 6-36；任何動詞（含 help、救援路徑）在 P &amp;lt; floor 都回 3 + 6-18（v2.9-7）；零寫入、無任何例外；以 P／schema 比" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1308,610,71"/>
<mxCell id="p14_tk4" value="多工具彙總（Q27）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1379,150,40"/>
<mxCell id="p14_tv4" value="不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）、做得完的做完，最後回最需要處理的碼：1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1379,610,40"/>
<mxCell id="p14_tk5" value="check.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1158,150,55"/>
<mxCell id="p14_tv5" value=".vendor_kit/ci/check.sh：export CI=1 → ⓪ local 被 track → 1 → ① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；⓪–⑤ 六步、一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（④⑤ 原碼傳出）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1158,610,55"/>
<mxCell id="p14_tk6" value="frozen（CI 為真）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1213,150,40"/>
<mxCell id="p14_tv6" value="CI 非空且不為 0／false → 不寫 tracked 檔、不查最新版；需改 tracked 檔 → 1 印清單（與 -y 無關）；6-6～6-8 提醒不紅燈；update 不受限" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1213,610,40"/>
<mxCell id="p14_tk7" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1253,150,55"/>
<mxCell id="p14_tv7" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1253,610,55"/>
<mxCell id="p14_tk8" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1308,150,71"/>
<mxCell id="p14_tv8" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1308,610,71"/>
</diagram>
<diagram id="v1p15" name="流程 v2：vendor_kit release（1）build 與驗收">
<mxCell id="title" value="流程 v2：vendor_kit release（1）── build → release-test → 驗收（#26／#27、§7.4）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,116"/>
<mxCell id="hdr0" value="維護者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,136,220,28"/>
<mxCell id="hdr1" value="GitHub Actions" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,136,560,28"/>
<mxCell id="hdr2" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="860,136,320,28"/>
<mxCell id="hdr3" value="Release 資產" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1200,136,390,28"/>
<mxCell id="bR" value="release vN（1）：兩平台各自 build → release-test → 驗收 → 兩平台一致檢查 → 全部通過？否 → 候選作廢；是 → 接（2）頁推 image 與資產" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,180,1590,991"/>
<mxCell id="bR_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bR" geo="1546,5,30,20"/>
<mxCell id="v0" value="推候選（候選 tag／workflow_dispatch 指定 vN）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bR" geo="20,36,220,80"/>
<mxCell id="v1" value="workflow 觸發：amd64 job + arm64 job（原生 runner）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,56,560,40"/>
<mxCell id="v2" value="build（#26）：兩 runner 各自單平台 buildx build（同一份 Dockerfile；LABEL =1／.protocol／.schema）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,136,560,42"/>
<mxCell id="v3a" value="release-test（各平台原生）：env-test" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,199,560,40"/>
<mxCell id="v3n" value="release-test 矩陣：rootless docker、Podman；just 1.33.0 + latest；不用 QEMU 當閘門" style="fillColor=#ffffff;strokeColor=#999999" parent="bR" geo="1180,198,390,42"/>
<mxCell id="v3b" value="release-test：完整主機流程 install → add → upgrade → dev/undev → remove → prune → uninstall" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,260,560,42"/>
<mxCell id="v4a" value="驗收（§7.4-1）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,322,560,40"/>
<mxCell id="v4g" value="已釋出引擎 image r（floor 以來每一版；永不刪）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bR" geo="840,322,320,40"/>
<mxCell id="v4r" value="已釋出 bootstrap.sh(r)（Release 資產；永不刪）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR" geo="1180,322,390,40"/>
<mxCell id="v4b" value="fixture 的 version.toml 第一行改成候選 C" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,382,560,40"/>
<mxCell id="v4c" value="跑 §7.4-1 序列：sync 1+6-1 → upgrade vendor_kit 1+6-2 → sync 0 → 第二次 upgrade vendor_kit 0" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,442,560,42"/>
<mxCell id="v5a" value="驗收（§7.4-4～8）：連升 r_i → r_j → C；floor 直接跳升；降版；&amp;lt; floor synthetic；舊引擎讀新檔 3" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,504,560,42"/>
<mxCell id="v5b" value="驗收（§7.4-3、9～13）：升級後 == 全新安裝；fresh clone 無 gen；frozen sync；中斷重跑；TOML 異常" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,566,560,42"/>
<mxCell id="v5c" value="驗收（§7.4-16／17）：離線包 amd64／arm64、斷網可用；禁止由候選樹複製 fixture、禁 stub 引擎" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,628,560,42"/>
<mxCell id="v6a" value="兩平台一致檢查：工具 dist 逐檔位元組一致" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,706,560,40"/>
<mxCell id="v6n" value="已定（decisions/multiarch）：不能靠單一 bake --push 帶測試就宣稱「失敗就不發佈」；分架構各自 build／test，綠了才 push-by-digest，最後由單一 job 合成 index；兩 runner 各自 push 同 tag 會互相覆蓋" style="fillColor=#ffffff;strokeColor=#999999" parent="bR" geo="1180,690,390,73"/>
<mxCell id="v6b" value="兩平台一致檢查：引擎 image 兩平台 LABEL（protocol／schema）一致" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR" geo="260,783,560,40"/>
<mxCell id="v7x" value="否 → 失敗：不推 image、不發 Release、不進正式 tag（候選作廢）" style="fillColor=#f8cecc;strokeColor=#000000" parent="bR" geo="20,843,220,80"/>
<mxCell id="v7" value="全部通過？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bR" geo="260,858,220,50"/>
<mxCell id="v7z" value="是 ↓ 續「release（2）」頁：push-by-digest → index → bootstrap.sh／tar／.digest → Release" style="fillColor=none;strokeColor=none" parent="bR" geo="260,943,560,42"/>
<mxCell id="ve0" edge="1" source="v0" target="v1"/>
<mxCell id="ve1" edge="1" source="v1" target="v2"/>
<mxCell id="ve2" edge="1" source="v2" target="v3a"/>
<mxCell id="ve2n" edge="1" source="v3a" target="v3n"/>
<mxCell id="ve2b" edge="1" source="v3a" target="v3b"/>
<mxCell id="ve3" edge="1" source="v3b" target="v4a"/>
<mxCell id="ve4" value="拉" edge="1" source="v4a" target="v4g"/>
<mxCell id="ve4r" value="取" edge="1" source="v4g" target="v4r"/>
<mxCell id="ve4b" edge="1" source="v4a" target="v4b"/>
<mxCell id="ve4c" edge="1" source="v4b" target="v4c"/>
<mxCell id="ve5" edge="1" source="v4c" target="v5a"/>
<mxCell id="ve5b" edge="1" source="v5a" target="v5b"/>
<mxCell id="ve5c" edge="1" source="v5b" target="v5c"/>
<mxCell id="ve6" edge="1" source="v5c" target="v6a"/>
<mxCell id="ve6n" edge="1" source="v6a" target="v6n"/>
<mxCell id="ve6b" edge="1" source="v6a" target="v6b"/>
<mxCell id="ve7" edge="1" source="v6b" target="v7"/>
<mxCell id="ve8" value="否" edge="1" source="v7" target="v7x"/>
<mxCell id="ve9" value="是" edge="1" source="v7" target="v7z"/>
<mxCell id="p15_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1187,200,60"/>
<mxCell id="p15_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1187,140,64"/>
<mxCell id="p15_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1195,140,44"/>
<mxCell id="p15_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1189,190,56"/>
<mxCell id="p15_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1189,210,56"/>
<mxCell id="p15_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1197,88,40"/>
<mxCell id="p15_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1197,170,40"/>
<mxCell id="p15_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1187,280,60"/>
<mxCell id="p15_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1255,120,36"/>
<mxCell id="p15_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1255,150,36"/>
<mxCell id="p15_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="350,1255,170,36"/>
<mxCell id="p15_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="540,1255,170,36"/>
<mxCell id="p15_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1293,200,28"/>
<mxCell id="p15_tk0" value="release" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1327,150,40"/>
<mxCell id="p15_tv0" value="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1327,610,40"/>
<mxCell id="p15_tk1" value="多架構 image／index digest（#26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1367,150,71"/>
<mxCell id="p15_tv1" value="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1367,610,71"/>
<mxCell id="p15_tk2" value="release-test" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1438,150,55"/>
<mxCell id="p15_tv2" value="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1438,610,55"/>
<mxCell id="p15_tk3" value="env-test" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1493,150,40"/>
<mxCell id="p15_tv3" value="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1493,610,40"/>
<mxCell id="p15_tk4" value="驗收（§7.4）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1533,150,71"/>
<mxCell id="p15_tv4" value="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&amp;lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1533,610,71"/>
<mxCell id="p15_tk5" value="兩平台一致檢查" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1604,150,40"/>
<mxCell id="p15_tv5" value="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1604,610,40"/>
<mxCell id="p15_tk6" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1327,150,71"/>
<mxCell id="p15_tv6" value="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &amp;lt;tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1327,610,71"/>
<mxCell id="p15_tk7" value="tar／.digest／SHA256SUMS（#27、Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1398,150,55"/>
<mxCell id="p15_tv7" value="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1398,610,55"/>
<mxCell id="p15_tk8" value="LABEL" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1453,150,40"/>
<mxCell id="p15_tv8" value="引擎 image build 時帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1453,610,40"/>
<mxCell id="p15_tk9" value="SemVer" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1493,150,40"/>
<mxCell id="p15_tv9" value="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1493,610,40"/>
<mxCell id="p15_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1533,150,71"/>
<mxCell id="p15_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1533,610,71"/>
</diagram>
<diagram id="v1p15c" name="流程 v2：vendor_kit release（2）推 image 與資產">
<mxCell id="title" value="流程 v2：vendor_kit release（2）── 推 image → 資產 → Release（#26／#27、Q26）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,116"/>
<mxCell id="hdr0" value="維護者" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,136,220,28"/>
<mxCell id="hdr1" value="GitHub Actions" style="fillColor=#e6e6e6;strokeColor=#999999" geo="280,136,560,28"/>
<mxCell id="hdr2" value="GHCR" style="fillColor=#e6e6e6;strokeColor=#999999" geo="860,136,320,28"/>
<mxCell id="hdr3" value="Release 資產" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1200,136,390,28"/>
<mxCell id="bR2" value="release vN（2）：全過才 push-by-digest → 單一 job 合成 index → 產 bootstrap.sh → tar + .digest → 離線包 → SHA256SUMS → 打正式 tag → 發布 Release" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,180,1590,870"/>
<mxCell id="bR2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bR2" geo="1546,5,30,20"/>
<mxCell id="v8e" value="來自「release（1）」頁：build／release-test／驗收／兩平台一致全部通過" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bR2" geo="260,36,560,58"/>
<mxCell id="v8a" value="兩平台各自 push-by-digest（不打 tag；tag vN 不覆蓋）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,115,560,40"/>
<mxCell id="v8ag" value="ghcr.io/&amp;lt;org&amp;gt;/vendor_kit@sha256:&amp;lt;amd64 digest&amp;gt;、@sha256:&amp;lt;arm64 digest&amp;gt;" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bR2" geo="840,114,320,42"/>
<mxCell id="v8b" value="單一 job：docker buildx imagetools create -t vendor_kit:vN &amp;lt;兩個 digest&amp;gt; → 合成 index" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,176,560,42"/>
<mxCell id="v8bg" value="ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;（多架構；公開）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bR2" geo="840,176,320,42"/>
<mxCell id="v8c" value="imagetools inspect 斷言：index 含 linux/amd64 + linux/arm64" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,238,560,40"/>
<mxCell id="v9" value="產 bootstrap.sh：內嵌完整引擎 ref（tag@index digest）；檔名固定" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,299,560,40"/>
<mxCell id="v9r" value="bootstrap.sh（releases/download/vN/；latest 連結指向最新）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR2" geo="1180,298,390,42"/>
<mxCell id="v10a" value="docker save 各平台 image → vendor_kit-vN-amd64.tar、vendor_kit-vN-arm64.tar" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,360,560,40"/>
<mxCell id="v10ar" value="vendor_kit-vN-&amp;lt;平台&amp;gt;.tar（各平台一個）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR2" geo="1180,360,390,40"/>
<mxCell id="v10b" value="寫同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = index digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,420,560,40"/>
<mxCell id="v10br" value="vendor_kit-vN-&amp;lt;平台&amp;gt;.tar.digest" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR2" geo="1180,420,390,40"/>
<mxCell id="v10c" value="組離線包 vendor_kit-vN-local.tar.gz" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,531,560,40"/>
<mxCell id="v10cr" value="離線包內容" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR2" geo="1180,480,390,142"/>
<mxCell id="v10cr_0" value="bootstrap.sh（契約入口：bootstrap.sh --local &amp;lt;tar&amp;gt;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="v10cr" geo="8,26,374,26"/>
<mxCell id="v10cr_1" value="各平台 tar + .tar.digest" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="v10cr" geo="8,58,374,26"/>
<mxCell id="v10cr_2" value="local_bootstrap.sh：便利包裝（非契約；偵測架構、挑 tar、exec bootstrap.sh --local）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="v10cr" geo="8,90,374,42"/>
<mxCell id="v10d" value="寫 SHA256SUMS（列所有資產）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,642,560,40"/>
<mxCell id="v10dr" value="SHA256SUMS" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bR2" geo="1180,642,390,40"/>
<mxCell id="v11a" value="打正式 tag vN（指向候選 commit）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,702,560,40"/>
<mxCell id="v11b" value="發布 Release vN：附 bootstrap.sh、tar、.digest、離線包、SHA256SUMS；release notes 含 index digest 與不用腳本的替代 docker run 指令" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bR2" geo="260,762,560,42"/>
<mxCell id="v11n" value="已釋出 image／Release 資產／fixture 永不刪；下游 Renovate 會看到新 tag@digest" style="fillColor=#ffffff;strokeColor=#999999" parent="bR2" geo="1180,762,390,42"/>
<mxCell id="v12" value="0：Release vN 發布" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bR2" geo="20,824,220,40"/>
<mxCell id="ve10" edge="1" source="v8e" target="v8a"/>
<mxCell id="ve10g" value="推" edge="1" source="v8a" target="v8ag"/>
<mxCell id="ve11" edge="1" source="v8a" target="v8b"/>
<mxCell id="ve11g" value="建" edge="1" source="v8b" target="v8bg"/>
<mxCell id="ve11c" edge="1" source="v8b" target="v8c"/>
<mxCell id="ve12" edge="1" source="v8c" target="v9"/>
<mxCell id="ve12r" value="產" edge="1" source="v9" target="v9r"/>
<mxCell id="ve13" edge="1" source="v9" target="v10a"/>
<mxCell id="ve13r" value="產" edge="1" source="v10a" target="v10ar"/>
<mxCell id="ve13b" edge="1" source="v10a" target="v10b"/>
<mxCell id="ve13br" value="寫" edge="1" source="v10b" target="v10br"/>
<mxCell id="ve13c" edge="1" source="v10b" target="v10c"/>
<mxCell id="ve13cr" value="組" edge="1" source="v10c" target="v10cr"/>
<mxCell id="ve13d" edge="1" source="v10c" target="v10d"/>
<mxCell id="ve13dr" value="寫" edge="1" source="v10d" target="v10dr"/>
<mxCell id="ve14" edge="1" source="v10d" target="v11a"/>
<mxCell id="ve15" edge="1" source="v11a" target="v11b"/>
<mxCell id="ve15n" edge="1" source="v11b" target="v11n"/>
<mxCell id="ve16" edge="1" source="v11b" target="v12"/>
<mxCell id="p15c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1066,200,60"/>
<mxCell id="p15c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1066,140,64"/>
<mxCell id="p15c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1074,140,44"/>
<mxCell id="p15c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1068,190,56"/>
<mxCell id="p15c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1068,210,56"/>
<mxCell id="p15c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1076,88,40"/>
<mxCell id="p15c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1076,170,40"/>
<mxCell id="p15c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1066,280,60"/>
<mxCell id="p15c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1134,120,36"/>
<mxCell id="p15c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="180,1134,170,36"/>
<mxCell id="p15c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="370,1134,170,36"/>
<mxCell id="p15c_lgx_entry" value="虛線橢圓：來自其他頁" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="560,1134,200,36"/>
<mxCell id="p15c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1172,200,28"/>
<mxCell id="p15c_tk0" value="release" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1206,150,40"/>
<mxCell id="p15c_tv0" value="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1206,610,40"/>
<mxCell id="p15c_tk1" value="多架構 image／index digest（#26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1246,150,71"/>
<mxCell id="p15c_tv1" value="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1246,610,71"/>
<mxCell id="p15c_tk2" value="release-test" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1317,150,55"/>
<mxCell id="p15c_tv2" value="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1317,610,55"/>
<mxCell id="p15c_tk3" value="env-test" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1372,150,40"/>
<mxCell id="p15c_tv3" value="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1372,610,40"/>
<mxCell id="p15c_tk4" value="驗收（§7.4）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1412,150,71"/>
<mxCell id="p15c_tv4" value="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&amp;lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1412,610,71"/>
<mxCell id="p15c_tk5" value="兩平台一致檢查" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1483,150,40"/>
<mxCell id="p15c_tv5" value="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1483,610,40"/>
<mxCell id="p15c_tk6" value="bootstrap.sh" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1206,150,71"/>
<mxCell id="p15c_tv6" value="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &amp;lt;tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1206,610,71"/>
<mxCell id="p15c_tk7" value="tar／.digest／SHA256SUMS（#27、Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1277,150,55"/>
<mxCell id="p15c_tv7" value="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1277,610,55"/>
<mxCell id="p15c_tk8" value="LABEL" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1332,150,40"/>
<mxCell id="p15c_tv8" value="引擎 image build 時帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1332,610,40"/>
<mxCell id="p15c_tk9" value="SemVer" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1372,150,40"/>
<mxCell id="p15c_tv9" value="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1372,610,40"/>
<mxCell id="p15c_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1412,150,71"/>
<mxCell id="p15c_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1412,610,71"/>
</diagram>
<diagram id="v1p16" name="流程 v2：離線包（1）bootstrap.sh --local">
<mxCell id="title" value="流程 v2：離線包（1）── bootstrap.sh --local &amp;lt;引擎 tar&amp;gt; → load → install（#27、Q26、§4.8）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &amp;lt;repo&amp;gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,163"/>
<mxCell id="hdr0" value="使用者（離線機）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,183,230,28"/>
<mxCell id="hdr1" value="bootstrap.sh（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="290,183,400,28"/>
<mxCell id="hdr2" value="docker daemon" style="fillColor=#e6e6e6;strokeColor=#999999" geo="710,183,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,183,320,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1310,183,280,28"/>
<mxCell id="bO1" value="離線接入（1）只涉及引擎：離線包 → bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（契約入口）→ 前置檢查（不分 tar／tag）→ 判別值三分支 → tar 形 load + 讀 .digest（tag 形跳過）→ image ID → install → version.local.toml" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,227,1590,1640"/>
<mxCell id="bO1_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bO1" geo="1546,5,30,20"/>
<mxCell id="o0" value="有網路的機器下載 vendor_kit-vN-local.tar.gz（SHA256SUMS 驗）→ 帶到離線機" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bO1" geo="-9,36,288,102"/>
<mxCell id="o1" value="解開：bootstrap.sh、各平台引擎 tar + .tar.digest（另附 local_bootstrap.sh）；不含工具 tar" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="20,154,230,73"/>
<mxCell id="o1w" value="【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：" style="fillColor=none;strokeColor=none" parent="bO1" geo="20,243,230,57"/>
<mxCell id="o1a" value="docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="20,316,230,57"/>
<mxCell id="o1b" value="挑該平台的引擎 tar（vendor_kit-vN-&amp;lt;arch&amp;gt;.tar）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="20,389,230,42"/>
<mxCell id="o1c" value="exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="20,447,230,42"/>
<mxCell id="o2" value="sh bootstrap.sh --local &amp;lt;引擎 tar&amp;gt; [-y]（契約入口；-t &amp;lt;repo&amp;gt; 走 registry 需網路，離線機不帶）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="20,505,230,57"/>
<mxCell id="o2l" value="↓ 前置檢查（v2.9-1：不分 --local 值是 tar 還是 tag，一律先做）" style="fillColor=none;strokeColor=none" parent="bO1" geo="270,512,400,42"/>
<mxCell id="o5x" value="否 → 1 + 6-16：請先 git init" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bO1" geo="20,578,230,58"/>
<mxCell id="o5" value="在 git repo 內？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="270,582,300,50"/>
<mxCell id="o6x" value="否 → 1 + 6-23：請裝 GitHub release 版 just" style="fillColor=#ffe6cc;strokeColor=#000000" parent="bO1" geo="20,652,230,80"/>
<mxCell id="o6" value="just ≥ 1.33.0？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="270,667,300,50"/>
<mxCell id="o3" value="--local 值含 / 或以 .tar 結尾？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="270,775,300,81"/>
<mxCell id="o3n" value="已定（B1；grilling 2026-09-19 末條、v2.7-2、v2.8-4、v2.9-1）三分支：值含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load；其餘 → image tag（不 load、不讀 .digest）；既存檔且可解讀為 tag → 1 + 6-37 消歧（請寫 ./&amp;lt;v&amp;gt; 或完整 ref）；前置檢查（git repo／just）不分型別一律先做" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bO1" geo="1290,748,280,135"/>
<mxCell id="o3bx" value="否 → 1：檔案路徑必須存在" style="fillColor=#f8cecc;strokeColor=#000000" parent="bO1" geo="20,910,230,58"/>
<mxCell id="o3b" value="該路徑的檔案存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="300,899,240,81"/>
<mxCell id="o3t" value="否 → tag 形：不 load、不讀 .digest（本機須已有該 image）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="550,903,120,73"/>
<mxCell id="o3cx" value="是 → 1 + 6-37：值歧義（既存檔也像 tag），請寫 ./&amp;lt;v&amp;gt; 或完整 ref" style="fillColor=#f8cecc;strokeColor=#000000" parent="bO1" geo="20,996,230,80"/>
<mxCell id="o3c" value="值同時可解讀為 image tag？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="270,996,300,81"/>
<mxCell id="o4x" value="否 → 1：同名 .tar.digest 旁檔缺" style="fillColor=#f8cecc;strokeColor=#000000" parent="bO1" geo="20,1104,230,58"/>
<mxCell id="o4" value="同名 .tar.digest 存在？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO1" geo="270,1093,300,81"/>
<mxCell id="o6c" value="docker load &amp;lt; &amp;lt;引擎 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="270,1198,300,40"/>
<mxCell id="o6d" value="本機 image vendor_kit:vN（只有 tag、無 RepoDigests）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bO1" geo="690,1190,170,57"/>
<mxCell id="o7a" value="讀 &amp;lt;tar&amp;gt;.digest → 正式 index digest" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="270,1263,300,40"/>
<mxCell id="o7b" value="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID（tag 形由此匯入：跳過 load 與 .digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="270,1319,400,42"/>
<mxCell id="o7bd" value="回 image ID（sha256:&amp;lt;hex64&amp;gt;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="690,1319,170,42"/>
<mxCell id="o8" value="docker run 本機 image install（本機有 → 不 pull）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="270,1428,400,40"/>
<mxCell id="o8e" value="install：建薄殼四檔、gen/.stamp、baseline/.gitkeep；version.toml 第一行 = 正式 ref@digest（tar 形來自 .digest；tag 形用既有 version.toml 值）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO1" geo="950,1411,320,73"/>
<mxCell id="o8f" value="install 寫" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bO1" geo="1290,1377,280,141"/>
<mxCell id="o8f_0" value="version.toml 第一行（正式 ref@sha256:&amp;lt;index digest&amp;gt;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="o8f" geo="8,26,264,42"/>
<mxCell id="o8f_1" value="薄殼四檔、gen/.stamp、baseline/.gitkeep、根 justfile 一行、.dockerignore 三行" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="o8f" geo="8,74,264,57"/>
<mxCell id="o9" value="install 成功後寫 version.local.toml：vendor_kit = &quot;vendor_kit:vN&quot; + vendor_kit_image_id（失敗清除）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1" geo="270,1534,400,42"/>
<mxCell id="o9f" value="version.local.toml（不進 git）：本機 tag + image ID" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bO1" geo="1290,1534,280,42"/>
<mxCell id="o9z" value="↓ 續「離線包（2）」頁：工具由使用者另備工具 tar，逐一 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；之後斷網 sync" style="fillColor=none;strokeColor=none" parent="bO1" geo="270,1592,400,42"/>
<mxCell id="oe0" edge="1" source="o0" target="o1"/>
<mxCell id="oe1" edge="1" source="o1" target="o1w"/>
<mxCell id="oe1a" edge="1" source="o1w" target="o1a"/>
<mxCell id="oe1b" edge="1" source="o1a" target="o1b"/>
<mxCell id="oe1c" edge="1" source="o1b" target="o1c"/>
<mxCell id="oe1w" edge="1" source="o1c" target="o2"/>
<mxCell id="oe2" edge="1" source="o2" target="o2l"/>
<mxCell id="oe2l" edge="1" source="o2l" target="o5"/>
<mxCell id="oe6x" value="否" edge="1" source="o5" target="o5x"/>
<mxCell id="oe6b" value="是" edge="1" source="o5" target="o6"/>
<mxCell id="oe6bx" value="否" edge="1" source="o6" target="o6x"/>
<mxCell id="oe6c" value="是" edge="1" source="o6" target="o3"/>
<mxCell id="oe3t" value="否" edge="1" source="o3" target="o3t"/>
<mxCell id="oe3b" value="是" edge="1" source="o3" target="o3b"/>
<mxCell id="oe3bx" value="否" edge="1" source="o3b" target="o3bx"/>
<mxCell id="oe3c" value="是" edge="1" source="o3b" target="o3c"/>
<mxCell id="oe3cx" value="是" edge="1" source="o3c" target="o3cx"/>
<mxCell id="oe4" value="否" edge="1" source="o3c" target="o4"/>
<mxCell id="oe5" value="否" edge="1" source="o4" target="o4x"/>
<mxCell id="oe7" value="是" edge="1" source="o4" target="o6c"/>
<mxCell id="oe8" value="載" edge="1" source="o6c" target="o6d"/>
<mxCell id="oe9" edge="1" source="o6c" target="o7a"/>
<mxCell id="oe9b" edge="1" source="o7a" target="o7b"/>
<mxCell id="oe9d" edge="1" source="o7b" target="o7bd"/>
<mxCell id="oe10" edge="1" source="o7b" target="o8"/>
<mxCell id="oe3tj" value="tag 形：跳過 load／.digest" edge="1" source="o3t" target="o7b"/>
<mxCell id="oe11" edge="1" source="o8" target="o8e"/>
<mxCell id="oe12" value="寫" edge="1" source="o8e" target="o8f"/>
<mxCell id="oe13" edge="1" source="o8" target="o9"/>
<mxCell id="oe14" value="寫" edge="1" source="o9" target="o9f"/>
<mxCell id="oe15" edge="1" source="o9" target="o9z"/>
<mxCell id="p16_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1883,200,60"/>
<mxCell id="p16_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1883,140,64"/>
<mxCell id="p16_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1891,140,44"/>
<mxCell id="p16_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1885,190,56"/>
<mxCell id="p16_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1885,210,56"/>
<mxCell id="p16_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1893,88,40"/>
<mxCell id="p16_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1893,170,40"/>
<mxCell id="p16_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1883,280,60"/>
<mxCell id="p16_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1951,120,36"/>
<mxCell id="p16_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1951,150,36"/>
<mxCell id="p16_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1951,190,36"/>
<mxCell id="p16_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1951,170,36"/>
<mxCell id="p16_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1951,170,36"/>
<mxCell id="p16_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1989,200,28"/>
<mxCell id="p16_tk0" value="離線包（#27、Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2023,150,55"/>
<mxCell id="p16_tv0" value="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2023,610,55"/>
<mxCell id="p16_tk1" value="bootstrap.sh --local（契約入口）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2078,150,102"/>
<mxCell id="p16_tv1" value="離線接入的契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &amp;lt;repo&amp;gt; 仍是 add &amp;lt;repo&amp;gt;[@tag]，走 registry、需網路，離線機不帶 -t；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load + 讀 .digest；其餘 → image tag（不 load、不讀 .digest，只 inspect image ID）；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&amp;lt;v&amp;gt; 或完整 ref」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2078,610,102"/>
<mxCell id="p16_tk2" value="工具 tar（來源，v2.8-5）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2180,150,71"/>
<mxCell id="p16_tv2" value="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &amp;lt;repo&amp;gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&amp;lt;hex64&amp;gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2180,610,71"/>
<mxCell id="p16_tk3" value="local_bootstrap.sh（便利包裝，非契約）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2251,150,55"/>
<mxCell id="p16_tv3" value="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2251,610,55"/>
<mxCell id="p16_tk4" value=".digest 旁檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2306,150,40"/>
<mxCell id="p16_tv4" value="&amp;lt;name&amp;gt;.tar.digest 一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2306,610,40"/>
<mxCell id="p16_tk5" value="image ID／local_image_id" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2023,150,55"/>
<mxCell id="p16_tv5" value="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2023,610,55"/>
<mxCell id="p16_tk6" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2078,150,40"/>
<mxCell id="p16_tv6" value="不進 git；--local 時寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2078,610,40"/>
<mxCell id="p16_tk7" value="離線可用（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2118,150,55"/>
<mxCell id="p16_tv7" value="啟動器一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2118,610,55"/>
<mxCell id="p16_tk8" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2173,150,55"/>
<mxCell id="p16_tv8" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2173,610,55"/>
<mxCell id="p16_tk9" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2228,150,71"/>
<mxCell id="p16_tv9" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2228,610,71"/>
</diagram>
<diagram id="v1p16c" name="流程 v2：離線包（2）add --local 與斷網 sync">
<mxCell id="title" value="流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具 → 斷網 sync（Q26、§4.8、§7.4-17）" style="fontSize=18" geo="40,20,1000,34"/>
<mxCell id="pend" value="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &amp;lt;repo&amp;gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。" style="fillColor=#ffffff;strokeColor=#999999" geo="1040,12,560,163"/>
<mxCell id="hdr0" value="使用者（離線機）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="40,183,230,28"/>
<mxCell id="hdr1" value="啟動器（主機 sh）" style="fillColor=#e6e6e6;strokeColor=#999999" geo="290,183,400,28"/>
<mxCell id="hdr2" value="docker daemon" style="fillColor=#e6e6e6;strokeColor=#999999" geo="710,183,240,28"/>
<mxCell id="hdr3" value="引擎容器" style="fillColor=#e6e6e6;strokeColor=#999999" geo="970,183,320,28"/>
<mxCell id="hdr4" value="專案目錄" style="fillColor=#e6e6e6;strokeColor=#999999" geo="1310,183,280,28"/>
<mxCell id="bO1b" value="離線接工具（v2.8-5）：工具 tar 由工具 repo 提供、使用者另備 → 每個工具各跑一次 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;：判別值 → load → 讀 .digest → image ID → resolve → create／cp → apply（flock → 重驗 → 寫入）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,227,1590,1062"/>
<mxCell id="bO1b_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bO1b" geo="1546,5,30,20"/>
<mxCell id="oo0" value="來自「離線包（1）」頁：install 完成、version.local.toml 已寫（引擎可離線跑）" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" parent="bO1b" geo="20,36,230,102"/>
<mxCell id="oo1" value="有網路的機器取得工具 tar + 同名 .tar.digest（由工具 repo 提供；不在 vendor_kit 離線包內）→ 帶到離線機" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="20,170,230,73"/>
<mxCell id="oo1n" value="已定（v2.8-5）：vendor_kit 離線包只含引擎；-t &amp;lt;repo&amp;gt; 走 registry（需網路）；離線接工具 = 使用者另備工具 tar（工具 repo 的 docker save + .digest），逐工具 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；離線 upgrade 不支援" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bO1b" geo="1290,154,280,104"/>
<mxCell id="o10l" value="↓ 每個工具各跑一次（一次一個）：" style="fillColor=none;strokeColor=none" parent="bO1b" geo="20,274,230,26"/>
<mxCell id="o10" value="just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt; [-y]" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="20,316,230,42"/>
<mxCell id="o10q" value="判別 --local 值（B1 三分支，同「離線包（1）」頁：路徑不存在 → 1；既存檔且可解讀為 tag → 1 + 6-37）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,316,400,42"/>
<mxCell id="o10a" value="docker load &amp;lt; &amp;lt;工具 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,374,300,40"/>
<mxCell id="o10d" value="本機 image &amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bO1b" geo="690,374,240,40"/>
<mxCell id="o10b" value="讀 &amp;lt;工具 tar&amp;gt;.digest → 正式 index digest（旁檔缺 → 1）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,430,400,40"/>
<mxCell id="o10c" value="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,486,300,42"/>
<mxCell id="o10cd" value="回 image ID（sha256:&amp;lt;hex64&amp;gt;）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="690,487,240,40"/>
<mxCell id="o10r" value="docker run 引擎 resolve add &amp;lt;repo&amp;gt; --local（帶 index digest + image ID；永不 -t）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,544,400,42"/>
<mxCell id="o10re" value="resolve（不寫）：算計畫、指紋；stdout vk-resolve/1" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO1b" geo="950,544,320,42"/>
<mxCell id="o10p" value="docker create／cp 取本機 image 的 dist 到暫存（不 pull）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,602,400,40"/>
<mxCell id="o10p2" value="docker run 引擎 apply add（暫存唯讀掛進 /dist）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO1b" geo="270,659,400,40"/>
<mxCell id="o10e" value="apply add：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO1b" geo="950,658,320,42"/>
<mxCell id="o10e2" value="重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO1b" geo="950,716,320,42"/>
<mxCell id="o10e3" value="寫入（見「add（2）」頁）：version.toml [tools] 正式 ref@digest；metadata 記 local_image_id" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO1b" geo="950,816,320,57"/>
<mxCell id="o10f" value="add 寫（同「add（2）」頁）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bO1b" geo="1290,774,280,142"/>
<mxCell id="o10f_0" value="version.toml [tools] 行（正式 ref@digest）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="o10f" geo="8,26,264,42"/>
<mxCell id="o10f_1" value="metadata：source + local_image_id" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="o10f" geo="8,74,264,26"/>
<mxCell id="o10f_2" value="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="o10f" geo="8,106,264,26"/>
<mxCell id="o11" value="0：該工具接入完成；version.toml 與線上接入一模一樣（可 commit）；下一個工具再跑一次 add" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bO1b" geo="20,932,230,124"/>
<mxCell id="oe20" edge="1" source="oo0" target="oo1"/>
<mxCell id="oe20l" edge="1" source="oo1" target="o10l"/>
<mxCell id="oe21" edge="1" source="o10l" target="o10"/>
<mxCell id="oe21q" edge="1" source="o10" target="o10q"/>
<mxCell id="oe22" edge="1" source="o10q" target="o10a"/>
<mxCell id="oe22d" value="載" edge="1" source="o10a" target="o10d"/>
<mxCell id="oe23" edge="1" source="o10a" target="o10b"/>
<mxCell id="oe24" edge="1" source="o10b" target="o10c"/>
<mxCell id="oe24d" edge="1" source="o10c" target="o10cd"/>
<mxCell id="oe25" edge="1" source="o10c" target="o10r"/>
<mxCell id="oe25e" edge="1" source="o10r" target="o10re"/>
<mxCell id="oe26" edge="1" source="o10r" target="o10p"/>
<mxCell id="oe26b" edge="1" source="o10p" target="o10p2"/>
<mxCell id="oe26e" edge="1" source="o10p2" target="o10e"/>
<mxCell id="oe26f" edge="1" source="o10e" target="o10e2"/>
<mxCell id="oe26g" edge="1" source="o10e2" target="o10e3"/>
<mxCell id="oe27" value="寫" edge="1" source="o10e3" target="o10f"/>
<mxCell id="oe28" edge="1" source="o10e3" target="o11"/>
<mxCell id="bO2" value="之後（Q26）：斷網下 sync／build 必成功 —— 啟動器先 docker image inspect，本機有就不 pull；離線 upgrade 不支援" style="fillColor=#f5f5f5;strokeColor=#000000" geo="20,1305,1590,470"/>
<mxCell id="bO2_v2" value="v2" style="fillColor=#00b050;strokeColor=none;fontColor=#ffffff;fontSize=9" parent="bO2" geo="1546,5,30,20"/>
<mxCell id="w0" value="斷網：just &amp;lt;ns&amp;gt; build（自動 _sync）／just vendor_kit sync" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bO2" geo="20,36,230,80"/>
<mxCell id="w1" value="快路徑：grep 比對 gen/*.stamp 第一行 vs version.toml；全相符 → 不起容器 → 0（sync --verify 或 CI 為真則全驗）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO2" geo="270,55,400,42"/>
<mxCell id="w2" value="有差：docker image inspect &amp;lt;ref&amp;gt;（version.toml 的正式 ref）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO2" geo="270,155,400,42"/>
<mxCell id="w2r" value="已定（v2.6-1、19條-11）：不用 --pull never（docker 19.03 無此旗標）；先 inspect 本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）" style="fillColor=#ffe6cc;strokeColor=#d79b00" parent="bO2" geo="1290,132,280,88"/>
<mxCell id="w3x" value="無 → 1 + 6-31：拉不到（--timeout 內結束、不 hang）" style="fillColor=#f8cecc;strokeColor=#000000" parent="bO2" geo="20,236,230,80"/>
<mxCell id="w3" value="本機有該 image？" style="fillColor=#FFF4C3;strokeColor=#000000" parent="bO2" geo="270,236,220,81"/>
<mxCell id="w3d" value="本機已有 image（docker load 過的）" style="fillColor=#e1d5e7;strokeColor=#9673a6" parent="bO2" geo="690,256,240,42"/>
<mxCell id="w4" value="有：直接 docker run（不 pull）resolve／apply sync" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" parent="bO2" geo="270,342,400,40"/>
<mxCell id="w4e" value="sync verify：image ID == metadata local_image_id（離線對照 index digest）→ materialize／verify cache" style="fillColor=#dae8fc;strokeColor=#6c8ebf" parent="bO2" geo="950,333,320,57"/>
<mxCell id="w4f" value="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just（只寫不進 git 的）" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" parent="bO2" geo="1290,340,280,42"/>
<mxCell id="w5" value="0：成功、不起 pull（驗收 §7.4-17）" style="fillColor=#d5e8d4;strokeColor=#000000" parent="bO2" geo="20,406,230,58"/>
<mxCell id="we0" edge="1" source="w0" target="w1"/>
<mxCell id="we1" edge="1" source="w1" target="w2"/>
<mxCell id="we2" edge="1" source="w2" target="w3"/>
<mxCell id="we3" value="無" edge="1" source="w3" target="w3x"/>
<mxCell id="we4" value="inspect" edge="1" source="w3" target="w3d"/>
<mxCell id="we5" value="有" edge="1" source="w3" target="w4"/>
<mxCell id="we6" edge="1" source="w4" target="w4e"/>
<mxCell id="we7" value="寫" edge="1" source="w4e" target="w4f"/>
<mxCell id="we8" edge="1" source="w4" target="w5"/>
<mxCell id="p16c_lg0" value="淺灰：情境分組（無狀態意義）" style="fillColor=#f5f5f5;strokeColor=#000000" geo="40,1791,200,60"/>
<mxCell id="p16c_lg1" value="黃：判斷" style="fillColor=#FFF4C3;strokeColor=#000000" geo="260,1791,140,64"/>
<mxCell id="p16c_lg2" value="綠：起點／終點" style="fillColor=#d5e8d4;strokeColor=#000000" geo="420,1799,140,44"/>
<mxCell id="p16c_lg3" value="紅：失敗終止（拉不到／寫壞）" style="fillColor=#f8cecc;strokeColor=#000000" geo="580,1793,190,56"/>
<mxCell id="p16c_lg4" value="橙：需要人動作（1／3 印指令；2 解衝突）" style="fillColor=#ffe6cc;strokeColor=#000000" geo="790,1793,210,56"/>
<mxCell id="p16c_lg5" value="白：步驟" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3)" geo="1020,1801,88,40"/>
<mxCell id="p16c_lg6" value="虛線框：專案裡的檔案" style="fillColor=#ffffff;strokeColor=light-dark(#000000,#9577A3);dashed=1" geo="1128,1801,170,40"/>
<mxCell id="p16c_lgt" value="實線 = 執行順序（指向檔案時 = 寫入／讀取）" style="fillColor=none;strokeColor=none" geo="1318,1791,280,60"/>
<mxCell id="p16c_lgx_note" value="便條：補充說明" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1859,120,36"/>
<mxCell id="p16c_lgx_rule" value="橘框：規則（已定）" style="fillColor=#ffe6cc;strokeColor=#d79b00" geo="180,1859,150,36"/>
<mxCell id="p16c_lgx_sub" value="藍：引擎子命令（容器內）" style="fillColor=#dae8fc;strokeColor=#6c8ebf" geo="350,1859,190,36"/>
<mxCell id="p16c_lgx_img" value="紫：image（引擎與工具）" style="fillColor=#e1d5e7;strokeColor=#9673a6" geo="560,1859,170,36"/>
<mxCell id="p16c_lgx_hdr" value="灰底：泳道／表格表頭" style="fillColor=#e6e6e6;strokeColor=#999999" geo="750,1859,170,36"/>
<mxCell id="p16c_lgx_entry" value="虛線橢圓：來自其他頁" style="fillColor=#ffffff;strokeColor=#000000;dashed=1" geo="940,1859,200,36"/>
<mxCell id="p16c_th" value="本頁名詞" style="fillColor=none;strokeColor=none;fontSize=13" geo="40,1897,200,28"/>
<mxCell id="p16c_tk0" value="離線包（#27、Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1931,150,55"/>
<mxCell id="p16c_tv0" value="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1931,610,55"/>
<mxCell id="p16c_tk1" value="bootstrap.sh --local（契約入口）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,1986,150,102"/>
<mxCell id="p16c_tv1" value="離線接入的契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &amp;lt;repo&amp;gt; 仍是 add &amp;lt;repo&amp;gt;[@tag]，走 registry、需網路，離線機不帶 -t；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load + 讀 .digest；其餘 → image tag（不 load、不讀 .digest，只 inspect image ID）；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&amp;lt;v&amp;gt; 或完整 ref」" style="fillColor=#ffffff;strokeColor=#999999" geo="190,1986,610,102"/>
<mxCell id="p16c_tk2" value="工具 tar（來源，v2.8-5）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2088,150,71"/>
<mxCell id="p16c_tv2" value="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &amp;lt;repo&amp;gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&amp;lt;hex64&amp;gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2088,610,71"/>
<mxCell id="p16c_tk3" value="local_bootstrap.sh（便利包裝，非契約）" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2159,150,55"/>
<mxCell id="p16c_tv3" value="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2159,610,55"/>
<mxCell id="p16c_tk4" value=".digest 旁檔" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2214,150,40"/>
<mxCell id="p16c_tv4" value="&amp;lt;name&amp;gt;.tar.digest 一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2214,610,40"/>
<mxCell id="p16c_tk5" value="image ID／local_image_id" style="fillColor=#ffffff;strokeColor=#999999" geo="40,2254,150,55"/>
<mxCell id="p16c_tv5" value="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）" style="fillColor=#ffffff;strokeColor=#999999" geo="190,2254,610,55"/>
<mxCell id="p16c_tk6" value="version.local.toml" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1931,150,40"/>
<mxCell id="p16c_tv6" value="不進 git；--local 時寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1931,610,40"/>
<mxCell id="p16c_tk7" value="離線可用（Q26）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,1971,150,55"/>
<mxCell id="p16c_tv7" value="啟動器一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang" style="fillColor=#ffffff;strokeColor=#999999" geo="990,1971,610,55"/>
<mxCell id="p16c_tk8" value="sync 快路徑（Q22）／--verify（F5）" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2026,150,71"/>
<mxCell id="p16c_tv8" value="sync（無參數）啟動器只用 grep 比對 gen/.stamp 第一行 == version.toml 引擎 ref、gen/&amp;lt;repo&amp;gt;.stamp 第一行 == 鎖定 digest、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0；有差才起引擎；sync --verify 或 CI 為真 → 每檔 sha256 全驗（verify 用 local_image_id 對照）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2026,610,71"/>
<mxCell id="p16c_tk9" value="6-N 訊息編號" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2097,150,55"/>
<mxCell id="p16c_tv9" value="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2097,610,55"/>
<mxCell id="p16c_tk10" value="結束碼 0／1／2／3" style="fillColor=#ffffff;strokeColor=#999999" geo="840,2152,150,71"/>
<mxCell id="p16c_tv10" value="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" style="fillColor=#ffffff;strokeColor=#999999" geo="990,2152,610,71"/>
</diagram>
</mxfile>
```
