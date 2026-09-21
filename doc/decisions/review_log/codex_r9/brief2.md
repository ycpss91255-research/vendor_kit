# 第九輪獨立審查 brief（draw.io v2_only，共 47 頁）

你是獨立審查者。請依下列審查標準，對照附件 PNG（47 頁）、附件「決策紀錄」（interface_spec.md）與附件 drawio XML，逐頁審查。

## 審查標準（使用者定的）
1. 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。
2. 顏色要有明確一致的意義，以各頁底部圖例為準；沒有的顏色不可出現。
3. 字要少，一般人（非工程師）也看得懂；專有名詞要在該頁底部「本頁名詞」表裡。
4. 線段：不穿無關方框、不交叉、不壓字、不裁切、不懸空、不該折的不折。
5. 線上文字 12pt。
6. 內容要跟 notes 的決策一致，且不可出現任何特定工具名（如 base）當實例，一律用 <repo>。
7. 每個方塊只放一件事（一個動作、一個判斷、一個檔案、一個最小單元）；一格裡有兩件事（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）就是問題，要拆成兩格。

## 本輪改動
第九輪：依第八輪 18 項必修＋10 項選修與 v2.10 澄清（需人動作一律橙；bootstrap --local tag 形第一次接入用內嵌引擎 ref 的 digest；add --local 只收 tar、離線包(2) 去掉 tag 三分支；upgrade vendor_kit 不建進度日誌＝明文例外（E(c) 兩頁與名詞表）；6-2b 只適用第一行已改，E(c)(2) 分兩個結束；help 印 6-33 仍 0；b18 除解析失敗檔外；update 0/1/2/3；一格一事：install(2) 刪日誌獨立步驟、prune 清理／日誌拆格、sync(2) 驗證／重裝拆、目錄樹 .tmp 兩格、schema 表兩列；排版：架構圖 f_user 標題、bootstrap(1) 交叉、add(2) 標籤、T 接改各自入口、離線包(2) 寬度、契約④ ③ 標籤、迴圈菱形 bootstrap(2)／sync(1′)、install(1) 移除重複問句 i4ld）。install(2) ie13 在零交叉限制下無法改直接接法，維持原繞行。共 47 頁。

## 特別注意
對照 interface_spec.md 與 proposal_v2.md v2.10 逐頁找：(1) 第八輪 18 項必修＋10 項選修是否修掉；(2) 頁間入口出口；(3) 每格一件事（只算真的兩個獨立動作）；(4) legend／名詞表；(5) 顏色：需人動作＝橙、拉取／寫入失敗＝紅，找全 47 頁是否還有不一致。已接受的設計（含 v2.10 的 add --local 只收 tar、upgrade vendor_kit 不建日誌、ie13 繞行）不要再質疑。只回報真正的問題；若某頁沒有問題請明說。最後給一句總評：這 47 頁能否交給使用者看（允許少量選修）。

## 請你回答的格式
逐頁列出 (A) 排版問題 (B) 顏色不符圖例 (C) 一般人看不懂的點與名詞表遺漏 (D) 與 notes 矛盾之處，每項給元件或線段 id（找不到 id 就寫元件上的文字）與一句說明，並標明是否必修（必須修才可交付）或選修；最後給「可以交付」或「還不行」。

## 附件 PNG 的頁次（依 -i 順序）
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

---

# 附件：決策紀錄（interface_spec.md 全文）

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


---

# 附件：drawio XML（v2_only.drawio，精簡版）

注意：因輸入長度上限，drawio XML 以精簡格式貼上（內容、id、顏色、字級、連線來源／目標與幾何皆保留，僅移除 whiteSpace／html／align／spacing／strokeWidth／labelBackground 等排版樣板）。格式說明：
- `<page name="頁名">` … `</page>` = 一頁。
- `<c .../>` = 一個 mxCell：`id`、`edge`（有＝線段）、`source`／`target`（線段兩端 id）、`parent`（省略＝根層）、`v`＝顯示文字（含 HTML 實體）、`g="x,y,w,h"`＝幾何、`pts`＝線段路徑點。
- `st` 樣式縮寫：`f`=fillColor、`s`=strokeColor、`fc`=fontColor、`fs`=fontSize（省略＝12）、`b`=fontStyle（1 粗體）、`es`=edgeStyle、`swf`=swimlaneFillColor；其餘（dashed／ellipse／rhombus／shape／swimlane／container／collapsible／startSize／text）原樣保留。

```xml
<page name="契約 v2：不變量與角色">
<c id="title" st="text;fs=18;b=1" g="40,20,960,34" v="契約① 使用者介面（1／3）── 目的、角色、不變量（interface_spec v2；&amp;lt;repo&amp;gt; = 工具 repo 名）"/>
<c id="p1_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p1_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;本頁只有目的、角色、不變量與初始檔規則；動詞表在 p1b、選項／結束碼／規則在 p1c"/>
<c id="p1A" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,234" v="0. 目的與角色（契約只對兩個黃橢圓承諾）"/>
<c id="p1A_goal" parent="p1A" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="20,50,740,106" v="目的（一句話）：工具 repo 把 dist/ 打包成 GHCR image；下游專案靠 bootstrap.sh + just vendor_kit add／upgrade／dev 拿到工具、跟上新版、在本機開發工具本身；其餘自動。&lt;br&gt;契約只對兩個黃橢圓承諾；我們（灰橢圓）不對自己承諾。"/>
<c id="p1A_r1" parent="p1A" st="ellipse;f=#FFF4C3;s=#000000;fs=14" g="790,50,240,106" v="工具 repo 開發者（供應側）&lt;br&gt;照契約③ p3 出貨 dist 與 image"/>
<c id="p1A_r2" parent="p1A" st="ellipse;f=#FFF4C3;s=#000000;fs=14" g="1050,50,240,106" v="使用者（下游專案）&lt;br&gt;每天打 just 的人；用 p1b 的動詞"/>
<c id="p1A_r3" parent="p1A" st="ellipse;f=#CCCCCC;s=#000000;fs=14" g="1310,50,230,106" v="vendor_kit 開發者（我們）&lt;br&gt;維護引擎與啟動器；不對自己承諾"/>
<c id="p1A_tech" parent="p1A" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,168,1520,46" v="&lt;b&gt;技術路線 [定]&lt;/b&gt;：自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file（行內合併）；&lt;b&gt;第一版不放 vendir／Copier&lt;/b&gt;。依據：無單一工具全包四項（拉、鎖、初始檔、合併）；vendir 只省 docker 三行；Copier 要求範本是帶 tag 的 git repo"/>
<c id="p1A_tech_v2" parent="p1A" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,170,30,20" v="v2"/>
<c id="p1B" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,350,1560,1123" v="1. 不變量（ADR；一列一主題，規則／條件／動作／結束碼分格）＋ 初始檔規則（§5；B = baseline、D = 磁碟上你的檔、N = 目標版範本 /dist/&amp;lt;repo&amp;gt;）"/>
<c id="p1B_inv" parent="p1B" st="f=#ffffff;s=#b85450;fs=14" g="20,50,1520,48" v="&lt;b&gt;1. 不變量（ADR）[定]：vendor_kit 對使用者的檔 ── 可以建（明說建了什麼）、要改先問（-y 免問）、永不刪、永不覆蓋。&lt;/b&gt;&lt;br&gt;「永不覆蓋」= 不用工具版本取代使用者客製內容；例外只有三處：根 justfile 一行、根 .dockerignore 三行、已納管初始檔經同意的換版／三方合併。never fail silently（結束碼 0／1／2／3）。"/>
<c id="p1B_inv_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,52,30,20" v="v2"/>
<c id="p1B_t_h0" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="20,114,170,30" v="主題"/>
<c id="p1B_t_h1" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="190,114,430,30" v="規則（一格一件事）"/>
<c id="p1B_t_h2" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="620,114,300,30" v="條件"/>
<c id="p1B_t_h3" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="920,114,340,30" v="動作"/>
<c id="p1B_t_h4" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="1260,114,280,30" v="結束碼／訊息"/>
<c id="p1B_t_r0c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,144,170,57" v="&lt;b&gt;自動化（sync）只碰不進 git 的東西&lt;/b&gt;"/>
<c id="p1B_t_r0c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,146,30,20" v="v2"/>
<c id="p1B_t_r0c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,144,430,26" v="可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p1B_t_r0c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,170,430,31" v="不碰使用者的檔、不寫薄殼四檔、不寫 gen/.stamp"/>
<c id="p1B_t_r0c2" parent="p1B" st="f=#ffffff;s=#999999" g="620,144,300,57" v="引擎 ref ≠ gen/.stamp 第一行"/>
<c id="p1B_t_r0c3" parent="p1B" st="f=#ffffff;s=#999999" g="920,144,340,57" v="不重寫薄殼，只提示"/>
<c id="p1B_t_r0c4" parent="p1B" st="f=#ffffff;s=#999999" g="1260,144,280,57" v="1 印 6-1「vendor_kit 已更新 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt;，請執行：just vendor_kit upgrade vendor_kit」"/>
<c id="p1B_t_r1c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,201,170,68" v="&lt;b&gt;薄殼重產只由 install／upgrade vendor_kit 做&lt;/b&gt;"/>
<c id="p1B_t_r1c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,203,30,20" v="v2"/>
<c id="p1B_t_r1c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,201,430,26" v="薄殼四檔與 gen/.stamp 只由 install／upgrade vendor_kit 重產"/>
<c id="p1B_t_r1c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,227,430,42" v="重產前先比對薄殼自描述首行（# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=…）：引擎重算 hash + 對 image 內模板二次比對"/>
<c id="p1B_t_r1c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="620,201,300,26" v="首行 hash 相符"/>
<c id="p1B_t_r1c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="620,227,300,42" v="首行 hash 不符（薄殼被改過）"/>
<c id="p1B_t_r1c3_0" parent="p1B" st="f=#ffffff;s=#999999" g="920,201,340,26" v="重產"/>
<c id="p1B_t_r1c3_1" parent="p1B" st="f=#ffffff;s=#999999" g="920,227,340,42" v="不動任何薄殼、列出差異（使用者 git checkout 還原後再跑）"/>
<c id="p1B_t_r1c4_0" parent="p1B" st="f=#ffffff;s=#999999" g="1260,201,280,26" v="—"/>
<c id="p1B_t_r1c4_1" parent="p1B" st="f=#ffffff;s=#999999" g="1260,227,280,42" v="1 印 6-28"/>
<c id="p1B_t_r2c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,269,170,83" v="&lt;b&gt;CI 為真（frozen）與 -y 無關&lt;/b&gt;"/>
<c id="p1B_t_r2c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,271,30,20" v="v2"/>
<c id="p1B_t_r2c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,269,430,26" v="frozen = 不寫任何 tracked 檔、不查最新版"/>
<c id="p1B_t_r2c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,295,430,26" v="仍拉鎖定版 image、仍寫 cache/、gen/"/>
<c id="p1B_t_r2c1_2" parent="p1B" st="f=#ffffff;s=#999999" g="190,321,430,31" v="-y 只在本機免詢問、不解除 frozen；update 不受影響"/>
<c id="p1B_t_r2c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="620,269,300,57" v="環境變數 CI 非空且不為 0／false（GitHub／GitLab 都設 CI=true；check.sh 自己 export CI=1）"/>
<c id="p1B_t_r2c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="620,326,300,26" v="frozen 下需要寫 tracked 檔"/>
<c id="p1B_t_r2c3_0" parent="p1B" st="f=#ffffff;s=#999999" g="920,269,340,57" v="進 frozen"/>
<c id="p1B_t_r2c3_1" parent="p1B" st="f=#ffffff;s=#999999" g="920,326,340,26" v="不寫，印需改的檔清單（與 -y 無關）"/>
<c id="p1B_t_r2c4_0" parent="p1B" st="f=#ffffff;s=#999999" g="1260,269,280,57" v="—"/>
<c id="p1B_t_r2c4_1" parent="p1B" st="f=#ffffff;s=#999999" g="1260,326,280,26" v="1"/>
<c id="p1B_t_r3c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,352,170,84" v="&lt;b&gt;「會碰使用者東西」只有三處&lt;/b&gt;"/>
<c id="p1B_t_r3c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,354,30,20" v="v2"/>
<c id="p1B_t_r3c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,352,430,26" v="根 justfile 一行（問後加／刪）"/>
<c id="p1B_t_r3c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,378,430,26" v="根 .dockerignore 三行（問後 append／刪）"/>
<c id="p1B_t_r3c1_2" parent="p1B" st="f=#ffffff;s=#999999" g="190,404,430,32" v="初始檔（init.toml 的 dest；含 strategy=append 經同意加的行）"/>
<c id="p1B_t_r3c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="620,352,300,42" v="使用者 .gitignore：工具以 strategy=append 宣告且你同意"/>
<c id="p1B_t_r3c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="620,394,300,42" v="其餘：未宣告的使用者 .gitignore、.git/info/exclude、.git 本身"/>
<c id="p1B_t_r3c3_0" parent="p1B" st="f=#ffffff;s=#999999" g="920,352,340,42" v="才加行"/>
<c id="p1B_t_r3c3_1" parent="p1B" st="f=#ffffff;s=#999999" g="920,394,340,42" v="不碰"/>
<c id="p1B_t_r3c4_0" parent="p1B" st="f=#ffffff;s=#999999" g="1260,352,280,42" v="—"/>
<c id="p1B_t_r3c4_1" parent="p1B" st="f=#ffffff;s=#999999" g="1260,394,280,42" v="—"/>
<c id="p1B_t_r4c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,436,170,110" v="&lt;b&gt;詢問通則&lt;/b&gt;"/>
<c id="p1B_t_r4c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,438,30,20" v="v2"/>
<c id="p1B_t_r4c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,436,430,26" v="詢問一律有拒絕分支"/>
<c id="p1B_t_r4c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,462,430,84" v="-y 只省略詢問：不授權覆蓋既有未納管檔、不硬加 append 行"/>
<c id="p1B_t_r4c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="620,436,300,42" v="明確回答「否」"/>
<c id="p1B_t_r4c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="620,478,300,42" v="需詢問但無 tty／EOF 且無 -y"/>
<c id="p1B_t_r4c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="620,520,300,26" v="EOF／Ctrl-C 中途中斷"/>
<c id="p1B_t_r4c3_0" parent="p1B" st="f=#ffffff;s=#999999" g="920,436,340,42" v="不寫；新檔（從未建立）→ state=declined；已納管檔 → state 不變、只記 declined_hash"/>
<c id="p1B_t_r4c3_1" parent="p1B" st="f=#ffffff;s=#999999" g="920,478,340,42" v="不寫"/>
<c id="p1B_t_r4c3_2" parent="p1B" st="f=#ffffff;s=#999999" g="920,520,340,26" v="中止整個 apply、不套用、不記 declined"/>
<c id="p1B_t_r4c4_0" parent="p1B" st="f=#ffffff;s=#999999" g="1260,436,280,42" v="繼續（該檔略過）"/>
<c id="p1B_t_r4c4_1" parent="p1B" st="f=#ffffff;s=#999999" g="1260,478,280,42" v="1 印 6-4「需要確認但沒有終端可互動。請加 -y，或在終端執行。」"/>
<c id="p1B_t_r4c4_2" parent="p1B" st="f=#ffffff;s=#999999" g="1260,520,280,26" v="1"/>
<c id="p1B_t_r5c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,546,170,120" v="&lt;b&gt;失敗恢復與零寫入&lt;/b&gt;"/>
<c id="p1B_t_r5c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,548,30,20" v="v2"/>
<c id="p1B_t_r5c1_0" parent="p1B" st="f=#ffffff;s=#999999" g="190,546,430,26" v="所有合併在暫存完成 → 逐檔原子替換"/>
<c id="p1B_t_r5c1_1" parent="p1B" st="f=#ffffff;s=#999999" g="190,572,430,26" v="apply 進度日誌在第一個寫入前建立、最後一步刪除"/>
<c id="p1B_t_r5c1_2" parent="p1B" st="f=#ffffff;s=#999999" g="190,598,430,26" v="結束碼 3 一律零寫入（無例外）"/>
<c id="p1B_t_r5c1_3" parent="p1B" st="f=#ffffff;s=#999999" g="190,624,430,42" v="「不留半成品」只對第一次 install 成立；衝突（2）與自身升級要求重跑（1）是獨立狀態"/>
<c id="p1B_t_r5c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="620,546,300,26" v="寫入中途失敗"/>
<c id="p1B_t_r5c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="620,572,300,26" v="下次可寫動詞遇到未完成日誌"/>
<c id="p1B_t_r5c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="620,598,300,68" v="唯讀動詞（sync／update／help）遇到未完成日誌"/>
<c id="p1B_t_r5c3_0" parent="p1B" st="f=#ffffff;s=#999999" g="920,546,340,26" v="明列已完成／未完成"/>
<c id="p1B_t_r5c3_1" parent="p1B" st="f=#ffffff;s=#999999" g="920,572,340,26" v="先恢復再繼續"/>
<c id="p1B_t_r5c3_2" parent="p1B" st="f=#ffffff;s=#999999" g="920,598,340,68" v="不恢復，只提示"/>
<c id="p1B_t_r5c4_0" parent="p1B" st="f=#ffffff;s=#999999" g="1260,546,280,26" v="1"/>
<c id="p1B_t_r5c4_1" parent="p1B" st="f=#ffffff;s=#999999" g="1260,572,280,26" v="—"/>
<c id="p1B_t_r5c4_2" parent="p1B" st="f=#ffffff;s=#999999" g="1260,598,280,68" v="sync／update：1 印 6-33；help：印 6-33 仍 0"/>
<c id="p1I_l" parent="p1B" st="text;fs=13;s=none;f=none;b=1" g="20,682,900,28" v="初始檔規則（同不變量；每列一種情況、一格一件事）"/>
<c id="p1I_h0" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="20,714,150,30" v="時機"/>
<c id="p1I_h1" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="170,714,360,30" v="情況"/>
<c id="p1I_h2" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="530,714,1010,30" v="做法（逐字問句見 6-20～6-22）"/>
<c id="p1I_r0c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,744,150,26" v="add"/>
<c id="p1I_r0c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,744,360,26" v="檔不存在"/>
<c id="p1I_r0c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,744,1010,26" v="建（印出建了什麼）；state=managed"/>
<c id="p1I_r1c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,770,150,26" v="add"/>
<c id="p1I_r1c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="138,772,30,20" v="v2"/>
<c id="p1I_r1c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,770,360,26" v="檔已存在（strategy=copy）"/>
<c id="p1I_r1c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,770,1010,26" v="不納管、不覆蓋（-y 也不覆蓋），印 6-11「&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對」；state=unmanaged"/>
<c id="p1I_r2c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,796,150,57" v="add（strategy=append）"/>
<c id="p1I_r2c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="138,798,30,20" v="v2"/>
<c id="p1I_r2c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,796,360,57" v="檔已存在"/>
<c id="p1I_r2c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,796,1010,57" v="問 6-21「要在 &amp;lt;X&amp;gt; 加這幾行嗎」→ append，實際插入的行記在 metadata lines（原本就有的相同行不認領）；state=appended；重跑不重複；拒絕 → 不加行、不納管（state=unmanaged）"/>
<c id="p1I_r3c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,853,150,26" v="upgrade"/>
<c id="p1I_r3c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="138,855,30,20" v="v2"/>
<c id="p1I_r3c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,853,360,26" v="D 缺（使用者刪了已納管檔）"/>
<c id="p1I_r3c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,853,1010,26" v="state=deleted，維持刪除、不重建"/>
<c id="p1I_r4c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,879,150,26" v="upgrade"/>
<c id="p1I_r4c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,879,360,26" v="D==N 或 B==N（新版沒改／你的檔已等於新版）"/>
<c id="p1I_r4c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,879,1010,26" v="不動"/>
<c id="p1I_r5c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,905,150,26" v="upgrade"/>
<c id="p1I_r5c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,905,360,26" v="D==B（新版改了、你沒改）"/>
<c id="p1I_r5c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,905,1010,26" v="問 6-22「&amp;lt;X&amp;gt; 換成新版？」→ 換；拒絕 → state 仍 managed、只記 declined_hash（N 的 hash 變了才再問）"/>
<c id="p1I_r6c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,931,150,42" v="upgrade"/>
<c id="p1I_r6c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,931,360,42" v="三者皆異（兩邊都改）"/>
<c id="p1I_r6c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,931,1010,42" v="問 6-22「你和新版都改了 &amp;lt;X&amp;gt;，要三方合併嗎？」→ git merge-file --diff3；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline、回 2；baseline 仍推到新版（合併結果解析失敗 → 2 留原檔、baseline 不推、記 conflicts）；拒絕 → state 不變、只記 declined_hash"/>
<c id="p1I_r7c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,973,150,26" v="upgrade"/>
<c id="p1I_r7c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,973,360,26" v="N 缺（新版刪除該檔）"/>
<c id="p1I_r7c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,973,1010,26" v="不刪，只 warn"/>
<c id="p1I_r8c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,999,150,26" v="upgrade"/>
<c id="p1I_r8c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="138,1001,30,20" v="v2"/>
<c id="p1I_r8c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,999,360,26" v="新版新增初始檔（Q14）"/>
<c id="p1I_r8c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,999,1010,26" v="問 6-22「要建 &amp;lt;X&amp;gt; 嗎」（-y 建）；拒絕 → 從未建立，state=declined + declined_hash，之後不問；新版 N 的 hash 變了才再問；dest 在 CI 路徑時先印 6-29"/>
<c id="p1I_r9c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1025,150,26" v="upgrade（append）"/>
<c id="p1I_r9c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,1025,360,26" v="找到上次加的行（原文相同；CRLF／LF 等價）"/>
<c id="p1I_r9c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,1025,1010,26" v="問後替換；拒絕 → state 仍 appended、只記 declined_hash；零命中或多處命中 → 保留只 warn、印新內容"/>
<c id="p1I_r10c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1051,150,26" v="upgrade"/>
<c id="p1I_r10c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="138,1053,30,20" v="v2"/>
<c id="p1I_r10c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,1051,360,26" v="二進位／symlink（不合併）"/>
<c id="p1I_r10c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,1051,1010,26" v="你沒改 → 問 6-22「&amp;lt;X&amp;gt; 是二進位檔，要換成新版嗎？」後才換（拒絕 → state 不變、只記 declined_hash）；改過 → 保留 + warn"/>
<c id="p1I_r11c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1077,150,26" v="remove／uninstall"/>
<c id="p1I_r11c1" parent="p1B" st="f=#ffffff;s=#999999" g="170,1077,360,26" v="任何"/>
<c id="p1I_r11c2" parent="p1B" st="f=#ffffff;s=#999999" g="530,1077,1010,26" v="永不刪初始檔，印清單；append 行問 6-21「要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎」後只刪原文相同的"/>
<c id="p1_lg0" st="ellipse;f=#FFF4C3;s=#000000;fs=14" g="40,1497,260,52" v="黃橢圓：契約承諾的角色"/>
<c id="p1_lg1" st="ellipse;f=#CCCCCC;s=#000000;fs=14" g="320,1497,260,52" v="灰橢圓：不承諾（我們）"/>
<c id="p1_lg2" st="f=#ffffff;s=#b85450;fs=14" g="600,1503,160,40" v="白底紅粗框：不變量"/>
<c id="p1_lg3" st="f=#ffe6cc;s=#d79b00;fs=14" g="780,1503,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p1_lg4" st="f=#e6e6e6;s=#999999;b=1" g="990,1503,110,40" v="灰底：表頭"/>
<c id="p1_lgt" st="text;s=none;f=none" g="1120,1493,300,60" v="橢圓／方框顏色只在本頁有效&lt;br&gt;動詞表 p1b；選項、結束碼、規則 p1c；流程細節一律在流程頁"/>
<c id="p1_lg5" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="40,1569,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p1_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="260,1569,200,40" v="右上角綠標籤：v2 改"/>
<c id="p1_lg6_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="428,1571,30,20" v="v2"/>
<c id="p1_lg7" st="shape=note;f=#ffffff;s=#999999" g="480,1569,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p1_th" st="text;fs=13;s=none;f=none;b=1" g="40,1625,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p1_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1659,150,40" v="&amp;lt;repo&amp;gt;"/>
<c id="p1_tv0" st="f=#ffffff;s=#999999" g="190,1659,610,40" v="工具 repo 名（占位符）；.vendor_kit/cache/&amp;lt;repo&amp;gt;/ = 專案裡展開的工具檔；ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist = 它的 image；&amp;lt;ns&amp;gt; = 工具 just 模組的命名空間"/>
<c id="p1_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1699,150,40" v="不變量（ADR）"/>
<c id="p1_tv1" st="f=#ffffff;s=#999999" g="190,1699,610,40" v="整個專案最高優先的四句：可以建、要改先問、永不刪、永不覆蓋；記在 docs/adr/（短格式 ADR），每個決議都對照它；不另建 PRD.md"/>
<c id="p1_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1739,150,40" v="ADR"/>
<c id="p1_tv2" st="f=#ffffff;s=#999999" g="190,1739,610,40" v="Architecture Decision Record：一份記錄「為什麼這樣決定」的短文件（docs/adr/）；破壞性變更、提高 floor 都要記一筆"/>
<c id="p1_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1779,150,40" v="tracked 檔"/>
<c id="p1_tv3" st="f=#ffffff;s=#999999" g="190,1779,610,40" v="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p1_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1819,150,55" v="frozen（CI 為真）"/>
<c id="p1_tv4" st="f=#ffffff;s=#999999" g="190,1819,610,55" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"/>
<c id="p1_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1874,150,40" v="CI／runner"/>
<c id="p1_tv5" st="f=#ffffff;s=#999999" g="190,1874,610,40" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）"/>
<c id="p1_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1914,150,55" v="結束碼 0／1／2／3"/>
<c id="p1_tv6" st="f=#ffffff;s=#999999" g="190,1914,610,55" v="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入"/>
<c id="p1_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1969,150,55" v="sync"/>
<c id="p1_tv7" st="f=#ffffff;s=#999999" g="190,1969,610,55" v="每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑"/>
<c id="p1_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2024,150,55" v="薄殼自描述首行"/>
<c id="p1_tv8" st="f=#ffffff;s=#999999" g="190,2024,610,55" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動"/>
<c id="p1_tk9" st="f=#ffffff;s=#999999;b=1" g="40,2079,150,55" v="strategy = &quot;append&quot;"/>
<c id="p1_tv9" st="f=#ffffff;s=#999999" g="190,2079,610,55" v="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）"/>
<c id="p1_tk10" st="f=#ffffff;s=#999999;b=1" g="40,2134,150,40" v="CRLF／LF"/>
<c id="p1_tv10" st="f=#ffffff;s=#999999" g="190,2134,610,40" v="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]"/>
<c id="p1_tk11" st="f=#ffffff;s=#999999;b=1" g="40,2174,150,40" v="三方合併"/>
<c id="p1_tv11" st="f=#ffffff;s=#999999" g="190,2174,610,40" v="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）"/>
<c id="p1_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1659,150,40" v="baseline"/>
<c id="p1_tv12" st="f=#ffffff;s=#999999" g="990,1659,610,40" v=".vendor_kit/baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep"/>
<c id="p1_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1699,150,40" v="N（目標版範本）"/>
<c id="p1_tv13" st="f=#ffffff;s=#999999" g="990,1699,610,40" v="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&amp;lt;id&amp;gt;/、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（唯讀），不是 cache；cache/&amp;lt;repo&amp;gt;/ 在 apply 決定套用後才 materialize"/>
<c id="p1_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1739,150,55" v="初始檔五態（state）"/>
<c id="p1_tv14" st="f=#ffffff;s=#999999" g="990,1739,610,55" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"/>
<c id="p1_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1794,150,55" v="declined／declined_hash"/>
<c id="p1_tv15" st="f=#ffffff;s=#999999" g="990,1794,610,55" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined"/>
<c id="p1_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1849,150,55" v="conflicts（衝突中檔案）"/>
<c id="p1_tv16" st="f=#ffffff;s=#999999" g="990,1849,610,55" v="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）"/>
<c id="p1_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1904,150,71" v="進度日誌"/>
<c id="p1_tv17" st="f=#ffffff;s=#999999" g="990,1904,610,71" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續；sync／update 偵測未完成交易 → 印 6-33 結束 1；help 印 6-33 但仍 0"/>
<c id="p1_tk18" st="f=#ffffff;s=#999999;b=1" g="840,1975,150,40" v="tty／trap"/>
<c id="p1_tv18" st="f=#ffffff;s=#999999" g="990,1975,610,40" v="tty = 互動終端（能問問題）；沒有 tty（管線、CI）又需詢問且無 -y → 1 印 6-4；trap = shell 的收尾勾子，啟動器用它在中斷時清容器與 .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p1_tk19" st="f=#ffffff;s=#999999;b=1" g="840,2015,150,71" v="根 .dockerignore 三行"/>
<c id="p1_tv19" st="f=#ffffff;s=#999999" g="990,2015,610,71" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache"/>
<c id="p1_tk20" st="f=#ffffff;s=#999999;b=1" g="840,2086,150,55" v="根 justfile 四行"/>
<c id="p1_tv20" st="f=#ffffff;s=#999999" g="990,2086,610,55" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行"/>
<c id="p1_tk21" st="f=#ffffff;s=#999999;b=1" g="840,2141,150,55" v="metadata"/>
<c id="p1_tv21" st="f=#ffffff;s=#999999" g="990,2141,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌"/>
</page>
<page name="契約 v2：動詞介面表">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約① 使用者介面（2／3）── 動詞介面表（interface_spec §1.2；just vendor_kit &amp;lt;verb&amp;gt; [args]）"/>
<c id="p1b_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p1b_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;選項總表（Q25）、結束碼、不開的動詞在 p1c；每個動詞的流程在流程頁 p5～"/>
<c id="p1B" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,1822" v="2. 契約① 使用者介面：常用 3 + 進階 8 + 一次性 1 + help（綠底 常用、白底 進階、藍底 一次性；一列一動詞、「做什麼」欄一格一件事；6-N = interface_spec §6 訊息編號）"/>
<c id="p1B_h0" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="20,50,220,30" v="動詞＋語法"/>
<c id="p1B_h1" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="240,50,84,30" v="反向"/>
<c id="p1B_h2" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="324,50,980,30" v="做什麼（一格一件事；細節見流程頁）"/>
<c id="p1B_h3" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="1304,50,180,30" v="結束碼"/>
<c id="p1B_h4" parent="p1B" st="f=#e6e6e6;s=#999999;b=1" g="1484,50,56,30" v="組"/>
<c id="p1B_r0c0" parent="p1B" st="f=#dae8fc;s=#999999;b=1" g="20,80,220,182" v="bootstrap.sh&lt;br&gt;sh bootstrap.sh [-t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]… [-y] [--local &amp;lt;image tag 或 tar&amp;gt;] [--timeout &amp;lt;秒&amp;gt;] [-h]"/>
<c id="p1B_r0c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,82,30,20" v="v2"/>
<c id="p1B_r0c1" parent="p1B" st="f=#dae8fc;s=#999999" g="240,80,84,182" v="uninstall（反向呼叫）"/>
<c id="p1B_r0c2_0" parent="p1B" st="f=#dae8fc;s=#999999" g="324,80,980,26" v="前置：在 git repo 內（否 → 1 印 6-16）；just ≥ 1.33.0（不足 → 1 印 6-23）；floor 檢查；已有 version.toml → 用該行引擎（不用內嵌）"/>
<c id="p1B_r0c2_1" parent="p1B" st="f=#dae8fc;s=#999999" g="324,106,980,26" v="docker image inspect 引擎 image：本機有 → 不 pull（離線可用）"/>
<c id="p1B_r0c2_2" parent="p1B" st="f=#dae8fc;s=#999999" g="324,132,980,26" v="本機無 → docker pull 引擎 ref（逾時 → 1 印 6-31）；--local &amp;lt;tar&amp;gt;：改 docker load，再讀 .digest 旁檔"/>
<c id="p1B_r0c2_3" parent="p1B" st="f=#dae8fc;s=#999999" g="324,158,980,26" v="呼叫引擎 install"/>
<c id="p1B_r0c2_4" parent="p1B" st="f=#dae8fc;s=#999999" g="324,184,980,26" v="對每個 -t 呼叫 add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（轉發 -y；EOF 不算同意）"/>
<c id="p1B_r0c2_5" parent="p1B" st="f=#dae8fc;s=#999999" g="324,210,980,26" v="--local：version.local.toml（vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id）在 install 成功後才寫、失敗清除；version.toml 仍寫正式 ref"/>
<c id="p1B_r0c2_6" parent="p1B" st="f=#dae8fc;s=#999999" g="324,236,980,26" v="再跑一次 = 呼叫 install（冪等修復）；不自刪；離線包 = bootstrap.sh --local；取得：releases/latest/download/bootstrap.sh"/>
<c id="p1B_r0c3" parent="p1B" st="f=#dae8fc;s=#999999" g="1304,80,180,182" v="0；1 失敗不留半成品（只對第一次 install 成立）；3"/>
<c id="p1B_r0c4" parent="p1B" st="f=#dae8fc;s=#999999" g="1484,80,56,182" v="一次性"/>
<c id="p1B_r1c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,262,220,146" v="install&lt;br&gt;install [-y] [--no-justfile]&lt;br&gt;install &amp;lt;repo&amp;gt; 誤用 → 1 印 6-17"/>
<c id="p1B_r1c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,264,30,20" v="v2"/>
<c id="p1B_r1c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,262,84,146" v="uninstall"/>
<c id="p1B_r1c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,262,980,26" v="前置：在 git repo 內（否 → 1 印 6-16）；上層與下層皆無 .vendor_kit/（否 → 1 印 6-35）；不被 gen/.stamp 關卡擋"/>
<c id="p1B_r1c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,288,980,26" v="第一次／修復判定用薄殼自描述首行：不存在 → 第一次；hash 相符 → 重產；不符 → 1 印 6-28 列差異不動"/>
<c id="p1B_r1c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="324,314,980,26" v="建 .vendor_kit/：version.toml（schema、written_by）、薄殼四檔、baseline/.gitkeep（不建 metadata）、gen/.stamp"/>
<c id="p1B_r1c2_3" parent="p1B" st="f=#ffffff;s=#999999" g="324,340,980,42" v="根 justfile：無 → 建逐字四行（import &#x27;.vendor_kit/entry.just&#x27;／空行／default:／\t@just --list）；有 → 問 6-20（-y 直接加）；已含 → 不再加；--no-justfile 只印指示"/>
<c id="p1B_r1c2_4" parent="p1B" st="f=#ffffff;s=#999999" g="324,382,980,26" v="根 .dockerignore：無 → 建三行（.vendor_kit/cache/、gen/、.tmp.*）；有 → 問 6-34 後 append，記於 baseline/.vendor_kit.toml；印建立或修改了什麼"/>
<c id="p1B_r1c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,262,180,146" v="0／1／3"/>
<c id="p1B_r1c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,262,56,146" v="進階"/>
<c id="p1B_r2c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,408,220,156" v="uninstall&lt;br&gt;uninstall [-y] [--dry-run]"/>
<c id="p1B_r2c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,410,30,20" v="v2"/>
<c id="p1B_r2c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,408,84,156" v="install"/>
<c id="p1B_r2c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,408,980,26" v="前置：預檢全部工具（有 dev 覆寫 → 1 提示先 undev）；hash 相符的保護清單在任何 remove 之前生效"/>
<c id="p1B_r2c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,434,980,26" v="apply：拿鎖、重驗指紋 → 建日誌 .tmp.uninstall.&amp;lt;id&amp;gt;.toml"/>
<c id="p1B_r2c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="324,460,980,26" v="逐工具 remove（保護模式）：只刪自產（hash 相符）的檔；未知或被改的保留並回報；目錄非空則保留；不 rm -rf"/>
<c id="p1B_r2c2_3" parent="p1B" st="f=#ffffff;s=#999999" g="324,486,980,26" v="任一工具回 1 → 中止並列出已完成部分；初始檔一律保留並印清單"/>
<c id="p1B_r2c2_4" parent="p1B" st="f=#ffffff;s=#999999" g="324,512,980,26" v="根 justfile 那行：問 6-20「要從 justfile 刪這一行嗎」只刪完全相同的行"/>
<c id="p1B_r2c2_5" parent="p1B" st="f=#ffffff;s=#999999" g="324,538,980,26" v="根 .dockerignore 三行與 append 行：問後只刪原文相同的 → 最後刪日誌"/>
<c id="p1B_r2c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,408,180,156" v="0／1／3"/>
<c id="p1B_r2c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,408,56,156" v="進階"/>
<c id="p1B_r3c0" parent="p1B" st="f=#d5e8d4;s=#999999;b=1" g="20,564,220,182" v="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]&lt;br&gt;add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] [--source &amp;lt;image&amp;gt;] [--local &amp;lt;tar&amp;gt;] [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]&lt;br&gt;&amp;lt;repo&amp;gt;：[A-Za-z0-9_][A-Za-z0-9_.-]*、不得為 vendor_kit"/>
<c id="p1B_r3c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,566,30,20" v="v2"/>
<c id="p1B_r3c1" parent="p1B" st="f=#d5e8d4;s=#999999" g="240,564,84,182" v="remove"/>
<c id="p1B_r3c2_0" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,564,980,26" v="前置：已接入且完成 → 0 無變更；@&amp;lt;tag&amp;gt; 與鎖定不同 → 1 提示 upgrade；私有 image 無憑證又未指定 @&amp;lt;tag&amp;gt; → 1 印 6-3；dest 撞名／越界 → 拒絕"/>
<c id="p1B_r3c2_1" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,590,980,26" v="前置：&amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（just --dump）(c) 保留名 vendor_kit 撞名 → 1 拒絕"/>
<c id="p1B_r3c2_2" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,616,980,26" v="resolve → 主機 docker 展開到 .tmp.dist.&amp;lt;id&amp;gt;/&amp;lt;repo&amp;gt;/ → apply：拿鎖、重驗指紋、建日誌（metadata [progress]）；逐檔讀 /dist"/>
<c id="p1B_r3c2_3" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,642,980,26" v="初始檔：無 → 建；有 → 不納管（unmanaged，印 6-11；-y 也不覆蓋）；strategy=&quot;append&quot; 且已存在 → 問 6-21（-y 免問，印出加了什麼）"/>
<c id="p1B_r3c2_4" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,668,980,26" v="收尾①：materialize → cache/&amp;lt;repo&amp;gt;/ + gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p1B_r3c2_5" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,694,980,26" v="收尾②：baseline/&amp;lt;repo&amp;gt;/ + metadata（complete=true；--local &amp;lt;tar&amp;gt;：.digest 旁檔取正式 index digest、記 local_image_id）"/>
<c id="p1B_r3c2_6" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,720,980,26" v="收尾③：gen/tools.just 重生 → version.toml 最後寫 → 刪日誌"/>
<c id="p1B_r3c3" parent="p1B" st="f=#d5e8d4;s=#999999" g="1304,564,180,182" v="0；1（version.toml 一律未動：dest 不合法、CI 為真需改 tracked、指紋不同、失敗）；3"/>
<c id="p1B_r3c4" parent="p1B" st="f=#d5e8d4;s=#999999" g="1484,564,56,182" v="常用"/>
<c id="p1B_r4c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,746,220,78" v="remove &amp;lt;repo&amp;gt;&lt;br&gt;remove &amp;lt;repo&amp;gt; [-y] [--dry-run]&lt;br&gt;裸跑 → 用法 + 1"/>
<c id="p1B_r4c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,748,30,20" v="v2"/>
<c id="p1B_r4c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,746,84,78" v="add"/>
<c id="p1B_r4c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,746,980,26" v="前置：有 dev 覆寫 → 1 提示先 undev；未接 = 0 + 提示；兩段（resolve → apply、重驗指紋）但不經 docker create/cp"/>
<c id="p1B_r4c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,772,980,26" v="建日誌 .tmp.remove.&amp;lt;id&amp;gt;.toml 後刪：version.toml 該行、cache/&amp;lt;repo&amp;gt;/、baseline/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just 該工具所有 mod? 行"/>
<c id="p1B_r4c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="324,798,980,26" v="初始檔永不刪，印清單；append 過的行 → 問 6-21「要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎」只刪原文相同的（CRLF/LF 等價）→ 刪日誌"/>
<c id="p1B_r4c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,746,180,78" v="0／1／3"/>
<c id="p1B_r4c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,746,56,78" v="進階"/>
<c id="p1B_r5c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,824,220,88" v="update [&amp;lt;repo&amp;gt;]&lt;br&gt;update [&amp;lt;repo&amp;gt;] [--exit-code]&lt;br&gt;&amp;lt;repo&amp;gt; 可省 = 全部含 vendor_kit"/>
<c id="p1B_r5c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,826,30,20" v="v2"/>
<c id="p1B_r5c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,824,84,88" v="（upgrade 的前一步）"/>
<c id="p1B_r5c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,824,980,26" v="只查 registry（tags/list 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 frozen 影響；單段、不經 docker create/cp"/>
<c id="p1B_r5c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,850,980,62" v="無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；末行固定 6-15「套用：just vendor_kit upgrade」"/>
<c id="p1B_r5c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,824,180,88" v="0 已列出；1 查詢失敗（任一工具 1 → 整體 1）；--exit-code 有新版 → 2；3"/>
<c id="p1B_r5c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,824,56,88" v="進階"/>
<c id="p1B_r6c0" parent="p1B" st="f=#d5e8d4;s=#999999;b=1" g="20,912,220,188" v="upgrade &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（工具）&lt;br&gt;upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]] [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]&lt;br&gt;@&amp;lt;tag&amp;gt; 限單一 repo；比現版舊 → warn 仍執行"/>
<c id="p1B_r6c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,914,30,20" v="v2"/>
<c id="p1B_r6c1" parent="p1B" st="f=#d5e8d4;s=#999999" g="240,912,84,188" v="git revert 整組 commit"/>
<c id="p1B_r6c2_0" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,912,980,26" v="前置：無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新增 &amp;lt;ns&amp;gt;／dest 撞名）再動任何東西"/>
<c id="p1B_r6c2_1" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,938,980,42" v="(0) conflicts 非空且檔案仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 @&amp;lt;tag&amp;gt;；frozen 不查）"/>
<c id="p1B_r6c2_2" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,980,980,42" v="resolve → 主機 docker → apply（拿鎖、重驗、建日誌）→ 逐檔狀態機（p1 表；N 讀自 /dist/&amp;lt;repo&amp;gt;）問 6-22；拒絕 → 已納管檔 state 不變只記 declined_hash、新檔 state=declined；CI 為真且需改 tracked 檔 → 1 印清單（與 -y 無關）"/>
<c id="p1B_r6c2_3" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1022,980,26" v="baseline 推到新版（有衝突仍推；解析失敗不推）+ metadata"/>
<c id="p1B_r6c2_4" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1048,980,26" v="materialize cache/、gen/&amp;lt;repo&amp;gt;.stamp；gen/tools.just 重生"/>
<c id="p1B_r6c2_5" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1074,980,26" v="version.toml 最後寫 → 刪日誌；--dry-run：只印會問哪些檔與 6-6～6-8、不寫"/>
<c id="p1B_r6c3" parent="p1B" st="f=#d5e8d4;s=#999999" g="1304,912,180,188" v="0；1 工具層不動 version.toml；2 有衝突（留標記、印檔名、baseline 仍推；解完重跑；merge-file I/O 錯誤 → 1）；3"/>
<c id="p1B_r6c4" parent="p1B" st="f=#d5e8d4;s=#999999" g="1484,912,56,188" v="常用"/>
<c id="p1B_r7c0" parent="p1B" st="f=#d5e8d4;s=#999999;b=1" g="20,1100,220,126" v="upgrade（不帶 repo：全部含自身）&lt;br&gt;upgrade [-y] [--dry-run] [--timeout &amp;lt;秒&amp;gt;]"/>
<c id="p1B_r7c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1102,30,20" v="v2"/>
<c id="p1B_r7c1" parent="p1B" st="f=#d5e8d4;s=#999999" g="240,1100,84,126" v="git revert 整組 commit"/>
<c id="p1B_r7c2_0" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1100,980,42" v="resolve 先判斷「引擎有新版？」：否 → 只升全部工具（同上列；Q27 彙總）；是 → 本次只改第一行、工具不升：舊引擎 apply（拿鎖、重驗、建日誌）只改 vendor_kit 正規行"/>
<c id="p1B_r7c2_1" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1142,980,42" v="啟動器 apply 前後各 grep 一次正規行：ref 變了 → local 覆寫有 vendor_kit= 則 docker image inspect 驗 ID 用該 image，否則 docker pull 新 ref → 用新引擎跑 upgrade vendor_kit（下一列）"/>
<c id="p1B_r7c2_2" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1184,980,42" v="第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b「引擎版本已鎖定為 &amp;lt;vY&amp;gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」，不再重跑"/>
<c id="p1B_r7c3" parent="p1B" st="f=#d5e8d4;s=#999999" g="1304,1100,180,126" v="1 印 6-2「已升級引擎 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」（已改第一行後回 1 是明列例外）"/>
<c id="p1B_r7c4" parent="p1B" st="f=#d5e8d4;s=#999999" g="1484,1100,56,126" v="常用"/>
<c id="p1B_r8c0" parent="p1B" st="f=#d5e8d4;s=#999999;b=1" g="20,1226,220,104" v="upgrade vendor_kit[@&amp;lt;tag&amp;gt;]&lt;br&gt;upgrade vendor_kit[@&amp;lt;tag&amp;gt;] [-y]&lt;br&gt;單段救援路徑（不依賴 resolve/apply 與 gen/）"/>
<c id="p1B_r8c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1228,30,20" v="v2"/>
<c id="p1B_r8c1" parent="p1B" st="f=#d5e8d4;s=#999999" g="240,1226,84,104" v="git revert 整組 commit"/>
<c id="p1B_r8c2_0" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1226,980,26" v="啟動器讀正規行（local 覆寫優先：docker image inspect 驗 vendor_kit_image_id、不 pull）→ 該引擎跑；不被 gen/.stamp 關卡擋"/>
<c id="p1B_r8c2_1" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1252,980,42" v="查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版且薄殼首行 hash 相符 → 改第一行 → 啟動器再以新 ref 跑一次 → 新引擎重產薄殼四檔 + gen/.stamp → 1 印 6-2；無新版且相符 → 0；只重產薄殼 → 1 印 6-2；被改 → 1 印 6-28"/>
<c id="p1B_r8c2_2" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1294,980,36" v="@&amp;lt;舊版&amp;gt; 降版：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（要退回請 git revert）"/>
<c id="p1B_r8c3" parent="p1B" st="f=#d5e8d4;s=#999999" g="1304,1226,180,104" v="0 無變更；1 印 6-2；3 印 6-10"/>
<c id="p1B_r8c4" parent="p1B" st="f=#d5e8d4;s=#999999" g="1484,1226,56,104" v="常用"/>
<c id="p1B_r9c0" parent="p1B" st="f=#d5e8d4;s=#999999;b=1" g="20,1330,220,110" v="dev &amp;lt;repo&amp;gt;&lt;br&gt;dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;／dev vendor_kit -i &amp;lt;tag&amp;gt;&lt;br&gt;-p（工具必填）與 -i（僅 vendor_kit，只能 tag）互斥"/>
<c id="p1B_r9c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1332,30,20" v="v2"/>
<c id="p1B_r9c1" parent="p1B" st="f=#d5e8d4;s=#999999" g="240,1330,84,110" v="undev"/>
<c id="p1B_r9c2_0" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1330,980,26" v="前置：工具必須已在 version.toml（否 → 1）；&amp;lt;dir&amp;gt;/dist/init.toml 存在（缺 → 1）；CI 為真 → 拒絕；單段、不經 docker create/cp"/>
<c id="p1B_r9c2_1" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1356,980,42" v="工具：version.local.toml [tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；cache/&amp;lt;repo&amp;gt;/ 改 symlink → &amp;lt;dir&amp;gt;/dist；gen/&amp;lt;repo&amp;gt;.stamp 第一行 path:&amp;lt;dir&amp;gt;；之後啟動器掛 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro，sync 跳過 materialize／verify"/>
<c id="p1B_r9c2_2" parent="p1B" st="f=#d5e8d4;s=#999999" g="324,1398,980,42" v="自身：version.local.toml vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；之後啟動器每次 docker image inspect 驗 ID、不 pull；-i 的 image 以 LABEL P／schema 判為「舊」→ 允許但禁止重產 tracked 薄殼"/>
<c id="p1B_r9c3" parent="p1B" st="f=#d5e8d4;s=#999999" g="1304,1330,180,110" v="0／1／3"/>
<c id="p1B_r9c4" parent="p1B" st="f=#d5e8d4;s=#999999" g="1484,1330,56,110" v="常用"/>
<c id="p1B_r10c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1440,220,84" v="undev &amp;lt;repo&amp;gt;&lt;br&gt;undev &amp;lt;repo&amp;gt;／undev vendor_kit"/>
<c id="p1B_r10c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1442,30,20" v="v2"/>
<c id="p1B_r10c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,1440,84,84" v="dev"/>
<c id="p1B_r10c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,1440,980,42" v="未啟用 = 0 + 提示；兩段：建日誌 .tmp.undev.&amp;lt;id&amp;gt;.toml → 撤 version.local.toml 該行（undev vendor_kit 一併撤 vendor_kit_image_id；最後一個覆寫撤掉後刪整個檔）"/>
<c id="p1B_r10c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,1482,980,42" v="工具：重新 materialize 鎖定版（經 docker create/cp）；失敗 → 1 保留可恢復狀態。undev vendor_kit：下次 just 用 version.toml 引擎；gen/.stamp ≠ ref → 只提示 6-1、不重寫"/>
<c id="p1B_r10c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,1440,180,84" v="0／1／3"/>
<c id="p1B_r10c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,1440,56,84" v="進階"/>
<c id="p1B_r11c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1524,220,152" v="sync [&amp;lt;repo&amp;gt;]&lt;br&gt;sync [&amp;lt;repo&amp;gt;]／sync --verify&lt;br&gt;&amp;lt;repo&amp;gt; 可省 = 全部；--verify = 每檔 sha256 全驗"/>
<c id="p1B_r11c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1526,30,20" v="v2"/>
<c id="p1B_r11c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,1524,84,152" v="—"/>
<c id="p1B_r11c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,1524,980,42" v="每次工具 recipe 自動前置（_sync）；快路徑（無參數）：啟動器只用 grep 比 gen/*.stamp 第一行 vs version.toml、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0"/>
<c id="p1B_r11c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,1566,980,42" v="引擎 ref ≠ gen/.stamp 第一行 → 1 印 6-1 不重寫（install／upgrade vendor_kit 跳過此關）；未完成交易 → 1 印 6-33 不恢復；CI 為真下任何 local 覆寫 → 1"/>
<c id="p1B_r11c2_2" parent="p1B" st="f=#ffffff;s=#999999" g="324,1608,980,42" v="只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp。每工具：覆寫 path → 跳過（仍查完成標記、落後）；cache 缺或印記 ≠ 鎖定 digest → materialize；否則 verify（--verify／CI 為真／版本變動時）→ 失敗 → 重裝 + warn；tools.just 缺 → 重生"/>
<c id="p1B_r11c2_3" parent="p1B" st="f=#ffffff;s=#999999" g="324,1650,980,26" v="無待辦 → resolve 回 apply|no 快路徑 0（不起第二個容器）；baseline 落後：本機 warn 提示 upgrade、CI 為真 → 1 印 6-5"/>
<c id="p1B_r11c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,1524,180,152" v="0；1：薄殼不符、無完成標記（6-13）、CI 為真下 baseline 落後（6-5）或任何 local 覆寫；3"/>
<c id="p1B_r11c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,1524,56,152" v="進階"/>
<c id="p1B_r12c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1676,220,84" v="prune&lt;br&gt;prune [-y] [--dry-run]"/>
<c id="p1B_r12c0_v2" parent="p1B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,1678,30,20" v="v2"/>
<c id="p1B_r12c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,1676,84,84" v="—"/>
<c id="p1B_r12c2_0" parent="p1B" st="f=#ffffff;s=#999999" g="324,1676,980,42" v="兩段：resolve prune 輸出 keep 清單（version.toml + version.local.toml 引用的全部 image）→ 啟動器 docker {container,image,network,volume} ls --filter label=io.github.&amp;lt;org&amp;gt;.vendor_kit=1 列候選、扣掉 keep"/>
<c id="p1B_r12c2_1" parent="p1B" st="f=#ffffff;s=#999999" g="324,1718,980,42" v="問 6-32「要刪除以上 vendor_kit 資源嗎？」（-y 免問）→ docker rm／image rm／network rm／volume rm；image 只刪「帶 label 且本專案未引用」者（--dry-run 先看）；活躍的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml 不刪、列出提示 6-33；apply prune 刪失效的 .tmp.dist.*"/>
<c id="p1B_r12c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,1676,180,84" v="0／1／3"/>
<c id="p1B_r12c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,1676,56,84" v="進階"/>
<c id="p1B_r13c0" parent="p1B" st="f=#ffffff;s=#999999;b=1" g="20,1760,220,42" v="help／h&lt;br&gt;help"/>
<c id="p1B_r13c1" parent="p1B" st="f=#ffffff;s=#999999" g="240,1760,84,42" v="—"/>
<c id="p1B_r13c2" parent="p1B" st="f=#ffffff;s=#999999" g="324,1760,980,42" v="命名空間層說明（just 做不到 just vendor_kit --help）；各動詞 --help 由引擎印；不觸網、不安裝；明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」"/>
<c id="p1B_r13c3" parent="p1B" st="f=#ffffff;s=#999999" g="1304,1760,180,42" v="0"/>
<c id="p1B_r13c4" parent="p1B" st="f=#ffffff;s=#999999" g="1484,1760,56,42" v="—"/>
<c id="p1b_lg0" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="40,1948,130,40" v="綠底：常用動詞"/>
<c id="p1b_lg1" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="190,1948,130,40" v="白底：進階動詞"/>
<c id="p1b_lg2" st="f=#dae8fc;s=light-dark(#000000,#9577A3);fs=14" g="340,1948,210,40" v="藍底：一次性（bootstrap.sh）"/>
<c id="p1b_lg3" st="f=#ffe6cc;s=#d79b00;fs=14" g="570,1948,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p1b_lg4" st="f=#e6e6e6;s=#999999;b=1" g="780,1948,110,40" v="灰底：表頭"/>
<c id="p1b_lg5" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="910,1948,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p1b_lgt" st="text;s=none;f=none" g="1130,1938,300,60" v="一列 = 一個動詞；「做什麼」欄一格一件事&lt;br&gt;「反向」= 收回它做的事的動詞"/>
<c id="p1b_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="40,2014,200,40" v="右上角綠標籤：v2 改"/>
<c id="p1b_lg6_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,2016,30,20" v="v2"/>
<c id="p1b_lg7" st="shape=note;f=#ffffff;s=#999999" g="260,2014,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p1b_th" st="text;fs=13;s=none;f=none;b=1" g="40,2070,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p1b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,2104,150,40" v="resolve／apply"/>
<c id="p1b_tv0" st="f=#ffffff;s=#999999" g="190,2104,610,40" v="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④"/>
<c id="p1b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2144,150,40" v="N（目標版範本）"/>
<c id="p1b_tv1" st="f=#ffffff;s=#999999" g="190,2144,610,40" v="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&amp;lt;id&amp;gt;/、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（唯讀），不是 cache；cache/&amp;lt;repo&amp;gt;/ 在 apply 決定套用後才 materialize"/>
<c id="p1b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2184,150,55" v="frozen（CI 為真）"/>
<c id="p1b_tv2" st="f=#ffffff;s=#999999" g="190,2184,610,55" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"/>
<c id="p1b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2239,150,55" v="docker image inspect"/>
<c id="p1b_tv3" st="f=#ffffff;s=#999999" g="190,2239,610,55" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）"/>
<c id="p1b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2294,150,55" v=".digest 旁檔"/>
<c id="p1b_tv4" st="f=#ffffff;s=#999999" g="190,2294,610,55" v="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1"/>
<c id="p1b_tk5" st="f=#ffffff;s=#999999;b=1" g="840,2104,150,55" v="初始檔五態（state）"/>
<c id="p1b_tv5" st="f=#ffffff;s=#999999" g="990,2104,610,55" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"/>
<c id="p1b_tk6" st="f=#ffffff;s=#999999;b=1" g="840,2159,150,55" v="救援路徑"/>
<c id="p1b_tv6" st="f=#ffffff;s=#999999" g="990,2159,610,55" v="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼"/>
<c id="p1b_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2214,150,55" v="「引擎已變」"/>
<c id="p1b_tv7" st="f=#ffffff;s=#999999" g="990,2214,610,55" v="不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行；ref 變了且 == 計畫的 engine → 用新 ref（local 覆寫時 inspect 驗 ID）跑 upgrade vendor_kit；第二次又變 → 1 印 6-2b"/>
</page>
<page name="契約 v2：規則、選項表、不開的動詞">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約① 使用者介面（3／3）── 規則、選項表（Q25）、結束碼（Q23／Q27）、不開的動詞、訊息文字（§6）"/>
<c id="p1c_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p1c_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;選項與結束碼以 interface_spec §1.1／§2 為準；訊息文字 §6 逐字（本頁只列 p1／p1b 引用到的）"/>
<c id="p1C" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,1777" v="3. 規則、選項總表（Q25）、結束碼總表（Q23／Q27）、不開的動詞、訊息文字（interface_spec §6 逐字）"/>
<c id="p1C_pair_t" parent="p1C" st="text;s=none;f=none;b=1" g="20,50,200,24" v="兩層成對（反向）"/>
<c id="p1C_pd0" parent="p1C" st="text;s=none;f=none" g="20,74,200,30" v="專案層（vendor_kit 自己）"/>
<c id="p1C_pa0" parent="p1C" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="225,74,110,30" v="install"/>
<c id="p1C_pb0" parent="p1C" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="410,74,110,30" v="uninstall"/>
<c id="p1C_pe0" edge source="p1C_pa0" target="p1C_pb0" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p1C_pd1" parent="p1C" st="text;s=none;f=none" g="20,112,200,30" v="工具層"/>
<c id="p1C_pa1" parent="p1C" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="225,112,110,30" v="add"/>
<c id="p1C_pb1" parent="p1C" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="410,112,110,30" v="remove"/>
<c id="p1C_pe1" edge source="p1C_pa1" target="p1C_pb1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p1C_pd2" parent="p1C" st="text;s=none;f=none" g="20,150,200,30" v="本機開發"/>
<c id="p1C_pa2" parent="p1C" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="225,150,110,30" v="dev"/>
<c id="p1C_pb2" parent="p1C" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="410,150,110,30" v="undev"/>
<c id="p1C_pe2" edge source="p1C_pa2" target="p1C_pb2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p1C_pd3" parent="p1C" st="text;s=none;f=none" g="20,188,200,30" v="只查 → 套用（apt 語意）"/>
<c id="p1C_pa3" parent="p1C" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="225,188,110,30" v="update"/>
<c id="p1C_pb3" parent="p1C" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="410,188,110,30" v="upgrade"/>
<c id="p1C_pe3" edge source="p1C_pa3" target="p1C_pb3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="前一步"/>
<c id="p1C_no" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,236,740,92" v="&lt;b&gt;不開的動詞與理由&lt;/b&gt;&lt;br&gt;init（→ install）／ensure（→ sync）／diff（= upgrade --dry-run）／accept（解完衝突重跑 upgrade）／rollback（git revert）／--repair（併進 install 冪等修復）／--purge（明確不提供：永不刪使用者檔；開 issue）／--porcelain（不做；v2 候選，本版無待拍板）／--tag（版本一律 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;）／materialize、verify、merge（引擎內部步驟，不對外）"/>
<c id="p1C_no_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="728,238,30,20" v="v2"/>
<c id="p1C_s1" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,342,740,77" v="&lt;b&gt;recipe 規則&lt;/b&gt;&lt;br&gt;動詞 recipe 一律 verb *args 一行轉發（set positional-arguments 只在 vendor.just）、放 tracked 的 vendor.just；[group(&#x27;常用&#x27;)]／[group(&#x27;進階&#x27;)]；每次呼叫引擎附 --protocol P（在子命令之前）；entry.just 與 gen/tools.just 只含 mod／mod?／import?，零 set 零 recipe（被 import 檔的 set 會外溢到根檔）"/>
<c id="p1C_s1_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="728,344,30,20" v="v2"/>
<c id="p1C_s2" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,433,740,92" v="&lt;b&gt;執行位置（Q20）&lt;/b&gt;&lt;br&gt;專案根 = 含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在專案根執行：recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免（工具 _sync 已 cd 回專案根）；須在某 git repo 內；禁止巢狀（上層或下層已有 → 1 印 6-35）；引擎不讀 .git、不碰 index、不做 git init"/>
<c id="p1C_s2_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="728,435,30,20" v="v2"/>
<c id="p1C_s3" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,539,740,77" v="&lt;b&gt;兩段編排的兩個獨立屬性（p3b 契約④）&lt;/b&gt;&lt;br&gt;需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve → 主機 docker → apply，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）"/>
<c id="p1C_s3_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="728,541,30,20" v="v2"/>
<c id="p1C_dry" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,630,740,77" v="&lt;b&gt;--dry-run（所有頁一致）&lt;/b&gt;&lt;br&gt;唯讀預覽（仍拉 image 展開到暫存，讀 /dist/&amp;lt;repo&amp;gt;）：印會建／會問哪些檔、6-6～6-8、metadata 遷移；本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單（version.toml 不動；與 -y 無關）；-y 也不覆蓋既有未納管檔、不硬加 append 行；EOF 不算同意"/>
<c id="p1C_dry_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="728,632,30,20" v="v2"/>
<c id="p1C_opt_l" parent="p1C" st="text;fs=13;s=none;f=none;b=1" g="790,50,700,28" v="選項總表（Q25；短選項只給常用）"/>
<c id="p1C_opt_h0" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="790,82,170,30" v="選項"/>
<c id="p1C_opt_h1" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="960,82,50,30" v="短形"/>
<c id="p1C_opt_h2" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="1010,82,90,30" v="型別"/>
<c id="p1C_opt_h3" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="1100,82,200,30" v="適用"/>
<c id="p1C_opt_h4" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="1300,82,240,30" v="說明"/>
<c id="p1C_opt_r0c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,112,170,42" v="--tool &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]"/>
<c id="p1C_opt_r0c0_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,114,30,20" v="v2"/>
<c id="p1C_opt_r0c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,112,50,42" v="-t"/>
<c id="p1C_opt_r0c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,112,90,42" v="string，可重複"/>
<c id="p1C_opt_r0c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,112,200,42" v="bootstrap.sh"/>
<c id="p1C_opt_r0c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,112,240,42" v="接入的工具與版本；@&amp;lt;tag&amp;gt; 省略 = 最新正式版"/>
<c id="p1C_opt_r1c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,154,170,57" v="--yes"/>
<c id="p1C_opt_r1c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,154,50,57" v="-y"/>
<c id="p1C_opt_r1c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,154,90,57" v="bool"/>
<c id="p1C_opt_r1c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,154,200,57" v="bootstrap.sh、install、uninstall、add、remove、upgrade、prune"/>
<c id="p1C_opt_r1c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,154,240,57" v="免詢問（不解除 frozen）"/>
<c id="p1C_opt_r2c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,211,170,26" v="--path &amp;lt;dir&amp;gt;"/>
<c id="p1C_opt_r2c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,211,50,26" v="-p"/>
<c id="p1C_opt_r2c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,211,90,26" v="string"/>
<c id="p1C_opt_r2c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,211,200,26" v="dev &amp;lt;repo&amp;gt;"/>
<c id="p1C_opt_r2c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,211,240,26" v="本機工具目錄"/>
<c id="p1C_opt_r3c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,237,170,26" v="--image &amp;lt;tag&amp;gt;"/>
<c id="p1C_opt_r3c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,237,50,26" v="-i"/>
<c id="p1C_opt_r3c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,237,90,26" v="string"/>
<c id="p1C_opt_r3c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,237,200,26" v="dev vendor_kit"/>
<c id="p1C_opt_r3c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,237,240,26" v="本機引擎 image tag（只能 tag）"/>
<c id="p1C_opt_r4c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,263,170,26" v="--help"/>
<c id="p1C_opt_r4c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,263,50,26" v="-h"/>
<c id="p1C_opt_r4c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,263,90,26" v="bool"/>
<c id="p1C_opt_r4c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,263,200,26" v="全部"/>
<c id="p1C_opt_r4c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,263,240,26" v="由引擎印；bootstrap.sh 自印"/>
<c id="p1C_opt_r5c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,289,170,42" v="--dry-run"/>
<c id="p1C_opt_r5c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,289,50,42" v="—"/>
<c id="p1C_opt_r5c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,289,90,42" v="bool"/>
<c id="p1C_opt_r5c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,289,200,42" v="uninstall、add、remove、upgrade、prune"/>
<c id="p1C_opt_r5c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,289,240,42" v="唯讀預覽（仍拉 image 展開）"/>
<c id="p1C_opt_r6c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,331,170,42" v="--source &amp;lt;image&amp;gt;"/>
<c id="p1C_opt_r6c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,331,50,42" v="—"/>
<c id="p1C_opt_r6c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,331,90,42" v="string"/>
<c id="p1C_opt_r6c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,331,200,42" v="add"/>
<c id="p1C_opt_r6c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,331,240,42" v="image 路徑不符 &amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist 慣例時"/>
<c id="p1C_opt_r7c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,373,170,57" v="--local &amp;lt;image tag 或 tar&amp;gt;"/>
<c id="p1C_opt_r7c0_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,375,30,20" v="v2"/>
<c id="p1C_opt_r7c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,373,50,57" v="—"/>
<c id="p1C_opt_r7c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,373,90,57" v="string"/>
<c id="p1C_opt_r7c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,373,200,57" v="bootstrap.sh、add"/>
<c id="p1C_opt_r7c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,373,240,57" v="離線：tar 先 docker load；值的判別已定（含 / 或 .tar 結尾 → 檔案，其餘 → tag；見名詞表）"/>
<c id="p1C_opt_r8c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,430,170,26" v="--exit-code"/>
<c id="p1C_opt_r8c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,430,50,26" v="—"/>
<c id="p1C_opt_r8c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,430,90,26" v="bool"/>
<c id="p1C_opt_r8c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,430,200,26" v="update"/>
<c id="p1C_opt_r8c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,430,240,26" v="有新版回 2"/>
<c id="p1C_opt_r9c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,456,170,42" v="--timeout &amp;lt;秒&amp;gt;"/>
<c id="p1C_opt_r9c0_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,458,30,20" v="v2"/>
<c id="p1C_opt_r9c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,456,50,42" v="—"/>
<c id="p1C_opt_r9c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,456,90,42" v="正整數"/>
<c id="p1C_opt_r9c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,456,200,42" v="bootstrap.sh、add、upgrade、sync、undev"/>
<c id="p1C_opt_r9c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,456,240,42" v="= VENDOR_KIT_PULL_TIMEOUT，由啟動器攔截、不轉發引擎；優先於環境變數"/>
<c id="p1C_opt_r10c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,498,170,26" v="--no-justfile"/>
<c id="p1C_opt_r10c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,498,50,26" v="—"/>
<c id="p1C_opt_r10c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,498,90,26" v="bool"/>
<c id="p1C_opt_r10c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,498,200,26" v="install"/>
<c id="p1C_opt_r10c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,498,240,26" v="跳過根 justfile 步驟只印指示"/>
<c id="p1C_opt_r11c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,524,170,26" v="--protocol P"/>
<c id="p1C_opt_r11c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,524,50,26" v="—"/>
<c id="p1C_opt_r11c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,524,90,26" v="整數"/>
<c id="p1C_opt_r11c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,524,200,26" v="內部"/>
<c id="p1C_opt_r11c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,524,240,26" v="薄殼→引擎全域旗標，不列 help"/>
<c id="p1C_opt_r12c0" parent="p1C" st="f=#ffffff;s=#999999" g="790,550,170,42" v="--verify"/>
<c id="p1C_opt_r12c0_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,552,30,20" v="v2"/>
<c id="p1C_opt_r12c1" parent="p1C" st="f=#ffffff;s=#999999" g="960,550,50,42" v="—"/>
<c id="p1C_opt_r12c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,550,90,42" v="bool"/>
<c id="p1C_opt_r12c3" parent="p1C" st="f=#ffffff;s=#999999" g="1100,550,200,42" v="sync"/>
<c id="p1C_opt_r12c4" parent="p1C" st="f=#ffffff;s=#999999" g="1300,550,240,42" v="每檔 sha256 全驗（= CI 為真時的行為）；無參數 sync 走快路徑"/>
<c id="p1C_opt_n" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,602,750,46" v="版本一律寫在位置參數：&amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;、vendor_kit@&amp;lt;tag&amp;gt;；@&amp;lt;tag&amp;gt; 比現版舊 → warn 仍執行。短選項只有 -t、-y、-p、-i、-h。"/>
<c id="p1C_opt_n_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,604,30,20" v="v2"/>
<c id="p1C_ex_l" parent="p1C" st="text;fs=13;s=none;f=none;b=1" g="20,723,700,28" v="結束碼總表（§2；多工具彙總見下框）"/>
<c id="p1C_ex_h0" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="20,755,50,30" v="碼"/>
<c id="p1C_ex_h1" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="70,755,700,30" v="定義"/>
<c id="p1C_ex_h2" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="770,755,770,30" v="動詞例外／特例"/>
<c id="p1C_ex_r0c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,785,50,42" v="0"/>
<c id="p1C_ex_r0c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,785,700,42" v="成功（含 warn）；add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符皆 0 + 提示"/>
<c id="p1C_ex_r0c2" parent="p1C" st="f=#ffffff;s=#999999" g="770,785,770,42" v="—"/>
<c id="p1C_ex_r1c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,827,50,42" v="1"/>
<c id="p1C_ex_r1c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,827,700,42" v="一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動"/>
<c id="p1C_ex_r1c2" parent="p1C" st="f=#ffffff;s=#999999" g="770,827,770,42" v="自身升級：已改 version.toml 第一行後回 1（明列例外）；upgrade vendor_kit 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）——既定回 1 的情境維持 1，不因提示含 upgrade 而改 3"/>
<c id="p1C_ex_r2c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,869,50,26" v="2"/>
<c id="p1C_ex_r2c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,869,700,26" v="合併衝突（留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版）"/>
<c id="p1C_ex_r2c2" parent="p1C" st="f=#ffffff;s=#999999" g="770,869,770,26" v="update --exit-code 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔 baseline 不推、記入 conflicts"/>
<c id="p1C_ex_r3c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,895,50,57" v="3"/>
<c id="p1C_ex_r3c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,895,700,57" v="現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且零寫入；「舊」一律以 P／schema 比，不以 SemVer；網路／認證／不存在 → 1，不得偽裝成 3；floor 檢查在任何上網之前"/>
<c id="p1C_ex_r3c1_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,897,30,20" v="v2"/>
<c id="p1C_ex_r3c2" parent="p1C" st="f=#ffffff;s=#999999" g="770,895,770,57" v="(a) 薄殼 P &amp;lt; 引擎 floor_P → 6-18；(b) 引擎讀到 schema &amp;gt; 支援上限 → 6-19；(c) upgrade vendor_kit@&amp;lt;舊版&amp;gt; 目標引擎 P／schema 低於現有檔 → 6-10；(d) dev vendor_kit -i 的引擎 P／schema 低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 6-36 提示先 upgrade vendor_kit"/>
<c id="p1C_multi" parent="p1C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,966,1520,30" v="&lt;b&gt;多工具彙總（Q27）&lt;/b&gt;：不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞"/>
<c id="p1C_multi_v2" parent="p1C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,968,30,20" v="v2"/>
<c id="p1C_msg_l" parent="p1C" st="text;fs=13;s=none;f=none;b=1" g="20,1010,900,28" v="訊息文字清單（§6 逐字；每句含可直接複製的指令）"/>
<c id="p1C_mL_h0" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="20,1042,50,30" v="#"/>
<c id="p1C_mL_h1" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="70,1042,170,30" v="時機"/>
<c id="p1C_mL_h2" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="240,1042,530,30" v="文字（逐字；&amp;lt;…&amp;gt; 占位符）"/>
<c id="p1C_mL_r0c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1072,50,42" v="6-1"/>
<c id="p1C_mL_r0c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1072,170,42" v="sync：gen/.stamp 第一行 ≠ 引擎 ref"/>
<c id="p1C_mL_r0c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1072,530,42" v="vendor_kit 已更新 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt;，請執行：just vendor_kit upgrade vendor_kit（結束 1）"/>
<c id="p1C_mL_r1c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1114,50,42" v="6-2"/>
<c id="p1C_mL_r1c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1114,170,42" v="upgrade vendor_kit 重產薄殼後"/>
<c id="p1C_mL_r1c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1114,530,42" v="已升級引擎 &amp;lt;vX&amp;gt; → &amp;lt;vY&amp;gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令（結束 1）"/>
<c id="p1C_mL_r2c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1156,50,42" v="6-2b"/>
<c id="p1C_mL_r2c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1156,170,42" v="第一行已改但未重產／第二次又變"/>
<c id="p1C_mL_r2c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1156,530,42" v="引擎版本已鎖定為 &amp;lt;vY&amp;gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit（結束 1）"/>
<c id="p1C_mL_r3c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1198,50,57" v="6-3"/>
<c id="p1C_mL_r3c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1198,170,57" v="update／upgrade／add 無 registry 憑證"/>
<c id="p1C_mL_r3c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1198,530,57" v="無法列舉 &amp;lt;repo&amp;gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;（拉取使用主機 docker 認證）"/>
<c id="p1C_mL_r4c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1255,50,42" v="6-4"/>
<c id="p1C_mL_r4c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1255,170,42" v="需詢問但無 tty／EOF 且無 -y"/>
<c id="p1C_mL_r4c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1255,530,42" v="需要確認但沒有終端可互動。請加 -y，或在終端執行。（結束 1）"/>
<c id="p1C_mL_r5c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1297,50,42" v="6-5"/>
<c id="p1C_mL_r5c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1297,170,42" v="CI 下 baseline 落後；Renovate PR 需合併"/>
<c id="p1C_mL_r5c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1297,530,42" v="請在本機執行 just vendor_kit upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push（結束 1）"/>
<c id="p1C_mL_r6c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1339,50,57" v="6-6／6-7／6-8"/>
<c id="p1C_mL_r6c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1339,170,57" v="dry-run／check.sh 提醒（不紅燈）"/>
<c id="p1C_mL_r6c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1339,530,57" v="有 &amp;lt;N&amp;gt; 個範本你拒絕過／&amp;lt;X&amp;gt; 沒納管，與範本差 &amp;lt;N&amp;gt; 行／&amp;lt;Y&amp;gt; 你拒絕過，&amp;lt;vZ&amp;gt; 有新版"/>
<c id="p1C_mL_r7c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1396,50,26" v="6-9"/>
<c id="p1C_mL_r7c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1396,170,26" v="不在專案根執行"/>
<c id="p1C_mL_r7c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1396,530,26" v="請到 &amp;lt;dir&amp;gt; 執行（結束 1）"/>
<c id="p1C_mL_r8c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1422,50,42" v="6-10"/>
<c id="p1C_mL_r8c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1422,170,42" v="upgrade vendor_kit@&amp;lt;舊版&amp;gt; 無法無損讀"/>
<c id="p1C_mL_r8c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1422,530,42" v="目標引擎 &amp;lt;vY&amp;gt;（協定 &amp;lt;P&amp;gt;、schema &amp;lt;M&amp;gt;）無法無損讀取現有檔（schema &amp;lt;N&amp;gt;）。未修改任何檔。要退回舊版請 git revert 相關 commit。（結束 3）"/>
<c id="p1C_mL_r9c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1464,50,26" v="6-11"/>
<c id="p1C_mL_r9c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1464,170,26" v="add 初始檔已存在（copy）"/>
<c id="p1C_mL_r9c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1464,530,26" v="&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對"/>
<c id="p1C_mL_r10c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1490,50,26" v="6-12"/>
<c id="p1C_mL_r10c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1490,170,26" v="apply 重驗指紋不同"/>
<c id="p1C_mL_r10c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1490,530,26" v="專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit &amp;lt;verb&amp;gt; …（結束 1）"/>
<c id="p1C_mL_r11c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1516,50,42" v="6-13"/>
<c id="p1C_mL_r11c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1516,170,42" v="sync metadata 無完成標記"/>
<c id="p1C_mL_r11c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1516,530,42" v="&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;（結束 1）"/>
<c id="p1C_mL_r12c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1558,50,42" v="6-14"/>
<c id="p1C_mL_r12c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1558,170,42" v="upgrade 補完待合併後另有新版"/>
<c id="p1C_mL_r12c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1558,530,42" v="已補齊 &amp;lt;repo&amp;gt; 至 &amp;lt;vB&amp;gt;；另有新版 &amp;lt;vX&amp;gt;，再跑一次 just vendor_kit upgrade &amp;lt;repo&amp;gt; 可升"/>
<c id="p1C_mL_r13c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1600,50,26" v="6-15"/>
<c id="p1C_mL_r13c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1600,170,26" v="update 末行"/>
<c id="p1C_mL_r13c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1600,530,26" v="套用：just vendor_kit upgrade"/>
<c id="p1C_mL_r14c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1626,50,42" v="6-16"/>
<c id="p1C_mL_r14c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1626,170,42" v="install 非 git repo"/>
<c id="p1C_mL_r14c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1626,530,42" v="目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。（結束 1）"/>
<c id="p1C_mL_r15c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1668,50,26" v="6-17"/>
<c id="p1C_mL_r15c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1668,170,26" v="install &amp;lt;repo&amp;gt; 誤用"/>
<c id="p1C_mL_r15c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1668,530,26" v="install 不接受工具名稱。接入工具請執行：just vendor_kit add &amp;lt;repo&amp;gt;（結束 1）"/>
<c id="p1C_mL_r16c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="20,1694,50,26" v="6-18"/>
<c id="p1C_mL_r16c1" parent="p1C" st="f=#ffffff;s=#999999" g="70,1694,170,26" v="薄殼／版本低於 floor"/>
<c id="p1C_mL_r16c2" parent="p1C" st="f=#ffffff;s=#999999" g="240,1694,530,26" v="目前薄殼或引擎低於支援下限 &amp;lt;floor&amp;gt;。請以 bootstrap.sh 重建。（結束 3、零寫入）"/>
<c id="p1C_mR_h0" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="790,1042,50,30" v="#"/>
<c id="p1C_mR_h1" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="840,1042,170,30" v="時機"/>
<c id="p1C_mR_h2" parent="p1C" st="f=#e6e6e6;s=#999999;b=1" g="1010,1042,530,30" v="文字（逐字；&amp;lt;…&amp;gt; 占位符）"/>
<c id="p1C_mR_r0c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1072,50,57" v="6-19"/>
<c id="p1C_mR_r0c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1072,170,57" v="引擎讀到 schema 高於支援上限"/>
<c id="p1C_mR_r0c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1072,530,57" v="無法讀取 &amp;lt;file&amp;gt;：schema &amp;lt;N&amp;gt; 高於本引擎支援的 &amp;lt;M&amp;gt;；寫入者為 vendor_kit &amp;lt;written_by&amp;gt;。請使用支援此 schema 的引擎，或使用 version.toml 指定的引擎。（結束 3）"/>
<c id="p1C_mR_r1c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1129,50,42" v="6-20"/>
<c id="p1C_mR_r1c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1129,170,42" v="問句：根 justfile"/>
<c id="p1C_mR_r1c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1129,530,42" v="要在 justfile 加這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;／要從 justfile 刪這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;"/>
<c id="p1C_mR_r2c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1171,50,26" v="6-21"/>
<c id="p1C_mR_r2c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1171,170,26" v="問句：append"/>
<c id="p1C_mR_r2c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1171,530,26" v="要在 &amp;lt;X&amp;gt; 加這幾行嗎（接列出行）／要刪我們加在 &amp;lt;X&amp;gt; 的這幾行嗎（接列出行）"/>
<c id="p1C_mR_r3c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1197,50,42" v="6-22"/>
<c id="p1C_mR_r3c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1197,170,42" v="問句：upgrade 逐檔"/>
<c id="p1C_mR_r3c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1197,530,42" v="&amp;lt;X&amp;gt; 換成新版？／你和新版都改了 &amp;lt;X&amp;gt;，要三方合併嗎？／要建 &amp;lt;X&amp;gt; 嗎／&amp;lt;X&amp;gt; 是二進位檔，要換成新版嗎？"/>
<c id="p1C_mR_r4c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1239,50,42" v="6-23"/>
<c id="p1C_mR_r4c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1239,170,42" v="bootstrap just 太舊"/>
<c id="p1C_mR_r4c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1239,530,42" v="需要 just ≥ 1.33.0，目前為 &amp;lt;version&amp;gt;。請使用 GitHub release 版。+ 固定兩行 下載：&amp;lt;平台對應 URL&amp;gt;、安裝：&amp;lt;不覆蓋既有檔的安裝指令&amp;gt;"/>
<c id="p1C_mR_r5c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1281,50,57" v="6-24"/>
<c id="p1C_mR_r5c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1281,170,57" v="docker pull 失敗"/>
<c id="p1C_mR_r5c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1281,530,57" v="原文 + 三分類（網路／認證／不存在；另「主機錯誤」：daemon 不可用、磁碟滿）；認證類：&amp;lt;ref&amp;gt; 不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login &amp;lt;host&amp;gt;；僅 add／bootstrap 追加 離線可用：--local &amp;lt;tar&amp;gt;"/>
<c id="p1C_mR_r6c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1338,50,42" v="6-26"/>
<c id="p1C_mR_r6c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1338,170,42" v="flock 逾時"/>
<c id="p1C_mR_r6c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1338,530,42" v="專案目錄被鎖定（PID &amp;lt;pid&amp;gt;，自 &amp;lt;time&amp;gt;）；60 秒內未釋放。確認無其他 vendor_kit 在跑後重試，或設 VENDOR_KIT_NO_LOCK=1。（結束 1）"/>
<c id="p1C_mR_r7c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1380,50,57" v="6-28"/>
<c id="p1C_mR_r7c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1380,170,57" v="薄殼被改（install／upgrade vendor_kit）"/>
<c id="p1C_mR_r7c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1380,530,57" v="偵測到薄殼被修改：&amp;lt;files&amp;gt;。未重產任何薄殼。請先檢視下列差異；確認並手動還原（git checkout -- .vendor_kit/&amp;lt;file&amp;gt;）後，再執行 just vendor_kit upgrade vendor_kit。（結束 1）"/>
<c id="p1C_mR_r8c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1437,50,42" v="6-29"/>
<c id="p1C_mR_r8c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1437,170,42" v="新增初始檔 dest 在 CI 路徑"/>
<c id="p1C_mR_r8c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1437,530,42" v="注意：新版範本將建立或修改 CI 設定 &amp;lt;X&amp;gt;。請確認下列內容後再決定是否套用。"/>
<c id="p1C_mR_r9c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1479,50,42" v="6-30"/>
<c id="p1C_mR_r9c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1479,170,42" v="啟動器驗 vk-resolve 失敗"/>
<c id="p1C_mR_r9c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1479,530,42" v="引擎輸出不完整或不相容（&amp;lt;原因&amp;gt;），未執行任何動作。（結束 1）"/>
<c id="p1C_mR_r10c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1521,50,42" v="6-31"/>
<c id="p1C_mR_r10c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1521,170,42" v="pull 逾時"/>
<c id="p1C_mR_r10c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1521,530,42" v="拉取 &amp;lt;ref&amp;gt; 超過 &amp;lt;秒&amp;gt; 秒未完成，已中止。可用 --timeout &amp;lt;秒&amp;gt; 或 VENDOR_KIT_PULL_TIMEOUT 調整。（結束 1）"/>
<c id="p1C_mR_r11c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1563,50,26" v="6-32"/>
<c id="p1C_mR_r11c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1563,170,26" v="問句：prune"/>
<c id="p1C_mR_r11c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1563,530,26" v="要刪除以上 vendor_kit 資源嗎？"/>
<c id="p1C_mR_r12c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1589,50,42" v="6-33"/>
<c id="p1C_mR_r12c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1589,170,42" v="唯讀動詞偵測未完成交易"/>
<c id="p1C_mR_r12c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1589,530,42" v="偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;（sync／update 結束 1；help 不受影響；prune 只列出不刪）"/>
<c id="p1C_mR_r13c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1631,50,42" v="6-34"/>
<c id="p1C_mR_r13c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1631,170,42" v="問句：根 .dockerignore"/>
<c id="p1C_mR_r13c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1631,530,42" v="要在 .dockerignore 加這三行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.*"/>
<c id="p1C_mR_r14c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1673,50,42" v="6-35"/>
<c id="p1C_mR_r14c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1673,170,42" v="install 巢狀"/>
<c id="p1C_mR_r14c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1673,530,42" v="&amp;lt;dir&amp;gt; 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。（結束 1）"/>
<c id="p1C_mR_r15c0" parent="p1C" st="f=#ffffff;s=#999999;b=1" g="790,1715,50,42" v="6-36"/>
<c id="p1C_mR_r15c1" parent="p1C" st="f=#ffffff;s=#999999" g="840,1715,170,42" v="舊薄殼跑新 major 一般動詞"/>
<c id="p1C_mR_r15c2" parent="p1C" st="f=#ffffff;s=#999999" g="1010,1715,530,42" v="薄殼協定 &amp;lt;P_shell&amp;gt; 低於引擎 &amp;lt;vY&amp;gt; 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit（結束 3、零寫入）"/>
<c id="p1c_lg0" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="40,1903,130,40" v="綠底：常用動詞"/>
<c id="p1c_lg1" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="190,1903,130,40" v="白底：進階動詞"/>
<c id="p1c_lg2" st="f=#ffe6cc;s=#d79b00;fs=14" g="340,1903,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p1c_lg3" st="f=#e6e6e6;s=#999999;b=1" g="550,1903,110,40" v="灰底：表頭"/>
<c id="p1c_lg4" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="680,1903,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p1c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="900,1903,200,40" v="右上角綠標籤：v2 改"/>
<c id="p1c_lg5_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1068,1905,30,20" v="v2"/>
<c id="p1c_lgt" st="text;s=none;f=none" g="1120,1893,300,60" v="「反向」= 收回它做的事的動詞&lt;br&gt;表格：一列一個選項／結束碼／訊息"/>
<c id="p1c_lg6" st="shape=note;f=#ffffff;s=#999999" g="40,1969,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p1c_th" st="text;fs=13;s=none;f=none;b=1" g="40,2025,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p1c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,2059,150,40" v="組（常用／進階／一次性）"/>
<c id="p1c_tv0" st="f=#ffffff;s=#999999" g="190,2059,610,40" v="常用 = 每天會打的（add／upgrade／dev）；進階 = 偶爾才用；一次性 = 只在第一次接入跑的 bootstrap.sh（release 附的腳本，不是 just 動詞）"/>
<c id="p1c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2099,150,40" v="反向"/>
<c id="p1c_tv1" st="f=#ffffff;s=#999999" g="190,2099,610,40" v="把該動詞做的事收回的動詞（install↔uninstall、add↔remove、dev↔undev）；upgrade 沒有動詞反向，靠 git revert（把整組升級 commit 反做一次的 git 指令）"/>
<c id="p1c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2139,150,28" v="apt 語意"/>
<c id="p1c_tv2" st="f=#ffffff;s=#999999" g="190,2139,610,28" v="跟 Debian 的 apt 一樣分兩步：update 只查有沒有新版、不動檔；upgrade 才真的套用"/>
<c id="p1c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2167,150,40" v="--local 值的判別"/>
<c id="p1c_tv3" st="f=#ffffff;s=#999999" g="190,2167,610,40" v="已定：--local &amp;lt;值&amp;gt; 含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立（tag 含 / 且存在同名檔）→ 1 提示用 ./ 或完整 ref 消歧"/>
<c id="p1c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2207,150,40" v="pull 逾時"/>
<c id="p1c_tv4" st="f=#ffffff;s=#999999" g="190,2207,610,40" v="VENDOR_KIT_PULL_TIMEOUT／--timeout &amp;lt;秒&amp;gt;：單次 pull 總秒數，預設 300、只收正整數；逾時 → 1 印 6-31；啟動器自讀、不轉發引擎"/>
<c id="p1c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2247,150,55" v="結束碼 0／1／2／3"/>
<c id="p1c_tv5" st="f=#ffffff;s=#999999" g="190,2247,610,55" v="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入"/>
<c id="p1c_tk6" st="f=#ffffff;s=#999999;b=1" g="840,2059,150,40" v="--protocol P"/>
<c id="p1c_tv6" st="f=#ffffff;s=#999999" g="990,2059,610,40" v="薄殼每次呼叫引擎都附的協定整數（第一版 P=1，在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 回應；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用"/>
<c id="p1c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2099,150,40" v="floor"/>
<c id="p1c_tv7" st="f=#ffffff;s=#999999" g="990,2099,610,40" v="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）"/>
<c id="p1c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2139,150,55" v="mod／mod?／import／import?"/>
<c id="p1c_tv8" st="f=#ffffff;s=#999999" g="990,2139,610,55" v="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）"/>
<c id="p1c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2194,150,71" v="專案根"/>
<c id="p1c_tv9" st="f=#ffffff;s=#999999" g="990,2194,610,71" v="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git"/>
</page>
<page name="契約 v2：目錄樹與檔案範例">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約② 專案裡的檔（1／3）── 目錄樹與檔案範例（interface_spec §4；誰寫它、誰可以改、進不進 git）"/>
<c id="p2_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p2_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,81" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;檔名 version.toml 已定（§4.1：它是「該裝哪版」的宣告，不是 lock 產物）；右欄範例框逐字（等寬、保留縮排），說明一律放框外"/>
<c id="p2_lbl" st="text;fs=13;s=none;f=none;b=1" g="40,109,620,28" v="3. 目錄樹（專案根 = 含 .vendor_kit/ 的目錄；每格：用途｜寫：誰產生｜改：誰可改）"/>
<c id="t_root" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="40,143,200,46" v="&lt;b&gt;專案/&lt;/b&gt;（使用者的；專案根）"/>
<c id="t_just" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="70,197,560,77" v="&lt;b&gt;justfile&lt;/b&gt; ── 使用者的 just 入口；install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;（無 → 建四行；有 → 問／-y；已含 → 不再加）&lt;br&gt;寫：install｜改：使用者隨意；uninstall 問後只刪完全相同的那行；add 只讀它查撞名"/>
<c id="t_just_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,199,30,20" v="v2"/>
<c id="t_di" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="70,282,560,77" v="&lt;b&gt;.dockerignore&lt;/b&gt; ── 使用者的；install 加三行 .vendor_kit/cache/、gen/、.tmp.*（無 → 建；有 → 問 6-34／-y）&lt;br&gt;寫：install（記於 baseline/.vendor_kit.toml）｜改：使用者隨意；uninstall 問後只刪原文相同行"/>
<c id="t_di_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,284,30,20" v="v2"/>
<c id="t_vk" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="70,367,560,77" v="&lt;b&gt;.vendor_kit/&lt;/b&gt; ── 根目錄只多這一個；薄殼 + 狀態 + 快取都在裡面；上層或下層不得再有一個（禁止巢狀）&lt;br&gt;寫：install、upgrade vendor_kit 重產薄殼（先比對薄殼首行）｜改：人不改；uninstall 只刪 hash 相符的自產檔"/>
<c id="t_vk_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,369,30,20" v="v2"/>
<c id="t_ver" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,452,530,77" v="&lt;b&gt;version.toml&lt;/b&gt; ── 進 git：唯一來源。vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot; 正規行（唯一）、schema、written_by、[tools] 一行一工具 tag@digest&lt;br&gt;寫：install／add／upgrade／remove（apply 最後才寫）｜改：使用者可手改、Renovate PR 改；sync 只讀"/>
<c id="t_ver_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,454,30,20" v="v2"/>
<c id="t_vl" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="100,537,530,108" v="&lt;b&gt;version.local.toml&lt;/b&gt; ── 不進 git（自有 .gitignore 擋）；與 version.toml 同形：工具覆寫 path:&amp;lt;dir&amp;gt;；引擎覆寫 tag + vendor_kit_image_id&lt;br&gt;寫：dev／undev（含 image ID）；bootstrap --local 在 install 成功後才寫｜改：不建議手改；uninstall hash 相符才刪；CI 為真下有任何覆寫 → sync 回 1"/>
<c id="t_vl_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,539,30,20" v="v2"/>
<c id="t_gi" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,653,530,61" v="&lt;b&gt;.gitignore&lt;/b&gt; ── 進 git，我們自己的：cache/ gen/ version.local.toml .tmp.*；第一行自描述&lt;br&gt;寫：install／upgrade vendor_kit 重產｜改：人不改"/>
<c id="t_gi_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,655,30,20" v="v2"/>
<c id="t_entry" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,722,530,61" v="&lt;b&gt;entry.just&lt;/b&gt; ── 進 git：mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;（零 set 零 recipe）；第一行自描述&lt;br&gt;寫：引擎 launcher-gen（install／upgrade vendor_kit）｜改：人不改"/>
<c id="t_entry_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,724,30,20" v="v2"/>
<c id="t_vj" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,791,530,77" v="&lt;b&gt;vendor.just&lt;/b&gt; ── 進 git：動詞 recipe 一行轉發 + 啟動器本體（POSIX sh；set positional-arguments 只放這；附 --protocol P）；第一行自描述&lt;br&gt;寫：引擎 launcher-gen｜改：人不改"/>
<c id="t_vj_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,793,30,20" v="v2"/>
<c id="t_ci" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,876,530,61" v="&lt;b&gt;ci/check.sh&lt;/b&gt; ── 進 git：下游 CI 呼叫的契約檢查（⓪–⑤ 六步，契約⑤ p3c）；第一行 shebang、第二行自描述、之後 export CI=1&lt;br&gt;寫：引擎 launcher-gen｜改：人不改"/>
<c id="t_ci_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,878,30,20" v="v2"/>
<c id="t_bl" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="100,945,530,92" v="&lt;b&gt;baseline/&lt;/b&gt; ── 進 git：install 建 .gitkeep（git 不追蹤空目錄）；&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；.vendor_kit.toml = install 對根 .dockerignore 的 append 記錄&lt;br&gt;寫：install（.gitkeep）；add 建 &amp;lt;repo&amp;gt;/、upgrade 推進（有衝突仍推）｜改：人不改（改了合併就錯）"/>
<c id="t_bl_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,947,30,20" v="v2"/>
<c id="t_meta" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="130,1045,500,61" v="&lt;b&gt;&amp;lt;repo&amp;gt;/.vendor_kit.toml&lt;/b&gt; ── 進 git：metadata（欄位見 p2b）；兼作該目錄佔位&lt;br&gt;寫：add／upgrade（install 不建）｜改：人不改"/>
<c id="t_meta_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1047,30,20" v="v2"/>
<c id="t_gen" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="100,1114,530,46" v="&lt;b&gt;gen/&lt;/b&gt; ── 不進 git：引擎產生的三種檔（下列三格），各自由不同動詞寫&lt;br&gt;寫：引擎｜改：人不改（會被覆蓋）"/>
<c id="t_gen_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1116,30,20" v="v2"/>
<c id="t_tools" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1168,500,92" v="&lt;b&gt;tools.just&lt;/b&gt; ── 每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;（上方一行 # &amp;lt;description&amp;gt;；零 set 零 recipe）&lt;br&gt;寫：sync／add／remove／upgrade 重生（最後寫、與 cache 同一 apply 內原子替換）｜改：人不改"/>
<c id="t_tools_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1170,30,20" v="v2"/>
<c id="t_gstamp" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1268,500,61" v="&lt;b&gt;.stamp&lt;/b&gt; ── 只記產生薄殼的引擎 ref（一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1（不重寫）&lt;br&gt;寫：只由 install／upgrade vendor_kit｜改：人不改"/>
<c id="t_gstamp_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1270,30,20" v="v2"/>
<c id="t_rstamp" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1337,500,61" v="&lt;b&gt;&amp;lt;repo&amp;gt;.stamp&lt;/b&gt; ── 每工具一個印記：第一行 index digest（dev 時 path:&amp;lt;dir&amp;gt;），之後每檔 sha256；sync 用它決定要不要 materialize&lt;br&gt;寫：引擎 materialize｜改：不可改"/>
<c id="t_rstamp_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1339,30,20" v="v2"/>
<c id="t_repo" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="100,1406,530,77" v="&lt;b&gt;cache/&amp;lt;repo&amp;gt;/&lt;/b&gt; ── 不進 git、使用者不可改；只放從暫存 /dist 展開的內容（dev 時是 symlink → &amp;lt;dir&amp;gt;/dist）&lt;br&gt;寫：引擎 materialize（apply 決定套用之後）｜改：不可改（verify 失敗 → 重裝並 warn）"/>
<c id="t_repo_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1408,30,20" v="v2"/>
<c id="t_files" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1491,500,46" v="&lt;b&gt;files/ …&lt;/b&gt; ── 工具檔案（dist/files/ 全部；無 symlink，展開時驗）｜寫：materialize｜改：不可改"/>
<c id="t_init" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1545,500,61" v="&lt;b&gt;init.toml&lt;/b&gt; ── 初始檔清單（[[file]] src／dest／strategy = &quot;copy&quot;|&quot;append&quot;；schema；description）｜寫：materialize｜改：不可改"/>
<c id="t_init_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1547,30,20" v="v2"/>
<c id="t_rjust" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="130,1614,500,46" v="&lt;b&gt;just/&amp;lt;ns&amp;gt;.just&lt;/b&gt; ── 工具的 just 模組，每檔一個頂層命名空間（&amp;lt;repo&amp;gt;.just 必有；含私有 _sync）｜寫：materialize｜改：不可改"/>
<c id="t_rjust_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1616,30,20" v="v2"/>
<c id="t_tmp" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="100,1668,530,92" v="&lt;b&gt;.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml&lt;/b&gt; ── 不進 git：進度日誌（remove／uninstall／undev／prune／修復型 install；add／upgrade 記在 metadata）&lt;br&gt;寫：apply 第一個寫入前建、最後一步刪｜改：人不改；未完成 → 可寫動詞先恢復、sync／update 印 6-33 結束 1、help 印 6-33 仍 0"/>
<c id="t_tmp_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1670,30,20" v="v2"/>
<c id="t_tmpd" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="100,1768,530,61" v="&lt;b&gt;.tmp.dist.&amp;lt;id&amp;gt;/&lt;/b&gt; ── 不進 git：啟動器暫存目錄（展開的 dist、vk-resolve 輸出）&lt;br&gt;寫：啟動器 mktemp、trap 刪｜改：人不改；失效殘留由 prune 清"/>
<c id="t_tmpd_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1770,30,20" v="v2"/>
<c id="t_user" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="70,1837,560,77" v="&lt;b&gt;初始檔&lt;/b&gt;（例 Dockerfile…；路徑由 init.toml 的 dest 決定）── 使用者的；進 git；state 記在 metadata（五態）&lt;br&gt;寫：add 建（已存在不納管；append 問後加行）、upgrade 逐檔問後換／三方合併／建新檔｜改：使用者隨意；remove／uninstall 永不刪，印清單"/>
<c id="t_user_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="598,1839,30,20" v="v2"/>
<c id="te1" edge source="t_root" target="t_just" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="54,235.5"/>
<c id="te21" edge source="t_root" target="t_di" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="54,320.5"/>
<c id="te2" edge source="t_root" target="t_vk" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="54,405.5"/>
<c id="te3" edge source="t_vk" target="t_ver" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,490.5"/>
<c id="te4" edge source="t_vk" target="t_vl" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,591.0"/>
<c id="te5" edge source="t_vk" target="t_gi" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,683.5"/>
<c id="te6" edge source="t_vk" target="t_entry" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,752.5"/>
<c id="te7" edge source="t_vk" target="t_vj" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,829.5"/>
<c id="te8" edge source="t_vk" target="t_ci" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,906.5"/>
<c id="te9" edge source="t_vk" target="t_bl" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,991.0"/>
<c id="te10" edge source="t_bl" target="t_meta" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1075.5"/>
<c id="te11" edge source="t_vk" target="t_gen" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,1137.0"/>
<c id="te12" edge source="t_gen" target="t_tools" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1214.0"/>
<c id="te13" edge source="t_gen" target="t_gstamp" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1298.5"/>
<c id="te15" edge source="t_gen" target="t_rstamp" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1367.5"/>
<c id="te14" edge source="t_vk" target="t_repo" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,1444.5"/>
<c id="te16" edge source="t_repo" target="t_files" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1514.0"/>
<c id="te17" edge source="t_repo" target="t_init" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1575.5"/>
<c id="te18" edge source="t_repo" target="t_rjust" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="114,1637.0"/>
<c id="te20" edge source="t_vk" target="t_tmp" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,1714.0"/>
<c id="te22" edge source="t_vk" target="t_tmpd" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="84,1798.5"/>
<c id="te19" edge source="t_root" target="t_user" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="54,1875.5"/>
<c id="p2_ver_l" st="text;fs=13;s=none;f=none;b=1" g="660,109,940,28" v=".vendor_kit/version.toml（進 git；schema = 1）── 啟動器只靠 grep 讀正規行"/>
<c id="p2_ver" st="f=#ffffff;s=#999999" g="660,141,497,108" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:v1.0.0@sha256:&amp;lt;digest&amp;gt;&quot;&lt;br&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;&lt;br&gt;[tools]&lt;br&gt;&amp;lt;repo&amp;gt; = &quot;ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:v2.3.0@sha256:&amp;lt;digest&amp;gt;&quot;&lt;/pre&gt;"/>
<c id="p2_ver_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1125,143,30,20" v="v2"/>
<c id="p2_ver_n" st="f=#ffffff;s=#999999;fs=14" g="1169,141,431,108" v="第 1 行 = 唯一正規行：行首無空白、鍵後一空白、=、一空白、雙引號、&lt;b&gt;無尾端註解&lt;/b&gt;、LF（regex 讀不到就是 1）&lt;br&gt;schema：格式版本，引擎讀、啟動器不讀；written_by：寫入引擎版本，純資訊&lt;br&gt;[tools]：每工具一行 tag@digest（多架構 index digest）"/>
<c id="p2_vl_l" st="text;fs=13;s=none;f=none;b=1" g="660,263,940,28" v=".vendor_kit/version.local.toml（不進 git；與 version.toml 同形）── dev 寫、undev 刪、bootstrap --local 寫"/>
<c id="p2_vl" st="f=#ffffff;s=#999999" g="660,295,346,124" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;vendor_kit:dev&quot;&lt;br&gt;vendor_kit_image_id = &quot;sha256:&amp;lt;image id&amp;gt;&quot;&lt;br&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;&lt;br&gt;[tools]&lt;br&gt;&amp;lt;repo&amp;gt; = &quot;path:/home/me/&amp;lt;repo&amp;gt;&quot;&lt;/pre&gt;"/>
<c id="p2_vl_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="974,297,30,20" v="v2"/>
<c id="p2_vl_n" st="f=#ffffff;s=#999999;fs=14" g="1018,295,582,124" v="vendor_kit：dev vendor_kit -i &amp;lt;tag&amp;gt; 寫的本機引擎 image，只能 tag（docker load 後無 RepoDigests）；同樣是正規行、無尾端註解&lt;br&gt;vendor_kit_image_id：啟動器每次 docker image inspect 比對、不 pull；同 tag 重 build 才會被發現；undev 一併撤&lt;br&gt;[tools].&amp;lt;repo&amp;gt;：dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt; 寫 path:&amp;lt;dir&amp;gt;；cache/&amp;lt;repo&amp;gt;/ 變 symlink → &amp;lt;dir&amp;gt;/dist；啟動器掛 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro"/>
<c id="p2_jf_l" st="text;fs=13;s=none;f=none;b=1" g="660,433,940,28" v="根 justfile（使用者的；install 新建時逐字四行；已有時只加第一行）"/>
<c id="p2_jf" st="f=#ffffff;s=#999999" g="660,465,300,77" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;br&gt;&lt;br&gt;default:&lt;br&gt;&#9;@just --list&lt;/pre&gt;"/>
<c id="p2_jf_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,467,30,20" v="v2"/>
<c id="p2_jf_n" st="f=#ffffff;s=#999999;fs=14" g="972,465,628,77" v="第 4 行行首是&lt;b&gt;真 tab&lt;/b&gt;（recipe 本體必須縮排；default: @just --list 寫成單行是 just 語法錯誤，所以拆兩行）&lt;br&gt;已有 justfile → 問 6-20 只加第 1 行；uninstall 只刪完全相同的那行"/>
<c id="p2_di_l" st="text;fs=13;s=none;f=none;b=1" g="660,556,940,28" v="根 .dockerignore（使用者的；install append 三行；uninstall 問後只刪原文相同行）"/>
<c id="p2_di" st="f=#ffffff;s=#999999" g="660,588,300,61" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;"/>
<c id="p2_di_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,590,30,20" v="v2"/>
<c id="p2_di_n" st="f=#ffffff;s=#999999;fs=14" g="972,588,628,61" v="無 → 建；有 → 問 6-34 後 append（-y 免問）；插入的行記於 baseline/.vendor_kit.toml&lt;br&gt;工具以專案根當 build context 時靠它排除 cache"/>
<c id="p2_tj_l" st="text;fs=13;s=none;f=none;b=1" g="660,663,940,28" v=".vendor_kit/gen/tools.just（不進 git；每個 &amp;lt;ns&amp;gt;.just 一行 mod?；零 set 零 recipe）"/>
<c id="p2_tj" st="f=#ffffff;s=#999999" g="660,695,353,46" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# &amp;lt;description&amp;gt;&lt;br&gt;mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;&lt;/pre&gt;"/>
<c id="p2_tj_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="981,697,30,20" v="v2"/>
<c id="p2_tj_n" st="f=#ffffff;s=#999999;fs=14" g="1025,695,575,46" v="# &amp;lt;description&amp;gt;：來自 init.toml 頂層 description；缺則 &amp;lt;repo&amp;gt; &amp;lt;tag&amp;gt;&lt;br&gt;mod?：cache 缺檔時其他 recipe 與 just vendor_kit sync 仍可跑"/>
<c id="p2_sh_l" st="text;fs=13;s=none;f=none;b=1" g="660,755,940,28" v="薄殼自描述首行（entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行）"/>
<c id="p2_sh" st="f=#ffffff;s=#999999" g="660,787,396,61" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# vendor_kit-shell/1 engine=v1.0.0 sha256=&amp;lt;hash&amp;gt;&lt;/pre&gt;"/>
<c id="p2_sh_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1024,789,30,20" v="v2"/>
<c id="p2_sh_n" st="f=#ffffff;s=#999999;fs=14" g="1068,787,532,61" v="&amp;lt;P&amp;gt; = 協定版本（1）、engine = 產生它的引擎；&amp;lt;hash&amp;gt; = 其餘內容 CRLF→LF 正規化後的 sha256&lt;br&gt;引擎重算 hash + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動"/>
<c id="p2_st_l" st="text;fs=13;s=none;f=none;b=1" g="660,862,940,28" v=".vendor_kit/gen/&amp;lt;repo&amp;gt;.stamp（每工具印記；materialize 寫）"/>
<c id="p2_st" st="f=#ffffff;s=#999999" g="660,894,300,77" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;sha256:&amp;lt;hex64&amp;gt;&lt;br&gt;&amp;lt;sha256&amp;gt;  files/…&lt;br&gt;&amp;lt;sha256&amp;gt;  init.toml&lt;br&gt;&amp;lt;sha256&amp;gt;  just/&amp;lt;ns&amp;gt;.just&lt;/pre&gt;"/>
<c id="p2_st_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,896,30,20" v="v2"/>
<c id="p2_st_n" st="f=#ffffff;s=#999999;fs=14" g="972,894,628,77" v="第 1 行：多架構 index digest（add --local 亦為正式 digest）；dev 時 path:&amp;lt;dir&amp;gt;；無 image:&amp;lt;tag&amp;gt; 形&lt;br&gt;之後每檔一行 &amp;lt;sha256&amp;gt;  &amp;lt;相對路徑&amp;gt;；verify 逐檔比；檔內沒有註解"/>
<c id="p2_gs_l" st="text;fs=13;s=none;f=none;b=1" g="660,985,940,28" v=".vendor_kit/gen/.stamp（只由 install／upgrade vendor_kit 寫）"/>
<c id="p2_gs" st="f=#ffffff;s=#999999" g="660,1017,389,46" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:v1.0.0@sha256:&amp;lt;digest&amp;gt;&lt;/pre&gt;"/>
<c id="p2_gs_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1017,1019,30,20" v="v2"/>
<c id="p2_gs_n" st="f=#ffffff;s=#999999;fs=14" g="1061,1017,539,46" v="唯一一行：產生薄殼的引擎 ref（local 覆寫時為 &amp;lt;tag&amp;gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1"/>
<c id="p2_tv_l" st="text;fs=13;s=none;f=none;b=1" g="660,1077,940,28" v=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（修復型 install／remove／uninstall／undev／prune 進度日誌；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機）"/>
<c id="p2_tv" st="f=#ffffff;s=#999999" g="660,1109,300,155" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1&lt;br&gt;written_by = &quot;v1.0.0&quot;&lt;br&gt;verb = &quot;remove&quot;&lt;br&gt;id = &quot;&amp;lt;id&amp;gt;&quot;&lt;br&gt;targets = [&quot;&amp;lt;repo&amp;gt;&quot;]&lt;br&gt;started = &quot;&amp;lt;UTC ISO 8601&amp;gt;&quot;&lt;br&gt;done = [...]&lt;br&gt;pending = [...]&lt;br&gt;consents = [...]&lt;/pre&gt;"/>
<c id="p2_tv_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,1111,30,20" v="v2"/>
<c id="p2_tv_n" st="f=#ffffff;s=#999999;fs=14" g="972,1109,628,155" v="consents = 已取得的同意；done／pending = 已完成／未完成步驟&lt;br&gt;第一個寫入前建、成功結束時整個檔刪除；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33"/>
<c id="p2_th" st="text;fs=13;s=none;f=none;b=1" g="660,1284,200,28" v="本頁名詞"/>
<c id="p2_tk0" st="f=#ffffff;s=#999999;b=1" g="660,1318,150,30" v="唯一來源"/>
<c id="p2_tv0" st="f=#ffffff;s=#999999" g="810,1318,790,30" v="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導"/>
<c id="p2_tk1" st="f=#ffffff;s=#999999;b=1" g="660,1348,150,57" v="vendor_kit = 正規行"/>
<c id="p2_tv1" st="f=#ffffff;s=#999999" g="810,1348,790,57" v="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路"/>
<c id="p2_tk2" st="f=#ffffff;s=#999999;b=1" g="660,1405,150,42" v="version.local.toml"/>
<c id="p2_tv2" st="f=#ffffff;s=#999999" g="810,1405,790,42" v="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1"/>
<c id="p2_tk3" st="f=#ffffff;s=#999999;b=1" g="660,1447,150,42" v="image ID"/>
<c id="p2_tv3" st="f=#ffffff;s=#999999" g="810,1447,790,42" v="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對"/>
<c id="p2_tk4" st="f=#ffffff;s=#999999;b=1" g="660,1489,150,42" v="薄殼"/>
<c id="p2_tv4" st="f=#ffffff;s=#999999" g="810,1489,790,42" v=".vendor_kit/ 進 git、vendor_kit 擁有、人不改的四檔：entry.just、vendor.just、.gitignore、ci/check.sh；只轉發、不做事；每檔自描述首行；只由 install／upgrade vendor_kit 重產"/>
<c id="p2_tk5" st="f=#ffffff;s=#999999;b=1" g="660,1531,150,42" v="薄殼自描述首行"/>
<c id="p2_tv5" st="f=#ffffff;s=#999999" g="810,1531,790,42" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動"/>
<c id="p2_tk6" st="f=#ffffff;s=#999999;b=1" g="660,1573,150,42" v="gen/"/>
<c id="p2_tv6" st="f=#ffffff;s=#999999" g="810,1573,790,42" v="引擎產生的檔，不進 git，三種：tools.just（sync／add／remove／upgrade 重生）、.stamp（只由 install／upgrade vendor_kit 寫）、&amp;lt;repo&amp;gt;.stamp（materialize 寫）"/>
<c id="p2_tk7" st="f=#ffffff;s=#999999;b=1" g="660,1615,150,42" v="gen/.stamp"/>
<c id="p2_tv7" st="f=#ffffff;s=#999999" g="810,1615,790,42" v="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行"/>
<c id="p2_tk8" st="f=#ffffff;s=#999999;b=1" g="660,1657,150,42" v="印記 gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p2_tv8" st="f=#ffffff;s=#999999" g="810,1657,790,42" v="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&amp;lt;dir&amp;gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref"/>
<c id="p2_tk9" st="f=#ffffff;s=#999999;b=1" g="660,1699,150,57" v="mod／mod?／import／import?"/>
<c id="p2_tv9" st="f=#ffffff;s=#999999" g="810,1699,790,57" v="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）"/>
<c id="p2_tk10" st="f=#ffffff;s=#999999;b=1" g="660,1756,150,42" v="cache/&amp;lt;repo&amp;gt;/"/>
<c id="p2_tv10" st="f=#ffffff;s=#999999" g="810,1756,790,42" v="工具 image 的 /dist 展開副本，收在 .vendor_kit/ 裡；不進 git、不可改；dev 時是 symlink → &amp;lt;dir&amp;gt;/dist；印記不在這裡（在 gen/&amp;lt;repo&amp;gt;.stamp）"/>
<c id="p2_tk11" st="f=#ffffff;s=#999999;b=1" g="660,1798,150,42" v="初始檔"/>
<c id="p2_tv11" st="f=#ffffff;s=#999999" g="810,1798,790,42" v="工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata"/>
<c id="p2_tk12" st="f=#ffffff;s=#999999;b=1" g="660,1840,150,42" v="初始檔五態（state）"/>
<c id="p2_tv12" st="f=#ffffff;s=#999999" g="810,1840,790,42" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"/>
<c id="p2_tk13" st="f=#ffffff;s=#999999;b=1" g="660,1882,150,42" v="baseline"/>
<c id="p2_tv13" st="f=#ffffff;s=#999999" g="810,1882,790,42" v=".vendor_kit/baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep"/>
<c id="p2_tk14" st="f=#ffffff;s=#999999;b=1" g="660,1924,150,42" v="baseline/.gitkeep"/>
<c id="p2_tv14" st="f=#ffffff;s=#999999" g="810,1924,790,42" v="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 兼作該工具目錄的佔位）"/>
<c id="p2_tk15" st="f=#ffffff;s=#999999;b=1" g="660,1966,150,57" v="進度日誌檔 .tmp.*"/>
<c id="p2_tv15" st="f=#ffffff;s=#999999" g="810,1966,790,57" v="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪"/>
<c id="p2_tk16" st="f=#ffffff;s=#999999;b=1" g="660,2023,150,42" v="暫存 .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p2_tv16" st="f=#ffffff;s=#999999" g="810,2023,790,42" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋"/>
<c id="p2_tk17" st="f=#ffffff;s=#999999;b=1" g="660,2065,150,42" v="根 justfile 四行"/>
<c id="p2_tv17" st="f=#ffffff;s=#999999" g="810,2065,790,42" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行"/>
<c id="p2_tk18" st="f=#ffffff;s=#999999;b=1" g="660,2107,150,57" v="根 .dockerignore 三行"/>
<c id="p2_tv18" st="f=#ffffff;s=#999999" g="810,2107,790,57" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache"/>
<c id="p2_tk19" st="f=#ffffff;s=#999999;b=1" g="660,2164,150,57" v="專案根"/>
<c id="p2_tv19" st="f=#ffffff;s=#999999" g="810,2164,790,57" v="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &amp;lt;dir&amp;gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git"/>
<c id="p2_lg0" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="40,2251.0,120,40" v="綠框：進 git"/>
<c id="p2_lg1" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="180,2251.0,200,40" v="灰虛線：不進 git（可重建）"/>
<c id="p2_lg2" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="400,2251.0,230,40" v="黃底綠框：使用者的檔（進 git）"/>
<c id="p2_lg3" st="f=#ffffff;s=#999999" g="650,2251.0,170,40" v="等寬字：檔案內容範例"/>
<c id="p2_lg4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="840,2251.0,200,40" v="右上角綠標籤：v2 改"/>
<c id="p2_lg4_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1008,2253.0,30,20" v="v2"/>
<c id="p2_lg5" st="shape=note;f=#ffffff;s=#999999" g="1060,2251.0,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p2_lgt" st="text;s=none;f=none" g="1300,2241.0,300,60" v="樹線 = 目錄包含；範例框右邊 = 框外說明&lt;br&gt;綠標籤 = v2 改；schema 表 p2b、矩陣 p2c"/>
</page>
<page name="契約 v2：schema：version.toml／local／metadata／印記／薄殼首行">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約② 專案裡的檔（2／3）── schema：version.toml／version.local.toml／metadata／印記／薄殼首行（interface_spec §4）"/>
<c id="p2b_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p2b_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;欄位名、型別、必填以 interface_spec §4 為準；範例見 p2；動詞 × 檔案矩陣見 p2c"/>
<c id="p2B" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,1372" v="4. 檔案 schema（欄位／型別／必填／說明；一列一欄位）"/>
<c id="p2b_gen" parent="p2B" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,50,750,92" v="&lt;b&gt;TOML 通則（所有 vendor_kit 寫的檔）&lt;/b&gt;&lt;br&gt;每檔 schema = N（integer）+ written_by = &quot;&amp;lt;vX&amp;gt;&quot;（string，純資訊，不作讀取門檻）；讀取門檻只看 schema；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯、重複宣告 → 1；schema 高於本引擎支援 → 3 印 6-19 零寫入；讀任一舊 schema → 直接寫當前 schema（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。第一版 schema = 1"/>
<c id="p2b_gen_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,52,30,20" v="v2"/>
<c id="p2b_ver_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="20,156,750,28" v="4.1 .vendor_kit/version.toml"/>
<c id="p2b_ver_m" parent="p2B" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="20,188,750,30" v="進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；使用者、Renovate 可手改；sync 只讀"/>
<c id="p2b_canon" parent="p2B" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,232,750,108" v="&lt;b&gt;version.toml 正規行契約&lt;/b&gt;&lt;br&gt;vendor_kit 行唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號基本字串、無尾端註解、LF 結尾）；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：^vendor_kit[[:space:]]*=[[:space:]]*&quot;\([^&quot;]*\)&quot;[[:space:]]*$（POSIX BRE，不用 \s）；命中數必須恰為 1（grep -c），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 [tools] 之前。禁止：BOM、重複鍵、[vendor_kit] 表旁路等 regex 讀不到／讀錯的等價寫法。公開格式：工具可讀它寫來源紀錄"/>
<c id="p2b_canon_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,234,30,20" v="v2"/>
<c id="p2b_ver_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="20,354,190,30" v="欄位"/>
<c id="p2b_ver_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="210,354,130,30" v="型別／必填"/>
<c id="p2b_ver_h2" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="340,354,430,30" v="說明"/>
<c id="p2b_ver_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,384,190,42" v="vendor_kit"/>
<c id="p2b_ver_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,384,130,42" v="string／是"/>
<c id="p2b_ver_r0c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,384,430,42" v="引擎 ref ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;digest&amp;gt;（多架構 index digest）"/>
<c id="p2b_ver_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,426,190,26" v="schema"/>
<c id="p2b_ver_r1c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,428,30,20" v="v2"/>
<c id="p2b_ver_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,426,130,26" v="integer／是"/>
<c id="p2b_ver_r1c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,426,430,26" v="啟動器不讀、只引擎讀"/>
<c id="p2b_ver_r2c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,452,190,26" v="written_by"/>
<c id="p2b_ver_r2c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,454,30,20" v="v2"/>
<c id="p2b_ver_r2c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,452,130,26" v="string／是"/>
<c id="p2b_ver_r2c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,452,430,26" v="寫入引擎版本，純資訊"/>
<c id="p2b_ver_r3c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,478,190,57" v="[tools].&amp;lt;repo&amp;gt;"/>
<c id="p2b_ver_r3c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,478,130,57" v="string／每工具"/>
<c id="p2b_ver_r3c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,478,430,57" v="ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;@sha256:&amp;lt;digest&amp;gt;（index digest；add --local 亦寫正式 index digest，來自 .digest 旁檔）"/>
<c id="p2b_vl_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="20,549,750,28" v="4.2 .vendor_kit/version.local.toml"/>
<c id="p2b_vl_m" parent="p2B" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="20,581,750,61" v="不進 git（自有 .gitignore 擋）；與 version.toml 同形（同一套讀寫器）；寫入者 dev／undev／bootstrap --local；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；frozen 下存在任何覆寫 → sync 回 1；啟動器先讀它再退回 version.toml"/>
<c id="p2b_vl_m_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,583,30,20" v="v2"/>
<c id="p2b_vl_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="20,656,190,30" v="欄位"/>
<c id="p2b_vl_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="210,656,130,30" v="型別／必填"/>
<c id="p2b_vl_h2" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="340,656,430,30" v="說明"/>
<c id="p2b_vl_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,686,190,26" v="vendor_kit"/>
<c id="p2b_vl_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,686,130,26" v="string／否"/>
<c id="p2b_vl_r0c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,686,430,26" v="本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）"/>
<c id="p2b_vl_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,712,190,57" v="vendor_kit_image_id"/>
<c id="p2b_vl_r1c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,714,30,20" v="v2"/>
<c id="p2b_vl_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,712,130,57" v="string／有 vendor_kit 時必填"/>
<c id="p2b_vl_r1c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,712,430,57" v="sha256:&amp;lt;hex64&amp;gt;，dev 時解析；啟動器每次 docker image inspect 比對，同 tag 重 build 才會被發現；undev vendor_kit 一併撤"/>
<c id="p2b_vl_r2c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,769,190,26" v="schema"/>
<c id="p2b_vl_r2c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,771,30,20" v="v2"/>
<c id="p2b_vl_r2c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,769,130,26" v="integer／是"/>
<c id="p2b_vl_r2c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,769,430,26" v="同通則（讀取門檻）"/>
<c id="p2b_vl_r3c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,795,190,26" v="written_by"/>
<c id="p2b_vl_r3c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,797,30,20" v="v2"/>
<c id="p2b_vl_r3c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,795,130,26" v="string／是"/>
<c id="p2b_vl_r3c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,795,430,26" v="同通則（純資訊）"/>
<c id="p2b_vl_r4c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,821,190,42" v="[tools].&amp;lt;repo&amp;gt;"/>
<c id="p2b_vl_r4c1" parent="p2B" st="f=#ffffff;s=#999999" g="210,821,130,42" v="string／否"/>
<c id="p2b_vl_r4c2" parent="p2B" st="f=#ffffff;s=#999999" g="340,821,430,42" v="path:&amp;lt;dir&amp;gt;（絕對路徑）；cache/&amp;lt;repo&amp;gt;/ 為 symlink → &amp;lt;dir&amp;gt;/dist"/>
<c id="p2b_gen_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="20,877,750,28" v="4.4 gen/.stamp、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just（不進 git）"/>
<c id="p2b_gn_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="20,909,180,30" v="檔"/>
<c id="p2b_gn_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="200,909,180,30" v="寫入者"/>
<c id="p2b_gn_h2" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="380,909,390,30" v="內容"/>
<c id="p2b_gn_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,939,180,57" v="gen/.stamp"/>
<c id="p2b_gn_r0c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="168,941,30,20" v="v2"/>
<c id="p2b_gn_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="200,939,180,57" v="只由 install／upgrade vendor_kit"/>
<c id="p2b_gn_r0c2" parent="p2B" st="f=#ffffff;s=#999999" g="380,939,390,57" v="第一行 = 產生薄殼的引擎 ref（local 覆寫時為 &amp;lt;tag&amp;gt;），供 sync grep 快速比對；不承擔薄殼 hash；fresh clone 缺此檔時相容判定改用薄殼自描述首行"/>
<c id="p2b_gn_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,996,180,88" v="gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p2b_gn_r1c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="168,998,30,20" v="v2"/>
<c id="p2b_gn_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="200,996,180,88" v="materialize"/>
<c id="p2b_gn_r1c2" parent="p2B" st="f=#ffffff;s=#999999" g="380,996,390,88" v="第一行 = 多架構 index digest sha256:&amp;lt;hex64&amp;gt;（與 version.toml 一致；add --local 亦為正式 index digest，本機驗證用 metadata local_image_id）或 dev 時 path:&amp;lt;dir&amp;gt;；無 image:&amp;lt;tag&amp;gt; 形；之後每檔一行 &amp;lt;sha256&amp;gt;  &amp;lt;相對路徑&amp;gt;；verify 逐檔比"/>
<c id="p2b_gn_r2c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,1084,180,73" v="gen/tools.just"/>
<c id="p2b_gn_r2c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="168,1086,30,20" v="v2"/>
<c id="p2b_gn_r2c1" parent="p2B" st="f=#ffffff;s=#999999" g="200,1084,180,73" v="sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換"/>
<c id="p2b_gn_r2c2" parent="p2B" st="f=#ffffff;s=#999999" g="380,1084,390,73" v="每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27;（一工具可多行），每行上方一行 # &amp;lt;description&amp;gt;；零 set 零 recipe"/>
<c id="p2b_tmp_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="20,1171,750,28" v="4.6 .vendor_kit/.tmp.*（皆由自有 .gitignore 的 .tmp.* 擋）"/>
<c id="p2b_tmp_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="20,1203,170,30" v="檔"/>
<c id="p2b_tmp_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="190,1203,580,30" v="內容"/>
<c id="p2b_tmp_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,1233,170,73" v=".tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml"/>
<c id="p2b_tmp_r0c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,1235,30,20" v="v2"/>
<c id="p2b_tmp_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="190,1233,580,73" v="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機，不用 &amp;lt;repo&amp;gt; 以免 uninstall 多工具撞名）；內容 = schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪；未完成 → 可寫動詞恢復、唯讀動詞印 6-33；prune 不刪未恢復者"/>
<c id="p2b_tmp_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="20,1306,170,42" v=".tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p2b_tmp_r1c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,1308,30,20" v="v2"/>
<c id="p2b_tmp_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="190,1306,580,42" v="啟動器暫存（展開的工具 dist、vk-resolve）；mktemp -d &quot;&amp;lt;專案根&amp;gt;/.vendor_kit/.tmp.dist.XXXXXX&quot;；trap 刪；prune 清殘留"/>
<c id="p2b_mt_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="790,50,750,28" v="4.3 baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（metadata）"/>
<c id="p2b_mt_m" parent="p2B" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="790,82,750,77" v="進 git；寫入者 add／upgrade；兼作 baseline/&amp;lt;repo&amp;gt;/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列。註：install 對根 .dockerignore 的三行 append 不屬任何工具，記於 baseline/.vendor_kit.toml（同 schema，只含 [[file]] dest=.dockerignore state=appended lines=三行），uninstall 讀它刪原文相同行"/>
<c id="p2b_mt_m_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,84,30,20" v="v2"/>
<c id="p2b_mt_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="790,173,190,30" v="欄位"/>
<c id="p2b_mt_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="980,173,130,30" v="型別／必填"/>
<c id="p2b_mt_h2" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="1110,173,430,30" v="說明"/>
<c id="p2b_mt_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,203,190,26" v="schema"/>
<c id="p2b_mt_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,203,130,26" v="integer／是"/>
<c id="p2b_mt_r0c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,203,430,26" v="同通則（讀取門檻）"/>
<c id="p2b_mt_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,229,190,26" v="written_by"/>
<c id="p2b_mt_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,229,130,26" v="string／是"/>
<c id="p2b_mt_r1c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,229,430,26" v="同通則（純資訊）"/>
<c id="p2b_mt_r2c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,255,190,57" v="source"/>
<c id="p2b_mt_r2c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,257,30,20" v="v2"/>
<c id="p2b_mt_r2c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,255,130,57" v="string／是"/>
<c id="p2b_mt_r2c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,255,430,57" v="這份 baseline 來自哪個工具 image &amp;lt;ref&amp;gt;（tag@index digest）= 最後合併版本；≠ version.toml → sync 本機 warn／CI 為真 1 印 6-5；upgrade 先補待合併到該版然後停"/>
<c id="p2b_mt_r3c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,312,190,42" v="local_image_id"/>
<c id="p2b_mt_r3c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,314,30,20" v="v2"/>
<c id="p2b_mt_r3c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,312,130,42" v="string／add --local 時"/>
<c id="p2b_mt_r3c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,312,430,42" v="sha256:&amp;lt;hex64&amp;gt;：本機 image ID ↔ source 的 index digest 對照，供離線驗證"/>
<c id="p2b_mt_r4c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,354,190,42" v="complete"/>
<c id="p2b_mt_r4c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,354,130,42" v="bool／是"/>
<c id="p2b_mt_r4c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,354,430,42" v="add 走完 materialize → 初始檔 → baseline 才 true；缺或 false → sync 1 印 6-13；true 且再 add → 0 無變更"/>
<c id="p2b_mt_r5c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,396,190,42" v="conflicts"/>
<c id="p2b_mt_r5c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,398,30,20" v="v2"/>
<c id="p2b_mt_r5c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,396,130,42" v="array of string／是（可空）"/>
<c id="p2b_mt_r5c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,396,430,42" v="upgrade 回 2 時留標記或解析失敗的 dest 清單；仍含標籤 → 2 停；解析失敗的 dest 其 baseline 不推；解完重跑才清空"/>
<c id="p2b_mt_r6c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,438,190,26" v="[[file]].dest"/>
<c id="p2b_mt_r6c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,438,130,26" v="string"/>
<c id="p2b_mt_r6c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,438,430,26" v="相對專案根"/>
<c id="p2b_mt_r7c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,464,190,57" v="[[file]].state"/>
<c id="p2b_mt_r7c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,466,30,20" v="v2"/>
<c id="p2b_mt_r7c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,464,130,57" v="string（單一列舉）"/>
<c id="p2b_mt_r7c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,464,430,57" v="managed（已納管）／appended（append 已插入）／declined（新增檔被拒、從未納管）／unmanaged（本來就有、沒納管）／deleted（使用者刪了已納管檔，upgrade 維持刪除）"/>
<c id="p2b_mt_r8c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,521,190,73" v="[[file]]&lt;br&gt;.declined_hash"/>
<c id="p2b_mt_r8c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,523,30,20" v="v2"/>
<c id="p2b_mt_r8c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,521,130,73" v="string／選填"/>
<c id="p2b_mt_r8c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,521,430,73" v="最近一次被拒絕的那版範本 N 的 sha256。已納管檔（managed／appended，含二進位）拒絕本次更新 → state 不變、只記此欄；新檔（從未建立）被拒 → state=declined + 此欄；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8"/>
<c id="p2b_mt_r9c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,594,190,42" v="[[file]].lines"/>
<c id="p2b_mt_r9c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,596,30,20" v="v2"/>
<c id="p2b_mt_r9c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,594,130,42" v="array of string／只在 appended"/>
<c id="p2b_mt_r9c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,594,430,42" v="實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）"/>
<c id="p2b_mt_r10c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,636,190,57" v="[progress]"/>
<c id="p2b_mt_r10c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,638,30,20" v="v2"/>
<c id="p2b_mt_r10c1" parent="p2B" st="f=#ffffff;s=#999999" g="980,636,130,57" v="table／交易中"/>
<c id="p2b_mt_r10c2" parent="p2B" st="f=#ffffff;s=#999999" g="1110,636,430,57" v="state = &quot;in-progress&quot;、started（UTC ISO 8601）、verb、id、done／pending（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、唯讀動詞印 6-33"/>
<c id="p2b_sm" parent="p2B" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,707,750,124" v="&lt;b&gt;upgrade 逐檔狀態機（B = baseline、D = 磁碟、N = 新版讀自 /dist/&amp;lt;repo&amp;gt;；只對 state=managed、無待解衝突）&lt;/b&gt;&lt;br&gt;D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 git merge-file --diff3（標籤 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 等），衝突 → 2；不論結果 baseline 推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → 問後換、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 conflicts、baseline 不推。拒絕：已納管檔 state 不變、只記 declined_hash；新增檔（從未建立）→ state=declined + declined_hash。五態轉移圖見狀態機頁"/>
<c id="p2b_sm_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,709,30,20" v="v2"/>
<c id="p2b_sh_l" parent="p2B" st="text;fs=13;s=none;f=none;b=1" g="790,845,750,28" v="4.5 薄殼（進 git，vendor_kit 擁有，人不改）與使用者的兩個根檔"/>
<c id="p2b_sh_h0" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="790,877,170,30" v="檔"/>
<c id="p2b_sh_h1" parent="p2B" st="f=#e6e6e6;s=#999999;b=1" g="960,877,580,30" v="內容"/>
<c id="p2b_sh_r0c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,907,170,73" v="自描述首行"/>
<c id="p2b_sh_r0c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,909,30,20" v="v2"/>
<c id="p2b_sh_r0c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,907,580,73" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;hash&amp;gt;；hash = 首行（含其換行）之後全部位元組 CRLF→LF 正規化後的 sha256；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 印 6-28 列差異不動；mode 變更只 warn"/>
<c id="p2b_sh_r1c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,980,170,26" v="entry.just"/>
<c id="p2b_sh_r1c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,980,580,26" v="mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;；零 set 零 recipe"/>
<c id="p2b_sh_r2c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,1006,170,42" v="vendor.just"/>
<c id="p2b_sh_r2c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,1006,580,42" v="動詞 recipe 一行轉發 + 啟動器本體（POSIX sh recipe）；set positional-arguments 只放這"/>
<c id="p2b_sh_r3c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,1048,170,26" v=".gitignore"/>
<c id="p2b_sh_r3c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,1048,580,26" v="cache/、gen/、version.local.toml、.tmp.*"/>
<c id="p2b_sh_r4c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,1074,170,26" v="ci/check.sh"/>
<c id="p2b_sh_r4c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,1074,580,26" v="契約⑤ p3c：shebang、自描述、export CI=1、⓪–⑤ 六步"/>
<c id="p2b_sh_r5c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,1100,170,42" v="根 justfile（使用者的）"/>
<c id="p2b_sh_r5c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,1102,30,20" v="v2"/>
<c id="p2b_sh_r5c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,1100,580,42" v="install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;；無檔則建，內容逐字四行：import 一行／空行／default:／\t@just --list；uninstall 只刪完全相同行"/>
<c id="p2b_sh_r6c0" parent="p2B" st="f=#ffffff;s=#999999;b=1" g="790,1142,170,42" v="根 .dockerignore（使用者的）"/>
<c id="p2b_sh_r6c0_v2" parent="p2B" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="928,1144,30,20" v="v2"/>
<c id="p2b_sh_r6c1" parent="p2B" st="f=#ffffff;s=#999999" g="960,1142,580,42" v="install append 三行 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34）；uninstall 問後只刪原文相同行"/>
<c id="p2b_lg0" st="f=#ffe6cc;s=#d79b00;fs=14" g="40,1498,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p2b_lg1" st="f=#e6e6e6;s=#999999;b=1" g="250,1498,110,40" v="灰底：表頭"/>
<c id="p2b_lg2" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="380,1498,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p2b_lg3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="600,1498,200,40" v="右上角綠標籤：v2 改"/>
<c id="p2b_lg3_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="768,1500,30,20" v="v2"/>
<c id="p2b_lg4" st="shape=note;f=#ffffff;s=#999999" g="820,1498,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p2b_lgt" st="text;s=none;f=none" g="1060,1488,300,60" v="一列一個欄位；「型別／必填」照 interface_spec §4&lt;br&gt;範例（等寬字）見 p2"/>
<c id="p2b_th" st="text;fs=13;s=none;f=none;b=1" g="40,1554,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p2b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1588,150,55" v="schema／written_by"/>
<c id="p2b_tv0" st="f=#ffffff;s=#999999" g="190,1588,610,55" v="每個 vendor_kit 寫的 TOML 都有 schema = N（integer，讀取門檻只看它）+ written_by = &quot;&amp;lt;vX&amp;gt;&quot;（純資訊）；同 schema 只加不改；讀時忽略未知欄位、寫時保留；只拒絕型別錯／重複宣告 → 1；schema 高於本引擎 → 3 印 6-19 零寫入"/>
<c id="p2b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1643,150,55" v="vendor_kit = 正規行"/>
<c id="p2b_tv1" st="f=#ffffff;s=#999999" g="190,1643,610,55" v="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&amp;lt;ref&amp;gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路"/>
<c id="p2b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1698,150,55" v="version.local.toml"/>
<c id="p2b_tv2" st="f=#ffffff;s=#999999" g="190,1698,610,55" v="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1"/>
<c id="p2b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1753,150,55" v="image ID"/>
<c id="p2b_tv3" st="f=#ffffff;s=#999999" g="190,1753,610,55" v="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對"/>
<c id="p2b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1808,150,55" v="metadata"/>
<c id="p2b_tv4" st="f=#ffffff;s=#999999" g="190,1808,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌"/>
<c id="p2b_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1863,150,55" v="初始檔五態（state）"/>
<c id="p2b_tv5" st="f=#ffffff;s=#999999" g="190,1863,610,55" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈"/>
<c id="p2b_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1918,150,55" v="declined／declined_hash"/>
<c id="p2b_tv6" st="f=#ffffff;s=#999999" g="190,1918,610,55" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined"/>
<c id="p2b_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1973,150,55" v="conflicts（衝突中檔案）"/>
<c id="p2b_tv7" st="f=#ffffff;s=#999999" g="190,1973,610,55" v="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）"/>
<c id="p2b_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2028,150,71" v="進度日誌"/>
<c id="p2b_tv8" st="f=#ffffff;s=#999999" g="190,2028,610,71" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續；sync／update 偵測未完成交易 → 印 6-33 結束 1；help 印 6-33 但仍 0"/>
<c id="p2b_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1588,150,40" v="三方合併"/>
<c id="p2b_tv9" st="f=#ffffff;s=#999999" g="990,1588,610,40" v="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）"/>
<c id="p2b_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1628,150,40" v="印記 gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p2b_tv10" st="f=#ffffff;s=#999999" g="990,1628,610,40" v="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&amp;lt;dir&amp;gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref"/>
<c id="p2b_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1668,150,55" v="gen/.stamp"/>
<c id="p2b_tv11" st="f=#ffffff;s=#999999" g="990,1668,610,55" v="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &amp;lt;tag&amp;gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行"/>
<c id="p2b_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1723,150,55" v="薄殼自描述首行"/>
<c id="p2b_tv12" st="f=#ffffff;s=#999999" g="990,1723,610,55" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 CRLF→LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動"/>
<c id="p2b_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1778,150,55" v="mod／mod?／import／import?"/>
<c id="p2b_tv13" st="f=#ffffff;s=#999999" g="990,1778,610,55" v="just 的載入：mod &amp;lt;ns&amp;gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）"/>
<c id="p2b_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1833,150,55" v="進度日誌檔 .tmp.*"/>
<c id="p2b_tv14" st="f=#ffffff;s=#999999" g="990,1833,610,55" v="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪"/>
<c id="p2b_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1888,150,40" v="暫存 .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p2b_tv15" st="f=#ffffff;s=#999999" g="990,1888,610,40" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋"/>
<c id="p2b_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1928,150,40" v="多架構 index／index digest"/>
<c id="p2b_tv16" st="f=#ffffff;s=#999999" g="990,1928,610,40" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）"/>
<c id="p2b_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1968,150,55" v=".digest 旁檔"/>
<c id="p2b_tv17" st="f=#ffffff;s=#999999" g="990,1968,610,55" v="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1"/>
</page>
<page name="契約 v2：動詞 × 檔案矩陣">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約② 專案裡的檔（3／3）── 動詞 × 檔案矩陣、會碰／不碰使用者東西、version.toml 怎麼被讀"/>
<c id="p2c_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p2c_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;寫 = 產生／覆蓋；刪 = 移除；— = 不碰；依 interface_spec §1.2 副作用欄與 §4 寫入者"/>
<c id="p2C" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,1516" v="5. 動詞 × 檔案（一列一動詞、一欄一檔；細節見 p1b 與流程頁）"/>
<c id="p2c_tc_l" parent="p2C" st="text;fs=13;s=none;f=none;b=1" g="20,50,1300,28" v="「會碰使用者東西」只有三處（不變量：可以建、要改先問、永不刪、永不覆蓋；拒絕 → 不寫：新檔 state=declined、已納管檔只記 declined_hash）"/>
<c id="p2c_tc_h0" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="20,82,200,30" v="東西"/>
<c id="p2c_tc_h1" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="220,82,1320,30" v="怎麼碰"/>
<c id="p2c_tc_r0c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,112,200,42" v="根 justfile 一行"/>
<c id="p2c_tc_r0c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="188,114,30,20" v="v2"/>
<c id="p2c_tc_r0c1" parent="p2C" st="f=#ffffff;s=#999999" g="220,112,1320,42" v="install：無 → 建四行（import + 空行 + default: + \t@just --list）；有 → 問 6-20（-y 直接加並印出）；已含 → 不再加；根檔是 symlink → 不寫、印遷移指示｜uninstall：問 6-20，只刪與我們寫的完全相同的行｜add：只讀它做撞名檢查（just --dump --dump-format json）"/>
<c id="p2c_tc_r1c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,154,200,26" v="根 .dockerignore 三行"/>
<c id="p2c_tc_r1c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="188,156,30,20" v="v2"/>
<c id="p2c_tc_r1c1" parent="p2C" st="f=#ffffff;s=#999999" g="220,154,1320,26" v="install：無 → 建；有 → 問 6-34 後 append（-y 免問），插入的行記於 baseline/.vendor_kit.toml｜uninstall：問後只刪原文相同的行｜工具 build 以專案根當 context 時靠它排除 cache"/>
<c id="p2c_tc_r2c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,180,200,42" v="初始檔（init.toml 的 dest）"/>
<c id="p2c_tc_r2c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="188,182,30,20" v="v2"/>
<c id="p2c_tc_r2c1" parent="p2C" st="f=#ffffff;s=#999999" g="220,180,1320,42" v="add：無 → 建；有 → 不納管、不覆蓋（unmanaged，印 6-11）；strategy=append 問 6-21 後加行｜upgrade：逐檔狀態機後問 6-22（換／三方合併／建新檔／二進位）；拒絕 → declined_hash（新檔 state=declined）；N 變了才再問｜remove／uninstall：永不刪，印清單；append 行問後只刪原文相同的"/>
<c id="p2c_not" parent="p2C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,236,1520,46" v="&lt;b&gt;不碰&lt;/b&gt;：使用者的 .gitignore（除非工具以 strategy=append 宣告且你同意）、.git/info/exclude（dev 也不寫）、.git 本身（引擎不讀 .git、不碰 index、不做 git init）；我們要忽略的路徑全放 .vendor_kit/.gitignore；-y 不授權覆蓋既有未納管檔、不硬加 append 行"/>
<c id="p2c_not_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,238,30,20" v="v2"/>
<c id="p2c_mx_l" parent="p2C" st="text;fs=13;s=none;f=none;b=1" g="20,296,1200,28" v="表 A：進 git 的宣告、使用者的兩個根檔、薄殼、gen/.stamp（動詞 × 檔案）"/>
<c id="p2c_mx_h0" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="20,328,130,30" v="動詞"/>
<c id="p2c_mx_h1" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="150,328,210,30" v="version.toml"/>
<c id="p2c_mx_h2" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="360,328,240,30" v="version.local.toml"/>
<c id="p2c_mx_h3" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="600,328,210,30" v="根 justfile"/>
<c id="p2c_mx_h4" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="810,328,200,30" v="根 .dockerignore"/>
<c id="p2c_mx_h5" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="1010,328,300,30" v="薄殼（tracked 四檔）"/>
<c id="p2c_mx_h6" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="1310,328,230,30" v="gen/.stamp"/>
<c id="p2c_mx_r0c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,358,130,42" v="install"/>
<c id="p2c_mx_r0c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,360,30,20" v="v2"/>
<c id="p2c_mx_r0c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,358,210,42" v="寫（schema、written_by、正規行）"/>
<c id="p2c_mx_r0c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,358,240,42" v="—（bootstrap --local 成功後才寫 tag + image ID）"/>
<c id="p2c_mx_r0c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,358,210,42" v="無 → 建四行；有 → 問加一行；已含 → 不再加"/>
<c id="p2c_mx_r0c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,358,200,42" v="無 → 建三行；有 → 問後 append"/>
<c id="p2c_mx_r0c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,358,300,42" v="首行 hash 相符才重產；不符 → 1 印 6-28"/>
<c id="p2c_mx_r0c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,358,230,42" v="寫（引擎 ref）"/>
<c id="p2c_mx_r1c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,400,130,26" v="uninstall"/>
<c id="p2c_mx_r1c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,402,30,20" v="v2"/>
<c id="p2c_mx_r1c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,400,210,26" v="hash 相符才刪"/>
<c id="p2c_mx_r1c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,400,240,26" v="hash 相符才刪；否則保留並回報"/>
<c id="p2c_mx_r1c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,400,210,26" v="問後只刪相同的行（之後才刪日誌）"/>
<c id="p2c_mx_r1c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,400,200,26" v="問後只刪原文相同三行"/>
<c id="p2c_mx_r1c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,400,300,26" v="只刪 hash 相符的自產檔；未知或被改的保留並回報"/>
<c id="p2c_mx_r1c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,400,230,26" v="刪（自產）"/>
<c id="p2c_mx_r2c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,426,130,26" v="add"/>
<c id="p2c_mx_r2c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,426,210,26" v="最後加 [tools] 一行"/>
<c id="p2c_mx_r2c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,426,240,26" v="—"/>
<c id="p2c_mx_r2c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,426,210,26" v="—（只讀：撞名檢查）"/>
<c id="p2c_mx_r2c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,426,200,26" v="—"/>
<c id="p2c_mx_r2c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,426,300,26" v="—"/>
<c id="p2c_mx_r2c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,426,230,26" v="—"/>
<c id="p2c_mx_r3c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,452,130,26" v="remove"/>
<c id="p2c_mx_r3c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,452,210,26" v="刪一行"/>
<c id="p2c_mx_r3c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,452,240,26" v="—"/>
<c id="p2c_mx_r3c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,452,210,26" v="—"/>
<c id="p2c_mx_r3c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,452,200,26" v="—"/>
<c id="p2c_mx_r3c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,452,300,26" v="—"/>
<c id="p2c_mx_r3c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,452,230,26" v="—"/>
<c id="p2c_mx_r4c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,478,130,26" v="upgrade（工具）"/>
<c id="p2c_mx_r4c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,478,210,26" v="最後改一行"/>
<c id="p2c_mx_r4c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,478,240,26" v="—"/>
<c id="p2c_mx_r4c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,478,210,26" v="—"/>
<c id="p2c_mx_r4c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,478,200,26" v="—"/>
<c id="p2c_mx_r4c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,478,300,26" v="—"/>
<c id="p2c_mx_r4c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,478,230,26" v="—"/>
<c id="p2c_mx_r5c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,504,130,57" v="upgrade（不帶 repo）遇引擎新版"/>
<c id="p2c_mx_r5c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,506,30,20" v="v2"/>
<c id="p2c_mx_r5c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,504,210,57" v="只改正規行（舊引擎）"/>
<c id="p2c_mx_r5c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,504,240,57" v="—（覆寫時啟動器 docker image inspect 驗 ID）"/>
<c id="p2c_mx_r5c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,504,210,57" v="—"/>
<c id="p2c_mx_r5c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,504,200,57" v="—"/>
<c id="p2c_mx_r5c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,504,300,57" v="接手：新引擎跑 upgrade vendor_kit"/>
<c id="p2c_mx_r5c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,504,230,57" v="同下列"/>
<c id="p2c_mx_r6c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,561,130,42" v="upgrade vendor_kit"/>
<c id="p2c_mx_r6c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,563,30,20" v="v2"/>
<c id="p2c_mx_r6c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,561,210,42" v="有新版才改正規行"/>
<c id="p2c_mx_r6c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,561,240,42" v="—（覆寫優先，inspect 驗 ID、不 pull）"/>
<c id="p2c_mx_r6c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,561,210,42" v="—"/>
<c id="p2c_mx_r6c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,561,200,42" v="—"/>
<c id="p2c_mx_r6c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,561,300,42" v="首行 hash 相符才重產四檔；降版讀不了 → 3 不動"/>
<c id="p2c_mx_r6c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,561,230,42" v="寫（引擎 ref）"/>
<c id="p2c_mx_r7c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,603,130,42" v="dev"/>
<c id="p2c_mx_r7c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,605,30,20" v="v2"/>
<c id="p2c_mx_r7c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,603,210,42" v="—"/>
<c id="p2c_mx_r7c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,603,240,42" v="加行（工具 path:／引擎 tag + vendor_kit_image_id）"/>
<c id="p2c_mx_r7c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,603,210,42" v="—"/>
<c id="p2c_mx_r7c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,603,200,42" v="—"/>
<c id="p2c_mx_r7c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,603,300,42" v="—（-i 舊 image 禁止重產）"/>
<c id="p2c_mx_r7c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,603,230,42" v="—"/>
<c id="p2c_mx_r8c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,645,130,42" v="undev"/>
<c id="p2c_mx_r8c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,647,30,20" v="v2"/>
<c id="p2c_mx_r8c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,645,210,42" v="—"/>
<c id="p2c_mx_r8c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,645,240,42" v="刪行（含 image ID；建日誌後；最後一個覆寫撤掉刪整檔）"/>
<c id="p2c_mx_r8c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,645,210,42" v="—"/>
<c id="p2c_mx_r8c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,645,200,42" v="—"/>
<c id="p2c_mx_r8c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,645,300,42" v="—"/>
<c id="p2c_mx_r8c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,645,230,42" v="—（undev vendor_kit 後不符只印 6-1）"/>
<c id="p2c_mx_r9c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,687,130,26" v="sync"/>
<c id="p2c_mx_r9c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,687,210,26" v="—（只讀）"/>
<c id="p2c_mx_r9c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,687,240,26" v="—（只讀；CI 為真下有覆寫 → 1）"/>
<c id="p2c_mx_r9c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,687,210,26" v="—"/>
<c id="p2c_mx_r9c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,687,200,26" v="—"/>
<c id="p2c_mx_r9c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,687,300,26" v="不寫（不符 → 1 印 6-1）"/>
<c id="p2c_mx_r9c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,687,230,26" v="不寫（只比對）"/>
<c id="p2c_mx_r10c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,713,130,26" v="update"/>
<c id="p2c_mx_r10c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,713,210,26" v="—"/>
<c id="p2c_mx_r10c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,713,240,26" v="—"/>
<c id="p2c_mx_r10c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,713,210,26" v="—"/>
<c id="p2c_mx_r10c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,713,200,26" v="—"/>
<c id="p2c_mx_r10c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,713,300,26" v="—"/>
<c id="p2c_mx_r10c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,713,230,26" v="—"/>
<c id="p2c_mx_r11c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,739,130,26" v="prune"/>
<c id="p2c_mx_r11c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,741,30,20" v="v2"/>
<c id="p2c_mx_r11c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,739,210,26" v="—（只讀：哪些 image 仍被引用）"/>
<c id="p2c_mx_r11c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,739,240,26" v="—（只讀：keep 含覆寫 tag）"/>
<c id="p2c_mx_r11c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,739,210,26" v="—"/>
<c id="p2c_mx_r11c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,739,200,26" v="—"/>
<c id="p2c_mx_r11c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,739,300,26" v="—"/>
<c id="p2c_mx_r11c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,739,230,26" v="—"/>
<c id="p2c_mx_r12c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,765,130,42" v="任何動詞（結束碼 3）"/>
<c id="p2c_mx_r12c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,767,30,20" v="v2"/>
<c id="p2c_mx_r12c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,765,210,42" v="—"/>
<c id="p2c_mx_r12c2" parent="p2C" st="f=#ffffff;s=#999999" g="360,765,240,42" v="—"/>
<c id="p2c_mx_r12c3" parent="p2C" st="f=#ffffff;s=#999999" g="600,765,210,42" v="—"/>
<c id="p2c_mx_r12c4" parent="p2C" st="f=#ffffff;s=#999999" g="810,765,200,42" v="—"/>
<c id="p2c_mx_r12c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,765,300,42" v="零寫入（無任何例外；救援路徑回 3 也零寫入）"/>
<c id="p2c_mx_r12c6" parent="p2C" st="f=#ffffff;s=#999999" g="1310,765,230,42" v="—"/>
<c id="p2c_my_l" parent="p2C" st="text;fs=13;s=none;f=none;b=1" g="20,821,1200,28" v="表 B：baseline／gen 兩檔／cache／初始檔／.tmp.*"/>
<c id="p2c_my_h0" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="20,853,130,30" v="動詞"/>
<c id="p2c_my_h1" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="150,853,250,30" v="baseline/ + metadata"/>
<c id="p2c_my_h2" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="400,853,190,30" v="gen/tools.just"/>
<c id="p2c_my_h3" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="590,853,190,30" v="gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="p2c_my_h4" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="780,853,230,30" v="cache/&amp;lt;repo&amp;gt;/"/>
<c id="p2c_my_h5" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="1010,853,320,30" v="初始檔"/>
<c id="p2c_my_h6" parent="p2C" st="f=#e6e6e6;s=#999999;b=1" g="1330,853,210,30" v=".tmp.*"/>
<c id="p2c_my_r0c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,883,130,73" v="install"/>
<c id="p2c_my_r0c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,885,30,20" v="v2"/>
<c id="p2c_my_r0c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,883,250,73" v="建 baseline/.gitkeep（不建 metadata）；.dockerignore 記錄寫 baseline/.vendor_kit.toml"/>
<c id="p2c_my_r0c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,883,190,73" v="—"/>
<c id="p2c_my_r0c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,883,190,73" v="—"/>
<c id="p2c_my_r0c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,883,230,73" v="—"/>
<c id="p2c_my_r0c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,883,320,73" v="—"/>
<c id="p2c_my_r0c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,883,210,73" v="修復型 install：.tmp.install.&amp;lt;id&amp;gt;.toml（第一次 install 不建日誌，失敗整包丟棄）"/>
<c id="p2c_my_r1c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,956,130,42" v="uninstall"/>
<c id="p2c_my_r1c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,956,250,42" v="先預檢（hash 相符清單）→ 逐工具 remove；未知或被改的保留"/>
<c id="p2c_my_r1c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,956,190,42" v="刪（自產）"/>
<c id="p2c_my_r1c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,956,190,42" v="刪（自產）"/>
<c id="p2c_my_r1c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,956,230,42" v="刪（未知檔保留並回報）"/>
<c id="p2c_my_r1c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,956,320,42" v="永不刪；append 行問後刪"/>
<c id="p2c_my_r1c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,956,210,42" v=".tmp.uninstall.&amp;lt;id&amp;gt;.toml（最後刪）"/>
<c id="p2c_my_r1c6_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,958,30,20" v="v2"/>
<c id="p2c_my_r2c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,998,130,42" v="add"/>
<c id="p2c_my_r2c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,998,250,42" v="建 &amp;lt;repo&amp;gt;/ + metadata（complete、五態、lines、source）"/>
<c id="p2c_my_r2c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,998,190,42" v="重生"/>
<c id="p2c_my_r2c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,998,190,42" v="materialize 寫"/>
<c id="p2c_my_r2c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,998,230,42" v="materialize"/>
<c id="p2c_my_r2c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,998,320,42" v="無 → 建；有 → 不納管；append 問後加"/>
<c id="p2c_my_r2c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,998,210,42" v="—（日誌在 metadata [progress]）"/>
<c id="p2c_my_r2c6_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1000,30,20" v="v2"/>
<c id="p2c_my_r3c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1040,130,26" v="remove"/>
<c id="p2c_my_r3c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1040,250,26" v="刪 &amp;lt;repo&amp;gt;/"/>
<c id="p2c_my_r3c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1040,190,26" v="刪該工具所有 mod? 行"/>
<c id="p2c_my_r3c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1040,190,26" v="刪"/>
<c id="p2c_my_r3c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1040,230,26" v="刪"/>
<c id="p2c_my_r3c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1040,320,26" v="永不刪；append 行問後刪（原文相同）"/>
<c id="p2c_my_r3c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1040,210,26" v=".tmp.remove.&amp;lt;id&amp;gt;.toml"/>
<c id="p2c_my_r3c6_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1042,30,20" v="v2"/>
<c id="p2c_my_r4c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1066,130,42" v="upgrade（工具）"/>
<c id="p2c_my_r4c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1066,250,42" v="推到新版（衝突仍推；解析失敗不推）+ metadata"/>
<c id="p2c_my_r4c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1066,190,42" v="重生"/>
<c id="p2c_my_r4c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1066,190,42" v="materialize 寫"/>
<c id="p2c_my_r4c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1066,230,42" v="materialize"/>
<c id="p2c_my_r4c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1066,320,42" v="逐檔問：換／三方合併／append 行替換／建新檔／二進位"/>
<c id="p2c_my_r4c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1066,210,42" v="—（日誌在 metadata [progress]）"/>
<c id="p2c_my_r4c6_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1068,30,20" v="v2"/>
<c id="p2c_my_r5c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1108,130,42" v="upgrade vendor_kit"/>
<c id="p2c_my_r5c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,1110,30,20" v="v2"/>
<c id="p2c_my_r5c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1108,250,42" v="schema 遷移（dry-run 明列）"/>
<c id="p2c_my_r5c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1108,190,42" v="重生"/>
<c id="p2c_my_r5c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1108,190,42" v="—"/>
<c id="p2c_my_r5c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1108,230,42" v="—"/>
<c id="p2c_my_r5c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1108,320,42" v="—"/>
<c id="p2c_my_r5c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1108,210,42" v="—"/>
<c id="p2c_my_r6c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1150,130,26" v="dev"/>
<c id="p2c_my_r6c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,1152,30,20" v="v2"/>
<c id="p2c_my_r6c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1150,250,26" v="—"/>
<c id="p2c_my_r6c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1150,190,26" v="—"/>
<c id="p2c_my_r6c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1150,190,26" v="寫 path:&amp;lt;dir&amp;gt;"/>
<c id="p2c_my_r6c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1150,230,26" v="改成 symlink → &amp;lt;dir&amp;gt;/dist"/>
<c id="p2c_my_r6c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1150,320,26" v="—"/>
<c id="p2c_my_r6c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1150,210,26" v="—"/>
<c id="p2c_my_r7c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1176,130,26" v="undev"/>
<c id="p2c_my_r7c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,1178,30,20" v="v2"/>
<c id="p2c_my_r7c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1176,250,26" v="—"/>
<c id="p2c_my_r7c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1176,190,26" v="—"/>
<c id="p2c_my_r7c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1176,190,26" v="重寫（materialize）"/>
<c id="p2c_my_r7c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1176,230,26" v="重新 materialize（經 docker）"/>
<c id="p2c_my_r7c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1176,320,26" v="—"/>
<c id="p2c_my_r7c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1176,210,26" v=".tmp.undev.&amp;lt;id&amp;gt;.toml"/>
<c id="p2c_my_r8c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1202,130,42" v="sync"/>
<c id="p2c_my_r8c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,1204,30,20" v="v2"/>
<c id="p2c_my_r8c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1202,250,42" v="—（只讀 complete、source 落後）"/>
<c id="p2c_my_r8c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1202,190,42" v="缺或需重生 → 重生"/>
<c id="p2c_my_r8c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1202,190,42" v="materialize 時寫"/>
<c id="p2c_my_r8c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1202,230,42" v="materialize／重裝（只拉鎖定版）"/>
<c id="p2c_my_r8c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1202,320,42" v="—"/>
<c id="p2c_my_r8c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1202,210,42" v="—（有未完成 → 1 印 6-33 不恢復）"/>
<c id="p2c_my_r9c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1244,130,26" v="update"/>
<c id="p2c_my_r9c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1244,250,26" v="—"/>
<c id="p2c_my_r9c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1244,190,26" v="—"/>
<c id="p2c_my_r9c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1244,190,26" v="—"/>
<c id="p2c_my_r9c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1244,230,26" v="—"/>
<c id="p2c_my_r9c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1244,320,26" v="—"/>
<c id="p2c_my_r9c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1244,210,26" v="—"/>
<c id="p2c_my_r10c0" parent="p2C" st="f=#ffffff;s=#999999;b=1" g="20,1270,130,57" v="prune"/>
<c id="p2c_my_r10c0_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="118,1272,30,20" v="v2"/>
<c id="p2c_my_r10c1" parent="p2C" st="f=#ffffff;s=#999999" g="150,1270,250,57" v="—"/>
<c id="p2c_my_r10c2" parent="p2C" st="f=#ffffff;s=#999999" g="400,1270,190,57" v="—"/>
<c id="p2c_my_r10c3" parent="p2C" st="f=#ffffff;s=#999999" g="590,1270,190,57" v="—"/>
<c id="p2c_my_r10c4" parent="p2C" st="f=#ffffff;s=#999999" g="780,1270,230,57" v="—"/>
<c id="p2c_my_r10c5" parent="p2C" st="f=#ffffff;s=#999999" g="1010,1270,320,57" v="—"/>
<c id="p2c_my_r10c6" parent="p2C" st="f=#ffffff;s=#999999" g="1330,1270,210,57" v=".tmp.prune.&amp;lt;id&amp;gt;.toml；刪失效 .tmp.dist.*、已完成殘留；活躍的不刪"/>
<c id="p2c_reno" parent="p2C" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,1341,750,155" v="&lt;b&gt;version.toml 怎麼被讀&lt;/b&gt;&lt;br&gt;・啟動器（sh）：以正規行 regex 於 version.local.toml（覆寫優先）→ version.toml 取 vendor_kit；命中數 ≠ 1 → 1；不解析 TOML（resolve 的 vk-resolve 才是它的輸入）；快路徑用 grep 比 gen/*.stamp&lt;br&gt;・引擎 version 模組：TOML 讀寫（schema 轉換）+ version.local.toml 覆寫；flock；apply 最後才寫 version.toml&lt;br&gt;・Renovate preset：regex manager（**/.vendor_kit/version.toml；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR&lt;br&gt;・deploy：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（工具契約一句；vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄"/>
<c id="p2c_reno_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,1343,30,20" v="v2"/>
<c id="p2c_rule" parent="p2C" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,1341,750,155" v="&lt;b&gt;規則摘要&lt;/b&gt;&lt;br&gt;・version.toml 是唯一來源：sync 拿它對印記，不一致就 materialize（只拉鎖定版）；apply 拿鎖後先重驗 resolve 給的輸入指紋，不同 → 1 印 6-12&lt;br&gt;・自動化（sync）只碰 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp：不碰使用者的檔、不寫薄殼、不寫 gen/.stamp；薄殼 ≠ 引擎 ref → 1 印 6-1（install／upgrade vendor_kit 不被擋）&lt;br&gt;・baseline 是上次合併的歷史狀態，不由 version.toml 推導（待合併時 version 已 B、baseline 仍 A）&lt;br&gt;・進 git 的只有：根 justfile 那行、根 .dockerignore 三行、.vendor_kit/（不含 cache/、gen/、version.local.toml、.tmp.*）、初始檔；人只改：justfile、初始檔、version.toml（手動升版）&lt;br&gt;・舊薄殼（--protocol P 太舊）跑新 major 引擎的一般動詞 → 3 零寫入（6-36）；救援路徑永遠可用"/>
<c id="p2c_rule_v2" parent="p2C" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1343,30,20" v="v2"/>
<c id="p2c_lg0" st="f=#ffe6cc;s=#d79b00;fs=14" g="40,1642,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p2c_lg1" st="f=#e6e6e6;s=#999999;b=1" g="250,1642,110,40" v="灰底：表頭"/>
<c id="p2c_lg2" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="380,1642,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p2c_lg3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="600,1642,200,40" v="右上角綠標籤：v2 改"/>
<c id="p2c_lg3_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="768,1644,30,20" v="v2"/>
<c id="p2c_lg4" st="shape=note;f=#ffffff;s=#999999" g="820,1642,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p2c_lgt" st="text;s=none;f=none" g="1060,1632,300,60" v="表格：一列一動詞、一欄一檔&lt;br&gt;目錄樹與範例 p2、schema p2b"/>
<c id="p2c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1698,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p2c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1732,150,40" v="唯一來源"/>
<c id="p2c_tv0" st="f=#ffffff;s=#999999" g="190,1732,610,40" v="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導"/>
<c id="p2c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1772,150,40" v="tracked 檔"/>
<c id="p2c_tv1" st="f=#ffffff;s=#999999" g="190,1772,610,40" v="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p2c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1812,150,55" v="frozen（CI 為真）"/>
<c id="p2c_tv2" st="f=#ffffff;s=#999999" g="190,1812,610,55" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"/>
<c id="p2c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1867,150,55" v="輸入指紋"/>
<c id="p2c_tv3" st="f=#ffffff;s=#999999" g="190,1867,610,55" v="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12"/>
<c id="p2c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1922,150,71" v="進度日誌"/>
<c id="p2c_tv4" st="f=#ffffff;s=#999999" g="190,1922,610,71" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續；sync／update 偵測未完成交易 → 印 6-33 結束 1；help 印 6-33 但仍 0"/>
<c id="p2c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1993,150,55" v="進度日誌檔 .tmp.*"/>
<c id="p2c_tv5" st="f=#ffffff;s=#999999" g="190,1993,610,55" v="修復型 install／remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在；第一次 install 不建）；&amp;lt;id&amp;gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪"/>
<c id="p2c_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2048,150,55" v="救援路徑"/>
<c id="p2c_tv6" st="f=#ffffff;s=#999999" g="190,2048,610,55" v="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼"/>
<c id="p2c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1732,150,55" v="Renovate preset"/>
<c id="p2c_tv7" st="f=#ffffff;s=#999999" g="990,1732,610,55" v="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25"/>
<c id="p2c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1787,150,40" v="deploy"/>
<c id="p2c_tv8" st="f=#ffffff;s=#999999" g="990,1787,610,40" v="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄"/>
<c id="p2c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1827,150,55" v="根 justfile 四行"/>
<c id="p2c_tv9" st="f=#ffffff;s=#999999" g="990,1827,610,55" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行"/>
<c id="p2c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1882,150,71" v="根 .dockerignore 三行"/>
<c id="p2c_tv10" st="f=#ffffff;s=#999999" g="990,1882,610,71" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache"/>
<c id="p2c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1953,150,40" v="baseline/.gitkeep"/>
<c id="p2c_tv11" st="f=#ffffff;s=#999999" g="990,1953,610,40" v="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 兼作該工具目錄的佔位）"/>
<c id="p2c_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1993,150,55" v="declined／declined_hash"/>
<c id="p2c_tv12" st="f=#ffffff;s=#999999" g="990,1993,610,55" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined"/>
</page>
<page name="契約 v2：工具 repo 契約③">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約③ 工具 repo 要交的（供應側；interface_spec §4.7、§4.8、§3.6；改了要升 major 並公告）"/>
<c id="p3_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p3_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,81" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;dist/files/ 的 symlink 已定禁止；dist 文字檔一律 LF、check.sh --dist 擋 CRLF 已定於 issue #29；Dockerfile.dist 必含 LABEL（16 條必修）"/>
<c id="p3L4" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,109,1560,1120" v="契約③ 工具 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）"/>
<c id="p3_dist" parent="p3L4" st="f=#ffffff;s=#999999" g="20,50,440,108" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;&amp;lt;repo&amp;gt;/                  # 工具 repo&lt;br&gt;├─ dist/&lt;br&gt;│  ├─ files/…            # 全部出貨（原樣展開）&lt;br&gt;│  ├─ init.toml          # 初始檔清單（下表）&lt;br&gt;│  └─ just/&amp;lt;ns&amp;gt;.just     # 一檔一命名空間（含 _sync）&lt;br&gt;└─ Dockerfile.dist       # 逐字三行（下框）&lt;/pre&gt;"/>
<c id="p3_dock_l" parent="p3L4" st="text;fs=13;s=none;f=none;b=1" g="20,170,440,28" v="Dockerfile.dist（逐字三行；純資料 image）"/>
<c id="p3_dock" parent="p3L4" st="f=#ffffff;s=#999999" g="20,202,440,61" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;FROM scratch&lt;br&gt;LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1&lt;br&gt;COPY dist/ /dist/&lt;/pre&gt;"/>
<c id="d4_1" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="480,50,253,155" v="&lt;b&gt;dist/files/&lt;/b&gt;&lt;br&gt;全部出貨；materialize 原樣展開到 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/；symlink／hardlink／特殊檔第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF [#29]"/>
<c id="d4_1_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="701,52,30,20" v="v2"/>
<c id="d4_2" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="749,50,253,155" v="&lt;b&gt;dist/init.toml&lt;/b&gt;&lt;br&gt;schema、description（單行）、[[file]] src／dest／strategy=&quot;copy&quot;|&quot;append&quot;（預設 copy），dest 相對專案根；用 copy 指向根 .gitignore／.dockerignore／.editorconfig → --dist 報錯（要用 append）；欄位表見下"/>
<c id="d4_2_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="970,52,30,20" v="v2"/>
<c id="d4_3" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1018,50,253,155" v="&lt;b&gt;dist/just/&amp;lt;ns&amp;gt;.just&lt;/b&gt;&lt;br&gt;每檔一個頂層命名空間，數量工具自決，&amp;lt;repo&amp;gt;.just 必須存在；每檔含私有 _sync（F1，見下）；撞名 → add 拒絕；recipe 用 cd {{quote(justfile_directory())}} 回專案根（禁止相對 working-directory）"/>
<c id="d4_3_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1239,52,30,20" v="v2"/>
<c id="d4_4" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1287,50,253,155" v="&lt;b&gt;Dockerfile.dist&lt;/b&gt;&lt;br&gt;逐字三行：FROM scratch／LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1／COPY dist/ /dist/；純資料，不承諾可執行、vendor_kit 不檢查 binary（Q21：只搬移）；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加，pull 無法追加）"/>
<c id="d4_4_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,52,30,20" v="v2"/>
<c id="d4_5" parent="p3L4" st="f=#e1d5e7;s=#9673a6;fs=14" g="480,221,253,186" v="&lt;b&gt;工具 image&lt;/b&gt;&lt;br&gt;ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;&lt;br&gt;多架構 amd64 + arm64（同一次 buildx、COPY-only；CI 驗兩平台位元組一致）；version.toml 與印記記 index digest（#26）；公開／私有自決（公開不可逆）；已釋出 image／index 子 digest 永不刪；LABEL …vendor_kit=1"/>
<c id="d4_5_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="701,223,30,20" v="v2"/>
<c id="d4_6" parent="p3L4" st="f=#e1d5e7;s=#9673a6;fs=14" g="749,221,253,186" v="&lt;b&gt;引擎 image&lt;/b&gt;&lt;br&gt;ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN&lt;br&gt;公開；多架構（只驗兩平台 LABEL 一致）；LABEL …vendor_kit=1、.protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、.schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）；每平台 docker save tar + .digest 旁檔；Release 資產永不刪"/>
<c id="d4_6_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="970,223,30,20" v="v2"/>
<c id="d4_7" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1018,221,253,186" v="&lt;b&gt;工具 repo 的 CI&lt;/b&gt;&lt;br&gt;跑 vendor_kit 出貨的 check.sh --dist：dist 佈局、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink、LF、just 1.33.0 解析每個 &amp;lt;ns&amp;gt;.just、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台一致"/>
<c id="d4_7_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1239,223,30,20" v="v2"/>
<c id="d4_8" parent="p3L4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1287,221,253,186" v="&lt;b&gt;deploy（一句話契約）&lt;/b&gt;&lt;br&gt;工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml、GHCR（需要的檔打包時複製進去）；vendor_kit 不檢查；保證方式 = 工具 repo 自己在乾淨機器解包驗收；version.toml 公開格式可供來源紀錄"/>
<c id="d4_8_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,223,30,20" v="v2"/>
<c id="p3_dest" parent="p3L4" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,423,1520,46" v="&lt;b&gt;dest 規則（引擎在任何寫入前驗，不只供應端 lint）&lt;/b&gt;：src 相對 dist/、正規化、不得越出 dist/；dest 相對專案根、正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；兩工具同 dest：copy/copy、copy/append → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查（含新版新增 &amp;lt;ns&amp;gt;／dest 的全域撞名）"/>
<c id="p3_dest_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,425,30,20" v="v2"/>
<c id="p3_init_l" parent="p3L4" st="text;fs=13;s=none;f=none;b=1" g="20,483,700,28" v="dist/init.toml（逐字範例；欄位說明在下表）"/>
<c id="p3_sync_l" parent="p3L4" st="text;fs=13;s=none;f=none;b=1" g="790,483,700,28" v="dist/just/&amp;lt;ns&amp;gt;.just 的 _sync（逐字，行首真 tab）與 label 表"/>
<c id="p3_init" parent="p3L4" st="f=#ffffff;s=#999999" g="20,515,750,186" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1&lt;br&gt;description = &quot;&amp;lt;repo&amp;gt; 的專案範本與 just recipe&quot;&lt;br&gt;&lt;br&gt;[[file]]&lt;br&gt;src = &quot;files/Dockerfile&quot;&lt;br&gt;dest = &quot;Dockerfile&quot;&lt;br&gt;&lt;br&gt;[[file]]&lt;br&gt;src = &quot;files/gitignore.snippet&quot;&lt;br&gt;dest = &quot;.gitignore&quot;&lt;br&gt;strategy = &quot;append&quot;&lt;/pre&gt;"/>
<c id="p3_sync" parent="p3L4" st="f=#ffffff;s=#999999" g="790,515,750,108" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;[private]&lt;br&gt;_sync:&lt;br&gt;&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; just vendor_kit sync&lt;br&gt;&lt;br&gt;build: _sync&lt;br&gt;&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; …&lt;/pre&gt;"/>
<c id="p3_initf_h0" parent="p3L4" st="f=#e6e6e6;s=#999999;b=1" g="20,711,170,30" v="欄位"/>
<c id="p3_initf_h1" parent="p3L4" st="f=#e6e6e6;s=#999999;b=1" g="190,711,110,30" v="型別／必填"/>
<c id="p3_initf_h2" parent="p3L4" st="f=#e6e6e6;s=#999999;b=1" g="300,711,470,30" v="說明"/>
<c id="p3_initf_r0c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="20,741,170,26" v="schema"/>
<c id="p3_initf_r0c1" parent="p3L4" st="f=#ffffff;s=#999999" g="190,741,110,26" v="integer／是"/>
<c id="p3_initf_r0c2" parent="p3L4" st="f=#ffffff;s=#999999" g="300,741,470,26" v="建置期契約（同 image 內讀寫），不進執行期矩陣"/>
<c id="p3_initf_r1c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="20,767,170,42" v="description"/>
<c id="p3_initf_r1c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,769,30,20" v="v2"/>
<c id="p3_initf_r1c1" parent="p3L4" st="f=#ffffff;s=#999999" g="190,767,110,42" v="string／否"/>
<c id="p3_initf_r1c2" parent="p3L4" st="f=#ffffff;s=#999999" g="300,767,470,42" v="頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod? 上方 # &amp;lt;description&amp;gt;；缺則 &amp;lt;repo&amp;gt; &amp;lt;tag&amp;gt;"/>
<c id="p3_initf_r2c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="20,809,170,26" v="[[file]].src"/>
<c id="p3_initf_r2c1" parent="p3L4" st="f=#ffffff;s=#999999" g="190,809,110,26" v="string／是"/>
<c id="p3_initf_r2c2" parent="p3L4" st="f=#ffffff;s=#999999" g="300,809,470,26" v="相對 dist/；正規化、不得越出 dist/"/>
<c id="p3_initf_r3c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="20,835,170,42" v="[[file]].dest"/>
<c id="p3_initf_r3c1" parent="p3L4" st="f=#ffffff;s=#999999" g="190,835,110,42" v="string／是"/>
<c id="p3_initf_r3c2" parent="p3L4" st="f=#ffffff;s=#999999" g="300,835,470,42" v="相對專案根；正規化、不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；跨工具撞 dest 規則見左"/>
<c id="p3_initf_r4c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="20,877,170,42" v="[[file]].strategy"/>
<c id="p3_initf_r4c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="158,879,30,20" v="v2"/>
<c id="p3_initf_r4c1" parent="p3L4" st="f=#ffffff;s=#999999" g="190,877,110,42" v="string／否"/>
<c id="p3_initf_r4c2" parent="p3L4" st="f=#ffffff;s=#999999" g="300,877,470,42" v="&quot;copy&quot;（預設）或 &quot;append&quot;，只有這兩值；根 .gitignore／.dockerignore／.editorconfig 類必須用 append"/>
<c id="p3_lbl_h0" parent="p3L4" st="f=#e6e6e6;s=#999999;b=1" g="790,633,200,30" v="資源"/>
<c id="p3_lbl_h1" parent="p3L4" st="f=#e6e6e6;s=#999999;b=1" g="990,633,540,30" v="label（鍵前綴 io.github.&amp;lt;org&amp;gt;.vendor_kit）"/>
<c id="p3_lbl_r0c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="790,663,200,42" v="啟動器建的容器／network／volume"/>
<c id="p3_lbl_r0c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="958,665,30,20" v="v2"/>
<c id="p3_lbl_r0c1" parent="p3L4" st="f=#ffffff;s=#999999" g="990,663,540,42" v="…=1、….project=&amp;lt;專案根絕對路徑&amp;gt;（專案路徑 label 不加在 image 上）"/>
<c id="p3_lbl_r1c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="790,705,200,26" v="引擎 image（build 時）"/>
<c id="p3_lbl_r1c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="958,707,30,20" v="v2"/>
<c id="p3_lbl_r1c1" parent="p3L4" st="f=#ffffff;s=#999999" g="990,705,540,26" v="…=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;"/>
<c id="p3_lbl_r2c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="790,731,200,26" v="工具 image（build 時）"/>
<c id="p3_lbl_r2c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="958,733,30,20" v="v2"/>
<c id="p3_lbl_r2c1" parent="p3L4" st="f=#ffffff;s=#999999" g="990,731,540,26" v="…=1（Dockerfile.dist 必含）"/>
<c id="p3_lbl_r3c0" parent="p3L4" st="f=#ffffff;s=#999999;b=1" g="790,757,200,42" v="prune"/>
<c id="p3_lbl_r3c0_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="958,759,30,20" v="v2"/>
<c id="p3_lbl_r3c1" parent="p3L4" st="f=#ffffff;s=#999999" g="990,757,540,42" v="依 label 掃四類資源；image 只刪帶 label 且本專案未引用者；vendor_kit 不建 network／volume（驗收差集為空，故意留的也要能刪）"/>
<c id="p3_syncr" parent="p3L4" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,933,1520,61" v="&lt;b&gt;sync 自動前置（F1 定案）&lt;/b&gt;：每個 dist/just/&amp;lt;ns&amp;gt;.just 必含上列私有 _sync（本體逐字、行首真 tab；justfile_directory() 在模組內 = 專案根；用 quote() 不直接插字串）；工具每個公開 recipe 相依它（例 build: _sync；例外集合：無）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump --dump-format json 檢查：_sync 存在、私有、本體逐字相符、每個公開 recipe 的 dependencies 含 _sync。限制（契約明寫）：just 在執行前已載入所有模組，同一次呼叫內看不到 sync 重建後的新 recipe；cache 缺檔時 mod? 讓 just vendor_kit sync 仍可進入；1.33.0 fixture 通過才算結案"/>
<c id="p3_syncr_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,935,30,20" v="v2"/>
<c id="p3_con" parent="p3L4" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,1008,750,92" v="&lt;b&gt;工具契約（初始檔與 recipe）&lt;/b&gt;：初始檔只能引用穩定入口 just &amp;lt;ns&amp;gt; …、.vendor_kit/ci/check.sh、.vendor_kit/entry.just、.vendor_kit/version.toml；不得寫死 cache 內部路徑（Q14）；rename／格式變更不得以 copy/append 假裝完成；工具的 build 若以專案根當 context，依賴 install 加進根 .dockerignore 的排除，不得再以其他方式繞過 .vendor_kit/；dist 可執行性是工具 repo 責任（check.sh --dist + 自己的測試）"/>
<c id="p3_con_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,1010,30,20" v="v2"/>
<c id="p3_off" parent="p3L4" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,1008,750,92" v="&lt;b&gt;離線包（Release 資產；Q26）&lt;/b&gt;：每個平台 tar（docker save）旁附同名 .digest 旁檔：&amp;lt;name&amp;gt;.tar + &amp;lt;name&amp;gt;.tar.digest，內容一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；bootstrap.sh --local &amp;lt;tar&amp;gt;／add --local &amp;lt;tar&amp;gt;：docker load 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 local_image_id；旁檔缺 → 1。離線可用：啟動器先 docker image inspect，本機有就不 pull；斷網 + 已有 image → sync／build 必須成功；斷網 + 無 image → 1 印 6-31 不 hang；離線 upgrade 不支援"/>
<c id="p3_off_v2" parent="p3L4" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1010,30,20" v="v2"/>
<c id="p3_lg0" st="f=#e1d5e7;s=#9673a6;fs=14" g="40,1259,170,40" v="紫：image（引擎與工具）"/>
<c id="p3_lg1" st="f=#ffffff;s=#999999" g="230,1259,170,40" v="等寬字：檔案內容範例"/>
<c id="p3_lg2" st="f=#ffe6cc;s=#d79b00;fs=14" g="420,1259,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p3_lg3" st="f=#e6e6e6;s=#999999;b=1" g="630,1259,110,40" v="灰底：表頭"/>
<c id="p3_lg4" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="760,1259,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p3_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="980,1259,200,40" v="右上角綠標籤：v2 改"/>
<c id="p3_lg5_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1148,1261,30,20" v="v2"/>
<c id="p3_lgt" st="text;s=none;f=none" g="1200,1249,300,60" v="紫 = image（工具／引擎）&lt;br&gt;淺灰底容器 = 契約③ 全部"/>
<c id="p3_lg6" st="shape=note;f=#ffffff;s=#999999" g="40,1325,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p3_th" st="text;fs=13;s=none;f=none;b=1" g="40,1381,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p3_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1415,150,40" v="dist/"/>
<c id="p3_tv0" st="f=#ffffff;s=#999999" g="190,1415,610,40" v="工具 repo 出貨的目錄：files/（展開到 cache/&amp;lt;repo&amp;gt;/ 的全部）、init.toml（初始檔清單）、just/&amp;lt;ns&amp;gt;.just（工具自己的 recipe，每檔含 _sync）"/>
<c id="p3_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1455,150,55" v="Dockerfile.dist"/>
<c id="p3_tv1" st="f=#ffffff;s=#999999" g="190,1455,610,55" v="逐字三行：FROM scratch／LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）"/>
<c id="p3_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1510,150,55" v="label"/>
<c id="p3_tv2" st="f=#ffffff;s=#999999" g="190,1510,610,55" v="docker 資源上的鍵值標籤，鍵前綴 io.github.&amp;lt;org&amp;gt;.vendor_kit：容器／network／volume = 1 + .project=&amp;lt;專案根絕對路徑&amp;gt;；引擎 image = 1 + .protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt; + .schema=&amp;lt;N&amp;gt;；工具 image = 1；prune 依 label 掃"/>
<c id="p3_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1565,150,55" v="dest"/>
<c id="p3_tv3" st="f=#ffffff;s=#999999" g="190,1565,610,55" v="init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗"/>
<c id="p3_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1620,150,55" v="strategy = &quot;append&quot;"/>
<c id="p3_tv4" st="f=#ffffff;s=#999999" g="190,1620,610,55" v="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）"/>
<c id="p3_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1675,150,40" v="CRLF／LF"/>
<c id="p3_tv5" st="f=#ffffff;s=#999999" g="190,1675,610,40" v="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]"/>
<c id="p3_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1715,150,40" v="symlink"/>
<c id="p3_tv6" st="f=#ffffff;s=#999999" g="190,1715,610,40" v="指向另一個路徑的捷徑檔；dev 時 cache/&amp;lt;repo&amp;gt;/ 就是指向 &amp;lt;dir&amp;gt;/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止"/>
<c id="p3_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1755,150,55" v="_sync recipe（F1）"/>
<c id="p3_tv7" st="f=#ffffff;s=#999999" g="190,1755,610,55" v="每個 dist/just/&amp;lt;ns&amp;gt;.just 必含的私有 recipe（逐字：[private] / _sync: / \tcd {{quote(justfile_directory())}} &amp;&amp; just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查"/>
<c id="p3_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1415,150,55" v="just 的兩個目錄函式"/>
<c id="p3_tv8" st="f=#ffffff;s=#999999" g="990,1415,610,55" v="justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」"/>
<c id="p3_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1470,150,28" v="buildx"/>
<c id="p3_tv9" st="f=#ffffff;s=#999999" g="990,1470,610,28" v="docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index"/>
<c id="p3_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1498,150,40" v="多架構 index／index digest"/>
<c id="p3_tv10" st="f=#ffffff;s=#999999" g="990,1498,610,40" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）"/>
<c id="p3_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1538,150,55" v="check.sh --dist"/>
<c id="p3_tv11" st="f=#ffffff;s=#999999" g="990,1538,610,55" v="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致"/>
<c id="p3_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1593,150,55" v=".digest 旁檔"/>
<c id="p3_tv12" st="f=#ffffff;s=#999999" g="990,1593,610,55" v="離線包 &amp;lt;name&amp;gt;.tar 旁的 &amp;lt;name&amp;gt;.tar.digest：一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1"/>
<c id="p3_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1648,150,40" v="離線可用（Q26）"/>
<c id="p3_tv13" st="f=#ffffff;s=#999999" g="990,1648,610,40" v="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援"/>
<c id="p3_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1688,150,40" v="deploy"/>
<c id="p3_tv14" st="f=#ffffff;s=#999999" g="990,1688,610,40" v="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄"/>
<c id="p3_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1728,150,40" v="命名空間"/>
<c id="p3_tv15" st="f=#ffffff;s=#999999" g="990,1728,610,40" v="just &amp;lt;ns&amp;gt; &amp;lt;recipe&amp;gt; 前面那個 &amp;lt;ns&amp;gt;；每個工具的 just/&amp;lt;ns&amp;gt;.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）"/>
<c id="p3_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1768,150,40" v="SemVer／正式版"/>
<c id="p3_tv16" st="f=#ffffff;s=#999999" g="990,1768,610,40" v="版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高 floor 或需手動步驟"/>
</page>
<page name="契約 v2：啟動器 ↔ 引擎契約④">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）"/>
<c id="p3b_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p3b_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;vk-resolve/1 文法（Q24）；主機命令白名單（16 條必修）；規則框逐條對應 interface_spec §3、§5，皆已定"/>
<c id="p3L2" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,96,1560,1725.5" v="契約④ 啟動器 ↔ 引擎（每格一件事；① 啟動器 grep → ② resolve → ③ 主機 docker → ④ apply；規則框 = §3、§5 逐條）"/>
<c id="s1" parent="p3L2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="30,60.5,190,108" v="① 以正規行 regex grep 引擎 ref&lt;br&gt;（version.local.toml 覆寫優先；命中 ≠ 1 → 1）&lt;br&gt;下一格 install／upgrade vendor_kit 跳過"/>
<c id="d1" parent="p3L2" st="rhombus;f=#FFF4C3;s=#000000;fs=14" g="244,56.5,180,116" v="gen/.stamp&lt;br&gt;= 引擎 ref？"/>
<c id="d1_e" edge source="s1" target="d1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="g2" parent="p3L2" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14;b=1" g="448,50.0,650,103" v="② docker run 引擎 resolve &amp;lt;動詞&amp;gt;（只讀、不寫檔、無 TTY；診斷走 stderr）"/>
<c id="s2a" parent="g2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="8,34.0,160,61" v="讀 version.toml／local&lt;br&gt;（CI 為真 → frozen）"/>
<c id="s2b" parent="g2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="184,34.0,180,61" v="查 registry 最新 tag／digest&lt;br&gt;（frozen／@&amp;lt;tag&amp;gt; 不查）"/>
<c id="s2c" parent="g2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="380,34.0,250,61" v="stdout vk-resolve/1&lt;br&gt;（pull／extract／mount／engine／fingerprint／apply／end）"/>
<c id="s2a_e" edge source="d1" target="s2a" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="s2b_e" edge source="s2a" target="s2b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="s2c_e" edge source="s2b" target="s2c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p3_err" parent="p3L2" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="204.0,212.5,260,84" v="否 → 1 印 6-1&lt;br&gt;（請 upgrade vendor_kit；不重寫薄殼）"/>
<c id="p3_err_e" edge source="d1" target="p3_err" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="d2" parent="p3L2" st="rhombus;f=#FFF4C3;s=#000000;fs=14" g="488.0,250.0,180,85" v="apply|yes？"/>
<c id="g3" parent="p3L2" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14;b=1" g="692.0,212.5,622,134" v="③ 主機 docker（每筆 pull／extract；不帶 --platform；先收完 vk-resolve 驗文法才動）"/>
<c id="s3a" parent="g3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="8,41.5,110,77" v="docker image inspect&lt;br&gt;（有 → 不 pull）"/>
<c id="s3b" parent="g3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="134,49.5,100,61" v="docker pull&lt;br&gt;（逾時 → 1 印 6-31）"/>
<c id="s3c" parent="g3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="250,41.5,100,77" v="docker create&lt;br&gt;（帶 label）&amp;lt;ref&amp;gt; /x"/>
<c id="s3d" parent="g3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="366,34.0,130,92" v="docker cp c:/dist/.&lt;br&gt;→ .tmp.dist.&amp;lt;id&amp;gt;/&lt;br&gt;&amp;lt;repo&amp;gt;/"/>
<c id="s3e" parent="g3" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="512,49.5,90,61" v="docker rm&lt;br&gt;（trap 也清）"/>
<c id="s4" parent="p3L2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1338.0,246.5,180,92" v="④ docker run 引擎&lt;br&gt;apply &amp;lt;動詞&amp;gt;（掛 /dist:ro）&lt;br&gt;→ 結束碼 0／1／2／3 回 just"/>
<c id="s3b_e" edge source="s3a" target="s3b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="s3c_e" edge source="s3b" target="s3c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="s3d_e" edge source="s3c" target="s3d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="s3e_e" edge source="s3d" target="s3e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="s4_e" edge source="s3e" target="s4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="d2_e" edge source="d2" target="s3a" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="d2_in" edge source="s2c" target="d2" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="993.0,288.5;618.0,288.5"/>
<c id="p3_ok" parent="p3L2" st="ellipse;f=#d5e8d4;s=#000000;fs=14" g="448.0,370.5,260,62" v="否（apply|no）→ 0 快路徑&lt;br&gt;不起第二個容器"/>
<c id="p3_ok_e" edge source="d2" target="p3_ok" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="p3_sh" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,456.5,750,92" v="&lt;b&gt;主機命令白名單（16 條必修；lint 擋清單外）&lt;/b&gt;：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files。啟動器 = POSIX sh（vendor.just 內的 recipe 殼）：不裝 python、不解析 TOML、不 eval；路徑含空白、$、非 ASCII 一律引號"/>
<c id="p3_sh_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="748,458.5,30,20" v="v2"/>
<c id="p3_uf" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,456.5,750,92" v="&lt;b&gt;使用者旗標（rootless 不加 -u／Podman keep-id）&lt;/b&gt;：docker info --format &#x27;{{.SecurityOptions}}&#x27; 含 name=rootless → rootless，不加 -u；docker --version 含 podman → 加 --userns=keep-id、不加 -u；其餘（rootful docker）加 -u &quot;$(id -u):$(id -g)&quot;"/>
<c id="p3_uf_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,458.5,30,20" v="v2"/>
<c id="p3_run" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,562.5,750,124" v="&lt;b&gt;docker run 參數&lt;/b&gt;：docker run --rm [&amp;lt;使用者旗標&amp;gt;] -v &quot;&amp;lt;專案根&amp;gt;:/repo&quot; -w /repo [-v &quot;&amp;lt;專案根&amp;gt;/.vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;:/dist:ro&quot;] [-v &quot;&amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro&quot;]… [-v &quot;&amp;lt;TOKEN_FILE&amp;gt;:/run/vk-token:ro&quot; -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.&amp;lt;org&amp;gt;.vendor_kit=1 --label io.github.&amp;lt;org&amp;gt;.vendor_kit.project=&amp;lt;專案根絕對路徑&amp;gt; &amp;lt;引擎 ref&amp;gt; --protocol P &amp;lt;子命令&amp;gt; [args]。--protocol P 一律在子命令之前；-w /repo 必給；-it 只在 apply 且互動（有 tty、無 -y、非 frozen），resolve 永不 -t；trap … EXIT INT TERM 清容器與 .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p3_run_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="748,564.5,30,20" v="v2"/>
<c id="p3_envw" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,562.5,750,124" v="&lt;b&gt;環境變數與 -e 白名單（§5）&lt;/b&gt;：轉發 CI（照原值；真值規則：非空且不為 0／false → frozen）、VENDOR_KIT_NO_LOCK（=1 跳過 flock）；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update／upgrade 的 resolve 階段以 -e 傳（不寫 log／檔、不傳給工具、dry-run 不印）；VENDOR_KIT_REGISTRY_TOKEN_FILE 改為 -v &amp;lt;主機檔&amp;gt;:/run/vk-token:ro 並以 -e …_TOKEN_FILE=/run/vk-token 傳容器內路徑（與 _TOKEN 同設 → 1「只能擇一」）；啟動器自讀不轉發：VENDOR_KIT_PULL_TIMEOUT（預設 300，--timeout 優先）；其餘一律不轉發（HTTP_PROXY 等 → v2）；README 列出全部 VENDOR_KIT_* 與 CI，lint 擋未列者；引擎容器內 LC_ALL=C.UTF-8、TZ=UTC、HOME=&amp;lt;容器內暫存&amp;gt;"/>
<c id="p3_envw_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,564.5,30,20" v="v2"/>
<c id="p3_img" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,700.5,750,139" v="&lt;b&gt;引擎 image 取得&lt;/b&gt;：一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull &amp;lt;ref&amp;gt;（逾時）。local 覆寫時：docker image inspect &amp;lt;tag&amp;gt; 的 .Id 必須 == version.local.toml vendor_kit_image_id，否則 1；不 pull（不用 docker run 的 pull 旗標：docker 19.03 沒有）。&lt;b&gt;引擎子命令&lt;/b&gt;：單段 install／update／dev／help／upgrade vendor_kit[@&amp;lt;tag&amp;gt;] = --protocol P &amp;lt;verb&amp;gt; [args]；resolve &amp;lt;verb&amp;gt;（只讀、不詢問、不寫檔、無 TTY）；apply &amp;lt;verb&amp;gt; [--dry-run]；內部 materialize／verify／merge 不對外"/>
<c id="p3_img_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="748,702.5,30,20" v="v2"/>
<c id="p3_two" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,700.5,750,139" v="&lt;b&gt;兩段編排的兩個獨立屬性&lt;/b&gt;：需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve &amp;lt;verb&amp;gt; → 主機 docker → apply &amp;lt;verb&amp;gt;，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）。&lt;b&gt;鎖&lt;/b&gt;：鎖在引擎 version 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗印 6-26；VENDOR_KIT_NO_LOCK=1 跳過；啟動器不鎖）。&lt;b&gt;pull 失敗&lt;/b&gt;：印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列「主機錯誤」）+ 僅 add／bootstrap 提示 6-24 的「離線可用 --local」；&lt;b&gt;逾時&lt;/b&gt;：VENDOR_KIT_PULL_TIMEOUT／--timeout，預設 300 秒，只收正整數（0 或非數字 → 1）；背景 pull + 每秒輪詢 + kill；逾時 → 1 印 6-31"/>
<c id="p3_two_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,702.5,30,20" v="v2"/>
<c id="p3_lock" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,853.5,1510,61" v="&lt;b&gt;apply 通則（所有動詞）&lt;/b&gt;：讀 /dist/vk-resolve（啟動器把 resolve 原始 stdout 存成 .tmp.dist.&amp;lt;id&amp;gt;/vk-resolve 一起掛入）→ 拿 flock → 重算指紋與計畫中的 fingerprint 比對（不同 → 1 印 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 為真需改 tracked → 1 印清單）→ 建進度日誌（第一個寫入前）→ 其後所有寫入（清除衝突狀態、append、baseline、metadata、cache、tools.just；version.toml 最後）→ 最後一步刪日誌（uninstall 在根 justfile 那行之後）；不重新選最新版；詢問後、替換前對目標檔再查一次前像；所有合併在暫存完成 → 逐檔原子替換；失敗明列已完成／未完成"/>
<c id="p3_lock_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,855.5,30,20" v="v2"/>
<c id="p3_vk_l" parent="p3L2" st="text;fs=13;s=none;f=none;b=1" g="30,928.5,700,28" v="vk-resolve/1 stdout 文法（Q24；P=1）"/>
<c id="p3_vkt_l" parent="p3L2" st="text;fs=13;s=none;f=none;b=1" g="790,928.5,700,28" v="kind 一覽（啟動器動作）"/>
<c id="p3_vk" parent="p3L2" st="f=#ffffff;s=#999999" g="30,960.5,750,248" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vk-resolve/&amp;lt;P&amp;gt;&lt;br&gt;&amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]&lt;br&gt;end|&amp;lt;N&amp;gt;&lt;br&gt;&lt;br&gt;vk-resolve/1&lt;br&gt;extract|&amp;lt;repo&amp;gt;|ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:v2.3.0@sha256:bbbb…&lt;br&gt;fingerprint|1c0e…77&lt;br&gt;apply|yes&lt;br&gt;end|3&lt;br&gt;&lt;br&gt;vk-resolve/1&lt;br&gt;mount|&amp;lt;repo&amp;gt;|/home/me/my\0040tools&lt;br&gt;fingerprint|9a2f…c1&lt;br&gt;apply|yes&lt;br&gt;end|3&lt;/pre&gt;"/>
<c id="p3_vk_n" parent="p3L2" st="f=#ffffff;s=#999999;fs=14" g="30,1216.5,750,77" v="上段 = 文法骨架：第一行 vk-resolve/&amp;lt;P&amp;gt;（P = 呼叫方 --protocol 的值）；每行一筆 &amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]（欄位以單一 | 分隔；UTF-8；LF；無空行、無註解；禁 CR／NUL／BOM）；最後一行 end|&amp;lt;N&amp;gt;（N = 記錄行數，之後立即 EOF）&lt;br&gt;中段範例 = sync，&amp;lt;repo&amp;gt; 的 cache 過期（extract）；下段範例 = sync，&amp;lt;repo&amp;gt; 在 dev 覆寫中（mount；路徑含空白 → \0040）。範例工具名一律 &amp;lt;repo&amp;gt;"/>
<c id="p3_vkt_h0" parent="p3L2" st="f=#e6e6e6;s=#999999;b=1" g="790,960.5,100,30" v="kind"/>
<c id="p3_vkt_h1" parent="p3L2" st="f=#e6e6e6;s=#999999;b=1" g="890,960.5,180,30" v="欄位"/>
<c id="p3_vkt_h2" parent="p3L2" st="f=#e6e6e6;s=#999999;b=1" g="1070,960.5,50,30" v="筆數"/>
<c id="p3_vkt_h3" parent="p3L2" st="f=#e6e6e6;s=#999999;b=1" g="1120,960.5,420,30" v="啟動器動作"/>
<c id="p3_vkt_r0c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,990.5,100,42" v="pull"/>
<c id="p3_vkt_r0c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,990.5,180,42" v="&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;"/>
<c id="p3_vkt_r0c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,990.5,50,42" v="0..n"/>
<c id="p3_vkt_r0c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,990.5,420,42" v="docker image inspect 有則略，否則 docker pull &amp;lt;ref&amp;gt;（逾時／失敗 → 6-24／6-31）；name = vendor_kit 或 &amp;lt;repo&amp;gt;"/>
<c id="p3_vkt_r1c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1032.5,100,57" v="extract"/>
<c id="p3_vkt_r1c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1032.5,180,57" v="&amp;lt;repo&amp;gt;|&amp;lt;ref&amp;gt;"/>
<c id="p3_vkt_r1c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1032.5,50,57" v="0..n"/>
<c id="p3_vkt_r1c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1032.5,420,57" v="同 pull 後 docker create … &amp;lt;ref&amp;gt; /x → docker cp c:/dist/. &quot;.tmp.dist.&amp;lt;id&amp;gt;/&amp;lt;repo&amp;gt;/&quot; → docker rm；同一 repo 不得同時有 extract 與 mount"/>
<c id="p3_vkt_r2c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1089.5,100,42" v="mount"/>
<c id="p3_vkt_r2c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1089.5,180,42" v="&amp;lt;repo&amp;gt;|&amp;lt;dir 八進位跳脫&amp;gt;"/>
<c id="p3_vkt_r2c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1089.5,50,42" v="0..n"/>
<c id="p3_vkt_r2c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1089.5,420,42" v="dev 覆寫：解碼後驗 &amp;lt;dir&amp;gt;/dist/init.toml 存在（缺 → 1）→ -v &quot;&amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro&quot;"/>
<c id="p3_vkt_r3c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1131.5,100,57" v="engine"/>
<c id="p3_vkt_r3c0_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="858,1133.5,30,20" v="v2"/>
<c id="p3_vkt_r3c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1131.5,180,57" v="&amp;lt;ref&amp;gt;"/>
<c id="p3_vkt_r3c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1131.5,50,57" v="0..1"/>
<c id="p3_vkt_r3c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1131.5,420,57" v="只在 upgrade（不帶 repo）：apply 會把正規行改成此 ref；啟動器先 pull（或 local 覆寫時 inspect 驗 ID）；有 engine 時本次不得夾帶工具寫入"/>
<c id="p3_vkt_r4c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1188.5,100,26" v="fingerprint"/>
<c id="p3_vkt_r4c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1188.5,180,26" v="&amp;lt;sha256 hex64&amp;gt;"/>
<c id="p3_vkt_r4c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1188.5,50,26" v="恰 1"/>
<c id="p3_vkt_r4c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1188.5,420,26" v="不解析，隨檔交給 apply"/>
<c id="p3_vkt_r5c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1214.5,100,57" v="apply"/>
<c id="p3_vkt_r5c0_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="858,1216.5,30,20" v="v2"/>
<c id="p3_vkt_r5c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1214.5,180,57" v="yes | no"/>
<c id="p3_vkt_r5c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1214.5,50,57" v="恰 1"/>
<c id="p3_vkt_r5c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1214.5,420,57" v="no → 驗完文法後直接 exit 0（sync 快路徑）；no 時不得有 pull／extract／mount／engine；yes → docker 階段後跑 apply &amp;lt;verb&amp;gt; [--dry-run] [args]"/>
<c id="p3_vkt_r6c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1271.5,100,42" v="keep"/>
<c id="p3_vkt_r6c0_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="858,1273.5,30,20" v="v2"/>
<c id="p3_vkt_r6c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1271.5,180,42" v="&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;"/>
<c id="p3_vkt_r6c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1271.5,50,42" v="0..n"/>
<c id="p3_vkt_r6c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1271.5,420,42" v="只在 prune：本專案引用、不可刪的 image（含 local 覆寫的 &amp;lt;tag&amp;gt;）"/>
<c id="p3_vkt_r7c0" parent="p3L2" st="f=#ffffff;s=#999999;b=1" g="790,1313.5,100,26" v="end"/>
<c id="p3_vkt_r7c1" parent="p3L2" st="f=#ffffff;s=#999999" g="890,1313.5,180,26" v="&amp;lt;N&amp;gt;"/>
<c id="p3_vkt_r7c2" parent="p3L2" st="f=#ffffff;s=#999999" g="1070,1313.5,50,26" v="恰 1"/>
<c id="p3_vkt_r7c3" parent="p3L2" st="f=#ffffff;s=#999999" g="1120,1313.5,420,26" v="必為最後一行"/>
<c id="p3_vkr" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,1353.5,1510,77" v="&lt;b&gt;欄位與驗證&lt;/b&gt;：安全字串 [A-Za-z0-9_.-]+；ref [A-Za-z0-9_.:/@-]+（引擎以 image-reference parser 驗證後才輸出）；自由文字（路徑）凡不在 [A-Za-z0-9_./:@+=,-] 的 byte 一律寫成 \0ooo（例：空白 \0040、| \0174、\ \0134），啟動器一行解碼 dir=$(printf &#x27;%b&#x27; &quot;$f2&quot;)、不 eval、不 source；IFS=&#x27;|&#x27; read -r 直接切欄。啟動器先收完整份存到 .tmp.dist.&amp;lt;id&amp;gt;/vk-resolve、驗文法才動 docker：首行 ≠ vk-resolve/&amp;lt;P&amp;gt;、缺 end、N 不符、end 後仍有資料、未知 kind、欄位數不對、fingerprint／apply 不是恰一筆、no 卻附動作記錄、安全字串含非法字元 → 1 印 6-30；引擎宣稱的 P 真不支援 → 3。resolve 結束碼非 0 → 不讀 stdout、原碼傳出。stderr 一律診斷；apply 的 stdout 不作為協定通道。指紋算法見名詞表"/>
<c id="p3_vkr_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1355.5,30,20" v="v2"/>
<c id="p3_self" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,1444.5,750,139" v="&lt;b&gt;自身升級的接手（§3.4）&lt;/b&gt;：「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行。apply 結束後 ref 變了（且 == 計畫的 engine）→ 以新 ref（local 覆寫有 vendor_kit= 則用該 image、inspect 驗 ID）跑 docker run … &amp;lt;新 ref&amp;gt; --protocol P upgrade vendor_kit，結束碼原樣傳出（預期 1 印 6-2）；第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b，不再重跑。&lt;b&gt;救援路徑（§3.5）&lt;/b&gt;：install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help = 單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼永遠可經此叫任何引擎重產薄殼"/>
<c id="p3_self_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="748,1446.5,30,20" v="v2"/>
<c id="p3_fast" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,1444.5,750,139" v="&lt;b&gt;sync 快路徑（Q22）與 sync --verify&lt;/b&gt;：sync（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml vendor_kit ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 frozen → 起引擎 resolve sync。每檔 sha256 verify 只在：CI 為真（frozen）、快路徑有差那次（版本變動）、sync --verify（長形）；sync &amp;lt;repo&amp;gt; 一律起引擎驗該範圍。前提：.vendor_kit/.gitignore 明列 cache/、gen/、version.local.toml、.tmp.*；install 把 .vendor_kit/cache/、gen/、.tmp.* 加進根 .dockerignore。&lt;b&gt;--local 值的判別&lt;/b&gt;：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立 → 1 提示用 ./ 或完整 ref 消歧"/>
<c id="p3_fast_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1446.5,30,20" v="v2"/>
<c id="p3_compat" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="30,1597.5,750,108" v="&lt;b&gt;相容承諾（Q16／Q19／Q23）&lt;/b&gt;：薄殼每次呼叫附 --protocol P（第一版就有），引擎依 P 回應。永久：任何 ≥ floor 的舊薄殼可呼叫新引擎的救援路徑並得正確提示；舊資料永遠可讀可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 3 印 6-36 零寫入。floor = 固定 release 常數（v1.0.0、P=1、schema=1），只能經 ADR 提高；引擎 image LABEL …protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt; 讓啟動器不起容器即可判 floor。降版 upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 P／schema 比）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10；dev vendor_kit -i &amp;lt;舊 image&amp;gt; 禁止重產 tracked 薄殼"/>
<c id="p3_compat_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="748,1599.5,30,20" v="v2"/>
<c id="p3_env" parent="p3L2" st="f=#ffe6cc;s=#d79b00;fs=14" g="790,1597.5,750,108" v="&lt;b&gt;執行環境（19 條）與主機需求&lt;/b&gt;：docker ≥ 19.03（或 Podman ≥ 4.9）、just ≥ 1.33.0、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA、引擎基底 EOL → issue v2。時間戳 UTC ISO 8601；需詢問但無 tty／EOF → 1 印 6-4；所有 docker 資源帶 vendor_kit label；不建 network／volume；離線 upgrade 不支援；worktree 進驗收；submodule 以實測為生效條件"/>
<c id="p3_env_v2" parent="p3L2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,1599.5,30,20" v="v2"/>
<c id="p3b_lg0" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="40,1851.5,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p3b_lg1" st="rhombus;f=#FFF4C3;s=#000000;fs=14" g="260,1841.5,150,66" v="黃：判斷"/>
<c id="p3b_lg2" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="430,1843.5,400,56" v="橙橢圓：需要人動作（1／3 印指令、2 解衝突）"/>
<c id="p3b_lg3" st="ellipse;f=#d5e8d4;s=#000000;fs=14" g="850,1845.5,270,52" v="綠橢圓：成功終點（exit 0）"/>
<c id="p3b_lg4" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1140,1851.5,130,40" v="白：步驟／說明"/>
<c id="p3b_lgt" st="text;s=none;f=none" g="1290,1841.5,300,60" v="實線 = 執行順序；線上文字 = 條件／接續編號&lt;br&gt;淺灰底容器 = ②③ 的分組（標題 = 該段做的事）"/>
<c id="p3b_lg5" st="f=#ffffff;s=#999999" g="40,1917.5,170,40" v="等寬字：檔案內容範例"/>
<c id="p3b_lg6" st="f=#ffe6cc;s=#d79b00;fs=14" g="230,1917.5,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p3b_lg7" st="f=#e6e6e6;s=#999999;b=1" g="440,1917.5,110,40" v="灰底：表頭"/>
<c id="p3b_lg8" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="570,1917.5,200,40" v="右上角綠標籤：v2 改"/>
<c id="p3b_lg8_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="738,1919.5,30,20" v="v2"/>
<c id="p3b_lg9" st="shape=note;f=#ffffff;s=#999999" g="790,1917.5,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p3b_th" st="text;fs=13;s=none;f=none;b=1" g="40,1973.5,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p3b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,2007.5,150,55" v="啟動器"/>
<c id="p3b_tv0" st="f=#ffffff;s=#999999" g="190,2007.5,610,55" v=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框"/>
<c id="p3b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2062.5,150,71" v="主機命令白名單"/>
<c id="p3b_tv1" st="f=#ffffff;s=#999999" g="190,2062.5,610,71" v="啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files；lint 擋清單外"/>
<c id="p3b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2133.5,150,55" v="docker image inspect"/>
<c id="p3b_tv2" st="f=#ffffff;s=#999999" g="190,2133.5,610,55" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）"/>
<c id="p3b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2188.5,150,55" v="docker create／cp"/>
<c id="p3b_tv3" st="f=#ffffff;s=#999999" g="190,2188.5,610,55" v="不執行容器，只建一個容器殼（docker create &amp;lt;ref&amp;gt; /x）再把 /dist 複製出來（docker cp c:/dist/. …）→ docker rm；純資料 image 沒有程式所以不能 docker run；不帶 --platform（daemon 挑原生）"/>
<c id="p3b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2243.5,150,40" v="暫存 .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p3b_tv4" st="f=#ffffff;s=#999999" g="190,2243.5,610,40" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋"/>
<c id="p3b_tk5" st="f=#ffffff;s=#999999;b=1" g="840,2007.5,150,55" v="使用者旗標（-u）"/>
<c id="p3b_tv5" st="f=#ffffff;s=#999999" g="990,2007.5,610,55" v="rootful docker 加 -u &quot;$(id -u):$(id -g)&quot;（寫出的檔才不會變 root 的）；rootless docker（docker info SecurityOptions 含 name=rootless）不加 -u；Podman（docker --version 含 podman）改加 --userns=keep-id、不加 -u"/>
<c id="p3b_tk6" st="f=#ffffff;s=#999999;b=1" g="840,2062.5,150,55" v="REGISTRY_TOKEN／&lt;br&gt;_TOKEN_FILE"/>
<c id="p3b_tv6" st="f=#ffffff;s=#999999" g="990,2062.5,610,55" v="私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v &amp;lt;file&amp;gt;:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt; 指定版本（主機 docker pull 走主機認證）"/>
<c id="p3b_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2117.5,150,55" v="vk-resolve/1"/>
<c id="p3b_tv7" st="f=#ffffff;s=#999999" g="990,2117.5,610,55" v="resolve 的 stdout 文法：首行 vk-resolve/&amp;lt;P&amp;gt;、每行 &amp;lt;kind&amp;gt;|&amp;lt;f1&amp;gt;[|&amp;lt;f2&amp;gt;…]（欄位以單一 | 分隔）、末行 end|&amp;lt;N&amp;gt;；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \0ooo 八進位跳脫（printf &#x27;%b&#x27; 可解）；啟動器先收完整份、驗文法才動 docker"/>
<c id="p3b_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2172.5,150,55" v="輸入指紋"/>
<c id="p3b_tv8" st="f=#ffffff;s=#999999" g="990,2172.5,610,55" v="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12"/>
</page>
<page name="契約 v2：CI 契約⑤ 與驗收矩陣">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="契約⑤ CI 與驗收矩陣（interface_spec §7；下游 check.sh；工具 repo check.sh --dist；自身分層 + 驗收 28 條）"/>
<c id="p3c_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p3c_pend" st="shape=note;f=#ffffff;s=#999999" g="1260,12,340,81" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;&lt;br&gt;check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 每條一情境"/>
<c id="p3L5" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,109,1560,1547" v="契約⑤ CI（下游 check.sh 六步 + Renovate；工具 repo check.sh --dist；vendor_kit 自身分層 + 驗收矩陣）"/>
<c id="p3_k0" parent="p3L5" st="text;s=none;f=none;b=1" g="20,50,200,60" v="下游專案 CI：只呼叫 .vendor_kit/ci/check.sh，一關過才下一關（每格一步）"/>
<c id="k0" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="240,50,190,60" v="⓪ version.local.toml 被 git track？"/>
<c id="k1" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="446,50,120,60" v="① sync（frozen）"/>
<c id="k1_e" edge source="k0" target="k1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k2" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="582,50,170,60" v="② verify（印記 sha256，全部工具）"/>
<c id="k2_e" edge source="k1" target="k2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k3" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="768,50,150,60" v="③ upgrade --dry-run"/>
<c id="k3_e" edge source="k2" target="k3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k4" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="934,50,250,60" v="④ 工具測試 just &amp;lt;repo&amp;gt; check（若有；不得再呼叫 check.sh）"/>
<c id="k4_e" edge source="k3" target="k4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k5" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1200,50,170,60" v="⑤ 專案測試（just check 若有）"/>
<c id="k5_e" edge source="k4" target="k5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k6" parent="p3L5" st="ellipse;f=#d5e8d4;s=#000000;fs=14" g="1386,50,130,60" v="全部通過 → 0"/>
<c id="k6_e" edge source="k5" target="k6" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="k0f" parent="p3L5" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="235.0,150,200,84" v="命中 → 1 拒絕&lt;br&gt;（請勿把 local 覆寫提交）"/>
<c id="k0f_e" edge source="k0" target="k0f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="命中"/>
<c id="k1f" parent="p3L5" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="416.0,254,300,84" v="1：薄殼不符（6-1）、未完成接入（6-13）、baseline 落後（6-5）、任何 local 覆寫；3"/>
<c id="k1f_e" edge source="k1" target="k1f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="升為失敗"/>
<c id="k3f" parent="p3L5" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="763.0,150,280,84" v="CI 為真且需改 tracked 檔&lt;br&gt;→ 1 印清單（version.toml 不動；與 -y 無關）"/>
<c id="k3f_e" edge source="k3" target="k3f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="需改檔"/>
<c id="k3g" parent="p3L5" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="1063.0,150,260,62" v="仍有衝突標記 → 2；印 6-6～6-8 但不紅燈"/>
<c id="k3g_e" edge source="k3" target="k3g" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="943.0,245;1233.0,245" v="衝突"/>
<c id="p3_kr" parent="p3L5" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,362,1520,46" v="&lt;b&gt;check.sh（§7.1）&lt;/b&gt;：第一行 shebang、第二行自描述、其後第一個動作 export CI=1；GitHub／GitLab 一樣、平台無關；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）"/>
<c id="p3_kr_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,364,30,20" v="v2"/>
<c id="p3_rn_l" parent="p3L5" st="text;fs=13;s=none;f=none;b=1" g="20,422,1000,28" v="Renovate 路徑（PR 需合併時；補合併在 PR 分支完成、CI 綠後才 merge）"/>
<c id="rn1" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="20,454,170,64" v="Renovate PR 改 version.toml 一行"/>
<c id="rn2" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="206,454,260,64" v="PR 的 CI 以新版跑 check.sh 完整流程（一行改動本身不構成通過依據）"/>
<c id="rn2_e" edge source="rn1" target="rn2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="rn3" parent="p3L5" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="482,454,140,64" v="需合併 → 1 印 6-5"/>
<c id="rn3_e" edge source="rn2" target="rn3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="rn4" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="638,454,240,64" v="維護者在 PR 分支本機 upgrade &amp;lt;repo&amp;gt; -y → commit → push"/>
<c id="rn4_e" edge source="rn3" target="rn4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="rn5" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="894,454,220,64" v="CI 全部再跑（Renovate 不動有人推過的分支）"/>
<c id="rn5_e" edge source="rn4" target="rn5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="rn6" parent="p3L5" st="ellipse;f=#d5e8d4;s=#000000;fs=14" g="1130,454,110,64" v="綠了才 merge"/>
<c id="rn6_e" edge source="rn5" target="rn6" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p3_c2" parent="p3L5" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,534,1000,155" v="&lt;b&gt;Renovate preset（§7.3；下游自選，vendor_kit 不出 bot）&lt;/b&gt;：放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；下游 extends: [&quot;github&amp;gt;ycpss91255-research/vendor_kit&quot;]；regex manager 匹配 **/.vendor_kit/version.toml（monorepo 子專案亦命中；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR（matchUpdateTypes）；hostRules 依 host 不寫死 ghcr.io；prBodyNotes = 6-25（6-5 的指令 + 「推 commit 後不要勾 rebase/retry」）；不設 gitIgnoredAuthors、不改 rebaseWhen；postUpgradeTasks 不採"/>
<c id="p3_c2_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="988,536,30,20" v="v2"/>
<c id="p3_c3" parent="p3L5" st="f=#ffe6cc;s=#d79b00;fs=14" g="1040,534,500,155" v="&lt;b&gt;工具 repo 的 CI：check.sh --dist（§7.2）&lt;/b&gt;：dist 佈局（files/、init.toml、just/&amp;lt;repo&amp;gt;.just 存在）、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗 [#29]）、以 just 1.33.0 解析每個 &amp;lt;ns&amp;gt;.just（並擋比 1.33 新的功能）、_sync lint（just --dump --dump-format json）、Dockerfile.dist 含 LABEL io.github.&amp;lt;org&amp;gt;.vendor_kit=1、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性"/>
<c id="p3_c3_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,536,30,20" v="v2"/>
<c id="p3_c0" parent="p3L5" st="text;s=none;f=none;b=1" g="20,713,180,60" v="vendor_kit 自身 CI（分層，一關過才下一關；每格一個檢查）"/>
<c id="c_a" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="210,713,84,60" v="env-test"/>
<c id="c_b" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="310,713,84,60" v="test-base"/>
<c id="c_b_e" edge source="c_a" target="c_b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_c1" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="410,713,84,60" v="lint"/>
<c id="c_c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="462,715,30,20" v="v2"/>
<c id="c_c1_e" edge source="c_b" target="c_c1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_c2" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="510,713,84,60" v="unit"/>
<c id="c_c2_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="562,715,30,20" v="v2"/>
<c id="c_c2_e" edge source="c_c1" target="c_c2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_c3" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="610,713,96,60" v="install"/>
<c id="c_c3_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="674,715,30,20" v="v2"/>
<c id="c_c3_e" edge source="c_c2" target="c_c3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_c4" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="722,713,96,60" v="merge"/>
<c id="c_c4_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="786,715,30,20" v="v2"/>
<c id="c_c4_e" edge source="c_c3" target="c_c4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_d" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="834,713,200,60" v="release（image、bootstrap.sh、tar + .digest）"/>
<c id="c_d_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1002,715,30,20" v="v2"/>
<c id="c_d_e" edge source="c_c4" target="c_d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_e" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1050,713,190,60" v="release-test（amd64、arm64 原生 runner）"/>
<c id="c_e_e" edge source="c_d" target="c_e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="c_f" parent="p3L5" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1256,713,250,60" v="驗收：已釋出版驅動候選 + 乾淨 fixture repo 跑完整流程"/>
<c id="c_f_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1474,715,30,20" v="v2"/>
<c id="c_f_e" edge source="c_e" target="c_f" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p3_jm" parent="p3L5" st="f=#ffe6cc;s=#d79b00;fs=14" g="20,789,1520,46" v="just 矩陣 1.33.0 + latest（latest 非 required）；lint 擋比 1.33 新的功能與白名單外主機命令（ADR 記破壞性變更）；驗收用 dev vendor_kit -i &amp;lt;剛 build 的 tag&amp;gt; 同一機制；每版最低環境（docker 19.03、just 1.33.0）跑完整、其他環境（docker 上界、just latest、arm64、WSL2）按世代；驗收 §7.4 條 1–13 缺任一不得出貨；已釋出 image／Release 資產／fixture 永不刪；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」"/>
<c id="p3_jm_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,791,30,20" v="v2"/>
<c id="p3_acc_l" parent="p3L5" st="text;fs=13;s=none;f=none;b=1" g="20,849,900,28" v="驗收矩陣（§7.4；每列一個情境；左右兩表接續）"/>
<c id="p3_acc_h0" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="20,881,40,30" v="#"/>
<c id="p3_acc_h1" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="60,881,150,30" v="情境"/>
<c id="p3_acc_h2" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="210,881,560,30" v="驗什麼"/>
<c id="p3_acc_r0c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,911,40,73" v="1"/>
<c id="p3_acc_r0c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,911,150,73" v="已釋出版驅動候選"/>
<c id="p3_acc_r0c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,913,30,20" v="v2"/>
<c id="p3_acc_r0c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,911,560,73" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1、零 tracked 寫入）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁止由候選樹複製 fixture、禁 stub 引擎"/>
<c id="p3_acc_r1c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,984,40,42" v="2"/>
<c id="p3_acc_r1c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,984,150,42" v="最低環境 × 世代"/>
<c id="p3_acc_r1c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,986,30,20" v="v2"/>
<c id="p3_acc_r1c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,984,560,42" v="每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境按世代覆蓋；成本上限當觸發討論條件"/>
<c id="p3_acc_r2c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1026,40,42" v="3"/>
<c id="p3_acc_r2c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1026,150,42" v="升級後 == 全新安裝"/>
<c id="p3_acc_r2c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1028,30,20" v="v2"/>
<c id="p3_acc_r2c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1026,560,42" v="升級後 .vendor_kit/ tracked 內容 == 用 C 全新 install + add（排除時間戳、digest、written_by）"/>
<c id="p3_acc_r3c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1068,40,26" v="4"/>
<c id="p3_acc_r3c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1068,150,26" v="連續升級"/>
<c id="p3_acc_r3c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1070,30,20" v="v2"/>
<c id="p3_acc_r3c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1068,560,26" v="r_i → r_j → C；固定 floor 直接跳升 C"/>
<c id="p3_acc_r4c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1094,40,42" v="5"/>
<c id="p3_acc_r4c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1094,150,42" v="降版"/>
<c id="p3_acc_r4c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1096,30,20" v="v2"/>
<c id="p3_acc_r4c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1094,560,42" v="upgrade vendor_kit@&amp;lt;舊版&amp;gt;：同 P／schema 成功；跨 schema 改檔前拒絕 3 印 6-10、零寫入"/>
<c id="p3_acc_r5c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1136,40,42" v="6"/>
<c id="p3_acc_r5c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1136,150,42" v="&amp;lt; floor 太舊"/>
<c id="p3_acc_r5c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1138,30,20" v="v2"/>
<c id="p3_acc_r5c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1136,560,42" v="唯一可用 synthetic fixture；任一動詞 → 3 印 6-18、零寫入；floor 檢查在任何上網之前（斷網也回 3）"/>
<c id="p3_acc_r6c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1178,40,57" v="7"/>
<c id="p3_acc_r6c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1178,150,57" v="舊 bootstrap.sh 再跑"/>
<c id="p3_acc_r6c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1180,30,20" v="v2"/>
<c id="p3_acc_r6c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1178,560,57" v="在已升級 repo 再跑：用 version.toml 指定引擎，不降版"/>
<c id="p3_acc_r7c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1235,40,26" v="8"/>
<c id="p3_acc_r7c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1235,150,26" v="舊引擎讀新檔"/>
<c id="p3_acc_r7c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1237,30,20" v="v2"/>
<c id="p3_acc_r7c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1235,560,26" v="dev vendor_kit -i 舊 image：寫入前拒絕 3 印 6-19；不重產 tracked 薄殼"/>
<c id="p3_acc_r8c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1261,40,42" v="9"/>
<c id="p3_acc_r8c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1261,150,42" v="只改第一行後 CI=true sync"/>
<c id="p3_acc_r8c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1263,30,20" v="v2"/>
<c id="p3_acc_r8c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1261,560,42" v="模擬 Renovate、驗 CI 真值規則 → 1 列薄殼不符、零 tracked 寫入"/>
<c id="p3_acc_r9c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1303,40,42" v="10"/>
<c id="p3_acc_r9c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1303,150,42" v="fresh clone 無 gen/"/>
<c id="p3_acc_r9c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1305,30,20" v="v2"/>
<c id="p3_acc_r9c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1303,560,42" v="just vendor_kit 列出 vendor_kit 命名空間不觸網（工具命名空間 sync 後才出現，mod? 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行"/>
<c id="p3_acc_r10c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1345,40,42" v="11"/>
<c id="p3_acc_r10c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1345,150,42" v="使用者改薄殼／未納管檔／append"/>
<c id="p3_acc_r10c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1347,30,20" v="v2"/>
<c id="p3_acc_r10c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1345,560,42" v="不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn"/>
<c id="p3_acc_r11c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1387,40,42" v="12"/>
<c id="p3_acc_r11c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1387,150,42" v="中斷與重跑"/>
<c id="p3_acc_r11c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1389,30,20" v="v2"/>
<c id="p3_acc_r11c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1387,560,42" v="resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗"/>
<c id="p3_acc_r12c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1429,40,42" v="13"/>
<c id="p3_acc_r12c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1429,150,42" v="歷史 parser × 異常 TOML"/>
<c id="p3_acc_r12c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1431,30,20" v="v2"/>
<c id="p3_acc_r12c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1429,560,42" v="BOM、空白、重複 vendor_kit 行 → 1、schema 位置、local 覆寫、尾端註解"/>
<c id="p3_acc_r13c0" parent="p3L5" st="f=#ffffff;s=#999999" g="20,1471,40,26" v="14"/>
<c id="p3_acc_r13c1" parent="p3L5" st="f=#ffffff;s=#999999" g="60,1471,150,26" v="just 矩陣"/>
<c id="p3_acc_r13c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="178,1473,30,20" v="v2"/>
<c id="p3_acc_r13c2" parent="p3L5" st="f=#ffffff;s=#999999" g="210,1471,560,26" v="1.33.0 + latest（latest 非 required）"/>
<c id="p3_accb_h0" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="790,881,40,30" v="#"/>
<c id="p3_accb_h1" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="830,881,150,30" v="情境"/>
<c id="p3_accb_h2" parent="p3L5" st="f=#e6e6e6;s=#999999;b=1" g="980,881,560,30" v="驗什麼"/>
<c id="p3_accb_r0c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,911,40,42" v="15"/>
<c id="p3_accb_r0c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,911,150,42" v="amd64 與 arm64 原生 runner"/>
<c id="p3_accb_r0c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,913,30,20" v="v2"/>
<c id="p3_accb_r0c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,911,560,42" v="各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致"/>
<c id="p3_accb_r1c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,953,40,57" v="16"/>
<c id="p3_accb_r1c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,953,150,57" v="離線包（Q26）"/>
<c id="p3_accb_r1c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,955,30,20" v="v2"/>
<c id="p3_accb_r1c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,953,560,57" v="無法連 GHCR 的機器用 bootstrap.sh --local &amp;lt;tar&amp;gt;（旁檔 .digest）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 local_image_id；旁檔缺 → 1；amd64／arm64 各一次"/>
<c id="p3_accb_r2c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1010,40,57" v="17"/>
<c id="p3_accb_r2c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1010,150,57" v="離線可用（Q22／Q26）"/>
<c id="p3_accb_r2c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1012,30,20" v="v2"/>
<c id="p3_accb_r2c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1010,560,57" v="本機已有 image 後斷網 → just &amp;lt;ns&amp;gt; build（自動 sync 快路徑）與 just vendor_kit sync 必須成功且不起 pull；斷網 + 無 image → 1 印 6-31 於 --timeout 5 內結束、不 hang"/>
<c id="p3_accb_r3c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1067,40,57" v="18"/>
<c id="p3_accb_r3c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1067,150,57" v="私有工具"/>
<c id="p3_accb_r3c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1069,30,20" v="v2"/>
<c id="p3_accb_r3c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1067,560,57" v="add &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt; 可拉；add &amp;lt;repo&amp;gt; 無 token → 1 印 6-3；update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token"/>
<c id="p3_accb_r4c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1124,40,42" v="19"/>
<c id="p3_accb_r4c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1124,150,42" v="append"/>
<c id="p3_accb_r4c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1126,30,20" v="v2"/>
<c id="p3_accb_r4c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1124,560,42" v="LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 .dockerignore 三行 append → uninstall 刪"/>
<c id="p3_accb_r5c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1166,40,42" v="20"/>
<c id="p3_accb_r5c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1166,150,42" v="空白路徑"/>
<c id="p3_accb_r5c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1168,30,20" v="v2"/>
<c id="p3_accb_r5c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1166,560,42" v="專案根含空白與 $、dev -p &quot;含 空白/路徑&quot;；vk-resolve mount 八進位跳脫往返；just vendor_kit add --help 到引擎"/>
<c id="p3_accb_r6c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1208,40,42" v="21"/>
<c id="p3_accb_r6c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1208,150,42" v="worktree／submodule"/>
<c id="p3_accb_r6c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1210,30,20" v="v2"/>
<c id="p3_accb_r6c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1208,560,42" v="git worktree（.git 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）"/>
<c id="p3_accb_r7c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1250,40,42" v="22"/>
<c id="p3_accb_r7c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1250,150,42" v="rootless docker／Podman"/>
<c id="p3_accb_r7c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1252,30,20" v="v2"/>
<c id="p3_accb_r7c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1250,560,42" v="setup-docker-action rootless: true（不加 -u、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：--userns=keep-id）各跑完整流程；uid 12345 無 passwd 項"/>
<c id="p3_accb_r8c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1292,40,57" v="23"/>
<c id="p3_accb_r8c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1292,150,57" v="prune"/>
<c id="p3_accb_r8c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1294,30,20" v="v2"/>
<c id="p3_accb_r8c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1292,560,57" v="完整流程前後 docker network ls／volume ls 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊工具 image 刪、version.toml 引用的與 local 覆寫 tag 保留；--dry-run 零刪除；未恢復的 .tmp.* 不刪"/>
<c id="p3_accb_r9c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1349,40,42" v="24"/>
<c id="p3_accb_r9c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1349,150,42" v="多工具彙總（Q27）"/>
<c id="p3_accb_r9c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1351,30,20" v="v2"/>
<c id="p3_accb_r9c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1349,560,42" v="兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1"/>
<c id="p3_accb_r10c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1391,40,42" v="25"/>
<c id="p3_accb_r10c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1391,150,42" v="F1 fixture（just 1.33.0）"/>
<c id="p3_accb_r10c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1393,30,20" v="v2"/>
<c id="p3_accb_r10c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1391,560,42" v="cache 缺檔時 just vendor_kit sync 可進入（mod?）；just &amp;lt;ns&amp;gt; build 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 _sync 的模組"/>
<c id="p3_accb_r11c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1433,40,26" v="26"/>
<c id="p3_accb_r11c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1433,150,26" v="無 tty／EOF"/>
<c id="p3_accb_r11c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1435,30,20" v="v2"/>
<c id="p3_accb_r11c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1433,560,26" v="CI 無 -y 需詢問 → 1 印 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑"/>
<c id="p3_accb_r12c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1459,40,42" v="27"/>
<c id="p3_accb_r12c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1459,150,42" v="Renovate 實際 repo"/>
<c id="p3_accb_r12c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1461,30,20" v="v2"/>
<c id="p3_accb_r12c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1459,560,42" v="人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中"/>
<c id="p3_accb_r13c0" parent="p3L5" st="f=#ffffff;s=#999999" g="790,1501,40,26" v="28"/>
<c id="p3_accb_r13c1" parent="p3L5" st="f=#ffffff;s=#999999" g="830,1501,150,26" v="驗收動詞集合"/>
<c id="p3_accb_r13c1_v2" parent="p3L5" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="948,1503,30,20" v="v2"/>
<c id="p3_accb_r13c2" parent="p3L5" st="f=#ffffff;s=#999999" g="980,1501,560,26" v="由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅"/>
<c id="p3c_lg0" st="ellipse;f=#ffe6cc;s=#000000;fs=14" g="40,1678,400,56" v="橙橢圓：需要人動作（1／3 印指令、2 解衝突）"/>
<c id="p3c_lg1" st="ellipse;f=#d5e8d4;s=#000000;fs=14" g="460,1680,270,52" v="綠橢圓：成功終點（exit 0）"/>
<c id="p3c_lg2" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="750,1686,130,40" v="白：步驟／說明"/>
<c id="p3c_lg3" st="f=#ffe6cc;s=#d79b00;fs=14" g="900,1686,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p3c_lg4" st="f=#e6e6e6;s=#999999;b=1" g="1110,1686,110,40" v="灰底：表頭"/>
<c id="p3c_lgt" st="text;s=none;f=none" g="1240,1676,300,60" v="實線 = 執行順序；線上文字 = 條件&lt;br&gt;驗收表：一列一個情境"/>
<c id="p3c_lg5" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="40,1752,200,40" v="淺灰底：分組（無狀態意義）"/>
<c id="p3c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="260,1752,200,40" v="右上角綠標籤：v2 改"/>
<c id="p3c_lg6_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="428,1754,30,20" v="v2"/>
<c id="p3c_lg7" st="shape=note;f=#ffffff;s=#999999" g="480,1752,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p3c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1808,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p3c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1842,150,55" v="check.sh 六步（⓪–⑤）"/>
<c id="p3c_tv0" st="f=#ffffff;s=#999999" g="190,1842,610,55" v="vendor_kit 出貨、進 git 的腳本（第二行自描述、第一個動作 export CI=1）：⓪ local 被 track → 1；① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；整體結束碼 = 第一個失敗步驟的碼"/>
<c id="p3c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1897,150,55" v="check.sh --dist"/>
<c id="p3c_tv1" st="f=#ffffff;s=#999999" g="190,1897,610,55" v="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致"/>
<c id="p3c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1952,150,55" v="frozen（CI 為真）"/>
<c id="p3c_tv2" st="f=#ffffff;s=#999999" g="190,1952,610,55" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"/>
<c id="p3c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2007,150,40" v="CI／runner"/>
<c id="p3c_tv3" st="f=#ffffff;s=#999999" g="190,2007,610,40" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）"/>
<c id="p3c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2047,150,55" v="Renovate preset"/>
<c id="p3c_tv4" st="f=#ffffff;s=#999999" g="190,2047,610,55" v="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25"/>
<c id="p3c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2102,150,40" v="Renovate／PR／rebase"/>
<c id="p3c_tv5" st="f=#ffffff;s=#999999" g="190,2102,610,40" v="Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）"/>
<c id="p3c_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2142,150,55" v="env-test／test-base"/>
<c id="p3c_tv6" st="f=#ffffff;s=#999999" g="190,2142,610,55" v="vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後 lint／unit／install／merge 各測試 stage 的共同基底，環境不對就沒有任何測試會跑"/>
<c id="p3c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1842,150,40" v="lint／unit／測試矩陣"/>
<c id="p3c_tv7" st="f=#ffffff;s=#999999" g="990,1842,610,40" v="lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）"/>
<c id="p3c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1882,150,40" v="release／release-test"/>
<c id="p3c_tv8" st="f=#ffffff;s=#999999" g="990,1882,610,40" v="release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次"/>
<c id="p3c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1922,150,40" v="fixture repo"/>
<c id="p3c_tv9" st="f=#ffffff;s=#999999" g="990,1922,610,40" v="驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪"/>
<c id="p3c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1962,150,40" v="floor"/>
<c id="p3c_tv10" st="f=#ffffff;s=#999999" g="990,1962,610,40" v="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）"/>
<c id="p3c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2002,150,40" v="rootless／Podman"/>
<c id="p3c_tv11" st="f=#ffffff;s=#999999" g="990,2002,610,40" v="rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收"/>
<c id="p3c_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2042,150,40" v="worktree／submodule"/>
<c id="p3c_tv12" st="f=#ffffff;s=#999999" g="990,2042,610,40" v="git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）"/>
<c id="p3c_tk13" st="f=#ffffff;s=#999999;b=1" g="840,2082,150,40" v="離線可用（Q26）"/>
<c id="p3c_tv13" st="f=#ffffff;s=#999999" g="990,2082,610,40" v="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援"/>
<c id="p3c_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2122,150,40" v="多工具彙總（Q27）"/>
<c id="p3c_tv14" st="f=#ffffff;s=#999999" g="990,2122,610,40" v="不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列"/>
</page>
<page name="架構圖 v2">
<c id="title" st="text;fs=18;b=1" g="40,20,1200,34" v="架構圖 v2 ── 主機、引擎 8 模組、registry（只畫模組、最小單元、模組間傳的資料）"/>
<c id="p4_num" st="text;s=none;f=none" g="40,56,1200,26" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字"/>
<c id="p4_np" st="shape=note;f=#ffffff;s=#999999" g="1000,12,600,65" v="&lt;b&gt;本頁無待拍板&lt;/b&gt;：本頁只畫模組、最小單元、模組間傳的資料（箭頭只標傳什麼，不標動作；雙箭頭 = 讀寫都有）；載入順序／操作順序／sync 判斷／拉取條件／退出流程一律見流程頁（p5～）。啟動器不算引擎模組（主機側薄殼）"/>
<c id="p4G" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#e1d5e7;swf=#ffffff;s=#9673a6" g="40,96,1560,162" v="GHCR（ghcr.io）── 兩種 image 都多架構；拉取都由主機上的啟動器執行，引擎容器內不呼叫 docker"/>
<c id="g_eng" parent="p4G" st="f=#e1d5e7;s=#9673a6;fs=14" g="20,50,520,92" v="&lt;b&gt;引擎 image ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN（公開）&lt;/b&gt;&lt;br&gt;多架構 amd64 + arm64；LABEL …vendor_kit=1、.protocol、.schema；一個專案用 version.toml 正規行那一版；引擎覆寫 vendor_kit=&amp;lt;tag&amp;gt;（version.local.toml）時啟動器 docker image inspect 驗 ID 後直接用本機 image、不 pull；也出 docker save tar + .digest（#27）；已釋出永不刪"/>
<c id="g_eng_v2" parent="p4G" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,52,30,20" v="v2"/>
<c id="g_dist" parent="p4G" st="f=#e1d5e7;s=#9673a6;fs=14" g="560,50,500,92" v="&lt;b&gt;工具 image ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;&lt;/b&gt;&lt;br&gt;多架構 amd64 + arm64（同一次 buildx、COPY-only）；純資料 FROM scratch 只有 /dist；LABEL …vendor_kit=1；version.toml 與印記記 index digest"/>
<c id="g_dist_v2" parent="p4G" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1028,52,30,20" v="v2"/>
<c id="g_note" parent="p4G" st="f=#ffe6cc;s=#d79b00;fs=14" g="1080,50,460,92" v="&lt;b&gt;registry 模組只查 tag／index digest&lt;/b&gt;（update／add／upgrade 用；私有 registry 用 VENDOR_KIT_REGISTRY_TOKEN 或 TOKEN_FILE（-v 掛 /run/vk-token），或改用 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;）&lt;br&gt;sync 不查最新版；只拉鎖定版；拉取由主機上的啟動器執行，先 docker image inspect 再 pull（逾時）"/>
<c id="g_note_v2" parent="p4G" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1508,52,30,20" v="v2"/>
<c id="p4H" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,328,520,1342" v="主機（使用者電腦／CI runner）"/>
<c id="h0" parent="p4H" st="ellipse;f=#FFF4C3;s=#000000;fs=14" g="20,50,220,106" v="使用者&lt;br&gt;打 just vendor_kit &amp;lt;動詞&amp;gt; …&lt;br&gt;或 just &amp;lt;ns&amp;gt; …"/>
<c id="h1" parent="p4H" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="20,186,220,61" v="根 justfile（使用者的，進 git）&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;"/>
<c id="h1_v2" parent="p4H" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,188,30,20" v="v2"/>
<c id="h2" parent="p4H" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="20,277,220,108" v=".vendor_kit/entry.just（進 git）&lt;br&gt;mod vendor_kit &#x27;vendor.just&#x27;&lt;br&gt;import? &#x27;gen/tools.just&#x27;"/>
<c id="h3" parent="p4H" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="20,415,220,79" v=".vendor_kit/vendor.just（進 git）&lt;br&gt;動詞 recipe（一行轉發）&lt;br&gt;+ 啟動器本體（POSIX sh）"/>
<c id="h3_v2" parent="p4H" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,417,30,20" v="v2"/>
<c id="h4" parent="p4H" st="f=#f8cecc;s=#b85450;fs=14" g="20,524,220,296" v="&lt;b&gt;啟動器&lt;/b&gt;（主機側薄殼，非引擎模組；主機需 docker ≥ 19.03、sh、just ≥ 1.33.0）&lt;br&gt;下列為責任單元；命令步驟見流程頁與 p3b"/>
<c id="h4_v2" parent="p4H" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="208,526,30,20" v="v2"/>
<c id="h4_u0_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,632,72,24" v="讀引擎 ref"/>
<c id="h4_u0_1" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="104,632,124,24" v="取得引擎／工具 image"/>
<c id="h4_u1_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,662,110,24" v="展開 /dist 到暫存"/>
<c id="h4_u1_1" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="142,662,68,24" v="起引擎容器"/>
<c id="h4_u2_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,692,114,24" v="vk-resolve 驗文法"/>
<c id="h4_u3_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,722,124,24" v="協定旗標 --protocol"/>
<c id="h4_u4_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,752,82,24" v="清理（trap）"/>
<c id="h4_u4_1" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="114,752,68,24" v="pull 逾時"/>
<c id="h4_u5_0" parent="p4H" st="f=#ffffff;s=#666666;fs=10" g="26,782,74,24" v="資源 label"/>
<c id="h_vk" parent="p4H" st="f=#ffffff;s=#999999" g="20,840,480,217" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/            # 契約② p2，根目錄只多這個&lt;br&gt;├─ version.toml        # 進 git：唯一來源&lt;br&gt;├─ version.local.toml  # 不進 git：dev 覆寫&lt;br&gt;├─ .gitignore          # 進 git：我們自己的&lt;br&gt;├─ entry.just          # 進 git：mod + import?&lt;br&gt;├─ vendor.just         # 進 git：動詞 + 啟動器&lt;br&gt;├─ ci/check.sh         # 進 git：CI 六步（⓪–⑤）&lt;br&gt;├─ baseline/           # 進 git：.gitkeep、&amp;lt;repo&amp;gt;/ 範本 + metadata&lt;br&gt;├─ gen/                # 不進 git：tools.just、.stamp、&lt;br&gt;│                      #   &amp;lt;repo&amp;gt;.stamp（印記）&lt;br&gt;├─ .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml  # 不進 git：進度日誌&lt;br&gt;├─ .tmp.dist.&amp;lt;id&amp;gt;/     # 不進 git：啟動器暫存&lt;br&gt;└─ cache/&amp;lt;repo&amp;gt;/       # 不進 git：工具檔展開&lt;/pre&gt;"/>
<c id="tmp" parent="p4H" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="260,50,200,94" v="暫存 .vendor_kit/&lt;br&gt;.tmp.dist.&amp;lt;id&amp;gt;/（專案內）&lt;br&gt;工具 /dist 展開副本 + vk-resolve&lt;br&gt;（唯讀掛進引擎當 /dist）"/>
<c id="g1" parent="p4H" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="260,277,240,108" v=".vendor_kit/gen/tools.just（不進 git）&lt;br&gt;mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/&lt;br&gt;just/&amp;lt;ns&amp;gt;.just&#x27;&lt;br&gt;一行一命名空間"/>
<c id="g1_v2" parent="p4H" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="468,279,30,20" v="v2"/>
<c id="g2" parent="p4H" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="260,415,240,79" v="工具命名空間 just &amp;lt;ns&amp;gt; …&lt;br&gt;= cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&lt;br&gt;裡的 recipe"/>
<c id="g2_v2" parent="p4H" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="468,417,30,20" v="v2"/>
<c id="p4E" st="swimlane;startSize=38;b=1;fs=16;container=1;collapsible=1;f=#e1d5e7;swf=#ffffff;s=#9673a6" g="600,328,560,1342" v="引擎容器 vendor_kit:vN（8 個模組；每個模組列最小單元，一格一個）"/>
<c id="m_reg" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="290,164,250,128" v="&lt;b&gt;registry&lt;/b&gt;：查 GHCR"/>
<c id="m_reg_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,166,30,20" v="v2"/>
<c id="m_reg_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,194,164,24" v="查 tag（SemVer 最大正式版）"/>
<c id="m_reg_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,224,106,24" v="查 index digest"/>
<c id="m_reg_u1_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="408,224,118,24" v="token／token file"/>
<c id="m_reg_u2_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,254,38,24" v="逾時"/>
<c id="m_ver" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="290,314,250,144" v="&lt;b&gt;version&lt;/b&gt;：version.toml／local 讀寫"/>
<c id="m_ver_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,316,30,20" v="v2"/>
<c id="m_ver_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,360,108,24" v="讀 toml（正規行）"/>
<c id="m_ver_u0_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="410,360,58,24" v="寫 toml"/>
<c id="m_ver_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,390,80,24" v="schema 轉換"/>
<c id="m_ver_u1_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="382,390,48,24" v="flock"/>
<c id="m_ver_u1_2" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="436,390,38,24" v="指紋"/>
<c id="m_ver_u2_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,420,58,24" v="進度日誌"/>
<c id="m_ver_u2_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="360,420,82,24" v="label／keep"/>
<c id="m_mat" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="290,480,250,172" v="&lt;b&gt;materialize&lt;/b&gt;：/dist → cache/&amp;lt;repo&amp;gt;/"/>
<c id="m_mat_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,482,30,20" v="v2"/>
<c id="m_mat_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,526,74,24" v="展開 /dist"/>
<c id="m_mat_u0_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="376,526,58,24" v="路徑驗證"/>
<c id="m_mat_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,556,140,24" v="印記 gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="m_mat_u2_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,586,96,24" v="verify sha256"/>
<c id="m_bl" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="290,674,250,114" v="&lt;b&gt;baseline&lt;/b&gt;：baseline/&amp;lt;repo&amp;gt;/ + metadata"/>
<c id="m_bl_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,676,30,20" v="v2"/>
<c id="m_bl_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,720,58,24" v="範本副本"/>
<c id="m_bl_u0_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="360,720,66,24" v="metadata"/>
<c id="m_bl_u0_2" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="432,720,74,24" v="五態 state"/>
<c id="m_bl_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,750,96,24" v="declined_hash"/>
<c id="m_bl_u1_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="398,750,72,24" v="conflicts"/>
<c id="m_lg" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="290,966,250,354" v="&lt;b&gt;launcher-gen&lt;/b&gt;：薄殼、gen/、根 justfile 一行、根 .dockerignore 三行"/>
<c id="m_lg_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="508,968,30,20" v="v2"/>
<c id="m_lg_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,1027,58,24" v="薄殼四檔"/>
<c id="m_lg_u0_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="360,1027,68,24" v="自描述首行"/>
<c id="m_lg_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,1057,122,24" v="tools.just（mod?）"/>
<c id="m_lg_u1_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="424,1057,66,24" v="check.sh"/>
<c id="m_lg_u2_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="296,1087,54,24" v=".stamp"/>
<c id="m_lg_u2_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="356,1087,92,24" v="justfile 四行"/>
<c id="m_mg" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="296,820,116,114" v="&lt;b&gt;merge&lt;/b&gt;：逐檔合併"/>
<c id="m_mg_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="380,822,30,20" v="v2"/>
<c id="m_mg_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="302,866,48,24" v="狀態機"/>
<c id="m_mg_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="302,896,78,24" v="merge-file"/>
<c id="m_init" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="422,820,116,114" v="&lt;b&gt;init&lt;/b&gt;：初始檔"/>
<c id="m_init_v2" parent="p4E" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="506,822,30,20" v="v2"/>
<c id="m_init_u0_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="428,866,38,24" v="建檔"/>
<c id="m_init_u0_1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="472,866,54,24" v="append"/>
<c id="m_init_u1_0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="428,896,58,24" v="新檔詢問"/>
<c id="grp_im" parent="p4E" st="f=none;s=#666666;dashed=1" g="290,810,250,134"/>
<c id="m_cli" parent="p4E" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="20,50,140,1270" v="&lt;b&gt;cli&lt;/b&gt;"/>
<c id="m_cli_u0" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,80,120,24" v="子命令解析"/>
<c id="m_cli_u1" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,110,120,24" v="--protocol P"/>
<c id="m_cli_u2" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,140,120,24" v="resolve／apply"/>
<c id="m_cli_u3" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,170,120,24" v="詢問／-y／tty"/>
<c id="m_cli_u4" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,200,120,24" v="結束碼 0/1/2/3"/>
<c id="m_cli_u5" parent="p4E" st="f=#ffffff;s=#666666;fs=10" g="30,230,120,24" v="呼叫其他模組"/>
<c id="d_reg" edge source="m_reg" target="m_cli" st="es=orthogonalEdgeStyle;s=default;fc=default" v="tag, index digest"/>
<c id="d_ver" edge source="m_cli" target="m_ver" st="es=orthogonalEdgeStyle;s=default;fc=default" v="version.toml 內容&lt;br&gt;指紋"/>
<c id="d_mat" edge source="m_cli" target="m_mat" st="es=orthogonalEdgeStyle;s=default;fc=default" v="/dist 路徑、&amp;lt;repo&amp;gt;"/>
<c id="d_bl" edge source="m_bl" target="m_cli" st="es=orthogonalEdgeStyle;s=default;fc=default" v="metadata"/>
<c id="d_im" edge source="m_cli" target="grp_im" st="es=orthogonalEdgeStyle;s=default;fc=default" v="檔案清單&lt;br&gt;逐檔決定"/>
<c id="d_lg" edge source="m_cli" target="m_lg" st="es=orthogonalEdgeStyle;s=default;fc=default" v="引擎 ref、動詞清單"/>
<c id="d_mat_bl" edge source="m_mat" target="m_bl" st="es=orthogonalEdgeStyle;s=default;fc=default" v="cache 路徑、印記"/>
<c id="d_im_bl" edge source="grp_im" target="m_bl" st="es=orthogonalEdgeStyle;s=default;fc=default" v="檔案清單、逐檔決定"/>
<c id="p4P" st="swimlane;startSize=38;b=1;fs=18;container=1;collapsible=1;f=#d5e8d4;swf=#ffffff;s=#000000" g="1320,328,280,1342" v="專案根（掛載為 /repo）"/>
<c id="f_note" parent="p4P" st="shape=note;f=#ffffff;s=#999999" g="15,50,240,94" v="整個專案根 -v &amp;lt;專案根&amp;gt;:/repo -w /repo 掛進引擎（可寫）；引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.&amp;lt;id&amp;gt;/ 唯讀掛 /dist/&amp;lt;repo&amp;gt;"/>
<c id="f_ver" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="15,314,240,36" v="version.toml（進 git）"/>
<c id="f_ver_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,316,30,20" v="v2"/>
<c id="f_vl" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="15,358,240,36" v="version.local.toml（dev 覆寫）"/>
<c id="f_vl_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,360,30,20" v="v2"/>
<c id="f_repo" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333;b=1" g="15,480,240,132" v="cache/&amp;lt;repo&amp;gt;/（不進 git，不可改）"/>
<c id="f_repo_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,482,30,20" v="v2"/>
<c id="f_repo_f0" parent="f_repo" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="10,44,210,24" v="files/…"/>
<c id="f_repo_f1" parent="f_repo" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="10,72,210,24" v="init.toml"/>
<c id="f_repo_f2" parent="f_repo" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="10,100,210,24" v="just/&amp;lt;ns&amp;gt;.just"/>
<c id="f_stamp" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="15,620,240,32" v="gen/&amp;lt;repo&amp;gt;.stamp（印記）"/>
<c id="f_stamp_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,622,30,20" v="v2"/>
<c id="f_bl" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366;b=1" g="15,674,240,90" v="baseline/&amp;lt;repo&amp;gt;/（進 git）"/>
<c id="f_bl_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,676,30,20" v="v2"/>
<c id="f_bl_f0" parent="f_bl" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,30,210,24" v="範本副本（上次合併的）"/>
<c id="f_bl_f1" parent="f_bl" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,58,210,24" v="metadata .vendor_kit.toml"/>
<c id="f_user" parent="p4P" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366;b=1" g="15,810,240,104" v="初始檔（使用者的，進 git；永不刪、永不覆蓋）"/>
<c id="f_user_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,812,30,20" v="v2"/>
<c id="f_user_f0" parent="f_user" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,44,210,24" v="Dockerfile 等（copy）"/>
<c id="f_user_f1" parent="f_user" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,72,210,24" v="根 .gitignore 幾行（append）"/>
<c id="f_just" parent="p4P" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="15,966,240,50" v="根 justfile（使用者的，進 git）&lt;br&gt;import 一行；新檔另有 default 兩行"/>
<c id="f_just_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,968,30,20" v="v2"/>
<c id="f_di" parent="p4P" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="15,1024,240,44" v="根 .dockerignore（使用者的）&lt;br&gt;三行（問後 append）"/>
<c id="f_di_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,1026,30,20" v="v2"/>
<c id="f_shell" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366;b=1" g="15,1076,240,146" v="自有薄殼（進 git；首行自描述）"/>
<c id="f_shell_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,1078,30,20" v="v2"/>
<c id="f_shell_f0" parent="f_shell" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,30,210,24" v="entry.just"/>
<c id="f_shell_f1" parent="f_shell" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,58,210,24" v="vendor.just"/>
<c id="f_shell_f2" parent="f_shell" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,86,210,24" v=".gitignore"/>
<c id="f_shell_f3" parent="f_shell" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="10,114,210,24" v="ci/check.sh"/>
<c id="f_gen" parent="p4P" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333;b=1" g="15,1230,240,90" v="gen/（不進 git）"/>
<c id="f_gen_v2" parent="p4P" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="223,1232,30,20" v="v2"/>
<c id="f_gen_f0" parent="f_gen" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="10,30,210,24" v="tools.just（mod? 行）"/>
<c id="f_gen_f1" parent="f_gen" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="10,58,210,24" v=".stamp（只記引擎 ref）"/>
<c id="w_ver" edge source="m_ver" target="f_ver" st="es=orthogonalEdgeStyle;s=default;fc=default" v="version.toml 內容"/>
<c id="w_vl" edge source="m_ver" target="f_vl" st="es=orthogonalEdgeStyle;s=default;fc=default" v="覆寫行（path:／&lt;br&gt;tag + image ID）"/>
<c id="w_repo" edge source="m_mat" target="f_repo" st="es=orthogonalEdgeStyle;s=default;fc=default" v="展開的工具檔&lt;br&gt;（整批替換）"/>
<c id="w_stamp" edge source="m_mat" target="f_stamp" st="es=orthogonalEdgeStyle;s=default;fc=default" v="index digest&lt;br&gt;+ 每檔 sha256"/>
<c id="w_bl" edge source="m_bl" target="f_bl" st="es=orthogonalEdgeStyle;s=default;fc=default" v="範本副本、metadata"/>
<c id="w_user" edge source="grp_im" target="f_user" st="es=orthogonalEdgeStyle;s=default;fc=default" v="初始檔內容&lt;br&gt;（現況／結果）"/>
<c id="w_just" edge source="m_lg" target="f_just" st="es=orthogonalEdgeStyle;s=default;fc=default" v="import 那一行"/>
<c id="w_di" edge source="m_lg" target="f_di" st="es=orthogonalEdgeStyle;s=default;fc=default" v=".dockerignore&lt;br&gt;三行"/>
<c id="w_shell" edge source="m_lg" target="f_shell" st="es=orthogonalEdgeStyle;s=default;fc=default" v="薄殼四檔內容&lt;br&gt;（首行／模板）"/>
<c id="w_gen" edge source="m_lg" target="f_gen" st="es=orthogonalEdgeStyle;s=default;fc=default" v="tools.just、&lt;br&gt;.stamp 內容"/>
<c id="run_cli" edge source="h4" target="m_cli" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.5,0,," v="動詞、參數、--protocol P →&lt;br&gt;← 結束碼、vk-resolve 清單"/>
<c id="mount_dist" edge source="tmp" target="p4E" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.5,0,," v="/dist/&amp;lt;repo&amp;gt;&lt;br&gt;（唯讀）"/>
<c id="pull_eng" edge source="g_eng" target="p4H" st="es=orthogonalEdgeStyle;s=default;fc=default" v="引擎 image&lt;br&gt;（覆寫時本機 image）"/>
<c id="pull_dist" edge source="g_dist" target="p4H" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.3,0,," pts="700,314;470,314" v="工具 image 的 /dist 層&lt;br&gt;→ .tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="q_reg" edge source="p4E" target="g_dist" st="es=orthogonalEdgeStyle;s=default;fc=default" v="tag、index digest"/>
<c id="p4_lg0" st="f=#e1d5e7;s=#9673a6;fs=14" g="40,1710,170,40" v="紫：image（引擎與工具）"/>
<c id="p4_lg1" st="f=#f8cecc;s=light-dark(#000000,#9577A3);fs=14" g="230,1710,130,40" v="紅：引擎模組"/>
<c id="p4_lg2" st="f=#ffffff;s=#666666;fs=10" g="380,1710,140,40" v="白小框：最小單元"/>
<c id="p4_lg3" st="f=#f8cecc;s=#b85450;fs=14" g="540,1710,240,40" v="紅底紅粗框：啟動器（主機側薄殼）"/>
<c id="p4_lg4" st="f=#f5f5f5;s=light-dark(#000000,#9577A3);fs=14" g="800,1710,150,40" v="淺灰底：主機分組"/>
<c id="p4_lg5" st="f=#d5e8d4;s=light-dark(#000000,#9577A3);fs=14" g="970,1710,160,40" v="綠底：專案目錄分組"/>
<c id="p4_lgt" st="text;s=none;f=none" g="1150,1700,300,60" v="實線 = 資料流（線上文字 = 傳什麼）&lt;br&gt;雙箭頭 = 讀寫／來回都有；黃橢圓 = 使用者；載入／執行順序與判斷見流程頁"/>
<c id="p4_lg6" st="f=#ffe6cc;s=#d79b00;fs=14" g="40,1776,190,40" v="淺橘底：規則／摘要（已定）"/>
<c id="p4_lg7" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="250,1776,120,40" v="綠框：進 git"/>
<c id="p4_lg8" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14;dashed=1;s=#999999;fc=#333333" g="390,1776,200,40" v="灰虛線：不進 git（可重建）"/>
<c id="p4_lg9" st="f=#FFF4C3;s=light-dark(#000000,#9577A3);fs=14;s=#82b366" g="610,1776,230,40" v="黃底綠框：使用者的檔（進 git）"/>
<c id="p4_lg10" st="f=#ffffff;s=#999999" g="860,1776,170,40" v="等寬字：檔案內容範例"/>
<c id="p4_lg11" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="1050,1776,200,40" v="右上角綠標籤：v2 改"/>
<c id="p4_lg11_v2" st="f=#00b050;s=#00b050;fc=#ffffff;fs=9;b=1" g="1218,1778,30,20" v="v2"/>
<c id="p4_lg12" st="f=none;s=#666666;dashed=1" g="40,1842,200,40" v="點線框：init／merge 共用箭頭"/>
<c id="p4_lg13" st="f=#ffffff;s=light-dark(#000000,#9577A3);fs=14" g="260,1842,300,40" v="白底黑框：主機上的目錄／命名空間（不是檔）"/>
<c id="p4_lg14" st="shape=note;f=#ffffff;s=#999999" g="580,1842,220,40" v="便條：說明（含「本頁無待拍板」）"/>
<c id="p4_th" st="text;fs=13;s=none;f=none;b=1" g="40,1898,300,28" v="本頁名詞（只列本頁用到的）"/>
<c id="p4_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1932,150,40" v="引擎"/>
<c id="p4_tv0" st="f=#ffffff;s=#999999" g="190,1932,610,40" v="vendor_kit 的程式本體：只以 image 存在（公開、多架構）、只在容器內跑；8 個模組見紫色容器；一個專案用 version.toml 正規行那一版（version.local.toml 可覆寫成本機 image）"/>
<c id="p4_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1972,150,55" v="啟動器"/>
<c id="p4_tv1" st="f=#ffffff;s=#999999" g="190,1972,610,55" v=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框"/>
<c id="p4_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2027,150,40" v="模組／最小單元"/>
<c id="p4_tv2" st="f=#ffffff;s=#999999" g="190,2027,610,40" v="模組 = 引擎裡一塊獨立責任的程式（紅框）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）"/>
<c id="p4_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2067,150,40" v="cli"/>
<c id="p4_tv3" st="f=#ffffff;s=#999999" g="190,2067,610,40" v="引擎的入口模組：解析子命令與參數（含 --protocol P）、負責所有詢問（-y 免問；無 tty → 1）、決定結束碼 0／1／2／3，並呼叫其他模組"/>
<c id="p4_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2107,150,40" v="version"/>
<c id="p4_tv4" st="f=#ffffff;s=#999999" g="190,2107,610,40" v="讀寫 version.toml／version.local.toml（schema 轉換）；apply 拿 flock；產生／重驗輸入指紋；寫 metadata [progress]；算 docker 資源 label（prune 用）"/>
<c id="p4_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2147,150,40" v="registry"/>
<c id="p4_tv5" st="f=#ffffff;s=#999999" g="190,2147,610,40" v="查 GHCR 的 tag 與 index digest（update／add／upgrade 用；私有 registry 用 TOKEN／TOKEN_FILE；查詢有逾時）；sync 不查最新版，只拉鎖定版"/>
<c id="p4_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2187,150,40" v="materialize"/>
<c id="p4_tv6" st="f=#ffffff;s=#999999" g="190,2187,610,40" v="引擎內部步驟（不對外）：把主機掛進來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/、寫印記 gen/&amp;lt;repo&amp;gt;.stamp、verify sha256；在 apply 決定套用之後才做"/>
<c id="p4_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2227,150,40" v="init／merge"/>
<c id="p4_tv7" st="f=#ffffff;s=#999999" g="190,2227,610,40" v="init 建初始檔、append 幾行或問「要建 X 嗎」；merge 在 upgrade 時對每個檔跑狀態機（D==B → 問後換、三者皆異 → 問後三方合併）+ git merge-file；兩者都把檔案清單與逐檔決定交給 baseline"/>
<c id="p4_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2267,150,40" v="baseline（模組）"/>
<c id="p4_tv8" st="f=#ffffff;s=#999999" g="190,2267,610,40" v="維護 baseline/&amp;lt;repo&amp;gt;/ 範本副本與 .vendor_kit.toml metadata（complete、五態、declined_hash、lines、conflicts、[progress]）"/>
<c id="p4_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1932,150,55" v="launcher-gen"/>
<c id="p4_tv9" st="f=#ffffff;s=#999999" g="990,1932,610,55" v="產生 .vendor_kit/ 自有薄殼四檔（含自描述首行）、gen/tools.just（mod? 行）、gen/.stamp、根 justfile 那一行（新檔時四行）、根 .dockerignore 三行；薄殼與 gen/.stamp 只由 install／upgrade vendor_kit 重產（先比首行 hash）；tools.just 由 sync／add／remove／upgrade 重生"/>
<c id="p4_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1987,150,40" v="多架構 index／index digest"/>
<c id="p4_tv10" st="f=#ffffff;s=#999999" g="990,1987,610,40" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）"/>
<c id="p4_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2027,150,40" v="暫存目錄 &amp;lt;tmp&amp;gt;"/>
<c id="p4_tv11" st="f=#ffffff;s=#999999" g="990,2027,610,40" v="啟動器把工具 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;/，再唯讀掛進引擎當 /dist/&amp;lt;repo&amp;gt;（逐檔判斷讀這裡，不是 cache）；dev 時改掛 &amp;lt;dir&amp;gt;/dist；trap 清掉"/>
<c id="p4_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2067,150,40" v="掛載（-v）"/>
<c id="p4_tv12" st="f=#ffffff;s=#999999" g="990,2067,610,40" v="docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/&amp;lt;repo&amp;gt; = dev 覆寫的 &amp;lt;dir&amp;gt;/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）"/>
<c id="p4_tk13" st="f=#ffffff;s=#999999;b=1" g="840,2107,150,40" v="resolve／apply"/>
<c id="p4_tv13" st="f=#ffffff;s=#999999" g="990,2107,610,40" v="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④"/>
<c id="p4_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2147,150,55" v="frozen（CI 為真）"/>
<c id="p4_tv14" st="f=#ffffff;s=#999999" g="990,2147,610,55" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"/>
<c id="p4_tk15" st="f=#ffffff;s=#999999;b=1" g="840,2202,150,40" v="CI／runner"/>
<c id="p4_tv15" st="f=#ffffff;s=#999999" g="990,2202,610,40" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）"/>
<c id="p4_tk16" st="f=#ffffff;s=#999999;b=1" g="840,2242,150,55" v="docker image inspect"/>
<c id="p4_tv16" st="f=#ffffff;s=#999999" g="990,2242,610,55" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）"/>
</page>
<page name="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install（§2／§3、v2.2 B／C、Q17／Q18、v2.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,108" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,128,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,128,460,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="760,128,260,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1040,128,180,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,128,360,28" v="專案目錄"/>
<c id="bA" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,172,1600,1493" v="5a bootstrap.sh 前半：檢查 git／just → 決定引擎 ref（Q18：不退回內嵌）→ --local 三分支（檔案先驗存在；既是檔又是 tag → 1 + 6-37；只有 tar 形讀 .digest，v2.9 §1）→ inspect → 無才 pull → install（失敗即中止）；後半見「bootstrap.sh（2）」頁"/>
<c id="bA_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="a0" parent="bA" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,58" v="執行 bootstrap.sh -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]…"/>
<c id="a2" parent="bA" st="ellipse;f=#ffe6cc;s=#000000" g="20,126,220,58" v="1：請先 git init（不代做）"/>
<c id="a1" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="390,114,200,81" v="是 git repo？"/>
<c id="a4" parent="bA" st="ellipse;f=#ffe6cc;s=#000000" g="20,226,220,58" v="1：印 just 下載＋安裝指令"/>
<c id="a3" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="390,215,200,81" v="just ≥ 1.33.0？"/>
<c id="a1v" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="370,316,240,81" v="專案已有 version.toml？"/>
<c id="a1v_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="586,306,30,20" v="v2"/>
<c id="a1r" parent="bA" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,317,360,79" v="Q18（v2.4 §5）：舊 bootstrap.sh 在已裝過的 repo 再跑 → 用 version.toml 第一行的引擎跑 install（不降版、不用內嵌）；該引擎拉不到 → 1 失敗，不得退回內嵌；只有第一次接入才用內嵌 ref"/>
<c id="a1r_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,307,30,20" v="v2"/>
<c id="a1vy" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,417,200,63" v="是：引擎 ref = version.toml 第一行（拉不到 → 1，不退回內嵌）"/>
<c id="a1vy_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="436,407,30,20" v="v2"/>
<c id="a1vn" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="520,424,200,48" v="否：引擎 ref = 內嵌引擎 ref（第一次接入）"/>
<c id="a1vn_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,414,30,20" v="v2"/>
<c id="a5" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="420,500,140,81" v="--local？"/>
<c id="a8q" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="260,601,230,81" v="是：值含 / 或以 .tar 結尾？"/>
<c id="a8q_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,591,30,20" v="v2"/>
<c id="a6i" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="540,618,180,48" v="否：docker image inspect &amp;lt;引擎 ref&amp;gt;"/>
<c id="a6i_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,608,30,20" v="v2"/>
<c id="a8ex" parent="bA" st="ellipse;f=#ffe6cc;s=#000000" g="20,702,220,80" v="否 → 1：--local 指定的檔案不存在（請檢查路徑）"/>
<c id="a8ex_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,692,30,20" v="v2"/>
<c id="a8e" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="260,717,230,50" v="是：該檔案存在？"/>
<c id="a8e_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,707,30,20" v="v2"/>
<c id="a6q" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="540,717,160,50" v="本機有？"/>
<c id="a6q_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,707,30,20" v="v2"/>
<c id="a8tx" parent="bA" st="ellipse;f=#ffe6cc;s=#000000" g="20,802,220,102" v="是 → 1：印 6-37（值既是既存檔案也可解讀為本機 image tag，請消歧）"/>
<c id="a8tx_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,792,30,20" v="v2"/>
<c id="a8t" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="260,812,230,81" v="是：本機也有同名 image tag？"/>
<c id="a8t_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,802,30,20" v="v2"/>
<c id="a6p" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="550,829,170,48" v="無：docker pull &amp;lt;引擎 ref&amp;gt;"/>
<c id="a6p_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,819,30,20" v="v2"/>
<c id="a7" parent="bA" st="f=#e1d5e7;s=#9673a6" g="1019,824,182,57" v="ghcr.io/…/vendor_kit:vN&lt;br&gt;（引擎 image；多架構 amd64+arm64）"/>
<c id="a8l" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,924,230,40" v="否：docker load &amp;lt;tar&amp;gt;"/>
<c id="a8l_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,914,30,20" v="v2"/>
<c id="a8d" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,984,230,48" v="tar 形才讀同名 .digest 旁檔 = 正式 index digest（旁檔缺 → 1）"/>
<c id="a8d_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,974,30,20" v="v2"/>
<c id="a8i" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1052,230,63" v="docker image inspect 取 image ID（tag 形 = 值即本機 image tag，不讀 .digest）"/>
<c id="a8i_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="466,1042,30,20" v="v2"/>
<c id="a9" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,1206,300,48" v="docker run &amp;lt;引擎&amp;gt; install（-y 轉發；本機 image 直接 run）"/>
<c id="a9_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="616,1196,30,20" v="v2"/>
<c id="a9e" parent="bA" st="f=#dae8fc;s=#6c8ebf" g="740,1201,260,57" v="install（見「install（1）（2）」頁）：建／重寫 .vendor_kit/ 薄殼、根 justfile、根 .dockerignore"/>
<c id="a9f" parent="bA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,1135,360,189" v="install 寫（見「install（1）（2）」頁）"/>
<c id="a9f_0" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,169,42" v=".vendor_kit/ 薄殼四檔（首行自描述）"/>
<c id="a9f_1" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="183,26,169,42" v="version.toml 第一行（引擎 ref）"/>
<c id="a9f_2" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,169,26" v="gen/.stamp（引擎 ref）"/>
<c id="a9f_3" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="183,74,169,26" v="baseline/.gitkeep"/>
<c id="a9f_4" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,106,169,73" v="根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）"/>
<c id="a9f_5" parent="a9f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="183,106,169,73" v="根 .dockerignore 三行（有 → 問後加）"/>
<c id="a9x" parent="bA" st="ellipse;f=#f8cecc;s=#000000" g="20,1344,220,80" v="是 → 1：中止（第一次不留半成品；--local 檔未寫）"/>
<c id="a9x_v2" parent="bA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1334,30,20" v="v2"/>
<c id="a9q" parent="bA" st="rhombus;f=#FFF4C3;s=#000000" g="390,1344,200,81" v="install 失敗？"/>
<c id="a9z" parent="bA" st="text;s=none;f=none;b=1" g="260,1445,460,42" v="否 ↓ 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add → 彙總"/>
<c id="ae1" edge source="a0" target="a1" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="150,276;510,276"/>
<c id="ae2" edge source="a1" target="a2" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ae3" edge source="a1" target="a3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ae4" edge source="a3" target="a4" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ae5" edge source="a3" target="a1v" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ae5y" edge source="a1v" target="a1vy" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="510,579;380,579" v="是"/>
<c id="ae5n" edge source="a1v" target="a1vn" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.05,0,," pts="510,579;640,579" v="否"/>
<c id="ae5a" edge source="a1vy" target="a5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="380,662;510,662"/>
<c id="ae5b" edge source="a1vn" target="a5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.05,0,," pts="640,662;510,662"/>
<c id="ae6" edge source="a5" target="a8q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="510,763;395,763" v="是"/>
<c id="ae7" edge source="a5" target="a6i" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.09,0,," pts="510,763;650,763" v="否"/>
<c id="ae8" edge source="a8q" target="a8e" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ae8n" edge source="a8q" target="a8i" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.89,0,," pts="522,814;522,1214;464,1214" v="否"/>
<c id="ae8e" edge source="a8e" target="a8ex" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ae8ey" edge source="a8e" target="a8t" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ae8t" edge source="a8t" target="a8tx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ae8tn" edge source="a8t" target="a8l" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ae9" edge source="a8l" target="a8d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae9d" edge source="a8d" target="a8i" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6q" edge source="a6i" target="a6q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6p" edge source="a6q" target="a6p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="無"/>
<c id="ae10" edge source="a7" target="a6p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="ae6y" edge source="a6q" target="a9" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="545,914" v="有"/>
<c id="ae11" edge source="a8i" target="a9" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.34,0,," pts="395,1297;510,1297"/>
<c id="ae11b" edge source="a6p" target="a9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae12" edge source="a9" target="a9e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae12f" edge source="a9e" target="a9f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ae13" edge source="a9" target="a9q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae14" edge source="a9q" target="a9x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ae15" edge source="a9q" target="a9z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="p5_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1681,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1681,140,64" v="黃：判斷"/>
<c id="p5_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1689,140,44" v="綠：起點／終點"/>
<c id="p5_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1683,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1683,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1691,88,40" v="白：步驟"/>
<c id="p5_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1691,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5_lgt" st="text;s=none;f=none" g="1318,1681,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1749,120,36" v="便條：補充說明"/>
<c id="p5_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1749,150,36" v="橘框：規則（已定）"/>
<c id="p5_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1749,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1749,170,36" v="紫：image（引擎與工具）"/>
<c id="p5_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1749,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1749,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1739,30,20" v="v2"/>
<c id="p5_th" st="text;fs=13;s=none;f=none;b=1" g="40,1787,200,28" v="本頁名詞"/>
<c id="p5_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1821,150,71" v="bootstrap.sh"/>
<c id="p5_tv0" st="f=#ffffff;s=#999999" g="190,1821,610,71" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install"/>
<c id="p5_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1892,150,55" v="release／tar／.digest／docker load"/>
<c id="p5_tv1" st="f=#ffffff;s=#999999" g="190,1892,610,55" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker"/>
<c id="p5_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1947,150,71" v="--local &amp;lt;image tag 或 tar&amp;gt;"/>
<c id="p5_tv2" st="f=#ffffff;s=#999999" g="190,1947,610,71" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID"/>
<c id="p5_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2018,150,40" v="GHCR／image／引擎 ref"/>
<c id="p5_tv3" st="f=#ffffff;s=#999999" g="190,2018,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）"/>
<c id="p5_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2058,150,71" v="docker image inspect／image ID"/>
<c id="p5_tv4" st="f=#ffffff;s=#999999" g="190,2058,610,71" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p5_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2129,150,55" v="install／uninstall"/>
<c id="p5_tv5" st="f=#ffffff;s=#999999" g="190,2129,610,55" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"/>
<c id="p5_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2184,150,40" v="冪等"/>
<c id="p5_tv6" st="f=#ffffff;s=#999999" g="190,2184,610,40" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）"/>
<c id="p5_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2224,150,55" v="薄殼 .vendor_kit/"/>
<c id="p5_tv7" st="f=#ffffff;s=#999999" g="190,2224,610,55" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p5_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2279,150,55" v="薄殼首行自描述（Q17）"/>
<c id="p5_tv8" st="f=#ffffff;s=#999999" g="190,2279,610,55" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）"/>
<c id="p5_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1821,150,40" v="gen/.stamp"/>
<c id="p5_tv9" st="f=#ffffff;s=#999999" g="990,1821,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"/>
<c id="p5_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1861,150,40" v="暫存目錄／原子替換"/>
<c id="p5_tv10" st="f=#ffffff;s=#999999" g="990,1861,610,40" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）"/>
<c id="p5_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1901,150,55" v="version.toml／version.local.toml"/>
<c id="p5_tv11" st="f=#ffffff;s=#999999" g="990,1901,610,55" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫"/>
<c id="p5_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1956,150,40" v="resolve／apply"/>
<c id="p5_tv12" st="f=#ffffff;s=#999999" g="990,1956,610,40" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"/>
<c id="p5_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1996,150,55" v="baseline／metadata"/>
<c id="p5_tv13" st="f=#ffffff;s=#999999" g="990,1996,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建"/>
<c id="p5_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2051,150,55" v="just／recipe／import／default"/>
<c id="p5_tv14" st="f=#ffffff;s=#999999" g="990,2051,610,55" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）"/>
<c id="p5_tk15" st="f=#ffffff;s=#999999;b=1" g="840,2106,150,40" v="docker pull／run"/>
<c id="p5_tv15" st="f=#ffffff;s=#999999" g="990,2106,610,40" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台"/>
<c id="p5_tk16" st="f=#ffffff;s=#999999;b=1" g="840,2146,150,40" v="flock／-y"/>
<c id="p5_tv16" st="f=#ffffff;s=#999999" g="990,2146,610,40" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）"/>
<c id="p5_tk17" st="f=#ffffff;s=#999999;b=1" g="840,2186,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5_tv17" st="f=#ffffff;s=#999999" g="990,2186,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add → 彙總（§2、v2.2 C、v2.5 §8、v2.6 Q26／Q27）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,108" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,128,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,128,460,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="760,128,260,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1040,128,180,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,128,360,28" v="專案目錄"/>
<c id="bA2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,172,1600,1025" v="5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add（resolve → docker → apply；一個失敗即中止）→ 彙總結束碼；不自刪"/>
<c id="bA2_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="a9e2" parent="bA2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="340,36,300,102" v="來自「bootstrap.sh（1）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫）"/>
<c id="a8q2" parent="bA2" st="rhombus;f=#FFF4C3;s=#000000" g="410,158,160,50" v="--local？"/>
<c id="a8q2_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="546,148,30,20" v="v2"/>
<c id="a8b" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="520,228,200,79" v="是：寫 version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋vendor_kit_image_id（install 成功後才寫）"/>
<c id="a8b_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,218,30,20" v="v2"/>
<c id="a8f" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,246,360,42" v="＋version.local.toml（不進 git；引擎覆寫：image tag + image ID；離線包 Q26）"/>
<c id="a10" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,327,300,40" v="呼叫 add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y 轉發）"/>
<c id="a10r" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,388,300,40" v="docker run &amp;lt;引擎&amp;gt; resolve add &amp;lt;repo&amp;gt;"/>
<c id="a10r_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="616,378,30,20" v="v2"/>
<c id="a10re" parent="bA2" st="f=#dae8fc;s=#6c8ebf" g="740,387,260,42" v="resolve add（不寫任何檔；見「add（1）」頁）"/>
<c id="a10d" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,449,300,48" v="啟動器 docker 段：拉工具 image、展開 /dist 到暫存（步驟見「add（1）」頁）"/>
<c id="a10d_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="616,439,30,20" v="v2"/>
<c id="a10g" parent="bA2" st="f=#e1d5e7;s=#9673a6" g="1020,452,180,42" v="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（工具 image）"/>
<c id="a10a" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,608,300,40" v="docker run &amp;lt;引擎&amp;gt; apply add &amp;lt;repo&amp;gt;"/>
<c id="a10a_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="616,598,30,20" v="v2"/>
<c id="a10ae" parent="bA2" st="f=#dae8fc;s=#6c8ebf" g="740,607,260,42" v="apply add（拿鎖、重驗、建日誌後寫入；見「add（2）」頁）"/>
<c id="a10f" parent="bA2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,517,360,222" v="add 寫（每個工具；見「add（2）」頁）"/>
<c id="a10f_0" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,344,26" v="version.toml [tools] 行"/>
<c id="a10f_1" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,344,26" v="cache/&amp;lt;repo&amp;gt;/"/>
<c id="a10f_2" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,90,344,26" v="gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="a10f_3" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,122,344,26" v="初始檔（init.toml 的 dest）"/>
<c id="a10f_4" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,154,344,26" v="baseline/&amp;lt;repo&amp;gt;/ + .vendor_kit.toml"/>
<c id="a10f_5" parent="a10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,186,344,26" v="gen/tools.just（重生，mod? 行）"/>
<c id="a10q" parent="bA2" st="rhombus;f=#FFF4C3;s=#000000" g="390,759,200,81" v="還有下一個 -t？"/>
<c id="a10q_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="566,749,30,20" v="v2"/>
<c id="a12" parent="bA2" st="ellipse;f=#f8cecc;s=#000000" g="20,860,220,80" v="是 → 1：明列已完成／未完成（多工具彙總：1 &amp;gt; 2 &amp;gt; 0）"/>
<c id="a12_v2" parent="bA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,850,30,20" v="v2"/>
<c id="a11" parent="bA2" st="rhombus;f=#FFF4C3;s=#000000" g="390,860,200,81" v="任一 add 失敗？"/>
<c id="a13" parent="bA2" st="ellipse;f=#d5e8d4;s=#000000" g="20,961,220,58" v="0：印摘要與要 git add 的清單"/>
<c id="ae16" edge source="a9e2" target="a8q2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae17" edge source="a8q2" target="a8b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="510,390;640,390" v="是"/>
<c id="ae17f" edge source="a8b" target="a8f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ae17n" edge source="a8q2" target="a10" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.34,0,," pts="380,355" v="否"/>
<c id="ae18" edge source="a8b" target="a10" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="640,489;510,489"/>
<c id="ae19" edge source="a10" target="a10r" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae19e" edge source="a10r" target="a10re" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae20" edge source="a10r" target="a10d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae20g" edge source="a10g" target="a10d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="ae21" edge source="a10d" target="a10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae21e" edge source="a10a" target="a10ae" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae21f" edge source="a10ae" target="a10f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ae22" edge source="a10a" target="a10q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae22y" edge source="a10q" target="a10" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.67,0,," pts="330,972;330,519" v="是：下一個 -t"/>
<c id="ae22n" edge source="a10q" target="a11" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ae23" edge source="a11" target="a12" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ae24" edge source="a11" target="a13" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.84,0,," pts="510,1162" v="否"/>
<c id="p5d_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1213,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5d_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1213,140,64" v="黃：判斷"/>
<c id="p5d_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1221,140,44" v="綠：起點／終點"/>
<c id="p5d_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1215,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5d_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1215,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5d_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1223,88,40" v="白：步驟"/>
<c id="p5d_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1223,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5d_lgt" st="text;s=none;f=none" g="1318,1213,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5d_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1281,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p5d_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1281,120,36" v="便條：補充說明"/>
<c id="p5d_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1281,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5d_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1281,170,36" v="紫：image（引擎與工具）"/>
<c id="p5d_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1281,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5d_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1281,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5d_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1271,30,20" v="v2"/>
<c id="p5d_th" st="text;fs=13;s=none;f=none;b=1" g="40,1319,200,28" v="本頁名詞"/>
<c id="p5d_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1353,150,71" v="bootstrap.sh"/>
<c id="p5d_tv0" st="f=#ffffff;s=#999999" g="190,1353,610,71" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install"/>
<c id="p5d_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1424,150,55" v="release／tar／.digest／docker load"/>
<c id="p5d_tv1" st="f=#ffffff;s=#999999" g="190,1424,610,55" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker"/>
<c id="p5d_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1479,150,71" v="--local &amp;lt;image tag 或 tar&amp;gt;"/>
<c id="p5d_tv2" st="f=#ffffff;s=#999999" g="190,1479,610,71" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID"/>
<c id="p5d_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1550,150,40" v="GHCR／image／引擎 ref"/>
<c id="p5d_tv3" st="f=#ffffff;s=#999999" g="190,1550,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）"/>
<c id="p5d_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1590,150,71" v="docker image inspect／image ID"/>
<c id="p5d_tv4" st="f=#ffffff;s=#999999" g="190,1590,610,71" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p5d_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1661,150,55" v="install／uninstall"/>
<c id="p5d_tv5" st="f=#ffffff;s=#999999" g="190,1661,610,55" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"/>
<c id="p5d_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1716,150,40" v="冪等"/>
<c id="p5d_tv6" st="f=#ffffff;s=#999999" g="190,1716,610,40" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）"/>
<c id="p5d_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1756,150,55" v="薄殼 .vendor_kit/"/>
<c id="p5d_tv7" st="f=#ffffff;s=#999999" g="190,1756,610,55" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p5d_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1811,150,55" v="薄殼首行自描述（Q17）"/>
<c id="p5d_tv8" st="f=#ffffff;s=#999999" g="190,1811,610,55" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）"/>
<c id="p5d_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1353,150,40" v="gen/.stamp"/>
<c id="p5d_tv9" st="f=#ffffff;s=#999999" g="990,1353,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"/>
<c id="p5d_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1393,150,40" v="暫存目錄／原子替換"/>
<c id="p5d_tv10" st="f=#ffffff;s=#999999" g="990,1393,610,40" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）"/>
<c id="p5d_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1433,150,55" v="version.toml／version.local.toml"/>
<c id="p5d_tv11" st="f=#ffffff;s=#999999" g="990,1433,610,55" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫"/>
<c id="p5d_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1488,150,40" v="resolve／apply"/>
<c id="p5d_tv12" st="f=#ffffff;s=#999999" g="990,1488,610,40" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"/>
<c id="p5d_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1528,150,55" v="baseline／metadata"/>
<c id="p5d_tv13" st="f=#ffffff;s=#999999" g="990,1528,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建"/>
<c id="p5d_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1583,150,55" v="just／recipe／import／default"/>
<c id="p5d_tv14" st="f=#ffffff;s=#999999" g="990,1583,610,55" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）"/>
<c id="p5d_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1638,150,40" v="docker pull／run"/>
<c id="p5d_tv15" st="f=#ffffff;s=#999999" g="990,1638,610,40" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台"/>
<c id="p5d_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1678,150,40" v="flock／-y"/>
<c id="p5d_tv16" st="f=#ffffff;s=#999999" g="990,1678,610,40" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）"/>
<c id="p5d_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1718,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5d_tv17" st="f=#ffffff;s=#999999" g="990,1718,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：install（1）薄殼">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：install ── 專案層動詞（§2／§3、v2.2 A／C、v2.4 Q17／Q20、v2.5 §8、v2.6 §4／§11／Q22 補）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,108" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,128,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,128,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,128,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,128,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,128,360,28" v="專案目錄"/>
<c id="bI" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,172,1600,1417" v="5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.&amp;lt;id&amp;gt;.toml（v2.8 §2）；禁止巢狀（Q20）"/>
<c id="bI_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="i0" parent="bI" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="just vendor_kit install（-y、--no-justfile）"/>
<c id="i1" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,55,280,42" v="docker run &amp;lt;引擎&amp;gt; install …&lt;br&gt;（啟動器不鎖；鎖在引擎）"/>
<c id="i3" parent="bI" st="ellipse;f=#ffe6cc;s=#000000" g="20,136,220,58" v="1：請先 git init（不代做）"/>
<c id="i2" parent="bI" st="rhombus;f=#FFF4C3;s=#000000" g="560,140,220,50" v="是 git repo？"/>
<c id="i2x" parent="bI" st="ellipse;f=#ffe6cc;s=#000000" g="20,219,220,102" v="是 → 1：&amp;lt;dir&amp;gt; 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall"/>
<c id="i2x_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,209,30,20" v="v2"/>
<c id="i2n" parent="bI" st="rhombus;f=#FFF4C3;s=#000000" g="560,214,300,112" v="上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）"/>
<c id="i2n_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,204,30,20" v="v2"/>
<c id="i4a" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,346,400,40" v="否：flock 專案目錄（60 秒）"/>
<c id="i4a_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,336,30,20" v="v2"/>
<c id="i4" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,438,400,40" v="產 .gitignore 到暫存（首行自描述）"/>
<c id="i4_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,428,30,20" v="v2"/>
<c id="i4n" parent="bI" st="shape=note;f=#ffffff;s=#999999" g="1220,406,360,104" v="第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫到正式位置的檔，專案不留任何檔 → 1（「不留半成品」只對第一次成立，v2.2 C）；修復型 install：建 .vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾（install（2））後刪（v2.8 §2）"/>
<c id="i4_2" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,530,400,40" v="產 entry.just 到暫存（首行自描述）"/>
<c id="i4_2_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,520,30,20" v="v2"/>
<c id="i4_3" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,590,400,40" v="產 vendor.just 到暫存（首行自描述）"/>
<c id="i4_3_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,580,30,20" v="v2"/>
<c id="i4_4" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,650,400,40" v="產 ci/check.sh 到暫存（自描述在第二行）"/>
<c id="i4_4_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,640,30,20" v="v2"/>
<c id="i4e" parent="bI" st="rhombus;f=#FFF4C3;s=#000000" g="560,710,240,50" v="薄殼已存在？"/>
<c id="i4e_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,700,30,20" v="v2"/>
<c id="i4en" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="830,711,130,48" v="否：第一次 = 全新建"/>
<c id="i4en_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,701,30,20" v="v2"/>
<c id="i4x" parent="bI" st="ellipse;f=#ffe6cc;s=#000000" g="20,796,220,80" v="否 → 1：被改過，列差異不動（git checkout 還原後再跑）"/>
<c id="i4x_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,786,30,20" v="v2"/>
<c id="i4q" parent="bI" st="rhombus;f=#FFF4C3;s=#000000" g="560,780,240,112" v="薄殼 == 上次產物？（首行自描述 hash）"/>
<c id="i4q_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,770,30,20" v="v2"/>
<c id="i4qn" parent="bI" st="shape=note;f=#ffffff;s=#999999" g="1220,796,360,79" v="自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）"/>
<c id="i4qn_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,786,30,20" v="v2"/>
<c id="i4l" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,912,240,63" v="是（修復型）：建進度日誌 .tmp.install.&amp;lt;id&amp;gt;.toml（第一個寫入前）"/>
<c id="i4l_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,902,30,20" v="v2"/>
<c id="i4lf" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,912,360,63" v="＋.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）"/>
<c id="i4lf_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,902,30,20" v="v2"/>
<c id="i4b" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,1054,400,40" v="薄殼四檔逐檔原子替換（暫存 → 正式位置）"/>
<c id="i4b_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1044,30,20" v="v2"/>
<c id="i4f" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,995,360,158" v="＋薄殼四檔（進 git）"/>
<c id="i4f_0" parent="i4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,344,26" v=".vendor_kit/.gitignore"/>
<c id="i4f_1" parent="i4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,344,26" v=".vendor_kit/entry.just"/>
<c id="i4f_2" parent="i4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,90,344,26" v=".vendor_kit/vendor.just"/>
<c id="i4f_3" parent="i4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,122,344,26" v=".vendor_kit/ci/check.sh"/>
<c id="i4c" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,1173,400,48" v="寫 version.toml：第一行 = 引擎 ref（＋schema、written_by；已有則不動）"/>
<c id="i4c_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1163,30,20" v="v2"/>
<c id="i4cf" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1176,360,42" v="＋version.toml（第一行引擎 ref、schema、written_by；進 git）"/>
<c id="i4d" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,1241,400,40" v="寫 gen/.stamp（只記引擎 ref）"/>
<c id="i4d_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1231,30,20" v="v2"/>
<c id="i4df" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1241,360,40" v="＋gen/.stamp（不進 git）"/>
<c id="i4g" parent="bI" st="f=#dae8fc;s=#6c8ebf" g="560,1301,400,48" v="建 baseline/.gitkeep（git 不追蹤空目錄；metadata 到 add 才建）"/>
<c id="i4g_v2" parent="bI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1291,30,20" v="v2"/>
<c id="i4gf" parent="bI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1305,360,40" v="＋baseline/.gitkeep（進 git）"/>
<c id="i5z" parent="bI" st="text;s=none;f=none;b=1" g="560,1369,300,42" v="↓ 續「install（2）」頁：根 justfile 與根 .dockerignore"/>
<c id="ie1" edge source="i0" target="i1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie2" edge source="i1" target="i2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.05,0,," pts="420,298;690,298"/>
<c id="ie3" edge source="i2" target="i3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ie2n" edge source="i2" target="i2n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.06,0,," pts="690,376;730,376" v="是"/>
<c id="ie2x" edge source="i2n" target="i2x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ie4" edge source="i2n" target="i4a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ie4b" edge source="i4a" target="i4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie4c" edge source="i4" target="i4_2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie4d" edge source="i4_2" target="i4_3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie4e" edge source="i4_3" target="i4_4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie5" edge source="i4_4" target="i4e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie5n" edge source="i4e" target="i4en" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ie5y" edge source="i4e" target="i4q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ie5x" edge source="i4q" target="i4x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ie6" edge source="i4q" target="i4l" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ie6n" edge source="i4en" target="i4b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie6lf" edge source="i4l" target="i4lf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie6ln" edge source="i4l" target="i4b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie6f" edge source="i4b" target="i4f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie6c" edge source="i4b" target="i4c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie6cf" edge source="i4c" target="i4cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie6d" edge source="i4c" target="i4d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie6df" edge source="i4d" target="i4df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie6g" edge source="i4d" target="i4g" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie6gf" edge source="i4g" target="i4gf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie7" edge source="i4g" target="i5z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p5c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1605,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1605,140,64" v="黃：判斷"/>
<c id="p5c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1613,140,44" v="綠：起點／終點"/>
<c id="p5c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1607,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1607,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1615,88,40" v="白：步驟"/>
<c id="p5c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1615,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5c_lgt" st="text;s=none;f=none" g="1318,1605,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1673,120,36" v="便條：補充說明"/>
<c id="p5c_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1673,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1673,170,36" v="紫：image（引擎與工具）"/>
<c id="p5c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1673,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5c_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1673,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5c_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1663,30,20" v="v2"/>
<c id="p5c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1711,200,28" v="本頁名詞"/>
<c id="p5c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1745,150,71" v="bootstrap.sh"/>
<c id="p5c_tv0" st="f=#ffffff;s=#999999" g="190,1745,610,71" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install"/>
<c id="p5c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1816,150,55" v="release／tar／.digest／docker load"/>
<c id="p5c_tv1" st="f=#ffffff;s=#999999" g="190,1816,610,55" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker"/>
<c id="p5c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1871,150,71" v="--local &amp;lt;image tag 或 tar&amp;gt;"/>
<c id="p5c_tv2" st="f=#ffffff;s=#999999" g="190,1871,610,71" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID"/>
<c id="p5c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1942,150,40" v="GHCR／image／引擎 ref"/>
<c id="p5c_tv3" st="f=#ffffff;s=#999999" g="190,1942,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）"/>
<c id="p5c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1982,150,71" v="docker image inspect／image ID"/>
<c id="p5c_tv4" st="f=#ffffff;s=#999999" g="190,1982,610,71" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p5c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2053,150,55" v="install／uninstall"/>
<c id="p5c_tv5" st="f=#ffffff;s=#999999" g="190,2053,610,55" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"/>
<c id="p5c_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2108,150,40" v="冪等"/>
<c id="p5c_tv6" st="f=#ffffff;s=#999999" g="190,2108,610,40" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）"/>
<c id="p5c_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2148,150,55" v="薄殼 .vendor_kit/"/>
<c id="p5c_tv7" st="f=#ffffff;s=#999999" g="190,2148,610,55" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p5c_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2203,150,55" v="薄殼首行自描述（Q17）"/>
<c id="p5c_tv8" st="f=#ffffff;s=#999999" g="190,2203,610,55" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）"/>
<c id="p5c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1745,150,40" v="gen/.stamp"/>
<c id="p5c_tv9" st="f=#ffffff;s=#999999" g="990,1745,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"/>
<c id="p5c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1785,150,40" v="暫存目錄／原子替換"/>
<c id="p5c_tv10" st="f=#ffffff;s=#999999" g="990,1785,610,40" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）"/>
<c id="p5c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1825,150,55" v="version.toml／version.local.toml"/>
<c id="p5c_tv11" st="f=#ffffff;s=#999999" g="990,1825,610,55" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫"/>
<c id="p5c_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1880,150,40" v="resolve／apply"/>
<c id="p5c_tv12" st="f=#ffffff;s=#999999" g="990,1880,610,40" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"/>
<c id="p5c_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1920,150,55" v="baseline／metadata"/>
<c id="p5c_tv13" st="f=#ffffff;s=#999999" g="990,1920,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建"/>
<c id="p5c_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1975,150,55" v="just／recipe／import／default"/>
<c id="p5c_tv14" st="f=#ffffff;s=#999999" g="990,1975,610,55" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）"/>
<c id="p5c_tk15" st="f=#ffffff;s=#999999;b=1" g="840,2030,150,40" v="docker pull／run"/>
<c id="p5c_tv15" st="f=#ffffff;s=#999999" g="990,2030,610,40" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台"/>
<c id="p5c_tk16" st="f=#ffffff;s=#999999;b=1" g="840,2070,150,40" v="flock／-y"/>
<c id="p5c_tv16" st="f=#ffffff;s=#999999" g="990,2070,610,40" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）"/>
<c id="p5c_tk17" st="f=#ffffff;s=#999999;b=1" g="840,2110,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5c_tv17" st="f=#ffffff;s=#999999" g="990,2110,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：install（2）根 justfile 與 .dockerignore">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22 補）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,108" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,128,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,128,140,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="440,128,560,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1020,128,200,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,128,360,28" v="專案目錄"/>
<c id="bI2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,172,1600,1293" v="5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建三行；有 → 問後 append）"/>
<c id="bI2_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="i5e" parent="bI2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="420,70,300,58" v="來自「install（1）」頁：薄殼與 .vendor_kit/ 各檔已寫"/>
<c id="i5" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,148,300,50" v="--no-justfile？"/>
<c id="i5_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,138,30,20" v="v2"/>
<c id="i6" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,224,300,81" v="否 → 有根 justfile？"/>
<c id="i7" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="860,236,120,57" v="無：建 justfile（四行，逐字見右）"/>
<c id="i7f" parent="bI2" st="f=#ffffff;s=#666666;dashed=1" g="1220,218,360,94" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋justfile（新建，逐字四行；recipe 本體以 tab 縮排）&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;br&gt;&lt;br&gt;default:&lt;br&gt;&#9;@just --list&lt;/pre&gt;"/>
<c id="i7f_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,208,30,20" v="v2"/>
<c id="i8" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,332,300,81" v="有 → 已含 import 那行？"/>
<c id="i8_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="696,322,30,20" v="v2"/>
<c id="i12" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,433,300,112" v="否 → 問「要在 justfile 加這一行嗎」同意？（-y 免問）"/>
<c id="i11" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="860,468,120,42" v="是：append 那一行"/>
<c id="i11f" parent="bI2" st="f=#ffffff;s=#666666;dashed=1" g="1220,465,360,48" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;justfile（尾端＋一行）：&lt;br&gt;import &#x27;.vendor_kit/entry.just&#x27;&lt;/pre&gt;"/>
<c id="i11f_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,455,30,20" v="v2"/>
<c id="im" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="360,565,360,42" v="印 justfile 結果（建了／加了一行／跳過／已含不再加／拒絕不動）"/>
<c id="ig" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,627,250,81" v="有根 .dockerignore？"/>
<c id="ig_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,617,30,20" v="v2"/>
<c id="ign" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="700,628,120,79" v="無：建 .dockerignore（三行，逐字見右）"/>
<c id="ign_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="796,618,30,20" v="v2"/>
<c id="ignf" parent="bI2" st="f=#ffffff;s=#666666;dashed=1" g="1220,628,360,79" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋.dockerignore（新建，三行）：&lt;br&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;"/>
<c id="ignf_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,618,30,20" v="v2"/>
<c id="idlx" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,784,220,63" v="否：刪進度日誌 .tmp.install.&amp;lt;id&amp;gt;.toml（修復型才有；最後一步）"/>
<c id="idlx_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,774,30,20" v="v2"/>
<c id="igq" parent="bI2" st="rhombus;f=#FFF4C3;s=#000000" g="420,728,250,174" v="有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）"/>
<c id="igq_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,718,30,20" v="v2"/>
<c id="idlz" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="700,784,120,63" v="刪進度日誌（修復型才有；最後一步）"/>
<c id="idlz_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="796,774,30,20" v="v2"/>
<c id="igx" parent="bI2" st="ellipse;f=#d5e8d4;s=#000000" g="20,922,220,102" v="0：不寫 .dockerignore、印指示（含 justfile 結果）"/>
<c id="igx_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,912,30,20" v="v2"/>
<c id="igz" parent="bI2" st="ellipse;f=#d5e8d4;s=#000000" g="860,764,120,102" v="0：印建立了什麼（含 justfile 結果）"/>
<c id="igz_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="956,754,30,20" v="v2"/>
<c id="igy" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="420,953,250,40" v="是：append 三行"/>
<c id="igy_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,943,30,20" v="v2"/>
<c id="igyf" parent="bI2" st="f=#ffffff;s=#666666;dashed=1" g="1220,934,360,79" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.dockerignore（尾端＋三行；Q22 補）：&lt;br&gt;.vendor_kit/cache/&lt;br&gt;.vendor_kit/gen/&lt;br&gt;.vendor_kit/.tmp.*&lt;/pre&gt;"/>
<c id="igyf_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,924,30,20" v="v2"/>
<c id="igm" parent="bI2" st="f=#dae8fc;s=#6c8ebf" g="420,1044,250,63" v="插入的行記在 baseline/.vendor_kit.toml（lines）"/>
<c id="igm_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,1034,30,20" v="v2"/>
<c id="igmf" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1052,360,48" v="baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）"/>
<c id="igmf_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,1042,30,20" v="v2"/>
<c id="idl" parent="bI2" st="f=#dae8fc;s=#6c8ebf" g="420,1127,250,48" v="刪進度日誌 .tmp.install.&amp;lt;id&amp;gt;.toml（修復型才有；最後一步）"/>
<c id="idl_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,1117,30,20" v="v2"/>
<c id="idlf" parent="bI2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1131,360,40" v="－.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml（修復型才有）"/>
<c id="idlf_v2" parent="bI2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,1121,30,20" v="v2"/>
<c id="iz" parent="bI2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1195,220,58" v="0：印建立／修改了什麼（含加的行）"/>
<c id="ie7" edge source="i5e" target="i5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie8" edge source="i5" target="im" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.83,0,," pts="418,345" v="是"/>
<c id="ie9" edge source="i5" target="i6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ie10" edge source="i6" target="i7" st="es=orthogonalEdgeStyle;s=default;fc=default" v="無"/>
<c id="ie11" edge source="i7" target="i7f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie12" edge source="i6" target="i8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ie13" edge source="i7" target="im" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="940,232;370,232;370,758"/>
<c id="ie13b" edge source="i8" target="im" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.78,0,," pts="432,544" v="是"/>
<c id="ie14" edge source="i8" target="i12" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ie17" edge source="i12" target="i11" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ie18" edge source="i12" target="im" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ie16f" edge source="i11" target="i11f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie19d" edge source="i11" target="im" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.12,0,," pts="940,727;704,727"/>
<c id="ie19" edge source="im" target="ig" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie20" edge source="ig" target="ign" st="es=orthogonalEdgeStyle;s=default;fc=default" v="無"/>
<c id="ie20f" edge source="ign" target="ignf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie21" edge source="ig" target="igq" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ie20z" edge source="ign" target="idlz" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie20zz" edge source="idlz" target="igz" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie22" edge source="igq" target="idlx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ie22x" edge source="idlx" target="igx" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie23" edge source="igq" target="igy" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ie23f" edge source="igy" target="igyf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie23m" edge source="igy" target="igm" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie23mf" edge source="igm" target="igmf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ie24" edge source="igm" target="idl" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ie24f" edge source="idl" target="idlf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="ie25" edge source="idl" target="iz" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.86,0,," pts="565,1396"/>
<c id="p5cc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1481,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5cc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1481,140,64" v="黃：判斷"/>
<c id="p5cc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1489,140,44" v="綠：起點／終點"/>
<c id="p5cc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1483,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5cc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1483,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5cc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1491,88,40" v="白：步驟"/>
<c id="p5cc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1491,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5cc_lgt" st="text;s=none;f=none" g="1318,1481,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5cc_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1549,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p5cc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1549,120,36" v="便條：補充說明"/>
<c id="p5cc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1549,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5cc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1549,170,36" v="紫：image（引擎與工具）"/>
<c id="p5cc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1549,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5cc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1549,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5cc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1539,30,20" v="v2"/>
<c id="p5cc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1587,200,28" v="本頁名詞"/>
<c id="p5cc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1621,150,71" v="bootstrap.sh"/>
<c id="p5cc_tv0" st="f=#ffffff;s=#999999" g="190,1621,610,71" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;] 呼叫 add；再跑 = install"/>
<c id="p5cc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1692,150,55" v="release／tar／.digest／docker load"/>
<c id="p5cc_tv1" st="f=#ffffff;s=#999999" g="190,1692,610,55" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker"/>
<c id="p5cc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1747,150,71" v="--local &amp;lt;image tag 或 tar&amp;gt;"/>
<c id="p5cc_tv2" st="f=#ffffff;s=#999999" g="190,1747,610,71" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID"/>
<c id="p5cc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1818,150,40" v="GHCR／image／引擎 ref"/>
<c id="p5cc_tv3" st="f=#ffffff;s=#999999" g="190,1818,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）"/>
<c id="p5cc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1858,150,71" v="docker image inspect／image ID"/>
<c id="p5cc_tv4" st="f=#ffffff;s=#999999" g="190,1858,610,71" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p5cc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1929,150,55" v="install／uninstall"/>
<c id="p5cc_tv5" st="f=#ffffff;s=#999999" g="190,1929,610,55" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"/>
<c id="p5cc_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1984,150,40" v="冪等"/>
<c id="p5cc_tv6" st="f=#ffffff;s=#999999" g="190,1984,610,40" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）"/>
<c id="p5cc_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2024,150,55" v="薄殼 .vendor_kit/"/>
<c id="p5cc_tv7" st="f=#ffffff;s=#999999" g="190,2024,610,55" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）"/>
<c id="p5cc_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2079,150,55" v="薄殼首行自描述（Q17）"/>
<c id="p5cc_tv8" st="f=#ffffff;s=#999999" g="190,2079,610,55" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 LF 正規化 hash&amp;gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）"/>
<c id="p5cc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1621,150,40" v="gen/.stamp"/>
<c id="p5cc_tv9" st="f=#ffffff;s=#999999" g="990,1621,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"/>
<c id="p5cc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1661,150,40" v="暫存目錄／原子替換"/>
<c id="p5cc_tv10" st="f=#ffffff;s=#999999" g="990,1661,610,40" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）"/>
<c id="p5cc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1701,150,55" v="version.toml／version.local.toml"/>
<c id="p5cc_tv11" st="f=#ffffff;s=#999999" g="990,1701,610,55" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&amp;lt;dir&amp;gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫"/>
<c id="p5cc_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1756,150,40" v="resolve／apply"/>
<c id="p5cc_tv12" st="f=#ffffff;s=#999999" g="990,1756,610,40" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"/>
<c id="p5cc_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1796,150,55" v="baseline／metadata"/>
<c id="p5cc_tv13" st="f=#ffffff;s=#999999" g="990,1796,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建"/>
<c id="p5cc_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1851,150,55" v="just／recipe／import／default"/>
<c id="p5cc_tv14" st="f=#ffffff;s=#999999" g="990,1851,610,55" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）"/>
<c id="p5cc_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1906,150,40" v="docker pull／run"/>
<c id="p5cc_tv15" st="f=#ffffff;s=#999999" g="990,1906,610,40" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台"/>
<c id="p5cc_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1946,150,40" v="flock／-y"/>
<c id="p5cc_tv16" st="f=#ffffff;s=#999999" g="990,1946,610,40" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）"/>
<c id="p5cc_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1986,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5cc_tv17" st="f=#ffffff;s=#999999" g="990,1986,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：add（1）resolve → docker">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：add &amp;lt;repo&amp;gt;（1）resolve → 啟動器 docker（§2／§5、v2.2 C／E、v2.5 §2／§3／§5）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="bB" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1257" v="5b add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（bootstrap.sh 對每個 -t 呼叫；使用者也直接打）= 引擎 resolve（不寫；私有 image 未指定 @&amp;lt;tag&amp;gt; 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；續「add（1′）」「add（2）」頁"/>
<c id="bB_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="c0" parent="bB" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="just vendor_kit add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y、--dry-run…）"/>
<c id="c1" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,44,280,63" v="docker run &amp;lt;引擎&amp;gt; resolve add &amp;lt;repo&amp;gt;（--local：tar 先 docker load，讀同名 .digest）"/>
<c id="c1_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,34,30,20" v="v2"/>
<c id="c2a" parent="bB" st="f=#dae8fc;s=#6c8ebf" g="560,56,400,40" v="resolve（不寫任何檔）：讀 version.toml"/>
<c id="c2a_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,46,30,20" v="v2"/>
<c id="c2b" parent="bB" st="f=#dae8fc;s=#6c8ebf" g="560,140,400,48" v="查 tag（預設最新正式版／@&amp;lt;tag&amp;gt;）與 index digest（--source 改來源）"/>
<c id="c2b_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,130,30,20" v="v2"/>
<c id="c3" parent="bB" st="f=#e1d5e7;s=#9673a6" g="980,136,220,57" v="ghcr.io/&amp;lt;org&amp;gt;/&amp;lt;repo&amp;gt;-dist&lt;br&gt;（工具 image；多架構 index digest）"/>
<c id="c2px" parent="bB" st="ellipse;f=#ffe6cc;s=#000000" g="20,213,220,102" v="是 → 1：印 6-3（私有 image：請指定 @&amp;lt;tag&amp;gt; 或提供 registry 憑證）"/>
<c id="c2px_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,203,30,20" v="v2"/>
<c id="c2pq" parent="bB" st="rhombus;f=#FFF4C3;s=#000000" g="560,224,310,81" v="私有 image 且未指定 @&amp;lt;tag&amp;gt; 且無憑證？"/>
<c id="c2pq_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="846,214,30,20" v="v2"/>
<c id="c4" parent="bB" st="rhombus;f=#FFF4C3;s=#000000" g="560,335,310,50" v="已接入 &amp;lt;repo&amp;gt;？"/>
<c id="c5" parent="bB" st="rhombus;f=#FFF4C3;s=#000000" g="560,405,310,50" v="metadata 有完成標記？"/>
<c id="c6x" parent="bB" st="ellipse;f=#ffe6cc;s=#000000" g="20,486,220,58" v="是 → 1：@&amp;lt;tag&amp;gt; 與鎖定不同，請改用 upgrade"/>
<c id="c6x_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,476,30,20" v="v2"/>
<c id="c5t" parent="bB" st="rhombus;f=#FFF4C3;s=#000000" g="605,475,220,81" v="@&amp;lt;tag&amp;gt; 與鎖定不同？"/>
<c id="c8" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="840,487,120,57" v="否：續作，只做缺的步驟（不補刻意刪的檔）"/>
<c id="c6" parent="bB" st="ellipse;f=#d5e8d4;s=#000000" g="20,576,220,58" v="否 → 0：已接入且完成，無變更"/>
<c id="c2c" parent="bB" st="f=#dae8fc;s=#6c8ebf" g="560,654,400,48" v="resolve 完 → 產生執行計畫（要拉的 image@digest、mount、apply 與否）"/>
<c id="c2c_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,644,30,20" v="v2"/>
<c id="c2d" parent="bB" st="f=#dae8fc;s=#6c8ebf" g="560,722,400,48" v="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 計畫＋指紋以 stdout 回啟動器"/>
<c id="c2d_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,712,30,20" v="v2"/>
<c id="c9a" parent="bB" st="rhombus;f=#FFF4C3;s=#000000" g="260,790,170,143" v="docker image inspect：本機有？"/>
<c id="c9a_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="406,780,30,20" v="v2"/>
<c id="c9p" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="440,953,100,48" v="無：docker pull"/>
<c id="c9p_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,943,30,20" v="v2"/>
<c id="c9g" parent="bB" st="f=#e1d5e7;s=#9673a6" g="980,956,220,42" v="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（鎖定的那一版）"/>
<c id="c9b" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1021,280,40" v="docker create &amp;lt;image&amp;gt; /x"/>
<c id="c9b_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,1011,30,20" v="v2"/>
<c id="c9c" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1081,280,48" v="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）"/>
<c id="c9c_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,1071,30,20" v="v2"/>
<c id="c9d" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1149,280,40" v="docker rm 該容器"/>
<c id="c9d_v2" parent="bB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,1139,30,20" v="v2"/>
<c id="c9z" parent="bB" st="text;s=none;f=none;b=1" g="260,1209,280,42" v="↓ 續「add（1′）」頁：docker run 引擎 apply add → 前置檢查"/>
<c id="cf_l" parent="bB" st="text;s=none;f=none;b=1" g="1220,40,340,26" v="add 前 → 後（專案目錄，一格一檔；＋ = add 新增）"/>
<c id="cf0" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,72,170,365" v="add 前（install 後）"/>
<c id="cf0_0" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,154,42" v="justfile（＋import 行）"/>
<c id="cf0_1" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,154,42" v=".dockerignore（＋三行）"/>
<c id="cf0_2" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,122,154,42" v="version.toml（vendor_kit 行）"/>
<c id="cf0_3" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,170,154,42" v="version.local.toml（--local 時）"/>
<c id="cf0_4" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,218,154,73" v="薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh"/>
<c id="cf0_5" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,297,154,26" v="gen/.stamp"/>
<c id="cf0_6" parent="cf0" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,329,154,26" v="baseline/.gitkeep"/>
<c id="cf1" parent="bB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1410,81,170,347" v="add 後（＋ = 新增）"/>
<c id="cf1_0" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,154,42" v="＋version.toml [tools] &amp;lt;repo&amp;gt; 行"/>
<c id="cf1_1" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,154,57" v="＋cache/&amp;lt;repo&amp;gt;/（不進 git：files/、init.toml、just/）"/>
<c id="cf1_2" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,137,154,26" v="＋gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="cf1_3" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,169,154,57" v="＋初始檔（init.toml 的 dest；append 問後加）"/>
<c id="cf1_4" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,232,154,42" v="＋baseline/&amp;lt;repo&amp;gt;/ + .vendor_kit.toml"/>
<c id="cf1_5" parent="cf1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,280,154,57" v="＋gen/tools.just（每個 &amp;lt;ns&amp;gt;.just 一行 mod?）"/>
<c id="ce1" edge source="c0" target="c1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce2" edge source="c1" target="c2a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce2b" edge source="c2a" target="c2b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce3" edge source="c2b" target="c3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="查"/>
<c id="ce4p" edge source="c2b" target="c2pq" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce4px" edge source="c2pq" target="c2px" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ce4" edge source="c2pq" target="c4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ce5" edge source="c4" target="c5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ce7" edge source="c5" target="c5t" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ce7b" edge source="c5" target="c8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.08,0,," pts="797,606;920,606" v="否"/>
<c id="ce8" edge source="c5t" target="c6x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ce9" edge source="c5t" target="c6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.91,0,," pts="735,746" v="否"/>
<c id="ce10" edge source="c4" target="c2c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.51,0,," pts="990,501;990,785;920,785" v="否"/>
<c id="ce11" edge source="c8" target="c2c" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,656;990,785;920,785"/>
<c id="ce12" edge source="c2c" target="c2d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce12a" edge source="c2d" target="c9a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="780,921;365,921"/>
<c id="ce12n" edge source="c9a" target="c9p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.60,0,," pts="510,1002" v="無"/>
<c id="ce12g" edge source="c9g" target="c9p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="ce12y" edge source="c9a" target="c9b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ce12p" edge source="c9p" target="c9b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce12c" edge source="c9b" target="c9c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce12d" edge source="c9c" target="c9d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce13" edge source="c9d" target="c9z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="cfe" edge source="cf0" target="cf1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p5b_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1414,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5b_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1414,140,64" v="黃：判斷"/>
<c id="p5b_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1422,140,44" v="綠：起點／終點"/>
<c id="p5b_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1416,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5b_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1416,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5b_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1424,88,40" v="白：步驟"/>
<c id="p5b_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1424,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5b_lgt" st="text;s=none;f=none" g="1318,1414,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5b_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1482,120,36" v="便條：補充說明"/>
<c id="p5b_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1482,150,36" v="橘框：規則（已定）"/>
<c id="p5b_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1482,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5b_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1482,170,36" v="紫：image（引擎與工具）"/>
<c id="p5b_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1482,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5b_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1482,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5b_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1472,30,20" v="v2"/>
<c id="p5b_th" st="text;fs=13;s=none;f=none;b=1" g="40,1520,200,28" v="本頁名詞"/>
<c id="p5b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1554,150,71" v="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]"/>
<c id="p5b_tv0" st="f=#ffffff;s=#999999" g="190,1554,610,71" v="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0"/>
<c id="p5b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1625,150,40" v="resolve／apply"/>
<c id="p5b_tv1" st="f=#ffffff;s=#999999" g="190,1625,610,40" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）"/>
<c id="p5b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1665,150,40" v="stdout／stderr"/>
<c id="p5b_tv2" st="f=#ffffff;s=#999999" g="190,1665,610,40" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行"/>
<c id="p5b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1705,150,40" v="輸入指紋"/>
<c id="p5b_tv3" st="f=#ffffff;s=#999999" g="190,1705,610,40" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」"/>
<c id="p5b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1745,150,55" v="GHCR／image／index digest／image inspect"/>
<c id="p5b_tv4" st="f=#ffffff;s=#999999" g="190,1745,610,55" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台"/>
<c id="p5b_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1800,150,55" v="--local／tar／.digest（Q26）"/>
<c id="p5b_tv5" st="f=#ffffff;s=#999999" g="190,1800,610,55" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local"/>
<c id="p5b_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1855,150,40" v="/dist/&amp;lt;repo&amp;gt;（暫存）／N"/>
<c id="p5b_tv6" st="f=#ffffff;s=#999999" g="190,1855,610,40" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）"/>
<c id="p5b_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1895,150,40" v="materialize／印記"/>
<c id="p5b_tv7" st="f=#ffffff;s=#999999" g="190,1895,610,40" v="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）"/>
<c id="p5b_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1935,150,55" v="初始檔／strategy"/>
<c id="p5b_tv8" st="f=#ffffff;s=#999999" g="190,1935,610,55" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）"/>
<c id="p5b_tk9" st="f=#ffffff;s=#999999;b=1" g="40,1990,150,40" v="dest 撞名"/>
<c id="p5b_tv9" st="f=#ffffff;s=#999999" g="190,1990,610,40" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/"/>
<c id="p5b_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1554,150,40" v="命名空間撞名（v2.5 §5）"/>
<c id="p5b_tv10" st="f=#ffffff;s=#999999" g="990,1554,610,40" v="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）"/>
<c id="p5b_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1594,150,71" v="baseline／metadata"/>
<c id="p5b_tv11" st="f=#ffffff;s=#999999" g="990,1594,610,71" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）"/>
<c id="p5b_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1665,150,28" v="續作"/>
<c id="p5b_tv12" st="f=#ffffff;s=#999999" g="990,1665,610,28" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔"/>
<c id="p5b_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1693,150,71" v="gen／mod?／recipe"/>
<c id="p5b_tv13" st="f=#ffffff;s=#999999" g="990,1693,610,71" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe"/>
<c id="p5b_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1764,150,55" v="CI 為真／frozen／dry-run"/>
<c id="p5b_tv14" st="f=#ffffff;s=#999999" g="990,1764,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）"/>
<c id="p5b_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1819,150,28" v="flock"/>
<c id="p5b_tv15" st="f=#ffffff;s=#999999" g="990,1819,610,28" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖"/>
<c id="p5b_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1847,150,28" v="symlink"/>
<c id="p5b_tv16" st="f=#ffffff;s=#999999" g="990,1847,610,28" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕"/>
<c id="p5b_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1875,150,40" v="CRLF"/>
<c id="p5b_tv17" st="f=#ffffff;s=#999999" g="990,1875,610,40" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p5b_tk18" st="f=#ffffff;s=#999999;b=1" g="840,1915,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5b_tv18" st="f=#ffffff;s=#999999" g="990,1915,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：add（1′）apply 前置">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：add &amp;lt;repo&amp;gt;（1′）apply 前置：拿鎖 → 重驗 → 檢查 → frozen → dry-run（v2.2 E、v2.5 §3／§5）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="bB1" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,726" v="5b′ add &amp;lt;repo&amp;gt; 的 apply 前置（承「add（1）」頁：工具 image 已展開到主機暫存）：docker run 引擎 apply → 拿鎖 → 重驗指紋 → dest 合法？→ 命名空間撞名？→ frozen → dry-run 分支；寫入段見「add（2）」頁"/>
<c id="bB1_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="c9e" parent="bB1" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="260,36,280,58" v="來自「add（1）」頁：/dist/&amp;lt;repo&amp;gt; 已在主機暫存"/>
<c id="c10" parent="bB1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,114,280,48" v="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply add &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）"/>
<c id="c10_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,104,30,20" v="v2"/>
<c id="c11a" parent="bB1" st="f=#dae8fc;s=#6c8ebf" g="560,118,400,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="c11a_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,108,30,20" v="v2"/>
<c id="c11b" parent="bB1" st="f=#dae8fc;s=#6c8ebf" g="560,191,240,40" v="重驗 resolve 的輸入指紋"/>
<c id="c11b_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,181,30,20" v="v2"/>
<c id="c11x" parent="bB1" st="ellipse;f=#ffe6cc;s=#000000" g="820,182,140,58" v="不同 → 1「請重跑」"/>
<c id="c11x_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,172,30,20" v="v2"/>
<c id="c12x" parent="bB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,260,220,80" v="否 → 1：dest 不合法（請修 init.toml／dest；需人動作）"/>
<c id="c12x_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,250,30,20" v="v2"/>
<c id="c12" parent="bB1" st="rhombus;f=#FFF4C3;s=#000000" g="560,260,400,81" v="init.toml 的 dest 全部合法？（任何寫入前檢查）"/>
<c id="c12_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,250,30,20" v="v2"/>
<c id="c12r" parent="bB1" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,261,360,79" v="dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/；dist 含 symlink → 拒絕"/>
<c id="c12r_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,251,30,20" v="v2"/>
<c id="c12bx" parent="bB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,377,220,80" v="是 → 1：命名空間撞名（請改名／移除撞名者；需人動作）"/>
<c id="c12bx_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,367,30,20" v="v2"/>
<c id="c12b" parent="bB1" st="rhombus;f=#FFF4C3;s=#000000" g="560,361,400,112" v="just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"/>
<c id="c12b_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,351,30,20" v="v2"/>
<c id="c12br" parent="bB1" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,386,360,63" v="命名空間撞名（v2.5 §5）：&amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）"/>
<c id="c12br_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,376,30,20" v="v2"/>
<c id="c14x" parent="bB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,494,220,80" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）"/>
<c id="c14x_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,484,30,20" v="v2"/>
<c id="c14" parent="bB1" st="rhombus;f=#FFF4C3;s=#000000" g="590,493,340,81" v="CI 為真（frozen）且需改 tracked 檔？"/>
<c id="c14_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="906,483,30,20" v="v2"/>
<c id="c13y" parent="bB1" st="ellipse;f=#d5e8d4;s=#000000" g="20,594,220,80" v="是 → 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/&amp;lt;repo&amp;gt;）"/>
<c id="c13y_v2" parent="bB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,584,30,20" v="v2"/>
<c id="c13" parent="bB1" st="rhombus;f=#FFF4C3;s=#000000" g="640,609,240,50" v="--dry-run？"/>
<c id="c13z" parent="bB1" st="text;s=none;f=none;b=1" g="560,694,300,26" v="否 ↓ 續「add（2）」頁：apply 寫入段"/>
<c id="ce13e" edge source="c9e" target="c10" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce14" edge source="c10" target="c11a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce14b" edge source="c11a" target="c11b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce15" edge source="c11b" target="c11x" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce16" edge source="c11b" target="c12" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce17" edge source="c12" target="c12x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ce18" edge source="c12" target="c12b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ce18x" edge source="c12b" target="c12bx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ce18b" edge source="c12b" target="c14" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ce19" edge source="c14" target="c14x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ce20" edge source="c14" target="c13" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ce21" edge source="c13" target="c13y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ce22" edge source="c13" target="c13z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p5bp_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,883,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5bp_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,883,140,64" v="黃：判斷"/>
<c id="p5bp_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,891,140,44" v="綠：起點／終點"/>
<c id="p5bp_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,885,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5bp_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,885,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5bp_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,893,88,40" v="白：步驟"/>
<c id="p5bp_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,893,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5bp_lgt" st="text;s=none;f=none" g="1318,883,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5bp_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,951,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p5bp_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,951,120,36" v="便條：補充說明"/>
<c id="p5bp_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,951,150,36" v="橘框：規則（已定）"/>
<c id="p5bp_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="570,951,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5bp_lgx_img" st="f=#e1d5e7;s=#9673a6" g="780,951,170,36" v="紫：image（引擎與工具）"/>
<c id="p5bp_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="970,951,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5bp_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1160,951,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5bp_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1336,941,30,20" v="v2"/>
<c id="p5bp_th" st="text;fs=13;s=none;f=none;b=1" g="40,989,200,28" v="本頁名詞"/>
<c id="p5bp_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1023,150,71" v="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]"/>
<c id="p5bp_tv0" st="f=#ffffff;s=#999999" g="190,1023,610,71" v="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0"/>
<c id="p5bp_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1094,150,40" v="resolve／apply"/>
<c id="p5bp_tv1" st="f=#ffffff;s=#999999" g="190,1094,610,40" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）"/>
<c id="p5bp_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1134,150,40" v="stdout／stderr"/>
<c id="p5bp_tv2" st="f=#ffffff;s=#999999" g="190,1134,610,40" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行"/>
<c id="p5bp_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1174,150,40" v="輸入指紋"/>
<c id="p5bp_tv3" st="f=#ffffff;s=#999999" g="190,1174,610,40" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」"/>
<c id="p5bp_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1214,150,55" v="GHCR／image／index digest／image inspect"/>
<c id="p5bp_tv4" st="f=#ffffff;s=#999999" g="190,1214,610,55" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台"/>
<c id="p5bp_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1269,150,55" v="--local／tar／.digest（Q26）"/>
<c id="p5bp_tv5" st="f=#ffffff;s=#999999" g="190,1269,610,55" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local"/>
<c id="p5bp_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1324,150,40" v="/dist/&amp;lt;repo&amp;gt;（暫存）／N"/>
<c id="p5bp_tv6" st="f=#ffffff;s=#999999" g="190,1324,610,40" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）"/>
<c id="p5bp_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1364,150,40" v="materialize／印記"/>
<c id="p5bp_tv7" st="f=#ffffff;s=#999999" g="190,1364,610,40" v="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）"/>
<c id="p5bp_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1404,150,55" v="初始檔／strategy"/>
<c id="p5bp_tv8" st="f=#ffffff;s=#999999" g="190,1404,610,55" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）"/>
<c id="p5bp_tk9" st="f=#ffffff;s=#999999;b=1" g="40,1459,150,40" v="dest 撞名"/>
<c id="p5bp_tv9" st="f=#ffffff;s=#999999" g="190,1459,610,40" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/"/>
<c id="p5bp_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1023,150,40" v="命名空間撞名（v2.5 §5）"/>
<c id="p5bp_tv10" st="f=#ffffff;s=#999999" g="990,1023,610,40" v="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）"/>
<c id="p5bp_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1063,150,71" v="baseline／metadata"/>
<c id="p5bp_tv11" st="f=#ffffff;s=#999999" g="990,1063,610,71" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）"/>
<c id="p5bp_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1134,150,28" v="續作"/>
<c id="p5bp_tv12" st="f=#ffffff;s=#999999" g="990,1134,610,28" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔"/>
<c id="p5bp_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1162,150,71" v="gen／mod?／recipe"/>
<c id="p5bp_tv13" st="f=#ffffff;s=#999999" g="990,1162,610,71" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe"/>
<c id="p5bp_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1233,150,55" v="CI 為真／frozen／dry-run"/>
<c id="p5bp_tv14" st="f=#ffffff;s=#999999" g="990,1233,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）"/>
<c id="p5bp_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1288,150,28" v="flock"/>
<c id="p5bp_tv15" st="f=#ffffff;s=#999999" g="990,1288,610,28" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖"/>
<c id="p5bp_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1316,150,28" v="symlink"/>
<c id="p5bp_tv16" st="f=#ffffff;s=#999999" g="990,1316,610,28" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕"/>
<c id="p5bp_tk17" st="f=#ffffff;s=#999999;b=1" g="840,1344,150,40" v="CRLF"/>
<c id="p5bp_tv17" st="f=#ffffff;s=#999999" g="990,1344,610,40" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p5bp_tk18" st="f=#ffffff;s=#999999;b=1" g="840,1384,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5bp_tv18" st="f=#ffffff;s=#999999" g="990,1384,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：add（2）apply 寫入段">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：add &amp;lt;repo&amp;gt;（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="bB2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1500" v="5b″ add &amp;lt;repo&amp;gt; 的 apply 寫入段（承「add（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → materialize → 印記 → 初始檔逐檔（每個 [[file]] 迴圈）→ baseline → metadata → tools.just → version.toml → 刪日誌"/>
<c id="bB2_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="c13c" parent="bB2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="610,36,300,58" v="來自「add（1′）」頁：apply 檢查通過（非 dry-run）"/>
<c id="c15a" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,115,400,40" v="建進度日誌（metadata state=in-progress；第一個寫入前）"/>
<c id="c15a_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,105,30,20" v="v2"/>
<c id="c15af" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,114,360,42" v="＋baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（state=in-progress）"/>
<c id="c15" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,176,400,40" v="materialize：/dist/&amp;lt;repo&amp;gt; 複製到暫存目錄"/>
<c id="c15_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,166,30,20" v="v2"/>
<c id="c15c" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,236,400,40" v="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）"/>
<c id="c15c_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,226,30,20" v="v2"/>
<c id="c15f" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,236,360,40" v="＋cache/&amp;lt;repo&amp;gt;/（不進 git）"/>
<c id="c15b" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,296,400,48" v="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）"/>
<c id="c15b_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,286,30,20" v="v2"/>
<c id="c15bf" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,300,360,40" v="＋gen/&amp;lt;repo&amp;gt;.stamp（不進 git）"/>
<c id="cl" parent="bB2" st="text;s=none;f=none;b=1" g="680,364,280,42" v="↓ 初始檔逐檔（init.toml 每個 [[file]]；範本讀 /dist/&amp;lt;repo&amp;gt;）"/>
<c id="c16" parent="bB2" st="rhombus;f=#FFF4C3;s=#000000" g="560,440,200,50" v="初始檔已存在？"/>
<c id="c17" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="810,444,150,42" v="無：建該檔（state=managed）"/>
<c id="cr" parent="bB2" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,426,360,79" v="復原（v2.2 C、v2.5 §3）：進度日誌在第一個寫入前建立、最後一步刪除；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復（唯讀動詞只提示重跑）"/>
<c id="cr_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,416,30,20" v="v2"/>
<c id="c18" parent="bB2" st="rhombus;f=#FFF4C3;s=#000000" g="560,525,200,81" v="strategy = append？"/>
<c id="c18_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="736,515,30,20" v="v2"/>
<c id="c19" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="780,529,180,73" v="否：不納管（state=unmanaged）、不覆蓋，印「已存在，範本在 cache」"/>
<c id="c20q" parent="bB2" st="rhombus;f=#FFF4C3;s=#000000" g="560,626,320,81" v="問「要在 X 加這幾行嗎」？（-y 免問）"/>
<c id="c20q_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="856,616,30,20" v="v2"/>
<c id="c20n" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,767,150,63" v="否：不寫；state=unmanaged 只記 declined_hash"/>
<c id="c20n_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="686,757,30,20" v="v2"/>
<c id="c20" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="750,770,210,57" v="是：append 那幾行（state=appended；實際插入的行之後記進 metadata）"/>
<c id="c20l" parent="bB2" st="rhombus;f=#FFF4C3;s=#000000" g="610,850,300,81" v="還有下一個 [[file]]？"/>
<c id="c20l_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="886,840,30,20" v="v2"/>
<c id="c21" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,951,400,40" v="否：寫 baseline/&amp;lt;repo&amp;gt;/（範本副本）"/>
<c id="c21f" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,951,360,40" v="＋baseline/&amp;lt;repo&amp;gt;/（進 git）"/>
<c id="c21b" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1011,400,48" v="寫 metadata：來源 ref@digest、最後合併版本（--local 另記 local_image_id）"/>
<c id="c21b_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1001,30,20" v="v2"/>
<c id="c21bf" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1015,360,40" v="＋baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（進 git）"/>
<c id="c21c" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1079,400,63" v="寫 metadata：每個 dest 的 state（managed／appended／unmanaged；新檔被拒才 declined）、declined_hash、append 行（lines）"/>
<c id="c21c_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1069,30,20" v="v2"/>
<c id="c21cf" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1090,360,42" v=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）"/>
<c id="c21d" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1162,400,40" v="寫 metadata：完成標記（complete）"/>
<c id="c21d_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1152,30,20" v="v2"/>
<c id="c21df" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1162,360,40" v=".vendor_kit.toml（complete = true）"/>
<c id="c22" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1222,400,48" v="重生 gen/tools.just（每個 &amp;lt;ns&amp;gt;.just 一行 mod?；一工具可多行）"/>
<c id="c22_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1212,30,20" v="v2"/>
<c id="c22f" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1226,360,40" v="gen/tools.just（不進 git；mod? 行）"/>
<c id="c23" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1290,400,48" v="最後寫 version.toml [tools]：&amp;lt;repo&amp;gt; = &quot;…:&amp;lt;tag&amp;gt;@sha256:…&quot;"/>
<c id="c23_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1280,30,20" v="v2"/>
<c id="c23f" parent="bB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1294,360,40" v="＋version.toml [tools] 行（進 git）"/>
<c id="c23x" parent="bB2" st="ellipse;f=#f8cecc;s=#000000" g="20,1358,220,58" v="失敗 → 1：明列已完成／未完成"/>
<c id="c23x_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1348,30,20" v="v2"/>
<c id="c23b" parent="bB2" st="f=#dae8fc;s=#6c8ebf" g="560,1367,400,40" v="刪進度日誌（最後一步）"/>
<c id="c23b_v2" parent="bB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1357,30,20" v="v2"/>
<c id="c24" parent="bB2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1436,220,58" v="成功 → 0：印摘要，提示 git add"/>
<c id="ce23a" edge source="c13c" target="c15a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce23b" edge source="c15a" target="c15af" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce23c" edge source="c15a" target="c15" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce23cc" edge source="c15" target="c15c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce23" edge source="c15c" target="c15f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce23d" edge source="c15c" target="c15b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce23e" edge source="c15b" target="c15bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce24" edge source="c15b" target="c16" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce25" edge source="c16" target="c17" st="es=orthogonalEdgeStyle;s=default;fc=default" v="無"/>
<c id="ce26" edge source="c16" target="c18" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ce27" edge source="c18" target="c19" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ce28" edge source="c18" target="c20q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="680,757;740,757" v="是"/>
<c id="ce28n" edge source="c20q" target="c20n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.19626168224299068,0,," v="否"/>
<c id="ce28y" edge source="c20q" target="c20" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.16838487972508587,0,," v="是"/>
<c id="ce29" edge source="c17" target="c20l" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,606;990,981;780,981"/>
<c id="ce30" edge source="c19" target="c20l" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,706;990,981;780,981"/>
<c id="ce31" edge source="c20" target="c20l" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.03,0,," pts="875,981;780,981"/>
<c id="ce31n" edge source="c20n" target="c20l" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="655,981;780,981"/>
<c id="ce31y" edge source="c20l" target="c16" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.69,0,," pts="565,1032;565,606" v="是"/>
<c id="ce31l" edge source="c20l" target="c21" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ce32" edge source="c21" target="c21f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce32b" edge source="c21" target="c21b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce32f" edge source="c21b" target="c21bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce32c" edge source="c21b" target="c21c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce32cf" edge source="c21c" target="c21cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce32d" edge source="c21c" target="c21d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce32df" edge source="c21d" target="c21df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce33" edge source="c21d" target="c22" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce34" edge source="c22" target="c22f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce35" edge source="c22" target="c23" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ce36" edge source="c23" target="c23f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ce37" edge source="c23" target="c23b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="成功"/>
<c id="ce38" edge source="c23" target="c23x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,1489;150,1489" v="失敗"/>
<c id="ce39" edge source="c23b" target="c24" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.90,0,," pts="780,1606"/>
<c id="p5bc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1657,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p5bc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1657,140,64" v="黃：判斷"/>
<c id="p5bc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1665,140,44" v="綠：起點／終點"/>
<c id="p5bc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1659,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p5bc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1659,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p5bc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1667,88,40" v="白：步驟"/>
<c id="p5bc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1667,170,40" v="虛線框：專案裡的檔案"/>
<c id="p5bc_lgt" st="text;s=none;f=none" g="1318,1657,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p5bc_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1725,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p5bc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1725,120,36" v="便條：補充說明"/>
<c id="p5bc_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,1725,150,36" v="橘框：規則（已定）"/>
<c id="p5bc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="570,1725,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p5bc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="780,1725,170,36" v="紫：image（引擎與工具）"/>
<c id="p5bc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="970,1725,170,36" v="灰底：泳道／表格表頭"/>
<c id="p5bc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1160,1725,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p5bc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1336,1715,30,20" v="v2"/>
<c id="p5bc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1763,200,28" v="本頁名詞"/>
<c id="p5bc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1797,150,71" v="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]"/>
<c id="p5bc_tv0" st="f=#ffffff;s=#999999" g="190,1797,610,71" v="接一個工具（@&amp;lt;tag&amp;gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0"/>
<c id="p5bc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1868,150,40" v="resolve／apply"/>
<c id="p5bc_tv1" st="f=#ffffff;s=#999999" g="190,1868,610,40" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）"/>
<c id="p5bc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1908,150,40" v="stdout／stderr"/>
<c id="p5bc_tv2" st="f=#ffffff;s=#999999" g="190,1908,610,40" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行"/>
<c id="p5bc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1948,150,40" v="輸入指紋"/>
<c id="p5bc_tv3" st="f=#ffffff;s=#999999" g="190,1948,610,40" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」"/>
<c id="p5bc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1988,150,55" v="GHCR／image／index digest／image inspect"/>
<c id="p5bc_tv4" st="f=#ffffff;s=#999999" g="190,1988,610,55" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台"/>
<c id="p5bc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2043,150,55" v="--local／tar／.digest（Q26）"/>
<c id="p5bc_tv5" st="f=#ffffff;s=#999999" g="190,2043,610,55" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local"/>
<c id="p5bc_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2098,150,40" v="/dist/&amp;lt;repo&amp;gt;（暫存）／N"/>
<c id="p5bc_tv6" st="f=#ffffff;s=#999999" g="190,2098,610,40" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&amp;lt;repo&amp;gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&amp;lt;repo&amp;gt;（v2.5 §2）"/>
<c id="p5bc_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2138,150,40" v="materialize／印記"/>
<c id="p5bc_tv7" st="f=#ffffff;s=#999999" g="190,2138,610,40" v="引擎內部步驟：apply 決定套用後才把 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 = gen/&amp;lt;repo&amp;gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）"/>
<c id="p5bc_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2178,150,55" v="初始檔／strategy"/>
<c id="p5bc_tv8" st="f=#ffffff;s=#999999" g="190,2178,610,55" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）"/>
<c id="p5bc_tk9" st="f=#ffffff;s=#999999;b=1" g="40,2233,150,40" v="dest 撞名"/>
<c id="p5bc_tv9" st="f=#ffffff;s=#999999" g="190,2233,610,40" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/"/>
<c id="p5bc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1797,150,40" v="命名空間撞名（v2.5 §5）"/>
<c id="p5bc_tv10" st="f=#ffffff;s=#999999" g="990,1797,610,40" v="工具 dist/just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）"/>
<c id="p5bc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1837,150,71" v="baseline／metadata"/>
<c id="p5bc_tv11" st="f=#ffffff;s=#999999" g="990,1837,610,71" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）"/>
<c id="p5bc_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1908,150,28" v="續作"/>
<c id="p5bc_tv12" st="f=#ffffff;s=#999999" g="990,1908,610,28" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔"/>
<c id="p5bc_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1936,150,71" v="gen／mod?／recipe"/>
<c id="p5bc_tv13" st="f=#ffffff;s=#999999" g="990,1936,610,71" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? &amp;lt;ns&amp;gt; &#x27;../cache/&amp;lt;repo&amp;gt;/just/&amp;lt;ns&amp;gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe"/>
<c id="p5bc_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2007,150,55" v="CI 為真／frozen／dry-run"/>
<c id="p5bc_tv14" st="f=#ffffff;s=#999999" g="990,2007,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）"/>
<c id="p5bc_tk15" st="f=#ffffff;s=#999999;b=1" g="840,2062,150,28" v="flock"/>
<c id="p5bc_tv15" st="f=#ffffff;s=#999999" g="990,2062,610,28" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖"/>
<c id="p5bc_tk16" st="f=#ffffff;s=#999999;b=1" g="840,2090,150,28" v="symlink"/>
<c id="p5bc_tv16" st="f=#ffffff;s=#999999" g="990,2090,610,28" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕"/>
<c id="p5bc_tk17" st="f=#ffffff;s=#999999;b=1" g="840,2118,150,40" v="CRLF"/>
<c id="p5bc_tv17" st="f=#ffffff;s=#999999" g="990,2118,610,40" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p5bc_tk18" st="f=#ffffff;s=#999999;b=1" g="840,2158,150,55" v="結束狀態 0／1／2／3"/>
<c id="p5bc_tv18" st="f=#ffffff;s=#999999" g="990,2158,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：sync（1）啟動器快路徑">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：sync（1）啟動器：gen/.stamp 比對 → 快路徑（Q22）→ 起引擎（§6、v2.3 §2、v2.5 §9、v2.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="eA" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,857" v="sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 0 不起容器；有差 → docker image inspect → 引擎 resolve sync（見「sync（1′）」頁）"/>
<c id="eA_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="n0" parent="eA" st="ellipse;f=#d5e8d4;s=#000000" g="20,51,220,80" v="打工具 recipe（_sync 自動前置）或 just vendor_kit sync"/>
<c id="n1" parent="eA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,60,280,63" v="grep version.toml 第一行取引擎 ref（version.local.toml 的 vendor_kit 覆寫優先）"/>
<c id="n1_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,50,30,20" v="v2"/>
<c id="n2" parent="eA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,36,360,110" v="讀"/>
<c id="n2_0" parent="n2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,344,26" v=".vendor_kit/version.toml（進 git）"/>
<c id="n2_1" parent="n2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,344,42" v=".vendor_kit/version.local.toml（不進 git，dev 用）"/>
<c id="n3n" parent="eA" st="ellipse;f=#ffe6cc;s=#000000" g="20,166,220,124" v="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」"/>
<c id="n3n_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,156,30,20" v="v2"/>
<c id="n3" parent="eA" st="rhombus;f=#FFF4C3;s=#000000" g="260,172,260,112" v="gen/.stamp 的引擎 ref ＝ 第一行？"/>
<c id="n3_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="496,162,30,20" v="v2"/>
<c id="n6" parent="eA" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,181,360,94" v="統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／upgrade vendor_kit 不受此關"/>
<c id="n6_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,171,30,20" v="v2"/>
<c id="nq0" parent="eA" st="ellipse;f=#d5e8d4;s=#000000" g="20,325,220,80" v="是 → 0：不起容器，接著跑原本的 recipe（快路徑）"/>
<c id="nq0_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,315,30,20" v="v2"/>
<c id="nq" parent="eA" st="rhombus;f=#FFF4C3;s=#000000" g="260,324,260,81" v="快路徑：grep 全相符且非 frozen？"/>
<c id="nq_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="496,314,30,20" v="v2"/>
<c id="nqr" parent="eA" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,310,360,110" v="快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；CI 不為真；sync 無參數。全相符 → 0；否則起引擎；每檔 sha256 只在 sync --verify、CI 為真、或版本變動的那次才做（§3.6）"/>
<c id="nqr_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,300,30,20" v="v2"/>
<c id="n1i" parent="eA" st="rhombus;f=#FFF4C3;s=#000000" g="280,440,220,112" v="docker image inspect：本機有？"/>
<c id="n1i_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="476,430,30,20" v="v2"/>
<c id="n6b" parent="eA" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,456,360,79" v="薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與 upgrade vendor_kit 做；做之前比對現內容 == 上次產物（首行自描述 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼"/>
<c id="n6b_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,446,30,20" v="v2"/>
<c id="n1p" parent="eA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,572,80,79" v="無：docker pull &amp;lt;引擎 ref&amp;gt;"/>
<c id="n1p_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,562,30,20" v="v2"/>
<c id="n1g" parent="eA" st="f=#e1d5e7;s=#9673a6" g="980,590,220,42" v="vendor_kit:vN@sha256:…&lt;br&gt;（引擎 image）"/>
<c id="n1v" parent="eA" st="rhombus;f=#FFF4C3;s=#000000" g="280,671,220,112" v="覆寫中且 .Id ≠ 記的 image ID？"/>
<c id="n1v_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="476,661,30,20" v="v2"/>
<c id="n1x" parent="eA" st="ellipse;f=#f8cecc;s=#000000" g="560,687,240,80" v="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"/>
<c id="n1x_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,677,30,20" v="v2"/>
<c id="n1b" parent="eA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,803,280,48" v="否：docker run &amp;lt;引擎&amp;gt; resolve sync（永不 -t）"/>
<c id="n1b_v2" parent="eA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,793,30,20" v="v2"/>
<c id="n1z" parent="eA" st="text;s=none;f=none;b=1" g="560,806,300,42" v="→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）"/>
<c id="ne1" edge source="n0" target="n1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ne2" edge source="n1" target="n2" st="es=orthogonalEdgeStyle;s=default;fc=default" v="讀"/>
<c id="ne3" edge source="n1" target="n3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ne4" edge source="n3" target="n3n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ne5" edge source="n3" target="nq" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ne5q" edge source="nq" target="nq0" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ne5n" edge source="nq" target="n1i" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ne5p" edge source="n1i" target="n1p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.68,0,," pts="520,652" v="無"/>
<c id="ne5g" edge source="n1g" target="n1p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="ne5v" edge source="n1i" target="n1v" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ne5pv" edge source="n1p" target="n1v" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="500,817;410,817"/>
<c id="ne5x" edge source="n1p" target="n1x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="540,825;640,825" v="失敗"/>
<c id="ne5y" edge source="n1v" target="n1x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ne5i" edge source="n1v" target="n1b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ne6" edge source="n1b" target="n1z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p6_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1029,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p6_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1029,140,64" v="黃：判斷"/>
<c id="p6_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1037,140,44" v="綠：起點／終點"/>
<c id="p6_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1031,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p6_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1031,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p6_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1039,88,40" v="白：步驟"/>
<c id="p6_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1039,170,40" v="虛線框：專案裡的檔案"/>
<c id="p6_lgt" st="text;s=none;f=none" g="1318,1029,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p6_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1097,120,36" v="便條：補充說明"/>
<c id="p6_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1097,150,36" v="橘框：規則（已定）"/>
<c id="p6_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1097,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p6_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1097,170,36" v="紫：image（引擎與工具）"/>
<c id="p6_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1097,170,36" v="灰底：泳道／表格表頭"/>
<c id="p6_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1097,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p6_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1087,30,20" v="v2"/>
<c id="p6_th" st="text;fs=13;s=none;f=none;b=1" g="40,1135,200,28" v="本頁名詞"/>
<c id="p6_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1169,150,55" v="sync"/>
<c id="p6_tv0" st="f=#ffffff;s=#999999" g="190,1169,610,55" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑"/>
<c id="p6_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1224,150,71" v="快路徑（Q22）"/>
<c id="p6_tv1" st="f=#ffffff;s=#999999" g="190,1224,610,71" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync"/>
<c id="p6_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1295,150,55" v="resolve／apply"/>
<c id="p6_tv2" st="f=#ffffff;s=#999999" g="190,1295,610,55" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no"/>
<c id="p6_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1350,150,40" v="stdout／stderr／指紋"/>
<c id="p6_tv3" st="f=#ffffff;s=#999999" g="190,1350,610,40" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」"/>
<c id="p6_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1390,150,71" v="frozen（CI 為真）"/>
<c id="p6_tv4" st="f=#ffffff;s=#999999" g="190,1390,610,71" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1"/>
<c id="p6_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1461,150,55" v="統一提示（Q10 (2)）"/>
<c id="p6_tv5" st="f=#ffffff;s=#999999" g="190,1461,610,55" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關"/>
<c id="p6_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1516,150,55" v="薄殼／引擎 ref／hash"/>
<c id="p6_tv6" st="f=#ffffff;s=#999999" g="190,1516,610,55" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋"/>
<c id="p6_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1571,150,55" v="gen/ 三種檔"/>
<c id="p6_tv7" st="f=#ffffff;s=#999999" g="190,1571,610,55" v="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）"/>
<c id="p6_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1626,150,55" v="materialize／印記／index digest"/>
<c id="p6_tv8" st="f=#ffffff;s=#999999" g="190,1626,610,55" v="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）"/>
<c id="p6_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1169,150,71" v="image tag／digest／image ID／image inspect"/>
<c id="p6_tv9" st="f=#ffffff;s=#999999" g="990,1169,610,71" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1"/>
<c id="p6_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1240,150,55" v="verify／sha256"/>
<c id="p6_tv10" st="f=#ffffff;s=#999999" g="990,1240,610,55" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify"/>
<c id="p6_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1295,150,55" v="metadata／完成標記／落後"/>
<c id="p6_tv11" st="f=#ffffff;s=#999999" g="990,1295,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）"/>
<c id="p6_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1350,150,55" v="mod?／recipe"/>
<c id="p6_tv12" st="f=#ffffff;s=#999999" g="990,1350,610,55" v="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe"/>
<c id="p6_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1405,150,40" v="symlink"/>
<c id="p6_tv13" st="f=#ffffff;s=#999999" g="990,1405,610,40" v="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify"/>
<c id="p6_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1445,150,55" v="覆寫兩種（v2.1 B／v2.2 B）"/>
<c id="p6_tv14" st="f=#ffffff;s=#999999" g="990,1445,610,55" v="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline"/>
<c id="p6_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1500,150,40" v="GHCR／image／daemon／flock"/>
<c id="p6_tv15" st="f=#ffffff;s=#999999" g="990,1500,610,40" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎"/>
<c id="p6_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1540,150,55" v="結束狀態 0／1／2／3"/>
<c id="p6_tv16" st="f=#ffffff;s=#999999" g="990,1540,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：sync（1′）引擎 resolve">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：sync（1′）引擎 resolve sync（逐工具；§6、v2.2 A／B／E、v2.3 §3／§4、v2.5 §9、v2.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="eA2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,1509" v="sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 逐工具算待辦 → 無待辦（apply|no）→ 0；有待辦 → 第 2 段見「sync（2）」頁"/>
<c id="eA2_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="n1e" parent="eA2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="610,36,300,58" v="來自「sync（1）」頁：docker run &amp;lt;引擎&amp;gt; resolve sync"/>
<c id="ncx" parent="eA2" st="ellipse;f=#ffe6cc;s=#000000" g="20,114,220,102" v="是 → 1：CI 拒絕本機覆寫（frozen；請先 undev 或勿在 CI 用 local 覆寫）"/>
<c id="ncx_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,104,30,20" v="v2"/>
<c id="nc" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,124,330,81" v="CI 為真（frozen）且有 local 覆寫？"/>
<c id="nc_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,114,30,20" v="v2"/>
<c id="nf" parent="eA2" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,126,360,79" v="frozen（CI 為真 = CI 非空且不為 0／false；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；任何需要寫 tracked 檔 → 1（-y 不解除）；升為失敗的警告：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫"/>
<c id="nf_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,116,30,20" v="v2"/>
<c id="t0" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,242,250,81" v="path 覆寫（dev 中）？"/>
<c id="t0_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,232,30,20" v="v2"/>
<c id="t0s" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="830,236,130,94" v="是：跳過 materialize／verify，仍查 metadata、baseline ↓"/>
<c id="t0s_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,226,30,20" v="v2"/>
<c id="t0r" parent="eA2" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,244,360,79" v="覆寫兩種（v2.1 B）：引擎 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache/&amp;lt;repo&amp;gt;/ 是 symlink，跳過 materialize／verify"/>
<c id="t0r_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,234,30,20" v="v2"/>
<c id="t1" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,350,250,81" v="cache 缺或印記 ≠ 鎖定 digest？"/>
<c id="t1_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,340,30,20" v="v2"/>
<c id="t1y" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="830,351,130,79" v="是：列待辦「materialize 鎖定版」（不 verify 舊 cache）"/>
<c id="t1y_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,341,30,20" v="v2"/>
<c id="t2q" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,451,250,112" v="否 → sync --verify、CI 為真、版本變動那次？"/>
<c id="t2q_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,441,30,20" v="v2"/>
<c id="t2qn" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="830,483,130,48" v="否：不逐檔驗（快）↓"/>
<c id="t2qn_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,473,30,20" v="v2"/>
<c id="t2" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,583,250,112" v="是 → verify：每檔 sha256 ＝ 印記？"/>
<c id="t2n" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="830,610,130,57" v="否：列待辦「重裝 + warn（cache 被改過）」"/>
<c id="t3a" parent="eA2" st="ellipse;f=#ffe6cc;s=#000000" g="20,715,220,102" v="否 → 1：「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」"/>
<c id="t3" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,726,250,81" v="metadata 有完成標記？"/>
<c id="t3r" parent="eA2" st="f=#ffffff;s=#b85450;b=1" g="1220,726,360,79" v="不變量（v2.1 A、v2.5 §9）：自動化不碰使用者的檔 —— sync 不寫 version.toml、初始檔、baseline、薄殼、gen/.stamp；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="t3r_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,716,30,20" v="v2"/>
<c id="t4" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,837,250,81" v="最後合併版本 ＝ version.toml？"/>
<c id="t4r" parent="eA2" st="ellipse;f=#ffe6cc;s=#000000" g="20,938,220,102" v="是 → 1：baseline 落後，印「請在本機 upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push」"/>
<c id="t4c" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,948,250,81" v="否（落後）→ CI 為真（frozen）？"/>
<c id="t5" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,1060,300,42" v="否：warn「baseline 落後，請 just vendor_kit upgrade &amp;lt;repo&amp;gt;」（繼續）"/>
<c id="tq" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,1122,270,50" v="還有工具？"/>
<c id="tq_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="806,1112,30,20" v="v2"/>
<c id="t6" parent="eA2" st="rhombus;f=#FFF4C3;s=#000000" g="560,1192,270,81" v="否 → tools.just 缺或不符？"/>
<c id="t6_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="806,1182,30,20" v="v2"/>
<c id="t6y" parent="eA2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="843,1201,117,63" v="是：列待辦「重生 gen/tools.just」"/>
<c id="t6y_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1191,30,20" v="v2"/>
<c id="z0" parent="eA2" st="f=#dae8fc;s=#6c8ebf" g="560,1293,400,48" v="resolve 完：產生待辦清單（要拉的 image、要重裝、要重生 gen/tools.just）→ 空 = apply|no"/>
<c id="z0_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1283,30,20" v="v2"/>
<c id="z2" parent="eA2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1361,220,80" v="無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe"/>
<c id="z2_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1351,30,20" v="v2"/>
<c id="z1" parent="eA2" st="f=#dae8fc;s=#6c8ebf" g="560,1377,400,48" v="產生輸入指紋（version.toml、metadata、印記 hash）→ 清單＋指紋＋apply|yes／no 以 stdout 回啟動器"/>
<c id="z1_v2" parent="eA2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1367,30,20" v="v2"/>
<c id="mb" parent="eA2" st="text;s=none;f=none;b=1" g="560,1461,400,42" v="有待辦 ↓ 續「sync（2）」頁：啟動器 docker → 引擎 apply sync"/>
<c id="ne6" edge source="n1e" target="nc" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ne7" edge source="nc" target="ncx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ne8" edge source="nc" target="t0" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.05,0,," pts="745,382;705,382" v="否"/>
<c id="te0" edge source="t0" target="t0s" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te1" edge source="t0" target="t1" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te2" edge source="t0s" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,439;990,861;705,861"/>
<c id="te3" edge source="t1" target="t1y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te4" edge source="t1" target="t2q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te5" edge source="t1y" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,546;990,861;705,861"/>
<c id="te3q" edge source="t2q" target="t2qn" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="te4q" edge source="t2q" target="t2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="te5q" edge source="t2qn" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,663;990,861;705,861"/>
<c id="te6" edge source="t2" target="t2n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="te7" edge source="t2" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="te8" edge source="t2n" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,795;990,861;705,861"/>
<c id="te9" edge source="t3" target="t3a" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="te10" edge source="t3" target="t4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="te11" edge source="t4" target="t4c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te12" edge source="t4c" target="t4r" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te13" edge source="t4c" target="t5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te14" edge source="t4" target="tq" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="990,1034;990,1268;715,1268" v="是"/>
<c id="te15" edge source="t5" target="tq" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te15n" edge source="tq" target="t6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te16" edge source="t6" target="t6y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te17" edge source="t6" target="z0" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te18" edge source="t6y" target="z0" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ze0" edge source="z0" target="z1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ze1" edge source="z1" target="z2" st="es=orthogonalEdgeStyle;s=default;fc=default" v="無待辦"/>
<c id="ze2" edge source="z1" target="mb" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te15y" edge source="tq" target="t0" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="1020,1303;1020,382;705,382" v="是：下一個工具"/>
<c id="p6r_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1681,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p6r_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1681,140,64" v="黃：判斷"/>
<c id="p6r_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1689,140,44" v="綠：起點／終點"/>
<c id="p6r_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1683,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p6r_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1683,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p6r_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1691,88,40" v="白：步驟"/>
<c id="p6r_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1691,170,40" v="虛線框：專案裡的檔案"/>
<c id="p6r_lgt" st="text;s=none;f=none" g="1318,1681,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p6r_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1749,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p6r_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1749,120,36" v="便條：補充說明"/>
<c id="p6r_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,1749,150,36" v="橘框：規則（已定）"/>
<c id="p6r_lgx_inv" st="f=#ffffff;s=#b85450;b=1" g="570,1749,130,36" v="紅粗框：不變量"/>
<c id="p6r_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="720,1749,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p6r_lgx_img" st="f=#e1d5e7;s=#9673a6" g="930,1749,170,36" v="紫：image（引擎與工具）"/>
<c id="p6r_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="1120,1749,170,36" v="灰底：泳道／表格表頭"/>
<c id="p6r_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1310,1749,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p6r_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1486,1739,30,20" v="v2"/>
<c id="p6r_th" st="text;fs=13;s=none;f=none;b=1" g="40,1787,200,28" v="本頁名詞"/>
<c id="p6r_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1821,150,55" v="sync"/>
<c id="p6r_tv0" st="f=#ffffff;s=#999999" g="190,1821,610,55" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑"/>
<c id="p6r_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1876,150,71" v="快路徑（Q22）"/>
<c id="p6r_tv1" st="f=#ffffff;s=#999999" g="190,1876,610,71" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync"/>
<c id="p6r_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1947,150,55" v="resolve／apply"/>
<c id="p6r_tv2" st="f=#ffffff;s=#999999" g="190,1947,610,55" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no"/>
<c id="p6r_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2002,150,40" v="stdout／stderr／指紋"/>
<c id="p6r_tv3" st="f=#ffffff;s=#999999" g="190,2002,610,40" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」"/>
<c id="p6r_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2042,150,71" v="frozen（CI 為真）"/>
<c id="p6r_tv4" st="f=#ffffff;s=#999999" g="190,2042,610,71" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1"/>
<c id="p6r_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2113,150,55" v="統一提示（Q10 (2)）"/>
<c id="p6r_tv5" st="f=#ffffff;s=#999999" g="190,2113,610,55" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關"/>
<c id="p6r_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2168,150,55" v="薄殼／引擎 ref／hash"/>
<c id="p6r_tv6" st="f=#ffffff;s=#999999" g="190,2168,610,55" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋"/>
<c id="p6r_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2223,150,55" v="gen/ 三種檔"/>
<c id="p6r_tv7" st="f=#ffffff;s=#999999" g="190,2223,610,55" v="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）"/>
<c id="p6r_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2278,150,55" v="materialize／印記／index digest"/>
<c id="p6r_tv8" st="f=#ffffff;s=#999999" g="190,2278,610,55" v="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）"/>
<c id="p6r_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1821,150,71" v="image tag／digest／image ID／image inspect"/>
<c id="p6r_tv9" st="f=#ffffff;s=#999999" g="990,1821,610,71" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1"/>
<c id="p6r_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1892,150,55" v="verify／sha256"/>
<c id="p6r_tv10" st="f=#ffffff;s=#999999" g="990,1892,610,55" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify"/>
<c id="p6r_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1947,150,55" v="metadata／完成標記／落後"/>
<c id="p6r_tv11" st="f=#ffffff;s=#999999" g="990,1947,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）"/>
<c id="p6r_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2002,150,55" v="mod?／recipe"/>
<c id="p6r_tv12" st="f=#ffffff;s=#999999" g="990,2002,610,55" v="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe"/>
<c id="p6r_tk13" st="f=#ffffff;s=#999999;b=1" g="840,2057,150,40" v="symlink"/>
<c id="p6r_tv13" st="f=#ffffff;s=#999999" g="990,2057,610,40" v="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify"/>
<c id="p6r_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2097,150,55" v="覆寫兩種（v2.1 B／v2.2 B）"/>
<c id="p6r_tv14" st="f=#ffffff;s=#999999" g="990,2097,610,55" v="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline"/>
<c id="p6r_tk15" st="f=#ffffff;s=#999999;b=1" g="840,2152,150,40" v="GHCR／image／daemon／flock"/>
<c id="p6r_tv15" st="f=#ffffff;s=#999999" g="990,2152,610,40" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎"/>
<c id="p6r_tk16" st="f=#ffffff;s=#999999;b=1" g="840,2192,150,55" v="結束狀態 0／1／2／3"/>
<c id="p6r_tv16" st="f=#ffffff;s=#999999" g="990,2192,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：sync（2）apply">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：sync（2）第 2 段 apply（§6、v2.3 §3／§4、v2.5 §9）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify、CI 為真、版本變動那次才做（§3.6）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="eB" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,1162" v="sync 第 2 段（承「sync（1′）」頁：有待辦才跑）：啟動器對每個要拉的 image inspect → 無才 pull → create → cp → rm → 引擎 apply sync；只寫 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp；版本變動那次逐檔 sha256 全驗（§3.6）"/>
<c id="eB_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="m00" parent="eB" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="260,36,280,80" v="來自「sync（1′）」頁：有待辦（resolve 的 stdout 清單，apply|yes）"/>
<c id="m0a" parent="eB" st="rhombus;f=#FFF4C3;s=#000000" g="260,136,170,206" v="對每個要拉的 image：docker image inspect 本機有？"/>
<c id="m0a_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="406,126,30,20" v="v2"/>
<c id="m0p" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="440,362,100,48" v="無：docker pull"/>
<c id="m0p_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,352,30,20" v="v2"/>
<c id="m0g" parent="eB" st="f=#e1d5e7;s=#9673a6" g="980,365,220,42" v="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（鎖定版；多架構 index）"/>
<c id="m0b" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,430,280,40" v="docker create &amp;lt;img&amp;gt; /x"/>
<c id="m0b_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,420,30,20" v="v2"/>
<c id="m0c" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,490,280,48" v="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）"/>
<c id="m0c_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,480,30,20" v="v2"/>
<c id="m0d" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,558,280,40" v="docker rm 該容器"/>
<c id="m0d_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,548,30,20" v="v2"/>
<c id="m1" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,618,280,48" v="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply sync"/>
<c id="m1_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,608,30,20" v="v2"/>
<c id="m2a" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,622,400,40" v="apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）"/>
<c id="m2a_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,612,30,20" v="v2"/>
<c id="m2b" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,695,240,40" v="重驗 resolve 的輸入指紋"/>
<c id="m2b_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,685,30,20" v="v2"/>
<c id="m2x" parent="eB" st="ellipse;f=#ffe6cc;s=#000000" g="820,686,140,58" v="不同 → 1「請重跑」"/>
<c id="m2x_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,676,30,20" v="v2"/>
<c id="m3" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,764,400,48" v="materialize／重裝（每個待辦工具）：/dist/&amp;lt;repo&amp;gt; 展開到暫存目錄"/>
<c id="m3_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,754,30,20" v="v2"/>
<c id="m3c" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,832,400,40" v="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）"/>
<c id="m3c_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,822,30,20" v="v2"/>
<c id="m3f" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,832,360,40" v="cache/&amp;lt;repo&amp;gt;/（重寫，不進 git）"/>
<c id="m3b" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,892,400,48" v="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）"/>
<c id="m3b_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,882,30,20" v="v2"/>
<c id="m3bf" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,896,360,40" v="gen/&amp;lt;repo&amp;gt;.stamp（重寫，不進 git）"/>
<c id="m3v" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,960,400,48" v="版本變動的那次（快路徑有差且由版本變動造成）：逐檔 sha256 驗 cache/&amp;lt;repo&amp;gt;/ ＝ 印記（§3.6）"/>
<c id="m3v_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,950,30,20" v="v2"/>
<c id="m3vq" parent="eB" st="rhombus;f=#FFF4C3;s=#000000" g="560,1028,200,50" v="全部相符？"/>
<c id="m3vq_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="736,1018,30,20" v="v2"/>
<c id="m3vn" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="810,1029,150,48" v="否：重裝該工具 + warn（cache 被改過）"/>
<c id="m3vn_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1019,30,20" v="v2"/>
<c id="m7" parent="eB" st="ellipse;f=#d5e8d4;s=#000000" g="20,1098,220,58" v="0：接著跑原本的 recipe"/>
<c id="m5" parent="eB" st="f=#dae8fc;s=#6c8ebf" g="560,1103,400,48" v="重生 gen/tools.just（待辦有它時；每個 &amp;lt;ns&amp;gt;.just 一行 mod?）"/>
<c id="m5_v2" parent="eB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1093,30,20" v="v2"/>
<c id="m5f" parent="eB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1107,360,40" v="gen/tools.just（不進 git；gen/.stamp 不動）"/>
<c id="me0" edge source="m00" target="m0a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="420,282;365,282"/>
<c id="me0n" edge source="m0a" target="m0p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.67,0,," pts="510,395" v="無"/>
<c id="me0g" edge source="m0g" target="m0p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="me0y" edge source="m0a" target="m0b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="me0p" edge source="m0p" target="m0b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me0c" edge source="m0b" target="m0c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me0d" edge source="m0c" target="m0d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me1" edge source="m0d" target="m1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me2" edge source="m1" target="m2a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me2b" edge source="m2a" target="m2b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me2x" edge source="m2b" target="m2x" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me3" edge source="m2b" target="m3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me3c" edge source="m3" target="m3c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me4" edge source="m3c" target="m3f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me4b" edge source="m3c" target="m3b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me4f" edge source="m3b" target="m3bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me4v" edge source="m3b" target="m3v" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me4q" edge source="m3v" target="m3vq" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me4n" edge source="m3vq" target="m3vn" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="me5" edge source="m3vq" target="m5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="me5n" edge source="m3vn" target="m5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me12" edge source="m5" target="m5f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me15" edge source="m5" target="m7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p6c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1334,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p6c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1334,140,64" v="黃：判斷"/>
<c id="p6c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1342,140,44" v="綠：起點／終點"/>
<c id="p6c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1336,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p6c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1336,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p6c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1344,88,40" v="白：步驟"/>
<c id="p6c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1344,170,40" v="虛線框：專案裡的檔案"/>
<c id="p6c_lgt" st="text;s=none;f=none" g="1318,1334,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p6c_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1402,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p6c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1402,120,36" v="便條：補充說明"/>
<c id="p6c_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1402,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p6c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1402,170,36" v="紫：image（引擎與工具）"/>
<c id="p6c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1402,170,36" v="灰底：泳道／表格表頭"/>
<c id="p6c_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1402,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p6c_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1392,30,20" v="v2"/>
<c id="p6c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1440,200,28" v="本頁名詞"/>
<c id="p6c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1474,150,55" v="sync"/>
<c id="p6c_tv0" st="f=#ffffff;s=#999999" g="190,1474,610,55" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&amp;lt;repo&amp;gt;/、gen/tools.just、gen/&amp;lt;repo&amp;gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑"/>
<c id="p6c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1529,150,71" v="快路徑（Q22）"/>
<c id="p6c_tv1" st="f=#ffffff;s=#999999" g="190,1529,610,71" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &amp;lt;repo&amp;gt; 的 digest == gen/&amp;lt;repo&amp;gt;.stamp 第一行（或 local 覆寫的 path:&amp;lt;dir&amp;gt;）；gen/tools.just 存在；無 .tmp.&amp;lt;verb&amp;gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync"/>
<c id="p6c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1600,150,55" v="resolve／apply"/>
<c id="p6c_tv2" st="f=#ffffff;s=#999999" g="190,1600,610,55" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no"/>
<c id="p6c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1655,150,40" v="stdout／stderr／指紋"/>
<c id="p6c_tv3" st="f=#ffffff;s=#999999" g="190,1655,610,40" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」"/>
<c id="p6c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1695,150,71" v="frozen（CI 為真）"/>
<c id="p6c_tv4" st="f=#ffffff;s=#999999" g="190,1695,610,71" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1"/>
<c id="p6c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1766,150,55" v="統一提示（Q10 (2)）"/>
<c id="p6c_tv5" st="f=#ffffff;s=#999999" g="190,1766,610,55" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關"/>
<c id="p6c_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1821,150,55" v="薄殼／引擎 ref／hash"/>
<c id="p6c_tv6" st="f=#ffffff;s=#999999" g="190,1821,610,55" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋"/>
<c id="p6c_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1876,150,55" v="gen/ 三種檔"/>
<c id="p6c_tv7" st="f=#ffffff;s=#999999" g="190,1876,610,55" v="gen/tools.just：每個 &amp;lt;ns&amp;gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&amp;lt;repo&amp;gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）"/>
<c id="p6c_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1931,150,55" v="materialize／印記／index digest"/>
<c id="p6c_tv8" st="f=#ffffff;s=#999999" g="190,1931,610,55" v="把啟動器 docker create/cp 取來的 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&amp;lt;dir&amp;gt;）"/>
<c id="p6c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1474,150,71" v="image tag／digest／image ID／image inspect"/>
<c id="p6c_tv9" st="f=#ffffff;s=#999999" g="990,1474,610,71" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1"/>
<c id="p6c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1545,150,55" v="verify／sha256"/>
<c id="p6c_tv10" st="f=#ffffff;s=#999999" g="990,1545,610,55" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&amp;lt;repo&amp;gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify"/>
<c id="p6c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1600,150,55" v="metadata／完成標記／落後"/>
<c id="p6c_tv11" st="f=#ffffff;s=#999999" g="990,1600,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&amp;lt;repo&amp;gt; 未完成接入，請執行：just vendor_kit add &amp;lt;repo&amp;gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）"/>
<c id="p6c_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1655,150,55" v="mod?／recipe"/>
<c id="p6c_tv12" st="f=#ffffff;s=#999999" g="990,1655,610,55" v="mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe"/>
<c id="p6c_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1710,150,40" v="symlink"/>
<c id="p6c_tv13" st="f=#ffffff;s=#999999" g="990,1710,610,40" v="指向另一個路徑的捷徑；dev 中的工具 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify"/>
<c id="p6c_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1750,150,55" v="覆寫兩種（v2.1 B／v2.2 B）"/>
<c id="p6c_tv14" st="f=#ffffff;s=#999999" g="990,1750,610,55" v="引擎覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; → cache 是 symlink，仍查 metadata／baseline"/>
<c id="p6c_tk15" st="f=#ffffff;s=#999999;b=1" g="840,1805,150,40" v="GHCR／image／daemon／flock"/>
<c id="p6c_tv15" st="f=#ffffff;s=#999999" g="990,1805,610,40" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎"/>
<c id="p6c_tk16" st="f=#ffffff;s=#999999;b=1" g="840,1845,150,55" v="結束狀態 0／1／2／3"/>
<c id="p6c_tv16" st="f=#ffffff;s=#999999" g="990,1845,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── A. Renovate 路徑">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── A. Renovate 路徑（§2／§7、v2.2 D、v2.3 §7、v2.5 §1／§7）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,97,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,97,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,97,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,97,280,28" v="專案目錄"/>
<c id="uA" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,920" v="A. Renovate 路徑（下游自選，vendor_kit 不出 bot）：機器人只改 version.toml 一行；PR 的 CI 以新版跑完整流程；baseline 落後 → PR 紅（需要人補合併）；補合併在 PR 分支上完成、CI 綠後才 merge"/>
<c id="uA_v2" parent="uA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="a0" parent="uA" st="ellipse;f=#d5e8d4;s=#000000" g="270,36,160,58" v="Renovate 定期查 GHCR"/>
<c id="a1" parent="uA" st="f=#e1d5e7;s=#9673a6" g="1100,44,180,42" v="&amp;lt;repo&amp;gt;-dist&lt;br&gt;出新 tag@digest"/>
<c id="a2" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,114,160,57" v="開 PR（獨立分支）：只改 version.toml 該工具一行（tag@digest）"/>
<c id="a3" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,122,280,42" v="version.toml（PR 分支）&lt;br&gt;&amp;lt;repo&amp;gt; 行 = 新 tag@digest"/>
<c id="a4a" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,191,220,57" v="PR 的 CI 呼叫 .vendor_kit/ci/check.sh（以新版跑完整流程）"/>
<c id="a4r" parent="uA" st="f=#ffe6cc;s=#d79b00;b=1" g="720,198,360,42" v="一行改動本身不可能出錯，不構成通過依據&lt;br&gt;→ PR 的 CI 必須以新版跑完整流程"/>
<c id="a4b" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,268,220,42" v="check.sh ①：sync（CI 為真 → frozen；export CI=1）"/>
<c id="a5" parent="uA" st="ellipse;f=#ffe6cc;s=#000000" g="20,330,220,102" v="1 → PR 紅：需要人補合併（印「本機 upgrade &amp;lt;repo&amp;gt; -y 後 push」）"/>
<c id="a5_v2" parent="uA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,320,30,20" v="v2"/>
<c id="a4q" parent="uA" st="rhombus;f=#FFF4C3;s=#000000" g="720,340,360,81" v="baseline 落後？（最後合併版本 ≠ version.toml）"/>
<c id="a4q_v2" parent="uA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,330,30,20" v="v2"/>
<c id="a4c" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,452,220,40" v="否：check.sh ②：verify"/>
<c id="a4d" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,512,220,42" v="check.sh ③：upgrade --dry-run"/>
<c id="a4e1" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,582,220,40" v="check.sh ④：工具測試"/>
<c id="a6a" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,582,220,40" v="PR 作者本機：切到 PR 分支"/>
<c id="a6a_v2" parent="uA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,572,30,20" v="v2"/>
<c id="a9" parent="uA" st="shape=note;f=#ffffff;s=#999999" g="1300,574,280,57" v="Renovate 預設不動有人推過的分支；PR body 加警告：勿勾 rebase（會蓋掉人補的合併 commit）。vendor_kit 無 bot。"/>
<c id="a4e2" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="470,662,220,40" v="check.sh ⑤：專案測試"/>
<c id="a6b" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,651,220,63" v="upgrade &amp;lt;repo&amp;gt; -y（走「B. 手動路徑（1）」頁，固定補到 PR 鎖定版）"/>
<c id="a6b_v2" parent="uA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,641,30,20" v="v2"/>
<c id="a6c" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,734,220,40" v="commit（合併結果）"/>
<c id="a6d" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,795,220,40" v="push 到 PR 分支"/>
<c id="a7" parent="uA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,794,150,42" v="PR 分支 CI 再跑完整流程（同上）→ 綠"/>
<c id="a8" parent="uA" st="ellipse;f=#d5e8d4;s=#000000" g="260,856,180,58" v="merge PR（CI 綠後才 merge）"/>
<c id="ae1" edge source="a0" target="a1" st="es=orthogonalEdgeStyle;s=default;fc=default" v="查"/>
<c id="ae2" edge source="a1" target="a2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.01,0,," pts="1210,245;370,245" v="有新版"/>
<c id="ae3" edge source="a2" target="a3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="改一行"/>
<c id="ae4" edge source="a2" target="a4a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="370,322;600,322"/>
<c id="ae4b" edge source="a4a" target="a4b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae4q" edge source="a4b" target="a4q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.03,0,," pts="600,461;920,461"/>
<c id="ae5" edge source="a4q" target="a5" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ae5n" edge source="a4q" target="a4c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.03,0,," pts="920,583;600,583" v="否"/>
<c id="ae5c" edge source="a4c" target="a4d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae5d" edge source="a4d" target="a4e1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae5e" edge source="a4e1" target="a4e2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6" edge source="a5" target="a6a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6b" edge source="a6a" target="a6b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6c" edge source="a6b" target="a6c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae6d" edge source="a6c" target="a6d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae7" edge source="a6d" target="a7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ae8" edge source="a4e2" target="a8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.56,0,," pts="688,1026" v="綠"/>
<c id="ae9" edge source="a7" target="a8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="555,987;370,987" v="綠"/>
<c id="p7_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1077,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1077,140,64" v="黃：判斷"/>
<c id="p7_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1085,140,44" v="綠：起點／終點"/>
<c id="p7_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1079,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1079,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1087,88,40" v="白：步驟"/>
<c id="p7_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1087,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7_lgt" st="text;s=none;f=none" g="1318,1077,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1145,120,36" v="便條：補充說明"/>
<c id="p7_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1145,150,36" v="橘框：規則（已定）"/>
<c id="p7_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1145,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1145,170,36" v="紫：image（引擎與工具）"/>
<c id="p7_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1145,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1145,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1135,30,20" v="v2"/>
<c id="p7_th" st="text;fs=13;s=none;f=none;b=1" g="40,1183,200,28" v="本頁名詞"/>
<c id="p7_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1217,150,40" v="Renovate／regex manager"/>
<c id="p7_tv0" st="f=#ffffff;s=#999999" g="190,1217,610,40" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"/>
<c id="p7_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1257,150,40" v="PR／commit／push／rebase／merge"/>
<c id="p7_tv1" st="f=#ffffff;s=#999999" g="190,1257,610,40" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"/>
<c id="p7_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1297,150,55" v="check.sh／CI 為真／frozen"/>
<c id="p7_tv2" st="f=#ffffff;s=#999999" g="190,1297,610,55" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1352,150,40" v="baseline 落後／待合併"/>
<c id="p7_tv3" st="f=#ffffff;s=#999999" g="190,1352,610,40" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2"/>
<c id="p7_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1392,150,55" v="resolve／apply／--dry-run"/>
<c id="p7_tv4" st="f=#ffffff;s=#999999" g="190,1392,610,55" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"/>
<c id="p7_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1447,150,40" v="flock／指紋／進度日誌"/>
<c id="p7_tv5" st="f=#ffffff;s=#999999" g="190,1447,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"/>
<c id="p7_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1487,150,40" v="dev 覆寫／undev"/>
<c id="p7_tv6" st="f=#ffffff;s=#999999" g="190,1487,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋"/>
<c id="p7_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1527,150,40" v="materialize／印記"/>
<c id="p7_tv7" st="f=#ffffff;s=#999999" g="190,1527,610,40" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256"/>
<c id="p7_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1567,150,86" v="B／D／N、逐檔判斷後詢問"/>
<c id="p7_tv8" st="f=#ffffff;s=#999999" g="190,1567,610,86" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"/>
<c id="p7_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1217,150,71" v="metadata"/>
<c id="p7_tv9" st="f=#ffffff;s=#999999" g="990,1217,610,71" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"/>
<c id="p7_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1288,150,40" v="gen／mod?"/>
<c id="p7_tv10" st="f=#ffffff;s=#999999" g="990,1288,610,40" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它"/>
<c id="p7_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1328,150,55" v="git merge-file --diff3"/>
<c id="p7_tv11" st="f=#ffffff;s=#999999" g="990,1328,610,55" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1383,150,40" v="CRLF／append 行"/>
<c id="p7_tv12" st="f=#ffffff;s=#999999" g="990,1383,610,40" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p7_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1423,150,40" v="GHCR／image／tag@digest"/>
<c id="p7_tv13" st="f=#ffffff;s=#999999" g="990,1423,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）"/>
<c id="p7_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1463,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7_tv14" st="f=#ffffff;s=#999999" g="990,1463,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── B. 手動路徑（1）resolve → docker">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── B. 手動路徑（1）前置（§2、v2.2 C／D、v2.5 §2／§3／§6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,97,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,97,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,97,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,97,280,28" v="專案目錄"/>
<c id="uB" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1511" v="B. 手動路徑：just vendor_kit upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]（不帶 repo = 全部含 vendor_kit 自身，先完整預檢再動；@&amp;lt;tag&amp;gt; 限單一 repo）= resolve（不寫）→ 啟動器 docker；apply 前置見「B（1′）」頁、寫入段見「B（2）」頁"/>
<c id="uB_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="b0" parent="uB" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,102" v="just vendor_kit upgrade &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]（-y、--dry-run）"/>
<c id="b1" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,56,240,63" v="docker run &amp;lt;引擎&amp;gt; resolve upgrade &amp;lt;repo&amp;gt;&lt;br&gt;（啟動器不鎖）"/>
<c id="b1_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,46,30,20" v="v2"/>
<c id="b1x" parent="uB" st="ellipse;f=#ffe6cc;s=#000000" g="20,170,220,58" v="是 → 1：請先 undev &amp;lt;repo&amp;gt;"/>
<c id="b1x_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,160,30,20" v="v2"/>
<c id="b1q" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="720,158,280,81" v="&amp;lt;repo&amp;gt; 在 dev 覆寫中？"/>
<c id="b1q_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="976,148,30,20" v="v2"/>
<c id="b2c" parent="uB" st="ellipse;f=#ffe6cc;s=#000000" g="20,266,220,58" v="是 → 2：先解完衝突再重跑"/>
<c id="b2c_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,256,30,20" v="v2"/>
<c id="b2" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="720,270,360,50" v="(0) 衝突檔仍含我們的標籤？"/>
<c id="b2_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,260,30,20" v="v2"/>
<c id="b2n" parent="uB" st="shape=note;f=#ffffff;s=#999999" g="1300,259,280,73" v="標籤 = 我們自己產的 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建日誌之後（v2.5 §3）"/>
<c id="b5" parent="uB" st="ellipse;f=#ffe6cc;s=#000000" g="20,352,220,58" v="否 → 1：無 baseline，請先 add &amp;lt;repo&amp;gt;"/>
<c id="b4" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="730,356,340,50" v="有 baseline/&amp;lt;repo&amp;gt;/？"/>
<c id="b6" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="720,430,170,81" v="(1) 有待合併？"/>
<c id="b6_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,420,30,20" v="v2"/>
<c id="b6y" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="910,531,170,63" v="是：目標版 = B（version.toml 那版），補到就停，不查最新"/>
<c id="b6y_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,521,30,20" v="v2"/>
<c id="b7a" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="720,614,170,112" v="否 → @&amp;lt;tag&amp;gt; 指定？"/>
<c id="b7a_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,604,30,20" v="v2"/>
<c id="b7t" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="910,646,170,48" v="是：目標版 = @&amp;lt;tag&amp;gt;（比現版舊 → warn 仍執行）"/>
<c id="b7t_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,636,30,20" v="v2"/>
<c id="b7b" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="720,746,170,112" v="否 → CI 為真（frozen）？"/>
<c id="b7b_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,736,30,20" v="v2"/>
<c id="b7z" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="910,778,170,48" v="是：不查最新；目標版 = 鎖定版（無事可做）"/>
<c id="b7z_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,768,30,20" v="v2"/>
<c id="b7c" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="720,878,170,48" v="否：(2) 查 registry 最新正式版 = 目標版"/>
<c id="b7c_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,868,30,20" v="v2"/>
<c id="b7s" parent="uB" st="f=#dae8fc;s=#6c8ebf" g="720,946,360,63" v="resolve 完 → stdout：目標 tag@digest ＋ 輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）"/>
<c id="b7s_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,936,30,20" v="v2"/>
<c id="b8a" parent="uB" st="rhombus;f=#FFF4C3;s=#000000" g="460,1029,170,143" v="docker image inspect：本機有？"/>
<c id="b8a_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="606,1019,30,20" v="v2"/>
<c id="b8p" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="630,1192,70,63" v="無：docker pull"/>
<c id="b8p_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,1182,30,20" v="v2"/>
<c id="b8g" parent="uB" st="f=#e1d5e7;s=#9673a6" g="1100,1202,180,42" v="&amp;lt;repo&amp;gt;-dist&lt;br&gt;目標 tag@digest"/>
<c id="b8b" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,1275,240,40" v="docker create &amp;lt;img&amp;gt; /x"/>
<c id="b8b_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,1265,30,20" v="v2"/>
<c id="b8c" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,1335,240,48" v="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）"/>
<c id="b8c_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,1325,30,20" v="v2"/>
<c id="b8d" parent="uB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,1403,240,40" v="docker rm 該容器"/>
<c id="b8d_v2" parent="uB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,1393,30,20" v="v2"/>
<c id="b8z" parent="uB" st="text;s=none;f=none;b=1" g="460,1463,240,42" v="↓ 續「B（1′）」頁：docker run 引擎 apply upgrade → 前置檢查"/>
<c id="be1" edge source="b0" target="b1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be1q" edge source="b1" target="b1q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.06,0,," pts="600,289;880,289"/>
<c id="be1x" edge source="b1q" target="b1x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be2" edge source="b1q" target="b2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.16,0,," pts="880,390;920,390" v="否"/>
<c id="be3" edge source="b2" target="b2c" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be4" edge source="b2" target="b4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be5" edge source="b4" target="b5" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="be6" edge source="b4" target="b6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.03,0,," pts="920,561;825,561" v="是"/>
<c id="be7" edge source="b6" target="b6y" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.37,0,," pts="1015,612" v="是"/>
<c id="be8" edge source="b6" target="b7a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be8t" edge source="b7a" target="b7t" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be8b" edge source="b7a" target="b7b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be8z" edge source="b7b" target="b7z" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be8c" edge source="b7b" target="b7c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be9" edge source="b6y" target="b7s" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,704;1110,1077;1064,1077"/>
<c id="be9t" edge source="b7t" target="b7s" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,811;1110,1077;1064,1077"/>
<c id="be9z" edge source="b7z" target="b7s" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,943;1110,1077;1064,1077"/>
<c id="be10" edge source="b7c" target="b7s" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be11" edge source="b7s" target="b8a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="920,1160;565,1160"/>
<c id="be11n" edge source="b8a" target="b8p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.72,0,," pts="685,1242" v="無"/>
<c id="be12" edge source="b8g" target="b8p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="be11y" edge source="b8a" target="b8b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="be11p" edge source="b8p" target="b8b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be12c" edge source="b8b" target="b8c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be12d" edge source="b8c" target="b8d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be13" edge source="b8d" target="b8z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p7c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1668,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1668,140,64" v="黃：判斷"/>
<c id="p7c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1676,140,44" v="綠：起點／終點"/>
<c id="p7c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1670,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1670,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1678,88,40" v="白：步驟"/>
<c id="p7c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1678,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7c_lgt" st="text;s=none;f=none" g="1318,1668,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1736,120,36" v="便條：補充說明"/>
<c id="p7c_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1736,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1736,170,36" v="紫：image（引擎與工具）"/>
<c id="p7c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1736,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7c_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1736,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7c_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1726,30,20" v="v2"/>
<c id="p7c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1774,200,28" v="本頁名詞"/>
<c id="p7c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1808,150,40" v="Renovate／regex manager"/>
<c id="p7c_tv0" st="f=#ffffff;s=#999999" g="190,1808,610,40" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"/>
<c id="p7c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1848,150,40" v="PR／commit／push／rebase／merge"/>
<c id="p7c_tv1" st="f=#ffffff;s=#999999" g="190,1848,610,40" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"/>
<c id="p7c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1888,150,55" v="check.sh／CI 為真／frozen"/>
<c id="p7c_tv2" st="f=#ffffff;s=#999999" g="190,1888,610,55" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1943,150,40" v="baseline 落後／待合併"/>
<c id="p7c_tv3" st="f=#ffffff;s=#999999" g="190,1943,610,40" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2"/>
<c id="p7c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1983,150,55" v="resolve／apply／--dry-run"/>
<c id="p7c_tv4" st="f=#ffffff;s=#999999" g="190,1983,610,55" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"/>
<c id="p7c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2038,150,40" v="flock／指紋／進度日誌"/>
<c id="p7c_tv5" st="f=#ffffff;s=#999999" g="190,2038,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"/>
<c id="p7c_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2078,150,40" v="dev 覆寫／undev"/>
<c id="p7c_tv6" st="f=#ffffff;s=#999999" g="190,2078,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋"/>
<c id="p7c_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2118,150,40" v="materialize／印記"/>
<c id="p7c_tv7" st="f=#ffffff;s=#999999" g="190,2118,610,40" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256"/>
<c id="p7c_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2158,150,86" v="B／D／N、逐檔判斷後詢問"/>
<c id="p7c_tv8" st="f=#ffffff;s=#999999" g="190,2158,610,86" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"/>
<c id="p7c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1808,150,71" v="metadata"/>
<c id="p7c_tv9" st="f=#ffffff;s=#999999" g="990,1808,610,71" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"/>
<c id="p7c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1879,150,40" v="gen／mod?"/>
<c id="p7c_tv10" st="f=#ffffff;s=#999999" g="990,1879,610,40" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它"/>
<c id="p7c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1919,150,55" v="git merge-file --diff3"/>
<c id="p7c_tv11" st="f=#ffffff;s=#999999" g="990,1919,610,55" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7c_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1974,150,40" v="CRLF／append 行"/>
<c id="p7c_tv12" st="f=#ffffff;s=#999999" g="990,1974,610,40" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p7c_tk13" st="f=#ffffff;s=#999999;b=1" g="840,2014,150,40" v="GHCR／image／tag@digest"/>
<c id="p7c_tv13" st="f=#ffffff;s=#999999" g="990,2014,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）"/>
<c id="p7c_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2054,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7c_tv14" st="f=#ffffff;s=#999999" g="990,2054,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置（§2、v2.2 C／D、v2.5 §2／§3／§5、v2.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,97,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,97,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,97,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,97,280,28" v="專案目錄"/>
<c id="uB1" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,901" v="B（1′）apply 前置（承「B（1）」頁：目標版 image 已展開到暫存）：拿鎖 → 重驗指紋 → dest／命名空間檢查 → 逐檔判斷 → frozen → dry-run 分支；寫入段見「B（2）」頁"/>
<c id="uB1_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="b8e" parent="uB1" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="460,36,240,58" v="來自「B（1）」頁：目標版 /dist 已在主機暫存"/>
<c id="b9" parent="uB1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,114,240,63" v="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro &amp;lt;引擎&amp;gt; apply upgrade &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）"/>
<c id="b9_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="676,104,30,20" v="v2"/>
<c id="b10a" parent="uB1" st="f=#dae8fc;s=#6c8ebf" g="720,126,360,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="b10a_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,116,30,20" v="v2"/>
<c id="b10b" parent="uB1" st="f=#dae8fc;s=#6c8ebf" g="720,206,220,40" v="重驗 resolve 的輸入指紋"/>
<c id="b10b_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="916,196,30,20" v="v2"/>
<c id="b10x" parent="uB1" st="ellipse;f=#ffe6cc;s=#000000" g="950,197,130,58" v="不同 → 1「請重跑」"/>
<c id="b10x_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,187,30,20" v="v2"/>
<c id="b10dx" parent="uB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,311,220,40" v="否 → 1：dest 不合法"/>
<c id="b10dx_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,301,30,20" v="v2"/>
<c id="b10d" parent="uB1" st="rhombus;f=#FFF4C3;s=#000000" g="720,275,340,112" v="新版 init.toml 的 dest 全部合法？（任何寫入前；規則同「add（1）」頁）"/>
<c id="b10d_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1036,265,30,20" v="v2"/>
<c id="b10nx" parent="uB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,474,220,40" v="是 → 1：命名空間撞名"/>
<c id="b10nx_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,464,30,20" v="v2"/>
<c id="b10n" parent="uB1" st="rhombus;f=#FFF4C3;s=#000000" g="720,407,340,174" v="是 → 新版 just/&amp;lt;ns&amp;gt;.just 的 &amp;lt;ns&amp;gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）"/>
<c id="b10n_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1036,397,30,20" v="v2"/>
<c id="b10c" parent="uB1" st="f=#dae8fc;s=#6c8ebf" g="720,601,360,48" v="否 → 逐檔判斷（B baseline／D 現況／N = 暫存 /dist/&amp;lt;repo&amp;gt;，見「逐檔判斷」頁）→ 詢問清單"/>
<c id="b10c_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,591,30,20" v="v2"/>
<c id="b12x" parent="uB1" st="ellipse;f=#ffe6cc;s=#000000" g="20,669,220,102" v="是 → 1：印需改清單（frozen；請在本機 upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push）"/>
<c id="b12x_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,659,30,20" v="v2"/>
<c id="b12" parent="uB1" st="rhombus;f=#FFF4C3;s=#000000" g="720,680,340,81" v="CI 為真（frozen）且需改 tracked 檔？"/>
<c id="b12_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1036,670,30,20" v="v2"/>
<c id="b11y" parent="uB1" st="ellipse;f=#d5e8d4;s=#000000" g="20,791,220,58" v="是 → 0：唯讀預覽（印會問哪些檔）"/>
<c id="b11y_v2" parent="uB1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,781,30,20" v="v2"/>
<c id="b11" parent="uB1" st="rhombus;f=#FFF4C3;s=#000000" g="770,795,240,50" v="--dry-run？"/>
<c id="b11z" parent="uB1" st="text;s=none;f=none;b=1" g="720,869,300,26" v="否 ↓ 續「B（2）」頁：apply 寫入段"/>
<c id="be13e" edge source="b8e" target="b9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be14" edge source="b9" target="b10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be15" edge source="b10a" target="b10b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be15x" edge source="b10b" target="b10x" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be15b" edge source="b10b" target="b10d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be15d" edge source="b10d" target="b10dx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="be15n" edge source="b10d" target="b10n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="be15nx" edge source="b10n" target="b10nx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be15c" edge source="b10n" target="b10c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be15e" edge source="b10c" target="b12" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be16" edge source="b12" target="b12x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be17" edge source="b12" target="b11" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be18" edge source="b11" target="b11y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be19" edge source="b11" target="b11z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p7cp_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1058,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7cp_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1058,140,64" v="黃：判斷"/>
<c id="p7cp_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1066,140,44" v="綠：起點／終點"/>
<c id="p7cp_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1060,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7cp_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1060,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7cp_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1068,88,40" v="白：步驟"/>
<c id="p7cp_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1068,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7cp_lgt" st="text;s=none;f=none" g="1318,1058,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7cp_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1126,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p7cp_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1126,120,36" v="便條：補充說明"/>
<c id="p7cp_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1126,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7cp_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1126,170,36" v="紫：image（引擎與工具）"/>
<c id="p7cp_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1126,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7cp_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1126,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7cp_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1116,30,20" v="v2"/>
<c id="p7cp_th" st="text;fs=13;s=none;f=none;b=1" g="40,1164,200,28" v="本頁名詞"/>
<c id="p7cp_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1198,150,40" v="Renovate／regex manager"/>
<c id="p7cp_tv0" st="f=#ffffff;s=#999999" g="190,1198,610,40" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"/>
<c id="p7cp_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1238,150,40" v="PR／commit／push／rebase／merge"/>
<c id="p7cp_tv1" st="f=#ffffff;s=#999999" g="190,1238,610,40" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"/>
<c id="p7cp_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1278,150,55" v="check.sh／CI 為真／frozen"/>
<c id="p7cp_tv2" st="f=#ffffff;s=#999999" g="190,1278,610,55" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7cp_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1333,150,40" v="baseline 落後／待合併"/>
<c id="p7cp_tv3" st="f=#ffffff;s=#999999" g="190,1333,610,40" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2"/>
<c id="p7cp_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1373,150,55" v="resolve／apply／--dry-run"/>
<c id="p7cp_tv4" st="f=#ffffff;s=#999999" g="190,1373,610,55" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"/>
<c id="p7cp_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1428,150,40" v="flock／指紋／進度日誌"/>
<c id="p7cp_tv5" st="f=#ffffff;s=#999999" g="190,1428,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"/>
<c id="p7cp_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1468,150,40" v="dev 覆寫／undev"/>
<c id="p7cp_tv6" st="f=#ffffff;s=#999999" g="190,1468,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋"/>
<c id="p7cp_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1508,150,40" v="materialize／印記"/>
<c id="p7cp_tv7" st="f=#ffffff;s=#999999" g="190,1508,610,40" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256"/>
<c id="p7cp_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1548,150,86" v="B／D／N、逐檔判斷後詢問"/>
<c id="p7cp_tv8" st="f=#ffffff;s=#999999" g="190,1548,610,86" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"/>
<c id="p7cp_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1198,150,71" v="metadata"/>
<c id="p7cp_tv9" st="f=#ffffff;s=#999999" g="990,1198,610,71" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"/>
<c id="p7cp_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1269,150,40" v="gen／mod?"/>
<c id="p7cp_tv10" st="f=#ffffff;s=#999999" g="990,1269,610,40" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它"/>
<c id="p7cp_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1309,150,55" v="git merge-file --diff3"/>
<c id="p7cp_tv11" st="f=#ffffff;s=#999999" g="990,1309,610,55" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7cp_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1364,150,40" v="CRLF／append 行"/>
<c id="p7cp_tv12" st="f=#ffffff;s=#999999" g="990,1364,610,40" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p7cp_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1404,150,40" v="GHCR／image／tag@digest"/>
<c id="p7cp_tv13" st="f=#ffffff;s=#999999" g="990,1404,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）"/>
<c id="p7cp_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1444,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7cp_tv14" st="f=#ffffff;s=#999999" g="990,1444,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併（§5、v2.2 D、v2.5 §2～§4、v2.6 §8／Q14）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,97,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,97,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,97,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,97,280,28" v="專案目錄"/>
<c id="uB2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1603" v="B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔詢問（四種情況各一問）→ 暫存合併 → 解析檢查（失敗 → 留原檔、記 conflicts）→ 通過才原子替換（§4.3）；收尾見「B（2′）」頁"/>
<c id="uB2_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="b10z" parent="uB2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="750,36,300,58" v="來自「B（1′）」頁：apply 檢查通過（非 dry-run）"/>
<c id="b10e" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="720,114,360,48" v="建進度日誌（metadata state=in-progress；第一個寫入前）"/>
<c id="b10e_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,104,30,20" v="v2"/>
<c id="b10ef" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,117,280,42" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（state=in-progress）"/>
<c id="b10f" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="720,182,360,40" v="(0) 判定已解 → 清除 metadata 的衝突狀態（有的話）"/>
<c id="b10f_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,172,30,20" v="v2"/>
<c id="b10ff" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,182,280,40" v=".vendor_kit.toml（衝突中檔案清單清空）"/>
<c id="b13a" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="720,242,360,48" v="materialize 目標版：/dist/&amp;lt;repo&amp;gt; → 暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）"/>
<c id="b13a_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,232,30,20" v="v2"/>
<c id="b13f" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,246,280,40" v="cache/&amp;lt;repo&amp;gt;/（目標版，不進 git）"/>
<c id="b13b" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="720,310,360,48" v="寫印記 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）"/>
<c id="b13b_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,300,30,20" v="v2"/>
<c id="b13bf" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,314,280,40" v="gen/&amp;lt;repo&amp;gt;.stamp（不進 git）"/>
<c id="bl" parent="uB2" st="text;s=none;f=none;b=1" g="720,378,360,42" v="↓ 逐檔（每檔恰一種情況，依「逐檔判斷」頁；不是該情況就看下一格；-y 免問）"/>
<c id="b14q1" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="720,440,240,112" v="文字檔：你沒改、新版改了 → 問「X 換成新版？」"/>
<c id="b14q1_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,430,30,20" v="v2"/>
<c id="b14a" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,472,90,48" v="是：換新版（在暫存）"/>
<c id="b14a_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,462,30,20" v="v2"/>
<c id="b14q1b" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="720,572,240,174" v="二進位／symlink：你沒改、新版改了 → 問「X 是二進位檔，要換成新版嗎？」"/>
<c id="b14q1b_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,562,30,20" v="v2"/>
<c id="b14ab" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,635,90,48" v="是：換新版（在暫存）"/>
<c id="b14ab_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,625,30,20" v="v2"/>
<c id="b14q2" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="720,766,240,143" v="兩邊都改 → 問「你和新版都改了 X，要三方合併嗎？」"/>
<c id="b14q2_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,756,30,20" v="v2"/>
<c id="b14b" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,798,90,79" v="是：git merge-file --diff3（在暫存）"/>
<c id="b14b_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,788,30,20" v="v2"/>
<c id="b14q3" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="720,929,240,112" v="append 行找到上次插入的行 → 問「要替換嗎？」"/>
<c id="b14q3_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,919,30,20" v="v2"/>
<c id="b14c" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,954,90,63" v="是：append 行替換（在暫存）"/>
<c id="b14c_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,944,30,20" v="v2"/>
<c id="b14q4" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="720,1076,240,112" v="新版新增（B 無）→ 問「要建 X 嗎」"/>
<c id="b14q4_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1066,30,20" v="v2"/>
<c id="b14d" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1100,90,63" v="是：建新檔（已有同名 → 不納管）"/>
<c id="b14d_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,1090,30,20" v="v2"/>
<c id="b14r" parent="uB2" st="f=#ffe6cc;s=#d79b00;b=1" g="1300,1061,280,141" v="Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined 從未建立；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑（.github/workflows/、.gitlab-ci.yml）時訊息醒目"/>
<c id="b14r_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,1051,30,20" v="v2"/>
<c id="b14n" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="620,1222,280,63" v="否：不動該檔；已納管檔 state 不變只記 declined_hash，新檔被拒 → state=declined（新版再更新時再問）"/>
<c id="b14n_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="876,1212,30,20" v="v2"/>
<c id="b14m" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="720,1305,360,48" v="暫存合併完成（每檔已定：換新版／合併／替換／建新／不動；都還在暫存）→ TOML／just 等可解析格式先重新解析"/>
<c id="b14m_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,1295,30,20" v="v2"/>
<c id="b14pc" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="720,1373,90,94" v="是：留原檔、記 conflicts（baseline 不推）"/>
<c id="b14pc_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,1363,30,20" v="v2"/>
<c id="b14pq" parent="uB2" st="rhombus;f=#FFF4C3;s=#000000" g="840,1380,240,81" v="可解析格式：重新解析失敗？"/>
<c id="b14pq_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,1370,30,20" v="v2"/>
<c id="b14w" parent="uB2" st="f=#dae8fc;s=#6c8ebf" g="840,1487,240,48" v="否：通過的檔逐檔原子替換（暫存 → 正式位置）"/>
<c id="b14w_v2" parent="uB2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,1477,30,20" v="v2"/>
<c id="b14f" parent="uB2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,1490,280,42" v="初始檔（合併後；衝突留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記）"/>
<c id="b14z" parent="uB2" st="text;s=none;f=none;b=1" g="720,1555,360,42" v="↓ 續「B（2′）」頁：baseline（解析失敗的檔不推）→ metadata → tools.just → version.toml → 刪日誌"/>
<c id="be20" edge source="b10z" target="b10e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be20f" edge source="b10e" target="b10ef" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be20b" edge source="b10e" target="b10f" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be20ff" edge source="b10f" target="b10ff" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be21" edge source="b10f" target="b13a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be21f" edge source="b13a" target="b13f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be21b" edge source="b13a" target="b13b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be21bf" edge source="b13b" target="b13bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be22" edge source="b13b" target="bl" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22a" edge source="bl" target="b14q1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22y1" edge source="b14q1" target="b14a" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be22n1" edge source="b14q1" target="b14q1b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22x1" edge source="b14q1" target="b14n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.95,0,," pts="700,637" v="否"/>
<c id="be22y1b" edge source="b14q1b" target="b14ab" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be22n1b" edge source="b14q1b" target="b14q2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22x1b" edge source="b14q1b" target="b14n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.92,0,," pts="690,800" v="否"/>
<c id="be22y2" edge source="b14q2" target="b14b" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be22n2" edge source="b14q2" target="b14q3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22x2" edge source="b14q2" target="b14n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.87,0,," pts="680,978" v="否"/>
<c id="be22y3" edge source="b14q3" target="b14c" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be22n3" edge source="b14q3" target="b14q4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be22x3" edge source="b14q3" target="b14n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.77,0,," pts="670,1126" v="否"/>
<c id="be22y4" edge source="b14q4" target="b14d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be22x4" edge source="b14q4" target="b14n" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.53,0,," pts="660,1272" v="否"/>
<c id="be23a" edge source="b14a" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,637;1110,1436;1064,1436"/>
<c id="be23ab" edge source="b14ab" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,800;1110,1436;1064,1436"/>
<c id="be23b" edge source="b14b" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,978;1110,1436;1064,1436"/>
<c id="be23c" edge source="b14c" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,1126;1110,1436;1064,1436"/>
<c id="be23d" edge source="b14d" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1110,1272;1110,1436;1064,1436"/>
<c id="be23n" edge source="b14n" target="b14m" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be23m" edge source="b14m" target="b14pq" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be23pc" edge source="b14pq" target="b14pc" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="be23pw" edge source="b14pq" target="b14w" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="be22f" edge source="b14w" target="b14f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be23z" edge source="b14w" target="b14z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be23pz" edge source="b14pc" target="b14z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p7cc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1760,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7cc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1760,140,64" v="黃：判斷"/>
<c id="p7cc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1768,140,44" v="綠：起點／終點"/>
<c id="p7cc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1762,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7cc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1762,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7cc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1770,88,40" v="白：步驟"/>
<c id="p7cc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1770,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7cc_lgt" st="text;s=none;f=none" g="1318,1760,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7cc_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1828,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p7cc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1828,120,36" v="便條：補充說明"/>
<c id="p7cc_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,1828,150,36" v="橘框：規則（已定）"/>
<c id="p7cc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="570,1828,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7cc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="780,1828,170,36" v="紫：image（引擎與工具）"/>
<c id="p7cc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="970,1828,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7cc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1160,1828,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7cc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1336,1818,30,20" v="v2"/>
<c id="p7cc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1866,200,28" v="本頁名詞"/>
<c id="p7cc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1900,150,40" v="Renovate／regex manager"/>
<c id="p7cc_tv0" st="f=#ffffff;s=#999999" g="190,1900,610,40" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"/>
<c id="p7cc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1940,150,40" v="PR／commit／push／rebase／merge"/>
<c id="p7cc_tv1" st="f=#ffffff;s=#999999" g="190,1940,610,40" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"/>
<c id="p7cc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1980,150,55" v="check.sh／CI 為真／frozen"/>
<c id="p7cc_tv2" st="f=#ffffff;s=#999999" g="190,1980,610,55" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7cc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2035,150,40" v="baseline 落後／待合併"/>
<c id="p7cc_tv3" st="f=#ffffff;s=#999999" g="190,2035,610,40" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2"/>
<c id="p7cc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2075,150,55" v="resolve／apply／--dry-run"/>
<c id="p7cc_tv4" st="f=#ffffff;s=#999999" g="190,2075,610,55" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"/>
<c id="p7cc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2130,150,40" v="flock／指紋／進度日誌"/>
<c id="p7cc_tv5" st="f=#ffffff;s=#999999" g="190,2130,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"/>
<c id="p7cc_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2170,150,40" v="dev 覆寫／undev"/>
<c id="p7cc_tv6" st="f=#ffffff;s=#999999" g="190,2170,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋"/>
<c id="p7cc_tk7" st="f=#ffffff;s=#999999;b=1" g="40,2210,150,40" v="materialize／印記"/>
<c id="p7cc_tv7" st="f=#ffffff;s=#999999" g="190,2210,610,40" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256"/>
<c id="p7cc_tk8" st="f=#ffffff;s=#999999;b=1" g="40,2250,150,86" v="B／D／N、逐檔判斷後詢問"/>
<c id="p7cc_tv8" st="f=#ffffff;s=#999999" g="190,2250,610,86" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"/>
<c id="p7cc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1900,150,71" v="metadata"/>
<c id="p7cc_tv9" st="f=#ffffff;s=#999999" g="990,1900,610,71" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"/>
<c id="p7cc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1971,150,40" v="gen／mod?"/>
<c id="p7cc_tv10" st="f=#ffffff;s=#999999" g="990,1971,610,40" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它"/>
<c id="p7cc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2011,150,55" v="git merge-file --diff3"/>
<c id="p7cc_tv11" st="f=#ffffff;s=#999999" g="990,2011,610,55" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7cc_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2066,150,40" v="CRLF／append 行"/>
<c id="p7cc_tv12" st="f=#ffffff;s=#999999" g="990,2066,610,40" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p7cc_tk13" st="f=#ffffff;s=#999999;b=1" g="840,2106,150,40" v="GHCR／image／tag@digest"/>
<c id="p7cc_tv13" st="f=#ffffff;s=#999999" g="990,2106,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）"/>
<c id="p7cc_tk14" st="f=#ffffff;s=#999999;b=1" g="840,2146,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7cc_tv14" st="f=#ffffff;s=#999999" g="990,2146,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入（§5、v2.2 D、v2.5 §3／§4、v2.6 Q27）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,97,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,97,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,97,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,97,280,28" v="專案目錄"/>
<c id="uB3" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,816" v="B（2′）apply 寫入段後半（承「B（2）」頁：通過解析的檔已替換；解析失敗的檔留原檔、已記 conflicts）：推 baseline（解析失敗的檔不推）→ metadata（版本／conflicts；state／lines）→ 重生 tools.just → 寫 version.toml → 刪日誌 → 0／2"/>
<c id="uB3_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="b15z" parent="uB3" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="750,36,300,80" v="來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原檔、已記 conflicts"/>
<c id="b15a" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,136,360,63" v="推 baseline/&amp;lt;repo&amp;gt;/ 到目標版：逐檔，通過的檔推到 N（有衝突標記也推）；解析失敗的檔跳過不推（該檔 baseline 留上一版；v2.9 §4）"/>
<c id="b15a_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,126,30,20" v="v2"/>
<c id="b15f" parent="uB3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,146,280,42" v="baseline/&amp;lt;repo&amp;gt;/（目標版範本副本，進 git；解析失敗的檔留上一版）"/>
<c id="b15b" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,219,360,48" v="寫 metadata：最後合併版本 = 目標版、衝突中檔案（conflicts）"/>
<c id="b15b_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,209,30,20" v="v2"/>
<c id="b15bf" parent="uB3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,222,280,42" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml（進 git）"/>
<c id="b15d" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,287,360,63" v="寫 metadata：每個 dest 的 state／declined_hash／append 行（lines）—— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined"/>
<c id="b15d_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,277,30,20" v="v2"/>
<c id="b15df" parent="uB3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,298,280,42" v=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）"/>
<c id="b15g" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,370,360,48" v="重生 gen/tools.just（新版的 just/&amp;lt;ns&amp;gt;.just 可能增減；每個一行 mod?）"/>
<c id="b15g_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,360,30,20" v="v2"/>
<c id="b15gf" parent="uB3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,374,280,40" v="gen/tools.just（不進 git；mod? 行）"/>
<c id="b16" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,438,360,48" v="寫 version.toml &amp;lt;repo&amp;gt; 行 → 目標 tag@digest（待合併：已是 B，不動）"/>
<c id="b16_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,428,30,20" v="v2"/>
<c id="b16f" parent="uB3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,442,280,40" v="version.toml（&amp;lt;repo&amp;gt; 行，進 git）"/>
<c id="b16x" parent="uB3" st="ellipse;f=#f8cecc;s=#000000" g="20,506,220,58" v="失敗 → 1：明列已完成／未完成"/>
<c id="b16x_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,496,30,20" v="v2"/>
<c id="b16b" parent="uB3" st="f=#dae8fc;s=#6c8ebf" g="720,515,360,40" v="刪進度日誌（最後一步）"/>
<c id="b16b_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1056,505,30,20" v="v2"/>
<c id="b17" parent="uB3" st="ellipse;f=#d5e8d4;s=#000000" g="20,611,220,58" v="否 → 0：印摘要 → commit"/>
<c id="b17_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,601,30,20" v="v2"/>
<c id="b16q" parent="uB3" st="rhombus;f=#FFF4C3;s=#000000" g="720,584,240,112" v="有衝突（conflicts 非空）？"/>
<c id="b16q_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,574,30,20" v="v2"/>
<c id="b18" parent="uB3" st="ellipse;f=#ffe6cc;s=#000000" g="720,723,360,80" v="是 → 2：印衝突檔名（含解析失敗的檔；解完再跑直到乾淨；baseline 已在目標版，除解析失敗檔外）"/>
<c id="b18r" parent="uB3" st="f=#ffe6cc;s=#d79b00;b=1" g="1300,716,280,94" v="多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；訊息全列；待合併補完後另有新版 → 印「已補齊 &amp;lt;repo&amp;gt; 至 vB；另有新版 vX，再跑一次可升」"/>
<c id="b18r_v2" parent="uB3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,706,30,20" v="v2"/>
<c id="be23" edge source="b15z" target="b15a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be24" edge source="b15a" target="b15f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be24b" edge source="b15a" target="b15b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be24bf" edge source="b15b" target="b15bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be24d" edge source="b15b" target="b15d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be24df" edge source="b15d" target="b15df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be25" edge source="b15d" target="b15g" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be25f" edge source="b15g" target="b15gf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be25g" edge source="b15g" target="b16" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be27" edge source="b16" target="b16f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="be26" edge source="b16" target="b16b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="成功"/>
<c id="be26x" edge source="b16" target="b16x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="812,637;150,637" v="失敗"/>
<c id="be28q" edge source="b16b" target="b16q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="be28" edge source="b16q" target="b17" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="be29" edge source="b16q" target="b18" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="p7cq_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,973,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7cq_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,973,140,64" v="黃：判斷"/>
<c id="p7cq_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,981,140,44" v="綠：起點／終點"/>
<c id="p7cq_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,975,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7cq_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,975,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7cq_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,983,88,40" v="白：步驟"/>
<c id="p7cq_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,983,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7cq_lgt" st="text;s=none;f=none" g="1318,973,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7cq_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1041,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p7cq_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1041,120,36" v="便條：補充說明"/>
<c id="p7cq_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,1041,150,36" v="橘框：規則（已定）"/>
<c id="p7cq_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="570,1041,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7cq_lgx_img" st="f=#e1d5e7;s=#9673a6" g="780,1041,170,36" v="紫：image（引擎與工具）"/>
<c id="p7cq_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="970,1041,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7cq_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1160,1041,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7cq_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1336,1031,30,20" v="v2"/>
<c id="p7cq_th" st="text;fs=13;s=none;f=none;b=1" g="40,1079,200,28" v="本頁名詞"/>
<c id="p7cq_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1113,150,40" v="Renovate／regex manager"/>
<c id="p7cq_tv0" st="f=#ffffff;s=#999999" g="190,1113,610,40" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行"/>
<c id="p7cq_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1153,150,40" v="PR／commit／push／rebase／merge"/>
<c id="p7cq_tv1" st="f=#ffffff;s=#999999" g="190,1153,610,40" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線"/>
<c id="p7cq_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1193,150,55" v="check.sh／CI 為真／frozen"/>
<c id="p7cq_tv2" st="f=#ffffff;s=#999999" g="190,1193,610,55" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7cq_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1248,150,40" v="baseline 落後／待合併"/>
<c id="p7cq_tv3" st="f=#ffffff;s=#999999" g="190,1248,610,40" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2"/>
<c id="p7cq_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1288,150,55" v="resolve／apply／--dry-run"/>
<c id="p7cq_tv4" st="f=#ffffff;s=#999999" g="190,1288,610,55" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）"/>
<c id="p7cq_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1343,150,40" v="flock／指紋／進度日誌"/>
<c id="p7cq_tv5" st="f=#ffffff;s=#999999" g="190,1343,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪"/>
<c id="p7cq_tk6" st="f=#ffffff;s=#999999;b=1" g="40,1383,150,40" v="dev 覆寫／undev"/>
<c id="p7cq_tv6" st="f=#ffffff;s=#999999" g="190,1383,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋"/>
<c id="p7cq_tk7" st="f=#ffffff;s=#999999;b=1" g="40,1423,150,40" v="materialize／印記"/>
<c id="p7cq_tv7" st="f=#ffffff;s=#999999" g="190,1423,610,40" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&amp;lt;repo&amp;gt; 展開到 cache/&amp;lt;repo&amp;gt;/（暫存 → 原子替換）；印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 index digest，之後每檔 sha256"/>
<c id="p7cq_tk8" st="f=#ffffff;s=#999999;b=1" g="40,1463,150,86" v="B／D／N、逐檔判斷後詢問"/>
<c id="p7cq_tv8" st="f=#ffffff;s=#999999" g="190,1463,610,86" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁"/>
<c id="p7cq_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1113,150,71" v="metadata"/>
<c id="p7cq_tv9" st="f=#ffffff;s=#999999" g="990,1113,610,71" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"/>
<c id="p7cq_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1184,150,40" v="gen／mod?"/>
<c id="p7cq_tv10" st="f=#ffffff;s=#999999" g="990,1184,610,40" v="gen/tools.just（不進 git）每個 &amp;lt;ns&amp;gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &amp;lt;ns&amp;gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它"/>
<c id="p7cq_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1224,150,55" v="git merge-file --diff3"/>
<c id="p7cq_tv11" st="f=#ffffff;s=#999999" g="990,1224,610,55" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7cq_tk12" st="f=#ffffff;s=#999999;b=1" g="840,1279,150,40" v="CRLF／append 行"/>
<c id="p7cq_tv12" st="f=#ffffff;s=#999999" g="990,1279,610,40" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn"/>
<c id="p7cq_tk13" st="f=#ffffff;s=#999999;b=1" g="840,1319,150,40" v="GHCR／image／tag@digest"/>
<c id="p7cq_tv13" st="f=#ffffff;s=#999999" g="990,1319,610,40" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）"/>
<c id="p7cq_tk14" st="f=#ffffff;s=#999999;b=1" g="840,1359,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7cq_tv14" st="f=#ffffff;s=#999999" g="990,1359,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── 逐檔判斷、衝突重入、回退">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── C. 逐檔判斷表、C′ 衝突重入、D. 回退（§5、v2.2 D、v2.3 §1、v2.5 §1／§2／§4）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,61" v="已定（v2.3 §1）：append 行比對 CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.2 E）：dist/files/ 第一版禁止 symlink。已定（v2.5 §2）：N 讀暫存 /dist/&amp;lt;repo&amp;gt;，materialize 在決定套用之後。自身升級見「E. 自身升級」頁。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,81,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,81,180,28" v="Renovate（GitHub 上）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="480,81,240,28" v="啟動器（主機 sh）"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="740,81,360,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1120,81,180,28" v="GHCR"/>
<c id="hdr5" st="f=#e6e6e6;s=#999999;b=1" g="1320,81,280,28" v="專案目錄"/>
<c id="uC" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,125,1600,905" v="C. 逐檔判斷後詢問（每個 init.toml 檔；引擎 merge 模組；§5 表；在 apply 內、拿到 flock、建日誌後）＋ C′ 衝突重入（v2.2 D (0)、v2.5 §3）"/>
<c id="uC_v2" parent="uC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="c_in0" parent="uC" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,50,280,42" v="B = baseline/&amp;lt;repo&amp;gt;/&amp;lt;檔&amp;gt;（上次合併的範本）"/>
<c id="c_in1" parent="uC" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,106,280,40" v="D = 專案裡的 &amp;lt;檔&amp;gt;（現況，你可能改過）"/>
<c id="c_in2" parent="uC" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,162,280,42" v="N = 目標版範本：暫存 /dist/&amp;lt;repo&amp;gt;/&amp;lt;檔&amp;gt;（不是 cache）"/>
<c id="c_in2_v2" parent="uC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,152,30,20" v="v2"/>
<c id="c_m" parent="uC" st="f=#dae8fc;s=#6c8ebf" g="730,54,340,60" v="引擎 merge 模組：三份比對，逐檔判斷（左表）→ 要改的先問（-y 免問；拒絕 → 不動、記 declined_hash；新檔才 state=declined）"/>
<c id="c_h0" parent="uC" st="f=#e6e6e6;s=#999999;b=1" g="20,70,170,28" v="情況"/>
<c id="c_h1" parent="uC" st="f=#e6e6e6;s=#999999;b=1" g="190,70,290,28" v="做法"/>
<c id="c_h2" parent="uC" st="f=#e6e6e6;s=#999999;b=1" g="480,70,230,28" v="結果"/>
<c id="c_r0c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,98,170,44" v="新版沒改／你的檔已等於新版（N==B 或 D==N）"/>
<c id="c_r0c1" parent="uC" st="f=#ffffff;s=#999999" g="190,98,290,44" v="不動"/>
<c id="c_r0c2" parent="uC" st="f=#ffffff;s=#999999" g="480,98,230,44" v="—"/>
<c id="c_r1c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,142,170,40" v="你刪了已納管的檔（D 缺）"/>
<c id="c_r1c1" parent="uC" st="f=#ffffff;s=#999999" g="190,142,290,40" v="不問、不重建"/>
<c id="c_r1c2" parent="uC" st="f=#ffffff;s=#999999" g="480,142,230,40" v="state=deleted，維持刪除（§4.3）"/>
<c id="c_r2c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,182,170,59" v="新版改了、你沒改（D==B、N≠B）"/>
<c id="c_r2c1" parent="uC" st="f=#ffffff;s=#999999" g="190,182,290,59" v="問「X 換成新版？」"/>
<c id="c_r2c2" parent="uC" st="f=#ffffff;s=#999999" g="480,182,230,59" v="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（目標新版再次更新時再問）"/>
<c id="c_r3c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,241,170,122" v="兩邊都改（D≠B、N≠B）"/>
<c id="c_r3c1" parent="uC" st="f=#ffffff;s=#999999" g="190,241,290,122" v="問「你和新版都改了 X，要三方合併嗎？」"/>
<c id="c_r3c2" parent="uC" st="f=#ffffff;s=#999999" g="480,241,230,122" v="同意 → git merge-file --diff3（在暫存做）：乾淨 → 原子替換寫入；衝突 → 留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、回 2；baseline 仍推到目標版；解完重跑直到乾淨；拒絕 → 不動、state 不變只記 declined_hash"/>
<c id="c_r4c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,363,170,106" v="新版新增（B 無）"/>
<c id="c_r4c1" parent="uC" st="f=#ffffff;s=#999999" g="190,363,290,106" v="問「要建 X 嗎」（-y 建）；已有同名 → 不納管；dest 在 CI 路徑時訊息醒目"/>
<c id="c_r4c2" parent="uC" st="f=#ffffff;s=#999999" g="480,363,230,106" v="拒絕 → 不建、state=declined（唯一會用 declined 的情況；之後不再問；目標新版再次更新時重新詢問；dry-run／check.sh 印「有 N 個範本你拒絕過」）；不覆蓋、印「已存在，範本在 cache」"/>
<c id="c_r5c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,469,170,40" v="新版刪除該檔（N 無）"/>
<c id="c_r5c1" parent="uC" st="f=#ffffff;s=#999999" g="190,469,290,40" v="不刪，只 warn"/>
<c id="c_r5c2" parent="uC" st="f=#ffffff;s=#999999" g="480,469,230,40" v="你的檔留著"/>
<c id="c_r6c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,509,170,75" v="append 行（strategy=append）"/>
<c id="c_r6c1" parent="uC" st="f=#ffffff;s=#999999" g="190,509,290,75" v="找到上次插入的行（CRLF／LF 視為相同，其餘精確）→ 問後替換"/>
<c id="c_r6c2" parent="uC" st="f=#ffffff;s=#999999" g="480,509,230,75" v="唯一命中 → 替換；零命中或多處 → 保留只 warn、印新內容；拒絕 → 不動、state 維持 appended 只記 declined_hash"/>
<c id="c_r7c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,584,170,59" v="二進位／symlink"/>
<c id="c_r7c1" parent="uC" st="f=#ffffff;s=#999999" g="190,584,290,59" v="不合併：你未改（D==B）→ 問「X 是二進位檔，要換成新版嗎？」（-y 免問）"/>
<c id="c_r7c2" parent="uC" st="f=#ffffff;s=#999999" g="480,584,230,59" v="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（新版再更新時再問）；改過 → 保留 + warn"/>
<c id="c_r8c0" parent="uC" st="f=#ffffff;s=#999999;b=1" g="20,643,170,59" v="CI 為真（frozen）且需改 tracked 檔"/>
<c id="c_r8c1" parent="uC" st="f=#ffffff;s=#999999" g="190,643,290,59" v="apply 印清單 → 1（version.toml 未動；-y 不解除 frozen）"/>
<c id="c_r8c2" parent="uC" st="f=#ffffff;s=#999999" g="480,643,230,59" v="--dry-run 也一樣：CI 為真且需改 tracked 檔 → 1；本機 → 0 只印清單"/>
<c id="c_note" parent="uC" st="shape=note;f=#ffffff;s=#999999" g="1300,218,280,73" v="--dry-run = 唯讀預覽，只印會問哪些檔。衝突解完 → 再跑一次 upgrade 直到乾淨（2 = 需要人解衝突，橙）。dest 撞名規則見「add（1）」頁；四種詢問各一格見「B（2）」頁。"/>
<c id="cx_l" parent="uC" st="text;s=none;f=none;b=1" g="20,732,700,26" v="C′ 衝突重入（解完衝突後再跑 upgrade；v2.2 D (0)）—— 偵測在 resolve，清除在 apply（拿鎖、建日誌後）"/>
<c id="cx0" parent="uC" st="ellipse;f=#d5e8d4;s=#000000" g="20,772.0,220,58" v="解完衝突後再跑 upgrade &amp;lt;repo&amp;gt;"/>
<c id="cx1" parent="uC" st="rhombus;f=#FFF4C3;s=#000000" g="730,776.0,340,50" v="衝突檔仍含我們的標籤？"/>
<c id="cx1_v2" parent="uC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1046,766,30,20" v="v2"/>
<c id="cx2" parent="uC" st="ellipse;f=#ffe6cc;s=#000000" g="1100,772.0,200,58" v="是 → 2：停（先解完標記再重跑）"/>
<c id="cx3" parent="uC" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="730,842,340,57" v="否：apply 拿鎖、建日誌後清除衝突狀態 → 接「B. 手動路徑（1）」頁的 (1)(2)（version.toml、baseline 已在目標版 → 通常「不動」）"/>
<c id="cx3_v2" parent="uC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1046,832,30,20" v="v2"/>
<c id="c_e0" edge source="c_in0" target="c_m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1296,195;1296,209"/>
<c id="c_e1" edge source="c_in1" target="c_m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1296,251;1296,209"/>
<c id="c_e2" edge source="c_in2" target="c_m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1296,307;1296,209"/>
<c id="c_e3" edge source="c_m" target="c_h2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="cx_e0" edge source="cx0" target="cx1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="cx_e1" edge source="cx1" target="cx2" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="cx_e2" edge source="cx1" target="cx3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.40,0,," v="否"/>
<c id="uD" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,1046,1600,615" v="D. 回退 ＝ git revert 該升級 commit（version.toml + 初始檔 + baseline 同一 commit）；下次 just 的 sync 只把 cache/ 換回舊版"/>
<c id="d0" parent="uD" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,58" v="git revert 該升級 commit"/>
<c id="d1a" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,44,240,42" v="下次 just：docker run 引擎 resolve sync"/>
<c id="d2" parent="uD" st="f=#dae8fc;s=#6c8ebf" g="720,36,360,57" v="sync resolve：gen/&amp;lt;repo&amp;gt;.stamp 第一行 ≠ version.toml 鎖定 digest → 待辦「materialize 舊版」"/>
<c id="d3b" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="20,172,220,57" v="初始檔、baseline/&amp;lt;repo&amp;gt;/、version.toml（由 git revert 還原，不是 sync 寫）"/>
<c id="d1b" parent="uD" st="rhombus;f=#FFF4C3;s=#000000" g="460,114,170,174" v="docker image inspect：舊版本機有？"/>
<c id="d1p" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="630,308,70,57" v="無：docker pull"/>
<c id="d1g" parent="uD" st="f=#e1d5e7;s=#9673a6" g="1100,308,180,57" v="&amp;lt;repo&amp;gt;-dist@digest&lt;br&gt;（version.toml 還原後的舊版）"/>
<c id="d1c" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,385,240,40" v="docker create &amp;lt;img&amp;gt; /x"/>
<c id="d1d" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,445,240,42" v="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/"/>
<c id="d1e" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,507,240,40" v="docker rm 該容器"/>
<c id="d1f" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="460,567,240,42" v="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro 引擎 apply sync"/>
<c id="d2c" parent="uD" st="f=#dae8fc;s=#6c8ebf" g="720,567,360,42" v="materialize 舊版 → cache/&amp;lt;repo&amp;gt;/、寫印記（只寫 cache/、gen/；初始檔與 baseline 不碰）"/>
<c id="d3" parent="uD" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1300,567,280,42" v="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp（舊版；sync 寫）"/>
<c id="de1" edge source="d0" target="d1a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2" edge source="d1a" target="d2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2b" edge source="d2" target="d1b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="920,1150;565,1150"/>
<c id="de2n" edge source="d1b" target="d1p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.75,0,," pts="685,1247" v="無"/>
<c id="de2g" edge source="d1g" target="d1p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="de2y" edge source="d1b" target="d1c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="de2p" edge source="d1p" target="d1c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2d" edge source="d1c" target="d1d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2e" edge source="d1d" target="d1e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2f" edge source="d1e" target="d1f" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2h" edge source="d1f" target="d2c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de3" edge source="d2c" target="d3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="de4" edge source="d0" target="d3b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p7b_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1677,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7b_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1677,140,64" v="黃：判斷"/>
<c id="p7b_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1685,140,44" v="綠：起點／終點"/>
<c id="p7b_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1679,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7b_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1679,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7b_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1687,88,40" v="白：步驟"/>
<c id="p7b_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1687,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7b_lgt" st="text;s=none;f=none" g="1318,1677,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7b_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1745,120,36" v="便條：補充說明"/>
<c id="p7b_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1745,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7b_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1745,170,36" v="紫：image（引擎與工具）"/>
<c id="p7b_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1745,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7b_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1745,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7b_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1735,30,20" v="v2"/>
<c id="p7b_th" st="text;fs=13;s=none;f=none;b=1" g="40,1783,200,28" v="本頁名詞"/>
<c id="p7b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1817,150,55" v="B／D／N"/>
<c id="p7b_tv0" st="f=#ffffff;s=#999999" g="190,1817,610,55" v="B = baseline（上次合併時的範本副本，進 git）；D = 現況（專案裡你的那份檔）；N = 目標版範本 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/&amp;lt;repo&amp;gt;（不是 cache；v2.5 §2）；「D==B」= 你沒改過"/>
<c id="p7b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1872,150,71" v="逐檔判斷後詢問／apply"/>
<c id="p7b_tv1" st="f=#ffffff;s=#999999" g="190,1872,610,71" v="apply = 動詞的第二段（拿到 flock、重驗指紋、建日誌後才寫檔）；三份比：N 改了才問「換成新版？」，兩邊都改才問「三方合併？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash，新檔（B 無）被拒才 state=declined；全部在暫存完成再逐檔原子替換；materialize 到 cache 在決定套用之後"/>
<c id="p7b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1943,150,40" v="resolve／apply"/>
<c id="p7b_tv2" st="f=#ffffff;s=#999999" g="190,1943,610,40" v="同一動詞兩段：resolve 只讀只算（查目標版、輸出要拉的 image 與輸入指紋，不寫檔）→ 啟動器 docker 拉 image、展開到暫存 → apply 拿 flock 後重驗指紋才寫"/>
<c id="p7b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1983,150,40" v="flock／指紋"/>
<c id="p7b_tv3" st="f=#ffffff;s=#999999" g="190,1983,610,40" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」"/>
<c id="p7b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2023,150,55" v="metadata"/>
<c id="p7b_tv4" st="f=#ffffff;s=#999999" g="190,2023,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行、衝突中檔案清單、進度日誌 state；衝突重入靠它的「衝突中檔案」清單"/>
<c id="p7b_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2078,150,40" v="git merge-file --diff3"/>
<c id="p7b_tv5" st="f=#ffffff;s=#999999" g="190,2078,610,40" v="git 的三方合併指令；衝突時在檔內留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline ||||||| ======= &amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt;&amp;gt; 標記（我們自己的標籤）；回傳衝突數 → 映射為結束狀態 2"/>
<c id="p7b_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2118,150,40" v="衝突重入（v2.2 D (0)）"/>
<c id="p7b_tv6" st="f=#ffffff;s=#999999" g="190,2118,610,40" v="再跑 upgrade 時 resolve 先看 metadata 的「衝突中檔案」：檔內仍有我們的標籤 → 2 停；檔案失蹤不算已解；都乾淨 → apply 拿鎖、建日誌後清除狀態再往下"/>
<c id="p7b_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1817,150,55" v="--dry-run／CI 為真"/>
<c id="p7b_tv7" st="f=#ffffff;s=#999999" g="990,1817,610,55" v="apply --dry-run 唯讀預覽：只印會問哪些檔（哪些要換／合併／append 替換；讀 /dist/&amp;lt;repo&amp;gt;），不動任何檔；本機 → 0；CI 為真（CI 非空且不為 0／false = frozen）且需改 tracked 檔 → 1（-y 不解除）"/>
<c id="p7b_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1872,150,40" v="append 行／CRLF"/>
<c id="p7b_tv8" st="f=#ffffff;s=#999999" g="990,1872,610,40" v="strategy=append 的初始檔：upgrade 找上次插入的行（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）→ 問後替換；零命中或多處 → 保留只 warn"/>
<c id="p7b_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1912,150,55" v="二進位／symlink"/>
<c id="p7b_tv9" st="f=#ffffff;s=#999999" g="990,1912,610,55" v="二進位 = 不是文字的檔（圖片等）；symlink = 指向另一個路徑的捷徑；兩者不做行內合併：你沒改 → 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過保留 + warn；dist/files/ 第一版禁止 symlink"/>
<c id="p7b_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1967,150,40" v="回退／git revert"/>
<c id="p7b_tv10" st="f=#ffffff;s=#999999" g="990,1967,610,40" v="git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、baseline 同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 只把 cache/&amp;lt;repo&amp;gt;/ 換回舊版"/>
<c id="p7b_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2007,150,71" v="GHCR／image／印記／declined／declined_hash"/>
<c id="p7b_tv11" st="f=#ffffff;s=#999999" g="990,2007,610,71" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；印記 = gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（= 被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）"/>
<c id="p7b_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2078,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7b_tv12" st="f=#ffffff;s=#999999" g="990,2078,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── E. 自身升級 (a)(b)">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── E. vendor_kit 自身升級 (a)(b)（v2.2 A／B、v2.3 §2、v2.5 §7、v2.6 §5）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,124" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,144,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,144,320,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="620,144,380,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1020,144,200,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,144,360,28" v="專案目錄"/>
<c id="uE" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,188,1600,1565" v="E. vendor_kit 自身升級（v2.3 §2 統一版、v2.5 §7、v2.6 §5）：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit 見「E(c)」頁；install 修復也走同樣比對"/>
<c id="uE_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="s0" parent="uE" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="(a) upgrade 不帶 repo（含 vendor_kit 自身）"/>
<c id="s0_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,26,30,20" v="v2"/>
<c id="s1" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="280,52,280,48" v="docker run 舊引擎 resolve upgrade（全部）"/>
<c id="s1_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="536,42,30,20" v="v2"/>
<c id="s2a" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,56,360,40" v="resolve：先完整預檢（含 dev 中工具 → 1 提示 undev）"/>
<c id="s2a_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,46,30,20" v="v2"/>
<c id="s2n" parent="uE" st="ellipse;f=#d5e8d4;s=#000000" g="20,136,220,80" v="否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）"/>
<c id="s2n_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,126,30,20" v="v2"/>
<c id="s2q" parent="uE" st="rhombus;f=#FFF4C3;s=#000000" g="600,151,240,50" v="引擎有新版？"/>
<c id="s2q_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="816,141,30,20" v="v2"/>
<c id="s2b" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,236,360,40" v="是：apply（舊引擎）：flock 專案目錄"/>
<c id="s2b_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,226,30,20" v="v2"/>
<c id="s2c" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,296,360,40" v="重驗指紋（不同 → 1「請重跑」，橙）"/>
<c id="s2c_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,286,30,20" v="v2"/>
<c id="s2d" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,356,360,40" v="建進度日誌（第一個寫入前）"/>
<c id="s2d_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,346,30,20" v="v2"/>
<c id="s2e" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,416,360,48" v="只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令）"/>
<c id="s2e_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,406,30,20" v="v2"/>
<c id="s2f" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1260,420,280,40" v="version.toml 第一行 = 新引擎 ref"/>
<c id="s2g" parent="uE" st="f=#dae8fc;s=#6c8ebf" g="610,484,360,40" v="刪進度日誌（最後一步）"/>
<c id="s2g_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,474,30,20" v="v2"/>
<c id="s2h" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="280,544,280,63" v="apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）"/>
<c id="s2h_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="536,534,30,20" v="v2"/>
<c id="s2hx" parent="uE" st="ellipse;f=#f8cecc;s=#000000" g="20,628,220,80" v="否 → 1：apply 未改第一行（印 apply 的錯誤）"/>
<c id="s2hx_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,618,30,20" v="v2"/>
<c id="s2h2" parent="uE" st="rhombus;f=#FFF4C3;s=#000000" g="300,627,240,81" v="第一行變了且 == 計畫的 engine？"/>
<c id="s2h2_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,617,30,20" v="v2"/>
<c id="s2ln" parent="uE" st="rhombus;f=#FFF4C3;s=#000000" g="310,728,220,112" v="是 → docker image inspect：本機有？"/>
<c id="s2ln_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="506,718,30,20" v="v2"/>
<c id="s2lp" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="500,860,80,79" v="無：docker pull 新引擎"/>
<c id="s2lp_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="556,850,30,20" v="v2"/>
<c id="s2gi" parent="uE" st="f=#e1d5e7;s=#9673a6" g="1000,878,200,42" v="vendor_kit:vY&lt;br&gt;（新引擎）"/>
<c id="s2lv" parent="uE" st="rhombus;f=#FFF4C3;s=#000000" g="310,959,220,112" v="覆寫中且 .Id ≠ 記的 image ID？"/>
<c id="s2lv_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="506,949,30,20" v="v2"/>
<c id="s2lx" parent="uE" st="ellipse;f=#f8cecc;s=#000000" g="600,975,240,80" v="拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 &amp;lt;vY&amp;gt;，薄殼尚未重產）"/>
<c id="s2lx_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="816,965,30,20" v="v2"/>
<c id="s4" parent="uE" st="ellipse;f=#d5e8d4;s=#000000" g="20,1091,220,146" v="→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）"/>
<c id="s4_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1081,30,20" v="v2"/>
<c id="s2r" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1144,320,40" v="docker run 新引擎 upgrade vendor_kit"/>
<c id="s2r_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="556,1134,30,20" v="v2"/>
<c id="s5" parent="uE" st="ellipse;f=#d5e8d4;s=#000000" g="20,1257,220,58" v="(b) 別人 pull 後（第一行已變）打任何 just"/>
<c id="s5_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1247,30,20" v="v2"/>
<c id="s6a" parent="uE" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="280,1266,280,40" v="啟動器：grep version.toml 第一行"/>
<c id="s6a_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="536,1256,30,20" v="v2"/>
<c id="s8" parent="uE" st="ellipse;f=#ffe6cc;s=#000000" g="20,1335,220,146" v="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）"/>
<c id="s8_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1325,30,20" v="v2"/>
<c id="s6q" parent="uE" st="rhombus;f=#FFF4C3;s=#000000" g="300,1352,240,112" v="gen/.stamp 的引擎 ref == 第一行？"/>
<c id="s6q_v2" parent="uE" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,1342,30,20" v="v2"/>
<c id="s6y" parent="uE" st="ellipse;f=#d5e8d4;s=#000000" g="300,1501,240,58" v="是 → 正常跑（「sync（1）」頁）"/>
<c id="se1" edge source="s0" target="s1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se2" edge source="s1" target="s2a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se2q" edge source="s2a" target="s2q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se2n" edge source="s2q" target="s2n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="se3" edge source="s2q" target="s2b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="se3c" edge source="s2b" target="s2c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se3d" edge source="s2c" target="s2d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se3e" edge source="s2d" target="s2e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se4" edge source="s2e" target="s2f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="se3g" edge source="s2e" target="s2g" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se5" edge source="s2g" target="s2h" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="702,722;440,722"/>
<c id="se5h" edge source="s2h" target="s2h2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se5x" edge source="s2h2" target="s2hx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="se5l" edge source="s2h2" target="s2ln" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="se6p" edge source="s2ln" target="s2lp" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.49,0,," pts="560,972" v="無"/>
<c id="se6" edge source="s2gi" target="s2lp" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="se6y" edge source="s2ln" target="s2lv" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="se6pv" edge source="s2lp" target="s2lv" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="540,1137;440,1137"/>
<c id="se6px" edge source="s2lp" target="s2lx" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="580,1145;680,1145" v="失敗"/>
<c id="se6vx" edge source="s2lv" target="s2lx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se7" edge source="s2r" target="s4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se8" edge source="s5" target="s6a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se8q" edge source="s6a" target="s6q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se9" edge source="s6q" target="s8" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="se9y" edge source="s6q" target="s6y" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="p7bc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1769,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7bc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1769,140,64" v="黃：判斷"/>
<c id="p7bc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1777,140,44" v="綠：起點／終點"/>
<c id="p7bc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1771,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7bc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1771,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7bc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1779,88,40" v="白：步驟"/>
<c id="p7bc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1779,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7bc_lgt" st="text;s=none;f=none" g="1318,1769,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7bc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1837,120,36" v="便條：補充說明"/>
<c id="p7bc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1837,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7bc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1837,170,36" v="紫：image（引擎與工具）"/>
<c id="p7bc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1837,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7bc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1837,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7bc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1827,30,20" v="v2"/>
<c id="p7bc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1875,200,28" v="本頁名詞"/>
<c id="p7bc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1909,150,86" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）"/>
<c id="p7bc_tv0" st="f=#ffffff;s=#999999" g="190,1909,610,86" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3"/>
<c id="p7bc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1995,150,55" v="resolve／apply"/>
<c id="p7bc_tv1" st="f=#ffffff;s=#999999" g="190,1995,610,55" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗；不建日誌）"/>
<c id="p7bc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2050,150,55" v="upgrade vendor_kit 不建進度日誌（v2.10）"/>
<c id="p7bc_tv2" st="f=#ffffff;s=#999999" g="190,2050,610,55" v="進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）"/>
<c id="p7bc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2105,150,55" v="薄殼首行自描述（Q17）／上次產物／相符"/>
<c id="p7bc_tv3" st="f=#ffffff;s=#999999" g="190,2105,610,55" v="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更"/>
<c id="p7bc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2160,150,40" v="gen/.stamp"/>
<c id="p7bc_tv4" st="f=#ffffff;s=#999999" g="190,2160,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）"/>
<c id="p7bc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2200,150,55" v="GHCR／registry／引擎 image／引擎 ref"/>
<c id="p7bc_tv5" st="f=#ffffff;s=#999999" g="190,2200,610,55" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）"/>
<c id="p7bc_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1909,150,55" v="image ID／docker image inspect／local 覆寫"/>
<c id="p7bc_tv6" st="f=#ffffff;s=#999999" g="990,1909,610,55" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p7bc_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1964,150,55" v="metadata"/>
<c id="p7bc_tv7" st="f=#ffffff;s=#999999" g="990,1964,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列"/>
<c id="p7bc_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2019,150,40" v="flock／指紋／進度日誌"/>
<c id="p7bc_tv8" st="f=#ffffff;s=#999999" g="990,2019,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪"/>
<c id="p7bc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2059,150,40" v="dev 覆寫／undev／多工具彙總（Q27）"/>
<c id="p7bc_tv9" st="f=#ffffff;s=#999999" g="990,2059,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7bc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2099,150,71" v="--protocol P／降版（Q19）／結束碼 3"/>
<c id="p7bc_tv10" st="f=#ffffff;s=#999999" g="990,2099,610,71" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用"/>
<c id="p7bc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2170,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7bc_tv11" st="f=#ffffff;s=#999999" g="990,2170,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）啟動器 → 查 registry → 改第一行（v2.7 §5）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,124" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,144,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,144,320,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="620,144,380,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1020,144,200,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,144,360,28" v="專案目錄"/>
<c id="uE2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,188,1600,1442" v="E(c)（1）upgrade vendor_kit[@&amp;lt;tag&amp;gt;]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗（不建日誌）→ 薄殼 == 上次產物？（否 → 1 零寫入）→ @舊版無法無損讀 → 3 → 查 registry → 有新版 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁"/>
<c id="uE2_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="s10" parent="uE2" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,124" v="(c) just vendor_kit upgrade vendor_kit[@&amp;lt;tag&amp;gt;]（(b) 提示後由使用者打；也可直接打）"/>
<c id="s10_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,26,30,20" v="v2"/>
<c id="s11a" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="280,66,280,63" v="grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）"/>
<c id="s11a_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="536,56,30,20" v="v2"/>
<c id="s11n" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="280,180,220,112" v="docker image inspect：本機有？"/>
<c id="s11n_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="476,170,30,20" v="v2"/>
<c id="s11p" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="500,312,80,79" v="無：docker pull 該引擎"/>
<c id="s11p_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="556,302,30,20" v="v2"/>
<c id="s11g" parent="uE2" st="f=#e1d5e7;s=#9673a6" g="1000,330,200,42" v="vendor_kit:vN&lt;br&gt;（第一行指到的引擎）"/>
<c id="s11v" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="280,411,220,112" v="覆寫中且 .Id ≠ 記的 image ID？"/>
<c id="s11v_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="476,401,30,20" v="v2"/>
<c id="s11x" parent="uE2" st="ellipse;f=#f8cecc;s=#000000" g="600,427,240,80" v="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"/>
<c id="s11x_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="816,417,30,20" v="v2"/>
<c id="s10a" parent="uE2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="20,543,220,102" v="來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect）"/>
<c id="s11r" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,574,320,40" v="否：docker run 該引擎 upgrade vendor_kit"/>
<c id="s11r_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="556,564,30,20" v="v2"/>
<c id="s12a" parent="uE2" st="f=#dae8fc;s=#6c8ebf" g="610,574,360,40" v="flock 專案目錄（60 秒）"/>
<c id="s12a_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,564,30,20" v="v2"/>
<c id="s12b" parent="uE2" st="f=#dae8fc;s=#6c8ebf" g="600,674,220,40" v="重驗指紋"/>
<c id="s12b_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="796,664,30,20" v="v2"/>
<c id="s12bx" parent="uE2" st="ellipse;f=#ffe6cc;s=#000000" g="850,665,130,58" v="不同 → 1「請重跑」"/>
<c id="s12bx_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="956,655,30,20" v="v2"/>
<c id="s12sx" parent="uE2" st="ellipse;f=#ffe6cc;s=#000000" g="20,748,220,102" v="否 → 1：偵測到薄殼被修改，列差異不動（零寫入；git checkout 還原後再跑）"/>
<c id="s12sx_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,738,30,20" v="v2"/>
<c id="s12s" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="600,743,260,112" v="薄殼 == 上次產物？（首行自描述 hash、未被改）"/>
<c id="s12s_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,733,30,20" v="v2"/>
<c id="s12sn" parent="uE2" st="shape=note;f=#ffffff;s=#999999" g="1220,760,360,79" v="「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入（含改第一行）之前檢查，不符 → 1 列差異、零寫入（v2.8 §3）"/>
<c id="s12sn_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,750,30,20" v="v2"/>
<c id="s12dx" parent="uE2" st="ellipse;f=#ffe6cc;s=#000000" g="20,875,220,124" v="是 → 3：印 6-10「目標引擎無法無損讀取現有檔；未修改任何檔；要退回請 git revert」（零寫入）"/>
<c id="s12dx_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,865,30,20" v="v2"/>
<c id="s12d" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="600,881,260,112" v="是 → @&amp;lt;tag&amp;gt; 為舊版且無法無損讀現有檔（P／schema）？"/>
<c id="s12d_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,871,30,20" v="v2"/>
<c id="s12t" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="600,1019,260,112" v="否 → @&amp;lt;tag&amp;gt; 指定或 CI 為真（frozen）？"/>
<c id="s12t_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,1009,30,20" v="v2"/>
<c id="s12tn" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="880,1051,100,48" v="是：不查 registry"/>
<c id="s12tn_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="956,1041,30,20" v="v2"/>
<c id="s12u" parent="uE2" st="f=#dae8fc;s=#6c8ebf" g="600,1151,260,48" v="否：查 registry（GHCR）取引擎最新正式版"/>
<c id="s12u_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,1141,30,20" v="v2"/>
<c id="s12v" parent="uE2" st="rhombus;f=#FFF4C3;s=#000000" g="600,1230,200,50" v="有新版？"/>
<c id="s12v_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,1220,30,20" v="v2"/>
<c id="s12vz" parent="uE2" st="text;s=none;f=none;b=1" g="870,1219,110,73" v="否／不查 → 續「E(c)（2）」頁：薄殼比對與重產"/>
<c id="s12hz" parent="uE2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1312,220,124" v="→ 用新引擎從本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）"/>
<c id="s12hz_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1302,30,20" v="v2"/>
<c id="s12h" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1342,300,63" v="啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）"/>
<c id="s12h_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="546,1332,30,20" v="v2"/>
<c id="s12w" parent="uE2" st="f=#dae8fc;s=#6c8ebf" g="600,1350,260,48" v="是：改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動、不建日誌）"/>
<c id="s12w_v2" parent="uE2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,1340,30,20" v="v2"/>
<c id="s12wf" parent="uE2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1354,360,40" v="version.toml 第一行 = 新引擎 ref（進 git）"/>
<c id="se11" edge source="s10" target="s11a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se11q" edge source="s11a" target="s11n" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se11p" edge source="s11n" target="s11p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.66,0,," pts="560,424" v="無"/>
<c id="se11g" edge source="s11g" target="s11p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="se11v" edge source="s11n" target="s11v" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="se11pv" edge source="s11p" target="s11v" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="540,589;410,589"/>
<c id="se11px" edge source="s11p" target="s11x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="580,597;680,597" v="失敗"/>
<c id="se11vx" edge source="s11v" target="s11x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se11e" edge source="s10a" target="s11r" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12" edge source="s11r" target="s12a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12b" edge source="s12a" target="s12b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12x" edge source="s12b" target="s12bx" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12s" edge source="s12b" target="s12s" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12sx" edge source="s12s" target="s12sx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="se12d" edge source="s12s" target="s12d" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="se12dx" edge source="s12d" target="s12dx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se12t" edge source="s12d" target="s12t" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="se12tn" edge source="s12t" target="s12tn" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se12u" edge source="s12t" target="s12u" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="se12v" edge source="s12u" target="s12v" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12vn" edge source="s12v" target="s12vz" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="se12tv" edge source="s12tn" target="s12vz" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12w" edge source="s12v" target="s12w" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="se12wf" edge source="s12w" target="s12wf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="se12wh" edge source="s12w" target="s12h" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se12hz" edge source="s12h" target="s12hz" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p7bcc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1646,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7bcc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1646,140,64" v="黃：判斷"/>
<c id="p7bcc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1654,140,44" v="綠：起點／終點"/>
<c id="p7bcc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1648,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7bcc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1648,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7bcc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1656,88,40" v="白：步驟"/>
<c id="p7bcc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1656,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7bcc_lgt" st="text;s=none;f=none" g="1318,1646,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7bcc_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1714,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p7bcc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1714,120,36" v="便條：補充說明"/>
<c id="p7bcc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1714,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7bcc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1714,170,36" v="紫：image（引擎與工具）"/>
<c id="p7bcc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1714,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7bcc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1714,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7bcc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1704,30,20" v="v2"/>
<c id="p7bcc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1752,200,28" v="本頁名詞"/>
<c id="p7bcc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1786,150,86" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）"/>
<c id="p7bcc_tv0" st="f=#ffffff;s=#999999" g="190,1786,610,86" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3"/>
<c id="p7bcc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1872,150,55" v="resolve／apply"/>
<c id="p7bcc_tv1" st="f=#ffffff;s=#999999" g="190,1872,610,55" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗；不建日誌）"/>
<c id="p7bcc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1927,150,55" v="upgrade vendor_kit 不建進度日誌（v2.10）"/>
<c id="p7bcc_tv2" st="f=#ffffff;s=#999999" g="190,1927,610,55" v="進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）"/>
<c id="p7bcc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1982,150,55" v="薄殼首行自描述（Q17）／上次產物／相符"/>
<c id="p7bcc_tv3" st="f=#ffffff;s=#999999" g="190,1982,610,55" v="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更"/>
<c id="p7bcc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2037,150,40" v="gen/.stamp"/>
<c id="p7bcc_tv4" st="f=#ffffff;s=#999999" g="190,2037,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）"/>
<c id="p7bcc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2077,150,55" v="GHCR／registry／引擎 image／引擎 ref"/>
<c id="p7bcc_tv5" st="f=#ffffff;s=#999999" g="190,2077,610,55" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）"/>
<c id="p7bcc_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1786,150,55" v="image ID／docker image inspect／local 覆寫"/>
<c id="p7bcc_tv6" st="f=#ffffff;s=#999999" g="990,1786,610,55" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p7bcc_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1841,150,55" v="metadata"/>
<c id="p7bcc_tv7" st="f=#ffffff;s=#999999" g="990,1841,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列"/>
<c id="p7bcc_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1896,150,40" v="flock／指紋／進度日誌"/>
<c id="p7bcc_tv8" st="f=#ffffff;s=#999999" g="990,1896,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪"/>
<c id="p7bcc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1936,150,40" v="dev 覆寫／undev／多工具彙總（Q27）"/>
<c id="p7bcc_tv9" st="f=#ffffff;s=#999999" g="990,1936,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7bcc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1976,150,71" v="--protocol P／降版（Q19）／結束碼 3"/>
<c id="p7bcc_tv10" st="f=#ffffff;s=#999999" g="990,1976,610,71" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用"/>
<c id="p7bcc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2047,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7bcc_tv11" st="f=#ffffff;s=#999999" g="990,2047,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）薄殼比對 → 重產（v2.2 A、v2.3 §2、Q17、v2.7 §5）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,124" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,144,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,144,320,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="620,144,380,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1020,144,200,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,144,360,28" v="專案目錄"/>
<c id="uE3" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,188,1600,902" v="E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼四檔 + gen/.stamp + tools.just（不建日誌；未完成由第一行 ≠ gen/.stamp 辨識）→ 1"/>
<c id="uE3_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="s12z0" parent="uE3" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="610,36,360,80" v="來自「E(c)（1）」頁：無新版／不查（第一行未變；已拿鎖、重驗，且薄殼 == 上次產物）"/>
<c id="s12n" parent="uE3" st="shape=note;f=#ffffff;s=#999999" g="1220,152,360,79" v="「薄殼 == 上次產物」（首行自描述 sha256 與其餘內容相符，Q17）已在「E(c)（1）」頁拿鎖重驗後、任何寫入前驗過（v2.8 §3）；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更（v2.7 §5）"/>
<c id="s12n_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,142,30,20" v="v2"/>
<c id="s12z" parent="uE3" st="ellipse;f=#d5e8d4;s=#000000" g="20,163,220,58" v="是 → 0：無變更（薄殼相符，已是本引擎產物）"/>
<c id="s12z_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,153,30,20" v="v2"/>
<c id="s12e" parent="uE3" st="rhombus;f=#FFF4C3;s=#000000" g="600,136,300,112" v="首行 engine == 本引擎且 gen/.stamp 相符？"/>
<c id="s12e_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="876,126,30,20" v="v2"/>
<c id="s13" parent="uE3" st="f=#dae8fc;s=#6c8ebf" g="610,327,360,40" v="否：重產薄殼四檔（暫存 → 原子替換）"/>
<c id="s13_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,317,30,20" v="v2"/>
<c id="s13f" parent="uE3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,268,360,158" v="薄殼四檔（進 git）"/>
<c id="s13f_0" parent="s13f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,344,26" v=".vendor_kit/.gitignore"/>
<c id="s13f_1" parent="s13f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,344,26" v=".vendor_kit/entry.just"/>
<c id="s13f_2" parent="s13f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,90,344,26" v=".vendor_kit/vendor.just"/>
<c id="s13f_3" parent="s13f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,122,344,26" v=".vendor_kit/ci/check.sh"/>
<c id="s13b" parent="uE3" st="f=#dae8fc;s=#6c8ebf" g="610,446,360,40" v="寫 gen/.stamp（本引擎 ref）"/>
<c id="s13b_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,436,30,20" v="v2"/>
<c id="s13bf" parent="uE3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,446,360,40" v="gen/.stamp（不進 git）"/>
<c id="s13c" parent="uE3" st="f=#dae8fc;s=#6c8ebf" g="610,548,360,40" v="重生 gen/tools.just（用本引擎的規則；mod? 行）"/>
<c id="s13c_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,538,30,20" v="v2"/>
<c id="s13cf" parent="uE3" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,548,360,40" v="gen/tools.just（不進 git；mod? 行）"/>
<c id="s14" parent="uE3" st="ellipse;f=#ffe6cc;s=#000000" g="20,506,220,124" v="成功 → 1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"/>
<c id="s14_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,496,30,20" v="v2"/>
<c id="s13x" parent="uE3" st="ellipse;f=#ffe6cc;s=#000000" g="20,650,220,146" v="是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」"/>
<c id="s13x_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,640,30,20" v="v2"/>
<c id="s13q" parent="uE3" st="rhombus;f=#FFF4C3;s=#000000" g="740,682,240,81" v="失敗 → 第一行已改（或又變）？"/>
<c id="s13q_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="956,672,30,20" v="v2"/>
<c id="s13xn" parent="uE3" st="ellipse;f=#ffe6cc;s=#000000" g="740,816,240,80" v="否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"/>
<c id="s13xn_v2" parent="uE3" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="956,806,30,20" v="v2"/>
<c id="se13" edge source="s12z0" target="s12e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se15z" edge source="s12e" target="s12z" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se15l" edge source="s12e" target="s13" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="se16" edge source="s13" target="s13f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="se17" edge source="s13" target="s13b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se18" edge source="s13b" target="s13bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="se18b" edge source="s13b" target="s13c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se18c" edge source="s13c" target="s13cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="se18d" edge source="s13c" target="s14" st="es=orthogonalEdgeStyle;s=default;fc=default" v="成功"/>
<c id="se18x" edge source="s13c" target="s13q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="失敗"/>
<c id="se19" edge source="s13q" target="s13x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="se19n" edge source="s13q" target="s13xn" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="p7bcd_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1106,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p7bcd_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1106,140,64" v="黃：判斷"/>
<c id="p7bcd_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1114,140,44" v="綠：起點／終點"/>
<c id="p7bcd_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1108,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p7bcd_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1108,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p7bcd_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1116,88,40" v="白：步驟"/>
<c id="p7bcd_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1116,170,40" v="虛線框：專案裡的檔案"/>
<c id="p7bcd_lgt" st="text;s=none;f=none" g="1318,1106,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p7bcd_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1174,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p7bcd_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1174,120,36" v="便條：補充說明"/>
<c id="p7bcd_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1174,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p7bcd_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1174,170,36" v="紫：image（引擎與工具）"/>
<c id="p7bcd_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1174,170,36" v="灰底：泳道／表格表頭"/>
<c id="p7bcd_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1174,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p7bcd_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1164,30,20" v="v2"/>
<c id="p7bcd_th" st="text;fs=13;s=none;f=none;b=1" g="40,1212,200,28" v="本頁名詞"/>
<c id="p7bcd_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1246,150,86" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）"/>
<c id="p7bcd_tv0" st="f=#ffffff;s=#999999" g="190,1246,610,86" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&amp;lt;tag&amp;gt;]：查 registry（@&amp;lt;tag&amp;gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3"/>
<c id="p7bcd_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1332,150,55" v="resolve／apply"/>
<c id="p7bcd_tv1" st="f=#ffffff;s=#999999" g="190,1332,610,55" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗；不建日誌）"/>
<c id="p7bcd_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1387,150,55" v="upgrade vendor_kit 不建進度日誌（v2.10）"/>
<c id="p7bcd_tv2" st="f=#ffffff;s=#999999" g="190,1387,610,55" v="進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）"/>
<c id="p7bcd_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1442,150,55" v="薄殼首行自描述（Q17）／上次產物／相符"/>
<c id="p7bcd_tv3" st="f=#ffffff;s=#999999" g="190,1442,610,55" v="薄殼每檔首行 # vendor_kit-shell/&amp;lt;P&amp;gt; engine=&amp;lt;vX&amp;gt; sha256=&amp;lt;其餘內容 hash&amp;gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更"/>
<c id="p7bcd_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1497,150,40" v="gen/.stamp"/>
<c id="p7bcd_tv4" st="f=#ffffff;s=#999999" g="190,1497,610,40" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）"/>
<c id="p7bcd_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1537,150,55" v="GHCR／registry／引擎 image／引擎 ref"/>
<c id="p7bcd_tv5" st="f=#ffffff;s=#999999" g="190,1537,610,55" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&amp;lt;tag&amp;gt; 不查）"/>
<c id="p7bcd_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1246,150,55" v="image ID／docker image inspect／local 覆寫"/>
<c id="p7bcd_tv6" st="f=#ffffff;s=#999999" g="990,1246,610,55" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）"/>
<c id="p7bcd_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1301,150,55" v="metadata"/>
<c id="p7bcd_tv7" st="f=#ffffff;s=#999999" g="990,1301,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列"/>
<c id="p7bcd_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1356,150,40" v="flock／指紋／進度日誌"/>
<c id="p7bcd_tv8" st="f=#ffffff;s=#999999" g="990,1356,610,40" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪"/>
<c id="p7bcd_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1396,150,40" v="dev 覆寫／undev／多工具彙總（Q27）"/>
<c id="p7bcd_tv9" st="f=#ffffff;s=#999999" g="990,1396,610,40" v="工具在 version.local.toml 有 path:&amp;lt;dir&amp;gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &amp;gt; 2 &amp;gt; 0，訊息全列"/>
<c id="p7bcd_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1436,150,71" v="--protocol P／降版（Q19）／結束碼 3"/>
<c id="p7bcd_tv10" st="f=#ffffff;s=#999999" g="990,1436,610,71" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用"/>
<c id="p7bcd_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1507,150,55" v="結束狀態 0／1／2／3"/>
<c id="p7bcd_tv11" st="f=#ffffff;s=#999999" g="990,1507,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：dev &lt;repo&gt;">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：dev &amp;lt;repo&amp;gt;（§2 dev 列；v2.1 B、v2.2 B、v2.3 §3；&amp;lt;repo&amp;gt; = 工具 repo 名）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="vA" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,872" v="dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;：工具 path 覆寫（v2.1 B）—— 用本機工具 repo 的 dist/ 取代 image（不進 git；CI 拒絕；工具必須已在 version.toml；不經 docker create/cp）"/>
<c id="vA_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="d0" parent="vA" st="ellipse;f=#d5e8d4;s=#000000" g="20,48,220,58" v="just vendor_kit dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;"/>
<c id="d1q" parent="vA" st="rhombus;f=#FFF4C3;s=#000000" g="300,36,240,81" v="&amp;lt;dir&amp;gt;/dist/ 內有 init.toml？"/>
<c id="d1q_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,26,30,20" v="v2"/>
<c id="d1x" parent="vA" st="ellipse;f=#ffe6cc;s=#000000" g="16,137,227,80" v="否 → 1：&amp;lt;dir&amp;gt;/dist/init.toml 不存在"/>
<c id="d1x_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="219,127,30,20" v="v2"/>
<c id="d1m" parent="vA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="336,146,204,63" v="是：準備掛載 -v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro（唯讀）"/>
<c id="d1m_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,136,30,20" v="v2"/>
<c id="d1" parent="vA" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="340,237,200,63" v="docker run 引擎 dev &amp;lt;repo&amp;gt; -p &amp;lt;dir&amp;gt;（不經 docker create/cp）"/>
<c id="d1_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,227,30,20" v="v2"/>
<c id="d3a" parent="vA" st="ellipse;f=#ffe6cc;s=#000000" g="20,340,220,40" v="是 → 1：CI 拒絕 dev"/>
<c id="d2a" parent="vA" st="rhombus;f=#FFF4C3;s=#000000" g="560,320,130,81" v="CI 為真？"/>
<c id="d2b" parent="vA" st="rhombus;f=#FFF4C3;s=#000000" g="720,336,240,50" v="已接入 &amp;lt;repo&amp;gt;？"/>
<c id="d3c" parent="vA" st="ellipse;f=#ffe6cc;s=#000000" g="20,421,220,58" v="否 → 1：dist/ 或 init.toml 不合法"/>
<c id="d2c" parent="vA" st="rhombus;f=#FFF4C3;s=#000000" g="560,425,180,50" v="dist 合法？"/>
<c id="d3b" parent="vA" st="ellipse;f=#ffe6cc;s=#000000" g="770,421,190,58" v="否 → 1：未接入，請先 add &amp;lt;repo&amp;gt;"/>
<c id="d6a" parent="vA" st="f=#dae8fc;s=#6c8ebf" g="560,499,400,40" v="是：flock 專案目錄（60 秒）"/>
<c id="d6a_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,489,30,20" v="v2"/>
<c id="d6" parent="vA" st="f=#dae8fc;s=#6c8ebf" g="560,559,400,63" v="寫 version.local.toml：&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）"/>
<c id="d6_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,549,30,20" v="v2"/>
<c id="d6f" parent="vA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,570,360,42" v="＋version.local.toml（不進 git）：&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;"/>
<c id="d7" parent="vA" st="f=#dae8fc;s=#6c8ebf" g="560,642,400,42" v="cache/&amp;lt;repo&amp;gt;/ 改為 symlink → &amp;lt;dir&amp;gt;/dist（本機工具 repo 的 dist/，唯讀）"/>
<c id="d7f" parent="vA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,643,360,40" v="cache/&amp;lt;repo&amp;gt;/ → &amp;lt;dir&amp;gt;/dist（symlink，內容不複製）"/>
<c id="d7b" parent="vA" st="f=#dae8fc;s=#6c8ebf" g="560,704,400,48" v="寫印記 gen/&amp;lt;repo&amp;gt;.stamp 第一行 = path:&amp;lt;dir&amp;gt;（印記不放在 symlink 裡）"/>
<c id="d7b_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,694,30,20" v="v2"/>
<c id="d7bf" parent="vA" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,708,360,40" v="gen/&amp;lt;repo&amp;gt;.stamp 第一行：path:&amp;lt;dir&amp;gt;（不進 git）"/>
<c id="d8" parent="vA" st="ellipse;f=#d5e8d4;s=#000000" g="20,790,220,58" v="0：之後每次 just 用 &amp;lt;dir&amp;gt;"/>
<c id="d8_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,780,30,20" v="v2"/>
<c id="d9" parent="vA" st="f=#ffe6cc;s=#d79b00;b=1" g="660,772,300,94" v="dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade &amp;lt;repo&amp;gt;／remove &amp;lt;repo&amp;gt; → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋"/>
<c id="d9_v2" parent="vA" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,762,30,20" v="v2"/>
<c id="de1" edge source="d0" target="d1q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de1x" edge source="d1q" target="d1x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.35,0,," pts="356,333" v="否"/>
<c id="de1y" edge source="d1q" target="d1m" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.18819188191881908,0,," v="是"/>
<c id="de1m" edge source="d1m" target="d1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de2" edge source="d1" target="d2a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="460,466;645,466"/>
<c id="de3" edge source="d2a" target="d3a" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="de4" edge source="d2a" target="d2b" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="de5" edge source="d2b" target="d2c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.06,0,," pts="812,567;670,567" v="是"/>
<c id="de6" edge source="d2b" target="d3b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.03296703296703296,0,," v="否"/>
<c id="de7" edge source="d2c" target="d3c" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="de8" edge source="d2c" target="d6a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="de8b" edge source="d6a" target="d6" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de9" edge source="d6" target="d6f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="de10" edge source="d6" target="d7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de11" edge source="d7" target="d7f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="de12" edge source="d7" target="d7b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="de13" edge source="d7b" target="d7bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="de14" edge source="d7b" target="d8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.84,0,," pts="620,975"/>
<c id="p8_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1044,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1044,140,64" v="黃：判斷"/>
<c id="p8_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1052,140,44" v="綠：起點／終點"/>
<c id="p8_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1046,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1046,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1054,88,40" v="白：步驟"/>
<c id="p8_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1054,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8_lgt" st="text;s=none;f=none" g="1318,1044,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1112,120,36" v="便條：補充說明"/>
<c id="p8_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1112,150,36" v="橘框：規則（已定）"/>
<c id="p8_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1112,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1112,170,36" v="紫：image（引擎與工具）"/>
<c id="p8_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1112,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1112,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1102,30,20" v="v2"/>
<c id="p8_th" st="text;fs=13;s=none;f=none;b=1" g="40,1150,200,28" v="本頁名詞"/>
<c id="p8_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1184,150,40" v="dev／undev"/>
<c id="p8_tv0" st="f=#ffffff;s=#999999" g="190,1184,610,40" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image"/>
<c id="p8_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1224,150,55" v="覆寫兩種（v2.1 B）"/>
<c id="p8_tv1" st="f=#ffffff;s=#999999" g="190,1224,610,55" v="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image"/>
<c id="p8_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1279,150,40" v="resolve／apply"/>
<c id="p8_tv2" st="f=#ffffff;s=#999999" g="190,1279,610,40" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image"/>
<c id="p8_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1319,150,55" v="version.local.toml"/>
<c id="p8_tv3" st="f=#ffffff;s=#999999" g="190,1319,610,55" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）"/>
<c id="p8_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1374,150,55" v="symlink／印記／materialize"/>
<c id="p8_tv4" st="f=#ffffff;s=#999999" g="190,1374,610,55" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/"/>
<c id="p8_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1429,150,55" v="image tag／image ID／RepoDigests"/>
<c id="p8_tv5" st="f=#ffffff;s=#999999" g="190,1429,610,55" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag"/>
<c id="p8_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1184,150,40" v="GHCR／tar／docker load"/>
<c id="p8_tv6" st="f=#ffffff;s=#999999" g="990,1184,610,40" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它"/>
<c id="p8_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1224,150,55" v="docker image inspect／掛載 -v"/>
<c id="p8_tv7" st="f=#ffffff;s=#999999" g="990,1224,610,55" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器"/>
<c id="p8_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1279,150,55" v="統一提示／gen/.stamp（Q10 (2)）"/>
<c id="p8_tv8" st="f=#ffffff;s=#999999" g="990,1279,610,55" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼"/>
<c id="p8_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1334,150,40" v="metadata／baseline"/>
<c id="p8_tv9" st="f=#ffffff;s=#999999" g="990,1334,610,40" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）"/>
<c id="p8_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1374,150,55" v="flock／指紋／進度日誌／CI 為真"/>
<c id="p8_tv10" st="f=#ffffff;s=#999999" g="990,1374,610,55" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1"/>
<c id="p8_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1429,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8_tv11" st="f=#ffffff;s=#999999" g="990,1429,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：dev vendor_kit">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：dev vendor_kit -i（§2 dev 列；v2.1 B、v2.2 B、v2.6 §1）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="vI" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,966" v="dev vendor_kit -i &amp;lt;本機 image tag&amp;gt;：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID（由啟動器 docker image inspect 取得後交給引擎，v2.8 §6）；驗收測試用同一機制"/>
<c id="vI_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="v0" parent="vI" st="ellipse;f=#d5e8d4;s=#000000" g="20,38,220,58" v="dev vendor_kit -i &amp;lt;本機 image tag&amp;gt;"/>
<c id="v1i" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,36,280,63" v="docker image inspect &amp;lt;tag&amp;gt; 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）"/>
<c id="v1i_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,26,30,20" v="v2"/>
<c id="v1" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,119,280,63" v="docker run 引擎 dev vendor_kit -i &amp;lt;tag&amp;gt;，image ID 一併交給引擎（引擎容器內不呼叫 docker）"/>
<c id="v1_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,109,30,20" v="v2"/>
<c id="v2x" parent="vI" st="ellipse;f=#ffe6cc;s=#000000" g="20,214,220,58" v="是 → 1：CI 拒絕 dev（請在本機執行）"/>
<c id="v2x_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,204,30,20" v="v2"/>
<c id="v2q" parent="vI" st="rhombus;f=#FFF4C3;s=#000000" g="560,202,130,81" v="CI 為真？"/>
<c id="v2a" parent="vI" st="f=#dae8fc;s=#6c8ebf" g="560,303,400,40" v="否：flock 專案目錄（60 秒）"/>
<c id="v2a_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,293,30,20" v="v2"/>
<c id="v2b" parent="vI" st="f=#dae8fc;s=#6c8ebf" g="560,364,400,40" v="寫 version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;（不動薄殼）"/>
<c id="v2b_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,354,30,20" v="v2"/>
<c id="v3" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,363,360,42" v="＋version.local.toml：vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;（不進 git）"/>
<c id="v2c" parent="vI" st="f=#dae8fc;s=#6c8ebf" g="560,430,400,48" v="寫 version.local.toml：vendor_kit_image_id = 啟動器交來的 image ID"/>
<c id="v2c_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,420,30,20" v="v2"/>
<c id="v3c" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,433,360,42" v="version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）"/>
<c id="v2z" parent="vI" st="ellipse;f=#d5e8d4;s=#000000" g="20,425,220,58" v="0：之後每次 just 用該本機 image"/>
<c id="v2z_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,415,30,20" v="v2"/>
<c id="v5" parent="vI" st="ellipse;f=#d5e8d4;s=#000000" g="20,553,220,40" v="下次打任何 just"/>
<c id="v6a" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,549,280,48" v="grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag"/>
<c id="v6a_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,539,30,20" v="v2"/>
<c id="vb" parent="vI" st="text;s=none;f=none;b=1" g="260,503,560,26" v="═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══"/>
<c id="v8" parent="vI" st="ellipse;f=#ffe6cc;s=#000000" g="20,617,220,102" v="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」"/>
<c id="v8_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,607,30,20" v="v2"/>
<c id="v7" parent="vI" st="rhombus;f=#FFF4C3;s=#000000" g="265,628,270,81" v="gen/.stamp 的引擎 ref == 該 tag？"/>
<c id="v7_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="511,618,30,20" v="v2"/>
<c id="v9" parent="vI" st="ellipse;f=#d5e8d4;s=#000000" g="20,760,220,102" v="→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）"/>
<c id="v9_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,750,30,20" v="v2"/>
<c id="v6b" parent="vI" st="rhombus;f=#FFF4C3;s=#000000" g="265,739,270,143" v="是：docker image inspect &amp;lt;tag&amp;gt; 的 .Id == 記的 image ID？"/>
<c id="v6b_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="511,729,30,20" v="v2"/>
<c id="v6x" parent="vI" st="ellipse;f=#f8cecc;s=#000000" g="560,770,240,80" v="否 → 1：本機 image 已變（同 tag 重 build）或不存在"/>
<c id="v6x_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,760,30,20" v="v2"/>
<c id="v6c" parent="vI" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,907,280,48" v="是：docker run &amp;lt;tag&amp;gt; resolve sync（不 pull）"/>
<c id="v6c_v2" parent="vI" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,897,30,20" v="v2"/>
<c id="v10" parent="vI" st="ellipse;f=#d5e8d4;s=#000000" g="560,902,240,58" v="0：正常跑（用該本機 image）"/>
<c id="ve1" edge source="v0" target="v1i" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve1i" edge source="v1i" target="v1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve2" edge source="v1" target="v2q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="420,348;645,348"/>
<c id="ve3" edge source="v2q" target="v2x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ve4" edge source="v2q" target="v2a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ve4b" edge source="v2a" target="v2b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve5" edge source="v2b" target="v3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ve5c" edge source="v2b" target="v2c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve5cf" edge source="v2c" target="v3c" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ve6" edge source="v2c" target="v2z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve7" edge source="v5" target="v6a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve8" edge source="v6a" target="v7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve9" edge source="v7" target="v8" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ve10" edge source="v8" target="v9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve11" edge source="v7" target="v6b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ve11x" edge source="v6b" target="v6x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ve11c" edge source="v6b" target="v6c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="ve12" edge source="v6c" target="v10" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p8v_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1138,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8v_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1138,140,64" v="黃：判斷"/>
<c id="p8v_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1146,140,44" v="綠：起點／終點"/>
<c id="p8v_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1140,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8v_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1140,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8v_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1148,88,40" v="白：步驟"/>
<c id="p8v_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1148,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8v_lgt" st="text;s=none;f=none" g="1318,1138,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8v_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1206,120,36" v="便條：補充說明"/>
<c id="p8v_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1206,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8v_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1206,170,36" v="紫：image（引擎與工具）"/>
<c id="p8v_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1206,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8v_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1206,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8v_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1196,30,20" v="v2"/>
<c id="p8v_th" st="text;fs=13;s=none;f=none;b=1" g="40,1244,200,28" v="本頁名詞"/>
<c id="p8v_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1278,150,40" v="dev／undev"/>
<c id="p8v_tv0" st="f=#ffffff;s=#999999" g="190,1278,610,40" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image"/>
<c id="p8v_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1318,150,55" v="覆寫兩種（v2.1 B）"/>
<c id="p8v_tv1" st="f=#ffffff;s=#999999" g="190,1318,610,55" v="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image"/>
<c id="p8v_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1373,150,40" v="resolve／apply"/>
<c id="p8v_tv2" st="f=#ffffff;s=#999999" g="190,1373,610,40" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image"/>
<c id="p8v_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1413,150,55" v="version.local.toml"/>
<c id="p8v_tv3" st="f=#ffffff;s=#999999" g="190,1413,610,55" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）"/>
<c id="p8v_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1468,150,55" v="symlink／印記／materialize"/>
<c id="p8v_tv4" st="f=#ffffff;s=#999999" g="190,1468,610,55" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/"/>
<c id="p8v_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1523,150,55" v="image tag／image ID／RepoDigests"/>
<c id="p8v_tv5" st="f=#ffffff;s=#999999" g="190,1523,610,55" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag"/>
<c id="p8v_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1278,150,40" v="GHCR／tar／docker load"/>
<c id="p8v_tv6" st="f=#ffffff;s=#999999" g="990,1278,610,40" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它"/>
<c id="p8v_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1318,150,55" v="docker image inspect／掛載 -v"/>
<c id="p8v_tv7" st="f=#ffffff;s=#999999" g="990,1318,610,55" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器"/>
<c id="p8v_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1373,150,55" v="統一提示／gen/.stamp（Q10 (2)）"/>
<c id="p8v_tv8" st="f=#ffffff;s=#999999" g="990,1373,610,55" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼"/>
<c id="p8v_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1428,150,40" v="metadata／baseline"/>
<c id="p8v_tv9" st="f=#ffffff;s=#999999" g="990,1428,610,40" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）"/>
<c id="p8v_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1468,150,55" v="flock／指紋／進度日誌／CI 為真"/>
<c id="p8v_tv10" st="f=#ffffff;s=#999999" g="990,1468,610,55" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1"/>
<c id="p8v_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1523,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8v_tv11" st="f=#ffffff;s=#999999" g="990,1523,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：undev &lt;repo&gt;">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：undev（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §3／§10；&amp;lt;repo&amp;gt; = 工具 repo 名）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="vB" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,1292" v="undev &amp;lt;repo&amp;gt;：回到 version.toml 鎖定版 = resolve → docker → apply（要重新 materialize，v2.3 §5；建日誌後才動，v2.5 §10；失敗 → 1 保留可恢復狀態，v2.2 B）"/>
<c id="vB_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="u0" parent="vB" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,58" v="just vendor_kit undev &amp;lt;repo&amp;gt;"/>
<c id="u1" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,45,280,40" v="docker run 引擎 resolve undev &amp;lt;repo&amp;gt;"/>
<c id="u3" parent="vB" st="ellipse;f=#d5e8d4;s=#000000" g="20,116,220,58" v="否 → 0：未啟用 dev（提示）"/>
<c id="u2" parent="vB" st="rhombus;f=#FFF4C3;s=#000000" g="560,120,220,50" v="有 path 覆寫？"/>
<c id="u4" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="800,114,160,63" v="是：resolve：要拉 &amp;lt;repo&amp;gt;-dist@digest（鎖定版）；輸出指紋"/>
<c id="u4_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,104,30,20" v="v2"/>
<c id="u5a" parent="vB" st="rhombus;f=#FFF4C3;s=#000000" g="260,197,170,143" v="docker image inspect：本機有？"/>
<c id="u5a_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="406,187,30,20" v="v2"/>
<c id="u5p" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="440,360,100,48" v="無：docker pull"/>
<c id="u5p_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,350,30,20" v="v2"/>
<c id="u5g" parent="vB" st="f=#e1d5e7;s=#9673a6" g="980,364,220,40" v="&amp;lt;repo&amp;gt;-dist@digest（鎖定版）"/>
<c id="u5b" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,428,280,40" v="docker create &amp;lt;img&amp;gt; /x"/>
<c id="u5b_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,418,30,20" v="v2"/>
<c id="u5c" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,488,280,48" v="docker cp c:/dist/. &amp;lt;tmp&amp;gt;/&amp;lt;repo&amp;gt;/（主機暫存）"/>
<c id="u5c_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,478,30,20" v="v2"/>
<c id="u5d" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,556,280,40" v="docker rm 該容器"/>
<c id="u5d_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,546,30,20" v="v2"/>
<c id="u5r" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,616,280,48" v="docker run … -v &amp;lt;tmp&amp;gt;:/dist:ro 引擎 apply undev &amp;lt;repo&amp;gt;"/>
<c id="u5r_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,606,30,20" v="v2"/>
<c id="u6a" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,620,400,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="u6a_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,610,30,20" v="v2"/>
<c id="u6b" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,693,240,40" v="重驗指紋"/>
<c id="u6b_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,683,30,20" v="v2"/>
<c id="u6bx" parent="vB" st="ellipse;f=#ffe6cc;s=#000000" g="820,684,140,58" v="不同 → 1「請重跑」"/>
<c id="u6bx_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,674,30,20" v="v2"/>
<c id="u6l" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,762,400,48" v="建進度日誌（.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml；第一個寫入前）"/>
<c id="u6l_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,752,30,20" v="v2"/>
<c id="u6lf" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,765,360,42" v="＋.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）"/>
<c id="u6c" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,830,400,48" v="刪 version.local.toml 該行（&amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；最後一個覆寫 → 刪整個檔）"/>
<c id="u6c_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,820,30,20" v="v2"/>
<c id="u6cf" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,834,360,40" v="version.local.toml（少一行；空了就刪檔）"/>
<c id="u6d" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,898,400,40" v="拆掉 cache/&amp;lt;repo&amp;gt;/ 的 symlink"/>
<c id="u6d_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,888,30,20" v="v2"/>
<c id="u6df" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,898,360,40" v="cache/&amp;lt;repo&amp;gt;/（不再是 symlink）"/>
<c id="u6e" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,958,400,40" v="materialize 鎖定版：/dist/&amp;lt;repo&amp;gt; 展開到暫存目錄"/>
<c id="u6e_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,948,30,20" v="v2"/>
<c id="u6e2" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,1018,400,40" v="暫存 → cache/&amp;lt;repo&amp;gt;/（原子替換）"/>
<c id="u6e2_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1008,30,20" v="v2"/>
<c id="u6ef" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1018,360,40" v="cache/&amp;lt;repo&amp;gt;/（重新展開）"/>
<c id="u6f" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,1078,400,48" v="寫 gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest，之後每檔 sha256）"/>
<c id="u6f_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1068,30,20" v="v2"/>
<c id="u6ff" parent="vB" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1082,360,40" v="gen/&amp;lt;repo&amp;gt;.stamp（第一行 index digest）"/>
<c id="u6x" parent="vB" st="ellipse;f=#f8cecc;s=#000000" g="20,1146,220,80" v="失敗（任一步）→ 1：保留可恢復狀態（下次任何動詞先恢復）"/>
<c id="u6x_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1136,30,20" v="v2"/>
<c id="u6g" parent="vB" st="f=#dae8fc;s=#6c8ebf" g="560,1166,400,40" v="刪進度日誌（最後一步）"/>
<c id="u6g_v2" parent="vB" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1156,30,20" v="v2"/>
<c id="u7" parent="vB" st="ellipse;f=#d5e8d4;s=#000000" g="20,1246,220,40" v="成功 → 0"/>
<c id="ue1" edge source="u0" target="u1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue2" edge source="u1" target="u2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.01,0,," pts="420,260;690,260"/>
<c id="ue3" edge source="u2" target="u3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ue4" edge source="u2" target="u4" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue5" edge source="u4" target="u5a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="900,343;365,343"/>
<c id="ue5n" edge source="u5a" target="u5p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.60,0,," pts="510,424" v="無"/>
<c id="ue6" edge source="u5g" target="u5p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉 /dist"/>
<c id="ue5y" edge source="u5a" target="u5b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="ue5p" edge source="u5p" target="u5b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue5c" edge source="u5b" target="u5c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue5d" edge source="u5c" target="u5d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue7" edge source="u5d" target="u5r" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue8" edge source="u5r" target="u6a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue8b" edge source="u6a" target="u6b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue8x" edge source="u6b" target="u6bx" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue9" edge source="u6b" target="u6l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue9f" edge source="u6l" target="u6lf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ue10" edge source="u6l" target="u6c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue10f" edge source="u6c" target="u6cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ue11" edge source="u6c" target="u6d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue11f" edge source="u6d" target="u6df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ue12" edge source="u6d" target="u6e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue12b" edge source="u6e" target="u6e2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue12f" edge source="u6e2" target="u6ef" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ue13" edge source="u6e2" target="u6f" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue13f" edge source="u6f" target="u6ff" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ue14" edge source="u6f" target="u6g" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="成功"/>
<c id="ue14x" edge source="u6f" target="u6x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,1292;150,1292" v="失敗"/>
<c id="ue15" edge source="u6g" target="u7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.90,0,," pts="780,1422"/>
<c id="p8c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1464,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1464,140,64" v="黃：判斷"/>
<c id="p8c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1472,140,44" v="綠：起點／終點"/>
<c id="p8c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1466,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1466,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1474,88,40" v="白：步驟"/>
<c id="p8c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1474,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8c_lgt" st="text;s=none;f=none" g="1318,1464,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1532,120,36" v="便條：補充說明"/>
<c id="p8c_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1532,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1532,170,36" v="紫：image（引擎與工具）"/>
<c id="p8c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1532,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8c_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1532,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8c_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1522,30,20" v="v2"/>
<c id="p8c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1570,200,28" v="本頁名詞"/>
<c id="p8c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1604,150,40" v="dev／undev"/>
<c id="p8c_tv0" st="f=#ffffff;s=#999999" g="190,1604,610,40" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image"/>
<c id="p8c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1644,150,55" v="覆寫兩種（v2.1 B）"/>
<c id="p8c_tv1" st="f=#ffffff;s=#999999" g="190,1644,610,55" v="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image"/>
<c id="p8c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1699,150,40" v="resolve／apply"/>
<c id="p8c_tv2" st="f=#ffffff;s=#999999" g="190,1699,610,40" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image"/>
<c id="p8c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1739,150,55" v="version.local.toml"/>
<c id="p8c_tv3" st="f=#ffffff;s=#999999" g="190,1739,610,55" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）"/>
<c id="p8c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1794,150,55" v="symlink／印記／materialize"/>
<c id="p8c_tv4" st="f=#ffffff;s=#999999" g="190,1794,610,55" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/"/>
<c id="p8c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1849,150,55" v="image tag／image ID／RepoDigests"/>
<c id="p8c_tv5" st="f=#ffffff;s=#999999" g="190,1849,610,55" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag"/>
<c id="p8c_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1604,150,40" v="GHCR／tar／docker load"/>
<c id="p8c_tv6" st="f=#ffffff;s=#999999" g="990,1604,610,40" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它"/>
<c id="p8c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1644,150,55" v="docker image inspect／掛載 -v"/>
<c id="p8c_tv7" st="f=#ffffff;s=#999999" g="990,1644,610,55" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器"/>
<c id="p8c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1699,150,55" v="統一提示／gen/.stamp（Q10 (2)）"/>
<c id="p8c_tv8" st="f=#ffffff;s=#999999" g="990,1699,610,55" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼"/>
<c id="p8c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1754,150,40" v="metadata／baseline"/>
<c id="p8c_tv9" st="f=#ffffff;s=#999999" g="990,1754,610,40" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）"/>
<c id="p8c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1794,150,55" v="flock／指紋／進度日誌／CI 為真"/>
<c id="p8c_tv10" st="f=#ffffff;s=#999999" g="990,1794,610,55" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1"/>
<c id="p8c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1849,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8c_tv11" st="f=#ffffff;s=#999999" g="990,1849,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：undev vendor_kit">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：undev vendor_kit（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §10、v2.6 §1、v2.7 §6；Q10 (2)）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&amp;lt;repo&amp;gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,112,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,112,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,112,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,112,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,112,360,28" v="專案目錄"/>
<c id="vB′" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,156,1600,1436" v="undev vendor_kit = resolve → apply（無 image 要拉）：建 .tmp.undev.&amp;lt;id&amp;gt;.toml 日誌後才撤 vendor_kit 行（含 image ID）；最後一個覆寫撤掉 → 刪整個 version.local.toml；下次 just：gen/.stamp 不符 → 只回 1 提示（Q10 (2)）"/>
<c id="vB′_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="w0" parent="vB′" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,58" v="just vendor_kit undev vendor_kit"/>
<c id="w1" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,41,280,48" v="docker run 引擎 resolve undev vendor_kit"/>
<c id="w1_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,31,30,20" v="v2"/>
<c id="w3" parent="vB′" st="ellipse;f=#d5e8d4;s=#000000" g="20,134,220,40" v="否 → 0：未啟用（提示）"/>
<c id="w2q" parent="vB′" st="rhombus;f=#FFF4C3;s=#000000" g="560,114,300,81" v="version.local.toml 有 vendor_kit 行？"/>
<c id="w2q_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="836,104,30,20" v="v2"/>
<c id="w2s" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,215,400,48" v="是：resolve（不寫）：無 image 要拉；輸出輸入指紋（version.local.toml hash）"/>
<c id="w2s_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,205,30,20" v="v2"/>
<c id="w1b" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,283,280,48" v="docker run 引擎 apply undev vendor_kit"/>
<c id="w1b_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,273,30,20" v="v2"/>
<c id="w2a" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,287,400,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="w2a_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,277,30,20" v="v2"/>
<c id="w2b" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,360,240,40" v="重驗指紋"/>
<c id="w2b_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,350,30,20" v="v2"/>
<c id="w2bx" parent="vB′" st="ellipse;f=#ffe6cc;s=#000000" g="820,351,140,58" v="不同 → 1「請重跑」"/>
<c id="w2bx_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,341,30,20" v="v2"/>
<c id="w2l" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,429,400,48" v="建進度日誌（.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml；第一個寫入前）"/>
<c id="w2l_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,419,30,20" v="v2"/>
<c id="w2lf" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,432,360,42" v="＋.vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）"/>
<c id="w2x" parent="vB′" st="ellipse;f=#f8cecc;s=#000000" g="20,497,220,80" v="失敗 → 1：保留可恢復狀態（下次可寫動詞先恢復）"/>
<c id="w2x_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,487,30,20" v="v2"/>
<c id="w2" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,513,400,48" v="刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）"/>
<c id="w2_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,503,30,20" v="v2"/>
<c id="w2f" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,516,360,42" v="version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）"/>
<c id="w2e" parent="vB′" st="rhombus;f=#FFF4C3;s=#000000" g="560,597,200,81" v="還有其他覆寫行？"/>
<c id="w2e_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="736,587,30,20" v="v2"/>
<c id="w2ed" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="790,606,170,63" v="否：刪整個 version.local.toml（最後一個覆寫已撤）"/>
<c id="w2ed_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,596,30,20" v="v2"/>
<c id="w2edf" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,618,360,40" v="－version.local.toml（整個檔）"/>
<c id="w2edf_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,608,30,20" v="v2"/>
<c id="w2g" parent="vB′" st="f=#dae8fc;s=#6c8ebf" g="560,698,400,40" v="是／已刪：刪進度日誌（最後一步）"/>
<c id="w2g_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,688,30,20" v="v2"/>
<c id="w2z" parent="vB′" st="ellipse;f=#d5e8d4;s=#000000" g="20,758,220,80" v="0：本次結束（下次 just 用 version.toml 的引擎）"/>
<c id="w2z_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,748,30,20" v="v2"/>
<c id="wb" parent="vB′" st="text;s=none;f=none;b=1" g="260,858,560,26" v="═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══"/>
<c id="w4" parent="vB′" st="ellipse;f=#d5e8d4;s=#000000" g="20,908,220,40" v="下次打任何 just"/>
<c id="w5a" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,904,280,48" v="grep version.toml 第一行取引擎 ref（local 已無覆寫）"/>
<c id="w5a_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,894,30,20" v="v2"/>
<c id="w7" parent="vB′" st="ellipse;f=#ffe6cc;s=#000000" g="20,972,220,124" v="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」（不重寫）"/>
<c id="w7_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,962,30,20" v="v2"/>
<c id="w6" parent="vB′" st="rhombus;f=#FFF4C3;s=#000000" g="260,994,270,81" v="gen/.stamp 的引擎 ref == 第一行？"/>
<c id="w6_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="506,984,30,20" v="v2"/>
<c id="w5b" parent="vB′" st="rhombus;f=#FFF4C3;s=#000000" g="260,1116,170,174" v="是 → docker image inspect：本機有？"/>
<c id="w5b_v2" parent="vB′" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="406,1106,30,20" v="v2"/>
<c id="w5p" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="440,1310,100,42" v="無：docker pull 該引擎"/>
<c id="w5g" parent="vB′" st="f=#e1d5e7;s=#9673a6" g="980,1310,220,42" v="vendor_kit:vN（version.toml 的引擎）"/>
<c id="w5c" parent="vB′" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,1381,280,40" v="docker run 該引擎 resolve sync"/>
<c id="w9" parent="vB′" st="ellipse;f=#d5e8d4;s=#000000" g="560,1372,200,58" v="0：正常跑（「sync（1）」頁）"/>
<c id="we1" edge source="w0" target="w1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2" edge source="w1" target="w2q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.01,0,," pts="420,260;730,260"/>
<c id="we2n" edge source="w2q" target="w3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="we2y" edge source="w2q" target="w2s" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="we2s" edge source="w2s" target="w1b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,429;420,429"/>
<c id="we2a" edge source="w1b" target="w2a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2b" edge source="w2a" target="w2b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2bx" edge source="w2b" target="w2bx" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2l" edge source="w2b" target="w2l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2lf" edge source="w2l" target="w2lf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="we2w" edge source="w2l" target="w2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we3" edge source="w2" target="w2f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="we3x" edge source="w2" target="w2x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="失敗"/>
<c id="we2e" edge source="w2" target="w2e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2ed" edge source="w2e" target="w2ed" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="we2edf" edge source="w2ed" target="w2edf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="we2g" edge source="w2e" target="w2g" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="we2gd" edge source="w2ed" target="w2g" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we4" edge source="w2g" target="w2z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.90,0,," pts="780,954"/>
<c id="we5" edge source="w4" target="w5a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we6" edge source="w5a" target="w6" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we7" edge source="w6" target="w7" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="we8" edge source="w6" target="w5b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.23,0,," pts="415,1262;365,1262" v="是"/>
<c id="we8n" edge source="w5b" target="w5p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.64,0,," pts="510,1359" v="無"/>
<c id="we8g" edge source="w5g" target="w5p" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="we8y" edge source="w5b" target="w5c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="we8p" edge source="w5p" target="w5c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we10" edge source="w5c" target="w9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p8cc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1608,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8cc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1608,140,64" v="黃：判斷"/>
<c id="p8cc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1616,140,44" v="綠：起點／終點"/>
<c id="p8cc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1610,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8cc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1610,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8cc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1618,88,40" v="白：步驟"/>
<c id="p8cc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1618,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8cc_lgt" st="text;s=none;f=none" g="1318,1608,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8cc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1676,120,36" v="便條：補充說明"/>
<c id="p8cc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1676,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8cc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1676,170,36" v="紫：image（引擎與工具）"/>
<c id="p8cc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1676,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8cc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1676,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8cc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1666,30,20" v="v2"/>
<c id="p8cc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1714,200,28" v="本頁名詞"/>
<c id="p8cc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1748,150,40" v="dev／undev"/>
<c id="p8cc_tv0" st="f=#ffffff;s=#999999" g="190,1748,610,40" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image"/>
<c id="p8cc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1788,150,55" v="覆寫兩種（v2.1 B）"/>
<c id="p8cc_tv1" st="f=#ffffff;s=#999999" g="190,1788,610,55" v="工具 path 覆寫 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;：cache/&amp;lt;repo&amp;gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;＋image ID：啟動器改用該本機 image"/>
<c id="p8cc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1843,150,40" v="resolve／apply"/>
<c id="p8cc_tv2" st="f=#ffffff;s=#999999" g="190,1843,610,40" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image"/>
<c id="p8cc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1883,150,55" v="version.local.toml"/>
<c id="p8cc_tv3" st="f=#ffffff;s=#999999" g="190,1883,610,55" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot; 或 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + image ID（成對，undev 一起撤）"/>
<c id="p8cc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1938,150,55" v="symlink／印記／materialize"/>
<c id="p8cc_tv4" st="f=#ffffff;s=#999999" g="190,1938,610,55" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&amp;lt;repo&amp;gt;/ 不放檔案，而是指到 &amp;lt;dir&amp;gt;/dist；印記 gen/&amp;lt;repo&amp;gt;.stamp 在 symlink 外，第一行 path:&amp;lt;dir&amp;gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&amp;lt;repo&amp;gt;/"/>
<c id="p8cc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1993,150,55" v="image tag／image ID／RepoDigests"/>
<c id="p8cc_tv5" st="f=#ffffff;s=#999999" g="190,1993,610,55" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag"/>
<c id="p8cc_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1748,150,40" v="GHCR／tar／docker load"/>
<c id="p8cc_tv6" st="f=#ffffff;s=#999999" g="990,1748,610,40" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &amp;lt;tag&amp;gt; 指定它"/>
<c id="p8cc_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1788,150,55" v="docker image inspect／掛載 -v"/>
<c id="p8cc_tv7" st="f=#ffffff;s=#999999" g="990,1788,610,55" v="啟動器每次 docker run 前先 docker image inspect &amp;lt;ref 或 tag&amp;gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &amp;lt;dir&amp;gt;/dist:/dist/&amp;lt;repo&amp;gt;:ro = 把本機目錄唯讀掛進容器"/>
<c id="p8cc_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1843,150,55" v="統一提示／gen/.stamp（Q10 (2)）"/>
<c id="p8cc_tv8" st="f=#ffffff;s=#999999" g="990,1843,610,55" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼"/>
<c id="p8cc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1898,150,40" v="metadata／baseline"/>
<c id="p8cc_tv9" st="f=#ffffff;s=#999999" g="990,1898,610,40" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）"/>
<c id="p8cc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1938,150,55" v="flock／指紋／進度日誌／CI 為真"/>
<c id="p8cc_tv10" st="f=#ffffff;s=#999999" g="990,1938,610,55" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&amp;lt;id&amp;gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1"/>
<c id="p8cc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1993,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8cc_tv11" st="f=#ffffff;s=#999999" g="990,1993,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：remove（1）resolve → apply 前置">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：remove（1）resolve → apply 前置（§2、§5；v2.2 C／E、v2.3 §5、v2.5 §3／§11）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="vC" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,928" v="remove &amp;lt;repo&amp;gt;（1）：拆掉一個工具（初始檔永不刪、印清單，要刪用 git rm）= resolve（讀 metadata → 刪除清單 → 詢問清單 → 計畫＋指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；無 image 要拉；寫入段見「remove（2）」頁"/>
<c id="vC_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="m0" parent="vC" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="just vendor_kit remove &amp;lt;repo&amp;gt;（-y、--dry-run）"/>
<c id="m1" parent="vC" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,52,280,48" v="docker run &amp;lt;引擎&amp;gt; resolve remove &amp;lt;repo&amp;gt;（不經 docker create/cp）"/>
<c id="m1_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,42,30,20" v="v2"/>
<c id="m3" parent="vC" st="ellipse;f=#d5e8d4;s=#000000" g="20,141,220,40" v="否 → 0：未接入（提示）"/>
<c id="m2" parent="vC" st="rhombus;f=#FFF4C3;s=#000000" g="560,136,280,50" v="已接入 &amp;lt;repo&amp;gt;？"/>
<c id="m5" parent="vC" st="ellipse;f=#ffe6cc;s=#000000" g="20,206,220,58" v="是 → 1：請先 undev &amp;lt;repo&amp;gt;（v2.1 B）"/>
<c id="m4" parent="vC" st="rhombus;f=#FFF4C3;s=#000000" g="560,210,280,50" v="有 dev path 覆寫？"/>
<c id="m6" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,284,400,40" v="否：resolve（不寫）：讀 metadata（append 過的行、完成標記）"/>
<c id="m6_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,274,30,20" v="v2"/>
<c id="m6b" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,344,400,63" v="產生刪除清單：version.toml 行、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、baseline/&amp;lt;repo&amp;gt;/、gen/tools.just 的 mod? 行"/>
<c id="m6b_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,334,30,20" v="v2"/>
<c id="m6c" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,427,400,40" v="產生詢問清單：metadata 記的 append 行（有才問）"/>
<c id="m6c_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,417,30,20" v="v2"/>
<c id="m6d" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,487,400,48" v="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）→ 計畫＋指紋以 stdout 回啟動器"/>
<c id="m6d_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,477,30,20" v="v2"/>
<c id="m8" parent="vC" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,555,280,48" v="docker run &amp;lt;引擎&amp;gt; apply remove &amp;lt;repo&amp;gt;（--dry-run 原樣轉發）"/>
<c id="m8_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,545,30,20" v="v2"/>
<c id="m9a" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,559,400,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="m9a_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,549,30,20" v="v2"/>
<c id="m9b" parent="vC" st="f=#dae8fc;s=#6c8ebf" g="560,632,240,40" v="重驗指紋"/>
<c id="m9b_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,622,30,20" v="v2"/>
<c id="m9x" parent="vC" st="ellipse;f=#ffe6cc;s=#000000" g="820,623,140,58" v="不同 → 1「請重跑」"/>
<c id="m9x_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,613,30,20" v="v2"/>
<c id="m7cx" parent="vC" st="ellipse;f=#ffe6cc;s=#000000" g="20,702,220,80" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）"/>
<c id="m7cx_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,692,30,20" v="v2"/>
<c id="m7c" parent="vC" st="rhombus;f=#FFF4C3;s=#000000" g="560,701,340,81" v="CI 為真（frozen）且需改 tracked 檔？"/>
<c id="m7c_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="876,691,30,20" v="v2"/>
<c id="m7y" parent="vC" st="ellipse;f=#d5e8d4;s=#000000" g="20,802,220,58" v="是 → 0：只印清單（會刪什麼、會問什麼）"/>
<c id="m7y_v2" parent="vC" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,792,30,20" v="v2"/>
<c id="m7" parent="vC" st="rhombus;f=#FFF4C3;s=#000000" g="610,806,240,50" v="--dry-run？"/>
<c id="m7z" parent="vC" st="text;s=none;f=none;b=1" g="560,880,400,42" v="否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌"/>
<c id="me1" edge source="m0" target="m1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me2" edge source="m1" target="m2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.05,0,," pts="420,267;720,267"/>
<c id="me3" edge source="m2" target="m3" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="me4" edge source="m2" target="m4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="me5" edge source="m4" target="m5" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="me6" edge source="m4" target="m6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="me6b" edge source="m6" target="m6b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me6c" edge source="m6b" target="m6c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me6d" edge source="m6c" target="m6d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me7" edge source="m6d" target="m8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,686;420,686"/>
<c id="me8" edge source="m8" target="m9a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me8b" edge source="m9a" target="m9b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me8x" edge source="m9b" target="m9x" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me9" edge source="m9b" target="m7c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me9x" edge source="m7c" target="m7cx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="me9c" edge source="m7c" target="m7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="me10" edge source="m7" target="m7y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="me11" edge source="m7" target="m7z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="p8b_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1085,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8b_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1085,140,64" v="黃：判斷"/>
<c id="p8b_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1093,140,44" v="綠：起點／終點"/>
<c id="p8b_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1087,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8b_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1087,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8b_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1095,88,40" v="白：步驟"/>
<c id="p8b_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1095,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8b_lgt" st="text;s=none;f=none" g="1318,1085,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8b_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1153,120,36" v="便條：補充說明"/>
<c id="p8b_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1153,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8b_lgx_img" st="f=#e1d5e7;s=#9673a6" g="390,1153,170,36" v="紫：image（引擎與工具）"/>
<c id="p8b_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="580,1153,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8b_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="770,1153,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8b_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="946,1143,30,20" v="v2"/>
<c id="p8b_th" st="text;fs=13;s=none;f=none;b=1" g="40,1191,200,28" v="本頁名詞"/>
<c id="p8b_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1225,150,55" v="remove"/>
<c id="p8b_tv0" st="f=#ffffff;s=#999999" g="190,1225,610,55" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單"/>
<c id="p8b_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1280,150,71" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）"/>
<c id="p8b_tv1" st="f=#ffffff;s=#999999" g="190,1280,610,71" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/"/>
<c id="p8b_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1351,150,55" v="resolve／apply／--dry-run"/>
<c id="p8b_tv2" st="f=#ffffff;s=#999999" g="190,1351,610,55" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）"/>
<c id="p8b_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1406,150,71" v="flock／指紋／進度日誌"/>
<c id="p8b_tv3" st="f=#ffffff;s=#999999" g="190,1406,610,71" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）"/>
<c id="p8b_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1477,150,55" v="baseline／metadata"/>
<c id="p8b_tv4" st="f=#ffffff;s=#999999" g="190,1477,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/"/>
<c id="p8b_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1532,150,55" v="append 行／CRLF／三分支"/>
<c id="p8b_tv5" st="f=#ffffff;s=#999999" g="190,1532,610,55" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）"/>
<c id="p8b_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1225,150,40" v="初始檔"/>
<c id="p8b_tv6" st="f=#ffffff;s=#999999" g="990,1225,610,40" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"/>
<c id="p8b_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1265,150,40" v="保護清單／保護模式"/>
<c id="p8b_tv7" st="f=#ffffff;s=#999999" g="990,1265,610,40" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過"/>
<c id="p8b_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1305,150,40" v="dev 覆寫"/>
<c id="p8b_tv8" st="f=#ffffff;s=#999999" g="990,1305,610,40" v="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋"/>
<c id="p8b_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1345,150,71" v="gen／mod?／import"/>
<c id="p8b_tv9" st="f=#ffffff;s=#999999" g="990,1345,610,71" v="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的"/>
<c id="p8b_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1416,150,55" v="CI 為真／frozen"/>
<c id="p8b_tv10" st="f=#ffffff;s=#999999" g="990,1416,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）"/>
<c id="p8b_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1471,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8b_tv11" st="f=#ffffff;s=#999999" g="990,1471,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：remove（2）寫入段">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：remove（2）apply 寫入段（§2、§5；v2.2 C／E、v2.3 §1／§5、v2.5 §3／§11）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="vC2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1128" v="remove &amp;lt;repo&amp;gt;（2）寫入段（承「remove（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 問 append 行（找行 → 命中幾處？）→ 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌"/>
<c id="vC2_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="m9e" parent="vC2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="610,36,300,58" v="來自「remove（1）」頁：apply 檢查通過（非 dry-run）"/>
<c id="m9l" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,114,400,48" v="建進度日誌（.vendor_kit/.tmp.remove.&amp;lt;id&amp;gt;.toml；第一個寫入前）"/>
<c id="m9l_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,104,30,20" v="v2"/>
<c id="m9lf" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,117,360,42" v="＋.vendor_kit/.tmp.remove.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）"/>
<c id="m9h" parent="vC2" st="rhombus;f=#FFF4C3;s=#000000" g="590,182,300,81" v="metadata 有 append 過的行？"/>
<c id="m9h_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,172,30,20" v="v2"/>
<c id="m9q" parent="vC2" st="rhombus;f=#FFF4C3;s=#000000" g="590,283,300,112" v="有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）"/>
<c id="m9q_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="866,273,30,20" v="v2"/>
<c id="m9s" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="640,415,200,48" v="是：找上次插入的行（CRLF／LF 視為相同、其餘精確）"/>
<c id="m9s_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="816,405,30,20" v="v2"/>
<c id="m9mn" parent="vC2" st="shape=note;f=#ffffff;s=#999999" g="1220,418,360,42" v="找行（v2.3 §1）：CRLF／LF 視為相同、其餘精確；唯一命中 → 刪；零命中 → 不刪印清單；多處 → 保留並 warn（Q13）"/>
<c id="m9z" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,495,70,57" v="零命中：不刪、印清單"/>
<c id="m9m" parent="vC2" st="rhombus;f=#FFF4C3;s=#000000" g="670,483,140,81" v="命中幾處？"/>
<c id="m9m_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,473,30,20" v="v2"/>
<c id="m9d" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="860,504,100,40" v="唯一：刪那幾行"/>
<c id="m9f" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,504,360,40" v="初始檔（只移除我們 append 的行；其餘不動；永不刪檔）"/>
<c id="m9w" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="670,604,140,40" v="多處：保留＋warn"/>
<c id="m9w_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,594,30,20" v="v2"/>
<c id="m10a" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="530,664,400,40" v="刪 baseline/&amp;lt;repo&amp;gt;/（含 metadata）"/>
<c id="m10a_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="906,654,30,20" v="v2"/>
<c id="m10af" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,664,360,40" v="－baseline/&amp;lt;repo&amp;gt;/（進 git）"/>
<c id="m10b" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,724,400,40" v="刪 cache/&amp;lt;repo&amp;gt;/"/>
<c id="m10b_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,714,30,20" v="v2"/>
<c id="m10bf" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,724,360,40" v="－cache/&amp;lt;repo&amp;gt;/（不進 git）"/>
<c id="m10c" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,784,400,40" v="刪 gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="m10c_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,774,30,20" v="v2"/>
<c id="m10cf" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,784,360,40" v="－gen/&amp;lt;repo&amp;gt;.stamp（不進 git）"/>
<c id="m10d" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,844,400,40" v="重生 gen/tools.just（去掉該工具所有 mod? 行）"/>
<c id="m10d_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,834,30,20" v="v2"/>
<c id="m10df" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,844,360,40" v="gen/tools.just（不進 git；mod? 行）"/>
<c id="m10e" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,904,400,40" v="最後刪 version.toml 該工具那一行"/>
<c id="m10e_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,894,30,20" v="v2"/>
<c id="m10ef" parent="vC2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,904,360,40" v="－version.toml &amp;lt;repo&amp;gt; 行（進 git）"/>
<c id="m10x" parent="vC2" st="ellipse;f=#f8cecc;s=#000000" g="20,964,220,58" v="失敗 → 1：明列已完成／未完成"/>
<c id="m10x_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,954,30,20" v="v2"/>
<c id="m10g" parent="vC2" st="f=#dae8fc;s=#6c8ebf" g="560,973,400,40" v="刪進度日誌（最後一步）"/>
<c id="m10g_v2" parent="vC2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,963,30,20" v="v2"/>
<c id="m11" parent="vC2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1042,220,80" v="0：印「以下初始檔保留，若不需要請 git rm：…」"/>
<c id="me11e" edge source="m9e" target="m9l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me11f" edge source="m9l" target="m9lf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me11h" edge source="m9l" target="m9h" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me11hn" edge source="m9h" target="m10a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.76,0,," pts="565,364" v="無"/>
<c id="me11q" edge source="m9h" target="m9q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="me12n" edge source="m9q" target="m10a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.73,0,," pts="575,480" v="否"/>
<c id="me12y" edge source="m9q" target="m9s" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="me12m" edge source="m9s" target="m9m" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me13z" edge source="m9m" target="m9z" st="es=orthogonalEdgeStyle;s=default;fc=default" v="零"/>
<c id="me13d" edge source="m9m" target="m9d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="唯一"/>
<c id="me13w" edge source="m9m" target="m9w" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="多處"/>
<c id="me13f" edge source="m9d" target="m9f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me14z" edge source="m9z" target="m10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me14w" edge source="m9w" target="m10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me14d" edge source="m9d" target="m10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me15a" edge source="m10a" target="m10af" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="me15b" edge source="m10a" target="m10b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me15bf" edge source="m10b" target="m10bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="me15c" edge source="m10b" target="m10c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me15cf" edge source="m10c" target="m10cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="me15d" edge source="m10c" target="m10d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me15df" edge source="m10d" target="m10df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="me15e" edge source="m10d" target="m10e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="me15ef" edge source="m10e" target="m10ef" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="me16" edge source="m10e" target="m10g" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="成功"/>
<c id="me16x" edge source="m10e" target="m10x" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,1095;150,1095" v="失敗"/>
<c id="me17" edge source="m10g" target="m11" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="780,1223"/>
<c id="p8b2_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1285,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8b2_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1285,140,64" v="黃：判斷"/>
<c id="p8b2_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1293,140,44" v="綠：起點／終點"/>
<c id="p8b2_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1287,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8b2_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1287,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8b2_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1295,88,40" v="白：步驟"/>
<c id="p8b2_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1295,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8b2_lgt" st="text;s=none;f=none" g="1318,1285,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8b2_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1353,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p8b2_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1353,120,36" v="便條：補充說明"/>
<c id="p8b2_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="400,1353,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8b2_lgx_img" st="f=#e1d5e7;s=#9673a6" g="610,1353,170,36" v="紫：image（引擎與工具）"/>
<c id="p8b2_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="800,1353,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8b2_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="990,1353,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8b2_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1166,1343,30,20" v="v2"/>
<c id="p8b2_th" st="text;fs=13;s=none;f=none;b=1" g="40,1391,200,28" v="本頁名詞"/>
<c id="p8b2_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1425,150,55" v="remove"/>
<c id="p8b2_tv0" st="f=#ffffff;s=#999999" g="190,1425,610,55" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單"/>
<c id="p8b2_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1480,150,71" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）"/>
<c id="p8b2_tv1" st="f=#ffffff;s=#999999" g="190,1480,610,71" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/"/>
<c id="p8b2_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1551,150,55" v="resolve／apply／--dry-run"/>
<c id="p8b2_tv2" st="f=#ffffff;s=#999999" g="190,1551,610,55" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）"/>
<c id="p8b2_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1606,150,71" v="flock／指紋／進度日誌"/>
<c id="p8b2_tv3" st="f=#ffffff;s=#999999" g="190,1606,610,71" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）"/>
<c id="p8b2_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1677,150,55" v="baseline／metadata"/>
<c id="p8b2_tv4" st="f=#ffffff;s=#999999" g="190,1677,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/"/>
<c id="p8b2_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1732,150,55" v="append 行／CRLF／三分支"/>
<c id="p8b2_tv5" st="f=#ffffff;s=#999999" g="190,1732,610,55" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）"/>
<c id="p8b2_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1425,150,40" v="初始檔"/>
<c id="p8b2_tv6" st="f=#ffffff;s=#999999" g="990,1425,610,40" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"/>
<c id="p8b2_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1465,150,40" v="保護清單／保護模式"/>
<c id="p8b2_tv7" st="f=#ffffff;s=#999999" g="990,1465,610,40" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過"/>
<c id="p8b2_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1505,150,40" v="dev 覆寫"/>
<c id="p8b2_tv8" st="f=#ffffff;s=#999999" g="990,1505,610,40" v="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋"/>
<c id="p8b2_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1545,150,71" v="gen／mod?／import"/>
<c id="p8b2_tv9" st="f=#ffffff;s=#999999" g="990,1545,610,71" v="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的"/>
<c id="p8b2_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1616,150,55" v="CI 為真／frozen"/>
<c id="p8b2_tv10" st="f=#ffffff;s=#999999" g="990,1616,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）"/>
<c id="p8b2_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1671,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8b2_tv11" st="f=#ffffff;s=#999999" g="990,1671,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：uninstall（1）resolve → apply 前置">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：uninstall（1）resolve → apply 前置（§2；v2.2 E、v2.3 §6、v2.5 §3／§10）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="vD" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,941" v="uninstall（1）：全部拆掉（install 的反向；bootstrap.sh 的反向也是它）= resolve（預檢 → hash → 保護清單 → 計畫 → 詢問清單 → 指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；寫入段見「uninstall（2）」頁；不 rm -rf .vendor_kit/"/>
<c id="vD_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="x0" parent="vD" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="just vendor_kit uninstall（-y、--dry-run）"/>
<c id="x1" parent="vD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,52,280,48" v="docker run &amp;lt;引擎&amp;gt; resolve uninstall（不經 docker create/cp）"/>
<c id="x1_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,42,30,20" v="v2"/>
<c id="x2x" parent="vD" st="ellipse;f=#ffe6cc;s=#000000" g="20,136,220,80" v="否 → 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）"/>
<c id="x2x_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,126,30,20" v="v2"/>
<c id="x2" parent="vD" st="rhombus;f=#FFF4C3;s=#000000" g="560,151,250,50" v="預檢全部工具通過？"/>
<c id="x2_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="786,141,30,20" v="v2"/>
<c id="x2b" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,236,400,48" v="是：算每個自產檔的 hash（薄殼、version.toml、gen/、cache/、baseline/；不動任何東西）"/>
<c id="x2b_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,226,30,20" v="v2"/>
<c id="x2bb" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,304,400,48" v="分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）"/>
<c id="x2bb_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,294,30,20" v="v2"/>
<c id="x2r" parent="vD" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,304,360,48" v="保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過"/>
<c id="x2r_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,294,30,20" v="v2"/>
<c id="x2c" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,372,400,40" v="產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）"/>
<c id="x2c_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,362,30,20" v="v2"/>
<c id="x2d" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,432,400,48" v="產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 三行"/>
<c id="x2d_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,422,30,20" v="v2"/>
<c id="x2e" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,500,400,48" v="產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）→ 計畫＋詢問清單＋指紋以 stdout 回啟動器"/>
<c id="x2e_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,490,30,20" v="v2"/>
<c id="x1b" parent="vD" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,568,280,48" v="docker run &amp;lt;引擎&amp;gt; apply uninstall（--dry-run 原樣轉發）"/>
<c id="x1b_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="516,558,30,20" v="v2"/>
<c id="x4a" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,572,400,40" v="apply：flock 專案目錄（60 秒）"/>
<c id="x4a_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,562,30,20" v="v2"/>
<c id="x4b" parent="vD" st="f=#dae8fc;s=#6c8ebf" g="560,645,240,40" v="重驗指紋"/>
<c id="x4b_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="776,635,30,20" v="v2"/>
<c id="x4bx" parent="vD" st="ellipse;f=#ffe6cc;s=#000000" g="820,636,140,58" v="不同 → 1「請重跑」"/>
<c id="x4bx_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,626,30,20" v="v2"/>
<c id="x3cx" parent="vD" st="ellipse;f=#ffe6cc;s=#000000" g="20,714,220,80" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）"/>
<c id="x3cx_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,704,30,20" v="v2"/>
<c id="x3c" parent="vD" st="rhombus;f=#FFF4C3;s=#000000" g="560,714,340,81" v="CI 為真（frozen）且需改 tracked 檔？"/>
<c id="x3c_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="876,704,30,20" v="v2"/>
<c id="x3y" parent="vD" st="ellipse;f=#d5e8d4;s=#000000" g="20,815,220,58" v="是 → 0：只印會刪什麼、會問什麼"/>
<c id="x3y_v2" parent="vD" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,805,30,20" v="v2"/>
<c id="x3" parent="vD" st="rhombus;f=#FFF4C3;s=#000000" g="610,819,240,50" v="--dry-run？"/>
<c id="x4z" parent="vD" st="text;s=none;f=none;b=1" g="560,893,400,42" v="否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌"/>
<c id="xe1" edge source="x0" target="x1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe2" edge source="x1" target="x2" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="420,267;705,267"/>
<c id="xe3" edge source="x2" target="x2x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="xe4" edge source="x2" target="x2b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="xe4b" edge source="x2b" target="x2bb" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe4c" edge source="x2bb" target="x2c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe4d" edge source="x2c" target="x2d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe4e" edge source="x2d" target="x2e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe5" edge source="x2e" target="x1b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="660,699;420,699"/>
<c id="xe5b" edge source="x1b" target="x4a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe5c" edge source="x4a" target="x4b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe5x" edge source="x4b" target="x4bx" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe5d" edge source="x4b" target="x3c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe5e" edge source="x3c" target="x3cx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="xe5f" edge source="x3c" target="x3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="xe6" edge source="x3" target="x3y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="xe7" edge source="x3" target="x4z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="p8bc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1098,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8bc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1098,140,64" v="黃：判斷"/>
<c id="p8bc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1106,140,44" v="綠：起點／終點"/>
<c id="p8bc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1100,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8bc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1100,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8bc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1108,88,40" v="白：步驟"/>
<c id="p8bc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1108,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8bc_lgt" st="text;s=none;f=none" g="1318,1098,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8bc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1166,120,36" v="便條：補充說明"/>
<c id="p8bc_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1166,150,36" v="橘框：規則（已定）"/>
<c id="p8bc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1166,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8bc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1166,170,36" v="紫：image（引擎與工具）"/>
<c id="p8bc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1166,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8bc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="940,1166,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8bc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1116,1156,30,20" v="v2"/>
<c id="p8bc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1204,200,28" v="本頁名詞"/>
<c id="p8bc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1238,150,55" v="remove"/>
<c id="p8bc_tv0" st="f=#ffffff;s=#999999" g="190,1238,610,55" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單"/>
<c id="p8bc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1293,150,71" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）"/>
<c id="p8bc_tv1" st="f=#ffffff;s=#999999" g="190,1293,610,71" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/"/>
<c id="p8bc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1364,150,55" v="resolve／apply／--dry-run"/>
<c id="p8bc_tv2" st="f=#ffffff;s=#999999" g="190,1364,610,55" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）"/>
<c id="p8bc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1419,150,71" v="flock／指紋／進度日誌"/>
<c id="p8bc_tv3" st="f=#ffffff;s=#999999" g="190,1419,610,71" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）"/>
<c id="p8bc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1490,150,55" v="baseline／metadata"/>
<c id="p8bc_tv4" st="f=#ffffff;s=#999999" g="190,1490,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/"/>
<c id="p8bc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1545,150,55" v="append 行／CRLF／三分支"/>
<c id="p8bc_tv5" st="f=#ffffff;s=#999999" g="190,1545,610,55" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）"/>
<c id="p8bc_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1238,150,40" v="初始檔"/>
<c id="p8bc_tv6" st="f=#ffffff;s=#999999" g="990,1238,610,40" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"/>
<c id="p8bc_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1278,150,40" v="保護清單／保護模式"/>
<c id="p8bc_tv7" st="f=#ffffff;s=#999999" g="990,1278,610,40" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過"/>
<c id="p8bc_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1318,150,40" v="dev 覆寫"/>
<c id="p8bc_tv8" st="f=#ffffff;s=#999999" g="990,1318,610,40" v="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋"/>
<c id="p8bc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1358,150,71" v="gen／mod?／import"/>
<c id="p8bc_tv9" st="f=#ffffff;s=#999999" g="990,1358,610,71" v="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的"/>
<c id="p8bc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1429,150,55" v="CI 為真／frozen"/>
<c id="p8bc_tv10" st="f=#ffffff;s=#999999" g="990,1429,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）"/>
<c id="p8bc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,1484,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8bc_tv11" st="f=#ffffff;s=#999999" g="990,1484,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：uninstall（2）寫入段">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：uninstall（2）apply 寫入段（§2；v2.2 E、v2.3 §6、v2.5 §3／§10、v2.6 Q22 補、v2.8 §1）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,77" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,97,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,97,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,97,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,97,220,28" v="GHCR"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1240,97,360,28" v="專案目錄"/>
<c id="vD2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,141,1600,1673" v="uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（含 baseline/ 根檔，v2.8 §1）→ justfile 那行、.dockerignore 行問後逐行刪（只刪仍相同的）→ 刪日誌 → 空才 rmdir"/>
<c id="vD2_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,5,30,20" v="v2"/>
<c id="x4e" parent="vD2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="610,36,300,58" v="來自「uninstall（1）」頁：apply 檢查通過（非 dry-run）"/>
<c id="x4l" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,114,400,48" v="建進度日誌（.vendor_kit/.tmp.uninstall.&amp;lt;id&amp;gt;.toml；第一個寫入前）"/>
<c id="x4l_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,104,30,20" v="v2"/>
<c id="x4lf" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,117,360,42" v="＋.vendor_kit/.tmp.uninstall.&amp;lt;id&amp;gt;.toml（進度日誌，不進 git）"/>
<c id="x4x" parent="vD2" st="ellipse;f=#f8cecc;s=#000000" g="20,182,220,58" v="任一失敗 → 1 中止，列出已完成部分"/>
<c id="x4x_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,172,30,20" v="v2"/>
<c id="x4" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,191,400,40" v="逐工具 remove（保護模式；步驟同「remove（2）」頁）"/>
<c id="x4_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,181,30,20" v="v2"/>
<c id="x5a" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,287,400,40" v="全部成功：刪薄殼四檔（hash 相符者）"/>
<c id="x5a_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,277,30,20" v="v2"/>
<c id="x5af" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,260,360,94" v="－.vendor_kit/ 薄殼四檔（保護清單內的保留）"/>
<c id="x5af_0" parent="x5af" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,169,26" v=".gitignore"/>
<c id="x5af_1" parent="x5af" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="183,26,169,26" v="entry.just"/>
<c id="x5af_2" parent="x5af" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,169,26" v="vendor.just"/>
<c id="x5af_3" parent="x5af" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="183,58,169,26" v="ci/check.sh"/>
<c id="x5b" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,374,400,40" v="刪 version.toml（hash 相符者）"/>
<c id="x5b_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,364,30,20" v="v2"/>
<c id="x5bf" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,374,360,40" v="－version.toml（進 git）"/>
<c id="x5c" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,434,400,40" v="刪 version.local.toml（有的話；hash 相符者）"/>
<c id="x5c_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,424,30,20" v="v2"/>
<c id="x5cf" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,434,360,40" v="－version.local.toml（不進 git）"/>
<c id="x5d" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,517,400,48" v="刪 gen/ 與 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）"/>
<c id="x5d_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,507,30,20" v="v2"/>
<c id="x5df" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1220,494,360,94" v="－gen/ 兩檔（不進 git）、baseline/ 根檔（進 git）"/>
<c id="x5df_0" parent="x5df" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,140,26" v="gen/.stamp"/>
<c id="x5df_1" parent="x5df" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="154,26,198,26" v="gen/tools.just"/>
<c id="x5df_2" parent="x5df" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,140,26" v="baseline/.gitkeep"/>
<c id="x5df_3" parent="x5df" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="154,58,198,26" v="baseline/.vendor_kit.toml"/>
<c id="x5dd" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,608,400,48" v="刪已空的子目錄 baseline/（gen/、cache/、ci/ 亦同；rmdir，不 rm -rf）"/>
<c id="x5dd_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,598,30,20" v="v2"/>
<c id="x6" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="700,676,260,112" v="根 justfile 有我們寫的那一行（完全相同）？"/>
<c id="x5r" parent="vD2" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,700,360,63" v="初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）"/>
<c id="x5r_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,690,30,20" v="v2"/>
<c id="x8" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,828,100,73" v="無／否：印指示（請自行移除 import 那行）"/>
<c id="x7" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="700,808,260,112" v="有 → 問「要刪這一行嗎」同意？（-y 免問）"/>
<c id="x7_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,798,30,20" v="v2"/>
<c id="x7y" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="760,941,140,40" v="是：只刪那一行"/>
<c id="x7f" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,940,360,42" v="justfile（少一行：import &#x27;.vendor_kit/entry.just&#x27;）"/>
<c id="x9a" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="680,1002,260,81" v="根 .dockerignore 存在？"/>
<c id="x9a_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="916,992,30,20" v="v2"/>
<c id="x9b" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="680,1103,260,143" v="有 → 逐行比對：仍有與紀錄原文相同的行？（CRLF／LF 等價）"/>
<c id="x9b_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="916,1093,30,20" v="v2"/>
<c id="x9r" parent="vD2" st="f=#ffe6cc;s=#d79b00;b=1" g="1220,1143,360,63" v="append 行逐行比對（§4.3、v2.9 §5）：對紀錄的每一行 —— 仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動"/>
<c id="x9r_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,1133,30,20" v="v2"/>
<c id="x9q" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="680,1266,260,112" v="有 → 問「要刪這幾行嗎」同意？（-y 免問）"/>
<c id="x9q_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="916,1256,30,20" v="v2"/>
<c id="x9z" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,1398,110,48" v="無／否：不動 .dockerignore"/>
<c id="x9z_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="646,1388,30,20" v="v2"/>
<c id="x9y" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="730,1398,230,48" v="是：逐行只刪仍相同的行；不同／缺的行跳過 warn"/>
<c id="x9y_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1388,30,20" v="v2"/>
<c id="x9f" parent="vD2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1220,1402,360,40" v=".dockerignore（只少仍相同的那幾行；其餘不動）"/>
<c id="x9f_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1556,1392,30,20" v="v2"/>
<c id="x5z" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,1466,400,40" v="刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成"/>
<c id="x5z_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1456,30,20" v="v2"/>
<c id="x5n" parent="vD2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1526,220,80" v="否 → 0：保留目錄與保護清單內的檔並回報；印摘要"/>
<c id="x5n_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1516,30,20" v="v2"/>
<c id="x5q" parent="vD2" st="rhombus;f=#FFF4C3;s=#000000" g="560,1526,205,81" v=".vendor_kit/ 已空？"/>
<c id="x5q_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="741,1516,30,20" v="v2"/>
<c id="x5y" parent="vD2" st="ellipse;f=#d5e8d4;s=#000000" g="20,1627,220,40" v="0：印摘要"/>
<c id="x5y_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="216,1617,30,20" v="v2"/>
<c id="x5t" parent="vD2" st="f=#dae8fc;s=#6c8ebf" g="560,1627,400,40" v="是：刪空目錄（rmdir；不 rm -rf）"/>
<c id="x5t_v2" parent="vD2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="936,1617,30,20" v="v2"/>
<c id="xe7" edge source="x4e" target="x4l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe7f" edge source="x4l" target="x4lf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="xe8" edge source="x4l" target="x4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe9" edge source="x4" target="x4x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="失敗"/>
<c id="xe10" edge source="x4" target="x5a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe10f" edge source="x5a" target="x5af" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="xe10b" edge source="x5a" target="x5b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe10bf" edge source="x5b" target="x5bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="xe10c" edge source="x5b" target="x5c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe10cf" edge source="x5c" target="x5cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="xe10d" edge source="x5c" target="x5d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe10df" edge source="x5d" target="x5df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="xe10e" edge source="x5d" target="x5dd" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe12" edge source="x5dd" target="x6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="780,807;850,807"/>
<c id="xe13" edge source="x6" target="x8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.12,0,," pts="630,873" v="無"/>
<c id="xe14" edge source="x6" target="x7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="xe14n" edge source="x7" target="x8" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="xe14y" edge source="x7" target="x7y" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="xe15" edge source="x7y" target="x7f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="xe16z" edge source="x8" target="x9a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.27,0,," pts="630,1133;830,1133"/>
<c id="xe16y" edge source="x7y" target="x9a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe16a" edge source="x9a" target="x9b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="xe16b" edge source="x9b" target="x9q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="xe16q" edge source="x9q" target="x9y" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="xe16f" edge source="x9y" target="x9f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="xe16an" edge source="x9a" target="x9z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.62,0,," pts="635,1184" v="無"/>
<c id="xe16bn" edge source="x9b" target="x9z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.45,0,," pts="635,1316" v="無"/>
<c id="xe16qn" edge source="x9q" target="x9z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="830,1529;635,1529" v="否"/>
<c id="xe16v" edge source="x9y" target="x5z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe16w" edge source="x9z" target="x5z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe17" edge source="x5z" target="x5q" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="xe18" edge source="x5q" target="x5n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="xe19" edge source="x5q" target="x5t" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="xe20" edge source="x5t" target="x5y" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p8bcc_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1830,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p8bcc_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1830,140,64" v="黃：判斷"/>
<c id="p8bcc_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1838,140,44" v="綠：起點／終點"/>
<c id="p8bcc_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1832,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p8bcc_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1832,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p8bcc_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1840,88,40" v="白：步驟"/>
<c id="p8bcc_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1840,170,40" v="虛線框：專案裡的檔案"/>
<c id="p8bcc_lgt" st="text;s=none;f=none" g="1318,1830,300,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p8bcc_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="40,1898,200,36" v="虛線橢圓：跨頁入口"/>
<c id="p8bcc_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="260,1898,120,36" v="便條：補充說明"/>
<c id="p8bcc_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="400,1898,150,36" v="橘框：規則（已定）"/>
<c id="p8bcc_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="570,1898,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p8bcc_lgx_img" st="f=#e1d5e7;s=#9673a6" g="780,1898,170,36" v="紫：image（引擎與工具）"/>
<c id="p8bcc_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="970,1898,170,36" v="灰底：泳道／表格表頭"/>
<c id="p8bcc_lgx_v2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1160,1898,200,36" v="右上綠標 v2：與 v1 不同處"/>
<c id="p8bcc_lgx_v2_v2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1336,1888,30,20" v="v2"/>
<c id="p8bcc_th" st="text;fs=13;s=none;f=none;b=1" g="40,1936,200,28" v="本頁名詞"/>
<c id="p8bcc_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1970,150,55" v="remove"/>
<c id="p8bcc_tv0" st="f=#ffffff;s=#999999" g="190,1970,610,55" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&amp;lt;repo&amp;gt;/、cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單"/>
<c id="p8bcc_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2025,150,71" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）"/>
<c id="p8bcc_tv1" st="f=#ffffff;s=#999999" g="190,2025,610,71" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/"/>
<c id="p8bcc_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2096,150,55" v="resolve／apply／--dry-run"/>
<c id="p8bcc_tv2" st="f=#ffffff;s=#999999" g="190,2096,610,55" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）"/>
<c id="p8bcc_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2151,150,71" v="flock／指紋／進度日誌"/>
<c id="p8bcc_tv3" st="f=#ffffff;s=#999999" g="190,2151,610,71" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml，因 metadata 會被刪）"/>
<c id="p8bcc_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2222,150,55" v="baseline／metadata"/>
<c id="p8bcc_tv4" st="f=#ffffff;s=#999999" g="190,2222,610,55" v="baseline/&amp;lt;repo&amp;gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&amp;lt;repo&amp;gt;/"/>
<c id="p8bcc_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2277,150,55" v="append 行／CRLF／三分支"/>
<c id="p8bcc_tv5" st="f=#ffffff;s=#999999" g="190,2277,610,55" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）"/>
<c id="p8bcc_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1970,150,40" v="初始檔"/>
<c id="p8bcc_tv6" st="f=#ffffff;s=#999999" g="990,1970,610,40" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"/>
<c id="p8bcc_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2010,150,40" v="保護清單／保護模式"/>
<c id="p8bcc_tv7" st="f=#ffffff;s=#999999" g="990,2010,610,40" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過"/>
<c id="p8bcc_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2050,150,40" v="dev 覆寫"/>
<c id="p8bcc_tv8" st="f=#ffffff;s=#999999" g="990,2050,610,40" v="version.local.toml 的 &amp;lt;repo&amp;gt; = &quot;path:&amp;lt;dir&amp;gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋"/>
<c id="p8bcc_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2090,150,71" v="gen／mod?／import"/>
<c id="p8bcc_tv9" st="f=#ffffff;s=#999999" g="990,2090,610,71" v="gen/tools.just 每個 &amp;lt;ns&amp;gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的"/>
<c id="p8bcc_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2161,150,55" v="CI 為真／frozen"/>
<c id="p8bcc_tv10" st="f=#ffffff;s=#999999" g="990,2161,610,55" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）"/>
<c id="p8bcc_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2216,150,55" v="結束狀態 0／1／2／3"/>
<c id="p8bcc_tv11" st="f=#ffffff;s=#999999" g="990,2216,610,55" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）"/>
</page>
<page name="流程 v2：prune">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：prune ── 依 label 清未引用的 docker 資源（interface_spec §1.2、§3.3 keep、§4.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,132" v="已定（v2.4-10、grilling 9 修正／補充、Q24、Q25、interface_spec A1、v2.7-7）：prune 第一版做；所有 vendor_kit 建的 docker 資源帶 label；prune 依 label 掃四類資源、刪 version.toml／local 未引用者；docker 指令由啟動器執行（不掛 socket）；image 只刪帶 label 且本專案未引用者（共享 daemon 提醒）；活躍的 .tmp.* 只列出不刪、不視為未完成交易；prune 自己的 apply 也走進度日誌（建 .tmp.prune.&amp;lt;id&amp;gt;.toml → 清理 → 刪日誌；v2.9-6）；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run（無 -n）。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,152,200,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="260,152,300,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,152,340,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="940,152,300,28" v="docker daemon"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1260,152,330,28" v="專案目錄"/>
<c id="bP" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,196,1590,1678" v="prune [-y] [--dry-run]：引擎 resolve 算保留清單（不寫）→ 啟動器依 label 列四類資源 → 差集 → 問後逐類刪 → 引擎 apply（flock → 重驗指紋 → 建 .tmp.prune.&amp;lt;id&amp;gt;.toml → 清 .tmp.dist.* → 清殘留 .tmp.* → 刪日誌）→ 摘要"/>
<c id="bP_v2" parent="bP" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="q0" parent="bP" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,200,80" v="just vendor_kit prune（-y／--dry-run）"/>
<c id="q1" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,55,300,42" v="docker run &amp;lt;引擎&amp;gt; resolve prune（永不 -t）"/>
<c id="q2" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,55,340,42" v="resolve（不寫任何檔）：讀 version.toml、version.local.toml"/>
<c id="q3" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,166,340,42" v="算保留清單 keep：引擎 ref、[tools] 每個工具 ref、local 覆寫的 vendor_kit &amp;lt;tag&amp;gt;"/>
<c id="q3f" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1240,132,330,110" v="只讀（不寫）"/>
<c id="q3f_0" parent="q3f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,302,26" v="version.toml（引擎 ref、[tools]）"/>
<c id="q3f_1" parent="q3f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,58,302,42" v="version.local.toml（vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot;）"/>
<c id="q4" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,258,340,42" v="偵測活躍（未恢復）的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml → 只列出、印 6-33（不刪、不視為未完成交易）"/>
<c id="q4f" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,258,330,42" v=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（活躍交易：保留）"/>
<c id="q5" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,316,340,42" v="stdout vk-resolve/1：keep|&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt;…、fingerprint、apply|yes、end|N"/>
<c id="q6" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,374,300,42" v="收完整份、驗首尾與筆數（不合 → 1 + 6-30，不動 docker）"/>
<c id="q7" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,448,300,57" v="docker container／image／network／volume ls --filter label=io.github.&amp;lt;org&amp;gt;.vendor_kit=1"/>
<c id="q7d" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="920,455,300,42" v="列出帶 label 的四類資源：容器、image、network、volume"/>
<c id="q7n" parent="bP" st="shape=note;f=#ffffff;s=#999999" g="1240,432,330,88" v="所有 vendor_kit 建的資源都帶 label（容器／network／volume 另加 .project=&amp;lt;專案根&amp;gt;）；不建 network／volume，若意外建立也要能刪（驗收 §7.4-23：故意留一個帶 label 的 network／volume，prune 後必須消失）"/>
<c id="q8" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,544,300,57" v="差集 = 候選 − keep（image：帶 label 且本專案未引用；容器／network／volume：帶 label 者）"/>
<c id="q8n" parent="bP" st="shape=note;f=#ffffff;s=#999999" g="920,536,300,73" v="共享 daemon 提醒：image 沒有 .project label，其他專案是否引用同一 image 不可知 → 只刪帶 label 且本專案未引用者；先 --dry-run 看；被刪的 image 下次 sync 會再拉"/>
<c id="q9y" parent="bP" st="ellipse;f=#d5e8d4;s=#000000" g="20,625,200,58" v="是 → 0：只列出會刪什麼（零刪除）"/>
<c id="q9" parent="bP" st="rhombus;f=#FFF4C3;s=#000000" g="290,629,200,50" v="--dry-run？"/>
<c id="q10n" parent="bP" st="ellipse;f=#d5e8d4;s=#000000" g="20,736,200,40" v="否 → 0：不刪、印清單"/>
<c id="q10" parent="bP" st="rhombus;f=#FFF4C3;s=#000000" g="240,715,300,81" v="問 6-32：要刪除以上資源嗎？（-y 免問）"/>
<c id="q11l" parent="bP" st="text;s=none;f=none;b=1" g="240,812,300,26" v="是 ↓ 對四類資源逐類刪（失敗的記下、續刪其餘）"/>
<c id="q11a" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,854,300,40" v="docker rm &amp;lt;差集內的容器&amp;gt;"/>
<c id="q11ad" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="920,854,300,40" v="容器被刪"/>
<c id="q11b" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,910,300,40" v="docker image rm &amp;lt;差集內的 image&amp;gt;"/>
<c id="q11bd" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="920,910,300,40" v="image 被刪（keep 內的 image 保留）"/>
<c id="q11c" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,966,300,40" v="docker network rm &amp;lt;差集內的 network&amp;gt;"/>
<c id="q11cd" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="920,966,300,40" v="network 被刪"/>
<c id="q11d" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,1022,300,40" v="docker volume rm &amp;lt;差集內的 volume&amp;gt;"/>
<c id="q11dd" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="920,1022,300,40" v="volume 被刪"/>
<c id="q12" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="240,1079,300,40" v="docker run &amp;lt;引擎&amp;gt; apply prune"/>
<c id="q12a" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1078,340,42" v="apply prune：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）"/>
<c id="q12b" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1136,340,42" v="重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）"/>
<c id="q12j" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1194,340,42" v="建進度日誌 .tmp.prune.&amp;lt;id&amp;gt;.toml（第一個寫入前；state=in-progress、done／pending）"/>
<c id="q12jf" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1194,330,42" v="＋.vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（prune 自己的交易日誌）"/>
<c id="q12c" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1252,340,40" v="刪失效的啟動器暫存 .tmp.dist.*／（trap 沒清到的）"/>
<c id="q12cf" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1252,330,40" v=".vendor_kit/.tmp.dist.&amp;lt;id&amp;gt;/（刪）"/>
<c id="q12c2" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1309,340,40" v="進度日誌記 done：清 .tmp.dist.*"/>
<c id="q12c2f" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1308,330,42" v=".vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（done 加一筆）"/>
<c id="q12d" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1366,340,42" v="刪已完成交易殘留的 .tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（活躍的不刪，只列出）"/>
<c id="q12df" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1366,330,42" v=".vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（殘留：刪；活躍：保留）"/>
<c id="q12d2" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1425,340,40" v="進度日誌記 done：清殘留 .tmp.&amp;lt;verb&amp;gt;.*"/>
<c id="q12d2f" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1424,330,42" v=".vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（done 加一筆）"/>
<c id="q12k" parent="bP" st="f=#dae8fc;s=#6c8ebf" g="560,1482,340,42" v="刪進度日誌 .tmp.prune.&amp;lt;id&amp;gt;.toml（最後一步）= 交易完成"/>
<c id="q12kf" parent="bP" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1240,1483,330,40" v="－.vendor_kit/.tmp.prune.&amp;lt;id&amp;gt;.toml（刪）"/>
<c id="q13x" parent="bP" st="ellipse;f=#f8cecc;s=#000000" g="20,1540,200,58" v="是 → 1：摘要全列，失敗的標出"/>
<c id="q13" parent="bP" st="rhombus;f=#FFF4C3;s=#000000" g="290,1544,200,50" v="有刪除失敗？"/>
<c id="q14" parent="bP" st="ellipse;f=#d5e8d4;s=#000000" g="20,1614,200,58" v="否 → 0：印刪了什麼、保留什麼（含原因）"/>
<c id="qe0" edge source="q0" target="q1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe1" edge source="q1" target="q2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe2" edge source="q2" target="q3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe3" edge source="q3" target="q3f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="讀"/>
<c id="qe4" edge source="q3" target="q4" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe5" edge source="q4" target="q4f" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe6" edge source="q4" target="q5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe7" edge source="q5" target="q6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.84,0,," pts="750,591"/>
<c id="qe8" edge source="q6" target="q7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe9" edge source="q7" target="q7d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="ls"/>
<c id="qe10" edge source="q7" target="q8" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe11" edge source="q8" target="q9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe12" edge source="q9" target="q9y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="qe13" edge source="q9" target="q10" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="qe14" edge source="q10" target="q10n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="qe15" edge source="q10" target="q11l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe15a" edge source="q11l" target="q11a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe16a" edge source="q11a" target="q11ad" st="es=orthogonalEdgeStyle;s=default;fc=default" v="rm"/>
<c id="qe16b" edge source="q11a" target="q11b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe16c" edge source="q11b" target="q11bd" st="es=orthogonalEdgeStyle;s=default;fc=default" v="rm"/>
<c id="qe16d" edge source="q11b" target="q11c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe16e" edge source="q11c" target="q11cd" st="es=orthogonalEdgeStyle;s=default;fc=default" v="rm"/>
<c id="qe16f" edge source="q11c" target="q11d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe16g" edge source="q11d" target="q11dd" st="es=orthogonalEdgeStyle;s=default;fc=default" v="rm"/>
<c id="qe17" edge source="q11d" target="q12" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe18" edge source="q12" target="q12a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe18a" edge source="q12a" target="q12b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe18j" edge source="q12b" target="q12j" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19j" edge source="q12j" target="q12jf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="建"/>
<c id="qe18b" edge source="q12j" target="q12c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19" edge source="q12c" target="q12cf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="qe18c2" edge source="q12c" target="q12c2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19c2" edge source="q12c2" target="q12c2f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="qe18c" edge source="q12c2" target="q12d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19d" edge source="q12d" target="q12df" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="qe18d2" edge source="q12d" target="q12d2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19d2" edge source="q12d2" target="q12d2f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="qe18k" edge source="q12d2" target="q12k" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="qe19k" edge source="q12k" target="q12kf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="qe20" edge source="q12k" target="q13" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="410,1699"/>
<c id="qe21" edge source="q13" target="q13x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="qe22" edge source="q13" target="q14" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.78,0,," pts="410,1839" v="否"/>
<c id="p9_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1890,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p9_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1890,140,64" v="黃：判斷"/>
<c id="p9_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1898,140,44" v="綠：起點／終點"/>
<c id="p9_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1892,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p9_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1892,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p9_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1900,88,40" v="白：步驟"/>
<c id="p9_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1900,170,40" v="虛線框：專案裡的檔案"/>
<c id="p9_lgt" st="text;s=none;f=none" g="1318,1890,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p9_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1958,120,36" v="便條：補充說明"/>
<c id="p9_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="180,1958,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p9_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="390,1958,170,36" v="灰底：泳道／表格表頭"/>
<c id="p9_th" st="text;fs=13;s=none;f=none;b=1" g="40,1996,200,28" v="本頁名詞"/>
<c id="p9_tk0" st="f=#ffffff;s=#999999;b=1" g="40,2030,150,55" v="prune"/>
<c id="p9_tv0" st="f=#ffffff;s=#999999" g="190,2030,610,55" v="清掉本專案不再引用的 docker 資源與殘留暫存：兩段（resolve prune 出 keep 清單 → 啟動器 docker ls／rm → apply prune 清 .tmp.*）；-y 免問、--dry-run 只列出零刪除（無短形）；結束 0／1／3"/>
<c id="p9_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2085,150,40" v="keep 清單"/>
<c id="p9_tv1" st="f=#ffffff;s=#999999" g="190,2085,610,40" v="vk-resolve 的 keep|&amp;lt;name&amp;gt;|&amp;lt;ref&amp;gt; 記錄：version.toml 引擎 ref、[tools] 每個工具 ref、version.local.toml 覆寫的 vendor_kit &amp;lt;tag&amp;gt;；這些 image 不可刪"/>
<c id="p9_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2125,150,55" v="docker label"/>
<c id="p9_tv2" st="f=#ffffff;s=#999999" g="190,2125,610,55" v="啟動器建的每個 docker 資源都帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1；容器／network／volume 另加 ….project=&amp;lt;專案根絕對路徑&amp;gt;；工具 image 由 Dockerfile.dist 的 LABEL 帶（check.sh --dist 擋缺 LABEL）；引擎 image 另帶 ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;"/>
<c id="p9_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2180,150,55" v="差集"/>
<c id="p9_tv3" st="f=#ffffff;s=#999999" g="190,2180,610,55" v="候選（依 label 列出的四類資源）扣掉 keep：image 只刪「帶 label 且本專案未引用」者；容器／network／volume 依 label 刪；vendor_kit 不建 network／volume，若意外建立也要能刪（驗收 §7.4-23）"/>
<c id="p9_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2235,150,40" v="共享 daemon"/>
<c id="p9_tv4" st="f=#ffffff;s=#999999" g="190,2235,610,40" v="一台 docker daemon 被多個專案共用：image 上沒有 .project label，其他專案是否引用同一 image 不可知 → 文件明寫、先 --dry-run 看；被刪的 image 下次 sync 會再拉（已釋出 image 永不刪）"/>
<c id="p9_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2275,150,71" v=".tmp.* 日誌／.tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p9_tv5" st="f=#ffffff;s=#999999" g="190,2275,610,71" v="前者 = 修復型 install／remove／uninstall／undev／prune 的進度日誌，未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；prune 自己的交易也建 .tmp.prune.&amp;lt;id&amp;gt;.toml（清理前建、清理後刪；v2.9-6）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清"/>
<c id="p9_tk6" st="f=#ffffff;s=#999999;b=1" g="840,2030,150,55" v="resolve／apply（兩段）"/>
<c id="p9_tv6" st="f=#ffffff;s=#999999" g="990,2030,610,55" v="同一動詞分兩段：引擎 resolve 只讀只算，stdout 回 vk-resolve/1 清單（永不 -t）；啟動器先收完整份、驗首尾與筆數才動 docker；apply 拿 flock、重驗指紋後才寫；--dry-run（無短形）= apply 的唯讀預覽"/>
<c id="p9_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2085,150,55" v="指紋／flock"/>
<c id="p9_tv7" st="f=#ffffff;s=#999999" g="990,2085,610,55" v="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎"/>
<c id="p9_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2140,150,55" v="6-N 訊息編號"/>
<c id="p9_tv8" st="f=#ffffff;s=#999999" g="990,2140,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p9_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2195,150,55" v="docker ls／rm（主機命令白名單）"/>
<c id="p9_tv9" st="f=#ffffff;s=#999999" g="990,2195,610,55" v="啟動器只用白名單命令：docker {container,image,network,volume} ls --filter label=…、docker rm／image rm／network rm／volume rm；逐類資源一次一個命令；不把 docker socket 掛進引擎（引擎不碰 daemon）"/>
<c id="p9_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2250,150,71" v="結束碼 0／1／2／3"/>
<c id="p9_tv10" st="f=#ffffff;s=#999999" g="990,2250,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="流程 v2：update">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,100" v="已定（Q11、Q27、v2.6-5、v2.7-8、v2.8-7、interface_spec §1.2 update）：無憑證時不支援需認證的版本列舉，該工具直接記失敗 1 + 6-3（不進 SemVer 解析；需人動作 → 橙），其他工具照查再彙總；token 只在 update／upgrade 的 resolve 階段以 -e 傳（TOKEN_FILE 用 -v 掛）；update 唯讀、不受 frozen 限制；有新版只在 --exit-code 時回 2；末行固定印 6-15。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,120,220,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,120,280,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="580,120,400,28" v="引擎容器"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1000,120,290,28" v="registry（GHCR）"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1310,120,280,28" v="專案目錄"/>
<c id="bU" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,164,1590,1325" v="update [&amp;lt;repo&amp;gt;] [--exit-code]：引擎查 registry（公開／有 token → 解析 SemVer；無憑證 → 直接記該目標失敗 6-3）→ 每個目標彙總（Q27）→ 末行 6-15 → 結束碼 0／1／2／3"/>
<c id="bU_v2" parent="bU" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="u0" parent="bU" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="just vendor_kit update [&amp;lt;repo&amp;gt;] [--exit-code]"/>
<c id="u1" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,40,280,73" v="組 docker run 引數：-e VENDOR_KIT_REGISTRY_TOKEN／_USER，或 -v &amp;lt;TOKEN_FILE&amp;gt;:/run/vk-token:ro（只在 update／upgrade 的 resolve 傳）"/>
<c id="u1r" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,136,280,42" v="docker run &amp;lt;引擎&amp;gt; update（單段、不經 create/cp）"/>
<c id="u2" parent="bU" st="f=#dae8fc;s=#6c8ebf" g="560,137,400,40" v="update（唯讀；不受 frozen 限制）：讀 version.toml 現版"/>
<c id="u2f" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1290,137,280,40" v="version.toml（只讀：引擎 ref、[tools]）"/>
<c id="u3x" parent="bU" st="ellipse;f=#ffe6cc;s=#000000" g="20,214,220,80" v="是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）"/>
<c id="u3" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="560,198,400,112" v="有未完成交易（.tmp.&amp;lt;verb&amp;gt;.*.toml／[progress]）？"/>
<c id="u4l" parent="bU" st="text;s=none;f=none;b=1" g="560,330,400,42" v="否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）"/>
<c id="u5" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="606,392,300,81" v="registry 不要求認證（公開）？"/>
<c id="u5g" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1110,404,160,57" v="是：GET /v2/&amp;lt;name&amp;gt;/tags/list（分頁）"/>
<c id="u6" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="560,513,392,112" v="有 VENDOR_KIT_REGISTRY_TOKEN／_TOKEN_FILE？"/>
<c id="u6g" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="980,532,132,73" v="是：WWW-Authenticate 換 token → tags/list"/>
<c id="u6r" parent="bU" st="f=#ffe6cc;s=#d79b00;b=1" g="1290,525,280,88" v="已定（Q11）：無憑證時不支援需認證的版本列舉；token 只在 update／upgrade 的 resolve 階段以 -e 傳，不寫 log、不傳給工具；GHCR 已測試，其他 registry 依標準協定可用但未驗證"/>
<c id="u7" parent="bU" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="560,645,240,57" v="否：無憑證、不查 → 該目標記「查詢失敗 1 + 6-3」（不進 SemVer 解析）→ 下一目標／彙總"/>
<c id="u8a" parent="bU" st="f=#dae8fc;s=#6c8ebf" g="810,722,150,42" v="取 SemVer 最大正式版（排除預發行）"/>
<c id="u8b" parent="bU" st="f=#dae8fc;s=#6c8ebf" g="810,784,150,42" v="與現版比較 → 記「現版 → 最新」"/>
<c id="u8q" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="610,846,300,50" v="還有下一個目標？"/>
<c id="u9" parent="bU" st="f=#dae8fc;s=#6c8ebf" g="560,916,400,42" v="否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的 6-3）；訊息全列"/>
<c id="u10" parent="bU" st="f=#dae8fc;s=#6c8ebf" g="560,978,400,40" v="末行固定印 6-15：「套用：just vendor_kit upgrade」"/>
<c id="u11x" parent="bU" st="ellipse;f=#ffe6cc;s=#000000" g="20,1038,220,102" v="是 → 1：查詢失敗（6-3：設 token 或指定 &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;；即使另有新版）"/>
<c id="u11" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="560,1048,300,81" v="任一目標查詢失敗（1）？"/>
<c id="u12y" parent="bU" st="ellipse;f=#ffe6cc;s=#000000" g="20,1172,220,58" v="是 → 2：有新版（給 CI 用）"/>
<c id="u12" parent="bU" st="rhombus;f=#FFF4C3;s=#000000" g="560,1160,300,81" v="有新版且 --exit-code？"/>
<c id="u13" parent="bU" st="ellipse;f=#d5e8d4;s=#000000" g="20,1261,220,58" v="否 → 0：已列出（有新版也 0）"/>
<c id="ue0" edge source="u0" target="u1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue0b" edge source="u1" target="u1r" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue1" edge source="u1r" target="u2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue2" edge source="u2" target="u2f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="讀"/>
<c id="ue3" edge source="u2" target="u3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue4" edge source="u3" target="u3x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue5" edge source="u3" target="u4l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue6" edge source="u4l" target="u5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue7" edge source="u5" target="u5g" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue8" edge source="u5" target="u6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ue9" edge source="u6" target="u6g" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue10" edge source="u6" target="u7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ue11" edge source="u5g" target="u8a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.45,0,," pts="1210,907"/>
<c id="ue12" edge source="u6g" target="u8a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.38,0,," pts="1066,907"/>
<c id="ue13" edge source="u7" target="u8q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="記失敗"/>
<c id="ue13b" edge source="u8a" target="u8b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue14" edge source="u8b" target="u8q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="905,1000;780,1000"/>
<c id="ue14y" edge source="u8q" target="u5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.73,0,," pts="570,1035;570,596" v="是：下一個目標"/>
<c id="ue14n" edge source="u8q" target="u9" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ue15" edge source="u9" target="u10" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue16" edge source="u10" target="u11" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ue17" edge source="u11" target="u11x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue18" edge source="u11" target="u12" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="ue19" edge source="u12" target="u12y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="ue20" edge source="u12" target="u13" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.91,0,," pts="730,1454" v="否"/>
<c id="p10_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1505,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p10_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1505,140,64" v="黃：判斷"/>
<c id="p10_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1513,140,44" v="綠：起點／終點"/>
<c id="p10_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1507,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p10_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1507,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p10_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1515,88,40" v="白：步驟"/>
<c id="p10_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1515,170,40" v="虛線框：專案裡的檔案"/>
<c id="p10_lgt" st="text;s=none;f=none" g="1318,1505,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p10_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1573,120,36" v="便條：補充說明"/>
<c id="p10_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1573,150,36" v="橘框：規則（已定）"/>
<c id="p10_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1573,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p10_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="560,1573,170,36" v="灰底：泳道／表格表頭"/>
<c id="p10_th" st="text;fs=13;s=none;f=none;b=1" g="40,1611,200,28" v="本頁名詞"/>
<c id="p10_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1645,150,55" v="update"/>
<c id="p10_tv0" st="f=#ffffff;s=#999999" g="190,1645,610,55" v="只查 registry 有沒有新版、不動任何檔（唯讀，不受 frozen 限制）；單段 docker run（不經 docker create/cp）；[&amp;lt;repo&amp;gt;] 省略 = 全部工具 + vendor_kit 自身；--exit-code：有新版回 2（給 CI 用）"/>
<c id="p10_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1700,150,55" v="查最新"/>
<c id="p10_tv1" st="f=#ffffff;s=#999999" g="190,1700,610,55" v="對 registry 走 Docker Registry 標準協定：需要時以 WWW-Authenticate 換 token → GET /v2/&amp;lt;name&amp;gt;/tags/list（分頁）→ 取 SemVer 最大正式版（排除預發行）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」；查詢步驟畫白格（不是 image）"/>
<c id="p10_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1755,150,55" v="registry 憑證（Q11）"/>
<c id="p10_tv2" st="f=#ffffff;s=#999999" g="190,1755,610,55" v="VENDOR_KIT_REGISTRY_TOKEN（+ _USER）或 VENDOR_KIT_REGISTRY_TOKEN_FILE（啟動器 -v &amp;lt;file&amp;gt;:/run/vk-token:ro 掛入；兩者同設 → 1）；只在 update／upgrade 的 resolve 階段以 -e 傳入引擎；不寫 log／檔、不傳給工具、dry-run 不印；不掛 ~/.docker/config.json"/>
<c id="p10_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1810,150,55" v="6-3"/>
<c id="p10_tv3" st="f=#ffffff;s=#999999" g="190,1810,610,55" v="無法列舉 &amp;lt;repo&amp;gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;（拉取使用主機 docker 認證）"/>
<c id="p10_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1865,150,40" v="多工具彙總（Q27）"/>
<c id="p10_tv4" st="f=#ffffff;s=#999999" g="190,1865,610,40" v="做得完的做完；最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」"/>
<c id="p10_tk5" st="f=#ffffff;s=#999999;b=1" g="840,1645,150,28" v="6-15（末行固定）"/>
<c id="p10_tv5" st="f=#ffffff;s=#999999" g="990,1645,610,28" v="update 最後一行永遠印「套用：just vendor_kit upgrade」"/>
<c id="p10_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1673,150,55" v="未完成交易（6-33）"/>
<c id="p10_tv6" st="f=#ffffff;s=#999999" g="990,1673,610,55" v="唯讀動詞（sync／update／help）偵測到 .tmp.&amp;lt;verb&amp;gt;.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;」，不自動恢復、不寫檔；update 結束 1"/>
<c id="p10_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1728,150,40" v="frozen"/>
<c id="p10_tv7" st="f=#ffffff;s=#999999" g="990,1728,610,40" v="CI 非空且不為 0／false → frozen：不寫 tracked 檔、不查最新版；update 是唯讀動詞，不受 frozen 影響（CI 裡也能查）"/>
<c id="p10_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1768,150,55" v="6-N 訊息編號"/>
<c id="p10_tv8" st="f=#ffffff;s=#999999" g="990,1768,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p10_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1823,150,71" v="結束碼 0／1／2／3"/>
<c id="p10_tv9" st="f=#ffffff;s=#999999" g="990,1823,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="狀態機 v2：初始檔五態">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="狀態機 v2：初始檔五態 ── metadata [[file]].state 與轉移（interface_spec §4.3、Q14／Q15、v2.7-3）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,100" v="已定（Q14、Q15、v2.6 16 條、v2.7-3、interface_spec §4.3）：metadata 對每個範本記單一 state（五值）+ declined_hash + lines；declined 只用於新檔被拒、從未建立；已納管檔拒絕換版／合併時 state 不變只記 declined_hash（自環）；add 時 append 檔已存在且拒絕 → unmanaged；新版 hash 不同才再問；unmanaged／declined 只在 dry-run／check.sh 提醒、不動檔不紅燈；使用者刪了已納管檔 → deleted、upgrade 維持刪除。"/>
<c id="bS" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,164,1590,1441" v="初始檔五態：每個範本一筆 state；箭頭 = 動詞：條件（自環 = 拒絕但狀態不變，只記 declined_hash）；每格一件事（狀態 → 轉入條件 → upgrade 時 → dry-run／check.sh 印什麼）；remove／uninstall 一律到終點"/>
<c id="bS_v2" parent="bS" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="s0" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="645,36,280,102" v="起點：範本存在於工具 dist/init.toml 的 [[file]]（src／dest／strategy）"/>
<c id="st_d" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="20,268,160,57" v="deleted&lt;br&gt;使用者刪了已納管檔"/>
<c id="st_m" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="330,268,160,57" v="managed&lt;br&gt;已納管（vendor_kit 建的 copy 檔）"/>
<c id="st_c" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="640,268,160,57" v="declined&lt;br&gt;新檔被拒、從未建立"/>
<c id="st_a" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="950,268,160,57" v="appended&lt;br&gt;已插入行（strategy=append）"/>
<c id="st_u" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="1260,268,160,57" v="unmanaged&lt;br&gt;本來就有、沒納管"/>
<c id="in_d" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="120,478,190,57" v="轉入：upgrade 逐檔判斷發現 D 缺（使用者刪了已納管檔）→ state=deleted"/>
<c id="in_m" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="430,470,190,73" v="轉入：add 時 dest 不存在 → 建；upgrade 新版新增檔、問「要建 X 嗎」同意 → 建；declined 再問後同意 → 建"/>
<c id="in_c" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="740,470,190,73" v="轉入：upgrade 新版新增檔、問「要建 X 嗎」後明確答否（EOF／Ctrl-C 不算）→ 從未建立、記 declined_hash"/>
<c id="in_a" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1050,463,190,88" v="轉入：add 時 strategy=append 且檔已存在、問「要在 X 加這幾行嗎」同意 → 插入並記 lines（原本就有的相同行不認領）"/>
<c id="in_u" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1360,455,190,104" v="轉入：add 時 copy 檔已存在 → 不納管、不覆蓋（-y 也不覆蓋），印 6-11；add 時 append 檔已存在、問後拒絕 → 同樣 unmanaged（只記 declined_hash）"/>
<c id="up_d" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="120,712,190,57" v="upgrade 時：維持刪除（不重建、不合併）；baseline 仍推到 N"/>
<c id="up_m" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="430,689,190,104" v="upgrade 時（仍 managed）：D==N／B==N 不動；D==B 問後寫 N；皆異問後三方合併（衝突 → 2）；拒絕 → 只記 declined_hash（自環）；baseline 推到 N"/>
<c id="up_c" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="740,712,190,57" v="upgrade 時：N 的 hash ≠ declined_hash → 再問；相同 → 不問（仍 declined）"/>
<c id="up_a" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1050,689,190,104" v="upgrade 時（仍 appended）：原文比對找 lines：唯一命中 → 問後替換（拒絕 → 只記 declined_hash，自環）；零命中 → 不動只印新內容；多處 → 保留並 warn"/>
<c id="up_u" parent="bS" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1360,720,190,42" v="upgrade 時：永遠不動（不合併、不覆蓋）；仍 unmanaged"/>
<c id="pr_d" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="120,946,190,42" v="dry-run／check.sh 印：維持刪除（不重建）；不紅燈"/>
<c id="pr_m" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="430,923,190,88" v="dry-run／check.sh 印：會問哪些檔（換新版／三方合併）；有 declined_hash 且新版相同 → 6-6；CI 需改 tracked 檔 → 1 印清單"/>
<c id="pr_c" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="740,930,190,73" v="dry-run／check.sh 印：6-6「有 N 個範本你拒絕過」；新版有更新 → 6-8「Y 你拒絕過，vZ 有新版」；不紅燈"/>
<c id="pr_a" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="1050,938,190,57" v="dry-run／check.sh 印：找到 lines → 會問替換；找不到 → 印新內容；多處 → warn"/>
<c id="pr_u" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="1360,938,190,57" v="dry-run／check.sh 印：6-7「X 沒納管，與範本差 N 行」；不紅燈"/>
<c id="end_d" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="20,1141,160,124" v="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失"/>
<c id="end_m" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="330,1141,160,124" v="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失"/>
<c id="end_c" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="640,1141,160,124" v="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失"/>
<c id="end_a" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="950,1141,160,124" v="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失"/>
<c id="end_u" parent="bS" st="ellipse;f=#d5e8d4;s=#000000" g="1260,1141,160,124" v="終點：remove &amp;lt;repo&amp;gt;／uninstall → 這筆 state 隨 metadata 消失"/>
<c id="s_endn" parent="bS" st="shape=note;f=#ffffff;s=#999999" g="20,1395,1530,40" v="終點（任一狀態皆同）：remove &amp;lt;repo&amp;gt;／uninstall → 初始檔保留並印清單（append 行問後只刪原文相同的）；metadata 隨 baseline/&amp;lt;repo&amp;gt;/ 刪除 → 狀態消失；要刪初始檔請自行 git rm"/>
<c id="sl_m_l" parent="bS" st="text;s=none;f=none" g="430,347.0,200,57" v="upgrade：拒絕換版／三方合併 → 只記 declined_hash（仍 managed）"/>
<c id="sl_c_l" parent="bS" st="text;s=none;f=none" g="740,347.0,200,57" v="upgrade：再問後仍拒絕 → 更新 declined_hash（仍 declined）"/>
<c id="sl_a_l" parent="bS" st="text;s=none;f=none" g="1050,347.0,200,57" v="upgrade：拒絕替換 lines → 只記 declined_hash（仍 appended）"/>
<c id="sl_u_l" parent="bS" st="text;s=none;f=none" g="1360,347.0,200,42" v="upgrade：永遠不動（仍 unmanaged）"/>
<c id="se_c" edge source="s0" target="st_c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="805,367;740,367" v="upgrade：拒絕建新檔"/>
<c id="se_m" edge source="s0" target="st_m" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.00,0,," pts="693,367;430,367" v="add：建；upgrade：新增檔同意建"/>
<c id="se_a" edge source="s0" target="st_a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="0.14,0,," pts="847,391;1050,391" v="add：append 檔已存在、同意插入"/>
<c id="se_u" edge source="s0" target="st_u" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.08,0,," pts="917,343;1360,343" v="add：copy 已存在；append 已存在但拒絕"/>
<c id="se_md" edge source="st_m" target="st_d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="upgrade：D 缺"/>
<c id="se_cm" edge source="st_c" target="st_m" st="es=orthogonalEdgeStyle;s=default;fc=default" v="upgrade：再問→同意建"/>
<c id="se_end_d" edge source="st_d" target="end_d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se_end_m" edge source="st_m" target="end_m" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se_end_c" edge source="st_c" target="end_c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se_end_a" edge source="st_a" target="end_a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="se_end_u" edge source="st_u" target="end_u" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="sl_m" edge source="st_m" target="st_m" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="524,472;524,507;478,507"/>
<c id="sl_c" edge source="st_c" target="st_c" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="834,472;834,507;788,507"/>
<c id="sl_a" edge source="st_a" target="st_a" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1144,472;1144,507;1098,507"/>
<c id="sl_u" edge source="st_u" target="st_u" st="es=orthogonalEdgeStyle;s=default;fc=default" pts="1454,472;1454,507;1408,507"/>
<c id="p11_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1621,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p11_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1621,140,64" v="黃：判斷"/>
<c id="p11_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1629,140,44" v="綠：起點／終點"/>
<c id="p11_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1623,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p11_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1623,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p11_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1631,88,40" v="白：步驟"/>
<c id="p11_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1631,170,40" v="虛線框：專案裡的檔案"/>
<c id="p11_lgt" st="text;s=none;f=none" g="1318,1621,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p11_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1689,120,36" v="便條：補充說明"/>
<c id="p11_lgx_state" st="f=#ffffff;s=light-dark(#000000,#9577A3);b=1" g="180,1689,200,36" v="粗框白格：狀態（state 值）"/>
<c id="p11_th" st="text;fs=13;s=none;f=none;b=1" g="40,1727,200,28" v="本頁名詞"/>
<c id="p11_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1761,150,40" v="初始檔／範本"/>
<c id="p11_tv0" st="f=#ffffff;s=#999999" g="190,1761,610,40" v="工具 dist/init.toml 每個 [[file]]（src、dest、strategy = copy｜append）：add 時建到專案（dest）、upgrade 時逐檔判斷；歸使用者、進 git"/>
<c id="p11_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1801,150,55" v="metadata [[file]].state（Q15、16 條）"/>
<c id="p11_tv1" st="f=#ffffff;s=#999999" g="190,1801,610,55" v="baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 對每個範本一筆：state 單一列舉 managed／appended／declined／unmanaged／deleted；declined_hash（選填）= 最近一次被拒絕的那版範本 N 的 sha256；lines（只在 appended）= 實際插入的行原文"/>
<c id="p11_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1856,150,55" v="declined 語意（v2.7-3）"/>
<c id="p11_tv2" st="f=#ffffff;s=#999999" g="190,1856,610,55" v="state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新 → state 不變、只記 declined_hash（畫成自環）；add 時 append 檔已存在且拒絕 → unmanaged（本來就有、沒納管）；二進位拒絕同"/>
<c id="p11_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1911,150,40" v="B／D／N"/>
<c id="p11_tv3" st="f=#ffffff;s=#999999" g="190,1911,610,40" v="B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/&amp;lt;repo&amp;gt;，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突"/>
<c id="p11_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1951,150,55" v="upgrade 逐檔判斷（managed）"/>
<c id="p11_tv4" st="f=#ffffff;s=#999999" g="190,1951,610,55" v="D 缺 → deleted；D==N 或 B==N → 不動；D==B → 問「X 換成新版？」；三者皆異 → 問後 git merge-file --diff3（衝突 → 2）；不論結果 baseline 推到 N（解析失敗除外）；二進位／symlink 未改 → 問後換、改過保留 + warn；拒絕 → 記 declined_hash、state 維持 managed"/>
<c id="p11_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2006,150,55" v="declined 再問規則（Q14／Q15）"/>
<c id="p11_tv5" st="f=#ffffff;s=#999999" g="190,2006,610,55" v="新版 N 的 hash ≠ declined_hash → 再問一次「要建 X 嗎」（同意 → 建 → managed；拒絕 → 仍 declined、更新 declined_hash）；相同 → 不問，只印 6-6／6-8；EOF／Ctrl-C 不算拒絕、不記 declined"/>
<c id="p11_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1761,150,55" v="append 行（Q6／Q12／Q13）"/>
<c id="p11_tv6" st="f=#ffffff;s=#999999" g="990,1761,610,55" v="strategy=append 的檔已存在 → 問「要在 X 加這幾行嗎」；同意 → 插入並記 lines；upgrade 用原文比對（CRLF／LF 等價）找上次插入的行：唯一命中 → 問後替換、零命中 → 不動只印新內容、多處 → 保留並 warn；remove／uninstall 問後只刪原文相同的行"/>
<c id="p11_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1816,150,40" v="dry-run／check.sh 印什麼"/>
<c id="p11_tv7" st="f=#ffffff;s=#999999" g="990,1816,610,40" v="upgrade --dry-run 與 ci/check.sh ③ 印 6-6「有 N 個範本你拒絕過」、6-7「X 沒納管，與範本差 N 行」、6-8「Y 你拒絕過，vZ 有新版」；不動檔、不紅燈（CI 需改 tracked 檔才 1）"/>
<c id="p11_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1856,150,40" v="6-11"/>
<c id="p11_tv8" st="f=#ffffff;s=#999999" g="990,1856,610,40" v="add 遇 copy 檔已存在：「&amp;lt;X&amp;gt; 已存在，未納管；範本在 .vendor_kit/cache/&amp;lt;repo&amp;gt;/files/ 可自行比對」"/>
<c id="p11_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1896,150,40" v="永不刪"/>
<c id="p11_tv9" st="f=#ffffff;s=#999999" g="990,1896,610,40" v="不變量：vendor_kit 對使用者的檔可以建、要改先問、永不刪、永不覆蓋；remove／uninstall 只印初始檔清單（要刪用 git rm）；新版刪除的檔（N 缺）只 warn 不刪"/>
<c id="p11_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1936,150,71" v="結束碼 0／1／2／3"/>
<c id="p11_tv10" st="f=#ffffff;s=#999999" g="990,1936,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="狀態機 v2：交易與進度日誌">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="狀態機 v2：交易與進度日誌（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,116" v="已定（v2.2 C、v2.4-12、v2.5-3、v2.6-9、v2.7-7、v2.8-2、interface_spec §0 進度日誌、§4.3 [progress]、§4.6）：apply 順序 = flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 寫入 → 最後一步刪日誌（uninstall 在根 justfile 那行之後）；中斷 → 1 明列已完成／未完成；下次可寫動詞先恢復（失敗 6-27）、唯讀動詞只提示 6-33 不恢復；prune 特例：活躍日誌只列出不刪、不視為未完成交易；install 例外：第一次 install 不建日誌、失敗整包丟棄，修復型 install 建 .tmp.install.&amp;lt;id&amp;gt;.toml。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,136,240,28" v="使用者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="300,136,480,28" v="引擎容器（apply 段）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="800,136,380,28" v="專案目錄"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1200,136,390,28" v="規則／說明"/>
<c id="bT1" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,180,1590,953" v="交易生命週期（所有可寫動詞的 apply 段；第一次 install 例外：不建日誌、失敗整包丟棄）：拿鎖 → 重驗指紋 → dry-run 分支 → 建日誌 → 逐步寫入（每步 ① 寫暫存 ② 原子替換 ③ 日誌 done）→ 刪日誌；中斷 → 1、日誌留著"/>
<c id="bT1_v2" parent="bT1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="t0" parent="bT1" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="20,36,240,80" v="來自各動詞頁：resolve → 啟動器 docker 之後，apply &amp;lt;verb&amp;gt;"/>
<c id="t1" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,55,480,42" v="拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26；VENDOR_KIT_NO_LOCK=1 跳過）"/>
<c id="t1i" parent="bT1" st="f=#ffffff;s=#b85450;b=1" g="1180,48,390,57" v="不變量：回 3 一律零寫入（無任何例外）；工具層回 1 時 version.toml 不動；日誌在第一個寫入前建、最後一步刪；never fail silently"/>
<c id="t2" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,132,480,42" v="重驗指紋（與 /dist/vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」，零寫入）"/>
<c id="t3y" parent="bT1" st="ellipse;f=#d5e8d4;s=#000000" g="20,190,240,80" v="是 → 0：唯讀預覽（CI 為真且需改 tracked 檔 → 1）；不建日誌"/>
<c id="t3" parent="bT1" st="rhombus;f=#FFF4C3;s=#000000" g="280,205,200,50" v="--dry-run？"/>
<c id="t4" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,368,480,42" v="建進度日誌（第一個寫入前）：state=in-progress、verb、id、started、targets、done[]／pending[]、consents"/>
<c id="t4f" parent="bT1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="780,286,380,206" v="日誌位置（依動詞）"/>
<c id="t4f_0" parent="t4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,352,42" v="add／upgrade：baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml [progress]"/>
<c id="t4f_1" parent="t4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,352,42" v="remove／uninstall／undev／prune：.vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml"/>
<c id="t4f_2" parent="t4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,122,352,42" v="修復型 install：.vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml"/>
<c id="t4f_3" parent="t4f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,170,352,26" v="第一次 install（薄殼不存在）：不建日誌"/>
<c id="t4n" parent="bT1" st="f=#ffe6cc;s=#d79b00;b=1" g="1180,329,390,120" v="已定（v2.8-2）install 例外：第一次 install（薄殼不存在）不建日誌，失敗整包丟棄、不留半成品，下次直接重跑；修復型 install（薄殼已存在）建 .tmp.install.&amp;lt;id&amp;gt;.toml，同其他可寫動詞走恢復。其餘兩種位置：remove／uninstall 會刪 metadata、undev／prune 沒有工具 metadata → 放 .vendor_kit/.tmp.*（自有 .gitignore 擋）；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機"/>
<c id="t5" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,524,480,40" v="逐步寫入 ①：寫暫存檔（合併也在暫存完成；詢問取得的同意先記進 consents）"/>
<c id="t5af" parent="bT1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,524,380,40" v="暫存檔（目標檔旁；未換上前目標檔不動）"/>
<c id="t5n" parent="bT1" st="shape=note;f=#ffffff;s=#999999" g="1180,508,390,73" v="每一步都是 ①②③ 三個可獨立失敗的動作；步驟順序固定：清除衝突狀態 → append／初始檔 → baseline → metadata → cache → gen/tools.just（最後寫、與 cache 同一 apply 內原子替換）→ version.toml 最後"/>
<c id="t5b" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,597,480,40" v="逐步寫入 ②：原子替換（rename 暫存檔 → 目標檔；一檔一次換上）"/>
<c id="t5bf" parent="bT1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,597,380,40" v="目標檔（換上；中斷只會留下「已換上」「未換上」兩種）"/>
<c id="t5c" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,653,480,40" v="逐步寫入 ③：更新日誌 done += 步驟（pending 移出）；還有步驟 → 回 ①"/>
<c id="t5f" parent="bT1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,653,380,40" v="日誌 done[]／pending[] 每步更新"/>
<c id="t6x" parent="bT1" st="ellipse;f=#f8cecc;s=#000000" g="20,709,240,124" v="是 → 1：明列已完成／未完成；日誌留著（state 仍 in-progress）；第一次 install：整包丟棄、無日誌"/>
<c id="t6" parent="bT1" st="rhombus;f=#FFF4C3;s=#000000" g="280,730,300,81" v="中斷？（寫入失敗／Ctrl-C／斷電）"/>
<c id="t7" parent="bT1" st="f=#dae8fc;s=#6c8ebf" g="280,850,480,40" v="否：最後一步刪日誌（uninstall：在根 justfile 那行之後才刪）"/>
<c id="t7f" parent="bT1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,849,380,42" v="日誌刪除 = 交易完成（.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml 刪／[progress] 移除）"/>
<c id="t8" parent="bT1" st="ellipse;f=#d5e8d4;s=#000000" g="20,907,240,40" v="0（或 2 有衝突）：印摘要"/>
<c id="te0" edge source="t0" target="t1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te1" edge source="t1" target="t2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te2" edge source="t2" target="t3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te3" edge source="t3" target="t3y" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te4" edge source="t3" target="t4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te5" edge source="t4" target="t4f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="建"/>
<c id="te6" edge source="t4" target="t5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te7a" edge source="t5" target="t5af" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="te6b" edge source="t5" target="t5b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te7b" edge source="t5b" target="t5bf" st="es=orthogonalEdgeStyle;s=default;fc=default" v="換"/>
<c id="te6c" edge source="t5b" target="t5c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te7" edge source="t5c" target="t5f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="te8" edge source="t5c" target="t6" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="te9" edge source="t6" target="t6x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="te10" edge source="t6" target="t7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="te11" edge source="t7" target="t7f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="te12" edge source="t7" target="t8" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="540,1107"/>
<c id="bT2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,1149,1590,694" v="中斷後的下一次執行（任何動詞開始前先偵測未完成交易）：可寫動詞先恢復再繼續；唯讀動詞只提示重跑原動詞；prune 特例只列出"/>
<c id="bT2_v2" parent="bT2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="r0" parent="bT2" st="ellipse;f=#d5e8d4;s=#000000" g="20,37,240,40" v="打任何 vendor_kit 動詞"/>
<c id="r1" parent="bT2" st="f=#dae8fc;s=#6c8ebf" g="280,36,480,42" v="偵測未完成交易：.vendor_kit/.tmp.&amp;lt;verb&amp;gt;.*.toml（含 .tmp.install.*）或任一 metadata [progress] state=in-progress"/>
<c id="r1f" parent="bT2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,37,380,40" v="讀日誌（verb、id、targets、done／pending、consents）"/>
<c id="r2n" parent="bT2" st="ellipse;f=#d5e8d4;s=#000000" g="20,99,240,40" v="否 → 正常執行本次動詞"/>
<c id="r2" parent="bT2" st="rhombus;f=#FFF4C3;s=#000000" g="370,94,220,50" v="有未完成交易？"/>
<c id="r2px" parent="bT2" st="ellipse;f=#d5e8d4;s=#000000" g="20,176,240,102" v="是 → prune 特例：只列出活躍日誌、印 6-33（不刪、不恢復）→ 繼續 prune（接 prune 頁）"/>
<c id="r2p" parent="bT2" st="rhombus;f=#FFF4C3;s=#000000" g="370,186,220,81" v="本動詞是 prune？"/>
<c id="r2pn" parent="bT2" st="f=#ffe6cc;s=#d79b00;b=1" g="1180,206,390,42" v="已定（v2.7-7）：prune 遇活躍日誌不擋、不恢復、不刪；只列出提示重跑原動詞；差集與 apply prune 照做"/>
<c id="r3x" parent="bT2" st="ellipse;f=#ffe6cc;s=#000000" g="20,326,240,80" v="否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）"/>
<c id="r3" parent="bT2" st="rhombus;f=#FFF4C3;s=#000000" g="280,310,400,112" v="本動詞可寫？（修復型 install／add／remove／upgrade／undev／uninstall）"/>
<c id="r3n" parent="bT2" st="f=#ffe6cc;s=#d79b00;b=1" g="1180,345,390,42" v="已定（v2.6-9）：唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復；help 不受影響"/>
<c id="r4" parent="bT2" st="f=#dae8fc;s=#6c8ebf" g="280,438,480,42" v="是：恢復 = 依日誌把上次交易走完（done 略過；pending 逐步補做；consents 已記的不再問）"/>
<c id="r4f" parent="bT2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,439,380,40" v="補做 pending 的寫入（暫存 → 原子替換）"/>
<c id="r5x" parent="bT2" st="ellipse;f=#f8cecc;s=#000000" g="20,496,240,80" v="否 → 1 + 6-27「未恢復：&amp;lt;檔名&amp;gt;」逐檔列出；日誌留著"/>
<c id="r5" parent="bT2" st="rhombus;f=#FFF4C3;s=#000000" g="280,511,220,50" v="恢復成功？"/>
<c id="r6" parent="bT2" st="f=#dae8fc;s=#6c8ebf" g="280,592,480,40" v="是：刪日誌 → 繼續本次動詞（resolve 會重算指紋）"/>
<c id="r6f" parent="bT2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="780,592,380,40" v="日誌刪除"/>
<c id="r7" parent="bT2" st="ellipse;f=#d5e8d4;s=#000000" g="20,648,240,40" v="→ 繼續本次動詞"/>
<c id="re0" edge source="r0" target="r1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="re1" edge source="r1" target="r1f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="讀"/>
<c id="re2" edge source="r1" target="r2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="re3" edge source="r2" target="r2n" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="re4" edge source="r2" target="r2p" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="re4p" edge source="r2p" target="r2px" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="re4n" edge source="r2p" target="r3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="re5" edge source="r3" target="r3x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="re6" edge source="r3" target="r4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="re7" edge source="r4" target="r4f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="re8" edge source="r4" target="r5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="re9" edge source="r5" target="r5x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="re10" edge source="r5" target="r6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="re11" edge source="r6" target="r6f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="刪"/>
<c id="re12" edge source="r6" target="r7" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="540,1817"/>
<c id="p12_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1859,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p12_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1859,140,64" v="黃：判斷"/>
<c id="p12_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1867,140,44" v="綠：起點／終點"/>
<c id="p12_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1861,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p12_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1861,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p12_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1869,88,40" v="白：步驟"/>
<c id="p12_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1869,170,40" v="虛線框：專案裡的檔案"/>
<c id="p12_lgt" st="text;s=none;f=none" g="1318,1859,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p12_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1927,120,36" v="便條：補充說明"/>
<c id="p12_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1927,150,36" v="橘框：規則（已定）"/>
<c id="p12_lgx_inv" st="f=#ffffff;s=#b85450;b=1" g="350,1927,130,36" v="紅粗框：不變量"/>
<c id="p12_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="500,1927,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p12_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="710,1927,170,36" v="灰底：泳道／表格表頭"/>
<c id="p12_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="900,1927,200,36" v="虛線橢圓：來自其他頁"/>
<c id="p12_th" st="text;fs=13;s=none;f=none;b=1" g="40,1965,200,28" v="本頁名詞"/>
<c id="p12_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1999,150,40" v="交易／apply"/>
<c id="p12_tv0" st="f=#ffffff;s=#999999" g="190,1999,610,40" v="一次會寫檔的動詞執行 = 一筆交易：apply 拿 flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 逐步寫入 → 最後一步刪日誌；回 3 一律零寫入；工具層回 1 時 version.toml 不動"/>
<c id="p12_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2039,150,40" v="進度日誌"/>
<c id="p12_tv1" st="f=#ffffff;s=#999999" g="190,2039,610,40" v="記錄交易進度的 TOML：state=&quot;in-progress&quot;、verb、id、started（UTC ISO 8601）、targets、done／pending（步驟清單）、consents（已取得的同意）；存在 = 上次沒走完"/>
<c id="p12_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2079,150,55" v="兩種位置"/>
<c id="p12_tv2" st="f=#ffffff;s=#999999" g="190,2079,610,55" v="add／upgrade 記在 metadata baseline/&amp;lt;repo&amp;gt;/.vendor_kit.toml 的 [progress]；remove／uninstall／undev／prune／修復型 install 放 .vendor_kit/.tmp.&amp;lt;verb&amp;gt;.&amp;lt;id&amp;gt;.toml（因為 metadata 會被刪或不存在）；&amp;lt;id&amp;gt; = UTC 時間戳 + 隨機（不用 &amp;lt;repo&amp;gt;，uninstall 多工具才不撞）"/>
<c id="p12_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2134,150,55" v="install 的日誌（v2.8-2）"/>
<c id="p12_tv3" st="f=#ffffff;s=#999999" g="190,2134,610,55" v="第一次 install（薄殼不存在）不建日誌：失敗整包丟棄、不留半成品（bootstrap.sh 的 1 失敗不留半成品只對它成立），下次直接重跑；修復型 install（薄殼已存在、冪等修復）建 .vendor_kit/.tmp.install.&amp;lt;id&amp;gt;.toml，與其他可寫動詞一樣走恢復"/>
<c id="p12_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2189,150,55" v="恢復"/>
<c id="p12_tv4" st="f=#ffffff;s=#999999" g="190,2189,610,55" v="可寫動詞（修復型 install／add／remove／upgrade／undev／uninstall）開始前偵測到未完成交易 → 先依日誌把交易走完（done 略過、pending 補做、consents 不再問）再繼續本次；失敗 → 1 印 6-27「未恢復：&amp;lt;檔名&amp;gt;」逐檔列出、日誌留著；第一次 install 沒有日誌可恢復（整包丟棄後重跑）"/>
<c id="p12_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2244,150,40" v="唯讀動詞不恢復"/>
<c id="p12_tv5" st="f=#ffffff;s=#999999" g="190,2244,610,40" v="sync／update 偵測到未完成交易只印 6-33「偵測到未完成的 &amp;lt;verb&amp;gt;（&amp;lt;id&amp;gt;）。請先重跑：just vendor_kit &amp;lt;verb&amp;gt; &amp;lt;targets&amp;gt;」→ 1，不寫任何檔；help 不受影響"/>
<c id="p12_tk6" st="f=#ffffff;s=#999999;b=1" g="40,2284,150,55" v="prune 特例（v2.7-7）"/>
<c id="p12_tv6" st="f=#ffffff;s=#999999" g="190,2284,610,55" v="prune 遇活躍（未恢復）日誌：只列出並印 6-33、不刪、不視為未完成交易（不擋 prune、不恢復）；prune 自己的 apply 也建 .tmp.prune.&amp;lt;id&amp;gt;.toml（清理前建、清理後刪；v2.9-6），與其他可寫動詞一樣走恢復"/>
<c id="p12_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1999,150,40" v="原子替換／暫存"/>
<c id="p12_tv7" st="f=#ffffff;s=#999999" g="990,1999,610,40" v="每個寫入先寫到暫存（合併也在暫存完成），確認沒問題再逐檔一次換上（rename）；gen/tools.just 最後寫、與 cache 同一 apply 內原子替換；中斷只會留下「已換上」與「未換上」兩種檔，不留半寫的檔"/>
<c id="p12_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2039,150,40" v=".tmp.dist.&amp;lt;id&amp;gt;/"/>
<c id="p12_tv8" st="f=#ffffff;s=#999999" g="990,2039,610,40" v="啟動器暫存（展開的工具 dist、vk-resolve）；不是交易日誌；啟動器 trap … EXIT INT TERM 清容器與此目錄；殘留由 prune 清"/>
<c id="p12_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2079,150,40" v="dry-run"/>
<c id="p12_tv9" st="f=#ffffff;s=#999999" g="990,2079,610,40" v="apply --dry-run：唯讀預覽（本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單）；不建日誌、不寫檔；也要先拉 image 展開才知道會問哪些檔"/>
<c id="p12_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2119,150,55" v="指紋／flock"/>
<c id="p12_tv10" st="f=#ffffff;s=#999999" g="990,2119,610,55" v="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎"/>
<c id="p12_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2174,150,55" v="6-N 訊息編號"/>
<c id="p12_tv11" st="f=#ffffff;s=#999999" g="990,2174,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p12_tk12" st="f=#ffffff;s=#999999;b=1" g="840,2229,150,71" v="結束碼 0／1／2／3"/>
<c id="p12_tv12" st="f=#ffffff;s=#999999" g="990,2229,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="相容性矩陣 v2">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="相容性矩陣 v2：舊薄殼 × 新引擎、舊引擎 × 新檔 → 0／1／3（interface_spec §2、§8；Q16／Q19／Q23）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定（Q16、Q19、Q23、v2.4-3／-6／-7、v2.6 16 條、v2.7-4、interface_spec §2、§4 通則、§8）：相容承諾兩層（永久：救援路徑 + 舊資料可讀可遷；非永久：舊薄殼跑新 major 一般動詞回 3）；floor = 固定 release 常數；新舊以 P／schema 比較不用版本字串；回 3 零寫入、無任何例外（救援路徑亦同）；written_by 純資訊欄、無 min_reader；同 schema 未知欄位讀忽略寫保留。"/>
<c id="l13a" st="text;s=none;f=none;b=1" g="40,120,900,24" v="(a) 舊薄殼 P × 新引擎（接受 [floor_P, current_P]）：一般動詞／救援路徑各回什麼"/>
<c id="ta_h0" st="f=#e6e6e6;s=#999999;b=1" g="40,150,330,30" v="薄殼 P 的情況"/>
<c id="ta_h1" st="f=#e6e6e6;s=#999999;b=1" g="370,150,640,30" v="一般動詞（add／remove／upgrade &amp;lt;repo&amp;gt;／sync 寫入／undev／uninstall／prune／dev／update）"/>
<c id="ta_h2" st="f=#e6e6e6;s=#999999;b=1" g="1010,150,590,30" v="救援路徑（install／upgrade vendor_kit／sync 不符提示／help；單段）"/>
<c id="ta_r0c0" st="s=#999999;f=#ffffff;b=1" g="40,180,330,30" v="P &amp;lt; floor_P（太舊）"/>
<c id="ta_r0c1" st="s=#999999;f=#ffe6cc" g="370,180,640,30" v="3 + 6-18「請以 bootstrap.sh 重建」；零寫入；floor 檢查先於任何上網（斷網也回 3）"/>
<c id="ta_r0c2" st="s=#999999;f=#ffe6cc" g="1010,180,590,30" v="3 + 6-18（救援路徑也不接、同樣零寫入；唯一可用 synthetic fixture 驗收）"/>
<c id="ta_r1c0" st="s=#999999;f=#ffffff;b=1" g="40,210,330,42" v="floor_P ≤ P &amp;lt; 引擎需求（舊薄殼 × 新 major）"/>
<c id="ta_r1c1" st="s=#999999;f=#ffe6cc" g="370,210,640,42" v="3 + 6-36「薄殼協定 &amp;lt;P_shell&amp;gt; 低於引擎 &amp;lt;vY&amp;gt; 的一般動詞需求，請先 upgrade vendor_kit」；零寫入"/>
<c id="ta_r1c2" st="s=#999999;f=#d5e8d4" g="1010,210,590,42" v="0／1 正常（永久保證）：install／upgrade vendor_kit 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」；sync 不符 → 1 + 6-1；help → 0"/>
<c id="ta_r2c0" st="s=#999999;f=#ffffff;b=1" g="40,252,330,42" v="同 major（P 在引擎支援範圍內）"/>
<c id="ta_r2c1" st="s=#999999;f=#d5e8d4" g="370,252,640,42" v="0／1／2 正常：引擎以呼叫方 P 輸出 vk-resolve/P 與結束碼語意；不輸出呼叫方不認識的 kind、不要求其未提供的 mount／環境變數"/>
<c id="ta_r2c2" st="s=#999999;f=#d5e8d4" g="1010,252,590,42" v="0／1 正常；upgrade vendor_kit 無新版且薄殼相符 → 0 無變更"/>
<c id="ta_r3c0" st="s=#999999;f=#ffffff;b=1" g="40,294,330,73" v="P &amp;gt; current_P（新薄殼 × 舊引擎：降版／dev -i 舊 image）"/>
<c id="ta_r3c1" st="s=#999999;f=#ffe6cc" g="370,294,640,73" v="3：P 不在引擎的 [floor_P, current_P]；零寫入"/>
<c id="ta_r3c2" st="s=#999999;f=#ffe6cc" g="1010,294,590,73" v="降版 upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎能無損讀現有檔（同 P／schema）→ 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前 3 + 6-10「請 git revert」（零寫入）；dev vendor_kit -i 舊 image 禁止重產 tracked 薄殼 → 3"/>
<c id="l13b" st="text;s=none;f=none;b=1" g="40,391,900,24" v="(b) 舊引擎 × 檔案 schema（每檔各自 schema = N；讀取門檻只看 schema）"/>
<c id="tb_h0" st="f=#e6e6e6;s=#999999;b=1" g="40,421,300,30" v="檔 vs 引擎"/>
<c id="tb_h1" st="f=#e6e6e6;s=#999999;b=1" g="340,421,420,30" v="讀"/>
<c id="tb_h2" st="f=#e6e6e6;s=#999999;b=1" g="760,421,560,30" v="寫"/>
<c id="tb_h3" st="f=#e6e6e6;s=#999999;b=1" g="1320,421,280,30" v="結束碼"/>
<c id="tb_r0c0" st="s=#999999;f=#ffffff;b=1" g="40,451,300,30" v="同 schema、有未知欄位"/>
<c id="tb_r0c1" st="s=#999999;f=#ffffff" g="340,451,420,30" v="讀時忽略未知欄位"/>
<c id="tb_r0c2" st="s=#999999;f=#ffffff" g="760,451,560,30" v="寫時保留未知欄位（不能保留 → 拒絕寫）；只拒絕型別錯／重複宣告"/>
<c id="tb_r0c3" st="s=#999999;f=#d5e8d4" g="1320,451,280,30" v="0（型別錯／重複宣告 → 1）"/>
<c id="tb_r1c0" st="s=#999999;f=#ffffff;b=1" g="40,481,300,42" v="檔 schema &amp;lt; 引擎（舊檔）"/>
<c id="tb_r1c1" st="s=#999999;f=#ffffff" g="340,481,420,42" v="可讀：記憶體轉換（讀任一舊 schema → 當前 schema，不鏈式）"/>
<c id="tb_r1c2" st="s=#999999;f=#ffffff" g="760,481,560,42" v="只在本來要寫該檔的明確動作才寫回當前 schema；metadata 遷移由 upgrade vendor_kit 做、dry-run 明列；同一專案短暫混合 schema 合法"/>
<c id="tb_r1c3" st="s=#999999;f=#d5e8d4" g="1320,481,280,42" v="0"/>
<c id="tb_r2c0" st="s=#999999;f=#ffffff;b=1" g="40,523,300,42" v="檔 schema &amp;gt; 引擎支援上限（新檔）"/>
<c id="tb_r2c1" st="s=#999999;f=#ffffff" g="340,523,420,42" v="拒絕讀：3 + 6-19「schema &amp;lt;N&amp;gt; 高於本引擎支援的 &amp;lt;M&amp;gt;；寫入者為 vendor_kit &amp;lt;written_by&amp;gt;」"/>
<c id="tb_r2c2" st="s=#999999;f=#ffffff" g="760,523,560,42" v="任何寫入前退出（零寫入）；dev vendor_kit -i 舊 image 亦同"/>
<c id="tb_r2c3" st="s=#999999;f=#ffe6cc" g="1320,523,280,42" v="3"/>
<c id="tb_r3c0" st="s=#999999;f=#ffffff;b=1" g="40,565,300,42" v="降版目標引擎（upgrade vendor_kit@&amp;lt;舊版&amp;gt;）"/>
<c id="tb_r3c1" st="s=#999999;f=#ffffff" g="340,565,420,42" v="以目標 image LABEL 的 P／schema 判：能無損讀現有檔 → 讀"/>
<c id="tb_r3c2" st="s=#999999;f=#ffffff" g="760,565,560,42" v="無損 → 重產薄殼 → 1 + 6-2（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前拒絕 3 + 6-10「請 git revert」"/>
<c id="tb_r3c3" st="s=#999999;f=#ffe6cc" g="1320,565,280,42" v="1（無損 → 重產薄殼）／3（否則）"/>
<c id="k13a" st="f=#ffe6cc;s=#d79b00;b=1" g="40,631,500,57" v="floor 常數（已定）：第一個正式版 v1.0.0、P=1、schema=1；寫在契約，只能經 ADR + major 提高；引擎 image LABEL ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt; 讓啟動器不起容器即可判 floor；低於 floor → 3 + 6-18 零寫入"/>
<c id="k13b" st="f=#ffe6cc;s=#d79b00;b=1" g="560,631,520,73" v="--protocol 協商（已定，Q16）：薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎接受 [floor_P, current_P]，以呼叫方 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1；引擎宣稱的 P 真不支援 → 3"/>
<c id="k13c" st="f=#ffe6cc;s=#d79b00;b=1" g="1100,631,490,73" v="Q16 兩層承諾（已定）：永久 —— 任何 ≥ floor 的舊薄殼可叫新引擎的救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/）並得正確提示；舊資料永遠可讀可遷。非永久 —— 舊薄殼跑新 major 一般動詞只保證乾淨回 3 + 6-36（零寫入）；同 major 內保留已承諾薄殼的一般呼叫"/>
<c id="k13d" st="shape=note;f=#ffffff;s=#999999" g="40,720,500,57" v="written_by：每個 vendor_kit 寫的 TOML 都有 written_by = &quot;&amp;lt;vX&amp;gt;&quot;（寫入引擎版本），純資訊欄、不作讀取門檻（無 min_reader）；6-19 印出它供人判斷該用哪個引擎"/>
<c id="k13e" st="shape=note;f=#ffffff;s=#999999" g="560,720,520,57" v="新舊怎麼比：一律以 P／schema 比較，不用 SemVer 版本字串；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1 的情境（印記不符、薄殼被改 6-28、自身升級完成要重跑 6-2）維持 1，不因訊息含 upgrade 而改 3；回 3 零寫入無任何例外（v2.7-4）"/>
<c id="k13f" st="shape=note;f=#ffffff;s=#999999" g="1100,720,490,73" v="驗收（§7.4-1～8）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 驅動候選 C（線性）；連升 r_i → r_j → C；floor 直接跳升；降版同 P／schema 成功（重產薄殼 → 1）、跨 schema 3；&amp;lt; floor 唯一 synthetic；舊引擎讀新檔 3 零寫入；舊 bootstrap.sh 再跑不降版；已釋出 image／資產／fixture 永不刪"/>
<c id="p13_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,823,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p13_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,823,140,64" v="黃：判斷"/>
<c id="p13_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,831,140,44" v="綠：起點／終點"/>
<c id="p13_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,825,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p13_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,825,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p13_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,833,88,40" v="白：步驟"/>
<c id="p13_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,833,170,40" v="虛線框：專案裡的檔案"/>
<c id="p13_lgt" st="text;s=none;f=none" g="1318,823,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p13_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,891,120,36" v="便條：補充說明"/>
<c id="p13_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,891,150,36" v="橘框：規則（已定）"/>
<c id="p13_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="350,891,170,36" v="灰底：泳道／表格表頭"/>
<c id="p13_lgx_c0" st="s=#999999;f=#d5e8d4" g="540,891,110,36" v="綠格：結束碼 0"/>
<c id="p13_lgx_cx" st="s=#999999;f=#ffe6cc" g="670,891,190,36" v="橙格：需要人動作（1／2／3）"/>
<c id="p13_lgx_cell" st="s=#999999;f=#ffffff" g="880,891,110,36" v="白格：表格內容"/>
<c id="p13_th" st="text;fs=13;s=none;f=none;b=1" g="40,929,200,28" v="本頁名詞"/>
<c id="p13_tk0" st="f=#ffffff;s=#999999;b=1" g="40,963,150,55" v="薄殼 P／引擎 [floor_P, current_P]"/>
<c id="p13_tv0" st="f=#ffffff;s=#999999" g="190,963,610,55" v="薄殼 = 進 git 的 .vendor_kit/ 四檔（entry.just、vendor.just、.gitignore、ci/check.sh），首行自描述帶協定號 P；引擎 image 接受 [floor_P, current_P]（LABEL ….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;，啟動器不起容器即可判 floor）"/>
<c id="p13_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1018,150,55" v="--protocol P"/>
<c id="p13_tv1" st="f=#ffffff;s=#999999" g="190,1018,610,55" v="薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎以呼叫方的 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1"/>
<c id="p13_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1073,150,40" v="floor"/>
<c id="p13_tv2" st="f=#ffffff;s=#999999" g="190,1073,610,40" v="固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1）；只能經 ADR + major 提高；低於 floor → 3 + 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）"/>
<c id="p13_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1113,150,55" v="救援路徑（永久）"/>
<c id="p13_tv3" st="f=#ffffff;s=#999999" g="190,1113,610,55" v="install、upgrade vendor_kit[@&amp;lt;tag&amp;gt;]、sync 的「薄殼不符 → 1 + 6-1」判定、help：單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼都能經此叫任何引擎重產薄殼（反向降版亦然，受 3 (c)(d) 限制）；救援路徑回 3 時同樣零寫入"/>
<c id="p13_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1168,150,55" v="一般動詞（非永久）"/>
<c id="p13_tv4" st="f=#ffffff;s=#999999" g="190,1168,610,55" v="add／remove／upgrade &amp;lt;repo&amp;gt;／sync 寫入／undev／uninstall／prune／dev／update：舊薄殼跑新 major 只保證乾淨回 3 + 6-36 提示先 upgrade vendor_kit（零寫入）；同 major 內保留所有已承諾薄殼的一般呼叫"/>
<c id="p13_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1223,150,55" v="schema N"/>
<c id="p13_tv5" st="f=#ffffff;s=#999999" g="190,1223,610,55" v="每個 vendor_kit 寫的 TOML（version.toml、version.local.toml、metadata、.tmp.*）有 schema = N（integer）：讀取門檻只看它；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯／重複宣告 → 1；讀任一舊 schema → 直接寫當前 schema（不鏈式）"/>
<c id="p13_tk6" st="f=#ffffff;s=#999999;b=1" g="840,963,150,40" v="written_by"/>
<c id="p13_tv6" st="f=#ffffff;s=#999999" g="990,963,610,40" v="寫入引擎版本（string），純資訊欄、不作讀取門檻（無 min_reader）；6-19 訊息印出它供人判斷該用哪個引擎"/>
<c id="p13_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1003,150,55" v="6-18／6-19／6-36／6-10"/>
<c id="p13_tv7" st="f=#ffffff;s=#999999" g="990,1003,610,55" v="6-18 薄殼／引擎低於 floor「請以 bootstrap.sh 重建」；6-19 schema N 高於本引擎支援的 M；6-36 薄殼協定低於引擎一般動詞需求「請先 upgrade vendor_kit」；6-10 降版目標引擎無法無損讀「請 git revert」；四者皆 3、零寫入"/>
<c id="p13_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1058,150,55" v="降版"/>
<c id="p13_tv8" st="f=#ffffff;s=#999999" g="990,1058,610,55" v="upgrade vendor_kit@&amp;lt;舊版&amp;gt;：目標引擎（以其 image LABEL 的 P／schema 判）能無損讀現有檔才做（做 = 重產薄殼 → 1 + 6-2），否則改檔前拒絕 3 + 6-10；dev vendor_kit -i &amp;lt;舊 image&amp;gt; 允許但禁止重產 tracked 薄殼"/>
<c id="p13_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1113,150,55" v="驗收（§7.4）"/>
<c id="p13_tv9" st="f=#ffffff;s=#999999" g="990,1113,610,55" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture 驅動候選（線性，非兩兩相乘）；連升 r_i → r_j → C；floor 直接跳升；降版；&amp;lt; floor 用唯一 synthetic；舊引擎讀新檔 3 零寫入；已釋出 image／Release 資產／fixture 永不刪"/>
<c id="p13_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1168,150,71" v="結束碼 0／1／2／3"/>
<c id="p13_tv10" st="f=#ffffff;s=#999999" g="990,1168,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="結束碼決策表 v2">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="結束碼決策表 v2：動詞 × 情況 → 0／1／2／3（interface_spec §1.2、§2、§7.1；Q23／Q27）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1080,12,520,92" v="已定（Q23、Q27、v2.6-15、v2.7-4／-8、interface_spec §1.2 每動詞結束碼欄、§2 結束碼總表、§7.1）：3 = 版本／協定／schema 不合且零寫入（無任何例外；P &amp;lt; floor 時任何動詞含 help 都回 3 + 6-18，v2.9-7）；既定回 1 的情境維持 1；多工具做得完的做完再回最需要處理的碼；CI 動作：0 過、1 修、2 解衝突、3 換版本；顏色：0 綠、需要人動作 1／2／3 橙（含 update 無憑證 6-3）、失敗 1 紅。"/>
<c id="te_h0" st="f=#e6e6e6;s=#999999;b=1" g="40,120,170,30" v="動詞"/>
<c id="te_h1" st="f=#e6e6e6;s=#999999;b=1" g="210,120,250,30" v="0 成功（綠）"/>
<c id="te_h2" st="f=#e6e6e6;s=#999999;b=1" g="460,120,420,30" v="1 需要人動作（橙：印指令）"/>
<c id="te_h3" st="f=#e6e6e6;s=#999999;b=1" g="880,120,260,30" v="1 失敗（紅）"/>
<c id="te_h4" st="f=#e6e6e6;s=#999999;b=1" g="1140,120,240,30" v="2 衝突／有新版（橙）"/>
<c id="te_h5" st="f=#e6e6e6;s=#999999;b=1" g="1380,120,210,30" v="3 版本不合（橙；零寫入）"/>
<c id="te_r0c0" st="s=#999999;f=#ffffff;b=1" g="40,150,170,42" v="bootstrap.sh"/>
<c id="te_r0c1" st="s=#999999;f=#d5e8d4" g="210,150,250,42" v="install 與每個 -t 的 add 都完成"/>
<c id="te_r0c2" st="s=#999999;f=#ffe6cc" g="460,150,420,42" v="非 git repo（6-16）；just &amp;lt; 1.33.0（6-23）；需問但無 tty（6-4）；任一 add 失敗（明列已完成／未完成）"/>
<c id="te_r0c3" st="s=#999999;f=#f8cecc" g="880,150,260,42" v="pull 失敗／逾時（6-24／6-31）；install 失敗（第一次不留半成品）"/>
<c id="te_r0c4" st="s=#999999;f=#ffffff" g="1140,150,240,42" v="—"/>
<c id="te_r0c5" st="s=#999999;f=#ffe6cc" g="1380,150,210,42" v="薄殼／引擎 &amp;lt; floor（6-18）"/>
<c id="te_r1c0" st="s=#999999;f=#ffffff;b=1" g="40,192,170,57" v="install"/>
<c id="te_r1c1" st="s=#999999;f=#d5e8d4" g="210,192,250,57" v="建立或修復完成；已含 import 行不再加；--no-justfile 只印指示；問後拒絕加行 → 不動、印指示"/>
<c id="te_r1c2" st="s=#999999;f=#ffe6cc" g="460,192,420,57" v="非 git（6-16）；巢狀（6-35）；install &amp;lt;repo&amp;gt; 誤用（6-17）；薄殼被改（6-28，列差異不動）；無 tty 需問（6-4）"/>
<c id="te_r1c3" st="s=#999999;f=#f8cecc" g="880,192,260,57" v="寫入失敗（第一次不留半成品）"/>
<c id="te_r1c4" st="s=#999999;f=#ffffff" g="1140,192,240,57" v="—"/>
<c id="te_r1c5" st="s=#999999;f=#ffe6cc" g="1380,192,210,57" v="P &amp;lt; floor（6-18）；檔 schema 高於支援（6-19）"/>
<c id="te_r2c0" st="s=#999999;f=#ffffff;b=1" g="40,249,170,42" v="uninstall"/>
<c id="te_r2c1" st="s=#999999;f=#d5e8d4" g="210,249,250,42" v="完成（初始檔保留印清單；未知或被改的檔保留並回報）；dry-run 本機"/>
<c id="te_r2c2" st="s=#999999;f=#ffe6cc" g="460,249,420,42" v="任一工具在 dev 覆寫中（先 undev）；CI 需改 tracked 檔；指紋不同（6-12）"/>
<c id="te_r2c3" st="s=#999999;f=#f8cecc" g="880,249,260,42" v="任一工具 remove 失敗 → 中止、列已完成部分"/>
<c id="te_r2c4" st="s=#999999;f=#ffffff" g="1140,249,240,42" v="—"/>
<c id="te_r2c5" st="s=#999999;f=#ffe6cc" g="1380,249,210,42" v="6-18／6-19"/>
<c id="te_r3c0" st="s=#999999;f=#ffffff;b=1" g="40,291,170,57" v="add &amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]"/>
<c id="te_r3c1" st="s=#999999;f=#d5e8d4" g="210,291,250,57" v="接入完成；已接入且完成 → 無變更；dry-run 本機"/>
<c id="te_r3c2" st="s=#999999;f=#ffe6cc" g="460,291,420,57" v="@&amp;lt;tag&amp;gt; 與鎖定不同（改用 upgrade）；私有且無憑證又未指定 @&amp;lt;tag&amp;gt;（6-3）；dest 不合法／撞名；&amp;lt;ns&amp;gt; 撞名；CI 需改 tracked；指紋不同（6-12）；未完成交易恢復失敗（6-27）"/>
<c id="te_r3c3" st="s=#999999;f=#f8cecc" g="880,291,260,57" v="pull 失敗／逾時；dist 含 symlink；寫入失敗（version.toml 一律未動）"/>
<c id="te_r3c4" st="s=#999999;f=#ffffff" g="1140,291,240,57" v="—"/>
<c id="te_r3c5" st="s=#999999;f=#ffe6cc" g="1380,291,210,57" v="6-18／6-19"/>
<c id="te_r4c0" st="s=#999999;f=#ffffff;b=1" g="40,348,170,42" v="remove &amp;lt;repo&amp;gt;"/>
<c id="te_r4c1" st="s=#999999;f=#d5e8d4" g="210,348,250,42" v="完成（初始檔永不刪、印清單）；未接 → 提示"/>
<c id="te_r4c2" st="s=#999999;f=#ffe6cc" g="460,348,420,42" v="dev 覆寫中（先 undev）；CI 需改 tracked；指紋不同"/>
<c id="te_r4c3" st="s=#999999;f=#f8cecc" g="880,348,260,42" v="寫入失敗（可恢復狀態）"/>
<c id="te_r4c4" st="s=#999999;f=#ffffff" g="1140,348,240,42" v="—"/>
<c id="te_r4c5" st="s=#999999;f=#ffe6cc" g="1380,348,210,42" v="6-18／6-19"/>
<c id="te_r5c0" st="s=#999999;f=#ffffff;b=1" g="40,390,170,42" v="update [&amp;lt;repo&amp;gt;]"/>
<c id="te_r5c1" st="s=#999999;f=#d5e8d4" g="210,390,250,42" v="已列出（有新版也 0；末行 6-15）"/>
<c id="te_r5c2" st="s=#999999;f=#ffe6cc" g="460,390,420,42" v="未完成交易（6-33）；任一目標查詢失敗（含無憑證 6-3：設 token 或 upgrade &amp;lt;repo&amp;gt;@&amp;lt;tag&amp;gt;；即使另有新版）"/>
<c id="te_r5c3" st="s=#999999;f=#ffffff" g="880,390,260,42" v="—"/>
<c id="te_r5c4" st="s=#999999;f=#ffe6cc" g="1140,390,240,42" v="--exit-code 且有新版"/>
<c id="te_r5c5" st="s=#999999;f=#ffe6cc" g="1380,390,210,42" v="6-18／6-19"/>
<c id="te_r6c0" st="s=#999999;f=#ffffff;b=1" g="40,432,170,73" v="upgrade [&amp;lt;repo&amp;gt;[@&amp;lt;tag&amp;gt;]]"/>
<c id="te_r6c1" st="s=#999999;f=#d5e8d4" g="210,432,250,73" v="完成；無新版；(1) 補齊待合併後停（6-14）；dry-run 本機"/>
<c id="te_r6c2" st="s=#999999;f=#ffe6cc" g="460,432,420,73" v="無 baseline（先 add）；dev 覆寫中（先 undev）；CI 需改 tracked（6-5）；指紋不同；自身升級後「請 commit 並再跑原指令」（6-2；已改第一行是明列例外）；6-2b"/>
<c id="te_r6c3" st="s=#999999;f=#f8cecc" g="880,432,260,73" v="pull 失敗；git merge-file I/O 錯誤；寫入失敗（工具層 version.toml 不動）"/>
<c id="te_r6c4" st="s=#999999;f=#ffe6cc" g="1140,432,240,73" v="合併衝突（留標記、baseline 仍推）；合併結果 TOML／just 解析失敗（留原檔、baseline 不推）；(0) 仍有衝突標記"/>
<c id="te_r6c5" st="s=#999999;f=#ffe6cc" g="1380,432,210,73" v="@&amp;lt;舊版&amp;gt; 無法無損讀（6-10）；6-18／6-19"/>
<c id="te_r7c0" st="s=#999999;f=#ffffff;b=1" g="40,505,170,57" v="dev &amp;lt;repo&amp;gt;／vendor_kit"/>
<c id="te_r7c1" st="s=#999999;f=#d5e8d4" g="210,505,250,57" v="覆寫寫入 version.local.toml"/>
<c id="te_r7c2" st="s=#999999;f=#ffe6cc" g="460,505,420,57" v="工具不在 version.toml；缺 &amp;lt;dir&amp;gt;/dist/init.toml；CI 拒絕；-p／-i 互斥用錯"/>
<c id="te_r7c3" st="s=#999999;f=#ffffff" g="880,505,260,57" v="—"/>
<c id="te_r7c4" st="s=#999999;f=#ffffff" g="1140,505,240,57" v="—"/>
<c id="te_r7c5" st="s=#999999;f=#ffe6cc" g="1380,505,210,57" v="6-18／6-19；-i 舊引擎 P／schema 低於薄殼首行且要重產 tracked 薄殼 → 拒絕"/>
<c id="te_r8c0" st="s=#999999;f=#ffffff;b=1" g="40,562,170,42" v="undev &amp;lt;repo&amp;gt;／vendor_kit"/>
<c id="te_r8c1" st="s=#999999;f=#d5e8d4" g="210,562,250,42" v="完成；未啟用 → 提示"/>
<c id="te_r8c2" st="s=#999999;f=#ffe6cc" g="460,562,420,42" v="指紋不同"/>
<c id="te_r8c3" st="s=#999999;f=#f8cecc" g="880,562,260,42" v="重新 materialize 失敗（保留可恢復狀態）"/>
<c id="te_r8c4" st="s=#999999;f=#ffffff" g="1140,562,240,42" v="—"/>
<c id="te_r8c5" st="s=#999999;f=#ffe6cc" g="1380,562,210,42" v="6-18／6-19"/>
<c id="te_r9c0" st="s=#999999;f=#ffffff;b=1" g="40,604,170,42" v="sync [&amp;lt;repo&amp;gt;] [--verify]"/>
<c id="te_r9c1" st="s=#999999;f=#d5e8d4" g="210,604,250,42" v="快路徑（不起容器）；materialize／verify 完成"/>
<c id="te_r9c2" st="s=#999999;f=#ffe6cc" g="460,604,420,42" v="薄殼不符（6-1，不重寫）；未完成接入（6-13）；CI 下 baseline 落後（6-5）；CI 下任何 local 覆寫；未完成交易（6-33）"/>
<c id="te_r9c3" st="s=#999999;f=#f8cecc" g="880,604,260,42" v="pull 失敗／逾時；verify 失敗且重裝失敗"/>
<c id="te_r9c4" st="s=#999999;f=#ffffff" g="1140,604,240,42" v="—"/>
<c id="te_r9c5" st="s=#999999;f=#ffe6cc" g="1380,604,210,42" v="6-18／6-19"/>
<c id="te_r10c0" st="s=#999999;f=#ffffff;b=1" g="40,646,170,42" v="prune"/>
<c id="te_r10c1" st="s=#999999;f=#d5e8d4" g="210,646,250,42" v="完成（印刪了什麼、保留什麼；活躍 .tmp.* 只列出）；dry-run 零刪除"/>
<c id="te_r10c2" st="s=#999999;f=#ffe6cc" g="460,646,420,42" v="vk-resolve 不合（6-30）；無 tty 需問（6-4）"/>
<c id="te_r10c3" st="s=#999999;f=#f8cecc" g="880,646,260,42" v="任一 docker rm／image rm／network rm／volume rm 失敗（摘要全列）"/>
<c id="te_r10c4" st="s=#999999;f=#ffffff" g="1140,646,240,42" v="—"/>
<c id="te_r10c5" st="s=#999999;f=#ffe6cc" g="1380,646,210,42" v="6-18／6-19"/>
<c id="te_r11c0" st="s=#999999;f=#ffffff;b=1" g="40,688,170,57" v="help／h"/>
<c id="te_r11c1" st="s=#999999;f=#d5e8d4" g="210,688,250,57" v="印說明（不觸網、不安裝）"/>
<c id="te_r11c2" st="s=#999999;f=#ffffff" g="460,688,420,57" v="—"/>
<c id="te_r11c3" st="s=#999999;f=#ffffff" g="880,688,260,57" v="—"/>
<c id="te_r11c4" st="s=#999999;f=#ffffff" g="1140,688,240,57" v="—"/>
<c id="te_r11c5" st="s=#999999;f=#ffe6cc" g="1380,688,210,57" v="P &amp;lt; floor → 3 + 6-18（零寫入；任何動詞含 help、救援路徑皆同）"/>
<c id="te_r12c0" st="s=#999999;f=#ffffff;b=1" g="40,745,170,42" v="ci/check.sh"/>
<c id="te_r12c1" st="s=#999999;f=#d5e8d4" g="210,745,250,42" v="⓪～⑤ 全過"/>
<c id="te_r12c2" st="s=#999999;f=#ffe6cc" g="460,745,420,42" v="⓪ version.local.toml 被 track；① sync 的 1；② verify 印記不符；③ upgrade --dry-run 需改 tracked 檔（印清單）"/>
<c id="te_r12c3" st="s=#999999;f=#f8cecc" g="880,745,260,42" v="④⑤ 工具／專案測試原碼傳出"/>
<c id="te_r12c4" st="s=#999999;f=#ffe6cc" g="1140,745,240,42" v="③ 仍有衝突標記"/>
<c id="te_r12c5" st="s=#999999;f=#ffe6cc" g="1380,745,210,42" v="① 的 3（P &amp;lt; floor 6-18／6-19）"/>
<c id="k14a" st="f=#ffe6cc;s=#d79b00;b=1" g="40,811,500,57" v="多工具彙總（已定，Q27）：不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）→ 做得完的做完 → 最後回最需要處理的碼：失敗 1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞"/>
<c id="k14b" st="f=#ffe6cc;s=#d79b00;b=1" g="560,811,520,88" v="結束碼 3 邊界（已定，Q23、v2.7-4）：版本／協定／schema 不合，須先升級或退回才能繼續；P &amp;lt; floor → 任何動詞（含 help、救援路徑）都回 3 + 6-18；回 3 時零寫入、無任何例外；新舊以 P／schema 比較，不用版本字串；floor 檢查先於任何上網；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1（印記不符、薄殼被改、自身升級完成要重跑）維持 1"/>
<c id="k14c" st="f=#ffe6cc;s=#d79b00;b=1" g="1100,811,490,88" v="CI 對應動作（已定）：0 → 過（merge）；1 → 修（照訊息裡的指令：本機 upgrade &amp;lt;repo&amp;gt; -y 後 commit 並 push／add／undev／git checkout 還原薄殼／加 -y／設 token）；2 → 解衝突（編輯檔案去掉 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記 → 重跑 upgrade 直到乾淨）；3 → 換版本（upgrade vendor_kit／git revert／bootstrap.sh 重建）"/>
<c id="k14d" st="shape=note;f=#ffffff;s=#999999" g="40,915,500,73" v="圖上顏色對應（v2.6-15、v2.7-8）：0 = 綠橢圓；1 需要人動作（印指令：請先 undev／請先 add／請先 git init／請重跑／請 upgrade vendor_kit／請設 token 或指定 @&amp;lt;tag&amp;gt;）= 橙橢圓；2 = 橙；3 = 橙；1 失敗（拉不到、寫入失敗、驗證失敗）= 紅橢圓"/>
<c id="k14e" st="shape=note;f=#ffffff;s=#999999" g="560,915,520,57" v="check.sh 整體結束碼 = 第一個失敗步驟的碼：⓪ local 被 track → 1；① sync 1／3；② verify 1；③ upgrade --dry-run：需改 tracked → 1、仍有衝突標記 → 2；④⑤ 原碼傳出（1／2／3 語意只對 vendor_kit 自身步驟成立）；⓪–⑤ 六步、一關過才下一關"/>
<c id="k14f" st="shape=note;f=#ffffff;s=#999999" g="1100,915,490,73" v="「—」= 該動詞沒有這個結束碼；表內 6-N = interface_spec §6 逐字訊息編號；dry-run 在本機一律 0（CI 為真且需改 tracked 檔 → 1）；EOF／Ctrl-C 中止 apply → 1、不套用、不記 declined；sync --verify（F5 已定）= 每檔 sha256 全驗，結束碼同 sync"/>
<c id="p14_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1018,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p14_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1018,140,64" v="黃：判斷"/>
<c id="p14_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1026,140,44" v="綠：起點／終點"/>
<c id="p14_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1020,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p14_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1020,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p14_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1028,88,40" v="白：步驟"/>
<c id="p14_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1028,170,40" v="虛線框：專案裡的檔案"/>
<c id="p14_lgt" st="text;s=none;f=none" g="1318,1018,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p14_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1086,120,36" v="便條：補充說明"/>
<c id="p14_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1086,150,36" v="橘框：規則（已定）"/>
<c id="p14_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="350,1086,170,36" v="灰底：泳道／表格表頭"/>
<c id="p14_lgx_c0" st="s=#999999;f=#d5e8d4" g="540,1086,110,36" v="綠格：結束碼 0"/>
<c id="p14_lgx_cx" st="s=#999999;f=#ffe6cc" g="670,1086,190,36" v="橙格：需要人動作（1／2／3）"/>
<c id="p14_lgx_c1" st="s=#999999;f=#f8cecc" g="880,1086,110,36" v="紅格：失敗 1"/>
<c id="p14_lgx_cell" st="s=#999999;f=#ffffff" g="1010,1086,110,36" v="白格：表格內容"/>
<c id="p14_th" st="text;fs=13;s=none;f=none;b=1" g="40,1124,200,28" v="本頁名詞"/>
<c id="p14_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1158,150,40" v="結束碼 0"/>
<c id="p14_tv0" st="f=#ffffff;s=#999999" g="190,1158,610,40" v="成功（含 warn）：add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符、update 已列出（有新版也 0）、dry-run 本機皆 0 + 提示"/>
<c id="p14_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1198,150,55" v="結束碼 1"/>
<c id="p14_tv1" st="f=#ffffff;s=#999999" g="190,1198,610,55" v="一般失敗或需使用者處理／重跑：工具層動詞回 1 時 version.toml 不動；例外：自身升級已改第一行後回 1、upgrade vendor_kit 重產薄殼後回 1（6-2）；圖上：印指令要人動作 = 橙、拉不到／寫入失敗／驗證失敗 = 紅"/>
<c id="p14_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1253,150,55" v="結束碼 2"/>
<c id="p14_tv2" st="f=#ffffff;s=#999999" g="190,1253,610,55" v="合併衝突（留 &amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt;&amp;lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版；解完重跑直到乾淨）；合併結果 TOML／just 解析失敗 → 2 留原檔、dest 入 conflicts、baseline 不推；update --exit-code 有新版 → 2"/>
<c id="p14_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1308,150,71" v="結束碼 3（Q23）"/>
<c id="p14_tv3" st="f=#ffffff;s=#999999" g="190,1308,610,71" v="現有薄殼／檔案／引擎的組合需先升級或退回：(a) P &amp;lt; floor 6-18 (b) schema 高於支援 6-19 (c) 降版無法無損讀 6-10 (d) dev -i 舊引擎要重產薄殼 (e) 舊薄殼跑新 major 一般動詞 6-36；任何動詞（含 help、救援路徑）在 P &amp;lt; floor 都回 3 + 6-18（v2.9-7）；零寫入、無任何例外；以 P／schema 比"/>
<c id="p14_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1379,150,40" v="多工具彙總（Q27）"/>
<c id="p14_tv4" st="f=#ffffff;s=#999999" g="190,1379,610,40" v="不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）、做得完的做完，最後回最需要處理的碼：1 &amp;gt; 衝突 2 &amp;gt; 有新版 2 &amp;gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞"/>
<c id="p14_tk5" st="f=#ffffff;s=#999999;b=1" g="840,1158,150,55" v="check.sh"/>
<c id="p14_tv5" st="f=#ffffff;s=#999999" g="990,1158,610,55" v=".vendor_kit/ci/check.sh：export CI=1 → ⓪ local 被 track → 1 → ① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；⓪–⑤ 六步、一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（④⑤ 原碼傳出）"/>
<c id="p14_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1213,150,40" v="frozen（CI 為真）"/>
<c id="p14_tv6" st="f=#ffffff;s=#999999" g="990,1213,610,40" v="CI 非空且不為 0／false → 不寫 tracked 檔、不查最新版；需改 tracked 檔 → 1 印清單（與 -y 無關）；6-6～6-8 提醒不紅燈；update 不受限"/>
<c id="p14_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1253,150,55" v="6-N 訊息編號"/>
<c id="p14_tv7" st="f=#ffffff;s=#999999" g="990,1253,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p14_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1308,150,71" v="結束碼 0／1／2／3"/>
<c id="p14_tv8" st="f=#ffffff;s=#999999" g="990,1308,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="流程 v2：vendor_kit release（1）build 與驗收">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：vendor_kit release（1）── build → release-test → 驗收（#26／#27、§7.4）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,116" v="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,136,220,28" v="維護者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,136,560,28" v="GitHub Actions"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="860,136,320,28" v="GHCR"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1200,136,390,28" v="Release 資產"/>
<c id="bR" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,180,1590,991" v="release vN（1）：兩平台各自 build → release-test → 驗收 → 兩平台一致檢查 → 全部通過？否 → 候選作廢；是 → 接（2）頁推 image 與資產"/>
<c id="bR_v2" parent="bR" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="v0" parent="bR" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,220,80" v="推候選（候選 tag／workflow_dispatch 指定 vN）"/>
<c id="v1" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,56,560,40" v="workflow 觸發：amd64 job + arm64 job（原生 runner）"/>
<c id="v2" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,136,560,42" v="build（#26）：兩 runner 各自單平台 buildx build（同一份 Dockerfile；LABEL =1／.protocol／.schema）"/>
<c id="v3a" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,199,560,40" v="release-test（各平台原生）：env-test"/>
<c id="v3n" parent="bR" st="shape=note;f=#ffffff;s=#999999" g="1180,198,390,42" v="release-test 矩陣：rootless docker、Podman；just 1.33.0 + latest；不用 QEMU 當閘門"/>
<c id="v3b" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,260,560,42" v="release-test：完整主機流程 install → add → upgrade → dev/undev → remove → prune → uninstall"/>
<c id="v4a" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,322,560,40" v="驗收（§7.4-1）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture"/>
<c id="v4g" parent="bR" st="f=#e1d5e7;s=#9673a6" g="840,322,320,40" v="已釋出引擎 image r（floor 以來每一版；永不刪）"/>
<c id="v4r" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1180,322,390,40" v="已釋出 bootstrap.sh(r)（Release 資產；永不刪）"/>
<c id="v4b" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,382,560,40" v="fixture 的 version.toml 第一行改成候選 C"/>
<c id="v4c" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,442,560,42" v="跑 §7.4-1 序列：sync 1+6-1 → upgrade vendor_kit 1+6-2 → sync 0 → 第二次 upgrade vendor_kit 0"/>
<c id="v5a" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,504,560,42" v="驗收（§7.4-4～8）：連升 r_i → r_j → C；floor 直接跳升；降版；&amp;lt; floor synthetic；舊引擎讀新檔 3"/>
<c id="v5b" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,566,560,42" v="驗收（§7.4-3、9～13）：升級後 == 全新安裝；fresh clone 無 gen；frozen sync；中斷重跑；TOML 異常"/>
<c id="v5c" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,628,560,42" v="驗收（§7.4-16／17）：離線包 amd64／arm64、斷網可用；禁止由候選樹複製 fixture、禁 stub 引擎"/>
<c id="v6a" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,706,560,40" v="兩平台一致檢查：工具 dist 逐檔位元組一致"/>
<c id="v6n" parent="bR" st="shape=note;f=#ffffff;s=#999999" g="1180,690,390,73" v="已定（decisions/multiarch）：不能靠單一 bake --push 帶測試就宣稱「失敗就不發佈」；分架構各自 build／test，綠了才 push-by-digest，最後由單一 job 合成 index；兩 runner 各自 push 同 tag 會互相覆蓋"/>
<c id="v6b" parent="bR" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,783,560,40" v="兩平台一致檢查：引擎 image 兩平台 LABEL（protocol／schema）一致"/>
<c id="v7x" parent="bR" st="ellipse;f=#f8cecc;s=#000000" g="20,843,220,80" v="否 → 失敗：不推 image、不發 Release、不進正式 tag（候選作廢）"/>
<c id="v7" parent="bR" st="rhombus;f=#FFF4C3;s=#000000" g="260,858,220,50" v="全部通過？"/>
<c id="v7z" parent="bR" st="text;s=none;f=none;b=1" g="260,943,560,42" v="是 ↓ 續「release（2）」頁：push-by-digest → index → bootstrap.sh／tar／.digest → Release"/>
<c id="ve0" edge source="v0" target="v1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve1" edge source="v1" target="v2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve2" edge source="v2" target="v3a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve2n" edge source="v3a" target="v3n" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve2b" edge source="v3a" target="v3b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve3" edge source="v3b" target="v4a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve4" edge source="v4a" target="v4g" st="es=orthogonalEdgeStyle;s=default;fc=default" v="拉"/>
<c id="ve4r" edge source="v4g" target="v4r" st="es=orthogonalEdgeStyle;s=default;fc=default" v="取"/>
<c id="ve4b" edge source="v4a" target="v4b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve4c" edge source="v4b" target="v4c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve5" edge source="v4c" target="v5a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve5b" edge source="v5a" target="v5b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve5c" edge source="v5b" target="v5c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve6" edge source="v5c" target="v6a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve6n" edge source="v6a" target="v6n" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve6b" edge source="v6a" target="v6b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve7" edge source="v6b" target="v7" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve8" edge source="v7" target="v7x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="ve9" edge source="v7" target="v7z" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="p15_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1187,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p15_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1187,140,64" v="黃：判斷"/>
<c id="p15_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1195,140,44" v="綠：起點／終點"/>
<c id="p15_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1189,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p15_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1189,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p15_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1197,88,40" v="白：步驟"/>
<c id="p15_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1197,170,40" v="虛線框：專案裡的檔案"/>
<c id="p15_lgt" st="text;s=none;f=none" g="1318,1187,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p15_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1255,120,36" v="便條：補充說明"/>
<c id="p15_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1255,150,36" v="橘框：規則（已定）"/>
<c id="p15_lgx_img" st="f=#e1d5e7;s=#9673a6" g="350,1255,170,36" v="紫：image（引擎與工具）"/>
<c id="p15_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="540,1255,170,36" v="灰底：泳道／表格表頭"/>
<c id="p15_th" st="text;fs=13;s=none;f=none;b=1" g="40,1293,200,28" v="本頁名詞"/>
<c id="p15_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1327,150,40" v="release"/>
<c id="p15_tv0" st="f=#ffffff;s=#999999" g="190,1327,610,40" v="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪"/>
<c id="p15_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1367,150,71" v="多架構 image／index digest（#26）"/>
<c id="p15_tv1" st="f=#ffffff;s=#999999" g="190,1367,610,71" v="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest"/>
<c id="p15_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1438,150,55" v="release-test"/>
<c id="p15_tv2" st="f=#ffffff;s=#999999" g="190,1438,610,55" v="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest"/>
<c id="p15_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1493,150,40" v="env-test"/>
<c id="p15_tv3" st="f=#ffffff;s=#999999" g="190,1493,610,40" v="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程"/>
<c id="p15_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1533,150,71" v="驗收（§7.4）"/>
<c id="p15_tv4" st="f=#ffffff;s=#999999" g="190,1533,610,71" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&amp;lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎"/>
<c id="p15_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1604,150,40" v="兩平台一致檢查"/>
<c id="p15_tv5" st="f=#ffffff;s=#999999" g="190,1604,610,40" v="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64"/>
<c id="p15_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1327,150,71" v="bootstrap.sh"/>
<c id="p15_tv6" st="f=#ffffff;s=#999999" g="990,1327,610,71" v="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &amp;lt;tar&amp;gt;"/>
<c id="p15_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1398,150,55" v="tar／.digest／SHA256SUMS（#27、Q26）"/>
<c id="p15_tv7" st="f=#ffffff;s=#999999" g="990,1398,610,55" v="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）"/>
<c id="p15_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1453,150,40" v="LABEL"/>
<c id="p15_tv8" st="f=#ffffff;s=#999999" g="990,1453,610,40" v="引擎 image build 時帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）"/>
<c id="p15_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1493,150,40" v="SemVer"/>
<c id="p15_tv9" st="f=#ffffff;s=#999999" g="990,1493,610,40" v="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR"/>
<c id="p15_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1533,150,71" v="結束碼 0／1／2／3"/>
<c id="p15_tv10" st="f=#ffffff;s=#999999" g="990,1533,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="流程 v2：vendor_kit release（2）推 image 與資產">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：vendor_kit release（2）── 推 image → 資產 → Release（#26／#27、Q26）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,116" v="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,136,220,28" v="維護者"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="280,136,560,28" v="GitHub Actions"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="860,136,320,28" v="GHCR"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="1200,136,390,28" v="Release 資產"/>
<c id="bR2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,180,1590,886" v="release vN（2）：全過才 push-by-digest → 單一 job 合成 index → 產 bootstrap.sh → tar + .digest → 離線包 → SHA256SUMS → 打正式 tag → 發布 Release"/>
<c id="bR2_v2" parent="bR2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="v8e" parent="bR2" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="260,36,560,58" v="來自「release（1）」頁：build／release-test／驗收／兩平台一致全部通過"/>
<c id="v8a" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,115,560,40" v="兩平台各自 push-by-digest（不打 tag；tag vN 不覆蓋）"/>
<c id="v8ag" parent="bR2" st="f=#e1d5e7;s=#9673a6" g="840,114,320,42" v="ghcr.io/&amp;lt;org&amp;gt;/vendor_kit@sha256:&amp;lt;amd64 digest&amp;gt;、@sha256:&amp;lt;arm64 digest&amp;gt;"/>
<c id="v8b" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,176,560,42" v="單一 job：docker buildx imagetools create -t vendor_kit:vN &amp;lt;兩個 digest&amp;gt; → 合成 index"/>
<c id="v8bg" parent="bR2" st="f=#e1d5e7;s=#9673a6" g="840,176,320,42" v="ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;（多架構；公開）"/>
<c id="v8c" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,238,560,40" v="imagetools inspect 斷言：index 含 linux/amd64 + linux/arm64"/>
<c id="v9" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,299,560,40" v="產 bootstrap.sh：內嵌完整引擎 ref（tag@index digest）；檔名固定"/>
<c id="v9r" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1180,298,390,42" v="bootstrap.sh（releases/download/vN/；latest 連結指向最新）"/>
<c id="v10a" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,360,560,40" v="docker save 各平台 image → vendor_kit-vN-amd64.tar、vendor_kit-vN-arm64.tar"/>
<c id="v10ar" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1180,360,390,40" v="vendor_kit-vN-&amp;lt;平台&amp;gt;.tar（各平台一個）"/>
<c id="v10b" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,420,560,40" v="寫同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = index digest）"/>
<c id="v10br" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1180,420,390,40" v="vendor_kit-vN-&amp;lt;平台&amp;gt;.tar.digest"/>
<c id="v10c" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,539,560,40" v="組離線包 vendor_kit-vN-local.tar.gz"/>
<c id="v10cr" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1180,480,390,158" v="離線包內容"/>
<c id="v10cr_0" parent="v10cr" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,362,42" v="bootstrap.sh（契約入口：bootstrap.sh --local &amp;lt;tar&amp;gt;）"/>
<c id="v10cr_1" parent="v10cr" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,362,26" v="各平台 tar + .tar.digest"/>
<c id="v10cr_2" parent="v10cr" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,106,362,42" v="local_bootstrap.sh：便利包裝（非契約；偵測架構、挑 tar、exec bootstrap.sh --local）"/>
<c id="v10d" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,658,560,40" v="寫 SHA256SUMS（列所有資產）"/>
<c id="v10dr" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1180,658,390,40" v="SHA256SUMS"/>
<c id="v11a" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,718,560,40" v="打正式 tag vN（指向候選 commit）"/>
<c id="v11b" parent="bR2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="260,778,560,42" v="發布 Release vN：附 bootstrap.sh、tar、.digest、離線包、SHA256SUMS；release notes 含 index digest 與不用腳本的替代 docker run 指令"/>
<c id="v11n" parent="bR2" st="shape=note;f=#ffffff;s=#999999" g="1180,778,390,42" v="已釋出 image／Release 資產／fixture 永不刪；下游 Renovate 會看到新 tag@digest"/>
<c id="v12" parent="bR2" st="ellipse;f=#d5e8d4;s=#000000" g="20,840,220,40" v="0：Release vN 發布"/>
<c id="ve10" edge source="v8e" target="v8a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve10g" edge source="v8a" target="v8ag" st="es=orthogonalEdgeStyle;s=default;fc=default" v="推"/>
<c id="ve11" edge source="v8a" target="v8b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve11g" edge source="v8b" target="v8bg" st="es=orthogonalEdgeStyle;s=default;fc=default" v="建"/>
<c id="ve11c" edge source="v8b" target="v8c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve12" edge source="v8c" target="v9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve12r" edge source="v9" target="v9r" st="es=orthogonalEdgeStyle;s=default;fc=default" v="產"/>
<c id="ve13" edge source="v9" target="v10a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve13r" edge source="v10a" target="v10ar" st="es=orthogonalEdgeStyle;s=default;fc=default" v="產"/>
<c id="ve13b" edge source="v10a" target="v10b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve13br" edge source="v10b" target="v10br" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ve13c" edge source="v10b" target="v10c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve13cr" edge source="v10c" target="v10cr" st="es=orthogonalEdgeStyle;s=default;fc=default" v="組"/>
<c id="ve13d" edge source="v10c" target="v10d" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve13dr" edge source="v10d" target="v10dr" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="ve14" edge source="v10d" target="v11a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve15" edge source="v11a" target="v11b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve15n" edge source="v11b" target="v11n" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="ve16" edge source="v11b" target="v12" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.88,0,," pts="560,1040"/>
<c id="p15c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1082,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p15c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1082,140,64" v="黃：判斷"/>
<c id="p15c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1090,140,44" v="綠：起點／終點"/>
<c id="p15c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1084,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p15c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1084,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p15c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1092,88,40" v="白：步驟"/>
<c id="p15c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1092,170,40" v="虛線框：專案裡的檔案"/>
<c id="p15c_lgt" st="text;s=none;f=none" g="1318,1082,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p15c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1150,120,36" v="便條：補充說明"/>
<c id="p15c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="180,1150,170,36" v="紫：image（引擎與工具）"/>
<c id="p15c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="370,1150,170,36" v="灰底：泳道／表格表頭"/>
<c id="p15c_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="560,1150,200,36" v="虛線橢圓：來自其他頁"/>
<c id="p15c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1188,200,28" v="本頁名詞"/>
<c id="p15c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1222,150,40" v="release"/>
<c id="p15c_tv0" st="f=#ffffff;s=#999999" g="190,1222,610,40" v="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪"/>
<c id="p15c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,1262,150,71" v="多架構 image／index digest（#26）"/>
<c id="p15c_tv1" st="f=#ffffff;s=#999999" g="190,1262,610,71" v="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest"/>
<c id="p15c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,1333,150,55" v="release-test"/>
<c id="p15c_tv2" st="f=#ffffff;s=#999999" g="190,1333,610,55" v="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest"/>
<c id="p15c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,1388,150,40" v="env-test"/>
<c id="p15c_tv3" st="f=#ffffff;s=#999999" g="190,1388,610,40" v="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程"/>
<c id="p15c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,1428,150,71" v="驗收（§7.4）"/>
<c id="p15c_tv4" st="f=#ffffff;s=#999999" g="190,1428,610,71" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&amp;lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎"/>
<c id="p15c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,1499,150,40" v="兩平台一致檢查"/>
<c id="p15c_tv5" st="f=#ffffff;s=#999999" g="190,1499,610,40" v="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64"/>
<c id="p15c_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1222,150,71" v="bootstrap.sh"/>
<c id="p15c_tv6" st="f=#ffffff;s=#999999" g="990,1222,610,71" v="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&amp;lt;org&amp;gt;/vendor_kit:vN@sha256:&amp;lt;index digest&amp;gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &amp;lt;tar&amp;gt;"/>
<c id="p15c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,1293,150,55" v="tar／.digest／SHA256SUMS（#27、Q26）"/>
<c id="p15c_tv7" st="f=#ffffff;s=#999999" g="990,1293,610,55" v="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&amp;lt;hex64&amp;gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）"/>
<c id="p15c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,1348,150,40" v="LABEL"/>
<c id="p15c_tv8" st="f=#ffffff;s=#999999" g="990,1348,610,40" v="引擎 image build 時帶 io.github.&amp;lt;org&amp;gt;.vendor_kit=1、….protocol=&amp;lt;floor_P&amp;gt;-&amp;lt;current_P&amp;gt;、….schema=&amp;lt;N&amp;gt;（啟動器不起容器即可判 floor）"/>
<c id="p15c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,1388,150,40" v="SemVer"/>
<c id="p15c_tv9" st="f=#ffffff;s=#999999" g="990,1388,610,40" v="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR"/>
<c id="p15c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,1428,150,71" v="結束碼 0／1／2／3"/>
<c id="p15c_tv10" st="f=#ffffff;s=#999999" g="990,1428,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="流程 v2：離線包（1）bootstrap.sh --local">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：離線包（1）── bootstrap.sh --local &amp;lt;引擎 tar&amp;gt; → load → install（#27、Q26、§4.8）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,163" v="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &amp;lt;repo&amp;gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,183,230,28" v="使用者（離線機）"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="290,183,400,28" v="bootstrap.sh（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="710,183,240,28" v="docker daemon"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="970,183,320,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1310,183,280,28" v="專案目錄"/>
<c id="bO1" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,227,1590,1625" v="離線接入（1）只涉及引擎：離線包 → bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（契約入口）→ 前置檢查（不分 tar／tag）→ 判別值三分支 → tar 形 load + 讀 .digest（tag 形跳過）→ image ID → install → version.local.toml"/>
<c id="bO1_v2" parent="bO1" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="o0" parent="bO1" st="ellipse;f=#d5e8d4;s=#000000" g="-9,36,288,102" v="有網路的機器下載 vendor_kit-vN-local.tar.gz（SHA256SUMS 驗）→ 帶到離線機"/>
<c id="o1" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,154,230,73" v="解開：bootstrap.sh、各平台引擎 tar + .tar.digest（另附 local_bootstrap.sh）；不含工具 tar"/>
<c id="o1w" parent="bO1" st="text;s=none;f=none;b=1" g="20,243,230,57" v="【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步："/>
<c id="o1a" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,316,230,57" v="docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構"/>
<c id="o1b" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,389,230,42" v="挑該平台的引擎 tar（vendor_kit-vN-&amp;lt;arch&amp;gt;.tar）"/>
<c id="o1c" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,447,230,42" v="exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;"/>
<c id="o2" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,505,230,57" v="sh bootstrap.sh --local &amp;lt;引擎 tar&amp;gt; [-y]（契約入口；-t &amp;lt;repo&amp;gt; 走 registry 需網路，離線機不帶）"/>
<c id="o2l" parent="bO1" st="text;s=none;f=none;b=1" g="270,512,400,42" v="↓ 前置檢查（v2.9-1：不分 --local 值是 tar 還是 tag，一律先做）"/>
<c id="o5x" parent="bO1" st="ellipse;f=#ffe6cc;s=#000000" g="20,578,230,58" v="否 → 1 + 6-16：請先 git init"/>
<c id="o5" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="270,582,300,50" v="在 git repo 內？"/>
<c id="o6x" parent="bO1" st="ellipse;f=#ffe6cc;s=#000000" g="20,652,230,80" v="否 → 1 + 6-23：請裝 GitHub release 版 just"/>
<c id="o6" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="270,667,300,50" v="just ≥ 1.33.0？"/>
<c id="o3" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="270,775,300,81" v="--local 值含 / 或以 .tar 結尾？"/>
<c id="o3n" parent="bO1" st="f=#ffe6cc;s=#d79b00;b=1" g="1290,748,280,135" v="已定（B1；grilling 2026-09-19 末條、v2.7-2、v2.8-4、v2.9-1）三分支：值含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load；其餘 → image tag（不 load、不讀 .digest）；既存檔且可解讀為 tag → 1 + 6-37 消歧（請寫 ./&amp;lt;v&amp;gt; 或完整 ref）；前置檢查（git repo／just）不分型別一律先做"/>
<c id="o3bx" parent="bO1" st="ellipse;f=#ffe6cc;s=#000000" g="20,910,230,58" v="否 → 1：檔案路徑必須存在"/>
<c id="o3b" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="300,899,240,81" v="該路徑的檔案存在？"/>
<c id="o3t" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="550,903,120,73" v="否 → tag 形：不 load、不讀 .digest（本機須已有該 image）"/>
<c id="o3cx" parent="bO1" st="ellipse;f=#ffe6cc;s=#000000" g="20,996,230,80" v="是 → 1 + 6-37：值歧義（既存檔也像 tag），請寫 ./&amp;lt;v&amp;gt; 或完整 ref"/>
<c id="o3c" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="270,996,300,81" v="值同時可解讀為 image tag？"/>
<c id="o4x" parent="bO1" st="ellipse;f=#ffe6cc;s=#000000" g="20,1104,230,58" v="否 → 1：同名 .tar.digest 旁檔缺"/>
<c id="o4" parent="bO1" st="rhombus;f=#FFF4C3;s=#000000" g="270,1093,300,81" v="同名 .tar.digest 存在？"/>
<c id="o6c" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1198,300,40" v="docker load &amp;lt; &amp;lt;引擎 tar&amp;gt;"/>
<c id="o6d" parent="bO1" st="f=#e1d5e7;s=#9673a6" g="690,1190,170,57" v="本機 image vendor_kit:vN（只有 tag、無 RepoDigests）"/>
<c id="o7a" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1263,300,40" v="讀 &amp;lt;tar&amp;gt;.digest → 正式 index digest"/>
<c id="o7b" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1319,400,42" v="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID（tag 形由此匯入：跳過 load 與 .digest）"/>
<c id="o7bd" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="690,1319,170,42" v="回 image ID（sha256:&amp;lt;hex64&amp;gt;）"/>
<c id="o8" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1420,400,40" v="docker run 本機 image install（本機有 → 不 pull）"/>
<c id="o8e" parent="bO1" st="f=#dae8fc;s=#6c8ebf" g="950,1396,320,88" v="install：建薄殼四檔、gen/.stamp、baseline/.gitkeep；version.toml 第一行 = 正式 ref@digest（tar 形：.digest 旁檔；tag 形：既有 version.toml 值，第一次接入用 bootstrap.sh 內嵌引擎 ref）"/>
<c id="o8f" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1290,1377,280,126" v="install 寫"/>
<c id="o8f_0" parent="o8f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,252,42" v="version.toml 第一行（正式 ref@digest）"/>
<c id="o8f_1" parent="o8f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,252,42" v="薄殼四檔、gen/.stamp、.gitkeep、justfile 一行、.dockerignore 三行"/>
<c id="o9" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,1519,400,42" v="install 成功後寫 version.local.toml：vendor_kit = &quot;vendor_kit:vN&quot; + vendor_kit_image_id（失敗清除）"/>
<c id="o9f" parent="bO1" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1290,1519,280,42" v="version.local.toml（不進 git）：本機 tag + image ID"/>
<c id="o9z" parent="bO1" st="text;s=none;f=none;b=1" g="270,1577,400,42" v="↓ 續「離線包（2）」頁：工具由使用者另備工具 tar，逐一 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；之後斷網 sync"/>
<c id="oe0" edge source="o0" target="o1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe1" edge source="o1" target="o1w" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe1a" edge source="o1w" target="o1a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe1b" edge source="o1a" target="o1b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe1c" edge source="o1b" target="o1c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe1w" edge source="o1c" target="o2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe2" edge source="o2" target="o2l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe2l" edge source="o2l" target="o5" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe6x" edge source="o5" target="o5x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="oe6b" edge source="o5" target="o6" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe6bx" edge source="o6" target="o6x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="oe6c" edge source="o6" target="o3" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe3t" edge source="o3" target="o3t" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.69,0,," pts="630,1042" v="否"/>
<c id="oe3b" edge source="o3" target="o3b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe3bx" edge source="o3b" target="o3bx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="oe3c" edge source="o3b" target="o3c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe3cx" edge source="o3c" target="o3cx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="是"/>
<c id="oe4" edge source="o3c" target="o4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="否"/>
<c id="oe5" edge source="o4" target="o4x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="oe7" edge source="o4" target="o6c" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe8" edge source="o6c" target="o6d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="載"/>
<c id="oe9" edge source="o6c" target="o7a" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe9b" edge source="o7a" target="o7b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe9d" edge source="o7b" target="o7bd" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe10" edge source="o7b" target="o8" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe3tj" edge source="o3t" target="o7b" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.85,0,," pts="910,1166;910,1538;650,1538" v="tag 形：跳過 load／.digest"/>
<c id="oe11" edge source="o8" target="o8e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe12" edge source="o8e" target="o8f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="oe13" edge source="o8" target="o9" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe14" edge source="o9" target="o9f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="oe15" edge source="o9" target="o9z" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="p16_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1868,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p16_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1868,140,64" v="黃：判斷"/>
<c id="p16_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1876,140,44" v="綠：起點／終點"/>
<c id="p16_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1870,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p16_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1870,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p16_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1878,88,40" v="白：步驟"/>
<c id="p16_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1878,170,40" v="虛線框：專案裡的檔案"/>
<c id="p16_lgt" st="text;s=none;f=none" g="1318,1868,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p16_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1936,120,36" v="便條：補充說明"/>
<c id="p16_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1936,150,36" v="橘框：規則（已定）"/>
<c id="p16_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1936,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p16_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1936,170,36" v="紫：image（引擎與工具）"/>
<c id="p16_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1936,170,36" v="灰底：泳道／表格表頭"/>
<c id="p16_th" st="text;fs=13;s=none;f=none;b=1" g="40,1974,200,28" v="本頁名詞"/>
<c id="p16_tk0" st="f=#ffffff;s=#999999;b=1" g="40,2008,150,55" v="離線包（#27、Q26）"/>
<c id="p16_tv0" st="f=#ffffff;s=#999999" g="190,2008,610,55" v="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援"/>
<c id="p16_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2063,150,102" v="bootstrap.sh --local（契約入口）"/>
<c id="p16_tv1" st="f=#ffffff;s=#999999" g="190,2063,610,102" v="離線接入的契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &amp;lt;repo&amp;gt; 仍是 add &amp;lt;repo&amp;gt;[@tag]，走 registry、需網路，離線機不帶 -t；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load + 讀 .digest；其餘 → image tag（不 load、不讀 .digest，只 inspect image ID）；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&amp;lt;v&amp;gt; 或完整 ref」"/>
<c id="p16_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2165,150,55" v="add --local 只收 tar（v2.10-3）"/>
<c id="p16_tv2" st="f=#ffffff;s=#999999" g="190,2165,610,55" v="add --local &amp;lt;值&amp;gt; 只接受存在的 .tar 檔（新工具沒有既有 digest 可用；tag 形只對 bootstrap.sh --local 有意義）；不是存在的 .tar → 1 + 6-24 類提示；§1.1 選項表的 tag 形只適用 bootstrap.sh"/>
<c id="p16_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2220,150,71" v="工具 tar（來源，v2.8-5）"/>
<c id="p16_tv3" st="f=#ffffff;s=#999999" g="190,2220,610,71" v="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &amp;lt;repo&amp;gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&amp;lt;hex64&amp;gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;"/>
<c id="p16_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2291,150,55" v="local_bootstrap.sh（便利包裝，非契約）"/>
<c id="p16_tv4" st="f=#ffffff;s=#999999" g="190,2291,610,55" v="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）"/>
<c id="p16_tk5" st="f=#ffffff;s=#999999;b=1" g="840,2008,150,40" v=".digest 旁檔"/>
<c id="p16_tv5" st="f=#ffffff;s=#999999" g="990,2008,610,40" v="&amp;lt;name&amp;gt;.tar.digest 一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag"/>
<c id="p16_tk6" st="f=#ffffff;s=#999999;b=1" g="840,2048,150,55" v="image ID／local_image_id"/>
<c id="p16_tv6" st="f=#ffffff;s=#999999" g="990,2048,610,55" v="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）"/>
<c id="p16_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2103,150,40" v="version.local.toml"/>
<c id="p16_tv7" st="f=#ffffff;s=#999999" g="990,2103,610,40" v="不進 git；--local 時寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull"/>
<c id="p16_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2143,150,55" v="離線可用（Q26）"/>
<c id="p16_tv8" st="f=#ffffff;s=#999999" g="990,2143,610,55" v="啟動器一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang"/>
<c id="p16_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2198,150,55" v="6-N 訊息編號"/>
<c id="p16_tv9" st="f=#ffffff;s=#999999" g="990,2198,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p16_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2253,150,71" v="結束碼 0／1／2／3"/>
<c id="p16_tv10" st="f=#ffffff;s=#999999" g="990,2253,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
<page name="流程 v2：離線包（2）add --local 與斷網 sync">
<c id="title" st="text;fs=18;b=1" g="40,20,1000,34" v="流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具 → 斷網 sync（Q26、§4.8、§7.4-17）"/>
<c id="pend" st="shape=note;f=#ffffff;s=#999999" g="1040,12,560,163" v="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &amp;lt;repo&amp;gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。"/>
<c id="hdr0" st="f=#e6e6e6;s=#999999;b=1" g="40,183,230,28" v="使用者（離線機）"/>
<c id="hdr1" st="f=#e6e6e6;s=#999999;b=1" g="290,183,400,28" v="啟動器（主機 sh）"/>
<c id="hdr2" st="f=#e6e6e6;s=#999999;b=1" g="710,183,240,28" v="docker daemon"/>
<c id="hdr3" st="f=#e6e6e6;s=#999999;b=1" g="970,183,320,28" v="引擎容器"/>
<c id="hdr4" st="f=#e6e6e6;s=#999999;b=1" g="1310,183,280,28" v="專案目錄"/>
<c id="bO1b" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,227,1590,1090" v="離線接工具（v2.8-5、v2.10-3）：工具 tar 由工具 repo 提供、使用者另備 → 每個工具各跑一次 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;（只收 tar）：驗 .tar 存在 → load → 讀 .digest → image ID → resolve → create／cp → apply（flock → 重驗 → 寫入）"/>
<c id="bO1b_v2" parent="bO1b" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="oo0" parent="bO1b" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="20,36,230,80" v="來自「離線包（1）」頁：install 完成（引擎可離線跑）"/>
<c id="oo1" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,148,230,73" v="有網路的機器取得工具 tar + 同名 .tar.digest（由工具 repo 提供；不在 vendor_kit 離線包內）→ 帶到離線機"/>
<c id="oo1n" parent="bO1b" st="f=#ffe6cc;s=#d79b00;b=1" g="1290,132,280,104" v="已定（v2.8-5）：vendor_kit 離線包只含引擎；-t &amp;lt;repo&amp;gt; 走 registry（需網路）；離線接工具 = 使用者另備工具 tar（工具 repo 的 docker save + .digest），逐工具 add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;；離線 upgrade 不支援"/>
<c id="o10l" parent="bO1b" st="text;s=none;f=none;b=1" g="20,252,230,26" v="↓ 每個工具各跑一次（一次一個）："/>
<c id="o10" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="20,294,230,42" v="just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt; [-y]"/>
<c id="o10qx" parent="bO1b" st="ellipse;f=#ffe6cc;s=#000000" g="20,352,230,80" v="否 → 1：add --local 只接受 tar（tag 形只有 bootstrap.sh）"/>
<c id="o10q" parent="bO1b" st="rhombus;f=#FFF4C3;s=#000000" g="270,367,300,50" v="值是存在的 .tar 檔？"/>
<c id="o10a" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,448,400,40" v="是：docker load &amp;lt; &amp;lt;工具 tar&amp;gt;"/>
<c id="o10d" parent="bO1b" st="f=#e1d5e7;s=#9673a6" g="690,448,240,40" v="本機 image &amp;lt;repo&amp;gt;-dist:&amp;lt;tag&amp;gt;"/>
<c id="o10b" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,504,400,40" v="讀 &amp;lt;工具 tar&amp;gt;.digest → 正式 index digest（旁檔缺 → 1）"/>
<c id="o10c" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,560,400,40" v="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID"/>
<c id="o10cd" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="690,560,240,40" v="回 image ID（sha256:&amp;lt;hex64&amp;gt;）"/>
<c id="o10r" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,616,400,42" v="docker run 引擎 resolve add &amp;lt;repo&amp;gt; --local（帶 index digest + image ID；永不 -t）"/>
<c id="o10re" parent="bO1b" st="f=#dae8fc;s=#6c8ebf" g="950,616,320,42" v="resolve（不寫）：算計畫、指紋；stdout vk-resolve/1"/>
<c id="o10p" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,674,400,40" v="docker create／cp 取本機 image 的 dist 到暫存（不 pull）"/>
<c id="o10p2" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,731,400,40" v="docker run 引擎 apply add（暫存唯讀掛進 /dist）"/>
<c id="o10e" parent="bO1b" st="f=#dae8fc;s=#6c8ebf" g="950,730,320,42" v="apply add：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）"/>
<c id="o10e2" parent="bO1b" st="f=#dae8fc;s=#6c8ebf" g="950,788,320,42" v="重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）"/>
<c id="o10e3" parent="bO1b" st="f=#dae8fc;s=#6c8ebf" g="950,888,320,57" v="寫入（見「add（2）」頁）：version.toml [tools] 正式 ref@digest；metadata 記 local_image_id"/>
<c id="o10f" parent="bO1b" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1;b=1;container=1;collapsible=0" g="1290,846,280,142" v="add 寫（同「add（2）」頁）"/>
<c id="o10f_0" parent="o10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,26,252,42" v="version.toml [tools] 行（正式 ref@digest）"/>
<c id="o10f_1" parent="o10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,74,252,26" v="metadata：source + local_image_id"/>
<c id="o10f_2" parent="o10f" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="8,106,252,26" v="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp"/>
<c id="o11" parent="bO1b" st="ellipse;f=#d5e8d4;s=#000000" g="20,1004,230,80" v="0：該工具接入完成（version.toml 同線上）；下一個工具再跑 add"/>
<c id="oe20" edge source="oo0" target="oo1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe20l" edge source="oo1" target="o10l" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe21" edge source="o10l" target="o10" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe21q" edge source="o10" target="o10q" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.05,0,," pts="155,571;440,571"/>
<c id="oe21x" edge source="o10q" target="o10qx" st="es=orthogonalEdgeStyle;s=default;fc=default" v="否"/>
<c id="oe22" edge source="o10q" target="o10a" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="是"/>
<c id="oe22d" edge source="o10a" target="o10d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="載"/>
<c id="oe23" edge source="o10a" target="o10b" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe24" edge source="o10b" target="o10c" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe24d" edge source="o10c" target="o10cd" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe25" edge source="o10c" target="o10r" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe25e" edge source="o10r" target="o10re" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe26" edge source="o10r" target="o10p" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe26b" edge source="o10p" target="o10p2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe26e" edge source="o10p2" target="o10e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe26f" edge source="o10e" target="o10e2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe26g" edge source="o10e2" target="o10e3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="oe27" edge source="o10e3" target="o10f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="oe28" edge source="o10e3" target="o11" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.90,0,," pts="1130,1271"/>
<c id="bO2" st="swimlane;startSize=30;b=1;container=1;collapsible=1;f=#f5f5f5;swf=#ffffff;s=#000000" g="20,1333,1590,470" v="之後（Q26）：斷網下 sync／build 必成功 —— 啟動器先 docker image inspect，本機有就不 pull；離線 upgrade 不支援"/>
<c id="bO2_v2" parent="bO2" st="f=#00b050;s=none;fc=#ffffff;fs=9;b=1" g="1546,5,30,20" v="v2"/>
<c id="w0" parent="bO2" st="ellipse;f=#d5e8d4;s=#000000" g="20,36,230,80" v="斷網：just &amp;lt;ns&amp;gt; build（自動 _sync）／just vendor_kit sync"/>
<c id="w1" parent="bO2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,55,400,42" v="快路徑：grep 比對 gen/*.stamp 第一行 vs version.toml；全相符 → 不起容器 → 0（sync --verify 或 CI 為真則全驗）"/>
<c id="w2" parent="bO2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,155,400,42" v="有差：docker image inspect &amp;lt;ref&amp;gt;（version.toml 的正式 ref）"/>
<c id="w2r" parent="bO2" st="f=#ffe6cc;s=#d79b00;b=1" g="1290,132,280,88" v="已定（v2.6-1、19條-11）：不用 --pull never（docker 19.03 無此旗標）；先 inspect 本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）"/>
<c id="w3x" parent="bO2" st="ellipse;f=#f8cecc;s=#000000" g="20,236,230,80" v="無 → 1 + 6-31：拉不到（--timeout 內結束、不 hang）"/>
<c id="w3" parent="bO2" st="rhombus;f=#FFF4C3;s=#000000" g="270,236,220,81" v="本機有該 image？"/>
<c id="w3d" parent="bO2" st="f=#e1d5e7;s=#9673a6" g="690,256,240,42" v="本機已有 image（docker load 過的）"/>
<c id="w4" parent="bO2" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="270,342,400,40" v="有：直接 docker run（不 pull）resolve／apply sync"/>
<c id="w4e" parent="bO2" st="f=#dae8fc;s=#6c8ebf" g="950,333,320,57" v="sync verify：image ID == metadata local_image_id（離線對照 index digest）→ materialize／verify cache"/>
<c id="w4f" parent="bO2" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1290,340,280,42" v="cache/&amp;lt;repo&amp;gt;/、gen/&amp;lt;repo&amp;gt;.stamp、gen/tools.just（只寫不進 git 的）"/>
<c id="w5" parent="bO2" st="ellipse;f=#d5e8d4;s=#000000" g="20,406,230,58" v="0：成功、不起 pull（驗收 §7.4-17）"/>
<c id="we0" edge source="w0" target="w1" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we1" edge source="w1" target="w2" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we2" edge source="w2" target="w3" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we3" edge source="w3" target="w3x" st="es=orthogonalEdgeStyle;s=default;fc=default" v="無"/>
<c id="we4" edge source="w3" target="w3d" st="es=orthogonalEdgeStyle;s=default;fc=default" v="inspect"/>
<c id="we5" edge source="w3" target="w4" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.6,0,," v="有"/>
<c id="we6" edge source="w4" target="w4e" st="es=orthogonalEdgeStyle;s=default;fc=default"/>
<c id="we7" edge source="w4e" target="w4f" st="es=orthogonalEdgeStyle;s=default;fc=default" v="寫"/>
<c id="we8" edge source="w4" target="w5" st="es=orthogonalEdgeStyle;s=default;fc=default" g="-0.80,0,," pts="490,1768"/>
<c id="p16c_lg0" st="swimlane;startSize=34;b=1;container=0;collapsible=0;f=#f5f5f5;swf=#ffffff;s=#000000" g="40,1819,200,60" v="淺灰：情境分組（無狀態意義）"/>
<c id="p16c_lg1" st="rhombus;f=#FFF4C3;s=#000000" g="260,1819,140,64" v="黃：判斷"/>
<c id="p16c_lg2" st="ellipse;f=#d5e8d4;s=#000000" g="420,1827,140,44" v="綠：起點／終點"/>
<c id="p16c_lg3" st="ellipse;f=#f8cecc;s=#000000" g="580,1821,190,56" v="紅：失敗終止（拉不到／寫壞）"/>
<c id="p16c_lg4" st="ellipse;f=#ffe6cc;s=#000000" g="790,1821,210,56" v="橙：需要人動作（1／3 印指令；2 解衝突）"/>
<c id="p16c_lg5" st="f=#ffffff;s=light-dark(#000000,#9577A3)" g="1020,1829,88,40" v="白：步驟"/>
<c id="p16c_lg6" st="f=#ffffff;s=light-dark(#000000,#9577A3);dashed=1" g="1128,1829,170,40" v="虛線框：專案裡的檔案"/>
<c id="p16c_lgt" st="text;s=none;f=none" g="1318,1819,280,60" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）"/>
<c id="p16c_lgx_note" st="shape=note;f=#ffffff;s=#999999" g="40,1887,120,36" v="便條：補充說明"/>
<c id="p16c_lgx_rule" st="f=#ffe6cc;s=#d79b00;b=1" g="180,1887,150,36" v="橘框：規則（已定）"/>
<c id="p16c_lgx_sub" st="f=#dae8fc;s=#6c8ebf" g="350,1887,190,36" v="藍：引擎子命令（容器內）"/>
<c id="p16c_lgx_img" st="f=#e1d5e7;s=#9673a6" g="560,1887,170,36" v="紫：image（引擎與工具）"/>
<c id="p16c_lgx_hdr" st="f=#e6e6e6;s=#999999;b=1" g="750,1887,170,36" v="灰底：泳道／表格表頭"/>
<c id="p16c_lgx_entry" st="ellipse;f=#ffffff;s=#000000;dashed=1" g="940,1887,200,36" v="虛線橢圓：來自其他頁"/>
<c id="p16c_th" st="text;fs=13;s=none;f=none;b=1" g="40,1925,200,28" v="本頁名詞"/>
<c id="p16c_tk0" st="f=#ffffff;s=#999999;b=1" g="40,1959,150,55" v="離線包（#27、Q26）"/>
<c id="p16c_tv0" st="f=#ffffff;s=#999999" g="190,1959,610,55" v="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援"/>
<c id="p16c_tk1" st="f=#ffffff;s=#999999;b=1" g="40,2014,150,102" v="bootstrap.sh --local（契約入口）"/>
<c id="p16c_tv1" st="f=#ffffff;s=#999999" g="190,2014,610,102" v="離線接入的契約入口 = bootstrap.sh --local &amp;lt;引擎 tar&amp;gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &amp;lt;repo&amp;gt; 仍是 add &amp;lt;repo&amp;gt;[@tag]，走 registry、需網路，離線機不帶 -t；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load + 讀 .digest；其餘 → image tag（不 load、不讀 .digest，只 inspect image ID）；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&amp;lt;v&amp;gt; 或完整 ref」"/>
<c id="p16c_tk2" st="f=#ffffff;s=#999999;b=1" g="40,2116,150,55" v="add --local 只收 tar（v2.10-3）"/>
<c id="p16c_tv2" st="f=#ffffff;s=#999999" g="190,2116,610,55" v="add --local &amp;lt;值&amp;gt; 只接受存在的 .tar 檔（新工具沒有既有 digest 可用；tag 形只對 bootstrap.sh --local 有意義）；不是存在的 .tar → 1 + 6-24 類提示；§1.1 選項表的 tag 形只適用 bootstrap.sh"/>
<c id="p16c_tk3" st="f=#ffffff;s=#999999;b=1" g="40,2171,150,71" v="工具 tar（來源，v2.8-5）"/>
<c id="p16c_tv3" st="f=#ffffff;s=#999999" g="190,2171,610,71" v="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &amp;lt;repo&amp;gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&amp;lt;hex64&amp;gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &amp;lt;repo&amp;gt; --local &amp;lt;工具 tar&amp;gt;"/>
<c id="p16c_tk4" st="f=#ffffff;s=#999999;b=1" g="40,2242,150,55" v="local_bootstrap.sh（便利包裝，非契約）"/>
<c id="p16c_tv4" st="f=#ffffff;s=#999999" g="190,2242,610,55" v="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &amp;lt;tar&amp;gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）"/>
<c id="p16c_tk5" st="f=#ffffff;s=#999999;b=1" g="40,2297,150,40" v=".digest 旁檔"/>
<c id="p16c_tv5" st="f=#ffffff;s=#999999" g="190,2297,610,40" v="&amp;lt;name&amp;gt;.tar.digest 一行 sha256:&amp;lt;hex64&amp;gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag"/>
<c id="p16c_tk6" st="f=#ffffff;s=#999999;b=1" g="840,1959,150,55" v="image ID／local_image_id"/>
<c id="p16c_tv6" st="f=#ffffff;s=#999999" g="990,1959,610,55" v="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）"/>
<c id="p16c_tk7" st="f=#ffffff;s=#999999;b=1" g="840,2014,150,40" v="version.local.toml"/>
<c id="p16c_tv7" st="f=#ffffff;s=#999999" g="990,2014,610,40" v="不進 git；--local 時寫 vendor_kit = &quot;&amp;lt;tag&amp;gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull"/>
<c id="p16c_tk8" st="f=#ffffff;s=#999999;b=1" g="840,2054,150,55" v="離線可用（Q26）"/>
<c id="p16c_tv8" st="f=#ffffff;s=#999999" g="990,2054,610,55" v="啟動器一律先 docker image inspect &amp;lt;ref&amp;gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang"/>
<c id="p16c_tk9" st="f=#ffffff;s=#999999;b=1" g="840,2109,150,71" v="sync 快路徑（Q22）／--verify（F5）"/>
<c id="p16c_tv9" st="f=#ffffff;s=#999999" g="990,2109,610,71" v="sync（無參數）啟動器只用 grep 比對 gen/.stamp 第一行 == version.toml 引擎 ref、gen/&amp;lt;repo&amp;gt;.stamp 第一行 == 鎖定 digest、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0；有差才起引擎；sync --verify 或 CI 為真 → 每檔 sha256 全驗（verify 用 local_image_id 對照）"/>
<c id="p16c_tk10" st="f=#ffffff;s=#999999;b=1" g="840,2180,150,55" v="6-N 訊息編號"/>
<c id="p16c_tv10" st="f=#ffffff;s=#999999" g="990,2180,610,55" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…"/>
<c id="p16c_tk11" st="f=#ffffff;s=#999999;b=1" g="840,2235,150,71" v="結束碼 0／1／2／3"/>
<c id="p16c_tv11" st="f=#ffffff;s=#999999" g="990,2235,610,71" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"/>
</page>
```
